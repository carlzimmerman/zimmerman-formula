#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG48 referee -- G6's Volterra stability counts re-derived with the referee's own discretisation and eigen-solver.  The PHYSICAL inputs (DE12's
layers: r, rho_b, B, W'', the gate normalisation U_0/M_0 and the reading A) come from G6's own layer_arrays(), exec'd read-only from the committed
file (so this checks CFG48's numerics, not DE12's physics).  What is independent: the grid (uniform in ln r, 4000 points, p and V interpolated in
ln r) and the linear algebra (scipy's sparse generalized eigensolver for eta_crit = 1 / mu_max of V m = mu K m, K the pressure stiffness; a
negative mode exists iff eta_crit < 1), in place of G6's LDL^T pivot counting and bisection on its own nonuniform grid.
Also checked on G6's committed JSON: a case has a negative mode on some window exactly when its full-layer eta_crit < 1 (Dirichlet domain
monotonicity), for both readings.
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

D48 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CFG48_gap1_switch")
sys.path.insert(0, D48)
os.environ["MUTATE"] = "0"
src = open(os.path.join(D48, "G6_nonlocal_gate_stiffness.py")).read()
g6 = {"__file__": os.path.join(D48, "G6_nonlocal_gate_stiffness.py"), "__name__": "g6_ref"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("def volterra(La):")], "G6", "exec"), g6)
layer_arrays = g6["layer_arrays"]
com = json.load(open(os.path.join(D48, "G6_nonlocal_gate_stiffness_results.json")))["numbers"]["cases"]
lines = []


def out(s=""):
    print(s); lines.append(s)


def eta_mine(La, N=4000):
    t = La["t"]; sel = np.where((t > 0.004) & (t < 0.996))[0]
    lr = np.log(La["r"][sel]); p = La["p"][sel]; V = La["V"][sel]
    u = np.linspace(lr[0], lr[-1], N); h = u[1] - u[0]; r = np.exp(u)
    pr = np.interp(u, lr, p); Vr = np.interp(u, lr, V)
    # E2 = 1/2 int [p m_r^2 - V m^2] dr with dr = r du, m_r = m_u / r:  1/2 int [(p/r) m_u^2 - V r m^2] du   (Dirichlet ends)
    q = pr / r; qm = 0.5 * (q[1:] + q[:-1])
    K = diags([(qm[:-1] + qm[1:]) / h, -qm[1:-1] / h, -qm[1:-1] / h], [0, 1, -1], format="csc")
    Vw = diags(Vr[1:-1] * r[1:-1] * h, 0, format="csc")
    if float(np.max(Vr)) <= 0:
        return math.inf
    mu = eigsh(Vw, k=1, M=K, which="LA", return_eigenvectors=False, tol=1e-10, maxiter=20000)[0]
    return 1.0 / mu if mu > 0 else math.inf


rows = []
for key, v in com.items():
    wtag, z, Mb, foot = key.split("/")
    w, z, Mb = float(wtag[1:]), float(z), float(Mb)
    for reading in ("1", "dyn"):
        La = layer_arrays(z, Mb, foot, w, "dyn" if reading == "dyn" else "1")
        em = eta_mine(La)
        ec = v[reading]["eta_crit"]; ec = math.inf if isinstance(ec, str) else ec
        rows.append((key, reading, em, ec, v[reading]["has_negative"], max(v[reading]["neg_modes"].values())))
agree = sum((r_[2] < 1) == r_[4] for r_ in rows)
mono = sum(((r_[3] < 1) == r_[4]) for r_ in rows)
rel = [abs(r_[2] / r_[3] - 1) for r_ in rows if math.isfinite(r_[2]) and math.isfinite(r_[3])]
n1 = sum(r_[2] < 1 for r_ in rows if r_[1] == "1"); nd = sum(r_[2] < 1 for r_ in rows if r_[1] == "dyn")
out("CFG48 G6 referee: Volterra gate, referee's grid (uniform ln r, 4000 pts) and generalized eigensolver")
out(f"  cases x readings: {len(rows)}")
out(f"  negative mode (eta_crit < 1), referee: baryon-mass reading {n1}/48, dynamical-mass reading {nd}/48   (CFG48: 0/48 and 29/48)")
out(f"  referee's verdict agrees with CFG48's has_negative on {agree}/{len(rows)}")
out(f"  CFG48's own JSON: has_negative <=> full-layer eta_crit < 1 on {mono}/{len(rows)} (Dirichlet domain monotonicity)")
out(f"  eta_crit, referee vs CFG48: median |ratio - 1| {np.median(rel):.2e}, max {np.max(rel):.2e}")
out(f"  baryon-mass reading: referee min eta_crit {min(r_[2] for r_ in rows if r_[1] == '1'):.2f} (CFG48 {min(r_[3] for r_ in rows if r_[1] == '1'):.2f})")
for r_ in sorted(rows, key=lambda x: abs(x[2] / x[3] - 1) if math.isfinite(x[2]) and math.isfinite(x[3]) else 0)[-3:]:
    out(f"    largest eta difference: {r_[0]} [{r_[1]}]: referee {r_[2]:.3g}, CFG48 {r_[3]:.3g}")
open(__file__.replace(".py", ".out"), "w").write("\n".join(lines) + "\n")
