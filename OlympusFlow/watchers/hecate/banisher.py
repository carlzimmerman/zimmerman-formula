#!/usr/bin/env python3
"""
HECATE BANISHER - Routing Logic for Failed Findings
====================================================

Hecate, goddess of the crossroads, decides which underworld lake
to cast failed findings into:

1. TARTARUS - Empirical failures (logic sound, data doesn't match)
2. LETHE - Hallucinations & sycophancy (consensus defaults)
3. LABYRINTH - Logical dead-ends (stuck but potentially valuable)

Author: Carl Zimmerman
Date: May 7, 2026
"""

from typing import Dict, Optional, Tuple
from enum import Enum

from OlympusFlow.lakes.banishment import BanishmentType, HecateBanishmentNote
from OlympusFlow.lakes.tartarus import TartarusLake
from OlympusFlow.lakes.lethe import LetheLake, SycophancyType
from OlympusFlow.lakes.labyrinth import LabyrinthLake, StuckReason


class FailureClassification(Enum):
    """Classification of why a derivation failed."""
    EMPIRICAL_MISMATCH = "empirical_mismatch"     # Good logic, bad match
    NUMEROLOGY = "numerology"                      # Pattern match, no derivation
    HALLUCINATION = "hallucination"                # Made up physics
    SYCOPHANCY = "sycophancy"                      # Consensus default
    CIRCULAR = "circular"                          # Circular reasoning
    STUCK = "stuck"                                # Couldn't complete
    NO_CONNECTION = "no_connection"                # No Z² path found
    UNKNOWN = "unknown"


class HecateBanisher:
    """
    Hecate's decision engine for banishing failed findings.

    At the crossroads, she examines each failed derivation and decides
    which underworld lake to cast it into based on the failure mode.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        # Initialize the three underworld lakes
        self.tartarus = TartarusLake()
        self.lethe = LetheLake()
        self.labyrinth = LabyrinthLake()

    def _log(self, msg: str):
        if self.verbose:
            print(f"[HecateBanisher] {msg}")

    def classify_failure(self, derivation_result: Dict) -> Tuple[FailureClassification, str]:
        """
        Classify the type of failure from a derivation result.

        Returns (classification, reason_details).
        """
        # Extract key fields
        level = derivation_result.get("level", "")
        status = derivation_result.get("status", "")
        hrm_score = derivation_result.get("hrm_score", 0)
        percent_error = derivation_result.get("percent_error", 100)
        sigma = derivation_result.get("sigma_deviation", 0)
        formula = derivation_result.get("formula", derivation_result.get("final_formula", ""))
        mechanism = derivation_result.get("physical_mechanism", "")

        # Check refinement metadata for classification
        refinement = derivation_result.get("refinement_metadata", {})
        final_verdict = refinement.get("final_verdict", "").upper()
        classification = refinement.get("classification", "").upper()

        # 1. Check for NUMEROLOGY classification
        if "NUMEROLOGY" in final_verdict or "NUMEROLOGY" in classification:
            # Numerology with good accuracy might still be valuable → Labyrinth
            if percent_error < 1.0:
                return (FailureClassification.NUMEROLOGY,
                        f"Pattern match without derivation, but {percent_error:.2f}% accuracy")
            else:
                return (FailureClassification.NUMEROLOGY,
                        "Pattern match without physical mechanism")

        # 2. Check for sycophancy (consensus defaults)
        sycophancy_marker = self.lethe.detect_sycophancy(mechanism)
        if sycophancy_marker:
            return (FailureClassification.SYCOPHANCY,
                    f"Defaulted to consensus term: {sycophancy_marker}")

        # 3. Check for empirical mismatch (good derivation, bad match)
        if level in ["derived", "first_principles"] and sigma > 3.0:
            return (FailureClassification.EMPIRICAL_MISMATCH,
                    f"Derivation logic sound but {sigma:.1f}σ from experiment")

        # 4. Check for no connection found
        if level == "failed" and not formula:
            if hrm_score > 0.4:  # Some potential was seen
                return (FailureClassification.STUCK,
                        "Could not extract formula despite potential connection")
            else:
                return (FailureClassification.NO_CONNECTION,
                        "No Z² connection found")

        # 5. Check for circular reasoning (in falsification field)
        falsification = refinement.get("falsification", "")
        if "circular" in falsification.lower():
            return (FailureClassification.CIRCULAR,
                    f"Circular reasoning detected: {falsification[:100]}")

        # 6. Default based on error magnitude
        if percent_error > 50:
            return (FailureClassification.NO_CONNECTION,
                    f"High error ({percent_error:.0f}%) suggests no real connection")
        elif percent_error > 10:
            return (FailureClassification.EMPIRICAL_MISMATCH,
                    f"Moderate error ({percent_error:.1f}%) - possible framework limitation")
        else:
            return (FailureClassification.UNKNOWN,
                    f"Unclear failure mode (error={percent_error:.2f}%, HRM={hrm_score:.2f})")

    def banish(self, derivation_result: Dict, task_id: str = "") -> Tuple[str, str]:
        """
        Banish a failed derivation to the appropriate underworld lake.

        Returns (lake_name, entry_id).
        """
        # Classify the failure
        classification, details = self.classify_failure(derivation_result)
        self._log(f"Classified as {classification.value}: {details}")

        # Extract common fields
        claim = derivation_result.get("target_constant",
                 derivation_result.get("claim", "Unknown"))
        formula = derivation_result.get("formula",
                  derivation_result.get("final_formula", ""))
        target = derivation_result.get("target_value", 0)
        computed = derivation_result.get("computed_value", 0)
        sigma = derivation_result.get("sigma_deviation", 0)
        hrm = derivation_result.get("hrm_score", 0)
        mechanism = derivation_result.get("physical_mechanism", "")

        # Route to appropriate lake
        if classification == FailureClassification.EMPIRICAL_MISMATCH:
            # → TARTARUS: Good logic, bad match
            entry_id = self.tartarus.banish_empirical_failure(
                claim=claim,
                formula=formula,
                target_value=target,
                computed_value=computed,
                sigma_deviation=sigma,
                hrm_score=hrm,
                physical_mechanism=mechanism,
                task_id=task_id
            )
            self._log(f"Cast into TARTARUS: {entry_id}")
            return ("tartarus", entry_id)

        elif classification == FailureClassification.SYCOPHANCY:
            # → LETHE: Consensus default
            sycophancy_marker = self.lethe.detect_sycophancy(mechanism)
            entry_id = self.lethe.banish_sycophancy(
                claim=claim,
                formula=formula,
                sycophancy_type=SycophancyType.GENERAL,
                consensus_term=sycophancy_marker or "unknown",
                task_id=task_id
            )
            self._log(f"Cast into LETHE: {entry_id}")
            return ("lethe", entry_id)

        elif classification == FailureClassification.HALLUCINATION:
            # → LETHE: Hallucinated physics
            entry_id = self.lethe.banish_hallucination(
                claim=claim,
                formula=formula,
                hallucination_type="invented_physics",
                evidence=details,
                task_id=task_id
            )
            self._log(f"Cast into LETHE: {entry_id}")
            return ("lethe", entry_id)

        elif classification == FailureClassification.NUMEROLOGY:
            # NUMEROLOGY goes to different places based on accuracy
            percent_error = derivation_result.get("percent_error", 100)
            if percent_error < 1.0:
                # Accurate numerology → LABYRINTH (might find derivation later)
                entry_id = self.labyrinth.banish_stuck(
                    claim=claim,
                    formula=formula,
                    stuck_reason=StuckReason.UNDERDETERMINED,
                    details=f"Accurate pattern ({percent_error:.2f}%) but no physical mechanism",
                    partial_progress=f"Formula {formula} matches to {percent_error:.2f}%",
                    needed_to_escape="Physical mechanism connecting Z² to this formula",
                    task_id=task_id
                )
                self._log(f"Cast into LABYRINTH (accurate numerology): {entry_id}")
                return ("labyrinth", entry_id)
            else:
                # Inaccurate numerology → LETHE
                entry_id = self.lethe.banish_hallucination(
                    claim=claim,
                    formula=formula,
                    hallucination_type="numerology_no_basis",
                    evidence=details,
                    task_id=task_id
                )
                self._log(f"Cast into LETHE (numerology): {entry_id}")
                return ("lethe", entry_id)

        elif classification in [FailureClassification.CIRCULAR, FailureClassification.STUCK]:
            # → LABYRINTH: Logical dead-end
            stuck_reason = (StuckReason.CIRCULAR if classification == FailureClassification.CIRCULAR
                           else StuckReason.INTRACTABLE)
            entry_id = self.labyrinth.banish_stuck(
                claim=claim,
                formula=formula,
                stuck_reason=stuck_reason,
                details=details,
                partial_progress=mechanism or "None",
                needed_to_escape="Additional data or alternative approach",
                task_id=task_id
            )
            self._log(f"Cast into LABYRINTH: {entry_id}")
            return ("labyrinth", entry_id)

        else:
            # NO_CONNECTION or UNKNOWN → TARTARUS (default rejection)
            entry_id = self.tartarus.banish_empirical_failure(
                claim=claim,
                formula=formula or "None",
                target_value=target,
                computed_value=computed,
                sigma_deviation=sigma or 999,
                hrm_score=hrm,
                physical_mechanism=mechanism,
                task_id=task_id
            )
            self._log(f"Cast into TARTARUS (default): {entry_id}")
            return ("tartarus", entry_id)

    def get_underworld_report(self) -> Dict:
        """
        Generate a report of all three underworld lakes.
        """
        return {
            "tartarus": self.tartarus.get_statistics(),
            "lethe": self.lethe.get_statistics(),
            "labyrinth": self.labyrinth.get_statistics(),
            "total_banished": (
                len(self.tartarus.entries) +
                len(self.lethe.entries) +
                len(self.labyrinth.entries)
            )
        }

    def hecate_declaration(self, derivation_result: Dict) -> str:
        """
        Generate Hecate's formal banishment declaration.
        """
        classification, details = self.classify_failure(derivation_result)
        claim = derivation_result.get("target_constant",
                 derivation_result.get("claim", "Unknown"))

        lake_map = {
            FailureClassification.EMPIRICAL_MISMATCH: "TARTARUS",
            FailureClassification.NUMEROLOGY: "LETHE or LABYRINTH",
            FailureClassification.HALLUCINATION: "LETHE",
            FailureClassification.SYCOPHANCY: "LETHE",
            FailureClassification.CIRCULAR: "LABYRINTH",
            FailureClassification.STUCK: "LABYRINTH",
            FailureClassification.NO_CONNECTION: "TARTARUS",
            FailureClassification.UNKNOWN: "TARTARUS",
        }

        lake = lake_map.get(classification, "TARTARUS")

        return (
            f"I, HECATE, Goddess of the Crossroads, have examined '{claim}'.\n"
            f"Classification: {classification.value.upper()}\n"
            f"Finding: {details}\n"
            f"It is hereby cast into {lake}.\n"
            f"Do not reference this entry in future Mnemosyne session memory."
        )
