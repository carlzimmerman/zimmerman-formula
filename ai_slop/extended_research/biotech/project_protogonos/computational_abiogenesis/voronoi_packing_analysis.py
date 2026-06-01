#!/usr/bin/env python3
"""
voronoi_packing_analysis.py

HIGH-FIDELITY VORONOI-BASED PACKING FRACTION CALCULATION

This script implements the proper Liang & Dill (2001) methodology:
f = V_atom / V_voronoi

where V_voronoi is the volume of the Voronoi cell around each atom,
NOT the convex hull volume.

Key insight: The literature value f ≈ 0.491 comes from:
1. Using atomic VdW volumes
2. Dividing by the SUM of individual Voronoi cell volumes
3. Only considering INTERIOR atoms (not surface)

Reference:
Liang, J. & Dill, K.A. (2001) "Are Proteins Well-Packed?"
Biophysical Journal 81:751-766

Author: Project Protogonos
Date: May 28, 2026
"""

import numpy as np
from scipy.spatial import Voronoi, ConvexHull, Delaunay
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
import urllib.request
import os

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # EXACTLY 32π/3
Z = np.sqrt(Z_SQUARED)       # 5.788810...
Z_OVER_12 = Z / 12           # 0.482401...

# Standard VdW radii (Bondi 1964, Rowland & Taylor 1996)
VDW_RADII = {
    'C': 1.70, 'N': 1.55, 'O': 1.52, 'S': 1.80,
    'P': 1.80, 'FE': 1.40, 'ZN': 1.39, 'MG': 1.73,
    'CA': 2.31, 'CL': 1.75, 'NA': 2.27, 'K': 2.75,
    'H': 1.20  # Include hydrogen for completeness
}
DEFAULT_RADIUS = 1.70

# =============================================================================
# PDB UTILITIES
# =============================================================================

def download_pdb(pdb_id: str, output_dir: str = '.') -> Optional[str]:
    """Download PDB file if not present."""
    pdb_id = pdb_id.lower()
    filepath = os.path.join(output_dir, f"{pdb_id}.pdb")

    if os.path.exists(filepath):
        return filepath

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        urllib.request.urlretrieve(url, filepath)
        return filepath
    except Exception as e:
        print(f"  [ERROR] Failed to download {pdb_id}: {e}")
        return None


def parse_pdb_atoms(filepath: str) -> Tuple[np.ndarray, List[str], List[str]]:
    """
    Parse PDB file and extract atom coordinates, elements, and residue info.

    Returns:
        coords: Nx3 array of coordinates
        elements: List of element symbols
        residues: List of residue names
    """
    coords = []
    elements = []
    residues = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    element = line[76:78].strip()
                    if not element:
                        # Infer from atom name
                        atom_name = line[12:16].strip()
                        element = atom_name[0]
                    residue = line[17:20].strip()

                    coords.append([x, y, z])
                    elements.append(element.upper())
                    residues.append(residue)
                except:
                    pass

    return np.array(coords), elements, residues


# =============================================================================
# VORONOI ANALYSIS
# =============================================================================

@dataclass
class VoronoiPackingResult:
    """Result container for Voronoi packing analysis."""
    f_global: float
    f_interior: float
    f_surface: float
    n_atoms: int
    n_interior: int
    n_surface: int
    A_global: float
    A_interior: float
    method: str
    uncertainty: float


def calculate_voronoi_cell_volume(vor: Voronoi, point_idx: int) -> Optional[float]:
    """
    Calculate the volume of the Voronoi cell for a specific point.

    Returns None if the cell is unbounded (surface atom).
    """
    region_idx = vor.point_region[point_idx]
    region = vor.regions[region_idx]

    # Check if cell is bounded
    if -1 in region or len(region) < 4:
        return None  # Unbounded cell (surface atom)

    try:
        vertices = vor.vertices[region]
        hull = ConvexHull(vertices)
        return hull.volume
    except:
        return None


def calculate_voronoi_packing(coords: np.ndarray, elements: List[str],
                               probe_radius: float = 1.4) -> VoronoiPackingResult:
    """
    Calculate packing fraction using Voronoi tessellation.

    This is the HIGH-FIDELITY method that should reproduce Liang & Dill f ≈ 0.49.

    Args:
        coords: Nx3 array of atom coordinates
        elements: List of element symbols
        probe_radius: Solvent probe radius for surface detection (Å)

    Returns:
        VoronoiPackingResult with interior and surface packing fractions
    """
    n_atoms = len(coords)

    # Get VdW radii for each atom
    radii = np.array([VDW_RADII.get(e.upper(), DEFAULT_RADIUS) for e in elements])

    # Calculate VdW volumes
    vdw_volumes = (4/3) * np.pi * radii**3

    # Compute Voronoi tessellation
    try:
        vor = Voronoi(coords)
    except Exception as e:
        print(f"  [WARNING] Voronoi tessellation failed: {e}")
        return VoronoiPackingResult(
            f_global=np.nan, f_interior=np.nan, f_surface=np.nan,
            n_atoms=n_atoms, n_interior=0, n_surface=n_atoms,
            A_global=np.nan, A_interior=np.nan,
            method='Voronoi (FAILED)', uncertainty=np.nan
        )

    # Calculate Voronoi cell volumes
    voronoi_volumes = []
    is_interior = []

    for i in range(n_atoms):
        vol = calculate_voronoi_cell_volume(vor, i)
        if vol is not None:
            voronoi_volumes.append(vol)
            is_interior.append(True)
        else:
            voronoi_volumes.append(np.nan)
            is_interior.append(False)

    voronoi_volumes = np.array(voronoi_volumes)
    is_interior = np.array(is_interior)

    n_interior = np.sum(is_interior)
    n_surface = n_atoms - n_interior

    # Calculate local packing fractions for interior atoms
    if n_interior > 0:
        interior_vdw = vdw_volumes[is_interior]
        interior_voronoi = voronoi_volumes[is_interior]

        # Local packing fraction: f_i = V_vdw_i / V_voronoi_i
        local_f = interior_vdw / interior_voronoi

        # Mean packing fraction (interior atoms only)
        f_interior = np.mean(local_f)
        σ_interior = np.std(local_f) / np.sqrt(n_interior)

        # Global packing fraction (total VdW / total Voronoi for interior)
        f_global_interior = np.sum(interior_vdw) / np.sum(interior_voronoi)
    else:
        f_interior = np.nan
        f_global_interior = np.nan
        σ_interior = np.nan

    # Surface atoms: Use a fallback (convex hull or average cell)
    if n_surface > 0 and n_interior > 0:
        # Estimate surface volume as average of interior
        avg_voronoi = np.nanmean(voronoi_volumes[is_interior])
        surface_vdw = np.sum(vdw_volumes[~is_interior])
        surface_voronoi_est = n_surface * avg_voronoi
        f_surface = surface_vdw / surface_voronoi_est
    else:
        f_surface = np.nan

    # Overall packing (weighted by number of atoms)
    if n_interior > 0:
        total_vdw = np.sum(vdw_volumes)
        if n_surface > 0:
            interior_voronoi_total = np.sum(interior_voronoi)
            surface_voronoi_total = n_surface * np.nanmean(voronoi_volumes[is_interior])
            total_voronoi = interior_voronoi_total + surface_voronoi_total
        else:
            total_voronoi = np.sum(interior_voronoi)
        f_global = total_vdw / total_voronoi
    else:
        f_global = np.nan

    # Calculate Aliveness Parameters
    A_global = ((f_global - Z_OVER_12) / Z_OVER_12) * 100 if not np.isnan(f_global) else np.nan
    A_interior = ((f_interior - Z_OVER_12) / Z_OVER_12) * 100 if not np.isnan(f_interior) else np.nan

    return VoronoiPackingResult(
        f_global=f_global,
        f_interior=f_interior,
        f_surface=f_surface,
        n_atoms=n_atoms,
        n_interior=n_interior,
        n_surface=n_surface,
        A_global=A_global,
        A_interior=A_interior,
        method='Voronoi tessellation (interior atoms only)',
        uncertainty=σ_interior if not np.isnan(σ_interior) else 0.05
    )


def calculate_local_packing_6A(coords: np.ndarray, elements: List[str],
                                center_idx: int, radius: float = 6.0) -> Dict:
    """
    Calculate local packing density within a 6 Å radius of a specific atom.

    This is the HIGH-FIDELITY method for mutational sensitivity analysis.

    Returns dictionary with local packing statistics.
    """
    center = coords[center_idx]
    distances = np.linalg.norm(coords - center, axis=1)

    # Select atoms within radius
    local_mask = distances <= radius
    n_local = np.sum(local_mask)

    if n_local < 4:
        return {
            'f_local': np.nan,
            'n_atoms': n_local,
            'status': 'INSUFFICIENT_ATOMS'
        }

    # Get local coordinates and elements
    local_coords = coords[local_mask]
    local_elements = [elements[i] for i in range(len(elements)) if local_mask[i]]

    # Calculate local Voronoi packing
    result = calculate_voronoi_packing(local_coords, local_elements)

    return {
        'f_local': result.f_interior,
        'n_atoms': n_local,
        'n_interior': result.n_interior,
        'A_local': result.A_interior,
        'status': 'COMPLETE'
    }


# =============================================================================
# THE LIANG-DILL REPRODUCTION TEST
# =============================================================================

def reproduce_liang_dill():
    """
    Attempt to reproduce the Liang & Dill (2001) result: f = 0.491 ± 0.015.

    They used 33 proteins (high-resolution, monomeric, no ligands).
    We'll test on a representative sample.
    """
    print("\n" + "=" * 70)
    print("LIANG & DILL (2001) REPRODUCTION TEST")
    print("=" * 70)
    print("""
    REFERENCE: Liang, J. & Dill, K.A. (2001) Biophys. J. 81:751-766

    Reported result: f = 0.491 ± 0.015 (n=33 proteins)

    METHOD:
    1. Voronoi tessellation of heavy atoms
    2. Only use INTERIOR atoms (bounded Voronoi cells)
    3. f = <V_vdw / V_voronoi>

    TEST STRUCTURES:
    - 1LYZ: Lysozyme (129 residues)
    - 1UBQ: Ubiquitin (76 residues)
    - 1CRN: Crambin (46 residues)
    """)

    test_structures = {
        '1lyz': {'name': 'Lysozyme', 'residues': 129},
        '1ubq': {'name': 'Ubiquitin', 'residues': 76},
        '1crn': {'name': 'Crambin', 'residues': 46}
    }

    results = []

    for pdb_id, info in test_structures.items():
        print(f"\n  Processing {pdb_id.upper()} ({info['name']})...")

        filepath = download_pdb(pdb_id)
        if filepath is None:
            continue

        coords, elements, residues = parse_pdb_atoms(filepath)

        # Filter to heavy atoms only (no H)
        heavy_mask = np.array([e != 'H' for e in elements])
        coords_heavy = coords[heavy_mask]
        elements_heavy = [e for e, m in zip(elements, heavy_mask) if m]

        print(f"    Heavy atoms: {len(coords_heavy)}")

        # Calculate Voronoi packing
        result = calculate_voronoi_packing(coords_heavy, elements_heavy)

        print(f"    f_global:   {result.f_global:.4f}")
        print(f"    f_interior: {result.f_interior:.4f}")
        print(f"    Interior atoms: {result.n_interior}/{result.n_atoms}")
        print(f"    A_interior: {result.A_interior:+.2f}%")

        results.append({
            'pdb': pdb_id,
            'name': info['name'],
            'f_interior': result.f_interior,
            'A_interior': result.A_interior,
            'n_interior': result.n_interior,
            'n_atoms': result.n_atoms
        })

    # Summary
    if results:
        f_values = [r['f_interior'] for r in results if not np.isnan(r['f_interior'])]

        if f_values:
            f_mean = np.mean(f_values)
            f_std = np.std(f_values)
            f_sem = f_std / np.sqrt(len(f_values))

            print("\n" + "-" * 70)
            print("  SUMMARY")
            print("-" * 70)
            print(f"    Mean f_interior: {f_mean:.4f} ± {f_sem:.4f}")
            print(f"    Literature value: 0.491 ± 0.015")
            print(f"    Deviation: {abs(f_mean - 0.491):.4f}")

            A_mean = ((f_mean - Z_OVER_12) / Z_OVER_12) * 100
            print(f"\n    Mean A: {A_mean:+.2f}%")
            print(f"    Expected A: +1.78%")

            if abs(f_mean - 0.491) < 0.05:
                print("\n    ✓ WITHIN ACCEPTABLE RANGE of literature value")
            else:
                print("\n    ⚠ SIGNIFICANT DEVIATION from literature value")
                print("      Possible causes:")
                print("      - Different atom selection criteria")
                print("      - Different VdW radii database")
                print("      - Numerical precision in Voronoi calculation")

    return results


# =============================================================================
# THERMAL SCALING WITH VORONOI
# =============================================================================

def thermal_voronoi_comparison():
    """
    Compare Voronoi packing at 100K vs 278K using proper methodology.

    Structures: 5KXK (100K), 5KXW (278K) from same crystal form
    """
    print("\n" + "=" * 70)
    print("THERMAL SCALING - VORONOI METHOD")
    print("=" * 70)
    print("""
    PREDICTION: If Z² thermal scaling is valid:
      f(T) = (Z/12) × (1 + k_B T / E_fold)

    Expected A values:
      A(100K) ≈ 2.1%
      A(278K) ≈ 5.8%
      ΔA ≈ +3.7%

    STRUCTURES:
      5KXK: Hen egg-white lysozyme at 100 K
      5KXW: Hen egg-white lysozyme at 278 K
    """)

    structures = {
        '5kxk': {'temp': 100, 'desc': 'Cryo'},
        '5kxw': {'temp': 278, 'desc': 'Near-RT'}
    }

    results = {}

    for pdb_id, info in structures.items():
        print(f"\n  Processing {pdb_id.upper()} ({info['desc']}, {info['temp']}K)...")

        filepath = download_pdb(pdb_id)
        if filepath is None:
            continue

        coords, elements, residues = parse_pdb_atoms(filepath)

        # Filter to heavy atoms
        heavy_mask = np.array([e != 'H' for e in elements])
        coords_heavy = coords[heavy_mask]
        elements_heavy = [e for e, m in zip(elements, heavy_mask) if m]

        print(f"    Heavy atoms: {len(coords_heavy)}")

        # Calculate Voronoi packing
        result = calculate_voronoi_packing(coords_heavy, elements_heavy)

        print(f"    f_interior: {result.f_interior:.4f} ± {result.uncertainty:.4f}")
        print(f"    A_interior: {result.A_interior:+.2f}%")
        print(f"    Interior atoms: {result.n_interior}/{result.n_atoms}")

        results[pdb_id] = {
            'temp': info['temp'],
            'f': result.f_interior,
            'A': result.A_interior,
            'σ': result.uncertainty,
            'n_interior': result.n_interior
        }

    # Thermal analysis
    if len(results) == 2:
        cryo = results['5kxk']
        warm = results['5kxw']

        ΔA = warm['A'] - cryo['A']
        ΔT = warm['temp'] - cryo['temp']
        dA_dT = ΔA / ΔT

        print("\n" + "-" * 70)
        print("  THERMAL SCALING RESULT")
        print("-" * 70)
        print(f"    A(100K): {cryo['A']:+.2f}%")
        print(f"    A(278K): {warm['A']:+.2f}%")
        print(f"    ΔA: {ΔA:+.2f}%")
        print(f"    dA/dT: {dA_dT:.4f} %/K")

        # Z² prediction
        k_B_eV = 8.617e-5
        E_fold_eV = 0.41
        ΔA_predicted = (k_B_eV / E_fold_eV) * ΔT * 100

        print(f"\n    Z² Predicted ΔA: +{ΔA_predicted:.2f}%")

        if dA_dT > 0:
            print("\n    RESULT: A increases with T ✓")
        else:
            print("\n    RESULT: A decreases with T ✗ (contradicts Z² model)")

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("VORONOI PACKING ANALYSIS - HIGH FIDELITY MODE")
    print("=" * 70)
    print(f"\n  Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"  Z = √(32π/3) = {Z:.6f} Å")
    print(f"  Z/12 = {Z_OVER_12:.6f} (Platonic Ideal packing)")

    # 1. Reproduce Liang & Dill
    ld_results = reproduce_liang_dill()

    # 2. Thermal comparison
    thermal_results = thermal_voronoi_comparison()

    # Save results
    all_results = {
        'liang_dill_reproduction': ld_results,
        'thermal_scaling': thermal_results,
        'Z_constants': {
            'Z_squared': Z_SQUARED,
            'Z': Z,
            'Z_over_12': Z_OVER_12
        }
    }

    with open('voronoi_packing_results.json', 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print("\n" + "=" * 70)
    print("Results saved to: voronoi_packing_results.json")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    main()
