#!/usr/bin/env python3
"""
HERMES EXPLORER AGENT
=====================

An intelligent agent that EXPLORES the web to find scientific data.
Uses Legomena for reasoning, tools for action.

The agent:
1. Reasons about where data might be
2. Searches for data portals (not direct files)
3. Navigates portals intelligently
4. Downloads and validates data

Tools available:
- search: Web search
- fetch: Get page content
- extract_links: Find links on page
- ask: Reason about next steps
- download: Get data file

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import re
import json
import subprocess
import requests
import pandas as pd
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-4b")

# Version with enhanced data acquisition
__version__ = "1.6.0"


@dataclass
class ExplorationStep:
    """Record of one exploration step."""
    action: str
    input: str
    result: str
    reasoning: str


@dataclass
class DataDiscovery:
    """Result of data exploration."""
    success: bool
    url: str
    data: Optional[pd.DataFrame]
    steps: List[ExplorationStep]
    description: str


class HermesExplorer:
    """
    Intelligent agent that explores the web to find data.

    Uses reasoning (Legomena) + tools (fetch, search, etc.)
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "HermesExplorer/1.0 (Scientific Research)"})
        self.steps: List[ExplorationStep] = []
        self.visited = set()
        self.max_steps = 15

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Hermes {ts}] {msg}")

    def _record(self, action: str, input: str, result: str, reasoning: str = ""):
        self.steps.append(ExplorationStep(action, input, result, reasoning))

    # =========================================================================
    # TOOLS
    # =========================================================================

    def tool_search(self, query: str) -> List[Dict]:
        """Search the web."""
        self._log(f"SEARCH: {query}")

        results = []
        try:
            response = self.session.post(
                "https://html.duckduckgo.com/html/",
                data={"q": query},
                timeout=20
            )

            if response.ok:
                pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
                for url, title in re.findall(pattern, response.text)[:8]:
                    if "uddg=" in url:
                        match = re.search(r'uddg=([^&]+)', url)
                        if match:
                            url = requests.utils.unquote(match.group(1))
                    results.append({"url": url, "title": title.strip()})

            self._record("search", query, f"Found {len(results)} results", "")
        except Exception as e:
            self._record("search", query, f"Error: {e}", "")

        return results

    def tool_fetch(self, url: str) -> Optional[str]:
        """Fetch page content."""
        if url in self.visited:
            return None

        self._log(f"FETCH: {url[:60]}...")
        self.visited.add(url)

        try:
            response = self.session.get(url, timeout=30)
            if response.ok:
                self._record("fetch", url, f"Got {len(response.content)/1024:.1f}KB", "")
                return response.text
        except Exception as e:
            self._record("fetch", url, f"Error: {e}", "")

        return None

    def tool_extract_links(self, html: str, base_url: str,
                          filter_terms: List[str] = None) -> List[Dict]:
        """Extract links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()[:80]
            full_url = urljoin(base_url, href)

            # Apply filter
            if filter_terms:
                matches = any(t.lower() in href.lower() or t.lower() in text.lower()
                            for t in filter_terms)
                if not matches:
                    continue

            # Enhanced data detection (v1.6.0)
            data_extensions = ['.csv', '.txt', '.json', '.nc', '.dat', '.asc', '.data', '.ascii']
            data_keywords = ['download', 'export', 'data.']
            is_data = (
                any(ext in href.lower() for ext in data_extensions) or
                any(kw in href.lower() for kw in data_keywords)
            )
            links.append({
                "url": full_url,
                "text": text,
                "is_data": is_data
            })

        return links

    def tool_download(self, url: str) -> Optional[bytes]:
        """Download file content."""
        self._log(f"DOWNLOAD: {url.split('/')[-1]}")

        try:
            response = self.session.get(url, timeout=300)
            if response.ok:
                # Verify it's not HTML
                content = response.content
                if b'<html' not in content[:500].lower():
                    self._record("download", url, f"Got {len(content)/1024:.1f}KB data", "")
                    return content
                else:
                    self._record("download", url, "Got HTML, not data", "")
        except Exception as e:
            self._record("download", url, f"Error: {e}", "")

        return None

    def tool_parse(self, content: bytes, content_type: str = None) -> Optional[pd.DataFrame]:
        """
        Parse data content with multi-format support (v1.6.0).

        Supports:
        - CSV files
        - ASCII fixed-width tables (NOAA style)
        - JSON data arrays
        - HTML embedded tables
        """
        text_content = None
        try:
            text_content = content.decode('utf-8', errors='ignore')
        except:
            pass

        # Detect if this looks like whitespace-delimited data (NOAA style)
        # Check for multiple whitespace-separated numbers
        if text_content:
            first_lines = text_content.strip().split('\n')[:5]
            looks_like_ascii = False
            for line in first_lines:
                parts = line.split()
                if len(parts) > 3:
                    # Check if most parts are numbers
                    numeric_parts = sum(1 for p in parts if self._is_numeric(p))
                    if numeric_parts >= len(parts) * 0.7:
                        looks_like_ascii = True
                        break

            if looks_like_ascii:
                df = self._parse_ascii_table(text_content)
                if df is not None and len(df) > 10:
                    self._log(f"  Parsed ASCII table: {len(df)} rows, {len(df.columns)} cols")
                    return df

        # Try standard CSV
        try:
            df = pd.read_csv(io.BytesIO(content), low_memory=False)
            if len(df) > 30 and len(df.columns) >= 2:
                self._log(f"  Parsed CSV: {len(df)} rows, {len(df.columns)} cols")
                return df
        except:
            pass

        try:
            df = pd.read_csv(io.BytesIO(content), skiprows=[1], low_memory=False, na_values=[' ', ''])
            if len(df) > 30 and len(df.columns) >= 2:
                self._log(f"  Parsed CSV (skip header): {len(df)} rows, {len(df.columns)} cols")
                return df
        except:
            pass

        # Try JSON
        if text_content:
            df = self._parse_json_data(text_content)
            if df is not None and len(df) > 10:
                self._log(f"  Parsed JSON: {len(df)} rows, {len(df.columns)} cols")
                return df

        # Try HTML tables
        if text_content and '<table' in text_content.lower():
            df = self._parse_html_tables(text_content)
            if df is not None and len(df) > 10:
                self._log(f"  Parsed HTML table: {len(df)} rows, {len(df.columns)} cols")
                return df

        return None

    def _is_numeric(self, s: str) -> bool:
        """Check if string is a number."""
        try:
            float(s)
            return True
        except:
            return False

    # =========================================================================
    # ENHANCED DATA ACQUISITION (v1.6.0)
    # =========================================================================

    def _parse_ascii_table(self, text: str) -> Optional[pd.DataFrame]:
        """
        Parse ASCII fixed-width tables like NOAA data.

        Handles multiple formats:
        - NOAA MEI: YEAR followed by 12 monthly values
        - NOAA SOI: Similar format
        - General fixed-width scientific data
        """
        lines = text.strip().split('\n')

        # Skip comment lines and find data start
        data_lines = []
        header_line = None
        skip_first_data = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip empty lines and common comment patterns
            if not stripped or stripped.startswith('#') or stripped.startswith('//'):
                continue
            # Skip lines that are mostly dashes or equals (separators)
            if len(stripped) > 5 and stripped.count('-') / len(stripped) > 0.5:
                continue
            if len(stripped) > 5 and stripped.count('=') / len(stripped) > 0.5:
                continue

            # Detect NOAA year-range header (e.g., "1979     2026")
            parts = stripped.split()
            if len(parts) == 2 and all(p.isdigit() and len(p) == 4 for p in parts):
                # This is a year range header, skip it
                skip_first_data = True
                continue

            # First non-comment line might be header
            if header_line is None:
                # Check if it looks like a header (contains letters, not just numbers)
                alpha_count = sum(1 for c in stripped if c.isalpha())
                digit_count = sum(1 for c in stripped if c.isdigit() or c in '.-')
                if alpha_count > digit_count:
                    header_line = stripped
                    continue

            data_lines.append(line)

        if len(data_lines) < 10:  # Lowered threshold
            return None

        # Try whitespace-delimited first (most common for NOAA)
        try:
            text_for_csv = '\n'.join(data_lines)
            df = pd.read_csv(io.StringIO(text_for_csv), sep=r'\s+', engine='python', header=None)

            if len(df) > 10 and len(df.columns) >= 2:
                # For NOAA monthly data: first column is year, rest are months
                if len(df.columns) == 13:
                    # NOAA monthly format: YEAR + 12 months
                    df.columns = ['YEAR', 'DJ', 'JF', 'FM', 'MA', 'AM', 'MJ',
                                  'JJ', 'JA', 'AS', 'SO', 'ON', 'ND']
                elif len(df.columns) == 12:
                    # Just 12 monthly values
                    df.columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                self._log(f"  Parsed whitespace-delimited: {len(df)} rows, {len(df.columns)} cols")
                return df
        except Exception as e:
            pass

        # Try to parse as fixed-width
        try:
            text_for_fwf = '\n'.join(data_lines)
            df = pd.read_fwf(io.StringIO(text_for_fwf), infer_nrows=100, header=None)

            # Clean up - drop columns that are all NaN
            df = df.dropna(axis=1, how='all')

            if len(df) > 10 and len(df.columns) >= 2:
                return df
        except Exception as e:
            pass

        return None

    def _parse_json_data(self, text: str) -> Optional[pd.DataFrame]:
        """Parse JSON data into DataFrame."""
        try:
            data = json.loads(text)

            # If it's a list of dicts, convert directly
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                return pd.DataFrame(data)

            # If it's a dict with a 'data' key
            if isinstance(data, dict):
                for key in ['data', 'values', 'records', 'results', 'items']:
                    if key in data and isinstance(data[key], list):
                        return pd.DataFrame(data[key])

            # If it's a dict of arrays (columnar format)
            if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
                return pd.DataFrame(data)

        except:
            pass

        return None

    def _parse_html_tables(self, html: str) -> Optional[pd.DataFrame]:
        """Extract data tables from HTML."""
        try:
            tables = pd.read_html(io.StringIO(html))

            # Find the largest table with numeric data
            best_table = None
            best_score = 0

            for table in tables:
                if len(table) < 10:
                    continue

                # Score by size and numeric content
                numeric_cols = table.select_dtypes(include=['number']).shape[1]
                score = len(table) * (numeric_cols + 1)

                if score > best_score:
                    best_score = score
                    best_table = table

            return best_table

        except:
            pass

        return None

    def _detect_api_endpoints(self, html: str, base_url: str) -> List[str]:
        """
        Detect API endpoints from HTML/JavaScript.

        Looks for patterns like:
        - /api/v1/data
        - data.json
        - fetch('...')
        """
        endpoints = []

        # API URL patterns
        patterns = [
            r'["\'](/api/[^"\']+)["\']',
            r'["\']([^"\']+\.json)["\']',
            r'["\']([^"\']+/data/[^"\']+)["\']',
            r'fetch\(["\']([^"\']+)["\']',
            r'url:\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if match.startswith('/'):
                    full_url = urljoin(base_url, match)
                elif match.startswith('http'):
                    full_url = match
                else:
                    full_url = urljoin(base_url, match)

                if full_url not in endpoints:
                    endpoints.append(full_url)

        return endpoints[:10]  # Limit to 10 most relevant

    def tool_fetch_data(self, url: str) -> Optional[pd.DataFrame]:
        """
        Fetch and parse data from a URL with format auto-detection.
        Enhanced for API endpoints and various formats.
        """
        self._log(f"FETCH DATA: {url[:60]}...")

        try:
            response = self.session.get(url, timeout=60)
            if not response.ok:
                return None

            content = response.content
            content_type = response.headers.get('content-type', '').lower()

            # Try to parse based on content
            df = self.tool_parse(content, content_type)

            if df is not None:
                self._record("fetch_data", url, f"Got {len(df)} rows", "")
                return df

        except Exception as e:
            self._record("fetch_data", url, f"Error: {e}", "")

        return None

    def tool_ask(self, question: str, context: str = "") -> str:
        """Ask Legomena for reasoning."""
        prompt = f"""{context}

{question}

Answer concisely:"""

        try:
            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=45
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        return ""

    # =========================================================================
    # LOCATION-AWARE DISCOVERY (v1.5.1)
    # =========================================================================

    def _detect_geographic_context(self, topic: str) -> Optional[Dict]:
        """
        Dynamically detect if topic has geographic context.
        Returns location info or None.
        """
        question = f"""Does this topic have a specific geographic location?
Topic: "{topic}"

If yes, respond with EXACTLY this format:
LOCATION: [place name]
COUNTRY: [country name]
LANGUAGE: [primary language for data]

If no specific location, respond with:
GLOBAL

Answer:"""

        response = self.tool_ask(question)

        if "GLOBAL" in response.upper() or "LOCATION:" not in response:
            return None

        # Parse location info
        location = {}
        for line in response.split('\n'):
            if 'LOCATION:' in line:
                location['place'] = line.split('LOCATION:')[1].strip()
            elif 'COUNTRY:' in line:
                location['country'] = line.split('COUNTRY:')[1].strip()
            elif 'LANGUAGE:' in line:
                location['language'] = line.split('LANGUAGE:')[1].strip()

        if location.get('place'):
            self._log(f"Geographic context detected: {location}")
            return location

        return None

    def _get_regional_data_sources(self, topic: str, domain: str,
                                   location: Dict) -> List[str]:
        """
        Ask Legomena for region-specific data sources dynamically.
        No hardcoded databases - pure reasoning.
        """
        place = location.get('place', '')
        country = location.get('country', '')
        language = location.get('language', 'English')

        question = f"""I need scientific data about: {topic}
Domain: {domain}
Location: {place}, {country}

What are the SPECIFIC data sources for this region? Consider:
1. National government agencies (environment, weather, science)
2. Regional monitoring organizations
3. University research centers
4. EU/international programs covering this area

List the most relevant data sources with their website domains if known.
Focus on sources that provide downloadable data files.

Answer concisely:"""

        response = self.tool_ask(question)
        self._log(f"Regional sources from Legomena: {response[:200]}...")

        # Extract organization names and URLs
        sources = []

        # Extract capitalized organization names
        org_names = re.findall(r'\b([A-Z][A-Za-z0-9\-\.]{2,}[A-Za-z0-9]*)\b', response)
        sources.extend([n for n in org_names if n not in ['CSV', 'JSON', 'API', 'URL', 'HTTP', 'The', 'For', 'Data']])

        # Extract any URLs mentioned
        urls = re.findall(r'https?://[^\s<>"\']+', response)

        return list(set(sources))[:8], urls[:5]

    def _generate_multilingual_queries(self, topic: str, location: Dict) -> List[str]:
        """
        Generate search queries in multiple languages for the location.
        """
        place = location.get('place', '')
        language = location.get('language', 'English')

        if language.lower() == 'english':
            return []  # No extra queries needed

        question = f"""Translate this search query to {language}:
"official data download {topic}"

Also provide a query for "{place} scientific measurements data"

Just give the translated queries, one per line:"""

        response = self.tool_ask(question)
        queries = [q.strip() for q in response.split('\n') if q.strip() and len(q) > 10]

        if queries:
            self._log(f"Multi-language queries: {queries[:3]}")

        return queries[:3]

    # =========================================================================
    # EXPLORATION STRATEGIES
    # =========================================================================

    def explore_for_data(self, topic: str, domain: str,
                        quantities: List[str]) -> DataDiscovery:
        """
        Explore the web to find scientific data.

        Uses multi-step reasoning:
        1. Ask: What databases exist for this domain?
        2. Search: Find data portals
        3. Navigate: Explore portals to find data
        4. Download: Get actual data files
        """
        self._log(f"\n{'='*60}")
        self._log(f"HERMES EXPLORER v{__version__}")
        self._log(f"Topic: {topic}")
        self._log(f"Domain: {domain}")
        self._log(f"Looking for: {quantities}")
        self._log(f"{'='*60}\n")

        self.steps = []
        self.visited = set()

        # Step 0: Detect geographic context (NEW in v1.5.1)
        self._log("--- Step 0: Detect Geographic Context ---")
        location = self._detect_geographic_context(topic)

        regional_sources = []
        regional_urls = []
        multilingual_queries = []

        if location:
            self._log(f"Location detected: {location.get('place', 'unknown')}, {location.get('country', 'unknown')}")

            # Get region-specific sources
            regional_sources, regional_urls = self._get_regional_data_sources(topic, domain, location)
            self._log(f"Regional sources: {regional_sources[:5]}")

            # Get multilingual search queries
            multilingual_queries = self._generate_multilingual_queries(topic, location)
        else:
            self._log("No specific geographic context - using global search")

        # Step 1: Ask about data sources
        self._log("\n--- Step 1: Identify Data Sources ---")
        sources_question = f"What are the main scientific databases for {domain} that would have {', '.join(quantities[:3])}? List database names."

        sources_response = self.tool_ask(sources_question)
        self._log(f"Legomena says: {sources_response[:200]}...")

        # Extract database names
        database_names = re.findall(r'\b([A-Z][A-Z0-9\-]{2,}[A-Za-z0-9]*)\b', sources_response)
        database_names = [d for d in database_names if d not in ['CSV', 'JSON', 'API', 'URL', 'HTTP']]

        # Add regional sources to database list (NEW in v1.5.1)
        database_names = regional_sources + database_names
        self._log(f"Databases identified: {database_names[:8]}")

        # Step 2: Search for data portals
        self._log("\n--- Step 2: Search for Data Portals ---")

        search_queries = [
            f"{topic} official data download",
            f"{domain} scientific data portal",
        ]

        # Add location-specific queries (NEW in v1.5.1)
        if location:
            place = location.get('place', '')
            country = location.get('country', '')
            search_queries.insert(0, f"{place} {topic} data CSV download")
            search_queries.insert(1, f"{country} {domain} official data portal")

        # Add multilingual queries (NEW in v1.5.1)
        search_queries.extend(multilingual_queries)

        # Add database-specific searches
        for db in database_names[:3]:
            search_queries.append(f"{db} official data download")

        all_results = []
        for query in search_queries[:4]:
            results = self.tool_search(query)
            all_results.extend(results)

            if len(all_results) >= 10:
                break

        # Add regional URLs directly (NEW in v1.5.1)
        for url in regional_urls:
            all_results.insert(0, {"url": url, "title": f"Regional: {url[:40]}"})

        # Deduplicate by domain
        seen_domains = set()
        unique_results = []
        for r in all_results:
            domain_name = urlparse(r['url']).netloc
            if domain_name not in seen_domains:
                seen_domains.add(domain_name)
                unique_results.append(r)

        self._log(f"Found {len(unique_results)} unique portals")

        # Step 3: Prioritize results
        self._log("\n--- Step 3: Prioritize Portals ---")

        # Build location-aware scoring (NEW in v1.5.1)
        location_terms = []
        if location:
            location_terms = [
                location.get('place', '').lower(),
                location.get('country', '').lower(),
            ]
            # Add country TLD
            country = location.get('country', '').lower()
            country_tlds = {
                'italy': '.it', 'germany': '.de', 'france': '.fr',
                'spain': '.es', 'switzerland': '.ch', 'austria': '.at',
                'netherlands': '.nl', 'belgium': '.be', 'uk': '.uk',
                'japan': '.jp', 'china': '.cn', 'australia': '.au',
            }
            if country in country_tlds:
                location_terms.append(country_tlds[country])

        # Prefer .gov, .edu, regional, and known scientific domains
        def score_result(r):
            url = r['url'].lower()
            score = 0

            # Regional sources get highest priority (NEW in v1.5.1)
            if any(term in url for term in location_terms if term):
                score += 20

            if '.gov' in url:
                score += 10
            if '.edu' in url:
                score += 8
            if any(org in url for org in ['noaa', 'nasa', 'esa', 'cern', 'ncei']):
                score += 15
            if 'data' in url:
                score += 5

            # Regional TLDs for scientific data
            regional_tlds = ['.it', '.de', '.fr', '.ch', '.eu']
            if any(tld in url for tld in regional_tlds):
                score += 5

            return score

        unique_results.sort(key=score_result, reverse=True)

        for r in unique_results[:5]:
            self._log(f"  {r['title'][:40]}: {r['url'][:50]}")

        # Step 4: Explore top portals (ENHANCED in v1.6.0)
        self._log("\n--- Step 4: Explore Portals (v1.6.0 Enhanced) ---")

        for result in unique_results[:5]:
            portal_url = result['url']
            self._log(f"\nExploring: {portal_url[:60]}")

            html = self.tool_fetch(portal_url)
            if not html:
                continue

            # NEW v1.6.0: Try to extract data tables directly from HTML
            df = self._parse_html_tables(html)
            if df is not None and len(df) > 30:
                self._log(f"  SUCCESS (HTML table): {len(df)} rows!")
                return DataDiscovery(
                    success=True,
                    url=portal_url,
                    data=df,
                    steps=self.steps,
                    description=f"Extracted HTML table from {portal_url}"
                )

            # NEW v1.6.0: Detect and try API endpoints
            api_endpoints = self._detect_api_endpoints(html, portal_url)
            for api_url in api_endpoints[:3]:
                self._log(f"  Trying API: {api_url[:50]}...")
                df = self.tool_fetch_data(api_url)
                if df is not None and len(df) > 30:
                    self._log(f"  SUCCESS (API): {len(df)} rows!")
                    return DataDiscovery(
                        success=True,
                        url=api_url,
                        data=df,
                        steps=self.steps,
                        description=f"Found data via API: {api_url}"
                    )

            # Find data links
            data_links = self.tool_extract_links(
                html, portal_url,
                filter_terms=['data', 'csv', 'download', 'access', 'dataset', 'ascii', 'txt', 'json']
            )

            self._log(f"  Found {len(data_links)} data-related links")

            # Ask which to follow
            if len(data_links) > 3:
                link_summary = "\n".join([f"- {l['text'][:40]}: {l['url'][:50]}"
                                         for l in data_links[:10]])
                follow_question = f"I'm looking for {topic} data.\nWhich link should I follow?\n{link_summary}"
                follow_response = self.tool_ask(follow_question)

                # Extract recommended URL
                url_match = re.search(r'https?://[^\s<>"\']+', follow_response)
                if url_match:
                    recommended = url_match.group()
                    # Put it first
                    data_links = [l for l in data_links if l['url'] == recommended] + \
                                [l for l in data_links if l['url'] != recommended]

            # Try data links with enhanced parsing
            for link in data_links[:8]:  # Increased from 5 to 8
                link_url = link['url']

                # NEW v1.6.0: Try to fetch and parse any link that might have data
                df = self.tool_fetch_data(link_url)
                if df is not None and len(df) > 30:
                    self._log(f"  SUCCESS: {len(df)} rows!")
                    return DataDiscovery(
                        success=True,
                        url=link_url,
                        data=df,
                        steps=self.steps,
                        description=f"Found data via {portal_url}"
                    )

                # Navigate deeper for non-data links
                if not link['is_data']:
                    sub_html = self.tool_fetch(link_url)
                    if not sub_html:
                        continue

                    # Try HTML tables on sub-page
                    df = self._parse_html_tables(sub_html)
                    if df is not None and len(df) > 30:
                        self._log(f"  SUCCESS (sub-page HTML table): {len(df)} rows!")
                        return DataDiscovery(
                            success=True,
                            url=link_url,
                            data=df,
                            steps=self.steps,
                            description=f"Extracted HTML table from {link_url}"
                        )

                    # Try API endpoints on sub-page
                    sub_api_endpoints = self._detect_api_endpoints(sub_html, link_url)
                    for api_url in sub_api_endpoints[:2]:
                        df = self.tool_fetch_data(api_url)
                        if df is not None and len(df) > 30:
                            self._log(f"  SUCCESS (sub-page API): {len(df)} rows!")
                            return DataDiscovery(
                                success=True,
                                url=api_url,
                                data=df,
                                steps=self.steps,
                                description=f"Found via API: {api_url}"
                            )

                    sub_links = self.tool_extract_links(sub_html, link_url, filter_terms=['.csv', '.txt', '.json', 'data', 'ascii'])

                    for sub_link in sub_links[:5]:
                        df = self.tool_fetch_data(sub_link['url'])
                        if df is not None and len(df) > 30:
                            self._log(f"  SUCCESS: {len(df)} rows!")
                            return DataDiscovery(
                                success=True,
                                url=sub_link['url'],
                                data=df,
                                steps=self.steps,
                                description=f"Found via navigation: {portal_url} -> {link_url}"
                            )

        return DataDiscovery(
            success=False,
            url="",
            data=None,
            steps=self.steps,
            description="Could not find data after exploration"
        )


def main():
    """Test the explorer."""
    explorer = HermesExplorer()

    result = explorer.explore_for_data(
        topic="hurricane eye and wind structure",
        domain="meteorology",
        quantities=["eye_diameter", "radius_of_maximum_wind", "wind_speed"]
    )

    print("\n" + "="*60)
    print("EXPLORATION RESULT")
    print("="*60)
    print(f"Success: {result.success}")
    print(f"URL: {result.url}")
    print(f"Steps taken: {len(result.steps)}")
    print(f"Description: {result.description}")

    if result.data is not None:
        print(f"\nData: {len(result.data)} rows, {len(result.data.columns)} columns")
        eye_cols = [c for c in result.data.columns if 'eye' in str(c).lower()]
        rmw_cols = [c for c in result.data.columns if 'rmw' in str(c).lower()]
        print(f"Eye columns: {eye_cols}")
        print(f"RMW columns: {rmw_cols}")


if __name__ == "__main__":
    main()
