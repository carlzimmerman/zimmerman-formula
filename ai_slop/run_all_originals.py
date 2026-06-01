#!/usr/bin/env python3
"""
RUN ALL ORIGINALS - Test Every Autonomous Research Discovery
=============================================================

This script tests ALL original constants from autonomous research through
the fixed v2 pipeline. No transforms, no filtering - just the raw discoveries.

The v1 pipeline NEVER tested originals - only garbage transforms.
This gives us a complete picture of what's actually Z² derivable.

Author: Carl Zimmerman
Date: May 7, 2026
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent))

# Constants
Z_SQUARED = 32 * math.pi / 3  # ≈ 33.510...
AUTONOMOUS_RESEARCH_DIR = Path("OlympusFlow/discoveries/autonomous_research")
OUTPUT_DIR = Path("full_pipeline_results")


@dataclass
class OriginalConstant:
    """An original constant from autonomous research."""
    name: str
    value: float
    formula: str  # Best Z² formula found
    percent_error: float
    domain: str
    source_file: str
    source_citation: Optional[str] = None
    uncertainty: Optional[float] = None


def load_all_originals() -> List[OriginalConstant]:
    """Load ALL original constants from autonomous research."""
    constants = []
    seen = set()  # Deduplicate by (name, value)

    if not AUTONOMOUS_RESEARCH_DIR.exists():
        print(f"ERROR: Directory not found: {AUTONOMOUS_RESEARCH_DIR}")
        return constants

    json_files = list(AUTONOMOUS_RESEARCH_DIR.glob("*.json"))
    print(f"Scanning {len(json_files)} research files...")

    for filepath in json_files:
        try:
            with open(filepath) as f:
                data = json.load(f)

            domain = data.get("domain", "unknown")

            # Get best Z² match
            best = data.get("best_z2_match")
            if not best:
                continue

            name = best.get("constant_name", "unknown")
            value = best.get("constant_value")
            formula = best.get("formula", "")
            error = abs(best.get("percent_error", 100))
            has_z2 = best.get("has_z2", False)

            if value is None or not has_z2:
                continue

            # Get source citation if available
            source_citation = None
            uncertainty = None
            raw_constants = data.get("constants", [])
            for c in raw_constants:
                if c.get("name") == name:
                    source_citation = c.get("source")
                    uncertainty = c.get("uncertainty")
                    break

            # Deduplicate
            key = (name.lower().strip(), round(value, 6))
            if key in seen:
                continue
            seen.add(key)

            constants.append(OriginalConstant(
                name=name,
                value=value,
                formula=formula,
                percent_error=error,
                domain=domain,
                source_file=filepath.name,
                source_citation=source_citation,
                uncertainty=uncertainty
            ))

        except Exception as e:
            print(f"  Warning: Failed to load {filepath.name}: {e}")

    # Sort by error (best matches first)
    constants.sort(key=lambda c: c.percent_error)

    return constants


def run_pipeline(constants: List[OriginalConstant], output_dir: Path, max_iterations: int = 0) -> Dict:
    """Run all constants through OlympusFlow."""
    from OlympusFlow.autonomous_controller import AutonomousController, DerivationTarget

    output_dir.mkdir(parents=True, exist_ok=True)

    controller = AutonomousController(output_dir=output_dir)

    # Add all constants as targets
    for const in constants:
        target = DerivationTarget(
            constant_name=const.name,
            target_value=const.value,
            domain=const.domain,
            priority=1.0 - (const.percent_error / 100)  # Lower error = higher priority
        )
        controller.add_target(target)

    print(f"\nAdded {len(constants)} original constants to queue")
    print("Running derivations...")

    total = len(constants) if max_iterations == 0 else min(max_iterations, len(constants))
    batch_size = 50
    processed = 0

    while processed < total:
        batch = min(batch_size, total - processed)
        controller.run_n(batch)
        processed += batch
        print(f"  Progress: {processed}/{total} ({100*processed/total:.1f}%)")

        if hasattr(controller, 'save_state'):
            controller.save_state()

    return {
        "total_processed": controller.stats.total_targets_processed,
        "successful": controller.stats.successful_derivations,
        "first_principles": controller.stats.first_principles_found,
        "numerology_rejected": controller.stats.numerology_rejected,
        "predictions_generated": controller.stats.predictions_generated
    }


def main():
    parser = argparse.ArgumentParser(description="Run ALL original constants through v2 pipeline")
    parser.add_argument("--run", action="store_true", help="Actually run the pipeline")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of constants")
    parser.add_argument("--max-error", type=float, default=100.0, help="Max error threshold (%)")
    parser.add_argument("--iterations", type=int, default=0, help="Max iterations (0=all)")
    args = parser.parse_args()

    print("=" * 70)
    print("RUN ALL ORIGINALS - Complete Autonomous Research Test")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print()

    # Load ALL originals
    print("Loading ALL original constants from autonomous research...")
    all_constants = load_all_originals()
    print(f"  Total unique constants with Z² matches: {len(all_constants)}")

    # Filter by max error if specified
    if args.max_error < 100:
        all_constants = [c for c in all_constants if c.percent_error <= args.max_error]
        print(f"  After error filter (<{args.max_error}%): {len(all_constants)}")

    # Apply limit
    if args.limit > 0:
        all_constants = all_constants[:args.limit]
        print(f"  After limit: {len(all_constants)}")

    # Show distribution
    print("\nError Distribution:")
    buckets = {"<0.01%": 0, "0.01-0.1%": 0, "0.1-0.5%": 0, "0.5-1%": 0, "1-5%": 0, ">5%": 0}
    for c in all_constants:
        if c.percent_error < 0.01:
            buckets["<0.01%"] += 1
        elif c.percent_error < 0.1:
            buckets["0.01-0.1%"] += 1
        elif c.percent_error < 0.5:
            buckets["0.1-0.5%"] += 1
        elif c.percent_error < 1.0:
            buckets["0.5-1%"] += 1
        elif c.percent_error < 5.0:
            buckets["1-5%"] += 1
        else:
            buckets[">5%"] += 1
    for bucket, count in buckets.items():
        print(f"  {bucket}: {count}")

    # Show by domain
    print("\nBy Domain:")
    domains = {}
    for c in all_constants:
        domains[c.domain] = domains.get(c.domain, 0) + 1
    for domain, count in sorted(domains.items(), key=lambda x: -x[1])[:10]:
        print(f"  {domain}: {count}")

    # Show top matches
    print("\nTop 20 Original Constants (by error):")
    for i, c in enumerate(all_constants[:20]):
        src = f" [{c.source_citation}]" if c.source_citation else ""
        print(f"  {i+1}. {c.name}: {c.value} = {c.formula} ({c.percent_error:.4f}%){src}")

    if not args.run:
        print("\n" + "=" * 70)
        print("DRY RUN - To run the pipeline, use: --run")
        print("=" * 70)
        print(f"\nWould process: {len(all_constants)} original constants")
        print(f"Estimated time: ~{len(all_constants) * 15 / 60:.0f} minutes")
        return

    # Run pipeline
    print("\n" + "=" * 70)
    print("RUNNING PIPELINE ON ALL ORIGINALS")
    print("=" * 70)

    output_dir = OUTPUT_DIR / f"all_originals_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    results = run_pipeline(all_constants, output_dir, max_iterations=args.iterations)

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total processed: {results['total_processed']}")
    print(f"Successful derivations: {results['successful']}")
    print(f"First principles found: {results['first_principles']}")
    print(f"Numerology rejected: {results['numerology_rejected']}")
    print(f"Predictions generated: {results['predictions_generated']}")

    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "description": "Complete test of ALL original autonomous research constants",
        "constants_tested": len(all_constants),
        "results": results,
        "output_dir": str(output_dir)
    }

    summary_path = output_dir / "all_originals_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to: {summary_path}")


if __name__ == "__main__":
    main()
