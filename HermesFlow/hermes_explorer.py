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

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")

# Version with dynamic persistent exploration
__version__ = "1.8.0"

# No hardcoded sources - everything discovered dynamically


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

        # Extract any URLs mentioned (handle markdown links properly)
        # First try to extract from markdown [text](url) format
        markdown_urls = re.findall(r'\]\((https?://[^)]+)\)', response)
        # Then extract raw URLs, excluding markdown artifacts
        raw_urls = re.findall(r'https?://[^\s<>"\'\)\]]+', response)
        urls = list(set(markdown_urls + raw_urls))

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
    # DATA VALIDATION (v1.7.0) - The key missing piece
    # =========================================================================

    def _validate_data_relevance(self, df: pd.DataFrame, topic: str,
                                  source_url: str) -> Tuple[bool, str]:
        """
        Dynamically validate if the downloaded data is actually relevant.

        This is the KEY fix - instead of accepting any data, we verify it
        actually relates to what we're looking for.

        Returns: (is_valid, reason)
        """
        if df is None or len(df) < 10:
            return False, "Insufficient data"

        # Get column names and sample values
        columns = list(df.columns)
        sample_values = []
        for col in columns[:8]:
            try:
                vals = df[col].dropna().head(3).tolist()
                sample_values.append(f"{col}: {vals}")
            except:
                pass

        # Ask Legomena to validate
        question = f"""I'm looking for data about: {topic}

I found this data from: {source_url}

Columns: {columns[:15]}
Sample data:
{chr(10).join(sample_values[:6])}

QUESTION: Does this data actually relate to "{topic}"?

Answer with EXACTLY one of:
- RELEVANT: [brief reason why]
- IRRELEVANT: [brief reason why]
- UNCERTAIN: [what's missing]

Answer:"""

        response = self.tool_ask(question)

        if "RELEVANT" in response.upper():
            self._log(f"  ✓ Data validated as relevant")
            return True, response
        elif "IRRELEVANT" in response.upper():
            self._log(f"  ✗ Data rejected: {response[:80]}")
            return False, response
        else:
            # Uncertain - apply additional checks
            self._log(f"  ? Uncertain relevance: {response[:80]}")
            # If uncertain, check for obvious garbage patterns
            if self._looks_like_garbage(df, topic):
                return False, "Failed garbage detection"
            return True, "Passed fallback checks"

    def _looks_like_garbage(self, df: pd.DataFrame, topic: str) -> bool:
        """
        Detect obviously wrong data without relying on LLM.

        Patterns that indicate garbage:
        - Columns named 'emoji', 'icon', 'badge', etc.
        - All string columns with no numbers
        - YouTube/social media patterns
        """
        columns_lower = [str(c).lower() for c in df.columns]

        # Garbage column indicators
        garbage_patterns = ['emoji', 'badge', 'icon', 'avatar', 'thumbnail',
                           'subscriber', 'follower', 'like', 'view', 'share',
                           'playlist', 'channel', 'video', 'stream']

        if any(pattern in ' '.join(columns_lower) for pattern in garbage_patterns):
            self._log(f"  ✗ Garbage detected: social media patterns in columns")
            return True

        # Check for numeric content - scientific data should have numbers
        numeric_cols = df.select_dtypes(include=['number']).shape[1]
        if numeric_cols < 1 and len(df.columns) > 3:
            self._log(f"  ✗ Garbage detected: no numeric columns")
            return True

        # Check if any column relates to topic keywords
        topic_words = set(topic.lower().split())
        topic_words -= {'data', 'the', 'of', 'and', 'for', 'a', 'in', 'to'}

        # At least one column should relate to topic
        has_relevant_column = False
        for col in columns_lower:
            if any(word in col for word in topic_words if len(word) > 2):
                has_relevant_column = True
                break

        # Not having a relevant column is suspicious but not definitive
        # Let other checks decide

        return False

    def _extract_topic_location(self, topic: str) -> Optional[Dict]:
        """
        Better location extraction for topics like 'Venice acqua alta'.

        Uses pattern matching + LLM fallback.
        """
        # Common location patterns in scientific topics
        known_locations = {
            'venice': {'place': 'Venice', 'country': 'Italy', 'language': 'Italian'},
            'tokyo': {'place': 'Tokyo', 'country': 'Japan', 'language': 'Japanese'},
            'london': {'place': 'London', 'country': 'UK', 'language': 'English'},
            'arctic': {'place': 'Arctic', 'country': 'International', 'language': 'English'},
            'antarctic': {'place': 'Antarctica', 'country': 'International', 'language': 'English'},
            'alps': {'place': 'Alps', 'country': 'Switzerland', 'language': 'German'},
            'california': {'place': 'California', 'country': 'USA', 'language': 'English'},
            'florida': {'place': 'Florida', 'country': 'USA', 'language': 'English'},
            'hawaii': {'place': 'Hawaii', 'country': 'USA', 'language': 'English'},
            'adriatic': {'place': 'Adriatic', 'country': 'Italy', 'language': 'Italian'},
        }

        topic_lower = topic.lower()

        # Check for known locations
        for location, info in known_locations.items():
            if location in topic_lower:
                self._log(f"Quick location match: {info['place']}")
                return info

        # Fall through to LLM-based detection
        return None

    def _try_return_validated(self, df: pd.DataFrame, url: str,
                               topic: str, description: str) -> Optional[DataDiscovery]:
        """
        Validate data before returning it as a discovery.

        Returns DataDiscovery if valid, None if invalid (continue searching).
        """
        if df is None:
            return None

        # Run validation
        is_valid, reason = self._validate_data_relevance(df, topic, url)

        if is_valid:
            return DataDiscovery(
                success=True,
                url=url,
                data=df,
                steps=self.steps,
                description=description
            )
        else:
            self._log(f"  Rejected: {reason[:60]}")
            return None

    # =========================================================================
    # DYNAMIC PERSISTENT EXPLORATION (v1.8.0)
    # =========================================================================

    def _explore_portal_deeply(self, portal_url: str, html: str, topic: str,
                               quantities: List[str], depth: int = 0) -> Optional[DataDiscovery]:
        """
        Deep exploration of a data portal page.

        This is the KEY to dynamic data discovery - we persistently explore
        the portal until we find actual data files, not just portal pages.

        Works for ANY domain/topic by:
        1. Extracting ALL links that might lead to data
        2. Categorizing them (direct files vs. intermediate pages)
        3. Trying direct files first
        4. Then recursively exploring intermediate pages
        """
        if depth > 2:  # Prevent infinite recursion
            return None

        self._log(f"  Deep exploration (depth={depth}): {portal_url[:50]}...")

        # Extract ALL links from the page
        soup = BeautifulSoup(html, 'html.parser')

        # Categorize links
        direct_data_files = []  # .csv, .json, .txt, etc.
        intermediate_pages = []  # Pages that might have data links
        api_endpoints = []  # API URLs

        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()[:80]

            # Skip empty or javascript links
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            full_url = urljoin(portal_url, href)

            # Skip already visited
            if full_url in self.visited:
                continue

            href_lower = href.lower()

            # Category 1: Direct data files (highest priority)
            data_extensions = ['.csv', '.txt', '.json', '.nc', '.dat', '.asc',
                              '.geojson', '.xml', '.data', '.tsv']
            if any(ext in href_lower for ext in data_extensions):
                direct_data_files.append({
                    'url': full_url,
                    'text': text,
                    'ext': next((ext for ext in data_extensions if ext in href_lower), '')
                })
                continue

            # Category 2: API endpoints
            if '/api/' in href_lower or 'query' in href_lower or 'service' in href_lower:
                api_endpoints.append({'url': full_url, 'text': text})
                continue

            # Category 3: Intermediate pages that might have data
            data_keywords = ['data', 'download', 'export', 'feed', 'catalog',
                            'archive', 'database', 'dataset', 'summary', 'output']
            if any(kw in href_lower or kw in text.lower() for kw in data_keywords):
                intermediate_pages.append({'url': full_url, 'text': text})

        self._log(f"    Found: {len(direct_data_files)} data files, "
                  f"{len(intermediate_pages)} intermediate pages, "
                  f"{len(api_endpoints)} APIs")

        # Strategy 1: Try direct data files first (most efficient)
        for file_info in direct_data_files[:10]:  # Try up to 10 files
            file_url = file_info['url']
            self._log(f"    Trying data file: {file_url.split('/')[-1]}")

            df = self.tool_fetch_data(file_url)
            if df is not None and len(df) > 10:
                is_valid, reason = self._validate_data_relevance(df, topic, file_url)
                if is_valid:
                    self._log(f"    SUCCESS: {len(df)} rows from {file_info['ext']}")
                    return DataDiscovery(
                        success=True,
                        url=file_url,
                        data=df,
                        steps=self.steps,
                        description=f"Found via deep exploration: {file_url}"
                    )

        # Strategy 2: Try API endpoints
        for api_info in api_endpoints[:5]:
            api_url = api_info['url']
            if api_url in self.visited:
                continue

            self._log(f"    Trying API: {api_url[:50]}...")
            df = self.tool_fetch_data(api_url)
            if df is not None and len(df) > 10:
                is_valid, reason = self._validate_data_relevance(df, topic, api_url)
                if is_valid:
                    self._log(f"    SUCCESS via API: {len(df)} rows")
                    return DataDiscovery(
                        success=True,
                        url=api_url,
                        data=df,
                        steps=self.steps,
                        description=f"Found via API endpoint: {api_url}"
                    )

        # Strategy 3: Recursively explore intermediate pages (deeper exploration)
        if depth < 2:
            for page_info in intermediate_pages[:3]:  # Only explore top 3
                page_url = page_info['url']
                if page_url in self.visited:
                    continue

                self._log(f"    Exploring intermediate: {page_info['text'][:30]}")
                page_html = self.tool_fetch(page_url)
                if page_html:
                    result = self._explore_portal_deeply(
                        page_url, page_html, topic, quantities, depth + 1
                    )
                    if result and result.success:
                        return result

        return None

    def _construct_common_data_urls(self, base_url: str, topic: str,
                                    quantities: List[str]) -> List[str]:
        """
        Dynamically construct common data URL patterns.

        Many data portals follow similar URL patterns. Instead of hardcoding,
        we ask Legomena to suggest URL patterns based on the portal structure.
        """
        question = f"""I'm on this data portal: {base_url}
Topic: {topic}
Looking for: {', '.join(quantities[:3])}

What are common URL patterns that might give me downloadable data?
Consider patterns like:
- /data/download.csv
- /api/v1/data?format=csv
- /summary/all.csv
- /export?type=csv

Give me 3-5 specific URL patterns to try (relative to base URL):"""

        response = self.tool_ask(question)

        # Extract URL patterns from response
        patterns = []
        for line in response.split('\n'):
            # Look for paths that look like URLs
            path_match = re.search(r'(/[a-zA-Z0-9/_\-\.]+(?:\?[a-zA-Z0-9=&]+)?)', line)
            if path_match:
                full_url = urljoin(base_url, path_match.group(1))
                if full_url not in self.visited:
                    patterns.append(full_url)

        return patterns[:5]

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

        # Step 0: Detect geographic context (IMPROVED in v1.7.0)
        self._log("--- Step 0: Detect Geographic Context ---")

        # Try quick pattern match first (v1.7.0)
        location = self._extract_topic_location(topic)

        # Fall back to LLM-based detection
        if not location:
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
            try:
                url = r.get('url', '')
                if not url or not url.startswith('http'):
                    continue
                domain_name = urlparse(url).netloc
                if domain_name and domain_name not in seen_domains:
                    seen_domains.add(domain_name)
                    unique_results.append(r)
            except (ValueError, TypeError):
                # Skip malformed URLs
                continue

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

        # Step 4: DYNAMIC PERSISTENT EXPLORATION (v1.8.0 - completely redesigned)
        self._log("\n--- Step 4: Dynamic Persistent Exploration (v1.8.0) ---")

        # Handle case where no results found
        if not unique_results:
            self._log("No search results found, going directly to fallback")
            ordered_results = []
        else:
            # Ask Legomena to analyze the search results and recommend the best path
            portal_summary = "\n".join([f"{i+1}. {r['title']}: {r['url']}"
                                       for i, r in enumerate(unique_results[:8])])

            guidance_question = f"""I found these potential data sources for "{topic}":

{portal_summary}

Which portals are MOST likely to have DOWNLOADABLE data files (CSV, TXT, JSON)?
Consider:
- Government/scientific institution sources (.gov, .edu) are usually best
- URLs with "data", "download", "feed", "csv" are promising
- Avoid documentation or help pages

Reply with:
BEST: [number 1-8]
ALSO_TRY: [second best number]
REASON: [one sentence]"""

            guidance = self.tool_ask(guidance_question)
            self._log(f"Legomena guidance: {guidance[:100]}...")

            # Parse recommended portals
            best_match = re.search(r'BEST:\s*(\d+)', guidance)
            also_match = re.search(r'ALSO_TRY:\s*(\d+)', guidance)
            best_idx = int(best_match.group(1)) - 1 if best_match else 0
            also_idx = int(also_match.group(1)) - 1 if also_match else 1

            best_idx = min(max(0, best_idx), len(unique_results) - 1)
            also_idx = min(max(0, also_idx), len(unique_results) - 1)

            # Prioritize Legomena's recommendations
            seen = set()
            ordered_results = []
            for idx in [best_idx, also_idx]:
                if idx not in seen:
                    ordered_results.append(unique_results[idx])
                    seen.add(idx)
            for i, r in enumerate(unique_results):
                if i not in seen:
                    ordered_results.append(r)

        # PERSISTENT EXPLORATION: Try each portal with deep exploration
        for result in ordered_results[:4]:  # Try top 4 portals
            portal_url = result['url']
            self._log(f"\nDeep exploration: {portal_url[:60]}")

            html = self.tool_fetch(portal_url)
            if not html:
                continue

            # v1.8.0: Use deep exploration to find data files recursively
            discovery = self._explore_portal_deeply(
                portal_url, html, topic, quantities, depth=0
            )
            if discovery and discovery.success:
                return discovery

            # If deep exploration didn't find direct files, try Legomena guidance
            page_links = self.tool_extract_links(html, portal_url)
            link_summary = "\n".join([f"- {l['text'][:40]}: {l['url'][:50]}"
                                     for l in page_links[:25] if l['text'].strip()])

            nav_question = f"""I'm on a data portal looking for {topic} data.

Links on this page:
{link_summary[:2500]}

Which link leads to ACTUAL DATA FILES (not documentation)?
Look for:
- Direct files: .csv, .txt, .json, .dat, .nc
- Feed/summary pages with data listings
- API or query endpoints

Reply with the BEST URL for data:
URL: [full url]"""

            nav_response = self.tool_ask(nav_question)
            url_match = re.search(r'URL:\s*\[?(?:\[[^\]]*\]\()?(https?://[^\s<>"\'\)\]]+)', nav_response)

            if url_match:
                recommended_url = url_match.group(1)
                self._log(f"  Legomena suggests: {recommended_url[:50]}")

                # If it's a page (not a file), explore it deeply too
                if not any(ext in recommended_url.lower() for ext in ['.csv', '.txt', '.json', '.dat']):
                    rec_html = self.tool_fetch(recommended_url)
                    if rec_html:
                        discovery = self._explore_portal_deeply(
                            recommended_url, rec_html, topic, quantities, depth=1
                        )
                        if discovery and discovery.success:
                            return discovery
                else:
                    # Direct file URL
                    df = self.tool_fetch_data(recommended_url)
                    if df is not None and len(df) > 20:
                        is_valid, reason = self._validate_data_relevance(df, topic, recommended_url)
                        if is_valid:
                            return DataDiscovery(
                                success=True,
                                url=recommended_url,
                                data=df,
                                steps=self.steps,
                                description=f"Found via Legomena guidance: {recommended_url}"
                            )

            # v1.8.0: Try constructing common URL patterns
            pattern_urls = self._construct_common_data_urls(portal_url, topic, quantities)
            for purl in pattern_urls:
                self._log(f"  Trying pattern: {purl.split('/')[-1]}")
                df = self.tool_fetch_data(purl)
                if df is not None and len(df) > 20:
                    is_valid, reason = self._validate_data_relevance(df, topic, purl)
                    if is_valid:
                        return DataDiscovery(
                            success=True,
                            url=purl,
                            data=df,
                            steps=self.steps,
                            description=f"Found via pattern matching: {purl}"
                        )

        # =====================================================================
        # FALLBACK STRATEGIES (v1.7.0) - Try alternative approaches
        # =====================================================================
        self._log("\n--- Fallback: Alternative Search Strategies ---")

        # Fallback 1: Ask Legomena for direct suggestions
        fallback_question = f"""I'm looking for scientific data about: {topic}
Domain: {domain}
I need quantities like: {', '.join(quantities[:3])}

My initial search didn't find downloadable data. What specific databases,
APIs, or data sources should I try? Give me DIRECT URLs if you know them.

Be specific - name the exact organization and data portal."""

        fallback_response = self.tool_ask(fallback_question)
        self._log(f"Fallback suggestions: {fallback_response[:200]}...")

        # Extract URLs from the response (handle markdown links properly)
        markdown_urls = re.findall(r'\]\((https?://[^)]+)\)', fallback_response)
        raw_urls = re.findall(r'https?://[^\s<>"\'\)\]]+', fallback_response)
        fallback_urls = list(set(markdown_urls + raw_urls))

        for url in fallback_urls[:5]:
            if url in self.visited:
                continue

            self._log(f"Trying fallback URL: {url[:50]}...")
            df = self.tool_fetch_data(url)

            if df is not None and len(df) > 20:
                # Validate relevance
                is_valid, reason = self._validate_data_relevance(df, topic, url)
                if is_valid:
                    self._log(f"  FALLBACK SUCCESS: {len(df)} rows!")
                    return DataDiscovery(
                        success=True,
                        url=url,
                        data=df,
                        steps=self.steps,
                        description=f"Found via fallback reasoning: {url}"
                    )

        # Fallback 2: Try broader search with different keywords (v1.8.0 enhanced)
        self._log("\n--- Fallback: Broader Search with Deep Exploration ---")

        broader_queries = [
            f"{domain} CSV data download feed",
            f"{quantities[0] if quantities else topic} CSV download",
            f"international {domain} monitoring data portal",
        ]

        for query in broader_queries:
            self._log(f"Broader search: {query}")
            results = self.tool_search(query)

            for result in results[:3]:
                if result['url'] in self.visited:
                    continue

                html = self.tool_fetch(result['url'])
                if not html:
                    continue

                # v1.8.0: Use deep exploration on search results
                discovery = self._explore_portal_deeply(
                    result['url'], html, topic, quantities, depth=0
                )
                if discovery and discovery.success:
                    self._log(f"  BROADER SUCCESS via deep exploration!")
                    return discovery

                # Fallback: Try data-looking links directly
                data_links = self.tool_extract_links(
                    html, result['url'],
                    filter_terms=['.csv', '.txt', '.json', 'download', 'data']
                )

                for link in data_links[:3]:
                    df = self.tool_fetch_data(link['url'])
                    if df is not None and len(df) > 20:
                        is_valid, reason = self._validate_data_relevance(df, topic, link['url'])
                        if is_valid:
                            self._log(f"  BROADER SUCCESS: {len(df)} rows!")
                            return DataDiscovery(
                                success=True,
                                url=link['url'],
                                data=df,
                                steps=self.steps,
                                description=f"Found via broader search: {query}"
                            )

        return DataDiscovery(
            success=False,
            url="",
            data=None,
            steps=self.steps,
            description="Could not find data after exploration and fallback strategies"
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
