#!/usr/bin/env python3
"""
Z² Supercharger - Aggregation Prevention via Surface Charge Engineering

SPDX-License-Identifier: AGPL-3.0-or-later

PROBLEM:
Our Z² protein has 6 Aggregation Prone Regions (APRs) because its perfect
packing makes the surface too hydrophobic. Proteins aggregate when
hydrophobic surfaces stick together.

SOLUTION:
Supercharge the surface with charged residues (Glu/Arg) to create
electrostatic repulsion WITHOUT disrupting the Z² = 8 contact core.

STRATEGY:
1. Calculate Relative Solvent Accessibility (RSA) for each residue
2. Identify Aggregation Prone Regions (APRs) - hydrophobic stretches
3. If RSA > 50% AND in APR → mutate to charged residue (E or R)
4. NEVER mutate RSA < 20% (core Z² load-bearing residues)
5. Balance positive/negative charges for optimal stability

THE PHYSICS:
- Like charges repel: prevents protein-protein aggregation
- Core Z² geometry preserved: maintains therapeutic function
- Surface modification only: doesn't disrupt 8-contact packing

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
OPTIMAL_CONTACTS = 8
CONTACT_CUTOFF = 8.0  # Å

# RSA thresholds
RSA_EXPOSED_THRESHOLD = 0.50  # >50% = highly exposed, safe to mutate
RSA_CORE_THRESHOLD = 0.20     # <20% = core residue, NEVER mutate

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Maximum accessible surface area per residue (Tien et al., 2013)
MAX_ASA = {
    'A': 129, 'R': 274, 'N': 195, 'D': 193, 'C': 167,
    'E': 223, 'Q': 225, 'G': 104, 'H': 224, 'I': 197,
    'L': 201, 'K': 236, 'M': 224, 'F': 240, 'P': 159,
    'S': 155, 'T': 172, 'W': 285, 'Y': 263, 'V': 174
}

# Aggregation propensity (Tango-like scale)
AGGREGATION_PROPENSITY = {
    'I': 1.8, 'V': 1.6, 'L': 1.4, 'F': 1.5, 'Y': 1.3,
    'M': 1.1, 'W': 1.2, 'A': 0.9, 'C': 1.0, 'G': 0.7,
    'T': 0.6, 'S': 0.5, 'N': 0.4, 'Q': 0.4, 'H': 0.5,
    'K': 0.2, 'R': 0.2, 'D': 0.1, 'E': 0.1, 'P': 0.3
}

# Hydrophobicity (Kyte-Doolittle)
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'N': -3.5,
    'D': -3.5, 'Q': -3.5, 'E': -3.5, 'K': -3.9, 'R': -4.5
}

# pKa values for pI calculation
PKA_CTERM = 3.65
PKA_NTERM = 8.0
PKA = {
    'D': 3.9, 'E': 4.1, 'C': 8.3, 'Y': 10.1,
    'H': 6.0, 'K': 10.5, 'R': 12.5
}


def parse_pdb(pdb_file: str) -> Tuple[np.ndarray, List[str], str]:
    """Parse PDB file to extract coordinates and sequence."""
    coords = []
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
                    residue_names.append(aa)

    sequence = ''.join(residue_names)
    return np.array(coords), residue_names, sequence


def calculate_contacts(coords: np.ndarray, cutoff: float = CONTACT_CUTOFF) -> np.ndarray:
    """Calculate contacts per residue."""
    n = len(coords)
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    distances = np.sqrt(np.sum(diff**2, axis=-1))

    contacts = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and distances[i, j] < cutoff:
                contacts[i] += 1

    return contacts


def calculate_rsa(coords: np.ndarray, contacts: np.ndarray,
                  residue_names: List[str]) -> np.ndarray:
    """
    Calculate Relative Solvent Accessibility (RSA) using contact-based estimation.

    RSA approximation: fewer contacts = more exposed = higher RSA
    Calibrated against typical buried/exposed ranges.
    """
    n = len(coords)

    # Maximum expected contacts for fully buried residue
    MAX_CONTACTS = 12

    # Calculate burial score (inverse of exposure)
    burial = contacts / MAX_CONTACTS
    burial = np.clip(burial, 0, 1)

    # RSA is inverse of burial
    rsa = 1 - burial

    # Adjust by distance from center of mass (surface residues further out)
    com = np.mean(coords, axis=0)
    dist_from_com = np.linalg.norm(coords - com, axis=1)
    max_dist = np.max(dist_from_com)
    radial_factor = dist_from_com / max_dist if max_dist > 0 else np.ones(n)

    # Combined RSA: weighted average of contact-based and radial
    rsa_combined = 0.7 * rsa + 0.3 * radial_factor

    return rsa_combined


def identify_aprs(sequence: str, window: int = 7,
                  threshold: float = 1.0) -> List[Dict]:
    """
    Identify Aggregation Prone Regions (APRs).

    APRs are stretches of hydrophobic residues that drive aggregation.
    """
    aprs = []
    scores = [AGGREGATION_PROPENSITY.get(aa, 0.5) for aa in sequence]

    for i in range(len(sequence) - window + 1):
        window_score = np.mean(scores[i:i+window])

        if window_score > threshold:
            aprs.append({
                'start': i,
                'end': i + window,
                'sequence': sequence[i:i+window],
                'score': float(window_score)
            })

    # Merge overlapping APRs
    merged = []
    for apr in sorted(aprs, key=lambda x: x['start']):
        if merged and apr['start'] <= merged[-1]['end']:
            merged[-1]['end'] = max(merged[-1]['end'], apr['end'])
            merged[-1]['score'] = max(merged[-1]['score'], apr['score'])
            merged[-1]['sequence'] = sequence[merged[-1]['start']:merged[-1]['end']]
        else:
            merged.append(apr)

    return merged


def calculate_pi(sequence: str) -> float:
    """Calculate theoretical isoelectric point (pI)."""
    def charge_at_ph(ph: float) -> float:
        charge = 0

        # N-terminus (positive at low pH)
        charge += 1 / (1 + 10**(ph - PKA_NTERM))

        # C-terminus (negative at high pH)
        charge -= 1 / (1 + 10**(PKA_CTERM - ph))

        # Side chains
        for aa in sequence:
            if aa in ['D', 'E']:  # Acidic
                charge -= 1 / (1 + 10**(PKA[aa] - ph))
            elif aa in ['K', 'R']:  # Basic
                charge += 1 / (1 + 10**(ph - PKA[aa]))
            elif aa == 'H':
                charge += 1 / (1 + 10**(ph - PKA['H']))
            elif aa == 'C':
                charge -= 1 / (1 + 10**(PKA['C'] - ph))
            elif aa == 'Y':
                charge -= 1 / (1 + 10**(PKA['Y'] - ph))

        return charge

    # Binary search for pI (pH where charge = 0)
    low, high = 0.0, 14.0

    while high - low > 0.01:
        mid = (low + high) / 2
        if charge_at_ph(mid) > 0:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def calculate_net_charge(sequence: str, ph: float = 7.4) -> float:
    """Calculate net charge at physiological pH."""
    charge = 0

    # N-terminus
    charge += 1 / (1 + 10**(ph - PKA_NTERM))

    # C-terminus
    charge -= 1 / (1 + 10**(PKA_CTERM - ph))

    for aa in sequence:
        if aa in ['D', 'E']:
            charge -= 1 / (1 + 10**(PKA[aa] - ph))
        elif aa in ['K', 'R']:
            charge += 1 / (1 + 10**(ph - PKA[aa]))
        elif aa == 'H':
            charge += 1 / (1 + 10**(ph - PKA['H']))

    return charge


def supercharge_sequence(sequence: str, coords: np.ndarray,
                         contacts: np.ndarray, rsa: np.ndarray,
                         aprs: List[Dict]) -> Tuple[str, List[Dict]]:
    """
    Supercharge the sequence by mutating exposed APR residues to charged residues.

    Rules:
    1. Only mutate if RSA > 50% (exposed)
    2. Never mutate if RSA < 20% (core Z² residues)
    3. Only target residues in APRs
    4. Alternate E/R to balance charge
    5. Preserve prolines (structure breakers)
    """
    sequence_list = list(sequence)
    mutations = []

    # Get all APR residue indices
    apr_residues = set()
    for apr in aprs:
        for i in range(apr['start'], apr['end']):
            apr_residues.add(i)

    # Track charge balance
    n_negative = 0
    n_positive = 0

    for i in range(len(sequence)):
        original = sequence[i]

        # Skip if not in APR
        if i not in apr_residues:
            continue

        # Skip core residues (RSA < 20%)
        if rsa[i] < RSA_CORE_THRESHOLD:
            continue

        # Skip if not exposed (RSA < 50%)
        if rsa[i] < RSA_EXPOSED_THRESHOLD:
            continue

        # Skip prolines (structural importance)
        if original == 'P':
            continue

        # Skip already charged residues
        if original in ['E', 'D', 'K', 'R']:
            continue

        # Skip glycines (flexibility important)
        if original == 'G':
            continue

        # Choose mutation: alternate to balance charge
        if n_negative <= n_positive:
            new_aa = 'E'  # Glutamate (negative)
            n_negative += 1
        else:
            new_aa = 'R'  # Arginine (positive)
            n_positive += 1

        sequence_list[i] = new_aa
        mutations.append({
            'position': i + 1,  # 1-indexed
            'original': original,
            'mutated': new_aa,
            'rsa': float(rsa[i]),
            'contacts': int(contacts[i]),
            'in_apr': True
        })

    return ''.join(sequence_list), mutations


def analyze_aggregation_improvement(original_seq: str,
                                    mutated_seq: str) -> Dict:
    """Analyze improvement in aggregation propensity."""
    def calc_agg_score(seq):
        return np.mean([AGGREGATION_PROPENSITY.get(aa, 0.5) for aa in seq])

    original_score = calc_agg_score(original_seq)
    mutated_score = calc_agg_score(mutated_seq)

    # Count APRs
    original_aprs = identify_aprs(original_seq)
    mutated_aprs = identify_aprs(mutated_seq)

    return {
        'original_aggregation_score': float(original_score),
        'mutated_aggregation_score': float(mutated_score),
        'improvement_percent': float((original_score - mutated_score) / original_score * 100),
        'original_apr_count': len(original_aprs),
        'mutated_apr_count': len(mutated_aprs),
        'aprs_eliminated': len(original_aprs) - len(mutated_aprs)
    }


def create_visualization(sequence: str, mutated_sequence: str,
                         rsa: np.ndarray, contacts: np.ndarray,
                         aprs: List[Dict], mutations: List[Dict],
                         output_dir: str):
    """Create visualization of supercharging results."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    n = len(sequence)
    residue_idx = np.arange(n)

    # 1. RSA profile with thresholds
    ax1 = axes[0, 0]
    colors = []
    for i in range(n):
        if rsa[i] < RSA_CORE_THRESHOLD:
            colors.append('green')  # Core - protected
        elif rsa[i] > RSA_EXPOSED_THRESHOLD:
            colors.append('red')  # Exposed - mutable
        else:
            colors.append('yellow')  # Intermediate

    ax1.bar(residue_idx, rsa, color=colors, width=1.0, alpha=0.7)
    ax1.axhline(y=RSA_CORE_THRESHOLD, color='green', linestyle='--',
                linewidth=2, label=f'Core (<{RSA_CORE_THRESHOLD*100:.0f}%)')
    ax1.axhline(y=RSA_EXPOSED_THRESHOLD, color='red', linestyle='--',
                linewidth=2, label=f'Exposed (>{RSA_EXPOSED_THRESHOLD*100:.0f}%)')
    ax1.set_xlabel('Residue')
    ax1.set_ylabel('RSA')
    ax1.set_title('Relative Solvent Accessibility')
    ax1.legend()

    # 2. Contacts with Z² optimum
    ax2 = axes[0, 1]
    ax2.bar(residue_idx, contacts, color='steelblue', width=1.0, alpha=0.7)
    ax2.axhline(y=OPTIMAL_CONTACTS, color='green', linestyle='--',
                linewidth=2, label=f'Z² optimal = {OPTIMAL_CONTACTS}')
    ax2.set_xlabel('Residue')
    ax2.set_ylabel('Contacts')
    ax2.set_title('Contact Profile (Z² Core)')
    ax2.legend()

    # 3. Mutation map
    ax3 = axes[1, 0]
    mutation_positions = [m['position'] - 1 for m in mutations]
    mutation_types = [1 if m['mutated'] == 'E' else -1 for m in mutations]

    # Background: APR regions
    for apr in aprs:
        ax3.axvspan(apr['start'], apr['end'], alpha=0.3, color='orange',
                   label='APR' if apr == aprs[0] else '')

    # Mutations
    colors_mut = ['red' if t == 1 else 'blue' for t in mutation_types]
    ax3.scatter(mutation_positions, mutation_types, c=colors_mut, s=100, zorder=5)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax3.set_yticks([-1, 0, 1])
    ax3.set_yticklabels(['R (+)', '', 'E (-)'])
    ax3.set_xlabel('Residue')
    ax3.set_ylabel('Mutation Type')
    ax3.set_title(f'Supercharging Mutations (n={len(mutations)})')
    ax3.legend()

    # 4. Summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    original_pi = calculate_pi(sequence)
    mutated_pi = calculate_pi(mutated_sequence)
    original_charge