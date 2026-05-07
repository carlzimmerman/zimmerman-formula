#!/usr/bin/env python3
"""
HERMES NAVIGATOR
================

Creative solution: Use HTML pages as navigation aids, not reject them.

When searching for scientific data:
1. Search for dataset landing page
2. Fetch HTML
3. Use Legomena to analyze HTML and find download links
4. Follow links to actual data
5. Recursively navigate if needed

This mimics how humans browse for data!

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import re
import json
import subprocess
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
import io

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-4b")
CACHE_DIR = Path(__file__).parent / "navigator_cache"
CACHE_DIR.mkdir(exist_ok=True)


@dataclass
class NavigationResult:
    """Result of navigation attempt."""
    success: bool
    url: str
    data: Optional[pd.DataFrame]
    path_taken: List[str]  # URLs we navigated through
    description: str


class HermesNavigator:
    """
    Navigate web pages to find scientific data.

    Uses Legomena to understand HTML and make navigation decisions.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HermesNavigator/1.0 (Scientific Research)"
        })
        self.visited = set()  # Avoid infinite loops
        self.max_depth = 5

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Navigator {ts}] {msg}")

    def _call_legomena(self, prompt: str, timeout: int = 60) -> Optional[str]:
        """Call Legomena LLM."""
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
            self._log("Legomena timeout")
        except Exception as e:
            self._log(f"Legomena error: {e}")
        return None

    def _fetch(self, url: str, timeout: int = 30) -> Optional[bytes]:
        """Fetch URL content."""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.content
        except Exception as e:
            self._log(f"Fetch error: {e}")
            return None

    def _is_data_file(self, url: str, content: bytes) -> bool:
        """Check if content is actual data (not HTML)."""
        url_lower = url.lower()

        # Check URL extension
        if any(url_lower.endswith(ext) for ext in ['.csv', '.txt', '.dat', '.json', '.tsv']):
            # Verify it's not HTML
            text = content[:500].decode('utf-8', errors='ignore').lower()
            if '<html' not in text and '<!doctype' not in text:
                return True

        # Check content type
        text = content[:1000].decode('utf-8', errors='ignore')
        if '<html' in text.lower():
            return False

        # Check if it looks like CSV/tabular data
        lines = text.split('\n')[:5]
        if len(lines) >= 2:
            # Check for consistent delimiters
            for delim in [',', '\t', '|']:
                counts = [line.count(delim) for line in lines if line.strip()]
                if len(counts) >= 2 and len(set(counts)) == 1 and counts[0] > 2:
                    return True

        return False

    def _extract_links(self, html: str, base_url: str) -> List[Dict]:
        """Extract all links from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()[:100]

            # Make absolute URL
            full_url = urljoin(base_url, href)

            # Categorize link
            href_lower = href.lower()
            is_data = any(ext in href_lower for ext in ['.csv', '.txt', '.dat', '.nc', '.json', 'download'])
            is_directory = href.endswith('/') or 'data' in href_lower or 'access' in href_lower

            links.append({
                "url": full_url,
                "text": text,
                "is_data": is_data,
                "is_directory": is_directory
            })

        return links

    def _ask_legomena_for_links(self, html: str, target: str, base_url: str) -> List[str]:
        """Ask Legomena to identify download links in HTML."""
        # Extract links first
        links = self._extract_links(html, base_url)

        # Filter to interesting links
        interesting = [l for l in links if l['is_data'] or l['is_directory'] or
                      any(kw in l['text'].lower() for kw in ['download', 'data', 'csv', 'access'])][:30]

        if not interesting:
            interesting = links[:30]

        # Format for Legomena
        link_list = "\n".join([f"- {l['text']}: {l['url']}" for l in interesting])

        prompt = f"""I'm looking for: {target}

This page has these links:
{link_list}

Which links are most likely to lead to downloadable data files (.csv, .txt)?
List the URLs (one per line) in order of relevance.
Only list URLs, no explanations.

URLs:"""

        response = self._call_legomena(prompt, timeout=45)

        if response:
            urls = []
            for line in response.split('\n'):
                line = line.strip().strip('-').strip()
                # Extract URL
                match = re.search(r'https?://[^\s<>"\']+', line)
                if match:
                    urls.append(match.group())
            return urls[:10]

        # Fallback: return data-looking links
        return [l['url'] for l in interesting if l['is_data']][:5]

    def _ask_legomena_for_directory(self, links: List[Dict], target: str) -> Optional[str]:
        """Ask Legomena which directory to explore."""
        dir_links = [l for l in links if l['is_directory']][:20]

        if not dir_links:
            return None

        link_list = "\n".join([f"- {l['text']}: {l['url']}" for l in dir_links])

        prompt = f"""I'm looking for: {target}

Which directory should I explore?
{link_list}

Answer with just the URL:"""

        response = self._call_legomena(prompt, timeout=30)

        if response:
            match = re.search(r'https?://[^\s<>"\']+', response)
            if match:
                return match.group()

        return None

    def _parse_data(self, content: bytes) -> Optional[pd.DataFrame]:
        """Parse data content into DataFrame."""
        text = content.decode('utf-8', errors='ignore')

        # Skip HTML
        if '<html' in text.lower()[:500]:
            return None

        # Try CSV
        try:
            df = pd.read_csv(io.StringIO(text), low_memory=False)
            if len(df) > 10 and len(df.columns) > 2:
                return df
        except:
            pass

        # Try tab-separated
        try:
            df = pd.read_csv(io.StringIO(text), sep='\t', low_memory=False)
            if len(df) > 10 and len(df.columns) > 2:
                return df
        except:
            pass

        # Try space-separated
        try:
            lines = [l for l in text.split('\n') if l.strip() and not l.startswith('#')]
            if len(lines) > 10:
                records = [line.split() for line in lines]
                # Filter to consistent column count
                col_counts = [len(r) for r in records]
                if col_counts:
                    mode_count = max(set(col_counts), key=col_counts.count)
                    records = [r for r in records if len(r) == mode_count]
                    if len(records) > 10:
                        df = pd.DataFrame(records)
                        return df
        except:
            pass

        return None

    def search_and_navigate(self, dataset_name: str, domain: str,
                           target_description: str) -> NavigationResult:
        """
        Search for a dataset and navigate to find actual data.

        1. Search for dataset landing page
        2. Analyze HTML to find download links
        3. Follow links until we find actual data
        """
        self._log(f"Searching for: {dataset_name}")
        self.visited.clear()
        path = []

        # Step 1: Search for landing page
        search_queries = [
            f"{dataset_name} download data CSV",
            f"{dataset_name} {domain} data access",
            f'"{dataset_name}" download site:gov'
        ]

        landing_pages = []
        for query in search_queries:
            try:
                response = self.session.post(
                    "https://html.duckduckgo.com/html/",
                    data={"q": query},
                    timeout=15
                )
                if response.ok:
                    pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"'
                    for match in re.findall(pattern, response.text)[:5]:
                        if "uddg=" in match:
                            url_match = re.search(r'uddg=([^&]+)', match)
                            if url_match:
                                landing_pages.append(requests.utils.unquote(url_match.group(1)))
                        else:
                            landing_pages.append(match)
                    if landing_pages:
                        break
            except Exception as e:
                self._log(f"Search error: {e}")
                continue

        if not landing_pages:
            return NavigationResult(False, "", None, [], "No landing pages found")

        # Step 2: Navigate from landing pages
        for landing_url in landing_pages[:3]:
            self._log(f"Exploring: {landing_url[:60]}...")
            result = self._navigate_page(landing_url, target_description, path, depth=0)
            if result.success:
                return result

        return NavigationResult(False, "", None, path, "Could not find data files")

    def _navigate_page(self, url: str, target: str, path: List[str],
                       depth: int) -> NavigationResult:
        """Recursively navigate a page to find data."""
        if depth > self.max_depth:
            return NavigationResult(False, url, None, path, "Max depth reached")

        if url in self.visited:
            return NavigationResult(False, url, None, path, "Already visited")

        self.visited.add(url)
        path.append(url)

        # Fetch page
        content = self._fetch(url)
        if not content:
            return NavigationResult(False, url, None, path, "Fetch failed")

        # Check if it's actual data
        if self._is_data_file(url, content):
            self._log(f"Found data file: {url[:60]}")
            df = self._parse_data(content)
            if df is not None:
                return NavigationResult(True, url, df, path, f"Found data: {len(df)} rows")

        # It's HTML - analyze for links
        html = content.decode('utf-8', errors='ignore')

        # Ask Legomena for relevant links
        candidate_urls = self._ask_legomena_for_links(html, target, url)
        self._log(f"Legomena suggested {len(candidate_urls)} links")

        # Try each candidate
        for candidate in candidate_urls:
            if candidate in self.visited:
                continue

            self._log(f"Trying: {candidate[:60]}...")

            # Quick check - try to fetch
            candidate_content = self._fetch(candidate)
            if not candidate_content:
                continue

            # Check if it's data
            if self._is_data_file(candidate, candidate_content):
                df = self._parse_data(candidate_content)
                if df is not None:
                    path.append(candidate)
                    return NavigationResult(True, candidate, df, path, f"Found data: {len(df)} rows")

            # If it's HTML, recurse (but limit depth)
            if depth < 2:  # Only go 2 levels deep
                result = self._navigate_page(candidate, target, path, depth + 1)
                if result.success:
                    return result

        return NavigationResult(False, url, None, path, "No data found on this page")

    def navigate_known_pattern(self, base_url: str, target: str) -> NavigationResult:
        """Navigate a known data directory structure."""
        self._log(f"Browsing directory: {base_url}")
        self.visited.clear()

        return self._navigate_page(base_url, target, [], depth=0)


    def navigate_from_landing_page(self, landing_url: str, target: str,
                                     file_pattern: str = None) -> NavigationResult:
        """
        Navigate from a known landing page to find data.

        More reliable than web search - starts from authoritative source.
        """
        self._log(f"Starting from: {landing_url}")
        path = [landing_url]

        # Fetch landing page
        content = self._fetch(landing_url)
        if not content:
            return NavigationResult(False, landing_url, None, path, "Could not fetch landing page")

        html = content.decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')

        # Look for data links (CSV, data, download, access)
        data_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip().lower()
            href_lower = href.lower()

            # Prioritize CSV/data links
            score = 0
            if 'csv' in text or 'csv' in href_lower:
                score += 10
            if 'data' in text or 'data' in href_lower:
                score += 5
            if 'download' in text or 'download' in href_lower:
                score += 5
            if 'access' in text or 'access' in href_lower:
                score += 3

            if score > 0:
                full_url = urljoin(landing_url, href)
                data_links.append((score, full_url, text))

        # Sort by score
        data_links.sort(reverse=True)
        self._log(f"Found {len(data_links)} data-related links")

        # Try top links
        for score, link_url, text in data_links[:5]:
            self._log(f"Trying: {text[:30]}... ({link_url[:50]})")

            content = self._fetch(link_url)
            if not content:
                continue

            # Check if it's a directory listing
            html = content.decode('utf-8', errors='ignore')
            if '<html' in html.lower():
                soup = BeautifulSoup(html, 'html.parser')

                # Look for CSV files
                csv_links = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.endswith('.csv') or href.endswith('.txt'):
                        full = urljoin(link_url, href)
                        csv_links.append(full)

                if csv_links:
                    self._log(f"Found {len(csv_links)} data files")

                    # Pick best file (or use pattern)
                    chosen = csv_links[0]
                    if file_pattern:
                        matches = [l for l in csv_links if file_pattern in l]
                        if matches:
                            chosen = matches[0]

                    # Download
                    self._log(f"Downloading: {chosen.split('/')[-1]}")
                    data_content = self._fetch(chosen)
                    if data_content:
                        df = self._parse_data(data_content)
                        if df is not None:
                            path.append(link_url)
                            path.append(chosen)
                            return NavigationResult(
                                True, chosen, df, path,
                                f"Found data: {len(df)} rows, {len(df.columns)} columns"
                            )

            else:
                # Direct data file
                df = self._parse_data(content)
                if df is not None:
                    path.append(link_url)
                    return NavigationResult(
                        True, link_url, df, path,
                        f"Found data: {len(df)} rows"
                    )

        return NavigationResult(False, landing_url, None, path, "Could not find data files")


def test_navigator():
    """Test the navigator on hurricane data."""
    nav = HermesNavigator()

    print("="*70)
    print("HERMES NAVIGATOR TEST")
    print("="*70)

    # Test 1: Navigate from known landing page
    print("\nTest 1: Navigate from IBTrACS landing page")
    result = nav.navigate_from_landing_page(
        landing_url="https://www.ncei.noaa.gov/products/international-best-track-archive",
        target="hurricane best track data with eye diameter",
        file_pattern=".NA."  # North Atlantic
    )

    print(f"\nResult:")
    print(f"  Success: {result.success}")
    print(f"  URL: {result.url}")
    print(f"  Path: {' -> '.join([p.split('/')[-1][:30] for p in result.path_taken])}")
    print(f"  Description: {result.description}")

    if result.data is not None:
        print(f"\n  Data preview:")
        print(f"    Rows: {len(result.data)}")
        print(f"    Columns: {list(result.data.columns)[:8]}...")

        # Check for eye/RMW
        eye_cols = [c for c in result.data.columns if 'eye' in str(c).lower()]
        rmw_cols = [c for c in result.data.columns if 'rmw' in str(c).lower()]
        print(f"    Eye columns: {eye_cols}")
        print(f"    RMW columns: {rmw_cols}")


if __name__ == "__main__":
    test_navigator()
