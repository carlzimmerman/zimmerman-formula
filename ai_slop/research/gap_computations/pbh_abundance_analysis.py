#!/usr/bin/env python3
"""
Primordial Black Hole Abundance Analysis for Z² Framework

Computes:
1. Power spectrum from Z² inflation parameters
2. PBH formation probability
3. Mass function and constraints
4. Comparison to observational limits

Carl Zimmerman | May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, special, stats
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# Physical Constants
M_PL = 2.435e18  # Reduced Planck mass in GeV
M_SUN = 1.989e30  # kg
M_SUN_g = 1.989e33  # grams

# Z² Constants
Z_SQUARED = 32 * np.pi / 3  # = 33.510321638...
Z = np.sqrt(Z_SQUARED)       # = 5.788810...

# Z² Inflation Parameters
R_Z2 = 1 / (2 * Z_SQUARED)  # tensor-to-scalar ratio = 0.0149
N_S_Z2 = 0.965              # spectral index
A_S = 2.1e-9                # scalar amplitude at k* = 0.05 Mpc⁻¹
K_PIVOT = 0.05              # Mpc⁻¹

# Running of spectral index (slow-roll)
ALPHA_S = -0.003            # dn_s/d ln k

# PBH formation threshold
DELTA_C = 0.45              # critical overdensity

print("=" * 70)
print("PRIMORDIAL BLACK HOLE ABUNDANCE ANALYSIS")
print("Z² Framework: Standard Slow-Roll Inflation")
print("=" * 70)

# =============================================================================
# 1. Z² INFLATION PARAMETERS
# =============================================================================

print("\n" + "=" * 70)
print("1. Z² INFLATION PARAMETERS")
print("=" * 70)

print(f"Tensor-to-scalar ratio: r = 1/(2Z²) = {R_Z2:.4f}")
print(f"Spectral index: n_s = {N_S_Z2:.4f}")
print(f"Running: αs = dn_s/d ln k = {ALPHA_S:.4f}")
print(f"Scalar amplitude: A_s = {A_S:.2e} at k* = {K_PIVOT} Mpc⁻¹")

# Slow-roll parameters
epsilon_v = R_Z2 / 16  # ε_V = r/16
eta_v = (N_S_Z2 - 1 + 2*epsilon_v) / 2  # η_V from n_s

print(f"\nSlow-roll parameters:")
print(f"  ε_V = r/16 = {epsilon_v:.5f}")
print(f"  η_V = (n_s - 1 + 2ε)/2 = {eta_v:.5f}")

# =============================================================================
# 2. POWER SPECTRUM
# =============================================================================

print("\n" + "=" * 70)
print("2. PRIMORDIAL POWER SPECTRUM")
print("=" * 70)

def power_spectrum(k: float, k_pivot: float = K_PIVOT, A_s: float = A_S,
                    n_s: float = N_S_Z2, alpha_s: float = ALPHA_S) -> float:
    """
    Primordial scalar power spectrum P(k).

    P(k) = A_s × (k/k*)^(n_s - 1 + (1/2)α_s ln(k/k*))
    """
    ln_k_ratio = np.log(k / k_pivot)
    spectral_index = n_s - 1 + 0.5 * alpha_s * ln_k_ratio
    return A_s * (k / k_pivot)**spectral_index

# Power spectrum at different scales
k_values = np.logspace(-4, 20, 100)  # Mpc⁻¹

print(f"Power spectrum at key scales:")
print(f"{'k (Mpc⁻¹)':<15} {'P(k)':<15} {'Notes':<30}")
print("-" * 60)

key_scales = [
    (K_PIVOT, "CMB pivot scale"),
    (1.0, "BAO scale"),
    (1e6, "Stellar-mass PBH"),
    (1e12, "Asteroid-mass PBH"),
    (1e18, "Planck-mass PBH"),
]

for k, note in key_scales:
    P_k = power_spectrum(k)
    print(f"{k:<15.0e} {P_k:<15.2e} {note:<30}")

# Required P(k) for PBH formation
P_required = 1e-2  # Need ~10⁻² for significant PBH
print(f"\nRequired P(k) for PBH formation: P ~ {P_required:.0e}")
print(f"Z² prediction at all scales: P ~ {A_S:.0e} (no enhancement)")
print(f"→ Enhancement factor needed: {P_required/A_S:.0e}×")

# =============================================================================
# 3. PBH MASS-SCALE RELATION
# =============================================================================

print("\n" + "=" * 70)
print("3. PBH MASS-SCALE RELATION")
print("=" * 70)

def k_to_mass(k: float) -> float:
    """
    Convert comoving wavenumber k to PBH mass M.

    M_PBH ≈ M_H(k) ≈ 10²⁰ g × (k / 10⁶ Mpc⁻¹)⁻²
    """
    return 1e20 * (k / 1e6)**(-2)  # grams

def mass_to_k(M: float) -> float:
    """Convert PBH mass M (grams) to comoving wavenumber k."""
    return 1e6 * (M / 1e20)**(-0.5)  # Mpc⁻¹

print(f"{'PBH Mass (g)':<20} {'PBH Mass (M☉)':<20} {'k (Mpc⁻¹)':<20}")
print("-" * 60)

mass_grams = np.logspace(15, 40, 10)
for M in mass_grams:
    k = mass_to_k(M)
    M_solar = M / M_SUN_g
    print(f"{M:<20.2e} {M_solar:<20.2e} {k:<20.2e}")

# =============================================================================
# 4. PBH FORMATION PROBABILITY
# =============================================================================

print("\n" + "=" * 70)
print("4. PBH FORMATION PROBABILITY")
print("=" * 70)

def variance_smoothed(k_M: float, P_func) -> float:
    """
    Compute smoothed variance σ²(M) at scale k_M.

    σ²(M) = (16/81) × P(k_M) for sharp-k window
    """
    return (16/81) * P_func(k_M)

def beta_formation(sigma: float, delta_c: float = DELTA_C) -> float:
    """
    PBH formation fraction β using Press-Schechter.

    β = erfc(δ_c / (√2 σ)) / 2 ≈ (σ/√(2π) δ_c) exp(-δ_c²/(2σ²))
    """
    if sigma < 1e-10:
        return 0
    x = delta_c / (np.sqrt(2) * sigma)
    if x > 30:  # Avoid underflow
        # Asymptotic expansion
        return sigma / (np.sqrt(2 * np.pi) * delta_c) * np.exp(-delta_c**2 / (2 * sigma**2))
    return 0.5 * special.erfc(x)

print(f"Critical overdensity: δ_c = {DELTA_C}")
print(f"\n{'Mass (g)':<15} {'k (Mpc⁻¹)':<15} {'P(k)':<12} {'σ':<12} {'β':<15}")
print("-" * 70)

for M in [1e15, 1e20, 1e25, 1e30, 1e35]:
    k = mass_to_k(M)
    P_k = power_spectrum(k)
    sigma = np.sqrt(variance_smoothed(k, power_spectrum))
    beta = beta_formation(sigma)
    print(f"{M:<15.0e} {k:<15.2e} {P_k:<12.2e} {sigma:<12.2e} {beta:<15.2e}")

# =============================================================================
# 5. PRESENT-DAY PBH FRACTION
# =============================================================================

print("\n" + "=" * 70)
print("5. PRESENT-DAY PBH DARK MATTER FRACTION f_PBH")
print("=" * 70)

def f_pbh(beta: float, M: float, T_eq: float = 3400) -> float:
    """
    Present-day PBH fraction of dark matter.

    f_PBH = β × (T_eq/T_form) × correction factors
    ≈ β × (M_eq/M)^(1/2) × (Ω_m/Ω_DM)

    Simplified: f_PBH ≈ β × 10⁸ × (M/M_☉)^(1/2)
    """
    M_solar = M / M_SUN_g
    return beta * 1e8 * np.sqrt(M_solar)

print(f"PBH DM fraction for Z² inflation:")
print(f"\n{'Mass (g)':<15} {'β (formation)':<18} {'f_PBH':<15} {'Status':<20}")
print("-" * 70)

for M in [1e17, 1e20, 1e23, 1e26, 1e30]:
    k = mass_to_k(M)
    sigma = np.sqrt(variance_smoothed(k, power_spectrum))
    beta = beta_formation(sigma)
    f = f_pbh(beta, M)
    status = "≪ 1 (negligible)" if f < 1e-10 else ("< constraints" if f < 1 else "excluded")
    print(f"{M:<15.0e} {beta:<18.2e} {f:<15.2e} {status:<20}")

# =============================================================================
# 6. OBSERVATIONAL CONSTRAINTS
# =============================================================================

print("\n" + "=" * 70)
print("6. OBSERVATIONAL CONSTRAINTS ON f_PBH")
print("=" * 70)

# Constraint data (simplified)
constraints = [
    (1e15, 1e17, 1.0, "Evaporation"),
    (1e17, 1e21, 0.01, "Femtolensing"),
    (1e21, 1e24, 0.1, "NS capture"),
    (1e24, 1e28, 1.0, "Open window"),  # Least constrained
    (1e28, 1e34, 0.01, "Microlensing"),
    (1e34, 1e40, 0.001, "CMB/dynamics"),
]

print(f"{'Mass Range (g)':<25} {'f_PBH limit':<15} {'Source':<20}")
print("-" * 60)
for M_min, M_max, f_limit, source in constraints:
    print(f"{M_min:.0e} - {M_max:.0e}    {f_limit:<15.3f} {source:<20}")

# =============================================================================
# 7. WHAT WOULD BE NEEDED FOR PBH DM
# =============================================================================

print("\n" + "=" * 70)
print("7. REQUIREMENTS FOR PBH AS ALL DARK MATTER")
print("=" * 70)

# To get f_PBH = 1, need β ~ 10⁻⁸ for solar mass
# β ~ 10⁻⁸ requires σ ~ 0.04 (from erfc formula)
# σ ~ 0.04 requires P(k) ~ 0.04² × 81/16 ~ 0.008

sigma_required = 0.04
P_required = sigma_required**2 * 81/16

print(f"To have f_PBH ~ 1 (all DM as PBHs):")
print(f"  Need β ~ 10⁻⁸ (for stellar-mass PBHs)")
print(f"  Need σ ~ {sigma_required:.2f}")
print(f"  Need P(k) ~ {P_required:.3f}")
print(f"\nZ² predicts P(k) ~ {A_S:.2e}")
print(f"Enhancement needed: {P_required/A_S:.0e}×")
print(f"\n→ Z² inflation CANNOT produce significant PBH abundance")
print(f"→ Would need features, multi-field, or other modifications")

# =============================================================================
# 8. VISUALIZATIONS
# =============================================================================

print("\n" + "=" * 70)
print("8. GENERATING VISUALIZATIONS")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Plot 1: Power spectrum
ax1 = axes[0, 0]
k_plot = np.logspace(-4, 20, 200)
P_Z2 = np.array([power_spectrum(k) for k in k_plot])
P_required_arr = np.ones_like(k_plot) * 1e-2

ax1.loglog(k_plot, P_Z2, 'b-', linewidth=2, label='Z² inflation')
ax1.loglog(k_plot, P_required_arr, 'r--', linewidth=2, label='Required for PBH')
ax1.axhline(A_S, color='gray', linestyle=':', alpha=0.5, label=f'CMB amplitude')
ax1.axvline(K_PIVOT, color='green', linestyle=':', alpha=0.5, label='CMB pivot')
ax1.fill_between(k_plot, P_required_arr, 1, alpha=0.2, color='red', label='PBH formation region')
ax1.set_xlabel('Comoving Wavenumber k (Mpc⁻¹)', fontsize=12)
ax1.set_ylabel('Power Spectrum P(k)', fontsize=12)
ax1.set_title('Primordial Power Spectrum', fontsize=14)
ax1.legend(fontsize=9, loc='lower left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim([1e-4, 1e20])
ax1.set_ylim([1e-12, 1])

# Plot 2: β formation probability
ax2 = axes[0, 1]
sigma_range = np.logspace(-6, -0.5, 100)
beta_range = np.array([beta_formation(s) for s in sigma_range])

# Mark Z² prediction region
sigma_Z2 = np.sqrt(variance_smoothed(1e12, power_spectrum))  # At asteroid mass

ax2.loglog(sigma_range, beta_range, 'b-', linewidth=2)
ax2.axvline(sigma_Z2, color='green', linestyle='-', linewidth=2, label=f'Z² σ ~ {sigma_Z2:.1e}')
ax2.axhline(1e-8, color='red', linestyle='--', label='β for f_PBH=1')
ax2.fill_between([0.01, 0.1], [1e-20, 1e-20], [1, 1], alpha=0.2, color='red', label='Significant PBH')
ax2.set_xlabel('Variance σ', fontsize=12)
ax2.set_ylabel('Formation Fraction β', fontsize=12)
ax2.set_title('PBH Formation Probability', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([1e-6, 0.3])
ax2.set_ylim([1e-20, 1])

# Plot 3: f_PBH constraints
ax3 = axes[1, 0]
M_plot = np.logspace(15, 40, 100)
f_plot = []

for M in M_plot:
    k = mass_to_k(M)
    sigma = np.sqrt(variance_smoothed(k, power_spectrum))
    beta = beta_formation(sigma)
    f = f_pbh(beta, M)
    f_plot.append(max(f, 1e-50))  # Floor for plotting

ax3.loglog(M_plot, f_plot, 'b-', linewidth=2, label='Z² prediction')
ax3.axhline(1.0, color='red', linestyle='--', linewidth=2, label='All DM')

# Add constraint regions
for M_min, M_max, f_limit, source in constraints:
    ax3.fill_between([M_min, M_max], [f_limit, f_limit], [100, 100],
                     alpha=0.3, label=source if M_min == 1e15 else None)

ax3.set_xlabel('PBH Mass (grams)', fontsize=12)
ax3.set_ylabel('f_PBH (DM fraction)', fontsize=12)
ax3.set_title('PBH Dark Matter Fraction', fontsize=14)
ax3.legend(fontsize=8, loc='lower right')
ax3.grid(True, alpha=0.3)
ax3.set_xlim([1e15, 1e40])
ax3.set_ylim([1e-40, 10])

# Add secondary x-axis for solar masses
ax3_top = ax3.twiny()
ax3_top.set_xscale('log')
ax3_top.set_xlim([1e15/M_SUN_g, 1e40/M_SUN_g])
ax3_top.set_xlabel('PBH Mass (M☉)', fontsize=10)

# Plot 4: Summary
ax4 = axes[1, 1]
ax4.axis('off')

summary_text = f"""
PBH ABUNDANCE IN Z² FRAMEWORK

Inflation Parameters:
━━━━━━━━━━━━━━━━━━━━
  r = 1/(2Z²) = {R_Z2:.4f}
  n_s = {N_S_Z2}
  α_s = {ALPHA_S}
  A_s = {A_S:.1e}

Power Spectrum:
━━━━━━━━━━━━━━
  P(k) ~ {A_S:.0e} at all scales
  NO enhancement features
  Red tilt (n_s < 1) → power decreases at small k

PBH Formation:
━━━━━━━━━━━━━━
  Need P(k) ~ 10⁻² for PBH
  Z² gives P(k) ~ 10⁻⁹
  Gap: 10⁷× too small!

  σ(asteroid mass) ~ {sigma_Z2:.1e}
  β(formation) ~ exp(-10⁸) ≈ 0

Result:
━━━━━━━
  f_PBH << 10⁻²⁰

  Z² PREDICTS NEGLIGIBLE PBH ✗

If PBH DM discovered:
  Z² slow-roll inflation falsified
  Would need features or multi-field
"""
ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes, fontsize=11,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Z² PBH Analysis: Standard Slow-Roll Predicts f_PBH ≈ 0', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/gap_computations/pbh_abundance_analysis.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Saved: pbh_abundance_analysis.png")

# =============================================================================
# 9. SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SUMMARY: PBH ABUNDANCE IN Z² FRAMEWORK")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│                    KEY RESULTS                                       │
├─────────────────────────────────────────────────────────────────────┤
│  Z² Inflation: Standard slow-roll with r = 1/(2Z²) = 0.015         │
├─────────────────────────────────────────────────────────────────────┤
│  Power Spectrum:                                                     │
│    • P(k) ~ 2×10⁻⁹ at CMB scales                                   │
│    • Red tilt n_s = 0.965 → P decreases at small scales            │
│    • NO features, bumps, or enhancements                            │
├─────────────────────────────────────────────────────────────────────┤
│  PBH Formation Requirements:                                         │
│    • Need P(k) ~ 10⁻² at PBH scales                                │
│    • Need σ ~ 0.04 for significant formation                        │
│    • Z² gives σ ~ 10⁻⁵ (factor 10³ too small)                      │
├─────────────────────────────────────────────────────────────────────┤
│  Z² PREDICTION: f_PBH << 10⁻²⁰ (essentially zero)                  │
├─────────────────────────────────────────────────────────────────────┤
│  Implications:                                                       │
│    • PBHs are NOT dark matter in Z² framework                       │
│    • Sub-solar mass BH mergers (if real) are NOT primordial         │
│    • Dark matter must be phantom DM (MOND-like effects)             │
├─────────────────────────────────────────────────────────────────────┤
│  Falsification:                                                      │
│    • If PBH DM detected → Z² inflation needs modification           │
└─────────────────────────────────────────────────────────────────────┘
""")

print("\nAnalysis complete.")
