#!/usr/bin/env python3
"""Weak-field size of QX17's non-advective khronon flux lambda P/Q against the advective flux rho_Q n^r, in SI.
Scaling (derivation in README.md, item B): with lapse N ~ 1 + Phi/c^2 and clock-flow tilt n^r ~ v/c,
  lambda ~ (1/c^3) (dPhi/dt + v g)       [E2 normal part; the gamma_L Pi_+ part is ~1e-10 or smaller]
  P^r = M_N(<r)/(4 pi r^2),  N = dM_N/dr/(4 pi r^2)  ->  P/N = r / (dln M_N / dln r)
  ratio = lambda P / (N v / c) = (g r / c^2) / (dln M_N/dln r)  +  (dPhi/dt) r / (c^2 v dlnM)
The steady (v g) part is independent of v; it equals v_c^2/c^2 for an isothermal (M ~ r) cold profile.
  python3 -I -B reviews/codex_mass_budget_audit_2026_11_14/audit_b_weakfield.py
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import math
G = 6.67430e-11; MSUN = 1.98892e30; KPC = 3.0856775814913673e19; C = 2.99792458e8
r = 100 * KPC
print("Milky-Way-mass system at r = 100 kpc; ratio = (g r / c^2) / (dlnM/dlnr) for the steady part")
for label, M in (("M(<100 kpc) = 6e11 Msun", 6e11), ("M(<100 kpc) = 1e12 Msun", 1e12)):
    g = G * M * MSUN / r ** 2
    print(f"  {label}: g = {g:.3e} m/s^2, GM/(r c^2) = {g * r / C ** 2:.2e}; isothermal (dlnM = 1): ratio {g * r / C ** 2:.2e}")
for ft, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    Mb = 6e10 * MSUN
    vflat = (G * Mb * a0) ** 0.25
    print(f"  {ft}: deep-law flat speed for M_b = 6e10 Msun: {vflat / 1e3:.1f} km/s, v^2/c^2 = {(vflat / C) ** 2:.2e}")
# a time-dependent potential adds (dPhi/dt) r / (c^2 v): for dPhi/dt ~ Phi / t_H and v ~ 100 km/s
tH = 13.8e9 * 3.15576e7; v = 100e3; Phi = 200e3 ** 2
print(f"  time-dependent part with |Phi| = (200 km/s)^2, t = 13.8 Gyr, v = 100 km/s: {Phi / tH * r / (C ** 2 * v):.2e}")
# gamma_L term across a layer of width delta: gamma_L Pi ~ 2 pi G N Lstar^2 / c^2, times (r / delta)
N = 1e-5 * MSUN / KPC ** 3 * 1e9                      # 1e-5 Msun/pc^3 in kg/m^3
for Lstar_pc in (21.7, 22.9):
    gp = 2 * math.pi * G * N * (Lstar_pc * KPC / 1e3) ** 2 / C ** 2
    print(f"  gamma_L Pi_+ at N = 1e-5 Msun/pc^3, Lstar {Lstar_pc} pc: {gp:.1e}; with r/delta = 1e3: {gp * 1e3:.1e}")
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
