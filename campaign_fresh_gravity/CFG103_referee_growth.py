#!/usr/bin/env python3
"""CFG103 referee: the quantitative core of the capped-fluid obstruction (CFG43, re-derived by CFG103), re-derived with the referee's own
linear-growth solver.  Spec = CFG103's FROZEN_DOCSTRING.txt A3(b) (Planck18 background, pressureless baryons + the capped fluid with
c_s^2 = n P_n / (rho + P), P = Pcap x^2/(1+x^2), Pcap = eps rho_L, eps = kappa^2/8pi, x = rho_c(z)/(nu* rho_L); start z = 1e4 with delta = a;
total-matter growth at z = 0 against LCDM; nu_min(k; d) = the smallest nu* with ratio >= 1 - d for all larger nu*) and its engagement
g0 = nu_M / (x_F nu_min) at the frozen primary (M_h = M_b/f_b, k = pi/R, F = 1/2).  Nothing from CFG43 or CFG103 is imported.
Run: python3 campaign_fresh_gravity/CFG103_referee_growth.py
"""
import math, numpy as np, time
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
OM, OB, OL = 0.315, 0.0493, 0.685
OC = OM - OB; FBAR = OB / OM
EPS = 0.25 / (8 * math.pi)
CH0 = 299792.458 / 67.4                                   # c / H0 in Mpc
def cs2(a, nus):                                          # in units of c^2
    x = (OC / OL) * a ** -3 / nus
    return 2 * EPS * x / ((1 + x * x) ** 2 * (nus + EPS * math.atan(x) + EPS * x / (1 + x * x)))
def rhs(la, y, k, nus):
    a = math.exp(la); E2 = OM * a ** -3 + OL
    dlnH = -1.5 * OM * a ** -3 / E2
    om = OM * a ** -3 / E2
    db, dbp, dc, dcp = y
    src = 1.5 * om * (FBAR * db + (1 - FBAR) * dc)
    pres = 0.0 if nus is None else cs2(a, nus) * (k * CH0) ** 2 / (a * a * E2)
    return [dbp, src - (2 + dlnH) * dbp, dcp, src - (2 + dlnH) * dcp - pres * dc]
def growth(k, nus, zi=1e4):
    ai = 1 / (1 + zi)
    s = solve_ivp(rhs, (math.log(ai), 0.0), [ai, ai, ai, ai], args=(k, nus), method="DOP853" if nus is None else "LSODA", rtol=1e-10, atol=1e-14)
    db, _, dc, _ = s.y[:, -1]
    return FBAR * db + (1 - FBAR) * dc
D0 = {}
def ratio(k, nus):
    if k not in D0: D0[k] = growth(k, None)
    return growth(k, nus) / D0[k]
t0 = time.time()
print("nu*=1 growth ratio at k = 0.5, 2, 10, 30 /Mpc:", [round(ratio(k, 1.0), 4) for k in (0.5, 2, 10, 30)], "  [CFG103 0.139 0.092 0.084 0.070; CFG43 0.140 0.099 0.080]", f"({time.time()-t0:.0f}s)")
print("c_s^2(z=0, nu*=1) =", round(cs2(1.0, 1.0), 6), " [CFG43 5.78e-3]")
res = []
for k in (0.5, 2.0, 10.0, 30.0):
    f = lambda lnu: ratio(k, 10 ** lnu) - 0.95
    grid = np.arange(2.0, 9.51, 0.25); vals = [f(g) for g in grid]
    idx = [i for i in range(len(grid)) if vals[i] < 0]
    i = max(idx)                                       # last grid point still below 0.95 -> smallest nu* above which ratio >= 0.95 for all larger
    root = brentq(f, grid[i], grid[i + 1], xtol=1e-6)
    res.append(10 ** root)
    print(f"k = {k:5.1f}/Mpc: nu_min(5%) = {10**root:.3e}   ({time.time()-t0:.0f}s)")
lk, ln = np.log10([0.5, 2, 10, 30]), np.log10(res)
print("exponent (fit):", round(float(np.polyfit(lk, ln, 1)[0]), 3), " local slopes:", [round(float(s), 3) for s in np.diff(ln) / np.diff(lk)], " [CFG103 2.17e4 1.74e5 1.95e6 1.01e7; exponent 1.501]")
# g0 at the frozen primary: M_h = M_b / f_b, k = pi / R (R the comoving Lagrangian radius of M_h), d = 5% and 20%, F = 1/2 (x_F = 1)
G, C, MSUN, MPC = 6.674e-11, 2.99792458e8, 1.989e30, 3.0857e22
H0 = 67.4e3 / MPC
RHOC = 3 * H0 ** 2 / (8 * math.pi * G); RHOL = OL * RHOC
A0 = 0.5 * C * math.sqrt(G * RHOL)
print(f"a0 = {A0:.5e} m/s^2 (Omega_L {OL})")
def numin(k, d):
    f = lambda lnu: ratio(k, 10 ** lnu) - (1 - d)
    grid = np.arange(0.0, 9.51, 0.25); vals = [f(g) for g in grid]
    i = max(j for j in range(len(grid)) if vals[j] < 0)
    return 10 ** brentq(f, grid[i], grid[i + 1], xtol=1e-7)
for Mb in (1e9, 3e11):
    rM = math.sqrt(G * Mb * MSUN / A0)
    nuM = A0 / (4 * math.pi * G * rM * math.sqrt(2)) / RHOL
    Mh = Mb / FBAR
    R = (3 * Mh * MSUN / (4 * math.pi * OM * RHOC)) ** (1 / 3) / MPC
    k = math.pi / R
    out = []
    for d in (0.05, 0.20):
        out.append(nuM / numin(k, d))
    print(f"M_b {Mb:.0e}: nu_M {nuM:.4e}, k = pi/R = {k:.3f}/Mpc, g0(5%) {out[0]:.3f}, g0(20%) {out[1]:.3f}   [CFG103: nu_M(1e9) 3.587e5, (3e11) 2.071e4; g0 0.205 / 0.606]")
