#!/usr/bin/env python3
"""
OLYMPUSFLOW - Honest Pipeline
===============================

The unified, honest pipeline for Z² derivations.

PRINCIPLES:
1. NO FALSE CLAIMS - Every result is labeled with its true evidence level
2. DYNAMIC - Real API calls, real web search, real LLM queries
3. TRANSPARENT - Full audit trail of what we did and why
4. SEPARATED - Clear distinction between proof, computation, and speculation

This is the HONEST version of the derivation pipeline.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

from .honest_contracts import (
    HonestDerivation, HonestResult, ExperimentalValue,
    EvidenceLevel, DerivationType, ConnectionStrength, SourceType
)
from .honest_derivation import HonestDerivationEngine
from .experimental_api import ExperimentalDataAPI
from .symbolic_engine import SymbolicEngine


# =============================================================================
# PIPELINE INPUT/OUTPUT
# =============================================================================

@dataclass
class HonestTask:
    """A task for the honest pipeline."""
    constant_name: str
    target_value: float
    unit: str = ""
    domain: str = ""
    source: str = ""  # Where did this task come from?


@dataclass
class HonestPipelineResult:
    """Complete result from the honest pipeline."""
    task: HonestTask
    result: HonestResult

    # Pipeline metadata
    pipeline_start: str = ""
    pipeline_end: str = ""
    pipeline_duration_seconds: float = 0.0

    # Audit trail
    phases_completed: List[str] = field(default_factory=list)
    api_calls_made: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "task": {
                "constant_name": self.task.constant_name,
                "target_value": self.task.target_value,
                "unit": self.task.unit,
                "domain": self.task.domain
            },
            "result": self.result.to_dict(),
            "metadata": {
                "pipeline_start": self.pipeline_start,
                "pipeline_end": self.pipeline_end,
                "duration_seconds": self.pipeline_duration_seconds,
                "phases_completed": self.phases_completed,
                "api_calls_made": self.api_calls_made,
                "warnings": self.warnings
            }
        }


# =============================================================================
# HONEST PIPELINE
# =============================================================================

class HonestPipeline:
    """
    The honest Z² derivation pipeline.

    Flow:
    1. RESEARCH: Look up constant in real sources (APIs, web)
    2. DERIVE: Try algebraic derivation, then numerical fit
    3. VERIFY: Use SymPy to verify mathematical steps
    4. COMPARE: Compare with experimental values from real sources
    5. LABEL: Honestly label what we found

    NO FALSE CLAIMS. FULL TRANSPARENCY.
    """

    def __init__(self, output_dir: str = "honest_results", verbose: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose

        # Initialize components
        self.engine = HonestDerivationEngine(verbose=verbose)
        self.experimental = ExperimentalDataAPI(verbose=verbose)
        self.symbolic = SymbolicEngine(verbose=verbose)

        # Statistics
        self.stats = {
            "total": 0,
            "algebraic_proofs": 0,
            "numerical_fits": 0,
            "speculative": 0,
            "failed": 0,
            "api_verified": 0,
            "llm_sourced": 0
        }

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[HonestPipeline {ts}] {msg}")

    # =========================================================================
    # MAIN PIPELINE
    # =========================================================================

    def run(self, task: HonestTask) -> HonestPipelineResult:
        """
        Run the honest pipeline on a single task.

        Returns HonestPipelineResult with full audit trail.
        """
        self._log(f"\n{'='*70}")
        self._log(f"HONEST PIPELINE: {task.constant_name}")
        self._log(f"{'='*70}")

        start_time = datetime.now()

        pipeline_result = HonestPipelineResult(
            task=task,
            result=None,
            pipeline_start=start_time.isoformat()
        )

        try:
            # Phase 1: Get derivation result
            self._log("\n[PHASE 1] Running honest derivation engine...")
            pipeline_result.phases_completed.append("derivation")

            result = self.engine.derive(
                task.constant_name,
                task.target_value,
                task.unit
            )

            pipeline_result.result = result

            # Phase 2: Additional API verification if needed
            self._log("\n[PHASE 2] Verifying experimental data sources...")
            pipeline_result.phases_completed.append("verification")

            if result.experimental:
                if result.experimental.source_type == SourceType.LLM_ASSERTION:
                    pipeline_result.warnings.append(
                        "Experimental value came from LLM - consider verifying manually"
                    )
                    self.stats["llm_sourced"] += 1
                elif result.experimental.is_verified:
                    self.stats["api_verified"] += 1
                    pipeline_result.api_calls_made.append(
                        f"CODATA/NIST: {result.experimental.source_url}"
                    )

            # Phase 3: Final assessment
            self._log("\n[PHASE 3] Final honest assessment...")
            pipeline_result.phases_completed.append("assessment")

            self._update_stats(result)

            # Add warnings based on evidence level
            self._add_honest_warnings(pipeline_result)

        except Exception as e:
            self._log(f"Pipeline error: {e}")
            pipeline_result.warnings.append(f"Pipeline error: {str(e)}")

        # Record timing
        end_time = datetime.now()
        pipeline_result.pipeline_end = end_time.isoformat()
        pipeline_result.pipeline_duration_seconds = (end_time - start_time).total_seconds()

        # Save result
        self._save_result(pipeline_result)

        self._log(f"\nCompleted in {pipeline_result.pipeline_duration_seconds:.1f}s")

        return pipeline_result

    def run_batch(self, tasks: List[HonestTask]) -> List[HonestPipelineResult]:
        """Run pipeline on multiple tasks."""
        results = []

        self._log(f"\n{'='*70}")
        self._log(f"HONEST BATCH RUN: {len(tasks)} tasks")
        self._log(f"{'='*70}")

        for i, task in enumerate(tasks):
            self._log(f"\n[{i+1}/{len(tasks)}] {task.constant_name}")
            result = self.run(task)
            results.append(result)
            self.stats["total"] += 1

        # Generate summary
        self._save_batch_summary(results)

        return results

    # =========================================================================
    # HONEST ASSESSMENT
    # =========================================================================

    def _update_stats(self, result: HonestResult):
        """Update statistics based on result."""
        level = result.derivation.evidence_level

        if level == EvidenceLevel.ALGEBRAIC_PROOF:
            self.stats["algebraic_proofs"] += 1
        elif level == EvidenceLevel.NUMERICAL_FIT:
            self.stats["numerical_fits"] += 1
        elif level == EvidenceLevel.LLM_SPECULATION:
            self.stats["speculative"] += 1
        else:
            self.stats["failed"] += 1

    def _add_honest_warnings(self, pipeline_result: HonestPipelineResult):
        """Add honest warnings based on evidence level."""
        result = pipeline_result.result
        level = result.derivation.evidence_level

        if level == EvidenceLevel.NUMERICAL_FIT:
            pipeline_result.warnings.append(
                "This is a NUMERICAL FIT, not a derivation. "
                "The formula matches the number but has no proven physical connection."
            )

        if level == EvidenceLevel.LLM_SPECULATION:
            pipeline_result.warnings.append(
                "This connection was SUGGESTED by an LLM. "
                "It has NOT been mathematically or physically verified."
            )

        if result.derivation.num_assumptions > 0:
            pipeline_result.warnings.append(
                f"Derivation includes {result.derivation.num_assumptions} unverified assumption(s)."
            )

        if result.derivation.connection_strength == ConnectionStrength.NUMERICAL_ONLY:
            pipeline_result.warnings.append(
                "Z² connection is numerical only - could be coincidence."
            )

        if not result.is_publishable:
            if result.algebraic_confidence < 0.8:
                pipeline_result.warnings.append(
                    f"Low algebraic confidence ({result.algebraic_confidence:.2f}) - "
                    "most steps not verified by SymPy."
                )

    # =========================================================================
    # OUTPUT
    # =========================================================================

    def _save_result(self, result: HonestPipelineResult):
        """Save individual result to disk."""
        # Sanitize filename
        safe_name = result.task.constant_name.lower()
        safe_name = "".join(c if c.isalnum() or c in "_ " else "_" for c in safe_name)
        safe_name = safe_name.replace(" ", "_")

        filepath = self.output_dir / f"{safe_name}_honest.json"
        filepath.write_text(json.dumps(result.to_dict(), indent=2, default=str))

    def _save_batch_summary(self, results: List[HonestPipelineResult]):
        """Save batch summary with honest statistics."""
        summary = {
            "run_timestamp": datetime.now().isoformat(),
            "total_tasks": len(results),
            "statistics": self.stats,
            "honest_breakdown": {
                "algebraic_proofs": {
                    "count": self.stats["algebraic_proofs"],
                    "description": "Mathematically verified derivations"
                },
                "numerical_fits": {
                    "count": self.stats["numerical_fits"],
                    "description": "Pattern matching - NOT derivations"
                },
                "speculative": {
                    "count": self.stats["speculative"],
                    "description": "LLM speculation - NOT verified"
                },
                "failed": {
                    "count": self.stats["failed"],
                    "description": "No Z² connection found"
                }
            },
            "data_source_reliability": {
                "api_verified": self.stats["api_verified"],
                "llm_sourced": self.stats["llm_sourced"],
                "note": "LLM-sourced values should be manually verified"
            },
            "results": [r.to_dict() for r in results]
        }

        filepath = self.output_dir / "HONEST_SUMMARY.json"
        filepath.write_text(json.dumps(summary, indent=2, default=str))
        self._log(f"Saved honest summary to {filepath}")

    # =========================================================================
    # REPORTING
    # =========================================================================

    def generate_honest_report(self, results: List[HonestPipelineResult]) -> str:
        """Generate a comprehensive honest report."""
        lines = [
            "=" * 70,
            "HONEST Z² DERIVATION REPORT",
            "=" * 70,
            f"Generated: {datetime.now().isoformat()}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 70,
            f"Total constants analyzed: {len(results)}",
            f"Algebraic proofs (publishable): {self.stats['algebraic_proofs']}",
            f"Numerical fits (NOT derivations): {self.stats['numerical_fits']}",
            f"LLM speculation only: {self.stats['speculative']}",
            f"No connection found: {self.stats['failed']}",
            "",
            "DATA SOURCE RELIABILITY",
            "-" * 70,
            f"API-verified experimental values: {self.stats['api_verified']}",
            f"LLM-sourced values (UNVERIFIED): {self.stats['llm_sourced']}",
            "",
        ]

        # Categorize results
        algebraic = [r for r in results
                     if r.result and r.result.derivation.evidence_level == EvidenceLevel.ALGEBRAIC_PROOF]
        numerical = [r for r in results
                     if r.result and r.result.derivation.evidence_level == EvidenceLevel.NUMERICAL_FIT]
        speculative = [r for r in results
                       if r.result and r.result.derivation.evidence_level == EvidenceLevel.LLM_SPECULATION]
        failed = [r for r in results
                  if r.result and r.result.derivation.evidence_level not in
                  [EvidenceLevel.ALGEBRAIC_PROOF, EvidenceLevel.NUMERICAL_FIT, EvidenceLevel.LLM_SPECULATION]]

        if algebraic:
            lines.extend([
                "=" * 70,
                "ALGEBRAIC PROOFS (Verified - Publishable)",
                "=" * 70,
            ])
            for r in algebraic:
                d = r.result.derivation
                lines.extend([
                    f"\n{d.constant_name}",
                    f"  Formula: {d.final_formula}",
                    f"  Computed: {d.computed_value:.10f}",
                    f"  Target: {d.target_value}",
                    f"  Error: {d.percent_error:.6f}%",
                    f"  SymPy verified steps: {d.num_sympy_verified}/{len(d.steps)}",
                    f"  Assumptions: {d.num_assumptions}",
                ])
            lines.append("")

        if numerical:
            lines.extend([
                "=" * 70,
                "NUMERICAL FITS (Pattern Matching - NOT Derivations)",
                "=" * 70,
                "",
                "WARNING: These formulas match the numbers but have NO proven",
                "         physical connection to Z². They could be coincidences.",
                "",
            ])
            for r in numerical:
                d = r.result.derivation
                lines.extend([
                    f"\n{d.constant_name}",
                    f"  Formula: {d.final_formula}",
                    f"  Computed: {d.computed_value:.10f}",
                    f"  Target: {d.target_value}",
                    f"  Error: {d.percent_error:.6f}%",
                    f"  Connection: NUMERICAL ONLY (unproven)",
                ])
            lines.append("")

        if speculative:
            lines.extend([
                "=" * 70,
                "LLM SPECULATION (Not Verified - Do Not Trust)",
                "=" * 70,
                "",
                "WARNING: These connections were suggested by an LLM.",
                "         They have NOT been mathematically verified.",
                "",
            ])
            for r in speculative:
                d = r.result.derivation
                lines.extend([
                    f"\n{d.constant_name}",
                    f"  LLM said: {d.llm_contribution[:80]}...",
                ])
            lines.append("")

        if failed:
            lines.extend([
                "=" * 70,
                "NO CONNECTION FOUND",
                "=" * 70,
            ])
            for r in failed:
                lines.append(f"  {r.task.constant_name}: No Z² connection established")
            lines.append("")

        lines.extend([
            "=" * 70,
            "METHODOLOGY NOTES",
            "=" * 70,
            "",
            "This pipeline uses:",
            "1. Real API calls to CODATA/NIST for experimental values",
            "2. SymPy for algebraic verification of derivation steps",
            "3. Legomena (LLM) for speculation (clearly labeled as such)",
            "4. Web search fallback for constants not in databases",
            "",
            "Evidence levels:",
            "- ALGEBRAIC_PROOF: Every step verified by SymPy",
            "- COMPUTED_MATCH: Formula evaluates correctly",
            "- NUMERICAL_FIT: Pattern matching found formula (numerology)",
            "- LLM_SPECULATION: LLM suggested connection (not evidence)",
            "- UNVERIFIED: No connection established",
            "",
            "ONLY 'ALGEBRAIC_PROOF' results should be considered for publication.",
            "=" * 70,
        ])

        return "\n".join(lines)


# =============================================================================
# DEMO / TEST
# =============================================================================

def demo():
    """Run the honest pipeline on test constants."""
    pipeline = HonestPipeline(output_dir="honest_demo_results")

    # Test constants
    tasks = [
        HonestTask("Dark Energy Density", 0.6847, "dimensionless", "cosmology"),
        HonestTask("Weak Mixing Angle", 0.23122, "dimensionless", "particle_physics"),
        HonestTask("von Karman Constant", 0.41, "dimensionless", "fluid_dynamics"),
        HonestTask("Fine Structure Constant", 1/137.036, "dimensionless", "QED"),
        HonestTask("Feigenbaum Delta", 4.669201, "dimensionless", "chaos_theory"),
    ]

    print("\n" + "=" * 70)
    print("HONEST PIPELINE DEMONSTRATION")
    print("=" * 70)

    results = pipeline.run_batch(tasks)

    # Print report
    report = pipeline.generate_honest_report(results)
    print("\n" + report)

    # Save report
    report_path = Path("honest_demo_results") / "HONEST_REPORT.txt"
    report_path.write_text(report)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    demo()
