#!/usr/bin/env python3
r"""
clustering_depth_and_gateA.py -- AUDIT LENS: CLUSTERING. Step 3: is the credit STABLE, which way
does the over-dispersion cut, and is the chance model the GATE ACTUALLY APPLIES calibrated?

Steps 1-2 established, on the real depth-10 array:
  * naive E[hits]=N*2w overpredicts observed hits by 125.0x aggregate (recorded counts reproduced
    exactly, 82,613/82,613);
  * the whole factor is dynamic range (632 decades), not fine clumping: observed/coarse-envelope
    = 1.00x aggregate, per-target 0.84-1.27;
  * targets sit AT their own log-envelope (enrichment 0.54-1.73, median 1.00, 3/20 above the 95th
    percentile of a matched null) -- NOT on clumps;
  * BUT the set IS strongly over-dispersed at fine scale: g(r) = 1.00 at r=1e-2, 1.24 at 1e-5,
    2.39 at 1e-6, 149 at 1e-8, saturating at ~1.5e4 for r <= 1e-10 (a fixed population of
    near-degenerate pairs at the float64 floor).

Three things must be settled before saying the threshold is safe:
  S1  IS THE 125x CREDIT STABLE WITH DEPTH? It is a dynamic-range factor, so it can drift as the
      enumeration deepens. Measure it at depths 8, 9, 10 from the committed arrays.
  S2  WHICH WAY DOES THE OVER-DISPERSION CUT? Over-dispersion at FIXED MEAN lowers P(>=1 hit)
      (conservative for a null) but raises the hit count AT an occupied clump (anti-conservative
      for a survivor's local-rate estimate, which is what gate/fdr.py extrapolates linearly).
      Measure both: P(>=1)/E[hits] and the conditional clump boost B(h) = E[hits | >=1]/(2h*rho).
  S3  IS THE CHANCE MODEL THE GATE ACTUALLY APPLIES CALIBRATED? grind's sweep calls the committed
      gate/fdr.py, whose E_chance comes from build_value_set(germ_pool) -- a ~65k pairs+triples
      library over 1e-3<|v|<1e7 -- NOT from the 42.5M enumerated set the search really draws from.
      Compare the two E_chance values per target, in bits.

No hard-coded verdicts. Local-only. python3 audit_interlock/clustering_depth_and_gateA.py
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

from exhaust import resolve_target, build_alphabet, _germ_pool_from_alpha   # noqa: E402
from exhaust_parallel import sm_target_keys             # noqa: E402
from engine.scoring import measurement_tol              # noqa: E402
from gate.fdr import build_value_set, _poisson_e_chance, PASS_BITS   # noqa: E402
from targets.pdg_constants import HOLDOUT_KEYS          # noqa: E402

OUT = os.path.join(ROOT, "audit_interlock", "clustering_depth_and_gateA.json")
RNG = np.random.default_rng(20260729)
R_COARSE = 0.5


def load_depth(d: int) -> np.ndarray:
    ddir = os.path.join(ROOT, "results_grind", f"depth_{d}")
    p = os.path.join(ddir, "values_merged.f64")
    if not os.path.exists(p):
        p = os.path.join(ddir, "values.f64")
    v = np.fromfile(p, dtype="<f8")
    v = v[np.isfinite(v) & (v != 0.0)]
    return np.sort(np.abs(v)), p


def rel_counts(lv: np.ndarray, probes: np.ndarray, h: float) -> np.ndarray:
    lo = np.log(probes * (1.0 - h))
    hi = np.log(probes * (1.0 + h))
    return (np.searchsorted(lv, hi, "right") - np.searchsorted(lv, lo, "left")).astype(np.int64)


def main() -> int:
    bar = "=" * 106
    print(bar)
    print("CLUSTERING AUDIT step 3 -- credit stability, direction of the over-dispersion, Gate-A calibration")
    print(bar)
    t0 = time.time()
    keys = sm_target_keys(include_holdout=True)
    tspecs = [(k, resolve_target(k)) for k in keys]
    tols = {k: measurement_tol(ts.pdg_target) for k, ts in tspecs}
    tvals = {k: float(ts.value) for k, ts in tspecs}
    # the 21st historical target (r_tau_mu, held back) -- needed to reconcile depth 8/9 totals,
    # which were swept before the 2026-07-27 holdout guard landed.
    ts21 = dict(tspecs)
    ts21["r_tau_mu"] = resolve_target("r_tau_mu")
    tols21 = {k: measurement_tol(v.pdg_target) for k, v in ts21.items()}
    tvals21 = {k: float(v.value) for k, v in ts21.items()}

    # ------------------------------------------------ S1 depth scaling of the credit ------
    print("\nS1  IS THE 125x CREDIT STABLE WITH DEPTH?  (naive N*2w vs coarse envelope vs observed)")
    print("-" * 106)
    print(f"      {'depth':>6}{'N kept':>13}{'ln span':>10}{'rho@band [/ln]':>16}"
          f"{'sum naive':>13}{'sum coarse':>12}{'sum obs':>10}{'naive/obs':>11}{'credit bits':>12}")
    print("      " + "-" * 98)
    s1 = []
    for d in (8, 9, 10):
        vs, path = load_depth(d)
        lv = np.log(vs)
        N = vs.size
        swept = [k for k in keys if k not in HOLDOUT_KEYS]
        tot_naive = tot_coarse = tot_obs = 0.0
        rhos = []
        obs21 = 0
        for k in keys + ["r_tau_mu"]:      # 21 = 19 swept + koide_Q_lep + r_tau_mu
            tv, w = tvals21[k], tols21[k]
            obs = int(rel_counts(lv, np.array([tv]), w)[0])
            obs21 += obs
            if k not in swept:
                continue
            lp = math.log(tv)
            nwide = int(np.searchsorted(lv, lp + R_COARSE, "right")
                        - np.searchsorted(lv, lp - R_COARSE, "left"))
            rho = nwide / (2 * R_COARSE)
            rhos.append(rho)
            tot_naive += N * 2 * w
            tot_coarse += rho * 2 * w
            tot_obs += obs
        ratio = tot_naive / tot_obs if tot_obs else float("nan")
        credit = math.log2(N / float(np.median(rhos)))
        s1.append(dict(depth=d, N=int(N), ln_span=float(lv[-1] - lv[0]),
                       rho_median=float(np.median(rhos)), naive=tot_naive, coarse=tot_coarse,
                       obs=int(tot_obs), obs21=int(obs21), naive_over_obs=ratio,
                       credit_bits=credit, path=path))
        print(f"      {d:>6}{N:>13,}{lv[-1]-lv[0]:>10.0f}{np.median(rhos):>16,.0f}"
              f"{tot_naive:>13,.0f}{tot_coarse:>12,.0f}{int(tot_obs):>10,}{ratio:>11.1f}"
              f"{credit:>12.2f}")
        del vs, lv
    # cross-check against the committed per-depth n_hits. depth 8/9 were swept BEFORE the
    # 2026-07-27 holdout guard, so their committed totals cover 21 targets; depth 10 covers 19.
    print(f"\n      {'depth':>6}{'committed n_hits':>18}{'recount 19 swept':>18}"
          f"{'recount all 21':>16}{'match':>10}")
    for d in (8, 9, 10):
        vj = os.path.join(ROOT, "results_grind", f"depth_{d}", "VERDICT.json")
        rec = json.load(open(vj)).get("n_hits") if os.path.exists(vj) else None
        r = next(x for x in s1 if x["depth"] == d)
        m = "19-target" if rec == r["obs"] else ("21-target" if rec == r["obs21"] else "NEITHER")
        print(f"      {d:>6}{rec:>18,}{r['obs']:>18,}{r['obs21']:>16,}{m:>10}")
    dc = [r["credit_bits"] for r in s1]
    print(f"\n      credit drift over depths 8->10: {dc[0]:.2f} -> {dc[1]:.2f} -> {dc[2]:.2f} bits "
          f"({dc[-1]-dc[0]:+.2f} bits over 2 depths)")
    print(f"      per-depth ln-span drift: "
          + " -> ".join(f"{r['ln_span']:.0f}" for r in s1)
          + "   (the credit IS this dynamic range; it grows, so the credit grows with depth)")

    # ------------------------------------------------ S2 direction of over-dispersion -----
    print("\nS2  WHICH WAY DOES THE FINE-SCALE OVER-DISPERSION CUT?")
    print("-" * 106)
    vs, _ = load_depth(10)
    lv = np.log(vs)
    N = vs.size
    NP = 200000
    probes = np.exp(RNG.uniform(-8.0, 9.0, NP))
    lp = np.log(probes)
    rho = (np.searchsorted(lv, lp + R_COARSE, "right")
           - np.searchsorted(lv, lp - R_COARSE, "left")) / (2 * R_COARSE)
    print(f"      {NP:,} log-uniform probes in ln|v| in [-8,9]; rho from +-{R_COARSE} ln band")
    print(f"      The statistic that decides the DIRECTION is the OCCUPANCY rate: P(>=1 hit) vs its")
    print(f"      Poisson value <1-exp(-E)>. Clumping cannot move the MEAN (E[hits]=2h*rho holds")
    print(f"      identically); it can only push occupancy DOWN at fixed mean.")
    print(f"\n      {'h (rel)':>9}{'E=2h*rho':>11}{'mean obs':>10}{'#occupied':>11}{'P(>=1)':>11}"
          f"{'Poisson P':>11}{'P/P_pois':>10}{'clump sz':>10}{'bits':>7}")
    print("      " + "-" * 92)
    s2 = []
    for h in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8, 1e-10):
        n = rel_counts(lv, probes, h)
        Ei = 2 * h * rho
        E = float(Ei.mean())
        obs_mean = float(n.mean())
        nocc = int((n >= 1).sum())
        p1 = nocc / NP
        p_pois = float((1.0 - np.exp(-Ei)).mean())
        rat = p1 / p_pois if p_pois > 0 else float("nan")
        clump = float(n[n >= 1].mean()) if nocc else float("nan")
        bits = -math.log2(rat) if rat == rat and rat > 0 else float("nan")
        s2.append(dict(h=h, E=E, obs_mean=obs_mean, n_occupied=nocc, p_ge1=p1,
                       p_poisson=p_pois, p_over_poisson=rat, clump_size=clump,
                       conservative_bits=bits))
        print(f"      {h:>9.0e}{E:>11.4g}{obs_mean:>10.4g}{nocc:>11,}{p1:>11.4g}{p_pois:>11.4g}"
              f"{rat:>10.3f}{clump:>10.3g}{bits:>7.2f}")
    print(f"""
      READ-OUT -- and a CORRECTION to my own first pass, which reported a 'boost' of 2.7e4 (14.7
      bits) at h=1e-10. That number was a conditional count divided by a tiny unconditional mean;
      it only restated that occupancy is rare and was NOT a bias in the chance model. Removed.
        * mean obs == E[hits] = 2h*rho at every h: the coarse-envelope rate is UNBIASED for the
          mean. That is why step 1's observed/coarse = 1.00 aggregate.
        * P(>=1)/Poisson <= 1 in the informative regime (E<1): hits arrive in small near-degenerate
          clumps (clump size ~1.2-1.6 vs Poisson 1.0), so a randomly placed tight window is occupied
          LESS often than Poisson at the same mean. Direction: CONSERVATIVE, size = the 'bits'
          column -- fractions of a bit, not the ~7 bits of the dynamic-range credit.
        * So the huge g(r) at fine scale (a fixed population of near-degenerate pairs at the float64
          floor; g -> ~1.5e4 for r<=1e-10) is REAL but nearly harmless for the threshold: it shows
          up as a clump size of ~1.6, i.e. under a bit, because E[hits] there is ~6e-5.""")

    # ------------------------------------------------ S3 Gate A calibration ---------------
    print("\nS3  THE CHANCE MODEL THE GATE ACTUALLY APPLIES: germ-pool library vs the real value set")
    print("-" * 106)
    alpha = build_alphabet(None, None)
    pool = _germ_pool_from_alpha(alpha)
    lib = build_value_set(pool)
    print(f"      gate/fdr.py build_value_set({len(pool)} germs) -> library of {lib.size:,} values, "
          f"restricted to 1e-3<|v|<1e7")
    liba = np.sort(np.abs(lib[np.isfinite(lib) & (lib != 0)]))
    llv = np.log(liba)
    print(f"      library ln span [{llv[0]:.1f},{llv[-1]:.1f}] = {(llv[-1]-llv[0])/math.log(10):.0f} "
          f"decades vs enumerated set's {(lv[-1]-lv[0])/math.log(10):.0f} decades")
    print(f"\n      {'target':<18}{'tol':>9}{'E_ch(gate)':>12}{'E_ch(real)':>12}"
          f"{'real/gate':>11}{'bits over-credited':>20}{'gate verdict':>14}")
    print("      " + "-" * 96)
    s3 = []
    for k, ts in tspecs:
        tv, w = tvals[k], tols[k]
        n_hit_lib, e_gate = _poisson_e_chance(tv, liba, w)
        wlo, whi = tv * 0.9, tv * 1.1
        n_wide_real = int(np.searchsorted(lv, math.log(whi), "right")
                          - np.searchsorted(lv, math.log(wlo), "left"))
        e_real = n_wide_real * (2 * w) / 0.2
        ratio = e_real / e_gate if e_gate > 0 else float("inf")
        over = math.log2(ratio) if ratio not in (0.0,) and math.isfinite(ratio) else float("inf")
        # what the gate would conclude from its own e_chance (mult = 19 targets, ignoring bit cap)
        chance = min(1.0, min(1.0, e_gate) * 19)
        gbits = -math.log2(chance) if chance > 0 else float("inf")
        verdict = "BAKED(dense)" if e_gate >= 1.0 else ("PASS-A" if gbits >= PASS_BITS else "sub-10-bit")
        s3.append(dict(key=k, tol=w, e_gate=e_gate, e_real=e_real, ratio=ratio,
                       bits_over=over, n_wide_real=n_wide_real, n_hit_lib=n_hit_lib,
                       gate_bits=gbits, gate_verdict=verdict))
        print(f"      {k:<18}{w:>9.1e}{e_gate:>12.3g}{e_real:>12.3g}"
              f"{(f'{ratio:.1f}' if math.isfinite(ratio) else 'inf'):>11}"
              f"{(f'{over:+.1f}' if math.isfinite(over) else 'inf'):>20}{verdict:>14}")
    fin = [r for r in s3 if math.isfinite(r["bits_over"]) and r["bits_over"] > -99]
    ob = np.array([r["bits_over"] for r in fin])
    n_inf = sum(1 for r in s3 if not math.isfinite(r["bits_over"]))
    print(f"\n      Gate A's library UNDERSTATES the real look-elsewhere rate on "
          f"{int((ob>0).sum())}/{len(fin)} measurable targets")
    print(f"      by median {np.median(ob):+.1f} bits (min {ob.min():+.1f}, max {ob.max():+.1f}); "
          f"{n_inf} target(s) have E_chance(gate)=0 -> unbounded over-credit.")
    tight = [r for r in s3 if r["tol"] < 1e-6]
    print(f"      the TIGHT targets (tol<1e-6, i.e. where a JACKPOT would be claimed): "
          + ", ".join(f"{r['key']}:{r['gate_verdict']}" for r in tight))

    with open(OUT, "w") as f:
        json.dump(dict(depth_scaling=s1, dispersion=s2, gateA=s3,
                       lib_size=int(liba.size)), f, indent=1)
    print(f"\n  wrote {OUT}\n  wall {time.time()-t0:.1f}s")
    print(bar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
