# Scripts

Stdlib-only, no network, no API key. Both read the markdown corpus through
`mental_models_kit.corpus` — there is no JSON index any more.

## `validate_corpus.py`

Format gate for the 98 model files. Per file it asserts:

- exactly one `## Mental Model = <Name>` header and one `**Category = …**` line
- each of the five bold section labels matches its regex **exactly once**
  (a substring search would let the bare word "description" in prose pass)
- every extracted section is non-empty
- the filename matches `m\d{2}_<slug>.md` and the parent is one of the eight
  category directories, with the expected per-directory counts
- normalized slugs are unique

Then it re-checks the content checksum — the sha256 of the sorted per-file
sha256 list — against the pinned value. A mismatch means the model prose was
edited, which is forbidden.

```bash
python3 scripts/validate_corpus.py
```

Equivalent shell gate (`-print0`/`-0` are mandatory: two filenames contain
apostrophes, and a plain `find | xargs shasum` dies with `unterminated quote`,
hashes nothing, and prints the sha256 of the empty string):

```bash
find skills/mental-models/models -name '*.md' ! -name '_TEMPLATE.md' -print0 \
  | xargs -0 shasum -a 256 | awk '{print $1}' | sort | shasum -a 256
# 12f869084e3019de5f11e714c69c20f07525a6032ae642517ef51a898ca27ffe
```

## `build_latticework.py`

Builds the shared-keyword graph and writes `docs/latticework.json`,
`docs/latticework.mmd` and `docs/latticework_core.mmd`. Output is fully sorted,
so CI drift-checks it with `git diff --exit-code`. `docs/latticework.svg` is
rendered separately and is not touched.

```bash
python3 scripts/build_latticework.py
```

Both exit 0 on success, 1 on failure.
