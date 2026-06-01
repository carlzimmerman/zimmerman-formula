#!/usr/bin/env python3
"""
Setup script for overnight OlympusFlow run with legomena-xl.
Merges all topics and creates fresh queue.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime

# Paths
BASE = Path(__file__).parent
CURATED_V3 = BASE / "OlympusFlow/discoveries/curated_topics_v3.json"
ANOMALIES = BASE / "OlympusFlow/discoveries/physics_anomalies_200.json"
QUEUE_STATE = BASE / "AlpheusFlow/queue_state.json"
ALL_TOPICS = BASE / "OlympusFlow/discoveries/all_topics_overnight.json"

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def topic_to_task(topic, priority=2):
    """Convert a topic dict to a research task."""
    name = topic.get("name", "unknown")
    task_id = str(uuid.uuid4())[:8]

    # Build description
    desc_parts = [topic.get("description", "")]
    if "physical_context" in topic:
        desc_parts.append(f"Physical context: {topic['physical_context']}")
    if "z2_hint" in topic:
        desc_parts.append(f"Z² hint: {topic['z2_hint']}")

    description = " ".join(desc_parts) if desc_parts[0] else name

    # Get target value
    target_value = topic.get("target_value", topic.get("value", 0.0))
    if target_value is None:
        target_value = 0.0

    return {
        "id": task_id,
        "name": name.lower().replace(" ", "_").replace("-", "_"),
        "description": description,
        "category": topic.get("category", topic.get("domain", "general")),
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "started_at": "",
        "completed_at": "",
        "elapsed_seconds": 0,
        "result": {},
        "error": "",
        "output_path": "",
        "target_constant": name,
        "target_value": float(target_value) if target_value else 0.0,
        "domain": topic.get("domain", topic.get("category", "physics")),
        "quantities": []
    }

def main():
    print("=" * 60)
    print("OVERNIGHT RUN SETUP")
    print("=" * 60)

    # Load curated topics
    print("\n1. Loading curated topics v3...")
    curated = load_json(CURATED_V3)
    curated_topics = curated.get("topics", [])
    print(f"   Found {len(curated_topics)} curated topics")

    # Load anomalies
    print("\n2. Loading physics anomalies...")
    anomalies = load_json(ANOMALIES)
    anomaly_topics = anomalies.get("topics", [])
    print(f"   Found {len(anomaly_topics)} anomaly topics")

    # Merge - anomalies get higher priority (1)
    print("\n3. Merging topics...")
    all_topics = []
    seen_names = set()

    # Add anomalies first (higher priority)
    for topic in anomaly_topics:
        name = topic.get("name", "").lower()
        if name and name not in seen_names:
            all_topics.append(topic)
            seen_names.add(name)

    # Add curated topics (normal priority)
    for topic in curated_topics:
        name = topic.get("name", "").lower()
        if name and name not in seen_names:
            all_topics.append(topic)
            seen_names.add(name)

    print(f"   Total unique topics: {len(all_topics)}")

    # Save merged topics
    save_json(ALL_TOPICS, {
        "metadata": {
            "created": datetime.now().isoformat(),
            "description": "All topics for overnight run",
            "total_topics": len(all_topics)
        },
        "topics": all_topics
    })
    print(f"   Saved to: {ALL_TOPICS}")

    # Create queue tasks
    print("\n4. Creating queue tasks...")
    tasks = []

    # Anomalies get priority 1 (HIGH)
    for topic in anomaly_topics:
        name = topic.get("name", "").lower()
        if name:
            tasks.append(topic_to_task(topic, priority=1))

    # Curated get priority 2 (NORMAL)
    for topic in curated_topics:
        name = topic.get("name", "").lower()
        if name and name not in {t.get("name", "").lower() for t in anomaly_topics}:
            tasks.append(topic_to_task(topic, priority=2))

    print(f"   Created {len(tasks)} tasks")

    # Save queue state
    queue_state = {"tasks": tasks}
    save_json(QUEUE_STATE, queue_state)
    print(f"   Saved to: {QUEUE_STATE}")

    # Summary
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print(f"\nTotal tasks: {len(tasks)}")
    print(f"  - Anomalies (priority 1): {len(anomaly_topics)}")
    print(f"  - Curated (priority 2): {len(tasks) - len(anomaly_topics)}")

    print("\nTo run the daemon:")
    print("  LEGOMENA_MODEL=carl_zimmerman/legomena-xl python -m OlympusFlow.daemon --mode continuous")

if __name__ == "__main__":
    main()
