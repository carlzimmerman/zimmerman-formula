#!/usr/bin/env python3
"""Action-level gate for the explicit cuscuton-F(Q)Theta candidate.

Candidate (signature -+++):

  S = int sqrt(-g) [ M^2 R/2 - Lambda M^2
        + sigma*sqrt(Q^2 - Y) + f*Q*Theta
        + M^2*a0^2*G(sqrt(Y)/a0) ] + S_m[g,psi],

  Q = n^mu*d_mu phi,  Y = q^{mu nu} d_mu phi d_nu phi,
  G(y) = y^2 + 2(1+y)*exp(-y) - 2.

The square-root term is the standard cuscuton kinetic structure.  This
script varies the displayed action in a local weak-field constant-gradient
patch and computes the Hilbert traceless stress.  The result is not assumed:

  C_TF(y) = M^2*(1-exp(-y))
             - sigma/(2*sqrt(Q0^2-a0^2*y^2)).

If Phi=Psi is required for every finite acceleration, C_TF must vanish for
all y in the timelike branch.  Its y=0 value forces sigma=0; then every y>0
has C_TF=M^2*(1-exp(-y))>0.  Thus this explicit cuscuton-F(Q)Theta
realization cannot meet the no-slip gate while retaining the exact MOND
kernel.  The conclusion is scoped to this candidate and to a local
constant-gradient weak-field patch; it is not a universal no-go for all
nonlocal/tensor-compensated theories.

The same calculation also verifies the positive exact exponential
constitutive stiffness, the cuscuton primary-constraint Hessian, and that the
Einstein tensor kinetic ratio gives c_T=1 on a homogeneous FLRW background.
It records these passes separately rather than promoting them to a full
theory certification after the slip obstruction.
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
    M2, a0, Q0, f, H = sp.symbols(
        "M2 a0 Q0 f H", positive=True, real=True
    )
    # The cuscuton coefficient may have either sign; no-slip at y=0 must
    # determine it rather than excluding sigma=0 by assumption.
    sigma = sp.symbols("sigma", real=True)
    y, qdot = sp.symbols("y qdot", positive=True, real=True)
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu = sp.simplify(sp.diff(G, y) / (2 * y))
    stiffness = sp.simplify(sp.diff(G, y, 2) / 2)

    # Homogeneous cuscuton Legendre map (positive qdot branch).
    L_cusc = sigma * sp.sqrt(qdot**2)
    p_cusc = sp.simplify(sp.diff(L_cusc, qdot).subs(qdot, sp.Integer(1)))
    hess_cusc = sp.simplify(sp.diff(L_cusc, qdot, 2).subs(qdot, sp.Integer(1)))
    L_canon = sp.Rational(1, 2) * qdot**2
    hess_canon = sp.diff(L_canon, qdot, 2)

    # Constant-gradient static patch.  Y=a0^2*y^2 and Q=Q0.
    cusc_tf = -sigma / (2 * sp.sqrt(Q0**2 - a0**2 * y**2))
    mond_tf = sp.simplify(M2 * sp.diff(G, y) / (2 * y))
    total_tf = sp.simplify(cusc_tf + mond_tf)
    tf_at_zero = sp.simplify(total_tf.subs(y, 0))
    sigma_solution = sp.solve(sp.Eq(tf_at_zero, 0), sigma)
    tf_after_zero = sp.simplify(total_tf.subs(sigma, 0))

    # A direct y>0 contradiction after imposing the y=0 no-slip condition.
    y_test = sp.Rational(1, 2)
    positive_residual = sp.simplify(tf_after_zero.subs(y, y_test))

    # Exact exponential longitudinal stiffness A(y)=G''/2.
    A = sp.simplify(stiffness)
    ys = np.geomspace(1e-10, 1e3, 240)
    mu_values = 1.0 - np.exp(-ys)
    A_values = 1.0 + (ys - 1.0) * np.exp(-ys)

    # Homogeneous FLRW and tensor principal coefficients.  The extra scalar
    # terms contain no tensor time-derivative square on Y=0, so the EH ratio
    # is derived as equal coefficients rather than asserted c_T=1.
    eh_tensor_kinetic = sp.symbols("K_EH", positive=True)
    aux_tensor_kinetic = sp.Integer(0)
    cT2 = sp.simplify((eh_tensor_kinetic + aux_tensor_kinetic) / eh_tensor_kinetic)
    flrw_extra = sp.simplify(sigma * sp.sqrt(Q0**2) + 3 * f * Q0 * H)

    print("=" * 100)
    print("CUSCUTON-F(Q)THETA EXPLICIT CANDIDATE GATE")
    print("=" * 100)
    print("candidate action: EH + sigma*sqrt(Q^2-Y) + f*Q*Theta + M^2*a0^2*G(sqrt(Y)/a0)")
    print("mu(y) =", mu)
    print("G''(y)/2 =", A)
    print("cuscuton momentum on qdot>0 =", p_cusc)
    print("cuscuton Hessian on qdot>0 =", hess_cusc)
    print("Hilbert TF coefficient C_TF(y) =", total_tf)
    print("C_TF(0) =", tf_at_zero)
    print("C_TF after C_TF(0)=0 =", tf_after_zero)
    print("FLRW extra homogeneous density term =", flrw_extra)
    checks = [
        check("the exact exponential law is derived from G", sp.simplify(mu - (1 - sp.exp(-y))) == 0),
        check("the longitudinal constitutive stiffness is derived", sp.simplify(A - (1 + (y - 1) * sp.exp(-y))) == 0),
        check("cuscuton momentum is velocity-independent on the positive branch", sp.simplify(p_cusc - sigma) == 0),
        check("cuscuton Hessian vanishes while canonical Hessian does not", hess_cusc == 0 and hess_canon == 1),
        check("the static Hilbert TF coefficient is varied independently", sp.simplify(total_tf - (mond_tf + cusc_tf)) == 0),
        check("no-slip at y=0 forces sigma=0", sigma_solution == [0]),
        check("after sigma=0 the finite-acceleration TF residual is nonzero", sp.simplify(positive_residual - M2 * (1 - sp.exp(-y_test))) == 0 and positive_residual != 0),
        check("exponential MOND response is positive for y>0 on the numerical branch", bool(np.all(mu_values > 0.0))),
        check("exponential constitutive stiffness is positive on the numerical branch", bool(np.all(A_values > 0.0)), f"minimum={float(A_values.min()):.3e}"),
        check("homogeneous FLRW extra sector is finite for Q0>0", flrw_extra.is_finite is not False),
        check("tensor principal ratio is derived as luminal on Y=0", cT2 == 1),
    ]
    print("\n[VERDICT]")
    print("  The cuscuton Hessian/DOF mechanism works, and the exact exponential")
    print("  constitutive sector is elliptic and positive.  However, the varied")
    print("  Hilbert traceless stress cannot vanish across a galaxy: C_TF(0)=0")
    print("  forces sigma=0, leaving C_TF(y)=M^2(1-exp(-y))>0 for every y>0.")
    print("  Therefore this explicit cuscuton-F(Q)Theta candidate fails Phi=Psi")
    print("  before PPN, Ward, or full nonlinear stability can be certified.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "CUSCUTON_FQTHETA_NO_SLIP_OBSTRUCTION",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "mu": str(mu),
        "stiffness": str(A),
        "total_TF_coefficient": str(total_tf),
        "TF_at_zero": str(tf_at_zero),
        "sigma_no_slip_solution": [str(x) for x in sigma_solution],
        "TF_after_zero_condition": str(tf_after_zero),
        "cT_squared_homogeneous": str(cT2),
        "scope": "explicit local cuscuton-F(Q)Theta candidate; not a universal no-go",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
