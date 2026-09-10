---
type: mental-model
title: Feedback Loops
description: Output that re-enters as input — reinforcing loops accelerate, balancing loops resist, and delay makes both unstable.
tags:
- systems-thinking
- dynamics
- unintended-consequences
status: stable
sources:
- id: meadows
  resource: https://en.wikipedia.org/wiki/Donella_Meadows
  title: Thinking in Systems — stocks, flows, and feedback
  author: Donella Meadows
- id: cybernetics
  resource: https://en.wikipedia.org/wiki/Cybernetics
  title: Cybernetics — control and communication in the animal and the machine
  author: Norbert Wiener
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

A feedback loop exists when a system's output comes back around as its input. Wiener's
cybernetics established the idea as a general one, applying equally to machines, organisms
and organisations [^cybernetics]. Meadows made it practical: systems are stocks connected by
flows, and the flows are governed by loops that either reinforce or balance [^meadows].

Reinforcing loops compound — more users make the product better which attracts more users.
They also compound downward, which is the same loop running in reverse and is why decline
is rarely gradual. Balancing loops seek a target and resist change; they are why so many
well-designed interventions produce nothing at all. The system was holding a level, you
pushed, and it pushed back.

Delay is what turns both into instability. A balancing loop with a long lag overshoots,
corrects, overshoots again. Most organisational thrash — hiring freezes followed by frantic
hiring, alert fatigue followed by alert deletion followed by missed outages — is a delayed
balancing loop oscillating, not a series of bad decisions.

## When to Avoid

- **On genuinely linear, one-shot situations.** If the output does not return as input,
  drawing loops is invented complexity.
- **When you cannot observe the loop.** A hypothesised feedback structure is unfalsifiable
  and endlessly elaborable. Without a measurement, it explains everything and predicts nothing.
- **When it excuses accountability.** "It's a systems problem" is sometimes true and
  sometimes a way of ensuring nobody has to change what they do on Monday.
- **When the timescale exceeds your horizon.** A loop that closes over five years is real but
  useless for a decision you make this quarter — you will never observe the correction.

## Thinking Steps

1. **Name the stock.** What accumulates? Users, trust, debt, unresolved tickets. Loops act on
   stocks, so find the stock first.
2. **Trace the flows in and out.** What raises it, what drains it, and what governs each rate.
3. **Ask whether output feeds back into input.** If more of the stock causes more inflow, it
   reinforces. If more causes more outflow or less inflow, it balances.
4. **Find the delay.** How long between the change and the response arriving? Long delays
   plus strong correction equals oscillation, every time.
5. **Locate the leverage.** Loop strength usually lives in one parameter or one rule. Changing
   the rule beats pushing harder against the loop.
6. **Check for a loop you're fighting.** If effort produces no change, you are probably
   pushing on a balancing loop that is doing its job.

## Coaching Questions

- "What accumulates here, and what fills and drains it?"
- "Does more of this cause more of it, or less?"
- "How long between a change and us seeing the result?"
- "What is holding this at its current level despite our pushing?"
- "If this loop ran backwards, how fast would it unwind?"
