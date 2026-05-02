#!/usr/bin/env python3
"""
Generate Extended Hurricane Forecasts with Multiple Model Comparisons

Creates longer forecasts (up to 120h) and compares:
1. Our ML Model
2. Persistence (linear extrapolation)
3. CLIPER-style (climatology + persistence blend)
4. Simulated "Official-like" (with typical NHC error characteristics)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from collections import defaultdict
import json
import warnings
warnings.filterwarnings('ignore')

# Constants
DEG_TO_NM = 60
EARTH_RADIUS = 6371
KM_TO_NM = 0.539957
Z_SQUARED = 32 * np.pi / 3

print("=" * 80)
print("  EXTENDED HURRICANE FORECAST GENERATOR")
print("=" * 80)

# Helper functions
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
with open('data/extended_best_track/EBTRK_Atlantic_2021.txt', 'r') as f:
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
                        'storm_id': storm_id,
                        'name': name,
                        'datetime': datetime_str,
                        'year': year,
                        'lat': lat,
                        'lon': lon,
                        'vmax': vmax,
                    })
            except:
                pass

df = pd.DataFrame(records)
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[(row['storm_id'], row['name'], row['year'])].append(row.to_dict())

print(f"  Loaded {len(df)} observations")

# Train ML model on pre-2018 data
print("\n  Training ML track model...")

def create_features(obs, idx):
    if idx < 4:
        return None
    curr = obs[idx]
    p1, p2, p4 = obs[idx-1], obs[idx-2], obs[idx-4]

    dlat_6h = curr['lat'] - p1['lat']
    dlon_6h = curr['lon'] - p1['lon']
    speed = haversine_distance(p1['lat'], p1['lon'], curr['lat'], curr['lon']) / 6

    # Bearing
    lat1, lon1 = np.radians(p1['lat']), np.radians(p1['lon'])
    lat2, lon2 = np.radians(curr['lat']), np.radians(curr['lon'])
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360

    return {
        'lat': curr['lat'], 'lon': curr['lon'], 'vmax': curr['vmax'],
        'dlat_6h': dlat_6h, 'dlon_6h': dlon_6h, 'speed_6h': speed,
        'dlat_12h': curr['lat'] - p2['lat'], 'dlon_12h': curr['lon'] - p2['lon'],
        'dlat_24h': curr['lat'] - p4['lat'], 'dlon_24h': curr['lon'] - p4['lon'],
        'd_dlat': dlat_6h - (p1['lat'] - p2['lat']),
        'd_dlon': dlon_6h - (p1['lon'] - p2['lon']),
        'bearing_sin': np.sin(np.radians(bearing)),
        'bearing_cos': np.cos(np.radians(bearing)),
    }

train_data = []
for (storm_id, name, year), obs in storms.items():
    if year >= 2018 or len(obs) < 9:
        continue
    obs = sorted(obs, key=lambda x: x['datetime'])
    for i in range(4, len(obs) - 1):
        features = create_features(obs, i)
        if features:
            features['target_dlat'] = obs[i+1]['lat'] - obs[i]['lat']
            features['target_dlon'] = obs[i+1]['lon'] - obs[i]['lon']
            train_data.append(features)

train_df = pd.DataFrame(train_data)
feature_cols = ['lat', 'lon', 'vmax', 'dlat_6h', 'dlon_6h', 'speed_6h',
                'dlat_12h', 'dlon_12h', 'dlat_24h', 'dlon_24h',
                'd_dlat', 'd_dlon', 'bearing_sin', 'bearing_cos']

X = train_df[feature_cols].values
y_lat = train_df['target_dlat'].values
y_lon = train_df['target_dlon'].values

model_lat = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lat.fit(X, y_lat)
model_lon = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lon.fit(X, y_lon)

print("  Model trained.")

# Notable storms
notable_storms = [
    ('AL092021', 'IDA', 2021),
    ('AL052019', 'DORIAN', 2019),
    ('AL132020', 'LAURA', 2020),
    ('AL142018', 'MICHAEL', 2018),
]

def generate_extended_forecast(obs_list, start_idx, max_hours=120):
    """Generate multi-model forecasts up to max_hours"""
    if start_idx < 4:
        return None

    steps = max_hours // 6

    # Get initial conditions
    curr = obs_list[start_idx]
    p1 = obs_list[start_idx - 1]
    p2 = obs_list[start_idx - 2]
    p4 = obs_list[start_idx - 4]

    init_dlat = curr['lat'] - p1['lat']
    init_dlon = curr['lon'] - p1['lon']

    # Calculate initial bearing
    lat1, lon1 = np.radians(p1['lat']), np.radians(p1['lon'])
    lat2, lon2 = np.radians(curr['lat']), np.radians(curr['lon'])
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    init_bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360

    # Storage for different models
    results = {
        'start': {'lat': curr['lat'], 'lon': curr['lon'], 'vmax': curr['vmax']},
        'actual': [],
        'ml_model': [],
        'persistence': [],
        'cliper': [],
        'official_like': [],
    }

    # Get actual track (if available)
    for step in range(1, steps + 1):
        actual_idx = start_idx + step
        if actual_idx < len(obs_list):
            results['actual'].append({
                'hours': step * 6,
                'lat': obs_list[actual_idx]['lat'],
                'lon': obs_list[actual_idx]['lon'],
                'vmax': obs_list[actual_idx]['vmax'],
            })

    # 1. PERSISTENCE MODEL (linear extrapolation)
    for step in range(1, steps + 1):
        hours = step * 6
        pers_lat = curr['lat'] + init_dlat * step
        pers_lon = curr['lon'] + init_dlon * step
        results['persistence'].append({'hours': hours, 'lat': pers_lat, 'lon': pers_lon})

    # 2. CLIPER MODEL (climatology + persistence blend)
    # Climatology: at low lat move WNW, at high lat recurve NE
    for step in range(1, steps + 1):
        hours = step * 6
        blend_factor = min(0.5, step * 0.02)  # More climo at longer range

        # Persistence component
        pers_lat = curr['lat'] + init_dlat * step
        pers_lon = curr['lon'] + init_dlon * step

        # Climatology component (latitude-dependent)
        base_lat = curr['lat'] + init_dlat * step * 0.5
        if base_lat < 25:
            climo_dlat = 0.3 * step  # Northward
            climo_dlon = -0.2 * step  # Westward
        elif base_lat < 35:
            climo_dlat = 0.5 * step  # More northward
            climo_dlon = 0.0 * step  # Slow down westward
        else:
            climo_dlat = 0.6 * step  # Strong northward
            climo_dlon = 0.3 * step  # Eastward (recurvature)

        climo_lat = curr['lat'] + climo_dlat
        climo_lon = curr['lon'] + climo_dlon

        # Blend
        cliper_lat = (1 - blend_factor) * pers_lat + blend_factor * climo_lat
        cliper_lon = (1 - blend_factor) * pers_lon + blend_factor * climo_lon

        results['cliper'].append({'hours': hours, 'lat': cliper_lat, 'lon': cliper_lon})

    # 3. ML MODEL (our model)
    ml_lat = curr['lat']
    ml_lon = curr['lon']
    ml_vmax = curr['vmax']
    dlat_6h = init_dlat
    dlon_6h = init_dlon
    dlat_12h = curr['lat'] - p2['lat']
    dlon_12h = curr['lon'] - p2['lon']
    dlat_24h = curr['lat'] - p4['lat']
    dlon_24h = curr['lon'] - p4['lon']
    d_dlat = dlat_6h - (p1['lat'] - p2['lat'])
    d_dlon = dlon_6h - (p1['lon'] - p2['lon'])
    speed_6h = haversine_distance(p1['lat'], p1['lon'], curr['lat'], curr['lon']) / 6
    bearing = init_bearing

    for step in range(1, steps + 1):
        features = np.array([[
            ml_lat, ml_lon, ml_vmax,
            dlat_6h, dlon_6h, speed_6h,
            dlat_12h, dlon_12h, dlat_24h, dlon_24h,
            d_dlat, d_dlon,
            np.sin(np.radians(bearing)), np.cos(np.radians(bearing))
        ]])

        pred_dlat = model_lat.predict(features)[0]
        pred_dlon = model_lon.predict(features)[0]

        new_lat = ml_lat + pred_dlat
        new_lon = ml_lon + pred_dlon

        results['ml_model'].append({'hours': step * 6, 'lat': new_lat, 'lon': new_lon})

        # Update for next step
        d_dlat = pred_dlat - dlat_6h
        d_dlon = pred_dlon - dlon_6h
        dlat_24h = dlat_12h + dlat_6h + pred_dlat
        dlat_12h = dlat_6h + pred_dlat
        dlat_6h = pred_dlat
        dlon_24h = dlon_12h + dlon_6h + pred_dlon
        dlon_12h = dlon_6h + pred_dlon
        dlon_6h = pred_dlon
        speed_6h = haversine_distance(ml_lat, ml_lon, new_lat, new_lon) / 6

        # Update bearing
        lat1, lon1 = np.radians(ml_lat), np.radians(ml_lon)
        lat2, lon2 = np.radians(new_lat), np.radians(new_lon)
        dlon = lon2 - lon1
        x = np.sin(dlon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360

        ml_lat = new_lat
        ml_lon = new_lon

    # 4. OFFICIAL-LIKE MODEL (simulated NHC-like with better physics)
    # Uses weighted blend of persistence + climatology + recurvature detection
    off_lat = curr['lat']
    off_lon = curr['lon']
    off_dlat = init_dlat
    off_dlon = init_dlon

    for step in range(1, steps + 1):
        hours = step * 6

        # Detect recurvature based on latitude
        recurve_factor = max(0, (off_lat - 25) / 15)  # Increases above 25°N

        # Beta drift (Coriolis-induced poleward motion)
        beta_drift_lat = 0.15 * step / 4  # Slight northward bias

        # Steering adjustment (simplified)
        if off_lat > 30:
            # Recurvature zone - turn eastward
            steer_dlon = 0.1 * recurve_factor * step / 4
        else:
            steer_dlon = 0

        # Apply motion with decay toward climatology at longer range
        decay = np.exp(-step / 20)  # Motion decays over time

        new_lat = off_lat + off_dlat * decay + beta_drift_lat * (1 - decay)
        new_lon = off_lon + off_dlon * decay + steer_dlon

        results['official_like'].append({'hours': hours, 'lat': new_lat, 'lon': new_lon})

        off_lat = new_lat
        off_lon = new_lon

    # Calculate errors for each model vs actual
    for model_name in ['ml_model', 'persistence', 'cliper', 'official_like']:
        for i, pred in enumerate(results[model_name]):
            if i < len(results['actual']):
                actual = results['actual'][i]
                error = haversine_distance(pred['lat'], pred['lon'], actual['lat'], actual['lon'])
                pred['error_nm'] = error
                pred['actual_lat'] = actual['lat']
                pred['actual_lon'] = actual['lon']

    return results

# Generate forecasts for all storms
print("\n" + "=" * 80)
print("  GENERATING EXTENDED FORECASTS")
print("=" * 80)

all_forecasts = {}

for storm_id, name, year in notable_storms:
    key = (storm_id, name, year)
    if key not in storms:
        print(f"  Storm not found: {name} ({year})")
        continue

    obs = sorted(storms[key], key=lambda x: x['datetime'])
    print(f"\n  Processing {name} ({year}): {len(obs)} observations")

    storm_data = {
        'name': name,
        'year': year,
        'storm_id': storm_id,
        'max_wind': max(o['vmax'] for o in obs),
        'category': 5 if max(o['vmax'] for o in obs) >= 137 else
                   (4 if max(o['vmax'] for o in obs) >= 113 else
                   (3 if max(o['vmax'] for o in obs) >= 96 else
                   (2 if max(o['vmax'] for o in obs) >= 83 else
                   (1 if max(o['vmax'] for o in obs) >= 64 else 0)))),
        'actual_track': [{'datetime': o['datetime'], 'lat': o['lat'], 'lon': -abs(o['lon']),
                         'vmax': o['vmax']} for o in obs],
        'forecasts': [],
    }

    # Generate forecasts at multiple points
    for forecast_idx in range(4, len(obs) - 20, 4):
        forecast_data = generate_extended_forecast(obs, forecast_idx, max_hours=120)

        if forecast_data and len(forecast_data['actual']) >= 8:
            storm_data['forecasts'].append({
                'forecast_time': obs[forecast_idx]['datetime'],
                'forecast_from': forecast_data['start'],
                'actual': forecast_data['actual'],
                'ml_model': forecast_data['ml_model'],
                'persistence': forecast_data['persistence'],
                'cliper': forecast_data['cliper'],
                'official_like': forecast_data['official_like'],
            })

    all_forecasts[f"{name}_{year}"] = storm_data
    print(f"    Generated {len(storm_data['forecasts'])} extended forecast points")

# Calculate and print error statistics
print("\n" + "=" * 80)
print("  ERROR STATISTICS BY MODEL")
print("=" * 80)

for storm_name, data in all_forecasts.items():
    print(f"\n  {storm_name}:")
    print(f"  {'Hours':>8} {'ML Model':>12} {'Persistence':>12} {'CLIPER':>12} {'Official':>12}")
    print("  " + "-" * 60)

    for hours in [12, 24, 48, 72, 96, 120]:
        errors = {'ml_model': [], 'persistence': [], 'cliper': [], 'official_like': []}

        for forecast in data['forecasts']:
            for model_name in errors.keys():
                for pred in forecast[model_name]:
                    if pred['hours'] == hours and 'error_nm' in pred:
                        errors[model_name].append(pred['error_nm'])

        ml = np.mean(errors['ml_model']) if errors['ml_model'] else float('nan')
        pers = np.mean(errors['persistence']) if errors['persistence'] else float('nan')
        clip = np.mean(errors['cliper']) if errors['cliper'] else float('nan')
        off = np.mean(errors['official_like']) if errors['official_like'] else float('nan')

        if not np.isnan(ml):
            print(f"  {hours:>8}h {ml:>12.1f} {pers:>12.1f} {clip:>12.1f} {off:>12.1f}")

# Save to JSON
print("\n  Saving extended forecast data...")

# Convert to JSON-serializable format
output_data = {}
for storm_name, data in all_forecasts.items():
    output_data[storm_name] = {
        'name': data['name'],
        'year': data['year'],
        'storm_id': data['storm_id'],
        'max_wind': data['max_wind'],
        'category': data['category'],
        'actual_track': data['actual_track'],
        'forecasts': []
    }

    for f in data['forecasts']:
        forecast_entry = {
            'forecast_time': f['forecast_time'],
            'forecast_from': {
                'lat': float(f['forecast_from']['lat']),
                'lon': float(-abs(f['forecast_from']['lon'])),
                'vmax': int(f['forecast_from']['vmax']),
            },
            'models': {}
        }

        for model_name in ['ml_model', 'persistence', 'cliper', 'official_like']:
            forecast_entry['models'][model_name] = []
            for pred in f[model_name]:
                entry = {
                    'hours': pred['hours'],
                    'lat': float(pred['lat']),
                    'lon': float(-abs(pred['lon'])) if pred['lon'] > 0 else float(pred['lon']),
                }
                if 'error_nm' in pred:
                    entry['error_nm'] = float(pred['error_nm'])
                    entry['actual_lat'] = float(pred['actual_lat'])
                    entry['actual_lon'] = float(-abs(pred['actual_lon'])) if pred['actual_lon'] > 0 else float(pred['actual_lon'])
                forecast_entry['models'][model_name].append(entry)

        output_data[storm_name]['forecasts'].append(forecast_entry)

with open('viz/hurricane_extended_forecasts.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("  Saved: viz/hurricane_extended_forecasts.json")
print("=" * 80)
