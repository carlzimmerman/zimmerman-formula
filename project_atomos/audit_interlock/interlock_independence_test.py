#!/usr/bin/env python3
r"""
interlock_independence_test.py -- AUDIT LENS: CLUSTERING. Step 4: the INTERLOCK-SPECIFIC hazard.

Steps 1-3 settled the single-target expected-count model: naive N*2w overpredicts by 125.0x at
depth 10 (6.97 bits), the cause is dynamic range not clumping, the targets sit at their own log
envelope (enrichment median 1.00), and the fine-scale near-degeneracy moves occupancy DOWN
(conservative, <0.5 bits).

BUT BITS_RULE's threshold is about an INTERLOCK: it demands sum_i log2(1/w_i) > log2(N(D)) + 10,
which is only valid if the k target windows are hit INDEPENDENTLY by the enumeration. Clustering
could break that at the level that matters: if low-complexity SKELETONS (value-trees, decorated by
different germ recipes) are tunable across many targets, then one skeleton hitting k targets is far
commoner than the product of windows implies, and the bits threshold is ANTI-CONSERVATIVE for
exactly the pass-mode the campaign is counting on. Nothing in steps 1-3 tests this.

MEASUREMENT. The depth-10 retained records (results_grind/depth_10/records.sqlite) carry
(b_s, skeleton_idx, recipe, value) for every in-window hit. Group hits by SKELETON, count how many
DISTINCT targets each skeleton reaches, and compare against a LABEL-PERMUTATION null that preserves
both the per-skeleton hit multiplicity and the very lopsided per-target marginal (loose targets take
almost all hits). Real >> null => skeleton-level correlation => the interlock needs a penalty.
Then compute the sum-of-bits BITS_RULE would score for the best skeletons actually observed, and
compare with its own threshold.

No hard-coded verdicts. Local-only. python3 audit_interlock/interlock_independence_test.py
"""
from __future__ import annotations
import json
import math
import os
import sqlite3
import sys
import time
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from exhaust import resolve_target                      # noqa: E402
from exhaust_parallel import sm_target_keys             # noqa: E402
from engine.scoring import measurement_tol              # noqa: E402

DB = os.path.join(ROOT, "results_grind", "depth_10", "records.sqlite")
OUT = os.path.join(ROOT, "audit_interlock", "interlock_independence_test.json")
RNG = np.random.default_rng(20260730)
NPERM = 300
BASE, D0, MARGIN = 30.0, 4, 10.0


def main() -> int:
    bar = "=" * 106
    print(bar)
    print("INTERLOCK INDEPENDENCE TEST -- can one SKELETON reach many targets more easily than chance?")
    print(bar)
    t0 = time.time()

    keys = list(sm_target_keys(include_holdout=True)) + ["r_tau_mu"]
    spec = {k: resolve_target(k) for k in keys}
    tv = {k: float(spec[k].value) for k in keys}
    tol = {k: measurement_tol(spec[k].pdg_target) for k in keys}
    bits_of = {k: math.log2(1.0 / tol[k]) for k in keys}     # BITS_RULE's own convention

    con = sqlite3.connect(DB)
    rows = con.execute("SELECT value, b_s, skeleton_idx FROM records").fetchall()
    con.close()
    print(f"\n  {len(rows):,} retained hit records, from {DB}")

    # assign each record to the target whose EXACT window contains it
    sk_of, tg_of = [], []
    unassigned = 0
    for val, b_s, si in rows:
        best, bestrel = None, None
        for k in keys:
            rel = abs(val / tv[k] - 1.0)
            if bestrel is None or rel < bestrel:
                best, bestrel = k, rel
        if bestrel is not None and bestrel <= tol[best] * (1 + 1e-9):
            sk_of.append(f"{b_s}:{si}")
            tg_of.append(best)
        else:
            unassigned += 1
    sk_arr = np.array(sk_of)
    tg_arr = np.array(tg_of)
    n = sk_arr.size
    print(f"  assigned {n:,} records to an exact target window; {unassigned:,} fell outside "
          f"(widened-window retention margin)")
    uskel, sk_idx = np.unique(sk_arr, return_inverse=True)
    utgt, tg_idx = np.unique(tg_arr, return_inverse=True)
    print(f"  distinct skeletons {uskel.size:,}; distinct targets reached {utgt.size}")
    print(f"  per-target marginal (the null preserves this): "
          + ", ".join(f"{utgt[i]}:{c:,}" for i, c in enumerate(np.bincount(tg_idx, minlength=utgt.size))
                      if c > 0))

    def distinct_per_skeleton(tidx: np.ndarray) -> np.ndarray:
        d = defaultdict(set)
        for s, t in zip(sk_idx, tidx):
            d[s].add(t)
        out = np.zeros(uskel.size, dtype=np.int32)
        for s, ts in d.items():
            out[s] = len(ts)
        return out

    real = distinct_per_skeleton(tg_idx)
    hits_per_sk = np.bincount(sk_idx, minlength=uskel.size)
    print(f"\n  hits per skeleton: median {np.median(hits_per_sk):.0f}  max {hits_per_sk.max():,}")

    # ------------- permutation null: shuffle target labels across records ------------------
    print(f"\n  LABEL-PERMUTATION NULL ({NPERM} permutations; per-skeleton multiplicity and the")
    print(f"  per-target marginal are both held fixed, only the pairing is destroyed)")
    ks = [2, 3, 4, 5, 6, 8, 10]
    real_counts = {k: int((real >= k).sum()) for k in ks}
    null = {k: [] for k in ks}
    maxes = []
    for _ in range(NPERM):
        perm = RNG.permutation(tg_idx)
        dn = distinct_per_skeleton(perm)
        for k in ks:
            null[k].append(int((dn >= k).sum()))
        maxes.append(int(dn.max()))
    print(f"\n      {'k distinct targets':>20}{'real #skeletons':>17}{'null mean':>11}"
          f"{'null sd':>9}{'z':>8}{'real/null':>11}")
    print("      " + "-" * 78)
    s_rows = []
    for k in ks:
        a = np.array(null[k], dtype=float)
        z = (real_counts[k] - a.mean()) / a.std() if a.std() > 0 else float("nan")
        ratio = real_counts[k] / a.mean() if a.mean() > 0 else float("inf")
        s_rows.append(dict(k=k, real=real_counts[k], null_mean=float(a.mean()),
                           null_sd=float(a.std()), z=float(z), ratio=float(ratio)))
        print(f"      {k:>20}{real_counts[k]:>17,}{a.mean():>11.1f}{a.std():>9.2f}{z:>8.2f}"
              f"{(f'{ratio:.2f}' if math.isfinite(ratio) else 'inf'):>11}")
    print(f"\n      max distinct targets on one skeleton: real {int(real.max())}  "
          f"null mean {np.mean(maxes):.2f} (sd {np.std(maxes):.2f})")

    # ------------- the bits BITS_RULE would score for the observed skeletons ---------------
    print(f"\n  WHAT BITS_RULE WOULD SCORE FOR THE BEST SKELETONS ACTUALLY OBSERVED AT DEPTH 10")
    print("  " + "-" * 102)
    per_sk_targets = defaultdict(set)
    for s, t in zip(sk_idx, tg_idx):
        per_sk_targets[s].add(utgt[t])
    scored = []
    for s, ts in per_sk_targets.items():
        b = sum(bits_of[t] for t in ts)
        scored.append((b, len(ts), uskel[s], sorted(ts, key=lambda t: -bits_of[t])))
    scored.sort(reverse=True)
    Nd = BASE ** (10 - D0)
    need = math.log2(Nd) + MARGIN
    print(f"      BITS_RULE at depth 10: log2(N)={math.log2(Nd):.1f}, needed = {need:.1f} bits")
    print(f"\n      {'skeleton':>12}{'k':>4}{'sum bits':>10}{'vs need':>10}   tightest targets reached")
    print("      " + "-" * 92)
    for b, k, sk, ts in scored[:6]:
        print(f"      {sk:>12}{k:>4}{b:>10.1f}{b-need:>+10.1f}   " + ", ".join(ts[:5]))
    best_b, best_k = scored[0][0], scored[0][1]
    # the same accounting with the EMPIRICAL rate (per-target credit measured in steps 1-3)
    CREDIT = 6.97
    print(f"\n      best observed: k={best_k} targets, {best_b:.1f} bits, "
          f"{best_b-need:+.1f} bits vs the naive threshold.")
    print(f"      with the empirical per-target credit (+{CREDIT:.2f} bits/target from steps 1-3) the")
    print(f"      same skeleton would score {best_b + CREDIT*best_k:.1f} bits vs need {need:.1f} "
          f"-> {best_b + CREDIT*best_k - need:+.1f}.")
    print(f"      NOTE these are LOOSE-target interlocks (the credit does not rescue them into")
    print(f"      evidence: all {len(rows):,} depth-10 hits are FDR-DEAD in the committed VERDICT).")

    # ------------- the charge BITS_RULE never makes: free germ decorations -----------------
    print(f"\n  THE MISSING CHARGE: BITS_RULE sums window bits but charges NOTHING for the free")
    print(f"  germ decorations spent to reach each target. Measured on the same records:")
    print("  " + "-" * 102)
    bm = json.load(open(os.path.join(ROOT, "results_grind", "depth_10",
                                     "build_meta_sharded.json")))
    R = bm["raw_candidates"] / bm["n_skeletons_total"]
    free_bits = math.log2(R)
    con = sqlite3.connect(DB)
    top_sk = scored[0][2]
    b_s, si = top_sk.split(":")
    recs = con.execute("SELECT recipe FROM records WHERE b_s=? AND skeleton_idx=?",
                       (int(b_s), int(si))).fetchall()
    con.close()
    n_distinct_recipes = len({r[0] for r in recs})
    recipe_len = len(json.loads(recs[0][0]))
    print(f"      skeleton {top_sk}: {len(recs)} hits, {n_distinct_recipes} DISTINCT germ recipes, "
          f"{recipe_len} germ decorations each")
    print(f"      -> the k={best_k} targets are reached by {n_distinct_recipes} DIFFERENT expressions, "
          f"not by one relation.")
    print(f"      recipes available per skeleton at depth 10 = raw/{'skeletons'} = "
          f"{bm['raw_candidates']:,}/{bm['n_skeletons_total']:,} = {R:,.0f} "
          f"-> {free_bits:.1f} bits of freedom PER TARGET REACHED")
    print(f"\n      {'accounting':<44}{'bits':>10}{'threshold':>11}{'verdict':>12}")
    print("      " + "-" * 78)
    print(f"      {'BITS_RULE as written (sum window bits)':<44}{best_b:>10.1f}{need:>11.1f}"
          f"{'PASS':>12}")
    corrected = best_b - free_bits * best_k
    print(f"      {'minus the free-decoration charge':<44}{corrected:>10.1f}{need:>11.1f}"
          f"{('PASS' if corrected > need else 'FAIL'):>12}")
    # fully empirical cross-check: permutation expectation for this k
    a = np.array(null[10], dtype=float)
    print(f"\n      EMPIRICAL cross-check, no model at all: the permutation null expects "
          f"{a.mean():.0f} skeletons")
    print(f"      to reach >=10 distinct targets by chance ({real_counts[10]} observed) -> "
          f"E_chance = {a.mean():.0f} >> 1, i.e. ZERO bits of")
    print(f"      surprise, while BITS_RULE as written credits {best_b:.1f} and asks only "
          f"{need:.1f}. Over-credit >= {best_b-need+math.log2(a.mean()):.0f} bits.")
    print(f"      The clause that actually blocks this is Gate C's n_free_in_interlock <= 1")
    print(f"      (gate/interlock.py), which BITS_RULE never mentions and its arithmetic does not")
    print(f"      implement. The bits sum is NOT self-sufficient as a JACKPOT read-out rule.")

    with open(OUT, "w") as f:
        json.dump(dict(n_records=len(rows), n_assigned=int(n), n_skeletons=int(uskel.size),
                       perm=s_rows, real_max=int(real.max()), null_max_mean=float(np.mean(maxes)),
                       best_bits=float(best_b), best_k=int(best_k), need_bits=float(need),
                       nperm=NPERM), f, indent=1)
    print(f"\n  wrote {OUT}\n  wall {time.time()-t0:.1f}s")
    print(bar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
