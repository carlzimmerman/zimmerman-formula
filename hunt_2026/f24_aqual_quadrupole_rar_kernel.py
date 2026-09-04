#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f24 -- the Solar-System EFE quadrupole of the framework's own kernel in EXACT AQUAL (non-spherical solve).

f23 section 6 computed the quadrupole with the committed QUMOND integral (DHF24 eq. 10).  The parallel agent's
review (two_kernel_orbit_shape_2026/REPORT.md, 2026-09-04) correctly scoped that as a QUMOND number: AQUAL does not
share it exactly.  DHF footnote 6 says AQUAL is ~25% LARGER for mu_1.  This file removes the caveat for the
framework's kernel by solving the full axisymmetric AQUAL boundary-value problem

    div[ mu(|grad phi|/a_0) grad phi ] = 4 pi G M delta^3(r),      grad phi -> -g_ext zhat,

with the repository's validated finite-volume solver (theory_2026/aqual_solver_2026.py: V1 spherical first
integral, V2 Blanchet-Novak 2011 anchor to 6%, V3 the DHF footnote-6 excess), and the framework's kernel in its
AQUAL form 1 - mu = exp(-sqrt(x mu)), tabulated once by root-finding and interpolated log-log.

Units GM = a_0 = 1.  q_zz = 2 c_2 from the inner multipole fit; the frozen convention is
|Q_2| = (3/2) |q_zz| a_0^{3/2} / sqrt(G M_sun), against the Park 2026 two-sigma ceiling 5.2e-27 s^-2.
Both footings; g_ext = 2.32 +/- 0.16 e-10 m/s^2 (Gaia EDR3 solar circle, DHF24 sec 3.3).
"""
import os, sys, math, time
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *
sys.path.insert(0, os.path.join(HERE, "..", "qwen_claude_field_theory", "theory_2026"))
from aqual_solver_2026 import Grid, solve, multipoles, grads

ck = Check()
t0 = time.time()
GM_SUN = 6.6743e-11*1.98892e30
GEXT, SGEXT = 2.32e-10, 0.16e-10
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27
PREF = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)
QUMOND_Q = {"rar_eta2": 0.2210, ("canonical", "rar"): 0.2748, ("alt", "rar"): 0.2272,
            ("canonical", "exp"): 0.1658, ("alt", "exp"): 0.1654,
            ("canonical", "rar-1s"): 0.2562, ("alt", "rar-1s"): 0.2105}      # f23 section 6 (committed integral)

P("=" * 110); P("f24 -- exact-AQUAL Solar-System quadrupole for the framework's kernel"); P("=" * 110)

# ---- the framework's kernel in AQUAL form, tabulated through s = sqrt(x mu): 1 - s^2/x = e^{-s}, s in (0, sqrt x)
def mu_root(xx):
    if xx < 1e-13: return xx*(1 - xx)
    sh = math.sqrt(xx); h = lambda s_: 1.0 - s_*s_/xx - math.exp(-s_)
    if h(sh) >= 0.0: return 1.0                      # e^{-sqrt x} below double precision: mu = 1 to machine accuracy
    s_ = brentq(h, 0.1*min(xx, 1.0), sh, xtol=1e-15*sh, rtol=1e-14)
    return s_*s_/xx
xs = np.logspace(-14, 8, 6001)
mus = np.minimum(np.array([mu_root(xx) for xx in xs]), 1.0)
lxs, lmus = np.log(xs), np.log(mus)
def mu_rar(x):
    x = np.asarray(x, float); lx = np.log(np.clip(x, 1e-14, 1e8))
    out = np.exp(np.interp(lx, lxs, lmus))
    return np.where(x > 1e8, 1.0, out)
def mu_exp(x): return 1.0 - np.exp(-np.asarray(x, float))
# fidelity against the INDEPENDENT closed form x(mu) = [ln(1 - mu)]^2 / mu (f23 5a), at random mu
rng = np.random.default_rng(3); mt = rng.uniform(0.001, 0.999, 200); xt = np.log(1 - mt)**2/mt
ck("T1 the tabulated kernel reproduces the closed-form inverse x(mu) = [ln(1-mu)]^2/mu to 1e-4 relative (the quadrupole is quoted to 1e-2) at 200 random "
   "points (interpolation on 6001 nodes), and is monotone with mu -> 1 at x = 1e8",
   np.max(np.abs(mu_rar(xt)/mt - 1)) < 1e-4 and np.all(np.diff(mus) >= -1e-12) and abs(float(mu_rar(1e8)) - 1) < 1e-12,
   f"max rel err {np.max(np.abs(mu_rar(xt)/mt - 1)):.1e}; mu(1e8) = {float(mu_rar(1e8)):.15f}")

# ---- V1-type spherical validation with THIS kernel: mu(g) g = 1/r^2 exactly
G1 = Grid(1e-4, 1e4, 320, 32)
u, phi, it, du = solve(G1, mu_rar, 0.0, itmax=400)
gnum = grads(G1, phi)[:, G1.nt//2]
gex = np.array([math.exp(brentq(lambda lg: math.log(float(mu_rar(math.exp(lg)))*math.exp(lg)) + 2*math.log(rr), -40.0, 40.0, xtol=1e-12)) for rr in G1.r])
m = (G1.r > 1e-3) & (G1.r < 1e3); err = np.max(np.abs(gnum[m]/gex[m] - 1))
ck("V1 with the framework's kernel the solver reproduces the exact spherical first integral mu(g) g = 1/r^2 to 2%",
   err < 0.02, f"max rel err {err:.3e}, {it} iters, resid {du:.1e}   ({time.time()-t0:.0f} s)")

# ---- the external-field solves on the validated grid
G2 = Grid(1e-4, 1e4, 512, 128)
def q_aqual(mufun, eta):
    u, phi, it, du = solve(G2, mufun, eta, itmax=400, relax=0.5)
    a0c, a2c, c2 = multipoles(G2, u, eta)
    return abs(2.0*c2), it, du
RES = {}
qa2, it, du = q_aqual(mu_rar, 2.0); RES["rar_eta2"] = qa2
info(f"framework kernel, eta = 2.000: AQUAL |q_zz| = {qa2:.4f}  vs QUMOND q = {QUMOND_Q['rar_eta2']:.4f}  excess {qa2/QUMOND_Q['rar_eta2']-1:+.1%}   ({it} iters, resid {du:.1e}, {time.time()-t0:.0f} s)")
ck("A1 the AQUAL-vs-QUMOND excess for the framework's kernel at eta = 2 is positive and of the size DHF footnote 6 "
   "reports for the similar mu_1 (about +25%; accepted band 0 to +60%)", 0.0 < qa2/QUMOND_Q["rar_eta2"] - 1 < 0.6,
   f"excess {qa2/QUMOND_Q['rar_eta2']-1:+.1%}")
for foot, a0 in A0.items():
    for nm, mf, key in (("framework kernel (RAR)", mu_rar, "rar"), ("mu_exp", mu_exp, "exp")):
        q, it, du = q_aqual(mf, GEXT/a0); RES[(foot, key)] = q
        Q = q*PREF(a0)
        info(f"{foot:9s} {nm:24s} eta = {GEXT/a0:.3f}: AQUAL |q_zz| = {q:.4f} (QUMOND {QUMOND_Q[(foot, key)]:.4f}, excess {q/QUMOND_Q[(foot, key)]-1:+.1%});  "
             f"|Q2| = {Q:.3e} s^-2 = {Q/Q2_CEIL:.2f}x ceiling, {(Q-Q2_CEN)/Q2_SIG:.1f} sigma above Park central   ({it} it, {time.time()-t0:.0f} s)")
    q, it, du = q_aqual(mu_rar, (GEXT - SGEXT)/a0); RES[(foot, "rar-1s")] = q
    info(f"{foot:9s} framework kernel at g_ext - 1 sigma (eta = {(GEXT-SGEXT)/a0:.3f}): AQUAL |q_zz| = {q:.4f}, |Q2| = {q*PREF(a0)/Q2_CEIL:.2f}x ceiling   ({time.time()-t0:.0f} s)")
ck("A2 (HYPOTHESIS CHECK -- a FAIL is the result) in exact AQUAL the framework's kernel clears the Park 2026 "
   "two-sigma ceiling on at least one footing at g_ext - 1 sigma",
   any(RES[(f, "rar-1s")]*PREF(A0[f])/Q2_CEIL < 1.0 for f in A0),
   "; ".join(f"{f}: {RES[(f, 'rar')]*PREF(A0[f])/Q2_CEIL:.2f}x central, {RES[(f, 'rar-1s')]*PREF(A0[f])/Q2_CEIL:.2f}x at g_ext - 1 sigma" for f in A0))
ck("A3 exact AQUAL is at least as constraining as the QUMOND integral for the framework's kernel on both footings "
   "(the parallel agent's caveat runs the wrong way for an escape)",
   all(RES[(f, "rar")] >= 0.95*QUMOND_Q[(f, "rar")] for f in A0), "; ".join(f"{f}: AQUAL/QUMOND = {RES[(f, 'rar')]/QUMOND_Q[(f, 'rar')]:.3f}" for f in A0))
ck("A4 mu_exp shows a comparable AQUAL excess, so the excess is a property of the AQUAL operator and not of this kernel's table",
   all(0.0 < RES[(f, "exp")]/QUMOND_Q[(f, "exp")] - 1 < 0.6 for f in A0), "; ".join(f"{f}: {RES[(f, 'exp')]/QUMOND_Q[(f, 'exp')]-1:+.1%}" for f in A0))
P(f"\n  total runtime {time.time()-t0:.0f} s")
sys.exit(ck.done())
