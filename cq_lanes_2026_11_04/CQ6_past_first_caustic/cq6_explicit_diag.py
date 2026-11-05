#!/usr/bin/env python3
"""CQ6 POST-RESULT diagnostic, no label weight: adaptive explicit velocity Verlet on cq6.py's discrete Lagrangian
(dt = min(1e-3, C*2/omega_max), omega_max from the regulator's local dispersion sqrt(12 lam)|dlnrho/dx|(pi/Delta)^2).
Asks whether the frozen integrator's blow-up at the first bounce is the integrator's or the discrete system's, and
how grid-scale gradients and accelerations scale with N. kappa = 1/2 FITTED; not theory closed. a0 does not enter.
usage: python3 cq6_explicit_diag.py N lam t_end C
"""
import os, sys, time, json, warnings
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cq6
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
N, lam, tend, C = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
M = cq6.Model(N, lam); m = M.m
x = M.q - cq6.A * np.sin(2 * np.pi * M.q); v = np.zeros(N)


def omega(x):
    F, G, f, D, psi = cq6.reg(x, lam, m)
    s = 0.5 * (D + np.roll(D, -1)); dl = 4 * np.abs(np.roll(psi, -1) - psi) / (s * 0.5 * (psi + np.roll(psi, -1)))
    return np.max(np.sqrt(12 * lam) * np.maximum(dl, np.roll(dl, 1)) * (np.pi / D) ** 2)


a = M.acc(x); t, n, nxt, Kmax, t0 = 0.0, 0, 2.9, 1e-300, time.time()
E0 = M.diag_row(0, x, v)[4]; rows = []; status = "reached_t_end"
while t < tend - 1e-12:
    dt = min(1e-3, C * 2.0 / omega(x), tend - t)
    v += 0.5 * dt * a; x += dt * v
    if np.min(cq6.cells(x)) <= 0 or not np.all(np.isfinite(x)):
        status = f"CROSS/BLOW at t={t:.5f}"; break
    a = M.acc(x); v += 0.5 * dt * a; t += dt; n += 1
    if t >= nxt - 1e-12:
        r = M.diag_row(t, x, v); Kmax = max(Kmax, r[1])
        row = {"t": round(t, 3), "steps": n, "dt": dt, "dE_over_Kmax": (r[4] - E0) / Kmax, "rho_c": r[7],
               "min_D": r[12], "max_dlnrho": r[13], "max_abs_acc": float(np.max(np.abs(a))), "Rv": r[6]}
        rows.append(row); print(json.dumps(row), flush=True); nxt += 0.1
print(json.dumps({"N": N, "lambda": lam, "C": C, "status": status, "t_reached": t, "steps": n,
                  "wall_s": round(time.time() - t0, 1), "note": cq6.NOTE}), flush=True)
