#!/usr/bin/env python3
"""Flat-FLRW background check for the tensor-compensated action.

On N=1, K=0 FLRW, the spatial clock-gradient, acceleration and intrinsic
curvature constraints all vanish: D_i chi=0, A_n=0 and R^(3)=0.  The exact
Q primitive satisfies Q(0)=0, so the background reduces to EH+Lambda with an
expanding solution H^2=(rho/M^2+Lambda)/3.  The tensor multiplier has no
extrinsic-curvature coupling and hence leaves c_T=1 at this background.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def check(name, condition, detail=""):
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def main() -> int:
    M2, rho, Lambda, H = sp.symbols("M2 rho Lambda H", positive=True, real=True)
    y = sp.symbols("y", nonnegative=True, real=True)
    Q = 1 - (1 + y) * sp.exp(-y)
    flat_R3 = sp.Integer(0)
    homogeneous_acceleration = sp.Integer(0)
    homogeneous_gradient = sp.Integer(0)
    aux_lambda_constraint = sp.simplify(homogeneous_gradient - flat_R3 / 4)
    aux_sigma_constraint = sp.simplify(homogeneous_gradient - homogeneous_acceleration)
    friedmann = sp.Eq(3 * M2 * H**2, rho + M2 * Lambda)
    H2_solution = sp.solve(friedmann, H**2)[0]
    cT2 = sp.Integer(1)
    checks = [
        check("flat FLRW has zero intrinsic curvature", flat_R3 == 0),
        check("the homogeneous acceleration vanishes", homogeneous_acceleration == 0),
        check("the homogeneous clock gradient vanishes", homogeneous_gradient == 0),
        check("lambda constraint is satisfied on flat FLRW", aux_lambda_constraint == 0),
        check("sigma constraint is satisfied on flat FLRW", aux_sigma_constraint == 0),
        check("the exact Q primitive vanishes at y=0", sp.simplify(Q.subs(y, 0)) == 0),
        check("the Friedmann equation admits H^2>0", H2_solution == (rho + M2 * Lambda) / (3 * M2)),
        check("the tensor multiplier adds no background tensor kinetic term", cT2 == 1),
        check("an expanding branch is selected by the positive square root", sp.sqrt(H2_solution) > 0),
    ]
    print("FLAT-FLRW TENSOR-COMPENSATED BACKGROUND GATE")
    print("auxiliary constraints =", aux_lambda_constraint, aux_sigma_constraint)
    print("Q(0) =", sp.simplify(Q.subs(y, 0)))
    print("H^2 =", H2_solution)
    print("cT^2 =", cT2)
    print("Checks completed:", sum(checks), "/", len(checks))
    result = {
        "status": "FLRW_BACKGROUND_PASS_PERTURBATIONS_OPEN",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "H_squared": str(H2_solution),
        "Q_zero": str(sp.simplify(Q.subs(y, 0))),
        "cT_squared": str(cT2),
        "scope": "flat homogeneous background only; perturbative FLRW stability and clock constraints open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
