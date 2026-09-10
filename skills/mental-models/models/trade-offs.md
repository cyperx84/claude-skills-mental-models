---
type: mental-model
title: Trade-offs
description: The real cost of a choice is the best thing you gave up to make it, not the money you spent.
tags:
- economics
- decision-making
- prioritisation
status: stable
sources:
- id: opportunity-cost
  resource: https://en.wikipedia.org/wiki/Opportunity_cost
  title: Opportunity cost — the value of the best forgone alternative
- id: sowell
  resource: https://en.wikipedia.org/wiki/Basic_Economics
  title: "Basic Economics — \"there are no solutions, only trade-offs\""
  author: Thomas Sowell
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

The cost of anything is the best alternative you did not take [^opportunity-cost]. That is
not an accounting cost and it never shows up on a budget, which is exactly why it gets
ignored. Sowell's formulation — there are no solutions, only trade-offs — is the operational
version: any proposal presented as strictly better is a proposal whose costs have not been
found yet [^sowell].

The dominant failure is evaluating options against zero rather than against each other. "Is
this project worth doing?" almost always returns yes, because almost everything has positive
value in isolation. The useful question is what it displaces. A team with one quarter has one
quarter, and the cost of the feature is the other feature.

The second failure is the false binary. "Rewrite or patch" usually has an option C that
nobody costed, and the frame itself was a choice.

## When to Avoid

- **When it becomes an excuse for inaction.** Every option has costs, so a sufficiently
  determined trade-off analysis can justify doing nothing forever.
- **When there genuinely is a Pareto improvement.** They are rare but real — fixing an
  obviously broken process can be better on every axis. Insisting a hidden cost must exist
  is dogma.
- **When the alternatives are incommensurable.** Some things do not convert to a common
  unit, and forcing safety, morale and revenue onto one scale hides a value judgement inside
  arithmetic.
- **On decisions too small to analyse.** The analysis has its own opportunity cost, and for
  most choices it exceeds the value of getting it right.

## Thinking Steps

1. **List the real alternatives, including "do nothing."** Doing nothing is a live option
   with its own cost and it is usually left off the list.
2. **For the leading option, name what it displaces.** Not its price — the specific other
   thing that will not happen because of it.
3. **Check whether the choice is actually binary.** Two options presented as exhaustive
   usually are not. What is option C?
4. **Identify the scarce resource.** Money, engineer-months, attention, goodwill. The
   trade-off is always denominated in whichever is genuinely scarce, and it is rarely money.
5. **Ask what you would need to believe to prefer the alternative.** This surfaces the
   assumption the decision actually rests on.
6. **Say the cost out loud when you decide.** A decision recorded with its forgone
   alternative can be evaluated later. One recorded as "we chose X" cannot.

## Coaching Questions

- "What doesn't happen because we do this?"
- "What's the third option we haven't named?"
- "What's actually scarce here — is it really the money?"
- "What would have to be true for the other choice to win?"
- "If this is strictly better than the alternative, what cost haven't we found?"
