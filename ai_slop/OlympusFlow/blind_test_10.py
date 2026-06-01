#!/usr/bin/env python3
"""
BLIND TEST: First 10 Derivations
=================================

This script runs 10 derivation tasks through OlympusFlow BLINDLY.
NO access to ground_truth_oracle during derivation.

The results are saved to /tmp/blind_test_results.json for
post-hoc validation against the oracle.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from OlympusFlow.derivation_engine import DerivationEngine
from OlympusFlow.derivation_contracts import DerivationLevel, ChainStatus

# =============================================================================
# TEST CASES (10 blind questions)
# =============================================================================

TEST_CASES = [
    {
        "name": "Monoatomic Heat Capacity Ratio (γ)",
        "target_value": 5/3,  # 1.6666...
        "domain": "thermodynamics",
        "description": "Ratio of specific heats for monoatomic ideal gas"
    },
    {
        "name": "Tetrahedral Bond Angle",
        "target_value": 109.4712,  # degrees, arccos(-1/3)
        "domain": "geometry",
        "description": "Angle between bonds in tetrahedral molecules like CH4"
    },
    {
        "name": "Dark Energy Density (Ω_Λ)",
        "target_value": 0.685,
        "domain": "cosmology",
        "description": "Fraction of universe that is dark energy"
    },
    {
        "name": "Weak Mixing Angle (sin²θ_W)",
        "target_value": 0.23122,
        "domain": "particle_physics",
        "description": "Electroweak mixing parameter"
    },
    {
        "name": "Murray's Law Exponent",
        "target_value": 3.0,
        "domain": "biophysics",
        "description": "Exponent in blood vessel branching optimization"
    },
    {
        "name": "von Kármán Constant",
        "target_value": 0.41,
        "domain": "fluid_dynamics",
        "description": "Turbulent boundary layer constant (empirical)"
    },
    {
        "name": "Strouhal Number (vortex shedding)",
        "target_value": 0.2,
        "domain": "fluid_dynamics",
        "description": "Dimensionless frequency of vortex shedding"
    },
    {
        "name": "Feigenbaum Constant (δ)",
        "target_value": 4.6692,
        "domain": "mathematics",
        "description": "Universal constant in chaos theory"
    },
    {
        "name": "Golden Ratio (φ)",
        "target_value": 1.6180339887,
        "domain": "mathematics",
        "description": "Fundamental geometric ratio (1+√5)/2"
    },
    {
        "name": "Fine Structure Constant Inverse (α⁻¹)",
        "target_value": 137.035999,
        "domain": "particle_physics",
        "description": "Electromagnetic coupling strength"
    }
]

# =============================================================================
# BLIND TEST RUNNER
# =============================================================================

def run_blind_test(verbose: bool = True):
    """
    Run all 10 derivations blindly through OlympusFlow.

    Returns results dict for post-hoc validation.
    """
    print("=" * 70)
    print("BLIND DERIVATION TEST - 10 Questions")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")
    print(f"NO oracle access - pure methodology")
    print("=" * 70)
    print()

    # Initialize engine
    engine = DerivationEngine(verbose=verbose)

    if not engine.legomena_available:
        print("⚠️  WARNING: Legomena not available!")
        print("   Results will be pattern-matching only.")
        print()

    results = {
        "test_name": "Blind Test - First 10",
        "started": datetime.now().isoformat(),
        "legomena_available": engine.legomena_available,
        "derivations": []
    }

    total_start = time.time()

    for i, test in enumerate(TEST_CASES):
        print(f"\n{'='*70}")
        print(f"TEST {i+1}/10: {test['name']}")
        print(f"{'='*70}")

        start = time.time()

        try:
            # Run derivation BLINDLY
            chain = engine.derive(
                constant_name=test['name'],
                target_value=test['target_value']
            )

            # Verify (without experimental lookup for speed)
            verified = engine.verify(
                chain,
                experimental_value=test['target_value'],
                experimental_source="Test input"
            )

            elapsed = time.time() - start

            # Collect results
            result = {
                "name": test['name'],
                "target_value": test['target_value'],
                "domain": test['domain'],
                "description": test['description'],

                # Engine outputs (what we're testing)
                "computed_value": chain.computed_value,
                "percent_error": chain.percent_error,
                "final_formula": chain.final_formula,
                "physical_mechanism": chain.physical_mechanism,

                # Classification
                "derivation_level": chain.level.value,
                "chain_status": chain.status.value,
                "overall_confidence": chain.overall_confidence,

                # Flags
                "starts_from_z2": chain.starts_from_z2,
                "has_physical_step": chain.has_physical_step,
                "is_first_principles": chain.is_first_principles(),
                "qualifies_for_aletheia": chain.qualifies_for_aletheia(),

                # HRM
                "hrm_score": verified.hrm_score,
                "destination": verified.destination.value,

                # Multi-prompt refinement
                "refinement_metadata": chain.refinement_metadata,

                # Timing
                "elapsed_seconds": elapsed
            }

            results["derivations"].append(result)

            # Summary print
            print(f"\n{'─'*50}")
            print(f"RESULT: {test['name']}")
            print(f"{'─'*50}")
            print(f"  Formula: {chain.final_formula}")
            print(f"  Computed: {chain.computed_value:.10f}")
            print(f"  Error: {chain.percent_error:.4f}%")
            print(f"  Level: {chain.level.value.upper()}")
            print(f"  Confidence: {chain.overall_confidence:.2f}")
            print(f"  HRM Score: {verified.hrm_score:.2f}")
            print(f"  Destination: {verified.destination.value}")

            if chain.refinement_metadata:
                print(f"  Multi-prompt attempts: {chain.refinement_metadata.get('attempts', 1)}")
                if chain.refinement_metadata.get('final_verdict'):
                    print(f"  Final verdict: {chain.refinement_metadata['final_verdict']}")

            print(f"  Time: {elapsed:.1f}s")

        except Exception as e:
            print(f"ERROR: {e}")
            results["derivations"].append({
                "name": test['name'],
                "target_value": test['target_value'],
                "error": str(e)
            })

    # Summary
    total_elapsed = time.time() - total_start
    results["completed"] = datetime.now().isoformat()
    results["total_seconds"] = total_elapsed

    # Count results
    first_principles = sum(1 for d in results["derivations"]
                          if d.get("derivation_level") == "first_principles")
    derived = sum(1 for d in results["derivations"]
                  if d.get("derivation_level") == "derived")
    numerical = sum(1 for d in results["derivations"]
                    if d.get("derivation_level") == "numerical_match")
    failed = sum(1 for d in results["derivations"]
                 if d.get("derivation_level") == "failed" or d.get("error"))

    results["summary"] = {
        "first_principles": first_principles,
        "derived": derived,
        "numerical_match": numerical,
        "failed": failed,
        "total": len(TEST_CASES)
    }

    print("\n" + "=" * 70)
    print("BLIND TEST COMPLETE")
    print("=" * 70)
    print(f"Total time: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    print(f"\nResults:")
    print(f"  First Principles: {first_principles}/10")
    print(f"  Derived (math only): {derived}/10")
    print(f"  Numerical Match: {numerical}/10")
    print(f"  Failed: {failed}/10")
    print("=" * 70)

    # Save results
    output_path = Path("/tmp/blind_test_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")
    print("Run validation script to compare against oracle.")

    return results


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Check for verbose flag
    verbose = "--quiet" not in sys.argv

    results = run_blind_test(verbose=verbose)
