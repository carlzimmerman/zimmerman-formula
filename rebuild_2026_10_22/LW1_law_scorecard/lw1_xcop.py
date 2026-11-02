#!/usr/bin/env python3
"""LW1 X-COP (FROZEN_CRITERIA.md part 2): the a0 law on DR1's cached rows and on CS2's FITS row builder; CS2's own core rule through the same builder, to show what its -0.151 is. Writes lw1_xcop.json. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, pickle, sys
import numpy as np
from astropy.io import fits
from scipy.optimize import brentq, minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
_C = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))
A0 = dict(_C["const"]["A0"])
Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16
def law(Mb_si, r_si, a0, G_):
    gb = G_ * Mb_si / r_si ** 2; return (0.5 * gb + np.sqrt(0.25 * gb ** 2 + a0 * gb)) * r_si ** 2 / G_
def cached(a0):
    from collections import defaultdict
    GE, MSE, MPCE = float(_DR["G"]), float(_DR["MS"]), float(_DR["MPC"]); D = []; bx = defaultdict(list); bc = defaultdict(list); M = defaultdict(list); xr = defaultdict(list)
    for z in _C["xcop"]["canonical"]["rows"]:
        r = z["r_kpc"] * 1e3 * MPCE / 1e6; Mb = z["Mb_Msun"] * MSE; Mh = z["MHSE_Msun"]; Ml = float(law(Mb, r, a0, GE)) / MSE; v = math.log10(Mh / Ml)
        if z["x"] <= 0.75: D.append(v); bc[z["cluster"]].append(v)
        bx[f"{z['x']:g}"].append(v); M[f"{z['x']:g}"].append((Mh - Ml, 1 - Ml / Mh, Mh, Ml, z["Mb_Msun"], z["cluster"]))
    d = np.array(D); return dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d), factor=float(10 ** d.mean()), by_x={k: float(np.mean(v)) for k, v in bx.items()}, n_by_x={k: len(v) for k, v in bx.items()}, by_cluster={k: float(np.mean(v)) for k, v in bc.items()},
        deficit_Msun={k: float(np.median([a[0] for a in v])) for k, v in M.items()}, missing_share={k: float(np.median([a[1] for a in v])) for k, v in M.items()}, M_HSE={k: float(np.median([a[2] for a in v])) for k, v in M.items()}, M_law={k: float(np.median([a[3] for a in v])) for k, v in M.items()}, M_b={k: float(np.median([a[4] for a in v])) for k, v in M.items()}, PASS=bool(abs(d.mean()) <= 0.05 and np.sqrt((d ** 2).mean()) <= 0.10))
_DR = dict(G=_C["const"]["GE"], MS=_C["const"]["MSUNE"], MPC=_C["const"]["MPCE"])
P(f"LW1 X-COP; kappa = 1/2 FITTED; convention log10(M_HSE / M_model), positive = model short. DR1 constants G {_DR['G']}, MS {_DR['MS']}, MPC {_DR['MPC']}")
# CS2's builder, verbatim in content
DATA = os.path.join(REPO, "real_research", "data")
def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
def Bk(x): x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
XC = []
for name in sorted(os.listdir(os.path.join(DATA, "xcop"))):
    p_ = os.path.join(DATA, "xcop", name)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    rows = []
    for x in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0):
        r = x * r500; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(gas["RADIUS"] * rg500, gas["MGAS"], r); ms = li(st["RADIUS"], st["MSTAR"], r)
        if np.all(np.isfinite([mh, mg, ms])): rows.append((x, r, mh, mg + ms))
    m500 = li(hm["RADIUS"], hm["M_FORW"], r500); XC.append(dict(name=name, rows=rows, sig=math.sqrt(Gm * m500 * MSm / (r500 * 1000 * PCm)) / 1e3 / math.sqrt(2)))
def cs2rule(A, q, piv):
    d = []
    for c in XC:
        S = 10 ** A * (c["sig"] / piv) ** q; x1 = [r for r in c["rows"] if abs(r[0] - 1.0) < 1e-9][0]; R5 = x1[1] * 1e3; Mc5 = x1[2] - x1[3]
        lm = lambda lr: math.log(S * math.exp(2 * lr) * math.pi * float(Bk(R5 / math.exp(lr))))
        pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(R5 * 1e-6), math.log(R5 * 1e3)), method="bounded", options={"xatol": 1e-10})
        r0 = math.exp(float(pk.x)) if lm(float(pk.x)) < math.log(Mc5) else math.exp(brentq(lambda lr: lm(lr) - math.log(Mc5), math.log(R5 * 1e-7), float(pk.x), xtol=1e-14))
        for x, r, mh, mb in c["rows"]:
            if x > 0.75: continue
            d.append(math.log10(mh / (mb + math.pi * S * r0 ** 2 * float(Bk(r * 1e3 / r0)))))
    d = np.array(d); return dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d))
def lawfits(a0):
    d = []
    for c in XC:
        for x, r, mh, mb in c["rows"]:
            if x > 0.75: continue
            d.append(math.log10(mh * MSm / float(law(mb * MSm, r * 1e3 * PCm, a0, Gm))))
    d = np.array(d); return dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d))
J = json.load(open(os.path.join(RB, "CS2_core_law_out_of_sample", "cs2_out_of_sample_results.json")))["calibration"]; D1 = json.load(open(os.path.join(RB, "DR1_density_term_law", "dr1_offline.json")))["xcop"]["R1|c0"]
R = dict(convention="log10(M_HSE/M_model)"); R["cs2_rule"] = cs2rule(J["A"], J["q"], 70.50); P(f"CS2's core rule through its own builder (Burkert, cold mass set to M_HSE - M_b at R500; NOT the a0 law): {R['cs2_rule']}")
for f, a0 in A0.items():
    a = cached(a0); b = lawfits(a0); m = cached(a0 * 1.5); R[f] = dict(cached=a, fits=b, MUTATE=m)
    k3 = max(abs(a["mean"] - D1[f]["mean"]), abs(a["rms"] - D1[f]["rms"])); R[f]["K3_d"] = k3
    P(f"[{f}] a0 law, cached rows: mean {a['mean']:+.4f}, rms {a['rms']:.4f}, n {a['n']}, factor M_HSE/M_law {a['factor']:.3f}; DR1 |d| {k3:.1e}; FITS builder {b['mean']:+.4f}, {b['rms']:.4f}, n {b['n']}, |d| {abs(a['mean'] - b['mean']):.1e}; MUTATE a0 x 1.5: {m['mean']:+.4f}, {m['rms']:.4f}")
    for x in sorted(a["by_x"], key=float): P(f"   x {x}: mean {a['by_x'][x]:+.3f} (factor {10 ** a['by_x'][x]:.2f}, n {a['n_by_x'][x]}); median M_HSE {a['M_HSE'][x]:.3e}, M_b {a['M_b'][x]:.3e}, M_law {a['M_law'][x]:.3e}, deficit {a['deficit_Msun'][x]:.3e} Msun, share missing {a['missing_share'][x]:.3f}")
    P("   by cluster: " + ", ".join(f"{k} {v:+.3f}" for k, v in a["by_cluster"].items()))
    P(f"   bracket, not a grade, HSE - 0.12 dex (LF1's offset): mean {a['mean'] - 0.12:+.3f}, factor {10 ** (a['mean'] - 0.12):.2f}")
json.dump(R, open(os.path.join(HERE, "lw1_xcop.json"), "w"), indent=1); open(os.path.join(HERE, "lw1_xcop.out"), "w").write("\n".join(OUT) + "\n")
