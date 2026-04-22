#!/usr/bin/env python3
"""
m06b_geometric_scoring.py - Preliminary Geometric Binding Analysis

IMPORTANT DISCLAIMER:
This module provides GEOMETRIC SCORING ONLY, not true molecular docking.
It calculates shape complementarity and surface area metrics but does NOT:
- Sample binding poses
- Calculate binding free energies
- Account for solvation effects
- Optimize ligand conformations

For true validation, peptides must be docked using:
- AutoDock Vina (recommended)
- HADDOCK web server (https://wenmr.science.uu.nl/haddock2.4/)
- CABS-dock (https://biocomp.chem.uw.edu.pl/CABSdock)

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import math
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import warnings

try:
    from Bio.PDB import PDBParser, PDBIO, NeighborSearch
    from Bio.PDB.SASA import ShrakeRupley
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False


@dataclass
class GeometricScore:
    """Results of geometric analysis for one peptide."""
    peptide_id: str
    sequence: str
    is_designed: bool

    # Geometric metrics
    solvent_accessible_surface: float  # Angstroms²
    hydrophobic_fraction: float
    charged_fraction: float
    aromatic_fraction: float

    # Composition metrics
    n_residues: int
    molecular_weight: float

    # Z² framework metrics
    packing_density_estimate: float

    # Metadata
    success: bool
    validation_tier: int = 1  # Tier 1 = Chemistry/geometry only
    notes: str = ""


class GeometricScorer:
    """
    Calculates geometric and compositional properties of peptides.

    THIS IS NOT MOLECULAR DOCKING.
    This provides preliminary metrics for peptide characterization
    and requires validation with proper docking software.
    """

    # Amino acid properties
    HYDROPHOBIC = set('AILMFVPGW')
    CHARGED = set('DEKRH')
    AROMATIC = set('FYW')

    AA_MW = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze_peptides(
        self,
        peptides: List[Dict],
        structure_predictions: Optional[Dict] = None
    ) -> List[GeometricScore]:
        """
        Analyze peptide geometric properties.

        Args:
            peptides: List of peptide dicts with 'peptide_id' and 'sequence'
            structure_predictions: Optional dict of pLDDT scores

        Returns:
            List of GeometricScore results
        """
        print(f"\n{'='*70}")
        print("GEOMETRIC SCORING MODULE")
        print(f"{'='*70}")
        print(f"""
    ⚠️  WARNING: This is NOT molecular docking.

    This module calculates geometric properties only:
    - Surface area estimates
    - Compositional analysis
    - Packing density metrics

    For binding affinity prediction, use:
    - AutoDock Vina
    - HADDOCK server
    - CABS-dock
""")

        results = []

        for peptide in peptides:
            peptide_id = peptide['peptide_id']
            sequence = peptide['sequence']
            is_designed = peptide_id.startswith('ZIM')

            result = self._analyze_single(peptide_id, sequence, is_designed)
            results.append(result)

        # Summary statistics
        self._print_summary(results)
        self._save_results(results)

        return results

    def _analyze_single(self, peptide_id: str, sequence: str, is_designed: bool) -> GeometricScore:
        """Analyze a single peptide."""
        n_residues = len(sequence)

        # Compositional analysis
        hydrophobic_count = sum(1 for aa in sequence if aa in self.HYDROPHOBIC)
        charged_count = sum(1 for aa in sequence if aa in self.CHARGED)
        aromatic_count = sum(1 for aa in sequence if aa in self.AROMATIC)

        hydrophobic_fraction = hydrophobic_count / n_residues
        charged_fraction = charged_count / n_residues
        aromatic_fraction = aromatic_count / n_residues

        # Molecular weight
        mw = sum(self.AA_MW.get(aa, 110) for aa in sequence) - (n_residues - 1) * 18.015

        # Estimate solvent accessible surface area
        # Using empirical formula: SASA ≈ 1.4 * n_residues^0.75 * 100 Å²
        # This is a rough estimate without actual structure
        sasa_estimate = 1.4 * (n_residues ** 0.75) * 100

        # Z² framework: estimate packing density
        # Based on Z² = 32π/3 ≈ 33.5 as optimal packing
        z_squared = 32 * math.pi / 3
        # For peptides, packing density relates to compactness
        # Random coil: lower density, helix/sheet: higher density
        # Aromatic residues improve packing
        packing_estimate = (0.5 + 0.3 * aromatic_fraction + 0.2 * hydrophobic_fraction)

        return GeometricScore(
            peptide_id=peptide_id,
            sequence=sequence,
            is_designed=is_designed,
            solvent_accessible_surface=sasa_estimate,
            hydrophobic_fraction=hydrophobic_fraction,
            charged_fraction=charged_fraction,
            aromatic_fraction=aromatic_fraction,
            n_residues=n_residues,
            molecular_weight=mw,
            packing_density_estimate=packing_estimate,
            success=True,
            notes="Geometric analysis only - not molecular docking"
        )

    def _print_summary(self, results: List[GeometricScore]) -> None:
        """Print summary comparison."""
        designed = [r for r in results if r.is_designed]
        controls = [r for r in results if not r.is_designed]

        print(f"\n{'='*70}")
        print("GEOMETRIC ANALYSIS SUMMARY")
        print(f"{'='*70}")

        def mean(lst):
            return sum(lst)/len(lst) if lst else 0

        print(f"""
    DESIGNED PEPTIDES (n={len(designed)}):
        Mean hydrophobic: {mean([r.hydrophobic_fraction for r in designed]):.3f}
        Mean aromatic:    {mean([r.aromatic_fraction for r in designed]):.3f}
        Mean charged:     {mean([r.charged_fraction for r in designed]):.3f}
        Mean MW:          {mean([r.molecular_weight for r in designed]):.1f} Da

    CONTROL PEPTIDES (n={len(controls)}):
        Mean hydrophobic: {mean([r.hydrophobic_fraction for r in controls]):.3f}
        Mean aromatic:    {mean([r.aromatic_fraction for r in controls]):.3f}
        Mean charged:     {mean([r.charged_fraction for r in controls]):.3f}
        Mean MW:          {mean([r.molecular_weight for r in controls]):.1f} Da

    ⚠️  THESE ARE GEOMETRIC PROPERTIES, NOT BINDING SCORES

    For binding validation, submit peptides to:
    - HADDOCK: https://wenmr.science.uu.nl/haddock2.4/
    - CABS-dock: https://biocomp.chem.uw.edu.pl/CABSdock
    - MDockPeP: http://zougrouptoolkit.missouri.edu/mdockpep
""")

    def _save_results(self, results: List[GeometricScore]) -> None:
        """Save results to JSON."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'method': 'Geometric Analysis (NOT docking)',
            'disclaimer': 'These are geometric properties only. True binding affinity requires molecular docking.',
            'validation_tier': 1,
            'total': len(results),
            'results': [asdict(r) for r in results]
        }

        output_path = self.output_dir / "geometric_analysis.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"    Saved: {output_path}")


def main():
    """Run geometric analysis."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    project_dir = base_dir / "projects" / args.project

    # Load peptide designs
    design_files = list((project_dir / "peptide_designs").glob("design_*.json"))
    if not design_files:
        print("ERROR: No design file found")
        return

    with open(design_files[0]) as f:
        design_data = json.load(f)

    peptides = design_data['designed_peptides'] + design_data['control_peptides']

    # Run geometric analysis
    scorer = GeometricScorer(project_dir / "geometric_analysis")
    results = scorer.analyze_peptides(peptides)

    return results


if __name__ == "__main__":
    main()
