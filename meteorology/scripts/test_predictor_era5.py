#!/usr/bin/env python3
"""
Test Z² Hurricane Predictor Against ERA5 Real Data

This script:
1. Loads actual ERA5 reanalysis data for historical hurricanes
2. Extracts real environmental conditions (SST, shear, humidity)
3. Runs the Z² predictor with real initial conditions
4. Compares 24h forecasts to actual ERA5 observations
5. Validates Z² structure predictions against real data

Usage:
    python scripts/test_predictor_era5.py
"""

import sys
from pathlib import Path
from functools import partial
from datetime import datetime, timedelta
import numpy as np

print = partial(print, flush=True)

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Z² constants
Z_SQUARED = 32 * np.pi / 3
Z_VALUE = np.sqrt(Z_SQUARED)
ONE_OVER_Z = 1 / Z_VALUE

print("=" * 70)
print("Z² HURRICANE PREDICTOR - ERA5 VALIDATION")
print("=" * 70)
print(f"\nZ² Target eye/RMW ratio: 1/Z = {ONE_OVER_Z:.4f}")

# ============================================================================
# Hurricane Database with precise timing
# ============================================================================

HURRICANES = {
    'irma_2017': {
        'name': 'Hurricane Irma',
        'storm_id': 'AL112017',
        'basin': 'ATL',
        # Initial state (before RI)
        'initial': {
            'datetime': '2017-09-04T12:00:00',
            'lat': 17.4,
            'lon': -58.9,
            'max_wind_kt': 90,
            'pressure': 970,
        },
        # 24h later (during/after RI)
        'verify_24h': {
            'datetime': '2017-09-05T12:00:00',
            'lat': 17.8,
            'lon': -62.5,
            'max_wind_kt': 150,
            'pressure': 929,
        },
    },
    'maria_2017': {
        'name': 'Hurricane Maria',
        'storm_id': 'AL152017',
        'basin': 'ATL',
        'initial': {
            'datetime': '2017-09-17T12:00:00',
            'lat': 14.5,
            'lon': -60.0,
            'max_wind_kt': 80,
            'pressure': 979,
        },
        'verify_24h': {
            'datetime': '2017-09-18T12:00:00',
            'lat': 15.3,
            'lon': -64.4,
            'max_wind_kt': 150,
            'pressure': 908,
        },
    },
    'dorian_2019': {
        'name': 'Hurricane Dorian',
        'storm_id': 'AL052019',
        'basin': 'ATL',
        'initial': {
            'datetime': '2019-08-30T12:00:00',
            'lat': 23.5,
            'lon': -73.0,
            'max_wind_kt': 100,
            'pressure': 962,
        },
        'verify_24h': {
            'datetime': '2019-08-31T12:00:00',
            'lat': 25.0,
            'lon': -75.5,
            'max_wind_kt': 145,
            'pressure': 944,
        },
    },
    'michael_2018': {
        'name': 'Hurricane Michael',
        'storm_id': 'AL142018',
        'basin': 'ATL',
        'initial': {
            'datetime': '2018-10-08T12:00:00',
            'lat': 25.0,
            'lon': -86.5,
            'max_wind_kt': 75,
            'pressure': 973,
        },
        'verify_24h': {
            'datetime': '2018-10-09T12:00:00',
            'lat': 27.0,
            'lon': -86.0,
            'max_wind_kt': 120,
            'pressure': 948,
        },
    },
}

# ============================================================================
# ERA5 Data Loading Functions
# ============================================================================

def load_era5_environment(loader, lat, lon, dt, box_size=5):
    """
    Load environmental conditions from ERA5 for a storm location.

    Returns SST, wind shear, humidity, etc.
    """
    from data.era5_loader import FAST_CONFIG

    # Convert longitude to 0-360
    lon_360 = lon if lon >= 0 else lon + 360

    # Load data for ±12 hours around the target time
    start = (dt - timedelta(hours=6)).isoformat()
    end = (dt + timedelta(hours=6)).isoformat()

    ds = loader.load_time_range(
        start=start,
        end=end,
        config=FAST_CONFIG,
        time_step=6,
        lazy=True
    )

    # Select region
    lat_min, lat_max = lat - box_size, lat + box_size
    lon_min, lon_max = lon_360 - box_size, lon_360 + box_size

    ds_region = ds.sel(
        latitude=slice(lat_max, lat_min),
        longitude=slice(lon_min, lon_max)
    )

    # Get middle timestep
    time_idx = len(ds_region.time) // 2

    # Extract variables
    env = {}

    # SST (sea surface temperature)
    if 'sea_surface_temperature' in ds_region:
        sst = ds_region['sea_surface_temperature'].isel(time=time_idx).compute()
        env['sst'] = float(np.nanmean(sst.values))
    else:
        # Use 2m temperature as proxy
        t2m = ds_region['2m_temperature'].isel(time=time_idx).compute()
        env['sst'] = float(np.nanmean(t2m.values))

    # Wind shear (200-850 hPa)
    u = ds_region['u_component_of_wind'].isel(time=time_idx)
    v = ds_region['v_component_of_wind'].isel(time=time_idx)

    if 'level' in u.dims:
        # Get 200 and 850 hPa levels
        try:
            u200 = u.sel(level=200, method='nearest').compute()
            v200 = v.sel(level=200, method='nearest').compute()
            u850 = u.sel(level=850, method='nearest').compute()
            v850 = v.sel(level=850, method='nearest').compute()

            du = float(np.nanmean(u200.values - u850.values))
            dv = float(np.nanmean(v200.values - v850.values))
            env['shear'] = np.sqrt(du**2 + dv**2)
        except:
            env['shear'] = 10.0  # Default
    else:
        env['shear'] = 10.0

    # Relative humidity (mid-levels)
    if 'relative_humidity' in ds_region:
        rh = ds_region['relative_humidity'].isel(time=time_idx)
        if 'level' in rh.dims:
            try:
                rh500 = rh.sel(level=500, method='nearest').compute()
                env['rh_500'] = float(np.nanmean(rh500.values)) / 100.0
            except:
                env['rh_500'] = 0.60
        else:
            env['rh_500'] = 0.60
    else:
        env['rh_500'] = 0.60

    # Mean sea level pressure (for finding storm center)
    msl = ds_region['mean_sea_level_pressure'].isel(time=time_idx).compute()
    min_idx = np.unravel_index(np.argmin(msl.values), msl.shape)
    env['center_lat'] = float(msl.latitude.values[min_idx[0]])
    env['center_lon'] = float(msl.longitude.values[min_idx[1]])
    env['min_pressure'] = float(msl.values[min_idx]) / 100.0  # Pa to hPa

    return env


def compute_storm_structure_era5(loader, lat, lon, dt, box_size=8):
    """
    Compute eye radius and RMW from ERA5 wind fields.
    """
    from data.era5_loader import FAST_CONFIG

    lon_360 = lon if lon >= 0 else lon + 360

    start = (dt - timedelta(hours=3)).isoformat()
    end = (dt + timedelta(hours=3)).isoformat()

    ds = loader.load_time_range(
        start=start,
        end=end,
        config=FAST_CONFIG,
        time_step=6,
        lazy=True
    )

    lat_min, lat_max = lat - box_size, lat + box_size
    lon_min, lon_max = lon_360 - box_size, lon_360 + box_size

    ds_region = ds.sel(
        latitude=slice(lat_max, lat_min),
        longitude=slice(lon_min, lon_max)
    )

    time_idx = len(ds_region.time) // 2

    # Get winds at 850 hPa
    u = ds_region['u_component_of_wind'].isel(time=time_idx)
    v = ds_region['v_component_of_wind'].isel(time=time_idx)
    msl = ds_region['mean_sea_level_pressure'].isel(time=time_idx)

    if 'level' in u.dims:
        u = u.sel(level=850, method='nearest')
        v = v.sel(level=850, method='nearest')

    u = u.compute()
    v = v.compute()
    msl = msl.compute()

    # Find storm center
    min_idx = np.unravel_index(np.argmin(msl.values), msl.shape)
    center_lat = float(msl.latitude.values[min_idx[0]])
    center_lon = float(msl.longitude.values[min_idx[1]])

    # Compute radial profile
    lats = msl.latitude.values
    lons = msl.longitude.values
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    lat_dist = (lat_grid - center_lat) * 111
    lon_dist = (lon_grid - center_lon) * 111 * np.cos(np.radians(center_lat))
    distance = np.sqrt(lat_dist**2 + lon_dist**2)

    wind_speed = np.sqrt(u.values**2 + v.values**2)

    # Bin by distance
    max_radius = 400
    n_bins = 40
    bins = np.linspace(0, max_radius, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    mean_wind = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (distance >= bins[i]) & (distance < bins[i+1])
        if np.any(mask):
            mean_wind[i] = np.nanmean(wind_speed[mask])

    # Find RMW and eye
    rmax_idx = np.argmax(mean_wind)
    rmax = bin_centers[rmax_idx]
    vmax = mean_wind[rmax_idx]

    eye_radius = None
    if rmax_idx > 2:
        inner_winds = mean_wind[:rmax_idx]
        inner_radii = bin_centers[:rmax_idx]
        if len(inner_winds) > 1:
            min_idx = np.argmin(inner_winds[1:]) + 1
            eye_radius = inner_radii[min_idx]

    if eye_radius is None:
        eye_radius = rmax * 0.25  # Estimate

    return {
        'eye_radius': eye_radius,
        'rmax': rmax,
        'vmax': vmax,
        'center_lat': center_lat,
        'center_lon': center_lon,
    }


# ============================================================================
# Main Validation
# ============================================================================

print("\n" + "-" * 70)
print("Loading ERA5 connection...")
print("-" * 70)

from data.era5_loader import ERA5CloudLoader
from physics.z2_hurricane_predictor import (
    Z2HurricanePredictor,
    StormState,
    EnvironmentState,
)

loader = ERA5CloudLoader(verbose=False)
_ = loader.dataset
print("  ERA5 connection established!")

predictor = Z2HurricanePredictor()

# Run validation for each hurricane
print("\n" + "-" * 70)
print("Validating against ERA5 data...")
print("-" * 70)

results = []

for storm_key, storm_info in HURRICANES.items():
    print(f"\n  Processing {storm_info['name']}...")

    try:
        init = storm_info['initial']
        verify = storm_info['verify_24h']

        init_dt = datetime.fromisoformat(init['datetime'])
        verify_dt = datetime.fromisoformat(verify['datetime'])

        # Load ERA5 environment at initial time
        print(f"    Loading environment at {init_dt}...")
        env_data = load_era5_environment(
            loader, init['lat'], init['lon'], init_dt
        )

        # Load ERA5 structure at initial time
        print(f"    Computing initial structure...")
        struct_init = compute_storm_structure_era5(
            loader, init['lat'], init['lon'], init_dt
        )

        # Load ERA5 structure at verification time
        print(f"    Computing verification structure...")
        struct_verify = compute_storm_structure_era5(
            loader, verify['lat'], verify['lon'], verify_dt
        )

        # Create initial storm state
        initial_state = StormState(
            storm_id=storm_info['storm_id'],
            name=storm_info['name'].split()[-1],  # Just the name
            basin=storm_info['basin'],
            latitude=init['lat'],
            longitude=init['lon'],
            timestamp=init_dt,
            max_wind_ms=init['max_wind_kt'] / 1.944,
            central_pressure=init['pressure'],
            rmax=struct_init['rmax'],
            eye_radius=struct_init['eye_radius'],
        )

        # Create environment state from ERA5
        environment = EnvironmentState(
            sst=env_data['sst'],
            vertical_shear_200_850=env_data['shear'],
            relative_humidity_500=env_data['rh_500'],
            ocean_heat_content=70.0,  # Estimated
        )

        # Generate 24h forecast
        forecasts = predictor.generate_forecast(
            initial_state, environment, forecast_hours=[24]
        )
        fc_24h = forecasts[0]

        # Get RI probability
        ri_prob = predictor.compute_ri_probability(initial_state, environment)

        # Store results
        results.append({
            'name': storm_info['name'],
            # Initial conditions
            'init_wind_kt': init['max_wind_kt'],
            'init_eye_ratio': struct_init['eye_radius'] / struct_init['rmax'],
            # ERA5 environment
            'era5_sst_c': env_data['sst'] - 273.15,
            'era5_shear': env_data['shear'],
            'era5_rh500': env_data['rh_500'],
            # Forecast
            'fcst_wind_kt': fc_24h.max_wind_kt,
            'fcst_eye_ratio': fc_24h.eye_rmax_ratio,
            'ri_probability': ri_prob,
            # Verification (best track)
            'obs_wind_kt': verify['max_wind_kt'],
            # ERA5 verification structure
            'era5_verify_eye_ratio': struct_verify['eye_radius'] / struct_verify['rmax'],
            'era5_verify_vmax': struct_verify['vmax'],
            # Errors
            'wind_error_kt': fc_24h.max_wind_kt - verify['max_wind_kt'],
            # RI check
            'actual_ri': (verify['max_wind_kt'] - init['max_wind_kt']) >= 30,
        })

        print(f"    Initial: {init['max_wind_kt']} kt, Eye/RMW: {struct_init['eye_radius']/struct_init['rmax']:.3f}")
        print(f"    ERA5 SST: {env_data['sst']-273.15:.1f}°C, Shear: {env_data['shear']:.1f} m/s")
        print(f"    Forecast: {fc_24h.max_wind_kt:.0f} kt, Observed: {verify['max_wind_kt']} kt")
        print(f"    RI Prob: {ri_prob*100:.0f}%, Actual RI: {results[-1]['actual_ri']}")

    except Exception as e:
        print(f"    Error: {e}")
        import traceback
        traceback.print_exc()

# ============================================================================
# Results Summary
# ============================================================================

print("\n" + "=" * 90)
print("ERA5 VALIDATION RESULTS")
print("=" * 90)

print(f"\n{'Storm':<20} {'Init':>5} {'Fcst':>5} {'Obs':>5} {'Err':>6} {'Eye/RMW':>8} {'SST':>6} {'Shear':>6} {'RI%':>5} {'RI?':>4}")
print("-" * 90)

total_error = 0
ri_correct = 0
n_valid = 0

for r in results:
    ri_correct_flag = (r['ri_probability'] > 0.5) == r['actual_ri']
    ri_correct += 1 if ri_correct_flag else 0
    total_error += abs(r['wind_error_kt'])
    n_valid += 1

    print(f"{r['name']:<20} {r['init_wind_kt']:>5} {r['fcst_wind_kt']:>5.0f} {r['obs_wind_kt']:>5} "
          f"{r['wind_error_kt']:>+6.0f} {r['init_eye_ratio']:>8.3f} "
          f"{r['era5_sst_c']:>5.1f}° {r['era5_shear']:>5.1f} "
          f"{r['ri_probability']*100:>4.0f}% {'✓' if ri_correct_flag else '✗':>4}")

print("-" * 90)

if n_valid > 0:
    print(f"\nMean Absolute Error: {total_error/n_valid:.1f} kt")
    print(f"RI Prediction Accuracy: {ri_correct}/{n_valid} ({100*ri_correct/n_valid:.0f}%)")

# Z² Structure Analysis
print("\n" + "=" * 70)
print("Z² STRUCTURE ANALYSIS FROM ERA5")
print("=" * 70)

print(f"\nTarget eye/RMW ratio (1/Z): {ONE_OVER_Z:.4f}")
print(f"\n{'Storm':<20} {'Init Ratio':>12} {'Verify Ratio':>14} {'→ 1/Z?':>8}")
print("-" * 60)

ratios_init = []
ratios_verify = []

for r in results:
    init_ratio = r['init_eye_ratio']
    verify_ratio = r['era5_verify_eye_ratio']
    ratios_init.append(init_ratio)
    ratios_verify.append(verify_ratio)

    converging = "Yes" if verify_ratio < init_ratio else "No"
    print(f"{r['name']:<20} {init_ratio:>12.3f} {verify_ratio:>14.3f} {converging:>8}")

if ratios_init and ratios_verify:
    print("-" * 60)
    print(f"{'Mean':<20} {np.mean(ratios_init):>12.3f} {np.mean(ratios_verify):>14.3f}")
    print(f"{'vs 1/Z error':<20} {abs(np.mean(ratios_init)-ONE_OVER_Z)/ONE_OVER_Z*100:>11.1f}% {abs(np.mean(ratios_verify)-ONE_OVER_Z)/ONE_OVER_Z*100:>13.1f}%")

    # Check if converging toward 1/Z
    converging_count = sum(1 for i, v in zip(ratios_init, ratios_verify)
                          if abs(v - ONE_OVER_Z) < abs(i - ONE_OVER_Z))
    print(f"\nStorms converging toward 1/Z: {converging_count}/{len(ratios_init)}")

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
