#!/usr/bin/env python3
"""Inject Prompt Gate mode into Claude Code before each submitted prompt."""

from __future__ import annotations

import json
import re
import sys
from typing import Any


APPROVAL_RE = re.compile(
    r"^\s*(?:ЗАПУСКАЙ|ВЫПОЛНЯЙ|EXECUTE|RUN)(?:\b|\s*:)",
    flags=re.IGNORECASE,
)

REVIEW_CONTEXT = (
    "PROMPT GATE — REVIEW MODE. Apply the prompt-gate skill before acting. "
    "Review and optimize this request, use only minimal read-only inspection or "
    "official-doc lookup, make no mutable changes, and wait for explicit "
    "ЗАПУСКАЙ or EXECUTE approval."
)

EXECUTE_CONTEXT = (
    "PROMPT GATE — EXECUTE MODE. The user explicitly approved execution. "
    "Execute the last proposed prompt without reviewing it again. If no proposed "
    "prompt exists in this conversation and none follows the approval marker, "
    "ask the user to provide it instead of guessing."
)


def read_input() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def main() -> int:
    payload = read_input()
    prompt = payload.get("prompt", "")
    if not isinstance(prompt, str):
        prompt = ""

    context = EXECUTE_CONTEXT if APPROVAL_RE.match(prompt) else REVIEW_CONTEXT
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    json.dump(output, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
