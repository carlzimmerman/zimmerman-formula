#!/usr/bin/env python3
"""
EL NINO ITERATION EXPERIMENT
=============================

Test CylleneFlow's iterative learning on El Nino climate data.
This should work better than Venice because NOAA has excellent public data.

Expected data sources:
- NOAA Climate Prediction Center (SOI, ONI indices)
- NOAA ESRL (SST anomalies)
- NCEI (historical records)

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
from pathlib import Path

# Add CylleneFlow to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from iteration_runner import IterationRunner


def run_elnino_experiment():
    """Run El Nino iteration experiment."""

    print("=" * 70)
    print("CYLLENEFLOW EL NINO EXPERIMENT")
    print("10 iterations on El Nino climate indices")
    print("=" * 70)

    runner = IterationRunner(
        domain="climatology",
        topic="El Nino Southern Oscillation SST anomalies and SOI index",
        max_iterations=10,
        experiment_name="elnino_10iter"
    )

    results = runner.run()

    # Summary
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    total_findings = sum(r['total_findings'] for r in results)
    total_validated = sum(r['validated_findings'] for r in results)
    total_truths = sum(r['new_truths'] for r in results)

    print(f"Total iterations: {len(results)}")
    print(f"Total validated findings: {total_validated}")
    print(f"Total new truths: {total_truths}")

    for r in results:
        print(f"  Iter {r['iteration']}: {r['new_truths']} truths, "
              f"{r['validated_findings']} validated, {r['time_seconds']:.0f}s")

    return results


if __name__ == "__main__":
    run_elnino_experiment()
