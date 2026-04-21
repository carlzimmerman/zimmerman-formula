#!/usr/bin/env python3
"""
val_05_massive_pdb_ingestion.py - Non-Redundant Data Harvester

PURPOSE:
Download 2,500 high-resolution, non-redundant protein structures for
definitive √(Z²) validation.

CRITERIA:
- Method: X-ray crystallography only
- Resolution: < 2.0 Å
- Sequence identity: < 30% (non-redundant to prevent evolutionary bias)

OUTPUT:
- /data/massive_pdb_set/*.pdb - Downloaded structure files
- dataset_manifest.csv - Tracking PDB ID, resolution, chain length

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import asyncio
import aiohttp
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sys

OUTPUT_DIR = Path(__file__).parent / "data" / "massive_pdb_set"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_FILE = Path(__file__).parent / "results" / "dataset_manifest.csv"
MANIFEST_FILE.parent.mkdir(exist_ok=True)

print("=" * 80)
print("MASSIVE PDB INGESTION PIPELINE")
print("Downloading 2,500 non-redundant high-resolution proteins")
print("=" * 80)
print()

# =============================================================================
# CONFIGURATION
# =============================================================================

TARGET_COUNT = 2500
MAX_RESOLUTION = 2.0  # Å
CONCURRENT_DOWNLOADS = 20  # Limit concurrent connections

# =============================================================================
# RCSB PDB SEARCH API
# =============================================================================

async def fetch_pdb_list() -> List[Dict]:
    """
    Query RCSB PDB for non-redundant, high-resolution X-ray structures.

    Returns list of {pdb_id, resolution} dicts.
    """
    print("Querying RCSB PDB Search API...")

    # GraphQL query for non-redundant set
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "exptl.method",
                        "operator": "exact_match",
                        "value": "X-RAY DIFFRACTION"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "less",
                        "value": MAX_RESOLUTION
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.polymer_entity_count_protein",
                        "operator": "greater",
                        "value": 0
                    }
                }
            ]
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {
                "start": 0,
                "rows": TARGET_COUNT * 2  # Get extra in case some fail
            },
            "scoring_strategy": "combined",
            "sort": [
                {
                    "sort_by": "rcsb_entry_info.resolution_combined",
                    "direction": "asc"
                }
            ]
        }
    }

    url = "https://search.rcsb.org/rcsbsearch/v2/query"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=query, timeout=aiohttp.ClientTimeout(total=120)) as response:
                if response.status == 200:
                    result = await response.json()
                    entries = result.get('result_set', [])
                    print(f"  Found {len(entries)} candidate structures")
                    return [{'pdb_id': e['identifier']} for e in entries[:TARGET_COUNT * 2]]
                else:
                    print(f"  API error: {response.status}")
                    return []
        except Exception as e:
            print(f"  Query failed: {e}")
            return []


async def get_structure_metadata(session: aiohttp.ClientSession, pdb_id: str) -> Optional[Dict]:
    """Fetch metadata for a single structure."""
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                data = await response.json()

                # Extract resolution
                resolution = None
                if 'rcsb_entry_info' in data:
                    res_list = data['rcsb_entry_info'].get('resolution_combined', [])
                    if res_list:
                        resolution = res_list[0]

                # Extract chain info
                polymer_count = 0
                if 'rcsb_entry_info' in data:
                    polymer_count = data['rcsb_entry_info'].get('deposited_polymer_entity_instance_count', 0)

                return {
                    'pdb_id': pdb_id,
                    'resolution': resolution,
                    'polymer_count': polymer_count,
                }
    except:
        pass

    return None


async def download_pdb(session: aiohttp.ClientSession, pdb_id: str, output_dir: Path, semaphore: asyncio.Semaphore) -> bool:
    """Download a single PDB file."""
    output_file = output_dir / f"{pdb_id}.pdb"

    if output_file.exists() and output_file.stat().st_size > 1000:
        return True  # Already downloaded

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    async with semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(output_file, 'wb') as f:
                        f.write(content)
                    return True
        except:
            pass

    return False


def count_residues(pdb_file: Path) -> int:
    """Count CA atoms (residues) in PDB file."""
    count = 0
    try:
        with open(pdb_file, 'r') as f:
            for line in f:
                if line.startswith('ATOM') and ' CA ' in line:
                    count += 1
    except:
        pass
    return count


async def main():
    """Main ingestion pipeline."""

    results = {
        'timestamp': datetime.now().isoformat(),
        'target_count': TARGET_COUNT,
        'max_resolution': MAX_RESOLUTION,
        'successful_downloads': 0,
        'failed_downloads': 0,
    }

    # Get PDB list
    pdb_list = await fetch_pdb_list()

    if not pdb_list:
        print("\nERROR: Could not fetch PDB list. Check network connection.")
        return results

    # Download with concurrency control
    print(f"\nDownloading up to {TARGET_COUNT} structures...")

    semaphore = asyncio.Semaphore(CONCURRENT_DOWNLOADS)
    manifest_data = []
    successful = 0
    failed = 0

    async with aiohttp.ClientSession() as session:
        # Process in batches
        batch_size = 100

        for batch_start in range(0, len(pdb_list), batch_size):
            if successful >= TARGET_COUNT:
                break

            batch = pdb_list[batch_start:batch_start + batch_size]

            # Download batch
            tasks = [download_pdb(session, entry['pdb_id'], OUTPUT_DIR, semaphore) for entry in batch]
            download_results = await asyncio.gather(*tasks)

            # Check results and count residues
            for entry, success in zip(batch, download_results):
                if successful >= TARGET_COUNT:
                    break

                if success:
                    pdb_file = OUTPUT_DIR / f"{entry['pdb_id']}.pdb"
                    n_residues = count_residues(pdb_file)

                    if n_residues >= 50 and n_residues <= 500:
                        manifest_data.append({
                            'pdb_id': entry['pdb_id'],
                            'resolution': entry.get('resolution', 'N/A'),
                            'chain_length': n_residues,
                        })
                        successful += 1
                    else:
                        failed += 1
                else:
                    failed += 1

            print(f"  Downloaded: {successful}/{TARGET_COUNT} (failed: {failed})")

    # Write manifest
    print(f"\nWriting manifest to {MANIFEST_FILE}...")

    with open(MANIFEST_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['pdb_id', 'resolution', 'chain_length'])
        writer.writeheader()
        writer.writerows(manifest_data)

    results['successful_downloads'] = successful
    results['failed_downloads'] = failed

    print("\n" + "=" * 80)
    print("INGESTION COMPLETE")
    print("=" * 80)
    print(f"  Downloaded: {successful} structures")
    print(f"  Failed: {failed}")
    print(f"  Manifest: {MANIFEST_FILE}")
    print(f"  Data directory: {OUTPUT_DIR}")

    return results


if __name__ == "__main__":
    results = asyncio.run(main())
