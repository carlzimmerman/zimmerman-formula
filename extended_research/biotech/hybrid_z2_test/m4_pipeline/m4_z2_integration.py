#!/usr/bin/env python3
"""
M4 Z² Integration Layer
========================

Integrates Z² unified physics optimization with the M4 therapeutic pipeline.

This module serves as the bridge between:
- Classical MD simulations (m4_gpu_molecular_dynamics.py)
- Z² holographic corrections (m4_z2_therapeutic_optimizer.py)
- Final therapeutic output

The integration applies Z² corrections post-MD to:
1. Refine binding energy predictions
2. Optimize BBB penetration scores
3. Suggest geometric mutations
4. Generate unified reports

USAGE:
    # After MD completes, run Z² integration:
    python m4_z2_integration.py overnight_results/

    # Or integrate into overnight pipeline:
    from m4_z2_integration import Z2IntegratedPipeline
    pipeline = Z2IntegratedPipeline()
    results = pipeline.run_integrated_analysis(md_results)

LICENSE: AGPL-3.0 + OpenMTA + CC-BY-SA-4.0
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

# Import Z² optimizer
try:
    from m4_z2_therapeutic_optimizer import (
        Z2TherapeuticOptimizer,
        Z2TherapeuticResult,
        Z, Z_SQUARED,
        AA_SURFACES, AA_VOLUMES
    )
    Z2_AVAILABLE = True
except ImportError:
    Z2_AVAILABLE = False
    Z = 2 * np.sqrt(8 * np.pi / 3)  # Z = 2√(8π/3) ≈ 5.7735
    Z_SQUARED = 32 * np.pi / 3       # Z² = 32π/3 ≈ 33.51


class Z2IntegratedPipeline:
    """
    Integrated pipeline combining classical MD with Z² optimization.

    Workflow:
    1. Load MD simulation results
    2. Extract structural metrics (RMSF, RMSD, energy)
    3. Apply Z² geometric corrections
    4. Generate optimized therapeutic candidates
    5. Output comprehensive analysis
    """

    def __init__(self, output_dir: str = "z2_integrated_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        if Z2_AVAILABLE:
            self.z2_optimizer = Z2TherapeuticOptimizer(output_dir=str(self.output_dir))
        else:
            self.z2_optimizer = None
            print("Warning: Z² optimizer not available, using simplified corrections")

        self.z = Z
        self.z2 = Z_SQUARED

    def load_md_results(self, md_dir: str) -> List[Dict]:
        """
        Load molecular dynamics results from overnight pipeline.
        """
        md_path = Path(md_dir)
        results = []

        # Check for checkpoint file
        checkpoint_file = md_path / "checkpoint.json"
        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                checkpoint = json.load(f)

            # Load completed MD sequences
            completed_md = checkpoint.get('completed_md', [])
            print(f"Found {len(completed_md)} completed MD simulations")

        # Load individual MD result files
        md_files = list(md_path.glob("md_*.json"))

        for md_file in md_files:
            try:
                with open(md_file) as f:
                    data = json.load(f)
                    results.append(data)
            except Exception as e:
                print(f"Warning: Could not load {md_file}: {e}")

        # Also load from structure files
        for fasta_file in md_path.glob("*.fasta"):
            try:
                with open(fasta_file) as f:
                    content = f.read()

                name = None
                sequence = ""

                for line in content.split('\n'):
                    if line.startswith('>'):
                        name = line[1:].split('|')[0].strip()
                    elif not line.startswith(';'):
                        sequence += line.strip()

                if name and sequence:
                    # Check if we have MD results for this
                    md_result_file = md_path / f"md_{name}.json"

                    if md_result_file.exists():
                        with open(md_result_file) as f:
                            md_data = json.load(f)
                    else:
                        # Create basic entry
                        md_data = {
                            'name': name,
                            'sequence': sequence,
                            'length': len(sequence),
                            'rmsf': None,
                            'rmsd': None,
                        }

                    results.append(md_data)

            except Exception as e:
                print(f"Warning: Could not process {fasta_file}: {e}")

        return results

    def estimate_binding_from_md(self, md_result: Dict) -> float:
        """
        Estimate binding energy from MD metrics.

        Uses RMSF as proxy for flexibility:
        - Lower RMSF = more rigid = stronger binding
        - Higher RMSF = more flexible = weaker binding
        """
        rmsf = md_result.get('rmsf', 300)
        sequence = md_result.get('sequence', '')
        n = len(sequence)

        # Base binding estimate from sequence composition
        # Hydrophobic residues contribute to binding
        hydrophobic = sum(1 for aa in sequence if aa in 'VILFWM')
        aromatic = sum(1 for aa in sequence if aa in 'FYW')

        base_binding = -8.0 - (hydrophobic / n) * 5 - (aromatic / n) * 3

        # RMSF correction (inverted - lower RMSF = better binding)
        if rmsf and rmsf > 0:
            rmsf_factor = 1 / (1 + rmsf / 500)  # Normalize
            base_binding *= (1 + rmsf_factor)

        return np.clip(base_binding, -20, -5)

    def estimate_stability_from_md(self, md_result: Dict) -> float:
        """
        Estimate protein stability from MD trajectory.

        Uses RMSD variation as stability indicator.
        """
        rmsd = md_result.get('rmsd', 5.0)
        sequence = md_result.get('sequence', '')
        n = len(sequence)

        # Base stability from sequence (disulfides, salt bridges)
        cysteine_count = sequence.count('C')
        charged = sum(1 for aa in sequence if aa in 'RKDE')

        base_stability = -6.0 - (cysteine_count / 2) * 2 - (charged / n) * 3

        # RMSD correction (lower = more stable)
        if rmsd and rmsd > 0:
            rmsd_factor = np.exp(-rmsd / 10)
            base_stability *= (1 + rmsd_factor * 0.5)

        return np.clip(base_stability, -15, 0)

    def apply_z2_corrections(self, md_result: Dict) -> Dict:
        """
        Apply Z² geometric corrections to MD results.
        """
        sequence = md_result.get('sequence', '')
        name = md_result.get('name', 'unknown')

        if not sequence:
            return md_result

        n = len(sequence)

        # Classical estimates
        classical_binding = self.estimate_binding_from_md(md_result)
        classical_stability = self.estimate_stability_from_md(md_result)

        # Classical BBB score
        mw = n * 110  # Average MW
        psa = sum(20 if aa in 'STNQRKHDE' else 5 for aa in sequence)
        classical_bbb = np.exp(-mw / 5000) * np.exp(-psa / 500)

        # Apply Z² optimization
        if self.z2_optimizer:
            z2_result = self.z2_optimizer.optimize_therapeutic(
                name, sequence,
                classical_binding,
                classical_stability,
                classical_bbb
            )

            corrected = {
                **md_result,
                'classical_binding': classical_binding,
                'classical_stability': classical_stability,
                'classical_bbb': classical_bbb,
                'z2_binding': z2_result.z2_binding_energy,
                'z2_stability': z2_result.z2_stability,
                'z2_bbb_score': z2_result.z2_bbb_score,
                'holographic_entropy': z2_result.holographic_entropy,
                'manifold_dimension': z2_result.manifold_dimension,
                'geometric_correction': z2_result.geometric_correction,
                'suggested_mutations': z2_result.suggested_mutations,
                'z2_optimized': True,
            }
        else:
            # Simplified Z² correction
            surface_area = sum(AA_SURFACES.get(aa, 100) for aa in sequence)

            # Holographic correction factor
            z2_factor = 1 + (self.z2 - 1) * (surface_area / (n * 150))

            corrected = {
                **md_result,
                'classical_binding': classical_binding,
                'classical_stability': classical_stability,
                'classical_bbb': classical_bbb,
                'z2_binding': classical_binding / z2_factor,
                'z2_stability': classical_stability * (1 + 0.1 * self.z2 / 10),
                'z2_bbb_score': classical_bbb * (1 + 1 / self.z2),
                'geometric_correction': z2_factor,
                'z2_optimized': True,
            }

        return corrected

    def classify_therapeutic(self, result: Dict) -> Dict:
        """
        Classify therapeutic based on Z²-corrected metrics.
        """
        z2_binding = result.get('z2_binding', -10)
        z2_stability = result.get('z2_stability', -8)
        z2_bbb = result.get('z2_bbb_score', 0.3)

        # Classification tiers
        if z2_binding < -12 and z2_stability < -10 and z2_bbb > 0.5:
            tier = 'A'
            classification = 'Excellent candidate - high affinity, stable, BBB penetrant'
        elif z2_binding < -10 and z2_stability < -8:
            tier = 'B'
            classification = 'Good candidate - strong binding, adequate stability'
        elif z2_binding < -8:
            tier = 'C'
            classification = 'Moderate candidate - acceptable binding'
        else:
            tier = 'D'
            classification = 'Weak candidate - consider optimization'

        result['tier'] = tier
        result['classification'] = classification

        return result

    def generate_integrated_report(self, results: List[Dict]) -> Dict:
        """
        Generate comprehensive integrated report.
        """
        # Sort by tier and binding energy
        tier_order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        results_sorted = sorted(results,
                               key=lambda x: (tier_order.get(x.get('tier', 'D'), 3),
                                            x.get('z2_binding', 0)))

        # Statistics
        z2_bindings = [r.get('z2_binding', 0) for r in results]
        z2_bbbs = [r.get('z2_bbb_score', 0) for r in results]

        tier_counts = {}
        for r in results:
            tier = r.get('tier', 'D')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        report = {
            'title': 'Z² Integrated Therapeutic Analysis',
            'generated': datetime.now().isoformat(),
            'z_factor': self.z,
            'z_squared': self.z2,
            'physics_basis': {
                'framework': 'Z² Unified Physics',
                'origin': 'Friedmann cosmology + Bekenstein-Hawking thermodynamics',
                'key_insight': 'Holographic information bounds constrain molecular interactions',
                'Z_value': f'{self.z:.6f}',
                'Z2_value': f'{self.z2:.6f}',
            },
            'summary': {
                'total_analyzed': len(results),
                'tier_distribution': tier_counts,
                'mean_z2_binding': np.mean(z2_bindings),
                'std_z2_binding': np.std(z2_bindings),
                'mean_z2_bbb': np.mean(z2_bbbs),
                'top_candidates': len([r for r in results if r.get('tier') in ['A', 'B']]),
            },
            'top_candidates': [
                {
                    'name': r.get('name'),
                    'tier': r.get('tier'),
                    'z2_binding': r.get('z2_binding'),
                    'z2_stability': r.get('z2_stability'),
                    'z2_bbb_score': r.get('z2_bbb_score'),
                    'classification': r.get('classification'),
                    'suggested_mutations': r.get('suggested_mutations', [])[:3],
                }
                for r in results_sorted[:20]
            ],
            'all_results': results_sorted,
            'license': 'AGPL-3.0 + OpenMTA + CC-BY-SA-4.0',
        }

        # Save report
        report_path = self.output_dir / "z2_integrated_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"Report saved: {report_path}")

        return report

    def run_integrated_analysis(self, md_dir: str = "overnight_results") -> Dict:
        """
        Run full integrated Z² analysis pipeline.
        """
        print("=" * 70)
        print("Z² INTEGRATED THERAPEUTIC ANALYSIS")
        print("Unified Physics Applied to Drug Design")
        print("=" * 70)
        print()
        print(f"Z = 2√(8π/3) = {self.z:.6f}")
        print(f"Z² = 8π/3 = {self.z2:.6f}")
        print()

        # Load MD results
        print(f"Loading MD results from: {md_dir}")
        md_results = self.load_md_results(md_dir)
        print(f"Found {len(md_results)} sequences")
        print()

        # Apply Z² corrections
        print("Applying Z² geometric corrections...")
        corrected_results = []

        for i, md_result in enumerate(md_results):
            if i % 20 == 0:
                print(f"  Processing {i+1}/{len(md_results)}...")

            corrected = self.apply_z2_corrections(md_result)
            classified = self.classify_therapeutic(corrected)
            corrected_results.append(classified)

        print()

        # Generate report
        print("Generating integrated report...")
        report = self.generate_integrated_report(corrected_results)

        # Summary
        print()
        print("=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print(f"Total sequences analyzed: {report['summary']['total_analyzed']}")
        print(f"Tier distribution: {report['summary']['tier_distribution']}")
        print(f"Mean Z² binding energy: {report['summary']['mean_z2_binding']:.2f} kcal/mol")
        print(f"Mean Z² BBB score: {report['summary']['mean_z2_bbb']:.3f}")
        print()

        # Top candidates
        print("TOP CANDIDATES (Tier A/B):")
        for candidate in report['top_candidates'][:10]:
            print(f"  [{candidate['tier']}] {candidate['name']}")
            print(f"      Z² binding: {candidate['z2_binding']:.2f} kcal/mol")
            print(f"      BBB score: {candidate['z2_bbb_score']:.3f}")

        print()
        print(f"Full report: {self.output_dir / 'z2_integrated_report.json'}")
        print()

        return report


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        md_dir = sys.argv[1]
    else:
        md_dir = "overnight_results"

    pipeline = Z2IntegratedPipeline()
    report = pipeline.run_integrated_analysis(md_dir)

    return report


if __name__ == "__main__":
    main()
