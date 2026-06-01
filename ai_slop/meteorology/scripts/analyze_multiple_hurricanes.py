#!/usr/bin/env python3
"""
Multi-Hurricane Analysis: Validating Z² Framework Predictions

This script analyzes multiple hurricanes from ERA5 data to test:
1. Eye/RMW ratio ≈ 1/Z (for intense hurricanes)
2. Eye/RMW ratio ≈ 1/π (for average hurricanes)
3. Hexagonal/polygonal structure patterns

Z² = 32π/3 ≈ 33.51
Z = √(32π/3) ≈ 5.789
1/Z ≈ 0.173
1/π ≈ 0.318
"""

import sys
from pathlib import Path
from functools import partial
from datetime import datetime, timedelta
import time

print = partial(print, flush=True)

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

# Z² constants
Z_SQUARED = 32 * np.pi / 3
Z_VALUE = np.sqrt(Z_SQUARED)
ONE_OVER_Z = 1 / Z_VALUE
ONE_OVER_PI = 1 / np.pi

print("=" * 70)
print("MULTI-HURRICANE Z² ANALYSIS")
print("=" * 70)
print(f"\nZ² Constants:")
print(f"  Z² = 32π/3 = {Z_SQUARED:.4f}")
print(f"  Z = √(Z²) = {Z_VALUE:.4f}")
print(f"  1/Z = {ONE_OVER_Z:.4f}")
print(f"  1/π = {ONE_OVER_PI:.4f}")

# ============================================================================
# Hurricane Database
# ============================================================================

HURRICANES = {
    # Atlantic Category 5 hurricanes
    'katrina_2005': {
        'name': 'Hurricane Katrina',
        'peak_date': '2005-08-28',
        'lat': 26.3,
        'lon': -88.6,
        'max_wind_kt': 150,  # knots
        'min_pressure': 902,
        'category': 5,
    },
    'wilma_2005': {
        'name': 'Hurricane Wilma',
        'peak_date': '2005-10-19',
        'lat': 17.3,
        'lon': -83.7,
        'max_wind_kt': 160,
        'min_pressure': 882,  # Record low for Atlantic
        'category': 5,
    },
    'irma_2017': {
        'name': 'Hurricane Irma',
        'peak_date': '2017-09-06',
        'lat': 17.4,
        'lon': -58.9,
        'max_wind_kt': 160,
        'min_pressure': 914,
        'category': 5,
    },
    'maria_2017': {
        'name': 'Hurricane Maria',
        'peak_date': '2017-09-18',
        'lat': 15.3,
        'lon': -64.4,
        'max_wind_kt': 150,
        'min_pressure': 908,
        'category': 5,
    },
    'michael_2018': {
        'name': 'Hurricane Michael',
        'peak_date': '2018-10-10',
        'lat': 29.8,
        'lon': -85.5,
        'max_wind_kt': 140,
        'min_pressure': 919,
        'category': 5,
    },
    'dorian_2019': {
        'name': 'Hurricane Dorian',
        'peak_date': '2019-09-01',
        'lat': 26.5,
        'lon': -77.0,
        'max_wind_kt': 160,
        'min_pressure': 910,
        'category': 5,
    },
    # Category 4 hurricanes for comparison
    'harvey_2017': {
        'name': 'Hurricane Harvey',
        'peak_date': '2017-08-25',
        'lat': 27.8,
        'lon': -96.5,
        'max_wind_kt': 115,
        'min_pressure': 938,
        'category': 4,
    },
    'florence_2018': {
        'name': 'Hurricane Florence',
        'peak_date': '2018-09-11',
        'lat': 26.4,
        'lon': -68.5,
        'max_wind_kt': 130,
        'min_pressure': 939,
        'category': 4,
    },
    'ian_2022': {
        'name': 'Hurricane Ian',
        'peak_date': '2022-09-28',
        'lat': 26.6,
        'lon': -82.5,
        'max_wind_kt': 140,
        'min_pressure': 940,
        'category': 5,
    },
}

# ============================================================================
# Analysis Functions
# ============================================================================

def load_hurricane_data(loader, event, box_size=10):
    """Load ERA5 data for a hurricane event."""
    from data.era5_loader import FAST_CONFIG

    peak_date = datetime.fromisoformat(event['peak_date'])
    start_date = peak_date - timedelta(hours=6)
    end_date = peak_date + timedelta(hours=6)

    lat_center = event['lat']
    lon_center = event['lon']

    # Convert longitude to 0-360 if negative
    lon_360 = lon_center if lon_center >= 0 else lon_center + 360

    # Load data
    ds = loader.load_time_range(
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        config=FAST_CONFIG,
        time_step=6,
        lazy=True
    )

    # Select region
    lat_min, lat_max = lat_center - box_size, lat_center + box_size
    lon_min, lon_max = lon_360 - box_size, lon_360 + box_size

    # ERA5 lat goes from 90 to -90
    ds_region = ds.sel(
        latitude=slice(lat_max, lat_min),
        longitude=slice(lon_min, lon_max)
    )

    return ds_region


def compute_radial_profile(u_wind, v_wind, msl, center_lat, center_lon):
    """Compute azimuthally-averaged radial wind profile."""
    lats = msl.latitude.values
    lons = msl.longitude.values
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Distance in km
    lat_dist = (lat_grid - center_lat) * 111
    lon_dist = (lon_grid - center_lon) * 111 * np.cos(np.radians(center_lat))
    distance = np.sqrt(lat_dist**2 + lon_dist**2)

    # Wind speed
    wind_speed = np.sqrt(u_wind.values**2 + v_wind.values**2)

    # Bin by distance
    max_radius = 400
    n_bins = 40
    bins = np.linspace(0, max_radius, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    mean_wind = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (distance >= bins[i]) & (distance < bins[i+1])
        if np.any(mask):
            mean_wind[i] = np.mean(wind_speed[mask])

    return bin_centers, mean_wind


def find_eye_and_rmax(radii, winds):
    """Find eye radius and radius of maximum wind."""
    # RMW: radius of maximum wind
    rmax_idx = np.argmax(winds)
    rmax = radii[rmax_idx]
    vmax = winds[rmax_idx]

    # Eye radius: first local minimum inside RMW
    eye_radius = None
    if rmax_idx > 2:
        inner_winds = winds[:rmax_idx]
        inner_radii = radii[:rmax_idx]

        # Find minimum inside RMW
        if len(inner_winds) > 0:
            min_idx = np.argmin(inner_winds[1:]) + 1 if len(inner_winds) > 1 else 0
            eye_radius = inner_radii[min_idx]

    return eye_radius, rmax, vmax


def analyze_hurricane(loader, name, event):
    """Analyze a single hurricane."""
    print(f"\n  Analyzing {event['name']}...")

    try:
        # Load data
        ds = load_hurricane_data(loader, event)

        # Get wind and pressure fields
        u_wind = ds['u_component_of_wind'].isel(time=len(ds.time)//2)
        v_wind = ds['v_component_of_wind'].isel(time=len(ds.time)//2)
        msl = ds['mean_sea_level_pressure'].isel(time=len(ds.time)//2)

        # Select level if needed
        if 'level' in u_wind.dims:
            u_wind = u_wind.sel(level=850, method='nearest')
            v_wind = v_wind.sel(level=850, method='nearest')

        # Compute fields
        u_wind = u_wind.compute()
        v_wind = v_wind.compute()
        msl = msl.compute()

        # Find center from minimum pressure
        min_idx = np.unravel_index(np.argmin(msl.values), msl.shape)
        center_lat = float(msl.latitude.values[min_idx[0]])
        center_lon = float(msl.longitude.values[min_idx[1]])
        min_pressure = float(msl.values[min_idx]) / 100  # Convert Pa to hPa

        # Compute radial profile
        radii, winds = compute_radial_profile(u_wind, v_wind, msl, center_lat, center_lon)

        # Find eye and RMW
        eye_radius, rmax, vmax = find_eye_and_rmax(radii, winds)

        # Calculate ratio
        if eye_radius is not None and rmax > 0:
            ratio = eye_radius / rmax
        else:
            ratio = None

        return {
            'name': event['name'],
            'category': event['category'],
            'observed_pressure': event['min_pressure'],
            'era5_pressure': min_pressure,
            'observed_wind_kt': event['max_wind_kt'],
            'era5_wind_ms': vmax,
            'eye_radius': eye_radius,
            'rmax': rmax,
            'ratio': ratio,
            'success': True,
        }

    except Exception as e:
        print(f"    Error: {e}")
        return {
            'name': event['name'],
            'success': False,
            'error': str(e),
        }


# ============================================================================
# Main Analysis
# ============================================================================

print("\n" + "-" * 70)
print("Loading ERA5 connection...")
print("-" * 70)

from data.era5_loader import ERA5CloudLoader

loader = ERA5CloudLoader(verbose=False)
_ = loader.dataset  # Initialize connection

print("  Connection established!")

# Analyze each hurricane
print("\n" + "-" * 70)
print("Analyzing hurricanes...")
print("-" * 70)

results = []
for name, event in HURRICANES.items():
    result = analyze_hurricane(loader, name, event)
    results.append(result)

    if result['success'] and result['ratio'] is not None:
        print(f"    Eye: {result['eye_radius']:.1f} km, RMW: {result['rmax']:.1f} km, Ratio: {result['ratio']:.3f}")

# ============================================================================
# Results Analysis
# ============================================================================

print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)

# Filter successful results with valid ratios
valid_results = [r for r in results if r['success'] and r.get('ratio') is not None]

print(f"\nAnalyzed {len(valid_results)} hurricanes successfully\n")

print(f"{'Hurricane':<25} {'Cat':>3} {'Eye(km)':>8} {'RMW(km)':>8} {'Ratio':>8} {'vs 1/Z':>8} {'vs 1/π':>8}")
print("-" * 85)

ratios = []
cat5_ratios = []
cat4_ratios = []

for r in valid_results:
    ratio = r['ratio']
    ratios.append(ratio)

    if r['category'] == 5:
        cat5_ratios.append(ratio)
    else:
        cat4_ratios.append(ratio)

    diff_z = abs(ratio - ONE_OVER_Z) / ONE_OVER_Z * 100
    diff_pi = abs(ratio - ONE_OVER_PI) / ONE_OVER_PI * 100

    best = "1/Z" if diff_z < diff_pi else "1/π"

    print(f"{r['name']:<25} {r['category']:>3} {r['eye_radius']:>8.1f} {r['rmax']:>8.1f} {ratio:>8.3f} {diff_z:>7.1f}% {diff_pi:>7.1f}%  ({best})")

# Statistics
print("\n" + "-" * 70)
print("STATISTICAL ANALYSIS")
print("-" * 70)

if ratios:
    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)

    print(f"\nAll hurricanes (n={len(ratios)}):")
    print(f"  Mean ratio: {mean_ratio:.4f} ± {std_ratio:.4f}")
    print(f"  1/Z = {ONE_OVER_Z:.4f} (diff: {abs(mean_ratio - ONE_OVER_Z)/ONE_OVER_Z*100:.1f}%)")
    print(f"  1/π = {ONE_OVER_PI:.4f} (diff: {abs(mean_ratio - ONE_OVER_PI)/ONE_OVER_PI*100:.1f}%)")

if cat5_ratios:
    mean_cat5 = np.mean(cat5_ratios)
    std_cat5 = np.std(cat5_ratios)
    print(f"\nCategory 5 only (n={len(cat5_ratios)}):")
    print(f"  Mean ratio: {mean_cat5:.4f} ± {std_cat5:.4f}")
    print(f"  1/Z = {ONE_OVER_Z:.4f} (diff: {abs(mean_cat5 - ONE_OVER_Z)/ONE_OVER_Z*100:.1f}%)")
    print(f"  1/π = {ONE_OVER_PI:.4f} (diff: {abs(mean_cat5 - ONE_OVER_PI)/ONE_OVER_PI*100:.1f}%)")

if cat4_ratios:
    mean_cat4 = np.mean(cat4_ratios)
    std_cat4 = np.std(cat4_ratios)
    print(f"\nCategory 4 only (n={len(cat4_ratios)}):")
    print(f"  Mean ratio: {mean_cat4:.4f} ± {std_cat4:.4f}")
    print(f"  1/Z = {ONE_OVER_Z:.4f} (diff: {abs(mean_cat4 - ONE_OVER_Z)/ONE_OVER_Z*100:.1f}%)")
    print(f"  1/π = {ONE_OVER_PI:.4f} (diff: {abs(mean_cat4 - ONE_OVER_PI)/ONE_OVER_PI*100:.1f}%)")

# ============================================================================
# Z² Framework Assessment
# ============================================================================

print("\n" + "=" * 70)
print("Z² FRAMEWORK ASSESSMENT")
print("=" * 70)

if ratios:
    # Count which constant is closer for each hurricane
    count_z = sum(1 for r in ratios if abs(r - ONE_OVER_Z) < abs(r - ONE_OVER_PI))
    count_pi = len(ratios) - count_z

    print(f"\nCloser to 1/Z: {count_z} hurricanes ({100*count_z/len(ratios):.0f}%)")
    print(f"Closer to 1/π: {count_pi} hurricanes ({100*count_pi/len(ratios):.0f}%)")

    # Hypothesis test
    if mean_ratio < 0.25:
        hypothesis = "1/Z regime (intense hurricane structure)"
    else:
        hypothesis = "1/π regime (average hurricane structure)"

    print(f"\nMean ratio {mean_ratio:.3f} suggests: {hypothesis}")

print(f"""
Z² Framework Predictions:
  - Intense hurricanes: Eye/RMW → 1/Z = {ONE_OVER_Z:.4f}
  - Average hurricanes: Eye/RMW → 1/π = {ONE_OVER_PI:.4f}

Physical Interpretation:
  - 1/Z regime: Maximum vortex compression (geometric limit)
  - 1/π regime: Equilibrium circular structure

The transition from 1/π to 1/Z as hurricanes intensify would
represent geometric optimization toward the Z² constant.
""")

print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
