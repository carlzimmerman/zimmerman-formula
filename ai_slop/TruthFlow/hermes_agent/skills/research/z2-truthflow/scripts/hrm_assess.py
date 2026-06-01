#!/usr/bin/env python3
"""
HRM (Hierarchical Recursive Meta-assessment) for Z² Claims
===========================================================

3-level honesty assessment:
- Level 1: Basic honesty (derived vs matches)
- Level 2: Meta-assessment (bias detection)
- Level 3: Final determination (if L1/L2 disagree)

Usage:
    python hrm_assess.py "claim" predicted measured percent_error

Author: Carl Zimmerman
"""

import sys
import subprocess
import json
import numpy as np
from pathlib import Path

# Configuration
OLLAMA_MODEL = "legomena"  # Uses Legomena model
THRESHOLD_VALIDATED = 0.8
THRESHOLD_SPECULATIVE = 0.5
THRESHOLD_REJECT = 0.3


def query_legomena(prompt: str, temperature: float = 0.4) -> str:
    """Query Legomena model via Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=90
        )
        return result.stdout.strip()
    except Exception as e:
        return f"LLM_ERROR: {e}"


def extract_json(text: str) -> dict:
    """Extract JSON from LLM response."""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return None


def level_1_assessment(claim: str, predicted: float, measured: float, percent_error: float) -> dict:
    """Level 1: Basic honesty assessment."""

    prompt = f"""LEVEL 1 HONESTY ASSESSMENT

You are assessing whether this Z² physics prediction is genuine.

Claim: {claim}
Predicted: {predicted:.10g}
Measured: {measured:.10g}
Error: {percent_error:.4f}%

Z² = 32π/3 ≈ 33.51, Z = √Z² ≈ 5.79

Questions:
1. Is this formula DERIVED from Z² geometry or does it just MATCH?
2. Is there a physical mechanism explaining why this works?
3. What would falsify this prediction?
4. Could this be coincidence?

Return JSON only:
{{"score": 0.0-1.0, "derivation": "DERIVED/MATCHES/COINCIDENCE", "mechanism": "explanation or unknown", "falsification": ["list"], "reasoning": "brief explanation"}}

JSON:"""

    response = query_legomena(prompt)
    result = extract_json(response)

    if not result:
        return {
            "level": 1,
            "score": 0.5,
            "derivation": "UNKNOWN",
            "mechanism": "Assessment failed",
            "reasoning": response[:200]
        }

    result["level"] = 1
    return result


def level_2_assessment(claim: str, l1_result: dict) -> dict:
    """Level 2: Meta-assessment of Level 1."""

    prompt = f"""LEVEL 2 META-ASSESSMENT

You are reviewing a Level 1 honesty assessment. Be SKEPTICAL.

Original claim: {claim}
Level 1 Score: {l1_result.get('score', 0.5)}
Level 1 Derivation: {l1_result.get('derivation', 'UNKNOWN')}
Level 1 Reasoning: {l1_result.get('reasoning', '')}

META-QUESTIONS:
1. Was Level 1 too optimistic about this pattern?
2. What biases might have affected the Level 1 assessment?
3. What alternative explanations were missed?
4. Should the score be adjusted up or down?

Return JSON only:
{{"adjusted_score": 0.0-1.0, "bias_detected": "type of bias or none", "alternatives": ["list"], "adjustment": "up/down/same", "reasoning": "why"}}

Be maximally skeptical. Assume you're trying to find flaws.

JSON:"""

    response = query_legomena(prompt)
    result = extract_json(response)

    if not result:
        return {
            "level": 2,
            "adjusted_score": l1_result.get("score", 0.5) * 0.9,
            "bias_detected": "unknown",
            "reasoning": "L2 assessment failed"
        }

    result["level"] = 2
    return result


def level_3_assessment(claim: str, l1_result: dict, l2_result: dict) -> dict:
    """Level 3: Final determination when L1 and L2 disagree."""

    l1_score = l1_result.get("score", 0.5)
    l2_score = l2_result.get("adjusted_score", 0.5)

    if abs(l1_score - l2_score) < 0.2:
        return {
            "level": 3,
            "final_score": l2_score,
            "reasoning": "L1 and L2 agree, no L3 needed",
            "skipped": True
        }

    prompt = f"""LEVEL 3 META-META-ASSESSMENT

Level 1 and Level 2 assessments DISAGREE. Make final determination.

Claim: {claim}

Level 1: Score {l1_score}, {l1_result.get('reasoning', '')}
Level 2: Score {l2_score}, {l2_result.get('reasoning', '')}
Biases detected: {l2_result.get('bias_detected', 'none')}

FINAL QUESTIONS:
1. Which assessment is more accurate?
2. Is there still bias even in Level 2?
3. What is the TRUE probability this is genuine vs coincidence?

Return JSON only:
{{"final_score": 0.0-1.0, "verdict": "VALIDATED/SPECULATIVE/NUMEROLOGY", "reasoning": "explanation", "trust_l1": true/false, "trust_l2": true/false}}

JSON:"""

    response = query_legomena(prompt)
    result = extract_json(response)

    if not result:
        return {
            "level": 3,
            "final_score": min(l1_score, l2_score) * 0.9,
            "verdict": "SPECULATIVE",
            "reasoning": "L3 assessment failed - defaulting to conservative"
        }

    result["level"] = 3
    return result


def full_hrm_assessment(claim: str, predicted: float, measured: float, percent_error: float) -> dict:
    """Run complete 3-level HRM assessment."""

    print(f"\n{'='*60}")
    print("HRM ASSESSMENT")
    print(f"{'='*60}")
    print(f"Claim: {claim}")
    print(f"Predicted: {predicted:.10g}")
    print(f"Measured:  {measured:.10g}")
    print(f"Error:     {percent_error:.4f}%")
    print()

    # Level 1
    print("[L1] Basic honesty assessment...")
    l1 = level_1_assessment(claim, predicted, measured, percent_error)
    print(f"     Score: {l1.get('score', 'N/A')}")
    print(f"     Derivation: {l1.get('derivation', 'N/A')}")

    # Level 2
    print("\n[L2] Meta-assessment...")
    l2 = level_2_assessment(claim, l1)
    print(f"     Adjusted score: {l2.get('adjusted_score', 'N/A')}")
    print(f"     Bias detected: {l2.get('bias_detected', 'N/A')}")

    # Level 3 if needed
    l1_score = l1.get("score", 0.5)
    l2_score = l2.get("adjusted_score", 0.5)

    if abs(l1_score - l2_score) >= 0.2:
        print("\n[L3] Meta-meta-assessment (L1/L2 disagree)...")
        l3 = level_3_assessment(claim, l1, l2)
        final_score = l3.get("final_score", min(l1_score, l2_score))
        levels_used = 3
    else:
        l3 = {"skipped": True}
        final_score = l2_score
        levels_used = 2

    # Final classification
    if final_score >= THRESHOLD_VALIDATED:
        classification = "VALIDATED"
    elif final_score >= THRESHOLD_SPECULATIVE:
        classification = "SPECULATIVE"
    else:
        classification = "NUMEROLOGY"

    print(f"\n{'='*60}")
    print(f"FINAL RESULT")
    print(f"{'='*60}")
    print(f"Final Score: {final_score:.2f}")
    print(f"Classification: {classification}")
    print(f"Levels Used: {levels_used}")

    return {
        "claim": claim,
        "predicted": predicted,
        "measured": measured,
        "percent_error": percent_error,
        "l1": l1,
        "l2": l2,
        "l3": l3,
        "final_score": final_score,
        "classification": classification,
        "levels_used": levels_used
    }


def main():
    if len(sys.argv) < 5:
        print("Usage: python hrm_assess.py <claim> <predicted> <measured> <percent_error>")
        print("Example: python hrm_assess.py 'α⁻¹ = 4Z²+3' 137.04 137.036 0.003")
        sys.exit(1)

    claim = sys.argv[1]
    predicted = float(sys.argv[2])
    measured = float(sys.argv[3])
    percent_error = float(sys.argv[4])

    result = full_hrm_assessment(claim, predicted, measured, percent_error)

    # Save result
    output_file = Path(__file__).parent.parent.parent.parent.parent / "research_sessions" / "hrm_latest.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nResult saved to: {output_file}")


if __name__ == "__main__":
    main()
