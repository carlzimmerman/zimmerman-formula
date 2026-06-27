#!/usr/bin/env python3
"""
keating_cmb_doors.py
====================
Both-ways honest magnitude audit: do Brian Keating's CMB-polarization experiments
(BICEP/BICEP2 -> POLARBEAR -> Simons Array -> Simons Observatory -> CMB-S4) open a
GENUINE above-floor near-term observational door for the de Sitter-Unruh modified-
inertia framework (a0 = c*H_Lambda/Z = 9.36e-11; preferred-frame = an SME background,
CPT-EVEN-only k_AF=0; a0(z) prop sqrt(rho_DE(z)); CMB-apex acceleration dipole ~0.06%)?

We test THREE candidate doors against the experiments' ACTUAL measured channels +
sensitivity floors. A door counts ONLY if the framework's signature is (i) framework-
DISTINCTIVE (not the SM/LCDM default, not MOND-shared), (ii) ABOVE the floor, and
(iii) near-term. Otherwise we say below-floor / null / consistency-only / shared.

Footing locked: a0 = 9.36e-11 m/s^2 (pure-Lambda, cH_Lambda/Z). NO re-derivation.

All experiment numbers are from REAL WebSearch (June 2026), cited inline.
"""

import math

C_KM = 299792.458  # km/s

print("="*78)
print("KEATING CMB-POLARIZATION DOORS  -  both-ways magnitude audit")
print("framework footing: a0 = 9.36e-11 m/s^2 (cH_Lambda/Z), preferred-frame SME bg")
print("="*78)

# ---------------------------------------------------------------------------
# Experiment floors (REAL, from WebSearch June 2026)
# ---------------------------------------------------------------------------
# BICEP/Keck:   r < 0.06 (95% CL), 95-220 GHz  (arXiv:1807.02199)
# POLARBEAR/Simons Array: B-mode lensing + inflation
# Simons Observatory (SO): 6 uK-arcmin, 1.4', 27-280 GHz; Keating = PI
# CMB-S4:       3 uK-arcmin, 1.0', 30-300 GHz, 21 telescopes
#
# Channel A -- ISOTROPIC COSMIC BIREFRINGENCE angle beta:
#   Minami-Komatsu 2020 (PR3):      beta = 0.34 +/- 0.14 deg  (2.4 sigma)
#   Diego-Palazuelos 2022 (PR4):    beta = 0.30 +/- 0.11 deg
#   WMAP+Planck joint:              beta = 0.342 +0.094/-0.091 deg
#   SO/S4/LiteBIRD: delensing -> sigma(beta) forecast ~ 0.01-0.05 deg
#
# Channel B -- CMB KINEMATIC DOPPLER BOOST (aberration+modulation), beta_v = v/c:
#   our peculiar motion: 369.82 km/s  -> beta_v = 1.2336e-3 (= 0.12%)
#   Planck boost detection S/N ~ 4 (lmax~4000); SO ~ 8.5; CMB-S4 ~ 20
#   (arXiv:1910.04315 forecast)
# ---------------------------------------------------------------------------

beta_birefr_meas_deg   = 0.30      # Diego-Palazuelos PR4 central
beta_birefr_err_deg    = 0.11
beta_birefr_sigma      = beta_birefr_meas_deg / beta_birefr_err_deg
sigma_beta_S4_deg      = 0.03      # representative SO/S4 delensed forecast (0.01-0.05)

beta_v_cmb             = 369.82 / C_KM   # kinematic Doppler boost parameter
SN_boost_Planck        = 4.0
SN_boost_SO            = 8.5
SN_boost_S4            = 20.0

# ---------------------------------------------------------------------------
# FRAMEWORK SIGNATURES
# ---------------------------------------------------------------------------
# (a) CMB-apex ACCELERATION/INERTIA dipole. The framework's preferred-frame
#     inertia anisotropy is a DIPOLE (l=1, cos psi) locked to the CMB apex,
#     NEGATIVE, saturating at -1/2 * beta_v in DEEP MOND (a << a0), and
#     SWITCHING OFF for a >> a0. Saturated amplitude:
apex_dipole_deepMOND = 0.5 * beta_v_cmb         # = 0.062%
#     CRITICAL: CMB photons free-stream at the speed of light; the relevant
#     "acceleration" of the CMB radiation field / of the last-scattering plasma
#     is the gravitational+expansion field, NOT a << a0. The framework's
#     inertia modification engages ONLY in the deep-MOND galaxy/lensing regime.
#     So the apex inertia-dipole lives in the WEAK-LENSING / GALAXY-KINEMATICS
#     channel, not in CMB polarization or CMB-temperature anisotropy.
#
# (b) CPT-even-only theorem: k_AF = a_mu = b_mu = 0 exactly
#     -> isotropic birefringence angle from the framework: beta_framework = 0.
#     The natural CPT-ODD scale hbar*H0 = 1.49e-42 GeV is 149x ABOVE the photon
#     CFJ bound (~1e-44 GeV), so a CPT-odd realization at the framework's own
#     scale would ALREADY be excluded -> the framework survives by predicting 0.
hbar_H0_GeV     = 1.49e-42
CFJ_bound_GeV   = 1.0e-44
cpt_odd_ratio   = hbar_H0_GeV / CFJ_bound_GeV

print("\n--- DOOR (a): CMB-apex acceleration/inertia DIPOLE vs CMB-pol/temp floor ---")
print(f"  framework deep-MOND apex inertia-dipole = 1/2*beta_v = {apex_dipole_deepMOND*100:.4f}%")
print(f"  ordinary CMB kinematic Doppler boost    =     beta_v = {beta_v_cmb*100:.4f}%")
print(f"  SO boost-detection S/N  ~ {SN_boost_SO}; CMB-S4 ~ {SN_boost_S4} (lmax~4000)")
print("  KEY DISTINCTION:")
print("   * The 0.12% kinematic boost IS measured by SO/S4 at high S/N -- but it is")
print("     the SM/LCDM peculiar-velocity effect, EVERYONE has it: NOT distinctive.")
print("   * The framework's DISTINCTIVE apex inertia-dipole exists ONLY at a<<a0")
print("     (galaxy/weak-lensing). CMB photons are NOT in the deep-MOND regime, so")
print("     the framework induces NO extra CMB-polarization or CMB-temperature")
print("     statistical anisotropy beyond the ordinary kinematic boost.")
# Quantify: even IF (counterfactually) the framework dipole leaked into the CMB
# temperature statistical-anisotropy channel at amplitude 0.062%, compare to the
# kinematic 0.12% that SO measures at S/N~8.5. A 0.062% signal degenerate with
# (half of) the kinematic boost is NOT separable as new physics.
leak_ratio = apex_dipole_deepMOND / beta_v_cmb
print(f"   * Counterfactual leak amplitude / kinematic boost = {leak_ratio:.3f}")
print("     -> fully degenerate with the kinematic-boost template; not separable.")
print("  VERDICT (a): BELOW-FLOOR / WRONG-CHANNEL. The distinctive content is a")
print("     deep-MOND lensing dipole (separate door, systematic-limited, 2030s+),")
print("     NOT a CMB-polarization observable. NOT a Keating-experiment door.")

print("\n--- DOOR (b): CPT-even null (beta_framework=0) vs Minami-Komatsu beta ---")
print(f"  measured isotropic birefringence: beta = {beta_birefr_meas_deg} +/- "
      f"{beta_birefr_err_deg} deg  ({beta_birefr_sigma:.1f} sigma from 0)")
print(f"  framework prediction:             beta_framework = 0 (CPT-even, k_AF=0)")
print(f"  SO/CMB-S4 forecast precision:     sigma(beta) ~ {sigma_beta_S4_deg} deg")
fut_sigma = beta_birefr_meas_deg / sigma_beta_S4_deg
print(f"  if 0.30 deg holds, SO/S4 reach    ~ {fut_sigma:.0f} sigma detection of beta!=0")
print(f"  natural CPT-odd scale hbar*H0/CFJ = {cpt_odd_ratio:.0f}x  (CPT-odd already excluded)")
print("  KEY DISTINCTION:")
print("   * beta_framework = 0 is ALSO the Standard-Model / LCDM default (no axion).")
print("     A confirmed beta != 0 means an EXTRA axion-like / parity-violating field")
print("     exists -- it does NOT falsify the framework's preferred frame (the frame")
print("     is CPT-EVEN, decoupled from the CPT-ODD k_AF channel that sources beta).")
print("   * So 'beta_framework=0' is a CONSISTENCY statement, not a discriminator:")
print("     the framework neither predicts the measured beta nor is killed by it.")
print("  VERDICT (b): CONSISTENCY-ONLY / SM-shared null. A measured beta!=0 at SO/S4")
print("     (which IS above-floor, ~10-30 sigma if 0.30 deg holds) is NOT a test of")
print("     THIS framework -- it tests axion/CPT-odd physics the framework excludes")
print("     by structure. NOT a genuine framework door. (This is the OLD retracted")
print("     'Z2 predicts beta=0 -> 6 sigma tension' overclaim, correctly demoted.)")

print("\n--- DOOR (g): radio/CMB source-count dipole anomaly (Secrest) ---")
# Secrest+2021 / Quaia / CatWISE: number-count dipole 2-5x the kinematic 0.12%,
# escalated to 5-6.4 sigma in 2026, same CMB apex.
secrest_excess = "2-5x kinematic (~0.3-0.6%), 5-6.4 sigma, same CMB apex"
print(f"  cosmic number-count dipole: {secrest_excess}")
print("  framework apex inertia-dipole (deep MOND) = 0.062%  -> ~8x BELOW the excess")
print("  CHANNEL: source counts of QSOs/radio gx at z~1-2 are HIGH-acceleration")
print("     (g >> a0, Newtonian). The framework's inertia law engages ONLY at a<<a0")
print("     and induces NO number-count dipole. Orthogonal observable.")
print("  VERDICT (g): DECOUPLED. ~8x too small AND wrong channel. Not a door.")

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("SUMMARY -- which Keating-experiment channel is a GENUINE above-floor door?")
print("="*78)
print(f"""
  channel                         | floor status     | framework verdict
  --------------------------------+------------------+--------------------------
  (a) CMB-apex inertia dipole     | wrong channel    | BELOW-FLOOR (lensing-only,
      in CMB pol/temp             | (a<<a0 needed)   |   not CMB; 2030s systematic)
  (b) isotropic birefringence     | ABOVE-floor      | CONSISTENCY-ONLY / SM-shared
      beta (Minami-Komatsu)       | (SO/S4 ~10-30 s) |   (beta=0 is SM default)
  (g) radio/CMB count dipole      | above-floor 5-6s | DECOUPLED (~8x small, wrong
      (Secrest)                   |                  |   channel)

  STRONGEST relative to the framework: door (b) -- the ONLY one that is genuinely
  ABOVE the SO/CMB-S4 floor and aligned with a real framework statement -- BUT it
  is a CONSISTENCY/SM-shared null, NOT a falsifiable framework-distinctive door.
  A confirmed beta != 0 tests CPT-ODD axion physics the framework structurally
  excludes (k_AF=0); it neither confirms nor kills the preferred frame.

  HONEST BOTTOM LINE: Keating's CMB-polarization program opens NO genuine above-
  floor framework-DISTINCTIVE door. The framework's only CMB-sector content is
  (b) a consistency null (beta=0, SM-shared) and (a) a kinematic-boost-degenerate
  dipole that lives in the LENSING channel, not in CMB polarization. The genuine
  live doors stay elsewhere (s^TX ephemeris 2028-32; a0(z) DESI DR3; dwarf sigma
  Gaia DR4) -- NOT in Keating's instruments.
""")

print("EXIT 0")
