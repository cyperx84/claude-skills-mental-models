---
type: mental-model
title: Regression to the Mean
description: Extreme results are followed by less extreme ones for statistical reasons, independent of anything you did.
tags:
- mathematics
- statistics
- performance
- evaluation
status: stable
sources:
- id: galton
  resource: https://en.wikipedia.org/wiki/Regression_toward_the_mean
  title: Regression toward the mean — Galton's 1886 study of hereditary stature
  author: Francis Galton
- id: kahneman
  resource: https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow
  title: Thinking, Fast and Slow — regression and the illusion of training effects
  author: Daniel Kahneman
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

When a measurement combines skill and luck, an extreme result usually had extreme luck in it,
and luck does not repeat. So the next measurement lands closer to average — not because
anything changed, but because that is what the arithmetic does. Galton named it while studying
heights: tall parents have tall children who are on average shorter than the parents [^galton].

Kahneman's flight-instructor example is the one that matters for managers. Instructors
observed that praising a good landing was followed by a worse one, and criticising a bad
landing was followed by a better one, and concluded that criticism works and praise
backfires. The pattern is pure regression — exceptional landings are followed by ordinary
ones either way — but it taught a generation of instructors to punish [^kahneman]. This is the
model's real bite: regression manufactures evidence for whatever you happened to do after an
extreme event.

Anything selected *because* it was extreme will regress. Best-performing team, worst-performing
region, the quarter that broke records, the candidate who aced the interview.

## When to Avoid

- **When the process genuinely changed.** Regression assumes a stable underlying distribution.
  If you shipped a real fix, the improvement may be causal. The model is a null hypothesis to
  rule out, not a verdict.
- **When there is no luck component.** Deterministic measurements do not regress. A slow
  query that is slow because of a missing index will stay slow forever.
- **In systems with real momentum.** Reinforcing loops can make extremes persist or intensify.
  Bank runs and viral growth do not regress toward the mean on the relevant timescale.
- **As blanket cynicism.** Explaining every improvement as regression is as unscientific as
  explaining every one as skill. It is a specific claim requiring a specific baseline.

## Thinking Steps

1. **Ask if the case was selected for being extreme.** If you are looking at it *because* it
   was the best or worst, regression is guaranteed to be part of what happens next.
2. **Estimate the luck component.** How much of this measurement is noise? High variance
   means strong regression.
3. **Establish the baseline.** What is the long-run average for this thing? Without it you
   cannot tell regression from change.
4. **Predict the regression explicitly.** Before intervening, write down what you expect
   next with no intervention at all.
5. **Compare the outcome against that prediction, not against the extreme.** This is the step
   that separates a real effect from an artifact.
6. **Watch for the causal story.** If you praised or punished in between, your mind will
   supply a mechanism. Notice it and set it aside.

## Coaching Questions

- "Are we looking at this because it was exceptional?"
- "What would have happened next if we'd done nothing?"
- "How much of this number is noise?"
- "What's the long-run average, and how far from it was this?"
- "Did the process change, or just the result?"
