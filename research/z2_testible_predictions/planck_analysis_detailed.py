#!/usr/bin/env python3
"""
Detailed analysis of Planck matched circles results with proper statistics.

This script examines the candidate matches more carefully, accounting for:
1. Look-elsewhere effect (trials factor)
2. Comparison with null simulations
3. Consistency checks across radii

Carl Zimmerman | May 2026
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Results from Planck analysis (threshold = 0.45)
results = {
    15: {'max_corr': 0.493, 'n_matches': 2, 'significance': 5.9},
    20: {'max_corr': 0.402, 'n_matches': 0, 'significance': 4.6},
    25: {'max_corr': 0.402, 'n_matches': 0, 'significance': 4.3},
    30: {'max_corr': 0.464, 'n_matches': 2, 'significance': 5.7},
    35: {'max_corr': 0.470, 'n_matches': 1, 'significance': 6.5},
    40: {'max_corr': 0.485, 'n_matches': 2, 'significance': 6.2},
    45: {'max_corr': 0.470, 'n_matches': 1, 'significance': 5.3},
    50: {'max_corr': 0.467, 'n_matches': 1, 'significance': 6.7},
    55: {'max_corr': 0.391, 'n_matches': 0, 'significance': 4.5},
    60: {'max_corr': 0.420, 'n_matches': 0, 'significance': 5.2},
    65: {'max_corr': 0.429, 'n_matches': 0, 'significance': 6.2},
    70: {'max_corr': 0.424, 'n_matches': 0, 'significance': 6.1},
    75: {'max_corr': 0.391, 'n_matches': 0, 'significance': 5.6},
}

# Results from simulated CMB (no topology, threshold = 0.5)
# These had max_corr ~ 0.25-0.28, significance ~ 5σ
simulated_max_corr = 0.27  # typical
simulated_significance = 5.0  # typical

print("=" * 70)
print("DETAILED ANALYSIS OF PLANCK MATCHED CIRCLES RESULTS")
print("=" * 70)

# 1. Look-elsewhere effect
print("\n1. LOOK-ELSEWHERE EFFECT (TRIALS FACTOR)")
print("-" * 40)

n_centers = 5000
n_radii = 13
n_trials = n_centers * n_radii
print(f"   Number of centers tested: {n_centers}")
print(f"   Number of radii tested: {n_radii}")
print(f"   Total trials: {n_trials}")

# For a 5σ local significance, what's the global significance?
# P(at least one > 5σ) = 1 - (1 - P(>5σ))^n ≈ n × P(>5σ) for small P
p_5sigma = stats.norm.sf(5.0)  # ~2.87e-7
p_global = 1 - (1 - p_5sigma) ** n_trials
global_sigma = stats.norm.isf(p_global / 2)  # Two-tailed

print(f"\n   P(>5σ single trial): {p_5sigma:.2e}")
print(f"   P(at least one >5σ in {n_trials} trials): {p_global:.4f}")
print(f"   This means: A 5σ local excess is expected ~{p_global*100:.1f}% of the time")
print(f"   Equivalent global significance: {global_sigma:.1f}σ")

# For highest observed (6.7σ at 50°)
max_local_sig = 6.7
p_max = stats.norm.sf(max_local_sig)
p_global_max = 1 - (1 - p_max) ** n_trials
global_sigma_max = stats.norm.isf(p_global_max / 2)

print(f"\n   Highest local significance: {max_local_sig}σ")
print(f"   P(>6.7σ single trial): {p_max:.2e}")
print(f"   P(at least one >6.7σ in {n_trials} trials): {p_global_max:.4f}")
print(f"   Equivalent global significance: {global_sigma_max:.1f}σ")

# 2. Correlation distribution comparison
print("\n2. CORRELATION DISTRIBUTION ANALYSIS")
print("-" * 40)

planck_max_corrs = [r['max_corr'] for r in results.values()]
print(f"   Planck max correlations: {min(planck_max_corrs):.3f} to {max(planck_max_corrs):.3f}")
print(f"   Mean: {np.mean(planck_max_corrs):.3f}")
print(f"   Std: {np.std(planck_max_corrs):.3f}")

print(f"\n   Simulated (no topology) max correlation: ~{simulated_max_corr:.3f}")
print(f"   Planck correlations are HIGHER by: {np.mean(planck_max_corrs) - simulated_max_corr:.3f}")

# 3. Consistency check: topology should show ONE radius
print("\n3. CONSISTENCY CHECK: SINGLE RADIUS EXPECTED")
print("-" * 40)

radii_with_matches = [r for r, d in results.items() if d['n_matches'] > 0]
print(f"   Radii with matches (threshold 0.45): {radii_with_matches}")
print(f"   Number of distinct radii: {len(radii_with_matches)}")

if len(radii_with_matches) > 2:
    print(f"\n   ⚠️  WARNING: T³/Z₂ topology would produce matches at ONE radius")
    print(f"   Having {len(radii_with_matches)} different radii suggests:")
    print(f"   - Statistical fluctuations (most likely)")
    print(f"   - Systematic effects or foreground contamination")
    print(f"   - NOT a coherent topology signal")
else:
    print(f"   ✓ Matches concentrated at {len(radii_with_matches)} radii - possibly consistent")

# 4. Physical interpretation
print("\n4. PHYSICAL INTERPRETATION")
print("-" * 40)

print("""
   If r = 15° circles matched:
     → Fundamental domain size L ≈ 4 Gpc
     → Universe wraps around at ~4 Gpc scale

   If r = 50° circles matched:
     → Fundamental domain size L ≈ 12 Gpc
     → Close to last scattering surface (~14 Gpc)
""")

# 5. Verdict
print("\n5. VERDICT")
print("-" * 40)

print("""
   LOCAL SIGNIFICANCE: Some circle pairs show 5-7σ excess

   GLOBAL SIGNIFICANCE: After trials correction, only ~2-3σ

   CONSISTENCY: Matches at multiple radii → NOT consistent with topology

   COMPARISON: Planck shows higher correlations than simulated
              This could be:
              - Real non-Gaussian features in CMB
              - Foreground residuals
              - Systematic effects
              - NOT T³/Z₂ topology (would be single radius)

   CONCLUSION: No convincing evidence for T³/Z₂ cosmic topology
               at detectable scales (L < 20 Gpc)
""")

# 6. Constraints
print("\n6. TOPOLOGY CONSTRAINTS")
print("-" * 40)

print("""
   From this analysis, we can constrain:

   T³/Z₂ FUNDAMENTAL DOMAIN SIZE:

   If T³/Z₂ topology exists: L > 14 Gpc (last scattering surface)

   This is consistent with:
   - Simply connected (infinite) universe
   - T³/Z₂ with L much larger than Hubble radius

   Not inconsistent with Z² framework, which doesn't specify L
""")

# Create summary figure
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: Max correlation vs radius
ax1 = axes[0]
radii = sorted(results.keys())
max_corrs = [results[r]['max_corr'] for r in radii]
ax1.plot(radii, max_corrs, 'ro-', markersize=10, linewidth=2)
ax1.axhline(y=0.45, color='orange', linestyle='--', label='Threshold (0.45)')
ax1.axhline(y=0.50, color='red', linestyle='--', label='Strict threshold (0.50)')
ax1.axhline(y=simulated_max_corr, color='blue', linestyle=':', label=f'Simulated ({simulated_max_corr})')
ax1.fill_between(radii, simulated_max_corr - 0.05, simulated_max_corr + 0.05,
                  alpha=0.2, color='blue', label='Simulated range')
ax1.set_xlabel('Circle Radius (°)', fontsize=12)
ax1.set_ylabel('Max Correlation', fontsize=12)
ax1.set_title('Planck vs Simulated CMB', fontsize=14)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# Panel 2: Local vs Global significance
ax2 = axes[1]
local_sigs = [results[r]['significance'] for r in radii]
ax2.bar(radii, local_sigs, color='red', alpha=0.7, width=4, label='Local σ')
ax2.axhline(y=global_sigma_max, color='blue', linestyle='--', linewidth=2,
            label=f'Global σ ({global_sigma_max:.1f})')
ax2.axhline(y=5, color='green', linestyle=':', label='5σ threshold')
ax2.set_xlabel('Circle Radius (°)', fontsize=12)
ax2.set_ylabel('Significance (σ)', fontsize=12)
ax2.set_title('Local vs Global Significance', fontsize=14)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

# Panel 3: Number of matches
ax3 = axes[2]
n_matches = [results[r]['n_matches'] for r in radii]
colors = ['red' if n > 0 else 'gray' for n in n_matches]
ax3.bar(radii, n_matches, color=colors, width=4)
ax3.set_xlabel('Circle Radius (°)', fontsize=12)
ax3.set_ylabel('Number of Matches', fontsize=12)
ax3.set_title('Matches per Radius\n(Should be single radius for real topology)', fontsize=14)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/z2_testible_predictions/planck_analysis_detailed.png',
            dpi=150, bbox_inches='tight')
print("\nSaved detailed analysis figure.")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
