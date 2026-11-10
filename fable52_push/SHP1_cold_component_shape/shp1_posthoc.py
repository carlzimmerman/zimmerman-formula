#!/usr/bin/env python3
"""SHP1 POST-HOC diagnostic (written after shp1.out was read; not in the frozen criteria; grades nothing).
Question: is B21's excess over the law a separate cold halo (R4's share profile) or a baryon-mass calibration?
Fit g_obs = g_law(k g_bar) (every lens's baryons scaled by k) with the full covariance, and compare chi^2 with
R4's best share fit on the same data. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["shp1.py"]; __file__ = os.path.join(HERE, "shp1.py")
src = open(__file__).read(); src = src[:src.index("# ====================================================================== Part A numbers")]
exec(compile(src, __file__, "exec"))
OUTL = []
def Q(s): print(s); OUTL.append(s)
def chi(r, C): return float(r @ np.linalg.solve(C, r))
ks = np.exp(np.linspace(math.log(0.3), math.log(8), 1200))
res = {}
for f in FOOT:
    a0 = A0[f]; res[f] = {}
    sets = dict(Nobins=([NOB], NOB_C, [10.45]), hotgas=([HOT], HOT_C, [10.45]), massbins=(MB, MB_C, list(BINS)))
    for nm, (ds, C, lms) in sets.items():
        gb = np.concatenate([d["gbar"] for d in ds]); go = np.concatenate([d["gobs"] for d in ds])
        c = np.array([chi(go - g_law(k * gb, a0), C) for k in ks]); i = int(np.argmin(c))
        ok = ks[c <= c[i] + 1]
        c0 = chi(go - g_law(gb, a0), C)
        r4 = R4(a0, 3.0) if nm == "massbins" else R4_nobins(ds[0], C, a0, 3.0)
        chi_share = r4["chi2_best"]
        n = len(go)
        res[f][nm] = dict(k_best=float(ks[i]), k_1sigma=[float(ok.min()), float(ok.max())], chi2_k=float(c[i]), chi2_law=c0,
                          chi2_share=chi_share, X_share=r4["X_best_clamped"], N=n)
        Q(f"{f} {nm}: law chi2 {c0:.1f}/{n}; baryons x k: k = {ks[i]:.2f} [{ok.min():.2f}, {ok.max():.2f}] chi2 {c[i]:.1f}; "
          f"separate share (R4, z_n 3) X_s {r4['X_best_clamped']:.1f} chi2 {chi_share:.1f}")
json.dump(res, open(os.path.join(HERE, "shp1_posthoc.json"), "w"), indent=1)
OUTL.append("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "shp1_posthoc.out"), "w").write("\n".join(OUTL) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
