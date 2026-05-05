#!/usr/bin/env python3
"""
TORNADO BLIND TEST - Full OlympusFlow Pipeline Analysis
========================================================

Tests whether OlympusFlow can discover Z² patterns in US tornado data
WITHOUT any pre-loaded tornado information in AletheiaLake.

This test captures detailed observability metrics at each pipeline stage
to identify opportunities for dynamic improvement.

Expected data sources:
- NOAA Storm Prediction Center
- NCEI tornado database
- Storm Events Database

Z² Framework predictions for severe weather:
- Energy ratios related to Z²/10 = 3.351
- Scale transitions at φ (golden ratio)
- CV patterns near Z = 5.789

Author: Carl Zimmerman
Date: May 5, 2026
"""

import sys
import os
import re
import math
import time
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Z² constants
Z2_SQUARED = 32 * math.pi / 3
Z = math.sqrt(Z2_SQUARED)
PHI = (1 + math.sqrt(5)) / 2


@dataclass
class PipelineObservation:
    """Captures observations at each pipeline stage for analysis."""
    stage: str
    timestamp: str
    duration_ms: float
    success: bool
    input_summary: str
    output_summary: str
    decision_points: List[Dict] = field(default_factory=list)
    potential_improvements: List[str] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)


class TornadoBlindTest:
    """
    Full pipeline test with observability for improvement analysis.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.observations: List[PipelineObservation] = []
        self.start_time = None
        self.test_dir = Path(__file__).parent.parent / "tests" / "tornado_blind_results"
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str, level: str = "INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        if self.verbose:
            print(f"[{ts}] [{level}] {msg}")

    def verify_blind_test(self) -> bool:
        """Ensure no tornado-related truths exist in AletheiaLake."""
        from AletheiaLake import AletheiaLake

        lake = AletheiaLake()
        all_truths = lake.get_all_truths()

        tornado_keywords = ['tornado', 'twister', 'supercell', 'funnel', 'ef_scale', 'fujita', 'severe_weather']

        for truth in all_truths:
            truth_text = f"{truth.name} {truth.claim} {truth.domain}".lower()
            for kw in tornado_keywords:
                if re.search(rf'\b{kw}\b', truth_text):
                    self.log(f"ERROR: Found tornado-related truth: {truth.name}", "ERROR")
                    return False

        return True

    def run_full_pipeline(self) -> Dict:
        """Run the complete OlympusFlow pipeline with observability."""

        self.log("=" * 70)
        self.log("TORNADO BLIND TEST - FULL OLYMPUSFLOW PIPELINE")
        self.log("=" * 70)
        self.log("")

        self.start_time = time.time()

        # Stage 0: Verify blind test conditions
        obs_blind = self._observe_stage("BlindVerification", self.verify_blind_test)
        if not obs_blind.success:
            return {"success": False, "reason": "Not a blind test - tornado data exists"}

        self.log("✓ Blind test verified - no tornado data in AletheiaLake")

        # Stage 1: HermesFlow Discovery
        obs_discovery = self._run_discovery_stage()

        if not obs_discovery.success:
            self.log("Discovery failed - generating analysis anyway", "WARN")

        # Stage 2: Analysis (Z² pattern finding)
        obs_analysis = self._run_analysis_stage(obs_discovery.metrics.get("data"))

        # Stage 3: Verification (would validate against ground truths)
        obs_verification = self._run_verification_stage(obs_analysis.metrics.get("findings", []))

        # Stage 4: Generate improvement report
        improvement_report = self._generate_improvement_report()

        # Save all observations
        self._save_observations()

        total_time = time.time() - self.start_time

        return {
            "success": obs_discovery.success,
            "total_time_seconds": total_time,
            "stages_completed": len(self.observations),
            "observations": [asdict(o) for o in self.observations],
            "improvement_report": improvement_report,
            "data_url": obs_discovery.metrics.get("url"),
            "data_shape": obs_discovery.metrics.get("shape"),
            "findings_count": len(obs_analysis.metrics.get("findings", [])),
            "z2_patterns": obs_analysis.metrics.get("z2_patterns", [])
        }

    def _observe_stage(self, stage_name: str, fn, *args, **kwargs) -> PipelineObservation:
        """Wrapper to observe a stage execution."""
        start = time.time()
        ts = datetime.now().isoformat()

        try:
            result = fn(*args, **kwargs)
            success = bool(result)
            output = str(result)[:200] if result else "None"
        except Exception as e:
            success = False
            output = f"Error: {e}"
            result = None

        duration = (time.time() - start) * 1000

        obs = PipelineObservation(
            stage=stage_name,
            timestamp=ts,
            duration_ms=duration,
            success=success,
            input_summary=str(args)[:100] if args else "None",
            output_summary=output
        )

        self.observations.append(obs)
        return obs

    def _run_discovery_stage(self) -> PipelineObservation:
        """Run HermesFlow discovery with detailed observation."""
        self.log("")
        self.log("--- Stage 1: HermesFlow Discovery ---")

        start = time.time()
        ts = datetime.now().isoformat()

        decision_points = []
        potential_improvements = []

        try:
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'HermesFlow'))
            from hermes_explorer import HermesExplorer

            explorer = HermesExplorer(verbose=True)

            # DECISION POINT 1: Topic formulation
            topic = "US tornado statistics EF scale intensity NOAA SPC storm prediction"
            decision_points.append({
                "point": "topic_formulation",
                "value": topic,
                "alternatives": [
                    "tornado frequency by state NOAA",
                    "severe weather statistics tornado damage",
                    "historical tornado data CSV download"
                ],
                "rationale": "Included multiple keywords for broader search"
            })

            # DECISION POINT 2: Domain selection
            domain = "meteorology"
            decision_points.append({
                "point": "domain_selection",
                "value": domain,
                "alternatives": ["severe_weather", "atmospheric_science"],
                "rationale": "Standard meteorology domain for tornado data"
            })

            # DECISION POINT 3: Quantities to search for
            quantities = ["count", "intensity", "ef_scale", "damage", "fatalities", "path_length"]
            decision_points.append({
                "point": "quantities",
                "value": quantities,
                "rationale": "Tornado-specific measurements that might show Z² patterns"
            })

            result = explorer.explore_for_data(
                topic=topic,
                domain=domain,
                quantities=quantities
            )

            success = result.success
            url = result.url if result.success else None
            data = result.data
            shape = tuple(data.shape) if data is not None else None
            columns = list(data.columns) if data is not None else []
            steps = len(result.steps)

            # Analyze decision points in the explorer's steps
            for step in result.steps:
                # Steps may be ExplorationStep objects or strings
                step_str = str(step) if not isinstance(step, str) else step
                if "search" in step_str.lower():
                    decision_points.append({
                        "point": "search_query",
                        "value": step_str[:100],
                        "stage": "discovery"
                    })
                elif "exploring" in step_str.lower():
                    decision_points.append({
                        "point": "portal_exploration",
                        "value": step_str[:100],
                        "stage": "discovery"
                    })

            # Identify potential improvements
            if not success:
                potential_improvements.append("CRITICAL: Discovery failed - need fallback strategies")
                potential_improvements.append("Consider: Pre-configured tornado data URLs (NOAA SPC known endpoints)")

            if steps > 10:
                potential_improvements.append(f"EFFICIENCY: {steps} steps taken - could optimize search ranking")

            self.log(f"Discovery {'SUCCESS' if success else 'FAILED'}")
            if success:
                self.log(f"  URL: {url}")
                self.log(f"  Shape: {shape}")
                self.log(f"  Columns: {columns[:5]}...")

        except Exception as e:
            success = False
            url = None
            data = None
            shape = None
            columns = []
            steps = 0
            potential_improvements.append(f"CRITICAL: Exception in discovery: {e}")
            self.log(f"Discovery ERROR: {e}", "ERROR")

        duration = (time.time() - start) * 1000

        obs = PipelineObservation(
            stage="HermesFlow_Discovery",
            timestamp=ts,
            duration_ms=duration,
            success=success,
            input_summary=f"topic={topic[:50]}, domain={domain}",
            output_summary=f"url={url}, shape={shape}",
            decision_points=decision_points,
            potential_improvements=potential_improvements,
            metrics={
                "url": url,
                "shape": shape,
                "columns": columns,
                "steps": steps,
                "data": data
            }
        )

        self.observations.append(obs)
        return obs

    def _run_analysis_stage(self, data) -> PipelineObservation:
        """Analyze discovered data for Z² patterns."""
        self.log("")
        self.log("--- Stage 2: Z² Pattern Analysis ---")

        start = time.time()
        ts = datetime.now().isoformat()

        findings = []
        z2_patterns = []
        decision_points = []
        potential_improvements = []

        if data is None:
            self.log("No data to analyze", "WARN")
            potential_improvements.append("CRITICAL: No data available for analysis")
        else:
            import pandas as pd
            import numpy as np

            # Z² targets
            targets = {
                "Z": Z,
                "Z²": Z2_SQUARED,
                "Z²/10": Z2_SQUARED / 10,
                "φ": PHI,
                "1/φ": 1 / PHI,
                "π": math.pi,
                "π/φ": math.pi / PHI,
            }

            numeric_cols = data.select_dtypes(include=[np.number]).columns
            self.log(f"Analyzing {len(numeric_cols)} numeric columns")

            for col in numeric_cols[:15]:
                col_data = data[col].dropna()
                if len(col_data) < 30:
                    continue

                mean = col_data.mean()
                std = col_data.std()

                if std == 0 or mean == 0:
                    continue

                cv = std / abs(mean)

                # Check CV against Z² targets
                for target_name, target_val in targets.items():
                    error = abs(cv - target_val) / target_val * 100
                    if error < 10:  # Within 10%
                        finding = {
                            "column": col,
                            "statistic": "CV",
                            "value": cv,
                            "target": target_name,
                            "target_value": target_val,
                            "error_percent": error,
                            "n_samples": len(col_data),
                            "mean": mean,
                            "std": std
                        }
                        findings.append(finding)

                        if error < 5:
                            z2_patterns.append(finding)
                            self.log(f"  Z² PATTERN: CV({col}) = {cv:.4f} ≈ {target_name} ({error:.2f}% error)")

                # Also check ratios between columns
                decision_points.append({
                    "point": "column_analysis",
                    "column": col,
                    "cv": cv,
                    "n_samples": len(col_data)
                })

            # Track analysis decisions
            if len(findings) == 0:
                potential_improvements.append("No Z² patterns found - consider different statistics (ratios, scaling)")
                potential_improvements.append("Could try: log transforms, running averages, cross-column ratios")

            if len(findings) > 10:
                potential_improvements.append("Many findings - may need stricter thresholds to avoid false positives")

        obs = PipelineObservation(
            stage="Z2_Analysis",
            timestamp=ts,
            duration_ms=(time.time() - start) * 1000,
            success=len(findings) > 0,
            input_summary=f"data shape: {data.shape if data is not None else 'None'}",
            output_summary=f"{len(findings)} findings, {len(z2_patterns)} strong patterns",
            decision_points=decision_points,
            potential_improvements=potential_improvements,
            metrics={
                "findings": findings,
                "z2_patterns": z2_patterns,
                "columns_analyzed": len(numeric_cols) if data is not None else 0
            }
        )

        self.observations.append(obs)
        return obs

    def _run_verification_stage(self, findings: List[Dict]) -> PipelineObservation:
        """Verify findings against statistical thresholds."""
        self.log("")
        self.log("--- Stage 3: Verification ---")

        start = time.time()
        ts = datetime.now().isoformat()

        validated = []
        rejected = []
        decision_points = []
        potential_improvements = []

        for f in findings:
            # Verification criteria
            passes_error = f.get('error_percent', 100) < 5
            passes_samples = f.get('n_samples', 0) >= 50
            passes_hrm = True  # Would compute HRM score here

            decision_points.append({
                "point": "validation",
                "finding": f.get("column"),
                "passes_error": passes_error,
                "passes_samples": passes_samples,
                "error": f.get('error_percent'),
                "samples": f.get('n_samples')
            })

            if passes_error and passes_samples:
                validated.append(f)
                self.log(f"  ✓ VALIDATED: {f.get('column')} → {f.get('target')}")
            else:
                rejected.append(f)

        if len(validated) == 0 and len(findings) > 0:
            potential_improvements.append("Findings exist but none validated - consider adjusting thresholds")

        obs = PipelineObservation(
            stage="Verification",
            timestamp=ts,
            duration_ms=(time.time() - start) * 1000,
            success=len(validated) > 0,
            input_summary=f"{len(findings)} findings to verify",
            output_summary=f"{len(validated)} validated, {len(rejected)} rejected",
            decision_points=decision_points,
            potential_improvements=potential_improvements,
            metrics={
                "validated": validated,
                "rejected": rejected
            }
        )

        self.observations.append(obs)
        return obs

    def _generate_improvement_report(self) -> Dict:
        """Generate comprehensive improvement report from observations."""

        all_improvements = []
        all_decisions = []
        stage_timings = {}

        for obs in self.observations:
            stage_timings[obs.stage] = obs.duration_ms
            all_improvements.extend(obs.potential_improvements)
            all_decisions.extend(obs.decision_points)

        # Categorize improvements
        critical = [i for i in all_improvements if "CRITICAL" in i]
        efficiency = [i for i in all_improvements if "EFFICIENCY" in i]
        enhancement = [i for i in all_improvements if i not in critical and i not in efficiency]

        # Identify bottlenecks
        total_time = sum(stage_timings.values())
        bottlenecks = [
            {"stage": stage, "time_ms": time, "percent": time/total_time*100}
            for stage, time in sorted(stage_timings.items(), key=lambda x: -x[1])
        ]

        return {
            "summary": {
                "total_stages": len(self.observations),
                "successful_stages": sum(1 for o in self.observations if o.success),
                "total_time_ms": total_time,
                "total_improvements_identified": len(all_improvements),
                "total_decision_points": len(all_decisions)
            },
            "critical_improvements": critical,
            "efficiency_improvements": efficiency,
            "enhancement_suggestions": enhancement,
            "bottlenecks": bottlenecks,
            "decision_analysis": all_decisions[:20]  # Top 20 decisions
        }

    def _save_observations(self):
        """Save observations to disk for later analysis."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Full observations
        obs_file = self.test_dir / f"observations_{ts}.json"
        with open(obs_file, 'w') as f:
            json.dump([asdict(o) for o in self.observations], f, indent=2, default=str)

        # Summary report
        report_file = self.test_dir / f"REPORT_{ts}.md"
        self._write_markdown_report(report_file)

        self.log(f"Observations saved to {self.test_dir}")

    def _write_markdown_report(self, path: Path):
        """Write markdown report."""
        total_time = time.time() - self.start_time if self.start_time else 0

        discovery_obs = next((o for o in self.observations if "Discovery" in o.stage), None)
        analysis_obs = next((o for o in self.observations if "Analysis" in o.stage), None)

        report = f"""# Tornado Blind Test Report

**Date:** {datetime.now().isoformat()}
**Total Time:** {total_time:.1f}s

## Z² Framework Reference

| Constant | Value |
|----------|-------|
| Z² | {Z2_SQUARED:.6f} |
| Z | {Z:.6f} |
| φ | {PHI:.6f} |

## Pipeline Execution

| Stage | Success | Duration |
|-------|---------|----------|
"""
        for obs in self.observations:
            report += f"| {obs.stage} | {'✓' if obs.success else '✗'} | {obs.duration_ms:.0f}ms |\n"

        if discovery_obs:
            report += f"""
## Discovery Results

- **URL:** {discovery_obs.metrics.get('url', 'None')}
- **Shape:** {discovery_obs.metrics.get('shape', 'None')}
- **Columns:** {discovery_obs.metrics.get('columns', [])[:5]}
- **Steps:** {discovery_obs.metrics.get('steps', 0)}
"""

        if analysis_obs:
            patterns = analysis_obs.metrics.get('z2_patterns', [])
            report += f"""
## Z² Patterns Found

| Column | Statistic | Value | Target | Error |
|--------|-----------|-------|--------|-------|
"""
            for p in patterns:
                report += f"| {p.get('column', '')} | {p.get('statistic', '')} | {p.get('value', 0):.4f} | {p.get('target', '')} | {p.get('error_percent', 0):.2f}% |\n"

        # Improvements section
        all_improvements = []
        for obs in self.observations:
            all_improvements.extend(obs.potential_improvements)

        if all_improvements:
            report += f"""
## Identified Improvements

"""
            for i, imp in enumerate(all_improvements, 1):
                report += f"{i}. {imp}\n"

        # Decision points
        report += f"""
## Key Decision Points

"""
        for obs in self.observations:
            for dp in obs.decision_points[:3]:
                report += f"- **{dp.get('point', '')}**: {dp.get('value', '')[:50] if isinstance(dp.get('value'), str) else dp.get('value')}\n"

        with open(path, 'w') as f:
            f.write(report)


def run_tornado_blind_test():
    """Run the full tornado blind test."""
    test = TornadoBlindTest(verbose=True)
    results = test.run_full_pipeline()

    print()
    print("=" * 70)
    print("TORNADO BLIND TEST COMPLETE")
    print("=" * 70)
    print(f"Success: {results['success']}")
    print(f"Time: {results['total_time_seconds']:.1f}s")
    print(f"Findings: {results['findings_count']}")
    print(f"Z² Patterns: {len(results['z2_patterns'])}")
    print()

    if results['improvement_report']:
        print("Critical Improvements Needed:")
        for imp in results['improvement_report']['critical_improvements']:
            print(f"  - {imp}")

    return results


if __name__ == "__main__":
    run_tornado_blind_test()
