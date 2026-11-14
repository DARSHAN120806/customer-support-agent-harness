"""The knowledge base: the shop's documents, searchable by meaning.

How the search works, in simple words:

1. Every document is cut into sections (one per "## heading").
2. Each section is turned into a list of numbers, called an "embedding", by an
   embedding model. Texts with a similar meaning get similar numbers.
3. To search, the customer's question is turned into numbers the same way, and
   the sections whose numbers are closest to it score highest.
4. Sections that also contain the exact words of the question get a bonus. This
   "hybrid" step matters for names and prices: an embedding is good at meaning
   ("money back" finds "refund") but weak at finding one product in a table.

Embeddings are saved in a cache file, so the documents are only sent to the
embedding model again when their text changes.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from .retry import RetryPolicy, call_with_retry

# Sections scoring below this are left out. The value was chosen by measuring
# real questions against the documents with Titan embeddings; a different
# embedding model needs its own value. It only removes clearly unrelated
# sections. Judging whether a returned section really answers the question is
# left to the model, which is much better at that than a single number is.
DEFAULT_MIN_SCORE = 0.22
DEFAULT_TOP_K = 6
# How much the exact-word bonus counts, compared with the embedding score.
KEYWORD_WEIGHT = 0.3
# Very common words say nothing about the topic, so they earn no bonus.
STOPWORDS = frozenset(
    "a about an and any are can could do does for from get have how i if in is it me my "
    "of on or our please she that the their they this to was we what when where which "
    "who why will with would you your".split()
)
# Text before the first "## heading" is only kept if it says something useful.
MIN_INTRO_LENGTH = 80


class Embedder(Protocol):
    # Identifies the model, so cached embeddings from another model are not reused.
    name: str

    def embed(self, text: str) -> list[float]:
        """Turn a text into a list of numbers of length 1 (a unit vector)."""
        ...


@dataclass(frozen=True)
class Chunk:
    """One section of one document."""

    source: str  # file name, for example "returns.md"
    title: str  # document title, for example "Returns Policy"
    section: str  # section heading, for example "Return window"
    text: str

    @property
    def embedding_text(self) -> str:
        # The title and heading are included so a short section still carries
        # enough meaning to be found.
        return f"{self.title} - {self.section}\n{self.text}"


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float


def load_chunks(folder: Path) -> list[Chunk]:
    """Read every .md file in the folder and split it into sections."""
    chunks: list[Chunk] = []
    for path in sorted(folder.glob("*.md")):
        title = path.stem
        section = "Introduction"
        lines: list[str] = []

        def finish_section() -> None:
            text = "\n".join(lines).strip()
            if text and (section != "Introduction" or len(text) >= MIN_INTRO_LENGTH):
                chunks.append(Chunk(path.name, title, section, text))

        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
            elif line.startswith("## "):
                finish_section()
                section = line[3:].strip()
                lines = []
            else:
                lines.append(line)
        finish_section()
    return chunks


class KnowledgeBase:
    def __init__(
        self,
        chunks: list[Chunk],
        vectors: list[list[float]],
        embedder: Embedder,
        top_k: int = DEFAULT_TOP_K,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> None:
        self._chunks = chunks
        self._vectors = vectors
        self._words = [_content_words(chunk.embedding_text) for chunk in chunks]
        self._embedder = embedder
        self._top_k = top_k
        self._min_score = min_score

    @classmethod
    def build(
        cls,
        folder: Path,
        embedder: Embedder,
        cache_path: Path | None = None,
        top_k: int = DEFAULT_TOP_K,
        min_score: float = DEFAULT_MIN_SCORE,
        retry_policy: RetryPolicy | None = None,
    ) -> "KnowledgeBase":
        chunks = load_chunks(folder)
        if not chunks:
            raise ValueError(f"No documents were found in {folder}.")
        policy = retry_policy or RetryPolicy(max_attempts=1)

        cache = _load_cache(cache_path, embedder.name)
        vectors: list[list[float]] = []
        cache_changed = False
        try:
            for chunk in chunks:
                key = hashlib.sha256(chunk.embedding_text.encode("utf-8")).hexdigest()
                if key not in cache:
                    text = chunk.embedding_text
                    cache[key] = call_with_retry(lambda: embedder.embed(text), policy)
                    cache_changed = True
                vectors.append(cache[key])
        finally:
            # Saved even if a later section failed, so the work already done
            # (and paid for) is not repeated on the next start.
            if cache_path is not None and cache_changed:
                _save_cache(cache_path, embedder.name, cache)
        return cls(chunks, vectors, embedder, top_k, min_score)

    def __len__(self) -> int:
        return len(self._chunks)

    def search(self, query: str) -> list[SearchHit]:
        """Return the most relevant sections, best first. The list is empty when
        nothing in the documents is relevant enough."""
        query_vector = self._embedder.embed(query)
        query_words = _content_words(query)
        hits = []
        for chunk, vector, words in zip(self._chunks, self._vectors, self._words):
            # The share of the question's meaningful words found in the section.
            keyword_score = len(query_words & words) / len(query_words) if query_words else 0.0
            hits.append(
                SearchHit(chunk, _dot(query_vector, vector) + KEYWORD_WEIGHT * keyword_score)
            )
        hits = [hit for hit in hits if hit.score >= self._min_score]
        hits.sort(key=lambda hit: hit.score, reverse=True)
        return hits[: self._top_k]


def _content_words(text: str) -> frozenset[str]:
    """The meaningful words of a text, lower-cased, with a plural "s" removed so
    that "refunds" and "refund" count as the same word."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return frozenset(
        word[:-1] if len(word) > 3 and word.endswith("s") else word
        for word in words
        if len(word) > 1 and word not in STOPWORDS
    )


def _dot(a: list[float], b: list[float]) -> float:
    # For unit vectors this is the "cosine similarity": 1 means the same
    # meaning, 0 means unrelated.
    return sum(x * y for x, y in zip(a, b))


def _load_cache(path: Path | None, embedder_name: str) -> dict[str, list[float]]:
    if path is None or not path.exists():
        return {}
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}  # An unreadable cache is simply rebuilt.
    if data.get("embedder") != embedder_name:
        return {}
    return data.get("vectors", {})


def _save_cache(path: Path, embedder_name: str, vectors: dict[str, list[float]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"embedder": embedder_name, "vectors": vectors}), encoding="utf-8"
        )
    except OSError:
        pass  # The cache only saves time. Without it, the search still works.
