#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG120 POST-HOC diagnostics (written AFTER seeing the main runs; NOT frozen; none of this can upgrade or change a verdict).
Purpose: explain three numerical misses of pre-declared implementation lines in script D and locate two numbers, without touching those lines.
  P1  T3a.2 missed its 1e-4 line (2.0e-4): which d, and is it quadrature?  (tighter direct integration)
  P2  T3b missed its 1e-12 ABSOLUTE line (1.2e-11): the same quantity relative to its own scale.
  P3  T4.1's declared 1e-4 bound: where the Hubble-scale kernel's R peaks and its size relative to the 0.9 pass line.
  P4  T1f (script B) B.4 was false for finite-range kernels: leakage of the recalled RM kernel versus shell separation, to show it is a range effect.
Run: python3 cfg120_POSTHOC_diagnostics.py
"""
import os, sys, math
import numpy as np
from scipy.integrate import quad

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg120_common import *

R = Report("cfg120_POSTHOC_diagnostics")
P = R.P
R.head(__doc__.split("Run: python3")[0])
kern = RM(1.0, 3.0, 0.1)
a0 = A0

R.banner("P1  direct 3-D cloud-force integral, per distance, with two quadrature settings")


def fdirect(d, eps, smax=3e3):
    def inner(s):
        f = lambda mu: (d - s * mu) / (d * d + s * s - 2 * d * s * mu) ** 1.5
        return 2 * math.pi * quad(f, -1, 1, epsabs=0, epsrel=eps, limit=400)[0]
    fcl = lambda s: s * s * float(kern.K(s)) * inner(s)
    tot = 0.0
    for a, b in ((1e-9, 0.5 * d), (0.5 * d, d), (d, 2 * d), (2 * d, 20 * d + 50.0), (20 * d + 50.0, smax)):
        tot += quad(fcl, a, b, epsabs=0, epsrel=eps, limit=800)[0]
    return tot


for d_ in (0.5, 5.0, 40.0):
    fa = float(kern.m(d_)) / d_ ** 2
    f1 = fdirect(d_, 1e-9)
    f2 = fdirect(d_, 1e-12)
    P(f"  d = {d_:5g} kpc: rel err (eps 1e-9) = {abs(f1 / fa - 1):.2e}; (eps 1e-12, split intervals) = {abs(f2 / fa - 1):.2e}")

R.banner("P2  self-force relative to its own scale")
mu_nodes, mu_w = np.polynomial.legendre.leggauss(64)
selfF, scale = 0.0, 0.0
for s in np.geomspace(1e-3, 1e3, 200):
    selfF += float(kern.K(s)) * (mu_nodes * mu_w).sum() * 2 * math.pi
    scale += float(kern.K(s)) * (np.abs(mu_nodes) * mu_w).sum() * 2 * math.pi
P(f"  |sum| = {abs(selfF):.2e}; scale sum|.| = {scale:.2e}; relative = {abs(selfF) / scale:.2e}  (the frozen-run line was an absolute 1e-12 on a dimensionful sum dominated by K(1e-3 kpc) ~ 3e4)")

R.banner("P3  Hubble-scale kernel K = 1/(4 pi L s^2): where R peaks")
Lh = C_KMS / (0.06736 * math.sqrt(3 * 0.6847))
best = (0, None)
for M in MASSES:
    for x in XGRID:
        r = rM(M, a0) * x
        Rv = float(R_point(RM(1.0, Lh, 0.0), np.array([r]), M, a0)[0])
        if Rv > best[0]:
            best = (Rv, (M, x, r))
P(f"  max R = {best[0]:.3e} at M = {best[1][0]:.1e}, x = {best[1][1]:.3g}, r = {best[1][2]:.3g} kpc; the 0.9 pass line is {0.9 / best[0]:.2e} times larger. (K is A/(4 pi L s^2) with L = c/(H0 sqrt(3 Omega_L)) = {Lh:.3e} kpc)")

R.banner("P4  shell leakage of the recalled RM kernel (h = 2 kpc, M = 1e10) versus shell separation; kernel range 1/mu = 10 kpc")
from cfg120_common import rhoD_sphere, cum_mass, exp_rho, Mb_exp
M = 1e10
rstar = rM(M, a0)
for fsep in (1.5, 2.0, 4.0, 8.0, 16.0):
    Rsh, msh = fsep * rstar, 10.0 * M
    rgrid = np.geomspace(2e-3, rstar, 400)
    rho0 = rhoD_sphere(kern, exp_rho(M, 2.0), rgrid, 120.0)
    rhoS = msh / (2 * rgrid * Rsh) * (kern.Q(rgrid + Rsh) - kern.Q(np.abs(rgrid - Rsh)))
    Mb = float(Mb_exp(M, 2.0, rstar))
    C0 = rho0[-1] * (Mb + cum_mass(rgrid, rho0)[-1])
    C1 = (rho0 + rhoS)[-1] * (Mb + cum_mass(rgrid, rho0 + rhoS)[-1])
    P(f"  shell at {fsep:g} r* = {Rsh:.1f} kpc: Delta C/C = {C1 / C0 - 1:+.3f}")
R.write()
