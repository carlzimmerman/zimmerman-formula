#!/usr/bin/env python3
"""AR1: setups for live validation at arg mass 1e10, 1e13, from UL1's table of NR2 medians, EM1's line, DR8's fc. Reads only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
_a = sys.argv; sys.argv = [_a[0]]
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "UL1_measured_upsilon_test")); import ul1_core as C
sys.argv = _a; G = C.load(); t = "A_c2b_refit"; bg = C.BG[t]; rc = C.rc_of(t); KPC = C.KPC; D = json.load(open(os.path.join(RB, "LC1_live_contraction", "lc1_setup.json"))); fc = float(D["fc"]); O = {}
lM_g = np.array([bg["a"] + bg["b"] * (q["lMb"] - 10) for q in G]); Rd_g = np.array([q["meta"]["Rdisk"] for q in G])
for tag, A in (("1e10", 1e10), ("1e12", 1e12), ("1e13", 1e13)):
    M2 = fc * A; lM = math.log10(M2); R2 = (3 * M2 * C.MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); s = C.Sfn(lM, t); r0 = C.r0_of(M2 * C.MSUNE, R2, s); lMb = (lM - bg["a"]) / bg["b"] + 10; sel = (np.abs(lM_g - lM) <= 0.25) & (Rd_g > 0)
    if sel.sum() < 5: sel = np.isin(np.arange(len(G)), np.argsort(np.where(Rd_g > 0, np.abs(lM_g - lM), 9e9))[:10])  # departure: at 1e13 no SPARC galaxy lies within 0.25 dex on EM1, so the 10 nearest
    Rd = float(np.median(Rd_g[sel])); O[tag] = dict(lMg_range=[float(lM_g[sel].min()), float(lM_g[sel].max())], lM=lM, M2=M2, R2=R2 / KPC * 1e-3, r0=r0 / KPC * 1e-3, Md=10 ** lMb, Rd=Rd * 1e-3, c_nfw=12.95, n_gal=int(sel.sum()), eps=0.7e-3 * (R2 / KPC) / 199.3, Sigma=s / C.MSUNE * (KPC / 1e3) ** 2)
    print(tag, O[tag], flush=True)
json.dump(O, open(os.path.join(HERE, "ar1_setup.json"), "w"), indent=1)
