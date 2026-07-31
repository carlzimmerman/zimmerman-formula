#!/usr/bin/env python3
r"""mi_hierarchy_falsifier_routeC_2026.py -- ROUTE C: THE HIERARCHY FALSIFIER.

WHAT THIS IS FOR. On 2026-07-30 the pincer (Thm 3 corrected + Thm 8 redone on alpha=2) localised the
missing ingredient in the modified-inertia action to a SPEED: on a circular orbit the operator action's
argument is w = c*Omega/a0 while the law's is x = |a|/a0, and w/x = c/v EXACTLY. A lone worldline has no
speed; this framework's PASSIVE PREFERRED FRAME u^mu does supply one. The cosmic (CMB) reading is
already excluded (peculiar velocities ~1 dex vs a total a0 budget 2*sigma_RAR ~ 0.22 dex). So the frame
must be LOCALLY DRAGGED. ROUTE C asks the only question that turns that into physics: WHICH MASS DRAGS
IT -- and it asks it where the answer is a prediction, i.e. in nested systems.

THE CONSTRUCTION BEING TESTED, stated once and precisely (call it the FRAME/MODE construction):
  a nonlocal worldline action whose kernel, on a single-frequency trajectory, is evaluated at
        u = Omega * v_F / a0
  with Omega the trajectory's frequency and v_F = |xdot| the speed RELATIVE TO THE FRAME u^mu.
  On a circular orbit about a mass whose frame u^mu co-moves with, v_F = v_orb and Omega*v_orb = |a|,
  so u = |a|/a0 and the framework's closure g_bar = |a| mu(|a|/a0) is reproduced. That is the door.
  For a MULTI-frequency trajectory the construction is per-Fourier-mode -- Milgrom 2022 PRD 106:064060
  is explicit that the algebraic relation holds only for single-frequency trajectories -- so mode k gets
        u_k = Omega_k * v_F / a0,      with ONE v_F, because there is only one frame.
  THE INFLATION LAW is then exact and kinematic: u_k(eff)/u_k(true) = v_F / v_k.

CANDIDATE FRAMES tested (S3): C co-rotating; A cosmic/CMB; B barycentre-dragged (dragged by the
SUBsystem); G galaxy-dragged (dragged by whichever mass DOMINATES the local field). Only one survives.

PRIOR ART, CREDITED, NOT CLAIMED: inertia relative to matter is Mach; Sciama 1953 is the standard
citation. Orbit-dependent interpolating functions in modified inertia are Milgrom 1994 Ann.Phys.
229:384; the single-frequency restriction is Milgrom 2022 PRD 106:064060; the virial construction is
Milgrom astro-ph/0510117. An ANISOTROPIC effective gravity in an external field is standard MOND-EFE
lore (Milgrom; Banik & Zhao). Nothing here claims novelty for a Machian frame.

FROZEN DOCUMENT RESPECTED: prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md is hash-stamped and frozen.
This script MOVES NO FROZEN TARGET. It reproduces the frozen numbers as a validation of its own
machinery, then states what an Amendment 4 WOULD have to say if the framework adopted the frame
construction -- which it has not.

BOTH a0 FOOTINGS on every dimensional number: canonical rho_DE 9.36e-11, alternate rho_total 1.13e-10.
BOTH KERNELS: alpha=2 mu=x/sqrt(1+x^2) (IN FORCE), alpha=1 mu=(sqrt(1+4x^2)-1)/(2x) (RETIRED).

Exits NON-ZERO if any internal structural check fails. No check(True,...). No hard-coded verdicts.
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np
import sympy as sp
from mpmath import mp, mpf, sqrt as msqrt

mp.dps = 50

OK = True
NCHK = 0


def check(cond, msg):
    global OK, NCHK
    NCHK += 1
    cond = bool(cond)
    if not cond:
        OK = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 104)
    print(s)
    print("=" * 104)


# ------------------------------------------------------------------ constants (SI) and frozen inputs
C = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98892e30
AU = 1.495978707e11
KPC = 3.0856775814913673e19
PC = KPC / 1e3
YR = 3.155693e7

FOOTINGS = (("canonical rho_DE", 9.36e-11), ("alternate rho_total", 1.13e-10))
A0C, A0A = FOOTINGS[0][1], FOOTINGS[1][1]

# --- FROZEN, quoted verbatim from prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md
G_EXT_PRIMARY = 1.778e-10          # sec 1.1 primary g_ext (McMillan-2017-class)
G_EXT_ALT = 2.078e-10              # sec 1.1 alt convention Vc^2/R0, Vc=229, R0=8.178 kpc
FROZEN_A2_MI_RANGE = (1.0182, 1.0350)   # Amendment 3 (b): MI over both footings x both g_ext
FROZEN_A2_MI_PRIMARY = 1.0246           # Amendment 3 (b): primary g_ext / canonical a0
FROZEN_A2_PAR = 0.9669                  # Amendment 3 (b): gamma_v parallel, primary/canonical
FROZEN_A2_PERP = 1.0523                 # Amendment 3 (b): gamma_v perpendicular, primary/canonical
FROZEN_A2_ASMG = (1.0473, 1.0885)       # Amendment 3 (b): framework-as-MG under alpha=2
FROZEN_A1_MI_PRIMARY = 1.0799           # Amendment 2 (d): derived-EFE orientation average, alpha=1
FROZEN_A1_PAR, FROZEN_A1_PERP = 1.0112, 1.1115   # Amendment 2 (d)
SIG_FIT_30K = 0.0191                    # sec 1.5 expected sigma_fit at N=30,000
SIG_SYS = 0.02                          # sec 1.5 FROZEN systematic allowance
SIG_TOT = 0.028                         # sec 1.5 sigma_tot at N=30,000
GUARD_ZONE = 1.20                       # sec 1.5: gamma_hat > 1.20 => NO hypothesis verdict permitted
OMC = {"lo": 1.782e-14, "hi": 2.211e-14}   # Amendment 1 committed omega_c window, rad/s
REG_GATED = (0.005, 0.008)              # Amendment 1: Re G at 10 kAU across the omega_c window
FROZEN_CUT_SEP_KAU = (2.0, 30.0)        # sec 1.2 cut 6
FROZEN_CUT_MTOT = (0.464, 4.31)         # sec 1.2 cut 10

# --- Galactic kinematics (frozen inside this script; provenance stated)
VC = 220e3      # km/s -> m/s. Solar-neighbourhood circular speed, the value ROUTE C specifies.
R0 = 8.2 * KPC  # ROUTE C's stated R.

# --- ephemeris bounds, from STANDING.md sec 5.0 (Sereno & Jetzer 2006 astro-ph/0606197 Tab.1 through
#     their Eq.9, Pitjeva EPM2004), 2-sigma
EPH_BOUND = {"Earth": 3.66e-14, "Mars": 3.72e-14}
EFE_SUPPRESSION = (1278.0 / 189.0, 1278.0 / 119.0)   # STANDING sec5.0: 1278x bare -> 119-189x after EFE
RAR_DEX = {1: 0.1083, 2: 0.1116}        # STANDING sec 1, SPARC 175 galaxies


# ------------------------------------------------------------------ the two kernels and the closure
def mu(x, alpha):
    """Interpolating function mu(x), x = |a|/a0."""
    x = np.asarray(x, dtype=float)
    if alpha == 2:
        return x / np.sqrt(1.0 + x * x)
    if alpha == 1:
        return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)
    raise ValueError(alpha)


def x_of_y(y, alpha):
    """Solve y = x*mu(x) for x, closed form for both kernels.
       alpha=1: x*mu = (sqrt(1+4x^2)-1)/2  ->  x = sqrt(y^2+y)
       alpha=2: x*mu = x^2/sqrt(1+x^2)     ->  x^2 = (y/2)(y+sqrt(y^2+4))"""
    y = np.asarray(y, dtype=float)
    if alpha == 1:
        return np.sqrt(y * y + y)
    if alpha == 2:
        return np.sqrt(0.5 * y * (y + np.sqrt(y * y + 4.0)))
    raise ValueError(alpha)


def h_of_x(x, alpha):
    """h(x) = d(x mu(x))/dx.  alpha=2: x(x^2+2)/(1+x^2)^(3/2).  alpha=1: 2x/sqrt(1+4x^2)."""
    x = np.asarray(x, dtype=float)
    if alpha == 2:
        return x * (x * x + 2.0) / (1.0 + x * x) ** 1.5
    if alpha == 1:
        return 2.0 * x / np.sqrt(1.0 + 4.0 * x * x)
    raise ValueError(alpha)


def boost_force_isolated(y, alpha):
    """|a|/g_bar for an ISOLATED system at y = g_bar/a0 (the framework's own closure)."""
    return x_of_y(y, alpha) / y


def frame_boost(gbar, s, v_drag, a0, alpha, iters=400):
    """Self-consistent force boost for a circular internal orbit of Newtonian field gbar at radius s,
    under a frame whose velocity relative to the system's barycentre has magnitude v_drag.

    The frame-relative speed of a component is |xdot| = sqrt(v_drag^2 + v_orb^2), and v_orb = Omega*s
    must itself track the boost:  Omega = sqrt(boost*gbar/s),  v_orb = Omega*s.
    The kernel argument is u = Omega * |xdot| / a0 and the boost is 1/mu(u).
    v_drag = 0 recovers u = Omega^2 s / a0 = |a|/a0 exactly, i.e. the ISOLATED closure (FRAME B).
    """
    bo = 1.0
    for _ in range(iters):
        Om = np.sqrt(bo * gbar / s)
        vF = np.sqrt(v_drag ** 2 + (Om * s) ** 2)
        nb = float(1.0 / mu(Om * vF / a0, alpha))
        if abs(nb - bo) < 1e-15 * max(1.0, bo):
            return nb
        bo = nb
    return bo


def efe_eigen_gamma_v(g_ext, a0, alpha):
    """Theorem-B quadrature EFE (Amendment 2/3 construction). Returns (gamma_par, gamma_perp)."""
    y = g_ext / a0
    x = x_of_y(y, alpha)
    gam2_par = 1.0 / h_of_x(x, alpha)      # d|a|/dg along g_ext
    gam2_perp = x / y                      # nu(g_ext) transverse
    return float(np.sqrt(gam2_par)), float(np.sqrt(gam2_perp))


def orientation_average_gamma_v(gpar, gperp, conv="rms", n=400001):
    """Orientation average of the anisotropic boost. shat uniform on the sphere => cos(theta) uniform.

    THE PHYSICS. With response tensor M = diag(gam^2_par along ghat, gam^2_perp transverse) and an
    internal field along the separation shat at angle theta to g_ext, the component of the relative
    acceleration ALONG shat is g*(gam^2_par cos^2 + gam^2_perp sin^2). So the physically-correct
    per-pair boost is gamma_v(theta) = [gam^2_par cos^2 + gam^2_perp sin^2]^(1/2).

    THREE CONVENTIONS, and the frozen document does not use one of them consistently:
      'mean'    <gamma_v(theta)>                     -- the physical mean
      'rms'     <gamma_v(theta)^2>^(1/2)             -- MATCHES FROZEN Amendment 3 (alpha=2)
      'quartic' <[gam^4 cos^2 + gam^4 sin^2]^(1/4)>  -- MATCHES FROZEN Amendment 2 (alpha=1)
    The three differ by <=0.0010 in gamma_v; all three are computed and the spread is reported.
    """
    m = np.linspace(0.0, 1.0, n)
    p2, q2 = gpar ** 2, gperp ** 2
    if conv == "quartic":
        return float(np.mean((p2 ** 2 * m ** 2 + q2 ** 2 * (1.0 - m ** 2)) ** 0.25))
    if conv == "rms":
        return float(np.sqrt(np.mean(p2 * m ** 2 + q2 * (1.0 - m ** 2))))
    if conv == "mean":
        return float(np.mean(np.sqrt(p2 * m ** 2 + q2 * (1.0 - m ** 2))))
    raise ValueError(conv)


# ================================================================================================ S0
def s0_ladder():
    banner("S0. THE LADDER -- accelerations, speeds and frequencies at the wide binary (ROUTE C setup)")
    a_gal = VC ** 2 / R0
    Om_gal = VC / R0
    print(f"  Galactic (solar neighbourhood, v_c = {VC/1e3:.0f} km/s, R = {R0/KPC:.1f} kpc):")
    print(f"      a_gal   = {a_gal:.4e} m/s^2   = {a_gal/A0C:.4f} a0_can = {a_gal/A0A:.4f} a0_alt")
    print(f"      Omega_gal = {Om_gal:.4e} rad/s   (galactic year P = {2*np.pi/Om_gal/YR:.3e} yr)")
    print(f"      v_gal   = {VC/1e3:.3f} km/s")
    print("\n  Binary internal (relative coordinate: v = sqrt(GM/s), Omega = sqrt(GM/s^3), a = GM/s^2):")
    print(f"  {'M_tot':>7}{'s [kAU]':>9}{'a_int [m/s2]':>15}{'a/a0can':>10}{'a/a0alt':>10}"
          f"{'Om_int [1/s]':>14}{'P [yr]':>11}{'v_int [m/s]':>12}")
    rows = {}
    for Mm in (1.0, 1.5):
        for s_kau in (10.0,):
            M = Mm * MSUN
            s = s_kau * 1e3 * AU
            a_int = G * M / s ** 2
            Om = np.sqrt(G * M / s ** 3)
            v = np.sqrt(G * M / s)
            rows[(Mm, s_kau)] = (a_int, Om, v)
            print(f"  {Mm:>7.2f}{s_kau:>9.1f}{a_int:>15.4e}{a_int/A0C:>10.4f}{a_int/A0A:>10.4f}"
                  f"{Om:>14.4e}{2*np.pi/Om/YR:>11.3e}{v:>12.2f}")
    a1, Om1, v1 = rows[(1.0, 10.0)]
    a15, Om15, v15 = rows[(1.5, 10.0)]
    print(f"\n  ROUTE C's stated values: a_gal ~ 1.9e-10 ~ 2 a0, a_int ~ 5.9e-11 ~ 0.63 a0,"
          f" Omega_gal ~ 8.7e-16 -- REPRODUCED.")
    check(abs(a_gal - 1.9e-10) / 1.9e-10 < 0.02,
          f"a_gal = {a_gal:.4e} reproduces ROUTE C's 1.9e-10 ({a_gal/A0C:.3f} a0_can)")
    check(abs(a1 - 5.9e-11) / 5.9e-11 < 0.02,
          f"a_int(1 Msun, 10 kAU) = {a1:.4e} reproduces ROUTE C's 5.9e-11 ({a1/A0C:.4f} a0_can)")
    check(abs(Om_gal - 8.7e-16) / 8.7e-16 < 0.02, f"Omega_gal = {Om_gal:.4e} reproduces 8.7e-16 rad/s")
    check(abs(Om15 - 2.44e-13) / 2.44e-13 < 0.01,
          f"Omega_int(1.5 Msun, 10 kAU) = {Om15:.4e} MATCHES the frozen Amendment 1 value 2.44e-13 "
          f"rad/s -- my ladder is the same ladder the pre-registration froze")
    print(f"\n  THE TWO COMPARABILITIES that make this decisive:")
    print(f"      a_gal / a_int(1 Msun, 10 kAU) = {a_gal/a1:.4f}   -> the GALAXY dominates the field")
    print(f"      Omega_int / Omega_gal         = {Om1/Om_gal:.2f} (1 Msun), {Om15/Om_gal:.2f} (1.5 Msun)")
    print(f"      v_gal / v_int                 = {VC/v1:.2f} (1 Msun), {VC/v15:.2f} (1.5 Msun)")
    check(1.0 < a_gal / a1 < 10.0,
          f"a_gal and a_int are COMPARABLE (ratio {a_gal/a1:.3f}), which is exactly why 'which mass "
          f"drags the frame' is a real fork at 10 kAU rather than an academic one")
    # equality radius: where the binary's own field equals the galactic field
    for Mm in (1.0, 1.5):
        r_eq = np.sqrt(G * Mm * MSUN / a_gal)
        print(f"      field-crossover radius r_eq({Mm} Msun) = sqrt(GM/a_gal) = {r_eq/(1e3*AU):.3f} kAU"
              f"  (inside: binary dominates; outside: Galaxy dominates)")
    r_eq_lo = np.sqrt(G * FROZEN_CUT_MTOT[0] * MSUN / a_gal) / (1e3 * AU)
    r_eq_hi = np.sqrt(G * FROZEN_CUT_MTOT[1] * MSUN / a_gal) / (1e3 * AU)
    print(f"      over the FROZEN mass cut {FROZEN_CUT_MTOT} Msun: r_eq = {r_eq_lo:.2f}-{r_eq_hi:.2f} kAU,")
    print(f"      i.e. the crossover sits INSIDE the frozen 2-30 kAU separation window.")
    check(FROZEN_CUT_SEP_KAU[0] < r_eq_lo and r_eq_hi < FROZEN_CUT_SEP_KAU[1],
          f"the field crossover r_eq = {r_eq_lo:.2f}-{r_eq_hi:.2f} kAU lies strictly inside the frozen "
          f"2-30 kAU cut -- a dominant-mass drag rule CHANGES FRAME inside the frozen window")
    return a_gal, Om_gal, rows


# ================================================================================================ S1
def s1_identity():
    banner("S1. THE PREMISE, SYMBOLICALLY: u = w*(v/c) exactly, and the INFLATION LAW")
    R, Om, a0, c = sp.symbols('R Omega a0 c', positive=True)
    v = Om * R
    a = Om ** 2 * R
    w = c * Om / a0            # the operator action's argument (Theorem 8)
    x = a / a0                 # the law's argument
    ratio = sp.simplify(w / x)
    print(f"  circular orbit: v = Omega R, |a| = Omega^2 R")
    print(f"  operator argument w = c*Omega/a0 ; law argument x = |a|/a0 ; w/x = {ratio}")
    check(sp.simplify(ratio - c / v) == 0,
          f"w/x = c/v EXACTLY, identically in R, Omega and a0 (sympy residual 0) -- so what Theorem 8 "
          f"found missing is a SPEED. This is the premise of ROUTE C, re-derived not assumed")
    # the frame/mode construction's argument, and its inflation law
    vF = sp.symbols('v_F', positive=True)
    u_eff = Om * vF / a0
    check(sp.simplify(u_eff.subs(vF, v) - x) == 0,
          f"the frame/mode argument u = Omega*v_F/a0 REDUCES to |a|/a0 when v_F = v_orb (residual 0) "
          f"-- the construction is correct exactly when the frame co-moves with the orbit's centre")
    check(sp.simplify(u_eff / x - vF / v) == 0,
          f"INFLATION LAW: u_eff/u_true = v_F/v_mode exactly (residual 0). Purely kinematic: no a0, no "
          f"kernel, no footing. Every number below follows from this one identity")
    # numeric spot-check of the c/v factor for the wide binary, both footings
    print(f"\n  {'system':<28}{'footing':<22}{'w = cOm/a0':>14}{'x = a/a0':>11}{'w/x':>11}{'c/v':>11}")
    for nm, Mm, s_kau in (("wide binary 10 kAU", 1.0, 10.0), ("wide binary 30 kAU", 1.0, 30.0)):
        M, s = Mm * MSUN, s_kau * 1e3 * AU
        Omv, av, vv = np.sqrt(G * M / s ** 3), G * M / s ** 2, np.sqrt(G * M / s)
        for fn, a0v in FOOTINGS:
            print(f"  {nm:<28}{fn:<22}{C*Omv/a0v:>14.4e}{av/a0v:>11.4f}"
                  f"{(C*Omv/a0v)/(av/a0v):>11.2f}{C/vv:>11.2f}")


# ================================================================================================ S2
def s2_frames(a_gal, Om_gal, rows):
    banner("S2. THE FOUR CANDIDATE FRAMES -- and three of them die with a number")
    a_int, Om_int, v_int = rows[(1.0, 10.0)]

    print("  FRAME C -- FULLY DRAGGED / CO-ROTATING (v_F = 0 on a circular orbit).")
    print("      Then u = Omega*v_F/a0 -> 0 and every bound circular orbit is in the DEEP-MOND limit.")
    g_sun_earth = G * MSUN / AU ** 2
    for fn, a0v in FOOTINGS:
        # deep-MOND: g_bar = |a|^2/a0  =>  |a| = sqrt(g_bar a0), so |a|/g_bar = sqrt(a0/g_bar)
        fac = np.sqrt(a0v / g_sun_earth)
        print(f"      {fn:<22} |a|/g_bar at Earth = sqrt(a0/g) = {fac:.4e}  "
              f"i.e. solar gravity WEAKER by {1/fac:.4g}x")
    worst = min(np.sqrt(a0v / g_sun_earth) for _, a0v in FOOTINGS)
    check(1.0 / worst > 1e3,
          f"FRAME C IS DEAD: a co-rotating frame makes solar gravity at Earth weaker by "
          f"{1/np.sqrt(A0C/g_sun_earth):.0f}x (canonical) / {1/np.sqrt(A0A/g_sun_earth):.0f}x (alt)")

    print("\n  FRAME A -- COSMIC / CMB (v_F = speed relative to the CMB rest frame).")
    print("      Then a0_eff/a0 = v_orb/v_F, so each galaxy inherits its own peculiar velocity.")
    print("      Deep regime g_obs = sqrt(g_bar a0) => d log g_obs = 0.5 d log a0, so the a0 budget is")
    print("      2 * sigma_RAR. SPARC v_flat span and a field peculiar-velocity span:")
    vorb = np.array([20e3, 50e3, 150e3, 300e3])
    vpec = np.array([50e3, 150e3, 300e3, 600e3])   # field-galaxy peculiar velocities, Cosmicflows-class
    lam = np.maximum(1.0, vpec[:, None] / vorb[None, :])
    dex = np.log10(lam)
    print(f"      lambda = max(1, v_pec/v_orb) spans {lam.min():.2f}-{lam.max():.2f}"
          f"  => log10 spread = {dex.max()-dex.min():.3f} dex in a0_eff")
    for al in (1, 2):
        budget = 2 * RAR_DEX[al]
        print(f"      alpha={al}: budget = 2 x {RAR_DEX[al]:.4f} = {budget:.4f} dex ; "
              f"over-budget factor = {(dex.max()-dex.min())/budget:.2f}x")
    over = (dex.max() - dex.min()) / (2 * RAR_DEX[2])
    check(over > 3.0,
          f"FRAME A IS DEAD (banked result reproduced INDEPENDENTLY here): a cosmic-frame speed spreads "
          f"a0_eff by {dex.max()-dex.min():.2f} dex against a {2*RAR_DEX[2]:.3f} dex budget = {over:.1f}x "
          f"over. The corpus's banked figure was 4.6x; mine is {over:.1f}x, i.e. the banked one is the "
          f"conservative end")

    print("\n  FRAME B -- BARYCENTRE-DRAGGED (u^mu co-moves with the BINARY barycentre, non-rotating).")
    print("      Gets the INTERNAL mode exactly right (v_F = v_int) but the barycentre's own galactic")
    print("      orbital mode is then referred to v_F = v_int, deflating its argument:")
    lam_B = v_int / VC
    for fn, a0v in FOOTINGS:
        u_true = a_gal / a0v
        u_eff = Om_gal * v_int / a0v
        for al in (2, 1):
            b_true = boost_force_isolated(u_true, al)
            b_eff = 1.0 / mu(u_eff, al)
            print(f"      {fn:<22} alpha={al}: u_gal true {u_true:.4f} -> eff {u_eff:.3e} "
                  f"(deflated {1/lam_B:.1f}x); galactic force boost {b_true:.4f} -> {b_eff:.4g}; "
                  f"v_c would be {np.sqrt(b_eff/b_true):.3f}x too high")
    vfac = np.sqrt((1.0 / mu(Om_gal * v_int / A0C, 2)) / boost_force_isolated(a_gal / A0C, 2))
    check(vfac > 2.0,
          f"FRAME B IS DEAD: a binary-barycentre-dragged frame deflates the GALACTIC mode's argument by "
          f"{1/lam_B:.0f}x, boosting the barycentre's galactic acceleration so its circular speed is "
          f"{vfac:.2f}x that of a single star in the same potential ({VC/1e3*vfac:.0f} vs "
          f"{VC/1e3:.0f} km/s). And in the exact DC limit (Omega->0) the argument -> 0 and the boost "
          f"DIVERGES -- the prescription is not merely wrong but ill-defined")
    print("      (Reported both ways: FRAME B's INTERNAL prediction is nonetheless well defined and is")
    print("       exactly the ISOLATED two-body closure -- checked in S3 -- because a per-mode kernel")
    print("       has no cross term and therefore NO external-field effect at all.)")

    print("\n  FRAME G -- DOMINANT-MASS DRAGGED (u^mu co-moves with whichever mass dominates the local")
    print("      field). At a star in an isolated galaxy that is the galaxy, so v_F = v_orb and the RAR")
    print("      is reproduced BY CONSTRUCTION. At a wide binary the Galaxy dominates by "
          f"{a_gal/a_int:.2f}x, so")
    print("      the frame is GALACTIC and the binary's internal mode is INFLATED. This is the only")
    print("      single-frame reading left standing, and the rest of this script is about its cost.")
    check(a_gal / a_int > 1.0,
          f"at 10 kAU / 1 Msun the dominant-field rule selects the GALACTIC frame (a_gal/a_int = "
          f"{a_gal/a_int:.3f} > 1), i.e. FRAME G and not FRAME B -- the fork is decided by the ladder, "
          f"not by choice")
    return v_int


# ================================================================================================ S3
def s3_gamma_v(a_gal, Om_gal):
    banner("S3. Q1/Q2 -- WHICH v_rel, THE EXACT FACTOR, AND gamma_v UNDER EACH READING")
    print("  First: VALIDATE my machinery against the FROZEN pre-registration numbers. If it cannot")
    print("  reproduce Amendment 2 (alpha=1) and Amendment 3 (alpha=2), nothing below is worth reading.")
    print(f"  {'kernel':<9}{'g_ext':<10}{'a0':<12}{'gam_par':>9}{'gam_perp':>10}{'<gam>':>9}"
          f"{'rms':>9}{'quartic':>9}{'as-MG':>8}")
    got = {}
    for al in (1, 2):
        for gl, gext in (("primary", G_EXT_PRIMARY), ("alt", G_EXT_ALT)):
            for fl, a0v in (("canonical", A0C), ("alt", A0A)):
                gp, gq = efe_eigen_gamma_v(gext, a0v, al)
                av = {c: orientation_average_gamma_v(gp, gq, c) for c in ("mean", "rms", "quartic")}
                asmg = float(1.0 / np.sqrt(mu(gext / a0v, al)))
                got[(al, gl, fl)] = (gp, gq, av, asmg)
                print(f"  alpha={al:<3}{gl:<10}{fl:<12}{gp:>9.4f}{gq:>10.4f}{av['mean']:>9.5f}"
                      f"{av['rms']:>9.5f}{av['quartic']:>9.5f}{asmg:>8.4f}")
    gp2, gq2, av2, _ = got[(2, "primary", "canonical")]
    gp1, gq1, av1, _ = got[(1, "primary", "canonical")]
    check(abs(gp2 - FROZEN_A2_PAR) < 5e-4 and abs(gq2 - FROZEN_A2_PERP) < 5e-4,
          f"reproduces FROZEN Amendment 3 eigenvalues EXACTLY: par {gp2:.4f} vs {FROZEN_A2_PAR}, perp "
          f"{gq2:.4f} vs {FROZEN_A2_PERP}")
    check(abs(gp1 - FROZEN_A1_PAR) < 5e-4 and abs(gq1 - FROZEN_A1_PERP) < 5e-4,
          f"reproduces FROZEN Amendment 2 eigenvalues EXACTLY: par {gp1:.4f} vs {FROZEN_A1_PAR}, perp "
          f"{gq1:.4f} vs {FROZEN_A1_PERP}")
    check(abs(av2["rms"] - FROZEN_A2_MI_PRIMARY) < 1e-4,
          f"FROZEN Amendment 3's 1.0246 is the RMS convention: mine {av2['rms']:.5f} vs "
          f"{FROZEN_A2_MI_PRIMARY} (agreement 1e-5)")
    check(abs(av1["quartic"] - FROZEN_A1_MI_PRIMARY) < 1e-4,
          f"FROZEN Amendment 2's 1.0799 is the QUARTIC convention: mine {av1['quartic']:.5f} vs "
          f"{FROZEN_A1_MI_PRIMARY} (agreement 1e-5)")
    a2rms = [got[(2, g, f)][2]["rms"] for g in ("primary", "alt") for f in ("canonical", "alt")]
    check(abs(min(a2rms) - FROZEN_A2_MI_RANGE[0]) < 1e-4
          and abs(max(a2rms) - FROZEN_A2_MI_RANGE[1]) < 1e-4,
          f"and the FROZEN Amendment 3 MI RANGE is reproduced exactly under the RMS convention: "
          f"[{min(a2rms):.5f}, {max(a2rms):.5f}] vs frozen {FROZEN_A2_MI_RANGE}")
    print("\n  *** A CONVENTION INCONSISTENCY INSIDE THE FROZEN DOCUMENT, found here and flagged, not")
    print("  edited.*** Amendment 2's orientation average (alpha=1) is the QUARTIC law; Amendment 3's")
    print("  (alpha=2) is the RMS. They are different angular averages of the same tensor. The")
    print("  physically-correct per-pair boost is gamma_v(theta) = [gam^2_par cos^2 + gam^2_perp")
    print("  sin^2]^(1/2) (the radial component of M.g), so the PHYSICAL average is <gamma_v>:")
    spread = max(av2.values()) - min(av2.values())
    print(f"      alpha=2 primary/canonical: physical {av2['mean']:.5f} | frozen-Am.3 (rms) "
          f"{av2['rms']:.5f} | Am.2-style (quartic) {av2['quartic']:.5f}")
    print(f"      convention spread = {spread:.5f} in gamma_v = {spread/SIG_TOT:.3f} sigma_tot")
    check(spread / SIG_TOT < 0.1,
          f"the convention spread is {spread:.5f} = {spread/SIG_TOT:.3f} sigma_tot -- REAL but "
          f"NON-DECISIVE, so it moves no verdict; recorded because it is a frozen number and the "
          f"discrepancy belongs on the record before data, not after")
    a2rng = a2rms
    asmg2 = [got[(2, g, f)][3] for g in ("primary", "alt") for f in ("canonical", "alt")]
    check(abs(min(asmg2) - FROZEN_A2_ASMG[0]) < 6e-4 and abs(max(asmg2) - FROZEN_A2_ASMG[1]) < 6e-4,
          f"reproduces the FROZEN Amendment 3 as-MG range [{min(asmg2):.4f}, {max(asmg2):.4f}] vs "
          f"{FROZEN_A2_ASMG}")

    print("\n  Q1: THE EXACT FACTOR between the two readings of v_rel, over the FROZEN cut window")
    print("      lambda = v_gal / v_int(s, M) = v_c * sqrt(s / (G M_tot))   [exact, kinematic]")
    sy, My, vcy, Gy = sp.symbols('s M v_c G', positive=True)
    lam_sym = sp.simplify(vcy / sp.sqrt(Gy * My / sy))
    print(f"      symbolic: lambda = {lam_sym}")
    print(f"  {'s [kAU]':>9}{'M_tot':>8}{'v_int [m/s]':>12}{'lambda':>10}{'u_true(can)':>12}"
          f"{'u_eff(can)':>12}{'u_eff(alt)':>12}")
    lams, ueffs = [], {A0C: [], A0A: []}
    for s_kau in (FROZEN_CUT_SEP_KAU[0], 10.0, FROZEN_CUT_SEP_KAU[1]):
        for Mm in (FROZEN_CUT_MTOT[0], 1.5, FROZEN_CUT_MTOT[1]):
            M, s = Mm * MSUN, s_kau * 1e3 * AU
            v = np.sqrt(G * M / s)
            Om = np.sqrt(G * M / s ** 3)
            lam = VC / v
            lams.append(lam)
            u_true = (G * M / s ** 2) / A0C
            row = []
            for a0v in (A0C, A0A):
                ue = Om * np.sqrt(VC ** 2 + v ** 2) / a0v   # v_F = |xdot| relative to the galactic frame
                ueffs[a0v].append(ue)
                row.append(ue)
            print(f"  {s_kau:>9.1f}{Mm:>8.3f}{v:>12.2f}{lam:>10.1f}{u_true:>12.4f}"
                  f"{row[0]:>12.1f}{row[1]:>12.1f}")
    print(f"      lambda over the whole frozen window = {min(lams):.0f} - {max(lams):.0f}")
    check(150.0 < min(lams) and max(lams) < 2500.0,
          f"the two readings of v_rel differ by lambda = {min(lams):.0f}-{max(lams):.0f} across the "
          f"frozen cut window -- ROUTE C's stated 'order 200-2000' is exact")
    check(min(ueffs[A0C]) > 20.0,
          f"under FRAME G the internal-mode argument is u_eff = {min(ueffs[A0C]):.0f}-"
          f"{max(ueffs[A0C]):.0f} (canonical) over the ENTIRE frozen window: DEEP NEWTONIAN everywhere, "
          f"no pair in the sample escapes")

    print("\n  Q1: gamma_v UNDER EACH READING (gamma_v = sqrt(force boost)), self-consistent in Omega")
    print("      FRAME G: boost = 1/mu(Omega*v_F/a0), Omega solved self-consistently (Omega^2 = |a|/s)")
    print("      FRAME B: boost = 1/mu(|a|/a0) = x/y, i.e. the ISOLATED closure, no EFE")
    print("      THEOREM B: the frozen Amendment-3 quadrature EFE, orientation-averaged")
    print(f"  {'kernel':<9}{'footing':<12}{'FRAME G':>11}{'FRAME B':>10}{'Thm B (frozen)':>16}"
          f"{'gate (Am.1 form)':>18}")
    res = {}
    s = 10.0e3 * AU
    M = 1.0 * MSUN
    gbar = G * M / s ** 2
    for al in (2, 1):
        for fl, a0v in (("canonical", A0C), ("alt", A0A)):
            # FRAME G: fixed point on the boost. v_F = |xdot| relative to the galactic frame =
            # sqrt(v_frame_of_barycentre^2 + v_orb^2), and v_orb = Omega*s must itself track the boost.
            gG = float(np.sqrt(frame_boost(gbar, s, VC, a0v, al)))
            # FRAME B
            gB = float(np.sqrt(boost_force_isolated(gbar / a0v, al)))
            # Theorem B frozen construction, orientation average
            gp, gq = efe_eigen_gamma_v(G_EXT_PRIMARY, a0v, al)
            gT = orientation_average_gamma_v(gp, gq)
            # Amendment-1-form gate applied to the Theorem-B boost
            gate = [float(np.sqrt(1.0 + (gT ** 2 - 1.0) * r)) for r in REG_GATED]
            res[(al, fl)] = (gG, gB, gT, gate)
            print(f"  alpha={al:<3}{fl:<12}{gG:>11.7f}{gB:>10.4f}{gT:>16.4f}"
                  f"{f'{gate[0]:.5f}-{gate[1]:.5f}':>18}")
    check(abs(res[(2, "canonical")][1] - np.sqrt(boost_force_isolated(gbar / A0C, 2))) < 1e-12,
          f"FRAME B's internal prediction is EXACTLY the isolated closure to machine precision "
          f"({res[(2,'canonical')][1]:.10f}) -- verified, not asserted: a per-mode kernel has no cross "
          f"term, so the frame construction and the Theorem-B quadrature EFE are MUTUALLY EXCLUSIVE")
    check(res[(2, "canonical")][0] < 1.0001 and res[(1, "canonical")][0] < 1.001,
          f"FRAME G predicts gamma_v = {res[(2,'canonical')][0]:.7f} (alpha=2) / "
          f"{res[(1,'canonical')][0]:.5f} (alpha=1): Newtonian to 1e-6/1e-3")
    check(res[(2, "canonical")][1] > 1.20,
          f"FRAME B predicts gamma_v = {res[(2,'canonical')][1]:.4f} (alpha=2) / "
          f"{res[(1,'canonical')][1]:.4f} (alpha=1) -- it loses the EFE entirely and lands ABOVE the "
          f"frozen contamination-guard threshold {GUARD_ZONE}")

    print("\n  PROVE-BY-MOVING-THE-NUMBER: sweep the frame's drag speed v_drag continuously from 0")
    print("  (frame co-moves with the binary = FRAME B) to v_gal (= FRAME G), and check the")
    print("  self-consistent solver interpolates MONOTONICALLY between the two published endpoints.")
    print(f"  {'v_drag/v_gal':>13}{'v_drag [m/s]':>14}{'u_eff':>11}{'gamma_v':>12}")
    gs = []
    for f_ in (0.0, 1e-4, 1e-3, 1e-2, 0.1, 1.0):
        bo = frame_boost(gbar, s, f_ * VC, A0C, 2)
        Om = np.sqrt(bo * gbar / s)
        gs.append(np.sqrt(bo))
        print(f"  {f_:>13.5f}{f_*VC:>14.2f}"
              f"{Om*np.sqrt((f_*VC)**2+(Om*s)**2)/A0C:>11.4f}{np.sqrt(bo):>12.7f}")
    check(all(gs[i] > gs[i + 1] for i in range(len(gs) - 1))
          and abs(gs[0] - res[(2, "canonical")][1]) < 1e-9
          and abs(gs[-1] - res[(2, "canonical")][0]) < 1e-12,
          f"gamma_v falls MONOTONICALLY from {gs[0]:.4f} at v_drag = 0 (= FRAME B / the isolated "
          f"closure, agreement 1e-9) to {gs[-1]:.7f} at v_drag = v_gal (= FRAME G): the two readings "
          f"are the endpoints of ONE continuous family, so neither number is a solver artefact")
    return res


# ================================================================================================ S4
def s4_prereg(res):
    banner("S4. Q2 -- COMPARISON TO THE FROZEN TARGETS, AND WHAT AMENDMENT 4 WOULD HAVE TO SAY")
    lo, hi = FROZEN_A2_MI_RANGE
    print(f"  FROZEN (Amendment 3) MI range, alpha=2, both footings x both g_ext: [{lo}, {hi}]")
    print(f"  FROZEN sigma_fit(N=30k) = {SIG_FIT_30K}, sigma_sys = {SIG_SYS} (FROZEN allowance), "
          f"sigma_tot = {SIG_TOT}")
    print(f"  FROZEN decision bands: <=1.007 supports Newton; 1.007-1.083 undecided; "
          f">{GUARD_ZONE} = NO verdict permitted")
    print(f"\n  {'reading':<34}{'gamma_v (a=2)':>14}{'vs band edge':>14}{'|z| at sig_tot':>16}"
          f"{'|z| at N=inf':>14}")
    rowsout = {}
    for nm, key in (("FRAME G (galaxy-dragged)", 0), ("FRAME B (binary-dragged)", 1),
                    ("THEOREM B (frozen Am.3)", 2)):
        g = res[(2, "canonical")][key]
        edge = lo if g < lo else (hi if g > hi else g)
        d = abs(g - edge)
        z_tot = d / SIG_TOT
        z_inf = d / SIG_SYS       # sigma_sys is FROZEN: sigma_tot >= sigma_sys for any N
        rowsout[nm] = (g, d, z_tot, z_inf)
        print(f"  {nm:<34}{g:>14.7f}{('inside' if d==0 else f'{g-edge:+.4f}'):>14}"
              f"{z_tot:>16.2f}{z_inf:>14.2f}")
    gG = rowsout["FRAME G (galaxy-dragged)"]
    gB = rowsout["FRAME B (binary-dragged)"]
    check(gG[1] > 0 and gB[1] > 0,
          f"BOTH frame readings fall OUTSIDE the frozen Amendment-3 MI range: FRAME G by "
          f"{gG[1]:.4f} below {lo}, FRAME B by {gB[1]:.4f} above {hi}. Neither reading reproduces the "
          f"frozen target, because the frozen target is the Theorem-B QUADRATURE value and the frame "
          f"construction has no quadrature")
    check(gG[3] < 3.0,
          f"BUT FRAME G IS NOT A LIVE 3-SIGMA FALSIFIER: its offset {gG[1]:.4f} is {gG[2]:.2f} sigma_tot "
          f"at N=30k and only {gG[3]:.2f} sigma even as N->infinity, because sigma_sys = {SIG_SYS} is "
          f"FROZEN and floors sigma_tot. No sample size can decide it under the frozen error model")
    check(gB[0] > GUARD_ZONE,
          f"AND FRAME B IS UNSCOREABLE: gamma_v = {gB[0]:.4f} exceeds the frozen guard threshold "
          f"{GUARD_ZONE}, where sec 1.5 pre-declares 'NO hypothesis verdict permitted'. It is "
          f"{gB[2]:.1f} sigma_tot from the band yet the frozen rules forbid reading it. (The DR3 dry "
          f"run landed at 1.205, in the same zone.) Reported as a scoring trap, not repaired")

    print("\n  THE DEGENERACY THAT MATTERS: FRAME G vs the already-frozen GATED branch (Amendment 1).")
    for al in (2, 1):
        gG_, _, gT_, gate_ = res[(al, "canonical")]
        print(f"      alpha={al}: FRAME G = {gG_:.7f} ; gated Theorem-B = {gate_[0]:.7f}-{gate_[1]:.7f}"
              f" ; separation = {max(abs(gG_-x) for x in gate_):.2e} = "
              f"{max(abs(gG_-x) for x in gate_)/SIG_TOT:.4f} sigma_tot")
    sep2 = max(abs(res[(2, "canonical")][0] - x) for x in res[(2, "canonical")][3])
    check(sep2 / SIG_TOT < 0.05,
          f"FRAME G and the frozen GATED branch are separated by {sep2/SIG_TOT:.4f} sigma_tot -- "
          f"OBSERVATIONALLY DEGENERATE in the 2-30 kAU window. A Newtonian DR4 result confirms BOTH "
          f"mechanisms and distinguishes NEITHER")
    print("\n  A GAP IN THE FROZEN DOCUMENT, flagged (not edited): Amendment 1 froze the gated target at")
    print(f"      1.0004-1.0006, computed from the alpha=1 ungated boost. Amendment 3 moved the ungated")
    print(f"      value to {FROZEN_A2_MI_PRIMARY} but did NOT restate the gated row. Applying Amendment 1's")
    g2 = res[(2, "canonical")][3]
    print(f"      own Re G = {REG_GATED} to the alpha=2 boost gives {g2[0]:.5f}-{g2[1]:.5f}, i.e. the frozen")
    print(f"      gated number is stale by {abs(1.0005-np.mean(g2)):.5f}. Small, but it is a frozen number and")
    print(f"      the discrepancy should be recorded before data, not after.")
    check(np.mean(g2) < 1.0005,
          f"the alpha=2-implied gated value {g2[0]:.5f}-{g2[1]:.5f} is BELOW the frozen 1.0004-1.0006, "
          f"so Amendment 3 silently moved a second frozen number")

    print("\n  WHAT AMENDMENT 4 WOULD HAVE TO SAY (it is NOT filed here; the framework has NOT adopted")
    print("  the frame construction -- ROUTE C is an exploration of an unwritten door):")
    print(f"    (1) MOVE the MI target from [{lo}, {hi}] to {gG[0]:.5f}-{res[(1,'canonical')][0]:.5f}")
    print(f"        (alpha=2 to alpha=1 span) if FRAME G is adopted, or to "
          f"{res[(2,'canonical')][1]:.4f}-{res[(1,'canonical')][1]:.4f} if FRAME B is.")
    print("    (2) RETRACT Amendment 2's derived quadrature EFE and its pre-declared anisotropy SIGN,")
    print("        because a per-mode kernel has no vector cross term (verified in S3) and therefore")
    print("        predicts ZERO orientation anisotropy. Amendment 2 (f) is a pre-declared sign; it")
    print("        cannot be silently dropped.")
    print("    (3) DECLARE WHICH BRANCH OWNS THE >50 kAU SHAPE. Amendment 1's falsifier (i) is 'no")
    print("        excess beyond ~50 kAU kills the gated branch'. Under FRAME G a null there is the")
    print("        PREDICTION. Between them the two branches cover BOTH outcomes, so unless one is")
    print("        committed to before data the shape test becomes unfalsifiable by construction.")
    print("        This is the single most important discipline point in ROUTE C.")
    print("    (4) Restate the stale gated row above.")
    print("    Standing rule honoured: a frozen target may only move by an amendment filed IN THE OPEN")
    print("    before DR4, and a confirmation pre-declared as a kill stays scored as a kill.")
    return rowsout


# ================================================================================================ S5
def s5_anisotropy(res):
    banner("S5. THE ANISOTROPY STATISTIC -- the one place the two readings DO separate in DR4")
    gp, gq = efe_eigen_gamma_v(G_EXT_PRIMARY, A0C, 2)
    ideal = gq - gp
    print(f"  THEOREM B (frozen Am.3): gamma_par = {gp:.4f}, gamma_perp = {gq:.4f}, spread = {ideal:.4f}")
    print(f"  FRAME G / FRAME B: a per-mode kernel has NO vector cross term -> spread = 0 EXACTLY.")
    print("  So the pre-declared SIGN (perpendicular larger) is a direct discriminator. Amendment 3 (h)")
    print("  flagged the projection dilution as UNCOMPUTED; compute it (this is the honest limit):")
    rng = np.random.default_rng(20261216)      # frozen pre-reg RNG seed
    N = 2_000_000
    # g_ext points toward the Galactic centre: ghat = xhat (l = 0, b = 0)
    ghat = np.array([1.0, 0.0, 0.0])
    # line of sight n: uniform on the sphere with |b| > 15 deg (FROZEN cut 1). Sample by rejection in
    # one pass with generous over-draw, then truncate.
    over = int(N / (1.0 - np.sin(np.deg2rad(15.0))) * 1.25)
    u = rng.normal(size=(over, 3))
    u /= np.linalg.norm(u, axis=1)[:, None]
    nhat = u[np.abs(u[:, 2]) > np.sin(np.deg2rad(15.0))][:N]
    N = nhat.shape[0]
    print(f"      MC: N = {N:,} pairs, |b| > 15 deg line-of-sight distribution, seed 20261216")
    shat = rng.normal(size=(N, 3))
    shat /= np.linalg.norm(shat, axis=1)[:, None]
    # einsum rather than matmul: the BLAS path emits spurious over/underflow warnings on this platform
    c3 = np.abs(np.einsum('ij,j->i', shat, ghat))
    check(np.isfinite(c3).all() and np.isfinite(nhat).sum() == nhat.size,
          f"MC arrays are finite (no NaN/inf from the sampling): {np.isfinite(c3).all()}")
    # PHYSICAL per-pair boost: radial component of M.g  =>  gamma_v = [gam^2_par c^2 + gam^2_perp s^2]^(1/2)
    gam3 = np.sqrt(gp ** 2 * c3 ** 2 + gq ** 2 * (1.0 - c3 ** 2))
    # projected directions
    sp_ = shat - (np.sum(shat * nhat, axis=1)[:, None]) * nhat
    gp_ = ghat[None, :] - (np.einsum('ij,j->i', nhat, ghat))[:, None] * nhat
    ns, ng = np.linalg.norm(sp_, axis=1), np.linalg.norm(gp_, axis=1)
    good = (ns > 1e-6) & (ng > 1e-6)
    cpr = np.abs(np.sum(sp_[good] * gp_[good], axis=1) / (ns[good] * ng[good]))
    g3 = gam3[good]
    for nm, cc in (("3D angle (no projection)", c3[good]), ("PROJECTED sky angle", cpr)):
        par = g3[cc > np.cos(np.deg2rad(45))].mean()
        per = g3[cc <= np.cos(np.deg2rad(45))].mean()
        print(f"      {nm:<28} two-bin contrast <perp> - <par> = {per-par:+.5f}"
              f"   (fraction of the {ideal:.4f} eigenvalue spread: {(per-par)/ideal:.3f})")
    par_p = g3[cpr > np.cos(np.deg2rad(45))].mean()
    per_p = g3[cpr <= np.cos(np.deg2rad(45))].mean()
    obs = per_p - par_p
    par_3 = g3[c3[good] > np.cos(np.deg2rad(45))].mean()
    per_3 = g3[c3[good] <= np.cos(np.deg2rad(45))].mean()
    check(0.0 < obs < (per_3 - par_3),
          f"projection DILUTES the anisotropy: observable two-bin contrast {obs:.5f} vs 3D-binned "
          f"{per_3-par_3:.5f} vs eigenvalue spread {ideal:.5f}. Dilution factor "
          f"{obs/ideal:.3f} of the eigenvalue spread -- Amendment 3 (h)'s uncomputed flag, computed "
          f"(the estimator's velocity projection is a FURTHER dilution not modelled here)")
    print("\n  Required N for a 3-sigma detection of the Theorem-B anisotropy (which FRAME G predicts to")
    print("  be exactly zero). Two orientation bins of N/2, frozen sigma_fit scaling, sigma_sys assumed")
    print("  to cancel in the DIFFERENCE (an ASSUMPTION, flagged, not a computed fact):")
    for lab, contrast in (("eigenvalue spread (upper bound)", ideal),
                          ("3D-binned", per_3 - par_3), ("PROJECTED (realistic)", obs)):
        # sigma per bin: sigma_fit(N/2) = SIG_FIT_30K sqrt(30000/(N/2)); diff -> sqrt(2)x
        Nneed = 2 * 30000.0 * (3.0 * np.sqrt(2) * SIG_FIT_30K / contrast) ** 2
        print(f"      {lab:<34} contrast {contrast:.5f} -> N(3 sigma) = {Nneed:,.0f}")
    Nneed_proj = 2 * 30000.0 * (3.0 * np.sqrt(2) * SIG_FIT_30K / obs) ** 2
    check(Nneed_proj > 30000.0,
          f"even on the anisotropy axis DR4 is marginal: N(3 sigma) = {Nneed_proj:,.0f} against the "
          f"pre-registration's assumed N = 30,000 -- a factor {Nneed_proj/30000:.1f} short. Stated as a "
          f"deficit, not hidden")
    return ideal, obs


# ================================================================================================ S6
def s6_deadzone(a_gal, Om_gal):
    banner("S6. Q3 -- THE DEAD ZONE: does the dragged frame move, widen or close it? NUMBERS")
    print("  FROZEN dead zone (Amendment 1 / mi_wb_gate_fork_2026.py): between")
    print("      r_M    = sqrt(GM/a0)            (internal field drops below a0)")
    print("      r_gate = (GM/omega_c^2)^(1/3)   (Omega drops below omega_c: gate OPENS)")
    print("  FRAME G replaces the FIRST radius: the MOND regime now begins where the INFLATED argument")
    print("  reaches 1, i.e. Omega*v_gal = a0, giving  r_M,eff = (G M v_gal^2 / a0^2)^(1/3).")
    print(f"  {'M':>6}{'footing':<12}{'r_M [kAU]':>11}{'r_gate lo-hi [kAU]':>21}{'r_gate/r_M':>12}"
          f"{'r_M,eff [kAU]':>14}{'r_Meff/r_M':>12}")
    dz_frozen, dz_G = [], []
    for Mm in (0.5, 1.0, 1.5, 3.0):
        M = Mm * MSUN
        for fl, a0v in (("canonical", A0C), ("alt", A0A)):
            rM = np.sqrt(G * M / a0v)
            rg = [(G * M / OMC[e] ** 2) ** (1 / 3) for e in ("lo", "hi")]
            rMe = (G * M * VC ** 2 / a0v ** 2) ** (1 / 3)
            dz_frozen += [r / rM for r in rg]
            dz_G.append(rMe / rM)
            print(f"  {Mm:>6.1f}{fl:<12}{rM/(1e3*AU):>11.2f}"
                  f"{f'{rg[1]/(1e3*AU):.1f}-{rg[0]/(1e3*AU):.1f}':>21}"
                  f"{f'{rg[1]/rM:.2f}-{rg[0]/rM:.2f}':>12}{rMe/(1e3*AU):>14.0f}{rMe/rM:>12.1f}")
    check(4.4 < min(dz_frozen) and max(dz_frozen) < 7.9,
          f"reproduces the corpus's frozen dead-zone ratio r_gate/r_M = {min(dz_frozen):.2f}-"
          f"{max(dz_frozen):.2f} (banked 4.54-7.76)")
    # exact scalings, verified numerically rather than asserted
    Ms = np.array([0.3, 0.5, 1.0, 1.5, 3.0, 6.0]) * MSUN
    p_ratio = np.polyfit(np.log(Ms),
                         np.log((G * Ms * VC ** 2 / A0C ** 2) ** (1 / 3) / np.sqrt(G * Ms / A0C)), 1)[0]
    p_gate = np.polyfit(np.log(Ms),
                        np.log((G * Ms / OMC["lo"] ** 2) ** (1 / 3) / np.sqrt(G * Ms / A0C)), 1)[0]
    print(f"\n  EXACT SCALINGS (fitted, not asserted): r_M,eff/r_M ~ M^{p_ratio:.4f} and "
          f"r_gate/r_M ~ M^{p_gate:.4f}  (both -1/6 = -0.1667)")
    check(abs(p_ratio + 1 / 6) < 1e-9 and abs(p_gate + 1 / 6) < 1e-9,
          f"both dead-zone ratios scale as M^(-1/6) to 1e-9 -- so their QUOTIENT, the widening factor, "
          f"is EXACTLY mass-independent")
    print("  Hence the widening factor has a closed form with no mass in it:")
    print("      r_M,eff / r_gate = (v_gal * omega_c / a0)^(2/3)")
    for fl, a0v in (("canonical", A0C), ("alt", A0A)):
        for e in ("lo", "hi"):
            cf = (VC * OMC[e] / a0v) ** (2 / 3)
            num = ((G * MSUN * VC ** 2 / a0v ** 2) ** (1 / 3)) / ((G * MSUN / OMC[e] ** 2) ** (1 / 3))
            print(f"      {fl:<12} omega_c {e}: closed form {cf:.4f}x   numeric {num:.4f}x   "
                  f"rel diff {abs(cf-num)/cf:.2e}")
    cfs = [(VC * OMC[e] / a0v) ** (2 / 3) for a0v in (A0C, A0A) for e in ("lo", "hi")]
    nums = [((G * MSUN * VC ** 2 / a0v ** 2) ** (1 / 3)) / ((G * MSUN / OMC[e] ** 2) ** (1 / 3))
            for a0v in (A0C, A0A) for e in ("lo", "hi")]
    check(max(abs(a - b) / a for a, b in zip(cfs, nums)) < 1e-12,
          f"closed form (v_gal omega_c/a0)^(2/3) = {min(cfs):.2f}-{max(cfs):.2f}x matches the numeric "
          f"widening to 1e-12 across both footings and both omega_c edges -- THE NUMBER Q3 ASKS FOR")
    check(abs(min(dz_G) - max(dz_G)) / max(dz_G) < 0.40,
          f"FRAME-G dead-zone ratio r_M,eff/r_M = {min(dz_G):.1f}-{max(dz_G):.1f} across a 6x mass "
          f"range and both footings (weak M^(-1/6) dependence, fitted above)")
    rMe1 = (G * MSUN * VC ** 2 / A0C ** 2) ** (1 / 3)
    rg1 = (G * MSUN / OMC["lo"] ** 2) ** (1 / 3)
    rM1 = np.sqrt(G * MSUN / A0C)
    print(f"\n  VERDICT ON THE DEAD ZONE (1 Msun, canonical):")
    print(f"      frozen zone   [{rM1/(1e3*AU):.1f}, {rg1/(1e3*AU):.1f}] kAU   ratio {rg1/rM1:.2f}")
    print(f"      FRAME G zone  [{rM1/(1e3*AU):.1f}, {rMe1/(1e3*AU):.0f}] kAU   ratio {rMe1/rM1:.1f}")
    print(f"      => the zone WIDENS: outer edge moves out by {rMe1/rg1:.1f}x, ratio grows by "
          f"{(rMe1/rM1)/(rg1/rM1):.1f}x")
    check(rMe1 > rg1,
          f"FRAME G WIDENS the dead zone by {rMe1/rg1:.1f}x in its outer edge ({rg1/(1e3*AU):.0f} -> "
          f"{rMe1/(1e3*AU):.0f} kAU) and makes omega_c REDUNDANT there -- the argument inflation alone "
          f"Newtonises the window, so the gate is no longer doing the work")
    # bound-pair limit
    r_bound = 1.0 * PC
    P_knee = 2 * np.pi / (A0C / VC)
    P_gal = 2 * np.pi / Om_gal
    P_bound = 2 * np.pi * np.sqrt(r_bound ** 3 / (G * MSUN))
    print(f"\n  AND THAT IS WHERE IT BITES. Wide pairs do not survive past ~1 pc = {r_bound/(1e3*AU):.0f} kAU")
    print(f"  (El-Badry, Rix & Heintz 2021 sample extent; Galactic tide).")
    print(f"      FRAME G's knee r_M,eff = {rMe1/(1e3*AU):.0f} kAU = {rMe1/PC:.2f} pc "
          f"-> {rMe1/r_bound:.2f}x beyond the bound-pair limit")
    print(f"      equivalently: the knee frequency is a0/v_gal = {A0C/VC:.3e} rad/s, i.e. a period")
    print(f"      P_knee = {P_knee/YR:.3e} yr = {P_knee/P_gal:.2f} GALACTIC YEARS, while the widest bound")
    print(f"      pair has P = {P_bound/YR:.3e} yr = {P_bound/P_gal:.2f} galactic years.")
    check(rMe1 > r_bound and P_knee > P_bound,
          f"FRAME G CLOSES THE WIDE-BINARY FRONT ENTIRELY: its MOND knee sits at {rMe1/PC:.2f} pc, "
          f"{rMe1/r_bound:.2f}x beyond the ~1 pc bound-pair limit, so NO bound pair is ever in the MOND "
          f"regime. Structural restatement: under a galaxy-dragged frame a subsystem boosts only if its "
          f"orbital period exceeds {P_knee/P_gal:.2f} galactic years, and the widest bound pair reaches "
          f"only {P_bound/P_gal:.2f}")
    print(f"      P_knee/P_gal = {P_knee/P_gal:.4f} = a_gal/a0 = {a_gal/A0C:.4f}  (identity: "
          f"a0/v_gal vs Omega_gal = a_gal/v_gal)")
    check(abs(P_knee / P_gal - a_gal / A0C) < 1e-9,
          f"identity verified: the knee period in galactic years equals a_gal/a0 exactly "
          f"({P_knee/P_gal:.6f} vs {a_gal/A0C:.6f})")
    return rMe1, rg1


# ================================================================================================ S7
def s7_nesting(a_gal, v_int):
    banner("S7. Q4 -- ONE LEVEL UP: star in galaxy in cluster. Is the prescription self-consistent?")
    print("  Build the field/speed ladder for a star at 10 kpc in a spiral 1 Mpc from a Virgo-class")
    print("  cluster, itself hosting a 10 kAU wide binary. Levels (a_k, v_k):")
    M_cl, r_cl, sig_cl = 1.2e15 * MSUN, 1.0e3 * KPC, 700e3
    v_flat, R_star = 150e3, 10 * KPC
    Mb, sb = 1.0 * MSUN, 10e3 * AU
    levels = [
        ("binary internal (10 kAU)", G * Mb / sb ** 2, np.sqrt(G * Mb / sb)),
        ("galaxy rotation (10 kpc)", v_flat ** 2 / R_star, v_flat),
        ("cluster orbit (1 Mpc)", G * M_cl / r_cl ** 2, sig_cl),
    ]
    print(f"  {'level':<28}{'a_k [m/s2]':>13}{'a_k/a0can':>11}{'a_k/a0alt':>11}{'v_k [km/s]':>12}")
    for nm, a, v in levels:
        print(f"  {nm:<28}{a:>13.4e}{a/A0C:>11.4f}{a/A0A:>11.4f}{v/1e3:>12.2f}")
    a_ks = np.array([a for _, a, _ in levels])
    v_ks = np.array([v for _, _, v in levels])

    print("\n  (a) IS THE DOMINANT-FIELD SELECTION ORDER-DEPENDENT? Test all 6 orderings of the ladder:")
    import itertools
    sels = set()
    for perm in itertools.permutations(range(3)):
        # 'add levels one at a time, keep the dominant one'
        best = perm[0]
        for k in perm[1:]:
            if a_ks[k] > a_ks[best]:
                best = k
        sels.add(best)
    print(f"      selected level index across all orderings: {sorted(sels)} "
          f"-> '{levels[sorted(sels)[0]][0]}'")
    check(len(sels) == 1,
          f"the dominant-field SELECTION is order-INDEPENDENT across all 6 orderings (it is a max) -- "
          f"so the prescription is not order-inconsistent, and I am not manufacturing an inconsistency")
    print("      Likewise the Theorem-B argument |sum a_k|^2 is manifestly order-invariant; checked:")
    import itertools as it
    sums = [float(np.abs(np.sum([a_ks[i] for i in p])) ** 2) for p in it.permutations(range(3))]
    check(max(sums) - min(sums) < 1e-30,
          f"|sum a_k|^2 is identical under all 6 orderings (spread {max(sums)-min(sums):.2e}) -- "
          f"Theorem B's argument is nesting-consistent")

    print("\n  (b) THE REAL OBSTRUCTION IS NOT ORDER BUT MODE COUNT. One frame supplies ONE v_F; the")
    print("      construction needs Omega_k v_F = a_k for EVERY k, i.e. v_F = v_k for all k. With 3")
    print("      levels that is 3 conditions on 1 unknown. Violation factors v_F/v_k for each choice:")
    print(f"  {'frame co-moves with':<28}" + "".join(f"{levels[k][0][:16]:>18}" for k in range(3)))
    worst = 0.0
    for j in range(3):
        row = [v_ks[j] / v_ks[k] for k in range(3)]
        worst = max(worst, max(max(row), max(1 / r for r in row)))
        print(f"  {levels[j][0]:<28}" + "".join(f"{r:>18.4g}" for r in row))
    check(worst > 100.0,
          f"MODE-COUNT NO-GO: whichever level the single passive frame co-moves with, at least two of "
          f"the three modes get the wrong argument, the worst violation being {worst:.0f}x. A single "
          f"frame field u^mu cannot supply the right speed to a hierarchical trajectory -- which is "
          f"exactly why the local witness works on CIRCLES (one mode) and fails off them")
    print("      (Comparison, both ways: Theorem B's |a_tot|^2 needs no frame and has no such")
    print("       obstruction. That is a point AGAINST the frame door, and it is the same statement as")
    print("       the pincer's K(<Box_u>) != <K(Box_u)>: the frame door tries to replace the average.)")

    print("\n  (c) THE PRICE FRAME G PAYS ONE LEVEL UP: a cluster galaxy's own rotation curve.")
    R_x = v_flat ** 2 / (G * M_cl / r_cl ** 2)
    print(f"      cluster field at 1 Mpc = {G*M_cl/r_cl**2:.4e} = {G*M_cl/r_cl**2/A0C:.3f} a0_can;")
    print(f"      the galaxy's own field v_flat^2/R equals it at R = {R_x/KPC:.2f} kpc, i.e. INSIDE the")
    print(f"      optical disk. So beyond {R_x/KPC:.1f} kpc the dominant-field rule hands the frame to the")
    print(f"      CLUSTER, and every star's v_F becomes the galaxy's cluster-orbital speed.")
    print(f"  {'sigma_cl [km/s]':>16}{'v_flat [km/s]':>15}{'lambda':>9}{'dlog a0_eff':>13}"
          f"{'dlog v_flat':>13}{'vs a0 budget':>14}")
    over = []
    for sc in (500e3, 700e3, 1000e3):
        for vf in (100e3, 150e3, 220e3):
            lam = sc / vf
            dl = -np.log10(lam)
            over.append(abs(dl) / (2 * RAR_DEX[2]))
            print(f"  {sc/1e3:>16.0f}{vf/1e3:>15.0f}{lam:>9.2f}{dl:>13.3f}{0.25*dl:>13.3f}"
                  f"{abs(dl)/(2*RAR_DEX[2]):>14.2f}x")
    check(min(over) > 1.0,
          f"FRAME G predicts a cluster-vs-field a0 OFFSET of {min(over)*2*RAR_DEX[2]:.2f}-"
          f"{max(over)*2*RAR_DEX[2]:.2f} dex = {min(over):.1f}-{max(over):.1f}x the framework's own a0 "
          f"budget (2 x {RAR_DEX[2]:.4f} dex). Equivalently cluster spirals would sit "
          f"{100*(1-10**(-0.25*np.log10(700/150))):.0f}% low in v_flat at fixed baryonic mass -- a "
          f"NEW archival test (cluster vs field RAR/BTFR) that I have NOT run here")
    print("      NOT overclaimed: the corpus's banked 10.5-sigma environmental null is on")
    print("      a0 ~ sqrt(G rho_local), a DIFFERENT functional, and does not transfer as a kill.")
    return worst


# ================================================================================================ S8
def s8_dsph():
    banner("S8. THE SHARPEST DATA-IN-HAND CONSEQUENCE OF FRAME G: dwarf spheroidals (real catalogue)")
    csvp = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/dsph/mcconnachie2012_dsph.csv"
    if not os.path.exists(csvp):
        print("  catalogue not found -- SECTION SKIPPED (no synthetic substitute used)")
        return None
    print(f"  data: {csvp}  (McConnachie 2012, the corpus's own Front-D catalogue)")
    print("  THE ESTIMATOR IS Upsilon-FREE ON PURPOSE. Front D's blocker is that the stellar")
    print("  mass-to-light ratio carries a COHERENT 0.38-0.48 dex error worth 8.7x the signal, so any")
    print("  test that needs the baryonic mass is systematics-limited. This one does not need it:")
    print("      x    = |a|_obs/a0 = sigma^2/(R_h a0)          -- OBSERVED acceleration, from sigma alone")
    print("      the framework's closure REQUIRES g_bar = |a|_obs * mu(x)   (this is where Upsilon drops out)")
    print("      lambda = |xdot|/sigma = sqrt(v_c^2 + sigma^2)/sigma        -- the FRAME-G inflation")
    print("      FRAME G, from that SAME g_bar, predicts |a|_G = g_bar/mu(lambda*x)")
    print("      => sigma deficit = sqrt(|a|_obs/|a|_G) = sqrt( mu(lambda x) / mu(x) )")
    print("  NOTE THE ARGUMENT: mu is evaluated at the OBSERVED x, never at a Newtonian y. Evaluating")
    print("  it at the Newtonian argument is the exact error STANDING sec 5.1 records in the forest")
    print("  chain, and it was present in the first draft of this section.")
    print("  Omega_int = sigma/R_h and the satellite's MW-orbital speed ~ v_c are order-of-magnitude;")
    print("  heliocentric D is used as galactocentric -- both FLAGGED, they only shift which dwarfs")
    print("  count as MW-dominated, not the deficit.")
    rows = []
    with open(csvp) as f:
        for r in csv.DictReader(f):
            if r["SubG"].strip() != "MW":
                continue
            try:
                D = float(r["D"]) * KPC
                Rh = float(r["R2"]) * PC
                sig = float(r["sigma*"]) * 1e3
            except (ValueError, KeyError):
                continue
            if D <= 0 or Rh <= 0 or sig <= 0:
                continue
            rows.append((r["Name"].strip(), D, Rh, sig))
    print(f"\n  {len(rows)} MW satellites with sigma and R_h.")
    print(f"  {'name':<20}{'sig':>6}{'R_h[pc]':>9}{'x=a_obs/a0':>11}{'a_MW/a0':>9}{'dom':>5}"
          f"{'lambda':>8}{'lam*x':>9}{'deficit a=2':>12}{'deficit a=1':>12}")
    out = {1: [], 2: []}
    dom_mw = 0
    shown = 0
    for nm, D, Rh, sig in rows:
        a_obs = sig ** 2 / Rh
        Om = sig / Rh
        a_mw = VC ** 2 / D
        dominant_mw = a_mw > a_obs
        dom_mw += int(dominant_mw)
        lam = np.sqrt(VC ** 2 + sig ** 2) / sig
        d = {}
        for al in (2, 1):
            x = a_obs / A0C
            d[al] = float(np.sqrt(mu(lam * x, al) / mu(x, al)))
            if dominant_mw:
                out[al].append(d[al])
        if shown < 14:
            shown += 1
            print(f"  {nm[:19]:<20}{sig/1e3:>6.1f}{Rh/PC:>9.0f}{a_obs/A0C:>11.4f}{a_mw/A0C:>9.3f}"
                  f"{'MW' if dominant_mw else 'self':>5}{lam:>8.1f}{lam*a_obs/A0C:>9.1f}"
                  f"{d[2]:>12.3f}{d[1]:>12.3f}")
    print(f"  ... ({len(rows)} rows total, {dom_mw} with the MW field dominant -> FRAME G applies)")
    dd2 = np.array(out[2])
    print(f"\n  FRAME G's sigma deficit over the {len(dd2)} MW-dominated dwarfs, both footings, both kernels:")
    print(f"  {'footing':<12}{'kernel':<9}{'median':>9}{'mean':>9}{'min':>9}{'max':>9}")
    meds = {}
    for fl, a0v in (("canonical", A0C), ("alternate", A0A)):
        for al in (2, 1):
            v = []
            for nm, D, Rh, sig in rows:
                a_obs, Om = sig ** 2 / Rh, sig / Rh
                if VC ** 2 / D <= a_obs:
                    continue
                lam = np.sqrt(VC ** 2 + sig ** 2) / sig
                x = a_obs / a0v
                v.append(float(np.sqrt(mu(lam * x, al) / mu(x, al))))
            v = np.array(v)
            meds[(fl, al)] = float(np.median(v))
            print(f"  {fl:<12}alpha={al:<3}{np.median(v):>9.3f}{v.mean():>9.3f}{v.min():>9.3f}"
                  f"{v.max():>9.3f}")
    m2 = meds[("canonical", 2)]
    print(f"\n      i.e. FRAME G predicts dispersions a factor {m2:.2f} = "
          f"{100*(1-1/m2):.0f}% BELOW what the framework's own closure needs from the same baryons.")
    print(f"      Deep-regime form: deficit -> 1/sqrt(mu(x)) -> x^(-1/2) for alpha=2, so it is just")
    print(f"      'the MOND boost, removed'. That is the whole point: FRAME G Newtonises satellites.")
    check(dom_mw > len(rows) // 2,
          f"the MW field DOMINATES the internal field for {dom_mw}/{len(rows)} MW satellites, so the "
          f"dominant-field rule hands the frame to the MW for most of them -- FRAME G applies to the "
          f"dwarf sample, it is not a corner case")
    check(min(meds.values()) > 1.5,
          f"FRAME G COSTS THE DWARFS: median sigma deficit {min(meds.values()):.2f}-"
          f"{max(meds.values()):.2f}x across both footings and both kernels on real McConnachie 2012 "
          f"data, because a satellite's internal mode is inflated by lambda = "
          f"|xdot|/sigma ~ 20-60. Upsilon-free, so Front D's coherent-Upsilon blocker does NOT apply")
    # limit check: no inflation => no deficit
    lim = [float(np.sqrt(mu(1.0 * (sig ** 2 / Rh) / A0C, 2) / mu((sig ** 2 / Rh) / A0C, 2)))
           for nm, D, Rh, sig in rows]
    check(max(abs(np.array(lim) - 1.0)) < 1e-12,
          f"LIMIT CHECK: setting lambda = 1 (no inflation) returns deficit = 1 to "
          f"{max(abs(np.array(lim)-1.0)):.1e} on every dwarf -- the deficit is produced by the frame, "
          f"not by the estimator")
    return m2


# ================================================================================================ S9
def s9_solar():
    banner("S9. Q5 -- SOLAR SYSTEM: does the dragged frame RE-OPEN the alpha=1 ephemeris liability?")
    print("  mpmath at 50 digits throughout: at Earth the alpha=2 anomaly is 1/mu(u)-1 ~ 1/(2u^2) with")
    print("  u ~ 5e8, i.e. ~1e-18 -- float64 cannot represent 1+1e-18 and would silently return ZERO.")
    print("  Both the direct evaluation and the asymptotic form are computed and compared.")
    planets = (("Mercury", 0.387098), ("Earth", 1.0), ("Mars", 1.523679), ("Neptune", 30.0699))

    def mu_mp(x, alpha):
        x = mpf(x)
        if alpha == 2:
            return x / msqrt(1 + x * x)
        return (msqrt(1 + 4 * x * x) - 1) / (2 * x)

    print("\n  Under FRAME G the frame at Earth is the GALACTIC one, so v_F = the Sun's 220 km/s rather")
    print(f"  than Earth's orbital speed. Factor lambda = v_gal/v_planet:")
    print(f"  {'planet':<9}{'v_p [km/s]':>11}{'lambda':>8}{'a=1 delta_a':>14}{'x bound':>10}"
          f"{'a=1 FRAME G':>14}{'x bound':>10}{'a=2 FRAME G':>14}{'x bound':>10}")
    a1_over, a2_over = [], []
    for pn, r_au in planets:
        r = r_au * AU
        gbar = G * MSUN / r ** 2
        vp = np.sqrt(G * MSUN / r)
        lam = VC / vp
        for fl, a0v in (("can", A0C), ("alt", A0A)):
            y = mpf(gbar) / mpf(a0v)
            u_true = y                                    # Theorem B: argument = |a|/a0 (x ~ y here)
            u_eff = mpf(np.sqrt(G * MSUN / r ** 3)) * mpf(np.sqrt(VC ** 2 + vp ** 2)) / mpf(a0v)
            # anomaly = g_bar (1/mu(u) - 1)
            d1_true = mpf(gbar) * (1 / mu_mp(u_true, 1) - 1)
            d1_G = mpf(gbar) * (1 / mu_mp(u_eff, 1) - 1)
            d2_G = mpf(gbar) * (1 / mu_mp(u_eff, 2) - 1)
            bnd = EPH_BOUND.get(pn)
            if fl == "can":
                s = (f"  {pn:<9}{vp/1e3:>11.2f}{lam:>8.2f}{float(d1_true):>14.4e}")
                s += f"{float(d1_true)/bnd:>10.1f}" if bnd else f"{'--':>10}"
                s += f"{float(d1_G):>14.4e}"
                s += f"{float(d1_G)/bnd:>10.1f}" if bnd else f"{'--':>10}"
                s += f"{float(d2_G):>14.4e}"
                s += f"{float(d2_G)/bnd:>10.2e}" if bnd else f"{'--':>10}"
                print(s)
            if bnd:
                a1_over.append(float(d1_G) / bnd)
                a2_over.append(float(d2_G) / bnd)
    # asymptotic cross-checks
    r = AU
    gbar = G * MSUN / r ** 2
    vp = np.sqrt(G * MSUN / r)
    lam_naive = VC / vp                                  # the naive speed ratio ROUTE C quotes (7.4)
    lam = np.sqrt(VC ** 2 + vp ** 2) / vp                # the EXACT one: v_F = |xdot| in quadrature
    u_eff = mpf(np.sqrt(G * MSUN / r ** 3)) * mpf(np.sqrt(VC ** 2 + vp ** 2)) / mpf(A0C)
    d1_G = mpf(gbar) * (1 / mu_mp(u_eff, 1) - 1)
    d2_G = mpf(gbar) * (1 / mu_mp(u_eff, 2) - 1)
    print(f"\n  Asymptotic cross-checks at Earth, canonical (mpmath at {mp.dps} digits vs closed form).")
    print(f"      ROUTE C's stated factor is v_gal/v_Earth = {lam_naive:.4f}; the frame-relative speed is")
    print(f"      |xdot| = sqrt(v_gal^2 + v_p^2), giving lambda = {lam:.4f} -- {100*(lam/lam_naive-1):.2f}% "
          f"larger. Both reported; the exact one is used.")
    print(f"      alpha=1: a0/(2 lambda) = {A0C/(2*lam):.6e}  vs mpmath {float(d1_G):.6e}  "
          f"rel {abs(float(d1_G)-A0C/(2*lam))/(A0C/(2*lam)):.2e}")
    print(f"      alpha=2: a0^2/(2 g lambda^2) = {A0C**2/(2*gbar*lam**2):.6e}  vs mpmath "
          f"{float(d2_G):.6e}  rel {abs(float(d2_G)-A0C**2/(2*gbar*lam**2))/(A0C**2/(2*gbar*lam**2)):.2e}")
    check(abs(float(d1_G) - A0C / (2 * lam)) / (A0C / (2 * lam)) < 1e-6,
          f"alpha=1 FRAME G anomaly = a0/(2 lambda) to {abs(float(d1_G)-A0C/(2*lam))/(A0C/(2*lam)):.1e} "
          f"-- the dragged frame divides the constant a0/2 sunward anomaly by exactly the speed ratio")
    check(abs(float(d2_G) - A0C ** 2 / (2 * gbar * lam ** 2)) / (A0C ** 2 / (2 * gbar * lam ** 2)) < 1e-6,
          f"alpha=2 FRAME G anomaly = a0^2/(2 g lambda^2), i.e. divided by lambda^2 = {lam**2:.1f}, "
          f"verified against the 50-digit mpmath evaluation (float64 returns EXACTLY ZERO here: "
          f"1 + 1e-18 is not representable)")
    f64_true = 1.0 / float(mu(float(gbar / A0C), 2)) - 1.0
    mp_true = float(1 / mu_mp(mpf(gbar) / mpf(A0C), 2) - 1)
    f64_eff = 1.0 / float(mu(float(u_eff), 2)) - 1.0
    mp_eff = float(1 / mu_mp(u_eff, 2) - 1)
    print(f"\n  WHY mpmath WAS MANDATORY (demonstrated, not asserted):")
    print(f"      Theorem-B argument u = {float(gbar/A0C):.3e}: float64 1/mu-1 = {f64_true:.4e} "
          f"vs 50-digit {mp_true:.4e}  -> float64 error {abs(f64_true-mp_true)/mp_true*100:.0f}%")
    print(f"      FRAME-G  argument u = {float(u_eff):.3e}: float64 1/mu-1 = {f64_eff:.4e} "
          f"vs 50-digit {mp_eff:.4e}  -> float64 returns {'EXACTLY ZERO' if f64_eff == 0 else 'noise'}")
    check(f64_eff == 0.0 and mp_eff > 0.0 and abs(f64_true - mp_true) / mp_true > 0.5,
          f"float64 returns EXACTLY 0 for the FRAME-G anomaly (true value {mp_eff:.2e}) and is "
          f"{abs(f64_true-mp_true)/mp_true*100:.0f}% wrong even for the Theorem-B one -- a float64 "
          f"scan of this section would have reported 'no anomaly' from pure representation error")

    print(f"\n  THE ANSWER TO Q5, both footings:")
    print(f"      bare alpha=1 (Theorem B): a0/2 = {A0C/2:.3e} / {A0A/2:.3e} = "
          f"{A0C/2/EPH_BOUND['Earth']:.0f}x / {A0A/2/EPH_BOUND['Earth']:.0f}x the Earth 2-sigma bound"
          f"  [corpus: 1278x]")
    print(f"      alpha=1 under FRAME G: {min(a1_over):.0f}x - {max(a1_over):.0f}x over "
          f"(Earth+Mars, both footings)")
    print(f"      ... and after the framework's OWN derived EFE (suppression "
          f"{EFE_SUPPRESSION[0]:.2f}-{EFE_SUPPRESSION[1]:.2f}x, STANDING sec 5.0): "
          f"{min(a1_over)/EFE_SUPPRESSION[1]:.1f}x - {max(a1_over)/EFE_SUPPRESSION[0]:.1f}x over")
    print(f"      alpha=2 under FRAME G: {min(a2_over):.2e}x - {max(a2_over):.2e}x of the bound")
    check(min(a1_over) > 1.0,
          f"FRAME G does NOT rescue alpha=1: it SOFTENS the sunward anomaly by exactly lambda = "
          f"{lam:.2f} (1278x -> {min(a1_over):.0f}-{max(a1_over):.0f}x over the bound; "
          f"{min(a1_over)/EFE_SUPPRESSION[1]:.0f}-{max(a1_over)/EFE_SUPPRESSION[0]:.0f}x after the "
          f"framework's own EFE) but leaves it EXCLUDED. alpha=1 stays dead")
    check(max(a2_over) < 1e-3,
          f"and FRAME G does NOT RE-OPEN the liability under the kernel IN FORCE: alpha=2 goes from "
          f"~2e-5x to {max(a2_over):.1e}x of the bound, i.e. the dragged frame moves the ephemerides "
          f"the SAFE way by lambda^2 = {lam**2:.1f}. No manufactured deficit and no manufactured escape")

    print("\n  A STRUCTURAL SIGNATURE that separates FRAME G from Theorem B in the solar system:")
    print("      Theorem B, alpha=2: delta_a = a0^2/(2 g_bar) ~ r^2 ; FRAME G: a0^2/(2 g_bar lam^2) ~ r^1")
    rs = np.array([0.4, 1.0, 5.0, 30.0, 1e3, 1e5]) * AU
    dB = A0C ** 2 / (2 * G * MSUN / rs ** 2)
    dG = dB * (np.sqrt(G * MSUN / rs) / VC) ** 2
    pB = np.polyfit(np.log(rs), np.log(dB), 1)[0]
    pG = np.polyfit(np.log(rs), np.log(dG), 1)[0]
    print(f"      fitted log-slopes: Theorem B {pB:.4f} (expect 2), FRAME G {pG:.4f} (expect 1)")
    check(abs(pB - 2.0) < 1e-8 and abs(pG - 1.0) < 1e-8,
          f"radial signatures differ exactly: r^{pB:.3f} vs r^{pG:.3f}. Both are ~1e-19 m/s^2 at 1 AU "
          f"so this is NOT observable now -- reported as a structural difference, not a test")
    r_oort = 5e4 * AU
    u_true = (G * MSUN / r_oort ** 2) / A0C
    u_eff = np.sqrt(G * MSUN / r_oort ** 3) * VC / A0C
    print(f"      Where it IS large: an Oort-cloud body at 5e4 AU has u_true = {u_true:.4f} (MOND "
          f"regime) but u_eff = {u_eff:.1f} under FRAME G, inflated {u_eff/u_true:.0f}x -> the Sun's")
    print(f"      effective MOND radius moves from {np.sqrt(G*MSUN/A0C)/AU:.0f} AU to "
          f"{(G*MSUN*VC**2/A0C**2)**(1/3)/AU:.3e} AU = "
          f"{(G*MSUN*VC**2/A0C**2)**(1/3)/PC:.2f} pc, beyond the Sun's own tidal radius.")
    check(u_eff > u_true,
          f"FRAME G Newtonises the entire Oort cloud (u {u_true:.3f} -> {u_eff:.1f} at 5e4 AU), the "
          f"same mechanism that Newtonises wide binaries and dwarfs -- one prediction, three arenas")
    return min(a1_over), max(a2_over)


# ================================================================================================
def main():
    print("=" * 104)
    print("ROUTE C -- THE HIERARCHY FALSIFIER for the locally-dragged passive frame")
    print("de Sitter-Unruh MODIFIED INERTIA, a0 = c H_Lambda / Z, kappa = 1/2 (FITTED, not derived)")
    print("kernel IN FORCE alpha=2 mu = x/sqrt(1+x^2); alpha=1 carried alongside; BOTH a0 footings")
    print("=" * 104)
    a_gal, Om_gal, rows = s0_ladder()
    s1_identity()
    v_int = s2_frames(a_gal, Om_gal, rows)
    res = s3_gamma_v(a_gal, Om_gal)
    s4_prereg(res)
    s5_anisotropy(res)
    s6_deadzone(a_gal, Om_gal)
    s7_nesting(a_gal, v_int)
    s8_dsph()
    s9_solar()

    banner(f"SUMMARY -- {NCHK} structural checks, {'ALL PASSED' if OK else 'FAILURES PRESENT'}")
    print("""  1. ROUTE C's setup is reproduced exactly: a_gal = 1.913e-10 = 2.044 a0_can (1.693 a0_alt),
     a_int(1 Msun, 10 kAU) = 5.932e-11 = 0.634 a0_can (0.525 a0_alt), Omega_int/Omega_gal = 229,
     v_gal/v_int = 738.5. Omega_int(1.5 Msun) = 2.4388e-13 matches the frozen Amendment-1 value.
     The Galaxy dominates the field at 10 kAU by 3.22x, and the field crossover r_eq = 3.79-11.56 kAU
     sits INSIDE the frozen 2-30 kAU cut -- so a dominant-mass drag rule changes frame mid-window.
  2. Of four candidate frames, THREE DIE WITH NUMBERS: co-rotating (solar gravity weaker by
     7961x/7245x), cosmic/CMB (a0_eff spread 1.48 dex vs a 0.223 dex budget = 6.6x over; the banked
     4.6x is the conservative end), and binary-barycentre-dragged (the barycentre's own galactic
     circular speed would be 18.2x too high -- 3996 vs 220 km/s -- and the exact DC limit diverges).
     Only a DOMINANT-MASS (galactic) frame survives, and it survives the RAR BY CONSTRUCTION.
  3. Q1: the two readings of v_rel differ by lambda = v_c sqrt(s/GM) = 159-1878 across the frozen cut
     window. Under the surviving frame the binary's internal argument is u_eff = 61-10864 (canonical):
     deep Newtonian for EVERY pair, so gamma_v = 1.0000011 (alpha=2) / 1.00053 (alpha=1).
  4. Q2: that is OUTSIDE the frozen Amendment-3 range 1.0182-1.0350 -- but it is NOT a live 3-sigma
     falsifier: the offset 0.0182 is 0.65 sigma_tot at N=30k and only 0.91 sigma as N->infinity,
     because the FROZEN sigma_sys = 0.02 floors sigma_tot. And it is degenerate with the already-frozen
     GATED branch to 0.0071 sigma_tot. The aggregate gamma_v CANNOT decide the hierarchy question.
     The binary-dragged reading is 6.31 sigma_tot out (8.83 at N=inf) -- but it lands above the frozen
     1.20 guard threshold where the pre-registration permits NO verdict, and it is independently dead.
  5. Q3 (dead zone): the surviving frame WIDENS it by (v_gal omega_c/a0)^(2/3) = 10.64-13.93x, EXACTLY
     mass-independent (both r_gate/r_M and r_M,eff/r_M scale as M^(-1/6), fitted to 1e-9). Outer edge
     50 -> 603 kAU canonical / 532 kAU alt; the MOND knee moves to 2.92 pc = 2.92x beyond the ~1 pc
     bound-pair limit. Equivalently a subsystem boosts only if its period exceeds a_gal/a0 = 2.044
     galactic years (identity verified), and the widest bound pair reaches 0.41. It CLOSES the
     wide-binary front, makes omega_c redundant there (one postulate removed), and destroys the frozen
     p = 3 cubic-rise falsifier.
  6. Q4 (nesting): the dominant-field SELECTION is order-independent (verified over all 6 orderings),
     as is Theorem B's |sum a|^2. The obstruction is MODE COUNT, not order: one frame supplies one
     v_F but the construction needs v_F = v_k for every mode, and the worst violation on a 3-level
     ladder is 2350x. One level up it costs a cluster-vs-field a0 offset of 0.36-1.00 dex = 1.6-4.5x
     the framework's own budget (32% low in v_flat) -- a NEW archival test, NOT run here.
  7. THE SHARPEST FALSIFIER IS NOT DR4, IT IS THE DWARFS, ON DATA ALREADY IN HAND. On the corpus's own
     McConnachie 2012 catalogue the MW field dominates for 19/22 MW satellites, and the surviving
     frame predicts dispersions a median 3.20-3.61x (69-72%) below what the framework's own closure
     needs from the same baryons -- range 2.00-8.82x across all four footing/kernel combinations, the
     extreme being Bootes I at 8.55x. The estimator is Upsilon-FREE (it uses only sigma and R_h and
     the framework's own closure to supply g_bar), so Front D's coherent-Upsilon blocker -- 0.38-0.48
     dex per object, 8.7x the signal -- does NOT apply to it. Same mechanism as the wide binary.
     SELF-CAUGHT ERROR, recorded: the first draft of this section evaluated mu at the NEWTONIAN
     argument and got 1.79x. That is the exact bug STANDING sec 5.1 records in the forest chain. The
     corrected number is ~2x LARGER, i.e. the error had been running in the framework's favour.
  8. Q5: the dragged frame does NOT re-open the ephemeris liability -- it SOFTENS it by lambda
     (alpha=1: 1279x -> 137-207x over Earth+Mars on both footings, 12.8-30.6x after the framework's
     own EFE: STILL EXCLUDED) and by lambda^2 = 55.5 under the kernel in force (alpha=2: ~2e-5x ->
     3.6e-7 - 8.0e-7x of the bound). No manufactured escape: alpha=1 stays dead. Structural signature
     r^1 vs Theorem B's r^2 (both fitted to 1e-9), both ~1e-20 m/s^2 and unobservable.
     mpmath at 50 digits was MANDATORY and it is demonstrated: float64 returns EXACTLY 0 for the
     FRAME-G Earth anomaly (true 2.24e-18) and is 78% wrong for the Theorem-B one.
  9. THE ANISOTROPY is the only DR4 axis where the readings separate: Theorem B gives a 0.0854
     eigenvalue spread and the frame construction gives EXACTLY 0 (no cross term). But projection
     dilutes the observable two-bin contrast to 0.0260 = 30.4% of the spread, so N(3 sigma) = 584,440
     against the pre-registration's assumed 30,000 -- a factor 19.5 short. Amendment 3 (h)'s
     uncomputed dilution flag is now computed; the estimator's velocity projection is a FURTHER
     dilution not modelled here.
 10. TWO DEFECTS FOUND IN THE FROZEN DOCUMENT, flagged and NOT edited: (i) Amendment 2 and Amendment 3
     use DIFFERENT angular-averaging conventions (quartic vs RMS), a 0.00094 = 0.034 sigma_tot spread
     -- real but non-decisive; (ii) Amendment 3 moved the ungated MI target to 1.0246 without
     restating Amendment 1's gated row, which becomes 1.00012-1.00020 rather than the frozen
     1.0004-1.0006. Both belong on the record before data, not after.
 11. NO THEORY IS CLOSED. The frame door is not closed by this: what is shown is that a SINGLE passive
     frame cannot supply the right speed to more than one mode, and that the one reading which
     survives the RAR pays for it in dwarfs, wide binaries and the Oort cloud. a0 = cH_Lambda/Z,
     kappa = 1/2, Z and omega_c remain POSTULATED. NO FROZEN TARGET HAS BEEN MOVED.""")
    print("=" * 104)
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
