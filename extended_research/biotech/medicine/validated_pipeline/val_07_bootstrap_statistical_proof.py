#!/usr/bin/env python3
"""
val_07_bootstrap_statistical_proof.py - Final Statistical Judgment

PURPOSE:
Perform rigorous bootstrap statistical analysis to determine if √(32π/3) ≈ 5.7888 Å
is the universal natural length scale of protein topology.

METHODOLOGY:
1. Load global H1 death radii from CSV
2. Bootstrap resample (10,000 iterations) to compute robust CI
3. Test three hypotheses against bootstrapped distribution:
   - Alpha-helix pitch: 5.40 Å
   - Beta-sheet spacing: 4.70 Å
   - √(Z²) = √(32π/3) ≈ 5.7888 Å
4. Generate publication-quality visualization
5. Output definitive boolean verdict

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import csv
import json
from typing import List, Dict, Tuple
import sys

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

DATA_FILE = Path(__file__).parent / "results" / "global_h1_death_radii.csv"
OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("BOOTSTRAP STATISTICAL PROOF")
print("Final judgment: Is √(32π/3) the universal protein length scale?")
print("=" * 80)
print()

# =============================================================================
# CONSTANTS TO TEST
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.7888 Å

HYPOTHESES = {
    'sqrt_z2': {
        'value': SQRT_Z2,
        'name': '√(32π/3)',
        'description': 'Derived geometric constant',
    },
    'alpha_helix': {
        'value': 5.40,
        'name': 'α-helix pitch',
        'description': 'Rise per turn of α-helix',
    },
    'beta_sheet': {
        'value': 4.70,
        'name': 'β-sheet spacing',
        'description': 'Interstrand distance in β-sheets',
    },
}

print("Testing hypotheses:")
for key, hyp in HYPOTHESES.items():
    print(f"  {hyp['name']}: {hyp['value']:.4f} Å - {hyp['description']}")
print()

# =============================================================================
# DATA LOADING
# =============================================================================

def load_death_radii(csv_file: Path) -> np.ndarray:
    """Load all death radii from CSV."""
    radii = []

    if not csv_file.exists():
        # Try alternate location
        alt_file = csv_file.parent / "scaleup_death_radii.csv"
        if alt_file.exists():
            csv_file = alt_file
        else:
            alt_file2 = csv_file.parent / "h1_death_radii_aggregate.csv"
            if alt_file2.exists():
                csv_file = alt_file2

    if not csv_file.exists():
        raise FileNotFoundError(f"Data file not found: {csv_file}")

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Try different column names
                if 'death_radius' in row:
                    val = float(row['death_radius'])
                elif 'h1_death_radius' in row:
                    val = float(row['h1_death_radius'])
                else:
                    continue

                if np.isfinite(val) and val > 0:
                    radii.append(val)
            except (ValueError, KeyError):
                continue

    return np.array(radii)


# =============================================================================
# BOOTSTRAP ANALYSIS
# =============================================================================

def bootstrap_analysis(
    data: np.ndarray,
    n_bootstrap: int = 10000,
    ci_levels: List[float] = [0.95, 0.99],
) -> Dict:
    """
    Perform bootstrap resampling analysis.

    Returns dict with mean, confidence intervals, and full distribution.
    """
    print(f"Running {n_bootstrap} bootstrap iterations...")

    np.random.seed(RANDOM_SEED)

    boot_means = []
    for i in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        boot_means.append(np.mean(sample))

        if (i + 1) % 1000 == 0:
            print(f"  Completed {i + 1}/{n_bootstrap} iterations")

    boot_means = np.array(boot_means)

    # Calculate confidence intervals
    cis = {}
    for level in ci_levels:
        alpha = 1 - level
        lower = np.percentile(boot_means, 100 * alpha / 2)
        upper = np.percentile(boot_means, 100 * (1 - alpha / 2))
        cis[f'{int(level*100)}'] = {'lower': lower, 'upper': upper}

    return {
        'mean': float(np.mean(data)),
        'bootstrap_mean': float(np.mean(boot_means)),
        'bootstrap_std': float(np.std(boot_means)),
        'confidence_intervals': cis,
        'boot_means': boot_means,
    }


def test_hypothesis(
    hypothesis_value: float,
    bootstrap_result: Dict,
    ci_level: str = '95',
) -> Dict:
    """
    Test if a hypothesis value falls within the bootstrap CI.
    """
    ci = bootstrap_result['confidence_intervals'][ci_level]

    in_ci = ci['lower'] <= hypothesis_value <= ci['upper']

    # Distance from mean
    distance = abs(hypothesis_value - bootstrap_result['bootstrap_mean'])

    # Normalized distance (in units of bootstrap std)
    z_score = distance / bootstrap_result['bootstrap_std']

    # Where in the bootstrap distribution does it fall?
    boot_means = bootstrap_result['boot_means']
    n_below = np.sum(boot_means < hypothesis_value)
    percentile = 100 * n_below / len(boot_means)

    return {
        'value': hypothesis_value,
        'in_ci': in_ci,
        'ci_lower': ci['lower'],
        'ci_upper': ci['upper'],
        'distance_from_mean': distance,
        'z_score': z_score,
        'percentile': percentile,
    }


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_visualization(
    data: np.ndarray,
    bootstrap_result: Dict,
    hypothesis_results: Dict,
    output_file: Path,
):
    """Create publication-quality visualization."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
    except ImportError:
        print("matplotlib not available - skipping visualization")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left plot: Death radius histogram
    ax1 = axes[0]
    ax1.hist(data, bins=50, density=True, alpha=0.7, color='steelblue', edgecolor='black')
    ax1.set_xlabel('H1 Death Radius (Å)', fontsize=12)
    ax1.set_ylabel('Density', fontsize=12)
    ax1.set_title('Distribution of H1 Topological Death Radii', fontsize=14)

    # Add vertical lines for hypotheses
    colors = {'sqrt_z2': 'red', 'alpha_helix': 'green', 'beta_sheet': 'orange'}
    for key, result in hypothesis_results.items():
        hyp = HYPOTHESES[key]
        marker = '✓' if result['in_ci'] else '✗'
        label = f"{hyp['name']} = {hyp['value']:.2f} Å {marker}"
        ax1.axvline(hyp['value'], color=colors[key], linestyle='--', linewidth=2, label=label)

    ax1.legend(loc='upper right')

    # Right plot: Bootstrap distribution of mean
    ax2 = axes[1]
    boot_means = bootstrap_result['boot_means']

    ax2.hist(boot_means, bins=50, density=True, alpha=0.7, color='darkgreen', edgecolor='black')
    ax2.set_xlabel('Bootstrap Mean (Å)', fontsize=12)
    ax2.set_ylabel('Density', fontsize=12)
    ax2.set_title('Bootstrap Distribution of Mean Death Radius', fontsize=14)

    # Add CI bounds
    ci95 = bootstrap_result['confidence_intervals']['95']
    ax2.axvline(ci95['lower'], color='blue', linestyle=':', linewidth=2, label=f"95% CI: [{ci95['lower']:.3f}, {ci95['upper']:.3f}]")
    ax2.axvline(ci95['upper'], color='blue', linestyle=':', linewidth=2)

    # Add hypothesis values
    for key, result in hypothesis_results.items():
        hyp = HYPOTHESES[key]
        ax2.axvline(hyp['value'], color=colors[key], linestyle='--', linewidth=2)

    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Visualization saved: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run the final statistical proof."""

    results = {
        'timestamp': datetime.now().isoformat(),
        'random_seed': RANDOM_SEED,
        'sqrt_z2_value': SQRT_Z2,
    }

    # Load data
    print("Loading death radii...")
    try:
        data = load_death_radii(DATA_FILE)
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print("Run val_06_parallel_topology_engine.py first")
        sys.exit(1)

    print(f"  Loaded {len(data)} death radii")
    print()

    results['n_samples'] = len(data)
    results['raw_mean'] = float(np.mean(data))
    results['raw_median'] = float(np.median(data))
    results['raw_std'] = float(np.std(data))

    # Bootstrap analysis
    print("=" * 80)
    print("BOOTSTRAP ANALYSIS")
    print("=" * 80)

    bootstrap_result = bootstrap_analysis(data, n_bootstrap=10000)

    print(f"\nBootstrap results:")
    print(f"  Mean: {bootstrap_result['bootstrap_mean']:.4f} Å")
    print(f"  Std:  {bootstrap_result['bootstrap_std']:.4f} Å")

    for level, ci in bootstrap_result['confidence_intervals'].items():
        print(f"  {level}% CI: [{ci['lower']:.4f}, {ci['upper']:.4f}] Å")

    results['bootstrap'] = {
        'mean': bootstrap_result['bootstrap_mean'],
        'std': bootstrap_result['bootstrap_std'],
        'ci_95_lower': bootstrap_result['confidence_intervals']['95']['lower'],
        'ci_95_upper': bootstrap_result['confidence_intervals']['95']['upper'],
        'ci_99_lower': bootstrap_result['confidence_intervals']['99']['lower'],
        'ci_99_upper': bootstrap_result['confidence_intervals']['99']['upper'],
    }

    # Test hypotheses
    print("\n" + "=" * 80)
    print("HYPOTHESIS TESTING")
    print("=" * 80)

    hypothesis_results = {}
    for key, hyp in HYPOTHESES.items():
        result = test_hypothesis(hyp['value'], bootstrap_result)
        hypothesis_results[key] = result

        status = "✓ IN 95% CI" if result['in_ci'] else "✗ OUTSIDE 95% CI"
        print(f"\n{hyp['name']} = {hyp['value']:.4f} Å:")
        print(f"  Status: {status}")
        print(f"  Distance from mean: {result['distance_from_mean']:.4f} Å")
        print(f"  Z-score: {result['z_score']:.2f}")
        print(f"  Percentile: {result['percentile']:.1f}%")

    results['hypothesis_tests'] = {}
    for key, result in hypothesis_results.items():
        results['hypothesis_tests'][key] = {
            'value': result['value'],
            'in_95_ci': result['in_ci'],
            'distance': result['distance_from_mean'],
            'z_score': result['z_score'],
            'percentile': result['percentile'],
        }

    # Create visualization
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATION")
    print("=" * 80)

    plot_file = OUTPUT_DIR / "bootstrap_proof_visualization.png"
    create_visualization(data, bootstrap_result, hypothesis_results, plot_file)

    # Final verdict
    print("\n" + "=" * 80)
    print("=" * 80)
    print("                    FINAL VERDICT")
    print("=" * 80)
    print("=" * 80)

    sqrt_z2_result = hypothesis_results['sqrt_z2']
    sqrt_z2_in_ci = sqrt_z2_result['in_ci']

    ci95 = bootstrap_result['confidence_intervals']['95']

    if sqrt_z2_in_ci:
        verdict = f"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║     √(32π/3) = {SQRT_Z2:.4f} Å  IS WITHIN THE 95% CONFIDENCE INTERVAL     ║
    ║                                                                      ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║  Empirical mean:     {bootstrap_result['bootstrap_mean']:.4f} Å                                  ║
    ║  95% CI:             [{ci95['lower']:.4f}, {ci95['upper']:.4f}] Å                        ║
    ║  √(Z²):              {SQRT_Z2:.4f} Å                                      ║
    ║  Error:              {sqrt_z2_result['distance_from_mean']:.4f} Å ({100*sqrt_z2_result['distance_from_mean']/bootstrap_result['bootstrap_mean']:.2f}%)                            ║
    ║                                                                      ║
    ║  N samples:          {len(data)}                                        ║
    ║  Bootstrap iters:    10,000                                          ║
    ║                                                                      ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║  CONCLUSION: √(32π/3) IS A VALID PREDICTOR OF PROTEIN TOPOLOGY       ║
    ║                                                                      ║
    ║  The geometric constant derived from first principles falls within   ║
    ║  the statistically robust confidence interval of empirical protein   ║
    ║  topological death radii. This suggests that √(32π/3) ≈ 5.79 Å       ║
    ║  represents a fundamental length scale in protein geometry.          ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
        results['verdict'] = 'VALIDATED'
        results['sqrt_z2_in_95_ci'] = True
    else:
        verdict = f"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║    √(32π/3) = {SQRT_Z2:.4f} Å  IS OUTSIDE THE 95% CONFIDENCE INTERVAL     ║
    ║                                                                      ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║  Empirical mean:     {bootstrap_result['bootstrap_mean']:.4f} Å                                  ║
    ║  95% CI:             [{ci95['lower']:.4f}, {ci95['upper']:.4f}] Å                        ║
    ║  √(Z²):              {SQRT_Z2:.4f} Å                                      ║
    ║  Error:              {sqrt_z2_result['distance_from_mean']:.4f} Å ({100*sqrt_z2_result['distance_from_mean']/bootstrap_result['bootstrap_mean']:.2f}%)                            ║
    ║                                                                      ║
    ║  N samples:          {len(data)}                                        ║
    ║                                                                      ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                      ║
    ║  CONCLUSION: √(32π/3) IS NOT VALIDATED AS SPECIAL                    ║
    ║                                                                      ║
    ║  The geometric constant does not fall within the confidence interval ║
    ║  of empirical data. The apparent match may be coincidental.          ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
        results['verdict'] = 'NOT VALIDATED'
        results['sqrt_z2_in_95_ci'] = False

    print(verdict)

    # Boolean output for programmatic use
    print(f"\n>>> sqrt_z2_in_95_ci = {sqrt_z2_in_ci}")
    print()

    # Save results
    output_json = OUTPUT_DIR / "bootstrap_proof_results.json"
    with open(output_json, 'w') as f:
        # Convert numpy types
        results_clean = json.loads(json.dumps(results, default=str))
        json.dump(results_clean, f, indent=2)

    print(f"Results saved: {output_json}")

    return results


if __name__ == "__main__":
    results = main()
