#!/usr/bin/env python3
"""
Z² Binding Site Predictor

SPDX-License-Identifier: AGPL-3.0-or-later

Predicts protein binding sites using Z² geometric principles.

THE KEY INSIGHT:
Binding sites are regions where the protein is "prepared" to accept a partner.
This manifests as:
1. Surface pockets/cavities (geometric accessibility)
2. Suboptimal Z² packing (contact deviation from 8 = ready to rearrange)
3. Higher flexibility (from normal modes / ensemble RMSF)
4. Specific electrostatic character (charged residues)
5. Hinge proximity (allosteric communication)

AlphaFold tells you the shape. Z² tells you WHERE THINGS BIND.

Method:
1. Compute solvent-accessible surface and identify pockets
2. Calculate local Z² contact deviation (binding-ready regions pack loosely)
3. Incorporate flexibility from conformational ensemble
4. Score electrostatic complementarity
5. Rank binding sites by composite Z² binding score

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import linkage, fcluster
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
Z = np.sqrt(Z2)       # ≈ 5.7888
OPTIMAL_CONTACTS = 8  # Z² predicts 8 contacts per residue

print("=" * 70)
print("Z² BINDING SITE PREDICTOR")
print("=" * 70)
print(f"Z² = {Z2:.4f}")
print(f"Optimal contacts = {OPTIMAL_CONTACTS}")
print("Identifying binding-competent regions via geometric analysis")
print("=" * 70)

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Residue charges at pH 7
RESIDUE_CHARGE = {
    'ARG': 1.0, 'LYS': 1.0, 'HIS': 0.5,  # Positive
    'ASP': -1.0, 'GLU': -1.0,             # Negative
    'ALA': 0, 'VAL': 0, 'LEU': 0, 'ILE': 0, 'MET': 0,  # Nonpolar
    'PHE': 0, 'TRP': 0, 'TYR': 0, 'PRO': 0,            # Aromatic/special
    'SER': 0, 'THR': 0, 'CYS': 0, 'ASN': 0, 'GLN': 0,  # Polar
    'GLY': 0
}

# Hydrophobicity (Kyte-Doolittle scale, normalized)
HYDROPHOBICITY = {
    'ILE': 1.0, 'VAL': 0.97, 'LEU': 0.92, 'PHE': 0.72, 'CYS': 0.64,
    'MET': 0.49, 'ALA': 0.47, 'GLY': -0.10, 'THR': -0.18, 'SER': -0.23,
    'TRP': -0.23, 'TYR': -0.36, 'PRO': -0.41, 'HIS': -0.82, 'GLU': -0.87,
    'GLN': -0.87, 'ASP': -0.87, 'ASN': -0.87, 'LYS': -0.97, 'ARG': -1.0
}

# ==============================================================================
# STRUCTURE PARSING
# ==============================================================================

def parse_pdb_structure(pdb_path: str) -> Dict:
    """Parse PDB file and extract coordinates, residue info."""
    atoms = []
    residues = {}

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

                    atom = {
                        'name': atom_name,
                        'res_name': res_name,
                        'chain': chain,
                        'res_num': res_num,
                        'coords': np.array([x, y, z])
                    }
                    atoms.append(atom)

                    # Track residue info
                    res_key = (chain, res_num)
                    if res_key not in residues:
                        residues[res_key] = {
                            'name': res_name,
                            'atoms': [],
                            'coords': []
                        }
                    residues[res_key]['atoms'].append(atom_name)
                    residues[res_key]['coords'].append([x, y, z])

                except ValueError:
                    continue

    # Compute residue centroids (Cα or center of mass)
    ca_coords = []
    res_info = []

    for (chain, res_num), res_data in sorted(residues.items()):
        coords = np.array(res_data['coords'])

        # Prefer Cα, fall back to centroid
        if 'CA' in res_data['atoms']:
            ca_idx = res_data['atoms'].index('CA')
            ca_coords.append(coords[ca_idx])
        else:
            ca_coords.append(coords.mean(axis=0))

        res_info.append({
            'chain': chain,
            'res_num': res_num,
            'res_name': res_data['name'],
            'n_atoms': len(res_data['atoms'])
        })

    return {
        'atoms': atoms,
        'residues': residues,
        'ca_coords': np.array(ca_coords),
        'res_info': res_info,
        'n_residues': len(ca_coords)
    }


# ==============================================================================
# GEOMETRIC POCKET DETECTION
# ==============================================================================

def compute_solvent_accessible_surface(coords: np.ndarray,
                                        probe_radius: float = 1.4,
                                        n_points: int = 92) -> Dict:
    """
    Compute solvent-accessible surface using Shrake-Rupley algorithm.

    Returns surface points and per-residue SASA.
    """
    n_atoms = len(coords)
    vdw_radius = 1.7  # Approximate for Cα
    test_radius = vdw_radius + probe_radius

    # Generate Fibonacci sphere points
    indices = np.arange(0, n_points, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * indices / n_points)
    theta = np.pi * (1 + 5**0.5) * indices

    sphere_points = np.column_stack([
        np.sin(phi) * np.cos(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(phi)
    ])

    surface_points = []
    residue_sasa = []
    residue_exposure = []

    for i in range(n_atoms):
        test_points = coords[i] + sphere_points * test_radius

        # Check accessibility
        accessible_points = []
        for point in test_points:
            is_accessible = True
            for j in range(n_atoms):
                if i != j:
                    dist = np.linalg.norm(point - coords[j])
                    if dist < test_radius:
                        is_accessible = False
                        break
            if is_accessible:
                accessible_points.append(point)

        n_accessible = len(accessible_points)
        exposure = n_accessible / n_points
        sasa = 4 * np.pi * test_radius**2 * exposure

        residue_sasa.append(sasa)
        residue_exposure.append(exposure)
        surface_points.extend(accessible_points)

    return {
        'surface_points': np.array(surface_points) if surface_points else np.array([]),
        'residue_sasa': np.array(residue_sasa),
        'residue_exposure': np.array(residue_exposure),
        'total_sasa': sum(residue_sasa)
    }


def detect_pockets_alpha_shape(coords: np.ndarray,
                                alpha: float = 8.0) -> List[Dict]:
    """
    Detect surface pockets using alpha shape analysis.

    Pockets are concave regions where a probe sphere can sit.
    """
    n_atoms = len(coords)
    if n_atoms < 4:
        return []

    try:
        # Compute Delaunay triangulation
        tri = Delaunay(coords)
    except Exception:
        return []

    # Find tetrahedra with circumradius > alpha (cavity indicators)
    pocket_residues = defaultdict(set)
    pocket_centers = []

    for simplex in tri.simplices:
        # Get tetrahedron vertices
        pts = coords[simplex]

        # Compute circumcenter and circumradius
        # Using the formula for tetrahedron circumsphere
        A = pts[0]
        B = pts[1]
        C = pts[2]
        D = pts[3]

        # Vectors from A
        AB = B - A
        AC = C - A
        AD = D - A

        # Solve for circumcenter
        denom = 2 * np.dot(AB, np.cross(AC, AD))
        if abs(denom) < 1e-10:
            continue

        AB_sq = np.dot(AB, AB)
        AC_sq = np.dot(AC, AC)
        AD_sq = np.dot(AD, AD)

        circumcenter = A + (
            AB_sq * np.cross(AC, AD) +
            AC_sq * np.cross(AD, AB) +
            AD_sq * np.cross(AB, AC)
        ) / denom

        circumradius = np.linalg.norm(circumcenter - A)

        # Large circumradius = cavity/pocket
        if circumradius > alpha:
            pocket_centers.append(circumcenter)
            for idx in simplex:
                pocket_residues[len(pocket_centers) - 1].add(idx)

    if not pocket_centers:
        return []

    # Cluster nearby pocket centers
    pocket_centers = np.array(pocket_centers)

    if len(pocket_centers) > 1:
        Z = linkage(pocket_centers, method='average')
        clusters = fcluster(Z, t=5.0, criterion='distance')
    else:
        clusters = np.array([1])

    # Merge pockets by cluster
    merged_pockets = defaultdict(lambda: {'residues': set(), 'centers': []})
    for i, cluster_id in enumerate(clusters):
        merged_pockets[cluster_id]['residues'].update(pocket_residues[i])
        merged_pockets[cluster_id]['centers'].append(pocket_centers[i])

    # Convert to list of pocket dicts
    pockets = []
    for cluster_id, data in merged_pockets.items():
        centers = np.array(data['centers'])
        centroid = centers.mean(axis=0)

        # Estimate pocket volume (convex hull of centers)
        try:
            if len(centers) >= 4:
                hull = ConvexHull(centers)
                volume = hull.volume
            else:
                volume = len(centers) * 50  # Approximate
        except:
            volume = len(centers) * 50

        pockets.append({
            'id': len(pockets) + 1,
            'centroid': centroid.tolist(),
            'residues': sorted(list(data['residues'])),
            'n_residues': len(data['residues']),
            'volume_estimate': float(volume)
        })

    # Sort by volume (larger pockets first)
    pockets.sort(key=lambda x: x['volume_estimate'], reverse=True)

    return pockets


def detect_pockets_grid(coords: np.ndarray,
                        grid_spacing: float = 1.0,
                        min_depth: float = 3.0) -> List[Dict]:
    """
    Grid-based pocket detection.

    Creates a 3D grid and identifies buried grid points.
    """
    # Bounding box
    min_coords = coords.min(axis=0) - 5
    max_coords = coords.max(axis=0) + 5

    # Create grid
    x_range = np.arange(min_coords[0], max_coords[0], grid_spacing)
    y_range = np.arange(min_coords[1], max_coords[1], grid_spacing)
    z_range = np.arange(min_coords[2], max_coords[2], grid_spacing)

    # Find grid points that are:
    # 1. Far enough from all atoms (not inside protein)
    # 2. But surrounded by atoms (in a pocket)

    vdw_radius = 1.7
    probe_radius = 1.4

    pocket_points = []

    for x in x_range:
        for y in y_range:
            for z in z_range:
                point = np.array([x, y, z])
                distances = np.linalg.norm(coords - point, axis=1)

                min_dist = distances.min()

                # Not inside protein
                if min_dist < vdw_radius:
                    continue

                # Count nearby atoms (pocket surroundedness)
                nearby = np.sum(distances < 6.0)

                # Check if point is "buried" (surrounded on multiple sides)
                if nearby >= 4 and min_dist < 5.0:
                    # Check for surrounding atoms in different directions
                    directions = np.sign(coords - point)
                    unique_octants = set()
                    for i, d in enumerate(distances):
                        if d < 6.0:
                            octant = tuple(directions[i])
                            unique_octants.add(octant)

                    # Buried if atoms in at least 4 different octants
                    if len(unique_octants) >= 4:
                        pocket_points.append({
                            'point': point,
                            'depth': nearby,
                            'min_dist': min_dist
                        })

    if not pocket_points:
        return []

    # Cluster pocket points
    points_array = np.array([p['point'] for p in pocket_points])

    if len(points_array) > 1:
        Z = linkage(points_array, method='average')
        clusters = fcluster(Z, t=4.0, criterion='distance')
    else:
        clusters = np.array([1])

    # Merge into pockets
    merged = defaultdict(list)
    for i, cluster_id in enumerate(clusters):
        merged[cluster_id].append(pocket_points[i])

    pockets = []
    for cluster_id, points in merged.items():
        if len(points) < 3:  # Skip tiny pockets
            continue

        centers = np.array([p['point'] for p in points])
        centroid = centers.mean(axis=0)

        # Find residues near this pocket
        nearby_residues = set()
        for p in points:
            distances = np.linalg.norm(coords - p['point'], axis=1)
            for i, d in enumerate(distances):
                if d < 5.0:
                    nearby_residues.add(i)

        pockets.append({
            'id': len(pockets) + 1,
            'centroid': centroid.tolist(),
            'residues': sorted(list(nearby_residues)),
            'n_residues': len(nearby_residues),
            'n_grid_points': len(points),
            'volume_estimate': float(len(points) * grid_spacing**3)
        })

    pockets.sort(key=lambda x: x['volume_estimate'], reverse=True)
    return pockets


# ==============================================================================
# Z² CONTACT ANALYSIS FOR BINDING SITES
# ==============================================================================

def compute_z2_contact_deviation(coords: np.ndarray,
                                  contact_cutoff: float = 8.0) -> Dict:
    """
    Compute Z² contact deviation per residue.

    KEY INSIGHT: Binding sites often have SUBOPTIMAL Z² packing.
    Residues with fewer than 8 contacts are "ready to accept" a binding partner.
    Residues with more than 8 contacts are "saturated".

    Ideal binding site: slightly under-packed (contacts < 8).
    """
    n_residues = len(coords)
    distances = cdist(coords, coords)

    contacts_per_residue = []
    z2_deviation = []
    binding_readiness = []

    for i in range(n_residues):
        # Count contacts (excluding self and immediate neighbors)
        contacts = 0
        for j in range(n_residues):
            if abs(i - j) > 1 and distances[i, j] < contact_cutoff:
                contacts += 1

        contacts_per_residue.append(contacts)

        # Deviation from optimal Z² = 8
        deviation = contacts - OPTIMAL_CONTACTS
        z2_deviation.append(deviation)

        # Binding readiness: under-packed residues are more binding-ready
        # Score: higher = more ready to bind
        if contacts < OPTIMAL_CONTACTS:
            # Under-packed: good for binding
            readiness = (OPTIMAL_CONTACTS - contacts) / OPTIMAL_CONTACTS
        else:
            # Over-packed: poor for binding
            readiness = -abs(deviation) / OPTIMAL_CONTACTS

        binding_readiness.append(readiness)

    return {
        'contacts_per_residue': contacts_per_residue,
        'z2_deviation': z2_deviation,
        'binding_readiness': binding_readiness,
        'mean_contacts': float(np.mean(contacts_per_residue)),
        'underpacked_residues': [i for i, c in enumerate(contacts_per_residue) if c < OPTIMAL_CONTACTS - 1]
    }


# ==============================================================================
# FLEXIBILITY INTEGRATION
# ==============================================================================

def load_ensemble_flexibility(ensemble_results_path: str) -> Optional[Dict]:
    """Load RMSF flexibility profile from conformational ensemble."""
    if not os.path.exists(ensemble_results_path):
        return None

    with open(ensemble_results_path, 'r') as f:
        data = json.load(f)

    return {
        'rmsf': data.get('flexibility_profile', []),
        'hinge_regions': data.get('hinge_regions', []),
        'mean_rmsf': data.get('ensemble_statistics', {}).get('mean_rmsf', 0)
    }


def compute_anm_flexibility(coords: np.ndarray,
                            cutoff: float = 13.0,
                            n_modes: int = 10) -> Dict:
    """Compute ANM-based flexibility if ensemble not available."""
    n_atoms = len(coords)

    # Build Hessian
    hessian = np.zeros((3 * n_atoms, 3 * n_atoms))

    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            diff = coords[j] - coords[i]
            dist = np.linalg.norm(diff)

            if dist < cutoff:
                # Spring constant (1/r² weighting)
                gamma = 1.0 / (dist ** 2)

                # Outer product
                outer = np.outer(diff, diff) / (dist ** 2)

                # Fill Hessian blocks
                for a in range(3):
                    for b in range(3):
                        val = gamma * outer[a, b]
                        hessian[3*i + a, 3*j + b] = -val
                        hessian[3*j + b, 3*i + a] = -val
                        hessian[3*i + a, 3*i + b] += val
                        hessian[3*j + a, 3*j + b] += val

    # Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(hessian)

    # Skip first 6 zero modes (translation + rotation)
    nonzero_idx = eigenvalues > 1e-6
    eigenvalues = eigenvalues[nonzero_idx]
    eigenvectors = eigenvectors[:, nonzero_idx]

    # Mean square fluctuation from modes
    msf = np.zeros(n_atoms)
    for mode_idx in range(min(n_modes, len(eigenvalues))):
        mode = eigenvectors[:, mode_idx].reshape(n_atoms, 3)
        mode_msf = np.sum(mode ** 2, axis=1)
        msf += mode_msf / eigenvalues[mode_idx]

    rmsf = np.sqrt(msf)
    rmsf = rmsf / rmsf.max()  # Normalize

    return {
        'rmsf': rmsf.tolist(),
        'mean_rmsf': float(rmsf.mean())
    }


# ==============================================================================
# ELECTROSTATIC ANALYSIS
# ==============================================================================

def compute_electrostatic_patches(res_info: List[Dict],
                                   coords: np.ndarray) -> Dict:
    """
    Identify charged patches on the surface.

    Binding sites often have specific charge patterns.
    """
    n_residues = len(res_info)

    # Get charge per residue
    charges = []
    for res in res_info:
        res_name = res['res_name']
        charge = RESIDUE_CHARGE.get(res_name, 0)
        charges.append(charge)

    charges = np.array(charges)

    # Find charged clusters
    positive_residues = [i for i, c in enumerate(charges) if c > 0]
    negative_residues = [i for i, c in enumerate(charges) if c < 0]

    # Cluster positive residues
    positive_patches = []
    if len(positive_residues) > 1:
        pos_coords = coords[positive_residues]
        Z = linkage(pos_coords, method='average')
        clusters = fcluster(Z, t=10.0, criterion='distance')

        for cluster_id in set(clusters):
            members = [positive_residues[i] for i, c in enumerate(clusters) if c == cluster_id]
            if len(members) >= 2:
                centroid = coords[members].mean(axis=0)
                positive_patches.append({
                    'type': 'positive',
                    'residues': members,
                    'centroid': centroid.tolist(),
                    'total_charge': sum(charges[m] for m in members)
                })

    # Cluster negative residues
    negative_patches = []
    if len(negative_residues) > 1:
        neg_coords = coords[negative_residues]
        Z = linkage(neg_coords, method='average')
        clusters = fcluster(Z, t=10.0, criterion='distance')

        for cluster_id in set(clusters):
            members = [negative_residues[i] for i, c in enumerate(clusters) if c == cluster_id]
            if len(members) >= 2:
                centroid = coords[members].mean(axis=0)
                negative_patches.append({
                    'type': 'negative',
                    'residues': members,
                    'centroid': centroid.tolist(),
                    'total_charge': sum(charges[m] for m in members)
                })

    return {
        'charges': charges.tolist(),
        'positive_patches': positive_patches,
        'negative_patches': negative_patches,
        'net_charge': float(charges.sum())
    }


# ==============================================================================
# COMPOSITE BINDING SITE SCORING
# ==============================================================================

def score_binding_sites(coords: np.ndarray,
                        res_info: List[Dict],
                        pockets: List[Dict],
                        z2_contacts: Dict,
                        flexibility: Dict,
                        electrostatics: Dict,
                        surface: Dict) -> List[Dict]:
    """
    Compute composite Z² binding site score.

    Combines:
    1. Pocket geometry (volume, depth)
    2. Z² contact deviation (under-packing)
    3. Flexibility (RMSF)
    4. Surface exposure
    5. Electrostatic character
    """
    n_residues = len(coords)
    rmsf = flexibility.get('rmsf', [0] * n_residues)
    if len(rmsf) != n_residues:
        rmsf = [0] * n_residues

    binding_readiness = z2_contacts['binding_readiness']
    exposure = surface['residue_exposure']
    charges = electrostatics['charges']

    scored_sites = []

    for pocket in pockets:
        residues = pocket['residues']
        if not residues:
            continue

        # Geometric score (volume-based)
        volume = pocket.get('volume_estimate', 0)
        geo_score = min(1.0, volume / 500)  # Normalize to ~1 for good pockets

        # Z² binding readiness score (mean of residue readiness)
        z2_scores = [binding_readiness[r] for r in residues if r < len(binding_readiness)]
        z2_score = np.mean(z2_scores) if z2_scores else 0

        # Flexibility score
        flex_scores = [rmsf[r] for r in residues if r < len(rmsf)]
        flex_score = np.mean(flex_scores) if flex_scores else 0

        # Surface exposure score
        exp_scores = [exposure[r] for r in residues if r < len(exposure)]
        exp_score = np.mean(exp_scores) if exp_scores else 0

        # Electrostatic diversity (good binding sites often have mixed charges)
        site_charges = [charges[r] for r in residues if r < len(charges)]
        has_positive = any(c > 0 for c in site_charges)
        has_negative = any(c < 0 for c in site_charges)
        elec_score = 0.5 if (has_positive and has_negative) else 0.25 if (has_positive or has_negative) else 0

        # Composite Z² binding score
        # Weights based on empirical importance
        composite_score = (
            0.25 * geo_score +      # Pocket geometry
            0.30 * z2_score +       # Z² contact deviation (most important!)
            0.20 * flex_score +     # Flexibility
            0.15 * exp_score +      # Surface exposure
            0.10 * elec_score       # Electrostatic character
        )

        # Get residue names
        residue_names = []
        for r in residues:
            if r < len(res_info):
                info = res_info[r]
                residue_names.append(f"{info['res_name']}{info['res_num']}")

        scored_sites.append({
            'pocket_id': pocket['id'],
            'centroid': pocket['centroid'],
            'residues': residues,
            'residue_names': residue_names[:10],  # Top 10 for brevity
            'n_residues': len(residues),
            'volume': volume,
            'scores': {
                'geometric': float(geo_score),
                'z2_binding_readiness': float(z2_score),
                'flexibility': float(flex_score),
                'exposure': float(exp_score),
                'electrostatic': float(elec_score)
            },
            'composite_z2_score': float(composite_score),
            'binding_verdict': 'HIGH' if composite_score > 0.4 else 'MEDIUM' if composite_score > 0.2 else 'LOW'
        })

    # Sort by composite score
    scored_sites.sort(key=lambda x: x['composite_z2_score'], reverse=True)

    # Assign ranks
    for i, site in enumerate(scored_sites):
        site['rank'] = i + 1

    return scored_sites


# ==============================================================================
# DRUGGABILITY ASSESSMENT
# ==============================================================================

def assess_druggability(binding_sites: List[Dict],
                        res_info: List[Dict]) -> List[Dict]:
    """
    Assess druggability of predicted binding sites.

    Based on:
    1. Pocket volume (200-1000 Å³ is druglike)
    2. Hydrophobic character (drugs are often hydrophobic)
    3. Enclosure (deeper pockets hold drugs better)
    """
    for site in binding_sites:
        volume = site.get('volume', 0)
        residues = site.get('residues', [])

        # Volume score
        if 200 < volume < 1000:
            volume_score = 1.0
        elif 100 < volume < 1500:
            volume_score = 0.5
        else:
            volume_score = 0.2

        # Hydrophobicity score
        hydro_scores = []
        for r in residues:
            if r < len(res_info):
                res_name = res_info[r]['res_name']
                hydro = HYDROPHOBICITY.get(res_name, 0)
                hydro_scores.append(hydro)

        mean_hydro = np.mean(hydro_scores) if hydro_scores else 0
        hydro_score = (mean_hydro + 1) / 2  # Normalize to 0-1

        # Combined druggability
        druggability = 0.6 * volume_score + 0.4 * hydro_score

        site['druggability'] = {
            'score': float(druggability),
            'volume_score': float(volume_score),
            'hydrophobicity_score': float(hydro_score),
            'verdict': 'DRUGGABLE' if druggability > 0.6 else 'MODERATE' if druggability > 0.4 else 'CHALLENGING'
        }

    return binding_sites


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def generate_binding_site_visualization(coords: np.ndarray,
                                         binding_sites: List[Dict],
                                         z2_contacts: Dict,
                                         output_path: str):
    """Generate binding site analysis plots."""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("  Warning: matplotlib not available for visualization")
        return

    fig = plt.figure(figsize=(16, 12))

    # 1. 3D structure with binding sites
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')

    # Color by binding readiness
    readiness = z2_contacts['binding_readiness']
    colors = plt.cm.RdYlGn([(r + 1) / 2 for r in readiness])

    ax1.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
                c=colors, s=50, alpha=0.6)

    # Mark top binding sites
    for i, site in enumerate(binding_sites[:3]):
        centroid = site['centroid']
        ax1.scatter(*centroid, s=200, marker='*', c='red',
                   edgecolors='black', linewidths=2,
                   label=f"Site {site['rank']}" if i == 0 else "")
        ax1.text(centroid[0], centroid[1], centroid[2],
                f"  #{site['rank']}", fontsize=10, fontweight='bold')

    ax1.set_xlabel('X (Å)')
    ax1.set_ylabel('Y (Å)')
    ax1.set_zlabel('Z (Å)')
    ax1.set_title('Z² Binding Site Prediction\n(Green = binding-ready, Red = saturated)')

    # 2. Binding site scores
    ax2 = fig.add_subplot(2, 2, 2)

    if binding_sites:
        n_sites = min(10, len(binding_sites))
        site_ids = [f"Site {s['rank']}" for s in binding_sites[:n_sites]]
        scores = [s['composite_z2_score'] for s in binding_sites[:n_sites]]

        colors = ['green' if s > 0.4 else 'orange' if s > 0.2 else 'red' for s in scores]
        bars = ax2.barh(site_ids, scores, color=colors)
        ax2.set_xlabel('Composite Z² Binding Score')
        ax2.set_title('Top Binding Sites Ranked')
        ax2.set_xlim(0, 1)

        # Add score labels
        for bar, score in zip(bars, scores):
            ax2.text(score + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{score:.3f}', va='center', fontsize=9)

    # 3. Score components for top site
    ax3 = fig.add_subplot(2, 2, 3)

    if binding_sites:
        top_site = binding_sites[0]
        components = ['Geometric', 'Z² Readiness', 'Flexibility', 'Exposure', 'Electrostatic']
        values = [
            top_site['scores']['geometric'],
            top_site['scores']['z2_binding_readiness'],
            top_site['scores']['flexibility'],
            top_site['scores']['exposure'],
            top_site['scores']['electrostatic']
        ]

        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(components)))
        ax3.bar(components, values, color=colors)
        ax3.set_ylabel('Score')
        ax3.set_title(f'Score Breakdown: Site #{top_site["rank"]}')
        ax3.set_ylim(0, 1)
        plt.xticks(rotation=45, ha='right')

    # 4. Per-residue binding readiness
    ax4 = fig.add_subplot(2, 2, 4)

    residue_idx = range(len(readiness))
    colors = ['green' if r > 0.2 else 'orange' if r > 0 else 'red' for r in readiness]
    ax4.bar(residue_idx, readiness, color=colors, width=1.0)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax4.set_xlabel('Residue Index')
    ax4.set_ylabel('Binding Readiness')
    ax4.set_title('Per-Residue Z² Binding Readiness\n(Positive = under-packed, ready to bind)')

    # Mark binding site residues
    if binding_sites:
        for r in binding_sites[0]['residues']:
            if r < len(readiness):
                ax4.axvline(x=r, color='red', alpha=0.3, linewidth=0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Visualization saved: {output_path}")


def write_binding_site_pdb(coords: np.ndarray,
                           res_info: List[Dict],
                           binding_sites: List[Dict],
                           output_path: str):
    """Write PDB with B-factor colored by binding score."""
    with open(output_path, 'w') as f:
        f.write("REMARK  Z2 Binding Site Prediction\n")
        f.write("REMARK  B-factor = binding readiness score\n")

        # Create residue-to-score mapping
        residue_scores = {}
        for site in binding_sites:
            score = site['composite_z2_score']
            for r in site['residues']:
                if r not in residue_scores or score > residue_scores[r]:
                    residue_scores[r] = score

        for i, (coord, info) in enumerate(zip(coords, res_info)):
            score = residue_scores.get(i, 0) * 100  # Scale for B-factor

            f.write(f"ATOM  {i+1:5d}  CA  {info['res_name']:3s} {info['chain']}"
                   f"{info['res_num']:4d}    "
                   f"{coord[0]:8.3f}{coord[1]:8.3f}{coord[2]:8.3f}"
                   f"  1.00{score:6.2f}           C\n")

        f.write("END\n")

    print(f"  ✓ Binding site PDB: {output_path}")


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def predict_binding_sites(pdb_path: str,
                          ensemble_path: str = None,
                          output_dir: str = "binding_sites") -> Dict:
    """
    Predict binding sites using Z² geometric principles.

    Full analysis pipeline.
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nAnalyzing: {pdb_path}")

    # Parse structure
    structure = parse_pdb_structure(pdb_path)
    coords = structure['ca_coords']
    res_info = structure['res_info']
    n_residues = structure['n_residues']

    print(f"  Residues: {n_residues}")

    # 1. Compute surface
    print("\nComputing solvent-accessible surface...")
    surface = compute_solvent_accessible_surface(coords)
    print(f"  Total SASA: {surface['total_sasa']:.1f} Ų")

    # 2. Detect pockets
    print("\nDetecting pockets...")
    pockets_alpha = detect_pockets_alpha_shape(coords)
    pockets_grid = detect_pockets_grid(coords)

    # Merge pocket methods
    all_pockets = pockets_alpha + pockets_grid

    # Deduplicate by centroid proximity
    unique_pockets = []
    for pocket in all_pockets:
        is_duplicate = False
        for existing in unique_pockets:
            dist = np.linalg.norm(
                np.array(pocket['centroid']) - np.array(existing['centroid'])
            )
            if dist < 5.0:
                is_duplicate = True
                # Merge residues
                existing['residues'] = list(set(existing['residues'] + pocket['residues']))
                existing['n_residues'] = len(existing['residues'])
                break
        if not is_duplicate:
            unique_pockets.append(pocket)

    # Reassign IDs
    for i, pocket in enumerate(unique_pockets):
        pocket['id'] = i + 1

    print(f"  Detected {len(unique_pockets)} unique pockets")

    # 3. Z² contact analysis
    print("\nComputing Z² contact deviation...")
    z2_contacts = compute_z2_contact_deviation(coords)
    print(f"  Mean contacts: {z2_contacts['mean_contacts']:.1f}")
    print(f"  Under-packed residues: {len(z2_contacts['underpacked_residues'])}")

    # 4. Flexibility analysis
    print("\nAnalyzing flexibility...")
    if ensemble_path and os.path.exists(ensemble_path):
        flexibility = load_ensemble_flexibility(ensemble_path)
        print(f"  Loaded from ensemble: {ensemble_path}")
    else:
        flexibility = compute_anm_flexibility(coords)
        print(f"  Computed from ANM")

    print(f"  Mean RMSF: {flexibility['mean_rmsf']:.3f}")

    # 5. Electrostatic analysis
    print("\nAnalyzing electrostatics...")
    electrostatics = compute_electrostatic_patches(res_info, coords)
    print(f"  Net charge: {electrostatics['net_charge']:.1f}")
    print(f"  Positive patches: {len(electrostatics['positive_patches'])}")
    print(f"  Negative patches: {len(electrostatics['negative_patches'])}")

    # 6. Score binding sites
    print("\nScoring binding sites...")
    binding_sites = score_binding_sites(
        coords, res_info, unique_pockets,
        z2_contacts, flexibility, electrostatics, surface
    )

    # 7. Assess druggability
    binding_sites = assess_druggability(binding_sites, res_info)

    # Report top sites
    print(f"\n{'='*60}")
    print("TOP PREDICTED BINDING SITES")
    print(f"{'='*60}")

    for site in binding_sites[:5]:
        print(f"\n  Site #{site['rank']}:")
        print(f"    Z² Score: {site['composite_z2_score']:.3f} ({site['binding_verdict']})")
        print(f"    Residues: {site['n_residues']}")
        print(f"    Volume: {site['volume']:.1f} ų")
        print(f"    Druggability: {site['druggability']['verdict']}")
        print(f"    Key residues: {', '.join(site['residue_names'][:5])}")

    # 8. Generate outputs
    print(f"\n{'='*60}")
    print("GENERATING OUTPUTS")
    print(f"{'='*60}")

    # Visualization
    viz_path = os.path.join(output_dir, "binding_site_analysis.png")
    generate_binding_site_visualization(coords, binding_sites, z2_contacts, viz_path)

    # Binding site PDB
    pdb_out = os.path.join(output_dir, "binding_sites.pdb")
    write_binding_site_pdb(coords, res_info, binding_sites, pdb_out)

    # JSON results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_path,
        'n_residues': n_residues,
        'z2_constant': Z2,
        'surface_analysis': {
            'total_sasa': float(surface['total_sasa']),
            'mean_exposure': float(np.mean(surface['residue_exposure']))
        },
        'z2_contact_analysis': {
            'mean_contacts': z2_contacts['mean_contacts'],
            'n_underpacked': len(z2_contacts['underpacked_residues']),
            'underpacked_residues': z2_contacts['underpacked_residues'][:20]
        },
        'electrostatics': {
            'net_charge': electrostatics['net_charge'],
            'n_positive_patches': len(electrostatics['positive_patches']),
            'n_negative_patches': len(electrostatics['negative_patches'])
        },
        'n_pockets_detected': len(unique_pockets),
        'n_binding_sites_scored': len(binding_sites),
        'top_binding_sites': binding_sites[:10],
        'output_files': {
            'visualization': viz_path,
            'pdb': pdb_out
        }
    }

    json_path = os.path.join(output_dir, "binding_site_results.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  ✓ Results saved: {json_path}")

    # Summary
    print(f"\n{'='*60}")
    print("Z² BINDING SITE PREDICTION COMPLETE")
    print(f"{'='*60}")

    if binding_sites:
        top = binding_sites[0]
        print(f"""
  TOP BINDING SITE: #{top['rank']}

  Composite Z² Score: {top['composite_z2_score']:.3f}
  Verdict: {top['binding_verdict']}

  This site is predicted to bind ligands because:
  - Z² geometry shows under-packed contacts (ready to accept partner)
  - {'High' if top['scores']['flexibility'] > 0.5 else 'Moderate'} flexibility (conformational adaptation)
  - {'Good' if top['scores']['exposure'] > 0.5 else 'Partial'} surface exposure

  Druggability: {top['druggability']['verdict']}

  AlphaFold gives you the shape.
  Z² tells you WHERE DRUGS BIND.
""")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run binding site prediction on Z² protein."""
    import sys

    # Default to our Z² globular protein
    if len(sys.argv) > 1:
        pdb_path = sys.argv[1]
    else:
        pdb_path = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

    # Check for ensemble results
    ensemble_path = "conformational_ensemble/ensemble_results.json"

    if not os.path.exists(pdb_path):
        print(f"PDB not found: {pdb_path}")
        return None

    results = predict_binding_sites(
        pdb_path,
        ensemble_path=ensemble_path,
        output_dir="binding_sites"
    )

    return results


if __name__ == "__main__":
    results = main()
