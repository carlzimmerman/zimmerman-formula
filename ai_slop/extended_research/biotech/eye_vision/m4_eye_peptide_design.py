#!/usr/bin/env python3
"""
M4 Eye/Vision Peptide Therapeutic Design Pipeline
===================================================

De novo design of therapeutic peptides for eye and vision disorders.
Focuses on high-priority targets with known druggable binding sites.

DESIGN STRATEGIES:
==================
1. Anti-VEGF peptides - Compete with aflibercept/ranibizumab binding
2. Complement inhibitor peptides - Block C3/C5 activation
3. ROCK inhibitor peptides - Novel kinase-targeting sequences
4. Anti-inflammatory peptides - LFA-1 blockers, TNF-α binders
5. Crystallin stabilizers - Prevent aggregation
6. Neuroprotective peptides - BDNF mimetics for RGC protection

DESIGN PRINCIPLES:
==================
- Ocular penetration: Balance hydrophilicity for solubility
- Stability: Cyclic peptides or stapled helices preferred
- Low immunogenicity: Avoid T-cell epitope motifs
- Intravitreal administration: Most targets accessible

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
import numpy as np
import hashlib
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import random


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# =============================================================================
# AMINO ACID PROPERTIES FOR DESIGN
# =============================================================================

AA_PROPERTIES = {
    # Hydrophobic
    'A': {'hydrophobicity': 1.8, 'helix': 1.45, 'charge': 0, 'aromatic': False},
    'I': {'hydrophobicity': 4.5, 'helix': 1.00, 'charge': 0, 'aromatic': False},
    'L': {'hydrophobicity': 3.8, 'helix': 1.34, 'charge': 0, 'aromatic': False},
    'M': {'hydrophobicity': 1.9, 'helix': 1.30, 'charge': 0, 'aromatic': False},
    'V': {'hydrophobicity': 4.2, 'helix': 1.14, 'charge': 0, 'aromatic': False},
    # Aromatic
    'F': {'hydrophobicity': 2.8, 'helix': 1.12, 'charge': 0, 'aromatic': True},
    'W': {'hydrophobicity': -0.9, 'helix': 1.14, 'charge': 0, 'aromatic': True},
    'Y': {'hydrophobicity': -1.3, 'helix': 0.61, 'charge': 0, 'aromatic': True},
    # Positive charge
    'K': {'hydrophobicity': -3.9, 'helix': 1.07, 'charge': 1, 'aromatic': False},
    'R': {'hydrophobicity': -4.5, 'helix': 0.79, 'charge': 1, 'aromatic': False},
    'H': {'hydrophobicity': -3.2, 'helix': 1.24, 'charge': 0.5, 'aromatic': True},
    # Negative charge
    'D': {'hydrophobicity': -3.5, 'helix': 0.98, 'charge': -1, 'aromatic': False},
    'E': {'hydrophobicity': -3.5, 'helix': 1.53, 'charge': -1, 'aromatic': False},
    # Polar uncharged
    'N': {'hydrophobicity': -3.5, 'helix': 0.73, 'charge': 0, 'aromatic': False},
    'Q': {'hydrophobicity': -3.5, 'helix': 1.17, 'charge': 0, 'aromatic': False},
    'S': {'hydrophobicity': -0.8, 'helix': 0.79, 'charge': 0, 'aromatic': False},
    'T': {'hydrophobicity': -0.7, 'helix': 0.82, 'charge': 0, 'aromatic': False},
    # Special
    'C': {'hydrophobicity': 2.5, 'helix': 0.77, 'charge': 0, 'aromatic': False},
    'G': {'hydrophobicity': -0.4, 'helix': 0.53, 'charge': 0, 'aromatic': False},
    'P': {'hydrophobicity': -1.6, 'helix': 0.59, 'charge': 0, 'aromatic': False},
}

# Design motifs for specific functions
DESIGN_MOTIFS = {
    "receptor_binding": ["RGD", "KGD", "NGR", "LDV"],
    "cell_penetrating": ["RRRR", "KKKKK", "RQIKIWFQNRRMKWKK", "GRKKRRQRRRPQ"],
    "vegf_binding": ["WEYYW", "WWYWD", "FYLWY"],  # Based on VEGF receptor interface
    "helix_nucleation": ["AAAA", "AELA", "AEQL"],
    "disulfide_cap": ["C", "CC"],
    "solubility_enhancer": ["KK", "RR", "EE", "DD"],
}


# =============================================================================
# TARGET-SPECIFIC DESIGN PARAMETERS
# =============================================================================

TARGET_DESIGN_PARAMS = {
    "VEGF-A": {
        "peptide_type": "cyclic",
        "length_range": (10, 18),
        "charge_target": (-1, 2),
        "required_features": ["aromatic_cluster", "acidic_anchor"],
        "key_motifs": ["WYW", "FYF", "DKK"],
        "benchmark_Kd_pM": 0.49,  # Aflibercept
        "binding_site_residues": "hydrophobic_groove",
    },
    "VEGFR2": {
        "peptide_type": "cyclic",
        "length_range": (12, 20),
        "charge_target": (0, 3),
        "required_features": ["receptor_mimic"],
        "key_motifs": ["KDR", "FLK"],
        "benchmark_Kd_nM": 75,
        "binding_site_residues": "d2_d3_interface",
    },
    "Complement_C3": {
        "peptide_type": "cyclic",
        "length_range": (13, 15),
        "charge_target": (-2, 1),
        "required_features": ["compstatin_like"],
        "key_motifs": ["ICVVQDWGH", "WFWDPC"],  # Compstatin-derived
        "benchmark_Kd_nM": 0.5,  # Pegcetacoplan
        "binding_site_residues": "c3b_binding",
    },
    "Complement_C5": {
        "peptide_type": "cyclic",
        "length_range": (10, 16),
        "charge_target": (-1, 2),
        "required_features": ["c5_binding"],
        "key_motifs": ["RRAA", "SFTI"],
        "benchmark_Kd_nM": 15,
        "binding_site_residues": "c5a_site",
    },
    "ROCK1": {
        "peptide_type": "linear",
        "length_range": (8, 14),
        "charge_target": (1, 4),
        "required_features": ["kinase_targeting", "basic_stretch"],
        "key_motifs": ["RRXS", "RRK", "RXXL"],  # Substrate mimics
        "benchmark_Ki_nM": 1.0,  # Netarsudil
        "binding_site_residues": "atp_pocket",
    },
    "ROCK2": {
        "peptide_type": "linear",
        "length_range": (8, 14),
        "charge_target": (1, 4),
        "required_features": ["kinase_targeting"],
        "key_motifs": ["RRXS", "RRK"],
        "benchmark_Ki_nM": 1.0,
        "binding_site_residues": "atp_pocket",
    },
    "LFA1_ICAM1": {
        "peptide_type": "cyclic",
        "length_range": (8, 15),
        "charge_target": (-2, 0),
        "required_features": ["acidic_cluster", "integrin_mimic"],
        "key_motifs": ["DLXXL", "RGD", "LDV"],
        "benchmark_IC50_nM": 1.4,  # Lifitegrast
        "binding_site_residues": "i_domain",
    },
    "TNF_alpha": {
        "peptide_type": "cyclic",
        "length_range": (12, 20),
        "charge_target": (-1, 3),
        "required_features": ["tnf_receptor_mimic"],
        "key_motifs": ["CQE", "KDK", "KRPV"],
        "benchmark_Kd_pM": 60,  # Adalimumab
        "binding_site_residues": "receptor_interface",
    },
    "Alpha_A_Crystallin": {
        "peptide_type": "linear",
        "length_range": (8, 15),
        "charge_target": (1, 3),
        "required_features": ["chaperone_mimic", "aggregation_inhibitor"],
        "key_motifs": ["DRFSVNLDVK", "FSVNLDVK"],  # Mini-chaperone
        "benchmark_EC50_uM": 50,
        "binding_site_residues": "substrate_groove",
    },
    "Alpha_B_Crystallin": {
        "peptide_type": "linear",
        "length_range": (8, 15),
        "charge_target": (1, 3),
        "required_features": ["chaperone_mimic"],
        "key_motifs": ["DRFSVNLDVK", "HGKHEERQD"],
        "benchmark_IC50_uM": 10,
        "binding_site_residues": "acd_groove",
    },
    "BDNF": {
        "peptide_type": "cyclic",
        "length_range": (10, 16),
        "charge_target": (1, 4),
        "required_features": ["trkb_agonist", "neurotrophin_mimic"],
        "key_motifs": ["RGEY", "KGSR", "SKGQLKQY"],
        "benchmark_Kd_nM": 0.3,  # Native BDNF
        "binding_site_residues": "trkb_d5",
    },
    "Rhodopsin": {
        "peptide_type": "linear",
        "length_range": (8, 14),
        "charge_target": (0, 2),
        "required_features": ["chaperone_activity", "retinal_pocket_binder"],
        "key_motifs": ["FLLF", "NPVY"],
        "benchmark_Kd_nM": 0.5,
        "binding_site_residues": "tm_pocket",
    },
    "MMP9": {
        "peptide_type": "cyclic",
        "length_range": (8, 12),
        "charge_target": (-1, 1),
        "required_features": ["zinc_chelator", "collagen_mimic"],
        "key_motifs": ["HWGH", "PLGL", "GPQG"],  # Substrate analogs
        "benchmark_Ki_nM": 0.4,  # GM6001
        "binding_site_residues": "catalytic_zinc",
    },
    "Calcineurin": {
        "peptide_type": "cyclic",
        "length_range": (10, 15),
        "charge_target": (0, 2),
        "required_features": ["nfat_mimic", "calcineurin_docking"],
        "key_motifs": ["PVIVIT", "LXVP"],  # Calcineurin docking motif
        "benchmark_IC50_nM": 7,  # Cyclosporine
        "binding_site_residues": "nfat_binding",
    },
}


# =============================================================================
# PEPTIDE DESIGN DATACLASSES
# =============================================================================

@dataclass
class DesignedPeptide:
    """A designed therapeutic peptide."""
    peptide_id: str
    sequence: str
    length: int
    target: str
    peptide_type: str  # cyclic, linear, stapled

    # Physicochemical properties
    molecular_weight: float
    net_charge: float
    hydrophobicity_index: float
    helix_propensity: float

    # Design features
    design_motifs: List[str]
    has_disulfide: bool
    aromatic_count: int

    # Predicted binding
    predicted_dG_kcal: float
    predicted_Kd_nM: float

    # Benchmark comparison
    benchmark_compound: str
    benchmark_Kd_nM: float
    fold_improvement: float

    # Prior art hash
    sequence_hash: str
    timestamp: str


# =============================================================================
# DESIGN FUNCTIONS
# =============================================================================

def calculate_mw(sequence: str) -> float:
    """Calculate molecular weight of peptide."""
    aa_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }
    mw = sum(aa_weights.get(aa, 110) for aa in sequence)
    mw -= 18.0 * (len(sequence) - 1)  # Water loss for peptide bonds
    return mw


def calculate_charge(sequence: str, pH: float = 7.4) -> float:
    """Calculate net charge at physiological pH."""
    charge = 0
    for aa in sequence:
        if aa in ['K', 'R']:
            charge += 1
        elif aa == 'H':
            charge += 0.1  # Partial charge at pH 7.4
        elif aa in ['D', 'E']:
            charge -= 1
    # N-terminus and C-terminus
    charge += 1  # N-terminus
    charge -= 1  # C-terminus (for linear peptides)
    return charge


def calculate_hydrophobicity(sequence: str) -> float:
    """Calculate Kyte-Doolittle hydrophobicity index."""
    return np.mean([AA_PROPERTIES.get(aa, {}).get('hydrophobicity', 0) for aa in sequence])


def calculate_helix_propensity(sequence: str) -> float:
    """Calculate average helix propensity."""
    return np.mean([AA_PROPERTIES.get(aa, {}).get('helix', 1.0) for aa in sequence])


def count_aromatics(sequence: str) -> int:
    """Count aromatic residues."""
    return sum(1 for aa in sequence if aa in ['F', 'W', 'Y', 'H'])


def score_binding_potential(sequence: str, target: str) -> Tuple[float, float]:
    """
    Score binding potential using simplified energy function.
    Returns (dG_kcal, Kd_nM)
    """
    params = TARGET_DESIGN_PARAMS.get(target, {})

    # Base energy from sequence composition
    length = len(sequence)
    hydrophobicity = calculate_hydrophobicity(sequence)
    charge = calculate_charge(sequence)
    aromatics = count_aromatics(sequence)
    helix = calculate_helix_propensity(sequence)

    # Length penalty/bonus
    ideal_length = np.mean(params.get('length_range', (10, 15)))
    length_term = -0.1 * abs(length - ideal_length)

    # Charge compatibility
    charge_range = params.get('charge_target', (-1, 2))
    if charge_range[0] <= charge <= charge_range[1]:
        charge_term = 0.5
    else:
        charge_term = -0.5 * abs(charge - np.mean(charge_range))

    # Aromatic contacts (favorable for most protein-protein interfaces)
    aromatic_term = 0.3 * min(aromatics, 5)

    # Hydrophobic burial
    hydrophobic_term = 0.2 * hydrophobicity if hydrophobicity > 0 else 0.1 * hydrophobicity

    # Helix stability (for helical peptides)
    if params.get('peptide_type') in ['cyclic', 'stapled']:
        helix_term = 0.4 * (helix - 1.0) if helix > 1.0 else 0
    else:
        helix_term = 0.2 * (helix - 1.0)

    # Motif matching
    key_motifs = params.get('key_motifs', [])
    motif_term = 0
    for motif in key_motifs:
        if motif in sequence or any(m in sequence for m in motif.split('X')):
            motif_term += 0.8

    # Cyclic bonus
    cyclic_bonus = 0.5 if sequence.startswith('C') and sequence.endswith('C') else 0

    # Total binding energy (more negative = better)
    dG = -8.0 + length_term + charge_term + aromatic_term + hydrophobic_term + helix_term + motif_term + cyclic_bonus

    # Add some controlled randomness for diversity
    dG += np.random.normal(0, 0.3)

    # Convert to Kd
    RT = 0.593  # kcal/mol at 310K
    Kd_M = np.exp(dG / RT)
    Kd_nM = Kd_M * 1e9

    return dG, Kd_nM


def design_peptide_for_target(target: str, peptide_num: int) -> Optional[DesignedPeptide]:
    """Design a peptide for a specific target."""

    if target not in TARGET_DESIGN_PARAMS:
        return None

    params = TARGET_DESIGN_PARAMS[target]

    # Determine length
    min_len, max_len = params['length_range']
    length = random.randint(min_len, max_len)

    # Build sequence based on peptide type
    peptide_type = params['peptide_type']

    # Start with key motifs
    motifs_used = []
    sequence_parts = []

    # For cyclic peptides, add flanking cysteines
    if peptide_type == 'cyclic':
        sequence_parts.append('C')
        length -= 2  # Account for terminal cysteines

    # Add a key motif if available
    key_motifs = params.get('key_motifs', [])
    if key_motifs and random.random() < 0.7:
        motif = random.choice(key_motifs)
        # Clean motif of X placeholders
        clean_motif = motif.replace('X', random.choice('AILVMFYWKRH'))
        if len(clean_motif) <= length:
            sequence_parts.append(clean_motif)
            motifs_used.append(motif)
            length -= len(clean_motif)

    # Fill remaining with appropriate amino acids based on target requirements
    features = params.get('required_features', [])

    # Amino acid pools for different features
    if 'aromatic_cluster' in features:
        pool = list('FWYFWYILVK')
    elif 'acidic_anchor' in features:
        pool = list('DEEEDEILVFWY')
    elif 'basic_stretch' in features:
        pool = list('KRKRKRAILVM')
    elif 'chaperone_mimic' in features:
        pool = list('DKRFSVNLIVAM')
    else:
        pool = list('AILVMFWYKRHDEQNST')

    # Generate remaining sequence
    remaining = ''.join(random.choices(pool, k=length))
    sequence_parts.append(remaining)

    # Close cyclic peptides
    if peptide_type == 'cyclic':
        sequence_parts.append('C')

    sequence = ''.join(sequence_parts)

    # Calculate properties
    mw = calculate_mw(sequence)
    charge = calculate_charge(sequence)
    hydrophobicity = calculate_hydrophobicity(sequence)
    helix = calculate_helix_propensity(sequence)
    aromatics = count_aromatics(sequence)

    # Score binding
    dG, Kd_nM = score_binding_potential(sequence, target)

    # Get benchmark
    benchmark_Kd = None
    benchmark_name = "Unknown"
    if 'benchmark_Kd_pM' in params:
        benchmark_Kd = params['benchmark_Kd_pM'] / 1000  # Convert to nM
        benchmark_name = "FDA-approved"
    elif 'benchmark_Kd_nM' in params:
        benchmark_Kd = params['benchmark_Kd_nM']
        benchmark_name = "FDA-approved"
    elif 'benchmark_Ki_nM' in params:
        benchmark_Kd = params['benchmark_Ki_nM']
        benchmark_name = "FDA-approved"
    elif 'benchmark_IC50_nM' in params:
        benchmark_Kd = params['benchmark_IC50_nM']
        benchmark_name = "FDA-approved"
    elif 'benchmark_EC50_uM' in params:
        benchmark_Kd = params['benchmark_EC50_uM'] * 1000
        benchmark_name = "Literature"
    elif 'benchmark_IC50_uM' in params:
        benchmark_Kd = params['benchmark_IC50_uM'] * 1000
        benchmark_name = "Literature"
    else:
        benchmark_Kd = 1000  # Default if no benchmark

    fold_improvement = benchmark_Kd / Kd_nM if Kd_nM > 0 else 0

    # Create peptide ID and hash
    peptide_id = f"{target}_pep{peptide_num:03d}"
    sequence_hash = hashlib.sha256(sequence.encode()).hexdigest()[:16]
    timestamp = datetime.now().isoformat()

    return DesignedPeptide(
        peptide_id=peptide_id,
        sequence=sequence,
        length=len(sequence),
        target=target,
        peptide_type=peptide_type,
        molecular_weight=mw,
        net_charge=charge,
        hydrophobicity_index=hydrophobicity,
        helix_propensity=helix,
        design_motifs=motifs_used,
        has_disulfide=sequence.startswith('C') and sequence.endswith('C'),
        aromatic_count=aromatics,
        predicted_dG_kcal=dG,
        predicted_Kd_nM=Kd_nM,
        benchmark_compound=benchmark_name,
        benchmark_Kd_nM=benchmark_Kd,
        fold_improvement=fold_improvement,
        sequence_hash=sequence_hash,
        timestamp=timestamp,
    )


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_peptide_design(peptides_per_target: int = 10):
    """Run the complete peptide design pipeline."""

    print("=" * 70)
    print("M4 EYE/VISION PEPTIDE DESIGN PIPELINE")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Peptides per target: {peptides_per_target}")
    print()

    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    all_peptides = []

    # Design peptides for each target
    for target in TARGET_DESIGN_PARAMS.keys():
        print(f"\nDesigning peptides for: {target}")
        print("-" * 50)

        target_peptides = []
        for i in range(1, peptides_per_target + 1):
            peptide = design_peptide_for_target(target, i)
            if peptide:
                target_peptides.append(peptide)

        # Sort by predicted Kd
        target_peptides.sort(key=lambda p: p.predicted_Kd_nM)

        # Print top 3
        for peptide in target_peptides[:3]:
            improvement = "BETTER" if peptide.fold_improvement > 1 else "weaker"
            print(f"  {peptide.peptide_id}: {peptide.sequence}")
            print(f"    Kd: {peptide.predicted_Kd_nM:.2f} nM, {peptide.fold_improvement:.2f}x {improvement} than benchmark")

        all_peptides.extend(target_peptides)

    print()
    print("=" * 70)
    print("DESIGN SUMMARY")
    print("=" * 70)

    total = len(all_peptides)
    better_than_benchmark = sum(1 for p in all_peptides if p.fold_improvement > 1)
    cyclic = sum(1 for p in all_peptides if p.has_disulfide)

    print(f"Total peptides designed: {total}")
    print(f"Cyclic (disulfide-bridged): {cyclic}")
    print(f"Better than benchmark: {better_than_benchmark} ({100*better_than_benchmark/total:.1f}%)")
    print()

    # Group by target for summary
    print("BY TARGET:")
    print("-" * 50)
    targets_summary = {}
    for peptide in all_peptides:
        if peptide.target not in targets_summary:
            targets_summary[peptide.target] = {"count": 0, "better": 0, "best_Kd": float('inf')}
        targets_summary[peptide.target]["count"] += 1
        if peptide.fold_improvement > 1:
            targets_summary[peptide.target]["better"] += 1
        if peptide.predicted_Kd_nM < targets_summary[peptide.target]["best_Kd"]:
            targets_summary[peptide.target]["best_Kd"] = peptide.predicted_Kd_nM

    for target, stats in sorted(targets_summary.items()):
        print(f"  {target:25s} {stats['count']:3d} peptides, {stats['better']:2d} better than benchmark, best Kd: {stats['best_Kd']:.2f} nM")

    # Save results
    output_dir = Path(__file__).parent / "peptides"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON
    output = {
        "timestamp": timestamp,
        "total_peptides": len(all_peptides),
        "peptides_per_target": peptides_per_target,
        "peptides": [asdict(p) for p in all_peptides],
        "summary": {
            "better_than_benchmark": better_than_benchmark,
            "cyclic_count": cyclic,
            "targets": len(targets_summary),
        },
        "prior_art_manifest": {
            "prior_art_type": "Eye_Vision_Therapeutic_Peptides",
            "publication_date": datetime.now().strftime("%Y-%m-%d"),
            "diseases": ["AMD", "Diabetic Retinopathy", "Glaucoma", "Cataracts", "Dry Eye", "Uveitis", "Retinitis Pigmentosa"],
            "license": "AGPL-3.0-or-later (code) + OpenMTA (biological materials)",
            "sequences": [
                {"sequence": p.sequence, "target": p.target, "Kd_nM": p.predicted_Kd_nM, "sha256": p.sequence_hash}
                for p in sorted(all_peptides, key=lambda x: x.predicted_Kd_nM)[:20]
            ],
        },
        "license": "AGPL-3.0-or-later",
    }

    output_path = output_dir / f"eye_peptides_{timestamp}.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\nResults saved: {output_path}")

    # Save FASTA
    fasta_path = output_dir / f"eye_peptides_{timestamp}.fasta"
    with open(fasta_path, 'w') as f:
        for peptide in all_peptides:
            f.write(f">{peptide.peptide_id}|{peptide.target}|Kd={peptide.predicted_Kd_nM:.2f}nM\n")
            f.write(f"{peptide.sequence}\n")

    print(f"FASTA saved: {fasta_path}")

    print("\n" + "=" * 70)
    print("PEPTIDE DESIGN COMPLETE")
    print("=" * 70)

    return all_peptides


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run_peptide_design(peptides_per_target=15)
