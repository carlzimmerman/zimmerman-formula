#!/usr/bin/env python3
"""
PROPOSED OBSERVATIONAL TEST: BTF Evolution with Redshift

This is the cleanest way to falsify/confirm the Zimmerman formula.

Prediction: BTFR zero-point shifts by -0.48 dex at z=2
            (galaxies appear 3x less massive for same velocity)

If this is NOT observed -> Zimmerman formula FALSIFIED
If this IS observed -> Strong confirmation
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
c = 2.998e8
G = 6.674e-11
M_sun = 1.989e30
Omega_m = 0.315
Omega_Lambda = 0.685

print("=" * 70)
print("PROPOSED TEST: BARYONIC TULLY-FISHER EVOLUTION")
print("=" * 70)
print()

def E_z(z):
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def btf_zero_point_shift(z):
    """Log shift in BTF zero-point at redshift z"""
    return -np.log10(E_z(z))

# ============================================================================
# THE PREDICTION
# ============================================================================

print("THE ZIMMERMAN PREDICTION")
print("-" * 50)
print()
print("Standard BTFR: M_bar = v^4 / (G * a0)")
print()
print("At redshift z, a0(z) = a0(0) * E(z)")
print()
print("So: M_bar(z) = v^4 / (G * a0 * E(z))")
print("            = M_bar(0) / E(z)")
print()
print("In magnitudes: Delta_log(M) = -log10(E(z))")
print()

redshifts = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
print(f"{'z':<10} {'E(z)':<15} {'Zero-point shift':<20} {'Mass ratio':<15}")
print("-" * 60)
for z in redshifts:
    Ez = E_z(z)
    shift = btf_zero_point_shift(z)
    ratio = 1/Ez
    print(f"{z:<10} {Ez:<15.2f} {shift:<20.2f} dex {ratio:<15.2f}")

print()

# ============================================================================
# WHAT OBSERVERS SHOULD MEASURE
# ============================================================================

print("=" * 70)
print("OBSERVATIONAL REQUIREMENTS")
print("=" * 70)
print()

print("TARGET SAMPLE:")
print("  - 20-50 disk galaxies at z ~ 2")
print("  - Must have: rotation velocity (ALMA CO, [CII]; JWST Halpha)")
print("  - Must have: stellar mass (SED fitting)")
print("  - Must have: gas mass (CO observations)")
print()

print("MEASURED QUANTITIES:")
print("  - v_flat or v_2.2 (rotation velocity at 2.2 disk scale lengths)")
print("  - M_* (stellar mass from photometry)")
print("  - M_gas (from CO luminosity or [CII])")
print("  - M_bar = M_* + 1.33 * M_gas")
print()

print("EXISTING DATA SOURCES:")
print("  - KMOS3D (VLT): z = 0.6-2.7, ~600 galaxies")
print("  - SINS/zC-SINF: z ~ 2, ~100 galaxies")
print("  - ALMA: CO observations at z ~ 1-3")
print("  - JWST NIRSpec: Halpha at z > 2")
print()

# ============================================================================
# DISTINGUISHING PREDICTIONS
# ============================================================================

print("=" * 70)
print("DISTINGUISHING PREDICTIONS")
print("=" * 70)
print()

print("At z = 2:")
print()
print("  ZIMMERMAN PREDICTION:")
print("    Zero-point shift = -0.48 dex")
print("    At fixed v_flat, inferred M_bar is 3x LOWER")
print()
print("  CONSTANT MOND:")
print("    Zero-point shift = 0")
print("    No evolution")
print()
print("  LAMBDA-CDM (no MOND):")
print("    No specific prediction for BTF")
print("    Scatter expected to be large")
print()

# ============================================================================
# STATISTICAL REQUIREMENTS
# ============================================================================

print("=" * 70)
print("STATISTICAL REQUIREMENTS")
print("=" * 70)
print()

# Typical scatter in local BTF is 0.1 dex
local_scatter = 0.1  # dex
predicted_shift = 0.48  # dex at z=2

# To detect at 5 sigma
sigma_required = predicted_shift / 5
n_galaxies_required = (local_scatter / sigma_required)**2

print(f"Local BTF scatter: {local_scatter} dex")
print(f"Predicted shift at z=2: {predicted_shift} dex")
print()
print(f"To detect at 5 sigma: need {sigma_required:.2f} dex precision")
print(f"Required sample size: N > {n_galaxies_required:.0f} galaxies")
print()
print("Current samples:")
print("  - KMOS3D has ~100 galaxies at z~2 with rotation curves")
print("  - This is SUFFICIENT to test the prediction!")
print()

# ============================================================================
# POTENTIAL COMPLICATIONS
# ============================================================================

print("=" * 70)
print("POTENTIAL COMPLICATIONS")
print("=" * 70)
print()

print("1. SELECTION EFFECTS")
print("   - High-z samples biased toward massive, star-forming galaxies")
print("   - Solution: Match z~0 sample to same mass/SFR range")
print()

print("2. MEASUREMENT SYSTEMATICS")
print("   - v_flat harder to measure at high-z (beam smearing)")
print("   - Solution: Use consistent v_2.2 or asymptotic velocity")
print()

print("3. GAS FRACTION EVOLUTION")
print("   - High-z galaxies are more gas-rich")
print("   - Solution: Include gas mass in M_bar (this is standard)")
print()

print("4. IMF VARIATION")
print("   - If IMF varies with redshift, M_* estimates affected")
print("   - Solution: Use multiple M_* estimators, check consistency")
print()

# ============================================================================
# PROPOSED OBSERVATION
# ============================================================================

print("=" * 70)
print("PROPOSED OBSERVATION")
print("=" * 70)
print()

print("TITLE: Testing Cosmological MOND with the Tully-Fisher Relation at z~2")
print()
print("ABSTRACT:")
print("The Zimmerman formula (a0 = cH0/5.79) predicts that the MOND")
print("acceleration scale evolves with redshift. This leads to a")
print("specific, falsifiable prediction: the Baryonic Tully-Fisher")
print("relation zero-point should shift by -0.48 dex at z=2.")
print("We propose to test this using existing KMOS3D and ALMA data")
print("combined with new JWST NIRSpec observations.")
print()

print("TELESCOPE/INSTRUMENT:")
print("  - JWST NIRSpec IFU (Halpha rotation curves)")
print("  - ALMA (CO for gas masses)")
print("  - Existing: KMOS3D, SINS, 3D-HST")
print()

print("SAMPLE REQUIREMENTS:")
print("  - 50 disk galaxies at 1.5 < z < 2.5")
print("  - log(M_*) > 9.5")
print("  - Inclination > 30 degrees")
print("  - Clear rotation signature")
print()

print("EXPECTED OUTCOME:")
print("  - If shift = -0.48 +/- 0.1 dex: ZIMMERMAN CONFIRMED")
print("  - If shift = 0.0 +/- 0.1 dex: ZIMMERMAN FALSIFIED")
print("  - Intermediate: Partial evolution, modified formula needed")
print()

# ============================================================================
# VISUALIZATION
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: BTF at different redshifts
ax1 = axes[0]

log_v = np.linspace(1.5, 2.8, 50)  # log10(v in km/s)
v = 10**log_v * 1000  # m/s
a0 = 1.2e-10

# Local BTF
M_local = v**4 / (G * a0)
log_M_local = np.log10(M_local / M_sun)

z_values = [0, 1, 2, 3]
colors = ['black', 'blue', 'red', 'purple']

for z, color in zip(z_values, colors):
    shift = btf_zero_point_shift(z)
    log_M_z = log_M_local + shift
    ax1.plot(log_v, log_M_z, color=color, linewidth=2, label=f'z = {z}')

ax1.set_xlabel('log(v_flat / km/s)', fontsize=12)
ax1.set_ylabel('log(M_bar / M_sun)', fontsize=12)
ax1.set_title('Zimmerman Prediction: BTF Evolution', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Zero-point shift vs redshift
ax2 = axes[1]

z_range = np.linspace(0, 4, 100)
shifts = [btf_zero_point_shift(z) for z in z_range]

ax2.plot(z_range, shifts, 'b-', linewidth=2, label='Zimmerman')
ax2.axhline(y=0, color='gray', linestyle='--', label='No evolution (constant a0)')

# Mark key redshifts
key_z = [1, 2, 3]
for z in key_z:
    shift = btf_zero_point_shift(z)
    ax2.plot(z, shift, 'ro', markersize=10)
    ax2.annotate(f'z={z}: {shift:.2f} dex', (z, shift),
                 textcoords='offset points', xytext=(10, 10))

ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('BTF Zero-point Shift (dex)', fontsize=12)
ax2.set_title('Testable Prediction', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 4)
ax2.set_ylim(-1, 0.2)

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(output_dir, 'output'), exist_ok=True)
plt.savefig(os.path.join(output_dir, 'output', 'btf_evolution_test.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print("=" * 70)
print("OUTPUT: output/btf_evolution_test.png")
print("=" * 70)
print()
print("THIS IS A CLEAN, FALSIFIABLE TEST.")
print("The data largely exists - it just needs to be analyzed")
print("with this specific prediction in mind.")
print("=" * 70)
