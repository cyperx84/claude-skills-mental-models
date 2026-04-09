# Example: Product Launch

## Situation

User: "We're launching a new B2B analytics product in 6 weeks. Early beta users love it, and we want to go big on launch day — PR, paid ads, a big keynote. Leadership wants the biggest possible day-one number."

## Problem shape

Looks like a marketing/execution question, but the real shape is a **complex system with feedback loops** (Tree 4) plus **people/adoption** (Tree 6) plus a hidden **survivorship bias** in the "beta users love it" signal.

## Models picked (3, cross-category)

1. **m41 Sampling / m96 Survivorship Bias** (Math / Human Nature) — because "beta users love it" is a biased sample
2. **m37 Critical Mass** (Systems) — because B2B adoption often has threshold dynamics
3. **m10 Activation Energy** (Science) — because day-one adoption is a starting-cost problem, not a demand problem

## Reasoning walkthrough

**Survivorship Bias — "Who are the beta users actually?"**
Beta users are self-selected enthusiasts. Their love tells you the ceiling, not the floor. The silent signal is: how many prospects churned out of the beta *before* giving feedback? If unknown, the "they love it" data is nearly worthless for projecting a broad launch. This is the first model to surface because it questions the premise leadership is using.

**Critical Mass — "Does this product need a threshold to work?"**
Analytics products often need: (a) enough data ingested to be useful, (b) enough teammates in the workspace to collaborate, (c) enough integrations connected. If any of these are true, a huge day-one burst of signups that don't cross the threshold produces a huge day-one burst of churn 2 weeks later. The big-bang launch may *destroy* long-term numbers by burning the audience before the product is ready to deliver value on first use.

**Activation Energy — "What's the cost of day-one success?"**
The real blocker to adoption usually isn't awareness; it's the friction from signup to first "aha". A launch that drives traffic without lowering activation energy converts a traffic spike into a churn spike. The lever is onboarding friction, not ad spend.

## Conclusion

Three models converging on the same warning: **the launch plan optimizes the wrong variable.** Day-one signups is a vanity metric when the system has threshold dynamics and high activation energy. Worse, the beta signal is biased, so nobody actually knows the conversion rate from cold prospect to activated user.

Recommendation:
1. Measure activation rate and time-to-first-value on the existing beta cohort before committing to the launch shape
2. Redefine the launch metric from "day-one signups" to "day-30 activated accounts"
3. Invest launch budget in *onboarding* and *integration templates* (lowering activation energy) rather than awareness
4. Stage the launch: invite-gated first, open later, so you don't burn the audience if threshold dynamics bite
5. Explicitly warn leadership about the survivorship bias in the beta feedback

Residual uncertainty: whether leadership can be moved off the vanity metric — that's an incentives/politics question (m19), potentially the next conversation.
