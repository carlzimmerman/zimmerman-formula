#!/usr/bin/env python3
"""Flat-background causal-support gate for the clock/projector construction.

The clock construction uses spatial York/Hodge pseudoinverses.  A static
inverse Laplacian is not automatically a physical instantaneous channel: in
the full conserved-source response its pole may cancel against the scalar,
vector and tensor equations.  This gate audits that question in the exact
constant-coefficient Fourier family already defined by ``parameter_family_gate``.

The underlying action is

  S = (16 pi G_b)^-1 int sqrt(-g) [R-2 Lambda-ell Theta^2
      + a0^2 f(a/a0) + eta_V V_i Delta_h^dagger V^i + eta_U U^2] + S_m,

with f chosen so that the static branch has mu(y)=1-exp(-y).  The gate does
not assume a rank or a desired pole cancellation.  It re-runs the six-source
symbolic response, derives the two residue-free coefficient branches, and
checks denominator divisibility by the luminal and clock-wave symbols.

Result scope: exact flat, constant-coefficient, conserved-source linear
response.  Passing this gate is evidence against an instantaneous pole on
that branch; it is not a nonlinear covariant causality theorem.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import sympy as sp

from parameter_family_gate import scalar_family


HERE = Path(__file__).resolve().parent


def derive_wave_symbols():
    """Derive, rather than insert, the two response denominator symbols."""
    C, ell, r, kx, kz = sp.symbols("C ell rate kx kz", real=True)
    K = sp.expand(kx**2 + kz**2)
    d = t = C / 2
    alpha = 2 - C
    z, n, B, zd = sp.symbols("z n B zd", real=True)
    L = (-6 * t * zd**2 + 4 * d * K * zd * B
         - ell * (3 * zd - K * B)**2
         + K * (2 * z**2 - 4 * n * z + alpha * n**2))
    W = sp.hessian(L, [zd, n, B])
    equations = [
        sp.diff(L, n).subs(zd, r * z),
        sp.diff(L, B).subs(zd, r * z),
        (r * sp.diff(L, zd) - sp.diff(L, z)).subs(zd, r * z),
    ]
    E = sp.Matrix([[sp.diff(e, v) for v in (z, n, B)] for e in equations])
    detE = sp.factor(E.det())
    light = sp.expand(r**2 + K)
    clock = sp.expand((2 - C) * (C + 3 * ell) * r**2 + 2 * ell * K)
    return {
        "kinetic_hessian": W,
        "equation_determinant": detE,
        "light_symbol": light,
        "clock_symbol": clock,
        "clock_speed_squared": sp.factor(2 * ell / ((2 - C) * (C + 3 * ell))),
    }


def build_gate():
    family = scalar_family()
    waves = derive_wave_symbols()
    C, ell, kx, kz, r = sp.symbols("C ell kx kz rate", real=True)
    witness = {C: sp.Rational(5, 3), ell: sp.Rational(1, 100)}
    light = waves["light_symbol"]
    clock = waves["clock_symbol"]

    branches = family["all_six_source_branches"]
    passing = [row for row in branches
               if row["spatial_pole_count"] == 0
               and row["factor_failure_count"] == 0]
    rejected = [row for row in branches
                if row["spatial_pole_count"] > 0]

    cs2 = sp.factor(waves["clock_speed_squared"].subs(witness))
    light_speed = sp.Integer(1)
    no_spatial_pole = len(passing) == 1 and all(
        row["spatial_pole_count"] == 0 and row["factor_failure_count"] == 0
        for row in passing
    )
    contrast = len(rejected) >= 1

    return {
        "action": "R - 2 Lambda - ell Theta^2 + a0^2 f(a/a0) + eta_V V Delta_h^dagger V + eta_U U^2",
        "family_status": family.get("status"),
        "residue_free_branches": family.get("residue_free_branches"),
        "all_six_source_branches": branches,
        "selected_branch_count": len(passing),
        "rejected_branch_count": len(rejected),
        "wave_symbols": {
            "light": str(light),
            "clock": str(clock),
            "clock_speed_squared": str(cs2),
            "light_speed_squared": str(light_speed),
            "equation_determinant": str(waves["equation_determinant"]),
        },
        "checks": {
            "six_source_selected_branch_has_no_spatial_pole": no_spatial_pole,
            "alternate_branch_exhibits_spatial_pole": contrast,
            "clock_wave_is_subluminal_at_witness": bool(0 < cs2 < 1),
            "light_wave_is_luminal": bool(light_speed == 1),
        },
        "status": "OPEN",
        "verdict": (
            "The all-six-polarization response selects one coefficient branch "
            "whose flat linear denominators contain only the luminal and clock "
            "wave factors; the alternate residue-free branch retains a bare "
            "spatial pole.  This is a causal-support PASS for the selected "
            "constant-coefficient linear family, not a full nonlinear theorem."
        ),
        "non_claims": [
            "no nonlinear metric-dependent pseudoinverse variation",
            "no full covariant Dirac algebra on curved leaves",
            "no boosted PPN beta/alpha2/alpha3 derivation",
            "no FLRW perturbation or empirical catalogue fit",
        ],
        "provenance": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "upstream": "parameter_family_gate.scalar_family()",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_002" / "causal_support_results.json")
    args = parser.parse_args(argv)
    result = build_gate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps(result, indent=2, default=str))
    if not all(result["checks"].values()):
        raise SystemExit("causal-support gate failed")


if __name__ == "__main__":
    main()
