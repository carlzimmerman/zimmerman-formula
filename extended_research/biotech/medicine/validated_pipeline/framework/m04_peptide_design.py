#!/usr/bin/env python3
"""
m04_peptide_design.py - Peptide Design Module with Negative Controls

Generates peptide candidates with MANDATORY negative controls.
If designed peptides don't outperform random, the design strategy is broken.

CRITICAL: No heuristic scoring. Only chemistry validation at this stage.
Binding prediction happens in Module 6 (Docking).

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import random
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
import warnings

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, MolFromSequence, MolToSmiles
    from rdkit.Chem.rdMolDescriptors import CalcMolFormula
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False
    warnings.warn("RDKit required: pip install rdkit")


# Standard amino acids
AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")

# Amino acid properties
AA_PROPERTIES = {
    'A': {'mw': 89.09, 'charge': 0, 'hydrophobic': True, 'aromatic': False},
    'C': {'mw': 121.16, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'D': {'mw': 133.10, 'charge': -1, 'hydrophobic': False, 'aromatic': False},
    'E': {'mw': 147.13, 'charge': -1, 'hydrophobic': False, 'aromatic': False},
    'F': {'mw': 165.19, 'charge': 0, 'hydrophobic': True, 'aromatic': True},
    'G': {'mw': 75.07, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'H': {'mw': 155.16, 'charge': 0, 'hydrophobic': False, 'aromatic': True},
    'I': {'mw': 131.17, 'charge': 0, 'hydrophobic': True, 'aromatic': False},
    'K': {'mw': 146.19, 'charge': 1, 'hydrophobic': False, 'aromatic': False},
    'L': {'mw': 131.17, 'charge': 0, 'hydrophobic': True, 'aromatic': False},
    'M': {'mw': 149.21, 'charge': 0, 'hydrophobic': True, 'aromatic': False},
    'N': {'mw': 132.12, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'P': {'mw': 115.13, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'Q': {'mw': 146.15, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'R': {'mw': 174.20, 'charge': 1, 'hydrophobic': False, 'aromatic': False},
    'S': {'mw': 105.09, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'T': {'mw': 119.12, 'charge': 0, 'hydrophobic': False, 'aromatic': False},
    'V': {'mw': 117.15, 'charge': 0, 'hydrophobic': True, 'aromatic': False},
    'W': {'mw': 204.23, 'charge': 0, 'hydrophobic': True, 'aromatic': True},
    'Y': {'mw': 181.19, 'charge': 0, 'hydrophobic': True, 'aromatic': True},
}


@dataclass
class PeptideCandidate:
    """A peptide candidate with validation status."""
    peptide_id: str
    sequence: str
    length: int
    is_designed: bool  # True = designed, False = random control

    # Chemistry (TIER 1)
    rdkit_valid: bool
    smiles: str
    molecular_formula: str
    molecular_weight: float

    # Properties (computed, not predicted binding)
    net_charge: int
    hydrophobic_fraction: float
    aromatic_count: int

    # Metadata
    design_rationale: str
    validation_tier: int = 1  # TIER 1 if RDKit valid

    # Later validation stages will add:
    # - structure_pdb (TIER 2)
    # - docking_score (TIER 3)
    # - md_rmsd (TIER 4)
    # - binding_dG (TIER 5)


@dataclass
class DesignResult:
    """Result of peptide design with controls."""
    project_id: str
    target_uniprot: str
    design_strategy: str

    designed_peptides: List[PeptideCandidate]
    control_peptides: List[PeptideCandidate]

    n_designed: int
    n_controls: int
    n_valid_designed: int
    n_valid_controls: int

    created_at: str
    validation_tier: int = 1


class PeptideDesigner:
    """
    Designs peptides with mandatory negative controls.

    CRITICAL: This module does NOT predict binding.
    It only generates sequences and validates chemistry.
    Binding prediction happens in Module 6 (Docking).
    """

    def __init__(self, output_dir: Path, project_id: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_id = project_id

        if not HAS_RDKIT:
            raise ImportError("RDKit required for chemistry validation")

    def design_peptides(
        self,
        target_uniprot: str,
        n_designed: int = 20,
        n_controls: int = 100,
        length_range: Tuple[int, int] = (4, 12),
        design_strategy: str = "constraint_based",
        constraints: Optional[Dict] = None
    ) -> DesignResult:
        """
        Design peptides with negative controls.

        Args:
            target_uniprot: UniProt ID of target protein
            n_designed: Number of designed peptides
            n_controls: Number of random controls (should be >= 5x designed)
            length_range: Min and max peptide length
            design_strategy: Description of design approach
            constraints: Optional constraints (charge, hydrophobicity, etc.)

        Returns:
            DesignResult with designed peptides and controls
        """
        print(f"\n{'='*70}")
        print(f"PEPTIDE DESIGN MODULE")
        print(f"{'='*70}")
        print(f"    Target: {target_uniprot}")
        print(f"    Designed: {n_designed}")
        print(f"    Controls: {n_controls}")
        print(f"    Length range: {length_range[0]}-{length_range[1]}")

        if n_controls < n_designed * 5:
            warnings.warn(f"Recommend at least {n_designed * 5} controls for statistical power")

        # Default constraints
        if constraints is None:
            constraints = {
                'min_charge': -2,
                'max_charge': 3,
                'min_hydrophobic': 0.2,
                'max_hydrophobic': 0.7,
                'require_aromatic': True,
            }

        # Generate designed peptides
        print(f"\n[1/3] Generating {n_designed} designed peptides...")
        designed = []
        attempts = 0
        max_attempts = n_designed * 10

        while len(designed) < n_designed and attempts < max_attempts:
            attempts += 1
            length = random.randint(length_range[0], length_range[1])
            sequence = self._generate_constrained_sequence(length, constraints)

            candidate = self._validate_peptide(
                sequence=sequence,
                peptide_id=f"ZIM-{self.project_id}-{len(designed)+1:03d}",
                is_designed=True,
                rationale=f"Constraint-based: {constraints}"
            )

            if candidate.rdkit_valid:
                designed.append(candidate)
                print(f"      {candidate.peptide_id}: {candidate.sequence} (MW: {candidate.molecular_weight:.1f})")

        # Generate random controls
        print(f"\n[2/3] Generating {n_controls} random controls...")
        controls = []

        for i in range(n_controls):
            length = random.randint(length_range[0], length_range[1])
            sequence = self._generate_random_sequence(length)

            candidate = self._validate_peptide(
                sequence=sequence,
                peptide_id=f"CTRL-{self.project_id}-{i+1:03d}",
                is_designed=False,
                rationale="Random control (no design constraints)"
            )

            if candidate.rdkit_valid:
                controls.append(candidate)

        print(f"      Generated {len(controls)} valid controls")

        # Build result
        result = DesignResult(
            project_id=self.project_id,
            target_uniprot=target_uniprot,
            design_strategy=design_strategy,
            designed_peptides=designed,
            control_peptides=controls,
            n_designed=len(designed),
            n_controls=len(controls),
            n_valid_designed=sum(1 for p in designed if p.rdkit_valid),
            n_valid_controls=sum(1 for p in controls if p.rdkit_valid),
            created_at=datetime.now().isoformat(),
            validation_tier=1,
        )

        # Save results
        self._save_results(result)

        # Print summary
        print(f"\n[3/3] Design Complete")
        print(f"{'='*70}")
        print(f"""
    DESIGN SUMMARY
    ──────────────
    Designed peptides: {result.n_valid_designed} / {n_designed}
    Random controls:   {result.n_valid_controls} / {n_controls}

    VALIDATION TIER: 1 (Chemistry Validated)

    IMPORTANT: No binding predictions made yet.
    These peptides need:
      - TIER 2: Structure prediction (ESMFold)
      - TIER 3: Docking (AutoDock Vina)
      - TIER 4: MD stability (OpenMM)
      - TIER 5: Binding energy (MM-PBSA)

    If designed peptides don't outperform controls at TIER 3+,
    the design strategy is ineffective.
""")

        return result

    def _generate_constrained_sequence(self, length: int, constraints: Dict) -> str:
        """Generate a sequence that satisfies constraints."""
        max_attempts = 100

        for _ in range(max_attempts):
            sequence = []

            # Start with constrained selection
            if constraints.get('require_aromatic', False):
                # Ensure at least one aromatic
                aromatic = random.choice(['F', 'W', 'Y', 'H'])
                sequence.append(aromatic)

            # Fill rest of sequence
            while len(sequence) < length:
                # Weighted selection based on constraints
                if random.random() < constraints.get('min_hydrophobic', 0.3):
                    aa = random.choice(['A', 'V', 'L', 'I', 'M', 'F', 'W', 'Y'])
                else:
                    aa = random.choice(AMINO_ACIDS)
                sequence.append(aa)

            random.shuffle(sequence)
            seq_str = ''.join(sequence)

            # Check constraints
            if self._check_constraints(seq_str, constraints):
                return seq_str

        # Fallback to random if constraints too strict
        return self._generate_random_sequence(length)

    def _generate_random_sequence(self, length: int) -> str:
        """Generate a completely random peptide sequence."""
        return ''.join(random.choices(AMINO_ACIDS, k=length))

    def _check_constraints(self, sequence: str, constraints: Dict) -> bool:
        """Check if sequence satisfies constraints."""
        # Calculate properties
        charge = sum(AA_PROPERTIES[aa]['charge'] for aa in sequence)
        hydrophobic = sum(1 for aa in sequence if AA_PROPERTIES[aa]['hydrophobic']) / len(sequence)
        aromatics = sum(1 for aa in sequence if AA_PROPERTIES[aa]['aromatic'])

        # Check bounds
        if charge < constraints.get('min_charge', -10):
            return False
        if charge > constraints.get('max_charge', 10):
            return False
        if hydrophobic < constraints.get('min_hydrophobic', 0):
            return False
        if hydrophobic > constraints.get('max_hydrophobic', 1):
            return False
        if constraints.get('require_aromatic', False) and aromatics == 0:
            return False

        return True

    def _validate_peptide(
        self,
        sequence: str,
        peptide_id: str,
        is_designed: bool,
        rationale: str
    ) -> PeptideCandidate:
        """Validate peptide chemistry with RDKit."""
        # Calculate basic properties
        charge = sum(AA_PROPERTIES.get(aa, {}).get('charge', 0) for aa in sequence)
        hydrophobic = sum(1 for aa in sequence if AA_PROPERTIES.get(aa, {}).get('hydrophobic', False)) / len(sequence)
        aromatics = sum(1 for aa in sequence if AA_PROPERTIES.get(aa, {}).get('aromatic', False))

        # RDKit validation
        rdkit_valid = False
        smiles = ""
        formula = ""
        mw = 0.0

        try:
            mol = MolFromSequence(sequence)
            if mol is not None:
                Chem.SanitizeMol(mol)
                rdkit_valid = True
                smiles = MolToSmiles(mol, canonical=True)
                formula = CalcMolFormula(mol)
                mw = Descriptors.ExactMolWt(mol)
        except Exception:
            pass

        return PeptideCandidate(
            peptide_id=peptide_id,
            sequence=sequence,
            length=len(sequence),
            is_designed=is_designed,
            rdkit_valid=rdkit_valid,
            smiles=smiles,
            molecular_formula=formula,
            molecular_weight=mw,
            net_charge=charge,
            hydrophobic_fraction=hydrophobic,
            aromatic_count=aromatics,
            design_rationale=rationale,
            validation_tier=1 if rdkit_valid else 0,
        )

    def _save_results(self, result: DesignResult) -> None:
        """Save design results to JSON."""
        output = {
            'project_id': result.project_id,
            'target_uniprot': result.target_uniprot,
            'design_strategy': result.design_strategy,
            'n_designed': result.n_designed,
            'n_controls': result.n_controls,
            'n_valid_designed': result.n_valid_designed,
            'n_valid_controls': result.n_valid_controls,
            'created_at': result.created_at,
            'validation_tier': result.validation_tier,
            'designed_peptides': [asdict(p) for p in result.designed_peptides],
            'control_peptides': [asdict(p) for p in result.control_peptides],
        }

        output_path = self.output_dir / f"design_{result.project_id}.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n    Saved: {output_path}")


def main():
    """Example usage."""
    output_dir = Path(__file__).parent.parent / "results" / "peptide_designs"

    designer = PeptideDesigner(
        output_dir=output_dir,
        project_id="ASYN"  # α-synuclein project
    )

    # Design peptides for α-synuclein
    result = designer.design_peptides(
        target_uniprot="P37840",
        n_designed=20,
        n_controls=100,
        length_range=(4, 8),
        design_strategy="Aromatic-rich for amyloid intercalation",
        constraints={
            'min_charge': -1,
            'max_charge': 2,
            'min_hydrophobic': 0.3,
            'max_hydrophobic': 0.8,
            'require_aromatic': True,
        }
    )

    print("\n" + "="*70)
    print("READY FOR MODULE 5: STRUCTURE PREDICTION")
    print("="*70)
    print(f"\n    Use: python m05_structure_prediction.py --project {result.project_id}")

    return result


if __name__ == "__main__":
    result = main()
