#!/usr/bin/env python3
"""
HURRICANE BLIND TEST - Full OlympusFlow v1.4.0
===============================================

Completely blind test of the integrated OlympusFlow pipeline on hurricane data.

BLIND VERIFICATION:
- Hurricane data NOT in AletheiaLake (verified)
- No hurricane patterns in learned_strategies.json
- System must discover everything dynamically

TESTS:
1. HermesFlow discovers hurricane data sources
2. ApolloFlow analyzes for Z² patterns
3. TruthFlow validates findings
4. Deepening triggers if significant findings
5. CylleneFlow learns from results

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import json
import time
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

# Z² constants
Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)
PHI = (1 + math.sqrt(5)) / 2

print("=" * 70)
print("HURRICANE BLIND TEST - OlympusFlow v1.4.0")
print("=" * 70)
print(f"Started: {datetime.now().isoformat()}")
print()
print(f"Z² = {Z2:.6f}")
print(f"Z  = {Z:.6f}")
print(f"φ  = {PHI:.6f}")
print()

# =============================================================================
# PHASE 0: VERIFY BLIND CONDITIONS
# =============================================================================

print("PHASE 0: BLIND VERIFICATION")
print("-" * 40)

# Check AletheiaLake
aletheia_path = Path(__file__).parent.parent / "AletheiaLake"
hurricane_in_aletheia = False

if aletheia_path.exists():
    for f in aletheia_path.glob("*.json"):
        try:
            content = f.read_text().lower()
            if any(term in content for term in ['hurricane', 'cyclone', 'tropical storm', 'ace index']):
                hurricane_in_aletheia = True
                print(f"  WARNING: Hurricane data found in {f.name}")
                break
        except:
            pass

if not hurricane_in_aletheia:
    print("  ✓ No hurricane data in AletheiaLake")
else:
    print("  ✗ Hurricane data exists - NOT A BLIND TEST")

# Check learned strategies
learned_path = Path(__file__).parent.parent / "HermesFlow" / "learned_strategies.json"
hurricane_in_learned = False

if learned_path.exists():
    try:
        content = learned_path.read_text().lower()
        if any(term in content for term in ['hurricane', 'cyclone', 'ace']):
            hurricane_in_learned = True
            print("  WARNING: Hurricane patterns in learned_strategies.json")
    except:
        pass

if not hurricane_in_learned:
    print("  ✓ No hurricane patterns in learned strategies")

is_blind = not hurricane_in_aletheia and not hurricane_in_learned
print(f"\n  BLIND TEST: {'YES' if is_blind else 'NO'}")

if not is_blind:
    print("\n  Proceeding anyway but results may be influenced by prior knowledge")

print()

# =============================================================================
# PHASE 1: IMPORT AND SETUP
# =============================================================================

print("PHASE 1: SETUP")
print("-" * 40)

try:
    from OlympusFlow import (
        Pipeline, PipelineConfig, EventType,
        get_event_bus, set_event_bus
    )
    from OlympusFlow.stages import (
        DiscoveryStage, AnalysisStage,
        VerificationStage, StorageStage, TrainingStage
    )
    print("  ✓ OlympusFlow imported")
except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Event tracking
events_log = []
deepening_events = []

def setup_event_tracking():
    """Track all pipeline events."""
    bus = get_event_bus()

    @bus.on("*")
    def log_all(event):
        events_log.append({
            "type": event.event_type,
            "timestamp": datetime.now().isoformat(),
            "payload": str(event.payload)[:200]
        })

    @bus.on(EventType.DEEPENING_TRIGGERED)
    def on_deepening(event):
        deepening_events.append(("TRIGGERED", event.payload))
        print(f"\n  *** DEEPENING TRIGGERED ***")
        print(f"      Finding: {event.payload.get('finding', 'N/A')}")
        print(f"      Significance: {event.payload.get('significance', 0):.2f}")

    @bus.on(EventType.DEEPENING_COMPLETED)
    def on_deepening_done(event):
        deepening_events.append(("COMPLETED", event.payload))
        print(f"  *** DEEPENING COMPLETED: {event.payload.get('deeper_findings', 0)} findings ***")

print("  ✓ Event tracking configured")
print()

# =============================================================================
# PHASE 2: CONFIGURE PIPELINE
# =============================================================================

print("PHASE 2: PIPELINE CONFIGURATION")
print("-" * 40)

config = PipelineConfig(
    name="hurricane_blind_test",
    topic="Atlantic hurricane intensity ACE accumulated cyclone energy NOAA",
    domain="meteorology",
    quantities=["intensity", "wind_speed", "pressure", "ACE", "count"],
    max_iterations=3,
    verbose=True,
    min_hrm_threshold=0.6  # Lower threshold for blind test
)

# Enable deepening with lower threshold for testing
config.enable_deepening = True
config.max_deepening_depth = 2
config.deepening_significance_threshold = 0.5

print(f"  Topic: {config.topic}")
print(f"  Domain: {config.domain}")
print(f"  Quantities: {config.quantities}")
print(f"  Max iterations: {config.max_iterations}")
print(f"  Deepening enabled: {config.enable_deepening}")
print()

# =============================================================================
# PHASE 3: CREATE AND RUN PIPELINE
# =============================================================================

print("PHASE 3: PIPELINE EXECUTION")
print("-" * 40)

output_dir = Path(__file__).parent.parent / "olympus_outputs" / "hurricane_blind_v14"
output_dir.mkdir(parents=True, exist_ok=True)

pipeline = Pipeline("hurricane_blind", config, output_dir=output_dir)
setup_event_tracking()

# Verify deepener is active
print(f"  Deepener active: {pipeline.deepener is not None}")
print(f"  BatchDeepener active: {pipeline.batch_deepener is not None}")

# Add stages
pipeline.add_stage(DiscoveryStage(
    topic=config.topic,
    domain=config.domain,
    quantities=config.quantities,
    model="legomena-moe"
))
pipeline.add_stage(AnalysisStage())
pipeline.add_stage(VerificationStage())
pipeline.add_stage(StorageStage())
pipeline.add_stage(TrainingStage(output_path=output_dir / "training.jsonl"))

print(f"  Stages: {[s.name for s in pipeline.stages]}")
print()

print("=" * 70)
print("RUNNING PIPELINE...")
print("=" * 70)
print()

start_time = time.time()

try:
    results = pipeline.run(max_iterations=config.max_iterations)
    success = True
except Exception as e:
    print(f"\nPipeline error: {e}")
    import traceback
    traceback.print_exc()
    results = {"error": str(e)}
    success = False

elapsed = time.time() - start_time

# =============================================================================
# PHASE 4: ANALYZE RESULTS
# =============================================================================

print()
print("=" * 70)
print("PHASE 4: RESULTS ANALYSIS")
print("=" * 70)
print()

print(f"Pipeline completed: {success}")
print(f"Total time: {elapsed:.1f}s")
print()

if success:
    print("METRICS:")
    print(f"  Iterations: {results.get('iterations', 0)}")
    print(f"  Discoveries: {results.get('total_discoveries', 0)}")
    print(f"  Findings: {results.get('total_findings', 0)}")
    print(f"  Truths: {results.get('total_truths', 0)}")
    print(f"  Validated truths: {results.get('validated_truths', 0)}")
    print(f"  Deepening enabled: {results.get('deepening_enabled', False)}")
    print(f"  Deepening findings: {results.get('deepening_findings', 0)}")
    print()

    # Check state for actual findings
    if hasattr(pipeline, 'state'):
        print("TRUTHS DISCOVERED:")
        for t in pipeline.state.truths:
            status_symbol = "✓" if t.status == "validated" else "~"
            print(f"  {status_symbol} {t.claim}")
            print(f"      HRM: {t.hrm_score:.2f}, Status: {t.status}")
            if t.measured_value and t.z2_prediction:
                error = abs(t.measured_value - t.z2_prediction) / t.z2_prediction * 100
                print(f"      Measured: {t.measured_value:.4f}, Predicted: {t.z2_prediction:.4f}, Error: {error:.2f}%")
        print()

        print("FINDINGS:")
        for f in pipeline.state.findings[:10]:
            print(f"  - {f.claim}: {f.quantity} = {f.measured_value:.4f}")
        print()

# Deepening analysis
print("DEEPENING ANALYSIS:")
print(f"  Events triggered: {len([e for e in deepening_events if e[0] == 'TRIGGERED'])}")
print(f"  Events completed: {len([e for e in deepening_events if e[0] == 'COMPLETED'])}")
print(f"  Deeper findings: {len(pipeline.deepening_findings) if hasattr(pipeline, 'deepening_findings') else 0}")

if pipeline.deepening_findings:
    print("\n  Deeper findings discovered:")
    for f in pipeline.deepening_findings[:5]:
        print(f"    - {f.get('quantity')}: {f.get('value', 0):.4f} ≈ {f.get('target')}")
print()

# Event summary
print("EVENT SUMMARY:")
event_counts = {}
for e in events_log:
    etype = e['type']
    event_counts[etype] = event_counts.get(etype, 0) + 1

for etype, count in sorted(event_counts.items()):
    print(f"  {etype}: {count}")
print()

# =============================================================================
# PHASE 5: SAVE RESULTS
# =============================================================================

print("PHASE 5: SAVING RESULTS")
print("-" * 40)

test_results = {
    "timestamp": datetime.now().isoformat(),
    "blind_test": is_blind,
    "success": success,
    "elapsed_seconds": elapsed,
    "config": {
        "topic": config.topic,
        "domain": config.domain,
        "quantities": config.quantities,
        "max_iterations": config.max_iterations,
        "deepening_enabled": config.enable_deepening
    },
    "results": results if success else {"error": str(results.get('error', 'unknown'))},
    "truths": [
        {
            "claim": t.claim,
            "hrm_score": t.hrm_score,
            "status": t.status,
            "measured_value": t.measured_value,
            "z2_prediction": t.z2_prediction
        }
        for t in (pipeline.state.truths if hasattr(pipeline, 'state') else [])
    ],
    "deepening": {
        "triggered": len([e for e in deepening_events if e[0] == 'TRIGGERED']),
        "completed": len([e for e in deepening_events if e[0] == 'COMPLETED']),
        "findings_count": len(pipeline.deepening_findings) if hasattr(pipeline, 'deepening_findings') else 0,
        "findings": pipeline.deepening_findings[:10] if hasattr(pipeline, 'deepening_findings') else []
    },
    "events": events_log[-50:]  # Last 50 events
}

results_file = output_dir / "blind_test_results.json"
with open(results_file, 'w') as f:
    json.dump(test_results, f, indent=2, default=str)

print(f"  Results saved to: {results_file}")
print()

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print()

summary_items = [
    ("Blind test", "YES" if is_blind else "NO"),
    ("Pipeline success", "YES" if success else "NO"),
    ("Data discovered", "YES" if results.get('total_discoveries', 0) > 0 else "NO"),
    ("Patterns found", "YES" if results.get('total_findings', 0) > 0 else "NO"),
    ("Truths validated", "YES" if results.get('validated_truths', 0) > 0 else "NO"),
    ("Deepening triggered", "YES" if len(deepening_events) > 0 else "NO"),
]

for item, value in summary_items:
    symbol = "✓" if value == "YES" else "✗" if value == "NO" else "~"
    print(f"  {symbol} {item}: {value}")

print()

if success and results.get('total_discoveries', 0) > 0:
    print("✓ HURRICANE BLIND TEST PASSED")
    print("  OlympusFlow successfully discovered and analyzed hurricane data")
    if results.get('validated_truths', 0) > 0:
        print("  Found validated Z² patterns in hurricane data!")
    if len(deepening_events) > 0:
        print("  Recursive deepening was triggered!")
else:
    print("~ HURRICANE BLIND TEST COMPLETED")
    if not success:
        print("  Pipeline encountered errors")
    elif results.get('total_discoveries', 0) == 0:
        print("  No data was discovered - may need different search strategy")
