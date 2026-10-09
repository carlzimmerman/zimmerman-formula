#!/usr/bin/env python3
"""CFG479: robustness of the RAR low-g slope as a law-vs-LCDM+feedback discriminator (FROZEN_CRITERIA.md). Run: python3 cfg479_slope.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MSUN, KPC, H = 6.674e-11, 1.989e30, 3.0857e19, 0.7
RHOC = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def moster(lMh):
    Mh = 10 ** lMh; M1 = 10 ** 11.590
    return math.log10(2 * 0.0351 * Mh / ((Mh / M1) ** -1.376 + (Mh / M1) ** 0.608))
def behroozi_form(le, lM1, al, de, ga):
    f = lambda x: -math.log10(10 ** (al * x) + 1) + de * (math.log10(1 + math.exp(x))) ** ga / (1 + math.exp(min(10 ** (-x), 700.0)))   # overflow guard (fixed after the first launch crashed; disclosed)
    return lambda lMh: le + lM1 + f(lMh - lM1) - f(0.0)
SHMR = {"Moster13": moster, "Behroozi13": behroozi_form(-1.777, 11.514, -1.412, 3.508, 0.316), "Kravtsov18": behroozi_form(-1.642, 11.35, -1.779, 4.394, 0.547)}
def inv(fn, lMs):
    # clip to the SHMR's range on [8.5, 16] (fixed after the second launch crashed on one Upsilon 0.7 galaxy; disclosed)
    lo, hi = fn(8.5), fn(16.0)
    if lMs <= lo: return 8.5
    if lMs >= hi: return 16.0
    return brentq(lambda x: fn(x) - lMs, 8.5, 16.0)
def c_dm(Mh): return 10 ** (0.905 - 0.101 * math.log10(Mh * H / 1e12))
XG = np.logspace(-5, 2.5, 600)
def menc_gen(a, b, g):
    f = XG ** 3 * XG ** (-g) * (1 + XG ** a) ** (-(b - g) / a)
    return np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(np.log(XG)))])
def dc14(X):
    Xc = min(max(X, -4.1), -1.3)
    a = 2.94 - math.log10((10 ** (Xc + 2.33)) ** -1.08 + (10 ** (Xc + 2.33)) ** 2.29)
    b = 4.23 + 1.34 * Xc + 0.26 * Xc ** 2
    g = -0.06 + math.log10((10 ** (Xc + 2.56)) ** -0.68 + 10 ** (Xc + 2.56))
    return a, b, g, math.exp(3.4 * (Xc + 4.5)) * 1e-5
mu = lambda x: np.log(1 + x) - x / (1 + x)
def halo_g(model, Mh, c, r, lMs, Rhalf):
    R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
    if model == "DMO":
        rs = R200 / c; M = Mh * mu(r / rs) / mu(c)
    elif model == "DC14":
        a, b, g, cb = dc14(lMs - math.log10(Mh)); cc = c * (1 + cb); rs = R200 / cc
        m = menc_gen(a, b, g); M = Mh * np.interp(r / rs, XG, m) / np.interp(cc, XG, m)
    else:   # coreNFW, n = 1
        rs = R200 / c; rc = 1.75 * Rhalf; M = Mh * mu(r / rs) / mu(c) * (np.tanh(r / rc) if rc > 0 else 1.0)
    return G * M * MSUN / r ** 2
def build(U):
    out = []
    for g in C.load_sparc():
        if not (g["meta"] and g["meta"]["Q"] <= 2): continue
        R = g["R"] * KPC
        b = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2) * 1e6 / R
        ok = (b > 0) & (g["Vobs"] > 0)
        if ok.sum() < 3: continue
        vb2 = g["Vbul"][-1] ** 2; vd2 = g["Vdisk"][-1] ** 2; fb = vb2 / max(vb2 + vd2, 1e-9)
        Ms = g["meta"]["L36"] * 1e9 * (U * (1 - fb) + 1.4 * U * fb)
        out.append(dict(R=R[ok], gb=b[ok], V=g["Vobs"][ok], eV=np.clip(g["eV"][ok], 1, None), lMs=math.log10(max(Ms, 1e6)), Rhalf=1.68 * g["meta"]["Rdisk"] * KPC))
    return out
def slope(gbl, gol):
    gb, go = np.concatenate(gbl), np.concatenate(gol); m = gb < 1e-11
    return float(np.polyfit(np.log10(gb[m]), np.log10(go[m]), 1)[0])
# K2: coreNFW rc -> 0 equals DMO
r = np.logspace(19, 22, 50); k2 = np.max(np.abs(halo_g("cNFW", 1e11, 10.0, r, 9.0, 0.0) / halo_g("DMO", 1e11, 10.0, r, 9.0, 0.0) - 1)) < 1e-6
res = {}
for U in (0.4, 0.5, 0.7):
    gals = build(U)
    dgo = [(g["V"] * 1e3) ** 2 / g["R"] for g in gals]; ds = slope([g["gb"] for g in gals], dgo)
    rng = np.random.default_rng(79); bs = []
    for _ in range(500):
        i = rng.integers(0, len(gals), len(gals)); bs.append(slope([gals[k]["gb"] for k in i], [dgo[k] for k in i]))
    sd = float(np.std(bs)); res[f"U{U}|data"] = dict(slope=ds, sd=sd)
    P(f"Upsilon {U}: DATA slope {ds:.3f} +- {sd:.3f} (N gal {len(gals)})")
    def mocks(fn_g):
        rng = np.random.default_rng(791); out = []
        for _ in range(100):
            gol = []
            for g in gals:
                V = np.sqrt(fn_g(g, rng) * g["R"]) / 1e3 + rng.normal(0, g["eV"]); V = np.clip(V, 1, None)
                gol.append((V * 1e3) ** 2 / g["R"])
            out.append(slope([g["gb"] for g in gals], gol))
        return np.array(out)
    for foot, a0 in A0.items():
        s = mocks(lambda g, rng, a0=a0: C.nu_mono(g["gb"] / a0) * g["gb"])
        m, w = float(np.median(s)), 0.5 * float(np.percentile(s, 84) - np.percentile(s, 16)); z = (m - ds) / math.hypot(sd, w)
        res[f"U{U}|law|{foot}"] = dict(median=m, half=w, z=z); P(f"   law ({foot:9s}) mock slope {m:.3f} +- {w:.3f}: data - law = {-z:+.2f} sigma")
    for sh, fn in SHMR.items():
        pre = []
        for g in gals:
            l0 = inv(fn, g["lMs"]); e = 1e-3; sl = (fn(l0 + e) - fn(l0 - e)) / (2 * e); pre.append((l0, sl))
        for model in ("DMO", "DC14", "cNFW"):
            def fg(g, rng, model=model, pre=pre, gals=gals):
                k = gals.index(g) if False else g["_k"]
                l0, sl = pre[k]; Mh = 10 ** (l0 + rng.normal(0, 0.15) / sl); c = c_dm(Mh) * 10 ** rng.normal(0, 0.11)
                if MUT: return C.nu_mono(g["gb"] / A0["canonical"]) * g["gb"]
                return g["gb"] + halo_g(model, Mh, c, g["R"], g["lMs"], g["Rhalf"])
            for k, g in enumerate(gals): g["_k"] = k
            s = mocks(fg); m, w = float(np.median(s)), 0.5 * float(np.percentile(s, 84) - np.percentile(s, 16)); z = (m - ds) / math.hypot(sd, w)
            res[f"U{U}|{sh}|{model}"] = dict(median=m, half=w, z=z)
            P(f"   {sh:10s} {model:4s}: mock slope {m:.3f} +- {w:.3f}; (mock - data)/sigma = {z:+.2f}")
fb = [v["z"] for k, v in res.items() if k.endswith("|DC14") or k.endswith("|cNFW")]
if all(z > 3 for z in fb): v = "SLOPE DISCRIMINATES (robust)"
elif any(abs(z) < 2 for z in fb): v = "NOT ROBUST"
else: v = "PARTIAL"
k1 = abs(res["U0.5|Moster13|DC14"]["median"] - 0.754) < 0.02
P(f"K1 Moster/DC14/U0.5 vs CFG477 0.754: {res['U0.5|Moster13|DC14']['median']:.3f} -> {'PASS' if k1 else 'FAIL'}; K2 coreNFW rc->0 = NFW: {'PASS' if k2 else 'FAIL'}")
P(f"feedback cells: min z {min(fb):+.2f}, max z {max(fb):+.2f} -> VERDICT: {v}")
json.dump(dict(res=res, verdict=v, K1=bool(k1), K2=bool(k2)), open(os.path.join(HERE, f"cfg479_slope{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg479_slope{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(1 if v == "NOT ROBUST" else 0)
sys.exit(0 if (k1 and k2) else 1)
