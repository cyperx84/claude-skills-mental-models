"""mental-models -- deterministic retrieval over 98 mental models.

The CLI never calls an LLM. It emits a compact catalog for the calling harness
to select from, and retrieves exact slugs. ``search`` is a documented
best-effort keyword fallback, not a selector.

Exit codes:
    0  success
    1  unexpected internal error
    2  not found (unknown slug/id; search with zero results)
    3  bad arguments (argparse errors, empty query, --top <= 0, unknown field
       or category)
    4  content root not found
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import __version__
from .catalog import FORMATS, catalog_document, render_catalog
from .corpus import (
    ContentRootNotFound,
    ModelNotFound,
    UnknownCategory,
    content_root_source,
    get_model,
    list_categories,
    list_models,
    load_models,
    models_root,
    resolve_category,
    set_content_root,
)
from .render import FIELD_NAMES, apply_dict, field_value, model_detail_dict, model_dict
from .search import has_searchable_tokens, search_models

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NOT_FOUND = 2
EXIT_BAD_ARGS = 3
EXIT_NO_CONTENT = 4


# ---------------------------------------------------------------- helpers


def _print_json(obj: Any) -> None:
    json.dump(obj, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def _err(msg: str) -> None:
    """Errors and warnings always go to stderr, so ``--json`` stdout stays parseable."""
    print(msg, file=sys.stderr)


def _flag(args: argparse.Namespace, name: str, default: Any = None) -> Any:
    # Shared flags use argparse.SUPPRESS defaults so a subparser cannot clobber a
    # value given before the subcommand (`mental-models --json list`).
    return getattr(args, name, default)


# ------------------------------------------------------------- subcommands


def cmd_catalog(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False) or args.format == "json"
    category = args.category
    if json_mode:
        cats = list_categories()
        if category is not None:
            wanted = resolve_category(category)
            cats = tuple(c for c in cats if c.key == wanted.key)
        payload = {
            "count": sum(c.count for c in cats),
            "categories": [
                {
                    "key": c.key,
                    "display": c.display,
                    "count": c.count,
                    "models": [model_dict(m) for m in list_models(c.key)],
                }
                for c in cats
            ],
        }
        _print_json(payload)
        return EXIT_OK
    if args.with_header:
        sys.stdout.write(catalog_document(args.format, category))
    else:
        sys.stdout.write(render_catalog(args.format, category))
    return EXIT_OK


def cmd_get(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False)
    slug = (args.slug or "").strip()
    if not slug:
        _err("error: empty slug")
        return EXIT_BAD_ARGS
    try:
        m = get_model(slug)
    except ModelNotFound as e:
        _err(f"error: {e}")
        return EXIT_NOT_FOUND

    if args.field:
        try:
            value = field_value(m, args.field)
        except ValueError as e:
            _err(f"error: {e}")
            return EXIT_BAD_ARGS
        if json_mode:
            _print_json(value)
        elif isinstance(value, list):
            print("\n".join(value))
        else:
            sys.stdout.write(value if value.endswith("\n") else value + "\n")
        return EXIT_OK

    if json_mode:
        _print_json(model_detail_dict(m))
        return EXIT_OK
    md = m.markdown
    sys.stdout.write(md if md.endswith("\n") else md + "\n")
    return EXIT_OK


def cmd_list(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False)
    models = list_models(args.category)
    if json_mode:
        _print_json({"count": len(models), "models": [model_dict(m) for m in models]})
        return EXIT_OK
    for m in models:
        print(f"{m.slug}\t{m.name}\t{m.category}")
    return EXIT_OK


def cmd_categories(args: argparse.Namespace) -> int:
    cats = list_categories()
    if _flag(args, "json", False):
        _print_json([{"key": c.key, "display": c.display, "count": c.count} for c in cats])
        return EXIT_OK
    for c in cats:
        print(f"{c.key}\t{c.display}\t{c.count}")
    return EXIT_OK


def cmd_apply(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False)
    slug = (args.slug or "").strip()
    if not slug:
        _err("error: empty slug")
        return EXIT_BAD_ARGS
    try:
        m = get_model(slug)
    except ModelNotFound as e:
        _err(f"error: {e}")
        return EXIT_NOT_FOUND
    problem = " ".join(args.problem).strip() if args.problem else ""
    payload = apply_dict(m, problem)
    if json_mode:
        _print_json(payload)
        return EXIT_OK
    print(f"# Applying {m.name} to: {problem or '(no problem supplied)'}")
    print()
    for key in ("description", "thinking_steps", "coaching_questions", "when_to_avoid"):
        value = payload[key]
        if value:
            print(f"## {key.replace('_', ' ').title()}\n{value}\n")
    return EXIT_OK


def cmd_search(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False)
    query = " ".join(args.query).strip()
    if not query:
        _err("error: empty query")
        return EXIT_BAD_ARGS
    if args.top is not None and args.top <= 0:
        _err("error: --top must be a positive integer")
        return EXIT_BAD_ARGS
    if len(query) > 4096:
        _err(f"warning: query is {len(query)} chars; truncated to 4096 for scoring")
    if not has_searchable_tokens(query):
        _err("error: query contains no searchable tokens (stopwords/punctuation only)")
        if json_mode:
            _print_json({"query": query, "count": 0, "models": []})
        return EXIT_NOT_FOUND

    results = search_models(query, top_k=args.top)
    if json_mode:
        _print_json(
            {
                "query": query,
                "count": len(results),
                "models": [model_dict(m) for m in results],
            }
        )
        return EXIT_OK if results else EXIT_NOT_FOUND
    if not results:
        _err("No matching models found.")
        return EXIT_NOT_FOUND
    _err(
        "note: keyword matching is a fallback, not selection. "
        "For a real problem run `mental-models catalog` and choose yourself."
    )
    for i, m in enumerate(results, 1):
        desc = (m.description or "").strip().replace("\n", " ")
        if len(desc) > 140:
            desc = desc[:137] + "..."
        print(f"{i}. {m.name} [{m.slug}]  ({m.category})")
        if desc:
            print(f"   {desc}")
        print(f"   path: {m.path}")
    return EXIT_OK


def cmd_which(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False)
    root = models_root()
    source = content_root_source()
    count = len(load_models())
    if json_mode:
        _print_json(
            {
                "content_root": str(root),
                "exists": root.is_dir(),
                "source": source,
                "model_count": count,
            }
        )
    else:
        print(root)
        print(f"source: {source}")
        print(f"models: {count}")
    return EXIT_OK


def cmd_doctor(args: argparse.Namespace) -> int:
    json_mode = _flag(args, "json", False)
    report: dict[str, Any] = {"version": __version__, "ok": True, "checks": {}}
    checks = report["checks"]
    try:
        root = models_root()
        checks["content_root"] = str(root)
        checks["content_root_exists"] = root.is_dir()
        checks["source"] = content_root_source()
        if not root.is_dir():
            report["ok"] = False
    except ContentRootNotFound as e:
        report["ok"] = False
        checks["content_root_error"] = str(e)
    try:
        models = load_models()
        checks["model_count"] = len(models)
        if not models:
            report["ok"] = False
    except Exception as e:  # noqa: BLE001 - doctor never raises
        report["ok"] = False
        checks["model_count_error"] = str(e)
    try:
        checks["category_count"] = len(list_categories())
    except Exception as e:  # noqa: BLE001
        report["ok"] = False
        checks["category_count_error"] = str(e)
    try:
        checks["catalog_bytes"] = len(catalog_document("compact").encode("utf-8"))
    except Exception as e:  # noqa: BLE001
        report["ok"] = False
        checks["catalog_bytes_error"] = str(e)

    if json_mode:
        _print_json(report)
    else:
        print(f"mental-models {report['version']}")
        print(f"status: {'OK' if report['ok'] else 'FAIL'}")
        for k, v in checks.items():
            print(f"  {k}: {v}")
    if "content_root_error" in checks:
        return EXIT_NO_CONTENT
    return EXIT_OK if report["ok"] else EXIT_ERROR


def cmd_version(args: argparse.Namespace) -> int:
    if _flag(args, "json", False):
        _print_json({"version": __version__})
    else:
        print(__version__)
    return EXIT_OK


# ------------------------------------------------------------ argparse plumbing


class _Parser(argparse.ArgumentParser):
    """argparse hardcodes exit status 2 for usage errors, which collides with
    "not found". Usage errors are bad arguments -- exit 3."""

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        self.exit(EXIT_BAD_ARGS, f"{self.prog}: error: {message}\n")


def _build_parser() -> argparse.ArgumentParser:
    # SUPPRESS defaults: without them a subparser re-parses the shared flags into
    # a fresh namespace and overwrites anything given before the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit JSON on stdout (all messages move to stderr)",
    )
    common.add_argument(
        "--content-root",
        metavar="PATH",
        default=argparse.SUPPRESS,
        help="Directory containing the Mental_Model_* folders",
    )

    parser = _Parser(
        prog="mental-models",
        description=(
            "Charlie Munger's latticework of 98 mental models. "
            "Run `catalog`, pick 2-4 models yourself, then `get` each by slug."
        ),
        parents=[common],
    )
    parser.add_argument("-V", "--version", action="store_true", help="Print version and exit")
    sub = parser.add_subparsers(dest="cmd", metavar="<command>", parser_class=_Parser)

    def add(name: str, **kw: Any) -> argparse.ArgumentParser:
        return sub.add_parser(name, parents=[common], **kw)

    p_cat = add("catalog", help="Print the compact catalog for an LLM to select from")
    p_cat.add_argument(
        "--format", choices=(*FORMATS, "json"), default="compact", help="Catalog format"
    )
    p_cat.add_argument("--category", help="Restrict to one category (key or display name)")
    p_cat.add_argument(
        "--with-header",
        action="store_true",
        help="Include the CATALOG.md header (this is the CI drift-gate form)",
    )
    p_cat.set_defaults(func=cmd_catalog)

    p_get = add("get", help="Retrieve one model by slug or id")
    p_get.add_argument("slug", help="Model slug (e.g. inversion) or id (e.g. m07)")
    p_get.add_argument("--field", help=f"Return a single field: {', '.join(FIELD_NAMES)}")
    p_get.set_defaults(func=cmd_get)

    p_list = add("list", help="List models")
    p_list.add_argument("--category", help="Filter by category key or display name")
    p_list.set_defaults(func=cmd_list)

    p_cats = add("categories", help="List the 8 categories and their counts")
    p_cats.set_defaults(func=cmd_categories)

    p_apply = add("apply", help="Thinking-steps / coaching-questions scaffold")
    p_apply.add_argument("slug", help="Model slug or id")
    p_apply.add_argument("--problem", nargs="*", help="The problem to apply the model to")
    p_apply.set_defaults(func=cmd_apply)

    p_search = add(
        "search",
        help="Best-effort keyword match (NOT selection -- use `catalog` for that)",
    )
    p_search.add_argument("query", nargs="+", help="Words to match")
    p_search.add_argument("-k", "--top", type=int, default=5, help="How many to return")
    p_search.set_defaults(func=cmd_search)

    p_which = add("which", help="Show the resolved content root")
    p_which.set_defaults(func=cmd_which)

    p_doctor = add("doctor", help="Health check")
    p_doctor.set_defaults(func=cmd_doctor)

    p_ver = add("version", help="Print version")
    p_ver.set_defaults(func=cmd_version)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:  # --help exits 0; usage errors exit 3 via _Parser
        return int(e.code or 0)

    if args.version:
        print(__version__)
        return EXIT_OK
    if not args.cmd:
        parser.print_help()
        return EXIT_OK

    override = _flag(args, "content_root")
    if override:
        set_content_root(override)

    try:
        return int(args.func(args))
    except ContentRootNotFound as e:
        _err(f"error: {e}")
        return EXIT_NO_CONTENT
    except (UnknownCategory, ValueError) as e:
        _err(f"error: {e}")
        return EXIT_BAD_ARGS
    except ModelNotFound as e:
        _err(f"error: {e}")
        return EXIT_NOT_FOUND
    except Exception as e:  # noqa: BLE001
        _err(f"error: {e}")
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
