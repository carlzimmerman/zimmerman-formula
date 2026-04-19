#!/usr/bin/env python3
"""
Z² Membrane Context Predictor

SPDX-License-Identifier: AGPL-3.0-or-later

Predicts membrane protein topology and lipid interactions using Z² geometry.

THE KEY INSIGHT:
Transmembrane residues achieve Z² = 8 contacts through LIPID interactions
instead of protein-protein contacts.

In soluble proteins: Z² = 8 from protein contacts + water
In membrane proteins: Z² = 8 from protein contacts + lipid tails

MEMBRANE PROTEIN TYPES:
1. Integral (transmembrane): Spans the bilayer
   - Alpha-helical: 20-25 hydrophobic residues per helix
   - Beta-barrel: Alternating in/out pattern
2. Peripheral: Associates with membrane surface
   - Amphipathic helices
   - Lipid anchors
3. Soluble: No membrane association

Methods:
1. Hydrophobicity profiling (transmembrane detection)
2. Amphipathic helix identification (peripheral binding)
3. Charge distribution analysis (membrane topology)
4. Contact deficiency in hydrophobic regions (lipid contacts)
5. Structural feature analysis
6. Membrane embedding simulation

AlphaFold struggles with membrane proteins (no lipid context).
Z² predicts WHERE lipids complete the contact geometry.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
Z = np.sqrt(Z2)       # ≈ 5.7888
OPTIMAL_CONTACTS = 8  # Z² predicts 8 contacts for stable packing

# Membrane parameters
MEMBRANE_THICKNESS = 30.0  # Å (hydrophobic core)
HEADGROUP_THICKNESS = 10.0  # Å per leaflet
TM_HELIX_LENGTH = 20  # Minimum residues for TM helix

print("=" * 70)
print("Z² MEMBRANE CONTEXT PREDICTOR")
print("=" * 70)
print(f"Z² = {Z2:.4f}")
print(f"Membrane thickness = {MEMBRANE_THICKNESS} Å")
print("Predicting membrane topology and lipid interaction sites")
print("=" * 70)

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Kyte-Doolittle hydrophobicity
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
}

# GES (Goldman-Engelman-Steitz) transfer energy scale
# More negative = prefers membrane
GES_SCALE = {
    'F': -3.7, 'M': -3.4, 'I': -3.1, 'L': -2.8, 'V': -2.6,
    'C': -2.0, 'W': -1.9, 'A': -1.6, 'T': -1.2, 'G': -1.0,
    'S': -0.6, 'P': 0.2, 'Y': 0.7, 'H': 3.0, 'Q': 4.1,
    'N': 4.8, 'E': 8.2, 'K': 8.8, 'D': 9.2, 'R': 12.3
}

# Charge at pH 7
CHARGE = {
    'R': 1.0, 'K': 1.0, 'H': 0.1,
    'D': -1.0, 'E': -1.0,
    'A': 0, 'C': 0, 'F': 0, 'G': 0, 'I': 0, 'L': 0,
    'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'S': 0, 'T': 0,
    'V': 0, 'W': 0, 'Y': 0
}

# Helix propensity (Chou-Fasman)
HELIX_PROPENSITY = {
    'A': 1.42, 'L': 1.21, 'E': 1.51, 'M': 1.45, 'Q': 1.11,
    'K': 1.16, 'R': 0.98, 'H': 1.00, 'V': 1.06, 'I': 1.08,
    'Y': 0.69, 'C': 0.70, 'W': 1.08, 'F': 1.13, 'T': 0.83,
    'G': 0.57, 'N': 0.67, 'P': 0.57, 'S': 0.77, 'D': 1.01
}

AA_3TO1 = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

# ==============================================================================
# STRUCTURE PARSING
# ==============================================================================

def parse_structure(pdb_path: str) -> Dict:
    """Parse PDB file for coordinates and sequence."""
    coords = []
    residues = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    res_name = line[17:20].strip()
                    res_num = int(line[22:26])

                    coords.append([x, y, z])
                    residues.append({
                        'name': res_name,
                        'num': res_num,
                        'aa': AA_3TO1.get(res_name, 'X')
                    })
                except ValueError:
                    continue

    sequence = ''.join(r['aa'] for r in residues)

    return {
        'coords': np.array(coords),
        'residues': residues,
        'sequence': sequence,
        'n_residues': len(residues)
    }


# ==============================================================================
# HYDROPHOBICITY ANALYSIS
# ==============================================================================

def compute_hydrophobicity_profile(sequence: str,
                                   window: int = 19) -> Dict:
    """
    Compute hydrophobicity profile using sliding window.

    Window of 19-21 residues detects transmembrane helices.
    """
    n = len(sequence)
    hydro = np.array([HYDROPHOBICITY.get(aa, 0) for aa in sequence])

    # Sliding window average
    if n >= window:
        profile = uniform_filter1d(hydro, size=window, mode='nearest')
    else:
        profile = hydro

    # GES transfer energy
    ges = np.array([GES_SCALE.get(aa, 0) for aa in sequence])
    if n >= window:
        ges_profile = uniform_filter1d(ges, size=window, mode='nearest')
    else:
        ges_profile = ges

    return {
        'hydrophobicity': profile.tolist(),
        'ges_transfer': ges_profile.tolist(),
        'mean_hydrophobicity': float(np.mean(hydro)),
        'max_hydrophobicity': float(np.max(profile)),
        'min_hydrophobicity': float(np.min(profile))
    }


def detect_transmembrane_regions(hydro_profile: List[float],
                                  ges_profile: List[float],
                                  threshold: float = 1.6,
                                  min_length: int = 15,
                                  max_length: int = 35) -> List[Dict]:
    """
    Detect potential transmembrane helices.

    TM helices: 15-35 residues with high hydrophobicity.
    """
    n = len(hydro_profile)
    hydro = np.array(hydro_profile)
    ges = np.array(ges_profile)

    # Find regions above threshold
    above_threshold = hydro > threshold

    tm_regions = []
    i = 0

    while i < n:
        if above_threshold[i]:
            start = i
            while i < n and above_threshold[i]:
                i += 1
            end = i

            length = end - start

            if min_length <= length <= max_length:
                # Calculate properties
                region_hydro = hydro[start:end]
                region_ges = ges[start:end]

                tm_regions.append({
                    'start': start,
                    'end': end - 1,
                    'length': length,
                    'mean_hydrophobicity': float(np.mean(region_hydro)),
                    'max_hydrophobicity': float(np.max(region_hydro)),
                    'mean_ges': float(np.mean(region_ges)),
                    'confidence': min(1.0, (np.mean(region_hydro) - threshold) / 2)
                })
        else:
            i += 1

    return tm_regions


# ==============================================================================
# AMPHIPATHIC HELIX DETECTION
# ==============================================================================

def compute_helical_wheel(sequence: str, start: int, length: int = 18) -> Dict:
    """
    Compute helical wheel properties for amphipathic helix detection.

    Amphipathic helices have one hydrophobic face and one hydrophilic face.
    """
    # Alpha helix: 3.6 residues per turn, 100° per residue
    angle_per_residue = 100 * np.pi / 180

    # Get subsequence
    subseq = sequence[start:start + length]
    if len(subseq) < length:
        return {'hydrophobic_moment': 0, 'mean_hydrophobicity': 0}

    # Compute hydrophobic moment
    hx = 0
    hy = 0

    for i, aa in enumerate(subseq):
        h = HYDROPHOBICITY.get(aa, 0)
        angle = i * angle_per_residue
        hx += h * np.cos(angle)
        hy += h * np.sin(angle)

    hydrophobic_moment = np.sqrt(hx**2 + hy**2) / length
    mean_h = np.mean([HYDROPHOBICITY.get(aa, 0) for aa in subseq])

    # Amphipathic: high moment, moderate mean hydrophobicity
    return {
        'hydrophobic_moment': float(hydrophobic_moment),
        'mean_hydrophobicity': float(mean_h),
        'moment_angle': float(np.arctan2(hy, hx) * 180 / np.pi)
    }


def detect_amphipathic_helices(sequence: str,
                               coords: np.ndarray,
                               moment_threshold: float = 0.4,
                               min_length: int = 11,
                               max_length: int = 25) -> List[Dict]:
    """
    Detect amphipathic helices that could associate with membranes.
    """
    n = len(sequence)
    amphipathic_regions = []

    # Scan with different window sizes
    for length in range(min_length, min(max_length + 1, n + 1)):
        for start in range(n - length + 1):
            wheel = compute_helical_wheel(sequence, start, length)

            # Amphipathic: high moment, moderate hydrophobicity
            if (wheel['hydrophobic_moment'] > moment_threshold and
                -0.5 < wheel['mean_hydrophobicity'] < 2.0):

                # Check helix propensity
                subseq = sequence[start:start + length]
                helix_prop = np.mean([HELIX_PROPENSITY.get(aa, 1.0) for aa in subseq])

                if helix_prop > 1.0:  # Good helix former
                    amphipathic_regions.append({
                        'start': start,
                        'end': start + length - 1,
                        'length': length,
                        'hydrophobic_moment': wheel['hydrophobic_moment'],
                        'mean_hydrophobicity': wheel['mean_hydrophobicity'],
                        'moment_angle': wheel['moment_angle'],
                        'helix_propensity': float(helix_prop),
                        'type': 'amphipathic_helix'
                    })

    # Remove overlapping regions, keep highest moment
    if not amphipathic_regions:
        return []

    amphipathic_regions.sort(key=lambda x: x['hydrophobic_moment'], reverse=True)

    filtered = []
    used_residues = set()

    for region in amphipathic_regions:
        region_residues = set(range(region['start'], region['end'] + 1))
        if len(region_residues & used_residues) < len(region_residues) * 0.5:
            filtered.append(region)
            used_residues.update(region_residues)

    return filtered


# ==============================================================================
# TOPOLOGY PREDICTION
# ==============================================================================

def predict_topology(sequence: str,
                     tm_regions: List[Dict]) -> Dict:
    """
    Predict membrane topology (which termini are inside/outside).

    Uses the positive-inside rule: Arg/Lys prefer cytoplasmic side.
    """
    if not tm_regions:
        return {
            'n_terminus': 'outside',
            'c_terminus': 'outside',
            'n_tm_helices': 0,
            'topology_string': 'o'  # Outside (soluble)
        }

    n = len(sequence)
    n_tm = len(tm_regions)

    # Sort TM regions by position
    tm_sorted = sorted(tm_regions, key=lambda x: x['start'])

    # Analyze loops between TM helices
    loop_charges = []

    # N-terminal loop (before first TM)
    if tm_sorted[0]['start'] > 0:
        n_loop = sequence[:tm_sorted[0]['start']]
        n_charge = sum(CHARGE.get(aa, 0) for aa in n_loop)
        loop_charges.append(('N-term', n_charge))

    # Inter-TM loops
    for i in range(len(tm_sorted) - 1):
        loop_start = tm_sorted[i]['end'] + 1
        loop_end = tm_sorted[i + 1]['start']
        if loop_end > loop_start:
            loop_seq = sequence[loop_start:loop_end]
            loop_charge = sum(CHARGE.get(aa, 0) for aa in loop_seq)
            loop_charges.append((f'Loop{i+1}', loop_charge))

    # C-terminal loop (after last TM)
    if tm_sorted[-1]['end'] < n - 1:
        c_loop = sequence[tm_sorted[-1]['end'] + 1:]
        c_charge = sum(CHARGE.get(aa, 0) for aa in c_loop)
        loop_charges.append(('C-term', c_charge))

    # Positive-inside rule: more positive = cytoplasmic (inside)
    # Determine N-terminus location
    if loop_charges:
        n_term_charge = loop_charges[0][1]
        n_terminus = 'inside' if n_term_charge > 0 else 'outside'
    else:
        n_terminus = 'outside'

    # C-terminus alternates based on number of TM helices
    if n_tm % 2 == 0:
        c_terminus = n_terminus  # Same side as N-term
    else:
        c_terminus = 'inside' if n_terminus == 'outside' else 'outside'

    # Generate topology string
    topology = []
    current = n_terminus[0]  # 'i' or 'o'

    for i, tm in enumerate(tm_sorted):
        topology.append(current)
        topology.append('M')  # Membrane
        current = 'o' if current == 'i' else 'i'

    topology.append(current)

    return {
        'n_terminus': n_terminus,
        'c_terminus': c_terminus,
        'n_tm_helices': n_tm,
        'topology_string': ''.join(topology),
        'loop_charges': loop_charges
    }


# ==============================================================================
# Z² CONTACT ANALYSIS FOR MEMBRANE
# ==============================================================================

def compute_membrane_contact_deficiency(coords: np.ndarray,
                                         sequence: str,
                                         cutoff: float = 8.0) -> Dict:
    """
    Compute contact deficiency considering membrane context.

    In membrane proteins, hydrophobic residues with low contacts
    may be lipid-facing (contacts completed by lipid tails).
    """
    from scipy.spatial.distance import cdist

    n = len(coords)
    distances = cdist(coords, coords)

    contacts = []
    protein_contacts = []
    potential_lipid_contacts = []

    for i in range(n):
        # Count protein contacts
        n_contacts = 0
        for j in range(n):
            if abs(i - j) > 2 and distances[i, j] < cutoff:
                n_contacts += 1

        protein_contacts.append(n_contacts)
        contacts.append(n_contacts)

        # Estimate potential lipid contacts for hydrophobic residues
        aa = sequence[i]
        hydro = HYDROPHOBICITY.get(aa, 0)

        # Hydrophobic residues with contact deficiency might be lipid-facing
        deficiency = OPTIMAL_CONTACTS - n_contacts
        if hydro > 1.5 and deficiency > 2:
            # Could be filled by lipid contacts
            lipid_contacts = min(deficiency, 4)  # Up to 4 lipid contacts
        else:
            lipid_contacts = 0

        potential_lipid_contacts.append(lipid_contacts)

    return {
        'protein_contacts': protein_contacts,
        'potential_lipid_contacts': potential_lipid_contacts,
        'total_contacts': [p + l for p, l in zip(protein_contacts, potential_lipid_contacts)],
        'mean_protein_contacts': float(np.mean(protein_contacts)),
        'lipid_contact_residues': sum(1 for l in potential_lipid_contacts if l > 0)
    }


# ==============================================================================
# MEMBRANE EMBEDDING ANALYSIS
# ==============================================================================

def analyze_membrane_embedding(coords: np.ndarray,
                               sequence: str,
                               tm_regions: List[Dict]) -> Dict:
    """
    Analyze how the protein might embed in a membrane.

    Estimates tilt angle and penetration depth.
    """
    if not tm_regions:
        return {
            'is_membrane_protein': False,
            'embedding_type': 'soluble',
            'tilt_angle': 0,
            'penetration_depth': 0
        }

    n = len(coords)

    # Get TM region coordinates
    tm_indices = []
    for tm in tm_regions:
        tm_indices.extend(range(tm['start'], tm['end'] + 1))

    if not tm_indices:
        return {
            'is_membrane_protein': False,
            'embedding_type': 'soluble',
            'tilt_angle': 0,
            'penetration_depth': 0
        }

    tm_coords = coords[tm_indices]

    # Principal axis of TM region (approximate helix axis)
    centered = tm_coords - tm_coords.mean(axis=0)
    U, S, Vt = np.linalg.svd(centered)

    # First principal component is helix axis
    helix_axis = Vt[0]

    # Membrane normal is typically along z-axis (0, 0, 1)
    membrane_normal = np.array([0, 0, 1])

    # Tilt angle between helix axis and membrane normal
    cos_angle = abs(np.dot(helix_axis, membrane_normal))
    tilt_angle = np.arccos(cos_angle) * 180 / np.pi

    # Span of TM region along membrane normal
    z_coords = tm_coords[:, 2]
    z_span = z_coords.max() - z_coords.min()

    # Estimate penetration depth
    penetration = min(z_span, MEMBRANE_THICKNESS)

    # Classify embedding type
    if len(tm_regions) > 0 and penetration > 20:
        embedding_type = 'transmembrane'
    elif penetration > 10:
        embedding_type = 'partially_embedded'
    else:
        embedding_type = 'peripheral'

    return {
        'is_membrane_protein': True,
        'embedding_type': embedding_type,
        'tilt_angle': float(tilt_angle),
        'penetration_depth': float(penetration),
        'z_span': float(z_span),
        'helix_axis': helix_axis.tolist(),
        'n_tm_residues': len(tm_indices)
    }


# ==============================================================================
# PROTEIN CLASSIFICATION
# ==============================================================================

def classify_membrane_association(sequence: str,
                                   hydro_profile: Dict,
                                   tm_regions: List[Dict],
                                   amphipathic: List[Dict],
                                   contact_analysis: Dict) -> Dict:
    """
    Classify the protein's membrane association type.
    """
    n = len(sequence)

    # Calculate various scores
    mean_hydro = hydro_profile['mean_hydrophobicity']
    max_hydro = hydro_profile['max_hydrophobicity']
    n_tm = len(tm_regions)
    n_amphipathic = len(amphipathic)
    lipid_residues = contact_analysis['lipid_contact_residues']

    # Scoring
    scores = {
        'integral_alpha': 0.0,
        'peripheral': 0.0,
        'lipid_anchored': 0.0,
        'soluble': 0.0
    }

    # Integral (transmembrane) evidence
    if n_tm >= 1:
        scores['integral_alpha'] += 0.4
        scores['integral_alpha'] += 0.1 * min(n_tm, 5)

    if max_hydro > 2.0:
        scores['integral_alpha'] += 0.2

    # Peripheral evidence
    if n_amphipathic >= 1:
        scores['peripheral'] += 0.3
        scores['peripheral'] += 0.1 * min(n_amphipathic, 3)

    if 0 < mean_hydro < 1.5:
        scores['peripheral'] += 0.2

    # Lipid-anchored evidence
    # Check for lipidation motifs at termini
    n_term = sequence[:10]
    c_term = sequence[-10:]

    # Myristoylation: G at position 2
    if len(sequence) > 1 and sequence[1] == 'G':
        scores['lipid_anchored'] += 0.2

    # GPI anchor: hydrophobic C-terminus
    c_hydro = np.mean([HYDROPHOBICITY.get(aa, 0) for aa in c_term])
    if c_hydro > 1.0:
        scores['lipid_anchored'] += 0.1

    # Soluble evidence
    if mean_hydro < 0:
        scores['soluble'] += 0.3

    if n_tm == 0 and n_amphipathic == 0:
        scores['soluble'] += 0.3

    if lipid_residues < 5:
        scores['soluble'] += 0.2

    # Normalize
    total = sum(scores.values())
    if total > 0:
        for key in scores:
            scores[key] /= total

    # Predict class
    predicted_class = max(scores, key=scores.get)
    confidence = scores[predicted_class]

    return {
        'predicted_class': predicted_class,
        'confidence': float(confidence),
        'class_probabilities': {k: float(v) for k, v in scores.items()},
        'evidence': {
            'n_tm_helices': n_tm,
            'n_amphipathic_helices': n_amphipathic,
            'mean_hydrophobicity': float(mean_hydro),
            'max_hydrophobicity': float(max_hydro),
            'lipid_contact_residues': lipid_residues
        }
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def generate_membrane_visualization(sequence: str,
                                    hydro_profile: Dict,
                                    tm_regions: List[Dict],
                                    amphipathic: List[Dict],
                                    classification: Dict,
                                    coords: np.ndarray,
                                    output_path: str):
    """Generate membrane context visualization."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    n = len(sequence)
    fig = plt.figure(figsize=(16, 12))

    # 1. Hydrophobicity profile
    ax1 = fig.add_subplot(2, 2, 1)

    x = range(n)
    ax1.plot(x, hydro_profile['hydrophobicity'], 'b-', linewidth=1.5, label='Kyte-Doolittle')
    ax1.axhline(y=1.6, color='red', linestyle='--', label='TM threshold')
    ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.5)

    # Shade TM regions
    for tm in tm_regions:
        ax1.axvspan(tm['start'], tm['end'], alpha=0.3, color='orange', label='_')

    # Mark amphipathic regions
    for amp in amphipathic:
        ax1.axvspan(amp['start'], amp['end'], alpha=0.2, color='green', label='_')

    ax1.set_xlabel('Residue Position')
    ax1.set_ylabel('Hydrophobicity')
    ax1.set_title('Hydrophobicity Profile (orange=TM, green=amphipathic)')
    ax1.legend(loc='upper right')
    ax1.set_xlim(0, n)

    # 2. Topology diagram
    ax2 = fig.add_subplot(2, 2, 2)

    # Draw membrane
    membrane_y = 0.5
    membrane_height = 0.3

    ax2.axhspan(membrane_y - membrane_height/2, membrane_y + membrane_height/2,
                color='yellow', alpha=0.5, label='Membrane')

    # Draw topology
    if tm_regions:
        current_y = 0.9  # Start outside (top)
        current_x = 0

        for i, tm in enumerate(tm_regions):
            # Loop before TM
            loop_x = (current_x + tm['start']) / 2 / n
            ax2.plot([current_x/n, loop_x, tm['start']/n],
                    [current_y, current_y, membrane_y],
                    'b-', linewidth=2)

            # TM helix
            next_y = 0.1 if current_y > 0.5 else 0.9
            ax2.plot([tm['start']/n, tm['end']/n],
                    [membrane_y, membrane_y],
                    'r-', linewidth=4)

            current_x = tm['end']
            current_y = next_y

        # Final loop
        ax2.plot([current_x/n, 1], [current_y, current_y], 'b-', linewidth=2)

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Sequence Position (normalized)')
    ax2.set_ylabel('Location')
    ax2.set_title('Membrane Topology')
    ax2.set_yticks([0.1, 0.5, 0.9])
    ax2.set_yticklabels(['Inside', 'Membrane', 'Outside'])

    # 3. 3D structure with membrane plane
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')

    # Plot protein
    ax3.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
               c='lightgray', s=30, alpha=0.5)

    # Highlight TM residues
    if tm_regions:
        for tm in tm_regions:
            tm_coords = coords[tm['start']:tm['end']+1]
            ax3.scatter(tm_coords[:, 0], tm_coords[:, 1], tm_coords[:, 2],
                       c='orange', s=60, alpha=0.8)

    # Draw membrane plane
    center = coords.mean(axis=0)
    xx, yy = np.meshgrid(
        np.linspace(coords[:, 0].min() - 5, coords[:, 0].max() + 5, 10),
        np.linspace(coords[:, 1].min() - 5, coords[:, 1].max() + 5, 10)
    )
    zz = np.ones_like(xx) * center[2]

    ax3.plot_surface(xx, yy, zz, alpha=0.2, color='yellow')

    ax3.set_xlabel('X (Å)')
    ax3.set_ylabel('Y (Å)')
    ax3.set_zlabel('Z (Å)')
    ax3.set_title('Structure with Membrane Plane')

    # 4. Classification results
    ax4 = fig.add_subplot(2, 2, 4)

    classes = list(classification['class_probabilities'].keys())
    probs = [classification['class_probabilities'][c] for c in classes]

    colors = ['green' if c == classification['predicted_class'] else 'gray' for c in classes]
    bars = ax4.barh(classes, probs, color=colors)

    ax4.set_xlabel('Probability')
    ax4.set_title(f"Predicted: {classification['predicted_class'].upper()}\n"
                 f"Confidence: {classification['confidence']:.2f}")
    ax4.set_xlim(0, 1)

    for bar, prob in zip(bars, probs):
        ax4.text(prob + 0.02, bar.get_y() + bar.get_height()/2,
                f'{prob:.2f}', va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Visualization saved: {output_path}")


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def analyze_membrane_context(pdb_path: str,
                             output_dir: str = "membrane_context") -> Dict:
    """
    Full membrane context analysis pipeline.
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nLoading structure: {pdb_path}")
    structure = parse_structure(pdb_path)
    coords = structure['coords']
    residues = structure['residues']
    sequence = structure['sequence']
    n_residues = structure['n_residues']

    print(f"  Residues: {n_residues}")
    print(f"  Sequence: {sequence[:50]}..." if len(sequence) > 50 else f"  Sequence: {sequence}")

    # 1. Hydrophobicity analysis
    print("\nComputing hydrophobicity profile...")
    hydro = compute_hydrophobicity_profile(sequence)
    print(f"  Mean hydrophobicity: {hydro['mean_hydrophobicity']:.2f}")
    print(f"  Max hydrophobicity: {hydro['max_hydrophobicity']:.2f}")

    # 2. Transmembrane detection
    print("\nDetecting transmembrane regions...")
    tm_regions = detect_transmembrane_regions(
        hydro['hydrophobicity'],
        hydro['ges_transfer']
    )
    print(f"  TM helices detected: {len(tm_regions)}")

    for tm in tm_regions:
        print(f"    {tm['start']+1}-{tm['end']+1}: {tm['length']} residues, "
              f"hydro={tm['mean_hydrophobicity']:.2f}")

    # 3. Amphipathic helix detection
    print("\nDetecting amphipathic helices...")
    amphipathic = detect_amphipathic_helices(sequence, coords)
    print(f"  Amphipathic helices: {len(amphipathic)}")

    for amp in amphipathic[:3]:
        print(f"    {amp['start']+1}-{amp['end']+1}: moment={amp['hydrophobic_moment']:.2f}")

    # 4. Topology prediction
    print("\nPredicting topology...")
    topology = predict_topology(sequence, tm_regions)
    print(f"  N-terminus: {topology['n_terminus']}")
    print(f"  C-terminus: {topology['c_terminus']}")
    print(f"  Topology: {topology['topology_string']}")

    # 5. Contact analysis
    print("\nAnalyzing Z² contacts in membrane context...")
    contacts = compute_membrane_contact_deficiency(coords, sequence)
    print(f"  Mean protein contacts: {contacts['mean_protein_contacts']:.1f}")
    print(f"  Potential lipid-contact residues: {contacts['lipid_contact_residues']}")

    # 6. Embedding analysis
    print("\nAnalyzing membrane embedding...")
    embedding = analyze_membrane_embedding(coords, sequence, tm_regions)
    print(f"  Embedding type: {embedding['embedding_type']}")
    if embedding['is_membrane_protein']:
        print(f"  Tilt angle: {embedding['tilt_angle']:.1f}°")
        print(f"  Penetration depth: {embedding['penetration_depth']:.1f} Å")

    # 7. Classification
    print("\nClassifying membrane association...")
    classification = classify_membrane_association(
        sequence, hydro, tm_regions, amphipathic, contacts
    )

    print(f"\n{'='*60}")
    print("MEMBRANE CONTEXT PREDICTION")
    print(f"{'='*60}")
    print(f"  Predicted class: {classification['predicted_class'].upper()}")
    print(f"  Confidence: {classification['confidence']:.2f}")
    print(f"\n  Probabilities:")
    for cls, prob in classification['class_probabilities'].items():
        marker = " ←" if cls == classification['predicted_class'] else ""
        print(f"    {cls}: {prob:.3f}{marker}")

    # 8. Generate visualization
    print(f"\n{'='*60}")
    print("GENERATING OUTPUTS")
    print(f"{'='*60}")

    viz_path = os.path.join(output_dir, "membrane_context.png")
    generate_membrane_visualization(
        sequence, hydro, tm_regions, amphipathic,
        classification, coords, viz_path
    )

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_path,
        'sequence': sequence,
        'n_residues': n_residues,
        'z2_constant': Z2,
        'hydrophobicity': {
            'mean': hydro['mean_hydrophobicity'],
            'max': hydro['max_hydrophobicity'],
            'min': hydro['min_hydrophobicity'],
            'profile': hydro['hydrophobicity']
        },
        'transmembrane_regions': tm_regions,
        'amphipathic_helices': amphipathic,
        'topology': topology,
        'contact_analysis': contacts,
        'embedding': embedding,
        'classification': classification,
        'output_files': {
            'visualization': viz_path
        }
    }

    # Save JSON
    json_path = os.path.join(output_dir, "membrane_results.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  ✓ Results saved: {json_path}")

    # Summary
    print(f"\n{'='*60}")
    print("Z² MEMBRANE CONTEXT ANALYSIS COMPLETE")
    print(f"{'='*60}")

    if classification['predicted_class'] == 'soluble':
        interpretation = f"""
  This protein is predicted to be SOLUBLE.

  Z² INTERPRETATION:
  - Mean hydrophobicity: {hydro['mean_hydrophobicity']:.2f} (below membrane threshold)
  - No transmembrane helices detected
  - Z² = 8 contacts achieved through protein + water
  - No lipid contacts needed for structural stability

  This protein would remain in the aqueous phase
  and not associate with lipid membranes.
"""
    elif classification['predicted_class'] == 'integral_alpha':
        interpretation = f"""
  This protein is predicted to be an INTEGRAL MEMBRANE PROTEIN.

  Z² INTERPRETATION:
  - {len(tm_regions)} transmembrane helix(es) detected
  - Hydrophobic residues achieve Z² = 8 through LIPID contacts
  - Topology: {topology['topology_string']}

  In the membrane: lipid tails complete the contact geometry
  that protein contacts alone cannot provide.
"""
    elif classification['predicted_class'] == 'peripheral':
        interpretation = f"""
  This protein is predicted to be a PERIPHERAL MEMBRANE PROTEIN.

  Z² INTERPRETATION:
  - {len(amphipathic)} amphipathic helix(es) detected
  - Associates with membrane surface, doesn't span bilayer
  - Partial lipid contacts supplement protein contacts

  The amphipathic face inserts into the lipid headgroup region.
"""
    else:
        interpretation = f"""
  Protein classification: {classification['predicted_class'].upper()}

  Z² contacts may be partially completed by lipid interactions.
"""

    print(interpretation)

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run membrane context analysis on Z² protein."""
    import sys

    if len(sys.argv) > 1:
        pdb_path = sys.argv[1]
    else:
        pdb_path = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

    if not os.path.exists(pdb_path):
        print(f"PDB not found: {pdb_path}")
        return None

    results = analyze_membrane_context(pdb_path, output_dir="membrane_context")

    return results


if __name__ == "__main__":
    results = main()
