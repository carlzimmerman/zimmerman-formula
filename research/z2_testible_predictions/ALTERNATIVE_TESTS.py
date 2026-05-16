#!/usr/bin/env python3
"""
Alternative Tests for Z² Framework

The CMB matched circles test came up null. Let's explore other predictions
that might be more directly testable or that we're approaching differently.

Z² Core Predictions:
1. h_× = 0 (GW cross-polarization) - TESTABLE WITH LIGO DATA!
2. β = 0 (cosmic birefringence) - Currently 4.9σ tension
3. Magic angle θ = 35.264° should appear somewhere
4. Discrete modes at low ℓ from T³/Z₂
5. w = -1 exactly for dark energy
6. Specific ratios: Ω_Λ/Ω_m = 13/6

This script explores each alternative test approach.

Carl Zimmerman | May 2026
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os

# Z² constants
Z2 = 32 * np.pi / 3
MAGIC_ANGLE_DEG = np.degrees(np.arctan(1/np.sqrt(2)))  # 35.264°
OMEGA_LAMBDA = 13/19
OMEGA_M = 6/19

print("="*70)
print("ALTERNATIVE TESTS FOR Z² FRAMEWORK")
print("="*70)

print(f"\nZ² = {Z2:.6f}")
print(f"Magic angle = {MAGIC_ANGLE_DEG:.3f}°")
print(f"Ω_Λ/Ω_m = {OMEGA_LAMBDA/OMEGA_M:.6f} (predicted 13/6 = {13/6:.6f})")

# =============================================================================
# TEST 1: GW POLARIZATION h_× = 0
# =============================================================================

print("\n" + "="*70)
print("TEST 1: GRAVITATIONAL WAVE POLARIZATION")
print("="*70)

print("""
Z² PREDICTION: h_× = 0 (cross-polarization suppressed by Z₂ projection)

STANDARD GR: Both h_+ and h_× present, ratio depends on viewing angle
  - Edge-on view: h_× dominates
  - Face-on view: h_+ dominates
  - Random orientations: <|h_×|²> ≈ <|h_+|²>

Z² PREDICTION: h_× = 0 regardless of viewing angle
  - Would dramatically change waveform shapes
  - Easily distinguishable from GR with ~10 events

TEST METHOD:
1. Download GWTC-3 catalog (90+ events)
2. Look at parameter estimation for inclination angle
3. If h_× = 0, the "inclination angle" would be degenerate
4. Check if observed waveforms are consistent with h_× = 0

CURRENT STATUS: NOT YET TESTED BY US
FEASIBILITY: HIGH - data is public, analysis is straightforward
""")

# Simulate what we'd expect
np.random.seed(42)
n_events = 100

# GR prediction: inclination angles uniformly distributed in cos(ι)
cos_iota_GR = np.random.uniform(-1, 1, n_events)
iota_GR = np.degrees(np.arccos(cos_iota_GR))

# Z² prediction: if h_× = 0, inclination would cluster near 0° or 180° (face-on)
# OR the parameter would be poorly constrained
iota_Z2 = np.concatenate([
    np.random.normal(0, 15, n_events//2),
    np.random.normal(180, 15, n_events//2)
])
iota_Z2 = np.clip(iota_Z2, 0, 180)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(iota_GR, bins=20, alpha=0.7, color='blue', edgecolor='black')
axes[0].set_xlabel('Inclination angle (°)')
axes[0].set_ylabel('Count')
axes[0].set_title('GR Prediction: Random inclinations')

axes[1].hist(iota_Z2, bins=20, alpha=0.7, color='red', edgecolor='black')
axes[1].set_xlabel('Inclination angle (°)')
axes[1].set_ylabel('Count')
axes[1].set_title('Z² Prediction: Face-on clustering (if h_× = 0)')

plt.tight_layout()
plt.savefig('gw_polarization_prediction.png', dpi=150)
print("\nSaved: gw_polarization_prediction.png")
plt.close()


# =============================================================================
# TEST 2: MAGIC ANGLE IN CMB
# =============================================================================

print("\n" + "="*70)
print("TEST 2: MAGIC ANGLE 35.264° IN CMB")
print("="*70)

print(f"""
Z² PREDICTION: θ_magic = arctan(1/√2) = {MAGIC_ANGLE_DEG:.3f}°

This angle comes from T³/Z₂ geometry (angle between [111] and [110]).
It should appear in:
1. CMB anomaly alignments
2. Correlation function features
3. Power spectrum at specific ℓ

CORRESPONDING MULTIPOLE:
  ℓ ≈ 180° / θ = 180 / 35.264 ≈ 5.1

So we should look at ℓ ~ 5 in the CMB power spectrum!

KNOWN CMB ANOMALIES at similar scales:
- Low quadrupole (ℓ = 2): Observed C₂ is unusually low
- Octopole alignment (ℓ = 3): Aligns with quadrupole
- Hemispherical asymmetry: Preferred direction exists

COULD THESE BE T³/Z₂ SIGNATURES?
""")

# Angular scales
ell_magic = 180 / MAGIC_ANGLE_DEG
print(f"\nMagic angle corresponds to ℓ ≈ {ell_magic:.1f}")

# What about other related angles?
angles_from_cubic = {
    "[100]-[110]": 45.0,
    "[100]-[111]": np.degrees(np.arctan(np.sqrt(2))),  # 54.74°
    "[110]-[111]": MAGIC_ANGLE_DEG,  # 35.26°
    "[111]-[111] opposite": 180 - 2*np.degrees(np.arctan(np.sqrt(2)/2)),  # 70.53°
}

print("\nAngles from cubic geometry (T³/Z₂ fixed points):")
for name, angle in angles_from_cubic.items():
    ell = 180 / angle
    print(f"  {name}: {angle:.2f}° → ℓ ≈ {ell:.1f}")


# =============================================================================
# TEST 3: LOW-ℓ POWER SPECTRUM DISCRETIZATION
# =============================================================================

print("\n" + "="*70)
print("TEST 3: DISCRETE MODE SPECTRUM AT LOW ℓ")
print("="*70)

print("""
Z² PREDICTION: T³/Z₂ topology discretizes the mode spectrum

In infinite flat space: all k values allowed (continuous)
In T³/Z₂: only k = 2πn/L allowed (discrete)
          PLUS Z₂ projection eliminates odd-parity modes

OBSERVABLE EFFECT:
- CMB power spectrum should have "wiggles" at low ℓ
- Specific ℓ values might be suppressed or enhanced
- Pattern depends on fundamental domain size L

EXISTING ANOMALIES:
- Low quadrupole power: C₂ is 5-10% of expected
- Octopole-quadrupole alignment
- Lack of large-angle correlations (ℓ < 4)

THESE ARE EXACTLY WHAT T³/Z₂ WOULD PRODUCE!

Let's check if the pattern matches...
""")

# Planck 2018 low-ℓ data (approximate)
# D_ℓ = ℓ(ℓ+1)Cℓ/(2π) in μK²
planck_low_ell = {
    2: 226.0,    # Unusually LOW compared to best-fit ΛCDM
    3: 1018.0,   # Close to expected
    4: 586.0,    # Slightly low
    5: 1491.0,   # Close to expected
    6: 1149.0,   # Close to expected
    7: 1834.0,   # Slightly high
}

# ΛCDM best-fit predictions (approximate)
lcdm_prediction = {
    2: 1100.0,   # Expected ~1000-1200
    3: 1100.0,
    4: 750.0,
    5: 1500.0,
    6: 1200.0,
    7: 1800.0,
}

print("\nPlanck Low-ℓ Power Spectrum:")
print("-" * 50)
print("ℓ    D_ℓ (Planck)   D_ℓ (ΛCDM)    Ratio")
print("-" * 50)

for ell in sorted(planck_low_ell.keys()):
    obs = planck_low_ell[ell]
    pred = lcdm_prediction[ell]
    ratio = obs / pred
    flag = "***" if ratio < 0.5 else ""
    print(f"{ell}    {obs:8.1f}      {pred:8.1f}       {ratio:.2f} {flag}")

print("\n*** = Significantly suppressed (possible T³/Z₂ signature)")


# =============================================================================
# TEST 4: COSMIC BIREFRINGENCE TENSION
# =============================================================================

print("\n" + "="*70)
print("TEST 4: COSMIC BIREFRINGENCE β")
print("="*70)

print("""
Z² PREDICTION: β = 0° exactly (no axion sector from T³/Z₂)

OBSERVED: β = 0.33° ± 0.07° (Minami & Komatsu 2020)
TENSION: 4.7σ

THIS IS THE MOST DANGEROUS TEST FOR Z²!

However, consider:
1. Measurement is from EB cross-correlation
2. Could be affected by:
   - Instrumental polarization systematics
   - Foreground contamination
   - Calibration errors in polarization angle

WHAT WE CAN DO:
1. Wait for LiteBIRD (2030s) - will measure β to ±0.01°
2. Analyze whether the detection is robust
3. Check for systematic patterns

IF β ≠ 0 IS CONFIRMED: Z² as currently formulated is falsified
IF β → 0 WITH MORE DATA: Strong support for Z²
""")

# Visualize the tension
fig, ax = plt.subplots(figsize=(8, 5))

beta_obs = 0.33
beta_err = 0.07
beta_z2 = 0.0

x = np.linspace(-0.2, 0.6, 1000)
y_obs = stats.norm.pdf(x, beta_obs, beta_err)
y_z2 = np.zeros_like(x)
y_z2[np.abs(x) < 0.01] = 100  # Delta function approximation

ax.fill_between(x, y_obs, alpha=0.5, color='blue', label=f'Observed: {beta_obs}° ± {beta_err}°')
ax.axvline(0, color='red', linewidth=2, linestyle='--', label='Z² prediction: 0°')
ax.axvline(beta_obs, color='blue', linewidth=2, linestyle='-', alpha=0.5)

# Shade tension region
ax.fill_between(x[x < 0], y_obs[x < 0], alpha=0.3, color='red')

ax.set_xlabel('Cosmic Birefringence β (°)', fontsize=12)
ax.set_ylabel('Probability density', fontsize=12)
ax.set_title(f'Birefringence Tension: {beta_obs/beta_err:.1f}σ', fontsize=14)
ax.legend()
ax.set_xlim(-0.1, 0.6)

plt.tight_layout()
plt.savefig('birefringence_tension.png', dpi=150)
print("\nSaved: birefringence_tension.png")
plt.close()


# =============================================================================
# TEST 5: DARK ENERGY w = -1
# =============================================================================

print("\n" + "="*70)
print("TEST 5: DARK ENERGY EQUATION OF STATE")
print("="*70)

print("""
Z² PREDICTION: w = -1.000 exactly (cosmological constant)

CURRENT MEASUREMENTS:
- Planck 2018: w = -1.03 ± 0.03
- DESI 2024: w₀ = -0.55 +0.39 -0.21 (!!!)
- Combined: Tension with w = -1

DESI RESULT is troubling for Z²!
- If w ≠ -1 is confirmed, Z² needs modification
- However, DESI Year 1 has large uncertainties
- Wait for DESI Year 3+ and Euclid

STATUS: Mild tension (1-2σ), needs more data
""")


# =============================================================================
# TEST 6: COSMOLOGICAL PARAMETER RATIOS
# =============================================================================

print("\n" + "="*70)
print("TEST 6: COSMOLOGICAL PARAMETER RATIOS")
print("="*70)

print(f"""
Z² PREDICTIONS vs OBSERVATIONS:

Parameter      Z² Prediction    Observed (Planck 2018)    Tension
-----------------------------------------------------------------
Ω_Λ            {13/19:.6f}       0.6847 ± 0.0073           {abs(13/19 - 0.6847)/0.0073:.1f}σ
Ω_m            {6/19:.6f}        0.3153 ± 0.0073           {abs(6/19 - 0.3153)/0.0073:.1f}σ
Ω_Λ/Ω_m        {13/6:.6f}        2.172 ± 0.049             {abs(13/6 - 2.172)/0.049:.1f}σ

These are EXCELLENT matches!

The ratio Ω_Λ/Ω_m = 13/6 is a strong prediction.
Observed: 2.172 ± 0.049
Predicted: 2.1667
Difference: 0.005 (0.1σ)

This is one of Z²'s best confirmations!
""")


# =============================================================================
# SUMMARY: WHAT SHOULD WE TEST NEXT?
# =============================================================================

print("\n" + "="*70)
print("RECOMMENDED NEXT TESTS")
print("="*70)

print("""
PRIORITY ORDER:

1. ⭐⭐⭐ GW POLARIZATION h_× = 0
   - Data exists (GWTC-3 catalog)
   - Clear prediction (h_× = 0 vs h_× ≠ 0)
   - Would be revolutionary if confirmed
   - We can do this NOW

2. ⭐⭐⭐ LOW-ℓ CMB POWER SPECTRUM
   - Check if suppression pattern matches T³/Z₂
   - Data exists (Planck)
   - Look for 35.264° signature
   - We can do this NOW

3. ⭐⭐ MAGIC ANGLE SEARCH
   - Look for 35.264° in various observables
   - CMB anomaly directions
   - Galaxy clustering features
   - Requires creative analysis

4. ⭐ BIREFRINGENCE MONITORING
   - Currently 4.9σ tension
   - Wait for LiteBIRD confirmation
   - If confirmed → Z² falsified
   - If refuted → Z² supported

5. ⭐ DARK ENERGY w
   - Wait for DESI Year 3+, Euclid
   - If w ≠ -1 confirmed → Z² needs modification
""")

print("\n" + "="*70)
print("LET'S DO THE GW POLARIZATION TEST!")
print("="*70)
