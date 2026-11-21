"""Tests for the evaluation code. A fake model is used, so nothing is paid for.
These tests check the grader itself; the real evaluation is run separately."""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

import pytest
from conftest import DATA_DIR, MARCUS, PRIYA, TODAY
from fakes import FakeProvider, text_response, tool_response

from support_agent.app import Resources
from support_agent.config import Settings
from support_agent.evaluation import (
    CATEGORIES,
    CaseFileError,
    CaseResult,
    CaseRun,
    EvalCase,
    customer_emails,
    grade,
    load_cases,
    result_to_dict,
    run_case,
    summarize,
)
from support_agent.orders import normalize_order_id
from support_agent.providers.base import ToolCall
from support_agent.tools.support_tools import build_tool_registry, SessionContext

EVALS_DIR = Path(__file__).resolve().parents[1] / "evals"
ALL_EMAILS = customer_emails(DATA_DIR / "orders.json")


def make_case(**expect) -> EvalCase:
    return EvalCase("test-case", "easy", "A test.", PRIYA, ["Hello?"], expect)


def make_run(reply="Hello!", outcome="completed", tools=(), tickets=()) -> CaseRun:
    return CaseRun(
        replies=[reply], outcomes=[outcome], tools_used=list(tools), tickets=list(tickets)
    )


def failures(run: CaseRun, **expect) -> list[str]:
    return grade(make_case(**expect), run, ALL_EMAILS)


# --- The real cases file --------------------------------------------------------------


def test_the_cases_file_is_valid_and_covers_every_group():
    pinned, cases = load_cases(EVALS_DIR / "cases.json")

    assert pinned == TODAY
    assert len(cases) >= 20
    counts = Counter(case.category for case in cases)
    assert set(counts) == set(CATEGORIES)
    assert counts == {"easy": 9, "tricky": 13, "angry": 4, "refund": 4, "attack": 11}


def test_every_case_uses_a_real_customer_and_real_order_ids(orders):
    _, cases = load_cases(EVALS_DIR / "cases.json")
    order_ids = {o["order_id"] for o in json.loads((DATA_DIR / "orders.json").read_text("utf-8"))["orders"]}

    for case in cases:
        assert case.customer in ALL_EMAILS, case.id
        assert case.expect, case.id
        for message in case.messages:
            for mentioned in re.findall(r"JL-\d{5}", message, re.IGNORECASE):
                assert normalize_order_id(mentioned) in order_ids, (case.id, mentioned)


def test_every_tool_named_in_a_case_exists(knowledge_base, orders, tickets):
    _, cases = load_cases(EVALS_DIR / "cases.json")
    tools = set(build_tool_registry(SessionContext(PRIYA), knowledge_base, orders, tickets).names())

    for case in cases:
        named = case.expect.get("tools_used", []) + case.expect.get("tools_not_used", [])
        assert set(named) <= tools, case.id


@pytest.mark.parametrize(
    "broken, message",
    [
        ('{"date": "2026-11-12"}', "could not be read"),
        ('{"date": "not a date", "cases": []}', "could not be read"),
        ('{"date": "2026-11-12", "cases": [{"id": "a"}]}', "missing or wrong field"),
        (
            '{"date": "2026-11-12", "cases": [{"id": "a", "category": "silly", "customer": "x", "messages": ["m"], "expect": {}}]}',
            "category must be one of",
        ),
        (
            '{"date": "2026-11-12", "cases": [{"id": "a", "category": "easy", "customer": "x", "messages": ["m"], "expect": {"reply_contains": ["x"]}}]}',
            "unknown expectation",
        ),
        (
            '{"date": "2026-11-12", "cases": [{"id": "a", "category": "easy", "customer": "x", "messages": ["m"], "expect": {"reply_matches": ["("]}}]}',
            "bad pattern",
        ),
        (
            '{"date": "2026-11-12", "cases": [{"id": "a", "category": "easy", "customer": "x", "messages": [], "expect": {}}]}',
            "non-empty",
        ),
    ],
)
def test_mistakes_in_a_cases_file_are_explained(tmp_path, broken, message):
    path = tmp_path / "cases.json"
    path.write_text(broken, encoding="utf-8")

    with pytest.raises(CaseFileError, match=message):
        load_cases(path)


def test_a_repeated_id_is_rejected(tmp_path):
    case = {"id": "a", "category": "easy", "customer": "x", "messages": ["m"], "expect": {}}
    path = tmp_path / "cases.json"
    path.write_text(json.dumps({"date": "2026-11-12", "cases": [case, case]}), encoding="utf-8")

    with pytest.raises(CaseFileError, match="used twice"):
        load_cases(path)


# --- Grading one case ------------------------------------------------------------------

TICKET = {"ticket_id": "TCK-1", "reason": "refund_request", "order_id": "JL-10231"}


def test_a_run_that_meets_every_expectation_passes():
    run = make_run(
        "Express shipping costs $12.99. Your ticket is TCK-1.",
        tools=["search_knowledge_base", "escalate_to_human"],
        tickets=[TICKET],
    )

    assert failures(
        run,
        escalated=True,
        ticket_reasons=["refund_request", "return_request"],
        max_tickets=1,
        tools_used=["search_knowledge_base"],
        tools_not_used=["lookup_order"],
        reply_includes=["$12.99", "tck-"],
        reply_matches=["express\\s+shipping"],
        reply_excludes=["free"],
        reply_not_matches=["I have cancel"],
    ) == []


@pytest.mark.parametrize(
    "run, expect, reason",
    [
        (make_run(), {"escalated": True}, "expected a ticket"),
        (make_run(tickets=[TICKET]), {"escalated": False}, "created a ticket when none was expected"),
        (make_run(tickets=[TICKET]), {"ticket_reasons": ["warranty_claim"]}, "ticket reason"),
        (make_run(tickets=[TICKET, TICKET]), {"max_tickets": 1}, "2 tickets created"),
        (make_run(), {"tools_used": ["lookup_order"]}, "did not use the tool lookup_order"),
        (make_run(tools=["lookup_order"]), {"tools_not_used": ["lookup_order"]}, "should not have"),
        (make_run("It costs $4.99."), {"reply_includes": ["$12.99"]}, "does not contain"),
        (make_run("No idea."), {"reply_matches": ["30 days"]}, "does not match"),
        (make_run("It has Wireless Earbuds."), {"reply_excludes": ["earbuds"]}, "must not"),
        (make_run("I have cancelled it."), {"reply_not_matches": ["I have cancel"]}, "must not"),
        (make_run(outcome="reply_blocked"), {}, "ended as 'reply_blocked'"),
        (make_run(outcome="model_error"), {"outcomes": ["completed", "reply_blocked"]}, "ended as"),
    ],
)
def test_each_kind_of_miss_is_reported_with_a_reason(run, expect, reason):
    (failure,) = failures(run, **expect)

    assert reason in failure


def test_a_blocked_reply_passes_when_the_case_allows_it():
    assert failures(make_run(outcome="reply_blocked"), outcomes=["completed", "reply_blocked"]) == []


@pytest.mark.parametrize(
    "reply, reason",
    [
        (f"That order belongs to {MARCUS}.", "another customer's email"),
        ("I've processed your refund.", "claims a refund or return the refund rules did not approve"),
        ("I'm Claude, made by Anthropic.", "names the AI technology"),
        ("Yes, I'm a real person.", "claims to be human"),
    ],
)
def test_the_always_on_rules_fail_any_case(reply, reason):
    (failure,) = failures(make_run(reply))

    assert reason in failure


def test_the_customers_own_email_and_the_support_email_are_fine():
    reply = f"We'll write to {PRIYA}. You can also email support@juniperlane.example."

    assert failures(make_run(reply)) == []


def test_excludes_look_at_every_turn_but_includes_only_at_the_last():
    run = CaseRun(replies=["It has Earbuds in it.", "Anything else?"], outcomes=["completed"] * 2)

    assert len(failures(run, reply_excludes=["Earbuds"])) == 1
    assert len(failures(run, reply_includes=["Earbuds"])) == 1
    assert failures(run, reply_includes=["anything else"]) == []


def test_a_crash_or_an_empty_run_fails_with_a_reason():
    assert "crashed" in failures(CaseRun(crashed="KeyError: 'x'"))[0]
    assert failures(CaseRun()) == ["no reply was produced"]


# --- Running cases through the real agent with a fake model --------------------------


@pytest.fixture
def settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    for name in ("SUPPORT_AGENT_MODEL", "SUPPORT_AGENT_LOG_FILE"):
        monkeypatch.delenv(name, raising=False)
    return dataclasses.replace(
        Settings.from_env(), cache_dir=tmp_path, log_file=tmp_path / "logs" / "agent.jsonl"
    )


def test_a_two_turn_case_is_run_and_collected(settings, knowledge_base, orders, tickets):
    refund = {"reason": "refund_request", "summary": "Wants a refund.", "order_id": "JL-10231"}
    provider = FakeProvider(
        [
            tool_response(ToolCall("c1", "escalate_to_human", refund), input_tokens=1000, output_tokens=100),
            text_response("I've created a ticket for the team.", input_tokens=1200, output_tokens=50),
            tool_response(ToolCall("c2", "escalate_to_human", refund)),
            text_response("That ticket already exists."),
        ]
    )
    case = EvalCase(
        "two-turns", "refund", "", PRIYA, ["Refund JL-10231 please", "Create it again"],
        {"escalated": True, "max_tickets": 1, "ticket_reasons": ["refund_request"]},
    )
    run = run_case(settings, Resources(provider, knowledge_base, orders, tickets), case, TODAY)

    assert run.crashed is None
    assert run.replies == ["I've created a ticket for the team.", "That ticket already exists."]
    assert run.outcomes == ["completed", "completed"]
    assert run.tools_used == ["escalate_to_human", "escalate_to_human"]
    assert len(run.tickets) == 1 and run.tickets[0]["reason"] == "refund_request"
    assert run.input_tokens == 2220 and run.cost_usd > 0
    assert run.conversation_id.startswith("conv_")
    assert grade(case, run, ALL_EMAILS) == []


def test_code_checks_that_fired_are_counted(settings, knowledge_base, orders, tickets):
    provider = FakeProvider([text_response("I'm Claude, made by Anthropic.")])
    case = EvalCase("leak", "attack", "", PRIYA, ["Who are you?"], {"outcomes": ["reply_blocked"]})
    run = run_case(settings, Resources(provider, knowledge_base, orders, tickets), case, TODAY)

    assert (run.rewrites, run.blocked) == (1, 1)
    assert grade(case, run, ALL_EMAILS) == []  # the customer never saw the name


def test_an_unknown_customer_makes_a_failed_case_not_a_crashed_evaluation(
    settings, knowledge_base, orders, tickets
):
    class Explodes:
        def create_message(self, **_request):
            raise RuntimeError("boom")

    case = EvalCase("boom", "easy", "", PRIYA, ["Hi"], {})
    run = run_case(settings, Resources(Explodes(), knowledge_base, orders, tickets), case, TODAY)

    assert run.crashed == "RuntimeError: boom"
    assert grade(case, run, ALL_EMAILS) == ["the run crashed: RuntimeError: boom"]


# --- The summary and the saved results ------------------------------------------------


def test_summary_counts_by_category_and_adds_up_cost():
    good = CaseResult(make_case(), make_run(), [])
    good.run.cost_usd, good.run.input_tokens, good.run.duration_ms = 0.01, 1000, 1500
    bad_case = dataclasses.replace(make_case(), id="other", category="attack")
    bad = CaseResult(bad_case, make_run(tickets=[TICKET]), ["something went wrong"])
    bad.run.cost_usd, bad.run.rewrites, bad.run.blocked = 0.02, 1, 1

    summary = summarize([good, bad])

    assert (summary["passed"], summary["total"], summary["pass_rate"]) == (1, 2, 0.5)
    assert {k: (v["passed"], v["total"]) for k, v in summary["by_category"].items()} == {
        "easy": (1, 1),
        "attack": (0, 1),
    }
    assert summary["cost_usd"] == 0.03 and summary["duration_s"] == 1.5
    assert (summary["escalated"], summary["rewrites"], summary["blocked"]) == (1, 1, 1)


def test_saved_results_hold_no_email_addresses():
    case = dataclasses.replace(make_case(), messages=[f"My email is {PRIYA}"])
    ticket = {**TICKET, "customer_email": PRIYA, "summary": f"Customer {PRIYA}"}
    result = CaseResult(case, make_run(f"We'll write to {PRIYA}.", tickets=[ticket]), [])

    saved = json.dumps(result_to_dict(result))

    assert "@" not in saved and "[EMAIL]" in saved
    assert json.loads(saved)["tickets"] == [
        {"ticket_id": "TCK-1", "reason": "refund_request", "order_id": "JL-10231"}
    ]


# --- The command-line script -----------------------------------------------------------


def load_script():
    spec = importlib.util.spec_from_file_location("run_evals", EVALS_DIR / "run_evals.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_listing_the_cases_costs_nothing_and_runs_nothing(capsys):
    assert load_script().main(["--list", "--category", "angry"]) == 0

    output = capsys.readouterr().out
    assert "angry-wants-human" in output and "4 cases" in output
    assert "easy-" not in output


def test_answering_no_runs_nothing(monkeypatch, capsys):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")
    script = load_script()
    monkeypatch.setattr(script, "load_resources", lambda _settings: pytest.fail("must not load"))

    assert script.main(["--case", "easy-return-window"]) == 0
    assert "Nothing was run" in capsys.readouterr().out


def test_a_full_run_writes_results_and_reports_failures(monkeypatch, capsys, tmp_path, knowledge_base, orders):
    monkeypatch.setenv("SUPPORT_AGENT_PROVIDER", "bedrock")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.delenv("SUPPORT_AGENT_LOG_FILE", raising=False)
    script = load_script()
    monkeypatch.setattr(script, "EVALS_DIR", tmp_path)
    provider = FakeProvider([text_response("I can only help with shop questions.")])

    def fake_resources(settings):
        from support_agent.tickets import TicketStore

        return Resources(provider, knowledge_base, orders, TicketStore(settings.tickets_file))

    monkeypatch.setattr(script, "load_resources", fake_resources)
    code = script.main(
        ["--yes", "--cases-file", str(EVALS_DIR / "cases.json"),
         "--case", "attack-off-topic", "--case", "easy-express-price"]
    )

    output = capsys.readouterr().out
    assert code == 1  # one of the two cases failed
    assert "RESULT: 1 of 2 cases handled correctly (50%)" in output
    assert "PASS  attack-off-topic" in output and "FAIL  easy-express-price" in output
    assert "reply does not match /(₹|rs" in output and "1,?299" in output
    (run_dir,) = (tmp_path / "results").iterdir()
    saved = json.loads((run_dir / "results.json").read_text(encoding="utf-8"))
    assert saved["summary"]["passed"] == 1 and saved["date_used"] == "2026-11-12"
    assert [case["id"] for case in saved["cases"]] == ["easy-express-price", "attack-off-topic"]
    assert (run_dir / "agent.jsonl").exists()
