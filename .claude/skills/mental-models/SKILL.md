---
name: mental-models
description: Apply Charlie Munger's latticework of mental models to any problem. Use when user requests decision analysis, says "help me think", "apply mental model", mentions model names (inversion, bottlenecks, second-order thinking), or needs structured thinking frameworks.
---

# Mental Models

Apply 98 cognitive frameworks from multiple disciplines to analyze problems, make decisions, and think more clearly. This skill uses progressive disclosure: start here, then load deeper files only as needed.

## When to Activate

Activate when the user:
- Names a specific model ("apply inversion", "use bottlenecks")
- Asks "help me think through X" or "what model fits X"
- Requests decision analysis, trade-off evaluation, or structured reasoning
- Describes a complex/ambiguous problem and wants a framework

## Category Map (8 categories, 98 models)

| Category | IDs | Focus |
|---|---|---|
| General Thinking | m01-m09 | Foundations: inversion, first principles, second-order |
| Science | m10-m29 | Natural laws: leverage, inertia, activation energy |
| Systems Thinking | m30-m40 | Constraints, feedback, emergence, scale |
| Mathematics | m41-m47 | Randomness, regression to mean, sampling |
| Economics | m48-m59 | Scarcity, trade-offs, supply/demand |
| Art | m60-m70 | Framing, audience, contrast |
| Strategy/Warfare | m71-m75 | Asymmetric advantage, seeing the front |
| Human Nature | m76-m98 | Biases, incentives, social proof |

For deep per-category walkthroughs with signature models and when to use each, load **REFERENCE.md**.

## Workflows

### 1. Quick Apply (user names a model)

User: "Apply inversion to this architecture decision"

1. Locate the model file under `models/Mental_Model_<Category>/m<NN>_<name>.md`
2. Read: Description, Thinking Steps, When to Avoid
3. Walk the Thinking Steps against the user's context
4. Deliver 3-5 concrete insights
5. Flag any "When to Avoid" conditions that apply

### 2. Discovery (user asks "what models for X")

User: "What mental models help with scaling?"

1. Search `resources/model-index.json` for keyword matches
2. Cross-reference `resources/quick-reference.md` for known problem→model mappings
3. If the situation matches a common pattern, load **PATTERNS.md** for a decision tree
4. Return top 3-5 candidates with one-line rationales
5. Offer to deep-dive on any candidate

### 3. Deep Analysis (complex decision)

User: "Help me think through whether to accept this job offer"

1. Ask 2-3 clarifying questions (stakes, constraints, reversibility)
2. Consult **PATTERNS.md** if the problem shape matches (risk, stuck, conflict, complex system)
3. Select **max 3** models — prefer cross-category coverage (latticework)
4. For each: apply Thinking Steps verbatim to the user's facts
5. Synthesize: where do the models agree? disagree? what does the union suggest?
6. Give actionable recommendations + residual uncertainties

For full worked walkthroughs see `examples/` (career_decision, architecture_review, product_launch, debugging_hard_bug, negotiation).

## Discovery Heuristics (how to pick models)

Match the problem's **shape** to a category first, then pick 2-3 models across categories:

- **Risk / uncertainty / reversibility** → General (inversion, probabilistic) + Systems (margin of safety)
- **Stuck / can't see options** → General (first principles, second-order) + Art (reframing)
- **Conflict / negotiation / competition** → Human Nature (incentives) + Strategy (asymmetric) + Economics (trade-offs)
- **Complex system / unintended effects** → Systems (feedback loops, emergence, bottlenecks, leverage points)
- **Performance / optimization** → Systems (bottlenecks) + Economics (diminishing returns, efficiency)
- **People / team / behavior** → Human Nature (incentives, social proof, biases)
- **Communication / persuasion** → Art (framing, audience, contrast)

Decision trees for each pattern live in **PATTERNS.md**.

## Model File Structure

Every file in `models/` contains:
- **Description** — core concept
- **When to Avoid** — limits and failure modes (always check)
- **Keywords** — application contexts
- **Thinking Steps** — the sequential framework (follow exactly; this is where the value is)
- **Coaching Questions** — prompts for deeper exploration

## Core Guidelines

1. **Max 3 models per analysis** — quality over quantity
2. **Follow Thinking Steps verbatim** — don't paraphrase the framework away
3. **Always check "When to Avoid"** — warn the user if the model misfits
4. **Latticework**: show how chosen models connect and where they disagree
5. **Be actionable**: end with concrete next steps, not theory
6. **Name biases honestly**: if the user seems caught in one (survivorship, confirmation), surface it

## Files in This Skill

- `SKILL.md` — this entry point
- `REFERENCE.md` — deep per-category walkthrough (load for discovery / teaching)
- `PATTERNS.md` — decision trees for common problem shapes (load for model selection)
- `examples/` — 5 worked scenarios (load when user wants an example or a close analog)
- `models/` — 98 model files organized by category
- `resources/model-index.json` — searchable keyword index of all models
- `resources/quick-reference.md` — problem→model lookup tables and power combinations
