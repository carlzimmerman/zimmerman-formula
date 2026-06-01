#!/usr/bin/env python3
"""
M4 Cross-Validation Controller - Master Orchestrator for Peptide Validation

Coordinates all three validation layers:
1. Orthogonal RMSD Checker (ESMFold vs AlphaFold2 consensus)
2. Stereochemical QA Parser (Ramachandran, clashes, geometry)
3. Thermal Stress MD (350K stability simulation)

A peptide must pass ALL THREE layers to be considered "validated".
This prevents any single method's hallucinations from reaching production.

Final Output:
- VALIDATED: Passes all three layers - safe for synthesis consideration
- FLAGGED: Fails one layer - investigate before proceeding
- REJECTED: Fails two or more layers - likely computational artifact

LICENSE: AGPL-3.0-or-later (code) + OpenMTA (biological materials)
PRIOR ART ESTABLISHED: April 20, 2026

WARNING: Even VALIDATED candidates require experimental verification
(synthesis, biophysical characterization, in vitro/vivo testing).
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, field
import numpy as np

# Import validation modules
from m4_orthogonal_rmsd_checker import OrthogonalRMSDChecker
from m4_stereochemical_qa_parser import StereochemicalQAParser
from m4_thermal_stress_md import ThermalStressValidator


@dataclass
class ValidationLayerResult:
    """Result from a single validation layer"""
    layer_name: str
    passed: bool
    score: float
    confidence: str
    details: Dict
    failure_reasons: List[str]


@dataclass
class CrossValidationResult:
    """Complete cross-validation result for a single peptide"""
    sequence: str
    sequence_hash: str
    n_residues: int

    # Layer results
    rmsd_consensus: ValidationLayerResult
    stereochemical_qa: ValidationLayerResult
    thermal_stress: ValidationLayerResult

    # Aggregate assessment
    layers_passed: int
    total_layers: int
    aggregate_score: float

    # Final verdict
    final_verdict: str  # VALIDATED, FLAGGED, REJECTED
    recommendation: str

    validation_timestamp: str


class CrossValidationController:
    """
    Master orchestrator for multi-layer peptide validation.

    Philosophy: Defense in depth. A hallucinated structure might fool one
    validation method (e.g., good pLDDT but physically impossible geometry),
    but is unlikely to pass ALL THREE independent checks.
    """

    VERDICT_THRESHOLDS = {
        'VALIDATED': 3,   # Must pass all 3 layers
        'FLAGGED': 2,     # Passed 2 layers - investigate
        'REJECTED': 0     # Passed 0-1 layers - likely artifact
    }

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("validation_results")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize sub-validators
        self.rmsd_checker = OrthogonalRMSDChecker(self.output_dir)
        self.stereo_parser = StereochemicalQAParser(self.output_dir)
        self.thermal_validator = ThermalStressValidator(self.output_dir, temperature=350.0)

    def run_rmsd_consensus(self, sequence: str) -> ValidationLayerResult:
        """Layer 1: Cross-validate ESMFold vs AlphaFold2"""
        result = self.rmsd_checker.validate_structure(sequence)

        return ValidationLayerResult(
            layer_name="RMSD Consensus (ESMFold vs AF2)",
            passed=not result.is_hallucination,
            score=100 - result.rmsd * 20,  # Lower RMSD = higher score
            confidence=result.consensus_confidence,
            details={
                'rmsd': result.rmsd,
                'tm_score': result.tm_score,
                'plddt_esm': result.mean_plddt_1,
                'plddt_af2': result.mean_plddt_2,
                'low_conf_regions': result.low_confidence_regions
            },
            failure_reasons=[result.hallucination_reason] if result.hallucination_reason else []
        )

    def run_stereochemical_qa(self, sequence: str) -> ValidationLayerResult:
        """Layer 2: Physics sanity check"""
        result = self.stereo_parser.validate_structure(sequence)

        return ValidationLayerResult(
            layer_name="Stereochemical QA (Ramachandran + Clashes)",
            passed=result.passes_qa,
            score=result.qa_score,
            confidence="HIGH" if result.qa_score > 80 else "MEDIUM" if result.qa_score > 60 else "LOW",
            details={
                'rama_favored_pct': result.rama_favored_percent,
                'rama_outliers': result.rama_outlier,
                'severe_clashes': result.n_severe_clashes,
                'bond_outliers': result.bond_outliers,
                'twisted_peptides': result.twisted_peptides
            },
            failure_reasons=result.failure_reasons
        )

    def run_thermal_stress(self, sequence: str) -> ValidationLayerResult:
        """Layer 3: Thermal stability simulation"""
        result = self.thermal_validator.validate_structure(sequence, n_steps=50000)  # Quick screen

        return ValidationLayerResult(
            layer_name="Thermal Stress MD (350K)",
            passed=result.is_stable,
            score=result.stability_score,
            confidence="HIGH" if result.stability_score > 80 else "MEDIUM" if result.stability_score > 50 else "LOW",
            details={
                'mean_rmsd': result.mean_rmsd,
                'rmsd_drift': result.rmsd_slope,
                'rg_expansion': result.rg_expansion,
                'hbond_retention': result.hbond_retention,
                'rmsd_plateau': result.rmsd_plateau
            },
            failure_reasons=result.failure_reasons
        )

    def cross_validate(self, sequence: str) -> CrossValidationResult:
        """
        Run all three validation layers on a peptide sequence.
        """
        seq_hash = hashlib.sha256(sequence.encode()).hexdigest()[:16]
        n_residues = len(sequence)

        print(f"\n{'='*60}")
        print(f"CROSS-VALIDATING: {sequence[:40]}{'...' if len(sequence) > 40 else ''}")
        print(f"{'='*60}")

        # Layer 1: RMSD Consensus
        print("\n[1/3] Running RMSD consensus validation...")
        rmsd_result = self.run_rmsd_consensus(sequence)
        status1 = "PASS" if rmsd_result.passed else "FAIL"
        print(f"      Result: {status1} (score: {rmsd_result.score:.1f})")

        # Layer 2: Stereochemical QA
        print("\n[2/3] Running stereochemical QA...")
        stereo_result = self.run_stereochemical_qa(sequence)
        status2 = "PASS" if stereo_result.passed else "FAIL"
        print(f"      Result: {status2} (score: {stereo_result.score:.1f})")

        # Layer 3: Thermal Stress
        print("\n[3/3] Running thermal stress simulation...")
        thermal_result = self.run_thermal_stress(sequence)
        status3 = "PASS" if thermal_result.passed else "FAIL"
        print(f"      Result: {status3} (score: {thermal_result.score:.1f})")

        # Aggregate results
        layers_passed = sum([
            rmsd_result.passed,
            stereo_result.passed,
            thermal_result.passed
        ])

        aggregate_score = (
            rmsd_result.score * 0.3 +
            stereo_result.score * 0.4 +  # Physics is most important
            thermal_result.score * 0.3
        )

        # Determine verdict
        if layers_passed >= self.VERDICT_THRESHOLDS['VALIDATED']:
            verdict = "VALIDATED"
            recommendation = "Safe for synthesis consideration. Proceed to experimental validation."
        elif layers_passed >= self.VERDICT_THRESHOLDS['FLAGGED']:
            verdict = "FLAGGED"
            recommendation = "Investigate failure layer. May need manual review before proceeding."
        else:
            verdict = "REJECTED"
            recommendation = "Likely computational artifact. Do not proceed to synthesis."

        return CrossValidationResult(
            sequence=sequence,
            sequence_hash=seq_hash,
            n_residues=n_residues,
            rmsd_consensus=rmsd_result,
            stereochemical_qa=stereo_result,
            thermal_stress=thermal_result,
            layers_passed=layers_passed,
            total_layers=3,
            aggregate_score=float(aggregate_score),
            final_verdict=verdict,
            recommendation=recommendation,
            validation_timestamp=datetime.now().isoformat()
        )

    def validate_batch(self, sequences: List[str]) -> Dict:
        """Run cross-validation on a batch of sequences."""
        results = []
        for seq in sequences:
            result = self.cross_validate(seq)
            results.append(result)

        # Summary statistics
        n_total = len(results)
        n_validated = sum(1 for r in results if r.final_verdict == "VALIDATED")
        n_flagged = sum(1 for r in results if r.final_verdict == "FLAGGED")
        n_rejected = sum(1 for r in results if r.final_verdict == "REJECTED")

        mean_score = np.mean([r.aggregate_score for r in results])

        # Layer-specific pass rates
        rmsd_pass_rate = sum(1 for r in results if r.rmsd_consensus.passed) / n_total
        stereo_pass_rate = sum(1 for r in results if r.stereochemical_qa.passed) / n_total
        thermal_pass_rate = sum(1 for r in results if r.thermal_stress.passed) / n_total

        summary = {
            "metadata": {
                "generator": "M4 Cross-Validation Controller",
                "timestamp": datetime.now().isoformat(),
                "n_sequences": n_total,
                "validation_layers": [
                    "RMSD Consensus (ESMFold vs AlphaFold2)",
                    "Stereochemical QA (Ramachandran + Clashes)",
                    "Thermal Stress MD (350K)"
                ],
                "license": "AGPL-3.0-or-later (code) + OpenMTA (biological materials)"
            },
            "summary": {
                "total_sequences": n_total,
                "validated": n_validated,
                "flagged": n_flagged,
                "rejected": n_rejected,
                "validation_rate": n_validated / n_total if n_total > 0 else 0,
                "mean_aggregate_score": float(mean_score),
                "layer_pass_rates": {
                    "rmsd_consensus": float(rmsd_pass_rate),
                    "stereochemical_qa": float(stereo_pass_rate),
                    "thermal_stress": float(thermal_pass_rate)
                }
            },
            "results": []
        }

        # Serialize results (convert dataclasses to dicts)
        for r in results:
            result_dict = {
                'sequence': r.sequence,
                'sequence_hash': r.sequence_hash,
                'n_residues': r.n_residues,
                'layers_passed': r.layers_passed,
                'total_layers': r.total_layers,
                'aggregate_score': r.aggregate_score,
                'final_verdict': r.final_verdict,
                'recommendation': r.recommendation,
                'validation_timestamp': r.validation_timestamp,
                'layer_results': {
                    'rmsd_consensus': asdict(r.rmsd_consensus),
                    'stereochemical_qa': asdict(r.stereochemical_qa),
                    'thermal_stress': asdict(r.thermal_stress)
                }
            }
            summary['results'].append(result_dict)

        return summary

    def save_results(self, summary: Dict, prefix: str = "cross_validation"):
        """Save validation results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{prefix}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"\nResults saved to: {filename}")
        return filename

    def generate_report(self, summary: Dict) -> str:
        """Generate human-readable validation report."""
        report = []
        report.append("=" * 70)
        report.append("M4 CROSS-VALIDATION REPORT")
        report.append(f"Generated: {summary['metadata']['timestamp']}")
        report.append("=" * 70)
        report.append("")

        # Summary
        s = summary['summary']
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Total candidates:    {s['total_sequences']}")
        report.append(f"VALIDATED:           {s['validated']} ({s['validation_rate']*100:.1f}%)")
        report.append(f"FLAGGED:             {s['flagged']}")
        report.append(f"REJECTED:            {s['rejected']}")
        report.append(f"Mean score:          {s['mean_aggregate_score']:.1f}/100")
        report.append("")

        # Layer pass rates
        report.append("LAYER PASS RATES")
        report.append("-" * 70)
        lpr = s['layer_pass_rates']
        report.append(f"RMSD Consensus:      {lpr['rmsd_consensus']*100:.1f}%")
        report.append(f"Stereochemical QA:   {lpr['stereochemical_qa']*100:.1f}%")
        report.append(f"Thermal Stress:      {lpr['thermal_stress']*100:.1f}%")
        report.append("")

        # Individual results
        report.append("INDIVIDUAL RESULTS")
        report.append("-" * 70)

        for i, r in enumerate(summary['results'], 1):
            verdict = r['final_verdict']
            seq = r['sequence'][:35] + "..." if len(r['sequence']) > 35 else r['sequence']

            report.append(f"\n{i}. {seq}")
            report.append(f"   Verdict: {verdict} | Score: {r['aggregate_score']:.1f}/100 | Layers: {r['layers_passed']}/3")

            # Layer details
            layers = r['layer_results']

            # RMSD
            rmsd = layers['rmsd_consensus']
            rmsd_status = "PASS" if rmsd['passed'] else "FAIL"
            report.append(f"   [1] RMSD Consensus: {rmsd_status} (RMSD={rmsd['details']['rmsd']:.2f} Å)")

            # Stereo
            stereo = layers['stereochemical_qa']
            stereo_status = "PASS" if stereo['passed'] else "FAIL"
            report.append(f"   [2] Stereochemical: {stereo_status} (Rama={stereo['details']['rama_favored_pct']:.1f}% favored)")

            # Thermal
            thermal = layers['thermal_stress']
            thermal_status = "PASS" if thermal['passed'] else "FAIL"
            report.append(f"   [3] Thermal Stress: {thermal_status} (H-bond retention={thermal['details']['hbond_retention']:.1f}%)")

            # Failures
            all_failures = (
                rmsd['failure_reasons'] +
                stereo['failure_reasons'] +
                thermal['failure_reasons']
            )
            if all_failures:
                report.append(f"   Failures: {'; '.join(all_failures[:3])}")

        report.append("")
        report.append("=" * 70)
        report.append("INTERPRETATION")
        report.append("-" * 70)
        report.append("VALIDATED: Passed all 3 layers. Safe for synthesis consideration.")
        report.append("FLAGGED:   Passed 2/3 layers. Investigate before proceeding.")
        report.append("REJECTED:  Passed 0-1 layers. Likely computational artifact.")
        report.append("")
        report.append("WARNING: Even VALIDATED candidates require experimental verification:")
        report.append("  1. Peptide synthesis (SPPS or recombinant)")
        report.append("  2. Biophysical characterization (CD, NMR, X-ray)")
        report.append("  3. In vitro activity assays")
        report.append("  4. ADMET/toxicity screening")
        report.append("  5. In vivo efficacy studies")
        report.append("=" * 70)

        return "\n".join(report)


def load_sequences_from_fasta(fasta_path: Path) -> List[str]:
    """Load sequences from FASTA file."""
    sequences = []
    current_seq = []

    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>') or line.startswith('#'):
                if current_seq:
                    sequences.append(''.join(current_seq))
                    current_seq = []
            elif line:
                current_seq.append(line)

        if current_seq:
            sequences.append(''.join(current_seq))

    return sequences


def main():
    """Run cross-validation pipeline on peptide candidates."""
    print("=" * 70)
    print("M4 CROSS-VALIDATION CONTROLLER")
    print("Three-Layer Defense Against Computational Hallucinations")
    print("=" * 70)
    print()
    print("Validation Layers:")
    print("  1. RMSD Consensus (ESMFold vs AlphaFold2)")
    print("  2. Stereochemical QA (Ramachandran + Steric Clashes)")
    print("  3. Thermal Stress MD (350K Stability)")
    print()

    # Initialize controller
    output_dir = Path(__file__).parent / "validation_results"
    controller = CrossValidationController(output_dir)

    # Collect sequences
    all_sequences = []

    # Look for FASTA files
    search_paths = [
        Path(__file__).parent.parent / "prolactinoma" / "peptides",
        Path(__file__).parent.parent.parent / "cftr_chaperones",
    ]

    for search_path in search_paths:
        if search_path.exists():
            for fasta in search_path.glob("*.fasta"):
                print(f"Loading sequences from: {fasta}")
                seqs = load_sequences_from_fasta(fasta)
                all_sequences.extend(seqs[:3])  # Only top 3 (full validation is slow)
                print(f"  Loaded {len(seqs)} sequences, using top 3 for full validation")

    if not all_sequences:
        print("No peptide files found, using example sequences...")
        all_sequences = [
            "CRGWYSSWVIINVSC",      # D2R agonist
            "YLSVTTAEVVATSTLLSF",   # CFTR chaperone
        ]

    print()
    print(f"Total sequences for cross-validation: {len(all_sequences)}")
    print("-" * 70)

    # Run cross-validation
    summary = controller.validate_batch(all_sequences)

    # Generate and print report
    report = controller.generate_report(summary)
    print(report)

    # Save results
    output_file = controller.save_results(summary)

    # Save report as text
    report_file = output_dir / f"cross_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()
