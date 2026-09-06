# Mental Models for Claude Code

[![GitHub stars](https://img.shields.io/github/stars/cyperx84/claude-skills-mental-models?style=flat-square)](https://github.com/cyperx84/claude-skills-mental-models/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](./LICENSE)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2?style=flat-square)](https://code.claude.com/docs)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](./.github/CONTRIBUTING.md)

Turn Claude Code into a thinking partner with 98 Munger-style mental models bundled as a single skill.

> A latticework for better decisions, one prompt away.

![mental-models demo](./docs/demo.gif)

## What It Does

98 mental models, each with Thinking Steps, Coaching Questions, and a **When to Avoid**
section. Ask for "inversion," "find the bottleneck," or "help me think through X" and Claude
picks 2–4 models from different disciplines, walks their Thinking Steps against your actual
problem, and tells you where the models disagree.

No dependencies, no runtime, no build step. It is markdown that Claude reads.

## Install

**Claude Code — plugin (recommended):**

```bash
/plugin marketplace add cyperx84/claude-skills-mental-models
/plugin install mental-models@mental-models
```

Or from your shell:

```bash
claude plugin marketplace add cyperx84/claude-skills-mental-models
claude plugin install mental-models@mental-models
```

**Any other harness — clone and symlink.** The skill is one self-contained folder with a
`SKILL.md` at its root, which is the format Codex, Cursor, OpenCode, and other
AgentSkills-convention harnesses read:

```bash
git clone https://github.com/cyperx84/claude-skills-mental-models.git
ln -s "$PWD/claude-skills-mental-models/skills/mental-models" ~/.claude/skills/mental-models
# or ~/.agents/skills/, or whatever your harness scans
```

Nothing else to run. The skill reads its own files.

## Quick Start

Once installed, it activates on its own:

```
Apply inversion to this architecture decision
```

```
What mental models help with scaling systems?
```

```
Help me think through whether to take this job offer
```

## Why Munger?

Charlie Munger argued that worldly wisdom comes from building a **latticework of mental
models** drawn from many disciplines—then hanging experience on that lattice. A single
discipline gives you a hammer; a latticework gives you judgment. This skill operationalizes
that idea: instead of one framework, Claude reaches across psychology, physics, economics,
math, and strategy to analyze your problem. Read more in
[Poor Charlie's Almanack](https://www.stripe.press/poor-charlies-almanack) or Farnam Street's
[Mental Models hub](https://fs.blog/mental-models/).

## The 98 Models

Full catalog with keywords: [`skills/mental-models/CATALOG.md`](./skills/mental-models/CATALOG.md).

| Category | Range | Sample |
|---|---|---|
| General Thinking | m01–m09 | First principles, inversion, second-order thinking |
| Science | m10–m29 | Leverage, inertia, activation energy |
| Systems Thinking | m30–m40 | Bottlenecks, scale, margin of safety |
| Mathematics | m41–m47 | Randomness, regression to the mean |
| Economics | m48–m59 | Trade-offs, scarcity, creative destruction |
| Art | m60–m70 | Framing, audience, contrast |
| Strategy | m71–m75 | Asymmetric warfare, seeing the front |
| Human Nature | m76–m98 | Cognitive biases, incentives, social proof |

![Latticework of 98 mental models](./docs/latticework.svg)

One problem, many lenses—that's the point.

## What's In Here

```
skills/mental-models/
├── SKILL.md      entry point: when to activate, how to select, how to apply
├── CATALOG.md    all 98 by slug + keywords (the agent reads this first)
├── REFERENCE.md  per-category walkthrough, signature models
├── models/       the 98 model files, grouped by category
└── examples/     5 worked scenarios
```

## Contributing

Model additions, fixes, and new examples welcome. See [CONTRIBUTING.md](./.github/CONTRIBUTING.md).

## License

[MIT](./LICENSE)

## References

Sources, citations, and further reading in [REFERENCES.md](./REFERENCES.md).
