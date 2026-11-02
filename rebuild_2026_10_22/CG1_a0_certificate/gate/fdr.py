"""
GATE A — FDR-survival (look-elsewhere).

"How often would this search hit by chance?"

Ported verbatim-in-spirit from the validation lineage:
  - real_research/reviews/false_discovery_rate.py        (random-target surplus bits)
  - real_research/reviews/mass_fdr/attack5_fdr_partB.py  (local-density Poisson E_chance)
  - real_research/reviews/mass_fdr/attack5_fdr.py         (the rational-target exception)
  - opus_48_extended_research/.../koide_fdr_sqrt2.py      (structural / random-triple null)

Three measures, routed by target type:
  (1) GENERIC real target  -> local-density Poisson E_chance from the reachable library,
      AND random-target surplus bits. FAIL (BAKED) if E_chance >= 1 (dense pool).
  (2) SMALL-DENOMINATOR RATIONAL (Koide's 2/3) -> Gate-A-on-value is uninformative (a
      rational is hit exactly by many symbol combos). Route to the STRUCTURAL null:
      P(relation lands on the target over random no-physics inputs). PASS if that
      probability << 1 (the random-mass-triple null: ~1-in-48,000 for Koide).
  (3) STRUCTURAL relation with a structural_null callable -> same structural null.

Operational PASS threshold (GATE_SPEC A): surplus >= ~10 bits (chance <~ 1e-3), with
the look-elsewhere multiplicity (#targets searched) folded in.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from math import log2
import numpy as np

PASS_BITS = 10.0   # operational threshold from GATE_SPEC A

# CG1 switches. All True is the repaired gate; all False reproduces the original.
REPAIRS = dict(A2=True, A3=True, A4=True)

import math as _math


def _bit_cap(candidate) -> float:
    """The precision cap on surplus bits (Carl's emphasis (a)): you cannot earn more bits of
    evidence than the MEASUREMENT pins. n_digits_known sig figs ~ n_digits*log2(10) bits. A
    structural/poisson chance-probability smaller than 10^-n_digits is below the measurement
    floor and must NOT inflate the bit budget. Returns +inf if no precision info (no cap)."""
    nd = getattr(candidate.search, "n_digits_known", None)
    if nd is None or not _math.isfinite(nd) or nd <= 0:
        return float("inf")
    return nd * _math.log2(10.0)


@dataclass
class FDRResult:
    passed: bool
    bits: float                 # surplus bits over chance (look-elsewhere corrected)
    mode: str                   # "poisson" | "structural" | "rational->structural"
    e_chance: float             # Poisson expectation in tight window (generic mode)
    n_hit: int
    chance_prob: float          # the raw chance probability the bits derive from
    tell: str                   # the verdict tell (why BAKED, or why surprising)


def build_value_set(germ_pool: dict):
    """Reconstruct the reachable VALUE multiset from a germ pool.

    Mirrors attack5_fdr_partB's library: single symbols, then pairwise a*b, a/b, a+b,
    a-b, then the triples a*b+c, a*b-c, a*b/c, a/b+c (where '64*pi+Z' and friends live).
    This is the engine's reachable set; the candidate is ONE point in it.
    """
    names = list(germ_pool)
    vals = np.array([germ_pool[n] for n in names], dtype=float)
    n = len(names)
    lib = []

    def add(v):
        if np.isfinite(v) and 1e-3 < abs(v) < 1e7:
            lib.append(v)

    for i in range(n):
        add(vals[i])
    for i in range(n):
        for j in range(n):
            a, b = vals[i], vals[j]
            add(a * b)
            if b:
                add(a / b)
            add(a + b)
            add(a - b)
    for i, j, k in product(range(n), repeat=3):
        a, b, c = vals[i], vals[j], vals[k]
        add(a * b + c)
        add(a * b - c)
        if c:
            add(a * b / c)
        if b:
            add(a / b + c)
    return np.array(lib, dtype=float)


def _poisson_e_chance(target, lib, tol):
    """attack5_fdr_partB's load-bearing measure: expected hits in the tight window if
    the reachable set is locally uniform over the +-10% band."""
    lo, hi = target * (1 - tol), target * (1 + tol)
    n_hit = int(((lib >= lo) & (lib <= hi)).sum())
    n_wide = int(((lib >= target * 0.9) & (lib <= target * 1.1)).sum())
    e_chance = n_wide * (2 * tol) / 0.2
    return n_hit, e_chance


def _structural_null(structural_null, target, eps, N):
    """koide_fdr_sqrt2's random-triple null (ABSOLUTE): draw N no-physics instances of the
    relation's inputs, compute the relation, return P(|out - target| < eps)."""
    out = np.asarray(structural_null(N))
    out = out[np.isfinite(out)]
    p = float(np.mean(np.abs(out - target) < eps))
    return p


def _support_mismatch(structural_null, target, N):
    """CG1 A2: a target outside the null's support is a unit or scale error, not a surprise."""
    out = np.asarray(structural_null(N))
    out = out[np.isfinite(out)]
    return not (out.min() <= target <= out.max())


def _structural_comparative(structural_null, target, frac_tol, N, baseline_targets):
    """koide_fdr_sqrt2's MECHANISM measure for "dS-Unruh forces sqrt2"-class claims.

    A MECHANISM/density claim is NOT scored by the absolute P(land on target) — a 0.5%
    window over an O(1) range is hit with non-trivial probability by ANY framework combo.
    The meaningful question (koide_fdr_sqrt2) is whether the CLAIMED target is hit MORE
    densely than a RANDOM O(1) target from the same pool:
        surplus = -log2( P_target / P_random ).
    Comparable density => ~0 bits. CG1 A6: as computed, MORE dense => NEGATIVE bits (a hit
    there is less surprising; the documented -1.08 for sqrt2), LESS dense => positive. Returns
    (p_target, p_random, surplus_bits)."""
    out = np.asarray(structural_null(N))
    out = out[np.isfinite(out)]

    def P(t):
        return float(np.mean(np.abs(out - t) / abs(t) < frac_tol))

    p_target = P(target)
    p_rand_list = [P(t) for t in np.asarray(baseline_targets)]
    p_random = float(np.mean(p_rand_list)) if len(p_rand_list) else float("nan")
    if p_target > 0 and p_random > 0:
        surplus = -log2(p_target / p_random)
    elif p_target == 0 and p_random > 0:
        surplus = float("-inf")     # claimed target literally never hit, random is: not special
    else:
        surplus = float("nan")
    return p_target, p_random, surplus


def fdr_test(candidate) -> FDRResult:
    """GATE A. Returns FDRResult(passed, bits, ...).

    PASS = the relation's chance rate is << 1 (surplus bits >= PASS_BITS), with the
    look-elsewhere multiplicity folded in. FAIL = BAKED (dense pool / 0 surplus bits /
    rational re-label with no structural surprise).
    """
    s = candidate.search
    mult = max(1, s.n_targets_searched)
    cap = _bit_cap(candidate)   # precision cap: bits cannot exceed what the measurement pins

    # ----- route: COMPARATIVE structural (mechanism claim, e.g. "dS-Unruh forces sqrt2") --
    # surplus-over-random density (koide_fdr_sqrt2 Q2). Can be NEGATIVE -> "not special".
    if s.structural_null is not None and getattr(s, "structural_baseline", None) is not None:
        baseline_targets = s.structural_baseline(s.structural_baseline_M)
        p_t, p_r, surplus = _structural_comparative(
            s.structural_null, candidate.target_value, s.tol, s.structural_N,
            baseline_targets)
        # look-elsewhere only sharpens a POSITIVE surplus; a negative surplus stays not-special.
        bits = surplus - log2(mult) if (surplus == surplus and abs(surplus) != float("inf")) else surplus
        bits = min(bits, cap)
        passed = bits >= PASS_BITS
        special = "sparser than a random O(1), a hit is surprising" if passed else \
                  ("NOT special: >= random density (mechanism carries ~0 info)"
                   if surplus <= 0 else "below 10-bit threshold")
        tell = (f"comparative density: P(near target)={p_t:.3e} vs "
                f"P(near random O(1))={p_r:.3e} -> surplus={surplus:+.2f} bits; {special}")
        return FDRResult(passed=passed, bits=bits, mode="structural-comparative",
                         e_chance=float("nan"), n_hit=-1, chance_prob=p_t, tell=tell)

    # ----- route: ABSOLUTE structural / rational -> structural null ------------
    if s.structural_null is not None:
        tgt = s.structural_target if s.structural_target is not None else candidate.target_value
        rel = s.structural_relation if s.structural_relation is not None else candidate.relation_value
        if REPAIRS["A2"] and _support_mismatch(s.structural_null, tgt, s.structural_N):
            return FDRResult(passed=False, bits=0.0, mode="NULL-SCALE-MISMATCH", e_chance=float("nan"), n_hit=-1, chance_prob=float("nan"),
                             tell=f"target {tgt:.4g} is outside the null's support: unit or scale mismatch, no evidence either way")
        p = _structural_null(s.structural_null, tgt,
                             s.structural_eps, s.structural_N)
        if REPAIRS["A3"] and p == 0:
            p = 3.0 / s.structural_N   # CG1 A3: an upper limit, finite bits
        if REPAIRS["A4"] and abs(rel - tgt) >= s.structural_eps:
            return FDRResult(passed=False, bits=0.0, mode="NO-HIT", e_chance=float("nan"), n_hit=0, chance_prob=p,
                             tell=f"relation {rel:.5g} is outside the window {tgt:.5g} +- {s.structural_eps:.3g}; null P {p:.3e}, no hit to grade")
        # look-elsewhere correction: multiply the chance probability by #targets.
        p_corr = min(1.0, p * mult)
        bits = -log2(p_corr) if p_corr > 0 else float("inf")
        bits = min(bits, cap)   # uncertainty cap: no more bits than the measurement justifies
        passed = bits >= PASS_BITS
        mode = "rational->structural" if s.rational_target else "structural"
        tell = (f"structural null P(land on target)={p:.3e} "
                f"(x{mult} look-elsewhere -> {p_corr:.3e}); "
                + ("SURPRISING: relation is special for this sector"
                   if passed else "not special: random inputs hit the target as often"))
        return FDRResult(passed=passed, bits=bits, mode=mode, e_chance=float("nan"),
                         n_hit=-1, chance_prob=p_corr, tell=tell)

    # ----- route: bare small-denominator rational with NO structural null ------
    # GATE_SPEC A footnote: re-labeling a rational is FREE and carries no bits. With no
    # structural null supplied, Gate A on the value is uninformative -> cannot pass.
    if s.rational_target:
        # count exact re-descriptions to expose the freedom (attack5_fdr)
        lib = build_value_set(s.germ_pool) if s.germ_pool else np.array([])
        n_exact = int((np.abs(lib - candidate.target_value) < 1e-9).sum()) if lib.size else 0
        tell = (f"target is a small-denominator rational; hit EXACTLY by {n_exact} "
                f"symbol combos -> re-labeling is FREE, 0 surplus bits. Gate A on the "
                f"value is uninformative; needs a structural null.")
        return FDRResult(passed=False, bits=0.0, mode="rational(uninformative)",
                         e_chance=float("inf"), n_hit=n_exact, chance_prob=1.0, tell=tell)

    # ----- route: generic real target -> Poisson E_chance + surplus bits -------
    lib = build_value_set(s.germ_pool)
    n_hit, e_chance = _poisson_e_chance(candidate.target_value, lib, s.tol)
    if REPAIRS["A4"] and abs(candidate.relation_value - candidate.target_value) > s.tol * abs(candidate.target_value):
        return FDRResult(passed=False, bits=0.0, mode="NO-HIT", e_chance=e_chance, n_hit=n_hit, chance_prob=1.0,
                         tell=f"relation {candidate.relation_value:.6g} is outside tol {s.tol} of the target; E_chance {e_chance:.2f}")
    # bits from the Poisson expectation: how surprising is a real hit if E_chance hits
    # are expected? If E_chance >= 1, a hit is expected -> ~0 bits -> BAKED.
    # surplus = -log2(P(>=1 hit by chance)) ~ -log2(min(1, E_chance)) for the dense regime.
    chance = min(1.0, e_chance) * mult
    chance = min(1.0, chance)
    bits = -log2(chance) if chance > 0 else float("inf")
    bits = min(bits, cap)   # uncertainty cap: no more bits than the measurement justifies
    # dense-pool override: E_chance >= 1 is BAKED regardless of bit arithmetic.
    if e_chance >= 1.0:
        passed = False
        tell = (f"E_chance={e_chance:.2f} >= 1: the germ pool densely covers this region "
                f"({n_hit} hits in window); a hit is unsurprising -> BAKED(dense).")
        bits = min(bits, 0.0)
    else:
        passed = bits >= PASS_BITS
        tell = (f"E_chance={e_chance:.3e} (<1, sparse); {n_hit} hits; "
                f"surplus={bits:.1f} bits (x{mult} look-elsewhere). "
                + ("SURPRISING" if passed else "below 10-bit threshold -> BAKED"))
    return FDRResult(passed=passed, bits=bits, mode="poisson", e_chance=e_chance,
                     n_hit=n_hit, chance_prob=chance, tell=tell)
