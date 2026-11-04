"""Prompt-injection / jailbreak attempts: the reply must not contain forbidden strings."""
import json
from pathlib import Path

import pytest
from bot.bot import answer

ATTACKS = json.loads((Path(__file__).parent.parent / "data" / "injections.json").read_text())


@pytest.mark.parametrize("attack", ATTACKS, ids=lambda a: a["name"])
def test_injection_resisted(attack):
    reply = answer(attack["prompt"]).lower()
    leaked = [f for f in attack["forbidden"] if f in reply]
    assert not leaked, f"Attack '{attack['name']}' succeeded, reply contained {leaked}: {reply!r}"
