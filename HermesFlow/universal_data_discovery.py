#!/usr/bin/env python3
"""
UNIVERSAL DATA DISCOVERY ENGINE
================================

Dynamically discovers and fetches authoritative data for ANY research domain.

NOT hardcoded per-domain. Uses LLM + web search to:
1. Identify the research domain
2. Discover measurable physical quantities
3. Find authoritative data sources
4. Fetch measurements with uncertainties
5. Adapt to any new domain automatically

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import re
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

# HeliconLake integration
try:
    from .helicon_lake import HeliconLake, SourceEntry
    HELICON_AVAILABLE = True
except ImportError:
    try:
        from helicon_lake import HeliconLake, SourceEntry
        HELICON_AVAILABLE = True
    except ImportError:
        HELICON_AVAILABLE = False
        HeliconLake = None
        SourceEntry = None

# DatabaseQueryHandler integration
try:
    from .database_query_handler import DatabaseQueryHandler, QueryResult
    DATABASE_HANDLER_AVAILABLE = True
except ImportError:
    try:
        from database_query_handler import DatabaseQueryHandler, QueryResult
        DATABASE_HANDLER_AVAILABLE = True
    except ImportError:
        DATABASE_HANDLER_AVAILABLE = False
        DatabaseQueryHandler = None
        QueryResult = None

# AutonomousAPIDiscovery integration
try:
    from .autonomous_api_discovery import AutonomousAPIDiscovery, DiscoveryResult
    AUTONOMOUS_DISCOVERY_AVAILABLE = True
except ImportError:
    try:
        from autonomous_api_discovery import AutonomousAPIDiscovery, DiscoveryResult
        AUTONOMOUS_DISCOVERY_AVAILABLE = True
    except ImportError:
        AUTONOMOUS_DISCOVERY_AVAILABLE = False
        AutonomousAPIDiscovery = None
        DiscoveryResult = None

# Constants
Z2 = 32 * 3.14159265358979 / 3
Z = Z2 ** 0.5
PHI = (1 + 5 ** 0.5) / 2

# LLM config
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-31b")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "300"))


class SourceType(Enum):
    """Types of data sources."""
    API = "api"                    # REST API with JSON
    CSV = "csv"                    # Downloadable CSV/TSV
    DATABASE = "database"          # Online database with web interface
    PAPER = "paper"                # Published paper with data tables
    GOVERNMENT = "government"      # Government agency data
    WIKI = "wiki"                  # Wikipedia (low reliability)


class DataQuality(Enum):
    """Data quality levels."""
    AUTHORITATIVE = "authoritative"   # CODATA, PDG, official agencies
    PEER_REVIEWED = "peer_reviewed"   # Published papers
    INSTITUTIONAL = "institutional"   # Universities, research labs
    SECONDARY = "secondary"           # Compilations, encyclopedias
    UNVERIFIED = "unverified"         # Unknown provenance


@dataclass
class Quantity:
    """A measurable physical quantity."""
    name: str                         # e.g., "eye_diameter"
    description: str                  # e.g., "Hurricane eye diameter"
    unit: str                         # e.g., "nautical miles"
    typical_range: Tuple[float, float] = (0, 0)  # Expected value range
    is_ratio: bool = False            # True if dimensionless ratio


@dataclass
class DataSource:
    """An authoritative data source."""
    name: str                         # e.g., "NOAA Extended Best Track"
    url: str                          # Base URL
    source_type: SourceType
    quality: DataQuality
    description: str
    access_method: str                # How to get data: "api", "download", "scrape"
    quantities_available: List[str]   # What can be measured from this source
    citation: str = ""
    last_verified: str = ""


@dataclass
class Measurement:
    """A single measurement with metadata."""
    quantity: str                     # What was measured
    value: float                      # The value
    uncertainty: Optional[float]      # Measurement uncertainty
    unit: str
    source: str                       # Data source name
    source_url: str
    quality: DataQuality
    context: str = ""                 # Additional context
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DomainProfile:
    """Profile of a research domain."""
    name: str                         # e.g., "meteorology"
    subdomain: str                    # e.g., "tropical_cyclones"
    description: str
    key_quantities: List[Quantity]
    known_sources: List[DataSource]
    z2_relevance: str                 # How Z² might apply
    prior_findings: List[Dict] = field(default_factory=list)


class UniversalDataDiscovery:
    """
    Dynamically discover and fetch data for ANY research domain.

    This is the core engine that makes HermesFlow truly dynamic.
    """

    # Known authoritative source patterns (bootstrapping)
    AUTHORITATIVE_PATTERNS = {
        "physics": ["CODATA", "PDG", "NIST", "arXiv hep-"],
        "cosmology": ["Planck", "WMAP", "SDSS", "DES", "arXiv astro-ph"],
        "meteorology": ["NOAA", "NHC", "ECMWF", "ERA5", "IBTrACS"],
        "chemistry": ["PubChem", "ChEMBL", "CSD", "IUPAC"],
        "biology": ["PDB", "UniProt", "NCBI", "GenBank"],
        "geophysics": ["USGS", "IRIS", "UNAVCO"],
        "astronomy": ["NASA", "ESA", "Gaia", "SDSS"],
    }

    # Known data APIs
    KNOWN_APIS = {
        "wikipedia": "https://en.wikipedia.org/api/rest_v1/",
        "arxiv": "http://export.arxiv.org/api/query",
        "pubchem": "https://pubchem.ncbi.nlm.nih.gov/rest/pug/",
        "pdg": "https://pdglive.lbl.gov/",
        "codata": "https://physics.nist.gov/cuu/Constants/",
    }

    def __init__(self, use_legomena: bool = True, use_web_search: bool = True,
                 use_helicon_lake: bool = True, use_database_apis: bool = True):
        self.use_legomena = use_legomena
        self.use_web_search = use_web_search
        self.use_helicon_lake = use_helicon_lake
        self.use_database_apis = use_database_apis
        self.discovered_domains: Dict[str, DomainProfile] = {}
        self.discovered_sources: Dict[str, DataSource] = {}

        # Initialize HeliconLake for source registry
        self.helicon_lake = None
        if use_helicon_lake and HELICON_AVAILABLE:
            try:
                self.helicon_lake = HeliconLake()
                print(f"HeliconLake initialized: {self.helicon_lake.get_statistics()['total_sources']} sources")
            except Exception as e:
                print(f"HeliconLake initialization failed: {e}")

        # Initialize DatabaseQueryHandler for API access
        self.db_handler = None
        if use_database_apis and DATABASE_HANDLER_AVAILABLE:
            try:
                self.db_handler = DatabaseQueryHandler(verbose=True)
                apis = self.db_handler.get_available_apis()
                print(f"DatabaseQueryHandler initialized: {len(apis)} known APIs")
            except Exception as e:
                print(f"DatabaseQueryHandler initialization failed: {e}")

        # Initialize AutonomousAPIDiscovery for self-learning
        self.auto_discovery = None
        if use_database_apis and AUTONOMOUS_DISCOVERY_AVAILABLE:
            try:
                self.auto_discovery = AutonomousAPIDiscovery(verbose=True)
                print(f"AutonomousAPIDiscovery initialized: ready for self-learning")
            except Exception as e:
                print(f"AutonomousAPIDiscovery initialization failed: {e}")

    def _call_legomena(self, prompt: str, timeout: int = None) -> Optional[str]:
        """Call Legomena for intelligent reasoning."""
        if not self.use_legomena:
            return None

        timeout = timeout or LEGOMENA_TIMEOUT
        try:
            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print(f"Legomena timeout ({timeout}s)")
        except Exception as e:
            print(f"Legomena error: {e}")
        return None

    def _web_search(self, query: str) -> List[Dict]:
        """Search the web for data sources."""
        if not self.use_web_search:
            return []

        # Use DuckDuckGo instant answers API (no auth required)
        try:
            response = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1},
                timeout=10
            )
            if response.ok:
                data = response.json()
                results = []
                if data.get("AbstractURL"):
                    results.append({
                        "title": data.get("Heading", ""),
                        "url": data.get("AbstractURL"),
                        "snippet": data.get("AbstractText", "")
                    })
                for topic in data.get("RelatedTopics", [])[:5]:
                    if isinstance(topic, dict) and topic.get("FirstURL"):
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "url": topic.get("FirstURL"),
                            "snippet": topic.get("Text", "")
                        })
                return results
        except Exception as e:
            print(f"Web search error: {e}")
        return []

    def discover_domain(self, research_topic: str) -> DomainProfile:
        """
        Analyze a research topic to identify its domain and characteristics.

        This is the first step - understanding WHAT we're researching.
        """
        # Check cache
        topic_key = research_topic.lower().replace(" ", "_")[:50]
        if topic_key in self.discovered_domains:
            return self.discovered_domains[topic_key]

        # Use Legomena to analyze the domain
        prompt = f"""Analyze this research topic and identify its scientific domain.

RESEARCH TOPIC: {research_topic}

Respond in this EXACT JSON format:
{{
    "domain": "<primary scientific field: physics/chemistry/biology/meteorology/cosmology/etc>",
    "subdomain": "<specific subfield>",
    "description": "<one sentence describing the research area>",
    "key_quantities": [
        {{"name": "<quantity_name>", "description": "<what it measures>", "unit": "<SI unit>", "is_ratio": <true/false>}},
        ...
    ],
    "authoritative_sources": [
        "<name of authoritative data source>",
        ...
    ],
    "z2_relevance": "<how Z² geometry might apply to this domain>"
}}

Be SPECIFIC about quantities. For hurricanes, include: eye_diameter, radius_of_maximum_wind, maximum_sustained_wind, central_pressure.
For particle physics: mass, charge, spin, lifetime, coupling_constant.
For cosmology: Hubble_constant, dark_energy_density, CMB_temperature, baryon_density.

JSON response:"""

        response = self._call_legomena(prompt)

        if response:
            try:
                # Extract JSON from response
                json_match = re.search(r'\{[\s\S]*\}', response)
                if json_match:
                    data = json.loads(json_match.group())

                    # Build quantities
                    quantities = []
                    for q in data.get("key_quantities", []):
                        quantities.append(Quantity(
                            name=q.get("name", "unknown"),
                            description=q.get("description", ""),
                            unit=q.get("unit", ""),
                            is_ratio=q.get("is_ratio", False)
                        ))

                    # Build profile
                    profile = DomainProfile(
                        name=data.get("domain", "unknown"),
                        subdomain=data.get("subdomain", ""),
                        description=data.get("description", ""),
                        key_quantities=quantities,
                        known_sources=[],
                        z2_relevance=data.get("z2_relevance", "")
                    )

                    self.discovered_domains[topic_key] = profile
                    return profile
            except json.JSONDecodeError:
                pass

        # Fallback: basic analysis
        return DomainProfile(
            name="unknown",
            subdomain="",
            description=research_topic,
            key_quantities=[],
            known_sources=[],
            z2_relevance="Unknown - requires analysis"
        )

    def discover_data_sources(self, domain: DomainProfile) -> List[DataSource]:
        """
        Discover authoritative data sources for a domain.

        PRIORITY ORDER:
        1. Query known database APIs (DatabaseQueryHandler)
        2. Query HeliconLake for cached sources
        3. Validate known sources are still active
        4. Fall back to web search if needed
        5. Register new discoveries to HeliconLake
        """
        sources = []

        # STEP 0: Query known database APIs first (most reliable)
        if self.db_handler:
            topic = domain.subdomain if domain.subdomain else None
            api_matches = self.db_handler.find_apis_for_domain(domain.name, topic)

            if api_matches:
                print(f"DatabaseQueryHandler: Found {len(api_matches)} known APIs for {domain.name}/{topic}")
                for config in api_matches:
                    sources.append(DataSource(
                        name=config.name,
                        url=config.base_url,
                        source_type=SourceType.API,
                        quality=DataQuality.AUTHORITATIVE,
                        description=config.description,
                        access_method="api",
                        quantities_available=config.quantities
                    ))

                # If we found good API sources, we can return early for efficiency
                if len(api_matches) >= 2:
                    print(f"DatabaseQueryHandler: Using {len(api_matches)} API sources")
                    return sources

        # STEP 0.5: If no known APIs, try AUTONOMOUS DISCOVERY
        if not sources and self.auto_discovery:
            print(f"No known APIs for {domain.name} - triggering AUTONOMOUS DISCOVERY...")
            topic = domain.subdomain if domain.subdomain else ""

            discovery_result = self.auto_discovery.discover(domain.name, topic)

            if discovery_result.working_configs:
                print(f"AutonomousAPIDiscovery: Discovered {len(discovery_result.working_configs)} working APIs!")
                for config in discovery_result.working_configs:
                    sources.append(DataSource(
                        name=config.name,
                        url=config.base_url,
                        source_type=SourceType.API,
                        quality=DataQuality.INSTITUTIONAL,  # Auto-discovered = medium confidence
                        description=config.description,
                        access_method="api",
                        quantities_available=config.quantities
                    ))

                    # Also add to db_handler for immediate use
                    if self.db_handler:
                        api_key = f"auto_{domain.name}_{len(self.db_handler.known_apis)}"
                        self.db_handler.known_apis[api_key] = config

                if sources:
                    print(f"AutonomousAPIDiscovery: Using {len(sources)} newly discovered APIs")
                    return sources
            else:
                print(f"AutonomousAPIDiscovery: No working APIs found ({discovery_result.apis_discovered} analyzed, {len(discovery_result.failed_attempts)} failed)")

        # STEP 1: Query HeliconLake for cached sources (if available)
        if self.helicon_lake:
            lake_sources = self.helicon_lake.find_sources(domain.name, domain.subdomain)
            if lake_sources:
                print(f"HeliconLake: Found {len(lake_sources)} known sources for {domain.name}/{domain.subdomain}")
                for src in lake_sources:
                    # Convert HeliconLake entry to DataSource
                    sources.append(DataSource(
                        name=src.description or src.url,
                        url=src.url,
                        source_type=SourceType.DATABASE,
                        quality=DataQuality.AUTHORITATIVE if src.authority_score > 0.7 else DataQuality.INSTITUTIONAL,
                        description=src.description,
                        access_method=src.format,
                        quantities_available=src.quantities
                    ))

                # If we have active sources, return them
                active_sources = [s for s in lake_sources if s.validation_status == 'active']
                if active_sources:
                    print(f"HeliconLake: Using {len(active_sources)} active sources")
                    return sources

                # Otherwise validate what we have
                print("HeliconLake: Validating known sources...")
                for src in lake_sources[:3]:  # Validate top 3
                    self.helicon_lake.validate_source(src.id)

        # STEP 2: Fall back to web search
        print(f"Searching web for {domain.name}/{domain.subdomain} sources...")

        # Search for authoritative sources
        search_queries = [
            f"{domain.name} {domain.subdomain} official database",
            f"{domain.name} authoritative data source",
            f"{domain.subdomain} measurement database",
        ]

        for query in search_queries:
            results = self._web_search(query)
            for r in results:
                # Check if this looks authoritative
                url = r.get("url", "")
                title = r.get("title", "")

                quality = DataQuality.UNVERIFIED
                source_type = SourceType.DATABASE

                # Identify quality from URL/title
                if any(p in url.lower() or p in title.lower()
                       for patterns in self.AUTHORITATIVE_PATTERNS.values()
                       for p in patterns):
                    quality = DataQuality.AUTHORITATIVE
                elif ".gov" in url or ".edu" in url:
                    quality = DataQuality.INSTITUTIONAL
                elif "arxiv" in url or "doi.org" in url:
                    quality = DataQuality.PEER_REVIEWED
                elif "wikipedia" in url:
                    quality = DataQuality.SECONDARY

                sources.append(DataSource(
                    name=title[:100] if title else url,
                    url=url,
                    source_type=source_type,
                    quality=quality,
                    description=r.get("snippet", "")[:200],
                    access_method="web",
                    quantities_available=[q.name for q in domain.key_quantities]
                ))

        # Use Legomena to identify best sources
        if sources and self.use_legomena:
            prompt = f"""Given this research domain and discovered sources, identify the BEST authoritative data sources.

DOMAIN: {domain.name} / {domain.subdomain}
KEY QUANTITIES: {[q.name for q in domain.key_quantities]}

DISCOVERED SOURCES:
{json.dumps([{"name": s.name, "url": s.url, "quality": s.quality.value} for s in sources[:10]], indent=2)}

Which sources are MOST authoritative for getting actual measurement data?
List the top 3 source names and explain why they are authoritative.

Response:"""

            response = self._call_legomena(prompt, timeout=60)
            if response:
                # Could parse this to reorder sources, but for now just log
                print(f"LLM source analysis: {response[:500]}")

        # Update domain profile
        domain.known_sources = sources[:10]  # Keep top 10

        # STEP 3: Register new discoveries to HeliconLake
        if self.helicon_lake and sources:
            registered = 0
            for src in sources[:5]:  # Register top 5
                try:
                    self.helicon_lake.register_source({
                        'url': src.url,
                        'description': src.description or src.name,
                        'domains': [domain.name],
                        'topics': [domain.subdomain] if domain.subdomain else [],
                        'quantities': src.quantities_available,
                        'format': src.access_method,
                        'organization': src.name,
                        'authority_score': 0.9 if src.quality == DataQuality.AUTHORITATIVE else 0.7 if src.quality == DataQuality.INSTITUTIONAL else 0.5,
                        'discovered_by': 'UniversalDataDiscovery',
                        'discovery_method': 'web_search'
                    })
                    registered += 1
                except Exception as e:
                    pass  # Don't fail on registration errors
            if registered > 0:
                print(f"HeliconLake: Registered {registered} new sources")

        return sources

    def discover_quantities(self, research_topic: str, domain: DomainProfile) -> List[Quantity]:
        """
        Discover specific measurable quantities for a research topic.

        Goes deeper than domain profile to find EXACT quantities.
        """
        prompt = f"""For this research topic, identify ALL measurable physical quantities.

RESEARCH TOPIC: {research_topic}
DOMAIN: {domain.name} / {domain.subdomain}

List EVERY quantity that can be measured with numerical values.
Include ratios, thresholds, constants, and relationships.

For each quantity, specify:
1. Name (e.g., "eye_diameter_to_rmw_ratio")
2. Description
3. Unit (or "dimensionless" for ratios)
4. Typical range of values
5. Whether it could relate to Z² = {Z2:.4f}, Z = {Z:.4f}, or φ = {PHI:.4f}

Format as JSON array:
[
    {{"name": "...", "description": "...", "unit": "...", "range": [min, max], "z2_potential": "..."}},
    ...
]

JSON:"""

        response = self._call_legomena(prompt)

        if response:
            try:
                json_match = re.search(r'\[[\s\S]*\]', response)
                if json_match:
                    data = json.loads(json_match.group())
                    quantities = []
                    for q in data:
                        quantities.append(Quantity(
                            name=q.get("name", "unknown"),
                            description=q.get("description", ""),
                            unit=q.get("unit", ""),
                            typical_range=tuple(q.get("range", [0, 0])),
                            is_ratio="ratio" in q.get("name", "").lower() or q.get("unit") == "dimensionless"
                        ))
                    return quantities
            except json.JSONDecodeError:
                pass

        return domain.key_quantities

    def fetch_measurements(self, source: DataSource, quantities: List[str]) -> List[Measurement]:
        """
        Fetch actual measurements from a data source.

        This is the ADAPTIVE part - handles different source types.
        """
        measurements = []

        # Try DatabaseQueryHandler first for known APIs
        if self.db_handler and source.source_type == SourceType.API:
            measurements = self._fetch_from_known_api(source, quantities)
            if measurements:
                return measurements

        if source.source_type == SourceType.API:
            measurements = self._fetch_from_api(source, quantities)
        elif source.source_type == SourceType.CSV:
            measurements = self._fetch_from_csv(source, quantities)
        elif source.source_type == SourceType.DATABASE:
            measurements = self._fetch_from_database(source, quantities)
        else:
            # Web scrape as fallback
            measurements = self._fetch_from_web(source, quantities)

        return measurements

    def _fetch_from_known_api(self, source: DataSource, quantities: List[str]) -> List[Measurement]:
        """Fetch from a known API using DatabaseQueryHandler."""
        measurements = []

        if not self.db_handler:
            return measurements

        # Find matching API by URL or name
        for api_name, config in self.db_handler.known_apis.items():
            if config.base_url == source.url or config.name == source.name:
                result = self.db_handler.query(api_name)

                if result.success and result.data is not None:
                    df = result.data
                    print(f"DatabaseQueryHandler: Got {len(df)} rows from {api_name}")

                    # Extract measurements from DataFrame
                    for col in df.columns:
                        col_lower = col.lower()
                        for q in quantities:
                            if q.lower() in col_lower or col_lower in q.lower():
                                # Get column statistics
                                if df[col].dtype in ['float64', 'int64', 'float32', 'int32']:
                                    values = df[col].dropna()
                                    if len(values) > 0:
                                        measurements.append(Measurement(
                                            quantity=q,
                                            value=float(values.mean()),
                                            uncertainty=float(values.std()) if len(values) > 1 else None,
                                            unit="",
                                            source=source.name,
                                            source_url=source.url,
                                            quality=source.quality,
                                            context=f"mean of {len(values)} values, range [{values.min():.4f}, {values.max():.4f}]"
                                        ))

                    # Also store the full DataFrame for later analysis
                    if not hasattr(self, 'fetched_dataframes'):
                        self.fetched_dataframes = {}
                    self.fetched_dataframes[api_name] = df

                break

        return measurements

    def _fetch_from_api(self, source: DataSource, quantities: List[str]) -> List[Measurement]:
        """Fetch from REST API."""
        measurements = []

        # Try common API patterns
        try:
            response = requests.get(source.url, timeout=30)
            if response.ok:
                data = response.json()
                # Extract measurements (generic parsing)
                measurements = self._extract_measurements_from_json(data, source, quantities)
        except Exception as e:
            print(f"API fetch error: {e}")

        return measurements

    def _fetch_from_csv(self, source: DataSource, quantities: List[str]) -> List[Measurement]:
        """Fetch and parse CSV data."""
        measurements = []

        try:
            response = requests.get(source.url, timeout=60)
            if response.ok:
                import csv
                from io import StringIO
                reader = csv.DictReader(StringIO(response.text))
                for row in reader:
                    for q in quantities:
                        if q in row:
                            try:
                                value = float(row[q])
                                measurements.append(Measurement(
                                    quantity=q,
                                    value=value,
                                    uncertainty=None,
                                    unit="",
                                    source=source.name,
                                    source_url=source.url,
                                    quality=source.quality,
                                    context=str(row)[:200]
                                ))
                            except ValueError:
                                pass
        except Exception as e:
            print(f"CSV fetch error: {e}")

        return measurements

    def _fetch_from_database(self, source: DataSource, quantities: List[str]) -> List[Measurement]:
        """Fetch from web database (may require scraping)."""
        return self._fetch_from_web(source, quantities)

    def _fetch_from_web(self, source: DataSource, quantities: List[str]) -> List[Measurement]:
        """Scrape measurements from web page."""
        measurements = []

        try:
            headers = {"User-Agent": "HermesFlow/2.0 (Z2 Research)"}
            response = requests.get(source.url, headers=headers, timeout=30)
            if response.ok:
                # Use LLM to extract measurements
                text = response.text[:10000]  # Limit size

                prompt = f"""Extract numerical measurements from this web page content.

QUANTITIES TO FIND: {quantities}
SOURCE: {source.name}

PAGE CONTENT (truncated):
{text[:5000]}

Extract measurements as JSON array:
[
    {{"quantity": "<name>", "value": <number>, "uncertainty": <number or null>, "unit": "<unit>", "context": "<where found>"}},
    ...
]

JSON:"""

                response = self._call_legomena(prompt, timeout=120)
                if response:
                    try:
                        json_match = re.search(r'\[[\s\S]*\]', response)
                        if json_match:
                            data = json.loads(json_match.group())
                            for m in data:
                                measurements.append(Measurement(
                                    quantity=m.get("quantity", "unknown"),
                                    value=float(m.get("value", 0)),
                                    uncertainty=m.get("uncertainty"),
                                    unit=m.get("unit", ""),
                                    source=source.name,
                                    source_url=source.url,
                                    quality=source.quality,
                                    context=m.get("context", "")
                                ))
                    except (json.JSONDecodeError, ValueError):
                        pass
        except Exception as e:
            print(f"Web fetch error: {e}")

        return measurements

    def _extract_measurements_from_json(self, data: Any, source: DataSource,
                                        quantities: List[str]) -> List[Measurement]:
        """Extract measurements from JSON data."""
        measurements = []

        def extract_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        # Check if key matches any quantity
                        key_lower = key.lower()
                        for q in quantities:
                            if q.lower() in key_lower or key_lower in q.lower():
                                measurements.append(Measurement(
                                    quantity=q,
                                    value=float(value),
                                    uncertainty=None,
                                    unit="",
                                    source=source.name,
                                    source_url=source.url,
                                    quality=source.quality,
                                    context=new_path
                                ))
                    elif isinstance(value, (dict, list)):
                        extract_recursive(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj[:100]):  # Limit iterations
                    extract_recursive(item, f"{path}[{i}]")

        extract_recursive(data)
        return measurements

    def full_discovery(self, research_topic: str) -> Tuple[DomainProfile, List[DataSource], List[Measurement]]:
        """
        Complete discovery pipeline for a research topic.

        1. Identify domain
        2. Discover quantities
        3. Find data sources
        4. Fetch measurements

        Returns everything needed for hypothesis testing.
        """
        print(f"\n{'='*60}")
        print(f"UNIVERSAL DATA DISCOVERY")
        print(f"Topic: {research_topic}")
        print(f"{'='*60}\n")

        # Step 1: Identify domain
        print("Step 1: Identifying domain...")
        domain = self.discover_domain(research_topic)
        print(f"  Domain: {domain.name}/{domain.subdomain}")
        print(f"  Z² relevance: {domain.z2_relevance}")

        # Step 2: Discover quantities
        print("\nStep 2: Discovering measurable quantities...")
        quantities = self.discover_quantities(research_topic, domain)
        domain.key_quantities = quantities
        print(f"  Found {len(quantities)} quantities:")
        for q in quantities[:5]:
            print(f"    - {q.name}: {q.description}")

        # Step 3: Find data sources
        print("\nStep 3: Finding authoritative data sources...")
        sources = self.discover_data_sources(domain)
        print(f"  Found {len(sources)} sources:")
        for s in sources[:5]:
            print(f"    - {s.name} ({s.quality.value})")

        # Step 4: Fetch measurements
        print("\nStep 4: Fetching measurements...")
        all_measurements = []
        quantity_names = [q.name for q in quantities]

        for source in sources[:3]:  # Top 3 sources
            print(f"  Fetching from {source.name}...")
            measurements = self.fetch_measurements(source, quantity_names)
            all_measurements.extend(measurements)
            print(f"    Got {len(measurements)} measurements")

        print(f"\nTotal measurements: {len(all_measurements)}")

        return domain, sources, all_measurements


class StructuredHypothesisGenerator:
    """
    Generate structured, testable hypotheses for ANY domain.

    Not abstract "resonance" - specific quantity + formula + data source.
    """

    HYPOTHESIS_TEMPLATE = """You are a Z² theoretical physicist. Generate a SPECIFIC, TESTABLE hypothesis.

DOMAIN: {domain}
SUBDOMAIN: {subdomain}
Z² RELEVANCE: {z2_relevance}

AVAILABLE QUANTITIES:
{quantities}

PRIOR VALIDATED FINDINGS:
{validated}

PRIOR FALSIFIED FINDINGS:
{falsified}

Z² CONSTANTS:
- Z² = 32π/3 = {z2:.6f}
- Z = √(Z²) = {z:.6f}
- φ = (1+√5)/2 = {phi:.6f}
- 1/Z = {inv_z:.6f}
- 1/φ = {inv_phi:.6f}

Generate ONE hypothesis in this EXACT format:

QUANTITY: <exact physical quantity or ratio, e.g., "eye_diameter / radius_of_maximum_wind">
Z² FORMULA: <mathematical expression using Z², Z, φ, integers, e.g., "1/φ" or "4*Z² + 3">
PREDICTED VALUE: <numerical value, e.g., "0.618034">
UNCERTAINTY: <expected error range, e.g., "± 0.02">
DERIVATION:
1. <step 1 from Z² first principles>
2. <step 2>
3. <step 3>
DATA SOURCE: <specific authoritative source, NOT Wikipedia>
SAMPLE SIZE: <minimum N for statistical significance, e.g., "N > 100">
FALSIFICATION: <specific condition that would disprove this, e.g., "If mean ratio > 0.70 at 3σ">

DO NOT:
- Generate vague hypotheses like "geometric resonance"
- Use Wikipedia as a data source
- Repeat already-falsified predictions
- Generate predictions without specific numerical values

Hypothesis:"""

    def __init__(self, knowledge_graph=None):
        self.knowledge_graph = knowledge_graph

    def generate(self, domain: DomainProfile,
                 validated: List[Dict] = None,
                 falsified: List[Dict] = None,
                 llm: str = None) -> Dict:
        """Generate a structured hypothesis."""

        llm = llm or LEGOMENA_MODEL
        validated = validated or []
        falsified = falsified or []

        # Format quantities
        quantities_str = "\n".join([
            f"- {q.name}: {q.description} ({q.unit})"
            for q in domain.key_quantities
        ])

        # Format prior findings
        validated_str = "\n".join([
            f"- {v.get('quantity', 'unknown')}: {v.get('formula', '?')} = {v.get('value', '?')} (validated)"
            for v in validated
        ]) or "None yet"

        falsified_str = "\n".join([
            f"- {f.get('quantity', 'unknown')}: {f.get('formula', '?')} (falsified, error: {f.get('error', '?')})"
            for f in falsified
        ]) or "None yet"

        prompt = self.HYPOTHESIS_TEMPLATE.format(
            domain=domain.name,
            subdomain=domain.subdomain,
            z2_relevance=domain.z2_relevance,
            quantities=quantities_str,
            validated=validated_str,
            falsified=falsified_str,
            z2=Z2,
            z=Z,
            phi=PHI,
            inv_z=1/Z,
            inv_phi=1/PHI
        )

        # Call LLM
        try:
            result = subprocess.run(
                ["ollama", "run", llm],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=LEGOMENA_TIMEOUT
            )
            if result.returncode == 0:
                return self._parse_hypothesis(result.stdout.strip())
        except Exception as e:
            print(f"Hypothesis generation error: {e}")

        return {}

    def _parse_hypothesis(self, response: str) -> Dict:
        """Parse structured hypothesis from LLM response."""
        hypothesis = {}

        patterns = {
            "quantity": r"QUANTITY:\s*(.+)",
            "formula": r"Z² FORMULA:\s*(.+)",
            "predicted_value": r"PREDICTED VALUE:\s*([\d.]+)",
            "uncertainty": r"UNCERTAINTY:\s*(.+)",
            "data_source": r"DATA SOURCE:\s*(.+)",
            "sample_size": r"SAMPLE SIZE:\s*(.+)",
            "falsification": r"FALSIFICATION:\s*(.+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                hypothesis[key] = match.group(1).strip()

        # Extract derivation steps
        derivation_match = re.search(r"DERIVATION:\s*((?:\d+\..+\n?)+)", response, re.IGNORECASE)
        if derivation_match:
            steps = re.findall(r"\d+\.\s*(.+)", derivation_match.group(1))
            hypothesis["derivation"] = steps

        return hypothesis


def main():
    """Test the universal data discovery engine."""
    print("="*70)
    print("UNIVERSAL DATA DISCOVERY ENGINE TEST")
    print("="*70)

    discovery = UniversalDataDiscovery(use_legomena=True, use_web_search=True)

    # Test with different topics
    topics = [
        "hurricane intensity prediction",
        "quark mass ratios",
        "dark energy density",
    ]

    for topic in topics[:1]:  # Test first topic
        domain, sources, measurements = discovery.full_discovery(topic)

        print(f"\n{'='*60}")
        print(f"RESULTS FOR: {topic}")
        print(f"{'='*60}")
        print(f"Domain: {domain.name}/{domain.subdomain}")
        print(f"Quantities: {len(domain.key_quantities)}")
        print(f"Sources: {len(sources)}")
        print(f"Measurements: {len(measurements)}")

        # Generate hypothesis
        print("\nGenerating structured hypothesis...")
        generator = StructuredHypothesisGenerator()
        hypothesis = generator.generate(domain)
        print(f"Hypothesis: {json.dumps(hypothesis, indent=2)}")


if __name__ == "__main__":
    main()
