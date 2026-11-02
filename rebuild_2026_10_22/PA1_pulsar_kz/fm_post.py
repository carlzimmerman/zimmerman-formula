#!/usr/bin/env python3
"""PA1 A1 post-result, no label: binary N1 at the median cell, distance coherent +-DIST_ERR, outliers out, Sun z 20 pc, round rule with r. Also N needed scaled from the real K_est error. python3 -I fm_post.py. kappa = 1/2 FITTED; not theory closed."""
import sys, os, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import fm_lib as FL
UX5 = os.path.join(H, "..", "UX5_mw_stellar_mass"); sys.path.insert(0, UX5)
from ux5_core import *
from scipy.optimize import minimize_scalar
OUT = {}; O = []
def gl(y, m, X, e):
    def f(ls):
        v = e ** 2 + math.exp(2 * ls); w = 1 / np.sqrt(v); c = np.linalg.lstsq(X * w[:, None], (y - m) * w, rcond=None)[0]; r = y - m - X @ c; return 0.5 * np.sum(r ** 2 / v + np.log(v))
    q = min((f(a), a) for a in np.linspace(-5, 3, 17))[1]; return -minimize_scalar(f, bounds=(q - .5, q + .5), method="bounded", options=dict(xatol=1e-5)).fun
for foot in ("canonical", "alt"):
    a0 = A0[foot]; MM = a0 / (1e-3 / (365.25 * 86400)); rows = [r for r in (json.loads(l) for l in open(os.path.join(UX5, "cache", f"{foot}_1.0.jsonl"))) if r["inp"] and r["A"]["L1"] and r["R"]["L1"]]; rows.sort(key=lambda r: (r["box"], r["sb"], r["mbb"], r["rd"], r.get("ht", 0), r.get("hk", 0), r.get("fk", 0)))
    c = rows[len(rows) // 2]; rhof, _ = rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); g, Mu = grid(a0); LU = Lapl(g); rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); PhiN = LU.newton(rho1)
    pr = PS.Problem(g, rho1, 2 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.0); Phi, _, _ = pr.solve_aqual()
    def fld(P_):
        dr, dt = g.grad_cells(P_); return np.sin(g.t2d) * dr + np.cos(g.t2d) * dt, np.cos(g.t2d) * dr - np.sin(g.t2d) * dt
    dRA, dzA = fld(Phi); dRN, dzN = fld(PhiN); s = FL.load("binary")
    def dl(ds=0.0, zs=0.0, drop=(), rr=False):
        k = np.array([n not in drop for n in s["name"]]); d = s["d"] + ds * np.nan_to_num(s["derr"]); R, z, n, x, y = FL.geom(s["l"], s["b"], d, zs); R, z, n, x, y = R[k], z[k], n[k], x[k], y[k]; yy, ee = s["y"][k], s["e"][k]
        RR = np.r_[R, R0]; ZZ = np.r_[z, zs]; AZ = np.abs(ZZ); SG = np.sign(ZZ)
        aRA = -g.interp_cells(dRA, RR, AZ) * MM; azA = -g.interp_cells(dzA, RR, AZ) * SG * MM; aRN = -g.interp_cells(dRN, RR, AZ) * MM; azN = -g.interp_cells(dzN, RR, AZ) * SG * MM
        yb = g.interp_cells(dRN, RR, np.zeros_like(RR)); gc = (0.5 + np.sqrt(0.25 + 1 / np.maximum(yb, 1e-30)) - 1) * yb * MM
        if rr: r_ = np.hypot(RR, ZZ); aRR = aRN - gc * RR / r_; azR = azN - gc * ZZ / r_
        else: aRR = aRN - gc; azR = azN - gc * ZZ / RR
        X = np.c_[n[:, 0], n[:, 1], n[:, 2], np.abs(z) * n[:, 2]]; N = len(x)
        ma = FL.alos(aRA[:N], azA[:N], aRA[-1], azA[-1], x, y, n); mr = FL.alos(aRR[:N], azR[:N], aRR[-1], azR[-1], x, y, n); return 2 * (gl(yy, ma, X, ee) - gl(yy, mr, X, ee)), N
    for tag, kw in (("base", {}), ("d +1 err", dict(ds=1)), ("d -1 err", dict(ds=-1)), ("outliers out", dict(drop=("J0125-2327", "J1400-1431"))), ("Sun z 20 pc", dict(zs=0.02)), ("round rule with r", dict(rr=True))):
        v, N = dl(**kw); OUT[f"{foot} {tag}"] = v; O.append(f"[{foot}] {tag}: dL A-R {v:+.2f}, n {N}")
res = json.load(open(os.path.join(H, "fm_read.json")))
for foot in ("canonical", "alt"):
    e = res[foot]["binary_N1"]["K"]["A"]["err"]; n = res[foot]["binary_N1"]["n"]; g = res[foot]["binary_N1"]; f = {"canonical": (14.55, 5.12), "alt": (16.39, 5.42)}[foot]
    for nm, gp in (("A vs R min gap", f[0]), ("A floor vs line top", f[1])):
        O.append(f"[{foot}] K_est err {e:.1f} at n {n}; {nm} {gp}: sigma K {gp / 3:.2f}, N scaled 1/sqrt(N), same errors {n * (e / (gp / 3)) ** 2:.0f}")
print("\n".join(O)); open(os.path.join(H, "fm_post.out"), "w").write("\n".join(O) + "\n")
