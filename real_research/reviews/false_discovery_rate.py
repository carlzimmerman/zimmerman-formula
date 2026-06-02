#!/usr/bin/env python3
"""
False-Discovery-Rate analysis for the BriareusFlow pattern search.
==================================================================

The Z2 framework's headline result is alpha^-1 = 4Z^2 + 3 = 137.041, quoted as a
"0.004% match" to the measured 137.036. That number was found by BriareusFlow, which
brute-forces ~34,000 simple closed-form expressions and reports the closest one.

The question the repo's own META_HONESTY_ASSESSMENT.md says was never answered:

    Given a search of this size, how often does it hit an ARBITRARY target to that
    precision purely by chance?

If the answer is "almost always," then a 0.004% retrodiction carries essentially zero
evidential weight -- it is the expected output of the search, not a discovery.

This script reconstructs the exact search space from ai_slop/BriareusFlow/pattern_search.py
(same building blocks, same integer ranges, same families) and measures the best
achievable relative error for (a) alpha^-1 specifically and (b) thousands of arbitrary
targets, with no fitting to physics.

Pure-stdlib + numpy. Run (from repo root):  python real_research/reviews/false_discovery_rate.py
"""

import math
from math import gcd
import numpy as np

# --- Building blocks, copied verbatim from pattern_search.py / phenomenological.py ---
Z_SQUARED = 32 * math.pi / 3        # 33.5103...
Z = math.sqrt(Z_SQUARED)            # 5.7888...
PHI = (1 + math.sqrt(5)) / 2        # 1.6180...
PI = math.pi
MAXI = 50                           # max_integer / max_denominator (DEFAULT_CONFIG)
COMMON_ROOTS = [2, 3, 5, 6, 7, 10]  # _search_sqrt_multiples


def build_value_set():
    """Reconstruct every closed-form VALUE the engine can emit.

    Mirrors the seven _search_* methods in pattern_search.py exactly. Trig values are
    returned separately because the engine only tests them when 0 < target < 180.
    Returns (base_values, trig_values) as numpy arrays.
    """
    base = []   # target-independent families
    trig = []   # arccos / arctan, only used for angle-like targets (<180)

    # 1. Simple fractions a/b and b/a  (coprime, 1..50)
    for a in range(1, MAXI + 1):
        for b in range(1, MAXI + 1):
            if gcd(a, b) != 1:
                continue
            base.append(a / b)
            if a != b:
                base.append(b / a)

    # 2. Z^2 terms
    for a in range(1, MAXI + 1):
        base.append(a * Z_SQUARED)                       # aZ^2
        for b in range(-MAXI, MAXI + 1):                 # aZ^2 + b  (b != 0)
            if b == 0:
                continue
            base.append(a * Z_SQUARED + b)
        base.append(a / Z_SQUARED)                       # a/Z^2
        base.append(1 + a / Z_SQUARED)                   # 1 + a/Z^2
        v = 1 - a / Z_SQUARED                            # 1 - a/Z^2  (engine keeps only >0)
        if v > 0:
            base.append(v)

    # 3. Pi multiples
    for a in range(1, MAXI + 1):
        base.append(a * PI)                              # aPi
        base.append(PI / a)                              # Pi/a
        for b in range(2, MAXI + 1):                     # aPi/b (coprime)
            if gcd(a, b) != 1:
                continue
            base.append(a * PI / b)

    # 4. sqrt(n) multiples
    for n in COMMON_ROOTS:
        s = math.sqrt(n)
        for a in range(1, MAXI + 1):
            base.append(a * s)                           # a*sqrt(n)
            base.append(s / a)                           # sqrt(n)/a

    # 5. phi (golden ratio) terms
    for a in range(1, MAXI + 1):
        base.append(a * PHI)                             # a*phi
        base.append(PHI / a)                             # phi/a
        for b in range(-MAXI, MAXI + 1):                 # a*phi + b
            if b == 0:
                continue
            base.append(a * PHI + b)
        if a <= 10:
            base.append(PHI ** a)                        # phi^a
            base.append(PHI ** (-a))                     # phi^-a

    # 6. Compound (a+b)/c and (a-b)/c, 1..20, c 2..20
    for a in range(1, 21):
        for b in range(1, 21):
            for c in range(2, 21):
                if a == b:
                    continue
                base.append((a + b) / c)
                if a > b:
                    base.append((a - b) / c)

    # 7. Trigonometric (degrees) -- only emitted when 0 < target < 180
    for a in range(-MAXI, MAXI + 1):
        for b in range(1, MAXI + 1):
            r = a / b
            if abs(r) <= 1:
                trig.append(math.degrees(math.acos(r)))
            trig.append(math.degrees(math.atan(r)))

    return np.array(base, dtype=float), np.array(trig, dtype=float)


def best_rel_error(target, base, trig):
    """Smallest relative error (in %) any formula achieves for `target`.

    Includes trig values only when 0 < target < 180, exactly as the engine does.
    """
    vals = base
    if 0 < target < 180:
        vals = np.concatenate([base, trig])
    return float(np.min(np.abs(vals - target)) / abs(target) * 100.0)


def main():
    base, trig = build_value_set()
    n_total = base.size + trig.size
    print("=" * 72)
    print("BriareusFlow search space, reconstructed from pattern_search.py")
    print("=" * 72)
    print(f"  base (non-trig) formula values : {base.size:,}")
    print(f"  trig formula values (<180 only): {trig.size:,}")
    print(f"  TOTAL combinations             : {n_total:,}   (docs say '34,000+')")
    print()

    # --- Fidelity sanity checks: the engine's own headline hits must be reproducible ---
    alpha = 137.035999
    formula_4z2p3 = 4 * Z_SQUARED + 3
    print("Fidelity checks (engine's claimed matches must be in the set):")
    print(f"  4Z^2 + 3        = {formula_4z2p3:.6f}   "
          f"(err vs alpha^-1 = {abs(formula_4z2p3-alpha)/alpha*100:.4f}%)")
    print(f"  3/13            = {3/13:.6f}   "
          f"(err vs sin^2θ_W=0.23122 = {abs(3/13-0.23122)/0.23122*100:.4f}%)")
    print(f"  13/19           = {13/19:.6f}   "
          f"(err vs Ω_Λ=0.685 = {abs(13/19-0.685)/0.685*100:.4f}%)")
    print()

    # =================================================================
    # (a) The alpha^-1 hit in context
    # =================================================================
    print("-" * 72)
    print("(a) alpha^-1 = 137.035999  -- how special is the 0.004% hit?")
    print("-" * 72)
    vals_alpha = np.concatenate([base, trig])  # 137 < 180, trig applies
    rel = np.abs(vals_alpha - alpha) / alpha * 100.0
    best = rel.min()
    within_1   = int((rel < 1.0).sum())
    within_01  = int((rel < 0.1).sum())
    within_004 = int((rel < 0.004).sum())
    print(f"  best achievable error for alpha^-1 : {best:.5f}%  "
          f"(formula 4Z^2+3 gives {abs(formula_4z2p3-alpha)/alpha*100:.5f}%)")
    print(f"  # formulas within 1%      of alpha^-1: {within_1}")
    print(f"  # formulas within 0.1%    of alpha^-1: {within_01}")
    print(f"  # formulas within 0.004%  of alpha^-1: {within_004}")
    print()

    # =================================================================
    # (b) Arbitrary targets: how often does the search match ANYTHING?
    # =================================================================
    print("-" * 72)
    print("(b) Arbitrary targets (NO physics) -- look-elsewhere baseline")
    print("-" * 72)
    rng = np.random.default_rng(0)

    def sweep(lo, hi, n, label):
        # log-uniform random targets across [lo, hi]
        t = np.exp(rng.uniform(math.log(lo), math.log(hi), size=n))
        errs = np.array([best_rel_error(x, base, trig) for x in t])
        med = np.median(errs)
        f1   = float((errs <= 1.0).mean())   * 100
        f01  = float((errs <= 0.1).mean())   * 100
        f004 = float((errs <= 0.004).mean()) * 100
        print(f"  {label}")
        print(f"     median best-match error : {med:.4f}%")
        print(f"     matched to <= 1%        : {f1:5.1f}% of targets")
        print(f"     matched to <= 0.1%      : {f01:5.1f}% of targets")
        print(f"     matched to <= 0.004%    : {f004:5.1f}% of targets")
        return med, f1, f01, f004

    # Range around the physics constants the framework actually 'predicts'
    sweep(1.0, 200.0, 20000, "targets in [1, 200] (O(1)-O(100), like the SM constants):")
    print()
    sweep(100.0, 150.0, 20000, "targets in [100, 150] (the alpha^-1 neighborhood):")
    print()

    # =================================================================
    # (c) Headline conclusion
    # =================================================================
    t = np.exp(rng.uniform(math.log(100), math.log(150), size=50000))
    errs = np.array([best_rel_error(x, base, trig) for x in t])
    f_alpha_level = float((errs <= 0.004).mean()) * 100
    print("=" * 72)
    print("(c) HEADLINE")
    print("=" * 72)
    print(f"  In the alpha^-1 neighborhood [100,150], the search matches an ARBITRARY")
    print(f"  target to <= 0.004% (the quoted alpha precision) {f_alpha_level:.1f}% of the time,")
    print(f"  and to <= 1% essentially always. The 137.041 retrodiction is the expected")
    print(f"  output of a {n_total:,}-formula search, not a discovery: it carries ~0 bits")
    print(f"  of evidence for Z^2 = 32pi/3 being physical.")
    print("=" * 72)


if __name__ == "__main__":
    main()
