#!/usr/bin/env python3
"""
Polite Structure Fetcher - Rate-Limited PDB API Client

SPDX-License-Identifier: AGPL-3.0-or-later

This script fetches protein structures from RCSB PDB with proper rate limiting
and exponential backoff to respect public server limits.

Features:
- Rate limiting (0.5s between requests)
- Exponential backoff on HTTP 429
- PDBFixer integration for structure cleanup
- Proper protonation at physiological pH 7.4
- Hydrogen addition and water removal

Target: Aβ42 structure (PDB: 1IYT) for Z² alignment testing

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURATION
# ==============================================================================

PDB_API_URL = "https://files.rcsb.org/download/{}.pdb"
PDB_GRAPHQL_URL = "https://data.rcsb.org/graphql"

# Rate limiting
MIN_REQUEST_INTERVAL = 0.5  # seconds
MAX_RETRIES = 5
INITIAL_BACKOFF = 1.0  # seconds

# ==============================================================================
# RATE-LIMITED API CLIENT
# ==============================================================================

class PoliteAPIClient:
    """
    API client with rate limiting and exponential backoff.

    Respects public server limits to avoid overloading RCSB infrastructure.
    """

    def __init__(self, min_interval: float = MIN_REQUEST_INTERVAL):
        self.min_interval = min_interval
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ZimmermanResearch/1.0 (scientific research; AGPL-3.0)',
            'Accept': 'text/plain, application/json'
        })

    def _wait_for_rate_limit(self):
        """Wait to respect rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            print(f"    Rate limiting: waiting {sleep_time:.2f}s...")
            time.sleep(sleep_time)

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Make a GET request with rate limiting and exponential backoff.
        """
        backoff = INITIAL_BACKOFF

        for attempt in range(MAX_RETRIES):
            self._wait_for_rate_limit()

            try:
                response = self.session.get(url, timeout=30, **kwargs)
                self.last_request_time = time.time()

                if response.status_code == 429:
                    # Too Many Requests - exponential backoff
                    retry_after = response.headers.get('Retry-After', backoff)
                    try:
                        wait_time = float(retry_after)
                    except ValueError:
                        wait_time = backoff

                    print(f"    HTTP 429: Rate limited. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    backoff *= 2  # Exponential backoff
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.Timeout:
                print(f"    Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
                time.sleep(backoff)
                backoff *= 2

            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                print(f"    Request error: {e}. Retrying...")
                time.sleep(backoff)
                backoff *= 2

        raise RuntimeError(f"Failed after {MAX_RETRIES} attempts")

    def post(self, url: str, **kwargs) -> requests.Response:
        """Make a POST request with rate limiting."""
        self._wait_for_rate_limit()
        response = self.session.post(url, timeout=30, **kwargs)
        self.last_request_time = time.time()
        return response


# ==============================================================================
# PDB STRUCTURE FETCHER
# ==============================================================================

def fetch_pdb_structure(
    pdb_id: str,
    output_dir: str = ".",
    client: Optional[PoliteAPIClient] = None
) -> str:
    """
    Fetch PDB structure with rate limiting.

    Args:
        pdb_id: 4-letter PDB ID
        output_dir: Output directory
        client: Polite API client instance

    Returns:
        Path to downloaded PDB file
    """
    if client is None:
        client = PoliteAPIClient()

    pdb_id = pdb_id.upper()
    url = PDB_API_URL.format(pdb_id)

    print(f"\n  Fetching PDB: {pdb_id}")
    print(f"  URL: {url}")

    response = client.get(url)

    os.makedirs(output_dir, exist_ok=True)
    pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

    with open(pdb_path, 'w') as f:
        f.write(response.text)

    # Count atoms
    n_atoms = sum(1 for line in response.text.split('\n')
                  if line.startswith('ATOM') or line.startswith('HETATM'))

    print(f"  Downloaded: {pdb_path}")
    print(f"  Atoms: {n_atoms}")

    return pdb_path


def get_pdb_metadata(
    pdb_id: str,
    client: Optional[PoliteAPIClient] = None
) -> Dict:
    """
    Get PDB metadata using GraphQL API.
    """
    if client is None:
        client = PoliteAPIClient()

    query = """
    query($id: String!) {
        entry(entry_id: $id) {
            rcsb_entry_info {
                resolution_combined
                experimental_method
            }
            struct {
                title
            }
            polymer_entities {
                rcsb_polymer_entity {
                    pdbx_description
                }
            }
        }
    }
    """

    print(f"\n  Fetching metadata for {pdb_id}...")

    response = client.post(
        PDB_GRAPHQL_URL,
        json={'query': query, 'variables': {'id': pdb_id.upper()}}
    )

    data = response.json()

    if 'data' in data and data['data']['entry']:
        entry = data['data']['entry']
        return {
            'pdb_id': pdb_id.upper(),
            'title': entry.get('struct', {}).get('title'),
            'resolution': entry.get('rcsb_entry_info', {}).get('resolution_combined'),
            'method': entry.get('rcsb_entry_info', {}).get('experimental_method')
        }

    return {'pdb_id': pdb_id.upper(), 'error': 'Metadata not found'}


# ==============================================================================
# STRUCTURE CLEANUP (PDBFixer)
# ==============================================================================

def prepare_structure_for_md(
    pdb_path: str,
    output_path: str,
    ph: float = 7.4,
    remove_water: bool = True,
    add_hydrogens: bool = True
) -> Dict:
    """
    Prepare structure for molecular dynamics using PDBFixer.

    Args:
        pdb_path: Input PDB file
        output_path: Output prepared PDB file
        ph: Target pH for protonation states
        remove_water: Remove water molecules
        add_hydrogens: Add missing hydrogens

    Returns:
        Dictionary with preparation details
    """
    print(f"\n  Preparing structure for MD...")
    print(f"  Input: {pdb_path}")
    print(f"  pH: {ph}")

    log = {
        'input': pdb_path,
        'output': output_path,
        'ph': ph,
        'operations': []
    }

    try:
        from pdbfixer import PDBFixer
        from openmm.app import PDBFile

        fixer = PDBFixer(filename=pdb_path)

        # Find and add missing residues
        fixer.findMissingResidues()
        missing_res = dict(fixer.missingResidues)
        if missing_res:
            print(f"  Found {len(missing_res)} gaps with missing residues")
            log['operations'].append(f"Missing residues: {len(missing_res)} gaps")
            # Note: Adding missing residues requires templates

        # Find and add missing atoms
        fixer.findMissingAtoms()
        n_missing = sum(len(atoms) for atoms in fixer.missingAtoms.values())
        if n_missing > 0:
            print(f"  Adding {n_missing} missing heavy atoms...")
            fixer.addMissingAtoms()
            log['operations'].append(f"Added {n_missing} missing heavy atoms")

        # Remove water molecules
        if remove_water:
            fixer.removeHeterogens(keepWater=False)
            print("  Removed water molecules and heterogens")
            log['operations'].append("Removed water molecules")

        # Add hydrogens at specified pH
        if add_hydrogens:
            print(f"  Adding hydrogens at pH {ph}...")
            fixer.addMissingHydrogens(ph)
            log['operations'].append(f"Added hydrogens at pH {ph}")

            # Log protonation states of titratable residues
            titratable = ['HIS', 'ASP', 'GLU', 'LYS', 'ARG', 'CYS', 'TYR']
            protonation_log = []

            for chain in fixer.topology.chains():
                for residue in chain.residues():
                    if residue.name in titratable:
                        protonation_log.append(f"{residue.name}{residue.id}")

            if protonation_log:
                print(f"  Titratable residues: {len(protonation_log)}")
                log['titratable_residues'] = protonation_log[:20]  # First 20

        # Save prepared structure
        with open(output_path, 'w') as f:
            PDBFile.writeFile(fixer.topology, fixer.positions, f)

        # Count final atoms
        n_atoms = sum(1 for _ in fixer.topology.atoms())
        print(f"  Final atom count: {n_atoms}")
        log['final_atoms'] = n_atoms

        print(f"  Saved: {output_path}")
        log['success'] = True

    except ImportError:
        print("\n  WARNING: PDBFixer not available")
        print("  Install with: conda install -c conda-forge pdbfixer")

        # Fallback: simple cleanup
        log = fallback_structure_cleanup(pdb_path, output_path)

    return log


def fallback_structure_cleanup(pdb_path: str, output_path: str) -> Dict:
    """
    Fallback structure cleanup without PDBFixer.

    Simply removes water and non-protein atoms.
    """
    print("  Using fallback cleanup (no PDBFixer)...")

    protein_lines = []
    water_count = 0
    hetero_count = 0

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                protein_lines.append(line)
            elif line.startswith('HETATM'):
                res_name = line[17:20].strip()
                if res_name in ['HOH', 'WAT', 'H2O']:
                    water_count += 1
                else:
                    hetero_count += 1
            elif line.startswith('END'):
                protein_lines.append(line)

    with open(output_path, 'w') as f:
        f.write(f"REMARK   Cleaned by fallback method\n")
        f.write(f"REMARK   Removed {water_count} waters, {hetero_count} heteroatoms\n")
        f.writelines(protein_lines)

    print(f"  Removed: {water_count} waters, {hetero_count} heteroatoms")
    print(f"  Saved: {output_path}")

    return {
        'method': 'fallback',
        'waters_removed': water_count,
        'heteroatoms_removed': hetero_count,
        'success': True
    }


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def fetch_and_prepare_structure(
    pdb_id: str,
    output_dir: str = "prepared_structures",
    ph: float = 7.4
) -> Dict:
    """
    Complete pipeline: fetch + prepare structure for MD.

    Args:
        pdb_id: PDB ID to fetch
        output_dir: Output directory
        ph: Target pH for protonation

    Returns:
        Complete results dictionary
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*70)
    print("POLITE STRUCTURE FETCHER")
    print("="*70)
    print(f"Target: {pdb_id}")
    print(f"Rate limit: {MIN_REQUEST_INTERVAL}s between requests")
    print("="*70)

    client = PoliteAPIClient()
    results = {
        'pdb_id': pdb_id,
        'timestamp': datetime.now().isoformat(),
        'license': 'AGPL-3.0-or-later'
    }

    # Step 1: Get metadata
    print("\n  [1] Fetching metadata...")
    metadata = get_pdb_metadata(pdb_id, client)
    results['metadata'] = metadata

    if 'title' in metadata:
        print(f"      Title: {metadata['title']}")
    if 'resolution' in metadata and metadata['resolution']:
        print(f"      Resolution: {metadata['resolution']} Å")
    if 'method' in metadata:
        print(f"      Method: {metadata['method']}")

    # Step 2: Download structure
    print("\n  [2] Downloading structure...")
    raw_pdb = fetch_pdb_structure(pdb_id, output_dir, client)
    results['raw_pdb'] = raw_pdb

    # Step 3: Prepare for MD
    print("\n  [3] Preparing for molecular dynamics...")
    prepared_pdb = os.path.join(output_dir, f"{pdb_id}_md_ready.pdb")
    prep_log = prepare_structure_for_md(raw_pdb, prepared_pdb, ph=ph)

    results['prepared_pdb'] = prepared_pdb
    results['preparation'] = prep_log

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"  PDB ID: {pdb_id}")
    print(f"  Raw structure: {raw_pdb}")
    print(f"  MD-ready structure: {prepared_pdb}")
    print(f"  Preparation pH: {ph}")

    if 'operations' in prep_log:
        print(f"\n  Operations performed:")
        for op in prep_log['operations']:
            print(f"    - {op}")

    # Save results
    results_file = os.path.join(output_dir, f"{pdb_id}_fetch_log.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Log saved: {results_file}")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Fetch and prepare Aβ42 structure for Z² alignment testing."""
    print("\n" + "="*70)
    print("POLITE STRUCTURE FETCHER - Aβ42 FOR Z² TESTING")
    print("="*70)
    print("Target: Amyloid-β 42 peptide (PDB: 1IYT)")
    print("Purpose: Prepare for hybrid Z² + AMBER force field testing")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    try:
        results = fetch_and_prepare_structure(
            pdb_id='1IYT',  # Aβ42 NMR structure
            output_dir='hybrid_z2_test',
            ph=7.4
        )

        return results

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


if __name__ == '__main__':
    main()
