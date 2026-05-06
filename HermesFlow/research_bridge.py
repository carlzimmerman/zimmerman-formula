#!/usr/bin/env python3
"""
HERMESFLOW - Research Bridge
=============================

Connects HermesFlow web research tools to BriareusFlow pattern discovery.

This bridges the gap between:
- HermesFlow: Web search, content extraction, research
- BriareusFlow: Pattern search, Z² discovery

The ResearchBridge handles:
1. Web search for scientific data on a topic
2. Extraction of numerical constants from text
3. Building SearchTarget objects for BriareusFlow
4. Saving domain definitions as JSON

Architecture:
┌─────────────────────────────────────────────────────────────────────┐
│                    RESEARCH BRIDGE                                   │
│                                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │   TOPIC      │────▶│  HERMESFLOW  │────▶│   CONSTANT   │        │
│  │   QUERY      │     │  WEB TOOLS   │     │  EXTRACTOR   │        │
│  └──────────────┘     └──────────────┘     └──────────────┘        │
│                              │                    │                  │
│                              ▼                    ▼                  │
│                       ┌──────────────┐     ┌──────────────┐        │
│                       │   SEARCH     │     │   DOMAIN     │        │
│                       │   TARGETS    │────▶│   REGISTRY   │        │
│                       └──────────────┘     └──────────────┘        │
│                              │                                       │
│                              ▼                                       │
│                       ┌──────────────┐                              │
│                       │ BRIAREUSFLOW │                              │
│                       │   PIPELINE   │                              │
│                       └──────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import re
import json
import asyncio
import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import Firecrawl search (lightweight standalone module)
try:
    from HermesFlow.firecrawl_search import (
        FirecrawlSearcher,
        is_firecrawl_available,
        extract_constants_from_content
    )
    FIRECRAWL_AVAILABLE = is_firecrawl_available()
    if FIRECRAWL_AVAILABLE:
        print("[ResearchBridge] Firecrawl web search available")
    else:
        print("[ResearchBridge] Warning: Firecrawl API key not found")
except ImportError:
    FIRECRAWL_AVAILABLE = False
    print("[ResearchBridge] Warning: Firecrawl search module not available")

# Legacy: Try to import full HermesFlow web tools (complex dependencies)
HERMES_AVAILABLE = False  # Disabled - use lightweight Firecrawl instead

# Import BriareusFlow types
try:
    from BriareusFlow import SearchTarget, SearchPriority, SearchConfig, BriareusController
    BRIAREUS_AVAILABLE = True
except ImportError:
    BRIAREUS_AVAILABLE = False
    # Define fallback types
    from enum import Enum
    class SearchPriority(Enum):
        CRITICAL = 0
        HIGH = 1
        NORMAL = 2
        LOW = 3

    @dataclass
    class SearchTarget:
        target_id: str
        name: str
        value: float
        uncertainty: float
        source: str
        domain: str
        priority: SearchPriority = SearchPriority.NORMAL
        metadata: Dict = field(default_factory=dict)


# =============================================================================
# CONSTANT EXTRACTOR - NLP/Regex extraction of numerical constants
# =============================================================================

@dataclass
class ExtractedConstant:
    """A numerical constant extracted from scientific text."""
    name: str
    value: float
    uncertainty: float
    unit: str
    source_text: str
    source_url: str
    confidence: float  # 0-1, how confident we are in extraction


class ConstantExtractor:
    """
    Extracts numerical constants from scientific text using regex patterns.

    Handles formats like:
    - "wavelength of 420 nm"
    - "angle of 215 degrees"
    - "coefficient of 0.746 ± 0.003"
    - "ratio = 3/4"
    - "exponent β = 0.75"
    """

    # Regex patterns for extracting numerical values with units
    PATTERNS = [
        # Value with uncertainty: "0.746 ± 0.003" or "0.746 +/- 0.003"
        (r'(\d+\.?\d*)\s*[±\+\-\/]+\s*(\d+\.?\d*)\s*([a-zA-Z°%]+)?', 'uncertainty'),

        # Scientific notation: "1.6e-19" or "1.6×10^-19"
        (r'(\d+\.?\d*)\s*[×x]\s*10\^?\s*\-?(\d+)\s*([a-zA-Z°%]+)?', 'scientific'),

        # Simple value with unit: "420 nm", "215 degrees", "0.75"
        (r'(\d+\.?\d*)\s*([a-zA-Z°%]+)', 'unit'),

        # Fraction: "3/4", "25/Z²"
        (r'(\d+)\s*/\s*(\d+|Z²|π)', 'fraction'),

        # Percentage: "23.1%", "75 percent"
        (r'(\d+\.?\d*)\s*(%|percent)', 'percent'),

        # Temperature: "273.15 K", "-40°C"
        (r'(\-?\d+\.?\d*)\s*(°?[CFK]|kelvin|celsius)', 'temperature'),

        # Wavelength: "420 nm", "550 nanometers"
        (r'(\d+\.?\d*)\s*(nm|nanometer|μm|micrometer)', 'wavelength'),

        # Angle: "215 degrees", "1.1°"
        (r'(\d+\.?\d*)\s*(°|deg|degrees?|radians?)', 'angle'),

        # Coefficient/ratio: "β = 0.75", "coefficient 2.44"
        (r'(coefficient|ratio|exponent|constant|factor|index)\s*[=:]?\s*(\d+\.?\d*)', 'named'),

        # Greek letter equals: "α = 137.036"
        (r'([αβγδεζηθλμξπρστφχψω])\s*[=≈]\s*(\d+\.?\d*)', 'greek'),
    ]

    # Units to recognize
    UNITS = {
        'nm': ('nanometer', 1e-9),
        'μm': ('micrometer', 1e-6),
        'mm': ('millimeter', 1e-3),
        'm': ('meter', 1),
        'km': ('kilometer', 1e3),
        'AU': ('astronomical unit', 1.496e11),
        's': ('second', 1),
        'Hz': ('hertz', 1),
        'K': ('kelvin', 1),
        '°': ('degree', 1),
        'deg': ('degree', 1),
        'rad': ('radian', 1),
        '%': ('percent', 0.01),
        'eV': ('electronvolt', 1.602e-19),
        'J': ('joule', 1),
    }

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(f"[ConstantExtractor] {msg}")

    def extract_from_text(self, text: str, source_url: str = "") -> List[ExtractedConstant]:
        """
        Extract numerical constants from a block of text.

        Returns list of ExtractedConstant objects.
        """
        constants = []

        # Split into sentences for context
        sentences = re.split(r'[.!?]\s+', text)

        for sentence in sentences:
            # Skip very short sentences
            if len(sentence) < 10:
                continue

            # Try each pattern
            for pattern, pattern_type in self.PATTERNS:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)

                for match in matches:
                    const = self._process_match(match, pattern_type, sentence, source_url)
                    if const and const.value != 0:
                        constants.append(const)

        # Deduplicate by value (within tolerance)
        unique = self._deduplicate(constants)

        self._log(f"Extracted {len(unique)} constants from text")
        return unique

    def _process_match(self, match, pattern_type: str, context: str,
                       source_url: str) -> Optional[ExtractedConstant]:
        """Process a regex match into an ExtractedConstant."""
        try:
            groups = match.groups()

            if pattern_type == 'uncertainty':
                value = float(groups[0])
                uncertainty = float(groups[1])
                unit = groups[2] if len(groups) > 2 and groups[2] else ""
                name = self._infer_name(context, value)

            elif pattern_type == 'scientific':
                mantissa = float(groups[0])
                exponent = int(groups[1])
                value = mantissa * (10 ** exponent)
                uncertainty = value * 0.01  # Assume 1% uncertainty
                unit = groups[2] if len(groups) > 2 and groups[2] else ""
                name = self._infer_name(context, value)

            elif pattern_type == 'fraction':
                numerator = float(groups[0])
                denom = groups[1]
                if denom == 'Z²':
                    value = numerator / 33.510322  # Z² ≈ 32π/3
                elif denom == 'π':
                    value = numerator / math.pi
                else:
                    value = numerator / float(denom)
                uncertainty = value * 0.001
                unit = "ratio"
                name = f"{int(numerator)}/{denom}"

            elif pattern_type in ['unit', 'wavelength', 'angle', 'temperature', 'percent']:
                value = float(groups[0])
                unit = groups[1] if len(groups) > 1 and groups[1] else ""
                uncertainty = value * 0.01
                name = self._infer_name(context, value)

                # Convert percent to decimal
                if pattern_type == 'percent':
                    value = value / 100
                    uncertainty = uncertainty / 100

            elif pattern_type == 'named':
                name = groups[0]
                value = float(groups[1])
                uncertainty = value * 0.01
                unit = ""

            elif pattern_type == 'greek':
                name = groups[0]
                value = float(groups[1])
                uncertainty = value * 0.01
                unit = ""

            else:
                return None

            # Calculate confidence based on context
            confidence = self._assess_confidence(context, value)

            return ExtractedConstant(
                name=name,
                value=value,
                uncertainty=uncertainty,
                unit=unit,
                source_text=context[:200],
                source_url=source_url,
                confidence=confidence
            )

        except (ValueError, IndexError):
            return None

    def _infer_name(self, context: str, value: float) -> str:
        """Infer a name for the constant from context."""
        # Look for keywords near the value
        keywords = [
            'wavelength', 'frequency', 'angle', 'ratio', 'coefficient',
            'constant', 'exponent', 'index', 'factor', 'limit', 'threshold',
            'migration', 'navigation', 'heading', 'bearing', 'direction',
            'distance', 'speed', 'velocity', 'temperature', 'pressure',
            'mass', 'energy', 'force', 'luminosity', 'period', 'radius'
        ]

        context_lower = context.lower()
        for kw in keywords:
            if kw in context_lower:
                return f"{kw} ({value:.4g})"

        return f"constant ({value:.4g})"

    def _assess_confidence(self, context: str, value: float) -> float:
        """Assess confidence in extraction based on context."""
        confidence = 0.5  # Base confidence

        # Higher confidence if context mentions measurement/experiment
        if any(w in context.lower() for w in ['measured', 'observed', 'experiment', 'data']):
            confidence += 0.2

        # Higher confidence if uncertainty is mentioned
        if '±' in context or 'error' in context.lower():
            confidence += 0.1

        # Higher confidence if source is cited
        if any(w in context.lower() for w in ['et al', 'reference', 'published', 'study']):
            confidence += 0.1

        # Lower confidence for very round numbers (might be estimates)
        if value == int(value) and value > 10:
            confidence -= 0.1

        return min(max(confidence, 0.1), 1.0)

    def _deduplicate(self, constants: List[ExtractedConstant],
                     tolerance: float = 0.001) -> List[ExtractedConstant]:
        """Remove duplicate constants (same value within tolerance)."""
        unique = []
        seen_values = set()

        for const in constants:
            # Round to 4 significant figures for comparison
            rounded = round(const.value, 4 - int(math.floor(math.log10(abs(const.value) + 1e-10))))
            if rounded not in seen_values:
                seen_values.add(rounded)
                unique.append(const)

        return unique


# =============================================================================
# RESEARCH BRIDGE - Connects HermesFlow to BriareusFlow
# =============================================================================

@dataclass
class DomainDefinition:
    """A domain definition for BriareusFlow."""
    name: str
    description: str
    keywords: List[str]
    constants: List[Dict[str, Any]]
    sources: List[str]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_search_targets(self, priority: SearchPriority = SearchPriority.HIGH) -> List[SearchTarget]:
        """Convert to list of SearchTargets for BriareusFlow."""
        targets = []
        for const in self.constants:
            target = SearchTarget(
                target_id=const.get('name', 'unknown').replace(' ', '_').replace('/', '_'),
                name=const.get('name', 'Unknown'),
                value=const.get('value', 0),
                uncertainty=const.get('uncertainty', 0.01),
                source=const.get('source', 'HermesFlow research'),
                domain=self.name,
                priority=priority,
                metadata={'unit': const.get('unit', '')}
            )
            targets.append(target)
        return targets


class ResearchBridge:
    """
    Bridges HermesFlow web research to BriareusFlow pattern discovery.

    Usage:
        bridge = ResearchBridge()
        domain = await bridge.research_topic("monarch butterfly navigation")
        targets = domain.to_search_targets()
        # Pass targets to BriareusFlow
    """

    def __init__(self,
                 domains_dir: str = None,
                 verbose: bool = True):
        """
        Initialize the ResearchBridge.

        Args:
            domains_dir: Directory to save domain JSON files
            verbose: Print progress
        """
        self.verbose = verbose
        self.extractor = ConstantExtractor(verbose=verbose)

        # Set up domains directory
        if domains_dir:
            self.domains_dir = Path(domains_dir)
        else:
            self.domains_dir = Path(__file__).parent.parent / "BriareusFlow" / "domains"
        self.domains_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Firecrawl searcher if available
        self.firecrawl = None
        if FIRECRAWL_AVAILABLE:
            try:
                self.firecrawl = FirecrawlSearcher(verbose=verbose)
                self._log("Firecrawl web search initialized")
            except Exception as e:
                self._log(f"Warning: Could not initialize Firecrawl: {e}")

        if not self.firecrawl:
            self._log("Warning: Web search not available - using mock search")

    def _log(self, msg: str):
        if self.verbose:
            print(f"[ResearchBridge] {msg}")

    async def research_topic(self, topic: str,
                             num_results: int = 5) -> DomainDefinition:
        """
        Research a topic and extract numerical constants.

        Args:
            topic: Topic to research (e.g., "monarch butterfly navigation")
            num_results: Number of web search results to process

        Returns:
            DomainDefinition with extracted constants
        """
        self._log(f"Researching topic: {topic}")

        # Generate search queries
        queries = self._generate_queries(topic)

        all_constants = []
        all_sources = []

        for query in queries[:2]:  # Limit to 2 queries (Firecrawl rate limits)
            self._log(f"Searching: {query}")

            if self.firecrawl:
                # Use Firecrawl web search
                constants, sources = self._search_with_firecrawl(query, num_results)
            else:
                # Fallback to mock search
                constants, sources = self._search_mock(query)

            all_constants.extend(constants)
            all_sources.extend(sources)

        # Deduplicate constants
        unique_constants = self._deduplicate_constants(all_constants)

        # Create domain definition
        domain = DomainDefinition(
            name=self._normalize_name(topic),
            description=f"Research on {topic}",
            keywords=topic.lower().split(),
            constants=[asdict(c) for c in unique_constants],
            sources=list(set(all_sources))
        )

        self._log(f"Found {len(unique_constants)} constants from {len(all_sources)} sources")

        return domain

    def _generate_queries(self, topic: str) -> List[str]:
        """Generate search queries for a topic."""
        return [
            f"{topic} scientific constants measurements",
            f"{topic} physics numerical values data",
        ]

    def _search_with_firecrawl(self, query: str,
                                num_results: int) -> Tuple[List[ExtractedConstant], List[str]]:
        """Search using Firecrawl and extract constants."""
        constants = []
        sources = []

        if not self.firecrawl:
            return constants, sources

        # Search
        results = self.firecrawl.search(query, limit=num_results)

        if not results:
            self._log("No search results found")
            return constants, sources

        # Extract content from top results
        for result in results[:3]:  # Limit extractions
            sources.append(result.url)

            # Use snippet first (faster)
            if result.snippet:
                extracted = self.extractor.extract_from_text(result.snippet, result.url)
                constants.extend(extracted)

            # Optionally scrape full content for top result
            if result == results[0]:
                try:
                    content = self.firecrawl.scrape_url(result.url)
                    if content.success and content.content:
                        self._log(f"Scraped {len(content.content)} chars from {result.title[:40]}...")
                        extracted = self.extractor.extract_from_text(content.content, result.url)
                        constants.extend(extracted)
                except Exception as e:
                    self._log(f"Scrape failed: {e}")

        return constants, sources

    async def _search_with_hermes_legacy(self, query: str,
                                   num_results: int) -> Tuple[List[ExtractedConstant], List[str]]:
        """Legacy: Search using HermesFlow web tools (complex dependencies)."""
        constants = []
        sources = []

        # This method is kept for backwards compatibility but disabled
        # Use _search_with_firecrawl instead
        return constants, sources

    def _search_with_hermes_disabled(self, query: str,
                                      num_results: int) -> Tuple[List[ExtractedConstant], List[str]]:
        """Disabled: Original HermesFlow search (kept for reference)."""
        constants = []
        sources = []

        # Web search - disabled, using Firecrawl instead
        # search_result = web_search_tool(query, limit=num_results)
        # ...

        return constants, sources

    def _search_mock(self, query: str) -> Tuple[List[ExtractedConstant], List[str]]:
        """Mock search for when HermesFlow is not available."""
        self._log("Using mock search (HermesFlow not available)")

        # Return some example constants based on common topics
        mock_constants = []

        if 'butterfly' in query.lower() or 'monarch' in query.lower():
            mock_constants = [
                ExtractedConstant(
                    name="Migration bearing",
                    value=215.0,
                    uncertainty=5.0,
                    unit="degrees",
                    source_text="Monarch butterflies migrate at a bearing of approximately 215 degrees",
                    source_url="mock://butterfly.research",
                    confidence=0.8
                ),
                ExtractedConstant(
                    name="UV wavelength sensitivity",
                    value=420.0,
                    uncertainty=10.0,
                    unit="nm",
                    source_text="Monarch butterflies are sensitive to UV light at 420 nm",
                    source_url="mock://butterfly.research",
                    confidence=0.7
                ),
            ]
        elif 'earthquake' in query.lower() or 'richter' in query.lower():
            mock_constants = [
                ExtractedConstant(
                    name="Gutenberg-Richter b-value",
                    value=1.0,
                    uncertainty=0.1,
                    unit="",
                    source_text="The Gutenberg-Richter b-value is typically around 1.0",
                    source_url="mock://earthquake.research",
                    confidence=0.9
                ),
            ]
        elif 'turbulence' in query.lower() or 'karman' in query.lower() or 'reynolds' in query.lower():
            mock_constants = [
                ExtractedConstant(
                    name="von Kármán constant",
                    value=0.41,
                    uncertainty=0.01,
                    unit="",
                    source_text="The von Kármán constant κ ≈ 0.41 in turbulent boundary layers",
                    source_url="mock://turbulence.research",
                    confidence=0.9
                ),
                ExtractedConstant(
                    name="Strouhal number",
                    value=0.21,
                    uncertainty=0.01,
                    unit="",
                    source_text="The Strouhal number for vortex shedding is approximately 0.21",
                    source_url="mock://turbulence.research",
                    confidence=0.9
                ),
                ExtractedConstant(
                    name="Critical Reynolds (pipe)",
                    value=2300,
                    uncertainty=100,
                    unit="",
                    source_text="Turbulence transition in pipes occurs at Re ≈ 2300",
                    source_url="mock://turbulence.research",
                    confidence=0.85
                ),
                ExtractedConstant(
                    name="Kolmogorov constant",
                    value=1.5,
                    uncertainty=0.1,
                    unit="",
                    source_text="The Kolmogorov constant C_K ≈ 1.5 in the energy spectrum",
                    source_url="mock://turbulence.research",
                    confidence=0.8
                ),
            ]

        return mock_constants, ["mock://research.source"]

    def _deduplicate_constants(self, constants: List[ExtractedConstant]) -> List[ExtractedConstant]:
        """Remove duplicate constants."""
        seen = {}
        unique = []

        for const in constants:
            key = round(const.value, 4)
            if key not in seen or const.confidence > seen[key].confidence:
                seen[key] = const

        return list(seen.values())

    def _normalize_name(self, topic: str) -> str:
        """Normalize topic name for use as domain name."""
        return topic.lower().replace(' ', '-').replace('_', '-')

    def save_domain(self, domain: DomainDefinition) -> Path:
        """Save domain definition to JSON file."""
        filename = f"{domain.name}.json"
        filepath = self.domains_dir / filename

        with open(filepath, 'w') as f:
            f.write(domain.to_json())

        self._log(f"Saved domain to {filepath}")
        return filepath

    def load_domain(self, name: str) -> Optional[DomainDefinition]:
        """Load domain definition from JSON file."""
        filepath = self.domains_dir / f"{name}.json"

        if not filepath.exists():
            return None

        with open(filepath, 'r') as f:
            data = json.load(f)

        return DomainDefinition(**data)

    def list_domains(self) -> List[str]:
        """List all saved domain names."""
        return [f.stem for f in self.domains_dir.glob("*.json")]


# =============================================================================
# DOMAIN REGISTRY - Load and manage domains
# =============================================================================

class DomainRegistry:
    """
    Registry for managing domain definitions.

    Replaces hardcoded TOPIC_KNOWLEDGE with JSON-based domains.
    """

    def __init__(self, domains_dir: str = None):
        if domains_dir:
            self.domains_dir = Path(domains_dir)
        else:
            self.domains_dir = Path(__file__).parent.parent / "BriareusFlow" / "domains"
        self.domains_dir.mkdir(parents=True, exist_ok=True)

        self.domains: Dict[str, DomainDefinition] = {}
        self._load_all()

    def _load_all(self):
        """Load all domain JSON files."""
        for filepath in self.domains_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                domain = DomainDefinition(**data)
                self.domains[domain.name] = domain
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")

    def get(self, name: str) -> Optional[DomainDefinition]:
        """Get a domain by name."""
        return self.domains.get(name)

    def search(self, query: str) -> Optional[DomainDefinition]:
        """Fuzzy search for a domain by query."""
        query_lower = query.lower()

        # Exact match
        if query_lower in self.domains:
            return self.domains[query_lower]

        # Keyword match
        for name, domain in self.domains.items():
            if any(kw in query_lower for kw in domain.keywords):
                return domain
            if any(kw in name for kw in query_lower.split()):
                return domain

        return None

    def add(self, domain: DomainDefinition):
        """Add a domain to the registry."""
        self.domains[domain.name] = domain
        self._save(domain)

    def _save(self, domain: DomainDefinition):
        """Save a domain to JSON file."""
        filepath = self.domains_dir / f"{domain.name}.json"
        with open(filepath, 'w') as f:
            f.write(domain.to_json())

    def list_all(self) -> List[str]:
        """List all domain names."""
        return list(self.domains.keys())


# =============================================================================
# AUTOMATED DISCOVERY PIPELINE
# =============================================================================

async def run_automated_discovery(topic: str,
                                   timeout: float = 60,
                                   verbose: bool = True) -> Dict[str, Any]:
    """
    Run fully automated discovery on a topic.

    1. Research the topic using HermesFlow web tools
    2. Extract numerical constants
    3. Run BriareusFlow pattern search
    4. Return results

    Args:
        topic: Topic to research
        timeout: BriareusFlow timeout
        verbose: Print progress

    Returns:
        Dict with domain, targets, and results
    """
    if verbose:
        print("=" * 70)
        print("Z² AUTOMATED DISCOVERY ENGINE")
        print("=" * 70)
        print(f"\nTopic: {topic}\n")

    # 1. Research the topic
    bridge = ResearchBridge(verbose=verbose)
    domain = await bridge.research_topic(topic)

    if verbose:
        print(f"\nExtracted {len(domain.constants)} constants:")
        for const in domain.constants[:10]:
            print(f"  {const.get('name', 'Unknown')}: {const.get('value', 0):.6f}")

    # 2. Save domain
    bridge.save_domain(domain)

    # 3. Convert to search targets
    targets = domain.to_search_targets()

    if not targets:
        if verbose:
            print("\nNo constants found to search!")
        return {
            'domain': domain.to_dict(),
            'targets': [],
            'results': None
        }

    # 4. Run BriareusFlow (if available)
    if BRIAREUS_AVAILABLE:
        if verbose:
            print(f"\n{'=' * 70}")
            print("BRIAREUSFLOW PATTERN SEARCH")
            print("=" * 70)

        config = SearchConfig(
            max_error_percent=1.0,
            num_threads=8,
            verbose=verbose,
        )
        controller = BriareusController(config)
        controller.add_targets(targets)

        result = controller.run(timeout=timeout)

        if verbose:
            controller.print_summary(result)

        return {
            'domain': domain.to_dict(),
            'targets': [asdict(t) for t in targets],
            'results': result.to_dict()
        }
    else:
        if verbose:
            print("\nBriareusFlow not available - returning domain only")
        return {
            'domain': domain.to_dict(),
            'targets': [asdict(t) for t in targets],
            'results': None
        }


# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Z² Research Bridge")
    parser.add_argument("topic", nargs="?", default="gravitational constant",
                        help="Topic to research")
    parser.add_argument("--timeout", type=float, default=60,
                        help="Search timeout in seconds")
    parser.add_argument("--quiet", action="store_true",
                        help="Reduce output")

    args = parser.parse_args()

    # Run async discovery
    result = asyncio.run(run_automated_discovery(
        args.topic,
        timeout=args.timeout,
        verbose=not args.quiet
    ))

    print("\n" + "=" * 70)
    print("DISCOVERY COMPLETE")
    print("=" * 70)
    print(f"Domain: {result['domain']['name']}")
    print(f"Constants: {len(result['domain']['constants'])}")
    if result['results']:
        print(f"Z² patterns found: {result['results'].get('z2_patterns_found', 0)}")
