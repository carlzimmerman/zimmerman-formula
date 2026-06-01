"""
ALPHEUSFLOW - Research Queue Orchestrator
==========================================

DEPRECATED: This module has moved to OlympusFlow.flows.alpheus

Please update imports:
    OLD: from AlpheusFlow import ResearchQueue
    NEW: from OlympusFlow.flows.alpheus import ResearchQueue

    OR: from OlympusFlow.flows import ResearchQueue

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "AlpheusFlow has moved to OlympusFlow.flows.alpheus. "
    "Please update imports: from OlympusFlow.flows.alpheus import ResearchQueue",
    DeprecationWarning,
    stacklevel=2
)

__version__ = "3.0.0"

# Re-export from new location
from OlympusFlow.flows.alpheus import (
    ResearchQueue,
    ResearchTask,
    TaskStatus,
    TaskPriority,
    BatchConfig,
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
