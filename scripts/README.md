# Scripts

## validate_models.py

Validates the `mental-models` skill: SKILL.md frontmatter, required H2
sections in every model file, and `model-index.json` drift in both
directions (missing entries and stale references).

Run locally from the repo root:

```bash
python3 scripts/validate_models.py
```

Exits 0 on success, 1 on failure. No dependencies beyond the Python 3 stdlib.
Used by `.github/workflows/validate.yml` in CI.
