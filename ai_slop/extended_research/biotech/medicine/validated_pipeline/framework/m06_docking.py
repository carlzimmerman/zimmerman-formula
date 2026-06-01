#!/usr/bin/env python3
"""
m06_docking.py - Molecular Docking with Statistical Validation

Docks peptides to target using AutoDock Vina and compares
designed peptides to random controls.

THE CRITICAL TEST:
If designed peptides don't significantly outperform random controls,
the design strategy is broken and we need to iterate.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import subprocess
import tempfile
import shutil
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import warnings
import numpy as np
from scipy import stats

try:
    from vina import Vina
    HAS_VINA_PYTHON = True
except ImportError:
    HAS_VINA_PYTHON = False


@dataclass
class DockingResult:
    """Result of docking one peptide."""
    peptide_id: str
    sequence: str
    is_designed: bool

    # Docking results
    success: bool
    vina_score: float  # kcal/mol (more negative = better)
    poses_found: int

    # Metadata
    target_pdb: str
    binding_site: Tuple[float, float, float]  # center
    box_size: Tuple[float, float, float]

    validation_tier: int = 3  # TIER 3 if successful


@dataclass
class DockingComparison:
    """Statistical comparison of designed vs control peptides."""
    # Designed peptides
    n_designed: int
    designed_mean: float
    designed_std: float
    designed_best: float

    # Control peptides
    n_controls: int
    control_mean: float
    control_std: float
    control_best: float

    # Statistical test
    t_statistic: float
    p_value: float
    effect_size: float  # Cohen's d

    # Verdict
    designed_better: bool
    statistically_significant: bool  # p < 0.05
    practically_significant: bool    # effect size > 0.5


class MolecularDocker:
    """
    Docks peptides to target and performs statistical comparison.

    Uses AutoDock Vina for docking.
    Compares designed peptides to random controls.
    """

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Check for Vina
        self.vina_available = self._check_vina()
        if not self.vina_available:
            warnings.warn("AutoDock Vina not found. Install with: conda install -c bioconda autodock-vina")

    def _check_vina(self) -> bool:
        """Check if Vina is available."""
        if HAS_VINA_PYTHON:
            return True

        # Check command line
        try:
            result = subprocess.run(
                ["vina", "--version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def dock_peptides(
        self,
        target_pdb: Path,
        peptide_structures: List[Dict],
        binding_center: Tuple[float, float, float],
        box_size: Tuple[float, float, float] = (25.0, 25.0, 25.0),
        exhaustiveness: int = 8
    ) -> Tuple[List[DockingResult], DockingComparison]:
        """
        Dock all peptides and compare designed vs controls.

        Args:
            target_pdb: Path to target protein PDB
            peptide_structures: List with peptide_id, sequence, is_designed, pdb_path
            binding_center: (x, y, z) center of binding site
            box_size: Search box dimensions
            exhaustiveness: Vina exhaustiveness parameter

        Returns:
            Tuple of (docking_results, statistical_comparison)
        """
        print(f"\n{'='*70}")
        print("MOLECULAR DOCKING MODULE")
        print(f"{'='*70}")
        print(f"    Target: {target_pdb}")
        print(f"    Peptides: {len(peptide_structures)}")
        print(f"    Binding site: {binding_center}")
        print(f"    Box size: {box_size}")

        if not self.vina_available:
            print("\n    WARNING: Vina not available. Using mock scores for demonstration.")
            print("    Install Vina for real docking: conda install -c bioconda autodock-vina")

        results = []

        for i, peptide in enumerate(peptide_structures):
            peptide_id = peptide['peptide_id']
            sequence = peptide['sequence']
            is_designed = peptide.get('is_designed', False)
            pdb_path = peptide.get('pdb_path')

            print(f"\n[{i+1}/{len(peptide_structures)}] {peptide_id}: {sequence}")

            if self.vina_available and pdb_path:
                result = self._dock_single_vina(
                    peptide_id, sequence, is_designed,
                    target_pdb, pdb_path,
                    binding_center, box_size, exhaustiveness
                )
            else:
                # Mock docking for demonstration (clearly labeled)
                result = self._mock_dock(
                    peptide_id, sequence, is_designed,
                    str(target_pdb), binding_center, box_size
                )

            results.append(result)

            if result.success:
                status = "designed" if is_designed else "control"
                print(f"    Score: {result.vina_score:.2f} kcal/mol ({status})")
            else:
                print(f"    FAILED")

        # Statistical comparison
        comparison = self._compare_designed_vs_controls(results)

        # Save results
        self._save_results(results, comparison)

        # Print comparison
        self._print_comparison(comparison)

        return results, comparison

    def _dock_single_vina(
        self,
        peptide_id: str,
        sequence: str,
        is_designed: bool,
        target_pdb: Path,
        ligand_pdb: str,
        center: Tuple[float, float, float],
        box_size: Tuple[float, float, float],
        exhaustiveness: int
    ) -> DockingResult:
        """Dock using AutoDock Vina."""
        try:
            if HAS_VINA_PYTHON:
                # Use Python bindings
                v = Vina(sf_name='vina')
                v.set_receptor(str(target_pdb))
                v.set_ligand_from_file(ligand_pdb)
                v.compute_vina_maps(center=center, box_size=box_size)
                v.dock(exhaustiveness=exhaustiveness, n_poses=5)

                score = v.score()[0]
                poses = len(v.poses())

                return DockingResult(
                    peptide_id=peptide_id,
                    sequence=sequence,
                    is_designed=is_designed,
                    success=True,
                    vina_score=score,
                    poses_found=poses,
                    target_pdb=str(target_pdb),
                    binding_site=center,
                    box_size=box_size,
                )
            else:
                # Use command line
                # This would require pdbqt conversion etc.
                raise NotImplementedError("Command-line Vina not implemented yet")

        except Exception as e:
            print(f"    ERROR: {e}")
            return DockingResult(
                peptide_id=peptide_id,
                sequence=sequence,
                is_designed=is_designed,
                success=False,
                vina_score=0.0,
                poses_found=0,
                target_pdb=str(target_pdb),
                binding_site=center,
                box_size=box_size,
            )

    def _mock_dock(
        self,
        peptide_id: str,
        sequence: str,
        is_designed: bool,
        target_pdb: str,
        center: Tuple[float, float, float],
        box_size: Tuple[float, float, float]
    ) -> DockingResult:
        """
        Mock docking for demonstration when Vina unavailable.

        IMPORTANT: These are NOT real scores. They are randomly generated
        to demonstrate the statistical framework. Real docking requires Vina.

        The mock scores are generated such that designed peptides have
        a SMALL advantage to show what a positive result would look like.
        In real science, this advantage must come from actual docking.
        """
        # Base score from sequence properties (rough approximation)
        # More aromatic residues generally dock better
        aromatics = sum(1 for aa in sequence if aa in 'FWY')
        hydrophobics = sum(1 for aa in sequence if aa in 'AVILMFYW')

        # Random baseline with some structure
        base_score = -4.0 + np.random.normal(0, 1.5)

        # Small bonus for aromatics (real physics-inspired)
        aromatic_bonus = -0.3 * aromatics

        # Designed peptides have constraints that MIGHT help
        # But this must be validated by real docking
        if is_designed:
            # NO artificial bonus - let the constraints speak for themselves
            design_effect = 0.0
        else:
            design_effect = 0.0

        score = base_score + aromatic_bonus + design_effect
        score = max(-12.0, min(-1.0, score))  # Realistic range

        return DockingResult(
            peptide_id=peptide_id,
            sequence=sequence,
            is_designed=is_designed,
            success=True,
            vina_score=score,
            poses_found=5,
            target_pdb=target_pdb,
            binding_site=center,
            box_size=box_size,
        )

    def _compare_designed_vs_controls(
        self,
        results: List[DockingResult]
    ) -> DockingComparison:
        """
        Statistical comparison of designed vs control peptides.

        This is THE critical test. If designed peptides don't significantly
        outperform random controls, the design strategy has failed.
        """
        # Separate designed and controls
        designed_scores = [r.vina_score for r in results if r.is_designed and r.success]
        control_scores = [r.vina_score for r in results if not r.is_designed and r.success]

        if not designed_scores or not control_scores:
            return DockingComparison(
                n_designed=len(designed_scores),
                designed_mean=0.0,
                designed_std=0.0,
                designed_best=0.0,
                n_controls=len(control_scores),
                control_mean=0.0,
                control_std=0.0,
                control_best=0.0,
                t_statistic=0.0,
                p_value=1.0,
                effect_size=0.0,
                designed_better=False,
                statistically_significant=False,
                practically_significant=False,
            )

        # Calculate statistics
        designed_mean = np.mean(designed_scores)
        designed_std = np.std(designed_scores, ddof=1) if len(designed_scores) > 1 else 0.0
        designed_best = min(designed_scores)  # More negative = better

        control_mean = np.mean(control_scores)
        control_std = np.std(control_scores, ddof=1) if len(control_scores) > 1 else 0.0
        control_best = min(control_scores)

        # Two-sample t-test (one-tailed: designed < control, i.e. better)
        # Lower (more negative) scores are better
        t_stat, p_value_two_tailed = stats.ttest_ind(designed_scores, control_scores)
        # One-tailed p-value (we want designed < control)
        p_value = p_value_two_tailed / 2 if t_stat < 0 else 1 - p_value_two_tailed / 2

        # Cohen's d effect size
        pooled_std = np.sqrt(
            ((len(designed_scores) - 1) * designed_std**2 +
             (len(control_scores) - 1) * control_std**2) /
            (len(designed_scores) + len(control_scores) - 2)
        ) if designed_std > 0 or control_std > 0 else 1.0

        effect_size = (control_mean - designed_mean) / pooled_std if pooled_std > 0 else 0.0

        # Verdicts
        designed_better = designed_mean < control_mean
        statistically_significant = p_value < 0.05
        practically_significant = abs(effect_size) > 0.5

        return DockingComparison(
            n_designed=len(designed_scores),
            designed_mean=designed_mean,
            designed_std=designed_std,
            designed_best=designed_best,
            n_controls=len(control_scores),
            control_mean=control_mean,
            control_std=control_std,
            control_best=control_best,
            t_statistic=t_stat,
            p_value=p_value,
            effect_size=effect_size,
            designed_better=designed_better,
            statistically_significant=statistically_significant,
            practically_significant=practically_significant,
        )

    def _print_comparison(self, comparison: DockingComparison) -> None:
        """Print statistical comparison."""
        print(f"\n{'='*70}")
        print("STATISTICAL COMPARISON: DESIGNED vs CONTROLS")
        print(f"{'='*70}")

        print(f"""
    DESIGNED PEPTIDES (n={comparison.n_designed})
    ─────────────────────────────────────
    Mean score:  {comparison.designed_mean:.2f} ± {comparison.designed_std:.2f} kcal/mol
    Best score:  {comparison.designed_best:.2f} kcal/mol

    RANDOM CONTROLS (n={comparison.n_controls})
    ─────────────────────────────────────
    Mean score:  {comparison.control_mean:.2f} ± {comparison.control_std:.2f} kcal/mol
    Best score:  {comparison.control_best:.2f} kcal/mol

    STATISTICAL TEST
    ─────────────────────────────────────
    t-statistic: {comparison.t_statistic:.3f}
    p-value:     {comparison.p_value:.4f}
    Effect size: {comparison.effect_size:.3f} (Cohen's d)
""")

        # Verdict
        print("    VERDICT")
        print("    ─────────────────────────────────────")

        if comparison.statistically_significant and comparison.designed_better:
            if comparison.practically_significant:
                print("    ✓ STRONG SIGNAL: Designed peptides significantly")
                print("      outperform random controls (p<0.05, d>0.5)")
                print("    → Proceed to MD validation (Module 7)")
            else:
                print("    ~ WEAK SIGNAL: Statistically significant but")
                print("      small effect size. Consider refining design.")
        else:
            print("    ✗ NO SIGNAL: Designed peptides do NOT outperform")
            print("      random controls.")
            print("")
            print("    This means the design strategy is ineffective.")
            print("    Options:")
            print("      1. Revise design constraints")
            print("      2. Try different binding site")
            print("      3. Use different design approach")
            print("")
            print("    DO NOT proceed to wet lab with these peptides.")

        print(f"""
    VALIDATION TIER: 3 (Docked)

    {'='*50}
""")

    def _save_results(
        self,
        results: List[DockingResult],
        comparison: DockingComparison
    ) -> None:
        """Save docking results."""
        # Convert numpy types to Python native types
        comparison_dict = asdict(comparison)
        for key, value in comparison_dict.items():
            if isinstance(value, (np.bool_, np.integer, np.floating)):
                comparison_dict[key] = value.item()

        output = {
            'timestamp': datetime.now().isoformat(),
            'method': 'AutoDock Vina' if self.vina_available else 'MOCK (demonstration only)',
            'warning': None if self.vina_available else 'These are NOT real docking scores. Install Vina for actual docking.',
            'comparison': comparison_dict,
            'results': [asdict(r) for r in results],
        }

        output_path = self.output_dir / "docking_results.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"    Saved: {output_path}")


def main():
    """Run docking on a project."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--target-pdb", type=str, help="Path to target PDB")
    parser.add_argument("--center", type=str, default="0,0,0", help="Binding site center x,y,z")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    project_dir = base_dir / "projects" / args.project

    # Load peptide structures
    struct_file = project_dir / "structures" / "structure_predictions.json"

    if struct_file.exists():
        with open(struct_file) as f:
            struct_data = json.load(f)
        peptides = struct_data['predictions']
    else:
        # Load from design if no structures yet
        design_files = list((project_dir / "peptide_designs").glob("design_*.json"))
        if not design_files:
            print("ERROR: No peptide data found")
            return

        with open(design_files[0]) as f:
            design_data = json.load(f)

        peptides = design_data['designed_peptides'] + design_data['control_peptides']

    # Parse binding center
    center = tuple(float(x) for x in args.center.split(','))

    # Find target PDB
    target_pdb = None
    if args.target_pdb:
        target_pdb = Path(args.target_pdb)
    else:
        # Try to find from target research
        target_file = project_dir / "target_research" / f"target_*.json"
        target_files = list(project_dir.glob("target_research/target_*.json"))
        if target_files:
            with open(target_files[0]) as f:
                target_data = json.load(f)
            best_pdb = target_data.get('best_pdb')
            if best_pdb:
                # Would need to download PDB
                print(f"Best PDB: {best_pdb}")
                print("Download with: wget https://files.rcsb.org/download/{best_pdb}.pdb")

    # Run docking
    docker = MolecularDocker(project_dir / "docking")

    if target_pdb and target_pdb.exists():
        results, comparison = docker.dock_peptides(
            target_pdb=target_pdb,
            peptide_structures=peptides,
            binding_center=center,
        )
    else:
        print("\nNo target PDB available. Running mock docking for demonstration.")
        results, comparison = docker.dock_peptides(
            target_pdb=Path("mock_target.pdb"),
            peptide_structures=peptides,
            binding_center=center,
        )

    return results, comparison


if __name__ == "__main__":
    main()
