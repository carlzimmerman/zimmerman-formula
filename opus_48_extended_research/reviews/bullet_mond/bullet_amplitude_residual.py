#!/usr/bin/env python3
"""
bullet_amplitude_residual.py  --  ROUTE 2 "the_amplitude"
=============================================================================
THE REAL BULLET ISSUE IS THE AMPLITUDE, not the offset.

This script computes the MOND lensing convergence (and projected mass) at the
Bullet Cluster (1E 0657-558, z=0.296) galaxy/lensing peaks from the VISIBLE
BARYONS ONLY -- galaxies' stars + the X-ray gas at/near the peak -- using the
ZIMMERMAN FRAMEWORK's own deep-MOND law g_obs = sqrt(g_bar^2 + g_bar*a0) at
a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2, and compares to the OBSERVED
lensing convergence (Clowe+2006) / projected mass (Famaey 2026).

OUTPUT: the residual factor -- how much extra COLLISIONLESS mass the framework's
own ghost-condensate field (NOT a new WIMP) must supply at the peaks -- and the
fraction the framework's own field + baryons can cover, tied to the banked
no-particle stack (CLUSTER_STACK_AND_DECISIVE_TEST: ~45% gas-tracking to ~54-65%
galaxy-tracking).

BOTH WAYS (#1 rule):
  - CONCEDE: the residual is REAL and SHARED (every MOND-family theory needs it;
    the framework's lower a0 makes it ~13% LARGER, not smaller).
  - CREDIT: it is the framework's OWN field (collisionless mode of its gravity
    sector), not a new particle; classically Angus-Famaey-Zhao needed ~2 eV
    neutrinos -- a PARTICLE the framework replaces with its own field, partially.

QUARANTINE: a0 / Z / kappa used as INPUTS, never asserted derived. I0 (the
field's residual amplitude) is FREE.

PRIMARY SOURCES (numbers transcribed from the papers):
  [C06]  Clowe, Bradac, Gonzalez, Markevitch, Randall, Jones, Zaritsky 2006,
         ApJL 648, L109 (astro-ph/0608407). Table 2 kbar, M_X, M_*. 7:1 ratio.
  [F26]  Famaey 2026, arXiv:2605.10022 "On the residual missing mass of the
         Bullet Cluster" (QUMOND, a0=3700 km^2/s^2/kpc=1.2e-10). The amplitude
         numbers: phantom+bar/bar = 2.8 (BCG1), 3.3 (BCG3) at 300 kpc; observed
         (bar+res+phantom)/bar = 8; residual = 3.4e14 Msun; M_lens(300) = 3.5e14
         (BCG1), 2.3e14 (BCG3); M_bar(300) = 4.6e13 (BCG1), 2.8e13 (BCG3).
  [AFZ]  Angus, Shan, Zhao & Famaey 2007 (astro-ph/0609125): inferred mass
         "exceed the observed baryons ... by a factor of 3 even in MOND" ->
         resolved with ~2 eV neutrinos (the particle the framework replaces).
  [M06]  Markevitch 2006: gas mass; bow shock.
  [STACK] CLUSTER_STACK_AND_DECISIVE_TEST_2026-06-20.md (no-particle stack).
"""
import numpy as np

# ============================================================================
# 0. CONSTANTS + FRAMEWORK a0
# ============================================================================
G      = 6.674e-11          # m^3 kg^-1 s^-2
c      = 2.998e8            # m/s
Msun   = 1.989e30           # kg
kpc    = 3.0857e19          # m
Mpc    = 1.0e3*kpc

a0_fw    = 9.36e-11         # framework: c^2 sqrt(Lambda/32pi)   [QUARANTINE: input]
a0_canon = 1.20e-10         # canonical/local MOND (Famaey 2026, all cited papers)

print("="*78)
print("BULLET CLUSTER -- THE AMPLITUDE RESIDUAL (ROUTE 2)")
print("framework a0 = %.3e m/s^2 (input, never derived);  canonical a0 = %.3e"
      % (a0_fw, a0_canon))
print("="*78)

# ============================================================================
# 1. THE FRAMEWORK'S OWN MOND LAW  g_obs = sqrt(g_bar^2 + g_bar*a0)
#    -> the BOOST nu = g_obs/g_bar, and the deep-MOND lensing-mass enhancement
# ============================================================================
def g_obs(g_bar, a0):
    """framework's dS-Unruh interpolation (the most-Newtonian MOND nu)."""
    return np.sqrt(g_bar**2 + g_bar*a0)

def nu(g_bar, a0):
    """boost factor g_obs/g_bar = effective M_dyn/M_bar (point-mass deep limit)."""
    return g_obs(g_bar, a0)/g_bar

# In AeST/relativistic MOND there is NO gravitational slip: the lensing potential
# equals the dynamical potential (Phi_lens = Phi_dyn = Phi_hat + phi). So the
# lensing mass = the dynamical (boosted) mass: M_lens(MOND) = nu * M_bar in the
# deep regime. (banked ROUTE3_BULLET_OFFSET_LENSING + AeST embedding.)

# ============================================================================
# 2. REAL BULLET DATA AT THE PEAKS  (Famaey 2026 = the modern, JWST-anchored
#    amplitude; aperture 300 kpc around each BCG)
# ============================================================================
print("\n--- (A) Famaey 2026 amplitude at 300 kpc (canonical a0=1.2e-10) [F26] ---")
# Projected masses within 300 kpc of each BCG:
M_lens   = {"BCG1_main": 3.5e14, "BCG3_sub": 2.3e14}   # observed lensing mass
M_bar    = {"BCG1_main": 4.6e13, "BCG3_sub": 2.8e13}   # baryons (gas+stars) in model
# MOND with baryons only -> (phantom+baryon)/baryon ratio at 300 kpc:
phantom_over_bar = {"BCG1_main": 2.8, "BCG3_sub": 3.3}  # = nu_eff (canonical a0)
# Observed (with residual added) (bar+res+phantom)/bar:
tot_over_bar     = 8.0                                   # both BCGs, F26

for k in M_lens:
    M_mond_canon = phantom_over_bar[k]*M_bar[k]   # what MOND-on-baryons supplies
    residual     = M_lens[k] - M_mond_canon       # what's left = collisionless
    res_factor   = M_lens[k]/M_mond_canon
    print(f"  {k:10s}: M_lens={M_lens[k]:.2e}  M_bar={M_bar[k]:.2e}"
          f"  nu_MOND(canon)={phantom_over_bar[k]:.2f}")
    print(f"             M_MOND(bar+phantom,canon)={M_mond_canon:.2e}"
          f"   M_lens/M_bar(obs)={M_lens[k]/M_bar[k]:.2f}")
    print(f"             RESIDUAL (collisionless) = {residual:.2e} Msun"
          f"   residual factor M_lens/M_MOND = {res_factor:.2f}x")

print(f"\n  F26 total projected residual (430 kpc main + 150 kpc sub) = 3.4e14 Msun")
print(f"  F26 statement: phantom+bar/bar = 2.8 (main), 3.3 (sub); obs/bar = 8")
print(f"  => MOND-on-baryons gets {2.8/8.0*100:.0f}-{3.3/8.0*100:.0f}% of the mass;"
      f" residual factor ~{8.0/2.8:.2f}-{8.0/3.3:.2f}x")

# ============================================================================
# 3. RE-FOOT ONTO THE FRAMEWORK'S a0=9.36e-11  (the honest surcharge)
#    deep-MOND boost (phantom) scales ~ sqrt(a0): lower a0 -> WEAKER phantom
#    -> LARGER residual. nu_deep = sqrt(a0/g_bar); the *extra* (phantom) mass
#    ~ (nu-1) scales ~ sqrt(a0) deep.
# ============================================================================
print("\n--- (B) Re-foot onto framework a0=9.36e-11 (the honest surcharge) ------")
surge = np.sqrt(a0_canon/a0_fw)     # how much WEAKER the framework phantom is
print(f"  deep-MOND phantom ~ sqrt(a0). sqrt(a0_canon/a0_fw) = {surge:.4f}")
print(f"  => framework phantom is ~{(1-1/surge)*100:.1f}% WEAKER -> residual ~{(surge-1)*100:.1f}% LARGER")

# Re-scale the phantom (the part above baryons) by sqrt(a0_fw/a0_canon):
ratio_fw = np.sqrt(a0_fw/a0_canon)  # = 1/surge = 0.883
print(f"  sqrt(a0_fw/a0_canon) = {ratio_fw:.4f} (phantom multiplier)")
for k in M_lens:
    nu_canon = phantom_over_bar[k]
    phantom_canon = (nu_canon - 1.0)*M_bar[k]        # the boost mass at canon a0
    phantom_fw    = phantom_canon*ratio_fw           # weaker at framework a0
    M_mond_fw     = M_bar[k] + phantom_fw
    nu_fw         = M_mond_fw/M_bar[k]
    residual_fw   = M_lens[k] - M_mond_fw
    res_factor_fw = M_lens[k]/M_mond_fw
    print(f"  {k:10s}: nu_canon={nu_canon:.2f} -> nu_fw={nu_fw:.2f}"
          f"   M_MOND_fw={M_mond_fw:.2e}")
    print(f"             RESIDUAL_fw = {residual_fw:.2e} Msun"
          f"   residual factor = {res_factor_fw:.2f}x  (vs {M_lens[k]/(M_bar[k]*nu_canon):.2f}x canon)")

# ============================================================================
# 4. CLOWE+2006 KAPPA AMPLITUDE CROSS-CHECK (the convergence at the peaks)
#    Observed kbar (mean convergence in 100 kpc aperture, Table 2):
#      main BCG  kbar = 0.36 +- 0.06    sub BCG  kbar = 0.20 +- 0.05
#    Plasma apertures kbar ~ 0.02-0.05  -> the 7:1 ratio C06 quote.
#    Convert kbar -> projected mass:  M_2D = kbar * Sigma_crit * (pi a^2).
# ============================================================================
print("\n--- (C) Clowe 2006 kappa amplitude cross-check [C06] -------------------")
# Sigma_crit for z_lens=0.296, z_source~1 (the C06 weak-lensing source plane).
# Standard cosmology (Om=0.3, OL=0.7, H0=70): angular-diameter distances ->
#   D_l ~ 920 Mpc, D_s ~ 1660 Mpc, D_ls ~ 1130 Mpc (z_s=1).
D_l  = 920.0*Mpc
D_s  = 1660.0*Mpc
D_ls = 1130.0*Mpc
Sigma_crit = (c**2/(4*np.pi*G))*(D_s/(D_l*D_ls))      # kg/m^2
Sigma_crit_Msun_Mpc2 = Sigma_crit*(Mpc**2)/Msun
print(f"  Sigma_crit (z_l=0.296, z_s~1) = {Sigma_crit:.3e} kg/m^2"
      f" = {Sigma_crit_Msun_Mpc2:.3e} Msun/Mpc^2")
a_ap = 100.0*kpc                                        # 100 kpc aperture radius
area = np.pi*a_ap**2
for lab, kbar in [("main BCG", 0.36), ("sub BCG", 0.20)]:
    M2D = kbar*Sigma_crit*area/Msun
    print(f"  {lab:9s} kbar={kbar:.2f} -> M_2D(<100kpc) = {M2D:.2e} Msun")
# Baryons at 100 kpc (C06 Table 2): gas + stars.
gas_main, star_main = 6.6e12, 0.54e12     # main BCG aperture (C06)
gas_sub,  star_sub  = 5.8e12, 0.58e12     # sub BCG aperture (gas is the offset peak)
print(f"  baryons@100kpc main BCG: gas={gas_main:.1e}+stars={star_main:.1e}"
      f" = {gas_main+star_main:.2e} Msun")
print(f"  baryons@100kpc sub  BCG: gas={gas_sub:.1e}+stars={star_sub:.1e}"
      f" = {gas_sub+star_sub:.2e} Msun")
# MOND boost at 100 kpc: estimate g_bar from the enclosed baryon mass.
for lab, kbar, Mb in [("main BCG", 0.36, gas_main+star_main),
                      ("sub BCG",  0.20, gas_sub+star_sub)]:
    M2D = kbar*Sigma_crit*area/Msun
    g_bar = G*(Mb*Msun)/a_ap**2          # rough Newtonian g at 100 kpc from M_bar
    boost_fw = nu(g_bar, a0_fw)
    M_mond_fw = boost_fw*Mb
    res = M2D/M_mond_fw
    print(f"  {lab:9s}: g_bar={g_bar:.2e} (g/a0={g_bar/a0_fw:.2f})"
          f"  nu_fw={boost_fw:.2f}  M_MOND_fw={M_mond_fw:.2e}"
          f"  M_2D(obs)={M2D:.2e}  residual={res:.2f}x")
print("  [C06 quote the needed kappa ratio (DM+gal):(plasma) ~ 7:1 at the peaks;")
print("   a pure constant-acceleration deep-MOND law needs a TRUE mass ratio up to 49:1.]")

# ============================================================================
# 5. CONNECT TO THE NO-PARTICLE STACK (banked CLUSTER_STACK_AND_DECISIVE_TEST)
#    The framework's OWN field + known baryons cover ~45% (gas-tracking, the
#    first-pass RX J1347 read) to ~54-65% (galaxy-tracking) of the residual.
#    The Bullet residual is the SAME shared MOND cluster gap.
# ============================================================================
print("\n--- (D) What the framework's OWN field covers at the Bullet peaks ------")
# Use the framework-footed residual (the harder, honest number).
res_factor_canon = tot_over_bar/np.mean(list(phantom_over_bar.values()))  # ~2.62x
# average phantom_over_bar = 3.05; residual factor canon:
nu_canon_avg = np.mean(list(phantom_over_bar.values()))
res_factor_fw_avg = tot_over_bar / (1.0 + (nu_canon_avg-1.0)*ratio_fw)
print(f"  mean MOND nu (canon)  = {nu_canon_avg:.2f}"
      f"  -> residual factor canon = {tot_over_bar/nu_canon_avg:.2f}x")
print(f"  mean MOND nu (framework) = {1.0+(nu_canon_avg-1.0)*ratio_fw:.2f}"
      f"  -> residual factor framework = {res_factor_fw_avg:.2f}x")
print(f"  => MOND-on-baryons (framework a0) supplies"
      f" {(1.0+(nu_canon_avg-1.0)*ratio_fw)/tot_over_bar*100:.0f}% of the lensing mass;")
print(f"     the COLLISIONLESS residual is the remaining"
      f" {100-(1.0+(nu_canon_avg-1.0)*ratio_fw)/tot_over_bar*100:.0f}% (~3.4e14 Msun, F26).")

# The no-particle stack (banked) covers a FRACTION of that residual with the
# framework's OWN field (Route B Y-Q boost ~+17-20%) + IGIMF stellar remnants
# (real baryons) -- NOT a new particle. Quote the banked stack coverage of the
# residual GAP (M_res), then translate to the total-mass accounting.
stack_gas   = 0.45      # gas-tracking (RX J1347 first-pass): field+baryons cover ~45% of M_res
stack_gal   = 0.595     # galaxy-tracking budget-respecting: ~54-65%, central ~59%
field_only  = 0.18      # the field's OWN Y-Q boost contribution (~17-20%), no remnants
print(f"\n  Banked no-particle stack (CLUSTER_STACK) coverage of the residual GAP M_res:")
print(f"    gas-tracking   : {stack_gas*100:.0f}% (field ~{field_only*100:.0f}% + budget-capped IGIMF remnants)")
print(f"    galaxy-tracking: {stack_gal*100:.0f}% (~54-65%)")
print(f"    field-ONLY (no remnants, pure Y-Q boost): ~{field_only*100:.0f}%")
print(f"    => irreducible SHARED gap that stays in EVERY scenario: ~35-55% of M_res")
print(f"       (~6-7.5e13 Msun) = the classic MOND rich-cluster residual.")

# Translate to the Bullet: of the ~3.4e14 residual, the framework's own field +
# budget-respecting remnants cover the stack fraction; the rest is the shared gap.
M_res_bullet = 3.4e14
for label, frac in [("gas-tracking", stack_gas), ("galaxy-tracking", stack_gal),
                    ("field-only", field_only)]:
    covered = frac*M_res_bullet
    gap     = (1-frac)*M_res_bullet
    print(f"  Bullet residual 3.4e14: {label:15s} field+baryons cover {covered:.2e}"
          f" ; shared gap {gap:.2e} Msun")

# ============================================================================
# 6. THE 2 eV NEUTRINO COMPARISON  (the particle the framework replaces)
# ============================================================================
print("\n--- (E) The particle the framework replaces [AFZ] ----------------------")
print("  Angus, Shan, Zhao & Famaey 2007 (astro-ph/0609125): MOND-inferred mass")
print('  at the peaks "exceed the observed baryons ... by a factor of 3 even in')
print('  MOND" -> resolved with ~2 eV NEUTRINOS (a new particle / hot-DM patch).')
print("  The FRAMEWORK replaces that 2 eV neutrino with its OWN ghost-condensate")
print("  field (a collisionless w=0 a^-3 mode of its gravity sector) -- which")
print("  covers ~45-65% of the residual; the rest is the shared MOND gap.")
print("  (Modern F26 2026 needs NO neutrinos either -- it just leaves the residual")
print("   as 'collisionless, centred on the galaxies, same as other clusters'.)")

print("\n" + "="*78)
print("HEADLINE NUMBERS:")
print("="*78)
print(f"  MOND-on-baryons (framework a0=9.36e-11) at 300 kpc: nu ~ {1.0+(nu_canon_avg-1.0)*ratio_fw:.2f}")
print(f"  observed M_lens/M_bar = 8  ->  RESIDUAL FACTOR ~ {res_factor_fw_avg:.2f}x (framework)")
print(f"  collisionless residual = 3.4e14 Msun (F26), centred on the GALAXIES")
print(f"  framework's OWN field+baryons cover ~45% (gas-track) to ~59% (gal-track)")
print(f"  -> shared MOND gap ~1.4-1.9e14 Msun stays (not a particle; not zero)")
print(f"  framework's lower a0 makes the residual ~{(surge-1)*100:.0f}% LARGER (conceded)")
print("="*78)
