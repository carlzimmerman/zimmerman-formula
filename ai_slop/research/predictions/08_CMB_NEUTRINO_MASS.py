#!/usr/bin/env python3
"""
================================================================================
PREDICTION 8: CMB + BAO NEUTRINO MASS SUM
================================================================================

Cosmological observations constrain the sum of neutrino masses Σmν.

The Zimmerman Framework predicts:
  Σmν = m₁ + m₂ + m₃ = 0 + 8.6 + 49.6 = 58.2 meV

This is exactly at the minimum for normal hierarchy!

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

BEKENSTEIN = 3 * Z_SQUARED / (8 * PI)
ALPHA_INV = 4 * Z_SQUARED + 3
ALPHA = 1 / ALPHA_INV
m_e_eV = 0.511e6

# Neutrino masses
m_3_meV = m_e_eV * ALPHA**3 / BEKENSTEIN * 1000
m_2_meV = m_3_meV / Z
m_1_meV = 0
sum_m_meV = m_1_meV + m_2_meV + m_3_meV

print("=" * 80)
print("PREDICTION 8: COSMOLOGICAL NEUTRINO MASS")
print("=" * 80)

print(f"\nZimmerman neutrino masses:")
print(f"  m₁ = {m_1_meV:.1f} meV")
print(f"  m₂ = {m_2_meV:.1f} meV")
print(f"  m₃ = {m_3_meV:.1f} meV")
print(f"  Σmν = {sum_m_meV:.1f} meV = {sum_m_meV/1000:.4f} eV")

# =============================================================================
# COSMOLOGICAL CONSTRAINTS
# =============================================================================

print("\n" + "=" * 80)
print("COSMOLOGICAL CONSTRAINTS")
print("=" * 80)

constraints = [
    ("Planck 2018 (CMB alone)", "<260 meV (95% CL)"),
    ("Planck + BAO", "<120 meV (95% CL)"),
    ("Planck + BAO + lensing", "<90 meV (95% CL)"),
    ("DESI + CMB (2024)", "<72 meV (95% CL)"),
    ("Forecast: DESI full + CMB-S4", "±17 meV (1σ)"),
    ("Zimmerman prediction", f"{sum_m_meV:.1f} meV"),
]

print(f"\n{'Method':<35} {'Constraint':<25}")
print("-" * 60)
for method, constraint in constraints:
    print(f"{method:<35} {constraint:<25}")

# =============================================================================
# PHYSICAL SIGNIFICANCE
# =============================================================================

print("\n" + "=" * 80)
print("PHYSICAL SIGNIFICANCE")
print("=" * 80)

print(f"""
The Zimmerman prediction Σmν = {sum_m_meV:.1f} meV is significant:

1. MINIMUM MASS FOR NORMAL HIERARCHY
   From oscillations: √Δm²₃₁ ~ 50 meV
   Minimum Σmν > 58 meV (if m₁ = 0)
   Our prediction is EXACTLY at this minimum!

2. DETECTABLE BY NEXT-GEN SURVEYS
   CMB-S4 + DESI full: σ(Σmν) ~ 17 meV
   Can detect Σmν = 58 meV at ~3σ

3. CONSISTENCY CHECK
   If measured Σmν = 58 ± 10 meV:
   - Confirms normal hierarchy
   - Suggests m₁ ~ 0
   - Supports Zimmerman framework

4. FALSIFICATION CONDITIONS
   If Σmν > 70 meV: our m₃ too small
   If Σmν < 50 meV: our m₁ ≠ 0 (inverted?)
""")

# =============================================================================
# PREDICTIONS
# =============================================================================

print("=" * 80)
print("SPECIFIC PREDICTIONS")
print("=" * 80)

print(f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  NEUTRINO MASS SUM PREDICTION                                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Prediction: Σmν = {sum_m_meV:.1f} meV = {sum_m_meV/1000:.4f} eV                             ║
║                                                                               ║
║  Composition:                                                                 ║
║    m₁ = 0 (lightest neutrino massless)                                       ║
║    m₂ = 8.6 meV                                                              ║
║    m₃ = 49.6 meV                                                             ║
║                                                                               ║
║  Falsification:                                                               ║
║    Σmν > 70 meV (excludes our m₃)                                            ║
║    Σmν < 50 meV (excludes our framework)                                     ║
║    Detection at Σmν ~ 100+ meV (requires m₁ >> 0)                            ║
║                                                                               ║
║  Strong support:                                                              ║
║    Σmν measured as 55-65 meV                                                 ║
║    Normal hierarchy confirmed by JUNO                                        ║
║                                                                               ║
║  Timeline: CMB-S4 + DESI (~2027-2028)                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# GENERATE PLOT
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Current upper limits
limits = [
    ("Planck 2018", 260),
    ("Planck+BAO", 120),
    ("Planck+BAO+lens", 90),
    ("DESI 2024", 72),
]

x_pos = range(len(limits))
ax.bar(x_pos, [l[1] for l in limits], color='lightblue', edgecolor='black')
ax.set_xticks(x_pos)
ax.set_xticklabels([l[0] for l in limits])
ax.set_ylabel('Σmν upper limit (meV, 95% CL)', fontsize=12)
ax.set_title('Cosmological Neutrino Mass Constraints', fontsize=14)

# Add prediction line
ax.axhline(sum_m_meV, color='red', linewidth=3, label=f'Zimmerman: {sum_m_meV:.1f} meV')
ax.axhline(58, color='green', linewidth=2, linestyle='--', label='Min for normal hierarchy')

# Forecast range
ax.axhspan(sum_m_meV - 17, sum_m_meV + 17, alpha=0.2, color='red',
           label='CMB-S4 + DESI forecast (1σ)')

ax.legend(loc='upper right')
ax.set_ylim(0, 300)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/predictions/08_CMB_neutrino_mass.png', dpi=150)
print("\nSaved: 08_CMB_neutrino_mass.png")
plt.close()

print("\n" + "=" * 80)
print("END OF PREDICTION 8")
print("=" * 80)
