# Landscape

Comparable projects, and the distribution levers that are still open. Salvaged from research
done for the 0.2.0 release (2026-04-10) and trimmed: everything about the CLI, the MCP
server, the selector and the repo rename is gone, because those are gone.

## Content analogues

| Project | What it is | What's worth taking |
|---|---|---|
| [ModelThinkers](https://modelthinkers.com/mental-model/mungers-latticework) | Web app, ~200 models, user-built latticeworks, spaced repetition | The user-built-latticework idea landed here as drop-in `.mental-models/` files. Spaced repetition is a different product; not ours. |
| [WiseCharlie/mental-models](https://github.com/WiseCharlie/mental-models) | Static content collection | Cross-check the bundled set for gaps; compare phrasings where ours are thin. |
| [AdrienLemaire/awesome-mental-models](https://github.com/AdrienLemaire/awesome-mental-models) | Awesome-list of heuristics and tools-for-thought | Mine for models we're missing. |
| [sourcesofinsight — 129 list](https://sourcesofinsight.com/charlie-munger-mental-models/) | Curated 129-model list | We ship 21, chosen for having real primary sources. Gap-audit target for anything that clears that bar. |
| [mahavak.github.io/models](https://mahavak.github.io/models/) | Static site rendering Munger's framework | Proof that a Pages site is a thin wrap over content we already have. |

## Structural analogues

| Project | Pattern |
|---|---|
| [modelcontextprotocol/servers — sequentialthinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | Stepwise thought protocol — `thought`, `revision`, `branch`, `hypothesis` nodes. Our Thinking Steps are the same shape, walked by the agent instead of a server. |
| [ckelsoe/claude-skill-prompt-architect](https://github.com/ckelsoe/claude-skill-prompt-architect) | Intent-router picks a framework from the user's phrasing. Our SKILL.md discovery heuristics do this in prose. |
| [glebis/claude-skills](https://github.com/glebis/claude-skills) | Common skill-repo conventions; sanity-check ours against it. |

## Open levers

**BundleDex** (https://bundledex.net) is a registry of 700+ OKF bundles with a submission
form. As of September 2026 none of the listed bundles are about reasoning, decision-making,
or thinking frameworks — they are overwhelmingly memory and knowledge-persistence tools.
Since `models/` is now a conformant OKF bundle, that shelf is open and directly reachable.


Ordered by cost. None of these need code.

1. **Awesome-list submissions** — [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills),
   [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills).
   Upstream PRs, zero local change, free distribution. Cheapest thing on the list.
2. **A catalog site.** Today one page ranks. One page per model plus `llms.txt` is a page
   per entry point. Note the provenance bar rises when the write-ups are published as pages rather
   than shipped as skill files — see the attribution note in [`REFERENCES.md`](../REFERENCES.md).
3. **Gap audit vs the 129-list.** Content work, not distribution, and only worth it for
   models that clear the sourcing bar the 21 set.

## Deferred, with reasons

- **`model-of-the-day` / spaced repetition** — retention feature with no usage data behind it.
- **Domain presets** (`mental-models-code`, `-product`) — premature. Drop-in user models
  cover the same need without a fork per domain.
