---
type: mental-model
title: Emergence
description: Aggregates have properties their parts don't, so understanding the components does not give you the whole.
tags:
- systems-thinking
- complexity
- scale
status: stable
sources:
- id: more-is-different
  resource: https://doi.org/10.1126/science.177.4047.393
  title: More Is Different — broken symmetry and the nature of the hierarchy of science
  author: P. W. Anderson
- id: emergence
  resource: https://en.wikipedia.org/wiki/Emergence
  title: Emergence — properties an entity has that its parts do not
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Emergent properties belong to a collection and not to any of its members [^emergence]. A
water molecule is not wet. A neuron does not think. A single trader has no opinion about
market sentiment. Anderson's argument was that this defeats pure reductionism: knowing the
laws governing the parts does not let you derive the behaviour of the assembly, because new
laws appear at each level of scale [^more-is-different].

The practical consequence is that expertise in components does not transfer to the system.
Excellent engineers produce incoherent architectures. Every individual on a team acting
reasonably produces a culture nobody would have chosen. Each hiring decision is defensible
and the org is unrecognisable in two years.

It also means you cannot fix emergent problems at the component level. Adding a rule for
each bad outcome treats the symptom of a structure that will keep generating new ones.
Emergent behaviour is changed by changing interaction patterns — who talks to whom, what
gets rewarded, what is easy versus hard — not by improving parts in isolation.

## When to Avoid

- **When the problem really is one broken component.** Emergence is the fashionable
  explanation; sometimes one service is misconfigured. Check the simple cause first.
- **As an excuse for unpredictability.** "It's emergent" can mean "we have not looked hard
  enough." Many surprising system behaviours have a boring traceable cause.
- **When it removes agency.** If the conclusion is that nobody is responsible because the
  outcome emerged, the model is being used to launder a decision someone made.
- **On small systems.** Three components interacting are usually just three components. The
  concept earns its keep at scale, where the interactions outnumber the parts.

## Thinking Steps

1. **Name the property that's bothering you.** Be specific: "releases are slow", "the culture
   is defensive". Then ask which single component has that property. Usually none do.
2. **If no part has it, look at the interactions.** The behaviour lives in the connections —
   handoffs, dependencies, incentives, meeting structure.
3. **Map who affects whom.** Not the org chart; the actual paths by which one part's output
   becomes another's input.
4. **Identify the rules generating the pattern.** Simple local rules produce complex global
   behaviour. Find the local rule everyone is rationally following.
5. **Intervene on the rule, not the instance.** Change what is easy, what is rewarded, or who
   is connected to whom.
6. **Expect a new emergent property.** Changing interaction structure produces a different
   whole, not a fixed one. Look for what appears next.

## Coaching Questions

- "Which individual part has this property? If none, why do we keep fixing parts?"
- "What simple rule is everyone following that produces this?"
- "Who talks to whom here, actually?"
- "If every person is behaving reasonably and the outcome is bad, what does that tell us?"
- "What new behaviour appears if we change this structure?"
