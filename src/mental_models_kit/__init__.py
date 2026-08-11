"""mental-models-kit: Charlie Munger's latticework of 98 mental models.

Retrieval is deterministic and lives here. **Selection is reasoning and belongs
to the calling LLM** -- hand it :func:`render_catalog` output and let it pick.
"""

from __future__ import annotations

from .catalog import render_catalog
from .corpus import (
    CATEGORIES,
    Category,
    ContentRootNotFound,
    Model,
    ModelNotFound,
    UnknownCategory,
    get_model,
    list_categories,
    list_models,
    load_models,
    models_root,
    normalize_slug,
    set_content_root,
    skill_root,
)
from .search import search_models

__version__ = "0.3.0"

__all__ = [
    "CATEGORIES",
    "Category",
    "ContentRootNotFound",
    "Model",
    "ModelNotFound",
    "UnknownCategory",
    "__version__",
    "get_model",
    "list_categories",
    "list_models",
    "load_models",
    "models_root",
    "normalize_slug",
    "render_catalog",
    "search_models",
    "set_content_root",
    "skill_root",
]
