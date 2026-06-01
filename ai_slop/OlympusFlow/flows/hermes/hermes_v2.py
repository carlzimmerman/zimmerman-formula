#!/usr/bin/env python3
"""
HERMES V2: Dynamic Data Acquisition
====================================

The integration layer that connects:
- Dynamic topic understanding (what to look for)
- Web navigation (how to find it)
- Adaptive validation (is this what we wanted?)
- Learning loop (remember what works)

This is the "brain" that drives the "hands" (web tools).

Key insight from 1000+ commits:
    Carl's process: Understand topic → Identify sources → Navigate to data → Validate → Learn
    HermesV2: Same process, automated

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import math
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Import the dynamic strategy components
from dynamic_strategy import (
    TopicAnalyzer, StrategyPlanner, DynamicValidator, OutcomeTracker,
    TopicProfile, SearchStrategy
)

# Import the existing HermesFlow tools
try:
    from hermes_explorer import HermesExplorer, DataDiscovery
    HERMES_V1_AVAILABLE = True
except ImportError:
    HERMES_V1_AVAILABLE = False
    print("[WARN] HermesExplorer v1 not available")


@dataclass
class AcquisitionResult:
    """Result of a dynamic data acquisition attempt."""
    success: bool
    topic: str
    domain: str

    # What we learned about the topic
    profile: Dict

    # What we found
    data_url: Optional[str] = None
    data_shape: Optional[Tuple] = None
    data_columns: Optional[List[str]] = None

    # Validation
    validation_passed: bool = False
    validation_reason: str = ""
    quantities_found: List[str] = None

    # Z² analysis
    z2_patterns: List[Dict] = None

    # Meta
    strategies_tried: int = 0
    time_seconds: float = 0
    timestamp: str = None


class HermesV2:
    """
    Dynamic Data Acquisition Engine.

    The key difference from V1:
    - V1: Uses LLM for search guidance but has hardcoded validation
    - V2: Uses LLM for EVERYTHING - understanding, searching, validating, learning

    Flow:
    1. Analyze topic → What are we looking for?
    2. Plan strategy → How should we search?
    3. Navigate → Use web tools to find data
    4. Validate dynamically → Is this what we wanted?
    5. Extract & analyze → Look for Z² patterns
    6. Learn → Remember what worked
    """

    # Z² constants
    Z2 = 32 * math.pi / 3
    Z = math.sqrt(Z2)
    PHI = (1 + math.sqrt(5)) / 2

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

        # Dynamic components
        self.analyzer = TopicAnalyzer(verbose)
        self.planner = StrategyPlanner(verbose)
        self.validator = DynamicValidator(verbose)
        self.tracker = OutcomeTracker()

        # V1 explorer for actual web operations
        self.explorer = HermesExplorer(verbose=verbose) if HERMES_V1_AVAILABLE else None

        # Z² context for predictions
        self.z2_context = f"""
Z² Framework Constants:
- Z² = 32π/3 = {self.Z2:.6f}
- Z = √(Z²) = {self.Z:.6f}
- φ = (1+√5)/2 = {self.PHI:.6f}

Common patterns:
- CV (coefficient of variation) ≈ Z or Z²/10
- Ratios ≈ φ or 1/φ
- Scale factors ≈ Z²
"""

    def _log(self, msg: str):
        if self.verbose:
            print(f"[HermesV2] {msg}")

    def acquire(self, topic: str, domain: str) -> AcquisitionResult:
        """
        Main entry point: Acquire data for ANY research topic.

        This does what Carl has been doing manually:
        1. Understand what we need
        2. Figure out where to get it
        3. Navigate there and get it
        4. Verify it's right
        5. Analyze for Z² patterns
        6. Learn from the experience
        """
        start_time = time.time()

        self._log("=" * 70)
        self._log(f"HERMES V2: Dynamic Data Acquisition")
        self._log(f"Topic: {topic}")
        self._log(f"Domain: {domain}")
        self._log("=" * 70)

        # =====================================================================
        # PHASE 1: UNDERSTAND THE TOPIC
        # =====================================================================
        self._log("\n>>> PHASE 1: Topic Understanding")

        profile = self.analyzer.analyze(topic, domain, self.z2_context)

        self._log(f"Discovered {len(profile.key_terms)} key terms")
        self._log(f"Identified {len(profile.authoritative_sources)} data sources")
        self._log(f"Target quantities: {profile.target_quantities[:5]}")

        # Check if we have learned hints for this domain
        domain_hints = self.tracker.get_domain_hints(domain)
        if domain_hints.get('successful_sources'):
            self._log(f"Learned hint: Try {domain_hints['successful_sources'][:2]}")
            # Boost these sources in the profile
            for source_url in domain_hints['successful_sources'][:2]:
                profile.authoritative_sources.insert(0, {
                    'name': 'Previously successful',
                    'url': source_url,
                    'learned': True
                })

        # =====================================================================
        # PHASE 2: PLAN SEARCH STRATEGY
        # =====================================================================
        self._log("\n>>> PHASE 2: Strategy Planning")

        strategies = self.planner.plan(profile)

        if not strategies:
            # Generate fallback strategies from profile
            strategies = self._generate_fallback_strategies(profile)

        self._log(f"Generated {len(strategies)} search strategies")

        # =====================================================================
        # PHASE 3: EXECUTE NAVIGATION
        # =====================================================================
        self._log("\n>>> PHASE 3: Web Navigation")

        discovery = None
        strategies_tried = 0

        for strategy in strategies[:5]:  # Try up to 5 strategies
            strategies_tried += 1
            self._log(f"\nTrying strategy {strategies_tried}: {strategy.query[:50]}...")

            if self.explorer:
                # Use profile's quantities for the search
                quantities = profile.target_quantities[:5] if profile.target_quantities else ['value', 'measurement']

                # Execute the search with our strategy
                discovery = self.explorer.explore_for_data(
                    topic=strategy.query,
                    domain=domain,
                    quantities=quantities
                )

                if discovery.success:
                    self._log(f"SUCCESS: Found data at {discovery.url}")
                    break
                else:
                    self._log(f"Strategy failed, trying next...")

        if not discovery or not discovery.success:
            self._log("All strategies failed")
            return AcquisitionResult(
                success=False,
                topic=topic,
                domain=domain,
                profile=asdict(profile),
                strategies_tried=strategies_tried,
                time_seconds=time.time() - start_time,
                timestamp=datetime.now().isoformat()
            )

        # =====================================================================
        # PHASE 4: DYNAMIC VALIDATION
        # =====================================================================
        self._log("\n>>> PHASE 4: Dynamic Validation")

        # Create data summary for validation
        data_summary = self._create_data_summary(discovery.data)

        is_valid, reason, val_info = self.validator.validate(data_summary, profile)

        self._log(f"Validation: {'PASSED' if is_valid else 'FAILED'}")
        self._log(f"Reason: {reason}")

        if not is_valid:
            # Record failure for learning
            self.tracker.record_failure(
                profile,
                strategies[strategies_tried - 1],
                f"Validation failed: {reason}"
            )

        # =====================================================================
        # PHASE 5: Z² PATTERN ANALYSIS
        # =====================================================================
        self._log("\n>>> PHASE 5: Z² Pattern Analysis")

        z2_patterns = self._analyze_z2_patterns(discovery.data, profile)

        self._log(f"Found {len(z2_patterns)} potential Z² patterns")

        for pattern in z2_patterns[:3]:
            self._log(f"  {pattern['quantity']}: {pattern['value']:.4f} ≈ {pattern['target']} ({pattern['error']:.2f}% error)")

        # =====================================================================
        # PHASE 6: LEARNING
        # =====================================================================
        self._log("\n>>> PHASE 6: Learning")

        if is_valid:
            self.tracker.record_success(
                profile,
                strategies[strategies_tried - 1],
                discovery.url,
                data_summary
            )
            self._log("Recorded successful strategy for future use")

        # =====================================================================
        # RESULT
        # =====================================================================
        elapsed = time.time() - start_time

        result = AcquisitionResult(
            success=is_valid,
            topic=topic,
            domain=domain,
            profile=asdict(profile),
            data_url=discovery.url,
            data_shape=tuple(discovery.data.shape) if discovery.data is not None else None,
            data_columns=list(discovery.data.columns) if discovery.data is not None else None,
            validation_passed=is_valid,
            validation_reason=reason,
            quantities_found=val_info.get('quantities', '').split(',') if val_info.get('quantities') else [],
            z2_patterns=z2_patterns,
            strategies_tried=strategies_tried,
            time_seconds=elapsed,
            timestamp=datetime.now().isoformat()
        )

        self._log("\n" + "=" * 70)
        self._log("ACQUISITION COMPLETE")
        self._log(f"Success: {result.success}")
        self._log(f"URL: {result.data_url}")
        self._log(f"Shape: {result.data_shape}")
        self._log(f"Z² patterns: {len(z2_patterns)}")
        self._log(f"Time: {elapsed:.1f}s")
        self._log("=" * 70)

        return result

    def _generate_fallback_strategies(self, profile: TopicProfile) -> List[SearchStrategy]:
        """Generate strategies from profile when planner returns empty."""
        strategies = []

        # Strategy from key terms
        if profile.key_terms:
            strategies.append(SearchStrategy(
                query=f"{' '.join(profile.key_terms[:3])} data CSV download",
                rationale="Direct search using key terms",
                expected_sources=[],
                fallback_queries=[],
                validation_criteria=profile.target_quantities[:3],
                priority=1
            ))

        # Strategy from authoritative sources
        for source in profile.authoritative_sources[:2]:
            if source.get('name'):
                strategies.append(SearchStrategy(
                    query=f"{source['name']} {profile.topic} data",
                    rationale=f"Search authoritative source: {source['name']}",
                    expected_sources=[source.get('url', '')],
                    fallback_queries=[],
                    validation_criteria=profile.target_quantities[:3],
                    priority=2
                ))

        # Domain-specific strategy
        strategies.append(SearchStrategy(
            query=f"{profile.domain} {profile.topic} official dataset",
            rationale="Domain-scoped official data search",
            expected_sources=[],
            fallback_queries=[],
            validation_criteria=profile.target_quantities[:3],
            priority=3
        ))

        return strategies

    def _create_data_summary(self, df) -> str:
        """Create a text summary of data for validation."""
        if df is None:
            return "No data"

        summary = f"Shape: {df.shape}\n"
        summary += f"Columns: {list(df.columns)}\n"
        summary += f"Sample (first 3 rows):\n{df.head(3).to_string()}"
        return summary

    def _analyze_z2_patterns(self, df, profile: TopicProfile) -> List[Dict]:
        """Analyze data for Z² patterns."""
        import numpy as np

        patterns = []
        if df is None:
            return patterns

        targets = {
            "Z": self.Z,
            "Z²": self.Z2,
            "Z²/10": self.Z2 / 10,
            "φ": self.PHI,
            "1/φ": 1 / self.PHI,
            "π": math.pi,
        }

        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols[:15]:
            data = df[col].dropna()
            if len(data) < 10:
                continue

            mean = data.mean()
            std = data.std()

            if std == 0 or mean == 0:
                continue

            cv = std / abs(mean)

            for target_name, target_val in targets.items():
                error = abs(cv - target_val) / target_val * 100
                if error < 10:  # Within 10%
                    patterns.append({
                        "quantity": f"CV({col})",
                        "value": cv,
                        "target": target_name,
                        "target_value": target_val,
                        "error": error,
                        "n_samples": len(data)
                    })

        return patterns


# =============================================================================
# FULL PIPELINE INTEGRATION
# =============================================================================

def run_research(topic: str, domain: str) -> AcquisitionResult:
    """
    Run full research pipeline for any topic.

    This is the entry point for autonomous scientific research.
    """
    hermes = HermesV2(verbose=True)
    return hermes.acquire(topic, domain)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("HERMES V2: DYNAMIC DATA ACQUISITION DEMO")
    print("=" * 70)
    print()

    # Test with a new topic - system should figure out everything dynamically
    result = run_research(
        topic="Global seismic activity magnitude distribution USGS",
        domain="seismology"
    )

    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)
    print(f"Success: {result.success}")
    print(f"Data URL: {result.data_url}")
    print(f"Data shape: {result.data_shape}")
    print(f"Validation: {result.validation_reason}")
    print(f"Z² patterns found: {len(result.z2_patterns) if result.z2_patterns else 0}")
    print(f"Strategies tried: {result.strategies_tried}")
    print(f"Time: {result.time_seconds:.1f}s")
