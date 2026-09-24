#!/usr/bin/env python3
"""
L04 -- GEOMETRY-DISCRIMINATION POWER STUDY + THE TWO-OPACITY TEST
2026-09-23.  Engine: J02_moment_hierarchy.simulate (central and volume).

Window ratio (the observable):  R = -ln A / E[D],  A = P(zero scatterings)
(zero-collision escape fraction, N == 0), D = tau - Q per photon
(J01/J02/J09p/J11 conventions).

SURVIVING CONTENT being powered here:
  central window R_c in [4/3, 2], tau0-INDEPENDENT (any tau0, any q):
      R_c = (1 + q/3)/(1/2 + q/4)          [J09p p=2, K01 F3-fixed scope]
  volume window R_v tau0-DEPENDENT:
      R_v(tau0=1, q=0) ~ 1.897, R_v(q=10) ~ 1.314; thin ~2.2, deep ~1.2 [J11]
  => GEOMETRY DISCRIMINATORS:
      (i)  POINT estimate: R_v(tau0=1) vs R_c(tau0=1), same q  (Part 1)
      (ii) TWO-OPACITY (curvature) test: an observer with TWO bands sees
           DIFFERENT effective opacities of the SAME object:
           slope := R(tau0=2.0) - R(tau0=0.5).
           central -> slope = 0 within SE (tau0-independence);
           volume  -> slope < 0 (ratio decreases into opacity).      (Part 2)

SE: delta method on f(a,d) = -ln(a)/d using the per-photon covariance of
(I, D), I = [N == 0], streamed in blocks of CHUNK photons (exact pooled
sufficient statistics; memory-bounded at n = 1e7).

Part 3: minimal per-ratio measurement precision to see the volume slope at
3 sigma given the MEASURED slope magnitude: se_req = |slope_v|/(3 sqrt(2)).
Part 4: observer protocol + required per-band S/N.

Honesty clause: the slope test is ALSO run at n = 1e7 (12 simulations of
10^7 photons) and the central-vs-volume slope separation is reported per q;
any q failing 3-sigma separation at 1e7 is a registered limitation.

REGISTERED CAVEAT (measured below, and in J11 V3 1.7104 @q=3): the POINT
ratio discriminator flips direction with q -- at q=0 central > volume
(2.002 vs ~1.897) but at q=3 volume > central (1.71 vs 1.60); the curves
cross near q ~ 1-2.  A point-ratio observer needs |Delta| or a known q.
The TWO-OPACITY slope test is direction-robust: volume slope < 0 at every q
measured, central slope = 0 within SE at every q.

Modes:
  python3 L04_geometry_power.py            -- full simulation run (~1 h)
  python3 L04_geometry_power.py --reanalyze -- re-derive ALL checks/P3/P4
       from the raw measurements already saved in L04_results.json
       (reproduces this lane's .out and .json without re-simulation).

No git commit (per task).
"""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import simulate

CHUNK = 2_000_000
HERE = os.path.dirname(os.path.abspath(__file__))


def seed_for(q, tau0, src, n):
    """Deterministic, collision-free seed per (q, tau0, src, n)."""
    qb = int(round(q * 10))          # {0, 30, 100}
    tb = int(round(tau0 * 10))       # {5, 10, 20}
    sb = 10 if src == "central" else 20
    nb = {1e5: 5, 1e6: 6, 1e7: 7}[int(n)]
    return qb * 10000 + tb * 100 + sb + nb


def window_ratio(n, tau0, q, src, seed):
    """R = -ln A / E[D] with delta-method SE (per-photon (I,D) covariance).

    Streamed in CHUNK blocks; pooled sums give the exact same mean/cov as a
    single n-run (blocks are IID MC photons), with bounded memory at n=1e7.
    """
    tot = dict(n=0, sI=0.0, sD=0.0, sII=0.0, sDD=0.0, sID=0.0)
    nblk = max(1, int(math.ceil(n / CHUNK)))
    for b in range(nblk):
        nb = min(CHUNK, n - b * CHUNK)
        r = simulate(nb, tau0, q, src, seed * 1000 + b)
        I = (r["N"] == 0).astype(np.float64)
        D = r["D"]
        tot["n"] += nb
        tot["sI"] += float(I.sum())
        tot["sD"] += float(D.sum())
        tot["sII"] += float((I * I).sum())
        tot["sDD"] += float((D * D).sum())
        tot["sID"] += float((I * D).sum())
    nn = tot["n"]
    a = tot["sI"] / nn
    d = tot["sD"] / nn
    varI = (tot["sII"] - tot["sI"] ** 2 / nn) / (nn - 1.0)
    varD = (tot["sDD"] - tot["sD"] ** 2 / nn) / (nn - 1.0)
    covID = (tot["sID"] - tot["sI"] * tot["sD"] / nn) / (nn - 1.0)
    R = -math.log(a) / d
    # f(a, d) = -ln(a)/d ;  df/da = -1/(a d) ;  df/dd = ln(a)/d^2  (< 0)
    dfda = -1.0 / (a * d)
    dfdd = math.log(a) / d ** 2
    se2 = (dfda * dfda * varI + dfdd * dfdd * varD
           + 2.0 * dfda * dfdd * covID) / nn
    return dict(R=R, se=math.sqrt(se2), A=a, dbar=d, n=nn,
                varI=varI, varD=varD, covID=covID)


def central_closed_form(q):
    return (1.0 + q / 3.0) / (0.5 + q / 4.0)


def run_simulations(res):
    """Parts 1-2 raw measurements (heavy)."""
    QS = (0.0, 3.0, 10.0)

    # ---------- PART 1: point-estimate discrimination at tau0 = 1 --------
    print("=" * 78)
    print("L04 PART 1: POINT-ESTIMATE DISCRIMINATION  (tau0 = 1, window ratio R = -lnA/E[D])")
    print("=" * 78)
    P1 = {}
    for q in QS:
        for n in (1e5, 1e6):
            row = {}
            for src in ("central", "volume"):
                m = window_ratio(int(n), 1.0, q, src, seed_for(q, 1.0, src, n))
                row[src] = m
                print(f"  q={q:4.0f} n={int(n):>7d} {src:7s}: R={m['R']:.4f} "
                      f"se={m['se']:.4f}  A={m['A']:.5f} E[D]={m['dbar']:.4f}")
            dR = row["central"]["R"] - row["volume"]["R"]
            se = math.hypot(row["central"]["se"], row["volume"]["se"])
            z = dR / se
            n_req = int(n) * (3.0 / z) ** 2
            row["z_sep"] = z
            row["n_req_3sig"] = n_req
            P1[f"q{int(q)}_n{int(n)}"] = row
            print(f"      -> central-vs-volume z = {z:7.2f}   "
                  f"n for 3sigma = {n_req:>10.0f}")
    res["measurements"]["P1_point_estimate_tau0_1"] = P1

    # ---------- PART 2: two-opacity pairs --------------------------------
    print("=" * 78)
    print("L04 PART 2: TWO-OPACITY TEST  slope = R(tau0=2.0) - R(tau0=0.5)")
    print("=" * 78)
    raw = {}
    for q in QS:
        for src in ("central", "volume"):
            for n in (1e6, 1e7):
                for tau0 in (0.5, 2.0):
                    key = f"q{int(q)}_{src}_n{int(n)}_t{tau0:g}"
                    m = window_ratio(int(n), tau0, q, src,
                                     seed_for(q, tau0, src, n))
                    raw[key] = m
                    print(f"  {key:28s}: R={m['R']:.4f} se={m['se']:.4f} "
                          f"A={m['A']:.5f} E[D]={m['dbar']:.4f}")
    res["measurements"]["P2_two_opacity_raw"] = raw


def analyze(res):
    """All checks, P2 slopes, P3 precision, P4 protocol (fast; pure JSON)."""
    ok = True
    QS = (0.0, 3.0, 10.0)

    def check(name, cond):
        res["checks"][name] = bool(cond)
        nonlocal ok
        ok &= bool(cond)

    P1 = res["measurements"]["P1_point_estimate_tau0_1"]

    # scaling consistency + 3-sigma power of the point estimate
    print("-" * 78)
    print("P1 recap (tau0 = 1, window ratio point estimates):")
    for q in QS:
        for n in (1e5, 1e6):
            k = f"q{int(q)}_n{int(n)}"
            row = P1[k]
            c, v = row["central"], row["volume"]
            print(f"  q={int(q):2d} n={int(n):>7d}: "
                  f"central R={c['R']:.4f}+-{c['se']:.4f}  "
                  f"volume R={v['R']:.4f}+-{v['se']:.4f}  "
                  f"dR={c['R'] - v['R']:+.4f}  z={row['z_sep']:7.2f}  "
                  f"n_for_3sig={row['n_req_3sig']:>9.0f}")
    for q in QS:
        z5 = P1[f"q{int(q)}_n100000"]["z_sep"]
        z6 = P1[f"q{int(q)}_n1000000"]["z_sep"]
        check(f"P1_z_scaling_q{int(q)}_sqrt10",
              abs(z6 / z5 - math.sqrt(10.0)) < 0.3 * math.sqrt(10.0))
        # magnitude of the separation is the discriminator (direction can
        # flip with q -- registered caveat; see md)
        check(f"P1_3sig_at_1e6_q{int(q)}", abs(z6) >= 3.0)
        nr5 = P1[f"q{int(q)}_n100000"]["n_req_3sig"]
        nr6 = P1[f"q{int(q)}_n1000000"]["n_req_3sig"]
        check(f"P1_nreq_consistent_q{int(q)}",
              abs(math.log10(nr5 / nr6)) < 0.25)
        # central closed form at tau0 = 1, n = 1e6
        rc = P1[f"q{int(q)}_n1000000"]["central"]
        cf = central_closed_form(q)
        zc = abs(rc["R"] - cf) / rc["se"]
        check(f"P1_central_closedform_q{int(q)}", zc < 5.0)
        print(f"  check q={int(q)}: central vs closed form "
              f"{rc['R']:.4f} vs {cf:.4f} (z={zc:.1f})")

    # ---------- Part 2 analysis: slopes ----------------------------------
    print("=" * 78)
    print("L04 PART 2 (analysis):  slope = R(tau0=2.0) - R(tau0=0.5)")
    print("=" * 78)
    raw = res["measurements"].get("P2_two_opacity_raw")
    if raw is None:
        # v1-schema migration: re-measure the 12 pairs at n = 1e6 (same
        # deterministic seeds as the full run -> bit-identical R/se, and
        # carries A/E[D]); the n = 1e7 rows carry R/se from the full run.
        raw = {}
        print("  [migration] re-measuring n=1e6 pairs for A/E[D] context "
              "(bit-identical seeds):")
        for q in QS:
            for src in ("central", "volume"):
                for tau0 in (0.5, 2.0):
                    m = window_ratio(1000000, tau0, q, src,
                                     seed_for(q, tau0, src, 1e6))
                    raw[f"q{int(q)}_{src}_n1000000_t{tau0:g}"] = m
                    print(f"    q{int(q)} {src:7s} t{tau0:g}: R={m['R']:.4f} "
                          f"A={m['A']:.5f} E[D]={m['dbar']:.4f}")
        for key, row in res["measurements"]["P2_two_opacity"].items():
            ns = key.split("_n")[1]
            if int(ns) != 10000000:
                continue
            q = int(key.split("_n")[0][1:])
            for src in ("central", "volume"):
                s = row[src]
                for tag, t0, fld in (("t0.5", 0.5, "R_low"),
                                     ("t2", 2.0, "R_high")):
                    raw[f"q{q}_{src}_n10000000_{tag}"] = dict(
                        R=s[fld], se=s["se_low" if tag == "t0.5" else "se_high"],
                        A=None, dbar=None, n=10000000,
                        note="R/se from full-run v1 JSON")
        res["measurements"]["P2_two_opacity_raw"] = raw
    P2 = {}
    for q in QS:
        for n in (1e6, 1e7):
            row = {}
            for src in ("central", "volume"):
                lo = raw[f"q{int(q)}_{src}_n{int(n)}_t0.5"]
                hi = raw[f"q{int(q)}_{src}_n{int(n)}_t2"]
                slope = hi["R"] - lo["R"]
                se_slope = math.hypot(hi["se"], lo["se"])
                row[src] = dict(R_low=lo["R"], se_low=lo["se"],
                                R_high=hi["R"], se_high=hi["se"],
                                slope=slope, se_slope=se_slope,
                                z_slope_vs0=slope / se_slope)
            z_sep_slope = ((row["volume"]["slope"] - row["central"]["slope"])
                           / math.hypot(row["volume"]["se_slope"],
                                        row["central"]["se_slope"]))
            row["z_sep_slope"] = z_sep_slope
            P2[f"q{int(q)}_n{int(n)}"] = row
            c = row["central"]; v = row["volume"]
            print(f"  q={int(q):2d} n={int(n):>7d}: "
                  f"central slope={c['slope']:+.4f} "
                  f"(z={c['z_slope_vs0']:+.2f})   "
                  f"volume slope={v['slope']:+.4f} "
                  f"(z={v['z_slope_vs0']:+.2f})   "
                  f"separation z={z_sep_slope:8.2f}")
    res["measurements"]["P2_two_opacity"] = P2

    # checks per q (n = 1e7 is the honesty-grade run; 1e6 secondary)
    for q in QS:
        for n in (1e7, 1e6):
            r = P2[f"q{int(q)}_n{int(n)}"]
            c = r["central"]; v = r["volume"]
            check(f"P2_central_flat_q{int(q)}_n{int(n)}",
                  abs(c["z_slope_vs0"]) < 3.0)
            check(f"P2_volume_decreasing_q{int(q)}_n{int(n)}",
                  v["slope"] < 0.0 and v["z_slope_vs0"] <= -3.0)
            # separation in MAGNITUDE (volume slope more negative) >= 3
            check(f"P2_slope_separation_q{int(q)}_n{int(n)}",
                  abs(r["z_sep_slope"]) >= 3.0
                  and v["slope"] < c["slope"])

    # registered limitation scan at n = 1e7
    res["limitations"] = []
    for q in QS:
        r = P2[f"q{int(q)}_n10000000"]
        if not (abs(r["z_sep_slope"]) >= 3.0
                and r["volume"]["z_slope_vs0"] <= -3.0):
            res["limitations"].append(
                f"q={int(q)} at n=1e7: slope test fails to separate "
                f"central from volume at 3 sigma "
                f"(|z_sep|={abs(r['z_sep_slope']):.2f})")

    # ---------- Part 3: minimal precision --------------------------------
    print("=" * 78)
    print("L04 PART 3: MINIMAL PER-RATIO PRECISION FOR A 3-SIGMA SLOPE")
    print("=" * 78)
    P3 = {}
    for q in QS:
        v = P2[f"q{int(q)}_n10000000"]["volume"]
        Delta = -v["slope"]                       # slope magnitude (positive)
        se_req = Delta / (3.0 * math.sqrt(2.0))   # per-ratio, balanced SEs
        # photon budget from the measured se at n = 1e7 per band
        n_req_band = {}
        for tag, m in (("low", v["se_low"]), ("high", v["se_high"])):
            n_req_band[tag] = 1e7 * (m / se_req) ** 2
        P3[f"q{int(q)}"] = dict(slope_mag=Delta, se_req_per_ratio=se_req,
                                n_req_band=n_req_band,
                                n_req_max=max(n_req_band.values()))
        print(f"  q={int(q):2d}: |slope|={Delta:.4f}  se_req={se_req:.4f}  "
              f"n_req low-band={n_req_band['low']:>9.0f}  "
              f"high-band={n_req_band['high']:>9.0f}")
    res["measurements"]["P3_min_precision"] = P3

    # ---------- Part 4: protocol + per-band S/N --------------------------
    print("=" * 78)
    print("L04 PART 4: OBSERVER PROTOCOL")
    print("=" * 78)
    P4 = {}
    for q in QS:
        v = P2[f"q{int(q)}_n10000000"]["volume"]
        Delta = -v["slope"]
        se_req = Delta / (3.0 * math.sqrt(2.0))
        sn_low = v["R_low"] / se_req
        sn_high = v["R_high"] / se_req
        P4[f"q{int(q)}"] = dict(SN_low_band=sn_low, SN_high_band=sn_high,
                                SN_required=max(sn_low, sn_high))
        print(f"  q={int(q):2d}: required per-band S/N = R/se_req : "
              f"low {sn_low:6.1f}  high {sn_high:6.1f}  "
              f"(protocol requirement {max(sn_low, sn_high):.1f})")
    res["measurements"]["P4_protocol_SN"] = P4

    protocol = (
        "TWO-OPACITY GEOMETRY PROTOCOL.  (1) An observer observes ONE object "
        "in TWO bands whose effective cloud opacities differ (tau0 = 0.5 and "
        "2.0 at same q in this study).  (2) In each band measure the window "
        "ratio R = -ln A / E[D] (A = zero-scatter escape fraction) with the "
        "per-photon delta-method SE.  (3) Form the opacity slope "
        "s = R(tau0=2.0) - R(tau0=0.5).  (4) DECISION: s = 0 within 3 sigma "
        "(|s|/se_s < 3) -> CENTRAL geometry (window tau0-independent, "
        "closed form (1+q/3)/(1/2+q/4) in [4/3,2]); s < 0 at 3 sigma "
        "(s/se_s <= -3) -> VOLUME-emissive geometry (window falls into "
        "opacity: ~2.2 thin -> ~1.2 deep; measured 1.909->1.802 at q=0, "
        "1.827->1.433 at q=3, 1.633->0.924 at q=10; the q=10 deep value "
        "sits BELOW the central floor 4/3, impossible for central at any "
        "tau0 or q).  A positive slope is unphysical for either geometry -> "
        "measurement error.  (5) Required per-band S/N (ratio/SE, worst "
        "band): "
        + "; ".join(f"q={int(q)}: {P4[f'q{int(q)}']['SN_required']:.1f}"
                    for q in QS)
        + " (equivalently per-ratio se <= |slope|/(3 sqrt(2)) = "
        + "; ".join(f"{P3[f'q{int(q)}']['se_req_per_ratio']:.4f} at "
                    f"q={int(q)}" for q in QS)
        + ", i.e. ~"
        + "; ".join(f"{P3[f'q{int(q)}']['n_req_max']:.0f} photons/band "
                    f"at q={int(q)}" for q in QS)
        + ").  (6) Single-band alternative (two objects, same tau0=1): "
        "3-sigma POINT discrimination needs n = "
        + "; ".join(
                    f"{P1[f'q{int(q)}_n1000000']['n_req_3sig']:.0f} photons/cloud "
                    f"at q={int(q)}" for q in QS)
                + ".  CAVEAT: the point-ratio separation flips "
        "direction with q (q=0: central>volume; q=3: volume>central, "
        "crossing near q~1-2), so the point test needs a known q or |Delta|; "
        "the two-opacity slope test is direction-robust.  (7) Deep-opacity "
        "bands (q=10, tau0=2) are A-limited: se_R ~ sqrt((1-A)/A)/"
        "(sqrt(n) E[D]); the A term dominates the ratio SE and drives the "
        "photon budget there."
    )
    res["protocol"] = protocol

    if not res["limitations"]:
        zs = ", ".join(f"{abs(P2[f'q{int(q)}_n10000000']['z_sep_slope']):.1f}"
                       for q in QS)
        res["limitations"].append(
            "none: at n=1e7 the slope test separates central from volume "
            f"at >3 sigma at every q (|z_sep| = {zs} for q = 0 / 3 / 10)")
    else:
        res["limitations"].append(
            "REGISTERED: at n=1e7 the slope test does NOT separate central "
            "from volume at 3 sigma for some q (see list).")
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    return ok


def main():
    t0 = time.time()
    res = {"checks": {}, "measurements": {}, "protocol": "", "limitations": []}
    reanalyze = "--reanalyze" in sys.argv[1:]
    fullwall = None
    if reanalyze:
        with open(os.path.join(HERE, "L04_results.json")) as f:
            res = json.load(f)
        fullwall = res.get("wall_seconds")
        if fullwall is None or fullwall < 60.0:
            # original full-run log (2026-09-23) printed wall=3597s; the
            # v1 JSON save did not survive an intermediate overwrite
            fullwall = 3597.0
        res["wall_seconds_fullrun"] = fullwall
        res["checks"] = {}
        res["measurements"] = res.get("measurements", {})
        print("L04 REANALYZE MODE: raw measurements loaded from "
              "L04_results.json (no re-simulation; wall time only analysis)")
    else:
        run_simulations(res)
    ok = analyze(res)
    res["wall_seconds"] = time.time() - t0
    res["mode"] = "reanalyze" if reanalyze else "full"
    with open(os.path.join(HERE, "L04_results.json"), "w") as f:
        json.dump(res, f, indent=1)
    print("-" * 78)
    print(f"checks passed {res['passed']}/{res['total_checks']}  "
          f"ALL_PASSED={ok}  wall={res['wall_seconds']:.0f}s  "
          f"mode={res['mode']}")
    print("ALL L04 CHECKS PASSED" if ok else "L04 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())