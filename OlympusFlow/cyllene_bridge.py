#!/usr/bin/env python3
"""
CYLLENE BRIDGE - Deepener Integration for Derivation Pipeline
==============================================================

Connects CylleneFlow's Deepener to the OlympusFlow derivation pipeline.

When a derivation succeeds:
1. CylleneBridge converts result to Deepener finding format
2. Deepener analyzes significance and generates research questions
3. Bridge converts questions into new DerivationTargets
4. Targets feed back into the autonomous derivation queue

This creates a self-expanding research loop:
    Derivation → "Why does this work?" → New research questions →
    New derivation targets → More derivations → ...

Author: Carl Zimmerman
Date: May 6, 2026
Version: 1.0.0
"""

import math
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime

# Add parent path
sys.path.insert(0, str(Path(__file__).parent.parent))

from CylleneFlow.deepener import Deepener, DeepeningDecision, ResearchQuestion


# Z² constant
Z_SQUARED = 32 * math.pi / 3


@dataclass
class DerivationInsight:
    """An insight generated from a derivation that needs investigation."""
    question: str
    rationale: str
    target_constant: Optional[str] = None
    target_value: Optional[float] = None
    domain: str = "general"
    priority: float = 0.5
    source_derivation: str = ""


class CylleneBridge:
    """
    Bridge between OlympusFlow derivation results and CylleneFlow deepener.

    Converts successful derivations into research questions and converts
    research questions into new derivation targets.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the bridge.

        Args:
            verbose: Print progress information
        """
        self.verbose = verbose
        self.deepener = Deepener(verbose=verbose, max_depth=2)

        # Knowledge base of related constants
        self.related_constants = self._load_related_constants()

        # Stats
        self.stats = {
            "derivations_analyzed": 0,
            "questions_generated": 0,
            "targets_generated": 0
        }

    def _log(self, msg: str):
        if self.verbose:
            print(f"[CylleneBridge] {msg}")

    def _load_related_constants(self) -> Dict[str, List[Dict]]:
        """Load knowledge base of related physics constants with actual values."""
        return {
            # If we derive sin²θ_W, consider these related
            "sin²θ_W": [
                {"name": "cos²θ_W", "value": 0.76878, "relation": "1 - sin²θ_W", "domain": "particle_physics"},
                {"name": "M_W/M_Z ratio", "value": 0.8815, "relation": "cos(θ_W)", "domain": "particle_physics"},
                {"name": "sin²θ_W(M_Z)", "value": 0.23122, "relation": "At Z pole", "domain": "particle_physics"},
            ],

            # If we derive α⁻¹
            "α⁻¹": [
                {"name": "α⁻¹(M_Z)", "value": 127.95, "relation": "RG running to Z pole", "domain": "particle_physics"},
                {"name": "α_s(M_Z)", "value": 0.1179, "relation": "Strong coupling at Z", "domain": "particle_physics"},
                {"name": "α_em", "value": 0.00729735, "relation": "1/137.036", "domain": "particle_physics"},
            ],

            # If we derive Ω_Λ
            "Ω_Λ": [
                {"name": "Ω_m", "value": 0.315, "relation": "1 - Ω_Λ (flat universe)", "domain": "cosmology"},
                {"name": "Ω_b h²", "value": 0.0224, "relation": "Baryon density", "domain": "cosmology"},
                {"name": "σ_8", "value": 0.811, "relation": "Matter fluctuation amplitude", "domain": "cosmology"},
            ],

            # Thermodynamics
            "γ": [
                {"name": "γ_diatomic", "value": 1.4, "relation": "7/5 for diatomic", "domain": "thermodynamics"},
                {"name": "C_v/R (monoatomic)", "value": 1.5, "relation": "3/2", "domain": "thermodynamics"},
            ],

            # cos²θ_W leads back to sin²θ_W
            "cos²θ_W": [
                {"name": "sin²θ_W", "value": 0.23122, "relation": "1 - cos²θ_W", "domain": "particle_physics"},
            ],

            # Default for unknown constants
            "_default": []
        }

    def derivation_to_finding(self, derivation: Dict) -> Dict:
        """
        Convert a derivation result to Deepener finding format.

        Args:
            derivation: Derivation result dict from AutonomousController

        Returns:
            Finding dict for Deepener
        """
        constant = derivation.get("constant_name", "unknown")
        value = derivation.get("computed_value", derivation.get("target_value", 0))
        formula = derivation.get("formula", "")
        error = derivation.get("percent_error", 1.0)
        domain = derivation.get("domain", "general")
        hrm = derivation.get("hrm_score", 0.5)
        level = derivation.get("derivation_level", "derived")

        # Determine target pattern
        if "Z²" in formula or "Z**2" in formula.upper():
            target = "Z²"
            target_value = Z_SQUARED
        elif "/" in formula and formula.count("/") == 1:
            # Simple fraction
            try:
                parts = formula.split("/")
                a, b = float(parts[0]), float(parts[1])
                target = f"{int(a)}/{int(b)}"
                target_value = a / b
            except:
                target = formula
                target_value = value
        else:
            target = formula
            target_value = value

        # Construct finding
        finding = {
            "domain": domain,
            "quantity": constant,
            "value": value,
            "target": target,
            "target_value": target_value,
            "error_percent": error,
            "error": error,  # Deepener uses both
            "n_samples": 1,  # Single derivation
            "formula": formula,
            "hrm_score": hrm,
            "derivation_level": level,

            # Extra metadata
            "source": "derivation",
            "timestamp": datetime.now().isoformat()
        }

        return finding

    def analyze_derivation(
        self,
        derivation: Dict,
        context: Dict = None
    ) -> DeepeningDecision:
        """
        Analyze a successful derivation to decide if further investigation is warranted.

        Args:
            derivation: Derivation result dict
            context: Additional context

        Returns:
            DeepeningDecision from Deepener
        """
        self.stats["derivations_analyzed"] += 1

        # Convert to finding format
        finding = self.derivation_to_finding(derivation)

        # Boost significance for first-principles derivations
        if derivation.get("derivation_level") == "first_principles":
            # Deepener will score this high anyway, but let's add HRM bonus
            hrm = derivation.get("hrm_score", 0.5)
            finding["hrm_boost"] = hrm  # Deepener can use this

        # Analyze with Deepener
        decision = self.deepener.analyze_finding(finding, context)

        self._log(f"Analyzed derivation: {derivation.get('constant_name')}")
        self._log(f"  Significance: {decision.significance_score:.2f}")
        self._log(f"  Should deepen: {decision.should_deepen}")
        self._log(f"  Questions: {len(decision.questions)}")

        self.stats["questions_generated"] += len(decision.questions)

        return decision

    def questions_to_targets(
        self,
        questions: List[ResearchQuestion],
        source_derivation: Dict
    ) -> List[Dict]:
        """
        Convert research questions into derivation targets.

        This is the key translation layer - turning "why" questions into
        concrete derivation tasks.

        Args:
            questions: Research questions from Deepener
            source_derivation: The derivation that generated these questions

        Returns:
            List of DerivationTarget-compatible dicts
        """
        targets = []
        source_constant = source_derivation.get("constant_name", "")
        source_domain = source_derivation.get("domain", "general")

        for q in questions:
            # Try to extract a concrete target from the question
            target = self._question_to_target(q, source_derivation)
            if target:
                targets.append(target)

        # Add related constants from knowledge base
        related = self._get_related_constants(source_constant, source_domain)
        targets.extend(related)

        # Deduplicate
        seen = set()
        unique_targets = []
        for t in targets:
            key = (t.get("constant_name", ""), t.get("target_value", 0))
            if key not in seen:
                seen.add(key)
                unique_targets.append(t)

        self.stats["targets_generated"] += len(unique_targets)

        return unique_targets

    def _question_to_target(
        self,
        question: ResearchQuestion,
        source_derivation: Dict
    ) -> Optional[Dict]:
        """
        Convert a single research question to a derivation target.

        Args:
            question: ResearchQuestion object
            source_derivation: Original derivation

        Returns:
            DerivationTarget-compatible dict, or None if can't convert
        """
        q_text = question.question.lower()
        domain = question.domain

        # Pattern matching for question types

        # "Why does X show Y pattern?" → Investigate X more deeply
        if "why does" in q_text and "pattern" in q_text:
            # Can't directly convert to target, but record for research
            return None

        # "Does pattern hold for..." → Validation target
        if "does" in q_text and "pattern hold" in q_text:
            # Suggests re-running with different parameters
            return None

        # "What other quantities..." → Search for related targets
        if "what other" in q_text:
            # This is handled by related constants lookup
            return None

        # "Cross-domain" questions → Look for analogous constants
        if question.domain == "cross-domain" or "other domain" in q_text:
            # Map to equivalent constants in other domains
            source_formula = source_derivation.get("formula", "")

            # If source was a simple fraction, look for same fraction elsewhere
            if "/" in source_formula:
                return {
                    "constant_name": f"[scan for {source_formula} pattern]",
                    "target_value": source_derivation.get("target_value", 0),
                    "domain": "cross-domain",
                    "priority": 0.6,
                    "source": "cyllene_bridge",
                    "question": question.question
                }

        return None

    def _get_related_constants(
        self,
        constant_name: str,
        domain: str
    ) -> List[Dict]:
        """
        Get constants related to the given constant.

        Args:
            constant_name: Name of the source constant
            domain: Physics domain

        Returns:
            List of related constant targets
        """
        targets = []

        # Look up in knowledge base
        related = self.related_constants.get(constant_name, [])
        if not related:
            # Try partial match
            for key in self.related_constants:
                if key.lower() in constant_name.lower() or constant_name.lower() in key.lower():
                    related = self.related_constants[key]
                    break

        if not related:
            related = self.related_constants.get("_default", [])

        for r in related:
            # Skip placeholders
            if "[" in r["name"]:
                continue

            # Get actual value if available
            target_value = r.get("value", 0)

            targets.append({
                "constant_name": r["name"],
                "target_value": target_value,
                "domain": r.get("domain", domain),
                "priority": 0.7,
                "source": "cyllene_bridge_related",
                "relation_to_source": r["relation"]
            })

        return targets

    def generate_followup_targets(
        self,
        derivation: Dict,
        max_targets: int = 5
    ) -> List[Dict]:
        """
        Generate follow-up derivation targets from a successful derivation.

        This is the main entry point for integration with AutonomousController.

        Args:
            derivation: Successful derivation result
            max_targets: Maximum number of targets to generate

        Returns:
            List of DerivationTarget-compatible dicts
        """
        # Skip if not worth investigating
        hrm = derivation.get("hrm_score", 0.5)
        level = derivation.get("derivation_level", "")

        if hrm < 0.5 and level != "first_principles":
            self._log("Skipping low-quality derivation")
            return []

        # Analyze with Deepener
        decision = self.analyze_derivation(derivation)

        if not decision.should_deepen:
            self._log(f"No deepening needed: {decision.reasoning}")
            return []

        # Convert questions to targets
        targets = self.questions_to_targets(decision.questions, derivation)

        # Add priority based on significance
        for t in targets:
            t["priority"] = min(1.0, t.get("priority", 0.5) + decision.significance_score * 0.3)

        # Sort by priority and limit
        targets.sort(key=lambda x: x.get("priority", 0), reverse=True)
        targets = targets[:max_targets]

        self._log(f"Generated {len(targets)} follow-up targets")

        return targets

    def generate_exploration_targets(
        self,
        domain: str,
        base_formula: str,
        n_targets: int = 5
    ) -> List[Dict]:
        """
        Generate exploration targets for a domain based on a formula pattern.

        Used when we find a formula pattern that might generalize.

        Args:
            domain: Physics domain to explore
            base_formula: Formula pattern to test (e.g., "3/13")
            n_targets: Number of targets to generate

        Returns:
            List of exploration targets
        """
        targets = []

        # Domain-specific constant suggestions
        domain_constants = {
            "particle_physics": [
                ("g_A/g_V ratio", -1.2723, "Axial-vector coupling ratio"),
                ("Cabibbo angle sin²θ_C", 0.0495, "CKM matrix parameter"),
                ("V_us", 0.2243, "CKM element"),
                ("α_s(M_Z)", 0.1179, "Strong coupling at Z"),
            ],
            "cosmology": [
                ("σ_8", 0.811, "Matter fluctuation amplitude"),
                ("n_s", 0.965, "Scalar spectral index"),
                ("τ_reion", 0.054, "Reionization optical depth"),
                ("Ω_b h²", 0.0224, "Baryon density"),
            ],
            "thermodynamics": [
                ("Prandtl number (air)", 0.71, "Pr = ν/α"),
                ("Prandtl number (water)", 7.0, "Pr = ν/α"),
                ("Stefan-Boltzmann exponent", 4.0, "σT^4"),
            ],
            "mathematics": [
                ("Euler-Mascheroni γ", 0.5772, "Gamma constant"),
                ("Apéry's constant ζ(3)", 1.2021, "Zeta(3)"),
                ("Catalan's constant", 0.9159, "G"),
            ]
        }

        constants = domain_constants.get(domain, domain_constants.get("mathematics", []))

        for name, value, desc in constants[:n_targets]:
            targets.append({
                "constant_name": name,
                "target_value": value,
                "domain": domain,
                "priority": 0.6,
                "source": "cyllene_exploration",
                "description": desc,
                "exploration_basis": base_formula
            })

        return targets

    def get_stats(self) -> Dict[str, Any]:
        """Get bridge statistics."""
        return {
            **self.stats,
            "deepener_summary": self.deepener.get_summary()
        }

    def reset(self):
        """Reset bridge state."""
        self.stats = {
            "derivations_analyzed": 0,
            "questions_generated": 0,
            "targets_generated": 0
        }
        self.deepener.reset_state()


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CYLLENE BRIDGE TEST")
    print("=" * 70)
    print()

    bridge = CylleneBridge(verbose=True)

    # Test 1: Analyze a successful first-principles derivation
    print("Test 1: Analyze First-Principles Derivation")
    print("-" * 40)

    derivation = {
        "constant_name": "sin²θ_W",
        "target_value": 0.23122,
        "computed_value": 0.230769,
        "formula": "3/13",
        "percent_error": 0.195,
        "derivation_level": "first_principles",
        "domain": "particle_physics",
        "hrm_score": 0.85,
        "physical_mechanism": "Electroweak gauge coupling ratio"
    }

    decision = bridge.analyze_derivation(derivation)
    print(f"\nDecision: {'Deepen' if decision.should_deepen else 'Skip'}")
    print(f"Significance: {decision.significance_score:.2f}")
    print()

    # Test 2: Generate follow-up targets
    print("Test 2: Generate Follow-up Targets")
    print("-" * 40)

    targets = bridge.generate_followup_targets(derivation)
    print(f"Generated {len(targets)} targets:")
    for t in targets:
        print(f"  - {t['constant_name']}")
        print(f"    Domain: {t['domain']}")
        print(f"    Priority: {t['priority']:.2f}")
    print()

    # Test 3: Exploration targets
    print("Test 3: Exploration Targets")
    print("-" * 40)

    exploration = bridge.generate_exploration_targets("particle_physics", "3/13", 3)
    print(f"Generated {len(exploration)} exploration targets:")
    for t in exploration:
        print(f"  - {t['constant_name']}: {t['target_value']}")
    print()

    # Test 4: Convert another derivation
    print("Test 4: Dark Energy Derivation")
    print("-" * 40)

    derivation2 = {
        "constant_name": "Ω_Λ",
        "target_value": 0.685,
        "computed_value": 0.684211,
        "formula": "13/19",
        "percent_error": 0.115,
        "derivation_level": "first_principles",
        "domain": "cosmology",
        "hrm_score": 0.80
    }

    targets2 = bridge.generate_followup_targets(derivation2)
    print(f"Generated {len(targets2)} targets for Ω_Λ:")
    for t in targets2[:3]:
        print(f"  - {t['constant_name']}")
    print()

    # Test 5: Stats
    print("Test 5: Bridge Statistics")
    print("-" * 40)
    stats = bridge.get_stats()
    print(f"Derivations analyzed: {stats['derivations_analyzed']}")
    print(f"Questions generated: {stats['questions_generated']}")
    print(f"Targets generated: {stats['targets_generated']}")
    print()

    print("=" * 70)
    print("CYLLENE BRIDGE TEST COMPLETE")
    print("=" * 70)
