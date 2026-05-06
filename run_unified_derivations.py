#!/usr/bin/env python3
"""
RUN ALL 50 Z² DERIVATION TASKS THROUGH UNIFIED PIPELINE
========================================================

This script runs all derivation tasks through the new unified pipeline
with real Legomena reasoning, proper timing, and correct routing.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import json
import time
from pathlib import Path
from datetime import datetime

from OlympusFlow import DerivationPipeline, DerivationTask

# Load all tasks from queue
QUEUE_FILE = Path("AlpheusFlow/queue_state.json")


def load_derivation_tasks():
    """Load all derivation tasks from the queue."""
    with open(QUEUE_FILE) as f:
        data = json.load(f)

    tasks = []
    seen = set()  # Avoid duplicates

    for t in data.get("tasks", []):
        name = t.get("target_constant", "")
        value = t.get("target_value", 0)

        if not name or name in seen:
            continue

        seen.add(name)

        # Extract domain from category
        category = t.get("category", "physics")
        domain_map = {
            "chaos_fluid_dynamics": "fluid_dynamics",
            "condensed_matter": "condensed_matter",
            "nuclear_subatomic": "particle_physics",
            "astrophysics_planetary": "astrophysics",
            "complex_systems_biology": "biology",
            "material_limits": "materials_science"
        }
        domain = domain_map.get(category, "physics")

        task = DerivationTask(
            constant_name=name,
            target_value=value,
            domain=domain,
            assignment=t.get("description", "")
        )
        tasks.append(task)

    return tasks


def main():
    print("=" * 80)
    print("UNIFIED DERIVATION PIPELINE - 50 Z² CONSTANT DERIVATIONS")
    print("=" * 80)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    # Load tasks
    tasks = load_derivation_tasks()
    print(f"Loaded {len(tasks)} unique derivation tasks")
    print()

    # Create pipeline
    pipeline = DerivationPipeline(
        output_dir="unified_derivation_results",
        verbose=True
    )

    # Run batch
    start = time.time()
    results = pipeline.run_batch(tasks)
    total_time = time.time() - start

    # Compile results
    print("\n" + "=" * 80)
    print("FINAL RESULTS SUMMARY")
    print("=" * 80)

    # Categorize results
    first_principles = []
    derived = []
    numerology = []
    failed = []

    aletheia = []
    mnemosyne = []
    rejected = []

    for r in results:
        level = r.verified.chain.level.value

        if level == "first_principles":
            first_principles.append(r)
        elif level == "derived":
            derived.append(r)
        elif level == "numerical_match":
            numerology.append(r)
        else:
            failed.append(r)

        dest = r.verified.destination.value
        if dest == "aletheia":
            aletheia.append(r)
        elif dest == "mnemosyne":
            mnemosyne.append(r)
        else:
            rejected.append(r)

    print(f"\nDerivation Levels:")
    print(f"  ★ First Principles: {len(first_principles)}")
    print(f"  → Derived: {len(derived)}")
    print(f"  ~ Numerology: {len(numerology)}")
    print(f"  ✗ Failed: {len(failed)}")

    print(f"\nStorage Destinations:")
    print(f"  ★ AletheiaLake (permanent): {len(aletheia)}")
    print(f"  → MnemosyneLake (working): {len(mnemosyne)}")
    print(f"  ✗ Rejected: {len(rejected)}")

    print(f"\nTiming:")
    print(f"  Total time: {total_time:.1f}s")
    print(f"  Per task: {total_time/len(tasks):.1f}s average")

    # Print first principles details
    if first_principles:
        print("\n" + "=" * 80)
        print("FIRST PRINCIPLES DERIVATIONS (AletheiaLake candidates)")
        print("=" * 80)
        for r in first_principles:
            chain = r.verified.chain
            print(f"\n  {chain.target_constant}:")
            print(f"    Formula: {chain.final_formula}")
            print(f"    Value: {chain.computed_value:.10f}")
            print(f"    Error: {chain.percent_error:.4f}%")
            print(f"    HRM: {r.verified.hrm_score:.2f}")
            print(f"    Mechanism: {chain.physical_mechanism[:60]}...")

    # Print rejected details
    if rejected:
        print("\n" + "=" * 80)
        print("REJECTED (No Z² connection / Failed)")
        print("=" * 80)
        for r in rejected[:10]:  # First 10
            chain = r.verified.chain
            print(f"\n  {chain.target_constant}:")
            print(f"    Level: {chain.level.value}")
            print(f"    Reason: {r.verified.rejection_reason}")

    # Save full results
    output_file = Path("unified_derivation_results/FULL_RESULTS.json")
    output_file.parent.mkdir(exist_ok=True)

    full_results = {
        "run_timestamp": datetime.now().isoformat(),
        "total_tasks": len(tasks),
        "total_time_seconds": total_time,
        "summary": {
            "first_principles": len(first_principles),
            "derived": len(derived),
            "numerology": len(numerology),
            "failed": len(failed),
            "to_aletheia": len(aletheia),
            "to_mnemosyne": len(mnemosyne),
            "rejected": len(rejected)
        },
        "first_principles_list": [
            {
                "constant": r.task.constant_name,
                "formula": r.verified.chain.final_formula,
                "value": r.verified.chain.computed_value,
                "error": r.verified.chain.percent_error,
                "hrm": r.verified.hrm_score,
                "mechanism": r.verified.chain.physical_mechanism
            }
            for r in first_principles
        ],
        "derived_list": [
            {
                "constant": r.task.constant_name,
                "formula": r.verified.chain.final_formula,
                "hrm": r.verified.hrm_score
            }
            for r in derived
        ],
        "rejected_list": [
            {
                "constant": r.task.constant_name,
                "reason": r.verified.rejection_reason
            }
            for r in rejected
        ]
    }

    output_file.write_text(json.dumps(full_results, indent=2, default=str))
    print(f"\nResults saved to: {output_file}")

    print("\n" + "=" * 80)
    print(f"COMPLETE: {datetime.now().isoformat()}")
    print("=" * 80)


if __name__ == "__main__":
    main()
