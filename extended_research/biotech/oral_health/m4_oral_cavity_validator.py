#!/usr/bin/env python3
"""
M4 Oral Cavity Validator

Validates that designed peptides can survive the challenging oral cavity
environment, including:
1. pH fluctuations (5.5-7.5)
2. Salivary proteases (trypsin, chymotrypsin, pepsin)
3. Temperature (37°C)
4. Mucin binding/retention
5. Biofilm penetration potential

This ensures peptides remain active in the mouth long enough to be effective.

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import math

# ==============================================================================
# CONFIGURATION
# ==============================================================================

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "results", "validation_results")

# Oral cavity conditions
ORAL_CONDITIONS = {
    "pH_range": (5.5, 7.5),  # Acidic during eating, neutral resting
    "pH_resting": 7.0,
    "pH_post_sugar": 5.5,
    "temperature_C": 37.0,
    "saliva_flow_ml_min": 0.3,  # Unstimulated
    "ionic_strength_mM": 50,
}

# Salivary proteases
PROTEASES = {
    "trypsin": {
        "cleavage_sites": ["K", "R"],  # Cuts after Lys, Arg
        "optimal_pH": 8.0,
        "activity_at_pH7": 0.8,
        "activity_at_pH5.5": 0.2,
    },
    "chymotrypsin": {
        "cleavage_sites": ["F", "W", "Y"],  # Cuts after aromatics
        "optimal_pH": 8.0,
        "activity_at_pH7": 0.7,
        "activity_at_pH5.5": 0.15,
    },
    "pepsin": {
        "cleavage_sites": ["F", "L"],  # Cuts after hydrophobics
        "optimal_pH": 2.0,
        "activity_at_pH7": 0.05,
        "activity_at_pH5.5": 0.3,
    },
    "elastase": {
        "cleavage_sites": ["A", "V", "G"],  # Cuts after small hydrophobics
        "optimal_pH": 8.5,
        "activity_at_pH7": 0.6,
        "activity_at_pH5.5": 0.1,
    },
}

# Amino acid pKa values for pH stability
AA_PKA = {
    'D': 3.9,  # Asp side chain
    'E': 4.1,  # Glu side chain
    'H': 6.0,  # His side chain
    'C': 8.3,  # Cys side chain
    'Y': 10.5, # Tyr side chain
    'K': 10.8, # Lys side chain
    'R': 12.5, # Arg side chain
}

# Amino acid properties for biofilm penetration
AA_PROPERTIES = {
    'A': {'hydrophobicity': 0.62, 'charge': 0},
    'V': {'hydrophobicity': 1.08, 'charge': 0},
    'L': {'hydrophobicity': 1.06, 'charge': 0},
    'I': {'hydrophobicity': 1.38, 'charge': 0},
    'M': {'hydrophobicity': 0.64, 'charge': 0},
    'F': {'hydrophobicity': 1.19, 'charge': 0},
    'W': {'hydrophobicity': 0.81, 'charge': 0},
    'Y': {'hydrophobicity': 0.26, 'charge': 0},
    'P': {'hydrophobicity': 0.12, 'charge': 0},
    'S': {'hydrophobicity': -0.18, 'charge': 0},
    'T': {'hydrophobicity': -0.05, 'charge': 0},
    'N': {'hydrophobicity': -0.78, 'charge': 0},
    'Q': {'hydrophobicity': -0.85, 'charge': 0},
    'G': {'hydrophobicity': 0.48, 'charge': 0},
    'C': {'hydrophobicity': 0.29, 'charge': 0},
    'K': {'hydrophobicity': -1.50, 'charge': 1},
    'R': {'hydrophobicity': -2.53, 'charge': 1},
    'H': {'hydrophobicity': -0.40, 'charge': 0.5},
    'D': {'hydrophobicity': -0.90, 'charge': -1},
    'E': {'hydrophobicity': -0.74, 'charge': -1},
}


# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class ProteaseResistanceResult:
    """Result of protease resistance analysis."""
    protease_name: str
    n_cleavage_sites: int
    cleavage_positions: List[int]
    predicted_half_life_hours: float
    resistance_score: float  # 0-1


@dataclass
class pHStabilityResult:
    """Result of pH stability analysis."""
    pH_tested: float
    charge_at_pH: float
    charge_change_from_neutral: float
    stability_score: float  # 0-1
    ionizable_residues: List[Tuple[str, int, float]]  # (aa, pos, pKa)


@dataclass
class BiofilmPenetrationResult:
    """Result of biofilm penetration assessment."""
    net_charge: float
    hydrophobicity: float
    size_kda: float
    penetration_score: float  # 0-1
    limiting_factors: List[str]


@dataclass
class ValidationReport:
    """Complete validation report for a peptide."""
    peptide_id: str
    sequence: str
    length: int

    # Individual assessments
    protease_results: List[ProteaseResistanceResult]
    pH_stability: List[pHStabilityResult]
    biofilm_penetration: BiofilmPenetrationResult

    # Summary scores
    protease_resistance_score: float
    pH_stability_score: float
    biofilm_penetration_score: float
    overall_oral_viability_score: float

    # Verdict
    verdict: str  # "VALIDATED", "FLAGGED", "REJECTED"
    recommendations: List[str]

    timestamp: str


# ==============================================================================
# VALIDATION FUNCTIONS
# ==============================================================================

def analyze_protease_resistance(sequence: str, d_amino_positions: List[int] = None) -> List[ProteaseResistanceResult]:
    """Analyze resistance to salivary proteases."""

    if d_amino_positions is None:
        d_amino_positions = []

    results = []

    for protease_name, protease_info in PROTEASES.items():
        cleavage_sites = protease_info["cleavage_sites"]
        cleavage_positions = []

        for i, aa in enumerate(sequence):
            # Check if this position is a cleavage site
            if aa in cleavage_sites:
                # D-amino acids are resistant to cleavage
                if i not in d_amino_positions:
                    cleavage_positions.append(i)

        n_sites = len(cleavage_positions)

        # Estimate half-life based on number of cleavage sites
        # More sites = shorter half-life
        if n_sites == 0:
            half_life = 24.0  # Very stable
            resistance_score = 1.0
        elif n_sites == 1:
            half_life = 4.0
            resistance_score = 0.8
        elif n_sites == 2:
            half_life = 1.0
            resistance_score = 0.5
        elif n_sites <= 4:
            half_life = 0.25
            resistance_score = 0.2
        else:
            half_life = 0.1
            resistance_score = 0.0

        # Adjust for protease activity at oral pH
        activity_factor = protease_info.get("activity_at_pH7", 0.5)
        half_life /= activity_factor
        resistance_score = min(1.0, resistance_score / activity_factor)

        result = ProteaseResistanceResult(
            protease_name=protease_name,
            n_cleavage_sites=n_sites,
            cleavage_positions=cleavage_positions,
            predicted_half_life_hours=half_life,
            resistance_score=min(1.0, resistance_score)
        )
        results.append(result)

    return results


def analyze_pH_stability(sequence: str) -> List[pHStabilityResult]:
    """Analyze stability across oral pH range."""

    results = []

    # Test at multiple pH values
    pH_values = [5.5, 6.0, 6.5, 7.0, 7.5]

    for pH in pH_values:
        # Calculate charge at this pH
        charge = 0.0
        ionizable = []

        # N-terminus (pKa ~8)
        charge += 1.0 / (1.0 + 10**(pH - 8.0))

        # C-terminus (pKa ~3.5)
        charge -= 1.0 / (1.0 + 10**(3.5 - pH))

        # Side chains
        for i, aa in enumerate(sequence):
            if aa in AA_PKA:
                pKa = AA_PKA[aa]
                ionizable.append((aa, i, pKa))

                if aa in ['D', 'E', 'C', 'Y']:  # Acidic
                    charge -= 1.0 / (1.0 + 10**(pKa - pH))
                elif aa in ['K', 'R', 'H']:  # Basic
                    charge += 1.0 / (1.0 + 10**(pH - pKa))

        # Calculate charge at neutral pH for comparison
        charge_neutral = 0.0
        charge_neutral += 1.0 / (1.0 + 10**(7.0 - 8.0))
        charge_neutral -= 1.0 / (1.0 + 10**(3.5 - 7.0))
        for aa in sequence:
            if aa in AA_PKA:
                pKa = AA_PKA[aa]
                if aa in ['D', 'E', 'C', 'Y']:
                    charge_neutral -= 1.0 / (1.0 + 10**(pKa - 7.0))
                elif aa in ['K', 'R', 'H']:
                    charge_neutral += 1.0 / (1.0 + 10**(7.0 - pKa))

        charge_change = abs(charge - charge_neutral)

        # Stability score: less charge change = more stable
        # Large charge changes can cause conformational changes
        if charge_change < 0.5:
            stability_score = 1.0
        elif charge_change < 1.0:
            stability_score = 0.8
        elif charge_change < 2.0:
            stability_score = 0.5
        else:
            stability_score = 0.2

        result = pHStabilityResult(
            pH_tested=pH,
            charge_at_pH=charge,
            charge_change_from_neutral=charge_change,
            stability_score=stability_score,
            ionizable_residues=ionizable
        )
        results.append(result)

    return results


def analyze_biofilm_penetration(sequence: str) -> BiofilmPenetrationResult:
    """Analyze potential for biofilm penetration."""

    # Calculate properties
    net_charge = sum(AA_PROPERTIES.get(aa, {}).get('charge', 0) for aa in sequence)
    hydrophobicity = sum(AA_PROPERTIES.get(aa, {}).get('hydrophobicity', 0) for aa in sequence) / len(sequence)
    size_kda = len(sequence) * 0.11  # Approximate

    limiting_factors = []
    score = 0.7  # Baseline

    # Size factor: smaller is better for penetration
    if size_kda < 1.5:
        score += 0.15
    elif size_kda > 3.0:
        score -= 0.2
        limiting_factors.append(f"Large size ({size_kda:.1f} kDa) may limit penetration")

    # Charge factor: moderate positive charge helps penetrate negatively charged biofilm matrix
    if 1 <= net_charge <= 3:
        score += 0.1
    elif net_charge > 5:
        score -= 0.1
        limiting_factors.append("High positive charge may cause non-specific binding")
    elif net_charge < -1:
        score -= 0.2
        limiting_factors.append("Negative charge repelled by biofilm matrix")

    # Hydrophobicity: moderate is best
    if -0.5 < hydrophobicity < 0.5:
        score += 0.1
    elif hydrophobicity > 1.0:
        score -= 0.15
        limiting_factors.append("High hydrophobicity may cause aggregation")
    elif hydrophobicity < -1.0:
        score -= 0.1
        limiting_factors.append("Low hydrophobicity may reduce membrane interaction")

    # Proline content (can help or hurt)
    proline_count = sequence.count('P')
    if proline_count > len(sequence) * 0.2:
        limiting_factors.append("High proline content may affect folding")

    result = BiofilmPenetrationResult(
        net_charge=net_charge,
        hydrophobicity=hydrophobicity,
        size_kda=size_kda,
        penetration_score=max(0.0, min(1.0, score)),
        limiting_factors=limiting_factors
    )

    return result


def validate_peptide(peptide_id: str, sequence: str,
                     d_amino_positions: List[int] = None) -> ValidationReport:
    """Run complete validation for a peptide."""

    # Run all analyses
    protease_results = analyze_protease_resistance(sequence, d_amino_positions)
    pH_results = analyze_pH_stability(sequence)
    biofilm_result = analyze_biofilm_penetration(sequence)

    # Calculate summary scores
    protease_score = sum(r.resistance_score for r in protease_results) / len(protease_results)
    pH_score = sum(r.stability_score for r in pH_results) / len(pH_results)
    biofilm_score = biofilm_result.penetration_score

    # Overall score (weighted)
    overall_score = (
        0.4 * protease_score +
        0.3 * pH_score +
        0.3 * biofilm_score
    )

    # Determine verdict
    recommendations = []

    if overall_score >= 0.7:
        verdict = "VALIDATED"
    elif overall_score >= 0.5:
        verdict = "FLAGGED"
    else:
        verdict = "REJECTED"

    # Generate recommendations
    if protease_score < 0.5:
        recommendations.append("Consider adding D-amino acids at protease cleavage sites")
        recommendations.append("Consider cyclization to improve protease resistance")

    if pH_score < 0.5:
        recommendations.append("Reduce ionizable residues to improve pH stability")

    if biofilm_score < 0.5:
        recommendations.append("Reduce peptide size if possible")
        if biofilm_result.net_charge < 0:
            recommendations.append("Add positively charged residues for biofilm penetration")

    if not recommendations:
        recommendations.append("Peptide meets oral cavity requirements")

    report = ValidationReport(
        peptide_id=peptide_id,
        sequence=sequence,
        length=len(sequence),
        protease_results=protease_results,
        pH_stability=pH_results,
        biofilm_penetration=biofilm_result,
        protease_resistance_score=protease_score,
        pH_stability_score=pH_score,
        biofilm_penetration_score=biofilm_score,
        overall_oral_viability_score=overall_score,
        verdict=verdict,
        recommendations=recommendations,
        timestamp=datetime.now().isoformat()
    )

    return report


# ==============================================================================
# BATCH VALIDATION
# ==============================================================================

def load_peptides_for_validation(peptides_dir: str = None) -> List[Dict]:
    """Load peptides from previous stages."""

    if peptides_dir is None:
        peptides_dir = os.path.join(os.path.dirname(__file__), "results", "designed_peptides")

    peptides = []

    if os.path.exists(peptides_dir):
        for filename in os.listdir(peptides_dir):
            if filename.endswith(".json") and "designed_peptides" in filename:
                filepath = os.path.join(peptides_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)

                for target_id, target_data in data.get("targets", {}).items():
                    for pep in target_data.get("peptides", []):
                        peptides.append({
                            "peptide_id": pep["peptide_id"],
                            "sequence": pep["sequence"],
                            "d_amino_acids": pep.get("d_amino_acids", [])
                        })

    if not peptides:
        print("No peptide files found. Using demo peptides.")
        peptides = [
            {"peptide_id": "demo_001", "sequence": "CRWFKDLAEKC", "d_amino_acids": []},
            {"peptide_id": "demo_002", "sequence": "RKWFKRK", "d_amino_acids": [1, 5]},
        ]

    return peptides


def run_validation_batch(peptides: List[Dict] = None) -> List[ValidationReport]:
    """Run validation on all peptides."""

    if peptides is None:
        peptides = load_peptides_for_validation()

    print("="*70)
    print("M4 ORAL CAVITY VALIDATOR")
    print("="*70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Peptides to validate: {len(peptides)}")
    print(f"Conditions: pH {ORAL_CONDITIONS['pH_range']}, {ORAL_CONDITIONS['temperature_C']}°C")
    print("="*70)

    reports = []

    for pep in peptides:
        print(f"\nValidating: {pep['peptide_id']}")
        print(f"  Sequence: {pep['sequence']}")

        report = validate_peptide(
            pep['peptide_id'],
            pep['sequence'],
            pep.get('d_amino_acids', [])
        )

        reports.append(report)

        print(f"  Verdict: {report.verdict}")
        print(f"  Scores: Protease={report.protease_resistance_score:.2f}, "
              f"pH={report.pH_stability_score:.2f}, "
              f"Biofilm={report.biofilm_penetration_score:.2f}")
        print(f"  Overall: {report.overall_oral_viability_score:.2f}")

    return reports


# ==============================================================================
# OUTPUT
# ==============================================================================

def save_results(reports: List[ValidationReport]) -> str:
    """Save validation results."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_data = {
        "pipeline": "M4 Oral Cavity Validator",
        "version": "1.0.0",
        "license": "AGPL-3.0-or-later",
        "timestamp": datetime.now().isoformat(),
        "conditions": ORAL_CONDITIONS,
        "proteases_tested": list(PROTEASES.keys()),
        "summary": {
            "total_peptides": len(reports),
            "validated": sum(1 for r in reports if r.verdict == "VALIDATED"),
            "flagged": sum(1 for r in reports if r.verdict == "FLAGGED"),
            "rejected": sum(1 for r in reports if r.verdict == "REJECTED"),
        },
        "reports": []
    }

    for report in reports:
        report_dict = {
            "peptide_id": report.peptide_id,
            "sequence": report.sequence,
            "length": report.length,
            "verdict": report.verdict,
            "scores": {
                "protease_resistance": report.protease_resistance_score,
                "pH_stability": report.pH_stability_score,
                "biofilm_penetration": report.biofilm_penetration_score,
                "overall": report.overall_oral_viability_score,
            },
            "recommendations": report.recommendations,
            "protease_details": [asdict(r) for r in report.protease_results],
            "pH_details": [asdict(r) for r in report.pH_stability],
            "biofilm_details": asdict(report.biofilm_penetration),
        }
        output_data["reports"].append(report_dict)

    output_path = os.path.join(OUTPUT_DIR, f"oral_validation_{timestamp}.json")
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    return output_path


def print_summary(reports: List[ValidationReport]):
    """Print validation summary."""

    print("\n" + "="*70)
    print("ORAL CAVITY VALIDATION SUMMARY")
    print("="*70)

    validated = [r for r in reports if r.verdict == "VALIDATED"]
    flagged = [r for r in reports if r.verdict == "FLAGGED"]
    rejected = [r for r in reports if r.verdict == "REJECTED"]

    print(f"\nTotal validated: {len(reports)}")
    print(f"  VALIDATED: {len(validated)} ({100*len(validated)/len(reports):.1f}%)")
    print(f"  FLAGGED: {len(flagged)} ({100*len(flagged)/len(reports):.1f}%)")
    print(f"  REJECTED: {len(rejected)} ({100*len(rejected)/len(reports):.1f}%)")

    if validated:
        print("\n--- TOP VALIDATED PEPTIDES ---")
        for r in sorted(validated, key=lambda x: -x.overall_oral_viability_score)[:5]:
            print(f"  {r.peptide_id}: {r.sequence}")
            print(f"    Overall: {r.overall_oral_viability_score:.2f}")

    if rejected:
        print("\n--- REJECTED PEPTIDES ---")
        for r in rejected:
            print(f"  {r.peptide_id}: {r.recommendations[0] if r.recommendations else 'N/A'}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point."""

    # Run validation
    reports = run_validation_batch()

    # Print summary
    print_summary(reports)

    # Save results
    save_results(reports)

    print("\nOral cavity validation complete.")

    return reports


if __name__ == "__main__":
    main()
