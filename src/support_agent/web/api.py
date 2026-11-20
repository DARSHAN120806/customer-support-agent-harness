"""The web API behind the React front end.

Start it with:

    .venv/Scripts/python -m uvicorn support_agent.web.api:create_app --factory --reload

It only wraps the existing agent: the same prompt, tools, safety checks,
limits, and logging run for a browser chat as for the terminal chat.

Endpoints (all under /api):

    GET    /health                         is the server up
    GET    /customers?q=priya              demo sign-in: find a customer
    POST   /sessions                       sign in as a customer, start a chat
    GET    /sessions/{id}                  the chat so far and the customer's orders
    POST   /sessions/{id}/messages         send a message, get the reply and what
                                           the harness did ("behind the scenes")
    DELETE /sessions/{id}                  sign out
    GET    /tickets                        support dashboard: tickets (emails masked)
    GET    /conversations                  support dashboard: logged conversations
    GET    /conversations/{id}             every event of one conversation
    GET    /evaluations                    saved evaluation baselines
    GET    /evaluations/{name}             one baseline in full

IMPORTANT: the sign-in is a demo. Anyone can choose any customer, and the
dashboard has no password. Run this on your own computer only; it must not be
put on the internet as it is.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .. import event_log
from ..app import Resources, create_agent, load_resources
from ..config import PROJECT_ROOT, ConfigError, Settings
from ..prompts import SHOP_NAME, fallback_reply
from .sessions import ChatSession, SessionBusy, SessionStore

MAX_MESSAGE_LENGTH = 2000
BASELINES_DIR = PROJECT_ROOT / "evals" / "baselines"
# The React development server. Only pages from here may call the API.
DEFAULT_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
# Events shown in the "behind the scenes" panel.
PANEL_EVENTS = {
    event_log.MODEL_CALL,
    event_log.TOOL_CALL,
    event_log.REPLY_REWRITE,
    event_log.REPLY_BLOCKED,
    event_log.TICKET_CREATED,
    event_log.RETRY,
    event_log.ERROR,
}


class SignIn(BaseModel):
    email: str = Field(min_length=3, max_length=200)


class Message(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


def create_app(
    settings: Settings | None = None,
    resources: Resources | None = None,
    today: date | None = None,
    baselines_dir: Path = BASELINES_DIR,
    allowed_origins: list[str] | None = None,
) -> FastAPI:
    """Build the web app. With no arguments it reads .env and connects to the
    real services; tests pass in a fake model and fake data instead."""
    if settings is None:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
        settings = Settings.from_env()
    if resources is None:
        resources = load_resources(settings)

    customers = _load_customers(settings.orders_file)
    sessions = SessionStore()
    app = FastAPI(title=f"{SHOP_NAME} support API", version="1.0")
    app.state.sessions = sessions  # reachable from tests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins or DEFAULT_ALLOWED_ORIGINS,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type"],
    )

    def session_or_404(session_id: str) -> ChatSession:
        session = sessions.get(session_id)
        if session is None:
            raise HTTPException(404, "This chat has ended. Please sign in again.")
        return session

    # --- Health and sign-in -------------------------------------------------------

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "shop": SHOP_NAME, "provider": settings.provider, "model": settings.model}

    @app.get("/api/customers")
    def find_customers(q: str = Query("", max_length=100), limit: int = Query(20, ge=1, le=50)) -> list[dict]:
        """Demo sign-in only: in a real shop the login decides who the customer is."""
        needle = q.strip().lower()
        found = [
            c for c in customers.values()
            if not needle or needle in c["email"] or needle in c["name"].lower()
        ]
        return [_public_customer(c) for c in found[:limit]]

    @app.post("/api/sessions", status_code=201)
    def sign_in(body: SignIn) -> dict[str, Any]:
        customer = customers.get(body.email.strip().lower())
        if customer is None:
            raise HTTPException(404, "No customer has that email address.")

        def make(session_id: str) -> ChatSession:
            agent, context = create_agent(settings, resources, customer["email"], today=today)
            session = ChatSession(session_id, agent, context, customer)
            context.logger.subscribe(
                lambda event: session.current_events.append(event)
                if event["event"] in PANEL_EVENTS
                else None
            )
            return session

        session = sessions.add(make)
        return _session_view(session)

    @app.get("/api/sessions/{session_id}")
    def get_session(session_id: str) -> dict[str, Any]:
        return _session_view(session_or_404(session_id))

    @app.delete("/api/sessions/{session_id}", status_code=204)
    def sign_out(session_id: str) -> None:
        sessions.remove(session_id)

    # --- Chatting -------------------------------------------------------------------

    @app.post("/api/sessions/{session_id}/messages")
    def send_message(session_id: str, body: Message) -> dict[str, Any]:
        session = session_or_404(session_id)
        if not session.lock.acquire(blocking=False):
            raise HTTPException(409, "Please wait for the reply to your last message.")
        try:
            return _answer(session, body.text.strip())
        finally:
            session.lock.release()

    def _answer(session: ChatSession, text: str) -> dict[str, Any]:
        if not text:
            raise HTTPException(422, "The message is empty.")
        session.current_events = []
        tickets_before = len(session.context.ticket_ids)
        history_before = len(session.history)
        try:
            result = session.agent.run(text, session.history)
        except Exception as error:  # last safety net, as in the terminal chat
            event_log.log_error(session.context.logger, "agent_run", error)
            del session.history[history_before:]
            reply = fallback_reply()
            session.transcript += [{"role": "customer", "text": text}, {"role": "assistant", "text": reply}]
            return {"reply": reply, "outcome": "error", "new_ticket_ids": [], "details": None}

        new_tickets = session.context.ticket_ids[tickets_before:]
        session.transcript.append({"role": "customer", "text": text})
        session.transcript.append(
            {"role": "assistant", "text": result.reply, "ticket_ids": new_tickets}
        )
        return {
            "reply": result.reply,
            "outcome": result.outcome,
            "new_ticket_ids": new_tickets,
            # Everything below is for the "behind the scenes" panel.
            "details": {
                "turn": session.context.logger.turn,
                "steps": result.steps,
                "tools_used": result.tools_used,
                "escalated": result.escalated,
                "violations": result.violations,
                "gave_up_because": result.gave_up_because,
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
                "cost_usd": result.cost_usd,
                "duration_ms": result.duration_ms,
                "events": list(session.current_events),
            },
        }

    # --- Support dashboard ----------------------------------------------------------

    @app.get("/api/tickets")
    def list_tickets() -> list[dict[str, Any]]:
        """Newest first. Emails are masked: the dashboard has no password."""
        tickets = resources.tickets.all()
        return [
            {**event_log.mask_value(t), "customer_email": event_log.EMAIL_MASK}
            for t in reversed(tickets)
        ]

    @app.get("/api/conversations")
    def list_conversations(limit: int = Query(100, ge=1, le=1000)) -> list[dict[str, Any]]:
        summaries: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"turns": 0, "cost_usd": 0.0, "escalated": False, "blocked_or_rewritten": 0}
        )
        for e in event_log.read_events(settings.log_file):
            s = summaries[e["conversation_id"]]
            s.setdefault("conversation_id", e["conversation_id"])
            s.setdefault("started_at", e["ts"])
            s.setdefault("customer_ref", e.get("customer_ref"))
            s["last_at"] = e["ts"]
            if e["event"] == event_log.CONVERSATION_START:
                s["model"] = e.get("model")
                s["harness"] = e.get("harness", True)
            elif e["event"] == event_log.TURN_START:
                s["turns"] += 1
                s.setdefault("first_message", e.get("message", "")[:200])
            elif e["event"] == event_log.TURN_END:
                s["cost_usd"] = round(s["cost_usd"] + (e.get("cost_usd") or 0), 6)
                s["escalated"] = s["escalated"] or bool(e.get("escalated"))
            elif e["event"] in (event_log.REPLY_REWRITE, event_log.REPLY_BLOCKED):
                s["blocked_or_rewritten"] += 1
        newest = sorted(summaries.values(), key=lambda s: s["last_at"], reverse=True)
        return newest[:limit]

    @app.get("/api/conversations/{conversation_id}")
    def get_conversation(conversation_id: str) -> list[dict[str, Any]]:
        if not re.fullmatch(r"conv_[0-9a-f]{12}", conversation_id):
            raise HTTPException(404, "No such conversation.")
        events = list(event_log.read_events(settings.log_file, conversation_id))
        if not events:
            raise HTTPException(404, "No such conversation.")
        return events

    @app.get("/api/evaluations")
    def list_evaluations() -> list[dict[str, Any]]:
        runs = []
        for path in sorted(baselines_dir.glob("*.json")):
            data = _read_json(path)
            if data:
                runs.append(
                    {
                        "name": path.stem,
                        "run_at": data.get("run_at"),
                        "model": data.get("model"),
                        "harness": data.get("harness", "on"),
                        "summary": data.get("summary", {}),
                    }
                )
        return runs

    @app.get("/api/evaluations/{name}")
    def get_evaluation(name: str) -> dict[str, Any]:
        # Only plain file names, so nothing outside the folder can be read.
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or name.startswith("."):
            raise HTTPException(404, "No such evaluation.")
        data = _read_json(baselines_dir / f"{name}.json")
        if data is None:
            raise HTTPException(404, "No such evaluation.")
        return data

    def _session_view(session: ChatSession) -> dict[str, Any]:
        return {
            "session_id": session.session_id,
            "conversation_id": session.context.logger.conversation_id,
            "customer": _public_customer(session.customer),
            "orders": [_order_summary(o) for o in session.customer["orders"]],
            "transcript": session.transcript,
            "assistant_name": f"{SHOP_NAME} virtual assistant",
        }

    return app


def _load_customers(orders_file: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(orders_file.read_text(encoding="utf-8"))
    by_id = {c["customer_id"]: {**c, "orders": []} for c in data["customers"]}
    for order in data["orders"]:
        by_id[order["customer_id"]]["orders"].append(order)
    return {c["email"].lower(): c for c in by_id.values()}


def _public_customer(customer: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": customer.get("name") or customer["email"].split("@")[0].replace(".", " ").title(),
        "email": customer["email"],
        "order_count": len(customer["orders"]),
    }


def _order_summary(order: dict[str, Any]) -> dict[str, Any]:
    """Enough for the 'your orders' list; the agent looks up the details."""
    return {
        "order_id": order["order_id"],
        "placed_on": order["placed_on"],
        "status": order["status"],
        "total": order["total"],
        "items": [item["name"] for item in order["items"]],
    }


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


__all__ = ["create_app", "ConfigError"]
