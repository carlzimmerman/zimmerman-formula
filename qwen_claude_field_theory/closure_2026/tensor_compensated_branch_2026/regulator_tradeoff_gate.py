#!/usr/bin/env python3
"""Test local quadratic regulators against IR regularity and exact no-slip.

At linear order the tensor-compensated branch has a Hessian metric coupling
``R + k**2*Lambda = 0`` and a multiplier equation of the form
``k**2*d + F(k**2)*Lambda = 0``, where d is the slip variable and F is any
local quadratic regulator kernel.  Solving both equations shows the tradeoff:
the metric equation fixes Lambda ~ 1/k**2; any nonzero regulator then creates
slip d ~ F*R/k**4.  Setting F to zero restores no-slip but leaves the IR pole.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    k, M2, S, y = sp.symbols("k M2 S y", positive=True, real=True)
    d, lam = sp.symbols("d Lambda_TF", real=True)
    f0, f2 = sp.symbols("f0 f2", real=True)
    residual = 2 * M2 * S * y**2 * sp.exp(-y)
    regulator = f0 + f2 * k**2
    equations = [sp.Eq(k**2 * d + regulator * lam, 0),
                 sp.Eq(residual + k**2 * lam, 0)]
    solution = sp.solve(equations, (d, lam), dict=True)[0]
    solved_lam = sp.factor(solution[lam])
    solved_slip = sp.factor(solution[d])

    # The no-slip condition for a nonzero residual is equivalent to a vanishing
    # regulator kernel.  A nonzero constant regulator makes the IR singularity
    # worse (d~k^-4); higher-derivative terms still leave d~k^-2.
    no_slip_condition = sp.factor(solved_slip / residual)
    finite_regulator_slip = sp.limit(solved_slip, k, 0, dir="+")
    pole_without_regulator = sp.factor(solved_lam.subs({f0: 0, f2: 0}))
    checks = {
        "metric_equation_is_satisfied": sp.simplify(residual + k**2 * solved_lam) == 0,
        "multiplier_equation_is_satisfied": sp.simplify(k**2 * solved_slip + regulator * solved_lam) == 0,
        "exact_no_slip_requires_zero_regulator": sp.simplify(no_slip_condition - regulator / k**4) == 0,
        "constant_regulator_has_ir_slip": sp.limit(
            solved_slip.subs({f0: 1, f2: 0, M2: 1, S: 1, y: 1}), k, 0, dir="+"
        ) in (sp.oo, -sp.oo, sp.zoo),
        "unregularized_multiplier_has_inverse_laplacian": pole_without_regulator == -residual / k**2,
    }
    print("LOCAL REGULATOR TRADEOFF GATE")
    print("solved Lambda_TF =", solved_lam)
    print("solved slip d =", solved_slip)
    print("d/R =", no_slip_condition)
    print("IR limit with constant regulator =", finite_regulator_slip)
    print("unregularized Lambda_TF =", pole_without_regulator)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    payload = {
        "status": "LOCAL_REGULATOR_TRADEOFF_CONFIRMED" if all(checks.values()) else "INCONCLUSIVE",
        "checks": checks,
        "lambda_solution": str(solved_lam),
        "slip_solution": str(solved_slip),
        "interpretation": (
            "Within this derivative multiplier architecture, a local quadratic "
            "regulator cannot simultaneously remove the inverse-Laplacian IR "
            "pole and keep exact Phi=Psi for a generic nonzero TF source."
        ),
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
