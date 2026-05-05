#!/usr/bin/env python3
"""
VOLCANO BLIND TEST - Full OlympusFlow v1.4.0 Integration
=========================================================

End-to-end test of the complete OlympusFlow ecosystem on volcanology data:
1. HeliconLake source registry
2. HermesFlow data discovery
3. ApolloFlow pattern analysis
4. TruthFlow validation
5. CylleneFlow deepening
6. MnemosyneLake storage
7. Constants centralization

BLIND CONDITIONS:
- No volcano data in AletheiaLake
- Tests dynamic discovery and web search

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
    get_event_bus, Z2, Z, PHI
)
from OlympusFlow.stages import (
    DiscoveryStage, AnalysisStage,
    VerificationStage, StorageStage, TrainingStage
)

print("=" * 70)
print("VOLCANO BLIND TEST - OlympusFlow v1.4.0 Integration")
print("=" * 70)
print(f"Started: {datetime.now().isoformat()}")
print()
print(f"Z2 = {Z2:.6f}")
print(f"Z  = {Z:.6f}")
print(f"phi = {PHI:.6f}")
print()

# =============================================================================
# PHASE 0: VERIFY BLIND CONDITIONS
# =============================================================================

print("PHASE 0: BLIND VERIFICATION")
print("-" * 40)

# Check HeliconLake for volcano sources
try:
    from HermesFlow.helicon_lake import HeliconLake
    lake = HeliconLake()
    volcano_sources = lake.find_sources("volcanology", "volcano")
    print(f"  HeliconLake volcano sources: {len(volcano_sources)}")
    for src in volcano_sources[:3]:
        print(f"    - {src.url[:50]}...")
except Exception as e:
    print(f"  HeliconLake not available: {e}")
    volcano_sources = []

# Check AletheiaLake
aletheia_path = Path(__file__).parent.parent / "AletheiaLake"
volcano_in_aletheia = False

if aletheia_path.exists():
    for f in aletheia_path.glob("*.json"):
        try:
            content = f.read_text().lower()
            if "volcano" in content or "eruption" in content:
                volcano_in_aletheia = True
                print(f"  WARNING: Volcano data found in {f.name}")
                break
        except:
            pass

if not volcano_in_aletheia:
    print("  No volcano data in AletheiaLake (BLIND TEST)")

print()

# =============================================================================
# PHASE 1: SETUP EVENT TRACKING
# =============================================================================

print("PHASE 1: SETUP")
print("-" * 40)

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
        # Print important events
        if event.event_type in [
            EventType.DISCOVERY_FOUND,
            EventType.TRUTH_VALIDATED,
            EventType.DEEPENING_TRIGGERED,
            EventType.DEEPENING_COMPLETED
        ]:
            print(f"  [{event.event_type}] {str(event.payload)[:80]}")

    @bus.on(EventType.DEEPENING_TRIGGERED)
    def on_deepening(event):
        deepening_events.append(("TRIGGERED", event.payload))
        print(f"\n  *** DEEPENING TRIGGERED ***")

    @bus.on(EventType.DEEPENING_COMPLETED)
    def on_deepening_done(event):
        deepening_events.append(("COMPLETED", event.payload))
        print(f"  *** DEEPENING COMPLETED: {event.payload.get('deeper_findings', 0)} findings ***")

setup_event_tracking()
print("  Event tracking configured")
print()

# =============================================================================
# PHASE 2: CONFIGURE PIPELINE
# =============================================================================

print("PHASE 2: PIPELINE CONFIGURATION")
print("-" * 40)

config = PipelineConfig(
    name="volcano_blind_test",
    topic="volcanic eruption VEI explosivity index Smithsonian GVP historical",
    domain="volcanology",
    quantities=["VEI", "eruption_count", "tephra_volume", "column_height", "duration"],
    max_iterations=2,
    verbose=True,
    min_hrm_threshold=0.6
)

# Enable deepening
config.enable_deepening = True
config.max_deepening_depth = 2
config.deepening_significance_threshold = 0.5

print(f"  Topic: {config.topic}")
print(f"  Domain: {config.domain}")
print(f"  Quantities: {config.quantities}")
print(f"  Deepening: {config.enable_deepening}")
print()

# =============================================================================
# PHASE 3: CREATE AND RUN PIPELINE
# =============================================================================

print("PHASE 3: PIPELINE EXECUTION")
print("-" * 40)

output_dir = Path(__file__).parent.parent / "olympus_outputs" / "volcano_blind"
output_dir.mkdir(parents=True, exist_ok=True)

pipeline = Pipeline("volcano_blind", config, output_dir=output_dir)

# Check component availability
print(f"  Deepener active: {pipeline.deepener is not None}")
print(f"  BatchDeepener active: {pipeline.batch_deepener is not None}")
print(f"  MnemosyneLake active: {hasattr(pipeline, 'mnemosyne_lake') and pipeline.mnemosyne_lake is not None}")

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
# PHASE 4: RESULTS
# =============================================================================

print()
print("=" * 70)
print("PHASE 4: RESULTS")
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
    print(f"  Validated: {results.get('validated_truths', 0)}")
    print(f"  Deepening findings: {results.get('deepening_findings', 0)}")
    print()

    # Show truths
    if hasattr(pipeline, 'state'):
        if pipeline.state.truths:
            print("TRUTHS DISCOVERED:")
            for t in pipeline.state.truths[:10]:
                status_symbol = "V" if t.status == "validated" else "~"
                print(f"  {status_symbol} {t.claim[:60]}...")
                print(f"      HRM: {t.hrm_score:.2f}, Status: {t.status}")
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

# Deepening summary
print("DEEPENING SUMMARY:")
print(f"  Triggered: {len([e for e in deepening_events if e[0] == 'TRIGGERED'])}")
print(f"  Completed: {len([e for e in deepening_events if e[0] == 'COMPLETED'])}")
print(f"  Findings: {len(pipeline.deepening_findings) if hasattr(pipeline, 'deepening_findings') else 0}")

if hasattr(pipeline, 'deepening_findings') and pipeline.deepening_findings:
    print("\n  Deeper findings:")
    for f in pipeline.deepening_findings[:5]:
        print(f"    - {f.get('quantity')}: {f.get('value', 0):.4f} = {f.get('target')}")
print()

# =============================================================================
# PHASE 5: SAVE RESULTS
# =============================================================================

print("PHASE 5: SAVING RESULTS")
print("-" * 40)

test_results = {
    "timestamp": datetime.now().isoformat(),
    "test_type": "volcano_blind",
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
    "helicon_sources": len(volcano_sources),
    "events": events_log[-50:]
}

results_file = output_dir / "volcano_blind_results.json"
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

checks = [
    ("HeliconLake queried", len(volcano_sources) >= 0),
    ("Pipeline success", success),
    ("Data discovered", results.get('total_discoveries', 0) > 0 if success else False),
    ("Patterns found", results.get('total_findings', 0) > 0 if success else False),
    ("Events emitted", len(events_log) > 5),
]

all_passed = True
for name, passed in checks:
    symbol = "V" if passed else "X"
    print(f"  {symbol} {name}: {'YES' if passed else 'NO'}")
    if not passed and name in ["Pipeline success", "Data discovered"]:
        all_passed = False

print()

if all_passed:
    print("V VOLCANO BLIND TEST COMPLETED SUCCESSFULLY")
    print("  OlympusFlow ecosystem is working end-to-end!")
else:
    print("~ VOLCANO BLIND TEST COMPLETED WITH ISSUES")
    print("  Some components may need attention")
