#!/usr/bin/env python3
"""CFG476: dark-matter-only LCDM (Moster+13 AM + Dutton-Maccio NFW, with scatter) vs SPARC's RAR tightness (FROZEN_CRITERIA.md).
Run: python3 cfg476_dmo_rar.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.optimize import minimize_scalar, brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MSUN, KPC, H = 6.674e-11, 1.989e30, 3.0857e19, 0.7
RHOC = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)       # kg/m^3
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
def moster(lMh):
    Mh = 10 ** lMh; M1 = 10 ** 11.590
    return math.log10(2 * 0.0351 * Mh / ((Mh / M1) ** -1.376 + (Mh / M1) ** 0.608))
def inv_moster(lMs): return brentq(lambda x: moster(x) - lMs, 9.0, 15.5)
k2 = max(abs(moster(inv_moster(l)) - l) for l in (8.0, 9.5, 10.5, 11.2)) < 1e-6
def nfw_g(Mh, r_m, c):
    R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3); rs = R200 / c
    m = lambda x: np.log(1 + x) - x / (1 + x)
    return G * Mh * MSUN * m(r_m / rs) / m(c) / r_m ** 2
def c_dm(Mh): return 10 ** (0.905 - 0.101 * math.log10(Mh * H / 1e12))
# data arrays
gals = []
for g in GAL:
    R = g["R"] * KPC
    b = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
    ok = (b > 0) & (g["Vobs"] > 0)
    if ok.sum() < 3: continue
    L = g["meta"]["L36"] * 1e9
    vb2 = g["Vbul"][-1] ** 2; vd2 = g["Vdisk"][-1] ** 2; fb = vb2 / max(vb2 + vd2, 1e-9)
    Ms = L * (0.5 * (1 - fb) + 0.7 * fb)
    gals.append(dict(R=R[ok], gb=b[ok], V=g["Vobs"][ok], eV=np.clip(g["eV"][ok], 1, None), lMs=math.log10(max(Ms, 1e6))))
def stat(gb_list, go_list, w_list):
    gb, go, w = (np.concatenate(x) for x in (gb_list, go_list, w_list))
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(C.nu_mono(gb / 10 ** la))) ** 2) / np.sum(w)
    r = minimize_scalar(f, bounds=(-11.5, -9.0), method="bounded", options={"xatol": 1e-5})
    low = gb < 1e-11
    slope = np.polyfit(lgb[low], lgo[low], 1)[0] if low.sum() > 10 else float("nan")
    return math.sqrt(r.fun), 10 ** r.x, slope
dgo = [(g["V"] * 1e3) ** 2 / g["R"] for g in gals]; dw = [1 / (g["eV"] / g["V"]) ** 2 for g in gals]
d_rms, d_a0, d_sl = stat([g["gb"] for g in gals], dgo, dw)
P(f"DATA (N gal {len(gals)}, Q<=2, Upsilon 0.5/0.7): rms {d_rms:.4f} dex, best a0 {d_a0:.3e}, low-g slope {d_sl:.3f}")
P(f"K2 Moster round-trip: {'PASS' if k2 else 'FAIL'}")
rng = np.random.default_rng(76); rows = []
for it in range(200):
    gol, wl = [], []
    for g in gals:
        lMh0 = inv_moster(g["lMs"]); e = 1e-3; sl = (moster(lMh0 + e) - moster(lMh0 - e)) / (2 * e)
        Mh = 10 ** (lMh0 + rng.normal(0, 0.15) / sl); c = c_dm(Mh) * 10 ** rng.normal(0, 0.11)
        gm = (C.nu_mono(g["gb"] / 9.3603e-11) * g["gb"]) if MUT else (g["gb"] + nfw_g(Mh, g["R"], c))
        V = np.sqrt(gm * g["R"]) / 1e3 + rng.normal(0, g["eV"])
        V = np.clip(V, 1, None); gol.append((V * 1e3) ** 2 / g["R"]); wl.append(1 / (g["eV"] / V) ** 2)
    rows.append(stat([g["gb"] for g in gals], gol, wl))
rows = np.array(rows); mr = float(np.median(rows[:, 0])); fr = float(np.mean(rows[:, 0] >= d_rms + 0.05))
v = "REPRODUCES" if mr <= d_rms + 0.02 else "FAILS" if fr >= 0.95 else "MARGINAL"
P(f"MOCKS (200): median rms {mr:.4f} dex (16-84% {np.percentile(rows[:,0],16):.4f}-{np.percentile(rows[:,0],84):.4f}); share >= data+0.05: {fr:.2f} -> DMO-LCDM {v}")
P(f"   emergent a0 median {np.median(rows[:,1]):.3e} (16-84% {np.percentile(rows[:,1],16):.3e}-{np.percentile(rows[:,1],84):.3e}) vs data {d_a0:.3e}; footings 9.36e-11 / 1.13e-10")
P(f"   low-g slope median {np.nanmedian(rows[:,2]):.3f} vs data {d_sl:.3f} (deep-MOND 0.5)")
json.dump(dict(data=dict(rms=d_rms, a0=d_a0, slope=d_sl), mocks=dict(median_rms=mr, share_fail=fr, a0=rows[:, 1].tolist(), slope=rows[:, 2].tolist()), verdict=v, K2=bool(k2)),
          open(os.path.join(HERE, f"cfg476_dmo_rar{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg476_dmo_rar{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(1 if v == "REPRODUCES" else 0)
sys.exit(0 if k2 else 1)
