#!/usr/bin/env python3
"""
val_06_parallel_topology_engine.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

val_06_parallel_topology_engine.py - High-Throughput Topology Computation

PURPOSE:
Process 2,500 PDB files in parallel to extract H1 death radii using ripser.
Maximizes CPU utilization across all available cores.

INPUT:
- /data/massive_pdb_set/*.pdb - Downloaded structure files
- dataset_manifest.csv - List of PDB IDs to process

OUTPUT:
- global_h1_death_radii.csv - All death radii from all proteins

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import csv
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys
from typing import List, Dict, Tuple, Optional

# Ensure reproducibility
np.random.seed(42)

DATA_DIR = Path(__file__).parent / "data" / "massive_pdb_set"
OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "global_h1_death_radii.csv"

print("=" * 80)
print("PARALLEL TOPOLOGY ENGINE")
print("Multi-core persistent homology computation")
print("=" * 80)
print()

# =============================================================================
# CHECK DEPENDENCIES
# =============================================================================

def check_ripser():
    """Verify ripser is available."""
    try:
        from ripser import ripser
        return True
    except ImportError:
        print("ERROR: ripser not installed")
        print("Install with: pip install ripser")
        return False

if not check_ripser():
    sys.exit(1)

print(f"✓ ripser available")
print(f"✓ CPU cores available: {mp.cpu_count()}")
print()

# =============================================================================
# PDB PARSING
# =============================================================================

def parse_ca_coords(pdb_file: Path) -> Optional[np.ndarray]:
    """
    Extract C-alpha coordinates from PDB file.

    Returns numpy array of shape (N, 3) or None if parsing fails.
    """
    coords = []

    try:
        with open(pdb_file, 'r') as f:
            for line in f:
                if line.startswith('ATOM') and ' CA ' in line:
                    try:
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        coords.append([x, y, z])
                    except ValueError:
                        continue
    except Exception:
        return None

    if len(coords) < 30:  # Too small
        return None

    return np.array(coords, dtype=np.float64)


# =============================================================================
# RIPSER COMPUTATION
# =============================================================================

def compute_h1_deaths(coords: np.ndarray, max_edge: float = 15.0) -> List[float]:
    """
    Compute H1 death radii using ripser.

    Returns list of finite death radii.
    """
    from ripser import ripser

    # Compute distance matrix
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))

    # Run ripser
    result = ripser(dist_matrix, distance_matrix=True, maxdim=1, thresh=max_edge)

    # Extract H1 deaths
    h1 = result['dgms'][1]
    deaths = [float(d) for d in h1[:, 1] if np.isfinite(d) and d > 0]

    return deaths


def process_single_protein(pdb_file: Path) -> Tuple[str, List[float]]:
    """
    Process a single protein file.

    Returns (pdb_id, list_of_death_radii)
    """
    pdb_id = pdb_file.stem

    # Parse coordinates
    coords = parse_ca_coords(pdb_file)
    if coords is None:
        return (pdb_id, [])

    # Compute topology
    try:
        deaths = compute_h1_deaths(coords)
        return (pdb_id, deaths)
    except Exception:
        return (pdb_id, [])


# =============================================================================
# PARALLEL PROCESSING
# =============================================================================

def parallel_process_all(pdb_files: List[Path], n_workers: int = None) -> Dict:
    """
    Process all PDB files in parallel using all CPU cores.

    Returns dict with results and statistics.
    """
    if n_workers is None:
        n_workers = max(1, mp.cpu_count() - 1)  # Leave one core free

    print(f"Processing {len(pdb_files)} proteins with {n_workers} workers...")
    print()

    all_deaths = []
    protein_stats = []
    successful = 0
    failed = 0

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        # Submit all jobs
        futures = {executor.submit(process_single_protein, pdb): pdb for pdb in pdb_files}

        # Collect results
        for i, future in enumerate(as_completed(futures)):
            pdb_id, deaths = future.result()

            if deaths:
                all_deaths.extend(deaths)
                protein_stats.append({
                    'pdb_id': pdb_id,
                    'n_h1_features': len(deaths),
                    'mean_death': np.mean(deaths),
                })
                successful += 1
            else:
                failed += 1

            # Progress update
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(pdb_files)} ({successful} successful, {failed} failed)")

    return {
        'all_deaths': all_deaths,
        'protein_stats': protein_stats,
        'successful': successful,
        'failed': failed,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""

    start_time = datetime.now()

    # Find all PDB files
    if DATA_DIR.exists():
        pdb_files = list(DATA_DIR.glob('*.pdb'))
    else:
        # Fall back to regular data directory
        alt_data_dir = Path(__file__).parent / "data"
        if alt_data_dir.exists():
            pdb_files = list(alt_data_dir.glob('*.pdb'))
        else:
            pdb_files = []

    if not pdb_files:
        print("ERROR: No PDB files found")
        print(f"  Looked in: {DATA_DIR}")
        print("  Run val_05_massive_pdb_ingestion.py first")
        sys.exit(1)

    print(f"Found {len(pdb_files)} PDB files")
    print()

    # Process in parallel
    results = parallel_process_all(pdb_files)

    all_deaths = results['all_deaths']

    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)

    print(f"\nStatistics:")
    print(f"  Proteins processed: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Total H1 features: {len(all_deaths)}")

    if all_deaths:
        print(f"\nDeath radius distribution:")
        print(f"  Mean:   {np.mean(all_deaths):.4f} Å")
        print(f"  Median: {np.median(all_deaths):.4f} Å")
        print(f"  Std:    {np.std(all_deaths):.4f} Å")
        print(f"  Min:    {np.min(all_deaths):.4f} Å")
        print(f"  Max:    {np.max(all_deaths):.4f} Å")

    # Write to CSV
    print(f"\nWriting results to {OUTPUT_CSV}...")

    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['death_radius'])
        for d in all_deaths:
            writer.writerow([d])

    # Also write protein-level stats
    stats_file = OUTPUT_DIR / "protein_topology_stats.csv"
    with open(stats_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['pdb_id', 'n_h1_features', 'mean_death'])
        writer.writeheader()
        writer.writerows(results['protein_stats'])

    elapsed = datetime.now() - start_time
    print(f"\nTotal time: {elapsed}")
    print(f"\nOutput files:")
    print(f"  {OUTPUT_CSV}")
    print(f"  {stats_file}")

    return results


if __name__ == "__main__":
    results = main()
