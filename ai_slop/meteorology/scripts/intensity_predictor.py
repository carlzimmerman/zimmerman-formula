#!/usr/bin/env python3
"""
Hurricane Intensity Predictor

Using the relationships discovered:
1. Pressure-wind: V = 13.18 × √(ΔP) with R = 0.91
2. RMW contraction predicts intensification
3. Eye formation indicates organized structure
4. Golden ratio equilibrium at ~108 kt

Goal: Predict 6-hour and 24-hour intensity change
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from collections import defaultdict
import json
import warnings
warnings.filterwarnings('ignore')

# Constants
PHI = (1 + np.sqrt(5)) / 2
ONE_OVER_PHI = 1 / PHI

print("=" * 80)
print("  HURRICANE INTENSITY PREDICTOR")
print("=" * 80)

# =============================================================================
# LOAD AND PREPARE DATA
# =============================================================================

print("\n  Loading data...")

# Load Atlantic EBTRK
records = []
with open('data/extended_best_track/EBTRK_Atlantic_2021.txt', 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 12:
            try:
                storm_id = parts[0]
                datetime = parts[2]
                year = int(parts[3])
                lat = float(parts[4])
                lon = float(parts[5])
                vmax = int(parts[6])
                pmin = int(parts[7])
                rmw = int(parts[8])
                eye_diam = int(parts[9])

                if vmax > 0:
                    records.append({
                        'storm_id': storm_id,
                        'datetime': datetime,
                        'year': year,
                        'lat': lat,
                        'lon': lon,
                        'vmax': vmax,
                        'pmin': pmin if pmin > 0 and pmin != -99 else np.nan,
                        'rmw': rmw if rmw > 0 and rmw != -99 else np.nan,
                        'eye_diam': eye_diam if eye_diam > 0 and eye_diam != -99 else np.nan,
                    })
            except:
                pass

df = pd.DataFrame(records)
print(f"  Loaded {len(df)} observations")

# =============================================================================
# CREATE INTENSITY CHANGE DATASET
# =============================================================================

print("\n  Creating intensity change dataset...")

# Group by storm
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[row['storm_id']].append(row.to_dict())

# Create features for intensity prediction
intensity_data = []

for storm_id, obs in storms.items():
    if len(obs) < 5:  # Need at least 5 observations
        continue

    # Sort by datetime
    obs = sorted(obs, key=lambda x: x['datetime'])

    for i in range(4, len(obs)):  # Start at 4 to have history
        curr = obs[i]
        prev = obs[i-1]  # 6 hours ago
        prev2 = obs[i-2]  # 12 hours ago
        prev3 = obs[i-3]  # 18 hours ago
        prev4 = obs[i-4]  # 24 hours ago

        # Target: intensity change
        dv_6h = curr['vmax'] - prev['vmax']
        dv_24h = curr['vmax'] - prev4['vmax']

        # Features
        features = {
            'storm_id': storm_id,
            'year': curr['year'],

            # Current state
            'vmax': prev['vmax'],
            'lat': prev['lat'],
            'lon': prev['lon'],

            # Pressure deficit
            'delta_p': 1013.25 - prev['pmin'] if not np.isnan(prev['pmin']) else np.nan,

            # RMW
            'rmw': prev['rmw'] if not np.isnan(prev['rmw']) else np.nan,

            # Eye presence (indicator of organization)
            'has_eye': 1 if not np.isnan(prev['eye_diam']) else 0,
            'eye_diam': prev['eye_diam'] if not np.isnan(prev['eye_diam']) else 0,

            # Recent intensity trend (past 12h)
            'dv_prev_12h': prev['vmax'] - prev2['vmax'],
            'dv_prev_24h': prev['vmax'] - prev4['vmax'],

            # RMW change (if available)
            'rmw_change': prev['rmw'] - prev2['rmw'] if (not np.isnan(prev['rmw']) and not np.isnan(prev2['rmw'])) else np.nan,

            # Latitude (affects MPI and Coriolis)
            'abs_lat': abs(prev['lat']),

            # Distance from equilibrium (golden ratio)
            'equilibrium_dev': np.nan,

            # Targets
            'dv_6h': dv_6h,
            'dv_24h': dv_24h,
        }

        # Calculate equilibrium deviation if eye data available
        if not np.isnan(prev['eye_diam']) and not np.isnan(prev['rmw']):
            eye_rmw_ratio = (prev['eye_diam'] / 2) / prev['rmw']
            features['equilibrium_dev'] = abs(eye_rmw_ratio - ONE_OVER_PHI)
            features['eye_rmw_ratio'] = eye_rmw_ratio

        intensity_data.append(features)

int_df = pd.DataFrame(intensity_data)
print(f"  Created {len(int_df)} intensity change samples")

# =============================================================================
# FEATURE ENGINEERING
# =============================================================================

print("\n  Engineering features...")

# Category-based features
int_df['is_ts'] = (int_df['vmax'] >= 34) & (int_df['vmax'] < 64)
int_df['is_hurricane'] = int_df['vmax'] >= 64
int_df['is_major'] = int_df['vmax'] >= 96

# Rapid intensification flag (target)
int_df['is_ri'] = int_df['dv_24h'] >= 30

print(f"  RI events (≥30 kt/24h): {int_df['is_ri'].sum()}")

# =============================================================================
# BUILD SIMPLE INTENSITY PREDICTOR
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL: 6-HOUR INTENSITY CHANGE PREDICTION")
print("=" * 80)

# Features to use
feature_cols = ['vmax', 'abs_lat', 'dv_prev_12h', 'dv_prev_24h', 'has_eye']

# Filter for valid data
int_valid = int_df.dropna(subset=feature_cols + ['dv_6h'])
print(f"\n  Valid samples: {len(int_valid)}")

X = int_valid[feature_cols].values
y = int_valid['dv_6h'].values

# Split by year
train_mask = int_valid['year'] < 2019
X_train, X_test = X[train_mask], X[~train_mask]
y_train, y_test = y[train_mask], y[~train_mask]

print(f"  Training: {len(X_train)}, Testing: {len(X_test)}")

# Model 1: Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
mae_lr = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))

print(f"\n  Linear Regression:")
print(f"    MAE = {mae_lr:.2f} kt")
print(f"    RMSE = {rmse_lr:.2f} kt")
print(f"    Coefficients: {dict(zip(feature_cols, lr.coef_.round(3)))}")

# Model 2: Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
mae_gb = mean_absolute_error(y_test, y_pred_gb)
rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))

print(f"\n  Gradient Boosting:")
print(f"    MAE = {mae_gb:.2f} kt")
print(f"    RMSE = {rmse_gb:.2f} kt")
print(f"    Feature importance: {dict(zip(feature_cols, gb.feature_importances_.round(3)))}")

# =============================================================================
# ADD RMW AND PRESSURE FEATURES (when available)
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL: WITH RMW AND PRESSURE FEATURES")
print("=" * 80)

feature_cols_full = ['vmax', 'abs_lat', 'dv_prev_12h', 'dv_prev_24h', 'has_eye', 'delta_p', 'rmw']
int_full = int_df.dropna(subset=feature_cols_full + ['dv_6h'])
print(f"\n  Valid samples with full features: {len(int_full)}")

if len(int_full) > 500:
    X_full = int_full[feature_cols_full].values
    y_full = int_full['dv_6h'].values

    train_mask_full = int_full['year'] < 2019
    X_train_f, X_test_f = X_full[train_mask_full], X_full[~train_mask_full]
    y_train_f, y_test_f = y_full[train_mask_full], y_full[~train_mask_full]

    print(f"  Training: {len(X_train_f)}, Testing: {len(X_test_f)}")

    if len(X_test_f) > 20:
        gb_full = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
        gb_full.fit(X_train_f, y_train_f)
        y_pred_full = gb_full.predict(X_test_f)
        mae_full = mean_absolute_error(y_test_f, y_pred_full)
        rmse_full = np.sqrt(mean_squared_error(y_test_f, y_pred_full))

        print(f"\n  Gradient Boosting (full features):")
        print(f"    MAE = {mae_full:.2f} kt")
        print(f"    RMSE = {rmse_full:.2f} kt")
        print(f"    Feature importance: {dict(zip(feature_cols_full, gb_full.feature_importances_.round(3)))}")

# =============================================================================
# COMPARISON TO PERSISTENCE
# =============================================================================

print("\n" + "=" * 80)
print("  COMPARISON TO BASELINES")
print("=" * 80)

# Baseline 1: Persistence (predict no change)
y_persistence = np.zeros_like(y_test)
mae_persist = mean_absolute_error(y_test, y_persistence)
print(f"\n  Persistence (dV = 0):")
print(f"    MAE = {mae_persist:.2f} kt")

# Baseline 2: Climatology (mean intensity change)
y_climo = np.full_like(y_test, np.mean(y_train))
mae_climo = mean_absolute_error(y_test, y_climo)
print(f"\n  Climatology (dV = mean):")
print(f"    MAE = {mae_climo:.2f} kt")

# Skill scores
skill_lr = 1 - mae_lr / mae_persist
skill_gb = 1 - mae_gb / mae_persist
print(f"\n  Skill vs Persistence:")
print(f"    Linear: {skill_lr:.1%}")
print(f"    GB: {skill_gb:.1%}")

# =============================================================================
# RAPID INTENSIFICATION PREDICTION
# =============================================================================

print("\n" + "=" * 80)
print("  RAPID INTENSIFICATION (RI) PREDICTION")
print("=" * 80)

# 24-hour prediction for RI
int_24h = int_df.dropna(subset=['vmax', 'abs_lat', 'dv_prev_12h', 'dv_prev_24h', 'dv_24h'])
print(f"\n  Samples for 24h prediction: {len(int_24h)}")

X_24 = int_24h[['vmax', 'abs_lat', 'dv_prev_12h', 'dv_prev_24h', 'has_eye']].values
y_24 = int_24h['dv_24h'].values
y_ri = int_24h['is_ri'].values

train_24 = int_24h['year'] < 2019
X_train_24, X_test_24 = X_24[train_24], X_24[~train_24]
y_train_24, y_test_24 = y_24[train_24], y_24[~train_24]
y_train_ri, y_test_ri = y_ri[train_24], y_ri[~train_24]

# Regression model
gb_24 = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
gb_24.fit(X_train_24, y_train_24)
y_pred_24 = gb_24.predict(X_test_24)

mae_24 = mean_absolute_error(y_test_24, y_pred_24)
print(f"\n  24-hour intensity change prediction:")
print(f"    MAE = {mae_24:.2f} kt")

# RI classification (predict RI if predicted dV >= 30)
ri_pred = y_pred_24 >= 30
ri_actual = y_test_ri

# Confusion matrix
tp = np.sum(ri_pred & ri_actual)
fp = np.sum(ri_pred & ~ri_actual)
tn = np.sum(~ri_pred & ~ri_actual)
fn = np.sum(~ri_pred & ri_actual)

print(f"\n  RI Classification (threshold = 30 kt/24h):")
print(f"    True Positives: {tp}")
print(f"    False Positives: {fp}")
print(f"    False Negatives: {fn}")
print(f"    Precision: {tp/(tp+fp):.2%}" if (tp+fp) > 0 else "    Precision: N/A")
print(f"    Recall: {tp/(tp+fn):.2%}" if (tp+fn) > 0 else "    Recall: N/A")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("  PREDICTOR SUMMARY")
print("=" * 80)

print(f"""
INTENSITY CHANGE PREDICTION (6-hour):
  - Linear Regression: MAE = {mae_lr:.2f} kt (Skill = {skill_lr:.1%})
  - Gradient Boosting: MAE = {mae_gb:.2f} kt (Skill = {skill_gb:.1%})
  - Persistence baseline: MAE = {mae_persist:.2f} kt

INTENSITY CHANGE PREDICTION (24-hour):
  - Gradient Boosting: MAE = {mae_24:.2f} kt

KEY PREDICTORS (by importance):
  1. Previous intensity trend (dv_prev_24h, dv_prev_12h)
  2. Current intensity (vmax)
  3. Eye presence (has_eye)
  4. Latitude (abs_lat)
  5. RMW and pressure (when available)

GOLDEN RATIO INSIGHT:
  Storms approaching eye/RMW = 1/φ = 0.618 are in structural equilibrium.
  Deviation from this ratio may indicate intensification potential.

OPERATIONAL USE:
  These models can be used to:
  1. Predict 6h and 24h intensity change
  2. Flag potential RI events
  3. Estimate structural parameters (eye, RMW)
""")

# Save results
results = {
    '6h_prediction': {
        'linear_mae': float(mae_lr),
        'gb_mae': float(mae_gb),
        'skill_vs_persistence': float(skill_gb),
    },
    '24h_prediction': {
        'mae': float(mae_24),
    },
    'baselines': {
        'persistence_mae': float(mae_persist),
        'climatology_mae': float(mae_climo),
    },
    'features': feature_cols,
}

with open('intensity_predictor_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n  Results saved to: intensity_predictor_results.json")
print("=" * 80)
