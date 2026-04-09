# Mental Models Selection Patterns

Decision trees for picking the right 2-3 models based on the **shape** of the user's problem. Load this file during discovery or deep analysis workflows.

Each tree ends with a recommended latticework (models from different categories) and a note on when to substitute.

---

## Tree 1 — Risk, Uncertainty, Reversibility

**Trigger phrases**: "should I risk", "what could go wrong", "is this safe", "how likely", "worst case"

```
Is the decision reversible?
├── YES, cheaply → m06 Probabilistic Thinking (just estimate odds and go)
│                   Avoid analysis paralysis.
│
└── NO / expensive to reverse
    │
    Are the failure modes knowable?
    ├── YES → m07 Inversion (enumerate ways to fail, then avoid)
    │          + m34 Margin of Safety (engineer buffer against known failures)
    │
    └── NO, mostly unknown unknowns
        → m32 Bottlenecks (what one thing, if it breaks, stops everything?)
          + m06 Probabilistic Thinking (distribution, not point estimate)
          + m34 Margin of Safety (bigger buffer when uncertainty is higher)
```

**Default latticework**: Inversion + Probabilistic Thinking + Margin of Safety.

---

## Tree 2 — Stuck / Blocked / Can't See Options

**Trigger phrases**: "I'm stuck", "can't figure out", "no good options", "analysis paralysis"

```
Is the user stuck on HOW, or on WHAT to do?
│
├── HOW (they know the goal, can't find a path)
│   │
│   Is the conventional approach failing?
│   ├── YES → m03 First Principles (rebuild from fundamentals)
│   │          + m04 Thought Experiment (relax a constraint; what becomes possible?)
│   │
│   └── NO, they just haven't thought it through
│       → m05 Second-Order Thinking (walk the chain forward 2-3 steps)
│
└── WHAT (they don't know what they want / options all look bad)
    → m63 Framing (the options look bad because of the frame — try 3 frames)
      + m07 Inversion (what are they trying to avoid? reverse it)
      + m51 Trade-offs (name what each option costs — often reveals the real priority)
```

**Default latticework**: First Principles + Second-Order Thinking + Framing.

---

## Tree 3 — Conflict, Negotiation, Competition

**Trigger phrases**: "disagree", "negotiate", "competitor", "opponent", "win", "team conflict"

```
Is there a thinking adversary, or aligned parties with different views?
│
├── ADVERSARIAL (competitor, negotiation counterparty)
│   │
│   Are you the stronger or weaker party?
│   ├── Weaker → m72 Asymmetric Warfare (don't fight on their terms)
│   │             + m19 Incentives (what do they actually want?)
│   │
│   └── Stronger/peer → m19 Incentives (align or exploit)
│                        + m51 Trade-offs (what can you give that costs you little?)
│                        + m63 Framing (shape what "winning" means)
│
└── ALIGNED but stuck (team conflict, family decision)
    → m19 Incentives (is someone's incentive misaligned with the stated goal?)
      + m84 Social Proof (is the disagreement actually about what others think?)
      + m01 Map ≠ Territory (everyone has a different model of the same facts)
```

**Default latticework**: Incentives + Framing + Trade-offs (or Asymmetric Warfare if weaker).

---

## Tree 4 — Complex System with Unintended Effects

**Trigger phrases**: "keeps happening", "fix one thing and another breaks", "system", "unintended", "cascade"

```
What is the symptom?
│
├── Throughput is capped despite adding resources
│   → m32 Bottlenecks (find the single constraint)
│     + m40 Diminishing Returns (you're past the knee of the curve elsewhere)
│
├── Behavior is accelerating or oscillating
│   → m30 Feedback Loops (identify reinforcing vs. balancing)
│     + m37 Critical Mass (is there a threshold being crossed?)
│
├── The whole behaves nothing like the parts
│   → m38 Emergence (stop looking at parts; look at interactions)
│     + m39 Irreducibility (some systems can't be understood piecewise)
│
└── Interventions keep backfiring
    → m05 Second-Order Thinking (first-order fix causes second-order harm)
      + m21 Leverage (you may be pushing the wrong place; find the leverage point)
      + m19 Incentives (the system is rewarding the broken behavior)
```

**Default latticework**: Bottlenecks + Feedback Loops + Second-Order Thinking.

---

## Tree 5 — Performance / Optimization

**Trigger phrases**: "slow", "optimize", "faster", "more efficient", "why isn't this scaling"

```
Are you optimizing the right thing?
│
├── Not sure → m32 Bottlenecks first (measure, don't guess)
│              + m71 Seeing the Front (look at actual production, not dashboards)
│
└── Yes, you know the target
    │
    Are returns flattening?
    ├── YES → m40 Diminishing Returns (stop; move effort elsewhere)
    │          + m51 Trade-offs (what are you giving up by pushing further?)
    │
    └── NO → m33 Scale (will this approach survive 10x?)
              + m34 Margin of Safety (don't optimize away all slack)
```

**Default latticework**: Bottlenecks + Diminishing Returns + Scale.

---

## Tree 6 — People / Behavior / Why-Did-They-Do-That

**Trigger phrases**: "why did they", "team isn't", "motivate", "adoption", "resistance"

```
Is the behavior surprising or predictable-but-unwanted?
│
├── SURPRISING (doesn't match what they said they'd do)
│   → m19 Incentives (the stated goal ≠ the rewarded behavior)
│     + m08 Hanlon's Razor (assume oversight before malice)
│     + m98 Confirmation Bias (are YOU seeing what you expected?)
│
└── PREDICTABLE (they won't change, adopt, start, stop)
    │
    Is this about starting or stopping?
    ├── Starting → m10 Activation Energy (lower the threshold, don't raise motivation)
    │               + m84 Social Proof (who else is doing it?)
    │
    └── Stopping / changing → m20 Inertia (momentum is the real opponent)
                                + m91 Commitment & Consistency (sunk cost)
                                + m19 Incentives (what's still rewarding the old behavior?)
```

**Default latticework**: Incentives + Activation Energy + Social Proof.

---

## Meta-Rule: When Trees Disagree

If two trees apply (e.g. a risky decision that is also a conflict), pick **one model from each tree** rather than doubling up inside one. The latticework principle: coverage across categories beats depth in one.

If no tree fits cleanly, fall back to the **Decision Triad**: m02 Circle of Competence + m05 Second-Order Thinking + m07 Inversion. It applies to almost anything.
