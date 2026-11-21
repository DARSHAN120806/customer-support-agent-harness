"""Tests for error handling and retries. Failures are acted out with fakes, and
waiting is replaced by a recorder, so these tests are instant."""

from __future__ import annotations

import dataclasses
import io
import json

import anthropic
import httpx2
import pytest
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError
from conftest import DATA_DIR, PRIYA, TODAY
from fakes import FakeEmbedder, FakeProvider, text_response, tool_response

from support_agent import embeddings
from support_agent.agent import COMPLETED, MODEL_ERROR
from support_agent.app import Resources, create_agent, load_resources
from support_agent.config import ConfigError, Settings
from support_agent.embeddings import TitanEmbedder
from support_agent.event_log import read_events
from support_agent.knowledge_base import KnowledgeBase
from support_agent.prompts import SUPPORT_EMAIL, fallback_reply
from support_agent.providers.anthropic_sdk import AnthropicSDKProvider, to_service_error
from support_agent.providers.base import ToolCall
from support_agent.retry import RetryPolicy, ServiceError, call_with_retry
from support_agent.tickets import TicketError, TicketStore


def busy(retry_after: float | None = None) -> ServiceError:
    return ServiceError(
        "busy", service="model", kind="rate_limit", retryable=True, retry_after=retry_after
    )


def wrong_key() -> ServiceError:
    return ServiceError("bad key", service="model", kind="auth", retryable=False)


def policy(waits: list, max_attempts: int = 3) -> RetryPolicy:
    """A retry policy that records the waits instead of really sleeping."""
    return RetryPolicy(max_attempts=max_attempts, sleep=waits.append)


# --- The retry helper ----------------------------------------------------------------


def test_success_on_the_first_try_does_not_wait():
    waits: list = []

    assert call_with_retry(lambda: "ok", policy(waits)) == "ok"
    assert waits == []


def test_temporary_failures_are_retried_until_success():
    waits: list = []
    outcomes = iter([busy(), busy(), "ok"])
    seen: list = []

    def operation():
        outcome = next(outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    result = call_with_retry(
        operation, policy(waits), on_retry=lambda *details: seen.append(details)
    )

    assert result == "ok"
    assert len(waits) == 2
    assert [(attempt, total) for attempt, total, _, _ in seen] == [(1, 3), (2, 3)]


def test_waits_grow_and_stay_under_the_maximum():
    waits: list = []
    with pytest.raises(ServiceError):
        call_with_retry(lambda: (_ for _ in ()).throw(busy()), policy(waits, max_attempts=6))

    assert len(waits) == 5
    assert 0.5 <= waits[0] <= 1.0  # about 1 second, with jitter
    assert 1.0 <= waits[1] <= 2.0  # about 2 seconds
    assert 2.0 <= waits[2] <= 4.0  # about 4 seconds
    assert all(wait <= 8.0 for wait in waits)


def test_the_wait_the_service_asks_for_is_used_but_capped():
    assert RetryPolicy().delay_before_retry(1, busy(retry_after=3)) == 3
    assert RetryPolicy().delay_before_retry(1, busy(retry_after=300)) == 8.0


def test_gives_up_after_the_last_attempt():
    waits: list = []
    calls = []

    def operation():
        calls.append(1)
        raise busy()

    with pytest.raises(ServiceError):
        call_with_retry(operation, policy(waits))

    assert len(calls) == 3 and len(waits) == 2


def test_permanent_failures_are_not_retried():
    waits: list = []
    calls = []

    def operation():
        calls.append(1)
        raise wrong_key()

    with pytest.raises(ServiceError):
        call_with_retry(operation, policy(waits))

    assert len(calls) == 1 and waits == []


def test_a_bug_is_not_retried():
    waits: list = []
    with pytest.raises(ZeroDivisionError):
        call_with_retry(lambda: 1 / 0, policy(waits))

    assert waits == []


# --- Sorting model errors into "try again" and "don't" --------------------------------

REQUEST = httpx2.Request("POST", "https://example.invalid/v1/messages")


def status_error(status: int, headers: dict | None = None) -> anthropic.APIStatusError:
    response = httpx2.Response(status, headers=headers or {}, request=REQUEST)
    return anthropic.APIStatusError("boom", response=response, body=None)


@pytest.mark.parametrize(
    "status, kind",
    [(429, "rate_limit"), (500, "server_error"), (503, "server_error"), (529, "server_error"), (408, "timeout")],
)
def test_temporary_http_errors_are_retryable(status, kind):
    error = to_service_error(status_error(status))

    assert error.retryable and error.kind == kind and error.service == "model"


@pytest.mark.parametrize(
    "status, kind",
    [(400, "bad_request"), (401, "auth"), (403, "permission"), (404, "not_found")],
)
def test_permanent_http_errors_are_not_retryable(status, kind):
    error = to_service_error(status_error(status))

    assert not error.retryable and error.kind == kind


def test_retry_after_header_is_read():
    assert to_service_error(status_error(429, {"retry-after": "2"})).retry_after == 2.0
    assert to_service_error(status_error(429)).retry_after is None


def test_network_problems_and_timeouts_are_retryable():
    connection = to_service_error(anthropic.APIConnectionError(request=REQUEST))
    timeout = to_service_error(anthropic.APITimeoutError(request=REQUEST))

    assert (connection.retryable, connection.kind) == (True, "connection")
    assert (timeout.retryable, timeout.kind) == (True, "timeout")


def test_the_provider_raises_our_own_error_type():
    class BrokenMessages:
        def create(self, **_request):
            raise status_error(503)

    class BrokenClient:
        messages = BrokenMessages()

    provider = AnthropicSDKProvider(BrokenClient(), "some-model", 1000)
    with pytest.raises(ServiceError) as caught:
        provider.create_message(system="s", messages=[], tools=[])

    assert caught.value.retryable


def test_real_clients_are_built_without_their_own_retries(monkeypatch):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    monkeypatch.setenv("SUPPORT_AGENT_REQUEST_TIMEOUT_SECONDS", "45")
    from support_agent.providers import create_provider

    provider = create_provider(Settings.from_env())

    assert provider._client.max_retries == 0
    assert provider._client.timeout == 45


# --- Sorting embedding errors ---------------------------------------------------------


def aws_error(code: str, status: int) -> ClientError:
    return ClientError(
        {"Error": {"Code": code}, "ResponseMetadata": {"HTTPStatusCode": status}}, "InvokeModel"
    )


def test_aws_errors_are_sorted():
    throttled = embeddings.to_service_error(aws_error("ThrottlingException", 429))
    denied = embeddings.to_service_error(aws_error("AccessDeniedException", 403))
    offline = embeddings.to_service_error(EndpointConnectionError(endpoint_url="https://x"))
    no_keys = embeddings.to_service_error(NoCredentialsError())

    assert throttled.retryable and throttled.service == "embeddings"
    assert not denied.retryable and denied.kind == "AccessDeniedException"
    assert offline.retryable
    assert not no_keys.retryable


def make_titan(client) -> TitanEmbedder:
    embedder = TitanEmbedder.__new__(TitanEmbedder)  # skip connecting to AWS
    embedder._client = client
    embedder._model_id = "test-model"
    embedder.name = "test"
    return embedder


def test_titan_failures_and_unreadable_answers_become_service_errors():
    class Throttled:
        def invoke_model(self, **_request):
            raise aws_error("ThrottlingException", 429)

    class Garbled:
        def invoke_model(self, **_request):
            return {"body": io.BytesIO(b"this is not json")}

    class Good:
        def invoke_model(self, **_request):
            return {"body": io.BytesIO(json.dumps({"embedding": [0.6, 0.8]}).encode())}

    with pytest.raises(ServiceError) as throttled:
        make_titan(Throttled()).embed("hello")
    with pytest.raises(ServiceError) as garbled:
        make_titan(Garbled()).embed("hello")

    assert throttled.value.retryable
    assert not garbled.value.retryable and garbled.value.kind == "bad_response"
    assert make_titan(Good()).embed("hello") == [0.6, 0.8]


# --- The whole agent when things go wrong ---------------------------------------------


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    for name in ("SUPPORT_AGENT_MODEL", "SUPPORT_AGENT_LOG_FILE", "SUPPORT_AGENT_MAX_ATTEMPTS"):
        monkeypatch.delenv(name, raising=False)
    return dataclasses.replace(
        Settings.from_env(),
        max_steps=6,
        cache_dir=tmp_path,
        log_file=tmp_path / "logs" / "agent.jsonl",
    )


def build(settings, knowledge_base, orders, tickets, responses, waits):
    resources = Resources(FakeProvider(responses), knowledge_base, orders, tickets)
    agent, session = create_agent(
        settings, resources, PRIYA, today=TODAY, retry_policy=policy(waits)
    )
    return agent, session, resources.provider


def events_named(settings, name):
    return [event for event in read_events(settings.log_file) if event["event"] == name]


def test_a_busy_model_is_retried_and_the_customer_gets_a_normal_reply(
    settings, knowledge_base, orders, tickets
):
    waits: list = []
    agent, _, provider = build(
        settings, knowledge_base, orders, tickets, [busy(), busy(), text_response("Hello!")], waits
    )
    result = agent.run("Hi")

    assert result.outcome == COMPLETED and result.reply == "Hello!"
    assert len(provider.requests) == 3 and len(waits) == 2
    assert result.steps == 1  # retries do not use up the step limit
    assert tickets.all() == []

    retries = events_named(settings, "retry")
    assert [(e["operation"], e["attempt"], e["max_attempts"]) for e in retries] == [
        ("model_call", 1, 3),
        ("model_call", 2, 3),
    ]
    assert retries[0]["error_kind"] == "rate_limit" and retries[0]["wait_ms"] > 0
    assert events_named(settings, "error") == []


def test_a_model_that_stays_down_ends_with_a_ticket_not_a_crash(
    settings, knowledge_base, orders, tickets
):
    waits: list = []
    agent, _, provider = build(settings, knowledge_base, orders, tickets, [busy()], waits)
    history: list = []
    result = agent.run("Where is my order JL-10231?", history)

    assert result.outcome == MODEL_ERROR
    assert len(provider.requests) == 3
    (ticket,) = tickets.all()
    assert result.reply == fallback_reply(ticket["ticket_id"])
    assert "could not be reached" in ticket["summary"] and "JL-10231" in ticket["summary"]
    assert [message["role"] for message in history] == ["user", "assistant"]

    (error,) = events_named(settings, "error")
    assert (error["operation"], error["error_kind"], error["retryable"]) == (
        "model_call",
        "rate_limit",
        True,
    )
    assert events_named(settings, "turn_end")[0]["outcome"] == "model_error"


def test_a_wrong_key_fails_straight_away_without_retries(settings, knowledge_base, orders, tickets):
    waits: list = []
    agent, _, provider = build(settings, knowledge_base, orders, tickets, [wrong_key()], waits)
    result = agent.run("Hi")

    assert result.outcome == MODEL_ERROR
    assert len(provider.requests) == 1 and waits == []
    assert events_named(settings, "retry") == []


def test_the_conversation_continues_after_a_failed_turn(settings, knowledge_base, orders, tickets):
    waits: list = []
    agent, _, _ = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [wrong_key(), text_response("Hello again!")],
        waits,
    )
    history: list = []
    first = agent.run("Hi", history)
    second = agent.run("Are you there?", history)

    assert first.outcome == MODEL_ERROR
    assert second.outcome == COMPLETED and second.reply == "Hello again!"


class FlakyEmbedder(FakeEmbedder):
    """Fails a set number of times, then works."""

    def __init__(self, failures: int, retryable: bool = True) -> None:
        super().__init__()
        self.failures = failures
        self.retryable = retryable

    def embed(self, text: str) -> list[float]:
        if self.failures > 0:
            self.failures -= 1
            raise ServiceError(
                "throttled", service="embeddings", kind="ThrottlingException", retryable=self.retryable
            )
        return super().embed(text)


SEARCH_THEN_ANSWER = [
    tool_response(ToolCall("c1", "search_knowledge_base", {"query": "How long is the return window?"})),
    text_response("You can return most items within 30 days of delivery."),
]


def flaky_knowledge_base(failures: int, retryable: bool = True):
    embedder = FlakyEmbedder(0)
    knowledge_base = KnowledgeBase.build(DATA_DIR / "knowledge_base", embedder)
    embedder.failures, embedder.retryable = failures, retryable
    return knowledge_base


def test_a_search_that_fails_once_is_retried(settings, orders, tickets):
    waits: list = []
    agent, _, provider = build(
        settings, flaky_knowledge_base(1), orders, tickets, SEARCH_THEN_ANSWER, waits
    )
    result = agent.run("How long is the return window?")

    assert result.outcome == COMPLETED and len(waits) == 1
    tool_result = provider.requests[1]["messages"][2]["content"][0]
    assert "is_error" not in tool_result and "30 days" in tool_result["content"]
    (retry,) = events_named(settings, "retry")
    assert retry["operation"] == "embedding"


def test_a_search_that_stays_down_tells_the_model_to_hand_over(settings, orders, tickets):
    waits: list = []
    agent, _, provider = build(
        settings,
        flaky_knowledge_base(99),
        orders,
        tickets,
        [
            SEARCH_THEN_ANSWER[0],
            tool_response(
                ToolCall("c2", "escalate_to_human", {"reason": "unsure_of_answer", "summary": "Search down."})
            ),
            text_response("I couldn't check our documents just now, so I've asked the team."),
        ],
        waits,
    )
    result = agent.run("How long is the return window?")

    tool_result = provider.requests[1]["messages"][2]["content"][0]
    assert tool_result["is_error"] is True
    assert "temporarily unavailable" in tool_result["content"]
    assert "Do not answer from memory" in tool_result["content"]
    assert result.escalated and len(tickets.all()) == 1
    assert events_named(settings, "error")[0]["operation"] == "embedding"


class BrokenTickets(TicketStore):
    """A ticket store whose file cannot be written."""

    def __init__(self, path, failures: int = 99) -> None:
        super().__init__(path)
        self.failures = failures

    def create(self, **details):
        if self.failures > 0:
            self.failures -= 1
            raise TicketError("The ticket file could not be written (PermissionError).")
        return super().create(**details)


ESCALATE = tool_response(
    ToolCall("c1", "escalate_to_human", {"reason": "human_requested", "summary": "Wants a person."})
)


def test_a_ticket_file_that_is_briefly_locked_is_retried(settings, knowledge_base, orders, tmp_path):
    waits: list = []
    tickets = BrokenTickets(tmp_path / "tickets.jsonl", failures=1)
    agent, session, _ = build(
        settings, knowledge_base, orders, tickets, [ESCALATE, text_response("Done.")], waits
    )
    agent.run("I want a human")

    assert len(tickets.all()) == 1 and len(session.ticket_ids) == 1
    assert events_named(settings, "retry")[0]["operation"] == "ticket_write"


def test_no_ticket_number_is_promised_when_the_ticket_cannot_be_saved(
    settings, knowledge_base, orders, tmp_path
):
    waits: list = []
    tickets = BrokenTickets(tmp_path / "tickets.jsonl")
    agent, session, provider = build(
        settings,
        knowledge_base,
        orders,
        tickets,
        [ESCALATE, text_response(f"Sorry, please email {SUPPORT_EMAIL}.")],
        waits,
    )
    result = agent.run("I want a human")

    tool_result = provider.requests[1]["messages"][2]["content"][0]
    assert tool_result["is_error"] is True
    assert "no ticket exists" in tool_result["content"] and SUPPORT_EMAIL in tool_result["content"]
    assert session.ticket_ids == [] and "TCK-" not in result.reply
    assert events_named(settings, "ticket_created") == []


def test_everything_failing_at_once_still_gives_a_polite_reply(
    settings, knowledge_base, orders, tmp_path
):
    waits: list = []
    tickets = BrokenTickets(tmp_path / "tickets.jsonl")
    agent, _, _ = build(settings, knowledge_base, orders, tickets, [busy()], waits)
    result = agent.run("Hi")

    assert result.outcome == MODEL_ERROR
    assert result.reply == fallback_reply()  # points to the support email
    assert SUPPORT_EMAIL in result.reply and result.auto_ticket_id is None
    operations = [event["operation"] for event in events_named(settings, "error")]
    assert operations == ["model_call", "ticket_write", "auto_escalate"]


# --- Starting up with bad data files --------------------------------------------------


def test_damaged_lines_in_the_ticket_file_are_skipped(tmp_path):
    path = tmp_path / "tickets.jsonl"
    store = TicketStore(path)
    store.create(customer_email=PRIYA, reason="other", summary="one")
    with path.open("a", encoding="utf-8") as file:
        file.write("{damaged\n\n")
    store.create(customer_email=PRIYA, reason="other", summary="two")

    assert [ticket["summary"] for ticket in store.all()] == ["one", "two"]


def test_a_real_unwritable_ticket_file_raises_a_ticket_error(tmp_path):
    folder_in_the_way = tmp_path / "tickets.jsonl"
    folder_in_the_way.mkdir()

    with pytest.raises(TicketError):
        TicketStore(folder_in_the_way).create(customer_email=PRIYA, reason="other", summary="x")


def test_index_progress_is_saved_when_embedding_fails_part_way(tmp_path):
    folder = tmp_path / "docs"
    folder.mkdir()
    (folder / "a.md").write_text("# Doc\n\n## One\nFirst.\n\n## Two\nSecond.\n", encoding="utf-8")
    cache = tmp_path / "cache.json"

    class FailsOnSecond(FakeEmbedder):
        def embed(self, text):
            if self.calls == 1:
                raise ServiceError("down", service="embeddings", kind="x", retryable=False)
            return super().embed(text)

    with pytest.raises(ServiceError):
        KnowledgeBase.build(folder, FailsOnSecond(), cache_path=cache)

    second_try = FakeEmbedder()
    KnowledgeBase.build(folder, second_try, cache_path=cache)
    assert second_try.calls == 1  # only the section that failed is embedded again


@pytest.mark.parametrize(
    "orders_text, expected",
    [(None, "missing or damaged"), ("{not json", "missing or damaged"), ('{"customers": []}', "missing or damaged")],
)
def test_a_bad_orders_file_is_explained_in_plain_words(
    settings, monkeypatch, tmp_path, orders_text, expected
):
    orders_file = tmp_path / "orders.json"
    if orders_text is not None:
        orders_file.write_text(orders_text, encoding="utf-8")
    monkeypatch.setattr("support_agent.app.create_embedder", lambda *args, **kwargs: FakeEmbedder())
    broken = dataclasses.replace(settings, orders_file=orders_file)

    with pytest.raises(ConfigError, match=expected):
        load_resources(broken)


def test_an_empty_documents_folder_is_explained_in_plain_words(settings, monkeypatch, tmp_path):
    monkeypatch.setattr("support_agent.app.create_embedder", lambda *args, **kwargs: FakeEmbedder())
    empty = tmp_path / "no_docs"
    empty.mkdir()

    with pytest.raises(ConfigError, match="could not be loaded"):
        load_resources(dataclasses.replace(settings, knowledge_base_dir=empty))


def test_bad_retry_settings_are_rejected(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("SUPPORT_AGENT_MAX_ATTEMPTS", "0")
    with pytest.raises(ConfigError, match="SUPPORT_AGENT_MAX_ATTEMPTS"):
        Settings.from_env()
