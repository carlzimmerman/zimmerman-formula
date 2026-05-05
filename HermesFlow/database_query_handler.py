#!/usr/bin/env python3
"""
DATABASE QUERY HANDLER - Structured API Access for Scientific Databases
========================================================================

Enables HermesFlow to query interactive scientific databases that don't
expose direct downloadable files. Uses structured API configurations and
Legomena-assisted discovery for unknown databases.

Supported databases:
- Smithsonian GVP (Global Volcanism Program)
- SILSO (Sunspot Index and Long-term Solar Observations)
- USGS Earthquake Catalog
- NOAA Climate APIs
- And more...

Author: Carl Zimmerman
Date: May 5, 2026
"""

import requests
import pandas as pd
import numpy as np
import json
import re
import io
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

# Try to import Legomena for API discovery
try:
    from Legomena import ask_legomena
    LEGOMENA_AVAILABLE = True
except ImportError:
    LEGOMENA_AVAILABLE = False
    def ask_legomena(prompt, **kwargs):
        return None


@dataclass
class APIConfig:
    """Configuration for a known database API."""
    name: str
    base_url: str
    method: str  # GET, POST
    default_params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    response_format: str = "csv"  # csv, json, xml, html_table, fixed_width
    rate_limit_seconds: float = 1.0
    description: str = ""
    domains: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    quantities: List[str] = field(default_factory=list)


@dataclass
class QueryResult:
    """Result from a database query."""
    success: bool
    data: Optional[pd.DataFrame] = None
    source_url: str = ""
    api_name: str = ""
    rows: int = 0
    columns: int = 0
    error: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class DatabaseQueryHandler:
    """
    Query interactive scientific databases via their APIs.

    This handler knows how to query specific databases that don't expose
    direct downloadable files but instead use APIs or form submissions.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'HermesFlow/2.0 (Scientific Research; contact@zimmerman-formula.org)'
        })
        self.last_request_time = {}

        # Initialize known API configurations
        self._init_known_apis()

    def _init_known_apis(self):
        """Initialize configurations for known scientific databases."""

        self.known_apis: Dict[str, APIConfig] = {

            # =========================================================
            # VOLCANOLOGY
            # =========================================================

            "smithsonian_gvp_eruptions": APIConfig(
                name="Smithsonian GVP Eruptions",
                base_url="https://volcano.si.edu/database/webservices/GVPWebService.asmx/GetEruptions",
                method="GET",
                default_params={
                    "vn": "",  # Volcano number (empty = all)
                    "ed": "true",  # Include eruption details
                },
                response_format="xml",
                rate_limit_seconds=2.0,
                description="Global Volcanism Program eruption database",
                domains=["volcanology", "geophysics"],
                topics=["volcano", "eruption", "VEI", "tephra"],
                quantities=["VEI", "eruption_count", "start_date", "end_date", "tephra_volume"]
            ),

            "smithsonian_gvp_volcanoes": APIConfig(
                name="Smithsonian GVP Volcanoes",
                base_url="https://volcano.si.edu/database/webservices/GVPWebService.asmx/GetVolcanoes",
                method="GET",
                default_params={
                    "reg": "",  # Region (empty = all)
                },
                response_format="xml",
                rate_limit_seconds=2.0,
                description="Global Volcanism Program volcano list",
                domains=["volcanology"],
                topics=["volcano", "location", "type"],
                quantities=["latitude", "longitude", "elevation", "volcano_type"]
            ),

            "noaa_significant_volcanoes": APIConfig(
                name="NOAA Significant Volcanic Eruptions",
                base_url="https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/volcanoes",
                method="GET",
                default_params={
                    "minYear": "-4360",
                    "maxYear": str(datetime.now().year),
                },
                headers={"Accept": "application/json"},
                response_format="json",
                rate_limit_seconds=1.0,
                description="NOAA/NCEI Significant Volcanic Eruptions Database",
                domains=["volcanology", "geophysics"],
                topics=["volcano", "eruption", "VEI", "fatalities"],
                quantities=["VEI", "deaths", "damage_millions", "tsunami", "earthquake"]
            ),

            # =========================================================
            # SOLAR PHYSICS
            # =========================================================

            "silso_monthly_total": APIConfig(
                name="SILSO Monthly Sunspot Number",
                base_url="https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.txt",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Monthly mean total sunspot number since 1749",
                domains=["astronomy", "solar_physics"],
                topics=["sunspot", "solar_cycle", "solar_activity"],
                quantities=["sunspot_number", "standard_deviation", "observations"]
            ),

            "silso_yearly_total": APIConfig(
                name="SILSO Yearly Sunspot Number",
                base_url="https://www.sidc.be/silso/DATA/SN_y_tot_V2.0.txt",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Yearly mean total sunspot number since 1700",
                domains=["astronomy", "solar_physics"],
                topics=["sunspot", "solar_cycle", "solar_activity"],
                quantities=["sunspot_number", "standard_deviation", "observations"]
            ),

            "silso_daily_total": APIConfig(
                name="SILSO Daily Sunspot Number",
                base_url="https://www.sidc.be/silso/DATA/SN_d_tot_V2.0.txt",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Daily total sunspot number since 1818",
                domains=["astronomy", "solar_physics"],
                topics=["sunspot", "solar_cycle", "daily"],
                quantities=["sunspot_number", "standard_deviation", "observations"]
            ),

            "silso_hemispheric": APIConfig(
                name="SILSO Hemispheric Sunspot Numbers",
                base_url="https://www.sidc.be/silso/DATA/SN_m_hem_V2.0.txt",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Monthly hemispheric sunspot numbers (North/South)",
                domains=["astronomy", "solar_physics"],
                topics=["sunspot", "hemispheric", "asymmetry"],
                quantities=["north_ssn", "south_ssn", "total_ssn"]
            ),

            "noaa_solar_flux": APIConfig(
                name="NOAA Solar F10.7 Flux",
                base_url="https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json",
                method="GET",
                default_params={},
                response_format="json",
                rate_limit_seconds=1.0,
                description="Solar cycle indices including F10.7 flux",
                domains=["astronomy", "solar_physics"],
                topics=["solar_flux", "F10.7", "solar_cycle"],
                quantities=["f10.7", "sunspot_number", "smoothed_ssn"]
            ),

            # =========================================================
            # SEISMOLOGY
            # =========================================================

            "usgs_earthquake": APIConfig(
                name="USGS Earthquake Catalog",
                base_url="https://earthquake.usgs.gov/fdsnws/event/1/query",
                method="GET",
                default_params={
                    "format": "csv",
                    "minmagnitude": "4.0",
                    "starttime": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
                    "endtime": datetime.now().strftime("%Y-%m-%d"),
                    "orderby": "time",
                },
                response_format="csv",
                rate_limit_seconds=1.0,
                description="USGS FDSN Event Web Service for earthquakes",
                domains=["seismology", "geophysics"],
                topics=["earthquake", "magnitude", "seismic"],
                quantities=["magnitude", "depth", "latitude", "longitude", "time"]
            ),

            "usgs_earthquake_historical": APIConfig(
                name="USGS Historical Earthquakes",
                base_url="https://earthquake.usgs.gov/fdsnws/event/1/query",
                method="GET",
                default_params={
                    "format": "csv",
                    "minmagnitude": "6.0",
                    "starttime": "1900-01-01",
                    "endtime": datetime.now().strftime("%Y-%m-%d"),
                    "orderby": "time",
                },
                response_format="csv",
                rate_limit_seconds=1.0,
                description="USGS historical significant earthquakes",
                domains=["seismology", "geophysics"],
                topics=["earthquake", "historical", "major"],
                quantities=["magnitude", "depth", "latitude", "longitude"]
            ),

            # =========================================================
            # METEOROLOGY / CLIMATE
            # =========================================================

            "noaa_tornado_monthly": APIConfig(
                name="NOAA PSL Tornado Monthly",
                base_url="https://psl.noaa.gov/data/correlation/tornado.us.mon.data",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Monthly US tornado counts from NOAA PSL",
                domains=["meteorology", "climatology"],
                topics=["tornado", "severe_weather", "monthly"],
                quantities=["tornado_count"]
            ),

            "noaa_hurricane_ace": APIConfig(
                name="NOAA PSL Hurricane ACE",
                base_url="https://psl.noaa.gov/data/correlation/hurr.atl.data",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Atlantic Hurricane ACE index from NOAA PSL",
                domains=["meteorology", "climatology"],
                topics=["hurricane", "ACE", "tropical_storm"],
                quantities=["ACE_index", "hurricane_count"]
            ),

            "noaa_oni_index": APIConfig(
                name="NOAA ONI Index (ENSO)",
                base_url="https://psl.noaa.gov/data/correlation/oni.data",
                method="GET",
                default_params={},
                response_format="fixed_width",
                rate_limit_seconds=1.0,
                description="Oceanic Nino Index for ENSO monitoring",
                domains=["meteorology", "oceanography", "climatology"],
                topics=["ENSO", "El_Nino", "La_Nina", "ONI"],
                quantities=["oni_index", "temperature_anomaly"]
            ),

            # =========================================================
            # PARTICLE PHYSICS
            # =========================================================

            "pdg_particle_masses": APIConfig(
                name="PDG Particle Masses",
                base_url="https://pdg.lbl.gov/2024/mcdata/mass_width_2024.csv",
                method="GET",
                default_params={},
                response_format="csv",
                rate_limit_seconds=1.0,
                description="Particle Data Group mass and width data",
                domains=["particle_physics", "physics"],
                topics=["particle", "mass", "decay", "width"],
                quantities=["mass", "width", "lifetime"]
            ),

            # =========================================================
            # COSMOLOGY
            # =========================================================

            "planck_parameters": APIConfig(
                name="Planck Cosmological Parameters",
                base_url="https://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_CosmoParams_fullGrid_R3.01.zip",
                method="GET",
                default_params={},
                response_format="zip",
                rate_limit_seconds=5.0,
                description="Planck 2018 cosmological parameters",
                domains=["cosmology", "astrophysics"],
                topics=["CMB", "cosmological_parameters", "Hubble"],
                quantities=["H0", "omega_m", "omega_lambda", "sigma8"]
            ),

            # =========================================================
            # GLACIOLOGY
            # =========================================================

            "wgms_mass_balance": APIConfig(
                name="WGMS Glacier Mass Balance",
                base_url="https://wgms.ch/downloads/DOI-WGMS-FoG-2023-09.zip",
                method="GET",
                default_params={},
                response_format="zip",
                rate_limit_seconds=5.0,
                description="World Glacier Monitoring Service mass balance data",
                domains=["glaciology", "climatology"],
                topics=["glacier", "mass_balance", "ice"],
                quantities=["mass_balance", "area", "volume_change"]
            ),
        }

    def _log(self, msg: str):
        """Log message if verbose."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[DatabaseQuery {timestamp}] {msg}")

    def _rate_limit(self, api_name: str, delay: float):
        """Apply rate limiting for API requests."""
        if api_name in self.last_request_time:
            elapsed = time.time() - self.last_request_time[api_name]
            if elapsed < delay:
                time.sleep(delay - elapsed)
        self.last_request_time[api_name] = time.time()

    def find_apis_for_domain(self, domain: str, topic: str = None) -> List[APIConfig]:
        """Find known APIs that match a domain and optionally a topic."""
        matches = []
        domain_lower = domain.lower()
        topic_lower = topic.lower() if topic else ""

        for api_name, config in self.known_apis.items():
            # Check domain match
            domain_match = any(d.lower() == domain_lower for d in config.domains)

            # Check topic match if specified
            if topic_lower:
                topic_match = any(topic_lower in t.lower() for t in config.topics)
            else:
                topic_match = True

            if domain_match and topic_match:
                matches.append(config)

        return matches

    def find_apis_for_quantities(self, quantities: List[str]) -> List[APIConfig]:
        """Find APIs that provide specific quantities."""
        matches = []
        quantities_lower = [q.lower() for q in quantities]

        for api_name, config in self.known_apis.items():
            api_quantities = [q.lower() for q in config.quantities]
            if any(q in api_quantities for q in quantities_lower):
                matches.append(config)

        return matches

    def query(self, api_name: str, **kwargs) -> QueryResult:
        """
        Query a known API by name.

        Args:
            api_name: Name of the API (key in known_apis)
            **kwargs: Override default parameters

        Returns:
            QueryResult with data or error
        """
        if api_name not in self.known_apis:
            return QueryResult(
                success=False,
                error=f"Unknown API: {api_name}. Known APIs: {list(self.known_apis.keys())}"
            )

        config = self.known_apis[api_name]
        return self._execute_query(config, **kwargs)

    def query_config(self, config: APIConfig, **kwargs) -> QueryResult:
        """Query using an APIConfig object."""
        return self._execute_query(config, **kwargs)

    def _execute_query(self, config: APIConfig, **kwargs) -> QueryResult:
        """Execute a query against an API."""
        self._log(f"Querying {config.name}...")

        # Apply rate limiting
        self._rate_limit(config.name, config.rate_limit_seconds)

        # Merge default params with overrides
        params = {**config.default_params, **kwargs}

        try:
            # Make request
            if config.method.upper() == "GET":
                response = self.session.get(
                    config.base_url,
                    params=params if params else None,
                    headers=config.headers,
                    timeout=60
                )
            else:
                response = self.session.post(
                    config.base_url,
                    data=params,
                    headers=config.headers,
                    timeout=60
                )

            response.raise_for_status()

            # Parse response
            df = self._parse_response(response, config.response_format, config.name)

            if df is not None and len(df) > 0:
                self._log(f"  SUCCESS: {len(df)} rows, {len(df.columns)} columns")
                return QueryResult(
                    success=True,
                    data=df,
                    source_url=config.base_url,
                    api_name=config.name,
                    rows=len(df),
                    columns=len(df.columns),
                    metadata={
                        "description": config.description,
                        "domains": config.domains,
                        "quantities": config.quantities
                    }
                )
            else:
                return QueryResult(
                    success=False,
                    source_url=config.base_url,
                    api_name=config.name,
                    error="Response parsed but no data found"
                )

        except requests.exceptions.Timeout:
            return QueryResult(success=False, error=f"Timeout querying {config.name}")
        except requests.exceptions.HTTPError as e:
            return QueryResult(success=False, error=f"HTTP error: {e}")
        except Exception as e:
            return QueryResult(success=False, error=f"Error querying {config.name}: {e}")

    def _parse_response(self, response: requests.Response, format_type: str, api_name: str) -> Optional[pd.DataFrame]:
        """Parse API response into DataFrame."""
        content = response.text

        try:
            if format_type == "csv":
                return pd.read_csv(io.StringIO(content))

            elif format_type == "json":
                data = response.json()
                # Handle various JSON structures
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    # Look for data array in common keys
                    for key in ['data', 'results', 'records', 'items', 'features']:
                        if key in data and isinstance(data[key], list):
                            return pd.DataFrame(data[key])
                    # If it's a flat dict, make single-row DataFrame
                    return pd.DataFrame([data])
                return None

            elif format_type == "xml":
                return self._parse_xml(content, api_name)

            elif format_type == "fixed_width":
                return self._parse_fixed_width(content, api_name)

            elif format_type == "html_table":
                tables = pd.read_html(io.StringIO(content))
                return tables[0] if tables else None

            elif format_type == "zip":
                # For zip files, we'd need to extract and parse
                self._log(f"  ZIP format - would need extraction")
                return None

            else:
                self._log(f"  Unknown format: {format_type}")
                return None

        except Exception as e:
            self._log(f"  Parse error: {e}")
            return None

    def _parse_xml(self, content: str, api_name: str) -> Optional[pd.DataFrame]:
        """Parse XML response (especially for GVP)."""
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)

            # Handle GVP-style XML
            if "gvp" in api_name.lower():
                records = []
                for elem in root.iter():
                    if elem.tag.endswith(('Eruption', 'Volcano')):
                        record = {}
                        for child in elem:
                            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                            record[tag] = child.text
                        if record:
                            records.append(record)
                return pd.DataFrame(records) if records else None

            # Generic XML parsing
            records = []
            for child in root:
                record = {subchild.tag: subchild.text for subchild in child}
                if record:
                    records.append(record)
            return pd.DataFrame(records) if records else None

        except Exception as e:
            self._log(f"  XML parse error: {e}")
            return None

    def _parse_fixed_width(self, content: str, api_name: str) -> Optional[pd.DataFrame]:
        """Parse fixed-width or whitespace-delimited data."""
        lines = content.strip().split('\n')

        # Skip comment lines and find data
        data_lines = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('%'):
                continue
            # Skip lines that are all text (headers without numbers)
            if not any(c.isdigit() for c in line):
                continue
            data_lines.append(line)

        if not data_lines:
            return None

        # Try to parse as whitespace-delimited
        try:
            # Split each line by whitespace
            rows = [line.split() for line in data_lines]

            # Find consistent column count
            col_counts = [len(row) for row in rows]
            if not col_counts:
                return None
            most_common = max(set(col_counts), key=col_counts.count)

            # Filter to rows with consistent column count
            consistent_rows = [row for row in rows if len(row) == most_common]

            if not consistent_rows:
                return None

            df = pd.DataFrame(consistent_rows)

            # Try to convert columns to numeric
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass

            # Add column names based on API type
            if "silso" in api_name.lower():
                if "monthly" in api_name.lower() or "yearly" in api_name.lower():
                    if len(df.columns) >= 4:
                        df.columns = ['year', 'month', 'decimal_year', 'ssn', 'std_dev', 'observations', 'provisional'][:len(df.columns)]
                elif "hemispheric" in api_name.lower():
                    if len(df.columns) >= 6:
                        df.columns = ['year', 'month', 'decimal_year', 'north_ssn', 'south_ssn', 'total_ssn'][:len(df.columns)]
            elif "tornado" in api_name.lower():
                if len(df.columns) == 13:
                    df.columns = ['year'] + [f'month_{i}' for i in range(1, 13)]

            return df

        except Exception as e:
            self._log(f"  Fixed-width parse error: {e}")
            return None

    def discover_api(self, url: str, domain: str, quantities: List[str]) -> Optional[Dict]:
        """
        Use Legomena to discover how to query an unknown database.

        Args:
            url: URL of the database or API endpoint
            domain: Scientific domain
            quantities: List of quantities we're looking for

        Returns:
            Dict with API configuration or None
        """
        if not LEGOMENA_AVAILABLE:
            self._log("Legomena not available for API discovery")
            return None

        self._log(f"Using Legomena to discover API at {url}...")

        # Fetch page content
        try:
            response = self.session.get(url, timeout=30)
            page_content = response.text[:5000]  # First 5000 chars
        except:
            page_content = "Could not fetch page"

        prompt = f"""
        I need to programmatically extract data from this scientific database.

        URL: {url}
        Domain: {domain}
        Quantities needed: {quantities}

        Page content preview:
        {page_content[:2000]}

        Analyze this page and determine:

        1. Is there a REST API? If so:
           - What is the endpoint URL?
           - What HTTP method (GET/POST)?
           - What parameters are needed?
           - What format is returned (JSON/CSV/XML)?

        2. Is there a direct data file download? If so:
           - What is the file URL?
           - What format (CSV/TXT/XLS)?

        3. Is there a form that needs to be submitted? If so:
           - What is the form action URL?
           - What fields need to be filled?

        Return a JSON object with this structure:
        {{
            "has_api": true/false,
            "api_url": "...",
            "method": "GET" or "POST",
            "params": {{}},
            "response_format": "json/csv/xml",
            "has_download": true/false,
            "download_url": "...",
            "download_format": "csv/txt/xls",
            "has_form": true/false,
            "form_action": "...",
            "form_fields": {{}},
            "notes": "..."
        }}

        Only return the JSON, no explanation.
        """

        try:
            result = ask_legomena(prompt, model="legomena-moe")
            if result:
                # Try to extract JSON from response
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    return json.loads(json_match.group())
        except Exception as e:
            self._log(f"  API discovery error: {e}")

        return None

    def query_all_for_domain(self, domain: str, topic: str = None) -> List[QueryResult]:
        """
        Query all known APIs that match a domain/topic.

        Returns list of successful results.
        """
        apis = self.find_apis_for_domain(domain, topic)
        results = []

        self._log(f"Found {len(apis)} APIs for domain={domain}, topic={topic}")

        for config in apis:
            result = self.query_config(config)
            if result.success:
                results.append(result)

        return results

    def get_available_apis(self) -> List[Dict]:
        """Get list of all available APIs with their details."""
        return [
            {
                "name": config.name,
                "domains": config.domains,
                "topics": config.topics,
                "quantities": config.quantities,
                "description": config.description
            }
            for config in self.known_apis.values()
        ]


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def query_database(api_name: str, **kwargs) -> QueryResult:
    """Convenience function to query a database."""
    handler = DatabaseQueryHandler(verbose=True)
    return handler.query(api_name, **kwargs)


def find_apis(domain: str, topic: str = None) -> List[APIConfig]:
    """Find APIs for a domain/topic."""
    handler = DatabaseQueryHandler(verbose=False)
    return handler.find_apis_for_domain(domain, topic)


def list_all_apis() -> List[Dict]:
    """List all available APIs."""
    handler = DatabaseQueryHandler(verbose=False)
    return handler.get_available_apis()


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("DATABASE QUERY HANDLER - Test")
    print("=" * 60)

    handler = DatabaseQueryHandler(verbose=True)

    # List available APIs
    print("\nAvailable APIs:")
    print("-" * 40)
    for api_info in handler.get_available_apis():
        print(f"  {api_info['name']}")
        print(f"    Domains: {api_info['domains']}")
        print(f"    Topics: {api_info['topics']}")
        print()

    # Test specific APIs
    print("\n" + "=" * 60)
    print("Testing APIs...")
    print("=" * 60)

    test_apis = [
        "silso_monthly_total",
        "noaa_significant_volcanoes",
        "usgs_earthquake",
    ]

    for api_name in test_apis:
        print(f"\n--- Testing {api_name} ---")
        result = handler.query(api_name)
        if result.success:
            print(f"SUCCESS: {result.rows} rows, {result.columns} columns")
            if result.data is not None:
                print(f"Columns: {list(result.data.columns)[:5]}...")
                print(f"Sample:\n{result.data.head(3)}")
        else:
            print(f"FAILED: {result.error}")
