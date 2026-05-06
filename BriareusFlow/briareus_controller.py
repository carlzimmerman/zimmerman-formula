#!/usr/bin/env python3
"""
BRIAREUS CONTROLLER - The Hundred-Handed Orchestrator
=======================================================

Named after Briareus (Aegaeon), the hundred-handed giant.
This controller orchestrates multi-threaded brute-force
phenomenological discovery.

Architecture:
┌─────────────────────────────────────────────────────────────────────┐
│                    BRIAREUS CONTROLLER                               │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   TARGET     │  │   PATTERN    │  │  GEOMETRIC   │               │
│  │    QUEUE     │──│   SEARCH     │──│ INTERPRETER  │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│         ▲                │                   │                       │
│         │                ▼                   ▼                       │
│         │         ┌──────────────┐   ┌──────────────┐               │
│         │         │  THREAD      │   │   FINDING    │               │
│         └─────────│  POOL (100)  │   │   STORAGE    │               │
│                   └──────────────┘   └──────────────┘               │
│                          │                   │                       │
│                          ▼                   ▼                       │
│                   ┌────────────────────────────────┐                │
│                   │     OLYMPUSFLOW BRIDGE         │                │
│                   │  (Send promising findings)     │                │
│                   └────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────┘

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import json
import time
import math
import threading
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set, Any, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from enum import Enum
import queue

from .phenomenological import (
    PhenomenologicalFinding,
    FindingCategory,
    NumerologyRisk,
    DiscoveryPath,
    DiscoveryMethod,
    FindingBatch,
    Z_SQUARED,
    Z,
    PHI
)
from .pattern_search import (
    PatternSearchEngine,
    SearchResult,
    PatternMatch
)
from .geometric_interpreter import (
    GeometricInterpreter,
    GeometricInterpretation
)


class SearchPriority(Enum):
    """Priority levels for search targets."""
    CRITICAL = 0     # Known Z² patterns to verify
    HIGH = 1         # Promising leads from OlympusFlow
    NORMAL = 2       # Standard exploration
    LOW = 3          # Speculative exploration
    BACKGROUND = 4   # Long-running exhaustive search


@dataclass
class SearchConfig:
    """Configuration for BriareusController."""
    # Search parameters
    max_error_percent: float = 1.0
    max_integer: int = 50
    max_denominator: int = 50
    max_z_coefficient: int = 10

    # Thread pool
    num_threads: int = 8  # The "hundred hands" (adjustable)
    max_queue_size: int = 1000

    # Storage
    output_dir: str = "/tmp/briareus"
    save_all_findings: bool = True
    save_promising_only: bool = False

    # Filters
    min_confidence: float = 0.3
    reject_pure_numerology: bool = True

    # Logging
    verbose: bool = True
    log_every_n: int = 10


@dataclass
class SearchTarget:
    """A target value to search for patterns."""
    target_id: str
    name: str
    value: float
    uncertainty: float
    source: str
    domain: str
    priority: SearchPriority = SearchPriority.NORMAL
    metadata: Dict = field(default_factory=dict)

    def __lt__(self, other):
        """Compare by priority for queue ordering."""
        return self.priority.value < other.priority.value


@dataclass
class BriareusResult:
    """Result from a BriareusController search run."""
    batch_id: str
    start_time: str
    end_time: str
    runtime_seconds: float

    # Counts
    targets_processed: int
    combinations_tested: int
    findings_total: int
    findings_promising: int
    findings_first_principles: int

    # Best findings
    best_findings: List[PhenomenologicalFinding]

    # Statistics
    avg_error_percent: float
    z2_patterns_found: int

    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "best_findings": [f.to_dict() for f in self.best_findings]
        }


class BriareusController:
    """
    The Hundred-Handed Controller for phenomenological discovery.

    Orchestrates multi-threaded brute-force search across:
    - Target values from OlympusFlow
    - Known constants needing investigation
    - Speculative exploration

    Like Briareus with his hundred hands, this controller
    can process many targets simultaneously.
    """

    def __init__(self, config: Optional[SearchConfig] = None):
        self.config = config or SearchConfig()
        self._setup_components()
        self._setup_storage()

    def _setup_components(self):
        """Initialize search components."""
        self.pattern_engine = PatternSearchEngine(
            config={
                "max_error_percent": self.config.max_error_percent,
                "max_integer": self.config.max_integer,
                "max_denominator": self.config.max_denominator,
                "max_z_coefficient": self.config.max_z_coefficient,
                "num_threads": self.config.num_threads,
            },
            verbose=False  # Controller handles logging
        )
        self.interpreter = GeometricInterpreter(verbose=False)

        # Thread-safe queue
        self.target_queue: queue.PriorityQueue = queue.PriorityQueue(
            maxsize=self.config.max_queue_size
        )

        # Thread-safe results storage
        self.results_lock = threading.Lock()
        self.all_findings: List[PhenomenologicalFinding] = []
        self.processed_count = 0
        self.total_combinations = 0

        # State
        self.running = False
        self.batch_id = ""

    def _setup_storage(self):
        """Setup storage directories."""
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.findings_dir = self.output_dir / "findings"
        self.findings_dir.mkdir(exist_ok=True)

        self.batches_dir = self.output_dir / "batches"
        self.batches_dir.mkdir(exist_ok=True)

    def _log(self, msg: str):
        if self.config.verbose:
            print(f"[Briareus] {msg}")

    def add_target(self, target: SearchTarget):
        """Add a target to the search queue."""
        try:
            self.target_queue.put_nowait((target.priority.value, target))
        except queue.Full:
            self._log(f"Queue full, dropping target: {target.name}")

    def add_targets(self, targets: List[SearchTarget]):
        """Add multiple targets to the queue."""
        for t in targets:
            self.add_target(t)

    def add_olympusflow_targets(self, olympus_results: List[Dict]):
        """
        Add targets from OlympusFlow results.

        Takes phenomenological findings that need investigation.
        """
        for result in olympus_results:
            if result.get("category") in ["phenomenological", "matches", "empirical"]:
                target = SearchTarget(
                    target_id=f"olympus_{result.get('constant_name', 'unknown')}",
                    name=result.get("constant_name", "Unknown"),
                    value=result.get("experimental_value", 0),
                    uncertainty=result.get("uncertainty", 0.001),
                    source="OlympusFlow",
                    domain=result.get("domain", "physics"),
                    priority=SearchPriority.HIGH,
                    metadata={"olympus_result": result}
                )
                self.add_target(target)

    def _process_target(self, target: SearchTarget) -> List[PhenomenologicalFinding]:
        """Process a single target - find patterns and interpret."""
        findings = []

        # Search for patterns
        result = self.pattern_engine.search(target.value, target.domain)

        # Process each match
        for match in result.matches:
            # Get geometric interpretation
            interp = self.interpreter.interpret(
                match.formula, match.computed_value, target.domain
            )

            # Assess numerology risk
            risk_str = self.interpreter.assess_numerology_risk(
                match.formula, match.computed_value,
                len(result.matches) - 1  # Alternative count
            )
            risk = {
                "low": NumerologyRisk.LOW,
                "medium": NumerologyRisk.MEDIUM,
                "high": NumerologyRisk.HIGH,
                "very_high": NumerologyRisk.VERY_HIGH
            }.get(risk_str, NumerologyRisk.UNKNOWN)

            # Skip pure numerology if configured
            if self.config.reject_pure_numerology and risk == NumerologyRisk.VERY_HIGH:
                continue

            # Skip low confidence
            if interp and interp.confidence < self.config.min_confidence:
                continue

            # Determine category
            if "Z²" in match.formula or "Z^2" in match.formula:
                category = FindingCategory.MATCHES
            elif interp and interp.confidence > 0.8:
                category = FindingCategory.MATCHES
            else:
                category = FindingCategory.PHENOMENOLOGICAL

            # Create finding
            finding = PhenomenologicalFinding(
                finding_id=f"{target.target_id}_{match.formula.replace('/', '_').replace(' ', '')}",
                name=target.name,
                domain=target.domain,
                formula=match.formula,
                computed_value=match.computed_value,
                experimental_value=target.value,
                experimental_uncertainty=target.uncertainty,
                experimental_source=target.source,
                percent_error=match.percent_error,
                sigma_deviation=(match.computed_value - target.value) / target.uncertainty if target.uncertainty > 0 else 0,
                category=category,
                numerology_risk=risk,
                discovery_path=DiscoveryPath(
                    method=match.discovery_method,
                    steps=[
                        f"BriareusFlow pattern search",
                        f"Formula: {match.formula}",
                        f"Value: {match.computed_value:.6f}",
                        f"Error: {match.percent_error:.4f}%"
                    ],
                    assumptions=[],
                    alternatives_tested=result.combinations_tested,
                    search_space_size=result.combinations_tested
                ),
                has_mechanism=bool(interp and interp.physical_mechanism),
                mechanism_description=interp.physical_mechanism if interp else "",
                testable_predictions=[]
            )

            # Add geometric interpretation details
            if interp:
                finding.mechanism_description = interp.physical_mechanism

            # Add alternative fits
            for alt_match in result.matches[:5]:
                if alt_match.formula != match.formula:
                    finding.add_alternative(
                        formula=alt_match.formula,
                        value=alt_match.computed_value,
                        error=alt_match.percent_error,
                        has_mechanism=False
                    )

            findings.append(finding)

        return findings

    def _worker(self):
        """Worker thread for processing targets."""
        while self.running:
            try:
                priority, target = self.target_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            try:
                findings = self._process_target(target)

                with self.results_lock:
                    self.all_findings.extend(findings)
                    self.processed_count += 1

                    if self.config.verbose and self.processed_count % self.config.log_every_n == 0:
                        self._log(f"Processed {self.processed_count} targets, {len(self.all_findings)} findings")

            except Exception as e:
                self._log(f"Error processing {target.name}: {e}")

            finally:
                self.target_queue.task_done()

    def run(self, max_targets: int = None, timeout: float = None) -> BriareusResult:
        """
        Run the brute-force search.

        Args:
            max_targets: Maximum targets to process (None = all)
            timeout: Maximum runtime in seconds (None = no limit)

        Returns:
            BriareusResult with all findings
        """
        self.batch_id = f"briareus_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        self._log(f"Starting batch {self.batch_id}")
        self._log(f"Queue size: {self.target_queue.qsize()}")
        self._log(f"Threads: {self.config.num_threads}")

        # Reset state
        self.running = True
        self.all_findings = []
        self.processed_count = 0
        self.total_combinations = 0

        # Start workers
        workers = []
        for i in range(self.config.num_threads):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            workers.append(t)

        # Wait for completion
        try:
            if timeout:
                deadline = time.time() + timeout
                while self.target_queue.qsize() > 0:
                    if time.time() > deadline:
                        self._log("Timeout reached")
                        break
                    time.sleep(0.5)
                    if max_targets and self.processed_count >= max_targets:
                        self._log(f"Max targets ({max_targets}) reached")
                        break
            else:
                self.target_queue.join()

        finally:
            self.running = False

        # Wait for workers
        for t in workers:
            t.join(timeout=1.0)

        end_time = datetime.now()
        runtime = (end_time - start_time).total_seconds()

        # Compute statistics
        promising = [f for f in self.all_findings if f.is_promising]
        first_principles = [f for f in self.all_findings
                           if f.category == FindingCategory.FIRST_PRINCIPLES]
        z2_patterns = [f for f in self.all_findings if "Z²" in f.formula or "Z^2" in f.formula]

        errors = [f.percent_error for f in self.all_findings]
        avg_error = sum(errors) / len(errors) if errors else 0

        # Sort best findings
        best = sorted(self.all_findings, key=lambda f: f.percent_error)[:20]

        result = BriareusResult(
            batch_id=self.batch_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            runtime_seconds=runtime,
            targets_processed=self.processed_count,
            combinations_tested=self.total_combinations,
            findings_total=len(self.all_findings),
            findings_promising=len(promising),
            findings_first_principles=len(first_principles),
            best_findings=best,
            avg_error_percent=avg_error,
            z2_patterns_found=len(z2_patterns)
        )

        # Save results
        self._save_batch(result)

        self._log(f"Batch complete: {result.findings_total} findings in {runtime:.1f}s")
        self._log(f"  Promising: {result.findings_promising}")
        self._log(f"  Z² patterns: {result.z2_patterns_found}")

        return result

    def run_on_targets(self, targets: List[SearchTarget],
                       timeout: float = None) -> BriareusResult:
        """
        Run search on specific targets.

        Args:
            targets: List of targets to search
            timeout: Maximum runtime

        Returns:
            BriareusResult
        """
        self.add_targets(targets)
        return self.run(max_targets=len(targets), timeout=timeout)

    def _save_batch(self, result: BriareusResult):
        """Save batch results to storage."""
        batch_file = self.batches_dir / f"{result.batch_id}.json"
        with open(batch_file, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

        # Save individual findings if configured
        if self.config.save_all_findings:
            for finding in self.all_findings:
                finding_file = self.findings_dir / f"{finding.finding_id}.json"
                with open(finding_file, "w") as f:
                    json.dump(finding.to_dict(), f, indent=2)

    def get_z2_findings(self) -> List[PhenomenologicalFinding]:
        """Get all findings involving Z²."""
        return [f for f in self.all_findings if "Z²" in f.formula or "Z^2" in f.formula]

    def get_promising_findings(self) -> List[PhenomenologicalFinding]:
        """Get promising findings (low error, low risk)."""
        return [f for f in self.all_findings if f.is_promising]

    def print_summary(self, result: BriareusResult):
        """Print a formatted summary of results."""
        print("=" * 70)
        print("BRIAREUS SEARCH RESULTS")
        print("=" * 70)
        print(f"Batch: {result.batch_id}")
        print(f"Runtime: {result.runtime_seconds:.1f}s")
        print(f"Targets processed: {result.targets_processed}")
        print()
        print("FINDINGS SUMMARY:")
        print(f"  Total: {result.findings_total}")
        print(f"  Promising: {result.findings_promising}")
        print(f"  First principles: {result.findings_first_principles}")
        print(f"  Z² patterns: {result.z2_patterns_found}")
        print(f"  Avg error: {result.avg_error_percent:.4f}%")
        print()
        print("BEST FINDINGS:")
        for i, f in enumerate(result.best_findings[:10], 1):
            risk_marker = "!" if f.numerology_risk in [NumerologyRisk.HIGH, NumerologyRisk.VERY_HIGH] else " "
            z2_marker = "Z²" if "Z²" in f.formula else "  "
            print(f"  {i:2}. [{z2_marker}]{risk_marker} {f.name}: {f.formula} = {f.computed_value:.6f} ({f.percent_error:.4f}%)")
        print("=" * 70)


# =============================================================================
# STANDARD TARGETS
# =============================================================================

STANDARD_PHYSICS_TARGETS = [
    SearchTarget(
        target_id="sin2_theta_w",
        name="sin²θ_W",
        value=0.23122,
        uncertainty=0.00003,
        source="PDG 2024",
        domain="particle_physics",
        priority=SearchPriority.CRITICAL
    ),
    SearchTarget(
        target_id="alpha_inv",
        name="α⁻¹",
        value=137.035999,
        uncertainty=0.000029,
        source="CODATA 2018",
        domain="particle_physics",
        priority=SearchPriority.CRITICAL
    ),
    SearchTarget(
        target_id="omega_lambda",
        name="Ω_Λ",
        value=0.685,
        uncertainty=0.007,
        source="Planck 2018",
        domain="cosmology",
        priority=SearchPriority.HIGH
    ),
    SearchTarget(
        target_id="omega_m",
        name="Ω_m",
        value=0.315,
        uncertainty=0.007,
        source="Planck 2018",
        domain="cosmology",
        priority=SearchPriority.HIGH
    ),
    SearchTarget(
        target_id="hubble",
        name="H₀",
        value=67.4,
        uncertainty=0.5,
        source="Planck 2018",
        domain="cosmology",
        priority=SearchPriority.NORMAL
    ),
    SearchTarget(
        target_id="proton_electron_ratio",
        name="m_p/m_e",
        value=1836.15267343,
        uncertainty=0.00000011,
        source="CODATA 2018",
        domain="particle_physics",
        priority=SearchPriority.NORMAL
    ),
    SearchTarget(
        target_id="gamma_mono",
        name="γ (monoatomic)",
        value=5/3,
        uncertainty=0.0001,
        source="Thermodynamics",
        domain="thermodynamics",
        priority=SearchPriority.NORMAL
    ),
    SearchTarget(
        target_id="tet_angle",
        name="θ_tetrahedral",
        value=109.4712,
        uncertainty=0.0001,
        source="Geometry",
        domain="chemistry",
        priority=SearchPriority.NORMAL
    ),
]


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BRIAREUS CONTROLLER TEST")
    print("The Hundred-Handed Phenomenological Discovery Engine")
    print("=" * 70)
    print()

    # Create controller
    config = SearchConfig(
        max_error_percent=1.0,
        num_threads=4,
        verbose=True,
        log_every_n=1
    )
    controller = BriareusController(config)

    # Add standard physics targets
    controller.add_targets(STANDARD_PHYSICS_TARGETS)

    print(f"Added {len(STANDARD_PHYSICS_TARGETS)} targets to queue")
    print()

    # Run search
    result = controller.run(timeout=60)

    # Print summary
    controller.print_summary(result)

    # Show Z² findings
    z2_findings = controller.get_z2_findings()
    if z2_findings:
        print()
        print("Z² PATTERN FINDINGS:")
        for f in z2_findings[:5]:
            print(f"  {f.name}: {f.formula} ({f.percent_error:.4f}%)")

    print()
    print("=" * 70)
    print("BRIAREUS TEST COMPLETE")
    print("=" * 70)
