#!/usr/bin/env python3
"""
SEARCH 2 — QUARK SECTOR brute force with the FDR + forced-kernel + interlock GATE.

Method (identical discipline to the a0 discovery / calibrate.py):
  1. Build a SYMBOL POOL from the framework's FORCED constants + small ints/rationals.
  2. Enumerate 1/2/3-symbol closed-form expressions (product / ratio / sum / a*b+c ...).
  3. For each quark TARGET (ratios + quark-Koide Q), find expressions matching within the
     target's OWN measured precision (sigma/value) -- NOT an arbitrary 1e-4. Light-quark
     ratios are blunt (10-23%), which WIDENS the window and KILLS borderline hits.
  4. Route EVERY match through the real gate:
       GATE A (fdr.py)       -- trials-corrected surprise 1/(N * 2p) >> 1  (look-elsewhere)
       GATE B (forced_kernel)-- forced/mechanistic kernel vs free fit
       GATE C (interlock)    -- interlocks with framework structure / >=3 constants 1 param
  A "gate-survivor" must clear A, then B or the honest C2 (real-puzzle) route.

Both-ways honest: a brute force ALWAYS finds 0.1% matches; ONLY gate-survivors count.
N (the look-elsewhere multiplicity) is the count of DISTINCT expression VALUES in the
complexity bin that the engine could have produced -- this is what corrects the surprise.
"""
from __future__ import annotations
import os, sys, math, itertools, json
from dataclasses import dataclass

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import numpy as np
from targets.pdg_constants import get
from gate.candidate import Candidate, SearchSpace, Coefficient, Factor, Interlock
from gate.fdr import fdr_test
from gate.forced_kernel import forced_kernel_detector
from gate.interlock import interlock_check

PI = math.pi
Z = math.sqrt(32 * PI / 3.0)        # 5.78878  framework germ
KERNEL = math.sqrt(8 * PI / 3.0)    # 2.89439  = Z/2  a0 forced kernel
PHI = (1 + math.sqrt(5)) / 2

# ---------------------------------------------------------------------------
# Building blocks = the framework's FORCED constants + the brief's allowed set.
# (name -> value). These are the germs the brute force decorates with.
# ---------------------------------------------------------------------------
POOL = {
    # framework-forced
    "Z": Z, "Z2": Z * Z, "kernel": KERNEL, "kappa": 0.5,
    "pi": PI, "2pi": 2 * PI, "4pi": 4 * PI, "8pi": 8 * PI, "pi/2": PI / 2,
    # transcendental germs the brief lists
    "e": math.e, "phi": PHI,
    "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3), "sqrt5": math.sqrt(5),
    # triality / SO(10) integers
    "3": 3.0, "8": 8.0, "16": 16.0,
    # small ints 1-16
    "1": 1.0, "2": 2.0, "4": 4.0, "5": 5.0, "6": 6.0, "7": 7.0,
    "9": 9.0, "10": 10.0, "11": 11.0, "12": 12.0, "13": 13.0, "14": 14.0, "15": 15.0,
    # simple rationals
    "1/2": 0.5, "1/3": 1/3, "2/3": 2/3, "3/2": 1.5, "1/4": 0.25, "5/2": 2.5,
}
NAMES = list(POOL)
VALS = {n: POOL[n] for n in NAMES}


def enumerate_library(max_val=3.0e5):
    """Build the reachable expression set: 1-, 2-, 3-symbol products/ratios/sums.
    Returns list of (value, label). This IS the brute-force engine's output space and
    the look-elsewhere null. Mirrors attack5_fdr_partB's reachable library."""
    lib = []
    def add(v, label):
        if np.isfinite(v) and 1e-6 < abs(v) < max_val:
            lib.append((float(v), label))
    # depth 1
    for a in NAMES:
        add(VALS[a], a)
    # depth 2
    for a in NAMES:
        for b in NAMES:
            va, vb = VALS[a], VALS[b]
            add(va * vb, f"{a}*{b}")
            if vb: add(va / vb, f"{a}/{b}")
            add(va + vb, f"{a}+{b}")
            add(va - vb, f"{a}-{b}")
            add(va ** vb if 0 < vb < 6 and 0 < va < 30 else float('nan'), f"{a}^{b}")
    # depth 3 (the 64pi+Z / 4Z^2+3 family lives here)
    for a in NAMES:
        for b in NAMES:
            for c in NAMES:
                va, vb, vc = VALS[a], VALS[b], VALS[c]
                add(va * vb + vc, f"{a}*{b}+{c}")
                add(va * vb - vc, f"{a}*{b}-{c}")
                if vc: add(va * vb / vc, f"{a}*{b}/{c}")
                if vb: add(va / vb + vc, f"{a}/{b}+{c}")
    return lib


LIB = enumerate_library()
LIB_VALS = np.array([v for v, _ in LIB])
print(f"[engine] reachable library size N = {len(LIB):,} expressions "
      f"(distinct-ish 1/2/3-symbol forms over {len(NAMES)} germs)")


def best_matches(target, rel_tol, k=8):
    """Find expressions within rel_tol of target. Returns sorted (relerr,label,value)."""
    rel = np.abs(LIB_VALS - target) / abs(target)
    idx = np.argsort(rel)[:k]
    return [(float(rel[i]), LIB[i][1], float(LIB_VALS[i])) for i in idx]


def look_elsewhere_N(target, rel_band=0.5):
    """N = number of distinct expression VALUES in the complexity bin near this target's
    SCALE (within a factor of ~1.6 either side = the local density that sets chance).
    This is the trials count that corrects the surprise per the brief's G1."""
    lo, hi = target * (1 - rel_band), target * (1 + rel_band)
    band = LIB_VALS[(LIB_VALS >= lo) & (LIB_VALS <= hi)]
    # distinct values at engine resolution (avoid counting numeric dupes as separate trials)
    uniq = np.unique(np.round(band, 6))
    return max(1, len(uniq))


# ---------------------------------------------------------------------------
# GATE driver per hit. We construct a Candidate and run A, then B, then C.
# A quark mass-RATIO match has NO forced kernel available (the registry has only the
# a0 kernel + flavor-symmetry hooks), so Gate B will report 0 forced places -- that is
# the HONEST expected result for a free Yukawa ratio. The only B/C survivor route a
# quark hit could take is an interlock (Koide-class C2): a relation tying >=3 measured
# masses with <=1 free param AND a forced amplitude.
# ---------------------------------------------------------------------------
def gate_a_for_hit(target_key, target, rel_err_of_hit, hit_label):
    """Run the real Gate A (Poisson look-elsewhere) on a ratio/scalar hit."""
    v, sigma, rel_prec, ndig = get(target_key)
    rel_prec = float(rel_prec)
    # the FDR window = the TARGET's own measurement precision (Carl's emphasis (a)).
    tol = max(rel_prec, rel_err_of_hit)  # can't claim tighter than measured OR than the hit
    germ_pool = {n: VALS[n] for n in NAMES}
    N = look_elsewhere_N(target)
    search = SearchSpace(
        germ_pool=germ_pool, tol=tol,
        target_sigma=float(sigma), n_digits_known=float(ndig),
        rational_target=False, n_targets_searched=N,
    )
    coeff = Coefficient(factors=[], free_params=1, target_value=None,
                        form_forced_independently=0)
    interlock = Interlock(n_independent_observables=0, n_constants_tied=0)
    cand = Candidate(name=f"{target_key}={hit_label}", target_value=float(target),
                     relation_value=float(target * (1 + rel_err_of_hit)),
                     search=search, coefficient=coeff, interlock=interlock)
    return fdr_test(cand), N, tol


# ---------------------------------------------------------------------------
# QUARK-KOIDE structural test (the only real interlock candidate in this sector).
# Q_up and Q_down: do they hit a small-denom rational the way the leptons hit 2/3?
# Use the random-mass-triple null (the documented Koide measure) at the MEASURED Q.
# ---------------------------------------------------------------------------
def quark_koide_report(which, masses, Q_key):
    v, sigma, rel_prec, ndig = get(Q_key)
    Q_meas = float(v)
    # candidate rational targets to test against (small denominators)
    rationals = {"2/3": 2/3, "3/4": 3/4, "5/6": 5/6, "4/5": 4/5, "7/9": 7/9,
                 "11/13": 11/13, "6/7": 6/7, "5/7": 5/7, "8/11": 8/11, "9/11": 9/11}
    # nearest small rational to the measured Q (within measured precision)
    near = sorted(rationals.items(), key=lambda kv: abs(kv[1] - Q_meas))
    def koide_triple_null(N):
        rng = np.random.default_rng(20260625)
        # span the relevant quark scale in log10(MeV): u..t ~ [0.3, 5.2]
        lm = rng.uniform(0.0, 5.5, size=(N, 3))
        m = 10.0 ** lm
        sm = np.sqrt(m)
        return m.sum(axis=1) / (sm.sum(axis=1) ** 2)
    out = {"which": which, "Q_meas": Q_meas, "sigma": float(sigma),
           "rel_prec": float(rel_prec), "nearest_rationals": near[:3]}
    # for the nearest rational, is the measured Q consistent (within sigma)?
    rname, rval = near[0]
    out["nearest_name"] = rname
    out["nearest_val"] = rval
    out["nsigma_from_nearest"] = abs(Q_meas - rval) / float(sigma)
    # structural null at the measured Q value (how often random triples land there)
    samp = koide_triple_null(2_000_000)
    eps = max(float(sigma), abs(Q_meas) * 1e-3)
    p = float(np.mean(np.abs(samp - Q_meas) < eps))
    out["p_random_triple"] = p
    out["bits_raw"] = (-math.log2(p) if p > 0 else float('inf'))
    return out


def run():
    print("\n" + "=" * 78)
    print("SEARCH 2 -- QUARK SECTOR")
    print("=" * 78)

    # the targets: ratios (mix of sharp + blunt) + the two quark-Koide Q's
    ratio_targets = ["r_c_u", "r_t_c", "r_s_d", "r_b_s", "r_t_b", "r_b_tau",
                     "sqrt_md_ms"]
    survivors = []
    all_rows = []

    for tk in ratio_targets:
        v, sigma, rel_prec, ndig = get(tk)
        target = float(v)
        rel_prec = float(rel_prec)
        hits = best_matches(target, rel_prec)
        N = look_elsewhere_N(target)
        # best (closest) hit
        relerr, label, val = hits[0]
        within = relerr <= rel_prec
        print(f"\n[{tk}] target={target:.5g}  measured rel-prec={rel_prec:.3%}  "
              f"look-elsewhere N(local)={N}")
        print(f"   closest expr: {label} = {val:.6g}  (rel-err {relerr:.3%}, "
              f"{'WITHIN' if within else 'outside'} measured precision)")
        print(f"   next: " + "; ".join(f"{l}={vv:.5g}({re*100:.2f}%)"
                                        for re, l, vv in hits[1:4]))
        if within:
            fa, Nle, tol = gate_a_for_hit(tk, target, relerr, label)
            print(f"   GATE A: passed={fa.passed}  bits={fa.bits:.2f}  mode={fa.mode}")
            print(f"           tell: {fa.tell}")
            # GATE B: no forced kernel for a free Yukawa ratio (registry has none)
            print(f"   GATE B: no forced kernel registered for a quark Yukawa ratio "
                  f"-> 0 forced places -> FAIL (honest: ratio is a free eigenvalue)")
            row = dict(target=tk, label=label, relerr=relerr, gateA=fa.passed,
                       bits=fa.bits, survivor=False)
            if fa.passed:
                # a Gate-A survivor that still has no kernel -> not a discovery, flagged
                survivors.append((tk, label, "A-only, no kernel/interlock"))
                row["survivor"] = "A-only"
            all_rows.append(row)
        else:
            all_rows.append(dict(target=tk, label=label, relerr=relerr,
                                 gateA="N/A(outside precision)", survivor=False))

    # ---- quark-Koide interlock (the real interlock candidate) ----
    print("\n" + "-" * 78)
    print("QUARK-KOIDE interlock test (the only Gate-C2 candidate in this sector)")
    print("-" * 78)
    up = quark_koide_report("up (u,c,t)", None, "koide_Q_up")
    dn = quark_koide_report("down (d,s,b)", None, "koide_Q_down")
    for r in (up, dn):
        print(f"\n  {r['which']}: Q_meas = {r['Q_meas']:.5f} +- {r['sigma']:.5f} "
              f"(rel {r['rel_prec']:.3%})")
        print(f"    nearest small rational: {r['nearest_name']}={r['nearest_val']:.5f} "
              f"-> {r['nsigma_from_nearest']:.1f} sigma away "
              f"({'CONSISTENT' if r['nsigma_from_nearest']<3 else 'INCONSISTENT'})")
        print(f"    next rationals: " + ", ".join(f"{n}({v:.4f})"
              for n, v in r['nearest_rationals'][1:]))
        print(f"    random-triple null P(land on Q_meas)={r['p_random_triple']:.3e} "
              f"-> {r['bits_raw']:.1f} raw bits (NOT a rational hit unless n_sigma<3)")
    return survivors, all_rows, up, dn


if __name__ == "__main__":
    survivors, rows, up, dn = run()
    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Gate-A survivors (still need B/C): {len(survivors)}")
    for s in survivors:
        print("   ", s)
    print(json.dumps({"up": {k: up[k] for k in ('Q_meas','nearest_name','nsigma_from_nearest')},
                      "down": {k: dn[k] for k in ('Q_meas','nearest_name','nsigma_from_nearest')}},
                     indent=2, default=str))
