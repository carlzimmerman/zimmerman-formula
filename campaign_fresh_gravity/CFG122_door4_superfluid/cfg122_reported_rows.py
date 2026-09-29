#!/usr/bin/env python3
"""CFG122 reported-only rows R1, R3, R4 (frozen criteria (c) 'Reported-only rows'; no pass lines; never pooled with the gates).  R2 (T convention x1/2, x2) is inside cfg122_g6_twofluid.py, R5 in cfg122_posthoc_prior_art.py.
R1  G1.3 against the nu_mono phantom (the chain's monotone kernel, CFG44 Bcommon.nu_mono, read-only): the pure-gradient B- solution g_b = g_N + sqrt(a0 g_N) (point mass, DM negligible) vs g_law = nu(g_N/a0) g_N.
R3  the finite-T superfluid fraction rho_s/rho = 1 - rho_crit/rho of the two-fluid halo along the CFG44 target profile (T = m sigma^2, sigma^2 = V_f^2/2), for m = 0.1, 1, 10 eV.
R4  the galaxy-galaxy lensing deficit of Branch F: dynamics M_dyn = M_b nu vs the lensing (Newtonian, real) mass M_b + M_DM; with M_DM negligible the deficit is nu = g_law/g_N (M_b = 6e10 at 40 kpc and 2.2 Mpc, both footings).
Run: ZF_REPO=<repo> python3 cfg122_reported_rows.py"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *
R = Report("cfg122_reported_rows")
P = R.P
R.banner("R1  Branch F (pure-gradient B-) against the nu_mono phantom law and against P2")
bc = None
if REPO:
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
    import Bcommon as bc
xg = np.geomspace(0.1, 30, 400)
for foot in FOOTINGS:
    y = 1.0 / xg ** 2          # g_N/a0 = (r_M/r)^2 = 1/x^2 (point mass)
    g_bk = y * (1 + np.sqrt(1 / y))        # (g_N + sqrt(a0 g_N))/a0
    g_p2 = y * np.sqrt(1 + 1 / y)
    line = f"  [{foot}] point mass: max |g_BK/g_P2 - 1| = {np.max(np.abs(g_bk / g_p2 - 1)):.3f} (at x = {xg[np.argmax(np.abs(g_bk / g_p2 - 1))]:.2f})"
    if bc is not None:
        g_nm = y * bc.nu_mono(y)
        e = np.abs(g_bk / g_nm - 1)
        line += f";  max |g_BK/g_numono - 1| = {np.max(e):.3f} (at x = {xg[np.argmax(e)]:.2f}); within 10% for x >= {xg[e <= 0.10].min() if (e <= 0.10).any() else float('nan'):.3g} and x <= {xg[e <= 0.10].max() if (e <= 0.10).any() else float('nan'):.3g}"
    P(line)
R.banner("R3  finite-T superfluid fraction along the target profile (two-fluid EOS, T = m sigma^2), point mass")
for foot in FOOTINGS[:1]:
    a0n = a0_nat(foot)
    for Mmsun in MASSES:
        M = Mmsun * MSUN_EV; rMv = float(rM(M, a0n)); V2 = float(Vf2(M, a0n)); sig2 = 0.5 * V2
        xs = np.array([0.1, 1.0, 3.0, 10.0, 30.0])
        rho_t = a0n / (4 * math.pi * G_N * rMv * xs * np.sqrt(1 + xs ** 2))
        for mm in (0.1, 1.0, 10.0):
            rc = mm * ZETA32 * (mm * mm * sig2 / (2 * math.pi)) ** 1.5
            fs = np.clip(1 - rc / rho_t, 0, 1)
            P(f"  [{foot}] M_b={Mmsun:.0e}, m = {mm:g} eV: rho_crit/rho_target(x=0.1..30) = " + ", ".join(f"{rc / v:.3g}" for v in rho_t) + "  -> superfluid fraction " + ", ".join(f"{v:.3f}" for v in fs))
R.banner("R4  Branch F lensing deficit (dynamics/lensing mass ratio nu = g_law/g_N; DM negligible)")
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    for lab, rkpc in (("40 kpc", 40.0), ("2.2 Mpc", 2200.0)):
        M = 6e10 * MSUN_EV
        gN = G_N * M / (rkpc * KPC_EV) ** 2
        P(f"  [{foot}] M_b = 6e10, r = {lab}: g_N/a0 = {gN / a0n:.3g}; P2 dynamical/baryonic mass = {math.sqrt(1 + a0n / gN):.4g}; BK (g_N + sqrt(a0 g_N))/g_N = {1 + math.sqrt(a0n / gN):.4g}")
R.check("reported rows R1, R3, R4 recorded", "no pass lines", True, load_bearing=False)
R.write()
