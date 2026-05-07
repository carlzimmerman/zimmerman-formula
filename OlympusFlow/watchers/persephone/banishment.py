#!/usr/bin/env python3
"""
WINTER BANISHER - Banishment Logic for Underworld Lakes
========================================================

The WinterBanisher manages the "descent to the underworld" of failed
findings from MnemosyneLake to the three underworld lakes:

1. TartarusLake: Mathematical errors, wrong derivations
   - Formula doesn't compute correctly
   - Logic errors in derivation
   - High sigma tension with experiment

2. LetheLake: Hallucinations, sycophantic responses
   - LLM made up physics
   - Consensus defaulted to sycophancy
   - No grounding in real data

3. LabyrinthLake: Stuck but potentially valuable
   - Research hit a dead end
   - Needs different approach
   - May be recoverable with more context

Author: Carl Zimmerman
Date: May 7, 2026
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable

from .orchestrator import BanishmentResult, LifecycleDecision, PersephoneConfig


@dataclass
class FailureAnalysis:
    """Analysis of why a finding failed."""
    failure_type: str                    # "math_error", "hallucination", "sycophancy", "stuck"
    severity: str                        # "critical", "major", "minor"
    destination: LifecycleDecision

    # Details
    error_description: str
    evidence: List[str]

    # Recovery
    recoverable: bool
    recovery_suggestions: List[str]

    # Metrics
    sigma_tension: float = 0.0
    sycophancy_score: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "failure_type": self.failure_type,
            "severity": self.severity,
            "destination": self.destination.value,
            "error_description": self.error_description,
            "evidence": self.evidence,
            "recoverable": self.recoverable,
            "recovery_suggestions": self.recovery_suggestions,
            "sigma_tension": self.sigma_tension,
            "sycophancy_score": self.sycophancy_score
        }


class WinterBanisher:
    """
    Manages the banishment of failed findings to underworld lakes.

    The Winter phase is when findings that failed validation are
    "cast down" into the appropriate underworld repository.
    """

    def __init__(self, config: PersephoneConfig, log_fn: Callable = None):
        self.config = config
        self._log = log_fn or print

    def analyze_failure(self, finding: Dict) -> FailureAnalysis:
        """
        Analyze why a finding failed and determine appropriate banishment.
        """
        evidence = []
        recovery_suggestions = []

        # Check for mathematical errors
        math_error = self._check_math_error(finding)
        if math_error:
            return FailureAnalysis(
                failure_type="math_error",
                severity="critical",
                destination=LifecycleDecision.BANISH_TARTARUS,
                error_description=math_error["description"],
                evidence=math_error["evidence"],
                recoverable=math_error.get("recoverable", False),
                recovery_suggestions=math_error.get("suggestions", []),
                sigma_tension=finding.get("sigma_tension", 0.0)
            )

        # Check for sycophancy
        sycophancy = self._check_sycophancy(finding)
        if sycophancy:
            return FailureAnalysis(
                failure_type="sycophancy",
                severity="major",
                destination=LifecycleDecision.BANISH_LETHE,
                error_description=sycophancy["description"],
                evidence=sycophancy["evidence"],
                recoverable=False,
                recovery_suggestions=["Re-run with adversarial prompting"],
                sycophancy_score=sycophancy.get("score", 0.95)
            )

        # Check for hallucination
        hallucination = self._check_hallucination(finding)
        if hallucination:
            return FailureAnalysis(
                failure_type="hallucination",
                severity="major",
                destination=LifecycleDecision.BANISH_LETHE,
                error_description=hallucination["description"],
                evidence=hallucination["evidence"],
                recoverable=False,
                recovery_suggestions=["Verify with external sources", "Check citations"]
            )

        # Check if stuck
        stuck = self._check_stuck(finding)
        if stuck:
            return FailureAnalysis(
                failure_type="stuck",
                severity="minor",
                destination=LifecycleDecision.BANISH_LABYRINTH,
                error_description=stuck["description"],
                evidence=stuck["evidence"],
                recoverable=True,
                recovery_suggestions=stuck.get("suggestions", [
                    "Try different derivation approach",
                    "Add more context from HECATE catalog",
                    "Break into smaller sub-problems"
                ])
            )

        # Default: retain if no clear failure
        return FailureAnalysis(
            failure_type="unknown",
            severity="minor",
            destination=LifecycleDecision.RETAIN,
            error_description="No clear failure pattern detected",
            evidence=[],
            recoverable=True,
            recovery_suggestions=["Continue research"]
        )

    def _check_math_error(self, finding: Dict) -> Optional[Dict]:
        """Check for mathematical errors in the derivation."""

        evidence = []

        # Check sigma tension
        sigma_tension = finding.get("sigma_tension", 0.0)
        if sigma_tension > self.config.banishment_sigma_threshold:
            evidence.append(f"High sigma tension: {sigma_tension:.1f}σ")

        # Check percent error
        percent_error = finding.get("percent_error", 0.0)
        if percent_error > 20.0:  # More than 20% error is suspect
            evidence.append(f"High percent error: {percent_error:.1f}%")

        # Check for formula computation issues
        computed = finding.get("computed_value", finding.get("z2_prediction"))
        expected = finding.get("experimental_value", finding.get("target_value"))

        if computed is not None and expected is not None:
            if expected != 0:
                actual_error = abs(computed - expected) / abs(expected) * 100
                if actual_error > 50.0:
                    evidence.append(f"Computed value {computed} differs significantly from expected {expected}")

        # Check for explicit error markers
        if finding.get("math_error"):
            evidence.append(finding["math_error"])

        if finding.get("derivation_error"):
            evidence.append(finding["derivation_error"])

        if evidence:
            return {
                "description": "Mathematical error detected in derivation",
                "evidence": evidence,
                "recoverable": len(evidence) == 1 and "percent error" in evidence[0].lower(),
                "suggestions": [
                    "Check formula computation",
                    "Verify algebraic steps",
                    "Compare against known Z² values"
                ]
            }

        return None

    def _check_sycophancy(self, finding: Dict) -> Optional[Dict]:
        """Check for sycophantic responses."""

        evidence = []

        # Check explicit sycophancy markers
        if finding.get("is_sycophantic"):
            evidence.append("Marked as sycophantic by Hecate")

        if finding.get("sycophancy_detected"):
            evidence.append(finding["sycophancy_detected"])

        # Check for suspiciously high agreement
        consensus_agreement = finding.get("consensus_agreement", 0.0)
        if consensus_agreement > self.config.banishment_sycophancy_threshold:
            evidence.append(f"Suspiciously high consensus: {consensus_agreement:.2f}")

        # Check for lack of citations despite confidence
        confidence = finding.get("confidence", finding.get("hrm_score", 0.0))
        has_citation = bool(finding.get("citation") or finding.get("source_url"))

        if confidence > 0.9 and not has_citation:
            evidence.append("High confidence claim without citations - potential sycophancy")

        # Check for vague derivation
        derivation = finding.get("derivation", "")
        if derivation and len(derivation) < 50 and confidence > 0.8:
            evidence.append("Brief derivation with high confidence - suspicious")

        if evidence:
            return {
                "description": "Sycophantic response pattern detected",
                "evidence": evidence,
                "score": consensus_agreement if consensus_agreement > 0.9 else 0.95
            }

        return None

    def _check_hallucination(self, finding: Dict) -> Optional[Dict]:
        """Check for hallucinated content."""

        evidence = []

        # Check explicit hallucination markers
        if finding.get("is_hallucination"):
            evidence.append("Marked as hallucination")

        if finding.get("hallucination_detected"):
            evidence.append(finding["hallucination_detected"])

        # Check for non-existent citations
        if finding.get("citation_not_found"):
            evidence.append("Cited source does not exist")

        if finding.get("fake_reference"):
            evidence.append("Reference appears to be fabricated")

        # Check for physically impossible claims
        if finding.get("physical_impossibility"):
            evidence.append(f"Physically impossible: {finding['physical_impossibility']}")

        # Check for contradiction with known physics
        if finding.get("contradicts_known_physics"):
            evidence.append("Contradicts established physics")

        if evidence:
            return {
                "description": "Hallucinated content detected",
                "evidence": evidence
            }

        return None

    def _check_stuck(self, finding: Dict) -> Optional[Dict]:
        """Check if research is stuck but potentially valuable."""

        evidence = []
        suggestions = []

        # Check for multiple failed attempts
        failed_attempts = finding.get("failed_attempts", 0)
        if failed_attempts >= 3:
            evidence.append(f"Failed {failed_attempts} derivation attempts")
            suggestions.append("Try different mathematical approach")

        # Check for circular reasoning
        if finding.get("circular_reasoning"):
            evidence.append("Circular reasoning detected")
            suggestions.append("Break circular dependency")

        # Check for missing information
        if finding.get("missing_data"):
            evidence.append(f"Missing required data: {finding['missing_data']}")
            suggestions.append("Gather additional empirical data")

        # Check for explicit stuck markers
        if finding.get("is_stuck"):
            evidence.append("Derivation reached dead end")

        if finding.get("needs_context"):
            evidence.append("Requires additional context")
            suggestions.append("Pull more context from HECATE catalog")

        # Low confidence despite effort
        confidence = finding.get("confidence", finding.get("hrm_score", 0.0))
        iterations = finding.get("iterations", 0)

        if confidence < 0.5 and iterations > 3:
            evidence.append(f"Low confidence ({confidence:.2f}) after {iterations} iterations")
            suggestions.append("Consider breaking into sub-problems")

        if evidence:
            return {
                "description": "Research stuck - may need different approach",
                "evidence": evidence,
                "suggestions": suggestions if suggestions else [
                    "Try alternative derivation strategy",
                    "Consult additional sources",
                    "Simplify the problem"
                ]
            }

        return None

    def create_banishment_entry(self, finding: Dict, analysis: FailureAnalysis) -> Dict:
        """
        Create a banishment entry for storage in an underworld lake.
        """
        entry = {
            # Core identity
            "id": finding.get("id", "unknown"),
            "name": finding.get("name", finding.get("constant_name", "unknown")),

            # The failed derivation
            "formula": finding.get("formula", ""),
            "attempted_value": finding.get("computed_value", finding.get("z2_prediction")),
            "expected_value": finding.get("experimental_value", finding.get("target_value")),

            # Failure analysis
            "failure_type": analysis.failure_type,
            "severity": analysis.severity,
            "error_description": analysis.error_description,
            "evidence": analysis.evidence,

            # Metrics
            "sigma_tension": analysis.sigma_tension,
            "sycophancy_score": analysis.sycophancy_score,
            "original_hrm_score": finding.get("hrm_score", finding.get("confidence", 0.0)),

            # Recovery info
            "recoverable": analysis.recoverable,
            "recovery_suggestions": analysis.recovery_suggestions,

            # Banishment metadata
            "banished_at": datetime.now().isoformat(),
            "banished_by": "Persephone",
            "destination": analysis.destination.value,

            # Origin
            "origin_lake": "MnemosyneLake",
            "origin_pipeline": finding.get("pipeline_id", ""),
            "original_created_at": finding.get("created_at", finding.get("timestamp", ""))
        }

        return entry

    def generate_lesson_learned(self, finding: Dict, analysis: FailureAnalysis) -> Dict:
        """
        Generate a "lesson learned" from a failure for future training.

        This helps prevent similar mistakes in future derivations.
        """
        lesson = {
            "lesson_id": f"LESSON-{finding.get('id', 'unknown')[:8]}-{datetime.now().strftime('%Y%m%d')}",
            "failure_type": analysis.failure_type,

            "what_was_attempted": finding.get("name", "unknown"),
            "why_it_failed": analysis.error_description,

            "warning_signs": analysis.evidence,

            "how_to_avoid": analysis.recovery_suggestions,

            "related_constants": [
                c for c in finding.get("related_constants", [])
            ],

            "generated_at": datetime.now().isoformat()
        }

        return lesson

    def should_banish(self, finding: Dict) -> bool:
        """
        Quick check if a finding should be banished.

        Returns True if the finding shows clear signs of failure.
        """
        # High sigma tension
        if finding.get("sigma_tension", 0) > self.config.banishment_sigma_threshold:
            return True

        # Marked as sycophantic
        if finding.get("is_sycophantic"):
            return True

        # Marked as hallucination
        if finding.get("is_hallucination"):
            return True

        # Very low HRM score
        if finding.get("hrm_score", finding.get("confidence", 1.0)) < 0.3:
            return True

        # Multiple failed attempts
        if finding.get("failed_attempts", 0) >= 5:
            return True

        return False
