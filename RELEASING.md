# Releasing `mental-models`

The Python package in `packages/mental_models/` publishes to PyPI via GitHub Actions using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC, no tokens).

## One-time PyPI setup

1. Create the project on PyPI: https://pypi.org/manage/account/publishing/
2. Add a **pending publisher** with:
   - PyPI Project Name: `mental-models`
   - Owner: `cyperx84`
   - Repository: `mental-models`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`
3. Repeat on https://test.pypi.org with environment name `testpypi` (for dry-runs).
4. In GitHub repo settings → Environments, create `pypi` and `testpypi` (can add protection rules).

## Cutting a release

1. Bump version in `packages/mental_models/pyproject.toml`
2. Update `CHANGELOG.md` — move Unreleased entries under a new `## [X.Y.Z] - YYYY-MM-DD`
3. Sync package data: `python scripts/sync_package_data.py`
4. Test locally:
   ```bash
   cd packages/mental_models
   uv sync
   uv run pytest
   uv build
   uv tool run twine check dist/*
   ```
5. Commit, tag, push:
   ```bash
   git commit -am "release: mental-models vX.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```
6. Create a GitHub Release from the tag → `publish.yml` runs → package on PyPI.

## TestPyPI dry-run

Trigger `publish.yml` manually via workflow_dispatch with `target: testpypi` before cutting a real release.
