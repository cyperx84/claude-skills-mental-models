# Mental Models for Claude Code

[![GitHub stars](https://img.shields.io/github/stars/cyperx84/claude-skills-mental-models?style=flat-square)](https://github.com/cyperx84/claude-skills-mental-models/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](./LICENSE)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-Compatible-8A2BE2?style=flat-square)](https://code.claude.com/docs)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](./.github/CONTRIBUTING.md)

Mental models as files an agent reads — bring your own, or start with the 21 that ship.

> A latticework for better decisions, one prompt away.

## What It Does

Ask for "inversion," "find the bottleneck," or "help me think through X" and Claude picks
2–4 models from different areas, walks their Thinking Steps against your actual problem,
surfaces the conditions under which each one misleads you, and tells you where they disagree.

The models are files. Twenty-one ship with it — each with a `sources` block whose claims
trace to something real — and you can add your own, which take precedence. No dependencies,
no runtime, no build step.

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

**Upgrading from an older clone?** Previous versions told you to symlink
`.claude/skills/mental-models`. That directory is gone. A stale symlink fails silently — the
skill simply stops activating, with no error. Repoint it:

```bash
cd /path/to/your/claude-skills-mental-models   # your existing clone
git pull                                        # skills/ does not exist until you do
rm -f ~/.claude/skills/mental-models            # -f: the old symlink may already be gone
ln -s "$PWD/skills/mental-models" ~/.claude/skills/mental-models
```

`ln -s` never checks that its target exists, so pull first or you will replace one dangling
symlink with another.

Or drop the symlink entirely and install the plugin above.

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

## Bring Your Own Models

The bundled models are a starting set, not a fixed list. Drop a markdown file in either place
and it joins the latticework:

```
.mental-models/<name>.md            this project's or team's models, committed with the code
~/.claude/mental-models/<name>.md   your personal models, available everywhere
```

Copy [`TEMPLATE.md`](./skills/mental-models/TEMPLATE.md) and fill in the sections.
No registration, no config, no rebuild — the skill globs those paths every time it runs, and
a model you wrote wins any name collision with a bundled one.

This is the interesting half. A general model about incidents is fine; *your* model about
how your team handles incidents, sitting in your repo where every agent working there picks
it up, is better. Institutional judgment, version-controlled, applied automatically.

Plugin updates never touch either path.

### It's an OKF bundle

`models/` conforms to Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) —
a directory of markdown files with YAML frontmatter, one `type` per concept, an `index.md` at
the root. That is not a detail: it means any OKF bundle is already a valid drop-in here, and
this bundle is readable by any OKF-aware agent. Obsidian vaults work too — `[[wikilinks]]`
are treated as links.

Nothing to convert. If you have a knowledge bundle, it's already in the right shape.

## Why Munger?

Charlie Munger argued that worldly wisdom comes from building a **latticework of mental
models** drawn from many disciplines—then hanging experience on that lattice. A single
discipline gives you a hammer; a latticework gives you judgment. This skill operationalizes
that idea: instead of one framework, Claude reaches across psychology, physics, economics,
math, and strategy to analyze your problem. Read more in
[Poor Charlie's Almanack](https://www.stripe.press/poor-charlies-almanack) or Farnam Street's
[Mental Models hub](https://fs.blog/mental-models/).

## The Models

Twenty-one, listed in [`models/index.md`](./skills/mental-models/models/index.md):

| Area | Models |
|---|---|
| Thinking tools | first-principles thinking, second-order thinking, inversion |
| Systems | bottlenecks, feedback loops, emergence, leverage, margin of safety |
| Physical | activation energy, inertia |
| Evidence | sampling, randomness, regression to the mean |
| Economics | trade-offs, scarcity, creative destruction |
| People | bias from incentives, social proof, confirmation bias, framing |
| Strategy | asymmetric warfare |

There were 98. They were one generation run that mirrored someone else's list with no
citations, so 2.0 replaced them with a smaller set that carries sources. The count was never
the point — [your own models](#bring-your-own-models) are.

One problem, many lenses — that's the point.

## What's In Here

```
skills/mental-models/
├── SKILL.md      entry point: when to activate, how to select, how to apply
├── TEMPLATE.md   the format — copy this to write your own
└── models/       an OKF bundle: index.md plus one file per model
```

Your own models live outside the skill, at `.mental-models/` or `~/.claude/mental-models/`,
so an update can never overwrite them.

## Contributing

Model additions, fixes, and new examples welcome. See [CONTRIBUTING.md](./.github/CONTRIBUTING.md).

## License

[MIT](./LICENSE)

## References

Sources, citations, and further reading in [REFERENCES.md](./REFERENCES.md).
