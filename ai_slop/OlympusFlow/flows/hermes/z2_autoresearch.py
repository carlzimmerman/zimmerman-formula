#!/usr/bin/env python3
"""
Z² AUTO-RESEARCH SYSTEM
========================

Fully autonomous Z² relationship discovery.
NO Claude - uses only open source tools:
  - Legomena LLM (via Ollama) for reasoning
  - Hermes Data Agent for data acquisition
  - Python for verification

The system:
1. Takes a topic as input
2. Discovers what quantities/ratios to look for (Legomena)
3. Finds and downloads real scientific data (Hermes)
4. Computes relationships and tests against Z² (Python)
5. Documents findings (Legomena)

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

# Import our components
from hermes_data_agent import HermesDataAgent, DataSource, ParsedDataset

# Z² Constants
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
    "1/3": 1/3,               # 0.333
    "2/3": 2/3,               # 0.667
    "1/e": 1/math.e,          # 0.368
    "1/pi": 1/math.pi,        # 0.318
}

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-31b")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "180"))
OUTPUT_DIR = Path(__file__).parent / "autoresearch_output"


@dataclass
class QuantityPair:
    """A pair of quantities whose ratio might be meaningful."""
    quantity_a: str
    quantity_b: str
    description: str
    data_columns: Tuple[str, str] = None  # Actual column names in data


@dataclass
class RatioResult:
    """Result of testing a ratio against Z² formulas."""
    quantity_pair: str
    mean_ratio: float
    std_ratio: float
    n_samples: int
    best_z2_formula: str
    z2_value: float
    error_percent: float
    p_value: float
    verdict: str  # VALIDATED, STRONG, WEAK, REJECTED


@dataclass
class ResearchSession:
    """Complete research session results."""
    topic: str
    started: str
    domain: str
    quantities_discovered: List[str]
    ratio_pairs: List[Dict]
    data_sources: List[Dict]
    results: List[Dict]
    best_match: Optional[Dict]
    conclusion: str
    completed: str = None


class LegomenaClient:
    """Client for Legomena LLM via Ollama."""

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
            else:
                self._log(f"Error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            self._log(f"Timeout ({timeout}s)")
            return None
        except Exception as e:
            self._log(f"Error: {e}")
            return None

    def identify_domain(self, topic: str) -> str:
        """Identify the scientific domain for a topic."""
        prompt = f"""What scientific domain does "{topic}" belong to?

Answer with just the domain name (one word):
Examples: meteorology, cosmology, particle_physics, biology, chemistry

Domain:"""

        response = self.generate(prompt, timeout=30)
        if response:
            # Extract first word
            domain = response.strip().split()[0].lower()
            domain = re.sub(r'[^a-z_]', '', domain)
            return domain
        return "unknown"

    def discover_quantities(self, topic: str, domain: str) -> List[str]:
        """Discover measurable quantities for a topic."""
        prompt = f"""For "{topic}" in {domain}, what are the key measurable physical quantities?

List 5-10 quantities that can be measured numerically.
Format: one quantity per line, just the name.

Examples for hurricanes:
- eye_diameter
- radius_of_maximum_wind
- maximum_wind_speed
- central_pressure

Your quantities:"""

        response = self.generate(prompt, timeout=60)
        quantities = []

        if response:
            for line in response.split('\n'):
                line = line.strip().strip('-').strip()
                if line and len(line) < 50:
                    # Clean up
                    q = re.sub(r'[^a-zA-Z0-9_]', '_', line.lower())
                    q = re.sub(r'_+', '_', q).strip('_')
                    if q:
                        quantities.append(q)

        return quantities[:10]

    def discover_ratio_pairs(self, quantities: List[str]) -> List[QuantityPair]:
        """Discover which quantity pairs might have meaningful ratios."""
        prompt = f"""Given these physical quantities:
{chr(10).join('- ' + q for q in quantities)}

Which PAIRS would have physically meaningful RATIOS?
Think about:
- Part/whole relationships (inner/outer, core/total)
- Structural ratios
- Intensity relationships

List 5 pairs in format: quantity_a / quantity_b
Only use quantities from the list above.

Pairs:"""

        response = self.generate(prompt, timeout=60)
        pairs = []

        if response:
            for line in response.split('\n'):
                match = re.search(r'(\w+)\s*/\s*(\w+)', line)
                if match:
                    a, b = match.groups()
                    a = a.lower()
                    b = b.lower()
                    # Verify both are in quantities list (fuzzy match)
                    a_match = next((q for q in quantities if a in q or q in a), None)
                    b_match = next((q for q in quantities if b in q or q in b), None)
                    if a_match and b_match and a_match != b_match:
                        pairs.append(QuantityPair(
                            quantity_a=a_match,
                            quantity_b=b_match,
                            description=f"{a_match} / {b_match}"
                        ))

        return pairs[:5]

    def find_data_sources(self, domain: str, quantities: List[str]) -> List[str]:
        """Find scientific databases for this domain."""
        prompt = f"""What scientific databases have data for {domain}?

I need databases with measurements of:
{chr(10).join('- ' + q for q in quantities[:5])}

List database names and their organizations:
Examples:
- IBTrACS (NOAA) - hurricane track data
- Planck Legacy Archive (ESA) - cosmological parameters
- Particle Data Group (LBNL) - particle physics

Databases:"""

        response = self.generate(prompt, timeout=60)
        sources = []

        if response:
            for line in response.split('\n'):
                line = line.strip().strip('-').strip()
                if line and len(line) < 100:
                    sources.append(line)

        return sources[:5]

    def map_columns(self, quantities: List[str], available_columns: List[str]) -> Dict[str, str]:
        """Map our quantity names to actual column names in data."""
        prompt = f"""I have these quantities I want to measure:
{chr(10).join('- ' + q for q in quantities)}

The dataset has these columns:
{chr(10).join('- ' + c for c in available_columns[:30])}

Map each quantity to the best matching column.
Format: quantity -> column_name

Mappings:"""

        response = self.generate(prompt, timeout=60)
        mappings = {}

        if response:
            for line in response.split('\n'):
                match = re.search(r'(\w+)\s*[->=]+\s*(\w+)', line)
                if match:
                    q, c = match.groups()
                    if c in available_columns or any(c.lower() in col.lower() for col in available_columns):
                        mappings[q.lower()] = c

        return mappings

    def write_finding(self, result: RatioResult, topic: str) -> str:
        """Write up a validated finding."""
        prompt = f"""Write a brief scientific finding:

Topic: {topic}
Discovery: {result.quantity_pair} = {result.best_z2_formula}
Measured: {result.mean_ratio:.4f} ± {result.std_ratio:.4f}
Predicted: {result.z2_value:.4f}
Error: {result.error_percent:.2f}%
N samples: {result.n_samples}
p-value: {result.p_value:.4f}

Write 2-3 sentences explaining this relationship and its significance.

Finding:"""

        return self.generate(prompt, timeout=60)


class Z2Verifier:
    """Python verification engine for Z² relationships."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[Verify {ts}] {msg}")

    def compute_ratios(self, data: pd.DataFrame, col_a: str, col_b: str,
                       filter_col: str = None, filter_value: Any = None) -> np.ndarray:
        """Compute ratio between two columns."""
        # Filter if specified
        df = data.copy()
        if filter_col and filter_value is not None:
            df = df[df[filter_col] == filter_value]

        # Get valid pairs
        valid = df.dropna(subset=[col_a, col_b])
        valid = valid[(valid[col_a] > 0) & (valid[col_b] > 0)]

        if len(valid) == 0:
            return np.array([])

        ratios = valid[col_a].values / valid[col_b].values
        return ratios

    def test_z2_formulas(self, ratios: np.ndarray) -> RatioResult:
        """Test ratios against all Z² formulas."""
        if len(ratios) < 5:
            return None

        mean = ratios.mean()
        std = ratios.std()
        n = len(ratios)

        best_match = None
        best_error = float('inf')

        for name, value in Z2_RATIOS.items():
            error_pct = abs(value - mean) / value * 100

            if error_pct < best_error:
                # t-test against this value
                t_stat, p_value = stats.ttest_1samp(ratios, value)

                best_error = error_pct
                best_match = {
                    "formula": name,
                    "value": value,
                    "error_pct": error_pct,
                    "p_value": p_value
                }

        # Determine verdict
        if best_error < 1:
            verdict = "VALIDATED" if best_match["p_value"] > 0.05 else "STRONG"
        elif best_error < 5:
            verdict = "STRONG" if best_match["p_value"] > 0.01 else "WEAK"
        elif best_error < 10:
            verdict = "WEAK"
        else:
            verdict = "REJECTED"

        return RatioResult(
            quantity_pair="",  # Set by caller
            mean_ratio=mean,
            std_ratio=std,
            n_samples=n,
            best_z2_formula=best_match["formula"],
            z2_value=best_match["value"],
            error_percent=best_error,
            p_value=best_match["p_value"],
            verdict=verdict
        )


class Z2AutoResearch:
    """
    Fully autonomous Z² research system.

    Integrates:
    - Legomena LLM for reasoning
    - Hermes Data Agent for data acquisition
    - Python for verification
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.legomena = LegomenaClient(verbose=verbose)
        self.hermes = HermesDataAgent(verbose=verbose)
        self.verifier = Z2Verifier(verbose=verbose)

        OUTPUT_DIR.mkdir(exist_ok=True)

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[AutoResearch {ts}] {msg}")

    def research(self, topic: str) -> ResearchSession:
        """
        Run complete autonomous research on a topic.

        1. Discover domain and quantities (Legomena)
        2. Find and fetch data (Hermes)
        3. Verify relationships (Python)
        4. Document findings (Legomena)
        """
        self._log(f"\n{'='*70}")
        self._log(f"Z² AUTO-RESEARCH")
        self._log(f"Topic: {topic}")
        self._log(f"{'='*70}")

        session = ResearchSession(
            topic=topic,
            started=datetime.now().isoformat(),
            domain="",
            quantities_discovered=[],
            ratio_pairs=[],
            data_sources=[],
            results=[],
            best_match=None,
            conclusion=""
        )

        # =====================================================================
        # PHASE 1: DISCOVER (Legomena)
        # =====================================================================
        self._log("\n--- PHASE 1: DISCOVER (Legomena) ---")

        # Identify domain
        self._log("Identifying domain...")
        domain = self.legomena.identify_domain(topic)
        session.domain = domain
        self._log(f"Domain: {domain}")

        # Discover quantities
        self._log("Discovering quantities...")
        quantities = self.legomena.discover_quantities(topic, domain)
        session.quantities_discovered = quantities
        self._log(f"Quantities: {quantities}")

        # Discover ratio pairs
        self._log("Discovering ratio pairs...")
        ratio_pairs = self.legomena.discover_ratio_pairs(quantities)
        session.ratio_pairs = [asdict(p) for p in ratio_pairs]
        self._log(f"Ratio pairs: {[p.description for p in ratio_pairs]}")

        # =====================================================================
        # PHASE 2: ACQUIRE DATA (Hermes)
        # =====================================================================
        self._log("\n--- PHASE 2: ACQUIRE DATA (Hermes) ---")

        # Get data based on domain
        datasets = []

        if "hurricane" in topic.lower() or "cyclone" in topic.lower() or domain == "meteorology":
            self._log("Fetching hurricane data from NOAA...")

            # Try Extended Best Track first (more eye data)
            try:
                import requests
                url = "https://rammb2.cira.colostate.edu/wp-content/uploads/2020/11/EBTRK_AL_final_1851-2021_new_format_02-Sep-2022-1.txt"
                response = requests.get(url, timeout=120)

                if response.ok:
                    self._log(f"Downloaded EBTRK: {len(response.content)/1024:.1f}KB")

                    # Parse
                    records = []
                    for line in response.text.strip().split('\n'):
                        parts = line.split()
                        if len(parts) >= 10:
                            try:
                                records.append({
                                    'storm_id': parts[0],
                                    'year': int(parts[3]),
                                    'max_wind': int(parts[6]),
                                    'rmw': int(parts[8]) if parts[8] != '-99' else np.nan,
                                    'eye_diam': int(parts[9]) if parts[9] != '-99' else np.nan
                                })
                            except:
                                continue

                    df = pd.DataFrame(records)
                    self._log(f"Parsed: {len(df)} records")

                    datasets.append(ParsedDataset(
                        source=DataSource(
                            name="Extended Best Track (NOAA/CIRA)",
                            url=url,
                            organization="NOAA/CIRA",
                            format="text",
                            description="Atlantic hurricane extended best track 1851-2021"
                        ),
                        data=df,
                        columns_used=['eye_diam', 'rmw', 'max_wind'],
                        n_rows=len(df),
                        fetch_time=datetime.now().isoformat()
                    ))
            except Exception as e:
                self._log(f"EBTRK fetch failed: {e}")

            # Fallback to IBTrACS
            if not datasets:
                result = self.hermes.fetch_hurricane_data()
                if result:
                    datasets.append(result)

        else:
            # Generic domain - use Hermes search
            datasets = self.hermes.fetch_data_for_domain(domain, quantities)

        session.data_sources = [asdict(d.source) for d in datasets]
        self._log(f"Data sources: {[d.source.name for d in datasets]}")

        if not datasets:
            self._log("No data found!")
            session.conclusion = "No data sources found for this topic."
            session.completed = datetime.now().isoformat()
            return session

        # =====================================================================
        # PHASE 3: VERIFY (Python)
        # =====================================================================
        self._log("\n--- PHASE 3: VERIFY (Python) ---")

        results = []

        for dataset in datasets:
            df = dataset.data
            self._log(f"Analyzing {dataset.source.name}...")

            # For hurricanes, we know the key relationship
            if 'eye_diam' in df.columns and 'rmw' in df.columns:
                # Convert eye diameter to radius
                df['eye_radius'] = df['eye_diam'] / 2

                # Compute Saffir-Simpson category
                def wind_to_cat(w):
                    if w >= 137: return 5
                    elif w >= 113: return 4
                    elif w >= 96: return 3
                    elif w >= 83: return 2
                    elif w >= 64: return 1
                    elif w >= 34: return 0
                    else: return -1

                df['category'] = df['max_wind'].apply(wind_to_cat)

                # Test each category
                for cat in range(1, 6):
                    ratios = self.verifier.compute_ratios(
                        df, 'eye_radius', 'rmw',
                        filter_col='category', filter_value=cat
                    )

                    if len(ratios) >= 10:
                        result = self.verifier.test_z2_formulas(ratios)
                        if result:
                            result.quantity_pair = f"eye_radius/RMW (Cat {cat})"
                            results.append(result)
                            self._log(f"  Cat {cat}: ratio={result.mean_ratio:.4f}, "
                                     f"matches {result.best_z2_formula} ({result.error_percent:.2f}%), "
                                     f"verdict={result.verdict}")

            # Also check IBTrACS columns
            elif 'USA_EYE' in df.columns and 'USA_RMW' in df.columns:
                df['eye_radius'] = pd.to_numeric(df['USA_EYE'], errors='coerce') / 2
                df['rmw'] = pd.to_numeric(df['USA_RMW'], errors='coerce')

                ratios = self.verifier.compute_ratios(df, 'eye_radius', 'rmw')
                if len(ratios) >= 10:
                    result = self.verifier.test_z2_formulas(ratios)
                    if result:
                        result.quantity_pair = "eye_radius/RMW"
                        results.append(result)

        session.results = [asdict(r) for r in results]

        # Find best match
        validated = [r for r in results if r.verdict in ["VALIDATED", "STRONG"]]
        if validated:
            best = min(validated, key=lambda r: r.error_percent)
            session.best_match = asdict(best)
            self._log(f"\nBest match: {best.quantity_pair} = {best.best_z2_formula} "
                     f"({best.error_percent:.2f}%)")

        # =====================================================================
        # PHASE 4: DOCUMENT (Legomena)
        # =====================================================================
        self._log("\n--- PHASE 4: DOCUMENT (Legomena) ---")

        if session.best_match:
            best = validated[0]
            finding = self.legomena.write_finding(best, topic)

            session.conclusion = f"""Z² RELATIONSHIP DISCOVERED
Topic: {topic}
Relationship: {best.quantity_pair} = {best.best_z2_formula}
Measured: {best.mean_ratio:.4f} ± {best.std_ratio:.4f}
Predicted: {best.z2_value:.4f}
Error: {best.error_percent:.2f}%
N: {best.n_samples}
Verdict: {best.verdict}

{finding or ''}"""
        else:
            session.conclusion = f"No Z² relationships found in {topic}"

        session.completed = datetime.now().isoformat()

        # Save results
        slug = topic.lower().replace(" ", "_")[:30]
        output_dir = OUTPUT_DIR / f"session_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(exist_ok=True)

        with open(output_dir / "session.json", "w") as f:
            json.dump(asdict(session), f, indent=2, default=str)

        with open(output_dir / "conclusion.txt", "w") as f:
            f.write(session.conclusion)

        self._log(f"\nSaved to: {output_dir}")

        return session


def main():
    """Run autonomous Z² research."""
    topic = sys.argv[1] if len(sys.argv) > 1 else "hurricane eye and wind structure"

    researcher = Z2AutoResearch()
    session = researcher.research(topic)

    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print(session.conclusion)


if __name__ == "__main__":
    main()
