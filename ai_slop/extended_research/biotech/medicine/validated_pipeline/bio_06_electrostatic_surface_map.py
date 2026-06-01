#!/usr/bin/env python3
"""
bio_06_electrostatic_surface_map.py

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

bio_06_electrostatic_surface_map.py - Emergent U(1) Gauge Field

Maps the electromagnetic field landscape around proteins.

Biology is governed by the U(1) electromagnetic gauge field operating
in a dielectric medium (water). The Poisson-Boltzmann equation describes
how charges distribute and fields propagate through this complex environment.

ε∇²φ = -ρ - κ²sinh(φ/kT)

where:
- ε = dielectric constant (2-4 inside protein, ~80 in water)
- φ = electrostatic potential
- ρ = charge density
- κ = Debye-Hückel screening parameter

Drug molecules must navigate this invisible electromagnetic landscape
to find their targets.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import urllib.request
from typing import Dict, List, Tuple

OUTPUT_DIR = Path(__file__).parent / "results" / "electrostatics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("ELECTROSTATIC SURFACE MAPPING")
print("The U(1) Gauge Field in Biological Media")
print("=" * 80)
print()

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Fundamental constants
ELECTRON_CHARGE = 1.602e-19  # Coulombs
AVOGADRO = 6.022e23
EPSILON_0 = 8.854e-12  # F/m
KB_SI = 1.381e-23  # J/K

# Dielectric constants
EPSILON_VACUUM = 1.0
EPSILON_PROTEIN = 4.0    # Low dielectric inside protein
EPSILON_MEMBRANE = 2.0   # Even lower in lipid
EPSILON_WATER = 78.5     # High dielectric in water (310K)

# Physiological conditions
TEMPERATURE = 310.0  # K
IONIC_STRENGTH = 0.15  # M (150 mM, physiological)

# Derived constants
KT = KB_SI * TEMPERATURE  # Thermal energy in J
KT_KCAL = 0.616  # kcal/mol at 310K

# Debye length (screening distance)
DEBYE_LENGTH = 7.8  # Å at 150 mM ionic strength

# Conversion factors
COULOMB_CONST = 332.0636  # kcal·Å/(mol·e²)

print(f"Temperature: {TEMPERATURE} K")
print(f"kT = {KT_KCAL:.3f} kcal/mol")
print(f"Ionic strength: {IONIC_STRENGTH} M")
print(f"Debye length: {DEBYE_LENGTH:.1f} Å")
print(f"ε(protein) = {EPSILON_PROTEIN}, ε(water) = {EPSILON_WATER}")
print()


# =============================================================================
# ATOMIC PARAMETERS
# =============================================================================

# Partial charges (AMBER ff14SB, simplified)
PARTIAL_CHARGES = {
    # Backbone
    'N': -0.4157, 'H': 0.2719, 'HN': 0.2719,
    'CA': 0.0337, 'HA': 0.0823,
    'C': 0.5973, 'O': -0.5679, 'OXT': -0.8055,
    # Sidechains (representative)
    'CB': -0.0825,
    'NZ': -0.3854, 'HZ': 0.34,  # Lys
    'OD1': -0.8014, 'OD2': -0.8014,  # Asp
    'OE1': -0.8188, 'OE2': -0.8188,  # Glu
    'NE': -0.5295, 'NH1': -0.8627, 'NH2': -0.8627,  # Arg
    'ND1': -0.3811, 'NE2': -0.5727,  # His
    'OG': -0.6546, 'OG1': -0.6761,  # Ser, Thr
    'SG': -0.2737,  # Cys
    'SD': -0.2737,  # Met
}

# VdW radii for surface calculation
VDW_RADII = {
    'C': 1.70, 'N': 1.55, 'O': 1.52, 'S': 1.80,
    'H': 1.20, 'P': 1.80, 'F': 1.47, 'CL': 1.75,
}


# =============================================================================
# PDB HANDLING
# =============================================================================

def download_pdb(pdb_id: str) -> Path:
    """Download PDB file from RCSB."""
    pdb_path = OUTPUT_DIR / f"{pdb_id}.pdb"
    if not pdb_path.exists():
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        print(f"Downloading {pdb_id}...")
        urllib.request.urlretrieve(url, pdb_path)
    return pdb_path


def parse_atoms_for_electrostatics(pdb_path: Path) -> List[Dict]:
    """
    Parse atoms with charges and radii for electrostatic calculation.
    """
    atoms = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    atom_name = line[12:16].strip()
                    res_name = line[17:20].strip()
                    chain = line[21]
                    res_num = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    element = line[76:78].strip() or atom_name[0]

                    # Get charge and radius
                    charge = PARTIAL_CHARGES.get(atom_name, 0.0)
                    radius = VDW_RADII.get(element, 1.70)

                    atoms.append({
                        'name': atom_name,
                        'res_name': res_name,
                        'chain': chain,
                        'res_num': res_num,
                        'coords': np.array([x, y, z]),
                        'element': element,
                        'charge': charge,
                        'radius': radius,
                    })

                except (ValueError, IndexError):
                    continue

    return atoms


# =============================================================================
# POISSON-BOLTZMANN SOLVER (Simplified)
# =============================================================================

def create_grid(atoms: List[Dict], padding: float = 10.0,
                 grid_spacing: float = 1.0) -> Tuple[np.ndarray, Dict]:
    """
    Create 3D grid around the protein for electrostatic calculation.
    """
    coords = np.array([a['coords'] for a in atoms])

    # Bounding box
    min_coords = coords.min(axis=0) - padding
    max_coords = coords.max(axis=0) + padding

    # Grid dimensions
    dims = np.ceil((max_coords - min_coords) / grid_spacing).astype(int)

    grid_info = {
        'origin': min_coords,
        'spacing': grid_spacing,
        'dims': dims,
        'n_points': np.prod(dims),
    }

    return np.zeros(dims), grid_info


def assign_dielectric(atoms: List[Dict], grid_shape: Tuple,
                       grid_info: Dict) -> np.ndarray:
    """
    Assign dielectric constant to each grid point.

    Points inside protein get low dielectric, outside get water dielectric.
    """
    epsilon = np.full(grid_shape, EPSILON_WATER)

    coords = np.array([a['coords'] for a in atoms])
    radii = np.array([a['radius'] for a in atoms])

    origin = grid_info['origin']
    spacing = grid_info['spacing']

    # For each grid point, check if inside any atom
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            for k in range(grid_shape[2]):
                point = origin + np.array([i, j, k]) * spacing

                # Distance to all atoms
                dists = np.linalg.norm(coords - point, axis=1)

                # Inside protein if within any atom's radius
                if np.any(dists < radii + 1.4):  # +1.4 for probe radius
                    epsilon[i, j, k] = EPSILON_PROTEIN

    return epsilon


def assign_charges(atoms: List[Dict], grid_shape: Tuple,
                    grid_info: Dict) -> np.ndarray:
    """
    Assign charges to grid points (simple Gaussian smearing).
    """
    rho = np.zeros(grid_shape)

    origin = grid_info['origin']
    spacing = grid_info['spacing']

    for atom in atoms:
        if abs(atom['charge']) < 0.01:
            continue

        # Find nearest grid point
        idx = np.round((atom['coords'] - origin) / spacing).astype(int)

        # Bounds check
        if np.all(idx >= 0) and np.all(idx < grid_shape):
            rho[idx[0], idx[1], idx[2]] += atom['charge']

    return rho


def solve_linearized_pb(rho: np.ndarray, epsilon: np.ndarray,
                         grid_info: Dict, n_iterations: int = 100,
                         tolerance: float = 1e-4) -> np.ndarray:
    """
    Solve linearized Poisson-Boltzmann equation using finite differences.

    ∇·(ε∇φ) = -ρ + κ²εφ

    Uses Gauss-Seidel iteration.
    """
    spacing = grid_info['spacing']
    dims = grid_info['dims']

    # Debye-Hückel parameter squared (in grid units)
    kappa2 = (1.0 / DEBYE_LENGTH) ** 2

    # Initialize potential
    phi = np.zeros(dims)

    # Prefactor for charge (convert to appropriate units)
    charge_factor = COULOMB_CONST / (4 * np.pi)

    print(f"  Solving Poisson-Boltzmann ({n_iterations} iterations)...")

    for iteration in range(n_iterations):
        phi_old = phi.copy()

        # Interior points only (skip boundaries)
        for i in range(1, dims[0]-1):
            for j in range(1, dims[1]-1):
                for k in range(1, dims[2]-1):
                    # Laplacian stencil
                    lap = (phi[i+1,j,k] + phi[i-1,j,k] +
                           phi[i,j+1,k] + phi[i,j-1,k] +
                           phi[i,j,k+1] + phi[i,j,k-1] - 6*phi[i,j,k])
                    lap /= spacing**2

                    # Source term
                    source = -charge_factor * rho[i,j,k] / epsilon[i,j,k]

                    # Screening term
                    screening = kappa2 * phi[i,j,k]

                    # Update
                    phi[i,j,k] = (source - lap * epsilon[i,j,k] / 6) / (1 + kappa2 * spacing**2 / 6)

        # Check convergence
        diff = np.max(np.abs(phi - phi_old))
        if diff < tolerance:
            print(f"    Converged at iteration {iteration+1}")
            break

    return phi


def compute_coulomb_potential(atoms: List[Dict], grid_info: Dict) -> np.ndarray:
    """
    Compute simple Coulomb potential (no dielectric, for comparison).
    """
    dims = grid_info['dims']
    origin = grid_info['origin']
    spacing = grid_info['spacing']

    phi = np.zeros(dims)

    print("  Computing Coulomb potential...")

    for atom in atoms:
        if abs(atom['charge']) < 0.01:
            continue

        q = atom['charge']
        r0 = atom['coords']

        for i in range(dims[0]):
            for j in range(dims[1]):
                for k in range(dims[2]):
                    point = origin + np.array([i, j, k]) * spacing
                    dist = np.linalg.norm(point - r0)

                    if dist > 1.0:  # Avoid singularity
                        phi[i, j, k] += COULOMB_CONST * q / (EPSILON_WATER * dist)

    return phi


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_electrostatic_surface(atoms: List[Dict], phi: np.ndarray,
                                    grid_info: Dict) -> Dict:
    """
    Analyze electrostatic potential on the molecular surface.
    """
    coords = np.array([a['coords'] for a in atoms])
    radii = np.array([a['radius'] for a in atoms])

    origin = grid_info['origin']
    spacing = grid_info['spacing']
    dims = grid_info['dims']

    # Sample potential at probe-accessible surface points
    surface_potentials = []
    surface_points = []

    probe_radius = 1.4  # Water probe

    # Generate surface points (simplified)
    for atom in atoms:
        r0 = atom['coords']
        r = atom['radius'] + probe_radius

        # Sample points on sphere
        for _ in range(20):
            # Random point on sphere
            theta = np.random.uniform(0, 2*np.pi)
            phi_angle = np.random.uniform(0, np.pi)

            point = r0 + r * np.array([
                np.sin(phi_angle) * np.cos(theta),
                np.sin(phi_angle) * np.sin(theta),
                np.cos(phi_angle)
            ])

            # Get potential at this point
            idx = np.round((point - origin) / spacing).astype(int)

            if np.all(idx >= 0) and np.all(idx < dims):
                potential = phi[idx[0], idx[1], idx[2]]
                surface_potentials.append(potential)
                surface_points.append(point)

    surface_potentials = np.array(surface_potentials)

    results = {
        'n_surface_points': len(surface_potentials),
        'mean_potential': float(np.mean(surface_potentials)),
        'std_potential': float(np.std(surface_potentials)),
        'min_potential': float(np.min(surface_potentials)),
        'max_potential': float(np.max(surface_potentials)),
        'positive_fraction': float(np.mean(surface_potentials > 0)),
        'negative_fraction': float(np.mean(surface_potentials < 0)),
    }

    # Identify charged regions
    positive_points = [surface_points[i] for i in range(len(surface_potentials))
                      if surface_potentials[i] > 1.0]
    negative_points = [surface_points[i] for i in range(len(surface_potentials))
                      if surface_potentials[i] < -1.0]

    results['n_positive_regions'] = len(positive_points)
    results['n_negative_regions'] = len(negative_points)

    return results


def save_dx_file(phi: np.ndarray, grid_info: Dict, output_path: Path):
    """
    Save potential grid in OpenDX format (for visualization).
    """
    dims = grid_info['dims']
    origin = grid_info['origin']
    spacing = grid_info['spacing']

    with open(output_path, 'w') as f:
        f.write(f"# Electrostatic potential from bio_06\n")
        f.write(f"object 1 class gridpositions counts {dims[0]} {dims[1]} {dims[2]}\n")
        f.write(f"origin {origin[0]:.3f} {origin[1]:.3f} {origin[2]:.3f}\n")
        f.write(f"delta {spacing:.3f} 0 0\n")
        f.write(f"delta 0 {spacing:.3f} 0\n")
        f.write(f"delta 0 0 {spacing:.3f}\n")
        f.write(f"object 2 class gridconnections counts {dims[0]} {dims[1]} {dims[2]}\n")
        f.write(f"object 3 class array type double rank 0 items {np.prod(dims)} data follows\n")

        # Write data
        count = 0
        for k in range(dims[2]):
            for j in range(dims[1]):
                for i in range(dims[0]):
                    f.write(f"{phi[i,j,k]:.6e} ")
                    count += 1
                    if count % 6 == 0:
                        f.write("\n")

        f.write(f'\nobject "potential" class field\n')

    return output_path


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def map_electrostatic_field(pdb_id: str, grid_spacing: float = 1.0) -> Dict:
    """
    Complete electrostatic analysis for a protein.
    """
    print(f"\n{'=' * 60}")
    print(f"ELECTROSTATIC MAPPING: {pdb_id}")
    print("=" * 60)

    # Load structure
    pdb_path = download_pdb(pdb_id)
    atoms = parse_atoms_for_electrostatics(pdb_path)

    print(f"  Loaded {len(atoms)} atoms")

    # Count charged atoms
    n_positive = sum(1 for a in atoms if a['charge'] > 0.5)
    n_negative = sum(1 for a in atoms if a['charge'] < -0.5)
    net_charge = sum(a['charge'] for a in atoms)

    print(f"  Positively charged atoms: {n_positive}")
    print(f"  Negatively charged atoms: {n_negative}")
    print(f"  Net charge: {net_charge:.2f} e")

    result = {
        'pdb_id': pdb_id,
        'n_atoms': len(atoms),
        'n_positive': n_positive,
        'n_negative': n_negative,
        'net_charge': float(net_charge),
        'timestamp': datetime.now().isoformat(),
    }

    # Create grid
    grid, grid_info = create_grid(atoms, padding=10.0, grid_spacing=grid_spacing)
    print(f"  Grid: {grid_info['dims']} ({grid_info['n_points']} points)")

    result['grid_dims'] = grid_info['dims'].tolist()
    result['grid_spacing'] = grid_spacing

    # Assign dielectric
    print("  Assigning dielectric constants...")
    epsilon = assign_dielectric(atoms, grid.shape, grid_info)

    protein_volume = np.sum(epsilon < EPSILON_WATER) * grid_spacing**3
    result['protein_volume_A3'] = float(protein_volume)
    print(f"  Protein volume: {protein_volume:.1f} Å³")

    # Assign charges
    rho = assign_charges(atoms, grid.shape, grid_info)

    # Solve P-B equation (simplified Coulomb for speed)
    phi = compute_coulomb_potential(atoms, grid_info)

    # Analyze surface
    surface_analysis = analyze_electrostatic_surface(atoms, phi, grid_info)
    result['surface'] = surface_analysis

    print(f"\n  SURFACE ELECTROSTATICS:")
    print(f"    Mean potential: {surface_analysis['mean_potential']:.3f} kcal/(mol·e)")
    print(f"    Range: [{surface_analysis['min_potential']:.2f}, {surface_analysis['max_potential']:.2f}]")
    print(f"    Positive fraction: {100*surface_analysis['positive_fraction']:.1f}%")
    print(f"    Negative fraction: {100*surface_analysis['negative_fraction']:.1f}%")

    # Save DX file
    dx_path = OUTPUT_DIR / f"{pdb_id}_potential.dx"
    save_dx_file(phi, grid_info, dx_path)
    result['dx_file'] = str(dx_path)
    print(f"\n  Potential grid: {dx_path}")

    # Interpretation
    print(f"\n  INTERPRETATION:")
    if net_charge > 2:
        print("    Protein is POSITIVELY charged")
        print("    Will attract negatively charged ligands")
    elif net_charge < -2:
        print("    Protein is NEGATIVELY charged")
        print("    Will attract positively charged ligands")
    else:
        print("    Protein is approximately NEUTRAL")
        print("    Electrostatic complementarity drives binding")

    return result


def main():
    """
    Map electrostatic fields for reference proteins.
    """
    proteins = [
        ('1PGB', 'Protein G B1 domain'),
        ('1UBQ', 'Ubiquitin'),
        ('1L2Y', 'Trp-cage miniprotein'),
    ]

    all_results = []

    for pdb_id, description in proteins:
        print(f"\n{description}")
        result = map_electrostatic_field(pdb_id, grid_spacing=1.0)
        result['description'] = description
        all_results.append(result)

    # Save results
    json_path = OUTPUT_DIR / "electrostatic_results.json"
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\nResults saved: {json_path}")

    # Summary
    print("\n" + "=" * 80)
    print("ELECTROSTATIC MAPPING SUMMARY")
    print("=" * 80)
    print()
    print("The U(1) gauge field (electromagnetism) governs:")
    print("  1. Protein-ligand recognition (charge complementarity)")
    print("  2. Binding specificity (electrostatic steering)")
    print("  3. Catalytic mechanisms (charge stabilization)")
    print("  4. Folding stability (salt bridges)")
    print()
    print("Drug molecules must navigate this invisible electromagnetic")
    print("landscape to find their targets. Electrostatic complementarity")
    print("is the primary determinant of molecular recognition.")
    print("=" * 80)

    return all_results


if __name__ == "__main__":
    main()
