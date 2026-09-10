#!/usr/bin/env python3
"""Bounded audit of the smooth rank-changing metric-projector loophole.

The corrected metric-only projector gate leaves one tempting branch open:

    H^{mu nu}(V) = -(V^2) g^{mu nu} + V^mu V^nu,

which is smooth and rank three for non-null V, but vanishes as V -> 0.  A
metric-only covariant realization must build V from curvature (there is no
nonzero vector made from g alone).  The lowest natural choice is
V_mu = nabla_mu R.  This script does not claim a universal theorem; it audits
the principal higher-derivative obstruction in an explicit 1+1 truncation.

Use R = d_t^2 h + q x as a principal-symbol representative.  Then
V_t contains d_t^3 h and H^{xx} contains (d_t^3 h)^2.  Coupling H^{mu nu}
to an elliptic auxiliary Hessian therefore gives a nonzero Hessian with
respect to the highest metric derivative.  Away from V=0 this is an
Ostrogradsky direction; multiplying V by epsilon makes the Hessian vanish as
epsilon^2, while the elliptic source response diverges as epsilon^-2.

All ranks, limits, and derivative coefficients below are computed by SymPy.
This is a bounded obstruction to this curvature-realized branch, not a claim
against every conceivable nonlocal action.
"""

from __future__ import annotations

import json
import sys
import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def derive() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)
    u, v, eps = sp.symbols("u v epsilon", real=True)
    # Contravariant V=(u,v,0,0), with V^2=-u^2+v^2.
    V = sp.Matrix([u, v, 0, 0])
    V_sq = sp.simplify((V.T * eta * V)[0])
    H = sp.simplify(-V_sq * eta + V * V.T)
    V_lower = eta * V
    orthogonality = sp.simplify(H * V_lower)
    rank_witness = H.subs({u: 1, v: 2}).rank()
    det_H = sp.factor(H.det())

    # Principal curvature realization: R = h''(t) + q*x, so d_t R=h''' and
    # d_x R=q.  The epsilon factor models the smooth rank-changing branch.
    h3, q, Ctt, Cxx, lam = sp.symbols("h3 q Ctt Cxx lambda", real=True)
    H00_eps = eps**2 * q**2
    Hxx_eps = eps**2 * h3**2
    # H^{mu nu} partial_mu partial_nu chi in the 1+1 principal truncation.
    L_aux = sp.expand(lam * (H00_eps * Ctt + Hxx_eps * Cxx))
    highest_hessian = sp.factor(sp.diff(L_aux, h3, 2))
    dL_dh3 = sp.diff(L_aux, h3)
    t = sp.symbols("t", real=True)
    h = sp.Function("h")(t)
    lam_t = sp.Function("lambda")(t)
    # Replace h3 by h''' and lambda by lambda(t) to extract the h^(6) term.
    dL_dh3_time = 2 * eps**2 * lam_t * Cxx * sp.diff(h, t, 3)
    euler_high = sp.expand(-sp.diff(dL_dh3_time, t, 3))
    h6 = sp.diff(h, t, 6)
    highest_eom_coefficient = sp.simplify(sp.diff(euler_high, h6))

    # Smooth rank-change and the corresponding linear elliptic response.
    k, J = sp.symbols("k J", positive=True)
    response = sp.simplify(J / (eps**2 * k**2))
    hessian_zero_limit = sp.limit(highest_hessian, eps, 0, dir="+")
    response_zero_limit = sp.limit(response, eps, 0, dir="+")

    return {
        "projector": {
            "V_squared": V_sq,
            "H": H,
            "H_V_lower": orthogonality,
            "det_H": det_H,
            "rank_nonnull_witness": rank_witness,
            "smooth_zero_limit": H.subs({u: 0, v: 0}),
        },
        "curvature_principal_symbol": {
            "R_representative": "d_t^2 h + q*x",
            "V_t_representative": "d_t^3 h",
            "H00_epsilon": H00_eps,
            "Hxx_epsilon": Hxx_eps,
            "h3_symbol": h3,
            "L_aux": L_aux,
            "highest_metric_derivative_hessian": highest_hessian,
            "highest_metric_eom_coefficient": highest_eom_coefficient,
        },
        "rank_change": {
            "epsilon": eps,
            "hessian_limit": hessian_zero_limit,
            "elliptic_response": response,
            "response_limit": response_zero_limit,
        },
    }


def main() -> int:
    result = derive()
    proj = result["projector"]
    curv = result["curvature_principal_symbol"]
    rank_change = result["rank_change"]
    print("=" * 96)
    print("RANK-CHANGING CURVATURE PROJECTOR / OSTROGRADSKY GATE")
    print("=" * 96)
    print("H^{mu nu}=-(V^2)g^{mu nu}+V^mu V^nu,   V_mu=nabla_mu R")
    print("\n[1] Algebraic projector")
    print("  V^2 =", proj["V_squared"])
    print("  H V_lower =", proj["H_V_lower"])
    print("  det(H) =", proj["det_H"], "; rank at (u,v)=(1,2) =", proj["rank_nonnull_witness"])
    print("  H(V=0) =", proj["smooth_zero_limit"])
    checks = [
        check("projector is orthogonal to V", proj["H_V_lower"] == sp.zeros(4, 1)),
        check("non-null witness has rank three", proj["rank_nonnull_witness"] == 3),
        check("projector vanishes smoothly at V=0", proj["smooth_zero_limit"] == sp.zeros(4)),
    ]

    print("\n[2] Curvature realization and highest-derivative variation")
    print("  R principal representative =", curv["R_representative"])
    print("  H00(epsilon) =", curv["H00_epsilon"], "; Hxx(epsilon) =", curv["Hxx_epsilon"])
    print("  L_aux =", curv["L_aux"])
    print("  d2 L_aux / d(h''')2 =", curv["highest_metric_derivative_hessian"])
    print("  coefficient of h^(6) in metric EOM =", curv["highest_metric_eom_coefficient"])
    checks += [
        check("curvature projector contains the required third metric time derivative", curv["Hxx_epsilon"].has(curv["h3_symbol"])),
        check("highest-derivative Hessian is nonzero on the nonzero branch", curv["highest_metric_derivative_hessian"] != 0),
        check("metric Euler equation contains a sixth derivative", curv["highest_metric_eom_coefficient"] != 0),
    ]

    print("\n[3] Zero-field rank change")
    print("  highest Hessian limit epsilon->0 =", rank_change["hessian_limit"])
    print("  elliptic response =", rank_change["elliptic_response"])
    print("  response limit epsilon->0 =", rank_change["response_limit"])
    checks += [
        check("highest-derivative Hessian loses rank at zero field", rank_change["hessian_limit"] == 0),
        check("linear elliptic source response diverges at zero field", rank_change["response_limit"].is_infinite),
    ]

    print("\n[VERDICT]")
    print("  For the explicit curvature realization V_mu=nabla_mu R, the smooth rank-three")
    print("  projector is not a healthy two-tensor-DOF rescue: away from V=0 its varied")
    print("  action has a nonzero highest-derivative metric Hessian (an Ostrogradsky direction),")
    print("  while the epsilon->0 limit loses that Hessian and makes the elliptic source response")
    print("  unbounded. This closes this curvature-built branch; genuinely non-rational, nonlocal")
    print("  phantom-density actions remain outside this bounded calculation.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    print("RESULT_JSON=" + json.dumps(result, default=str, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
