#!/usr/bin/env python3
"""Clock-only Dirac gate for the acceleration-locked action.

For T=t+tau on a locally flat background, the acceleration is
a_i=-partial_i dot(tau)+O(2).  The mimetic multiplier fluctuation s=delta sigma
therefore gives the exact quadratic Fourier-mode model

  L = 1/2 (sigma0+4 M2 k^2) dot(tau)^2 + s dot(tau)
      - 1/2 sigma0 k^2 tau^2.

The script derives the momenta, Hamiltonian, primary/secondary constraints,
their Poisson matrix, and the k=0/k!=0 count.  It is a clock-sector result;
metric mixing and the full nonlinear khronon chain remain open.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def pb(A, B, qs, ps):
    return sp.simplify(sum(sp.diff(A, q) * sp.diff(B, p)
                          - sp.diff(A, p) * sp.diff(B, q)
                          for q, p in zip(qs, ps)))


def build_gate():
    tau, s, ptau, ps = sp.symbols("tau delta_sigma p_tau p_sigma", real=True)
    zdot = sp.symbols("tau_dot", real=True)
    sigma0, M2, k = sp.symbols("sigma0 M2 k", positive=True, real=True)
    A = sigma0 + 4 * M2 * k**2
    L = sp.Rational(1, 2) * A * zdot**2 + s * zdot \
        - sp.Rational(1, 2) * sigma0 * k**2 * tau**2
    p_tau = sp.diff(L, zdot)
    H = sp.simplify((ptau - s)**2 / (2 * A)
                    + sp.Rational(1, 2) * sigma0 * k**2 * tau**2)
    qs, pvars = [tau, s], [ptau, ps]
    primary = [ps]
    secondary = [ptau - s]
    constraints = primary + secondary
    C = sp.Matrix([[pb(Ac, Bc, qs, pvars) for Bc in constraints]
                   for Ac in constraints])
    detC = sp.factor(C.det())
    jac = sp.Matrix([[sp.diff(c, v) for v in qs + pvars]
                     for c in constraints])
    sample = {sigma0: 1, M2: 1, k: 1}
    zero = {sigma0: 1, M2: 1, k: 0}
    return {
        "L_quadratic": str(L),
        "acceleration_kinetic_coefficient": str(A),
        "p_tau": str(p_tau),
        "Hamiltonian": str(H),
        "primary_constraints": [str(c) for c in primary],
        "secondary_constraints": [str(c) for c in secondary],
        "poisson_matrix": [[str(x) for x in row] for row in C.tolist()],
        "poisson_rank_k_nonzero": C.subs(sample).rank(),
        "poisson_rank_k_zero": C.subs(zero).rank(),
        "poisson_determinant": str(detC),
        "constraint_jacobian_rank": jac.subs(sample).rank(),
        "closure": "the secondary fixes the multiplier of p_sigma; no tertiary constraint is generated",
        "tau_dot_on_constraints": "0",
        "reduced_H_on_constraints": "sigma0*k^2*tau^2/2",
        "interpretation": "the acceleration term changes the would-be kinetic coefficient but the mimetic secondary removes tau_dot; the clock remains a zero-sound-speed matter mode, not an acceleration-propagating wave",
        "status": "OPEN",
        "non_claims": ["metric-clock mixing", "full covariant khronon Dirac algebra", "caustic/strong-coupling health"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "clock_dirac.json")
    args = parser.parse_args(argv)
    result = build_gate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
