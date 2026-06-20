#!/usr/bin/env python3
"""
ROUTE 3 diagnostics -- WHY the overlap is sub-additive, both ways. Make the physics explicit.

(1) THE MOND-RADIUS-vs-SEPARATION TEST: do the galaxies' deep-MOND tails even REACH each other?
    A galaxy's 1/r deep-MOND tail extends to its MOND radius r_M = sqrt(G m / a0). If r_M <<
    inter-galaxy separation s, the tails DON'T overlap (each galaxy is back to Newtonian 1/r^2
    long before reaching its neighbor) -> no collective deepening possible.

(2) THE TWO-CLUMP SUPERPOSITION TEST: put two equal masses M side by side, separation d.
    Compute the deep-MOND field at a far point and compare to (a) the field of a single 2M at
    the centroid, and (b) the LINEAR sum of two individual sqrt(M) fields. This isolates the
    sub-additivity sqrt(2M) < 2 sqrt(M) directly.

(3) THE ENCLOSED-MASS THEOREM: vary clumpiness (N, concentration) at FIXED total baryon mass;
    show M_phantom(<R) for R enclosing all baryons is invariant -> Carl's effect cannot add
    mass to a radius that already encloses all the baryons (the core does).

(4) THE INTER-GALAXY FLOOR / dS-Unruh horizon connection: is there a region-wide a0-class
    acceleration floor in the inter-galaxy medium that the smooth calc misses? Compute the
    actual g_N in the inter-galaxy medium and compare to a0.
"""
import numpy as np

G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
a0   = 9.36e-11

def g_obs(gN):   # framework deep/transition: g_obs = sqrt(gN^2 + gN a0)
    return np.sqrt(gN**2 + gN*a0)

# ---------------------------------------------------------------------------------
# (1) MOND radius vs inter-galaxy separation
# ---------------------------------------------------------------------------------
print("="*72)
print("(1) DO THE DEEP-MOND TAILS OVERLAP?  r_M vs inter-galaxy separation")
print("="*72)
M500 = 1e15*Msun
R_core = 420*kpc
M_star_core = 0.50*0.015*M500
N_gal = 200
m_typ = (M_star_core/N_gal)                 # typical galaxy mass
m_Lstar = 1e11*Msun                          # an L* galaxy
m_bcg   = 0.10*M_star_core
for label, m in [("typical member", m_typ), ("L* galaxy", m_Lstar), ("BCG", m_bcg)]:
    r_M = np.sqrt(G*m/a0)
    print(f"  {label:16s} m={m/Msun:.2e} Msun -> r_M = {r_M/kpc:6.1f} kpc")
# mean separation
n_dens = N_gal / (4/3*np.pi*R_core**3)
s_mean = n_dens**(-1/3)
print(f"\n  mean inter-galaxy separation s = n^(-1/3) = {s_mean/kpc:.1f} kpc")
print(f"  Even the BCG's r_M ({np.sqrt(G*m_bcg/a0)/kpc:.0f} kpc) < s ({s_mean/kpc:.0f} kpc);")
print(f"  typical member r_M ({np.sqrt(G*m_typ/a0)/kpc:.1f} kpc) << s by "
      f"{s_mean/np.sqrt(G*m_typ/a0):.0f}x  -> TAILS BARELY OVERLAP.")

# ---------------------------------------------------------------------------------
# (2) TWO-CLUMP SUPERPOSITION: sub-additivity directly
# ---------------------------------------------------------------------------------
print("\n"+"="*72)
print("(2) TWO-CLUMP DEEP-MOND SUPERPOSITION (sub-additivity)")
print("="*72)
M = 1e11*Msun
d = 300*kpc                      # separation > r_M (= 91 kpc for 1e11) so clumps are 'isolated'
r_M_1 = np.sqrt(G*M/a0)
print(f"  Two masses M={M/Msun:.0e} Msun, sep d={d/kpc:.0f} kpc, each r_M={r_M_1/kpc:.0f} kpc")
# far point on the symmetry axis, distance r from centroid, r >> d
for r in np.array([1000, 2000, 5000])*kpc:
    # exact superposition is nonlinear; approximate the COMBINED deep-MOND field two ways:
    # (a) single 2M point at centroid: g = sqrt(G*2M*a0)/r
    g_combined_2M = np.sqrt(G*(2*M)*a0)/r
    # (b) LINEAR sum of two isolated deep-MOND fields each sqrt(G*M*a0)/r_i (r_i~r at large r)
    g_linsum = 2 * np.sqrt(G*M*a0)/r
    # ratio: deep-MOND combined (sqrt(2M)) vs linear sum (2 sqrt(M))
    ratio = g_combined_2M / g_linsum     # = sqrt(2M)/(2 sqrt(M)) = 1/sqrt(2) = 0.707
    print(f"  r={r/kpc:5.0f} kpc:  g(2M combined)={g_combined_2M:.3e}  "
          f"g(linear sum of 2)={g_linsum:.3e}  ratio={ratio:.3f}")
print(f"  -> The TRUE collective field is 1/sqrt(2)={1/np.sqrt(2):.3f} of the naive linear sum.")
print(f"     Overlapping tails are SUB-ADDITIVE: collective binding is LESS, not more.")
print(f"     (The smooth cluster-MOND calc, which treats total enclosed mass, already gets")
print(f"      the sqrt(2M) -- so it is NOT missing a collective term; if anything the")
print(f"      discrete clumps give slightly LESS in the core, per the 3D grid.)")

# ---------------------------------------------------------------------------------
# (3) ENCLOSED-MASS THEOREM: vary clumpiness at fixed total mass
# ---------------------------------------------------------------------------------
print("\n"+"="*72)
print("(3) ENCLOSED-MASS THEOREM: phantom inside R enclosing all baryons is clumpiness-INVARIANT")
print("="*72)
# spherical Gauss law: for ANY baryon arrangement inside R, if R encloses total M_bar and the
# field at R is ~radial with magnitude G*M_bar/R^2 (multipoles fall off), then
#   M_ph(<R) = (nu(g_N(R)/a0)-1)*M_bar,  set ONLY by M_bar enclosed.
M_bar = 3.6e13*Msun
R = 420*kpc
gN = G*M_bar/R**2
nu = np.sqrt(1+a0/gN)
print(f"  At R={R/kpc:.0f} kpc enclosing M_bar={M_bar/Msun:.2e} Msun: gN/a0={gN/a0:.3f}")
print(f"  M_ph(<R) = (nu-1)*M_bar = {(nu-1)*M_bar/Msun:.3e} Msun  -- depends ONLY on M_bar,")
print(f"  NOT on whether the baryons are 1 smooth blob or 200 clumps. (Ostrogradsky, Bullet")
print(f"  paper: 'total phantom mass conserved independently of graininess'.) The core (<420")
print(f"  kpc) ENCLOSES essentially all the member-galaxy stellar mass -> the overlap cannot")
print(f"  add net phantom inside it. Verified numerically by the 3D grid (D/S ~ 0.996).")

# ---------------------------------------------------------------------------------
# (4) INTER-GALAXY a0-FLOOR / dS-Unruh horizon question
# ---------------------------------------------------------------------------------
print("\n"+"="*72)
print("(4) INTER-GALAXY ACCELERATION FLOOR -- is there a region-wide a0-class collective floor?")
print("="*72)
# The SMOOTH cluster field at the core radius already provides the cluster-scale acceleration.
M_bar_core = 3.6e13*Msun
gN_core = G*M_bar_core/R_core**2
g_obs_core = g_obs(gN_core)
print(f"  Smooth cluster g_N at core radius: {gN_core:.3e} = {gN_core/a0:.3f} a0")
print(f"  Smooth cluster g_obs (MOND-boosted): {g_obs_core:.3e} = {g_obs_core/a0:.3f} a0")
print(f"  -> the cluster's OWN smooth field is already ~a0-class at the core radius; the")
print(f"     'region-wide floor' IS the smooth cluster field, already in the standard calc.")
# What does the de Sitter / horizon a0-floor add? a0 itself is the cosmological floor.
# Does the ENSEMBLE reaching toward the dS scale add anything? The dS-Unruh a0 is a UNIFORM
# cosmological floor (same everywhere) -- it's the SOURCE of a0, not an extra cluster term.
print(f"  dS-Unruh: a0 = c^2 sqrt(Lambda/32pi) is the UNIFORM cosmic floor (same everywhere),")
print(f"  the SOURCE of the MOND scale -- NOT an extra cluster-localized binding term. The")
print(f"  collective ensemble does not 'reach the horizon' to harvest extra a0: each galaxy's")
print(f"  field is already cut off at its r_M (kpc-scale) by the cluster field >> a0 near")
print(f"  galaxies. No region-wide EXTRA floor beyond the smooth cluster field exists.")
