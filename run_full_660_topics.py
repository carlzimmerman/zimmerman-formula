#!/usr/bin/env python3
"""
FULL 660 TOPICS RUN - With Persephone Lifecycle
================================================

Runs the complete OlympusFlow pipeline on all 660 science topics
discovered during autonomous research, with full Persephone lifecycle
management.

Duration: ~6-12 hours depending on LLM speed
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Ensure imports work
sys.path.insert(0, str(Path(__file__).parent))

def load_all_topics():
    """Load all 660 topics from autonomous research."""
    topics_dir = Path("OlympusFlow/discoveries/autonomous_research")
    topics = []

    for f in sorted(topics_dir.glob("*.json")):
        if f.name == "research_summary.json":
            continue
        if f.name.startswith("AUTONOMOUS"):
            continue

        try:
            data = json.loads(f.read_text())

            # Extract topic info
            topic = {
                "name": data.get("constant_name", f.stem),
                "target_value": data.get("experimental_value", data.get("value", 0)),
                "domain": data.get("domain", "physics"),
                "description": data.get("description", ""),
                "source": data.get("source", ""),
                "z2_patterns": data.get("z2_patterns", []),
                "category": "autonomous_discovery"
            }

            # Create a research question
            if not topic["description"]:
                topic["description"] = f"Investigate Z² connections for {topic['name']} = {topic['target_value']}"

            topics.append(topic)

        except Exception as e:
            print(f"Error loading {f}: {e}")
            continue

    return topics


def create_queue_tasks(topics):
    """Convert topics to queue tasks."""
    import hashlib
    from OlympusFlow.flows.alpheus import ResearchTask, TaskPriority

    tasks = []
    for i, topic in enumerate(topics):
        # Create detailed assignment
        z2_hints = ""
        if topic.get("z2_patterns"):
            patterns = topic["z2_patterns"][:3]  # Top 3 patterns
            z2_hints = f" Known Z² patterns to investigate: {patterns}"

        assignment = (
            f"Derive the value {topic['name']} = {topic['target_value']} from Z² = 32π/3 first principles. "
            f"{topic['description']}"
            f"{z2_hints} "
            f"Focus on: (1) Physical mechanism connecting to Z², (2) Algebraic derivation, "
            f"(3) Verification against experimental value."
        )

        # Generate unique ID
        task_id = hashlib.md5(topic["name"].encode()).hexdigest()[:8]

        task = ResearchTask(
            id=task_id,
            name=topic["name"],
            description=assignment,
            category=topic.get("category", "physics"),
            priority=TaskPriority.NORMAL,
            target_value=topic.get("target_value", 0),
            domain=topic.get("domain", "physics")
        )
        tasks.append(task)

    return tasks


def main():
    print("=" * 70)
    print("OLYMPUSFLOW - FULL 660 TOPICS RUN")
    print("With Persephone Lifecycle Orchestrator")
    print("=" * 70)
    print()

    # Load topics
    print("Loading 660 science topics...")
    topics = load_all_topics()
    print(f"Loaded {len(topics)} topics")

    # Show domain distribution
    domains = {}
    for t in topics:
        d = t.get("domain", "unknown")
        domains[d] = domains.get(d, 0) + 1

    print("\nDomain distribution:")
    for d, count in sorted(domains.items(), key=lambda x: -x[1])[:10]:
        print(f"  {d}: {count}")

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"daemon_outputs/full_660_run_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nOutput directory: {output_dir}")

    # Create tasks
    print("\nCreating queue tasks...")
    tasks = create_queue_tasks(topics)
    print(f"Created {len(tasks)} tasks")

    # Initialize queue
    from OlympusFlow.flows.alpheus import ResearchQueue
    queue = ResearchQueue(persistence_path=str(output_dir / "queue_state.json"))

    # Clear and reload
    queue.tasks = {}
    queue.task_order = []

    for task in tasks:
        queue.add(task)

    print(f"Queue loaded: {len(queue.tasks)} tasks")

    # Save config
    config_info = {
        "timestamp": datetime.now().isoformat(),
        "total_topics": len(topics),
        "domains": domains,
        "persephone_enabled": True,
        "persephone_periodic_interval": 50,  # Review every 50 tasks
        "hrm_threshold": 0.80,
        "adversarial_threshold": 0.60
    }
    (output_dir / "run_config.json").write_text(json.dumps(config_info, indent=2))

    print("\n" + "=" * 70)
    print("STARTING DAEMON")
    print("=" * 70)
    print()
    print("Run command:")
    print(f"  nohup python3 -m OlympusFlow.daemon \\")
    print(f"    --mode timed \\")
    print(f"    --duration 43200 \\")  # 12 hours
    print(f"    --output {output_dir} \\")
    print(f"    --verbose > {output_dir}/daemon.log 2>&1 &")
    print()

    # Actually start it
    import subprocess

    cmd = [
        "nohup", "python3", "-m", "OlympusFlow.daemon",
        "--mode", "timed",
        "--duration", "43200",  # 12 hours
        "--output", str(output_dir),
        "--verbose"
    ]

    log_file = open(output_dir / "daemon.log", "w")
    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True
    )

    print(f"Daemon started with PID: {process.pid}")
    print(f"Log file: {output_dir}/daemon.log")
    print()
    print("Monitor with:")
    print(f"  tail -f {output_dir}/daemon.log")
    print()
    print("Check status with:")
    print(f"  ps aux | grep {process.pid}")
    print()

    # Save PID
    (output_dir / "daemon.pid").write_text(str(process.pid))

    return process.pid


if __name__ == "__main__":
    pid = main()
    print(f"\nDaemon running as PID {pid}")
    print("This script will now exit. The daemon continues in background.")
