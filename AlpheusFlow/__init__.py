#!/usr/bin/env python3
"""
ALPHEUSFLOW - Research Queue Orchestrator
==========================================

Named after Alpheus, the Greek river god. Rivers flow sequentially -
just like research tasks flowing through this queue.

AlpheusFlow sits ABOVE OlympusFlow and manages:
1. Research request queue (add tasks for processing)
2. Sequential execution (one task at a time through OlympusFlow)
3. Batch processing (run multiple related tasks)
4. Progress tracking and persistence
5. Results aggregation

Architecture:
```
    AlpheusFlow (Queue Orchestrator)
         |
         v
    OlympusFlow (Pipeline Runner)
         |
    +---------+---------+---------+
    v         v         v         v
 Hermes    Apollo   TruthFlow  Cyllene
 (Data)   (Analysis) (Verify)  (Deepen)
```

Quick Start:
    from AlpheusFlow import ResearchQueue, submit_task, run_queue

    # Submit tasks
    submit_task("Derive von Karman constant from Z2 geometry")
    submit_task("Derive Feigenbaum delta from cubic tessellation")

    # Process all tasks
    run_queue()

Author: Carl Zimmerman
Date: May 5, 2026
"""

__version__ = "1.0.0"

from .queue import (
    ResearchQueue,
    ResearchTask,
    TaskStatus,
    TaskPriority,
    BatchConfig
)

from .orchestrator import (
    AlpheusOrchestrator,
    run_queue,
    submit_task,
    get_queue_status,
    pause_queue,
    resume_queue
)

__all__ = [
    "__version__",

    # Queue management
    "ResearchQueue",
    "ResearchTask",
    "TaskStatus",
    "TaskPriority",
    "BatchConfig",

    # Orchestrator
    "AlpheusOrchestrator",
    "run_queue",
    "submit_task",
    "get_queue_status",
    "pause_queue",
    "resume_queue"
]
