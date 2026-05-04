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
import subprocess
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from urllib.parse import quote_plus

# Camofox for anti-detection browsing
CAMOFOX_URL = os.environ.get("CAMOFOX_URL", "http://localhost:9377")

# Legomena model for intelligent parsing
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-31b")


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

    def __init__(self, use_legomena: bool = True):
        self.cache = {}
        self.measurements_found = []
        self.use_legomena = use_legomena
        self._legomena_available = None  # Lazy check

    def _is_legomena_available(self) -> bool:
        """Check if Legomena model is available via Ollama."""
        if self._legomena_available is not None:
            return self._legomena_available

        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True, text=True, timeout=5
            )
            self._legomena_available = "legomena" in result.stdout.lower()
        except Exception:
            self._legomena_available = False

        return self._legomena_available

    def _call_legomena(self, prompt: str, timeout: int = 60) -> Optional[str]:
        """Call Legomena model for intelligent parsing."""
        if not self._is_legomena_available():
            return None

        try:
            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL, prompt],
                capture_output=True, text=True, timeout=timeout
            )
            # Clean ANSI codes
            text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', result.stdout)
            return text.strip()
        except Exception:
            return None

    def extract_with_legomena(self, content: str, topic: str) -> List[Measurement]:
        """
        Use Legomena LLM to intelligently extract measurements from text.

        This is more powerful than regex - it understands context and can:
        - Identify what values are being measured
        - Extract values with proper units
        - Understand uncertainty notation
        - Recognize physical constants

        Args:
            content: Text content to parse
            topic: Research topic for context

        Returns:
            List of Measurement objects
        """
        if not self.use_legomena or not self._is_legomena_available():
            return []

        # Truncate content if too long
        max_chars = 4000
        if len(content) > max_chars:
            content = content[:max_chars] + "..."

        prompt = f"""Extract all numerical measurements from this text about {topic}.

TEXT:
{content}

Return ONLY valid JSON array. Each measurement should have:
- name: what is being measured (e.g., "fine_structure_constant", "wind_speed")
- value: the numerical value (number only)
- uncertainty: uncertainty if given (number or null)
- unit: the unit (e.g., "kt", "GeV", "degrees", or "" if dimensionless)

Example output:
[
  {{"name": "alpha_inverse", "value": 137.036, "uncertainty": 0.001, "unit": ""}},
  {{"name": "wind_speed", "value": 34, "uncertainty": null, "unit": "kt"}}
]

Return ONLY the JSON array, no other text:"""

        response = self._call_legomena(prompt, timeout=90)
        if not response:
            return []

        # Parse JSON from response
        measurements = []
        try:
            # Find JSON array in response
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)

                for item in data:
                    if isinstance(item, dict) and 'name' in item and 'value' in item:
                        try:
                            measurements.append(Measurement(
                                name=str(item['name']),
                                value=float(item['value']),
                                uncertainty=float(item['uncertainty']) if item.get('uncertainty') else None,
                                unit=str(item.get('unit', '')),
                                source=f"Legomena extraction: {topic}",
                                context=f"LLM-extracted from {topic} content"
                            ))
                        except (ValueError, TypeError):
                            continue
        except json.JSONDecodeError:
            pass

        return measurements

    def analyze_z2_relevance(self, content: str, topic: str) -> Dict:
        """
        Use Legomena to analyze potential Z² connections in content.

        Args:
            content: Text content to analyze
            topic: Research topic

        Returns:
            Dict with Z² relevance analysis
        """
        if not self.use_legomena or not self._is_legomena_available():
            return {"error": "Legomena not available"}

        # Truncate content
        max_chars = 3000
        if len(content) > max_chars:
            content = content[:max_chars] + "..."

        prompt = f"""Analyze this text about {topic} for potential connections to Z² = 32π/3 ≈ 33.51.

Z² is a geometric constant (cube × sphere ratio) that appears in:
- Fine structure constant: α⁻¹ = 4Z² + 3 ≈ 137
- Dark energy density: Ω_Λ = 13/19 ≈ 0.684
- Golden ratio relationships: φ = 1.618, 1/φ = 0.618

TEXT:
{content}

Analyze and return JSON:
{{
  "potential_z2_connections": [
    {{"measurement": "name", "value": number, "possible_formula": "formula", "reasoning": "why"}}
  ],
  "key_constants_found": ["list of numerical constants mentioned"],
  "relevance_score": 0-10,
  "summary": "brief analysis"
}}

Return ONLY valid JSON:"""

        response = self._call_legomena(prompt, timeout=90)
        if not response:
            return {"error": "Legomena call failed"}

        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            pass

        return {"error": "Failed to parse response", "raw": response[:500]}

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

    def extract_measurements(self, content: str, context: str = "",
                              topic: str = None) -> List[Measurement]:
        """
        Extract numerical measurements from text content.

        Uses Legomena LLM for intelligent extraction if available,
        falls back to regex patterns.

        Args:
            content: Text content to parse
            context: Source context for attribution
            topic: Research topic (helps Legomena understand context)

        Returns:
            List of Measurement objects
        """
        measurements = []

        # Try Legomena first for intelligent extraction
        if self.use_legomena and topic:
            legomena_results = self.extract_with_legomena(content, topic)
            if legomena_results:
                measurements.extend(legomena_results)
                # If Legomena found results, return them (more accurate)
                if len(measurements) >= 2:
                    return measurements

        # Fallback to regex patterns
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
                    # Pass topic to enable Legomena extraction
                    measurements = self.extract_measurements(content, source.name, topic=topic)
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
        # Use Wikipedia API (requires User-Agent header)
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(topic)}"
        headers = {
            "User-Agent": "HermesFlow/1.1 (Z2 Research; contact@zimmerman-research.org)"
        }

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                extract = data.get("extract", "")

                result = {
                    "title": data.get("title"),
                    "extract": extract,
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                    "measurements": self.extract_measurements(
                        extract,
                        f"Wikipedia: {topic}",
                        topic=topic
                    )
                }

                # If Legomena available, also analyze for Z² relevance
                if self.use_legomena and self._is_legomena_available():
                    result["z2_analysis"] = self.analyze_z2_relevance(extract, topic)

                return result
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
        headers = {
            "User-Agent": "HermesFlow/1.1 (Z2 Research; contact@zimmerman-research.org)"
        }

        papers = []
        try:
            response = requests.get(api_url, headers=headers, timeout=15)
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
                        title = title_match.group(1).strip()
                        summary = summary_match.group(1).strip() if summary_match else ""

                        paper = {
                            "title": title,
                            "summary": summary,
                            "url": link_match.group(1) if link_match else "",
                        }
                        # Extract measurements from abstract with Legomena
                        paper["measurements"] = self.extract_measurements(
                            summary,
                            f"arXiv: {title[:50]}",
                            topic=query  # Use search query as topic
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
