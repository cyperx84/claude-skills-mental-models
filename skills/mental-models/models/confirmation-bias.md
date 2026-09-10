---
type: mental-model
title: Confirmation Bias
description: We search for and weight evidence that supports what we already believe, and the search feels neutral from inside.
tags:
- human-nature
- evidence
- reasoning
- bias
status: stable
sources:
- id: wason
  resource: https://en.wikipedia.org/wiki/Wason_selection_task
  title: The Wason selection task — failure to seek falsifying evidence
  author: Peter Wason
- id: popper
  resource: https://en.wikipedia.org/wiki/Falsifiability
  title: Falsifiability — theories are tested by attempts to refute them
  author: Karl Popper
generated:
  by: claude-opus-5
  at: '2026-09-10T00:00:00Z'
---

Wason gave people a rule and asked which cards they would turn over to test it. Almost
everyone chose cards that could confirm the rule and almost nobody chose the card that could
falsify it — the only one that carried real information [^wason]. The bias is not that we
ignore contrary evidence once we see it. It is that we never go looking, and the search feels
thorough from the inside.

Popper's response was to make refutation the standard: a theory earns confidence by surviving
serious attempts to kill it, not by accumulating supporting instances [^popper]. That is a
procedure, not an attitude, which is what makes it usable. "Be open-minded" is not
actionable. "Name the observation that would prove you wrong, then go look for it" is.

In practice this is the model behind most protracted debugging sessions and most bad
strategy meetings. The team has a theory and spends its time gathering instances consistent
with it, and consistency is cheap — a wrong theory has plenty of confirming instances.

## When to Avoid

- **When you have to act.** Falsification is unbounded; decisions are not. At some point
  you commit on incomplete evidence, and demanding one more disconfirming test becomes
  procrastination in a lab coat.
- **When the belief is well-established.** Not every accepted finding deserves adversarial
  re-litigation. Applied indiscriminately, this becomes the engine of crankery.
- **As a rhetorical weapon.** "You're just confirming your bias" is unanswerable and
  therefore useless in an argument. It is a tool for auditing your own search, not for
  winning.
- **When falsifying evidence is unobtainable.** If no observation could distinguish the
  hypotheses, the honest move is to say the question is undecidable here, not to run a
  theatrical search.

## Thinking Steps

1. **State the belief precisely enough to be wrong.** Vague claims cannot be falsified, which
   is why they survive so long.
2. **Name the observation that would refute it.** Concretely: what would you have to see?
   If nothing would, stop — this is not a factual claim.
3. **Go look for that specific thing.** Not for evidence generally. The bias operates on
   what you search for, so the search is the intervention.
4. **Weight disconfirming evidence at face value.** Notice the impulse to explain it away and
   apply the same scrutiny you would give confirming evidence, which is usually none.
5. **Ask who would disagree and what they know.** Find the strongest version of the opposing
   case, not the weakest.
6. **Set the threshold in advance.** Decide what would change your mind *before* the evidence
   arrives, or the threshold will move to accommodate it.

## Coaching Questions

- "What would we have to see for this to be wrong?"
- "What have we looked for that would contradict this — not just support it?"
- "Who believes the opposite, and what's their best argument?"
- "Are we collecting evidence or collecting agreement?"
- "What would change our minds, and did we decide that before or after looking?"
