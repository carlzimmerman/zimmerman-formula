#!/usr/bin/env python3
"""
START 100-HOUR OLYMPUSFLOW RUN
==============================

Configuration: v2.0 First-Principles Derivation Mode
- Topics: research_topics_v2_firstprinciples.json (25+ curated topics)
- Mode: Scientific method with HRM validation
- Duration: 100 hours (360,000 seconds)
- Output naming: olympus_run_{config}_{timestamp}

Author: Carl Zimmerman
Date: May 7, 2026
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
RUN_CONFIG = {
    "version": "2.0.0",
    "name": "firstprinciples_derivation",
    "methodology": "scientific_method_z2",
    "topics_version": "v2_firstprinciples",
    "duration_hours": 100,
    "require_physical_mechanism": True,
    "reject_numerology": True,
    "min_confidence": 0.85,
}

def main():
    # Timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create descriptive output folder name
    output_name = f"olympus_run_v{RUN_CONFIG['version']}_{RUN_CONFIG['name']}_{timestamp}"
    output_dir = Path("daemon_outputs") / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("OLYMPUSFLOW 100-HOUR RUN CONFIGURATION")
    print("=" * 70)
    print(f"Run ID: {output_name}")
    print(f"Topics: v2 First-Principles Derivation (25+ curated)")
    print(f"Duration: {RUN_CONFIG['duration_hours']} hours ({RUN_CONFIG['duration_hours'] * 3600}s)")
    print(f"Output: {output_dir}")
    print(f"Methodology: {RUN_CONFIG['methodology']}")
    print("=" * 70)

    # Save run config
    config_file = output_dir / "run_config.json"
    with open(config_file, 'w') as f:
        json.dump({
            **RUN_CONFIG,
            "timestamp": timestamp,
            "output_dir": str(output_dir),
            "start_time": datetime.now().isoformat()
        }, f, indent=2)
    print(f"Config saved: {config_file}")

    # Step 1: Load v2 first-principles topics
    print("\n[1/3] Loading v2 first-principles research topics...")
    try:
        # Add parent to path
        sys.path.insert(0, str(Path(__file__).parent))

        # Import and load topics
        from OlympusFlow.flows.alpheus.queue import ResearchQueue
        from OlympusFlow.flows.alpheus.load_v2_firstprinciples import load_v2_firstprinciples_tasks

        queue = ResearchQueue(persistence_path=str(output_dir / "queue_state.json"))
        tasks_added = load_v2_firstprinciples_tasks(queue, clear_existing=True)
        print(f"[1/3] Loaded {tasks_added} first-principles tasks")

    except Exception as e:
        print(f"[1/3] Error loading topics: {e}")
        print("[1/3] Will use existing queue")

    # Step 2: Build daemon command
    print("\n[2/3] Configuring daemon...")
    duration_seconds = RUN_CONFIG['duration_hours'] * 3600  # 360,000 seconds

    cmd = [
        "python3", "-m", "OlympusFlow.daemon",
        "--mode", "timed",
        "--duration", str(duration_seconds),
        "--output", str(output_dir),
        "--verbose"
    ]

    print(f"Command: {' '.join(cmd)}")

    # Step 3: Start daemon
    print("\n[3/3] Starting OlympusFlow daemon...")
    print(f"Log file: {output_dir / 'daemon.log'}")
    print("\nDaemon is running. Use Ctrl+C to stop.")
    print("-" * 70)

    # Run daemon with output to log file
    log_file = output_dir / "daemon.log"
    with open(log_file, 'w') as logf:
        # Write header
        logf.write(f"OlympusFlow Run: {output_name}\n")
        logf.write(f"Started: {datetime.now().isoformat()}\n")
        logf.write(f"Config: {json.dumps(RUN_CONFIG, indent=2)}\n")
        logf.write("=" * 70 + "\n\n")
        logf.flush()

        try:
            # Run daemon - output to both console and log
            import subprocess
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=str(Path(__file__).parent)
            )

            # Stream output
            for line in process.stdout:
                print(line, end='')
                logf.write(line)
                logf.flush()

            process.wait()

        except KeyboardInterrupt:
            print("\n\n[INTERRUPTED] Stopping daemon...")
            process.terminate()
            process.wait()

        # Write end marker
        logf.write("\n" + "=" * 70 + "\n")
        logf.write(f"Ended: {datetime.now().isoformat()}\n")

    print(f"\nRun complete. Results in: {output_dir}")


if __name__ == "__main__":
    main()
