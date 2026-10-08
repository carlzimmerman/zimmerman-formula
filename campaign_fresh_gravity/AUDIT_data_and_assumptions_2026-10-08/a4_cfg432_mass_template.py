#!/usr/bin/env python3
"""AUDIT A4 (read-only): CFG432 (X-COP unsettled cold-mass SHAPE).  CFG432 takes M_tot = M_FORW, the X-COP forward
hydrostatic mass, which comes from a parametric (generalised-NFW-type) pressure model -- a shape template calibrated on
LCDM clusters -- with constant hydrostatic bias b.  This script re-does the gas-tracking slope
d ln(M_u/M_gas)/d ln r over 0.1-1 R500 (M_u = M_tot/(1-b(r)) - nu M_b) with each mass model the X-COP files carry
(M_FORW, M_NFW, M_EIN, M_ISO, M_BUR) and with a radially RISING bias b(r) = 0.05 -> 0.30 (non-thermal pressure growing
outward, the direction that would most help gas tracking).  Stars: the cluster's own M* file if present, else 0.10 M_gas
(CFG432's declared alternative convention), so the baseline is CFG432's 'stars=0.10Mgas' row, not its primary row.
Nothing in CFG432 is imported or rewritten.  Gas exclusion survives iff |median slope| > 0.15 at z > 3 in every row."""
import os, glob, json, numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "real_research", "data", "xcop"))
G, MS, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(y)))
li = lambda x, xp, fp: np.exp(np.interp(np.log(x), np.log(xp), np.log(np.clip(fp, 1e-30, None)), left=np.nan, right=np.nan))
cl = []
for d in sorted(glob.glob(os.path.join(DATA, "*", ""))):
    n = os.path.basename(os.path.dirname(d))
    with fits.open(os.path.join(d, n + "_hydro_mass.fits")) as f:
        rh = np.array(f[1].data["RADIUS"], float); M = {k: np.array(f[1].data[k], float) for k in ("M_FORW", "M_NFW", "M_EIN", "M_ISO", "M_BUR")}
    with fits.open(os.path.join(d, n + "_fgas_profile.fits")) as f:
        r500 = float(f[1].header["R500"]); rg = np.array(f[1].data["RADIUS"], float) * r500; mg = np.array(f[1].data["MGAS"], float)
    r = np.logspace(np.log10(0.1 * r500), np.log10(r500), 16); mgr = li(r, rg, mg); st = os.path.join(d, n + "_mstar.fits")
    if os.path.exists(st):
        with fits.open(st) as f: ms = li(r, np.array(f[2].data["RADIUS"], float), np.array(f[2].data["MSTAR"], float))
    else: ms = 0.10 * mgr
    cl.append(dict(n=n, r=r, mg=mgr, mb=mgr + ms, M={k: li(r, rh, v) for k, v in M.items()}))
def slope(r, q):
    ok = np.isfinite(q) & (q > 0)
    return float(np.polyfit(np.log(r[ok]), np.log(q[ok]), 1)[0]) if ok.sum() >= 6 else np.nan
def boot(s, seed=432):
    s = np.array([x for x in s if np.isfinite(x)]); rng = np.random.default_rng(seed)
    return float(np.median(s)), float(np.std([np.median(s[rng.integers(0, len(s), len(s))]) for _ in range(2000)])), len(s)
out, L = {}, [f"N clusters {len(cl)}; slope of ln(M_u/M_gas) over 0.1-1 R500 (flat = gas tracking; tolerance 0.15)"]
for foot, a0 in A0.items():
    for bl, bfun in (("b=0", lambda x: 0 * x), ("b=0.3", lambda x: 0.3 + 0 * x), ("b(r) 0.05->0.30", lambda x: 0.05 + 0.25 * np.log10(x / x[0]))):
        for mk in ("M_FORW", "M_NFW", "M_EIN", "M_ISO", "M_BUR"):
            s = []
            for c in cl:
                gb = G * c["mb"] * MS / (c["r"] * KPC) ** 2; mu = c["M"][mk] / (1 - bfun(c["r"])) - nu(gb / a0) * c["mb"]
                s.append(slope(c["r"], mu / c["mg"]))
            m, sd, n = boot(s); z = abs(m) / sd if sd > 0 else np.inf
            call = "EXCLUDED" if abs(m) > 0.15 and z > 3 else ("CONSISTENT" if abs(m) <= 0.15 and z <= 2 else "INCONCLUSIVE")
            out[f"{foot}|{bl}|{mk}"] = dict(median=m, sd=sd, n=n, z=z, call=call)
            L.append(f"  {foot:9s} {bl:16s} {mk:7s}: gas slope {m:+.3f} +- {sd:.3f} (n {n}, z {z:.1f}) {call}")
calls = {v["call"] for v in out.values()}
L.append(f"gas tracking EXCLUDED in {sum(v['call'] == 'EXCLUDED' for v in out.values())}/{len(out)} rows; other calls: {sorted(calls - {'EXCLUDED'})}")
json.dump(out, open(os.path.join(HERE, "a4_cfg432_mass_template.json"), "w"), indent=1)
print("\n".join(L)); open(os.path.join(HERE, "a4_cfg432_mass_template.out"), "w").write("\n".join(L) + "\n")
