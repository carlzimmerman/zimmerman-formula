#!/usr/bin/env python3
"""IR regularity test for the tensor-compensated elliptic branch.

The finite-k gate solves the trace-free metric equation

    R_TF + k^2 Lambda_TF = 0.

For a generic anisotropic source R_TF that has a nonzero k->0 limit, the
solution is proportional to 1/k^2.  This script derives that result
symbolically and scans nonzero source values; it does not assume a target
rank, determinant, PPN number, or DOF count.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    k, M2, S, y = sp.symbols("k M2 S y", positive=True, real=True)
    lam = sp.symbols("Lambda_TF", real=True)
    residual = 2 * M2 * S * y**2 * sp.exp(-y)
    equation = sp.Eq(residual + k**2 * lam, 0)
    solution = sp.solve(equation, lam)[0]

    # A regular auxiliary field has a finite limit as k->0.  Its contribution
    # k^2*Lambda then vanishes, so it cannot cancel a nonzero residual.
    regular_product_limit = sp.limit(k**2 * sp.Symbol("L0"), k, 0)
    solution_limit = sp.limit(solution, k, 0, dir="+")
    residual_nonzero = sp.simplify(residual.subs({M2: 1, S: 1, y: 1})) != 0

    checks = {
        "solution_is_inverse_laplacian": sp.simplify(solution * k**2 + residual) == 0,
        "regular_auxiliary_cannot_cancel": regular_product_limit == 0,
        "generic_residual_nonzero": residual_nonzero,
        "solution_diverges_in_ir": solution_limit in (sp.oo, -sp.oo, sp.zoo),
    }
    print("TENSOR COMPENSATOR IR REGULARITY GATE")
    print("trace-free residual R =", residual)
    print("solved Lambda_TF =", solution)
    print("lim[k->0+] k^2 Lambda_regular =", regular_product_limit)
    print("lim[k->0+] Lambda_solution =", solution_limit)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    payload = {
        "status": "IR_SINGULAR_FOR_GENERIC_ANISOTROPIC_SOURCE"
        if all(checks.values())
        else "IR_TEST_INCONCLUSIVE",
        "checks": checks,
        "residual": str(residual),
        "solution": str(solution),
        "interpretation": (
            "The finite-k cancellation requires an inverse spatial Laplacian. "
            "A regular k=0 continuation cannot cancel a nonzero anisotropic "
            "source; the spherical angular-average zero is only a special "
            "source restriction, not a generic IR closure."
        ),
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
