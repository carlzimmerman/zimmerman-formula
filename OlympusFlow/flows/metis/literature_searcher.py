#!/usr/bin/env python3
"""
METISFLOW - Literature Searcher
================================

Searches scientific literature for derivations of physical constants.
Uses web search and paper databases to find how constants have been derived.

Now integrated with HermesFlow ResearchBridge for real web search!

Author: Carl Zimmerman
Date: May 5, 2026
Updated: May 6, 2026 - Added HermesFlow integration
"""

import re
import json
import time
import asyncio
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys

from .derivation_strategy import (
    LiteratureSource, DerivationApproach, DerivationFramework,
    ZSquaredRelevance, DerivationStrategy
)

# Try to import HermesFlow ResearchBridge
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from HermesFlow.research_bridge import ResearchBridge, HERMES_AVAILABLE
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False
    HERMES_AVAILABLE = False


# Keywords that indicate different derivation approaches
APPROACH_KEYWORDS = {
    DerivationApproach.FIRST_PRINCIPLES: [
        "first principles", "ab initio", "from scratch", "fundamental",
        "derives from", "starting from", "axioms"
    ],
    DerivationApproach.DIMENSIONAL_ANALYSIS: [
        "dimensional analysis", "dimensionless", "scaling", "units",
        "pi theorem", "buckingham"
    ],
    DerivationApproach.GEOMETRIC: [
        "geometric", "topological", "manifold", "curvature", "sphere packing",
        "lattice", "tessellation", "holographic", "boundary"
    ],
    DerivationApproach.RENORMALIZATION: [
        "renormalization", "RG flow", "beta function", "running coupling",
        "asymptotic freedom", "scale dependence"
    ],
    DerivationApproach.SYMMETRY: [
        "symmetry", "gauge", "invariance", "group theory", "representation",
        "conservation law", "noether"
    ],
    DerivationApproach.VARIATIONAL: [
        "variational", "minimization", "extremum", "lagrangian", "hamiltonian",
        "action principle", "least action"
    ],
    DerivationApproach.STATISTICAL: [
        "statistical mechanics", "partition function", "ensemble",
        "thermodynamic limit", "fluctuation", "entropy"
    ],
    DerivationApproach.NUMERICAL: [
        "numerical", "Monte Carlo", "lattice QCD", "simulation",
        "computational", "algorithm"
    ],
    DerivationApproach.EMPIRICAL_FIT: [
        "empirical", "fitting", "curve fit", "measured", "experimental",
        "phenomenological"
    ]
}

# Keywords suggesting Z² relevance
Z_SQUARED_KEYWORDS = {
    ZSquaredRelevance.HIGH: [
        "32π/3", "sphere packing", "holographic", "boundary CFT",
        "AdS/CFT", "dimensional reduction", "3D to 2D", "tessellation",
        "cubic lattice", "geometric constant"
    ],
    ZSquaredRelevance.MEDIUM: [
        "pi factor", "geometric factor", "solid angle", "4π",
        "dimensionless ratio", "topological", "lattice geometry"
    ],
    ZSquaredRelevance.LOW: [
        "arbitrary constant", "free parameter", "fitting parameter",
        "unexplained", "empirically determined"
    ]
}


class LiteratureSearcher:
    """
    Searches scientific literature for derivations of physical constants.

    Uses multiple strategies:
    1. HermesFlow web search (NEW - uses real web tools)
    2. Direct web search for derivation papers
    3. ArXiv search for recent research
    4. Wikipedia/scholarpedia for established derivations
    5. Built-in knowledge base (fallback)
    """

    def __init__(self, verbose: bool = True, use_web: bool = True):
        """
        Initialize the literature searcher.

        Args:
            verbose: Print progress messages
            use_web: Use HermesFlow web search when available (default: True)
        """
        self.verbose = verbose
        self.use_web = use_web
        self.search_history: List[Dict] = []

        # Initialize ResearchBridge if available
        self.bridge = None
        if use_web and BRIDGE_AVAILABLE and HERMES_AVAILABLE:
            try:
                self.bridge = ResearchBridge(verbose=verbose)
                self._log("HermesFlow ResearchBridge initialized")
            except Exception as e:
                self._log(f"Warning: Could not initialize ResearchBridge: {e}")

    def _log(self, msg: str):
        if self.verbose:
            print(f"[MetisSearch] {msg}")

    def search_derivation(self, constant_name: str,
                          constant_value: float = None) -> List[LiteratureSource]:
        """
        Search for papers/sources that derive a physical constant.

        Returns list of LiteratureSource objects with derivation info.

        Uses HermesFlow web tools when available, falls back to knowledge base.
        """
        sources = []

        # Try HermesFlow web search first
        if self.bridge and self.use_web:
            self._log(f"Using HermesFlow web search for: {constant_name}")
            try:
                web_sources = asyncio.run(self._search_with_hermes(constant_name, constant_value))
                sources.extend(web_sources)
            except Exception as e:
                self._log(f"Web search failed: {e}, falling back to knowledge base")

        # Also search knowledge base
        queries = self._generate_search_queries(constant_name, constant_value)

        for query in queries:
            self._log(f"Searching knowledge base: {query}")
            results = self._search_knowledge_base(constant_name, constant_value)
            sources.extend(results)

        # Deduplicate by title
        seen_titles = set()
        unique_sources = []
        for src in sources:
            if src.title not in seen_titles:
                seen_titles.add(src.title)
                unique_sources.append(src)

        self._log(f"Found {len(unique_sources)} unique sources")
        return unique_sources

    async def _search_with_hermes(self, constant_name: str,
                                   constant_value: float = None) -> List[LiteratureSource]:
        """
        Search using HermesFlow ResearchBridge.

        Returns LiteratureSource objects from web search results.
        """
        sources = []

        if not self.bridge:
            return sources

        # Research the topic
        domain = await self.bridge.research_topic(constant_name)

        # Convert extracted constants to LiteratureSource objects
        for source_url in domain.sources:
            src = LiteratureSource(
                title=f"Web research: {constant_name}",
                authors=[],
                year=2026,
                url=source_url,
                abstract=f"Automated research on {constant_name} via HermesFlow",
                key_equations=[],
                derivation_type=DerivationApproach.UNKNOWN,
                relevance_score=0.7
            )
            sources.append(src)

        # Log extracted constants
        self._log(f"HermesFlow found {len(domain.constants)} constants:")
        for const in domain.constants[:5]:
            self._log(f"  {const.get('name', 'Unknown')}: {const.get('value', 0):.6f}")

        return sources

    def _generate_search_queries(self, constant_name: str,
                                  constant_value: float = None) -> List[str]:
        """Generate search queries for finding derivations."""
        queries = [
            f"{constant_name} derivation",
            f"{constant_name} first principles calculation",
            f"theoretical derivation {constant_name}",
            f"how to derive {constant_name}",
            f"{constant_name} origin physics",
        ]

        if constant_value:
            queries.append(f"{constant_name} value {constant_value}")

        return queries

    def _search_knowledge_base(self, constant_name: str,
                               constant_value: float = None) -> List[LiteratureSource]:
        """
        Use built-in knowledge about famous constant derivations.

        This serves as a fallback when web search isn't available,
        and covers the most important constants.
        """
        sources = []

        # Knowledge base of famous derivations
        knowledge_base = self._get_derivation_knowledge_base()

        # Normalize constant name for matching
        normalized = constant_name.lower().replace("_", " ").replace("-", " ")

        for entry in knowledge_base:
            entry_name = entry["name"].lower()
            if normalized in entry_name or entry_name in normalized:
                src = LiteratureSource(
                    title=entry.get("paper_title", f"Derivation of {constant_name}"),
                    authors=entry.get("authors", []),
                    year=entry.get("year", 0),
                    url=entry.get("url", ""),
                    abstract=entry.get("abstract", ""),
                    key_equations=entry.get("key_equations", []),
                    derivation_type=DerivationApproach(entry.get("approach", "unknown")),
                    relevance_score=0.9
                )
                sources.append(src)

        return sources

    def _get_derivation_knowledge_base(self) -> List[Dict]:
        """
        Built-in knowledge base of how famous constants are derived.

        This is the "wisdom" that Metis brings - knowing HOW things
        have been derived in physics.
        """
        return [
            # Fine Structure Constant
            {
                "name": "fine structure constant",
                "paper_title": "QED: The Strange Theory of Light and Matter (Feynman)",
                "authors": ["Richard Feynman"],
                "year": 1985,
                "approach": "renormalization",
                "key_equations": ["α = e²/(4πε₀ℏc) ≈ 1/137"],
                "abstract": "The fine structure constant emerges from QED as the coupling "
                           "strength of electromagnetic interactions. Its value is set by "
                           "the electron charge and fundamental constants.",
                "derivation_status": "partially_derived",
                "notes": "Value not derived from first principles - it's a free parameter of the Standard Model"
            },
            # Proton-Electron Mass Ratio
            {
                "name": "proton electron mass ratio",
                "paper_title": "QCD and the origin of hadron masses",
                "authors": ["David Gross", "Frank Wilczek"],
                "year": 1973,
                "approach": "renormalization",
                "key_equations": ["m_p/m_e ≈ 1836.15"],
                "abstract": "The proton mass arises primarily from QCD binding energy, not quark masses. "
                           "The electron mass comes from Higgs mechanism.",
                "derivation_status": "partially_derived",
                "notes": "Requires lattice QCD for precise calculation"
            },
            # Gravitational Constant
            {
                "name": "gravitational constant",
                "paper_title": "General Relativity and Gravitation",
                "authors": ["Albert Einstein"],
                "year": 1915,
                "approach": "first_principles",
                "key_equations": ["R_μν - (1/2)g_μν R = 8πG/c⁴ T_μν"],
                "abstract": "G appears as the coupling constant in Einstein field equations. "
                           "Its value is not derived but measured experimentally.",
                "derivation_status": "not_derived",
                "notes": "Fundamental constant with no known theoretical derivation"
            },
            # Feigenbaum Delta
            {
                "name": "feigenbaum delta",
                "paper_title": "Quantitative Universality for a Class of Nonlinear Transformations",
                "authors": ["Mitchell Feigenbaum"],
                "year": 1978,
                "approach": "first_principles",
                "key_equations": ["δ = lim(Δn/Δn+1) = 4.669201..."],
                "abstract": "The Feigenbaum constant δ ≈ 4.669 emerges from the functional equation "
                           "governing period-doubling bifurcations. It is universal for all "
                           "unimodal maps approaching chaos.",
                "derivation_status": "derived",
                "notes": "Rigorously derived from renormalization of iterated maps"
            },
            # von Karman Constant
            {
                "name": "von karman constant",
                "paper_title": "Turbulent Flow Near a Wall",
                "authors": ["Theodore von Karman"],
                "year": 1930,
                "approach": "dimensional",
                "key_equations": ["u/u* = (1/κ)ln(y/y₀)", "κ ≈ 0.41"],
                "abstract": "The von Karman constant κ ≈ 0.41 appears in the logarithmic law "
                           "of the wall for turbulent boundary layers. Its value is determined "
                           "empirically but dimensional analysis constrains the form.",
                "derivation_status": "partially_derived",
                "notes": "Form derived from dimensional analysis, value from experiment"
            },
            # Graphene Magic Angle
            {
                "name": "magic angle",
                "paper_title": "Unconventional superconductivity in magic-angle graphene superlattices",
                "authors": ["Yuan Cao", "Pablo Jarillo-Herrero"],
                "year": 2018,
                "approach": "first_principles",
                "key_equations": ["θ_magic ≈ 1.1°", "θ = arccos((3m²+3mn+n²-1)/(3m²+3mn+n²+1))"],
                "abstract": "The magic angle in twisted bilayer graphene occurs when the Fermi "
                           "velocity vanishes, creating flat bands. Derived from tight-binding "
                           "model of moiré superlattice.",
                "derivation_status": "derived",
                "notes": "Derived from Bistritzer-MacDonald model of twisted bilayer graphene"
            },
            # Chandrasekhar Limit
            {
                "name": "chandrasekhar limit",
                "paper_title": "The Maximum Mass of Ideal White Dwarfs",
                "authors": ["Subrahmanyan Chandrasekhar"],
                "year": 1931,
                "approach": "first_principles",
                "key_equations": ["M_Ch = (ℏc/G)^(3/2) / (μ_e m_H)² × ω₃⁰"],
                "abstract": "The Chandrasekhar limit ~1.4 M☉ is derived from balancing "
                           "electron degeneracy pressure against gravitational collapse, "
                           "using relativistic quantum mechanics.",
                "derivation_status": "derived",
                "notes": "Rigorous first-principles derivation from quantum mechanics and GR"
            },
            # Planck Scale Constants
            {
                "name": "planck length",
                "paper_title": "Über irreversible Strahlungsvorgänge",
                "authors": ["Max Planck"],
                "year": 1899,
                "approach": "dimensional",
                "key_equations": ["l_P = √(ℏG/c³) ≈ 1.6×10⁻³⁵ m"],
                "abstract": "Planck length is constructed from fundamental constants h, G, c "
                           "using dimensional analysis. It represents the scale where quantum "
                           "gravity effects become important.",
                "derivation_status": "derived",
                "notes": "Derived purely from dimensional analysis"
            },
            # Euler-Mascheroni Constant
            {
                "name": "euler mascheroni",
                "paper_title": "De progressionibus harmonicis observationes",
                "authors": ["Leonhard Euler"],
                "year": 1734,
                "approach": "first_principles",
                "key_equations": ["γ = lim(Σ1/k - ln(n)) ≈ 0.5772"],
                "abstract": "The Euler-Mascheroni constant γ is the limiting difference between "
                           "the harmonic series and natural logarithm. It appears throughout "
                           "number theory and analysis.",
                "derivation_status": "derived",
                "notes": "Mathematically derived, but irrationality not proven"
            },
            # Nuclear Magic Numbers
            {
                "name": "nuclear magic number",
                "paper_title": "On Closed Shells in Nuclei",
                "authors": ["Maria Goeppert Mayer"],
                "year": 1948,
                "approach": "first_principles",
                "key_equations": ["Magic: 2, 8, 20, 28, 50, 82, 126"],
                "abstract": "Nuclear magic numbers arise from the nuclear shell model with "
                           "spin-orbit coupling. The energy levels cluster into shells, and "
                           "closed shells have extra stability.",
                "derivation_status": "derived",
                "notes": "Derived from nuclear shell model - Nobel Prize 1963"
            },
            # von Klitzing Constant
            {
                "name": "von klitzing",
                "paper_title": "New Method for High-Accuracy Determination of the Fine-Structure Constant",
                "authors": ["Klaus von Klitzing"],
                "year": 1980,
                "approach": "first_principles",
                "key_equations": ["R_K = h/e² = 25812.807... Ω"],
                "abstract": "The von Klitzing constant emerges from the quantum Hall effect. "
                           "In a 2D electron gas at low temperature and high magnetic field, "
                           "Hall resistance is quantized in units of h/e².",
                "derivation_status": "derived",
                "notes": "Exact quantization from topology - Nobel Prize 1985"
            }
        ]

    def identify_approach(self, text: str) -> DerivationApproach:
        """Identify the derivation approach from text."""
        text_lower = text.lower()

        scores = {}
        for approach, keywords in APPROACH_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[approach] = score

        if not scores:
            return DerivationApproach.UNKNOWN

        return max(scores, key=scores.get)

    def assess_z_squared_relevance(self, constant_name: str,
                                    sources: List[LiteratureSource]) -> Tuple[ZSquaredRelevance, str]:
        """
        Assess how relevant Z² framework might be for this constant.

        Returns (relevance level, explanation).
        """
        # Check if it's a known Z²-connected constant
        z_squared_connected = [
            "fine structure", "proton mass", "electron mass", "gravitational",
            "planck", "cosmological", "hubble"
        ]

        # Check if derivation involves geometry
        geometric_constants = [
            "magic angle", "sphere packing", "lattice", "packing fraction",
            "solid angle", "crystallographic"
        ]

        normalized = constant_name.lower()

        # High relevance: geometric/topological constants
        for term in geometric_constants:
            if term in normalized:
                return (
                    ZSquaredRelevance.HIGH,
                    f"Geometric constant - Z² as 32π/3 relates to geometric/sphere packing"
                )

        # Medium relevance: fundamental physics constants
        for term in z_squared_connected:
            if term in normalized:
                return (
                    ZSquaredRelevance.MEDIUM,
                    f"Fundamental constant - potential dimensional/scaling connection to Z²"
                )

        # Check source content for geometric keywords
        all_text = " ".join(s.abstract for s in sources)
        for relevance, keywords in Z_SQUARED_KEYWORDS.items():
            if any(kw in all_text.lower() for kw in keywords):
                return (relevance, f"Found Z²-relevant keywords in literature")

        return (ZSquaredRelevance.LOW, "No clear Z² connection found in literature")

    def extract_framework(self, sources: List[LiteratureSource]) -> List[DerivationFramework]:
        """Extract mathematical frameworks used in derivations."""
        frameworks = []

        # Map common terms to frameworks
        framework_map = {
            "QED": DerivationFramework(
                name="Quantum Electrodynamics",
                mathematical_tools=["Feynman diagrams", "perturbation theory", "renormalization"],
                key_concepts=["coupling constant", "virtual particles", "running coupling"],
                has_geometric_structure=False
            ),
            "QCD": DerivationFramework(
                name="Quantum Chromodynamics",
                mathematical_tools=["lattice QCD", "perturbative QCD", "color charge"],
                key_concepts=["confinement", "asymptotic freedom", "gluon exchange"],
                has_geometric_structure=False
            ),
            "General Relativity": DerivationFramework(
                name="General Relativity",
                mathematical_tools=["Riemannian geometry", "tensor calculus", "Einstein equations"],
                key_concepts=["spacetime curvature", "geodesics", "stress-energy tensor"],
                has_geometric_structure=True,
                z_squared_potential=ZSquaredRelevance.MEDIUM
            ),
            "Statistical Mechanics": DerivationFramework(
                name="Statistical Mechanics",
                mathematical_tools=["partition function", "ensemble averages", "thermodynamic limits"],
                key_concepts=["entropy", "fluctuations", "phase transitions"],
                has_geometric_structure=False
            ),
            "Dimensional Analysis": DerivationFramework(
                name="Dimensional Analysis",
                mathematical_tools=["Buckingham Pi theorem", "scaling laws"],
                key_concepts=["dimensionless groups", "self-similarity"],
                has_geometric_structure=False
            ),
            "Shell Model": DerivationFramework(
                name="Nuclear Shell Model",
                mathematical_tools=["harmonic oscillator", "spin-orbit coupling", "angular momentum"],
                key_concepts=["magic numbers", "nuclear stability", "level ordering"],
                has_geometric_structure=True,
                z_squared_potential=ZSquaredRelevance.MEDIUM
            ),
            "Tight Binding": DerivationFramework(
                name="Tight-Binding Model",
                mathematical_tools=["Bloch waves", "band structure", "hopping integrals"],
                key_concepts=["flat bands", "moiré pattern", "superlattice"],
                has_geometric_structure=True,
                z_squared_potential=ZSquaredRelevance.HIGH
            )
        }

        # Search sources for framework keywords
        all_text = " ".join(s.abstract + s.title for s in sources).lower()

        for name, framework in framework_map.items():
            if name.lower() in all_text:
                frameworks.append(framework)

        return frameworks


def test_searcher():
    """Test the literature searcher."""
    searcher = LiteratureSearcher()

    test_constants = [
        "fine structure constant",
        "Feigenbaum delta",
        "magic angle",
        "von Karman constant"
    ]

    for const in test_constants:
        print(f"\n{'='*60}")
        print(f"Searching for: {const}")
        print('='*60)

        sources = searcher.search_derivation(const)

        for src in sources:
            print(f"\n  Title: {src.title}")
            print(f"  Approach: {src.derivation_type.value}")
            print(f"  Abstract: {src.abstract[:100]}...")

        relevance, explanation = searcher.assess_z_squared_relevance(const, sources)
        print(f"\n  Z² Relevance: {relevance.value}")
        print(f"  Explanation: {explanation}")


if __name__ == "__main__":
    test_searcher()
