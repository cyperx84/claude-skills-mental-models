#!/usr/bin/env python3
"""LLM-judge module for the mental-models eval harness.

Grades a response against a rubric using the Anthropic SDK with structured
tool-use output for reliable parsing.

Rubric (each criterion scored 0-2):
    a. model_selection   - Did the response apply the expected mental models
                           (or defensible alternatives)?
    b. reasoning_quality - Does it walk the model's thinking steps, not just
                           name-drop?
    c. actionability     - Does it give the user something concrete to do?

Total score 0-6; pass threshold = 4.

Known limitations:
- Same-model grading (generator and judge can be the same model) introduces
  bias. Treat scores as indicative, not authoritative.
- Rubric is subjective; two runs may differ by +/- 1 point per criterion.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from typing import Any

PASS_THRESHOLD = 4
MAX_SCORE = 6


@dataclass
class JudgeResult:
    scores: dict[str, int] = field(default_factory=dict)
    total: int = 0
    pass_: bool = False
    rationale: str = ""


JUDGE_SYSTEM = """You are a strict but fair grader evaluating whether an AI
assistant applied Charlie Munger-style mental models to a user's problem.

You will be given:
- The user's prompt
- The expected mental models a thoughtful human would reach for
- The assistant's response

Grade the response on three criteria, each 0-2:

1. model_selection (0-2):
   0 = applied none of the expected models or defensible alternatives
   1 = applied one relevant model, or named models without substance
   2 = applied two or more expected models (or clearly defensible alternatives)
       with genuine engagement

2. reasoning_quality (0-2):
   0 = name-drops models without working through their logic
   1 = walks through reasoning for at least one model
   2 = genuinely walks the thinking steps of multiple models, not just labels

3. actionability (0-2):
   0 = vague or abstract, no concrete next step
   1 = some concrete suggestions but mixed with vagueness
   2 = clear, concrete, actionable guidance the user can act on today

Be honest. A pass (total >= 4) should mean the response genuinely helped."""


JUDGE_TOOL = {
    "name": "submit_grade",
    "description": "Submit the rubric scores and rationale for the response.",
    "input_schema": {
        "type": "object",
        "properties": {
            "model_selection": {
                "type": "integer",
                "minimum": 0,
                "maximum": 2,
                "description": "0-2 score for model selection criterion",
            },
            "reasoning_quality": {
                "type": "integer",
                "minimum": 0,
                "maximum": 2,
                "description": "0-2 score for reasoning quality criterion",
            },
            "actionability": {
                "type": "integer",
                "minimum": 0,
                "maximum": 2,
                "description": "0-2 score for actionability criterion",
            },
            "rationale": {
                "type": "string",
                "description": "2-4 sentence explanation of the scores.",
            },
        },
        "required": [
            "model_selection",
            "reasoning_quality",
            "actionability",
            "rationale",
        ],
    },
}


def _require_sdk() -> Any:
    try:
        import anthropic  # type: ignore
    except ImportError:
        print(
            "error: `anthropic` package not installed. Run `pip install anthropic`.",
            file=sys.stderr,
        )
        sys.exit(2)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "error: ANTHROPIC_API_KEY not set in environment.",
            file=sys.stderr,
        )
        sys.exit(2)
    return anthropic


def judge_response(
    case: dict,
    response: str,
    model: str = "claude-opus-4-6",
) -> JudgeResult:
    """Grade a response against the rubric. Returns a JudgeResult."""
    anthropic = _require_sdk()
    client = anthropic.Anthropic()

    user_msg = (
        f"USER PROMPT:\n{case['prompt']}\n\n"
        f"EXPECTED MENTAL MODELS: {', '.join(case['expected_models'])}\n\n"
        f"CATEGORY: {case.get('category', 'n/a')}\n\n"
        f"ASSISTANT RESPONSE:\n{response}\n\n"
        "Grade the response using the submit_grade tool."
    )

    msg = client.messages.create(
        model=model,
        max_tokens=1024,
        system=JUDGE_SYSTEM,
        tools=[JUDGE_TOOL],
        tool_choice={"type": "tool", "name": "submit_grade"},
        messages=[{"role": "user", "content": user_msg}],
    )

    tool_input: dict[str, Any] | None = None
    for block in msg.content:
        if getattr(block, "type", None) == "tool_use":
            tool_input = block.input  # type: ignore[assignment]
            break

    if not tool_input:
        return JudgeResult(
            scores={},
            total=0,
            pass_=False,
            rationale="judge did not return a tool_use block",
        )

    scores = {
        "model_selection": int(tool_input.get("model_selection", 0)),
        "reasoning_quality": int(tool_input.get("reasoning_quality", 0)),
        "actionability": int(tool_input.get("actionability", 0)),
    }
    total = sum(scores.values())
    return JudgeResult(
        scores=scores,
        total=total,
        pass_=total >= PASS_THRESHOLD,
        rationale=str(tool_input.get("rationale", "")),
    )


if __name__ == "__main__":
    # smoke test the dataclass
    r = JudgeResult(scores={"x": 1}, total=1, pass_=False, rationale="demo")
    print(json.dumps({"scores": r.scores, "total": r.total, "pass": r.pass_}))
