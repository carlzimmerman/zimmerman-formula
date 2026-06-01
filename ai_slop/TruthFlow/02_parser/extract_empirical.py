#!/usr/bin/env python3
"""
TruthFlow Parser - Extract Empirical Data Only
===============================================
Uses LLM to extract ONLY measured values (no theory).

The key insight from LegomenaLLM: Train the parser to
recognize the difference between:
- Empirical: "We measured Ω_Λ = 0.685 ± 0.007"
- Theoretical: "Our model predicts Ω_Λ = 0.7"

We ONLY trust the empirical values.

Author: Carl Zimmerman
Date: May 2, 2026
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
from pathlib import Path

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class EmpiricalValue:
    """A single empirical measurement extracted from a paper."""
    quantity: str           # e.g., "Omega_Lambda", "alpha_inverse"
    value: float            # Central value
    uncertainty: float      # 1-sigma uncertainty
    units: str              # Units (if any)
    source: str             # Paper arXiv ID
    context: str            # Surrounding text
    confidence: str         # "high", "medium", "low" (extraction confidence)


@dataclass
class ExtractionResult:
    """Results of extracting empirical data from a paper."""
    arxiv_id: str
    title: str
    extracted_values: List[EmpiricalValue]
    raw_abstract: str
    extraction_notes: str


# ============================================================================
# EXTRACTION PATTERNS
# ============================================================================

# Patterns for quantities we care about (Z² predictions)
QUANTITY_PATTERNS = {
    "Omega_Lambda": [
        r"Ω[_Λ]?\s*=\s*([\d.]+)\s*±\s*([\d.]+)",
        r"Omega[_\s]?Lambda\s*=\s*([\d.]+)\s*±\s*([\d.]+)",
        r"dark energy density.*?([\d.]+)\s*±\s*([\d.]+)",
    ],
    "Omega_m": [
        r"Ω[_m]?\s*=\s*([\d.]+)\s*±\s*([\d.]+)",
        r"matter density.*?([\d.]+)\s*±\s*([\d.]+)",
    ],
    "alpha_inverse": [
        r"α\^?\{?-1\}?\s*=\s*([\d.]+)\s*±?\s*([\d.]*)",
        r"1/α\s*=\s*([\d.]+)",
        r"fine.?structure.*?137\.([\d]+)",
    ],
    "sin2_theta_W": [
        r"sin\^?2\s*θ[_W]?\s*=\s*([\d.]+)\s*±\s*([\d.]+)",
        r"weak mixing angle.*?([\d.]+)\s*±\s*([\d.]+)",
    ],
    "H0": [
        r"H[_0]?\s*=\s*([\d.]+)\s*±\s*([\d.]+)\s*km",
        r"Hubble constant.*?([\d.]+)\s*±\s*([\d.]+)",
    ],
    "a0_mond": [
        r"a[_0]?\s*=\s*([\d.eE+-]+)\s*m/s",
        r"MOND.*?acceleration.*?([\d.eE+-]+)",
    ],
    "tensor_scalar_r": [
        r"r\s*[<>=]\s*([\d.]+)",
        r"tensor.to.scalar.*?([\d.]+)",
    ],
}

# Keywords that indicate EMPIRICAL (measurement) vs THEORETICAL (model)
EMPIRICAL_KEYWORDS = [
    "measured", "observed", "detected", "found", "data",
    "experiment", "survey", "measurement", "constraint",
    "95% CL", "68% CL", "σ", "uncertainty", "error",
    "Planck 2018", "Planck 2020", "PDG", "CODATA",
    "SPARC", "THINGS", "LITTLE THINGS", "DiskMass",
]

THEORETICAL_KEYWORDS = [
    "predict", "model", "theory", "calculate", "derive",
    "assume", "postulate", "propose", "suggest", "expect",
    "ΛCDM", "standard model", "our framework", "we find that",
]


# ============================================================================
# EXTRACTION FUNCTIONS
# ============================================================================

def is_empirical_context(context: str) -> Tuple[bool, str]:
    """
    Determine if a context indicates empirical measurement or theory.

    Returns: (is_empirical, confidence)
    """
    context_lower = context.lower()

    empirical_score = sum(1 for kw in EMPIRICAL_KEYWORDS if kw.lower() in context_lower)
    theoretical_score = sum(1 for kw in THEORETICAL_KEYWORDS if kw.lower() in context_lower)

    if empirical_score > theoretical_score + 1:
        return True, "high"
    elif empirical_score > theoretical_score:
        return True, "medium"
    elif theoretical_score > empirical_score:
        return False, "high"
    else:
        return True, "low"  # Default to empirical but low confidence


def extract_value(text: str, quantity: str) -> List[EmpiricalValue]:
    """
    Extract values for a specific quantity from text.
    """
    values = []
    patterns = QUANTITY_PATTERNS.get(quantity, [])

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Get context (surrounding 200 chars)
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end]

            # Check if empirical
            is_emp, confidence = is_empirical_context(context)
            if not is_emp:
                continue  # Skip theoretical values

            # Extract value and uncertainty
            groups = match.groups()
            try:
                value = float(groups[0]) if groups[0] else 0.0
                uncertainty = float(groups[1]) if len(groups) > 1 and groups[1] else 0.0
            except (ValueError, IndexError):
                continue

            values.append(EmpiricalValue(
                quantity=quantity,
                value=value,
                uncertainty=uncertainty,
                units="",  # Would need more parsing
                source="",  # Set by caller
                context=context,
                confidence=confidence
            ))

    return values


def extract_from_abstract(abstract: str, arxiv_id: str) -> List[EmpiricalValue]:
    """
    Extract all empirical values from a paper abstract.
    """
    all_values = []

    for quantity in QUANTITY_PATTERNS:
        values = extract_value(abstract, quantity)
        for v in values:
            v.source = arxiv_id
        all_values.extend(values)

    return all_values


def process_fetched_papers(input_dir: str) -> List[ExtractionResult]:
    """
    Process all fetched papers and extract empirical values.
    """
    results = []
    input_path = Path(input_dir)

    for json_file in input_path.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

        for paper in data.get("papers", []):
            values = extract_from_abstract(
                paper["abstract"],
                paper["arxiv_id"]
            )

            result = ExtractionResult(
                arxiv_id=paper["arxiv_id"],
                title=paper["title"],
                extracted_values=values,
                raw_abstract=paper["abstract"],
                extraction_notes=f"Extracted {len(values)} empirical values"
            )
            results.append(result)

    return results


def save_extractions(results: List[ExtractionResult], output_dir: str):
    """Save extraction results."""
    os.makedirs(output_dir, exist_ok=True)

    # Group by quantity for easy validation
    by_quantity = {}
    for result in results:
        for value in result.extracted_values:
            if value.quantity not in by_quantity:
                by_quantity[value.quantity] = []
            by_quantity[value.quantity].append(asdict(value))

    # Save per-quantity files
    for quantity, values in by_quantity.items():
        filepath = os.path.join(output_dir, f"{quantity}_empirical.json")
        with open(filepath, "w") as f:
            json.dump({
                "quantity": quantity,
                "count": len(values),
                "values": values
            }, f, indent=2)
        print(f"Saved {len(values)} values for {quantity}")

    # Save full extraction results
    all_results = [asdict(r) for r in results]
    with open(os.path.join(output_dir, "all_extractions.json"), "w") as f:
        json.dump(all_results, f, indent=2)


# ============================================================================
# LLM-ENHANCED EXTRACTION (Future)
# ============================================================================

EXTRACTION_PROMPT = """
You are an empirical data extractor. Your job is to extract ONLY measured/observed
values from scientific papers. Do NOT extract theoretical predictions or model outputs.

Given this paper abstract, extract any measured values for:
- Ω_Λ (dark energy density)
- Ω_m (matter density)
- α⁻¹ (inverse fine structure constant)
- sin²θ_W (weak mixing angle)
- H₀ (Hubble constant)
- a₀ (MOND acceleration scale)
- r (tensor-to-scalar ratio)

For each value, provide:
1. The quantity name
2. The central value
3. The uncertainty (if given)
4. Whether this is DEFINITELY empirical (measurement, observation, constraint)

ABSTRACT:
{abstract}

Return JSON with format:
{{
  "values": [
    {{"quantity": "Omega_Lambda", "value": 0.685, "uncertainty": 0.007, "is_empirical": true}}
  ]
}}
"""


def extract_with_llm(abstract: str, arxiv_id: str) -> List[EmpiricalValue]:
    """
    Use LLM for more sophisticated extraction.
    This is a placeholder - would integrate with actual LLM API.
    """
    # For now, fall back to regex extraction
    # In production, would call OpenAI/Anthropic/local LLM
    return extract_from_abstract(abstract, arxiv_id)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TRUTHFLOW PARSER - Empirical Data Extraction")
    print("=" * 60)
    print()
    print("This parser extracts ONLY empirical measurements.")
    print("Theoretical predictions are filtered out.")
    print()

    input_dir = os.path.join(os.path.dirname(__file__), "..", "fetched_papers")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "extracted_data")

    # Check if input exists
    if not os.path.exists(input_dir):
        print(f"No fetched papers found at {input_dir}")
        print("Run 01_fetcher/fetch_arxiv.py first.")
        exit(1)

    # Process papers
    results = process_fetched_papers(input_dir)
    print(f"\nProcessed {len(results)} papers")

    # Count extractions
    total_values = sum(len(r.extracted_values) for r in results)
    print(f"Extracted {total_values} empirical values")

    # Save results
    save_extractions(results, output_dir)

    print(f"\nResults saved to: {output_dir}")
    print("Next step: Run 03_compute to validate Z² predictions")
