"""Minimal CLI: `mental-models "how do I decide between two jobs"`."""
from __future__ import annotations

import argparse
import sys

from .selector import select_models


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mental-models",
        description="Select relevant mental models for a problem or query.",
    )
    parser.add_argument("query", nargs="+", help="Your problem or question")
    parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of models to return")
    args = parser.parse_args(argv)

    query = " ".join(args.query)
    results = select_models(query, top_k=args.top_k)
    if not results:
        print("No matching models found.", file=sys.stderr)
        return 1
    print(f"Top {len(results)} mental models for: {query!r}\n")
    for i, m in enumerate(results, 1):
        desc = (m.description or "").strip().replace("\n", " ")
        if len(desc) > 140:
            desc = desc[:137] + "..."
        print(f"{i}. {m.name} [{m.slug}]  ({m.category})")
        print(f"   {desc}")
        print(f"   path: {m.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
