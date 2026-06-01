#!/usr/bin/env python3
"""
M4 Antivirulence Peptide Designer

Designs peptides that geometrically stabilize bacterial virulence factors without killing
the bacteria. This reduces selective pressure for resistance development.

Design Strategies:
1. Active Site Blockers - Competitive inhibitors for enzyme targets
2. Adhesin Disruptors - Block bacterial attachment
3. Cyclic Peptides - Enhanced stability in oral cavity

Key Targets:
- GtfC: Block glucan synthesis (S. mutans biofilm)
- RgpB: geometrically stabilize gingipain protease (P. gingivalis tissue damage)
- FadA: Disrupt adhesin function (F. nucleatum invasion)

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

import json
import hashlib
import os
import random
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import math

# ==============================================================================
# CONFIGURATION
# ==============================================================================

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "results", "designed_peptides")

# Amino acid properties
AA_PROPERTIES = {
    # Hydrophobic
    'A': {'charge': 0, 'hydrophobicity': 0.62, 'volume': 88.6, 'type': 'hydrophobic'},
    'V': {'charge': 0, 'hydrophobicity': 1.08, 'volume': 140.0, 'type': 'hydrophobic'},
    'L': {'charge': 0, 'hydrophobicity': 1.06, 'volume': 166.7, 'type': 'hydrophobic'},
    'I': {'charge': 0, 'hydrophobicity': 1.38, 'volume': 166.7, 'type': 'hydrophobic'},
    'M': {'charge': 0, 'hydrophobicity': 0.64, 'volume': 162.9, 'type': 'hydrophobic'},
    'F': {'charge': 0, 'hydrophobicity': 1.19, 'volume': 189.9, 'type': 'aromatic'},
    'W': {'charge': 0, 'hydrophobicity': 0.81, 'volume': 227.8, 'type': 'aromatic'},
    'Y': {'charge': 0, 'hydrophobicity': 0.26, 'volume': 193.6, 'type': 'aromatic'},
    'P': {'charge': 0, 'hydrophobicity': 0.12, 'volume': 112.7, 'type': 'special'},

    # Polar uncharged
    'S': {'charge': 0, 'hydrophobicity': -0.18, 'volume': 89.0, 'type': 'polar'},
    'T': {'charge': 0, 'hydrophobicity': -0.05, 'volume': 116.1, 'type': 'polar'},
    'N': {'charge': 0, 'hydrophobicity': -0.78, 'volume': 114.1, 'type': 'polar'},
    'Q': {'charge': 0, 'hydrophobicity': -0.85, 'volume': 143.8, 'type': 'polar'},
    'G': {'charge': 0, 'hydrophobicity': 0.48, 'volume': 60.1, 'type': 'special'},
    'C': {'charge': 0, 'hydrophobicity': 0.29, 'volume': 108.5, 'type': 'special'},

    # Charged
    'K': {'charge': 1, 'hydrophobicity': -1.50, 'volume': 168.6, 'type': 'basic'},
    'R': {'charge': 1, 'hydrophobicity': -2.53, 'volume': 173.4, 'type': 'basic'},
    'H': {'charge': 0.5, 'hydrophobicity': -0.40, 'volume': 153.2, 'type': 'basic'},
    'D': {'charge': -1, 'hydrophobicity': -0.90, 'volume': 111.1, 'type': 'acidic'},
    'E': {'charge': -1, 'hydrophobicity': -0.74, 'volume': 138.4, 'type': 'acidic'},
}

# Design templates for different target types
DESIGN_TEMPLATES = {
    "enzyme_inhibitor": {
        "length_range": (8, 15),
        "net_charge_range": (0, 2),
        "hydrophobic_fraction": (0.3, 0.5),
        "cyclization": True,
        "d_amino_acids": False,
    },
    "adhesin_blocker": {
        "length_range": (10, 18),
        "net_charge_range": (-1, 1),
        "hydrophobic_fraction": (0.4, 0.6),
        "cyclization": False,
        "d_amino_acids": True,  # For protease resistance
    },
    "protease_inhibitor": {
        "length_range": (6, 12),
        "net_charge_range": (1, 3),
        "hydrophobic_fraction": (0.2, 0.4),
        "cyclization": True,
        "d_amino_acids": False,
    },
}

# Target-specific design parameters
TARGET_PARAMETERS = {
    "GtfC_S_mutans": {
        "template": "enzyme_inhibitor",
        "key_motifs": ["DXE", "WXH"],  # Catalytic site interactions
        "anchor_residues": ["R", "K"],  # For Asp477 interaction
        "aromatic_positions": [3, 7],  # For Trp517, Phe433 stacking
        "avoid_residues": ["M", "C"],  # Oxidation-sensitive
    },
    "RgpB_P_gingivalis": {
        "template": "protease_inhibitor",
        "key_motifs": ["RXR", "KXK"],  # Arg-specific protease
        "anchor_residues": ["R"],  # Substrate mimetic
        "aromatic_positions": [2, 5],  # For Trp284 interaction
        "avoid_residues": ["R"],  # Would be cleaved at P1 position
        "warhead": "aldehyde",  # Cys protease inhibitor
    },
    "FadA_F_nucleatum": {
        "template": "adhesin_blocker",
        "key_motifs": ["LXXL"],  # Leucine zipper mimetic
        "anchor_residues": ["L", "I", "V"],  # Hydrophobic interface
        "aromatic_positions": [],  # Coiled-coil target
        "avoid_residues": ["P"],  # Would break helix
    },
    "SrtA_S_mutans": {
        "template": "enzyme_inhibitor",
        "key_motifs": ["LPXTG"],  # Sortase recognition motif
        "anchor_residues": ["L", "P"],  # Substrate mimetic
        "aromatic_positions": [1, 5],
        "avoid_residues": [],
    },
}


# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class DesignedPeptide:
    """Represents a designed antivirulence peptide."""
    peptide_id: str
    target_id: str
    sequence: str
    length: int

    # Properties
    net_charge: float
    hydrophobicity: float
    hydrophobic_fraction: float
    molecular_weight: float

    # Design features
    cyclization: str  # "head-to-tail", "disulfide", "none"
    d_amino_acids: List[int]  # Positions with D-amino acids
    warhead: Optional[str]  # Chemical warhead for covalent inhibitors

    # Predicted metrics
    binding_score: float
    selectivity_score: float
    stability_score: float
    overall_score: float

    # Metadata
    design_rationale: str
    timestamp: str
    sha256_hash: str


# ==============================================================================
# PEPTIDE DESIGN ENGINE
# ==============================================================================

def calculate_net_charge(sequence: str, ph: float = 7.0) -> float:
    """Calculate net charge at given pH."""
    charge = 0.0
    for aa in sequence:
        if aa in AA_PROPERTIES:
            charge += AA_PROPERTIES[aa]['charge']

    # pH adjustment for histidine
    his_count = sequence.count('H')
    if ph < 6.0:
        charge += his_count * 0.5  # More protonated at low pH

    return charge


def calculate_hydrophobicity(sequence: str) -> float:
    """Calculate average hydrophobicity (Eisenberg scale)."""
    if not sequence:
        return 0.0
    total = sum(AA_PROPERTIES.get(aa, {}).get('hydrophobicity', 0) for aa in sequence)
    return total / len(sequence)


def calculate_hydrophobic_fraction(sequence: str) -> float:
    """Calculate fraction of hydrophobic residues."""
    if not sequence:
        return 0.0
    hydrophobic = sum(1 for aa in sequence
                      if AA_PROPERTIES.get(aa, {}).get('type') in ['hydrophobic', 'aromatic'])
    return hydrophobic / len(sequence)


def calculate_molecular_weight(sequence: str) -> float:
    """Calculate approximate molecular weight."""
    # Average MW per residue ~ 110 Da, minus water for each peptide bond
    return len(sequence) * 110 - (len(sequence) - 1) * 18


def score_binding(sequence: str, target_params: Dict) -> float:
    """Score predicted binding affinity based on design rules."""
    score = 0.5  # Baseline

    # Check for key motifs
    for motif in target_params.get("key_motifs", []):
        # Convert motif pattern (X = any) to check
        motif_check = motif.replace("X", ".")
        import re
        if re.search(motif_check, sequence):
            score += 0.1

    # Check anchor residues
    anchor_residues = target_params.get("anchor_residues", [])
    anchor_count = sum(1 for aa in sequence if aa in anchor_residues)
    score += min(0.2, anchor_count * 0.05)

    # Check aromatic positions
    aromatic_positions = target_params.get("aromatic_positions", [])
    for pos in aromatic_positions:
        if pos < len(sequence) and sequence[pos] in "FWY":
            score += 0.05

    # Penalize avoided residues
    for aa in target_params.get("avoid_residues", []):
        if aa in sequence:
            score -= 0.1

    return max(0.0, min(1.0, score))


def score_selectivity(sequence: str, target_id: str) -> float:
    """
    Score selectivity for target system vs commensal bacteria.

    Higher scores indicate better selectivity.
    """
    score = 0.7  # Default assumption of reasonable selectivity

    # GtfC is highly specific to cariogenic streptococci
    if "GtfC" in target_id:
        score = 0.85

    # RgpB is unique to P. gingivalis
    if "RgpB" in target_id:
        score = 0.90

    # FadA is specific to F. nucleatum
    if "FadA" in target_id:
        score = 0.80

    # Sortases are widespread - lower selectivity
    if "SrtA" in target_id:
        score = 0.60

    return score


def score_stability(sequence: str, cyclization: str, d_amino_acids: List[int]) -> float:
    """Score predicted stability in oral cavity."""
    score = 0.5  # Baseline

    # Cyclization improves stability
    if cyclization != "none":
        score += 0.2

    # D-amino acids improve protease resistance
    d_fraction = len(d_amino_acids) / len(sequence) if sequence else 0
    score += d_fraction * 0.3

    # Penalize oxidation-sensitive residues
    ox_sensitive = sequence.count('M') + sequence.count('C')
    score -= ox_sensitive * 0.05

    # Penalize protease-sensitive sequences
    # Trypsin cuts after K/R
    trypsin_sites = sequence.count('K') + sequence.count('R')
    score -= trypsin_sites * 0.02

    return max(0.0, min(1.0, score))


def generate_candidate_sequence(target_id: str, target_params: Dict,
                                 template: Dict, seed: int) -> str:
    """Generate a candidate peptide sequence."""
    random.seed(seed)

    length = random.randint(*template["length_range"])
    target_charge = random.uniform(*template["net_charge_range"])
    target_hydrophobic = random.uniform(*template["hydrophobic_fraction"])

    # Build sequence
    sequence = []

    # Start with anchor residues
    anchor_residues = target_params.get("anchor_residues", ["A"])
    sequence.append(random.choice(anchor_residues))

    # Fill remaining positions
    for i in range(1, length):
        # Check if this should be an aromatic position
        if i in target_params.get("aromatic_positions", []):
            sequence.append(random.choice(["F", "W", "Y"]))
        elif random.random() < target_hydrophobic:
            # Hydrophobic residue
            hydrophobic = [aa for aa, props in AA_PROPERTIES.items()
                          if props['type'] in ['hydrophobic', 'aromatic']
                          and aa not in target_params.get("avoid_residues", [])]
            sequence.append(random.choice(hydrophobic))
        else:
            # Polar/charged residue (adjust for target charge)
            current_charge = calculate_net_charge("".join(sequence))
            if current_charge < target_charge:
                charged = [aa for aa, props in AA_PROPERTIES.items()
                          if props['charge'] > 0]
                sequence.append(random.choice(charged))
            elif current_charge > target_charge:
                charged = [aa for aa, props in AA_PROPERTIES.items()
                          if props['charge'] < 0]
                sequence.append(random.choice(charged))
            else:
                polar = [aa for aa, props in AA_PROPERTIES.items()
                        if props['type'] == 'polar']
                sequence.append(random.choice(polar))

    return "".join(sequence)


def design_peptides_for_target(target_id: str, n_candidates: int = 10) -> List[DesignedPeptide]:
    """Design peptides for a specific target."""

    if target_id not in TARGET_PARAMETERS:
        print(f"Warning: No parameters for {target_id}, using defaults")
        target_params = TARGET_PARAMETERS.get("GtfC_S_mutans")  # Default
    else:
        target_params = TARGET_PARAMETERS[target_id]

    template_name = target_params.get("template", "enzyme_inhibitor")
    template = DESIGN_TEMPLATES[template_name]

    peptides = []

    for i in range(n_candidates):
        # Generate candidate sequence
        sequence = generate_candidate_sequence(target_id, target_params, template, seed=i*1000+hash(target_id))

        # Determine cyclization
        if template["cyclization"]:
            # Add cysteines for disulfide if needed
            if "C" not in sequence:
                sequence = "C" + sequence[1:-1] + "C"
            cyclization = "disulfide"
        else:
            cyclization = "none"

        # Determine D-amino acid positions
        if template["d_amino_acids"]:
            # Place D-amino acids at protease-sensitive sites
            d_positions = [j for j, aa in enumerate(sequence) if aa in "KR"][:2]
        else:
            d_positions = []

        # Calculate properties
        net_charge = calculate_net_charge(sequence)
        hydrophobicity = calculate_hydrophobicity(sequence)
        hydrophobic_fraction = calculate_hydrophobic_fraction(sequence)
        mw = calculate_molecular_weight(sequence)

        # Score
        binding_score = score_binding(sequence, target_params)
        selectivity_score = score_selectivity(sequence, target_id)
        stability_score = score_stability(sequence, cyclization, d_positions)

        # Overall score (weighted average)
        overall_score = (
            0.4 * binding_score +
            0.35 * selectivity_score +
            0.25 * stability_score
        )

        # Design rationale
        rationale = f"Designed for {target_id} using {template_name} template. "
        if cyclization != "none":
            rationale += f"Cyclized via {cyclization} for stability. "
        if d_positions:
            rationale += f"D-amino acids at positions {d_positions} for protease resistance. "

        # Create peptide object
        peptide_id = f"{target_id}_pep{i+1:03d}"

        peptide = DesignedPeptide(
            peptide_id=peptide_id,
            target_id=target_id,
            sequence=sequence,
            length=len(sequence),
            net_charge=net_charge,
            hydrophobicity=hydrophobicity,
            hydrophobic_fraction=hydrophobic_fraction,
            molecular_weight=mw,
            cyclization=cyclization,
            d_amino_acids=d_positions,
            warhead=target_params.get("warhead"),
            binding_score=binding_score,
            selectivity_score=selectivity_score,
            stability_score=stability_score,
            overall_score=overall_score,
            design_rationale=rationale,
            timestamp=datetime.now().isoformat(),
            sha256_hash=""
        )

        # Compute hash for prior art
        peptide_str = json.dumps(asdict(peptide), sort_keys=True, default=str)
        peptide.sha256_hash = hashlib.sha256(peptide_str.encode()).hexdigest()

        peptides.append(peptide)

    # Sort by overall score
    peptides.sort(key=lambda x: x.overall_score, reverse=True)

    return peptides


# ==============================================================================
# MAIN DESIGN WORKFLOW
# ==============================================================================

def run_design_pipeline(targets: List[str] = None, n_per_target: int = 10) -> Dict:
    """Run the full peptide design pipeline."""

    if targets is None:
        targets = list(TARGET_PARAMETERS.keys())

    print("="*70)
    print("M4 ANTIVIRULENCE PEPTIDE DESIGNER")
    print("="*70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Targets: {len(targets)}")
    print(f"Candidates per target: {n_per_target}")
    print("="*70)

    all_peptides = {}
    total_designed = 0

    for target_id in targets:
        print(f"\nDesigning for: {target_id}")

        peptides = design_peptides_for_target(target_id, n_per_target)
        all_peptides[target_id] = peptides
        total_designed += len(peptides)

        # Print top 3
        print(f"  Top candidates:")
        for p in peptides[:3]:
            print(f"    {p.sequence} (score: {p.overall_score:.3f})")

    print("\n" + "="*70)
    print(f"Total peptides designed: {total_designed}")
    print("="*70)

    return all_peptides


def save_results(all_peptides: Dict) -> str:
    """Save design results to files."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON with all data
    output_data = {
        "pipeline": "M4 Antivirulence Peptide Designer",
        "version": "1.0.0",
        "license": "AGPL-3.0-or-later",
        "timestamp": datetime.now().isoformat(),
        "targets": {},
        "prior_art_manifest": {}
    }

    for target_id, peptides in all_peptides.items():
        output_data["targets"][target_id] = {
            "n_designed": len(peptides),
            "peptides": [asdict(p) for p in peptides]
        }

        # Prior art hashes
        for p in peptides:
            output_data["prior_art_manifest"][p.peptide_id] = {
                "sequence": p.sequence,
                "sha256": p.sha256_hash
            }

    json_path = os.path.join(OUTPUT_DIR, f"designed_peptides_{timestamp}.json")
    with open(json_path, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    # Save FASTA files per target
    for target_id, peptides in all_peptides.items():
        fasta_path = os.path.join(OUTPUT_DIR, f"{target_id}_peptides.fasta")
        with open(fasta_path, 'w') as f:
            for p in peptides:
                f.write(f">{p.peptide_id} score={p.overall_score:.3f} charge={p.net_charge:.1f}\n")
                f.write(f"{p.sequence}\n")

    print(f"\nResults saved to: {OUTPUT_DIR}")
    print(f"  JSON: designed_peptides_{timestamp}.json")
    print(f"  FASTA: *_peptides.fasta (one per target)")

    return json_path


def print_summary(all_peptides: Dict):
    """Print design summary."""

    print("\n" + "="*70)
    print("DESIGN SUMMARY")
    print("="*70)

    for target_id, peptides in all_peptides.items():
        print(f"\n{target_id}:")
        print(f"  Designed: {len(peptides)} peptides")
        print(f"  Top candidate: {peptides[0].sequence}")
        print(f"  Score: {peptides[0].overall_score:.3f}")
        print(f"    - Binding: {peptides[0].binding_score:.3f}")
        print(f"    - Selectivity: {peptides[0].selectivity_score:.3f}")
        print(f"    - Stability: {peptides[0].stability_score:.3f}")

    # Overall best
    all_flat = [p for peptides in all_peptides.values() for p in peptides]
    best = max(all_flat, key=lambda x: x.overall_score)

    print("\n" + "-"*70)
    print("OVERALL BEST CANDIDATE")
    print("-"*70)
    print(f"  Target: {best.target_id}")
    print(f"  Sequence: {best.sequence}")
    print(f"  Length: {best.length} aa")
    print(f"  MW: {best.molecular_weight:.1f} Da")
    print(f"  Charge: {best.net_charge:.1f}")
    print(f"  Cyclization: {best.cyclization}")
    print(f"  Score: {best.overall_score:.3f}")
    print(f"  SHA256: {best.sha256_hash}")
    print(f"  Rationale: {best.design_rationale}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point."""

    # Run design for all targets
    all_peptides = run_design_pipeline(n_per_target=10)

    # Print summary
    print_summary(all_peptides)

    # Save results
    save_results(all_peptides)

    print("\nDesign complete.")

    return all_peptides


if __name__ == "__main__":
    main()
