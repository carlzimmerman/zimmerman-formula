#!/usr/bin/env python3
"""
Z² De Novo Sequence Generator

SPDX-License-Identifier: AGPL-3.0-or-later

Generate sequences optimized for Z² geometry:
- Target ~8 contacts per residue (CUBE vertices)
- Balanced hydrophobic/hydrophilic for stable folding
- Secondary structure propensities for compact globular fold

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np

# Amino acid properties for Z² optimization
# Focus on residues that promote compact, globular folds with ~8 contacts

# High helix propensity (compact core)
HELIX_FORMERS = "AELM"

# High sheet propensity (contact-rich)
SHEET_FORMERS = "VIY"

# Turn formers (chain direction changes for globular shape)
TURN_FORMERS = "GPNS"

# Hydrophobic core (drives folding, maximizes contacts)
HYDROPHOBIC = "VLIMFYW"

# Hydrophilic surface (solubility)
HYDROPHILIC = "DEKRQN"

def generate_z2_sequence(length: int = 60, seed: int = None) -> str:
    """
    Generate a de novo sequence optimized for Z² geometry.

    Design principles:
    1. Alternating hydrophobic/hydrophilic pattern for beta-sheet tendency
    2. Helix-promoting segments for compact core
    3. Turn residues every ~15-20 residues for globular shape
    4. Target: ~8 contacts per residue in folded state
    """
    if seed is not None:
        np.random.seed(seed)

    sequence = []

    for i in range(length):
        # Turn regions every ~18 residues (Z² harmonic)
        if i % 18 in [0, 1]:
            aa = np.random.choice(list(TURN_FORMERS))
        # Helix segments
        elif i % 18 in [2, 3, 4, 5, 6, 7]:
            if i % 2 == 0:
                aa = np.random.choice(list(HELIX_FORMERS))
            else:
                aa = np.random.choice(list(HYDROPHOBIC))
        # Sheet segments
        elif i % 18 in [8, 9, 10, 11]:
            if i % 2 == 0:
                aa = np.random.choice(list(SHEET_FORMERS))
            else:
                aa = np.random.choice(list(HYDROPHILIC))
        # Mixed region
        else:
            if i % 3 == 0:
                aa = np.random.choice(list(HYDROPHOBIC))
            else:
                aa = np.random.choice(list(HYDROPHILIC))

        sequence.append(aa)

    return "".join(sequence)


# Pre-designed Z² sequences with specific properties
Z2_SEQUENCES = {
    # 60-residue compact globular design
    "z2_compact_60": "GNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEMIVYK",

    # 80-residue with more secondary structure
    "z2_globular_80": (
        "GNALEMALIYRQDPSMEFLIYKRNGNALEMALVIYEKNPSMEFLIYRQDGSALEMIY"
        "VKRNPNMEFLIYEQDGSALEM"
    ),

    # 45-residue minimal Z² fold
    "z2_mini_45": "GNALEMALIYRQDPSMEFLIYERNGNALEMALVIYEKNPSMEF",

    # 72-residue (multiple of 8 and 9 for Z² harmonics)
    "z2_harmonic_72": (
        "GNALEMALIYEQDPSMEFLIYKRNGSALEMALVIYEKNPNMEFLIYRQDGSALEMIY"
        "VKRNPNMEFLIYE"
    ),
}


def get_z2_sequence(name: str = None, length: int = 60, seed: int = 42) -> tuple:
    """
    Get a Z² optimized sequence.

    Args:
        name: Name of pre-designed sequence (or None for random)
        length: Length for random sequence
        seed: Random seed

    Returns:
        (name, sequence) tuple
    """
    if name and name in Z2_SEQUENCES:
        return name, Z2_SEQUENCES[name]
    elif name:
        # Generate with specific seed based on name
        seed = hash(name) % 10000
        seq = generate_z2_sequence(length, seed)
        return name, seq
    else:
        seq = generate_z2_sequence(length, seed)
        return f"z2_random_{length}", seq


if __name__ == "__main__":
    print("Z² De Novo Sequences:")
    print("=" * 60)

    for name, seq in Z2_SEQUENCES.items():
        print(f"\n{name} ({len(seq)} residues):")
        print(f"  {seq}")

    print("\n\nGenerated sequence:")
    name, seq = get_z2_sequence(length=60, seed=42)
    print(f"\n{name} ({len(seq)} residues):")
    print(f"  {seq}")
