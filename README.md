# Mental Models Skill for Claude Code

A Claude Code skill that applies Charlie Munger's "latticework of mental models" to help analyze problems and make better decisions.

## Installation

Copy the skill to your Claude Code skills directory:

```bash
cp -r .claude/skills/mental-models ~/.claude/skills/
```

Or symlink it:

```bash
ln -s $(pwd)/.claude/skills/mental-models ~/.claude/skills/mental-models
```

## Usage

The skill activates when you:
- Say "help me think", "apply mental model", or mention specific models
- Ask for decision analysis or thinking frameworks
- Mention model names like "inversion", "bottlenecks", "second-order thinking"

**Examples:**

```
Apply inversion to this architecture decision

What mental models help with scaling systems?

Help me think through whether to take this job offer
```

## What's Included

**98 mental models** across 8 categories:

| Category | Models | Examples |
|----------|--------|----------|
| General Thinking | m01-m09 | First principles, inversion, second-order thinking |
| Science | m10-m29 | Leverage, inertia, feedback loops |
| Systems Thinking | m30-m40 | Bottlenecks, scale, margin of safety |
| Mathematics | m41-m47 | Randomness, regression to mean |
| Economics | m48-m59 | Trade-offs, scarcity, creative destruction |
| Art | m60-m70 | Framing, audience, contrast |
| Strategy | m71-m75 | Asymmetric warfare, seeing the front |
| Human Nature | m76-m98 | Cognitive biases, incentives, social proof |

## Structure

```
.claude/skills/mental-models/
├── SKILL.md              # Skill definition
├── models/               # 98 mental model files
└── resources/
    ├── model-index.json  # Searchable index
    └── quick-reference.md
```

## License

MIT
