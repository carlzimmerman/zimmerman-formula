#!/usr/bin/env python3
"""
Example 19: Dark Energy Equation of State Prediction

If the Zimmerman formula correctly derives Λ from a₀, then dark energy
must be a TRUE cosmological constant with w = -1 exactly.

This is a strong, falsifiable prediction testable by DESI, Euclid, Roman.

If w ≠ -1 is measured → Zimmerman interpretation is wrong
If w = -1 exactly → Consistent with Zimmerman (Λ from a₀)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

print("=" * 70)
print("EXAMPLE 19: DARK ENERGY EQUATION OF STATE PREDICTION")
print("=" * 70)
print()

# ============================================================================
# 1. THE ARGUMENT
# ============================================================================

print("PART 1: THE ZIMMERMAN ARGUMENT FOR w = -1")
print("-" * 50)
print()
print("The Zimmerman formula connects a₀ to cosmology:")
print("  a₀ = c√(Gρc)/2 = cH₀/5.79")
print()
print("At late times (z → -1), the universe approaches de Sitter:")
print("  H → H_∞ = H₀√Ω_Λ")
print("  a₀ → a₀,∞ = c√(Gρ_Λ)/2")
print()
print("Inverting, we derive the cosmological constant:")
print("  Λ = 32π × a₀² × Ω_Λ / c⁴")
print()
print("KEY IMPLICATION:")
print("  If Λ is derived from a₀ (which is constant at late times),")
print("  then Λ is a TRUE CONSTANT, not evolving dark energy.")
print()
print("  Therefore: w = -1 EXACTLY")
print()

# ============================================================================
# 2. CURRENT OBSERVATIONS
# ============================================================================

print("PART 2: CURRENT OBSERVATIONAL CONSTRAINTS")
print("-" * 50)
print()

# Current measurements (as of 2025)
measurements = [
    ("Planck 2020 (CMB)", -1.03, 0.03),
    ("Planck + BAO", -1.04, 0.03),
    ("DES Y3", -0.98, 0.05),
    ("Pantheon+ SNe", -1.01, 0.04),
    ("Combined", -1.02, 0.02),
]

print(f"{'Measurement':<25} {'w':<10} {'±σ':<10}")
print("-" * 45)
for name, w, sigma in measurements:
    print(f"{name:<25} {w:<10.2f} {sigma:<10.2f}")
print()

# Zimmerman prediction
w_zimmerman = -1.00

print(f"Zimmerman prediction:    w = {w_zimmerman:.2f} (exactly)")
print()

# Check consistency
combined_w = -1.02
combined_sigma = 0.02
tension = abs(combined_w - w_zimmerman) / combined_sigma

print(f"Tension with current data: {tension:.1f}σ")
print(f"Status: {'CONSISTENT' if tension < 2 else 'TENSION'}")
print()

# ============================================================================
# 3. FUTURE TESTS
# ============================================================================

print("PART 3: FUTURE TESTS")
print("-" * 50)
print()

future_missions = [
    ("DESI (2024-2029)", 0.01, "BAO + RSD"),
    ("Euclid (2024-2030)", 0.01, "Weak lensing + clustering"),
    ("Roman (2027-2032)", 0.01, "SNe Ia + BAO"),
    ("Combined 2030s", 0.005, "All probes"),
]

print(f"{'Mission':<25} {'σ(w)':<10} {'Method':<25}")
print("-" * 60)
for name, sigma, method in future_missions:
    print(f"{name:<25} {sigma:<10.3f} {method:<25}")
print()

print("With σ(w) = 0.005, we can distinguish:")
print("  w = -1.00 (Zimmerman/Λ) from w = -0.99 (quintessence)")
print()

# ============================================================================
# 4. ALTERNATIVE DARK ENERGY MODELS
# ============================================================================

print("PART 4: WHAT IF w ≠ -1?")
print("-" * 50)
print()

alternatives = [
    ("Quintessence", "w > -1, possibly evolving", "a₀ would also evolve differently"),
    ("Phantom", "w < -1", "Universe ends in Big Rip"),
    ("Early dark energy", "w(z) varies", "a₀(z) would deviate from prediction"),
    ("Modified gravity", "Effective w ≠ -1", "Zimmerman might still hold"),
]

print(f"{'Model':<20} {'Prediction':<30} {'Zimmerman implication':<30}")
print("-" * 80)
for model, prediction, implication in alternatives:
    print(f"{model:<20} {prediction:<30} {implication:<30}")
print()

print("CRITICAL TEST:")
print("  If DESI/Euclid measure w = -0.95 ± 0.01 → Zimmerman Λ-derivation WRONG")
print("  If DESI/Euclid measure w = -1.00 ± 0.01 → Zimmerman SUPPORTED")
print()

# ============================================================================
# 5. VISUALIZATION
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Current and future constraints
ax1 = axes[0]

# Current measurements
names = [m[0] for m in measurements]
w_vals = [m[1] for m in measurements]
sigmas = [m[2] for m in measurements]

y_pos = np.arange(len(names))
ax1.errorbar(w_vals, y_pos, xerr=sigmas, fmt='o', capsize=5,
             color='blue', markersize=8, label='Current (1σ)')

# Zimmerman prediction
ax1.axvline(x=-1.0, color='red', linestyle='--', linewidth=2,
            label='Zimmerman: w = -1')

# Future precision
ax1.axvspan(-1.005, -0.995, alpha=0.3, color='green',
            label='2030s precision (±0.005)')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(names)
ax1.set_xlabel('Dark Energy Equation of State w', fontsize=12)
ax1.set_title('Current Constraints on w', fontsize=14)
ax1.legend(loc='upper left', fontsize=9)
ax1.set_xlim(-1.15, -0.85)
ax1.grid(True, alpha=0.3, axis='x')

# Plot 2: w(z) evolution scenarios
ax2 = axes[1]

z_range = np.linspace(0, 2, 100)

# Different models
w_constant = np.ones_like(z_range) * (-1.0)  # Zimmerman/Λ
w_quintessence = -1.0 + 0.1 * z_range / (1 + z_range)  # Evolving
w_phantom = -1.0 - 0.05 * z_range / (1 + z_range)  # Phantom

ax2.plot(z_range, w_constant, 'r-', linewidth=2, label='Zimmerman (w = -1)')
ax2.plot(z_range, w_quintessence, 'b--', linewidth=2, label='Quintessence')
ax2.plot(z_range, w_phantom, 'g:', linewidth=2, label='Phantom')

ax2.axhline(y=-1, color='gray', linestyle=':', alpha=0.5)
ax2.set_xlabel('Redshift z', fontsize=12)
ax2.set_ylabel('w(z)', fontsize=12)
ax2.set_title('Dark Energy Evolution Models', fontsize=14)
ax2.legend(loc='upper right')
ax2.set_xlim(0, 2)
ax2.set_ylim(-1.15, -0.85)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(output_dir, 'output', 'dark_energy_eos.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print("=" * 70)
print("OUTPUT: output/dark_energy_eos.png")
print("=" * 70)

# ============================================================================
# 6. SUMMARY
# ============================================================================

print()
print("=" * 70)
print("SUMMARY: ZIMMERMAN PREDICTION FOR DARK ENERGY")
print("=" * 70)
print()
print("PREDICTION: w = -1 exactly (true cosmological constant)")
print()
print("REASONING:")
print("  • Zimmerman derives Λ from a₀")
print("  • a₀ approaches constant value at late times")
print("  • Therefore Λ is constant, not evolving")
print("  • Therefore w = p/ρ = -1 exactly")
print()
print("CURRENT STATUS: Consistent (w = -1.02 ± 0.02)")
print()
print("FUTURE TEST: DESI + Euclid + Roman will measure w to ±0.005")
print("  • If w = -1.00 ± 0.005 → Strong support for Zimmerman")
print("  • If w ≠ -1 at >3σ → Zimmerman Λ-derivation falsified")
print()
print("This is a CLEAN, FALSIFIABLE prediction.")
print("=" * 70)
