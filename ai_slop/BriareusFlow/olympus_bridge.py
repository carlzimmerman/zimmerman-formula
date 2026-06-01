#!/usr/bin/env python3
"""
OLYMPUS BRIDGE - Integration with OlympusFlow
===============================================

Connects BriareusFlow (exploratory) with OlympusFlow (validating).

Data Flow:
┌────────────────┐         ┌─────────────────┐
│  OLYMPUSFLOW   │         │   BRIAREUSFLOW  │
│  (Validation)  │◀────────│  (Exploration)  │
│                │         │                 │
│  - First       │ promote │  - Brute force  │
│    principles  │◀────────│    patterns     │
│  - Rigorous    │         │  - Alternatives │
│    derivation  │         │  - Geometric    │
│  - HRM scoring │         │    meaning      │
└────────────────┘         └─────────────────┘
        │                          ▲
        │    phenomenological      │
        └──────────────────────────┘
             needs investigation

Author: Carl Zimmerman
Date: May 6, 2026
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .phenomenological import (
    PhenomenologicalFinding,
    FindingCategory,
    NumerologyRisk
)
from .briareus_controller import (
    BriareusController,
    SearchConfig,
    SearchTarget,
    SearchPriority,
    BriareusResult
)


@dataclass
class BridgeConfig:
    """Configuration for OlympusBridge."""
    # When to send to OlympusFlow
    max_error_for_promotion: float = 1.0
    min_confidence_for_promotion: float = 0.7
    require_mechanism: bool = False

    # What to receive from OlympusFlow
    accept_phenomenological: bool = True
    accept_empirical: bool = True
    accept_matches: bool = True

    # Priority mapping
    default_priority: SearchPriority = SearchPriority.NORMAL


class OlympusBridge:
    """
    Bridge between BriareusFlow and OlympusFlow.

    Handles bidirectional communication:
    - Receives phenomenological findings from OlympusFlow
    - Sends promising patterns back for rigorous validation
    """

    def __init__(self, config: Optional[BridgeConfig] = None, verbose: bool = True):
        self.config = config or BridgeConfig()
        self.verbose = verbose

        # Track what we've sent/received
        self.received_from_olympus: List[Dict] = []
        self.promoted_to_olympus: List[PhenomenologicalFinding] = []

    def _log(self, msg: str):
        if self.verbose:
            print(f"[OlympusBridge] {msg}")

    def receive_from_olympusflow(self, olympus_results: List[Dict]) -> List[SearchTarget]:
        """
        Receive results from OlympusFlow and convert to search targets.

        Args:
            olympus_results: List of OlympusFlow derivation results

        Returns:
            List of SearchTargets for BriareusFlow
        """
        targets = []

        for result in olympus_results:
            category = result.get("category", "")

            # Filter by category
            if category == "phenomenological" and not self.config.accept_phenomenological:
                continue
            if category == "empirical" and not self.config.accept_empirical:
                continue
            if category == "matches" and not self.config.accept_matches:
                continue

            # Skip numerology
            if result.get("numerology_risk") == "very_high":
                continue

            # Convert to search target
            priority = self._determine_priority(result)

            target = SearchTarget(
                target_id=f"olympus_{result.get('constant_name', 'unknown').replace(' ', '_')}",
                name=result.get("constant_name", "Unknown"),
                value=result.get("experimental_value", 0),
                uncertainty=result.get("uncertainty", 0.001),
                source=result.get("source", "OlympusFlow"),
                domain=result.get("domain", "physics"),
                priority=priority,
                metadata={
                    "olympus_result": result,
                    "original_hrm_score": result.get("hrm_score", 0),
                    "original_category": category
                }
            )
            targets.append(target)

        self.received_from_olympus.extend(olympus_results)
        self._log(f"Received {len(targets)} targets from OlympusFlow")

        return targets

    def _determine_priority(self, result: Dict) -> SearchPriority:
        """Determine search priority based on OlympusFlow result."""
        hrm = result.get("hrm_score", 0)
        category = result.get("category", "")

        if hrm > 0.8:
            return SearchPriority.HIGH
        elif hrm > 0.6:
            return SearchPriority.NORMAL
        elif category == "phenomenological":
            return SearchPriority.NORMAL
        else:
            return SearchPriority.LOW

    def promote_to_olympusflow(self, finding: PhenomenologicalFinding) -> Optional[Dict]:
        """
        Promote a BriareusFlow finding to OlympusFlow for validation.

        Args:
            finding: A promising phenomenological finding

        Returns:
            Dict formatted for OlympusFlow input, or None if not promoted
        """
        # Check promotion criteria
        if finding.percent_error > self.config.max_error_for_promotion:
            return None

        # Only reject VERY_HIGH risk, allow HIGH for further investigation
        if finding.numerology_risk == NumerologyRisk.VERY_HIGH:
            return None

        # Z² findings get priority promotion
        is_z2 = "Z²" in finding.formula or "Z^2" in finding.formula

        # Create OlympusFlow input format
        olympus_input = {
            "constant_name": finding.name,
            "experimental_value": finding.experimental_value,
            "uncertainty": finding.experimental_uncertainty,
            "source": f"BriareusFlow: {finding.experimental_source}",
            "domain": finding.domain,
            "suggested_formula": finding.formula,
            "suggested_value": finding.computed_value,
            "briareus_metadata": {
                "finding_id": finding.finding_id,
                "percent_error": finding.percent_error,
                "discovery_path": finding.discovery_path.to_dict(),
                "is_z2_pattern": is_z2,
                "alternatives_count": len(finding.alternative_fits),
                "mechanism_proposed": finding.mechanism_description
            }
        }

        self.promoted_to_olympus.append(finding)
        self._log(f"Promoted {finding.name}: {finding.formula} to OlympusFlow")

        return olympus_input

    def batch_promote(self, findings: List[PhenomenologicalFinding]) -> List[Dict]:
        """
        Promote multiple findings to OlympusFlow.

        Args:
            findings: List of findings to promote

        Returns:
            List of OlympusFlow inputs
        """
        olympus_inputs = []

        for finding in findings:
            result = self.promote_to_olympusflow(finding)
            if result:
                olympus_inputs.append(result)

        self._log(f"Batch promoted {len(olympus_inputs)}/{len(findings)} findings")
        return olympus_inputs

    def get_z2_candidates_for_olympus(self, findings: List[PhenomenologicalFinding]) -> List[Dict]:
        """
        Get Z² pattern findings specifically for OlympusFlow validation.

        Z² patterns are the core focus - these get priority handling.
        """
        z2_findings = [f for f in findings if "Z²" in f.formula or "Z^2" in f.formula]
        return self.batch_promote(z2_findings)

    def summary(self) -> str:
        """Generate bridge activity summary."""
        return (
            f"OlympusBridge Summary:\n"
            f"  Received from OlympusFlow: {len(self.received_from_olympus)}\n"
            f"  Promoted to OlympusFlow: {len(self.promoted_to_olympus)}\n"
        )


def integrate_with_olympusflow(briareus_result: BriareusResult,
                                bridge: OlympusBridge = None) -> Dict:
    """
    Full integration: take BriareusFlow results and prepare for OlympusFlow.

    Args:
        briareus_result: Result from BriareusController.run()
        bridge: Optional OlympusBridge (creates one if not provided)

    Returns:
        Dict with:
        - olympus_inputs: Ready for OlympusFlow
        - z2_candidates: Z² patterns specifically
        - summary: Statistics
    """
    bridge = bridge or OlympusBridge()

    # Get all findings
    findings = briareus_result.best_findings

    # Promote promising findings
    all_promoted = bridge.batch_promote(findings)

    # Get Z² candidates specifically
    z2_candidates = bridge.get_z2_candidates_for_olympus(findings)

    return {
        "olympus_inputs": all_promoted,
        "z2_candidates": z2_candidates,
        "summary": {
            "total_findings": briareus_result.findings_total,
            "promoted": len(all_promoted),
            "z2_candidates": len(z2_candidates),
            "avg_error": briareus_result.avg_error_percent
        },
        "bridge_summary": bridge.summary()
    }


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("OLYMPUS BRIDGE TEST")
    print("=" * 70)
    print()

    # Simulate OlympusFlow results
    olympus_results = [
        {
            "constant_name": "sin²θ_W",
            "experimental_value": 0.23122,
            "uncertainty": 0.00003,
            "category": "phenomenological",
            "hrm_score": 0.65,
            "domain": "particle_physics",
            "source": "PDG 2024"
        },
        {
            "constant_name": "Ω_Λ",
            "experimental_value": 0.685,
            "uncertainty": 0.007,
            "category": "matches",
            "hrm_score": 0.75,
            "domain": "cosmology",
            "source": "Planck 2018"
        }
    ]

    # Create bridge
    bridge = OlympusBridge(verbose=True)

    # Receive from OlympusFlow
    targets = bridge.receive_from_olympusflow(olympus_results)
    print(f"\nTargets for BriareusFlow:")
    for t in targets:
        print(f"  {t.name}: {t.value} (priority: {t.priority.name})")

    # Run BriareusFlow
    from .briareus_controller import BriareusController, SearchConfig

    config = SearchConfig(num_threads=2, verbose=False)
    controller = BriareusController(config)
    controller.add_targets(targets)

    print(f"\nRunning BriareusFlow...")
    result = controller.run(timeout=30)
    print(f"Found {result.findings_total} findings")

    # Integrate back to OlympusFlow
    integration = integrate_with_olympusflow(result, bridge)
    print(f"\nIntegration Summary:")
    print(f"  Promoted to OlympusFlow: {integration['summary']['promoted']}")
    print(f"  Z² candidates: {integration['summary']['z2_candidates']}")

    print()
    print("=" * 70)
    print("OLYMPUS BRIDGE TEST COMPLETE")
    print("=" * 70)
