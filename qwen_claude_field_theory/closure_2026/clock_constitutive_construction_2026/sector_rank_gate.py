#!/usr/bin/env python3
"""Compute the distinct k=0 and k!=0 sectors of the selected linear branch.

The spatial York/Hodge inverse is defined on the complement of its kernel, so
the homogeneous sector must not be inferred by substituting k=0 into a
nonzero-mode inverse.  This gate derives the Euler-symbol matrix, its actual
determinant and numerical ranks, then checks only sector relations and the
factorization identity.  No rank or determinant is inserted as an expected
constant.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def equation_matrix():
    C, ell, rate, kx, kz = sp.symbols("C ell rate kx kz", real=True)
    K = sp.expand(kx**2 + kz**2)
    # This is the selected residue-free surface d=t=C/2, rederived here.
    matrix = sp.Matrix([
        [-4*K, -2*(C-2)*K, 0],
        [2*rate*(C+3*ell)*K, 0, -2*ell*K**2],
        [-2*(3*C*rate**2 + 9*ell*rate**2 + 2*K),
         4*K, 2*rate*(C+3*ell)*K],
    ])
    determinant = sp.factor(matrix.det())
    factor = sp.factor(8*C*K**3 * (
        C**2*rate**2 + 3*C*ell*rate**2 - 2*C*rate**2
        - 2*ell*K - 6*ell*rate**2))
    return (C, ell, rate, kx, kz, K, matrix, determinant, factor)


def build_gate():
    C, ell, rate, kx, kz, K, matrix, determinant, factor = equation_matrix()
    witness = {C: sp.Rational(5, 3), ell: sp.Rational(1, 100)}
    sectors = {
        "k0_static": {**witness, kx: 0, kz: 0, rate: 0},
        "k0_dynamic": {**witness, kx: 0, kz: 0, rate: 1},
        "kneq_static": {**witness, kx: 1, kz: 0, rate: 0},
        "clock_characteristic": {
            **witness, kx: 1, kz: 0,
            rate: sp.I * sp.sqrt(sp.Rational(18, 509)),
        },
    }
    ranks = {name: int(matrix.subs(values).rank())
             for name, values in sectors.items()}
    determinants = {name: sp.factor(determinant.subs(values))
                    for name, values in sectors.items()}
    factor_identity = sp.simplify(determinant - factor) == 0
    static_zero_mode_is_degenerate = determinants["k0_static"] == 0
    static_nonzero_mode_is_regular = determinants["kneq_static"] != 0
    characteristic_rank_drops = ranks["clock_characteristic"] < ranks["kneq_static"]
    homogeneous_dynamic_differs = ranks["k0_dynamic"] != ranks["kneq_static"]
    checks = {
        "determinant_factorization_derived": factor_identity,
        "k0_static_is_degenerate": static_zero_mode_is_degenerate,
        "kneq_static_is_not_degenerate": static_nonzero_mode_is_regular,
        "clock_characteristic_rank_drops": characteristic_rank_drops,
        "homogeneous_dynamic_sector_is_distinct": homogeneous_dynamic_differs,
    }
    return {
        "status": "SECTOR_SPLIT_COMPLETED; FULL_THEORY_OPEN",
        "branch": "d=t=C/2 (rederived in this gate)",
        "witness": {"C": "5/3", "ell": "1/100"},
        "equation_matrix": [[str(x) for x in matrix.row(i)] for i in range(3)],
        "determinant": str(determinant),
        "factored_determinant": str(factor),
        "sector_ranks": ranks,
        "sector_determinants": {name: str(value) for name, value in determinants.items()},
        "checks": checks,
        "interpretation": {
            "k0": "homogeneous kernel sector; no inverse-Laplacian division is permitted",
            "kneq": "nonzero spatial Fourier sector where the projector complement is defined",
            "characteristic": "rank loss occurs on the derived clock-wave factor, not assumed",
        },
        "non_claims": [
            "No continuum k=0 constraint theorem on curved FLRW",
            "No nonlinear pseudoinverse/domain variation",
            "No full Dirac closure or boosted PPN",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_002" / "sector_rank_results.json")
    args = parser.parse_args(argv)
    result = build_gate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps(result, indent=2, default=str))
    if not all(result["checks"].values()):
        raise SystemExit("sector-rank gate failed")


if __name__ == "__main__":
    main()
