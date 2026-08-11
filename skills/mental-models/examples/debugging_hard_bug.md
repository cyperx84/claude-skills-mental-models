# Example: Debugging a Hard Bug

## Situation

User: "We have a bug that only happens in production, only for about 0.3% of requests, only on Tuesdays. We've been chasing it for two weeks. The team is convinced it's a race condition in the payment service. I'm not sure."

## Problem shape

The user is stuck (**Tree 2**) on a complex system (**Tree 4**) and is also suspicious their team is anchored. That's a classic bias-check situation — so **Human Nature** gets a seat at the table.

## Models picked (3, cross-category)

1. **m01 Map ≠ Territory** (General) — because the team has a mental model of the system that may not match reality
2. **m98 Confirmation Bias** (Human Nature) — because two weeks of chasing one hypothesis is exactly when this bias calcifies
3. **m71 Seeing the Front** (Strategy) — because "convinced it's a race condition" usually means nobody's looked at the actual failing request end-to-end

## Reasoning walkthrough

**Map ≠ Territory — "What does the team believe that might not be true?"**
Enumerate the assumptions baked into "race condition in payment service":
- That the failure is in *our* code (vs. a dependency, infra, data)
- That "Tuesdays" is a real pattern vs. a sampling artifact
- That 0.3% is uniform across customers vs. concentrated in a subset
- That the payment service is where the symptom originates vs. where it surfaces

Any one of these, if wrong, invalidates the hypothesis. The map has at least four un-verified claims.

**Confirmation Bias — "What would have to be true for the race-condition theory to be wrong?"**
This is the inversion of the debugging question. Force the team to write down:
- What evidence, if found, would disprove the race-condition hypothesis?
- What evidence have they been *not* looking at because it's "irrelevant" to the race theory?
Two weeks of evidence that fits the theory is also two weeks of disconfirming evidence filtered out.

**Seeing the Front — "Has anyone traced one actual failing request end-to-end?"**
Reports, dashboards, and aggregated metrics lie by omission. The fix: pull one real failing transaction ID from logs, walk it through every hop, every service, every DB call. If no one on the team can produce that walkthrough, they're debugging the map, not the territory.

## Conclusion

The three models collectively say: **stop chasing the hypothesis, start questioning it.** The team's problem isn't lack of effort; it's two weeks of confirmation bias hardening around an unverified map.

Recommendation:
1. Before any more code changes, produce a full end-to-end trace of one real failing request (seeing the front)
2. Write down and verify the four assumptions explicitly (map≠territory)
3. Run a "falsify the theory" session: list evidence that would disprove the race condition and go look for it (anti-confirmation)
4. Check the "Tuesdays" pattern with proper statistical tests — is it real or is it sampling? (m42 randomness as a backup model)
5. Expand the search outside the payment service for 48 hours even if it feels wrong

Residual uncertainty: the bug might still be a race condition — but the team won't know that until they've *earned* the belief by trying to kill it.
