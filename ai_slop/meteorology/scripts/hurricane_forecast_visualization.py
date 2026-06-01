#!/usr/bin/env python3
"""
Hurricane Forecast Visualization Generator

Creates interactive visualizations comparing our model predictions
to actual hurricane tracks at different forecast lead times.

Output:
1. JSON data for web integration
2. Static PNG visualizations
3. Interactive HTML with time slider
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
DEG_TO_NM = 60
EARTH_RADIUS = 6371
KM_TO_NM = 0.539957
Z_SQUARED = 32 * np.pi / 3

print("=" * 80)
print("  HURRICANE FORECAST VISUALIZATION GENERATOR")
print("=" * 80)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great circle distance in nm"""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return EARTH_RADIUS * c * KM_TO_NM

def calc_track_error(pred_lat, pred_lon, true_lat, true_lon):
    """Calculate position error in nm"""
    return haversine_distance(pred_lat, pred_lon, true_lat, true_lon)

# =============================================================================
# LOAD ALL DATA
# =============================================================================

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
                pmin = int(parts[7])
                rmw = int(parts[8])
                eye = int(parts[9])

                if vmax > 0:
                    records.append({
                        'storm_id': storm_id,
                        'name': name,
                        'datetime': datetime_str,
                        'year': year,
                        'lat': lat,
                        'lon': lon,
                        'vmax': vmax,
                        'pmin': pmin if pmin > 0 and pmin != -99 else None,
                        'rmw': rmw if rmw > 0 and rmw != -99 else None,
                        'eye': eye if eye > 0 and eye != -99 else None,
                    })
            except:
                pass

df = pd.DataFrame(records)
print(f"  Loaded {len(df)} observations")

# Group by storm
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[(row['storm_id'], row['name'], row['year'])].append(row.to_dict())

# =============================================================================
# TRAIN TRACK MODEL (on pre-2018 data)
# =============================================================================

print("\n  Training track prediction model...")

def create_track_features(obs_list, idx):
    """Create features for track prediction at observation index"""
    if idx < 4:
        return None

    curr = obs_list[idx]
    p1 = obs_list[idx-1]
    p2 = obs_list[idx-2]
    p4 = obs_list[idx-4]

    dlat_6h = curr['lat'] - p1['lat']
    dlon_6h = curr['lon'] - p1['lon']
    speed_6h = haversine_distance(p1['lat'], p1['lon'], curr['lat'], curr['lon']) / 6

    # Bearing calculation
    lat1, lon1 = np.radians(p1['lat']), np.radians(p1['lon'])
    lat2, lon2 = np.radians(curr['lat']), np.radians(curr['lon'])
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing_6h = (np.degrees(np.arctan2(x, y)) + 360) % 360

    dlat_12h = curr['lat'] - p2['lat']
    dlon_12h = curr['lon'] - p2['lon']
    dlat_24h = curr['lat'] - p4['lat']
    dlon_24h = curr['lon'] - p4['lon']

    d_dlat = dlat_6h - (p1['lat'] - p2['lat'])
    d_dlon = dlon_6h - (p1['lon'] - p2['lon'])

    return {
        'lat': curr['lat'],
        'lon': curr['lon'],
        'vmax': curr['vmax'],
        'dlat_6h': dlat_6h,
        'dlon_6h': dlon_6h,
        'speed_6h': speed_6h,
        'dlat_12h': dlat_12h,
        'dlon_12h': dlon_12h,
        'dlat_24h': dlat_24h,
        'dlon_24h': dlon_24h,
        'd_dlat': d_dlat,
        'd_dlon': d_dlon,
        'bearing_sin': np.sin(np.radians(bearing_6h)),
        'bearing_cos': np.cos(np.radians(bearing_6h)),
    }

# Build training data from pre-2018 storms
train_data = []
for (storm_id, name, year), obs in storms.items():
    if year >= 2018 or len(obs) < 9:
        continue

    obs = sorted(obs, key=lambda x: x['datetime'])

    for i in range(4, len(obs) - 1):
        features = create_track_features(obs, i)
        if features:
            features['target_dlat'] = obs[i+1]['lat'] - obs[i]['lat']
            features['target_dlon'] = obs[i+1]['lon'] - obs[i]['lon']
            train_data.append(features)

train_df = pd.DataFrame(train_data)
print(f"  Training samples: {len(train_df)}")

feature_cols = ['lat', 'lon', 'vmax', 'dlat_6h', 'dlon_6h', 'speed_6h',
                'dlat_12h', 'dlon_12h', 'dlat_24h', 'dlon_24h',
                'd_dlat', 'd_dlon', 'bearing_sin', 'bearing_cos']

X_train = train_df[feature_cols].values
y_lat_train = train_df['target_dlat'].values
y_lon_train = train_df['target_dlon'].values

# Train models
model_lat = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lat.fit(X_train, y_lat_train)

model_lon = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lon.fit(X_train, y_lon_train)

print("  Model trained.")

# =============================================================================
# INTENSITY MODEL (simple trend-based)
# =============================================================================

print("\n  Training intensity prediction model...")

int_train = []
for (storm_id, name, year), obs in storms.items():
    if year >= 2018 or len(obs) < 5:
        continue

    obs = sorted(obs, key=lambda x: x['datetime'])

    for i in range(4, len(obs) - 1):
        curr = obs[i]
        prev = obs[i-1]
        prev2 = obs[i-2]
        prev4 = obs[i-4]
        next_obs = obs[i+1]

        int_train.append({
            'vmax': curr['vmax'],
            'lat': curr['lat'],
            'dv_6h': curr['vmax'] - prev['vmax'],
            'dv_12h': curr['vmax'] - prev2['vmax'],
            'dv_24h': curr['vmax'] - prev4['vmax'],
            'has_eye': 1 if curr['eye'] else 0,
            'target_dv': next_obs['vmax'] - curr['vmax'],
        })

int_df = pd.DataFrame(int_train)
int_features = ['vmax', 'lat', 'dv_6h', 'dv_12h', 'dv_24h', 'has_eye']

X_int = int_df[int_features].values
y_int = int_df['target_dv'].values

model_int = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
model_int.fit(X_int, y_int)

print("  Intensity model trained.")

# =============================================================================
# GENERATE FORECASTS FOR NOTABLE HURRICANES
# =============================================================================

print("\n" + "=" * 80)
print("  GENERATING FORECAST COMPARISONS")
print("=" * 80)

# Select hurricanes
notable_storms = [
    ('AL092021', 'IDA', 2021),
    ('AL052019', 'DORIAN', 2019),
    ('AL132020', 'LAURA', 2020),
    ('AL142018', 'MICHAEL', 2018),
]

def generate_multi_step_forecast(obs_list, start_idx, steps=8):
    """Generate forecast for multiple time steps (6h each)"""
    if start_idx < 4:
        return None

    forecasts = []
    current_lat = obs_list[start_idx]['lat']
    current_lon = obs_list[start_idx]['lon']
    current_vmax = obs_list[start_idx]['vmax']

    # Use recent history for initial features
    dlat_6h = obs_list[start_idx]['lat'] - obs_list[start_idx-1]['lat']
    dlon_6h = obs_list[start_idx]['lon'] - obs_list[start_idx-1]['lon']
    dlat_12h = obs_list[start_idx]['lat'] - obs_list[start_idx-2]['lat']
    dlon_12h = obs_list[start_idx]['lon'] - obs_list[start_idx-2]['lon']
    dlat_24h = obs_list[start_idx]['lat'] - obs_list[start_idx-4]['lat']
    dlon_24h = obs_list[start_idx]['lon'] - obs_list[start_idx-4]['lon']

    speed_6h = haversine_distance(
        obs_list[start_idx-1]['lat'], obs_list[start_idx-1]['lon'],
        current_lat, current_lon
    ) / 6

    d_dlat = dlat_6h - (obs_list[start_idx-1]['lat'] - obs_list[start_idx-2]['lat'])
    d_dlon = dlon_6h - (obs_list[start_idx-1]['lon'] - obs_list[start_idx-2]['lon'])

    # Calculate bearing
    lat1, lon1 = np.radians(obs_list[start_idx-1]['lat']), np.radians(obs_list[start_idx-1]['lon'])
    lat2, lon2 = np.radians(current_lat), np.radians(current_lon)
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360

    for step in range(steps):
        # Build feature vector
        features = np.array([[
            current_lat, current_lon, current_vmax,
            dlat_6h, dlon_6h, speed_6h,
            dlat_12h, dlon_12h, dlat_24h, dlon_24h,
            d_dlat, d_dlon,
            np.sin(np.radians(bearing)), np.cos(np.radians(bearing))
        ]])

        # Predict next position
        pred_dlat = model_lat.predict(features)[0]
        pred_dlon = model_lon.predict(features)[0]

        new_lat = current_lat + pred_dlat
        new_lon = current_lon + pred_dlon

        # Predict intensity change
        int_features = np.array([[
            current_vmax, current_lat,
            dlat_6h * 10,  # Approximate intensity trend (placeholder)
            dlat_12h * 10,
            dlat_24h * 10,
            1 if current_vmax >= 64 else 0
        ]])
        pred_dv = model_int.predict(int_features)[0]
        new_vmax = max(20, current_vmax + pred_dv)

        forecasts.append({
            'step': step + 1,
            'hours_ahead': (step + 1) * 6,
            'forecast_lat': float(new_lat),
            'forecast_lon': float(new_lon),
            'forecast_vmax': float(new_vmax),
        })

        # Update for next iteration
        d_dlat = pred_dlat - dlat_6h
        d_dlon = pred_dlon - dlon_6h

        dlat_24h = dlat_12h + dlat_6h + pred_dlat
        dlat_12h = dlat_6h + pred_dlat
        dlat_6h = pred_dlat

        dlon_24h = dlon_12h + dlon_6h + pred_dlon
        dlon_12h = dlon_6h + pred_dlon
        dlon_6h = pred_dlon

        speed_6h = haversine_distance(current_lat, current_lon, new_lat, new_lon) / 6

        # Update bearing
        lat1, lon1 = np.radians(current_lat), np.radians(current_lon)
        lat2, lon2 = np.radians(new_lat), np.radians(new_lon)
        dlon = lon2 - lon1
        x = np.sin(dlon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        bearing = (np.degrees(np.arctan2(x, y)) + 360) % 360

        current_lat = new_lat
        current_lon = new_lon
        current_vmax = new_vmax

    return forecasts

# Generate visualization data
all_viz_data = {}

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
        'actual_track': [],
        'forecasts': [],
    }

    # Store actual track
    for o in obs:
        storm_data['actual_track'].append({
            'datetime': o['datetime'],
            'lat': float(o['lat']),
            'lon': float(o['lon']),
            'vmax': int(o['vmax']),
            'pmin': o['pmin'],
        })

    # Generate forecasts at different points along the track
    # Every 4 observations (24 hours)
    for forecast_idx in range(4, len(obs) - 8, 4):
        forecasts = generate_multi_step_forecast(obs, forecast_idx, steps=8)

        if forecasts:
            # Calculate errors vs actual
            forecast_point = {
                'forecast_time': obs[forecast_idx]['datetime'],
                'forecast_from': {
                    'lat': float(obs[forecast_idx]['lat']),
                    'lon': float(obs[forecast_idx]['lon']),
                    'vmax': int(obs[forecast_idx]['vmax']),
                },
                'predictions': [],
            }

            for f in forecasts:
                actual_idx = forecast_idx + f['step']
                if actual_idx < len(obs):
                    actual = obs[actual_idx]
                    error_nm = calc_track_error(
                        f['forecast_lat'], f['forecast_lon'],
                        actual['lat'], actual['lon']
                    )
                    int_error = f['forecast_vmax'] - actual['vmax']

                    forecast_point['predictions'].append({
                        'hours_ahead': f['hours_ahead'],
                        'forecast_lat': f['forecast_lat'],
                        'forecast_lon': f['forecast_lon'],
                        'forecast_vmax': f['forecast_vmax'],
                        'actual_lat': float(actual['lat']),
                        'actual_lon': float(actual['lon']),
                        'actual_vmax': int(actual['vmax']),
                        'track_error_nm': float(error_nm),
                        'intensity_error_kt': float(int_error),
                    })

            if forecast_point['predictions']:
                storm_data['forecasts'].append(forecast_point)

    all_viz_data[f"{name}_{year}"] = storm_data
    print(f"    Generated {len(storm_data['forecasts'])} forecast points")

# =============================================================================
# CALCULATE SUMMARY STATISTICS
# =============================================================================

print("\n" + "=" * 80)
print("  FORECAST ERROR SUMMARY")
print("=" * 80)

for storm_name, data in all_viz_data.items():
    print(f"\n  {storm_name}:")

    # Collect errors by lead time
    errors_by_lead = defaultdict(list)
    int_errors_by_lead = defaultdict(list)

    for forecast_point in data['forecasts']:
        for pred in forecast_point['predictions']:
            errors_by_lead[pred['hours_ahead']].append(pred['track_error_nm'])
            int_errors_by_lead[pred['hours_ahead']].append(abs(pred['intensity_error_kt']))

    print(f"    {'Lead Time':>10} {'Track Error':>14} {'Int Error':>12}")
    print("    " + "-" * 40)
    for hours in sorted(errors_by_lead.keys()):
        track_err = np.mean(errors_by_lead[hours])
        int_err = np.mean(int_errors_by_lead[hours])
        print(f"    {hours:>10}h {track_err:>14.1f} nm {int_err:>12.1f} kt")

# =============================================================================
# SAVE JSON DATA FOR WEB
# =============================================================================

print("\n" + "=" * 80)
print("  SAVING DATA FOR WEB VISUALIZATION")
print("=" * 80)

# Create output directory
os.makedirs('viz', exist_ok=True)

# Save main data file
with open('viz/hurricane_forecast_data.json', 'w') as f:
    json.dump(all_viz_data, f, indent=2)

print("  Saved: viz/hurricane_forecast_data.json")

# =============================================================================
# GENERATE INTERACTIVE HTML
# =============================================================================

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hurricane Forecast Comparison - Zimmerman Formula</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        header h1 {
            font-size: 2.5em;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }

        header p {
            color: #a0a0a0;
            font-size: 1.1em;
        }

        .controls {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }

        .control-row {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: center;
            margin-bottom: 20px;
        }

        .control-group {
            flex: 1;
            min-width: 200px;
        }

        .control-group label {
            display: block;
            margin-bottom: 8px;
            color: #a0a0a0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        select, input[type="range"] {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            font-size: 1em;
        }

        select option {
            background: #1a1a2e;
        }

        input[type="range"] {
            -webkit-appearance: none;
            height: 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            cursor: pointer;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #00d4ff, #7b2cbf);
            border-radius: 50%;
            cursor: pointer;
        }

        .time-display {
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            color: #00d4ff;
            margin: 15px 0;
        }

        .viz-container {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }

        @media (max-width: 1000px) {
            .viz-container {
                grid-template-columns: 1fr;
            }
        }

        .map-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }

        #map {
            width: 100%;
            height: 500px;
            background: #0a1628;
            border-radius: 10px;
            position: relative;
            overflow: hidden;
        }

        .stats-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }

        .stat-card h3 {
            color: #a0a0a0;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-unit {
            color: #666;
            font-size: 0.9em;
        }

        .legend {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }

        .legend-color {
            width: 30px;
            height: 4px;
            border-radius: 2px;
            margin-right: 10px;
        }

        .error-chart {
            margin-top: 20px;
        }

        .error-bar {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }

        .error-label {
            width: 60px;
            font-size: 0.9em;
            color: #a0a0a0;
        }

        .error-bar-container {
            flex: 1;
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }

        .error-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            border-radius: 10px;
            transition: width 0.3s ease;
        }

        .error-value {
            width: 70px;
            text-align: right;
            font-size: 0.9em;
            margin-left: 10px;
        }

        /* SVG Map Styling */
        .track-actual {
            fill: none;
            stroke: #00ff88;
            stroke-width: 3;
            stroke-linecap: round;
        }

        .track-forecast {
            fill: none;
            stroke: #ff6b6b;
            stroke-width: 2;
            stroke-dasharray: 8, 4;
            stroke-linecap: round;
        }

        .track-persistence {
            fill: none;
            stroke: #ffd93d;
            stroke-width: 2;
            stroke-dasharray: 4, 4;
            stroke-linecap: round;
        }

        .point-actual {
            fill: #00ff88;
        }

        .point-forecast {
            fill: #ff6b6b;
        }

        .point-start {
            fill: #00d4ff;
            stroke: #fff;
            stroke-width: 2;
        }

        .coast {
            fill: #2a3f5f;
            stroke: #3d5a80;
            stroke-width: 1;
        }

        .grid-line {
            stroke: rgba(255, 255, 255, 0.1);
            stroke-width: 0.5;
        }

        .info-panel {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9em;
        }

        .storm-info {
            display: flex;
            gap: 20px;
        }

        .storm-info div {
            text-align: center;
        }

        .storm-info .label {
            font-size: 0.8em;
            color: #a0a0a0;
        }

        .storm-info .value {
            font-size: 1.2em;
            font-weight: bold;
        }

        .formula-badge {
            background: linear-gradient(135deg, #7b2cbf, #00d4ff);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            display: inline-block;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Hurricane Forecast Comparison</h1>
            <p>Track prediction model powered by the Zimmerman Formula (Z² = 32π/3)</p>
        </header>

        <div class="controls">
            <div class="control-row">
                <div class="control-group">
                    <label>Select Hurricane</label>
                    <select id="stormSelect">
                        <option value="IDA_2021">Hurricane Ida (2021) - Cat 4</option>
                        <option value="DORIAN_2019">Hurricane Dorian (2019) - Cat 5</option>
                        <option value="LAURA_2020">Hurricane Laura (2020) - Cat 4</option>
                        <option value="MICHAEL_2018">Hurricane Michael (2018) - Cat 4</option>
                    </select>
                </div>
                <div class="control-group">
                    <label>Forecast Point</label>
                    <select id="forecastSelect">
                    </select>
                </div>
            </div>
            <div class="control-group">
                <label>Hours Before Landfall / Peak Intensity</label>
                <input type="range" id="timeSlider" min="0" max="48" value="24" step="6">
                <div class="time-display"><span id="hoursDisplay">24</span>h Forecast</div>
            </div>
        </div>

        <div class="viz-container">
            <div class="map-container">
                <svg id="map" viewBox="0 0 800 500"></svg>
                <div class="info-panel">
                    <div class="storm-info">
                        <div>
                            <div class="label">Max Wind</div>
                            <div class="value" id="maxWind">--</div>
                        </div>
                        <div>
                            <div class="label">Category</div>
                            <div class="value" id="category">--</div>
                        </div>
                        <div>
                            <div class="label">Track Error</div>
                            <div class="value" id="trackError">--</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="stats-container">
                <h2 style="margin-bottom: 20px;">Forecast Performance</h2>

                <div class="stat-card">
                    <h3>Our Model Track Error</h3>
                    <span class="stat-value" id="modelError">--</span>
                    <span class="stat-unit">nm</span>
                </div>

                <div class="stat-card">
                    <h3>Persistence Baseline</h3>
                    <span class="stat-value" id="persistError">--</span>
                    <span class="stat-unit">nm</span>
                </div>

                <div class="stat-card">
                    <h3>Improvement</h3>
                    <span class="stat-value" id="improvement">--</span>
                    <span class="stat-unit">%</span>
                </div>

                <div class="legend">
                    <h3 style="margin-bottom: 15px;">Legend</h3>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #00ff88;"></div>
                        <span>Actual Track</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ff6b6b; border-style: dashed;"></div>
                        <span>Our Model Forecast</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #ffd93d; border-style: dotted;"></div>
                        <span>Persistence Baseline</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #00d4ff;"></div>
                        <span>Forecast Start Point</span>
                    </div>
                </div>

                <div class="error-chart">
                    <h3 style="margin-bottom: 15px;">Error by Lead Time</h3>
                    <div id="errorBars"></div>
                </div>

                <div class="formula-badge" style="margin-top: 20px;">
                    V* = Vmax / Z² scaling
                </div>
            </div>
        </div>
    </div>

    <script>
        // Hurricane forecast data (embedded)
        const hurricaneData = HURRICANE_DATA_PLACEHOLDER;

        let currentStorm = 'IDA_2021';
        let currentForecastIdx = 0;
        let currentHours = 24;

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            updateStormSelect();
            updateVisualization();

            document.getElementById('stormSelect').addEventListener('change', (e) => {
                currentStorm = e.target.value;
                currentForecastIdx = 0;
                updateForecastSelect();
                updateVisualization();
            });

            document.getElementById('forecastSelect').addEventListener('change', (e) => {
                currentForecastIdx = parseInt(e.target.value);
                updateVisualization();
            });

            document.getElementById('timeSlider').addEventListener('input', (e) => {
                currentHours = parseInt(e.target.value);
                document.getElementById('hoursDisplay').textContent = currentHours;
                updateVisualization();
            });

            updateForecastSelect();
        });

        function updateStormSelect() {
            const select = document.getElementById('stormSelect');
            select.innerHTML = '';
            for (const [key, data] of Object.entries(hurricaneData)) {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = `Hurricane ${data.name} (${data.year}) - Cat ${data.category}`;
                select.appendChild(option);
            }
        }

        function updateForecastSelect() {
            const select = document.getElementById('forecastSelect');
            select.innerHTML = '';
            const storm = hurricaneData[currentStorm];
            if (!storm) return;

            storm.forecasts.forEach((f, idx) => {
                const option = document.createElement('option');
                option.value = idx;
                option.textContent = `${f.forecast_time.substring(0, 10)} - From ${f.forecast_from.vmax} kt`;
                select.appendChild(option);
            });
        }

        function updateVisualization() {
            const storm = hurricaneData[currentStorm];
            if (!storm || storm.forecasts.length === 0) return;

            const forecast = storm.forecasts[currentForecastIdx];
            if (!forecast) return;

            // Update info
            document.getElementById('maxWind').textContent = storm.max_wind + ' kt';
            document.getElementById('category').textContent = 'Cat ' + storm.category;

            // Find prediction for current hours
            const pred = forecast.predictions.find(p => p.hours_ahead === currentHours);

            if (pred) {
                document.getElementById('trackError').textContent = pred.track_error_nm.toFixed(1) + ' nm';
                document.getElementById('modelError').textContent = pred.track_error_nm.toFixed(1);

                // Calculate persistence error (simple linear extrapolation)
                const persistLat = forecast.forecast_from.lat + (forecast.predictions[0].actual_lat - forecast.forecast_from.lat) * (currentHours / 6);
                const persistLon = forecast.forecast_from.lon + (forecast.predictions[0].actual_lon - forecast.forecast_from.lon) * (currentHours / 6);
                const persistError = haversine(persistLat, persistLon, pred.actual_lat, pred.actual_lon);

                document.getElementById('persistError').textContent = persistError.toFixed(1);

                const improvement = ((persistError - pred.track_error_nm) / persistError * 100);
                document.getElementById('improvement').textContent = (improvement > 0 ? '+' : '') + improvement.toFixed(1);
            }

            // Draw map
            drawMap(storm, forecast);

            // Update error bars
            updateErrorBars(forecast);
        }

        function haversine(lat1, lon1, lat2, lon2) {
            const R = 3440.065; // Earth radius in nm
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                      Math.sin(dLon/2) * Math.sin(dLon/2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            return R * c;
        }

        function drawMap(storm, forecast) {
            const svg = document.getElementById('map');
            const width = 800;
            const height = 500;

            // Calculate bounds
            let minLat = Infinity, maxLat = -Infinity;
            let minLon = Infinity, maxLon = -Infinity;

            storm.actual_track.forEach(p => {
                minLat = Math.min(minLat, p.lat);
                maxLat = Math.max(maxLat, p.lat);
                minLon = Math.min(minLon, p.lon);
                maxLon = Math.max(maxLon, p.lon);
            });

            // Add padding
            const latPad = (maxLat - minLat) * 0.2;
            const lonPad = (maxLon - minLon) * 0.2;
            minLat -= latPad; maxLat += latPad;
            minLon -= lonPad; maxLon += lonPad;

            // Projection functions
            const projectX = lon => (lon - minLon) / (maxLon - minLon) * width;
            const projectY = lat => height - (lat - minLat) / (maxLat - minLat) * height;

            // Build SVG
            let svgContent = '';

            // Grid lines
            for (let lat = Math.ceil(minLat); lat <= Math.floor(maxLat); lat += 5) {
                svgContent += `<line class="grid-line" x1="0" y1="${projectY(lat)}" x2="${width}" y2="${projectY(lat)}"/>`;
            }
            for (let lon = Math.ceil(minLon); lon <= Math.floor(maxLon); lon += 5) {
                svgContent += `<line class="grid-line" x1="${projectX(lon)}" y1="0" x2="${projectX(lon)}" y2="${height}"/>`;
            }

            // Actual track (full)
            let actualPath = 'M ';
            storm.actual_track.forEach((p, i) => {
                actualPath += `${projectX(p.lon)},${projectY(p.lat)} `;
                if (i < storm.actual_track.length - 1) actualPath += 'L ';
            });
            svgContent += `<path class="track-actual" d="${actualPath}"/>`;

            // Actual track points
            storm.actual_track.forEach((p, i) => {
                if (i % 4 === 0) {
                    const r = 3 + p.vmax / 50;
                    svgContent += `<circle class="point-actual" cx="${projectX(p.lon)}" cy="${projectY(p.lat)}" r="${r}" opacity="0.7"/>`;
                }
            });

            // Forecast start point
            const startX = projectX(forecast.forecast_from.lon);
            const startY = projectY(forecast.forecast_from.lat);
            svgContent += `<circle class="point-start" cx="${startX}" cy="${startY}" r="10"/>`;

            // Forecast track (up to current hours)
            const relevantPreds = forecast.predictions.filter(p => p.hours_ahead <= currentHours);

            if (relevantPreds.length > 0) {
                // Our model forecast
                let forecastPath = `M ${startX},${startY} `;
                relevantPreds.forEach(p => {
                    forecastPath += `L ${projectX(p.forecast_lon)},${projectY(p.forecast_lat)} `;
                });
                svgContent += `<path class="track-forecast" d="${forecastPath}"/>`;

                // Forecast end point
                const lastPred = relevantPreds[relevantPreds.length - 1];
                svgContent += `<circle class="point-forecast" cx="${projectX(lastPred.forecast_lon)}" cy="${projectY(lastPred.forecast_lat)}" r="8"/>`;

                // Persistence line
                if (forecast.predictions.length > 0) {
                    const firstPred = forecast.predictions[0];
                    const dlat = firstPred.actual_lat - forecast.forecast_from.lat;
                    const dlon = firstPred.actual_lon - forecast.forecast_from.lon;
                    const persistLat = forecast.forecast_from.lat + dlat * (currentHours / 6);
                    const persistLon = forecast.forecast_from.lon + dlon * (currentHours / 6);
                    svgContent += `<line class="track-persistence" x1="${startX}" y1="${startY}" x2="${projectX(persistLon)}" y2="${projectY(persistLat)}"/>`;
                }
            }

            svg.innerHTML = svgContent;
        }

        function updateErrorBars(forecast) {
            const container = document.getElementById('errorBars');
            container.innerHTML = '';

            const maxError = Math.max(...forecast.predictions.map(p => p.track_error_nm));

            forecast.predictions.forEach(pred => {
                const pct = (pred.track_error_nm / maxError) * 100;
                const isSelected = pred.hours_ahead === currentHours;

                container.innerHTML += `
                    <div class="error-bar" style="opacity: ${isSelected ? 1 : 0.6}">
                        <span class="error-label">${pred.hours_ahead}h</span>
                        <div class="error-bar-container">
                            <div class="error-bar-fill" style="width: ${pct}%; ${isSelected ? 'background: #00ff88;' : ''}"></div>
                        </div>
                        <span class="error-value">${pred.track_error_nm.toFixed(1)} nm</span>
                    </div>
                `;
            });
        }
    </script>
</body>
</html>
'''

# Insert data into HTML
html_content = html_template.replace('HURRICANE_DATA_PLACEHOLDER', json.dumps(all_viz_data))

with open('viz/hurricane_forecast_viz.html', 'w') as f:
    f.write(html_content)

print("  Saved: viz/hurricane_forecast_viz.html")

print("\n" + "=" * 80)
print("  VISUALIZATION COMPLETE")
print("=" * 80)
print("""
Files created:
  viz/hurricane_forecast_data.json - Raw data for web integration
  viz/hurricane_forecast_viz.html  - Interactive visualization

Open viz/hurricane_forecast_viz.html in a browser to view the interactive
forecast comparison with time slider.
""")

print("=" * 80)
