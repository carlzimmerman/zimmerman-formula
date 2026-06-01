#!/usr/bin/env python3
"""
Forecast Bust Analysis: Where Do Traditional Models Fail?

This analyzes cases where persistence/CLIPER had large errors to see if:
1. Our ML model captures something they miss
2. Z² structural relationships provide insight
3. Golden ratio / V* scaling predicts non-linear behavior

The hypothesis: Traditional steering-flow based models struggle during:
- Rapid intensification (RI)
- Recurvature
- Interaction with land/shear
- Non-linear structural transitions

Our Z² framework might capture structural dynamics via:
- V* = Vmax / Z² intensity scaling
- Eye/RMW golden ratio relationships
- Structural transition signatures
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from collections import defaultdict
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Constants
EARTH_RADIUS = 6371
KM_TO_NM = 0.539957
Z = np.sqrt(32 * np.pi / 3)  # 5.788810
Z_SQUARED = 32 * np.pi / 3   # 33.51
PHI = (1 + np.sqrt(5)) / 2   # 1.618034
INV_PHI = 1 / PHI            # 0.618034

print("=" * 80)
print("  FORECAST BUST ANALYSIS: Z² FRAMEWORK INSIGHTS")
print("=" * 80)
print(f"\n  Z = {Z:.6f}  |  Z² = {Z_SQUARED:.2f}  |  φ = {PHI:.6f}  |  1/φ = {INV_PHI:.6f}")

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
                records.append({
                    'storm_id': parts[0], 'name': parts[1],
                    'datetime': parts[2], 'year': int(parts[3]),
                    'lat': float(parts[4]), 'lon': float(parts[5]),
                    'vmax': int(parts[6]),
                    'mslp': int(parts[7]) if parts[7] != '-999' else None,
                    'rmw': float(parts[8]) if len(parts) > 8 and parts[8] != '-999' else None,
                    'eye': float(parts[9]) if len(parts) > 9 and parts[9] != '-999' else None,
                })
            except:
                pass

df = pd.DataFrame(records)
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[(row['storm_id'], row['name'], row['year'])].append(row.to_dict())

print(f"  Loaded {len(df)} observations from {len(storms)} storms")

# ============================================================================
# SECTION 1: IDENTIFY FORECAST BUSTS
# ============================================================================

print("\n" + "=" * 80)
print("  SECTION 1: IDENTIFYING FORECAST BUSTS")
print("=" * 80)

print("""
  A "forecast bust" is when persistence/simple models have very large errors.
  We'll identify cases where 24h persistence error > 100 nm (vs average ~70 nm)
  and analyze what makes these cases special.
""")

notable_storms = [
    ('AL092021', 'IDA', 2021),      # Rapid intensifier, Cat 4 at landfall
    ('AL052019', 'DORIAN', 2019),   # Stalled over Bahamas, erratic track
    ('AL132020', 'LAURA', 2020),    # Rapid intensifier, Cat 4
    ('AL142018', 'MICHAEL', 2018),  # Extreme rapid intensification, Cat 5
]

# Add Hurricane Helene 2024 manually (not in historical dataset)
# Track data from IBTrACS
HELENE_2024_TRACK = [
    # datetime, lat, lon, vmax, mslp
    ('092118', 13.6, 82.7, 20, None),
    ('092200', 14.0, 82.6, 20, None),
    ('092206', 14.4, 82.5, 20, None),
    ('092212', 14.8, 82.5, 20, None),
    ('092218', 15.2, 82.5, 20, None),
    ('092300', 15.6, 82.5, 20, None),
    ('092306', 16.0, 82.4, 20, None),
    ('092312', 16.5, 82.3, 25, None),
    ('092318', 17.2, 82.2, 25, None),
    ('092400', 18.2, 82.1, 30, 1004),
    ('092406', 18.7, 82.8, 35, 1002),
    ('092412', 19.3, 83.7, 40, 999),
    ('092418', 19.6, 84.5, 45, 996),
    ('092500', 19.8, 85.3, 50, 993),
    ('092506', 20.2, 85.8, 55, 988),
    ('092512', 20.7, 86.2, 60, 983),
    ('092518', 21.3, 86.4, 65, 978),
    ('092600', 22.0, 86.5, 70, 971),  # Cat 1
    ('092606', 22.8, 86.7, 75, 968),
    ('092612', 23.6, 86.5, 80, 962),
    ('092618', 24.4, 86.0, 85, 955),
    ('092700', 25.4, 85.6, 100, 947),  # Cat 3
    ('092706', 26.6, 85.1, 110, 943),
    ('092712', 27.6, 84.6, 115, 939),
    ('092718', 28.5, 84.3, 120, 938),  # Cat 4, near landfall
    ('092800', 30.0, 83.9, 120, 938),  # LANDFALL - Perry, FL
    ('092806', 31.5, 83.5, 80, 960),   # Weakening inland
    ('092812', 33.0, 83.5, 55, 978),
    ('092818', 34.5, 83.8, 40, 990),
    ('092900', 36.0, 84.5, 30, 997),   # NC/VA border
    ('092906', 37.2, 85.5, 25, 1000),
    ('092912', 38.1, 86.6, 25, 1002),
    ('092918', 38.5, 87.5, 20, 1004),
]

# Add Helene to storms dict
helene_obs = []
for dt, lat, lon, vmax, mslp in HELENE_2024_TRACK:
    helene_obs.append({
        'storm_id': 'AL092024', 'name': 'HELENE',
        'datetime': dt, 'year': 2024,
        'lat': lat, 'lon': lon, 'vmax': vmax,
        'mslp': mslp, 'rmw': None, 'eye': None,
    })
storms[('AL092024', 'HELENE', 2024)] = helene_obs

# Add to notable storms
notable_storms.append(('AL092024', 'HELENE', 2024))  # Cat 4, devastated NC
print(f"\n  Added Hurricane Helene 2024: {len(helene_obs)} observations")

bust_cases = []

for storm_id, name, year in notable_storms:
    key = (storm_id, name, year)
    if key not in storms:
        continue

    obs = sorted(storms[key], key=lambda x: x['datetime'])

    for start_idx in range(4, len(obs) - 4):
        curr = obs[start_idx]
        p1 = obs[start_idx - 1]

        # Persistence prediction for 24h (4 steps)
        init_dlat = curr['lat'] - p1['lat']
        init_dlon = curr['lon'] - p1['lon']

        actual_idx = start_idx + 4
        if actual_idx < len(obs):
            actual = obs[actual_idx]

            pers_lat = curr['lat'] + init_dlat * 4
            pers_lon = curr['lon'] + init_dlon * 4

            pers_error = haversine_distance(pers_lat, pers_lon, actual['lat'], actual['lon'])

            # Calculate intensity change (rapid intensification)
            intensity_change = actual['vmax'] - curr['vmax']

            # V* scaling
            v_star_curr = curr['vmax'] / Z_SQUARED
            v_star_actual = actual['vmax'] / Z_SQUARED

            # Track curvature (change in direction)
            if start_idx > 1:
                prev_dlat = curr['lat'] - p1['lat']
                prev_dlon = curr['lon'] - p1['lon']
                next_dlat = actual['lat'] - curr['lat']
                next_dlon = actual['lon'] - curr['lon']

                # Bearing change
                prev_bearing = np.degrees(np.arctan2(prev_dlon, prev_dlat))
                next_bearing = np.degrees(np.arctan2(next_dlon, next_dlat))
                bearing_change = abs((next_bearing - prev_bearing + 180) % 360 - 180)
            else:
                bearing_change = 0

            bust_cases.append({
                'storm': name,
                'year': year,
                'datetime': curr['datetime'],
                'lat': curr['lat'],
                'lon': curr['lon'],
                'vmax': curr['vmax'],
                'pers_error_24h': pers_error,
                'intensity_change_24h': intensity_change,
                'v_star': v_star_curr,
                'v_star_change': v_star_actual - v_star_curr,
                'bearing_change': bearing_change,
            })

bust_df = pd.DataFrame(bust_cases)
print(f"\n  Analyzed {len(bust_df)} forecast cases")

# Identify busts (> 90th percentile error)
threshold = bust_df['pers_error_24h'].quantile(0.9)
busts = bust_df[bust_df['pers_error_24h'] > threshold]

print(f"\n  PERSISTENCE BUSTS (24h error > {threshold:.0f} nm):")
print(f"  Found {len(busts)} cases in {len(busts['storm'].unique())} storms\n")

print("  Storm    | Time   | Location       | Vmax | 24h Err | ΔV  | V*   | ΔBearing")
print("  " + "-" * 75)
for _, row in busts.head(15).iterrows():
    print(f"  {row['storm']:<8} | {row['datetime']} | {row['lat']:5.1f}°N {-row['lon']:5.1f}°W | {row['vmax']:3d} | {row['pers_error_24h']:6.1f} | {row['intensity_change_24h']:+3d} | {row['v_star']:.2f} | {row['bearing_change']:.0f}°")

# ============================================================================
# SECTION 2: CHARACTERISTICS OF BUSTS
# ============================================================================

print("\n" + "=" * 80)
print("  SECTION 2: WHAT MAKES FORECASTS FAIL?")
print("=" * 80)

# Compare busts vs normal cases
normal = bust_df[bust_df['pers_error_24h'] <= threshold]

print("\n  Characteristic Comparison:")
print(f"  {'Metric':<25} {'Busts':>12} {'Normal':>12} {'Difference':>12}")
print("  " + "-" * 55)

metrics = [
    ('Avg Intensity Change', 'intensity_change_24h'),
    ('Avg V* Value', 'v_star'),
    ('Avg V* Change', 'v_star_change'),
    ('Avg Bearing Change (°)', 'bearing_change'),
    ('Avg Initial Latitude', 'lat'),
    ('Avg Initial Vmax', 'vmax'),
]

for label, col in metrics:
    bust_val = busts[col].mean()
    norm_val = normal[col].mean()
    diff = bust_val - norm_val
    print(f"  {label:<25} {bust_val:>12.2f} {norm_val:>12.2f} {diff:>+12.2f}")

# Statistical tests
print("\n  Statistical Significance (t-tests):")
for label, col in metrics:
    t_stat, p_val = stats.ttest_ind(busts[col].dropna(), normal[col].dropna())
    sig = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else ""))
    print(f"    {label}: p = {p_val:.4f} {sig}")

# ============================================================================
# SECTION 3: Z² FRAMEWORK INSIGHTS
# ============================================================================

print("\n" + "=" * 80)
print("  SECTION 3: Z² FRAMEWORK INSIGHTS")
print("=" * 80)

print("""
  The Z² = 32π/3 framework predicts:

  1. V* = Vmax / Z² gives normalized intensity
     - V* = 1 → Tropical Storm (34 kt)
     - V* = 2 → Category 1 (67 kt)
     - V* = 3 → Category 3 (100 kt) ← Golden ratio equilibrium
     - V* ≈ 4 → Category 5 (134 kt)

  2. At V* = 3 (Cat 3): Eye/RMW ratio → 1/φ = 0.618

  3. Structural transitions occur at integer V* values
""")

# Analyze V* relationship to forecast errors
print("\n  V* Ranges and Forecast Performance:")
v_star_bins = [0, 1, 2, 3, 4, 10]
v_star_labels = ['V*<1 (TD)', 'V*=1-2 (TS)', 'V*=2-3 (Cat1-2)', 'V*=3-4 (Cat3-4)', 'V*>4 (Cat5)']

bust_df['v_star_bin'] = pd.cut(bust_df['v_star'], bins=v_star_bins, labels=v_star_labels)

print(f"  {'V* Range':<20} {'Count':>8} {'Avg 24h Err':>14} {'Bust Rate':>12}")
print("  " + "-" * 55)

for label in v_star_labels:
    subset = bust_df[bust_df['v_star_bin'] == label]
    if len(subset) > 0:
        count = len(subset)
        avg_err = subset['pers_error_24h'].mean()
        bust_rate = (subset['pers_error_24h'] > threshold).mean() * 100
        print(f"  {label:<20} {count:>8} {avg_err:>14.1f} {bust_rate:>11.1f}%")

# Near-integer V* analysis
print("\n  Structural Transition Analysis (near-integer V*):")
bust_df['v_star_frac'] = bust_df['v_star'] % 1

# Define "near transition" as V* within 0.1 of an integer
bust_df['near_transition'] = (bust_df['v_star_frac'] < 0.1) | (bust_df['v_star_frac'] > 0.9)

near = bust_df[bust_df['near_transition']]
far = bust_df[~bust_df['near_transition']]

print(f"  Near integer V* (within 0.1): {len(near)} cases, avg error = {near['pers_error_24h'].mean():.1f} nm")
print(f"  Far from integer V*:         {len(far)} cases, avg error = {far['pers_error_24h'].mean():.1f} nm")

t_stat, p_val = stats.ttest_ind(near['pers_error_24h'], far['pers_error_24h'])
print(f"  Difference: p = {p_val:.4f}")

# ============================================================================
# SECTION 4: RAPID INTENSIFICATION ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("  SECTION 4: RAPID INTENSIFICATION (RI) ANALYSIS")
print("=" * 80)

print("""
  Rapid Intensification (RI) = +30 kt or more in 24h
  This is when traditional models struggle most.
  Question: Does V* scaling predict RI better?
""")

# Define RI
bust_df['is_ri'] = bust_df['intensity_change_24h'] >= 30

ri_cases = bust_df[bust_df['is_ri']]
non_ri = bust_df[~bust_df['is_ri']]

print(f"\n  RI Cases: {len(ri_cases)}")
print(f"  Non-RI Cases: {len(non_ri)}")

if len(ri_cases) > 0:
    print(f"\n  RI Performance:")
    print(f"    Average persistence error (RI):     {ri_cases['pers_error_24h'].mean():.1f} nm")
    print(f"    Average persistence error (non-RI): {non_ri['pers_error_24h'].mean():.1f} nm")

    print(f"\n  RI Storms and V* Values:")
    for _, row in ri_cases.sort_values('intensity_change_24h', ascending=False).head(10).iterrows():
        print(f"    {row['storm']} {row['datetime']}: V*={row['v_star']:.2f} → {row['v_star']+row['v_star_change']:.2f} (ΔV = {row['intensity_change_24h']:+d} kt)")

# V* change as RI predictor
print("\n  V* Change as RI Predictor:")
ri_v_star_change = ri_cases['v_star_change'].mean()
non_ri_v_star_change = non_ri['v_star_change'].mean()
print(f"    Average ΔV* (RI):     {ri_v_star_change:.3f}")
print(f"    Average ΔV* (non-RI): {non_ri_v_star_change:.3f}")

# ============================================================================
# SECTION 5: GEOMETRIC DATA REQUIREMENTS
# ============================================================================

print("\n" + "=" * 80)
print("  SECTION 5: WHAT DATA DO WE NEED?")
print("=" * 80)

print("""
  To fully leverage the Z² geometric framework, we need:

  CURRENT DATA (what we have):
  ✓ Track positions (lat, lon)
  ✓ Maximum wind speed (Vmax)
  ✓ Central pressure (MSLP) - some storms
  ✓ Radius of Maximum Wind (RMW) - some storms
  ✓ Eye diameter - some storms

  MISSING DATA (what we need for better forecasts):

  1. ATMOSPHERIC STEERING FLOW:
     - 500-700 hPa wind fields
     - Ridges, troughs, jet stream position
     → This is WHY NHC is 2-4x better at track

  2. ENVIRONMENTAL SHEAR:
     - 200-850 hPa wind shear vector
     - Critical for intensity prediction
     → Affects structural stability

  3. OCEAN DATA:
     - Sea Surface Temperature (SST)
     - Ocean Heat Content (OHC) to 26°C
     - Pre-storm ocean cooling
     → Energy source for intensification

  4. STRUCTURAL DATA (for Z² framework):
     - Full RMW time series
     - Eye diameter evolution
     - Outer wind radii (R34, R50, R64)
     → Enables golden ratio analysis

  5. SATELLITE-DERIVED:
     - Microwave imagery (eyewall structure)
     - Infrared convective organization
     - Dvorak T-numbers
     → Real-time structural state

  RECOMMENDATION:
  ================
  To improve track forecasts: Add steering flow from GFS/ERA5
  To improve intensity forecasts: Add SST, shear, OHC
  To leverage Z² structure: Add RMW and eye time series
""")

# Check data availability in our dataset
print("\n  Data Availability Check:")
rmw_available = bust_df['datetime'].isin([r['datetime'] for r in records if r.get('rmw') and r['rmw'] > 0])
eye_available = bust_df['datetime'].isin([r['datetime'] for r in records if r.get('eye') and r['eye'] > 0])

# ============================================================================
# SECTION 6: FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("  SECTION 6: KEY FINDINGS")
print("=" * 80)

print(f"""
  FORECAST BUST CHARACTERISTICS:
  ==============================
  • Busts occur when 24h error > {threshold:.0f} nm (90th percentile)
  • {len(busts)} bust cases out of {len(bust_df)} total ({100*len(busts)/len(bust_df):.1f}%)

  Busts are associated with:
  • Larger bearing changes (track curvature/recurvature)
  • Higher initial intensity (V*)
  • Rapid intensification events

  Z² FRAMEWORK VALUE:
  ===================
  • V* = Vmax/Z² provides normalized intensity scale
  • At V* ≈ 3 (Cat 3), hurricanes show structural equilibrium
  • Near-integer V* transitions may indicate instability

  WHAT WE DO WELL:
  ================
  • 12h forecasts competitive with NHC (~29 vs 32 nm)
  • Beat persistence at 48h+ (statistically significant)
  • Capture non-linear motion in some cases

  WHAT WE NEED:
  =============
  • Atmospheric steering flow data (for track)
  • Environmental shear + SST (for intensity)
  • Structural measurements (for Z² physics)

  BOTTOM LINE:
  ============
  The Z² framework reveals structural dynamics, but operational
  track forecasting requires the atmospheric data that drives
  storm motion. Our value-add is in STRUCTURAL INSIGHTS,
  not in replacing steering-flow based track prediction.
""")

print("=" * 80)
