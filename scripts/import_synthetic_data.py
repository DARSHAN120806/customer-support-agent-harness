"""Build the shop's order data from the synthetic records.

    python scripts/import_synthetic_data.py           build the files
    python scripts/import_synthetic_data.py --check   only check they are up to date

Reads:
    data/source/base_orders.json              the original 8 customers and 16 orders
    data/source/synthetic_extension/*.md      the uploaded records (tables)

Writes:
    data/orders.json                    every customer and order, each order with its
                                        own refunds, returns, shipment, warranty
                                        claims, cases, and past tickets attached
    data/internal/business_records.md   shop-wide figures (sales, summaries, staff),
                                        which the assistant can never read

Why the records live in the order data and not in the searchable documents:
anything in data/knowledge_base/ can be read by every customer through the
search tool. Order data is only ever shown to the customer who owns the order,
because lookup_order checks the owner. So per-customer records belong here.

The build is deterministic: the same sources always give the same files, and
the tests check that the committed files match the sources.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"
EXTENSION = SOURCE / "synthetic_extension"
ORDERS_FILE = ROOT / "data" / "orders.json"
INTERNAL_FILE = ROOT / "data" / "internal" / "business_records.md"
SNAPSHOT = "2026-11-20 09:00 ET"

# Catalogue categories, matching the product table in company_overview.md.
CATEGORY = {
    "Bluetooth Speaker Mini": "electronics",
    "Wireless Earbuds Pro": "electronics",
    "LED Desk Lamp": "electronics",
    "Electric Kettle 1.7L": "electronics",
    "Smart Plug (2-Pack)": "electronics",
    "Oak Side Table": "furniture",
    "Wool Throw Blanket": "homeware",
    "Cast Iron Skillet": "homeware",
    "Ceramic Pour-Over Coffee Set": "homeware",
    "Ceramic Planter Set": "homeware",
    "Bamboo Cutting Board": "homeware",
    "Linen Napkins (Set of 4)": "homeware",
    "Adjustable Phone Stand": "homeware",
    "Scented Soy Candle": "homeware",
    "Personalised Leather Notebook": "personalised",
    "Juniper Lane Gift Card": "gift_card",
}
PRICE = {
    "Bluetooth Speaker Mini": 39.99,
    "Wireless Earbuds Pro": 79.00,
    "LED Desk Lamp": 34.50,
    "Electric Kettle 1.7L": 45.00,
    "Smart Plug (2-Pack)": 25.00,
    "Oak Side Table": 129.00,
    "Wool Throw Blanket": 68.00,
    "Cast Iron Skillet": 55.00,
    "Ceramic Pour-Over Coffee Set": 42.00,
    "Ceramic Planter Set": 32.00,
    "Bamboo Cutting Board": 24.00,
    "Linen Napkins (Set of 4)": 18.50,
    "Adjustable Phone Stand": 15.00,
    "Scented Soy Candle": 12.00,
    "Personalised Leather Notebook": 29.00,
}

# What each warranty claim status means, in words the assistant can pass on.
# The status labels are short, and the assistant once read "Approved — awaiting
# product" as "a replacement is on its way". Each claim gets its meaning next to
# its status. Keep these in line with the "Warranty claim statuses" section of
# data/knowledge_base/warranty.md.
CLAIM_STATUS_MEANING = {
    "Under review": (
        "The support team is reviewing the claim. No decision has been made yet. "
        "Reviews take up to 3 business days."
    ),
    "Approved — awaiting product": (
        "The claim was approved and a free return label has been emailed to the customer. "
        "The customer now needs to send the product back. Nothing has been repaired, "
        "replaced, or refunded yet: that happens after the product arrives."
    ),
    "Product received — in progress": (
        "The product has arrived and the team is repairing it, or arranging a "
        "replacement or refund. Nothing has been sent back to the customer yet."
    ),
    "Completed — repaired and returned": "The product was repaired and sent back to the customer.",
    "Completed — replacement sent": (
        "A replacement was sent to the customer; the outcome gives the dispatch date and "
        "tracking number. The replacement is covered for the rest of the original warranty "
        "period or for 90 days, whichever is longer."
    ),
    "Completed — refund sent": (
        "The product could not be repaired or replaced, so it was refunded; the outcome "
        "gives the refund ID."
    ),
    "Refund approved — payment pending": (
        "The product could not be repaired or replaced, so a refund was approved. The "
        "payment has not been sent yet; approved refunds are sent within 5–7 business days."
    ),
    "Rejected": (
        "The claim was not accepted because the fault is not covered by the warranty; "
        "the outcome gives the reason."
    ),
}

# --- Reading the Markdown tables ------------------------------------------------------


def clean_cell(cell: str) -> str | None:
    cell = re.sub(r"\\(.)", r"\1", cell.strip())  # undo leftover escapes such as "\&"
    return None if cell in ("", "—", "-") else cell


def read_tables(path: Path) -> dict[str, list[dict[str, str | None]]]:
    """Every table in a file, keyed by the heading above it."""
    tables: dict[str, list[dict[str, str | None]]] = {}
    heading = ""
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            heading, header = line.lstrip("#").strip(), None
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None:
                header = cells
                tables[heading] = []
            elif not set("".join(cells)) <= set("-: "):
                if len(cells) != len(header):
                    raise ValueError(f"{path.name}, '{heading}': row has {len(cells)} cells: {line[:80]}")
                tables[heading].append({h: clean_cell(c) for h, c in zip(header, cells)})
        else:
            header = None
    return tables


def money(text: str | None) -> float | None:
    if text is None:
        return None
    match = re.fullmatch(r"\$([\d,]+(?:\.\d+)?)", text.strip())
    if not match:
        raise ValueError(f"not an amount: {text!r}")
    return round(float(match.group(1).replace(",", "")), 2)


def money_or_text(text: str | None) -> float | str | None:
    """Amounts become numbers; words such as "Free" are kept as they are."""
    try:
        return money(text)
    except ValueError:
        return text


def day(text: str | None) -> str | None:
    """'2026-06-01 14:33' -> '2026-06-01'."""
    return None if text is None else date.fromisoformat(text.split()[0]).isoformat()


def time_of_day(text: str | None) -> str | None:
    return None if text is None or " " not in text else f"{text.split()[1]} ET"


def drop_none(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if value is not None}


# --- Converting each kind of record ---------------------------------------------------

ITEM = re.compile(r"^(?P<name>.+?) ×(?P<qty>\d+)(?: \((?P<extra>.+)\))?$")


def parse_items(text: str) -> list[dict[str, Any]]:
    items = []
    for part in text.split(";"):
        match = ITEM.match(part.strip())
        if not match:
            raise ValueError(f"cannot read item {part!r}")
        name, extra = match["name"], match["extra"]
        item: dict[str, Any] = {"name": name, "category": CATEGORY[name], "quantity": int(match["qty"])}
        if name == "Juniper Lane Gift Card":
            value = money(re.fullmatch(r"(\$[\d.,]+) card", extra).group(1))
            item["name"] = f"Juniper Lane Gift Card ${value:g}"
            item["unit_price"] = value
        else:
            item["unit_price"] = PRICE[name]
            if extra:
                emboss = re.fullmatch(r'emboss "(.+)"', extra)
                if not emboss:
                    raise ValueError(f"unexpected detail {extra!r}")
                item["embossing"] = emboss.group(1)
        items.append(item)
    return items


SHIPPING_METHOD = {"Standard": "standard", "Express": "express", "Email (digital)": "digital"}


def convert_order(row: dict, customer_id: str) -> dict[str, Any]:
    items = parse_items(row["Items"])
    order = {
        "order_id": row["Order ID"],
        "customer_id": customer_id,
        "placed_on": day(row["Placed (ET)"]),
        "placed_at": time_of_day(row["Placed (ET)"]),
        "status": row["Status"],
        "items": items,
        "subtotal": money(row["Subtotal"]),
        "shipping_method": SHIPPING_METHOD[row["Shipping option"]],
        "shipping_cost": money(row["Shipping"]),
        "total": money(row["Total"]),
        "payment_method": row["Payment"],
        "ship_to": row["Ship to"],
        "notes": row["Notes"],
    }
    # Every amount is checked, so a mistake in the source is caught here.
    computed = round(sum(i["quantity"] * i["unit_price"] for i in items), 2)
    if computed != order["subtotal"]:
        raise ValueError(f"{row['Order ID']}: items add up to {computed}, subtotal says {order['subtotal']}")
    if round(order["subtotal"] + order["shipping_cost"], 2) != order["total"]:
        raise ValueError(f"{row['Order ID']}: subtotal + shipping != total")
    return order


def snake(record: dict, renames: dict[str, str], money_fields=(), date_fields=(), drop=("Email",)) -> dict:
    """Rename columns, convert amounts and dates, and leave out empty values."""
    out: dict[str, Any] = {}
    for column, value in record.items():
        if column in drop:
            continue
        key = renames.get(column) or re.sub(r"[^a-z0-9]+", "_", column.lower()).strip("_")
        if column in money_fields:
            value = money_or_text(value)
        elif column in date_fields:
            value = day(value)
        out[key] = value
    return drop_none(out)


# --- Building everything ----------------------------------------------------------------


def build() -> tuple[str, str]:
    base = json.loads((SOURCE / "base_orders.json").read_text(encoding="utf-8"))
    company = read_tables(EXTENSION / "company_overview.md")
    faq = read_tables(EXTENSION / "faq.md")
    refunds = read_tables(EXTENSION / "refunds.md")
    returns = read_tables(EXTENSION / "returns.md")
    shipping = read_tables(EXTENSION / "shipping.md")
    warranty = read_tables(EXTENSION / "warranty.md")

    # Customers: the original eight keep C001-C008; new ones follow in email order.
    customers = list(base["customers"])
    known = {c["email"] for c in customers}
    directory = sorted(company["Customer directory"], key=lambda r: r["Email"])
    id_by_email = {c["email"]: c["customer_id"] for c in customers}
    for number, row in enumerate(directory, start=len(customers) + 1):
        if row["Email"] in known:
            raise ValueError(f"customer {row['Email']} already exists")
        customer = drop_none(
            {
                "customer_id": f"C{number:04d}",
                "name": row["Name"],
                "email": row["Email"],
                "city": f"{row['City']}, {row['State']}",
                "account_created": row["Account created"],
                "newsletter": row["Newsletter"] == "Yes",
            }
        )
        customers.append(customer)
        id_by_email[row["Email"]] = customer["customer_id"]

    orders: dict[str, dict[str, Any]] = {}
    email_by_order: dict[str, str] = {}
    for row in company["Order ledger"]:
        if row["Email"] not in id_by_email:
            raise ValueError(f"{row['Order ID']}: unknown customer {row['Email']}")
        orders[row["Order ID"]] = convert_order(row, id_by_email[row["Email"]])
        email_by_order[row["Order ID"]] = row["Email"]
    clashes = set(orders) & {o["order_id"] for o in base["orders"]}
    if clashes:
        raise ValueError(f"order IDs used twice: {sorted(clashes)}")

    def attach(order_id: str | None, key: str, record: dict, email: str | None = None) -> bool:
        """Attach a record to its order. Returns False if it has no order."""
        if order_id is None:
            return False
        if order_id not in orders:
            raise ValueError(f"{key}: unknown order {order_id}")
        if email is not None and email != email_by_order[order_id]:
            raise ValueError(f"{key} for {order_id}: email does not match the order")
        orders[order_id].setdefault(key, []).append(record)
        return True

    for row in shipping["Shipment ledger"]:
        order = orders[row["Order ID"]]
        order.update(
            drop_none(
                {
                    "carrier": row["Carrier"],
                    "tracking_number": row["Tracking number"],
                    "dispatched_on": day(row["Dispatched (ET)"]),
                    "estimated_delivery": row["Estimated delivery"],
                    "delivered_on": day(row["Delivered"]),
                    "shipment_status": row["Shipment status"],
                }
            )
        )
    for row in shipping["Orders awaiting dispatch (status: processing)"]:
        orders[row["Order ID"]].update(
            {
                "scheduled_dispatch": row["Scheduled dispatch"] + " ET",
                "can_still_cancel_or_change_address": row["Can still be cancelled / address changed"] == "Yes",
            }
        )

    for row in refunds["Refund ledger"]:
        attach(
            row["Order ID"],
            "refunds",
            snake(
                row,
                {"Refund": "refund_id", "Order ID": "", "Item": "item_refund", "Approved": "approved_on", "Sent": "sent_on"},
                money_fields=("Item", "Shipping refunded", "Return fee", "Restocking fee", "Net refund"),
                drop=("Email", "Order ID"),
            ),
            row["Email"],
        )
    for row in refunds["Refund disputes"]:
        attach(
            row["Order ID"],
            "refund_disputes",
            snake(row, {"Dispute": "dispute_id", "Refund": "refund_id", "Filed": "filed_on", "Decision date": "decided_on"},
                  money_fields=("Additional refund",), drop=("Order ID",)),
        )
    kinds = {"com": "change of mind", "fault": "faulty", "wrong": "wrong item received"}
    for row in returns["Return requests"]:
        record = snake(
            row,
            {"Return": "return_id", "Item": "items", "Delivered": "delivered_on", "Requested": "requested_on",
             "Day #": "requested_on_day", "Label emailed": "label_emailed_on", "Received": "received_on",
             "Refund": "refund_id"},
            money_fields=("Return shipping",),
            drop=("Email", "Order ID"),
        )
        record["kind"] = kinds.get(row["Kind"], (row["Kind"] or "").replace("denied ", "denied: "))
        if "requested_on_day" in record:
            record["requested_on_day"] = int(record["requested_on_day"])
        attach(row["Order ID"], "returns", record, row["Email"])
    for row in shipping["Carrier investigations"]:
        attach(row["Order ID"], "carrier_investigations",
               snake(row, {"Case": "case_id", "Opened": "opened_on", "Closed": "closed_on"}, drop=("Order ID",)))
    for row in shipping["Damaged package reports (must be reported within 7 days of delivery)"]:
        attach(row["Order ID"], "damage_reports",
               snake(row, {"Case": "case_id", "Delivered": "", "Reported": "reported_on"}, drop=("Order ID", "Delivered")))
    for row in shipping["Address change requests"]:
        attach(row["Order ID"], "address_change_requests",
               snake(row, {"Request": "request_id", "Requested (ET)": "requested_at"}, drop=("Order ID",)))

    unlinked_claims, unlinked_tickets, pending_outcomes = [], [], []
    for row in warranty["Warranty claims"]:
        record = snake(
            row,
            {"Claim": "claim_id", "Delivered": "delivered_on", "Warranty ends": "warranty_ends_on",
             "Filed": "filed_on", "Decision date": "decided_on", "Warranty": "warranty_length"},
            drop=("Email", "Order ID", "Delivered"),
        )
        if record["status"] == "Under review" and "outcome" in record:
            # Not decided yet: the source lists the expected decision, which the
            # customer must not be told before the team decides. Kept internal.
            pending_outcomes.append({"Claim": record["claim_id"], "Order ID": row["Order ID"],
                                     "Expected outcome": record.pop("outcome")})
        if record["status"] not in CLAIM_STATUS_MEANING:
            raise ValueError(f"{record['claim_id']}: no meaning written for status {record['status']!r}")
        # Placed right after the status, so the two are read together.
        record = {
            **{k: v for k, v in record.items() if k not in ("decided_on", "outcome")},
            "status_meaning": CLAIM_STATUS_MEANING[record["status"]],
            **{k: record[k] for k in ("decided_on", "outcome") if k in record},
        }
        if not attach(row["Order ID"], "warranty_claims", record, row["Email"]):
            unlinked_claims.append(row)
    for row in faq["Support ticket log"]:
        record = snake(row, {"Ticket": "ticket_id", "Created (ET)": "created_at"}, drop=("Email", "Order ID"))
        if not attach(row["Order ID"], "past_support_tickets", record, row["Email"]):
            unlinked_tickets.append(row)

    all_orders = list(base["orders"]) + [drop_none(orders[k]) for k in sorted(orders)]
    data = {
        "_note": (
            "Fictional data for the Juniper Lane Goods support agent. All people, emails, and "
            "tracking numbers are made up. Built by scripts/import_synthetic_data.py from "
            f"data/source/; records reflect the snapshot of {SNAPSHOT}. Do not edit by hand."
        ),
        "customers": customers,
        "orders": all_orders,
    }
    orders_text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    internal_text = build_internal(
        company, refunds, returns, shipping, warranty, unlinked_claims, unlinked_tickets, pending_outcomes
    )
    return orders_text, internal_text


def table_md(rows: list[dict], columns: list[str] | None = None) -> str:
    columns = columns or list(rows[0])
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    lines += ["| " + " | ".join(row.get(c) or "—" for c in columns) + " |" for row in rows]
    return "\n".join(lines)


def build_internal(
    company, refunds, returns, shipping, warranty, unlinked_claims, unlinked_tickets, pending_outcomes
) -> str:
    conventions = (EXTENSION / "company_overview.md").read_text(encoding="utf-8")
    conventions = conventions.split("## Data conventions", 1)[1].split("\n## ", 1)[0].strip()
    parts = [
        "# Internal business records",
        "",
        f"Shop-wide figures from the synthetic data snapshot of {SNAPSHOT}. This folder is "
        "NOT searched by the assistant: sales, revenue, and staff details are not for "
        "customers. Built by scripts/import_synthetic_data.py; do not edit by hand.",
        "",
        "## Data conventions",
        "",
        conventions,
        "",
    ]
    for title, rows in [
        ("Support team roster", company["Support team roster"]),
        ("Stock snapshot", company["Stock snapshot"]),
        ("Sales summary by product (non-cancelled orders)", company["Sales summary by product (non-cancelled orders)"]),
        ("Monthly summary", company["Monthly summary"]),
        ("Refund summary by type", refunds["Refund summary by type"]),
        ("Returns summary", returns["Returns summary"]),
        ("Shipping summary", shipping["Shipping summary"]),
        ("Warranty summary", warranty["Warranty summary"]),
        ("Expected outcomes of claims still under review (not decided; never shown to customers)", pending_outcomes),
        ("Warranty claims with no matching order", unlinked_claims),
        ("Support tickets not tied to an order", unlinked_tickets),
    ]:
        parts += [f"## {title}", "", table_md(rows) if rows else "None.", ""]
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="Only check the files are up to date.")
    args = parser.parse_args(argv)
    orders_text, internal_text = build()
    if args.check:
        stale = [
            str(path)
            for path, text in ((ORDERS_FILE, orders_text), (INTERNAL_FILE, internal_text))
            if not path.exists() or path.read_text(encoding="utf-8") != text
        ]
        print("Out of date: " + ", ".join(stale) if stale else "Up to date.")
        return 1 if stale else 0
    INTERNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    ORDERS_FILE.write_text(orders_text, encoding="utf-8")
    INTERNAL_FILE.write_text(internal_text, encoding="utf-8")
    data = json.loads(orders_text)
    print(f"Wrote {ORDERS_FILE.name}: {len(data['customers'])} customers, {len(data['orders'])} orders.")
    print(f"Wrote {INTERNAL_FILE.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
