---
type: mental-model
title: Inversion
description: Approach a goal backward by asking what would guarantee failure, then avoid those things.
tags:
- general-thinking
- risk
- planning
- decision-making
status: stable
sources:
- id: jacobi
  resource: https://en.wikipedia.org/wiki/Carl_Gustav_Jacob_Jacobi
  title: Carl Gustav Jacob Jacobi — "man muss immer umkehren" (invert, always invert)
  author: Carl Gustav Jacob Jacobi
- id: almanack
  resource: https://www.stripe.press/poor-charlies-almanack
  title: Poor Charlie's Almanack
  author: Charlie Munger
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Inversion approaches a problem backward. Instead of asking "how do I succeed?", you ask
"what would guarantee failure?" — then systematically avoid those things. The phrasing comes
from the mathematician Carl Jacobi, who told students that hard problems yield when you
invert them [^jacobi]. Munger built it into a standing habit and credited Jacobi directly:
his 1986 commencement speech was structured entirely as prescriptions for a *miserable* life,
on the grounds that the route to a good one is easier to see in the negative [^almanack].

It works because failure modes are more concrete than success factors. "Be a great manager"
resists action; "never let a report find out they're being replaced from someone else" is a
rule you can follow on Tuesday. Avoiding stupidity is a smaller, better-defined target than
achieving brilliance, and it is more reliably reached.

## When to Avoid

- **When the path forward is already clear.** Inversion earns its cost on ambiguous,
  high-stakes, or novel problems. On a well-understood task it adds a step that returns nothing.
- **When it curdles into pessimism.** Cataloguing failure is a risk tool, not a strategy. Teams
  that only invert stop taking the asymmetric bets that actually compound, and mistake
  timidity for rigour.
- **When the failure modes are unknowable.** In genuinely novel territory your list of ways to
  fail is a list of ways you *imagine* failing. Inverting an unfamiliar domain produces
  confident, specific, wrong answers.
- **When it becomes a veto.** "Here's how this could fail" is easy to say and hard to answer.
  Used as rhetoric rather than analysis, it kills proposals without ever making a claim that
  can be tested.

## Thinking Steps

1. **State the goal plainly.** One sentence, concrete enough to be wrong. "Launch the new
   pricing by March without losing enterprise accounts."
2. **Invert it.** Ask what would guarantee the opposite. Not "what might go wrong" — what
   would *reliably* produce disaster.
3. **Generate failure modes without filtering.** Incompetence, bad luck, wrong sequencing,
   the thing everyone knows but nobody says. Quantity first; judge later.
4. **Separate what you control from what you don't.** The uncontrollable half becomes
   contingency planning. The controllable half becomes rules.
5. **Convert each into an avoidance rule.** A failure mode is an observation; a rule is
   something you can be held to. "Don't ship pricing changes in the same week as a migration."
6. **Check the rules don't forbid winning.** If following all of them guarantees you never
   lose and never gain, you have inverted into paralysis. Loosen until the upside survives.

## Coaching Questions

- "It's a year from now and this failed badly. What's the story of how that happened?"
- "What would we have to do to guarantee this goes wrong?"
- "Which of those failure modes are we currently doing?"
- "What must we *not* do, no matter what else changes?"
- "If we wanted to lose our biggest customer on purpose, what would we start doing today?"
