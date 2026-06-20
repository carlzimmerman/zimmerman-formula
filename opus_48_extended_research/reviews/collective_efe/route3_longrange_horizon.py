#!/usr/bin/env python3
"""
ROUTE 3 -- the LONG-RANGE / "reaches to the horizon" overlapping deep-MOND tails.

Carl's idea: in a relaxed cluster the member galaxies each source a long-range deep-MOND
field g ~ sqrt(G M a0)/r (1/r, not 1/r^2) that reaches FAR -- out to the EFE transition
(MOND radius) where it meets the cluster/cosmic external field g_ext ~ a0. The overlapping
1/r tails of N galaxies may build a region-wide COLLECTIVE potential that is DEEPER than the
SMOOTH-baryon cluster-MOND estimate -- adding binding (extra effective gravitating mass) with
NO new mass. Could close part of the ~30-49% irreducible cluster-core residual.

This script computes the actual QUMOND phantom mass in a rich cluster core TWO ways at the
framework's a0=9.36e-11:
  (A) member galaxies as N DISCRETE deep-MOND clumps + smooth ICM gas  (Carl's clumpy/overlap)
  (B) the SAME total baryonic mass as a SMOOTH distribution             (standard cluster-MOND)
and asks: does the discrete/overlap TOTAL phantom in the core EXCEED the smooth total?

Both ways. Quarantine: a0/Z/kappa NEVER asserted derived; a0=9.36e-11 used as input.

Key theory anchors (literature, this session):
 - Bullet MOND (arXiv:2605.10022): "From Ostrogradsky's theorem, the total phantom mass must
   be conserved independently of the graininess of the sources" -> enclosed-mass theorem.
 - SAME paper: "n baryonic masses M/n along the line-of-sight will produce MORE lensing than a
   single compact baryonic mass M, if separated by more than their MOND radius" -> separated
   clumps DO raise LOCAL phantom density (the genuine opening for Carl's idea).
 - Milgrom: deep-MOND superposition is NONLINEAR (field of two bodies != vector sum).
"""
import numpy as np
from scipy import integrate

# ----------------------------------------------------------------------------------
# Constants (SI) and framework footing
# ----------------------------------------------------------------------------------
G     = 6.674e-11            # m^3 kg^-1 s^-2
Msun  = 1.989e30            # kg
kpc   = 3.0857e19            # m
Mpc   = 1000.0 * kpc
a0    = 9.36e-11             # m/s^2  -- FRAMEWORK value (input, never asserted derived)
a0_kr = 1.2e-10             # m/s^2  -- regular-MOND default, for both-ways comparison

# deep-MOND simple/ dS-Unruh nu: g_obs = sqrt(g_N^2 + g_N a0).  nu(y)= 0.5 + sqrt(0.25 + 1/y),
# y = g_N/a0, so that g_obs = nu * g_N.  Phantom density via QUMOND.
def nu_dsunruh(y):
    # framework's own interpolation g_obs = sqrt(gN^2 + gN a0) => nu = g_obs/gN
    # = sqrt(1 + a0/gN) = sqrt(1 + 1/y)
    return np.sqrt(1.0 + 1.0/y)

# ----------------------------------------------------------------------------------
# Rich relaxed cluster, core target from the banked ledger (CLUSTER_STACK_2026-06-20):
#   M500 = 1e15 Msun, core radius R_core = 420 kpc, core M_res target = 1.357e14 Msun,
#   framework MI phantom baseline 3.508e13 (25.9%), bare gap 1.006e14. Residual ~30-49%.
# ----------------------------------------------------------------------------------
M500      = 1.0e15 * Msun
R_core    = 420.0 * kpc
M_res_tot = 1.357e14 * Msun     # total missing mass in core (lensing - baryons)
M_gap     = 1.006e14 * Msun     # bare gap after MI phantom baseline

# Baryon budget in the core. f_gas500 ~ 0.095, stars ~ 0.015. Core (<420 kpc ~ 0.28 R500)
# contains a fraction of the gas; use a representative core baryon mass.
fb        = 0.156
M_bar500  = fb * M500
# core gas fraction (gas is centrally less concentrated; ~30% of gas inside 0.28 R500)
M_gas_core   = 0.30 * 0.095 * M500 * Msun / Msun  # keep units: 0.30*0.095*M500
M_gas_core   = 0.30 * 0.095 * M500
M_star_core  = 0.50 * 0.015 * M500   # stars more concentrated, ~50% in core
M_bar_core   = M_gas_core + M_star_core
print(f"Core baryons: gas {M_gas_core/Msun:.3e}, stars {M_star_core/Msun:.3e}, "
      f"total {M_bar_core/Msun:.3e} Msun")

# ----------------------------------------------------------------------------------
# Member galaxy population. A rich cluster has ~ several hundred galaxies; the Bullet MOND
# paper used 219 discrete Plummer galaxies. The STELLAR mass in galaxies is M_star_core; the
# galaxies ALSO carry their own gas but the cluster gas is mostly ICM (smooth). For the
# clumpy/overlap test the relevant clumps are the STELLAR galaxies (the discrete baryon peaks).
# A galaxy's deep-MOND field reaches r_M = sqrt(G m a0)/a0 = sqrt(G m / a0).
# ----------------------------------------------------------------------------------
N_gal       = 200                      # member galaxies in the core
# distribute the core stellar mass over a Schechter-like luminosity function; for the field
# reach what matters is the per-galaxy mass. Use a characteristic L* galaxy + fainter tail.
# Simplify: give the BCG ~10% of core stellar mass, the rest spread over N-1 with a power law.
M_bcg       = 0.10 * M_star_core
m_rest_tot  = M_star_core - M_bcg
# power-law masses (steepish) for the N-1 satellites
ranks       = np.arange(1, N_gal)      # 1..N-1
w           = ranks**(-1.0)            # ~ 1/rank weighting
m_sat       = m_rest_tot * w / w.sum()
m_gal       = np.concatenate([[M_bcg], m_sat])   # N galaxy masses
assert abs(m_gal.sum() - M_star_core) / M_star_core < 1e-9

# MOND radius (field reach) per galaxy: r_M = sqrt(G m / a0)
r_M_gal = np.sqrt(G * m_gal / a0)
print(f"\nN_gal={N_gal}; BCG mass {M_bcg/Msun:.3e} Msun, r_M(BCG)={r_M_gal[0]/kpc:.1f} kpc")
print(f"median satellite mass {np.median(m_sat)/Msun:.3e} Msun, "
      f"median r_M={np.median(r_M_gal[1:])/kpc:.1f} kpc")
print(f"Mean inter-galaxy separation in core ~ "
      f"{(R_core/kpc)/(N_gal**(1/3)):.1f} kpc (core radius / N^(1/3))")

# mean baryon density in the core -> the SMOOTH g_N at the core radius
def gN_smooth_sphere(r, M_enc):
    return G * M_enc / r**2

# ----------------------------------------------------------------------------------
# THE KEY QUMOND COMPUTATION
# Phantom density: rho_ph = -(1/(4 pi G)) div[ (nu(|gN|/a0) - 1) gN ]
# Total phantom enclosed in radius R = -(1/(4 pi G)) * surface_integral[ (nu-1) gN . dA ]
#   = (1/G) * R^2 * (nu(g_N(R)/a0)-1) * g_N(R)      [spherical, Gauss law]
# This is the ENCLOSED-MASS THEOREM: for a spherical total baryon mass M_enc(R), the total
# phantom inside R depends ONLY on the boundary g_N(R) -> only on M_enc(R), the TOTAL enclosed
# baryon mass -- INDEPENDENT of clumpiness. We verify this, then test the NON-spherical /
# overlap correction that Carl's idea actually needs.
# ----------------------------------------------------------------------------------

def M_phantom_enclosed_spherical(R, M_bar_enc, a0=a0):
    """Total QUMOND phantom mass inside R for a spherical baryon distribution with
    M_bar_enc enclosed (Gauss-law boundary term)."""
    gN = G * M_bar_enc / R**2
    y  = gN / a0
    nu = nu_dsunruh(y)
    # M_ph(<R) = R^2/G * (nu-1) * gN  = (nu-1)*M_bar_enc
    return (nu - 1.0) * M_bar_enc

# (B) SMOOTH: all core baryons (gas+stars) as one spherical enclosed mass
Mph_smooth = M_phantom_enclosed_spherical(R_core, M_bar_core)
print(f"\n(B) SMOOTH spherical phantom in core (<{R_core/kpc:.0f} kpc): "
      f"{Mph_smooth/Msun:.3e} Msun, factor (nu-1)={Mph_smooth/M_bar_core:.2f}")
print(f"    -> baryon+phantom MOND mass in core = {(M_bar_core+Mph_smooth)/Msun:.3e} Msun")
print(f"    target M_res = {M_res_tot/Msun:.3e}; smooth MOND covers "
      f"{100*(M_bar_core+Mph_smooth)/M_res_tot:.1f}% of total (incl baryons)")
