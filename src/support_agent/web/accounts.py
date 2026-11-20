"""Sign-in accounts: customers and the shop's admin.

Passwords are never stored as they are typed. Each one is turned into a
"hash" with scrypt, a deliberately slow method built into Python, together
with a random "salt", so the stored text cannot be turned back into the
password, and two people with the same password still get different hashes.

The accounts file is made by scripts/create_test_passwords.py and lives in
private/, which is never committed to git.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ..config import ConfigError

CUSTOMER = "customer"
ADMIN = "admin"
ROLES = (CUSTOMER, ADMIN)

# scrypt settings: about 50 ms per check on a laptop, which is nothing for one
# sign-in but makes guessing millions of passwords very slow.
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
HASH_BYTES = 32


def hash_password(password: str, *, n: int = SCRYPT_N) -> str:
    """Return the stored form of a password: method, settings, salt and hash."""
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=n, r=SCRYPT_R, p=SCRYPT_P, dklen=HASH_BYTES)
    return "$".join(["scrypt", str(n), str(SCRYPT_R), str(SCRYPT_P), _b64(salt), _b64(digest)])


def verify_password(password: str, stored: str) -> bool:
    """True if the password matches the stored hash. Never raises on bad input."""
    try:
        method, n, r, p, salt, expected = stored.split("$")
        if method != "scrypt":
            return False
        digest = hashlib.scrypt(
            password.encode(), salt=_unb64(salt), n=int(n), r=int(r), p=int(p), dklen=HASH_BYTES
        )
    except (ValueError, TypeError):
        return False
    # compare_digest takes the same time however many characters match, so the
    # answer time gives nothing away.
    return hmac.compare_digest(digest, _unb64(expected))


@dataclass(frozen=True)
class Account:
    email: str
    role: str
    password_hash: str


class AccountStore:
    """All accounts, looked up by email (ignoring capitals and spaces)."""

    def __init__(self, accounts: list[Account]) -> None:
        self._by_email = {a.email.strip().lower(): a for a in accounts}
        # Checked when the email is unknown, so a wrong email takes as long as a
        # wrong password and the answer time does not reveal which emails exist.
        self._dummy_hash = hash_password(secrets.token_urlsafe(16))

    @classmethod
    def load(cls, path: Path) -> "AccountStore":
        if not path.exists():
            raise ConfigError(
                f"No sign-in accounts found at {path}. Create them once with: "
                ".venv/Scripts/python scripts/create_test_passwords.py"
            )
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            accounts = [
                Account(a["email"], a["role"], a["password_hash"]) for a in data["accounts"]
            ]
        except (ValueError, KeyError, TypeError) as error:
            raise ConfigError(f"The accounts file {path} could not be read ({error}).") from error
        if any(a.role not in ROLES for a in accounts):
            raise ConfigError(f"The accounts file {path} has an account with an unknown role.")
        return cls(accounts)

    def check(self, email: str, password: str) -> Account | None:
        """The account if the email and password match, otherwise None."""
        account = self._by_email.get(email.strip().lower())
        stored = account.password_hash if account else self._dummy_hash
        matches = verify_password(password, stored)
        return account if account and matches else None

    def __len__(self) -> int:
        return len(self._by_email)


class SignInLimiter:
    """Stops password guessing: after too many wrong passwords for one email,
    sign-in for that email is refused for a while, even with the right one."""

    def __init__(
        self,
        max_failures: int = 5,
        window_seconds: float = 15 * 60,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._max = max_failures
        self._window = window_seconds
        self._clock = clock
        self._failures: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def is_locked(self, email: str) -> bool:
        with self._lock:
            return len(self._recent(email)) >= self._max

    def record_failure(self, email: str) -> None:
        with self._lock:
            self._recent(email).append(self._clock())

    def clear(self, email: str) -> None:
        with self._lock:
            self._failures.pop(_key(email), None)

    def _recent(self, email: str) -> deque[float]:
        times = self._failures[_key(email)]
        while times and self._clock() - times[0] > self._window:
            times.popleft()
        return times


class AdminSessions:
    """Signed-in admins, by a random token. Tokens expire after an hour idle."""

    def __init__(self, idle_seconds: float = 3600, clock: Callable[[], float] = time.monotonic) -> None:
        self._last_used: dict[str, float] = {}
        self._idle = idle_seconds
        self._clock = clock
        self._lock = threading.Lock()

    def start(self) -> str:
        token = secrets.token_urlsafe(32)
        with self._lock:
            self._last_used[token] = self._clock()
        return token

    def is_valid(self, token: str) -> bool:
        with self._lock:
            last = self._last_used.get(token)
            if last is None or self._clock() - last > self._idle:
                self._last_used.pop(token, None)
                return False
            self._last_used[token] = self._clock()
            return True

    def end(self, token: str) -> None:
        with self._lock:
            self._last_used.pop(token, None)


def _key(email: str) -> str:
    return email.strip().lower()


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def _unb64(text: str) -> bytes:
    return base64.b64decode(text.encode("ascii"), validate=True)
