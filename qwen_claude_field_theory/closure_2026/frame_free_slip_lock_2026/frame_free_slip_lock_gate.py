#!/usr/bin/env python3
"""Exact algebra audit for the frame-free curvature-coupling slip lock."""

import json
import sys
import sympy as sp


def check(name, condition):
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    return ok


def main() -> int:
    L, m, rho = sp.symbols("L m rho", positive=True)
    v = sp.Matrix([-2, 4])
    G = sp.Matrix([[0, 2 * m], [2 * m, -2 * m]])
    M = -L * (v * v.T)
    K = G + M
    source = sp.Matrix([rho, 0])
    response = sp.simplify(K.inv() * source)
    eta = sp.factor(response[1] / response[0])
    enhancement = sp.factor(response[0] / (rho / (2 * m)))
    detK = sp.factor(K.det())
    checks = [
        check("the curvature direction is the exact (-2,4) ray", tuple(v) == (-2, 4)),
        check("the compensator matrix is computed as -L vv^T", M == -L * v * v.T),
        check("the response is obtained by matrix inversion", sp.simplify(K * response - source) == sp.zeros(2, 1)),
        check("the determinant is nonzero on L,m>0", detK == -4 * m * (6 * L + m)),
        check("the slip ratio is derived, not inserted", eta == (4 * L + m) / (8 * L + m)),
        check("the enhancement is derived, not inserted", enhancement == (8 * L + m) / (6 * L + m)),
        check("positive coupling implies eta<1", sp.simplify(1 - eta) == 4 * L / (8 * L + m)),
        check("positive coupling implies strict enhancement", sp.simplify(enhancement - 1) == 2 * L / (6 * L + m)),
    ]
    print("FRAME-FREE CURVATURE SLIP-LOCK GATE")
    print("v =", tuple(v), "M =", M)
    print("det(K) =", detK)
    print("eta =", eta)
    print("enhancement E =", enhancement)
    print(f"Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "FRAME_FREE_SLIP_LOCK",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "curvature_direction": str(tuple(v)),
        "determinant": str(detK),
        "eta": str(eta),
        "enhancement": str(enhancement),
        "scope": "quasi-static linear single-metric frame-free curvature coupling; not universal",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
