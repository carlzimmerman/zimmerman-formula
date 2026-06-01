#!/usr/bin/env python3
"""
Enhanced Track Model with SHIPS Atmospheric Data

This script tests whether adding SHIPS environmental predictors
(wind shear, SST, steering flow) improves our track forecasting.

Comparison:
1. Baseline: Track-only features (lat, lon, motion)
2. Enhanced: Track + SHIPS atmospheric predictors
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("  ENHANCED TRACK MODEL: BASELINE vs SHIPS-ENHANCED")
print("=" * 80)

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Z_SQUARED = 32 * np.pi / 3  # 33.51

# Load SHIPS features
ships_df = pd.read_csv(os.path.join(DATA_DIR, 'data/ships/ships_features.csv'))
print(f"\n  Loaded {len(ships_df)} samples from SHIPS data")
print(f"  Years: {ships_df['year'].min()} - {ships_df['year'].max()}")

# Filter to lead time = 24h for comparison
df = ships_df[ships_df['lead_time'] == 24].copy()
print(f"  Using {len(df)} samples at 24h lead time")

# Define feature sets
BASELINE_FEATURES = [
    'LAT_t0', 'LON_t0', 'VMAX_t0',  # Position and intensity
]

SHIPS_FEATURES = [
    # Environmental steering
    'SHRD_t0', 'SHDC_t0',           # Vertical shear
    'U200_t0', 'V20C_t0',           # Upper-level winds
    'V850_t0', 'V500_t0',           # Mid-level winds
    'D200_t0', 'DIVC_t0',           # Divergence

    # Thermodynamic
    'CSST_t0', 'COHC_t0',           # SST and ocean heat
    'RHLO_t0', 'RHMD_t0',           # Humidity
    'VMPI_t0',                       # Max potential intensity

    # Position and motion
    'DTL_t0',                        # Distance to land
    'TWAC_t0', 'TWXC_t0',           # Track motion
]

# Targets
TARGET_LAT = 'dlat'
TARGET_LON = 'dlon'

# Calculate targets if not present
if TARGET_LAT not in df.columns:
    df[TARGET_LAT] = df['LAT_t24'] - df['LAT_t0']
if TARGET_LON not in df.columns:
    df[TARGET_LON] = df['LON_t24'] - df['LON_t0']

# Clean data
df = df.replace([np.inf, -np.inf], np.nan)

# ============================================================================
# PREPARE DATA
# ============================================================================

# Filter to valid samples
baseline_cols = BASELINE_FEATURES + [TARGET_LAT, TARGET_LON]
ships_cols = BASELINE_FEATURES + SHIPS_FEATURES + [TARGET_LAT, TARGET_LON]

# Baseline dataset
baseline_df = df[baseline_cols].dropna()
print(f"\n  Baseline samples (track only): {len(baseline_df)}")

# SHIPS-enhanced dataset
ships_valid = [c for c in ships_cols if c in df.columns]
enhanced_df = df[ships_valid].dropna()
print(f"  SHIPS-enhanced samples: {len(enhanced_df)}")

# Use common samples for fair comparison
common_idx = baseline_df.index.intersection(enhanced_df.index)
baseline_df = baseline_df.loc[common_idx]
enhanced_df = enhanced_df.loc[common_idx]
print(f"  Common samples for comparison: {len(common_idx)}")

# Scale units (LAT/LON are in tenths of degrees, convert to degrees)
for col in ['LAT_t0', 'LON_t0', TARGET_LAT, TARGET_LON]:
    if col in baseline_df.columns:
        baseline_df[col] = baseline_df[col] / 10.0
    if col in enhanced_df.columns:
        enhanced_df[col] = enhanced_df[col] / 10.0

# ============================================================================
# HAVERSINE DISTANCE
# ============================================================================

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate great-circle distance in nautical miles"""
    R = 3440.065  # Earth radius in nm
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

# ============================================================================
# TRAIN AND EVALUATE MODELS
# ============================================================================

def train_and_evaluate(X, y_lat, y_lon, name, n_splits=5):
    """Train model and evaluate with cross-validation"""

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Models
    model_lat = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
    model_lon = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)

    # Time series cross-validation
    tscv = TimeSeriesSplit(n_splits=n_splits)

    errors = []
    for train_idx, test_idx in tscv.split(X_scaled):
        X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
        y_lat_train, y_lat_test = y_lat.iloc[train_idx], y_lat.iloc[test_idx]
        y_lon_train, y_lon_test = y_lon.iloc[train_idx], y_lon.iloc[test_idx]

        # Train
        model_lat.fit(X_train, y_lat_train)
        model_lon.fit(X_train, y_lon_train)

        # Predict
        pred_dlat = model_lat.predict(X_test)
        pred_dlon = model_lon.predict(X_test)

        # Calculate track errors
        actual_lat = baseline_df.loc[y_lat_test.index, 'LAT_t0'].values + y_lat_test.values
        actual_lon = baseline_df.loc[y_lon_test.index, 'LON_t0'].values + y_lon_test.values
        pred_lat = baseline_df.loc[y_lat_test.index, 'LAT_t0'].values + pred_dlat
        pred_lon = baseline_df.loc[y_lon_test.index, 'LON_t0'].values + pred_dlon

        for i in range(len(pred_lat)):
            err = haversine_distance(pred_lat[i], pred_lon[i], actual_lat[i], actual_lon[i])
            if not np.isnan(err) and err < 5000:  # Filter outliers
                errors.append(err)

    errors = np.array(errors)
    return {
        'name': name,
        'mean_error': np.mean(errors),
        'std_error': np.std(errors),
        'median_error': np.median(errors),
        'n_samples': len(errors),
        'errors': errors,
    }

print("\n" + "=" * 80)
print("  TRAINING MODELS")
print("=" * 80)

# Baseline model (track only)
print("\n  Training BASELINE model (track features only)...")
X_baseline = baseline_df[BASELINE_FEATURES].values
y_lat_baseline = baseline_df[TARGET_LAT]
y_lon_baseline = baseline_df[TARGET_LON]
baseline_results = train_and_evaluate(X_baseline, y_lat_baseline, y_lon_baseline, "Baseline")

# SHIPS-enhanced model
print("  Training SHIPS-ENHANCED model...")
ships_feat_valid = [f for f in BASELINE_FEATURES + SHIPS_FEATURES if f in enhanced_df.columns]
X_enhanced = enhanced_df[ships_feat_valid].values
y_lat_enhanced = enhanced_df[TARGET_LAT]
y_lon_enhanced = enhanced_df[TARGET_LON]
enhanced_results = train_and_evaluate(X_enhanced, y_lat_enhanced, y_lon_enhanced, "SHIPS-Enhanced")

# ============================================================================
# RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("  RESULTS: 24-HOUR TRACK FORECAST ERRORS")
print("=" * 80)

print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  MODEL COMPARISON: 24h Track Forecast Error (nm)                │
  ├─────────────────────────────────────────────────────────────────┤
  │                                                                 │
  │  BASELINE (Track Only)                                          │
  │    Mean Error:   {baseline_results['mean_error']:>7.1f} nm                                  │
  │    Median Error: {baseline_results['median_error']:>7.1f} nm                                  │
  │    Std Dev:      {baseline_results['std_error']:>7.1f} nm                                  │
  │    N samples:    {baseline_results['n_samples']:>7}                                     │
  │                                                                 │
  │  SHIPS-ENHANCED (Track + Atmospheric)                           │
  │    Mean Error:   {enhanced_results['mean_error']:>7.1f} nm                                  │
  │    Median Error: {enhanced_results['median_error']:>7.1f} nm                                  │
  │    Std Dev:      {enhanced_results['std_error']:>7.1f} nm                                  │
  │    N samples:    {enhanced_results['n_samples']:>7}                                     │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
""")

# Calculate improvement
improvement = baseline_results['mean_error'] - enhanced_results['mean_error']
pct_improvement = 100 * improvement / baseline_results['mean_error']

# Statistical significance test
t_stat, p_value = stats.ttest_ind(baseline_results['errors'], enhanced_results['errors'])

print(f"""
  IMPROVEMENT ANALYSIS:
  =====================
  Absolute improvement: {improvement:+.1f} nm
  Relative improvement: {pct_improvement:+.1f}%

  Statistical significance (t-test):
    t-statistic: {t_stat:.2f}
    p-value:     {p_value:.6f}
    Significant? {'YES (p < 0.05)' if p_value < 0.05 else 'NO'}
""")

# Compare to NHC
NHC_24H = 47  # nm

print(f"""
  COMPARISON TO NHC OFFICIAL:
  ===========================
  NHC Official (2019-2023 avg): ~{NHC_24H} nm

  Our Baseline:       {baseline_results['mean_error']:.1f} nm ({baseline_results['mean_error']/NHC_24H:.2f}x NHC)
  Our SHIPS-Enhanced: {enhanced_results['mean_error']:.1f} nm ({enhanced_results['mean_error']/NHC_24H:.2f}x NHC)
""")

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================

print("\n" + "=" * 80)
print("  FEATURE IMPORTANCE (SHIPS-Enhanced Model)")
print("=" * 80)

# Retrain on full data to get feature importance
scaler = StandardScaler()
X_full = scaler.fit_transform(enhanced_df[ships_feat_valid].values)
y_lat_full = enhanced_df[TARGET_LAT]
y_lon_full = enhanced_df[TARGET_LON]

model_lat_full = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lat_full.fit(X_full, y_lat_full)

model_lon_full = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model_lon_full.fit(X_full, y_lon_full)

# Average importance across lat and lon models
importance = (model_lat_full.feature_importances_ + model_lon_full.feature_importances_) / 2
importance_df = pd.DataFrame({
    'feature': ships_feat_valid,
    'importance': importance
}).sort_values('importance', ascending=False)

print("\n  Top 10 Features for Track Prediction:")
print(f"  {'Rank':<6} {'Feature':<15} {'Importance':>12}")
print("  " + "-" * 35)
for i, row in importance_df.head(10).iterrows():
    rank = importance_df.index.get_loc(i) + 1
    print(f"  {rank:<6} {row['feature']:<15} {row['importance']:>12.4f}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("  SUMMARY")
print("=" * 80)

print(f"""
  KEY FINDINGS:
  =============

  1. SHIPS atmospheric data {'IMPROVES' if improvement > 0 else 'DOES NOT IMPROVE'} track forecasts
     - Improvement: {improvement:+.1f} nm ({pct_improvement:+.1f}%)
     - Statistically significant: {'YES' if p_value < 0.05 else 'NO'}

  2. Most important atmospheric predictors:
""")
for i, row in importance_df.head(5).iterrows():
    rank = importance_df.index.get_loc(i) + 1
    var = row['feature'].replace('_t0', '')
    print(f"     {rank}. {var}: importance = {row['importance']:.4f}")

print(f"""
  3. Comparison to operational models:
     - NHC Official: ~47 nm at 24h
     - Our Enhanced: {enhanced_results['mean_error']:.1f} nm
     - Ratio: {enhanced_results['mean_error']/47:.2f}x

  CONCLUSION:
  ===========
  {'The SHIPS atmospheric data significantly improves our track forecasts!' if improvement > 10 and p_value < 0.05 else 'Adding atmospheric data provides modest improvement, but we still lag operational models that use full 3D atmospheric fields.'}
""")

print("=" * 80)
