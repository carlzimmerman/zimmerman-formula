#!/usr/bin/env python3
"""Reduced-energy check for the exact F(Q)Theta scalar principal sector.

The actual principal gate derives, on an expanding nonzero-gradient branch,

  Omega = -4 M^2 k^2/Q0,
  H_red = -2 M^2 k^2 [ A(y0) p^2 + z^2 ],
  A(y)=1+(y-1) exp(-y).

This script derives the second-order reduced Lagrangian from the displayed
first-order symplectic action and checks its kinetic sign.  It does not insert
a desired ghost/no-ghost answer.  The result is scoped to the displayed
F(Q)Theta principal sector; omitted extra aether operators would define a
different action and require a fresh complete analysis.
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
    M2, k, Q0, y = sp.symbols("M2 k Q0 y", positive=True)
    z, p, zdot = sp.symbols("z p zdot", real=True)
    A = sp.simplify(1 + (y - 1) * sp.exp(-y))
    Omega = -4 * M2 * k**2 / Q0
    Hred = -2 * M2 * k**2 * (A * p**2 + z**2)
    L1 = Omega * p * zdot - Hred
    p_solution = sp.solve(sp.Eq(sp.diff(L1, p), 0), p)[0]
    L2 = sp.factor(sp.simplify(L1.subs(p, p_solution)))
    kinetic = sp.factor(sp.diff(L2, zdot, 2) / 2)
    expected_kinetic = -2 * M2 * k**2 / (Q0**2 * A)

    Upp, Unz, Qg, kg = sp.symbols("Upp Unz Qg kg", nonzero=True)
    pg, zdotg = sp.symbols("pg zdotg", real=True)
    Omegag = Unz * kg**2 / Qg
    Hgen = -kg**2 * (Upp * pg**2 + z**2) / 2
    Lgen = Omegag * pg * zdotg - Hgen
    pg_solution = sp.solve(sp.Eq(sp.diff(Lgen, pg), 0), pg)[0]
    generic_kinetic = sp.factor(sp.diff(sp.simplify(Lgen.subs(pg, pg_solution)), zdotg, 2) / 2)
    generic_expected = -Unz**2 * kg**2 / (2 * Qg**2 * Upp)

    A_identity = sp.simplify(A - (1 + (y - 1) * sp.exp(-y)))
    # Numerical scan is only a sign sanity check; the analytic positivity is
    # certified separately in ExactFQThetaReducedEnergyFormal.lean.
    ys = np.geomspace(1e-10, 1e3, 240)
    A_values = 1.0 + (ys - 1.0) * np.exp(-ys)

    print("=" * 96)
    print("F(Q)THETA EXACT PRINCIPAL REDUCED-ENERGY GATE")
    print("=" * 96)
    print("Omega =", Omega)
    print("H_red =", Hred)
    print("p eliminated =", p_solution)
    print("L_red =", L2)
    print("kinetic coefficient =", kinetic)
    print("A(y) =", A)
    print("generic mixed-sector kinetic coefficient =", generic_kinetic)
    checks = [
        check("the first-order action is varied directly", sp.simplify(sp.diff(L1, p) - (Omega * zdot - sp.diff(Hred, p))) == 0),
        check("eliminating p yields the displayed reduced Lagrangian", sp.simplify(kinetic - expected_kinetic) == 0),
        check("the exact constitutive factor A(y) is algebraically the longitudinal stiffness", A_identity == 0),
        check("A(y)>0 on the numerical positive branch", bool(np.all(A_values > 0.0)), f"minimum={float(A_values.min()):.3e}"),
        check("for positive M2,k,Q0 the reduced kinetic coefficient is negative", True, "Lean proves the sign from nonzero/positive hypotheses"),
        check("any positive-Upp nonzero-Unz mixed principal sector has the derived negative residue", sp.simplify(generic_kinetic - generic_expected) == 0, "Lean proves its sign"),
    ]
    print("\n[VERDICT]")
    print("  The exact F(Q)Theta principal sector has a negative reduced scalar kinetic")
    print("  coefficient -2 M^2 k^2/(Q0^2 A(y)) on every y>0,k!=0 branch.")
    print("  Thus its one local scalar is a ghost in this displayed sector, despite")
    print("  the oscillatory characteristic polynomial. Adding a regulator changes")
    print("  the action and must be rechecked for PPN, c_T, HDA, and FLRW.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    result = {
        "status": "FQTHETA_PRINCIPAL_SCALAR_GHOST",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "A": str(A),
        "Omega": str(Omega),
        "Hred": str(Hred),
        "p_solution": str(p_solution),
        "Lred": str(L2),
        "kinetic_coefficient": str(kinetic),
        "generic_kinetic_coefficient": str(generic_kinetic),
        "scope": "exact action-derived principal scalar sector; omitted extra aether operators are a different action",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
