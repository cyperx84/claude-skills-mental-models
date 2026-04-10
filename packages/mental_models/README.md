# mental-models

Charlie Munger's latticework of mental models as a tiny Python library.

Wraps the [`mental-models` Claude Code skill](https://github.com/cyperx84/mental-models)
so you can select and look up models programmatically, without needing Claude Code.

## Install

```bash
# From the repo (editable):
pip install -e packages/mental_models

# Optional Claude-powered selection:
pip install -e "packages/mental_models[claude]"
```

## Quickstart

```python
from mental_models import select_models, get_model, list_categories

hits = select_models("how do I decide between two jobs", top_k=5)
for m in hits:
    print(m.slug, "-", m.name, f"({m.category})")

inversion = get_model("inversion")
print(inversion.description)

print(list_categories())
```

## CLI

The CLI is the canonical interface — the Claude Code skill, MCP server, and any third-party harness all shell out to it. Every command supports `--json`.

```bash
# Discovery
mental-models select "how do I decide between two jobs" -k 5
mental-models select "scaling issues" --json
mental-models categories
mental-models list --category "Human Nature"

# Lookup
mental-models get inversion                  # full markdown
mental-models get inversion --field keywords
mental-models get inversion --json

# Guided application (structured output for agents)
mental-models apply inversion --problem "pricing strategy" --json

# Meta
mental-models doctor           # diagnose install, data path, model count
mental-models which            # print resolved index path
mental-models version
```

**Exit codes**: 0 ok, 2 not found, 3 bad args.

Run without install: `uvx mental-models select "your query"`.

## API

- `select_models(query: str, top_k: int = 5) -> list[Model]` keyword-scored search
- `get_model(slug: str) -> Model` exact slug lookup (raises `KeyError` if missing)
- `list_categories() -> list[str]` unique category names
- `load_index() -> list[Model]` all models (cached)
- `select_models_with_claude(query, api_key=None)` optional; uses `anthropic` SDK
  if installed, otherwise transparently falls back to the keyword selector

### `Model`

```python
@dataclass(frozen=True)
class Model:
    slug: str
    name: str
    category: str
    keywords: tuple[str, ...]
    description: str
    path: str
    id: str
```

## Data source

The package loads `model-index.json` using this resolution order:

1. Walks up from `cwd` for `.claude/skills/mental-models/resources/model-index.json`
2. Walks up from the package install location for the same file
3. Falls back to the bundled copy at `mental_models/data/model-index.json`

In the source tree, the bundled copy is a **symlink** to the canonical index to
avoid duplication. When a wheel is built, `hatch` follows the symlink and ships
a real file.

## License

MIT. See the main repo.
