#!/usr/bin/env python3
"""Operator-level IR tradeoff for screened/hyperbolic compensators.

Replacing the pure Laplacian by a Helmholtz or covariant wave operator gives
the formal response

    Lambda = -R / (k^2 + m^2 - omega^2/c^2).

This gate computes the static IR limit and the pole of the dynamical operator.
It does not claim that this operator has already been embedded in the
covariant MOND action; that embedding is the remaining construction problem.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    k, omega, m, c, R = sp.symbols("k omega m c R", positive=True, real=True)
    P = k**2 + m**2 - omega**2 / c**2
    lam = -R / P
    static = sp.simplify(lam.subs(omega, 0))
    static_ir = sp.limit(static, k, 0, dir="+")
    massless_static_ir = sp.limit(static.subs(m, 0), k, 0, dir="+")
    pole_frequency = sp.solve(sp.Eq(P, 0), omega)

    checks = {
        "static_equation_is_solved": sp.simplify(P * lam + R) == 0,
        "massive_elliptic_response_is_ir_finite": static_ir not in (sp.oo, -sp.oo, sp.zoo),
        "massless_elliptic_response_has_ir_pole": massless_static_ir in (sp.oo, -sp.oo, sp.zoo),
        "hyperbolic_completion_has_frequency_pole": len(pole_frequency) >= 1,
        "pole_solves_the_dispersion_relation": bool(pole_frequency)
        and sp.simplify(P.subs(omega, pole_frequency[0])) == 0,
    }
    print("IR OPERATOR TRADEOFF GATE")
    print("operator P(k,omega) =", P)
    print("static response Lambda =", static)
    print("static k->0 limit =", static_ir)
    print("massless static k->0 limit =", massless_static_ir)
    print("hyperbolic poles omega =", pole_frequency)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    payload = {
        "status": "SCREENED_ELLIPTIC_OR_PROPAGATING_HYPERBOLIC_FORK"
        if all(checks.values())
        else "INCONCLUSIVE",
        "checks": checks,
        "operator": str(P),
        "static_response": str(static),
        "static_ir_limit": str(static_ir),
        "hyperbolic_poles": [str(x) for x in pole_frequency],
        "interpretation": (
            "A nonzero Helmholtz mass makes the purely spatial response finite "
            "but introduces a new screening scale. Promoting the operator to a "
            "wave operator produces a real frequency pole and hence a propagating "
            "auxiliary mode. The covariant action-level embedding remains open."
        ),
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
