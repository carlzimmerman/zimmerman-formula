#!/usr/bin/env python3
"""
m05_structure_prediction.py - Peptide Structure Prediction

Predicts 3D structures for peptides using ESMFold API.
Only peptides with confident predictions (pLDDT > 70) proceed to docking.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import warnings

try:
    from Bio.PDB import PDBParser, PDBIO
    from Bio.PDB.DSSP import DSSP
    HAS_BIOPYTHON = True
except ImportError:
    HAS_BIOPYTHON = False


@dataclass
class StructurePrediction:
    """Result of structure prediction for one peptide."""
    peptide_id: str
    sequence: str

    # Prediction results
    success: bool
    pdb_path: Optional[str]
    plddt_mean: float  # Mean predicted LDDT (0-100)
    plddt_min: float

    # Quality metrics
    passes_threshold: bool  # pLDDT > 70

    # Metadata
    method: str = "ESMFold"
    validation_tier: int = 2  # TIER 2 if successful


class StructurePredictor:
    """
    Predicts peptide 3D structures using ESMFold.

    ESMFold is open-source and doesn't require MSA,
    making it suitable for short peptides.
    """

    ESMFOLD_API = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    PLDDT_THRESHOLD = 0.70  # Minimum confidence for docking (0-1 scale from ESMFold API)

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.structures_dir = self.output_dir / "structures"
        self.structures_dir.mkdir(exist_ok=True)

    def predict_structures(
        self,
        peptides: List[Dict],
        batch_delay: float = 1.0
    ) -> List[StructurePrediction]:
        """
        Predict structures for all peptides.

        Args:
            peptides: List of peptide dicts with 'peptide_id' and 'sequence'
            batch_delay: Delay between API calls (be nice to server)

        Returns:
            List of StructurePrediction results
        """
        print(f"\n{'='*70}")
        print("STRUCTURE PREDICTION MODULE")
        print(f"{'='*70}")
        print(f"    Peptides: {len(peptides)}")
        print(f"    Method: ESMFold API")
        print(f"    Threshold: pLDDT > {self.PLDDT_THRESHOLD}")

        results = []
        passed = 0
        failed = 0

        for i, peptide in enumerate(peptides):
            # Handle both dict and dataclass objects
            if hasattr(peptide, 'peptide_id'):
                peptide_id = peptide.peptide_id
                sequence = peptide.sequence
            else:
                peptide_id = peptide['peptide_id']
                sequence = peptide['sequence']

            print(f"\n[{i+1}/{len(peptides)}] {peptide_id}: {sequence}")

            result = self._predict_single(peptide_id, sequence)
            results.append(result)

            if result.passes_threshold:
                passed += 1
                print(f"    ✓ pLDDT: {result.plddt_mean:.1f} (PASS)")
            else:
                failed += 1
                print(f"    ✗ pLDDT: {result.plddt_mean:.1f} (FAIL)")

            # Rate limiting
            if i < len(peptides) - 1:
                time.sleep(batch_delay)

        # Summary
        print(f"\n{'='*70}")
        print("STRUCTURE PREDICTION SUMMARY")
        print(f"{'='*70}")
        print(f"""
    Total:   {len(peptides)}
    Passed:  {passed} (pLDDT > {self.PLDDT_THRESHOLD})
    Failed:  {failed}

    VALIDATION TIER: 2 (Structure Predicted)

    Peptides with pLDDT > {self.PLDDT_THRESHOLD} proceed to docking.
""")

        # Save results
        self._save_results(results)

        return results

    def _predict_single(self, peptide_id: str, sequence: str, max_retries: int = 3) -> StructurePrediction:
        """Predict structure for a single peptide with retry logic."""
        last_error = None

        for attempt in range(max_retries):
            try:
                # Call ESMFold API with exponential backoff
                response = requests.post(
                    self.ESMFOLD_API,
                    data=sequence,
                    headers={"Content-Type": "text/plain"},
                    timeout=120  # Increased timeout for longer sequences
                )

                if response.status_code == 429:  # Rate limited
                    wait_time = 2 ** (attempt + 1)
                    print(f"    Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                if response.status_code == 503:  # Service unavailable
                    wait_time = 5 * (attempt + 1)
                    print(f"    Service unavailable, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                if response.status_code != 200:
                    last_error = f"HTTP {response.status_code}"
                    continue

                pdb_content = response.text

                # Save PDB
                pdb_path = self.structures_dir / f"{peptide_id}.pdb"
                with open(pdb_path, 'w') as f:
                    f.write(pdb_content)

                # Extract pLDDT from B-factor column
                plddt_values = self._extract_plddt(pdb_content)
                plddt_mean = sum(plddt_values) / len(plddt_values) if plddt_values else 0.0
                plddt_min = min(plddt_values) if plddt_values else 0.0

                return StructurePrediction(
                    peptide_id=peptide_id,
                    sequence=sequence,
                    success=True,
                    pdb_path=str(pdb_path),
                    plddt_mean=plddt_mean,
                    plddt_min=plddt_min,
                    passes_threshold=plddt_mean >= self.PLDDT_THRESHOLD,
                )

            except requests.exceptions.Timeout:
                last_error = "Timeout"
                print(f"    Timeout on attempt {attempt + 1}")
                continue
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {e}"
                print(f"    Connection error on attempt {attempt + 1}")
                time.sleep(2 ** attempt)
                continue
            except Exception as e:
                last_error = str(e)
                print(f"    ERROR on attempt {attempt + 1}: {e}")
                continue

        # All retries failed
        return StructurePrediction(
            peptide_id=peptide_id,
            sequence=sequence,
            success=False,
            pdb_path=None,
            plddt_mean=0.0,
            plddt_min=0.0,
            passes_threshold=False,
        )

    def _extract_plddt(self, pdb_content: str) -> List[float]:
        """Extract pLDDT values from B-factor column of PDB."""
        plddt_values = []

        for line in pdb_content.split('\n'):
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    # B-factor is columns 61-66
                    bfactor = float(line[60:66].strip())
                    plddt_values.append(bfactor)
                except (ValueError, IndexError):
                    pass

        return plddt_values

    def _save_results(self, results: List[StructurePrediction]) -> None:
        """Save prediction results."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'method': 'ESMFold',
            'threshold': self.PLDDT_THRESHOLD,
            'total': len(results),
            'passed': sum(1 for r in results if r.passes_threshold),
            'predictions': [asdict(r) for r in results]
        }

        output_path = self.output_dir / "structure_predictions.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"    Saved: {output_path}")


def main():
    """Test structure prediction."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    args = parser.parse_args()

    # Load peptides from design results
    base_dir = Path(__file__).parent.parent
    project_dir = base_dir / "projects" / args.project

    # Find design file
    design_files = list((project_dir / "peptide_designs").glob("design_*.json"))
    if not design_files:
        print("ERROR: No design file found")
        return

    with open(design_files[0]) as f:
        design_data = json.load(f)

    # Get peptides (designed + controls)
    peptides = design_data['designed_peptides'] + design_data['control_peptides']

    # Predict structures
    predictor = StructurePredictor(project_dir / "structures")
    results = predictor.predict_structures(peptides)

    # Report
    passed = [r for r in results if r.passes_threshold]
    print(f"\n{len(passed)} peptides ready for docking")

    return results


if __name__ == "__main__":
    main()
