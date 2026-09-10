#!/usr/bin/env python3
"""Preferred-frame coefficient locus for the tensor-compensated candidate.

The candidate may include the standard Einstein-aether kinetic invariants
with coefficients c1,...,c4.  This gate derives the usual weak-field
preferred-frame expressions symbolically and solves their numerator conditions
on the luminal branch c13=c1+c3=0.  It does not assume the PPN values.

The resulting locus c3=-c1,c4=-c1 makes alpha_1=alpha_2=0 and c_T=1, but
also has c14=c1+c4=0.  The spin-0 aether speed formula is therefore singular
(generally instantaneous), so this is a tuning gate, not a complete pass.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    c13 = c1 + c3
    c14 = c1 + c4
    c123 = c1 + c2 + c3
    den1 = 2 * c1 - c1**2 + c3**2
    den2 = (2 - c14) * c123
    alpha1 = sp.factor(-8 * (c3**2 + c1 * c4) / den1)
    alpha2 = sp.factor(alpha1 / 2 -
                       (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) / den2)
    cT2 = sp.factor(1 / (1 - c13))

    luminal_subs = {c3: -c1}
    a1_luminal = sp.factor(alpha1.subs(luminal_subs))
    a2_luminal = sp.factor(alpha2.subs(luminal_subs))
    a1_num = sp.factor(sp.together(a1_luminal).as_numer_denom()[0])
    a2_num = sp.factor(sp.together(a2_luminal).as_numer_denom()[0])
    c4_solution = sp.solve(sp.Eq(a1_num, 0), c4)
    tuned = {c3: -c1, c4: -c1}
    witness = {c1: sp.Rational(1, 2), c2: sp.Rational(1, 3), **tuned}

    alpha1_tuned = sp.factor(alpha1.subs(tuned))
    alpha2_tuned = sp.factor(alpha2.subs(tuned))
    cT2_tuned = sp.factor(cT2.subs(tuned))
    c13_tuned = sp.simplify(c13.subs(tuned))
    c14_tuned = sp.simplify(c14.subs(tuned))
    den1_witness = sp.simplify(den1.subs(witness))
    den2_witness = sp.simplify(den2.subs(witness))
    spin0_denominator = sp.factor(c14 * (1 - c13) * (2 + c13 + 3 * c2))
    spin0_den_tuned = sp.factor(spin0_denominator.subs(tuned))

    checks = [
        sp.simplify(a1_num - (-4 * (c1 + c4))) == 0,
        c4_solution == [-c1],
        c13_tuned == 0,
        c14_tuned == 0,
        alpha1_tuned == 0,
        alpha2_tuned == 0,
        cT2_tuned == 1,
        den1_witness != 0,
        den2_witness != 0,
        spin0_den_tuned == 0,
    ]

    print("EINSTEIN-AETHER PPN TUNING GATE")
    print("alpha1 =", alpha1)
    print("alpha2 =", alpha2)
    print("cT^2 =", cT2)
    print("luminal alpha1 numerator =", a1_num)
    print("luminal alpha2 numerator =", a2_num)
    print("derived c4 solution =", c4_solution)
    print("tuned (c3,c4) =", tuned[c3], tuned[c4])
    print("tuned alpha1/alpha2/cT^2 =", alpha1_tuned, alpha2_tuned, cT2_tuned)
    print("tuned c13/c14 =", c13_tuned, c14_tuned)
    print("spin-0 speed denominator on tuned locus =", spin0_den_tuned)
    print("checks =", sum(bool(x) for x in checks), "/", len(checks))

    result = {
        "status": "PPN_ALPHA12_PASS_INSTANTANEOUS_SPIN0_OPEN",
        "checks": {"count": len(checks), "passed": sum(bool(x) for x in checks)},
        "derived_locus": "c3=-c1, c4=-c1 on c13=0",
        "alpha1": str(alpha1_tuned),
        "alpha2": str(alpha2_tuned),
        "cT_squared": str(cT2_tuned),
        "c13": str(c13_tuned),
        "c14": str(c14_tuned),
        "spin0_speed_denominator": str(spin0_den_tuned),
        "scope": "standard Einstein-aether weak-field PPN coefficient locus; full candidate metric variation and causal scalar analysis remain open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(bool(x) for x in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
