"""Tests for sign-in accounts: password hashing, the accounts file, the
wrong-password lock, admin tokens, and the script that makes test passwords."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from support_agent.config import ConfigError
from support_agent.web.accounts import (
    ADMIN,
    CUSTOMER,
    Account,
    AccountStore,
    AdminSessions,
    SignInLimiter,
    hash_password,
    verify_password,
)

ROOT = Path(__file__).resolve().parents[1]
FAST = 2**4  # low scrypt cost so the tests stay quick


# --- Hashing -------------------------------------------------------------------------


def test_a_password_is_stored_only_as_a_hash():
    stored = hash_password("juniper-lane-1", n=FAST)

    assert "juniper-lane-1" not in stored
    assert stored.startswith("scrypt$")
    assert verify_password("juniper-lane-1", stored)
    assert not verify_password("juniper-lane-2", stored)


def test_the_same_password_gets_a_different_hash_each_time():
    assert hash_password("same", n=FAST) != hash_password("same", n=FAST)


def test_the_default_hash_is_slow_enough():
    assert hash_password("x").split("$")[1] == str(2**14)


@pytest.mark.parametrize("stored", ["", "plain-text", "md5$1$2$3$4$5", "scrypt$x$8$1$AAAA$AAAA", "scrypt$16$8$1$!!$!!"])
def test_a_broken_stored_hash_never_matches(stored):
    assert not verify_password("anything", stored)


# --- The account store ---------------------------------------------------------------


@pytest.fixture
def store() -> AccountStore:
    return AccountStore(
        [
            Account("Priya.Nair@example.com", CUSTOMER, hash_password("p-pass", n=FAST)),
            Account("admin@juniperlane.example", ADMIN, hash_password("a-pass", n=FAST)),
        ]
    )


def test_the_right_password_finds_the_account(store):
    account = store.check(" PRIYA.NAIR@example.com ", "p-pass")

    assert account is not None and account.role == CUSTOMER
    assert store.check("admin@juniperlane.example", "a-pass").role == ADMIN
    assert len(store) == 2


def test_a_wrong_password_or_unknown_email_finds_nothing(store):
    assert store.check("priya.nair@example.com", "a-pass") is None  # someone else's password
    assert store.check("nobody@example.com", "p-pass") is None


def test_the_accounts_file_is_read(tmp_path):
    path = tmp_path / "accounts.json"
    path.write_text(
        json.dumps({"accounts": [{"email": "a@b.example", "role": "customer", "password_hash": hash_password("x", n=FAST)}]}),
        encoding="utf-8",
    )

    assert AccountStore.load(path).check("a@b.example", "x") is not None


def test_a_missing_accounts_file_says_how_to_make_one(tmp_path):
    with pytest.raises(ConfigError, match="create_test_passwords.py"):
        AccountStore.load(tmp_path / "missing.json")


@pytest.mark.parametrize(
    "content",
    ["not json", json.dumps({"wrong": []}), json.dumps({"accounts": [{"email": "a@b.example", "role": "boss", "password_hash": "x"}]})],
)
def test_a_broken_accounts_file_is_reported_plainly(tmp_path, content):
    path = tmp_path / "accounts.json"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ConfigError, match="accounts file"):
        AccountStore.load(path)


# --- The wrong-password lock ---------------------------------------------------------


def test_an_email_is_locked_after_too_many_wrong_passwords_then_unlocked():
    now = [0.0]
    limiter = SignInLimiter(max_failures=2, window_seconds=60, clock=lambda: now[0])

    limiter.record_failure("a@b.example")
    assert not limiter.is_locked("a@b.example")
    limiter.record_failure(" A@B.example ")
    assert limiter.is_locked("a@b.example")
    assert not limiter.is_locked("c@d.example")

    now[0] = 61
    assert not limiter.is_locked("a@b.example")


def test_a_successful_sign_in_clears_the_count():
    limiter = SignInLimiter(max_failures=2)
    limiter.record_failure("a@b.example")
    limiter.clear("a@b.example")
    limiter.record_failure("a@b.example")

    assert not limiter.is_locked("a@b.example")


# --- Admin tokens ----------------------------------------------------------------------


def test_admin_tokens_work_until_signed_out_or_idle():
    now = [0.0]
    admins = AdminSessions(idle_seconds=60, clock=lambda: now[0])
    first, second = admins.start(), admins.start()

    assert first != second and admins.is_valid(first)
    assert not admins.is_valid("made-up-token")
    admins.end(first)
    assert not admins.is_valid(first)

    now[0] = 61
    assert not admins.is_valid(second)


# --- The script ------------------------------------------------------------------------


def run_script(out: Path, *extra: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "create_test_passwords.py"), "--out", str(out), "--scrypt-n", str(FAST), *extra],
        capture_output=True, text=True, check=True, timeout=600,
    )
    return result.stdout


def test_the_script_makes_a_password_for_every_customer_and_the_admin(tmp_path):
    out = tmp_path / "private"
    run_script(out)

    customers = json.loads((ROOT / "data" / "orders.json").read_text(encoding="utf-8"))["customers"]
    accounts = json.loads((out / "accounts.json").read_text(encoding="utf-8"))["accounts"]
    with (out / "test_passwords.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(accounts) == len(rows) == len(customers) + 1
    assert [r["role"] for r in rows].count("admin") == 1
    # No password appears in the file the app reads.
    accounts_text = (out / "accounts.json").read_text(encoding="utf-8")
    assert not any(r["password"] in accounts_text for r in rows)
    # The passwords in the list really open their accounts.
    store = AccountStore.load(out / "accounts.json")
    for row in (rows[0], rows[-1]):
        assert store.check(row["email"], row["password"]).role == row["role"]

    before = (out / "accounts.json").read_text(encoding="utf-8")
    assert "already exist" in run_script(out)  # running again changes nothing
    assert (out / "accounts.json").read_text(encoding="utf-8") == before
