#!/usr/bin/env python3
"""FZS1 diagnostic (reported, not graded): why the settled rule lowers R_cold. At z 2.2, canonical, for four halo masses:
regime, R_set, r_M, r200m (comoving Mpc/h), s, the cold mass inside 0.25 / 0.5 R_set over that inside R_set (law shape vs reference),
and U_S / U_R at k 3 / 10 h/Mpc. Executes fzs1_hm.py up to its run marker (read-only). nice -n 10 python3 fzs1_diag.py fzs1_hm.py > fzs1_diag.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, math, numpy as np, warnings
warnings.filterwarnings("ignore")
SRC = sys.argv[1]; code = open(SRC).read(); cut = code.rindex("\n# ------------------------------------------------------------------ checkpointed run\n")
G = {"__file__": SRC, "__name__": "x"}; exec(compile(code[:cut], SRC, "exec"), G)
L = G["L"]; G["set_z"](2.2); ft = "canonical"; KK = G["KK"]
for M in (1e10, 1e11, 1e12, 1e13):
    hb = min(L["HB"], key=lambda b: abs(math.log(b["M"] / M))); fn = G["lay_S"](ft, 2.2)
    r, MS, inf = fn(hb); rR, MR, _ = G["layout"](hb, ft, mode="Rb"); rB, MB, _ = G["layout"](hb, ft, mode="B")
    R = inf.get("R_set"); bar = G["Bar"](hb, ft, r); CS = MS - bar; CRr = np.interp(r, rR, MR - G["Bar"](hb, ft, rR))
    fr = lambda C, x: np.interp(x * R, r, C) / np.interp(R, r, C)
    US = G["F"]["U_of"](r, MS, np.array([3.0, 10.0])); UR = G["F"]["U_of"](rR, MR, np.array([3.0, 10.0]))
    rM = math.sqrt(G["F"]["G"] * (G["FB"] * hb["M200c"] if inf["regime"] == "cluster" else (1 - G["FB"]) * hb["Mta"] / G["Xsh"](ft)) * G["h"] / G["F"]["a0c"](ft))
    print(f"M {hb['M']:.1e} {inf['regime']}: R_set {R:.4f} r_M {rM:.4f} r200 {hb['r200']:.3f} s {inf.get('s', float('nan')):.3f}; cold(<0.25/0.5 R_set)/cold(<R_set): law {fr(CS,0.25):.3f}/{fr(CS,0.5):.3f}, ref {fr(CRr,0.25):.3f}/{fr(CRr,0.5):.3f}; U_S/U_R at k 3/10: {US[0]/UR[0]:.4f}/{US[1]/UR[1]:.4f}")
