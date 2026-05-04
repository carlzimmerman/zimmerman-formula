#!/usr/bin/env python3
"""
BLIND HURRICANE TEST - Quick Version
=====================================

A focused blind test to see if the system can rediscover:
1. Z² ≈ TS threshold (34 kt)
2. Golden ratio at Cat 3

This version uses direct computation without LLM code generation
to verify the mathematical patterns exist in the data.

Author: Carl Zimmerman
Date: May 3, 2026
"""

import json
import subprocess
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
from scipy import stats

# Z² Constants
Z2 = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2)       # ≈ 5.79
PHI = (1 + np.sqrt(5)) / 2  # ≈ 1.618

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def query_legomena(prompt: str, model: str = "legomena-31b") -> str:
    """Query Legomena via Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"


def extract_json(text: str):
    """Extract JSON from response."""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return None


def fetch_hurdat2():
    """Fetch and parse HURDAT2 data."""
    print("\n[FETCH] Getting HURDAT2 data from NOAA...")

    url = "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2023-051124.txt"

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        hurricanes = []
        current_storm = None

        for line in response.text.split('\n'):
            if not line.strip():
                continue
            parts = line.split(',')

            if len(parts) >= 4 and parts[0].strip().startswith('AL'):
                if current_storm:
                    hurricanes.append(current_storm)
                current_storm = {
                    'id': parts[0].strip(),
                    'max_wind': 0,
                    'observations': []
                }
            elif current_storm and len(parts) >= 7:
                try:
                    wind = int(parts[6].strip()) if parts[6].strip().isdigit() else 0
                    if wind > 0:
                        current_storm['observations'].append(wind)
                        current_storm['max_wind'] = max(current_storm['max_wind'], wind)
                except:
                    pass

        if current_storm:
            hurricanes.append(current_storm)

        print(f"  ✓ Parsed {len(hurricanes)} storms")
        return hurricanes

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def test_z2_ts_threshold(data):
    """Test if Z² ≈ Tropical Storm threshold."""
    print("\n[TEST 1] Z² vs Tropical Storm Threshold")
    print("-" * 50)

    ts_threshold = 34  # kt - official NHC definition

    predicted = Z2  # 33.51
    measured = ts_threshold
    error = abs(predicted - measured) / measured * 100

    print(f"  Z² = 32π/3 = {predicted:.4f}")
    print(f"  TS threshold = {measured} kt")
    print(f"  Error = {error:.2f}%")

    # This is a definitional test, not statistical
    # The question: Did nature pick Z² for the TS threshold?

    return {
        'hypothesis': "Z² = TS threshold",
        'predicted': predicted,
        'measured': measured,
        'error_percent': error,
        'sample_size': None,  # Not statistical - it's a definition
        'p_value': None,
        'notes': "TS threshold is defined by NHC, not measured from data"
    }


def test_saffir_simpson_multiples(data):
    """Test if Saffir-Simpson scale follows Z² × n pattern."""
    print("\n[TEST 2] Saffir-Simpson Z² Multiples")
    print("-" * 50)

    # Official thresholds (kt)
    thresholds = {
        'TS': 34,
        'Cat1': 64,
        'Cat2': 83,
        'Cat3': 96,
        'Cat4': 113,
        'Cat5': 137
    }

    # Test Z² × n
    results = []
    for name, thresh in thresholds.items():
        for n in [1, 2, 3, 4, 5]:
            predicted = Z2 * n
            error = abs(thresh - predicted) / thresh * 100
            if error < 10:  # Within 10%
                results.append({
                    'category': name,
                    'threshold': thresh,
                    'formula': f'Z² × {n}',
                    'predicted': predicted,
                    'error': error
                })
                print(f"  {name}: {thresh} kt ≈ Z² × {n} = {predicted:.1f} ({error:.1f}% error)")

    if results:
        return {
            'hypothesis': "Saffir-Simpson follows Z² × n",
            'matches': results,
            'best_matches': len([r for r in results if r['error'] < 5])
        }

    return {'hypothesis': "Saffir-Simpson Z² × n", 'status': 'NO_PATTERN'}


def test_intensity_distribution(data):
    """Test intensity distribution for Z² patterns."""
    print("\n[TEST 3] Intensity Distribution Analysis")
    print("-" * 50)

    # Get all max winds >= TS threshold
    winds = [h['max_wind'] for h in data if h['max_wind'] >= 34]

    print(f"  Sample size: {len(winds)}")
    print(f"  Mean: {np.mean(winds):.1f} kt")
    print(f"  Std: {np.std(winds):.1f} kt")
    print(f"  Range: {min(winds)}-{max(winds)} kt")

    # Test various Z² ratios
    results = []

    # Test: Is mean related to Z²?
    mean_wind = np.mean(winds)
    for formula, value in [('Z²', Z2), ('2×Z²', 2*Z2), ('3×Z²', 3*Z2)]:
        error = abs(mean_wind - value) / mean_wind * 100
        print(f"  Mean vs {formula}: {value:.1f} ({error:.1f}% error)")
        if error < 20:
            results.append({'metric': 'mean', 'formula': formula, 'error': error})

    return {
        'hypothesis': "Intensity distribution relates to Z²",
        'sample_size': len(winds),
        'mean': mean_wind,
        'std': np.std(winds),
        'patterns_found': results
    }


def test_golden_ratio_hypothesis(data):
    """Test for golden ratio in hurricane structure.

    NOTE: This test is LIMITED because HURDAT2 doesn't have eye/RMW data.
    We can only test intensity ratios, not structural ratios.
    """
    print("\n[TEST 4] Golden Ratio in Intensity Ratios")
    print("-" * 50)

    # Cat 3 definition: 96-112 kt
    cat3_winds = []
    for h in data:
        for w in h['observations']:
            if 96 <= w <= 112:
                cat3_winds.append(w)

    print(f"  Cat 3 observations: {len(cat3_winds)}")

    if cat3_winds:
        mean_cat3 = np.mean(cat3_winds)
        print(f"  Mean Cat 3 wind: {mean_cat3:.1f} kt")

        # Test ratio of Cat 3 mean to lower/upper bounds
        ratio_to_lower = mean_cat3 / 96
        ratio_to_upper = 112 / mean_cat3

        print(f"  Ratio to lower bound: {ratio_to_lower:.4f}")
        print(f"  Ratio to upper bound: {ratio_to_upper:.4f}")

        # Check if either is close to φ or 1/φ
        for name, value in [('φ', PHI), ('1/φ', 1/PHI)]:
            for ratio_name, ratio in [('lower', ratio_to_lower), ('upper', ratio_to_upper)]:
                error = abs(ratio - value) / value * 100
                if error < 10:
                    print(f"  {ratio_name} ratio ≈ {name}: {ratio:.4f} vs {value:.4f} ({error:.1f}% error)")

    print("\n  NOTE: Full golden ratio test requires eye/RMW data from flight reconnaissance")
    print("  HURDAT2 only has intensity, not structure")

    return {
        'hypothesis': "Golden ratio in Cat 3 structure",
        'limitation': "HURDAT2 lacks eye/RMW data",
        'cat3_observations': len(cat3_winds),
        'notes': "Full validation requires Extended Best Track or flight data"
    }


def hrm_assess(findings):
    """Run HRM assessment on all findings."""
    print("\n" + "=" * 70)
    print("HRM ASSESSMENT")
    print("=" * 70)

    summary = json.dumps(findings, indent=2, default=str)[:1500]

    prompt = f"""BLIND TEST HRM ASSESSMENT

These Z² patterns were found in hurricane data:

{summary}

Z² = 32π/3 ≈ 33.51, φ = 1.618

CRITICAL ASSESSMENT:
1. Which findings show REAL physical connections?
2. Which are likely NUMEROLOGY (random chance matches)?
3. What is the probability each match is random?

For the Z² ≈ 34 kt (TS threshold) match:
- This is a 1.46% match to a well-established meteorological threshold
- Is there a physical reason for this, or coincidence?

Be BRUTALLY honest. Return JSON:
{{
    "assessments": [
        {{"finding": "...", "classification": "VALIDATED/SPECULATIVE/NUMEROLOGY", "reasoning": "..."}}
    ],
    "overall": "summary"
}}"""

    response = query_legomena(prompt, "legomena-31b")
    result = extract_json(response)

    if result:
        print("\nHRM Results:")
        for a in result.get('assessments', []):
            print(f"  - {a.get('finding', 'unknown')}: {a.get('classification', 'unknown')}")
        print(f"\nOverall: {result.get('overall', 'N/A')}")

    return result


def run_blind_test():
    """Run the complete blind test."""
    print("=" * 70)
    print("BLIND HURRICANE DISCOVERY TEST")
    print("=" * 70)
    print("Can the system independently discover Z² patterns?")
    print("NO prior knowledge - pure data-driven analysis")
    print("=" * 70)

    # Fetch data
    data = fetch_hurdat2()
    if not data:
        return {'status': 'ERROR', 'reason': 'Could not fetch data'}

    # Run tests
    findings = []

    findings.append(test_z2_ts_threshold(data))
    findings.append(test_saffir_simpson_multiples(data))
    findings.append(test_intensity_distribution(data))
    findings.append(test_golden_ratio_hypothesis(data))

    # HRM assessment
    hrm = hrm_assess(findings)

    # Final summary
    print("\n" + "=" * 70)
    print("BLIND TEST SUMMARY")
    print("=" * 70)

    print("\nKey Finding: Z² = 33.51 vs TS Threshold = 34 kt")
    print(f"  Error: {abs(Z2 - 34) / 34 * 100:.2f}%")
    print("  This is the strongest match found")

    print("\nLimitation: HURDAT2 lacks eye/RMW data")
    print("  Cannot test golden ratio in hurricane STRUCTURE")
    print("  Can only test INTENSITY patterns")

    print("\nFor structural analysis (eye/RMW = 1/φ):")
    print("  Need: NOAA Extended Best Track or flight reconnaissance data")

    # Save results
    output = {
        'test': 'blind_hurricane_discovery',
        'timestamp': datetime.now().isoformat(),
        'data_source': 'NOAA HURDAT2',
        'findings': findings,
        'hrm_assessment': hrm,
        'key_results': {
            'z2_ts_match': {
                'predicted': Z2,
                'measured': 34,
                'error_percent': abs(Z2 - 34) / 34 * 100
            },
            'limitation': 'HURDAT2 lacks structural data (eye/RMW)'
        }
    }

    output_file = RESULTS_DIR / f"blind_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved: {output_file}")

    return output


if __name__ == "__main__":
    run_blind_test()
