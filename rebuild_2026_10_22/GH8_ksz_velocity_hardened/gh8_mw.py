#!/usr/bin/env python3
"""GH8 MW-mass verdict, run only because the control validated: hardened velocities, blank pixels dropped, weights."""
import os, json
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, healpy as hp
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W7, W8 = os.path.join(EXT, "gh7_work"), os.path.join(EXT, "gh8_work")
assert json.load(open(os.path.join(HERE, "gh8_control.json")))["validated"]
C_ = np.load(os.path.join(W7, "gh7_cap.npz")); L_ = np.load(os.path.join(W7, "gh7_lenses.npz")); J = json.load(open(os.path.join(HERE, "gh8_vel.json"))); V = np.load(os.path.join(W8, "gh8_v.npy")); G32 = np.load(os.path.join(W8, "gh8_good32.npy")); RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
ra_, de_ = L_["ra"], L_["dec"]; g = C_["good"] & G32[hp.ang2pix(32, ra_, de_, lonlat=True)]; print("lenses", int(C_["good"].sum()), "->", int(g.sum()), flush=True)
cap0, iz0, il0, v0, ra, de, ss = C_["cap"][g].astype(np.float64), C_["iz"][g], C_["il"][g], V[g].astype(np.float64) / 299792.458, ra_[g], de_[g], (L_["sfr"] - L_["lm"])[g]; TCMB = 2.72548e6
Rs = {"fm": J["R_fm"], "cut": J["R_cut"], "ctx": J["R_ctx"]}; KS = ("1.0", "1.8", "3.0"); rng = np.random.default_rng(828); print("R", Rs, flush=True)
for i in range(10): cap0[iz0 == i] -= cap0[iz0 == i].mean(axis=0)
pix = hp.ang2pix(8, ra, de, lonlat=True)
def weights(c, p):
    w = np.tile(1 / c.var(axis=0), (len(c), 1))
    for q0 in np.unique(p):
        q = p == q0
        if q.sum() >= 500: w[q] = 1 / c[q].var(axis=0)
    return w
def est(c, u, w): return -np.sum(w * c * u[:, None], axis=0) / np.sum(w * (u * u)[:, None], axis=0)
def shuf(u, iz, r):
    o = u.copy()
    for b in range(10):
        q = np.where(iz == b)[0]; o[q] = u[r.permutation(q)]
    return o
def run(sel, label, nsh=2200):
    c, u, iz, il = cap0[sel].copy(), v0[sel].copy(), iz0[sel], il0[sel]; w = weights(c, pix[sel])
    for b in range(10):
        q = iz == b; c[q] -= np.sum(w[q] * c[q], axis=0) / np.sum(w[q], axis=0); u[q] -= u[q].mean()
    wu = np.sum(w * (u * u)[:, None], axis=0)
    mod = {k: np.sum(w * C_["m" + k][iz, il] * (u * u)[:, None], axis=0) / wu * TCMB for k in KS}; T = est(c, u, w); NS = np.array([est(c, shuf(u, iz, rng), w) for _ in range(nsh)]); Cv = np.cov(NS[:200].T); Ci = 190 / 199 * np.linalg.inv(Cv); ex = NS[200:]
    o = {"N": int(sel.sum()), "That": T.tolist(), "err": np.sqrt(np.diag(Cv)).tolist(), "null_chi2": float(T @ Ci @ T), "p_null": float((np.einsum("ij,jk,ik->i", ex, Ci, ex) >= T @ Ci @ T).mean()), "S": {}}
    Cc[label] = (c, u, w); print(f"--- {label}: N {sel.sum()}; That {np.round(T, 1)}; null chi2 {o['null_chi2']:.1f}/8 p {o['p_null']:.3f}", flush=True)
    for n, R in Rs.items():
        for k in KS:
            m = mod[k] * R; f = np.einsum("i,ij", m, Ci) / np.einsum("i,ij,j", m, Ci, m); A = float(f @ T); s = float((ex @ f).std()); o[f"A_{k}_{n}"] = dict(A=A, s=s, p=float((ex @ f >= A).mean()), f=f.tolist())
        d = (mod["1.8"] - mod["1.0"]) * R; o["S"][n] = dict(S18=float(np.sqrt((mod["1.8"] * R) @ Ci @ (mod["1.8"] * R))), S18m1=float(np.sqrt(d @ Ci @ d)))
        print(f"  R {n} {R:.3f}: " + "; ".join(f"A({k}) {o[f'A_{k}_{n}']['A']:+.2f}+-{o[f'A_{k}_{n}']['s']:.2f} (p {o[f'A_{k}_{n}']['p']:.3f}, null mean {float((ex @ np.array(o[f'A_{k}_{n}']['f'])).mean()):+.3f})" for k in KS) + f"; S(1.8) {o['S'][n]['S18']:.1f} S(1.8-1) {o['S'][n]['S18m1']:.1f}", flush=True)
    return o, mod, Ci, w, T
Cc = {}
allg = np.ones(g.sum(), bool); O, mod, Ci, w, T = run(allg, "ALL"); RES["ALL"] = O
# jackknife (reported; enters the BELOW class via the larger error)
c_all, u_all, w_all = Cc["ALL"]; parts = np.array_split(np.argsort(ra), 50); jk = {}
for n, R in Rs.items():
    f = np.array(O[f"A_1.8_{n}"]["f"]); js = []
    for p in parts:
        k = np.ones(len(ra), bool); k[p] = False; js.append(f @ est(c_all[k], u_all[k], w_all[k]))
    js = np.array(js); jk[n] = float(np.sqrt(49 / 50 * np.sum((js - js.mean()) ** 2)))
RES["jack_A18"] = jk; print("jackknife sigma A(1.8):", {k: round(v, 3) for k, v in jk.items()}, flush=True)
cls = {}
for n in Rs:
    a, s, p = O[f"A_1.8_{n}"]["A"], O[f"A_1.8_{n}"]["s"], O[f"A_1.8_{n}"]["p"]; e = max(s, jk[n]); cl = "GAS DETECTED" if a / s >= 3 and p < .003 else ("BELOW" if a + 2 * e < 1 else "INCONCLUSIVE"); a1, s1 = O[f"A_1.0_{n}"]["A"], O[f"A_1.0_{n}"]["s"]; cls[n] = cl + (" (below at every extent)" if cl == "BELOW" and a1 + 2 * s1 < 1 else "")
RES["class"] = cls; print("CLASS", cls, "R-LIMITED" if len(set(cls.values())) > 1 else "agrees across R", flush=True)
for lab, sel in (("passive", ss < -11), ("star-forming", ss >= -11), ("north RA 90-280", (ra > 90) & (ra < 280)), ("south", ~((ra > 90) & (ra < 280)))): RES[lab] = run(sel, lab, 1200)[0]
d = float(np.max(np.abs(est(c_all, -u_all, w_all) + T))); check("MUTATE_flip", d < 1e-9, f"{d:.1e}"); ns = est(c_all, shuf(u_all, iz0, np.random.default_rng(929)), w_all); from scipy.stats import chi2; pn = float(chi2.sf(ns @ Ci @ ns, 8)); check("MUTATE_shuffle", pn > .01, f"p {pn:.3f}")
json.dump(RES, open(os.path.join(HERE, "gh8_mw.json"), "w"), indent=1, sort_keys=True)
