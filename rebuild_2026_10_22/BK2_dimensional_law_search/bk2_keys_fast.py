#!/usr/bin/env python3
"""BK2 G8 fast tier: SL1's cached linear response with F's total mass, gas +0, f* 0.034. Allowed only if it reproduces LW1's law row (criteria). kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
from bk2_lib import *
os.environ["SL1_HERE"] = os.path.join(RB, "SL1_symbolic_law_search")
_NS = {"__name__": "sl1_lib"}; exec(compile(open(os.path.join(RB, "SL1_symbolic_law_search", "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0], "discover_law", "exec"), _NS)
D = _NS["Data"](); KEYS = _NS["KEYS"]; kc = _NS["keys_core"]; red = _NS["redf"]
def keys(s, foot, a0, h, ge=None):
    o = D.cl[h]; Ge = D.c["GE"]; nd = o["nd"]; Mb = o["Mb"]; R = nd; gb = Ge * Mb / R ** 2; fs = 0.034; gg = gb / (1 + fs); gs = gb - gg
    lM = np.log(np.maximum(Mb, 1e-300)); lR = np.log(R); dl = np.zeros_like(lM); dl[:, 1:-1] = (lM[:, 2:] - lM[:, :-2]) / (lR[:, 2:] - lR[:, :-2]); dl[:, 0] = dl[:, 1]; dl[:, -1] = dl[:, -2]; inner = np.zeros_like(gb)
    for k in range(R.shape[1] - 2, -1, -1): inner[:, k] = inner[:, k + 1] + 0.5 * (gb[:, k] + gb[:, k + 1]) * (R[:, k + 1] - R[:, k])
    L = _local_(gs, gg, R, dl, R * gb + inner + gb[:, -1:] * R[:, -1:], a0); g = ev(s, L); 
    if not (np.all(np.isfinite(g)) and np.all(g > 0)): return None
    MF = g * R ** 2 / Ge; ok = o["M0"] > 0; ratio = np.where(ok, (MF - Mb) / np.where(ok, o["M0"], 1), 1.0); de = ratio - 1.0
    Pp = o["P0"] + np.einsum("ibk,ik->ib", o["LP"], de); Sb = np.maximum(o["S0"] + np.einsum("ibk,ik->ib", o["LS"], de), 1e-300); V = o["W"] * Pp * red(o, Sb); return kc(D.C["clusters"], V, foot, h, None)
def _local_(gs, gg, r, dl, Phi, a0):
    import bk2_lib as B; return B._local(gs, gg, r, dl, Phi, a0)
if __name__ == "__main__":
    Lw = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_keys_g0_f034.json"))); out = []
    print(list(Lw["R1|c0|canonical"].keys())[:12])
    for f in ("canonical", "alt"):
        cell = Lw[f"R1|c0|{f}"]
        for h in ("h0672", "h0686"):
            z = keys("I1(gb,a0)", f, A0S[f], h); Zr = cell["Z"][h]; rr = np.array([Zr[k] for k in KEYS]); print(f, h, "max |dZ|", float(np.abs(z - rr).max()), dict(zip(KEYS, np.round(z - rr, 2).tolist())), "M3", round(float(rr[13]), 2), round(float(z[13]), 2))
