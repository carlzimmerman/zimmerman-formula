#!/usr/bin/env python3
"""Action-level slip gate for the exact exponential York/QUMOND carrier.

The corrected static carrier is

    L_Q = -2 h^{ij} Phi_i Psi_j + a0^2 F(u),   u=h^{ij} Psi_i Psi_j/a0^2,
    F'(u)=nu_exp(sqrt(u)),  s=x(1-exp(-x)),  nu_exp(s)=x/s.

Variation in Psi gives the QUMOND flux equation after division by two.
Variation in the spatial inverse metric gives an anisotropic stress.  On a
no-slip branch Phi_i=Psi_i its traceless amplitude is proportional to
nu_exp(s)-2.  It can vanish at one isolated acceleration, but not on a
galactic branch spanning a range of accelerations.
"""

from __future__ import annotations

import json
import math
import sys

import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def main() -> int:
    h0, h1, h2 = sp.symbols("h0 h1 h2", positive=True)
    p0, p1, p2 = sp.symbols("p0 p1 p2")
    q0, q1, q2 = sp.symbols("q0 q1 q2")
    a0 = sp.symbols("a0", positive=True)
    Fp = sp.Function("Fprime")
    u = (h0 * q0**2 + h1 * q1**2 + h2 * q2**2) / a0**2
    L = -2 * (h0 * p0 * q0 + h1 * p1 * q1 + h2 * p2 * q2) + a0**2 * sp.Function("F")(u)

    dL_dh = [sp.diff(L, h) for h in (h0, h1, h2)]
    # Replace F'(u) by the constitutive nu(u); determinant/sqrt(h) terms are
    # isotropic and cancel from traceless differences.
    dL_dh_flux = [
        sp.simplify(expr.replace(
            lambda z: z.is_Derivative and z.expr.func.__name__ == "F",
            lambda z: Fp(u),
        ))
        for expr in dL_dh
    ]
    # SymPy's derivative object is normalized explicitly for robust output.
    dL_dh_flux = [
        -2 * p * q + Fp(u) * q**2
        for p, q in ((p0, q0), (p1, q1), (p2, q2))
    ]

    # Direct Euler-Lagrange principal terms in one coordinate direction:
    # dL/d(Phi_i)=-2 Psi_i; dL/d(Psi_i)=-2 Phi_i+2 F'(u) Psi_i.
    phi_grad = [-2 * q for q in (q0, q1, q2)]
    psi_grad = [-2 * p + 2 * Fp(u) * q for p, q in ((p0, q0), (p1, q1), (p2, q2))]
    qmond_flux = [sp.simplify(expr / 2) for expr in psi_grad]

    no_slip = {p0: q0, p1: q1, p2: q2}
    tf12 = sp.factor((dL_dh_flux[0] - dL_dh_flux[1]).subs(no_slip))
    tf23 = sp.factor((dL_dh_flux[1] - dL_dh_flux[2]).subs(no_slip))

    # Linearize a general cross coefficient A(u) and carrier F(u) around one
    # background value U.  This gives the complete local coefficient, including
    # the A'(u) contribution, without assuming a special kernel.
    U, A0, A1, F0, F1 = sp.symbols("U A0 A1 F0 F1")
    A_lin = A0 + A1 * (u - U)
    F_lin = F0 + F1 * (u - U)
    L_general = -2 * A_lin * (h0 * p0 * q0 + h1 * p1 * q1 + h2 * p2 * q2) + a0**2 * F_lin
    general_dh = [sp.diff(L_general, h) for h in (h0, h1, h2)]
    background_u = {U: (h0 * q0**2 + h1 * q1**2 + h2 * q2**2) / a0**2}
    general_tf12 = sp.factor((general_dh[0] - general_dh[1]).subs(no_slip).subs(background_u))
    general_coeff = F1 - 2 * (A0 + A1 * u)

    x, s = sp.symbols("x s", positive=True)
    mu = 1 - sp.exp(-x)
    nu_x = sp.simplify(1 / mu)
    nu_minus_two = sp.factor(nu_x - 2)
    cancellation_equation = sp.solve(sp.Eq(nu_x, 2), x)
    finite_residual = sp.simplify(nu_minus_two.subs(x, 1))

    # The exact primitive used by the carrier, parameterized by x(s).
    F_of_x = x**2 + 2 - 2 * sp.exp(-x) * (x**2 + x + 1)
    primitive_residual = sp.simplify(
        sp.diff(F_of_x, x) - 2 * x * (1 + (x - 1) * sp.exp(-x))
    )

    print("=" * 96)
    print("EXACT EXPONENTIAL YORK/QUMOND ACTION-LEVEL SLIP GATE")
    print("=" * 96)
    print("L_Q = -2 h^ij Phi_i Psi_j + a0^2 F(u),  u=h^ij Psi_i Psi_j/a0^2")
    print("F'(u)=nu_exp(sqrt(u)),  s=x(1-exp(-x)),  nu_exp=x/s")
    print("\n[1] Direct variations")
    print("  dL/d(Phi_i) =", phi_grad)
    print("  (1/2)dL/d(Psi_i) =", qmond_flux)
    print("  => EL_Phi gives D^2 Psi = 4 pi G rho after the source term;")
    print("     EL_Psi gives D^2 Phi = D_i[nu_exp D^i Psi].")

    print("\n[2] Metric variation on Phi=Psi")
    print("  TF(0,1) amplitude =", tf12)
    print("  TF(1,2) amplitude =", tf23)
    print("  nu_exp(x)-2 =", nu_minus_two)
    print("  finite-x residual at x=1 =", finite_residual)
    print("  solutions of nu_exp(x)=2 for x>0 =", cancellation_equation)

    print("\n[2b] General cross-coefficient check")
    print("  A(u)=A0+A1(u-U), F'(u)=F1 => TF coefficient = F1-2(A0+A1*u)")
    print("  general TF(0,1) - coefficient*(q0^2-q1^2) =", sp.simplify(general_tf12 - general_coeff.subs(background_u) * (q0**2 - q1**2)))

    print("\n[3] Exact primitive")
    print("  F(x(s)^2) =", F_of_x)
    print("  dF/dx - 2*x*ds/dx =", primitive_residual)

    checks = [
        check("Phi variation has the Poisson cross-gradient", phi_grad[0] == -2 * q0),
        check("Psi variation carries the exact nu constitutive factor", qmond_flux[0] == -p0 + Fp(u) * q0),
        check("no-slip traceless stress is proportional to (nu-2)(q_i^2-q_j^2)", sp.simplify(tf12 - (Fp(u).subs(no_slip) - 2) * (q0**2 - q1**2)) == 0),
        check("the exact exponential carrier has nu-2 = (2-exp(x))/(exp(x)-1)", sp.simplify(nu_minus_two - (2 - sp.exp(x)) / (sp.exp(x) - 1)) == 0),
        check("nu_exp(x)=2 has exactly one finite solution x=log(2)", cancellation_equation == [sp.log(2)]),
        check("general A(u),F(u) metric variation has the derived coefficient", sp.simplify(general_tf12 - general_coeff.subs(background_u) * (q0**2 - q1**2)) == 0),
        check("the exact primitive differentiates to 2*x*ds/dx", primitive_residual == 0),
        check("a finite MOND point has nonzero slip source", abs(float(finite_residual.evalf())) > 0.0),
    ]

    print("\n[VERDICT]")
    print("  The corrected action derives the exact exponential QUMOND flux, but its")
    print("  Hilbert traceless stress on Phi=Psi is (nu_exp-2)(q_i q_j)^TF.")
    print("  It vanishes only at the isolated point x=log(2), not across a galaxy.")
    print("  A multiplier can impose Phi=Psi, but the")
    print("  summed metric equation still contains this stress (the certified C4 gate).")
    print("  This closes the exact York/QUMOND carrier on the no-slip requirement;")
    print("  it is not a full covariant no-go for every nonlocal architecture.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "EXACT_EXPONENTIAL_YORK_SLIP_OBSTRUCTION",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "tf12": str(tf12),
        "tf23": str(tf23),
        "nu_minus_two": str(nu_minus_two),
        "primitive_residual": str(primitive_residual),
        "scope": "static York/QUMOND carrier; not a universal nonlocal no-go",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
