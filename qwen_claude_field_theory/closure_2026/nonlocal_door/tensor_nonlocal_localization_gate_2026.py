#!/usr/bin/env python3
"""Canonical gate for tensorial causal nonlocality in a single-copy action.

To evade the scalar-curvature slip source, a nonlinear covariant candidate can
try to use a tensor response U_mn=L_ret^{-1}G_mn.  The standard local action
representation is

  S_loc = S_EH + int sqrt(-g) [ Lambda^mn (L U_mn - G_mn) + V(g,U) ].

For the hyperbolic principal part L=Box, integration by parts yields
-nabla Lambda.nabla U.  On any TT component (for example U_12), neither U nor
Lambda has a scalar gauge redundancy.  The velocity Hessian is necessarily

  K = [[a, b], [b, 0]],  b != 0,

where V may change a but cannot give the multiplier Lambda a self-kinetic term.
Its determinant is -b^2, so the localized single-copy action has one negative
kinetic direction.  Retarded data do not create a Dirac constraint: two sources
with identical data in a neighbourhood of the Cauchy slice can have different
retarded U data because their earlier histories differ.

Scope: this closes finite/rational tensor localizations of a conventional
single-copy action.  A non-rational kernel needs a continuum of such response
pairs; a doubled CTP canonical construction would require its own explicit
second-class reduction and is not claimed closed here.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_tensor_localization_gate() -> dict[str, Any]:
    """Derive the TT kinetic signature and an exact history-dependence witness."""

    a = sp.symbols("a", real=True)
    b = sp.symbols("b", positive=True)
    udot, ldot = sp.symbols("Udot Lambda_dot", real=True)
    velocities = sp.Matrix([udot, ldot])
    velocity_lagrangian = sp.Rational(1, 2) * a * udot**2 + b * udot * ldot
    hessian = sp.hessian(velocity_lagrangian, velocities)
    determinant = sp.factor(hessian.det())
    eigenvalues = list(hessian.eigenvals().keys())
    eigenvalue_product = sp.simplify(sp.prod(eigenvalues))
    primary_nullity = len(hessian.nullspace())

    # Exact retarded witness in the k=0 TT component: U_ddot=-J.  J1=0 and
    # J2 is a polynomial bump supported only on [-4,-3]; therefore their full
    # germs at t=0 are identically equal, while retarded data differ exactly.
    t = sp.symbols("t", real=True)
    bump = (t + 4) ** 2 * (t + 3) ** 2
    u0_difference = sp.simplify(sp.integrate(t * bump, (t, -4, -3)))
    udot0_difference = sp.simplify(-sp.integrate(bump, (t, -4, -3)))
    same_jet_different_history = bool(u0_difference != 0 and udot0_difference != 0)

    return {
        "localized_action": {
            "principal_form": "Lambda^mn(Box U_mn-G_mn) -> -nabla Lambda^mn . nabla U_mn",
            "tt_component": "U_12, Lambda_12",
        },
        "kinetic": {
            "velocity_lagrangian": velocity_lagrangian,
            "hessian": hessian,
            "determinant": determinant,
            "eigenvalues": eigenvalues,
            "eigenvalue_product": eigenvalue_product,
            "primary_nullity": primary_nullity,
        },
        "retarded": {
            "u0_difference": u0_difference,
            "udot0_difference": udot0_difference,
            "same_jet_different_history": same_jet_different_history,
            "is_dirac_constraint": False,
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_tensor_localization_gate()
    localized = result["localized_action"]
    kinetic = result["kinetic"]
    retarded = result["retarded"]

    print("=" * 92)
    print("TENSOR NONLOCAL LOCALIZATION GATE: TT KINETIC SIGNATURE AND RETARDED DATA")
    print("=" * 92)
    print("\n[1] Localized tensor action")
    print(f"  Principal form: {localized['principal_form']}")
    print(f"  Gauge-independent test component: {localized['tt_component']}")
    print(f"  TT velocity Lagrangian = {kinetic['velocity_lagrangian']}")
    print(f"  Hessian = {kinetic['hessian']}")
    print(f"  det(K) = {kinetic['determinant']}")
    print(f"  eigenvalues = {kinetic['eigenvalues']}")
    print(f"  eigenvalue product = {kinetic['eigenvalue_product']}")
    print(f"  Hessian nullity / primary constraints in the TT pair = {kinetic['primary_nullity']}")

    checks = [
        _check("the tensor response-multiplier block is nondegenerate", kinetic["determinant"] != 0 and kinetic["primary_nullity"] == 0),
        _check("the TT pair has opposite-sign kinetic eigenvalues for every b!=0", kinetic["eigenvalue_product"] < 0),
    ]

    print("\n[2] Retarded data are history conditions, not Dirac constraints")
    print("  J1=0 and J2=(t+4)^2(t+3)^2 on [-4,-3], both exactly zero near t=0.")
    print(f"  Delta U_ret(0) = int t J2 dt = {retarded['u0_difference']}")
    print(f"  Delta Udot_ret(0) = -int J2 dt = {retarded['udot0_difference']}")
    print(f"  Same Cauchy germ, different retarded data: {retarded['same_jet_different_history']}")
    print(f"  Retarded condition is a Dirac constraint on one slice: {retarded['is_dirac_constraint']}")
    checks.append(_check("retarded boundary data cannot remove this TT pair by a one-slice Dirac constraint", retarded["same_jet_different_history"] and not retarded["is_dirac_constraint"]))

    print("\n[VERDICT]")
    print("  DEAD for a finite/rational tensor localization in a conventional single-copy action:")
    print("  it contains a TT response-multiplier ghost, and retarded data do not canonically remove it.")
    print("  Residual OPEN route: a genuinely non-rational tensor kernel with an explicitly demonstrated")
    print("  doubled-CTP second-class phase-space reduction.  No such construction is supplied here.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
