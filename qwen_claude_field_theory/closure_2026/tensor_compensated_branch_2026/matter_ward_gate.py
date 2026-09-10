#!/usr/bin/env python3
"""Action-level ordinary-matter Ward identity for the one-metric branch.

For a canonical scalar matter field minimally coupled to the same metric g,
this script derives the matter Euler--Lagrange expression and the covariant
stress divergence on a generic diagonal 1+1 metric.  It verifies

    nabla^mu T_{mu nu} = E_psi * partial_nu psi,

so ordinary matter is conserved on its own equation of motion, independently
of the auxiliary gravity equations.  The computation is a local coordinate
check, not a claim about the unfinished full covariant tensor-multiplier
variation.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def euler_lagrange(density, field, coords):
    result = sp.diff(density, field)
    for coord in coords:
        result -= sp.diff(sp.diff(density, sp.diff(field, coord)), coord)
    return sp.simplify(result)


def main() -> int:
    t, x = sp.symbols("t x", real=True)
    coords = (t, x)
    N = sp.Function("N")(t, x)
    A = sp.Function("A")(t, x)
    psi = sp.Function("psi")(t, x)
    V = sp.Function("V")
    g = sp.diag(-N**2, A**2)
    gi = g.inv()
    n = 2

    Gamma = [[[sp.simplify(sum(
        gi[l, d] * (sp.diff(g[d, j], coords[i]) + sp.diff(g[d, i], coords[j])
                    - sp.diff(g[i, j], coords[d])) / 2
        for d in range(n))) for j in range(n)] for i in range(n)]
              for l in range(n)]
    dpsi = [sp.diff(psi, coord) for coord in coords]
    kinetic = sp.simplify(sum(gi[a, b] * dpsi[a] * dpsi[b]
                              for a in range(n) for b in range(n)))
    sqrt_minus_g = N * A
    density = sqrt_minus_g * (-kinetic / 2 - V(psi))

    box_psi = sp.simplify(sum(
        gi[a, b] * (sp.diff(psi, coords[a], coords[b]) -
                    sum(Gamma[l][a][b] * dpsi[l] for l in range(n)))
        for a in range(n) for b in range(n)))
    Epsi = sp.simplify(box_psi - sp.diff(V(psi), psi))
    direct_el = euler_lagrange(density, psi, coords)

    T = sp.MutableDenseMatrix(n, n, lambda a, b: sp.simplify(
        dpsi[a] * dpsi[b] - g[a, b] * (kinetic / 2 + V(psi))))
    divergence = []
    for nu in range(n):
        value = 0
        for mu in range(n):
            for al in range(n):
                term = sp.diff(T[al, nu], coords[mu])
                term -= sum(Gamma[b][mu][al] * T[b, nu] for b in range(n))
                term -= sum(Gamma[b][mu][nu] * T[al, b] for b in range(n))
                value += gi[mu, al] * term
        divergence.append(sp.simplify(value))

    checks = [
        sp.simplify(direct_el - sqrt_minus_g * Epsi) == 0,
        all(sp.simplify(divergence[nu] - Epsi * dpsi[nu]) == 0
            for nu in range(n)),
        any(divergence[nu] != 0 for nu in range(n)),
        any(Epsi * dpsi[nu] != 0 for nu in range(n)),
    ]
    print("MINIMAL-MATTER WARD IDENTITY GATE")
    print("E_psi =", Epsi)
    print("direct Euler-Lagrange / (sqrt-g E_psi) residual =",
          sp.simplify(direct_el - sqrt_minus_g * Epsi))
    print("divergence residuals =",
          [sp.simplify(divergence[nu] - Epsi * dpsi[nu]) for nu in range(n)])
    print("checks =", sum(bool(x) for x in checks), "/", len(checks))
    result = {
        "status": "ORDINARY_MATTER_WARD_PASS",
        "checks": {"count": len(checks), "passed": sum(bool(x) for x in checks)},
        "euler_lagrange_residual": str(sp.simplify(direct_el - sqrt_minus_g * Epsi)),
        "ward_residuals": [str(sp.simplify(divergence[nu] - Epsi * dpsi[nu]))
                           for nu in range(n)],
        "identity": "nabla^mu T_{mu nu}=E_psi partial_nu psi; E_psi=0 => ordinary matter conservation",
        "scope": "canonical scalar minimally coupled to the single physical metric on a generic diagonal 1+1 chart",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(bool(x) for x in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
