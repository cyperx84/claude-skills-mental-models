---
type: mental-model
title: Randomness
description: Much of what looks like signal is noise, and we build causal stories over both without noticing.
tags:
- mathematics
- probability
- evidence
- luck
status: stable
sources:
- id: taleb
  resource: https://en.wikipedia.org/wiki/Fooled_by_Randomness
  title: Fooled by Randomness — the hidden role of chance
  author: Nassim Nicholas Taleb
- id: clustering
  resource: https://en.wikipedia.org/wiki/Clustering_illusion
  title: The clustering illusion — seeing patterns in random distributions
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Random processes produce streaks, clusters and apparent patterns as a matter of course, and
we are reliably bad at recognising them as random [^clustering]. Genuinely random sequences
look less random to us than evenly spaced ones — which is why a shuffled playlist gets
complaints about repeats.

Taleb's argument extends this to outcomes generally: in any domain with a large luck
component, success is heavily sampled from lucky people, and their explanations of their
success are constructed after the fact [^taleb]. The explanation feels compelling to
everyone involved, including the person giving it, because we are unable to experience a
sequence of events without generating a cause.

The practical form is that process and outcome are different things. A good decision can
produce a bad result and a terrible decision can pay off, and if you evaluate decisions by
their outcomes in a high-variance domain, you will systematically learn the wrong lessons.

## When to Avoid

- **In low-variance domains.** Where outcomes are mostly determined by skill and process,
  attributing results to chance is an excuse. Most engineering is not a casino.
- **When it becomes unfalsifiable.** "That was luck" applied to every result you dislike is
  not analysis. It has to be a claim about the variance of a specific process.
- **When there is a discoverable cause.** Reaching for randomness before investigating is
  how root causes stay unfound. Intermittent bugs are not random, they are conditional.
- **When it removes responsibility.** Real luck exists and so does negligence, and the model
  is very comfortable to hide behind.

## Thinking Steps

1. **Estimate the luck component.** How much of the outcome in this domain is determined by
   factors nobody controls? This sets how much to discount the result.
2. **Separate the decision from the outcome.** Judge the decision on what was knowable at the
   time. Write it down before the result arrives, or you cannot do this honestly.
3. **Ask what the distribution would produce anyway.** Would a purely random process generate
   this streak at this rate? Often the answer is yes.
4. **Look for the unsuccessful cases.** Survivors are visible and failures are not, so success
   stories are sampled from the lucky tail by construction.
5. **Increase sample size before concluding.** One quarter, three customers and two incidents
   are not evidence about a process.
6. **Ask what result would have changed the lesson.** If a different outcome would have
   produced the opposite conclusion from the same decision, you are learning from noise.

## Coaching Questions

- "Was this a good decision, or just a good outcome?"
- "How much of this domain is luck?"
- "Would a random process have produced this pattern anyway?"
- "Who made the same call and it didn't work — have we looked for them?"
- "How many observations is this conclusion resting on?"
