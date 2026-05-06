#!/usr/bin/env python3
"""
METISFLOW - Metis Engine (Wisdom Engine)
==========================================

The core engine that researches derivations and creates strategies.

Metis was the Titan goddess of wisdom, prudent counsel, and deep thought.
She was the first wife of Zeus and mother of Athena.

MetisEngine embodies "thinking before acting" - researching HOW constants
have been derived before attempting our own Z² derivation.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .derivation_strategy import (
    DerivationStrategy, DerivationApproach, DerivationFramework,
    ZSquaredRelevance, LiteratureSource, MetisResearchResult
)
from .literature_searcher import LiteratureSearcher


# Physical meanings of constants (for context)
CONSTANT_MEANINGS = {
    "fine_structure_constant": {
        "meaning": "Strength of electromagnetic interaction between charged particles",
        "units": "dimensionless",
        "related": ["electron charge", "Planck constant", "speed of light"]
    },
    "proton_electron_mass_ratio": {
        "meaning": "Ratio of proton mass to electron mass",
        "units": "dimensionless",
        "related": ["quark masses", "QCD binding energy", "Higgs coupling"]
    },
    "gravitational_constant": {
        "meaning": "Coupling strength of gravitational interaction",
        "units": "m³/(kg·s²)",
        "related": ["Planck mass", "Newton's law", "Einstein equations"]
    },
    "feigenbaum_delta": {
        "meaning": "Universal ratio governing approach to chaos in period-doubling",
        "units": "dimensionless",
        "related": ["bifurcation", "logistic map", "chaos theory"]
    },
    "von_karman_constant": {
        "meaning": "Coefficient in logarithmic velocity profile of turbulent boundary layers",
        "units": "dimensionless",
        "related": ["turbulence", "Reynolds number", "boundary layer"]
    },
    "magic_angle": {
        "meaning": "Twist angle at which bilayer graphene becomes superconducting",
        "units": "degrees",
        "related": ["moiré pattern", "flat bands", "superconductivity"]
    },
    "chandrasekhar_limit": {
        "meaning": "Maximum mass of a stable white dwarf star",
        "units": "solar masses",
        "related": ["electron degeneracy", "gravitational collapse", "neutron star"]
    },
    "von_klitzing_constant": {
        "meaning": "Quantum of resistance from quantum Hall effect",
        "units": "ohms",
        "related": ["Planck constant", "electron charge", "topological quantum number"]
    }
}


class MetisEngine:
    """
    The Wisdom Engine - researches derivations and creates strategies.

    Flow:
    1. Receive a target constant
    2. Search literature for existing derivations
    3. Identify mathematical frameworks used
    4. Assess Z² relevance
    5. Create a DerivationStrategy for OlympusFlow
    """

    def __init__(self, output_dir: str = "metis_outputs", verbose: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        self.searcher = LiteratureSearcher(verbose=verbose)

        # Cache of researched strategies
        self.strategy_cache: Dict[str, DerivationStrategy] = {}

    def _log(self, msg: str):
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[Metis {timestamp}] {msg}")

    def research(self, constant_name: str,
                 constant_value: float = None,
                 force: bool = False) -> MetisResearchResult:
        """
        Research a constant and create a derivation strategy.

        Args:
            constant_name: Name of the constant (e.g., "fine structure constant")
            constant_value: Target value (e.g., 0.007297)
            force: If True, research even if cached

        Returns:
            MetisResearchResult with strategy and research metadata
        """
        start_time = time.time()
        normalized_name = constant_name.lower().replace(" ", "_")

        # Check cache
        if not force and normalized_name in self.strategy_cache:
            self._log(f"Using cached strategy for {constant_name}")
            return MetisResearchResult(
                query=constant_name,
                strategy=self.strategy_cache[normalized_name],
                sources_searched=0,
                papers_found=0,
                derivations_analyzed=0,
                research_time_seconds=0.0,
                derivation_exists=True,
                z_squared_viable=self.strategy_cache[normalized_name].z_squared_relevance != ZSquaredRelevance.NONE,
                recommendation="Using cached research"
            )

        self._log(f"Researching: {constant_name}")

        # Step 1: Search literature
        sources = self.searcher.search_derivation(constant_name, constant_value)
        papers_found = len(sources)
        self._log(f"Found {papers_found} relevant sources")

        # Step 2: Extract frameworks
        frameworks = self.searcher.extract_framework(sources)
        self._log(f"Identified {len(frameworks)} mathematical frameworks")

        # Step 3: Assess Z² relevance
        z_relevance, z_explanation = self.searcher.assess_z_squared_relevance(
            constant_name, sources
        )
        self._log(f"Z² relevance: {z_relevance.value}")

        # Step 4: Determine recommended approach
        recommended_approach = self._determine_approach(sources, frameworks, z_relevance)
        self._log(f"Recommended approach: {recommended_approach.value}")

        # Step 5: Get physical meaning
        meaning_info = CONSTANT_MEANINGS.get(normalized_name, {})

        # Step 6: Build strategy
        strategy = DerivationStrategy(
            target_constant=constant_name,
            target_value=constant_value or 0.0,
            existing_derivations=sources,
            frameworks_used=frameworks,
            recommended_approach=recommended_approach,
            z_squared_relevance=z_relevance,
            z_squared_connection=z_explanation,
            physical_meaning=meaning_info.get("meaning", ""),
            dimensional_units=meaning_info.get("units", ""),
            related_constants=meaning_info.get("related", []),
            key_equations=[eq for s in sources for eq in s.key_equations],
            mathematical_path=self._suggest_mathematical_path(
                constant_name, recommended_approach, z_relevance
            ),
            required_assumptions=self._identify_assumptions(sources),
            confidence_score=self._calculate_confidence(sources, z_relevance)
        )

        # Cache strategy
        self.strategy_cache[normalized_name] = strategy

        # Save to disk
        self._save_strategy(strategy)

        elapsed = time.time() - start_time

        # Determine if derivation exists and Z² is viable
        derivation_exists = any(
            s.derivation_type != DerivationApproach.UNKNOWN
            and s.derivation_type != DerivationApproach.EMPIRICAL_FIT
            for s in sources
        )

        z_squared_viable = z_relevance in [ZSquaredRelevance.HIGH, ZSquaredRelevance.MEDIUM]

        # Generate recommendation
        recommendation = self._generate_recommendation(
            constant_name, derivation_exists, z_squared_viable, recommended_approach
        )

        return MetisResearchResult(
            query=constant_name,
            strategy=strategy,
            sources_searched=len(sources),
            papers_found=papers_found,
            derivations_analyzed=len([s for s in sources if s.derivation_type != DerivationApproach.UNKNOWN]),
            research_time_seconds=elapsed,
            derivation_exists=derivation_exists,
            z_squared_viable=z_squared_viable,
            recommendation=recommendation
        )

    def _determine_approach(self, sources: List[LiteratureSource],
                            frameworks: List[DerivationFramework],
                            z_relevance: ZSquaredRelevance) -> DerivationApproach:
        """Determine the best derivation approach."""
        # Count approaches used in literature
        approach_counts = {}
        for src in sources:
            if src.derivation_type != DerivationApproach.UNKNOWN:
                approach_counts[src.derivation_type] = approach_counts.get(src.derivation_type, 0) + 1

        if not approach_counts:
            # No known approaches - try geometric if Z² relevant
            if z_relevance == ZSquaredRelevance.HIGH:
                return DerivationApproach.GEOMETRIC
            return DerivationApproach.DIMENSIONAL_ANALYSIS

        # Return most common approach
        return max(approach_counts, key=approach_counts.get)

    def _suggest_mathematical_path(self, constant_name: str,
                                   approach: DerivationApproach,
                                   z_relevance: ZSquaredRelevance) -> str:
        """Suggest a mathematical path for derivation."""
        paths = {
            DerivationApproach.FIRST_PRINCIPLES: (
                "Start from fundamental laws (QFT/GR). Identify relevant Lagrangian. "
                "Use perturbation theory or exact solutions. Extract dimensionless ratio."
            ),
            DerivationApproach.DIMENSIONAL_ANALYSIS: (
                "Identify relevant physical quantities. Form dimensionless groups. "
                "Use Buckingham Pi theorem. Constrain form of constant."
            ),
            DerivationApproach.GEOMETRIC: (
                "Identify geometric structure (lattice, manifold, boundary). "
                "Compute relevant geometric invariants. Connect to Z² = 32π/3 "
                "through sphere packing or dimensional reduction arguments."
            ),
            DerivationApproach.RENORMALIZATION: (
                "Set up renormalization group flow. Compute beta function. "
                "Find fixed points. Extract universal constants from flow behavior."
            ),
            DerivationApproach.SYMMETRY: (
                "Identify symmetry group. Find invariants under group action. "
                "Use representation theory to constrain constant values."
            ),
            DerivationApproach.VARIATIONAL: (
                "Formulate variational principle. Find extremum. "
                "Extract constant from solution."
            ),
            DerivationApproach.STATISTICAL: (
                "Set up statistical ensemble. Compute partition function. "
                "Take thermodynamic limit. Extract constant from free energy."
            ),
            DerivationApproach.NUMERICAL: (
                "Set up numerical simulation (lattice, Monte Carlo). "
                "Extrapolate to continuum limit. Compare with experiment."
            )
        }

        base_path = paths.get(approach, "Approach unclear - further research needed.")

        if z_relevance == ZSquaredRelevance.HIGH:
            base_path += (
                "\n\nZ² CONNECTION: Strong geometric connection identified. "
                "Consider how Z² = 32π/3 (solid angle of sphere packing / lattice constant) "
                "enters the derivation through boundary/bulk correspondence or dimensional reduction."
            )
        elif z_relevance == ZSquaredRelevance.MEDIUM:
            base_path += (
                "\n\nZ² CONNECTION: Possible dimensional connection. "
                "Look for where factors of π or geometric ratios appear. "
                "Z² = 32π/3 may relate to integration over spherical geometry."
            )

        return base_path

    def _identify_assumptions(self, sources: List[LiteratureSource]) -> List[str]:
        """Identify assumptions required for derivation."""
        common_assumptions = [
            "Standard Model physics applies",
            "No new physics beyond SM at relevant scales",
            "Classical spacetime (no quantum gravity corrections)",
            "Equilibrium/steady-state conditions"
        ]

        # Check sources for specific assumptions
        if any("perturbative" in s.abstract.lower() for s in sources):
            common_assumptions.append("Perturbation theory valid (coupling << 1)")

        if any("lattice" in s.abstract.lower() for s in sources):
            common_assumptions.append("Continuum limit exists and is well-defined")

        if any("thermodynamic" in s.abstract.lower() for s in sources):
            common_assumptions.append("Thermodynamic limit well-defined")

        return common_assumptions[:5]  # Keep top 5

    def _calculate_confidence(self, sources: List[LiteratureSource],
                              z_relevance: ZSquaredRelevance) -> float:
        """Calculate confidence score for the strategy."""
        score = 0.3  # Base confidence

        # More sources = more confidence
        score += min(0.3, len(sources) * 0.1)

        # Known derivations = more confidence
        derived_count = sum(
            1 for s in sources
            if s.derivation_type not in [DerivationApproach.UNKNOWN, DerivationApproach.EMPIRICAL_FIT]
        )
        score += min(0.2, derived_count * 0.1)

        # Z² relevance affects confidence in Z² approach
        if z_relevance == ZSquaredRelevance.HIGH:
            score += 0.2
        elif z_relevance == ZSquaredRelevance.MEDIUM:
            score += 0.1

        return min(1.0, score)

    def _generate_recommendation(self, constant_name: str,
                                 derivation_exists: bool,
                                 z_squared_viable: bool,
                                 approach: DerivationApproach) -> str:
        """Generate recommendation for next steps."""
        if derivation_exists and z_squared_viable:
            return (
                f"PROCEED: Rigorous derivation exists for {constant_name}. "
                f"Z² approach is viable. Use {approach.value} framework "
                f"and look for geometric/dimensional connection to Z² = 32π/3."
            )
        elif derivation_exists and not z_squared_viable:
            return (
                f"CAUTION: Derivation exists but Z² connection is weak. "
                f"May be forcing pattern where none exists. Consider whether "
                f"Z² framework genuinely applies to {constant_name}."
            )
        elif not derivation_exists and z_squared_viable:
            return (
                f"OPPORTUNITY: No rigorous derivation exists. Z² approach "
                f"could provide novel insight. Focus on geometric arguments "
                f"using {approach.value}."
            )
        else:
            return (
                f"SKIP: No derivation exists and Z² connection is weak. "
                f"This constant may not be derivable from first principles "
                f"or may require physics beyond current understanding."
            )

    def _save_strategy(self, strategy: DerivationStrategy):
        """Save strategy to disk."""
        # Sanitize filename (remove problematic characters)
        import re
        normalized = strategy.target_constant.lower().replace(" ", "_")
        normalized = re.sub(r'[/\\:*?"<>|]', '_', normalized)  # Remove filesystem-unsafe chars
        filepath = self.output_dir / f"{normalized}_strategy.json"
        filepath.write_text(json.dumps(strategy.to_dict(), indent=2))
        self._log(f"Saved strategy to {filepath}")

    def get_z_squared_candidates(self) -> List[str]:
        """
        Return constants most likely to have Z² derivations.

        Based on geometric/topological nature.
        """
        high_priority = [
            "graphene magic angle",      # Geometric interference
            "sphere packing fraction",   # Direct geometry
            "von Klitzing constant",     # Topological quantum number
            "nuclear magic numbers",     # Shell geometry
            "chandrasekhar limit",       # Dimensional analysis
        ]

        medium_priority = [
            "fine structure constant",   # Possible deep connection
            "Planck length",             # Dimensional
            "proton electron mass ratio" # QCD geometry
        ]

        return high_priority + medium_priority

    def batch_research(self, constants: List[Tuple[str, float]]) -> Dict[str, MetisResearchResult]:
        """
        Research multiple constants and return results.

        Args:
            constants: List of (name, value) tuples

        Returns:
            Dict mapping constant names to research results
        """
        results = {}
        total = len(constants)

        for i, (name, value) in enumerate(constants):
            self._log(f"\n[{i+1}/{total}] Researching {name}")
            results[name] = self.research(name, value)

        return results


def demo():
    """Demonstrate MetisFlow capabilities."""
    engine = MetisEngine()

    # Test on a few constants
    test_constants = [
        ("fine structure constant", 1/137.036),
        ("Feigenbaum delta", 4.669),
        ("graphene magic angle", 1.1),
        ("von Karman constant", 0.41)
    ]

    print("\n" + "="*70)
    print("METISFLOW DEMONSTRATION - Wisdom Before Action")
    print("="*70)

    for name, value in test_constants:
        print(f"\n{'='*70}")
        print(f"RESEARCHING: {name} = {value}")
        print("="*70)

        result = engine.research(name, value)

        print(f"\n📚 Sources Found: {result.papers_found}")
        print(f"📊 Derivation Exists: {result.derivation_exists}")
        print(f"🔷 Z² Viable: {result.z_squared_viable}")
        print(f"⏱️  Research Time: {result.research_time_seconds:.2f}s")
        print(f"\n💡 RECOMMENDATION:")
        print(f"   {result.recommendation}")

        if result.strategy.frameworks_used:
            print(f"\n📐 Frameworks: {', '.join(f.name for f in result.strategy.frameworks_used)}")

        print(f"\n🎯 Confidence: {result.strategy.confidence_score:.2f}")


if __name__ == "__main__":
    demo()
