#!/usr/bin/env python3
"""
Validate Golden Ratio Finding on Pacific Typhoons

HYPOTHESIS TO TEST:
At Cat 3 intensity (~96-112 kt), eye/RMW = 1/φ = 0.618

Atlantic finding:
- Cat 3 mean ratio = 0.6187
- Deviation from 1/φ = +0.11%
- p-value = 0.96 (NOT significantly different)

Now testing on:
1. Western Pacific typhoons
2. Eastern Pacific hurricanes
"""

import numpy as np
import pandas as pd
from scipy import stats
import json

# Constants
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
ONE_OVER_PHI = 1 / PHI  # 0.6180339887
Z_SQUARED = 32 * np.pi / 3  # 33.51
ONE_OVER_Z = 1 / np.sqrt(Z_SQUARED)  # 0.1727

print("=" * 80)
print("  PACIFIC VALIDATION: GOLDEN RATIO IN HURRICANE/TYPHOON STRUCTURE")
print("=" * 80)

print(f"\n  Target: 1/φ = {ONE_OVER_PHI:.6f}")
print(f"  Atlantic Cat 3 result: 0.6187 (p=0.96)")

# =============================================================================
# LOAD WESTERN PACIFIC DATA
# =============================================================================

print("\n" + "=" * 80)
print("  WESTERN PACIFIC TYPHOONS (IBTrACS)")
print("=" * 80)

# Load data
wp_df = pd.read_csv('data/ibtracs_wp.csv', skiprows=[1], low_memory=False)  # Skip units row

# Filter for valid eye and RMW data
wp_df['USA_EYE'] = pd.to_numeric(wp_df['USA_EYE'], errors='coerce')
wp_df['USA_RMW'] = pd.to_numeric(wp_df['USA_RMW'], errors='coerce')
wp_df['USA_WIND'] = pd.to_numeric(wp_df['USA_WIND'], errors='coerce')

wp_valid = wp_df[(wp_df['USA_EYE'] > 0) & (wp_df['USA_RMW'] > 0) &
                  (wp_df['USA_WIND'] > 0)].copy()

print(f"\n  Total records: {len(wp_df)}")
print(f"  Valid eye+RMW records: {len(wp_valid)}")

if len(wp_valid) > 0:
    # Calculate ratio (EYE is diameter, so divide by 2 for radius)
    wp_valid['eye_radius'] = wp_valid['USA_EYE'] / 2.0
    wp_valid['ratio'] = wp_valid['eye_radius'] / wp_valid['USA_RMW']

    # Overall stats
    print(f"\n  Overall eye/RMW ratio:")
    print(f"    Mean = {wp_valid['ratio'].mean():.4f}")
    print(f"    Median = {wp_valid['ratio'].median():.4f}")
    print(f"    1/φ = {ONE_OVER_PHI:.4f}")
    print(f"    1/Z = {ONE_OVER_Z:.4f}")

    # By intensity category (using USA_WIND in knots)
    categories = [
        ('Tropical Storm', 34, 63),
        ('Cat 1', 64, 82),
        ('Cat 2', 83, 95),
        ('Cat 3', 96, 112),
        ('Cat 4', 113, 136),
        ('Cat 5', 137, 200),
    ]

    print(f"\n  {'Category':<20} {'N':>6} {'Mean':>10} {'Median':>10} {'vs 1/φ':>10} {'p-value':>10}")
    print("-" * 75)

    wp_results = {}
    for cat_name, vmin, vmax in categories:
        cat_data = wp_valid[(wp_valid['USA_WIND'] >= vmin) &
                            (wp_valid['USA_WIND'] <= vmax)]['ratio']
        if len(cat_data) >= 5:
            mean_r = cat_data.mean()
            med_r = cat_data.median()
            dev = (mean_r - ONE_OVER_PHI) / ONE_OVER_PHI * 100
            t_stat, p_val = stats.ttest_1samp(cat_data, ONE_OVER_PHI)
            wp_results[cat_name] = {
                'n': len(cat_data),
                'mean': float(mean_r),
                'median': float(med_r),
                'deviation_pct': float(dev),
                'p_value': float(p_val)
            }
            sig = "" if p_val > 0.05 else "*"
            print(f"  {cat_name:<20} {len(cat_data):>6} {mean_r:>10.4f} {med_r:>10.4f} {dev:>+9.1f}% {p_val:>10.4f} {sig}")

# =============================================================================
# LOAD EASTERN PACIFIC DATA
# =============================================================================

print("\n" + "=" * 80)
print("  EASTERN PACIFIC HURRICANES (IBTrACS)")
print("=" * 80)

ep_df = pd.read_csv('data/ibtracs_ep.csv', skiprows=[1], low_memory=False)

ep_df['USA_EYE'] = pd.to_numeric(ep_df['USA_EYE'], errors='coerce')
ep_df['USA_RMW'] = pd.to_numeric(ep_df['USA_RMW'], errors='coerce')
ep_df['USA_WIND'] = pd.to_numeric(ep_df['USA_WIND'], errors='coerce')

ep_valid = ep_df[(ep_df['USA_EYE'] > 0) & (ep_df['USA_RMW'] > 0) &
                  (ep_df['USA_WIND'] > 0)].copy()

print(f"\n  Total records: {len(ep_df)}")
print(f"  Valid eye+RMW records: {len(ep_valid)}")

if len(ep_valid) > 0:
    ep_valid['eye_radius'] = ep_valid['USA_EYE'] / 2.0
    ep_valid['ratio'] = ep_valid['eye_radius'] / ep_valid['USA_RMW']

    print(f"\n  Overall eye/RMW ratio:")
    print(f"    Mean = {ep_valid['ratio'].mean():.4f}")
    print(f"    Median = {ep_valid['ratio'].median():.4f}")

    print(f"\n  {'Category':<20} {'N':>6} {'Mean':>10} {'Median':>10} {'vs 1/φ':>10} {'p-value':>10}")
    print("-" * 75)

    ep_results = {}
    for cat_name, vmin, vmax in categories:
        cat_data = ep_valid[(ep_valid['USA_WIND'] >= vmin) &
                            (ep_valid['USA_WIND'] <= vmax)]['ratio']
        if len(cat_data) >= 5:
            mean_r = cat_data.mean()
            med_r = cat_data.median()
            dev = (mean_r - ONE_OVER_PHI) / ONE_OVER_PHI * 100
            t_stat, p_val = stats.ttest_1samp(cat_data, ONE_OVER_PHI)
            ep_results[cat_name] = {
                'n': len(cat_data),
                'mean': float(mean_r),
                'median': float(med_r),
                'deviation_pct': float(dev),
                'p_value': float(p_val)
            }
            sig = "" if p_val > 0.05 else "*"
            print(f"  {cat_name:<20} {len(cat_data):>6} {mean_r:>10.4f} {med_r:>10.4f} {dev:>+9.1f}% {p_val:>10.4f} {sig}")

# =============================================================================
# COMBINE ALL BASINS
# =============================================================================

print("\n" + "=" * 80)
print("  COMBINED ANALYSIS: ATLANTIC + WESTERN PACIFIC + EASTERN PACIFIC")
print("=" * 80)

# Load Atlantic EBTRK data for comparison
atl_records = []
with open('data/extended_best_track/EBTRK_Atlantic_2021.txt', 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 10:
            try:
                rmw = int(parts[8])
                eye_diam = int(parts[9])
                vmax = int(parts[6])
                if rmw > 0 and rmw != -99 and eye_diam > 0 and eye_diam != -99:
                    atl_records.append({
                        'basin': 'Atlantic',
                        'vmax': vmax,
                        'ratio': (eye_diam / 2.0) / rmw
                    })
            except:
                pass

# Add Pacific data
for idx, row in wp_valid.iterrows():
    atl_records.append({
        'basin': 'Western Pacific',
        'vmax': row['USA_WIND'],
        'ratio': row['ratio']
    })

for idx, row in ep_valid.iterrows():
    atl_records.append({
        'basin': 'Eastern Pacific',
        'vmax': row['USA_WIND'],
        'ratio': row['ratio']
    })

all_df = pd.DataFrame(atl_records)

print(f"\n  Combined observations by basin:")
print(all_df.groupby('basin').size())

print(f"\n  COMBINED CAT 3 ANALYSIS (96-112 kt):")
cat3_all = all_df[(all_df['vmax'] >= 96) & (all_df['vmax'] <= 112)]

print(f"\n  By basin:")
print(f"  {'Basin':<20} {'N':>6} {'Mean':>10} {'vs 1/φ':>10}")
print("-" * 50)

for basin in ['Atlantic', 'Western Pacific', 'Eastern Pacific']:
    basin_data = cat3_all[cat3_all['basin'] == basin]['ratio']
    if len(basin_data) >= 5:
        mean_r = basin_data.mean()
        dev = (mean_r - ONE_OVER_PHI) / ONE_OVER_PHI * 100
        print(f"  {basin:<20} {len(basin_data):>6} {mean_r:>10.4f} {dev:>+9.1f}%")

# Combined all basins
print(f"\n  COMBINED ALL BASINS:")
combined_mean = cat3_all['ratio'].mean()
combined_dev = (combined_mean - ONE_OVER_PHI) / ONE_OVER_PHI * 100
t_stat, p_val = stats.ttest_1samp(cat3_all['ratio'], ONE_OVER_PHI)

print(f"    N = {len(cat3_all)}")
print(f"    Mean = {combined_mean:.6f}")
print(f"    1/φ = {ONE_OVER_PHI:.6f}")
print(f"    Deviation = {combined_dev:+.4f}%")
print(f"    t-statistic = {t_stat:.4f}")
print(f"    p-value = {p_val:.4f}")

# Bootstrap CI
n_boot = 10000
boot_means = []
cat3_ratios = cat3_all['ratio'].values
for _ in range(n_boot):
    idx = np.random.randint(0, len(cat3_ratios), len(cat3_ratios))
    boot_means.append(np.mean(cat3_ratios[idx]))
ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])

print(f"    95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
print(f"    1/φ in CI: {ci_low <= ONE_OVER_PHI <= ci_high}")

# =============================================================================
# FIND OPTIMAL INTENSITY
# =============================================================================

print("\n" + "=" * 80)
print("  FINDING OPTIMAL INTENSITY FOR 1/φ (ALL BASINS)")
print("=" * 80)

# Linear fit
slope, intercept, r_val, p_val, _ = stats.linregress(all_df['vmax'], all_df['ratio'])
vmax_at_phi = (ONE_OVER_PHI - intercept) / slope

print(f"\n  Linear fit: ratio = {intercept:.4f} + {slope:.6f} × Vmax")
print(f"  R² = {r_val**2:.4f}")
print(f"  Ratio = 1/φ at Vmax = {vmax_at_phi:.1f} kt")

# Search for best match
best_match = None
best_dev = float('inf')

for vmin in range(50, 130, 2):
    for vmax in range(vmin + 10, 150, 2):
        subset = all_df[(all_df['vmax'] >= vmin) & (all_df['vmax'] <= vmax)]['ratio']
        if len(subset) >= 50:
            mean_r = subset.mean()
            dev = abs(mean_r - ONE_OVER_PHI)
            if dev < best_dev:
                best_dev = dev
                best_match = (vmin, vmax, len(subset), mean_r)

if best_match:
    vmin, vmax, n, mean_r = best_match
    print(f"\n  Best match to 1/φ (all basins):")
    print(f"    Intensity range: {vmin}-{vmax} kt")
    print(f"    N = {n}")
    print(f"    Mean ratio = {mean_r:.6f}")
    print(f"    1/φ = {ONE_OVER_PHI:.6f}")
    print(f"    Deviation = {(mean_r - ONE_OVER_PHI)/ONE_OVER_PHI*100:+.4f}%")

# =============================================================================
# INTENSITY THRESHOLDS vs Z²
# =============================================================================

print("\n" + "=" * 80)
print("  VALIDATION: TS THRESHOLD ≈ Z²")
print("=" * 80)

print(f"\n  Z² = 32π/3 = {Z_SQUARED:.4f}")
print(f"  TS threshold = 34 kt")
print(f"  Deviation = {(34 - Z_SQUARED)/Z_SQUARED*100:+.2f}%")

print("\n  This relationship is NOT basin-dependent")
print("  (Saffir-Simpson scale is universally applied)")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("  VALIDATION SUMMARY")
print("=" * 80)

print(f"""
HYPOTHESIS: At Cat 3 intensity, eye/RMW = 1/φ = 0.618

ATLANTIC (EBTRK flight data):
  Cat 3 mean = 0.6187
  Deviation from 1/φ = +0.11%
  p-value = 0.96 → NOT significantly different ✓

WESTERN PACIFIC (IBTrACS):
  Cat 3 mean = {wp_results.get('Cat 3', {}).get('mean', 'N/A'):.4f if 'Cat 3' in wp_results else 'N/A'}
  Deviation from 1/φ = {wp_results.get('Cat 3', {}).get('deviation_pct', 'N/A'):.2f if 'Cat 3' in wp_results else 'N/A'}%
  p-value = {wp_results.get('Cat 3', {}).get('p_value', 'N/A'):.4f if 'Cat 3' in wp_results else 'N/A'}

EASTERN PACIFIC (IBTrACS):
  Cat 3 mean = {ep_results.get('Cat 3', {}).get('mean', 'N/A'):.4f if 'Cat 3' in ep_results else 'N/A'}
  Deviation from 1/φ = {ep_results.get('Cat 3', {}).get('deviation_pct', 'N/A'):.2f if 'Cat 3' in ep_results else 'N/A'}%
  p-value = {ep_results.get('Cat 3', {}).get('p_value', 'N/A'):.4f if 'Cat 3' in ep_results else 'N/A'}

COMBINED (ALL BASINS):
  Cat 3 N = {len(cat3_all)}
  Mean = {combined_mean:.4f}
  Deviation from 1/φ = {combined_dev:+.2f}%
  p-value = {p_val:.4f}
  1/φ in 95% CI: {ci_low <= ONE_OVER_PHI <= ci_high}
""")

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    'hypothesis': 'At Cat 3 intensity, eye/RMW = 1/phi',
    'target': float(ONE_OVER_PHI),
    'atlantic': {
        'cat3_mean': 0.6187,
        'cat3_deviation': 0.11,
        'cat3_p_value': 0.96,
    },
    'western_pacific': wp_results,
    'eastern_pacific': ep_results,
    'combined': {
        'cat3_n': len(cat3_all),
        'cat3_mean': float(combined_mean),
        'cat3_deviation': float(combined_dev),
        'cat3_p_value': float(p_val),
        'cat3_ci_95': [float(ci_low), float(ci_high)],
        'phi_in_ci': bool(ci_low <= ONE_OVER_PHI <= ci_high),
    },
    'optimal_range': {
        'vmin': best_match[0] if best_match else None,
        'vmax': best_match[1] if best_match else None,
        'mean': float(best_match[3]) if best_match else None,
    }
}

with open('pacific_validation_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to: pacific_validation_results.json")
print("=" * 80)
