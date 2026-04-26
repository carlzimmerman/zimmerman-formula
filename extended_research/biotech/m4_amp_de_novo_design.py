#!/usr/bin/env python3
"""
M4 Antimicrobial Peptide (AMP) De Novo Designer
================================================

Designs novel antimicrobial peptides that:
1. Form amphipathic alpha-helices (hydrophobic face + hydrophilic face)
2. Have net positive charge (+3 to +6) for bacterial membrane selectivity
3. Selectively bind anionic bacterial membranes over zwitterionic mammalian membranes

THE ANTIBIOTIC APOCALYPSE:
Bacteria are evolving resistance to chemical antibiotics. AMPs use PHYSICAL
mechanisms (membrane disruption) that are harder to evolve resistance against.

MECHANISM:
- Amphipathic helix inserts hydrophobic face into lipid bilayer
- Cationic residues bind anionic bacterial membrane (not mammalian)
- Multiple peptides oligomerize to form pores ("barrel-stave" or "toroidal")
- Membrane integrity lost → bacterial death

LICENSE: AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0
AUTHOR: Carl Zimmerman
DATE: April 2026

PRIOR ART: This design methodology is released as open-source prior art
to prevent corporate capture of AMP therapeutic development.
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random
import math

# =============================================================================
# CONSTANTS
# =============================================================================

# Amino acid properties
AA_HYDROPHOBICITY = {
    # Kyte-Doolittle scale
    'A':  1.8, 'C':  2.5, 'D': -3.5, 'E': -3.5, 'F':  2.8,
    'G': -0.4, 'H': -3.2, 'I':  4.5, 'K': -3.9, 'L':  3.8,
    'M':  1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5,
    'S': -0.8, 'T': -0.7, 'V':  4.2, 'W': -0.9, 'Y': -1.3,
}

AA_CHARGE = {
    # Charge at pH 7.4
    'A': 0, 'C': 0, 'D': -1, 'E': -1, 'F': 0,
    'G': 0, 'H': 0.1, 'I': 0, 'K': 1, 'L': 0,  # H is ~10% protonated at pH 7.4
    'M': 0, 'N': 0, 'P': 0, 'Q': 0, 'R': 1,
    'S': 0, 'T': 0, 'V': 0, 'W': 0, 'Y': 0,
}

AA_HELIX_PROPENSITY = {
    # Chou-Fasman helix propensity (higher = more helical)
    'A': 1.42, 'C': 0.70, 'D': 1.01, 'E': 1.51, 'F': 1.13,
    'G': 0.57, 'H': 1.00, 'I': 1.08, 'K': 1.16, 'L': 1.21,
    'M': 1.45, 'N': 0.67, 'P': 0.57, 'Q': 1.11, 'R': 0.98,
    'S': 0.77, 'T': 0.83, 'V': 1.06, 'W': 1.08, 'Y': 0.69,
}

# Ideal AMP parameters
IDEAL_LENGTH_MIN = 20
IDEAL_LENGTH_MAX = 30
IDEAL_CHARGE_MIN = 3
IDEAL_CHARGE_MAX = 6
IDEAL_HYDROPHOBIC_MOMENT_MIN = 0.4  # Normalized
IDEAL_HYDROPHOBICITY_MEAN = 0.0     # Slightly amphipathic

# Alpha helix geometry
HELIX_RESIDUES_PER_TURN = 3.6
HELIX_ANGLE_PER_RESIDUE = 100  # degrees (360/3.6)

# Amino acid categories for AMP design
HYDROPHOBIC_AA = ['L', 'I', 'V', 'F', 'W', 'A', 'M']  # Helix-forming hydrophobic
CATIONIC_AA = ['K', 'R']  # Positive charge
POLAR_AA = ['S', 'T', 'N', 'Q']  # Neutral polar
HELIX_BREAKERS = ['P', 'G']  # Avoid in helix core


# =============================================================================
# AMPHIPATHIC HELIX DESIGN
# =============================================================================

@dataclass
class AMPCandidate:
    """Antimicrobial peptide candidate."""
    sequence: str
    length: int
    net_charge: float
    hydrophobic_moment: float
    mean_hydrophobicity: float
    helix_propensity: float
    amphipathicity_score: float
    selectivity_score: float
    overall_score: float
    design_notes: str


def calculate_net_charge(sequence: str) -> float:
    """Calculate net charge at pH 7.4."""
    return sum(AA_CHARGE.get(aa, 0) for aa in sequence)


def calculate_mean_hydrophobicity(sequence: str) -> float:
    """Calculate mean hydrophobicity."""
    values = [AA_HYDROPHOBICITY.get(aa, 0) for aa in sequence]
    return np.mean(values) if values else 0


def calculate_helix_propensity(sequence: str) -> float:
    """Calculate mean helix propensity."""
    values = [AA_HELIX_PROPENSITY.get(aa, 1.0) for aa in sequence]
    return np.mean(values) if values else 1.0


def calculate_hydrophobic_moment(sequence: str) -> float:
    """
    Calculate hydrophobic moment (μH) for an ideal alpha helix.

    The hydrophobic moment is the vector sum of hydrophobicity values
    projected onto a helical wheel. High μH indicates amphipathicity.

    μH = sqrt(sum_i(H_i * sin(i*δ))² + sum_i(H_i * cos(i*δ))²) / N

    where δ = 100° (angle per residue in alpha helix)
    """
    if len(sequence) < 3:
        return 0.0

    delta = math.radians(HELIX_ANGLE_PER_RESIDUE)

    sum_sin = 0.0
    sum_cos = 0.0

    for i, aa in enumerate(sequence):
        h = AA_HYDROPHOBICITY.get(aa, 0)
        angle = i * delta
        sum_sin += h * math.sin(angle)
        sum_cos += h * math.cos(angle)

    mu_h = math.sqrt(sum_sin**2 + sum_cos**2) / len(sequence)

    # Normalize to 0-1 scale (typical range is 0-0.6)
    return min(mu_h / 0.6, 1.0)


def calculate_amphipathicity_score(sequence: str) -> float:
    """
    Score how well the sequence forms an amphipathic helix.

    Ideal: hydrophobic residues on one face, cationic on other.
    """
    if len(sequence) < 7:
        return 0.0

    # Check helical wheel positions
    # Positions 0, 3-4, 7 should be similar (same face)
    # Positions 1-2, 5-6 should be similar (opposite face)

    face_a = []  # Positions 0, 3, 4, 7, 10, 11, 14... (hydrophobic face)
    face_b = []  # Positions 1, 2, 5, 6, 8, 9, 12, 13... (hydrophilic face)

    for i, aa in enumerate(sequence):
        # Simplified helical wheel assignment
        pos_in_turn = i % 7
        if pos_in_turn in [0, 3, 4]:
            face_a.append(AA_HYDROPHOBICITY.get(aa, 0))
        else:
            face_b.append(AA_HYDROPHOBICITY.get(aa, 0))

    # Ideal: face_a hydrophobic (positive), face_b hydrophilic (negative)
    mean_a = np.mean(face_a) if face_a else 0
    mean_b = np.mean(face_b) if face_b else 0

    # Score based on difference (higher = more amphipathic)
    amphipathicity = (mean_a - mean_b) / 8.0  # Normalize

    return max(0, min(1, amphipathicity + 0.5))


def calculate_selectivity_score(sequence: str, net_charge: float) -> float:
    """
    Score selectivity for bacterial vs mammalian membranes.

    Bacterial membranes: anionic (phosphatidylglycerol, cardiolipin)
    Mammalian membranes: zwitterionic (phosphatidylcholine)

    High positive charge + moderate hydrophobicity = bacterial selective
    """
    # Charge component (optimal: +3 to +6)
    if IDEAL_CHARGE_MIN <= net_charge <= IDEAL_CHARGE_MAX:
        charge_score = 1.0
    elif net_charge > IDEAL_CHARGE_MAX:
        charge_score = max(0, 1 - (net_charge - IDEAL_CHARGE_MAX) / 4)
    else:
        charge_score = max(0, net_charge / IDEAL_CHARGE_MIN)

    # Hydrophobicity component (moderate is best)
    mean_h = calculate_mean_hydrophobicity(sequence)
    if -1.0 <= mean_h <= 1.0:
        hydro_score = 1.0
    else:
        hydro_score = max(0, 1 - abs(mean_h) / 3)

    # Tryptophan bonus (anchors at membrane interface)
    trp_count = sequence.count('W')
    trp_score = min(1.0, trp_count * 0.3)

    return 0.5 * charge_score + 0.3 * hydro_score + 0.2 * trp_score


def design_amphipathic_sequence(length: int, target_charge: int) -> str:
    """
    Design an amphipathic alpha-helix sequence.

    Strategy:
    1. Place cationic residues (K, R) at hydrophilic positions
    2. Place hydrophobic residues (L, I, V, F, W) at hydrophobic positions
    3. Ensure overall charge matches target
    4. Avoid helix breakers (P, G) except at termini
    """
    sequence = ['A'] * length  # Start with alanine (good helix former)

    # Define helical wheel positions (simplified)
    # In a 3.6 residue/turn helix, positions form faces
    hydrophobic_positions = []
    hydrophilic_positions = []

    for i in range(length):
        angle = (i * 100) % 360
        if 60 <= angle <= 180:  # One face
            hydrophobic_positions.append(i)
        else:
            hydrophilic_positions.append(i)

    # Place hydrophobic residues
    for pos in hydrophobic_positions:
        sequence[pos] = random.choice(HYDROPHOBIC_AA)

    # Place cationic residues to achieve target charge
    cationic_placed = 0
    random.shuffle(hydrophilic_positions)

    for pos in hydrophilic_positions:
        if cationic_placed < target_charge:
            sequence[pos] = random.choice(CATIONIC_AA)
            cationic_placed += 1
        else:
            # Fill remaining with polar or small hydrophobic
            sequence[pos] = random.choice(POLAR_AA + ['A', 'S'])

    # Add 1-2 tryptophans for membrane anchoring (near termini)
    if length >= 20:
        sequence[2] = 'W'
        sequence[-3] = 'W'

    return ''.join(sequence)


def generate_amp_library(
    n_candidates: int = 100,
    length_range: Tuple[int, int] = (20, 26),
    charge_range: Tuple[int, int] = (3, 6),
) -> List[AMPCandidate]:
    """Generate a library of AMP candidates."""

    candidates = []

    for _ in range(n_candidates):
        # Random parameters within ranges
        length = random.randint(length_range[0], length_range[1])
        target_charge = random.randint(charge_range[0], charge_range[1])

        # Design sequence
        sequence = design_amphipathic_sequence(length, target_charge)

        # Calculate properties
        net_charge = calculate_net_charge(sequence)
        hydrophobic_moment = calculate_hydrophobic_moment(sequence)
        mean_hydrophobicity = calculate_mean_hydrophobicity(sequence)
        helix_propensity = calculate_helix_propensity(sequence)
        amphipathicity = calculate_amphipathicity_score(sequence)
        selectivity = calculate_selectivity_score(sequence, net_charge)

        # Overall score
        overall = (
            0.25 * hydrophobic_moment +
            0.25 * amphipathicity +
            0.25 * selectivity +
            0.15 * min(1, helix_propensity / 1.2) +
            0.10 * (1 if IDEAL_CHARGE_MIN <= net_charge <= IDEAL_CHARGE_MAX else 0.5)
        )

        candidate = AMPCandidate(
            sequence=sequence,
            length=length,
            net_charge=net_charge,
            hydrophobic_moment=hydrophobic_moment,
            mean_hydrophobicity=mean_hydrophobicity,
            helix_propensity=helix_propensity,
            amphipathicity_score=amphipathicity,
            selectivity_score=selectivity,
            overall_score=overall,
            design_notes=f"Designed for charge +{target_charge}, length {length}",
        )

        candidates.append(candidate)

    # Sort by overall score
    candidates.sort(key=lambda x: x.overall_score, reverse=True)

    return candidates


# =============================================================================
# STRUCTURE PREDICTION (Heuristic for speed, ESMFold for validation)
# =============================================================================

def predict_secondary_structure(sequence: str) -> Dict:
    """
    Predict secondary structure content.

    For AMPs designed as alpha-helices, we expect high helix content.
    This is a heuristic; ESMFold validation recommended for top candidates.
    """
    helix_score = calculate_helix_propensity(sequence)

    # Count helix breakers
    breakers = sum(1 for aa in sequence if aa in HELIX_BREAKERS)
    breaker_penalty = breakers / len(sequence)

    # Estimate helix content
    estimated_helix = max(0, min(1, (helix_score - 0.7) * 2 - breaker_penalty))

    return {
        'estimated_helix_fraction': estimated_helix,
        'helix_propensity': helix_score,
        'helix_breakers': breakers,
        'prediction_method': 'heuristic',
        'note': 'ESMFold validation recommended for top candidates',
    }


def calculate_membrane_disruption_potential(candidate: AMPCandidate) -> float:
    """
    Estimate membrane disruption potential.

    Based on:
    1. Hydrophobic moment (insertion capability)
    2. Net charge (bacterial membrane binding)
    3. Amphipathicity (pore formation)
    4. Length (spanning capability)
    """
    # Length score (20-26 optimal for membrane spanning)
    if 20 <= candidate.length <= 26:
        length_score = 1.0
    elif candidate.length < 20:
        length_score = candidate.length / 20
    else:
        length_score = max(0.5, 1 - (candidate.length - 26) / 10)

    # Combined disruption potential
    potential = (
        0.30 * candidate.hydrophobic_moment +
        0.25 * candidate.amphipathicity_score +
        0.25 * candidate.selectivity_score +
        0.20 * length_score
    )

    return potential


# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def generate_fasta_header(candidate: AMPCandidate, rank: int) -> str:
    """Generate FASTA header with metadata."""
    return (
        f">AMP_ZF_{rank:03d} "
        f"length={candidate.length} "
        f"charge=+{candidate.net_charge:.0f} "
        f"uH={candidate.hydrophobic_moment:.3f} "
        f"score={candidate.overall_score:.3f} "
        f"| AGPL-3.0 + OpenMTA + CC-BY-SA-4.0"
    )


def export_fasta(
    candidates: List[AMPCandidate],
    output_file: str,
    n_top: int = 10,
) -> str:
    """Export top candidates to FASTA format."""

    lines = [
        "# Antimicrobial Peptide Candidates",
        "# Designed by M4 AMP De Novo Designer",
        f"# Generated: {datetime.now().isoformat()}",
        "#",
        "# LICENSE: AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0",
        "# This work is released as PRIOR ART to prevent corporate capture.",
        "# Any derivative work must remain open-source.",
        "#",
        "# DISCLAIMER: These are computational designs, NOT validated drugs.",
        "# Experimental validation required before any therapeutic use.",
        "#",
    ]

    for i, candidate in enumerate(candidates[:n_top], 1):
        lines.append(generate_fasta_header(candidate, i))
        # Wrap sequence at 60 characters
        seq = candidate.sequence
        for j in range(0, len(seq), 60):
            lines.append(seq[j:j+60])

    content = '\n'.join(lines)

    with open(output_file, 'w') as f:
        f.write(content)

    return content


def export_detailed_report(
    candidates: List[AMPCandidate],
    output_file: str,
    n_top: int = 10,
) -> Dict:
    """Export detailed analysis report."""

    report = {
        'metadata': {
            'generator': 'M4 AMP De Novo Designer',
            'timestamp': datetime.now().isoformat(),
            'license': 'AGPL-3.0-or-later + OpenMTA + CC-BY-SA-4.0',
            'total_candidates': len(candidates),
            'top_n': n_top,
        },
        'design_parameters': {
            'length_range': [IDEAL_LENGTH_MIN, IDEAL_LENGTH_MAX],
            'charge_range': [IDEAL_CHARGE_MIN, IDEAL_CHARGE_MAX],
            'target_structure': 'amphipathic alpha-helix',
            'target_mechanism': 'membrane disruption',
        },
        'top_candidates': [],
    }

    for i, candidate in enumerate(candidates[:n_top], 1):
        disruption = calculate_membrane_disruption_potential(candidate)
        structure = predict_secondary_structure(candidate.sequence)

        entry = {
            'rank': i,
            'sequence': candidate.sequence,
            'length': candidate.length,
            'net_charge': candidate.net_charge,
            'hydrophobic_moment': round(candidate.hydrophobic_moment, 4),
            'mean_hydrophobicity': round(candidate.mean_hydrophobicity, 4),
            'helix_propensity': round(candidate.helix_propensity, 4),
            'amphipathicity_score': round(candidate.amphipathicity_score, 4),
            'selectivity_score': round(candidate.selectivity_score, 4),
            'membrane_disruption_potential': round(disruption, 4),
            'overall_score': round(candidate.overall_score, 4),
            'structure_prediction': structure,
            'design_notes': candidate.design_notes,
        }

        report['top_candidates'].append(entry)

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    return report


# =============================================================================
# MAIN
# =============================================================================

def run_amp_design(
    n_candidates: int = 500,
    n_top: int = 10,
    output_dir: str = "amp_designs",
) -> Dict:
    """Run the full AMP design pipeline."""

    print("="*70)
    print("M4 ANTIMICROBIAL PEPTIDE DE NOVO DESIGNER")
    print("="*70)
    print(f"\nTarget: Amphipathic alpha-helices for membrane disruption")
    print(f"Candidates to generate: {n_candidates}")
    print(f"Top candidates to select: {n_top}")

    # Create output directory
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True)

    # Generate library
    print(f"\nGenerating {n_candidates} candidates...")
    candidates = generate_amp_library(
        n_candidates=n_candidates,
        length_range=(20, 26),
        charge_range=(3, 6),
    )

    print(f"Generated {len(candidates)} candidates")

    # Analyze top candidates
    print(f"\nTop {n_top} candidates:")
    print("-"*70)
    print(f"{'Rank':<5} {'Sequence':<28} {'Len':<4} {'Chg':<4} {'μH':<6} {'Score':<6}")
    print("-"*70)

    for i, c in enumerate(candidates[:n_top], 1):
        seq_display = c.sequence[:25] + "..." if len(c.sequence) > 25 else c.sequence
        print(f"{i:<5} {seq_display:<28} {c.length:<4} +{c.net_charge:<3.0f} {c.hydrophobic_moment:<6.3f} {c.overall_score:<6.3f}")

    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    fasta_file = out_path / f"amp_candidates_{timestamp}.fasta"
    export_fasta(candidates, str(fasta_file), n_top)
    print(f"\nFASTA exported: {fasta_file}")

    json_file = out_path / f"amp_detailed_report_{timestamp}.json"
    report = export_detailed_report(candidates, str(json_file), n_top)
    print(f"Report exported: {json_file}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    top = candidates[0]
    print(f"\nBest candidate: {top.sequence}")
    print(f"  Length: {top.length} residues")
    print(f"  Net charge: +{top.net_charge:.0f}")
    print(f"  Hydrophobic moment: {top.hydrophobic_moment:.3f}")
    print(f"  Amphipathicity: {top.amphipathicity_score:.3f}")
    print(f"  Selectivity: {top.selectivity_score:.3f}")
    print(f"  Overall score: {top.overall_score:.3f}")

    disruption = calculate_membrane_disruption_potential(top)
    print(f"  Membrane disruption potential: {disruption:.3f}")

    print("\n" + "="*70)
    print("MECHANISM OF ACTION")
    print("="*70)
    print("""
Designed AMPs work by PHYSICAL membrane disruption:

1. BINDING: Cationic residues (+3 to +6) bind anionic bacterial membrane
   (phosphatidylglycerol, cardiolipin) but NOT zwitterionic mammalian
   membranes (phosphatidylcholine).

2. INSERTION: Hydrophobic face of amphipathic helix inserts into lipid
   bilayer. Tryptophans anchor at membrane-water interface.

3. OLIGOMERIZATION: Multiple peptides associate to form pores
   ("barrel-stave" or "toroidal pore" models).

4. DISRUPTION: Membrane integrity lost → ion leakage → cell death.

Because this is a PHYSICAL mechanism (not enzyme geometrically stabilize), bacteria
cannot easily evolve resistance through single mutations.
""")

    print("="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
1. ESMFold validation - Confirm helical structure prediction
2. Molecular dynamics - Simulate membrane insertion
3. Hemolysis assay - Verify mammalian cell safety
4. MIC determination - Measure bacterial killing (E. coli, S. aureus)
5. Resistance evolution - Serial passage to test durability
""")

    print("\n" + "="*70)
    print("LICENSE & PRIOR ART")
    print("="*70)
    print("""
These designs are released under triple license:
  - AGPL-3.0-or-later (code)
  - OpenMTA (materials)
  - CC-BY-SA-4.0 (documentation)

PRIOR ART ESTABLISHED: April 20, 2026

This prevents patenting of these specific sequences and design methodology.
Any derivative work must remain open-source.
""")

    return {
        'candidates': candidates[:n_top],
        'fasta_file': str(fasta_file),
        'json_file': str(json_file),
        'report': report,
    }


if __name__ == "__main__":
    results = run_amp_design(
        n_candidates=500,
        n_top=10,
        output_dir="amp_designs",
    )
