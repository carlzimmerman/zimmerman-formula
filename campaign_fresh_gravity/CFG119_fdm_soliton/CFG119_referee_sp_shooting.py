#!/usr/bin/env python3
"""CFG119 referee check (written by the reviewing chat, independently of CFG119_fdm_soliton.py; it reads no CFG119 code).

The no-baryon Schrodinger-Poisson ground state by plain shooting, in units G = hbar = m = 1:
    psi'' = -(2/r) psi' + 2 (Phi - E) psi,   Phi'' = -(2/r) Phi' + 4 pi psi^2,   psi(0) = 1, psi'(0) = Phi(0) = Phi'(0) = 0,
with E bisected on the node / turn-up criterion.  It reports the scale-free numbers CFG119's C1 and C1x quote:
E M^-2 (E measured from Phi(inf) = 0), r_c M (r_c = the half-peak-density radius), f_c = M(<r_c)/M, the profile against
Schive et al. 2014's fit (1 + 0.091 (r/r_c)^2)^-8, and Schive's amplitude (1.9 Msun pc^-3 kpc^4 at m = 1e-23 eV, a = 1).
MUTATE=1 perturbs the Poisson source by 5% (4 pi -> 4.2 pi): the scale-free numbers must move, so the check can fail.
"""
import os
import numpy as np
from scipy.integrate import solve_ivp

FOURPI = 4 * np.pi * (1.05 if os.environ.get("MUTATE", "0") == "1" else 1.0)


def rhs(r, y, E):
    psi, dpsi, phi, dphi = y
    return [dpsi, -2 / r * dpsi + 2 * (phi - E) * psi, dphi, -2 / r * dphi + FOURPI * psi ** 2]


def shoot(E, R=12.0):
    r0 = 1e-6
    y0 = [1 - E * r0 ** 2 / 3, -2 * E * r0 / 3, FOURPI * r0 ** 2 / 6, FOURPI * r0 / 3]
    node = lambda r, y, E: y[0]
    node.terminal, node.direction = True, -1
    up = lambda r, y, E: y[1]
    up.terminal, up.direction = True, 1
    s = solve_ivp(rhs, (r0, R), y0, args=(E,), events=[node, up], rtol=1e-12, atol=1e-14, dense_output=True)
    return (+1 if s.t_events[0].size else -1), s


lo, hi = 0.0, 3.0
assert shoot(lo)[0] == -1 and shoot(hi)[0] == +1
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if shoot(mid)[0] > 0:
        hi = mid
    else:
        lo = mid
E = 0.5 * (lo + hi)
_, s = shoot(lo)
r = np.linspace(1e-6, s.t[-1], 200001)
y = s.sol(r)
i = int(np.argmin(np.abs(y[0])))
r, psi, phi = r[:i], y[0][:i], y[2][:i]
dM = 4 * np.pi * r ** 2 * psi ** 2
M = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(r))])
Mtot = M[-1]
E_true = E - (phi[-1] + (FOURPI / (4 * np.pi)) * Mtot / r[-1])
rho = psi ** 2
rc = float(np.interp(0.5, rho[::-1], r[::-1]))
fc = float(np.interp(rc, r, M)) / Mtot
hbar, G, eV, c = 1.054571817e-34, 6.67430e-11, 1.602176634e-19, 2.99792458e8
Msun, pc = 1.98892e30, 3.0856775814913673e16
kpc = 1e3 * pc
m = 1e-23 * eV / c ** 2
amp = rho[0] * rc ** 4 * hbar ** 2 / (G * m ** 2) / (Msun / pc ** 3 * kpc ** 4)

print("CFG119 referee: the no-baryon SP ground state by shooting (independent of CFG119_fdm_soliton.py)"
      + ("   [MUTATE: Poisson source x 1.05]" if FOURPI != 4 * np.pi else ""))
print(f"  E M^-2 = {E_true / Mtot ** 2:.6f}   (CFG119 C1x: -0.1627692)")
print(f"  r_c M  = {rc * Mtot:.5f}    (CFG119: 2.67940)")
print(f"  f_c    = {fc:.5f}     (CFG119: 0.23635)")
print(f"  Schive amplitude at m = 1e-23 eV, a = 1: {amp:.4f} Msun pc^-3 kpc^4   (Schive 1.9; CFG119 1.938)")
worst = 0.0
for x in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    sp, fit = float(np.interp(x * rc, r, rho)), (1 + 0.091 * x ** 2) ** -8
    worst = max(worst, abs(sp / fit - 1))
    print(f"  r/r_c {x:3.1f}: rho/rho0 {sp:.5f}   fit {fit:.5f}   SP/fit - 1 {100 * (sp / fit - 1):+.2f}%")
ok = (abs(E_true / Mtot ** 2 + 0.1627692) < 1e-5 and abs(rc * Mtot - 2.67940) < 1e-4 and abs(fc - 0.23635) < 1e-4
      and abs(amp - 1.938) < 0.002)
print(f"  REFEREE CHECK (CFG119's C1/C1x numbers reproduced): {'PASS' if ok else 'FAIL'}; worst |SP/fit - 1| on the table {100 * worst:.1f}%")
raise SystemExit(0 if ok else 1)
