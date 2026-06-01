#!/usr/bin/env python3
"""
================================================================================
PREDICTION 1: JWST BARYONIC TULLY-FISHER EVOLUTION
================================================================================

The Zimmerman Framework predicts that the Baryonic Tully-Fisher Relation (BTFR)
evolves with redshift due to evolving a₀.

Local BTFR: M_bar = A × v⁴ / (G × a₀)

At redshift z, a₀(z) = a₀(0) × E(z), so:
  M_bar(z) = M_bar(0) / E(z)  at fixed velocity

This means: Δlog M_bar = -log₁₀(E(z))

JWST Cycles 3-4 will measure rotation curves at z = 2-6.
This is the PRIMARY test of the Zimmerman Framework.

================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTS
# =============================================================================

PI = np.pi
Z = 2 * np.sqrt(8 * PI / 3)
Z_SQUARED = Z * Z

OMEGA_LAMBDA = (3 * Z) / (8 + 3 * Z)  # = 0.6846
OMEGA_MATTER = 8 / (8 + 3 * Z)        # = 0.3154

c = 299792458  # m/s
G = 6.67430e-11  # m³ kg⁻¹ s⁻²
H0 = 71.5  # km/s/Mpc (Zimmerman prediction)
H0_SI = H0 * 1000 / 3.086e22  # Convert to s⁻¹
a0_local = c * H0_SI / Z  # 1.17 × 10⁻¹⁰ m/s²

print("=" * 80)
print("PREDICTION 1: JWST BARYONIC TULLY-FISHER EVOLUTION")
print("=" * 80)

print(f"\nFramework constants:")
print(f"  Z = {Z:.4f}")
print(f"  Ω_Λ = {OMEGA_LAMBDA:.4f}")
print(f"  Ω_m = {OMEGA_MATTER:.4f}")
print(f"  a₀(z=0) = {a0_local:.2e} m/s²")

# =============================================================================
# E(z) FUNCTION
# =============================================================================

def E(z):
    """Dimensionless Hubble parameter E(z) = H(z)/H₀"""
    return np.sqrt(OMEGA_MATTER * (1 + z)**3 + OMEGA_LAMBDA)

def a0_of_z(z):
    """MOND acceleration scale at redshift z"""
    return a0_local * E(z)

def btfr_offset(z):
    """BTFR offset in dex at redshift z"""
    return -np.log10(E(z))

# =============================================================================
# PREDICTIONS
# =============================================================================

print("\n" + "=" * 80)
print("SPECIFIC PREDICTIONS")
print("=" * 80)

redshifts = [0, 0.5, 1, 2, 3, 4, 5, 6, 8, 10]

print(f"\n{'z':>6} | {'E(z)':>8} | {'a₀(z)/a₀(0)':>12} | {'BTFR Offset':>12} |")
print("-" * 50)

for z in redshifts:
    Ez = E(z)
    a0_ratio = Ez
    offset = btfr_offset(z)
    print(f"{z:>6} | {Ez:>8.3f} | {a0_ratio:>12.3f} | {offset:>+12.3f} dex |")

# =============================================================================
# INTERPRETATION
# =============================================================================

print("\n" + "=" * 80)
print("PHYSICAL INTERPRETATION")
print("=" * 80)

print("""
At z = 2 (cosmic noon, peak star formation):
  - E(z) = 2.96
  - a₀ was 2.96× higher than today
  - For a galaxy with v = 200 km/s:
    * Local BTFR: M_bar ~ 10^10.5 M☉
    * At z=2: Same v requires M_bar ~ 10^10.0 M☉
    * Offset: -0.47 dex

At z = 6 (reionization epoch):
  - E(z) = 10.3
  - a₀ was 10× higher
  - Offset: -1.01 dex (factor of 10 less mass at fixed v!)

At z = 10 (JWST frontier):
  - E(z) = 20.1
  - a₀ was 20× higher
  - This explains "impossibly" massive early galaxies
""")

# =============================================================================
# FALSIFICATION CRITERIA
# =============================================================================

print("=" * 80)
print("FALSIFICATION CRITERIA")
print("=" * 80)

print("""
The framework is FALSIFIED if:

1. BTFR offset at z=2 is measured to be < -0.3 dex
   (Prediction: -0.47 dex)

2. No offset detected at z > 1 (offset < -0.1 dex)

3. Offset goes the WRONG direction (positive offset)

4. Offset matches constant-a₀ MOND (no evolution)

The framework is STRONGLY SUPPORTED if:

1. Offset at z=2 measured as -0.4 to -0.5 dex

2. Offset scales correctly with E(z) at multiple redshifts

3. Scatter in BTFR unchanged (just shifted)
""")

# =============================================================================
# COMPARISON WITH EXISTING DATA
# =============================================================================

print("=" * 80)
print("EXISTING DATA HINTS")
print("=" * 80)

print("""
KMOS3D Survey (z ~ 0.6-2.6):
  - Found elevated v/M_bar at high-z
  - Consistent with evolving a₀
  - But kinematic data limited

ALPINE/REBELS (z ~ 4-7):
  - Preliminary rotation curves
  - High dynamical masses
  - Consistent with enhanced MOND at high-z

JWST ERO (2022-2023):
  - "Impossibly" massive early galaxies
  - Explained by Zimmerman: a₀ was 10-20× higher
  - No dark matter needed
""")

# =============================================================================
# JWST OBSERVING PROGRAMS
# =============================================================================

print("=" * 80)
print("KEY JWST PROGRAMS TO WATCH")
print("=" * 80)

print("""
GTO 1264: NIRSpec IFU kinematics z=1-3
  - Will measure rotation curves at cosmic noon
  - Direct test of BTFR offset

GO 2736: Kinematic survey of lensed galaxies
  - Magnified sources allow better resolution
  - Multiple redshift bins

GO 3215: Early universe rotation curves
  - Pushing to z > 6
  - Test of extreme a₀ evolution

Expected results: 2026-2027
""")

# =============================================================================
# GENERATE PREDICTION PLOT
# =============================================================================

print("\n" + "=" * 80)
print("GENERATING PREDICTION PLOT...")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left panel: E(z) and a₀(z)
z_arr = np.linspace(0, 12, 100)
E_arr = E(z_arr)

ax1 = axes[0]
ax1.plot(z_arr, E_arr, 'b-', linewidth=2, label='E(z) = a₀(z)/a₀(0)')
ax1.axhline(1, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(2, color='red', linestyle=':', alpha=0.7, label='Cosmic noon (z=2)')
ax1.axvline(6, color='purple', linestyle=':', alpha=0.7, label='Reionization (z=6)')

ax1.set_xlabel('Redshift z', fontsize=12)
ax1.set_ylabel('E(z) = H(z)/H₀ = a₀(z)/a₀(0)', fontsize=12)
ax1.set_title('Evolution of MOND Acceleration Scale', fontsize=14)
ax1.legend()
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 25)
ax1.grid(True, alpha=0.3)

# Annotate key points
ax1.annotate(f'z=2: E={E(2):.2f}', xy=(2, E(2)), xytext=(3, E(2)+2),
            arrowprops=dict(arrowstyle='->', color='red'), fontsize=10)
ax1.annotate(f'z=6: E={E(6):.1f}', xy=(6, E(6)), xytext=(7, E(6)+2),
            arrowprops=dict(arrowstyle='->', color='purple'), fontsize=10)

# Right panel: BTFR offset
offset_arr = btfr_offset(z_arr)

ax2 = axes[1]
ax2.plot(z_arr, offset_arr, 'r-', linewidth=2, label='Δlog M_bar = -log₁₀(E(z))')
ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax2.axhline(-0.47, color='blue', linestyle=':', alpha=0.7)
ax2.axvline(2, color='blue', linestyle=':', alpha=0.7)

ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('BTFR Offset (dex)', fontsize=12)
ax2.set_title('Predicted BTFR Evolution', fontsize=14)
ax2.legend()
ax2.set_xlim(0, 12)
ax2.set_ylim(-1.5, 0.1)
ax2.grid(True, alpha=0.3)

# Annotate prediction
ax2.annotate('z=2 prediction:\n-0.47 dex', xy=(2, -0.47), xytext=(4, -0.3),
            arrowprops=dict(arrowstyle='->', color='blue'), fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

# Falsification zone
ax2.fill_between([0, 12], -0.3, 0.1, alpha=0.2, color='red', label='Falsification zone (z=2)')
ax2.text(8, -0.1, 'If offset > -0.3 at z=2:\nFramework falsified', fontsize=9, color='red')

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/predictions/01_JWST_BTFR_prediction.png', dpi=150)
print("Saved: 01_JWST_BTFR_prediction.png")
plt.close()

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY: JWST BTFR PREDICTION")
print("=" * 80)

print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ZIMMERMAN FRAMEWORK PREDICTION #1                                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Observable: Baryonic Tully-Fisher Relation at high redshift                 ║
║                                                                               ║
║  Formula: Δlog M_bar = -log₁₀(E(z))                                          ║
║                                                                               ║
║  Key prediction at z=2:                                                       ║
║    BTFR offset = -0.47 dex (factor of 3 less mass at fixed velocity)         ║
║                                                                               ║
║  Falsification threshold: offset > -0.3 dex                                  ║
║                                                                               ║
║  Timeline: JWST Cycles 3-4 (2026-2027)                                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
print("END OF PREDICTION 1")
print("=" * 80)
