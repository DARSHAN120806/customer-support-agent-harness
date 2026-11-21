"""The event log: a record of everything the agent does.

Every model call, tool call, rewritten or blocked reply, and ticket is written
as one line of JSON to a log file (the "JSON Lines" format). One line is one
event, so the file is easy to read back with a script, load into a spreadsheet,
or feed to a dashboard.

Every line has the same first fields:

    v                 version of this format
    ts                when it happened (UTC)
    event             what happened, e.g. "model_call" or "ticket_created"
    conversation_id   the same for every event of one conversation
    customer_ref      a code that stands for the customer, never their email
    turn              which customer message this belongs to (1, 2, 3, ...)

Personal data is masked at the last moment, inside `EventLogger.log`, so no
caller can forget to do it: emails, phone numbers, and street addresses are
replaced before a line is written.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA_VERSION = 1

# The event names. Scripts that read the log can rely on these.
CONVERSATION_START = "conversation_start"
TURN_START = "turn_start"  # a customer message arrived
MODEL_CALL = "model_call"
TOOL_CALL = "tool_call"
REPLY_REWRITE = "reply_rewrite"  # a draft failed a check and the model was asked to redo it
REPLY_BLOCKED = "reply_blocked"  # a reply was withheld from the customer
TICKET_CREATED = "ticket_created"
REFUND_REQUEST = "refund_request"  # a refund or return request was checked by the rules
TURN_END = "turn_end"  # the reply was sent
RETRY = "retry"  # a call failed for a temporary reason and is being tried again
ERROR = "error"  # a call failed for good (after any retries)

EMAIL_MASK = "[EMAIL]"
PHONE_MASK = "[PHONE]"
NUMBER_MASK = "[NUMBER]"
ADDRESS_MASK = "[ADDRESS]"

# Long text is cut so one event cannot make the log file huge.
MAX_TEXT_LENGTH = 4000

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
# A run of digits with the usual phone separators. It must not start in the
# middle of a word or code, so order IDs (JL-10231), tracking numbers
# (TRK7002317785), and ticket numbers (TCK-20261113-A8C008) are left alone.
_DIGIT_RUN = re.compile(r"(?<![\w-])\+?\(?\d[\d \t().-]{6,}\d(?![\w-]*[A-Za-z])")
# A date, optionally followed by the hour: "2026-06-21" or "2026-06-21 10"
# (from "2026-06-21 10:39"). Dates and times are kept, never taken for phones.
_DATE_TIME = re.compile(r"\d{4}-\d{2}-\d{2}(?:[ T]\d{1,2})?")
_STREET_WORDS = (
    "Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way|Place|Pl|"
    "Terrace|Close|Crescent|Square|Highway|Hwy|Parkway|Pkwy"
)
# A street address: a house number, one to four capitalised words, a street
# word, and optionally a flat or suite.
_STREET_ADDRESS = re.compile(
    rf"\b\d{{1,6}}[A-Za-z]?\s+(?:[A-Z][\w'.-]*\s+){{1,4}}(?:{_STREET_WORDS})\b\.?"
    r"(?:,?\s*(?:Apt|Apartment|Suite|Ste|Unit|Flat|#)\.?\s*[\w-]+)?"
)
# Fields whose whole value is personal data, whatever it looks like.
_SENSITIVE_KEYS = {
    "email": EMAIL_MASK,
    "phone": PHONE_MASK,
    "mobile": PHONE_MASK,
    "address": ADDRESS_MASK,
    "street": ADDRESS_MASK,
    "postcode": ADDRESS_MASK,
    "zip": ADDRESS_MASK,
}


def mask_text(text: str) -> str:
    """Replace emails, phone numbers, and street addresses in a piece of text."""
    text = _EMAIL.sub(EMAIL_MASK, text)
    text = _STREET_ADDRESS.sub(ADDRESS_MASK, text)
    return _DIGIT_RUN.sub(_mask_digit_run, text)


def _mask_digit_run(match: re.Match[str]) -> str:
    text = match.group(0)
    if _DATE_TIME.fullmatch(text.strip()):
        return text
    digits = sum(character.isdigit() for character in text)
    # Dates such as 2026-11-07 have 8 digits and are kept. Phone numbers have 10
    # to 15 (or start with "+"). Anything longer could be a card or account number.
    if text.startswith("+") and digits >= 8 or 10 <= digits <= 15:
        return PHONE_MASK
    if digits > 15:
        return NUMBER_MASK
    return text


def mask_value(value: Any, key: str = "") -> Any:
    """Mask personal data anywhere inside a value: text, lists, and dictionaries."""
    if isinstance(value, dict):
        return {str(k): mask_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [mask_value(item, key) for item in value]
    if isinstance(value, str):
        for word, mask in _SENSITIVE_KEYS.items():
            if word in key.lower() and value:
                return mask
        return mask_text(value[:MAX_TEXT_LENGTH])
    return value


def new_conversation_id() -> str:
    return f"conv_{uuid.uuid4().hex[:12]}"


def load_or_create_salt(path: Path) -> str:
    """Read the secret used to turn emails into customer codes, creating it on
    first use. It lives next to the logs and is never committed."""
    try:
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
        path.parent.mkdir(parents=True, exist_ok=True)
        salt = secrets.token_hex(16)
        path.write_text(salt, encoding="utf-8")
        return salt
    except OSError:
        return secrets.token_hex(16)  # still works, but codes change between runs


def customer_ref(email: str, salt: str) -> str:
    """A code that is always the same for the same customer, but cannot be
    turned back into their email without the salt."""
    digest = hmac.new(salt.encode(), email.strip().lower().encode(), hashlib.sha256)
    return f"cust_{digest.hexdigest()[:12]}"


class EventLogger:
    """Writes the events of one conversation to the log file."""

    def __init__(self, path: Path, conversation_id: str, customer_ref: str) -> None:
        self._path = path
        self.conversation_id = conversation_id
        self.customer_ref = customer_ref
        self.turn = 0
        self._warned = False

    def log(self, event: str, **fields: Any) -> None:
        record = {
            "v": SCHEMA_VERSION,
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "event": event,
            "conversation_id": self.conversation_id,
            "customer_ref": self.customer_ref,
            "turn": self.turn,
            **mask_value(fields),
        }
        # A second pass over the finished line, in case personal data was hiding
        # somewhere the first pass does not look, such as a dictionary key.
        line = mask_text(json.dumps(record, ensure_ascii=False, default=str))
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as file:
                file.write(line + "\n")
        except OSError as error:
            # A logging problem must never stop a customer from getting a reply.
            if not self._warned:
                print(f"Warning: could not write to the log file: {error}", file=sys.stderr)
                self._warned = True


def retry_recorder(logger: "EventLogger | NullLogger", operation: str, **extra: Any):
    """Build the function that writes a `retry` event. It is handed to
    `call_with_retry`, which calls it before each wait."""

    def record(attempt: int, max_attempts: int, wait_seconds: float, error: Exception) -> None:
        logger.log(
            RETRY,
            operation=operation,
            attempt=attempt,
            max_attempts=max_attempts,
            wait_ms=round(wait_seconds * 1000),
            error_kind=getattr(error, "kind", type(error).__name__),
            error=str(error)[:300],
            **extra,
        )

    return record


def log_error(logger: "EventLogger | NullLogger", operation: str, error: Exception, **extra: Any) -> None:
    """Write an `error` event for a call that failed for good."""
    logger.log(
        ERROR,
        operation=operation,
        error_kind=getattr(error, "kind", type(error).__name__),
        retryable=bool(getattr(error, "retryable", False)),
        error=str(error)[:300],
        **extra,
    )


class NullLogger:
    """Used when logging is switched off, for example in small tests."""

    conversation_id = ""
    customer_ref = ""
    turn = 0

    def log(self, event: str, **fields: Any) -> None:
        pass


def read_events(path: Path, conversation_id: str | None = None) -> Iterator[dict[str, Any]]:
    """Read events back from a log file, optionally for one conversation only.
    Lines that are not valid JSON are skipped."""
    if not path.exists():
        return
    with path.open(encoding="utf-8") as file:
        for line in file:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if conversation_id is None or event.get("conversation_id") == conversation_id:
                yield event
