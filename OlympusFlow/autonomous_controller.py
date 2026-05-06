#!/usr/bin/env python3
"""
AUTONOMOUS CONTROLLER - Continuous Z² Discovery Engine
=======================================================

Orchestrates continuous, autonomous derivation discovery:
1. Pulls targets from queue (AlpheusFlow)
2. Runs derivations (DerivationEngine)
3. Learns from results (LearningLoop)
4. Generates new targets
5. Checkpoints for resumability

Can run indefinitely without human intervention.

Author: Carl Zimmerman
Date: May 6, 2026
Version: 2.0.0
"""

import os
import sys
import json
import time
import signal
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Callable
from pathlib import Path
from datetime import datetime
from queue import PriorityQueue
from enum import Enum
import threading

# Add parent path
sys.path.insert(0, str(Path(__file__).parent.parent))

from OlympusFlow.formula_generator import FormulaGenerator, FormulaCandidate
from OlympusFlow.learning_loop import LearningLoop, SuggestedTarget
from OlympusFlow.derivation_engine import DerivationEngine
from OlympusFlow.derivation_contracts import DerivationLevel, ChainStatus
from OlympusFlow.sympy_verifier import SymPyVerifier, VerificationLevel
from OlympusFlow.prediction_generator import PredictionGenerator, TestablePrediction
from OlympusFlow.cyllene_bridge import CylleneBridge


class ControllerState(Enum):
    """States of the autonomous controller."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class DerivationTarget:
    """A target constant for derivation."""
    constant_name: str
    target_value: float
    domain: str
    priority: float = 0.5      # 0-1, higher = process first
    source: str = "manual"     # How this target was added
    attempts: int = 0          # Number of derivation attempts
    max_attempts: int = 3      # Max attempts before giving up

    def __lt__(self, other):
        """For priority queue ordering (higher priority = lower number)."""
        return (1 - self.priority) < (1 - other.priority)


@dataclass
class ControllerStats:
    """Statistics for the autonomous controller."""
    started_at: str = ""
    last_checkpoint: str = ""
    total_targets_processed: int = 0
    successful_derivations: int = 0
    failed_derivations: int = 0
    numerology_rejected: int = 0
    first_principles_found: int = 0
    queue_size: int = 0
    running_time_seconds: float = 0
    targets_generated: int = 0
    predictions_generated: int = 0
    high_value_predictions: int = 0
    cyllene_deepenings: int = 0

    def to_dict(self) -> Dict:
        return asdict(self)


class AutonomousController:
    """
    Autonomous Z² derivation discovery engine.

    Runs continuously, processing derivation targets from a queue,
    learning from results, and generating new targets.
    """

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        checkpoint_interval: int = 60,
        verbose: bool = True
    ):
        """
        Initialize the autonomous controller.

        Args:
            output_dir: Directory for output and checkpoints
            checkpoint_interval: Seconds between checkpoints
            verbose: Print progress information
        """
        self.output_dir = output_dir or Path("/tmp/autonomous_z2")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.checkpoint_interval = checkpoint_interval
        self.verbose = verbose

        # Core components
        self.engine = DerivationEngine(verbose=verbose)
        self.formula_gen = FormulaGenerator(max_error=1.0, verbose=False)
        self.learning = LearningLoop(self.output_dir / "learning")
        self.sympy_verifier = SymPyVerifier(verbose=False)  # Formal algebraic verification
        self.prediction_gen = PredictionGenerator()  # Testable prediction generation
        self.cyllene = CylleneBridge(verbose=False)  # Deepener integration

        # Queue (priority queue - lower number = higher priority)
        self.queue: PriorityQueue = PriorityQueue()

        # State
        self.state = ControllerState.IDLE
        self.stats = ControllerStats()
        self._running = False
        self._stop_event = threading.Event()

        # Results storage
        self.results: List[Dict] = []

        # Callbacks
        self.on_success: Optional[Callable] = None
        self.on_failure: Optional[Callable] = None
        self.on_checkpoint: Optional[Callable] = None

        # Load checkpoint if exists
        self._load_checkpoint()

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.log("Received shutdown signal, stopping gracefully...")
        self.stop()

    def log(self, msg: str):
        """Log with timestamp."""
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}")

        # Also write to log file
        with open(self.output_dir / "controller.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")

    def add_target(self, target: DerivationTarget):
        """Add a target to the queue."""
        self.queue.put(target)
        self.stats.queue_size = self.queue.qsize()

    def add_targets(self, targets: List[DerivationTarget]):
        """Add multiple targets to the queue."""
        for t in targets:
            self.queue.put(t)
        self.stats.queue_size = self.queue.qsize()

    def seed_from_oracle(self, oracle_path: Path):
        """
        Seed the queue from the ground truth oracle.

        Args:
            oracle_path: Path to oracle_data.json
        """
        with open(oracle_path) as f:
            oracle = json.load(f)

        targets = []
        for entry in oracle["entries"]:
            if entry["target_value"] == 0:
                continue

            target = DerivationTarget(
                constant_name=entry["name"],
                target_value=entry["target_value"],
                domain=entry.get("domain", "general"),
                priority=0.5,
                source="oracle"
            )
            targets.append(target)

        self.add_targets(targets)
        self.log(f"Seeded {len(targets)} targets from oracle")

    def seed_from_list(self, constants: List[Dict]):
        """
        Seed the queue from a list of constants.

        Args:
            constants: List of dicts with name, target_value, domain
        """
        targets = []
        for c in constants:
            target = DerivationTarget(
                constant_name=c["name"],
                target_value=c["target_value"],
                domain=c.get("domain", "general"),
                priority=c.get("priority", 0.5),
                source="manual"
            )
            targets.append(target)

        self.add_targets(targets)
        self.log(f"Seeded {len(targets)} targets")

    def run_forever(self):
        """
        Run the autonomous loop until stopped.

        This is the main entry point for continuous operation.
        """
        self.state = ControllerState.RUNNING
        self._running = True
        self._stop_event.clear()

        self.stats.started_at = datetime.now().isoformat()
        start_time = time.time()
        last_checkpoint = time.time()

        self.log("=" * 60)
        self.log("AUTONOMOUS Z² ENGINE STARTED")
        self.log(f"Queue size: {self.queue.qsize()}")
        self.log("=" * 60)

        while self._running and not self._stop_event.is_set():
            # Check if queue is empty
            if self.queue.empty():
                self.log("Queue empty, generating new targets...")
                self._generate_new_targets()

                if self.queue.empty():
                    self.log("No more targets to process, stopping")
                    break

            # Get next target
            target = self.queue.get()
            self.stats.queue_size = self.queue.qsize()

            # Process target
            try:
                self._process_target(target)
            except Exception as e:
                self.log(f"Error processing {target.constant_name}: {e}")
                import traceback
                traceback.print_exc()

            # Update stats
            self.stats.total_targets_processed += 1
            self.stats.running_time_seconds = time.time() - start_time

            # Checkpoint
            if time.time() - last_checkpoint > self.checkpoint_interval:
                self._save_checkpoint()
                last_checkpoint = time.time()

        # Final checkpoint
        self._save_checkpoint()
        self.state = ControllerState.STOPPED

        self.log("=" * 60)
        self.log("AUTONOMOUS ENGINE STOPPED")
        self.log(f"Processed: {self.stats.total_targets_processed} targets")
        self.log(f"Successes: {self.stats.successful_derivations}")
        self.log(f"First principles: {self.stats.first_principles_found}")
        self.log(f"Numerology rejected: {self.stats.numerology_rejected}")
        self.log(f"Runtime: {self.stats.running_time_seconds:.1f}s")
        self.log("=" * 60)

    def run(
        self,
        max_iterations: int = None,
        timeout: float = None,
        stop_on_empty: bool = True
    ):
        """
        Run the autonomous derivation engine.

        Args:
            max_iterations: Maximum number of targets to process (None = unlimited)
            timeout: Maximum runtime in seconds (None = unlimited)
            stop_on_empty: Stop when queue is empty (default True)

        Returns:
            Dict with run statistics
        """
        import time
        start_time = time.time()
        iterations = 0

        self.state = ControllerState.RUNNING
        self._running = True
        self.stats.started_at = datetime.now().isoformat()

        self.log("=" * 60)
        self.log("AUTONOMOUS Z² ENGINE STARTING")
        self.log(f"Max iterations: {max_iterations or 'unlimited'}")
        self.log(f"Timeout: {timeout or 'unlimited'}s")
        self.log(f"Queue size: {self.queue.qsize()}")
        self.log("=" * 60)

        try:
            while self._running:
                # Check timeout
                if timeout and (time.time() - start_time) > timeout:
                    self.log("Timeout reached")
                    break

                # Check max iterations
                if max_iterations and iterations >= max_iterations:
                    self.log(f"Max iterations ({max_iterations}) reached")
                    break

                # Check queue
                if self.queue.empty():
                    self._generate_new_targets()
                    if self.queue.empty():
                        if stop_on_empty:
                            self.log("Queue empty, stopping")
                            break
                        else:
                            time.sleep(1)  # Wait for new targets
                            continue

                # Process target
                target = self.queue.get()
                self._process_target(target)
                self.stats.total_targets_processed += 1
                iterations += 1

                # Periodic checkpoint
                elapsed = time.time() - start_time
                if elapsed > 0 and int(elapsed) % self.checkpoint_interval == 0:
                    self._save_checkpoint()

        except KeyboardInterrupt:
            self.log("Interrupted by user")
        except Exception as e:
            self.log(f"Error: {e}")
            raise
        finally:
            self.stats.running_time_seconds = time.time() - start_time
            self._save_checkpoint()
            self.state = ControllerState.STOPPED

        return {
            "iterations": iterations,
            "runtime": time.time() - start_time,
            "successes": self.stats.successful_derivations,
            "failures": self.stats.failed_derivations,
            "numerology_rejected": self.stats.numerology_rejected,
            "first_principles": self.stats.first_principles_found
        }

    def run_n(self, n: int):
        """
        Run the loop for exactly n targets.

        Args:
            n: Number of targets to process
        """
        return self.run(max_iterations=n, stop_on_empty=True)

    def _process_target(self, target: DerivationTarget):
        """
        Process a single derivation target.

        Args:
            target: The target to process
        """
        self.log(f"\n{'─'*50}")
        self.log(f"Processing: {target.constant_name}")
        self.log(f"Target: {target.target_value}")
        self.log(f"Domain: {target.domain}")
        self.log(f"Attempt: {target.attempts + 1}/{target.max_attempts}")

        start_time = time.time()

        # Step 1: Find candidate formulas
        formula_result = self.formula_gen.search(target.target_value)
        best_formula = formula_result.best_match

        if not best_formula:
            self.log("  No formula found")
            self._handle_failure(target, "No formula found", [])
            return

        self.log(f"  Best formula: {best_formula.formula_str}")
        self.log(f"  Type: {best_formula.formula_type.value}")
        self.log(f"  Error: {best_formula.percent_error:.4f}%")

        # Step 2: Run derivation with DerivationEngine
        try:
            chain = self.engine.derive(
                constant_name=target.constant_name,
                target_value=target.target_value
            )
        except Exception as e:
            self.log(f"  Derivation error: {e}")
            self._handle_failure(target, str(e), [best_formula.formula_str])
            return

        # Step 3: Check result
        if chain.level == DerivationLevel.FAILED:
            self.log(f"  Derivation FAILED")
            self._handle_failure(target, "Derivation failed", [chain.final_formula])
            return

        # Step 4: Verify
        try:
            verified = self.engine.verify(
                chain,
                experimental_value=target.target_value,
                experimental_source="Target value"
            )
        except Exception as e:
            self.log(f"  Verification error: {e}")
            self._handle_failure(target, str(e), [chain.final_formula])
            return

        # Step 5: Evaluate result
        elapsed = time.time() - start_time

        result = {
            "constant_name": target.constant_name,
            "target_value": target.target_value,
            "domain": target.domain,
            "formula": chain.final_formula,
            "formula_type": best_formula.formula_type.value,
            "computed_value": chain.computed_value,
            "percent_error": chain.percent_error,
            "derivation_level": chain.level.value,
            "chain_status": chain.status.value,
            "confidence": chain.overall_confidence,
            "hrm_score": verified.hrm_score,
            "destination": verified.destination.value,
            "processing_time": elapsed,
            "timestamp": datetime.now().isoformat()
        }

        # Check for numerology rejection
        refinement = chain.refinement_metadata
        if refinement and refinement.get("final_verdict") == "NUMEROLOGY":
            self.log(f"  Verdict: NUMEROLOGY (rejected)")
            self.stats.numerology_rejected += 1
            result["verdict"] = "NUMEROLOGY"
            self._handle_failure(
                target,
                "numerology - no physical mechanism",
                [chain.final_formula]
            )
            return

        # Step 6: SymPy Formal Verification
        # Add algebraic verification to catch any remaining numerology
        sympy_result = self.sympy_verifier.verify(
            formula=chain.final_formula,
            target_value=target.target_value,
            uncertainty=target.target_value * 0.01  # 1% default uncertainty
        )

        result["sympy_verification"] = {
            "level": sympy_result.level.value,
            "z2_appears": sympy_result.z2_appears,
            "z2_essential": sympy_result.z2_essential,
            "simplified": sympy_result.simplified_formula,
            "relative_error": sympy_result.relative_error
        }

        # Log SymPy results
        self.log(f"  SymPy Level: {sympy_result.level.value}")
        if sympy_result.z2_appears:
            self.log(f"  Z² Present: Yes (essential: {sympy_result.z2_essential})")

        # If SymPy finds Z² is not essential when LLM thought it was, warn
        if sympy_result.z2_appears and not sympy_result.z2_essential:
            result["warnings"] = result.get("warnings", [])
            result["warnings"].append("Z² may be coincidental - not algebraically essential")
            self.log(f"  WARNING: Z² may not be algebraically essential")

        # Success!
        self.log(f"  SUCCESS: {chain.level.value}")
        self.log(f"  Formula: {chain.final_formula}")
        self.log(f"  HRM: {verified.hrm_score:.2f}")
        self.log(f"  Destination: {verified.destination.value}")

        self.stats.successful_derivations += 1
        if chain.level == DerivationLevel.FIRST_PRINCIPLES:
            self.stats.first_principles_found += 1

        result["success"] = True
        self.results.append(result)

        # Learn from success
        self.learning.learn_from_success(result)

        # Step 7: Generate Testable Predictions
        # This is what distinguishes physics from numerology
        predictions = self.prediction_gen.generate_predictions(result)
        result["testable_predictions"] = [
            {
                "id": p.prediction_id,
                "type": p.prediction_type.value,
                "description": p.description,
                "predicted_value": p.predicted_value,
                "distinguishing_power": p.distinguishing_power,
                "testability": p.testability
            }
            for p in predictions
        ]

        # Log high-value predictions and update stats
        high_value = [p for p in predictions if p.distinguishing_power >= 0.7]
        self.stats.predictions_generated += len(predictions)
        self.stats.high_value_predictions += len(high_value)

        if high_value:
            self.log(f"  Generated {len(predictions)} predictions ({len(high_value)} high-value)")
            for p in high_value[:3]:  # Show top 3
                self.log(f"    - {p.description}")

        # Generate follow-up targets from learning loop
        suggestions = self.learning.suggest_similar_targets(result)
        for s in suggestions[:3]:  # Add top 3 suggestions
            if s.target_value > 0:
                new_target = DerivationTarget(
                    constant_name=s.constant_name,
                    target_value=s.target_value,
                    domain=s.domain,
                    priority=s.priority,
                    source="learning_loop"
                )
                self.add_target(new_target)
                self.stats.targets_generated += 1

        # Step 8: CylleneBridge deepening - ask "why does this work?"
        # For first-principles derivations, generate deeper research targets
        if chain.level == DerivationLevel.FIRST_PRINCIPLES:
            cyllene_targets = self.cyllene.generate_followup_targets(result, max_targets=3)
            for ct in cyllene_targets:
                if ct.get("target_value", 0) > 0:
                    new_target = DerivationTarget(
                        constant_name=ct["constant_name"],
                        target_value=ct["target_value"],
                        domain=ct.get("domain", "general"),
                        priority=ct.get("priority", 0.6),
                        source="cyllene_deepener"
                    )
                    self.add_target(new_target)
                    self.stats.targets_generated += 1

            if cyllene_targets:
                self.log(f"  CylleneBridge: +{len(cyllene_targets)} deepening targets")

        # Callback
        if self.on_success:
            self.on_success(result)

    def _handle_failure(
        self,
        target: DerivationTarget,
        reason: str,
        attempted: List[str]
    ):
        """Handle a failed derivation."""
        target.attempts += 1

        # Re-queue if not at max attempts
        if target.attempts < target.max_attempts:
            target.priority *= 0.8  # Lower priority
            self.add_target(target)
            self.log(f"  Re-queued (attempt {target.attempts})")
        else:
            self.stats.failed_derivations += 1
            self.log(f"  Gave up after {target.attempts} attempts")

        # Learn from failure
        failure_result = {
            "constant_name": target.constant_name,
            "target_value": target.target_value,
            "failure_reason": reason,
            "attempted_formulas": attempted,
            "domain": target.domain
        }
        self.learning.learn_from_failure(failure_result)

        # Callback
        if self.on_failure:
            self.on_failure(failure_result)

    def _generate_new_targets(self):
        """Generate new targets when queue is empty."""
        # Strategy 1: Use learned patterns to suggest new targets
        for pattern_id, pattern in self.learning.patterns.items():
            if pattern.success_count > 0:
                # TODO: Generate similar constants
                pass

        # Strategy 2: Scan for unexplored domains
        explored_domains = set(
            r.get("domain") for r in self.results if r.get("success")
        )
        all_domains = [
            "particle_physics", "cosmology", "quantum", "thermodynamics",
            "fluid_dynamics", "mathematics", "geometry", "materials",
            "nuclear", "astrophysics"
        ]

        unexplored = [d for d in all_domains if d not in explored_domains]
        if unexplored:
            self.log(f"  Unexplored domains: {unexplored}")
            # TODO: Generate targets for unexplored domains

    def stop(self):
        """Stop the autonomous loop."""
        self._running = False
        self._stop_event.set()
        self.state = ControllerState.STOPPED

    def pause(self):
        """Pause the autonomous loop."""
        self._running = False
        self.state = ControllerState.PAUSED

    def resume(self):
        """Resume the autonomous loop."""
        if self.state == ControllerState.PAUSED:
            self.run_forever()

    def _save_checkpoint(self):
        """Save current state to checkpoint."""
        self.stats.last_checkpoint = datetime.now().isoformat()

        checkpoint = {
            "stats": self.stats.to_dict(),
            "queue_size": self.queue.qsize(),
            "results_count": len(self.results),
            "learning_stats": self.learning.get_stats()
        }

        checkpoint_file = self.output_dir / "checkpoint.json"
        with open(checkpoint_file, "w") as f:
            json.dump(checkpoint, f, indent=2)

        # Save results
        results_file = self.output_dir / "results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

        if self.verbose:
            self.log(f"Checkpoint saved ({len(self.results)} results)")

        if self.on_checkpoint:
            self.on_checkpoint(checkpoint)

    def _load_checkpoint(self):
        """Load state from checkpoint if exists."""
        checkpoint_file = self.output_dir / "checkpoint.json"
        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                checkpoint = json.load(f)

            self.stats = ControllerStats(**checkpoint.get("stats", {}))
            self.log(f"Loaded checkpoint: {self.stats.total_targets_processed} processed")

        # Load results
        results_file = self.output_dir / "results.json"
        if results_file.exists():
            with open(results_file) as f:
                self.results = json.load(f)

    def get_status(self) -> Dict:
        """Get current controller status."""
        return {
            "state": self.state.value,
            "queue_size": self.queue.qsize(),
            "stats": self.stats.to_dict(),
            "learning": self.learning.get_stats()
        }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Starting Autonomous Z² Engine...")
    print()

    controller = AutonomousController(
        output_dir=Path("/tmp/autonomous_z2_test"),
        checkpoint_interval=30
    )

    # Seed with known Z² constants for testing
    test_constants = [
        {"name": "Weak Mixing Angle", "target_value": 0.23122, "domain": "particle_physics", "priority": 0.9},
        {"name": "Fine Structure Inverse", "target_value": 137.036, "domain": "particle_physics", "priority": 0.9},
        {"name": "Dark Energy Fraction", "target_value": 0.685, "domain": "cosmology", "priority": 0.8},
        {"name": "Tetrahedral Angle", "target_value": 109.4712, "domain": "geometry", "priority": 0.7},
        {"name": "Heat Capacity Ratio", "target_value": 5/3, "domain": "thermodynamics", "priority": 0.7},
    ]

    controller.seed_from_list(test_constants)

    # Run for 5 targets
    controller.run_n(5)

    # Print final status
    print("\nFinal Status:")
    print(json.dumps(controller.get_status(), indent=2))
