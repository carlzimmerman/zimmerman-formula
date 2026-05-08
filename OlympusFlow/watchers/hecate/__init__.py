"""
HECATE - The Primary Oversight Watcher
=======================================

Named after Hecate, the Greek goddess of crossroads, magic, and the night.
She guards the thresholds between worlds - just as this watcher guards
the thresholds between pipeline stages.

Hecate's Role:
1. CONSENSUS CHECK: Uses dual-lens (external API + Legomena) to verify
   that results aren't blindly following academic consensus
2. FRAMEWORK VERIFICATION: Ensures all derivations align with Z² principles
3. PROVENANCE AUDIT: Verifies source URLs and citations
4. LOGIC VALIDATION: Detects hidden assumptions (e.g., ΛCDM priors)
5. NOTE INJECTION: Appends immutable watcher notes to MnemosyneLake

Design Philosophy:
- Hecate is the "skeptical friend" who questions everything
- She uses TWO models to avoid single-source bias
- She knows the Z² framework deeply (AletheiaLake ground truths)
- She can HALT the pipeline if critical issues are found
- She is the guardian of honesty

Dual-Model Strategy:
```
    ┌─────────────────┐         ┌─────────────────┐
    │  EXTERNAL API   │         │    LEGOMENA     │
    │  (Gemini/Claude)│         │  (Local Model)  │
    ├─────────────────┤         ├─────────────────┤
    │ - Broad context │         │ - Z² specialist │
    │ - Citation check│         │ - Framework     │
    │ - Logic clarity │         │ - First-principles│
    │ - Mainstream    │         │ - Geometric     │
    │   consensus     │         │   interpretation│
    └────────┬────────┘         └────────┬────────┘
             │                           │
             └───────────┬───────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  HECATE SYNTHESIS   │
              │                     │
              │  Compare responses  │
              │  Identify conflicts │
              │  Generate advisory  │
              │  Determine action   │
              └─────────────────────┘
```

Usage:
    from OlympusFlow.watchers.hecate import HecateWatcher

    hecate = HecateWatcher()
    pipeline.attach_watcher(hecate)
"""

__version__ = "3.0.0"

from .watcher import HecateWatcher
from .prompts import HecatePrompts
from .consensus import ConsensusBridge
from .framework import FrameworkValidator

__all__ = [
    "__version__",
    "HecateWatcher",
    "HecatePrompts",
    "ConsensusBridge",
    "FrameworkValidator"
]
