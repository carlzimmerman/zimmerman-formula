#!/usr/bin/env python3
"""Verify the extracted Gaia IDs are real."""

import json
import requests
import time

with open('real_wide_binaries.json') as f:
    data = json.load(f)

gaia_ids = []
for b in data['binaries']:
    gaia_ids.append(b['gaia_id_primary'])
    gaia_ids.append(b['gaia_id_secondary'])

print(f"Verifying {len(gaia_ids)} Gaia DR3 source IDs...")

TAP_URL = "https://gea.esac.esa.int/tap-server/tap/sync"

id_list = ",".join(gaia_ids)
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

resp = requests.get(TAP_URL, params=params, timeout=30)
result = resp.json()

found = {}
if 'data' in result:
    for row in result['data']:
        found[str(row[0])] = {
            'ra': row[1],
            'dec': row[2],
            'parallax': row[3],
            'g_mag': row[4]
        }

print(f"\n{'='*70}")
print("GAIA DR3 VERIFICATION RESULTS")
print("="*70)

verified = 0
for gid in gaia_ids:
    if gid in found:
        verified += 1
        r = found[gid]
        print(f"✓ {gid}: RA={r['ra']:.4f}° Dec={r['dec']:.4f}° plx={r['parallax']:.2f}mas G={r['g_mag']:.2f}")
    else:
        print(f"✗ {gid}: NOT FOUND")

print(f"\n{'='*70}")
print(f"VERIFIED: {verified}/{len(gaia_ids)} ({100*verified/len(gaia_ids):.1f}%)")
print("="*70)
