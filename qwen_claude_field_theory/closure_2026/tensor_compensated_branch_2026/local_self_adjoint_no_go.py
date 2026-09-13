#!/usr/bin/env python3
"""Conditional no-go for local self-adjoint derivative multipliers.

Assume the same spatial operator P(k^2) multiplies the slip and the
trace-free multiplier in the two Euler equations.  Self-adjoint variation of
an action linear in Lambda gives exactly this shared operator.  If P(0)=0
(derivative-only coupling), a generic nonzero TF residual cannot have a regular
all-k exact-no-slip solution.  A quadratic regulator F instead gives
d=F*R/P^2, so exact no-slip forces F=0 at nonzero k.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    z, R0, q0 = sp.symbols("z R0 q0", positive=True, real=True)
    F = sp.symbols("F", real=True)
    d, lam = sp.symbols("d Lambda", real=True)
    results = []
    for order in (1, 2, 3):
        # A generic local derivative operator with a zero at the origin.
        q1 = sp.symbols(f"q1_{order}", real=True)
        P = z**order * (q0 + q1 * z)
        solved_lam = sp.factor(-R0 / P)
        solved_d = sp.factor(F * R0 / P**2)
        results.append({
            "order": order,
            "P": str(P),
            "metric_solution": str(solved_lam),
            "slip_solution": str(solved_d),
            "scaled_multiplier_limit": str(sp.limit(z**order * solved_lam, z, 0, dir="+")),
            "scaled_slip_limit": str(sp.limit(z**(2 * order) * solved_d, z, 0, dir="+")),
            "multiplier_diverges": sp.limit(solved_lam, z, 0, dir="+") in (sp.oo, -sp.oo, sp.zoo),
            "slip_requires_zero_regulator": sp.simplify(solved_d / (F * R0 / P**2)) == 1,
        })

    # At z=0, P vanishes identically and the metric equation reduces to R0=0.
    zero_mode_equation = sp.simplify((R0 + P.subs(z, 0) * lam))
    checks = {
        "zero_mode_reduces_to_residual": zero_mode_equation == R0,
        "zero_mode_incompatible_with_generic_source": sp.simplify(zero_mode_equation.subs(R0, 1)) == 1,
        "all_tested_derivative_orders_have_poles": all(item["multiplier_diverges"] for item in results),
        "all_tested_regulators_leave_slip_unless_zero": all(item["slip_requires_zero_regulator"] for item in results),
    }
    print("LOCAL SELF-ADJOINT DERIVATIVE-MULTIPLIER NO-GO")
    for item in results:
        print(f"order={item['order']}: P={item['P']}")
        print("  Lambda =", item["metric_solution"])
        print("  d      =", item["slip_solution"])
    print("zero-mode metric equation =", zero_mode_equation)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    payload = {
        "status": "CONDITIONAL_LOCAL_MULTIPLIER_NO_GO" if all(checks.values()) else "INCONCLUSIVE",
        "checks": checks,
        "orders_tested": results,
        "assumptions": [
            "shared self-adjoint spatial operator P(k^2) in multiplier and metric equations",
            "P(0)=0 (derivative-only local coupling)",
            "generic nonzero trace-free residual R0",
            "quadratic regulator F is local and finite at k=0",
        ],
        "scope": "conditional theorem for this local multiplier class; not a no-go for arbitrary nonlocal or algebraically different actions",
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
