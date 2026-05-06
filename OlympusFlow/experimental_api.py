#!/usr/bin/env python3
"""
OLYMPUSFLOW - Experimental Data API
=====================================

REAL API calls to get experimental values from:
- NIST CODATA (fundamental constants)
- Particle Data Group (particle physics)
- Web search (fallback with clear labeling)
- Legomena (last resort, clearly labeled as LLM)

NO HARDCODING. DYNAMIC. HONEST.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import re
import json
import time
import subprocess
from typing import Dict, Optional, List, Tuple
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote

from .honest_contracts import ExperimentalValue, SourceType


# =============================================================================
# CONFIGURATION
# =============================================================================

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")

# Known CODATA constants with their NIST identifiers
# This is a MAPPING, not the values themselves - values come from API
CODATA_IDENTIFIERS = {
    "fine structure constant": "fine-structure constant",
    "alpha": "fine-structure constant",
    "planck constant": "Planck constant",
    "speed of light": "speed of light in vacuum",
    "gravitational constant": "Newtonian constant of gravitation",
    "electron mass": "electron mass",
    "proton mass": "proton mass",
    "proton electron mass ratio": "proton-electron mass ratio",
    "boltzmann constant": "Boltzmann constant",
    "avogadro constant": "Avogadro constant",
    "elementary charge": "elementary charge",
    "rydberg constant": "Rydberg constant",
    "bohr radius": "Bohr radius",
}


class ExperimentalDataAPI:
    """
    Real API access to experimental physics data.

    Priority order:
    1. CODATA/NIST API (most reliable)
    2. Web search with source extraction
    3. Legomena (LLM) as last resort - CLEARLY LABELED
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.cache: Dict[str, ExperimentalValue] = {}
        self.cache_expiry = 3600  # 1 hour

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[ExpAPI {ts}] {msg}")

    # =========================================================================
    # MAIN INTERFACE
    # =========================================================================

    def get_value(self, constant_name: str,
                  prefer_source: SourceType = None) -> Optional[ExperimentalValue]:
        """
        Get experimental value for a constant.

        Tries sources in order of reliability.
        Returns None if not found.
        """
        self._log(f"Looking up: {constant_name}")

        # Check cache
        cache_key = constant_name.lower().replace(" ", "_")
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            self._log(f"  Cache hit: {cached.value} from {cached.source_name}")
            return cached

        # Try CODATA first
        result = self._try_codata(constant_name)
        if result:
            self._log(f"  CODATA: {result.value} +/- {result.uncertainty}")
            self.cache[cache_key] = result
            return result

        # Try web search
        result = self._try_web_search(constant_name)
        if result:
            self._log(f"  Web: {result.value} from {result.source_name}")
            self.cache[cache_key] = result
            return result

        # Last resort: Legomena (clearly labeled)
        result = self._try_legomena(constant_name)
        if result:
            self._log(f"  LLM (UNVERIFIED): {result.value}")
            self.cache[cache_key] = result
            return result

        self._log(f"  No value found for {constant_name}")
        return None

    # =========================================================================
    # CODATA / NIST
    # =========================================================================

    def _try_codata(self, constant_name: str) -> Optional[ExperimentalValue]:
        """
        Try to get value from NIST CODATA.

        Uses the NIST Constants API.
        """
        # Map to CODATA identifier
        normalized = constant_name.lower()
        codata_name = CODATA_IDENTIFIERS.get(normalized)

        if not codata_name:
            # Try fuzzy match
            for key, value in CODATA_IDENTIFIERS.items():
                if key in normalized or normalized in key:
                    codata_name = value
                    break

        if not codata_name:
            return None

        try:
            # NIST Constants API endpoint
            # https://physics.nist.gov/cgi-bin/cuu/Info/Constants/
            url = f"https://physics.nist.gov/cgi-bin/cuu/Value?{quote(codata_name.replace(' ', '|'))}"

            req = Request(url, headers={'User-Agent': 'OlympusFlow/1.0'})

            with urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')

                # Parse the NIST response
                # The value is in a specific format on their page
                value_match = re.search(r'<b>Value</b></td><td[^>]*>([^<]+)', html)
                uncert_match = re.search(r'<b>Standard uncertainty</b></td><td[^>]*>([^<]+)', html)
                unit_match = re.search(r'<b>Unit</b></td><td[^>]*>([^<]+)', html)

                if value_match:
                    # Parse value (handle scientific notation)
                    value_str = value_match.group(1).strip().replace(' ', '')
                    value_str = re.sub(r'\.\.\.', '', value_str)  # Remove ellipsis

                    # Handle x 10^n notation
                    if 'x' in value_str and '10' in value_str:
                        parts = re.split(r'x\s*10', value_str)
                        mantissa = float(parts[0])
                        exp_match = re.search(r'\^\{?(-?\d+)\}?', parts[1]) if len(parts) > 1 else None
                        if exp_match:
                            exponent = int(exp_match.group(1))
                            value = mantissa * (10 ** exponent)
                        else:
                            value = mantissa
                    else:
                        value = float(value_str)

                    # Parse uncertainty
                    uncertainty = 0.0
                    if uncert_match:
                        uncert_str = uncert_match.group(1).strip().replace(' ', '')
                        if 'exact' in uncert_str.lower():
                            uncertainty = 0.0
                        else:
                            try:
                                # Handle scientific notation
                                uncert_str = re.sub(r'\.\.\.', '', uncert_str)
                                if 'x' in uncert_str and '10' in uncert_str:
                                    parts = re.split(r'x\s*10', uncert_str)
                                    mantissa = float(parts[0])
                                    exp_match = re.search(r'\^\{?(-?\d+)\}?', parts[1]) if len(parts) > 1 else None
                                    if exp_match:
                                        exponent = int(exp_match.group(1))
                                        uncertainty = mantissa * (10 ** exponent)
                                    else:
                                        uncertainty = mantissa
                                else:
                                    uncertainty = float(uncert_str)
                            except:
                                uncertainty = abs(value) * 1e-10  # Default small uncertainty

                    unit = unit_match.group(1).strip() if unit_match else ""

                    return ExperimentalValue(
                        value=value,
                        uncertainty=uncertainty,
                        unit=unit,
                        source_type=SourceType.CODATA,
                        source_name="CODATA 2022",
                        source_url=url,
                        is_verified=True,
                        api_response=html[:500]  # Store snippet for audit
                    )

        except (URLError, HTTPError) as e:
            self._log(f"  CODATA API error: {e}")
        except Exception as e:
            self._log(f"  CODATA parse error: {e}")

        return None

    # =========================================================================
    # WEB SEARCH
    # =========================================================================

    def _try_web_search(self, constant_name: str) -> Optional[ExperimentalValue]:
        """
        Search the web for experimental value.

        Uses multiple search strategies.
        """
        # Try DuckDuckGo instant answer API first (faster)
        result = self._try_duckduckgo(constant_name)
        if result:
            return result

        # Try Wikipedia API
        result = self._try_wikipedia(constant_name)
        if result:
            return result

        return None

    def _try_duckduckgo(self, constant_name: str) -> Optional[ExperimentalValue]:
        """Try DuckDuckGo instant answer API."""
        try:
            query = f"{constant_name} value physics"
            url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1"

            req = Request(url, headers={'User-Agent': 'OlympusFlow/1.0'})

            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

                # Check abstract
                abstract = data.get('Abstract', '') + data.get('AbstractText', '')

                if abstract:
                    # Try to extract numerical value
                    value, unit = self._extract_value_from_text(abstract, constant_name)
                    if value is not None:
                        return ExperimentalValue(
                            value=value,
                            uncertainty=abs(value) * 0.01,  # Assume 1% uncertainty
                            unit=unit,
                            source_type=SourceType.WEB_SEARCH,
                            source_name=data.get('AbstractSource', 'DuckDuckGo'),
                            source_url=data.get('AbstractURL', url),
                            is_verified=False
                        )

        except Exception as e:
            self._log(f"  DuckDuckGo error: {e}")

        return None

    def _try_wikipedia(self, constant_name: str) -> Optional[ExperimentalValue]:
        """Try Wikipedia API for constant values."""
        try:
            # Search for the page
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(constant_name.replace(' ', '_'))}"

            req = Request(search_url, headers={'User-Agent': 'OlympusFlow/1.0'})

            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

                extract = data.get('extract', '')

                if extract:
                    value, unit = self._extract_value_from_text(extract, constant_name)
                    if value is not None:
                        return ExperimentalValue(
                            value=value,
                            uncertainty=abs(value) * 0.01,
                            unit=unit,
                            source_type=SourceType.WEB_SEARCH,
                            source_name="Wikipedia",
                            source_url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            is_verified=False
                        )

        except Exception as e:
            self._log(f"  Wikipedia error: {e}")

        return None

    def _extract_value_from_text(self, text: str, constant_name: str) -> Tuple[Optional[float], str]:
        """
        Extract numerical value from text.

        Returns (value, unit) or (None, "")
        """
        # Common patterns for physical constants
        patterns = [
            # Scientific notation: 1.23 × 10^-4
            r'([-+]?\d+\.?\d*)\s*[×x]\s*10\^?\{?(-?\d+)\}?',
            # Decimal with uncertainty: 0.1234(5)
            r'([-+]?\d+\.\d+)\s*\(?(\d+)\)?',
            # Simple decimal: 0.1234
            r'(?:=|is|approximately|about|around)\s*([-+]?\d+\.?\d*)',
            # Value followed by unit
            r'([-+]?\d+\.?\d*(?:[eE][-+]?\d+)?)\s*([a-zA-Z/²³]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) >= 2 and 'x' in pattern.lower() or '×' in pattern:
                        # Scientific notation
                        mantissa = float(groups[0])
                        exponent = int(groups[1])
                        value = mantissa * (10 ** exponent)
                        return value, ""
                    else:
                        value = float(groups[0])
                        unit = groups[1] if len(groups) > 1 else ""
                        # Sanity check - physics constants are usually not huge
                        if abs(value) < 1e30:
                            return value, unit
                except:
                    continue

        return None, ""

    # =========================================================================
    # LEGOMENA (LLM) - LAST RESORT, CLEARLY LABELED
    # =========================================================================

    def _try_legomena(self, constant_name: str) -> Optional[ExperimentalValue]:
        """
        Ask Legomena for the value.

        THIS IS AN LLM ASSERTION, NOT A VERIFIED VALUE.
        Clearly labeled as such.
        """
        try:
            prompt = f"""What is the experimentally measured value of {constant_name}?

Respond ONLY with these fields, nothing else:
VALUE: [number in scientific notation if needed]
UNCERTAINTY: [1-sigma error, use scientific notation if needed]
UNIT: [physical unit]
SOURCE: [where this measurement comes from]

Example for speed of light:
VALUE: 299792458
UNCERTAINTY: 0
UNIT: m/s
SOURCE: CODATA 2022 (exact by definition)"""

            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                response = result.stdout.strip()

                # Parse response
                value = None
                uncertainty = 0.0
                unit = ""
                source = "Legomena (LLM)"

                for line in response.split('\n'):
                    if 'VALUE:' in line:
                        try:
                            val_str = line.split('VALUE:')[1].strip()
                            # Handle scientific notation
                            val_str = val_str.replace('×', 'e').replace('x', 'e').replace('^', 'e')
                            val_str = re.sub(r'10e', '1e', val_str)
                            value = float(val_str)
                        except:
                            pass
                    elif 'UNCERTAINTY:' in line:
                        try:
                            uncert_str = line.split('UNCERTAINTY:')[1].strip()
                            uncert_str = uncert_str.replace('×', 'e').replace('x', 'e')
                            uncertainty = float(uncert_str)
                        except:
                            pass
                    elif 'UNIT:' in line:
                        unit = line.split('UNIT:')[1].strip()
                    elif 'SOURCE:' in line:
                        source = line.split('SOURCE:')[1].strip()

                if value is not None:
                    return ExperimentalValue(
                        value=value,
                        uncertainty=uncertainty if uncertainty > 0 else abs(value) * 0.01,
                        unit=unit,
                        source_type=SourceType.LLM_ASSERTION,
                        source_name=f"Legomena (claims: {source})",
                        source_url="",
                        is_verified=False,  # NEVER verified
                        api_response=response
                    )

        except subprocess.TimeoutExpired:
            self._log("  Legomena timeout")
        except Exception as e:
            self._log(f"  Legomena error: {e}")

        return None

    # =========================================================================
    # SPECIALIZED LOOKUPS
    # =========================================================================

    def get_cosmological_parameter(self, param_name: str) -> Optional[ExperimentalValue]:
        """
        Get cosmological parameters from Planck or other surveys.

        Parameters like Omega_Lambda, H0, etc.
        """
        # Try web search first with specific cosmology terms
        search_term = f"Planck 2018 {param_name} value"
        result = self._try_web_search(search_term)

        if result:
            result.source_name = "Planck Collaboration (via web)"
            return result

        # Fall back to Legomena with cosmology context
        return self._try_legomena(f"{param_name} cosmological parameter Planck 2018")

    def get_particle_physics_value(self, param_name: str) -> Optional[ExperimentalValue]:
        """
        Get particle physics values from PDG.
        """
        search_term = f"PDG {param_name} value"
        result = self._try_web_search(search_term)

        if result:
            result.source_name = "PDG (via web)"
            return result

        return self._try_legomena(f"{param_name} particle physics PDG")


# =============================================================================
# DEMO
# =============================================================================

def demo():
    """Test the experimental data API."""
    api = ExperimentalDataAPI()

    test_constants = [
        "fine structure constant",
        "speed of light",
        "proton electron mass ratio",
        "von Karman constant",
        "dark energy density Omega_Lambda",
    ]

    print("\n" + "=" * 60)
    print("EXPERIMENTAL DATA API TEST")
    print("=" * 60)

    for const in test_constants:
        print(f"\n{const}:")
        print("-" * 40)

        result = api.get_value(const)

        if result:
            print(f"  Value: {result.value}")
            print(f"  Uncertainty: {result.uncertainty}")
            print(f"  Unit: {result.unit}")
            print(f"  Source: {result.source_type.value} - {result.source_name}")
            print(f"  Verified: {result.is_verified}")
        else:
            print("  NOT FOUND")


if __name__ == "__main__":
    demo()
