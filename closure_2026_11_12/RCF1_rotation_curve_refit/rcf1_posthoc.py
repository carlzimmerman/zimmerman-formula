#!/usr/bin/env python3
"""
RCF1 post hoc diagnostic (AMENDMENT_A1.md): the e_N bound. Reported, not graded.
Re-uses the frozen model by executing rcf1.py's definitions only (up to the known-answer checks) in this
process; writes rcf1_posthoc.out only.  kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "rcf1.py")).read()
cut = src.index('sec("RCF1  Milky Way')
src = src[:cut].replace('OUT = open(os.path.join(HERE, "rcf1.out"), "w")', 'OUT = open(os.devnull, "w")')
ns = {"__file__": os.path.join(HERE, "rcf1.py")}
exec(compile(src, "rcf1_defs", "exec"), ns)
CURVES, A0, STARS, errs = ns["CURVES"], ns["A0"], ns["STARS"], ns["errs"]
g_disc, g_bulge, g_hot, SV, chi2_surface, summarize, S_GRID = ns["g_disc"], ns["g_bulge"], ns["g_hot"], ns["SV"], ns["chi2_surface"], ns["summarize"], ns["S_GRID"]
out = open(os.path.join(HERE, "rcf1_posthoc.out"), "w")
def say(s=""):
    print(s); out.write(s + "\n")
say("RCF1 POST HOC (AMENDMENT_A1): primary McMillan census, MB15 hot gas, stat+sys errors. Reported, not graded.")
E0 = np.array([0.0]); EW = np.round(np.arange(0.0, 0.2 + 1e-9, 0.0005), 6); SW = np.round(np.arange(0.5, 3.0 + 1e-9, 0.0005), 6)
for c in CURVES:
    R, v, _, _ = CURVES[c]; sig = errs(c, "stat+sys")
    gs = g_disc(R, SV["thin"]) + g_disc(R, SV["thick"]) + g_bulge(R); gf = g_disc(R, SV["HI"]) + g_disc(R, SV["H2"]) + g_hot(R)
    for f, a0 in A0.items():
        z0 = summarize(chi2_surface(R, v, sig, gs, gf, a0, S_GRID, E0), S_GRID, E0, STARS)
        e3 = summarize(chi2_surface(R, v, sig, gs, gf, a0, S_GRID, np.array([0.03])), S_GRID, np.array([0.03]), STARS)
        wd = summarize(chi2_surface(R, v, sig, gs, gf, a0, SW, EW), SW, EW, STARS)
        say(f"{c:10s} {f:9s} e_N = 0 fixed: M* {z0['M']:.3f} [{z0['Mlo']:.3f}, {z0['Mhi']:.3f}], chi2 {z0['chi2']:.2f}"
            f" | e_N = 0.03 fixed: M* {e3['M']:.3f}, chi2 {e3['chi2']:.2f} (Delta chi2 vs e_N = 0: {e3['chi2']-z0['chi2']:+.2f})"
            f" | e_N free on [0, 0.2]: best e_N {wd['e']:.4f} (Delta chi2 = 1 range up to {wd['ehi']:.4f}), M* {wd['M']:.3f} [{wd['Mlo']:.3f}, {wd['Mhi']:.3f}], chi2 {wd['chi2']:.2f}")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
