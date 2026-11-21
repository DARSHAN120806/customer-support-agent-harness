"""The web API behind the React front end.

Start it with:

    .venv/Scripts/python -m uvicorn support_agent.web.api:create_app --factory --reload

It only wraps the existing agent: the same prompt, tools, safety checks,
limits, and logging run for a browser chat as for the terminal chat.

Endpoints (all under /api):

    GET    /health                         is the server up
    POST   /sessions                       sign in with email and password; a
                                           customer gets a chat, the admin a token
    GET    /products                       the shop's products, prices and stock
    GET    /sessions/{id}                  the chat so far and the customer's orders
    GET    /sessions/{id}/tickets          the customer's own support tickets
    POST   /sessions/{id}/messages         send a message, get the reply (what the
                                           harness did goes to the log, for the admin)
    DELETE /sessions/{id}                  sign out
    DELETE /admin/session                  admin sign-out

Admin only (header "Authorization: Bearer <admin token>"):

    GET    /stats                          numbers for the admin overview
    GET    /admin/model                    the chat and search models in use (keys hidden)
    POST   /admin/model/test               try a model choice with tiny requests
    PUT    /admin/model                    save a model choice; new chats use it
    DELETE /admin/model                    forget the saved choice, go back to .env
    GET    /tickets                        support dashboard: tickets (emails masked)
    GET    /conversations                  support dashboard: logged conversations
    GET    /conversations/{id}             every event of one conversation
    GET    /evaluations                    saved evaluation baselines
    GET    /evaluations/{name}             one baseline in full

Accounts and passwords come from private/accounts.json, made by
scripts/create_test_passwords.py. Passwords are stored only as scrypt hashes.
This is still a local demo: there is no HTTPS, no password reset, and sessions
live in memory, so do not put it on the internet as it is.
"""

from __future__ import annotations

import dataclasses
import json
import re
from dataclasses import dataclass
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Callable

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .. import event_log
from ..app import Resources, build_knowledge_base, create_agent, load_resources
from ..catalogue import load_catalogue
from ..config import PROJECT_ROOT, ConfigError, Settings
from ..model_settings import apply as apply_saved
from ..model_settings import load_saved, public_view, save
from ..prompts import SHOP_NAME, fallback_reply
from ..providers import create_embedder, create_provider
from ..retry import ServiceError
from .accounts import ADMIN, AccountStore, AdminSessions, SignInLimiter
from .model_admin import ModelForm, candidate_settings, check_connection, problems, same_search, to_saved
from .sessions import ChatSession, SessionBusy, SessionStore
from .stats import overview

MAX_MESSAGE_LENGTH = 2000
BASELINES_DIR = PROJECT_ROOT / "evals" / "baselines"
# The React development server. Only pages from here may call the API.
DEFAULT_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]


WRONG_SIGN_IN = "Email or password is incorrect."
# Ticket reasons in the words a customer would use.
REASON_LABELS = {
    "refund_request": "Refund request",
    "return_request": "Return request",
    "warranty_claim": "Warranty claim",
    "order_problem": "Problem with an order",
    "upset_customer": "Complaint",
    "unsure_of_answer": "Question for the team",
    "outside_shop_documents": "Question for the team",
    "human_requested": "Asked for a person",
    "other": "Other",
}
MAX_TICKETS_SHOWN = 20
TOO_MANY_TRIES = "Too many wrong passwords. Please wait 15 minutes and try again."


class SignIn(BaseModel):
    email: str = Field(min_length=3, max_length=200)
    password: str = Field(min_length=1, max_length=200)


class Message(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


@dataclass
class LiveModel:
    """The model in use right now. Saving a new choice in the admin panel swaps
    these, so the next sign-in gets the new model; open chats keep theirs."""

    settings: Settings
    resources: Resources
    saved: dict[str, Any] | None


def create_app(
    settings: Settings | None = None,
    resources: Resources | None = None,
    today: date | None = None,
    baselines_dir: Path = BASELINES_DIR,
    allowed_origins: list[str] | None = None,
    accounts: AccountStore | None = None,
    limiter: SignInLimiter | None = None,
    provider_factory: Callable[[Settings], Any] = create_provider,
    embedder_factory: Callable[[Settings], Any] = create_embedder,
) -> FastAPI:
    """Build the web app. With no arguments it reads .env (plus any model chosen
    in the admin panel) and connects to the real services; tests pass in a fake
    model and fake data instead."""
    saved = None
    if settings is None:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
        base_settings = Settings.from_env()
        saved = load_saved(base_settings.model_settings_file)
        settings = apply_saved(base_settings, saved) if saved else base_settings
    else:
        base_settings = settings
    if resources is None:
        resources = load_resources(settings)
    live = LiveModel(settings, resources, saved)

    customers = _load_customers(settings.orders_file)
    products = [p.to_dict() for p in load_catalogue(settings.knowledge_base_dir)]
    if accounts is None:
        accounts = AccountStore.load(settings.accounts_file)
    limiter = limiter or SignInLimiter()
    admins = AdminSessions()
    sessions = SessionStore()
    app = FastAPI(title=f"{SHOP_NAME} support API", version="1.0")
    app.state.sessions = sessions  # reachable from tests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins or DEFAULT_ALLOWED_ORIGINS,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
    )

    def session_or_404(session_id: str) -> ChatSession:
        session = sessions.get(session_id)
        if session is None:
            raise HTTPException(404, "This chat has ended. Please sign in again.")
        return session

    def admin_token(authorization: str | None = Header(None)) -> str:
        """Every dashboard endpoint needs a signed-in admin."""
        token = (authorization or "").removeprefix("Bearer ").strip()
        if not token or not admins.is_valid(token):
            raise HTTPException(401, "Please sign in as an admin.")
        return token

    admin_only = [Depends(admin_token)]

    # --- Health and sign-in -------------------------------------------------------

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "shop": SHOP_NAME, "provider": live.settings.provider, "model": live.settings.model}

    @app.get("/api/products")
    def list_products() -> list[dict[str, Any]]:
        return products

    @app.post("/api/sessions", status_code=201)
    def sign_in(body: SignIn) -> dict[str, Any]:
        email = body.email.strip().lower()
        if limiter.is_locked(email):
            raise HTTPException(429, TOO_MANY_TRIES)
        account = accounts.check(email, body.password)
        if account is None:
            limiter.record_failure(email)
            raise HTTPException(401, WRONG_SIGN_IN)
        limiter.clear(email)
        if account.role == ADMIN:
            return {"role": ADMIN, "admin_token": admins.start()}
        customer = customers.get(email)
        if customer is None:  # an account with no customer record behind it
            raise HTTPException(401, WRONG_SIGN_IN)

        def make(session_id: str) -> ChatSession:
            agent, context = create_agent(live.settings, live.resources, customer["email"], today=today)
            return ChatSession(session_id, agent, context, customer)

        session = sessions.add(make)
        return _session_view(session)

    @app.delete("/api/admin/session", status_code=204)
    def admin_sign_out(token: str = Depends(admin_token)) -> None:
        admins.end(token)

    @app.get("/api/sessions/{session_id}")
    def get_session(session_id: str) -> dict[str, Any]:
        return _session_view(session_or_404(session_id))

    @app.get("/api/sessions/{session_id}/tickets")
    def my_tickets(session_id: str) -> list[dict[str, Any]]:
        """Only the signed-in customer's tickets: earlier ones attached to their
        orders, and any the assistant created for them. Newest first."""
        session = session_or_404(session_id)
        email = session.customer["email"].lower()
        found = [
            _past_ticket(ticket, order["order_id"])
            for order in session.customer["orders"]
            for ticket in order.get("past_support_tickets", [])
        ]
        found += [
            _chat_ticket(ticket)
            for ticket in resources.tickets.all()
            if str(ticket.get("customer_email", "")).lower() == email
        ]
        found.sort(key=lambda t: t["created_at"], reverse=True)
        return found[:MAX_TICKETS_SHOWN]

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
        tickets_before = len(session.context.ticket_ids)
        history_before = len(session.history)
        try:
            result = session.agent.run(text, session.history)
        except Exception as error:  # last safety net, as in the terminal chat
            event_log.log_error(session.context.logger, "agent_run", error)
            del session.history[history_before:]
            reply = fallback_reply()
            session.transcript += [{"role": "customer", "text": text}, {"role": "assistant", "text": reply}]
            return {"reply": reply, "outcome": "error", "new_ticket_ids": []}

        new_tickets = session.context.ticket_ids[tickets_before:]
        session.transcript.append({"role": "customer", "text": text})
        session.transcript.append(
            {"role": "assistant", "text": result.reply, "ticket_ids": new_tickets}
        )
        # Only what the customer needs. The steps, tools, checks, tokens and cost
        # are in the event log, where the admin can see them; customers never get them.
        return {"reply": result.reply, "outcome": result.outcome, "new_ticket_ids": new_tickets}

    # --- Support dashboard ----------------------------------------------------------

    # --- Model settings (admin) ------------------------------------------------------

    def switch_to(new_settings: Settings, new_saved: dict[str, Any] | None) -> None:
        """Build the new model (and search index, if the search model changed)
        first; only if that works is anything switched. Open chats are untouched."""
        try:
            provider = provider_factory(new_settings)
            knowledge_base = live.resources.knowledge_base
            if not same_search(new_settings, live.settings):
                knowledge_base = build_knowledge_base(new_settings, embedder_factory(new_settings))
        except (ConfigError, ServiceError) as error:
            raise HTTPException(400, f"Nothing was changed: {error}") from error
        live.settings = new_settings
        live.resources = dataclasses.replace(live.resources, provider=provider, knowledge_base=knowledge_base)
        live.saved = new_saved

    def checked(form: ModelForm) -> tuple[dict[str, Any], dict[str, Any], Settings]:
        found = problems(form)
        if found:
            raise HTTPException(400, " ".join(found))
        chat, search = to_saved(form, live.saved)
        return chat, search, candidate_settings(base_settings, chat, search)

    @app.get("/api/admin/model", dependencies=admin_only)
    def get_model() -> dict[str, Any]:
        return public_view(live.settings, live.saved)

    @app.post("/api/admin/model/test", dependencies=admin_only)
    def test_model(form: ModelForm) -> dict[str, Any]:
        _, _, candidate = checked(form)
        return check_connection(candidate, provider_factory, embedder_factory)

    @app.put("/api/admin/model", dependencies=admin_only)
    def save_model(form: ModelForm) -> dict[str, Any]:
        chat, search, candidate = checked(form)
        switch_to(candidate, {"chat": chat, "search": search})
        live.saved = save(base_settings.model_settings_file, chat, search)
        return public_view(live.settings, live.saved)

    @app.delete("/api/admin/model", dependencies=admin_only)
    def reset_model() -> dict[str, Any]:
        switch_to(base_settings, None)
        base_settings.model_settings_file.unlink(missing_ok=True)
        return public_view(live.settings, None)

    @app.get("/api/stats", dependencies=admin_only)
    def stats() -> dict[str, Any]:
        return overview(event_log.read_events(settings.log_file), resources.tickets.all(), today or date.today())

    @app.get("/api/tickets", dependencies=admin_only)
    def list_tickets() -> list[dict[str, Any]]:
        """Newest first. Emails are masked: the dashboard has no password."""
        tickets = resources.tickets.all()
        return [
            {**event_log.mask_value(t), "customer_email": event_log.EMAIL_MASK}
            for t in reversed(tickets)
        ]

    @app.get("/api/conversations", dependencies=admin_only)
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
        # A sign-in with no message sent is not a conversation worth listing.
        talked = [s for s in summaries.values() if s["turns"] > 0]
        newest = sorted(talked, key=lambda s: s["last_at"], reverse=True)
        return newest[:limit]

    @app.get("/api/conversations/{conversation_id}", dependencies=admin_only)
    def get_conversation(conversation_id: str) -> list[dict[str, Any]]:
        if not re.fullmatch(r"conv_[0-9a-f]{12}", conversation_id):
            raise HTTPException(404, "No such conversation.")
        events = list(event_log.read_events(settings.log_file, conversation_id))
        if not events:
            raise HTTPException(404, "No such conversation.")
        return events

    @app.get("/api/evaluations", dependencies=admin_only)
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

    @app.get("/api/evaluations/{name}", dependencies=admin_only)
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
            "role": "customer",
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


def _past_ticket(ticket: dict[str, Any], order_id: str) -> dict[str, Any]:
    """A ticket from the shop's records. Staff names stay internal."""
    return {
        "ticket_id": ticket["ticket_id"],
        "created_at": str(ticket.get("created_at", "")).replace(" ", "T"),
        "status": str(ticket.get("status", "")).lower(),
        "topic": ticket.get("category") or "Support",
        "summary": ticket.get("summary", ""),
        "order_id": order_id,
        "source": "records",
    }


def _chat_ticket(ticket: dict[str, Any]) -> dict[str, Any]:
    """A ticket the assistant (or the harness) created in a chat."""
    return {
        "ticket_id": ticket["ticket_id"],
        "created_at": ticket.get("created_at", ""),
        "status": str(ticket.get("status", "open")).lower(),
        "topic": REASON_LABELS.get(ticket.get("reason", ""), "Other"),
        "summary": ticket.get("summary", ""),
        "order_id": ticket.get("order_id"),
        "source": "chat",
    }


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


__all__ = ["create_app", "ConfigError"]
