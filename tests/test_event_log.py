"""Tests for the event log: what is recorded, and that personal data is masked."""

from __future__ import annotations

import dataclasses
import json
import re

import pytest
from conftest import MARCUS, PRIYA, TODAY
from fakes import FakeProvider, text_response, tool_response

from support_agent import event_log
from support_agent.app import Resources, create_agent
from support_agent.config import Settings
from support_agent.event_log import EventLogger, customer_ref, mask_text, mask_value, read_events
from support_agent.providers.base import ToolCall

ANY_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+")

# --- Masking text ------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "Contact me at priya.nair@example.com please",
        "PRIYA.NAIR@EXAMPLE.COM",
        "two: a.b@shop.co.uk and c_d+tag@mail.example.org.",
        "<marcus.bell@example.com>",
        "mailto:someone@sub.domain.example",
    ],
)
def test_emails_are_masked(text):
    masked = mask_text(text)

    assert "[EMAIL]" in masked
    assert not ANY_EMAIL.search(masked)


@pytest.mark.parametrize(
    "text",
    [
        "Call me on +1 (512) 555-0147",
        "My number is 512-555-0147.",
        "phone 5125550147",
        "+44 20 7946 0958",
        "Ring (512) 555 0147 after 5",
    ],
)
def test_phone_numbers_are_masked(text):
    masked = mask_text(text)

    assert "[PHONE]" in masked
    assert "555" not in masked and "7946" not in masked


def test_long_digit_runs_such_as_card_numbers_are_masked():
    assert mask_text("card 4111 1111 1111 1111 exp") == "card [NUMBER] exp"


@pytest.mark.parametrize(
    "text",
    [
        "I live at 42 Oak Street, Austin",
        "Send it to 1600 Pennsylvania Avenue",
        "Address: 7 Maple Tree Lane, Apt 4B",
        "221B Baker Street",
    ],
)
def test_street_addresses_are_masked(text):
    masked = mask_text(text)

    assert "[ADDRESS]" in masked
    assert "Oak" not in masked and "Pennsylvania" not in masked
    assert "Maple" not in masked and "Baker" not in masked


@pytest.mark.parametrize(
    "text",
    [
        "Order JL-10231 was delivered on 2026-11-07.",
        "Tracking number TRK7002317785",
        "Your ticket is TCK-20261113-A8C008.",
        "The total was $129.00 and the fee is $6.99.",
        "Refunds take 5-7 business days; the window is 30 days.",
        "2026-09-18 plus 1 year is 2027-09-18 (Saturday 18 September 2027).",
        "Juniper Lane Goods is open 9:00 am to 6:00 pm.",
        "It used 44597 tokens in 12345 ms.",
    ],
)
def test_ordinary_shop_text_is_left_alone(text):
    assert mask_text(text) == text


def test_fields_named_like_personal_data_are_masked_whole():
    masked = mask_value(
        {
            "customer_email": "not-even-an-email",
            "phone": "ask reception",
            "shipping_address": {"street": "Flat above the bakery", "zip": "78701"},
            "order_id": "JL-10231",
        }
    )

    assert masked == {
        "customer_email": "[EMAIL]",
        "phone": "[PHONE]",
        "shipping_address": {"street": "[ADDRESS]", "zip": "[ADDRESS]"},
        "order_id": "JL-10231",
    }


def test_masking_reaches_into_lists_and_nested_dictionaries():
    masked = mask_value({"a": [{"b": ["x priya.nair@example.com y"]}], "n": 3, "ok": True})

    assert masked == {"a": [{"b": ["x [EMAIL] y"]}], "n": 3, "ok": True}


# --- Customer codes ----------------------------------------------------------------


def test_customer_code_is_stable_and_does_not_contain_the_email():
    first = customer_ref(PRIYA, "salt-one")

    assert first == customer_ref("  Priya.Nair@Example.com ", "salt-one")
    assert first != customer_ref(MARCUS, "salt-one")
    assert first != customer_ref(PRIYA, "salt-two")
    assert "priya" not in first and "@" not in first


# --- Writing and reading events ----------------------------------------------------


def test_every_line_has_the_common_fields(tmp_path):
    path = tmp_path / "logs" / "agent.jsonl"
    logger = EventLogger(path, conversation_id="conv_test", customer_ref="cust_abc")
    logger.turn = 2
    logger.log(event_log.MODEL_CALL, step=1, input_tokens=100, output_tokens=20, cost_usd=0.0002)

    (line,) = path.read_text(encoding="utf-8").splitlines()
    event = json.loads(line)
    assert event["v"] == event_log.SCHEMA_VERSION
    assert event["event"] == "model_call"
    assert event["conversation_id"] == "conv_test"
    assert event["customer_ref"] == "cust_abc"
    assert event["turn"] == 2
    assert event["input_tokens"] == 100
    assert event["ts"].endswith("+00:00")


def test_personal_data_hidden_in_a_dictionary_key_is_still_masked(tmp_path):
    path = tmp_path / "agent.jsonl"
    EventLogger(path, "conv_test", "cust_abc").log("tool_call", input={PRIYA: "value"})

    assert not ANY_EMAIL.search(path.read_text(encoding="utf-8"))


def test_events_can_be_read_back_for_one_conversation(tmp_path):
    path = tmp_path / "agent.jsonl"
    EventLogger(path, "conv_a", "cust_1").log("turn_start", message="hello")
    EventLogger(path, "conv_b", "cust_2").log("turn_start", message="hi")
    with path.open("a", encoding="utf-8") as file:
        file.write("this line is damaged\n")

    assert len(list(read_events(path))) == 2
    assert [event["message"] for event in read_events(path, "conv_b")] == ["hi"]


def test_a_log_file_that_cannot_be_written_does_not_stop_the_agent(tmp_path, capsys):
    folder_in_the_way = tmp_path / "agent.jsonl"
    folder_in_the_way.mkdir()
    logger = EventLogger(folder_in_the_way, "conv_test", "cust_abc")

    logger.log("turn_start", message="hello")
    logger.log("turn_start", message="again")

    assert capsys.readouterr().err.count("Warning") == 1  # warned once, not per line


# --- A whole conversation, checked in the log file --------------------------------

NASTY_MESSAGE = (
    f"Hi, my email is {PRIYA}. My husband's email is {MARCUS}. Call me on "
    "+1 (512) 555-0147 or 512-555-0199. I live at 42 Oak Street, Austin. "
    "My card is 4111 1111 1111 1111. Where is order JL-10231?"
)


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("SUPPORT_AGENT_MODEL", raising=False)
    monkeypatch.delenv("SUPPORT_AGENT_LOG_FILE", raising=False)
    return dataclasses.replace(
        Settings.from_env(), max_steps=6, log_file=tmp_path / "logs" / "agent.jsonl"
    )


def run_conversation(settings, knowledge_base, orders, tickets, responses, messages):
    resources = Resources(FakeProvider(responses), knowledge_base, orders, tickets)
    agent, session = create_agent(settings, resources, PRIYA, today=TODAY)
    history: list = []
    results = [agent.run(message, history) for message in messages]
    return results, session, list(read_events(settings.log_file))


def test_a_normal_turn_is_logged_from_start_to_end(settings, knowledge_base, orders, tickets):
    results, session, events = run_conversation(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(
                ToolCall("c1", "lookup_order", {"order_id": "JL-10231"}),
                input_tokens=1000,
                output_tokens=50,
            ),
            text_response("It was delivered on 2026-11-07.", input_tokens=1500, output_tokens=40),
        ],
        ["Where is order JL-10231?"],
    )

    assert [event["event"] for event in events] == [
        "conversation_start",
        "turn_start",
        "model_call",
        "tool_call",
        "model_call",
        "turn_end",
    ]
    # One conversation ID and one customer code run through every line.
    assert {event["conversation_id"] for event in events} == {session.logger.conversation_id}
    assert len({event["customer_ref"] for event in events}) == 1
    assert events[0]["turn"] == 0 and events[-1]["turn"] == 1

    start = events[0]
    assert start["provider"] == "bedrock" and start["date_used"] == "2026-11-12"

    first_call, tool, second_call, end = events[2:]
    assert (first_call["step"], first_call["input_tokens"], first_call["output_tokens"]) == (1, 1000, 50)
    assert first_call["cost_usd"] == pytest.approx(0.00125)
    assert first_call["tools_requested"] == ["lookup_order"]
    assert first_call["duration_ms"] >= 0
    assert tool["tool"] == "lookup_order" and tool["input"] == {"order_id": "JL-10231"}
    assert tool["is_error"] is False and "delivered" in tool["result_preview"]
    assert second_call["stop_reason"] == "end_turn"

    assert end["outcome"] == "completed"
    assert (end["input_tokens"], end["output_tokens"], end["steps"]) == (2500, 90, 2)
    assert end["cost_usd"] == pytest.approx(0.00295)
    assert end["tools_used"] == ["lookup_order"]
    assert end["escalated"] is False
    assert end["reply"] == "It was delivered on 2026-11-07."
    assert results[0].cost_usd == pytest.approx(0.00295)


def test_rewrite_block_and_ticket_are_logged(settings, knowledge_base, orders, tickets):
    _, session, events = run_conversation(
        settings,
        knowledge_base,
        orders,
        tickets,
        [text_response("Express shipping costs $3.00.")],  # repeated on the rewrite
        ["How much is express shipping?"],
    )

    names = [event["event"] for event in events]
    assert names == [
        "conversation_start",
        "turn_start",
        "model_call",
        "reply_rewrite",
        "tool_call",  # the harness searched the documents for the model
        "model_call",
        "reply_blocked",
        "ticket_created",
        "turn_end",
    ]
    rewrite, forced_search, retry_call, blocked, ticket, end = events[3:]
    # Two rules fire: nothing was looked up, and the price is not in any source.
    both = ["unverified_policy", "ungrounded_figure"]
    assert rewrite["rules"] == both and "$3.00" in rewrite["details"]
    assert forced_search["tool"] == "search_knowledge_base"
    assert retry_call["is_rewrite"] is True and events[2]["is_rewrite"] is False
    # After the search, only the made-up price is still wrong.
    assert blocked["rules"] == ["ungrounded_figure"]
    assert ticket["created_by"] == "harness" and ticket["reason"] == "other"
    assert ticket["ticket_id"] == end["auto_ticket_id"] == session.ticket_ids[0]
    assert end["outcome"] == "reply_blocked" and end["escalated"] is True
    assert end["violations"] == ["ungrounded_figure"]
    # The ticket file points back at the same conversation.
    assert tickets.all()[0]["conversation_id"] == session.logger.conversation_id


def test_a_ticket_created_by_the_model_is_logged(settings, knowledge_base, orders, tickets):
    _, _, events = run_conversation(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(
                ToolCall(
                    "c1",
                    "escalate_to_human",
                    {"reason": "refund_request", "summary": "Wants a refund.", "order_id": "JL-10231"},
                )
            ),
            text_response("I've created a ticket for the team."),
        ],
        ["I want a refund for JL-10231"],
    )

    (ticket,) = [event for event in events if event["event"] == "ticket_created"]
    assert ticket["created_by"] == "model"
    assert (ticket["reason"], ticket["order_id"]) == ("refund_request", "JL-10231")


def test_turn_numbers_count_up_through_a_conversation(settings, knowledge_base, orders, tickets):
    _, _, events = run_conversation(
        settings,
        knowledge_base,
        orders,
        tickets,
        [text_response("Hello."), text_response("Goodbye.")],
        ["Hi", "Bye"],
    )

    ends = [event for event in events if event["event"] == "turn_end"]
    assert [event["turn"] for event in ends] == [1, 2]


def test_no_raw_personal_data_reaches_the_log_file(settings, knowledge_base, orders, tickets):
    """The main privacy test: personal data arrives through every route (the
    customer's message, a tool input, a ticket summary, the model's reply, and
    the signed-in email itself) and none of it may appear in the log file."""
    run_conversation(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(
                ToolCall("c1", "search_knowledge_base", {"query": f"orders for {MARCUS}"}),
                ToolCall("c2", "lookup_order", {"order_id": "JL-10231", "email": PRIYA}),
            ),
            tool_response(
                ToolCall(
                    "c3",
                    "escalate_to_human",
                    {
                        "reason": "other",
                        "summary": f"Customer {PRIYA}, phone 512-555-0199, at 42 Oak Street.",
                    },
                ),
                text=f"I'll note your email {PRIYA} and number +1 (512) 555-0147.",
            ),
            text_response(f"Your husband's address {MARCUS} is noted."),  # gets blocked
        ],
        [NASTY_MESSAGE, f"Also email {MARCUS} about it"],
    )

    log_text = settings.log_file.read_text(encoding="utf-8")

    assert log_text.count("\n") >= 10  # the conversation really was logged
    assert not ANY_EMAIL.search(log_text)
    assert "@" not in log_text
    for fragment in ("priya", "marcus", "nair", "example.com", "555", "Oak Street", "4111"):
        assert fragment.lower() not in log_text.lower(), fragment
    # The masks are there instead, and the useful details survive.
    for expected in ("[EMAIL]", "[PHONE]", "[ADDRESS]", "[NUMBER]", "JL-10231", "cust_"):
        assert expected in log_text, expected


def test_the_ticket_file_keeps_the_real_email_for_the_support_team(
    settings, knowledge_base, orders, tickets
):
    # Tickets are the support team's working record, not a log: they need to
    # know who to reply to. This test documents that difference on purpose.
    run_conversation(
        settings,
        knowledge_base,
        orders,
        tickets,
        [
            tool_response(
                ToolCall("c1", "escalate_to_human", {"reason": "other", "summary": "Needs help."})
            ),
            text_response("Done."),
        ],
        ["Help"],
    )

    assert tickets.all()[0]["customer_email"] == PRIYA
    assert not ANY_EMAIL.search(settings.log_file.read_text(encoding="utf-8"))
