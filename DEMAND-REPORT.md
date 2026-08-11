# DEMAND-REPORT — why this repo gets starred, and what's actually broken

Companion to [`SCAN-REPORT.md`](./SCAN-REPORT.md) (architecture/complexity audit, 2026-07-30).
That one answers *what the code is*. This one answers *who uses it, why, and what to lean into*.
Scan date: 2026-08-11. Every number below pulled live from the GitHub and PyPI APIs.

---

## 1. The actual numbers

| Metric | Value |
|---|---|
| Stars | **14** |
| Forks | 2 |
| Watchers | 0 |
| Issues opened by outsiders | **0** (all 6 open issues self-filed 2026-04/07) |
| PRs from outsiders | 0 |
| Views (14 days) | 59 views / 30 uniques |
| Referrers (14 days) | **Google 31 / 12 uniques**, github.com 5 / 2 |
| Created | 2025-10-30 |
| Last push | 2026-05-19 (~3 months idle) |

Confirmed most-starred repo on the account — next is `ski-instructor-booking-platform` at 3.
So "most stars" is true, and it's 14. State it flat.

**Star arrival — no spike, pure trickle:**

```
2025-12-10  brunolelles
2026-03-02  13Kart
2026-03-21  armstrongl
2026-03-23  tylerseymour
2026-03-29  lamaniaditya275-spec
2026-04-02  musiskr
2026-04-10  cyperx84          (self)
2026-05-02  machinarii
2026-05-26  chrispian
2026-06-09  skinnyluv
2026-06-27  Beastars-awsl
2026-06-29  ourzeta
2026-07-28  chileanman
2026-08-11  LinhLe223         (today)
```

~1–2/month, unbroken, still arriving with zero promotion and three months of no commits.
**That is the signal.** Not the count — the *shape*. There is standing search demand for
"mental models Claude Code skill," this repo ranks for it, and nothing has ever been done
to amplify it (issue #9, submit to awesome-lists, still open and never actioned).

## 2. What they actually come for

Top traffic paths, 14 days:

| Path | Views |
|---|---|
| Overview (README) | 29 |
| `/tree/main/skills` | 5 |
| `.claude/skills/mental-models/SKILL.md` | 5 |
| README.md | 2 |
| `docs/latticework.mmd` + `.svg` | 4 combined |
| `skills/mental-models/SKILL.md` | 2 |

Everyone who goes past the README goes to **a SKILL.md or the skills tree**. Nobody
visits `packages/`. Nobody visits the MCP configs. The demand is:

1. **The 98-model corpus** — hand-written, template-consistent, 5 sections each
   (Description / Keywords / Thinking Steps / Coaching Questions / When to Avoid).
   The `When to Avoid` section in particular is rare in mental-model collections and is
   real IP — most catalogs are a list of names and a paragraph.
2. **Packaged as a drop-in skill** — one symlink and Claude Code gains a thinking mode.
   Zero-install, zero-config, works immediately.
3. **The latticework visual** — the SVG/mermaid graph gets disproportionate views for a
   generated artifact. It's the thing that makes the idea legible in five seconds.

That's the whole product. Everything else in the repo is unexercised.

## 3. The distribution path is fiction — and this is the headline finding

**`mental-models` on PyPI is not this project.** It belongs to Kwame Porter Robinson,
uploaded January 2020, an unrelated NLP package ("Extracts human mental models from text…
See J Diesner 2003"). Versions 0.1.0–0.1.5, homepage `github.com/robinsonkwame/mental_models`.

Consequences, all verified:

- `pip install mental-models` **silently installs a stranger's 2020 package.** Its wheel has
  no `entry_points.txt`, so no `mental-models` command appears. The user gets a successful
  install and a missing binary.
- `uvx mental-models select "..."` — the README's *headline* "fastest on-ramp, no install" —
  cannot work. No console script to execute.
- `pip install mental-models-mcp` — **404, the package does not exist on PyPI at all.**
- The `publish` workflow **failed** on the v0.2.0 release (2026-04-09). Trusted Publishing
  can't claim a name you don't own. Nothing from this repo has ever reached PyPI.
- The 148 downloads/month on `mental-models` are Kwame's. **Do not cite them as demand.**

So of the five advertised surfaces, exactly one has ever been installable: the Claude Code
skill via clone + symlink. The CLI, the MCP server, the Python library, and the portable
skill's CLI-first workflow all route through a package that doesn't exist.

The skill still *works* only by luck: SKILL.md's preflight (`mental-models doctor` →
`uvx mental-models doctor` → File Fallback) degrades into the file-fallback path, which
reads `models/` directly. The fallback the SCAN-REPORT flagged as redundant is, in fact,
the only thing keeping the skill functional.

**Every star this repo has was earned by the file fallback.**

## 4. Corrections to prior in-repo analysis

Things currently written down in this repo that are wrong and would misdirect the rewrite:

- **`docs/research/landscape.md`** (unmerged, `origin/claude/refine-local-plan-gKFRe`)
  recommends renaming the repo to `cyperx84/mental-models` and states: *"PyPI: no action
  required — the package is already `mental-models`."* False. The package is someone else's.
  The single "concrete reason worth renaming for" in that doc evaporates. Do not merge as-is.
- **README + RELEASING.md** both claim PyPI availability for `mental-models` and
  `mental-models-mcp`. Neither is true.
- **`evals.yml` fails on every single run** since 2026-04-09 — 6 consecutive failures.
  Dead CI signal, not a passing gate. `validate.yml` is genuinely green.
- **Unmerged work exists on two branches** and is invisible from main:
  `claude/implement-awesome-plan-4dz07` (compare/random commands, shared `utils.py`, drops
  `compile_index.py` — −1187 lines) and `claude/refine-local-plan-gKFRe` (landscape +
  roadmap docs, rename prep). Both branch from `53e14dd` and predate the merged
  optimization PR #10 — they will need rebasing, and per the standing rule, diff the trees
  before assuming either is stale.

## 5. Names — checked, not guessed

GitHub `cyperx84/{mental-models, latticework, munger-models}` all free (404).

PyPI availability (all confirmed 404 = free): `munger-models`, `latticework`,
`mental-models-kit`, `mungerkit`, `latticework-cli`, `mental-latticework`,
`munger-latticework`, `mmodels`.

`mental-models` is permanently unavailable on PyPI. Whatever the repo is called, the
package name has to change, and the README's install lines have to change with it.

## 6. What the rewrite should lean into

Ordered by what the evidence supports, not by what's most fun to build.

1. **Content is the asset. Grow and sharpen the corpus.** 98 models, hand-written, with
   `When to Avoid` — that's the moat. Issue #8 (gap audit vs. the 129-model list) is the
   highest-value open issue in the repo. Depth per model beats breadth of surfaces.
2. **Skill-first distribution, done properly.** The only working path today is a manual
   symlink. Current standard is a `.claude-plugin/plugin.json` marketplace plugin — one
   `/plugin marketplace add` instead of clone+ln. This is the single biggest reduction in
   friction available, and it targets exactly the surface people already visit.
3. **Make the skill work standalone by design, not by accident.** The file-fallback path
   is load-bearing. Promote it to the primary path; a CLI, if it ships, is an accelerant,
   not a dependency. This also matches the standing doctrine — the calling harness is
   already an LLM; the skill's job is content plus a playbook.
4. **Fix or delete the broken install surfaces before the rewrite ships.** Pick a free
   package name, republish, and correct README/RELEASING — or cut the CLI/MCP claims
   entirely until they're real. Shipping a rewrite on top of four fictional install paths
   repeats the current failure at larger scale.
5. **Bank the free distribution.** Issue #9 — submit to `VoltAgent/awesome-agent-skills`
   and `ComposioHQ/awesome-claude-skills`. Zero code, and discovery is currently 100%
   unassisted organic search. This is the cheapest multiplier on the table.
6. **Keep the latticework visual and invest in it.** Disproportionate view counts for a
   generated SVG. It is the repo's one piece of visual identity.

The SCAN-REPORT's refactor plan (single content store, one package, one canonical skill)
is still sound — but its priority order changes. Distribution and naming now come *before*
the plumbing dedup, because the plumbing dedup optimizes surfaces that currently have
zero possible users.

---

_Scope note: this is scan + assessment. It stops short of the rewrite plan itself._
