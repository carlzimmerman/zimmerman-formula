"""
BASE WATCHER - Abstract Base Class for All Watchers
=====================================================

Provides the common interface and utilities that all watchers share.
"""

import json
import hashlib
import time
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable

from .contracts import (
    WatcherConfig, WatcherResult, WatcherNote, StageTransition,
    InterventionType, TrustLevel, ConsensusCheck, FrameworkCheck
)


class BaseWatcher(ABC):
    """
    Abstract base class for all OlympusFlow watchers.

    Watchers observe stage transitions and can:
    1. Audit data for quality and consistency
    2. Add notes to MnemosyneLake entries
    3. Trigger interventions (warn, correct, halt)
    4. Perform consensus checks across models
    5. Validate against Z² framework principles
    """

    def __init__(self, config: WatcherConfig = None):
        self.config = config or WatcherConfig()
        self.watcher_id = self.config.watcher_id

        # Statistics
        self.stats = {
            "transitions_watched": 0,
            "interventions_triggered": 0,
            "corrections_applied": 0,
            "halts_triggered": 0,
            "notes_created": 0,
            "consensus_checks": 0,
            "framework_checks": 0
        }

        # Audit log
        self.audit_log: List[WatcherResult] = []

        # Notes storage
        if self.config.notes_persist:
            self.notes_path = Path(self.config.notes_path) if self.config.notes_path else \
                              Path(__file__).parent / "notes"
            self.notes_path.mkdir(parents=True, exist_ok=True)

        # Callbacks
        self.on_intervention: Optional[Callable] = None
        self.on_halt: Optional[Callable] = None

    def _log(self, msg: str, level: str = "INFO"):
        if self.config.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{self.config.watcher_name} {ts}] [{level}] {msg}")

    def _generate_transition_id(self, transition: StageTransition) -> str:
        """Generate unique ID for a transition."""
        content = f"{transition.pipeline_id}:{transition.task_id}:{transition.source_stage}:{transition.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    # =========================================================================
    # MAIN INTERFACE
    # =========================================================================

    def watch(self, transition: StageTransition) -> WatcherResult:
        """
        Main entry point: watch a stage transition.

        This is called by the pipeline at each stage boundary.
        """
        start_time = time.time()
        self.stats["transitions_watched"] += 1

        transition_id = self._generate_transition_id(transition)

        self._log(f"Watching: {transition.source_stage} → {transition.target_stage}")

        if self.config.log_all_transitions:
            self._log(f"  Data: {json.dumps(transition.result_data, default=str)[:100]}...")

        # Perform the audit
        result = self.audit(transition, transition_id)

        # Update timing
        result.audit_duration_ms = (time.time() - start_time) * 1000

        # Log result
        self.audit_log.append(result)

        # Handle interventions
        if result.intervention != InterventionType.PASS:
            self.stats["interventions_triggered"] += 1
            self._handle_intervention(result, transition)

        # Persist note if configured
        if self.config.notes_persist:
            self._persist_note(transition_id, result.note)

        self.stats["notes_created"] += 1

        return result

    def _handle_intervention(self, result: WatcherResult, transition: StageTransition):
        """Handle non-PASS interventions."""

        if result.intervention == InterventionType.WARN:
            self._log(f"WARNING: {result.note.advisory}", level="WARN")

        elif result.intervention == InterventionType.CORRECT:
            self._log(f"CORRECTION: {result.correction_applied}", level="CORRECT")
            self.stats["corrections_applied"] += 1

        elif result.intervention == InterventionType.HALT:
            self._log(f"HALT: {result.halt_reason}", level="CRITICAL")
            self.stats["halts_triggered"] += 1
            if self.on_halt:
                self.on_halt(result, transition)

        elif result.intervention == InterventionType.ESCALATE:
            self._log(f"ESCALATE to: {result.escalate_to}", level="ESCALATE")

        if self.on_intervention:
            self.on_intervention(result, transition)

    def _persist_note(self, transition_id: str, note: WatcherNote):
        """Persist a watcher note to disk."""
        note_file = self.notes_path / f"{transition_id}.json"
        note_file.write_text(json.dumps(note.to_dict(), indent=2))

    # =========================================================================
    # ABSTRACT METHODS (Subclasses must implement)
    # =========================================================================

    @abstractmethod
    def audit(self, transition: StageTransition, transition_id: str) -> WatcherResult:
        """
        Perform the actual audit of a stage transition.

        Subclasses implement their specific auditing logic here.
        """
        pass

    @abstractmethod
    def check_consensus(self, query: str, context: Dict) -> ConsensusCheck:
        """
        Check consensus across multiple sources/models.
        """
        pass

    @abstractmethod
    def check_framework(self, claim: str, formula: str,
                        computed_value: float) -> FrameworkCheck:
        """
        Check alignment with Z² framework principles.
        """
        pass

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def should_block(self, hrm_score: float, deviation_sigma: float) -> bool:
        """Determine if this transition should be blocked."""
        if not self.config.blocking_mode:
            return False

        if hrm_score < self.config.blocking_threshold:
            return True

        if deviation_sigma > self.config.deviation_threshold:
            return True

        return False

    def get_stats(self) -> Dict:
        """Get watcher statistics."""
        return dict(self.stats)

    def get_recent_audits(self, n: int = 10) -> List[WatcherResult]:
        """Get the N most recent audit results."""
        return self.audit_log[-n:]

    def clear_audit_log(self):
        """Clear the in-memory audit log (notes on disk are preserved)."""
        self.audit_log.clear()
