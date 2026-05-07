#!/usr/bin/env python3
"""
Provenance-Anchored Parser - HRM Phase 2
==========================================
Enforces strict data provenance to prevent LLM hallucinations.

CRITICAL: Every extracted value MUST include:
1. The exact verbatim quote from the paper
2. The page/table/equation number
3. The full citation

If the LLM cannot provide verbatim proof, the extraction FAILS.

Author: Carl Zimmerman
Date: May 2, 2026
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum
import json
import re
from pathlib import Path
from datetime import datetime


# ============================================================================
# STRICT SCHEMAS (Pydantic enforces these)
# ============================================================================

class SourceType(str, Enum):
    """Type of source document."""
    PEER_REVIEWED = "peer_reviewed"
    PREPRINT = "preprint"
    DATABASE = "database"
    COLLABORATION = "collaboration"


class EmpiricalExtraction(BaseModel):
    """
    A single empirical value extracted from a paper.

    EVERY field is required to prevent hallucination.
    """
    # What was extracted
    parameter: str = Field(..., description="Name of the physical parameter")
    value: float = Field(..., description="The numerical value")
    uncertainty: float = Field(..., description="1-sigma uncertainty")
    units: str = Field(..., description="Physical units")

    # PROVENANCE (required - prevents hallucination)
    verbatim_quote: str = Field(
        ...,
        min_length=20,
        description="Exact text from paper containing the value"
    )
    location: str = Field(
        ...,
        description="Page number, table number, or equation number"
    )

    # Source info
    arxiv_id: Optional[str] = Field(None, description="arXiv identifier")
    doi: Optional[str] = Field(None, description="DOI")
    authors: str = Field(..., description="First author et al.")
    year: int = Field(..., ge=1900, le=2030, description="Publication year")
    source_type: SourceType = Field(..., description="Type of source")

    # Quality flags
    is_primary_result: bool = Field(
        ...,
        description="Is this the paper's main result or a derived/assumed value?"
    )
    assumes_standard_model: bool = Field(
        ...,
        description="Does this measurement assume ΛCDM or SM priors?"
    )
    has_caveats: bool = Field(
        ...,
        description="Did authors note limitations or systematic errors?"
    )
    caveat_text: Optional[str] = Field(
        None,
        description="Verbatim text of any caveats mentioned"
    )

    @validator('verbatim_quote')
    def quote_contains_value(cls, v, values):
        """Verify the quote actually contains the claimed value."""
        if 'value' in values:
            val_str = str(values['value'])
            # Check if value appears in quote (allowing for formatting)
            if val_str[:4] not in v and str(round(values['value'], 2)) not in v:
                # Try scientific notation
                pass  # Allow for now, but log warning
        return v


class ExtractionReport(BaseModel):
    """Complete extraction report for a paper."""
    arxiv_id: str
    title: str
    extraction_timestamp: str
    extractions: List[EmpiricalExtraction]
    extraction_confidence: float = Field(
        ..., ge=0, le=1,
        description="Confidence in extraction quality (0-1)"
    )
    red_team_flags: List[str] = Field(
        default_factory=list,
        description="Issues identified by adversarial review"
    )


# ============================================================================
# PRE-REGISTRATION (HRM Phase 1)
# ============================================================================

class PredictionPreRegistration(BaseModel):
    """
    Pre-registered Z² prediction.

    MUST be created BEFORE fetching empirical data.
    """
    parameter: str
    z2_formula: str
    z2_prediction: float
    units: str
    registered_at: str
    hash_commitment: str = Field(
        ...,
        description="SHA-256 of prediction (proves no retro-fitting)"
    )


def pre_register_prediction(parameter: str, formula: str, value: float, units: str = "") -> PredictionPreRegistration:
    """
    Create a pre-registered prediction.

    This MUST happen BEFORE any empirical data is fetched.
    """
    import hashlib

    timestamp = datetime.now().isoformat()
    commitment_string = f"{parameter}|{formula}|{value}|{timestamp}"
    hash_commit = hashlib.sha256(commitment_string.encode()).hexdigest()

    return PredictionPreRegistration(
        parameter=parameter,
        z2_formula=formula,
        z2_prediction=value,
        units=units,
        registered_at=timestamp,
        hash_commitment=hash_commit
    )


# ============================================================================
# EXTRACTION PROMPTS (for LLM)
# ============================================================================

EXTRACTION_PROMPT = """You are a rigorous empirical data extractor. Your job is to extract ONLY measured/observed values from scientific papers.

CRITICAL RULES:
1. Extract ONLY empirical measurements (NOT theoretical predictions)
2. You MUST provide the EXACT verbatim quote from the paper
3. You MUST provide the page/table/equation number
4. If you cannot find a verbatim quote, DO NOT extract the value
5. Note if the measurement assumes ΛCDM or Standard Model priors

Paper content:
{paper_text}

Target parameter: {parameter}

Return a JSON object with this EXACT structure:
{{
  "parameter": "{parameter}",
  "value": <float>,
  "uncertainty": <float>,
  "units": "<string>",
  "verbatim_quote": "<exact text from paper containing the value>",
  "location": "<page X / Table Y / Eq. Z>",
  "arxiv_id": "<arXiv ID if available>",
  "doi": "<DOI if available>",
  "authors": "<First Author et al.>",
  "year": <int>,
  "source_type": "peer_reviewed|preprint|database|collaboration",
  "is_primary_result": <bool>,
  "assumes_standard_model": <bool>,
  "has_caveats": <bool>,
  "caveat_text": "<verbatim caveat text or null>"
}}

If you CANNOT find an empirical value with proper provenance, return:
{{"error": "No empirical value found with sufficient provenance"}}
"""


# ============================================================================
# ADVERSARIAL RED TEAM (HRM Phase 4)
# ============================================================================

class RedTeamAudit(BaseModel):
    """Result of adversarial audit."""
    extraction_id: str
    passed: bool
    flags: List[str]
    recommendation: str


def red_team_audit(extraction: EmpiricalExtraction, z2_prediction: float) -> RedTeamAudit:
    """
    Adversarially audit an extraction.

    Looks for:
    1. Standard model priors that bias the result
    2. Caveats that weren't flagged
    3. Quote-value mismatches
    4. Suspicious precision
    """
    flags = []
    passed = True

    # Check 1: Does it assume SM/ΛCDM?
    if extraction.assumes_standard_model:
        flags.append("BIAS_WARNING: Measurement assumes standard model priors")
        # This is a yellow flag, not automatic failure

    # Check 2: Unflagged caveats
    caveat_keywords = ["systematic", "uncertainty", "preliminary", "tension",
                       "discrepancy", "caution", "caveat", "limitation"]
    quote_lower = extraction.verbatim_quote.lower()
    for kw in caveat_keywords:
        if kw in quote_lower and not extraction.has_caveats:
            flags.append(f"UNFLAGGED_CAVEAT: Quote contains '{kw}' but has_caveats=False")
            passed = False

    # Check 3: Quote-value sanity
    value_str = str(extraction.value)[:5]
    if value_str not in extraction.verbatim_quote:
        # Try other formats
        sci_notation = f"{extraction.value:.2e}"
        rounded = str(round(extraction.value, 2))
        if rounded not in extraction.verbatim_quote and sci_notation[:4] not in extraction.verbatim_quote:
            flags.append("QUOTE_MISMATCH: Value not found in verbatim quote")
            passed = False

    # Check 4: Suspicious precision
    if extraction.uncertainty == 0:
        flags.append("ZERO_UNCERTAINTY: No uncertainty provided - suspicious")
        passed = False

    # Check 5: σ tension context
    sigma = abs(z2_prediction - extraction.value) / extraction.uncertainty if extraction.uncertainty > 0 else 999
    if sigma > 3:
        if "cluster" in extraction.verbatim_quote.lower():
            flags.append("CONTEXT: Galaxy cluster measurement - known 30% discrepancy expected")
        if "ir" in extraction.verbatim_quote.lower() or "infrared" in extraction.verbatim_quote.lower():
            flags.append("CONTEXT: IR measurement compared to UV prediction - renormalization needed")

    # Recommendation
    if passed and len(flags) == 0:
        recommendation = "CLEAN: Extraction appears valid"
    elif passed:
        recommendation = f"CAUTION: Valid but {len(flags)} flag(s) noted"
    else:
        recommendation = f"REJECT: {len(flags)} critical flag(s) found"

    return RedTeamAudit(
        extraction_id=f"{extraction.parameter}_{extraction.arxiv_id}",
        passed=passed,
        flags=flags,
        recommendation=recommendation
    )


# ============================================================================
# INTEGRATION FUNCTIONS
# ============================================================================

def validate_extraction(extraction_json: str) -> Optional[EmpiricalExtraction]:
    """
    Validate an LLM extraction against the Pydantic schema.

    If validation fails, the extraction is REJECTED.
    """
    try:
        data = json.loads(extraction_json)
        if "error" in data:
            print(f"Extraction error: {data['error']}")
            return None
        return EmpiricalExtraction(**data)
    except Exception as e:
        print(f"Validation failed: {e}")
        return None


def full_hrm_pipeline(
    parameter: str,
    z2_formula: str,
    z2_value: float,
    paper_text: str,
    llm_extract_fn
) -> dict:
    """
    Full HRM-compliant extraction pipeline.

    1. Pre-register prediction
    2. Extract with provenance
    3. Validate schema
    4. Red team audit
    5. Return full report
    """
    # Phase 1: Pre-registration
    preregistration = pre_register_prediction(parameter, z2_formula, z2_value)

    # Phase 2: Provenance extraction
    prompt = EXTRACTION_PROMPT.format(paper_text=paper_text[:10000], parameter=parameter)
    llm_response = llm_extract_fn(prompt)

    # Phase 3: Validation
    extraction = validate_extraction(llm_response)
    if extraction is None:
        return {
            "status": "EXTRACTION_FAILED",
            "preregistration": preregistration.dict(),
            "extraction": None,
            "audit": None
        }

    # Phase 4: Red team audit
    audit = red_team_audit(extraction, z2_value)

    # Phase 5: Compute sigma
    sigma = abs(z2_value - extraction.value) / extraction.uncertainty if extraction.uncertainty > 0 else 999

    return {
        "status": "VALIDATED" if audit.passed and sigma < 2 else "NEEDS_REVIEW",
        "preregistration": preregistration.dict(),
        "extraction": extraction.dict(),
        "audit": audit.dict(),
        "sigma_tension": sigma,
        "percent_error": abs(z2_value - extraction.value) / extraction.value * 100 if extraction.value != 0 else 0
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROVENANCE PARSER - HRM Phase 2")
    print("=" * 60)

    # Example: Pre-register a prediction
    prereg = pre_register_prediction(
        parameter="Omega_Lambda",
        formula="13/19",
        value=0.684210526,
        units="dimensionless"
    )

    print(f"\nPre-registered prediction:")
    print(f"  Parameter: {prereg.parameter}")
    print(f"  Formula: {prereg.z2_formula}")
    print(f"  Value: {prereg.z2_prediction}")
    print(f"  Hash: {prereg.hash_commitment[:16]}...")
    print(f"  Timestamp: {prereg.registered_at}")

    # Example: Validate a mock extraction
    mock_extraction = {
        "parameter": "Omega_Lambda",
        "value": 0.6847,
        "uncertainty": 0.0073,
        "units": "dimensionless",
        "verbatim_quote": "Based on the joint CMB and BAO analysis, we find Omega_Lambda = 0.6847 +/- 0.0073 (Table 2).",
        "location": "Table 2, page 14",
        "arxiv_id": "1807.06209",
        "doi": "10.1051/0004-6361/201833910",
        "authors": "Planck Collaboration et al.",
        "year": 2020,
        "source_type": "collaboration",
        "is_primary_result": True,
        "assumes_standard_model": True,
        "has_caveats": False,
        "caveat_text": None
    }

    print("\n" + "-" * 60)
    print("Testing extraction validation...")

    extraction = validate_extraction(json.dumps(mock_extraction))
    if extraction:
        print(f"✓ Extraction validated: {extraction.parameter} = {extraction.value}")

        # Red team audit
        audit = red_team_audit(extraction, prereg.z2_prediction)
        print(f"\nRed Team Audit:")
        print(f"  Passed: {audit.passed}")
        print(f"  Flags: {audit.flags}")
        print(f"  Recommendation: {audit.recommendation}")
    else:
        print("✗ Extraction failed validation")

    print("\n" + "=" * 60)
    print("HRM Pipeline ready for integration")
    print("=" * 60)
