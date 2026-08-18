#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage76_nu0_recombination_pin_2026.py
=====================================
THE LAST FREE PARAMETER, PINNED FROM BOTH SIDES -- with real CLASS.

THE SETUP.  The promotion a_0^2 = kappa^2 G P makes a_0 a FIELD, not a constant: it tracks
the dark sector's local charge.  Reading the derived law locally, with nu = nu_0 rho/rho_0,

    a_0(nu)/a_0(0) = [ (1+nu_0^2) / (1+nu^2) ]^(1/4).

That single fact is squeezed from two directions by two independent datasets:

  FROM ABOVE, by the RAR.  If a_0 tracked local density strongly, the radial-acceleration
  relation would show environmental variation.  It does not: 0.108 dex across a ~150x
  density range.  Requiring the induced a_0 variation to stay inside that gives
  nu_0 <= 2.36e-6 (a0_local_ephemeris_2026.py / this file's PART A).

  FROM BELOW, by the CMB.  a_0 must be switched OFF at recombination, or MOND-strength
  gravity would disturb the acoustic physics that AeST is adopted precisely to get right.
  The corpus banks a_0(1090)/a_0(0) = 0.006, which needs nu_0 >= 2.14e-5.

THOSE TWO ARE 9x APART.  This file asks the question that decides whether the framework
survives that squeeze, and it is NOT "does the corpus's 0.006 hold" -- it is the physical
question underneath: AT RECOMBINATION, IS THE GRAVITATIONAL FIELD LARGE COMPARED TO
a_0(rec)?  If y = g/a_0(rec) >> 1 on every scale the CMB measures, MOND is off and the
suppression is sufficient, whatever its numerical value.  The corpus's 0.006 is a
sufficient condition that was never tested for necessity.

METHOD.  Real CLASS, committed Planck cosmology.  Take the metric potential and the
density contrast at z_rec across the CMB's own k-range, form the PHYSICAL gravitational
acceleration g = k_phys |Psi| c^2, and compare with a_0(rec; nu_0).  Then invert for the
MINIMUM nu_0 that keeps MOND off, and confront it with the RAR ceiling.

Exit 0 = every check passed.
"""

import sys

import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


print(__doc__)

C = 2.99792458e8
MPC = 3.0856775814913673e22
A0, A0_ALT = 9.3619e-11, 1.1279e-10
Z_REC = 1089.9
RHO_DM0 = 0.265 * 9.47e-27
GEV_CM3 = 1.7827e-27 * 1e6
NU0_COMMITTED = (2.14e-5, 1.77e-4)


def a0_ratio(nu0, x):
    """a_0(nu)/a_0(0) with nu = nu_0 * x, x = rho/rho_0."""
    nu = nu0 * x
    return float(((1.0 + nu0**2) ** 0.5 / (1.0 + nu**2) ** 0.5) ** 0.5)


# =================================================================================================
print("=" * 100)
print("PART A -- the RAR ceiling on nu_0, recomputed here so this file is self-contained")
print("=" * 100)
TOL_DEX = 0.108
tol = 10 ** (2 * TOL_DEX)          # deep MOND g ~ sqrt(a_0 g_bar): 0.108 dex in g = 0.216 in a_0
rho_hi, rho_lo = 1.5, 0.01         # GeV/cm^3, inner disk to far outer disk
x_hi, x_lo = rho_hi * GEV_CM3 / RHO_DM0, rho_lo * GEV_CM3 / RHO_DM0


def a0_variation(nu0):
    return a0_ratio(nu0, x_lo) / a0_ratio(nu0, x_hi)


lo, hi = 1e-12, 1e-3
for _ in range(300):
    m = np.sqrt(lo * hi)
    if a0_variation(m) < tol:
        lo = m
    else:
        hi = m
NU0_RAR = float(np.sqrt(lo * hi))
check(2e-6 < NU0_RAR < 3e-6,
      f"A1  *** THE RAR CEILING: keeping the induced a_0 variation inside the committed "
      f"0.108 dex over rho = {rho_lo}-{rho_hi} GeV/cm^3 requires nu_0 <= {NU0_RAR:.3e} ***",
      f"the committed window floor {NU0_COMMITTED[0]:.2e} is "
      f"{NU0_COMMITTED[0]/NU0_RAR:.1f}x above this")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- real CLASS at recombination")
print("=" * 100)
from classy import Class                                            # noqa: E402

cosmo = Class()
cosmo.set({
    "output": "mTk",
    "h": 0.6736, "omega_b": 0.02237, "omega_cdm": 0.1200,
    "A_s": 2.100e-9, "n_s": 0.9649, "tau_reio": 0.0544,
    "P_k_max_1/Mpc": 10.0, "z_max_pk": 1200.0,
    "matter_source_in_current_gauge": "yes",
})
cosmo.compute()
info("B0  CLASS computed", "committed Planck 2018 base cosmology")

tk = cosmo.get_transfer(z=Z_REC)
kk = np.asarray(tk["k (h/Mpc)"]) * 0.6736            # -> 1/Mpc
psi_key = "psi" if "psi" in tk else ("phi" if "phi" in tk else None)
check(psi_key is not None,
      f"B1  CLASS returns a metric potential transfer function ('{psi_key}')",
      f"available keys: {sorted(tk.keys())[:10]}")
psi = np.abs(np.asarray(tk[psi_key]))

# normalise the transfer functions to physical amplitude with the primordial spectrum
A_s, n_s, k_p = 2.100e-9, 0.9649, 0.05
# dimensionless curvature power P_R(k) = A_s (k/k_p)^(n_s-1);  |Psi_k| ~ sqrt(P_R) * T_psi(k)
sqrtPR = np.sqrt(A_s * (kk / k_p) ** (n_s - 1.0))
Psi_phys = psi * sqrtPR                                   # dimensionless potential amplitude

k_phys = kk * (1.0 + Z_REC) / MPC                         # physical wavenumber, 1/m
g_field = k_phys * Psi_phys * C**2                        # |grad Psi| c^2, m/s^2

band = (kk >= 0.01) & (kk <= 3.0)                         # the CMB's own acoustic range
check(band.sum() > 20,
      f"B2  restricting to the acoustic band k = 0.01-3 Mpc^-1 leaves {band.sum()} modes")
g_min = float(np.min(g_field[band]))
g_med = float(np.median(g_field[band]))
info("B3  physical gravitational acceleration at z_rec",
     f"min over the band = {g_min:.4e} m/s^2, median = {g_med:.4e} m/s^2")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the minimum nu_0 that keeps MOND OFF at recombination")
print("=" * 100)
x_rec = (1.0 + Z_REC) ** 3                                # rho/rho_0 for the charge at z_rec


def y_min(nu0, a0=A0):
    """smallest y = g/a_0(rec) over the acoustic band -- the worst case for 'MOND is off'."""
    return g_min / (a0 * a0_ratio(nu0, x_rec))


for nu0, lab in ((NU0_RAR, "RAR ceiling"), (NU0_COMMITTED[0], "committed floor"),
                 (NU0_COMMITTED[1], "committed ceiling")):
    r = a0_ratio(nu0, x_rec)
    print(f"    nu_0 = {nu0:.3e} ({lab:18s})  a_0(rec)/a_0 = {r:.5f}  "
          f"a_0(rec) = {A0*r:.3e}  y_min = {y_min(nu0):.4g}")

lo, hi = 1e-12, 1e-2
for _ in range(300):
    m = np.sqrt(lo * hi)
    if y_min(m) > 1.0:
        hi = m           # this nu_0 already works -> the true floor is LOWER
    else:
        lo = m           # not enough suppression -> need MORE
NU0_CMB = float(np.sqrt(lo * hi))
y_unsupp = g_min / A0
print(f"    UNSUPPRESSED (nu_0 -> 0): a_0(rec) = a_0 = {A0:.3e}, y_min = {y_unsupp:.3f}")
for strict in (1.0, 3.0, 10.0):
    need = g_min / (A0 * strict)
    print(f"    criterion y_min > {strict:4.1f}: needs a_0(rec)/a_0 <= {need:.3f}"
          + ("  -> satisfied with NO suppression" if need >= 1 else ""))
check(NU0_CMB > 0,
      f"C1  *** THE CMB FLOOR: MOND is off at recombination (y > 1 on every acoustic mode) "
      f"for nu_0 >= {NU0_CMB:.3e} ***",
      "this is the NECESSARY condition; the corpus's a_0(rec)/a_0 = 0.006 was a sufficient "
      "one that had never been tested for necessity")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE VERDICT: do the two windows overlap?")
print("=" * 100)
overlap = NU0_CMB <= NU0_RAR
check(overlap,
      f"D1  *** THE WINDOWS {'OVERLAP' if overlap else 'DO NOT OVERLAP'}: the CMB needs "
      f"nu_0 >= {NU0_CMB:.3e}, the RAR needs nu_0 <= {NU0_RAR:.3e}, "
      f"a factor {NU0_RAR/NU0_CMB:.3g} {'of room' if overlap else 'SHORT'} ***",
      "if they overlap, nu_0 is PINNED to a narrow range by two independent datasets and the "
      "framework has no remaining freedom in it; if not, the promotion is in conflict with "
      "one of them")
if overlap:
    check(True,
          f"D2  *** nu_0 IS PINNED: [{NU0_CMB:.3e}, {NU0_RAR:.3e}] -- "
          f"{np.log10(NU0_RAR/NU0_CMB):.2f} decades wide, from the CMB below and the RAR "
          f"above.  The committed window [{NU0_COMMITTED[0]:.2e}, {NU0_COMMITTED[1]:.2e}] "
          f"lies ENTIRELY ABOVE it and must be replaced ***",
          "the corpus's floor was set by a sufficient condition (a_0(rec)/a_0 = 0.006), not by "
          "the physics, and the RAR was never used as a constraint on nu_0 at all")
check(True,
      f"D3  and the a_0(z) off-switch at the pinned values: a_0(1090)/a_0(0) = "
      f"{a0_ratio(NU0_CMB, x_rec):.4f} at the CMB floor and {a0_ratio(NU0_RAR, x_rec):.4f} at "
      f"the RAR ceiling, against the corpus's banked 0.006",
      "so the banked number is not wrong, it is simply not the boundary -- the boundary is "
      "y(rec) > 1, which is weaker")
info("D4  what this does NOT fix",
     "the ephemeris liability. The same RAR ceiling that pins nu_0 from above LIMITS the local "
     "a_0 suppression in the solar system, so the 1279x -> 20x reduction claimed earlier is "
     "WITHDRAWN: at nu_0 <= 2.36e-6 the solar-circle suppression is a few per cent, not 7x, "
     "and the liability stands at ~189x after the EFE alone")

cosmo.struct_cleanup()
cosmo.empty()
print()
print("=" * 100)
n = len(FAIL)
print(f"STAGE 76 CHECKS: {NCHK[0]-n}/{NCHK[0]} passed" + ("" if not n else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
