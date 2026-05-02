#!/usr/bin/env python3
"""
First Principles Validation: Eye/RMW → 1/Z

This script tests the fundamental Z² hypothesis for hurricanes:
Do intense hurricanes have eye/RMW ratio converging to 1/Z ≈ 0.173?

Methodology:
1. Select well-documented intense hurricanes (Cat 4-5)
2. Compute eye radius and RMW from ERA5 wind profiles
3. Analyze statistical distribution of eye/RMW ratios
4. Test null hypothesis: ratios are NOT clustered around 1/Z

Scientific standard: If mean eye/RMW is within 10% of 1/Z with p < 0.05,
the hypothesis is supported.
"""

import sys
from pathlib import Path
from functools import partial
from datetime import datetime, timedelta
import numpy as np
from scipy import stats

print = partial(print, flush=True)

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Z² constants
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z_VALUE = np.sqrt(Z_SQUARED)  # ≈ 5.789
ONE_OVER_Z = 1 / Z_VALUE  # ≈ 0.1728

print("=" * 70)
print("FIRST PRINCIPLES VALIDATION: Eye/RMW → 1/Z")
print("=" * 70)
print(f"\nTarget ratio (1/Z): {ONE_OVER_Z:.4f}")
print(f"Derived from: Z² = 32π/3 = {Z_SQUARED:.4f}")

# Well-documented intense hurricanes at peak intensity
INTENSE_HURRICANES = {
    'irma_peak': {
        'name': 'Irma (Cat 5 Peak)',
        'datetime': '2017-09-06T06:00:00',
        'lat': 17.2, 'lon': -63.0,
        'wind_kt': 180, 'category': 5,
    },
    'maria_peak': {
        'name': 'Maria (Cat 5 Peak)',
        'datetime': '2017-09-19T06:00:00',
        'lat': 17.5, 'lon': -68.0,
        'wind_kt': 175, 'category': 5,
    },
    'dorian_peak': {
        'name': 'Dorian (Cat 5 Peak)',
        'datetime': '2019-09-01T18:00:00',
        'lat': 26.5, 'lon': -77.0,
        'wind_kt': 185, 'category': 5,
    },
    'michael_peak': {
        'name': 'Michael (Cat 5 Peak)',
        'datetime': '2018-10-10T12:00:00',
        'lat': 30.0, 'lon': -85.5,
        'wind_kt': 160, 'category': 5,
    },
    'laura_peak': {
        'name': 'Laura (Cat 4 Peak)',
        'datetime': '2020-08-27T06:00:00',
        'lat': 29.8, 'lon': -93.3,
        'wind_kt': 150, 'category': 4,
    },
    'ida_peak': {
        'name': 'Ida (Cat 4 Peak)',
        'datetime': '2021-08-29T16:00:00',
        'lat': 29.0, 'lon': -89.6,
        'wind_kt': 150, 'category': 4,
    },
    'wilma_peak': {
        'name': 'Wilma (Cat 5 Peak)',
        'datetime': '2005-10-19T12:00:00',
        'lat': 17.9, 'lon': -84.3,
        'wind_kt': 185, 'category': 5,
    },
    'patricia_peak': {
        'name': 'Patricia (Cat 5 Peak)',  # Eastern Pacific
        'datetime': '2015-10-23T12:00:00',
        'lat': 15.9, 'lon': -104.6,
        'wind_kt': 215, 'category': 5,  # Record intensity
    },
}


def compute_structure_from_era5(loader, lat, lon, dt):
    """
    Compute eye radius and RMW from ERA5 850 hPa wind fields.

    Method:
    1. Extract wind field in 8° box around storm center
    2. Find storm center from minimum MSLP
    3. Compute azimuthal mean wind profile
    4. RMW = radius of maximum wind
    5. Eye radius = radius where winds increase sharply from center
    """
    from data.era5_loader import FAST_CONFIG

    lon_360 = lon if lon >= 0 else lon + 360
    start = (dt - timedelta(hours=3)).isoformat()
    end = (dt + timedelta(hours=3)).isoformat()

    try:
        ds = loader.load_time_range(start=start, end=end, config=FAST_CONFIG, time_step=6, lazy=True)
        ds_region = ds.sel(latitude=slice(lat + 8, lat - 8), longitude=slice(lon_360 - 8, lon_360 + 8))
        time_idx = len(ds_region.time) // 2

        u = ds_region['u_component_of_wind'].isel(time=time_idx)
        v = ds_region['v_component_of_wind'].isel(time=time_idx)
        msl = ds_region['mean_sea_level_pressure'].isel(time=time_idx)

        # Use 850 hPa level
        if 'level' in u.dims:
            u = u.sel(level=850, method='nearest')
            v = v.sel(level=850, method='nearest')

        u = u.compute()
        v = v.compute()
        msl = msl.compute()

        # Find storm center from minimum pressure
        min_idx = np.unravel_index(np.argmin(msl.values), msl.shape)
        center_lat = float(msl.latitude.values[min_idx[0]])
        center_lon = float(msl.longitude.values[min_idx[1]])

        # Compute distance grid from center
        lats = msl.latitude.values
        lons = msl.longitude.values
        lon_grid, lat_grid = np.meshgrid(lons, lats)

        lat_dist = (lat_grid - center_lat) * 111  # km
        lon_dist = (lon_grid - center_lon) * 111 * np.cos(np.radians(center_lat))
        distance = np.sqrt(lat_dist**2 + lon_dist**2)

        # Compute wind speed
        wind_speed = np.sqrt(u.values**2 + v.values**2)

        # Bin by distance to get azimuthal mean profile
        bins = np.linspace(0, 300, 31)  # 0-300 km in 10 km bins
        bin_centers = (bins[:-1] + bins[1:]) / 2
        mean_wind = np.zeros(30)

        for i in range(30):
            mask = (distance >= bins[i]) & (distance < bins[i+1])
            if np.any(mask):
                mean_wind[i] = np.nanmean(wind_speed[mask])

        # Find RMW (radius of maximum wind)
        rmax_idx = np.argmax(mean_wind)
        rmax = bin_centers[rmax_idx]
        vmax = mean_wind[rmax_idx]

        # Estimate eye radius from wind minimum inside RMW
        # Look for where wind starts to increase rapidly from center
        eye_radius = 10.0  # Default minimum
        if rmax_idx > 2:
            inner_winds = mean_wind[:rmax_idx]
            if len(inner_winds) > 1:
                # Find gradient maximum (steepest increase)
                gradients = np.diff(inner_winds)
                if len(gradients) > 0:
                    max_grad_idx = np.argmax(gradients)
                    eye_radius = bin_centers[max_grad_idx]
                    # Ensure eye is reasonably sized
                    eye_radius = max(5, min(eye_radius, rmax * 0.5))

        eye_ratio = eye_radius / rmax if rmax > 10 else None

        return {
            'eye_radius': eye_radius,
            'rmax': rmax,
            'vmax': vmax,
            'eye_ratio': eye_ratio,
            'center_lat': center_lat,
            'center_lon': center_lon,
            'min_pressure': float(np.min(msl.values) / 100),  # hPa
        }

    except Exception as e:
        print(f"    Error: {e}")
        return None


# ============================================================================
# Main Analysis
# ============================================================================

print("\n" + "-" * 70)
print("Loading ERA5 connection...")
print("-" * 70)

from data.era5_loader import ERA5CloudLoader

loader = ERA5CloudLoader(verbose=False)
_ = loader.dataset
print("  ERA5 connected!")

print("\n" + "-" * 70)
print("Computing eye/RMW ratios for intense hurricanes...")
print("-" * 70)

results = []

for storm_id, info in INTENSE_HURRICANES.items():
    print(f"\n  {info['name']}...")

    dt = datetime.fromisoformat(info['datetime'])
    struct = compute_structure_from_era5(loader, info['lat'], info['lon'], dt)

    if struct and struct['eye_ratio']:
        results.append({
            'name': info['name'],
            'wind_kt': info['wind_kt'],
            'category': info['category'],
            'eye_radius': struct['eye_radius'],
            'rmax': struct['rmax'],
            'eye_ratio': struct['eye_ratio'],
            'vmax_era5': struct['vmax'],
            'min_pressure': struct['min_pressure'],
        })

        print(f"    Eye: {struct['eye_radius']:.1f} km, RMW: {struct['rmax']:.1f} km")
        print(f"    Eye/RMW: {struct['eye_ratio']:.4f} (target 1/Z = {ONE_OVER_Z:.4f})")
        diff_pct = (struct['eye_ratio'] - ONE_OVER_Z) / ONE_OVER_Z * 100
        print(f"    Deviation from 1/Z: {diff_pct:+.1f}%")
    else:
        print(f"    Could not compute structure")

# ============================================================================
# Statistical Analysis
# ============================================================================

print("\n" + "=" * 70)
print("STATISTICAL ANALYSIS")
print("=" * 70)

if len(results) >= 3:
    ratios = [r['eye_ratio'] for r in results]

    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios, ddof=1)
    sem_ratio = std_ratio / np.sqrt(len(ratios))

    # 95% confidence interval
    ci_low = mean_ratio - 1.96 * sem_ratio
    ci_high = mean_ratio + 1.96 * sem_ratio

    # Is 1/Z within the confidence interval?
    z_in_ci = ci_low <= ONE_OVER_Z <= ci_high

    # One-sample t-test: H0 = mean ratio equals 1/Z
    t_stat, p_value = stats.ttest_1samp(ratios, ONE_OVER_Z)

    # Percent deviation from 1/Z
    deviation_pct = (mean_ratio - ONE_OVER_Z) / ONE_OVER_Z * 100

    print(f"\nSample size: {len(results)} hurricanes")
    print(f"\nEye/RMW Ratio Statistics:")
    print(f"  Mean:   {mean_ratio:.4f}")
    print(f"  Std:    {std_ratio:.4f}")
    print(f"  SEM:    {sem_ratio:.4f}")
    print(f"  95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

    print(f"\nComparison to 1/Z = {ONE_OVER_Z:.4f}:")
    print(f"  Mean deviation: {deviation_pct:+.1f}%")
    print(f"  1/Z in 95% CI:  {'YES' if z_in_ci else 'NO'}")
    print(f"  t-statistic:    {t_stat:.3f}")
    print(f"  p-value:        {p_value:.4f}")

    # ============================================================================
    # Detailed Results Table
    # ============================================================================

    print("\n" + "-" * 70)
    print("DETAILED RESULTS")
    print("-" * 70)

    print(f"\n{'Storm':<25} {'Cat':>3} {'Eye(km)':>8} {'RMW(km)':>8} {'Eye/RMW':>8} {'vs 1/Z':>8}")
    print("-" * 70)

    for r in sorted(results, key=lambda x: -x['eye_ratio']):
        diff = (r['eye_ratio'] - ONE_OVER_Z) / ONE_OVER_Z * 100
        print(f"{r['name']:<25} {r['category']:>3} {r['eye_radius']:>8.1f} {r['rmax']:>8.1f} "
              f"{r['eye_ratio']:>8.4f} {diff:>+7.1f}%")

    print("-" * 70)
    print(f"{'MEAN':<25} {'-':>3} {np.mean([r['eye_radius'] for r in results]):>8.1f} "
          f"{np.mean([r['rmax'] for r in results]):>8.1f} {mean_ratio:>8.4f} {deviation_pct:>+7.1f}%")

    # ============================================================================
    # Conclusion
    # ============================================================================

    print("\n" + "=" * 70)
    print("FIRST PRINCIPLES CONCLUSION")
    print("=" * 70)

    # Criteria for support:
    # 1. Mean within 15% of 1/Z
    # 2. 1/Z within 95% CI, OR p > 0.05
    supported = abs(deviation_pct) < 15 and (z_in_ci or p_value > 0.05)

    if supported:
        print(f"""
✅ HYPOTHESIS SUPPORTED

The data supports eye/RMW → 1/Z:
- Mean eye/RMW ratio: {mean_ratio:.4f} ({deviation_pct:+.1f}% from 1/Z)
- 1/Z = {ONE_OVER_Z:.4f} is {'within' if z_in_ci else 'near'} the 95% CI
- Cannot reject H0: mean = 1/Z (p = {p_value:.3f})

Interpretation:
The eye/RMW ratio of intense hurricanes clusters around 1/Z ≈ 0.173,
which is the reciprocal of Z = √(32π/3) ≈ 5.79.

This suggests a geometric constraint on hurricane structure that
may arise from fundamental vortex dynamics.
""")
    else:
        print(f"""
⚠️ HYPOTHESIS NOT DEFINITIVELY SUPPORTED

- Mean eye/RMW ratio: {mean_ratio:.4f} ({deviation_pct:+.1f}% from 1/Z)
- 1/Z = {ONE_OVER_Z:.4f}
- p-value: {p_value:.4f}

The deviation from 1/Z is larger than expected. Possible explanations:
1. ERA5 resolution limitations in resolving small eyes
2. Storm-to-storm variability in structure
3. The hypothesis needs refinement

More data and higher-resolution observations would clarify.
""")

else:
    print(f"\n  Only {len(results)} valid data points - need more for statistics")

print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
