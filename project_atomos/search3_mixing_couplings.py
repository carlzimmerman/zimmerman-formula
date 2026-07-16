#!/usr/bin/env python3
"""
SEARCH 3 — MIXING + COUPLINGS.

Brute-force closed-form expressions for the SM mixing angles + gauge couplings against
the framework's FORCED building-block pool (geometry germs + group/GUT invariants), then
run EVERY near-hit through the 3-part gate (A: FDR/look-elsewhere; B: forced kernel;
C: interlock). Report N, best matches, gate verdict. Both-ways honest.

Targets: CKM lambda/A/rhobar/etabar + angles; PMNS sin2/angles + deltaCP; sin2_thetaW;
alpha_em^-1(0) & (MZ); alpha_s(MZ).

Search space = a depth-stratified product/ratio/power/sqrt enumeration over the building-
block pool (dimensionless, single-leaf-free — these targets ARE dimensionless O(1) numbers
so the "leaf" is the germ pool itself). This is NOT the engine's measured-leaf cross-tying
(fitting one CKM param from others is meaningless); it asks the real question: does a forced
GROUP-THEORY / GEOMETRIC ratio land the number?

The gate is the whole point. A brute force over ~10^4-10^5 expressions hits a 3-digit O(1)
target by chance; only a gate-survivor counts.
"""
from __future__ import annotations
import itertools
import math
import sys
from dataclasses import dataclass

import mpmath as mp
mp.mp.dps = 40

sys.path.insert(0, "/Users/carlzimmerman/new_physics/project_atomos")

from gate.candidate import Candidate, SearchSpace, Coefficient, Interlock, Factor
from gate.verdict import validate
from targets.pdg_constants import get

# ---------------------------------------------------------------------------
# Building-block pool — FORCED primitives only (the brief's list).
# Each entry: (name, value, is_forced_provenance_or_None)
# "forced provenance" = a registry/group tag meaning the number is pinned by symmetry
# BEFORE any fit. A bare integer/transcendental is a building block but NOT a forced kernel.
# ---------------------------------------------------------------------------
pi = mp.pi

POOL = {
    # transcendental measure factors (building blocks, NOT forced kernels by themselves)
    "pi":     pi,
    "2pi":    2 * pi,
    "4pi":    4 * pi,
    "8pi":    8 * pi,
    "e":      mp.e,
    "phi":    (1 + mp.sqrt(5)) / 2,
    # framework forced kernels
    "Z":      mp.sqrt(32 * pi / 3),
    "kernel": mp.sqrt(8 * pi / 3),
    # small integers / simple roots
    "2":  mp.mpf(2), "3": mp.mpf(3), "4": mp.mpf(4), "5": mp.mpf(5),
    "6":  mp.mpf(6), "7": mp.mpf(7), "8": mp.mpf(8), "9": mp.mpf(9),
    "10": mp.mpf(10), "11": mp.mpf(11), "12": mp.mpf(12), "13": mp.mpf(13),
    "16": mp.mpf(16), "24": mp.mpf(24),
    "sqrt2": mp.sqrt(2), "sqrt3": mp.sqrt(3), "sqrt5": mp.sqrt(5),
    # group/GUT FORCED invariants (these carry a forced provenance)
    "su5_dim":   mp.mpf(24),
    "so10_dim":  mp.mpf(45),
    "e6_dim":    mp.mpf(78),
    "gen_so10":  mp.mpf(16),
    "gen_su5":   mp.mpf(15),
    "gen_e6":    mp.mpf(27),
    "sin2tw_tree": mp.mpf(3) / 8,   # FORCED 3/8 (SU(5) tree Weinberg)
    "gut_5_3":   mp.mpf(5) / 3,     # FORCED GUT normalization
    "ngen":      mp.mpf(3),
    "S3":        mp.mpf(6),
    "A4":        mp.mpf(12),
    "S4":        mp.mpf(24),
    "D27":       mp.mpf(27),
    "coxeter_so10": mp.mpf(8),
    "casimir": mp.mpf(2),
}

# which pool names are FORCED-provenance (group/GUT/geometry-forced) for Gate B
FORCED_PROVENANCE = {
    "su5_dim": "group_su5", "so10_dim": "group_so10", "e6_dim": "group_e6",
    "gen_so10": "group_so10_gen", "gen_su5": "group_su5_gen", "gen_e6": "group_e6_gen",
    "sin2tw_tree": "weinberg_tree_3_8", "gut_5_3": "gut_norm_5_3", "ngen": "n_generations",
    "S3": "group_s3", "A4": "group_a4", "S4": "group_s4", "D27": "group_d27",
    "coxeter_so10": "coxeter_so10", "casimir": "casimir_su2",
}

EXPS = [mp.mpf(1), mp.mpf(2), mp.mpf(3), mp.mpf("0.5"), mp.mpf(-1), mp.mpf(-2),
        mp.mpf("1.5"), mp.mpf("-0.5"), mp.mpf(1) / 3, mp.mpf(2) / 3, mp.mpf("0.25")]


def enumerate_expressions():
    """Depth-limited enumeration of closed forms over POOL.

    Forms (a,b,c in POOL, p,q in EXPS):
      a^p
      a^p * b^q
      a^p / b^q
      a^p + b^q   (only for a few additive, small)
      (a^p * b^q) / c
      (a^p + b^q) / c
    Yields (value_float, formula_str, set_of_pool_names_used).
    """
    names = list(POOL)
    # single power
    for a in names:
        va = POOL[a]
        for p in EXPS:
            try:
                v = va ** p
            except Exception:
                continue
            if mp.isfinite(v) and v > 0:
                yield float(v), f"{a}^{_fp(p)}", {a}
    # two-term products / ratios
    for a, b in itertools.product(names, repeat=2):
        va, vb = POOL[a], POOL[b]
        for p, q in itertools.product(EXPS, EXPS):
            try:
                ap = va ** p
                bq = vb ** q
            except Exception:
                continue
            for op, sym in ((ap * bq, "*"), (ap / bq if bq != 0 else None, "/"),
                            (ap + bq, "+"), (ap - bq, "-")):
                if op is None:
                    continue
                if mp.isfinite(op) and op > 0:
                    yield float(op), f"{a}^{_fp(p)}{sym}{b}^{_fp(q)}", {a, b}
    # three-term: (a^p * b^q)/c  and (a^p + b^q)/c   (c integer-ish scaler)
    scalers = ["2", "3", "4", "5", "6", "8", "ngen", "pi", "2pi", "4pi", "su5_dim",
               "so10_dim", "Z", "kernel", "sqrt2"]
    for a, b in itertools.product(names, repeat=2):
        va, vb = POOL[a], POOL[b]
        for p, q in itertools.product([mp.mpf(1), mp.mpf(2), mp.mpf("0.5"), mp.mpf(-1)], repeat=2):
            try:
                ap = va ** p
                bq = vb ** q
            except Exception:
                continue
            base_mul = ap * bq
            base_add = ap + bq
            for c in scalers:
                vc = POOL[c]
                if vc == 0:
                    continue
                for base, bsym in ((base_mul, "*"), (base_add, "+")):
                    v = base / vc
                    if mp.isfinite(v) and v > 0:
                        yield float(v), f"({a}^{_fp(p)}{bsym}{b}^{_fp(q)})/{c}", {a, b, c}


def _fp(x):
    f = float(x)
    if abs(f - round(f)) < 1e-9:
        return str(int(round(f)))
    return f"{f:.3g}"


@dataclass
class Hit:
    target: str
    formula: str
    value: float
    target_value: float
    rel_err: float
    n_sigma: float
    used: set


def search_target(key, target_value, sigma, rel_prec, n_targets_searched):
    """Enumerate, keep hits within max(3 sigma, 0.3% rel) for ranking; track N."""
    tol_rank = max(3 * sigma / abs(target_value) if sigma else 0.003, 0.003)
    hits = []
    N = 0
    seen_vals = set()
    for v, formula, used in enumerate_expressions():
        N += 1
        rel = abs(v - target_value) / abs(target_value)
        if rel < tol_rank:
            ns = abs(v - target_value) / sigma if sigma else float("inf")
            key_v = round(v, 9)
            if key_v in seen_vals:
                # keep simplest formula only
                continue
            seen_vals.add(key_v)
            hits.append(Hit(key, formula, v, target_value, rel, ns, used))
    # rank: closest first, then fewest building blocks (simplest)
    hits.sort(key=lambda h: (h.rel_err, len(h.formula)))
    return N, hits


def gate_hit(hit, rel_prec, sigma, n_digits, n_targets_searched):
    """Build a Candidate and run the full 3-gate validator on a single hit.

    Search space = the POOL as a germ_pool dict (Gate A reconstructs the reachable density
    near the target -> the look-elsewhere/FDR test). Gate B: declare which used building
    blocks are forced-provenance. Gate C: dimensionless single-number targets have NO
    multi-observable interlock and tie no >=3 constants -> C will be 'none' unless a real
    interlock is declared. We do NOT fake an interlock; that's the honest signal.
    """
    # forced factors among the used blocks
    forced_used = [n for n in hit.used if n in FORCED_PROVENANCE]
    factors = [Factor(value=float(POOL[n]), provenance=FORCED_PROVENANCE[n],
                      appears_in=[FORCED_PROVENANCE[n]]) for n in forced_used]
    # free params = non-forced building blocks used (each unforced germ is a free choice)
    n_unforced = len(hit.used) - len(forced_used)

    germ_pool = {n: float(POOL[n]) for n in POOL}
    ss = SearchSpace(
        germ_pool=germ_pool,
        tol=max(rel_prec, 1e-4),
        target_sigma=sigma,
        n_digits_known=n_digits,
        n_targets_searched=n_targets_searched,
    )
    coeff = Coefficient(
        factors=factors,
        free_params=max(0, n_unforced),  # honest: each non-forced germ is a free knob
        target_value=hit.value,
        form_forced_independently=0,
    )
    # NO interlock declared (a single dimensionless number forces no 2nd observable and
    # ties no 3 constants) -> Gate C will FAIL 'none'. This is the honest default; we only
    # raise it where a genuine structural interlock exists (handled separately).
    il = Interlock(n_independent_observables=0, n_constants_tied=0, n_free_in_interlock=99)
    cand = Candidate(
        name=f"{hit.target}={hit.formula}",
        target_value=hit.target_value,
        relation_value=hit.value,
        search=ss, coefficient=coeff, interlock=il,
    )
    return validate(cand)


# Targets for Search 3
SEARCH3 = [
    "ckm_lambda", "ckm_A", "ckm_rhobar", "ckm_etabar",
    "ckm_theta12", "ckm_theta23", "ckm_theta13", "ckm_deltaCP",
    "pmns_sin2_12", "pmns_sin2_23", "pmns_sin2_13",
    "pmns_theta12", "pmns_theta23", "pmns_theta13", "pmns_deltaCP",
    "sin2_thetaW_MZ", "alpha_em_inv_0", "alpha_em_inv_MZ", "alpha_s_MZ",
]


def main():
    n_targets = len(SEARCH3)
    print(f"SEARCH 3 — MIXING + COUPLINGS  ({n_targets} targets, look-elsewhere x{n_targets})")
    print("=" * 90)
    grand_N = 0
    survivors = []
    real_puzzles = []
    for key in SEARCH3:
        try:
            val, sigma, rel_prec, n_digits = get(key)
        except Exception as ex:
            print(f"[skip {key}: {ex}]")
            continue
        val = float(val); sigma = float(sigma)
        N, hits = search_target(key, val, sigma, rel_prec, n_targets)
        grand_N += N
        print(f"\n### {key}  = {val:.6g}  (sigma={sigma:.2g}, rel_prec={rel_prec:.1e})")
        print(f"    N_expressions = {N:,} | near-hits (<max(3sig,0.3%)) = {len(hits)}")
        if not hits:
            print("    no expression within window -> nothing even to gate.")
            continue
        for h in hits[:5]:
            v = gate_hit(h, rel_prec, sigma, n_digits, n_targets)
            tag = v.status
            print(f"    {h.formula:42s} = {h.value:.6g}  "
                  f"relerr={h.rel_err:.2e} nsig={h.n_sigma:.2f}  -> {tag}")
            print(f"        A:{v.fdr.passed}(bits={v.fdr.bits:.1f}) "
                  f"B:{v.kernel.passed} C:{v.interlock.passed} | {v.fdr.tell[:70]}")
            if v.status == "CERTIFIED":
                survivors.append((key, h.formula, v))
            elif v.status == "REAL-PUZZLE-RE-LABELED":
                real_puzzles.append((key, h.formula, v))
    print("\n" + "=" * 90)
    print(f"GRAND TOTAL expressions searched (sum over targets): {grand_N:,}")
    print(f"CERTIFIED gate-survivors: {len(survivors)}")
    print(f"REAL-PUZZLE-RE-LABELED:   {len(real_puzzles)}")
    for k, f, v in survivors:
        print(f"   SURVIVOR: {k} = {f}")
    for k, f, v in real_puzzles:
        print(f"   REAL-PUZZLE: {k} = {f}")


if __name__ == "__main__":
    main()
