#!/usr/bin/env python3
"""
m04c_hybrid_design.py - Hybrid Peptide Design (Binding + Stability)

LESSON LEARNED:
- Compositional design (m04): High stability, low binding → useless marbles
- Pharmacophore design (m04b): High binding, low stability → unstable binders

SOLUTION: Combine both approaches:
1. Start with pharmacophore targeting (Z² = 6.02 Å geometry)
2. Filter/modify for stability constraints
3. Optimize for both properties simultaneously

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import warnings

try:
    from Bio.PDB import PDBParser, NeighborSearch
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False


# =============================================================================
# Z² AND STABILITY CONSTANTS
# =============================================================================

Z2_INTERACTION_DISTANCE = 6.015152508891966  # Å - precise: 5.788810036466141 × 1.0391 (310K expansion)

# Stability constraints (from compositional design lessons)
MAX_HYDROPHOBIC_FRACTION = 0.50  # Prevent aggregation
MIN_CHARGED_RESIDUES = 1  # Ensure solubility
MAX_CONSECUTIVE_HYDROPHOBIC = 3  # Prevent hydrophobic collapse

# Amino acid properties for stability scoring
AA_PROPERTIES = {
    'A': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 1.41, 'stability': 0.7},
    'C': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 0.77, 'stability': 0.5},
    'D': {'hydrophobic': False, 'charge': -1, 'helix_propensity': 0.99, 'stability': 0.8},
    'E': {'hydrophobic': False, 'charge': -1, 'helix_propensity': 1.59, 'stability': 0.9},
    'F': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 1.16, 'stability': 0.6},
    'G': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 0.43, 'stability': 0.5},
    'H': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 1.05, 'stability': 0.7},
    'I': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 1.09, 'stability': 0.6},
    'K': {'hydrophobic': False, 'charge': 1, 'helix_propensity': 1.23, 'stability': 0.9},
    'L': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 1.34, 'stability': 0.7},
    'M': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 1.30, 'stability': 0.6},
    'N': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 0.76, 'stability': 0.8},
    'P': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 0.34, 'stability': 0.4},
    'Q': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 1.27, 'stability': 0.8},
    'R': {'hydrophobic': False, 'charge': 1, 'helix_propensity': 1.21, 'stability': 0.9},
    'S': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 0.57, 'stability': 0.7},
    'T': {'hydrophobic': False, 'charge': 0, 'helix_propensity': 0.76, 'stability': 0.7},
    'V': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 0.90, 'stability': 0.6},
    'W': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 1.02, 'stability': 0.5},
    'Y': {'hydrophobic': True, 'charge': 0, 'helix_propensity': 0.74, 'stability': 0.6},
}

# Sidechain lengths for pharmacophore matching
SIDECHAIN_LENGTHS = {
    'A': 1.5, 'C': 2.8, 'D': 3.6, 'E': 4.9, 'F': 5.1,
    'G': 0.0, 'H': 4.5, 'I': 3.8, 'K': 6.3, 'L': 3.8,
    'M': 4.7, 'N': 3.5, 'P': 2.4, 'Q': 4.8, 'R': 7.3,
    'S': 2.4, 'T': 2.5, 'V': 2.6, 'W': 5.9, 'Y': 6.5
}

# Interaction types for pharmacophore matching
INTERACTION_TYPES = {
    'hbond_donor': ['R', 'K', 'N', 'Q', 'W', 'H', 'S', 'T', 'Y'],
    'hbond_acceptor': ['D', 'E', 'N', 'Q', 'S', 'T', 'Y'],
    'hydrophobic': ['F', 'W', 'Y', 'L', 'I', 'V', 'M', 'A'],
    'charged_pos': ['R', 'K'],
    'charged_neg': ['D', 'E'],
}


# =============================================================================
# HYBRID PEPTIDE DESIGN
# =============================================================================

@dataclass
class HybridCandidate:
    """A peptide designed with both binding and stability optimization."""
    peptide_id: str
    sequence: str
    length: int

    # Binding metrics
    pharmacophore_coverage: float
    z2_match_score: float
    binding_score: float

    # Stability metrics
    hydrophobic_fraction: float
    net_charge: int
    stability_score: float

    # Combined score (the key innovation)
    hybrid_score: float

    # Metadata
    design_strategy: str
    validation_tier: int = 1


class HybridDesigner:
    """
    Designs peptides optimizing for BOTH binding affinity AND structural stability.

    Strategy:
    1. Generate candidates using pharmacophore constraints
    2. Score each for binding potential (Z² geometry)
    3. Score each for stability (compositional properties)
    4. Rank by combined hybrid score
    5. Apply stability filters to ensure foldability
    """

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def design_peptides(
        self,
        target_pdb: Optional[str] = None,
        target_uniprot: str = "UNKNOWN",
        n_peptides: int = 50,
        length_range: Tuple[int, int] = (5, 10),
        binding_weight: float = 0.5,
        stability_weight: float = 0.5
    ) -> List[HybridCandidate]:
        """
        Design peptides balancing binding and stability.

        Args:
            target_pdb: Optional path to target PDB for pharmacophore analysis
            target_uniprot: UniProt ID for tracking
            n_peptides: Number of candidates to generate
            length_range: (min, max) peptide length
            binding_weight: Weight for binding score (0-1)
            stability_weight: Weight for stability score (0-1)
        """
        print(f"\n{'='*70}")
        print("HYBRID PEPTIDE DESIGN (Binding + Stability)")
        print(f"{'='*70}")
        print(f"    Target: {target_uniprot}")
        print(f"    Binding weight: {binding_weight}")
        print(f"    Stability weight: {stability_weight}")
        print(f"    Z² distance: {Z2_INTERACTION_DISTANCE} Å")

        # Load pharmacophore info if PDB provided
        pharmacophore_types = None
        if target_pdb and HAS_BIOPYTHON:
            pharmacophore_types = self._analyze_pocket(target_pdb)
            print(f"    Pharmacophore types needed: {pharmacophore_types}")

        # Generate diverse candidates
        print(f"\n[1/3] Generating {n_peptides * 3} initial candidates...")
        initial_candidates = []
        for _ in range(n_peptides * 3):
            length = np.random.randint(length_range[0], length_range[1] + 1)
            seq = self._generate_hybrid_sequence(length, pharmacophore_types)
            initial_candidates.append(seq)

        # Score all candidates
        print(f"\n[2/3] Scoring for binding + stability...")
        scored = []
        for i, seq in enumerate(initial_candidates):
            binding = self._score_binding(seq, pharmacophore_types)
            stability = self._score_stability(seq)

            # Combined hybrid score
            hybrid = (binding_weight * binding['total'] +
                     stability_weight * stability['total'])

            scored.append({
                'sequence': seq,
                'binding': binding,
                'stability': stability,
                'hybrid': hybrid
            })

        # Sort by hybrid score
        scored = sorted(scored, key=lambda x: x['hybrid'], reverse=True)

        # Apply stability filters and take top N
        print(f"\n[3/3] Applying stability filters...")
        candidates = []
        for i, s in enumerate(scored):
            if len(candidates) >= n_peptides:
                break

            seq = s['sequence']

            # Check stability constraints
            if not self._passes_stability_filter(seq):
                continue

            candidates.append(HybridCandidate(
                peptide_id=f"ZIM-HYB-{len(candidates)+1:03d}",
                sequence=seq,
                length=len(seq),
                pharmacophore_coverage=s['binding']['coverage'],
                z2_match_score=s['binding']['z2_match'],
                binding_score=s['binding']['total'],
                hydrophobic_fraction=s['stability']['hydrophobic_frac'],
                net_charge=s['stability']['charge'],
                stability_score=s['stability']['total'],
                hybrid_score=s['hybrid'],
                design_strategy="Hybrid (Binding + Stability)"
            ))

        # Summary
        print(f"\n    Generated {len(candidates)} hybrid candidates")
        print(f"\n    TOP 5 CANDIDATES:")
        print(f"    {'ID':<15} {'Sequence':<12} {'Binding':<10} {'Stability':<10} {'Hybrid'}")
        print(f"    {'-'*57}")
        for c in candidates[:5]:
            print(f"    {c.peptide_id:<15} {c.sequence:<12} {c.binding_score:.3f}     {c.stability_score:.3f}      {c.hybrid_score:.3f}")

        # Save results
        self._save_results(candidates, target_uniprot, binding_weight, stability_weight)

        return candidates

    def _analyze_pocket(self, pdb_path: str) -> Dict[str, int]:
        """Analyze pocket to determine pharmacophore type distribution."""
        parser = PDBParser(QUIET=True)
        try:
            structure = parser.get_structure('target', pdb_path)
            types = {'hbond_donor': 0, 'hbond_acceptor': 0, 'hydrophobic': 0}

            hbond_donors = {'N', 'NE', 'NH1', 'NH2', 'NZ'}
            hbond_acceptors = {'O', 'OD1', 'OD2', 'OE1', 'OE2'}
            hydrophobic = {'CB', 'CG', 'CD', 'CE', 'CZ'}

            for atom in structure.get_atoms():
                name = atom.get_name()
                if name in hbond_donors:
                    types['hbond_donor'] += 1
                elif name in hbond_acceptors:
                    types['hbond_acceptor'] += 1
                elif name in hydrophobic:
                    types['hydrophobic'] += 1

            return types
        except:
            return None

    def _generate_hybrid_sequence(
        self,
        length: int,
        pharmacophore_types: Optional[Dict] = None
    ) -> str:
        """Generate a sequence balancing binding and stability."""
        sequence = []

        # Ensure at least one charged residue for solubility
        charged_pos = np.random.randint(0, length)

        for pos in range(length):
            if pos == charged_pos:
                # Insert charged residue
                aa = np.random.choice(['K', 'R', 'E', 'D'])
            elif pos % 2 == 0 and pharmacophore_types:
                # Pharmacophore-targeted position
                # Weight selection by pharmacophore needs
                options = []
                weights = []

                if pharmacophore_types.get('hbond_donor', 0) > 0:
                    options.extend(INTERACTION_TYPES['hbond_donor'])
                    weights.extend([1.0] * len(INTERACTION_TYPES['hbond_donor']))
                if pharmacophore_types.get('hbond_acceptor', 0) > 0:
                    options.extend(INTERACTION_TYPES['hbond_acceptor'])
                    weights.extend([1.0] * len(INTERACTION_TYPES['hbond_acceptor']))
                if pharmacophore_types.get('hydrophobic', 0) > 0:
                    options.extend(INTERACTION_TYPES['hydrophobic'])
                    weights.extend([0.8] * len(INTERACTION_TYPES['hydrophobic']))

                if options:
                    weights = np.array(weights) / sum(weights)
                    aa = np.random.choice(options, p=weights)
                else:
                    aa = np.random.choice(list('ACDEFGHIKLMNPQRSTVWY'))
            else:
                # Stability-focused position (small, polar)
                aa = np.random.choice(['G', 'S', 'A', 'T', 'N', 'Q'])

            sequence.append(aa)

        return ''.join(sequence)

    def _score_binding(self, sequence: str, pharmacophore_types: Optional[Dict]) -> Dict:
        """Score binding potential based on Z² geometry."""
        z2_matches = 0
        coverage_types = set()

        for aa in sequence:
            if aa not in SIDECHAIN_LENGTHS:
                continue

            # Check Z² distance match
            sidechain_len = SIDECHAIN_LENGTHS[aa]
            deviation = abs(sidechain_len - Z2_INTERACTION_DISTANCE)
            if deviation < 2.0:  # Within 2 Å of ideal
                z2_matches += 1

            # Check pharmacophore type coverage
            for ptype, aas in INTERACTION_TYPES.items():
                if aa in aas:
                    coverage_types.add(ptype)

        z2_match = z2_matches / len(sequence) if sequence else 0
        coverage = len(coverage_types) / 3  # 3 main types

        # Interaction strength
        strength = sum(
            AA_PROPERTIES.get(aa, {}).get('stability', 0.5)
            for aa in sequence
        ) / len(sequence)

        total = 0.4 * z2_match + 0.3 * coverage + 0.3 * strength

        return {
            'z2_match': z2_match,
            'coverage': coverage,
            'strength': strength,
            'total': total
        }

    def _score_stability(self, sequence: str) -> Dict:
        """Score structural stability based on compositional properties."""
        if not sequence:
            return {'hydrophobic_frac': 0, 'charge': 0, 'helix': 0, 'total': 0}

        hydrophobic_count = sum(
            1 for aa in sequence
            if AA_PROPERTIES.get(aa, {}).get('hydrophobic', False)
        )
        hydrophobic_frac = hydrophobic_count / len(sequence)

        charge = sum(
            AA_PROPERTIES.get(aa, {}).get('charge', 0)
            for aa in sequence
        )

        helix_propensity = sum(
            AA_PROPERTIES.get(aa, {}).get('helix_propensity', 0.5)
            for aa in sequence
        ) / len(sequence)

        # Penalize extreme hydrophobicity
        hydrophobic_score = 1.0 - abs(hydrophobic_frac - 0.3) * 2

        # Reward some charge (solubility)
        charge_score = min(1.0, abs(charge) * 0.3)

        # Reward helix propensity (structure)
        helix_score = helix_propensity / 1.5

        total = 0.4 * hydrophobic_score + 0.3 * charge_score + 0.3 * helix_score

        return {
            'hydrophobic_frac': hydrophobic_frac,
            'charge': charge,
            'helix': helix_propensity,
            'total': total
        }

    def _passes_stability_filter(self, sequence: str) -> bool:
        """Check if sequence passes stability constraints."""
        # Check hydrophobic fraction
        hydrophobic = sum(
            1 for aa in sequence
            if AA_PROPERTIES.get(aa, {}).get('hydrophobic', False)
        )
        if hydrophobic / len(sequence) > MAX_HYDROPHOBIC_FRACTION:
            return False

        # Check for charged residues
        charges = sum(
            abs(AA_PROPERTIES.get(aa, {}).get('charge', 0))
            for aa in sequence
        )
        if charges < MIN_CHARGED_RESIDUES:
            return False

        # Check consecutive hydrophobic stretch
        consecutive = 0
        max_consecutive = 0
        for aa in sequence:
            if AA_PROPERTIES.get(aa, {}).get('hydrophobic', False):
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0

        if max_consecutive > MAX_CONSECUTIVE_HYDROPHOBIC:
            return False

        return True

    def _save_results(
        self,
        candidates: List[HybridCandidate],
        target_uniprot: str,
        binding_weight: float,
        stability_weight: float
    ) -> None:
        """Save design results."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'method': 'Hybrid Design (Binding + Stability)',
            'z2_distance': Z2_INTERACTION_DISTANCE,
            'binding_weight': binding_weight,
            'stability_weight': stability_weight,
            'target_uniprot': target_uniprot,
            'n_candidates': len(candidates),
            'candidates': [asdict(c) for c in candidates]
        }

        output_path = self.output_dir / f"hybrid_design_{target_uniprot}.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n    Saved: {output_path}")


def main():
    """Test hybrid design."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pdb", type=str, help="Target PDB file")
    parser.add_argument("--uniprot", type=str, default="UNKNOWN")
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--binding-weight", type=float, default=0.5)
    parser.add_argument("--stability-weight", type=float, default=0.5)
    parser.add_argument("--output", type=str, default="./hybrid_designs")

    args = parser.parse_args()

    designer = HybridDesigner(Path(args.output))
    candidates = designer.design_peptides(
        target_pdb=args.pdb,
        target_uniprot=args.uniprot,
        n_peptides=args.n,
        binding_weight=args.binding_weight,
        stability_weight=args.stability_weight
    )

    return candidates


if __name__ == "__main__":
    main()
