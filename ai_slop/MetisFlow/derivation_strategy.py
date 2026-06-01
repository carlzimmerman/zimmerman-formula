#!/usr/bin/env python3
"""
METISFLOW - Derivation Strategy Contracts
==========================================

Data structures for representing derivation strategies.

Metis was the Titan goddess of wisdom, prudent counsel, and deep thought.
She represents the strategic thinking that precedes action.

Author: Carl Zimmerman
Date: May 5, 2026
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class DerivationApproach(Enum):
    """Types of derivation approaches found in literature."""
    FIRST_PRINCIPLES = "first_principles"       # Derive from fundamental laws
    DIMENSIONAL_ANALYSIS = "dimensional"        # Use dimensional arguments
    GEOMETRIC = "geometric"                     # Geometric/topological derivation
    RENORMALIZATION = "renormalization"         # RG flow derivation
    SYMMETRY = "symmetry"                       # Symmetry-based derivation
    VARIATIONAL = "variational"                 # Minimization/extremization
    STATISTICAL = "statistical"                 # Statistical mechanics approach
    EMPIRICAL_FIT = "empirical"                 # Curve fitting (low value)
    NUMERICAL = "numerical"                     # Numerical computation
    UNKNOWN = "unknown"                         # No clear approach found


class ZSquaredRelevance(Enum):
    """How relevant Z² might be to this derivation."""
    HIGH = "high"           # Clear geometric/topological connection
    MEDIUM = "medium"       # Possible dimensional/scaling connection
    LOW = "low"             # Weak or speculative connection
    NONE = "none"           # No clear Z² relevance
    UNKNOWN = "unknown"     # Not yet assessed


@dataclass
class LiteratureSource:
    """A source from scientific literature."""
    title: str
    authors: List[str] = field(default_factory=list)
    year: int = 0
    journal: str = ""
    url: str = ""
    arxiv_id: str = ""
    doi: str = ""
    abstract: str = ""
    key_equations: List[str] = field(default_factory=list)
    derivation_type: DerivationApproach = DerivationApproach.UNKNOWN
    relevance_score: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "journal": self.journal,
            "url": self.url,
            "arxiv_id": self.arxiv_id,
            "doi": self.doi,
            "abstract": self.abstract,
            "key_equations": self.key_equations,
            "derivation_type": self.derivation_type.value,
            "relevance_score": self.relevance_score
        }


@dataclass
class DerivationFramework:
    """Mathematical framework used in a derivation."""
    name: str                                   # e.g., "QED", "CFT", "Lattice QCD"
    mathematical_tools: List[str] = field(default_factory=list)  # e.g., ["Feynman diagrams", "RG flow"]
    key_concepts: List[str] = field(default_factory=list)        # e.g., ["running coupling", "beta function"]
    dimensionality: int = 4                     # Spacetime dimensions
    has_geometric_structure: bool = False       # Does it involve geometry?
    z_squared_potential: ZSquaredRelevance = ZSquaredRelevance.UNKNOWN

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "mathematical_tools": self.mathematical_tools,
            "key_concepts": self.key_concepts,
            "dimensionality": self.dimensionality,
            "has_geometric_structure": self.has_geometric_structure,
            "z_squared_potential": self.z_squared_potential.value
        }


@dataclass
class DerivationStrategy:
    """
    A strategy for deriving a physical constant.

    This is the output of MetisFlow research phase - it tells OlympusFlow
    HOW to approach the derivation rather than just pattern-matching.
    """
    target_constant: str
    target_value: float

    # Research findings
    existing_derivations: List[LiteratureSource] = field(default_factory=list)
    frameworks_used: List[DerivationFramework] = field(default_factory=list)

    # Strategy
    recommended_approach: DerivationApproach = DerivationApproach.UNKNOWN
    z_squared_relevance: ZSquaredRelevance = ZSquaredRelevance.UNKNOWN
    z_squared_connection: str = ""              # Explanation of Z² relevance

    # Physical context
    physical_meaning: str = ""                  # What does this constant represent?
    dimensional_units: str = ""                 # Units of the constant
    related_constants: List[str] = field(default_factory=list)

    # Derivation hints
    key_equations: List[str] = field(default_factory=list)
    mathematical_path: str = ""                 # Suggested derivation path
    required_assumptions: List[str] = field(default_factory=list)

    # Metadata
    research_timestamp: str = ""
    confidence_score: float = 0.0               # How confident are we in this strategy?
    notes: str = ""

    def __post_init__(self):
        if not self.research_timestamp:
            self.research_timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "target_constant": self.target_constant,
            "target_value": self.target_value,
            "existing_derivations": [s.to_dict() for s in self.existing_derivations],
            "frameworks_used": [f.to_dict() for f in self.frameworks_used],
            "recommended_approach": self.recommended_approach.value,
            "z_squared_relevance": self.z_squared_relevance.value,
            "z_squared_connection": self.z_squared_connection,
            "physical_meaning": self.physical_meaning,
            "dimensional_units": self.dimensional_units,
            "related_constants": self.related_constants,
            "key_equations": self.key_equations,
            "mathematical_path": self.mathematical_path,
            "required_assumptions": self.required_assumptions,
            "research_timestamp": self.research_timestamp,
            "confidence_score": self.confidence_score,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'DerivationStrategy':
        """Reconstruct from dictionary."""
        strategy = cls(
            target_constant=data.get("target_constant", ""),
            target_value=data.get("target_value", 0.0)
        )

        # Reconstruct nested objects
        for src_data in data.get("existing_derivations", []):
            src = LiteratureSource(
                title=src_data.get("title", ""),
                authors=src_data.get("authors", []),
                year=src_data.get("year", 0),
                url=src_data.get("url", "")
            )
            src.derivation_type = DerivationApproach(src_data.get("derivation_type", "unknown"))
            strategy.existing_derivations.append(src)

        for fw_data in data.get("frameworks_used", []):
            fw = DerivationFramework(
                name=fw_data.get("name", ""),
                mathematical_tools=fw_data.get("mathematical_tools", []),
                key_concepts=fw_data.get("key_concepts", [])
            )
            fw.z_squared_potential = ZSquaredRelevance(fw_data.get("z_squared_potential", "unknown"))
            strategy.frameworks_used.append(fw)

        strategy.recommended_approach = DerivationApproach(data.get("recommended_approach", "unknown"))
        strategy.z_squared_relevance = ZSquaredRelevance(data.get("z_squared_relevance", "unknown"))
        strategy.z_squared_connection = data.get("z_squared_connection", "")
        strategy.physical_meaning = data.get("physical_meaning", "")
        strategy.dimensional_units = data.get("dimensional_units", "")
        strategy.related_constants = data.get("related_constants", [])
        strategy.key_equations = data.get("key_equations", [])
        strategy.mathematical_path = data.get("mathematical_path", "")
        strategy.required_assumptions = data.get("required_assumptions", [])
        strategy.research_timestamp = data.get("research_timestamp", "")
        strategy.confidence_score = data.get("confidence_score", 0.0)
        strategy.notes = data.get("notes", "")

        return strategy


@dataclass
class MetisResearchResult:
    """Complete result from MetisFlow research phase."""
    query: str
    strategy: DerivationStrategy
    sources_searched: int = 0
    papers_found: int = 0
    derivations_analyzed: int = 0
    research_time_seconds: float = 0.0

    # Assessment
    derivation_exists: bool = False             # Does a rigorous derivation exist?
    z_squared_viable: bool = False              # Is Z² approach viable?
    recommendation: str = ""                    # What should we do next?

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "strategy": self.strategy.to_dict(),
            "sources_searched": self.sources_searched,
            "papers_found": self.papers_found,
            "derivations_analyzed": self.derivations_analyzed,
            "research_time_seconds": self.research_time_seconds,
            "derivation_exists": self.derivation_exists,
            "z_squared_viable": self.z_squared_viable,
            "recommendation": self.recommendation
        }
