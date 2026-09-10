---
type: mental-model
title: Margin of Safety
description: Build for materially worse than your best estimate, because your estimate is an estimate.
tags:
- systems-thinking
- risk
- engineering
- resilience
status: stable
sources:
- id: factor-of-safety
  resource: https://en.wikipedia.org/wiki/Factor_of_safety
  title: Factor of safety — designed capacity beyond expected load
- id: graham
  resource: https://en.wikipedia.org/wiki/Margin_of_safety_(financial)
  title: Margin of safety — buying below intrinsic value to absorb error
  author: Benjamin Graham
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Engineers do not build a bridge to hold the expected load. They build it to hold several
times the expected load, because materials vary, loads exceed forecasts, and the calculation
itself might be wrong [^factor-of-safety]. The margin is not for the risks you modelled — it
is for the ones you did not.

Graham brought the same idea to investing: buy sufficiently below your estimate of intrinsic
value that you can be substantially wrong and still not lose [^graham]. The margin is
insurance against your own analysis.

The two conditions that make it necessary are uncertainty and asymmetry. If being wrong is
cheap and reversible, run close to the edge. If failure is catastrophic or irreversible, the
margin is the whole design. This is why the model is really about which failures you can
survive, not about being conservative in general — and why "we've never hit the limit" is an
argument for keeping the margin, not removing it.

## When to Avoid

- **When margin has a real competitive cost.** Over-provisioning everything is expensive and
  slow. Margins belong where failure is expensive, not everywhere.
- **When it hides a bad estimate.** A large margin over a number nobody trusts is not safety,
  it is a way to avoid doing the analysis.
- **When the failure is cheap and reversible.** For most software changes, fast rollback beats
  a large safety factor.
- **When margins stack invisibly.** Each layer adding its own conservative buffer produces a
  system sized for a load that cannot occur, at a cost nobody can see or defend.

## Thinking Steps

1. **State the expected load and how confident you are.** Both numbers. The confidence sets
   the margin.
2. **Ask what happens at failure.** Degraded, or gone? Recoverable, or permanent? This decides
   whether you need a margin at all.
3. **Size the margin to the consequence, not the probability.** Low-probability catastrophic
   failure still needs a large margin; high-probability trivial failure needs none.
4. **Identify what the margin is protecting against.** Load variance, or model error? Model
   error needs more, because you cannot bound it.
5. **Check for stacked margins.** Add up the buffers across layers and see what total load
   the system is now sized for.
6. **Protect the margin explicitly.** Unused capacity looks like waste and will be
   reallocated by the first person optimising costs unless it is documented as a margin.

## Coaching Questions

- "What happens if we're wrong by a factor of two?"
- "Is this failure recoverable, and how fast?"
- "How confident are we in the estimate the margin sits on top of?"
- "How many layers have each added their own buffer?"
- "Is that spare capacity waste, or is it the margin doing its job?"
