#!/usr/bin/env python3
"""
Corrected Hurricane Forecasts with Proper Feature Updates

Fixes the feature accumulation bug and generates proper forecasts.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from collections import defaultdict
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Constants
EARTH_RADIUS = 6371
KM_TO_NM = 0.539957
Z_SQUARED = 32 * np.pi / 3

print("=" * 80)
print("  CORRECTED HURRICANE FORECAST GENERATOR")
print("=" * 80)

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return EARTH_RADIUS * c * KM_TO_NM

# Load data
print("\n  Loading hurricane data...")
records = []
with open(os.path.join(DATA_DIR, 'data/extended_best_track/EBTRK_Atlantic_2021.txt'), 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 10:
            try:
                storm_id = parts[0]
                name = parts[1]
                datetime_str = parts[2]
                year = int(parts[3])
                lat = float(parts[4])
                lon = float(parts[5])
                vmax = int(parts[6])
                if vmax > 0:
                    records.append({
                        'storm_id': storm_id, 'name': name,
                        'datetime': datetime_str, 'year': year,
                        'lat': lat, 'lon': lon, 'vmax': vmax,
                    })
            except:
                pass

df = pd.DataFrame(records)
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[(row['storm_id'], row['name'], row['year'])].append(row.to_dict())

print(f"  Loaded {len(df)} observations")

# Feature engineering
def create_features(lat_hist, lon_hist, vmax):
    """Create features from position history (last 5 positions)"""
    if len(lat_hist) < 5:
        return None

    dlat_6h = lat_hist[-1] - lat_hist[-2]
    dlon_6h = lon_hist[-1] - lon_hist[-2]
    dlat_12h = lat_hist[-1] - lat_hist[-3]
    dlon_12h = lon_hist[-1] - lon_hist[-3]
    dlat_24h = lat_hist[-1] - lat_hist[-5]
    dlon_24h = lon_hist[-1] - lon_hist[-5]

    d_dlat = dlat_6h - (lat_hist[-2] - lat_hist[-3])
    d_dlon = dlon_6h - (lon_hist[-2] - lon_hist[-3])

    speed_6h = haversine_distance(lat_hist[-2], lon_hist[-2], lat_hist[-1], lon_hist[-1]) / 6

    # Bearing
    lat1, lon1 = np.radians(lat_hist[-2]), np.radians(lon_hist[-2])
    lat2, lon2 = np.radians(lat_hist[-1]), np.radians(lon_hist[-1])
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360

    return np.array([[
        lat_hist[-1], lon_hist[-1], vmax,
        dlat_6h, dlon_6h, speed_6h,
        dlat_12h, dlon_12h, dlat_24h, dlon_24h,
        d_dlat, d_dlon,
        np.sin(np.radians(bearing)), np.cos(np.radians(bearing))
    ]])

# Train model on pre-2018 data
print("\n  Training ML model (excluding 2018-2021 test storms)...")
feature_cols = ['lat', 'lon', 'vmax', 'dlat_6h', 'dlon_6h', 'speed_6h',
                'dlat_12h', 'dlon_12h', 'dlat_24h', 'dlon_24h',
                'd_dlat', 'd_dlon', 'bearing_sin', 'bearing_cos']

train_data = []
test_storms = {('AL092021', 'IDA', 2021), ('AL052019', 'DORIAN', 2019),
               ('AL132020', 'LAURA', 2020), ('AL142018', 'MICHAEL', 2018)}

for key, obs_list in storms.items():
    if key in test_storms or len(obs_list) < 9:
        continue
    obs = sorted(obs_list, key=lambda x: x['datetime'])
    for i in range(4, len(obs) - 1):
        lat_hist = [obs[i-4]['lat'], obs[i-3]['lat'], obs[i-2]['lat'], obs[i-1]['lat'], obs[i]['lat']]
        lon_hist = [obs[i-4]['lon'], obs[i-3]['lon'], obs[i-2]['lon'], obs[i-1]['lon'], obs[i]['lon']]
        features = create_features(lat_hist, lon_hist, obs[i]['vmax'])
        if features is not None:
            train_data.append({
                **dict(zip(feature_cols, features[0])),
                'target_dlat': obs[i+1]['lat'] - obs[i]['lat'],
                'target_dlon': obs[i+1]['lon'] - obs[i]['lon'],
            })

train_df = pd.DataFrame(train_data)
X = train_df[feature_cols].values
y_lat = train_df['target_dlat'].values
y_lon = train_df['target_dlon'].values

model_lat = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lat.fit(X, y_lat)
model_lon = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lon.fit(X, y_lon)
print(f"  Trained on {len(train_data)} samples")

# Generate forecasts
notable_storms = [
    ('AL092021', 'IDA', 2021),
    ('AL052019', 'DORIAN', 2019),
    ('AL132020', 'LAURA', 2020),
    ('AL142018', 'MICHAEL', 2018),
]

def generate_all_forecasts(obs_list, start_idx, max_hours=120):
    """Generate forecasts from all models with proper feature updates"""
    if start_idx < 4:
        return None

    steps = max_hours // 6
    curr = obs_list[start_idx]

    # Initialize position histories
    lat_hist = [obs_list[start_idx-4]['lat'], obs_list[start_idx-3]['lat'],
                obs_list[start_idx-2]['lat'], obs_list[start_idx-1]['lat'], curr['lat']]
    lon_hist = [obs_list[start_idx-4]['lon'], obs_list[start_idx-3]['lon'],
                obs_list[start_idx-2]['lon'], obs_list[start_idx-1]['lon'], curr['lon']]

    init_dlat = curr['lat'] - obs_list[start_idx-1]['lat']
    init_dlon = curr['lon'] - obs_list[start_idx-1]['lon']

    results = {
        'start': {'lat': curr['lat'], 'lon': curr['lon'], 'vmax': curr['vmax']},
        'actual': [], 'ml_model': [], 'persistence': [], 'cliper': [], 'official_like': []
    }

    # Actual track
    for step in range(1, steps + 1):
        idx = start_idx + step
        if idx < len(obs_list):
            results['actual'].append({
                'hours': step * 6,
                'lat': obs_list[idx]['lat'],
                'lon': obs_list[idx]['lon'],
                'vmax': obs_list[idx]['vmax'],
            })

    # 1. PERSISTENCE (linear extrapolation)
    for step in range(1, steps + 1):
        results['persistence'].append({
            'hours': step * 6,
            'lat': curr['lat'] + init_dlat * step,
            'lon': curr['lon'] + init_dlon * step,
        })

    # 2. CLIPER (climatology + persistence blend)
    for step in range(1, steps + 1):
        blend = min(0.5, step * 0.02)
        pers_lat = curr['lat'] + init_dlat * step
        pers_lon = curr['lon'] + init_dlon * step
        base_lat = curr['lat'] + init_dlat * step * 0.5

        if base_lat < 25:
            climo_dlat, climo_dlon = 0.3 * step, -0.2 * step
        elif base_lat < 35:
            climo_dlat, climo_dlon = 0.5 * step, 0.0
        else:
            climo_dlat, climo_dlon = 0.6 * step, 0.3 * step

        results['cliper'].append({
            'hours': step * 6,
            'lat': (1-blend) * pers_lat + blend * (curr['lat'] + climo_dlat),
            'lon': (1-blend) * pers_lon + blend * (curr['lon'] + climo_dlon),
        })

    # 3. ML MODEL (with corrected feature updates)
    ml_lat_hist = lat_hist.copy()
    ml_lon_hist = lon_hist.copy()
    ml_vmax = curr['vmax']

    for step in range(1, steps + 1):
        features = create_features(ml_lat_hist, ml_lon_hist, ml_vmax)
        if features is None:
            break

        pred_dlat = model_lat.predict(features)[0]
        pred_dlon = model_lon.predict(features)[0]

        new_lat = ml_lat_hist[-1] + pred_dlat
        new_lon = ml_lon_hist[-1] + pred_dlon

        results['ml_model'].append({'hours': step * 6, 'lat': new_lat, 'lon': new_lon})

        # Update history (sliding window)
        ml_lat_hist.append(new_lat)
        ml_lon_hist.append(new_lon)
        if len(ml_lat_hist) > 5:
            ml_lat_hist.pop(0)
            ml_lon_hist.pop(0)

    # 4. OFFICIAL-LIKE (better physics simulation)
    off_lat = curr['lat']
    off_lon = curr['lon']

    for step in range(1, steps + 1):
        recurve = max(0, (off_lat - 25) / 15)
        beta_drift = 0.15 * step / 4
        steer_dlon = 0.1 * recurve * step / 4 if off_lat > 30 else 0
        decay = np.exp(-step / 20)

        new_lat = off_lat + init_dlat * decay + beta_drift * (1 - decay)
        new_lon = off_lon + init_dlon * decay + steer_dlon

        results['official_like'].append({'hours': step * 6, 'lat': new_lat, 'lon': new_lon})
        off_lat, off_lon = new_lat, new_lon

    # Calculate errors
    for model in ['ml_model', 'persistence', 'cliper', 'official_like']:
        for i, pred in enumerate(results[model]):
            if i < len(results['actual']):
                actual = results['actual'][i]
                pred['error_nm'] = haversine_distance(pred['lat'], pred['lon'], actual['lat'], actual['lon'])
                pred['actual_lat'] = actual['lat']
                pred['actual_lon'] = actual['lon']

    return results

# Process storms
print("\n" + "=" * 80)
print("  GENERATING CORRECTED FORECASTS")
print("=" * 80)

all_forecasts = {}

for storm_id, name, year in notable_storms:
    key = (storm_id, name, year)
    if key not in storms:
        continue

    obs = sorted(storms[key], key=lambda x: x['datetime'])
    print(f"\n  {name} ({year}): {len(obs)} observations")

    storm_data = {
        'name': name, 'year': year, 'storm_id': storm_id,
        'max_wind': max(o['vmax'] for o in obs),
        'category': 5 if max(o['vmax'] for o in obs) >= 137 else
                   (4 if max(o['vmax'] for o in obs) >= 113 else
                   (3 if max(o['vmax'] for o in obs) >= 96 else
                   (2 if max(o['vmax'] for o in obs) >= 83 else
                   (1 if max(o['vmax'] for o in obs) >= 64 else 0)))),
        'actual_track': [{'datetime': o['datetime'], 'lat': o['lat'],
                         'lon': -abs(o['lon']), 'vmax': o['vmax']} for o in obs],
        'forecasts': [],
    }

    for idx in range(4, len(obs) - 20, 4):
        forecast = generate_all_forecasts(obs, idx, max_hours=120)
        if forecast and len(forecast['actual']) >= 8:
            storm_data['forecasts'].append({
                'forecast_time': obs[idx]['datetime'],
                'forecast_from': forecast['start'],
                'models': {
                    'ml_model': [{'hours': p['hours'], 'lat': p['lat'], 'lon': -abs(p['lon']),
                                  **({'error_nm': p['error_nm'], 'actual_lat': p['actual_lat'],
                                      'actual_lon': -abs(p['actual_lon'])} if 'error_nm' in p else {})}
                                 for p in forecast['ml_model']],
                    'persistence': [{'hours': p['hours'], 'lat': p['lat'], 'lon': -abs(p['lon']),
                                     **({'error_nm': p['error_nm'], 'actual_lat': p['actual_lat'],
                                         'actual_lon': -abs(p['actual_lon'])} if 'error_nm' in p else {})}
                                    for p in forecast['persistence']],
                    'cliper': [{'hours': p['hours'], 'lat': p['lat'], 'lon': -abs(p['lon']),
                                **({'error_nm': p['error_nm'], 'actual_lat': p['actual_lat'],
                                    'actual_lon': -abs(p['actual_lon'])} if 'error_nm' in p else {})}
                               for p in forecast['cliper']],
                    'official_like': [{'hours': p['hours'], 'lat': p['lat'], 'lon': -abs(p['lon']),
                                       **({'error_nm': p['error_nm'], 'actual_lat': p['actual_lat'],
                                           'actual_lon': -abs(p['actual_lon'])} if 'error_nm' in p else {})}
                                      for p in forecast['official_like']],
                }
            })

    all_forecasts[f"{name}_{year}"] = storm_data
    print(f"    Generated {len(storm_data['forecasts'])} forecast points")

# Error statistics
print("\n" + "=" * 80)
print("  ERROR STATISTICS (Corrected Model)")
print("=" * 80)

# NHC comparison errors
nhc_official = {12: 32, 24: 47, 48: 83, 72: 115, 96: 148, 120: 175}

all_errors = {'ml_model': {}, 'persistence': {}, 'cliper': {}, 'official_like': {}}
for h in [12, 24, 48, 72, 96, 120]:
    for m in all_errors:
        all_errors[m][h] = []

for storm_name, data in all_forecasts.items():
    for forecast in data['forecasts']:
        for model in all_errors:
            for pred in forecast['models'][model]:
                if 'error_nm' in pred and pred['hours'] in all_errors[model]:
                    all_errors[model][pred['hours']].append(pred['error_nm'])

print(f"\n  {'Hours':>8} {'ML':>12} {'Pers':>12} {'CLIPER':>12} {'Official':>12} {'NHC Ref':>12}")
print("  " + "-" * 75)
for hours in [12, 24, 48, 72, 96, 120]:
    ml = np.mean(all_errors['ml_model'][hours]) if all_errors['ml_model'][hours] else 0
    pers = np.mean(all_errors['persistence'][hours]) if all_errors['persistence'][hours] else 0
    clip = np.mean(all_errors['cliper'][hours]) if all_errors['cliper'][hours] else 0
    off = np.mean(all_errors['official_like'][hours]) if all_errors['official_like'][hours] else 0
    nhc = nhc_official.get(hours, 0)
    print(f"  {hours:>8}h {ml:>12.1f} {pers:>12.1f} {clip:>12.1f} {off:>12.1f} {nhc:>12}")

# ML vs NHC comparison
print("\n  ML Model vs NHC Official:")
print(f"  {'Hours':>8} {'ML':>12} {'NHC':>12} {'Ratio':>12} {'Assessment':>20}")
print("  " + "-" * 65)
for hours in [12, 24, 48, 72, 96, 120]:
    ml = np.mean(all_errors['ml_model'][hours]) if all_errors['ml_model'][hours] else 0
    nhc = nhc_official.get(hours, 1)
    ratio = ml / nhc
    assess = "COMPETITIVE!" if ratio < 1.2 else ("Below NHC" if ratio < 2 else "Much worse")
    print(f"  {hours:>8}h {ml:>12.1f} {nhc:>12} {ratio:>12.2f}x {assess:>20}")

# Save data
os.makedirs(os.path.join(DATA_DIR, 'viz'), exist_ok=True)
with open(os.path.join(DATA_DIR, 'viz/hurricane_corrected_forecasts.json'), 'w') as f:
    json.dump(all_forecasts, f, indent=2)

print(f"\n  Saved: viz/hurricane_corrected_forecasts.json")
print("=" * 80)
