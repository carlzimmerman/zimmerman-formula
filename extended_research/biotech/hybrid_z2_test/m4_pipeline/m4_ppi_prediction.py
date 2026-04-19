#!/usr/bin/env python3
"""
Z² Protein-Protein Interaction (PPI) Prediction

SPDX-License-Identifier: AGPL-3.0-or-later

Predicts protein-protein interaction sites and binding partners using Z² geometry.

Z² THEORY FOR PPI:
- Residues with contact deficiency (< 8 contacts) seek external partners
- Interface residues have UNDER-PACKED coordination that proteins complete
- Optimal interfaces restore Z² = 8 contacts per residue
- Binding hotspots are residues where contact completion is most favorable

PREDICTIONS:
1. Interface residue identification
2. Binding hotspot ranking
3. Surface patch analysis (hydrophobic, charged, polar)
4. Partner type prediction
5. Interaction energy estimation
6. Docking-ready interface mapping

Input: ESM-predicted PDB structure
Output: PPI predictions with interface maps

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
OPTIMAL_CONTACTS = 8  # Z² topological optimum
CONTACT_CUTOFF = 8.0  # Å
INTERFACE_CUTOFF = 10.0  # Å for interface detection
SURFACE_CUTOFF = 0.25  # Relative SASA threshold for surface residues

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Interface propensity (from protein-protein interface statistics)
INTERFACE_PROPENSITY = {
    'W': 1.84, 'Y': 1.53, 'F': 1.27, 'M': 1.29, 'H': 1.22,
    'I': 1.15, 'L': 1.14, 'V': 1.04, 'R': 1.15, 'K': 0.95,
    'C': 1.13, 'T': 0.92, 'A': 0.87, 'N': 0.88, 'Q': 0.98,
    'S': 0.82, 'G': 0.72, 'P': 0.76, 'D': 0.79, 'E': 0.84
}

# Hydrophobicity (Kyte-Doolittle)
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'N': -3.5,
    'D': -3.5, 'Q': -3.5, 'E': -3.5, 'K': -3.9, 'R': -4.5
}

# Charge at pH 7
CHARGE = {
    'K': 1, 'R': 1, 'H': 0.5, 'D': -1, 'E': -1,
    'A': 0, 'C': 0, 'F': 0, 'G': 0, 'I': 0,
    'L': 0, 'M': 0, 'N': 0, 'P': 0, 'Q': 0,
    'S': 0, 'T': 0, 'V': 0, 'W': 0, 'Y': 0
}

# Hotspot propensity (residues that contribute most to binding energy)
HOTSPOT_PROPENSITY = {
    'W': 2.31, 'R': 1.95, 'Y': 1.67, 'F': 1.43, 'M': 1.38,
    'I': 1.21, 'L': 1.18, 'H': 1.52, 'K': 1.12, 'D': 1.35,
    'E': 1.28, 'N': 1.15, 'Q': 1.08, 'T': 0.92, 'V': 0.95,
    'C': 1.05, 'A': 0.72, 'S': 0.78, 'G': 0.58, 'P': 0.65
}


def parse_pdb(pdb_file: str) -> Tuple[np.ndarray, List[str], List[str]]:
    """Parse PDB file to extract Cα coordinates and residue info."""
    coords = []
    residues = []
    residue_names = []

    aa_map = {
        'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
        'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
        'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
        'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
    }

    seen_residues = set()

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_num = int(line[22:26])
                res_name = line[17:20].strip()

                if res_num not in seen_residues:
                    seen_residues.add(res_num)
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])

                    aa = aa_map.get(res_name, 'X')
                    residues.append(f"{aa}{res_num}")
                    residue_names.append(aa)

    return np.array(coords), residues, residue_names


def calculate_contacts(coords: np.ndarray, cutoff: float = CONTACT_CUTOFF) -> np.ndarray:
    """Calculate contact matrix and contacts per residue."""
    n = len(coords)
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    distances = np.sqrt(np.sum(diff**2, axis=-1))

    # Contact matrix (excluding sequential neighbors)
    contact_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and distances[i, j] < cutoff:
                contact_matrix[i, j] = 1

    contacts_per_residue = np.sum(contact_matrix, axis=1)
    return contacts_per_residue, contact_matrix, distances


def calculate_surface_accessibility(coords: np.ndarray,
                                    contacts: np.ndarray) -> np.ndarray:
    """Estimate surface accessibility from contact count and position."""
    n = len(coords)

    # Center of mass
    com = np.mean(coords, axis=0)

    # Distance from COM (more distant = more surface)
    dist_from_com = np.linalg.norm(coords - com, axis=1)
    max_dist = np.max(dist_from_com)
    radial_exposure = dist_from_com / max_dist if max_dist > 0 else np.ones(n)

    # Contact-based burial (fewer contacts = more exposed)
    max_contacts = np.max(contacts) if np.max(contacts) > 0 else 1
    contact_exposure = 1 - (contacts / max_contacts)

    # Combined accessibility score
    accessibility = 0.5 * radial_exposure + 0.5 * contact_exposure

    return accessibility


def identify_interface_residues(coords: np.ndarray,
                                contacts: np.ndarray,
                                accessibility: np.ndarray,
                                residue_names: List[str]) -> List[Dict]:
    """Identify residues likely to be at protein-protein interfaces."""
    n = len(coords)
    interface_residues = []

    for i in range(n):
        aa = residue_names[i]

        # Contact deficiency (under-packed = interface candidate)
        contact_deficiency = OPTIMAL_CONTACTS - contacts[i]

        # Interface propensity from amino acid type
        aa_propensity = INTERFACE_PROPENSITY.get(aa, 1.0)

        # Surface requirement
        if accessibility[i] < SURFACE_CUTOFF:
            continue  # Skip buried residues

        # Hotspot propensity
        hotspot = HOTSPOT_PROPENSITY.get(aa, 1.0)

        # Calculate interface score
        # Higher for: surface exposed, under-packed, high propensity
        interface_score = (
            contact_deficiency * 0.3 +
            aa_propensity * 0.3 +
            accessibility[i] * 0.2 +
            hotspot * 0.2
        )

        if interface_score > 0.5:
            interface_residues.append({
                'residue_idx': i,
                'residue': f"{aa}{i+1}",
                'aa': aa,
                'contacts': int(contacts[i]),
                'contact_deficiency': float(contact_deficiency),
                'accessibility': float(accessibility[i]),
                'interface_propensity': float(aa_propensity),
                'hotspot_propensity': float(hotspot),
                'interface_score': float(interface_score),
                'is_hotspot': hotspot > 1.3
            })

    # Sort by interface score
    interface_residues.sort(key=lambda x: -x['interface_score'])

    return interface_residues


def identify_surface_patches(coords: np.ndarray,
                             interface_residues: List[Dict],
                             residue_names: List[str],
                             distances: np.ndarray) -> List[Dict]:
    """Identify contiguous surface patches for PPI."""
    if len(interface_residues) == 0:
        return []

    # Get interface residue indices
    interface_idx = set(r['residue_idx'] for r in interface_residues)

    # Cluster nearby interface residues into patches
    patches = []
    visited = set()

    for res in interface_residues:
        idx = res['residue_idx']
        if idx in visited:
            continue

        # BFS to find connected patch
        patch_residues = []
        queue = [idx]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            if current in interface_idx:
                patch_residues.append(current)

                # Find neighbors within patch distance
                for j in interface_idx:
                    if j not in visited and distances[current, j] < INTERFACE_CUTOFF:
                        queue.append(j)

        if len(patch_residues) >= 3:  # Minimum patch size
            # Characterize the patch
            patch_aas = [residue_names[i] for i in patch_residues]
            patch_coords = coords[patch_residues]

            # Patch properties
            mean_hydro = np.mean([HYDROPHOBICITY.get(aa, 0) for aa in patch_aas])
            net_charge = sum(CHARGE.get(aa, 0) for aa in patch_aas)
            mean_hotspot = np.mean([HOTSPOT_PROPENSITY.get(aa, 1) for aa in patch_aas])

            # Patch center and size
            patch_center = np.mean(patch_coords, axis=0)
            patch_radius = np.max(np.linalg.norm(patch_coords - patch_center, axis=1))

            # Classify patch type
            if mean_hydro > 1.0:
                patch_type = "hydrophobic"
            elif abs(net_charge) > 2:
                patch_type = "charged"
            else:
                patch_type = "polar"

            patches.append({
                'residue_indices': patch_residues,
                'residues': [f"{residue_names[i]}{i+1}" for i in patch_residues],
                'size': len(patch_residues),
                'patch_type': patch_type,
                'mean_hydrophobicity': float(mean_hydro),
                'net_charge': float(net_charge),
                'mean_hotspot_propensity': float(mean_hotspot),
                'center': patch_center.tolist(),
                'radius': float(patch_radius),
                'binding_potential': float(mean_hotspot * len(patch_residues) / 10)
            })

    # Sort patches by binding potential
    patches.sort(key=lambda x: -x['binding_potential'])

    return patches


def predict_binding_energy(interface_residues: List[Dict],
                           patches: List[Dict]) -> Dict:
    """Estimate binding energy from interface properties."""
    if len(interface_residues) == 0:
        return {'estimated_dG': 0, 'confidence': 0}

    # Empirical binding energy estimation
    # Based on interface size and hotspot content

    n_interface = len(interface_residues)
    n_hotspots = sum(1 for r in interface_residues if r['is_hotspot'])

    # Average hotspot propensity
    mean_hotspot = np.mean([r['hotspot_propensity'] for r in interface_residues])

    # Buried surface area proxy (from contact deficiency)
    total_deficiency = sum(r['contact_deficiency'] for r in interface_residues)

    # Empirical formula for ΔG (kcal/mol)
    # More negative = stronger binding
    dG = -0.5 * n_hotspots - 0.1 * total_deficiency - 0.2 * mean_hotspot * n_interface

    # Confidence based on interface quality
    confidence = min(1.0, n_interface / 20 + n_hotspots / 10)

    return {
        'estimated_dG_kcal_mol': float(dG),
        'n_interface_residues': n_interface,
        'n_hotspots': n_hotspots,
        'mean_hotspot_propensity': float(mean_hotspot),
        'total_contact_deficiency': float(total_deficiency),
        'confidence': float(confidence),
        'binding_strength': 'strong' if dG < -8 else 'moderate' if dG < -4 else 'weak'
    }


def predict_partner_types(patches: List[Dict],
                          interface_residues: List[Dict]) -> List[Dict]:
    """Predict likely binding partner characteristics."""
    if len(patches) == 0:
        return []

    partner_predictions = []

    for i, patch in enumerate(patches[:3]):  # Top 3 patches
        patch_type = patch['patch_type']
        charge = patch['net_charge']
        hydro = patch['mean_hydrophobicity']

        # Predict complementary partner
        if patch_type == 'hydrophobic':
            partner = {
                'patch_id': i + 1,
                'our_patch_type': 'hydrophobic',
                'partner_type': 'hydrophobic',
                'partner_description': 'Hydrophobic domain (e.g., transmembrane, lipid-binding)',
                'interaction_mode': 'Hydrophobic burial',
                'example_partners': ['membrane proteins', 'lipid carriers', 'hydrophobic clefts']
            }
        elif charge > 2:
            partner = {
                'patch_id': i + 1,
                'our_patch_type': 'positively_charged',
                'partner_type': 'negatively_charged',
                'partner_description': 'Acidic surface (Asp/Glu rich)',
                'interaction_mode': 'Electrostatic attraction',
                'example_partners': ['DNA/RNA', 'phosphoproteins', 'acidic domains']
            }
        elif charge < -2:
            partner = {
                'patch_id': i + 1,
                'our_patch_type': 'negatively_charged',
                'partner_type': 'positively_charged',
                'partner_description': 'Basic surface (Lys/Arg rich)',
                'interaction_mode': 'Electrostatic attraction',
                'example_partners': ['histones', 'basic domains', 'cationic peptides']
            }
        else:
            partner = {
                'patch_id': i + 1,
                'our_patch_type': 'polar',
                'partner_type': 'polar',
                'partner_description': 'Polar/H-bonding surface',
                'interaction_mode': 'Hydrogen bonding network',
                'example_partners': ['enzymes', 'signaling proteins', 'antibodies']
            }

        partner['binding_potential'] = patch['binding_potential']
        partner_predictions.append(partner)

    return partner_predictions


def calculate_z2_interface_analysis(contacts: np.ndarray,
                                    interface_residues: List[Dict]) -> Dict:
    """Analyze how Z² geometry relates to PPI potential."""
    n = len(contacts)

    # Overall statistics
    mean_contacts = np.mean(contacts)
    z2_deviation = mean_contacts - OPTIMAL_CONTACTS

    # Interface-specific
    if len(interface_residues) > 0:
        interface_contacts = [r['contacts'] for r in interface_residues]
        mean_interface_contacts = np.mean(interface_contacts)
        interface_deficiency = OPTIMAL_CONTACTS - mean_interface_contacts
    else:
        mean_interface_contacts = 0
        interface_deficiency = OPTIMAL_CONTACTS

    # Z² interpretation
    # Interface residues should have contact deficiency that partners fill
    z2_ppi_potential = interface_deficiency / OPTIMAL_CONTACTS

    return {
        'mean_contacts_overall': float(mean_contacts),
        'z2_deviation_overall': float(z2_deviation),
        'mean_contacts_interface': float(mean_interface_contacts),
        'interface_contact_deficiency': float(interface_deficiency),
        'z2_ppi_potential': float(z2_ppi_potential),
        'interpretation': (
            f"Interface residues average {mean_interface_contacts:.1f} contacts "
            f"(deficiency: {interface_deficiency:.1f}). "
            f"Binding partner would restore Z² = 8 optimum."
        )
    }


def create_visualization(coords: np.ndarray, contacts: np.ndarray,
                         accessibility: np.ndarray, interface_residues: List[Dict],
                         patches: List[Dict], residue_names: List[str],
                         output_dir: str):
    """Create visualization of PPI predictions."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Patch
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    n = len(coords)
    residue_idx = np.arange(n)

    # 1. Contact profile with interface highlighting
    ax1 = axes[0, 0]
    interface_set = set(r['residue_idx'] for r in interface_residues)
    colors = ['red' if i in interface_set else 'steelblue' for i in range(n)]
    ax1.bar(residue_idx, contacts, color=colors, width=1.0, alpha=0.7)
    ax1.axhline(y=OPTIMAL_CONTACTS, color='green', linestyle='--',
                linewidth=2, label=f'Z² optimal = {OPTIMAL_CONTACTS}')
    ax1.set_xlabel('Residue')
    ax1.set_ylabel('Contacts')
    ax1.set_title('Contact Profile (red = interface)')
    ax1.legend()

    # 2. Surface accessibility
    ax2 = axes[0, 1]
    ax2.fill_between(residue_idx, accessibility, alpha=0.7, color='orange')
    ax2.axhline(y=SURFACE_CUTOFF, color='black', linestyle='--',
                label=f'Surface threshold = {SURFACE_CUTOFF}')
    ax2.set_xlabel('Residue')
    ax2.set_ylabel('Accessibility')
    ax2.set_title('Surface Accessibility')
    ax2.legend()

    # 3. Interface score profile
    ax3 = axes[0, 2]
    interface_scores = np.zeros(n)
    hotspot_mask = np.zeros(n, dtype=bool)
    for r in interface_residues:
        interface_scores[r['residue_idx']] = r['interface_score']
        if r['is_hotspot']:
            hotspot_mask[r['residue_idx']] = True

    colors = ['gold' if hotspot_mask[i] else 'purple' for i in range(n)]
    ax3.bar(residue_idx, interface_scores, color=colors, width=1.0, alpha=0.7)
    ax3.set_xlabel('Residue')
    ax3.set_ylabel('Interface Score')
    ax3.set_title('Interface Propensity (gold = hotspot)')

    # 4. 2D projection with patches
    ax4 = axes[1, 0]
    # Project to 2D using PCA
    coords_centered = coords - np.mean(coords, axis=0)
    if len(coords) > 2:
        U, S, Vt = np.linalg.svd(coords_centered, full_matrices=False)
        proj_2d = coords_centered @ Vt[:2].T
    else:
        proj_2d = coords_centered[:, :2]

    # Color by interface
    scatter_colors = ['red' if i in interface_set else 'lightblue' for i in range(n)]
    ax4.scatter(proj_2d[:, 0], proj_2d[:, 1], c=scatter_colors, s=50, alpha=0.7)

    # Highlight patches
    patch_colors = ['green', 'orange', 'purple']
    for i, patch in enumerate(patches[:3]):
        patch_idx = patch['residue_indices']
        ax4.scatter(proj_2d[patch_idx, 0], proj_2d[patch_idx, 1],
                   c=patch_colors[i % 3], s=100, marker='s', alpha=0.8,
                   label=f"Patch {i+1}: {patch['patch_type']}")
    ax4.set_xlabel('PC1')
    ax4.set_ylabel('PC2')
    ax4.set_title('2D Projection with Interface Patches')
    if patches:
        ax4.legend(fontsize=8)

    # 5. Patch properties
    ax5 = axes[1, 1]
    if patches:
        patch_names = [f"P{i+1}" for i in range(len(patches[:5]))]
        patch_sizes = [p['size'] for p in patches[:5]]
        patch_potentials = [p['binding_potential'] for p in patches[:5]]
        patch_types = [p['patch_type'] for p in patches[:5]]

        colors = {'hydrophobic': 'brown', 'charged': 'blue', 'polar': 'green'}
        bar_colors = [colors.get(t, 'gray') for t in patch_types]

        x = np.arange(len(patch_names))
        ax5.bar(x - 0.2, patch_sizes, 0.4, label='Size', color='lightblue')
        ax5.bar(x + 0.2, [p * 10 for p in patch_potentials], 0.4,
               label='Potential×10', color=bar_colors)
        ax5.set_xticks(x)
        ax5.set_xticklabels(patch_names)
        ax5.set_ylabel('Value')
        ax5.set_title('Surface Patch Properties')
        ax5.legend()
    else:
        ax5.text(0.5, 0.5, 'No patches detected', ha='center', va='center')
        ax5.set_title('Surface Patch Properties')

    # 6. Summary statistics
    ax6 = axes[1, 2]
    ax6.axis('off')

    n_interface = len(interface_residues)
    n_hotspots = sum(1 for r in interface_residues if r['is_hotspot'])
    mean_contacts_all = np.mean(contacts)

    summary_text = f"""
    PPI PREDICTION SUMMARY
    {'='*40}

    Total residues: {n}
    Interface residues: {n_interface} ({100*n_interface/n:.1f}%)
    Binding hotspots: {n_hotspots}

    Mean contacts (all): {mean_contacts_all:.2f}
    Z² optimal: {OPTIMAL_CONTACTS}
    Z² deviation: {mean_contacts_all - OPTIMAL_CONTACTS:+.2f}

    Surface patches: {len(patches)}
    """

    if interface_residues:
        top_hotspots = [r['residue'] for r in interface_residues[:5] if r['is_hotspot']]
        summary_text += f"\n    Top hotspots: {', '.join(top_hotspots[:3])}"

    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.suptitle('Z² Protein-Protein Interaction Prediction', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'ppi_prediction.png'), dpi=150)
    plt.close()

    print(f"  ✓ Visualization saved: {output_dir}/ppi_prediction.png")


def main():
    """Run PPI prediction."""
    print("=" * 70)
    print("Z² PROTEIN-PROTEIN INTERACTION PREDICTION")
    print("=" * 70)
    print(f"Z² = {Z2:.4f}")
    print(f"Optimal contacts = {OPTIMAL_CONTACTS}")
    print("=" * 70)

    print("\n" + "=" * 60)
    print("Z² THEORY FOR PPI")
    print("=" * 60)
    print("""
  Interface residues have UNDER-PACKED coordination.
  They seek binding partners to restore Z² = 8 contacts.

  Key insight: Contact deficiency drives protein binding.
  Hotspots are residues where completion is most favorable.
    """)

    # Find input structure
    pdb_file = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"
    if not os.path.exists(pdb_file):
        print(f"✗ ERROR: PDB file not found: {pdb_file}")
        return None

    # Create output directory
    output_dir = "ppi_prediction"
    os.makedirs(output_dir, exist_ok=True)

    # Parse structure
    print(f"\n  Loading structure: {pdb_file}")
    coords, residues, residue_names = parse_pdb(pdb_file)
    n_residues = len(coords)
    print(f"  Residues: {n_residues}")

    # Calculate contacts
    print("\n" + "=" * 60)
    print("CONTACT ANALYSIS")
    print("=" * 60)
    contacts, contact_matrix, distances = calculate_contacts(coords)
    mean_contacts = np.mean(contacts)
    print(f"  Mean contacts: {mean_contacts:.2f}")
    print(f"  Z² deviation: {mean_contacts - OPTIMAL_CONTACTS:+.2f}")

    # Calculate surface accessibility
    print("\n" + "=" * 60)
    print("SURFACE ACCESSIBILITY")
    print("=" * 60)
    accessibility = calculate_surface_accessibility(coords, contacts)
    n_surface = np.sum(accessibility > SURFACE_CUTOFF)
    print(f"  Surface residues: {n_surface} ({100*n_surface/n_residues:.1f}%)")

    # Identify interface residues
    print("\n" + "=" * 60)
    print("INTERFACE RESIDUE PREDICTION")
    print("=" * 60)
    interface_residues = identify_interface_residues(
        coords, contacts, accessibility, residue_names
    )
    n_interface = len(interface_residues)
    n_hotspots = sum(1 for r in interface_residues if r['is_hotspot'])
    print(f"  Interface candidates: {n_interface}")
    print(f"  Binding hotspots: {n_hotspots}")

    if interface_residues:
        print("\n  Top 5 interface residues:")
        for r in interface_residues[:5]:
            hotspot_marker = " *HOTSPOT*" if r['is_hotspot'] else ""
            print(f"    {r['residue']}: score={r['interface_score']:.3f}, "
                  f"contacts={r['contacts']}, deficiency={r['contact_deficiency']:.1f}{hotspot_marker}")

    # Identify surface patches
    print("\n" + "=" * 60)
    print("SURFACE PATCH ANALYSIS")
    print("=" * 60)
    patches = identify_surface_patches(coords, interface_residues, residue_names, distances)
    print(f"  Binding patches found: {len(patches)}")

    if patches:
        print("\n  Top patches:")
        for i, patch in enumerate(patches[:3]):
            print(f"    Patch {i+1}: {patch['patch_type']}, size={patch['size']}, "
                  f"charge={patch['net_charge']:+.1f}, potential={patch['binding_potential']:.2f}")
            print(f"      Residues: {', '.join(patch['residues'][:5])}...")

    # Predict binding energy
    print("\n" + "=" * 60)
    print("BINDING ENERGY ESTIMATION")
    print("=" * 60)
    binding_energy = predict_binding_energy(interface_residues, patches)
    print(f"  Estimated ΔG: {binding_energy['estimated_dG_kcal_mol']:.1f} kcal/mol")
    print(f"  Binding strength: {binding_energy['binding_strength']}")
    print(f"  Confidence: {binding_energy['confidence']:.2f}")

    # Predict partner types
    print("\n" + "=" * 60)
    print("BINDING PARTNER PREDICTION")
    print("=" * 60)
    partner_predictions = predict_partner_types(patches, interface_residues)

    if partner_predictions:
        for pred in partner_predictions:
            print(f"\n  Patch {pred['patch_id']} ({pred['our_patch_type']}):")
            print(f"    Likely partner: {pred['partner_description']}")
            print(f"    Interaction mode: {pred['interaction_mode']}")
            print(f"    Examples: {', '.join(pred['example_partners'][:2])}")

    # Z² interface analysis
    print("\n" + "=" * 60)
    print("Z² INTERFACE ANALYSIS")
    print("=" * 60)
    z2_analysis = calculate_z2_interface_analysis(contacts, interface_residues)
    print(f"  Overall mean contacts: {z2_analysis['mean_contacts_overall']:.2f}")
    print(f"  Interface mean contacts: {z2_analysis['mean_contacts_interface']:.2f}")
    print(f"  Interface deficiency: {z2_analysis['interface_contact_deficiency']:.2f}")
    print(f"  Z² PPI potential: {z2_analysis['z2_ppi_potential']:.3f}")
    print(f"\n  {z2_analysis['interpretation']}")

    # Create visualization
    create_visualization(coords, contacts, accessibility, interface_residues,
                        patches, residue_names, output_dir)

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_file,
        'n_residues': n_residues,
        'z2_constant': Z2,
        'optimal_contacts': OPTIMAL_CONTACTS,
        'contact_analysis': {
            'mean_contacts': float(mean_contacts),
            'z2_deviation': float(mean_contacts - OPTIMAL_CONTACTS),
            'contacts_per_residue': contacts.tolist()
        },
        'surface_analysis': {
            'n_surface_residues': int(n_surface),
            'surface_fraction': float(n_surface / n_residues),
            'accessibility': accessibility.tolist()
        },
        'interface_prediction': {
            'n_interface_residues': n_interface,
            'n_hotspots': n_hotspots,
            'interface_fraction': float(n_interface / n_residues),
            'top_interface_residues': interface_residues[:20]
        },
        'surface_patches': patches,
        'binding_energy': binding_energy,
        'partner_predictions': partner_predictions,
        'z2_analysis': z2_analysis
    }

    # Save results
    output_file = os.path.join(output_dir, 'ppi_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  ✓ Results saved: {output_file}")

    # Final summary
    print("\n" + "=" * 70)
    print("PPI PREDICTION COMPLETE")
    print("=" * 70)
    print(f"""
  SUMMARY:
  ┌─────────────────────────────────────────────────────────────┐
  │ Interface residues: {n_interface:3d} ({100*n_interface/n_residues:5.1f}%)                       │
  │ Binding hotspots:   {n_hotspots:3d}                                      │
  │ Surface patches:    {len(patches):3d}                                      │
  │ Estimated ΔG:       {binding_energy['estimated_dG_kcal_mol']:6.1f} kcal/mol ({binding_energy['binding_strength']})       │
  │                                                             │
  │ Z² INSIGHT:                                                 │
  │ Interface residues average {z2_analysis['mean_contacts_interface']:.1f} contacts              │
  │ Contact deficiency of {z2_analysis['interface_contact_deficiency']:.1f} drives binding          │
  │ Partners would restore Z² = 8 optimum                       │
  └─────────────────────────────────────────────────────────────┘
    """)

    return results


if __name__ == "__main__":
    results = main()
