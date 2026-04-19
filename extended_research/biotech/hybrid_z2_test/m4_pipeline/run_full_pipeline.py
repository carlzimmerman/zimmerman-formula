#!/usr/bin/env python3
"""
M4 Full Pipeline: Physics-First Protein Design

SPDX-License-Identifier: AGPL-3.0-or-later

Runs the complete physics-first protein pipeline:
1. ESM-2 structure prediction (Metal MPS)
2. OpenMM thermodynamic validation (OpenCL GPU)
3. Z² resonance filtering (ANM normal modes)

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
from datetime import datetime

# Add pipeline directory to path
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PIPELINE_DIR)

def run_full_pipeline(
    sequence: str,
    name: str = "z2_protein",
    output_dir: str = None
):
    """
    Run complete physics-first protein pipeline.

    Returns combined results from all stages.
    """
    if output_dir is None:
        output_dir = os.path.join(PIPELINE_DIR, "pipeline_output")

    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("M4 PHYSICS-FIRST PROTEIN PIPELINE")
    print("=" * 70)
    print(f"Sequence: {sequence[:50]}..." if len(sequence) > 50 else f"Sequence: {sequence}")
    print(f"Length: {len(sequence)} residues")
    print(f"Output: {output_dir}")
    print("=" * 70)

    results = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "sequence": sequence,
        "length": len(sequence),
        "stages": {}
    }

    # =========================================================================
    # STAGE 1: ESM-2 Structure Prediction
    # =========================================================================
    print("\n" + "=" * 70)
    print("STAGE 1: ESM-2 STRUCTURE PREDICTION")
    print("=" * 70)

    try:
        from m4_esm_predictor import predict_and_validate

        esm_result = predict_and_validate(
            sequence,
            name=name,
            output_dir=os.path.join(output_dir, "esm_prediction"),
            model_name="esm2_t33_650M_UR50D"
        )

        results["stages"]["esm_prediction"] = {
            "status": "success",
            "device": esm_result.get("device", "unknown"),
            "z2_compatible": esm_result.get("z2_geometry", {}).get("z2_compatible", False),
            "mean_contacts": esm_result.get("z2_geometry", {}).get("mean_contacts", 0),
            "pdb_path": os.path.join(output_dir, "esm_prediction", f"{name}_esm.pdb")
        }

        pdb_path = results["stages"]["esm_prediction"]["pdb_path"]
        print(f"\n✓ Stage 1 complete: {pdb_path}")

    except Exception as e:
        print(f"\n✗ Stage 1 failed: {e}")
        results["stages"]["esm_prediction"] = {"status": "failed", "error": str(e)}
        results["overall_status"] = "failed_stage_1"
        save_results(results, output_dir)
        return results

    # =========================================================================
    # STAGE 2: OpenMM Thermodynamic Validation
    # =========================================================================
    print("\n" + "=" * 70)
    print("STAGE 2: OPENMM THERMODYNAMIC VALIDATION")
    print("=" * 70)

    try:
        from m4_openmm_thermodynamics import validate_structure

        openmm_result = validate_structure(
            pdb_path,
            output_dir=os.path.join(output_dir, "openmm_validation"),
            temperature=310.0,
            equilibration_steps=2000,
            production_steps=5000
        )

        is_stable = openmm_result.get("thermodynamically_stable", False)

        results["stages"]["openmm_validation"] = {
            "status": "success" if openmm_result.get("status") == "completed" else "failed",
            "platform": openmm_result.get("platform", "unknown"),
            "model_type": openmm_result.get("model_type", "unknown"),
            "thermodynamically_stable": is_stable,
            "equilibration": openmm_result.get("equilibration", {}),
            "thermodynamics": openmm_result.get("thermodynamics", {})
        }

        if not is_stable:
            print("\n⚠ Structure is not thermodynamically stable")
        else:
            print("\n✓ Stage 2 complete: Structure is thermodynamically stable")

    except Exception as e:
        print(f"\n✗ Stage 2 failed: {e}")
        import traceback
        traceback.print_exc()
        results["stages"]["openmm_validation"] = {"status": "failed", "error": str(e)}
        # Continue to stage 3 even if stage 2 fails

    # =========================================================================
    # STAGE 3: Z² Resonance Filtering
    # =========================================================================
    print("\n" + "=" * 70)
    print("STAGE 3: Z² RESONANCE FILTERING")
    print("=" * 70)

    try:
        from m4_z2_resonance_selector import Z2ResonanceSelector

        selector = Z2ResonanceSelector(
            alignment_threshold=2.0,  # Adjusted for realistic proteins
            p_value_threshold=0.01
        )

        z2_result = selector.evaluate_pdb(pdb_path)

        passes_core = z2_result.get("verdict", {}).get("passes_core", False)

        results["stages"]["z2_resonance"] = {
            "status": "success",
            "alignment_ratio": z2_result.get("z2_analysis", {}).get("alignment_ratio", 0),
            "z2_score": z2_result.get("z2_analysis", {}).get("z2_score", 0),
            "pearson_r": z2_result.get("z2_analysis", {}).get("pearson_r", 0),
            "p_value": z2_result.get("z2_analysis", {}).get("p_value", 1.0),
            "passes_core": passes_core,
            "recommendation": z2_result.get("verdict", {}).get("recommendation", "unknown")
        }

        print(f"\n✓ Stage 3 complete")
        print(f"  Z² alignment: {results['stages']['z2_resonance']['alignment_ratio']:.1f}×")
        print(f"  Pearson r: {results['stages']['z2_resonance']['pearson_r']:.4f}")
        print(f"  p-value: {results['stages']['z2_resonance']['p_value']:.2e}")
        print(f"  Verdict: {results['stages']['z2_resonance']['recommendation']}")

    except Exception as e:
        print(f"\n✗ Stage 3 failed: {e}")
        import traceback
        traceback.print_exc()
        results["stages"]["z2_resonance"] = {"status": "failed", "error": str(e)}

    # =========================================================================
    # FINAL VERDICT
    # =========================================================================
    print("\n" + "=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)

    # Determine overall status
    esm_ok = results["stages"].get("esm_prediction", {}).get("status") == "success"
    openmm_ok = results["stages"].get("openmm_validation", {}).get("thermodynamically_stable", False)
    z2_ok = results["stages"].get("z2_resonance", {}).get("passes_core", False)

    if esm_ok and openmm_ok and z2_ok:
        overall = "PASSED"
        verdict = "Structure is physically viable with Z² resonance"
    elif esm_ok and openmm_ok:
        overall = "PARTIAL"
        verdict = "Thermodynamically stable but Z² alignment below threshold"
    elif esm_ok:
        overall = "UNSTABLE"
        verdict = "Structure predicted but thermodynamically unstable"
    else:
        overall = "FAILED"
        verdict = "Pipeline failed at structure prediction"

    results["overall_status"] = overall
    results["verdict"] = verdict

    print(f"\nStage 1 (ESM-2):    {'✓' if esm_ok else '✗'}")
    print(f"Stage 2 (OpenMM):   {'✓' if openmm_ok else '✗'}")
    print(f"Stage 3 (Z²):       {'✓' if z2_ok else '✗'}")
    print(f"\nOverall: {overall}")
    print(f"Verdict: {verdict}")

    # Save results
    save_results(results, output_dir)

    return results


def save_results(results: dict, output_dir: str):
    """Save pipeline results to JSON."""
    output_path = os.path.join(output_dir, "pipeline_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n✓ Results saved to: {output_path}")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    # Test sequence: Human serum albumin fragment (first 80 residues)
    # This is a real protein sequence for realistic testing
    TEST_SEQUENCE = (
        "MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPF"
        "DEHVKLVNELTEFAKTCVADE"
    )

    print("\n" + "=" * 70)
    print("RUNNING FULL M4 PHYSICS-FIRST PIPELINE")
    print("=" * 70)
    print(f"\nTest: Human serum albumin fragment")
    print(f"Length: {len(TEST_SEQUENCE)} residues")

    results = run_full_pipeline(
        TEST_SEQUENCE,
        name="hsa_fragment",
        output_dir=os.path.join(PIPELINE_DIR, "pipeline_output")
    )

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
