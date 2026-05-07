#!/usr/bin/env python3
"""
OLYMPUSFLOW DAEMON - 24/7 Autonomous Research System
======================================================

The daemon orchestrates continuous, autonomous research using the
full OlympusFlow stack:

    Flows: Hermes, Metis, Briareus, Truth, Cyllene, Alpheus, Ergon
    Lakes: Aletheia, Mnemosyne, Helicon
    Watchers: Hecate (primary oversight)

Scientific Method Loop:
    1. OBSERVE: Fetch data from external sources (Hermes)
    2. HYPOTHESIZE: Generate Z² predictions (Briareus, Ergon)
    3. TEST: Run derivations (DerivationPipeline)
    4. VALIDATE: Verify against experiment (TruthFlow)
    5. ASSESS: Honest HRM evaluation (Hecate)
    6. LEARN: Update training data (Cyllene)
    7. DEEPEN: Generate follow-up questions (Cyllene)
    8. REPEAT

Architecture:
```
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     OLYMPUSFLOW DAEMON                               │
    │                     (24/7 Orchestrator)                              │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                      │
    │   ┌─────────────────────────────────────────────────────────────┐   │
    │   │                        HECATE                                │   │
    │   │              (Watches all transitions)                       │   │
    │   └─────────────────────────────────────────────────────────────┘   │
    │                              │                                       │
    │        ┌─────────────────────┼─────────────────────┐                │
    │        │                     │                     │                │
    │        ▼                     ▼                     ▼                │
    │   ┌─────────┐          ┌─────────┐          ┌─────────┐            │
    │   │ ALPHEUS │          │ PIPELINE│          │ CYLLENE │            │
    │   │ (Queue) │─────────▶│ (Run)   │─────────▶│ (Learn) │            │
    │   └─────────┘          └─────────┘          └─────────┘            │
    │        │                     │                     │                │
    │        │                     │                     │                │
    │        ▼                     ▼                     ▼                │
    │   ┌─────────────────────────────────────────────────────────────┐   │
    │   │                         LAKES                                │   │
    │   │  Aletheia (truths)  Mnemosyne (memory)  Helicon (sources)   │   │
    │   └─────────────────────────────────────────────────────────────┘   │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

Usage:
    # Start the daemon
    python -m OlympusFlow.daemon --mode continuous

    # Run for specific duration
    python -m OlympusFlow.daemon --duration 3600  # 1 hour

    # Dry run (no external API calls)
    python -m OlympusFlow.daemon --dry-run

Author: Carl Zimmerman
Date: May 7, 2026
"""

import os
import sys
import json
import time
import signal
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum

# Ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent))


class DaemonMode(Enum):
    """Daemon operating modes."""
    CONTINUOUS = "continuous"      # Run forever
    TIMED = "timed"                # Run for duration
    BATCH = "batch"                # Process queue then stop
    SINGLE = "single"              # Single task then stop


class DaemonState(Enum):
    """Daemon state machine states."""
    INITIALIZING = "initializing"
    IDLE = "idle"
    OBSERVING = "observing"        # Fetching data
    HYPOTHESIZING = "hypothesizing"  # Generating predictions
    TESTING = "testing"            # Running derivations
    VALIDATING = "validating"      # Verifying results
    ASSESSING = "assessing"        # HRM evaluation
    LEARNING = "learning"          # Updating training
    DEEPENING = "deepening"        # Generating questions
    CHECKPOINTING = "checkpointing"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"


@dataclass
class DaemonConfig:
    """Configuration for the daemon."""
    # Mode
    mode: DaemonMode = DaemonMode.CONTINUOUS
    duration_seconds: int = 0      # 0 = infinite for CONTINUOUS

    # Timing
    iteration_delay: int = 5       # Seconds between iterations
    checkpoint_interval: int = 300  # Seconds between checkpoints (5 min)

    # Thresholds
    min_hrm_for_training: float = 0.8
    halt_on_hecate_block: bool = True

    # Sources
    enable_web_fetch: bool = True
    enable_arxiv: bool = True
    enable_codata: bool = True

    # Learning
    auto_train_legomena: bool = False  # Auto-update Legomena
    training_batch_size: int = 100

    # Watchers
    enable_hecate: bool = True
    hecate_blocking: bool = True

    # Output
    output_dir: str = "daemon_outputs"
    checkpoint_file: str = "daemon_checkpoint.json"

    # Logging
    verbose: bool = True
    log_file: str = ""


@dataclass
class DaemonStats:
    """Statistics for daemon operation."""
    start_time: str = ""
    iterations: int = 0

    # Scientific method phases
    observations: int = 0
    hypotheses: int = 0
    tests: int = 0
    validations: int = 0

    # Results
    first_principles_found: int = 0
    derived_found: int = 0
    numerology_rejected: int = 0
    total_rejected: int = 0

    # Storage
    to_aletheia: int = 0
    to_mnemosyne: int = 0
    training_examples: int = 0

    # Hecate
    hecate_passes: int = 0
    hecate_warns: int = 0
    hecate_halts: int = 0

    # Timing
    total_runtime_seconds: float = 0
    avg_iteration_seconds: float = 0


class OlympusDaemon:
    """
    The 24/7 autonomous research daemon.

    Orchestrates continuous research using the scientific method:
    observe → hypothesize → test → validate → assess → learn → deepen
    """

    def __init__(self, config: DaemonConfig = None):
        self.config = config or DaemonConfig()
        self.state = DaemonState.INITIALIZING
        self.stats = DaemonStats(start_time=datetime.now().isoformat())

        # Components (lazy loaded)
        self._pipeline = None
        self._honest_pipeline = None
        self._queue = None
        self._hecate = None
        self._mnemosyne = None
        self._aletheia = None
        self._cyllene = None

        # Control
        self.running = False
        self.paused = False
        self._stop_requested = False

        # Callbacks
        self.on_iteration_complete: Optional[Callable] = None
        self.on_discovery: Optional[Callable] = None
        self.on_halt: Optional[Callable] = None

        # Output
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging."""
        self.log_file = None
        if self.config.log_file:
            self.log_file = open(self.config.log_file, 'a')

    def _log(self, msg: str, level: str = "INFO"):
        """Log a message."""
        if self.config.verbose:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_msg = f"[OlympusDaemon {ts}] [{level}] {msg}"
            print(log_msg)
            if self.log_file:
                self.log_file.write(log_msg + "\n")
                self.log_file.flush()

    # =========================================================================
    # COMPONENT LOADING
    # =========================================================================

    def _load_components(self):
        """Lazy load all components."""
        self._log("Loading components...")

        # Pipeline
        try:
            from OlympusFlow.derivation_pipeline import DerivationPipeline
            self._pipeline = DerivationPipeline(
                output_dir=str(self.output_dir / "derivations"),
                verbose=self.config.verbose
            )
            self._log("✓ DerivationPipeline loaded")
        except ImportError as e:
            self._log(f"⚠ DerivationPipeline not available: {e}", "WARN")

        # Honest Pipeline
        try:
            from OlympusFlow.honest_pipeline import HonestPipeline
            self._honest_pipeline = HonestPipeline(
                output_dir=str(self.output_dir / "honest"),
                verbose=self.config.verbose
            )
            self._log("✓ HonestPipeline loaded")
        except ImportError as e:
            self._log(f"⚠ HonestPipeline not available: {e}", "WARN")

        # Queue
        try:
            from OlympusFlow.flows.alpheus import ResearchQueue
            self._queue = ResearchQueue(
                persistence_path=str(self.output_dir / "queue_state.json")
            )
            self._log(f"✓ ResearchQueue loaded ({len(self._queue.tasks)} tasks)")
        except ImportError as e:
            self._log(f"⚠ ResearchQueue not available: {e}", "WARN")

        # Hecate
        if self.config.enable_hecate:
            try:
                from OlympusFlow.watchers import HecateWatcher, WatcherConfig
                self._hecate = HecateWatcher(WatcherConfig(
                    blocking_mode=self.config.hecate_blocking,
                    verbose=self.config.verbose
                ))
                self._log("✓ Hecate watcher loaded")
            except ImportError as e:
                self._log(f"⚠ Hecate not available: {e}", "WARN")

        # Lakes
        try:
            from OlympusFlow.lakes.mnemosyne import MnemosyneLake
            self._mnemosyne = MnemosyneLake(persist=True)
            self._log("✓ MnemosyneLake loaded")
        except ImportError as e:
            self._log(f"⚠ MnemosyneLake not available: {e}", "WARN")

        try:
            from OlympusFlow.lakes.aletheia import AletheiaLake
            self._aletheia = AletheiaLake()
            self._log(f"✓ AletheiaLake loaded ({len(self._aletheia.get_all_truths())} truths)")
        except ImportError as e:
            self._log(f"⚠ AletheiaLake not available: {e}", "WARN")

        # Cyllene (learning)
        try:
            from OlympusFlow.flows.cyllene import Deepener
            self._cyllene = Deepener(verbose=self.config.verbose)
            self._log("✓ Cyllene deepener loaded")
        except ImportError as e:
            self._log(f"⚠ Cyllene not available: {e}", "WARN")

    # =========================================================================
    # MAIN LOOP
    # =========================================================================

    def run(self):
        """
        Main daemon loop.

        Implements the scientific method:
        observe → hypothesize → test → validate → assess → learn → deepen
        """
        self._log("=" * 70)
        self._log("OLYMPUSFLOW DAEMON STARTING")
        self._log(f"Mode: {self.config.mode.value}")
        self._log("=" * 70)

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        # Load components
        self._load_components()

        # Start
        self.running = True
        self.state = DaemonState.IDLE
        start_time = time.time()
        last_checkpoint = time.time()

        try:
            while self.running and not self._stop_requested:
                iteration_start = time.time()

                # Check duration limit
                if self.config.mode == DaemonMode.TIMED:
                    elapsed = time.time() - start_time
                    if elapsed >= self.config.duration_seconds:
                        self._log(f"Duration limit reached ({self.config.duration_seconds}s)")
                        break

                # Check if paused
                if self.paused:
                    self.state = DaemonState.PAUSED
                    time.sleep(1)
                    continue

                # Run one iteration of the scientific method
                self._run_iteration()

                # Checkpoint if needed
                if time.time() - last_checkpoint >= self.config.checkpoint_interval:
                    self._checkpoint()
                    last_checkpoint = time.time()

                # Update stats
                self.stats.iterations += 1
                iteration_time = time.time() - iteration_start
                self.stats.total_runtime_seconds = time.time() - start_time
                self.stats.avg_iteration_seconds = (
                    self.stats.total_runtime_seconds / self.stats.iterations
                )

                # Callback
                if self.on_iteration_complete:
                    self.on_iteration_complete(self.stats)

                # Delay between iterations
                if self.config.iteration_delay > 0:
                    time.sleep(self.config.iteration_delay)

                # Single mode - stop after one iteration
                if self.config.mode == DaemonMode.SINGLE:
                    break

                # Batch mode - stop when queue is empty
                if self.config.mode == DaemonMode.BATCH:
                    if self._queue and not self._queue.get_next():
                        self._log("Queue empty, batch complete")
                        break

        except Exception as e:
            self._log(f"Daemon error: {e}", "ERROR")
            raise

        finally:
            self._shutdown()

    def _run_iteration(self):
        """Run one iteration of the scientific method loop."""
        self._log(f"\n--- Iteration {self.stats.iterations + 1} ---")

        # 1. OBSERVE: Get next task or generate one
        self.state = DaemonState.OBSERVING
        task = self._observe()
        if not task:
            self._log("No tasks available, idle...")
            return

        self._log(f"Task: {task.get('name', task.get('constant_name', 'unknown'))}")

        # 2. HYPOTHESIZE: (handled by derivation engine)
        self.state = DaemonState.HYPOTHESIZING
        self.stats.hypotheses += 1

        # 3. TEST: Run derivation
        self.state = DaemonState.TESTING
        result = self._test(task)
        self.stats.tests += 1

        if not result:
            self._log("No result from test phase")
            return

        # 4. VALIDATE: Check result
        self.state = DaemonState.VALIDATING
        validated = self._validate(result)
        self.stats.validations += 1

        # 5. ASSESS: Hecate oversight
        self.state = DaemonState.ASSESSING
        assessment = self._assess(result, validated)

        # Handle Hecate halt
        if assessment and not assessment.get("allow_continue", True):
            self._log("Hecate HALTED this result", "WARN")
            self.stats.hecate_halts += 1
            if self.config.halt_on_hecate_block:
                if self.on_halt:
                    self.on_halt(result, assessment)
                return

        # 6. LEARN: Store and export
        self.state = DaemonState.LEARNING
        self._learn(result, validated)

        # 7. DEEPEN: Generate follow-up questions
        self.state = DaemonState.DEEPENING
        self._deepen(result)

        self.state = DaemonState.IDLE

    # =========================================================================
    # SCIENTIFIC METHOD PHASES
    # =========================================================================

    def _observe(self) -> Optional[Dict]:
        """
        OBSERVE phase: Get the next task to process.

        Sources:
        1. AlpheusFlow queue (priority tasks)
        2. Cyllene deepening questions
        3. Auto-generated from gaps in AletheiaLake
        """
        # Try queue first
        if self._queue:
            task = self._queue.get_next()
            if task:
                self.stats.observations += 1
                return {
                    "constant_name": task.name,
                    "target_value": task.target_value,
                    "domain": task.domain,
                    "assignment": task.description
                }

        # TODO: Generate from gaps in AletheiaLake
        # TODO: Pull from Cyllene deepening questions

        return None

    def _test(self, task: Dict) -> Optional[Dict]:
        """
        TEST phase: Run the derivation pipeline.
        """
        if not self._pipeline:
            self._log("No pipeline available", "WARN")
            return None

        try:
            from OlympusFlow.derivation_pipeline import DerivationTask

            deriv_task = DerivationTask(
                constant_name=task.get("constant_name", ""),
                target_value=task.get("target_value", 0.0),
                domain=task.get("domain", "physics"),
                assignment=task.get("assignment", "")
            )

            result = self._pipeline.run(deriv_task)

            # Extract key info
            return {
                "task": task,
                "result": result,
                "level": result.verified.chain.level.value if result.verified else "failed",
                "formula": result.verified.chain.final_formula if result.verified else "",
                "hrm_score": result.verified.hrm_score if result.verified else 0.0,
                "stored_to": result.stored_to
            }

        except Exception as e:
            self._log(f"Test phase error: {e}", "ERROR")
            return None

    def _validate(self, result: Dict) -> bool:
        """
        VALIDATE phase: Check result against AletheiaLake.
        """
        level = result.get("level", "")
        hrm = result.get("hrm_score", 0.0)

        # Update stats
        if level == "first_principles":
            self.stats.first_principles_found += 1
            return True
        elif level == "derived":
            self.stats.derived_found += 1
            return hrm >= 0.7
        elif level == "numerical_match":
            self.stats.numerology_rejected += 1
            return False
        else:
            self.stats.total_rejected += 1
            return False

    def _assess(self, result: Dict, validated: bool) -> Optional[Dict]:
        """
        ASSESS phase: Run Hecate oversight.
        """
        if not self._hecate:
            return {"allow_continue": True}

        try:
            from OlympusFlow.watchers import StageTransition

            transition = StageTransition(
                source_stage="derivation",
                source_agent="DerivationPipeline",
                target_stage="storage",
                target_storage="mnemosyne" if validated else "rejected",
                result_type="derivation",
                result_data=result,
                pipeline_id="daemon",
                task_id=result.get("task", {}).get("constant_name", "unknown"),
                hrm_score=result.get("hrm_score", 0.0)
            )

            watcher_result = self._hecate.watch(transition)

            # Update stats
            if watcher_result.intervention.value == "pass":
                self.stats.hecate_passes += 1
            elif watcher_result.intervention.value == "warn":
                self.stats.hecate_warns += 1
            elif watcher_result.intervention.value == "halt":
                self.stats.hecate_halts += 1

            return {
                "allow_continue": watcher_result.allow_continue,
                "intervention": watcher_result.intervention.value,
                "note": watcher_result.note.to_dict()
            }

        except Exception as e:
            self._log(f"Assessment error: {e}", "WARN")
            return {"allow_continue": True}

    def _learn(self, result: Dict, validated: bool):
        """
        LEARN phase: Store result and export training data.
        """
        stored_to = result.get("stored_to", "")

        if stored_to == "aletheia":
            self.stats.to_aletheia += 1
        elif stored_to == "mnemosyne":
            self.stats.to_mnemosyne += 1

        # Export training data periodically
        if self._mnemosyne and self.stats.to_mnemosyne % 10 == 0:
            try:
                training = self._mnemosyne.graduate_to_training(
                    output_path=str(self.output_dir / "training_export.jsonl"),
                    min_hrm=self.config.min_hrm_for_training
                )
                self.stats.training_examples = len(training)
                self._log(f"Exported {len(training)} training examples")
            except Exception as e:
                self._log(f"Training export error: {e}", "WARN")

    def _deepen(self, result: Dict):
        """
        DEEPEN phase: Generate follow-up research questions.
        """
        if not self._cyllene:
            return

        # Only deepen successful results
        level = result.get("level", "")
        if level not in ["first_principles", "derived"]:
            return

        # TODO: Generate research questions and add to queue
        # questions = self._cyllene.analyze_finding(result)
        # for q in questions:
        #     self._queue.add(convert_question_to_task(q))

    # =========================================================================
    # CONTROL
    # =========================================================================

    def pause(self):
        """Pause the daemon."""
        self.paused = True
        self._log("Daemon PAUSED")

    def resume(self):
        """Resume the daemon."""
        self.paused = False
        self._log("Daemon RESUMED")

    def stop(self):
        """Request daemon stop."""
        self._stop_requested = True
        self._log("Stop requested...")

    def _handle_signal(self, signum, frame):
        """Handle OS signals."""
        self._log(f"Received signal {signum}")
        self.stop()

    def _shutdown(self):
        """Graceful shutdown."""
        self.state = DaemonState.STOPPING
        self._log("Shutting down...")

        # Final checkpoint
        self._checkpoint()

        # Close resources
        if self.log_file:
            self.log_file.close()

        self.state = DaemonState.STOPPED
        self.running = False

        self._log("Daemon stopped")
        self._print_final_stats()

    def _checkpoint(self):
        """Save daemon state to disk."""
        self.state = DaemonState.CHECKPOINTING

        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "state": self.state.value,
            "stats": asdict(self.stats),
            "config": {
                "mode": self.config.mode.value,
                "duration": self.config.duration_seconds
            }
        }

        checkpoint_path = self.output_dir / self.config.checkpoint_file
        checkpoint_path.write_text(json.dumps(checkpoint, indent=2))
        self._log(f"Checkpoint saved to {checkpoint_path}")

    def _print_final_stats(self):
        """Print final statistics."""
        s = self.stats
        print("\n" + "=" * 70)
        print("OLYMPUSFLOW DAEMON - FINAL STATISTICS")
        print("=" * 70)
        print(f"Runtime: {s.total_runtime_seconds:.1f}s ({s.total_runtime_seconds/3600:.2f} hours)")
        print(f"Iterations: {s.iterations}")
        print(f"Avg iteration: {s.avg_iteration_seconds:.1f}s")
        print()
        print("Scientific Method:")
        print(f"  Observations: {s.observations}")
        print(f"  Hypotheses: {s.hypotheses}")
        print(f"  Tests: {s.tests}")
        print(f"  Validations: {s.validations}")
        print()
        print("Results:")
        print(f"  First-principles: {s.first_principles_found}")
        print(f"  Derived: {s.derived_found}")
        print(f"  Numerology rejected: {s.numerology_rejected}")
        print(f"  Total rejected: {s.total_rejected}")
        print()
        print("Storage:")
        print(f"  → AletheiaLake: {s.to_aletheia}")
        print(f"  → MnemosyneLake: {s.to_mnemosyne}")
        print(f"  Training examples: {s.training_examples}")
        print()
        print("Hecate Oversight:")
        print(f"  Passes: {s.hecate_passes}")
        print(f"  Warnings: {s.hecate_warns}")
        print(f"  Halts: {s.hecate_halts}")
        print("=" * 70)


# =============================================================================
# CLI
# =============================================================================

def main():
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="OlympusFlow Daemon - 24/7 Autonomous Research"
    )

    parser.add_argument(
        "--mode", "-m",
        choices=["continuous", "timed", "batch", "single"],
        default="single",
        help="Operating mode"
    )

    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=0,
        help="Duration in seconds (for timed mode)"
    )

    parser.add_argument(
        "--output", "-o",
        default="daemon_outputs",
        help="Output directory"
    )

    parser.add_argument(
        "--no-hecate",
        action="store_true",
        help="Disable Hecate oversight"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run (no external API calls)"
    )

    args = parser.parse_args()

    # Build config
    config = DaemonConfig(
        mode=DaemonMode(args.mode),
        duration_seconds=args.duration,
        output_dir=args.output,
        enable_hecate=not args.no_hecate,
        verbose=args.verbose or True,
        enable_web_fetch=not args.dry_run
    )

    # Run daemon
    daemon = OlympusDaemon(config)
    daemon.run()


if __name__ == "__main__":
    main()
