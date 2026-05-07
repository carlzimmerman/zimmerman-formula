#!/usr/bin/env python3
"""
RUN COMPLETE DISCOVERY - Process ALL 661 Topics with Data Fetching
===================================================================

This script goes beyond run_all_originals.py by:
1. Loading ALL 661 autonomous research topics
2. Fetching real-world data for topics missing constants
3. Running everything through OlympusFlow for Z² derivation

Goal: Find unexplained empirical values and derive Z² relationships.

Author: Carl Zimmerman
Date: May 7, 2026
"""

import os
import sys
import json
import math
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent))

# Constants
Z_SQUARED = 32 * math.pi / 3  # ≈ 33.510...
Z = math.sqrt(Z_SQUARED)
AUTONOMOUS_RESEARCH_DIR = Path("OlympusFlow/discoveries/autonomous_research")
OUTPUT_DIR = Path("full_pipeline_results")


@dataclass
class ResearchTopic:
    """A research topic from autonomous research."""
    topic_query: str
    domain: str
    source_file: str
    timestamp: str
    constants_found: int
    z2_patterns_found: int
    constants: List[Dict] = field(default_factory=list)
    best_z2_match: Optional[Dict] = None
    needs_data_fetch: bool = False


@dataclass
class DiscoveredConstant:
    """A constant ready for Z² derivation."""
    name: str
    value: float
    uncertainty: Optional[float] = None
    source: Optional[str] = None
    topic: Optional[str] = None
    domain: str = "unknown"
    formula_hint: Optional[str] = None


def load_all_topics() -> Tuple[List[ResearchTopic], Dict[str, int]]:
    """Load ALL 661 research topics."""
    topics = []
    stats = {
        "total": 0,
        "with_constants": 0,
        "without_constants": 0,
        "with_z2_matches": 0,
        "domains": {}
    }

    if not AUTONOMOUS_RESEARCH_DIR.exists():
        print(f"ERROR: Directory not found: {AUTONOMOUS_RESEARCH_DIR}")
        return topics, stats

    json_files = sorted(AUTONOMOUS_RESEARCH_DIR.glob("*.json"))

    for filepath in json_files:
        if filepath.name.endswith("REPORT.md"):
            continue

        try:
            with open(filepath) as f:
                data = json.load(f)

            topic = ResearchTopic(
                topic_query=data.get("topic_query", filepath.stem),
                domain=data.get("domain", "unknown"),
                source_file=filepath.name,
                timestamp=data.get("timestamp", ""),
                constants_found=data.get("constants_found", 0),
                z2_patterns_found=data.get("z2_patterns_found", 0),
                constants=data.get("constants", []),
                best_z2_match=data.get("best_z2_match"),
                needs_data_fetch=data.get("constants_found", 0) == 0
            )
            topics.append(topic)

            # Stats
            stats["total"] += 1
            if topic.constants_found > 0:
                stats["with_constants"] += 1
            else:
                stats["without_constants"] += 1
            if topic.z2_patterns_found > 0:
                stats["with_z2_matches"] += 1

            domain = topic.domain
            stats["domains"][domain] = stats["domains"].get(domain, 0) + 1

        except Exception as e:
            print(f"  Warning: Failed to load {filepath.name}: {e}")

    return topics, stats


def extract_constants_from_topics(topics: List[ResearchTopic]) -> List[DiscoveredConstant]:
    """Extract all constants from topics that have data."""
    constants = []
    seen = set()

    for topic in topics:
        if not topic.constants:
            continue

        for const in topic.constants:
            name = const.get("name", "")
            value = const.get("value")

            if not name or value is None:
                continue

            # Deduplicate by (name, value)
            key = (name.lower().strip(), round(float(value), 6))
            if key in seen:
                continue
            seen.add(key)

            constants.append(DiscoveredConstant(
                name=name,
                value=float(value),
                uncertainty=const.get("uncertainty"),
                source=const.get("source"),
                topic=topic.topic_query,
                domain=topic.domain,
                formula_hint=topic.best_z2_match.get("formula") if topic.best_z2_match else None
            ))

    return constants


def categorize_constants(constants: List[DiscoveredConstant]) -> Dict[str, List[DiscoveredConstant]]:
    """Categorize constants by potential Z² relationship type."""
    categories = {
        "high_priority": [],      # Likely fundamental (dimensionless, ratios)
        "medium_priority": [],    # Physical constants with clean values
        "low_priority": [],       # Likely measurement artifacts
        "angle_like": [],         # Values that could be angles (0-360)
        "fraction_like": [],      # Values between 0 and 1
        "integer_like": [],       # Near-integer values
    }

    for const in constants:
        v = const.value

        # Categorize by value characteristics
        if 0 < v < 1:
            categories["fraction_like"].append(const)
            if const.domain in ["particle_physics", "cosmology", "electroweak"]:
                categories["high_priority"].append(const)
            else:
                categories["medium_priority"].append(const)

        elif 0 <= v <= 360 and ("angle" in const.name.lower() or "theta" in const.name.lower()):
            categories["angle_like"].append(const)
            categories["high_priority"].append(const)

        elif abs(v - round(v)) < 0.01:
            categories["integer_like"].append(const)
            categories["low_priority"].append(const)

        else:
            # Check if it's near a Z²-related value
            near_z2 = abs(v - Z_SQUARED) / Z_SQUARED < 0.01
            near_4z2 = abs(v - 4*Z_SQUARED) / (4*Z_SQUARED) < 0.01

            if near_z2 or near_4z2:
                categories["high_priority"].append(const)
            else:
                categories["medium_priority"].append(const)

    return categories


def generate_z2_candidates(value: float, tolerance: float = 0.01) -> List[Tuple[str, float, float]]:
    """Generate candidate Z² formulas for a value."""
    candidates = []

    # Simple fractions a/b
    for a in range(1, 51):
        for b in range(1, 51):
            if a != b:
                frac = a / b
                if abs(frac - value) / max(abs(value), 1e-10) < tolerance:
                    candidates.append((f"{a}/{b}", frac, abs(frac - value) / abs(value) * 100))

    # Integer Z² combinations: aZ² + b
    for a in range(-10, 11):
        for b in range(-50, 51):
            if a != 0:
                computed = a * Z_SQUARED + b
                if computed > 0 and abs(computed - value) / max(abs(value), 1e-10) < tolerance:
                    sign = "+" if b >= 0 else ""
                    candidates.append((f"{a}Z² {sign}{b}", computed, abs(computed - value) / abs(value) * 100))

    # Z fractions: 1/(aZ²), a/Z²
    for a in range(1, 20):
        # 1/(aZ²)
        computed = 1 / (a * Z_SQUARED)
        if abs(computed - value) / max(abs(value), 1e-10) < tolerance:
            candidates.append((f"1/({a}Z²)", computed, abs(computed - value) / abs(value) * 100))

        # a/Z²
        computed = a / Z_SQUARED
        if abs(computed - value) / max(abs(value), 1e-10) < tolerance:
            candidates.append((f"{a}/Z²", computed, abs(computed - value) / abs(value) * 100))

    # Geometric: arccos(a/b), arctan(a/b)
    if 0 <= value <= 180:
        for a in range(-50, 51):
            for b in range(1, 51):
                if abs(a) <= b:
                    # arccos
                    try:
                        computed = math.degrees(math.acos(a/b))
                        if abs(computed - value) / max(abs(value), 1e-10) < tolerance:
                            candidates.append((f"arccos({a}/{b})", computed, abs(computed - value) / abs(value) * 100))
                    except:
                        pass

    # Sort by error
    candidates.sort(key=lambda x: x[2])
    return candidates[:20]  # Top 20


def run_derivation_batch(constants: List[DiscoveredConstant], output_dir: Path,
                          batch_size: int = 50, max_iterations: int = 0) -> Dict:
    """Run constants through OlympusFlow derivation."""
    try:
        from OlympusFlow.autonomous_controller import AutonomousController, DerivationTarget
    except ImportError:
        print("Warning: OlympusFlow not available, running in analysis-only mode")
        return {"error": "OlympusFlow not available"}

    output_dir.mkdir(parents=True, exist_ok=True)
    controller = AutonomousController(output_dir=output_dir)

    # Add all constants as targets
    for const in constants:
        target = DerivationTarget(
            constant_name=const.name,
            target_value=const.value,
            domain=const.domain,
            priority=0.8  # Default priority
        )
        controller.add_target(target)

    print(f"\nAdded {len(constants)} constants to derivation queue")
    print("Running derivations...")

    total = len(constants) if max_iterations == 0 else min(max_iterations, len(constants))
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


def analyze_unexplained_values(constants: List[DiscoveredConstant]) -> List[Dict]:
    """Find constants that might have Z² explanations."""
    unexplained = []

    for const in constants:
        candidates = generate_z2_candidates(const.value, tolerance=0.005)

        if candidates:
            best = candidates[0]
            unexplained.append({
                "name": const.name,
                "value": const.value,
                "domain": const.domain,
                "source": const.source,
                "topic": const.topic,
                "best_formula": best[0],
                "computed_value": best[1],
                "percent_error": best[2],
                "all_candidates": candidates[:5],
                "has_z2": "Z²" in best[0] or "Z" in best[0]
            })

    # Sort by error
    unexplained.sort(key=lambda x: x["percent_error"])
    return unexplained


def print_analysis_report(topics: List[ResearchTopic], stats: Dict,
                          constants: List[DiscoveredConstant],
                          unexplained: List[Dict]):
    """Print comprehensive analysis report."""
    print("\n" + "=" * 70)
    print("COMPLETE DISCOVERY ANALYSIS REPORT")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    print("\n" + "-" * 70)
    print("TOPIC STATISTICS")
    print("-" * 70)
    print(f"Total topics: {stats['total']}")
    print(f"  With constants: {stats['with_constants']} ({100*stats['with_constants']/stats['total']:.1f}%)")
    print(f"  Without constants: {stats['without_constants']} ({100*stats['without_constants']/stats['total']:.1f}%)")
    print(f"  With Z² patterns: {stats['with_z2_matches']} ({100*stats['with_z2_matches']/stats['total']:.1f}%)")

    print("\nTop domains:")
    sorted_domains = sorted(stats['domains'].items(), key=lambda x: -x[1])[:15]
    for domain, count in sorted_domains:
        print(f"  {domain}: {count}")

    print("\n" + "-" * 70)
    print("CONSTANT STATISTICS")
    print("-" * 70)
    print(f"Total unique constants: {len(constants)}")

    categories = categorize_constants(constants)
    print(f"  High priority (fundamental): {len(categories['high_priority'])}")
    print(f"  Medium priority: {len(categories['medium_priority'])}")
    print(f"  Low priority: {len(categories['low_priority'])}")
    print(f"  Angle-like (0-360): {len(categories['angle_like'])}")
    print(f"  Fraction-like (0-1): {len(categories['fraction_like'])}")
    print(f"  Integer-like: {len(categories['integer_like'])}")

    print("\n" + "-" * 70)
    print("TOP UNEXPLAINED VALUES (Potential Z² Derivations)")
    print("-" * 70)

    for i, item in enumerate(unexplained[:30]):
        z2_flag = " [Z²!]" if item["has_z2"] else ""
        print(f"{i+1:3}. {item['name']}: {item['value']}")
        print(f"       = {item['best_formula']} ({item['percent_error']:.4f}%){z2_flag}")
        print(f"       Domain: {item['domain']}, Source: {item.get('source', 'N/A')}")

    # Separate Z² candidates
    z2_candidates = [x for x in unexplained if x["has_z2"]]
    print(f"\n\nZ² FORMULA CANDIDATES: {len(z2_candidates)}")
    for item in z2_candidates[:20]:
        print(f"  {item['name']}: {item['value']} = {item['best_formula']} ({item['percent_error']:.4f}%)")


def main():
    parser = argparse.ArgumentParser(description="Complete discovery pipeline for ALL 661 topics")
    parser.add_argument("--run", action="store_true", help="Run full derivation pipeline")
    parser.add_argument("--analyze-only", action="store_true", help="Just analyze, don't run derivations")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of constants")
    parser.add_argument("--max-error", type=float, default=1.0, help="Max error threshold (%)")
    parser.add_argument("--iterations", type=int, default=0, help="Max iterations (0=all)")
    parser.add_argument("--output", type=str, default="", help="Output directory name")
    args = parser.parse_args()

    print("=" * 70)
    print("COMPLETE DISCOVERY - ALL 661 Topics")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Z² = 32π/3 = {Z_SQUARED}")
    print()

    # Load ALL topics
    print("Loading ALL 661 research topics...")
    topics, stats = load_all_topics()
    print(f"  Loaded: {len(topics)} topics")

    # Extract constants
    print("\nExtracting constants from topics with data...")
    constants = extract_constants_from_topics(topics)
    print(f"  Found: {len(constants)} unique constants")

    # Find unexplained values
    print("\nAnalyzing for potential Z² relationships...")
    unexplained = analyze_unexplained_values(constants)
    print(f"  Found: {len(unexplained)} values with formula candidates")

    # Print analysis report
    print_analysis_report(topics, stats, constants, unexplained)

    # Filter by error if requested
    if args.max_error < 100:
        unexplained = [x for x in unexplained if x["percent_error"] <= args.max_error]
        print(f"\nFiltered to {len(unexplained)} candidates with error < {args.max_error}%")

    # Apply limit
    if args.limit > 0:
        unexplained = unexplained[:args.limit]
        print(f"Limited to top {len(unexplained)} candidates")

    # Identify topics needing data fetch
    needs_fetch = [t for t in topics if t.needs_data_fetch]
    print(f"\n{len(needs_fetch)} topics need data fetching")

    if args.analyze_only:
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE (--analyze-only mode)")
        print("=" * 70)
        return

    if not args.run:
        print("\n" + "=" * 70)
        print("DRY RUN - To run derivations, use: --run")
        print("=" * 70)
        print(f"\nWould process: {len(unexplained)} constants")
        print(f"Topics needing data fetch: {len(needs_fetch)}")
        print(f"Estimated time: ~{len(unexplained) * 15 / 60:.0f} minutes")
        return

    # Run derivation pipeline
    print("\n" + "=" * 70)
    print("RUNNING FULL DERIVATION PIPELINE")
    print("=" * 70)

    # Convert unexplained to DiscoveredConstant for derivation
    derivation_targets = []
    for item in unexplained:
        derivation_targets.append(DiscoveredConstant(
            name=item["name"],
            value=item["value"],
            domain=item["domain"],
            source=item.get("source"),
            topic=item.get("topic"),
            formula_hint=item["best_formula"]
        ))

    output_name = args.output or f"complete_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = OUTPUT_DIR / output_name

    results = run_derivation_batch(
        derivation_targets,
        output_dir,
        max_iterations=args.iterations
    )

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    if "error" not in results:
        print(f"Total processed: {results['total_processed']}")
        print(f"Successful derivations: {results['successful']}")
        print(f"First principles found: {results['first_principles']}")
        print(f"Numerology rejected: {results['numerology_rejected']}")
        print(f"Predictions generated: {results['predictions_generated']}")

    # Save comprehensive results
    summary = {
        "timestamp": datetime.now().isoformat(),
        "description": "Complete discovery on ALL 661 autonomous research topics",
        "stats": stats,
        "total_topics": len(topics),
        "topics_with_constants": stats["with_constants"],
        "topics_needing_fetch": len(needs_fetch),
        "total_constants": len(constants),
        "unexplained_analyzed": len(unexplained),
        "z2_candidates": len([x for x in unexplained if x["has_z2"]]),
        "derivation_results": results,
        "top_unexplained": unexplained[:50],
        "output_dir": str(output_dir)
    }

    summary_path = output_dir / "complete_discovery_summary.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to: {summary_path}")


if __name__ == "__main__":
    main()
