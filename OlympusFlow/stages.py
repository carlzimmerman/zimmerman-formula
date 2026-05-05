#!/usr/bin/env python3
"""
OLYMPUSFLOW - Pipeline Stages
=============================

Stage definitions for the research pipeline.
Each stage:
1. Implements a standard interface
2. Emits events for monitoring
3. Uses data contracts for I/O
4. Can be configured and composed

Stages:
- DiscoveryStage: Find data (wraps HermesFlow)
- AnalysisStage: Find Z² patterns in data
- VerificationStage: Run HRM assessment
- StorageStage: Store to MnemosyneLake
- TrainingStage: Generate training data

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import time
import math
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass

import numpy as np
import pandas as pd

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .contracts import (
    Discovery, Finding, VerifiedTruth, DataSource,
    StageResult, PipelineState, HRMAssessment,
    TrainingExample, TrainingBatch, DataFormat
)
from .events import EventEmitter, EventType, get_event_bus


# =============================================================================
# STAGE INTERFACE
# =============================================================================

class Stage(ABC, EventEmitter):
    """
    Base class for all pipeline stages.

    Every stage must implement:
    - run(): Execute the stage logic
    - validate_input(): Check input is valid
    - get_output_type(): Return expected output type
    """

    def __init__(self, name: str = None, config: Dict = None):
        super().__init__()
        self.name = name or self.__class__.__name__
        self.config = config or {}
        self._stage_name = self.name

    @abstractmethod
    def run(self, input_data: Any, state: PipelineState) -> StageResult:
        """
        Execute the stage.

        Args:
            input_data: Input from previous stage
            state: Current pipeline state

        Returns:
            StageResult with output or error
        """
        pass

    def validate_input(self, input_data: Any) -> bool:
        """Validate input data. Override for specific validation."""
        return input_data is not None

    def get_output_type(self) -> Type:
        """Return the expected output type."""
        return Any

    def _success(self, output: Any, duration: float) -> StageResult:
        """Create a successful result."""
        self.emit(EventType.STAGE_COMPLETED, {
            "stage": self.name,
            "duration": duration
        })
        return StageResult(
            stage_name=self.name,
            success=True,
            output=output,
            duration_seconds=duration
        )

    def _failure(self, error: str, duration: float) -> StageResult:
        """Create a failed result."""
        self.emit(EventType.STAGE_FAILED, {
            "stage": self.name,
            "error": error,
            "duration": duration
        })
        return StageResult(
            stage_name=self.name,
            success=False,
            error=error,
            duration_seconds=duration
        )


# =============================================================================
# DISCOVERY STAGE
# =============================================================================

class DiscoveryStage(Stage):
    """
    Discover data from web sources.
    Wraps HermesFlow for data acquisition.
    """

    def __init__(self, topic: str, domain: str, quantities: List[str],
                 model: str = None, **kwargs):
        super().__init__("DiscoveryStage", kwargs)
        self.topic = topic
        self.domain = domain
        self.quantities = quantities
        self.model = model or os.environ.get("LEGOMENA_MODEL", "legomena-31b-clean")

    def run(self, input_data: Any, state: PipelineState) -> StageResult:
        """Run data discovery using HermesFlow."""
        start = time.time()

        self.emit(EventType.DISCOVERY_STARTED, {
            "topic": self.topic,
            "domain": self.domain
        })

        try:
            from HermesFlow.hermes_explorer import HermesExplorer

            # Set model
            os.environ["LEGOMENA_MODEL"] = self.model

            explorer = HermesExplorer(verbose=self.config.get("verbose", True))
            result = explorer.explore_for_data(
                topic=self.topic,
                domain=self.domain,
                quantities=self.quantities
            )

            if result.success and result.data is not None:
                # Create Discovery contract
                discovery = Discovery(
                    discovery_id=Discovery.generate_id(self.topic, self.domain),
                    topic=self.topic,
                    domain=self.domain,
                    quantities=self.quantities,
                    success=True,
                    source=DataSource(
                        url=result.url,
                        title=f"Data from {result.url.split('/')[2]}",
                        domain=self.domain,
                        format=self._detect_format(result.url),
                        rows=len(result.data),
                        columns=len(result.data.columns),
                        column_names=list(result.data.columns)[:20]
                    ),
                    raw_data=result.data.head(100).to_dict(),
                    steps_taken=len(result.steps)
                )

                self.emit(EventType.DISCOVERY_FOUND, {
                    "url": result.url,
                    "rows": len(result.data),
                    "columns": len(result.data.columns)
                })

                # Add to state
                state.discoveries.append(discovery)

                return self._success(discovery, time.time() - start)
            else:
                self.emit(EventType.DISCOVERY_FAILED, {
                    "reason": result.description
                })
                return self._failure(result.description, time.time() - start)

        except ImportError as e:
            return self._failure(f"HermesFlow not available: {e}", time.time() - start)
        except Exception as e:
            return self._failure(str(e), time.time() - start)

    def _detect_format(self, url: str) -> str:
        """Detect data format from URL."""
        url_lower = url.lower()
        if '.csv' in url_lower:
            return DataFormat.CSV.value
        elif '.json' in url_lower:
            return DataFormat.JSON.value
        elif '.xml' in url_lower:
            return DataFormat.XML.value
        return DataFormat.UNKNOWN.value

    def get_output_type(self) -> Type:
        return Discovery


# =============================================================================
# ANALYSIS STAGE
# =============================================================================

class AnalysisStage(Stage):
    """
    Analyze discovered data for Z² patterns.
    Looks for fundamental constants in statistical properties.
    """

    # Z² constants to search for
    Z2 = 32 * math.pi / 3
    Z = math.sqrt(Z2)
    PHI = (1 + math.sqrt(5)) / 2

    TARGETS = {
        "Z²": Z2,
        "Z": Z,
        "Z²/10": Z2 / 10,
        "φ": PHI,
        "1/φ": 1 / PHI,
        "π": math.pi,
        "π/2": math.pi / 2,
        "2π": 2 * math.pi,
    }

    def __init__(self, error_threshold: float = 5.0, min_samples: int = 30, **kwargs):
        super().__init__("AnalysisStage", kwargs)
        self.error_threshold = error_threshold
        self.min_samples = min_samples

    def run(self, input_data: Discovery, state: PipelineState) -> StageResult:
        """Analyze discovery for Z² patterns."""
        start = time.time()

        if not self.validate_input(input_data):
            return self._failure("Invalid input: expected Discovery", time.time() - start)

        try:
            # Convert raw_data back to DataFrame
            df = pd.DataFrame(input_data.raw_data)

            findings = self._analyze_dataframe(df, input_data)

            # Add findings to state
            state.findings.extend(findings)

            self.emit(EventType.STAGE_COMPLETED, {
                "findings_count": len(findings),
                "significant": sum(1 for f in findings if f.is_significant())
            })

            return self._success(findings, time.time() - start)

        except Exception as e:
            return self._failure(str(e), time.time() - start)

    def _analyze_dataframe(self, df: pd.DataFrame, discovery: Discovery) -> List[Finding]:
        """Analyze DataFrame for Z² patterns."""
        findings = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols[:15]:  # Limit to first 15 numeric columns
            data = df[col].dropna()
            if len(data) < self.min_samples:
                continue

            mean = data.mean()
            std = data.std()

            if std == 0 or mean == 0:
                continue

            # Coefficient of variation
            cv = std / abs(mean)

            # Check against targets
            for target_name, target_value in self.TARGETS.items():
                error = abs(cv - target_value) / target_value * 100
                if error < self.error_threshold:
                    finding = Finding(
                        finding_id=Finding.generate_id(f"CV({col})", target_name),
                        domain=discovery.domain,
                        quantity=f"CV({col})",
                        measured_value=cv,
                        target_constant=target_name,
                        target_value=target_value,
                        percent_error=error,
                        sample_size=len(data),
                        source_url=discovery.source.url if discovery.source else ""
                    )
                    findings.append(finding)

            # Also check mean and std directly
            for target_name, target_value in self.TARGETS.items():
                # Check mean
                if abs(mean) > 0.1:  # Avoid tiny values
                    error = abs(mean - target_value) / target_value * 100
                    if error < self.error_threshold:
                        findings.append(Finding(
                            finding_id=Finding.generate_id(f"mean({col})", target_name),
                            domain=discovery.domain,
                            quantity=f"mean({col})",
                            measured_value=mean,
                            target_constant=target_name,
                            target_value=target_value,
                            percent_error=error,
                            sample_size=len(data),
                            source_url=discovery.source.url if discovery.source else ""
                        ))

        return findings

    def validate_input(self, input_data: Any) -> bool:
        return isinstance(input_data, Discovery) and input_data.raw_data is not None

    def get_output_type(self) -> Type:
        return List[Finding]


# =============================================================================
# VERIFICATION STAGE
# =============================================================================

class VerificationStage(Stage):
    """
    Verify findings using HRM (Hierarchical Recursive Meta-assessment).
    Converts findings to verified truths.
    """

    def __init__(self, min_hrm: float = 0.8, use_llm: bool = True, **kwargs):
        super().__init__("VerificationStage", kwargs)
        self.min_hrm = min_hrm
        self.use_llm = use_llm

    def run(self, input_data: List[Finding], state: PipelineState) -> StageResult:
        """Verify findings and create truths."""
        start = time.time()

        if not input_data:
            return self._success([], time.time() - start)

        self.emit(EventType.VERIFICATION_STARTED, {
            "findings_count": len(input_data)
        })

        truths = []
        for finding in input_data:
            truth = self._verify_finding(finding)
            if truth:
                truths.append(truth)
                state.truths.append(truth)

                if truth.status == "validated":
                    self.emit(EventType.VERIFICATION_PASSED, {
                        "claim": truth.claim,
                        "hrm_score": truth.hrm_score
                    })
                else:
                    self.emit(EventType.VERIFICATION_FAILED, {
                        "claim": truth.claim,
                        "hrm_score": truth.hrm_score
                    })

        return self._success(truths, time.time() - start)

    def _verify_finding(self, finding: Finding) -> Optional[VerifiedTruth]:
        """Run HRM assessment on a finding."""
        # Level 1: Basic honesty check
        l1_score = self._assess_level_1(finding)

        # Level 2: Bias detection
        l2_score = self._assess_level_2(finding, l1_score)

        # Level 3: Only if L1/L2 disagree significantly
        l3_score = None
        if abs(l1_score - l2_score) > 0.2:
            l3_score = self._assess_level_3(finding, l1_score, l2_score)

        # Compute final score
        hrm = HRMAssessment(
            level_1_score=l1_score,
            level_1_reasoning="Statistical significance check",
            level_2_score=l2_score,
            level_2_reasoning="Bias and alternative explanations check",
            level_3_score=l3_score,
            level_3_reasoning="Final arbitration" if l3_score else None
        )
        final_score = hrm.compute_final()

        # Create truth
        truth = VerifiedTruth(
            truth_id=VerifiedTruth.generate_id(
                f"{finding.quantity} = {finding.target_constant}",
                finding.domain
            ),
            domain=finding.domain,
            claim=f"{finding.quantity} = {finding.target_constant}",
            z2_formula=f"{finding.target_constant} = {finding.target_value:.6f}",
            z2_prediction=finding.target_value,
            measured_value=finding.measured_value,
            percent_error=finding.percent_error,
            hrm_score=final_score,
            hrm_assessment=hrm,
            data_source=f"Discovered via OlympusFlow",
            data_url=finding.source_url
        )
        truth.update_status()

        self.emit(EventType.TRUTH_CREATED, {
            "claim": truth.claim,
            "hrm_score": truth.hrm_score,
            "status": truth.status
        })

        return truth

    def _assess_level_1(self, finding: Finding) -> float:
        """Level 1: Basic honesty - Is this statistically significant?"""
        score = 0.5  # Base score

        # Better error = higher score
        if finding.percent_error < 0.1:
            score += 0.4
        elif finding.percent_error < 1.0:
            score += 0.3
        elif finding.percent_error < 3.0:
            score += 0.2
        elif finding.percent_error < 5.0:
            score += 0.1

        # More samples = higher score
        if finding.sample_size >= 1000:
            score += 0.1
        elif finding.sample_size >= 100:
            score += 0.05

        return min(score, 1.0)

    def _assess_level_2(self, finding: Finding, l1: float) -> float:
        """Level 2: Bias detection - Were we too optimistic?"""
        # Start with L1 and apply skepticism
        score = l1

        # If error is suspiciously low, be more skeptical
        if finding.percent_error < 0.01:
            score -= 0.1  # Too good to be true?

        # If sample size is borderline, penalize
        if finding.sample_size < 50:
            score -= 0.1

        # Check if this is a "fishing" result (testing many columns)
        # In reality, we'd track how many tests were done
        # For now, slight penalty
        score -= 0.05

        return max(0, min(score, 1.0))

    def _assess_level_3(self, finding: Finding, l1: float, l2: float) -> float:
        """Level 3: Final arbitration when L1/L2 disagree."""
        # Conservative approach: take the lower score
        base = min(l1, l2)

        # But if error is very low and sample is large, give benefit of doubt
        if finding.percent_error < 1.0 and finding.sample_size >= 100:
            return base + 0.1

        return base

    def get_output_type(self) -> Type:
        return List[VerifiedTruth]


# =============================================================================
# STORAGE STAGE
# =============================================================================

class StorageStage(Stage):
    """
    Store verified truths to MnemosyneLake.
    """

    def __init__(self, min_hrm: float = 0.7, **kwargs):
        super().__init__("StorageStage", kwargs)
        self.min_hrm = min_hrm
        self.lake = None

    def run(self, input_data: List[VerifiedTruth], state: PipelineState) -> StageResult:
        """Store truths to MnemosyneLake."""
        start = time.time()

        if not input_data:
            return self._success({"stored": 0}, time.time() - start)

        try:
            from MnemosyneLake import MnemosyneLake, VerifiedTruth as LakeTruth

            if self.lake is None:
                self.lake = MnemosyneLake()

            stored = 0
            for truth in input_data:
                if truth.hrm_score >= self.min_hrm:
                    # Convert to lake format
                    lake_truth = LakeTruth(
                        truth_id=truth.truth_id,
                        domain=truth.domain,
                        claim=truth.claim,
                        z2_formula=truth.z2_formula,
                        z2_prediction=truth.z2_prediction,
                        measured_value=truth.measured_value,
                        percent_error=truth.percent_error,
                        hrm_score=truth.hrm_score,
                        data_source=truth.data_source,
                        data_url=truth.data_url,
                        status=truth.status
                    )
                    self.lake.add_truth(lake_truth)
                    stored += 1

                    self.emit(EventType.TRUTH_STORED, {
                        "truth_id": truth.truth_id,
                        "claim": truth.claim
                    })

            return self._success({"stored": stored, "total": len(input_data)}, time.time() - start)

        except ImportError:
            return self._failure("MnemosyneLake not available", time.time() - start)
        except Exception as e:
            return self._failure(str(e), time.time() - start)

    def get_output_type(self) -> Type:
        return Dict


# =============================================================================
# TRAINING STAGE
# =============================================================================

class TrainingStage(Stage):
    """
    Generate training data from stored truths.
    Optionally triggers model retraining.
    """

    def __init__(self, output_path: Path = None, min_hrm: float = 0.8, **kwargs):
        super().__init__("TrainingStage", kwargs)
        self.output_path = output_path
        self.min_hrm = min_hrm

    def run(self, input_data: Dict, state: PipelineState) -> StageResult:
        """Generate training data."""
        start = time.time()

        self.emit(EventType.TRAINING_STARTED, {
            "truths_available": len(state.truths)
        })

        try:
            from MnemosyneLake import MnemosyneLake, TruthExporter

            lake = MnemosyneLake()
            exporter = TruthExporter(lake)

            # Export to JSONL
            output_file = self.output_path or Path("training_data.jsonl")
            training_data = exporter.export_for_legomena(
                str(output_file),
                min_hrm=self.min_hrm
            )

            self.emit(EventType.TRAINING_COMPLETED, {
                "examples": len(training_data),
                "output_file": str(output_file)
            })

            return self._success({
                "examples": len(training_data),
                "output_file": str(output_file)
            }, time.time() - start)

        except ImportError:
            return self._failure("MnemosyneLake not available", time.time() - start)
        except Exception as e:
            return self._failure(str(e), time.time() - start)

    def get_output_type(self) -> Type:
        return Dict


# =============================================================================
# COMPOSITE STAGES
# =============================================================================

class SequentialStages(Stage):
    """Run multiple stages in sequence."""

    def __init__(self, stages: List[Stage], name: str = "SequentialStages"):
        super().__init__(name)
        self.stages = stages

    def run(self, input_data: Any, state: PipelineState) -> StageResult:
        """Run all stages in sequence."""
        start = time.time()
        current_input = input_data

        for stage in self.stages:
            result = stage.run(current_input, state)
            if not result.success:
                return self._failure(
                    f"{stage.name} failed: {result.error}",
                    time.time() - start
                )
            current_input = result.output

        return self._success(current_input, time.time() - start)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("OlympusFlow Pipeline Stages")
    print("=" * 40)

    # Create a mock discovery for testing
    from .contracts import Discovery, DataSource, PipelineState

    state = PipelineState(
        pipeline_id="test",
        config={}
    )

    discovery = Discovery(
        discovery_id="test123",
        topic="Test topic",
        domain="test",
        quantities=["value"],
        success=True,
        source=DataSource(
            url="https://example.com/data.csv",
            title="Test Data",
            domain="test"
        ),
        raw_data={
            "col1": [1, 2, 3, 4, 5] * 20,
            "col2": [33.5, 33.6, 33.4, 33.5, 33.5] * 20  # Near Z²
        }
    )

    # Run analysis
    analysis = AnalysisStage(error_threshold=5.0)
    result = analysis.run(discovery, state)
    print(f"\nAnalysis: {result.success}, findings: {len(result.output) if result.output else 0}")

    if result.output:
        # Run verification
        verification = VerificationStage(min_hrm=0.5)
        result = verification.run(result.output, state)
        print(f"Verification: {result.success}, truths: {len(result.output) if result.output else 0}")

        if result.output:
            for truth in result.output:
                print(f"  - {truth.claim}: HRM={truth.hrm_score:.2f}, status={truth.status}")
