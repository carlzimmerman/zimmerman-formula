#!/usr/bin/env python3
"""PPN-singular-corner and constitutive-Hessian audit for ALC.

The acceleration-only covariant term is the hypersurface-orthogonal analogue
of an Einstein-aether c4 invariant.  Standard aether PPN formulae are evaluated
symbolically rather than replaced by zeros.  The same action's Hessian with
respect to the acceleration vector is also derived; its longitudinal eigenvalue
changes sign at y=1.  These are warnings for the full coupled gate, not a
universal no-go, because the mimetic constraint can remove the corresponding
clock velocity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def build_audit():
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    c123 = c1 + c2 + c3
    c13 = c1 + c3
    c14 = c1 + c4
    alpha1 = sp.factor(-8 * (c3**2 + c1 * c4)
                       / (2 * c1 - c1**2 + c3**2))
    alpha2 = sp.factor(alpha1 / 2
                       - (c1 + 2 * c3 - c4)
                       * (2 * c1 + 3 * c2 + c3 + c4)
                       / (c123 * (2 - c14)))
    q = sp.symbols("q", nonnegative=True)
    pure_c4 = {c1: 0, c2: 0, c3: 0, c4: q}
    alpha1_c4 = sp.simplify(alpha1.subs(pure_c4))
    alpha2_c4 = sp.simplify(alpha2.subs(pure_c4))
    eps = sp.symbols("epsilon", positive=True)
    alpha1_path_c3zero = sp.simplify(
        sp.limit(alpha1.subs({c1: eps, c2: 0, c3: 0, c4: q}), eps, 0)
    )
    alpha1_path_c1zero = sp.simplify(
        sp.limit(alpha1.subs({c1: 0, c2: 0, c3: eps, c4: q}), eps, 0)
    )

    # ALC acceleration momentum Pi_i=4 M2 exp(-y) a_i.  The Hessian in
    # directions transverse/parallel to the nonzero background acceleration is
    # obtained by differentiating this vector constitutive law.
    y, M2 = sp.symbols("y M2", positive=True)
    lam_perp = sp.simplify(4 * M2 * sp.exp(-y))
    lam_parallel = sp.simplify(4 * M2 * sp.exp(-y) * (1 - y))
    crossing = sp.solve(sp.Eq(lam_parallel, 0), y)
    sample = {M2: 1}
    return {
        "standard_aether_alpha1": str(alpha1),
        "standard_aether_alpha2": str(alpha2),
        "ALC_effective_corner": "c1=c2=c3=0, c4=nonzero (acceleration invariant only)",
        "alpha1_pure_c4": str(alpha1_c4),
        "alpha2_pure_c4": str(alpha2_c4),
        "alpha1_path_c3_zero": str(alpha1_path_c3zero),
        "alpha1_path_c1_zero": str(alpha1_path_c1zero),
        "alpha1_path_dependence": sp.simplify(alpha1_path_c3zero - alpha1_path_c1zero) != 0,
        "ppn_corner_is_regular": bool(alpha1_c4.is_finite and alpha2_c4.is_finite),
        "acceleration_momentum": "Pi_i=4 M2 exp(-y) a_i",
        "hessian_transverse": str(lam_perp),
        "hessian_longitudinal": str(lam_parallel),
        "longitudinal_sign_crossing": [str(v) for v in crossing],
        "deep_mond_sign": str(sp.sign(lam_parallel.subs({y: sp.Rational(1, 2)}).subs(sample))),
        "high_acceleration_sign": str(sp.sign(lam_parallel.subs({y: 2}).subs(sample))),
        "interpretation": "the constitutive Hessian is positive transverse but longitudinally changes sign at y=1; the mimetic constraint and metric mixing must decide whether this is a propagating instability",
        "status": "OPEN",
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "ppn_stability.json")
    args = parser.parse_args(argv)
    result = build_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
