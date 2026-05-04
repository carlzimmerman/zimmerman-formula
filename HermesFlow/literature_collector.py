#!/usr/bin/env python3
"""
HermesFlow Literature Collector
================================

Dynamic literature discovery and measurement extraction.
Finds sources, fetches data, and extracts numerical values for Z² analysis.

Sources supported:
- Wikipedia (structured data)
- arXiv (preprints)
- NIST (physical constants)
- NASA (astronomy/cosmology)
- NOAA (meteorology)
- PDG (particle physics)

Author: Carl Zimmerman
Date: May 3, 2026
"""

import re
import json
import os
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import quote_plus

# Camofox for anti-detection browsing
CAMOFOX_URL = os.environ.get("CAMOFOX_URL", "http://localhost:9377")


@dataclass
class Source:
    """A literature source."""
    name: str
    url: str
    type: str  # 'database', 'paper', 'wiki', 'official'
    domain: str
    reliability: float  # 0-1


@dataclass
class Measurement:
    """An extracted measurement."""
    name: str
    value: float
    uncertainty: Optional[float]
    unit: str
    source: str
    context: str


class LiteratureCollector:
    """
    Dynamic literature discovery and measurement extraction.

    Usage:
        collector = LiteratureCollector()

        # Find sources for a topic
        sources = collector.find_sources('hurricane intensity')

        # Extract measurements from a source
        measurements = collector.extract_measurements(source_url)

        # Full pipeline: topic -> measurements
        data = collector.collect('neutrino mixing angles')
    """

    # Known authoritative sources by domain
    AUTHORITATIVE_SOURCES = {
        "physics": [
            Source("NIST CODATA", "https://physics.nist.gov/cuu/Constants/", "database", "physics", 1.0),
            Source("Particle Data Group", "https://pdglive.lbl.gov/", "database", "particle_physics", 1.0),
        ],
        "cosmology": [
            Source("Planck Legacy Archive", "https://wiki.cosmos.esa.int/planck-legacy-archive/", "database", "cosmology", 1.0),
            Source("NASA Lambda", "https://lambda.gsfc.nasa.gov/", "database", "cosmology", 0.95),
        ],
        "meteorology": [
            Source("NHC", "https://www.nhc.noaa.gov/", "official", "meteorology", 1.0),
            Source("NOAA HRD", "https://www.aoml.noaa.gov/hrd/", "database", "meteorology", 0.95),
        ],
        "neutrino": [
            Source("NuFIT", "http://www.nu-fit.org/", "database", "neutrino", 1.0),
        ],
    }

    # URL patterns for dynamic search
    SEARCH_PATTERNS = {
        "wikipedia": "https://en.wikipedia.org/wiki/{topic}",
        "arxiv": "https://arxiv.org/search/?query={topic}&searchtype=all",
        "scholar": "https://scholar.google.com/scholar?q={topic}",
        "nist": "https://physics.nist.gov/cgi-bin/cuu/Results?search_for={topic}",
    }

    # Regex patterns for extracting numbers with units
    NUMBER_PATTERNS = [
        # Scientific notation: 1.23e-4, 1.23×10⁻⁴
        r'(\d+\.?\d*)\s*[×x]\s*10[⁻\-]?(\d+)',
        r'(\d+\.?\d*)[eE]([+-]?\d+)',
        # With uncertainty: 137.036 ± 0.001
        r'(\d+\.?\d*)\s*[±\+\-]+\s*(\d+\.?\d*)',
        # Simple numbers with units
        r'(\d+\.?\d*)\s*(kt|km|GeV|MeV|eV|Hz|K|m|s|kg)',
        # Percentages
        r'(\d+\.?\d*)\s*%',
        # Ratios
        r'(\d+)/(\d+)',
    ]

    def __init__(self):
        self.cache = {}
        self.measurements_found = []

    def _is_camofox_available(self) -> bool:
        """Check if Camofox server is running."""
        try:
            response = requests.get(f"{CAMOFOX_URL}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def _fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL content, using Camofox if available."""
        # Check cache
        if url in self.cache:
            return self.cache[url]

        content = None

        # Try Camofox first (anti-detection)
        if self._is_camofox_available():
            try:
                response = requests.post(
                    f"{CAMOFOX_URL}/fetch",
                    json={"url": url},
                    timeout=30
                )
                if response.status_code == 200:
                    content = response.json().get("content", "")
            except Exception:
                pass

        # Fallback to direct requests
        if not content:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) HermesFlow/1.0'
                }
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    content = response.text
            except Exception:
                pass

        if content:
            self.cache[url] = content

        return content

    def find_sources(self, topic: str, max_sources: int = 5) -> List[Source]:
        """
        Dynamically find sources for a research topic.

        Args:
            topic: Research topic (e.g., 'hurricane structure', 'quark masses')
            max_sources: Maximum number of sources to return

        Returns:
            List of Source objects
        """
        sources = []
        topic_lower = topic.lower()

        # 1. Check authoritative sources by keyword
        for domain, domain_sources in self.AUTHORITATIVE_SOURCES.items():
            if domain in topic_lower or any(kw in topic_lower for kw in self._domain_keywords(domain)):
                sources.extend(domain_sources)

        # 2. Generate Wikipedia URL
        wiki_topic = topic.replace(' ', '_')
        sources.append(Source(
            f"Wikipedia: {topic}",
            self.SEARCH_PATTERNS["wikipedia"].format(topic=wiki_topic),
            "wiki",
            "general",
            0.7
        ))

        # 3. Generate arXiv search
        arxiv_query = quote_plus(topic)
        sources.append(Source(
            f"arXiv: {topic}",
            self.SEARCH_PATTERNS["arxiv"].format(topic=arxiv_query),
            "paper",
            "academic",
            0.9
        ))

        # Sort by reliability and limit
        sources.sort(key=lambda s: s.reliability, reverse=True)
        return sources[:max_sources]

    def _domain_keywords(self, domain: str) -> List[str]:
        """Get keywords associated with a domain."""
        keywords = {
            "physics": ["constant", "coupling", "mass", "charge", "fine structure"],
            "cosmology": ["dark energy", "hubble", "cmb", "cosmic", "expansion", "lambda"],
            "meteorology": ["hurricane", "cyclone", "storm", "wind", "weather"],
            "neutrino": ["neutrino", "oscillation", "mixing angle", "theta"],
        }
        return keywords.get(domain, [])

    def extract_measurements(self, content: str, context: str = "") -> List[Measurement]:
        """
        Extract numerical measurements from text content.

        Args:
            content: Text content to parse
            context: Source context for attribution

        Returns:
            List of Measurement objects
        """
        measurements = []

        # Look for common physics patterns
        patterns = {
            # Fine structure constant
            r'(?:fine.structure|α⁻¹|alpha)[^0-9]*(\d+\.?\d*)': ('alpha_inverse', None),
            # Weinberg angle
            r'sin²θ[_W]?\s*[=≈]\s*(\d+\.?\d*)': ('sin2_theta_w', None),
            # Dark energy
            r'Ω[_Λ]?\s*[=≈]\s*(\d+\.?\d*)': ('omega_lambda', None),
            # Hubble constant
            r'H[_0]?\s*[=≈]\s*(\d+\.?\d*)': ('hubble_constant', 'km/s/Mpc'),
            # Hurricane thresholds
            r'(\d+)\s*(?:kt|knots)[^0-9]*(?:tropical|storm|hurricane|category)': ('wind_threshold', 'kt'),
            # Neutrino angles
            r'θ[_12]*\s*[=≈]\s*(\d+\.?\d*)°?': ('theta_12', 'degrees'),
            r'θ[_23]*\s*[=≈]\s*(\d+\.?\d*)°?': ('theta_23', 'degrees'),
            r'θ[_13]*\s*[=≈]\s*(\d+\.?\d*)°?': ('theta_13', 'degrees'),
            # Mass values
            r'(\d+\.?\d*)\s*(?:GeV|MeV)': ('mass', 'GeV'),
            # Ratios
            r'ratio[^0-9]*(\d+\.?\d*)': ('ratio', None),
            # Eye/RMW
            r'eye[/\s]RMW[^0-9]*(\d+\.?\d*)': ('eye_rmw_ratio', None),
        }

        for pattern, (name, unit) in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match) if isinstance(match, str) else float(match[0])
                    measurements.append(Measurement(
                        name=name,
                        value=value,
                        uncertainty=None,
                        unit=unit or "",
                        source=context,
                        context=f"Extracted from {context}"
                    ))
                except (ValueError, IndexError):
                    continue

        # Extract numbers with uncertainty: 137.036 ± 0.001
        uncertainty_pattern = r'(\d+\.?\d*)\s*[±]\s*(\d+\.?\d*)'
        for match in re.finditer(uncertainty_pattern, content):
            try:
                value = float(match.group(1))
                unc = float(match.group(2))
                measurements.append(Measurement(
                    name=f"value_{len(measurements)}",
                    value=value,
                    uncertainty=unc,
                    unit="",
                    source=context,
                    context=f"Value with uncertainty from {context}"
                ))
            except ValueError:
                continue

        return measurements

    def collect(self, topic: str) -> Dict:
        """
        Full pipeline: Find sources, fetch content, extract measurements.

        Args:
            topic: Research topic

        Returns:
            Dict with sources, measurements, and summary
        """
        result = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "sources": [],
            "measurements": [],
            "errors": []
        }

        # Find sources
        sources = self.find_sources(topic)
        result["sources"] = [asdict(s) for s in sources]

        # Fetch and extract from each source
        for source in sources:
            try:
                content = self._fetch_url(source.url)
                if content:
                    measurements = self.extract_measurements(content, source.name)
                    result["measurements"].extend([asdict(m) for m in measurements])
                else:
                    result["errors"].append(f"Failed to fetch: {source.url}")
            except Exception as e:
                result["errors"].append(f"Error processing {source.url}: {str(e)}")

        # Deduplicate measurements by name
        seen = {}
        unique_measurements = []
        for m in result["measurements"]:
            key = (m["name"], round(m["value"], 4))
            if key not in seen:
                seen[key] = True
                unique_measurements.append(m)
        result["measurements"] = unique_measurements

        # Summary
        result["summary"] = {
            "sources_found": len(result["sources"]),
            "sources_fetched": len(result["sources"]) - len(result["errors"]),
            "measurements_extracted": len(result["measurements"]),
            "unique_values": len(unique_measurements)
        }

        return result

    def search_wikipedia(self, topic: str) -> Optional[Dict]:
        """
        Search Wikipedia for structured data about a topic.
        Uses Wikipedia API for reliable data extraction.

        Args:
            topic: Topic to search

        Returns:
            Dict with extracted data or None
        """
        # Use Wikipedia API
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(topic)}"

        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "title": data.get("title"),
                    "extract": data.get("extract"),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                    "measurements": self.extract_measurements(
                        data.get("extract", ""),
                        f"Wikipedia: {topic}"
                    )
                }
        except Exception:
            pass

        return None

    def search_arxiv(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search arXiv for relevant papers.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of paper metadata
        """
        # arXiv API
        api_url = f"http://export.arxiv.org/api/query?search_query=all:{quote_plus(query)}&max_results={max_results}"

        papers = []
        try:
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                # Parse Atom feed (simplified)
                content = response.text

                # Extract entries
                entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
                for entry in entries:
                    title_match = re.search(r'<title>(.*?)</title>', entry)
                    summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                    link_match = re.search(r'<id>(.*?)</id>', entry)

                    if title_match:
                        paper = {
                            "title": title_match.group(1).strip(),
                            "summary": summary_match.group(1).strip() if summary_match else "",
                            "url": link_match.group(1) if link_match else "",
                        }
                        # Extract measurements from abstract
                        paper["measurements"] = self.extract_measurements(
                            paper["summary"],
                            f"arXiv: {paper['title'][:50]}"
                        )
                        papers.append(paper)
        except Exception:
            pass

        return papers


# =============================================================================
# Integration with HermesFlow
# =============================================================================

def collect_literature_for_research(topic: str) -> Dict:
    """
    Main entry point for literature collection.

    Args:
        topic: Research topic

    Returns:
        Dict ready for Z² analysis
    """
    collector = LiteratureCollector()

    # Collect from all sources
    result = collector.collect(topic)

    # Also try Wikipedia API
    wiki_data = collector.search_wikipedia(topic)
    if wiki_data:
        result["wikipedia"] = wiki_data

    # Try arXiv
    arxiv_papers = collector.search_arxiv(topic, max_results=3)
    if arxiv_papers:
        result["arxiv_papers"] = arxiv_papers
        # Add measurements from papers
        for paper in arxiv_papers:
            for m in paper.get("measurements", []):
                result["measurements"].append(asdict(m) if hasattr(m, '__dict__') else m)

    return result


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI for literature collection."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python literature_collector.py <topic>")
        print("Example: python literature_collector.py 'hurricane intensity'")
        sys.exit(1)

    topic = ' '.join(sys.argv[1:])
    print(f"Collecting literature for: {topic}")
    print("=" * 60)

    result = collect_literature_for_research(topic)

    print(f"\nSources found: {result['summary']['sources_found']}")
    print(f"Measurements extracted: {result['summary']['measurements_extracted']}")

    if result["measurements"]:
        print("\nMeasurements:")
        for m in result["measurements"][:10]:
            print(f"  {m['name']}: {m['value']} {m.get('unit', '')}")

    if result.get("wikipedia"):
        print(f"\nWikipedia: {result['wikipedia'].get('title')}")

    if result.get("arxiv_papers"):
        print(f"\narXiv papers: {len(result['arxiv_papers'])}")
        for p in result["arxiv_papers"]:
            print(f"  - {p['title'][:60]}...")


if __name__ == "__main__":
    main()
