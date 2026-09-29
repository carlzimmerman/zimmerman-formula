#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POSTHOC_1_notes -- POST-HOC (written AFTER the first G1 number; nothing here is a gate, a pre-registered claim or evidence).  Reported so the reader can see
what was looked at after the fact.

(1) numerology flagged, not claimed: a_mech/a0 = mu/(kappa sqrt(3 Omega_L/8 pi)) is 1.986 for kappa = 1/2; it is 0.993 for kappa = 1, i.e. m c^2 is within 0.7% of c sqrt(G rho_Lambda) (a0 with kappa = 1).
    That is the expected SCALE (the RR dark energy is ~ m^2 c^2/G by construction, m is shot to Omega_DE = 0.68) plus an accidental 0.7%; no derivation exists; kappa = 1/2 is FITTED.
    A coincidence of a shot number of the RR background with a constant is not a tie (G4-b stays FAIL).
(2) at what radius would the RR response weaken gravity by 10%?  delta g / g_N = -(m r)^2/6 (A1, exact leading order) -> r = sqrt(0.6)/m.
(3) robustness of the nonlinear coefficient to the U prescription: the N1 run used 'U -> 0 at infinity'; here U(r_max) = 0 at r_max = 1000 h is imposed instead
    (a different homogeneous constant), and the eps = +/-1e-4 second-order coefficient c2(r/h) is recomputed.
(4) the RR effective-density sign: rho_eff < 0 everywhere; the ratio of |rho_eff| to the uniform background dark-energy density at r = x r_M.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *
import cfg123_nl as NL

print("POST-HOC notes (not gates)")
lam, sol = rr_background()
mu = math.sqrt(lam)
print(f"(1) a_mech/a0 = {mu / (KAPPA * math.sqrt(3 * OL_CANON / (8 * math.pi))):.4f} at kappa = 1/2; the kappa that would make it 1: {mu / math.sqrt(3 * OL_CANON / (8 * math.pi)):.4f}")
m_inv = mu * H0_SI / C_SI
r10 = math.sqrt(0.6) / m_inv
print(f"(2) delta g/g_N = -(m r)^2/6 reaches -10% at r = {r10 / MPC / 1e3:.2f} Gpc = {r10 * H0_SI / C_SI:.2f} c/H0")

# (3) alternative U prescription
rmax = 1000.0
rr = np.array([0.5, 2.0, 5.0, 20.0, 100.0, 500.0])
res = {}
for e in (1e-4, -1e-4):
    pc = NL.solve_bg_pc(e, rmax)
    a = NL.integrate(e, 0.0, pc, 0.0, rmax).y[3, -1]
    b = NL.integrate(e, 0.0, pc, 1.0, rmax).y[3, -1]
    Uc_alt = -a / (b - a)                                       # U~(r_max) = 0
    o, _ = NL.variational(e, rmax, pc=pc, Uc=Uc_alt, rout=rr)
    res[e] = o["g_lam"]
o0, _ = NL.variational(0.0, rmax, rout=rr)
# for eps = 0 the alternative prescription is U~(rmax) = 0 as well
a = NL.integrate(0.0, 0.0, 0.0, 0.0, rmax).y[3, -1]; b = NL.integrate(0.0, 0.0, 0.0, 1.0, rmax).y[3, -1]
o0a, _ = NL.variational(0.0, rmax, pc=0.0, Uc=-a / (b - a), rout=rr)
c2 = (res[1e-4] - res[-1e-4]) / (2e-4) / o0a["g_lam"]
print("(3) r/h:                       ", rr.tolist())
print("    linear g_lam, standard P0:  ", np.round(o0["g_lam"], 5).tolist())
print("    linear g_lam, U(rmax)=0:    ", np.round(o0a["g_lam"], 5).tolist(), " (the LINEAR response itself depends on this homogeneous constant at large r/h)")
print("    c2 (U(rmax)=0):             ", np.round(c2, 4).tolist(), "  (standard P0 range in A3: -0.302 .. +0.846)")
# (4)
rho_bg = 3 * H0_SI ** 2 * OL_CANON / (8 * math.pi * G_SI)
a0 = A0_FOOT["canonical"]
print("(4) |rho_eff|/rho_DE^bg at r = x r_M (point mass, canonical):")
for M in MASSES:
    rM = rM_m(M, a0)
    print(f"    {M:.0e}: " + "  ".join(f"x={x:g}: {m_inv ** 2 * M * MSUN / (12 * math.pi * x * rM) / rho_bg:.2e}" for x in (0.1, 1.0, 30.0)))
