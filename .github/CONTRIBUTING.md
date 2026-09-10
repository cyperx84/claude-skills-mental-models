# Contributing

This repo is markdown only. No build step, no test suite, no code. Edit files, open a PR.

## Layout

```
skills/mental-models/
├── SKILL.md      entry point — when to activate, how to select, how to apply
├── TEMPLATE.md   the format; copy it to write a model
└── models/       an Open Knowledge Format bundle
    ├── index.md  the catalog (OKF reserved name)
    └── <slug>.md one file per model
```

Files are flat and named by slug: `models/inversion.md`. There are no category directories
and no numbering — both existed once and were the source of two retrieval bugs. Category
lives in frontmatter `tags`.

## Adding or changing a model

1. Copy [`TEMPLATE.md`](../skills/mental-models/TEMPLATE.md) to `models/<slug>.md`.
2. Fill in the frontmatter. `type` is the only field OKF requires, but **`sources` is the one
   that matters here** — a model whose claims trace somewhere is worth more than three that
   don't. Cite inline with `[^id]` matching a `sources[].id`.
3. Write the four parts: description prose, `## When to Avoid`, `## Thinking Steps`,
   `## Coaching Questions`.
4. Add a line to [`models/index.md`](../skills/mental-models/models/index.md). A model missing
   from the index is invisible to the agent.

**When to Avoid is the section that earns the model's place.** Anyone can restate a
framework; the value is knowing when it misleads you. Be specific about conditions, not
generic about caveats.

Bad: "Don't apply it rigidly."
Good: "Not for chronic degradation — there's no expanding radius, so it manufactures urgency
and burns the team on something that needed a project, not a page."

## Bar for a new model

- It has at least one real, resolvable source. Not "as popularised by" — something a reader
  can go and check.
- It is not a rephrasing of a model already in the set.
- Its *When to Avoid* names conditions you could actually hit.

The set is deliberately small. A model that only just clears the bar makes the set worse, not
bigger.

## Style

- Plain, concrete prose. No hype.
- Thinking Steps are actions the reader takes, not descriptions of the concept.
- Coaching Questions are things a person would say out loud.

## Checking your work

OKF conformance is three rules: every non-reserved `.md` has parseable YAML frontmatter,
every frontmatter has a non-empty `type`, and reserved names (`index.md`, `log.md`) follow
their structures — only the root `index.md` carries frontmatter, with `okf_version`. See the
[OKF spec](https://github.com/GoogleCloudPlatform/open-knowledge-format).

- Manifests must stay valid JSON:
  `python3 -c "import json;json.load(open('.claude-plugin/plugin.json'))"`
- Every `[^id]` in a body must match a `sources[].id`.
- Source links must resolve. Check them; a dead citation is worse than none.
- Try it locally: `claude plugin marketplace add .` then
  `claude plugin install mental-models@mental-models`. A version bump alone does **not**
  refresh the plugin cache — `marketplace remove`, `add`, reinstall.
- `claude plugin details mental-models` shows the component inventory and token cost.
