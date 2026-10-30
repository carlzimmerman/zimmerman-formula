#!/usr/bin/env python3
"""GH7 measurement: T-hat(theta), velocity-shuffle covariance, A(k), checks and splits."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data"); W = os.path.join(EXT, "gh7_work")
C_ = np.load(os.path.join(W, "gh7_cap.npz")); V = np.load(os.path.join(W, "gh7_vel.npz"))["v"]; L_ = np.load(os.path.join(W, "gh7_lenses.npz")); J = json.load(open(os.path.join(HERE, "gh7_vel.json")))
RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
g = C_["good"]; cap0 = C_["cap"][g].astype(np.float64); iz0, il0 = C_["iz"][g], C_["il"][g]; v0 = V[g].astype(np.float64) / 299792.458; TCMB = 2.72548e6
ra, sfr, lm = L_["ra"][g], L_["sfr"][g], L_["lm"][g]; RF = J["R"]; RC = .64 * 300 / (v0.std() * 299792.458); KS = ("1.0", "1.8", "3.0"); rng = np.random.default_rng(707)
print(f"N {g.sum()}, R frozen {RF:.3f}, R context {RC:.3f}", flush=True)
def that(c, v): return -np.sum(c * v[:, None], axis=0) / np.sum(v * v)
def shuffled(v, iz, r):
    o = v.copy()
    for i in range(10):
        q = np.where(iz == i)[0]; o[q] = v[r.permutation(q)]
    return o
def run(sel, label, nsh=2200, extra=None):
    cap, v, iz, il = cap0[sel].copy(), v0[sel], iz0[sel], il0[sel]
    for i in range(10): cap[iz == i] -= cap[iz == i].mean(axis=0)
    if extra is not None: cap += extra[sel]
    w = np.array([[np.sum(v[(iz == i) & (il == j)] ** 2) for j in range(4)] for i in range(10)]) / np.sum(v * v); mod = {k: np.einsum("ij,ijk", w, C_["m" + k]) * TCMB for k in KS}
    T = that(cap, v); NS = np.array([that(cap, shuffled(v, iz, rng)) for _ in range(nsh)]); Cv = np.cov(NS[:200].T); h = (200 - 8 - 2) / 199; Ci = h * np.linalg.inv(Cv)
    out = {"N": int(sel.sum()), "That": T.tolist(), "err": np.sqrt(np.diag(Cv)).tolist(), "null_chi2": float(T @ Ci @ T)}; ex = NS[200:]; out["p_null_shuffle"] = float((np.einsum("ij,jk,ik->i", ex, Ci, ex) >= out["null_chi2"]).mean())
    for Rn, R in (("frozen", RF), ("context", RC)):
        for k in KS:
            m = mod[k] * R; fac = m @ Ci / (m @ Ci @ m); A = float(fac @ T); sA = float((ex @ fac).std()); pA = float((ex @ fac >= A).mean()); chi = float((T - A * m) @ Ci @ (T - A * m)); chi1 = float((T - m) @ Ci @ (T - m))
            out[f"A_{k}_{Rn}"] = dict(A=A, s=sA, p=pA, chi2_free=chi, chi2_A1=chi1)
    print(f"--- {label}: N {sel.sum()}; null chi2 {out['null_chi2']:.1f}/8 shuffle p {out['p_null_shuffle']:.3f}", flush=True)
    if label == "ALL": print("That uK", np.round(T, 4), "\nerr", np.round(out["err"], 4), flush=True)
    for Rn in ("frozen", "context"): print(f"  R {Rn}: " + "; ".join(f"A({k}) {out[f'A_{k}_{Rn}']['A']:+.2f}+-{out[f'A_{k}_{Rn}']['s']:.2f} (p {out[f'A_{k}_{Rn}']['p']:.3f}, chi2@1 {out[f'A_{k}_{Rn}']['chi2_A1']:.1f})" for k in KS), flush=True)
    return out, T, Ci, mod
allg = np.ones(g.sum(), bool); O, T0, Ci0, mod0 = run(allg, "ALL"); RES["ALL"] = O
# jackknife on A(1.8), reported only
o = np.argsort(ra); parts = np.array_split(o, 50); cz = cap0.copy()
for i in range(10): cz[iz0 == i] -= cz[iz0 == i].mean(axis=0)
for Rn, R in (("frozen", RF), ("context", RC)):
    m = mod0["1.8"] * R; fac = m @ Ci0 / (m @ Ci0 @ m); js = []
    for p in parts:
        k = np.ones(len(ra), bool); k[p] = False; js.append(fac @ that(cz[k], v0[k]))
    js = np.array(js); RES[f"jack_A18_{Rn}"] = float(np.sqrt(49 / 50 * np.sum((js - js.mean()) ** 2))); print(f"jackknife sigma A(1.8), R {Rn}: {RES[f'jack_A18_{Rn}']:.2f}", flush=True)
# splits
ss = sfr - lm
for lab, sel in (("passive", ss < -11), ("star-forming", ss >= -11), ("north RA 90-280", (ra > 90) & (ra < 280)), ("south", ~((ra > 90) & (ra < 280)))): RES[lab] = run(sel, lab, nsh=1200)[0]
# K5: inject A = 1 (frozen R) per lens from the cell model; recovery of the increment
mc = C_["m1.8"][iz0, il0] * TCMB * RF; inj = -mc * v0[:, None]; TI = that(cz + inj, v0); m = mod0["1.8"] * RF; fac = m @ Ci0 / (m @ Ci0 @ m); dA = float(fac @ (TI - T0)); check("K5_injection_recovery", abs(dA - 1) < .02, f"increment in A(1.8) {dA:.4f}")
# MUTATE
d = float(np.max(np.abs(that(cz, -v0) + T0))); check("MUTATE_sign_flip", d < 1e-9, f"max |T(-v)+T(v)| {d:.1e}")
r2 = np.random.default_rng(909); ns = that(cz, shuffled(v0, iz0, r2)); c2 = float(ns @ Ci0 @ ns); from scipy.stats import chi2; pn = float(chi2.sf(c2, 8)); check("MUTATE_shuffled_null", pn > .01, f"chi2 {c2:.1f}/8, p {pn:.3f}")
json.dump(RES, open(os.path.join(HERE, "gh7_results.json"), "w"), indent=1, sort_keys=True); print("done", flush=True)
