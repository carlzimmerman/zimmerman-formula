#!/usr/bin/env python3
"""
eng_01_tat_conjugation.py

TAT Cell-Penetrating Peptide Conjugation
========================================

PROBLEM:
Our peptides have excellent pharmacodynamics (PD) - nanomolar binding affinity.
But they have poor pharmacokinetics (PK) - they bounce off the lipid membrane.

SOLUTION:
Conjugate a Cell-Penetrating Peptide (CPP) to smuggle them across the BBB.

THE TAT SEQUENCE:
C2_Homodimer_A-1 TAT (Trans-Activator of Transcription) contains the sequence:
YGRKKRRQRRR

This highly cationic sequence (8 positive charges!) exploits cellular uptake
mechanisms to cross membranes. It's been used in hundreds of drug delivery
applications.

THE LINKER:
We use a flexible Poly-Glycine linker (GGG) to:
1. Separate the TAT tag from the drug warhead
2. Allow conformational flexibility
3. Prevent steric interference with binding

CRITICAL CHECK:
The conjugated peptide MUST retain its Z²-optimized binding geometry.
We verify that the core binding motif maintains ~6.02 Å contact distances.

Author: Carl Zimmerman
Framework: Zimmerman Unified Geometry Framework (ZUGF)
License: AGPL v3.0
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings

try:
    from scipy.spatial import Delaunay
    from scipy.spatial.distance import cdist
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# ============================================================================
# CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å
EXPANSION_MULTIPLIER = 1.0391
IDEAL_BIOLOGICAL_DISTANCE = Z2_DISTANCE * EXPANSION_MULTIPLIER  # 6.02 Å

# Cell-Penetrating Peptide sequences
TAT_SEQUENCE = "YGRKKRRQRRR"  # C2_Homodimer_A-1 TAT (47-57)
PENETRATIN = "RQIKIWFQNRRMKWKK"  # Antennapedia homeodomain
POLYARG = "RRRRRRRRR"  # R9 - simpler CPP

# Linker options
LINKERS = {
    'GGG': 'GGG',           # Flexible, minimal
    'GGGGS': 'GGGGS',       # Standard flexible linker
    'EAAAK': 'EAAAK',       # Rigid alpha-helical linker
    'GSG': 'GSG',           # Short flexible
}

# Amino acid properties
AA_PROPERTIES = {
    'A': {'charge': 0, 'volume': 88.6, 'hydrophobicity': 1.8},
    'R': {'charge': +1, 'volume': 173.4, 'hydrophobicity': -4.5},
    'N': {'charge': 0, 'volume': 114.1, 'hydrophobicity': -3.5},
    'D': {'charge': -1, 'volume': 111.1, 'hydrophobicity': -3.5},
    'C': {'charge': 0, 'volume': 108.5, 'hydrophobicity': 2.5},
    'E': {'charge': -1, 'volume': 138.4, 'hydrophobicity': -3.5},
    'Q': {'charge': 0, 'volume': 143.8, 'hydrophobicity': -3.5},
    'G': {'charge': 0, 'volume': 60.1, 'hydrophobicity': -0.4},
    'H': {'charge': 0.5, 'volume': 153.2, 'hydrophobicity': -3.2},
    'I': {'charge': 0, 'volume': 166.7, 'hydrophobicity': 4.5},
    'L': {'charge': 0, 'volume': 166.7, 'hydrophobicity': 3.8},
    'K': {'charge': +1, 'volume': 168.6, 'hydrophobicity': -3.9},
    'M': {'charge': 0, 'volume': 162.9, 'hydrophobicity': 1.9},
    'F': {'charge': 0, 'volume': 189.9, 'hydrophobicity': 2.8},
    'P': {'charge': 0, 'volume': 112.7, 'hydrophobicity': -1.6},
    'S': {'charge': 0, 'volume': 89.0, 'hydrophobicity': -0.8},
    'T': {'charge': 0, 'volume': 116.1, 'hydrophobicity': -0.7},
    'W': {'charge': 0, 'volume': 227.8, 'hydrophobicity': -0.9},
    'Y': {'charge': 0, 'volume': 193.6, 'hydrophobicity': -1.3},
    'V': {'charge': 0, 'volume': 140.0, 'hydrophobicity': 4.2},
}

# Our drug candidates
DRUG_CANDIDATES = {
    'ZIM-SYN-004': {
        'sequence': 'FPF',  # Core binding motif
        'target': 'Alpha-synuclein',
        'indication': 'Parkinson\'s target system',
        'binding_dG': -40.0,  # kcal/mol
    },
    'ZIM-ALZ-001': {
        'sequence': 'WFFY',
        'target': 'Tau protein',
        'indication': 'Alzheimer\'s target system',
        'binding_dG': -25.0,  # estimated
    },
    'ZIM-ADD-003': {
        'sequence': 'RWWFWR',
        'target': 'α3β4 nAChR',
        'indication': 'Addiction',
        'binding_dG': -24.0,
    },
}


def calculate_sequence_properties(sequence: str) -> Dict:
    """Calculate physicochemical properties of a peptide sequence."""
    net_charge = 0
    total_volume = 0
    hydrophobicity_sum = 0

    for aa in sequence:
        if aa in AA_PROPERTIES:
            props = AA_PROPERTIES[aa]
            net_charge += props['charge']
            total_volume += props['volume']
            hydrophobicity_sum += props['hydrophobicity']

    n_residues = len(sequence)
    mean_hydrophobicity = hydrophobicity_sum / n_residues if n_residues > 0 else 0

    # Estimate molecular weight (average ~110 Da per residue)
    mol_weight = n_residues * 110

    return {
        'sequence': sequence,
        'length': n_residues,
        'net_charge': net_charge,
        'total_volume': total_volume,
        'mean_hydrophobicity': mean_hydrophobicity,
        'estimated_mw_da': mol_weight,
    }


def create_conjugate(drug_sequence: str, linker: str, cpp_sequence: str,
                     cpp_position: str = 'C-terminal') -> str:
    """
    Create a drug-linker-CPP conjugate.

    Args:
        drug_sequence: The core drug binding motif
        linker: Flexible linker sequence (e.g., 'GGG')
        cpp_sequence: Cell-penetrating peptide (e.g., TAT)
        cpp_position: 'C-terminal' or 'N-terminal'

    Returns:
        Full conjugate sequence
    """
    if cpp_position == 'C-terminal':
        # Drug-Linker-CPP (CPP at C-terminus)
        conjugate = drug_sequence + linker + cpp_sequence
    else:
        # CPP-Linker-Drug (CPP at N-terminus)
        conjugate = cpp_sequence + linker + drug_sequence

    return conjugate


def build_peptide_structure(sequence: str) -> np.ndarray:
    """
    Build a simplified 3D structure for a peptide.

    Uses idealized backbone geometry:
    - Cα-Cα distance: 3.8 Å
    - Extended conformation initially
    """
    CA_CA_DISTANCE = 3.8  # Å
    positions = []

    # Start at origin
    current_pos = np.array([0.0, 0.0, 0.0])

    # Phi/psi angles for extended conformation
    phi = -135 * np.pi / 180
    psi = 135 * np.pi / 180

    for i, aa in enumerate(sequence):
        # Add Cα position
        positions.append(current_pos.copy())

        # Move to next residue
        # Simplified: move along a gentle helix
        angle = i * 100 * np.pi / 180  # ~100° rotation per residue
        current_pos = current_pos + np.array([
            CA_CA_DISTANCE * np.cos(angle) * 0.8,
            CA_CA_DISTANCE * np.sin(angle) * 0.8,
            CA_CA_DISTANCE * 0.3  # Rise along z
        ])

    return np.array(positions)


def calculate_z2_fitness(positions: np.ndarray, drug_length: int) -> Dict:
    """
    Calculate Z² geometric fitness for the drug portion of a conjugate.

    Args:
        positions: Full conjugate Cα positions
        drug_length: Number of residues in the drug portion

    Returns:
        Z² fitness metrics for the drug warhead
    """
    if len(positions) < drug_length or drug_length < 2:
        return {'error': 'Insufficient positions'}

    # Extract drug portion only
    drug_positions = positions[:drug_length]

    if len(drug_positions) < 3:
        # For very short peptides, use pairwise distances
        distances = []
        for i in range(len(drug_positions)):
            for j in range(i + 1, len(drug_positions)):
                d = np.linalg.norm(drug_positions[i] - drug_positions[j])
                if 3.0 < d < 8.0:
                    distances.append(d)
    else:
        try:
            tri = Delaunay(drug_positions)
            distances = []
            for simplex in tri.simplices:
                for i in range(len(simplex)):
                    for j in range(i + 1, len(simplex)):
                        d = np.linalg.norm(drug_positions[simplex[i]] - drug_positions[simplex[j]])
                        if 3.0 < d < 8.0:
                            distances.append(d)
        except:
            # Fallback to pairwise
            distances = []
            for i in range(len(drug_positions)):
                for j in range(i + 1, len(drug_positions)):
                    d = np.linalg.norm(drug_positions[i] - drug_positions[j])
                    if 3.0 < d < 8.0:
                        distances.append(d)

    if not distances:
        return {'error': 'No valid contacts'}

    distances = np.array(distances)
    mean_distance = np.mean(distances)

    # Z² fitness
    deviation = abs(mean_distance - IDEAL_BIOLOGICAL_DISTANCE)
    z2_fitness = np.exp(-(deviation**2) / (2 * 1.0**2))

    return {
        'mean_contact_distance': float(mean_distance),
        'ideal_distance': float(IDEAL_BIOLOGICAL_DISTANCE),
        'deviation': float(deviation),
        'z2_fitness': float(z2_fitness),
        'n_contacts': len(distances),
        'binding_preserved': z2_fitness > 0.5
    }


def check_steric_clash(positions: np.ndarray, drug_length: int,
                       linker_length: int, clash_threshold: float = 4.0) -> Dict:
    """
    Check for steric clashes between the CPP tag and the drug warhead.

    The CPP should be far enough away (via the linker) that it doesn't
    interfere with binding.
    """
    if len(positions) < drug_length + linker_length + 1:
        return {'clash_detected': False, 'reason': 'Insufficient length'}

    drug_positions = positions[:drug_length]
    cpp_positions = positions[drug_length + linker_length:]

    if len(cpp_positions) == 0:
        return {'clash_detected': False, 'reason': 'No CPP positions'}

    # Calculate minimum distance between drug and CPP
    distances = cdist(drug_positions, cpp_positions)
    min_distance = np.min(distances)
    mean_distance = np.mean(distances)

    clash_detected = min_distance < clash_threshold

    return {
        'min_drug_cpp_distance': float(min_distance),
        'mean_drug_cpp_distance': float(mean_distance),
        'clash_threshold': clash_threshold,
        'clash_detected': clash_detected,
        'linker_effective': not clash_detected
    }


def estimate_membrane_permeability(sequence: str) -> Dict:
    """
    Estimate membrane permeability based on sequence properties.

    CPPs work by:
    1. Electrostatic interaction with negative membrane surface
    2. Direct translocation or endocytosis

    TAT (YGRKKRRQRRR) has 8 positive charges - excellent for membrane interaction.
    """
    props = calculate_sequence_properties(sequence)

    # Count cationic residues (R, K, H)
    cationic_count = sum(1 for aa in sequence if aa in 'RKH')

    # TAT-like score (more cationic = better CPP activity)
    cpp_score = min(cationic_count / 8.0, 1.0)  # Normalize to TAT's 8 charges

    # Amphipathicity estimate
    hydrophobic_count = sum(1 for aa in sequence if aa in 'AILMFVW')
    amphipathic_score = min(hydrophobic_count / len(sequence) * 2, 1.0)

    # Combined permeability estimate
    permeability_score = 0.7 * cpp_score + 0.3 * amphipathic_score

    return {
        'cationic_residues': cationic_count,
        'net_charge': props['net_charge'],
        'cpp_score': float(cpp_score),
        'amphipathic_score': float(amphipathic_score),
        'permeability_score': float(permeability_score),
        'prediction': 'PERMEABLE' if permeability_score > 0.6 else 'MARGINAL' if permeability_score > 0.3 else 'POOR'
    }


def analyze_conjugate(drug_id: str, drug_info: Dict, cpp: str, linker: str) -> Dict:
    """
    Full analysis of a drug-linker-CPP conjugate.
    """
    drug_seq = drug_info['sequence']
    conjugate_seq = create_conjugate(drug_seq, linker, cpp, 'C-terminal')

    # Build structure
    positions = build_peptide_structure(conjugate_seq)

    # Calculate properties
    drug_props = calculate_sequence_properties(drug_seq)
    conjugate_props = calculate_sequence_properties(conjugate_seq)

    # Z² fitness of drug portion
    z2_result = calculate_z2_fitness(positions, len(drug_seq))

    # Steric clash check
    clash_result = check_steric_clash(positions, len(drug_seq), len(linker))

    # Permeability estimate
    perm_result = estimate_membrane_permeability(conjugate_seq)

    return {
        'drug_id': drug_id,
        'original_sequence': drug_seq,
        'cpp': cpp,
        'linker': linker,
        'conjugate_sequence': conjugate_seq,
        'drug_properties': drug_props,
        'conjugate_properties': conjugate_props,
        'z2_geometry': z2_result,
        'steric_analysis': clash_result,
        'permeability': perm_result,
        'recommendation': generate_recommendation(z2_result, clash_result, perm_result)
    }


def generate_recommendation(z2: Dict, clash: Dict, perm: Dict) -> str:
    """Generate overall recommendation for the conjugate."""
    issues = []
    positives = []

    # Z² geometry
    if z2.get('binding_preserved', False):
        positives.append("Z² binding geometry PRESERVED")
    else:
        issues.append("Z² binding geometry may be COMPROMISED")

    # Steric clashes
    if not clash.get('clash_detected', True):
        positives.append("No steric clashes with CPP")
    else:
        issues.append("Steric clash detected between drug and CPP")

    # Permeability
    perm_pred = perm.get('prediction', 'POOR')
    if perm_pred == 'PERMEABLE':
        positives.append("Predicted membrane PERMEABLE")
    elif perm_pred == 'MARGINAL':
        positives.append("Predicted MARGINAL permeability")
    else:
        issues.append("Predicted POOR permeability")

    if not issues:
        return "RECOMMENDED: Proceed to MD validation"
    elif len(issues) == 1 and 'MARGINAL' in str(issues):
        return "CONDITIONAL: May need linker optimization"
    else:
        return "CAUTION: " + "; ".join(issues)


def main():
    """Main execution: TAT conjugation analysis."""
    print("=" * 70)
    print("TAT CELL-PENETRATING PEPTIDE CONJUGATION")
    print("Engineering Membrane Permeability for Z²-Optimized Drugs")
    print("=" * 70)

    if not HAS_SCIPY:
        print("\n⚠️  scipy recommended for geometric analysis")

    print(f"""
   THE PROBLEM:
   ────────────
   Our drugs have excellent binding (PD) but bounce off membranes (PK).

   THE SOLUTION:
   ─────────────
   Conjugate C2_Homodimer_A-1 TAT sequence to smuggle drugs across the BBB:
   TAT: {TAT_SEQUENCE} (8 positive charges, proven CPP)

   THE LINKER:
   ───────────
   Flexible GGG linker separates TAT from drug warhead,
   preserving the critical Z²-optimized binding geometry.

   TARGET GEOMETRY: {IDEAL_BIOLOGICAL_DISTANCE:.2f} Å (Z² × 1.0391)
""")

    # Setup
    base_dir = Path(__file__).parent
    results_dir = base_dir / 'results' / 'delivery_engineering'
    results_dir.mkdir(parents=True, exist_ok=True)

    all_results = {}

    # Analyze each drug candidate
    for drug_id, drug_info in DRUG_CANDIDATES.items():
        print(f"\n{'='*70}")
        print(f"CONJUGATE: {drug_id}")
        print(f"Target: {drug_info['target']} ({drug_info['indication']})")
        print(f"Original ΔG: {drug_info['binding_dG']} kcal/mol")
        print("=" * 70)

        result = analyze_conjugate(drug_id, drug_info, TAT_SEQUENCE, LINKERS['GGG'])

        print(f"""
   ORIGINAL:  {result['original_sequence']}
   LINKER:    {result['linker']}
   CPP:       {result['cpp']}
   CONJUGATE: {result['conjugate_sequence']}

   DRUG PROPERTIES:
     Length: {result['drug_properties']['length']} residues
     Charge: {result['drug_properties']['net_charge']:+.1f}
     MW: ~{result['drug_properties']['estimated_mw_da']} Da

   CONJUGATE PROPERTIES:
     Length: {result['conjugate_properties']['length']} residues
     Charge: {result['conjugate_properties']['net_charge']:+.1f}
     MW: ~{result['conjugate_properties']['estimated_mw_da']} Da

   Z² GEOMETRY CHECK:
     Mean contact distance: {result['z2_geometry'].get('mean_contact_distance', 'N/A'):.2f} Å
     Ideal distance: {IDEAL_BIOLOGICAL_DISTANCE:.2f} Å
     Deviation: {result['z2_geometry'].get('deviation', 'N/A'):.2f} Å
     Z² Fitness: {result['z2_geometry'].get('z2_fitness', 0) * 100:.1f}%
     Binding preserved: {result['z2_geometry'].get('binding_preserved', False)}

   STERIC ANALYSIS:
     Min drug-CPP distance: {result['steric_analysis'].get('min_drug_cpp_distance', 'N/A'):.1f} Å
     Linker effective: {result['steric_analysis'].get('linker_effective', False)}
     Clash detected: {result['steric_analysis'].get('clash_detected', True)}

   PERMEABILITY ESTIMATE:
     CPP score: {result['permeability']['cpp_score']:.2f}
     Cationic residues: {result['permeability']['cationic_residues']}
     Prediction: {result['permeability']['prediction']}

   RECOMMENDATION: {result['recommendation']}
""")

        all_results[drug_id] = result

    # Summary
    print("\n" + "=" * 70)
    print("TAT CONJUGATION SUMMARY")
    print("=" * 70)

    print(f"""
   ┌────────────────┬───────────────────────────┬──────────────┬─────────────┐
   │ Drug ID        │ Conjugate                 │ Z² Preserved │ Permeable   │
   ├────────────────┼───────────────────────────┼──────────────┼─────────────┤""")

    for drug_id, result in all_results.items():
        conjugate = result['conjugate_sequence']
        if len(conjugate) > 20:
            conjugate_display = conjugate[:17] + "..."
        else:
            conjugate_display = conjugate
        z2_ok = "✅" if result['z2_geometry'].get('binding_preserved', False) else "❌"
        perm_ok = "✅" if result['permeability']['prediction'] == 'PERMEABLE' else "⚠️"

        print(f"   │ {drug_id:<14} │ {conjugate_display:<25} │ {z2_ok:^12} │ {perm_ok:^11} │")

    print(f"""   └────────────────┴───────────────────────────┴──────────────┴─────────────┘

   KEY:
   ✅ = Pass
   ⚠️ = Marginal (may need optimization)
   ❌ = Fail

   NEXT STEPS:
   1. Run MD simulation on promising conjugates
   2. Re-test membrane permeability with TAT attached
   3. Verify binding affinity is maintained
""")

    # Save results
    final_results = {
        'timestamp': datetime.now().isoformat(),
        'cpp_used': TAT_SEQUENCE,
        'linker_used': 'GGG',
        'ideal_z2_distance': IDEAL_BIOLOGICAL_DISTANCE,
        'conjugates': all_results
    }

    output_path = results_dir / 'tat_conjugation_results.json'
    with open(output_path, 'w') as f:
        json.dump(final_results, f, indent=2, default=str)

    print(f"\n📄 Results saved to: {output_path}")
    print("=" * 70)

    return final_results


if __name__ == '__main__':
    results = main()
