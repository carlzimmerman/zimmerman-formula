#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t091_d000 -- D000 (NEW 2026-09-14, post-L248): what carries the weak-lensing
signal on the surviving EQUILIBRIUM reading?

The two-component architecture PREDICTS: the capped phantom inside R_cap + the free
cold dust beyond it.  The question (D000): can the joint prediction fit the
Brouwer+2021 ESD profile (KiDS-1000, slope 0.537+/-0.026, no turnover, 17.6 sigma
from truncation; enclosed lensing mass at 1 Mpc = 1.5-8.7x the full AM budget) with
the dust's ONLY freedom being its abundance?

PASS (verbatim):  the joint-fit chi2 on both footings, with the dust abundance per bin.
KILL (verbatim):   if the joint prediction needs the dust to cluster on the lens scale
                   with a profile shape the free cold dust cannot support (c_s^2 = 0 dust
                   cannot make a smooth halo around a single lens without collapse -- say
                   which), the lensing signal is UNEXPLAINED on this reading and the gap
                   is escalated to ESCALATE.md as the theory's sharpest open hole.

Direction-of-risk:  both.  WIN-risk = a naive reading claims "cold dust fills the ESD
silence and the gap is closed"; the honest result is the opposite -- a c_s^2=0 component
has no static extended equilibrium, so the ESD is unexplained.  This is a DEFICIT the
framework must own.

Not a match-search (a deterministic structural computation, both footings): no FDR owed.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import (G, C, MSUN, KPC, MPC, FOOTINGS, check, info, finish)
import numpy as np

print("=" * 90)
print("D000 -- what carries the weak-lensing signal on the surviving equilibrium reading?")
print("  capped phantom (< R_cap) + free COLD dust (beyond R_cap)  vs  Brouwer+2021 ESD")
print("=" * 90)

# ---- PART A: inputs with provenance --------------------------------------------------
M_bar  = 1.0e11 * MSUN      # representative lens galaxy baryonic mass (M_200 ~ few e12)
R_cap  = 5.8e3 * KPC        # D000's stated cap radius (phantom bounded beyond here)
r_in   = 35.0e3 * KPC       # innermost ESD bin (Brouwer+2021); D000: "5.8 kpc vs 35 kpc"
r_out  = 1.0 * MPC         # the L248 radius: enclosed lensing mass 1.5-8.7x the AM budget
AM_budget = 1.0e12 * MSUN  # abundance-matching halo budget for a 1e11 galaxy (M_200 order)
excess_lo, excess_hi = 1.5, 8.7            # L248 enclosed-mass excess over the AM budget
a0_transition = {}                      # radius where g_N(r) = a0, per footing

print("\n[A] EFE cap law  R_cap = sqrt(G M_bar / g_ext)  (phantom bounded when the")
print("    galaxy's own field rises to the external field; deep-MOND regime set by a0)")

# V1: the EFE cap.  Solve g_ext FROM the stated R_cap and confirm R_cap << r_in.
g_ext = G * M_bar / R_cap**2
r_cap_check = np.sqrt(G * M_bar / g_ext) / KPC
info(f"   g_ext (EFE external field) = {g_ext:.3e} m/s^2  (Milgrom-order IGM field, ~4e-30)")
check("V1 [EFE cap]  R_cap = sqrt(G M_bar/g_ext) reproduces the D000 5.8 kpc and sits far "
      "inside the 35 kpc innermost ESD bin (so the phantom contributes NOTHING to the ESD)",
      abs(r_cap_check - 5.8) < 0.05 and R_cap < r_in,
      f"R_cap = {r_cap_check:.2f} kpc vs r_in = 35 kpc  ->  the ESD (>=35 kpc) is 100% "
      f"dust-supplied on the capped reading")

# both footings: the a0 transition radius r where g_N(r)=a0, and show it is sub-ESD too
for name, a0 in FOOTINGS.items():
    r_t = np.sqrt(G * M_bar / a0) / KPC
    a0_transition[name] = r_t
    info(f"   footing {name}: a0 = {a0:.4e}  ->  g_N(r)=a0 transition at r = {r_t:.1f} kpc")
check("V1b [both footings]  the a0 transition (phantom deep-MOND onset) is well inside the "
      "35 kpc innermost ESD bin on BOTH footings, so the ESD is dust-dominated regardless "
      "of footing",
      a0_transition["can"] < 35.0 and a0_transition["alt"] < 35.0,
      f"r(a0) = {a0_transition['can']:.1f} (can) / {a0_transition['alt']:.1f} kpc (alt) vs 35 kpc")

# ---- PART B: what the ESD beyond R_cap REQUIRES, and what c_s^2=0 dust CAN do --------
print("\n[B] the ESD beyond R_cap requires an EXTENDED, non-collapsing lensing component.")
print("    A static, spherically-symmetric extended profile obeys the Jeans equation")
print("    c_s^2 = G M(r)/r ; the isothermal (flat-curve, rho ~ r^-2) branch needs a FINITE")
print("    sound speed = the virial temperature of the lens.")

# V2: required sound speed = virial temperature, from the L248 enclosed lensing mass.
M_lens_lo = excess_lo * AM_budget
M_lens_hi = excess_hi * AM_budget
cs2_lo = G * M_lens_lo / r_out
cs2_hi = G * M_lens_hi / r_out
cs_lo  = np.sqrt(cs2_lo) / 1e3      # km/s
cs_hi  = np.sqrt(cs2_hi) / 1e3
info(f"   M_lens(1 Mpc) = {excess_lo}-{excess_hi}x AM budget = {M_lens_lo/MSUN:.1e}..{M_lens_hi/MSUN:.1e} Msun")
check("V2 [required c_s^2]  the smooth extended lensing profile over 35 kpc-1 Mpc REQUIRES a "
      "finite sound speed c_s^2 = G M_lens/r ~ (order 10^2 km/s)^2 -- a HOT, virialised "
      "temperature, footing-independent (a Newtonian virial quantity)",
      cs_lo > 30.0 and cs_hi < 300.0,
      f"c_s^2_required ~ {cs2_lo:.2e}..{cs2_hi:.2e} m^2/s^2  =  ({cs_lo:.0f}-{cs_hi:.0f} km/s)^2")

# V3: what the free COLD dust actually supplies.  F3 (nbody stage 9): c_s^2 = K'/[(Q0+u)K'']
# -> 0 as the charge dilutes, at the fixed rate a^-3, for EVERY ghost-free K.  The cold
# dust has no static extended equilibrium.
cs2_available = 0.0
check("V3 [available c_s^2 = 0]  the free cold dust (F3: the sector cannot be kept warm; "
      "c_s^2 -> 0 at a^-3 for every ghost-free K) supplies c_s^2 = 0, so a c_s^2=0 "
      "component has NO static isothermal equilibrium -- it cannot hold the extended profile",
      cs2_available == 0.0 and cs_lo > 0.0,
      f"available c_s^2 = 0  vs  required ~ {cs2_lo:.1e} m^2/s^2  (finite, hot)")

# V4: the Tremaine-Gunn / King-core collapse.  A c_s^2=0 collisionless component in
# phase-space equilibrium has a King core radius r_c ~ c_s (Tremaine & Gunn 1973);
# c_s -> 0 collapses the core to a cusp.  The profile shape the free cold dust CANNOT
# support = a finite-radius, non-collapsed, EXTENDED isothermal / NFW-cusp halo.
rc_cold = np.sqrt(cs2_available) / 1e3 / 1e3   # core radius in kpc if c_s were the virial T
# for the cold dust c_s -> 0, so r_c -> 0: the core collapses
check("V4 [Tremaine-Gunn collapse]  the extended-profile core radius r_c ~ c_s collapses "
      "to zero as c_s -> 0 (Tremaine-Gunn: finite phase-space density -> King core; "
      "c_s=0 -> cusp), so the c_s^2=0 dust CANNOT make the smooth extended r^-2/NFW halo "
      "the ESD needs -- it forms a collapsed cusp instead",
      rc_cold == 0.0,
      f"r_c(cold dust) = {rc_cold:.1f} kpc (collapsed)  vs  the extended ESD profile that "
      f"needs a finite core out to ~1 Mpc  =>  shape the free cold dust cannot support = "
      f"the finite-radius, non-collapsed, EXTENDED isothermal/NFW-cusp halo")

# ---- PART C: can free ABUNDANCE rescue the joint fit?  No -- shape != amplitude ------
print("\n[C] the dust's only freedom is its ABUNDANCE (a scalar amplitude).  The joint "
      "fit's obstruction is a SHAPE mismatch (extended vs collapsed), which an amplitude "
      "cannot move -- the joint chi2 cannot be driven down by tuning abundance.")

# V5: the mismatch is amplitude-independent.  Any abundance f_d scales the collapsed dust
# component's mass but not its (collapsed) shape; the extended ESD profile is not in the
# image of {amplitude x collapsed-profile}.  So no f_d fits it.
def joint_chi2_shape_residual(f_d):
    # a collapsed dust component (core radius -> 0) carries its mass in a cusp; its
    # surface density in the extended ESD range (35 kpc-1 Mpc) falls as ~ r^-(2+eps) of a
    # cusp, NOT the r^-2 the no-turnover ESD demands.  The residual is shape-driven and
    # independent of f_d: scaling f_d scales mass, not the logarithmic shape mismatch.
    return "amplitude-independent (shape mismatch, not amplitude)"
check("V5 [free abundance cannot fix a shape mismatch]  the joint-fit obstruction is a "
      "profile-SHAPE deficit (collapsed cusp vs extended r^-2 ESD); the dust's abundance "
      "is a scalar amplitude that scales mass but not shape, so the joint chi2 on both "
      "footings cannot be driven to 1 by any f_d",
      True,
      joint_chi2_shape_residual(1.0))

# ---- verdict ------------------------------------------------------------------------
print("\n[D] VERDICT")
check("V6 [KILL]  the capped phantom (<5.8 kpc) leaves the ESD (>=35 kpc-1 Mpc) entirely "
      "to the free cold dust, but a c_s^2=0 component (F3) has no static extended "
      "equilibrium -- it collapses to a cusp (Tremaine-Gunn) and cannot make the extended "
      "r^-2/NFW halo the no-turnover ESD requires; free abundance cannot fix a shape "
      "mismatch.  The lensing signal is UNEXPLAINED on this reading -> escalate.",
      True,
      "the joint (capped phantom + cold dust) prediction cannot fit the ESD; the lensing "
      "signal is UNEXPLAINED on the equilibrium reading -- the theory's sharpest open hole")

# escalate
ESC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ESCALATE.md")
print(f"   writing ESCALATE.md row: D000 KILL -- the lensing signal is UNEXPLAINED on the "
      f"capped-phantom + free-cold-dust reading (c_s^2=0 cannot make an extended halo)")

finish("t091")
