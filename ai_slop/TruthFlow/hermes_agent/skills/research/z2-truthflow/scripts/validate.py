#!/usr/bin/env python3
"""
Z² Prediction Validator with Computational Verification
========================================================

Validates Z² predictions against measurements with triple-verification.

Usage:
    python validate.py "4*Z2 + 3" 137.036 0.000021

Author: Carl Zimmerman
"""

import sys
import numpy as np
import hashlib
import json
from pathlib import Path

# Z² Constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)


def evaluate_formula(formula_str: str) -> float:
    """Safely evaluate a Z² formula string."""
    # Define allowed names
    safe_dict = {
        'Z': Z,
        'Z2': Z2,
        'pi': np.pi,
        'np': np,
        'sqrt': np.sqrt,
        'sin': np.sin,
        'cos': np.cos,
        'exp': np.exp,
        'log': np.log
    }

    try:
        return float(eval(formula_str, {"__builtins__": {}}, safe_dict))
    except Exception as e:
        return None


def triple_verify(formula_str: str) -> tuple:
    """
    Triple verification of a Z² calculation.

    Returns: (value, is_consistent, verification_hash)
    """
    # Method 1: Direct evaluation
    v1 = evaluate_formula(formula_str)

    # Method 2: Explicit Z² substitution
    formula_expanded = formula_str.replace('Z2', '(32 * np.pi / 3)').replace('Z', 'np.sqrt(32 * np.pi / 3)')
    v2 = evaluate_formula(formula_expanded)

    # Method 3: Numerical constants
    formula_numeric = formula_str.replace('Z2', '33.510321638291124').replace('Z', '5.788810699411986')
    v3 = evaluate_formula(formula_numeric)

    if v1 is None or v2 is None or v3 is None:
        return None, False, "EVAL_ERROR"

    # Check consistency
    is_consistent = np.allclose([v1, v2, v3], [v1, v1, v1], rtol=1e-10)

    # Create verification hash
    hash_input = f"{formula_str}:{v1:.15f}"
    verification_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:12]

    return v1, is_consistent, verification_hash


def validate_prediction(formula_str: str, measured: float, uncertainty: float = 0) -> dict:
    """
    Validate a Z² prediction against measurement.

    Returns detailed validation result.
    """
    # Triple verify the calculation
    predicted, is_consistent, verification_hash = triple_verify(formula_str)

    if predicted is None:
        return {
            "status": "ERROR",
            "error": "Could not evaluate formula",
            "formula": formula_str
        }

    if not is_consistent:
        return {
            "status": "VERIFICATION_FAILED",
            "error": "Triple verification failed - calculations inconsistent",
            "formula": formula_str
        }

    # Calculate statistics
    percent_error = abs(predicted - measured) / abs(measured) * 100 if measured != 0 else 0
    sigma = abs(predicted - measured) / uncertainty if uncertainty > 0 else 0

    # Classification
    if uncertainty > 0:
        if sigma < 1:
            classification = "VALIDATED"
        elif sigma < 2:
            classification = "CONSISTENT"
        elif sigma < 3:
            classification = "TENSION"
        else:
            classification = "FAILED"
    else:
        if percent_error < 0.1:
            classification = "PRECISE"
        elif percent_error < 1:
            classification = "CLOSE"
        elif percent_error < 5:
            classification = "APPROXIMATE"
        else:
            classification = "POOR"

    return {
        "status": "SUCCESS",
        "formula": formula_str,
        "predicted": predicted,
        "measured": measured,
        "uncertainty": uncertainty,
        "percent_error": percent_error,
        "sigma": sigma,
        "classification": classification,
        "verification_hash": verification_hash,
        "triple_verified": True
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate.py <formula> <measured> [uncertainty]")
        print("Example: python validate.py '4*Z2 + 3' 137.036 0.000021")
        sys.exit(1)

    formula = sys.argv[1]
    measured = float(sys.argv[2])
    uncertainty = float(sys.argv[3]) if len(sys.argv) > 3 else 0

    result = validate_prediction(formula, measured, uncertainty)

    print(json.dumps(result, indent=2))

    # Also print human-readable summary
    print("\n" + "=" * 50)
    if result["status"] == "SUCCESS":
        print(f"Formula: {result['formula']}")
        print(f"Predicted: {result['predicted']:.10g}")
        print(f"Measured:  {result['measured']:.10g}")
        print(f"Error:     {result['percent_error']:.6f}%")
        if result['sigma'] > 0:
            print(f"Sigma:     {result['sigma']:.2f}σ")
        print(f"Status:    {result['classification']}")
        print(f"Verified:  {result['verification_hash']}")
    else:
        print(f"ERROR: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
