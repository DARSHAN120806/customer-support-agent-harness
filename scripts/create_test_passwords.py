"""Create a test password for every customer, plus one admin account.

Run once from the project folder:

    .venv/Scripts/python scripts/create_test_passwords.py

It writes two files into private/, a folder git never commits:

    private/accounts.json        what the web app reads: emails, roles and
                                 password HASHES (never the passwords)
    private/test_passwords.csv   the passwords themselves, for you to test with

Every password is random, so each copy of the project gets its own. Running
the script again keeps every existing password and only adds accounts that are
missing (such as the support staff); --force makes new passwords for everyone.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import secrets
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from support_agent.web.accounts import ADMIN, CUSTOMER, SCRYPT_N, STAFF, hash_password  # noqa: E402

PRIVATE = ROOT / "private"
ADMIN_EMAIL = "admin@juniperlane.example"
ADMIN_PERSON = (ADMIN_EMAIL, "Shop admin", ADMIN, "JLS-100")
# The company's support people (made up). They sign in to the admin panel and
# answer tickets; their name and staff ID are shown with every reply.
STAFF_PEOPLE = [
    ("asha.rao@juniperlane.example", "Asha Rao", STAFF, "JLS-101"),
    ("tom.becker@juniperlane.example", "Tom Becker", STAFF, "JLS-102"),
    ("mei.lin@juniperlane.example", "Mei Lin", STAFF, "JLS-103"),
]
COLUMNS = ["email", "name", "role", "staff_id", "password"]
# Shown at the end so you can sign in straight away.
DEMO_EMAILS = ["priya.nair@example.com", "marcus.bell@example.com"]


def new_password() -> str:
    """Twelve random letters and digits, easy to copy, impossible to guess."""
    alphabet = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O, 1/l/I
    return "".join(secrets.choice(alphabet) for _ in range(12))


def write_files(accounts_file: Path, passwords_file: Path, rows: list[dict[str, str]], hashes: dict[str, str]) -> None:
    accounts = [
        {"email": r["email"], "role": r["role"], "password_hash": hashes[r["email"]],
         **({"name": r["name"], "staff_id": r["staff_id"]} if r["role"] != CUSTOMER else {})}
        for r in rows
    ]
    accounts_file.parent.mkdir(parents=True, exist_ok=True)
    # Both files are written as temporary copies first, then swapped in, the
    # password list first. If the list is open in another program (Excel locks
    # it), the swap fails before the accounts file changes, so the two files
    # never disagree.
    new_accounts = accounts_file.with_suffix(".json.new")
    new_passwords = passwords_file.with_suffix(".csv.new")
    new_accounts.write_text(json.dumps({"accounts": accounts}, indent=1), encoding="utf-8")
    with new_passwords.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows({c: r.get(c, "") for c in COLUMNS} for r in rows)
    try:
        os.replace(new_passwords, passwords_file)
    except PermissionError:
        new_accounts.unlink(missing_ok=True)
        new_passwords.unlink(missing_ok=True)
        raise SystemExit(f"{passwords_file} is open in another program (for example Excel). Close it and run this again. Nothing was changed.")
    os.replace(new_accounts, accounts_file)


def add_missing(accounts_file: Path, passwords_file: Path, scrypt_n: int) -> int:
    """Keep every existing account and password; add any staff (or admin
    details) that are missing."""
    data = json.loads(accounts_file.read_text(encoding="utf-8"))
    hashes = {a["email"]: a["password_hash"] for a in data["accounts"]}
    roles = {a["email"]: a["role"] for a in data["accounts"]}
    rows: dict[str, dict[str, str]] = {}
    if passwords_file.exists():
        with passwords_file.open(encoding="utf-8") as f:
            rows = {r["email"]: {c: r.get(c) or "" for c in COLUMNS} for r in csv.DictReader(f)}
    for email in hashes:  # accounts whose password is not in the list (should not happen)
        rows.setdefault(email, {"email": email, "name": "", "role": roles[email], "staff_id": "", "password": ""})

    added = []
    for email, name, role, staff_id in [ADMIN_PERSON, *STAFF_PEOPLE]:
        row = rows.get(email)
        if row is None:
            password = new_password()
            hashes[email] = hash_password(password, n=scrypt_n)
            rows[email] = {"email": email, "name": name, "role": role, "staff_id": staff_id, "password": password}
            added.append(email)
        else:
            row.update({"name": row["name"] or name, "role": role, "staff_id": row["staff_id"] or staff_id})
    write_files(accounts_file, passwords_file, list(rows.values()), hashes)
    if added:
        print(f"Added {len(added)} account(s): {', '.join(added)}. Their passwords are in {passwords_file}.")
    else:
        print(f"All accounts already exist in {accounts_file}. Use --force to make new passwords.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="Replace existing passwords with new ones.")
    parser.add_argument("--out", type=Path, default=PRIVATE, help="Folder to write into (default: private/).")
    # Only the tests lower this, so they run quickly. Never lower it for real use.
    parser.add_argument("--scrypt-n", type=int, default=SCRYPT_N, help=argparse.SUPPRESS)
    args = parser.parse_args()

    accounts_file = args.out / "accounts.json"
    passwords_file = args.out / "test_passwords.csv"
    if accounts_file.exists() and not args.force:
        return add_missing(accounts_file, passwords_file, args.scrypt_n)

    data = json.loads((ROOT / "data" / "orders.json").read_text(encoding="utf-8"))
    rows = [{"email": c["email"].lower(), "name": c["name"], "role": CUSTOMER, "staff_id": ""} for c in data["customers"]]
    rows += [{"email": e, "name": n, "role": r, "staff_id": i} for e, n, r, i in [ADMIN_PERSON, *STAFF_PEOPLE]]
    for row in rows:
        row["password"] = new_password()

    print(f"Hashing {len(rows)} passwords (this takes a little while)...")
    with ThreadPoolExecutor() as pool:
        hashed = list(pool.map(lambda r: hash_password(r["password"], n=args.scrypt_n), rows))
    write_files(accounts_file, passwords_file, rows, {r["email"]: h for r, h in zip(rows, hashed)})

    print(f"Wrote {accounts_file} and {passwords_file}.")
    print(f"Accounts to try first are in {passwords_file}:")
    for email in [ADMIN_EMAIL, STAFF_PEOPLE[0][0], *DEMO_EMAILS]:
        print(f"  {email}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
