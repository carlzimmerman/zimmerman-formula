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
                    │  Hecate: Stage transition auditor    │
                    │  [Future: Argus, Cerberus, etc.]    │
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
    │ Cyllene │    │                     │    │         │
    └─────────┘    └─────────────────────┘    └─────────┘
```

Design Principles:
1. NON-BLOCKING by default (observes, doesn't halt)
2. BLOCKING only on critical issues (HRM < threshold, contradictions)
3. DUAL-LENS perspective (external API + local Legomena)
4. IMMUTABLE audit trail (watcher notes cannot be deleted)
5. REAL-TIME monitoring (hooks into stage transitions)

Watcher Types:
- Hecate: Primary supervisor, consensus + framework verification
- [Future] Argus: Multi-source correlation checker
- [Future] Cerberus: Entry/exit guardian for lakes

Usage:
    from OlympusFlow.watchers import HecateWatcher, WatcherConfig

    # Create watcher
    hecate = HecateWatcher(config=WatcherConfig(
        blocking_threshold=0.5,
        dual_model=True
    ))

    # Attach to pipeline
    pipeline.attach_watcher(hecate)

    # Run pipeline (Hecate watches all transitions)
    results = pipeline.run()
"""

__version__ = "1.0.0"

# Core contracts
from .contracts import (
    WatcherConfig, WatcherResult, WatcherNote, StageTransition,
    InterventionType, TrustLevel, WatcherPriority, ConsensusSource,
    ConsensusCheck, FrameworkCheck
)

# Base watcher
from .base import BaseWatcher

# Hecate watcher
from .hecate import HecateWatcher, HecatePrompts, ConsensusBridge, FrameworkValidator

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
    # Hecate
    "HecateWatcher",
    "HecatePrompts",
    "ConsensusBridge",
    "FrameworkValidator",
]
