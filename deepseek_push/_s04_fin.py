#!/usr/bin/env python3
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
spec = importlib.util.spec_from_file_location("_s04_proto", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s04_proto.py"))

def fit_grad(X, Y, v, w):
    A = np.column_stack([np.ones_like(X), X, Y]); W = np.sqrt(w)
    c, *_ = np.linalg.lstsq(A*W[:, None], v*W, rcond=None)
    return c

# reload data fresh (same as proto)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s04_proto.py")).read().split("# --- per-cluster gradient fit prototype ---")[0])

shell = (d["R"] >= 0.2) & (d["R"] < 1.5)
clusters = np.unique(d["cl"])
rng = np.random.default_rng(42)
amps, errs, nulls, angles, gs = [], [], [], [], []
for k in clusters:
    m = (d["cl"] == k) & shell
    n = int(m.sum())
    if n < 10:
        continue
    X, Y, v, e = d["X"][m], d["Y"][m], d["V"][m], d["e"][m]
    w = np.where(e > 0, 1.0/e**2, 1.0)
    c = fit_grad(X, Y, v, w); a, b = c[1], c[2]
    amps.append(math.hypot(a, b)); angles.append(math.atan2(b, a)); gs.append((a, b))
    bs = []
    for _ in range(150):
        idx = rng.integers(0, n, n)
        c2 = fit_grad(X[idx], Y[idx], v[idx], w[idx]); bs.append((c2[1], c2[2]))
    bs = np.array(bs); cov = np.cov(bs[:, 0], bs[:, 1])
    J = np.array([a/math.hypot(a, b), b/math.hypot(a, b)]) if a*a + b*b > 0 else np.array([1.0, 1.0])
    errs.append(math.sqrt(J @ cov @ J))
    nv = []
    for _ in range(100):
        vs = rng.permutation(v)
        c3 = fit_grad(X, Y, vs, w); nv.append(math.hypot(c3[1], c3[2]))
    nulls.append(np.mean(nv))
amps = np.array(amps); errs = np.array(errs); nulls = np.array(nulls); angles = np.array(angles)
gs = np.array(gs)
ncl = len(amps)
print("n clusters:", ncl)
print("mean A:", round(amps.mean(), 1), "null:", round(nulls.mean(), 1), "excess:", round((amps-nulls).mean(), 1),
      "+-", round((amps-nulls).std(ddof=1)/math.sqrt(ncl), 1))
print("median excess:", round(np.median(amps-nulls), 1))
gm = gs.mean(axis=0)
se = gs.std(axis=0, ddof=1)/math.sqrt(ncl)
print("coherent vector mean (a,b):", np.round(gm, 1), "se:", np.round(se, 1))
print("coherent amplitude:", round(math.hypot(*gm), 1), " z:", round(math.hypot(*gm)/(se.mean()), 2))
nnv = []
for _ in range(50):
    sh = []
    for k in clusters:
        m = (d["cl"] == k) & shell
        if int(m.sum()) < 10:
            continue
        X, Y, v, e = d["X"][m], d["Y"][m], d["V"][m], d["e"][m]
        w = np.where(e > 0, 1.0/e**2, 1.0)
        c3 = fit_grad(X, Y, rng.permutation(v), w); sh.append((c3[1], c3[2]))
    nnv.append(np.mean(np.array(sh), axis=0))
nnv = np.array(nnv)
print("null vector-mean amplitude:", round(np.hypot(nnv[:, 0], nnv[:, 1]).mean(), 1))
Rbar = np.hypot(np.cos(angles).mean(), np.sin(angles).mean())
z_ray = Rbar*math.sqrt(2*ncl)
print("Rayleigh Rbar:", round(Rbar, 4), " z:", round(z_ray, 2))
print("n clusters A>3err:", int((amps > 3*errs).sum()), "of", ncl)
print("median per-cluster err(A):", round(np.median(errs), 1))
ul = (amps-nulls).mean() + 2*((amps-nulls).std(ddof=1)/math.sqrt(ncl))
print("2-sigma UL on gradient excess:", round(ul, 1), "-> v_rot,los UL:", round(ul*math.sqrt(0.2*1.5), 1), "km/s")
print("mean radius shell (R500):", round(d["R"][shell].mean(), 3))