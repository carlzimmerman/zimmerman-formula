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

Version History:
- v1.5.0: Added derivation mode to DiscoveryStage
- v1.6.0: Added MetisFlow integration for research-driven derivation
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

# HeliconLake integration for source registry
try:
    from OlympusFlow.lakes.helicon import HeliconLake
    HELICON_AVAILABLE = True
except ImportError:
    HELICON_AVAILABLE = False
    HeliconLake = None


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
    Discover data from web sources OR derive Z² formulas.

    v1.5.0: Added derivation mode
    - When target_constant is set, uses TruthEngine for Z² formula discovery
    - Otherwise, uses HermesFlow for web data discovery

    v1.6.0: Added MetisFlow integration (research-driven derivation)
    - MetisFlow researches existing derivations in literature
    - Assesses Z² relevance before attempting derivation
    - Provides mathematical path guidance to TruthEngine
    - Skips derivation if no Z² relevance found
    """

    def __init__(self, topic: str, domain: str, quantities: List[str],
                 model: str = None,
                 target_constant: str = "", target_value: float = 0.0,
                 **kwargs):
        super().__init__("DiscoveryStage", kwargs)
        self.topic = topic
        self.domain = domain
        self.quantities = quantities
        self.model = model or os.environ.get("LEGOMENA_MODEL", "legomena-moe")

        # Z² Derivation mode (v1.5.0)
        self.target_constant = target_constant
        self.target_value = target_value
        self.is_derivation = bool(target_constant and target_value)

    def run(self, input_data: Any, state: PipelineState) -> StageResult:
        """
        Run discovery:
        - Derivation mode: Use TruthEngine to find Z² formula matches
        - Data mode: Use HermesFlow for web data discovery
        """
        start = time.time()

        self.emit(EventType.DISCOVERY_STARTED, {
            "topic": self.topic,
            "domain": self.domain,
            "mode": "derivation" if self.is_derivation else "data"
        })

        # =====================================================================
        # DERIVATION MODE: Use TruthEngine for Z² formula matching
        # =====================================================================
        if self.is_derivation:
            return self._run_derivation_discovery(state, start)

        # =====================================================================
        # DATA MODE: Use HermesFlow for web data discovery
        # =====================================================================
        return self._run_data_discovery(state, start)

    def _run_derivation_discovery(self, state: PipelineState, start: float) -> StageResult:
        """
        Use MetisFlow + TruthEngine for principled Z² derivation.

        v1.6.0: Added MetisFlow integration for research-driven derivation
        1. MetisFlow researches existing derivations in literature
        2. Assesses if Z² approach is viable
        3. Creates derivation strategy
        4. TruthEngine attempts derivation with strategy guidance
        """
        print(f"[Discovery] Z² derivation pipeline: {self.target_constant}")

        # =====================================================================
        # STEP 1: METISFLOW RESEARCH (Wisdom before action)
        # =====================================================================
        metis_result = None
        strategy = None

        try:
            from MetisFlow import MetisEngine, ZSquaredRelevance

            print(f"[MetisFlow] Researching: {self.target_constant}")
            metis = MetisEngine(verbose=False)
            metis_result = metis.research(self.target_constant, self.target_value)
            strategy = metis_result.strategy

            print(f"[MetisFlow] Research complete:")
            print(f"  - Derivation exists: {metis_result.derivation_exists}")
            print(f"  - Z² viable: {metis_result.z_squared_viable}")
            print(f"  - Approach: {strategy.recommended_approach.value}")
            print(f"  - Confidence: {strategy.confidence_score:.2f}")

            # Check if Z² approach is viable
            if strategy.z_squared_relevance == ZSquaredRelevance.NONE:
                print(f"[MetisFlow] SKIPPING: No Z² relevance for {self.target_constant}")
                self.emit(EventType.DISCOVERY_FAILED, {
                    "reason": f"MetisFlow: No Z² relevance for {self.target_constant}",
                    "recommendation": metis_result.recommendation
                })
                return self._failure(
                    f"No Z² relevance: {metis_result.recommendation}",
                    time.time() - start
                )

        except ImportError:
            print(f"[MetisFlow] Not available, proceeding without research")
        except Exception as e:
            print(f"[MetisFlow] Research failed: {e}, proceeding without strategy")

        # =====================================================================
        # STEP 2: TRUTHENGINE DERIVATION (Guided by MetisFlow strategy)
        # =====================================================================
        print(f"[Discovery] Using TruthEngine for Z² derivation: {self.target_constant}")

        try:
            from TruthFlow import TruthEngine

            engine = TruthEngine()
            result = engine.derive_constant(
                target=self.target_constant,
                target_value=self.target_value,
                assignment=self.topic
            )

            # Create Discovery contract with derivation results
            if result.get('formulas'):
                best = result.get('best_formula', 'unknown')
                best_error = result.get('best_error', 100)

                # Include MetisFlow research in raw_data
                metis_data = {}
                if metis_result and strategy:
                    metis_data = {
                        'metis_research': {
                            'derivation_exists': metis_result.derivation_exists,
                            'z_squared_viable': metis_result.z_squared_viable,
                            'z_squared_relevance': strategy.z_squared_relevance.value,
                            'recommended_approach': strategy.recommended_approach.value,
                            'z_squared_connection': strategy.z_squared_connection,
                            'confidence_score': strategy.confidence_score,
                            'physical_meaning': strategy.physical_meaning,
                            'mathematical_path': strategy.mathematical_path[:200] if strategy.mathematical_path else "",
                            'recommendation': metis_result.recommendation
                        }
                    }

                discovery = Discovery(
                    discovery_id=Discovery.generate_id(self.target_constant, self.domain),
                    topic=self.topic,
                    domain=self.domain,
                    quantities=[self.target_constant],
                    success=True,
                    source=DataSource(
                        url="",
                        title=f"Z² Derivation: {self.target_constant}",
                        domain=self.domain,
                        format=DataFormat.JSON.value
                    ),
                    raw_data={
                        'target_constant': self.target_constant,
                        'target_value': self.target_value,
                        'best_formula': best,
                        'best_error': best_error,
                        'formulas': result.get('formulas', []),
                        'derivation_status': result.get('status', 'unknown'),
                        **metis_data
                    },
                    steps_taken=2 if metis_result else 1  # Count MetisFlow as a step
                )

                self.emit(EventType.DISCOVERY_FOUND, {
                    "type": "derivation",
                    "target": self.target_constant,
                    "best_formula": best,
                    "error": best_error
                })

                state.discoveries.append(discovery)
                return self._success(discovery, time.time() - start)
            else:
                self.emit(EventType.DISCOVERY_FAILED, {
                    "reason": "No Z² formula candidates found"
                })
                return self._failure("No Z² formula candidates found", time.time() - start)

        except ImportError as e:
            return self._failure(f"TruthEngine not available: {e}", time.time() - start)
        except Exception as e:
            return self._failure(str(e), time.time() - start)

    def _run_data_discovery(self, state: PipelineState, start: float) -> StageResult:
        """Use HermesFlow for web data discovery (original behavior)."""

        # STEP 1: Query HeliconLake for cached sources
        helicon_sources = []
        if HELICON_AVAILABLE:
            try:
                helicon_lake = HeliconLake()
                helicon_sources = helicon_lake.find_sources(self.domain, self.topic)
                if helicon_sources:
                    print(f"[HeliconLake] Found {len(helicon_sources)} cached sources for {self.domain}/{self.topic}")
                    for src in helicon_sources[:3]:
                        print(f"  - {src.url[:60]}...")
            except Exception as e:
                print(f"[HeliconLake] Query failed: {e}")

        try:
            from HermesFlow.hermes_explorer import HermesExplorer

            # Set model
            os.environ["LEGOMENA_MODEL"] = self.model

            explorer = HermesExplorer(verbose=self.config.get("verbose", True))

            # STEP 2: Try HeliconLake sources first
            result = None
            if helicon_sources:
                for src in helicon_sources[:3]:  # Try top 3 cached sources
                    try:
                        print(f"[HeliconLake] Trying cached source: {src.url}")
                        result = explorer.try_specific_url(
                            url=src.url,
                            topic=self.topic,
                            quantities=self.quantities
                        )
                        if result and result.success:
                            print(f"[HeliconLake] Successfully used cached source!")
                            # Mark as validated
                            if HELICON_AVAILABLE:
                                helicon_lake.validate_source(src.id)
                            break
                    except Exception as e:
                        print(f"[HeliconLake] Cached source failed: {e}")
                        if HELICON_AVAILABLE:
                            helicon_lake.mark_dead(src.id)
                        continue

            # STEP 3: Fall back to HermesFlow discovery
            if not result or not result.success:
                print(f"[Discovery] Falling back to HermesFlow web discovery...")
                result = explorer.explore_for_data(
                    topic=self.topic,
                    domain=self.domain,
                    quantities=self.quantities
                )

                # STEP 4: Register successful discovery to HeliconLake
                if result.success and HELICON_AVAILABLE and result.url:
                    try:
                        helicon_lake.register_source({
                            'url': result.url,
                            'description': f"Discovered data for {self.topic}",
                            'domains': [self.domain],
                            'topics': [self.topic] + self.quantities[:3],
                            'quantities': self.quantities,
                            'format': self._detect_format(result.url),
                            'discovered_by': 'DiscoveryStage',
                            'discovery_method': 'HermesFlow'
                        })
                        print(f"[HeliconLake] Registered new source: {result.url[:60]}...")
                    except Exception as e:
                        print(f"[HeliconLake] Registration failed: {e}")

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
    Verify findings using HRM (Hierarchical Recursive Meta-assessment)
    AND validate against AletheiaLake ground truths.

    Two-Lake Architecture:
    - Findings are validated against AletheiaLake Z² predictions
    - AletheiaLake matches boost HRM score (validated framework)
    - Contradictions with AletheiaLake are flagged
    """

    def __init__(self, min_hrm: float = 0.8, use_llm: bool = True, **kwargs):
        super().__init__("VerificationStage", kwargs)
        self.min_hrm = min_hrm
        self.use_llm = use_llm
        self.aletheia_lake = None  # Set by pipeline

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
        """
        Run HRM assessment AND AletheiaLake validation on a finding.

        The Two-Lake Architecture validates new discoveries against
        established Z² ground truths stored in AletheiaLake.
        """
        # =====================================================================
        # ALETHEIALAKE VALIDATION (Two-Lake Architecture)
        # =====================================================================
        aletheia_match = None
        aletheia_boost = 0.0
        ground_truth_ref = None

        if self.aletheia_lake:
            aletheia_match = self._check_against_aletheia(finding)
            if aletheia_match:
                ground_truth_ref = aletheia_match.get("truth_name")
                deviation_sigma = aletheia_match.get("deviation_sigma", float('inf'))

                # Boost score if finding matches Z² ground truth
                if deviation_sigma < 1.0:
                    aletheia_boost = 0.15  # Strong match with ground truth
                    self.emit(EventType.TRUTH_CREATED, {
                        "type": "aletheia_match",
                        "finding": finding.quantity,
                        "ground_truth": ground_truth_ref,
                        "deviation_sigma": deviation_sigma
                    })
                elif deviation_sigma < 2.0:
                    aletheia_boost = 0.10  # Consistent with ground truth
                elif deviation_sigma > 3.0:
                    aletheia_boost = -0.20  # CONTRADICTS ground truth!
                    self.emit(EventType.VERIFICATION_FAILED, {
                        "type": "aletheia_contradiction",
                        "finding": finding.quantity,
                        "ground_truth": ground_truth_ref,
                        "deviation_sigma": deviation_sigma,
                        "warning": "Finding contradicts Z² ground truth"
                    })

        # =====================================================================
        # HRM ASSESSMENT
        # =====================================================================

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

        # Apply AletheiaLake boost/penalty
        final_score = max(0, min(1.0, final_score + aletheia_boost))

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
            data_url=finding.source_url,
            ground_truth_ref=ground_truth_ref  # Track which AletheiaLake truth matched
        )
        truth.update_status()

        self.emit(EventType.TRUTH_CREATED, {
            "claim": truth.claim,
            "hrm_score": truth.hrm_score,
            "status": truth.status,
            "aletheia_match": ground_truth_ref
        })

        return truth

    def _check_against_aletheia(self, finding: Finding) -> Optional[Dict]:
        """
        Check if finding matches any AletheiaLake ground truth.

        Returns match info if found, None otherwise.
        """
        if not self.aletheia_lake:
            return None

        # Get all truths in the same domain
        domain_truths = self.aletheia_lake.get_truths_by_domain(finding.domain)

        best_match = None
        best_deviation = float('inf')

        for truth in domain_truths:
            # Check if the prediction values are close
            if truth.z2_prediction is not None and finding.measured_value is not None:
                # Calculate deviation
                if finding.measured_uncertainty and finding.measured_uncertainty > 0:
                    deviation = abs(finding.measured_value - truth.z2_prediction) / finding.measured_uncertainty
                else:
                    # Use percent difference as fallback
                    deviation = abs(finding.measured_value - truth.z2_prediction) / max(abs(truth.z2_prediction), 1e-10) * 100

                if deviation < best_deviation:
                    best_deviation = deviation
                    best_match = {
                        "truth_name": truth.name,
                        "z2_prediction": truth.z2_prediction,
                        "measured_value": finding.measured_value,
                        "deviation_sigma": deviation,
                        "formula": truth.formula
                    }

        # Only return if reasonably close (within 10 sigma)
        if best_match and best_deviation < 10:
            return best_match
        return None

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
            from OlympusFlow.lakes.mnemosyne import MnemosyneLake, VerifiedTruth as LakeTruth

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
            from OlympusFlow.lakes.mnemosyne import MnemosyneLake, TruthExporter

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
