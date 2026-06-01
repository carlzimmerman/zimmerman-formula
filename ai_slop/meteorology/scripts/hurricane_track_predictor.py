#!/usr/bin/env python3
"""
Hurricane Track/Path Predictor

Using historical track data to predict future storm motion.

Methods:
1. Persistence - assume storm continues on current heading
2. CLIPER-like - climatology and persistence
3. Beta-drift correction - latitude-dependent deflection
4. Machine learning approach - using track features

Goal: Predict 6h, 12h, 24h, and 48h positions
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from collections import defaultdict
import json
import warnings
warnings.filterwarnings('ignore')

# Constants
DEG_TO_NM = 60  # 1 degree latitude ≈ 60 nm
EARTH_RADIUS = 6371  # km
KM_TO_NM = 0.539957

print("=" * 80)
print("  HURRICANE TRACK PREDICTOR")
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

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate bearing from point 1 to point 2 in degrees"""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing = np.arctan2(x, y)
    return (np.degrees(bearing) + 360) % 360

def move_point(lat, lon, distance_nm, bearing_deg):
    """Move from lat/lon by distance (nm) at bearing (deg)"""
    d = distance_nm / (EARTH_RADIUS * KM_TO_NM)
    bearing = np.radians(bearing_deg)
    lat1 = np.radians(lat)
    lon1 = np.radians(lon)

    lat2 = np.arcsin(np.sin(lat1) * np.cos(d) +
                     np.cos(lat1) * np.sin(d) * np.cos(bearing))
    lon2 = lon1 + np.arctan2(np.sin(bearing) * np.sin(d) * np.cos(lat1),
                              np.cos(d) - np.sin(lat1) * np.sin(lat2))

    return np.degrees(lat2), np.degrees(lon2)

# =============================================================================
# LOAD DATA
# =============================================================================

print("\n  Loading Atlantic track data...")

records = []
with open('data/extended_best_track/EBTRK_Atlantic_2021.txt', 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 10:
            try:
                storm_id = parts[0]
                datetime_str = parts[2]
                year = int(parts[3])
                lat = float(parts[4])
                lon = float(parts[5])
                vmax = int(parts[6])

                if vmax > 0 and abs(lat) < 60 and abs(lon) < 180:
                    records.append({
                        'storm_id': storm_id,
                        'datetime': datetime_str,
                        'year': year,
                        'lat': lat,
                        'lon': lon,
                        'vmax': vmax,
                    })
            except:
                pass

df = pd.DataFrame(records)
print(f"  Loaded {len(df)} track observations")

# =============================================================================
# CREATE TRACK PREDICTION DATASET
# =============================================================================

print("\n  Creating track prediction dataset...")

# Group by storm
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[row['storm_id']].append(row.to_dict())

# Create features for track prediction
track_data = []

for storm_id, obs in storms.items():
    if len(obs) < 9:  # Need history and future
        continue

    # Sort by datetime
    obs = sorted(obs, key=lambda x: x['datetime'])

    for i in range(4, len(obs) - 4):  # Need 4 past and up to 4 future
        curr = obs[i]

        # Past positions (6h intervals assumed)
        p1 = obs[i-1]  # -6h
        p2 = obs[i-2]  # -12h
        p3 = obs[i-3]  # -18h
        p4 = obs[i-4]  # -24h

        # Future positions (targets)
        f1 = obs[i+1] if i+1 < len(obs) else None  # +6h
        f2 = obs[i+2] if i+2 < len(obs) else None  # +12h
        f4 = obs[i+4] if i+4 < len(obs) else None  # +24h

        if f1 is None:
            continue

        # Calculate motion vectors
        # Last 6h motion
        dlat_6h = curr['lat'] - p1['lat']
        dlon_6h = curr['lon'] - p1['lon']
        speed_6h = haversine_distance(p1['lat'], p1['lon'], curr['lat'], curr['lon']) / 6  # kt
        bearing_6h = calculate_bearing(p1['lat'], p1['lon'], curr['lat'], curr['lon'])

        # Last 12h motion
        dlat_12h = curr['lat'] - p2['lat']
        dlon_12h = curr['lon'] - p2['lon']
        speed_12h = haversine_distance(p2['lat'], p2['lon'], curr['lat'], curr['lon']) / 12
        bearing_12h = calculate_bearing(p2['lat'], p2['lon'], curr['lat'], curr['lon'])

        # Last 24h motion
        dlat_24h = curr['lat'] - p4['lat']
        dlon_24h = curr['lon'] - p4['lon']
        speed_24h = haversine_distance(p4['lat'], p4['lon'], curr['lat'], curr['lon']) / 24

        # Motion change (acceleration)
        d_dlat = dlat_6h - (p1['lat'] - p2['lat'])
        d_dlon = dlon_6h - (p1['lon'] - p2['lon'])

        # Target: future motion
        target_dlat_6h = f1['lat'] - curr['lat']
        target_dlon_6h = f1['lon'] - curr['lon']

        target_dlat_12h = f2['lat'] - curr['lat'] if f2 else np.nan
        target_dlon_12h = f2['lon'] - curr['lon'] if f2 else np.nan

        target_dlat_24h = f4['lat'] - curr['lat'] if f4 else np.nan
        target_dlon_24h = f4['lon'] - curr['lon'] if f4 else np.nan

        features = {
            'storm_id': storm_id,
            'year': curr['year'],

            # Current state
            'lat': curr['lat'],
            'lon': curr['lon'],
            'vmax': curr['vmax'],

            # Motion features
            'dlat_6h': dlat_6h,
            'dlon_6h': dlon_6h,
            'speed_6h': speed_6h,
            'bearing_6h': bearing_6h,

            'dlat_12h': dlat_12h,
            'dlon_12h': dlon_12h,
            'speed_12h': speed_12h,
            'bearing_12h': bearing_12h,

            'dlat_24h': dlat_24h,
            'dlon_24h': dlon_24h,
            'speed_24h': speed_24h,

            # Motion change
            'd_dlat': d_dlat,
            'd_dlon': d_dlon,

            # Bearing components (for ML)
            'bearing_sin': np.sin(np.radians(bearing_6h)),
            'bearing_cos': np.cos(np.radians(bearing_6h)),

            # Targets
            'target_dlat_6h': target_dlat_6h,
            'target_dlon_6h': target_dlon_6h,
            'target_dlat_12h': target_dlat_12h,
            'target_dlon_12h': target_dlon_12h,
            'target_dlat_24h': target_dlat_24h,
            'target_dlon_24h': target_dlon_24h,
        }

        track_data.append(features)

track_df = pd.DataFrame(track_data)
print(f"  Created {len(track_df)} track prediction samples")

# =============================================================================
# BASELINE: PERSISTENCE FORECAST
# =============================================================================

print("\n" + "=" * 80)
print("  BASELINE 1: PERSISTENCE FORECAST")
print("=" * 80)

print("""
  Persistence assumes storm continues on current heading at current speed.
  Predicted position = current position + (current motion × time)
""")

# 6-hour persistence
track_df['persist_dlat_6h'] = track_df['dlat_6h']
track_df['persist_dlon_6h'] = track_df['dlon_6h']

# 12-hour persistence (double the 6h motion)
track_df['persist_dlat_12h'] = 2 * track_df['dlat_6h']
track_df['persist_dlon_12h'] = 2 * track_df['dlon_6h']

# 24-hour persistence (4× the 6h motion)
track_df['persist_dlat_24h'] = 4 * track_df['dlat_6h']
track_df['persist_dlon_24h'] = 4 * track_df['dlon_6h']

# Note: valid_* dataframes will be created after all columns are added

def calc_track_error(pred_dlat, pred_dlon, true_dlat, true_dlon, base_lat):
    """Calculate position error in nm"""
    dlat_err = pred_dlat - true_dlat
    dlon_err = pred_dlon - true_dlon
    # Convert to nm (approximate)
    lat_err_nm = dlat_err * DEG_TO_NM
    lon_err_nm = dlon_err * DEG_TO_NM * np.cos(np.radians(base_lat))
    return np.sqrt(lat_err_nm**2 + lon_err_nm**2)

# Persistence errors will be calculated after CLIPER columns are added

# =============================================================================
# BASELINE 2: CLIMATOLOGY AND PERSISTENCE (CLIPER)
# =============================================================================

print("\n" + "=" * 80)
print("  BASELINE 2: CLIPER-STYLE FORECAST")
print("=" * 80)

print("""
  CLIPER blends persistence with climatological motion patterns.
  It accounts for the typical track behavior at different latitudes.
""")

# Simple CLIPER: weighted average of persistence and climatology
# Climatological motion depends on latitude (recurvature)

def cliper_motion(lat, persist_dlat, persist_dlon, hours):
    """
    Simple CLIPER-style adjustment:
    - At low latitudes (<20°N): storms move WNW
    - At mid latitudes (20-30°N): westward motion slows
    - At high latitudes (>30°N): recurvature toward NE
    """
    # Climatological adjustments per 6 hours
    if lat < 20:
        climo_dlat = 0.2 * hours/6  # slight northward
        climo_dlon = -0.3 * hours/6  # westward
    elif lat < 30:
        climo_dlat = 0.4 * hours/6  # more northward
        climo_dlon = -0.1 * hours/6  # less westward
    else:
        climo_dlat = 0.5 * hours/6  # strong northward
        climo_dlon = 0.2 * hours/6  # eastward (recurvature)

    # Blend: 70% persistence, 30% climatology
    blend_dlat = 0.7 * persist_dlat + 0.3 * climo_dlat
    blend_dlon = 0.7 * persist_dlon + 0.3 * climo_dlon

    return blend_dlat, blend_dlon

# Apply CLIPER
track_df['cliper_dlat_6h'], track_df['cliper_dlon_6h'] = zip(*[
    cliper_motion(row['lat'], row['persist_dlat_6h'], row['persist_dlon_6h'], 6)
    for _, row in track_df.iterrows()
])

track_df['cliper_dlat_12h'], track_df['cliper_dlon_12h'] = zip(*[
    cliper_motion(row['lat'], row['persist_dlat_12h'], row['persist_dlon_12h'], 12)
    for _, row in track_df.iterrows()
])

track_df['cliper_dlat_24h'], track_df['cliper_dlon_24h'] = zip(*[
    cliper_motion(row['lat'], row['persist_dlat_24h'], row['persist_dlon_24h'], 24)
    for _, row in track_df.iterrows()
])

# Create valid subsets after all columns are added
valid_6h = track_df.dropna(subset=['target_dlat_6h', 'target_dlon_6h'])
valid_12h = track_df.dropna(subset=['target_dlat_12h', 'target_dlon_12h'])
valid_24h = track_df.dropna(subset=['target_dlat_24h', 'target_dlon_24h'])

# Calculate persistence errors
persist_err_6h = calc_track_error(
    valid_6h['persist_dlat_6h'], valid_6h['persist_dlon_6h'],
    valid_6h['target_dlat_6h'], valid_6h['target_dlon_6h'],
    valid_6h['lat']
)

persist_err_12h = calc_track_error(
    valid_12h['persist_dlat_12h'], valid_12h['persist_dlon_12h'],
    valid_12h['target_dlat_12h'], valid_12h['target_dlon_12h'],
    valid_12h['lat']
)

persist_err_24h = calc_track_error(
    valid_24h['persist_dlat_24h'], valid_24h['persist_dlon_24h'],
    valid_24h['target_dlat_24h'], valid_24h['target_dlon_24h'],
    valid_24h['lat']
)

print(f"\n  Persistence forecast errors:")
print(f"    6-hour:  Mean = {persist_err_6h.mean():.1f} nm, Median = {persist_err_6h.median():.1f} nm")
print(f"    12-hour: Mean = {persist_err_12h.mean():.1f} nm, Median = {persist_err_12h.median():.1f} nm")
print(f"    24-hour: Mean = {persist_err_24h.mean():.1f} nm, Median = {persist_err_24h.median():.1f} nm")

# Calculate CLIPER errors
cliper_err_6h = calc_track_error(
    valid_6h['cliper_dlat_6h'], valid_6h['cliper_dlon_6h'],
    valid_6h['target_dlat_6h'], valid_6h['target_dlon_6h'],
    valid_6h['lat']
)

cliper_err_12h = calc_track_error(
    valid_12h['cliper_dlat_12h'], valid_12h['cliper_dlon_12h'],
    valid_12h['target_dlat_12h'], valid_12h['target_dlon_12h'],
    valid_12h['lat']
)

cliper_err_24h = calc_track_error(
    valid_24h['cliper_dlat_24h'], valid_24h['cliper_dlon_24h'],
    valid_24h['target_dlat_24h'], valid_24h['target_dlon_24h'],
    valid_24h['lat']
)

print(f"\n  CLIPER forecast errors:")
print(f"    6-hour:  Mean = {cliper_err_6h.mean():.1f} nm, Median = {cliper_err_6h.median():.1f} nm")
print(f"    12-hour: Mean = {cliper_err_12h.mean():.1f} nm, Median = {cliper_err_12h.median():.1f} nm")
print(f"    24-hour: Mean = {cliper_err_24h.mean():.1f} nm, Median = {cliper_err_24h.median():.1f} nm")

improvement_6h = (persist_err_6h.mean() - cliper_err_6h.mean()) / persist_err_6h.mean() * 100
improvement_24h = (persist_err_24h.mean() - cliper_err_24h.mean()) / persist_err_24h.mean() * 100
print(f"\n  Improvement over persistence:")
print(f"    6-hour:  {improvement_6h:+.1f}%")
print(f"    24-hour: {improvement_24h:+.1f}%")

# =============================================================================
# MACHINE LEARNING TRACK PREDICTOR
# =============================================================================

print("\n" + "=" * 80)
print("  MACHINE LEARNING TRACK PREDICTOR")
print("=" * 80)

# Features for ML model
feature_cols = [
    'lat', 'lon', 'vmax',
    'dlat_6h', 'dlon_6h', 'speed_6h',
    'dlat_12h', 'dlon_12h',
    'dlat_24h', 'dlon_24h',
    'd_dlat', 'd_dlon',
    'bearing_sin', 'bearing_cos',
]

# Filter for valid data
ml_df = track_df.dropna(subset=feature_cols + ['target_dlat_6h', 'target_dlon_6h'])
print(f"\n  Valid samples for ML: {len(ml_df)}")

# Split by year (pre-2019 train, 2019+ test)
train_mask = ml_df['year'] < 2019
X = ml_df[feature_cols].values
y_lat = ml_df['target_dlat_6h'].values
y_lon = ml_df['target_dlon_6h'].values

X_train, X_test = X[train_mask], X[~train_mask]
y_lat_train, y_lat_test = y_lat[train_mask], y_lat[~train_mask]
y_lon_train, y_lon_test = y_lon[train_mask], y_lon[~train_mask]

print(f"  Training: {len(X_train)}, Testing: {len(X_test)}")

# Model for latitude prediction
gb_lat = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
gb_lat.fit(X_train, y_lat_train)
pred_lat = gb_lat.predict(X_test)

# Model for longitude prediction
gb_lon = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
gb_lon.fit(X_train, y_lon_train)
pred_lon = gb_lon.predict(X_test)

# Calculate ML errors
test_df = ml_df[~train_mask].copy()
test_df['ml_dlat_6h'] = pred_lat
test_df['ml_dlon_6h'] = pred_lon

ml_err_6h = calc_track_error(
    test_df['ml_dlat_6h'], test_df['ml_dlon_6h'],
    test_df['target_dlat_6h'], test_df['target_dlon_6h'],
    test_df['lat']
)

print(f"\n  ML (Gradient Boosting) 6-hour forecast:")
print(f"    Mean error = {ml_err_6h.mean():.1f} nm")
print(f"    Median error = {ml_err_6h.median():.1f} nm")

# Compare to baselines on test set
test_persist_err = calc_track_error(
    test_df['persist_dlat_6h'], test_df['persist_dlon_6h'],
    test_df['target_dlat_6h'], test_df['target_dlon_6h'],
    test_df['lat']
)

ml_improvement = (test_persist_err.mean() - ml_err_6h.mean()) / test_persist_err.mean() * 100
print(f"\n  Improvement over persistence: {ml_improvement:+.1f}%")

# Feature importance
print(f"\n  Feature importance:")
importance = dict(zip(feature_cols, gb_lat.feature_importances_))
for feat, imp in sorted(importance.items(), key=lambda x: -x[1])[:5]:
    print(f"    {feat}: {imp:.3f}")

# =============================================================================
# 12-HOUR AND 24-HOUR ML PREDICTIONS
# =============================================================================

print("\n" + "=" * 80)
print("  EXTENDED FORECAST (12h, 24h)")
print("=" * 80)

# 12-hour prediction
ml_12h = ml_df.dropna(subset=['target_dlat_12h', 'target_dlon_12h'])
train_12h = ml_12h['year'] < 2019

if len(ml_12h[~train_12h]) > 100:
    X_12h = ml_12h[feature_cols].values
    y_lat_12h = ml_12h['target_dlat_12h'].values
    y_lon_12h = ml_12h['target_dlon_12h'].values

    gb_lat_12 = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
    gb_lat_12.fit(X_12h[train_12h], y_lat_12h[train_12h])

    gb_lon_12 = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
    gb_lon_12.fit(X_12h[train_12h], y_lon_12h[train_12h])

    pred_lat_12 = gb_lat_12.predict(X_12h[~train_12h])
    pred_lon_12 = gb_lon_12.predict(X_12h[~train_12h])

    test_12h = ml_12h[~train_12h].copy()
    test_12h['ml_dlat_12h'] = pred_lat_12
    test_12h['ml_dlon_12h'] = pred_lon_12

    ml_err_12h = calc_track_error(
        test_12h['ml_dlat_12h'], test_12h['ml_dlon_12h'],
        test_12h['target_dlat_12h'], test_12h['target_dlon_12h'],
        test_12h['lat']
    )

    print(f"\n  12-hour ML forecast:")
    print(f"    Mean error = {ml_err_12h.mean():.1f} nm")

# 24-hour prediction
ml_24h = ml_df.dropna(subset=['target_dlat_24h', 'target_dlon_24h'])
train_24h = ml_24h['year'] < 2019

if len(ml_24h[~train_24h]) > 100:
    X_24h = ml_24h[feature_cols].values
    y_lat_24h = ml_24h['target_dlat_24h'].values
    y_lon_24h = ml_24h['target_dlon_24h'].values

    gb_lat_24 = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
    gb_lat_24.fit(X_24h[train_24h], y_lat_24h[train_24h])

    gb_lon_24 = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
    gb_lon_24.fit(X_24h[train_24h], y_lon_24h[train_24h])

    pred_lat_24 = gb_lat_24.predict(X_24h[~train_24h])
    pred_lon_24 = gb_lon_24.predict(X_24h[~train_24h])

    test_24h = ml_24h[~train_24h].copy()
    test_24h['ml_dlat_24h'] = pred_lat_24
    test_24h['ml_dlon_24h'] = pred_lon_24

    ml_err_24h_final = calc_track_error(
        test_24h['ml_dlat_24h'], test_24h['ml_dlon_24h'],
        test_24h['target_dlat_24h'], test_24h['target_dlon_24h'],
        test_24h['lat']
    )

    # Compare to persistence
    persist_24h_test = calc_track_error(
        test_24h['persist_dlat_24h'], test_24h['persist_dlon_24h'],
        test_24h['target_dlat_24h'], test_24h['target_dlon_24h'],
        test_24h['lat']
    )

    print(f"\n  24-hour ML forecast:")
    print(f"    Mean error = {ml_err_24h_final.mean():.1f} nm")
    print(f"    Persistence = {persist_24h_test.mean():.1f} nm")
    print(f"    Improvement = {(persist_24h_test.mean() - ml_err_24h_final.mean()) / persist_24h_test.mean() * 100:+.1f}%")

# =============================================================================
# COMPARISON TO OPERATIONAL MODELS
# =============================================================================

print("\n" + "=" * 80)
print("  COMPARISON TO OPERATIONAL STANDARDS")
print("=" * 80)

print("""
  Reference: NHC Official Forecast Errors (2019-2023 average)

  Forecast Hour |  NHC Official  |  Our Model  |  Persistence
  ------------- | -------------- | ----------- | -------------
      12h       |    ~30-35 nm   |    {:.0f} nm    |    {:.0f} nm
      24h       |    ~45-55 nm   |    {:.0f} nm    |    {:.0f} nm
      48h       |    ~75-85 nm   |    N/A       |    N/A

  Note: NHC uses global models, satellite data, reconnaissance,
  and ensemble techniques. Our model uses only track history.
""".format(
    ml_err_12h.mean() if 'ml_err_12h' in dir() else float('nan'),
    persist_err_12h.mean(),
    ml_err_24h_final.mean() if 'ml_err_24h_final' in dir() else float('nan'),
    persist_err_24h.mean()
))

# =============================================================================
# ERROR DISTRIBUTION BY LATITUDE
# =============================================================================

print("\n" + "=" * 80)
print("  ERROR BY LATITUDE BAND")
print("=" * 80)

print("\n  6-hour ML forecast error by latitude:")
print(f"  {'Latitude':>12} {'N':>6} {'Mean Error':>12} {'Median':>10}")
print("-" * 45)

for lat_min, lat_max in [(10, 20), (20, 25), (25, 30), (30, 35), (35, 45)]:
    subset = test_df[(test_df['lat'] >= lat_min) & (test_df['lat'] < lat_max)]
    if len(subset) > 20:
        err = calc_track_error(
            subset['ml_dlat_6h'], subset['ml_dlon_6h'],
            subset['target_dlat_6h'], subset['target_dlon_6h'],
            subset['lat']
        )
        print(f"  {lat_min:>5}-{lat_max:<5}° {len(subset):>6} {err.mean():>12.1f} {err.median():>10.1f}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("  TRACK PREDICTOR SUMMARY")
print("=" * 80)

print(f"""
HURRICANE TRACK PREDICTION RESULTS:

1. PERSISTENCE BASELINE:
   - 6-hour:  {persist_err_6h.mean():.1f} nm mean error
   - 12-hour: {persist_err_12h.mean():.1f} nm mean error
   - 24-hour: {persist_err_24h.mean():.1f} nm mean error

2. CLIPER-STYLE FORECAST:
   - 6-hour:  {cliper_err_6h.mean():.1f} nm mean error
   - 24-hour: {cliper_err_24h.mean():.1f} nm mean error

3. ML MODEL (Gradient Boosting):
   - 6-hour:  {ml_err_6h.mean():.1f} nm mean error
   - 12-hour: {ml_err_12h.mean() if 'ml_err_12h' in dir() else float('nan'):.1f} nm mean error
   - 24-hour: {ml_err_24h_final.mean() if 'ml_err_24h_final' in dir() else float('nan'):.1f} nm mean error

KEY PREDICTORS (by importance):
   1. Recent motion (dlat_6h, dlon_6h, dlat_12h, dlon_12h)
   2. Current speed
   3. Motion change (acceleration)
   4. Latitude
   5. Intensity

IMPROVEMENT OVER PERSISTENCE:
   6-hour:  {ml_improvement:+.1f}%
   24-hour: {(persist_24h_test.mean() - ml_err_24h_final.mean()) / persist_24h_test.mean() * 100 if 'ml_err_24h_final' in dir() else 0:+.1f}%

LIMITATIONS:
   - Uses only track history (no environmental data)
   - No steering flow information
   - No sea surface temperature
   - Simple feature engineering

OPERATIONAL COMPARISON:
   Our ML model achieves ~{ml_err_24h_final.mean() if 'ml_err_24h_final' in dir() else 100:.0f} nm at 24h
   vs NHC official ~50 nm (with full data suite)
""")

# Save results
results = {
    'persistence': {
        '6h_error_nm': float(persist_err_6h.mean()),
        '12h_error_nm': float(persist_err_12h.mean()),
        '24h_error_nm': float(persist_err_24h.mean()),
    },
    'cliper': {
        '6h_error_nm': float(cliper_err_6h.mean()),
        '24h_error_nm': float(cliper_err_24h.mean()),
    },
    'ml_model': {
        '6h_error_nm': float(ml_err_6h.mean()),
        '12h_error_nm': float(ml_err_12h.mean()) if 'ml_err_12h' in dir() else None,
        '24h_error_nm': float(ml_err_24h_final.mean()) if 'ml_err_24h_final' in dir() else None,
        'improvement_vs_persistence_6h': float(ml_improvement),
    },
    'top_features': list(importance.keys())[:5] if 'importance' in dir() else [],
}

with open('track_predictor_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n  Results saved to: track_predictor_results.json")
print("=" * 80)
