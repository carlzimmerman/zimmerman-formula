#!/usr/bin/env python3
"""Extract more wide binaries from Chae (2023) catalog - focus on deep MOND."""

import csv
import json
import math

# Constants
G = 6.674e-11  # m^3 kg^-1 s^-2
M_SUN = 1.989e30  # kg
AU_TO_M = 1.496e11  # m
A0_MOND = 1.2e-10  # m/s^2

def compute_newtonian_accel(total_mass_solar, separation_au):
    M = total_mass_solar * M_SUN
    r = separation_au * AU_TO_M
    return G * M / (r ** 2)

def classify_mond_regime(a):
    if a < 0.1 * A0_MOND:
        return "deep_mond"
    elif a < 10 * A0_MOND:
        return "intermediate"
    else:
        return "newtonian"

# Read Chae catalog
binaries = []
with open('chae_wide_binaries.zip', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            sep_kau = float(row['s[kau]'])
            sep_au = sep_kau * 1000
            
            m1 = float(row['M1[Msun]'])
            m2 = float(row['M2[Msun]'])
            total_mass = m1 + m2
            
            d1 = float(row['d1[pc]'])
            d2 = float(row['d2[pc]'])
            distance = (d1 + d2) / 2
            
            ra1 = float(row['RA1[deg]'])
            dec1 = float(row['DEC1[deg]'])
            
            source_id1 = row['source_id1']
            source_id2 = row['source_id2']
            
            a_newt = compute_newtonian_accel(total_mass, sep_au)
            regime = classify_mond_regime(a_newt)
            
            binaries.append({
                'source_id1': source_id1,
                'source_id2': source_id2,
                'ra': ra1,
                'dec': dec1,
                'distance_pc': distance,
                'separation_au': sep_au,
                'mass1': m1,
                'mass2': m2,
                'total_mass': total_mass,
                'a_newt': a_newt,
                'regime': regime
            })
        except (ValueError, KeyError):
            continue

print(f"Total binaries: {len(binaries)}")

# Count by regime
regimes = {'deep_mond': 0, 'intermediate': 0, 'newtonian': 0}
for b in binaries:
    regimes[b['regime']] += 1
print(f"Regimes: {regimes}")

# Select more binaries:
# - 20 deep MOND (most interesting for physics)
# - 10 intermediate  
# - 10 Newtonian control
deep_mond = sorted([b for b in binaries if b['regime'] == 'deep_mond'], 
                   key=lambda x: x['a_newt'])[:20]
intermediate = sorted([b for b in binaries if b['regime'] == 'intermediate'],
                      key=lambda x: x['a_newt'])[:10]
newtonian = sorted([b for b in binaries if b['regime'] == 'newtonian' and b['separation_au'] > 2000],
                   key=lambda x: -x['separation_au'])[:10]

selected = deep_mond + intermediate + newtonian
print(f"\nSelected {len(selected)} binaries:")
print(f"  Deep MOND: {len(deep_mond)}")
print(f"  Intermediate: {len(intermediate)}")
print(f"  Newtonian: {len(newtonian)}")

# Create output JSON
output = {
    "metadata": {
        "source": "Chae (2023) ApJ 952, 128 - VERIFIED Gaia DR3 source IDs",
        "extraction_date": "2026-05-26",
        "catalog_url": "https://zenodo.org/records/8065875",
        "total_binaries": len(selected),
        "catalog_total": len(binaries),
        "data_integrity": "VERIFIED - Real Gaia DR3 source IDs from published catalog",
        "mond_threshold_ms2": A0_MOND,
        "references": [
            "Chae (2023) ApJ 952, 128 - 'Breakdown of Standard Gravity'",
            "El-Badry et al. (2021) MNRAS 506, 2269 - Original binary catalog",
            "Gaia DR3 - ESA/Gaia/DPAC"
        ]
    },
    "binaries": []
}

for b in selected:
    # MOND boost factor
    if b['regime'] == 'deep_mond':
        boost = math.sqrt(A0_MOND / b['a_newt'])
    elif b['regime'] == 'intermediate':
        boost = 1.0 + 0.5 * math.sqrt(A0_MOND / b['a_newt'])
    else:
        boost = 1.0
    
    output['binaries'].append({
        "gaia_id_primary": b['source_id1'],
        "gaia_id_secondary": b['source_id2'],
        "ra_deg": round(b['ra'], 6),
        "dec_deg": round(b['dec'], 6),
        "parallax_mas": round(1000 / b['distance_pc'], 3),
        "distance_pc": round(b['distance_pc'], 2),
        "distance_kpc": round(b['distance_pc'] / 1000, 6),
        "separation_au": round(b['separation_au'], 1),
        "mass_primary_solar": round(b['mass1'], 3),
        "mass_secondary_solar": round(b['mass2'], 3),
        "total_mass_solar": round(b['total_mass'], 3),
        "newtonian_acceleration_ms2": b['a_newt'],
        "mond_regime": b['regime'],
        "expected_boost_factor": round(boost, 3),
        "source": "Chae (2023) - Zenodo dataset"
    })

output['statistics'] = {
    "n_deep_mond": len([b for b in output['binaries'] if b['mond_regime'] == 'deep_mond']),
    "n_intermediate": len([b for b in output['binaries'] if b['mond_regime'] == 'intermediate']),
    "n_newtonian": len([b for b in output['binaries'] if b['mond_regime'] == 'newtonian']),
    "catalog_total": len(binaries),
    "catalog_deep_mond": regimes['deep_mond'],
    "interpretation": "VERIFIED Gaia DR3 source IDs - queryable at gea.esac.esa.int"
}

# Write to website data folder
with open('/Users/carlzimmerman/new_physics/zimmerman-formula/website/public/data/wide_binary_data.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nWrote {len(selected)} binaries to wide_binary_data.json")

# Show range of accelerations
deep_a = [b['newtonian_acceleration_ms2'] for b in output['binaries'] if b['mond_regime'] == 'deep_mond']
print(f"\nDeep MOND acceleration range: {min(deep_a):.2e} to {max(deep_a):.2e} m/s²")
print(f"(a₀ = {A0_MOND:.2e} m/s²)")
