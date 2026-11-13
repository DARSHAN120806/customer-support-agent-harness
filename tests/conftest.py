"""Shared test set-up: real shop data, a fake embedding model, and a temporary
ticket file, so tests never call a paid service or touch real tickets."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from fakes import FakeEmbedder

from support_agent.knowledge_base import KnowledgeBase
from support_agent.orders import OrderStore
from support_agent.tickets import TicketStore
from support_agent.tools import SessionContext, build_tool_registry

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

TODAY = date(2026, 11, 12)  # the date the fake orders were written around
PRIYA = "priya.nair@example.com"  # owns JL-10198 and JL-10231
MARCUS = "marcus.bell@example.com"  # owns JL-10205 and JL-10240


@pytest.fixture(scope="session")
def knowledge_base() -> KnowledgeBase:
    return KnowledgeBase.build(DATA_DIR / "knowledge_base", FakeEmbedder())


@pytest.fixture(scope="session")
def orders() -> OrderStore:
    return OrderStore(DATA_DIR / "orders.json")


@pytest.fixture
def tickets(tmp_path) -> TicketStore:
    return TicketStore(tmp_path / "tickets" / "tickets.jsonl")


@pytest.fixture
def session() -> SessionContext:
    return SessionContext(customer_email=PRIYA)


@pytest.fixture
def registry(session, knowledge_base, orders, tickets):
    return build_tool_registry(session, knowledge_base, orders, tickets, today=TODAY)
