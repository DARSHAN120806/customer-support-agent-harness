"""The core agent loop.

One customer message is handled like this:

    1. Send the conversation to the model.
    2. If the model asks for tools, run them and send the results back. Go to 1.
    3. If the model writes a reply, check it, then return it to the customer.

The loop has hard limits (steps, tokens, cost), so the agent can never run
forever or run up an unlimited bill. Whenever the loop cannot produce a safe
reply, it hands the conversation to a human instead of guessing. Every step is
written to the event log.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from . import event_log
from .event_log import EventLogger, NullLogger
from .prompts import fallback_reply, handover_note
from .providers.base import ModelProvider, ToolCall
from .retry import RetryPolicy, ServiceError, call_with_retry
from .safety import Budget, Violation
from .tools.registry import ToolRegistry

# Why the loop ended.
COMPLETED = "completed"  # the model wrote a normal reply
STEP_LIMIT = "step_limit"  # the maximum number of steps was reached
BUDGET_LIMIT = "budget_limit"  # the token or cost limit was reached
MODEL_STOPPED = "model_stopped"  # the model stopped without a usable reply
REPLY_BLOCKED = "reply_blocked"  # the reply failed a safety check
MODEL_ERROR = "model_error"  # the model could not be reached, even after retries

CORRECTION_NOTE = (
    "Automatic check: the reply you just drafted was not shown to the customer, "
    "because {details}. Write the reply again. {hints}"
)

# Called when the loop gives up. Receives the reason, the customer's message, and
# whether the model already created a ticket during this message. It makes sure
# a ticket exists for the human team and returns the ticket number.
AutoEscalate = Callable[[str, str, bool], str]
# Called on the final reply, together with the conversation so far and the
# names of the tools used for this message. Returns the rules the reply breaks.
ReplyCheck = Callable[[str, list[dict[str, Any]], list[str]], list[Violation]]


@dataclass(frozen=True)
class AgentResult:
    reply: str
    outcome: str
    steps: int
    input_tokens: int
    output_tokens: int
    # The names of the tools that were run, in order.
    tools_used: list[str] = field(default_factory=list)
    # Set when the harness itself (not the model) created a ticket.
    auto_ticket_id: str | None = None
    # Names of the safety rules the reply broke.
    violations: list[str] = field(default_factory=list)
    # Why the loop gave up, when it did. Used in logs and tickets.
    gave_up_because: str | None = None
    # Estimated cost of this message in US dollars, when prices are known.
    cost_usd: float | None = None
    duration_ms: int = 0

    @property
    def escalated(self) -> bool:
        """True if this message ended up with the human support team."""
        return self.auto_ticket_id is not None or "escalate_to_human" in self.tools_used


class Agent:
    def __init__(
        self,
        provider: ModelProvider,
        tools: ToolRegistry,
        system_prompt: str,
        max_steps: int,
        budget: Budget | None = None,
        reply_check: ReplyCheck | None = None,
        auto_escalate: AutoEscalate | None = None,
        logger: EventLogger | NullLogger | None = None,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be 1 or more.")
        self._provider = provider
        self._tools = tools
        self._system_prompt = system_prompt
        self._max_steps = max_steps
        self._budget = budget
        self._reply_check = reply_check
        self._auto_escalate = auto_escalate
        self._log = logger or NullLogger()
        # Without a policy, a failed model call is not tried again.
        self._retry_policy = retry_policy or RetryPolicy(max_attempts=1)

    def run(
        self, customer_message: str, history: list[dict[str, Any]] | None = None
    ) -> AgentResult:
        """Handle one customer message and return the agent's reply.

        `history` holds the earlier messages of the same conversation. It is
        updated in place, so passing the same list again continues the chat.
        """
        messages = history if history is not None else []
        messages.append({"role": "user", "content": customer_message})

        started = time.perf_counter()
        self._log.turn += 1
        self._log.log(event_log.TURN_START, message=customer_message)

        input_tokens = 0
        output_tokens = 0
        tools_used: list[str] = []
        # The pieces of text that make up the reply. See _keeps_text below.
        reply_parts: list[str] = []
        steps = 0
        # Set when a draft reply failed a correctable check. It is added to the
        # instructions for one more attempt.
        correction: str | None = None
        if self._budget:
            self._budget.start_message()

        def finish(
            reply: str,
            outcome: str,
            auto_ticket_id: str | None = None,
            violations: list[Violation] | None = None,
            gave_up_because: str | None = None,
        ) -> AgentResult:
            """Build the result and write the closing log line for this message."""
            result = AgentResult(
                reply=reply,
                outcome=outcome,
                steps=steps,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                tools_used=tools_used,
                auto_ticket_id=auto_ticket_id,
                violations=[violation.rule for violation in violations or []],
                gave_up_because=gave_up_because,
                cost_usd=self._cost(input_tokens, output_tokens),
                duration_ms=_elapsed_ms(started),
            )
            self._log.log(
                event_log.TURN_END,
                outcome=result.outcome,
                steps=result.steps,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                cost_usd=result.cost_usd,
                duration_ms=result.duration_ms,
                tools_used=result.tools_used,
                escalated=result.escalated,
                auto_ticket_id=result.auto_ticket_id,
                violations=result.violations,
                gave_up_because=result.gave_up_because,
                reply=result.reply,
            )
            return result

        def give_up(outcome: str, why: str, violations: list[Violation] | None = None) -> AgentResult:
            """End the turn with a fixed, safe reply and hand over to a human."""
            already_escalated = "escalate_to_human" in tools_used
            ticket_id = self._safe_auto_escalate(why, customer_message, already_escalated)
            # With no ticket, the fixed reply gives the support email instead.
            reply = fallback_reply(ticket_id)
            messages.append({"role": "assistant", "content": reply})
            return finish(reply, outcome, ticket_id, violations, gave_up_because=why)

        for step in range(1, self._max_steps + 1):
            # Checked before every model call, including the first: a
            # conversation that has already used up its budget stops here.
            over_budget = self._budget.exceeded() if self._budget else None
            if over_budget:
                return give_up(BUDGET_LIMIT, over_budget)

            steps = step
            call_started = time.perf_counter()
            system = self._system_prompt + (f"\n\n{correction}" if correction else "")
            try:
                # A temporary failure (busy service, network blip) is tried
                # again after a short wait; each retry is written to the log.
                response = call_with_retry(
                    lambda: self._provider.create_message(
                        system=system, messages=messages, tools=self._tools.definitions()
                    ),
                    self._retry_policy,
                    on_retry=event_log.retry_recorder(self._log, "model_call", step=step),
                )
            except ServiceError as error:
                # Still failing, or a failure that retrying cannot fix. The
                # customer gets the fixed reply and a ticket instead of a crash.
                event_log.log_error(self._log, "model_call", error, step=step)
                return give_up(MODEL_ERROR, f"the model could not be reached ({error.kind})")
            input_tokens += response.input_tokens
            output_tokens += response.output_tokens
            if self._budget:
                self._budget.record(response.input_tokens, response.output_tokens)
            self._log.log(
                event_log.MODEL_CALL,
                step=step,
                duration_ms=_elapsed_ms(call_started),
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                cost_usd=self._cost(response.input_tokens, response.output_tokens),
                stop_reason=response.stop_reason,
                tools_requested=[call.name for call in response.tool_calls],
                is_rewrite=correction is not None,
            )

            if response.stop_reason == "tool_use" and response.tool_calls:
                # The model's own message goes back unchanged, followed by one
                # message holding the results of every tool it asked for.
                messages.append({"role": "assistant", "content": response.content})
                tools_used.extend(call.name for call in response.tool_calls)
                if response.text and self._keeps_text(response.tool_calls):
                    reply_parts.append(response.text)
                messages.append(
                    {
                        "role": "user",
                        "content": [self._run_tool(call, step) for call in response.tool_calls],
                    }
                )
                continue

            if response.stop_reason == "end_turn" and response.text:
                reply_parts.append(response.text)
                reply = "\n\n".join(reply_parts)
                violations = (
                    self._reply_check(reply, messages, tools_used) if self._reply_check else []
                )
                if violations:
                    details = "; ".join(violation.detail for violation in violations)
                    rules = [violation.rule for violation in violations]
                    if correction is None and all(v.correctable for v in violations):
                        # One chance to rewrite. The note goes into the
                        # instructions, not the conversation, so the customer's
                        # side of the chat stays exactly as they wrote it. The
                        # rejected draft is not shown and not kept in the history.
                        hints = " ".join(v.fix_hint for v in violations if v.fix_hint)
                        correction = CORRECTION_NOTE.format(details=details, hints=hints)
                        reply_parts.pop()
                        self._log.log(
                            event_log.REPLY_REWRITE, step=step, rules=rules, details=details
                        )
                        for number, violation in enumerate(violations):
                            if violation.run_tool:
                                self._run_tool_for_model(
                                    violation.run_tool, f"harness_{step}_{number}", step, messages
                                )
                                tools_used.append(violation.run_tool[0])
                        continue
                    if any(v.blocks_reply for v in violations):
                        self._log.log(
                            event_log.REPLY_BLOCKED, step=step, rules=rules, details=details
                        )
                        safe_replies = [v.safe_reply for v in violations]
                        if all(safe_replies) and not tools_used:
                            # A question about the assistant itself, with no
                            # shop work done: a fixed reply is enough, and no
                            # ticket is needed. (If tools were used, a real
                            # shop question is at stake, so a human gets it.)
                            reply = safe_replies[0]
                            messages.append({"role": "assistant", "content": reply})
                            return finish(reply, REPLY_BLOCKED, None, violations)
                        return give_up(
                            REPLY_BLOCKED, f"reply blocked by safety check: {details}", violations
                        )
                    # The reply is fine to show but a ticket is missing, so the
                    # harness creates it and tells the customer.
                    ticket_id = self._safe_auto_escalate(details, customer_message, False)
                    if ticket_id:
                        reply = f"{reply}\n\n{handover_note(ticket_id)}"
                        messages.append({"role": "assistant", "content": reply})
                        return finish(reply, COMPLETED, ticket_id, violations)
                messages.append({"role": "assistant", "content": response.content})
                return finish(reply, COMPLETED)

            # Anything else (the reply was cut off, the model declined, or it
            # returned nothing) is not safe to show.
            return give_up(MODEL_STOPPED, f"model stopped early ({response.stop_reason})")

        return give_up(STEP_LIMIT, f"step limit of {self._max_steps} reached")

    def _safe_auto_escalate(
        self, why: str, customer_message: str, already_escalated: bool
    ) -> str | None:
        """Ask the harness for a ticket. If even that fails (for example the
        ticket file cannot be written), carry on without one rather than crash."""
        if not self._auto_escalate:
            return None
        try:
            return self._auto_escalate(why, customer_message, already_escalated)
        except Exception as error:
            event_log.log_error(self._log, "auto_escalate", error)
            return None

    def _cost(self, input_tokens: int, output_tokens: int) -> float | None:
        return self._budget.cost_of(input_tokens, output_tokens) if self._budget else None

    def _keeps_text(self, calls: list[ToolCall]) -> bool:
        """Decide whether text written alongside tool calls is shown to the customer.

        Text written alongside look-ups is dropped: the model wrote it before it
        had the facts, so it is either filler ("let me check") or a guess. Text
        written alongside an action such as creating a ticket is kept: by then
        the model has the facts, and this is usually where it explains the
        policy before ending with a short closing line.
        """
        return any(self._tools.shows_text_alongside(call.name) for call in calls)

    def _run_tool_for_model(
        self, tool: tuple[str, dict[str, Any]], call_id: str, step: int, messages: list[dict[str, Any]]
    ) -> None:
        """Run a tool the model should have used, and add the call and its
        result to the conversation exactly as if the model had asked for it."""
        name, tool_input = tool
        messages.append(
            {
                "role": "assistant",
                "content": [{"type": "tool_use", "id": call_id, "name": name, "input": tool_input}],
            }
        )
        result = self._run_tool(ToolCall(id=call_id, name=name, input=tool_input), step)
        messages.append({"role": "user", "content": [result]})

    def _run_tool(self, call: ToolCall, step: int) -> dict[str, Any]:
        started = time.perf_counter()
        result = self._tools.execute(call.name, call.input)
        self._log.log(
            event_log.TOOL_CALL,
            step=step,
            tool=call.name,
            input=call.input,
            is_error=result.is_error,
            duration_ms=_elapsed_ms(started),
            result_chars=len(result.content),
            result_preview=result.content[:1000],
        )
        block: dict[str, Any] = {
            "type": "tool_result",
            "tool_use_id": call.id,
            "content": result.content,
        }
        if result.is_error:
            block["is_error"] = True
        return block


def _elapsed_ms(started: float) -> int:
    return round((time.perf_counter() - started) * 1000)
