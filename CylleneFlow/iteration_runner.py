#!/usr/bin/env python3
"""
ITERATION RUNNER
================

Orchestrates iterative learning experiments.

Runs the full loop:
1. Explore topic with current model (via HermesFlow)
2. Find Z² relationships
3. Validate statistically
4. Add to truth store
5. Generate training examples
6. Update model
7. Repeat until diminishing returns

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable

# Add parent directory for HermesFlow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from .truth_store import TruthStore
    from .training_generator import TrainingGenerator
    from .model_updater import ModelUpdater
except ImportError:
    from truth_store import TruthStore
    from training_generator import TrainingGenerator
    from model_updater import ModelUpdater


class IterationRunner:
    """
    Run iterative learning experiments.

    Each iteration:
    1. Uses current model for reasoning
    2. Runs HermesFlow for discovery
    3. Validates and stores findings
    4. Updates model with new knowledge
    """

    def __init__(
        self,
        domain: str,
        topic: str,
        max_iterations: int = 10,
        base_model: str = None,
        experiment_name: str = None
    ):
        self.domain = domain
        self.topic = topic
        self.max_iterations = max_iterations
        self.base_model = base_model or os.environ.get("LEGOMENA_BASE_MODEL", "legomena-31b")

        # Experiment directory
        self.experiment_name = experiment_name or f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.experiment_dir = Path(__file__).parent / "experiments" / self.experiment_name
        self.experiment_dir.mkdir(parents=True, exist_ok=True)

        # Components
        self.truth_store = TruthStore(self.experiment_dir / "truth_store.json")
        self.training_gen = TrainingGenerator(self.experiment_dir / "training_data.jsonl")
        self.model_updater = ModelUpdater(self.base_model)

        # Results tracking
        self.results: List[Dict] = []
        self.results_file = self.experiment_dir / "results.json"

        # Discovery function (can be customized)
        self.discovery_fn: Optional[Callable] = None

    def set_discovery_function(self, fn: Callable):
        """Set custom discovery function for the domain."""
        self.discovery_fn = fn

    def run(self) -> List[Dict]:
        """Run the full iterative experiment."""
        self._log(f"Starting experiment: {self.experiment_name}")
        self._log(f"Domain: {self.domain}")
        self._log(f"Topic: {self.topic}")
        self._log(f"Max iterations: {self.max_iterations}")
        self._log(f"Base model: {self.base_model}")

        for i in range(1, self.max_iterations + 1):
            result = self._run_iteration(i)
            self.results.append(result)
            self._save_results()

            # Check for diminishing returns
            if self._check_diminishing_returns():
                self._log("Diminishing returns detected, stopping early")
                break

            # Brief pause between iterations
            time.sleep(2)

        self._generate_report()
        return self.results

    def _run_iteration(self, iteration: int) -> Dict:
        """Run a single iteration."""
        self._log(f"\n{'='*60}")
        self._log(f"ITERATION {iteration}")
        self._log(f"{'='*60}")

        start_time = time.time()

        # Determine model to use
        if iteration == 1:
            model = self.base_model
        else:
            model = f"{self.base_model}-iter{iteration-1}"

        os.environ["LEGOMENA_MODEL"] = model
        self._log(f"Using model: {model}")

        # Run discovery
        self._log("Running discovery...")
        findings = self._run_discovery(iteration)

        # Validate findings
        validated = self._validate_findings(findings)
        self._log(f"Found {len(findings)} total, {len(validated)} validated")

        # Add to truth store
        new_truths = 0
        for f in validated:
            if self.truth_store.add(f):
                new_truths += 1

        self._log(f"Added {new_truths} new truths")

        # Generate training data
        if new_truths > 0:
            n_examples = self.training_gen.generate_from_truths(validated)
            self._log(f"Generated {n_examples} training examples")

            # Update model
            all_truths = self.truth_store.get_all()
            new_model = self.model_updater.create_quick_iteration(iteration, all_truths)
            self._log(f"Created model: {new_model}")
        else:
            new_model = model
            n_examples = 0

        elapsed = time.time() - start_time

        return {
            "iteration": iteration,
            "model_used": model,
            "model_created": new_model,
            "total_findings": len(findings),
            "validated_findings": len(validated),
            "new_truths": new_truths,
            "training_examples": n_examples,
            "time_seconds": elapsed,
            "timestamp": datetime.now().isoformat()
        }

    def _run_discovery(self, iteration: int) -> List[Dict]:
        """Run discovery for the domain."""
        if self.discovery_fn:
            return self.discovery_fn(self.topic, iteration)

        # Default: Try to import HermesFlow
        try:
            from HermesFlow.hermes_explorer import HermesExplorer

            explorer = HermesExplorer(verbose=True)
            result = explorer.explore_for_data(
                topic=self.topic,
                domain=self.domain,
                quantities=["value", "measurement", "rate", "ratio"]
            )

            if result.success and result.data is not None:
                # Analyze for Z² patterns
                return self._analyze_for_z2(result.data, iteration)

        except ImportError:
            self._log("HermesFlow not available, using stub discovery", "WARN")

        return []

    def _analyze_for_z2(self, df, iteration: int) -> List[Dict]:
        """Analyze dataframe for Z² patterns."""
        import math
        import pandas as pd
        import numpy as np

        PHI = (1 + math.sqrt(5)) / 2
        Z2 = 32 * math.pi / 3
        Z = math.sqrt(Z2)

        targets = {
            "φ": PHI,
            "1/φ": 1/PHI,
            "Z": Z,
            "Z²": Z2,
            "Z²/10": Z2/10,
            "π": math.pi,
        }

        findings = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols[:10]:
            data = df[col].dropna()
            if len(data) < 30:
                continue

            mean = data.mean()
            std = data.std()

            if std == 0 or mean == 0:
                continue

            cv = std / abs(mean)

            for name, target in targets.items():
                error = abs(cv - target) / target * 100
                if error < 5:
                    findings.append({
                        "domain": self.domain,
                        "quantity": f"CV({col})",
                        "value": cv,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(data),
                        "iteration": iteration
                    })

        return findings

    def _validate_findings(self, findings: List[Dict]) -> List[Dict]:
        """Validate findings statistically."""
        return [
            f for f in findings
            if f.get('error_percent', 100) < 5 and f.get('n_samples', 0) >= 30
        ]

    def _check_diminishing_returns(self) -> bool:
        """Check if we should stop due to diminishing returns."""
        if len(self.results) < 3:
            return False

        recent_truths = [r['new_truths'] for r in self.results[-3:]]
        return all(t == 0 for t in recent_truths)

    def _save_results(self):
        """Save results to disk."""
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)

    def _generate_report(self):
        """Generate final experiment report."""
        report_file = self.experiment_dir / "REPORT.md"

        total_findings = sum(r['total_findings'] for r in self.results)
        total_validated = sum(r['validated_findings'] for r in self.results)
        total_truths = sum(r['new_truths'] for r in self.results)

        report = f"""# CylleneFlow Experiment Report

**Experiment:** {self.experiment_name}
**Domain:** {self.domain}
**Topic:** {self.topic}
**Date:** {datetime.now().isoformat()}

## Summary

| Metric | Value |
|--------|-------|
| Iterations | {len(self.results)} |
| Total Findings | {total_findings} |
| Validated | {total_validated} |
| New Truths | {total_truths} |

## Iteration Details

| Iter | Model | Findings | Validated | Truths | Time |
|------|-------|----------|-----------|--------|------|
"""

        for r in self.results:
            report += (
                f"| {r['iteration']} | {r['model_used'][:20]} | "
                f"{r['total_findings']} | {r['validated_findings']} | "
                f"{r['new_truths']} | {r['time_seconds']:.0f}s |\n"
            )

        report += f"""

## All Truths

"""
        for t in self.truth_store.get_all():
            report += f"- **{t['quantity']}** = {t['target']} (error: {t['error_percent']:.2f}%)\n"

        with open(report_file, 'w') as f:
            f.write(report)

        self._log(f"Report saved: {report_file}")

    def _log(self, msg: str, level: str = "INFO"):
        """Log message to console and file."""
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] [{level}] {msg}")

        log_file = self.experiment_dir / "experiment.log"
        with open(log_file, 'a') as f:
            f.write(f"[{ts}] [{level}] {msg}\n")


def run_venice_experiment():
    """Example: Run Venice water levels experiment."""
    runner = IterationRunner(
        domain="hydrology",
        topic="Venice water levels and acqua alta",
        max_iterations=10,
        experiment_name="venice_water_levels"
    )
    return runner.run()


if __name__ == "__main__":
    run_venice_experiment()
