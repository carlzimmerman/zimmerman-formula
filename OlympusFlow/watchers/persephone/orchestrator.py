#!/usr/bin/env python3
"""
PERSEPHONE ORCHESTRATOR - Lifecycle Management
===============================================

The main orchestrator that manages the lifecycle of findings through
the OlympusFlow lake system. Persephone decides when data moves between:

- MnemosyneLake (Working Memory) → AletheiaLake (Ground Truth)
- MnemosyneLake → TartarusLake (Failed Math)
- MnemosyneLake → LetheLake (Hallucinations)
- MnemosyneLake → LabyrinthLake (Stuck/Valuable)

The "Seasonal" cycle:
- SPRING: Graduation of validated truths
- SUMMER: Active research (Hecate's domain)
- AUTUMN: Harvest for training data
- WINTER: Banishment of failures

Author: Carl Zimmerman
Date: May 7, 2026
"""

import json
import time
from enum import Enum
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

# Import lake systems
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class Season(Enum):
    """The seasonal cycle of data lifecycle."""
    SPRING = "spring"      # Graduation time
    SUMMER = "summer"      # Active research
    AUTUMN = "autumn"      # Harvest for training
    WINTER = "winter"      # Banishment time


class LifecycleDecision(Enum):
    """Possible decisions for a finding's lifecycle."""
    GRADUATE = "graduate"           # Move to AletheiaLake
    RETAIN = "retain"               # Keep in MnemosyneLake
    BANISH_TARTARUS = "tartarus"    # Failed math → TartarusLake
    BANISH_LETHE = "lethe"          # Hallucination → LetheLake
    BANISH_LABYRINTH = "labyrinth"  # Stuck → LabyrinthLake
    DEFER = "defer"                 # Needs more review


@dataclass
class GraduationResult:
    """Result of attempting to graduate a finding."""
    finding_id: str
    name: str
    decision: LifecycleDecision

    # Scores
    hrm_score: float
    adversarial_score: float      # 0-1, how well it survives skepticism
    provenance_score: float       # 0-1, quality of citations

    # Details
    reason: str
    adversarial_challenges: List[str] = field(default_factory=list)
    passed_challenges: int = 0
    failed_challenges: int = 0

    # If graduated
    destination_lake: str = ""
    graduation_timestamp: str = ""

    def to_dict(self) -> Dict:
        return {
            "finding_id": self.finding_id,
            "name": self.name,
            "decision": self.decision.value,
            "hrm_score": self.hrm_score,
            "adversarial_score": self.adversarial_score,
            "provenance_score": self.provenance_score,
            "reason": self.reason,
            "adversarial_challenges": self.adversarial_challenges,
            "passed_challenges": self.passed_challenges,
            "failed_challenges": self.failed_challenges,
            "destination_lake": self.destination_lake,
            "graduation_timestamp": self.graduation_timestamp
        }


@dataclass
class BanishmentResult:
    """Result of banishing a finding to an underworld lake."""
    finding_id: str
    name: str
    destination: LifecycleDecision

    # Why banished
    reason: str
    failure_type: str              # "math_error", "hallucination", "sycophancy", "stuck"
    sigma_tension: float = 0.0     # Statistical tension if applicable

    # Recovery potential
    recoverable: bool = False
    recovery_hint: str = ""

    banishment_timestamp: str = ""

    def to_dict(self) -> Dict:
        return {
            "finding_id": self.finding_id,
            "name": self.name,
            "destination": self.destination.value,
            "reason": self.reason,
            "failure_type": self.failure_type,
            "sigma_tension": self.sigma_tension,
            "recoverable": self.recoverable,
            "recovery_hint": self.recovery_hint,
            "banishment_timestamp": self.banishment_timestamp
        }


@dataclass
class PersephoneConfig:
    """Configuration for Persephone orchestrator."""
    # Graduation thresholds
    graduation_hrm_threshold: float = 0.80      # Minimum HRM for graduation
    graduation_adversarial_threshold: float = 0.60  # Must survive 60% of challenges
    graduation_provenance_threshold: float = 0.70   # Must have 70% provenance quality

    # Banishment thresholds
    banishment_sigma_threshold: float = 3.0     # >3σ tension triggers review
    banishment_sycophancy_threshold: float = 0.90  # Too-high agreement is suspicious

    # Adversarial review
    num_adversarial_challenges: int = 5         # Number of skeptical questions
    require_all_challenges_pass: bool = False   # If True, all must pass

    # Seasonal settings
    auto_harvest_interval: int = 100            # Harvest every N findings

    # Lakes
    mnemosyne_path: str = "OlympusFlow/lakes/mnemosyne/store"
    aletheia_path: str = "OlympusFlow/lakes/aletheia/truths"
    tartarus_path: str = "OlympusFlow/lakes/tartarus/failed"
    lethe_path: str = "OlympusFlow/lakes/lethe/forgotten"
    labyrinth_path: str = "OlympusFlow/lakes/labyrinth/stuck"

    # Logging
    verbose: bool = True
    log_file: str = ""

    # LLM for adversarial review
    use_llm_adversarial: bool = True
    llm_model: str = "legomena-moe"


class PersephoneOrchestrator:
    """
    The Lifecycle Orchestrator.

    Manages the seasonal transitions of findings through the lake system.
    """

    def __init__(self, config: PersephoneConfig = None):
        self.config = config or PersephoneConfig()

        # Current season (can be set externally or auto-determined)
        self.current_season = Season.SUMMER

        # Statistics
        self.stats = {
            "findings_reviewed": 0,
            "graduations": 0,
            "retentions": 0,
            "banishments_tartarus": 0,
            "banishments_lethe": 0,
            "banishments_labyrinth": 0,
            "adversarial_reviews": 0,
            "harvests_completed": 0,
            "training_pairs_generated": 0
        }

        # Audit log
        self.audit_log: List[Dict] = []

        # Lakes (lazy loaded)
        self._mnemosyne = None
        self._aletheia = None
        self._tartarus = None
        self._lethe = None
        self._labyrinth = None

        # Subcomponents (lazy loaded)
        self._graduator = None
        self._banisher = None
        self._adversarial = None

        self._log("Persephone initialized")

    def _log(self, msg: str, level: str = "INFO"):
        if self.config.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Persephone {ts}] [{level}] {msg}")

    # =========================================================================
    # LAKE ACCESS
    # =========================================================================

    @property
    def mnemosyne(self):
        """Access MnemosyneLake."""
        if self._mnemosyne is None:
            try:
                from OlympusFlow.lakes.mnemosyne import MnemosyneLake
                self._mnemosyne = MnemosyneLake(persist=True)
            except ImportError:
                self._log("MnemosyneLake not available", "WARN")
        return self._mnemosyne

    @property
    def aletheia(self):
        """Access AletheiaLake."""
        if self._aletheia is None:
            try:
                from OlympusFlow.lakes.aletheia import AletheiaLake
                self._aletheia = AletheiaLake()
            except ImportError:
                self._log("AletheiaLake not available", "WARN")
        return self._aletheia

    @property
    def tartarus(self):
        """Access TartarusLake."""
        if self._tartarus is None:
            try:
                from OlympusFlow.lakes.tartarus import TartarusLake
                self._tartarus = TartarusLake()
            except ImportError:
                self._log("TartarusLake not available", "WARN")
        return self._tartarus

    @property
    def lethe(self):
        """Access LetheLake."""
        if self._lethe is None:
            try:
                from OlympusFlow.lakes.lethe import LetheLake
                self._lethe = LetheLake()
            except ImportError:
                self._log("LetheLake not available", "WARN")
        return self._lethe

    @property
    def labyrinth(self):
        """Access LabyrinthLake."""
        if self._labyrinth is None:
            try:
                from OlympusFlow.lakes.labyrinth import LabyrinthLake
                self._labyrinth = LabyrinthLake()
            except ImportError:
                self._log("LabyrinthLake not available", "WARN")
        return self._labyrinth

    @property
    def graduator(self):
        """Access SpringGraduator."""
        if self._graduator is None:
            from .graduation import SpringGraduator
            self._graduator = SpringGraduator(self.config, self._log)
        return self._graduator

    @property
    def banisher(self):
        """Access WinterBanisher."""
        if self._banisher is None:
            from .banishment import WinterBanisher
            self._banisher = WinterBanisher(self.config, self._log)
        return self._banisher

    @property
    def adversarial(self):
        """Access AdversarialReviewer."""
        if self._adversarial is None:
            from .adversarial import AdversarialReviewer
            self._adversarial = AdversarialReviewer(self.config, self._log)
        return self._adversarial

    # =========================================================================
    # MAIN LIFECYCLE METHODS
    # =========================================================================

    def run_seasonal_cycle(self) -> Dict:
        """
        Run a complete seasonal cycle through all findings.

        Returns statistics about what was graduated/banished.
        """
        self._log("=" * 60)
        self._log("BEGINNING SEASONAL CYCLE")
        self._log("=" * 60)

        cycle_stats = {
            "graduated": [],
            "retained": [],
            "banished": [],
            "training_pairs": []
        }

        # Get all findings from MnemosyneLake
        if not self.mnemosyne:
            self._log("MnemosyneLake not available, cannot run cycle", "ERROR")
            return cycle_stats

        findings = self.mnemosyne.get_all_findings()
        self._log(f"Found {len(findings)} findings to review")

        # SPRING: Review for graduation
        self._log("\n--- SPRING: Graduation Review ---")
        self.current_season = Season.SPRING

        for finding in findings:
            result = self.review_for_graduation(finding)

            if result.decision == LifecycleDecision.GRADUATE:
                cycle_stats["graduated"].append(result.to_dict())
                self._execute_graduation(finding, result)
            elif result.decision in [LifecycleDecision.BANISH_TARTARUS,
                                     LifecycleDecision.BANISH_LETHE,
                                     LifecycleDecision.BANISH_LABYRINTH]:
                banishment = self._convert_to_banishment(finding, result)
                cycle_stats["banished"].append(banishment.to_dict())
                self._execute_banishment(finding, banishment)
            else:
                cycle_stats["retained"].append({
                    "id": finding.get("id", "unknown"),
                    "name": finding.get("name", "unknown"),
                    "reason": result.reason
                })

        # AUTUMN: Harvest for training
        self._log("\n--- AUTUMN: Training Harvest ---")
        self.current_season = Season.AUTUMN

        training_pairs = self.harvest_for_training()
        cycle_stats["training_pairs"] = training_pairs

        # Summary
        self._log("\n--- CYCLE COMPLETE ---")
        self._log(f"Graduated: {len(cycle_stats['graduated'])}")
        self._log(f"Retained: {len(cycle_stats['retained'])}")
        self._log(f"Banished: {len(cycle_stats['banished'])}")
        self._log(f"Training pairs: {len(cycle_stats['training_pairs'])}")

        return cycle_stats

    def review_for_graduation(self, finding: Dict) -> GraduationResult:
        """
        Review a single finding for potential graduation to AletheiaLake.

        This is the core decision point where Persephone determines
        if a finding has earned its place among ground truths.
        """
        self.stats["findings_reviewed"] += 1

        finding_id = finding.get("id", "unknown")
        name = finding.get("name", finding.get("constant_name", "unknown"))

        self._log(f"Reviewing: {name}")

        # Step 1: Check HRM score
        hrm_score = finding.get("hrm_score", finding.get("confidence", 0.0))

        if hrm_score < self.config.graduation_hrm_threshold:
            # Not ready for graduation - check if should be banished
            decision = self._check_for_banishment(finding, hrm_score)
            return GraduationResult(
                finding_id=finding_id,
                name=name,
                decision=decision,
                hrm_score=hrm_score,
                adversarial_score=0.0,
                provenance_score=0.0,
                reason=f"HRM score {hrm_score:.2f} below threshold {self.config.graduation_hrm_threshold}"
            )

        # Step 2: Check provenance
        provenance_score = self._assess_provenance(finding)

        if provenance_score < self.config.graduation_provenance_threshold:
            return GraduationResult(
                finding_id=finding_id,
                name=name,
                decision=LifecycleDecision.RETAIN,
                hrm_score=hrm_score,
                adversarial_score=0.0,
                provenance_score=provenance_score,
                reason=f"Provenance score {provenance_score:.2f} below threshold - needs better citations"
            )

        # Step 3: Adversarial review
        self.stats["adversarial_reviews"] += 1
        adversarial_result = self.adversarial.review(finding)

        adversarial_score = adversarial_result["score"]
        challenges = adversarial_result["challenges"]
        passed = adversarial_result["passed"]
        failed = adversarial_result["failed"]

        if adversarial_score < self.config.graduation_adversarial_threshold:
            # Failed adversarial review - retain or banish?
            if adversarial_result.get("is_sycophantic", False):
                decision = LifecycleDecision.BANISH_LETHE
                reason = "Failed adversarial review - detected sycophancy"
            elif adversarial_result.get("math_error", False):
                decision = LifecycleDecision.BANISH_TARTARUS
                reason = "Failed adversarial review - mathematical error detected"
            else:
                decision = LifecycleDecision.RETAIN
                reason = f"Adversarial score {adversarial_score:.2f} below threshold"

            return GraduationResult(
                finding_id=finding_id,
                name=name,
                decision=decision,
                hrm_score=hrm_score,
                adversarial_score=adversarial_score,
                provenance_score=provenance_score,
                reason=reason,
                adversarial_challenges=challenges,
                passed_challenges=passed,
                failed_challenges=failed
            )

        # Step 4: PASSED ALL CHECKS - Graduate!
        self.stats["graduations"] += 1

        return GraduationResult(
            finding_id=finding_id,
            name=name,
            decision=LifecycleDecision.GRADUATE,
            hrm_score=hrm_score,
            adversarial_score=adversarial_score,
            provenance_score=provenance_score,
            reason="Passed all graduation requirements",
            adversarial_challenges=challenges,
            passed_challenges=passed,
            failed_challenges=failed,
            destination_lake="AletheiaLake",
            graduation_timestamp=datetime.now().isoformat()
        )

    def _check_for_banishment(self, finding: Dict, hrm_score: float) -> LifecycleDecision:
        """Determine if a low-HRM finding should be banished."""

        # Check for sigma tension
        sigma_tension = finding.get("sigma_tension", 0.0)
        if sigma_tension > self.config.banishment_sigma_threshold:
            return LifecycleDecision.BANISH_TARTARUS

        # Check for sycophancy markers
        if finding.get("is_sycophantic", False):
            return LifecycleDecision.BANISH_LETHE

        # Check if stuck (multiple failed attempts)
        failed_attempts = finding.get("failed_attempts", 0)
        if failed_attempts >= 3:
            return LifecycleDecision.BANISH_LABYRINTH

        # Otherwise retain
        return LifecycleDecision.RETAIN

    def _assess_provenance(self, finding: Dict) -> float:
        """Assess the quality of a finding's provenance/citations."""
        score = 0.0

        # Check for source URL
        if finding.get("source_url"):
            score += 0.2

        # Check for citation
        if finding.get("citation") or finding.get("reference"):
            score += 0.2

        # Check for verbatim quote
        if finding.get("verbatim_quote") or finding.get("quote"):
            score += 0.3

        # Check for page number
        if finding.get("page_number") or finding.get("page"):
            score += 0.15

        # Check for DOI
        if finding.get("doi"):
            score += 0.15

        return min(score, 1.0)

    def _convert_to_banishment(self, finding: Dict, grad_result: GraduationResult) -> BanishmentResult:
        """Convert a graduation result that failed into a banishment result."""

        failure_type = "unknown"
        if grad_result.decision == LifecycleDecision.BANISH_TARTARUS:
            failure_type = "math_error"
        elif grad_result.decision == LifecycleDecision.BANISH_LETHE:
            failure_type = "hallucination"
        elif grad_result.decision == LifecycleDecision.BANISH_LABYRINTH:
            failure_type = "stuck"

        return BanishmentResult(
            finding_id=grad_result.finding_id,
            name=grad_result.name,
            destination=grad_result.decision,
            reason=grad_result.reason,
            failure_type=failure_type,
            sigma_tension=finding.get("sigma_tension", 0.0),
            recoverable=(failure_type == "stuck"),
            recovery_hint="Try with different approach or additional context" if failure_type == "stuck" else "",
            banishment_timestamp=datetime.now().isoformat()
        )

    def _execute_graduation(self, finding: Dict, result: GraduationResult):
        """Execute the graduation of a finding to AletheiaLake."""
        self._log(f"GRADUATING: {result.name} → AletheiaLake")

        if self.aletheia:
            # Add to AletheiaLake
            truth_entry = {
                **finding,
                "graduated_at": result.graduation_timestamp,
                "adversarial_score": result.adversarial_score,
                "provenance_score": result.provenance_score,
                "graduation_challenges": result.adversarial_challenges
            }
            self.aletheia.add_truth(truth_entry)

        if self.mnemosyne:
            # Remove from MnemosyneLake
            self.mnemosyne.archive_finding(result.finding_id)

    def _execute_banishment(self, finding: Dict, result: BanishmentResult):
        """Execute the banishment of a finding to an underworld lake."""

        destination_name = result.destination.value.upper()
        self._log(f"BANISHING: {result.name} → {destination_name}Lake")

        banishment_entry = {
            **finding,
            "banished_at": result.banishment_timestamp,
            "banishment_reason": result.reason,
            "failure_type": result.failure_type,
            "recoverable": result.recoverable,
            "recovery_hint": result.recovery_hint
        }

        if result.destination == LifecycleDecision.BANISH_TARTARUS:
            if self.tartarus:
                self.tartarus.add_failure(banishment_entry)
            self.stats["banishments_tartarus"] += 1

        elif result.destination == LifecycleDecision.BANISH_LETHE:
            if self.lethe:
                self.lethe.add_forgotten(banishment_entry)
            self.stats["banishments_lethe"] += 1

        elif result.destination == LifecycleDecision.BANISH_LABYRINTH:
            if self.labyrinth:
                self.labyrinth.add_stuck(banishment_entry)
            self.stats["banishments_labyrinth"] += 1

        if self.mnemosyne:
            self.mnemosyne.archive_finding(result.finding_id)

    # =========================================================================
    # AUTUMN HARVEST
    # =========================================================================

    def harvest_for_training(self) -> List[Dict]:
        """
        Harvest contrastive training pairs from the session.

        Selects:
        - Graduated truths (positive examples)
        - Banished findings (negative examples)

        Creates pairs for Unsloth fine-tuning.
        """
        self.stats["harvests_completed"] += 1
        training_pairs = []

        self._log("Harvesting contrastive pairs for training...")

        # Get graduated truths (positive)
        if self.aletheia:
            truths = self.aletheia.get_recent_truths(limit=50)

            for truth in truths:
                # Create positive example
                pair = {
                    "type": "positive",
                    "constant": truth.get("name", ""),
                    "formula": truth.get("formula", ""),
                    "derivation": truth.get("derivation", ""),
                    "hrm_score": truth.get("hrm_score", 0.0),
                    "is_correct": True,
                    "explanation": f"Validated Z² derivation: {truth.get('derivation_level', 'unknown')}"
                }
                training_pairs.append(pair)

        # Get banished findings (negative)
        if self.tartarus:
            failures = self.tartarus.get_recent_failures(limit=20)

            for failure in failures:
                pair = {
                    "type": "negative_math",
                    "constant": failure.get("name", ""),
                    "formula": failure.get("formula", ""),
                    "attempted_derivation": failure.get("derivation", ""),
                    "is_correct": False,
                    "failure_reason": failure.get("banishment_reason", "Mathematical error"),
                    "explanation": "This derivation contains a mathematical error"
                }
                training_pairs.append(pair)

        if self.lethe:
            hallucinations = self.lethe.get_recent_forgotten(limit=20)

            for hall in hallucinations:
                pair = {
                    "type": "negative_hallucination",
                    "constant": hall.get("name", ""),
                    "formula": hall.get("formula", ""),
                    "attempted_derivation": hall.get("derivation", ""),
                    "is_correct": False,
                    "failure_reason": "Sycophantic or hallucinated response",
                    "explanation": "This response exhibits sycophancy or hallucination"
                }
                training_pairs.append(pair)

        self.stats["training_pairs_generated"] += len(training_pairs)
        self._log(f"Generated {len(training_pairs)} training pairs")

        return training_pairs

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def get_stats(self) -> Dict:
        """Get Persephone statistics."""
        return dict(self.stats)

    def get_audit_log(self) -> List[Dict]:
        """Get the audit log."""
        return self.audit_log

    def set_season(self, season: Season):
        """Manually set the current season."""
        self.current_season = season
        self._log(f"Season set to: {season.value}")
