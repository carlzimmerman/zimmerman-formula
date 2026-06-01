#!/usr/bin/env python3
"""
SHIPS Data Parser

Parses the SHIPS developmental dataset and extracts environmental predictors
for use in improved hurricane track and intensity forecasting.

Key predictors for steering/track:
- U200, V200: 200 hPa winds
- U850, V850: 850 hPa winds (via V850)
- SHRD: Deep layer shear (steering proxy)
- TLAT, TLON: Track latitude/longitude

Key predictors for intensity:
- SHRD: Vertical wind shear
- CSST: Sea surface temperature
- COHC: Ocean heat content
- VMPI: Maximum potential intensity
- RHLO, RHMD, RHHI: Relative humidity
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import os
import json

print("=" * 80)
print("  SHIPS DATA PARSER")
print("=" * 80)

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIPS_FILE = os.path.join(DATA_DIR, 'data/ships/lsdiaga_1982_2023_sat_ts_7day.txt')

# Key variables we want to extract
KEY_VARS = [
    'VMAX', 'MSLP', 'LAT', 'LON',     # Storm state
    'CSST', 'RSST', 'DSST',            # SST variables
    'CD20', 'CD26', 'COHC',            # Ocean heat content
    'SHRD', 'SHDC', 'SHRG',            # Vertical shear (deep, directional, generalized)
    'SHTD', 'SHRS', 'SHTS',            # More shear components
    'U200', 'V20C',                     # Upper level winds (steering)
    'V850', 'V500', 'V300',            # Mid/low level winds
    'VMPI', 'PENV',                     # Max potential intensity, environmental pressure
    'D200', 'DIVC',                     # Divergence
    'RHLO', 'RHMD', 'RHHI',            # Relative humidity
    'DTL', 'OAGE', 'NAGE',             # Distance to land, storm age
    'TLAT', 'TLON',                     # Track position
    'TWAC', 'TWXC',                     # Track motion
    'INCV', 'DELV',                     # Intensity change
]

# Time columns in the file
TIME_COLS = [-12, -6, 0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72,
             78, 84, 90, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168]

def parse_ships_file(filepath, max_storms=None):
    """Parse SHIPS predictor file and return structured data"""

    storms = []
    current_storm = None
    current_vars = {}

    print(f"\n  Parsing {filepath}...")

    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f):
            # Remove trailing whitespace and get the line type
            line = line.rstrip()
            if len(line) < 10:
                continue

            # Line type is at the end
            parts = line.split()
            if not parts:
                continue

            line_type = parts[-1].strip()

            # Header line starts a new storm
            if line_type == 'HEAD':
                # Save previous storm if exists
                if current_storm and current_vars:
                    current_storm['variables'] = current_vars
                    storms.append(current_storm)

                    if max_storms and len(storms) >= max_storms:
                        break

                # Parse header: "ALBE 820602 12   20   21.7   87.1 1005 AL011982"
                try:
                    name = parts[0]
                    date = parts[1]  # YYMMDD
                    hour = parts[2]   # HH
                    vmax_init = int(parts[3])
                    lat_init = float(parts[4])
                    lon_init = float(parts[5])
                    mslp_init = int(parts[6]) if parts[6] != '9999' else None
                    storm_id = parts[7] if len(parts) > 7 else f"{name}_{date}"

                    # Parse year from storm_id or date
                    if len(storm_id) >= 8:
                        year = int(storm_id[-4:])
                    else:
                        year = 1900 + int(date[:2]) if int(date[:2]) > 50 else 2000 + int(date[:2])

                    current_storm = {
                        'name': name,
                        'storm_id': storm_id,
                        'date': date,
                        'hour': hour,
                        'year': year,
                        'lat_init': lat_init,
                        'lon_init': lon_init,
                        'vmax_init': vmax_init,
                        'mslp_init': mslp_init,
                    }
                    current_vars = {}
                except Exception as e:
                    print(f"    Error parsing header at line {line_num}: {e}")
                    current_storm = None
                    current_vars = {}
                    continue

            elif line_type == 'TIME':
                # Skip time header line
                continue

            elif line_type == 'LAST':
                # End of storm record
                if current_storm and current_vars:
                    current_storm['variables'] = current_vars
                    storms.append(current_storm)

                    if max_storms and len(storms) >= max_storms:
                        break

                current_storm = None
                current_vars = {}

            elif current_storm is not None:
                # This is a variable line
                var_name = line_type.split()[0]  # Handle cases like "RSST    0"

                if var_name in KEY_VARS:
                    # Parse values (skip first column if it's a space)
                    try:
                        # Values are typically space-separated integers
                        values = []
                        raw_values = parts[:-1]  # Exclude the variable name

                        for v in raw_values:
                            try:
                                val = int(v) if '.' not in v else float(v)
                                values.append(val if val != 9999 else None)
                            except:
                                values.append(None)

                        # Pad or trim to match TIME_COLS length
                        while len(values) < len(TIME_COLS):
                            values.append(None)
                        values = values[:len(TIME_COLS)]

                        current_vars[var_name] = dict(zip(TIME_COLS, values))
                    except Exception as e:
                        pass  # Skip problematic lines

    # Don't forget the last storm
    if current_storm and current_vars:
        current_storm['variables'] = current_vars
        storms.append(current_storm)

    print(f"  Parsed {len(storms)} storm records")
    return storms

def extract_storm_features(storms):
    """Extract features for ML modeling from parsed storms"""

    records = []

    for storm in storms:
        name = storm['name']
        storm_id = storm['storm_id']
        year = storm['year']
        date = storm['date']
        hour = storm['hour']

        variables = storm.get('variables', {})

        # Get T=0 values for each variable
        t0_values = {}
        for var_name, time_values in variables.items():
            t0_val = time_values.get(0)
            if t0_val is not None:
                t0_values[var_name] = t0_val

        # Also get future values for targets
        for lead in [6, 12, 24, 48, 72]:
            record = {
                'storm_id': storm_id,
                'name': name,
                'year': year,
                'date': date,
                'hour': hour,
                'lead_time': lead,
            }

            # Add T=0 features
            for var, val in t0_values.items():
                record[f'{var}_t0'] = val

            # Add target values (at lead time)
            for var_name, time_values in variables.items():
                future_val = time_values.get(lead)
                if future_val is not None:
                    record[f'{var_name}_t{lead}'] = future_val

            # Calculate derived features
            if 'LAT_t0' in record and f'LAT_t{lead}' in record:
                record['dlat'] = record[f'LAT_t{lead}'] - record['LAT_t0']
            if 'LON_t0' in record and f'LON_t{lead}' in record:
                record['dlon'] = record[f'LON_t{lead}'] - record['LON_t0']
            if 'VMAX_t0' in record and f'VMAX_t{lead}' in record:
                record['dvmax'] = record[f'VMAX_t{lead}'] - record['VMAX_t0']

            records.append(record)

    return pd.DataFrame(records)

# Parse the data
storms = parse_ships_file(SHIPS_FILE, max_storms=None)

# Show sample
print(f"\n  Sample storm records:")
for storm in storms[:3]:
    print(f"    {storm['name']} ({storm['year']}): {storm['storm_id']}")
    print(f"      Init: {storm['lat_init']}°N, {storm['lon_init']}°W, {storm['vmax_init']} kt")
    print(f"      Variables: {list(storm.get('variables', {}).keys())[:10]}...")

# Extract features
print("\n  Extracting features for ML...")
df = extract_storm_features(storms)
print(f"  Created {len(df)} training samples")
print(f"  Columns: {len(df.columns)}")

# Show statistics
print("\n" + "=" * 80)
print("  DATA STATISTICS")
print("=" * 80)

print(f"\n  Years covered: {df['year'].min()} - {df['year'].max()}")
print(f"  Unique storms: {df['storm_id'].nunique()}")

# Key predictor statistics
print("\n  Key Predictor Statistics at T=0:")
key_stats = ['SHRD_t0', 'CSST_t0', 'COHC_t0', 'VMPI_t0', 'VMAX_t0']
for col in key_stats:
    if col in df.columns:
        valid = df[col].dropna()
        print(f"    {col}: mean={valid.mean():.1f}, std={valid.std():.1f}, n={len(valid)}")

# Save to CSV for ML
output_file = os.path.join(DATA_DIR, 'data/ships/ships_features.csv')
df.to_csv(output_file, index=False)
print(f"\n  Saved features to: {output_file}")

# Also save a summary JSON
summary = {
    'n_storms': df['storm_id'].nunique(),
    'n_records': len(df),
    'years': [int(df['year'].min()), int(df['year'].max())],
    'key_predictors': KEY_VARS,
    'lead_times': [6, 12, 24, 48, 72],
}
with open(os.path.join(DATA_DIR, 'data/ships/ships_summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print("\n" + "=" * 80)
print("  SHIPS DATA READY FOR ML INTEGRATION")
print("=" * 80)
