#!/usr/bin/env python3
"""A controlled Einstein--aether completion of the ALC corner.

The acceleration-only ALC term sits at the singular constant-aether corner
``c1=c2=c3=0``.  This gate does not replace that action.  It asks a sharper
question: if the corner is regularised by nonzero constant aether coefficients,
can the standard PPN tuning and the luminal-GW condition be met while the
extra scalar mode disappears?

The two PPN equations are solved symbolically.  The mode speeds are then
evaluated from the standard quadratic Einstein--aether principal-symbol
formulae.  No rank, determinant, or degree-of-freedom count is inserted as a
target: regularity of the denominators is used to identify the ordinary
branch, and vanishing kinetic denominators are reported as a separate
degenerate branch requiring its own Dirac analysis.

This is a necessary-condition gate, not a certification of the full ALC
theory.  In particular, a regular completion has a nonzero spin-0 aether
principal symbol and therefore does not satisfy ``N_grav=2``.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def symbolic_branch():
    e, r = sp.symbols("epsilon r", real=True)
    c1 = e
    c3 = r * e
    # alpha_1=0 gives c1*c4 + c3**2=0 on the regular denominator branch.
    c4 = sp.simplify(-c3**2 / c1)
    # alpha_2=0 is solved by the second factor in the standard expression.
    c2 = sp.simplify((-2 * c1**2 - c1 * c3 + c3**2) / (3 * c1))
    c13 = sp.factor(c1 + c3)
    c14 = sp.factor(c1 + c4)
    c123 = sp.factor(c1 + c2 + c3)
    alpha1 = sp.factor(-8 * (c3**2 + c1 * c4)
                       / (2 * c1 - c1**2 + c3**2))
    alpha2 = sp.factor(alpha1 / 2
                       - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4)
                       / (c123 * (2 - c14)))
    s0 = sp.factor(c123 * (2 - c14)
                   / (c14 * (1 - c13) * (2 + c13 + 3 * c2)))
    s1 = sp.factor((2 * c1 - c1**2 + c3**2)
                   / (2 * c14 * (1 - c13)))
    s2 = sp.factor(1 / (1 - c13))
    exact_c13_roots = sp.solve(sp.Eq(c13, 0), r)
    exact_tensor_substitution = {
        "c13": sp.simplify(c13.subs(r, -1)),
        "c14": sp.simplify(c14.subs(r, -1)),
        "c123": sp.simplify(c123.subs(r, -1)),
        "s0_sq": sp.simplify(s0.subs(r, -1)),
    }
    s0_from_above = sp.limit(s0, r, -1, dir="+")
    # General (not epsilon-r parameterised) exact-luminal implication.
    d1, d2, d3, d4 = sp.symbols("d1 d2 d3 d4", real=True)
    general_alpha1_num = sp.factor(d3**2 + d1 * d4)
    exact_luminal_alpha1_num = sp.factor(general_alpha1_num.subs(d3, -d1))
    exact_luminal_c14 = sp.factor((d1 + d4).subs(d4, -d1))
    exact_luminal_alpha2_first_factor = sp.factor(
        (d1 + 2 * d3 - d4).subs({d3: -d1, d4: -d1})
    )
    return {
        "symbols": (e, r),
        "c1": c1, "c2": c2, "c3": c3, "c4": c4,
        "c13": c13, "c14": c14, "c123": c123,
        "alpha1": alpha1, "alpha2": alpha2,
        "s0_sq": s0, "s1_sq": s1, "s2_sq": s2,
        "s0_minus_one": sp.factor(sp.together(s0 - 1)),
        "exact_c13_zero_roots": exact_c13_roots,
        "exact_tensor_substitution": exact_tensor_substitution,
        "s0_limit_r_to_minus_one_from_above": s0_from_above,
        "general_exact_luminal_alpha1_numerator": general_alpha1_num,
        "exact_luminal_alpha1_numerator_after_c13": exact_luminal_alpha1_num,
        "exact_luminal_c14_after_alpha1": exact_luminal_c14,
        "exact_luminal_alpha2_first_factor": exact_luminal_alpha2_first_factor,
    }


def _float(expr, subs):
    value = complex(sp.N(expr.subs(subs), 30))
    if abs(value.imag) > 1e-10:
        return float("nan")
    return float(value.real)


def evaluate_point(branch, epsilon, r, gw_bound=1e-15, speed_floor=1.0):
    e, rs = branch["symbols"]
    subs = {e: sp.Float(epsilon, 30), rs: sp.Float(r, 30)}
    vals = {name: _float(branch[name], subs)
            for name in ("c1", "c2", "c3", "c4", "c13", "c14", "c123",
                         "s0_sq", "s1_sq", "s2_sq")}
    scalar_kinetic_factor = (vals["c14"] * (1.0 - vals["c13"])
                             * (2.0 + vals["c13"] + 3.0 * vals["c2"]))
    scalar_gradient_factor = vals["c123"] * (2.0 - vals["c14"])
    regular = all(math.isfinite(vals[key]) for key in
                  ("s0_sq", "s1_sq", "s2_sq"))
    denominators_nonzero = (abs(vals["c14"]) > 0.0 and
                            abs(vals["c123"]) > 0.0 and
                            abs(1.0 - vals["c13"]) > 0.0)
    speeds_positive = all(vals[key] > 0.0 for key in ("s0_sq", "s1_sq", "s2_sq"))
    speeds_not_sub_c = all(vals[key] >= speed_floor for key in
                           ("s0_sq", "s1_sq", "s2_sq"))
    gw_ok = abs(vals["c13"]) <= gw_bound
    # On the regular branch c14 and c123 are the denominators controlling the
    # scalar principal symbol.  Their simultaneous vanishing is precisely the
    # degenerate case, not a regular way to erase the scalar.
    extra_scalar_mode = (regular and denominators_nonzero
                         and scalar_kinetic_factor != 0.0
                         and scalar_gradient_factor != 0.0)
    return {
        "epsilon": epsilon,
        "r": r,
        **vals,
        "regular_principal_symbol": regular and denominators_nonzero,
        "scalar_kinetic_factor": scalar_kinetic_factor,
        "scalar_gradient_factor": scalar_gradient_factor,
        "speeds_positive": speeds_positive,
        "speeds_at_least_c": speeds_not_sub_c,
        "gw_c13_ok": gw_ok,
        "extra_scalar_mode_on_regular_branch": extra_scalar_mode,
        "passes_necessary_ppn_gw_speed_gate": (
            regular and denominators_nonzero and gw_ok and speeds_positive
            and speeds_not_sub_c
        ),
    }


def build_scan(gw_bound=1e-15, speed_floor=1.0):
    branch = symbolic_branch()
    # Include both ordinary regularisations and the limiting region in which
    # c14 or c123 tends to zero.  The grid is deliberately deterministic.
    epsilons = [10.0 ** (-p) for p in range(2, 17)]
    ratios = [-1.2, -1.0, -0.9, -0.5, 0.0, 0.5, 0.6, 1.0, 2.0]
    points = [evaluate_point(branch, e, r, gw_bound, speed_floor)
              for e in epsilons for r in ratios]
    regular_passes = [p for p in points
                      if p["passes_necessary_ppn_gw_speed_gate"]]
    regular_mode_failures = [p for p in regular_passes
                             if p["extra_scalar_mode_on_regular_branch"]]
    degenerate_limits = [p for p in points
                         if not p["regular_principal_symbol"]]
    return {
        "symbolic_branch": {key: str(value) for key, value in branch.items()
                            if key != "symbols"},
        "scan_definition": {
            "epsilon_values": epsilons,
            "r_values": ratios,
            "gw_bound_on_c13": gw_bound,
            "speed_floor_squared": speed_floor,
        },
        "points": points,
        "counts": {
            "total": len(points),
            "regular_necessary_gate_passes": len(regular_passes),
            "regular_passes_with_extra_scalar": len(regular_mode_failures),
            "degenerate_or_singular_points": len(degenerate_limits),
        },
        "interpretation": {
            "exact_luminal_tensor_implication": "On the alpha-tuned branch with epsilon nonzero, c13=0 solves r=-1 exactly; this simultaneously gives c14=c123=0, so exact tensor luminality is the degenerate scalar surface rather than a regular two-tensor point.",
            "regular_branch": "alpha1=alpha2=0 is algebraically tunable and can coexist with c13≈0 and positive/superluminal principal speeds, but every such regular point has a nonzero scalar aether principal symbol; this violates N_grav=2 if that scalar is gravitational.",
            "degenerate_branch": "c14=0 or c123=0 is not a regular PPN solution; standard speed/PPN formulae lose their denominators and require a separate full Dirac calculation.",
            "status": "OPEN",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "aether_regularization.json")
    parser.add_argument("--gw-bound", type=float, default=1e-15)
    parser.add_argument("--speed-floor", type=float, default=1.0)
    args = parser.parse_args(argv)
    result = build_scan(args.gw_bound, args.speed_floor)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
