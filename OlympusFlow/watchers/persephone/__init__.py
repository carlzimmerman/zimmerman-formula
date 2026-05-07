"""
PERSEPHONE - Lifecycle Orchestrator
====================================

Persephone is the Queen of the Underworld and the Orchestrator of the Data Lifecycle.
She oversees the "Seasonal" transition of findings from MnemosyneLake (Session Memory)
to their final destination.

Mythological Role:
- Lives in BOTH the Underworld AND the world of light
- This duality maps perfectly to HRM (Honesty and Rigor Metric) assessment
- Only she can handle the "Dual-Lake" logic effectively

Two Complementary Orchestrators:
- HECATE: Execution Supervisor (real-time process monitoring, crossroads)
- PERSEPHONE: Lifecycle Orchestrator (state transitions, seasonal graduations)

Persephone's Duties:

1. THE SPRING (Graduation):
   - Truths with HRM score >= 0.8 are "brought to the surface"
   - Moved from MnemosyneLake to AletheiaLake
   - Requires adversarial review before graduation
   - Must have verified provenance (verbatim quote + page number)

2. THE WINTER (Banishment):
   - Findings with high sigma tension (>3σ) or detected sycophancy
   - Cast into the appropriate Underworld Lake:
     * TartarusLake: Failed math, wrong derivations
     * LetheLake: Hallucinations, sycophantic consensus defaults
     * LabyrinthLake: Stuck but potentially valuable

3. THE HARVEST (Fine-Tuning):
   - Selects best contrastive pairs for LegomenaLLM training
   - Ensures next iteration is stronger and more rigorous

4. THE LABYRINTH THREAD:
   - When research is truly stuck, pulls in more context
   - Uses connection to "roots" of data from HECATE catalog

Author: Carl Zimmerman
Date: May 7, 2026
Version: 1.0.0
"""

from .orchestrator import (
    PersephoneOrchestrator,
    PersephoneConfig,
    Season,
    LifecycleDecision,
    GraduationResult,
    BanishmentResult
)

from .graduation import SpringGraduator
from .banishment import WinterBanisher
from .adversarial import AdversarialReviewer

__version__ = "1.0.0"
__all__ = [
    "PersephoneOrchestrator",
    "PersephoneConfig",
    "Season",
    "LifecycleDecision",
    "GraduationResult",
    "BanishmentResult",
    "SpringGraduator",
    "WinterBanisher",
    "AdversarialReviewer"
]
