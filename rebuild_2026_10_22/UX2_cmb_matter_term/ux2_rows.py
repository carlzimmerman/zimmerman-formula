#!/usr/bin/env python3
"""UX2 rows 1-3, 6, 9 on published F: SZ f = x (lambda_s infinite, PC1, PC2) and SZ-simple at lambda_s 1, 2, 10 (PC3), against the law, on H1's AG4b SPARC pipeline, RF2's IC 1613 model, X-COP rows.
Frozen: FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, pickle, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LY = np.linspace(-8, 6, 28001)
def tab(lam):
    if lam is None: return lambda y: 0.5 + np.sqrt(0.25 + 1 / y)
    b = 0.0 if math.isinf(lam) else 1 / lam; Y = 10 ** LY / (1 + b); lo = np.full(Y.shape, -40.0); hi = np.full(Y.shape, 40.0)
    for _ in range(120):
        m = 0.5 * (lo + hi); X = np.exp(m); big = X / (1 + b + b * X) * X > Y if b > 0 else X * X > Y; hi = np.where(big, m, hi); lo = np.where(big, lo, m)
    g = Y + np.exp(0.5 * (lo + hi)); L = np.log10(g)
    return lambda y: 10 ** np.interp(np.log10(np.maximum(y, 1e-8)), LY, L) / y
MODELS = {"law (control)": tab(None), "PC1,PC2 f=x": tab(math.inf), "PC3 ls=10": tab(10.0), "PC3 ls=2": tab(2.0), "PC3 ls=1": tab(1.0)}
R = {}
# SPARC, H1's AG4b pipeline
LN10 = math.log(10); KPC = 3.0857e19; LU0, SU, S0 = math.log10(0.5), 0.10, 0.05; LU = LU0 + np.linspace(-0.5, 0.5, 201); UG = 10 ** LU; D = []
for g in C.load_sparc():
    r, Vo, eV, Vg, Vd, Vb = (np.asarray(g[k], float) for k in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul")); Rm = r * KPC
    gl = (np.sign(Vg) * Vg ** 2 + UG[0] * Vd ** 2 + 1.4 * UG[0] * Vb ** 2) * 1e6 / Rm; gh = (np.sign(Vg) * Vg ** 2 + UG[-1] * Vd ** 2 + 1.4 * UG[-1] * Vb ** 2) * 1e6 / Rm; go = (Vo * 1e3) ** 2 / Rm
    m = (Vo > 0) & (go > 0) & (gl > 0) & (gh > 0) & np.isfinite(go) & (r > 0)
    if m.sum() < 5: continue
    D.append(dict(go=go[m], gas=np.sign(Vg[m]) * Vg[m] ** 2 * 1e6 / Rm[m], star=(Vd[m] ** 2 + 1.4 * Vb[m] ** 2) * 1e6 / Rm[m], sv=2 / LN10 * np.clip(eV[m], 1, None) / np.clip(Vo[m], 1, None), V=float(np.median(Vo[m][-5:]))))
for f, a0 in A0.items():
    for n, nu in MODELS.items():
        rm, U, V = [], [], []
        for d in D:
            gb = d["gas"][:, None] + d["star"][:, None] * UG[None, :]; rr = np.log10(d["go"])[:, None] - np.log10(nu(gb / a0) * gb); c2 = (rr ** 2 / (d["sv"][:, None] ** 2 + S0 ** 2)).sum(0) + ((LU - LU0) / SU) ** 2; i = int(np.argmin(c2))
            rm.append(math.sqrt(np.mean((rr[:, i] / 2) ** 2))); U.append(UG[i]); V.append(d["V"])
        rm, U, V = map(np.array, (rm, U, V)); tilt = float(np.median(U[V < 100]) - np.median(U[V > 150]))
        R.setdefault("sparc", {}).setdefault(f, {})[n] = dict(rms=float(np.median(rm)), U=float(np.median(U)), U_lowV=float(np.median(U[V < 100])), U_highV=float(np.median(U[V > 150])), tilt=tilt, n=len(D))
        P(f"[{f}] SPARC {n:15s}: median rms {np.median(rm):.4f}, Upsilon {np.median(U):.3f} (with prior 0.5 +- 0.10 dex), V<100 {np.median(U[V < 100]):.3f}, V>150 {np.median(U[V > 150]):.3f}, tilt {tilt:+.3f}")
# IC 1613, RF2's numbers
G, MSUN, PC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; KPCm = 1e3 * PC; VROT, I0, RMAX, MS, MG, S_HI = 16.9, 48.0, 2.71, 2.88e7, 5.93e7, 0.075
for f, a0 in A0.items():
    for n, nu in MODELS.items():
        e = {}
        for i in (32.0, 36.0, 38.0, 48.0):
            V = VROT * math.sin(math.radians(I0)) / math.sin(math.radians(i)); gobs = (V * 1e3) ** 2 / (RMAX * KPCm); gN = G * (MS + MG) * MSUN / (RMAX * KPCm) ** 2
            e[str(i)] = float(math.log10(gobs) - math.log10(float(nu(np.array([gN / a0]))[0]) * gN))
        R.setdefault("ic1613", {}).setdefault(f, {})[n] = e; P(f"[{f}] IC 1613 E_HI {n:15s}: " + ", ".join(f"i {k} {v:+.3f} (Z {v / S_HI:+.1f})" for k, v in e.items()))
# X-COP
_C = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb")); GE, MSE, MPCE = _C["const"]["GE"], _C["const"]["MSUNE"], _C["const"]["MPCE"]
for f, a0 in A0.items():
    for n, nu in MODELS.items():
        d = [math.log10(z["MHSE_Msun"] / (float(nu(np.array([GE * z["Mb_Msun"] * MSE / (z["r_kpc"] * 1e3 * MPCE / 1e6) ** 2 / a0]))[0]) * z["Mb_Msun"])) for z in _C["xcop"]["canonical"]["rows"] if z["x"] <= 0.75]
        d = np.array(d); R.setdefault("xcop", {}).setdefault(f, {})[n] = dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), factor=float(10 ** d.mean())); P(f"[{f}] X-COP {n:15s}: {d.mean():+.3f} rms {np.sqrt((d ** 2).mean()):.3f} factor {10 ** d.mean():.2f}")
json.dump(R, open(os.path.join(HERE, "ux2_rows.json"), "w"), indent=1, sort_keys=True); open(os.path.join(HERE, "ux2_rows.out"), "w").write("\n".join(OUT) + "\n")
