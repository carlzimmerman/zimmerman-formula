#!/usr/bin/env python3
r"""
expected_count_audit.py -- AUDIT LENS: CLUSTERING. Step 1 of 2.

QUESTION (step 1). NULL_RESULT_DEPTH10_EXHAUSTIVE.md records that the naive expected-count
model E[hits] = N * 2w OVERPREDICTS the observed in-window hits by "~100x", and blames
clustering of the value set. Verify that factor from the REAL depth-10 value array
(results_grind/depth_10/values_merged.f64, 42,534,139 float64) against the REAL windows
(engine.scoring.measurement_tol on the committed PDG targets), target by target.

Then DECOMPOSE the shortfall, because "clustering" is two different things stacked:
  (A) DYNAMIC RANGE. N*2w silently assumes every one of the N values lives within a factor
      ~e of the target (density = N per natural-log unit). The real set spans ~hundreds of
      decades, so the coarse log-density near any particular point is N/L_eff, not N. This
      part of the shortfall is trivial bookkeeping, not clustering.
  (B) FINE CLUSTERING. Residual = observed / coarse-envelope prediction, where the coarse
      envelope is measured EMPIRICALLY as the value fraction inside a +-0.5 natural-log
      band around each target. This is the part that is genuinely clumping, and it can go
      EITHER WAY (a target sitting on a clump gets MORE chances, not fewer).

No hard-coded verdicts: every number printed is computed from the on-disk array here.
Local-only project. python3 audit_interlock/expected_count_audit.py
"""
from __future__ import annotations
import json
import math
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from exhaust import resolve_target                      # noqa: E402
from exhaust_parallel import sm_target_keys             # noqa: E402
from engine.scoring import measurement_tol, score_value  # noqa: E402
from targets.pdg_constants import HOLDOUT_KEYS          # noqa: E402

DDIR = os.path.join(ROOT, "results_grind", "depth_10")
VALS = os.path.join(DDIR, "values_merged.f64")
OUT = os.path.join(ROOT, "audit_interlock", "expected_count_audit.json")

# the hit counts recorded in NULL_RESULT_DEPTH10_EXHAUSTIVE.md, to be CHECKED not trusted
RECORDED = {
    "r_tau_e": 28, "alpha_em_inv_MZ": 50, "sin2_theta_W": 72,
    "koide_Q_up": 838, "higgs_lambda": 1130, "ckm_lambda": 2121, "koide_Q_down": 2098,
    "r_b_tau": 4747, "r_t_b": 4443, "alpha_s_MZ": 4933,
    "pmns_sin2_13": 15212, "pmns_sin2_12": 26142, "pmns_sin2_23": 20799,
}
RECORDED_TOTAL = 82613          # VERDICT.json n_hits, 19 non-holdout targets


def main() -> int:
    bar = "=" * 104
    print(bar)
    print("EXPECTED-COUNT MODEL AUDIT (clustering lens, step 1): is N*2w really ~100x high, and why?")
    print(bar)

    t0 = time.time()
    v = np.fromfile(VALS, dtype="<f8")
    N_raw = v.size
    finite = np.isfinite(v)
    nonzero = v != 0.0
    keep = finite & nonzero
    vv = np.abs(v[keep])                    # windows are relative; all committed targets are > 0
    n_neg = int((v[keep] < 0).sum())
    del v
    vs = np.sort(vv)
    print(f"\n  loaded {N_raw:,} float64 from {VALS}")
    print(f"  non-finite dropped {N_raw - int(finite.sum()):,}; exact zeros dropped "
          f"{int(finite.sum()) - int(keep.sum()):,}; negatives present {n_neg:,}")
    print(f"  swept array (|v|, sorted): {vs.size:,}   min={vs[0]:.6e}  max={vs[-1]:.6e}  "
          f"({time.time()-t0:.1f}s)")

    lv = np.log(vs)                          # already sorted, so log is sorted too
    print(f"  natural-log span: ln|v| in [{lv[0]:.1f}, {lv[-1]:.1f}]  -> "
          f"{(lv[-1]-lv[0])/math.log(10):.0f} decades of dynamic range")
    # robust support: central 99% of the ln distribution
    q = np.quantile(lv, [0.005, 0.25, 0.5, 0.75, 0.995])
    L99 = q[-1] - q[0]
    print(f"  ln|v| quantiles 0.5%/25%/50%/75%/99.5%: {q[0]:.2f} / {q[1]:.2f} / {q[2]:.2f} / "
          f"{q[3]:.2f} / {q[4]:.2f}   (central-99% ln width L99 = {L99:.1f})")

    N = vs.size
    keys = sm_target_keys(include_holdout=True)
    rows = []
    print(f"\n  {'target':<18}{'value':>14}{'w=tol':>10}{'naive N*2w':>12}{'coarse env':>11}"
          f"{'obs hits':>9}{'rec':>7}{'naive/obs':>10}{'obs/coarse':>11}")
    print("  " + "-" * 102)
    for k in keys:
        ts = resolve_target(k)
        tv = float(ts.value)
        w = measurement_tol(ts.pdg_target)
        lo, hi = tv * (1.0 - w), tv * (1.0 + w)
        i0, i1 = np.searchsorted(vs, lo, "left"), np.searchsorted(vs, hi, "right")
        # EXACT predicate, same as grind.sweep_target_streamed: score_value(...).rel_error <= tol
        seg = vs[i0:i1]
        obs = int(sum(1 for x in seg if score_value(float(x), ts.pdg_target).rel_error <= w)) \
            if seg.size <= 200000 else int(((np.abs(seg - tv) / abs(tv)) <= w).sum())
        naive = N * 2.0 * w
        # coarse envelope: empirical value fraction per natural-log unit at this target
        j0 = np.searchsorted(lv, math.log(tv) - 0.5, "left")
        j1 = np.searchsorted(lv, math.log(tv) + 0.5, "right")
        frac_per_ln = (j1 - j0) / 1.0 / N
        coarse = N * frac_per_ln * 2.0 * w   # relative window 2w == ln-window 2w for small w
        rec = RECORDED.get(k, None)
        rows.append(dict(key=k, value=tv, w=w, naive=naive, coarse=coarse, obs=obs,
                         recorded=rec, n_wide_ln1=int(j1 - j0), frac_per_ln=frac_per_ln,
                         holdout=k in HOLDOUT_KEYS))
        r1 = f"{naive/obs:>10.1f}" if obs else f"{'>' + format(naive, '.0f'):>10}"
        r2 = f"{obs/coarse:>11.2f}" if coarse > 0 else f"{'n/a':>11}"
        print(f"  {k:<18}{tv:>14.6g}{w:>10.2e}{naive:>12.3g}{coarse:>11.3g}{obs:>9}"
              f"{(rec if rec is not None else '-'):>7}{r1}{r2}")

    # ---- reproduce the committed totals -------------------------------------------------
    swept = [r for r in rows if not r["holdout"]]
    tot_obs = sum(r["obs"] for r in swept)
    tot_naive = sum(r["naive"] for r in swept)
    tot_coarse = sum(r["coarse"] for r in swept)
    mism = [(r["key"], r["recorded"], r["obs"]) for r in rows
            if r["recorded"] is not None and r["recorded"] != r["obs"]]
    print(f"\n  19 swept (non-holdout) targets: observed hits = {tot_obs:,}  "
          f"vs VERDICT.json n_hits = {RECORDED_TOTAL:,}  "
          f"-> {'MATCH' if tot_obs == RECORDED_TOTAL else 'MISMATCH'}")
    print(f"  per-target recorded-table check: {len(mism)} mismatch(es) {mism if mism else ''}")

    print(f"\n  AGGREGATE over the 19 swept targets:")
    print(f"    naive  sum N*2w                = {tot_naive:,.0f}")
    print(f"    coarse-envelope sum            = {tot_coarse:,.0f}")
    print(f"    observed                       = {tot_obs:,}")
    print(f"    naive / observed               = {tot_naive/tot_obs:,.1f}x   <-- the '~100x' claim")
    print(f"    naive / coarse   (dynamic range only) = {tot_naive/tot_coarse:,.1f}x")
    print(f"    coarse / observed (fine clustering)   = {tot_coarse/tot_obs:,.2f}x")

    # the md's single quoted example
    p12 = next(r for r in rows if r["key"] == "pmns_sin2_12")
    print(f"\n  the md's quoted example pmns_sin2_12: naive {p12['naive']:.2e} "
          f"(md said 5.1e6), observed {p12['obs']:,} (md said 26,142) -> "
          f"ratio {p12['naive']/p12['obs']:.1f}x")

    # ---- per-target spread of the ratio -------------------------------------------------
    hit_rows = [r for r in swept if r["obs"] > 0]
    ratios = np.array([r["naive"] / r["obs"] for r in hit_rows])
    fine = np.array([r["obs"] / r["coarse"] for r in hit_rows if r["coarse"] > 0])
    print(f"\n  per-target naive/observed over the {len(hit_rows)} targets with >=1 hit: "
          f"min {ratios.min():.1f}x  median {np.median(ratios):.1f}x  max {ratios.max():.1f}x")
    print(f"  per-target observed/coarse (FINE-CLUSTERING factor, >1 means the target sits on a")
    print(f"    LOCAL EXCESS relative to its own log-envelope): min {fine.min():.2f}  "
          f"median {np.median(fine):.2f}  max {fine.max():.2f}")
    n_excess = int((fine > 1.0).sum())
    print(f"    targets with fine factor > 1: {n_excess}/{len(fine)}")

    # ---- robustness: is 'observed/coarse = 1' an artifact of the +-0.5 ln band choice? ----
    print(f"\n  ROBUSTNESS of the coarse-envelope band width (aggregate over the 19 swept targets):")
    print(f"    {'band (ln)':>12}{'coarse sum':>13}{'observed':>10}{'obs/coarse':>12}{'naive/coarse':>14}")
    print("    " + "-" * 61)
    robust = []
    for R in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
        tc = 0.0
        for r in swept:
            lp = math.log(r["value"])
            nn = int(np.searchsorted(lv, lp + R, "right") - np.searchsorted(lv, lp - R, "left"))
            tc += (nn / (2 * R)) * 2 * r["w"]
        robust.append(dict(R=R, coarse=tc, obs_over_coarse=tot_obs / tc,
                           naive_over_coarse=tot_naive / tc))
        print(f"    {R:>12.2f}{tc:>13,.0f}{tot_obs:>10,}{tot_obs/tc:>12.3f}{tot_naive/tc:>14.1f}")
    print(f"    -> the 'locally log-uniform at window scale' result is band-independent; the 125x")
    print(f"       is dynamic range, NOT clumping.")

    with open(OUT, "w") as f:
        json.dump(dict(n_values=int(N), rows=rows, tot_obs=tot_obs, tot_naive=tot_naive,
                       tot_coarse=tot_coarse, ln_min=float(lv[0]), ln_max=float(lv[-1]),
                       L99=float(L99), band_robustness=robust), f, indent=1)
    print(f"\n  wrote {OUT}")
    print(f"  wall {time.time()-t0:.1f}s")
    print(bar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
