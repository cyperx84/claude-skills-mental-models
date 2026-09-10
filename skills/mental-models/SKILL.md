---
name: mental-models
description: Apply Charlie Munger's latticework of 98 mental models to any problem. Use when user requests decision analysis, says "help me think", "apply mental model", mentions model names (inversion, bottlenecks, second-order thinking), or needs structured thinking frameworks.
---

# Mental Models

Apply cognitive frameworks from several disciplines — systems, economics, psychology,
mathematics, strategy — to analyse problems, make decisions, and think more clearly.

Everything this skill needs is a file. No install, no dependencies, no tooling — you read
markdown.

## When to Activate

- User names a specific model ("apply inversion", "use bottlenecks")
- User asks "help me think through X" or "what model fits X"
- User requests decision analysis, trade-off evaluation, or structured reasoning
- User describes a complex/ambiguous problem and wants a framework

## Step 1 — Load the index

Read [`models/index.md`](./models/index.md). It lists every bundled model with a one-line
description. It is short; load it in full.

Then check for the user's own models. The bundled set is a starting point, not a fixed list:

| Path | Holds |
|---|---|
| `.mental-models/` (relative to the working directory) | this project's or team's models, committed with the code |
| `~/.claude/mental-models/` | the user's personal models, available everywhere |

Glob both for `*.md`. If neither exists, skip on — that is the normal case and costs nothing.
If either has files, read each one's YAML frontmatter (`title`, `description`, `tags`) to
learn what is there. A directory may have its own `index.md`; read that instead if present.

**A user model always wins a name collision with a bundled one.** If someone wrote their own
`inversion.md`, they meant it — use theirs, and don't mention the built-in unless asked.

Treat user models as first-class. A model a team wrote about their own domain usually beats
a general one at that domain.

## Step 2 — YOU select the models

Read the user's problem and pick **2–4 models from different areas**. Selection is a
reasoning task and you are better at it than any keyword matcher: cross-area coverage is the
entire point of a *latticework* — a single-area pick means blind spots go unchecked.

**Discovery heuristics** to bias your reading of the index:

- **Risk / uncertainty / reversibility** → inversion, margin of safety, randomness
- **Stuck / can't see options** → first-principles thinking, second-order thinking, framing
- **Conflict / negotiation / competition** → bias from incentives, asymmetric warfare, trade-offs
- **Complex system / unintended effects** → feedback loops, emergence, bottlenecks, leverage
- **Performance / optimization** → bottlenecks, leverage, activation energy
- **People / team / behaviour** → bias from incentives, social proof, confirmation bias
- **Evaluating evidence or results** → sampling, regression to the mean, randomness
- **Change that won't start, or won't stop** → activation energy, inertia

## Step 3 — Retrieve each pick

Read the file directly. Bundled models are flat files named by slug:

```
models/<slug>.md
```

e.g. `models/inversion.md`. The index gives you the exact filename — use it rather than
guessing. User models are at the path you found them.

## Step 4 — Apply

Each model file has YAML frontmatter and four parts:

- the **description prose** — what the idea is and where it comes from, with `[^footnotes]`
  pointing at entries in the frontmatter's `sources`
- **When to Avoid** — read this *before* concluding, and surface it if it applies. It is what
  separates a mental model from a slogan.
- **Thinking Steps** — walk these against the user's actual facts. Follow them; don't
  paraphrase the framework away.
- **Coaching Questions** — ask these to deepen the analysis where useful.

Show where the chosen models agree, and where they disagree.

## Step 5 — Report

- Name which models you used and why you picked them
- Where models disagreed, say so explicitly rather than silently picking a winner
- End with 3–5 concrete, actionable next steps
- Name any "when to avoid" conditions that apply to this case
- If a source matters to the point you are making, cite it — the `sources` block has the link

## Core Guidelines

1. **2–4 models per analysis, from different areas** — coverage over quantity
2. **Follow the Thinking Steps verbatim** — don't paraphrase the framework away
3. **Always check When to Avoid** — warn the user if the model misfits
4. **Latticework**: show how chosen models connect and where they disagree
5. **Be actionable**: end with concrete next steps, not theory
6. **Name biases honestly**: if the user seems caught in one, surface it

## The format

`models/` is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle: a directory of markdown files, each with YAML frontmatter carrying at minimum a
`type`. That means any OKF bundle can be dropped into `.mental-models/` and read the same way,
and this bundle can be consumed by any OKF-aware agent.

Obsidian vaults work too — treat `[[wikilink]]` as a link to `wikilink.md`.

To write your own, copy [`TEMPLATE.md`](./TEMPLATE.md).

## Files in This Skill

- `SKILL.md` — this entry point
- `TEMPLATE.md` — the format; copy it to write your own model
- `models/` — the bundled OKF bundle: `index.md` plus one file per model

Outside this skill, and never overwritten by an update:

- `.mental-models/*.md` — the working directory's own models
- `~/.claude/mental-models/*.md` — the user's personal models

Source: <https://github.com/cyperx84/claude-skills-mental-models>
