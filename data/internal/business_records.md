# Internal business records

Shop-wide figures from the synthetic data snapshot of 2026-11-20 09:00 ET. This folder is NOT searched by the assistant: sales, revenue, and staff details are not for customers. Built by scripts/import_synthetic_data.py; do not edit by hand.

## Data conventions

- Order IDs run JL-10001 to JL-11000 (orders placed 2026-06-01 to 2026-11-20). Orders are identified by order ID plus the email on the order.

- Order status values: processing, dispatched, delivered, cancelled, lost.

- Dispatch happens at 16:00 ET on the dispatch date. Orders placed before 14:00 ET on a business day dispatch that day; otherwise the next business day (Personalised Leather Notebook adds 2 business days).

- US public holidays used for business days: 2026-06-19, 2026-07-03, 2026-09-07, 2026-10-12, 2026-11-11, 2026-11-26, 2026-12-25.

- Related-record IDs: RT = return, RF = refund, WC = warranty claim, INV = carrier investigation, DMG = damaged package report, DS = refund dispute, ADR = address change, TK = support ticket.

## Support team roster

| Agent | Role | Hours (ET) |
|---|---|---|
| Priya N. | Support agent | Mon–Fri 9:00–18:00 |
| Marcus T. | Support agent | Mon–Fri 9:00–18:00 |
| Elena R. | Support agent | Mon–Fri 9:00–18:00 |
| Dan K. | Support agent | Mon–Fri 9:00–18:00 |
| Sofia L. | Support agent | Mon–Fri 9:00–18:00 |
| Helen W. (Senior) | Senior reviewer (refund disputes) | Mon–Fri 9:00–18:00 |

## Stock snapshot

| Product | SKU | Units in stock | Status | Back-in-stock sign-ups |
|---|---|---|---|---|
| Bluetooth Speaker Mini | SKU-EL-101 | 98 | In stock | — |
| Wireless Earbuds Pro | SKU-EL-102 | 118 | In stock | — |
| LED Desk Lamp | SKU-EL-103 | 201 | In stock | — |
| Electric Kettle 1.7L | SKU-EL-104 | 165 | In stock | — |
| Smart Plug (2-Pack) | SKU-EL-105 | 150 | In stock | — |
| Oak Side Table | SKU-FU-201 | 60 | In stock | — |
| Wool Throw Blanket | SKU-HW-301 | 0 | Out of stock | 2 |
| Cast Iron Skillet | SKU-HW-302 | 140 | In stock | — |
| Ceramic Pour-Over Coffee Set | SKU-HW-303 | 164 | In stock | — |
| Ceramic Planter Set | SKU-HW-304 | 9 | Low stock | — |
| Bamboo Cutting Board | SKU-HW-305 | 185 | In stock | — |
| Linen Napkins (Set of 4) | SKU-HW-306 | 155 | In stock | — |
| Adjustable Phone Stand | SKU-HW-307 | 196 | In stock | — |
| Scented Soy Candle | SKU-HW-308 | 156 | In stock | — |
| Personalised Leather Notebook | SKU-PE-401 | 41 | In stock | — |

## Sales summary by product (non-cancelled orders)

| Product | Units sold | Revenue |
|---|---|---|
| Bluetooth Speaker Mini | 170 | $6,798.30 |
| Wireless Earbuds Pro | 168 | $13,272.00 |
| LED Desk Lamp | 133 | $4,588.50 |
| Electric Kettle 1.7L | 146 | $6,570.00 |
| Smart Plug (2-Pack) | 124 | $3,100.00 |
| Oak Side Table | 49 | $6,321.00 |
| Wool Throw Blanket | 91 | $6,188.00 |
| Cast Iron Skillet | 105 | $5,775.00 |
| Ceramic Pour-Over Coffee Set | 84 | $3,528.00 |
| Ceramic Planter Set | 100 | $3,200.00 |
| Bamboo Cutting Board | 136 | $3,264.00 |
| Linen Napkins (Set of 4) | 112 | $2,072.00 |
| Adjustable Phone Stand | 95 | $1,425.00 |
| Scented Soy Candle | 173 | $2,076.00 |
| Personalised Leather Notebook | 77 | $2,233.00 |
| Juniper Lane Gift Card | 66 | $4,100.00 |

## Monthly summary

| Month | Orders placed | Cancelled | Revenue (non-cancelled) |
|---|---|---|---|
| 2026-06 | 177 | 9 | $14,880.83 |
| 2026-07 | 181 | 12 | $14,202.81 |
| 2026-08 | 183 | 9 | $14,632.89 |
| 2026-09 | 184 | 6 | $14,137.41 |
| 2026-10 | 184 | 12 | $13,486.74 |
| 2026-11 | 91 | 7 | $6,822.51 |

## Refund summary by type

| Type | Refunds | Total net |
|---|---|---|
| Cancelled before dispatch | 55 | $5,120.68 |
| Damaged on arrival | 8 | $369.42 |
| Package confirmed lost / not received | 15 | $930.88 |
| Return — change of mind | 126 | $5,043.88 |
| Return — faulty | 9 | $521.43 |
| Return — wrong item received | 1 | $28.99 |
| Warranty — repair/replacement not possible | 4 | $519.00 |

## Returns summary

| Kind | Count |
|---|---|
| com | 149 |
| denied_candle | 3 |
| denied_gift | 1 |
| denied_late | 26 |
| denied_personal | 4 |
| fault | 10 |
| wrong | 7 |

## Shipping summary

| Metric | Value |
|---|---|
| Orders dispatched | 879 |
| Orders awaiting dispatch | 4 |
| Carrier: FedEx | 249 |
| Carrier: UPS | 354 |
| Carrier: USPS | 276 |
| Status: Delivered | 782 |
| Status: Delivered (late) | 37 |
| Status: Delivered per carrier — customer reports not received | 22 |
| Status: In transit | 22 |
| Status: In transit — past estimate | 1 |
| Status: Lost in transit | 15 |

## Warranty summary

| Status / outcome | Claims |
|---|---|
| Approved / repair | 4 |
| Approved / replace | 3 |
| Completed / refund | 3 |
| Completed / repair | 15 |
| Completed / replace | 15 |
| Product received / repair | 1 |
| Product received / replace | 1 |
| Refund approved / refund | 1 |
| Rejected / rejected | 31 |
| Under review / rejected | 3 |
| Under review / replace | 2 |

## Expected outcomes of claims still under review (not decided; never shown to customers)

| Claim | Order ID | Expected outcome |
|---|---|---|
| WC-40075 | JL-10639 | Cracked casing from a drop (accidental damage) |
| WC-40076 | JL-10793 | Replacement pending |
| WC-40077 | JL-10837 | Scratches and fading (normal wear and tear) |
| WC-40078 | JL-10861 | Replacement pending |
| WC-40079 | JL-10870 | Housing opened — unauthorised repair |

## Warranty claims with no matching order

| Claim | Order ID | Email | Product | Delivered | Warranty | Warranty ends | Filed | Fault reported | Evidence | Status | Decision date | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WC-40005 | — | not found | Electric Kettle 1.7L | — | None | — | 2026-08-07 | Stopped working | Photos | Rejected | 2026-08-11 | No order found — product not bought from Juniper Lane Goods |
| WC-40008 | — | not found | Electric Kettle 1.7L | — | None | — | 2026-08-11 | Stopped working | Photos | Rejected | 2026-08-13 | No order found — product not bought from Juniper Lane Goods |
| WC-40040 | — | not found | Oak Side Table | — | None | — | 2026-10-09 | Stopped working | Photos | Rejected | 2026-10-14 | No order found — product not bought from Juniper Lane Goods |
| WC-40042 | — | not found | Electric Kettle 1.7L | — | None | — | 2026-10-10 | Stopped working | Photos | Rejected | 2026-10-14 | No order found — product not bought from Juniper Lane Goods |

## Support tickets not tied to an order

| Ticket | Created (ET) | Channel | Category | Order ID | Email | Status | Assigned to | Summary |
|---|---|---|---|---|---|---|---|---|
| TK-60135 | 2026-08-07 13:15 | Email | Warranty claim | — | claimant562@mailbox.example | Closed | Sofia L. | Electric Kettle 1.7L — Stopped working |
| TK-60146 | 2026-08-11 20:13 | Assistant chat | Warranty claim | — | claimant953@mailbox.example | Closed | Sofia L. | Electric Kettle 1.7L — Stopped working |
| TK-60342 | 2026-10-09 15:23 | Email | Warranty claim | — | claimant319@mailbox.example | Closed | Sofia L. | Oak Side Table — Stopped working |
| TK-60350 | 2026-10-10 18:12 | Assistant chat | Warranty claim | — | claimant793@mailbox.example | Closed | Marcus T. | Electric Kettle 1.7L — Stopped working |
