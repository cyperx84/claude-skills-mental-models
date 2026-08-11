# REBUILD-PLAN

Companion to [`DEMAND-REPORT.md`](./DEMAND-REPORT.md) (why it's starred, what's broken) and
[`SCAN-REPORT.md`](./SCAN-REPORT.md) (architecture/complexity audit).
Decisions locked 2026-08-11.

## Governing finding

Content + skill is the product. The CLI, MCP server, and Python library have never had a
possible user — nothing from this repo has ever reached PyPI. Every star was earned by the
file-fallback path that reads the 98 model files directly. Rebuild around that.

## Locked decisions

| Decision | Value | Note |
|---|---|---|
| Repo slug | **`cyperx84/mental-models`** | Chris's call, risk accepted (see below) |
| PyPI package | **`mental-models-kit`** | verified free; `mental-models` permanently taken |
| MCP server | **deferred** | never shipped, nobody noticed; build when asked |
| Selector | **kept, dependency inverted** | files+index primary, CLI accelerant |

**Accepted risk on the repo rename:** discovery is 100% unassisted Google, and the current
slug contains the exact ranking terms ("claude", "skills", "mental models"). GitHub redirects
HTTP; Google re-ranks from scratch. Mitigation: keep those terms in the repo description,
topics, and README H1, and make the Phase 3 site the real ranking asset — 98 indexable pages
beats one slug.

## Current → target

```
NOW                                          verdict
.claude/skills/mental-models/  98 md + skill  ONLY working path (via file fallback)
skills/mental-models/          portable copy  broken — CLI-first, no CLI exists
packages/mental_models/        CLI + lib      never published
packages/mental_models_mcp/    MCP            never published, 404

TARGET
repo root = one uv project
  skills/mental-models/SKILL.md      canonical skill, standalone by design
  .claude-plugin/plugin.json         /plugin marketplace add  (kills symlink friction)
  src/mental_models/data/models/*.md 98 md = only content store
  src/mental_models/{index,selector,cli}.py  thin CLI — accelerant, not spine
  site/                              98 indexable pages + llms.txt
```

---

## Phase 0 — stop the bleeding (hours, mandatory) — **DONE 2026-08-11, uncommitted**

1. ~~README/RELEASING/docs instruct users to install a stranger's package~~ — fixed.
   README install section rewritten with a status note; `⚠️ Not published` banner prepended to
   `RELEASING.md`, `skills/README.md`, `docs/mcp/README.md`, `docs/openclaw/README.md`,
   `packages/mental_models/README.md`, `packages/mental_models_mcp/README.md`.
2. ~~Both SKILL.md preflights told the agent to `uvx mental-models`~~ — fixed. Both now route
   straight to the File Fallback and explicitly warn against the PyPI name. The portable
   skill's "Install the CLI" section was replaced with a File Fallback section (it previously
   had none — it was CLI-only and therefore fully broken).
3. ~~`evals.yml` failing on every push~~ — deleted (`git rm`, recoverable).
   Root cause: `if: ${{ secrets.ANTHROPIC_API_KEY != '' }}` at **job** level — the `secrets`
   context is unavailable there, so the workflow failed at parse time on every commit
   regardless of its `workflow_dispatch`-only trigger. Also unrunnable in principle: the
   account is OAuth/subscription-only, no API key exists to supply.
   Verified after: `validate_models.py` 98/0 errors, selector evals 30/30.

**Remaining in Phase 0:** branch triage. Two unmerged branches both fork from `53e14dd` and
predate merged PR #10 — they will conflict. **Re-derive, don't rebase.** Diff trees before
discarding anything. Named salvage:
- `claude/refine-local-plan-gKFRe` — the competitive-landscape research in
  `docs/research/landscape.md`, **minus its false claim** that the PyPI package is already
  published (that claim was the sole stated reason for the rename; it is untrue).
  Also `docs/research/roadmap.md`.
- `claude/implement-awesome-plan-4dz07` — the `compare`/`random` commands, the shared
  `utils.py` extraction, and the `compile_index.py` deletion approach (−1187 lines).

## Phase 1 — distribution (days, mandatory)

- **FIRST, before anything else: reserve `mental-models-kit` on PyPI** with a 0.0.x
  placeholder. The chosen name is now written into seven public-facing files while
  unregistered — this repo's entire crisis is a name collision; do not invite a second one.
- Rename repo to `cyperx84/mental-models`; keep search terms in description + topics.
- Rename package to `mental-models-kit`; publish for real; **verify `uvx mental-models-kit`
  end-to-end before any README claims it.** No unverified claim ships again.
- `.claude-plugin/plugin.json` — one `/plugin marketplace add` replaces clone+symlink.
  Biggest friction cut available, aimed at the surface people already visit.
- SKILL.md standalone by design: file path primary, CLI optional accelerant.
- Invert the selector dependency (don't delete it). Selection is reasoning; the harness does
  reasoning. The CLI's deterministic value is retrieval + formatting. Selector stays in the
  package for CLI/library callers, 30 eval cases intact.
- Migration stub at the old `.claude/skills/` path — 14 stargazers is the entire user base.
- Collapse: one content store (md as package data; delete the 258 KB embedded-prose JSON and
  its compile/sync/drift machinery), one package, one skill.
- Run **skilleval** on the new SKILL.md description before shipping — a skill triggering on
  "help me think" is exactly the contention case it measures.

## Phase 2 — content moat (open-ended, independently shippable)

The 98 hand-written models with **When to Avoid** are the actual IP; most catalogs are a name
and a paragraph. Gap audit vs the 129-list (issue #8), per-model citations, sharpen
`When to Avoid` hardest since it is the differentiator.

## Phase 3 — discovery (targets the one working channel)

Today **one page** ranks. A Pages/Cloudflare catalog site = **98 indexable entry points**,
plus `llms.txt` and agent-ready-web treatment, plus the latticework graph as visual identity.
Carry `REFERENCES.md` attribution onto the site — publishing 98 write-ups publicly raises the
provenance bar. Then awesome-list submissions (issue #9): zero code, free multiplier, and
currently the cheapest lever on the table.

## Phase 4 — differentiator

Decision-record output (a thinking session currently evaporates into chat scrollback);
`walk <slug>` stepwise thinking-steps iterator.

## Permanent cuts

`select_models_with_claude` (violates the CLI-never-calls-an-LLM doctrine), the LLM-judge eval
harness, the `quick-reference.md` / `PATTERNS.md` overlap, double content storage.
