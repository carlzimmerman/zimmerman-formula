#!/usr/bin/env python3
"""CFG477: LCDM with DC14 feedback cores vs SPARC's RAR (FROZEN_CRITERIA.md). Reuses CFG476's data, AM and statistic. Run: python3 cfg477_dc14.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
src = open(os.path.join(LANES, "CFG476_lcdm_dmo_rar_tightness", "cfg476_dmo_rar.py")).read()
ns = {"__file__": os.path.join(LANES, "CFG476_lcdm_dmo_rar_tightness", "cfg476_dmo_rar.py"), "__name__": "c476"}
argv = sys.argv; sys.argv = [argv[0]]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:src.index("rng = np.random.default_rng(76)")], ns)
sys.argv = argv
gals, stat, inv_moster, moster, c_dm, C = ns["gals"], ns["stat"], ns["inv_moster"], ns["moster"], ns["c_dm"], ns["C"]
G, MSUN, RHOC, d_rms, d_a0, d_sl = ns["G"], ns["MSUN"], ns["RHOC"], ns["d_rms"], ns["d_a0"], ns["d_sl"]
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
XG = np.logspace(-5, 2.5, 600)
def menc(a, b, g):
    rho = XG ** (-g) * (1 + XG ** a) ** (-(b - g) / a)
    f = XG ** 3 * rho                                   # integrate x^2 rho dx = x^3 rho dlnx
    return np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(np.log(XG)))])
def dc14(X):
    Xc = min(max(X, -4.1), -1.3)
    a = 2.94 - math.log10((10 ** (Xc + 2.33)) ** -1.08 + (10 ** (Xc + 2.33)) ** 2.29)
    b = 4.23 + 1.34 * Xc + 0.26 * Xc ** 2
    g = -0.06 + math.log10((10 ** (Xc + 2.56)) ** -0.68 + 10 ** (Xc + 2.56))
    return a, b, g, math.exp(3.4 * (Xc + 4.5)) * 1e-5, (Xc != X)
def halo_g(Mh, r_m, c, abg):
    R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3); rs = R200 / c
    m = menc(*abg); mx = np.interp(r_m / rs, XG, m); mc = np.interp(c, XG, m)
    return G * Mh * MSUN * mx / mc / r_m ** 2
# K2: enclosed mass at R200 = Mh
abg = dc14(-2.7)[:3]; Mh = 1e11; c = c_dm(Mh)
R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
k2 = abs(halo_g(Mh, np.array([R200]), c, abg)[0] * R200 ** 2 / G / MSUN / Mh - 1) < 1e-4
def run(seed, mode):
    rng = np.random.default_rng(seed); rows = []; clipped = 0; n = 0
    for it in range(200):
        gol, wl = [], []
        for g in gals:
            lMh0 = inv_moster(g["lMs"]); e = 1e-3; sl = (moster(lMh0 + e) - moster(lMh0 - e)) / (2 * e)
            Mh = 10 ** (lMh0 + rng.normal(0, 0.15) / sl); c0 = c_dm(Mh) * 10 ** rng.normal(0, 0.11)
            if mode == "nfw":
                gh = halo_g(Mh, g["R"], c0, (1.0, 3.0, 1.0))
            else:
                X = g["lMs"] - math.log10(Mh) - (3 if MUT else 0)
                a, b, gg, cboost, clip = dc14(X); clipped += clip; n += 1
                gh = halo_g(Mh, g["R"], c0 * (1 + cboost), (a, b, gg))
            V = np.sqrt((g["gb"] + gh) * g["R"]) / 1e3 + rng.normal(0, g["eV"])
            V = np.clip(V, 1, None); gol.append((V * 1e3) ** 2 / g["R"]); wl.append(1 / (g["eV"] / V) ** 2)
        rows.append(stat([g["gb"] for g in gals], gol, wl))
    return np.array(rows), (clipped / n if n else 0.0)
k1rows, _ = run(76, "nfw"); k1m = float(np.median(k1rows[:, 0])); k1 = abs(k1m - 0.2052) < 0.005
P(f"K1 forced-NFW generic integrator vs CFG476 median 0.2052: {k1m:.4f} -> {'PASS' if k1 else 'FAIL'};  K2 M(<R200) = Mh: {'PASS' if k2 else 'FAIL'}")
rows, clipf = run(77, "dc14")
mr = float(np.median(rows[:, 0])); fr = float(np.mean(rows[:, 0] >= d_rms + 0.05))
v = "REPRODUCES" if mr <= d_rms + 0.02 else "FAILS" if fr >= 0.95 else "MARGINAL"
P(f"DATA rms {d_rms:.4f}, a0 {d_a0:.3e}, low-g slope {d_sl:.3f}")
P(f"DC14 MOCKS (200{', MUTATE X-3' if MUT else ''}): median rms {mr:.4f} (16-84% {np.percentile(rows[:,0],16):.4f}-{np.percentile(rows[:,0],84):.4f}); share >= data+0.05 {fr:.2f}; X clipped to DC14 range in {clipf:.2f} of draws -> {v}")
P(f"   emergent a0 median {np.median(rows[:,1]):.3e} (16-84% {np.percentile(rows[:,1],16):.3e}-{np.percentile(rows[:,1],84):.3e}); low-g slope {np.nanmedian(rows[:,2]):.3f}")
P(f"   vs CFG476 DMO: rms 0.2052 -> {mr:.4f}; a0 3.856e-10 -> {np.median(rows[:,1]):.3e}")
json.dump(dict(K1=k1m, K1ok=bool(k1), K2=bool(k2), median_rms=mr, share=fr, a0=rows[:, 1].tolist(), slope=rows[:, 2].tolist(), clipped=clipf, verdict=v),
          open(os.path.join(HERE, f"cfg477_dc14{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg477_dc14{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg477_dc14_results.json")))["median_rms"]
    ok = mr - base > 0.02; P(f"MUTATE: median rms {base:.4f} -> {mr:.4f} -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if (k1 and k2) else 1)
