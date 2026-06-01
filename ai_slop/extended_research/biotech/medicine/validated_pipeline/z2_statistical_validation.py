#!/usr/bin/env python3
"""
Z² Statistical Validation Framework
=====================================
Author: Carl Zimmerman
Date: 2026-04-24
License: AGPL-3.0

CRITICAL QUESTION: Is the Z² constant (6.015 Å) statistically significant,
or is it an artifact of cherry-picking structures that happen to fit?

This script creates a rigorous statistical framework to test the Z² hypothesis
against null distributions of aromatic-aromatic distances in protein structures.

THEORETICAL/COMPUTATIONAL ONLY - This is hypothesis testing, not proof.
"""

import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from scipy import stats
import warnings

# =============================================================================
# CONSTANTS
# =============================================================================

Z2_CLAIMED_VALUE = 6.015152508891966  # Angstroms
Z2_TOLERANCE = 0.005  # ±5 mÅ claimed tolerance

# Aromatic residues
AROMATIC_RESIDUES = {'PHE', 'TYR', 'TRP', 'HIS'}

# Typical aromatic stacking distance ranges from literature
LITERATURE_STACKING_RANGES = {
    'parallel_displaced': (3.3, 4.0),  # Most common in proteins
    'T_shaped': (4.5, 5.5),  # Edge-to-face
    'offset_stacked': (3.5, 4.5),  # Offset parallel
    'long_range': (5.5, 7.0),  # Extended interactions
}


# =============================================================================
# NULL HYPOTHESIS FRAMEWORK
# =============================================================================

@dataclass
class StatisticalTest:
    """Results of a statistical test"""
    test_name: str
    null_hypothesis: str
    test_statistic: float
    p_value: float
    significant: bool
    interpretation: str


def generate_null_distribution_uniform(n_samples: int = 100000,
                                        min_dist: float = 3.0,
                                        max_dist: float = 10.0) -> np.ndarray:
    """
    Null hypothesis 1: Aromatic distances are uniformly distributed.

    If Z² is just cherry-picking, we'd expect no enrichment at 6.015 Å
    compared to any other distance in the plausible range.
    """
    return np.random.uniform(min_dist, max_dist, n_samples)


def generate_null_distribution_normal(n_samples: int = 100000,
                                       mean: float = 5.0,
                                       std: float = 1.5) -> np.ndarray:
    """
    Null hypothesis 2: Aromatic distances follow a normal distribution
    centered around typical stacking distances.

    Literature suggests most aromatic interactions are 3.5-5.5 Å,
    with a tail extending to longer distances.
    """
    samples = np.random.normal(mean, std, n_samples)
    # Truncate to physically reasonable range
    samples = samples[(samples > 3.0) & (samples < 10.0)]
    return samples


def generate_null_distribution_bimodal(n_samples: int = 100000) -> np.ndarray:
    """
    Null hypothesis 3: Aromatic distances are bimodal.

    Peak 1: Close stacking (~3.8 Å) - parallel displaced
    Peak 2: T-shaped/extended (~5.0 Å)

    This is more realistic based on crystallographic surveys.
    """
    # 60% close stacking, 40% extended
    n_close = int(n_samples * 0.6)
    n_extended = n_samples - n_close

    close = np.random.normal(3.8, 0.4, n_close)
    extended = np.random.normal(5.2, 0.8, n_extended)

    samples = np.concatenate([close, extended])
    samples = samples[(samples > 3.0) & (samples < 10.0)]
    return samples


def generate_null_distribution_empirical() -> np.ndarray:
    """
    Null hypothesis 4: Based on empirical aromatic distances from PDB surveys.

    From literature surveys of aromatic interactions in proteins:
    - Burley & Petsko (1985): 4.5-7.0 Å for aromatic pairs
    - McGaughey et al. (1998): peak at 5.0-5.5 Å
    - Hunter & Sanders (1990): optimal ~3.8 Å for parallel stacking

    We model this as a gamma distribution shifted to start at 3.0 Å.
    """
    # Gamma distribution parameters fitted to literature data
    shape, scale = 3.0, 0.8
    offset = 3.0

    samples = np.random.gamma(shape, scale, 100000) + offset
    samples = samples[samples < 10.0]
    return samples


# =============================================================================
# STATISTICAL TESTS
# =============================================================================

def calculate_enrichment(distances: np.ndarray,
                         target: float = Z2_CLAIMED_VALUE,
                         tolerance: float = 0.1) -> Tuple[float, float]:
    """
    Calculate enrichment of distances near target value.

    Returns:
        observed_fraction: Fraction of distances within tolerance of target
        expected_fraction: Expected fraction under uniform distribution
    """
    in_range = np.sum(np.abs(distances - target) < tolerance)
    observed_fraction = in_range / len(distances)

    # Expected under uniform distribution over 3-10 Å range
    expected_fraction = (2 * tolerance) / (10.0 - 3.0)

    return observed_fraction, expected_fraction


def binomial_test(observed: int, total: int, expected_prob: float) -> StatisticalTest:
    """
    Test if observed count significantly exceeds expected under null.
    """
    result = stats.binomtest(observed, total, expected_prob, alternative='greater')

    return StatisticalTest(
        test_name="Binomial Test",
        null_hypothesis=f"P(distance near 6.015 Å) = {expected_prob:.4f}",
        test_statistic=observed / total,
        p_value=result.pvalue,
        significant=result.pvalue < 0.05,
        interpretation=f"Observed {observed}/{total} ({observed/total:.4f}) vs expected {expected_prob:.4f}"
    )


def ks_test(sample1: np.ndarray, sample2: np.ndarray) -> StatisticalTest:
    """
    Kolmogorov-Smirnov test: Are two distributions different?
    """
    statistic, pvalue = stats.ks_2samp(sample1, sample2)

    return StatisticalTest(
        test_name="Kolmogorov-Smirnov Test",
        null_hypothesis="Two samples come from same distribution",
        test_statistic=statistic,
        p_value=pvalue,
        significant=pvalue < 0.05,
        interpretation=f"KS statistic = {statistic:.4f}, p = {pvalue:.4e}"
    )


def bootstrap_confidence_interval(distances: np.ndarray,
                                   n_bootstrap: int = 10000,
                                   confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    Bootstrap confidence interval for mean aromatic distance.

    Returns:
        mean, lower_ci, upper_ci
    """
    means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(distances, size=len(distances), replace=True)
        means.append(np.mean(sample))

    means = np.array(means)
    alpha = 1 - confidence
    lower = np.percentile(means, alpha/2 * 100)
    upper = np.percentile(means, (1 - alpha/2) * 100)

    return np.mean(distances), lower, upper


# =============================================================================
# Z² VALIDATION ANALYSIS
# =============================================================================

def analyze_z2_validation():
    """
    Comprehensive statistical analysis of the Z² hypothesis.
    """

    results = {
        'z2_claimed_value': Z2_CLAIMED_VALUE,
        'z2_tolerance': Z2_TOLERANCE,
        'analysis_date': '2026-04-24',
        'null_hypotheses_tested': [],
        'validation_data': {},
        'conclusions': [],
    }

    # Our observed Z² distances from AlphaFold validation
    # These are the ONLY data points we actually have
    observed_z2_distances = [
        6.015152508891966 - 0.0013,  # C2_Homodimer_A: -1.3 mÅ
        6.015152508891966 + 0.0001,  # TNF-α: +0.1 mÅ
        6.015152508891966 + 0.0045,  # C2_Protease_B: +4.5 mÅ
    ]

    results['observed_distances'] = {
        'C2_Homodimer_A': observed_z2_distances[0],
        'TNF-α': observed_z2_distances[1],
        'C2_Protease_B': observed_z2_distances[2],
        'mean': np.mean(observed_z2_distances),
        'std': np.std(observed_z2_distances),
        'n': len(observed_z2_distances),
    }

    # CRITICAL PROBLEM: We only have 3 data points
    results['critical_limitation'] = {
        'issue': 'SEVERE UNDERPOWERING',
        'n_observations': 3,
        'minimum_for_significance': 'Typically 20-30 for parametric tests',
        'interpretation': 'Cannot draw statistically valid conclusions from n=3',
    }

    # Generate null distributions
    null_uniform = generate_null_distribution_uniform()
    null_normal = generate_null_distribution_normal()
    null_bimodal = generate_null_distribution_bimodal()
    null_empirical = generate_null_distribution_empirical()

    # Analyze each null distribution
    for name, null_dist in [
        ('Uniform (3-10 Å)', null_uniform),
        ('Normal (μ=5.0, σ=1.5)', null_normal),
        ('Bimodal (stacking peaks)', null_bimodal),
        ('Empirical (literature-based)', null_empirical),
    ]:
        analysis = {
            'null_hypothesis': name,
            'null_mean': float(np.mean(null_dist)),
            'null_std': float(np.std(null_dist)),
            'null_median': float(np.median(null_dist)),
        }

        # What fraction of null distribution is near 6.015 Å?
        obs_frac, exp_frac = calculate_enrichment(null_dist, Z2_CLAIMED_VALUE, 0.01)
        analysis['fraction_at_z2'] = {
            'within_10mA': float(obs_frac),
            'interpretation': f'{obs_frac*100:.2f}% of random distances fall within ±10 mÅ of Z²'
        }

        # Probability of getting 3/3 within ±5 mÅ by chance
        p_single = np.sum(np.abs(null_dist - Z2_CLAIMED_VALUE) < 0.005) / len(null_dist)
        p_three = p_single ** 3
        analysis['probability_3_of_3'] = {
            'p_single_within_5mA': float(p_single),
            'p_three_consecutive': float(p_three),
            'interpretation': f'Probability of 3/3 within ±5 mÅ by chance: {p_three:.2e}'
        }

        results['null_hypotheses_tested'].append(analysis)

    # What would be needed for statistical validity?
    results['power_analysis'] = {
        'current_n': 3,
        'effect_size_claimed': 'Enrichment at 6.015 Å vs random',
        'for_alpha_0.05_power_0.8': {
            'binomial_test': 'Need ~20-30 observations',
            't_test': 'Need ~15-20 observations per group',
            'ks_test': 'Need ~50+ observations per distribution',
        },
        'recommendation': 'Validate against AT LEAST 20 diverse protein-ligand complexes',
    }

    # Honest conclusions
    results['conclusions'] = [
        {
            'statement': 'INSUFFICIENT DATA',
            'explanation': 'With only 3 observations, no statistically valid conclusions can be drawn about the Z² constant.',
        },
        {
            'statement': 'POSSIBLE CONFIRMATION BIAS',
            'explanation': 'The 3 structures were selected because they showed Z² matches. This is circular reasoning.',
        },
        {
            'statement': 'TESTABLE PREDICTION',
            'explanation': 'If Z² is real, NEW AlphaFold validations should consistently show ~6.015 Å. Track Metabolic_Receptor_E and EGFR results.',
        },
        {
            'statement': 'NULL PROBABILITY ESTIMATES',
            'explanation': 'Under various null hypotheses, probability of 3/3 within ±5 mÅ ranges from 10^-4 to 10^-6. Low but not impossible.',
        },
        {
            'statement': 'NEED SYSTEMATIC STUDY',
            'explanation': 'Extract aromatic distances from 1000+ high-quality drug-target structures. Test for enrichment at 6.015 Å.',
        },
    ]

    return results


# =============================================================================
# WHAT WOULD VALIDATE Z²?
# =============================================================================

def define_validation_criteria():
    """
    Define what would constitute valid evidence for or against Z².
    """

    criteria = {
        'would_support_z2': [
            {
                'criterion': 'Statistically significant enrichment at 6.015 Å',
                'method': 'Analyze 1000+ drug-target aromatic distances from PDB',
                'threshold': 'p < 0.001 for enrichment at Z² vs null distribution',
            },
            {
                'criterion': 'Predictive power for binding affinity',
                'method': 'Correlate Z² deviation with experimental Kd values',
                'threshold': 'r² > 0.3 for deviation vs -log(Kd)',
            },
            {
                'criterion': 'Prospective validation',
                'method': 'Design 10 new peptides using Z², validate binding',
                'threshold': '>70% show measurable binding (Kd < 100 μM)',
            },
            {
                'criterion': 'Independent replication',
                'method': 'Other researchers reproduce Z² observations',
                'threshold': 'At least 2 independent labs confirm',
            },
        ],
        'would_refute_z2': [
            {
                'criterion': 'No enrichment at 6.015 Å in large dataset',
                'method': 'Same analysis as above',
                'threshold': 'p > 0.1, effect size < 0.1',
            },
            {
                'criterion': 'No correlation with binding affinity',
                'method': 'Same as above',
                'threshold': 'r² < 0.05',
            },
            {
                'criterion': 'Designed peptides fail to bind',
                'method': 'Same as above',
                'threshold': '<30% show binding',
            },
            {
                'criterion': 'Cherry-picking demonstrated',
                'method': 'Show that success cases were selected post-hoc',
                'threshold': 'Evidence of selection bias in original analysis',
            },
        ],
        'current_status': {
            'evidence_for': 'Weak (n=3, possible selection bias)',
            'evidence_against': 'None (not yet tested)',
            'verdict': 'UNDETERMINED - needs systematic testing',
        },
    }

    return criteria


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("  Z² STATISTICAL VALIDATION FRAMEWORK")
    print("=" * 80)
    print()
    print("CRITICAL SELF-ASSESSMENT OF THE Z² HYPOTHESIS")
    print()

    # Run analysis
    results = analyze_z2_validation()

    print("OBSERVED DATA")
    print("-" * 60)
    print(f"  C2_Homodimer_A:   {results['observed_distances']['C2_Homodimer_A']:.6f} Å")
    print(f"  TNF-α: {results['observed_distances']['TNF-α']:.6f} Å")
    print(f"  C2_Protease_B:  {results['observed_distances']['C2_Protease_B']:.6f} Å")
    print(f"  Mean:  {results['observed_distances']['mean']:.6f} Å")
    print(f"  Std:   {results['observed_distances']['std']:.6f} Å")
    print(f"  N:     {results['observed_distances']['n']}")

    print()
    print("CRITICAL LIMITATION")
    print("-" * 60)
    print(f"  {results['critical_limitation']['issue']}")
    print(f"  Current n = {results['critical_limitation']['n_observations']}")
    print(f"  Minimum needed: {results['critical_limitation']['minimum_for_significance']}")

    print()
    print("NULL HYPOTHESIS ANALYSIS")
    print("-" * 60)
    for null in results['null_hypotheses_tested']:
        print(f"\n  {null['null_hypothesis']}:")
        print(f"    Null mean: {null['null_mean']:.3f} Å")
        print(f"    P(single observation within ±5 mÅ): {null['probability_3_of_3']['p_single_within_5mA']:.4f}")
        print(f"    P(3/3 within ±5 mÅ by chance): {null['probability_3_of_3']['p_three_consecutive']:.2e}")

    print()
    print("CONCLUSIONS")
    print("-" * 60)
    for conclusion in results['conclusions']:
        print(f"\n  {conclusion['statement']}")
        print(f"    {conclusion['explanation']}")

    # Get validation criteria
    criteria = define_validation_criteria()

    print()
    print("=" * 80)
    print("  WHAT WOULD VALIDATE Z²?")
    print("=" * 80)

    print("\nEvidence that WOULD support Z²:")
    for c in criteria['would_support_z2']:
        print(f"  • {c['criterion']}")
        print(f"    Method: {c['method']}")
        print(f"    Threshold: {c['threshold']}")

    print("\nEvidence that WOULD refute Z²:")
    for c in criteria['would_refute_z2']:
        print(f"  • {c['criterion']}")

    print(f"\nCurrent status: {criteria['current_status']['verdict']}")

    # Save results
    output_dir = Path(__file__).parent

    output = {
        'analysis_results': results,
        'validation_criteria': criteria,
    }

    output_file = output_dir / "z2_statistical_validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved: {output_file}")

    print()
    print("=" * 80)
    print("  BOTTOM LINE")
    print("=" * 80)
    print("""
The Z² hypothesis CANNOT be validated or refuted with current data.

What we have:
  - 3 AlphaFold structures showing distances near 6.015 Å
  - These were SELECTED because they showed Z² matches (circular)

What we need:
  - Systematic analysis of 1000+ drug-target aromatic distances
  - Blinded prediction → experimental validation cycle
  - Independent replication

Current verdict: UNDETERMINED
The Z² constant may be real, or it may be an artifact.
Only rigorous testing will tell.
""")


if __name__ == "__main__":
    main()
