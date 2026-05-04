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

            links.append({
                "url": full_url,
                "text": text,
                "is_data": any(ext in href.lower() for ext in ['.csv', '.txt', '.json', '.nc'])
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

    def tool_parse(self, content: bytes) -> Optional[pd.DataFrame]:
        """Parse data content."""
        try:
            # Try CSV with header skip (common for scientific data)
            df = pd.read_csv(io.BytesIO(content), skiprows=[1], low_memory=False, na_values=[' ', ''])
            if len(df) > 100 and len(df.columns) > 5:
                return df
        except:
            pass

        try:
            df = pd.read_csv(io.BytesIO(content), low_memory=False)
            if len(df) > 100:
                return df
        except:
            pass

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
        self._log(f"HERMES EXPLORER")
        self._log(f"Topic: {topic}")
        self._log(f"Domain: {domain}")
        self._log(f"Looking for: {quantities}")
        self._log(f"{'='*60}\n")

        self.steps = []
        self.visited = set()

        # Step 1: Ask about data sources
        self._log("--- Step 1: Identify Data Sources ---")
        sources_question = f"What are the main scientific databases for {domain} that would have {', '.join(quantities[:3])}? List database names."

        sources_response = self.tool_ask(sources_question)
        self._log(f"Legomena says: {sources_response[:200]}...")

        # Extract database names
        database_names = re.findall(r'\b([A-Z][A-Z0-9\-]{2,}[A-Za-z0-9]*)\b', sources_response)
        database_names = [d for d in database_names if d not in ['CSV', 'JSON', 'API', 'URL', 'HTTP']]
        self._log(f"Databases identified: {database_names[:5]}")

        # Step 2: Search for data portals
        self._log("\n--- Step 2: Search for Data Portals ---")

        search_queries = [
            f"{topic} official data download",
            f"{domain} scientific data portal",
        ]

        # Add database-specific searches
        for db in database_names[:3]:
            search_queries.append(f"{db} official data download")

        all_results = []
        for query in search_queries[:4]:
            results = self.tool_search(query)
            all_results.extend(results)

            if len(all_results) >= 10:
                break

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

        # Prefer .gov, .edu, and known scientific domains
        def score_result(r):
            url = r['url'].lower()
            score = 0
            if '.gov' in url:
                score += 10
            if '.edu' in url:
                score += 8
            if any(org in url for org in ['noaa', 'nasa', 'esa', 'cern', 'ncei']):
                score += 15
            if 'data' in url:
                score += 5
            return score

        unique_results.sort(key=score_result, reverse=True)

        for r in unique_results[:5]:
            self._log(f"  {r['title'][:40]}: {r['url'][:50]}")

        # Step 4: Explore top portals
        self._log("\n--- Step 4: Explore Portals ---")

        for result in unique_results[:5]:
            portal_url = result['url']
            self._log(f"\nExploring: {portal_url[:60]}")

            html = self.tool_fetch(portal_url)
            if not html:
                continue

            # Find data links
            data_links = self.tool_extract_links(
                html, portal_url,
                filter_terms=['data', 'csv', 'download', 'access', 'dataset']
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

            # Try data links
            for link in data_links[:5]:
                link_url = link['url']

                if link['is_data']:
                    # Direct data file
                    content = self.tool_download(link_url)
                    if content:
                        df = self.tool_parse(content)
                        if df is not None:
                            self._log(f"  SUCCESS: {len(df)} rows!")
                            return DataDiscovery(
                                success=True,
                                url=link_url,
                                data=df,
                                steps=self.steps,
                                description=f"Found data via {portal_url}"
                            )

                else:
                    # Navigate deeper
                    sub_html = self.tool_fetch(link_url)
                    if not sub_html:
                        continue

                    sub_links = self.tool_extract_links(sub_html, link_url, filter_terms=['.csv', '.txt'])

                    for sub_link in sub_links[:5]:
                        if sub_link['is_data']:
                            content = self.tool_download(sub_link['url'])
                            if content:
                                df = self.tool_parse(content)
                                if df is not None:
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
