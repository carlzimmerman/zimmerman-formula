#!/usr/bin/env python3
"""CFG228 Stage 3, POST HOC EXTENSION (added after the first Stage-3 result showed R_t on a bound in all six fits; labelled, not frozen): the rotation-curve SHAPE is degenerate with V_a, so the conditional error of V(R_out)
(computed with R_t held at its bound) understates the shape uncertainty.  Here R_t is FIXED at 0.2, 0.6, 1.0, 1.5 and 3.0 kpc and the other five parameters are refitted; V(R_out) and chi^2 are reported for each.  The range of V(R_out)
over the R_t values whose chi^2 exceeds the free fit's by less than N_beam x 4 (a 2 sigma interval after the beam-correlation inflation) is the shape band used as a labelled variant in the scoring.
Run: python3 campaign_fresh_gravity/CFG228_alma_cubes/cfg228_stage3_profile.py"""
import os, sys, math, json, time
sys.dont_write_bytecode = True
import numpy as np
import multiprocessing as mp
from scipy.optimize import least_squares

LANE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LANE)
import cfg228_stage3 as S3

RT = (0.2, 0.6, 1.0, 1.5, 3.0)


def work(args):
    g, rt = args
    D = S3.prepare(g)
    mask = D["mask"]
    resid5 = lambda th5: ((D["data"] - S3.model(D, [th5[0], th5[1], th5[2], rt, th5[3], th5[4]])) / D["rms"])[:, mask].ravel()
    lo = [-360, D["vpk"] - 250, 10, 5, 0.05 * D["S"]]; hi = [720, D["vpk"] + 250, 800, 250, 5 * D["S"]]
    best = None
    for pa0 in (D["pa0"], D["pa0"] + 180):
        th0 = [pa0, D["vpk"], S3.START["Va"], S3.START["sig"], D["S"]]
        try:
            ft = least_squares(resid5, th0, bounds=(lo, hi), x_scale=[30, 30, 50, 20, 0.5], max_nfev=80)
        except Exception:
            continue
        if best is None or ft.cost < best.cost:
            best = ft
    th = [best.x[0], best.x[1], best.x[2], rt, best.x[3], best.x[4]]
    return dict(g=g, rt=rt, chi2=2 * best.cost, V_Rout=S3.vrot(th, D["R_out"]), V_R15=S3.vrot(th, D["R15"]), V_R30=S3.vrot(th, D["R30"]), Va=float(best.x[2]), sigma0=float(best.x[3]))


if __name__ == "__main__":
    T0 = time.time()
    real = {r["gid"]: r for r in json.load(open(os.path.join(LANE, "cfg228_stage3_results.json")))["REAL"]}
    jobs = [(g, rt) for g in S3.TAGS for rt in RT]
    ctx = mp.get_context("spawn")
    with ctx.Pool(4) as pool:
        res = pool.map(work, jobs)
    out, PROFILE = [], {}
    out.append("CFG228 Stage 3 POST HOC profile in the rotation-curve turnover radius R_t (the free fit of Stage 3 put R_t on a bound for every galaxy); V(R_out) in km/s, chi^2 relative to the free fit, acceptable = delta chi^2 < 4 N_beam")
    out.append("  galaxy          free-fit V(R_out) [R_t]      " + "   ".join(f"R_t={rt:<4}" for rt in RT) + "      acceptable V(R_out) range")
    for g in S3.TAGS:
        D = S3.prepare(g); r0 = real[g]
        rr = {x["rt"]: x for x in res if x["g"] == g}
        PROFILE[g] = {str(rt): dict(V_Rout=rr[rt]["V_Rout"], V_R15=rr[rt]["V_R15"], V_R30=rr[rt]["V_R30"], chi2=rr[rt]["chi2"], dchi2=rr[rt]["chi2"] - r0["chi2"], Va=rr[rt]["Va"], sigma0=rr[rt]["sigma0"]) for rt in RT}
        acc = [rr[rt]["V_Rout"] for rt in RT if rr[rt]["chi2"] - r0["chi2"] < 4 * D["Nbeam"]]
        PROFILE[g]["acceptable_range"] = [min(acc), max(acc)] if acc else [float("nan")] * 2
        out.append(f"  {g:13s} {r0['V_Rout']:6.1f} [{r0['theta'][3]:.2f}]        " + "   ".join(f"{rr[rt]['V_Rout']:6.1f} ({rr[rt]['chi2'] - r0['chi2']:+6.0f})" for rt in RT) + f"      {min(acc):6.1f} to {max(acc):6.1f}  (N_beam {D['Nbeam']:.1f})")
    out.append(f"\n{time.time() - T0:.0f} s")
    print("\n".join(out))
    json.dump(dict(PROFILE=PROFILE, RT=RT), open(os.path.join(LANE, "cfg228_stage3_profile_results.json"), "w"), indent=1, default=float)
    open(os.path.join(LANE, "cfg228_stage3_profile.out"), "w").write("\n".join(out) + "\n")
