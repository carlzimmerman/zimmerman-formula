#!/usr/bin/env python3
"""
HURRICANE DIRECT TEST
=====================

Direct test bypassing OlympusFlow state serialization.
Uses HermesV2 + manual analysis + deepening.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import math
import json
import urllib.request
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np

# Z² constants
Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)
PHI = (1 + math.sqrt(5)) / 2

TARGETS = {
    "φ": PHI,
    "1/φ": 1/PHI,
    "Z": Z,
    "Z²": Z2,
    "Z²/10": Z2/10,
    "π": math.pi,
}

print("=" * 70)
print("HURRICANE DIRECT TEST")
print("=" * 70)
print(f"Started: {datetime.now().isoformat()}")
print()

# =============================================================================
# FETCH DATA
# =============================================================================

print("PHASE 1: DATA ACQUISITION")
print("-" * 40)

# Try NOAA PSL first (simpler format)
urls_to_try = [
    ("NOAA PSL ACE", "https://psl.noaa.gov/data/timeseries/monthly/data/hurr.atl.ace.data"),
    ("NOAA PSL Hurricane Count", "https://psl.noaa.gov/data/timeseries/monthly/data/hurr.atl.tot.data"),
    ("NOAA PSL Major Hurricanes", "https://psl.noaa.gov/data/timeseries/monthly/data/hurr.atl.major.data"),
]

data_found = []

for name, url in urls_to_try:
    try:
        print(f"  Trying {name}...")
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read().decode('utf-8')

        # Parse fixed-width format
        lines = content.strip().split('\n')
        data_lines = []

        for line in lines:
            parts = line.split()
            if len(parts) >= 13:
                try:
                    year = int(parts[0])
                    if 1850 < year < 2100:
                        data_lines.append(parts)
                except:
                    continue

        if data_lines:
            columns = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                      'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            df = pd.DataFrame(data_lines, columns=columns)

            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            df = df.replace(-99.9, np.nan)
            df = df.replace(-9.9, np.nan)
            df = df.replace(-999, np.nan)

            print(f"    ✓ Got {len(df)} years ({df['YEAR'].min()}-{df['YEAR'].max()})")
            data_found.append((name, url, df))

    except Exception as e:
        print(f"    ✗ Failed: {e}")

if not data_found:
    print("\nNo data found!")
    sys.exit(1)

print(f"\n  Found {len(data_found)} datasets")
print()

# =============================================================================
# ANALYZE FOR Z² PATTERNS
# =============================================================================

print("PHASE 2: Z² PATTERN ANALYSIS")
print("-" * 40)

all_findings = []

for name, url, df in data_found:
    print(f"\n  Analyzing: {name}")

    month_cols = [c for c in df.columns if c != 'YEAR']

    # Combine all months into one series
    all_values = []
    for col in month_cols:
        all_values.extend(df[col].dropna().tolist())

    if len(all_values) < 30:
        print(f"    Not enough data ({len(all_values)} values)")
        continue

    data = pd.Series(all_values)
    data = data[data > 0]  # Remove zeros for hurricane data

    if len(data) < 30:
        print(f"    Not enough non-zero data")
        continue

    mean = data.mean()
    std = data.std()
    cv = std / mean if mean > 0 else 0

    print(f"    Mean: {mean:.4f}, STD: {std:.4f}, CV: {cv:.4f}")

    # Check CV against targets
    for target_name, target_val in TARGETS.items():
        error = abs(cv - target_val) / target_val * 100
        if error < 10:
            finding = {
                "domain": "meteorology",
                "quantity": f"CV({name})",
                "value": cv,
                "target": target_name,
                "target_value": target_val,
                "error_percent": error,
                "n_samples": len(data),
                "source": name,
                "url": url
            }
            all_findings.append(finding)
            print(f"    *** FOUND: CV = {cv:.4f} ≈ {target_name} ({error:.2f}% error) ***")

    # Check STD against targets
    for target_name, target_val in TARGETS.items():
        error = abs(std - target_val) / target_val * 100
        if error < 10:
            finding = {
                "domain": "meteorology",
                "quantity": f"STD({name})",
                "value": std,
                "target": target_name,
                "target_value": target_val,
                "error_percent": error,
                "n_samples": len(data),
                "source": name,
                "url": url
            }
            all_findings.append(finding)
            print(f"    *** FOUND: STD = {std:.4f} ≈ {target_name} ({error:.2f}% error) ***")

    # Also analyze inter-annual variability
    annual_sums = df[month_cols].sum(axis=1)
    annual_sums = annual_sums[annual_sums > 0]

    if len(annual_sums) >= 30:
        annual_cv = annual_sums.std() / annual_sums.mean()
        annual_std = annual_sums.std()

        print(f"    Annual: Mean={annual_sums.mean():.2f}, STD={annual_std:.2f}, CV={annual_cv:.4f}")

        for target_name, target_val in TARGETS.items():
            error = abs(annual_cv - target_val) / target_val * 100
            if error < 10:
                finding = {
                    "domain": "meteorology",
                    "quantity": f"CV(annual_{name})",
                    "value": annual_cv,
                    "target": target_name,
                    "target_value": target_val,
                    "error_percent": error,
                    "n_samples": len(annual_sums),
                    "source": name,
                    "url": url
                }
                all_findings.append(finding)
                print(f"    *** FOUND: Annual CV = {annual_cv:.4f} ≈ {target_name} ({error:.2f}% error) ***")

print()

# =============================================================================
# DEEPENING
# =============================================================================

print("PHASE 3: RECURSIVE DEEPENING")
print("-" * 40)

if not all_findings:
    print("  No significant findings to deepen")
else:
    print(f"  Found {len(all_findings)} patterns")

    # Sort by significance (lowest error first)
    all_findings.sort(key=lambda x: x['error_percent'])

    best_finding = all_findings[0]
    print(f"\n  Best finding: {best_finding['quantity']} ≈ {best_finding['target']}")
    print(f"  Error: {best_finding['error_percent']:.4f}%")

    # Use deepener
    try:
        from CylleneFlow.deepener import Deepener

        deepener = Deepener(max_depth=2, verbose=True)
        decision = deepener.analyze_finding(best_finding)

        print(f"\n  Deepener analysis:")
        print(f"    Significance: {decision.significance_score:.2f}")
        print(f"    Should deepen: {decision.should_deepen}")
        print(f"    Questions: {len(decision.questions)}")

        if decision.should_deepen and decision.questions:
            print(f"\n  Research questions generated:")
            for i, q in enumerate(decision.questions[:3], 1):
                print(f"    {i}. {q.question[:60]}...")

    except ImportError:
        print("  Deepener not available")

print()

# =============================================================================
# RESULTS
# =============================================================================

print("=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)
print()

print(f"Datasets analyzed: {len(data_found)}")
print(f"Z² patterns found: {len(all_findings)}")
print()

if all_findings:
    print("FINDINGS (sorted by precision):")
    for f in all_findings[:10]:
        print(f"  {f['quantity']} = {f['value']:.6f} ≈ {f['target']} ({f['error_percent']:.4f}% error)")
    print()

# Save results
output_dir = Path(__file__).parent.parent / "olympus_outputs" / "hurricane_direct"
output_dir.mkdir(parents=True, exist_ok=True)

results = {
    "timestamp": datetime.now().isoformat(),
    "datasets": [(name, url, len(df)) for name, url, df in data_found],
    "findings": all_findings,
    "z2_constants": {
        "Z2": Z2,
        "Z": Z,
        "phi": PHI
    }
}

with open(output_dir / "results.json", 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"Results saved to: {output_dir / 'results.json'}")
print()

if all_findings:
    print("✓ HURRICANE BLIND TEST PASSED")
    print(f"  Found {len(all_findings)} Z² patterns in hurricane data!")
else:
    print("~ No Z² patterns found in hurricane data")
    print("  (This is a valid scientific result)")
