#!/usr/bin/env python3
"""
GLACIER ITERATION EXPERIMENT
============================

Test CylleneFlow's iterative learning on glacier mass balance data.

Expected data sources:
- WGMS (World Glacier Monitoring Service)
- GLAMOS (Glacier Monitoring in Switzerland)
- NSIDC (National Snow and Ice Data Center)

This tests the Z² prediction that glacier mass balance relates to 1/φ.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
from pathlib import Path

# Add CylleneFlow to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from iteration_runner import IterationRunner


def run_glacier_experiment(model: str = None, iterations: int = 3):
    """Run glacier iteration experiment.

    Args:
        model: Legomena model to use (e.g., 'legomena-31b', 'legomena-27b')
        iterations: Number of iterations to run
    """

    # Set model if specified
    if model:
        os.environ["LEGOMENA_MODEL"] = model

    current_model = os.environ.get("LEGOMENA_MODEL", "legomena-31b")

    print("=" * 70)
    print(f"CYLLENEFLOW GLACIER EXPERIMENT")
    print(f"Model: {current_model}")
    print(f"Iterations: {iterations}")
    print("=" * 70)

    runner = IterationRunner(
        domain="glaciology",
        topic="Swiss glacier mass balance measurements",
        max_iterations=iterations,
        experiment_name=f"glacier_{current_model.replace('-', '_')}"
    )

    results = runner.run()

    # Summary
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    total_findings = sum(r.get('total_findings', 0) for r in results)
    total_validated = sum(r.get('validated_findings', 0) for r in results)
    total_truths = sum(r.get('new_truths', 0) for r in results)

    print(f"Model: {current_model}")
    print(f"Total iterations: {len(results)}")
    print(f"Total validated findings: {total_validated}")
    print(f"Total new truths: {total_truths}")

    for r in results:
        print(f"  Iter {r['iteration']}: {r.get('new_truths', 0)} truths, "
              f"{r.get('validated_findings', 0)} validated, {r.get('time_seconds', 0):.0f}s")

    return results


def compare_models():
    """Compare legomena-27b vs legomena-31b on glacier data."""

    print("\n" + "=" * 70)
    print("MODEL COMPARISON: legomena-27b vs legomena-31b")
    print("=" * 70 + "\n")

    # Test with legomena-27b
    print("--- Testing legomena-27b ---")
    results_27b = run_glacier_experiment(model="legomena-27b", iterations=3)

    print("\n" + "-" * 70 + "\n")

    # Test with legomena-31b
    print("--- Testing legomena-31b ---")
    results_31b = run_glacier_experiment(model="legomena-31b", iterations=3)

    # Comparison
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)

    truths_27b = sum(r.get('new_truths', 0) for r in results_27b)
    truths_31b = sum(r.get('new_truths', 0) for r in results_31b)

    print(f"legomena-27b: {truths_27b} truths discovered")
    print(f"legomena-31b: {truths_31b} truths discovered")

    if truths_27b > truths_31b:
        print("WINNER: legomena-27b (smaller, efficient)")
    elif truths_31b > truths_27b:
        print("WINNER: legomena-31b (larger, more capable)")
    else:
        print("TIE: Both models found same number of truths")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run glacier CylleneFlow experiment")
    parser.add_argument("--model", default="legomena-31b", help="Legomena model to use")
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations")
    parser.add_argument("--compare", action="store_true", help="Compare 27b vs 31b models")

    args = parser.parse_args()

    if args.compare:
        compare_models()
    else:
        run_glacier_experiment(model=args.model, iterations=args.iterations)
