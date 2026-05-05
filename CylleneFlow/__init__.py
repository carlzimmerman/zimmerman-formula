"""
CylleneFlow v1.3.0
==================

Iterative Learning Layer for Z² Discovery

Components:
- TruthStore: Persistent storage for validated discoveries
- TrainingGenerator: Converts truths to training examples
- ModelUpdater: Fine-tunes LegomenaLLM (with cleanup!)
- IterationRunner: Orchestrates experiments
- Deepener: Recursive research decision engine (NEW in v1.3.0)
- BatchDeepener: Coordinates deepening across findings (NEW in v1.3.0)

Key v1.3.0 Features:
- RECURSIVE DEEPENING: When significant findings are discovered,
  automatically generates research questions and investigates deeper
- MODEL CLEANUP: Prevents storage clutter by keeping only base + latest
- BATCH PROCESSING: Groups moderate findings before deepening

Usage:
    from CylleneFlow import IterationRunner

    runner = IterationRunner(
        domain="seismology",
        topic="Earthquake magnitude patterns",
        max_iterations=10
    )
    results = runner.run()

    # After experiment: cleanup intermediate models
    runner.cleanup_models()

    # Or consolidate all knowledge into single model
    runner.consolidate_knowledge()
"""

__version__ = "1.3.0"
__author__ = "Carl Zimmerman"

from .truth_store import TruthStore
from .training_generator import TrainingGenerator
from .model_updater import ModelUpdater
from .iteration_runner import IterationRunner
from .deepener import Deepener, BatchDeepener, ResearchQuestion, DeepeningDecision

__all__ = [
    "TruthStore",
    "TrainingGenerator",
    "ModelUpdater",
    "IterationRunner",
    "Deepener",
    "BatchDeepener",
    "ResearchQuestion",
    "DeepeningDecision"
]
