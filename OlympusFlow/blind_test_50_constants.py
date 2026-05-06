#!/usr/bin/env python3
"""
FULL 50-CONSTANT BLIND TEST
============================

Tests ALL 50 constants from the ground truth oracle through the complete
OlympusFlow derivation pipeline with multi-prompt refinement.

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# =============================================================================
# CONFIGURATION - NO RUSHING
# =============================================================================
os.environ["LEGOMENA_TIMEOUT"] = "600"  # 10 minutes per call
os.environ["DERIVATION_ATTEMPTS"] = "4"  # Full 4-attempt multi-prompt

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from OlympusFlow.derivation_engine import DerivationEngine, MULTI_PROMPT_ATTEMPTS
from OlympusFlow.derivation_contracts import DerivationLevel, ChainStatus

# =============================================================================
# LOAD ALL 50 CONSTANTS FROM ORACLE
# =============================================================================

def load_oracle_constants() -> List[Dict]:
    """Load all 50 constants from the ground truth oracle."""
    oracle_path = Path("/Users/carlzimmerman/new_physics/ground_truth_oracle/oracle_data.json")

    with open(oracle_path) as f:
        oracle = json.load(f)

    test_cases = []
    for entry in oracle["entries"]:
        # Skip entries with 0 or very small target values (would cause issues)
        if entry["target_value"] == 0 or abs(entry["target_value"]) < 1e-30:
            continue

        test_cases.append({
            "name": entry["name"],
            "symbol": entry["name"][:10],  # Short symbol
            "target_value": entry["target_value"],
            "domain": entry.get("domain", "general"),
            "description": entry.get("physics_explanation", "")[:200],
            "derivation_status": entry.get("derivation_status", "unknown"),
            "z2_connection_known": entry.get("z2_connection_known", False),
            "known_derivation": entry.get("known_derivation", ""),
            "unit": entry.get("unit", "dimensionless")
        })

    return test_cases


# =============================================================================
# FULL PIPELINE RUNNER
# =============================================================================

class FullPipelineRunner:
    """
    Runs complete pipeline with all components and NO timeouts.
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("/tmp/blind_test_50")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize derivation engine with verbose logging
        self.engine = DerivationEngine(verbose=True)

        # Track all results
        self.results = {
            "test_name": "Full Pipeline Blind Test - 50 Oracle Constants",
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

    def run_single_derivation(self, test_case: Dict, index: int, total: int) -> Dict:
        """
        Run complete derivation for a single test case.
        """
        name = test_case["name"]
        target = test_case["target_value"]
        symbol = test_case["symbol"]

        self.log(f"\n{'='*70}")
        self.log(f"TASK {index}/{total}: {name}")
        self.log(f"Target: {target} ({test_case['unit']})")
        self.log(f"Domain: {test_case['domain']}")
        self.log(f"Oracle status: {test_case['derivation_status']}")
        self.log(f"Known Z² connection: {test_case['z2_connection_known']}")
        self.log(f"{'='*70}")

        task_start = time.time()
        llm_calls_before = self.total_llm_calls

        try:
            # ================================================================
            # PHASE 1: DERIVATION (with multi-prompt refinement)
            # ================================================================
            self.log("Phase 1: Running derivation with multi-prompt refinement...")

            chain = self.engine.derive(
                constant_name=f"{name}",
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
                experimental_source="Oracle ground truth"
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
                "unit": test_case["unit"],
                "domain": test_case["domain"],
                "description": test_case["description"],

                # Oracle info
                "oracle_derivation_status": test_case["derivation_status"],
                "oracle_z2_known": test_case["z2_connection_known"],
                "oracle_known_derivation": test_case["known_derivation"],

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
            self.log(f"  Computed: {chain.computed_value}")
            self.log(f"  Target:   {target}")
            self.log(f"  Error: {chain.percent_error:.4f}%")
            self.log(f"  Level: {chain.level.value.upper()}")
            self.log(f"  Confidence: {chain.overall_confidence:.2f}")
            self.log(f"  HRM Score: {verified.hrm_score:.2f}")
            self.log(f"  Destination: {verified.destination.value}")

            if chain.refinement_metadata:
                verdict = chain.refinement_metadata.get('final_verdict', 'N/A')
                self.log(f"  Final Verdict: {verdict}")

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

    def run_all(self, test_cases: List[Dict]) -> Dict:
        """Run all test cases."""
        total = len(test_cases)

        self.log("=" * 70)
        self.log(f"FULL PIPELINE BLIND TEST - {total} ORACLE CONSTANTS")
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

        for i, test_case in enumerate(test_cases, 1):
            result = self.run_single_derivation(test_case, i, total)
            self.results["derivations"].append(result)

            # Save intermediate results after each task
            self._save_results()

            # Progress update
            elapsed = time.time() - total_start
            remaining = total - i
            if i > 0:
                avg_per_task = elapsed / i
                eta = avg_per_task * remaining
                self.log(f"\nProgress: {i}/{total} complete")
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
            "total": total,
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
        self.log(f"  First Principles: {first_principles}/{total}")
        self.log(f"  Derived (math only): {derived}/{total}")
        self.log(f"  Numerical Match: {numerical}/{total}")
        self.log(f"  Failed: {failed}/{total}")
        self.log("=" * 70)
        self.log(f"\nResults saved to: {self.output_dir / 'results.json'}")

        return self.results

    def _save_results(self):
        """Save current results to disk."""
        with open(self.output_dir / "results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Loading 50 constants from ground truth oracle...")
    test_cases = load_oracle_constants()
    print(f"Loaded {len(test_cases)} constants")
    print("")

    print("Starting Full Pipeline Blind Test...")
    print("This may take several hours. Results saved incrementally.")
    print("")

    runner = FullPipelineRunner()
    results = runner.run_all(test_cases)
