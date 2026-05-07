#!/usr/bin/env python3
"""
SPRING GRADUATOR - Graduation Logic for AletheiaLake
=====================================================

The SpringGraduator manages the "coming to the surface" of validated
findings from MnemosyneLake to AletheiaLake.

Graduation Requirements:
1. HRM score >= 0.80
2. Provenance verified (citation, quote, page number)
3. Passes adversarial review (survives skepticism)
4. Framework-aligned (consistent with Z² principles)

Author: Carl Zimmerman
Date: May 7, 2026
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable

from .orchestrator import GraduationResult, LifecycleDecision, PersephoneConfig


@dataclass
class ProvenanceCheck:
    """Result of checking a finding's provenance."""
    has_source_url: bool = False
    has_citation: bool = False
    has_verbatim_quote: bool = False
    has_page_number: bool = False
    has_doi: bool = False

    score: float = 0.0
    issues: List[str] = None

    def __post_init__(self):
        if self.issues is None:
            self.issues = []

    def to_dict(self) -> Dict:
        return {
            "has_source_url": self.has_source_url,
            "has_citation": self.has_citation,
            "has_verbatim_quote": self.has_verbatim_quote,
            "has_page_number": self.has_page_number,
            "has_doi": self.has_doi,
            "score": self.score,
            "issues": self.issues
        }


class SpringGraduator:
    """
    Manages the graduation of findings to AletheiaLake.

    The Spring phase is when validated truths are "brought to the surface"
    from the working memory of MnemosyneLake to the permanent ground
    truth store of AletheiaLake.
    """

    def __init__(self, config: PersephoneConfig, log_fn: Callable = None):
        self.config = config
        self._log = log_fn or print

        # Z² framework validation
        self.z2_value = 32 * 3.141592653589793 / 3  # Z² = 32π/3

        # Known Z² derivations for validation
        self.known_derivations = {
            "fine_structure_constant_inverse": {
                "formula": "4Z² + 3",
                "value": 137.041286553,
                "tolerance": 0.01
            },
            "weak_mixing_angle": {
                "formula": "3/13",
                "value": 0.230769,
                "tolerance": 0.01
            },
            "dark_energy_fraction": {
                "formula": "13/19",
                "value": 0.684211,
                "tolerance": 0.01
            },
            "matter_density_fraction": {
                "formula": "6/19",
                "value": 0.315789,
                "tolerance": 0.01
            }
        }

    def check_provenance(self, finding: Dict) -> ProvenanceCheck:
        """
        Check the provenance/citation quality of a finding.

        Provenance is critical for graduation - every ground truth
        must have verifiable sources.
        """
        check = ProvenanceCheck()

        # Source URL
        if finding.get("source_url"):
            check.has_source_url = True
        else:
            check.issues.append("Missing source URL")

        # Citation
        citation_fields = ["citation", "reference", "source", "paper"]
        if any(finding.get(f) for f in citation_fields):
            check.has_citation = True
        else:
            check.issues.append("Missing citation/reference")

        # Verbatim quote
        quote_fields = ["verbatim_quote", "quote", "excerpt", "text"]
        if any(finding.get(f) for f in quote_fields):
            check.has_verbatim_quote = True
        else:
            check.issues.append("Missing verbatim quote from source")

        # Page number
        page_fields = ["page_number", "page", "pages", "location"]
        if any(finding.get(f) for f in page_fields):
            check.has_page_number = True

        # DOI
        if finding.get("doi"):
            check.has_doi = True

        # Calculate score
        score = 0.0
        if check.has_source_url:
            score += 0.2
        if check.has_citation:
            score += 0.2
        if check.has_verbatim_quote:
            score += 0.3
        if check.has_page_number:
            score += 0.15
        if check.has_doi:
            score += 0.15

        check.score = min(score, 1.0)

        return check

    def validate_z2_alignment(self, finding: Dict) -> Dict:
        """
        Validate that a finding aligns with Z² framework principles.

        Checks:
        1. Does the formula use Z² correctly?
        2. Does the computed value match experimental?
        3. Is the derivation level appropriate?
        """
        result = {
            "aligned": False,
            "score": 0.0,
            "issues": [],
            "derivation_level": finding.get("derivation_level", "unknown")
        }

        # Check formula
        formula = finding.get("formula", "")
        computed_value = finding.get("computed_value", finding.get("z2_prediction", 0.0))
        experimental_value = finding.get("experimental_value", finding.get("target_value", 0.0))

        if not formula:
            result["issues"].append("No formula provided")
            return result

        # Check if formula references Z² framework
        z2_terms = ["Z²", "Z^2", "Z2", "CUBE", "SPHERE", "GAUGE", "BEKENSTEIN", "N_GEN"]
        has_z2_reference = any(term in formula.upper() for term in z2_terms)

        if not has_z2_reference:
            # Could still be a valid ratio like 3/13
            if "/" in formula:
                # Simple fraction - acceptable
                pass
            else:
                result["issues"].append("Formula doesn't reference Z² framework")

        # Check value accuracy
        if computed_value and experimental_value:
            percent_error = abs(computed_value - experimental_value) / abs(experimental_value) * 100
            result["percent_error"] = percent_error

            if percent_error < 0.1:
                result["score"] = 1.0
            elif percent_error < 1.0:
                result["score"] = 0.8
            elif percent_error < 5.0:
                result["score"] = 0.5
            else:
                result["score"] = 0.2
                result["issues"].append(f"High percent error: {percent_error:.2f}%")

        # Check derivation level
        level = result["derivation_level"]
        if level == "first_principles":
            result["score"] = min(result["score"] + 0.2, 1.0)
        elif level == "phenomenological":
            result["issues"].append("Phenomenological - not first principles")

        result["aligned"] = result["score"] >= 0.6 and len(result["issues"]) == 0

        return result

    def prepare_graduation_entry(self, finding: Dict, result: GraduationResult) -> Dict:
        """
        Prepare a finding for graduation to AletheiaLake.

        Adds graduation metadata and formats for ground truth storage.
        """
        entry = {
            # Core identity
            "id": finding.get("id", result.finding_id),
            "name": result.name,

            # The derivation
            "formula": finding.get("formula", ""),
            "z2_prediction": finding.get("computed_value", finding.get("z2_prediction")),
            "experimental_value": finding.get("experimental_value", finding.get("target_value")),
            "percent_error": finding.get("percent_error", 0.0),

            # Derivation details
            "derivation_level": finding.get("derivation_level", "unknown"),
            "physical_mechanism": finding.get("physical_mechanism", ""),
            "derivation_steps": finding.get("derivation_steps", []),

            # Provenance
            "source_url": finding.get("source_url", ""),
            "citation": finding.get("citation", finding.get("reference", "")),
            "verbatim_quote": finding.get("verbatim_quote", finding.get("quote", "")),
            "page_number": finding.get("page_number", ""),
            "doi": finding.get("doi", ""),

            # Graduation metadata
            "graduated_at": result.graduation_timestamp,
            "graduated_by": "Persephone",
            "hrm_score": result.hrm_score,
            "adversarial_score": result.adversarial_score,
            "provenance_score": result.provenance_score,

            # Adversarial review record
            "adversarial_challenges": result.adversarial_challenges,
            "challenges_passed": result.passed_challenges,
            "challenges_failed": result.failed_challenges,

            # Origin
            "origin_lake": "MnemosyneLake",
            "origin_pipeline": finding.get("pipeline_id", ""),
            "original_discovery_date": finding.get("created_at", finding.get("timestamp", ""))
        }

        return entry

    def check_duplicate(self, finding: Dict, aletheia) -> bool:
        """
        Check if this finding already exists in AletheiaLake.

        Prevents duplicate graduations.
        """
        if not aletheia:
            return False

        existing = aletheia.get_truth_by_name(finding.get("name", ""))
        if existing:
            return True

        # Also check by formula
        formula = finding.get("formula", "")
        if formula:
            all_truths = aletheia.get_all_truths()
            for truth in all_truths:
                if truth.get("formula") == formula:
                    return True

        return False

    def create_graduation_certificate(self, finding: Dict, result: GraduationResult) -> Dict:
        """
        Create a graduation certificate documenting the review process.

        This serves as an audit trail for why this finding was promoted
        to ground truth status.
        """
        certificate = {
            "certificate_id": f"GRAD-{result.finding_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "issued_by": "Persephone",
            "issued_at": datetime.now().isoformat(),

            "finding": {
                "id": result.finding_id,
                "name": result.name,
                "formula": finding.get("formula", "")
            },

            "review_summary": {
                "hrm_score": result.hrm_score,
                "adversarial_score": result.adversarial_score,
                "provenance_score": result.provenance_score
            },

            "adversarial_review": {
                "num_challenges": len(result.adversarial_challenges),
                "passed": result.passed_challenges,
                "failed": result.failed_challenges,
                "challenges": result.adversarial_challenges
            },

            "destination": result.destination_lake,

            "certification_statement": (
                f"This finding has been reviewed by Persephone and meets all "
                f"requirements for graduation to {result.destination_lake}. "
                f"HRM score: {result.hrm_score:.2f}, "
                f"Adversarial survival: {result.adversarial_score:.2f}, "
                f"Provenance quality: {result.provenance_score:.2f}."
            )
        }

        return certificate
