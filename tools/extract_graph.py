"""AST-based import/class graph extractor for simulasyon_11.py (PR 3)."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any


def _resolve_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _resolve_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def _collect_imports(tree: ast.Module) -> list[dict[str, Any]]:
    imports: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "kind": "import",
                        "module": alias.name,
                        "name": alias.asname or alias.name,
                        "line": node.lineno,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(
                    {
                        "kind": "from",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno,
                    }
                )
    return imports


def _collect_classes(tree: ast.Module) -> list[dict[str, Any]]:
    classes: list[dict[str, Any]] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [_resolve_name(base) for base in node.bases]
        methods = [
            n.name
            for n in node.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        classes.append(
            {
                "name": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "bases": [b for b in bases if b],
                "methods": methods,
            }
        )
    return classes


def _build_class_edges(classes: list[dict[str, Any]]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    for cls in classes:
        for base in cls["bases"]:
            base_name = base.split(".")[-1]
            edges.append({"from": cls["name"], "to": base_name, "kind": "inherits"})
    return edges


def extract_graph(source_path: Path) -> dict[str, Any]:
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    classes = _collect_classes(tree)
    return {
        "source": str(source_path),
        "line_count": source.count("\n") + 1,
        "imports": _collect_imports(tree),
        "classes": classes,
        "class_edges": _build_class_edges(classes),
        "duplicate_class_names": sorted(
            {
                name
                for name in {c["name"] for c in classes}
                if sum(1 for c in classes if c["name"] == name) > 1
            }
        ),
    }


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parent.parent
    source = Path(argv[0]) if argv else root / "simulasyon_11.py"
    output = root / "archive" / "audits" / "import_graph.json"

    if not source.exists():
        print(f"Source not found: {source}", file=sys.stderr)
        return 1

    graph = extract_graph(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(graph, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(
        f"Wrote {output} "
        f"({len(graph['classes'])} classes, {len(graph['imports'])} imports)"
    )
    if graph["duplicate_class_names"]:
        print(f"Duplicate classes: {', '.join(graph['duplicate_class_names'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))