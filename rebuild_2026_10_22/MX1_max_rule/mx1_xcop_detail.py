#!/usr/bin/env python3
"""MX1: B24's own error for cell P (bootstrap over 7 clusters; MGAS_LO, HI as the gas term) and the K2 diagnosis: contraction allowed to expand (this lane) against rf <= ri (DW2's bracket). Harness's rows_xcop, read with its data path. kappa = 1/2 FITTED."""
import os, sys, json, math
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import numpy as np, mx1_core as M
from astropy.io import fits
Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16; D = os.path.join(os.path.dirname(os.path.dirname(HERE)), "real_research", "data", "xcop"); li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
XC = []
for n in sorted(os.listdir(D)):
    p = os.path.join(D, n)
    if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{n}_mstar.fits"))): continue
    with fits.open(os.path.join(p, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
    with fits.open(os.path.join(p, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
    for x in (.1, .2, .3, .5, .7):
        r = x * r5; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(ga["RADIUS"] * rg, ga["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
        if np.all(np.isfinite([mh, mg, ms])): XC.append(dict(n=n, x=x, r=r * 1e3 * PCm, r5=r5 * 1e3 * PCm, mh=mh, mg=mg, ms=ms, efg=.5 * (li(ga["RADIUS"] * rg, ga["MGAS_HI"], r) - li(ga["RADIUS"] * rg, ga["MGAS_LO"], r)) / mg))
rr = np.array([z["r"] for z in XC]); mb = np.array([z["mg"] + z["ms"] for z in XC]); gb = Gm * mb * MSm / rr ** 2; r5a = np.array([z["r5"] for z in XC]); names = np.array([z["n"] for z in XC]); mh = np.array([z["mh"] for z in XC])
def run(cell, a0=9.3603e-11, gas=1.0):
    R = M.rule(cell); v = R.g(dict(gb=gb * gas, r=rr, r500=r5a, a0=a0)); return np.log10(mh / (v * rr ** 2 / Gm / MSm))
OUT = {}
for f, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    d = run("P", a0); u = sorted(set(names)); rg_ = np.random.default_rng(20261102); bs = []
    for _ in range(4000):
        pick = rg_.choice(u, len(u)); q = np.concatenate([d[names == n] for n in pick]); bs.append(math.sqrt((q ** 2).mean()))
    OUT[f] = dict(mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), boot_sd=float(np.std(bs)), by_cluster={n: float(d[names == n].mean()) for n in u}, median_gas_frac_err=float(np.median([z["efg"] for z in XC])))
    print(f, OUT[f])
print("cold points in zone, P canonical", )
for nm, setb in (("expansion allowed, D2", None), ("no expansion, DW2's bracket, D2", 1.0001)):
    src = open(os.path.join(HERE, "mx1_core.py")).read()
    if setb: src = src.replace("B = np.log(ri * 1.5)", f"B = np.log(ri * {setb})"); 
    g = {"__file__": os.path.join(HERE, "mx1_core.py"), "__name__": "m2"}; exec(compile(src, "m2", "exec"), g); d = np.log10(mh / (g["rule"]("D2").g(dict(gb=gb, r=rr, r500=r5a, a0=9.3603e-11)) * rr ** 2 / Gm / MSm)); d2 = np.log10(mh / (g["rule"]("P").g(dict(gb=gb, r=rr, r500=r5a, a0=9.3603e-11)) * rr ** 2 / Gm / MSm)); OUT[nm] = dict(D2_mean=float(d.mean()), D2_rms=float(math.sqrt((d ** 2).mean())), P_mean=float(d2.mean()), P_rms=float(math.sqrt((d2 ** 2).mean()))); print(nm, OUT[nm])
json.dump(OUT, open(os.path.join(HERE, "mx1_xcop_detail.json"), "w"), indent=1, sort_keys=True)
