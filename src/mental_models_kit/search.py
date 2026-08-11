"""Best-effort keyword scorer.

This is **retrieval, not selection**. It works well when you already know a
model's name and want to find it; it is measurably wrong on natural-language
problem statements (see ``evals/selection_cases.jsonl`` for the honest ledger).
The primary selection path is the harness LLM reading
:func:`mental_models_kit.render_catalog` output and choosing for itself.

Scoring (unchanged from the pre-rebuild implementation): a query token scores
+4.0 against name tokens, +3.0 against keyword tokens, +1.0 against description
tokens and +0.5 for a raw substring hit in the description; a whole model name
appearing in the query adds +5.0. Ties break on slug, so output is deterministic.
"""

from __future__ import annotations

import re
from functools import lru_cache

from .corpus import Model, load_models, register_cache_clearer

__all__ = ["search_models"]

# Longest query we will tokenize. Beyond this we truncate so a pasted 10 KB blob
# cannot thrash the scorer.
_MAX_QUERY_CHARS = 4096

_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "else", "is", "are",
    "was", "were", "be", "been", "being", "of", "to", "in", "on", "at", "by",
    "for", "with", "about", "as", "into", "through", "during", "how", "do",
    "i", "me", "my", "we", "our", "you", "your", "it", "its", "this", "that",
    "these", "those", "should", "could", "would", "can", "will", "just",
    "between", "from", "up", "down", "out", "over", "under", "again", "not",
    "no", "yes", "so", "than", "too", "very", "s", "t",
}

_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9\-]+")

_IRREGULAR = {
    "crises": "crisis",
    "analyses": "analysis",
    "hypotheses": "hypothesis",
    "diagnoses": "diagnosis",
    "syntheses": "synthesis",
    "emphases": "emphasis",
    "theses": "thesis",
    "biases": "bias",
}


def _stem(w: str) -> str:
    """Zero-dependency suffix stemmer folding common plurals onto singulars."""
    if len(w) <= 3:
        return w
    if w in _IRREGULAR:
        return _IRREGULAR[w]
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("sses") or w.endswith("xes"):
        return w[:-2]
    if w.endswith("ches") or w.endswith("shes"):
        if w in ("niches",):
            return w[:-1]
        return w[:-2]
    if w.endswith("s"):
        if any(w.endswith(x) for x in ("as", "is", "us", "os", "ss")):
            return w
        return w[:-1]
    return w


def _tokenize(text: str) -> list[str]:
    """Lowercase ASCII word tokens, stopwords dropped, lightly stemmed.

    Hyphenated tokens also emit their bare subwords so ``first-principle``
    matches ``first principles``. Non-ASCII letters are dropped by the regex.
    """
    if not text:
        return []
    if len(text) > _MAX_QUERY_CHARS:
        text = text[:_MAX_QUERY_CHARS]
    out: list[str] = []
    for raw in _TOKEN_RE.findall(text):
        t = raw.lower()
        if len(t) > 1 and t not in _STOPWORDS:
            out.append(_stem(t))
        if "-" in t:
            for part in t.split("-"):
                if len(part) > 1 and part not in _STOPWORDS:
                    out.append(_stem(part))
    return out


def has_searchable_tokens(query: str) -> bool:
    """False when the query is empty or reduces to stopwords/punctuation."""
    return bool(_tokenize(query))


@lru_cache(maxsize=1)
def _token_index() -> dict[str, tuple[frozenset[str], frozenset[str], frozenset[str]]]:
    """slug -> (name tokens, keyword tokens, description tokens).

    Registered with the corpus cache registry so a ``set_content_root`` swap
    cannot leave a stale index behind.
    """
    index: dict[str, tuple[frozenset[str], frozenset[str], frozenset[str]]] = {}
    for m in load_models():
        kw: set[str] = set()
        for k in m.keywords:
            kw.update(_tokenize(k))
        index[m.slug] = (
            frozenset(_tokenize(m.name)),
            frozenset(kw),
            frozenset(_tokenize(m.description)),
        )
    return index


register_cache_clearer(lambda: _token_index.cache_clear())


def _score(m: Model, query_tokens: list[str], query_lower: str) -> float:
    name_tokens, kw_tokens, desc_tokens = _token_index()[m.slug]
    desc_lower = (m.description or "").lower()
    score = 0.0
    for qt in query_tokens:
        if qt in name_tokens:
            score += 4.0
        if qt in kw_tokens:
            score += 3.0
        if qt in desc_tokens:
            score += 1.0
        if qt in desc_lower:
            score += 0.5
    if m.name and m.name.lower() in query_lower:
        score += 5.0
    return score


def search_models(query: str, top_k: int = 5) -> tuple[Model, ...]:
    """Best-effort keyword match. This is retrieval, not selection -- see
    ``render_catalog()``.

    Returns an empty tuple for an empty, whitespace-only or stopword-only query,
    and for ``top_k <= 0``.
    """
    if top_k <= 0:
        return ()
    q_tokens = _tokenize(query)
    if not q_tokens:
        return ()
    q_lower = (query or "")[:_MAX_QUERY_CHARS].lower()
    scored = [(m, _score(m, q_tokens, q_lower)) for m in load_models()]
    scored = [pair for pair in scored if pair[1] > 0]
    scored.sort(key=lambda p: (-p[1], p[0].slug))
    return tuple(m for m, _ in scored[:top_k])
