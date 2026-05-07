"""
CYLLENEFLOW - Iterative Learning Layer
=======================================

Named after Cyllene, the nymph who nursed Hermes on Mount Cyllene.
Like her nurturing role, this flow nurtures discoveries through
iterative learning and recursive deepening.

Components:
- TruthStore: Persistent storage for validated discoveries
- TrainingGenerator: Converts truths to training examples
- ModelUpdater: Fine-tunes LegomenaLLM (with cleanup!)
- IterationRunner: Orchestrates experiments
- Deepener: Recursive research decision engine
- BatchDeepener: Coordinates deepening across findings

Key Features:
- RECURSIVE DEEPENING: When significant findings are discovered,
  automatically generates research questions and investigates deeper
- MODEL CLEANUP: Prevents storage clutter by keeping only base + latest
- BATCH PROCESSING: Groups moderate findings before deepening

Usage:
    from OlympusFlow.flows.cyllene import IterationRunner

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

from .truth_store import TruthStore
from .training_generator import TrainingGenerator
from .model_updater import ModelUpdater
from .iteration_runner import IterationRunner
from .deepener import Deepener, BatchDeepener, ResearchQuestion, DeepeningDecision

__all__ = [
    "__version__",
    "TruthStore",
    "TrainingGenerator",
    "ModelUpdater",
    "IterationRunner",
    "Deepener",
    "BatchDeepener",
    "ResearchQuestion",
    "DeepeningDecision"
]
