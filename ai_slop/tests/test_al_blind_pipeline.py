#!/usr/bin/env python3
"""
BLIND A_L LENSING TEST - Full OlympusFlow Pipeline
===================================================

This test validates the Two-Lake Architecture by:
1. Simulating "discovered" Planck CMB data (A_L measurement)
2. Running it through the full OlympusFlow pipeline
3. Letting VerificationStage validate against AletheiaLake
4. Checking if the system recognizes the Z² prediction match

The test is BLIND - we do NOT hard-code A_L = 1.18 in the pipeline.
The pipeline should autonomously recognize the match.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from OlympusFlow import Pipeline, PipelineConfig
from OlympusFlow.contracts import Finding, Discovery, VerifiedTruth
from OlympusFlow.stages import AnalysisStage, VerificationStage, StorageStage
from OlympusFlow.events import EventType


def create_simulated_planck_finding():
    """
    Simulate a finding from "Planck CMB Analysis".

    This represents what HermesFlow would discover from real data.
    The A_L value (1.18) comes from actual Planck 2018 results.

    IMPORTANT: The pipeline does NOT know what A_L "should" be.
    It will validate this against AletheiaLake ground truths.
    """
    return Finding(
        finding_id=Finding.generate_id("A_L", "CMB_lensing"),
        domain="cosmology",
        quantity="A_L",
        target_constant="CMB_lensing_amplitude",
        target_value=1.0,  # What LCDM expects
        measured_value=1.18,  # What Planck measured
        measured_uncertainty=0.065,  # Planck uncertainty
        percent_error=18.0,  # 18% excess over LCDM
        sample_size=1000000,  # Planck has millions of CMB pixels
        source_url="https://arxiv.org/abs/1807.06209"
    )


def run_blind_al_test():
    """
    Run the full OlympusFlow pipeline on the A_L anomaly.

    This is an END-TO-END test:
    1. Create simulated Planck finding
    2. Run through VerificationStage (with AletheiaLake)
    3. Check if system recognizes Z² match
    4. Graduate to MnemosyneLake
    """
    print("=" * 70)
    print("BLIND A_L LENSING TEST - Full OlympusFlow Pipeline")
    print("=" * 70)
    print()

    # Create pipeline
    config = PipelineConfig(
        name="al_blind_test",
        topic="CMB lensing anomaly",
        domain="cosmology",
        quantities=["A_L", "lensing_amplitude"],
        max_iterations=1,
        verbose=True
    )

    pipeline = Pipeline("al_blind_test", config)

    # Verify Two-Lake Architecture is active
    print("Two-Lake Architecture Status:")
    print(f"  AletheiaLake: {'ACTIVE' if pipeline.aletheia_lake else 'NOT AVAILABLE'}")
    print(f"  MnemosyneLake: {'ACTIVE' if pipeline.mnemosyne_lake else 'NOT AVAILABLE'}")
    print()

    if pipeline.aletheia_lake:
        # Show what ground truths are available (but NOT the A_L value)
        cosmology_truths = pipeline.aletheia_lake.get_truths_by_domain("cosmology")
        print(f"  Cosmology ground truths in AletheiaLake: {len(cosmology_truths)}")
        for t in cosmology_truths:
            print(f"    - {t.name}: {t.claim[:50]}...")
    print()

    # Create the simulated finding
    print("STEP 1: Simulating Planck CMB Discovery")
    print("-" * 50)
    finding = create_simulated_planck_finding()
    print(f"  Quantity: {finding.quantity}")
    print(f"  Measured: {finding.measured_value} +/- {finding.measured_uncertainty}")
    print(f"  Expected (LCDM): {finding.target_value}")
    print(f"  Excess: {finding.percent_error}%")
    print()

    # Run through VerificationStage
    print("STEP 2: Running VerificationStage with AletheiaLake")
    print("-" * 50)

    verification_stage = VerificationStage(min_hrm=0.7)
    verification_stage.aletheia_lake = pipeline.aletheia_lake  # Connect to AletheiaLake

    from OlympusFlow.contracts import PipelineState
    state = PipelineState(
        pipeline_id="al_blind_test",
        config=config.to_dict()
    )

    # Run verification
    result = verification_stage.run([finding], state)

    print(f"  Verification success: {result.success}")
    print(f"  Truths created: {len(result.output) if result.output else 0}")
    print()

    # Analyze results
    print("STEP 3: Analyzing Results")
    print("-" * 50)

    if result.output:
        for truth in result.output:
            print(f"  Claim: {truth.claim}")
            print(f"  HRM Score: {truth.hrm_score:.3f}")
            print(f"  Status: {truth.status}")
            print(f"  Ground Truth Ref: {truth.ground_truth_ref}")

            # Check if AletheiaLake match was found
            if truth.ground_truth_ref:
                print()
                print("  ** ALETHEIALAKE MATCH DETECTED **")
                al_truth = pipeline.aletheia_lake.get_truth(truth.ground_truth_ref)
                if al_truth:
                    print(f"  Z² Prediction: {al_truth.z2_prediction:.6f}")
                    print(f"  Z² Formula: {al_truth.formula}")

                    # Use experimental uncertainty from AletheiaLake if truth doesn't have it
                    uncertainty = truth.measured_uncertainty or al_truth.experimental_uncertainty or 0.065
                    deviation = abs(truth.measured_value - al_truth.z2_prediction) / uncertainty
                    print(f"  Deviation: {deviation:.3f}σ")

                    if deviation < 1:
                        print("  VERDICT: Z² EXPLAINS THE A_L ANOMALY!")
                    elif deviation < 2:
                        print("  VERDICT: Consistent with Z² prediction")
                    else:
                        print("  VERDICT: Tension with Z² prediction")
    print()

    # Add to MnemosyneLake
    print("STEP 4: Graduating to MnemosyneLake")
    print("-" * 50)

    if result.output and pipeline.mnemosyne_lake:
        from OlympusFlow.lakes.mnemosyne import VerifiedTruth as MnemoTruth

        for truth in result.output:
            if truth.status == "validated":
                mnemosyne_truth = MnemoTruth(
                    truth_id=truth.truth_id,
                    domain=truth.domain,
                    claim=truth.claim,
                    z2_prediction=truth.z2_prediction,
                    measured_value=truth.measured_value,
                    measured_uncertainty=truth.measured_uncertainty,
                    percent_error=truth.percent_error,
                    sigma_deviation=truth.sigma_deviation,
                    hrm_score=truth.hrm_score,
                    data_source=truth.data_source,
                    data_url=truth.data_url,
                    status=truth.status,
                    z2_formula=truth.z2_formula,
                    notes=f"Ground truth: {truth.ground_truth_ref}" if truth.ground_truth_ref else ""
                )
                pipeline.mnemosyne_lake.add_truth(mnemosyne_truth)

        summary = pipeline.mnemosyne_lake.get_session_summary()
        print(f"  Session: {summary['session_id']}")
        print(f"  Truths stored: {summary['total_truths']}")
        print(f"  Validated: {summary['validated_truths']}")

        # Graduate to training
        training_data = pipeline.mnemosyne_lake.graduate_to_training(
            output_path=str(pipeline.output_dir / "al_training.jsonl"),
            min_hrm=0.7
        )
        print(f"  Graduated to training: {len(training_data)}")
    print()

    # Final summary
    print("=" * 70)
    print("BLIND TEST COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  Input: Planck A_L = 1.18 +/- 0.065")
    print(f"  Pipeline: OlympusFlow with Two-Lake Architecture")
    print(f"  AletheiaLake validation: {'YES' if result.output and result.output[0].ground_truth_ref else 'NO'}")

    if result.output and result.output[0].ground_truth_ref:
        al_truth = pipeline.aletheia_lake.get_truth(result.output[0].ground_truth_ref)
        if al_truth:
            print(f"  Z² Prediction: A_L = 1 + 6/Z² = {al_truth.z2_prediction:.6f}")
            deviation = abs(1.18 - al_truth.z2_prediction) / 0.065
            print(f"  Agreement: {deviation:.3f}σ")

            if deviation < 1:
                print()
                print("  RESULT: The A_L 'anomaly' is NOT an anomaly.")
                print("          It is the predicted holographic signature of Z² cosmology.")

    return result


if __name__ == "__main__":
    result = run_blind_al_test()
