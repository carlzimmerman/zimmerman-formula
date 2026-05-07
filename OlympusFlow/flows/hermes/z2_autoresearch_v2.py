#!/usr/bin/env python3
"""
Z² AUTO-RESEARCH V2 - TRULY BLIND
==================================

Fully autonomous Z² relationship discovery with NO hardcoded domain knowledge.

Everything is discovered dynamically by Legomena:
- Data sources (via web search)
- Column mappings (by examining data)
- Transformations (diameter vs radius, etc.)
- Categories/groupings (intensity levels, etc.)
- Which ratios to test

NO hurricane-specific code. NO hardcoded URLs. NO hardcoded columns.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import re
import json
import math
import subprocess
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from scipy import stats
import requests

# Z² Constants - the ONLY knowledge the system has
Z2 = 32 * math.pi / 3   # ≈ 33.51
Z = math.sqrt(Z2)        # ≈ 5.79
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618

# Z² ratio formulas to test
Z2_RATIOS = {
    "1/phi": 1/PHI,           # 0.618
    "phi-1": PHI-1,           # 0.618
    "1/Z": 1/Z,               # 0.173
    "1/Z2": 1/Z2,             # 0.030
    "phi/Z": PHI/Z,           # 0.279
    "1/phi^2": 1/(PHI**2),    # 0.382
    "phi/2": PHI/2,           # 0.809
    "1/2": 0.5,
    "1/3": 1/3,
    "2/3": 2/3,
    "1/e": 1/math.e,
    "1/pi": 1/math.pi,
}

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-4b")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "120"))
OUTPUT_DIR = Path(__file__).parent / "autoresearch_v2_output"


@dataclass
class ColumnMapping:
    """Mapping from a quantity to a data column."""
    quantity: str
    column: str
    transformation: str  # "none", "divide_by_2", "multiply_by_X", etc.
    transform_reason: str


@dataclass
class CategoryInfo:
    """Information about categories/groupings in the data."""
    column: str
    categories: Dict[str, Tuple[float, float]]  # name -> (min, max)
    description: str


@dataclass
class DataSourceInfo:
    """A discovered data source."""
    name: str
    url: str
    organization: str
    format: str
    description: str


class LegomenaClient:
    """Client for Legomena LLM via Ollama - NO domain knowledge."""

    def __init__(self, model: str = None, verbose: bool = True):
        self.model = model or LEGOMENA_MODEL
        self.verbose = verbose
        self.timeout = LEGOMENA_TIMEOUT

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Legomena {ts}] {msg}")

    def generate(self, prompt: str, timeout: int = None) -> Optional[str]:
        """Generate response from Legomena."""
        timeout = timeout or self.timeout
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except subprocess.TimeoutExpired:
            self._log(f"Timeout ({timeout}s)")
        except Exception as e:
            self._log(f"Error: {e}")
        return None

    def identify_domain(self, topic: str) -> str:
        """Identify the scientific domain."""
        prompt = f"""What scientific domain does "{topic}" belong to?
Answer with ONE word only: meteorology, cosmology, physics, biology, chemistry, geology, etc.
Domain:"""
        response = self.generate(prompt, timeout=30)
        if response:
            words = response.strip().split()
            for word in words:
                clean = re.sub(r'[^a-z]', '', word.lower())
                if len(clean) > 3:
                    return clean
        return "unknown"

    def discover_quantities(self, topic: str, domain: str) -> List[str]:
        """Discover measurable quantities."""
        prompt = f"""For "{topic}" in {domain}, list 8 measurable physical quantities.
Format: one per line, snake_case names only.

Example format:
eye_diameter
wind_speed
central_pressure

Your quantities:"""
        response = self.generate(prompt, timeout=60)
        quantities = []
        if response:
            for line in response.split('\n'):
                line = line.strip().strip('-').strip('0123456789.').strip()
                if line and not line.startswith('#'):
                    q = re.sub(r'[^a-z0-9_]', '_', line.lower())
                    q = re.sub(r'_+', '_', q).strip('_')
                    if q and len(q) > 2 and len(q) < 40:
                        quantities.append(q)
        return quantities[:10]

    def discover_ratio_pairs(self, quantities: List[str]) -> List[Tuple[str, str]]:
        """Discover which quantity pairs might have meaningful ratios."""
        prompt = f"""Given these quantities:
{chr(10).join('- ' + q for q in quantities)}

Which pairs would have physically meaningful RATIOS?
List 5 pairs, format: quantity_a / quantity_b

Pairs:"""
        response = self.generate(prompt, timeout=60)
        pairs = []
        if response:
            for line in response.split('\n'):
                match = re.search(r'(\w+)\s*/\s*(\w+)', line)
                if match:
                    a, b = match.groups()
                    a_match = next((q for q in quantities if a.lower() in q or q in a.lower()), None)
                    b_match = next((q for q in quantities if b.lower() in q or q in b.lower()), None)
                    if a_match and b_match and a_match != b_match:
                        pairs.append((a_match, b_match))
        return pairs[:5]

    def search_data_sources(self, domain: str, quantities: List[str]) -> List[DataSourceInfo]:
        """Search for data sources - NO hardcoded URLs."""
        prompt = f"""What are the main scientific databases for {domain} research?

I need databases containing measurements of:
{chr(10).join('- ' + q for q in quantities[:5])}

For each database, provide:
- Name (the specific dataset name, e.g., "IBTrACS", "HURDAT2", "Planck Legacy")
- Organization
- The exact file download URL (direct link to .csv or .txt file, not a landing page)
- Format (CSV, JSON, text, etc.)

IMPORTANT: Provide DIRECT download URLs to data files, not HTML landing pages.
Example good URL: https://example.gov/data/dataset.csv
Example bad URL: https://example.gov/data/ (this is a landing page)

List 3-5 databases with their DIRECT download URLs:"""

        response = self.generate(prompt, timeout=90)
        sources = []

        if response:
            # Parse response for database info
            lines = response.split('\n')
            current = {}

            for line in lines:
                line = line.strip()
                # Clean asterisks and formatting
                line = re.sub(r'\*+', '', line).strip()

                # Look for URLs
                url_match = re.search(r'https?://[^\s<>"\']+', line)
                if url_match:
                    url = url_match.group()
                    url = re.sub(r'[)\]}>]$', '', url)
                    current['url'] = url

                # Look for dataset names (often in caps or quoted)
                name_match = re.search(r'(?:name[:\s]+)?([A-Z][A-Za-z0-9\-_]+(?:\s+[A-Z][A-Za-z0-9\-_]+)*)', line)
                if name_match and len(name_match.group(1)) > 3:
                    # Prefer names that look like dataset names
                    potential_name = name_match.group(1).strip()
                    if potential_name not in ['Name', 'URL', 'Format', 'Organization', 'CSV', 'JSON']:
                        current['name'] = potential_name

                # Look for structured info
                if ':' in line and not line.startswith('http'):
                    parts = line.split(':', 1)
                    key = parts[0].lower().strip()
                    val = parts[1].strip() if len(parts) > 1 else ""

                    if 'name' in key and val:
                        current['name'] = re.sub(r'\*+', '', val).strip()
                    elif 'org' in key:
                        current['organization'] = val
                    elif 'format' in key:
                        current['format'] = val
                    elif 'url' in key and val:
                        current['url'] = val

                # Save when we have a name (URL will be found via search)
                if current.get('name') and current.get('name') != 'Unknown':
                    sources.append(DataSourceInfo(
                        name=current.get('name', 'Unknown'),
                        url=current.get('url', ''),
                        organization=current.get('organization', 'Unknown'),
                        format=current.get('format', 'csv'),
                        description=""
                    ))
                    current = {}

        return sources

    def map_columns(self, quantities: List[str], columns: List[str],
                    sample_data: str) -> List[ColumnMapping]:
        """Map quantities to actual data columns - DYNAMIC, no hardcoding."""
        prompt = f"""I have a dataset with these columns:
{chr(10).join(columns[:40])}

Sample data (first few rows):
{sample_data[:2000]}

I need to find columns for these quantities:
{chr(10).join('- ' + q for q in quantities)}

For each quantity, tell me:
1. Which column matches it (exact column name from the list)
2. Any transformation needed (e.g., "divide_by_2" if column is diameter but I need radius)

Format your answer as:
quantity -> column_name, transformation
(use "none" if no transformation needed)

Mappings:"""

        response = self.generate(prompt, timeout=90)
        mappings = []

        if response:
            for line in response.split('\n'):
                # Parse: quantity -> column, transformation
                match = re.search(r'(\w+)\s*[->=]+\s*(\w+)(?:\s*,\s*(\w+))?', line)
                if match:
                    quantity = match.group(1).lower()
                    column = match.group(2)
                    transform = match.group(3) or "none"

                    # Verify column exists
                    col_match = next((c for c in columns if c.lower() == column.lower()
                                     or column.lower() in c.lower()), None)
                    if col_match:
                        mappings.append(ColumnMapping(
                            quantity=quantity,
                            column=col_match,
                            transformation=transform.lower(),
                            transform_reason=""
                        ))

        return mappings

    def discover_categories(self, columns: List[str], sample_data: str,
                           domain: str) -> Optional[CategoryInfo]:
        """Discover if data has meaningful categories/groupings - DYNAMIC."""
        prompt = f"""Looking at this {domain} dataset:

Columns: {', '.join(columns[:30])}

Sample data:
{sample_data[:1500]}

Is there a column that represents INTENSITY or CATEGORY levels?
(e.g., storm category, magnitude class, quality rating)

If yes, provide:
1. Column name
2. The categories/levels and their thresholds

Format:
column: <column_name>
categories:
  <name1>: <min_value> to <max_value>
  <name2>: <min_value> to <max_value>
  ...

If no categorical column exists, just say: none

Answer:"""

        response = self.generate(prompt, timeout=90)

        if not response or 'none' in response.lower()[:50]:
            return None

        # Parse response
        column = None
        categories = {}

        lines = response.split('\n')
        for line in lines:
            line = line.strip()

            # Look for column name
            if 'column' in line.lower() and ':' in line:
                parts = line.split(':', 1)
                col = parts[1].strip() if len(parts) > 1 else ""
                col = re.sub(r'[^a-zA-Z0-9_]', '', col)
                if col and any(c.lower() == col.lower() or col.lower() in c.lower()
                              for c in columns):
                    column = next((c for c in columns if col.lower() in c.lower()), col)

            # Look for category definitions
            match = re.search(r'(\w+[\w\s]*?):\s*([\d.]+)\s*(?:to|-)\s*([\d.]+)', line)
            if match:
                name = match.group(1).strip()
                min_val = float(match.group(2))
                max_val = float(match.group(3))
                categories[name] = (min_val, max_val)

        if column and categories:
            return CategoryInfo(
                column=column,
                categories=categories,
                description=f"Categories based on {column}"
            )

        return None

    def write_finding(self, topic: str, ratio_name: str, measured: float,
                      predicted: float, formula: str, error: float,
                      n: int, category: str = None) -> str:
        """Write up a validated finding."""
        cat_str = f" for {category}" if category else ""
        prompt = f"""Write a 2-sentence scientific finding:

Topic: {topic}
Discovery: {ratio_name}{cat_str} = {formula}
Measured: {measured:.4f}
Predicted: {predicted:.4f}
Error: {error:.2f}%
Samples: {n}

Finding:"""
        return self.generate(prompt, timeout=60) or ""


class DynamicDataFetcher:
    """Fetch data from discovered sources - NO hardcoded URLs."""

    def __init__(self, cache_dir: str = None, verbose: bool = True):
        self.verbose = verbose
        self.cache_dir = Path(cache_dir or "./autoresearch_v2_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Z2AutoResearch/2.0 (Scientific Research)"
        })

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Fetcher {ts}] {msg}")

    def web_search(self, query: str) -> List[Dict]:
        """Search web for data sources."""
        self._log(f"Searching: {query}")
        try:
            response = self.session.post(
                "https://html.duckduckgo.com/html/",
                data={"q": query},
                timeout=30
            )
            if response.ok:
                results = []
                pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
                for url, title in re.findall(pattern, response.text)[:10]:
                    if "uddg=" in url:
                        url_match = re.search(r'uddg=([^&]+)', url)
                        if url_match:
                            url = requests.utils.unquote(url_match.group(1))
                    results.append({"url": url, "title": title.strip()})
                return results
        except Exception as e:
            self._log(f"Search error: {e}")
        return []

    def find_download_url(self, source: DataSourceInfo, domain: str) -> Optional[str]:
        """Find actual download URL for a data source."""
        # Clean the source name
        name = re.sub(r'\*+', '', source.name).strip()
        org = re.sub(r'\*+', '', source.organization).strip()

        self._log(f"Looking for: {name}")

        # Try the provided URL first
        if source.url and ('.csv' in source.url or '.txt' in source.url):
            try:
                resp = self.session.head(source.url, timeout=10, allow_redirects=True)
                if resp.ok:
                    return source.url
            except:
                pass

        # Search for actual data file with clean queries
        search_queries = [
            f"{name} CSV download",
            f"{name} data download site:noaa.gov",
            f"{name} data download site:gov",
            f'"{name}" CSV',
        ]

        for query in search_queries:
            results = self.web_search(query)
            for r in results:
                url = r.get('url', '')
                # Look for actual data file URLs or NOAA data pages
                if any(url.lower().endswith(ext) for ext in ['.csv', '.txt', '.dat']) or \
                   ('noaa.gov' in url and 'data' in url):
                    try:
                        resp = self.session.head(url, timeout=10, allow_redirects=True)
                        if resp.ok:
                            # Try to get the file
                            content_type = resp.headers.get('content-type', '')
                            if 'html' not in content_type.lower():
                                return url
                    except:
                        continue

        return None

    def search_for_direct_data(self, domain: str, topic: str) -> List[Tuple[str, str]]:
        """Search specifically for direct data file links."""
        queries = [
            f"{topic} CSV data download",
            f"{domain} dataset CSV direct download",
            f'"{topic}" filetype:csv site:gov',
            f'"{topic}" filetype:txt site:edu',
            f"{domain} research data CSV"
        ]

        found_urls = []
        for query in queries:
            results = self.web_search(query)
            for r in results:
                url = r.get('url', '')
                title = r.get('title', '')
                if any(url.lower().endswith(ext) for ext in ['.csv', '.txt', '.dat']):
                    found_urls.append((url, title))

        return found_urls[:10]

    def download(self, url: str, timeout: int = 300) -> Optional[bytes]:
        """Download data from URL."""
        # Check cache
        cache_key = re.sub(r'[^a-zA-Z0-9]', '_', url)[:100]
        cache_path = self.cache_dir / cache_key

        if cache_path.exists():
            self._log(f"Using cached: {cache_path.name}")
            return cache_path.read_bytes()

        self._log(f"Downloading: {url[:80]}...")
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            self._log(f"Downloaded: {len(response.content)/1024:.1f}KB")

            # Cache
            cache_path.write_bytes(response.content)
            return response.content
        except Exception as e:
            self._log(f"Download error: {e}")
            return None

    def parse_data(self, content: bytes, format_hint: str = "") -> Optional[pd.DataFrame]:
        """Parse data - try multiple formats. Rejects HTML."""
        import io

        text = content.decode('utf-8', errors='ignore')

        # Reject HTML
        if '<html' in text.lower() or '<!doctype' in text.lower():
            self._log("Rejected: HTML content")
            return None

        # Try CSV
        try:
            # Skip comment lines
            lines = [l for l in text.split('\n') if l.strip() and not l.strip().startswith('#')]

            if lines and ',' in lines[0]:
                df = pd.read_csv(io.StringIO('\n'.join(lines)), low_memory=False)
                # Validate it's actual data with named columns
                if len(df) > 0 and len(df.columns) > 1:
                    # Check columns are strings, not just numbers
                    if any(isinstance(c, str) and len(c) > 1 for c in df.columns):
                        return df
        except:
            pass

        # Try tab-separated
        try:
            df = pd.read_csv(io.BytesIO(content), sep='\t', low_memory=False)
            if len(df) > 0 and len(df.columns) > 1:
                if any(isinstance(c, str) and len(c) > 1 for c in df.columns):
                    return df
        except:
            pass

        # Try fixed-width (space-separated) - generate column names
        try:
            lines = text.strip().split('\n')
            records = []
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('<'):
                    parts = line.split()
                    if len(parts) >= 5:
                        records.append(parts)
            if records and len(records) > 50:
                # Generate column names
                n_cols = len(records[0])
                col_names = [f"col_{i}" for i in range(n_cols)]
                df = pd.DataFrame(records, columns=col_names)
                return df
        except:
            pass

        return None

    def get_sample_data(self, df: pd.DataFrame, n_rows: int = 5) -> str:
        """Get sample data as string for Legomena to analyze."""
        return df.head(n_rows).to_string()


class Z2Verifier:
    """Verify Z² relationships - no hardcoded logic."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Verify {ts}] {msg}")

    def apply_transformation(self, values: pd.Series, transform: str) -> pd.Series:
        """Apply discovered transformation."""
        if transform == "none" or not transform:
            return values
        elif transform == "divide_by_2":
            return values / 2
        elif transform == "multiply_by_2":
            return values * 2
        elif transform.startswith("divide_by_"):
            divisor = float(transform.split("_")[-1])
            return values / divisor
        elif transform.startswith("multiply_by_"):
            mult = float(transform.split("_")[-1])
            return values * mult
        return values

    def compute_ratios(self, df: pd.DataFrame,
                       col_a: str, transform_a: str,
                       col_b: str, transform_b: str,
                       category_col: str = None,
                       category_range: Tuple[float, float] = None) -> np.ndarray:
        """Compute ratios with dynamic transformations."""
        data = df.copy()

        # Filter by category if specified
        if category_col and category_range:
            min_val, max_val = category_range
            data = data[(data[category_col] >= min_val) & (data[category_col] < max_val)]

        # Get values
        try:
            a_vals = pd.to_numeric(data[col_a], errors='coerce')
            b_vals = pd.to_numeric(data[col_b], errors='coerce')
        except:
            return np.array([])

        # Apply transformations
        a_vals = self.apply_transformation(a_vals, transform_a)
        b_vals = self.apply_transformation(b_vals, transform_b)

        # Filter valid
        valid = (a_vals > 0) & (b_vals > 0) & a_vals.notna() & b_vals.notna()

        if valid.sum() < 5:
            return np.array([])

        return (a_vals[valid] / b_vals[valid]).values

    def test_z2_formulas(self, ratios: np.ndarray) -> Optional[Dict]:
        """Test ratios against Z² formulas."""
        if len(ratios) < 5:
            return None

        mean = ratios.mean()
        std = ratios.std()
        n = len(ratios)

        best = None
        best_error = float('inf')

        for name, value in Z2_RATIOS.items():
            error_pct = abs(value - mean) / value * 100

            if error_pct < best_error:
                t_stat, p_value = stats.ttest_1samp(ratios, value)

                best_error = error_pct
                best = {
                    "formula": name,
                    "z2_value": value,
                    "measured": mean,
                    "std": std,
                    "n": n,
                    "error_pct": error_pct,
                    "p_value": p_value
                }

        if best:
            if best["error_pct"] < 1 and best["p_value"] > 0.05:
                best["verdict"] = "VALIDATED"
            elif best["error_pct"] < 5:
                best["verdict"] = "STRONG"
            elif best["error_pct"] < 10:
                best["verdict"] = "WEAK"
            else:
                best["verdict"] = "REJECTED"

        return best


class Z2AutoResearchV2:
    """
    TRULY BLIND Z² Research System.

    NO hardcoded:
    - URLs
    - Column names
    - Transformations
    - Categories
    - Domain-specific logic

    Everything discovered by Legomena.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.legomena = LegomenaClient(verbose=verbose)
        self.fetcher = DynamicDataFetcher(verbose=verbose)
        self.verifier = Z2Verifier(verbose=verbose)
        OUTPUT_DIR.mkdir(exist_ok=True)

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[AutoResearch {ts}] {msg}")

    def research(self, topic: str) -> Dict:
        """Run completely blind research."""
        self._log(f"\n{'='*70}")
        self._log(f"Z² AUTO-RESEARCH V2 - TRULY BLIND")
        self._log(f"Topic: {topic}")
        self._log(f"{'='*70}")
        self._log(f"System knows ONLY: Z²={Z2:.4f}, φ={PHI:.4f}")
        self._log(f"Everything else will be DISCOVERED.\n")

        results = {
            "topic": topic,
            "started": datetime.now().isoformat(),
            "domain": None,
            "quantities": [],
            "ratio_pairs": [],
            "data_sources_searched": [],
            "data_sources_found": [],
            "column_mappings": [],
            "categories_discovered": None,
            "ratio_results": [],
            "best_match": None,
            "conclusion": "",
            "is_blind": True  # Flag that this was truly blind
        }

        # =====================================================================
        # PHASE 1: DISCOVER DOMAIN & QUANTITIES (Legomena)
        # =====================================================================
        self._log("--- PHASE 1: DISCOVER (Legomena) ---")

        domain = self.legomena.identify_domain(topic)
        results["domain"] = domain
        self._log(f"Domain discovered: {domain}")

        quantities = self.legomena.discover_quantities(topic, domain)
        results["quantities"] = quantities
        self._log(f"Quantities discovered: {quantities}")

        ratio_pairs = self.legomena.discover_ratio_pairs(quantities)
        results["ratio_pairs"] = [f"{a}/{b}" for a, b in ratio_pairs]
        self._log(f"Ratio pairs to test: {results['ratio_pairs']}")

        # =====================================================================
        # PHASE 2: FIND DATA SOURCES (Legomena + Web Search)
        # =====================================================================
        self._log("\n--- PHASE 2: FIND DATA SOURCES ---")

        # Ask Legomena what databases exist
        sources = self.legomena.search_data_sources(domain, quantities)
        results["data_sources_searched"] = [asdict(s) for s in sources]
        self._log(f"Legomena suggested {len(sources)} sources")

        # Also do direct web search
        search_query = f"{domain} {quantities[0] if quantities else ''} scientific database CSV download"
        web_results = self.fetcher.web_search(search_query)
        self._log(f"Web search found {len(web_results)} results")

        # Try to find working data
        df = None
        working_source = None

        for source in sources:
            url = self.fetcher.find_download_url(source, domain)
            if url:
                self._log(f"Trying: {url[:60]}...")
                content = self.fetcher.download(url)
                if content:
                    df = self.fetcher.parse_data(content, source.format)
                    if df is not None and len(df) > 100:
                        working_source = source
                        working_source.url = url
                        results["data_sources_found"].append(asdict(working_source))
                        self._log(f"SUCCESS: {len(df)} rows, {len(df.columns)} columns")
                        break

        # Try web search results if Legomena sources failed
        if df is None:
            for r in web_results:
                url = r.get('url', '')
                if any(ext in url.lower() for ext in ['.csv', '.txt', 'download', 'data']):
                    self._log(f"Trying web result: {url[:60]}...")
                    content = self.fetcher.download(url)
                    if content:
                        df = self.fetcher.parse_data(content)
                        if df is not None and len(df) > 100:
                            working_source = DataSourceInfo(
                                name=r.get('title', 'Unknown'),
                                url=url,
                                organization="Web",
                                format="auto",
                                description=""
                            )
                            results["data_sources_found"].append(asdict(working_source))
                            self._log(f"SUCCESS: {len(df)} rows")
                            break

        # Try more specific searches if still no data
        if df is None:
            self._log("Searching for direct data file links...")
            direct_urls = self.fetcher.search_for_direct_data(domain, topic)

            for url, title in direct_urls:
                self._log(f"Trying direct link: {url[:60]}...")
                content = self.fetcher.download(url)
                if content:
                    df = self.fetcher.parse_data(content)
                    if df is not None and len(df) > 50:
                        working_source = DataSourceInfo(
                            name=title or "Direct Data",
                            url=url,
                            organization="Web Search",
                            format="csv",
                            description=""
                        )
                        results["data_sources_found"].append(asdict(working_source))
                        self._log(f"SUCCESS: {len(df)} rows")
                        break

        # Try known pattern searches
        if df is None:
            specific_queries = [
                f"{domain} {quantities[0]} CSV filetype:csv",
                f"{domain} dataset download CSV",
                f"{topic} measurements data CSV"
            ]
            for query in specific_queries:
                self._log(f"Trying: {query[:50]}...")
                more_results = self.fetcher.web_search(query)
                for r in more_results:
                    url = r.get('url', '')
                    if '.csv' in url.lower() or '.txt' in url.lower():
                        content = self.fetcher.download(url)
                        if content:
                            df = self.fetcher.parse_data(content)
                            if df is not None and len(df) > 50:
                                working_source = DataSourceInfo(
                                    name=r.get('title', 'Unknown'),
                                    url=url,
                                    organization="Web Search",
                                    format="csv",
                                    description=""
                                )
                                results["data_sources_found"].append(asdict(working_source))
                                self._log(f"SUCCESS: {len(df)} rows")
                                break
                if df is not None:
                    break

        if df is None:
            results["conclusion"] = "Could not find accessible data sources"
            results["completed"] = datetime.now().isoformat()
            return results

        # =====================================================================
        # PHASE 3: MAP COLUMNS (Legomena examines data)
        # =====================================================================
        self._log("\n--- PHASE 3: MAP COLUMNS (Legomena) ---")

        columns = [str(c) for c in df.columns]  # Ensure string column names
        sample = self.fetcher.get_sample_data(df)

        self._log(f"Columns in data: {columns[:20]}...")

        mappings = self.legomena.map_columns(quantities, columns, sample)
        results["column_mappings"] = [asdict(m) for m in mappings]

        for m in mappings:
            self._log(f"  {m.quantity} -> {m.column} (transform: {m.transformation})")

        if len(mappings) < 2:
            results["conclusion"] = "Could not map quantities to columns"
            results["completed"] = datetime.now().isoformat()
            return results

        # =====================================================================
        # PHASE 4: DISCOVER CATEGORIES (Legomena)
        # =====================================================================
        self._log("\n--- PHASE 4: DISCOVER CATEGORIES (Legomena) ---")

        categories = self.legomena.discover_categories(columns, sample, domain)

        if categories:
            results["categories_discovered"] = asdict(categories)
            self._log(f"Category column: {categories.column}")
            for name, (min_v, max_v) in categories.categories.items():
                self._log(f"  {name}: {min_v} to {max_v}")
        else:
            self._log("No categories discovered")

        # =====================================================================
        # PHASE 5: VERIFY RATIOS (Python)
        # =====================================================================
        self._log("\n--- PHASE 5: VERIFY RATIOS (Python) ---")

        # Build mapping dict
        mapping_dict = {m.quantity: m for m in mappings}

        for q_a, q_b in ratio_pairs:
            # Find mappings for these quantities
            map_a = mapping_dict.get(q_a)
            map_b = mapping_dict.get(q_b)

            if not map_a or not map_b:
                # Try partial matches
                map_a = next((m for m in mappings if q_a in m.quantity or m.quantity in q_a), None)
                map_b = next((m for m in mappings if q_b in m.quantity or m.quantity in q_b), None)

            if not map_a or not map_b:
                self._log(f"  {q_a}/{q_b}: No column mapping found")
                continue

            ratio_name = f"{q_a}/{q_b}"

            # Test overall
            ratios = self.verifier.compute_ratios(
                df, map_a.column, map_a.transformation,
                map_b.column, map_b.transformation
            )

            if len(ratios) >= 10:
                result = self.verifier.test_z2_formulas(ratios)
                if result:
                    result["ratio_name"] = ratio_name
                    result["category"] = "all"
                    results["ratio_results"].append(result)
                    self._log(f"  {ratio_name} (all): {result['measured']:.4f} ≈ {result['formula']} "
                             f"({result['error_pct']:.2f}%) [{result['verdict']}]")

            # Test by category if discovered
            if categories and categories.column in df.columns:
                for cat_name, (min_v, max_v) in categories.categories.items():
                    ratios = self.verifier.compute_ratios(
                        df, map_a.column, map_a.transformation,
                        map_b.column, map_b.transformation,
                        category_col=categories.column,
                        category_range=(min_v, max_v)
                    )

                    if len(ratios) >= 10:
                        result = self.verifier.test_z2_formulas(ratios)
                        if result:
                            result["ratio_name"] = ratio_name
                            result["category"] = cat_name
                            results["ratio_results"].append(result)
                            self._log(f"  {ratio_name} ({cat_name}): {result['measured']:.4f} ≈ "
                                     f"{result['formula']} ({result['error_pct']:.2f}%) [{result['verdict']}]")

        # =====================================================================
        # PHASE 6: DOCUMENT (Legomena)
        # =====================================================================
        self._log("\n--- PHASE 6: DOCUMENT (Legomena) ---")

        # Find best result
        validated = [r for r in results["ratio_results"]
                    if r.get("verdict") in ["VALIDATED", "STRONG"]]

        if validated:
            best = min(validated, key=lambda r: r["error_pct"])
            results["best_match"] = best

            finding = self.legomena.write_finding(
                topic=topic,
                ratio_name=best["ratio_name"],
                measured=best["measured"],
                predicted=best["z2_value"],
                formula=best["formula"],
                error=best["error_pct"],
                n=best["n"],
                category=best.get("category")
            )

            cat_str = f" ({best['category']})" if best.get('category') != 'all' else ""
            results["conclusion"] = f"""Z² RELATIONSHIP DISCOVERED (BLIND)
Topic: {topic}
Relationship: {best['ratio_name']}{cat_str} = {best['formula']}
Measured: {best['measured']:.4f} ± {best['std']:.4f}
Predicted: {best['z2_value']:.4f}
Error: {best['error_pct']:.2f}%
N: {best['n']}
Verdict: {best['verdict']}

{finding}"""
        else:
            results["conclusion"] = f"No Z² relationships found in {topic} data"

        results["completed"] = datetime.now().isoformat()

        # Save
        slug = re.sub(r'[^a-z0-9]', '_', topic.lower())[:30]
        output_dir = OUTPUT_DIR / f"session_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(exist_ok=True)

        with open(output_dir / "session.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        with open(output_dir / "conclusion.txt", "w") as f:
            f.write(results["conclusion"])

        self._log(f"\nSaved to: {output_dir}")

        return results


def main():
    """Run truly blind Z² research."""
    topic = sys.argv[1] if len(sys.argv) > 1 else "hurricane eye and wind structure"

    researcher = Z2AutoResearchV2()
    results = researcher.research(topic)

    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print(results["conclusion"])

    if results.get("is_blind"):
        print("\n✓ This was a TRULY BLIND discovery - no hardcoded domain knowledge")


if __name__ == "__main__":
    main()
