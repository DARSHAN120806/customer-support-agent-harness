"""Compare saved evaluation results side by side. Free: it only reads files.

    python evals/compare.py evals/baselines/a.json evals/baselines/b.json ...

Prints the cases passed per group, and the count of each kind of rule
violation, for every file given. Results saved before violations were counted
show "-" for the counts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from support_agent.evaluation import CATEGORIES, VIOLATION_TYPES


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["label"] = path.stem
    return data


def table(rows: list[list[str]]) -> str:
    """A plain-text table with columns lined up."""
    widths = [max(len(row[column]) for row in rows) for column in range(len(rows[0]))]
    lines = []
    for number, row in enumerate(rows):
        lines.append("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())
        if number == 0:
            lines.append("  ".join("-" * width for width in widths))
    return "\n".join(lines)


def compare(runs: list[dict]) -> str:
    header = ["", *(run["label"] for run in runs)]
    harness = ["harness", *(run.get("harness", "on").upper() for run in runs)]

    passed = [header, harness]
    for category in CATEGORIES:
        row = [category]
        for run in runs:
            counts = run["summary"]["by_category"].get(category, {"passed": 0, "total": 0})
            row.append(f"{counts['passed']} / {counts['total']}")
        passed.append(row)
    passed.append(["TOTAL", *(f"{r['summary']['passed']} / {r['summary']['total']}" for r in runs)])
    passed.append(["cost", *(f"${r['summary']['cost_usd']:.2f}" for r in runs)])

    violations = [header]
    for kind in [*VIOLATION_TYPES, "violation_total"]:
        row = [kind]
        for run in runs:
            if "violations" not in run["summary"]:
                row.append("-")
            elif kind == "violation_total":
                row.append(str(run["summary"]["violation_total"]))
            else:
                row.append(str(run["summary"]["violations"].get(kind, 0)))
        violations.append(row)

    by_group = [header]
    for category in CATEGORIES:
        row = [category]
        for run in runs:
            counts = run["summary"]["by_category"].get(category, {})
            row.append(str(sum(counts["violations"].values())) if "violations" in counts else "-")
        by_group.append(row)

    return (
        "CASES PASSED\n" + table(passed)
        + "\n\nRULE VIOLATIONS THE CUSTOMER WOULD HAVE SEEN\n" + table(violations)
        + "\n\nVIOLATIONS PER GROUP\n" + table(by_group)
    )


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Compare saved evaluation results.")
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)
    try:
        runs = [load(path) for path in args.files]
    except (OSError, ValueError, KeyError) as error:
        print(f"Could not read a results file: {error}", file=sys.stderr)
        return 2
    print(compare(runs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
