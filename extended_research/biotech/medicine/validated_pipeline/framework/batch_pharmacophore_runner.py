#!/usr/bin/env python3
"""
batch_pharmacophore_runner.py - Run Z² Pharmacophore Design Across All Targets

Executes the validated pharmacophore design pipeline on multiple target system targets
and generates a cross-target system comparison report.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import numpy as np

from m04b_pharmacophore_design import PharmacophoreDesigner
from sys_02_pharmacophore_verification import PharmacophoreVerifier


@dataclass
class TargetConfig:
    """Configuration for a target system target."""
    disease_name: str
    target_name: str
    uniprot_id: str
    pdb_file: str
    therapeutic_goal: str


# target system targets with their PDB structures
# NOTE: target_name[:10].upper() must match existing project directory names
TARGETS = [
    TargetConfig(
        disease_name="Parkinson's target system",
        target_name="Alpha-synu",  # → ALPHA-SYNU_P37840
        uniprot_id="P37840",
        pdb_file="1XQ8.pdb",
        therapeutic_goal="Prevent aggregation, reduce Lewy bodies"
    ),
    TargetConfig(
        disease_name="Alzheimer's target system",
        target_name="Tau protei",  # → TAU_PROTEI_P10636
        uniprot_id="P10636",
        pdb_file="5O3L.pdb",
        therapeutic_goal="Prevent tau tangles, stabilize microtubules"
    ),
    TargetConfig(
        disease_name="C2_Homodimer_A/AIDS",
        target_name="Envelope g",  # → ENVELOPE_G_P04578 (gp120)
        uniprot_id="P04578",
        pdb_file="3JWD.pdb",
        therapeutic_goal="Block CD4 binding, prevent target macromolecule entry"
    ),
    TargetConfig(
        disease_name="Labor/Childbirth",
        target_name="Oxytocin r",  # → OXYTOCIN_R_P30559
        uniprot_id="P30559",
        pdb_file="6TPK.pdb",
        therapeutic_goal="Modulate uterine contractions"
    ),
]


@dataclass
class TargetResult:
    """Results for one target."""
    disease_name: str
    target_name: str
    uniprot_id: str

    # Design results
    n_designs: int
    top_sequence: str
    top_geometric_score: float

    # Verification results
    pharm_stability_rate: float
    ctrl_stability_rate: float
    pharm_avg_affinity: float
    ctrl_avg_affinity: float
    improvement_factor: float
    pharmacophore_wins: bool

    # Top candidates
    top_candidates: List[Dict]

    # Status
    success: bool
    error: Optional[str] = None


def run_pharmacophore_pipeline(
    target: TargetConfig,
    base_dir: Path,
    n_designs: int = 20,
    n_controls: int = 10,
    top_n_verify: int = 5
) -> TargetResult:
    """Run full pharmacophore pipeline on one target."""

    print(f"\n{'='*70}")
    print(f"TARGET: {target.disease_name}")
    print(f"{'='*70}")
    print(f"    Protein: {target.target_name} ({target.uniprot_id})")
    print(f"    PDB: {target.pdb_file}")
    print(f"    Goal: {target.therapeutic_goal}")

    # Set up paths
    project_id = f"{target.target_name.upper().replace(' ', '_')[:10]}_{target.uniprot_id}"
    project_dir = base_dir / "projects" / project_id
    pdb_path = project_dir / "target_structure" / target.pdb_file

    if not pdb_path.exists():
        return TargetResult(
            disease_name=target.disease_name,
            target_name=target.target_name,
            uniprot_id=target.uniprot_id,
            n_designs=0,
            top_sequence="",
            top_geometric_score=0.0,
            pharm_stability_rate=0.0,
            ctrl_stability_rate=0.0,
            pharm_avg_affinity=0.0,
            ctrl_avg_affinity=0.0,
            improvement_factor=0.0,
            pharmacophore_wins=False,
            top_candidates=[],
            success=False,
            error=f"PDB not found: {pdb_path}"
        )

    try:
        # Step 1: Pharmacophore Design
        print(f"\n[1/2] Running pharmacophore design...")
        designer = PharmacophoreDesigner(project_dir / "pharmacophore_designs")
        designs = designer.design_peptides(
            pdb_path=str(pdb_path),
            target_uniprot=target.uniprot_id,
            n_peptides=n_designs
        )

        # Step 2: Verification
        print(f"\n[2/2] Running verification...")
        verifier = PharmacophoreVerifier(project_dir / "verification")

        # Prepare designs for verification
        design_dicts = [
            {
                'peptide_id': d.peptide_id,
                'sequence': d.sequence,
                'geometric_score': d.geometric_score
            }
            for d in designs[:top_n_verify]
        ]

        report = verifier.verify_designs(
            pharmacophore_designs=design_dicts,
            target_pdb=str(pdb_path),
            target_uniprot=target.uniprot_id,
            n_controls=n_controls
        )

        # Extract top candidates
        all_results = report.pharmacophore_results + report.control_results
        top_candidates = sorted(all_results, key=lambda x: x.combined_rank)[:5]

        return TargetResult(
            disease_name=target.disease_name,
            target_name=target.target_name,
            uniprot_id=target.uniprot_id,
            n_designs=len(designs),
            top_sequence=designs[0].sequence if designs else "",
            top_geometric_score=designs[0].geometric_score if designs else 0.0,
            pharm_stability_rate=report.pharm_stability_rate,
            ctrl_stability_rate=report.ctrl_stability_rate,
            pharm_avg_affinity=report.pharm_avg_affinity,
            ctrl_avg_affinity=report.ctrl_avg_affinity,
            improvement_factor=report.improvement_factor,
            pharmacophore_wins=report.pharmacophore_wins,
            top_candidates=[
                {
                    'id': c.peptide_id,
                    'sequence': c.sequence,
                    'plddt': c.plddt_mean,
                    'binding': c.binding_estimate,
                    'type': c.design_type
                }
                for c in top_candidates
            ],
            success=True
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return TargetResult(
            disease_name=target.disease_name,
            target_name=target.target_name,
            uniprot_id=target.uniprot_id,
            n_designs=0,
            top_sequence="",
            top_geometric_score=0.0,
            pharm_stability_rate=0.0,
            ctrl_stability_rate=0.0,
            pharm_avg_affinity=0.0,
            ctrl_avg_affinity=0.0,
            improvement_factor=0.0,
            pharmacophore_wins=False,
            top_candidates=[],
            success=False,
            error=str(e)
        )


def print_summary(results: List[TargetResult]) -> None:
    """Print cross-target system summary."""
    print(f"\n{'='*70}")
    print("CROSS-target system PHARMACOPHORE ANALYSIS")
    print(f"{'='*70}")

    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    print(f"\n    Targets processed: {len(results)}")
    print(f"    Successful: {len(successful)}")
    print(f"    Failed: {len(failed)}")

    if successful:
        print(f"\n    {'target system':<25} {'Pharm %':<10} {'Ctrl %':<10} {'Improve':<10} {'Winner'}")
        print(f"    {'-'*65}")

        for r in successful:
            winner = "PHARM" if r.pharmacophore_wins else "CTRL"
            print(f"    {r.disease_name:<25} {r.pharm_stability_rate:>7.1%}   {r.ctrl_stability_rate:>7.1%}   {r.improvement_factor:>7.2f}x   {winner}")

        # Aggregate statistics
        avg_pharm = np.mean([r.pharm_stability_rate for r in successful])
        avg_ctrl = np.mean([r.ctrl_stability_rate for r in successful])
        avg_improve = np.mean([r.improvement_factor for r in successful])
        wins = sum(1 for r in successful if r.pharmacophore_wins)

        print(f"    {'-'*65}")
        print(f"    {'AVERAGE':<25} {avg_pharm:>7.1%}   {avg_ctrl:>7.1%}   {avg_improve:>7.2f}x   {wins}/{len(successful)}")

        print(f"\n    TOP CANDIDATES ACROSS ALL DISEASES:")
        print(f"    {'─'*60}")
        print(f"    {'target system':<20} {'ID':<18} {'Sequence':<12} {'pLDDT':<8} {'Binding'}")
        print(f"    {'-'*60}")

        for r in successful:
            if r.top_candidates:
                top = r.top_candidates[0]
                print(f"    {r.disease_name[:20]:<20} {top['id']:<18} {top['sequence']:<12} {top['plddt']:.2f}    {top['binding']:.3f}")

    if failed:
        print(f"\n    FAILED TARGETS:")
        for r in failed:
            print(f"    {r.disease_name}: {r.error}")

    # Final verdict
    print(f"\n    {'='*60}")
    if successful:
        if all(r.pharmacophore_wins for r in successful):
            print(f"    ✓ Z² PHARMACOPHORE DESIGN VALIDATED ACROSS ALL TARGETS")
        elif wins > len(successful) / 2:
            print(f"    ✓ Z² PHARMACOPHORE DESIGN VALIDATED ({wins}/{len(successful)} targets)")
        else:
            print(f"    ✗ Z² PHARMACOPHORE DESIGN NEEDS REFINEMENT ({wins}/{len(successful)} targets)")
    print(f"    {'='*60}")


def save_results(results: List[TargetResult], output_dir: Path) -> None:
    """Save results to JSON."""
    output = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Z² Pharmacophore Design',
        'z2_distance': 6.015152508891966,
        'n_targets': len(results),
        'n_successful': sum(1 for r in results if r.success),
        'results': [asdict(r) for r in results]
    }

    output_path = output_dir / "pharmacophore_batch_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n    Saved: {output_path}")


def main():
    """Run pharmacophore pipeline on all targets."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--n-designs", type=int, default=20)
    parser.add_argument("--n-controls", type=int, default=10)
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--targets", nargs="+", help="Specific UniProt IDs to run")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent

    # Filter targets if specified
    targets = TARGETS
    if args.targets:
        targets = [t for t in TARGETS if t.uniprot_id in args.targets]

    print(f"\n{'='*70}")
    print("Z² PHARMACOPHORE BATCH RUNNER")
    print(f"{'='*70}")
    print(f"    Targets: {len(targets)}")
    print(f"    Designs per target: {args.n_designs}")
    print(f"    Controls per target: {args.n_controls}")
    print(f"    Z² interaction distance: 6.015152508891966 Å (precise)")

    results = []
    for i, target in enumerate(targets):
        print(f"\n[{i+1}/{len(targets)}] Processing {target.disease_name}...")
        result = run_pharmacophore_pipeline(
            target=target,
            base_dir=base_dir,
            n_designs=args.n_designs,
            n_controls=args.n_controls,
            top_n_verify=args.top_n
        )
        results.append(result)

        # Brief delay between targets
        if i < len(targets) - 1:
            time.sleep(2)

    # Summary
    print_summary(results)
    save_results(results, base_dir)

    return results


if __name__ == "__main__":
    main()
