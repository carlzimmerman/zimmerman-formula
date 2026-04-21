#!/usr/bin/env python3
"""
03_strict_persistent_homology.py - Deterministic Topological Analysis

PURPOSE:
Run persistent homology on protein structures with STRICT determinism.
Implements Gemini's "Strict Determinism (Anti-Hallucination)" prompt.

CRITICAL RULES:
1. NO mock data or hardcoded outputs
2. If calculation fails, raise Exception (do NOT return defaults)
3. Explicit random seeds where needed
4. Output RAW float arrays to CSV (no interpretation)
5. Use ripser if available, otherwise FAIL (not fallback)

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
import sys
from typing import List, Tuple, Optional

# Strict random seed
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "results"
LOG_DIR = Path(__file__).parent / "logs"

for d in [DATA_DIR, OUTPUT_DIR, LOG_DIR]:
    d.mkdir(exist_ok=True)

print("=" * 80)
print("STRICT PERSISTENT HOMOLOGY PIPELINE")
print("Deterministic topological analysis - NO fallbacks")
print("=" * 80)
print()


# =============================================================================
# STRICT LIBRARY CHECK
# =============================================================================

def check_ripser():
    """Check if ripser is available. FAIL if not."""
    try:
        from ripser import ripser
        print("✓ ripser library available")
        return True
    except ImportError:
        print("✗ ripser NOT INSTALLED")
        print("\nTo install: pip install ripser")
        print("\nThis script requires ripser for GOLD STANDARD persistent homology.")
        print("Fallback methods are NOT acceptable for rigorous analysis.")
        return False


RIPSER_AVAILABLE = check_ripser()


# =============================================================================
# PDB PARSING (STRICT)
# =============================================================================

def parse_pdb_strict(pdb_file: Path) -> np.ndarray:
    """
    Parse PDB file and extract C-alpha coordinates.

    STRICT: Raises exceptions on any parsing error.
    """
    if not pdb_file.exists():
        raise FileNotFoundError(f"PDB file not found: {pdb_file}")

    coords = []

    with open(pdb_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    coords.append([x, y, z])
                except ValueError as e:
                    raise ValueError(f"Parse error at line {line_num}: {e}")

    if len(coords) == 0:
        raise ValueError(f"No C-alpha atoms found in {pdb_file}")

    coords = np.array(coords, dtype=np.float64)

    # Validate coordinates are reasonable
    if np.any(np.isnan(coords)):
        raise ValueError("NaN values in coordinates")

    if np.any(np.abs(coords) > 1000):
        raise ValueError("Unreasonable coordinate values (>1000 Å)")

    print(f"  Parsed {len(coords)} C-alpha atoms from {pdb_file.name}")

    return coords


# =============================================================================
# DISTANCE MATRIX (STRICT)
# =============================================================================

def compute_distance_matrix_strict(coords: np.ndarray) -> np.ndarray:
    """
    Compute pairwise Euclidean distance matrix.

    STRICT: Validates output, raises on any numerical issues.
    """
    n = len(coords)

    # Use efficient numpy broadcasting
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))

    # Validate
    if np.any(np.isnan(dist_matrix)):
        raise ValueError("NaN in distance matrix")

    if np.any(np.isinf(dist_matrix)):
        raise ValueError("Inf in distance matrix")

    # Check symmetry
    if not np.allclose(dist_matrix, dist_matrix.T):
        raise ValueError("Distance matrix not symmetric")

    # Check diagonal is zero
    if not np.allclose(np.diag(dist_matrix), 0):
        raise ValueError("Distance matrix diagonal not zero")

    return dist_matrix


# =============================================================================
# PERSISTENT HOMOLOGY (STRICT - RIPSER ONLY)
# =============================================================================

def compute_persistent_homology_strict(
    dist_matrix: np.ndarray,
    max_dim: int = 2,
    max_edge_length: float = 50.0,
) -> dict:
    """
    Compute persistent homology using ripser.

    STRICT: No fallback. Raises if ripser unavailable.
    """
    if not RIPSER_AVAILABLE:
        raise ImportError(
            "ripser not available. Install with: pip install ripser\n"
            "Fallback methods are NOT acceptable for rigorous analysis."
        )

    from ripser import ripser

    print(f"  Running ripser (max_dim={max_dim}, max_edge={max_edge_length})...")

    result = ripser(
        dist_matrix,
        distance_matrix=True,
        maxdim=max_dim,
        thresh=max_edge_length,
    )

    # Extract persistence diagrams
    diagrams = {}

    for dim in range(max_dim + 1):
        dgm = result['dgms'][dim]

        # Filter out infinite death times for statistics
        finite_mask = np.isfinite(dgm[:, 1])
        dgm_finite = dgm[finite_mask]

        diagrams[f'H{dim}'] = {
            'birth': dgm[:, 0].tolist(),
            'death': dgm[:, 1].tolist(),
            'persistence': (dgm[:, 1] - dgm[:, 0]).tolist(),
            'n_features': len(dgm),
            'n_finite': len(dgm_finite),
        }

        if len(dgm_finite) > 0:
            diagrams[f'H{dim}']['finite_stats'] = {
                'birth_mean': float(np.mean(dgm_finite[:, 0])),
                'birth_std': float(np.std(dgm_finite[:, 0])),
                'death_mean': float(np.mean(dgm_finite[:, 1])),
                'death_std': float(np.std(dgm_finite[:, 1])),
                'persistence_mean': float(np.mean(dgm_finite[:, 1] - dgm_finite[:, 0])),
                'persistence_std': float(np.std(dgm_finite[:, 1] - dgm_finite[:, 0])),
            }

    return diagrams


# =============================================================================
# RAW OUTPUT (NO INTERPRETATION)
# =============================================================================

def save_raw_output(pdb_id: str, diagrams: dict, output_dir: Path):
    """
    Save raw numerical output to CSV files.

    NO interpretation. NO "success" messages. Just raw data.
    """
    for dim_name, dgm_data in diagrams.items():
        csv_file = output_dir / f"{pdb_id}_{dim_name}_raw.csv"

        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['birth', 'death', 'persistence'])

            births = dgm_data['birth']
            deaths = dgm_data['death']
            persistence = dgm_data['persistence']

            for b, d, p in zip(births, deaths, persistence):
                writer.writerow([b, d, p])


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def analyze_single_protein(pdb_file: Path) -> dict:
    """
    Analyze a single protein structure.

    Returns raw numerical results. No interpretation.
    """
    pdb_id = pdb_file.stem

    print(f"\nAnalyzing: {pdb_id}")

    # Parse
    coords = parse_pdb_strict(pdb_file)

    # Distance matrix
    print("  Computing distance matrix...")
    dist_matrix = compute_distance_matrix_strict(coords)

    # Persistent homology
    diagrams = compute_persistent_homology_strict(dist_matrix)

    # Save raw output
    save_raw_output(pdb_id, diagrams, OUTPUT_DIR)

    result = {
        'pdb_id': pdb_id,
        'n_residues': len(coords),
        'coord_range': {
            'x': [float(coords[:, 0].min()), float(coords[:, 0].max())],
            'y': [float(coords[:, 1].min()), float(coords[:, 1].max())],
            'z': [float(coords[:, 2].min()), float(coords[:, 2].max())],
        },
        'dist_range': [float(dist_matrix[dist_matrix > 0].min()),
                       float(dist_matrix.max())],
        'diagrams': diagrams,
    }

    return result


def analyze_protein_set(pdb_files: List[Path]) -> dict:
    """
    Analyze multiple proteins.

    STRICT: Stops on first failure.
    """
    print("=" * 80)
    print(f"Analyzing {len(pdb_files)} protein structures")
    print("=" * 80)

    results = {
        'timestamp': datetime.now().isoformat(),
        'n_proteins': len(pdb_files),
        'random_seed': RANDOM_SEED,
        'ripser_available': RIPSER_AVAILABLE,
        'proteins': [],
    }

    for pdb_file in pdb_files:
        try:
            protein_result = analyze_single_protein(pdb_file)
            results['proteins'].append(protein_result)
        except Exception as e:
            # STRICT: Re-raise, don't continue
            raise RuntimeError(f"Analysis failed for {pdb_file}: {e}")

    return results


# =============================================================================
# AGGREGATE STATISTICS (RAW)
# =============================================================================

def compute_aggregate_statistics(results: dict) -> dict:
    """
    Compute aggregate statistics across all proteins.

    Returns RAW numbers. No Z² comparison here - that's for blinded analysis.
    """
    all_h1_deaths = []

    for protein in results['proteins']:
        if 'H1' in protein['diagrams']:
            h1 = protein['diagrams']['H1']
            # Only include finite deaths
            deaths = [d for d in h1['death'] if np.isfinite(d)]
            all_h1_deaths.extend(deaths)

    if len(all_h1_deaths) == 0:
        return {'error': 'No H1 features found'}

    all_h1_deaths = np.array(all_h1_deaths)

    stats = {
        'n_proteins': len(results['proteins']),
        'total_h1_features': len(all_h1_deaths),
        'h1_death_min': float(all_h1_deaths.min()),
        'h1_death_max': float(all_h1_deaths.max()),
        'h1_death_mean': float(np.mean(all_h1_deaths)),
        'h1_death_median': float(np.median(all_h1_deaths)),
        'h1_death_std': float(np.std(all_h1_deaths)),
        'h1_death_percentiles': {
            '10': float(np.percentile(all_h1_deaths, 10)),
            '25': float(np.percentile(all_h1_deaths, 25)),
            '50': float(np.percentile(all_h1_deaths, 50)),
            '75': float(np.percentile(all_h1_deaths, 75)),
            '90': float(np.percentile(all_h1_deaths, 90)),
        },
    }

    # Histogram bins (raw counts)
    bins = [0, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 30, 50]
    hist, _ = np.histogram(all_h1_deaths, bins=bins)
    stats['h1_death_histogram'] = {
        'bins': bins,
        'counts': hist.tolist(),
    }

    return stats


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""

    if not RIPSER_AVAILABLE:
        print("\n" + "=" * 80)
        print("CANNOT PROCEED: ripser not installed")
        print("=" * 80)
        print("\nThis pipeline requires ripser for rigorous analysis.")
        print("Install with: pip install ripser")
        print("\nFallback methods are NOT acceptable.")
        sys.exit(1)

    # Find PDB files
    pdb_files = list(DATA_DIR.glob('*.pdb'))

    if len(pdb_files) == 0:
        print("\n" + "=" * 80)
        print("NO PDB FILES FOUND")
        print("=" * 80)
        print(f"\nExpected PDB files in: {DATA_DIR}")
        print("Run 01_data_provenance.py first to fetch structures.")
        sys.exit(1)

    print(f"\nFound {len(pdb_files)} PDB files")

    # Analyze
    try:
        results = analyze_protein_set(pdb_files)
    except RuntimeError as e:
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)

    # Aggregate statistics
    print("\n" + "=" * 80)
    print("AGGREGATE STATISTICS (RAW)")
    print("=" * 80)

    stats = compute_aggregate_statistics(results)
    results['aggregate_statistics'] = stats

    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        elif isinstance(value, int):
            print(f"  {key}: {value}")

    # Save results
    output_file = OUTPUT_DIR / "persistent_homology_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved: {output_file}")

    # Save aggregate CSV
    csv_file = OUTPUT_DIR / "h1_death_radii_aggregate.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['pdb_id', 'h1_death_radius'])

        for protein in results['proteins']:
            if 'H1' in protein['diagrams']:
                for death in protein['diagrams']['H1']['death']:
                    if np.isfinite(death):
                        writer.writerow([protein['pdb_id'], death])

    print(f"Aggregate CSV: {csv_file}")

    print("\n" + "=" * 80)
    print("RAW DATA READY FOR BLINDED ANALYSIS")
    print("=" * 80)
    print("""
    The data has been computed WITHOUT any Z² bias.

    To perform blinded analysis:
    1. Run 04_blinded_analysis.py
    2. Provide the raw CSV data
    3. Let statistics determine if Z² = 9.14 Å is special

    DO NOT manually inspect for Z² matches - that introduces bias.
    """)

    return results


if __name__ == "__main__":
    results = main()
