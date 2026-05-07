#!/usr/bin/env python3
"""
HERMESFLOW - Firecrawl Search (Standalone)
==========================================

A lightweight Firecrawl-based web search module that doesn't require
the full hermes_agent dependencies. Used by ResearchBridge for
dynamic topic research.

Usage:
    from HermesFlow.firecrawl_search import FirecrawlSearcher

    searcher = FirecrawlSearcher()
    results = searcher.search("turbulence von Karman constant")
    content = searcher.extract_urls(["https://example.com"])

Environment Variables:
    FIRECRAWL_API_KEY or FIRECRAWL_ACCESS_TOKEN - Your Firecrawl API key

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

# Try to load from .env file
def _load_env():
    """Load environment variables from .env files."""
    env_paths = [
        Path("/Users/carlzimmerman/new_physics/.env"),
        Path.home() / ".env",
        Path.cwd() / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key and value:
                                os.environ.setdefault(key, value)
            except Exception:
                pass

_load_env()


def get_firecrawl_key() -> Optional[str]:
    """Get Firecrawl API key from environment."""
    return (
        os.environ.get("FIRECRAWL_API_KEY") or
        os.environ.get("FIRECRAWL_ACCESS_TOKEN") or
        None
    )


def is_firecrawl_available() -> bool:
    """Check if Firecrawl is configured."""
    return get_firecrawl_key() is not None


@dataclass
class SearchResult:
    """A web search result."""
    title: str
    url: str
    snippet: str
    score: float = 0.0


@dataclass
class ExtractedContent:
    """Extracted content from a URL."""
    url: str
    title: str
    content: str
    success: bool


class FirecrawlSearcher:
    """
    Lightweight Firecrawl-based web searcher.

    Provides:
    - search(): Web search for a query
    - extract_urls(): Extract content from URLs
    - scrape_url(): Scrape a single URL
    """

    BASE_URL = "https://api.firecrawl.dev/v1"

    def __init__(self, api_key: str = None, verbose: bool = True):
        """
        Initialize the searcher.

        Args:
            api_key: Firecrawl API key (or uses environment variable)
            verbose: Print progress messages
        """
        self.api_key = api_key or get_firecrawl_key()
        self.verbose = verbose

        if not self.api_key:
            self._log("Warning: No Firecrawl API key found")
            self._log("Set FIRECRAWL_API_KEY or FIRECRAWL_ACCESS_TOKEN environment variable")

    def _log(self, msg: str):
        if self.verbose:
            print(f"[FirecrawlSearch] {msg}")

    def _make_request(self, endpoint: str, method: str = "POST",
                      data: Dict = None) -> Dict:
        """Make HTTP request to Firecrawl API."""
        import urllib.request
        import urllib.error

        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if data:
            body = json.dumps(data).encode('utf-8')
        else:
            body = None

        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            self._log(f"HTTP Error {e.code}: {error_body[:200]}")
            return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            self._log(f"URL Error: {e.reason}")
            return {"success": False, "error": str(e.reason)}
        except Exception as e:
            self._log(f"Request error: {e}")
            return {"success": False, "error": str(e)}

    def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        """
        Search the web for a query.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of SearchResult objects
        """
        if not self.api_key:
            self._log("No API key - cannot search")
            return []

        self._log(f"Searching: {query}")

        data = {
            "query": query,
            "limit": limit,
            "scrapeOptions": {
                "formats": ["markdown"]
            }
        }

        response = self._make_request("search", data=data)

        results = []
        if response.get("success") and response.get("data"):
            for item in response["data"]:
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("description", item.get("markdown", "")[:500]),
                    score=item.get("score", 0.0)
                )
                results.append(result)
                self._log(f"  Found: {result.title[:50]}...")

        self._log(f"Found {len(results)} results")
        return results

    def scrape_url(self, url: str) -> ExtractedContent:
        """
        Scrape content from a single URL.

        Args:
            url: URL to scrape

        Returns:
            ExtractedContent object
        """
        if not self.api_key:
            return ExtractedContent(url=url, title="", content="", success=False)

        self._log(f"Scraping: {url}")

        data = {
            "url": url,
            "formats": ["markdown"]
        }

        response = self._make_request("scrape", data=data)

        if response.get("success") and response.get("data"):
            data = response["data"]
            return ExtractedContent(
                url=url,
                title=data.get("metadata", {}).get("title", ""),
                content=data.get("markdown", ""),
                success=True
            )

        return ExtractedContent(url=url, title="", content="", success=False)

    def extract_urls(self, urls: List[str]) -> List[ExtractedContent]:
        """
        Extract content from multiple URLs.

        Args:
            urls: List of URLs to extract

        Returns:
            List of ExtractedContent objects
        """
        results = []
        for url in urls[:5]:  # Limit to 5 URLs
            content = self.scrape_url(url)
            results.append(content)
        return results

    def search_and_extract(self, query: str, limit: int = 3) -> Tuple[List[SearchResult], List[ExtractedContent]]:
        """
        Search and extract content in one call.

        Args:
            query: Search query
            limit: Number of results to search and extract

        Returns:
            Tuple of (search_results, extracted_contents)
        """
        # Search
        search_results = self.search(query, limit=limit)

        # Extract top results
        urls = [r.url for r in search_results if r.url]
        extracted = self.extract_urls(urls[:limit])

        return search_results, extracted


# =============================================================================
# INTEGRATION WITH RESEARCH BRIDGE
# =============================================================================

def extract_constants_from_content(content: str, source_url: str = "") -> List[Dict]:
    """
    Extract numerical constants from scraped content.

    Uses regex patterns to find values like:
    - "0.41" (plain numbers)
    - "κ = 0.41" (Greek letters)
    - "2300" (integers)
    - "3/4" (fractions)
    - "0.41 ± 0.02" (with uncertainty)
    """
    constants = []

    # Patterns for extracting values
    patterns = [
        # Greek letter = value: "κ = 0.41"
        (r'([κλαβγδεζηθμξπρστφχψω])\s*[=≈]\s*(\d+\.?\d*)', 'greek'),
        # Named constant: "von Kármán constant is 0.41"
        (r'(constant|coefficient|number|ratio|exponent)\s+(?:is\s+)?(?:approximately\s+)?(\d+\.?\d*)', 'named'),
        # Value with uncertainty: "0.41 ± 0.02"
        (r'(\d+\.?\d*)\s*[±\+\-/]+\s*(\d+\.?\d*)', 'uncertainty'),
        # Simple decimal: "= 0.41" or "≈ 0.21"
        (r'[=≈]\s*(\d+\.?\d+)', 'equals'),
        # Fraction: "3/4" or "2/3"
        (r'\b(\d+)\s*/\s*(\d+)\b', 'fraction'),
    ]

    seen_values = set()

    for pattern, ptype in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            try:
                if ptype == 'greek':
                    name = f"Greek {match.group(1)}"
                    value = float(match.group(2))
                    uncertainty = value * 0.05
                elif ptype == 'named':
                    name = match.group(1)
                    value = float(match.group(2))
                    uncertainty = value * 0.05
                elif ptype == 'uncertainty':
                    value = float(match.group(1))
                    uncertainty = float(match.group(2))
                    name = f"value {value}"
                elif ptype == 'equals':
                    value = float(match.group(1))
                    uncertainty = value * 0.05
                    name = f"value {value}"
                elif ptype == 'fraction':
                    num = int(match.group(1))
                    denom = int(match.group(2))
                    if denom != 0 and num < 100 and denom < 100:
                        value = num / denom
                        uncertainty = 0.001
                        name = f"{num}/{denom}"
                    else:
                        continue
                else:
                    continue

                # Skip if we've seen this value (rounded)
                rounded = round(value, 4)
                if rounded in seen_values or rounded == 0:
                    continue
                seen_values.add(rounded)

                constants.append({
                    "name": name,
                    "value": value,
                    "uncertainty": uncertainty,
                    "source": source_url,
                })

            except (ValueError, IndexError):
                continue

    return constants


# =============================================================================
# TEST / CLI
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("FIRECRAWL SEARCH TEST")
    print("=" * 70)

    print(f"\nFirecrawl available: {is_firecrawl_available()}")
    print(f"API Key: {get_firecrawl_key()[:10] if get_firecrawl_key() else 'None'}...")

    if not is_firecrawl_available():
        print("\nNo API key found. Set FIRECRAWL_API_KEY or FIRECRAWL_ACCESS_TOKEN")
        sys.exit(1)

    query = sys.argv[1] if len(sys.argv) > 1 else "von Karman constant turbulence 0.41"

    print(f"\nSearching: {query}")
    print("-" * 70)

    searcher = FirecrawlSearcher()
    results = searcher.search(query, limit=3)

    print(f"\nFound {len(results)} results:")
    for r in results:
        print(f"  - {r.title}")
        print(f"    {r.url}")
        print(f"    {r.snippet[:100]}...")
        print()

    if results:
        print("-" * 70)
        print("Extracting content from first result...")
        content = searcher.scrape_url(results[0].url)
        if content.success:
            print(f"Title: {content.title}")
            print(f"Content length: {len(content.content)} chars")

            # Extract constants
            constants = extract_constants_from_content(content.content, content.url)
            print(f"\nExtracted {len(constants)} constants:")
            for c in constants[:10]:
                print(f"  {c['name']}: {c['value']}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
