#!/usr/bin/env python3
"""
Gravitational Wave Polarization Test for Z²

Z² PREDICTION: h_× = 0 (cross-polarization eliminated by Z₂ projection)

This is a REVOLUTIONARY prediction that can be tested with LIGO data!

In standard GR:
- GW have two polarizations: h_+ (plus) and h_× (cross)
- For a binary merger, both are present
- Observed amplitudes depend on viewing angle (inclination ι)
  - Face-on (ι=0°): |h_+| >> |h_×|
  - Edge-on (ι=90°): |h_+| ≈ |h_×|
- Random binary orientations: <|h_×|²>/<|h_+|²> ≈ 1

In Z²:
- h_× = 0 intrinsically (topology eliminates this polarization)
- Only h_+ exists
- Waveforms would look VERY different

This script analyzes what we can test with LIGO data.

Carl Zimmerman | May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

print("="*70)
print("GRAVITATIONAL WAVE POLARIZATION TEST FOR Z²")
print("="*70)

# =============================================================================
# THEORETICAL BACKGROUND
# =============================================================================

print("""
THEORETICAL BACKGROUND
======================

In GR, the GW strain from a compact binary is:

h_+ = A(t) × (1 + cos²ι)/2 × cos(2Φ(t) + 2ψ)
h_× = A(t) × cos(ι) × sin(2Φ(t) + 2ψ)

where:
  ι = inclination angle (0° = face-on, 90° = edge-on)
  ψ = polarization angle
  A(t) = amplitude (depends on masses, distance)
  Φ(t) = orbital phase

The ratio of amplitudes:
  |h_×| / |h_+| = 2 cos(ι) / (1 + cos²ι)

This ratio ranges from:
  - ι = 0° (face-on):   |h_×|/|h_+| = 2/2 = 1
  - ι = 90° (edge-on):  |h_×|/|h_+| = 0/1 = 0

Wait... this is backwards from what I said earlier!

Actually:
  - Face-on: h_× is maximal (= h_+)
  - Edge-on: h_× → 0

If Z² predicts h_× = 0, then ALL events would appear edge-on!
This would be a very distinctive signature.
""")

# =============================================================================
# SIMULATION: GR vs Z² PREDICTIONS
# =============================================================================

print("\n" + "="*70)
print("GR vs Z² PREDICTIONS")
print("="*70)

# Inclination angle distribution
# In GR, binaries are randomly oriented
# cos(ι) is uniformly distributed in [-1, 1]

np.random.seed(42)
n_events = 100

# GR: random inclinations
cos_iota_GR = np.random.uniform(-1, 1, n_events)
iota_GR = np.degrees(np.arccos(np.abs(cos_iota_GR)))  # 0° to 90°

# Calculate h_×/h_+ ratio for GR
# |h_×/h_+| = 2|cos(ι)|/(1 + cos²ι)
ratio_GR = 2 * np.abs(cos_iota_GR) / (1 + cos_iota_GR**2)

# Z²: h_× = 0 means ratio = 0 always
ratio_Z2 = np.zeros(n_events)

print(f"GR prediction:")
print(f"  Mean |h_×/h_+| = {np.mean(ratio_GR):.3f}")
print(f"  Std  |h_×/h_+| = {np.std(ratio_GR):.3f}")
print(f"  Expected range: 0 to 1")

print(f"\nZ² prediction:")
print(f"  |h_×/h_+| = 0 always")


# =============================================================================
# WHAT LIGO ACTUALLY MEASURES
# =============================================================================

print("\n" + "="*70)
print("WHAT LIGO ACTUALLY MEASURES")
print("="*70)

print("""
LIGO doesn't measure h_+ and h_× directly!

A single detector measures a combination:
  h(t) = F_+ h_+ + F_× h_×

where F_+ and F_× are antenna pattern functions.

To separate h_+ and h_×, you need:
1. Multiple detectors (LIGO Hanford + Livingston + Virgo)
2. Parameter estimation that fits for inclination ι

The parameter ι is INFERRED from the waveform shape!

If h_× = 0 (Z² prediction):
- Waveform shape would be different
- Inferred ι would cluster near 90° (edge-on)
- OR parameter estimation would give poor fits

WHAT TO CHECK:
1. Distribution of inferred inclination angles
2. Quality of waveform fits with h_× = 0 template
3. Correlation between ι and signal-to-noise ratio
""")


# =============================================================================
# GWTC-3 DATA ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("GWTC-3 CATALOG ANALYSIS")
print("="*70)

# Representative inclination angles from GWTC-3 events
# These are from the posterior median values
# Note: Most events have large uncertainties on ι

gwtc3_events = {
    'GW150914': {'iota': 143, 'iota_err': 20},  # First detection!
    'GW151226': {'iota': 47, 'iota_err': 30},
    'GW170104': {'iota': 115, 'iota_err': 30},
    'GW170608': {'iota': 150, 'iota_err': 20},
    'GW170729': {'iota': 100, 'iota_err': 40},
    'GW170809': {'iota': 120, 'iota_err': 40},
    'GW170814': {'iota': 155, 'iota_err': 15},  # First 3-detector
    'GW170817': {'iota': 152, 'iota_err': 8},   # Neutron star merger!
    'GW170818': {'iota': 140, 'iota_err': 30},
    'GW170823': {'iota': 120, 'iota_err': 40},
    'GW190412': {'iota': 125, 'iota_err': 15},  # Asymmetric masses
    'GW190521': {'iota': 90, 'iota_err': 40},   # Most massive
    'GW190814': {'iota': 110, 'iota_err': 20},  # Mystery object
}

print("GWTC-3 Inclination Angles (median ± 1σ):")
print("-" * 50)

iota_values = []
iota_errors = []
for name, data in gwtc3_events.items():
    iota = data['iota']
    err = data['iota_err']
    iota_values.append(iota)
    iota_errors.append(err)
    # Flag if consistent with edge-on (90° or 180°-90°=90°)
    edge_on = min(abs(iota - 90), abs(iota - 90))
    flag = "← edge-on" if edge_on < 30 else ""
    print(f"  {name}: {iota:3d}° ± {err:2d}°  {flag}")

iota_values = np.array(iota_values)
iota_errors = np.array(iota_errors)

# Convert to standard range [0°, 180°]
# Values near 0° or 180° are face-on
# Values near 90° are edge-on

print(f"\nStatistics:")
# Distance from edge-on (90°)
dist_from_edgeon = np.minimum(np.abs(iota_values - 90), np.abs(180 - iota_values - 90))
print(f"  Mean distance from edge-on: {np.mean(dist_from_edgeon):.1f}°")
print(f"  Events within 30° of edge-on: {np.sum(dist_from_edgeon < 30)}/{len(iota_values)}")


# =============================================================================
# THE KEY TEST
# =============================================================================

print("\n" + "="*70)
print("THE KEY TEST")
print("="*70)

print("""
If h_× = 0 (Z² prediction):
  - INFERRED ι should cluster near 90° (edge-on)
  - Because h_× = 0 looks like an edge-on source in GR templates

Let's test this statistically...

Null hypothesis (GR): cos(ι) uniformly distributed
  → ι has distribution: P(ι) ∝ sin(ι)
  → Expected: more face-on (ι near 0° or 180°) than edge-on (ι=90°)

Z² prediction: ι should cluster near 90°
  → Would appear as excess of edge-on sources
""")

# Generate expected distribution from GR
n_mc = 10000
cos_iota_mc = np.random.uniform(-1, 1, n_mc)
iota_mc = np.degrees(np.arccos(cos_iota_mc))  # 0° to 180°

# Compare observed to expected
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Panel 1: Observed vs GR expected
ax1 = axes[0]
ax1.hist(iota_mc, bins=18, range=(0, 180), density=True, alpha=0.5,
         color='blue', label='GR expected (sin(ι))')
ax1.hist(iota_values, bins=9, range=(0, 180), density=True, alpha=0.7,
         color='red', label=f'GWTC-3 ({len(iota_values)} events)')
ax1.axvline(90, color='green', linestyle='--', label='Edge-on (90°)')
ax1.set_xlabel('Inclination angle (°)', fontsize=12)
ax1.set_ylabel('Probability density', fontsize=12)
ax1.set_title('Inclination Distribution', fontsize=14)
ax1.legend()

# Panel 2: h_×/h_+ ratio
ax2 = axes[1]
# For each event, compute expected |h_×/h_+| ratio
observed_ratios = 2 * np.abs(np.cos(np.radians(iota_values))) / (1 + np.cos(np.radians(iota_values))**2)
expected_ratios = 2 * np.abs(cos_iota_mc) / (1 + cos_iota_mc**2)

ax2.hist(expected_ratios, bins=20, range=(0, 1), density=True, alpha=0.5,
         color='blue', label='GR expected')
ax2.hist(observed_ratios, bins=10, range=(0, 1), density=True, alpha=0.7,
         color='red', label='GWTC-3 implied')
ax2.axvline(0, color='green', linestyle='--', linewidth=2, label='Z² prediction')
ax2.set_xlabel('|h_×| / |h_+| ratio', fontsize=12)
ax2.set_ylabel('Probability density', fontsize=12)
ax2.set_title('Polarization Ratio', fontsize=14)
ax2.legend()

# Panel 3: Test statistic
ax3 = axes[2]
ax3.axis('off')

# Compute test statistics
mean_ratio_obs = np.mean(observed_ratios)
mean_ratio_exp = np.mean(expected_ratios)
std_ratio_exp = np.std(expected_ratios)

z_score = (mean_ratio_obs - mean_ratio_exp) / (std_ratio_exp / np.sqrt(len(observed_ratios)))

# Also compute distance from Z² prediction (ratio = 0)
mean_ratio_z2 = 0
z_score_z2 = mean_ratio_obs / (std_ratio_exp / np.sqrt(len(observed_ratios)))

test_text = f"""
STATISTICAL TEST

Observed mean |h_×/h_+|: {mean_ratio_obs:.3f}
GR expected:            {mean_ratio_exp:.3f} ± {std_ratio_exp:.3f}
Z² prediction:          0.000

Test vs GR:
  z-score = {z_score:.2f}
  Result: {'Consistent' if abs(z_score) < 2 else 'TENSION'} with GR

Test vs Z²:
  z-score = {z_score_z2:.1f}
  Result: {'Consistent' if abs(z_score_z2) < 2 else 'INCONSISTENT'} with Z²

INTERPRETATION:
- Observed ratios are consistent with GR
- Observed ratios REJECT Z² prediction (h_×=0)

⚠️  IMPORTANT CAVEAT:
GWTC-3 parameter estimation ASSUMES GR!
If h_× = 0, the templates would be wrong,
and the inferred ι would be biased.

A PROPER TEST requires:
1. Fitting with h_× = 0 templates
2. Comparing Bayesian evidence GR vs Z²
3. This requires access to strain data
"""

ax3.text(0.1, 0.9, test_text, transform=ax3.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('gw_polarization_test.png', dpi=150, bbox_inches='tight')
print("\nSaved: gw_polarization_test.png")
plt.close()


# =============================================================================
# CONCLUSION
# =============================================================================

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)

print(f"""
PRELIMINARY FINDING:
Based on inferred inclination angles from GWTC-3,
the observed |h_×/h_+| ratios are:
  - CONSISTENT with GR (z = {z_score:.1f}σ)
  - INCONSISTENT with Z² h_×=0 (z = {z_score_z2:.1f}σ)

⚠️  IMPORTANT CAVEATS:

1. CIRCULAR REASONING: GWTC-3 analysis assumes GR templates!
   The inferred ι values might be biased if h_× = 0.

2. PROPER TEST NEEDED:
   - Reanalyze events with h_× = 0 templates
   - Compare Bayesian evidence: P(data|GR) vs P(data|Z²)
   - This requires significant computational resources

3. ALTERNATIVE INTERPRETATION:
   If Z² is correct, LIGO might be systematically
   misinterpreting waveforms, leading to:
   - Biased mass estimates
   - Wrong distance measurements
   - Poor fits for some events

RECOMMENDATION:
A definitive test requires running custom GW analysis
with h_× = 0 templates. This is beyond our current scope
but would be a powerful test of Z².
""")
