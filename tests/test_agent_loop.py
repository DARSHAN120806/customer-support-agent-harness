"""Tests for the core agent loop, using a fake model."""

from __future__ import annotations

from fakes import FakeProvider, stopped_response, text_response, tool_response

from support_agent.agent import COMPLETED, MODEL_STOPPED, STEP_LIMIT, Agent
from support_agent.prompts import fallback_reply

FALLBACK_REPLY = fallback_reply()
from support_agent.providers.base import ToolCall
from support_agent.tools import Tool, ToolRegistry


def make_registry() -> ToolRegistry:
    def broken(_input):
        raise RuntimeError("secret internal detail")

    registry = ToolRegistry()
    registry.register(
        Tool(
            name="echo",
            description="Repeats the given text.",
            input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
            handler=lambda tool_input: f"echo: {tool_input['text']}",
        )
    )
    registry.register(
        Tool(
            name="act",
            description="Does something for the customer.",
            input_schema={"type": "object"},
            handler=lambda _input: "done",
            read_only=False,
        )
    )
    registry.register(
        Tool(name="broken", description="Always fails.", input_schema={"type": "object"}, handler=broken)
    )
    return registry


def make_agent(provider: FakeProvider, max_steps: int = 5) -> Agent:
    return Agent(provider, make_registry(), system_prompt="test prompt", max_steps=max_steps)


def test_plain_reply_finishes_in_one_step():
    provider = FakeProvider([text_response("Hello!")])
    result = make_agent(provider).run("Hi")

    assert result.reply == "Hello!"
    assert result.outcome == COMPLETED
    assert result.steps == 1
    assert provider.requests[0]["system"] == "test prompt"
    assert provider.requests[0]["messages"] == [{"role": "user", "content": "Hi"}]


def test_tool_is_run_and_its_result_is_sent_back_to_the_model():
    provider = FakeProvider(
        [tool_response(ToolCall("call_1", "echo", {"text": "abc"})), text_response("Done.")]
    )
    result = make_agent(provider).run("Please echo abc")

    assert result.reply == "Done."
    assert result.steps == 2
    second_request = provider.requests[1]["messages"]
    assert second_request[1]["role"] == "assistant"
    assert second_request[2] == {
        "role": "user",
        "content": [{"type": "tool_result", "tool_use_id": "call_1", "content": "echo: abc"}],
    }


def test_several_tool_calls_are_answered_in_one_message():
    provider = FakeProvider(
        [
            tool_response(
                ToolCall("call_1", "echo", {"text": "a"}),
                ToolCall("call_2", "echo", {"text": "b"}),
            ),
            text_response("Done."),
        ]
    )
    make_agent(provider).run("Echo twice")

    results = provider.requests[1]["messages"][2]["content"]
    assert [block["tool_use_id"] for block in results] == ["call_1", "call_2"]


def test_step_limit_stops_a_model_that_never_finishes():
    provider = FakeProvider([tool_response(ToolCall("call_1", "echo", {"text": "again"}))])
    result = make_agent(provider, max_steps=3).run("Loop forever")

    assert result.outcome == STEP_LIMIT
    assert result.reply == FALLBACK_REPLY
    assert result.steps == 3
    assert len(provider.requests) == 3


def test_failing_tool_is_reported_to_the_model_without_internal_details():
    provider = FakeProvider(
        [tool_response(ToolCall("call_1", "broken", {})), text_response("Sorry, that failed.")]
    )
    result = make_agent(provider).run("Use the broken tool")

    block = provider.requests[1]["messages"][2]["content"][0]
    assert block["is_error"] is True
    assert "secret internal detail" not in block["content"]
    assert result.outcome == COMPLETED


def test_unknown_tool_is_reported_as_an_error():
    provider = FakeProvider(
        [tool_response(ToolCall("call_1", "issue_refund", {})), text_response("I can't do that.")]
    )
    make_agent(provider).run("Refund me")

    block = provider.requests[1]["messages"][2]["content"][0]
    assert block["is_error"] is True


def test_cut_off_or_declined_reply_is_replaced_by_the_fallback():
    for stop_reason in ("max_tokens", "refusal"):
        provider = FakeProvider([stopped_response(stop_reason, text="Half a sent")])
        result = make_agent(provider).run("Hi")

        assert result.outcome == MODEL_STOPPED
        assert result.reply == FALLBACK_REPLY


def test_tokens_are_added_up_across_steps():
    provider = FakeProvider(
        [
            tool_response(ToolCall("call_1", "echo", {"text": "a"}), input_tokens=100, output_tokens=20),
            text_response("Done.", input_tokens=150, output_tokens=30),
        ]
    )
    result = make_agent(provider).run("Hi")

    assert (result.input_tokens, result.output_tokens) == (250, 50)


def test_history_continues_across_customer_messages():
    provider = FakeProvider([text_response("First."), text_response("Second.")])
    agent = make_agent(provider)
    history: list = []

    agent.run("One", history)
    agent.run("Two", history)

    roles = [message["role"] for message in provider.requests[1]["messages"]]
    assert roles == ["user", "assistant", "user"]
    assert [message["role"] for message in history] == ["user", "assistant", "user", "assistant"]


def test_text_written_while_looking_things_up_is_not_shown():
    provider = FakeProvider(
        [
            tool_response(ToolCall("call_1", "echo", {"text": "a"}), text="Let me check that."),
            text_response("You can return it within 30 days."),
        ]
    )
    result = make_agent(provider).run("Can I return this?")

    assert result.reply == "You can return it within 30 days."


def test_text_written_when_taking_an_action_is_part_of_the_reply():
    provider = FakeProvider(
        [
            tool_response(ToolCall("call_1", "echo", {"text": "a"}), text="Let me check that."),
            tool_response(ToolCall("call_2", "act", {}), text="You can return it within 30 days."),
            text_response("Your ticket number is TCK-1."),
        ]
    )
    result = make_agent(provider).run("I want to return this")

    assert result.reply == "You can return it within 30 days.\n\nYour ticket number is TCK-1."
