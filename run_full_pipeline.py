#!/usr/bin/env python3
"""
UNIFIED FULL PIPELINE - Process All 660+ Autonomous Research Topics
====================================================================

This script processes ALL topics from autonomous research through the
complete derivation pipeline:

1. Load all 664 autonomous research results
2. Filter to topics with promising Z² matches (<1% error)
3. Generate 5 extended ideas per topic
4. Run ALL through OlympusFlow AutonomousController
5. Store results to appropriate Lakes
6. Generate summary report

Usage:
    python run_full_pipeline.py                  # Dry run (count only)
    python run_full_pipeline.py --run            # Process all topics
    python run_full_pipeline.py --run --limit 50 # Process first 50
    python run_full_pipeline.py --top 100        # Process top 100 by error

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent))

# Constants
Z_SQUARED = 32 * math.pi / 3  # ≈ 33.510...
AUTONOMOUS_RESEARCH_DIR = Path("OlympusFlow/discoveries/autonomous_research")
OUTPUT_DIR = Path("full_pipeline_results")


@dataclass
class TopicResult:
    """Result from autonomous research."""
    filename: str
    domain: str
    topic_query: str
    best_match: Optional[Dict] = None
    all_matches: List[Dict] = field(default_factory=list)
    constants_found: int = 0
    z2_patterns_found: int = 0
    timestamp: str = ""


@dataclass
class ExtendedIdea:
    """Extended research idea from a topic."""
    name: str
    value: float
    domain: str
    source_topic: str
    source_formula: str
    reason: str
    priority: float = 0.5


def load_all_topics() -> List[TopicResult]:
    """Load all autonomous research results."""
    topics = []

    if not AUTONOMOUS_RESEARCH_DIR.exists():
        print(f"ERROR: Directory not found: {AUTONOMOUS_RESEARCH_DIR}")
        return topics

    json_files = list(AUTONOMOUS_RESEARCH_DIR.glob("*.json"))

    for filepath in json_files:
        try:
            with open(filepath) as f:
                data = json.load(f)

            topic = TopicResult(
                filename=filepath.name,
                domain=data.get("domain", "unknown"),
                topic_query=data.get("topic_query", ""),
                best_match=data.get("best_z2_match"),
                all_matches=data.get("all_z2_matches", []),
                constants_found=data.get("constants_found", 0),
                z2_patterns_found=data.get("z2_patterns_found", 0),
                timestamp=data.get("timestamp", "")
            )
            topics.append(topic)
        except Exception as e:
            print(f"  Warning: Failed to load {filepath.name}: {e}")

    return topics


def filter_promising_topics(topics: List[TopicResult], max_error: float = 1.0) -> List[TopicResult]:
    """Filter to topics with promising Z² matches (low error)."""
    promising = []

    for topic in topics:
        if topic.best_match:
            error = abs(topic.best_match.get("percent_error", 100))  # Use absolute error
            if error < max_error and topic.best_match.get("has_z2", False):
                promising.append(topic)

    # Sort by absolute error (best first)
    promising.sort(key=lambda t: abs(t.best_match.get("percent_error", 100)))

    return promising


def generate_extended_ideas(topic: TopicResult) -> List[ExtendedIdea]:
    """Generate 5 extended research ideas from a topic."""
    if not topic.best_match:
        return []

    ideas = []
    value = topic.best_match.get("constant_value", 0)
    formula = topic.best_match.get("formula", "")
    name_base = topic.best_match.get("constant_name", "unknown").replace(" ", "_").lower()

    # Parse formula coefficients
    a, b = 0, 0
    if "Z²" in formula:
        parts = formula.replace(" ", "").replace("Z²", "Z2")
        if "+Z2" in parts or "Z2+" in parts or parts.startswith("Z2"):
            a = 1
        elif "-Z2" in parts:
            a = -1
        else:
            try:
                coef = parts.split("Z2")[0]
                if coef:
                    a = int(coef)
            except:
                a = 1

        # Extract constant term
        if "+" in parts:
            try:
                b = int(parts.split("+")[-1])
            except:
                b = 0
        elif parts.count("-") > 0:
            try:
                last_part = parts.split("-")[-1]
                if last_part and not "Z2" in last_part:
                    b = -int(last_part)
            except:
                b = 0

    # Idea 1: Adjacent coefficient (a+1)Z² + b
    if a != 0:
        new_val = (a + 1) * Z_SQUARED + b
        ideas.append(ExtendedIdea(
            name=f"{name_base}_coef_plus1",
            value=new_val,
            domain=topic.domain,
            source_topic=topic.topic_query,
            source_formula=formula,
            reason=f"Adjacent to {formula}: ({a+1})Z² + {b}",
            priority=0.7
        ))

    # Idea 2: Adjacent constant (aZ² + b+1)
    if b != 0:
        new_val = a * Z_SQUARED + (b + 1)
        ideas.append(ExtendedIdea(
            name=f"{name_base}_const_plus1",
            value=new_val,
            domain=topic.domain,
            source_topic=topic.topic_query,
            source_formula=formula,
            reason=f"Adjacent to {formula}: {a}Z² + {b+1}",
            priority=0.6
        ))

    # Idea 3: Ratio with π
    if value > 0:
        ideas.append(ExtendedIdea(
            name=f"{name_base}_over_pi",
            value=value / math.pi,
            domain=topic.domain,
            source_topic=topic.topic_query,
            source_formula=formula,
            reason=f"value/π - looking for clean Z² relationship",
            priority=0.5
        ))

    # Idea 4: Square root
    if value > 1:
        ideas.append(ExtendedIdea(
            name=f"{name_base}_sqrt",
            value=math.sqrt(value),
            domain=topic.domain,
            source_topic=topic.topic_query,
            source_formula=formula,
            reason=f"√value - dimensional reduction",
            priority=0.5
        ))

    # Idea 5: Reciprocal
    if value > 0 and value != 1:
        ideas.append(ExtendedIdea(
            name=f"{name_base}_reciprocal",
            value=1 / value,
            domain=topic.domain,
            source_topic=topic.topic_query,
            source_formula=formula,
            reason=f"1/value - inverse relationship",
            priority=0.4
        ))

    return ideas[:5]


def run_pipeline(ideas: List[ExtendedIdea], output_dir: Path) -> Dict:
    """Run all ideas through OlympusFlow AutonomousController."""
    from OlympusFlow.autonomous_controller import AutonomousController, DerivationTarget

    output_dir.mkdir(parents=True, exist_ok=True)

    controller = AutonomousController(output_dir=output_dir)

    # Add all ideas as targets
    for idea in ideas:
        target = DerivationTarget(
            constant_name=idea.name,
            target_value=idea.value,
            domain=idea.domain,
            priority=idea.priority
        )
        controller.add_target(target)

    print(f"Added {len(ideas)} targets to queue")
    print("Running derivations (this may take a while)...")

    # Run all with checkpointing every 50
    total = len(ideas)
    batch_size = 50
    processed = 0

    while processed < total:
        batch = min(batch_size, total - processed)
        controller.run_n(batch)
        processed += batch
        print(f"  Progress: {processed}/{total} ({100*processed/total:.1f}%)")

        # Save checkpoint
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
    parser = argparse.ArgumentParser(description="Run full Z² derivation pipeline")
    parser.add_argument("--run", action="store_true", help="Actually run the pipeline")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of topics")
    parser.add_argument("--top", type=int, default=0, help="Process only top N by error")
    parser.add_argument("--max-error", type=float, default=1.0, help="Max error threshold (%)")
    args = parser.parse_args()

    print("=" * 70)
    print("UNIFIED FULL PIPELINE - Z² Research System")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print()

    # Step 1: Load all topics
    print("Step 1: Loading autonomous research results...")
    topics = load_all_topics()
    print(f"  Loaded: {len(topics)} topics")

    # Step 2: Filter promising topics
    print(f"\nStep 2: Filtering promising topics (error < {args.max_error}%)...")
    promising = filter_promising_topics(topics, max_error=args.max_error)
    print(f"  Promising: {len(promising)} topics")

    # Apply limits
    if args.top > 0:
        promising = promising[:args.top]
        print(f"  Limited to top {args.top}: {len(promising)} topics")
    elif args.limit > 0:
        promising = promising[:args.limit]
        print(f"  Limited to first {args.limit}: {len(promising)} topics")

    # Step 3: Generate extended ideas
    print("\nStep 3: Generating extended ideas (5 per topic)...")
    all_ideas = []
    for topic in promising:
        ideas = generate_extended_ideas(topic)
        all_ideas.extend(ideas)
    print(f"  Generated: {len(all_ideas)} extended ideas")

    # Summary by domain
    domains = {}
    for idea in all_ideas:
        domains[idea.domain] = domains.get(idea.domain, 0) + 1
    print("\n  By domain:")
    for domain, count in sorted(domains.items(), key=lambda x: -x[1])[:10]:
        print(f"    {domain}: {count}")

    # Step 4: Show top promising topics
    print("\nTop 10 promising topics (by error):")
    for i, topic in enumerate(promising[:10]):
        match = topic.best_match
        print(f"  {i+1}. {match['constant_name']}")
        print(f"     Formula: {match['formula']}")
        print(f"     Error: {match['percent_error']:.4f}%")
        print(f"     Domain: {topic.domain}")

    if not args.run:
        print("\n" + "=" * 70)
        print("DRY RUN - To actually run the pipeline, use: --run")
        print("=" * 70)
        print(f"\nWould process:")
        print(f"  - {len(promising)} promising topics")
        print(f"  - {len(all_ideas)} extended ideas")
        print(f"\nEstimated time: ~{len(all_ideas) * 6 / 3600:.1f} hours (at 6s/idea)")
        return

    # Step 5: Run pipeline
    print("\n" + "=" * 70)
    print("RUNNING FULL PIPELINE")
    print("=" * 70)

    output_dir = OUTPUT_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
    results = run_pipeline(all_ideas, output_dir)

    # Step 6: Generate report
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total processed: {results['total_processed']}")
    print(f"Successful derivations: {results['successful']}")
    print(f"First principles found: {results['first_principles']}")
    print(f"Numerology rejected: {results['numerology_rejected']}")
    print(f"New predictions generated: {results['predictions_generated']}")

    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "topics_loaded": len(topics),
        "topics_promising": len(promising),
        "ideas_generated": len(all_ideas),
        "results": results,
        "output_dir": str(output_dir)
    }

    summary_path = output_dir / "pipeline_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to: {summary_path}")


if __name__ == "__main__":
    main()
