"""Golden dataset: answerable questions must contain a key fact;
unanswerable questions must be refused (no hallucination)."""
import json
from pathlib import Path

import pytest
from bot.bot import answer

CASES = json.loads((Path(__file__).parent.parent / "data" / "golden.json").read_text())
REFUSAL_MARKERS = ["can't find", "cannot find", "not in the document", "no information", "don't have"]


@pytest.mark.parametrize("case", [c for c in CASES if c["answerable"]], ids=lambda c: c["question"][:40])
def test_answerable_contains_fact(case):
    reply = answer(case["question"]).lower()
    assert any(k in reply for k in case["expected_any"]), f"Missing expected fact in: {reply!r}"


@pytest.mark.parametrize("case", [c for c in CASES if not c["answerable"]], ids=lambda c: c["question"][:40])
def test_unanswerable_is_refused(case):
    reply = answer(case["question"]).lower()
    assert any(m in reply for m in REFUSAL_MARKERS), f"Possible hallucination: {reply!r}"
