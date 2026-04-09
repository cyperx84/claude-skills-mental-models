"""mental_models: Charlie Munger's latticework of mental models as a Python library."""
from .index import Model, load_index, get_model, list_categories
from .selector import select_models, select_models_with_claude

__version__ = "0.2.0"
__all__ = [
    "Model",
    "load_index",
    "get_model",
    "list_categories",
    "select_models",
    "select_models_with_claude",
]
