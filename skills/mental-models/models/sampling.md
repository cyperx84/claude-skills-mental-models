---
type: mental-model
title: Sampling
description: Small and self-selected samples lie confidently, and the people you can hear from are rarely the ones you need.
tags:
- mathematics
- statistics
- evidence
- research
status: stable
sources:
- id: small-numbers
  resource: https://en.wikipedia.org/wiki/Insensitivity_to_sample_size
  title: Belief in the law of small numbers — treating small samples as representative
  author: Amos Tversky and Daniel Kahneman
- id: survivorship
  resource: https://en.wikipedia.org/wiki/Survivorship_bias
  title: Survivorship bias — analysing only the cases that made it through
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Tversky and Kahneman showed that people treat small samples as though they carry the
properties of the population — the "law of small numbers" — and so read strong conclusions
out of a handful of observations [^small-numbers]. Small samples have high variance, which
means they produce extreme results routinely, which means the striking finding from five
users is the expected output of a process with no signal in it.

The second failure is worse because sample size does not fix it. If the sample is selected by
a process related to what you are measuring, more data makes you more confident and no more
correct. Survivorship bias is the canonical case: studying successful companies tells you
what successful companies do, not what causes success, because the identical behaviours in
the firms that died are not in the dataset [^survivorship].

In practice the sample is almost always self-selected. The customers who answer surveys, the
users who file bugs, the candidates who apply, the people who stayed to give feedback.

## When to Avoid

- **When you must decide now.** Five interviews beat zero. The model says calibrate
  confidence to the sample, not to refuse to act on small ones.
- **On existence proofs.** One counterexample disproves a universal claim. If a single user
  cannot complete signup, that is not a sampling problem.
- **When the population is genuinely small.** With eleven enterprise customers, six is most
  of the population, not a small sample.
- **As a way to dismiss inconvenient data.** "Small sample" is the standard move for
  discarding evidence you do not like, and it is usually applied selectively.

## Thinking Steps

1. **Ask how the sample was selected.** Before size, mechanism: who ended up in this data and
   why. Selection bias is not repaired by more data.
2. **Name who is missing.** The churned customers, the candidates who did not apply, the
   projects that were cancelled. Absence is the information.
3. **Consider the size against the variance.** Noisy measurements need far more observations
   than people expect to say anything.
4. **Ask what result would be surprising.** If almost any outcome would be consistent with
   your theory, the sample cannot test it.
5. **Look for the failures deliberately.** Survivorship is fixed by going and finding the
   dead cases, which is work nobody schedules.
6. **State confidence in proportion.** "Three of five users struggled here, which is a signal
   worth testing" is honest. "Users struggle here" is not.

## Coaching Questions

- "How did these particular people end up in our data?"
- "Who isn't in this sample, and would they answer differently?"
- "How many observations is this, really?"
- "Have we looked at the ones that failed, or only the ones that worked?"
- "What result would have surprised us? If none, what did we learn?"
