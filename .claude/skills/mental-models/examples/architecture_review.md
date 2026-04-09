# Example: Architecture Review

## Situation

User: "We're designing a new service to handle 10x our current write load. The team wants to use a new event-sourced design with a message bus. I need to sanity-check this before we commit two quarters to it."

## Problem shape

A high-stakes, low-reversibility technical decision on a complex system that must scale. Matches **Tree 4 (complex system)** and **Tree 5 (performance)** — plus a risk dimension from **Tree 1**.

## Models picked (3, cross-category)

1. **m32 Bottlenecks** (Systems) — because the user said "10x write load" without saying where
2. **m33 Scale** (Systems) — because 10x means non-linear effects kick in
3. **m07 Inversion** (General) — classic architecture sanity check: how does this design fail?

## Reasoning walkthrough

**Bottlenecks — "What is the actual constraint at 10x?"**
Ask the user: is the current bottleneck CPU, disk I/O, network, lock contention, or downstream fan-out? Event sourcing moves work around but doesn't create throughput. If the current constraint is disk write throughput, an event bus may just relocate the problem to the broker. If the constraint is lock contention, event sourcing may genuinely help. Without identifying the constraint, the redesign is speculative.

**Scale — "What breaks non-linearly at 10x?"**
- Event stream replay time (linear in events, so 10x data = 10x cold-start)
- Debugging cognitive load (non-linear — distributed traces at 10x volume are disproportionately painful)
- Operational surface area (new component = new failure mode, new on-call burden)
- Consistency guarantees that held at current load may be violated at 10x concurrency

Scale suggests a warning: event sourcing has a famously steep operational tax that is paid constantly, not just at peak.

**Inversion — "How would this architecture guarantee failure?"**
- Ship it without a replay strategy; discover at month 6 that replays take 14 hours
- Adopt event sourcing for a domain where the aggregate boundaries aren't clear yet
- Add a message bus without idempotency in consumers
- Underestimate the learning curve for engineers not familiar with the pattern
- Commit two quarters before validating the bottleneck assumption on a prototype

## Conclusion

The models agree the design *might* be right, but the decision is premature. The failure mode isn't "event sourcing is bad" — it's "we don't yet know it's the right answer to the right question."

Recommendation to give the user:
1. Measure first — identify the actual bottleneck at current load before picking an architecture
2. Build a one-week spike of just the write path with the new design under synthetic 10x load
3. Inversion checklist: replay time, aggregate boundaries, consumer idempotency, on-call cost
4. Reserve event sourcing for domains where audit/replay is a feature, not a tax

Residual uncertainty: the team's familiarity with event sourcing is a gating factor none of these models measure directly — worth asking.
