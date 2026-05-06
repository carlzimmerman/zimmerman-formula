#!/usr/bin/env python3
"""
FULL PIPELINE BLIND TEST - 10 Derivations
==========================================

This runs the COMPLETE OlympusFlow pipeline for 10 derivation tasks:
- AlpheusFlow queue management
- OlympusFlow 6-stage pipeline
- HermesFlow discovery (if needed)
- MetisFlow research
- Multi-prompt Legomena refinement
- Full HRM verification
- AletheiaLake/MnemosyneLake storage

NO TIMEOUTS - let each call complete fully.
Estimated time: 3-5 hours for 10 tasks.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# =============================================================================
# INCREASE ALL TIMEOUTS - NO RUSHING
# =============================================================================
os.environ["LEGOMENA_TIMEOUT"] = "600"  # 10 minutes per call
os.environ["DERIVATION_ATTEMPTS"] = "4"  # Full 4-attempt multi-prompt

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from OlympusFlow.derivation_engine import DerivationEngine, MULTI_PROMPT_ATTEMPTS
from OlympusFlow.derivation_contracts import DerivationLevel, ChainStatus

# =============================================================================
# TEST CASES - 10 BLIND QUESTIONS
# =============================================================================

TEST_CASES = [
    {
        "name": "Monoatomic Heat Capacity Ratio",
        "symbol": "γ",
        "target_value": 5/3,
        "domain": "thermodynamics",
        "description": "Ratio of specific heats Cp/Cv for monoatomic ideal gas"
    },
    {
        "name": "Tetrahedral Bond Angle",
        "symbol": "θ_tet",
        "target_value": 109.4712,
        "domain": "geometry",
        "description": "Angle between bonds in tetrahedral molecules (CH4, etc)"
    },
    {
        "name": "Dark Energy Density Fraction",
        "symbol": "Ω_Λ",
        "target_value": 0.685,
        "domain": "cosmology",
        "description": "Fraction of universe energy density that is dark energy"
    },
    {
        "name": "Weak Mixing Angle",
        "symbol": "sin²θ_W",
        "target_value": 0.23122,
        "domain": "particle_physics",
        "description": "Electroweak mixing parameter (Weinberg angle)"
    },
    {
        "name": "Murray Law Blood Vessel Exponent",
        "symbol": "n_Murray",
        "target_value": 3.0,
        "domain": "biophysics",
        "description": "Exponent in optimal blood vessel branching (r³ law)"
    },
    {
        "name": "von Karman Turbulence Constant",
        "symbol": "κ",
        "target_value": 0.41,
        "domain": "fluid_dynamics",
        "description": "Universal constant in turbulent boundary layer (empirical)"
    },
    {
        "name": "Strouhal Vortex Shedding Number",
        "symbol": "St",
        "target_value": 0.2,
        "domain": "fluid_dynamics",
        "description": "Dimensionless frequency of vortex shedding from cylinders"
    },
    {
        "name": "Feigenbaum Period Doubling Constant",
        "symbol": "δ",
        "target_value": 4.6692,
        "domain": "mathematics",
        "description": "Universal constant in chaos theory period-doubling cascade"
    },
    {
        "name": "Golden Ratio",
        "symbol": "φ",
        "target_value": 1.6180339887,
        "domain": "mathematics",
        "description": "Fundamental geometric ratio (1+√5)/2"
    },
    {
        "name": "Fine Structure Constant Inverse",
        "symbol": "α⁻¹",
        "target_value": 137.035999,
        "domain": "particle_physics",
        "description": "Electromagnetic coupling strength (~1/137)"
    }
]

# =============================================================================
# FULL PIPELINE RUNNER
# =============================================================================

class FullPipelineRunner:
    """
    Runs complete pipeline with all components and NO timeouts.
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("/tmp/blind_test_full")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize derivation engine with verbose logging
        self.engine = DerivationEngine(verbose=True)

        # Track all results
        self.results = {
            "test_name": "Full Pipeline Blind Test - 10 Questions",
            "started": datetime.now().isoformat(),
            "config": {
                "legomena_timeout": os.environ.get("LEGOMENA_TIMEOUT", "600"),
                "derivation_attempts": os.environ.get("DERIVATION_ATTEMPTS", "4"),
                "legomena_model": os.environ.get("LEGOMENA_MODEL", "legomena-moe"),
                "legomena_available": self.engine.legomena_available
            },
            "derivations": [],
            "llm_call_log": []
        }

        self.total_llm_calls = 0
        self.total_llm_time = 0

    def log(self, msg: str):
        """Log with timestamp."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        # Also write to log file
        with open(self.output_dir / "run.log", "a") as f:
            f.write(f"[{ts}] {msg}\n")

    def run_single_derivation(self, test_case: Dict, index: int) -> Dict:
        """
        Run complete derivation for a single test case.

        This goes through:
        1. Initial derivation prompt
        2. Multi-prompt refinement (4 attempts)
        3. Verification
        4. HRM assessment
        """
        name = test_case["name"]
        target = test_case["target_value"]
        symbol = test_case["symbol"]

        self.log(f"\n{'='*70}")
        self.log(f"TASK {index}/10: {name} ({symbol} = {target})")
        self.log(f"Domain: {test_case['domain']}")
        self.log(f"{'='*70}")

        task_start = time.time()
        llm_calls_before = self.total_llm_calls

        try:
            # ================================================================
            # PHASE 1: DERIVATION (with multi-prompt refinement)
            # ================================================================
            self.log("Phase 1: Running derivation with multi-prompt refinement...")

            chain = self.engine.derive(
                constant_name=f"{name} ({symbol})",
                target_value=target
            )

            derivation_time = time.time() - task_start
            self.log(f"  Derivation completed in {derivation_time:.1f}s")

            # Count LLM calls from refinement metadata
            refinement = chain.refinement_metadata
            if refinement:
                attempts = refinement.get('attempts', 1)
                self.log(f"  Multi-prompt attempts: {attempts}")
                self.total_llm_calls += attempts + 1  # +1 for initial
            else:
                self.total_llm_calls += 1

            # ================================================================
            # PHASE 2: VERIFICATION
            # ================================================================
            self.log("Phase 2: Running verification...")

            verify_start = time.time()
            verified = self.engine.verify(
                chain,
                experimental_value=target,
                experimental_source="Known experimental value"
            )
            verify_time = time.time() - verify_start
            self.log(f"  Verification completed in {verify_time:.1f}s")
            self.total_llm_calls += 1  # Experimental lookup

            # ================================================================
            # COLLECT RESULTS
            # ================================================================
            total_time = time.time() - task_start
            llm_calls_this_task = self.total_llm_calls - llm_calls_before

            result = {
                "index": index,
                "name": name,
                "symbol": symbol,
                "target_value": target,
                "domain": test_case["domain"],
                "description": test_case["description"],

                # Derivation results
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
                "hrm_honesty": verified.hrm_honesty,
                "hrm_rigor": verified.hrm_rigor,
                "hrm_mechanism": verified.hrm_mechanism,
                "hrm_score": verified.hrm_score,
                "destination": verified.destination.value,

                # Multi-prompt refinement details
                "refinement_metadata": chain.refinement_metadata,

                # Timing
                "derivation_time_seconds": derivation_time,
                "verification_time_seconds": verify_time,
                "total_time_seconds": total_time,
                "llm_calls": llm_calls_this_task
            }

            # Log summary
            self.log(f"\n{'─'*50}")
            self.log(f"RESULT: {name}")
            self.log(f"{'─'*50}")
            self.log(f"  Formula: {chain.final_formula}")
            self.log(f"  Computed: {chain.computed_value:.10f}")
            self.log(f"  Target:   {target}")
            self.log(f"  Error: {chain.percent_error:.4f}%")
            self.log(f"  Level: {chain.level.value.upper()}")
            self.log(f"  Confidence: {chain.overall_confidence:.2f}")
            self.log(f"  HRM Score: {verified.hrm_score:.2f}")
            self.log(f"  Destination: {verified.destination.value}")

            if chain.refinement_metadata:
                verdict = chain.refinement_metadata.get('final_verdict', 'N/A')
                self.log(f"  Final Verdict: {verdict}")
                if chain.refinement_metadata.get('honest_assessment'):
                    self.log(f"  Assessment: {chain.refinement_metadata['honest_assessment'][:80]}...")

            self.log(f"  LLM Calls: {llm_calls_this_task}")
            self.log(f"  Time: {total_time:.1f}s ({total_time/60:.1f} min)")

            return result

        except Exception as e:
            self.log(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {
                "index": index,
                "name": name,
                "symbol": symbol,
                "target_value": target,
                "error": str(e),
                "total_time_seconds": time.time() - task_start
            }

    def run_all(self) -> Dict:
        """Run all 10 test cases."""
        self.log("=" * 70)
        self.log("FULL PIPELINE BLIND TEST - 10 DERIVATIONS")
        self.log("=" * 70)
        self.log(f"Started: {self.results['started']}")
        self.log(f"Output directory: {self.output_dir}")
        self.log(f"Legomena available: {self.engine.legomena_available}")
        self.log(f"Legomena model: {os.environ.get('LEGOMENA_MODEL', 'legomena-moe')}")
        self.log(f"Timeout per call: {os.environ.get('LEGOMENA_TIMEOUT', '600')}s")
        self.log(f"Multi-prompt attempts: {os.environ.get('DERIVATION_ATTEMPTS', '4')}")
        self.log("=" * 70)
        self.log("")

        total_start = time.time()

        for i, test_case in enumerate(TEST_CASES, 1):
            result = self.run_single_derivation(test_case, i)
            self.results["derivations"].append(result)

            # Save intermediate results after each task
            self._save_results()

            # Progress update
            elapsed = time.time() - total_start
            remaining = len(TEST_CASES) - i
            if i > 0:
                avg_per_task = elapsed / i
                eta = avg_per_task * remaining
                self.log(f"\nProgress: {i}/{len(TEST_CASES)} complete")
                self.log(f"Elapsed: {elapsed/60:.1f} min")
                self.log(f"ETA: {eta/60:.1f} min ({eta/3600:.1f} hours)")
                self.log(f"Total LLM calls so far: {self.total_llm_calls}")

        # Final summary
        total_time = time.time() - total_start
        self.results["completed"] = datetime.now().isoformat()
        self.results["total_seconds"] = total_time
        self.results["total_llm_calls"] = self.total_llm_calls

        # Compute summary stats
        derivations = self.results["derivations"]
        first_principles = sum(1 for d in derivations
                              if d.get("derivation_level") == "first_principles")
        derived = sum(1 for d in derivations
                      if d.get("derivation_level") == "derived")
        numerical = sum(1 for d in derivations
                        if d.get("derivation_level") == "numerical_match")
        failed = sum(1 for d in derivations
                     if d.get("derivation_level") == "failed" or d.get("error"))

        self.results["summary"] = {
            "first_principles": first_principles,
            "derived": derived,
            "numerical_match": numerical,
            "failed": failed,
            "total": len(TEST_CASES),
            "total_llm_calls": self.total_llm_calls,
            "total_time_seconds": total_time,
            "total_time_hours": total_time / 3600
        }

        self._save_results()

        # Print final summary
        self.log("\n" + "=" * 70)
        self.log("BLIND TEST COMPLETE")
        self.log("=" * 70)
        self.log(f"Total time: {total_time:.1f}s ({total_time/60:.1f} min = {total_time/3600:.2f} hours)")
        self.log(f"Total LLM calls: {self.total_llm_calls}")
        self.log(f"\nResults:")
        self.log(f"  First Principles: {first_principles}/10")
        self.log(f"  Derived (math only): {derived}/10")
        self.log(f"  Numerical Match: {numerical}/10")
        self.log(f"  Failed: {failed}/10")
        self.log("=" * 70)
        self.log(f"\nResults saved to: {self.output_dir / 'results.json'}")
        self.log(f"Run validation: python /Users/carlzimmerman/new_physics/ground_truth_oracle/validate_blind_test.py")

        return self.results

    def _save_results(self):
        """Save current results to disk."""
        # Save to both locations for validation script
        with open(self.output_dir / "results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)

        # Also save to /tmp for validation script
        with open("/tmp/blind_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Starting Full Pipeline Blind Test...")
    print("This will take 3-5 hours. Results saved incrementally.")
    print("")

    runner = FullPipelineRunner()
    results = runner.run_all()
