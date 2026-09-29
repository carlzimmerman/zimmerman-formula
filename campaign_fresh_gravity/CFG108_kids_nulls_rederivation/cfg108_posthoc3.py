"""CFG108 POST HOC 3: the E-mode-only class-dependent stellar-mass (g_bar-assignment) equivalent of the whole split (V2 amplitude).
 A class-dependent offset d (dex) in the baryonic mass moves every lens of that class in log g_bar by d at fixed pair radius; the ESD at fixed assigned g changes by slope*d, slope = d log ESD / d log g_bar (local, K1, all sources).
"""
import os, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "real_research", "data", "lensing_rar")): return env
    p = HERE
    for _ in range(14):
        if os.path.isdir(os.path.join(p, "real_research", "data", "lensing_rar")): return p
        p = os.path.dirname(p)
DATA = os.path.join(find_repo(), "real_research", "data", "lensing_rar")
NP = 50; KG = 1.98847e30 / (3.0857e16) ** 2
typ = np.load(os.path.join(DATA, "lr_lenses.npz"))["typ"]; patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
K1 = np.arange(8, 15)
GE = np.logspace(-15, math.log10(5e-12), 16); lg = 0.5 * (np.log10(GE[:-1]) + np.log10(GE[1:]))[K1]
def esd(c): 
    m = typ == c
    return pl["WG"][m][:, K1].sum(0) / pl["WW"][m][:, K1].sum(0) / KG
for c, nm in ((0, "late"), (1, "early")):
    e = esd(c)
    sl = np.polyfit(lg, np.log10(e), 1)[0]
    print("%-5s K1 ESD %s ; local log-slope d log ESD / d log g_bar = %+.3f" % (nm, np.round(e, 1), sl))
# amplitude V2 all-source
Aall = 0.182
sl = np.mean([np.polyfit(lg, np.log10(esd(c)), 1)[0] for c in (0, 1)])
print("mean slope %+.3f ; class-dependent M_gal offset that mimics the whole split (A_all V2 = %.3f dex): d = %.2f dex (early overestimated relative to late means their true g_bar is lower ...) " % (sl, Aall, abs(Aall / sl)))
