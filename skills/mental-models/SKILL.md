---
name: mental-models
description: Apply Charlie Munger's latticework of 98 mental models to any problem. Use when user requests decision analysis, says "help me think", "apply mental model", mentions model names (inversion, bottlenecks, second-order thinking), or needs structured thinking frameworks.
---

# Mental Models

Apply 98 cognitive frameworks from multiple disciplines — physics, economics, systems
thinking, math, art, strategy, and human judgment — to analyze problems, make decisions,
and think more clearly.

Everything this skill needs is a file in this directory. No install, no dependencies, no
tooling — you read markdown.

## When to Activate

- User names a specific model ("apply inversion", "use bottlenecks")
- User asks "help me think through X" or "what model fits X"
- User requests decision analysis, trade-off evaluation, or structured reasoning
- User describes a complex/ambiguous problem and wants a framework

## Step 1 — Load the catalog

Read [`CATALOG.md`](./CATALOG.md) (path relative to this file). It lists all 98 bundled
models by slug, name, and keywords, grouped into 8 categories — about 4k tokens, cheap to
load in full.

Then check for the user's own models. The 98 are a starting set, not a fixed list:

| Path | Holds |
|---|---|
| `.mental-models/*.md` (relative to the working directory) | this project's or team's models, committed with the code |
| `~/.claude/mental-models/*.md` | the user's personal models, available everywhere |

Glob both. If neither exists, skip on — that is the normal case and costs nothing. If either
has files, read their headings to learn what is there; they follow the same section format
as the bundled models, so they slot into selection exactly the same way.

**A user model always wins a slug collision with a bundled one.** If someone wrote their own
`inversion.md`, they meant it — use theirs and don't mention the built-in unless they ask.

Treat user models as first-class, not as an appendix. A model a team wrote about their own
domain usually beats a general one at that domain.

## Step 2 — YOU select the models

Read the user's problem and pick **2–4 models from different categories**. Selection is a
reasoning task and you are better at it than any keyword matcher: cross-category coverage is
the entire point of a *latticework* — a single-category pick means blind spots go
unchecked.

**Discovery heuristics** to bias your reading of the catalog:

- **Risk / uncertainty / reversibility** → inversion, probabilistic thinking, margin of safety
- **Stuck / can't see options** → first principles, second-order thinking, framing
- **Conflict / negotiation / competition** → incentives, asymmetric warfare, trade-offs
- **Complex system / unintended effects** → feedback loops, emergence, bottlenecks, leverage
- **Performance / optimization** → bottlenecks, diminishing returns, efficiency
- **People / team / behavior** → incentives, social proof, biases
- **Communication / persuasion** → framing, audience, contrast

Per-category deep walkthroughs: [`REFERENCE.md`](./REFERENCE.md). Worked examples:
[`examples/`](./examples/).

## Step 3 — Retrieve each pick exactly

Read the file directly. Bundled models:

```
models/<Category_Dir>/<mNN>_<slug>.md
```

e.g. `models/Mental_Model_General/m07_inversion.md`. Category directories:
`Mental_Model_{General,Science,SysThinking,Math,Economics,Art,War,HumanNature}`
(see the Category Map below, and `CATALOG.md`'s headings, for the exact mapping).

User models are flat files at the path you found them — `.mental-models/<name>.md` or
`~/.claude/mental-models/<name>.md`. No category directories, no numbering.

## Step 4 — Apply

- Walk each model's **Thinking Steps** against the user's facts — follow them, don't
  paraphrase the framework away
- Read **When to Avoid** *before* concluding, and surface it if it applies — this section
  is what separates a mental model from a slogan
- Ask the **Coaching Questions** to deepen the analysis where useful
- Show where the chosen models agree, and where they disagree

## Step 5 — Report

- Name which models you used and why you picked them
- Where models disagreed, say so explicitly rather than silently picking a winner
- End with 3–5 concrete, actionable next steps
- Name any "when to avoid" conditions that apply to this case

## Core Guidelines

1. **2–4 models per analysis, cross-category** — quality and coverage over quantity
2. **Follow the Thinking Steps verbatim** — don't paraphrase the framework away
3. **Always check When to Avoid** — warn the user if the model misfits
4. **Latticework**: show how chosen models connect and where they disagree
5. **Be actionable**: end with concrete next steps, not theory
6. **Name biases honestly**: if the user seems caught in one, surface it

## Category Map

| Category | Directory | IDs | Focus |
|---|---|---|---|
| General Thinking | `Mental_Model_General` | m01–m09 | Foundations: inversion, first principles, second-order |
| Science | `Mental_Model_Science` | m10–m29 | Natural laws: leverage, inertia, activation energy |
| Systems Thinking | `Mental_Model_SysThinking` | m30–m40 | Constraints, feedback, emergence, scale |
| Mathematics | `Mental_Model_Math` | m41–m47 | Randomness, regression to mean, sampling |
| Economics | `Mental_Model_Economics` | m48–m59 | Scarcity, trade-offs, supply/demand |
| Art | `Mental_Model_Art` | m60–m70 | Framing, audience, contrast |
| Strategy / Warfare | `Mental_Model_War` | m71–m75 | Asymmetric advantage, seeing the front |
| Human Nature | `Mental_Model_HumanNature` | m76–m98 | Biases, incentives, social proof |

## Files in This Skill

- `SKILL.md` — this entry point
- `CATALOG.md` — all 98 models by slug + keywords, grouped by category (**read this first**)
- `REFERENCE.md` — deep per-category walkthrough, signature models, latticework combos
- `examples/` — 5 worked scenarios (architecture review, career decision, debugging,
  negotiation, product launch)
- `models/` — the 98 bundled model files, the one thing every consumer of this skill reads
- `models/_TEMPLATE.md` — the section format; a user model is any file that follows it

Outside this skill, and never overwritten by an update:

- `.mental-models/*.md` — the working directory's own models
- `~/.claude/mental-models/*.md` — the user's personal models

Source: <https://github.com/cyperx84/claude-skills-mental-models>
