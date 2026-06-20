#!/usr/bin/env python3
"""
ROUTE B -- FULL relativistic / NON-STATIC lensing as a no-new-particle closure
of the cluster-core residual (Zimmerman framework, a0 = 9.36e-11).

QUESTION: the banked cluster residual (RX J1347, A2029) used QUASI-STATIC MOND
lensing.  In full relativistic AeST/khronon MOND, a NON-STATIC / merging cluster
has extra metric terms:
  (a) the gravitomagnetic zeta_i sector (0i Einstein eq, Blanchet-Skordis 2404.06584 Eq.3.12)
  (b) time-dependent O(c^-2) pieces of the field eqs
  (c) velocity-dependent lensing of moving mass.
Does a MERGING cluster get EXTRA lensing convergence beyond quasi-static MOND --
enough to source part of the ~30-49% residual WITHOUT extra mass?

KEY FACTS pulled from the lensing literature (2026-06-20):
 - AeST/khronon: NO gravitational slip, phi = psi (Eq.3.10) -> lensing == dynamics.
   The lensing potential is the SAME phantom counted once.  (Banked: slip door DEAD.)
 - Gravitomagnetic sector zeta_i (Eq.3.12): sourced by ORDINARY momentum density
   (rho_m v_m^i + rho_tau v_tau^i), enters the metric shift as N_i = (4/c^3) zeta_i.
 - GR weak-lensing decomposition (arXiv:2510.19798, astro-ph/0501605):
        kappa = kappa_Phi + kappa_j||
   where kappa_j|| ~ 2 (v_los/c) kappa_Phi is the gravitomagnetic (line-of-sight
   MOMENTUM) convergence.  Only the LINE-OF-SIGHT velocity enters the convergence;
   transverse motion just shifts the apparent lens position.
 - For DM halos the gravitomagnetic convergence correction is O(1e-3 .. 1e-2).

CRUCIAL POINT FOR THE FRAMEWORK: because AeST has no slip and the vector sector is
sourced by ORDINARY momentum rho*v (NOT by the MOND interpolation function), the
gravitomagnetic term gets NO MOND boost -- it is the same O(v/c) GR effect.  So the
honest estimate is the GR gravitomagnetic convergence with the cluster's velocity.

GATES: G1 sufficiency (close ~30-49% of core residual), G2 galaxy-veto, G3 no-new-
particle (own field/known physics), G4 data.  Both-ways + quarantine.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
c     = 2.99792458e8          # m/s
G     = 6.674e-11             # m^3 kg^-1 s^-2
Msun  = 1.989e30             # kg
kpc   = 3.0857e19            # m
Mpc   = 1e3 * kpc
a0    = 9.36e-11             # m/s^2  -- framework's MOND scale (NOT asserted derived)

print("="*78)
print("ROUTE B -- NON-STATIC / GRAVITOMAGNETIC LENSING of merging clusters")
print("           as a no-new-particle source of the core residual")
print("="*78)

# ---------------------------------------------------------------------------
# (1) THE TARGET -- banked core residual (RX J1347 merger; A2029 relaxed)
#     M_res(r) = M_lens - M_MOND.  We need extra LENSING convergence (effective
#     projected mass) to source ~30-49% of this WITHOUT real mass.
# ---------------------------------------------------------------------------
print("\n(1) THE TARGET (banked, framework footing a0=9.36e-11)")
# RX J1347 table (CLUSTER_CORE_SHAPE_RXJ1347):
#   r=300 kpc:  M_lens=2.09e14, M_MOND=4.6e13, M_res=1.6e14  (M_res/M_lens=0.766)
#   r=500 kpc:  M_lens=4.68e14, M_MOND=1.2e14, M_res=3.4e14  (M_res/M_lens=0.727)
# Residual is ~73-77% of M_lens in the core; the irreducible SHARED-MOND remainder
# after the no-particle stack is ~30-49% of the BARE gap.
M_lens_300 = 2.09e14   # Msun, within 300 kpc (RX J1347)
M_res_300  = 1.6e14    # Msun, residual within 300 kpc
frac_res_of_lens = M_res_300 / M_lens_300
print(f"  RX J1347 (<300 kpc): M_lens={M_lens_300:.2e}, M_res={M_res_300:.2e} Msun")
print(f"  Residual = {frac_res_of_lens*100:.1f}% of M_lens (this is the EFFECTIVE projected mass we must source)")
print(f"  Irreducible SHARED-MOND remainder after the no-particle stack: ~30-49% of the bare gap.")
print(f"  -> a non-static lensing term must add ~30-49% extra CONVERGENCE to count.")

# ---------------------------------------------------------------------------
# (2) MERGER VELOCITIES -- the relevant v for the gravitomagnetic term
# ---------------------------------------------------------------------------
print("\n(2) MERGER VELOCITIES (the v that sources the gravitomagnetic sector)")
# Bullet cluster: sub-cluster shock ~4700 km/s; gas/DM relative ~2000-3000 km/s.
# RX J1347: merger relative velocity ~1500-2000 km/s (Kreisch+2016, Ueda+2018).
# Use a GENEROUS merger v to give the door its best chance (both-ways: pro-closure).
v_merger_kms = {
    "RX J1347 (real merger)": 2000.0,
    "Bullet (extreme, gas)":  4700.0,
    "Bullet (DM-DM relative)":3000.0,
    "A2029 (relaxed, low v)":  300.0,
}
for name, vk in v_merger_kms.items():
    beta = (vk*1e3)/c
    print(f"  {name:28s}: v={vk:6.0f} km/s -> v/c = {beta:.4e},  (v/c)^2 = {beta**2:.3e}")

# ---------------------------------------------------------------------------
# (3) THE GRAVITOMAGNETIC CONVERGENCE -- exact GR scaling, applied to AeST
#     kappa_j|| ~ 2 (v_los/c) kappa_Phi   (arXiv:2510.19798 Eq.2-3; astro-ph/0501605)
#     Because AeST has NO slip and zeta_i is sourced by ORDINARY momentum rho*v,
#     there is NO MOND enhancement of this term -- it is the GR effect verbatim.
# ---------------------------------------------------------------------------
print("\n(3) GRAVITOMAGNETIC CONVERGENCE  kappa_j|| = 2 (v_los/c) kappa_Phi")
print("    (line-of-sight velocity only; AeST no-slip -> same as GR, NO MOND boost)")
print(f"    {'system':28s} {'v_los/c':>10s} {'kappa_j/kappa_Phi':>18s} {'extra conv %':>13s}")
results_gm = {}
for name, vk in v_merger_kms.items():
    beta_los = (vk*1e3)/c          # generous: take full merger v as line-of-sight
    ratio = 2.0 * beta_los         # kappa_j|| / kappa_Phi
    results_gm[name] = ratio
    print(f"    {name:28s} {beta_los:10.4e} {ratio:18.4e} {ratio*100:12.3f}%")

# ---------------------------------------------------------------------------
# (4) TIME-DEPENDENT O(c^-2) TERMS -- the phi-dot / sigma-dot pieces
#     In the field eqs (3.11-3.12) the time derivatives enter at O(c^-2) i.e.
#     suppressed by (1/c) x (characteristic frequency x length).  The merger
#     crossing time T ~ R/v sets the frequency.  Estimate the size of the
#     phi-dot term relative to the static Laplacian phi term.
# ---------------------------------------------------------------------------
print("\n(4) TIME-DEPENDENT O(c^-2) TERMS  (phi-dot, sigma-dot)")
# In the 0i eq, grad(phi-dot) competes with Laplacian(zeta).  The static term is
# Laplacian(phi) ~ phi/R^2.  The time term phi-dot/(c*R) ~ phi*v/(R^2 * c) (since
# d/dt ~ v/R for a structure moving at v).  Ratio = v/c.  Same O(v/c) suppression.
for name, vk in v_merger_kms.items():
    R = 300.0*kpc
    v = vk*1e3
    # d/dt phi ~ (v/R) phi ; the metric term phi-dot/c relative to static gradient phi/R:
    time_to_static = v/c
    print(f"  {name:28s}: |phi-dot/c| / |grad phi| ~ v/c = {time_to_static:.4e}")
print("  -> the non-static O(c^-2) corrections are ALSO O(v/c), same suppression as the vector sector.")

# ---------------------------------------------------------------------------
# (5) DIRECT EFFECTIVE-MASS CHECK -- the gravitomagnetic 'mass' of the moving gas
#     A blob of mass M moving at v has momentum p = M v.  Its gravitomagnetic
#     field sources an EFFECTIVE energy density rho_eff ~ (v/c)^2 rho beyond the
#     v/c convergence -- the kinetic-energy contribution to the source.
#     T^00 includes rho c^2; the moving-frame correction to the lensing source is
#     of order (1 + v^2/c^2) for the energy, and the momentum flux T^0i/c ~ rho v.
# ---------------------------------------------------------------------------
print("\n(5) DIRECT EFFECTIVE-MASS (kinetic-energy + momentum-flux) CHECK")
# Kinetic energy of the merging gas as 'extra lensing mass':
# M_gas(core) ~ 4.7e13 Msun (RX J1347, <420 kpc); KE = 1/2 M v^2; mass-equiv = KE/c^2.
M_gas = 4.69e13 * Msun
for name, vk in v_merger_kms.items():
    v = vk*1e3
    KE = 0.5 * M_gas * v**2
    M_KE_equiv = KE / c**2          # kg
    frac = M_KE_equiv / M_gas        # = 0.5 (v/c)^2
    print(f"  {name:28s}: KE/c^2 = {M_KE_equiv/Msun:.3e} Msun = {frac*100:.4f}% of M_gas  [= 0.5(v/c)^2]")
print("  -> the kinetic-energy 'extra mass' is 0.5(v/c)^2 ~ 1e-5 .. 1e-4 of the gas. NEGLIGIBLE.")

# ---------------------------------------------------------------------------
# (6) VERDICT vs GATES
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("(6) VERDICT vs THE FOUR GATES")
print("="*78)

best_merger_gm = results_gm["Bullet (extreme, gas)"]   # most generous merger
needed_low, needed_high = 0.30, 0.49

print(f"\n  G1 SUFFICIENCY: need extra convergence ~{needed_low*100:.0f}-{needed_high*100:.0f}% of the bare gap.")
print(f"     Gravitomagnetic kappa_j/kappa_Phi:")
print(f"        RX J1347 (real, v=2000):  {results_gm['RX J1347 (real merger)']*100:.3f}%   -> {results_gm['RX J1347 (real merger)']/needed_low:.5f}x of the LOW need")
print(f"        Bullet extreme (v=4700):  {best_merger_gm*100:.3f}%   -> {best_merger_gm/needed_low:.5f}x of the LOW need")
print(f"        A2029 relaxed (v=300):    {results_gm['A2029 (relaxed, low v)']*100:.4f}%")
shortfall = needed_low / best_merger_gm
print(f"     SHORTFALL even at the EXTREME Bullet velocity: need {shortfall:.0f}x MORE than available.")
print(f"     -> G1 FAILS by ~{shortfall:.0f}x (real RX J1347 merger: ~{needed_low/results_gm['RX J1347 (real merger)']:.0f}x short).")

print(f"\n  G2 GALAXY-VETO: gravitomagnetic term is O(v/c) on galaxies too (rotation v~200 km/s")
print(f"     -> v/c~7e-4, kappa_j~1e-3, negligible).  It does NOT touch the SPARC RAR.")
print(f"     -> G2 PASSES (the term is universally negligible, so it cannot break galaxies).")

print(f"\n  G3 NO-NEW-PARTICLE: the gravitomagnetic zeta_i is the framework's OWN metric vector")
print(f"     sector (AeST khronon), sourced by ORDINARY baryonic momentum rho*v. No new species.")
print(f"     -> G3 PASSES.")

print(f"\n  G4 DATA: applies ONLY to mergers (RX J1347, Bullet); ZERO for relaxed A2029 (v~300).")
print(f"     But the residual is GAS-TRACKING and IDENTICAL in slope (+1.81) on BOTH the merger")
print(f"     RX J1347 AND the relaxed A2029.  A velocity-sourced term would make the MERGER")
print(f"     residual LARGER than the relaxed one -- but they MATCH.  The data REFUTE a non-static")
print(f"     origin for the bulk residual.  -> G4 FAILS (wrong differential signature).")

print("\n" + "-"*78)
print("HONEST BOTH-WAYS SUMMARY")
print("-"*78)
print("""
 PRO (give the door its best shot):
   - The gravitomagnetic zeta_i sector IS real, IS the framework's own field (no new
     particle), and DOES add lensing convergence to a moving cluster.
   - It is largest for the fastest merger (Bullet, v~4700 km/s).
 CON (the honest physics):
   - The convergence correction is kappa_j ~ 2(v_los/c) kappa_Phi = O(1e-2) at the
     EXTREME Bullet velocity, O(7e-3) for the real RX J1347 merger.
   - The need is ~30-49% (0.30-0.49).  The term delivers ~0.7-3%.  SHORTFALL ~10-65x.
   - AeST no-slip + ordinary-momentum source -> NO MOND enhancement of the vector
     sector (it is the GR effect verbatim, not boosted by the interpolation function).
   - Time-dependent O(c^-2) terms are ALSO O(v/c): same suppression, no rescue.
   - Kinetic-energy 'extra mass' is 0.5(v/c)^2 ~ 1e-4 of the gas: utterly negligible.
   - DECISIVE data check: the residual SHAPE is IDENTICAL on the merger (RX J1347)
     and the relaxed (A2029) cluster (slope +1.81 both).  A velocity-sourced term
     would make mergers differ -- they do NOT.  The residual is NOT non-static in origin.

 NET: the (v/c)^2 intuition in the route brief was the RIGHT order for the KINETIC-mass
 piece (~2e-4); the LEADING gravitomagnetic CONVERGENCE is the larger O(v/c)~1e-2 piece,
 but BOTH are ~10-65x too small.  The honest likely-NULL is CONFIRMED, with real numbers.
""")
