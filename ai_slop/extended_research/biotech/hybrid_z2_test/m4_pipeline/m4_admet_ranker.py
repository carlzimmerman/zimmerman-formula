#!/usr/bin/env python3
"""
M4 ADMET Pharmacokinetic Ranker
================================

Final ranking algorithm combining all empirical biophysics metrics:
- Structural stability (pLDDT)
- Binding affinity (MM/PBSA ΔG)
- Pharmacokinetic properties (ADMET)

ADMET = Absorption, Distribution, Metabolism, Excretion, Toxicity

Key metrics calculated:
1. Isoelectric Point (pI) - charge at neutral pH
2. GRAVY score - hydrophobicity (negative = soluble)
3. Net charge at pH 7.4 - aggregation prevention
4. Molecular weight - size constraints
5. Instability index - in vivo half-life

A top-tier therapeutic must have:
- ΔG < -15 kcal/mol (strong binding)
- pLDDT > 85 (stable structure)
- GRAVY < 0 (hydrophilic/soluble)
- |Net charge| > 3 (prevents aggregation)

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 (Open Science Prior Art)
"""

import json
import csv
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, fields
import warnings

# Try importing BioPython
try:
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    from Bio.SeqUtils import molecular_weight
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False
    print("[WARNING] BioPython not available. Install with: pip install biopython")


# Amino acid properties for fallback calculations
AA_MW = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
    'Q': 146.2, 'E': 147.1, 'G': 75.1, 'H': 155.2, 'I': 131.2,
    'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
    'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1,
}

# Kyte-Doolittle hydropathy scale
AA_HYDROPATHY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}

# pKa values for pI calculation
AA_PKA = {
    'D': 3.9,   # Asp
    'E': 4.1,   # Glu
    'H': 6.0,   # His
    'C': 8.3,   # Cys
    'Y': 10.1,  # Tyr
    'K': 10.5,  # Lys
    'R': 12.5,  # Arg
}


@dataclass
class ADMETResult:
    """ADMET pharmacokinetic analysis result."""
    name: str
    sequence_length: int

    # Physicochemical properties
    molecular_weight: float   # Da
    isoelectric_point: float  # pI
    gravy_score: float        # hydrophobicity (-2 to +2)
    net_charge_ph7: float     # net charge at physiological pH
    instability_index: float  # <40 = stable in vivo

    # Composition metrics
    aromatic_fraction: float
    charged_fraction: float
    hydrophobic_fraction: float

    # Solubility prediction
    predicted_solubility: str  # High, Medium, Low
    aggregation_risk: str      # Low, Medium, High

    # From previous analyses (if available)
    plddt_score: Optional[float]
    delta_G_bind: Optional[float]

    # Final composite score
    composite_score: float
    final_tier: str           # A, B, C, D
    recommendation: str


class ADMETRanker:
    """
    Calculate ADMET properties and generate final therapeutic rankings.
    """

    def __init__(self, output_dir: str = "admet_rankings"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def calculate_admet(
        self,
        name: str,
        sequence: str,
        plddt: Optional[float] = None,
        delta_G: Optional[float] = None
    ) -> ADMETResult:
        """
        Calculate ADMET properties for a sequence.
        """
        # Clean sequence
        sequence = ''.join(aa for aa in sequence.upper() if aa in AA_MW)
        n = len(sequence)

        if n == 0:
            return self._empty_result(name)

        # Calculate properties
        if BIOPYTHON_AVAILABLE:
            try:
                analysis = ProteinAnalysis(sequence)

                mw = analysis.molecular_weight()
                pI = analysis.isoelectric_point()
                gravy = analysis.gravy()
                instability = analysis.instability_index()

                # Amino acid percentages
                aa_percent = analysis.get_amino_acids_percent()
                aromatic = aa_percent.get('F', 0) + aa_percent.get('Y', 0) + aa_percent.get('W', 0)
                charged = (aa_percent.get('R', 0) + aa_percent.get('K', 0) +
                          aa_percent.get('D', 0) + aa_percent.get('E', 0))
                hydrophobic = (aa_percent.get('V', 0) + aa_percent.get('I', 0) +
                              aa_percent.get('L', 0) + aa_percent.get('F', 0) +
                              aa_percent.get('W', 0) + aa_percent.get('M', 0))

            except Exception as e:
                print(f"[WARNING] BioPython analysis failed for {name}: {e}")
                mw, pI, gravy, instability, aromatic, charged, hydrophobic = self._fallback_calc(sequence)
        else:
            mw, pI, gravy, instability, aromatic, charged, hydrophobic = self._fallback_calc(sequence)

        # Net charge at pH 7.4
        net_charge = self._calculate_net_charge(sequence, 7.4)

        # Solubility prediction
        if gravy < -0.5 and abs(net_charge) > 5:
            solubility = "High"
        elif gravy < 0.5 and abs(net_charge) > 2:
            solubility = "Medium"
        else:
            solubility = "Low"

        # Aggregation risk
        if abs(net_charge) > 5 and gravy < 0:
            aggregation = "Low"
        elif abs(net_charge) > 2 or gravy < 0.5:
            aggregation = "Medium"
        else:
            aggregation = "High"

        # Composite score calculation
        # Weights based on pharmaceutical importance
        composite = self._calculate_composite_score(
            plddt=plddt,
            delta_G=delta_G,
            gravy=gravy,
            net_charge=net_charge,
            instability=instability
        )

        # Final tier assignment
        if composite >= 80:
            tier = 'A'
            recommendation = "Excellent candidate - proceed to in vitro validation"
        elif composite >= 60:
            tier = 'B'
            recommendation = "Good candidate - consider optimization"
        elif composite >= 40:
            tier = 'C'
            recommendation = "Moderate candidate - requires significant optimization"
        else:
            tier = 'D'
            recommendation = "Poor candidate - consider alternative designs"

        return ADMETResult(
            name=name,
            sequence_length=n,
            molecular_weight=mw,
            isoelectric_point=pI,
            gravy_score=gravy,
            net_charge_ph7=net_charge,
            instability_index=instability,
            aromatic_fraction=aromatic,
            charged_fraction=charged,
            hydrophobic_fraction=hydrophobic,
            predicted_solubility=solubility,
            aggregation_risk=aggregation,
            plddt_score=plddt,
            delta_G_bind=delta_G,
            composite_score=composite,
            final_tier=tier,
            recommendation=recommendation,
        )

    def _fallback_calc(self, sequence: str) -> Tuple[float, float, float, float, float, float, float]:
        """Fallback calculations without BioPython."""
        n = len(sequence)

        # Molecular weight
        mw = sum(AA_MW.get(aa, 110) for aa in sequence) - (n - 1) * 18.015

        # GRAVY
        gravy = sum(AA_HYDROPATHY.get(aa, 0) for aa in sequence) / n

        # pI (simplified)
        pI = self._estimate_pI(sequence)

        # Instability index (simplified)
        instability = 40.0  # Default

        # Fractions
        aromatic = sum(1 for aa in sequence if aa in 'FYW') / n
        charged = sum(1 for aa in sequence if aa in 'RKDE') / n
        hydrophobic = sum(1 for aa in sequence if aa in 'VILFWM') / n

        return mw, pI, gravy, instability, aromatic, charged, hydrophobic

    def _estimate_pI(self, sequence: str) -> float:
        """Estimate isoelectric point."""
        # Count ionizable residues
        n_asp = sequence.count('D')
        n_glu = sequence.count('E')
        n_his = sequence.count('H')
        n_lys = sequence.count('K')
        n_arg = sequence.count('R')
        n_cys = sequence.count('C')
        n_tyr = sequence.count('Y')

        # Simple estimate based on charge balance
        positive = n_lys + n_arg + n_his * 0.1  # His partially charged at pH 7
        negative = n_asp + n_glu

        if positive > negative:
            pI = 7.0 + (positive - negative) * 0.5
        else:
            pI = 7.0 - (negative - positive) * 0.5

        return np.clip(pI, 3.0, 12.0)

    def _calculate_net_charge(self, sequence: str, pH: float = 7.4) -> float:
        """Calculate net charge at given pH."""
        charge = 0.0

        # N-terminus (pKa ~9.6)
        charge += 1.0 / (1.0 + 10**(pH - 9.6))

        # C-terminus (pKa ~2.3)
        charge -= 1.0 / (1.0 + 10**(2.3 - pH))

        # Side chains
        for aa in sequence:
            if aa == 'K':
                charge += 1.0 / (1.0 + 10**(pH - 10.5))
            elif aa == 'R':
                charge += 1.0 / (1.0 + 10**(pH - 12.5))
            elif aa == 'H':
                charge += 1.0 / (1.0 + 10**(pH - 6.0))
            elif aa == 'D':
                charge -= 1.0 / (1.0 + 10**(3.9 - pH))
            elif aa == 'E':
                charge -= 1.0 / (1.0 + 10**(4.1 - pH))
            elif aa == 'C':
                charge -= 1.0 / (1.0 + 10**(8.3 - pH))
            elif aa == 'Y':
                charge -= 1.0 / (1.0 + 10**(10.1 - pH))

        return charge

    def _calculate_composite_score(
        self,
        plddt: Optional[float],
        delta_G: Optional[float],
        gravy: float,
        net_charge: float,
        instability: float
    ) -> float:
        """
        Calculate composite score (0-100) for final ranking.

        Weights:
        - pLDDT (structural stability): 30%
        - ΔG binding energy: 30%
        - Solubility (GRAVY + charge): 25%
        - Stability index: 15%
        """
        score = 0.0

        # pLDDT component (30 points max)
        if plddt is not None:
            plddt_score = np.clip((plddt - 50) / 50, 0, 1) * 30
            score += plddt_score
        else:
            score += 15  # Default if not available

        # Binding energy component (30 points max)
        if delta_G is not None:
            # More negative is better, -20 kcal/mol would be perfect
            dG_score = np.clip((-delta_G - 5) / 15, 0, 1) * 30
            score += dG_score
        else:
            score += 15  # Default if not available

        # Solubility component (25 points max)
        # GRAVY < 0 is good, charge magnitude > 3 is good
        gravy_score = np.clip((0.5 - gravy) / 1.5, 0, 1) * 12.5
        charge_score = np.clip(abs(net_charge) / 10, 0, 1) * 12.5
        score += gravy_score + charge_score

        # Instability component (15 points max)
        # Instability index < 40 is stable
        stability_score = np.clip((50 - instability) / 30, 0, 1) * 15
        score += stability_score

        return np.clip(score, 0, 100)

    def _empty_result(self, name: str) -> ADMETResult:
        """Return empty result for invalid sequences."""
        return ADMETResult(
            name=name,
            sequence_length=0,
            molecular_weight=0,
            isoelectric_point=7.0,
            gravy_score=0,
            net_charge_ph7=0,
            instability_index=100,
            aromatic_fraction=0,
            charged_fraction=0,
            hydrophobic_fraction=0,
            predicted_solubility="Unknown",
            aggregation_risk="Unknown",
            plddt_score=None,
            delta_G_bind=None,
            composite_score=0,
            final_tier='D',
            recommendation="Invalid sequence",
        )

    def rank_candidates(
        self,
        sequences: Dict[str, str],
        stability_results: Optional[Dict] = None,
        binding_results: Optional[Dict] = None
    ) -> List[ADMETResult]:
        """
        Rank all candidates with ADMET analysis.
        """
        results = []

        # Build lookup tables from previous results
        plddt_lookup = {}
        dG_lookup = {}

        if stability_results:
            # Include both stable and unstable candidates for pLDDT lookup
            for candidate in stability_results.get('stable_candidates', []):
                name = candidate.get('name', '')
                plddt_lookup[name] = candidate.get('payload_plddt', candidate.get('mean_plddt'))
            for candidate in stability_results.get('unstable_flagged', []):
                name = candidate.get('name', '')
                plddt_lookup[name] = candidate.get('payload_plddt', candidate.get('mean_plddt'))

        if binding_results:
            for candidate in binding_results.get('binding_rankings', []):
                name = candidate.get('name', '')
                dG_lookup[name] = candidate.get('delta_G_bind')

        print(f"\n[ADMET] Analyzing {len(sequences)} sequences...")
        print("=" * 60)

        for i, (name, sequence) in enumerate(sequences.items()):
            if i % 20 == 0:
                print(f"  Processing {i+1}/{len(sequences)}...")

            plddt = plddt_lookup.get(name)
            delta_G = dG_lookup.get(name)

            result = self.calculate_admet(name, sequence, plddt, delta_G)
            results.append(result)

        return results

    def save_results(self, results: List[ADMETResult]) -> Tuple[str, str]:
        """Save results to JSON and CSV."""
        # Sort by composite score (highest first)
        sorted_results = sorted(results, key=lambda x: -x.composite_score)

        # Summary statistics
        all_scores = [r.composite_score for r in results]

        # JSON output
        json_output = {
            "title": "M4 ADMET Pharmacokinetic Rankings",
            "generated": datetime.now().isoformat(),
            "methodology": "Composite scoring: pLDDT (30%) + ΔG (30%) + Solubility (25%) + Stability (15%)",
            "summary": {
                "total_ranked": len(results),
                "mean_composite_score": float(np.mean(all_scores)),
                "std_composite_score": float(np.std(all_scores)),
                "top_candidate": sorted_results[0].name if sorted_results else None,
                "top_score": sorted_results[0].composite_score if sorted_results else None,
                "tier_distribution": {
                    "A_excellent": len([r for r in results if r.final_tier == 'A']),
                    "B_good": len([r for r in results if r.final_tier == 'B']),
                    "C_moderate": len([r for r in results if r.final_tier == 'C']),
                    "D_poor": len([r for r in results if r.final_tier == 'D']),
                },
            },
            "rankings": [asdict(r) for r in sorted_results],
            "license": "AGPL-3.0 + OpenMTA + CC BY-SA 4.0",
        }

        json_path = self.output_dir / "admet_rankings.json"
        with open(json_path, 'w') as f:
            json.dump(json_output, f, indent=2)

        # CSV output
        csv_path = self.output_dir / "m4_empirical_master_rankings.csv"

        # Add license header
        csv_header = """# M4 Empirical Therapeutic Rankings
# Generated: {}
# License: AGPL-3.0 + OpenMTA + CC BY-SA 4.0
# Methodology: Composite scoring combining pLDDT, MM/PBSA, and ADMET
#
# This dataset is released as PRIOR ART to prevent patent enclosure.
# Free for academic, research, and commercial use under open terms.
#
""".format(datetime.now().isoformat())

        with open(csv_path, 'w', newline='') as f:
            f.write(csv_header)

            # Get field names from dataclass
            fieldnames = [field.name for field in fields(ADMETResult)]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in sorted_results:
                writer.writerow(asdict(result))

        print(f"\n[ADMET] Results saved:")
        print(f"  JSON: {json_path}")
        print(f"  CSV:  {csv_path}")

        return str(json_path), str(csv_path)


def load_sequences_from_json(filepath: str) -> Dict[str, str]:
    """Load sequences from JSON file."""
    with open(filepath) as f:
        data = json.load(f)

    sequences = {}

    # Handle simple {name: sequence} format
    if isinstance(data, dict):
        for name, seq in data.items():
            if isinstance(seq, str) and len(seq) > 10:
                sequences[name] = seq
        if sequences:
            return sequences

    # Handle nested format
    for item in data.get('sequences', []):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', ''))
            seq = item.get('sequence', '')
            if name and seq:
                sequences[name] = seq

    return sequences


def main():
    """Main entry point."""
    import sys

    print("=" * 70)
    print("M4 ADMET PHARMACOKINETIC RANKER")
    print("Final Composite Scoring for Drug Candidate Selection")
    print("=" * 70)
    print()
    print("Composite Score = pLDDT (30%) + ΔG (30%) + Solubility (25%) + Stability (15%)")
    print()

    # Load sequences
    sequences_file = "all_therapeutic_sequences.json"
    if len(sys.argv) > 1:
        sequences_file = sys.argv[1]

    if not Path(sequences_file).exists():
        print(f"[ERROR] Sequences file not found: {sequences_file}")
        return

    sequences = load_sequences_from_json(sequences_file)
    print(f"Loaded {len(sequences)} sequences")

    # Load previous results if available
    stability_results = None
    binding_results = None

    stability_file = Path("empirical_stability/empirical_candidates.json")
    if stability_file.exists():
        with open(stability_file) as f:
            stability_results = json.load(f)
        print(f"Loaded stability results: {len(stability_results.get('stable_candidates', []))} stable")

    binding_file = Path("mmpbsa_results/binding_energies.json")
    if binding_file.exists():
        with open(binding_file) as f:
            binding_results = json.load(f)
        print(f"Loaded binding results: {len(binding_results.get('binding_rankings', []))} evaluated")

    # Run ADMET analysis
    ranker = ADMETRanker()
    results = ranker.rank_candidates(sequences, stability_results, binding_results)

    # Save results
    json_path, csv_path = ranker.save_results(results)

    # Print summary
    sorted_results = sorted(results, key=lambda x: -x.composite_score)

    print()
    print("=" * 70)
    print("FINAL RANKINGS COMPLETE")
    print("=" * 70)
    print(f"Total candidates: {len(results)}")
    print()

    tier_counts = {}
    for r in results:
        tier_counts[r.final_tier] = tier_counts.get(r.final_tier, 0) + 1

    print("TIER DISTRIBUTION:")
    for tier in ['A', 'B', 'C', 'D']:
        count = tier_counts.get(tier, 0)
        pct = 100 * count / len(results)
        bar = '#' * int(pct / 5)
        print(f"  Tier {tier}: {count:3d} ({pct:5.1f}%) {bar}")

    print()
    print("TOP 15 THERAPEUTIC CANDIDATES:")
    print("-" * 70)
    print(f"{'Rank':<5} {'Name':<35} {'Score':<8} {'Tier':<5} {'ΔG':<10} {'pLDDT':<8}")
    print("-" * 70)

    for i, r in enumerate(sorted_results[:15], 1):
        dG_str = f"{r.delta_G_bind:.1f}" if r.delta_G_bind else "N/A"
        plddt_str = f"{r.plddt_score:.1f}" if r.plddt_score else "N/A"
        print(f"{i:<5} {r.name:<35} {r.composite_score:<8.1f} {r.final_tier:<5} {dG_str:<10} {plddt_str:<8}")

    print()
    print("=" * 70)
    print("THE EMPIRICAL WINNER:")
    print("=" * 70)
    winner = sorted_results[0]
    print(f"  {winner.name}")
    print(f"  Composite Score: {winner.composite_score:.1f}/100")
    print(f"  Final Tier: {winner.final_tier}")
    print(f"  Recommendation: {winner.recommendation}")
    print()
    print(f"Full CSV report: {csv_path}")


if __name__ == "__main__":
    main()
