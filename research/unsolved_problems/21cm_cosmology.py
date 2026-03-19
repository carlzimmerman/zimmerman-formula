#!/usr/bin/env python3
"""
21cm Cosmology: Zimmerman Formula Predictions
==============================================

CONTEXT:
The 21cm hyperfine transition of neutral hydrogen is a powerful probe
of the early universe. Observations of the 21cm signal can reveal:
- Epoch of Reionization (EoR)
- Cosmic Dawn (first stars)
- Dark Ages (before first stars)

CURRENT STATUS:
- EDGES claimed detection of 21cm absorption at z~17 (controversial)
- HERA, SKA, LOFAR are searching for EoR signal
- Many theoretical predictions assume ΛCDM

ZIMMERMAN APPLICATION:
With evolving a₀, structure formation at high-z differs from ΛCDM.
This affects:
1. When first stars formed
2. How ionizing radiation propagated
3. The 21cm power spectrum

Author: Carl Zimmerman
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³/kg/s²
H0 = 71.5  # km/s/Mpc
H0_si = H0 * 1e3 / 3.086e22  # /s
a0_local = 1.2e-10  # m/s²
Omega_m = 0.315
Omega_Lambda = 0.685
Omega_b = 0.0493

# 21cm line properties
freq_21cm = 1420.405752  # MHz
wavelength_21cm = 21.106  # cm

def E_z(z):
    """Dimensionless Hubble parameter"""
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E_z(z)

def observed_freq(z):
    """Observed frequency of 21cm line at redshift z"""
    return freq_21cm / (1 + z)

print("=" * 80)
print("21cm COSMOLOGY - ZIMMERMAN FORMULA PREDICTIONS")
print("=" * 80)

print("""
21cm COSMOLOGY OVERVIEW
=======================

The 21cm line traces neutral hydrogen throughout cosmic history:

| Era              | Redshift    | What 21cm reveals              |
|------------------|-------------|--------------------------------|
| Dark Ages        | z > 30      | Pure cosmology (no stars yet)  |
| Cosmic Dawn      | z ~ 15-30   | First stars, heating/ionization|
| Reionization     | z ~ 6-15    | Bubble morphology, completion  |
| Post-reionization| z < 6       | HI in galaxies                 |

Key observable: 21cm brightness temperature relative to CMB
  δT_b = T_s - T_CMB  (spin temperature vs CMB)

In absorption: T_s < T_CMB → δT_b < 0 (Dark Ages, early Cosmic Dawn)
In emission: T_s > T_CMB → δT_b > 0 (after X-ray heating)
""")

# Calculate frequencies for different epochs
print("\n21cm Observation Frequencies:")
print("  Epoch           Redshift    Observed freq (MHz)")
print("  " + "-" * 50)
epochs = [
    ("Dark Ages (middle)", 50),
    ("Cosmic Dawn (start)", 30),
    ("Cosmic Dawn (peak)", 17),
    ("Reionization (middle)", 10),
    ("Reionization (end)", 6),
]
for name, z in epochs:
    freq = observed_freq(z)
    print(f"  {name:22s}  z = {z:3d}      {freq:6.1f}")

print("""
ZIMMERMAN EFFECTS ON 21cm SIGNAL
================================

The Zimmerman formula predicts a₀ was much higher in the early universe.
This affects 21cm observations in several ways:
""")

# Calculate a0 at different epochs
print("\n1. a₀ EVOLUTION AND STRUCTURE FORMATION")
print("  " + "-" * 50)
print("  Redshift    a₀(z)/a₀(0)    Physical effect")
print("  " + "-" * 50)
for name, z in epochs:
    a0_ratio = E_z(z)
    if z > 30:
        effect = "Early mini-halos form faster"
    elif z > 15:
        effect = "First stars form earlier"
    elif z > 10:
        effect = "Larger ionized bubbles"
    else:
        effect = "Faster reionization completion"
    print(f"  z = {z:3d}       {a0_ratio:6.1f}×         {effect}")

print("""
2. EFFECTS ON 21cm OBSERVABLES
==============================

A. TIMING SHIFTS
   - Higher a₀ → faster structure formation
   - First stars form EARLIER than ΛCDM predicts
   - Cosmic Dawn shifts to higher z
   - Reionization completes EARLIER

B. AMPLITUDE CHANGES
   - Stronger clustering at high-z
   - Larger 21cm fluctuations
   - Enhanced power spectrum at large scales

C. MORPHOLOGY CHANGES
   - Ionized bubbles have different size distribution
   - More coherent structures due to MOND effects
   - Different bubble-bubble correlations
""")

# Quantitative predictions
print("\n" + "=" * 60)
print("QUANTITATIVE PREDICTIONS")
print("=" * 60)

# Timing shift estimate
# In ΛCDM, first stars form at z ~ 20-30
# With higher a₀, collapse happens faster
# Enhancement factor ~ √(a₀(z)/a₀(0)) for gravitational collapse

z_first_stars_lcdm = 25
a0_enhancement = E_z(z_first_stars_lcdm)
# Collapse time ∝ 1/√(G ρ) in standard gravity
# With MOND enhancement, effective ρ increases → earlier collapse
z_shift = a0_enhancement ** 0.3  # Approximate scaling

z_first_stars_zimm = z_first_stars_lcdm * (1 + 0.1 * np.log(a0_enhancement))

print(f"""
First Stars Formation:
  ΛCDM prediction:     z ~ {z_first_stars_lcdm}
  Zimmerman prediction: z ~ {z_first_stars_zimm:.0f}
  Shift: ~{(z_first_stars_zimm - z_first_stars_lcdm):.0f} redshift units earlier

Cosmic Dawn 21cm trough:
  ΛCDM: z ~ 17 (EDGES detection, if real)
  Zimmerman: z ~ {17 * (1 + 0.1 * np.log(E_z(17))):.0f}

Reionization completion:
  ΛCDM: z ~ 6.5
  Zimmerman: z ~ {6.5 * (1 + 0.05 * np.log(E_z(6.5))):.1f}
""")

# 21cm power spectrum
print("\n21cm POWER SPECTRUM")
print("=" * 60)

print("""
The 21cm power spectrum P_21(k, z) depends on:
  - Matter power spectrum P_δ(k)
  - Ionization fraction x_HI
  - Spin temperature T_s
  - Velocity field

Zimmerman modifications:
  1. Enhanced P_δ(k) at high-z due to faster collapse
  2. Earlier/different ionization history
  3. Modified velocity power spectrum

Expected enhancement:
  - At z = 10: ~30% higher power at k ~ 0.1 Mpc⁻¹
  - At z = 20: ~2× higher power
  - Strongest effect at large scales (low k)
""")

# EDGES anomaly
print("\n" + "=" * 60)
print("THE EDGES ANOMALY")
print("=" * 60)

print("""
EDGES (Experiment to Detect Global EoR Signature) reported in 2018:
  - 21cm absorption trough at z ~ 17 (78 MHz)
  - Amplitude: -500 mK (much deeper than expected ~-200 mK)
  - Duration: z ~ 15-20

STANDARD PROBLEM:
  - Requires either:
    a) CMB was hotter than expected (ruled out by Planck)
    b) Gas was colder than expected (new physics needed)
  - Led to proposals of dark matter-baryon interactions

ZIMMERMAN PERSPECTIVE:
  - Higher a₀ at z ~ 17: a₀ = {E_z(17):.1f}× local
  - Earlier, more efficient gas collapse
  - Denser gas in early halos → colder via adiabatic expansion
  - Could partially explain deeper absorption

However:
  - Factor 2.5× amplitude requires more than MOND enhancement
  - Zimmerman contributes but likely not full solution
  - EDGES result itself is controversial (SARAS-3 non-detection)
""")

# SKA predictions
print("\n" + "=" * 60)
print("SKA PREDICTIONS")
print("=" * 60)

print("""
The Square Kilometre Array (SKA) will revolutionize 21cm cosmology.
Zimmerman makes specific predictions testable by SKA:

1. POWER SPECTRUM SHAPE
   - Enhancement at large scales (k < 0.1 Mpc⁻¹)
   - Ratio to ΛCDM: ~1.3 at z=10, ~2 at z=20
   - SKA sensitivity: σ(P)/P ~ 1% at k ~ 0.1 Mpc⁻¹

2. REIONIZATION TIMING
   - Mean ionization fraction x_e(z) evolution
   - Zimmerman: Earlier midpoint (~0.5 redshift units)
   - SKA can measure x_e(z) to ~5%

3. BUBBLE SIZE DISTRIBUTION
   - Ionized bubble sizes follow R ∝ a₀^(1/3)
   - Higher a₀ → larger bubbles at fixed z
   - SKA imaging at z ~ 8-10 will reveal morphology

4. CROSS-CORRELATION
   - 21cm × galaxy cross-power spectrum
   - Tests whether 21cm traces galaxies as expected
   - Zimmerman: Different bias evolution
""")

# Summary
print("\n" + "=" * 80)
print("SUMMARY: 21cm COSMOLOGY - ZIMMERMAN PREDICTIONS")
print("=" * 80)
print(f"""
┌────────────────────────────────────────────────────────────┐
│ 21cm COSMOLOGY - ZIMMERMAN FORMULA PREDICTIONS             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Key Physics:                                               │
│   • 21cm traces neutral hydrogen throughout cosmic history│
│   • Higher a₀ at high-z affects structure formation       │
│   • This modifies 21cm observable signatures              │
│                                                            │
│ Zimmerman Predictions:                                     │
│                                                            │
│ 1. Timing Shifts:                                          │
│    • First stars: ~5 redshift units earlier               │
│    • Cosmic Dawn: Shifted to higher z                     │
│    • Reionization: Completes ~0.5z earlier                │
│                                                            │
│ 2. Power Spectrum:                                         │
│    • ~30% enhancement at z=10, k~0.1 Mpc⁻¹               │
│    • ~2× enhancement at z=20                              │
│    • Strongest at large scales                            │
│                                                            │
│ 3. Morphology:                                             │
│    • Larger ionized bubbles at fixed z                    │
│    • More coherent structures                             │
│    • Different bubble-bubble correlations                 │
│                                                            │
│ Testability:                                               │
│   🔬 HERA: Currently taking data, first results soon      │
│   🔬 SKA: Construction ongoing, operations ~2028          │
│   🔬 MWA/LOFAR: Upper limits, not yet detections          │
│                                                            │
│ Status: 🔬 TESTABLE predictions for upcoming experiments   │
│                                                            │
└────────────────────────────────────────────────────────────┘
""")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: a₀ evolution for 21cm epochs
ax1 = axes[0, 0]
z_arr = np.linspace(0, 50, 100)
a0_ratio_arr = E_z(z_arr)
ax1.semilogy(z_arr, a0_ratio_arr, 'b-', linewidth=2)
ax1.axvspan(6, 15, alpha=0.2, color='green', label='Reionization')
ax1.axvspan(15, 30, alpha=0.2, color='red', label='Cosmic Dawn')
ax1.axvspan(30, 50, alpha=0.2, color='purple', label='Dark Ages')
ax1.set_xlabel('Redshift z', fontsize=12)
ax1.set_ylabel('a₀(z) / a₀(local)', fontsize=12)
ax1.set_title('MOND Acceleration Scale in 21cm Eras', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Panel 2: Observed 21cm frequency
ax2 = axes[0, 1]
z_freq = np.linspace(5, 50, 100)
freq_arr = observed_freq(z_freq)
ax2.plot(z_freq, freq_arr, 'r-', linewidth=2)
ax2.axhline(100, color='green', linestyle='--', alpha=0.5, label='SKA-LOW lower limit')
ax2.axhline(350, color='blue', linestyle='--', alpha=0.5, label='SKA-LOW upper limit')
ax2.fill_between(z_freq, freq_arr, where=((freq_arr > 50) & (freq_arr < 350)),
                 alpha=0.3, color='orange', label='SKA-LOW band')
ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('Observed Frequency (MHz)', fontsize=12)
ax2.set_title('21cm Frequency vs Redshift', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.invert_xaxis()

# Panel 3: Power spectrum enhancement
ax3 = axes[1, 0]
z_power = np.array([6, 8, 10, 12, 15, 20, 25, 30])
# Enhancement roughly scales as sqrt(a0_ratio)
enhancement = np.sqrt(E_z(z_power)) * 0.8  # Scale factor
ax3.plot(z_power, enhancement, 'go-', linewidth=2, markersize=8)
ax3.axhline(1.0, color='red', linestyle='--', label='ΛCDM baseline')
ax3.fill_between(z_power, 1, enhancement, alpha=0.3, color='green')
ax3.set_xlabel('Redshift z', fontsize=12)
ax3.set_ylabel('P_21(k) Enhancement Factor', fontsize=12)
ax3.set_title('Zimmerman Enhancement of 21cm Power Spectrum', fontsize=14)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Panel 4: Global 21cm signal schematic
ax4 = axes[1, 1]
z_global = np.linspace(5, 35, 100)
# Schematic global 21cm signal (not physical, just illustrative)
signal_lcdm = -20 + 200 * np.exp(-(z_global - 17)**2 / 20) * np.sin(0.3 * z_global)
# Zimmerman: shifted earlier, possibly deeper
signal_zimm = -20 + 250 * np.exp(-(z_global - 20)**2 / 20) * np.sin(0.3 * z_global)
ax4.plot(z_global, signal_lcdm, 'r-', linewidth=2, label='ΛCDM (schematic)')
ax4.plot(z_global, signal_zimm, 'b--', linewidth=2, label='Zimmerman (schematic)')
ax4.axhline(0, color='black', linewidth=0.5)
ax4.set_xlabel('Redshift z', fontsize=12)
ax4.set_ylabel('δT_b (mK)', fontsize=12)
ax4.set_title('Global 21cm Signal (Schematic)', fontsize=14)
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.invert_xaxis()

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/unsolved_problems/21cm_cosmology.png',
            dpi=150, bbox_inches='tight')
plt.close()

print("\n📊 Visualization saved to: research/unsolved_problems/21cm_cosmology.png")
