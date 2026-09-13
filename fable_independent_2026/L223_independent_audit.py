#!/usr/bin/env python3
"""Independent audit of L223's end-to-end consolidation claim.

L223 is valuable as a simultaneous consistency check, but it is not allowed to
call a gate action-derived when its measured value is inserted as a literal.
This audit parses the executable source and reports such insertions in the
gate table, plus whether the run uses a labelled stand-in reach.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
import sys


def is_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str))


def main() -> int:
    path = Path(__file__).with_name("L223_end_to_end.py")
    text = path.read_text()
    tree = ast.parse(text, filename=str(path))
    literal_measurements = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "gates" for t in node.targets):
            continue
        if not isinstance(node.value, ast.List):
            continue
        for entry in node.value.elts:
            if not isinstance(entry, ast.Tuple) or len(entry.elts) < 2:
                continue
            name = entry.elts[0]
            measurement = entry.elts[1]
            if isinstance(name, ast.Constant) and is_literal(measurement):
                literal_measurements.append(
                    {"line": entry.lineno, "gate": name.value, "measurement": ast.unparse(measurement)}
                )

    hardcoded_ppn = [x for x in literal_measurements if any(
        key in str(x["gate"]).lower() for key in ("gamma", "alpha", "preferred-frame")
    )]
    uses_standin = "stand-in" in text.lower() and "KAPPA =" in text
    findings = {
        "literal_gate_measurements": literal_measurements,
        "hardcoded_ppn_measurements": hardcoded_ppn,
        "uses_forest_standin": uses_standin,
        "has_action_variation": "Euler" in text or "variation" in text,
    }
    status = "CONSOLIDATION_NOT_ACTION_CERTIFICATION"
    print(json.dumps({"status": status, "findings": findings}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
