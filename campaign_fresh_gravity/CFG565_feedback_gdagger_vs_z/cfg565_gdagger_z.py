#!/usr/bin/env python3
"""CFG565: sign of LCDM-with-feedback's g-dagger(z) (FROZEN_CRITERIA.md). Reuses CFG476/477. Run: python3 cfg565_gdagger_z.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
argv = sys.argv; sys.argv = [argv[0]]
ns = {"__name__": "c476"}; p476 = os.path.join(LANES, "CFG476_lcdm_dmo_rar_tightness", "cfg476_dmo_rar.py"); ns["__file__"] = p476
src = open(p476).read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:src.index("rng = np.random.default_rng(76)")], ns)
n7 = {"__name__": "c477", "np": np, "math": math}; p477 = os.path.join(LANES, "CFG477_lcdm_dc14_rar", "cfg477_dc14.py"); s7 = open(p477).read()
exec(s7[s7.index("XG = np.logspace"):s7.index("def halo_g")], n7)
sys.argv = argv
gals, stat, G, MSUN = ns["gals"], ns["stat"], ns["G"], ns["MSUN"]
XG, menc, dc14 = n7["XG"], n7["menc"], n7["dc14"]
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
H, OM = 0.7, 0.315
def E(z): return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)
RHOC0 = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
def moster(lMh, z):
    zz = z / (1 + z); M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz; b = 1.376 - 0.826 * zz; g = 0.608 + 0.329 * zz
    Mh = 10 ** lMh; return math.log10(2 * N * Mh / ((Mh / M1) ** -b + (Mh / M1) ** g))
def inv(lMs, z):
    lo, hi = moster(8.5, z), moster(16.0, z)
    if lMs <= lo: return 8.5
    if lMs >= hi: return 16.0
    return brentq(lambda x: moster(x, z) - lMs, 8.5, 16.0)
def cdm(M, z):
    a = 0.520 + 0.385 * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M * H / 1e12))
k2 = abs(moster(12.0, 0.0) - ns["moster"](12.0)) < 1e-12
def run(z, seed):
    zh = 0.0 if MUT else z
    rhoc = RHOC0 * E(zh) ** 2; s = (1 + z) ** -0.75
    rng = np.random.default_rng(seed); rows = []
    pre = []
    for g in gals:
        l0 = inv(g["lMs"], zh); e = 1e-3; sl = (moster(l0 + e, zh) - moster(l0 - e, zh)) / (2 * e); pre.append((l0, max(sl, 1e-3)))
    for _ in range(100):
        gbl, gol, wl = [], [], []
        for g, (l0, sl) in zip(gals, pre):
            r = g["R"] * s; gb = g["gb"] / s ** 2
            Mh = 10 ** (l0 + rng.normal(0, 0.15) / sl); c0 = cdm(Mh, zh) * 10 ** rng.normal(0, 0.11)
            a_, b_, g_, cb = dc14(g["lMs"] - math.log10(Mh))[:4]; cc = c0 * (1 + cb)
            R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = R200 / cc
            m = menc(a_, b_, g_); gh = G * Mh * MSUN * np.interp(r / rs, XG, m) / np.interp(cc, XG, m) / r ** 2
            V = np.sqrt((gb + gh) * r) / 1e3 + rng.normal(0, g["eV"]); V = np.clip(V, 1, None)
            gbl.append(gb); gol.append((V * 1e3) ** 2 / r); wl.append(1 / (g["eV"] / V) ** 2)
        rows.append(stat(gbl, gol, wl)[1])
    return np.array(rows)
res = {}; base = run(0.0, 565)
k1 = abs(np.median(base) / 9.686e-11 - 1) < 0.03
P(f"K1 z=0 g-dagger {np.median(base):.3e} vs CFG477 9.686e-11 -> {'PASS' if k1 else 'FAIL'}; K2 Moster z-terms vanish at z=0: {'PASS' if k2 else 'FAIL'}")
fw = {1.0: (1.0, 1.77), 2.0: (0.87, 3.0), 2.5: (0.805, 3.7)}
for z in (1.0, 2.0, 2.5):
    gz = run(z, 565); ratio = gz / base
    res[str(z)] = dict(median=float(np.median(ratio)), p16=float(np.percentile(ratio, 16)), p84=float(np.percentile(ratio, 84)), gd=float(np.median(gz)))
    P(f"z = {z}: feedback-LCDM g-dagger/g-dagger(0) = {np.median(ratio):.2f} (16-84% {np.percentile(ratio,16):.2f}-{np.percentile(ratio,84):.2f}) | framework DE-tracking ~{fw[z][0]}, flat 1.0, a0~H(z) {fw[z][1]}")
r25 = res["2.5"]
if r25["p16"] > 1.3: v = "FEEDBACK RISES"
elif 0.85 <= r25["p16"] and r25["p84"] <= 1.15: v = "FEEDBACK FLAT"
elif r25["p84"] < 0.85: v = "FEEDBACK FALLS"
else: v = "INTERMEDIATE"
P(f"VERDICT: {v}")
json.dump(dict(K1=bool(k1), K2=bool(k2), z0=float(np.median(base)), res=res, verdict=v), open(os.path.join(HERE, f"cfg565_gdagger_z{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg565_gdagger_z{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    m = json.load(open(os.path.join(HERE, "cfg565_gdagger_z_results.json")))["res"]["2.5"]["median"]
    ok = abs(r25["median"] / m - 1) > 0.10; P(f"MUTATE: ratio {m:.2f} -> {r25['median']:.2f} -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if (k1 and k2) else 1)
