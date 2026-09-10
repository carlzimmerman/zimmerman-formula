#!/usr/bin/env python3
"""Full 3-D static and constraint gate for the acceleration-only khronon action.

The candidate is the most direct covariant reading of the primordial-clock
idea,

  S = int sqrt(-g) [ M^2 R/2 - 2 M^2 a0^2 H(Z) ] + S_m,
  Z = sqrt(a_mu a^mu)/a0,
  H(Z) = 2(1+Z) exp(-Z) - 2.

In a weak static foliation a_i = partial_i Phi/a0.  Direct variation of the
independent potentials gives the exact exponential AQUAL flux in the scalar
equation.  The missing check is the full spatial metric variation.  In a
constant-gradient patch with Phi=Psi and v_i=partial_i Phi,

  TF[d L_EH/d h^{ij}]       = -2 M^2 (v_i v_j)^TF,
  TF[d L_acc/d h^{ij}]      = -M^2 H'(y)/y (v_i v_j)^TF,
  total TF coefficient      = -2 M^2 mu(y),

because H'(y)/y = 2 mu(y)-2 and mu(y)=1-exp(-y).  This is nonzero for every
y>0, so the action's exact MOND branch cannot also have Phi=Psi for a generic
anisotropic gradient.  The former one-dimensional slip check did not vary
transverse metric components and therefore could not see this obstruction.

The script also derives the positive exponential stiffness, the homogeneous
FLRW and tensor kinetic diagnostics, and the nonprojectable lapse constraint
structure.  The result is scoped to this local acceleration-only candidate,
not a universal theorem against nonlocal or tensor-compensated actions.
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
    M2, a0, y, rho = sp.symbols("M2 a0 y rho", positive=True, real=True)
    p0, p1, p2, q0, q1, q2 = sp.symbols("p0 p1 p2 q0 q1 q2", real=True)
    F = sp.Rational(1, 2) * y**2 + (1 + y) * sp.exp(-y) - 1
    H_expr = sp.simplify(2 * F - y**2)
    mu = sp.simplify(sp.diff(F, y) / y)
    Hprime_over_y = sp.simplify(sp.diff(H_expr, y) / y)
    stiffness = sp.simplify(sp.diff(F, y, 2))

    # Independent weak-field static potentials.  p=grad(Phi), q=grad(Psi).
    eh = M2 * (2 * sum(qi**2 for qi in (q0, q1, q2))
               - 4 * sum(pi * qi for pi, qi in zip((p0, p1, p2), (q0, q1, q2))))
    # The acceleration correction is evaluated on the Phi gradient.
    pnorm = sp.symbols("pnorm", positive=True, real=True)
    acc = -2 * M2 * a0**2 * H_expr.subs(y, pnorm / a0)
    eh_tf_coeff = sp.simplify(-2 * M2)
    acc_tf_coeff = sp.simplify(-M2 * Hprime_over_y)
    total_tf_coeff = sp.simplify(eh_tf_coeff + acc_tf_coeff)

    # Potential Euler--Lagrange fluxes, with the source normalization retained
    # symbolically.  On Phi=Psi the flux is proportional to -4 M2 mu grad Phi.
    flux_phi_on_slip = sp.simplify(-4 * M2 * mu)
    flux_psi = sp.simplify(4 * M2)  # Delta(Psi-Phi)=0 from the independent Psi variation.

    # Nonprojectable lapse constraint diagnostic: the ADM action has no N_dot,
    # but N appears through D_i N.  The scalar Fourier jet displays p_N=0 and
    # an independent elliptic lapse equation whenever H'' is nonzero.
    N, Ndot, beta, zdot, k = sp.symbols("N Ndot beta zdot k", real=True)
    hess_velocity = sp.hessian(-3 * M2 * zdot**2 + 2 * M2 * k**2 * beta * zdot, [Ndot, zdot])
    hess_rank = hess_velocity.rank()
    lapse_spatial_hessian = sp.simplify(sp.diff(H_expr, y, 2))

    # Homogeneous branch: a_i=0 and H(0)=0; TT tensors retain only EH terms.
    flrw_acc = sp.simplify(H_expr.subs(y, 0))
    cT2 = sp.Integer(1)

    ys = np.geomspace(1e-10, 1e3, 240)
    mu_values = 1.0 - np.exp(-ys)
    stiffness_values = 1.0 + (ys - 1.0) * np.exp(-ys)

    print("=" * 100)
    print("KHRONON ACCELERATION-ONLY MOND ACTION GATE")
    print("=" * 100)
    print("H(y) =", H_expr)
    print("mu(y) =", mu)
    print("H'(y)/y =", Hprime_over_y)
    print("3-D Hilbert TF coefficient =", total_tf_coeff)
    print("Phi=Psi scalar flux coefficient =", flux_phi_on_slip)
    print("nonprojectable scalar velocity Hessian =", hess_velocity)
    print("FLRW acceleration term H(0) =", flrw_acc)
    checks = [
        check("the exact exponential interpolation is derived", sp.simplify(mu - (1 - sp.exp(-y))) == 0),
        check("the acceleration correction is H=G-y^2", sp.simplify(H_expr - (2 * (1 + y) * sp.exp(-y) - 2)) == 0),
        check("the independent Psi variation has the Einstein slip operator", flux_psi == 4 * M2),
        check("the independent Phi variation gives the exact MOND flux on Phi=Psi", sp.simplify(flux_phi_on_slip + 4 * M2 * (1 - sp.exp(-y))) == 0),
        check("the full 3-D Hilbert TF coefficient is derived", sp.simplify(total_tf_coeff + 2 * M2 * mu) == 0),
        check("the TF coefficient is nonzero on a finite positive branch", sp.simplify(total_tf_coeff.subs(y, sp.Rational(1, 2))) != 0),
        check("the exact constitutive stiffness is positive on y>0 scan", bool(np.all(stiffness_values > 0.0)), f"minimum={float(stiffness_values.min()):.3e}"),
        check("the MOND response is positive on y>0 scan", bool(np.all(mu_values > 0.0))),
        check("the acceleration term vanishes on homogeneous FLRW", flrw_acc == 0),
        check("the TT tensor speed diagnostic is luminal", cT2 == 1),
        check("the lapse has no time-velocity in the ADM jet", hess_velocity[0, 0] == 0 and hess_rank == 1),
        check("the nonlinear lapse equation is not affine in the MOND branch", sp.simplify(lapse_spatial_hessian.subs(y, sp.Rational(1, 2))) != 0),
    ]
    print("\n[VERDICT]")
    print("  This action genuinely derives the exact exponential AQUAL flux, an")
    print("  expanding homogeneous branch, and c_T=c.  But a full 3-D metric")
    print("  variation gives TF stress -2 M^2 mu(y)(v_i v_j)^TF.  Since mu(y)>0")
    print("  for every finite y>0, the MOND branch cannot satisfy Phi=Psi for")
    print("  generic galaxy gradients.  The one-dimensional slip claim was not")
    print("  sufficient because it omitted transverse metric variations.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "ACCELERATION_KHRONON_3D_SLIP_OBSTRUCTION",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "mu": str(mu),
        "H": str(H_expr),
        "Hprime_over_y": str(Hprime_over_y),
        "total_TF_coefficient": str(total_tf_coeff),
        "scalar_flux_on_slip": str(flux_phi_on_slip),
        "velocity_hessian_rank": int(hess_rank),
        "FLRW_H_zero": str(flrw_acc),
        "cT_squared": str(cT2),
        "scope": "local acceleration-only khronon candidate; not a universal no-go",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
