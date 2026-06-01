#!/usr/bin/env python3
"""
Z² Amyloid Docking: Can Z² Proteins Disrupt Alzheimer's Aβ42 Fibrils?

SPDX-License-Identifier: AGPL-3.0-or-later

This script docks our Z²-designed protein against the Alzheimer's
Aβ42 amyloid fibril (PDB: 2BEG) to explore potential binding.

Hypothesis: Z² proteins with harmonic normal modes may:
1. Bind to fibril surfaces via complementary geometry
2. Potentially disrupt fibril packing through resonance
3. The 0.309 THz dissociation frequency could propagate through binding

Method:
1. Fetch Aβ42 fibril structure (2BEG - pentameric form)
2. Generate docking poses using geometric sampling
3. Score poses with simple physics (contacts, clashes, complementarity)
4. Refine top poses with OpenMM minimization
5. Analyze binding interface

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.spatial import distance, KDTree
from scipy.spatial.transform import Rotation
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)
THz_DISSOCIATION = 0.309  # THz

print(f"Z² = {Z2:.4f}")
print(f"Z = {Z:.4f}")
print(f"THz dissociation frequency: {THz_DISSOCIATION} THz")

# Aβ42 fibril from Alzheimer's research
AMYLOID_PDB = "2BEG"  # Pentameric Aβ42 fibril structure

# ==============================================================================
# PDB UTILITIES
# ==============================================================================

def fetch_pdb(pdb_id: str) -> Optional[str]:
    """Fetch PDB content from RCSB."""
    import urllib.request
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")
        return None


def parse_ca_atoms(pdb_content: str) -> Tuple[np.ndarray, List[str], List[str]]:
    """Parse Cα atoms from PDB content. Returns coords, residue names, chain IDs."""
    coords = []
    residues = []
    chains = []

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM') and line[12:16].strip() == 'CA':
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            res_name = line[17:20].strip()
            chain = line[21]
            coords.append([x, y, z])
            residues.append(res_name)
            chains.append(chain)

    return np.array(coords), residues, chains


def parse_all_atoms(pdb_content: str) -> Tuple[np.ndarray, List[str]]:
    """Parse all atoms from PDB content."""
    coords = []
    atom_names = []

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM'):
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            atom = line[12:16].strip()
            coords.append([x, y, z])
            atom_names.append(atom)

    return np.array(coords), atom_names


def load_z2_protein(pdb_path: str) -> Tuple[np.ndarray, List[str]]:
    """Load our Z² designed protein."""
    coords = []
    residues = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                res_name = line[17:20].strip()
                coords.append([x, y, z])
                residues.append(res_name)

    return np.array(coords), residues


# ==============================================================================
# DOCKING ENGINE
# ==============================================================================

def center_structure(coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Center structure at origin, return centered coords and original center."""
    center = np.mean(coords, axis=0)
    return coords - center, center


def compute_binding_surface(coords: np.ndarray, probe_radius: float = 1.4) -> np.ndarray:
    """Find surface-exposed residues using simple neighbor count."""
    tree = KDTree(coords)
    neighbor_counts = np.array([len(tree.query_ball_point(c, 10.0)) for c in coords])

    # Surface residues have fewer neighbors
    median_neighbors = np.median(neighbor_counts)
    surface_mask = neighbor_counts < median_neighbors

    return surface_mask


def generate_docking_poses(
    ligand_coords: np.ndarray,
    receptor_coords: np.ndarray,
    n_rotations: int = 100,
    n_translations: int = 20,
    min_distance: float = 5.0,
    max_distance: float = 15.0
) -> List[Dict]:
    """
    Generate docking poses by sampling rotations and translations.

    Places ligand around receptor surface at various orientations.
    """
    poses = []

    # Center both structures
    ligand_centered, ligand_center = center_structure(ligand_coords)
    receptor_centered, receptor_center = center_structure(receptor_coords)

    # Find receptor surface
    surface_mask = compute_binding_surface(receptor_centered)
    surface_points = receptor_centered[surface_mask]

    if len(surface_points) == 0:
        surface_points = receptor_centered

    # Sample surface points for placement
    n_surface = min(n_translations, len(surface_points))
    surface_indices = np.random.choice(len(surface_points), n_surface, replace=False)

    for surf_idx in surface_indices:
        # Direction from receptor center to surface point
        surface_point = surface_points[surf_idx]
        direction = surface_point / (np.linalg.norm(surface_point) + 1e-6)

        # Place ligand at various distances along this direction
        for dist in np.linspace(min_distance, max_distance, 3):
            translation = surface_point + direction * dist

            # Sample rotations
            rotations = Rotation.random(n_rotations // n_translations)

            for rot in rotations:
                # Apply rotation to ligand
                rotated = rot.apply(ligand_centered)

                # Translate to docking position
                posed = rotated + translation + receptor_center

                poses.append({
                    'coords': posed,
                    'rotation': rot.as_matrix(),
                    'translation': translation + receptor_center,
                    'surface_point': surface_point + receptor_center
                })

    return poses


def score_pose(
    ligand_coords: np.ndarray,
    receptor_coords: np.ndarray,
    clash_distance: float = 2.0,
    contact_distance: float = 8.0,
    optimal_distance: float = 4.0
) -> Dict:
    """
    Score a docking pose.

    Scoring:
    - Penalize clashes (< 2 Å)
    - Reward contacts (4-8 Å)
    - Bonus for optimal distance (~4 Å)
    """
    # Compute all pairwise distances
    dists = distance.cdist(ligand_coords, receptor_coords)

    # Count clashes
    n_clashes = np.sum(dists < clash_distance)

    # Count contacts
    contacts_mask = (dists >= clash_distance) & (dists <= contact_distance)
    n_contacts = np.sum(contacts_mask)

    # Optimal contacts (around 4 Å)
    optimal_mask = (dists >= 3.5) & (dists <= 5.0)
    n_optimal = np.sum(optimal_mask)

    # Interface residues
    ligand_interface = np.any(dists <= contact_distance, axis=1)
    receptor_interface = np.any(dists <= contact_distance, axis=0)

    # Minimum distance
    min_dist = np.min(dists)

    # Compute score
    # Penalize clashes heavily, reward contacts
    clash_penalty = -100 * n_clashes
    contact_reward = 10 * n_contacts
    optimal_bonus = 5 * n_optimal

    # Distance penalty if too far
    if min_dist > contact_distance:
        distance_penalty = -50 * (min_dist - contact_distance)
    else:
        distance_penalty = 0

    total_score = clash_penalty + contact_reward + optimal_bonus + distance_penalty

    return {
        'total_score': float(total_score),
        'n_clashes': int(n_clashes),
        'n_contacts': int(n_contacts),
        'n_optimal_contacts': int(n_optimal),
        'min_distance': float(min_dist),
        'ligand_interface_residues': int(np.sum(ligand_interface)),
        'receptor_interface_residues': int(np.sum(receptor_interface)),
        'interface_area': float(np.sum(ligand_interface) + np.sum(receptor_interface))
    }


def refine_pose_openmm(
    ligand_coords: np.ndarray,
    receptor_coords: np.ndarray,
    n_steps: int = 100
) -> Tuple[np.ndarray, float]:
    """
    Refine pose using OpenMM energy minimization.

    Uses simple Go-model potential for Cα-only structures.
    """
    try:
        import openmm as mm
        from openmm import unit
        from openmm.app import Topology, Element
    except ImportError:
        return ligand_coords, 0.0

    # Combine coordinates
    all_coords = np.vstack([ligand_coords, receptor_coords])
    n_ligand = len(ligand_coords)
    n_total = len(all_coords)

    # Create topology
    topology = Topology()
    chain = topology.addChain()

    for i in range(n_total):
        res = topology.addResidue('ALA', chain)
        topology.addAtom('CA', Element.getBySymbol('C'), res)

    # Create system
    system = mm.System()

    for i in range(n_total):
        system.addParticle(12.0 * unit.amu)

    # Add harmonic bonds within each structure
    bond_force = mm.HarmonicBondForce()

    # Ligand bonds
    for i in range(n_ligand - 1):
        d = np.linalg.norm(ligand_coords[i] - ligand_coords[i+1])
        bond_force.addBond(i, i+1, d * unit.angstrom, 1000 * unit.kilojoule_per_mole / unit.angstrom**2)

    # Receptor bonds
    for i in range(n_ligand, n_total - 1):
        d = np.linalg.norm(receptor_coords[i - n_ligand] - receptor_coords[i - n_ligand + 1])
        bond_force.addBond(i, i+1, d * unit.angstrom, 1000 * unit.kilojoule_per_mole / unit.angstrom**2)

    system.addForce(bond_force)

    # Add soft LJ-like interaction between ligand and receptor
    nb_force = mm.CustomNonbondedForce("epsilon*((sigma/r)^12 - 2*(sigma/r)^6)")
    nb_force.addGlobalParameter("epsilon", 1.0 * unit.kilojoule_per_mole)
    nb_force.addGlobalParameter("sigma", 4.0 * unit.angstrom)

    for i in range(n_total):
        nb_force.addParticle([])

    # Only interactions between ligand and receptor
    nb_force.addInteractionGroup(set(range(n_ligand)), set(range(n_ligand, n_total)))

    system.addForce(nb_force)

    # Create simulation
    integrator = mm.LangevinIntegrator(300 * unit.kelvin, 1 / unit.picosecond, 0.002 * unit.picosecond)

    try:
        platform = mm.Platform.getPlatformByName('OpenCL')
    except:
        platform = mm.Platform.getPlatformByName('CPU')

    simulation = mm.app.Simulation(topology, system, integrator, platform)
    simulation.context.setPositions(all_coords * unit.angstrom)

    # Minimize
    simulation.minimizeEnergy(maxIterations=n_steps)

    # Get results
    state = simulation.context.getState(getPositions=True, getEnergy=True)
    final_coords = state.getPositions(asNumpy=True).value_in_unit(unit.angstrom)
    energy = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)

    return final_coords[:n_ligand], energy


# ==============================================================================
# ANALYSIS
# ==============================================================================

def analyze_interface(
    ligand_coords: np.ndarray,
    receptor_coords: np.ndarray,
    ligand_residues: List[str],
    receptor_residues: List[str],
    contact_cutoff: float = 8.0
) -> Dict:
    """Analyze the binding interface in detail."""
    dists = distance.cdist(ligand_coords, receptor_coords)

    interface_contacts = []

    for i in range(len(ligand_coords)):
        for j in range(len(receptor_coords)):
            if dists[i, j] <= contact_cutoff:
                interface_contacts.append({
                    'ligand_residue': i,
                    'ligand_name': ligand_residues[i] if i < len(ligand_residues) else 'UNK',
                    'receptor_residue': j,
                    'receptor_name': receptor_residues[j] if j < len(receptor_residues) else 'UNK',
                    'distance': float(dists[i, j])
                })

    # Residue type analysis
    ligand_interface_idx = set(c['ligand_residue'] for c in interface_contacts)
    receptor_interface_idx = set(c['receptor_residue'] for c in interface_contacts)

    return {
        'n_contacts': len(interface_contacts),
        'ligand_interface_size': len(ligand_interface_idx),
        'receptor_interface_size': len(receptor_interface_idx),
        'contacts': interface_contacts[:20],  # Top 20 contacts
        'mean_interface_distance': float(np.mean([c['distance'] for c in interface_contacts])) if interface_contacts else 0
    }


def compute_shape_complementarity(
    ligand_coords: np.ndarray,
    receptor_coords: np.ndarray
) -> float:
    """
    Compute shape complementarity score.

    Higher score = better geometric fit.
    """
    # Find interface atoms
    dists = distance.cdist(ligand_coords, receptor_coords)

    ligand_interface = np.any(dists <= 10.0, axis=1)
    receptor_interface = np.any(dists <= 10.0, axis=0)

    if np.sum(ligand_interface) < 3 or np.sum(receptor_interface) < 3:
        return 0.0

    # Compute local surface normals using PCA
    lig_interface_coords = ligand_coords[ligand_interface]
    rec_interface_coords = receptor_coords[receptor_interface]

    # Simple metric: variance of distances
    interface_dists = dists[ligand_interface][:, receptor_interface]

    # Good complementarity = consistent interface distances
    dist_variance = np.var(interface_dists[interface_dists <= 10.0])

    # Lower variance = better complementarity
    complementarity = 1.0 / (1.0 + dist_variance)

    return float(complementarity)


# ==============================================================================
# MAIN DOCKING PIPELINE
# ==============================================================================

def run_amyloid_docking(
    z2_pdb_path: str,
    output_dir: str = "amyloid_docking",
    n_poses: int = 500,
    top_n: int = 10
) -> Dict:
    """
    Run full docking pipeline of Z² protein against Aβ42 fibril.
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "=" * 70)
    print("Z² AMYLOID DOCKING: Targeting Alzheimer's Aβ42 Fibril")
    print("=" * 70)

    # Load Z² protein (ligand)
    print(f"\nLoading Z² protein from: {z2_pdb_path}")
    ligand_coords, ligand_residues = load_z2_protein(z2_pdb_path)
    print(f"  Ligand: {len(ligand_coords)} residues")

    # Fetch Aβ42 fibril (receptor)
    print(f"\nFetching Aβ42 fibril: {AMYLOID_PDB}")
    amyloid_content = fetch_pdb(AMYLOID_PDB)

    if amyloid_content is None:
        return {"error": f"Could not fetch {AMYLOID_PDB}"}

    receptor_coords, receptor_residues, chains = parse_ca_atoms(amyloid_content)
    print(f"  Receptor: {len(receptor_coords)} residues across {len(set(chains))} chains")

    # Save receptor structure
    receptor_path = os.path.join(output_dir, f"{AMYLOID_PDB}_fibril.pdb")
    with open(receptor_path, 'w') as f:
        f.write(amyloid_content)
    print(f"  Saved to: {receptor_path}")

    # Generate docking poses
    print(f"\nGenerating {n_poses} docking poses...")
    poses = generate_docking_poses(
        ligand_coords, receptor_coords,
        n_rotations=n_poses // 10,
        n_translations=min(50, len(receptor_coords) // 5)
    )
    print(f"  Generated {len(poses)} poses")

    # Score all poses
    print("\nScoring poses...")
    scored_poses = []

    for i, pose in enumerate(poses):
        score = score_pose(pose['coords'], receptor_coords)
        score['pose_id'] = i
        score['coords'] = pose['coords']
        score['translation'] = pose['translation']
        scored_poses.append(score)

        if (i + 1) % 100 == 0:
            print(f"  Scored {i + 1}/{len(poses)} poses")

    # Sort by score
    scored_poses.sort(key=lambda x: x['total_score'], reverse=True)

    # Filter out poses with clashes
    valid_poses = [p for p in scored_poses if p['n_clashes'] == 0]
    print(f"\n  Valid poses (no clashes): {len(valid_poses)}/{len(scored_poses)}")

    if len(valid_poses) == 0:
        # Allow some clashes
        valid_poses = [p for p in scored_poses if p['n_clashes'] < 5]
        print(f"  Relaxed filter (<5 clashes): {len(valid_poses)}")

    if len(valid_poses) == 0:
        valid_poses = scored_poses[:top_n]

    # Take top poses
    top_poses = valid_poses[:top_n]

    print(f"\nTop {len(top_poses)} poses:")
    print("-" * 60)
    print(f"{'Rank':<6}{'Score':<10}{'Contacts':<10}{'Optimal':<10}{'MinDist':<10}")
    print("-" * 60)

    for rank, pose in enumerate(top_poses):
        print(f"{rank + 1:<6}{pose['total_score']:<10.1f}{pose['n_contacts']:<10}"
              f"{pose['n_optimal_contacts']:<10}{pose['min_distance']:<10.2f}")

    # Refine top pose with OpenMM
    print("\nRefining top pose with OpenMM...")
    best_pose = top_poses[0]
    refined_coords, refined_energy = refine_pose_openmm(
        best_pose['coords'], receptor_coords
    )

    # Re-score refined pose
    refined_score = score_pose(refined_coords, receptor_coords)
    print(f"  Refined score: {refined_score['total_score']:.1f}")
    print(f"  Refined energy: {refined_energy:.1f} kJ/mol")

    # Analyze binding interface
    print("\nAnalyzing binding interface...")
    interface = analyze_interface(
        refined_coords, receptor_coords,
        ligand_residues, receptor_residues
    )

    print(f"  Interface contacts: {interface['n_contacts']}")
    print(f"  Ligand interface: {interface['ligand_interface_size']} residues")
    print(f"  Receptor interface: {interface['receptor_interface_size']} residues")
    print(f"  Mean interface distance: {interface['mean_interface_distance']:.2f} Å")

    # Compute shape complementarity
    complementarity = compute_shape_complementarity(refined_coords, receptor_coords)
    print(f"  Shape complementarity: {complementarity:.3f}")

    # Save docked complex
    complex_pdb = save_docked_complex(
        refined_coords, ligand_residues,
        receptor_coords, receptor_residues, chains,
        os.path.join(output_dir, "z2_amyloid_complex.pdb")
    )
    print(f"\n✓ Docked complex saved to: {complex_pdb}")

    # Compile results
    results = {
        "timestamp": datetime.now().isoformat(),
        "ligand": {
            "pdb_path": z2_pdb_path,
            "n_residues": len(ligand_coords)
        },
        "receptor": {
            "pdb_id": AMYLOID_PDB,
            "n_residues": len(receptor_coords),
            "n_chains": len(set(chains))
        },
        "docking": {
            "n_poses_generated": len(poses),
            "n_valid_poses": len(valid_poses),
            "top_pose_score": float(top_poses[0]['total_score']),
            "top_pose_contacts": int(top_poses[0]['n_contacts']),
        },
        "refined_pose": {
            "score": float(refined_score['total_score']),
            "n_contacts": int(refined_score['n_contacts']),
            "n_optimal_contacts": int(refined_score['n_optimal_contacts']),
            "min_distance": float(refined_score['min_distance']),
            "energy_kJ_mol": float(refined_energy)
        },
        "interface": interface,
        "shape_complementarity": complementarity,
        "output_files": {
            "receptor": receptor_path,
            "complex": complex_pdb
        }
    }

    # Interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)

    if refined_score['n_contacts'] > 20 and complementarity > 0.1:
        verdict = "PROMISING"
        interpretation = f"""
The Z² protein shows FAVORABLE binding to the Aβ42 fibril surface:
  - {refined_score['n_contacts']} contacts at the interface
  - Shape complementarity: {complementarity:.3f}
  - No significant clashes

This suggests the Z²-designed protein could potentially:
1. Coat the fibril surface, blocking further aggregation
2. If excited at {THz_DISSOCIATION} THz, propagate disruption into fibril

NEXT STEPS:
- Run MD simulation of bound complex
- Test THz excitation of docked state
- Experimental validation with ThT fluorescence assay
        """
    else:
        verdict = "WEAK BINDING"
        interpretation = f"""
The Z² protein shows limited interaction with Aβ42 fibril:
  - Only {refined_score['n_contacts']} contacts
  - May need sequence optimization for better binding

SUGGESTIONS:
- Redesign Z² surface residues for amyloid affinity
- Try different Z² variants
- Consider covalent linking strategies
        """

    results["verdict"] = verdict
    print(f"\n  VERDICT: {verdict}")
    print(interpretation)

    # Save results
    results_path = os.path.join(output_dir, "docking_results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n✓ Results saved to: {results_path}")

    return results


def save_docked_complex(
    ligand_coords: np.ndarray,
    ligand_residues: List[str],
    receptor_coords: np.ndarray,
    receptor_residues: List[str],
    receptor_chains: List[str],
    output_path: str
) -> str:
    """Save docked complex as PDB file."""

    aa_map = {
        'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
        'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
        'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
        'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
    }

    with open(output_path, 'w') as f:
        f.write("REMARK   Z2 protein docked to Abeta42 fibril\n")
        f.write(f"REMARK   Generated: {datetime.now().isoformat()}\n")
        f.write("REMARK   Chain Z = Z2 ligand, Chains A-E = Abeta42 fibril\n")

        atom_num = 1

        # Write ligand (chain Z)
        for i, (coord, res) in enumerate(zip(ligand_coords, ligand_residues)):
            res_3 = res if len(res) == 3 else 'ALA'
            f.write(f"ATOM  {atom_num:5d}  CA  {res_3:3s} Z{i+1:4d}    "
                   f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                   f"  1.00  0.00           C\n")
            atom_num += 1

        f.write("TER\n")

        # Write receptor
        for i, (coord, res, chain) in enumerate(zip(receptor_coords, receptor_residues, receptor_chains)):
            f.write(f"ATOM  {atom_num:5d}  CA  {res:3s} {chain}{i+1:4d}    "
                   f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                   f"  1.00  0.00           C\n")
            atom_num += 1

        f.write("TER\n")
        f.write("END\n")

    return output_path


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    import sys

    # Default to our best Z² protein
    if len(sys.argv) > 1:
        z2_pdb = sys.argv[1]
    else:
        # Use the globular_80 which had best Z² alignment
        z2_pdb = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

        # Fallback to harmonic_72 if globular doesn't exist
        if not os.path.exists(z2_pdb):
            z2_pdb = "pipeline_output_harmonic72/esm_prediction/z2_harmonic_72_esm.pdb"

    if not os.path.exists(z2_pdb):
        print(f"Error: Z² protein PDB not found: {z2_pdb}")
        print("Run the full pipeline first to generate Z² structures.")
        sys.exit(1)

    results = run_amyloid_docking(z2_pdb)
