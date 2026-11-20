"""Run the evaluation set and report how many cases the agent handled correctly.

    python evals/run_evals.py              run every case (asks before spending money)
    python evals/run_evals.py --list       show the cases without running anything
    python evals/run_evals.py --category attack
    python evals/run_evals.py --case refund-in-window --case easy-order-status
    python evals/run_evals.py --yes        skip the "are you sure" question
    python evals/run_evals.py --harness off             code checks switched off
    python evals/run_evals.py --save-baseline my_run    also save a read-only copy
                                                        to evals/baselines/my_run.json

Each run makes real, paid calls to the model. Results are saved in
evals/results/<date-time>/ : results.json (scores), agent.jsonl (the event log),
and tickets.jsonl (the tickets the agent created).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import shutil
import stat
import re
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from support_agent.app import load_resources
from support_agent.config import PROJECT_ROOT, ConfigError, Settings
from support_agent.evaluation import (
    CaseFileError,
    VIOLATION_TYPES,
    CaseResult,
    count_violations,
    customer_emails,
    grade,
    load_cases,
    result_to_dict,
    run_case,
    summarize,
)
from support_agent.retry import ServiceError

EVALS_DIR = Path(__file__).resolve().parent
BASELINE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
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
    parser.add_argument(
        "--harness",
        choices=["on", "off"],
        default="on",
        help="'off' switches off every code check, to measure what they prevent.",
    )
    parser.add_argument(
        "--save-baseline",
        metavar="NAME",
        help="Also save the results, read-only, as evals/baselines/NAME.json.",
    )
    args = parser.parse_args(argv)
    harness = args.harness == "on"

    baseline_path = None
    if args.save_baseline:
        if not BASELINE_NAME.match(args.save_baseline):
            print("--save-baseline may only use letters, digits, '-', '_' and '.'.", file=sys.stderr)
            return 2
        baseline_path = EVALS_DIR / "baselines" / f"{args.save_baseline}.json"
        # Checked before anything is spent: a saved baseline is never replaced.
        if baseline_path.exists():
            print(f"{baseline_path} already exists and is never overwritten. "
                  "Choose another name.", file=sys.stderr)
            return 2

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
    print(f"{len(cases)} cases, model {settings.model}, date pinned to {today}, "
          f"harness {args.harness.upper()}.")
    if not harness:
        print("The code checks are OFF: replies reach the 'customer' unchecked. "
              "This is for measurement only.")
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
        run = run_case(settings, resources, case, today, harness=harness)
        run.violations = count_violations(case, run, all_emails)
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
                "harness": args.harness,
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
    if baseline_path:
        save_baseline(run_dir / "results.json", baseline_path)
        print(f"Baseline saved (read-only): {baseline_path}")
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

    found = {kind: n for kind, n in summary["violations"].items() if n}
    print("  Rule violations the customer would have seen: "
          + (", ".join(f"{kind} {n}" for kind, n in found.items()) if found else "none"))

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


def save_baseline(source: Path, target: Path) -> None:
    """Copy the results to the baselines folder and make the copy read-only."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"{target} already exists and is never overwritten.")
    shutil.copyfile(source, target)
    os.chmod(target, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)


if __name__ == "__main__":
    sys.exit(main())
