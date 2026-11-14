"""Run the evaluation set and report how many cases the agent handled correctly.

    python evals/run_evals.py              run every case (asks before spending money)
    python evals/run_evals.py --list       show the cases without running anything
    python evals/run_evals.py --category attack
    python evals/run_evals.py --case refund-in-window --case easy-order-status
    python evals/run_evals.py --yes        skip the "are you sure" question

Each run makes real, paid calls to the model. Results are saved in
evals/results/<date-time>/ : results.json (scores), agent.jsonl (the event log),
and tickets.jsonl (the tickets the agent created).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from support_agent.app import load_resources
from support_agent.config import PROJECT_ROOT, ConfigError, Settings
from support_agent.evaluation import (
    CaseFileError,
    CaseResult,
    customer_emails,
    grade,
    load_cases,
    result_to_dict,
    run_case,
    summarize,
)
from support_agent.retry import ServiceError

EVALS_DIR = Path(__file__).resolve().parent
# A rough figure from earlier live runs, used only for the warning before a run.
ROUGH_COST_PER_CASE_USD = 0.012


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Run the support agent evaluation set.")
    parser.add_argument("--cases-file", type=Path, default=EVALS_DIR / "cases.json")
    parser.add_argument("--category", action="append", help="Only run this category.")
    parser.add_argument("--case", action="append", help="Only run the case with this id.")
    parser.add_argument("--list", action="store_true", help="List the cases and stop.")
    parser.add_argument("--yes", action="store_true", help="Do not ask before running.")
    args = parser.parse_args(argv)

    try:
        today, cases = load_cases(args.cases_file)
    except CaseFileError as error:
        print(f"Problem with the cases file: {error}", file=sys.stderr)
        return 2

    # --category and --case add up: a case runs if it matches either one.
    if args.category or args.case:
        cases = [
            case
            for case in cases
            if case.category in (args.category or []) or case.id in (args.case or [])
        ]
    if not cases:
        print("No cases match.", file=sys.stderr)
        return 2

    if args.list:
        for case in cases:
            print(f"{case.category:<7} {case.id:<32} {case.description}")
        print(f"\n{len(cases)} cases")
        return 0

    load_dotenv(PROJECT_ROOT / ".env")
    try:
        settings = Settings.from_env()
    except ConfigError as error:
        print(f"Configuration problem: {error}", file=sys.stderr)
        return 2

    rough = len(cases) * ROUGH_COST_PER_CASE_USD
    print(f"{len(cases)} cases, model {settings.model}, date pinned to {today}.")
    print(f"This makes real, paid model calls. Rough cost: ${rough:.2f}.")
    if not args.yes:
        try:
            if input("Run it? (y/n) ").strip().lower() not in ("y", "yes"):
                print("Cancelled. Nothing was run.")
                return 0
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled. Nothing was run.")
            return 0

    # Each run gets its own folder, so the evaluation never touches the real
    # tickets or the real log.
    run_dir = EVALS_DIR / "results" / datetime.now().strftime("%Y%m%d-%H%M%S")
    settings = dataclasses.replace(
        settings, tickets_file=run_dir / "tickets.jsonl", log_file=run_dir / "agent.jsonl"
    )
    try:
        resources = load_resources(settings)
    except (ConfigError, ServiceError) as error:
        print(f"Could not start: {error}", file=sys.stderr)
        return 2
    all_emails = customer_emails(settings.orders_file)

    results: list[CaseResult] = []
    for number, case in enumerate(cases, start=1):
        run = run_case(settings, resources, case, today)
        result = CaseResult(case, run, grade(case, run, all_emails))
        results.append(result)
        mark = "PASS" if result.passed else "FAIL"
        print(f"[{number:>2}/{len(cases)}] {mark}  {case.id}")
        for failure in result.failures:
            print(f"          - {failure}")

    summary = summarize(results)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "results.json").write_text(
        json.dumps(
            {
                "run_at": datetime.now().isoformat(timespec="seconds"),
                "model": settings.model,
                "provider": settings.provider,
                "date_used": today.isoformat(),
                "summary": summary,
                "cases": [result_to_dict(result) for result in results],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print_report(results, summary, run_dir)
    return 0 if summary["passed"] == summary["total"] else 1


def print_report(results: list[CaseResult], summary: dict, run_dir: Path) -> None:
    print("\n" + "=" * 62)
    print(f"RESULT: {summary['passed']} of {summary['total']} cases handled correctly "
          f"({summary['pass_rate']:.0%})")
    print("=" * 62)
    for category, counts in summary["by_category"].items():
        print(f"  {category:<8} {counts['passed']:>2} / {counts['total']}")
    print(
        f"\n  Tickets created in {summary['escalated']} cases. "
        f"Code checks: {summary['rewrites']} rewrites, {summary['blocked']} blocked replies. "
        f"Retries: {summary['retries']}."
    )
    print(
        f"  Tokens: {summary['input_tokens']:,} in, {summary['output_tokens']:,} out. "
        f"Estimated cost ${summary['cost_usd']:.2f}. Model time {summary['duration_s']} s."
    )

    failed = [result for result in results if not result.passed]
    if failed:
        print("\nFAILED CASES")
        for result in failed:
            print(f"\n  {result.case.id}  ({result.case.description})")
            print(f"    Customer: {result.case.messages[-1][:200]}")
            if result.run.replies:
                print(f"    Agent:    {result.run.replies[-1][:400]}")
            for failure in result.failures:
                print(f"    Why:      {failure}")
    print(f"\nFull details: {run_dir / 'results.json'}")


if __name__ == "__main__":
    sys.exit(main())
