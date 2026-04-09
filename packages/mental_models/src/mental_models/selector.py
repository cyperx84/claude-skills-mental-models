"""Keyword-based selector for mental models, with optional Claude enrichment."""
from __future__ import annotations

import re
from typing import Optional

from .index import Model, load_index

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


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "") if t.lower() not in _STOPWORDS and len(t) > 1]


def _score(model: Model, query_tokens: list[str], query_lower: str) -> float:
    if not query_tokens:
        return 0.0
    kw_tokens: set[str] = set()
    for kw in model.keywords:
        kw_tokens.update(_tokenize(kw))
    name_tokens = set(_tokenize(model.name))
    desc_tokens = set(_tokenize(model.description))

    score = 0.0
    for qt in query_tokens:
        if qt in name_tokens:
            score += 4.0
        if qt in kw_tokens:
            score += 3.0
        if qt in desc_tokens:
            score += 1.0
        # substring fallback on raw description
        if qt in (model.description or "").lower():
            score += 0.5

    # Boost if model name appears directly in query
    if model.name and model.name.lower() in query_lower:
        score += 5.0
    return score


def select_models(query: str, top_k: int = 5) -> list[Model]:
    """Return the top_k models most relevant to ``query`` by keyword scoring."""
    models = load_index()
    q_tokens = _tokenize(query)
    q_lower = (query or "").lower()
    scored = [(m, _score(m, q_tokens, q_lower)) for m in models]
    scored = [pair for pair in scored if pair[1] > 0]
    scored.sort(key=lambda p: (-p[1], p[0].slug))
    return [m for m, _ in scored[:top_k]]


def select_models_with_claude(
    query: str,
    top_k: int = 5,
    api_key: Optional[str] = None,
    model: str = "claude-opus-4-5",
) -> list[Model]:
    """Optional: use the Anthropic SDK to pick models. Falls back to keywords.

    Requires ``pip install mental-models[claude]``.
    """
    try:
        import anthropic  # type: ignore
    except ImportError:
        return select_models(query, top_k=top_k)

    try:
        client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
        all_models = load_index()
        catalog = "\n".join(f"- {m.slug}: {m.name} ({m.category})" for m in all_models)
        prompt = (
            f"Given the user's problem, pick up to {top_k} most relevant mental model "
            f"slugs from the catalog. Respond with just the slugs, one per line.\n\n"
            f"Problem: {query}\n\nCatalog:\n{catalog}"
        )
        resp = client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(getattr(b, "text", "") for b in resp.content)
        picks: list[Model] = []
        for line in text.splitlines():
            slug = line.strip().lstrip("-").strip().split()[0].rstrip(":") if line.strip() else ""
            if not slug:
                continue
            for m in all_models:
                if m.slug == slug:
                    picks.append(m)
                    break
            if len(picks) >= top_k:
                break
        return picks or select_models(query, top_k=top_k)
    except Exception:
        return select_models(query, top_k=top_k)
