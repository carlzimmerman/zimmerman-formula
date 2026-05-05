#!/usr/bin/env python3
"""
OLYMPUSFLOW - Pipeline Orchestrator
====================================

The unified orchestrator that ties all components together.

Features:
- Declarative pipeline definition
- Automatic state management
- Event emission for monitoring
- Iteration support for learning loops
- Persistence for resumability

Usage:
    pipeline = Pipeline(
        name="earthquake_research",
        config=PipelineConfig(
            topic="USGS earthquake data",
            domain="seismology",
            quantities=["magnitude", "depth"]
        )
    )

    pipeline.add_stage(DiscoveryStage(...))
    pipeline.add_stage(AnalysisStage(...))
    pipeline.add_stage(VerificationStage(...))
    pipeline.add_stage(StorageStage(...))

    results = pipeline.run(max_iterations=10)

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent.parent))

from .contracts import (
    PipelineConfig, PipelineState, StageResult,
    ResearchPhase, Discovery
)
from .events import (
    EventBus, EventType, EventEmitter,
    ConsoleLogger, MetricsCollector, get_event_bus, set_event_bus
)
from .stages import (
    Stage, DiscoveryStage, AnalysisStage,
    VerificationStage, StorageStage, TrainingStage
)


# =============================================================================
# PIPELINE
# =============================================================================

class Pipeline(EventEmitter):
    """
    Main pipeline orchestrator for Z² research.

    Coordinates:
    - HermesFlow (discovery)
    - Analysis (pattern finding)
    - TruthFlow (verification)
    - MnemosyneLake (storage)
    - Legomena (training)
    """

    def __init__(self, name: str, config: PipelineConfig,
                 output_dir: Optional[Path] = None):
        """
        Initialize pipeline.

        Args:
            name: Pipeline name
            config: Pipeline configuration
            output_dir: Directory for outputs (default: ./olympus_outputs/{name})
        """
        # Set up event bus first
        self._event_bus = EventBus()
        set_event_bus(self._event_bus)
        super().__init__(self._event_bus)

        self.name = name
        self.config = config
        self._stage_name = "OlympusFlow"

        # Output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent.parent / "olympus_outputs" / name
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set up event logging
        self._event_bus._log_path = self.output_dir / "events.jsonl"

        # Pipeline state
        self.state = PipelineState(
            pipeline_id=PipelineState.generate_id(name),
            config=config.to_dict()
        )

        # Stages
        self.stages: List[Stage] = []

        # Monitoring
        self.logger = ConsoleLogger(verbose=config.verbose)
        self.metrics = MetricsCollector()
        self._event_bus.subscribe("*", self.logger)
        self._event_bus.subscribe("*", self.metrics)

        # Callbacks
        self._on_iteration_complete: List[Callable] = []
        self._on_truth_found: List[Callable] = []

    def add_stage(self, stage: Stage) -> "Pipeline":
        """Add a stage to the pipeline. Returns self for chaining."""
        self.stages.append(stage)
        return self

    def on_iteration_complete(self, callback: Callable) -> "Pipeline":
        """Register callback for iteration completion."""
        self._on_iteration_complete.append(callback)
        return self

    def on_truth_found(self, callback: Callable) -> "Pipeline":
        """Register callback for when a truth is found."""
        self._on_truth_found.append(callback)
        return self

    def run(self, max_iterations: int = None) -> Dict:
        """
        Run the pipeline.

        Args:
            max_iterations: Override config max_iterations

        Returns:
            Summary of pipeline run
        """
        iterations = max_iterations or self.config.max_iterations

        self.emit(EventType.PIPELINE_STARTED, {
            "name": self.name,
            "topic": self.config.topic,
            "domain": self.config.domain,
            "max_iterations": iterations
        })

        start_time = time.time()
        results = []

        for i in range(1, iterations + 1):
            self.state.current_iteration = i
            self.state.update()

            self.emit(EventType.ITERATION_STARTED, {
                "iteration": i,
                "truths_so_far": len(self.state.truths)
            })

            # Run all stages
            iteration_result = self._run_iteration(i)
            results.append(iteration_result)

            # Save state
            self._save_state()

            # Call iteration callbacks
            for callback in self._on_iteration_complete:
                try:
                    callback(i, iteration_result)
                except Exception as e:
                    print(f"Callback error: {e}")

            self.emit(EventType.ITERATION_COMPLETED, {
                "iteration": i,
                "new_truths": iteration_result.get("new_truths", 0)
            })

            # Check for diminishing returns
            if self._check_diminishing_returns(results):
                self.emit(EventType.DIMINISHING_RETURNS, {
                    "iteration": i,
                    "reason": "No new truths in last 3 iterations"
                })
                break

            # Brief pause between iterations
            if i < iterations:
                time.sleep(1)

        # Finalize
        total_time = time.time() - start_time
        self.state.current_phase = ResearchPhase.COMPLETE.value

        summary = self._generate_summary(results, total_time)

        self.emit(EventType.PIPELINE_COMPLETED, summary)

        # Save final report
        self._save_report(summary)

        return summary

    def _run_iteration(self, iteration: int) -> Dict:
        """Run a single iteration of all stages."""
        iteration_start = time.time()
        stage_results = []
        current_input = None
        new_truths = 0

        for stage in self.stages:
            self.emit(EventType.STAGE_STARTED, {
                "stage": stage.name,
                "iteration": iteration
            })

            # Run stage
            result = stage.run(current_input, self.state)
            stage_results.append(result)
            self.state.stage_results.append(result)

            if not result.success:
                # Stage failed - log and continue to next iteration
                break

            current_input = result.output

            # Track new truths
            if stage.name == "VerificationStage" and result.output:
                new_truths = len([t for t in result.output
                                 if t.status == "validated"])

                # Call truth callbacks
                for truth in result.output:
                    for callback in self._on_truth_found:
                        try:
                            callback(truth)
                        except Exception as e:
                            print(f"Truth callback error: {e}")

        return {
            "iteration": iteration,
            "stage_results": [r.to_dict() for r in stage_results],
            "new_truths": new_truths,
            "total_truths": len(self.state.truths),
            "duration": time.time() - iteration_start
        }

    def _check_diminishing_returns(self, results: List[Dict]) -> bool:
        """Check if we should stop due to no progress."""
        if len(results) < 3:
            return False

        recent_truths = [r.get("new_truths", 0) for r in results[-3:]]
        return all(t == 0 for t in recent_truths)

    def _save_state(self):
        """Save current state to disk."""
        state_file = self.output_dir / "state.json"
        with open(state_file, 'w') as f:
            json.dump(self.state.to_dict(), f, indent=2, default=str)

    def _generate_summary(self, results: List[Dict], total_time: float) -> Dict:
        """Generate pipeline summary."""
        return {
            "pipeline_id": self.state.pipeline_id,
            "name": self.name,
            "topic": self.config.topic,
            "domain": self.config.domain,
            "iterations": len(results),
            "total_discoveries": len(self.state.discoveries),
            "total_findings": len(self.state.findings),
            "total_truths": len(self.state.truths),
            "validated_truths": len([t for t in self.state.truths if t.status == "validated"]),
            "total_time_seconds": total_time,
            "metrics": self.metrics.get_summary()
        }

    def _save_report(self, summary: Dict):
        """Save final report."""
        # JSON summary
        summary_file = self.output_dir / "summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        # Markdown report
        report = self._generate_markdown_report(summary)
        report_file = self.output_dir / "REPORT.md"
        with open(report_file, 'w') as f:
            f.write(report)

    def _generate_markdown_report(self, summary: Dict) -> str:
        """Generate markdown report."""
        return f"""# OlympusFlow Pipeline Report

**Pipeline:** {summary['name']}
**ID:** {summary['pipeline_id']}
**Generated:** {datetime.now().isoformat()}

## Configuration

| Setting | Value |
|---------|-------|
| Topic | {self.config.topic} |
| Domain | {self.config.domain} |
| Quantities | {', '.join(self.config.quantities)} |
| Model | {self.config.model_name} |

## Summary

| Metric | Value |
|--------|-------|
| Iterations | {summary['iterations']} |
| Total Time | {summary['total_time_seconds']:.1f}s |
| Discoveries | {summary['total_discoveries']} |
| Findings | {summary['total_findings']} |
| Total Truths | {summary['total_truths']} |
| Validated Truths | {summary['validated_truths']} |

## Verified Truths

| Claim | HRM Score | Status |
|-------|-----------|--------|
""" + '\n'.join([
    f"| {t.claim[:50]} | {t.hrm_score:.2f} | {t.status} |"
    for t in self.state.truths
]) + f"""

## Event Metrics

| Event Type | Count |
|------------|-------|
""" + '\n'.join([
    f"| {k} | {v} |"
    for k, v in summary['metrics'].get('events_by_type', {}).items()
])

    @classmethod
    def create_default(cls, topic: str, domain: str,
                       quantities: List[str] = None,
                       model: str = "legomena-31b-clean") -> "Pipeline":
        """
        Create a pipeline with default stages.

        Args:
            topic: Research topic
            domain: Scientific domain
            quantities: Quantities to look for
            model: Legomena model to use

        Returns:
            Configured Pipeline instance
        """
        config = PipelineConfig(
            name=f"{domain}_research",
            topic=topic,
            domain=domain,
            quantities=quantities or ["value", "measurement"],
            model_name=model
        )

        pipeline = cls(f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}", config)

        # Add default stages
        pipeline.add_stage(DiscoveryStage(
            topic=topic,
            domain=domain,
            quantities=quantities or ["value", "measurement"],
            model=model
        ))
        pipeline.add_stage(AnalysisStage())
        pipeline.add_stage(VerificationStage())
        pipeline.add_stage(StorageStage())
        pipeline.add_stage(TrainingStage(output_path=pipeline.output_dir / "training.jsonl"))

        return pipeline


# =============================================================================
# QUICK BUILDERS
# =============================================================================

def research(topic: str, domain: str, quantities: List[str] = None,
             iterations: int = 5, model: str = "legomena-31b-clean") -> Dict:
    """
    Quick function to run research on a topic.

    Usage:
        results = research(
            topic="USGS earthquake magnitude data",
            domain="seismology",
            quantities=["magnitude", "depth"],
            iterations=5
        )
    """
    pipeline = Pipeline.create_default(topic, domain, quantities, model)
    return pipeline.run(max_iterations=iterations)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("OlympusFlow Pipeline Orchestrator")
    print("=" * 50)

    # Create a test pipeline
    config = PipelineConfig(
        name="test_pipeline",
        topic="Test scientific data",
        domain="test",
        quantities=["value", "rate"],
        max_iterations=2,
        verbose=True
    )

    pipeline = Pipeline("test_run", config)

    # Add minimal stages for testing
    pipeline.add_stage(AnalysisStage())
    pipeline.add_stage(VerificationStage())

    print(f"\nPipeline: {pipeline.name}")
    print(f"Output dir: {pipeline.output_dir}")
    print(f"Stages: {[s.name for s in pipeline.stages]}")

    # We won't actually run without real discovery data
    print("\nPipeline configured. Use pipeline.run() with DiscoveryStage for full execution.")
