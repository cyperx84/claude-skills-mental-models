---
name: mental-models
description: Apply Charlie Munger's latticework of mental models to any problem. Use when user requests decision analysis, says "help me think", "apply mental model", mentions model names (inversion, bottlenecks, second-order thinking), or needs structured thinking frameworks.
---

# Mental Models

Apply 98 cognitive frameworks from multiple disciplines to analyze problems, make decisions, and think more clearly.

This skill is backed by the **`mental-models` CLI** — a single command that does model selection, lookup, and structured application. The CLI is the fast path; the fallback is reading files directly. Both work. Prefer the CLI.

## When to Activate

- User names a specific model ("apply inversion", "use bottlenecks")
- User asks "help me think through X" or "what model fits X"
- User requests decision analysis, trade-off evaluation, or structured reasoning
- User describes a complex/ambiguous problem and wants a framework

## Preflight: is the CLI available?

Run once per session:

```bash
mental-models doctor --json
```

**If it returns `{"ok": true, ...}`** → use the CLI workflow below.

**If the command is not found** → try `uvx mental-models doctor --json` (runs from PyPI without install). If that also fails, fall back to the **File Fallback** section at the bottom of this doc — you can still do everything by reading files directly from `models/`, `REFERENCE.md`, and `PATTERNS.md`.

## CLI Workflow (preferred)

### Step 1 — Select models for the problem

```bash
mental-models select "<user's question or paraphrased problem>" -k 5 --json
```

Returns a JSON object with a `models` array. Each entry has `slug`, `name`, `category`, `description`, `keywords`, `path`. Pick **2–3** that best fit — prefer cross-category coverage (that's the latticework).

### Step 2 — Get structured guidance for each chosen model

```bash
mental-models apply <slug> --problem "<user's problem>" --json
```

Returns:
- `description` — what the model is
- `thinking_steps` — the sequential framework (walk these verbatim, don't paraphrase)
- `coaching_questions` — prompts to deepen the analysis
- `when_to_avoid` — failure modes (always check and surface if relevant)

### Step 3 — Synthesize

- Walk each model's `thinking_steps` against the user's facts
- Show where the models agree, where they disagree
- End with 3–5 concrete, actionable next steps
- Name any "when to avoid" conditions that apply to this case

### Other useful CLI commands

```bash
mental-models get <slug>                 # full markdown for deep reading
mental-models get <slug> --field keywords
mental-models list --category "Human Nature"
mental-models categories
mental-models which                      # resolve data path
```

All commands support `--json`. Exit codes: 0 ok, 2 not found, 3 bad args.

## Discovery Heuristics (before calling select)

Match the problem's **shape** to bias your query terms:

- **Risk / uncertainty / reversibility** → inversion, probabilistic thinking, margin of safety
- **Stuck / can't see options** → first principles, second-order thinking, reframing
- **Conflict / negotiation / competition** → incentives, asymmetric warfare, trade-offs
- **Complex system / unintended effects** → feedback loops, emergence, bottlenecks, leverage
- **Performance / optimization** → bottlenecks, diminishing returns, efficiency
- **People / team / behavior** → incentives, social proof, biases
- **Communication / persuasion** → framing, audience, contrast

Full decision trees: **PATTERNS.md**. Per-category deep walkthroughs: **REFERENCE.md**. Worked examples: **examples/**.

## Core Guidelines

1. **Max 3 models per analysis** — quality over quantity
2. **Follow `thinking_steps` verbatim** — don't paraphrase the framework away
3. **Always check `when_to_avoid`** — warn the user if the model misfits
4. **Latticework**: show how chosen models connect and where they disagree
5. **Be actionable**: end with concrete next steps, not theory
6. **Name biases honestly**: if the user seems caught in one, surface it

## Category Map

| Category | IDs | Focus |
|---|---|---|
| General Thinking | m01-m09 | Foundations: inversion, first principles, second-order |
| Science | m10-m29 | Natural laws: leverage, inertia, activation energy |
| Systems Thinking | m30-m40 | Constraints, feedback, emergence, scale |
| Mathematics | m41-m47 | Randomness, regression to mean, sampling |
| Economics | m48-m59 | Scarcity, trade-offs, supply/demand |
| Art | m60-m70 | Framing, audience, contrast |
| Strategy / Warfare | m71-m75 | Asymmetric advantage, seeing the front |
| Human Nature | m76-m98 | Biases, incentives, social proof |

## Files in This Skill

- `SKILL.md` — this entry point (CLI-driven playbook)
- `REFERENCE.md` — deep per-category walkthrough (fallback + teaching)
- `PATTERNS.md` — decision trees for common problem shapes
- `examples/` — 5 worked scenarios
- `models/` — 98 model files (the source of truth the CLI reads)
- `resources/model-index.json` — searchable keyword index
- `resources/quick-reference.md` — problem→model lookup tables

## File Fallback (when CLI is unavailable)

If `mental-models` is not installed and `uvx mental-models` is not available:

1. **Discovery**: read `resources/model-index.json` and grep `resources/quick-reference.md` for keyword matches
2. **Selection**: use the Discovery Heuristics above + **PATTERNS.md** decision trees
3. **Application**: open the model file at `models/Mental_Model_<Category>/m<NN>_<name>.md` and walk the **Thinking Steps** section verbatim
4. **Always check** the **When to Avoid** section before recommending the model

This fallback gives you the same content as the CLI — the CLI just makes selection, lookup, and section extraction faster and more deterministic.
