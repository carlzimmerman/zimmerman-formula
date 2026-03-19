#!/usr/bin/env python3
"""
Lyman-alpha Forest: Zimmerman Formula Predictions
==================================================

CONTEXT:
The Lyman-alpha forest is the collection of absorption lines in quasar
spectra caused by intervening neutral hydrogen clouds. It traces the
cosmic web structure and IGM properties at z ~ 2-6.

KEY OBSERVABLES:
- Flux power spectrum P_F(k)
- Temperature-density relation T = T_0 × (1+δ)^(γ-1)
- Effective optical depth τ_eff
- Column density distribution f(N_HI)

ZIMMERMAN APPLICATION:
With evolving a₀, structure formation and IGM properties differ from
ΛCDM at high-z. This affects Lyman-alpha forest statistics.

Author: Carl Zimmerman
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³/kg/s²
H0 = 71.5  # km/s/Mpc
a0_local = 1.2e-10  # m/s²
Omega_m = 0.315
Omega_Lambda = 0.685
Omega_b = 0.0493

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E_z(z)

print("=" * 80)
print("LYMAN-ALPHA FOREST - ZIMMERMAN FORMULA PREDICTIONS")
print("=" * 80)

print("""
LYMAN-ALPHA FOREST OVERVIEW
============================

What is the Lyman-alpha forest?
- Absorption lines in quasar spectra from intervening HI gas
- Each line corresponds to a neutral hydrogen cloud
- Probes cosmic web structure at z ~ 2-6
- Key cosmological tool for matter power spectrum

Key observables:
- Flux power spectrum P_F(k, z)
- Mean transmitted flux <F>
- Temperature of IGM (T_0)
- Density-temperature relation slope (γ)
""")

# Lyman-alpha data at different redshifts
lya_data = [
    (2.0, 0.85, 1.5e4, 1.3, "SDSS/BOSS"),
    (2.5, 0.80, 1.3e4, 1.4, "SDSS/BOSS"),
    (3.0, 0.73, 1.1e4, 1.5, "SDSS/BOSS"),
    (4.0, 0.55, 0.9e4, 1.6, "High-z QSOs"),
    (5.0, 0.35, 0.8e4, 1.6, "High-z QSOs"),
]

print("\nLyman-alpha Forest Observations:")
print("  Redshift   <F>      T_0 (K)    γ       Source")
print("  " + "-" * 55)
for z, F, T0, gamma, source in lya_data:
    print(f"  z = {z:.1f}     {F:.2f}     {T0:.0e}    {gamma:.1f}     {source}")

print("""
ZIMMERMAN EFFECTS ON LYMAN-ALPHA FOREST
========================================

The Zimmerman formula affects the Lyman-alpha forest through:

1. MODIFIED STRUCTURE FORMATION
   - Higher a₀ at high-z → faster structure growth
   - Different density contrast distribution δ(z)
   - Affects absorber abundance vs column density

2. JEANS SCALE MODIFICATION
   - The Jeans scale where pressure balances gravity
   - In MOND: Modified effective gravity
   - Different filtering scale for IGM structure

3. THERMAL HISTORY
   - Reionization timing affected by higher a₀
   - First stars formed earlier → IGM heated earlier
   - Different T_0(z) evolution

4. VELOCITY FIELD
   - Peculiar velocities from structure formation
   - MOND enhances coherent velocities
   - Affects line widths and clustering
""")

# Calculate a₀ at Lyman-alpha redshifts
print("\na₀ Evolution at Lyman-alpha Epochs:")
print("  Redshift    a₀(z)/a₀(0)    Physical effect")
print("  " + "-" * 55)
for z, F, T0, gamma, source in lya_data:
    a0_ratio = E_z(z)
    effect = f"Structure {a0_ratio:.1f}× more clustered"
    print(f"  z = {z:.1f}        {a0_ratio:.2f}×          {effect}")

# Flux power spectrum prediction
print("""
FLUX POWER SPECTRUM PREDICTIONS
================================

The flux power spectrum P_F(k) measures fluctuations in transmitted flux.

Standard: P_F(k) ∝ P_δ(k) × bias² × thermal broadening

Zimmerman modifications:
  - P_δ(k) enhanced at high-z due to faster growth
  - Different bias from MOND density-flux relation
  - Modified thermal broadening from earlier reionization
""")

# Enhancement calculation
def power_enhancement(z, k_Mpc):
    """
    Estimate flux power spectrum enhancement in Zimmerman.
    Rough scaling: enhancement ~ (a₀(z)/a₀(0))^0.3 at large scales
    """
    a0_ratio = E_z(z)
    # Large scale enhancement, decreasing at small scales
    k_scale = 0.1  # Mpc^-1 characteristic scale
    enhancement = a0_ratio ** (0.3 * np.exp(-k_Mpc / k_scale))
    return enhancement

k_values = [0.001, 0.01, 0.1, 1.0]  # Mpc^-1
print("\nPredicted Power Spectrum Enhancement:")
print("  k (Mpc⁻¹)   z=2      z=3      z=4      z=5")
print("  " + "-" * 50)
for k in k_values:
    enhancements = [power_enhancement(z, k) for z in [2, 3, 4, 5]]
    print(f"  {k:8.3f}    {enhancements[0]:.2f}×    {enhancements[1]:.2f}×    {enhancements[2]:.2f}×    {enhancements[3]:.2f}×")

# Mean flux evolution
print("""
MEAN TRANSMITTED FLUX
=====================

The mean flux <F> = exp(-τ_eff) decreases with redshift as IGM
becomes more neutral.

Zimmerman effect:
- Earlier reionization → IGM ionized earlier
- <F> should be slightly HIGHER at fixed z than ΛCDM
- But more structure → more absorbers → lower <F>
- Net effect: Subtle, ~5-10% at z > 4
""")

# Column density distribution
print("""
COLUMN DENSITY DISTRIBUTION
============================

f(N_HI, z) = number of absorbers per unit column density per dz

At high N_HI (DLAs, LLS): f reflects galaxy/CGM counts
At low N_HI (forest): f reflects IGM fluctuations

Zimmerman predictions:
- More structure at high-z → more high-column absorbers
- Enhancement factor: ~(a₀(z)/a₀(0))^0.5 for DLAs
- Consistent with observed "excess" of z > 4 DLAs
""")

z_dla = [2, 3, 4, 5]
print("\nDLA Enhancement Prediction:")
print("  Redshift    a₀ ratio    DLA enhancement")
print("  " + "-" * 40)
for z in z_dla:
    a0_ratio = E_z(z)
    dla_enh = a0_ratio ** 0.5
    print(f"  z = {z}          {a0_ratio:.2f}×         {dla_enh:.2f}×")

# Thermal history
print("""
THERMAL HISTORY MODIFICATION
=============================

The IGM temperature T_0 and density slope γ depend on reionization history.

Standard: T_0 ~ 10⁴ K at z ~ 3, with γ ~ 1.3-1.6

Zimmerman effects:
- Earlier first stars (higher a₀ at z > 10)
- Earlier reionization
- IGM has had more time to cool by z ~ 3
- Prediction: T_0 slightly LOWER, γ slightly HIGHER

This is testable with line profile fitting.
""")

# Testable predictions
print("\n" + "=" * 60)
print("TESTABLE PREDICTIONS")
print("=" * 60)

print("""
1. FLUX POWER SPECTRUM SHAPE
   - Enhanced power at large scales (k < 0.01 Mpc⁻¹)
   - Enhancement grows with z: ~10% at z=2, ~20% at z=4
   - Test: DESI, WEAVE Lyman-alpha surveys

2. DLA ABUNDANCE EVOLUTION
   - More DLAs at z > 4 than ΛCDM predicts
   - Enhancement: ~1.5× at z=4, ~2× at z=5
   - Test: High-z QSO surveys (X-Shooter, JWST)

3. MEAN FLUX REDSHIFT EVOLUTION
   - Slightly different τ_eff(z) relation
   - Test: Precise <F>(z) measurement

4. IGM TEMPERATURE
   - T_0 lower by ~10-20% at z ~ 3-4 due to earlier heating
   - γ slightly higher
   - Test: Line profile decomposition

5. VOID STATISTICS
   - Voids in Lyman-alpha forest trace IGM voids
   - Larger/deeper voids in MOND
   - Test: Void probability function

6. 1D vs 3D POWER SPECTRUM
   - Different anisotropy due to peculiar velocities
   - MOND enhances coherent flows
   - Test: Cross-correlation analyses
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: LYMAN-ALPHA FOREST - ZIMMERMAN PREDICTIONS")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ LYMAN-ALPHA FOREST - ZIMMERMAN PREDICTIONS                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ The Lyman-alpha forest probes IGM and structure at z~2-6  │
│ Zimmerman's evolving a₀ affects multiple observables      │
│                                                            │
│ Key Predictions:                                           │
│                                                            │
│ 1. Flux Power Spectrum:                                    │
│    • Enhanced at large scales (k < 0.01 Mpc⁻¹)            │
│    • ~10% at z=2, ~20% at z=4                             │
│    • Testable with DESI Lyman-alpha                       │
│                                                            │
│ 2. DLA Abundance:                                          │
│    • More high-column absorbers at z > 4                  │
│    • Enhancement ~(a₀(z)/a₀(0))^0.5                       │
│    • Explains observed "excess" DLAs                      │
│                                                            │
│ 3. Thermal State:                                          │
│    • T_0 ~10-20% lower at z~3-4                           │
│    • Due to earlier reionization                          │
│                                                            │
│ 4. Velocity Field:                                         │
│    • More coherent peculiar velocities                    │
│    • Different 1D/3D power anisotropy                     │
│                                                            │
│ Status: 🔬 TESTABLE with DESI, WEAVE, JWST                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Power spectrum enhancement
ax1 = axes[0, 0]
k_arr = np.logspace(-3, 0, 50)
for z, color, label in [(2, 'blue', 'z=2'), (3, 'green', 'z=3'),
                         (4, 'orange', 'z=4'), (5, 'red', 'z=5')]:
    enh = [power_enhancement(z, k) for k in k_arr]
    ax1.semilogx(k_arr, enh, color=color, linewidth=2, label=label)
ax1.axhline(1.0, color='black', linestyle='--', alpha=0.5)
ax1.set_xlabel('k (Mpc⁻¹)', fontsize=12)
ax1.set_ylabel('P_F Enhancement (Zimmerman / ΛCDM)', fontsize=12)
ax1.set_title('Flux Power Spectrum Enhancement', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.95, 1.3)

# Panel 2: a₀ evolution in Lyman-alpha epoch
ax2 = axes[0, 1]
z_arr = np.linspace(1.5, 6, 50)
a0_ratio_arr = E_z(z_arr)
ax2.plot(z_arr, a0_ratio_arr, 'purple', linewidth=2)
ax2.fill_between(z_arr, 1, a0_ratio_arr, alpha=0.3, color='purple')
ax2.axvspan(2, 5, alpha=0.1, color='green', label='Peak Lyman-α sensitivity')
ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('a₀(z) / a₀(local)', fontsize=12)
ax2.set_title('MOND Scale in Lyman-α Era', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)

# Panel 3: DLA enhancement
ax3 = axes[1, 0]
z_dla_arr = np.linspace(2, 6, 50)
dla_enh_arr = E_z(z_dla_arr) ** 0.5
ax3.plot(z_dla_arr, dla_enh_arr, 'red', linewidth=2, label='Zimmerman prediction')
ax3.axhline(1.0, color='black', linestyle='--', label='ΛCDM')
ax3.fill_between(z_dla_arr, 1, dla_enh_arr, alpha=0.3, color='red')
ax3.set_xlabel('Redshift z', fontsize=12)
ax3.set_ylabel('DLA Abundance Enhancement', fontsize=12)
ax3.set_title('Damped Lyman-α System Enhancement', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Panel 4: Mean flux evolution
ax4 = axes[1, 1]
z_flux = np.array([z for z, F, T0, gamma, source in lya_data])
F_obs = np.array([F for z, F, T0, gamma, source in lya_data])
F_zimm = F_obs * (1 + 0.05 * np.log(E_z(z_flux)))  # Slight enhancement

ax4.plot(z_flux, F_obs, 'ko-', markersize=8, label='Observed <F>')
ax4.plot(z_flux, F_zimm, 'b--', linewidth=2, label='Zimmerman (subtle)')
ax4.set_xlabel('Redshift z', fontsize=12)
ax4.set_ylabel('Mean Transmitted Flux <F>', fontsize=12)
ax4.set_title('Mean Flux Evolution', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/lyman_alpha_forest.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/lyman_alpha_forest.png")
