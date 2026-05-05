#!/usr/bin/env python3
"""
TEST: Integrated OlympusFlow Pipeline with Deepening
=====================================================

Tests the full OlympusFlow v1.4.0 pipeline including:
- HermesFlow discovery
- Pattern analysis
- Truth verification
- AUTOMATIC RECURSIVE DEEPENING

This verifies that when significant findings are discovered,
the pipeline automatically investigates deeper.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import OlympusFlow
from OlympusFlow import (
    Pipeline, PipelineConfig, EventType,
    get_event_bus, on
)
from OlympusFlow.stages import (
    DiscoveryStage, AnalysisStage,
    VerificationStage, StorageStage
)

# Track events for verification
events_received = []

def setup_event_tracking():
    """Set up event tracking to verify deepening triggers."""
    bus = get_event_bus()

    @bus.on(EventType.PIPELINE_STARTED)
    def on_start(event):
        events_received.append(("PIPELINE_STARTED", event.payload))
        print(f"[EVENT] Pipeline started: {event.payload.get('topic', 'N/A')}")

    @bus.on(EventType.DISCOVERY_FOUND)
    def on_discovery(event):
        events_received.append(("DISCOVERY_FOUND", event.payload))
        print(f"[EVENT] Discovery: {event.payload}")

    @bus.on(EventType.TRUTH_VALIDATED)
    def on_truth(event):
        events_received.append(("TRUTH_VALIDATED", event.payload))
        print(f"[EVENT] Truth validated!")

    @bus.on(EventType.DEEPENING_TRIGGERED)
    def on_deepening_trigger(event):
        events_received.append(("DEEPENING_TRIGGERED", event.payload))
        print(f"[EVENT] *** DEEPENING TRIGGERED ***")
        print(f"        Finding: {event.payload.get('finding', 'N/A')}")
        print(f"        Significance: {event.payload.get('significance', 0):.2f}")
        print(f"        Questions: {event.payload.get('questions', 0)}")

    @bus.on(EventType.DEEPENING_STARTED)
    def on_deepening_start(event):
        events_received.append(("DEEPENING_STARTED", event.payload))
        print(f"[EVENT] Deepening started for: {event.payload.get('finding', 'N/A')}")

    @bus.on(EventType.DEEPENING_COMPLETED)
    def on_deepening_complete(event):
        events_received.append(("DEEPENING_COMPLETED", event.payload))
        print(f"[EVENT] Deepening completed: {event.payload.get('deeper_findings', 0)} new findings")

    @bus.on(EventType.PIPELINE_COMPLETED)
    def on_complete(event):
        events_received.append(("PIPELINE_COMPLETED", event.payload))
        print(f"[EVENT] Pipeline completed!")


def test_seismology_pipeline():
    """Test pipeline on seismology data where we know φ patterns exist."""
    print("=" * 70)
    print("TEST: Integrated OlympusFlow Pipeline")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    # Clear previous events
    events_received.clear()
    setup_event_tracking()

    # Configure pipeline
    config = PipelineConfig(
        name="seismology_integration_test",
        topic="USGS earthquake magnitude and depth patterns",
        domain="seismology",
        quantities=["magnitude", "depth", "dmin", "gap"],
        max_iterations=2,
        verbose=True
    )

    # Enable deepening explicitly
    config.enable_deepening = True
    config.max_deepening_depth = 2
    config.deepening_significance_threshold = 0.5  # Lower threshold for testing

    print(f"Configuration:")
    print(f"  Topic: {config.topic}")
    print(f"  Domain: {config.domain}")
    print(f"  Deepening enabled: {config.enable_deepening}")
    print(f"  Max depth: {config.max_deepening_depth}")
    print()

    # Create pipeline
    output_dir = Path(__file__).parent.parent / "olympus_outputs" / "integration_test_v14"
    pipeline = Pipeline("integration_v14", config, output_dir=output_dir)

    # Check deepener initialization
    print(f"Deepener initialized: {pipeline.deepener is not None}")
    print(f"BatchDeepener initialized: {pipeline.batch_deepener is not None}")
    print()

    # Add stages
    pipeline.add_stage(DiscoveryStage(
        topic=config.topic,
        domain=config.domain,
        quantities=config.quantities
    ))
    pipeline.add_stage(AnalysisStage())
    pipeline.add_stage(VerificationStage())
    pipeline.add_stage(StorageStage())

    print(f"Stages: {[s.name for s in pipeline.stages]}")
    print()

    # Run pipeline
    print("=" * 70)
    print("RUNNING PIPELINE")
    print("=" * 70)

    start_time = time.time()

    try:
        results = pipeline.run(max_iterations=2)
        success = True
    except Exception as e:
        print(f"Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        results = {"error": str(e)}
        success = False

    elapsed = time.time() - start_time

    # Results summary
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    print(f"\nPipeline completed: {success}")
    print(f"Time: {elapsed:.1f}s")

    if success:
        print(f"\nMetrics:")
        print(f"  Iterations: {results.get('iterations', 0)}")
        print(f"  Discoveries: {results.get('total_discoveries', 0)}")
        print(f"  Findings: {results.get('total_findings', 0)}")
        print(f"  Truths: {results.get('total_truths', 0)}")
        print(f"  Validated: {results.get('validated_truths', 0)}")
        print(f"  Deepening enabled: {results.get('deepening_enabled', False)}")
        print(f"  Deepening findings: {results.get('deepening_findings', 0)}")

    # Event analysis
    print()
    print("-" * 40)
    print("EVENT ANALYSIS")
    print("-" * 40)

    event_counts = {}
    for event_type, payload in events_received:
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

    for event_type, count in sorted(event_counts.items()):
        print(f"  {event_type}: {count}")

    # Check for deepening events
    deepening_triggered = any(e[0] == "DEEPENING_TRIGGERED" for e in events_received)
    deepening_completed = any(e[0] == "DEEPENING_COMPLETED" for e in events_received)

    print()
    print("-" * 40)
    print("DEEPENING VERIFICATION")
    print("-" * 40)
    print(f"  Deepening triggered: {deepening_triggered}")
    print(f"  Deepening completed: {deepening_completed}")
    print(f"  Deepening findings: {len(pipeline.deepening_findings)}")

    if pipeline.deepening_findings:
        print(f"\n  Deeper findings discovered:")
        for f in pipeline.deepening_findings[:5]:
            print(f"    - {f.get('quantity', 'N/A')}: {f.get('value', 0):.4f} ≈ {f.get('target', 'N/A')}")

    # Save test results
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "success": success,
        "elapsed_seconds": elapsed,
        "pipeline_results": results,
        "events_received": [(e[0], str(e[1])[:100]) for e in events_received],
        "event_counts": event_counts,
        "deepening_triggered": deepening_triggered,
        "deepening_completed": deepening_completed,
        "deepening_findings_count": len(pipeline.deepening_findings),
        "deepening_findings": pipeline.deepening_findings[:10] if pipeline.deepening_findings else []
    }

    results_file = output_dir / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_file}")

    return test_results


def test_direct_deepener():
    """Test the deepener directly to verify it works."""
    print()
    print("=" * 70)
    print("TEST: Direct Deepener Verification")
    print("=" * 70)

    try:
        from CylleneFlow.deepener import Deepener

        deepener = Deepener(max_depth=2, verbose=True)

        # Test with a known significant finding
        test_finding = {
            "domain": "seismology",
            "quantity": "CV(dmin)",
            "value": 1.618147,
            "target": "φ",
            "target_value": 1.618034,
            "error_percent": 0.007,
            "n_samples": 150
        }

        decision = deepener.analyze_finding(test_finding)

        print(f"\nTest finding: CV(dmin) ≈ φ (0.007% error)")
        print(f"Significance: {decision.significance_score:.2f}")
        print(f"Should deepen: {decision.should_deepen}")
        print(f"Questions generated: {len(decision.questions)}")

        if decision.questions:
            print(f"\nQuestions:")
            for i, q in enumerate(decision.questions[:3], 1):
                print(f"  {i}. {q.question[:60]}...")

        return {
            "success": True,
            "significance": decision.significance_score,
            "should_deepen": decision.should_deepen,
            "questions": len(decision.questions)
        }

    except Exception as e:
        print(f"Deepener test failed: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # First verify deepener works directly
    deepener_result = test_direct_deepener()

    if deepener_result.get("success"):
        print("\n✓ Deepener verification passed")
    else:
        print("\n✗ Deepener verification failed")

    # Then test integrated pipeline
    print()
    pipeline_result = test_seismology_pipeline()

    # Final summary
    print()
    print("=" * 70)
    print("FINAL TEST SUMMARY")
    print("=" * 70)

    print(f"\nDeepener direct test: {'PASS' if deepener_result.get('success') else 'FAIL'}")
    print(f"Pipeline integration: {'PASS' if pipeline_result.get('success') else 'FAIL'}")
    print(f"Deepening triggered: {'YES' if pipeline_result.get('deepening_triggered') else 'NO'}")

    if pipeline_result.get('success') and pipeline_result.get('deepening_triggered'):
        print("\n✓ OlympusFlow v1.4.0 integration test PASSED")
        print("  Deepening is working in the integrated pipeline!")
    elif pipeline_result.get('success'):
        print("\n~ Pipeline ran but deepening was not triggered")
        print("  (May need significant findings to trigger deepening)")
    else:
        print("\n✗ Integration test had issues")
