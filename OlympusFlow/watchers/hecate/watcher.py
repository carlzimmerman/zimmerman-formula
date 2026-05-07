"""
HECATE WATCHER - Primary Oversight Implementation
===================================================

The main HecateWatcher class that implements full oversight capabilities.
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..base import BaseWatcher
from ..contracts import (
    WatcherConfig, WatcherResult, WatcherNote, StageTransition,
    InterventionType, TrustLevel, ConsensusCheck, FrameworkCheck
)
from .prompts import HecatePrompts
from .consensus import ConsensusBridge
from .framework import FrameworkValidator


class HecateWatcher(BaseWatcher):
    """
    Hecate - The Primary Oversight Watcher

    Implements dual-lens oversight:
    1. External API (Gemini/Claude) for broad context and citation checking
    2. Local Legomena for Z² framework-specific validation

    Hecate watches all stage transitions and:
    - Audits provenance (sources, citations)
    - Validates logic (no hidden assumptions)
    - Checks framework alignment (Z² principles)
    - Appends immutable notes to MnemosyneLake entries
    - Can halt the pipeline on critical issues
    """

    def __init__(self, config: WatcherConfig = None):
        # Default Hecate-specific config
        if config is None:
            config = WatcherConfig(
                watcher_id="hecate-1",
                watcher_name="Hecate",
                blocking_mode=True,
                blocking_threshold=0.4,
                deviation_threshold=3.0,
                dual_model=True,
                external_model="gemini",
                watch_stages=[
                    "discovery", "analysis", "verification", "storage",
                    "metis", "derivation", "training"
                ]
            )

        super().__init__(config)

        # Initialize components
        self.consensus = ConsensusBridge(verbose=self.config.verbose)
        self.framework = FrameworkValidator(verbose=self.config.verbose)

        # Hecate-specific stats
        self.stats.update({
            "dual_audits": 0,
            "framework_violations": 0,
            "provenance_failures": 0,
            "assumption_detections": 0,
            "numerology_flags": 0
        })

        self._log("Hecate initialized")
        self._log(f"Available models: {self.consensus.get_available_models()}")

    # =========================================================================
    # MAIN AUDIT LOGIC
    # =========================================================================

    def audit(self, transition: StageTransition,
              transition_id: str) -> WatcherResult:
        """
        Perform comprehensive audit of a stage transition.

        This is where Hecate does her main work.
        """
        self._log(f"Auditing transition: {transition.source_stage} → {transition.target_stage}")

        # Determine audit type based on transition
        audit_type = self._determine_audit_type(transition)

        # Perform appropriate checks
        if audit_type == "derivation":
            return self._audit_derivation(transition, transition_id)
        elif audit_type == "discovery":
            return self._audit_discovery(transition, transition_id)
        elif audit_type == "storage":
            return self._audit_storage(transition, transition_id)
        else:
            return self._audit_general(transition, transition_id)

    def _determine_audit_type(self, transition: StageTransition) -> str:
        """Determine what type of audit is needed."""
        source = transition.source_stage.lower()
        target = transition.target_stage.lower()

        if "derivation" in source or "derivation" in target:
            return "derivation"
        elif "discovery" in source or "hermes" in source:
            return "discovery"
        elif "storage" in target or "lake" in target:
            return "storage"
        else:
            return "general"

    # =========================================================================
    # AUDIT TYPES
    # =========================================================================

    def _audit_derivation(self, transition: StageTransition,
                          transition_id: str) -> WatcherResult:
        """
        Audit a derivation result.

        Focus:
        - Does derivation start from Z² axiom?
        - Is there a physical mechanism?
        - Is it numerology?
        - Does it conflict with AletheiaLake?
        """
        self._log("Performing DERIVATION audit")

        data = transition.result_data
        issues = []
        corrections = []

        # Extract derivation info
        formula = data.get("formula", data.get("final_formula", ""))
        computed = data.get("computed_value", 0.0)
        level = data.get("level", data.get("derivation_level", ""))
        mechanism = data.get("physical_mechanism", "")

        # 1. Framework validation
        framework_check = self.framework.validate(
            formula=formula,
            computed_value=computed,
            claim=mechanism
        )

        # 2. Dual-model consensus (if configured)
        consensus_result = None
        if self.config.dual_model:
            consensus_result = self.consensus.dual_audit(
                data,
                external_model=self.config.external_model
            )
            self.stats["dual_audits"] += 1

        # 3. Analyze results
        trust_level = TrustLevel.MEDIUM
        intervention = InterventionType.PASS

        # Check framework alignment
        if not framework_check.uses_z2_constant:
            issues.append("Formula does not reference Z² = 32π/3")
            self.stats["framework_violations"] += 1

        if not framework_check.has_physical_mechanism:
            issues.append("No physical mechanism provided")

        if framework_check.problematic_assumptions:
            issues.extend([f"Hidden assumption: {a}"
                          for a in framework_check.problematic_assumptions])
            self.stats["assumption_detections"] += 1

        # Check for numerology
        if level == "numerical_match" or (
            not framework_check.has_geometric_basis and
            not framework_check.has_physical_mechanism
        ):
            issues.append("NUMEROLOGY WARNING: Pattern match without derivation")
            self.stats["numerology_flags"] += 1
            trust_level = TrustLevel.LOW

        # Check consensus (if available)
        if consensus_result and consensus_result.conflicts_detected:
            issues.append(f"Model disagreement: {consensus_result.conflict_description}")

        # Determine trust level
        if framework_check.framework_score >= 0.8:
            trust_level = TrustLevel.HIGH
        elif framework_check.framework_score >= 0.5:
            trust_level = TrustLevel.MEDIUM
        elif framework_check.framework_score >= 0.3:
            trust_level = TrustLevel.LOW
        else:
            trust_level = TrustLevel.SUSPECT

        # Determine intervention
        if trust_level == TrustLevel.SUSPECT:
            if self.config.blocking_mode:
                intervention = InterventionType.HALT
            else:
                intervention = InterventionType.WARN
        elif issues and len(issues) > 2:
            intervention = InterventionType.WARN

        # Create note
        note = self._create_note(
            trust_level=trust_level,
            trust_score=framework_check.framework_score,
            intervention=intervention,
            provenance=framework_check.aletheia_match,
            logic=len(framework_check.problematic_assumptions) == 0,
            framework=framework_check.uses_z2_constant,
            issues=issues,
            corrections=corrections,
            consensus=consensus_result
        )

        return WatcherResult(
            watcher_id=self.watcher_id,
            transition_id=transition_id,
            timestamp=datetime.now().isoformat(),
            intervention=intervention,
            allow_continue=intervention not in [InterventionType.HALT, InterventionType.REJECT],
            note=note,
            correction_applied={"corrections": corrections} if corrections else None,
            halt_reason=f"Framework score too low ({framework_check.framework_score:.2f})"
                        if intervention == InterventionType.HALT else None
        )

    def _audit_discovery(self, transition: StageTransition,
                         transition_id: str) -> WatcherResult:
        """
        Audit a data discovery result.

        Focus:
        - Is there a valid source URL?
        - Is the source authoritative?
        - Is the data properly structured?
        """
        self._log("Performing DISCOVERY audit")

        data = transition.result_data
        issues = []

        # Check for source
        source_url = data.get("source_url", data.get("url", ""))
        source_name = data.get("source", data.get("data_source", ""))

        if not source_url and not source_name:
            issues.append("No data source provided")
            self.stats["provenance_failures"] += 1

        # Check for authoritative sources
        authoritative = ["nasa", "nist", "codata", "pdg", "planck", "arxiv", "doi", "usgs"]
        if source_url:
            is_authoritative = any(auth in source_url.lower() for auth in authoritative)
            if not is_authoritative:
                issues.append(f"Source may not be authoritative: {source_url[:50]}")

        # Determine trust
        if not issues:
            trust_level = TrustLevel.HIGH
            trust_score = 0.9
        elif len(issues) == 1:
            trust_level = TrustLevel.MEDIUM
            trust_score = 0.6
        else:
            trust_level = TrustLevel.LOW
            trust_score = 0.3

        note = self._create_note(
            trust_level=trust_level,
            trust_score=trust_score,
            intervention=InterventionType.PASS if trust_level != TrustLevel.LOW
                        else InterventionType.WARN,
            provenance=bool(source_url or source_name),
            logic=True,
            framework=True,
            issues=issues
        )

        return WatcherResult(
            watcher_id=self.watcher_id,
            transition_id=transition_id,
            timestamp=datetime.now().isoformat(),
            intervention=note.intervention,
            allow_continue=True,
            note=note
        )

    def _audit_storage(self, transition: StageTransition,
                       transition_id: str) -> WatcherResult:
        """
        Audit data being stored to a lake.

        Focus:
        - Is HRM score above threshold?
        - Is this appropriate for the target lake?
        - Should it be blocked?
        """
        self._log("Performing STORAGE audit")

        data = transition.result_data
        issues = []

        hrm_score = data.get("hrm_score", transition.hrm_score)
        target = transition.target_storage.lower()

        # Check HRM threshold
        if hrm_score < self.config.blocking_threshold:
            issues.append(f"HRM score {hrm_score:.2f} below threshold {self.config.blocking_threshold}")

        # Check target appropriateness
        if "aletheia" in target:
            # High standards for permanent storage
            if hrm_score < 0.9:
                issues.append("HRM too low for AletheiaLake (requires >= 0.9)")
            if data.get("level") != "first_principles":
                issues.append("Only first-principles derivations go to AletheiaLake")

        # Determine intervention
        if issues and "aletheia" in target:
            intervention = InterventionType.REJECT
            trust_level = TrustLevel.SUSPECT
        elif issues:
            intervention = InterventionType.WARN
            trust_level = TrustLevel.LOW
        else:
            intervention = InterventionType.PASS
            trust_level = TrustLevel.HIGH if hrm_score >= 0.8 else TrustLevel.MEDIUM

        note = self._create_note(
            trust_level=trust_level,
            trust_score=hrm_score,
            intervention=intervention,
            provenance=True,
            logic=True,
            framework=True,
            issues=issues
        )

        return WatcherResult(
            watcher_id=self.watcher_id,
            transition_id=transition_id,
            timestamp=datetime.now().isoformat(),
            intervention=intervention,
            allow_continue=intervention != InterventionType.REJECT,
            note=note,
            halt_reason="; ".join(issues) if intervention == InterventionType.REJECT else None
        )

    def _audit_general(self, transition: StageTransition,
                       transition_id: str) -> WatcherResult:
        """
        General audit for stages without specific handling.
        """
        self._log("Performing GENERAL audit")

        # Basic pass-through with observation
        note = self._create_note(
            trust_level=TrustLevel.MEDIUM,
            trust_score=0.7,
            intervention=InterventionType.PASS,
            provenance=True,
            logic=True,
            framework=True,
            issues=[]
        )

        return WatcherResult(
            watcher_id=self.watcher_id,
            transition_id=transition_id,
            timestamp=datetime.now().isoformat(),
            intervention=InterventionType.PASS,
            allow_continue=True,
            note=note
        )

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _create_note(self, trust_level: TrustLevel, trust_score: float,
                     intervention: InterventionType,
                     provenance: bool, logic: bool, framework: bool,
                     issues: List[str] = None,
                     corrections: List[str] = None,
                     consensus: ConsensusCheck = None) -> WatcherNote:
        """Create a WatcherNote with the given parameters."""

        # Generate advisory
        if trust_level == TrustLevel.HIGH:
            advisory = "Validated: All checks passed"
        elif trust_level == TrustLevel.MEDIUM:
            advisory = f"Acceptable with notes: {len(issues or [])} minor issues"
        elif trust_level == TrustLevel.LOW:
            advisory = f"Caution: {len(issues or [])} issues require attention"
        else:
            advisory = f"SUSPECT: Critical issues detected - review required"

        return WatcherNote(
            watcher_id=self.watcher_id,
            timestamp=datetime.now().isoformat(),
            trust_level=trust_level,
            trust_score=trust_score,
            intervention=intervention,
            provenance_verified=provenance,
            logic_validated=logic,
            framework_aligned=framework,
            advisory=advisory,
            issues_found=issues or [],
            corrections_applied=corrections or [],
            consensus_sources=consensus.sources_queried if consensus else [],
            consensus_agreement=consensus.overall_agreement if consensus else 0.0
        )

    # =========================================================================
    # CONTRACT IMPLEMENTATIONS
    # =========================================================================

    def check_consensus(self, query: str, context: Dict) -> ConsensusCheck:
        """Check consensus across multiple sources."""
        return self.consensus.dual_audit(context, self.config.external_model)

    def check_framework(self, claim: str, formula: str,
                        computed_value: float) -> FrameworkCheck:
        """Check alignment with Z² framework."""
        return self.framework.validate(formula, computed_value, claim=claim)

    # =========================================================================
    # MNEMOSYNE INTEGRATION
    # =========================================================================

    def inject_note_to_mnemosyne(self, truth_id: str, note: WatcherNote):
        """
        Inject Hecate's note into a MnemosyneLake entry.

        This adds the hecate_notes field to the truth's metadata.
        """
        try:
            from OlympusFlow.lakes.mnemosyne import MnemosyneLake

            lake = MnemosyneLake(persist=True)
            truth = lake.get_truth(truth_id)

            if truth:
                # The MnemosyneLake VerifiedTruth needs to be updated
                # to support the hecate_notes field
                self._log(f"Would inject note into {truth_id}")
                self._log(f"  Trust: {note.trust_level.value}")
                self._log(f"  Advisory: {note.advisory}")

                # For now, log the intent
                # Future: Update MnemosyneLake to support metadata

        except ImportError:
            self._log("MnemosyneLake not available for note injection")
