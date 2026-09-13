#!/usr/bin/env python3
"""Audit Dirac/DOF gates for hard-coded expected counts.

The research contract forbids certifying a rank, class count, or DOF count by
comparing it with a preselected integer.  This scanner is deliberately
independent of the SymPy calculations: it inspects the executable source and
reports comparisons involving the derived-count fields.  A clean audit is
necessary (though not sufficient) before a numerical gate can be called a
derivation.

Default mode reports findings and exits zero so it can be used diagnostically.
``--strict`` exits one when any finding is present.
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import sys


FIELDS = {
    "constraint_rank",
    "first_class",
    "second_class",
    "physical_dof",
    "vector_rank",
    "vector_dof",
    "finite_k_physical_dof",
}


def _is_count_field(node: ast.AST) -> bool:
    """Return whether an AST node indexes one of the derived count fields."""
    if not isinstance(node, ast.Subscript):
        return False
    field = node.slice
    if isinstance(field, ast.Constant) and isinstance(field.value, str):
        return field.value in FIELDS
    # Python 3.8 compatibility for ``result["field"]`` represented by Index.
    if isinstance(field, ast.Index):  # pragma: no cover - old Python only
        return isinstance(field.value, ast.Constant) and field.value.value in FIELDS
    return False


def _literal(node: ast.AST) -> bool:
    """Whether node is a literal integer/string count used as an expectation."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, str)) and not isinstance(node.value, bool)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return node.func.attr in {"Integer", "Rational"}
    return False


def scan_file(path: Path) -> list[dict[str, object]]:
    tree = ast.parse(path.read_text(), filename=str(path))
    findings: list[dict[str, object]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare) or len(node.ops) != 1:
            continue
        if not isinstance(node.ops[0], (ast.Eq, ast.NotEq)):
            continue
        sides = [node.left, *node.comparators]
        if not any(_is_count_field(side) for side in sides):
            continue
        field_side = next(side for side in sides if _is_count_field(side))
        other_sides = [side for side in sides if side is not field_side]
        if not any(_literal(side) for side in other_sides):
            continue
        findings.append(
            {
                "file": str(path),
                "line": node.lineno,
                "expression": ast.unparse(node),
            }
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    findings: list[dict[str, object]] = []
    for path in sorted(root.glob("*.py")):
        if path.name == Path(__file__).name:
            continue
        findings.extend(scan_file(path))
    payload = {
        "status": "HARD_CODED_COUNT_EXPECTATIONS_FOUND" if findings else "CLEAN",
        "files_scanned": len(list(root.glob("*.py"))) - 1,
        "finding_count": len(findings),
        "findings": findings,
        "strict_exit_meaning": "nonzero means a gate still compares a derived count to a literal",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
