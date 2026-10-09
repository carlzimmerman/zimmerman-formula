#!/usr/bin/env python3
"""CFG560: bar rotation rate R vs the law's dark fraction at corotation (FROZEN_CRITERIA.md). Run: python3 cfg560_bars.py [--mutate]"""
import os, sys, json, math, io, contextlib
import numpy as np
from scipy.stats import spearmanr, rankdata
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES); sys.path.insert(0, LANES)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
KPC = 3.0857e19; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
lines = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research/data/bars/geron2023_manga_barspeeds_table3.tsv")) if l.strip() and not l.startswith("#")]
hdr = [h.strip() for h in lines[0]]; rows = lines[3:]
def col(name): i = hdr.index(name); return np.array([float(r[i]) if r[i].strip() not in ("", "nan") else np.nan for r in rows])
Om, Rcr, R, eR, ER = col("Omph"), col("Rcrph"), col("R"), col("e_R"), col("E_R")
ok = np.isfinite(Om) & np.isfinite(Rcr) & np.isfinite(R) & (Om > 0) & (Rcr > 0) & (R > 0) & np.isfinite(eR) & np.isfinite(ER) & (eR > 0) & (ER > 0)
Om, Rcr, R, sR = Om[ok], Rcr[ok], R[ok], 0.5 * (ER[ok] - eR[ok])   # e_R/E_R are the published lower/upper BOUNDS (fixed after the first run; disclosed)
k1 = (ok.sum() == 210) and abs(np.median(R) - 1.663) < 0.01
P(f"K1 rows {ok.sum()} (h29: 210), median R {np.median(R):.3f} (h29 1.663) -> {'PASS' if k1 else 'FAIL'}")
gobs = (Om * Rcr * 1e3) ** 2 / (Rcr * KPC)                      # m/s^2
def invert(go, a0): return brentq(lambda gb: float(C.nu_mono(np.array([gb / a0]))[0]) * gb - go, go * 1e-6, go, xtol=1e-30, rtol=1e-14)   # tolerance fixed after the first run (K2), disclosed
gt = 3e-11; k2 = abs(float(C.nu_mono(np.array([invert(gt, A0['canonical']) / A0['canonical']]))[0]) * invert(gt, A0['canonical']) / gt - 1) < 1e-8
P(f"K2 inversion round-trip: {'PASS' if k2 else 'FAIL'}; median g_obs(R_CR) = {np.median(gobs)/A0['canonical']:.2f} a0 (canonical)")
if MUT: R = np.random.default_rng(560).permutation(R)
def partial_spearman(x, y, z):
    rx, ry, rz = (rankdata(v) for v in (x, y, z))
    res = lambda a, b: a - np.polyval(np.polyfit(b, a, 1), b)
    return np.corrcoef(res(rx, rz), res(ry, rz))[0, 1]
def perm_p(stat, x, y, z=None, n=4000, seed=5600):
    rng = np.random.default_rng(seed); obs = stat(x, y, z); c = 0
    for _ in range(n):
        xs = rng.permutation(x); c += abs(stat(xs, y, z)) >= abs(obs)
    return obs, (c + 1) / (n + 1)
s1 = lambda x, y, z: spearmanr(x, y)[0]
s2 = lambda x, y, z: partial_spearman(x, y, z)
res = {}
for foot, a0 in A0.items():
    gbar = np.array([invert(g, a0) for g in gobs]); fd = 1 - gbar / gobs
    for lab, m in (("ALL", np.ones_like(R, bool)), ("q<=0.35", sR / R <= 0.35), ("q<=0.20", sR / R <= 0.20)):
        r1, p1 = perm_p(s1, R[m], fd[m]); r2, p2 = perm_p(s2, R[m], fd[m], Rcr[m]); r3 = spearmanr(R[m], gobs[m] / a0)[0]
        res[f"{foot}|{lab}"] = dict(n=int(m.sum()), S1=r1, p1=p1, S2=r2, p2=p2, S3=r3, fdark_median=float(np.median(fd[m])))
        P(f"{foot:9s} {lab:8s} N {m.sum():3d}: median f_dark {np.median(fd[m]):.2f}; S1 rho(R,f_dark) {r1:+.3f} (p {p1:.3f}); S2 partial|R_CR {r2:+.3f} (p {p2:.3f}); S3 rho(R,g/a0) {r3:+.3f}")
pr = res["canonical|q<=0.35"]
if pr["S2"] > 0 and pr["p2"] < 0.01 and pr["S1"] > 0: v = "FRICTION SIGNAL"
elif pr["S2"] <= 0 or (pr["p2"] > 0.05 and pr["p1"] > 0.05): v = "NO FRICTION SIGNAL"
else: v = "HINT"
P(f"VERDICT (primary: canonical, q<=0.35, S2): {v}")
json.dump(dict(K1=bool(k1), K2=bool(k2), res=res, verdict=v), open(os.path.join(HERE, f"cfg560_bars{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg560_bars{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(1 if pr["p2"] > 0.05 else 0)
sys.exit(0 if (k1 and k2) else 1)
