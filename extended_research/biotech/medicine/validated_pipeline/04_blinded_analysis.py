#!/usr/bin/env python3
"""
04_blinded_analysis.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

04_blinded_analysis.py - Blinded Statistical Analysis

PURPOSE:
Implement Gemini's "Blinded Data Analysis" prompt.
Test whether Z² = 9.14 Å is statistically special WITHOUT knowing the answer beforehand.

METHODOLOGY:
1. Load raw persistent homology data (death radii)
2. Generate 1000+ random "candidate constants" uniformly sampled
3. Score how well EACH constant matches the data
4. Where does Z² = 9.14 Å rank among random constants?

CRITICAL: If Z² ranks in top 5% = meaningful. Otherwise = random.

BLINDING PROTOCOL:
- Analysis code written BEFORE seeing results
- Z² value not used in scoring function
- All constants tested identically
- Results reveal Z² rank at the very end

Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
from typing import List, Dict, Tuple
import sys

# Strict random seed
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

DATA_DIR = Path(__file__).parent / "results"
OUTPUT_DIR = Path(__file__).parent / "results"
LOG_DIR = Path(__file__).parent / "logs"

for d in [DATA_DIR, OUTPUT_DIR, LOG_DIR]:
    d.mkdir(exist_ok=True)

print("=" * 80)
print("BLINDED STATISTICAL ANALYSIS")
print("Testing Z² against random constants - NO PEEKING")
print("=" * 80)
print()


# =============================================================================
# BLINDING: DEFINE Z² ONLY AT THE END
# =============================================================================

# This constant is ONLY used to report the final rank.
# The scoring functions NEVER see this value during analysis.
Z_SQUARED_VALUE = 32 * np.pi / 3  # ~33.51
R_NATURAL_VALUE = np.sqrt(Z_SQUARED_VALUE)  # ~5.79 Å? Wait, let me recalculate

# Actually from the prior work:
# Z² = 32π/3 ≈ 33.51
# r_natural = √(32π/3) ≈ 5.79 Å
# But the claim was 9.14 Å... let me check the physics

# From ZIMMERMAN_FORMULA.md:
# Actually the r_natural comes from a different derivation
# Let me use the empirically claimed value
Z2_CLAIMED_RADIUS = 9.14  # Å - the claimed "natural scale"

# Alternative interpretations to test
Z2_ALTERNATIVES = {
    'z2_claimed': 9.14,
    'z2_sqrt': np.sqrt(32 * np.pi / 3),  # 5.79 Å
    'z2_value': 32 * np.pi / 3,  # 33.51 - too large for death radii
    'z2_half': 9.14 / 2,  # 4.57 Å
    'z2_double': 9.14 * 2,  # 18.28 Å
}


# =============================================================================
# DATA LOADING
# =============================================================================

def load_death_radii(csv_file: Path) -> List[float]:
    """
    Load H1 death radii from aggregate CSV.

    STRICT: Raises if file doesn't exist or is empty.
    """
    if not csv_file.exists():
        raise FileNotFoundError(f"Data file not found: {csv_file}")

    radii = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                radius = float(row['h1_death_radius'])
                if np.isfinite(radius) and radius > 0:
                    radii.append(radius)
            except (ValueError, KeyError):
                continue

    if len(radii) == 0:
        raise ValueError(f"No valid death radii found in {csv_file}")

    print(f"Loaded {len(radii)} death radii from {csv_file.name}")
    return radii


def load_from_json(json_file: Path) -> List[float]:
    """
    Alternative: Load death radii from JSON results file.
    """
    if not json_file.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    with open(json_file, 'r') as f:
        data = json.load(f)

    radii = []

    for protein in data.get('proteins', []):
        if 'diagrams' in protein and 'H1' in protein['diagrams']:
            h1 = protein['diagrams']['H1']
            for death in h1.get('death', []):
                if np.isfinite(death) and death > 0:
                    radii.append(death)

    if len(radii) == 0:
        raise ValueError(f"No valid death radii found in {json_file}")

    print(f"Loaded {len(radii)} death radii from {json_file.name}")
    return radii


# =============================================================================
# SCORING FUNCTIONS (BLINDED - NO Z² KNOWLEDGE)
# =============================================================================

def score_constant_match(
    constant: float,
    death_radii: np.ndarray,
    tolerance: float = 0.10,
) -> Dict[str, float]:
    """
    Score how well a constant matches the death radii distribution.

    BLINDED: This function knows NOTHING about Z².
    It just measures how well any constant explains the data.

    Metrics:
    1. Fraction of radii within tolerance of constant or its multiples
    2. Mean deviation from nearest multiple
    3. Correlation with constant multiples
    """
    radii = np.array(death_radii)

    # Metric 1: Fraction matching constant or multiples (1x, 2x, 3x, 4x)
    multiples = [1, 2, 3, 4]
    matches = 0

    for r in radii:
        for m in multiples:
            expected = constant * m
            if abs(r - expected) / expected <= tolerance:
                matches += 1
                break  # Count each radius only once

    fraction_matching = matches / len(radii)

    # Metric 2: Mean deviation from nearest multiple
    deviations = []
    for r in radii:
        nearest_multiple = round(r / constant) * constant
        if nearest_multiple > 0:
            rel_dev = abs(r - nearest_multiple) / nearest_multiple
            deviations.append(rel_dev)

    mean_deviation = float(np.mean(deviations)) if deviations else 1.0

    # Metric 3: Composite score (higher = better match)
    # Penalize deviation, reward matching
    composite_score = fraction_matching - mean_deviation

    return {
        'constant': float(constant),
        'fraction_matching': float(fraction_matching),
        'mean_deviation': float(mean_deviation),
        'composite_score': float(composite_score),
        'n_radii': len(radii),
    }


def score_peak_alignment(
    constant: float,
    death_radii: np.ndarray,
) -> Dict[str, float]:
    """
    Score whether peaks in the distribution align with constant multiples.

    BLINDED: No knowledge of Z².
    """
    radii = np.array(death_radii)

    # Create histogram
    bins = np.linspace(0, radii.max() * 1.1, 50)
    hist, bin_edges = np.histogram(radii, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Find peaks (local maxima)
    peaks = []
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i-1] and hist[i] > hist[i+1] and hist[i] > 2:
            peaks.append(bin_centers[i])

    if len(peaks) == 0:
        return {
            'constant': float(constant),
            'peak_alignment_score': 0.0,
            'n_peaks': 0,
        }

    # Score alignment: how close are peaks to multiples of constant?
    alignments = []
    for peak in peaks:
        nearest_multiple = round(peak / constant) * constant
        if nearest_multiple > 0:
            alignment = 1 - abs(peak - nearest_multiple) / constant
            alignments.append(max(0, alignment))

    return {
        'constant': float(constant),
        'peak_alignment_score': float(np.mean(alignments)),
        'n_peaks': len(peaks),
        'peaks': [float(p) for p in peaks],
    }


# =============================================================================
# BLINDED ANALYSIS
# =============================================================================

def generate_random_constants(
    n_constants: int,
    min_value: float,
    max_value: float,
) -> np.ndarray:
    """
    Generate uniformly distributed random constants for comparison.

    These constants have NO relationship to Z².
    """
    np.random.seed(RANDOM_SEED)
    return np.random.uniform(min_value, max_value, n_constants)


def run_blinded_analysis(
    death_radii: List[float],
    n_random: int = 1000,
) -> Dict:
    """
    Run complete blinded analysis.

    Protocol:
    1. Generate 1000 random constants
    2. Score ALL constants (including random)
    3. Rank all constants by score
    4. ONLY AT THE END: reveal where Z² ranks
    """
    radii = np.array(death_radii)

    # Determine range for random constants
    r_min = radii.min() * 0.5
    r_max = radii.max() * 0.5  # Expect constants to be smaller than max death radius

    print(f"\nGenerating {n_random} random constants in range [{r_min:.2f}, {r_max:.2f}]...")
    random_constants = generate_random_constants(n_random, r_min, r_max)

    # Score all random constants
    print("Scoring random constants (BLINDED)...")
    random_scores = []

    for i, const in enumerate(random_constants):
        score = score_constant_match(const, radii)
        random_scores.append(score)

        if (i + 1) % 100 == 0:
            print(f"  Scored {i + 1}/{n_random}...")

    # Extract composite scores
    all_composites = np.array([s['composite_score'] for s in random_scores])

    print(f"\nRandom constant score distribution:")
    print(f"  Min: {all_composites.min():.4f}")
    print(f"  Max: {all_composites.max():.4f}")
    print(f"  Mean: {np.mean(all_composites):.4f}")
    print(f"  Std: {np.std(all_composites):.4f}")
    print(f"  95th percentile: {np.percentile(all_composites, 95):.4f}")

    # Store random results for output
    results = {
        'n_random_constants': n_random,
        'constant_range': [float(r_min), float(r_max)],
        'random_score_stats': {
            'min': float(all_composites.min()),
            'max': float(all_composites.max()),
            'mean': float(np.mean(all_composites)),
            'std': float(np.std(all_composites)),
            'p95': float(np.percentile(all_composites, 95)),
            'p99': float(np.percentile(all_composites, 99)),
        },
        'z2_analysis': {},
    }

    # =========================================================================
    # UNBLINDING: NOW test Z² values
    # =========================================================================

    print("\n" + "=" * 80)
    print("UNBLINDING: Testing Z² values")
    print("=" * 80)

    for name, z2_value in Z2_ALTERNATIVES.items():
        z2_score = score_constant_match(z2_value, radii)
        z2_peak = score_peak_alignment(z2_value, radii)

        # Where does Z² rank among random constants?
        n_better = np.sum(all_composites > z2_score['composite_score'])
        percentile = 100 * (1 - n_better / n_random)

        results['z2_analysis'][name] = {
            'value': float(z2_value),
            'score': z2_score,
            'peak_alignment': z2_peak,
            'rank_percentile': float(percentile),
            'n_random_better': int(n_better),
            'is_significant': bool(percentile >= 95),
        }

        sig_marker = "✓ SIGNIFICANT" if percentile >= 95 else "✗ NOT SIGNIFICANT"
        print(f"\n{name} = {z2_value:.4f} Å:")
        print(f"  Composite score: {z2_score['composite_score']:.4f}")
        print(f"  Fraction matching: {z2_score['fraction_matching']:.4f}")
        print(f"  Percentile rank: {percentile:.1f}% {sig_marker}")

    # Best Z² variant
    best_z2 = max(
        results['z2_analysis'].items(),
        key=lambda x: x[1]['rank_percentile']
    )
    results['best_z2_variant'] = {
        'name': best_z2[0],
        'value': best_z2[1]['value'],
        'percentile': best_z2[1]['rank_percentile'],
        'is_significant': best_z2[1]['is_significant'],
    }

    # Best random constant (for comparison)
    best_random_idx = np.argmax(all_composites)
    best_random = random_scores[best_random_idx]
    results['best_random_constant'] = {
        'value': best_random['constant'],
        'composite_score': best_random['composite_score'],
    }

    return results


# =============================================================================
# FINAL VERDICT
# =============================================================================

def generate_verdict(results: Dict) -> str:
    """
    Generate final verdict based on blinded analysis.

    This is the HONEST assessment.
    """
    verdict_lines = []
    verdict_lines.append("=" * 80)
    verdict_lines.append("BLINDED ANALYSIS VERDICT")
    verdict_lines.append("=" * 80)

    best_z2 = results['best_z2_variant']

    if best_z2['is_significant']:
        verdict_lines.append(f"""
RESULT: Z² = {best_z2['value']:.4f} Å ranks in the {best_z2['percentile']:.1f}th percentile

This means Z² performs BETTER than {best_z2['percentile']:.1f}% of random constants.

INTERPRETATION:
If Z² were random, we'd expect ~50th percentile.
Being in the {best_z2['percentile']:.1f}th percentile is {"statistically significant" if best_z2['percentile'] >= 95 else "borderline"}.

VERDICT: Z² shows {"MEANINGFUL" if best_z2['percentile'] >= 95 else "WEAK"} correlation with death radii.
""")
    else:
        verdict_lines.append(f"""
RESULT: Z² = {best_z2['value']:.4f} Å ranks in the {best_z2['percentile']:.1f}th percentile

This means Z² performs NO BETTER than {100 - best_z2['percentile']:.1f}% of random constants.

INTERPRETATION:
Z² is NOT statistically special. A random constant has equal or better
explanatory power {100 - best_z2['percentile']:.1f}% of the time.

VERDICT: Z² shows NO SIGNIFICANT correlation with death radii.

The Z² framework appears to be numerological coincidence, not physics.
""")

    # Add comparison with best random
    best_random = results['best_random_constant']
    verdict_lines.append(f"""
For comparison:
  Best random constant: {best_random['value']:.4f} Å
  Best Z² variant: {best_z2['value']:.4f} Å ({best_z2['name']})

The best random constant explains the data {"better" if best_random['composite_score'] > results['z2_analysis'][best_z2['name']]['score']['composite_score'] else "similarly to"} Z².
""")

    verdict_lines.append("=" * 80)

    return '\n'.join(verdict_lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""

    # Try to load data from multiple sources
    csv_file = DATA_DIR / "h1_death_radii_aggregate.csv"
    json_file = DATA_DIR / "persistent_homology_results.json"

    death_radii = None

    if csv_file.exists():
        try:
            death_radii = load_death_radii(csv_file)
        except Exception as e:
            print(f"Could not load CSV: {e}")

    if death_radii is None and json_file.exists():
        try:
            death_radii = load_from_json(json_file)
        except Exception as e:
            print(f"Could not load JSON: {e}")

    if death_radii is None:
        print("\n" + "=" * 80)
        print("NO DATA AVAILABLE")
        print("=" * 80)
        print(f"""
Cannot run blinded analysis without data.

Please run in order:
1. 01_data_provenance.py - Fetch PDB structures
2. 03_strict_persistent_homology.py - Compute death radii
3. Then run this script

Expected data files:
  {csv_file}
  OR
  {json_file}
""")
        sys.exit(1)

    # Run blinded analysis
    print(f"\nRunning blinded analysis on {len(death_radii)} death radii...")
    results = run_blinded_analysis(death_radii, n_random=1000)

    # Add metadata
    results['timestamp'] = datetime.now().isoformat()
    results['random_seed'] = RANDOM_SEED
    results['n_death_radii'] = len(death_radii)
    results['death_radii_stats'] = {
        'min': float(np.min(death_radii)),
        'max': float(np.max(death_radii)),
        'mean': float(np.mean(death_radii)),
        'median': float(np.median(death_radii)),
        'std': float(np.std(death_radii)),
    }

    # Generate verdict
    verdict = generate_verdict(results)
    results['verdict'] = verdict

    print(verdict)

    # Save results
    output_file = OUTPUT_DIR / "blinded_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved: {output_file}")

    # Save verdict separately
    verdict_file = OUTPUT_DIR / "blinded_analysis_verdict.txt"
    with open(verdict_file, 'w') as f:
        f.write(verdict)

    print(f"Verdict saved: {verdict_file}")

    return results


if __name__ == "__main__":
    results = main()
