# Contributing

Thanks for helping grow the Mental Models skill. This guide covers how to add a new model, how to keep the index in sync, and how to validate your work before opening a PR.

## Repository layout

Models live under:

```
.claude/skills/mental-models/models/<Category_Folder>/mNN_snake_case_title.md
```

Category folders currently in use:

- `Mental_Model_General`      - General Thinking Tools
- `Mental_Model_Science`      - Science
- `Mental_Model_SysThinking`  - Systems Thinking
- `Mental_Model_Math`         - Mathematics
- `Mental_Model_Economics`    - Economics
- `Mental_Model_Art`          - Art
- `Mental_Model_War`          - Strategy (military/competition)
- `Mental_Model_HumanNature`  - Human Nature and Judgment

## Naming convention

- File name: `mNN_snake_case_title.md`
  - `NN` is the next available two-digit number (zero-padded, e.g. `m99`).
  - Title is lowercase, snake_case, words separated by underscores.
  - Example: `m42_regression_to_the_mean.md`
- If your title contains an apostrophe, keep it (e.g. `m08_hanlon's_razor.md`), matching existing convention.

## Required sections

Every model file must contain these H2 sections, in this order, using the exact labels below. Start from `.claude/skills/mental-models/models/_TEMPLATE.md` to avoid mistakes.

1. `## Mental Model = <Title>`
2. `**Category = <Category Name>**`
3. `**Description:**`
4. `**When to Avoid (or Use with Caution):**`
5. `**Keywords for Situations:**`
6. `**Thinking Steps:**`
7. `**Coaching Questions:**`

Keep each model roughly 2 to 3 KB. Be specific, practical, and plainly written.

## Updating the model index

After adding or renaming a model, update `model-index.json` so the skill loader can find it. Each entry should include:

```json
{
  "id": "m99",
  "title": "Your Title",
  "category": "General Thinking Tools",
  "path": ".claude/skills/mental-models/models/Mental_Model_General/m99_your_title.md",
  "keywords": ["keyword1", "keyword2"]
}
```

Entries are sorted by `id`.

## Validating locally

Before opening a PR, run:

```bash
python scripts/validate_corpus.py
uv run pytest -q
```

`validate_corpus.py` checks:

- Filenames follow `mNN_snake_case.md` and sit in the right category directory.
- All five required sections are present and non-empty.
- Slugs and ids are unique.
- The corpus checksum, printed so a content change is always visible in a diff.

There is **no index to update**. The old `model-index.json` was deleted: the
corpus is parsed from the markdown at import time behind an `lru_cache`, so
adding a model is just adding the file.

## Pull request checklist

- [ ] New/changed model files follow the naming convention.
- [ ] All required sections are present and non-empty.
- [ ] `python scripts/validate_corpus.py` passes.
- [ ] `uv run pytest -q` passes.
- [ ] The model has a real **When to Avoid** section — a model without one is a
      slogan, and that section is what distinguishes this corpus.
- [ ] `CHANGELOG.md` updated with a short entry.
- [ ] PR description explains why the model belongs in the latticework.

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](./CODE_OF_CONDUCT.md).
