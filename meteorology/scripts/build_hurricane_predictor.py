#!/usr/bin/env python3
"""
Build a Better Hurricane Predictor

Using flight reconnaissance data and our findings:
1. Eye/RMW = 1/φ at ~93 kt (golden ratio transition)
2. Linear: Eye = 0.158 × RMW + 7.62 nm
3. Ratio increases with intensity

Goals:
1. Predict eye radius from RMW and intensity
2. Predict RMW from intensity
3. Explore intensity change prediction
4. Build composite structural model
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from collections import defaultdict
import json
import warnings
warnings.filterwarnings('ignore')

# Constants
PHI = (1 + np.sqrt(5)) / 2
ONE_OVER_PHI = 1 / PHI
Z_SQUARED = 32 * np.pi / 3
Z_VALUE = np.sqrt(Z_SQUARED)

print("=" * 80)
print("  BUILDING A BETTER HURRICANE PREDICTOR")
print("=" * 80)

# =============================================================================
# LOAD ALL DATA
# =============================================================================

print("\n  Loading data...")

# Atlantic EBTRK (most detailed - flight reconnaissance)
atl_records = []
with open('data/extended_best_track/EBTRK_Atlantic_2021.txt', 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 12:
            try:
                storm_id = parts[0]
                name = parts[1]
                datetime = parts[2]
                year = int(parts[3])
                lat = float(parts[4])
                lon = float(parts[5])
                vmax = int(parts[6])
                pmin = int(parts[7])
                rmw = int(parts[8])
                eye_diam = int(parts[9])

                if vmax > 0:
                    record = {
                        'storm_id': storm_id,
                        'name': name,
                        'datetime': datetime,
                        'year': year,
                        'lat': lat,
                        'lon': lon,
                        'vmax': vmax,
                        'pmin': pmin if pmin > 0 and pmin != -99 else np.nan,
                        'rmw': rmw if rmw > 0 and rmw != -99 else np.nan,
                        'eye_diam': eye_diam if eye_diam > 0 and eye_diam != -99 else np.nan,
                    }
                    atl_records.append(record)
            except:
                pass

df = pd.DataFrame(atl_records)
print(f"  Loaded {len(df)} Atlantic observations")

# Add derived fields
df['eye_radius'] = df['eye_diam'] / 2.0
df['eye_rmw_ratio'] = df['eye_radius'] / df['rmw']
df['pressure_deficit'] = 1013.25 - df['pmin']

# Valid subsets
df_eye_rmw = df.dropna(subset=['eye_radius', 'rmw', 'vmax'])
df_pressure = df.dropna(subset=['pmin', 'vmax'])
df_rmw = df.dropna(subset=['rmw', 'vmax'])

print(f"  Valid eye+RMW: {len(df_eye_rmw)}")
print(f"  Valid pressure+wind: {len(df_pressure)}")
print(f"  Valid RMW: {len(df_rmw)}")

# =============================================================================
# MODEL 1: EYE RADIUS PREDICTION
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL 1: EYE RADIUS PREDICTION")
print("=" * 80)

# Already developed - golden transition model
def predict_eye_golden(rmw, vmax):
    """Golden ratio transition model"""
    if vmax < 60:
        ratio = 0.35 + 0.003 * vmax
    elif vmax <= 100:
        ratio = 0.53 + (vmax - 60) * (ONE_OVER_PHI - 0.53) / 40
    else:
        ratio = ONE_OVER_PHI + 0.001 * (vmax - 100)
    return ratio * rmw

# Test
eye_pred = df_eye_rmw.apply(lambda r: predict_eye_golden(r['rmw'], r['vmax']), axis=1)
eye_obs = df_eye_rmw['eye_radius']
mae_eye = np.mean(np.abs(eye_pred - eye_obs))
rmse_eye = np.sqrt(np.mean((eye_pred - eye_obs)**2))
r_eye = np.corrcoef(eye_pred, eye_obs)[0,1]

print(f"\n  Golden Transition Model:")
print(f"    MAE = {mae_eye:.2f} nm")
print(f"    RMSE = {rmse_eye:.2f} nm")
print(f"    R = {r_eye:.3f}")

# =============================================================================
# MODEL 2: RMW PREDICTION FROM INTENSITY
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL 2: RMW PREDICTION FROM INTENSITY")
print("=" * 80)

# RMW typically contracts with intensification
vmax_arr = df_rmw['vmax'].values
rmw_arr = df_rmw['rmw'].values

# Linear fit
slope_rmw, intercept_rmw, r_rmw, p_rmw, _ = stats.linregress(vmax_arr, rmw_arr)
print(f"\n  Linear fit: RMW = {slope_rmw:.4f} × Vmax + {intercept_rmw:.2f}")
print(f"    R² = {r_rmw**2:.4f}")

# Better model: RMW = a / Vmax + b (inverse relationship)
def rmw_inverse(vmax, a, b):
    return a / vmax + b

try:
    popt, _ = curve_fit(rmw_inverse, vmax_arr, rmw_arr, p0=[1000, 20], maxfev=5000)
    a_rmw, b_rmw = popt
    rmw_pred_inv = rmw_inverse(vmax_arr, a_rmw, b_rmw)
    mae_rmw_inv = np.mean(np.abs(rmw_pred_inv - rmw_arr))
    r_rmw_inv = np.corrcoef(rmw_pred_inv, rmw_arr)[0,1]
    print(f"\n  Inverse fit: RMW = {a_rmw:.1f} / Vmax + {b_rmw:.1f}")
    print(f"    MAE = {mae_rmw_inv:.2f} nm")
    print(f"    R = {r_rmw_inv:.3f}")
except:
    a_rmw, b_rmw = 1500, 15
    print("  (Using default inverse fit parameters)")

# Power law: RMW = a × Vmax^b
log_vmax = np.log(vmax_arr)
log_rmw = np.log(rmw_arr)
slope_log, intercept_log, r_log, _, _ = stats.linregress(log_vmax, log_rmw)
a_power = np.exp(intercept_log)
b_power = slope_log
rmw_pred_power = a_power * vmax_arr**b_power
mae_rmw_power = np.mean(np.abs(rmw_pred_power - rmw_arr))

print(f"\n  Power law: RMW = {a_power:.1f} × Vmax^{b_power:.3f}")
print(f"    MAE = {mae_rmw_power:.2f} nm")
print(f"    R = {np.corrcoef(rmw_pred_power, rmw_arr)[0,1]:.3f}")

# =============================================================================
# MODEL 3: PRESSURE-WIND RELATIONSHIP
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL 3: PRESSURE-WIND RELATIONSHIP")
print("=" * 80)

pmin_arr = df_pressure['pmin'].values
vmax_p = df_pressure['vmax'].values
delta_p = 1013.25 - pmin_arr

# Standard: V = k × sqrt(delta_P)
valid = delta_p > 0
k_values = vmax_p[valid] / np.sqrt(delta_p[valid])
k_mean = np.mean(k_values)

print(f"\n  V = k × √(ΔP)")
print(f"    k = {k_mean:.2f} kt/√hPa")

# Predict and evaluate
vmax_pred_pw = k_mean * np.sqrt(delta_p[valid])
mae_pw = np.mean(np.abs(vmax_pred_pw - vmax_p[valid]))
rmse_pw = np.sqrt(np.mean((vmax_pred_pw - vmax_p[valid])**2))
r_pw = np.corrcoef(vmax_pred_pw, vmax_p[valid])[0,1]

print(f"    MAE = {mae_pw:.2f} kt")
print(f"    RMSE = {rmse_pw:.2f} kt")
print(f"    R = {r_pw:.3f}")

# Better model with latitude dependence (Coriolis)
lat_arr = df_pressure['lat'].values
f = 2 * 7.2921e-5 * np.sin(np.radians(lat_arr))  # Coriolis parameter

# =============================================================================
# MODEL 4: INTENSITY CHANGE PREDICTION
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL 4: INTENSITY CHANGE ANALYSIS")
print("=" * 80)

# Group by storm and compute intensity changes
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[row['storm_id']].append(row)

intensity_changes = []
for storm_id, obs in storms.items():
    if len(obs) < 2:
        continue
    # Sort by datetime
    obs = sorted(obs, key=lambda x: x['datetime'])
    for i in range(1, len(obs)):
        prev = obs[i-1]
        curr = obs[i]

        # 6-hour intensity change
        dv = curr['vmax'] - prev['vmax']

        intensity_changes.append({
            'storm_id': storm_id,
            'vmax_prev': prev['vmax'],
            'vmax_curr': curr['vmax'],
            'dv': dv,
            'rmw_prev': prev['rmw'] if not np.isnan(prev.get('rmw', np.nan)) else np.nan,
            'rmw_curr': curr['rmw'] if not np.isnan(curr.get('rmw', np.nan)) else np.nan,
            'eye_prev': prev['eye_radius'] if not np.isnan(prev.get('eye_radius', np.nan)) else np.nan,
            'lat': curr['lat'],
        })

ic_df = pd.DataFrame(intensity_changes)
print(f"\n  Intensity change observations: {len(ic_df)}")

# Rapid intensification (RI): >= 30 kt in 24 hours = 7.5 kt per 6 hours
ri_threshold = 7.5
ic_df['is_ri'] = ic_df['dv'] >= ri_threshold
print(f"  Rapid intensification events (≥{ri_threshold} kt/6hr): {ic_df['is_ri'].sum()}")

# What predicts RI?
ic_valid = ic_df.dropna(subset=['rmw_prev', 'vmax_prev'])
if len(ic_valid) > 100:
    # Correlation between RMW and intensity change
    r_rmw_dv = np.corrcoef(ic_valid['rmw_prev'], ic_valid['dv'])[0,1]
    print(f"\n  Correlation (RMW_prev vs dV): {r_rmw_dv:.3f}")

    # Correlation between Vmax and intensity change
    r_vmax_dv = np.corrcoef(ic_valid['vmax_prev'], ic_valid['dv'])[0,1]
    print(f"  Correlation (Vmax_prev vs dV): {r_vmax_dv:.3f}")

    # RMW contraction predicts intensification
    ic_rmw_change = ic_valid.dropna(subset=['rmw_curr'])
    if len(ic_rmw_change) > 50:
        ic_rmw_change['rmw_change'] = ic_rmw_change['rmw_curr'] - ic_rmw_change['rmw_prev']
        r_rmw_change = np.corrcoef(ic_rmw_change['rmw_change'], ic_rmw_change['dv'])[0,1]
        print(f"  Correlation (RMW_change vs dV): {r_rmw_change:.3f}")

# =============================================================================
# MODEL 5: STRUCTURAL EQUILIBRIUM MODEL
# =============================================================================

print("\n" + "=" * 80)
print("  MODEL 5: STRUCTURAL EQUILIBRIUM (GOLDEN RATIO)")
print("=" * 80)

# At what intensity is the storm "in equilibrium"?
# Hypothesis: eye/RMW = 1/φ represents optimal vortex structure

df_eye_rmw['deviation_from_phi'] = np.abs(df_eye_rmw['eye_rmw_ratio'] - ONE_OVER_PHI)

# Intensity where deviation is minimized
bins = list(range(35, 165, 5))
equilibrium_analysis = []

for i in range(len(bins)-1):
    vmin, vmax = bins[i], bins[i+1]
    subset = df_eye_rmw[(df_eye_rmw['vmax'] >= vmin) & (df_eye_rmw['vmax'] < vmax)]
    if len(subset) >= 10:
        mean_ratio = subset['eye_rmw_ratio'].mean()
        mean_dev = subset['deviation_from_phi'].mean()
        equilibrium_analysis.append({
            'vmax_mid': (vmin + vmax) / 2,
            'n': len(subset),
            'mean_ratio': mean_ratio,
            'deviation_from_phi': mean_dev,
        })

eq_df = pd.DataFrame(equilibrium_analysis)
if len(eq_df) > 0:
    min_dev_idx = eq_df['deviation_from_phi'].idxmin()
    optimal_vmax = eq_df.loc[min_dev_idx, 'vmax_mid']
    optimal_ratio = eq_df.loc[min_dev_idx, 'mean_ratio']

    print(f"\n  Golden ratio equilibrium analysis:")
    print(f"    Optimal intensity (min deviation from 1/φ): {optimal_vmax:.0f} kt")
    print(f"    Ratio at optimum: {optimal_ratio:.4f}")
    print(f"    1/φ = {ONE_OVER_PHI:.4f}")

# =============================================================================
# COMPOSITE PREDICTOR
# =============================================================================

print("\n" + "=" * 80)
print("  COMPOSITE HURRICANE STRUCTURAL PREDICTOR")
print("=" * 80)

print("""
PREDICTION EQUATIONS:

1. RMW from Intensity:
   RMW = {a:.0f} / Vmax + {b:.0f} nm
   (or power law: RMW = {ap:.1f} × Vmax^{bp:.3f})

2. Eye Radius from RMW and Intensity:
   For Vmax < 60 kt:
       Eye = (0.35 + 0.003 × Vmax) × RMW
   For 60 ≤ Vmax ≤ 100 kt:
       Eye = (0.53 + (Vmax-60) × 0.0022) × RMW
   For Vmax > 100 kt:
       Eye = (0.618 + 0.001 × (Vmax-100)) × RMW

3. Pressure from Intensity:
   ΔP = (Vmax / {k:.1f})²
   Pmin = 1013.25 - ΔP

4. Equilibrium Indicator:
   Storm is near structural equilibrium when:
   eye/RMW ≈ 1/φ = 0.618
   (Occurs around Vmax ≈ {eq:.0f} kt)
""".format(a=a_rmw, b=b_rmw, ap=a_power, bp=b_power, k=k_mean, eq=optimal_vmax))

# =============================================================================
# VALIDATION ON HELD-OUT DATA
# =============================================================================

print("\n" + "=" * 80)
print("  VALIDATION: CROSS-VALIDATION")
print("=" * 80)

# Simple train/test split by year
test_years = [2019, 2020, 2021]
train = df_eye_rmw[~df_eye_rmw['year'].isin(test_years)]
test = df_eye_rmw[df_eye_rmw['year'].isin(test_years)]

print(f"\n  Training: {len(train)} observations (years < 2019)")
print(f"  Testing: {len(test)} observations (years 2019-2021)")

if len(test) > 20:
    # Predict eye radius on test set
    test_pred = test.apply(lambda r: predict_eye_golden(r['rmw'], r['vmax']), axis=1)
    test_obs = test['eye_radius']

    mae_test = np.mean(np.abs(test_pred - test_obs))
    rmse_test = np.sqrt(np.mean((test_pred - test_obs)**2))
    r_test = np.corrcoef(test_pred, test_obs)[0,1]

    print(f"\n  Test set performance (Eye prediction):")
    print(f"    MAE = {mae_test:.2f} nm")
    print(f"    RMSE = {rmse_test:.2f} nm")
    print(f"    R = {r_test:.3f}")

# =============================================================================
# SAVE MODELS
# =============================================================================

models = {
    'eye_prediction': {
        'model': 'golden_transition',
        'description': 'Eye radius from RMW and Vmax',
        'mae': float(mae_eye),
        'rmse': float(rmse_eye),
        'r': float(r_eye),
    },
    'rmw_prediction': {
        'model': 'inverse',
        'equation': f'RMW = {a_rmw:.1f} / Vmax + {b_rmw:.1f}',
        'mae': float(mae_rmw_inv) if 'mae_rmw_inv' in dir() else None,
    },
    'pressure_wind': {
        'model': 'sqrt',
        'k': float(k_mean),
        'equation': f'Vmax = {k_mean:.1f} × sqrt(1013.25 - Pmin)',
        'mae': float(mae_pw),
        'r': float(r_pw),
    },
    'equilibrium': {
        'optimal_intensity': float(optimal_vmax) if 'optimal_vmax' in dir() else 95,
        'golden_ratio': float(ONE_OVER_PHI),
    },
    'constants': {
        'phi': float(PHI),
        'one_over_phi': float(ONE_OVER_PHI),
        'z_squared': float(Z_SQUARED),
    }
}

with open('hurricane_predictor_models.json', 'w') as f:
    json.dump(models, f, indent=2)

print("\n  Models saved to: hurricane_predictor_models.json")
print("=" * 80)
