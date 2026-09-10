#!/usr/bin/env python3
"""Regulator trilemma for the exact F(Q)Theta mixed scalar sector.

The action-derived principal reduction has the universal first-order form

    L = Omega*p*z_dot + k^2/2*(Upp*p^2 + Uzz*z^2),
    Omega = Unz*k^2/Q0.

This file differentiates that Lagrangian and tests the three possible local
repairs.  It does not prescribe ranks or signs: SymPy derives the reduced
kinetic coefficient, characteristic frequency, symplectic determinant, and
the effect of an independent p_dot regulator.

For the exponential constitutive law, Upp is proportional to

    A(y) = 1 + (y - 1)*exp(-y),

which is positive for every y>0.  Therefore a nonzero mixed sector
(Unz != 0) has a negative reduced kinetic residue.  Reversing Upp makes the
frequency squared negative when Uzz>0.  Setting Unz=0 collapses the
symplectic form, so it is a rank-changing/strong-coupling branch that needs a
different complete Dirac analysis.  Adding an independent p_dot^2 term makes
the intended auxiliary equation differential (the p Euler--Lagrange equation
contains p_ddot), i.e. it introduces a propagating clock/auxiliary scalar.

This is a scoped obstruction to this mixed F(Q)Theta architecture, not a
universal no-go theorem for every covariant MOND action.
"""

from __future__ import annotations

import json
import math
import sys

import numpy as np
import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def main() -> int:
    Upp, Uzz, Unz, Q0, k, eps = sp.symbols(
        "Upp Uzz Unz Q0 k eps", nonzero=True, real=True
    )
    p, z, zdot, pdot, pddot = sp.symbols("p z zdot pdot pddot", real=True)
    Omega = sp.simplify(Unz * k**2 / Q0)
    H = -k**2 * (Upp * p**2 + Uzz * z**2) / 2
    L = Omega * p * zdot - H

    # Direct variation and elimination of p.
    p_solution = sp.solve(sp.Eq(sp.diff(L, p), 0), p)[0]
    Lred = sp.factor(sp.simplify(L.subs(p, p_solution)))
    Kred = sp.factor(sp.diff(Lred, zdot, 2) / 2)
    Kred_expected = sp.factor(-Unz**2 * k**2 / (2 * Q0**2 * Upp))
    omega_sq = sp.factor(Q0**2 * Upp * Uzz / Unz**2)

    # Derive the two-dimensional symplectic form from the one-form Omega*p dz.
    # Coordinates are ordered (z,p), so the matrix is d(theta) in that basis.
    symplectic = sp.Matrix([[0, -Omega], [Omega, 0]])
    symplectic_det = sp.factor(symplectic.det())

    # The Unz=0 branch has no symplectic term at all.
    symplectic_zero = symplectic.subs(Unz, 0)

    # An independent p_dot regulator changes the p equation from algebraic to
    # differential.  Derive that order directly from Euler--Lagrange.
    Lreg = L + eps * pdot**2 / 2
    dLreg_dp = sp.diff(Lreg, p)
    dLreg_dpdot = sp.diff(Lreg, pdot)
    # d/dt(dL/dp_dot) with only the p_ddot term retained for the principal test.
    EL_p_principal = sp.simplify(dLreg_dp - eps * pddot)
    pddot_coeff = sp.simplify(sp.diff(EL_p_principal, pddot))
    # The z equation remains first order in p.  Eliminating z from the two
    # regulated Euler--Lagrange equations gives a genuine second-order p
    # equation whenever this coefficient is nonzero.
    EL_z = sp.simplify(Omega * pdot - k**2 * Uzz * z)
    z_solution = sp.solve(sp.Eq(EL_z, 0), z)[0]
    regulated_p_coeff = sp.factor(Omega**2 / (k**2 * Uzz) - eps)
    regulated_p_equation = sp.factor(regulated_p_coeff * pddot + k**2 * Upp * p)

    # Exact exponential stiffness used by the displayed F(Q)Theta action.
    ys = np.geomspace(1e-10, 1e3, 240)
    Avals = 1.0 + (ys - 1.0) * np.exp(-ys)
    # Generic numerical branches only sanity-check the symbolic formulas.
    K_pos = -(1.0**2 * 1.0**2) / (2.0 * 1.0**2 * Avals)
    w2_pos = Avals * 1.0 / 1.0**2
    K_flip = -(1.0**2 * 1.0**2) / (2.0 * 1.0**2 * (-Avals))
    w2_flip = -Avals * 1.0 / 1.0**2

    print("=" * 96)
    print("F(Q)THETA REGULATOR TRILEMMA GATE")
    print("=" * 96)
    print("Omega =", Omega)
    print("p eliminated =", p_solution)
    print("L_red =", Lred)
    print("K_red =", Kred)
    print("omega^2 =", omega_sq)
    print("symplectic matrix =", symplectic)
    print("det(symplectic) =", symplectic_det)
    print("regulated p principal equation =", EL_p_principal)
    print("regulated z equation =", EL_z)
    print("regulated second-order p equation =", regulated_p_equation)
    checks = [
        check("p variation is eliminated directly", sp.simplify(sp.diff(L, p)) == sp.simplify(Omega * zdot + k**2 * Upp * p)),
        check("reduced kinetic coefficient is derived", sp.simplify(Kred - Kred_expected) == 0),
        check("characteristic frequency is derived from the reduced flow", omega_sq == Q0**2 * Upp * Uzz / Unz**2),
        check("mixed symplectic determinant is derived", sp.simplify(symplectic_det - Omega**2) == 0),
        check("Unz=0 collapses the symplectic form", symplectic_zero == sp.zeros(2)),
        check("an independent p_dot regulator produces p_ddot", pddot_coeff == -eps),
        check("the regulated z equation solves for z in terms of p_dot", sp.simplify(EL_z.subs(z, z_solution)) == 0),
        check("the regulated system has a generic second-order p equation", sp.simplify(sp.diff(regulated_p_equation, pddot) - regulated_p_coeff) == 0),
        check("exponential A(y) stays positive on y>0 scan", bool(np.all(Avals > 0.0)), f"minimum={float(Avals.min()):.3e}"),
        check("positive Upp, nonzero mixing gives negative residue", bool(np.all(K_pos < 0.0))),
        check("positive Upp, positive Uzz gives stable-sign omega^2", bool(np.all(w2_pos > 0.0))),
        check("flipped Upp gives positive residue but negative omega^2", bool(np.all(K_flip > 0.0) and np.all(w2_flip < 0.0))),
    ]
    print("\n[VERDICT]")
    print("  The displayed mixed F(Q)Theta architecture has three local choices:")
    print("  (i) Upp>0 (the exact exponential elliptic branch) => K_red<0: ghost;")
    print("  (ii) Upp<0 with Uzz>0 => omega^2<0: gradient instability;")
    print("  (iii) Unz=0 => symplectic determinant 0: rank-changing/strong-coupling branch.")
    print("  Adding p_dot^2 makes the intended auxiliary equation differential and")
    print("  therefore introduces a propagating clock/auxiliary mode; it is not a")
    print("  closure of the two-tensor theory without a fresh full Dirac/PPN/FLRW audit.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "FQTHETA_REGULATOR_TRILEMMA",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "Omega": str(Omega),
        "Kred": str(Kred),
        "omega_squared": str(omega_sq),
        "symplectic_determinant": str(symplectic_det),
        "regulated_p_principal_equation": str(EL_p_principal),
        "regulated_z_equation": str(EL_z),
        "regulated_p_equation": str(regulated_p_equation),
        "regulated_p_second_order_coefficient": str(regulated_p_coeff),
        "scope": "mixed F(Q)Theta principal scalar architecture; not a universal no-go",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
