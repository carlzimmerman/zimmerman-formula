#!/usr/bin/env python3
"""
LOAD Z² FIRST-PRINCIPLES DERIVATION TASKS v2.0
================================================

Loads refined research topics that focus on FIRST-PRINCIPLES DERIVATIONS,
not formula fitting. These topics require physical mechanism explanations
and computational verification.

Key difference from v1:
- v1: "Find any formula that matches constant X"
- v2: "Derive from Z² geometry WHY constant X has this value"

Author: Carl Zimmerman
Date: May 7, 2026
"""

import json
from pathlib import Path
from datetime import datetime

from .queue import ResearchQueue, ResearchTask, TaskPriority, TaskStatus


def load_v2_firstprinciples_tasks(queue: ResearchQueue, clear_existing: bool = True):
    """Load the v2 first-principles research topics into the queue."""

    # Load the research topics JSON
    topics_file = Path(__file__).parent.parent.parent / "research_topics_v2_firstprinciples.json"

    if not topics_file.exists():
        raise FileNotFoundError(f"Research topics file not found: {topics_file}")

    with open(topics_file) as f:
        topics_data = json.load(f)

    if clear_existing:
        # Clear existing tasks by setting to empty list
        queue.tasks = []
        print(f"[LoadV2] Cleared existing queue")

    tasks_added = 0

    # Priority mapping for tiers
    tier_priorities = {
        "tier1_verified": TaskPriority.CRITICAL,      # Known Z² derivations
        "tier2_strong_candidates": TaskPriority.HIGH,  # Plausible Z² connections
        "tier3_geometric_derivations": TaskPriority.NORMAL,  # Geometric derivations
        "tier4_pmns_ckm_angles": TaskPriority.NORMAL,  # Mixing angles
        "tier5_physical_constants_investigation": TaskPriority.LOW,  # Investigation
        "tier6_skeptical_tests": TaskPriority.BACKGROUND,  # Numerology tests
    }

    for tier_name, tier_data in topics_data.get("categories", {}).items():
        tier_desc = tier_data.get("description", "")
        topics = tier_data.get("topics", [])
        priority = tier_priorities.get(tier_name, TaskPriority.NORMAL)

        print(f"\n[LoadV2] Loading {tier_name}: {len(topics)} topics ({tier_desc})")

        for topic in topics:
            task = ResearchTask(
                id="",  # Auto-generate
                name=topic["name"],
                description=topic["question"],
                category=tier_name,
                priority=priority,
                status=TaskStatus.PENDING,
                target_constant=topic["name"].replace("_", " ").title(),
                target_value=float(topic["target_value"]) if isinstance(topic["target_value"], (int, float)) else 0.0,
                domain="z2_firstprinciples"
            )

            # Store expected formula and verification in metadata
            task.result = {
                "expected_formula": topic.get("expected_formula", ""),
                "verification": topic.get("verification", ""),
                "methodology": "first_principles_derivation"
            }

            queue.add_task(task)
            tasks_added += 1

    queue.save()
    print(f"\n[LoadV2] Loaded {tasks_added} first-principles derivation tasks")
    print(f"[LoadV2] Queue saved to: {queue.persistence_path}")

    return tasks_added


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Load v2 first-principles research topics")
    parser.add_argument("--output", "-o", default="AlpheusFlow/queue_state.json",
                       help="Queue state file path")
    parser.add_argument("--keep-existing", action="store_true",
                       help="Don't clear existing tasks")

    args = parser.parse_args()

    queue = ResearchQueue(persistence_path=args.output)
    load_v2_firstprinciples_tasks(queue, clear_existing=not args.keep_existing)


if __name__ == "__main__":
    main()
