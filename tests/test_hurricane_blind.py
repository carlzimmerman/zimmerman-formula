#!/usr/bin/env python3
"""
HURRICANE BLIND TEST - True Blind Discovery
============================================

Tests whether OlympusFlow can discover Z² patterns in Atlantic hurricane data
WITHOUT any pre-loaded hurricane information in AletheiaLake.

The Z² framework predicts certain patterns in cyclonic systems based on
the geometric constants. This test verifies if those patterns can be
discovered autonomously from NOAA hurricane data.

Expected data sources:
- NOAA National Hurricane Center
- HURDAT2 (Atlantic hurricane database)
- ACE (Accumulated Cyclone Energy) indices

Author: Carl Zimmerman
Date: May 5, 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from datetime import datetime

# Verify hurricane is NOT in AletheiaLake (blind test requirement)
from AletheiaLake import AletheiaLake

def verify_blind_test():
    """Ensure no hurricane-related truths exist."""
    import re
    lake = AletheiaLake()
    all_truths = lake.get_all_truths()

    # Use word boundaries to avoid false positives like "cube_faces" matching "ace"
    hurricane_keywords = ['hurricane', 'cyclone', 'storm', 'saffir', 'typhoon']
    # Note: Removed 'ace', 'wind' as they cause false positives

    for truth in all_truths:
        truth_text = f"{truth.name} {truth.claim} {truth.domain}".lower()
        for kw in hurricane_keywords:
            # Use word boundary regex to avoid partial matches
            if re.search(rf'\b{kw}\b', truth_text):
                print(f"ERROR: Found hurricane-related truth: {truth.name}")
                print("This is NOT a blind test!")
                return False

    return True


def run_hurricane_blind_test():
    """Run the full CylleneFlow pipeline on hurricane data."""

    print("=" * 70)
    print("ATLANTIC HURRICANE - TRUE BLIND DISCOVERY TEST")
    print("=" * 70)
    print()

    # Verify blind test conditions
    is_blind = verify_blind_test()
    print(f"Hurricane in AletheiaLake: {not is_blind}")
    if is_blind:
        print("  ✓ Hurricane data is NOT pre-loaded - this is a TRUE blind test")
    else:
        print("  ✗ Hurricane data found in AletheiaLake - NOT a blind test!")
        return
    print()

    # Z² framework values for reference (NOT used in discovery)
    Z2_SQUARED = 32 * math.pi / 3
    Z = math.sqrt(Z2_SQUARED)

    print(f"Z² Framework Reference (for analysis only):")
    print(f"  Z² = 32π/3 = {Z2_SQUARED:.6f}")
    print(f"  Z = {Z:.6f}")
    print()

    # Import CylleneFlow
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'CylleneFlow'))
        from experiment_runner import run_experiment
    except ImportError:
        print("ERROR: Could not import CylleneFlow experiment_runner")
        print("Running HermesFlow directly instead...")

        # Fallback to direct HermesFlow
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'HermesFlow'))
        from hermes_explorer import HermesExplorer

        explorer = HermesExplorer(verbose=True)

        result = explorer.explore_for_data(
            topic="Atlantic hurricane intensity measurements ACE accumulated cyclone energy NOAA",
            domain="meteorology",
            quantities=["value", "measurement", "intensity", "wind_speed", "pressure"]
        )

        print()
        print("=" * 70)
        print("DISCOVERY RESULTS")
        print("=" * 70)
        print(f"Success: {result.success}")
        print(f"URL: {result.url}")
        if result.data is not None:
            print(f"Data shape: {result.data.shape}")
            print(f"Columns: {list(result.data.columns)}")
        print(f"Steps: {len(result.steps)}")
        return result

    # Run through CylleneFlow
    print("Running CylleneFlow experiment...")
    print("-" * 70)

    results = run_experiment(
        topic="Atlantic hurricane intensity measurements ACE accumulated cyclone energy",
        domain="meteorology",
        max_iterations=3,
        experiment_name=f"hurricane_blind_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    print()
    print("=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)

    return results


if __name__ == "__main__":
    run_hurricane_blind_test()
