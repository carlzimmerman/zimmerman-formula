#!/usr/bin/env python3
"""WLG1 POST HOC readings (written after the frozen run; no word). From wlg1_per_lens.csv (main configuration):
(1) per lens, the source redshift at which r reaches the +0.10 line (above it the reference halo under-predicts);
(2) per lens, the gas each footing needs for s = 1, against ESZ1's 5.2e12 measured and 8.3e12 two-sigma limit;
(3) the share of M_b that is the class-level gas.
Run: nice -n 19 python3 -I wlg1_posthoc.py   Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, csv, math, importlib.util
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
def load_mod(name, path):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
E = load_mod("euc1_ro", os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling", "euc1.py"))
J = load_mod("jnt2_common_ro", os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_common.py"))
R = list(csv.DictReader(open(os.path.join(HERE, "wlg1_per_lens.csv"), newline="")))
OUT = []
def P(s): print(s); OUT.append(s)
P("WLG1 POST HOC readings (no word). Main configuration: N-A, R_200c self-consistent, w 0.08, EUC17-corrected, gas G-MID, c x 1.")
zs_star, need = [], {"canonical": [], "alt": []}; gshare = []
for r in R:
    zl = float(r["z_l"]); lobs = float(r["logM_obs_inf"]); lref = float(r["logM_ref"])
    target = lref + 0.10                       # M_obs at which r = +0.10
    f = lambda zs: math.log10(E.EUCLID.sigcr(zl, zs) / E.EUCLID.sigcr(zl, E.ZS_INF)) + lobs - target
    if f(E.ZS_INF) >= 0: zs_star.append(np.inf)          # under-predicts already at infinity
    elif f(zl + 0.01) < 0: zs_star.append(zl + 0.01)
    else: zs_star.append(brentq(f, zl + 0.01, E.ZS_INF))
    Mb = float(r["M_b"]); Mg = float(r["M_gas"]); Ms = Mb - Mg
    gshare.append(Mg / Mb)
    for ft in ("canonical", "alt"):
        v = J.vstar_kms(ft, zl) * 1e3
        Mb_need = v ** 3 / (10 * J.G * (1 + J.XS) * J.H0 * J.E(zl)) / J.MSUN
        need[ft].append(Mb_need - Ms)
zs_star = np.array(zs_star); zcap = np.where(np.isfinite(zs_star), zs_star, 1.0e4)   # infinite = short already at z_s infinity
P(f"(1) source redshift z_s* below which r > +0.10 (sources nearer than z_s* leave the halo short): median {np.median(zcap):.2f}; 16-84 % {np.percentile(zcap,16):.2f} to {np.percentile(zcap,84):.2f} (1e4 = short at infinity); "
  f"already short at infinity: {int(np.sum(~np.isfinite(zs_star)))} of {len(zs_star)}; fraction with z_s* < 2: {np.mean(zs_star < 2):.2f}, < 3: {np.mean(zs_star < 3):.2f}")
for ft in ("canonical", "alt"):
    n = np.array(need[ft])
    P(f"(2) {ft}: gas needed for s = 1 (stars and net members as counted): median {np.median(n):.3g} Msun (16-84 % {np.percentile(n,16):.3g} to {np.percentile(n,84):.3g}); "
      f"fraction of lenses needing more than ESZ1's measured 5.2e12: {np.mean(n > 5.2e12):.2f}; more than its 2-sigma 8.3e12: {np.mean(n > 8.3e12):.2f}")
P(f"(3) gas share of M_b in the main configuration: median {np.median(gshare):.2f}")
open(os.path.join(HERE, "wlg1_posthoc.out"), "w").write("\n".join(OUT) + "\n")
