# Mental Models Reference

Deep walkthrough of the 8 categories with signature models and when to reach for each. Use this file when the user wants to learn a category, browse what's available, or when you need to pick models beyond the discovery heuristics in SKILL.md.

Model files live at `models/Mental_Model_<Category>/m<NN>_<name>.md`.

---

## 1. General Thinking (m01-m09)

Foundation models — applicable to nearly any problem. Start here when in doubt.

### Signature models

**m03 — First Principles Thinking**
Strip a problem to its irreducible truths and rebuild from scratch. Reach for it when: conventional wisdom feels wrong, analogies keep failing, you're stuck inside someone else's framing, or the domain is new. Avoid when speed matters more than novelty.

**m05 — Second-Order Thinking**
Ask "and then what?" at least twice. Reach for it when: a decision looks obviously good, effects are delayed, or you're optimizing one variable. The first-order winner is often a second-order loser.

**m07 — Inversion**
Instead of "how do I succeed?", ask "how do I guarantee failure?" then avoid those. Reach for it when: the path forward is ambiguous but the failure modes are clear, stakes are high, or you need a quick sanity check on a plan.

Also in this category: m01 map≠territory, m02 circle of competence, m04 thought experiment, m06 probabilistic thinking, m08 Hanlon's razor, m09 Occam's razor.

---

## 2. Science (m10-m29)

Natural laws re-applied to human systems. Reach for these when dynamics feel physical — momentum, energy, ecosystems, thresholds.

### Signature models

**m10 — Activation Energy**
Every change requires an initial kick larger than the steady-state cost. Reach for it when: you're stuck at the start of something, adoption is low, or a team can't get a habit going. The lever is lowering the threshold, not raising motivation.

**m21 — Leverage**
Small input, disproportionate output. Reach for it when: resources are scarce, you need non-linear returns, or you're picking between many efforts. Pair with Bottlenecks to find where leverage lives.

**m20 — Inertia**
Systems (and people) in motion stay in motion; at rest, stay at rest. Reach for it when: explaining resistance to change, or when a small head start would compound.

Also in this category: ecosystems, niches, cooperation, evolution, catalysts, velocity.

---

## 3. Systems Thinking (m30-m40)

For interconnected systems where the whole ≠ sum of parts. Reach for these when behavior is counterintuitive, delayed, or non-linear.

### Signature models

**m32 — Bottlenecks (Theory of Constraints)**
A system's throughput is set by its single slowest step. Reach for it when: optimizing performance, allocating scarce resources, or debugging why more input yields no more output. The rule: optimizing anything but the bottleneck is wasted effort.

**m30 — Feedback Loops**
Reinforcing (snowballs) vs. balancing (thermostats). Reach for it when: behavior is accelerating or oscillating, or when you want a system to self-correct rather than requiring constant intervention.

**m38 — Emergence**
Properties of the whole that no part possesses. Reach for it when: reductionist analysis is failing, or when team/market/codebase behavior surprises you. Warns against assuming you can predict collective behavior from individual pieces.

Also in this category: m33 scale, m34 margin of safety, m37 critical mass, m39 irreducibility, m40 diminishing returns.

---

## 4. Mathematics (m41-m47)

Quantitative reasoning. Reach for these whenever the user is drawing conclusions from data, streaks, extremes, or small samples.

### Signature models

**m42 — Randomness**
Much of what looks like signal is noise. Reach for it when: explaining short-term results, evaluating a "hot hand", or deciding whether a change caused an outcome.

**m43 — Regression to the Mean**
Extreme results tend to be followed by less extreme ones — independent of any intervention. Reach for it when: evaluating the impact of a fix applied after a crisis, or judging someone's performance after an outlier year.

**m41 — Sampling**
Small/biased samples lie confidently. Reach for it when: user cites "we tried it with 3 customers", or when survivorship is a risk.

Also in this category: local vs global maxima, compounding, power laws.

---

## 5. Economics (m48-m59)

Resource allocation under scarcity. Reach for these whenever choices, costs, or markets are involved.

### Signature models

**m51 — Trade-offs**
Every choice has an opportunity cost; "having it all" is usually a framing error. Reach for it when: a plan seems to have no downside, or when the user is struggling to prioritize.

**m48 — Scarcity**
What is limited drives decisions. Reach for it when: identifying the binding constraint on a system (time, attention, capital, talent) — often the bottleneck in disguise.

**m57 — Creative Destruction**
Progress requires tearing down what works. Reach for it when: defending a legacy investment, or evaluating whether to rewrite vs. patch.

Also in this category: m49 supply/demand, m54 efficiency, m56 monopoly/competition.

---

## 6. Art (m60-m70)

Communication, perception, creative framing. Reach for these when the problem is how something is received, not what it is.

### Signature models

**m63 — Framing**
The same fact lands differently depending on reference points. Reach for it when: persuading, negotiating, writing, or when the user is stuck because they're locked into one framing.

**m60 — Audience**
Meaning is co-created with the receiver. Reach for it when: a message isn't landing, or when the user is writing/designing/pitching for themselves instead of the reader.

**m62 — Contrast**
Nothing has value in isolation — meaning comes from comparison. Reach for it when: a feature/offer/argument feels flat, or pricing/positioning seems off.

---

## 7. Strategy & Warfare (m71-m75)

Adversarial and competitive thinking. Reach for these when there is a thinking opponent.

### Signature models

**m72 — Asymmetric Warfare**
Don't fight on the incumbent's terms. Reach for it when: the user is a small player facing a large one, or resources are mismatched. Find the dimension where your constraints are advantages.

**m71 — Seeing the Front**
Ground truth beats reports. Reach for it when: a leader is deciding from dashboards, or debugging from logs instead of running the system.

**m73 — Two-Front War**
Fighting on multiple fronts loses all of them. Reach for it when: the user is trying to do too many strategic things at once.

---

## 8. Human Nature & Judgment (m76-m98)

Biases, incentives, and predictable irrationality. The largest category — reach for these whenever people are involved.

### Signature models

**m19 / m79 — Incentives**
"Show me the incentive and I'll show you the outcome" (Munger). Reach for it when: explaining surprising behavior, designing systems, or debugging a team problem. Usually the first model to try in any people question.

**m84 — Social Proof**
People look sideways before deciding. Reach for it when: explaining adoption curves, crowd behavior, or resistance to a correct-but-unpopular choice.

**m98 — Confirmation / Falsification Bias**
We seek evidence that confirms us, not evidence that breaks us. Reach for it when: the user is very sure, or when debugging. The fix: "what would have to be true for me to be wrong?"

Also critical: m82 availability heuristic, m88 first-conclusion bias, m91 commitment/consistency, m96 survivorship bias.

---

## Picking Across Categories (Latticework)

Good analyses pull from 2-3 different categories so blind spots in one are covered by another. Classic combinations:

- **Decision Triad**: m02 circle of competence + m05 second-order + m07 inversion
- **System Optimizer**: m32 bottlenecks + m30 feedback loops + m34 margin of safety
- **Bias Detector**: m82 availability + m96 survivorship + m98 confirmation
- **Strategic Planner**: m51 trade-offs + m33 scale + m57 creative destruction

For problem-shape → model selection, see the discovery heuristics in **SKILL.md**.
