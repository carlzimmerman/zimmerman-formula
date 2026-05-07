#!/usr/bin/env python3
"""
FIXED FULL PIPELINE V2 - Process Original Constants + Known Z² Values
======================================================================

FIXES from v1:
1. Tests ORIGINAL constants directly (not just transforms)
2. Removes tautological transforms (_coef_plus1, _const_plus1)
3. Adds known Z² constants for first-principles verification
4. Keeps only physically meaningful transforms (_sqrt for dimensional, _over_pi for angular)

Author: Carl Zimmerman
Date: May 6, 2026
Version: 2.0.0
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
Z = math.sqrt(Z_SQUARED)       # ≈ 5.789...
AUTONOMOUS_RESEARCH_DIR = Path("OlympusFlow/discoveries/autonomous_research")
OUTPUT_DIR = Path("full_pipeline_results")


# =============================================================================
# KNOWN Z² CONSTANTS (Ground Truth)
# =============================================================================

KNOWN_Z2_CONSTANTS = [
    # First-principles verified
    {
        "name": "sin2_theta_w",
        "display_name": "Weak mixing angle sin²θ_W",
        "value": 0.23122,
        "expected_formula": "3/13",
        "expected_value": 3/13,
        "domain": "particle_physics",
        "derivation_level": "first_principles",
        "priority": 1.0,
        "notes": "Electroweak gauge coupling ratio"
    },
    {
        "name": "fine_structure_inverse",
        "display_name": "Fine structure constant α⁻¹",
        "value": 137.035999,
        "expected_formula": "4Z² + 3",
        "expected_value": 4 * Z_SQUARED + 3,
        "domain": "particle_physics",
        "derivation_level": "first_principles",
        "priority": 1.0,
        "notes": "Geometric structure of QED"
    },
    {
        "name": "dark_energy_fraction",
        "display_name": "Dark energy fraction Ω_Λ",
        "value": 0.685,
        "expected_formula": "13/19",
        "expected_value": 13/19,
        "domain": "cosmology",
        "derivation_level": "first_principles",
        "priority": 1.0,
        "notes": "Holographic dark energy from Z²"
    },
    {
        "name": "hubble_constant",
        "display_name": "Hubble constant H₀",
        "value": 70.0,  # km/s/Mpc
        "expected_formula": "Z·a₀/c (in appropriate units)",
        "expected_value": 71.5,  # Z * 1.2e-10 / 2.998e8 * 3.086e22 / 1000
        "domain": "cosmology",
        "derivation_level": "first_principles",
        "priority": 0.9,
        "notes": "MOND-cosmology connection"
    },
    # PMNS matrix angles
    {
        "name": "pmns_theta12",
        "display_name": "PMNS θ₁₂ (solar angle)",
        "value": 33.44,  # degrees
        "expected_formula": "arcsin(1/√3)",
        "expected_value": math.degrees(math.asin(1/math.sqrt(3))),
        "domain": "particle_physics",
        "derivation_level": "first_principles",
        "priority": 0.95,
        "notes": "Neutrino mixing from geometry"
    },
    {
        "name": "pmns_theta23",
        "display_name": "PMNS θ₂₃ (atmospheric angle)",
        "value": 49.2,  # degrees
        "expected_formula": "45°",
        "expected_value": 45.0,
        "domain": "particle_physics",
        "derivation_level": "first_principles",
        "priority": 0.95,
        "notes": "Maximal mixing"
    },
    {
        "name": "pmns_theta13",
        "display_name": "PMNS θ₁₃ (reactor angle)",
        "value": 8.57,  # degrees
        "expected_formula": "arcsin(1/√(2Z²))",
        "expected_value": math.degrees(math.asin(1/math.sqrt(2*Z_SQUARED))),
        "domain": "particle_physics",
        "derivation_level": "first_principles",
        "priority": 0.95,
        "notes": "Z² suppressed mixing"
    },
    # Cosmological
    {
        "name": "tensor_to_scalar_ratio",
        "display_name": "Tensor-to-scalar ratio r",
        "value": 0.01,  # Upper bound
        "expected_formula": "1/(2Z²)",
        "expected_value": 1/(2*Z_SQUARED),
        "domain": "cosmology",
        "derivation_level": "first_principles",
        "priority": 0.85,
        "notes": "CMB B-mode prediction"
    },
    # Matter fractions
    {
        "name": "matter_fraction",
        "display_name": "Matter fraction Ω_m",
        "value": 0.315,
        "expected_formula": "6/19",
        "expected_value": 6/19,
        "domain": "cosmology",
        "derivation_level": "derived",
        "priority": 0.8,
        "notes": "Complement of Ω_Λ"
    },
    # Tetrahedral angle (geometry)
    {
        "name": "tetrahedral_angle",
        "display_name": "Tetrahedral angle",
        "value": 109.4712,  # degrees
        "expected_formula": "arccos(-1/3)",
        "expected_value": math.degrees(math.acos(-1/3)),
        "domain": "chemistry",
        "derivation_level": "geometric",
        "priority": 0.7,
        "notes": "sp³ hybridization geometry"
    },
]


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
class DerivationIdea:
    """A derivation target for the pipeline."""
    name: str
    value: float
    domain: str
    source: str  # "known_z2", "autonomous_original", "autonomous_transform"
    expected_formula: Optional[str] = None
    priority: float = 0.5
    notes: str = ""


def load_all_topics() -> List[TopicResult]:
    """Load all autonomous research results."""
    topics = []

    if not AUTONOMOUS_RESEARCH_DIR.exists():
        print(f"WARNING: Directory not found: {AUTONOMOUS_RESEARCH_DIR}")
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


def filter_promising_topics(topics: List[TopicResult], max_error: float = 0.1) -> List[TopicResult]:
    """
    Filter to topics with promising Z² matches.

    FIXED: Lower threshold (0.1% instead of 1%) to focus on real discoveries.
    """
    promising = []

    for topic in topics:
        if topic.best_match:
            error = abs(topic.best_match.get("percent_error", 100))
            if error < max_error and topic.best_match.get("has_z2", False):
                promising.append(topic)

    promising.sort(key=lambda t: abs(t.best_match.get("percent_error", 100)))
    return promising


def generate_ideas_from_topic(topic: TopicResult) -> List[DerivationIdea]:
    """
    Generate derivation ideas from a topic.

    FIXED:
    - Primary: Test ORIGINAL constant directly
    - Secondary: Only physically meaningful transforms (_sqrt, _over_pi)
    - REMOVED: Tautological transforms (_coef_plus1, _const_plus1)
    """
    if not topic.best_match:
        return []

    ideas = []
    value = topic.best_match.get("constant_value", 0)
    formula = topic.best_match.get("formula", "")
    name_base = topic.best_match.get("constant_name", "unknown").replace(" ", "_").lower()

    # IDEA 1 (PRIMARY): Test the ORIGINAL constant directly
    ideas.append(DerivationIdea(
        name=name_base,
        value=value,
        domain=topic.domain,
        source="autonomous_original",
        expected_formula=formula,
        priority=0.9,  # High priority - this is the real test
        notes=f"Original constant from {topic.topic_query}"
    ))

    # IDEA 2: Square root (dimensional analysis - physically meaningful)
    # √value might reveal simpler structure
    if value > 1:
        ideas.append(DerivationIdea(
            name=f"{name_base}_sqrt",
            value=math.sqrt(value),
            domain=topic.domain,
            source="autonomous_transform",
            priority=0.4,
            notes="Square root - dimensional reduction"
        ))

    # IDEA 3: Divided by π (for angular quantities)
    # value/π might reveal clean fractions for angles
    if value > 0 and topic.domain in ["geometry", "chemistry", "optics", "acoustics"]:
        ideas.append(DerivationIdea(
            name=f"{name_base}_over_pi",
            value=value / math.pi,
            domain=topic.domain,
            source="autonomous_transform",
            priority=0.3,
            notes="Divided by π - angular normalization"
        ))

    # REMOVED: _coef_plus1 and _const_plus1 (tautological)
    # These create targets that BY DEFINITION match Z² formulas

    return ideas


def generate_known_z2_ideas() -> List[DerivationIdea]:
    """
    Generate ideas from known Z² constants.

    These are the ground truth - constants we KNOW have Z² derivations.
    The pipeline should verify it can find these.
    """
    ideas = []

    for const in KNOWN_Z2_CONSTANTS:
        ideas.append(DerivationIdea(
            name=const["name"],
            value=const["value"],
            domain=const["domain"],
            source="known_z2",
            expected_formula=const["expected_formula"],
            priority=const["priority"],
            notes=const.get("notes", "")
        ))

    return ideas


def run_pipeline(ideas: List[DerivationIdea], output_dir: Path, max_iterations: int = 0) -> Dict:
    """Run all ideas through OlympusFlow AutonomousController."""
    from OlympusFlow.autonomous_controller import AutonomousController, DerivationTarget

    output_dir.mkdir(parents=True, exist_ok=True)

    controller = AutonomousController(output_dir=output_dir)

    # Sort by priority (highest first)
    ideas.sort(key=lambda x: -x.priority)

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
    print(f"  - Known Z² constants: {sum(1 for i in ideas if i.source == 'known_z2')}")
    print(f"  - Original constants: {sum(1 for i in ideas if i.source == 'autonomous_original')}")
    print(f"  - Transforms: {sum(1 for i in ideas if i.source == 'autonomous_transform')}")
    print("\nRunning derivations (this may take a while)...")

    total = len(ideas) if max_iterations == 0 else min(max_iterations, len(ideas))
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
    parser = argparse.ArgumentParser(description="Run fixed Z² derivation pipeline v2")
    parser.add_argument("--run", action="store_true", help="Actually run the pipeline")
    parser.add_argument("--limit", type=int, default=0, help="Limit total targets")
    parser.add_argument("--known-only", action="store_true", help="Only test known Z² constants")
    parser.add_argument("--max-error", type=float, default=0.1, help="Max error threshold (%)")
    parser.add_argument("--iterations", type=int, default=0, help="Max iterations (0=all)")
    args = parser.parse_args()

    print("=" * 70)
    print("FIXED FULL PIPELINE V2 - Z² Research System")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print()
    print("FIXES IN V2:")
    print("  ✓ Tests ORIGINAL constants directly")
    print("  ✓ Removed tautological transforms (_coef_plus1, _const_plus1)")
    print("  ✓ Added known Z² constants for verification")
    print("  ✓ Lower error threshold (0.1% vs 1%)")
    print()

    all_ideas = []

    # Step 1: Load known Z² constants (ground truth)
    print("Step 1: Loading known Z² constants...")
    known_ideas = generate_known_z2_ideas()
    print(f"  Loaded: {len(known_ideas)} known Z² constants")
    all_ideas.extend(known_ideas)

    if not args.known_only:
        # Step 2: Load autonomous research topics
        print(f"\nStep 2: Loading autonomous research results...")
        topics = load_all_topics()
        print(f"  Loaded: {len(topics)} topics")

        # Step 3: Filter promising topics
        print(f"\nStep 3: Filtering promising topics (error < {args.max_error}%)...")
        promising = filter_promising_topics(topics, max_error=args.max_error)
        print(f"  Promising: {len(promising)} topics")

        # Step 4: Generate ideas from topics
        print("\nStep 4: Generating derivation ideas...")
        for topic in promising:
            topic_ideas = generate_ideas_from_topic(topic)
            all_ideas.extend(topic_ideas)

        print(f"  Generated: {len(all_ideas)} total ideas")

    # Apply limit
    if args.limit > 0:
        all_ideas = all_ideas[:args.limit]
        print(f"\nLimited to: {len(all_ideas)} ideas")

    # Summary by source
    print("\nIdeas by source:")
    sources = {}
    for idea in all_ideas:
        sources[idea.source] = sources.get(idea.source, 0) + 1
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count}")

    # Summary by domain
    print("\nIdeas by domain:")
    domains = {}
    for idea in all_ideas:
        domains[idea.domain] = domains.get(idea.domain, 0) + 1
    for domain, count in sorted(domains.items(), key=lambda x: -x[1])[:10]:
        print(f"  {domain}: {count}")

    # Show known Z² constants
    print("\nKnown Z² constants to verify:")
    for idea in [i for i in all_ideas if i.source == "known_z2"][:10]:
        print(f"  {idea.name}: {idea.value} → {idea.expected_formula}")

    # Show top autonomous discoveries
    print("\nTop autonomous discoveries to verify:")
    auto_ideas = [i for i in all_ideas if i.source == "autonomous_original"]
    for idea in auto_ideas[:10]:
        print(f"  {idea.name}: {idea.value} → {idea.expected_formula}")

    if not args.run:
        print("\n" + "=" * 70)
        print("DRY RUN - To actually run the pipeline, use: --run")
        print("=" * 70)
        print(f"\nWould process:")
        print(f"  - {len(all_ideas)} total ideas")
        print(f"  - {len([i for i in all_ideas if i.source == 'known_z2'])} known Z² constants")
        print(f"  - {len([i for i in all_ideas if i.source == 'autonomous_original'])} original constants")
        print(f"\nEstimated time: ~{len(all_ideas) * 10 / 60:.1f} minutes (at 10s/idea)")
        return

    # Step 5: Run pipeline
    print("\n" + "=" * 70)
    print("RUNNING FIXED PIPELINE V2")
    print("=" * 70)

    output_dir = OUTPUT_DIR / f"v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    results = run_pipeline(all_ideas, output_dir, max_iterations=args.iterations)

    # Step 6: Generate report
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total processed: {results['total_processed']}")
    print(f"Successful derivations: {results['successful']}")
    print(f"First principles found: {results['first_principles']}")
    print(f"Numerology rejected: {results['numerology_rejected']}")
    print(f"New predictions generated: {results['predictions_generated']}")

    # Check if known constants were found
    print("\nKnown Z² constant verification:")
    # TODO: Read results and check which known constants were verified

    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "fixes": [
            "Tests original constants directly",
            "Removed tautological transforms",
            "Added known Z² constants",
            "Lower error threshold"
        ],
        "ideas_total": len(all_ideas),
        "ideas_by_source": sources,
        "results": results,
        "output_dir": str(output_dir)
    }

    summary_path = output_dir / "pipeline_summary_v2.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to: {summary_path}")


if __name__ == "__main__":
    main()
