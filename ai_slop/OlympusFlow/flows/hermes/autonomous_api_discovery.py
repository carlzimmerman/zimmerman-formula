#!/usr/bin/env python3
"""
AUTONOMOUS API DISCOVERY - Self-Learning Data Source Discovery
===============================================================

This is the key missing piece for true autonomous research.

When HermesFlow encounters an unknown domain with no pre-configured APIs,
this module:
1. Searches the web for scientific databases in that domain
2. Uses Legomena to analyze each database and discover its API/data format
3. Auto-generates APIConfig objects
4. Tests the discovered APIs to verify they work
5. Persists working configurations to HeliconLake for future use

This creates a SELF-EXPANDING knowledge base of data sources.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import re
import json
import time
import requests
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import pandas as pd

# Import from sibling modules
try:
    from .database_query_handler import DatabaseQueryHandler, APIConfig, QueryResult
except ImportError:
    from database_query_handler import DatabaseQueryHandler, APIConfig, QueryResult

# HeliconLake from new location
try:
    from OlympusFlow.lakes.helicon import HeliconLake, SourceEntry
except ImportError:
    HeliconLake = None
    SourceEntry = None

# Legomena config
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "300"))


@dataclass
class DiscoveredDatabase:
    """A database discovered through web search."""
    url: str
    name: str
    description: str
    domain: str
    topics: List[str]
    discovery_method: str  # web_search, citation, known_source
    confidence: float  # 0-1 confidence it's a real data source
    page_content_preview: str = ""


@dataclass
class DiscoveredAPI:
    """An API discovered through Legomena analysis."""
    database: DiscoveredDatabase
    api_type: str  # rest_api, direct_download, form_submit, graphql
    endpoint_url: str
    method: str  # GET, POST
    parameters: Dict[str, Any]
    response_format: str  # json, csv, xml, html_table, fixed_width
    auth_required: bool
    rate_limit_hint: float  # seconds between requests
    sample_query: str  # Example query to test
    analysis_notes: str  # Legomena's reasoning


@dataclass
class DiscoveryResult:
    """Result of autonomous API discovery."""
    domain: str
    topic: str
    databases_found: int
    apis_discovered: int
    apis_working: int
    working_configs: List[APIConfig]
    failed_attempts: List[Dict]
    discovery_time_seconds: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AutonomousAPIDiscovery:
    """
    Self-learning API discovery system.

    This is what makes HermesFlow truly autonomous - the ability to
    discover new data sources without human configuration.
    """

    # Known authoritative database patterns by domain
    AUTHORITATIVE_PATTERNS = {
        "oceanography": ["NOAA", "NCEI", "Copernicus", "CMEMS", "ARGO", "WOD"],
        "hydrology": ["USGS", "GRDC", "UNESCO", "WMO"],
        "ecology": ["GBIF", "iNaturalist", "LTER", "DataONE"],
        "atmospheric": ["NOAA", "NASA", "ECMWF", "ERA5", "MERRA"],
        "paleoclimate": ["NOAA Paleo", "Pangaea", "NCEI", "LiPD"],
        "dendrochronology": ["ITRDB", "NCEI Paleo"],
        "glaciology": ["WGMS", "NSIDC", "GLIMS"],
        "epidemiology": ["WHO", "CDC", "ECDC", "Our World in Data"],
        "genomics": ["NCBI", "GenBank", "UniProt", "Ensembl"],
        "astronomy": ["NASA", "ESA", "MAST", "NED", "Vizier"],
    }

    # Search query templates
    SEARCH_TEMPLATES = [
        "{domain} {topic} database API",
        "{domain} {topic} data download CSV",
        "{domain} {topic} REST API endpoint",
        "{domain} open data repository",
        "{topic} scientific database",
        "{domain} {topic} data portal",
    ]

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HermesFlow/2.0 (Autonomous Research; Z2 Framework)'
        })

        # Initialize components
        self.db_handler = DatabaseQueryHandler(verbose=False)
        self.helicon_lake = HeliconLake() if HeliconLake else None

        # Track discovery attempts
        self.discovery_log = []

    def _log(self, msg: str):
        """Log message if verbose."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[AutoDiscovery {timestamp}] {msg}")

    def _call_legomena(self, prompt: str, timeout: int = None) -> Optional[str]:
        """Call Legomena for intelligent analysis."""
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
            self._log(f"Legomena timeout ({timeout}s)")
        except FileNotFoundError:
            self._log("Legomena (ollama) not available")
        except Exception as e:
            self._log(f"Legomena error: {e}")
        return None

    # Known authoritative data portals by domain
    KNOWN_DATA_PORTALS = {
        "oceanography": [
            {"url": "https://coastwatch.pfeg.noaa.gov/erddap/index.html", "name": "NOAA CoastWatch ERDDAP", "desc": "Ocean data including SST"},
            {"url": "https://www.ncei.noaa.gov/products/world-ocean-database", "name": "World Ocean Database", "desc": "NCEI ocean profiles"},
            {"url": "https://resources.marine.copernicus.eu/products", "name": "Copernicus Marine", "desc": "EU ocean data service"},
        ],
        "dendrochronology": [
            {"url": "https://www.ncei.noaa.gov/products/paleoclimatology/tree-ring", "name": "NCEI Tree Ring Data", "desc": "International Tree-Ring Data Bank"},
        ],
        "hydrology": [
            {"url": "https://waterdata.usgs.gov/nwis", "name": "USGS Water Data", "desc": "National Water Information System"},
            {"url": "https://www.bafg.de/GRDC/EN/Home/homepage_node.html", "name": "GRDC", "desc": "Global Runoff Data Centre"},
        ],
        "paleoclimate": [
            {"url": "https://www.ncei.noaa.gov/products/paleoclimatology", "name": "NCEI Paleoclimatology", "desc": "Paleo data archives"},
        ],
        "ecology": [
            {"url": "https://www.gbif.org/developer/summary", "name": "GBIF API", "desc": "Global Biodiversity Information"},
        ],
    }

    def _web_search(self, query: str) -> List[Dict]:
        """Search the web for databases using DuckDuckGo."""
        results = []

        try:
            # DuckDuckGo instant answers API
            response = self.session.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1},
                timeout=10
            )
            if response.ok and response.text.strip():
                data = response.json()

                # Main result
                if data.get("AbstractURL"):
                    results.append({
                        "title": data.get("Heading", ""),
                        "url": data.get("AbstractURL"),
                        "snippet": data.get("AbstractText", ""),
                        "source": "duckduckgo_abstract"
                    })

                # Related topics
                for topic in data.get("RelatedTopics", [])[:10]:
                    if isinstance(topic, dict) and topic.get("FirstURL"):
                        results.append({
                            "title": topic.get("Text", "")[:100],
                            "url": topic.get("FirstURL"),
                            "snippet": topic.get("Text", ""),
                            "source": "duckduckgo_related"
                        })

        except Exception as e:
            self._log(f"Web search error: {e}")

        return results

    def _get_known_portals(self, domain: str) -> List[Dict]:
        """Get known data portals for a domain as fallback."""
        portals = self.KNOWN_DATA_PORTALS.get(domain.lower(), [])
        return [
            {
                "title": p["name"],
                "url": p["url"],
                "snippet": p["desc"],
                "source": "known_portal"
            }
            for p in portals
        ]

    def _fetch_page_content(self, url: str, max_chars: int = 10000) -> str:
        """Fetch and extract text content from a page."""
        try:
            response = self.session.get(url, timeout=30)
            if response.ok:
                content = response.text[:max_chars]
                # Basic HTML tag removal for analysis
                content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
                content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
                content = re.sub(r'<[^>]+>', ' ', content)
                content = re.sub(r'\s+', ' ', content)
                return content.strip()
        except Exception as e:
            self._log(f"Fetch error for {url}: {e}")
        return ""

    def search_for_databases(self, domain: str, topic: str = "") -> List[DiscoveredDatabase]:
        """
        Search the web for scientific databases in a domain.

        Uses multiple search strategies:
        1. Direct search queries
        2. Known authoritative patterns
        3. Domain-specific repositories
        """
        self._log(f"Searching for databases: domain={domain}, topic={topic}")
        databases = []
        seen_urls = set()

        # Strategy 1: Web search with multiple query templates
        for template in self.SEARCH_TEMPLATES[:4]:  # Limit to avoid rate limiting
            query = template.format(domain=domain, topic=topic or domain)
            self._log(f"  Searching: {query}")

            results = self._web_search(query)
            time.sleep(1)  # Rate limit

            for r in results:
                url = r.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)

                    # Evaluate if this looks like a data source
                    confidence = self._evaluate_data_source_confidence(
                        url, r.get("title", ""), r.get("snippet", ""), domain
                    )

                    if confidence > 0.3:  # Minimum threshold
                        databases.append(DiscoveredDatabase(
                            url=url,
                            name=r.get("title", url)[:100],
                            description=r.get("snippet", "")[:300],
                            domain=domain,
                            topics=[topic] if topic else [],
                            discovery_method="web_search",
                            confidence=confidence
                        ))

        # Strategy 2: Check known authoritative patterns
        if domain.lower() in self.AUTHORITATIVE_PATTERNS:
            patterns = self.AUTHORITATIVE_PATTERNS[domain.lower()]
            for pattern in patterns[:3]:  # Top 3 authorities
                query = f"{pattern} {topic or domain} data API"
                results = self._web_search(query)
                time.sleep(1)

                for r in results:
                    url = r.get("url", "")
                    if url and url not in seen_urls and pattern.lower() in url.lower():
                        seen_urls.add(url)
                        databases.append(DiscoveredDatabase(
                            url=url,
                            name=f"{pattern} - {r.get('title', '')[:80]}",
                            description=r.get("snippet", "")[:300],
                            domain=domain,
                            topics=[topic] if topic else [],
                            discovery_method="authoritative_pattern",
                            confidence=0.8  # High confidence for known authorities
                        ))

        # Strategy 3: Use known data portals as fallback
        if len(databases) < 3:
            known_portals = self._get_known_portals(domain)
            for portal in known_portals:
                url = portal.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    databases.append(DiscoveredDatabase(
                        url=url,
                        name=portal.get("title", url),
                        description=portal.get("snippet", ""),
                        domain=domain,
                        topics=[topic] if topic else [],
                        discovery_method="known_portal",
                        confidence=0.85  # High confidence for known portals
                    ))
            if known_portals:
                self._log(f"  Added {len(known_portals)} known portals for {domain}")

        # Sort by confidence
        databases.sort(key=lambda x: x.confidence, reverse=True)

        self._log(f"  Found {len(databases)} potential databases")
        return databases[:10]  # Return top 10

    def _evaluate_data_source_confidence(self, url: str, title: str,
                                          snippet: str, domain: str) -> float:
        """Evaluate confidence that a URL is a real scientific data source."""
        score = 0.0
        text = f"{url} {title} {snippet}".lower()

        # Positive signals
        if ".gov" in url:
            score += 0.3
        if ".edu" in url:
            score += 0.2
        if ".org" in url and any(p in url.lower() for p in ["noaa", "nasa", "usgs", "esa"]):
            score += 0.3

        # Data-related keywords
        data_keywords = ["database", "data", "api", "download", "csv", "json",
                        "repository", "catalog", "archive", "dataset"]
        score += 0.05 * sum(1 for kw in data_keywords if kw in text)

        # Domain relevance
        if domain.lower() in text:
            score += 0.1

        # Negative signals
        if "wikipedia" in url:
            score -= 0.3
        if "amazon" in url or "shop" in text:
            score -= 0.5
        if "news" in url or "blog" in url:
            score -= 0.2

        return max(0.0, min(1.0, score))

    def analyze_database_for_api(self, database: DiscoveredDatabase) -> Optional[DiscoveredAPI]:
        """
        Use Legomena to analyze a database and discover its API.

        This is the CORE of autonomous discovery - using LLM to understand
        how to programmatically access a data source.
        """
        self._log(f"Analyzing: {database.url}")

        # Fetch page content
        page_content = self._fetch_page_content(database.url)
        if not page_content:
            return None

        database.page_content_preview = page_content[:2000]

        # Construct Legomena prompt
        prompt = f"""You are an expert at discovering APIs and data access methods for scientific databases.

TASK: Analyze this webpage and determine how to programmatically download data.

DATABASE URL: {database.url}
DOMAIN: {database.domain}
DESCRIPTION: {database.description}

PAGE CONTENT (truncated):
{page_content[:4000]}

ANALYSIS REQUIRED:
1. Is there a REST API? Look for:
   - API documentation links
   - Endpoint URLs (containing /api/, /v1/, /query, /search)
   - JSON/XML response mentions

2. Is there a direct data file download? Look for:
   - Links ending in .csv, .json, .txt, .zip, .nc
   - "Download" buttons or links
   - FTP links

3. Is there a form-based query? Look for:
   - HTML forms with action URLs
   - Search/filter interfaces
   - Parameter-based URLs

4. What authentication is required?
   - API keys mentioned?
   - Login required?
   - Rate limits mentioned?

RESPOND WITH JSON ONLY:
{{
    "has_api": true/false,
    "api_type": "rest_api" | "direct_download" | "form_submit" | "graphql" | "none",
    "endpoint_url": "<full URL of API endpoint or download link>",
    "method": "GET" | "POST",
    "parameters": {{"param1": "value1", "param2": "value2"}},
    "response_format": "json" | "csv" | "xml" | "html_table" | "fixed_width" | "binary",
    "auth_required": true/false,
    "rate_limit_seconds": <number>,
    "sample_query": "<example URL or curl command to test>",
    "confidence": <0.0 to 1.0>,
    "reasoning": "<brief explanation of how you determined this>"
}}

If you cannot determine how to access the data, return:
{{"has_api": false, "api_type": "none", "reasoning": "<why access is not possible>"}}

JSON:"""

        response = self._call_legomena(prompt)

        if not response:
            self._log("  Legomena analysis failed")
            return None

        # Parse response
        try:
            # Extract JSON from response - clean control characters first
            cleaned_response = response.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            # Remove any other control characters
            cleaned_response = ''.join(c if ord(c) >= 32 or c in '\n\r\t' else ' ' for c in cleaned_response)

            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned_response)
            if json_match:
                json_str = json_match.group()
                # Fix common JSON issues
                json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
                json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays

                data = json.loads(json_str)

                if not data.get("has_api") or data.get("api_type") == "none":
                    self._log(f"  No API found: {data.get('reasoning', 'unknown')[:100]}")
                    return None

                return DiscoveredAPI(
                    database=database,
                    api_type=data.get("api_type", "unknown"),
                    endpoint_url=data.get("endpoint_url", ""),
                    method=data.get("method", "GET"),
                    parameters=data.get("parameters", {}),
                    response_format=data.get("response_format", "json"),
                    auth_required=data.get("auth_required", False),
                    rate_limit_hint=data.get("rate_limit_seconds", 1.0),
                    sample_query=data.get("sample_query", ""),
                    analysis_notes=data.get("reasoning", "")[:200] if data.get("reasoning") else ""
                )
            else:
                self._log(f"  No JSON found in response")

        except json.JSONDecodeError as e:
            self._log(f"  JSON parse error: {e}")
            # Try to extract key info without full JSON
            if "has_api" in response.lower() and "false" in response.lower():
                self._log(f"  Detected no API in response")

        return None

    def test_discovered_api(self, api: DiscoveredAPI) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Test a discovered API to verify it actually works.

        Returns:
            (success, data_frame, error_message)
        """
        self._log(f"Testing API: {api.endpoint_url}")

        if not api.endpoint_url:
            return False, None, "No endpoint URL"

        try:
            # Respect rate limit hint
            time.sleep(api.rate_limit_hint)

            # Make request
            if api.method.upper() == "GET":
                response = self.session.get(
                    api.endpoint_url,
                    params=api.parameters if api.parameters else None,
                    timeout=60
                )
            else:
                response = self.session.post(
                    api.endpoint_url,
                    data=api.parameters,
                    timeout=60
                )

            if not response.ok:
                return False, None, f"HTTP {response.status_code}"

            # Parse response based on format
            df = self._parse_response(response, api.response_format)

            if df is not None and len(df) > 0:
                self._log(f"  SUCCESS: {len(df)} rows, {len(df.columns)} columns")
                return True, df, ""
            else:
                return False, None, "Response parsed but no data"

        except requests.exceptions.Timeout:
            return False, None, "Timeout"
        except Exception as e:
            return False, None, str(e)

    def _parse_response(self, response: requests.Response,
                        format_type: str) -> Optional[pd.DataFrame]:
        """Parse API response into DataFrame."""
        import io

        try:
            if format_type == "json":
                data = response.json()
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    for key in ['data', 'results', 'records', 'items', 'features']:
                        if key in data and isinstance(data[key], list):
                            return pd.DataFrame(data[key])
                    return pd.DataFrame([data])

            elif format_type == "csv":
                return pd.read_csv(io.StringIO(response.text))

            elif format_type == "xml":
                # Basic XML to DataFrame
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                records = []
                for child in root:
                    record = {subchild.tag: subchild.text for subchild in child}
                    if record:
                        records.append(record)
                return pd.DataFrame(records) if records else None

            elif format_type == "html_table":
                tables = pd.read_html(io.StringIO(response.text))
                return tables[0] if tables else None

            elif format_type == "fixed_width":
                lines = response.text.strip().split('\n')
                data_lines = [l for l in lines if l.strip() and not l.startswith('#')]
                if data_lines:
                    rows = [line.split() for line in data_lines]
                    return pd.DataFrame(rows)

        except Exception as e:
            self._log(f"  Parse error: {e}")

        return None

    def create_api_config(self, api: DiscoveredAPI) -> APIConfig:
        """Convert a discovered API into a reusable APIConfig."""
        return APIConfig(
            name=f"AUTO: {api.database.name[:50]}",
            base_url=api.endpoint_url,
            method=api.method,
            default_params=api.parameters,
            response_format=api.response_format,
            rate_limit_seconds=max(1.0, api.rate_limit_hint),
            description=f"Auto-discovered: {api.database.description[:100]}",
            domains=[api.database.domain],
            topics=api.database.topics,
            quantities=[]  # Will be populated after data analysis
        )

    def persist_discovered_api(self, config: APIConfig,
                                sample_data: pd.DataFrame) -> bool:
        """
        Persist a working API configuration to HeliconLake.

        This is what makes the system LEARN - discovered APIs are saved
        for future use.
        """
        if not self.helicon_lake:
            self._log("HeliconLake not available for persistence")
            return False

        try:
            # Infer quantities from column names
            quantities = list(sample_data.columns)[:10]  # Top 10 columns

            source_entry = {
                'url': config.base_url,
                'description': config.description,
                'domains': config.domains,
                'topics': config.topics,
                'quantities': quantities,
                'format': config.response_format,
                'organization': config.name.replace("AUTO: ", ""),
                'authority_score': 0.6,  # Medium confidence for auto-discovered
                'discovered_by': 'AutonomousAPIDiscovery',
                'discovery_method': 'legomena_analysis',
                'notes': f"Auto-discovered. Sample: {len(sample_data)} rows."
            }

            self.helicon_lake.register_source(source_entry)
            self._log(f"Persisted to HeliconLake: {config.base_url}")
            return True

        except Exception as e:
            self._log(f"Persistence error: {e}")
            return False

    def discover(self, domain: str, topic: str = "") -> DiscoveryResult:
        """
        Main entry point: Autonomously discover APIs for a domain.

        This is the FULL PIPELINE:
        1. Search for databases
        2. Analyze each with Legomena
        3. Test discovered APIs
        4. Persist working ones
        5. Return usable configs
        """
        start_time = time.time()
        self._log(f"Starting autonomous discovery: {domain}/{topic}")

        result = DiscoveryResult(
            domain=domain,
            topic=topic,
            databases_found=0,
            apis_discovered=0,
            apis_working=0,
            working_configs=[],
            failed_attempts=[],
            discovery_time_seconds=0
        )

        # Step 1: Search for databases
        databases = self.search_for_databases(domain, topic)
        result.databases_found = len(databases)

        if not databases:
            self._log("No databases found")
            result.discovery_time_seconds = time.time() - start_time
            return result

        # Step 2: Analyze each database
        for db in databases[:5]:  # Limit to top 5 to avoid taking too long
            self._log(f"Analyzing database: {db.name}")

            api = self.analyze_database_for_api(db)

            if api:
                result.apis_discovered += 1

                # Step 3: Test the API
                success, df, error = self.test_discovered_api(api)

                if success and df is not None:
                    result.apis_working += 1

                    # Step 4: Create config and persist
                    config = self.create_api_config(api)
                    result.working_configs.append(config)

                    # Add to current handler for immediate use
                    self.db_handler.known_apis[f"auto_{len(result.working_configs)}"] = config

                    # Persist to HeliconLake
                    self.persist_discovered_api(config, df)

                    self._log(f"  Working API found: {config.base_url}")
                else:
                    result.failed_attempts.append({
                        "database": db.name,
                        "api_endpoint": api.endpoint_url if api else "",
                        "error": error
                    })
            else:
                result.failed_attempts.append({
                    "database": db.name,
                    "error": "Legomena could not discover API"
                })

        result.discovery_time_seconds = time.time() - start_time

        self._log(f"Discovery complete: {result.apis_working}/{result.apis_discovered} APIs working")
        return result


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def discover_apis(domain: str, topic: str = "") -> DiscoveryResult:
    """Convenience function for autonomous API discovery."""
    discoverer = AutonomousAPIDiscovery(verbose=True)
    return discoverer.discover(domain, topic)


def discover_and_query(domain: str, topic: str = "") -> List[QueryResult]:
    """Discover APIs and immediately query them."""
    discoverer = AutonomousAPIDiscovery(verbose=True)
    result = discoverer.discover(domain, topic)

    query_results = []
    for config in result.working_configs:
        qr = discoverer.db_handler.query_config(config)
        if qr.success:
            query_results.append(qr)

    return query_results


# =============================================================================
# CLI TEST
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("AUTONOMOUS API DISCOVERY - Test")
    print("=" * 70)

    # Test with a domain that has NO pre-configured APIs
    test_domain = sys.argv[1] if len(sys.argv) > 1 else "oceanography"
    test_topic = sys.argv[2] if len(sys.argv) > 2 else "sea_surface_temperature"

    print(f"\nTest domain: {test_domain}")
    print(f"Test topic: {test_topic}")
    print()

    result = discover_apis(test_domain, test_topic)

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Databases found: {result.databases_found}")
    print(f"APIs discovered: {result.apis_discovered}")
    print(f"APIs working: {result.apis_working}")
    print(f"Time: {result.discovery_time_seconds:.1f}s")

    if result.working_configs:
        print("\nWorking APIs:")
        for config in result.working_configs:
            print(f"  - {config.name}")
            print(f"    URL: {config.base_url}")
            print(f"    Format: {config.response_format}")

    if result.failed_attempts:
        print("\nFailed attempts:")
        for fa in result.failed_attempts[:5]:
            print(f"  - {fa['database']}: {fa['error']}")
