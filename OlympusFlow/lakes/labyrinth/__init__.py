#!/usr/bin/env python3
"""
LABYRINTH LAKE - For Logical Dead-Ends
======================================

The Labyrinth holds "stuck" tasks that are too complex to be validated
or falsified immediately.

Purpose: Stores findings where:
1. Math hits a singularity that even SymPy cannot simplify
2. Reasoning becomes circular
3. The inquiry is promising but currently intractable
4. Needs additional data (like HECATE catalog) to provide the "thread"

Hecate, as Goddess of the Crossroads, monitors the Labyrinth to see if
new data can provide the "Ariadne's thread" needed to escape.

Author: Carl Zimmerman
Date: May 7, 2026
"""

from typing import Dict, List, Optional
from datetime import datetime
from ..banishment import (
    BaseBanishmentLake, BanishedEntry, HecateBanishmentNote,
    BanishmentType, BanishmentSeverity
)


class StuckReason:
    """Why is this finding stuck in the Labyrinth?"""
    CIRCULAR = "circular_reasoning"           # A depends on B depends on A
    SINGULARITY = "mathematical_singularity"  # Division by zero, infinities
    INTRACTABLE = "computationally_intractable"  # Too complex to solve
    MISSING_DATA = "missing_data"             # Needs specific experimental data
    UNDERDETERMINED = "underdetermined"       # Multiple solutions, can't pick
    CONVERGENCE_FAILURE = "convergence_failure"  # Iterative method didn't converge


class LabyrinthLake(BaseBanishmentLake):
    """
    The Labyrinth for Logical Dead-Ends.

    Entries here are NOT failures in the traditional sense - they're
    promising leads that got stuck. Unlike Tartarus (wrong) or Lethe
    (fake), Labyrinth entries might be TRUE but we can't prove it yet.

    Hecate watches for new information that could provide the
    "Ariadne's thread" to lead these back to productive flow.
    """

    LAKE_NAME = "labyrinth"
    LAKE_DESCRIPTION = "Maze of logical dead-ends - stuck but potentially valuable"

    def banish_stuck(
        self,
        claim: str,
        formula: str,
        stuck_reason: str,
        details: str,
        partial_progress: str = "",
        needed_to_escape: str = "",
        task_id: str = ""
    ) -> str:
        """
        Banish a stuck finding to the Labyrinth.

        Unlike other lakes, Labyrinth entries include information about
        what's needed to "escape" - to continue the derivation.

        Args:
            claim: The original claim
            formula: Partial formula (if any)
            stuck_reason: From StuckReason
            details: What exactly went wrong
            partial_progress: What we DID figure out
            needed_to_escape: What data/insight would help
            task_id: Original task ID

        Returns entry_id.
        """
        # Determine severity - stuck isn't as bad as hallucination
        if stuck_reason in [StuckReason.SINGULARITY, StuckReason.CIRCULAR]:
            severity = BanishmentSeverity.MAJOR
        else:
            severity = BanishmentSeverity.MINOR

        note = HecateBanishmentNote(
            banishment_type=BanishmentType.LABYRINTH.value,
            severity=severity.value,
            reason=f"Logical dead-end: {stuck_reason}. {details}",
            correction_guidance=(
                f"This inquiry became stuck due to {stuck_reason}. "
                f"Partial progress: {partial_progress or 'None recorded'}. "
                f"To escape the Labyrinth: {needed_to_escape or 'Unknown'}."
            )
        )

        entry = BanishedEntry(
            entry_id="",
            original_claim=claim,
            original_formula=formula,
            target_value=0.0,
            computed_value=0.0,
            percent_error=100.0,  # Unknown
            sigma_deviation=0.0,  # Unknown
            banishment_type=BanishmentType.LABYRINTH.value,
            banishment_reason=f"Stuck: {stuck_reason}",
            banishment_note=note,
            derivation_level="stuck",
            hrm_score=0.5,  # Neutral - not wrong, just stuck
            physical_mechanism=partial_progress or "Incomplete",
            original_task_id=task_id,
            # Store escape info in lesson fields
            root_cause=details,
            lesson_learned=f"NEEDED: {needed_to_escape}" if needed_to_escape else ""
        )

        return self.banish(entry)

    def check_for_thread(self, entry_id: str, new_data: Dict) -> bool:
        """
        Check if new data provides the "Ariadne's thread" to escape.

        Args:
            entry_id: The stuck entry to check
            new_data: New information that might help

        Returns True if entry should be re-attempted.
        """
        entry = self.entries.get(entry_id)
        if not entry:
            return False

        # Check if needed data matches what we have
        needed = entry.lesson_learned.replace("NEEDED: ", "")
        if not needed:
            return False

        # Simple keyword matching - could be more sophisticated
        needed_lower = needed.lower()
        for key, value in new_data.items():
            if key.lower() in needed_lower or str(value).lower() in needed_lower:
                # Mark that we found a potential thread
                entry.recovery_attempts += 1
                entry.last_recovery_attempt = datetime.now().isoformat()
                self._save_index()
                return True

        return False

    def get_promising_leads(self) -> List[BanishedEntry]:
        """
        Get entries that are most likely to be resolvable.

        These are stuck entries with:
        - Clear "needed to escape" information
        - Only MINOR severity
        - Some partial progress
        """
        return [
            e for e in self.entries.values()
            if e.lesson_learned and
               e.banishment_note and
               e.banishment_note.severity == BanishmentSeverity.MINOR.value and
               "Incomplete" not in e.physical_mechanism
        ]

    def get_by_stuck_reason(self, reason: str) -> List[BanishedEntry]:
        """Get all entries stuck for a specific reason."""
        return [
            e for e in self.entries.values()
            if reason in e.banishment_reason
        ]

    def generate_research_questions(self) -> List[Dict]:
        """
        Convert stuck entries into research questions for CylleneFlow.

        Each stuck entry represents an open question that could advance
        the Z² framework if solved.
        """
        questions = []

        for entry in self.entries.values():
            needed = entry.lesson_learned.replace("NEEDED: ", "")
            if not needed:
                continue

            questions.append({
                "claim": entry.original_claim,
                "partial_formula": entry.original_formula,
                "stuck_reason": entry.banishment_reason.replace("Stuck: ", ""),
                "research_question": f"What {needed} to complete derivation of {entry.original_claim}?",
                "partial_progress": entry.physical_mechanism,
                "priority": "high" if entry.recovery_attempts == 0 else "medium",
                "entry_id": entry.entry_id
            })

        # Sort by priority
        questions.sort(key=lambda q: 0 if q["priority"] == "high" else 1)
        return questions

    def labyrinth_report(self) -> Dict:
        """
        Generate a report of the Labyrinth status.

        Useful for understanding what's blocking progress.
        """
        if not self.entries:
            return {"total": 0, "message": "Labyrinth is empty"}

        by_reason = {}
        for entry in self.entries.values():
            reason = entry.banishment_reason.replace("Stuck: ", "")
            by_reason[reason] = by_reason.get(reason, 0) + 1

        promising = self.get_promising_leads()

        return {
            "total": len(self.entries),
            "by_stuck_reason": by_reason,
            "promising_leads": len(promising),
            "with_escape_plan": sum(1 for e in self.entries.values() if e.lesson_learned),
            "recovery_attempts": sum(e.recovery_attempts for e in self.entries.values()),
            "research_questions": len(self.generate_research_questions())
        }
