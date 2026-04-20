#!/usr/bin/env python3
"""
M4 Z² Overnight Therapeutic Analyzer
=====================================

Applies the Z² unified physics framework to all overnight therapeutic sequences.

Computes for each therapeutic:
1. Holographic entropy bounds
2. 8D manifold embedding
3. Z² binding correction
4. Z² stability prediction
5. Z² BBB penetration score
6. Suggested mutations for optimization

Z² Framework:
    Z = 2√(8π/3) ≈ 5.7735
    Z² = 32π/3 ≈ 33.51

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional

# Z² Constants
Z = 2 * np.sqrt(8 * np.pi / 3)  # Z = 2√(8π/3) ≈ 5.7735
Z_SQUARED = 32 * np.pi / 3       # Z² = 32π/3 ≈ 33.51

# Amino acid properties
AA_MW = {
    'A': 89, 'R': 174, 'N': 132, 'D': 133, 'C': 121,
    'Q': 146, 'E': 147, 'G': 75, 'H': 155, 'I': 131,
    'L': 131, 'K': 146, 'M': 149, 'F': 165, 'P': 115,
    'S': 105, 'T': 119, 'W': 204, 'Y': 181, 'V': 117,
}

AA_SURFACE = {  # Accessible surface area (Å²)
    'A': 115, 'R': 241, 'N': 160, 'D': 150, 'C': 135,
    'Q': 180, 'E': 190, 'G': 75, 'H': 195, 'I': 175,
    'L': 170, 'K': 200, 'M': 185, 'F': 210, 'P': 145,
    'S': 115, 'T': 140, 'W': 255, 'Y': 230, 'V': 155,
}

AA_HYDROPHOBICITY = {  # Kyte-Doolittle scale
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}

AA_CHARGE = {
    'A': 0, 'R': 1, 'N': 0, 'D': -1, 'C': 0,
    'Q': 0, 'E': -1, 'G': 0, 'H': 0.5, 'I': 0,
    'L': 0, 'K': 1, 'M': 0, 'F': 0, 'P': 0,
    'S': 0, 'T': 0, 'W': 0, 'Y': 0, 'V': 0,
}


@dataclass
class Z2TherapeuticAnalysis:
    """Complete Z² analysis for a therapeutic sequence."""
    name: str
    category: str
    sequence_length: int
    molecular_weight: float

    # Sequence properties
    hydrophobicity: float
    net_charge: float
    aromatic_fraction: float

    # Z² Framework metrics
    holographic_entropy: float
    manifold_dimension: float
    z2_correction_factor: float

    # Z² Therapeutic scores
    z2_binding_score: float
    z2_stability_score: float
    z2_bbb_score: float
    z2_overall_score: float

    # Classification
    tier: str
    therapeutic_potential: str

    # Optimization suggestions
    suggested_mutations: List[str]


class Z2OvernightAnalyzer:
    """
    Analyze all overnight therapeutic sequences with Z² framework.
    """

    def __init__(self, output_dir: str = "z2_overnight_analysis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.z = Z
        self.z2 = Z_SQUARED

        # Effective Planck length in molecular units
        self.a0 = 0.529  # Bohr radius in Å
        self.l_eff = self.a0 / self.z

    def compute_sequence_properties(self, sequence: str) -> Dict:
        """Compute basic sequence properties."""
        seq = sequence.upper()
        n = len(seq)

        # Molecular weight
        mw = sum(AA_MW.get(aa, 110) for aa in seq)

        # Hydrophobicity
        hydro = np.mean([AA_HYDROPHOBICITY.get(aa, 0) for aa in seq])

        # Net charge at pH 7
        charge = sum(AA_CHARGE.get(aa, 0) for aa in seq)

        # Surface area
        surface = sum(AA_SURFACE.get(aa, 150) for aa in seq)

        # Aromatic content
        aromatic = sum(1 for aa in seq if aa in 'FYW') / n

        # Hydrophobic content
        hydrophobic = sum(1 for aa in seq if aa in 'VILFWM') / n

        return {
            'length': n,
            'mw': mw,
            'hydrophobicity': hydro,
            'charge': charge,
            'surface_area': surface,
            'aromatic_fraction': aromatic,
            'hydrophobic_fraction': hydrophobic,
        }

    def compute_holographic_entropy(self, props: Dict) -> Dict:
        """
        Compute holographic entropy and information metrics.

        The holographic principle bounds information by surface area:
            S_max = A / (4 l_eff²)

        For proteins, the effective length scale is:
            l_eff = a₀ / Z ≈ 0.091 Å
        """
        n = props['length']
        surface_A2 = props['surface_area']

        # Holographic entropy bound
        S_max = surface_A2 / (4 * self.l_eff**2)

        # Actual entropy from conformational DOF
        # Each residue has ~2 backbone angles + sidechain DOF
        n_dof = 3 * n - 6  # Remove translation/rotation
        S_actual = n_dof * np.log(2)  # Bits per DOF

        # Information ratio
        info_ratio = min(S_actual / S_max, 1.0) if S_max > 0 else 0

        # 8D manifold dimension
        # Full dimension = 8, reduces as info approaches bound
        d_eff = 3 + 5 * (1 - info_ratio)

        # Projection factor from 8D to 3D
        f_proj = 1 - (d_eff / 8)**2

        # Z² correction factor
        z2_correction = 1 + (self.z2 - 1) * info_ratio * f_proj

        return {
            'S_max': S_max,
            'S_actual': S_actual,
            'info_ratio': info_ratio,
            'manifold_dimension': d_eff,
            'f_projection': f_proj,
            'z2_correction': z2_correction,
            'holographic_entropy_bits': S_actual / np.log(2),
        }

    def compute_z2_binding(self, props: Dict, holo: Dict) -> float:
        """
        Compute Z²-corrected binding score.

        Higher hydrophobic content and aromatic residues
        contribute to binding, modified by Z² correction.
        """
        # Classical binding estimate
        hydrophobic_contrib = props['hydrophobic_fraction'] * 10
        aromatic_contrib = props['aromatic_fraction'] * 5
        charge_penalty = abs(props['charge']) * 0.1

        classical_binding = hydrophobic_contrib + aromatic_contrib - charge_penalty

        # Z² correction
        z2_binding = classical_binding * holo['z2_correction']

        # Normalize to 0-1 scale
        return min(z2_binding / 15, 1.0)

    def compute_z2_stability(self, props: Dict, holo: Dict) -> float:
        """
        Compute Z²-corrected stability score.

        Based on:
        - Hydrophobic core formation
        - Charge balance
        - Manifold dimension (higher = more stable)
        """
        # Classical stability
        hydro_balance = 1 - abs(props['hydrophobicity']) / 5
        charge_balance = 1 / (1 + abs(props['charge']) / 10)

        classical_stability = (hydro_balance + charge_balance) / 2

        # Z² enhancement from manifold dimension
        # Higher dimension = more conformational flexibility = better stability search
        manifold_factor = holo['manifold_dimension'] / 8

        z2_stability = classical_stability * manifold_factor * holo['z2_correction']

        return min(z2_stability, 1.0)

    def compute_z2_bbb(self, props: Dict, holo: Dict) -> float:
        """
        Compute Z²-corrected BBB penetration score.

        BBB penetration favors:
        - Lower MW
        - Moderate hydrophobicity
        - Low PSA (polar surface area)
        - Z² holographic optimization
        """
        mw = props['mw']
        hydro = props['hydrophobicity']

        # MW penalty (larger = harder to cross)
        mw_factor = np.exp(-mw / 50000)

        # Hydrophobicity optimum around +1
        hydro_factor = np.exp(-(hydro - 1)**2 / 4)

        # Charge penalty
        charge_factor = 1 / (1 + abs(props['charge']) / 5)

        classical_bbb = mw_factor * hydro_factor * charge_factor

        # Z² enhancement
        # Lower info_ratio = more room for BBB transport optimization
        z2_factor = 1 + (1 - holo['info_ratio']) / self.z2

        z2_bbb = classical_bbb * z2_factor

        return min(z2_bbb * 10, 1.0)  # Scale up and cap

    def suggest_mutations(self, sequence: str, props: Dict, holo: Dict) -> List[str]:
        """
        Suggest mutations to optimize Z² therapeutic potential.
        """
        suggestions = []
        seq = sequence.upper()
        n = len(seq)

        # Low stability: suggest disulfide or salt bridge
        if props['hydrophobicity'] < -1:
            # Find positions that could form disulfides
            for i in range(n - 4):
                if seq[i] == 'S':
                    suggestions.append(f"S{i+1}C for potential disulfide")
                    if len(suggestions) >= 2:
                        break

        # High charge: suggest neutralization
        if abs(props['charge']) > 10:
            for i, aa in enumerate(seq):
                if aa == 'K' and props['charge'] > 0:
                    suggestions.append(f"K{i+1}Q to reduce positive charge")
                elif aa == 'E' and props['charge'] < 0:
                    suggestions.append(f"E{i+1}Q to reduce negative charge")
                if len(suggestions) >= 3:
                    break

        # Low BBB: suggest hydrophobic substitutions
        if props['hydrophobicity'] < 0:
            for i, aa in enumerate(seq):
                if aa in 'ST' and i > 10:
                    suggestions.append(f"{aa}{i+1}V for BBB optimization")
                    if len(suggestions) >= 3:
                        break

        # Manifold optimization
        if holo['manifold_dimension'] < 7.5:
            suggestions.append("Consider flexible linker regions to increase conformational space")

        return suggestions[:5]  # Max 5 suggestions

    def classify_therapeutic(self, analysis: Z2TherapeuticAnalysis) -> Tuple[str, str]:
        """
        Classify therapeutic into tiers based on Z² scores.
        """
        overall = analysis.z2_overall_score

        if overall >= 0.8:
            tier = 'A'
            potential = 'Excellent - High priority for experimental validation'
        elif overall >= 0.6:
            tier = 'B'
            potential = 'Good - Strong candidate with optimization potential'
        elif overall >= 0.4:
            tier = 'C'
            potential = 'Moderate - Requires significant optimization'
        else:
            tier = 'D'
            potential = 'Low - Consider redesign or alternative targets'

        return tier, potential

    def analyze_sequence(self, name: str, sequence: str) -> Z2TherapeuticAnalysis:
        """
        Perform complete Z² analysis on a therapeutic sequence.
        """
        # Extract category from name
        category = name.split('/')[0] if '/' in name else 'unknown'

        # Compute properties
        props = self.compute_sequence_properties(sequence)

        # Holographic analysis
        holo = self.compute_holographic_entropy(props)

        # Z² therapeutic scores
        z2_binding = self.compute_z2_binding(props, holo)
        z2_stability = self.compute_z2_stability(props, holo)
        z2_bbb = self.compute_z2_bbb(props, holo)

        # Overall score (weighted average)
        z2_overall = 0.4 * z2_binding + 0.3 * z2_stability + 0.3 * z2_bbb

        # Mutation suggestions
        mutations = self.suggest_mutations(sequence, props, holo)

        # Create analysis object
        analysis = Z2TherapeuticAnalysis(
            name=name,
            category=category,
            sequence_length=props['length'],
            molecular_weight=props['mw'],
            hydrophobicity=props['hydrophobicity'],
            net_charge=props['charge'],
            aromatic_fraction=props['aromatic_fraction'],
            holographic_entropy=holo['holographic_entropy_bits'],
            manifold_dimension=holo['manifold_dimension'],
            z2_correction_factor=holo['z2_correction'],
            z2_binding_score=z2_binding,
            z2_stability_score=z2_stability,
            z2_bbb_score=z2_bbb,
            z2_overall_score=z2_overall,
            tier='',
            therapeutic_potential='',
            suggested_mutations=mutations,
        )

        # Classify
        tier, potential = self.classify_therapeutic(analysis)
        analysis.tier = tier
        analysis.therapeutic_potential = potential

        return analysis

    def analyze_all(self, sequences: Dict[str, str]) -> List[Z2TherapeuticAnalysis]:
        """
        Analyze all therapeutic sequences.
        """
        print("="*70)
        print("Z² OVERNIGHT THERAPEUTIC ANALYZER")
        print("="*70)
        print(f"Z = 2√(8π/3) = {self.z:.6f}")
        print(f"Z² = 8π/3 = {self.z2:.6f}")
        print(f"\nAnalyzing {len(sequences)} therapeutic sequences...")
        print()

        results = []

        for i, (name, seq) in enumerate(sequences.items()):
            if i % 20 == 0:
                print(f"  Processing {i+1}/{len(sequences)}...")

            try:
                analysis = self.analyze_sequence(name, seq)
                results.append(analysis)
            except Exception as e:
                print(f"  Warning: Failed to analyze {name}: {e}")

        # Sort by overall score
        results.sort(key=lambda x: -x.z2_overall_score)

        return results

    def generate_report(self, results: List[Z2TherapeuticAnalysis]) -> Dict:
        """
        Generate comprehensive analysis report.
        """
        # Tier distribution
        tiers = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        for r in results:
            tiers[r.tier] = tiers.get(r.tier, 0) + 1

        # Category analysis
        categories = {}
        for r in results:
            cat = r.category
            if cat not in categories:
                categories[cat] = {'count': 0, 'total_score': 0}
            categories[cat]['count'] += 1
            categories[cat]['total_score'] += r.z2_overall_score

        for cat in categories:
            categories[cat]['mean_score'] = categories[cat]['total_score'] / categories[cat]['count']

        # Statistics
        scores = [r.z2_overall_score for r in results]
        manifolds = [r.manifold_dimension for r in results]
        entropies = [r.holographic_entropy for r in results]

        report = {
            'title': 'Z² Overnight Therapeutic Analysis',
            'generated': datetime.now().isoformat(),
            'z_factor': self.z,
            'z_squared': self.z2,
            'framework': {
                'description': 'Z² Unified Physics Framework',
                'origin': 'Friedmann cosmology + Bekenstein-Hawking thermodynamics',
                'key_insight': 'Holographic information bounds constrain molecular interactions',
            },
            'summary': {
                'total_analyzed': len(results),
                'tier_distribution': tiers,
                'mean_z2_score': float(np.mean(scores)),
                'std_z2_score': float(np.std(scores)),
                'mean_manifold_dimension': float(np.mean(manifolds)),
                'mean_holographic_entropy': float(np.mean(entropies)),
            },
            'category_analysis': categories,
            'top_candidates': [asdict(r) for r in results[:20]],
            'all_results': [asdict(r) for r in results],
            'license': 'AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication',
        }

        # Save report
        report_path = self.output_dir / "z2_overnight_analysis.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        return report

    def print_summary(self, results: List[Z2TherapeuticAnalysis], report: Dict):
        """
        Print analysis summary to console.
        """
        print()
        print("="*70)
        print("Z² OVERNIGHT ANALYSIS COMPLETE")
        print("="*70)
        print()

        summary = report['summary']
        print(f"Total sequences analyzed: {summary['total_analyzed']}")
        print(f"Mean Z² score: {summary['mean_z2_score']:.4f} ± {summary['std_z2_score']:.4f}")
        print(f"Mean manifold dimension: {summary['mean_manifold_dimension']:.3f}/8.0")
        print(f"Mean holographic entropy: {summary['mean_holographic_entropy']:.0f} bits")
        print()

        print("TIER DISTRIBUTION:")
        for tier, count in sorted(summary['tier_distribution'].items()):
            pct = count / summary['total_analyzed'] * 100
            bar = '█' * int(pct / 5)
            print(f"  Tier {tier}: {count:3d} ({pct:5.1f}%) {bar}")
        print()

        print("TOP 15 CANDIDATES:")
        print("-"*80)
        print(f"{'Name':<35} {'Tier':>4} {'Z² Score':>9} {'Binding':>8} {'BBB':>6} {'Manifold':>9}")
        print("-"*80)

        for r in results[:15]:
            name = r.name[:34]
            print(f"{name:<35} {r.tier:>4} {r.z2_overall_score:>9.4f} {r.z2_binding_score:>8.3f} {r.z2_bbb_score:>6.3f} {r.manifold_dimension:>9.2f}")

        print()
        print("CATEGORY RANKINGS:")
        print("-"*50)

        cat_sorted = sorted(report['category_analysis'].items(),
                           key=lambda x: -x[1]['mean_score'])
        for cat, data in cat_sorted[:10]:
            print(f"  {cat:<30} {data['count']:>3} seqs, mean Z²={data['mean_score']:.4f}")

        print()
        print(f"Full report: {self.output_dir / 'z2_overnight_analysis.json'}")


def main():
    """Run Z² overnight analysis."""
    # Load sequences
    with open('all_therapeutic_sequences.json') as f:
        sequences = json.load(f)

    # Run analysis
    analyzer = Z2OvernightAnalyzer()
    results = analyzer.analyze_all(sequences)
    report = analyzer.generate_report(results)
    analyzer.print_summary(results, report)

    return results, report


if __name__ == "__main__":
    main()
