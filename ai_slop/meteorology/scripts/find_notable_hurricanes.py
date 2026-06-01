#!/usr/bin/env python3
"""
Find notable recent hurricanes in the EBTRK data for visualization.
"""

import pandas as pd
from collections import defaultdict

print("=" * 80)
print("  FINDING NOTABLE HURRICANES FOR VISUALIZATION")
print("=" * 80)

# Load data
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
                    })
            except:
                pass

df = pd.DataFrame(records)

# Group by storm and find stats
storms = defaultdict(list)
for _, row in df.iterrows():
    storms[(row['storm_id'], row['name'], row['year'])].append(row.to_dict())

print(f"\n  Total storms in dataset: {len(storms)}")

# Find major hurricanes (Cat 3+, 96+ kt)
print("\n" + "=" * 80)
print("  MAJOR HURRICANES (2018-2021)")
print("=" * 80)

major_hurricanes = []
for (storm_id, name, year), obs in storms.items():
    if year >= 2018:
        max_wind = max(o['vmax'] for o in obs)
        min_pres = min((o['pmin'] for o in obs if o['pmin']), default=None)
        n_obs = len(obs)

        # Get landfall info (lat > 24 and lon > -100 as rough US/Caribbean proxy)
        landfalls = [o for o in obs if o['lat'] > 24 and o['lon'] > -100]

        if max_wind >= 96:  # Cat 3+
            major_hurricanes.append({
                'storm_id': storm_id,
                'name': name,
                'year': year,
                'max_wind': max_wind,
                'min_pressure': min_pres,
                'n_obs': n_obs,
                'category': 5 if max_wind >= 137 else (4 if max_wind >= 113 else 3),
            })

major_hurricanes.sort(key=lambda x: (-x['year'], -x['max_wind']))

print(f"\n  {'Name':<15} {'Year':>6} {'Cat':>4} {'Max Wind':>10} {'Min P':>8} {'Obs':>5}")
print("-" * 55)
for h in major_hurricanes[:20]:
    print(f"  {h['name']:<15} {h['year']:>6} {h['category']:>4} {h['max_wind']:>10} kt {h['min_pressure'] or 'N/A':>7} {h['n_obs']:>5}")

# Notable storms for visualization
print("\n" + "=" * 80)
print("  RECOMMENDED FOR VISUALIZATION")
print("=" * 80)

# Find Ida 2021, Henri 2021, Laura 2020, Michael 2018, Dorian 2019
notable_names = ['IDA', 'LAURA', 'MICHAEL', 'DORIAN', 'FLORENCE', 'IRMA', 'MARIA', 'HARVEY']

print("\n  Looking for notable storms...")
for (storm_id, name, year), obs in storms.items():
    if name.upper() in notable_names and year >= 2017:
        max_wind = max(o['vmax'] for o in obs)
        min_pres = min((o['pmin'] for o in obs if o['pmin']), default=None)

        # Get track extent
        min_lat = min(o['lat'] for o in obs)
        max_lat = max(o['lat'] for o in obs)
        min_lon = min(o['lon'] for o in obs)
        max_lon = max(o['lon'] for o in obs)

        print(f"\n  {name} ({year}):")
        print(f"    Storm ID: {storm_id}")
        print(f"    Max wind: {max_wind} kt")
        print(f"    Min pressure: {min_pres} hPa")
        print(f"    Observations: {len(obs)}")
        print(f"    Track: {min_lat:.1f}°-{max_lat:.1f}°N, {min_lon:.1f}°-{max_lon:.1f}°W")

# All 2021 storms
print("\n" + "=" * 80)
print("  ALL 2021 STORMS")
print("=" * 80)

storms_2021 = [(sid, name, year, obs) for (sid, name, year), obs in storms.items() if year == 2021]
storms_2021.sort(key=lambda x: x[1])

print(f"\n  {'Name':<15} {'Max Wind':>10} {'Observations':>12}")
print("-" * 40)
for storm_id, name, year, obs in storms_2021:
    max_wind = max(o['vmax'] for o in obs)
    print(f"  {name:<15} {max_wind:>10} kt {len(obs):>12}")

print("\n" + "=" * 80)
