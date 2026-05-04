#!/usr/bin/env python3
"""
HERMES DATA AGENT
=================

Autonomous data acquisition agent for Z² research.
NO Claude - uses only open source tools.

Components:
- Web search (DuckDuckGo)
- HTTP downloads (requests)
- Data parsing (pandas, custom parsers)
- File caching

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import io
import re
import json
import hashlib
import requests
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse, urljoin
import time


@dataclass
class DataSource:
    """A discovered data source."""
    name: str
    url: str
    organization: str
    format: str  # csv, json, netcdf, fixed-width, etc.
    description: str
    verified: bool = False


@dataclass
class ParsedDataset:
    """A parsed dataset ready for analysis."""
    source: DataSource
    data: pd.DataFrame
    columns_used: List[str]
    n_rows: int
    fetch_time: str


class HermesDataAgent:
    """
    Autonomous data acquisition agent.

    Capabilities:
    - Web search for data sources
    - Download files (with caching)
    - Parse multiple formats (CSV, JSON, fixed-width)
    - Verify URLs exist
    """

    def __init__(self, cache_dir: str = None, verbose: bool = True):
        self.verbose = verbose
        self.cache_dir = Path(cache_dir or "./hermes_cache")
        self.cache_dir.mkdir(exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HermesDataAgent/1.0 (Z2 Research; contact@example.com)"
        })

        # Known scientific data repositories
        self.known_repositories = {
            "noaa": {
                "base_url": "https://www.ncei.noaa.gov",
                "data_url": "https://www.ncei.noaa.gov/data",
                "ibtracs": "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/",
            },
            "cira": {
                "base_url": "https://rammb2.cira.colostate.edu",
                "ebtrk": "https://rammb2.cira.colostate.edu/research/tropical-cyclones/tc_extended_best_track_dataset/",
            },
            "planck": {
                "base_url": "https://pla.esac.esa.int",
                "wiki": "https://wiki.cosmos.esa.int/planck-legacy-archive/",
            },
            "pdg": {
                "base_url": "https://pdg.lbl.gov",
                "api": "https://pdg.lbl.gov/2024/",
            },
            "zenodo": {
                "base_url": "https://zenodo.org",
                "api": "https://zenodo.org/api/records/",
            }
        }

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Hermes {ts}] {msg}")

    def _cache_key(self, url: str) -> str:
        """Generate cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()

    def _get_cached(self, url: str) -> Optional[bytes]:
        """Get cached content if exists."""
        cache_path = self.cache_dir / self._cache_key(url)
        if cache_path.exists():
            self._log(f"Cache hit: {url[:60]}...")
            return cache_path.read_bytes()
        return None

    def _set_cached(self, url: str, content: bytes):
        """Cache content."""
        cache_path = self.cache_dir / self._cache_key(url)
        cache_path.write_bytes(content)

    # =========================================================================
    # WEB SEARCH
    # =========================================================================

    def web_search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search the web using DuckDuckGo.

        Returns list of {title, url, description}
        """
        self._log(f"Searching: {query}")

        try:
            # DuckDuckGo HTML search (no API key needed)
            url = "https://html.duckduckgo.com/html/"
            response = self.session.post(
                url,
                data={"q": query},
                timeout=30
            )

            if not response.ok:
                return []

            # Parse results (simple regex extraction)
            results = []
            html = response.text

            # Find result links
            pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)

            for url, title in matches[:max_results]:
                # Clean URL (DuckDuckGo wraps them)
                if "uddg=" in url:
                    url = re.search(r'uddg=([^&]+)', url)
                    if url:
                        url = requests.utils.unquote(url.group(1))

                results.append({
                    "title": title.strip(),
                    "url": url,
                    "description": ""
                })

            self._log(f"Found {len(results)} results")
            return results

        except Exception as e:
            self._log(f"Search error: {e}")
            return []

    def find_dataset_urls(self, domain: str, keywords: List[str]) -> List[DataSource]:
        """
        Search for dataset download URLs.

        Combines web search with known repository patterns.
        """
        sources = []

        # Search with domain + keywords + "download csv"
        query = f"{domain} {' '.join(keywords)} scientific database download csv"
        results = self.web_search(query)

        for r in results:
            url = r.get("url", "")

            # Identify format from URL
            fmt = "unknown"
            if ".csv" in url.lower():
                fmt = "csv"
            elif ".json" in url.lower():
                fmt = "json"
            elif ".nc" in url.lower() or "netcdf" in url.lower():
                fmt = "netcdf"
            elif ".txt" in url.lower():
                fmt = "text"

            # Identify organization
            org = "unknown"
            parsed = urlparse(url)
            if "noaa" in parsed.netloc:
                org = "NOAA"
            elif "nasa" in parsed.netloc:
                org = "NASA"
            elif "esa" in parsed.netloc:
                org = "ESA"
            elif "cern" in parsed.netloc:
                org = "CERN"

            sources.append(DataSource(
                name=r.get("title", "Unknown"),
                url=url,
                organization=org,
                format=fmt,
                description=r.get("description", "")
            ))

        return sources

    # =========================================================================
    # DOWNLOAD
    # =========================================================================

    def url_exists(self, url: str) -> bool:
        """Check if a URL exists and is accessible."""
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

    def download(self, url: str, use_cache: bool = True, timeout: int = 300) -> Optional[bytes]:
        """
        Download a file from URL.

        Args:
            url: URL to download
            use_cache: Use cached version if available
            timeout: Download timeout in seconds

        Returns:
            File content as bytes, or None if failed
        """
        # Check cache
        if use_cache:
            cached = self._get_cached(url)
            if cached:
                return cached

        self._log(f"Downloading: {url[:80]}...")

        try:
            response = self.session.get(url, timeout=timeout, stream=True)
            response.raise_for_status()

            # Download with progress for large files
            total = int(response.headers.get('content-length', 0))
            content = b''

            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if self.verbose and total > 0:
                    pct = len(content) / total * 100
                    if len(content) % (1024*1024) < 8192:  # Log every ~1MB
                        self._log(f"  {pct:.1f}% ({len(content)/1024/1024:.1f}MB)")

            self._log(f"Downloaded: {len(content)/1024:.1f}KB")

            # Cache
            if use_cache:
                self._set_cached(url, content)

            return content

        except requests.exceptions.Timeout:
            self._log(f"Timeout downloading: {url}")
            return None
        except requests.exceptions.RequestException as e:
            self._log(f"Download error: {e}")
            return None

    def download_ibtracs(self, basin: str = "ALL") -> Optional[bytes]:
        """
        Download IBTrACS hurricane data from NOAA.

        Args:
            basin: "ALL", "NA" (North Atlantic), "EP" (East Pacific), etc.

        Returns:
            CSV content as bytes
        """
        base = self.known_repositories["noaa"]["ibtracs"]
        filename = f"ibtracs.{basin}.list.v04r01.csv"
        url = urljoin(base, filename)

        return self.download(url, timeout=600)  # Large file, 10min timeout

    def download_extended_best_track(self, basin: str = "atlantic") -> Optional[bytes]:
        """
        Download Extended Best Track data from CIRA.

        Args:
            basin: "atlantic", "epac", "cpac"

        Returns:
            Text content as bytes
        """
        base = self.known_repositories["cira"]["ebtrk"]

        # File naming convention
        filenames = {
            "atlantic": "ebtrk_atlc_1851_2021.txt",
            "epac": "ebtrk_epac_1949_2021.txt",
            "cpac": "ebtrk_cpac_1950_2021.txt"
        }

        filename = filenames.get(basin.lower())
        if not filename:
            self._log(f"Unknown basin: {basin}")
            return None

        url = urljoin(base, f"data/{filename}")
        return self.download(url)

    # =========================================================================
    # PARSING
    # =========================================================================

    def parse_csv(self, content: bytes, **kwargs) -> Optional[pd.DataFrame]:
        """Parse CSV content into DataFrame."""
        try:
            return pd.read_csv(io.BytesIO(content), **kwargs)
        except Exception as e:
            self._log(f"CSV parse error: {e}")
            return None

    def parse_fixed_width(self, content: bytes, colspecs: List[Tuple[int, int]],
                          names: List[str] = None) -> Optional[pd.DataFrame]:
        """Parse fixed-width text file into DataFrame."""
        try:
            return pd.read_fwf(io.BytesIO(content), colspecs=colspecs, names=names)
        except Exception as e:
            self._log(f"Fixed-width parse error: {e}")
            return None

    def parse_ibtracs(self, content: bytes) -> Optional[pd.DataFrame]:
        """
        Parse IBTrACS CSV with proper column handling.

        Key columns:
        - USA_EYE: Eye diameter (nautical miles)
        - USA_RMW: Radius of maximum wind (nautical miles)
        - USA_SSHS: Saffir-Simpson category
        - WMO_WIND: Max sustained wind (knots)
        - WMO_PRES: Minimum central pressure (mb)
        """
        try:
            # Skip first row (units) and use second row as header
            df = pd.read_csv(
                io.BytesIO(content),
                skiprows=[1],  # Skip units row
                low_memory=False,
                na_values=[' ', '', 'MM', 'NA']
            )

            self._log(f"Parsed IBTrACS: {len(df)} rows, {len(df.columns)} columns")

            # Convert numeric columns
            numeric_cols = ['USA_EYE', 'USA_RMW', 'USA_SSHS', 'WMO_WIND', 'WMO_PRES']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            return df

        except Exception as e:
            self._log(f"IBTrACS parse error: {e}")
            return None

    def parse_extended_best_track(self, content: bytes) -> Optional[pd.DataFrame]:
        """
        Parse Extended Best Track fixed-width format.

        Key columns:
        - Eye diameter (nautical miles)
        - Speed (knots)
        - Pressure outer closed isobar
        - Radius outer closed isobar
        - R34, R50, R64 (wind radii)
        """
        try:
            # EBTRK column specifications (from documentation)
            # This is a simplified version - actual format is more complex
            colspecs = [
                (0, 6),    # Basin/Storm Number
                (6, 10),   # Year
                (10, 12),  # Month
                (12, 14),  # Day
                (14, 16),  # Hour
                (16, 20),  # Lat (tenths)
                (20, 25),  # Lon (tenths)
                (25, 28),  # Max Wind (knots)
                (28, 33),  # Min Pressure (mb)
                (33, 36),  # Storm Speed
                (36, 39),  # Eye Diameter (nm)
                (39, 44),  # Pressure OCI
                (44, 48),  # Radius OCI
                # ... more columns for wind radii
            ]

            names = [
                'storm_id', 'year', 'month', 'day', 'hour',
                'lat', 'lon', 'max_wind', 'min_pressure',
                'storm_speed', 'eye_diameter', 'poci', 'roci'
            ]

            df = pd.read_fwf(
                io.BytesIO(content),
                colspecs=colspecs,
                names=names,
                na_values=['-999', '-99', '999', '']
            )

            self._log(f"Parsed EBTRK: {len(df)} rows")
            return df

        except Exception as e:
            self._log(f"EBTRK parse error: {e}")
            return None

    def auto_parse(self, content: bytes, source: DataSource) -> Optional[pd.DataFrame]:
        """
        Automatically parse content based on format hints.
        """
        fmt = source.format.lower()
        url = source.url.lower()

        # IBTrACS special handling
        if "ibtracs" in url or "ibtracs" in source.name.lower():
            return self.parse_ibtracs(content)

        # Extended Best Track special handling
        if "ebtrk" in url or "extended" in source.name.lower():
            return self.parse_extended_best_track(content)

        # Generic CSV
        if fmt == "csv" or ".csv" in url:
            return self.parse_csv(content)

        # Generic JSON
        if fmt == "json" or ".json" in url:
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame([data])
            except:
                pass

        # Try CSV as fallback
        return self.parse_csv(content)

    # =========================================================================
    # HIGH-LEVEL API
    # =========================================================================

    def fetch_hurricane_data(self) -> Optional[ParsedDataset]:
        """
        Fetch hurricane data with eye and RMW measurements.

        Uses IBTrACS as primary source.
        """
        self._log("Fetching hurricane data from IBTrACS...")

        # Download
        content = self.download_ibtracs("NA")  # North Atlantic has best coverage
        if not content:
            self._log("Failed to download IBTrACS")
            return None

        # Parse
        df = self.parse_ibtracs(content)
        if df is None:
            return None

        # Filter for records with eye and RMW data
        if 'USA_EYE' in df.columns and 'USA_RMW' in df.columns:
            df_filtered = df.dropna(subset=['USA_EYE', 'USA_RMW'])
            self._log(f"Records with eye+RMW: {len(df_filtered)}")
        else:
            df_filtered = df

        source = DataSource(
            name="IBTrACS North Atlantic",
            url=self.known_repositories["noaa"]["ibtracs"] + "ibtracs.NA.list.v04r01.csv",
            organization="NOAA",
            format="csv",
            description="International Best Track Archive for Climate Stewardship",
            verified=True
        )

        return ParsedDataset(
            source=source,
            data=df_filtered,
            columns_used=['USA_EYE', 'USA_RMW', 'USA_SSHS', 'WMO_WIND'],
            n_rows=len(df_filtered),
            fetch_time=datetime.now().isoformat()
        )

    def fetch_data_for_domain(self, domain: str, quantities: List[str]) -> List[ParsedDataset]:
        """
        Fetch data for any domain based on quantities needed.

        Uses web search + known repositories to find data.
        """
        datasets = []

        # Domain-specific shortcuts
        domain_lower = domain.lower()

        if "hurricane" in domain_lower or "cyclone" in domain_lower or "meteorolog" in domain_lower:
            data = self.fetch_hurricane_data()
            if data:
                datasets.append(data)

        # TODO: Add more domain shortcuts
        # - cosmology -> Planck
        # - particle physics -> PDG
        # - etc.

        # If no shortcuts, try web search
        if not datasets:
            sources = self.find_dataset_urls(domain, quantities)

            for source in sources[:5]:  # Limit to top 5
                if self.url_exists(source.url):
                    source.verified = True
                    content = self.download(source.url)

                    if content:
                        df = self.auto_parse(content, source)
                        if df is not None and len(df) > 0:
                            datasets.append(ParsedDataset(
                                source=source,
                                data=df,
                                columns_used=list(df.columns),
                                n_rows=len(df),
                                fetch_time=datetime.now().isoformat()
                            ))

        return datasets


def main():
    """Test the Hermes Data Agent."""
    agent = HermesDataAgent()

    print("="*70)
    print("HERMES DATA AGENT TEST")
    print("="*70)

    # Test hurricane data fetch
    print("\nFetching hurricane data...")
    result = agent.fetch_hurricane_data()

    if result:
        print(f"\nSuccess!")
        print(f"Source: {result.source.name}")
        print(f"Rows: {result.n_rows}")
        print(f"Columns: {result.columns_used}")

        # Show sample
        print(f"\nSample data (eye and RMW):")
        df = result.data
        if 'USA_EYE' in df.columns and 'USA_RMW' in df.columns:
            sample = df[['USA_EYE', 'USA_RMW', 'USA_SSHS']].dropna().head(20)
            print(sample.to_string())

            # Compute ratio
            valid = df.dropna(subset=['USA_EYE', 'USA_RMW'])
            valid = valid[(valid['USA_EYE'] > 0) & (valid['USA_RMW'] > 0)]
            ratios = valid['USA_EYE'] / valid['USA_RMW']

            print(f"\n--- RATIO ANALYSIS ---")
            print(f"eye/RMW mean: {ratios.mean():.4f}")
            print(f"eye/RMW std:  {ratios.std():.4f}")
            print(f"n samples:    {len(ratios)}")
            print(f"1/φ =         {1/1.618:.4f}")
            print(f"Error:        {abs(ratios.mean() - 0.618)/0.618*100:.2f}%")
    else:
        print("Failed to fetch data")


if __name__ == "__main__":
    main()
