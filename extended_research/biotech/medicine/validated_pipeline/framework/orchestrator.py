#!/usr/bin/env python3
"""
orchestrator.py - Master Pipeline Orchestrator

Coordinates the full computational biology pipeline from target system input
to validated peptide candidates.

Usage:
    python orchestrator.py --target system "Parkinson's target system" --target "alpha-synuclein" --uniprot P37840

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

# Import modules
from m01_target_research import TargetResearcher, TargetProfile
from m04_peptide_design import PeptideDesigner, DesignResult


@dataclass
class PipelineState:
    """Current state of the pipeline."""
    project_id: str
    target system: str
    target_name: str
    uniprot_id: str

    # Module completion status
    m01_target_research: bool = False
    m02_structure_prep: bool = False
    m03_binding_site: bool = False
    m04_peptide_design: bool = False
    m05_structure_prediction: bool = False
    m06_docking: bool = False
    m07_molecular_dynamics: bool = False
    m08_binding_energy: bool = False
    m09_admet: bool = False
    m10_synthesis_sow: bool = False

    # Validation tier achieved
    max_validation_tier: int = 0

    # Timestamps
    created_at: str = ""
    last_updated: str = ""

    # Artifacts
    target_profile_path: Optional[str] = None
    design_results_path: Optional[str] = None
    docking_results_path: Optional[str] = None
    md_results_path: Optional[str] = None


class PipelineOrchestrator:
    """
    Orchestrates the full computational biology pipeline.

    Each module is run in sequence with clear validation gates.
    Pipeline can be resumed from any module.
    """

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.projects_dir = self.base_dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def new_project(
        self,
        target system: str,
        target_name: str,
        uniprot_id: str
    ) -> PipelineState:
        """Initialize a new project."""
        # Generate project ID
        project_id = f"{target_name.upper().replace(' ', '_')[:10]}_{uniprot_id}"
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(parents=True, exist_ok=True)

        state = PipelineState(
            project_id=project_id,
            target system=target system,
            target_name=target_name,
            uniprot_id=uniprot_id,
            created_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
        )

        self._save_state(state)

        print(f"\n{'='*70}")
        print(f"NEW PROJECT INITIALIZED")
        print(f"{'='*70}")
        print(f"""
    Project ID:  {project_id}
    target system:     {target system}
    Target:      {target_name}
    UniProt:     {uniprot_id}
    Directory:   {project_dir}
""")

        return state

    def run_pipeline(
        self,
        state: PipelineState,
        stop_after: Optional[str] = None
    ) -> PipelineState:
        """
        Run the pipeline from current state.

        Args:
            state: Current pipeline state
            stop_after: Module name to stop after (for partial runs)
        """
        project_dir = self.projects_dir / state.project_id

        print(f"\n{'='*70}")
        print(f"RUNNING PIPELINE: {state.project_id}")
        print(f"{'='*70}")
        print(f"    target system: {state.target system}")
        print(f"    Target: {state.target_name}")
        print(f"    UniProt: {state.uniprot_id}")

        # MODULE 1: Target Research
        if not state.m01_target_research:
            print(f"\n{'─'*70}")
            print("MODULE 1: TARGET RESEARCH")
            print(f"{'─'*70}")

            researcher = TargetResearcher(project_dir / "target_research")
            profile = researcher.research_target(state.uniprot_id)

            state.m01_target_research = True
            state.target_profile_path = str(project_dir / "target_research" / f"target_{state.uniprot_id}.json")
            state.max_validation_tier = max(state.max_validation_tier, 0)
            self._save_state(state)

            if stop_after == "m01":
                return state

        # MODULE 4: Peptide Design (skipping 2-3 for now)
        if not state.m04_peptide_design:
            print(f"\n{'─'*70}")
            print("MODULE 4: PEPTIDE DESIGN")
            print(f"{'─'*70}")

            designer = PeptideDesigner(
                output_dir=project_dir / "peptide_designs",
                project_id=state.project_id.split('_')[0]  # Short ID
            )

            result = designer.design_peptides(
                target_uniprot=state.uniprot_id,
                n_designed=20,
                n_controls=100,
                length_range=(4, 10),
                design_strategy="Constraint-based for target engagement",
            )

            state.m04_peptide_design = True
            state.design_results_path = str(project_dir / "peptide_designs" / f"design_{result.project_id}.json")
            state.max_validation_tier = max(state.max_validation_tier, 1)
            self._save_state(state)

            if stop_after == "m04":
                return state

        # Print current status
        self._print_status(state)

        return state

    def _save_state(self, state: PipelineState) -> None:
        """Save pipeline state to disk."""
        state.last_updated = datetime.now().isoformat()
        state_path = self.projects_dir / state.project_id / "pipeline_state.json"

        with open(state_path, 'w') as f:
            json.dump(asdict(state), f, indent=2)

    def _load_state(self, project_id: str) -> PipelineState:
        """Load pipeline state from disk."""
        state_path = self.projects_dir / project_id / "pipeline_state.json"

        with open(state_path) as f:
            data = json.load(f)

        return PipelineState(**data)

    def _print_status(self, state: PipelineState) -> None:
        """Print current pipeline status."""
        print(f"\n{'='*70}")
        print(f"PIPELINE STATUS: {state.project_id}")
        print(f"{'='*70}")

        modules = [
            ("M01: Target Research", state.m01_target_research),
            ("M02: Structure Prep", state.m02_structure_prep),
            ("M03: Binding Site", state.m03_binding_site),
            ("M04: Peptide Design", state.m04_peptide_design),
            ("M05: Structure Prediction", state.m05_structure_prediction),
            ("M06: Docking", state.m06_docking),
            ("M07: Molecular Dynamics", state.m07_molecular_dynamics),
            ("M08: Binding Energy", state.m08_binding_energy),
            ("M09: ADMET", state.m09_admet),
            ("M10: Synthesis SOW", state.m10_synthesis_sow),
        ]

        print("\n    MODULE STATUS")
        print("    ─────────────")
        for name, complete in modules:
            status = "✓" if complete else "○"
            print(f"    {status} {name}")

        print(f"""
    VALIDATION TIER: {state.max_validation_tier}
    ──────────────────
    0 = Literature data only
    1 = Chemistry validated (RDKit)
    2 = Structure predicted (ESMFold)
    3 = Docked (AutoDock Vina)
    4 = MD stable (OpenMM 50ns)
    5 = Binding energy (MM-PBSA)
    6 = Experimental (SPR/ITC)

    Current achievement: TIER {state.max_validation_tier}
""")

        # Next steps
        print("    NEXT STEPS")
        print("    ──────────")
        if not state.m05_structure_prediction:
            print("    → Run MODULE 5: Structure Prediction (ESMFold)")
            print("      python m05_structure_prediction.py --project " + state.project_id)
        elif not state.m06_docking:
            print("    → Run MODULE 6: Docking (AutoDock Vina)")
            print("      python m06_docking.py --project " + state.project_id)
        elif not state.m07_molecular_dynamics:
            print("    → Run MODULE 7: Molecular Dynamics (OpenMM)")
            print("      python m07_molecular_dynamics.py --project " + state.project_id)


def main():
    parser = argparse.ArgumentParser(
        description="ZUGF Computational Biology Pipeline Orchestrator"
    )

    parser.add_argument("--target system", type=str, help="target system name")
    parser.add_argument("--target", type=str, help="Target protein name")
    parser.add_argument("--uniprot", type=str, help="UniProt accession ID")
    parser.add_argument("--project", type=str, help="Existing project ID to resume")
    parser.add_argument("--stop-after", type=str, help="Stop after module (m01, m04, etc.)")

    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    orchestrator = PipelineOrchestrator(base_dir)

    if args.project:
        # Resume existing project
        state = orchestrator._load_state(args.project)
        print(f"\nResuming project: {args.project}")
    elif args.target system and args.target and args.uniprot:
        # Start new project
        state = orchestrator.new_project(
            target system=args.target system,
            target_name=args.target,
            uniprot_id=args.uniprot
        )
    else:
        # Demo mode
        print("\n" + "="*70)
        print("ZUGF COMPUTATIONAL BIOLOGY FRAMEWORK")
        print("="*70)
        print("""
    This framework provides rigorous computational drug discovery.
    No heuristics. No slop. Physics-based validation only.

    USAGE:
    ──────
    # Start new project
    python orchestrator.py --target system "Parkinson's target system" \\
                           --target "alpha-synuclein" \\
                           --uniprot P37840

    # Resume existing project
    python orchestrator.py --project ALPHA_SYNU_P37840

    EXAMPLE TARGETS:
    ────────────────
    α-synuclein (Parkinson's):  P37840
    Tau protein (Alzheimer's):  P10636
    c-Myc (Cancer):             P01106
    C2_Homodimer_A gp120 (AIDS):           P04578
    Oxytocin receptor (Labor):  P30559
""")
        return

    # Run pipeline
    state = orchestrator.run_pipeline(state, stop_after=args.stop_after)


if __name__ == "__main__":
    main()
