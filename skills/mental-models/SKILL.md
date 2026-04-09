---
name: mental-models
description: Apply Charlie Munger's latticework of 98 mental models to any problem. Use when user requests decision analysis, says "help me think", "apply mental model", mentions model names (inversion, bottlenecks, second-order thinking), or needs structured thinking frameworks.
---

# Mental Models

Apply 98 cognitive frameworks from multiple disciplines to analyze problems,
make decisions, and think more clearly.

This skill is backed by the **`mental-models` CLI** — the canonical interface.
The CLI does selection, lookup, and structured application in one command. No
file walking, no hand-parsing. Prefer the CLI.

## When to Activate

- User names a specific model ("apply inversion", "use bottlenecks")
- User asks "help me think through X" or "what model fits X"
- User requests decision analysis, trade-off evaluation, or structured reasoning
- User describes a complex/ambiguous problem and wants a framework

## Preflight: is the CLI available?

Run once per session via OpenClaw's `exec` tool:

```bash
mental-models doctor --json
```

**`{"ok": true, ...}`** → use the CLI workflow below.

**Command not found** → try `uvx mental-models doctor --json` (runs from PyPI
without install — requires `uv` on PATH). If that also fails, tell the user:

> Install with: `pip install mental-models` (or `uv tool install mental-models`).

## CLI Workflow

### Step 1 — Select models for the problem

```bash
mental-models select "<paraphrased problem>" -k 5 --json
```

Returns a JSON object with a `models` array. Each entry has `slug`, `name`,
`category`, `description`, `keywords`, `path`. Pick **2–3** that best fit —
prefer cross-category coverage (that's the latticework).

### Step 2 — Get structured guidance for each chosen model

```bash
mental-models apply <slug> --problem "<user's problem>" --json
```

Returns:

- `description` — what the model is
- `thinking_steps` — the sequential framework (walk verbatim, don't paraphrase)
- `coaching_questions` — prompts to deepen the analysis
- `when_to_avoid` — failure modes (always check and surface if relevant)

### Step 3 — Synthesize

- Walk each model's `thinking_steps` against the user's facts
- Show where the models agree, where they disagree
- End with 3–5 concrete, actionable next steps
- Name any "when to avoid" conditions that apply to this case

### Other useful commands

```bash
mental-models get <slug>                 # full markdown
mental-models get <slug> --field keywords
mental-models list --category "Human Nature"
mental-models categories
mental-models which                      # resolved data path
```

All commands support `--json`. Exit codes: 0 ok, 2 not found, 3 bad args.

## Discovery Heuristics (bias your `select` query)

- **Risk / uncertainty / reversibility** → inversion, probabilistic thinking, margin of safety
- **Stuck / can't see options** → first principles, second-order thinking, reframing
- **Conflict / negotiation / competition** → incentives, asymmetric warfare, trade-offs
- **Complex system / unintended effects** → feedback loops, emergence, bottlenecks, leverage
- **Performance / optimization** → bottlenecks, diminishing returns, efficiency
- **People / team / behavior** → incentives, social proof, biases
- **Communication / persuasion** → framing, audience, contrast

## Core Guidelines

1. **Max 3 models per analysis** — quality over quantity
2. **Follow `thinking_steps` verbatim** — don't paraphrase the framework away
3. **Always check `when_to_avoid`** — warn the user if the model misfits
4. **Latticework**: show how chosen models connect and where they disagree
5. **Be actionable**: end with concrete next steps, not theory

## Install the CLI

```bash
# one-shot (recommended)
uvx mental-models select "your question"

# or install globally
pip install mental-models
# or
uv tool install mental-models
```

Source: <https://github.com/cyperx84/claude-skills-mental-models>
