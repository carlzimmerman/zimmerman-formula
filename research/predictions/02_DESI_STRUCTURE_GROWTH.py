#!/usr/bin/env python3
"""
================================================================================
PREDICTION 2: DESI STRUCTURE GROWTH
================================================================================

DESI Year 3 data (2026) will measure structure growth via BAO + RSD.

The Zimmerman Framework predicts:
  - Evolving a₀(z) affects structure formation
  - S8 tension should show redshift dependence
  - Structure growth enhanced at high-z relative to ΛCDM

================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTS
# =============================================================================

PI = np.pi
Z = 2 * np.sqrt(8 * PI / 3)
OMEGA_LAMBDA = (3 * Z) / (8 + 3 * Z)  # = 0.6846
OMEGA_MATTER = 8 / (8 + 3 * Z)        # = 0.3154

print("=" * 80)
print("PREDICTION 2: DESI STRUCTURE GROWTH")
print("=" * 80)

# =============================================================================
# S8 TENSION
# =============================================================================

print(f"""
THE S8 TENSION:

S8 = σ₈ × (Ω_m/0.3)^0.5 measures structure amplitude.

Measurements:
  - Planck CMB (z~1100): S8 = 0.832 ± 0.013
  - DES Y3 weak lensing (z~0.5): S8 = 0.776 ± 0.017
  - KiDS-1000 (z~0.5): S8 = 0.759 ± 0.021

Tension: ~2-3σ between CMB and low-z measurements

Zimmerman explanation:
  - a₀(z) = a₀(0) × E(z) affects structure growth
  - Higher a₀ at high-z enhances MONDian effects
  - Structure forms faster at high-z, appears as higher S8
  - Low-z measurements see lower effective S8
""")

# =============================================================================
# PREDICTIONS
# =============================================================================

def E(z):
    return np.sqrt(OMEGA_MATTER * (1 + z)**3 + OMEGA_LAMBDA)

print("\n" + "=" * 80)
print("PREDICTIONS FOR DESI YEAR 3")
print("=" * 80)

print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  STRUCTURE GROWTH PREDICTIONS                                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  1. S8 tension should persist between CMB and low-z                          ║
║                                                                               ║
║  2. S8 measurements should show REDSHIFT DEPENDENCE                          ║
║     - Higher S8 at higher z                                                  ║
║     - Roughly: ΔS8/S8 ∝ log(E(z))                                            ║
║                                                                               ║
║  3. Growth rate f(z)σ₈(z) measurements:                                       ║
║     - Should deviate from ΛCDM at z > 1                                      ║
║     - Enhanced growth at high-z due to stronger MOND                         ║
║                                                                               ║
║  Falsification:                                                               ║
║     - S8 tension resolves with no z-dependence                               ║
║     - Structure growth matches ΛCDM exactly                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# E(z) AT DESI REDSHIFTS
# =============================================================================

print("\nE(z) at DESI redshifts:")
for z in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
    print(f"  z = {z:.1f}: E(z) = {E(z):.3f}")

# =============================================================================
# GENERATE PLOT
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

# S8 measurements
data = [
    ('Planck CMB', 0.832, 0.013, 1100, 'blue'),
    ('ACT DR4', 0.840, 0.030, 1100, 'cyan'),
    ('SPT-3G', 0.797, 0.042, 1100, 'lightblue'),
    ('DES Y3', 0.776, 0.017, 0.5, 'green'),
    ('KiDS-1000', 0.759, 0.021, 0.5, 'lime'),
    ('HSC Y3', 0.769, 0.031, 0.8, 'orange'),
]

# Plot in order of redshift
x_pos = range(len(data))
colors = [d[4] for d in data]
values = [d[1] for d in data]
errors = [d[2] for d in data]
labels = [f"{d[0]}\n(z~{d[3]})" for d in data]

ax.errorbar(x_pos, values, yerr=errors, fmt='o', markersize=10,
            capsize=5, capthick=2, color='black')
for i, (x, v, c) in enumerate(zip(x_pos, values, colors)):
    ax.scatter(x, v, s=200, color=c, edgecolor='black', linewidth=2, zorder=10)

ax.axhline(0.832, color='blue', linestyle='--', alpha=0.5, label='Planck S8')
ax.axhline(0.776, color='green', linestyle='--', alpha=0.5, label='DES S8')
ax.axhspan(0.76, 0.78, alpha=0.1, color='green')
ax.axhspan(0.82, 0.84, alpha=0.1, color='blue')

ax.set_xticks(x_pos)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel('S8 = σ₈(Ω_m/0.3)^0.5', fontsize=12)
ax.set_title('S8 Measurements: CMB vs Low-z Surveys', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, axis='y', alpha=0.3)

# Annotate tension
ax.annotate('S8 Tension\n~2-3σ', xy=(2.5, 0.805), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
            ha='center')

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/predictions/02_DESI_S8_prediction.png', dpi=150)
print("\nSaved: 02_DESI_S8_prediction.png")
plt.close()

print("\n" + "=" * 80)
print("END OF PREDICTION 2")
print("=" * 80)
