---
type: mental-model
title: Social Proof
description: We infer correct behaviour from what others do, most strongly exactly when we are least certain.
tags:
- human-nature
- influence
- groups
- bias
status: stable
sources:
- id: cialdini
  resource: https://en.wikipedia.org/wiki/Influence:_The_Psychology_of_Persuasion
  title: Influence — social proof as a principle of persuasion
  author: Robert Cialdini
- id: asch
  resource: https://en.wikipedia.org/wiki/Asch_conformity_experiments
  title: The Asch conformity experiments
  author: Solomon Asch
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

When we are unsure what to do, we look at what others are doing and treat it as evidence
[^cialdini]. Asch showed how far this goes: subjects gave obviously wrong answers about line
lengths after hearing confederates give them, and a meaningful fraction did so repeatedly
[^asch]. The line lengths were not ambiguous. The social signal simply outweighed the eyes.

Two conditions amplify it: uncertainty, and similarity. The less confident you are, the more
weight others' behaviour carries — which is precisely backwards, because uncertain situations
are where independent evidence matters most. And the more the others resemble you, the
stronger the pull, which is why an industry converges on practices nobody has tested.

The trap in technology decisions is that adoption is presented as evidence of quality when it
is usually evidence of adoption. Everybody moved to microservices partly because everybody
was moving to microservices, and the companies that quietly moved back rarely write the
conference talk.

## When to Avoid

- **When the crowd has real information you lack.** Following experienced people in an
  unfamiliar domain is usually correct. The model warns against *unexamined* deference, not
  all deference.
- **When contrarianism becomes the reflex.** Being reliably against consensus is as
  thoughtless as being reliably for it, and it feels like independent thinking.
- **On genuine conventions.** Which side of the road to drive on has no independently correct
  answer. Coordination problems are solved by doing what others do.
- **When there is no time.** Under time pressure with no way to evaluate, copying the crowd is
  a reasonable heuristic. Say that out loud rather than pretending it was analysis.

## Thinking Steps

1. **Notice the uncertainty.** Ask whether you would hold this view if nobody else did. The
   pull is strongest where you are least sure, so uncertainty is the cue to check.
2. **Ask what evidence the crowd actually has.** Did they evaluate, or did they also copy?
   Trace one or two steps back and you often find nobody tested anything.
3. **Look for the silent evidence.** Who tried this and stopped? Those cases rarely publish,
   and their absence is what makes the practice look more successful than it is.
4. **Find the dissenter.** Someone who examined it and disagreed is worth more than a hundred
   who agreed by default.
5. **Separate popularity from fit.** Widely adopted is a claim about the average case, not
   about your constraints.
6. **State what would change your mind.** If nothing would, you are holding a social position,
   not an analytical one.

## Coaching Questions

- "If no other company had done this, would we still?"
- "Who here actually evaluated it, versus heard it was standard?"
- "Who tried this and went back? Have we looked?"
- "Who on this team disagrees, and have we asked them properly?"
- "Are we choosing this because it fits us or because it's what's done?"
