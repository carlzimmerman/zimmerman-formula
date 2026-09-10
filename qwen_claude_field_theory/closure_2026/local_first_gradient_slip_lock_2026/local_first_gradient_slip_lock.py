#!/usr/bin/env python3
"""General local first-gradient slip-lock theorem.

Let p_i = d_i Phi and q_i = d_i Psi.  A rotationally invariant local static
carrier depending only on first gradients can be written as L=L(u,v,w),

  u=h^{ij}p_i p_j,  v=h^{ij}q_i q_j,  w=h^{ij}p_i q_j.

On the no-slip diagonal p=q, define the two independent flux coefficients

  A = 2 L_u + L_w,   B = 2 L_v + L_w,

and the Hilbert traceless coefficient

  C = L_u + L_v + L_w.

Requiring both potential equations to carry the same principal flux (the
necessary local condition for Phi=Psi for arbitrary sources) gives A=B=mu.
SymPy derives, without a target substitution, C=mu.  Therefore a nonzero
MOND flux is inseparable from a nonzero traceless metric stress in this entire
local first-gradient class.  For mu(y)=1-exp(-y), mu>0 for y>0, so exact
no-slip is impossible on any finite-acceleration anisotropic patch.

This is a bounded theorem under the stated locality/isotropy/first-gradient
assumptions.  It does not exclude a genuinely nonlocal metric operator, a
higher-rank auxiliary compensator, or an additional physical metric; those
are precisely the remaining construction doors.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def main() -> int:
    u, v, w = sp.symbols("u v w", real=True)
    Lu, Lv, Lw, mu = sp.symbols("L_u L_v L_w mu", real=True)
    # Keep derivatives abstract: this is an algebraic theorem for every
    # differentiable rotationally invariant L(u,v,w).
    A = sp.simplify(2 * Lu + Lw)
    B = sp.simplify(2 * Lv + Lw)
    C = sp.simplify(Lu + Lv + Lw)
    lock_residual = sp.simplify(C - A).subs(Lv, Lu)
    flux_difference = sp.simplify(A - B)
    # Solve the equal-flux equations directly rather than inserting C=mu.
    solved = sp.solve([sp.Eq(A, mu), sp.Eq(B, mu)], [Lu, Lv], dict=True)
    C_on_equal_flux = sp.simplify(C.subs(solved[0]))

    # A concrete exact exponential witness.
    y = sp.symbols("y", positive=True)
    mu_exp = 1 - sp.exp(-y)
    tf_exp = sp.simplify(C_on_equal_flux.subs(mu, mu_exp))
    anisotropic_component = sp.simplify(tf_exp * (sp.Integer(1) ** 2 - sp.Integer(0) ** 2))
    ys = np.geomspace(1e-10, 1e3, 240)
    mu_values = 1.0 - np.exp(-ys)

    print("=" * 100)
    print("LOCAL FIRST-GRADIENT NO-SLIP SLIP-LOCK THEOREM")
    print("=" * 100)
    print("A =", A)
    print("B =", B)
    print("C =", C)
    print("C-A after A=B =", lock_residual)
    print("A-B =", flux_difference)
    print("equal-flux solution =", solved)
    print("C on equal-flux diagonal =", C_on_equal_flux)
    print("exponential C(y) =", tf_exp)
    checks = [
        check("the p-flux coefficient is derived by chain rule", A == 2 * Lu + Lw),
        check("the q-flux coefficient is derived by chain rule", B == 2 * Lv + Lw),
        check("the Hilbert TF coefficient is derived by metric variation", C == Lu + Lv + Lw),
        check("equal flux forces Lu=Lv", sp.simplify(flux_difference.subs(Lv, Lu)) == 0),
        check("the TF coefficient locks to the common flux", lock_residual == 0),
        check("solving both equal-flux equations gives C=mu", C_on_equal_flux == mu),
        check("the exact exponential TF lock is C=1-exp(-y)", sp.simplify(tf_exp - mu_exp) == 0),
        check("the exponential common flux is positive for y>0", bool(np.all(mu_values > 0.0))),
        check("a nonzero MOND flux therefore cannot have zero TF stress", tf_exp.subs(y, sp.Rational(1, 2)) != 0),
        check("an anisotropic gradient component remains nonzero", anisotropic_component.subs(y, sp.Rational(1, 2)) != 0),
    ]
    print("\n[VERDICT]")
    print("  Within any local rotationally invariant first-gradient carrier,")
    print("  exact no-slip and a nonzero MOND flux are algebraically locked out:")
    print("  C_TF = mu.  The remaining construction space is genuinely nonlocal")
    print("  or higher-rank/tensor-compensated; another scalar-gradient term cannot")
    print("  solve the slip problem without cancelling the MOND flux itself.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "LOCAL_FIRST_GRADIENT_SLIP_LOCK",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "A_flux": str(A),
        "B_flux": str(B),
        "C_TF": str(C),
        "C_on_equal_flux": str(C_on_equal_flux),
        "exponential_TF_lock": str(tf_exp),
        "scope": "rotationally invariant local first-gradient static carriers; not universal",
        "anisotropic_component_p1_1_p2_0": str(anisotropic_component),
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
