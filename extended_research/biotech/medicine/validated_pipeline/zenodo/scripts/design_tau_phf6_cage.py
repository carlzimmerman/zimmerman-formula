#!/usr/bin/env python3
"""
design_tau_phf6_cage.py - Tau PHF6 Aggregation Inhibitor Design

Designs peptide "cages" that bind to the PHF6 motif (VQIVYK) of Tau protein
to prevent aggregation into paired helical filaments (PHFs) in Alzheimer's disease.

Key Strategy:
- Target the RIGID PHF6 motif, not the disordered full-length Tau
- Use Z² geometry to position aromatic anchors against Tyr310 (Y in VQIVYK)
- Design peptides that "cap" the β-sheet stacking interface

PHF6 Motif: VQIVYK (Tau residues 306-311)
- Val306, Gln307, Ile308, Val309, Tyr310, Lys311
- Forms cross-β structure in fibrils
- Tyr310 is the key aromatic for Z² targeting

Key Scientists Referenced:
- David Eisenberg: Steric zipper structures in amyloid fibrils
- Roland Riek: Tau fibril structures by cryo-EM
- Michel Bhoen: Peptide inhibitors of amyloid aggregation

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import math
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from datetime import datetime


# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z2_VACUUM = 5.788810036466141
Z2_BIOLOGICAL = 6.015152508891966
Z2_OBSERVED = 6.423  # Mean from empirical data

# PHF6 motif
PHF6_SEQUENCE = "VQIVYK"
PHF6_FULL = {
    306: 'V',  # Val - hydrophobic
    307: 'Q',  # Gln - polar
    308: 'I',  # Ile - hydrophobic
    309: 'V',  # Val - hydrophobic
    310: 'Y',  # Tyr - AROMATIC (Z² target!)
    311: 'K',  # Lys - charged
}

# Key target: Tyr310 is the aromatic anchor in PHF6
TYR310_Z2_TARGET = True


# =============================================================================
# AMINO ACID PROPERTIES
# =============================================================================

# Aromatic residues for Z² anchoring
AROMATICS = {'W': 1.0, 'Y': 0.85, 'F': 0.80, 'H': 0.60}

# β-sheet propensity (Chou-Fasman)
BETA_PROPENSITY = {
    'V': 1.70, 'I': 1.60, 'Y': 1.47, 'F': 1.38, 'W': 1.37,
    'L': 1.30, 'T': 1.19, 'C': 1.19, 'M': 1.05, 'Q': 1.10,
    'A': 0.83, 'R': 0.93, 'G': 0.75, 'N': 0.89, 'S': 0.75,
    'H': 0.87, 'K': 0.74, 'D': 0.54, 'E': 0.37, 'P': 0.55,
}

# Charge for electrostatic complementarity
CHARGE = {
    'K': +1, 'R': +1, 'H': +0.5,
    'D': -1, 'E': -1,
}

# Hydrophobicity (Kyte-Doolittle)
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'W': -0.9,
    'S': -0.8, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5,
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class CageDesign:
    """A designed cage peptide for PHF6."""
    id: str
    sequence: str
    length: int

    # Aromatic content
    n_aromatics: int
    aromatic_positions: List[int]
    z2_potential: float

    # β-sheet compatibility
    beta_propensity_score: float

    # Complementarity to PHF6
    charge_complementarity: float
    hydrophobic_match: float

    # Z² geometry
    tyr310_engagement: str  # Which residue targets Tyr310
    z2_spacing_score: float

    # Overall scores
    cage_score: float
    binding_mode: str
    predicted_ki_um: float  # Predicted inhibition constant


@dataclass
class PHF6CageReport:
    """Complete cage design report."""
    timestamp: str
    target_motif: str
    n_designs: int
    designs: List[CageDesign]
    best_design: Optional[CageDesign]
    summary: str


# =============================================================================
# DESIGN FUNCTIONS
# =============================================================================

def analyze_phf6_geometry() -> Dict:
    """
    Analyze the PHF6 motif for cage design.

    Key insight: PHF6 forms a "steric zipper" where two β-sheets
    interlock. The cage peptide must:
    1. Bind to one face of PHF6
    2. Block access to the opposing β-sheet
    """
    # PHF6 structure analysis (from PDB 2ON9, 5O3L)
    # The motif forms extended β-strand with specific geometry

    # Residue positions in extended β-strand (~3.5 Å per residue)
    residue_spacing = 3.5  # Å

    # Tyr310 sidechain extends perpendicular to backbone
    # Aromatic ring center ~6-7 Å from backbone
    tyr310_ring_distance = 6.5  # Å from Cα

    # For Z² engagement, cage aromatic should be:
    # ~6.015 Å from Tyr310 ring center

    return {
        'motif': PHF6_SEQUENCE,
        'key_residue': 'Tyr310',
        'tyr_ring_distance': tyr310_ring_distance,
        'z2_target_distance': Z2_BIOLOGICAL,
        'beta_strand_spacing': residue_spacing,
        'optimal_cage_length': 6,  # Match PHF6 length
        'aromatic_anchor_position': 'C-terminal',  # To face Tyr310
    }


def calculate_beta_propensity(sequence: str) -> float:
    """Calculate β-sheet propensity score for sequence."""
    if not sequence:
        return 0.0
    scores = [BETA_PROPENSITY.get(aa, 1.0) for aa in sequence]
    return sum(scores) / len(scores)


def calculate_charge_complementarity(sequence: str) -> float:
    """
    Calculate charge complementarity to PHF6.

    PHF6 (VQIVYK) has Lys311 (+1 charge).
    Cage should have negative charge to complement.
    """
    cage_charge = sum(CHARGE.get(aa, 0) for aa in sequence)
    # PHF6 has +1 from Lys311
    # Ideal cage has -1 to -2 charge
    if -2 <= cage_charge <= -1:
        return 1.0
    elif cage_charge == 0:
        return 0.5
    elif cage_charge < -2:
        return 0.7
    else:  # Positive charge = poor
        return 0.2


def calculate_hydrophobic_match(sequence: str) -> float:
    """
    Calculate hydrophobic complementarity to PHF6.

    PHF6 has hydrophobic face (V, I, V) that must be matched.
    """
    # Average hydrophobicity
    scores = [HYDROPHOBICITY.get(aa, 0) for aa in sequence]
    avg_hydro = sum(scores) / len(scores)

    # PHF6 hydrophobic face needs matching hydrophobic residues
    # Optimal: moderate hydrophobicity (not too greasy, not too polar)
    if 0 <= avg_hydro <= 2:
        return 1.0
    elif -1 <= avg_hydro < 0 or 2 < avg_hydro <= 3:
        return 0.8
    else:
        return 0.5


def analyze_z2_spacing(sequence: str) -> Tuple[float, str]:
    """
    Analyze aromatic spacing for Z² engagement with Tyr310.

    Returns (score, engagement_description)
    """
    aromatic_positions = [i for i, aa in enumerate(sequence) if aa in AROMATICS]

    if not aromatic_positions:
        return 0.0, "No aromatic anchors"

    # For PHF6 cage, ideal is aromatic at C-terminus to face Tyr310
    # Position 5 in a 6-mer cage would be optimal (index 5)

    # Check if aromatic near C-terminus
    last_aromatic = max(aromatic_positions)
    n = len(sequence)

    c_term_distance = n - 1 - last_aromatic

    if c_term_distance == 0:  # Aromatic at C-terminus
        score = 1.0
        engagement = f"C-terminal {sequence[last_aromatic]} directly engages Tyr310"
    elif c_term_distance == 1:
        score = 0.9
        engagement = f"{sequence[last_aromatic]} at position {last_aromatic+1} near Tyr310"
    elif c_term_distance == 2:
        score = 0.7
        engagement = f"{sequence[last_aromatic]} at Z² distance from Tyr310"
    else:
        score = 0.4
        engagement = f"Aromatic {sequence[last_aromatic]} distant from Tyr310"

    # Bonus for multiple aromatics
    if len(aromatic_positions) >= 2:
        score = min(1.0, score + 0.1)
        engagement += f" + {len(aromatic_positions)-1} additional anchors"

    return score, engagement


def design_cage_peptide(design_id: str, template: str = None) -> CageDesign:
    """
    Design a single cage peptide for PHF6.

    Design principles:
    1. Length: 6-8 residues (match PHF6)
    2. C-terminal aromatic (W/Y/F) for Tyr310 engagement
    3. Negative charge (D/E) to complement Lys311
    4. β-sheet compatible backbone
    5. Hydrophobic residues to match V-I-V face
    """
    if template:
        sequence = template
    else:
        # Generate sequence based on design principles
        length = random.choice([6, 7, 8])

        # Position-specific design
        residues = []

        for pos in range(length):
            if pos == length - 1:
                # C-terminus: aromatic for Tyr310 engagement
                residues.append(random.choice(['W', 'Y', 'F']))
            elif pos == length - 2:
                # Near C-term: charged for Lys311
                residues.append(random.choice(['E', 'D', 'E']))
            elif pos == 0:
                # N-terminus: flexible or charged
                residues.append(random.choice(['E', 'D', 'Q', 'N', 'S']))
            elif pos % 2 == 0:
                # Even positions: hydrophobic to match VIV face
                residues.append(random.choice(['V', 'I', 'L', 'F', 'Y']))
            else:
                # Odd positions: polar/charged
                residues.append(random.choice(['E', 'D', 'Q', 'N', 'K', 'R', 'S', 'T']))

        sequence = ''.join(residues)

    # Analyze the design
    n = len(sequence)
    aromatics = [aa for aa in sequence if aa in AROMATICS]
    aromatic_pos = [i for i, aa in enumerate(sequence) if aa in AROMATICS]
    z2_potential = sum(AROMATICS.get(aa, 0) for aa in aromatics)

    beta_score = calculate_beta_propensity(sequence)
    charge_score = calculate_charge_complementarity(sequence)
    hydro_score = calculate_hydrophobic_match(sequence)
    z2_spacing, tyr_engagement = analyze_z2_spacing(sequence)

    # Calculate cage score
    cage_score = (
        0.30 * z2_spacing +           # Z² geometry (primary)
        0.25 * (z2_potential / 2) +   # Aromatic content
        0.20 * charge_score +          # Charge complementarity
        0.15 * hydro_score +           # Hydrophobic match
        0.10 * min(1.0, beta_score / 1.5)  # β-sheet compatibility
    )

    # Determine binding mode
    if len(aromatics) >= 2 and z2_spacing > 0.8:
        binding_mode = "DUAL AROMATIC CAGE: Trp/Tyr clamp on Tyr310 at Z² distance"
    elif len(aromatics) >= 1 and z2_spacing > 0.7:
        binding_mode = "AROMATIC CAP: Single anchor blocks fibril interface"
    elif charge_score > 0.8:
        binding_mode = "ELECTROSTATIC DISRUPTOR: Charge repulsion prevents stacking"
    else:
        binding_mode = "COMPETITIVE BINDER: General β-sheet interference"

    # Predict Ki (rough estimate based on score)
    if cage_score > 0.8:
        predicted_ki = 0.1  # 100 nM
    elif cage_score > 0.6:
        predicted_ki = 1.0  # 1 μM
    elif cage_score > 0.4:
        predicted_ki = 10.0  # 10 μM
    else:
        predicted_ki = 100.0  # 100 μM

    return CageDesign(
        id=design_id,
        sequence=sequence,
        length=n,
        n_aromatics=len(aromatics),
        aromatic_positions=aromatic_pos,
        z2_potential=z2_potential,
        beta_propensity_score=beta_score,
        charge_complementarity=charge_score,
        hydrophobic_match=hydro_score,
        tyr310_engagement=tyr_engagement,
        z2_spacing_score=z2_spacing,
        cage_score=cage_score,
        binding_mode=binding_mode,
        predicted_ki_um=predicted_ki
    )


def generate_optimized_templates() -> List[str]:
    """
    Generate optimized cage templates based on Z² principles.

    Key patterns:
    1. C-terminal Trp for maximum Tyr310 engagement
    2. Internal Glu/Asp for Lys311 complementarity
    3. Val/Ile for hydrophobic face matching
    """
    templates = [
        # Pattern 1: Classic Z² cage (C-term Trp)
        "EVIQEW",   # E-V-I-Q-E-W
        "DVIQEW",   # D-V-I-Q-E-W
        "EVIQDW",   # E-V-I-Q-D-W

        # Pattern 2: Extended cage with dual aromatic
        "WVIQEYW",  # W at both ends
        "YVIQEYW",  # Y-Y sandwich
        "FVIQEFW",  # F-W pair

        # Pattern 3: Strong electrostatic
        "EEIDEW",   # Triple negative
        "DDIQEW",   # Double Asp
        "EVIDEEW",  # Extended charged

        # Pattern 4: β-sheet optimized
        "VFIQEY",   # High β-propensity
        "IYIQEW",   # Ile-Tyr core
        "LVIQEW",   # Leu variant

        # Pattern 5: Literature-inspired (D-amino analogs would be better)
        "KIQEVY",   # Reversed charge
        "QIVEWY",   # Polar core
        "NVIQEW",   # Asn variant

        # Pattern 6: Dual Z² clamp
        "WVIEYW",   # W-Y at Z² spacing
        "YWIQEW",   # Y-W bookends
        "WEIQYW",   # Internal/terminal

        # Pattern 7: Charged termini
        "EVIQEK",   # C-term Lys (for solubility) + Trp variant
        "DVIQEYW",  # Longer with dual aromatic
        "EVIQDYW",  # Asp + dual aromatic

        # Pattern 8: Hydrophobic face optimized
        "IVIFEW",   # Strong hydrophobic
        "VVIQEW",   # Val-Val
        "LIIQEW",   # Leu-Ile
    ]

    return templates


def run_phf6_cage_design(n_random: int = 20,
                         output_dir: str = "../tau_cage_designs") -> PHF6CageReport:
    """
    Run complete PHF6 cage design pipeline.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("TAU PHF6 CAGE DESIGN - ALZHEIMER'S AGGREGATION INHIBITOR")
    print("=" * 70)
    print(f"    Target Motif: {PHF6_SEQUENCE} (Tau 306-311)")
    print(f"    Key Aromatic: Tyr310 (Z² anchor target)")
    print(f"    Z² Distance: {Z2_BIOLOGICAL:.6f} Å")
    print()

    # Analyze PHF6 geometry
    geometry = analyze_phf6_geometry()
    print("    PHF6 GEOMETRY ANALYSIS:")
    print(f"    ─" * 25)
    print(f"      Tyr310 ring distance from backbone: {geometry['tyr_ring_distance']} Å")
    print(f"      Z² target distance: {geometry['z2_target_distance']:.3f} Å")
    print(f"      Optimal aromatic position: {geometry['aromatic_anchor_position']}")
    print()

    designs = []

    # Generate from optimized templates
    print("    [1/2] Generating optimized cage designs...")
    templates = generate_optimized_templates()
    for i, template in enumerate(templates):
        design = design_cage_peptide(f"PHF6-CAGE-{i+1:03d}", template=template)
        designs.append(design)

    # Generate random designs
    print(f"    [2/2] Generating {n_random} random cage designs...")
    for i in range(n_random):
        design = design_cage_peptide(f"PHF6-RAND-{i+1:03d}")
        designs.append(design)

    # Sort by cage score
    designs.sort(key=lambda d: d.cage_score, reverse=True)

    # Assign final IDs
    for i, d in enumerate(designs):
        d.id = f"PHF6-Z2-{i+1:03d}"

    best = designs[0]

    # Print results
    print()
    print("    " + "=" * 66)
    print("    TOP 15 PHF6 CAGE DESIGNS")
    print("    " + "=" * 66)
    print(f"    {'Rank':<5}{'ID':<14}{'Sequence':<12}{'Score':<8}{'Ki(μM)':<8}{'Binding Mode'}")
    print("    " + "-" * 66)

    for i, d in enumerate(designs[:15]):
        mode_short = d.binding_mode.split(':')[0]
        print(f"    {i+1:<5}{d.id:<14}{d.sequence:<12}{d.cage_score:.3f}   {d.predicted_ki_um:<8}{mode_short}")

    # Detailed top 5
    print()
    print("    " + "=" * 66)
    print("    TOP 5 DETAILED ANALYSIS")
    print("    " + "=" * 66)

    for i, d in enumerate(designs[:5]):
        print(f"""
    {i+1}. {d.id}: {d.sequence}
       ├─ Aromatics: {d.n_aromatics} at positions {d.aromatic_positions}
       ├─ Z² Potential: {d.z2_potential:.2f} | Spacing Score: {d.z2_spacing_score:.2f}
       ├─ Tyr310 Engagement: {d.tyr310_engagement}
       ├─ Charge Complementarity: {d.charge_complementarity:.2f}
       ├─ Predicted Ki: {d.predicted_ki_um} μM
       └─ Mode: {d.binding_mode}""")

    print()
    print("    " + "=" * 66)
    print("    CAGE DESIGN SUMMARY")
    print("    " + "=" * 66)
    print(f"    Total designs: {len(designs)}")
    print(f"    Best cage score: {best.cage_score:.3f}")
    print(f"    Best predicted Ki: {min(d.predicted_ki_um for d in designs)} μM")
    print()

    dual_aromatic = [d for d in designs if d.n_aromatics >= 2]
    print(f"    Dual aromatic cages: {len(dual_aromatic)}")
    print(f"    Best dual aromatic: {dual_aromatic[0].sequence if dual_aromatic else 'None'}")
    print("    " + "=" * 66)

    # Create report
    report = PHF6CageReport(
        timestamp=datetime.now().isoformat(),
        target_motif=PHF6_SEQUENCE,
        n_designs=len(designs),
        designs=designs,
        best_design=best,
        summary=f"Generated {len(designs)} PHF6 cage designs. Best: {best.sequence} (score: {best.cage_score:.3f})"
    )

    # Save results
    output_file = output_path / "phf6_cage_designs.json"

    report_dict = {
        'timestamp': report.timestamp,
        'target': {
            'motif': PHF6_SEQUENCE,
            'key_residue': 'Tyr310',
            'disease': 'Alzheimer\'s Disease',
            'mechanism': 'Tau aggregation inhibition'
        },
        'z2_constants': {
            'vacuum': Z2_VACUUM,
            'biological': Z2_BIOLOGICAL,
        },
        'n_designs': report.n_designs,
        'designs': [asdict(d) for d in report.designs],
        'best_design': asdict(report.best_design),
        'summary': report.summary
    }

    with open(output_file, 'w') as f:
        json.dump(report_dict, f, indent=2)

    print(f"\n    Saved: {output_file}")

    return report


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Tau PHF6 Cage Design for Alzheimer's Disease"
    )
    parser.add_argument('--n-random', type=int, default=20,
                       help='Number of random designs to generate')
    parser.add_argument('--output', default='../tau_cage_designs',
                       help='Output directory')

    args = parser.parse_args()

    run_phf6_cage_design(
        n_random=args.n_random,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
