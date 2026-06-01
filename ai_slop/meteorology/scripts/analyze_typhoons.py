#!/usr/bin/env python3
"""
Typhoon Analysis: Extending Z² Framework to Western Pacific

Typhoons are the same meteorological phenomenon as hurricanes,
just occurring in the Western Pacific. They should exhibit the
same 1/Z eye structure ratio if the Z² framework is universal.

Key typhoons analyzed:
- Haiyan 2013: Strongest at landfall (195 kt)
- Tip 1979: Largest ever recorded
- Goni 2020: Strongest of 2020 season
- Noru 2022: Underwent rapid intensification
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
print("TYPHOON Z² ANALYSIS - WESTERN PACIFIC")
print("=" * 70)
print(f"\nZ² Constants:")
print(f"  1/Z = {ONE_OVER_Z:.4f} (prediction)")
print(f"  1/π = {ONE_OVER_PI:.4f} (alternative)")

# ============================================================================
# Typhoon Database
# ============================================================================

TYPHOONS = {
    # Super Typhoons
    'haiyan_2013': {
        'name': 'Super Typhoon Haiyan',
        'peak_date': '2013-11-07',
        'lat': 11.2,
        'lon': 125.0,  # Near Philippines
        'max_wind_kt': 195,  # Strongest at landfall
        'min_pressure': 895,
        'category': 'Super',
        'basin': 'WPAC',
    },
    'goni_2020': {
        'name': 'Super Typhoon Goni',
        'peak_date': '2020-10-31',
        'lat': 13.5,
        'lon': 124.0,
        'max_wind_kt': 180,
        'min_pressure': 905,
        'category': 'Super',
        'basin': 'WPAC',
    },
    'hagupit_2014': {
        'name': 'Typhoon Hagupit',
        'peak_date': '2014-12-04',
        'lat': 10.5,
        'lon': 132.0,
        'max_wind_kt': 150,
        'min_pressure': 920,
        'category': 'Super',
        'basin': 'WPAC',
    },
    'mangkhut_2018': {
        'name': 'Super Typhoon Mangkhut',
        'peak_date': '2018-09-13',
        'lat': 17.5,
        'lon': 133.0,
        'max_wind_kt': 160,
        'min_pressure': 905,
        'category': 'Super',
        'basin': 'WPAC',
    },
    'noru_2022': {
        'name': 'Super Typhoon Noru',
        'peak_date': '2022-09-24',
        'lat': 15.5,
        'lon': 122.0,
        'max_wind_kt': 150,
        'min_pressure': 915,
        'category': 'Super',
        'basin': 'WPAC',
    },
    'rai_2021': {
        'name': 'Super Typhoon Rai',
        'peak_date': '2021-12-16',
        'lat': 10.0,
        'lon': 127.0,
        'max_wind_kt': 160,
        'min_pressure': 915,
        'category': 'Super',
        'basin': 'WPAC',
    },
}

# ============================================================================
# Analysis Functions (same as hurricane analysis)
# ============================================================================

def load_typhoon_data(loader, event, box_size=10):
    """Load ERA5 data for a typhoon event."""
    from data.era5_loader import FAST_CONFIG

    peak_date = datetime.fromisoformat(event['peak_date'])
    start_date = peak_date - timedelta(hours=6)
    end_date = peak_date + timedelta(hours=6)

    lat_center = event['lat']
    lon_center = event['lon']

    # Typhoons are already in 0-360 longitude (Western Pacific)
    lon_360 = lon_center if lon_center >= 0 else lon_center + 360

    ds = loader.load_time_range(
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        config=FAST_CONFIG,
        time_step=6,
        lazy=True
    )

    lat_min, lat_max = lat_center - box_size, lat_center + box_size
    lon_min, lon_max = lon_360 - box_size, lon_360 + box_size

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

    lat_dist = (lat_grid - center_lat) * 111
    lon_dist = (lon_grid - center_lon) * 111 * np.cos(np.radians(center_lat))
    distance = np.sqrt(lat_dist**2 + lon_dist**2)

    wind_speed = np.sqrt(u_wind.values**2 + v_wind.values**2)

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
    rmax_idx = np.argmax(winds)
    rmax = radii[rmax_idx]
    vmax = winds[rmax_idx]

    eye_radius = None
    if rmax_idx > 2:
        inner_winds = winds[:rmax_idx]
        inner_radii = radii[:rmax_idx]

        if len(inner_winds) > 0:
            min_idx = np.argmin(inner_winds[1:]) + 1 if len(inner_winds) > 1 else 0
            eye_radius = inner_radii[min_idx]

    return eye_radius, rmax, vmax


def analyze_typhoon(loader, name, event):
    """Analyze a single typhoon."""
    print(f"\n  Analyzing {event['name']}...")

    try:
        ds = load_typhoon_data(loader, event)

        u_wind = ds['u_component_of_wind'].isel(time=len(ds.time)//2)
        v_wind = ds['v_component_of_wind'].isel(time=len(ds.time)//2)
        msl = ds['mean_sea_level_pressure'].isel(time=len(ds.time)//2)

        if 'level' in u_wind.dims:
            u_wind = u_wind.sel(level=850, method='nearest')
            v_wind = v_wind.sel(level=850, method='nearest')

        u_wind = u_wind.compute()
        v_wind = v_wind.compute()
        msl = msl.compute()

        min_idx = np.unravel_index(np.argmin(msl.values), msl.shape)
        center_lat = float(msl.latitude.values[min_idx[0]])
        center_lon = float(msl.longitude.values[min_idx[1]])
        min_pressure = float(msl.values[min_idx]) / 100

        radii, winds = compute_radial_profile(u_wind, v_wind, msl, center_lat, center_lon)
        eye_radius, rmax, vmax = find_eye_and_rmax(radii, winds)

        if eye_radius is not None and rmax > 0:
            ratio = eye_radius / rmax
        else:
            ratio = None

        return {
            'name': event['name'],
            'category': event['category'],
            'basin': event['basin'],
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
_ = loader.dataset

print("  Connection established!")

print("\n" + "-" * 70)
print("Analyzing typhoons...")
print("-" * 70)

results = []
for name, event in TYPHOONS.items():
    result = analyze_typhoon(loader, name, event)
    results.append(result)

    if result['success'] and result['ratio'] is not None:
        print(f"    Eye: {result['eye_radius']:.1f} km, RMW: {result['rmax']:.1f} km, Ratio: {result['ratio']:.3f}")

# ============================================================================
# Results
# ============================================================================

print("\n" + "=" * 70)
print("TYPHOON RESULTS")
print("=" * 70)

valid_results = [r for r in results if r['success'] and r.get('ratio') is not None]

print(f"\nAnalyzed {len(valid_results)} typhoons successfully\n")

print(f"{'Typhoon':<30} {'Cat':>6} {'Eye(km)':>8} {'RMW(km)':>8} {'Ratio':>8} {'vs 1/Z':>8}")
print("-" * 80)

ratios = []
for r in valid_results:
    ratio = r['ratio']
    ratios.append(ratio)

    diff_z = abs(ratio - ONE_OVER_Z) / ONE_OVER_Z * 100
    diff_pi = abs(ratio - ONE_OVER_PI) / ONE_OVER_PI * 100

    best = "1/Z" if diff_z < diff_pi else "1/π"

    print(f"{r['name']:<30} {r['category']:>6} {r['eye_radius']:>8.1f} {r['rmax']:>8.1f} {ratio:>8.3f} {diff_z:>7.1f}%  ({best})")

# Statistics
print("\n" + "-" * 70)
print("STATISTICAL ANALYSIS")
print("-" * 70)

if ratios:
    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)

    print(f"\nAll typhoons (n={len(ratios)}):")
    print(f"  Mean ratio: {mean_ratio:.4f} ± {std_ratio:.4f}")
    print(f"  1/Z = {ONE_OVER_Z:.4f} (diff: {abs(mean_ratio - ONE_OVER_Z)/ONE_OVER_Z*100:.1f}%)")
    print(f"  1/π = {ONE_OVER_PI:.4f} (diff: {abs(mean_ratio - ONE_OVER_PI)/ONE_OVER_PI*100:.1f}%)")

    count_z = sum(1 for r in ratios if abs(r - ONE_OVER_Z) < abs(r - ONE_OVER_PI))
    count_pi = len(ratios) - count_z

    print(f"\nCloser to 1/Z: {count_z} typhoons ({100*count_z/len(ratios):.0f}%)")
    print(f"Closer to 1/π: {count_pi} typhoons ({100*count_pi/len(ratios):.0f}%)")

print("\n" + "=" * 70)
print("COMBINED ATLANTIC + PACIFIC ANALYSIS")
print("=" * 70)

# Load hurricane results if available
print("""
If typhoon results match hurricane results (mean ≈ 1/Z = 0.173),
this confirms the Z² framework is UNIVERSAL across:
- Atlantic hurricanes
- Western Pacific typhoons
- Both hemispheres

The same geometric constant 1/Z appears regardless of:
- Basin location
- Storm size
- Absolute intensity
""")

print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
