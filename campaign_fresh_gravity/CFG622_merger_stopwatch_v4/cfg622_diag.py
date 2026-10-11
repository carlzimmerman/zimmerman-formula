#!/usr/bin/env python3
"""CFG622 post-run diagnosis (README disclosures D-1..D-3).  Reads runs/ only; changes no verdict; every number here is
REPORTED ONLY (post hoc), never a score.
D-1: what sets T_M (which variant, which alpha, which epochs give the large control spreads).
D-2: why M2 fails: per-epoch Harvey beta at alpha = 0, split at t - t_peri = 0.2 Gyr, grid seed 599 and the 6 alpha = 0 controls;
     and which epochs CFG621's stability rule (spread <= T_L, unmasked) had dropped.
D-3: alpha = 1: the masked primary lensing peak's distance from the bisector (edge guard) at the Bullet epoch.
Run: python3 cfg622_diag.py -> cfg622_diag.out, cfg622_diag_results.json"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg622_main as M
VAR = ["(300,60)", "(300,90)", "(200,75)", "(400,75)"]
OUT, RES = [], {}
P = lambda s="": (print(s), OUT.append(s))

# D-1
d1 = {}
for fn in sorted(glob.glob(os.path.join(HERE, "runs", "a*_seed60[0-2].json"))):
    r = json.load(open(fn)); nm = os.path.basename(fn)[:-5]; tp = r["t_peri"]
    rows = []
    for d in M.window(r["diag"], tp):
        if M.beta_of(d)[1] < 50:
            continue
        s = d["sub"]; L = np.array(s["lens"])
        dist = [float(np.hypot(*(np.array(a) - L))) for a in s["lens_alts"]]
        if max(dist) > 100:
            rows.append(dict(t_after=round(d["t"] - tp, 3), worst=VAR[int(np.argmax(dist))], spread=round(max(dist), 1),
                             d_sub_main=round(float(np.hypot(*(np.array(s["gal"]) - np.array(d["main"]["gal"])))), 1),
                             lens_minus_gal=round(float(np.hypot(*(L - np.array(s["gal"])))), 1)))
    d1[nm] = rows
    P(f"D-1 {nm}: {len(rows)} epochs with spread > 100 kpc" + (f"; t-t_peri {rows[0]['t_after']}-{rows[-1]['t_after']}, worst variant "
      f"{sorted(set(x['worst'] for x in rows))}, d_sub-main {rows[0]['d_sub_main']}-{rows[-1]['d_sub_main']} kpc, primary lens-gal "
      f"{rows[0]['lens_minus_gal']}-{rows[-1]['lens_minus_gal']} kpc" if rows else ""))
RES["D1_large_control_spreads"] = d1

# D-2
d2 = {}
o621 = json.load(open(os.path.join(M.C621, "runs_B", "a0_can_v2666.7_eta1.132.json")))
for fn in sorted(glob.glob(os.path.join(HERE, "runs", "a0_*_v2666.7_eta1.132*.json"))):
    nm = os.path.basename(fn)[:-5]
    if "calib" in nm or "swap" in nm:
        continue
    r = json.load(open(fn)); tp = r["t_peri"]
    q = [d for d in M.window(r["diag"], tp) if M.beta_of(d)[1] >= 50]
    b = np.array([M.beta_of(d)[0] for d in q]); t = np.array([d["t"] - tp for d in q])
    e = dict(n=len(q), beta_bar_all=float(b.mean()), beta_bar_t_lt_0p2=float(b[t < 0.2 - 1e-9].mean()),
             beta_bar_t_ge_0p2=float(b[t >= 0.2 - 1e-9].mean()), max_beta_early=float(b[t < 0.2 - 1e-9].max()))
    if nm == "a0_can_v2666.7_eta1.132":
        st = np.array([dd["sub"]["lens_spread"] <= M.T_L for dd in M.window(o621["diag"], tp) if M.beta_of(dd)[1] >= 50])
        e["cfg621_dropped_t_after"] = [round(float(x), 2) for x in t[~st]]
        e["cfg621_beta_bar_stable_only"] = float(b[st].mean())
    d2[nm] = e
    P(f"D-2 {nm}: beta-bar all {e['beta_bar_all']:.3f} | t<0.2 {e['beta_bar_t_lt_0p2']:.3f} (max {e['max_beta_early']:.3f}) | "
      f"t>=0.2 {e['beta_bar_t_ge_0p2']:.3f}" + (f" | CFG621 dropped t-t_peri {e['cfg621_dropped_t_after']} -> {e['cfg621_beta_bar_stable_only']:.3f}"
                                                 if "cfg621_dropped_t_after" in e else ""))
RES["D2_alpha0_harvey"] = d2

# D-3
d3 = {}
for f in M.FEET:
    r = json.load(open(os.path.join(HERE, "runs", f"a1_{f}_v2666.7_eta1.132.json"))); ep = M.S.epoch(r["diag"], r["t_peri"])
    rows = []
    for i in (ep["i_obs"] - 1, ep["i_obs"]):
        s = r["diag"][i]["sub"]; g = np.array(s["gal"])
        rows.append(dict(lens_edge=s["lens_edge"], alts_edge=s["alts_edge"], gas_edge=s["gas_edge"],
                         lens_minus_gal=float(np.hypot(*(np.array(s["lens"]) - g))), lens_nomask_minus_gal=float(np.hypot(*(np.array(s["lens_nomask"]) - g))),
                         gas_minus_gal=float(np.hypot(*(np.array(s["gas"]) - g)))))
    d3[f] = rows
    P(f"D-3 alpha 1 {f}: masked primary {[round(x['lens_minus_gal']) for x in rows]} kpc from galaxies, {[round(x['lens_edge']) for x in rows]} kpc "
      f"from the bisector (guard 75); unmasked {[round(x['lens_nomask_minus_gal']) for x in rows]}; gas {[round(x['gas_minus_gal']) for x in rows]} kpc")
RES["D3_alpha1_edge"] = d3
open(os.path.join(HERE, "cfg622_diag.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg622_diag_results.json"), "w"), indent=1)
