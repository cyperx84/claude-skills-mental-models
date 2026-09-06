# Contributing

Thanks for helping grow the Mental Models skill. This repo is markdown only — there is no
build step, no test suite, and no code to run. Edit files, open a PR.

## Repository layout

```
skills/mental-models/
├── SKILL.md      entry point
├── CATALOG.md    index of all 98 models
├── REFERENCE.md  per-category walkthrough
├── models/<Category_Folder>/mNN_snake_case_title.md
└── examples/
```

Category folders:

| Folder | Category | IDs |
|---|---|---|
| `Mental_Model_General` | General Thinking Tools | m01–m09 |
| `Mental_Model_Science` | Physics, Chemistry, and Biology | m10–m29 |
| `Mental_Model_SysThinking` | Systems Thinking | m30–m40 |
| `Mental_Model_Math` | Mathematics | m41–m47 |
| `Mental_Model_Economics` | Economics | m48–m59 |
| `Mental_Model_Art` | Art | m60–m70 |
| `Mental_Model_War` | Strategy (military/competition) | m71–m75 |
| `Mental_Model_HumanNature` | Human Nature and Judgment | m76–m98 |

## Adding or editing a model

1. Copy [`skills/mental-models/models/_TEMPLATE.md`](../skills/mental-models/models/_TEMPLATE.md)
   into the right category folder. Name it `mNN_snake_case_title.md`, continuing the numbering.
2. Fill in every section: **Description**, **When to Avoid (or Use with Caution)**,
   **Keywords for Situations**, **Thinking Steps**, **Coaching Questions**.
3. Add a matching line to [`CATALOG.md`](../skills/mental-models/CATALOG.md) under the right
   heading, in the existing `` `slug` — Name: keywords `` format. The catalog is what the
   agent reads to choose models, so a model missing from it is invisible.
4. If the model belongs in a category's signature set, mention it in
   [`REFERENCE.md`](../skills/mental-models/REFERENCE.md).

**When to Avoid** is the section that matters most. Anyone can restate a framework; the
value here is knowing when it misleads you. Be specific about the conditions, not generic
about the caveats.

## Style

- Plain, concrete prose. No hype.
- Thinking Steps are actions the reader takes, not descriptions of the concept.
- Coaching Questions are things a person would actually say out loud.
- Cite a source when a model comes from a specific book, paper, or speech.

## Checking your work

- The plugin manifests must stay valid JSON:
  `python3 -c "import json;json.load(open('.claude-plugin/plugin.json'))"`
- To try the skill locally before opening a PR:
  `claude plugin marketplace add .` then `claude plugin install mental-models@mental-models`
- `claude plugin details mental-models` shows the component inventory and token cost.
