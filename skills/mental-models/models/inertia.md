---
type: mental-model
title: Inertia
description: Things keep doing what they were doing; change requires a force, and mass determines how much.
tags:
- science
- change
- organisations
status: stable
sources:
- id: newton
  resource: https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion
  title: Newton's first law — a body remains at rest or in uniform motion unless acted upon
  author: Isaac Newton
- id: inertia
  resource: https://en.wikipedia.org/wiki/Inertia
  title: Inertia — resistance to change in state of motion, proportional to mass
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

A body at rest stays at rest, and a body in motion continues in a straight line, unless acted
on by a force [^newton]. Resistance to that change is proportional to mass [^inertia]. Both
halves matter for the transferred version, and the second one is the half people forget.

At rest: organisations, habits and codebases persist by default. Nothing continues because it
was chosen; it continues because stopping requires a decision and nobody made one. Quarterly
reports, standing meetings, that service nobody owns.

In motion: a project with momentum keeps going in its original direction after the reasons
have expired. This is the more expensive failure, because motion looks like progress. Teams
ship the roadmap written for a market that changed.

And mass sets the cost. A ten-person company turns; a thousand-person company does not turn
at the same price. Underestimating organisational mass is the standard error behind change
programmes that were correct and still failed.

## When to Avoid

- **When stability is the point.** Inertia is what makes systems predictable. Reliability,
  trust and institutional memory are all inertia working correctly.
- **When it becomes fatalism.** "Too much inertia" is a real constraint and also a
  comfortable excuse for not attempting the change.
- **In genuinely fast-moving systems.** Some environments have very little mass and change
  direction on a signal. Assuming inertia there makes you slow.
- **When the persistent thing is persisting for a live reason.** Before concluding a practice
  survives on momentum, check whether it is solving something you have not noticed.

## Thinking Steps

1. **Ask whether this is continuing by decision or by default.** When was it last actively
   chosen? "Nobody remembers" is your answer.
2. **Determine rest or motion.** Are you starting something stationary or redirecting
   something moving? They need different forces and different arguments.
3. **Estimate the mass.** How many people, systems, contracts and habits are attached? Mass
   is what makes the estimate wrong, and it is almost always larger than the plan assumes.
4. **Work out the force required, honestly.** Then ask whether you have it. An underpowered
   change attempt is worse than none — it burns credibility and teaches people that change
   fails here.
5. **Prefer redirecting to stopping.** Changing the direction of something already moving is
   usually cheaper than halting it and starting again.
6. **Remove the force sustaining the old motion.** Often something is actively maintaining
   the current state. Stopping that beats pushing against it.

## Coaching Questions

- "When did we last actually decide to do this?"
- "Is this at rest or already moving, and in what direction?"
- "How much mass is attached to this — people, systems, promises?"
- "Do we have enough force to actually move it, or will we stall halfway?"
- "What's actively keeping this going that we could just stop?"
