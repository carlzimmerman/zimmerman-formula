#!/usr/bin/env python3
"""BF2: which way does A30 fail. Mean model/data per mass bin before two-halo, RQ3's path. kappa = 1/2 FITTED; not theory closed."""
import importlib.util as iu, math, os
from bf2_common import *
A = rq3(); A.crg(); import crg1_lens as Le
L = Le.load(); st = Le.Stencil(L["Rn"] * 1e6); SIk = 1e6 / 3.0857e16; a0 = A0["canonical"]
for t in ("law", "P2", "P3", "P7", "P8"):
    sp = iu.spec_from_file_location(t, os.path.join(RQ3, "candidates", "law.py") if t == "law" else os.path.join(LANE, "candidates", t + ".py")); c = iu.module_from_spec(sp); sp.loader.exec_module(c); Tb = np.zeros((len(Le.LMG), 60)); o = []
    for i, lm in enumerate(Le.LMG):
        MB, Mbm = Le.baryon(float(lm)); gb = Le.Gpc * MB / Le.RGRID ** 2; gg = Le.Gpc * (MB - 10 ** float(lm)) / Le.RGRID ** 2; v = c.g(dict(gb=gb * SIk, gg=gg * SIk, gs=(gb - gg) * SIk, r=Le.RGRID * 3.0857e16, a0=a0, sample="lens")); Tb[i] = st.dsig(MB * v / (gb * SIk), "linear")
        if abs(lm - 10.6) < .06: k = np.searchsorted(Le.RGRID, [3e4, 1e5, 3e5, 1e6]); o = [(round(float(gb[j] * SIk / a0), 4), round(float(gg[j] / gb[j]), 2), round(float(v[j] / law(gb[j] * SIk, a0)), 3)) for j in k]
    m = Le.stack(L, Tb).reshape(4, 15); Y = L["Yn"]; print(t, "model/data, mean, by bin:", [round(float((m[b] / Y[b]).mean()), 2) for b in range(4)], "inner 5:", [round(float((m[b][:5] / Y[b][:5]).mean()), 2) for b in range(4)], "outer 5:", [round(float((m[b][-5:] / Y[b][-5:]).mean()), 2) for b in range(4)], "(y, f, g/law) at log M* ~10.6, 30, 100, 300, 1000 pc units of RGRID:", o, flush=True)
