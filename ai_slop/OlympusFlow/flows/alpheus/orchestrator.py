#!/usr/bin/env python3
"""
ALPHEUSFLOW ORCHESTRATOR - Queue Processing Engine
===================================================

Processes tasks from the queue through OlympusFlow/TruthFlow.

The orchestrator:
1. Pulls tasks from the queue in priority order
2. Configures OlympusFlow for each task
3. Runs the task
4. Records results
5. Moves to next task

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import time
import json
import signal
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from threading import Event

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .queue import (
    ResearchQueue, ResearchTask, TaskStatus,
    TaskPriority, BatchConfig, create_derivation_task
)

# Import OlympusFlow components
try:
    from OlympusFlow import Pipeline, PipelineConfig, Z2, Z, PHI
    from OlympusFlow.stages import (
        DiscoveryStage, AnalysisStage,
        VerificationStage, StorageStage
    )
    OLYMPUS_AVAILABLE = True
except ImportError:
    OLYMPUS_AVAILABLE = False
    print("Warning: OlympusFlow not available")

# TruthFlow is now used by OlympusFlow's DiscoveryStage for derivation tasks


@dataclass
class OrchestratorConfig:
    """Configuration for the orchestrator."""
    output_dir: str = "alpheus_outputs"
    max_task_time: int = 3600          # Max seconds per task
    pause_between_tasks: int = 5        # Seconds between tasks
    auto_save_interval: int = 60        # Save state every N seconds
    stop_on_consecutive_failures: int = 3  # Stop after N failures in a row
    verbose: bool = True


class AlpheusOrchestrator:
    """
    Main orchestrator that processes the research queue.

    Pulls tasks from ResearchQueue, runs them through OlympusFlow,
    and manages the overall research workflow.
    """

    def __init__(self, config: OrchestratorConfig = None):
        self.config = config or OrchestratorConfig()
        self.queue = ResearchQueue()
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # State
        self.running = False
        self.paused = False
        self.current_task: Optional[ResearchTask] = None
        self.consecutive_failures = 0
        self.tasks_completed = 0
        self.tasks_failed = 0

        # Stop event for graceful shutdown
        self.stop_event = Event()

        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # Callbacks
        self.queue.on_task_start = self._on_task_start
        self.queue.on_task_complete = self._on_task_complete
        self.queue.on_task_fail = self._on_task_fail

    def _log(self, msg: str):
        """Log message with timestamp."""
        if self.config.verbose:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[AlpheusFlow {timestamp}] {msg}")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self._log("Received shutdown signal, finishing current task...")
        self.stop_event.set()
        self.running = False

    def _on_task_start(self, task: ResearchTask):
        """Called when a task starts."""
        self._log(f"Starting task: {task.name} ({task.id})")

    def _on_task_complete(self, task: ResearchTask):
        """Called when a task completes."""
        self._log(f"Completed task: {task.name} in {task.elapsed_seconds:.1f}s")
        self.tasks_completed += 1
        self.consecutive_failures = 0

    def _on_task_fail(self, task: ResearchTask):
        """Called when a task fails."""
        self._log(f"Failed task: {task.name} - {task.error}")
        self.tasks_failed += 1
        self.consecutive_failures += 1

    def submit(self, task: ResearchTask) -> str:
        """Submit a task to the queue."""
        task_id = self.queue.add(task)
        self._log(f"Submitted task: {task.name} ({task_id})")
        return task_id

    def submit_derivation(self, target: str, target_value: float,
                          assignment: str, category: str = "derivation") -> str:
        """Submit a Z² constant derivation task."""
        task = create_derivation_task(target, target_value, assignment, category)
        return self.submit(task)

    def submit_batch(self, tasks: List[ResearchTask], category: str = None) -> List[str]:
        """Submit a batch of tasks."""
        ids = []
        for task in tasks:
            if category:
                task.category = category
            ids.append(self.submit(task))
        self._log(f"Submitted batch of {len(ids)} tasks")
        return ids

    def run_task(self, task: ResearchTask) -> bool:
        """
        Run a single task through the appropriate engine.

        Returns True if successful, False if failed.
        """
        self.current_task = task
        task_output_dir = self.output_dir / task.category / task.id
        task_output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # ALL tasks go through OlympusFlow research pipeline
            # AlpheusFlow is purely the queue manager
            # OlympusFlow stages handle all processing (discovery, analysis, verification, storage)
            result = self._run_research_task(task, task_output_dir)

            # Record result
            self.queue.complete_task(
                task.id,
                result=result,
                output_path=str(task_output_dir)
            )
            return True

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            self._log(f"Task error: {error_msg}")
            traceback.print_exc()

            self.queue.fail_task(task.id, error_msg)
            return False

        finally:
            self.current_task = None

    def _run_research_task(self, task: ResearchTask,
                           output_dir: Path) -> Dict:
        """
        Run a task through OlympusFlow.

        Handles both:
        - Data discovery tasks (search web for data)
        - Derivation tasks (find Z² formula matches when target_constant is set)
        """
        is_derivation = bool(task.target_constant and task.target_value)
        task_type = "derivation" if is_derivation else "research"
        self._log(f"Running {task_type}: {task.name}")

        result = {
            'task_id': task.id,
            'topic': task.description,
            'domain': task.domain,
            'task_type': task_type,
            'status': 'attempted'
        }

        if is_derivation:
            result['target_constant'] = task.target_constant
            result['target_value'] = task.target_value

        if OLYMPUS_AVAILABLE:
            config = PipelineConfig(
                name=task.name,
                topic=task.description,
                domain=task.domain or "unknown",
                quantities=task.quantities or [task.target_constant] if task.target_constant else [],
                max_iterations=3 if not is_derivation else 1,  # Derivations only need 1 iteration
                verbose=True,
                # Z² derivation parameters (v1.5.0)
                target_constant=task.target_constant,
                target_value=task.target_value,
                is_derivation=is_derivation
            )

            pipeline = Pipeline(task.name, config, output_dir=output_dir)

            # DiscoveryStage now handles both data discovery AND derivation
            pipeline.add_stage(DiscoveryStage(
                topic=task.description,
                domain=task.domain or "unknown",
                quantities=task.quantities or [],
                # Pass derivation parameters to stage
                target_constant=task.target_constant,
                target_value=task.target_value
            ))
            pipeline.add_stage(AnalysisStage())
            pipeline.add_stage(VerificationStage())
            pipeline.add_stage(StorageStage())

            pipeline_result = pipeline.run(max_iterations=config.max_iterations)
            result['pipeline_result'] = pipeline_result
            result['status'] = 'completed'
        else:
            result['status'] = 'skipped'
            result['error'] = 'OlympusFlow not available'

        # Save result
        result_file = output_dir / "result.json"
        result_file.write_text(json.dumps(result, indent=2, default=str))

        return result

    def run(self, max_tasks: int = None):
        """
        Run the queue until empty or max_tasks reached.

        This is the main loop that processes tasks sequentially.
        """
        self.running = True
        self.paused = False
        tasks_processed = 0

        self._log(f"Starting queue processing ({self.queue.get_pending_count()} pending)")

        while self.running and not self.stop_event.is_set():
            # Check for pause
            while self.paused and self.running:
                time.sleep(1)

            # Check for too many consecutive failures
            if self.consecutive_failures >= self.config.stop_on_consecutive_failures:
                self._log(f"Stopping: {self.consecutive_failures} consecutive failures")
                break

            # Check max tasks
            if max_tasks and tasks_processed >= max_tasks:
                self._log(f"Reached max tasks limit ({max_tasks})")
                break

            # Get next task
            task = self.queue.pop_next()
            if not task:
                self._log("Queue empty, stopping")
                break

            # Run the task
            self.run_task(task)
            tasks_processed += 1

            # Pause between tasks
            if self.config.pause_between_tasks > 0:
                time.sleep(self.config.pause_between_tasks)

        self.running = False
        self._log(f"Queue processing complete: {tasks_processed} tasks processed")

        return {
            'tasks_processed': tasks_processed,
            'completed': self.tasks_completed,
            'failed': self.tasks_failed,
            'remaining': self.queue.get_pending_count()
        }

    def pause(self):
        """Pause queue processing."""
        self.paused = True
        self._log("Queue paused")

    def resume(self):
        """Resume queue processing."""
        self.paused = False
        self._log("Queue resumed")

    def stop(self):
        """Stop queue processing."""
        self.running = False
        self.stop_event.set()
        self._log("Queue stopped")

    def get_status(self) -> Dict:
        """Get current orchestrator status."""
        return {
            'running': self.running,
            'paused': self.paused,
            'current_task': self.current_task.name if self.current_task else None,
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'consecutive_failures': self.consecutive_failures,
            'queue_stats': self.queue.get_statistics()
        }


# =============================================================================
# GLOBAL ORCHESTRATOR INSTANCE
# =============================================================================

_orchestrator: Optional[AlpheusOrchestrator] = None


def get_orchestrator() -> AlpheusOrchestrator:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AlpheusOrchestrator()
    return _orchestrator


def submit_task(description: str, domain: str = "physics",
                category: str = "research", priority: TaskPriority = TaskPriority.NORMAL) -> str:
    """Submit a task to the global queue."""
    task = ResearchTask(
        id="",
        name=description[:50].lower().replace(" ", "_"),
        description=description,
        domain=domain,
        category=category,
        priority=priority
    )
    return get_orchestrator().submit(task)


def run_queue(max_tasks: int = None) -> Dict:
    """Run the global queue."""
    return get_orchestrator().run(max_tasks)


def get_queue_status() -> Dict:
    """Get status of the global queue."""
    return get_orchestrator().get_status()


def pause_queue():
    """Pause the global queue."""
    get_orchestrator().pause()


def resume_queue():
    """Resume the global queue."""
    get_orchestrator().resume()


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AlpheusFlow Queue Orchestrator")
    parser.add_argument("--run", action="store_true", help="Run the queue")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    parser.add_argument("--submit", type=str, help="Submit a task")
    parser.add_argument("--max", type=int, help="Max tasks to process")

    args = parser.parse_args()

    orchestrator = get_orchestrator()

    if args.status:
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))

    elif args.submit:
        task_id = submit_task(args.submit)
        print(f"Submitted: {task_id}")

    elif args.run:
        result = orchestrator.run(max_tasks=args.max)
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()
