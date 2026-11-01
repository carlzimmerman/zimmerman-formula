#!/usr/bin/env python3
"""TP1 read, FROZEN_CRITERIA.md. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
import numpy as np
from scipy.stats import rankdata
H = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(H, "..", ".."); J = json.load(open(os.path.join(H, "tp1_results.json"))); OUT = []
def P(s): print(s); OUT.append(s)
G = {}
for l in open(os.path.join(RT, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) < 18: continue
    try: t = dict(T=float(p[1]), D=float(p[2]), fD=int(p[4]), inc=float(p[5]), L=float(p[7]), SBe=float(p[10]), Rd=float(p[11]), SBd=float(p[12]), MHI=float(p[13]), vf=float(p[15]), Q=int(p[17]))
    except ValueError: continue
    if p[0] in J["blum"] and t["vf"] > 0 and t["Q"] <= 2 and t["inc"] >= 30:
        a = np.loadtxt(os.path.join(RT, "real_research", "data", "sparc_data", p[0] + "_rotmod.dat"), comments="#"); r, vd, vb = a[:, 0], a[:, 4], a[:, 5]; w = 0.7 * np.trapz(vb ** 2, r); t["bul"] = w / (w + 0.5 * np.trapz(vd ** 2, r) + 1e-30); t["ub"] = J["blum"][p[0]]; t["uo"] = J["off"][p[0]]; t["n"] = p[0]; G[p[0]] = t
g = list(G.values()); arr = lambda k: np.array([x[k] for x in g]); v, ub, uo = arr("vf"), arr("ub"), arr("uo"); BN = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]
P("K1 Blumenthal by bin " + str([round(float(np.median(ub[(v >= a) & (v < b)])), 2) for a, b in BN]) + " n " + str([int(((v >= a) & (v < b)).sum()) for a, b in BN]) + " (UR2 0.43 0.52 0.47 0.30 0.36 0.47)")
rng = np.random.default_rng(20261101)
def trough(u, vv):
    t, c = (vv >= 150) & (vv < 250), ((vv >= 100) & (vv < 150)) | ((vv >= 250) & (vv < 400)); a, b = u[t], u[c]; o = np.median(a) - np.median(b); bs = np.median(a[rng.integers(0, len(a), (20000, len(a)))], axis=1) - np.median(b[rng.integers(0, len(b), (20000, len(b)))], axis=1); return o, np.percentile(bs, [2.5, 97.5])
for n, u in (("Blumenthal", ub), ("off", uo)):
    o, ci = trough(u, v); P(f"Trough {n}: {o:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}]: " + ("TROUGH REAL" if ci[1] < 0 or ci[0] > 0 else "NOT DISTINCT"))
o, ci = trough(ub, rng.permutation(v)); P(f"MUTATE shuffled V_flat: {o:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}]")
m = (v >= 100) & (v < 400); lv = np.log10(v[m]); uu = ub[m]; gf = 1.33 * arr("MHI") / (0.5 * arr("L") + 1.33 * arr("MHI")); PR = dict(lgSBeff=np.log10(arr("SBe")), lgSBdisk=np.log10(arr("SBd")), lgRd=np.log10(arr("Rd")), gasfrac=gf, T=arr("T"), bulge=arr("bul"), D=arr("D"))
def resid(y): rk = rankdata(y).astype(float); c = np.polyfit(lv, rk, 1); return rk - np.polyval(c, lv)
ru = resid(uu); P(f"\nPredictors, 100-400 km/s, n {m.sum()}, partial Spearman with U_Blum at fixed lg V_flat; line p < {0.05 / 7:.4f}"); RES = {}
for k, x in PR.items():
    rx = resid(x[m]); s = np.corrcoef(ru, rx)[0, 1]; pm = np.array([np.corrcoef(rng.permutation(ru), rx)[0, 1] for _ in range(20000)]); pv = float((np.sum(np.abs(pm) >= abs(s)) + 1) / 20001); RES[k] = (float(s), pv); P(f"  {k:9s} rho {s:+.3f} p {pv:.5f} {'PREDICTOR' if pv < 0.05 / 7 else ''}")
rx = resid(rng.permutation(PR["lgSBeff"][m])); s = np.corrcoef(ru, rx)[0, 1]; P(f"MUTATE shuffled SB: rho {s:+.3f}")
fd = arr("fD")[m]; P("\nDistance method, U_Blum median: " + ", ".join(f"f_D {d}: {np.median(uu[fd == d]):.2f} (n {(fd == d).sum()})" for d in sorted(set(fd))))
b = (v >= 150) & (v < 250)
for k, s in RES.items():
    if s[1] < 0.05 / 7:
        x = PR[k][b]; c = np.median(x); P(f"split {k} at {c:.3f} within 150-250: low half U {np.median(ub[b][x < c]):.2f} n {(x < c).sum()}, high half U {np.median(ub[b][x >= c]):.2f} n {(x >= c).sum()}")
P(f"\ngrid-end flags: U_Blum at <= 0.30: {(ub[b] <= 0.30).sum()} of {b.sum()} in 150-250; all: {(ub <= 0.30).sum()} of {len(ub)}")
P("LABEL: " + ", ".join(k for k, s in RES.items() if s[1] < 0.05 / 7) if any(s[1] < 0.05 / 7 for s in RES.values()) else "LABEL: NO PREDICTOR")
open(os.path.join(H, "tp1.out"), "w").write("\n".join(OUT) + "\n")
