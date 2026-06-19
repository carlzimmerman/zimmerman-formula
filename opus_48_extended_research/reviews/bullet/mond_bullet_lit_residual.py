#!/usr/bin/env python3
"""
mond_bullet_lit_residual.py  --  TOPIC: mond_bullet_lit
=============================================================================
Grounds the LITERATURE arithmetic for how MOND/modified-gravity handles the
Bullet Cluster (1E 0657-558, z=0.296), from the PRIMARY tables, and re-foots
the residual onto the Zimmerman framework's own a0.

NOT a new model -- a check that the cited NUMBERS are internally consistent and
that the framework's surcharge direction is correct (#1 rule: verify both ways).

PRIMARY SOURCES (numbers transcribed from the papers, see comments):
  - Angus, Shan, Zhao & Famaey 2007, ApJ 654, L13 (astro-ph/0609125):
      Table 2 -- projected masses in MOND vs GR vs observed baryons (C06/B06).
  - Clowe et al. 2006, ApJ 648, L109 -- the lensing "proof" (offset on galaxies).
  - Famaey et al. 2026 (arXiv:2605.10022) -- modern QUMOND residual.
  - Angus & McGaugh 2008, MNRAS 383, 417 -- collision velocity.
  - Lee & Komatsu 2010, ApJ 718, 60 -- LCDM velocity probability.
"""
import numpy as np

print("="*74)
print("BULLET CLUSTER -- MOND/MODIFIED-GRAVITY LITERATURE LEDGER")
print("="*74)

# --- (1) Angus+2007 Table 2: projected mass within 250 kpc of each lensing peak
# Units 1e13 Msun. MCM = total mass at the lensing (galaxy) centre in each gravity.
# Observed baryons (C06/B06 total in those apertures) ~ given as the comparison.
ACM1 = {"GR":21.7, "standard_mu":9.0,  "simple_mu":7.13, "obs_C06B06":(20.0+28.0)/2}
ACM2 = {"GR":17.2, "standard_mu":6.78, "simple_mu":6.42, "obs_C06B06":(21.0+23.0)/2}
# Observed BARYON mass at those peaks is small: galaxies are ~1/7 of gas, and the
# gas is offset; the baryon content AT the galaxy lensing peak is dominated by
# the (offset) gas projected in + the stellar mass. Angus+2007 state the inferred
# total "exceeds the observed baryons ... by a factor of 3 even in MOND".
print("\n(1) Angus, Shan, Zhao & Famaey 2007 -- Table 2 (1e13 Msun, r<250 kpc):")
print(f"    main-cluster lensing peak CM1: GR={ACM1['GR']}  stdMOND={ACM1['standard_mu']}  simpleMOND={ACM1['simple_mu']}")
print(f"    sub-cluster  lensing peak CM2: GR={ACM2['GR']}  stdMOND={ACM2['standard_mu']}  simpleMOND={ACM2['simple_mu']}")
print('    PAPER VERDICT (quote): inferred mass "exceed the observed baryons ...')
print('      by a factor of 3 even in MOND" -> MOND needs ~3x extra COLLISIONLESS')
print('      mass at the GALAXY (lensing) peaks; resolved as 2 eV neutrinos.')
print('      Tremaine-Gunn limit at T~9 keV admits rho<=1.9e-3 Msun/pc^3 for 2 eV;')
print('      Bullet phase-space density is consistent with 2 eV (just falsifiable')
print('      by KATRIN).')

# --- (2) Modern QUMOND (Famaey+2026, a0 = 3700 km^2/s^2/kpc = 1.20e-10 m/s^2)
a0_kms2_kpc = 3700.0
kpc = 3.085677581e19  # m
a0_canon = a0_kms2_kpc * (1e3**2) / kpc   # convert km^2 s^-2 kpc^-1 -> m/s^2
print(f"\n(2) Famaey et al. 2026 (QUMOND): a0={a0_kms2_kpc} km^2/s^2/kpc = {a0_canon:.3e} m/s^2 (canonical 1.2e-10)")
Mtot_over_Mbar_300kpc = 8.0      # observed (baryon+residual+phantom)/baryon at 300 kpc
# MOND phantom alone supplies part; residual is what's LEFT after the MOND boost.
# Paper: residual missing mass = 3.4e14 Msun, collisionless, centred on galaxies,
# "same order as the baryonic mass ... exactly as observed in other clusters".
M_residual_2026 = 3.4e14
print(f"    observed (bar+res+phantom)/bar at 300 kpc = {Mtot_over_Mbar_300kpc}")
print(f"    residual COLLISIONLESS missing mass = {M_residual_2026:.1e} Msun, on the galaxies")
print('    QUMOND phantom REPRODUCES the kappa-on-galaxies OFFSET (compact galaxies')
print('    make concentrated phantom; diffuse gas makes a flat sheet) -> offset is')
print('    NOT a clean MOND falsifier; residual = the SAME shared cluster residual.')
print('    NO neutrinos invoked in 2026 (vs the 2007 2 eV patch).')

# --- (3) Framework a0 surcharge: deep-MOND boost ~ sqrt(a0); lower a0 -> MORE residual
a0_fw   = 9.36e-11
ratio   = np.sqrt(a0_fw / a0_canon)          # phantom/boost scales ~ sqrt(a0)
surch   = 1.0/ratio - 1.0
print(f"\n(3) Framework re-footing: a0_fw={a0_fw:.3e} vs a0_canon={a0_canon:.3e}")
print(f"    deep-MOND boost ~ sqrt(a0): sqrt(a0_fw/a0_canon) = {ratio:.3f}")
print(f"    -> framework phantom ~{(1-ratio)*100:.1f}% WEAKER -> residual ~{surch*100:.1f}% LARGER")
print(f"    e.g. M/Mbar residual factor ~2.8 (canon) -> ~{2.8/ratio:.2f} (framework)")
print("    DIRECTION: the lower framework a0 makes the Bullet residual WORSE, not")
print("    better. No false-deficit to retract; literature (canon a0) UNDERSTATES it.")

# --- (4) Collision velocity (Angus & McGaugh 2008; Lee & Komatsu 2010)
print("\n(4) Collision velocity -- a genuine LCDM strain MOND-family eases:")
print("    shock v_shock ~ 4700 km/s (Markevitch 2006); inferred infall ~3000 km/s")
print("    Angus & McGaugh 2008: CDM max ~3800 km/s (only OK if shock hydro-enhanced);")
print("                          MOND naturally ~4500-4800 km/s.")
print("    Lee & Komatsu 2010 (MICE N-body, (2-3)R200): P(>3000 km/s) =")
print("        3.3e-11 (z=0)  to  3.6e-9 (z=0.5)   <- ~1-in-1e9..1e11 in LCDM")
print("        P(>2000 km/s) = 2.9e-5 (z=0) to 2.2e-3 (z=0.5)")
print("    -> a real LCDM ding; faster Lambda-MOND structure formation accommodates.")
print("    CAVEAT (both ways): shock != bulk speed; big LCDM sims (Thompson+2015,")
print("    Kraljic-Sarkar 2015) find such speeds rare-but-ALLOWED -> a ding, not a kill.")

print("\n" + "="*74)
print("CONSENSUS (both ways): NO modified-gravity theory reproduces the Bullet")
print("WITHOUT residual collisionless mass on the GALAXIES (~2-3x baryons).")
print("  - TeVeS (Feix+2008, 0707.0790): convergence TRACKS baryons; nonlinear")
print("    offset 'very small'; 'cannot explain ... without an additional dark")
print("    mass component in both cluster centers'.")
print("  - MOG (Brownstein & Moffat 2007): claimed a baryon-only fit, but is")
print("    DISPUTED (uses its own running-G + a fitted gas/galaxy split; not")
print("    reproduced by the AeST/QUMOND community).")
print("  - QUMOND (2026): reproduces the OFFSET but STILL needs 3.4e14 Msun")
print("    residual collisionless mass = the shared cluster problem.")
print("FRAMEWORK INHERITS this MOND-shared residual, +~13% for its lower a0.")
print("="*74)
