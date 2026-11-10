#!/usr/bin/env python3
"""KL1 PART C, AMENDMENT C3 (post hoc, a5d8d7f322): the polished DES Y3 scan for the gate, and the same polish on DES's KC1 base.
Every grid sigma8 is refitted from kl1_lib.fit's default starts, then restarted from the lowest point until a restart improves by
< 1e-4 (at most 8), with two sweeps along the grid (each point also started from its neighbour's polished vector); the lowest
chi^2 per point is kept and CO2's parabola rule applied. Machinery as kl1c.py (Part A's kl1_lib; C0's R1 from co2_posthoc.py;
layouts from kl1c_gas.json; A2's covariance at the model, copied).

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1c_polish.py <footing>     -> parts/polish_<footing>.json, .out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as CH
import kl1_lib as K1
FT = sys.argv[1]; assert FT in K1.FOOTS
HERE = K1.HERE; G, SURV = K1.G, K1.SURV; T0 = time.time(); LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
K, SN, PZ0 = K1.K, K1.SN, K1.PZ0
rr = np.array(SN["zi"]["P"]) / (SN["zi"]["D"] ** 2 * G["P_lin0"](K))
w = np.clip(1 - np.log(np.maximum(K, 0.3) / 0.3) / math.log(1.0 / 0.3), 0, 1); PZV = {None: PZ0, "R1": {z: PZ0[z] / rr ** w for z in PZ0}}
NU = json.load(open(os.path.join(HERE, "kl1_nu.json"))); GC = json.load(open(os.path.join(HERE, "kl1c_gas.json"))); PA = json.load(open(os.path.join(HERE, "parts", f"rows_{FT}.json")))
S8 = NU["A1"][FT]["sigma8_nu"]; R = dict(co1=np.array(K1.HM["primary"][FT]["R_tot"]), **{k: np.array(v["R_tot"]) for k, v in GC["rows"][FT].items()})
def Pm_of(Rk, s8, pz): K1.setP(PZV[pz]); return K1.Pmat(K1.run_of(Rk, (s8 / K1.S8E) ** 2, "resp"), "F")
sn = "DES"; S = SURV[sn]; pub = np.where(S["pubkeep"])[0]; fid = PA["rows"]["A0"][sn]["best_sigma8"]
Pf = Pm_of(R["co1"], fid, None); G1, N1 = K1.gauss_cov(S, pub, K1.cell_full(S, Pf)); Cp = S["cov"][np.ix_(pub, pub)]
nf = np.diag(N1) / np.diag(G1); nd = nf >= 0.8; area = float(1.0 / np.median(np.diag(Cp)[nd] / np.diag(G1)[nd])); Rr = Cp - G1 / area; xif = K1.xi_nominal(S, Pf)
km = K1.keep_mask(sn); D = K1.subset(S, km); kept = np.where(km)[0]; pos = {int(g): i for i, g in enumerate(pub)}; kp = np.array([pos[int(g)] for g in kept])
x00, lo, hi, unpack, prior = G["nuis_spec"](S, 1.0, True); BND = list(zip(lo, hi))
def setup(Rk, pz, s8):
    Pm = Pm_of(Rk, s8, pz); Gm, _ = K1.gauss_cov(S, kept, K1.cell_full(S, Pm)); s = np.clip(K1.xi_nominal(S, Pm)[kept] / xif[kept], 0.5, 3.0)
    Ci = np.linalg.inv(Gm / area + Rr[np.ix_(kp, kp)] * np.outer(s, s)); return Pm, Ci
def obj(Pm, Ci):
    def f(x):
        r = D["d"] - G["theory"](S, D, unpack(x), Pm, "PM"); return float(r @ Ci @ r) + prior(x)
    return f
def polish(f, xs, fun0):
    best_x, best_f = np.array(xs), fun0
    for _ in range(8):
        r = minimize(f, best_x, method="L-BFGS-B", bounds=BND, options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
        fv = min(float(r.fun), f(r.x)); xv = r.x if f(r.x) <= float(r.fun) + 1e-12 else r.x
        if fv < best_f - 1e-4: best_x, best_f = xv, fv
        else:
            if fv < best_f: best_x, best_f = xv, fv
            break
    return best_x, best_f
def scan_polished(Rk, pz):
    grid = list(np.round(K1.GRID, 6)); cache = {}
    def point(s, extra=None):
        Pm, Ci = setup(Rk, pz, s); f = obj(Pm, Ci)
        if s not in cache:
            d = K1.fit(S, D, Pm, Cinv=Ci); xb, fb = polish(f, d["x"], f(np.array(d["x"])))
            cache[s] = [fb, xb]
        if extra is not None:
            xb, fb = polish(f, extra, f(np.array(extra)))
            if fb < cache[s][0]: cache[s] = [fb, xb]
        return cache[s]
    while True:
        for s in grid: point(s)
        prev = None
        for s in grid:                                        # sweep up
            if prev is not None: point(s, cache[prev][1])
            prev = s
        prev = None
        for s in reversed(grid):                              # sweep down
            if prev is not None: point(s, cache[prev][1])
            prev = s
        c2 = np.array([cache[s][0] for s in grid]); i = int(np.argmin(c2))
        if i == 0 and grid[0] > 0.60 + 1e-9: grid = [round(grid[0] - 0.0125, 6)] + grid; continue
        if i == len(grid) - 1 and grid[-1] < 1.00 - 1e-9: grid = grid + [round(grid[-1] + 0.0125, 6)]; continue
        break
    ss = np.array(grid); c2 = np.array([cache[s][0] for s in grid]); i = int(np.argmin(c2)); lo_, hi_ = max(i - 2, 0), min(i + 3, len(ss))
    co = np.polyfit(ss[lo_:hi_], c2[lo_:hi_], 2); sb = float(-co[1] / (2 * co[0])); wd = 1 / math.sqrt(co[0])
    # the target, polished from the nearest grid points' vectors
    Pm, Ci = setup(Rk, pz, S8); f = obj(Pm, Ci); d = K1.fit(S, D, Pm, Cinv=Ci); xb, fb = polish(f, d["x"], f(np.array(d["x"])))
    for s in sorted(grid, key=lambda q: abs(q - S8))[:2]:
        x2, f2 = polish(f, cache[s][1], f(np.array(cache[s][1])))
        if f2 < fb: xb, fb = x2, f2
    r_ = D["d"] - G["theory"](S, D, unpack(xb), Pm, "PM"); c2d = float(r_ @ Ci @ r_)
    return dict(sigma8=ss.tolist(), chi2=c2.tolist(), best_sigma8=sb, width=wd, gap_widths=(S8 - sb) / wd, target_chi2=fb, target_chi2_data=c2d, p=float(CH.sf(c2d, D["N"])),
                label=K1.lab(float(CH.sf(c2d, D["N"]))))
RES = dict(lane="KL1", part="C polish (AMENDMENT C3, post hoc)", amendment="a5d8d7f322", foot=FT, note="kappa = 1/2 FITTED; not theory closed", rows={})
for name, Rk, pz in (("GATE", R["A3_AD"], "R1"), ("KC1_base", R["A3_NR"], None)):
    o = scan_polished(Rk, pz); RES["rows"][name] = o
    P(f"[{FT}] DES {name} polished: target chi2 {o['target_chi2']:.3f} (data {o['target_chi2_data']:.3f}), p {o['p']:.3f} {o['label']}; best {o['best_sigma8']:.4f} +- {o['width']:.4f}, gap {o['gap_widths']:+.2f}   [{time.time() - T0:.0f} s]")
    json.dump(RES, open(os.path.join(HERE, "parts", f"polish_{FT}.json"), "w"), indent=1)
K1.setP(PZ0)
open(os.path.join(HERE, "parts", f"polish_{FT}.out"), "w").write("\n".join(LOG) + "\n")
