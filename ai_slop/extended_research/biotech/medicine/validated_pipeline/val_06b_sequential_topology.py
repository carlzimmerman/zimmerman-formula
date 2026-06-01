#!/usr/bin/env python3
"""
val_06b_sequential_topology.py

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

val_06b_sequential_topology.py - Robust Sequential Topology Computation

More robust version that writes results incrementally to avoid data loss.
Processes proteins sequentially with progress saving.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import csv
import sys
from typing import List, Optional

np.random.seed(42)

DATA_DIR = Path(__file__).parent / "data" / "massive_pdb_set"
OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "global_h1_death_radii.csv"
PROGRESS_FILE = OUTPUT_DIR / "topology_progress.txt"

print("=" * 80)
print("SEQUENTIAL TOPOLOGY ENGINE (Robust)")
print("Incremental persistent homology computation")
print("=" * 80)
print()

# Check ripser
try:
    from ripser import ripser
    print("✓ ripser available")
except ImportError:
    print("ERROR: ripser not installed")
    sys.exit(1)

def parse_ca_coords(pdb_file: Path) -> Optional[np.ndarray]:
    """Extract C-alpha coordinates from PDB file."""
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

    if len(coords) < 30:
        return None
    return np.array(coords, dtype=np.float64)


def compute_h1_deaths(coords: np.ndarray, max_edge: float = 15.0) -> List[float]:
    """Compute H1 death radii using ripser."""
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


def load_processed_ids() -> set:
    """Load already-processed PDB IDs from progress file."""
    processed = set()
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            for line in f:
                processed.add(line.strip())
    return processed


def main():
    """Main execution with incremental saving."""

    start_time = datetime.now()

    # Find all PDB files
    pdb_files = list(DATA_DIR.glob('*.pdb'))
    if not pdb_files:
        print(f"ERROR: No PDB files found in {DATA_DIR}")
        sys.exit(1)

    print(f"Found {len(pdb_files)} PDB files")

    # Load progress
    processed_ids = load_processed_ids()
    print(f"Already processed: {len(processed_ids)}")

    # Filter to unprocessed
    remaining = [p for p in pdb_files if p.stem not in processed_ids]
    print(f"Remaining to process: {len(remaining)}")
    print()

    # Open output files in append mode
    write_header = not OUTPUT_CSV.exists() or OUTPUT_CSV.stat().st_size == 0

    successful = len(processed_ids)
    failed = 0
    all_deaths = []

    with open(OUTPUT_CSV, 'a', newline='') as csv_file, \
         open(PROGRESS_FILE, 'a') as progress_file:

        writer = csv.writer(csv_file)
        if write_header:
            writer.writerow(['death_radius'])

        for i, pdb_file in enumerate(remaining):
            pdb_id = pdb_file.stem

            # Parse and compute
            coords = parse_ca_coords(pdb_file)
            if coords is None:
                failed += 1
                continue

            try:
                deaths = compute_h1_deaths(coords)
                if deaths:
                    # Write deaths immediately
                    for d in deaths:
                        writer.writerow([d])
                    all_deaths.extend(deaths)

                    # Mark as processed
                    progress_file.write(f"{pdb_id}\n")
                    progress_file.flush()
                    csv_file.flush()

                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                continue

            # Progress update
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(remaining)} ({successful} successful, {failed} failed)")

    # Summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)

    # Read all deaths from CSV
    all_deaths_final = []
    with open(OUTPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                all_deaths_final.append(float(row['death_radius']))
            except:
                pass

    print(f"\nStatistics:")
    print(f"  Total proteins processed: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total H1 features: {len(all_deaths_final)}")

    if all_deaths_final:
        print(f"\nDeath radius distribution:")
        print(f"  Mean:   {np.mean(all_deaths_final):.4f} Å")
        print(f"  Median: {np.median(all_deaths_final):.4f} Å")
        print(f"  Std:    {np.std(all_deaths_final):.4f} Å")
        print(f"  Min:    {np.min(all_deaths_final):.4f} Å")
        print(f"  Max:    {np.max(all_deaths_final):.4f} Å")

    elapsed = datetime.now() - start_time
    print(f"\nTime: {elapsed}")
    print(f"Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
