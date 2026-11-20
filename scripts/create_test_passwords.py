"""Create a test password for every customer, plus one admin account.

Run once from the project folder:

    .venv/Scripts/python scripts/create_test_passwords.py

It writes two files into private/, a folder git never commits:

    private/accounts.json        what the web app reads: emails, roles and
                                 password HASHES (never the passwords)
    private/test_passwords.csv   the passwords themselves, for you to test with

Every password is random, so each copy of the project gets its own. Running
the script again does nothing unless you add --force, which makes new ones.
"""

from __future__ import annotations

import argparse
import csv
import json
import secrets
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from support_agent.web.accounts import ADMIN, CUSTOMER, SCRYPT_N, hash_password  # noqa: E402

PRIVATE = ROOT / "private"
ADMIN_EMAIL = "admin@juniperlane.example"
# Shown at the end so you can sign in straight away.
DEMO_EMAILS = ["priya.nair@example.com", "marcus.bell@example.com"]


def new_password() -> str:
    """Twelve random letters and digits, easy to copy, impossible to guess."""
    alphabet = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O, 1/l/I
    return "".join(secrets.choice(alphabet) for _ in range(12))


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
        print(f"Accounts already exist in {accounts_file}. Use --force to make new passwords.")
        return 0

    data = json.loads((ROOT / "data" / "orders.json").read_text(encoding="utf-8"))
    people = [(c["email"].lower(), c["name"], CUSTOMER) for c in data["customers"]]
    people.append((ADMIN_EMAIL, "Shop admin", ADMIN))
    passwords = [new_password() for _ in people]

    print(f"Hashing {len(people)} passwords (this takes a little while)...")
    with ThreadPoolExecutor() as pool:
        hashes = list(pool.map(lambda pw: hash_password(pw, n=args.scrypt_n), passwords))

    args.out.mkdir(parents=True, exist_ok=True)
    accounts = [
        {"email": email, "role": role, "password_hash": hashed}
        for (email, _, role), hashed in zip(people, hashes)
    ]
    accounts_file.write_text(json.dumps({"accounts": accounts}, indent=1), encoding="utf-8")
    with passwords_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "name", "role", "password"])
        writer.writerows((email, name, role, pw) for (email, name, role), pw in zip(people, passwords))

    print(f"Wrote {accounts_file} and {passwords_file}.")
    print(f"Accounts to try first are in {passwords_file}:")
    for email in [ADMIN_EMAIL, *DEMO_EMAILS]:
        print(f"  {email}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
