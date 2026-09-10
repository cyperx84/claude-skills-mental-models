---
type: mental-model
title: Bottlenecks
description: A system's throughput is set by its single tightest constraint; work spent anywhere else is wasted.
tags:
- systems-thinking
- performance
- optimization
- operations
status: stable
sources:
- id: toc
  resource: https://en.wikipedia.org/wiki/Theory_of_constraints
  title: Theory of Constraints — the five focusing steps
  author: Eliyahu M. Goldratt
- id: goal
  resource: https://en.wikipedia.org/wiki/The_Goal_(novel)
  title: The Goal — a process of ongoing improvement
  author: Eliyahu M. Goldratt
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Every system has exactly one constraint that determines its output at any given time.
Improving anything else changes nothing you can measure. Goldratt formalised this as the
Theory of Constraints and gave it five focusing steps: identify the constraint, exploit it,
subordinate everything else to it, elevate it, then repeat because the constraint will have
moved [^toc]. He argued the case as a novel about a failing factory, which is why the idea
spread past operations research into software, hospitals and sales pipelines [^goal].

The counterintuitive part is *subordinate*. Local efficiency away from the constraint is not
merely useless — it is actively harmful, because it builds inventory in front of the
bottleneck and gives everyone the impression of progress. A team optimising its own throughput
while sitting upstream of the real constraint is producing work that queues.

The step people skip is the last one. Elevate a constraint and it moves somewhere else,
usually somewhere less comfortable. Fix deploy coupling and discover the new limit is
on-call capacity.

## When to Avoid

- **When the system isn't throughput-limited.** If the problem is quality, morale, or
  direction, the constraint frame quietly redefines it as a speed problem and optimises the
  wrong thing.
- **When you can't measure where the constraint is.** The model's whole value is knowing
  which one it is. Applied on a guess, it concentrates all your effort on a single wrong
  place — worse than spreading it.
- **When the constraint is a person.** Technically the model still holds. Socially,
  "you are the bottleneck" is rarely the sentence that fixes it, and the framing damages the
  thing you needed to improve.
- **When the constraint is deliberate.** Code review, safety checks and approvals are
  constraints on purpose. Elevating them removes the control you installed.

## Thinking Steps

1. **Map the flow end to end.** Where does work enter, what does it pass through, where does
   it leave. You cannot find a constraint in a system you haven't drawn.
2. **Find where work piles up.** Queues are the reliable tell. Look for the stage with things
   waiting in front of it and idle capacity behind it.
3. **Exploit before you invest.** Get everything possible out of the existing constraint
   before spending money on more of it. Usually it is idle part of the time for stupid reasons.
4. **Subordinate the rest.** Deliberately slow or re-point non-constraint work so it stops
   feeding the queue. This feels wrong and is correct.
5. **Elevate.** Now add capacity — hire, buy, parallelise.
6. **Find the new one.** It has moved. Naming where you expect it to move next is the
   difference between a fix and a treadmill.

## Coaching Questions

- "If we could instantly double the speed of one step, which one changes the output?"
- "Where is work waiting right now?"
- "What are we optimising that sits upstream of the real constraint?"
- "Is the constraint idle at any point, and why?"
- "When we fix this, where does the constraint move to?"
