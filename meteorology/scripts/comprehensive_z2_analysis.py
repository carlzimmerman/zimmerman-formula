#!/usr/bin/env python3
"""
Comprehensive Z² / 8D Manifold Analysis of Hurricane Data

Explores multiple potential relationships where Z² = 32π/3 might appear:
- Eye/RMW ratios (already falsified at 1/Z = 0.173)
- Pressure-wind relationships
- Intensity thresholds
- Scale ratios between different hurricane radii
- Angular momentum relationships
- Vortex structure parameters

Key 8D manifold constants:
- Z² = 32π/3 ≈ 33.51
- Z = √(32π/3) ≈ 5.789
- 1/Z ≈ 0.1727
- π/3 ≈ 1.047 (Vol(S⁷)/Vol(S⁵) ratio)
- 32 (compactification coefficient)

Data source: NOAA Extended Best Track (Flight Reconnaissance)
"""

import numpy as np
from collections import defaultdict
from scipy import stats
import json

# =============================================================================
# 8D MANIFOLD CONSTANTS
# =============================================================================

PI = np.pi
Z_SQUARED = 32 * PI / 3  # ≈ 33.51
Z_VALUE = np.sqrt(Z_SQUARED)  # ≈ 5.789
ONE_OVER_Z = 1 / Z_VALUE  # ≈ 0.1727
SPHERE_RATIO = PI / 3  # Vol(S⁷)/Vol(S⁵) ≈ 1.047
SQRT_PI_OVER_3 = np.sqrt(PI / 3)  # ≈ 1.023

# Related mathematical constants
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio ≈ 1.618
E = np.e  # Euler's number

print("=" * 80)
print("  8D MANIFOLD / Z² COMPREHENSIVE HURRICANE ANALYSIS")
print("=" * 80)
print(f"\nKey constants:")
print(f"  Z² = 32π/3 = {Z_SQUARED:.6f}")
print(f"  Z = √(32π/3) = {Z_VALUE:.6f}")
print(f"  1/Z = {ONE_OVER_Z:.6f}")
print(f"  π/3 (sphere volume ratio) = {SPHERE_RATIO:.6f}")
print(f"  √(π/3) = {SQRT_PI_OVER_3:.6f}")

# =============================================================================
# LOAD DATA
# =============================================================================

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

            record = {
                'storm_id': storm_id,
                'name': name,
                'year': year,
                'date_time': date_time,
                'lat': lat,
                'lon': lon,
                'vmax': vmax,
                'pmin': pmin,
                'rmw': rmw,
                'eye_diam': eye_diam,
            }
            records.append(record)
            storms[f"{name}_{year}"].append(record)

        except (ValueError, IndexError):
            continue

print(f"Loaded {len(records)} total observations from {len(storms)} storms")

# Filter for valid data
valid_eye_rmw = [r for r in records if r['rmw'] > 0 and r['rmw'] != -99
                 and r['eye_diam'] > 0 and r['eye_diam'] != -99]
valid_pressure_wind = [r for r in records if r['pmin'] > 0 and r['pmin'] != -99
                       and r['vmax'] > 0]
valid_rmw = [r for r in records if r['rmw'] > 0 and r['rmw'] != -99 and r['vmax'] > 0]

print(f"  Valid eye+RMW data: {len(valid_eye_rmw)} observations")
print(f"  Valid pressure+wind data: {len(valid_pressure_wind)} observations")
print(f"  Valid RMW data: {len(valid_rmw)} observations")

# =============================================================================
# ANALYSIS 1: EYE/RMW RATIOS (already falsified)
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 1: EYE/RMW RATIOS")
print("  (Already falsified - documenting for completeness)")
print("=" * 80)

if len(valid_eye_rmw) > 0:
    eye_radii = [r['eye_diam'] / 2.0 for r in valid_eye_rmw]
    rmws = [r['rmw'] for r in valid_eye_rmw]
    ratios = [e / r for e, r in zip(eye_radii, rmws)]

    mean_ratio = np.mean(ratios)
    median_ratio = np.median(ratios)

    print(f"\n  Mean eye/RMW = {mean_ratio:.4f}")
    print(f"  Median eye/RMW = {median_ratio:.4f}")
    print(f"  1/Z prediction = {ONE_OVER_Z:.4f}")
    print(f"  Deviation from 1/Z: {(mean_ratio - ONE_OVER_Z) / ONE_OVER_Z * 100:+.1f}%")
    print(f"\n  STATUS: FALSIFIED (ratio ~ 0.5, not 0.17)")

# =============================================================================
# ANALYSIS 2: PRESSURE-WIND RELATIONSHIPS
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 2: PRESSURE-WIND RELATIONSHIPS")
print("=" * 80)

if len(valid_pressure_wind) > 0:
    # Standard reference: 1013 hPa
    P_REF = 1013.25  # Standard sea level pressure

    pressures = np.array([r['pmin'] for r in valid_pressure_wind])
    winds = np.array([r['vmax'] for r in valid_pressure_wind])

    # Pressure deficit
    delta_p = P_REF - pressures

    # Various relationships to test
    print("\nTesting pressure-wind relationship forms:")

    # V = C * sqrt(delta_P)  -- Physical basis from cyclostrophic balance
    # If V = k * sqrt(delta_P), what is k?
    # k = V / sqrt(delta_P)

    valid_dp = delta_p > 0
    if np.sum(valid_dp) > 100:
        k_values = winds[valid_dp] / np.sqrt(delta_p[valid_dp])
        mean_k = np.mean(k_values)

        print(f"\n  V = k × √(ΔP) relationship:")
        print(f"    Mean k = {mean_k:.4f} kt/√hPa")
        print(f"    Compare to Z = {Z_VALUE:.4f}")
        print(f"    Compare to Z² = {Z_SQUARED:.4f}")
        print(f"    k/Z = {mean_k / Z_VALUE:.4f}")
        print(f"    k²/Z² = {mean_k**2 / Z_SQUARED:.4f}")

        # What about k² ?
        print(f"\n    k² = {mean_k**2:.4f}")
        print(f"    Z² = {Z_SQUARED:.4f}")
        print(f"    k²/Z² = {mean_k**2 / Z_SQUARED:.4f}")

        # Is k close to any Z-related constant?
        for name, val in [('Z', Z_VALUE), ('Z²/Z=Z', Z_VALUE), ('√(Z²)', Z_VALUE),
                          ('Z²', Z_SQUARED), ('1/Z', ONE_OVER_Z), ('π/3', SPHERE_RATIO),
                          ('10', 10), ('√10', np.sqrt(10))]:
            deviation = (mean_k - val) / val * 100
            print(f"    k vs {name} ({val:.4f}): {deviation:+.1f}%")

# =============================================================================
# ANALYSIS 3: RMW RELATIONSHIPS
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 3: RMW vs WIND SPEED RELATIONSHIPS")
print("=" * 80)

if len(valid_rmw) > 0:
    rmws = np.array([r['rmw'] for r in valid_rmw])
    winds = np.array([r['vmax'] for r in valid_rmw])
    lats = np.array([r['lat'] for r in valid_rmw])

    # RMW in nautical miles
    mean_rmw = np.mean(rmws)
    median_rmw = np.median(rmws)

    print(f"\n  RMW Statistics:")
    print(f"    Mean RMW = {mean_rmw:.2f} nm")
    print(f"    Median RMW = {median_rmw:.2f} nm")

    # Is RMW related to Z?
    print(f"\n  RMW vs Z-related constants:")
    print(f"    Mean RMW / 10 = {mean_rmw / 10:.4f}")
    print(f"    Mean RMW / Z = {mean_rmw / Z_VALUE:.4f}")
    print(f"    Mean RMW / Z² = {mean_rmw / Z_SQUARED:.4f}")

    # RMW × f (Coriolis parameter)
    # f = 2Ω sin(lat), Ω = 7.2921e-5 rad/s
    OMEGA = 7.2921e-5
    coriolis = 2 * OMEGA * np.sin(np.radians(lats))
    rmw_km = rmws * 1.852  # Convert nm to km

    # RMW * f has units of velocity
    rmw_f_product = rmw_km * 1000 * coriolis  # m/s

    print(f"\n  RMW × Coriolis parameter:")
    print(f"    Mean RMW × f = {np.mean(rmw_f_product):.4f} m/s")
    print(f"    Compare to Z = {Z_VALUE:.4f}")

    # Ratio of RMW to some reference
    # Typical hurricane scale: 100 km
    rmw_normalized = rmw_km / 100
    print(f"\n  Normalized RMW (/ 100 km):")
    print(f"    Mean = {np.mean(rmw_normalized):.4f}")

# =============================================================================
# ANALYSIS 4: INTENSITY CATEGORIES AND Z²
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 4: INTENSITY CATEGORY THRESHOLDS")
print("=" * 80)

# Saffir-Simpson thresholds (knots)
SS_THRESHOLDS = {
    'TS': 34,
    'Cat 1': 64,
    'Cat 2': 83,
    'Cat 3': 96,
    'Cat 4': 113,
    'Cat 5': 137,
}

print("\nSaffir-Simpson thresholds vs Z constants:")
for cat, thresh in SS_THRESHOLDS.items():
    print(f"  {cat}: {thresh} kt")
    print(f"    / Z = {thresh / Z_VALUE:.4f}")
    print(f"    / Z² = {thresh / Z_SQUARED:.4f}")
    print(f"    / 10 = {thresh / 10:.4f}")

# Are there natural thresholds in the data related to Z?
print("\nChecking if Z² × n = observed thresholds:")
for n in [1, 2, 3, 4, 5]:
    val = Z_SQUARED * n
    print(f"  Z² × {n} = {val:.2f} kt")

print("\nChecking if Z × n = observed thresholds:")
for n in range(5, 25):
    val = Z_VALUE * n
    for cat, thresh in SS_THRESHOLDS.items():
        if abs(val - thresh) / thresh < 0.05:  # Within 5%
            print(f"  Z × {n} = {val:.2f} kt ≈ {cat} ({thresh} kt)")

# =============================================================================
# ANALYSIS 5: EYE + RMW COMBINED ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 5: COMBINED EYE-RMW STRUCTURAL ANALYSIS")
print("=" * 80)

if len(valid_eye_rmw) > 100:
    eyes = np.array([r['eye_diam'] / 2.0 for r in valid_eye_rmw])  # radius
    rmws = np.array([r['rmw'] for r in valid_eye_rmw])
    winds = np.array([r['vmax'] for r in valid_eye_rmw])

    # Eye + RMW = total inner structure width
    total_inner = eyes + rmws
    eyewall_width = rmws - eyes  # Eyewall thickness

    print("\nStructural ratios:")
    print(f"  Mean eye radius = {np.mean(eyes):.2f} nm")
    print(f"  Mean RMW = {np.mean(rmws):.2f} nm")
    print(f"  Mean eyewall width (RMW - eye) = {np.mean(eyewall_width):.2f} nm")

    # New ratios to test
    eyewall_to_eye = eyewall_width / eyes
    eyewall_to_total = eyewall_width / total_inner
    eye_to_total = eyes / total_inner

    # Only valid where eyewall_width > 0
    valid_ew = eyewall_width > 0

    if np.sum(valid_ew) > 50:
        print(f"\n  Eyewall/Eye ratio:")
        print(f"    Mean = {np.mean(eyewall_to_eye[valid_ew]):.4f}")
        print(f"    Median = {np.median(eyewall_to_eye[valid_ew]):.4f}")
        print(f"    vs Z = {Z_VALUE:.4f}")
        print(f"    vs 1/Z = {ONE_OVER_Z:.4f}")

        print(f"\n  Eye/(Eye+RMW) ratio:")
        mean_eye_total = np.mean(eye_to_total[valid_ew])
        print(f"    Mean = {mean_eye_total:.4f}")
        print(f"    vs 1/Z = {ONE_OVER_Z:.4f}")
        print(f"    vs 1/3 = {1/3:.4f}")
        print(f"    vs 1/4 = {0.25:.4f}")

        print(f"\n  Eyewall/(Eye+RMW) ratio:")
        mean_ew_total = np.mean(eyewall_to_total[valid_ew])
        print(f"    Mean = {mean_ew_total:.4f}")
        print(f"    vs (Z-1)/Z = {(Z_VALUE-1)/Z_VALUE:.4f}")

# =============================================================================
# ANALYSIS 6: ANGULAR MOMENTUM RELATIONSHIPS
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 6: ANGULAR MOMENTUM RELATIONSHIPS")
print("=" * 80)

if len(valid_rmw) > 100:
    rmws_km = np.array([r['rmw'] * 1.852 for r in valid_rmw])  # km
    winds_ms = np.array([r['vmax'] * 0.514444 for r in valid_rmw])  # m/s
    lats = np.array([r['lat'] for r in valid_rmw])

    # Angular momentum M = r*V + f*r²/2
    # For simplicity: M ≈ r * V (dominant term at RMW)
    # M = RMW × Vmax (in km × m/s = km²/s × 1000)

    angular_mom = rmws_km * winds_ms  # km × m/s

    print(f"\n  Angular momentum proxy (RMW × Vmax):")
    print(f"    Mean = {np.mean(angular_mom):.2f} km·m/s")
    print(f"    Median = {np.median(angular_mom):.2f} km·m/s")

    # Normalize by something
    mean_am = np.mean(angular_mom)
    print(f"\n  AM / Z² = {mean_am / Z_SQUARED:.2f}")
    print(f"  AM / 1000 = {mean_am / 1000:.4f}")
    print(f"  AM / (Z² × 100) = {mean_am / (Z_SQUARED * 100):.4f}")

# =============================================================================
# ANALYSIS 7: RATIOS BETWEEN WIND RADII
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 7: WIND RADII RATIOS")
print("=" * 80)

# EBTRK also has radii of 34, 50, 64 kt winds (R34, R50, R64)
# These are in columns after eye diameter
# Let's check if these exist

# Parse additional radii
records_with_radii = []
with open(data_file, 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) < 22:  # Need at least 22 columns for R34 in all quadrants
            continue

        try:
            rmw = int(parts[8])
            eye_diam = int(parts[9])

            # R34 NE, SE, SW, NW (columns 14-17 or similar)
            # Format varies - need to check
            if rmw > 0 and rmw != -99:
                record = {
                    'rmw': rmw,
                    'eye_diam': eye_diam,
                    'vmax': int(parts[6]),
                    'pmin': int(parts[7]),
                }
                records_with_radii.append(record)
        except:
            continue

print(f"  Records with RMW data: {len(records_with_radii)}")

# =============================================================================
# ANALYSIS 8: SEARCHING FOR Z² IN DISTRIBUTIONS
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 8: SEARCHING FOR Z² IN DISTRIBUTIONS")
print("=" * 80)

if len(valid_eye_rmw) > 100:
    eyes = np.array([r['eye_diam'] / 2.0 for r in valid_eye_rmw])
    rmws = np.array([r['rmw'] for r in valid_eye_rmw])
    ratios = eyes / rmws

    # What constants best fit the observed ratio distribution?
    test_constants = {
        '1/Z': ONE_OVER_Z,
        '1/6': 1/6,
        '1/5': 1/5,
        '1/4': 1/4,
        '1/3': 1/3,
        '1/π': 1/np.pi,
        '1/e': 1/np.e,
        '1/2': 0.5,
        '1/φ': 1/PHI,
        'φ-1': PHI - 1,  # 0.618
        '2/3': 2/3,
        '√(π/3)/Z': SQRT_PI_OVER_3/Z_VALUE,
        'π/Z²': np.pi/Z_SQUARED,
    }

    print("\nFitting observed eye/RMW distribution to constants:")
    print(f"{'Constant':<20} {'Value':>10} {'Mean Dev':>12} {'t-stat':>10} {'p-value':>12}")
    print("-" * 70)

    results = []
    for name, val in sorted(test_constants.items(), key=lambda x: abs(np.mean(ratios) - x[1])):
        t_stat, p_val = stats.ttest_1samp(ratios, val)
        mean_dev = (np.mean(ratios) - val) / val * 100
        results.append((name, val, mean_dev, t_stat, p_val))
        sig = "" if p_val > 0.05 else "*" if p_val > 0.01 else "**"
        print(f"{name:<20} {val:>10.4f} {mean_dev:>+11.1f}% {t_stat:>10.2f} {p_val:>12.2e} {sig}")

    print("\n  * p < 0.05, ** p < 0.01")
    print("  Closest match (smallest |deviation|) listed first")

# =============================================================================
# ANALYSIS 9: LOOKING FOR Z² IN RATIOS OF MEANS
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 9: RATIOS OF MEAN VALUES")
print("=" * 80)

if len(valid_eye_rmw) > 0 and len(valid_pressure_wind) > 0:
    mean_eye = np.mean([r['eye_diam']/2 for r in valid_eye_rmw])
    mean_rmw = np.mean([r['rmw'] for r in valid_eye_rmw])
    mean_vmax = np.mean([r['vmax'] for r in valid_pressure_wind])
    mean_pmin = np.mean([r['pmin'] for r in valid_pressure_wind])

    print(f"\nMean values:")
    print(f"  Eye radius: {mean_eye:.2f} nm")
    print(f"  RMW: {mean_rmw:.2f} nm")
    print(f"  Vmax: {mean_vmax:.2f} kt")
    print(f"  Pmin: {mean_pmin:.2f} hPa")

    print(f"\nRatios of means:")
    print(f"  mean_eye / mean_rmw = {mean_eye / mean_rmw:.4f}")
    print(f"  mean_vmax / Z = {mean_vmax / Z_VALUE:.4f}")
    print(f"  mean_vmax / Z² = {mean_vmax / Z_SQUARED:.4f}")
    print(f"  (1013 - mean_pmin) / Z² = {(1013 - mean_pmin) / Z_SQUARED:.4f}")
    print(f"  mean_rmw / Z = {mean_rmw / Z_VALUE:.4f}")
    print(f"  mean_rmw / Z² = {mean_rmw / Z_SQUARED:.4f}")

# =============================================================================
# ANALYSIS 10: LINEAR FIT EYE = a*RMW + b
# =============================================================================

print("\n" + "=" * 80)
print("  ANALYSIS 10: LINEAR EYE-RMW RELATIONSHIP")
print("=" * 80)

if len(valid_eye_rmw) > 100:
    eyes = np.array([r['eye_diam'] / 2.0 for r in valid_eye_rmw])
    rmws = np.array([r['rmw'] for r in valid_eye_rmw])

    # Linear fit: eye = a * rmw + b
    slope, intercept, r_value, p_value, std_err = stats.linregress(rmws, eyes)

    print(f"\n  Linear fit: Eye_radius = {slope:.4f} × RMW + {intercept:.4f}")
    print(f"  R² = {r_value**2:.4f}")
    print(f"  p-value = {p_value:.2e}")

    print(f"\n  Coefficients vs Z-related constants:")
    print(f"    Slope = {slope:.4f}")
    print(f"    1/Z = {ONE_OVER_Z:.4f}")
    print(f"    Slope vs 1/Z: {(slope - ONE_OVER_Z)/ONE_OVER_Z*100:+.1f}%")

    print(f"\n    Intercept = {intercept:.4f} nm")
    print(f"    Z = {Z_VALUE:.4f}")
    print(f"    Z² = {Z_SQUARED:.4f}")
    print(f"    Intercept/Z = {intercept/Z_VALUE:.4f}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("  SUMMARY: Z² / 8D MANIFOLD IN HURRICANE DATA")
print("=" * 80)

print("""
FINDINGS:

1. EYE/RMW = 1/Z PREDICTION: FALSIFIED
   - Observed mean: ~0.58, predicted: 0.173
   - Flight reconnaissance data definitively rejects this

2. OTHER Z² RELATIONSHIPS: See analysis above
   - Various ratios and relationships tested
   - Need to identify if any show significant Z² signal

3. THE MATHEMATICAL FRAMEWORK REMAINS VALID:
   - Z² = 32π/3 = 32 × Vol(S⁷)/Vol(S⁵) is exact
   - Question: Does it describe any physical hurricane property?

NEXT STEPS:
1. Review which analyses show smallest deviation from Z-related constants
2. Test any promising relationships on independent data (Pacific, other years)
3. Investigate theoretical basis for any observed relationships
""")

print("=" * 80)
print("  Analysis complete")
print("=" * 80)
