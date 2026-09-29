#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG49 referee -- the m2 -> infinity minimal gradient stiffness per galaxy layer, re-derived with the referee's own discretisation and
eigensolver, against DE13's COMMITTED form-(i) values (DE13_gate_gradient_repair_results.json, F1 rows mu_U) -- not against CFG49's code.

Inputs: DE12's layers through CFG49's loader (cv6_common.layer_fine / layer_coeffs: r, t, the gas modulus a = c_s^2/(rho h^2), B W''),
exec'd read-only.  The operator is the referee's own derivation (Schur complement of the gas, m2 -> infinity):
     E2 = 1/2 int r^2 [ mu dchi'^2 + (a - B W'') dchi^2 ] dr,
and a layer is stable at mu iff no Dirichlet window of DE13's five (t-width 0.5) carries a negative mode.  Numerics independent of CFG49:
the variable u = ln r on a uniform 3000-point grid per window (a, B W'' interpolated in u), E2 = 1/2 int [ mu r chi_u^2 + r^3 U chi^2 ] du,
and mu_crit(window) = the largest eigenvalue lambda of (-M_U) v = lambda K v (scipy.linalg.eigh on the dense pencil); mu_min = max over windows.
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.linalg import eigh

D49 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CFG49_gate_scalar")
sys.path.insert(0, D49)
with contextlib.redirect_stdout(io.StringIO()):
    import cv6_common as c
DE13 = json.load(open(os.path.join(os.path.dirname(D49), "..", "real_research", "dark_energy_2026", "DE13_gate_gradient_repair_results.json")))
rows = (DE13.get("numbers", DE13))["F1"]["rows"]
lines = []


def out(s=""):
    print(s); lines.append(s)


def mu_crit_window(r, U, N=3000):
    u0, u1 = math.log(r[0]), math.log(r[-1])
    u = np.linspace(u0, u1, N); h = u[1] - u[0]; rr = np.exp(u)
    Ui = np.interp(u, np.log(r), U)
    rm = np.exp(0.5 * (u[1:] + u[:-1]))
    # stiffness K (Dirichlet: interior nodes 1..N-2), potential M_U (lumped)
    kd = (rm[:-1] + rm[1:]) / h; ko = -rm[1:-1] / h
    K = np.diag(kd) + np.diag(ko, 1) + np.diag(ko, -1)
    MU = np.diag((rr ** 3 * Ui)[1:-1] * h)
    if np.all(Ui >= 0):
        return 0.0
    lam = eigh(-MU, K, eigvals_only=True, subset_by_index=[N - 3, N - 3])[0]
    return max(0.0, float(lam))


res = []
for key in rows:
    z, Mb, foot = key.split("/"); z, Mb = float(z), float(Mb)
    trf = c.layer_fine(z, Mb, foot)
    if trf is None:
        continue
    co = c.layer_coeffs(trf)
    U = co["a"] - co["BW2"]
    mus = []
    for (t0, t1) in c.WINS:
        m = (co["t"] >= t0) & (co["t"] <= t1)
        if m.sum() < 5:
            continue
        idx = np.where(m)[0]
        r_, U_ = co["r"][idx], U[idx]
        order = np.argsort(r_)
        mus.append(mu_crit_window(r_[order], U_[order]))
    mine = max(mus) if mus else 0.0
    res.append((key, mine, rows[key]["mu_U"]))
    out(f"  {key:22s}: referee mu_min {mine:.4e}   DE13 mu_U {rows[key]['mu_U']:.4e}   ratio {mine / rows[key]['mu_U']:.4f}")
rat = np.array([m / d for _, m, d in res])
out(f"\n  {len(res)} layers: referee / DE13 committed mu_U: median {np.median(rat):.4f}, range {rat.min():.4f} - {rat.max():.4f}")
out(f"  largest mu_min (the uniform stiffness a single constant must reach at m2 = inf): referee {max(m for _, m, _ in res):.3e}, "
    f"DE13 {max(d for _, _, d in res):.3e} J/m")
open(__file__.replace(".py", ".out"), "w").write("\n".join(lines) + "\n")
