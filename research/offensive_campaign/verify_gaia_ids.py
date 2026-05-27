#!/usr/bin/env python3
"""Verify Gaia DR3 source IDs against the actual catalog."""

import json
import requests
import time

# Load our wide binary data
with open('/Users/carlzimmerman/new_physics/zimmerman-formula/website/public/data/wide_binary_data.json') as f:
    data = json.load(f)

# Extract all Gaia IDs
gaia_ids = []
for b in data['binaries']:
    gaia_ids.append(b['gaia_id_primary'])
    gaia_ids.append(b['gaia_id_secondary'])

print(f"Verifying {len(gaia_ids)} Gaia DR3 source IDs...")
print()

# Gaia Archive TAP query endpoint
TAP_URL = "https://gea.esac.esa.int/tap-server/tap/sync"

# Query in batches (Gaia TAP has query limits)
results = {}
batch_size = 10

for i in range(0, len(gaia_ids), batch_size):
    batch = gaia_ids[i:i+batch_size]
    id_list = ",".join(batch)
    
    query = f"""
    SELECT source_id, ra, dec, parallax, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE source_id IN ({id_list})
    """
    
    params = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "json",
        "QUERY": query
    }
    
    try:
        resp = requests.get(TAP_URL, params=params, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            if 'data' in result:
                for row in result['data']:
                    source_id = str(row[0])
                    results[source_id] = {
                        'ra': row[1],
                        'dec': row[2],
                        'parallax': row[3],
                        'g_mag': row[4]
                    }
        else:
            print(f"Query failed: {resp.status_code}")
            print(resp.text[:500])
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(0.5)  # Rate limit

# Report findings
print("=" * 60)
print("GAIA DR3 VERIFICATION RESULTS")
print("=" * 60)
print()

verified = 0
not_found = []

for gid in gaia_ids:
    if gid in results:
        verified += 1
        r = results[gid]
        print(f"✓ {gid}: RA={r['ra']:.4f}° Dec={r['dec']:.4f}° plx={r['parallax']:.2f}mas G={r['g_mag']:.2f}")
    else:
        not_found.append(gid)
        print(f"✗ {gid}: NOT FOUND in Gaia DR3")

print()
print("=" * 60)
print(f"VERIFIED: {verified}/{len(gaia_ids)} ({100*verified/len(gaia_ids):.1f}%)")
if not_found:
    print(f"NOT FOUND: {len(not_found)} IDs")
print("=" * 60)
