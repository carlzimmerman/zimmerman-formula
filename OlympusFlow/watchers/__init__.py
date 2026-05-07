"""
OLYMPUSFLOW WATCHERS - Autonomous Oversight System
====================================================

Watchers are middleware supervisors that observe and audit the research
pipeline in real-time. Unlike flows (which process data) or lakes (which
store data), watchers OVERSEE transitions between stages.

Architecture:
```
                    ┌─────────────────────────────────────┐
                    │           WATCHERS                   │
                    │  (Middleware Supervisors)            │
                    ├─────────────────────────────────────┤
                    │  Hecate: Execution supervisor        │
                    │  Persephone: Lifecycle orchestrator  │
                    └─────────────────────────────────────┘
                              │
                              │ intercepts & audits
                              ▼
    ┌─────────┐    ┌─────────────────────┐    ┌─────────┐
    │  FLOWS  │───►│  STAGE TRANSITION   │───►│  LAKES  │
    │         │    │                     │    │         │
    │ Hermes  │    │  StageResult object │    │ Aletheia│
    │ Metis   │    │  passes through     │    │Mnemosyne│
    │ Truth   │    │  watcher validation │    │ Helicon │
    │ Cyllene │    │                     │    │Tartarus │
    └─────────┘    └─────────────────────┘    │ Lethe   │
                                              │Labyrinth│
                                              └─────────┘

Two Complementary Orchestrators:
--------------------------------
1. HECATE (Execution Supervisor):
   - Real-time process monitoring
   - Stage transition validation
   - Consensus checking during research
   - Halts on critical issues

2. PERSEPHONE (Lifecycle Orchestrator):
   - State transitions between lakes
   - Seasonal graduation/banishment cycles
   - Training data harvest
   - Spring: Graduation to AletheiaLake (HRM >= 0.80)
   - Winter: Banishment to Tartarus/Lethe/Labyrinth
   - Autumn: Harvest contrastive pairs for training

Design Principles:
1. NON-BLOCKING by default (observes, doesn't halt)
2. BLOCKING only on critical issues (HRM < threshold, contradictions)
3. DUAL-LENS perspective (external API + local Legomena)
4. IMMUTABLE audit trail (watcher notes cannot be deleted)
5. REAL-TIME monitoring (hooks into stage transitions)

Usage:
    from OlympusFlow.watchers import HecateWatcher, WatcherConfig
    from OlympusFlow.watchers.persephone import PersephoneOrchestrator

    # Hecate for real-time oversight
    hecate = HecateWatcher(config=WatcherConfig(
        blocking_threshold=0.5,
        dual_model=True
    ))

    # Persephone for lifecycle management
    persephone = PersephoneOrchestrator()

    # Run pipeline with Hecate watching
    results = pipeline.run()

    # Run Persephone seasonal cycle at end of session
    cycle_stats = persephone.run_seasonal_cycle()
"""

__version__ = "3.1.0"

# Core contracts
from .contracts import (
    WatcherConfig, WatcherResult, WatcherNote, StageTransition,
    InterventionType, TrustLevel, WatcherPriority, ConsensusSource,
    ConsensusCheck, FrameworkCheck
)

# Base watcher
from .base import BaseWatcher

# Hecate watcher (Execution Supervisor)
from .hecate import HecateWatcher, HecatePrompts, ConsensusBridge, FrameworkValidator

# Persephone orchestrator (Lifecycle Orchestrator)
from .persephone import (
    PersephoneOrchestrator,
    PersephoneConfig,
    Season,
    LifecycleDecision,
    GraduationResult,
    BanishmentResult,
    SpringGraduator,
    WinterBanisher,
    AdversarialReviewer
)

__all__ = [
    "__version__",
    # Contracts
    "WatcherConfig",
    "WatcherResult",
    "WatcherNote",
    "StageTransition",
    "InterventionType",
    "TrustLevel",
    "WatcherPriority",
    "ConsensusSource",
    "ConsensusCheck",
    "FrameworkCheck",
    # Base
    "BaseWatcher",
    # Hecate (Execution Supervisor)
    "HecateWatcher",
    "HecatePrompts",
    "ConsensusBridge",
    "FrameworkValidator",
    # Persephone (Lifecycle Orchestrator)
    "PersephoneOrchestrator",
    "PersephoneConfig",
    "Season",
    "LifecycleDecision",
    "GraduationResult",
    "BanishmentResult",
    "SpringGraduator",
    "WinterBanisher",
    "AdversarialReviewer",
]
