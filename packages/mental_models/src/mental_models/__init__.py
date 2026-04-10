"""mental_models: Charlie Munger's latticework of mental models as a Python library."""
from .index import Model, load_index, get_model, list_categories
from .selector import select_models, select_models_with_claude
from .utils import model_to_dict, read_model_markdown, extract_sections
from .compare import compare_models, random_model

__version__ = "0.2.0"
__all__ = [
    "Model",
    "load_index",
    "get_model",
    "list_categories",
    "select_models",
    "select_models_with_claude",
    "model_to_dict",
    "read_model_markdown",
    "extract_sections",
    "compare_models",
    "random_model",
]
