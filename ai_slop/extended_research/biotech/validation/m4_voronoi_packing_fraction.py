#!/usr/bin/env python3
"""
M4 Voronoi Packing Fraction Analysis
======================================

Rigorous test of Z² = 32π/3 predictions using Voronoi tessellation.

PREDICTIONS FROM Z² = 32π/3:
1. Coordination number = Z²/Vol(B³) = 8 (BCC-like)
2. Voronoi cells should be truncated octahedra (14 faces)
3. Local packing fraction η ≈ 0.68 (BCC packing)

This script:
1. Calculates Voronoi tessellation of Cα atoms in proteins
2. Measures actual coordination numbers
3. Counts Voronoi cell faces
4. Computes local packing fractions
5. Tests against Z²-derived predictions

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import requests

from scipy.spatial import Voronoi, ConvexHull
from scipy.spatial.distance import pdist, squareform


# Physical constants
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
VOL_B3 = 4 * np.pi / 3      # Volume of unit 3-ball
PREDICTED_COORDINATION = Z_SQUARED / VOL_B3  # = 8 exactly
PREDICTED_VORONOI_FACES = 14  # Truncated octahedron (BCC Voronoi cell)
PREDICTED_PACKING_BCC = np.pi * np.sqrt(3) / 8  # ≈ 0.68


@dataclass
class VoronoiResult:
    """Results from Voronoi analysis of a single protein."""
    pdb_id: str
    n_residues: int
    n_interior_residues: int  # Not on boundary

    # Coordination (number of Voronoi neighbors)
    mean_coordination: float
    std_coordination: float
    median_coordination: float

    # Face counts
    mean_faces: float
    std_faces: float

    # Packing fraction
    mean_packing: float
    std_packing: float

    # Cell volumes
    mean_cell_volume: float
    median_cell_volume: float


@dataclass
class Z2ValidationVoronoi:
    """Complete validation results."""
    timestamp: str
    n_structures: int
    total_interior_residues: int

    # Coordination test
    overall_mean_coordination: float
    coordination_sem: float
    coordination_ci_95: Tuple[float, float]
    coordination_prediction: float
    coordination_p_value: float
    coordination_validated: bool

    # Face count test
    overall_mean_faces: float
    faces_sem: float
    faces_prediction: float
    faces_validated: bool

    # Packing test
    overall_mean_packing: float
    packing_sem: float
    packing_prediction: float
    packing_validated: bool


def download_pdb(pdb_id: str, cache_dir: Path) -> Optional[Path]:
    """Download PDB file."""
    pdb_path = cache_dir / f"{pdb_id.lower()}.pdb"

    if pdb_path.exists():
        return pdb_path

    try:
        response = requests.get(
            f"https://files.rcsb.org/download/{pdb_id}.pdb",
            timeout=30
        )
        response.raise_for_status()

        with open(pdb_path, "w") as f:
            f.write(response.text)

        return pdb_path
    except Exception as e:
        return None


def parse_ca_coordinates(pdb_path: Path) -> np.ndarray:
    """Extract Cα coordinates from PDB file."""
    coords = []

    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
                except ValueError:
                    continue

    return np.array(coords)


def compute_voronoi_statistics(coords: np.ndarray) -> Optional[Dict]:
    """
    Compute Voronoi tessellation and extract statistics.

    Returns statistics for interior cells only (boundary cells are infinite).
    """
    if len(coords) < 10:
        return None

    try:
        vor = Voronoi(coords)
    except Exception as e:
        return None

    # Analyze each cell
    coordination_numbers = []
    face_counts = []
    cell_volumes = []
    packing_fractions = []

    # van der Waals radius approximation for Cα
    r_vdw = 1.7  # Å (carbon vdW radius)
    v_atom = (4/3) * np.pi * r_vdw**3

    for i, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]

        # Skip infinite regions (boundary cells)
        if -1 in region or len(region) == 0:
            continue

        # Get vertices of this Voronoi cell
        vertices = vor.vertices[region]

        # Skip if any vertex is far from the point (numerical issues)
        if np.any(np.linalg.norm(vertices - coords[i], axis=1) > 50):
            continue

        # Coordination number = number of Voronoi neighbors
        # This is the number of faces of the Voronoi cell
        n_faces = len(region)
        face_counts.append(n_faces)

        # Each face corresponds to a neighbor
        coordination_numbers.append(n_faces)

        # Compute cell volume using convex hull
        try:
            hull = ConvexHull(vertices)
            cell_vol = hull.volume
            cell_volumes.append(cell_vol)

            # Packing fraction = atom volume / cell volume
            packing = v_atom / cell_vol
            if 0 < packing < 1:  # Sanity check
                packing_fractions.append(packing)
        except Exception:
            continue

    if len(coordination_numbers) < 5:
        return None

    return {
        "n_interior": len(coordination_numbers),
        "coordination": np.array(coordination_numbers),
        "faces": np.array(face_counts),
        "volumes": np.array(cell_volumes) if cell_volumes else np.array([0]),
        "packing": np.array(packing_fractions) if packing_fractions else np.array([0])
    }


def analyze_protein(pdb_path: Path) -> Optional[VoronoiResult]:
    """Complete Voronoi analysis of a single protein."""
    coords = parse_ca_coordinates(pdb_path)

    if len(coords) < 20:
        return None

    stats = compute_voronoi_statistics(coords)

    if stats is None:
        return None

    return VoronoiResult(
        pdb_id=pdb_path.stem.upper(),
        n_residues=len(coords),
        n_interior_residues=stats["n_interior"],
        mean_coordination=float(np.mean(stats["coordination"])),
        std_coordination=float(np.std(stats["coordination"])),
        median_coordination=float(np.median(stats["coordination"])),
        mean_faces=float(np.mean(stats["faces"])),
        std_faces=float(np.std(stats["faces"])),
        mean_packing=float(np.mean(stats["packing"])) if len(stats["packing"]) > 0 else 0.0,
        std_packing=float(np.std(stats["packing"])) if len(stats["packing"]) > 0 else 0.0,
        mean_cell_volume=float(np.mean(stats["volumes"])) if len(stats["volumes"]) > 0 else 0.0,
        median_cell_volume=float(np.median(stats["volumes"])) if len(stats["volumes"]) > 0 else 0.0
    )


def run_voronoi_validation(n_structures: int = 50) -> Z2ValidationVoronoi:
    """
    Run complete Voronoi-based validation of Z² predictions.
    """
    print("=" * 70)
    print("M4 VORONOI PACKING FRACTION ANALYSIS")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Print predictions
    print("Z² = 32π/3 PREDICTIONS:")
    print("-" * 50)
    print(f"Z² = {Z_SQUARED:.6f}")
    print(f"Z² / Vol(B³) = {PREDICTED_COORDINATION:.4f} (coordination number)")
    print(f"BCC Voronoi cell: {PREDICTED_VORONOI_FACES} faces (truncated octahedron)")
    print(f"BCC packing fraction: η = {PREDICTED_PACKING_BCC:.6f}")
    print()

    # Setup
    cache_dir = Path(__file__).parent / "pdb_cache"
    cache_dir.mkdir(exist_ok=True)

    # Get PDB list
    print(f"Fetching {n_structures} high-resolution structures...")

    # Use a diverse set of well-characterized proteins
    pdb_ids = [
        "1LYZ", "1UBQ", "1CRN", "4HHB", "1MBN", "2PTC", "1IGD", "1PGB",
        "1ENH", "1ROP", "1CTF", "256B", "1ECA", "1SN3", "1HOE", "1L2Y",
        "3BLM", "4MDH", "1AKE", "1PHT", "1TIM", "1TPH", "5CYT", "3PGB",
        "1FME", "1LMB", "1A3N", "1GZX", "5PTI", "6LYZ", "2DHB", "3ADK",
        "2AK3", "2PHH", "2TIM", "2LYZ", "3LYZ", "4LYZ", "5LYZ", "2ENH",
        "1VII", "1L63", "1PIN", "1BPI", "1COA", "1FNA", "1HRC", "2I1B",
        "1CSK", "1GUX"
    ][:n_structures]

    # Analyze structures
    results = []
    print(f"\nAnalyzing {len(pdb_ids)} structures...")

    for i, pdb_id in enumerate(pdb_ids):
        pdb_path = download_pdb(pdb_id, cache_dir)

        if pdb_path is None:
            continue

        result = analyze_protein(pdb_path)

        if result is not None:
            results.append(result)

            if (i + 1) % 10 == 0:
                avg_coord = np.mean([r.mean_coordination for r in results])
                print(f"  Processed {i+1}/{len(pdb_ids)}, "
                      f"current mean coordination: {avg_coord:.2f}")

    print(f"\nSuccessfully analyzed {len(results)} structures")

    if len(results) < 10:
        print("ERROR: Insufficient data")
        return None

    # Aggregate statistics
    all_coordination = np.array([r.mean_coordination for r in results])
    all_faces = np.array([r.mean_faces for r in results])
    all_packing = np.array([r.mean_packing for r in results if r.mean_packing > 0])

    n = len(results)

    # Coordination statistics
    coord_mean = np.mean(all_coordination)
    coord_std = np.std(all_coordination, ddof=1)
    coord_sem = coord_std / np.sqrt(n)
    coord_ci = (coord_mean - 1.96 * coord_sem, coord_mean + 1.96 * coord_sem)

    # t-test against prediction
    from scipy import stats
    t_stat, p_coord = stats.ttest_1samp(all_coordination, PREDICTED_COORDINATION)
    coord_validated = coord_ci[0] <= PREDICTED_COORDINATION <= coord_ci[1]

    # Face count statistics
    faces_mean = np.mean(all_faces)
    faces_std = np.std(all_faces, ddof=1)
    faces_sem = faces_std / np.sqrt(n)
    faces_validated = abs(faces_mean - PREDICTED_VORONOI_FACES) < 2 * faces_sem

    # Packing statistics
    if len(all_packing) > 0:
        packing_mean = np.mean(all_packing)
        packing_std = np.std(all_packing, ddof=1)
        packing_sem = packing_std / np.sqrt(len(all_packing))
        packing_validated = abs(packing_mean - PREDICTED_PACKING_BCC) < 0.1
    else:
        packing_mean = 0.0
        packing_sem = 0.0
        packing_validated = False

    # Print results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Structures analyzed: {len(results)}")
    print(f"Total interior residues: {sum(r.n_interior_residues for r in results)}")
    print()

    print("COORDINATION NUMBER (Voronoi neighbors):")
    print("-" * 50)
    print(f"  Observed mean: {coord_mean:.3f} ± {coord_sem:.3f}")
    print(f"  95% CI: [{coord_ci[0]:.3f}, {coord_ci[1]:.3f}]")
    print(f"  Prediction (Z²/Vol): {PREDICTED_COORDINATION:.3f}")
    print(f"  t-statistic: {t_stat:.3f}")
    print(f"  p-value: {p_coord:.2e}")
    if coord_validated:
        print(f"  ✅ VALIDATED: Prediction within 95% CI")
    else:
        print(f"  ⚠️ NOT VALIDATED: Prediction outside 95% CI")
    print()

    print("VORONOI CELL FACES:")
    print("-" * 50)
    print(f"  Observed mean: {faces_mean:.2f} ± {faces_sem:.2f}")
    print(f"  Prediction (BCC): {PREDICTED_VORONOI_FACES}")
    if faces_validated:
        print(f"  ✅ CONSISTENT with BCC topology")
    else:
        print(f"  ⚠️ DIFFERS from BCC prediction")
    print()

    print("PACKING FRACTION:")
    print("-" * 50)
    if len(all_packing) > 0:
        print(f"  Observed mean: {packing_mean:.4f} ± {packing_sem:.4f}")
        print(f"  Prediction (BCC): {PREDICTED_PACKING_BCC:.4f}")
        print(f"  Known values: FCC=0.74, BCC=0.68, RCP=0.64")
        if packing_validated:
            print(f"  ✅ CONSISTENT with BCC packing")
        else:
            print(f"  ⚠️ DIFFERS from BCC prediction")
    else:
        print("  Could not compute packing fractions")
    print()

    # Distribution analysis
    print("COORDINATION DISTRIBUTION:")
    print("-" * 50)
    for n_coord in range(5, 16):
        count = sum(1 for c in all_coordination if n_coord - 0.5 <= c < n_coord + 0.5)
        pct = count / len(all_coordination) * 100
        bar = "█" * int(pct / 2)
        print(f"  {n_coord:2d} neighbors: {pct:5.1f}% {bar}")
    print()

    # Summary
    print("=" * 70)
    print("Z² = 32π/3 VALIDATION SUMMARY")
    print("=" * 70)
    print()

    validated_count = sum([coord_validated, faces_validated, packing_validated])
    print(f"Tests passed: {validated_count}/3")
    print()

    if coord_validated:
        print("✅ Coordination number matches Z²/Vol(B³) = 8")
    else:
        print(f"❌ Coordination number ({coord_mean:.2f}) differs from prediction (8)")

    if faces_validated:
        print("✅ Voronoi faces consistent with BCC (14)")
    else:
        print(f"❌ Voronoi faces ({faces_mean:.1f}) differ from BCC prediction (14)")

    if packing_validated:
        print("✅ Packing fraction consistent with BCC (0.68)")
    else:
        print(f"❌ Packing fraction ({packing_mean:.3f}) differs from BCC (0.68)")

    # Create result object
    result = Z2ValidationVoronoi(
        timestamp=datetime.now().isoformat(),
        n_structures=len(results),
        total_interior_residues=sum(r.n_interior_residues for r in results),
        overall_mean_coordination=float(coord_mean),
        coordination_sem=float(coord_sem),
        coordination_ci_95=(float(coord_ci[0]), float(coord_ci[1])),
        coordination_prediction=PREDICTED_COORDINATION,
        coordination_p_value=float(p_coord),
        coordination_validated=bool(coord_validated),
        overall_mean_faces=float(faces_mean),
        faces_sem=float(faces_sem),
        faces_prediction=PREDICTED_VORONOI_FACES,
        faces_validated=bool(faces_validated),
        overall_mean_packing=float(packing_mean),
        packing_sem=float(packing_sem),
        packing_prediction=PREDICTED_PACKING_BCC,
        packing_validated=bool(packing_validated)
    )

    # Save results
    output_dir = Path(__file__).parent / "voronoi_analysis"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save summary
    summary = asdict(result)
    summary["structure_results"] = [asdict(r) for r in results]

    with open(output_dir / f"voronoi_validation_{timestamp}.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\nResults saved to: voronoi_analysis/voronoi_validation_{timestamp}.json")

    return result


if __name__ == "__main__":
    run_voronoi_validation(n_structures=50)
