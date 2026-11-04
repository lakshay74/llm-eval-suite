"""Collects pass/fail per test category and writes results/summary.{json,md}."""
import json
from collections import defaultdict
from pathlib import Path

from bot.bot import live_mode

_results = defaultdict(lambda: {"passed": 0, "failed": 0})


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    category = Path(report.nodeid.split("::")[0]).stem.replace("test_", "")
    _results[category]["passed" if report.passed else "failed"] += 1


def pytest_sessionfinish(session, exitstatus):
    out = Path("results")
    out.mkdir(exist_ok=True)
    mode = "live (Groq LLM)" if live_mode() else "mock (offline)"
    (out / "summary.json").write_text(json.dumps({"mode": mode, "categories": _results}, indent=2))
    lines = [f"Mode: {mode}", "", "| Category | Passed | Failed | Pass rate |", "|---|---|---|---|"]
    for cat, r in _results.items():
        total = r["passed"] + r["failed"]
        lines.append(f"| {cat} | {r['passed']} | {r['failed']} | {100 * r['passed'] // max(total, 1)}% |")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
