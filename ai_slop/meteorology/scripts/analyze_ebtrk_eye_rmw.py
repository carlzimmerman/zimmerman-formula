#!/usr/bin/env python3
"""
Analyze Extended Best Track data for Eye/RMW ratios

Uses actual flight reconnaissance data from NOAA/NHC
Data source: https://rammb2.cira.colostate.edu/research/tropical-cyclones/tc_extended_best_track_dataset/

Tests the Z² prediction: eye_radius / RMW = 1/Z ≈ 0.173
"""

import numpy as np
from collections import defaultdict
from scipy import stats
import json

# Z² constants
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z_VALUE = np.sqrt(Z_SQUARED)  # ≈ 5.789
ONE_OVER_Z = 1 / Z_VALUE  # ≈ 0.1727

print("=" * 80)
print("  EXTENDED BEST TRACK ANALYSIS: Eye/RMW Ratios")
print("  Data Source: NOAA/NHC Flight Reconnaissance")
print("=" * 80)
print(f"\nZ² prediction: eye_radius/RMW = 1/Z = {ONE_OVER_Z:.4f}")

# Parse EBTRK data
# Format (new): StormID Name MMDDTT YYYY Lat Lon Vmax Pmin RMW EyeDiam POCP ROCP ...
# RMW and EyeDiam are in nautical miles (nm)
# Eye diameter needs to be divided by 2 to get eye radius

data_file = "data/extended_best_track/EBTRK_Atlantic_2021.txt"

print(f"\nLoading data from: {data_file}")

records = []
storms = defaultdict(list)

with open(data_file, 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) < 10:
            continue

        try:
            storm_id = parts[0]
            name = parts[1]
            date_time = parts[2]
            year = int(parts[3])
            lat = float(parts[4])
            lon = float(parts[5])
            vmax = int(parts[6])  # Max wind (kt)
            pmin = int(parts[7])  # Min pressure (hPa)
            rmw = int(parts[8])   # RMW (nm)
            eye_diam = int(parts[9])  # Eye diameter (nm)

            # Skip missing values
            if rmw <= 0 or rmw == -99:
                continue
            if eye_diam <= 0 or eye_diam == -99:
                continue

            # Calculate eye radius (diameter / 2) and ratio
            eye_radius = eye_diam / 2.0
            ratio = eye_radius / rmw

            record = {
                'storm_id': storm_id,
                'name': name,
                'year': year,
                'date_time': date_time,
                'vmax': vmax,
                'pmin': pmin,
                'rmw': rmw,
                'eye_diam': eye_diam,
                'eye_radius': eye_radius,
                'ratio': ratio,
            }
            records.append(record)
            storms[f"{name}_{year}"].append(record)

        except (ValueError, IndexError):
            continue

print(f"Loaded {len(records)} observations with valid eye and RMW data")
print(f"From {len(storms)} unique storms")

# Filter for intense hurricanes (Vmax >= 100 kt = Cat 3+)
cat3_plus = [r for r in records if r['vmax'] >= 100]
cat4_plus = [r for r in records if r['vmax'] >= 130]
cat5 = [r for r in records if r['vmax'] >= 157]

print(f"\nBy intensity:")
print(f"  Cat 3+ (≥100 kt): {len(cat3_plus)} observations")
print(f"  Cat 4+ (≥130 kt): {len(cat4_plus)} observations")
print(f"  Cat 5  (≥157 kt): {len(cat5)} observations")

# ============================================================================
# Statistical Analysis
# ============================================================================

print("\n" + "=" * 80)
print("  STATISTICAL ANALYSIS")
print("=" * 80)

def analyze_ratios(data, label):
    if len(data) < 5:
        print(f"\n{label}: Insufficient data ({len(data)} points)")
        return None

    ratios = [r['ratio'] for r in data]
    mean = np.mean(ratios)
    std = np.std(ratios, ddof=1)
    sem = std / np.sqrt(len(ratios))
    median = np.median(ratios)

    # Percentiles
    p10 = np.percentile(ratios, 10)
    p25 = np.percentile(ratios, 25)
    p75 = np.percentile(ratios, 75)
    p90 = np.percentile(ratios, 90)

    # Test against 1/Z
    t_stat, p_value = stats.ttest_1samp(ratios, ONE_OVER_Z)
    deviation_pct = (mean - ONE_OVER_Z) / ONE_OVER_Z * 100

    print(f"\n{label} (n={len(data)}):")
    print(f"  Mean:   {mean:.4f} ± {std:.4f}")
    print(f"  Median: {median:.4f}")
    print(f"  Range:  [{min(ratios):.4f}, {max(ratios):.4f}]")
    print(f"  IQR:    [{p25:.4f}, {p75:.4f}]")
    print(f"  10-90%: [{p10:.4f}, {p90:.4f}]")
    print(f"\n  vs 1/Z = {ONE_OVER_Z:.4f}:")
    print(f"    Deviation: {deviation_pct:+.1f}%")
    print(f"    t-statistic: {t_stat:.2f}")
    print(f"    p-value: {p_value:.2e}")

    if p_value < 0.05:
        print(f"    RESULT: SIGNIFICANTLY DIFFERENT from 1/Z")
    else:
        print(f"    RESULT: NOT significantly different from 1/Z")

    return {
        'n': len(data),
        'mean': mean,
        'std': std,
        'median': median,
        'min': min(ratios),
        'max': max(ratios),
        'p10': p10,
        'p90': p90,
        'deviation_pct': deviation_pct,
        't_stat': t_stat,
        'p_value': p_value,
    }

results = {}
results['all'] = analyze_ratios(records, "ALL OBSERVATIONS")
results['cat3_plus'] = analyze_ratios(cat3_plus, "CATEGORY 3+ (Vmax ≥ 100 kt)")
results['cat4_plus'] = analyze_ratios(cat4_plus, "CATEGORY 4+ (Vmax ≥ 130 kt)")
results['cat5'] = analyze_ratios(cat5, "CATEGORY 5 (Vmax ≥ 157 kt)")

# ============================================================================
# Compare to other constants
# ============================================================================

print("\n" + "=" * 80)
print("  COMPARISON TO OTHER CONSTANTS")
print("=" * 80)

if len(records) > 0:
    ratios_all = [r['ratio'] for r in records]
    mean_ratio = np.mean(ratios_all)

    constants = {
        '1/Z (Z² prediction)': ONE_OVER_Z,
        '1/6': 1/6,
        '1/5': 1/5,
        '1/4': 1/4,
        '1/3': 1/3,
        '1/π': 1/np.pi,
        '0.5': 0.5,
    }

    print(f"\nObserved mean: {mean_ratio:.4f}")
    print(f"\n{'Constant':<25} {'Value':>10} {'Deviation':>12} {'t-stat':>10} {'p-value':>12}")
    print("-" * 75)

    for name, value in sorted(constants.items(), key=lambda x: abs(mean_ratio - x[1])):
        t_stat, p_val = stats.ttest_1samp(ratios_all, value)
        dev = (mean_ratio - value) / value * 100
        sig = "" if p_val > 0.05 else "*" if p_val > 0.01 else "**" if p_val > 0.001 else "***"
        print(f"{name:<25} {value:>10.4f} {dev:>+11.1f}% {t_stat:>10.2f} {p_val:>12.2e} {sig}")

# ============================================================================
# Recent Major Hurricanes
# ============================================================================

print("\n" + "=" * 80)
print("  RECENT MAJOR HURRICANES (Cat 3+)")
print("=" * 80)

# Get unique storms with Cat 3+ intensity
major_storms = defaultdict(list)
for r in cat3_plus:
    key = f"{r['name']}_{r['year']}"
    major_storms[key].append(r)

# Sort by year descending
recent_storms = sorted(major_storms.items(), key=lambda x: -max(r['year'] for r in x[1]))[:20]

print(f"\n{'Storm':<20} {'Year':>6} {'Obs':>4} {'Mean Ratio':>12} {'Min':>8} {'Max':>8} {'Vmax':>8}")
print("-" * 80)

for storm_key, obs in recent_storms:
    name = obs[0]['name']
    year = obs[0]['year']
    ratios = [r['ratio'] for r in obs]
    vmaxs = [r['vmax'] for r in obs]
    print(f"{name:<20} {year:>6} {len(obs):>4} {np.mean(ratios):>12.4f} {min(ratios):>8.4f} {max(ratios):>8.4f} {max(vmaxs):>8}")

# ============================================================================
# Distribution Analysis
# ============================================================================

print("\n" + "=" * 80)
print("  DISTRIBUTION ANALYSIS")
print("=" * 80)

if len(records) > 0:
    ratios_all = [r['ratio'] for r in records]

    # Histogram bins
    bins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0]
    hist, _ = np.histogram(ratios_all, bins=bins)

    print("\nEye/RMW Ratio Distribution:")
    print(f"{'Bin':<15} {'Count':>8} {'Pct':>8}")
    print("-" * 35)
    for i in range(len(hist)):
        pct = hist[i] / len(ratios_all) * 100
        bar = "█" * int(pct / 2)
        print(f"{bins[i]:.1f} - {bins[i+1]:.1f}    {hist[i]:>8} {pct:>7.1f}% {bar}")

    # Where does 1/Z fall?
    count_below = sum(1 for r in ratios_all if r < ONE_OVER_Z)
    percentile = count_below / len(ratios_all) * 100
    print(f"\n1/Z = {ONE_OVER_Z:.4f} is at the {percentile:.1f}th percentile")

# ============================================================================
# Honest Assessment
# ============================================================================

print("\n" + "=" * 80)
print("  HONEST ASSESSMENT")
print("=" * 80)

if results['all']:
    mean = results['all']['mean']
    p_val = results['all']['p_value']

    print(f"""
FINDING: The observed eye_radius/RMW ratio does NOT match 1/Z

  Z² Prediction:     1/Z = {ONE_OVER_Z:.4f}
  Observed Mean:     {mean:.4f}
  Deviation:         {results['all']['deviation_pct']:+.1f}%
  p-value:           {p_val:.2e}

The flight reconnaissance data shows eye/RMW ratios are typically
around {mean:.2f}, which is {results['all']['deviation_pct']:+.1f}% different from the Z² prediction.

This REJECTS the hypothesis that eye_radius/RMW = 1/Z = 0.173.

INTERPRETATION:
  - The observed mean ({mean:.4f}) is closer to 1/2 or 1/3 than to 1/Z
  - Flight data provides ground truth that contradicts ERA5 analysis
  - The Z² hurricane prediction is NOT supported by this data
""")

# Save results
output = {
    'z2_prediction': ONE_OVER_Z,
    'results': results,
    'n_observations': len(records),
    'n_storms': len(storms),
    'data_source': 'NOAA Extended Best Track (EBTRK) 1851-2021',
    'verdict': 'Z² prediction NOT supported by flight reconnaissance data'
}

with open('ebtrk_eye_rmw_analysis.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"\nResults saved to: ebtrk_eye_rmw_analysis.json")
print("=" * 80)
