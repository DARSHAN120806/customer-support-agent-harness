"""Chat sessions kept in memory while the web server runs.

Each browser chat is one session: one signed-in customer, one agent, and the
conversation so far. Sessions that sit unused are removed, and there is a cap
on how many can exist, so the server cannot fill up its memory.
"""

from __future__ import annotations

import secrets
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ..agent import Agent
from ..tools import SessionContext


class SessionBusy(Exception):
    """Raised when a second message arrives before the first was answered."""


@dataclass
class ChatSession:
    session_id: str
    agent: Agent
    context: SessionContext
    customer: dict[str, Any]
    history: list[dict[str, Any]] = field(default_factory=list)
    # What the customer and the assistant said, for showing the chat again.
    transcript: list[dict[str, Any]] = field(default_factory=list)
    last_used: float = field(default_factory=time.monotonic)
    lock: threading.Lock = field(default_factory=threading.Lock)


class SessionStore:
    def __init__(
        self,
        max_sessions: int = 200,
        idle_seconds: float = 3600,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._sessions: dict[str, ChatSession] = {}
        self._lock = threading.Lock()
        self._max = max_sessions
        self._idle = idle_seconds
        self._clock = clock

    def add(self, make: Callable[[str], ChatSession]) -> ChatSession:
        with self._lock:
            self._remove_idle()
            if len(self._sessions) >= self._max:
                # Make room by dropping the session that was used longest ago.
                oldest = min(self._sessions.values(), key=lambda s: s.last_used)
                del self._sessions[oldest.session_id]
            session_id = secrets.token_urlsafe(16)  # impossible to guess
            session = make(session_id)
            session.last_used = self._clock()
            self._sessions[session_id] = session
            return session

    def get(self, session_id: str) -> ChatSession | None:
        with self._lock:
            self._remove_idle()
            session = self._sessions.get(session_id)
            if session:
                session.last_used = self._clock()
            return session

    def remove(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def __len__(self) -> int:
        return len(self._sessions)

    def _remove_idle(self) -> None:
        now = self._clock()
        for session_id in [s.session_id for s in self._sessions.values() if now - s.last_used > self._idle]:
            del self._sessions[session_id]
