"""
CylleneFlow v1.0.0
==================

Iterative Learning Layer for Z² Discovery

Components:
- TruthStore: Persistent storage for validated discoveries
- TrainingGenerator: Converts truths to training examples
- ModelUpdater: Fine-tunes LegomenaLLM
- IterationRunner: Orchestrates experiments

Usage:
    from cylleneflow import IterationRunner

    runner = IterationRunner(
        domain="glaciology",
        topic="Swiss Alps glaciers",
        max_iterations=10
    )
    results = runner.run()
"""

__version__ = "1.0.0"
__author__ = "Carl Zimmerman"

from .truth_store import TruthStore
from .training_generator import TrainingGenerator
from .model_updater import ModelUpdater
from .iteration_runner import IterationRunner

__all__ = [
    "TruthStore",
    "TrainingGenerator",
    "ModelUpdater",
    "IterationRunner"
]
