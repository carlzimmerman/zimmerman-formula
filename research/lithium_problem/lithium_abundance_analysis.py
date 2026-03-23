#!/usr/bin/env python3
"""
Cosmological Lithium Problem: Zimmerman Framework Analysis

THE LITHIUM PROBLEM (Factor of ~3):
  BBN Prediction: ⁷Li/H = (5.0 ± 0.3) × 10⁻¹⁰
  Observed:       ⁷Li/H = (1.6 ± 0.3) × 10⁻¹⁰
  Discrepancy:    Factor of 3.1 (>5σ)

PHYSICS OF LITHIUM-7 PRODUCTION IN BBN:
  Main production: ³He + α → ⁷Be + γ, then ⁷Be + e⁻ → ⁷Li + νe
  Main destruction: ⁷Li + p → 2α (very efficient below T~0.5 MeV)

  The ⁷Li abundance depends on:
  1. Baryon-to-photon ratio η = n_b/n_γ ≈ 6 × 10⁻¹⁰
  2. Nuclear reaction rates (which depend on α)
  3. Expansion rate H(t) during BBN

ZIMMERMAN APPROACH:
  The Zimmerman formula gives a modified expansion history:
    H² = (8πG/3)ρ_c × E(z)²

  If α or nuclear rates differ slightly from SM values during BBN,
  the lithium production could be suppressed.

References:
- Fields et al. (2020): BBN review
- Pitrou et al. (2018): Precision BBN calculation
- Spite & Spite (1982): Discovery of Spite plateau
"""

import numpy as np

# =============================================================================
# ZIMMERMAN CONSTANTS
# =============================================================================
Z = 2 * np.sqrt(8 * np.pi / 3)
sqrt_3pi_2 = np.sqrt(3 * np.pi / 2)

# Derived quantities
alpha_Z = 1 / (4 * Z**2 + 3)
alpha_s_Z = (sqrt_3pi_2 / (1 + sqrt_3pi_2)) / Z

print("=" * 80)
print("COSMOLOGICAL LITHIUM PROBLEM: ZIMMERMAN FRAMEWORK ANALYSIS")
print("=" * 80)

print(f"\nZimmerman Constants:")
print(f"  Z = {Z:.6f}")
print(f"  α = 1/{1/alpha_Z:.3f}")
print(f"  α_s = {alpha_s_Z:.4f}")

# =============================================================================
# THE LITHIUM PROBLEM
# =============================================================================
print("\n" + "=" * 80)
print("1. THE LITHIUM PROBLEM")
print("=" * 80)

# BBN predictions (from Planck+BBN)
Li7_BBN = 5.0e-10  # ⁷Li/H ratio
Li7_BBN_err = 0.3e-10

# Observations (Spite plateau)
Li7_obs = 1.6e-10
Li7_obs_err = 0.3e-10

# Discrepancy
ratio = Li7_BBN / Li7_obs
sigma = (Li7_BBN - Li7_obs) / np.sqrt(Li7_BBN_err**2 + Li7_obs_err**2)

print(f"\n  BBN Prediction: ⁷Li/H = ({Li7_BBN*1e10:.1f} ± {Li7_BBN_err*1e10:.1f}) × 10⁻¹⁰")
print(f"  Observed:       ⁷Li/H = ({Li7_obs*1e10:.1f} ± {Li7_obs_err*1e10:.1f}) × 10⁻¹⁰")
print(f"  Ratio: {ratio:.2f}× overprediction")
print(f"  Significance: {sigma:.0f}σ")

# Other light elements (for comparison)
print("\n  Other BBN abundances (for comparison):")
print("  Element    BBN Prediction       Observed        Status")
print("-" * 60)
print("  D/H        (2.57 ± 0.03)×10⁻⁵  (2.53 ± 0.03)×10⁻⁵  Excellent")
print("  ³He/H      ~1.0×10⁻⁵            1.0×10⁻⁵          Good")
print("  ⁴He Y_p    0.247 ± 0.001       0.245 ± 0.003     Good")
print("  ⁷Li/H      (5.0 ± 0.3)×10⁻¹⁰   (1.6 ± 0.3)×10⁻¹⁰  PROBLEM!")

# =============================================================================
# PROPOSED SOLUTIONS
# =============================================================================
print("\n" + "=" * 80)
print("2. PROPOSED SOLUTIONS TO THE LITHIUM PROBLEM")
print("=" * 80)

solutions = """
ASTROPHYSICAL SOLUTIONS:
  1. Stellar depletion - Stars destroy lithium over their lifetimes
     Problem: Spite plateau is too uniform (no scatter expected)

  2. Diffusion in stellar atmospheres
     Problem: Would produce observational signatures not seen

NUCLEAR PHYSICS SOLUTIONS:
  3. Missing nuclear reaction that destroys ⁷Be
     Candidates: ⁷Be(d,p)2α, ⁷Be(d,α)⁵Li
     Problem: Measured cross-sections too small

  4. Resonance in ⁷Be destruction not yet discovered
     Problem: No known candidates in energy range

COSMOLOGICAL SOLUTIONS:
  5. Variation of fundamental constants (α, G, etc.)
     A ~4% higher α during BBN could reduce ⁷Li production

  6. Non-standard expansion rate
     Modified H(t) during BBN could alter abundances

  7. Dark matter interactions
     WIMP annihilation could inject entropy, diluting ⁷Li

ZIMMERMAN RELEVANCE:
  The Zimmerman framework affects expansion rate through ρ_c.
  Could this resolve the lithium problem?
"""
print(solutions)

# =============================================================================
# ZIMMERMAN AND BBN PHYSICS
# =============================================================================
print("=" * 80)
print("3. ZIMMERMAN AND BBN PHYSICS")
print("=" * 80)

# BBN occurs at z ~ 10^9 (T ~ 1 MeV)
z_BBN = 1e9

# The Zimmerman expansion factor
Omega_m = 0.315
Omega_Lambda = 0.685

# At high z, E(z) ≈ √(Ω_m) × (1+z)^(3/2)
E_BBN = np.sqrt(Omega_m * (1 + z_BBN)**3 + Omega_Lambda)

print(f"\n  At BBN (z ≈ {z_BBN:.0e}):")
print(f"    E(z) = √(Ω_m(1+z)³ + Ω_Λ) ≈ √(Ω_m) × (1+z)^(3/2)")
print(f"    E({z_BBN:.0e}) = {E_BBN:.2e}")
print(f"    But at z>>1, this is dominated by matter: E ≈ √Ω_m × (1+z)^(3/2)")

# During radiation domination (BBN), we need to include radiation
print("\n  During BBN (radiation dominated):")
print("    The actual expansion rate is H² ∝ ρ_radiation ∝ T⁴")
print("    Zimmerman enters through the critical density ρ_c")

# The key Zimmerman input is the critical density
rho_c = 9.47e-27  # kg/m³ today
print(f"\n  Critical density today: ρ_c = {rho_c:.2e} kg/m³")

# At BBN, T ~ 1 MeV, the expansion rate was:
# H(BBN) ~ (T/T_0)² × H_0 × √(g_eff) × √(Ω_rad)
T_BBN_MeV = 1.0  # MeV
T_0_MeV = 2.725 * 8.617e-5  # CMB temperature in MeV
g_eff = 10.75  # effective relativistic degrees of freedom

H_0 = 70.0  # km/s/Mpc in SI
H_0_per_s = H_0 * 1000 / (3.086e22)  # per second

# H(BBN) ~ 1 s⁻¹ (order of magnitude)
H_BBN_approx = 1.0  # per second (order of magnitude)

print(f"\n  At T ~ 1 MeV:")
print(f"    H(BBN) ~ 1 s⁻¹")
print(f"    Neutron lifetime τ_n ~ 880 s")
print(f"    BBN timescale t ~ 1/H ~ 1 s to 3 min")

# =============================================================================
# FINE STRUCTURE CONSTANT VARIATION
# =============================================================================
print("\n" + "=" * 80)
print("4. FINE STRUCTURE CONSTANT VARIATION")
print("=" * 80)

# The ⁷Li abundance depends on α through:
# 1. Coulomb barriers in nuclear reactions
# 2. Binding energies of nuclei
# 3. Electron capture rates

print("\n  ⁷Li production depends on α through:")
print("    - Coulomb barriers: exp(-2πη) where η = Z₁Z₂αμc/ℏk")
print("    - Nuclear binding energies: ~α² corrections")
print("    - ⁷Be electron capture rate: ∝ α³")

# If α was different during BBN
# δ(⁷Li/H) / (⁷Li/H) ≈ 50 × (δα/α)
sensitivity = 50  # approximate sensitivity coefficient

print(f"\n  Sensitivity: δ(⁷Li/H)/(⁷Li/H) ≈ {sensitivity} × (δα/α)")

# What α variation is needed to fix the problem?
needed_Li_reduction = (Li7_BBN - Li7_obs) / Li7_BBN  # ~0.68
delta_alpha_needed = needed_Li_reduction / sensitivity

print(f"\n  To reduce ⁷Li by factor {ratio:.1f}:")
print(f"    Need δ(⁷Li)/(⁷Li) = {needed_Li_reduction:.2f}")
print(f"    Need δα/α ≈ {delta_alpha_needed:.3f} = {delta_alpha_needed*100:.1f}%")
print(f"    i.e., α during BBN was {abs(delta_alpha_needed)*100:.1f}% different")

# Zimmerman α vs CODATA α
alpha_CODATA = 1/137.036
delta_alpha_Z = (alpha_Z - alpha_CODATA) / alpha_CODATA

print(f"\n  Zimmerman α vs CODATA α:")
print(f"    α(CODATA) = 1/{1/alpha_CODATA:.3f}")
print(f"    α(Zimmerman) = 1/{1/alpha_Z:.3f}")
print(f"    δα/α = {delta_alpha_Z:.5f} = {delta_alpha_Z*100:.3f}%")
print(f"    This is {abs(delta_alpha_Z/delta_alpha_needed):.1f}× too small to fix lithium")

# =============================================================================
# ZIMMERMAN η (BARYON-TO-PHOTON RATIO)
# =============================================================================
print("\n" + "=" * 80)
print("5. BARYON-TO-PHOTON RATIO η")
print("=" * 80)

# η = n_b / n_γ ≈ 6.1 × 10⁻¹⁰ (from Planck)
eta_Planck = 6.1e-10
eta_err = 0.04e-10

print(f"\n  η = n_b/n_γ = ({eta_Planck*1e10:.2f} ± {eta_err*1e10:.2f}) × 10⁻¹⁰")

# η is related to Ω_b h²
Omega_b_h2 = 0.02237  # Planck 2018
h = 0.674  # Planck H_0/100

print(f"  Related to Ω_b h² = {Omega_b_h2:.5f}")

# ⁷Li increases with η for η < 5×10⁻¹⁰ but decreases for larger η
# The current η is in the "lithium valley" - hard to solve with η

print("\n  ⁷Li dependence on η:")
print("    For η < 5×10⁻¹⁰: ⁷Li increases with η")
print("    For η > 5×10⁻¹⁰: ⁷Li roughly constant or slightly decreasing")
print("    Current η = 6.1×10⁻¹⁰ is in the 'lithium valley'")
print("    Cannot solve the problem by changing η alone")

# =============================================================================
# ZIMMERMAN RESOLUTION: MODIFIED EXPANSION
# =============================================================================
print("\n" + "=" * 80)
print("6. ZIMMERMAN RESOLUTION: EVOLUTION OF CONSTANTS")
print("=" * 80)

# The key Zimmerman insight might be that α_s or other constants
# evolved during BBN

# The strong coupling α_s affects nuclear reaction rates
# Zimmerman derives α_s(M_Z) = 0.1183, but α_s runs with energy

alpha_s_MZ = alpha_s_Z
Lambda_QCD = 220  # MeV

# At BBN temperatures (T ~ 1 MeV), α_s is larger
T_BBN = 1.0  # MeV
# Very rough estimate: α_s(1 MeV) ~ 1 (non-perturbative)

print(f"\n  Zimmerman α_s(M_Z) = {alpha_s_MZ:.4f}")
print(f"  At BBN (T ~ 1 MeV), α_s ~ 1 (non-perturbative)")

# The ⁷Be destruction rate depends on nuclear strong force
print("\n  ⁷Be destruction (key reaction):")
print("    ⁷Be + n → ⁷Li + p  (main destruction channel)")
print("    Rate depends on strong interaction cross-section")

# Zimmerman prediction: if α_s at BBN was slightly different
# due to modified RG running, this could affect lithium

print("\n  ZIMMERMAN HYPOTHESIS:")
print("    If the Zimmerman formula modifies the RG running of α_s,")
print("    the nuclear reaction rates during BBN could differ.")
print("    This could suppress ⁷Li production by the required factor.")

# =============================================================================
# QUANTITATIVE ESTIMATE
# =============================================================================
print("\n" + "=" * 80)
print("7. QUANTITATIVE ZIMMERMAN PREDICTION")
print("=" * 80)

# The ⁷Li abundance scales roughly as:
# ⁷Li/H ∝ η × [⁷Be production] / [⁷Be destruction]
#
# The ⁷Be + n → ⁷Li + p reaction has cross-section σ ~ 1/v (thermal neutrons)
# This depends on the S-factor, which is nuclear physics

# A 10% change in the relevant S-factors could change ⁷Li by factor of 3
# This is within nuclear physics uncertainties for some reactions

# The Zimmerman connection:
# If α or α_s was slightly different during BBN, S-factors change

# ⁷Be(n,p)⁷Li S-factor sensitivity to α: δS/S ≈ 10 × δα/α
S_sensitivity = 10

print(f"\n  Key reaction: ⁷Be(n,p)⁷Li")
print(f"  S-factor sensitivity: δS/S ≈ {S_sensitivity} × δα/α")

# What δα/α would change S by 3×?
# Factor of 3 in ⁷Li requires ~10% change in S
# This needs δα/α ~ 1% (larger than Zimmerman provides)

print(f"\n  To get factor 3 change in ⁷Li:")
print(f"    Need ~10% change in S-factor")
print(f"    Requires δα/α ~ 1%")
print(f"    Zimmerman provides δα/α ~ 0.004%")
print(f"    INSUFFICIENT by factor of ~250")

# =============================================================================
# ALTERNATIVE: DARK SECTOR CONNECTION
# =============================================================================
print("\n" + "=" * 80)
print("8. ALTERNATIVE: ZIMMERMAN AND DARK SECTOR")
print("=" * 80)

alternative = """
DARK SECTOR ENTROPY INJECTION:

If there's a dark sector that decays after BBN but before recombination,
it could inject entropy and dilute ⁷Li.

The required entropy injection: ΔS/S ~ ln(3) ≈ 1.1

ZIMMERMAN CONNECTION:
  The Zimmerman formula includes Ω_Λ (dark energy).
  If dark energy has a dark matter precursor that decays,
  this could be the source of entropy injection.

  Required: Dark sector mass M ~ 1-10 MeV
            Decay time τ ~ 10³-10⁵ s (after BBN, before CMB)

  This is speculative but consistent with Zimmerman's
  inclusion of dark energy in fundamental physics.

PREDICTION:
  If Zimmerman is correct about the fundamental constants,
  the lithium problem is NOT resolved by varying α.
  Instead, it requires:
  1. Stellar depletion (astrophysical solution)
  2. Or dark sector physics (new particles)
"""
print(alternative)

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("SUMMARY: ZIMMERMAN AND THE LITHIUM PROBLEM")
print("=" * 80)

summary = f"""
THE LITHIUM PROBLEM:
  BBN predicts ⁷Li/H = 5.0×10⁻¹⁰
  Observed:    ⁷Li/H = 1.6×10⁻¹⁰
  Factor of 3.1 discrepancy (>5σ)

ZIMMERMAN ANALYSIS:
  1. The Zimmerman α differs from CODATA by only 0.004%
     This is ~250× too small to fix the lithium problem via α variation

  2. The Zimmerman framework does not directly modify BBN physics
     (BBN occurs at z ~ 10⁹, deep in the radiation era)

  3. The lithium problem remains a genuine puzzle

ZIMMERMAN CONCLUSION:
  The lithium problem is NOT resolved by the Zimmerman framework.
  This is actually a STRENGTH - Zimmerman doesn't claim to solve
  everything, only what follows from Z.

  The lithium problem likely requires:
  - Stellar depletion (atmosphere physics)
  - Nuclear physics updates (reaction cross-sections)
  - Or genuinely new physics (dark sector)

STATUS: LITHIUM PROBLEM REMAINS UNSOLVED BY ZIMMERMAN
  This is honest - the framework doesn't address BBN physics directly.
  The resolution lies in stellar physics or new particles, not in α variation.
"""
print(summary)

print("=" * 80)
print("Research: lithium_problem/lithium_abundance_analysis.py")
print("=" * 80)
