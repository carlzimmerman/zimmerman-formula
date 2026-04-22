#!/usr/bin/env python3
"""
batch_runner.py - Batch Pipeline Runner for Multiple Disease Targets

Runs the validated pipeline across multiple disease targets in sequence,
with proper error handling, progress tracking, and summary reporting.

Usage:
    python batch_runner.py --all
    python batch_runner.py --targets P37840 P10636 P04578
    python batch_runner.py --diseases parkinsons alzheimers hiv

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import time
import traceback
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import argparse

# Import pipeline modules
from m01_target_research import TargetResearcher
from m04_peptide_design import PeptideDesigner
from m05_structure_prediction import StructurePredictor


@dataclass
class DiseaseTarget:
    """Definition of a disease target for the pipeline."""
    disease_name: str
    target_name: str
    uniprot_id: str
    therapeutic_goal: str
    priority: int = 1  # 1 = highest


# Master list of disease targets
DISEASE_TARGETS = {
    # Neurodegenerative
    'parkinsons': DiseaseTarget(
        disease_name="Parkinson's Disease",
        target_name="Alpha-synuclein",
        uniprot_id="P37840",
        therapeutic_goal="Prevent aggregation, reduce Lewy body formation",
        priority=1
    ),
    'alzheimers': DiseaseTarget(
        disease_name="Alzheimer's Disease",
        target_name="Tau protein",
        uniprot_id="P10636",
        therapeutic_goal="Prevent tau tangles, stabilize microtubules",
        priority=1
    ),
    'huntingtons': DiseaseTarget(
        disease_name="Huntington's Disease",
        target_name="Huntingtin",
        uniprot_id="P42858",
        therapeutic_goal="Reduce polyQ aggregation",
        priority=2
    ),

    # Infectious Disease
    'hiv': DiseaseTarget(
        disease_name="HIV/AIDS",
        target_name="Envelope glycoprotein gp120",
        uniprot_id="P04578",
        therapeutic_goal="Block CD4 binding, prevent viral entry",
        priority=1
    ),
    'covid': DiseaseTarget(
        disease_name="COVID-19",
        target_name="Spike protein RBD",
        uniprot_id="P0DTC2",
        therapeutic_goal="Block ACE2 binding",
        priority=2
    ),

    # Women's Health
    'childbirth': DiseaseTarget(
        disease_name="Labor/Childbirth",
        target_name="Oxytocin receptor",
        uniprot_id="P30559",
        therapeutic_goal="Modulate uterine contractions",
        priority=1
    ),
    'preeclampsia': DiseaseTarget(
        disease_name="Preeclampsia",
        target_name="sFlt-1 (VEGFR1)",
        uniprot_id="P17948",
        therapeutic_goal="Restore angiogenic balance",
        priority=2
    ),

    # Cancer
    'cancer_myc': DiseaseTarget(
        disease_name="Cancer (MYC-driven)",
        target_name="c-Myc",
        uniprot_id="P01106",
        therapeutic_goal="Disrupt MYC-MAX dimerization",
        priority=2
    ),

    # Autoimmune
    'rheumatoid': DiseaseTarget(
        disease_name="Rheumatoid Arthritis",
        target_name="TNF-alpha",
        uniprot_id="P01375",
        therapeutic_goal="Block TNF receptor binding",
        priority=2
    ),

    # Metabolic
    'diabetes': DiseaseTarget(
        disease_name="Type 2 Diabetes",
        target_name="GLP-1 receptor",
        uniprot_id="P43220",
        therapeutic_goal="Enhance insulin secretion",
        priority=2
    ),
}


@dataclass
class PipelineResult:
    """Results from running pipeline on one target."""
    disease_name: str
    target_name: str
    uniprot_id: str

    # Status
    success: bool
    error_message: Optional[str] = None

    # Module completion
    m01_complete: bool = False
    m04_complete: bool = False
    m05_complete: bool = False

    # Results
    n_designed: int = 0
    n_controls: int = 0
    n_structures_passed: int = 0
    designed_pass_rate: float = 0.0
    control_pass_rate: float = 0.0

    # Top candidates
    top_candidates: List[Dict] = None

    # Timing
    runtime_seconds: float = 0.0

    def __post_init__(self):
        if self.top_candidates is None:
            self.top_candidates = []


class BatchRunner:
    """
    Runs the validated pipeline across multiple disease targets.

    Features:
    - Sequential processing with error isolation
    - Progress tracking and resumption
    - Comprehensive summary reporting
    - Rate limiting for API calls
    """

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.projects_dir = self.base_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[PipelineResult] = []

    def run_targets(
        self,
        targets: List[DiseaseTarget],
        n_designed: int = 20,
        n_controls: int = 100,
        api_delay: float = 2.0
    ) -> List[PipelineResult]:
        """
        Run pipeline on multiple targets.

        Args:
            targets: List of DiseaseTarget objects
            n_designed: Number of designed peptides per target
            n_controls: Number of random control peptides
            api_delay: Delay between API calls (seconds)
        """
        print("\n" + "="*70)
        print("BATCH PIPELINE RUNNER")
        print("="*70)
        print(f"    Targets: {len(targets)}")
        print(f"    Peptides per target: {n_designed} designed + {n_controls} controls")
        print(f"    API delay: {api_delay}s")

        for i, target in enumerate(targets):
            print(f"\n{'━'*70}")
            print(f"[{i+1}/{len(targets)}] {target.disease_name}")
            print(f"    Target: {target.target_name} ({target.uniprot_id})")
            print(f"    Goal: {target.therapeutic_goal}")
            print(f"{'━'*70}")

            result = self._run_single_target(
                target, n_designed, n_controls, api_delay
            )
            self.results.append(result)

            # Brief summary
            if result.success:
                print(f"\n    ✓ Complete: {result.n_structures_passed} structures passed")
                print(f"      Designed: {result.designed_pass_rate:.1%} pass rate")
                print(f"      Controls: {result.control_pass_rate:.1%} pass rate")
            else:
                print(f"\n    ✗ Failed: {result.error_message}")

            # Delay between targets
            if i < len(targets) - 1:
                print(f"\n    Waiting {api_delay}s before next target...")
                time.sleep(api_delay)

        # Final summary
        self._print_summary()
        self._save_results()

        return self.results

    def _run_single_target(
        self,
        target: DiseaseTarget,
        n_designed: int,
        n_controls: int,
        api_delay: float
    ) -> PipelineResult:
        """Run pipeline on a single target with error handling."""
        start_time = time.time()

        result = PipelineResult(
            disease_name=target.disease_name,
            target_name=target.target_name,
            uniprot_id=target.uniprot_id,
            success=False
        )

        try:
            # Generate project ID
            project_id = f"{target.target_name.upper().replace(' ', '_')[:10]}_{target.uniprot_id}"
            project_dir = self.projects_dir / project_id
            project_dir.mkdir(parents=True, exist_ok=True)

            # MODULE 1: Target Research
            print("\n    [M01] Target Research...")
            researcher = TargetResearcher(project_dir / "target_research")
            profile = researcher.research_target(target.uniprot_id)
            result.m01_complete = True

            # MODULE 4: Peptide Design
            print("\n    [M04] Peptide Design...")
            designer = PeptideDesigner(
                output_dir=project_dir / "peptide_designs",
                project_id=project_id.split('_')[0]
            )
            design_result = designer.design_peptides(
                target_uniprot=target.uniprot_id,
                n_designed=n_designed,
                n_controls=n_controls,
                length_range=(4, 10),
                design_strategy=f"Constraint-based for {target.therapeutic_goal}",
            )
            result.m04_complete = True
            result.n_designed = n_designed
            result.n_controls = n_controls

            # MODULE 5: Structure Prediction
            print("\n    [M05] Structure Prediction...")
            predictor = StructurePredictor(project_dir / "structures")

            peptides = design_result.designed_peptides + design_result.control_peptides
            predictions = predictor.predict_structures(peptides, batch_delay=api_delay)
            result.m05_complete = True

            # Analyze results with corrected threshold
            THRESHOLD = 0.70
            designed_passing = [p for p in predictions
                              if p.peptide_id.startswith('ZIM') and p.plddt_mean >= THRESHOLD]
            control_passing = [p for p in predictions
                             if p.peptide_id.startswith('CTRL') and p.success and p.plddt_mean >= THRESHOLD]

            successful_controls = [p for p in predictions if p.peptide_id.startswith('CTRL') and p.success]

            result.n_structures_passed = len(designed_passing) + len(control_passing)
            result.designed_pass_rate = len(designed_passing) / n_designed if n_designed > 0 else 0
            result.control_pass_rate = len(control_passing) / len(successful_controls) if successful_controls else 0

            # Get top candidates
            all_passing = designed_passing + control_passing
            sorted_candidates = sorted(all_passing, key=lambda x: x.plddt_mean, reverse=True)
            result.top_candidates = [
                {"id": p.peptide_id, "sequence": p.sequence, "plddt": p.plddt_mean}
                for p in sorted_candidates[:5]
            ]

            result.success = True

        except Exception as e:
            result.error_message = str(e)
            print(f"\n    ERROR: {e}")
            traceback.print_exc()

        result.runtime_seconds = time.time() - start_time
        return result

    def _print_summary(self) -> None:
        """Print summary of all pipeline runs."""
        print("\n" + "="*70)
        print("BATCH PIPELINE SUMMARY")
        print("="*70)

        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]

        print(f"\n    Total targets: {len(self.results)}")
        print(f"    Successful: {len(successful)}")
        print(f"    Failed: {len(failed)}")

        if successful:
            print(f"\n    SUCCESSFUL TARGETS:")
            print(f"    {'Disease':<25} {'Pass Rate (D)':<15} {'Pass Rate (C)':<15} {'Top Candidate'}")
            print(f"    {'-'*70}")
            for r in successful:
                top = r.top_candidates[0] if r.top_candidates else {"sequence": "N/A", "plddt": 0}
                print(f"    {r.disease_name:<25} {r.designed_pass_rate:>12.1%}   {r.control_pass_rate:>12.1%}   {top['sequence']} ({top['plddt']:.2f})")

        if failed:
            print(f"\n    FAILED TARGETS:")
            for r in failed:
                print(f"    {r.disease_name}: {r.error_message}")

        # Statistical comparison
        if len(successful) >= 2:
            print(f"\n    CROSS-DISEASE ANALYSIS:")
            print(f"    {'─'*50}")

            # Are designed peptides better than controls across diseases?
            designed_rates = [r.designed_pass_rate for r in successful]
            control_rates = [r.control_pass_rate for r in successful]

            avg_designed = sum(designed_rates) / len(designed_rates)
            avg_control = sum(control_rates) / len(control_rates)

            print(f"    Avg designed pass rate: {avg_designed:.1%}")
            print(f"    Avg control pass rate:  {avg_control:.1%}")

            if avg_designed > avg_control + 0.1:
                print(f"    → SIGNAL: Designed peptides show {(avg_designed - avg_control)*100:.1f}pp advantage")
            else:
                print(f"    → NO SIGNAL: Design strategy not outperforming random")

    def _save_results(self) -> None:
        """Save batch results to JSON."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_targets': len(self.results),
            'successful': len([r for r in self.results if r.success]),
            'results': [asdict(r) for r in self.results]
        }

        output_path = self.base_dir / "batch_results.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2, default=str)

        print(f"\n    Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch pipeline runner for multiple disease targets"
    )

    parser.add_argument("--all", action="store_true",
                       help="Run all defined disease targets")
    parser.add_argument("--priority1", action="store_true",
                       help="Run only priority 1 targets")
    parser.add_argument("--diseases", nargs="+",
                       choices=list(DISEASE_TARGETS.keys()),
                       help="Specific diseases to run")
    parser.add_argument("--targets", nargs="+",
                       help="UniProt IDs to run")
    parser.add_argument("--n-designed", type=int, default=20,
                       help="Number of designed peptides per target")
    parser.add_argument("--n-controls", type=int, default=100,
                       help="Number of control peptides per target")
    parser.add_argument("--api-delay", type=float, default=1.5,
                       help="Delay between ESMFold API calls (seconds)")
    parser.add_argument("--list", action="store_true",
                       help="List available disease targets")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable Disease Targets:")
        print("-"*70)
        for key, target in DISEASE_TARGETS.items():
            print(f"  {key:<15} {target.disease_name:<30} {target.uniprot_id} (P{target.priority})")
        return

    # Select targets
    targets = []
    if args.all:
        targets = list(DISEASE_TARGETS.values())
    elif args.priority1:
        targets = [t for t in DISEASE_TARGETS.values() if t.priority == 1]
    elif args.diseases:
        targets = [DISEASE_TARGETS[d] for d in args.diseases]
    elif args.targets:
        # Create custom targets from UniProt IDs
        for uid in args.targets:
            targets.append(DiseaseTarget(
                disease_name=f"Custom ({uid})",
                target_name=uid,
                uniprot_id=uid,
                therapeutic_goal="Custom target analysis"
            ))
    else:
        # Default: priority 1 targets
        targets = [t for t in DISEASE_TARGETS.values() if t.priority == 1]

    if not targets:
        print("No targets selected. Use --list to see available targets.")
        return

    # Run batch
    base_dir = Path(__file__).parent.parent
    runner = BatchRunner(base_dir)

    results = runner.run_targets(
        targets=targets,
        n_designed=args.n_designed,
        n_controls=args.n_controls,
        api_delay=args.api_delay
    )

    return results


if __name__ == "__main__":
    main()
