#!/usr/bin/env python3
"""
TARTARUS LAKE - For Empirical Failures
======================================

In OlympusFlow hierarchy, Tartarus is the abyss beneath the underworld.

Purpose: Stores findings that are logically sound and follow the Z²
framework, but fail to match empirical evidence (>3σ deviation).

Hecate banishes these here for root cause analysis in the learnings/ folder.

Author: Carl Zimmerman
Date: May 7, 2026
"""

from typing import Dict, List, Optional
from ..banishment import (
    BaseBanishmentLake, BanishedEntry, HecateBanishmentNote,
    BanishmentType, BanishmentSeverity
)


class TartarusLake(BaseBanishmentLake):
    """
    Lake for Empirical Failures.

    Entries here have:
    - Valid Z² framework derivation
    - Physical mechanism proposed
    - But > 3σ deviation from experimental data

    The derivation logic is sound, but nature says "no."
    """

    LAKE_NAME = "tartarus"
    LAKE_DESCRIPTION = "Abyss for empirical failures - logic sound, data doesn't match"

    def banish_empirical_failure(
        self,
        claim: str,
        formula: str,
        target_value: float,
        computed_value: float,
        sigma_deviation: float,
        hrm_score: float = 0.0,
        physical_mechanism: str = "",
        task_id: str = ""
    ) -> str:
        """
        Banish a finding that failed empirically.

        Returns entry_id.
        """
        # Calculate percent error
        if target_value != 0:
            percent_error = abs(computed_value - target_value) / abs(target_value) * 100
        else:
            percent_error = 100.0

        # Determine severity based on deviation
        if sigma_deviation > 10:
            severity = BanishmentSeverity.CRITICAL
        elif sigma_deviation > 5:
            severity = BanishmentSeverity.MAJOR
        else:
            severity = BanishmentSeverity.MINOR

        # Create banishment note
        note = HecateBanishmentNote(
            banishment_type=BanishmentType.TARTARUS.value,
            severity=severity.value,
            reason=f"Empirical deviation: {sigma_deviation:.1f}σ from experimental value",
            correction_guidance=(
                "Analyze why the derivation logic failed to match observation. "
                "Consider: measurement uncertainty, missing physics, or framework limitation."
            )
        )

        # Create entry
        entry = BanishedEntry(
            entry_id="",  # Will be auto-generated
            original_claim=claim,
            original_formula=formula,
            target_value=target_value,
            computed_value=computed_value,
            percent_error=percent_error,
            sigma_deviation=sigma_deviation,
            banishment_type=BanishmentType.TARTARUS.value,
            banishment_reason=f"Empirical failure: {sigma_deviation:.1f}σ deviation",
            banishment_note=note,
            derivation_level="derived",  # It was derived, just wrong
            hrm_score=hrm_score,
            physical_mechanism=physical_mechanism,
            original_task_id=task_id
        )

        return self.banish(entry)

    def get_recoverable(self, max_sigma: float = 5.0) -> List[BanishedEntry]:
        """
        Get entries that might be recoverable with better data or refinement.

        Entries with lower sigma deviation are more likely to be close to truth.
        """
        return [
            e for e in self.entries.values()
            if e.sigma_deviation <= max_sigma
        ]

    def get_recent_failures(self, limit: int = 20) -> List[Dict]:
        """
        Get recent failures for Persephone training harvest.

        Returns entries as dicts with keys expected by PersephoneOrchestrator.
        """
        failures = []
        for entry in list(self.entries.values())[:limit]:
            failures.append({
                "name": entry.original_claim,
                "formula": entry.original_formula,
                "derivation": entry.physical_mechanism,
                "banishment_reason": entry.banishment_reason,
                "sigma_deviation": entry.sigma_deviation,
                "percent_error": entry.percent_error
            })
        return failures

    def analyze_patterns(self) -> Dict:
        """
        Analyze patterns in empirical failures.

        Returns insights about common failure modes.
        """
        if not self.entries:
            return {"total": 0}

        # Group by error magnitude
        small_error = []  # < 1%
        medium_error = []  # 1-10%
        large_error = []  # > 10%

        for entry in self.entries.values():
            if entry.percent_error < 1:
                small_error.append(entry)
            elif entry.percent_error < 10:
                medium_error.append(entry)
            else:
                large_error.append(entry)

        return {
            "total": len(self.entries),
            "small_error_count": len(small_error),
            "medium_error_count": len(medium_error),
            "large_error_count": len(large_error),
            "average_sigma": sum(e.sigma_deviation for e in self.entries.values()) / len(self.entries),
            "potentially_recoverable": len(self.get_recoverable())
        }
