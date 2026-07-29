#!/usr/bin/env python3
r"""
clustering_local_density.py -- AUDIT LENS: CLUSTERING. Step 2 of 2: the DECISIVE question.

Step 1 (expected_count_audit.py) showed the naive model E[hits] = N*2w overpredicts observed
depth-10 hits by 125.0x aggregate, and that essentially ALL of that factor is DYNAMIC RANGE
(632 decades of ln|v| span => coarse log-density ~ N/125 per natural-log unit near the O(1)
targets), not fine clumping (observed/coarse-envelope = 1.00x aggregate).

THE DECISIVE QUESTION THIS SCRIPT ANSWERS. A 125x deficit of chances near a RANDOM point makes
the look-elsewhere threshold CONSERVATIVE. But clustering is a two-sided hazard: if the value set
clumps, a target that happens to SIT ON a clump gets MORE chances than N*2w/125 -- possibly more
than N*2w -- and the threshold becomes ANTI-CONSERVATIVE for exactly the target you care about.
Deciding requires three measurements, none of which can be replaced by argument:

  S2  ENSEMBLE FINE-SCALE STRUCTURE. Two-point correlation g(r) of the value set in log space,
      r = 1e-1 down to 1e-14 (the tight targets' windows are 1e-10). g(r) ~ 1 => locally Poisson
      at window scale => the coarse-envelope rate is the RIGHT rate at every scale the windows
      probe, including for the zero-hit tight targets where hits cannot be counted. g(r) >> 1 =>
      fractal/clumped => small-window rates are UNDERestimated by linear extrapolation, which is
      the anti-conservative failure mode (and is also the assumption inside gate/fdr.py's
      _poisson_e_chance, which rescales a +-10% band count linearly down to the tight window).

  S3  ARE THE MEASURED TARGETS IN DENSE OR SPARSE REGIONS? Per target, local count vs a
      MATCHED null: random probe points drawn log-uniformly in the same +-0.5 ln band, same
      relative window. Reports the target's percentile in that null.

  S4  WORST-CASE CLUMP TAIL. The threshold must survive a target that lands on the densest
      clump the set has, not just the median point. Distribution of enrichment over 20,000
      random probes; the max, in bits.

  S5  IS ARITHMETIC SIMPLICITY THE CLUMP LOCATION? (integers, small rationals, germ powers)
      -- i.e. WHICH targets, if any, are structurally at risk.

  S6  BITS VERDICT. Recompute BITS_RULE.py's threshold with the empirical rates and say whether
      it needs a penalty, with the number.

No hard-coded verdicts. Local-only. python3 audit_interlock/clustering_local_density.py
"""
from __future__ import annotations
import json
import math
import os
import sys
import time
from fractions import Fraction

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from exhaust import resolve_target                      # noqa: E402
from exhaust_parallel import sm_target_keys             # noqa: E402
from engine.scoring import measurement_tol              # noqa: E402
from targets.pdg_constants import HOLDOUT_KEYS          # noqa: E402

DDIR = os.path.join(ROOT, "results_grind", "depth_10")
VALS = os.path.join(DDIR, "values_merged.f64")
OUT = os.path.join(ROOT, "audit_interlock", "clustering_local_density.json")

RNG = np.random.default_rng(20260728)
R_COARSE = 0.5          # +-0.5 natural-log units == the coarse envelope scale (as in step 1)


def counts_in_rel_windows(lv: np.ndarray, probes: np.ndarray, h: float) -> np.ndarray:
    """# values with |v/probe - 1| <= h, computed in log space (ln(1+h) ~ h, exact form used)."""
    lo = np.log(probes * (1.0 - h))
    hi = np.log(probes * (1.0 + h))
    return (np.searchsorted(lv, hi, "right") - np.searchsorted(lv, lo, "left")).astype(np.int64)


def coarse_density(lv: np.ndarray, probes: np.ndarray, R: float = R_COARSE) -> np.ndarray:
    """values per natural-log unit in a +-R ln band around each probe."""
    lp = np.log(probes)
    n = (np.searchsorted(lv, lp + R, "right") - np.searchsorted(lv, lp - R, "left"))
    return n / (2.0 * R)


def main() -> int:
    bar = "=" * 106
    print(bar)
    print("CLUSTERING AUDIT step 2 -- does clustering make the bits threshold CONSERVATIVE or NOT?")
    print(bar)
    t0 = time.time()

    v = np.fromfile(VALS, dtype="<f8")
    v = v[np.isfinite(v) & (v != 0.0)]
    vs = np.sort(np.abs(v))
    del v
    N = vs.size
    lv = np.log(vs)
    print(f"\n  N (finite, nonzero, |v|) = {N:,}    ln|v| in [{lv[0]:.1f}, {lv[-1]:.1f}]")

    # ---------------- S1  degeneracy / duplicate structure -------------------------------
    print("\nS1  DEGENERACY STRUCTURE OF THE STORED float64 VALUE SET")
    print("-" * 106)
    d = np.diff(vs)
    n_exact_dup = int((d == 0.0).sum())
    print(f"      dedup is by mpmath 30-dps key, so float64 near-degeneracies survive:")
    print(f"      exact float64 duplicate adjacencies : {n_exact_dup:,} "
          f"({100.0*n_exact_dup/max(1, N-1):.3f}% of gaps)")
    dl = np.diff(lv)
    pos = dl[dl > 0]
    for qq in (0.001, 0.01, 0.1, 0.5):
        print(f"      log-gap quantile {qq:>6.3f} : {np.quantile(pos, qq):.3e} ln units "
              f"(= relative spacing)")
    del d, dl, pos

    # ---------------- S2  two-point correlation in log space ------------------------------
    print("\nS2  ENSEMBLE TWO-POINT CORRELATION g(r) IN LOG SPACE  (the fine-scale test)")
    print("-" * 106)
    LO, HI = -8.0, 9.0                      # ln band containing every committed target
    b0, b1 = int(np.searchsorted(lv, LO, "left")), int(np.searchsorted(lv, HI, "right"))
    xb = lv[b0:b1]
    M = xb.size
    print(f"      band ln|v| in [{LO}, {HI}] (all 21 targets lie inside): M = {M:,} values")
    # local density per point, estimated at scale R_G (>> the r values probed)
    R_G = 0.05
    rho_i = (np.searchsorted(lv, xb + R_G, "right")
             - np.searchsorted(lv, xb - R_G, "left")) / (2.0 * R_G)
    rho_sum = float(rho_i.sum())
    print(f"      per-point local density estimated at +-{R_G} ln; mean rho = "
          f"{rho_sum/M:,.0f} values per ln unit")
    print(f"\n      {'r [ln units]':>14}{'obs pairs(<r)':>16}{'exp Poisson':>14}{'g(r)':>9}"
          f"{'log2 g':>9}")
    print("      " + "-" * 62)
    g_rows = []
    for r in (1e-1, 3e-2, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14):
        right = np.searchsorted(lv, xb + r, "right") - (np.arange(b0, b1) + 1)
        obs = int(right.sum())
        exp = rho_sum * r
        g = obs / exp if exp > 0 else float("nan")
        g_rows.append(dict(r=r, obs=obs, exp=exp, g=g))
        l2 = math.log2(g) if g > 0 else float("-inf")
        print(f"      {r:>14.0e}{obs:>16,}{exp:>14,.1f}{g:>9.3f}{l2:>9.2f}")
    del rho_i, xb

    # ---------------- S3  per-target local density vs matched controls --------------------
    print("\nS3  DO THE MEASURED TARGETS SIT IN DENSE OR SPARSE REGIONS?  (matched-null percentile)")
    print("-" * 106)
    keys = sm_target_keys(include_holdout=True)
    NCTRL = 4000
    print(f"      For each target: count in its own real window w, and in a widened probe window")
    print(f"      h_probe (>= w, chosen so the null has usable statistics), vs {NCTRL:,}控 controls")
    print(f"      drawn log-uniformly in the SAME +-{R_COARSE} ln band. 'pct' = target's percentile.")
    print(f"\n      {'target':<18}{'w':>10}{'h_probe':>10}{'n(target)':>10}{'null mean':>11}"
          f"{'enrich':>8}{'pct':>7}{'log2 enr':>9}")
    print("      " + "-" * 88)
    s3 = []
    for k in keys:
        ts = resolve_target(k)
        tv = float(ts.value)
        w = measurement_tol(ts.pdg_target)
        rho = float(coarse_density(lv, np.array([tv]))[0])
        # widen the probe window until the matched null expects >= 30 values (usable statistics)
        h = w
        while 2.0 * h * rho < 30.0 and h < 0.05:
            h *= 2.0
        lp = math.log(tv)
        ctrl = np.exp(RNG.uniform(lp - R_COARSE, lp + R_COARSE, NCTRL))
        nc = counts_in_rel_windows(lv, ctrl, h)
        nt = int(counts_in_rel_windows(lv, np.array([tv]), h)[0])
        mu = float(nc.mean())
        enr = nt / mu if mu > 0 else float("nan")
        pct = 100.0 * float((nc <= nt).mean())
        s3.append(dict(key=k, w=w, h=h, n_target=nt, null_mean=mu, enrich=enr, pct=pct,
                       rho=rho, holdout=k in HOLDOUT_KEYS))
        l2 = math.log2(enr) if enr and enr > 0 else float("-inf")
        print(f"      {k:<18}{w:>10.1e}{h:>10.1e}{nt:>10,}{mu:>11.1f}{enr:>8.2f}{pct:>7.1f}"
              f"{l2:>9.2f}")
    enrs = np.array([r["enrich"] for r in s3 if r["enrich"] == r["enrich"]])
    print(f"\n      enrichment over the {len(enrs)} targets: min {enrs.min():.2f}  "
          f"median {np.median(enrs):.2f}  max {enrs.max():.2f}   "
          f"(1.00 = target sits exactly on its own log-envelope)")
    print(f"      targets ABOVE the null median (pct>50): "
          f"{sum(1 for r in s3 if r['pct'] > 50)}/{len(s3)};  "
          f"above 95th pct: {sum(1 for r in s3 if r['pct'] > 95)}/{len(s3)}")

    # ---------------- S4  worst-case clump tail ------------------------------------------
    print("\nS4  WORST-CASE CLUMP TAIL -- how dense is the DENSEST place a target could land?")
    print("-" * 106)
    NBIG = 20000
    s4 = []
    for h in (1e-2, 1e-3, 1e-5):
        probes = np.exp(RNG.uniform(-8.0, 9.0, NBIG))
        rho = coarse_density(lv, probes)
        n = counts_in_rel_windows(lv, probes, h)
        exp = 2.0 * h * rho
        ok = exp > 0
        enr = n[ok] / exp[ok]
        qs = np.quantile(enr, [0.5, 0.9, 0.99, 0.999, 1.0])
        naive_ratio = float(np.median(N * 2.0 * h / np.maximum(n[ok], 0.5)))
        s4.append(dict(h=h, q50=qs[0], q90=qs[1], q99=qs[2], q999=qs[3], qmax=qs[4],
                       frac_over_125=float((enr > 125.0).mean()),
                       median_naive_over_obs=naive_ratio))
        print(f"      h={h:.0e}: enrichment over envelope  median {qs[0]:.2f}  p90 {qs[1]:.2f}  "
              f"p99 {qs[2]:.2f}  p99.9 {qs[3]:.2f}  MAX {qs[4]:.2f}  "
              f"(= {math.log2(max(qs[4],1e-9)):+.2f} bits)")
        print(f"                fraction of probes whose LOCAL rate exceeds the NAIVE N*2w rate "
              f"(enr > 125): {100.0*s4[-1]['frac_over_125']:.4f}%")

    # ---------------- S5  is arithmetic simplicity the clump location? -------------------
    print("\nS5  WHERE ARE THE CLUMPS? arithmetically simple values vs random probes  (h=1e-3)")
    print("-" * 106)
    h = 1e-3
    simple = []
    for p in range(1, 13):
        for q in range(1, 13):
            fr = Fraction(p, q)
            if 0.001 <= float(fr) <= 8000.0:
                simple.append((f"{p}/{q}", float(fr)))
    simple = sorted({s[1]: s for s in simple}.values(), key=lambda s: s[1])
    sv = np.array([s[1] for s in simple])
    rho_s = coarse_density(lv, sv)
    n_s = counts_in_rel_windows(lv, sv, h)
    enr_s = n_s / np.maximum(2.0 * h * rho_s, 1e-12)
    probes = np.exp(RNG.uniform(math.log(sv.min()), math.log(sv.max()), 20000))
    rho_r = coarse_density(lv, probes)
    n_r = counts_in_rel_windows(lv, probes, h)
    enr_r = n_r[rho_r > 0] / (2.0 * h * rho_r[rho_r > 0])
    print(f"      {len(sv)} small rationals p/q (p,q<=12) vs {len(enr_r):,} log-uniform probes:")
    print(f"        simple-rational enrichment: median {np.median(enr_s):.2f}  "
          f"mean {enr_s.mean():.2f}  max {enr_s.max():.2f}")
    print(f"        random-probe   enrichment: median {np.median(enr_r):.2f}  "
          f"mean {enr_r.mean():.2f}  max {enr_r.max():.2f}")
    top = sorted(zip(enr_s, [s[0] for s in simple], n_s), reverse=True)[:8]
    print(f"        densest simple rationals: "
          + ", ".join(f"{nm}({e:.1f}x,n={int(nn)})" for e, nm, nn in top))
    # which committed targets are within a real window of a simple rational?
    near = []
    for r in s3:
        tv = float(resolve_target(r["key"]).value)
        j = int(np.argmin(np.abs(sv / tv - 1.0)))
        rel = abs(sv[j] / tv - 1.0)
        if rel <= max(r["w"], 1e-3):
            near.append((r["key"], simple[j][0], rel))
    print(f"        committed targets within max(w,1e-3) of a small rational: "
          + (", ".join(f"{k}~{nm} (rel {rl:.1e})" for k, nm, rl in near) if near else "NONE"))

    # ---------------- S6  the bits verdict ------------------------------------------------
    print("\nS6  BITS VERDICT -- what the empirical rate does to BITS_RULE's threshold")
    print("-" * 106)
    BASE, D0, MARGIN = 30.0, 4, 10.0
    Nd = BASE ** (10 - D0)
    cost = math.log2(Nd)
    # empirical per-target credit: naive rate 2w vs empirical local rate (2w * rho / N)
    creds = []
    for r in s3:
        p_naive = 2.0 * r["w"]
        p_emp = 2.0 * r["w"] * r["rho"] / N * max(r["enrich"], 1e-9) if r["enrich"] == r["enrich"] \
            else 2.0 * r["w"] * r["rho"] / N
        creds.append((r["key"], math.log2(p_naive / p_emp)))
    cred = np.array([c for _, c in creds])
    print(f"      per-target CREDIT = log2(naive rate / empirical local rate), i.e. how many bits")
    print(f"      of look-elsewhere BITS_RULE over-charges per interlocked target:")
    print(f"        min {cred.min():.2f}  median {np.median(cred):.2f}  max {cred.max():.2f} bits")
    worst_clump_bits = math.log2(max(s4[1]["qmax"], 1e-9))
    net_worst = float(np.median(cred)) - worst_clump_bits
    print(f"      worst observed clump (h=1e-3, {len(enr_r):,} probes) = "
          f"{s4[1]['qmax']:.2f}x envelope = {worst_clump_bits:+.2f} bits of ANTI-conservative risk")
    print(f"      NET at the median target if it landed on the worst clump in the set: "
          f"{net_worst:+.2f} bits")
    print(f"\n      BITS_RULE at depth 10: log2(N(10)) = {cost:.1f}, needed = {cost+MARGIN:.1f} bits.")
    print(f"      With the empirical rate the same k-target interlock earns an EXTRA "
          f"{np.median(cred):.1f} bits per target,")
    print(f"      so the committed threshold is CONSERVATIVE by ~{np.median(cred):.1f}k bits "
          f"(k = # interlocked targets)")
    print(f"      unless a target sits on a clump denser than {2**np.median(cred):.0f}x its "
          f"envelope; the densest place")
    print(f"      found anywhere in {len(enr_r):,} probes is {s4[1]['qmax']:.1f}x.")

    with open(OUT, "w") as f:
        json.dump(dict(N=int(N), g_of_r=g_rows, per_target=s3, clump_tail=s4,
                       simple_rational_median_enrich=float(np.median(enr_s)),
                       random_probe_median_enrich=float(np.median(enr_r)),
                       credit_bits=dict(min=float(cred.min()), median=float(np.median(cred)),
                                        max=float(cred.max())),
                       worst_clump_bits=worst_clump_bits, net_worst_bits=net_worst,
                       n_exact_dup=n_exact_dup), f, indent=1)
    print(f"\n  wrote {OUT}\n  wall {time.time()-t0:.1f}s")
    print(bar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
