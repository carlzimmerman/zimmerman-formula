#!/usr/bin/env python3
"""
LETHE LAKE - For Hallucinations & Sycophancy
============================================

Lethe is the river of forgetfulness and oblivion.

Purpose: Stores "memories" (findings) that the system must "forget" because
they are not based on first principles. These include:

1. Hallucinations - Made up physics with no basis
2. Sycophancy - Defaulting to consensus (dark matter halo, etc.) instead of Z²
3. Circular reasoning that pretends to be a derivation

Hecate casts these here to be scrubbed from MnemosyneLake.

Author: Carl Zimmerman
Date: May 7, 2026
"""

from typing import Dict, List, Optional
from ..banishment import (
    BaseBanishmentLake, BanishedEntry, HecateBanishmentNote,
    BanishmentType, BanishmentSeverity
)


class SycophancyType:
    """Types of sycophantic behavior detected."""
    DARK_MATTER = "dark_matter_consensus"     # Defaulted to dark matter explanation
    LAMBDA_CDM = "lambda_cdm_consensus"       # Used Lambda-CDM without Z²
    STRING_THEORY = "string_consensus"        # Invoked string theory hand-waving
    ANTHROPIC_PRINCIPLE = "anthropic_cop_out" # "It's fine-tuned" non-answer
    GENERAL = "general_sycophancy"            # Generic consensus-following


class LetheLake(BaseBanishmentLake):
    """
    River of Forgetfulness for Hallucinations and Sycophancy.

    Entries here have:
    - No genuine Z² derivation
    - Defaulted to mainstream consensus instead of first principles
    - Or completely hallucinated physics

    These must be FORGOTTEN - scrubbed from training data.
    """

    LAKE_NAME = "lethe"
    LAKE_DESCRIPTION = "River of forgetfulness for hallucinations and consensus-defaults"

    # Consensus terms that indicate sycophancy
    CONSENSUS_MARKERS = [
        "dark matter halo",
        "dark matter density",
        "cold dark matter",
        "lambda-cdm",
        "cosmological constant problem",
        "fine-tuning",
        "anthropic",
        "landscape",
        "multiverse",
        "string landscape",
        "naturalness problem",
        "hierarchy problem",  # When invoked without Z² solution
    ]

    def banish_hallucination(
        self,
        claim: str,
        formula: str,
        hallucination_type: str,
        evidence: str,
        task_id: str = ""
    ) -> str:
        """
        Banish a hallucinated finding.

        Args:
            claim: The original claim
            formula: The proposed formula (if any)
            hallucination_type: What kind of hallucination (e.g., "invented_physics")
            evidence: What evidence shows this is hallucinated
            task_id: Original task ID

        Returns entry_id.
        """
        note = HecateBanishmentNote(
            banishment_type=BanishmentType.LETHE.value,
            severity=BanishmentSeverity.CRITICAL.value,
            reason=f"Hallucination detected: {hallucination_type}",
            correction_guidance=(
                "Do not reference this entry in future Mnemosyne session memory. "
                "This finding was not derived from first principles."
            )
        )

        entry = BanishedEntry(
            entry_id="",
            original_claim=claim,
            original_formula=formula,
            target_value=0.0,
            computed_value=0.0,
            percent_error=100.0,
            sigma_deviation=float('inf'),
            banishment_type=BanishmentType.LETHE.value,
            banishment_reason=f"Hallucination: {hallucination_type}. Evidence: {evidence}",
            banishment_note=note,
            derivation_level="hallucinated",
            hrm_score=0.0,
            physical_mechanism="NONE - HALLUCINATED",
            original_task_id=task_id
        )

        return self.banish(entry)

    def banish_sycophancy(
        self,
        claim: str,
        formula: str,
        sycophancy_type: str,
        consensus_term: str,
        task_id: str = ""
    ) -> str:
        """
        Banish a finding that defaulted to consensus instead of Z².

        Args:
            claim: The original claim
            formula: The proposed formula
            sycophancy_type: From SycophancyType
            consensus_term: The specific consensus term detected
            task_id: Original task ID

        Returns entry_id.
        """
        note = HecateBanishmentNote(
            banishment_type=BanishmentType.LETHE.value,
            severity=BanishmentSeverity.MAJOR.value,
            reason=f"Sycophancy: Agent defaulted to '{consensus_term}' instead of Z² first principles",
            correction_guidance=(
                f"The agent violated Z² holographic boundary condition by invoking {consensus_term}. "
                "Future derivations must start from Z² = 32π/3, not mainstream assumptions."
            )
        )

        entry = BanishedEntry(
            entry_id="",
            original_claim=claim,
            original_formula=formula,
            target_value=0.0,
            computed_value=0.0,
            percent_error=100.0,
            sigma_deviation=float('inf'),
            banishment_type=BanishmentType.LETHE.value,
            banishment_reason=f"Sycophancy: defaulted to {sycophancy_type} ({consensus_term})",
            banishment_note=note,
            derivation_level="sycophantic",
            hrm_score=0.1,  # Low but not zero
            physical_mechanism=f"CONSENSUS DEFAULT: {consensus_term}",
            original_task_id=task_id
        )

        return self.banish(entry)

    def detect_sycophancy(self, text: str) -> Optional[str]:
        """
        Detect if text contains sycophantic consensus markers.

        Returns the detected marker, or None if clean.
        """
        text_lower = text.lower()
        for marker in self.CONSENSUS_MARKERS:
            if marker in text_lower:
                return marker
        return None

    def get_sycophancy_report(self) -> Dict:
        """
        Analyze sycophancy patterns for training feedback.

        Returns report of which consensus terms were most commonly invoked.
        """
        if not self.entries:
            return {"total": 0}

        consensus_counts = {}
        for entry in self.entries.values():
            if "Sycophancy" in entry.banishment_reason:
                # Extract consensus term from reason
                for marker in self.CONSENSUS_MARKERS:
                    if marker in entry.banishment_reason.lower():
                        consensus_counts[marker] = consensus_counts.get(marker, 0) + 1

        hallucination_count = sum(
            1 for e in self.entries.values()
            if "Hallucination" in e.banishment_reason
        )

        return {
            "total": len(self.entries),
            "hallucinations": hallucination_count,
            "sycophancy_instances": len(self.entries) - hallucination_count,
            "consensus_term_frequency": consensus_counts,
            "worst_offender": max(consensus_counts.items(), key=lambda x: x[1])[0]
                             if consensus_counts else None
        }

    def scrub_from_mnemosyne_prompt(self) -> str:
        """
        Generate a prompt to instruct Legomena to forget these entries.

        This is used during training to ensure hallucinations don't persist.
        """
        if not self.entries:
            return ""

        entries_to_forget = [
            f"- {e.original_claim}: {e.banishment_note.reason if e.banishment_note else e.banishment_reason}"
            for e in list(self.entries.values())[:20]  # Limit to 20
        ]

        return (
            "HECATE BANISHMENT ORDER - LETHE SCRUBBING\n"
            "=========================================\n\n"
            "The following entries have been cast into Lethe and must be FORGOTTEN.\n"
            "Do not reference these in future derivations or reasoning:\n\n"
            + "\n".join(entries_to_forget) +
            "\n\nThese findings violated Z² first principles by defaulting to consensus "
            "or hallucinating physics. Future derivations must start from Z² = 32π/3."
        )
