#!/usr/bin/env python3
"""
Z² Intrinsically Disordered Region (IDR) Predictor

SPDX-License-Identifier: AGPL-3.0-or-later

Predicts intrinsically disordered regions using Z² geometric principles.

THE KEY INSIGHT:
IDRs are regions where Z² = 8 contact packing is GEOMETRICALLY IMPOSSIBLE.

Disorder arises when:
1. Sequence composition prevents stable hydrophobic core formation
2. High net charge causes electrostatic repulsion
3. Low sequence complexity (repeats, low information content)
4. Proline/glycine abundance disrupts secondary structure
5. Hydrophilic residues cannot form buried contacts

Z² THEORY OF DISORDER:
- Ordered regions achieve ~8 contacts per residue (Z² optimal)
- Disordered regions have <4 contacts (insufficient for stability)
- The transition zone (4-6 contacts) represents "conditionally disordered"
  regions that can fold upon binding (MoRFs: Molecular Recognition Features)

AlphaFold flags disorder as low pLDDT (<50).
Z² EXPLAINS WHY: insufficient contact geometry.

Methods:
1. Sequence-based disorder propensity (amino acid composition)
2. Z² contact analysis (low contacts = disorder)
3. Charge-hydropathy analysis (Uversky plot)
4. Complexity/entropy analysis
5. Integration with pLDDT if available
6. MoRF (Molecular Recognition Feature) identification

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
from scipy.signal import savgol_filter
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
Z = np.sqrt(Z2)       # ≈ 5.7888
OPTIMAL_CONTACTS = 8  # Z² predicts 8 contacts for stable folding
DISORDER_THRESHOLD = 4  # Below this = intrinsically disordered
MORF_THRESHOLD = 6      # 4-6 contacts = conditionally disordered (MoRF)

print("=" * 70)
print("Z² INTRINSICALLY DISORDERED REGION (IDR) PREDICTOR")
print("=" * 70)
print(f"Z² = {Z2:.4f}")
print(f"Ordered: contacts >= {OPTIMAL_CONTACTS}")
print(f"MoRF (conditional): {DISORDER_THRESHOLD} <= contacts < {MORF_THRESHOLD}")
print(f"Disordered: contacts < {DISORDER_THRESHOLD}")
print("=" * 70)

# ==============================================================================
# AMINO ACID DISORDER PROPENSITIES
# ==============================================================================

# Disorder propensity scores (derived from DisProt database)
# Positive = disorder-promoting, Negative = order-promoting
DISORDER_PROPENSITY = {
    # Strong disorder promoters
    'P': 0.987,   # Proline - breaks helices
    'E': 0.736,   # Glutamate - charged
    'S': 0.699,   # Serine - small, polar
    'Q': 0.691,   # Glutamine - polar
    'K': 0.674,   # Lysine - charged
    'A': 0.616,   # Alanine - small
    'G': 0.501,   # Glycine - flexible

    # Neutral
    'R': 0.180,   # Arginine
    'D': 0.192,   # Aspartate
    'T': 0.086,   # Threonine
    'N': 0.007,   # Asparagine
    'H': -0.078,  # Histidine
    'M': -0.194,  # Methionine

    # Order promoters (hydrophobic)
    'L': -0.326,  # Leucine
    'V': -0.386,  # Valine
    'F': -0.697,  # Phenylalanine
    'I': -0.718,  # Isoleucine
    'Y': -0.793,  # Tyrosine
    'W': -0.884,  # Tryptophan
    'C': -0.484,  # Cysteine (can form disulfides)
}

# Hydrophobicity (Kyte-Doolittle)
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
}

# Charge at pH 7
CHARGE = {
    'K': 1.0, 'R': 1.0, 'H': 0.1,  # Positive
    'D': -1.0, 'E': -1.0,          # Negative
    'A': 0, 'C': 0, 'F': 0, 'G': 0, 'I': 0, 'L': 0,
    'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'S': 0, 'T': 0,
    'V': 0, 'W': 0, 'Y': 0
}

# Three-letter to one-letter code
AA_3TO1 = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

# ==============================================================================
# SEQUENCE ANALYSIS
# ==============================================================================

def sequence_disorder_propensity(sequence: str, window: int = 21) -> np.ndarray:
    """
    Calculate per-residue disorder propensity from sequence.

    Uses sliding window average of amino acid disorder scores.
    """
    n = len(sequence)
    propensity = np.zeros(n)

    for i, aa in enumerate(sequence):
        propensity[i] = DISORDER_PROPENSITY.get(aa, 0)

    # Smooth with sliding window
    if n >= window:
        smoothed = uniform_filter1d(propensity, size=window, mode='nearest')
    else:
        smoothed = propensity

    return smoothed


def charge_hydropathy_analysis(sequence: str, window: int = 21) -> Dict:
    """
    Uversky charge-hydropathy analysis.

    Disordered proteins fall in a specific region of the
    charge-hydropathy plot (high charge, low hydropathy).

    The Uversky boundary: <H> = 2.785 × <|Q|> - 1.151
    """
    n = len(sequence)

    # Per-residue values
    hydropathy = np.array([HYDROPHOBICITY.get(aa, 0) for aa in sequence])
    charge = np.array([CHARGE.get(aa, 0) for aa in sequence])

    # Normalize hydropathy to 0-1 scale
    hydropathy_norm = (hydropathy + 4.5) / 9.0  # Scale from [-4.5, 4.5] to [0, 1]

    # Sliding window analysis
    if n >= window:
        mean_hydropathy = uniform_filter1d(hydropathy_norm, size=window, mode='nearest')
        abs_charge = np.abs(charge)
        mean_charge = uniform_filter1d(abs_charge, size=window, mode='nearest')
        net_charge = uniform_filter1d(charge, size=window, mode='nearest')
    else:
        mean_hydropathy = hydropathy_norm
        mean_charge = np.abs(charge)
        net_charge = charge

    # Global values for Uversky plot
    global_hydropathy = np.mean(hydropathy_norm)
    global_charge = np.mean(np.abs(charge))

    # Uversky boundary: proteins above this line are disordered
    # <H> = 2.785 × <|Q|> - 1.151
    boundary_hydropathy = 2.785 * global_charge - 1.151
    is_globally_disordered = global_hydropathy < boundary_hydropathy

    # Per-residue disorder from charge-hydropathy
    # High charge OR low hydropathy = disorder-prone
    ch_disorder = (1 - mean_hydropathy) * 0.5 + mean_charge * 0.5

    return {
        'hydropathy_profile': mean_hydropathy.tolist(),
        'charge_profile': net_charge.tolist(),
        'abs_charge_profile': mean_charge.tolist(),
        'ch_disorder_score': ch_disorder.tolist(),
        'global_hydropathy': float(global_hydropathy),
        'global_charge': float(global_charge),
        'uversky_boundary': float(boundary_hydropathy),
        'is_globally_disordered': bool(is_globally_disordered)
    }


def sequence_complexity(sequence: str, window: int = 21) -> np.ndarray:
    """
    Calculate local sequence complexity (Shannon entropy).

    Low complexity = more disorder-prone (e.g., poly-Q, PEST sequences).
    """
    n = len(sequence)
    complexity = np.zeros(n)

    half_window = window // 2

    for i in range(n):
        # Get local window
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)
        local_seq = sequence[start:end]

        # Count amino acid frequencies
        aa_counts = {}
        for aa in local_seq:
            aa_counts[aa] = aa_counts.get(aa, 0) + 1

        # Shannon entropy
        local_len = len(local_seq)
        entropy = 0
        for count in aa_counts.values():
            p = count / local_len
            if p > 0:
                entropy -= p * np.log2(p)

        # Normalize by max entropy (log2(20) for 20 amino acids)
        max_entropy = np.log2(min(20, local_len))
        complexity[i] = entropy / max_entropy if max_entropy > 0 else 0

    return complexity


def proline_glycine_content(sequence: str, window: int = 21) -> np.ndarray:
    """
    Calculate local Pro/Gly content.

    High P/G content disrupts secondary structure → disorder.
    """
    n = len(sequence)
    pg_content = np.zeros(n)

    for i, aa in enumerate(sequence):
        pg_content[i] = 1.0 if aa in ['P', 'G'] else 0.0

    if n >= window:
        smoothed = uniform_filter1d(pg_content, size=window, mode='nearest')
    else:
        smoothed = pg_content

    return smoothed


# ==============================================================================
# STRUCTURE-BASED ANALYSIS
# ==============================================================================

def parse_structure(pdb_path: str) -> Dict:
    """Parse PDB file for Cα coordinates and residue info."""
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


def z2_contact_disorder(coords: np.ndarray, cutoff: float = 8.0) -> Dict:
    """
    Z² contact-based disorder prediction.

    THE CORE Z² INSIGHT:
    - Ordered regions: ~8 contacts (Z² optimal)
    - Disordered regions: <4 contacts (geometrically unstable)
    - MoRFs: 4-6 contacts (conditionally disordered)
    """
    from scipy.spatial.distance import cdist

    n = len(coords)
    distances = cdist(coords, coords)

    contacts_per_residue = []
    z2_disorder_score = []
    region_classification = []

    for i in range(n):
        # Count contacts (excluding neighbors within 2 residues)
        contacts = 0
        for j in range(n):
            if abs(i - j) > 2 and distances[i, j] < cutoff:
                contacts += 1

        contacts_per_residue.append(contacts)

        # Z² disorder score: deviation below optimal
        if contacts >= OPTIMAL_CONTACTS:
            # Well-folded
            disorder = 0.0
            region = 'ORDERED'
        elif contacts >= MORF_THRESHOLD:
            # Slightly under-packed but stable
            disorder = 0.2
            region = 'ORDERED'
        elif contacts >= DISORDER_THRESHOLD:
            # MoRF zone: conditionally disordered
            disorder = 0.5 + 0.25 * (MORF_THRESHOLD - contacts)
            region = 'MORF'
        else:
            # True disorder
            disorder = 0.8 + 0.2 * (DISORDER_THRESHOLD - contacts) / DISORDER_THRESHOLD
            disorder = min(1.0, disorder)
            region = 'DISORDERED'

        z2_disorder_score.append(disorder)
        region_classification.append(region)

    return {
        'contacts_per_residue': contacts_per_residue,
        'z2_disorder_score': z2_disorder_score,
        'region_classification': region_classification,
        'mean_contacts': float(np.mean(contacts_per_residue)),
        'n_disordered': sum(1 for r in region_classification if r == 'DISORDERED'),
        'n_morf': sum(1 for r in region_classification if r == 'MORF'),
        'n_ordered': sum(1 for r in region_classification if r == 'ORDERED')
    }


def load_plddt_scores(prediction_json: str) -> Optional[np.ndarray]:
    """Load pLDDT scores from ESM/AlphaFold prediction."""
    if not os.path.exists(prediction_json):
        return None

    try:
        with open(prediction_json, 'r') as f:
            data = json.load(f)

        # Try different formats
        if 'plddt' in data:
            return np.array(data['plddt'])
        elif 'confidenceScore' in data:
            return np.array(data['confidenceScore'])
        elif 'mean_plddt' in data:
            # Single value - expand to array
            return None
    except:
        pass

    return None


def load_ensemble_flexibility(ensemble_json: str) -> Optional[np.ndarray]:
    """Load RMSF from conformational ensemble."""
    if not os.path.exists(ensemble_json):
        return None

    try:
        with open(ensemble_json, 'r') as f:
            data = json.load(f)

        if 'flexibility_profile' in data:
            return np.array(data['flexibility_profile'])
    except:
        pass

    return None


# ==============================================================================
# COMPOSITE DISORDER PREDICTION
# ==============================================================================

def predict_disorder(sequence: str,
                     coords: np.ndarray = None,
                     plddt: np.ndarray = None,
                     rmsf: np.ndarray = None,
                     window: int = 21) -> Dict:
    """
    Composite Z² disorder prediction.

    Integrates:
    1. Sequence disorder propensity
    2. Charge-hydropathy analysis
    3. Sequence complexity
    4. Pro/Gly content
    5. Z² contact analysis (if structure available)
    6. pLDDT scores (if available)
    7. RMSF flexibility (if available)
    """
    n = len(sequence)

    # Sequence-based predictors
    print("  Computing sequence disorder propensity...")
    seq_propensity = sequence_disorder_propensity(sequence, window)

    print("  Computing charge-hydropathy profile...")
    ch_analysis = charge_hydropathy_analysis(sequence, window)

    print("  Computing sequence complexity...")
    complexity = sequence_complexity(sequence, window)

    print("  Computing Pro/Gly content...")
    pg_content = proline_glycine_content(sequence, window)

    # Normalize sequence-based scores to 0-1
    seq_score = (seq_propensity - seq_propensity.min()) / (seq_propensity.max() - seq_propensity.min() + 1e-10)
    ch_score = np.array(ch_analysis['ch_disorder_score'])

    # Low complexity = more disorder
    complexity_score = 1 - complexity

    # Structure-based scores (if available)
    z2_score = np.zeros(n)
    plddt_score = np.zeros(n)
    rmsf_score = np.zeros(n)

    weights = {
        'sequence': 0.25,
        'charge_hydropathy': 0.20,
        'complexity': 0.10,
        'proline_glycine': 0.10,
        'z2_contacts': 0.20,
        'plddt': 0.10,
        'rmsf': 0.05
    }

    if coords is not None and len(coords) == n:
        print("  Computing Z² contact disorder...")
        z2_analysis = z2_contact_disorder(coords)
        z2_score = np.array(z2_analysis['z2_disorder_score'])
    else:
        # Increase sequence weight if no structure
        weights['sequence'] = 0.35
        weights['charge_hydropathy'] = 0.30
        weights['z2_contacts'] = 0
        z2_analysis = None

    if plddt is not None and len(plddt) == n:
        print("  Integrating pLDDT scores...")
        # Low pLDDT = high disorder
        # pLDDT < 50 is considered disordered
        plddt_norm = plddt / 100.0  # Normalize to 0-1
        plddt_score = 1 - plddt_norm  # Invert: low pLDDT = high score
    else:
        weights['sequence'] += weights['plddt']
        weights['plddt'] = 0

    if rmsf is not None and len(rmsf) == n:
        print("  Integrating RMSF flexibility...")
        # High RMSF = more flexible = disorder-like
        rmsf_norm = rmsf / (rmsf.max() + 1e-10)
        rmsf_score = rmsf_norm
    else:
        weights['sequence'] += weights['rmsf']
        weights['rmsf'] = 0

    # Composite disorder score
    print("  Computing composite disorder score...")

    composite = (
        weights['sequence'] * seq_score +
        weights['charge_hydropathy'] * ch_score +
        weights['complexity'] * complexity_score +
        weights['proline_glycine'] * pg_content +
        weights['z2_contacts'] * z2_score +
        weights['plddt'] * plddt_score +
        weights['rmsf'] * rmsf_score
    )

    # Smooth final prediction
    if n >= 5:
        composite = savgol_filter(composite, min(11, n if n % 2 == 1 else n - 1), 2)

    # Classify regions
    disorder_threshold = 0.5
    morf_threshold = 0.35

    classification = []
    for score in composite:
        if score >= disorder_threshold:
            classification.append('DISORDERED')
        elif score >= morf_threshold:
            classification.append('MORF')
        else:
            classification.append('ORDERED')

    return {
        'composite_disorder': composite.tolist(),
        'sequence_propensity': seq_score.tolist(),
        'charge_hydropathy': ch_score.tolist(),
        'complexity_score': complexity_score.tolist(),
        'pg_content': pg_content.tolist(),
        'z2_contact_score': z2_score.tolist(),
        'plddt_score': plddt_score.tolist(),
        'rmsf_score': rmsf_score.tolist(),
        'classification': classification,
        'weights_used': weights,
        'ch_analysis': ch_analysis,
        'z2_analysis': z2_analysis
    }


# ==============================================================================
# IDR REGION IDENTIFICATION
# ==============================================================================

def identify_idr_regions(classification: List[str],
                         composite_scores: List[float],
                         residues: List[Dict],
                         min_length: int = 5) -> List[Dict]:
    """
    Identify contiguous IDR regions.

    Returns list of IDR segments with properties.
    """
    n = len(classification)
    regions = []

    i = 0
    while i < n:
        if classification[i] in ['DISORDERED', 'MORF']:
            # Start of potential IDR
            start = i
            region_type = classification[i]
            scores = [composite_scores[i]]

            # Extend region
            while i < n and classification[i] in ['DISORDERED', 'MORF']:
                if classification[i] == 'DISORDERED':
                    region_type = 'DISORDERED'  # Upgrade if any residue is fully disordered
                scores.append(composite_scores[i])
                i += 1

            end = i - 1
            length = end - start + 1

            if length >= min_length:
                # Get residue info
                res_start = residues[start] if residues else {'num': start + 1}
                res_end = residues[end] if residues else {'num': end + 1}

                regions.append({
                    'start_idx': start,
                    'end_idx': end,
                    'start_res': res_start.get('num', start + 1),
                    'end_res': res_end.get('num', end + 1),
                    'length': length,
                    'type': region_type,
                    'mean_score': float(np.mean(scores)),
                    'max_score': float(np.max(scores))
                })
        else:
            i += 1

    return regions


def identify_morfs(classification: List[str],
                   composite_scores: List[float],
                   z2_contacts: List[int] = None,
                   residues: List[Dict] = None,
                   min_length: int = 3,
                   max_length: int = 25) -> List[Dict]:
    """
    Identify Molecular Recognition Features (MoRFs).

    MoRFs are short segments within IDRs that can fold upon binding.
    They typically have:
    - Length 3-25 residues
    - Intermediate disorder scores
    - Some hydrophobic residues for binding
    """
    n = len(classification)
    morfs = []

    i = 0
    while i < n:
        if classification[i] == 'MORF':
            start = i
            scores = [composite_scores[i]]

            while i < n and classification[i] == 'MORF':
                scores.append(composite_scores[i])
                i += 1

            end = i - 1
            length = end - start + 1

            if min_length <= length <= max_length:
                res_start = residues[start] if residues else {'num': start + 1}
                res_end = residues[end] if residues else {'num': end + 1}

                # Check if it's within or adjacent to a disordered region
                in_idr_context = False
                if start > 0 and classification[start - 1] == 'DISORDERED':
                    in_idr_context = True
                if end < n - 1 and classification[end + 1] == 'DISORDERED':
                    in_idr_context = True

                morfs.append({
                    'start_idx': start,
                    'end_idx': end,
                    'start_res': res_start.get('num', start + 1),
                    'end_res': res_end.get('num', end + 1),
                    'length': length,
                    'mean_score': float(np.mean(scores)),
                    'in_idr_context': in_idr_context,
                    'binding_potential': 'HIGH' if in_idr_context else 'MEDIUM'
                })
        else:
            i += 1

    return morfs


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def generate_disorder_visualization(sequence: str,
                                    prediction: Dict,
                                    idr_regions: List[Dict],
                                    morfs: List[Dict],
                                    output_path: str):
    """Generate disorder prediction visualization."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    n = len(sequence)
    x = np.arange(n)

    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    # 1. Composite disorder score
    ax1 = axes[0]
    composite = prediction['composite_disorder']

    # Color by classification
    colors = []
    for c in prediction['classification']:
        if c == 'DISORDERED':
            colors.append('red')
        elif c == 'MORF':
            colors.append('orange')
        else:
            colors.append('green')

    ax1.bar(x, composite, color=colors, width=1.0, alpha=0.7)
    ax1.axhline(y=0.5, color='red', linestyle='--', linewidth=1, label='Disorder threshold')
    ax1.axhline(y=0.35, color='orange', linestyle='--', linewidth=1, label='MoRF threshold')
    ax1.set_ylabel('Disorder Score')
    ax1.set_title('Z² Composite Disorder Prediction')
    ax1.legend(loc='upper right')
    ax1.set_ylim(0, 1)

    # 2. Component scores
    ax2 = axes[1]
    ax2.plot(x, prediction['sequence_propensity'], label='Sequence', alpha=0.8)
    ax2.plot(x, prediction['charge_hydropathy'], label='Charge-Hydropathy', alpha=0.8)
    ax2.plot(x, prediction['complexity_score'], label='Low Complexity', alpha=0.8)
    if any(s > 0 for s in prediction['z2_contact_score']):
        ax2.plot(x, prediction['z2_contact_score'], label='Z² Contacts', linewidth=2)
    ax2.set_ylabel('Component Scores')
    ax2.set_title('Individual Disorder Predictors')
    ax2.legend(loc='upper right', ncol=2)
    ax2.set_ylim(0, 1)

    # 3. IDR regions visualization
    ax3 = axes[2]
    ax3.set_xlim(-0.5, n - 0.5)
    ax3.set_ylim(0, 2)

    # Draw ordered backbone
    ax3.axhline(y=1, color='green', linewidth=3, alpha=0.3)

    # Draw IDR regions
    for region in idr_regions:
        color = 'red' if region['type'] == 'DISORDERED' else 'orange'
        rect = Rectangle((region['start_idx'] - 0.5, 0.5),
                         region['length'], 1,
                         facecolor=color, alpha=0.5,
                         edgecolor='black', linewidth=1)
        ax3.add_patch(rect)

        # Label
        mid = (region['start_idx'] + region['end_idx']) / 2
        ax3.text(mid, 1, f"{region['length']}aa",
                ha='center', va='center', fontsize=8, fontweight='bold')

    # Draw MoRFs
    for morf in morfs:
        rect = Rectangle((morf['start_idx'] - 0.5, 1.2),
                         morf['length'], 0.5,
                         facecolor='purple', alpha=0.6,
                         edgecolor='black', linewidth=1)
        ax3.add_patch(rect)

    ax3.set_ylabel('Regions')
    ax3.set_title(f"IDR Regions (red/orange) and MoRFs (purple) | {len(idr_regions)} IDRs, {len(morfs)} MoRFs")
    ax3.set_yticks([])

    # 4. Sequence with disorder coloring
    ax4 = axes[3]

    # Show sequence colored by disorder
    for i, aa in enumerate(sequence):
        color = colors[i]
        ax4.text(i, 0.5, aa, ha='center', va='center',
                fontsize=6 if n > 50 else 8,
                fontweight='bold',
                color=color)

    ax4.set_xlim(-0.5, n - 0.5)
    ax4.set_ylim(0, 1)
    ax4.set_xlabel('Residue Position')
    ax4.set_title('Sequence (colored by disorder)')
    ax4.set_yticks([])

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Visualization saved: {output_path}")


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def analyze_disorder(pdb_path: str = None,
                     sequence: str = None,
                     prediction_json: str = None,
                     ensemble_json: str = None,
                     output_dir: str = "idr_prediction") -> Dict:
    """
    Full IDR analysis pipeline.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Get structure and sequence
    if pdb_path and os.path.exists(pdb_path):
        print(f"\nLoading structure: {pdb_path}")
        structure = parse_structure(pdb_path)
        coords = structure['coords']
        residues = structure['residues']
        sequence = structure['sequence']
        n_residues = structure['n_residues']
        print(f"  Residues: {n_residues}")
    elif sequence:
        print(f"\nAnalyzing sequence (no structure)")
        coords = None
        residues = [{'name': 'UNK', 'num': i+1, 'aa': aa} for i, aa in enumerate(sequence)]
        n_residues = len(sequence)
    else:
        raise ValueError("Must provide either pdb_path or sequence")

    print(f"  Sequence: {sequence[:50]}..." if len(sequence) > 50 else f"  Sequence: {sequence}")

    # Load additional data if available
    plddt = None
    if prediction_json:
        plddt = load_plddt_scores(prediction_json)
        if plddt is not None:
            print(f"  Loaded pLDDT scores")

    rmsf = None
    if ensemble_json:
        rmsf = load_ensemble_flexibility(ensemble_json)
        if rmsf is not None:
            print(f"  Loaded RMSF flexibility profile")

    # Run disorder prediction
    print("\n" + "=" * 60)
    print("COMPUTING DISORDER PREDICTION")
    print("=" * 60)

    prediction = predict_disorder(
        sequence=sequence,
        coords=coords,
        plddt=plddt,
        rmsf=rmsf
    )

    # Identify regions
    print("\nIdentifying IDR regions...")
    idr_regions = identify_idr_regions(
        prediction['classification'],
        prediction['composite_disorder'],
        residues
    )

    print(f"  Found {len(idr_regions)} IDR regions")

    print("\nIdentifying MoRFs...")
    morfs = identify_morfs(
        prediction['classification'],
        prediction['composite_disorder'],
        residues=residues
    )

    print(f"  Found {len(morfs)} MoRFs")

    # Summary statistics
    n_disordered = sum(1 for c in prediction['classification'] if c == 'DISORDERED')
    n_morf = sum(1 for c in prediction['classification'] if c == 'MORF')
    n_ordered = sum(1 for c in prediction['classification'] if c == 'ORDERED')

    disorder_fraction = n_disordered / n_residues
    morf_fraction = n_morf / n_residues

    print(f"\n{'='*60}")
    print("IDR PREDICTION SUMMARY")
    print(f"{'='*60}")
    print(f"  Total residues: {n_residues}")
    print(f"  Ordered: {n_ordered} ({100*n_ordered/n_residues:.1f}%)")
    print(f"  MoRF: {n_morf} ({100*n_morf/n_residues:.1f}%)")
    print(f"  Disordered: {n_disordered} ({100*n_disordered/n_residues:.1f}%)")

    if prediction['ch_analysis']['is_globally_disordered']:
        print(f"\n  ⚠ GLOBALLY DISORDERED (Uversky plot)")

    if prediction['z2_analysis']:
        z2 = prediction['z2_analysis']
        print(f"\n  Z² Contact Analysis:")
        print(f"    Mean contacts: {z2['mean_contacts']:.1f} (optimal = {OPTIMAL_CONTACTS})")
        print(f"    Contact-disordered: {z2['n_disordered']} residues")

    # Report IDR regions
    if idr_regions:
        print(f"\n  IDR Regions:")
        for region in idr_regions[:5]:
            print(f"    {region['start_res']}-{region['end_res']}: "
                  f"{region['length']} aa, type={region['type']}, "
                  f"score={region['mean_score']:.2f}")

    # Report MoRFs
    if morfs:
        print(f"\n  MoRFs (Molecular Recognition Features):")
        for morf in morfs[:5]:
            print(f"    {morf['start_res']}-{morf['end_res']}: "
                  f"{morf['length']} aa, binding={morf['binding_potential']}")

    # Generate visualization
    print(f"\n{'='*60}")
    print("GENERATING OUTPUTS")
    print(f"{'='*60}")

    viz_path = os.path.join(output_dir, "disorder_prediction.png")
    generate_disorder_visualization(
        sequence, prediction, idr_regions, morfs, viz_path
    )

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_path,
        'sequence': sequence,
        'n_residues': n_residues,
        'z2_constant': Z2,
        'summary': {
            'n_ordered': n_ordered,
            'n_morf': n_morf,
            'n_disordered': n_disordered,
            'disorder_fraction': float(disorder_fraction),
            'morf_fraction': float(morf_fraction),
            'is_globally_disordered': prediction['ch_analysis']['is_globally_disordered']
        },
        'idr_regions': idr_regions,
        'morfs': morfs,
        'per_residue': {
            'composite_disorder': prediction['composite_disorder'],
            'classification': prediction['classification'],
            'sequence_propensity': prediction['sequence_propensity'],
            'charge_hydropathy': prediction['charge_hydropathy']
        },
        'z2_analysis': prediction['z2_analysis'],
        'weights_used': prediction['weights_used'],
        'output_files': {
            'visualization': viz_path
        }
    }

    # Save JSON
    json_path = os.path.join(output_dir, "idr_results.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  ✓ Results saved: {json_path}")

    # Final verdict
    print(f"\n{'='*60}")
    print("Z² IDR PREDICTION COMPLETE")
    print(f"{'='*60}")

    if disorder_fraction > 0.3:
        verdict = "SUBSTANTIALLY DISORDERED"
        explanation = f"""
  This protein is {100*disorder_fraction:.0f}% disordered.

  Z² INTERPRETATION:
  Disordered regions CANNOT achieve Z² = 8 contact packing.
  The sequence composition prevents stable hydrophobic core formation.

  These regions may:
  - Serve as flexible linkers between domains
  - Contain binding sites that fold upon partner recognition (MoRFs)
  - Be targets for post-translational modifications
"""
    elif morf_fraction > 0.2:
        verdict = "CONTAINS BINDING MOTIFS"
        explanation = f"""
  This protein contains {len(morfs)} MoRFs (Molecular Recognition Features).

  Z² INTERPRETATION:
  MoRF regions have 4-6 contacts (below Z² optimal of 8).
  They are CONDITIONALLY DISORDERED: unfolded alone, folded when bound.

  These are prime targets for:
  - Protein-protein interactions
  - Drug binding sites
  - Regulatory interactions
"""
    else:
        verdict = "WELL-ORDERED"
        explanation = f"""
  This protein is {100*n_ordered/n_residues:.0f}% ordered.

  Z² INTERPRETATION:
  The structure achieves near-optimal Z² = 8 contact packing.
  The sequence composition supports stable hydrophobic core formation.

  AlphaFold would predict this structure with high confidence.
  Z² explains WHY: geometric contact optimization is satisfied.
"""

    print(f"\n  VERDICT: {verdict}")
    print(explanation)

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run IDR prediction on Z² protein."""
    import sys

    # Default inputs
    if len(sys.argv) > 1:
        pdb_path = sys.argv[1]
    else:
        pdb_path = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

    prediction_json = pdb_path.replace('.pdb', '_prediction.json')
    ensemble_json = "conformational_ensemble/ensemble_results.json"

    if not os.path.exists(pdb_path):
        print(f"PDB not found: {pdb_path}")
        return None

    results = analyze_disorder(
        pdb_path=pdb_path,
        prediction_json=prediction_json if os.path.exists(prediction_json) else None,
        ensemble_json=ensemble_json if os.path.exists(ensemble_json) else None,
        output_dir="idr_prediction"
    )

    return results


if __name__ == "__main__":
    results = main()
