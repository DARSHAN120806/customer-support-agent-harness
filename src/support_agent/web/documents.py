"""The shop documents, as the admin panel edits them.

The documents are the Markdown files in data/knowledge_base/: everything the
assistant may answer from, and (for company_overview.md) the products and stock
the shop page shows. Every save keeps the text from before it in
private/document_history/, so any change can be undone.

Before a save, the new text is checked:
- it must not add customer details (emails, order numbers, tracking numbers),
  because every customer can search these documents;
- a section must not be so long that the search model cannot read it;
- the product and stock tables must still be readable by the shop page;
- sections that must stay in step with the order records are left alone.
"""

from __future__ import annotations

import hashlib
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..catalogue import OVERVIEW_FILE, load_catalogue
from ..config import ConfigError

NAME = re.compile(r"^[a-z0-9_]+\.md$")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
SHOP_EMAIL_DOMAIN = "@juniperlane.example"
# A section longer than this still works, but the search finds long sections
# less reliably; far below the search model's real limit.
SECTION_WARN_CHARS = 4000
# Beyond this a section risks being cut off by the search model.
SECTION_MAX_CHARS = 20000
DOCUMENT_MAX_CHARS = 200_000
HISTORY_KEPT = 50
# Sections whose text must match data kept elsewhere, so they are not edited here.
PROTECTED_SECTIONS = {
    "warranty.md": {
        "Warranty claim statuses": (
            "is kept word for word in step with the warranty records in the order data, so it "
            "cannot be changed here"
        ),
    },
}


class DocumentError(Exception):
    """A document that does not exist, or a save that was refused."""

    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


def version_of(text: str) -> str:
    """A short fingerprint of a text, to notice when someone else saved first."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def sections(text: str) -> list[dict[str, Any]]:
    """The "## " sections of a document, with their sizes."""
    found: list[dict[str, Any]] = []
    for line in text.splitlines():
        if line.startswith("## "):
            found.append({"heading": line[3:].strip(), "chars": 0, "text": ""})
        elif found:
            found[-1]["text"] += line + "\n"
    for section in found:
        section["text"] = section["text"].strip()
        section["chars"] = len(section["text"])
    return found


def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


class DocumentStore:
    def __init__(self, folder: Path, history: Path) -> None:
        self._folder = folder
        self._history = history

    # --- Reading ---------------------------------------------------------------------

    def _path(self, name: str) -> Path:
        path = self._folder / name
        if not NAME.match(name) or not path.is_file():
            raise DocumentError("No such document.", status=404)
        return path

    def list(self) -> list[dict[str, Any]]:
        result = []
        for path in sorted(self._folder.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            result.append(
                {
                    "name": path.name,
                    "title": title_of(text, path.stem),
                    "sections": len(sections(text)),
                    "chars": len(text),
                    "updated_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                }
            )
        return result

    def read(self, name: str) -> dict[str, Any]:
        path = self._path(name)
        text = path.read_text(encoding="utf-8")
        return {
            "name": name,
            "title": title_of(text, path.stem),
            "text": text,
            "version": version_of(text),
            "updated_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
            "sections": [{"heading": s["heading"], "chars": s["chars"]} for s in sections(text)],
            "protected": sorted(PROTECTED_SECTIONS.get(name, {})),
            "history": self.history(name),
        }

    def history(self, name: str) -> list[dict[str, Any]]:
        folder = self._history / name.removesuffix(".md")
        if not folder.is_dir():
            return []
        entries = []
        for path in sorted(folder.glob("*.md"), reverse=True):
            stamp = path.stem
            try:
                saved = datetime.strptime(stamp, "%Y%m%dT%H%M%S%fZ").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            entries.append({"id": stamp, "saved_at": saved.isoformat(timespec="seconds"), "chars": path.stat().st_size})
        return entries

    def history_text(self, name: str, version_id: str) -> str:
        self._path(name)
        if not re.fullmatch(r"\d{8}T\d{12}Z", version_id):
            raise DocumentError("No such earlier version.", status=404)
        path = self._history / name.removesuffix(".md") / f"{version_id}.md"
        if not path.is_file():
            raise DocumentError("No such earlier version.", status=404)
        return path.read_text(encoding="utf-8")

    # --- Checking ----------------------------------------------------------------------

    def check(self, name: str, text: str, private_values: set[str]) -> tuple[list[str], list[str]]:
        """Problems that stop the save, and warnings that do not."""
        old = self._path(name).read_text(encoding="utf-8")
        problems: list[str] = []
        warnings: list[str] = []

        if not text.strip():
            problems.append("The document is empty.")
            return problems, warnings
        if len(text) > DOCUMENT_MAX_CHARS:
            problems.append(f"The document is too long ({len(text):,} characters; at most {DOCUMENT_MAX_CHARS:,}).")

        # Customer details must never be added: every customer can search these documents.
        old_lower = old.lower()
        new_lower = text.lower()
        added_emails = {
            e for e in EMAIL.findall(text) if not e.lower().endswith(SHOP_EMAIL_DOMAIN) and e.lower() not in old_lower
        }
        added_private = sorted(v for v in private_values if v.lower() in new_lower and v.lower() not in old_lower)
        if added_emails:
            problems.append(
                "Email addresses cannot be added to a shop document, because every customer can search it: "
                + ", ".join(sorted(added_emails)[:5])
            )
        if added_private:
            problems.append(
                "Customer details cannot be added to a shop document, because every customer can search it: "
                + ", ".join(added_private[:5])
            )

        new_sections = sections(text)
        if not new_sections:
            warnings.append('The document has no "## " headings, so the search treats it as one block.')
        for s in new_sections:
            if s["chars"] > SECTION_MAX_CHARS:
                problems.append(
                    f'The section "{s["heading"]}" is too long for the search ({s["chars"]:,} characters; '
                    f"at most {SECTION_MAX_CHARS:,}). Split it with more \"## \" headings."
                )
            elif s["chars"] > SECTION_WARN_CHARS:
                warnings.append(
                    f'The section "{s["heading"]}" is long ({s["chars"]:,} characters). The search finds '
                    "shorter sections more reliably; think about splitting it."
                )
            elif not s["text"]:
                warnings.append(f'The section "{s["heading"]}" is empty.')

        old_by_heading = {s["heading"]: s["text"] for s in sections(old)}
        new_by_heading = {s["heading"]: s["text"] for s in new_sections}
        for heading, reason in PROTECTED_SECTIONS.get(name, {}).items():
            if old_by_heading.get(heading) != new_by_heading.get(heading):
                problems.append(f'The section "{heading}" {reason}. Put it back as it was.')

        if name == OVERVIEW_FILE:
            # The shop page reads its products and stock from this document.
            with tempfile.TemporaryDirectory() as folder:
                (Path(folder) / OVERVIEW_FILE).write_text(text, encoding="utf-8")
                try:
                    products = load_catalogue(Path(folder))
                except ConfigError:
                    problems.append(
                        'The shop page could not read the "Product catalogue and prices" table. Keep its '
                        "columns as they are: Product, Category, Price, Warranty."
                    )
                else:
                    before = len(load_catalogue(self._folder))
                    if len(products) != before:
                        warnings.append(f"The shop page will show {len(products)} products (it showed {before}).")
        return problems, warnings

    # --- Saving -----------------------------------------------------------------------

    def save(self, name: str, text: str, expected_version: str) -> None:
        """Write the new text, keeping the old one in the history first."""
        path = self._path(name)
        old = path.read_text(encoding="utf-8")
        if version_of(old) != expected_version:
            raise DocumentError(
                "Someone else saved this document while you were editing it. Copy your changes, "
                "open it again, and make them on top of the new text.",
                status=409,
            )
        if text == old:
            return
        folder = self._history / name.removesuffix(".md")
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{_stamp()}.md").write_text(old, encoding="utf-8", newline="\n")
        for stale in sorted(folder.glob("*.md"), reverse=True)[HISTORY_KEPT:]:
            stale.unlink(missing_ok=True)
        # Plain line breaks, also on Windows, so git sees only the lines that changed.
        path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")

    def write_back(self, name: str, text: str) -> None:
        """Put a text back without adding to the history (used to undo a save
        whose new text the search could not index)."""
        self._path(name).write_text(text, encoding="utf-8", newline="\n")
