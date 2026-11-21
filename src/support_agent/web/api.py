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
    DELETE /admin/session                  admin or staff sign-out
    GET    /sessions/{id}/updates?after=N  new chat lines (a support person joining,
                                           their messages, the chat ending)
    POST   /sessions/{id}/tickets/{ticket}/messages  a customer's reply on a ticket

Admin panel (header "Authorization: Bearer <token>"); the admin and support staff:

    GET    /admin/me                       who is signed in
    GET    /stats, /tickets, /conversations, /admin/orders (see below)
    GET    /tickets/{id}                   one ticket, its earlier chat and its messages
    POST   /tickets/{id}/take              take a waiting ticket
    POST   /tickets/{id}/messages          reply to the customer
    POST   /tickets/{id}/end               end the chat; the ticket is closed

Admin only: model settings, documents, evaluations.

    GET    /stats                          numbers for the admin overview
    GET    /admin/model                    the chat and search models in use (keys hidden)
    POST   /admin/model/test               try a model choice with tiny requests
    PUT    /admin/model                    save a model choice; new chats use it
    DELETE /admin/model                    forget the saved choice, go back to .env
    GET    /admin/documents                the shop documents
    GET    /admin/documents/{name}         one document, its sections and earlier versions
    PUT    /admin/documents/{name}         save a document (checked, then re-indexed)
    GET    /admin/documents/{name}/history/{id}  an earlier version's text
    POST   /admin/documents/{name}/restore put an earlier version back
    GET    /admin/orders?q=...             find orders by order ID, customer or item
    GET    /admin/orders/{order_id}        one order with all its records
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
from .accounts import ADMIN, PANEL_ROLES, Account, AccountStore, AdminSessions, SignInLimiter
from .documents import DocumentError, DocumentStore
from .model_admin import ModelForm, candidate_settings, check_connection, problems, same_search, to_saved
from .sessions import ChatSession, SessionBusy, SessionStore
from .stats import overview
from .ticket_chat import TicketChatError, customer_message, end, first_name, staff_message, take, team

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


class DocumentEdit(BaseModel):
    text: str = Field(max_length=250_000)
    # The fingerprint of the text the editor started from (see documents.version_of).
    version: str = Field(min_length=1, max_length=64)


class DocumentRestore(BaseModel):
    version_id: str = Field(min_length=1, max_length=40)
    version: str = Field(min_length=1, max_length=64)


ORDERS_SHOWN = 50


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
    documents: DocumentStore | None = None,
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
    catalogue = {"products": [p.to_dict() for p in load_catalogue(settings.knowledge_base_dir)]}
    # Earlier versions of the documents are kept next to the other private files.
    documents = documents or DocumentStore(
        settings.knowledge_base_dir, base_settings.model_settings_file.parent / "document_history"
    )
    # Values that must never be added to a shop document: every customer can
    # search those documents.
    private_values = {
        value
        for customer in customers.values()
        for value in [customer["email"], *(o["order_id"] for o in customer["orders"]),
                      *(o.get("tracking_number") or "" for o in customer["orders"])]
        if value
    }
    orders_by_id = {o["order_id"]: (o, c) for c in customers.values() for o in c["orders"]}
    if accounts is None:
        accounts = AccountStore.load(settings.accounts_file)
    limiter = limiter or SignInLimiter()
    admins = AdminSessions()
    sessions = SessionStore()
    app = FastAPI(title=f"{SHOP_NAME} support API", version="1.0")
    app.state.sessions = sessions  # reachable from tests
    app.state.live = live
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
        """The token of a signed-in admin-panel user (admin or staff)."""
        token = (authorization or "").removeprefix("Bearer ").strip()
        if not token or not admins.is_valid(token):
            raise HTTPException(401, "Please sign in as an admin.")
        return token

    def panel_person(token: str = Depends(admin_token)) -> Account:
        """Who is signed in to the admin panel: the admin or a support person."""
        person = admins.get(token)
        if person is None:  # pragma: no cover - admin_token has just checked it
            raise HTTPException(401, "Please sign in as an admin.")
        return person

    def admin_person(person: Account = Depends(panel_person)) -> Account:
        if person.role != ADMIN:
            raise HTTPException(403, "Only the admin can do this.")
        return person

    # Support staff see tickets, conversations, orders and the overview; the
    # admin also sees the model, the documents and the evaluations.
    panel_only = [Depends(panel_person)]
    admin_only = [Depends(admin_person)]

    def live_session_for(ticket: dict[str, Any]) -> ChatSession | None:
        """The customer's chat window this ticket came from, if it is still open."""
        conversation = ticket.get("conversation_id")
        email = str(ticket.get("customer_email", "")).lower()
        if not conversation:
            return None
        return sessions.find(
            lambda s: s.context.logger.conversation_id == conversation and s.customer["email"].lower() == email
        )

    def ticket_view(ticket: dict[str, Any]) -> dict[str, Any]:
        """A ticket for the admin panel. Emails are masked, as everywhere there."""
        view = {**event_log.mask_value(ticket), "customer_email": event_log.EMAIL_MASK}
        view["status"] = ticket.get("status", "open")
        view["messages"] = event_log.mask_value(ticket.get("messages", []))
        view["live"] = live_session_for(ticket) is not None
        customer = customers.get(str(ticket.get("customer_email", "")).lower())
        view["customer_name"] = customer["name"] if customer else None
        view["customer_id"] = customer["customer_id"] if customer else None
        return view

    def ticket_customer(ticket: dict[str, Any]) -> dict[str, Any] | None:
        """Who the ticket is from, so the person answering can check their
        orders. The email stays masked, as everywhere in the panel."""
        customer = customers.get(str(ticket.get("customer_email", "")).lower())
        if customer is None:
            return None
        newest_first = sorted(customer["orders"], key=lambda o: o["placed_on"], reverse=True)
        return {
            "name": customer["name"],
            "customer_id": customer["customer_id"],
            "city": customer.get("city"),
            "email": event_log.EMAIL_MASK,
            "orders": [_order_summary(o) for o in newest_first],
        }

    def chat_call(action: Callable[[], Any]) -> Any:
        try:
            return action()
        except TicketChatError as error:
            raise HTTPException(error.status, str(error)) from error

    # --- Health and sign-in -------------------------------------------------------

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "shop": SHOP_NAME, "provider": live.settings.provider, "model": live.settings.model}

    @app.get("/api/products")
    def list_products() -> list[dict[str, Any]]:
        return catalogue["products"]

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
        if account.role in PANEL_ROLES:
            return {
                "role": account.role,
                "admin_token": admins.start(account),
                "name": account.name or "Admin",
                "staff_id": account.staff_id,
            }
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

    @app.get("/api/admin/me")
    def who_am_i(person: Account = Depends(panel_person)) -> dict[str, str]:
        return {"role": person.role, "name": person.name or "Admin", "staff_id": person.staff_id}

    # --- Support staff answering tickets ---------------------------------------------

    @app.get("/api/tickets/{ticket_id}", dependencies=panel_only)
    def get_ticket(ticket_id: str) -> dict[str, Any]:
        ticket = resources.tickets.get(ticket_id)
        if ticket is None:
            raise HTTPException(404, "No such ticket.")
        # The customer's chat with the assistant before the hand-over, from the
        # (masked) log.
        chat = []
        if ticket.get("conversation_id"):
            for e in event_log.read_events(settings.log_file, ticket["conversation_id"]):
                if e["event"] == event_log.TURN_START:
                    chat.append({"role": "customer", "text": e.get("message", "")})
                elif e["event"] == event_log.TURN_END and e.get("reply"):
                    chat.append({"role": "assistant", "text": e["reply"]})
        return {"ticket": ticket_view(ticket), "chat": chat, "customer": ticket_customer(ticket)}

    @app.post("/api/tickets/{ticket_id}/take")
    def take_ticket(ticket_id: str, person: Account = Depends(panel_person)) -> dict[str, Any]:
        ticket = chat_call(lambda: take(resources.tickets, ticket_id, person))
        session = live_session_for(ticket)
        if session is not None and not session.handoff:
            name = first_name(ticket["assigned_to"]["name"])
            session.handoff = {"ticket_id": ticket_id, "name": name}
            session.transcript.append(
                {"role": "system", "text": f"{name} from the support team has joined the chat. You're now talking to a person."}
            )
        return get_ticket(ticket_id)

    @app.post("/api/tickets/{ticket_id}/messages")
    def reply_to_ticket(ticket_id: str, body: Message, person: Account = Depends(panel_person)) -> dict[str, Any]:
        ticket, message = chat_call(lambda: staff_message(resources.tickets, ticket_id, person, body.text))
        session = live_session_for(ticket)
        if session is not None and (session.handoff or {}).get("ticket_id") == ticket_id:
            session.transcript.append({"role": "staff", "text": message["text"], "name": first_name(message["name"])})
        return get_ticket(ticket_id)

    @app.post("/api/tickets/{ticket_id}/end")
    def end_ticket(ticket_id: str, person: Account = Depends(panel_person)) -> dict[str, Any]:
        ticket = chat_call(lambda: end(resources.tickets, ticket_id, person))
        session = live_session_for(ticket)
        if session is not None and (session.handoff or {}).get("ticket_id") == ticket_id:
            name = session.handoff["name"]
            session.handoff = None
            session.transcript.append(
                {"role": "system", "text": f"{name} has ended the chat. The virtual assistant can help with anything else."}
            )
        return get_ticket(ticket_id)

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

    @app.get("/api/sessions/{session_id}/updates")
    def chat_updates(session_id: str, after: int = Query(0, ge=0)) -> dict[str, Any]:
        """New chat lines since `after`, so the chat window can show a support
        person's messages as they arrive."""
        session = session_or_404(session_id)
        return {
            "entries": session.transcript[after:],
            "next": len(session.transcript),
            "handoff": _handoff_view(session),
        }

    @app.post("/api/sessions/{session_id}/tickets/{ticket_id}/messages")
    def customer_ticket_reply(session_id: str, ticket_id: str, body: Message) -> dict[str, Any]:
        """A customer answering a ticket from "Your tickets" (for example after
        coming back later)."""
        session = session_or_404(session_id)
        ticket, message = chat_call(
            lambda: customer_message(resources.tickets, ticket_id, session.customer["email"], body.text)
        )
        if (session.handoff or {}).get("ticket_id") == ticket_id:
            session.transcript.append({"role": "customer", "text": message["text"]})
        return _chat_ticket(ticket)

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
        if session.handoff:
            # A person from the support team is in this chat: the message goes
            # to them, not to the assistant.
            try:
                customer_message(resources.tickets, session.handoff["ticket_id"], session.customer["email"], text)
            except TicketChatError:
                session.handoff = None  # the ticket was closed meanwhile; the assistant answers
            else:
                session.transcript.append({"role": "customer", "text": text})
                return {"reply": None, "outcome": "sent_to_team", "new_ticket_ids": []}
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

    # --- Shop documents (admin) ------------------------------------------------------

    def reindex_or_undo(name: str, old_text: str) -> None:
        """Rebuild the search from the saved documents. If that fails, put the
        old text back, so the documents and the search never disagree."""
        try:
            knowledge_base = build_knowledge_base(live.settings, embedder_factory(live.settings))
        except (ConfigError, ServiceError) as error:
            documents.write_back(name, old_text)
            raise HTTPException(400, f"Nothing was changed: the search could not read the new text ({error}).") from error
        live.resources = dataclasses.replace(live.resources, knowledge_base=knowledge_base)
        catalogue["products"] = [p.to_dict() for p in load_catalogue(settings.knowledge_base_dir)]

    def save_document(name: str, text: str, version: str) -> dict[str, Any]:
        try:
            problems_found, warnings = documents.check(name, text, private_values)
            if problems_found:
                raise HTTPException(400, "\n".join(problems_found))
            old_text = documents.read(name)["text"]
            documents.save(name, text, version)
        except DocumentError as error:
            raise HTTPException(error.status, str(error)) from error
        reindex_or_undo(name, old_text)
        return {"document": documents.read(name), "warnings": warnings}

    def document_or_404(action: Callable[[], Any]) -> Any:
        try:
            return action()
        except DocumentError as error:
            raise HTTPException(error.status, str(error)) from error

    @app.get("/api/admin/documents", dependencies=admin_only)
    def list_documents() -> list[dict[str, Any]]:
        return documents.list()

    @app.get("/api/admin/documents/{name}", dependencies=admin_only)
    def get_document(name: str) -> dict[str, Any]:
        return document_or_404(lambda: documents.read(name))

    @app.put("/api/admin/documents/{name}", dependencies=admin_only)
    def put_document(name: str, body: DocumentEdit) -> dict[str, Any]:
        return save_document(name, body.text, body.version)

    @app.get("/api/admin/documents/{name}/history/{version_id}", dependencies=admin_only)
    def get_document_version(name: str, version_id: str) -> dict[str, Any]:
        return {"text": document_or_404(lambda: documents.history_text(name, version_id))}

    @app.post("/api/admin/documents/{name}/restore", dependencies=admin_only)
    def restore_document(name: str, body: DocumentRestore) -> dict[str, Any]:
        text = document_or_404(lambda: documents.history_text(name, body.version_id))
        return save_document(name, text, body.version)

    # --- Orders (admin, read only) ----------------------------------------------------

    @app.get("/api/admin/orders", dependencies=panel_only)
    def find_orders(q: str = Query("", max_length=100)) -> dict[str, Any]:
        needle = q.strip().lower()
        found = [
            (o, c) for o, c in orders_by_id.values()
            if not needle
            or needle in o["order_id"].lower()
            or needle in c["name"].lower()
            or needle == c["email"].lower()
            or any(needle in item["name"].lower() for item in o["items"])
        ]
        found.sort(key=lambda pair: pair[0]["placed_on"], reverse=True)
        return {
            "total": len(found),
            "orders": [
                {**_order_summary(o), "customer_name": c["name"], "records": _record_count(o)}
                for o, c in found[:ORDERS_SHOWN]
            ],
        }

    @app.get("/api/admin/orders/{order_id}", dependencies=panel_only)
    def get_order(order_id: str) -> dict[str, Any]:
        pair = orders_by_id.get(order_id.strip().upper())
        if pair is None:
            raise HTTPException(404, "No such order.")
        order, customer = pair
        # The order records hold no emails, so the admin sees them as they are,
        # with tracking numbers and times. The customer's email stays masked.
        return {
            "order": order,
            "customer": {"name": customer["name"], "email": event_log.EMAIL_MASK, "city": customer.get("city")},
        }

    @app.get("/api/stats", dependencies=panel_only)
    def stats() -> dict[str, Any]:
        tickets = resources.tickets.all()
        return overview(event_log.read_events(settings.log_file), tickets, today or date.today()) | {"team": team(tickets)}

    @app.get("/api/tickets", dependencies=panel_only)
    def list_tickets() -> list[dict[str, Any]]:
        """Newest first. Emails are masked."""
        return [ticket_view(t) for t in reversed(resources.tickets.all())]

    @app.get("/api/conversations", dependencies=panel_only)
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

    @app.get("/api/conversations/{conversation_id}", dependencies=panel_only)
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
            "handoff": _handoff_view(session),
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


def _handoff_view(session: ChatSession) -> dict[str, str] | None:
    """Who from the support team is in this chat, if anyone."""
    return {"name": session.handoff["name"]} if session.handoff else None


def _chat_ticket(ticket: dict[str, Any]) -> dict[str, Any]:
    """A ticket the assistant (or the harness) created in a chat, as its
    customer sees it: support people appear by first name only."""
    assigned = ticket.get("assigned_to") or {}
    return {
        "assigned_name": first_name(assigned["name"]) if assigned else None,
        "messages": [
            {"from": m["from"], "text": m["text"], "at": m["at"], **({"name": first_name(m.get("name", ""))} if m["from"] == "staff" else {})}
            for m in ticket.get("messages", [])
        ],
        "ticket_id": ticket["ticket_id"],
        "created_at": ticket.get("created_at", ""),
        "status": str(ticket.get("status", "open")).lower(),
        "topic": REASON_LABELS.get(ticket.get("reason", ""), "Other"),
        "summary": ticket.get("summary", ""),
        "order_id": ticket.get("order_id"),
        "source": "chat",
    }


# The kinds of records an order can carry (refunds, returns, tickets, ...).
RECORD_KEYS = (
    "past_support_tickets", "refunds", "returns", "warranty_claims", "address_change_requests",
    "carrier_investigations", "refund_disputes", "damage_reports",
)


def _record_count(order: dict[str, Any]) -> int:
    return sum(len(order.get(key) or []) for key in RECORD_KEYS)


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


__all__ = ["create_app", "ConfigError"]
