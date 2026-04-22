#!/usr/bin/env python3
"""
val_08_aggregate_and_final_proof.py

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

val_08_aggregate_and_final_proof.py - Aggregate All Data and Final Verdict

PURPOSE:
Aggregate H1 death radii from all available sources and run
definitive bootstrap statistical analysis.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import csv
import json
import sys

np.random.seed(42)

RESULTS_DIR = Path(__file__).parent / "results"
OUTPUT_FILE = RESULTS_DIR / "FINAL_AGGREGATE_BOOTSTRAP_RESULTS.json"

print("=" * 80)
print("FINAL AGGREGATE BOOTSTRAP PROOF")
print("Collecting all H1 death radii and computing definitive verdict")
print("=" * 80)
print()

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.7888 Å

# =============================================================================
# DATA AGGREGATION
# =============================================================================

def collect_all_h1_deaths() -> np.ndarray:
    """Collect H1 death radii from all available sources."""
    all_deaths = []
    sources = []

    # Source 1: Individual H1 raw files
    h1_files = list(RESULTS_DIR.glob("*_H1_raw.csv"))
    for f in h1_files:
        try:
            with open(f, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    # Try different column names
                    val = None
                    for col in ['death', 'death_radius', 'Death', 'death_time']:
                        if col in row:
                            try:
                                val = float(row[col])
                                break
                            except:
                                pass
                    if val is not None and np.isfinite(val) and val > 0:
                        all_deaths.append(val)
                        count += 1
                if count > 0:
                    sources.append(f"H1_raw: {f.stem} ({count} deaths)")
        except Exception as e:
            pass

    # Source 2: Global death radii CSV
    global_csv = RESULTS_DIR / "global_h1_death_radii.csv"
    if global_csv.exists():
        try:
            with open(global_csv, 'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    try:
                        val = float(row['death_radius'])
                        if np.isfinite(val) and val > 0:
                            all_deaths.append(val)
                            count += 1
                    except:
                        pass
                if count > 0:
                    sources.append(f"global_h1_death_radii.csv ({count} deaths)")
        except:
            pass

    # Source 3: Scaleup death radii
    scaleup_csv = RESULTS_DIR / "scaleup_death_radii.csv"
    if scaleup_csv.exists():
        try:
            with open(scaleup_csv, 'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    for col in ['death_radius', 'h1_death_radius']:
                        if col in row:
                            try:
                                val = float(row[col])
                                if np.isfinite(val) and val > 0:
                                    all_deaths.append(val)
                                    count += 1
                                    break
                            except:
                                pass
                if count > 0:
                    sources.append(f"scaleup_death_radii.csv ({count} deaths)")
        except:
            pass

    # Source 4: Aggregate file
    agg_csv = RESULTS_DIR / "h1_death_radii_aggregate.csv"
    if agg_csv.exists():
        try:
            with open(agg_csv, 'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    for col in ['death_radius', 'h1_death_radius', 'death']:
                        if col in row:
                            try:
                                val = float(row[col])
                                if np.isfinite(val) and val > 0:
                                    all_deaths.append(val)
                                    count += 1
                                    break
                            except:
                                pass
                if count > 0:
                    sources.append(f"h1_death_radii_aggregate.csv ({count} deaths)")
        except:
            pass

    print(f"Data sources collected:")
    for s in sources[:10]:
        print(f"  - {s}")
    if len(sources) > 10:
        print(f"  ... and {len(sources) - 10} more")
    print()

    return np.array(all_deaths), sources


# =============================================================================
# BOOTSTRAP ANALYSIS
# =============================================================================

def bootstrap_ci(data: np.ndarray, n_bootstrap: int = 10000) -> dict:
    """Compute bootstrap confidence intervals."""
    print(f"Running {n_bootstrap} bootstrap iterations...")

    np.random.seed(42)

    boot_means = []
    for i in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        boot_means.append(np.mean(sample))
        if (i + 1) % 2000 == 0:
            print(f"  {i + 1}/{n_bootstrap}")

    boot_means = np.array(boot_means)

    return {
        'mean': float(np.mean(data)),
        'bootstrap_mean': float(np.mean(boot_means)),
        'bootstrap_std': float(np.std(boot_means)),
        'ci_95_lower': float(np.percentile(boot_means, 2.5)),
        'ci_95_upper': float(np.percentile(boot_means, 97.5)),
        'ci_99_lower': float(np.percentile(boot_means, 0.5)),
        'ci_99_upper': float(np.percentile(boot_means, 99.5)),
        'boot_means': boot_means,
    }


def test_hypothesis(value: float, name: str, bootstrap: dict) -> dict:
    """Test if a hypothesis value is within the bootstrap CI."""
    in_95_ci = bootstrap['ci_95_lower'] <= value <= bootstrap['ci_95_upper']
    in_99_ci = bootstrap['ci_99_lower'] <= value <= bootstrap['ci_99_upper']

    distance = abs(value - bootstrap['bootstrap_mean'])
    z_score = distance / bootstrap['bootstrap_std']

    # Percentile in bootstrap distribution
    n_below = np.sum(bootstrap['boot_means'] < value)
    percentile = 100 * n_below / len(bootstrap['boot_means'])

    return {
        'name': name,
        'value': value,
        'in_95_ci': in_95_ci,
        'in_99_ci': in_99_ci,
        'distance': distance,
        'z_score': z_score,
        'percentile': percentile,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    # Collect all data
    all_deaths, sources = collect_all_h1_deaths()

    if len(all_deaths) == 0:
        print("ERROR: No data found!")
        sys.exit(1)

    # Remove duplicates (approximately, using rounding)
    rounded = np.round(all_deaths, decimals=6)
    unique_deaths = np.array(list(set(rounded)))

    print(f"Total death radii collected: {len(all_deaths)}")
    print(f"Unique death radii (deduplicated): {len(unique_deaths)}")
    print()

    # Use all data (not deduplicated, for statistical validity)
    data = all_deaths

    print("=" * 80)
    print("RAW STATISTICS")
    print("=" * 80)
    print(f"  N samples:  {len(data)}")
    print(f"  Mean:       {np.mean(data):.4f} Å")
    print(f"  Median:     {np.median(data):.4f} Å")
    print(f"  Std:        {np.std(data):.4f} Å")
    print(f"  Min:        {np.min(data):.4f} Å")
    print(f"  Max:        {np.max(data):.4f} Å")
    print()

    # Bootstrap analysis
    print("=" * 80)
    print("BOOTSTRAP ANALYSIS")
    print("=" * 80)

    bootstrap = bootstrap_ci(data, n_bootstrap=10000)

    print()
    print(f"Bootstrap results:")
    print(f"  Mean:     {bootstrap['bootstrap_mean']:.4f} Å")
    print(f"  Std:      {bootstrap['bootstrap_std']:.6f} Å")
    print(f"  95% CI:   [{bootstrap['ci_95_lower']:.4f}, {bootstrap['ci_95_upper']:.4f}] Å")
    print(f"  99% CI:   [{bootstrap['ci_99_lower']:.4f}, {bootstrap['ci_99_upper']:.4f}] Å")
    print()

    # Test hypotheses
    print("=" * 80)
    print("HYPOTHESIS TESTING")
    print("=" * 80)

    hypotheses = [
        (SQRT_Z2, "√(32π/3)"),
        (5.40, "α-helix pitch"),
        (4.70, "β-sheet spacing"),
        (6.0, "Empirical guess 6.0"),
    ]

    results = []
    for value, name in hypotheses:
        result = test_hypothesis(value, name, bootstrap)
        results.append(result)

        status_95 = "✓ IN 95% CI" if result['in_95_ci'] else "✗ OUTSIDE 95% CI"
        print(f"\n{name} = {value:.4f} Å:")
        print(f"  Status:     {status_95}")
        print(f"  Distance:   {result['distance']:.4f} Å")
        print(f"  Z-score:    {result['z_score']:.2f}")
        print(f"  Percentile: {result['percentile']:.1f}%")

    # Final verdict
    sqrt_z2_result = results[0]

    print("\n" + "=" * 80)
    print("=" * 80)
    print("                    FINAL VERDICT")
    print("=" * 80)
    print("=" * 80)

    if sqrt_z2_result['in_95_ci']:
        verdict = "VALIDATED"
        conclusion = "√(32π/3) IS within the 95% CI"
    else:
        verdict = "NOT VALIDATED"
        conclusion = "√(32π/3) is OUTSIDE the 95% CI"

    print(f"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║  √(32π/3) = {SQRT_Z2:.4f} Å                                              ║
    ║                                                                      ║
    ║  Empirical mean:    {bootstrap['bootstrap_mean']:.4f} Å                                  ║
    ║  95% CI:            [{bootstrap['ci_95_lower']:.4f}, {bootstrap['ci_95_upper']:.4f}] Å                        ║
    ║  Z-score:           {sqrt_z2_result['z_score']:.2f}                                         ║
    ║                                                                      ║
    ║  CONCLUSION: {conclusion:<42} ║
    ║                                                                      ║
    ║  N samples:         {len(data):<10}                                  ║
    ║  Data sources:      {len(sources):<10}                                  ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    print(f">>> verdict = '{verdict}'")
    print(f">>> sqrt_z2_in_95_ci = {sqrt_z2_result['in_95_ci']}")
    print()

    # Save results
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'n_samples': len(data),
        'n_sources': len(sources),
        'raw_mean': float(np.mean(data)),
        'raw_std': float(np.std(data)),
        'bootstrap': {
            'mean': bootstrap['bootstrap_mean'],
            'std': bootstrap['bootstrap_std'],
            'ci_95_lower': bootstrap['ci_95_lower'],
            'ci_95_upper': bootstrap['ci_95_upper'],
            'ci_99_lower': bootstrap['ci_99_lower'],
            'ci_99_upper': bootstrap['ci_99_upper'],
        },
        'sqrt_z2': {
            'value': float(SQRT_Z2),
            'in_95_ci': bool(sqrt_z2_result['in_95_ci']),
            'z_score': float(sqrt_z2_result['z_score']),
            'percentile': float(sqrt_z2_result['percentile']),
        },
        'verdict': verdict,
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Results saved: {OUTPUT_FILE}")

    return output_data


if __name__ == "__main__":
    main()
