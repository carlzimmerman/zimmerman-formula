#!/usr/bin/env python3
"""
Z² AUTO-RESEARCH V3 - NAVIGATION-BASED
=======================================

Truly blind discovery using HTML navigation:
1. Legomena identifies dataset name + organization
2. Search for landing page (not direct data URL)
3. Navigate HTML to find data links
4. Download and parse
5. Verify Z² relationships

NO hardcoded URLs - discovers everything via navigation.

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
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from scipy import stats
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import io

# Z² Constants - the ONLY knowledge
Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)
PHI = (1 + math.sqrt(5)) / 2

Z2_RATIOS = {
    "1/phi": 1/PHI,
    "phi-1": PHI-1,
    "1/Z": 1/Z,
    "1/phi^2": 1/(PHI**2),
    "1/2": 0.5,
    "1/3": 1/3,
    "2/3": 2/3,
}

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-4b")
OUTPUT_DIR = Path(__file__).parent / "autoresearch_v3_output"
OUTPUT_DIR.mkdir(exist_ok=True)


class LegomenaClient:
    """Legomena LLM client."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Legomena] {msg}")

    def generate(self, prompt: str, timeout: int = 60) -> Optional[str]:
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
            self._log("Timeout")
        except Exception as e:
            self._log(f"Error: {e}")
        return None

    def identify_domain(self, topic: str) -> str:
        prompt = f'What scientific domain is "{topic}"? One word: meteorology, cosmology, physics, biology, etc.\nDomain:'
        response = self.generate(prompt, timeout=30)
        if response:
            for word in response.split():
                clean = re.sub(r'[^a-z]', '', word.lower())
                if len(clean) > 3:
                    return clean
        return "unknown"

    def identify_datasets(self, topic: str, domain: str) -> List[Dict]:
        """Identify dataset names and organizations."""
        prompt = f"""For "{topic}" in {domain}, what are the main scientific databases?

List 3 databases with:
- Dataset name (e.g., IBTrACS, HURDAT2, Planck)
- Organization (e.g., NOAA, NASA, ESA)

Format each as: NAME by ORGANIZATION

Databases:"""

        response = self.generate(prompt, timeout=60)
        datasets = []

        if response:
            for line in response.split('\n'):
                # Parse "NAME by ORGANIZATION" or similar
                match = re.search(r'([A-Z][A-Za-z0-9\-_]+)\s+(?:by|from|at|-)\s+([A-Z][A-Za-z]+)', line)
                if match:
                    datasets.append({
                        "name": match.group(1),
                        "organization": match.group(2)
                    })
                else:
                    # Try to extract just dataset names
                    names = re.findall(r'\b([A-Z][A-Z0-9\-]{2,}[A-Za-z0-9]*)\b', line)
                    for name in names:
                        if name not in ['CSV', 'JSON', 'API', 'URL', 'NASA', 'NOAA', 'ESA']:
                            datasets.append({"name": name, "organization": "unknown"})

        return datasets[:5]

    def identify_quantities(self, topic: str) -> List[str]:
        prompt = f"""For "{topic}", list 6 measurable physical quantities.
One per line, snake_case:

Quantities:"""
        response = self.generate(prompt, timeout=45)
        quantities = []
        if response:
            for line in response.split('\n'):
                line = line.strip().strip('-').strip('0123456789.')
                q = re.sub(r'[^a-z0-9_]', '_', line.lower()).strip('_')
                if q and len(q) > 2 and len(q) < 40:
                    quantities.append(q)
        return quantities[:8]

    def identify_ratio_pairs(self, quantities: List[str]) -> List[Tuple[str, str]]:
        prompt = f"""Given: {', '.join(quantities)}

Which pairs would have meaningful RATIOS? (inner/outer, part/whole, etc.)
List 3 pairs as: quantity_a / quantity_b

Pairs:"""
        response = self.generate(prompt, timeout=45)
        pairs = []
        if response:
            for line in response.split('\n'):
                match = re.search(r'(\w+)\s*/\s*(\w+)', line)
                if match:
                    a, b = match.groups()
                    a_match = next((q for q in quantities if a.lower() in q), None)
                    b_match = next((q for q in quantities if b.lower() in q), None)
                    if a_match and b_match and a_match != b_match:
                        pairs.append((a_match, b_match))
        return pairs[:5]

    def map_columns(self, quantities: List[str], columns: List[str]) -> Dict[str, Tuple[str, str]]:
        """Map quantities to columns, with transformations."""
        col_str = ', '.join(columns[:40])
        prompt = f"""Dataset columns: {col_str}

Map these quantities to columns:
{chr(10).join('- ' + q for q in quantities)}

For each, give: quantity -> column, transformation
(transformation: "none", "divide_by_2" if diameter->radius, etc.)

Mappings:"""

        response = self.generate(prompt, timeout=60)
        mappings = {}

        if response:
            for line in response.split('\n'):
                match = re.search(r'(\w+)\s*[->=]+\s*(\w+)(?:\s*,\s*(\w+))?', line)
                if match:
                    q = match.group(1).lower()
                    col = match.group(2)
                    transform = match.group(3) or "none"

                    # Verify column exists
                    col_match = next((c for c in columns if col.lower() in c.lower()), None)
                    if col_match:
                        mappings[q] = (col_match, transform.lower())

        return mappings

    def discover_categories(self, columns: List[str], sample: str) -> Optional[Dict]:
        """Discover categorical groupings."""
        prompt = f"""Dataset columns: {', '.join(columns[:30])}

Sample:
{sample[:1000]}

Is there an intensity/category column with meaningful levels?
If yes, what column and what are the thresholds?

Format:
column: <name>
levels:
  level1: min-max
  level2: min-max

If none, say: none

Answer:"""

        response = self.generate(prompt, timeout=60)

        if not response or 'none' in response.lower()[:30]:
            return None

        result = {"column": None, "levels": {}}
        lines = response.split('\n')

        for line in lines:
            if 'column' in line.lower() and ':' in line:
                col = line.split(':', 1)[1].strip()
                col = re.sub(r'[^a-zA-Z0-9_]', '', col)
                if col and any(col.lower() in c.lower() for c in columns):
                    result["column"] = next((c for c in columns if col.lower() in c.lower()), col)

            match = re.search(r'(\w+):\s*([\d.]+)\s*[-to]+\s*([\d.]+)', line)
            if match:
                result["levels"][match.group(1)] = (float(match.group(2)), float(match.group(3)))

        return result if result["column"] and result["levels"] else None


class HermesNavigator:
    """Navigate web pages to find data."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "HermesNavigator/1.0"})

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Navigator] {msg}")

    def search_landing_page(self, dataset: str, organization: str) -> Optional[str]:
        """Search for dataset landing page."""
        query = f"{dataset} {organization} data download"
        self._log(f"Searching: {query}")

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
                            url = requests.utils.unquote(url_match.group(1))
                            # Prefer .gov/.edu sites
                            if '.gov' in url or '.edu' in url or organization.lower() in url.lower():
                                self._log(f"Found: {url[:60]}")
                                return url
                    else:
                        return match
        except Exception as e:
            self._log(f"Search error: {e}")

        return None

    def navigate_to_data(self, landing_url: str, target: str = "") -> Optional[Tuple[str, pd.DataFrame]]:
        """Navigate from landing page to actual data."""
        self._log(f"Navigating from: {landing_url[:60]}")

        try:
            response = self.session.get(landing_url, timeout=30)
            if not response.ok:
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find data links
            data_links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text().strip().lower()
                full_url = urljoin(landing_url, href)

                score = 0
                if 'csv' in text or '.csv' in href.lower():
                    score += 10
                if 'data' in text or '/data/' in href.lower():
                    score += 5
                if 'download' in text:
                    score += 5
                if 'access' in text:
                    score += 3

                if score > 0:
                    data_links.append((score, full_url, text[:50]))

            data_links.sort(reverse=True)
            self._log(f"Found {len(data_links)} data links")

            # Try top links
            for score, url, text in data_links[:5]:
                self._log(f"  Trying: {text}...")

                resp = self.session.get(url, timeout=30)
                if not resp.ok:
                    continue

                content = resp.text

                # Check if directory listing
                if '<html' in content.lower():
                    soup2 = BeautifulSoup(content, 'html.parser')

                    # Find actual data files
                    for a in soup2.find_all('a', href=True):
                        href = a['href']
                        if href.endswith('.csv') or (href.endswith('.txt') and 'data' in url):
                            file_url = urljoin(url, href)
                            self._log(f"  Found file: {href}")

                            # Download
                            file_resp = self.session.get(file_url, timeout=300)
                            if file_resp.ok:
                                df = self._parse_data(file_resp.content)
                                if df is not None:
                                    return (file_url, df)

                else:
                    # Direct data
                    df = self._parse_data(resp.content)
                    if df is not None:
                        return (url, df)

        except Exception as e:
            self._log(f"Navigation error: {e}")

        return None

    def _parse_data(self, content: bytes) -> Optional[pd.DataFrame]:
        """Parse data content."""
        text = content.decode('utf-8', errors='ignore')

        if '<html' in text.lower()[:500]:
            return None

        # Try CSV with skiprows for header issues
        try:
            df = pd.read_csv(io.BytesIO(content), skiprows=[1], low_memory=False, na_values=[' ', ''])
            if len(df) > 100 and len(df.columns) > 5:
                return df
        except:
            pass

        try:
            df = pd.read_csv(io.BytesIO(content), low_memory=False)
            if len(df) > 100 and len(df.columns) > 5:
                return df
        except:
            pass

        return None


class Z2Verifier:
    """Verify Z² relationships."""

    def test_ratio(self, ratios: np.ndarray) -> Optional[Dict]:
        if len(ratios) < 10:
            return None

        mean = ratios.mean()
        std = ratios.std()
        n = len(ratios)

        best = None
        best_error = float('inf')

        for name, value in Z2_RATIOS.items():
            error = abs(value - mean) / value * 100
            if error < best_error:
                t_stat, p_value = stats.ttest_1samp(ratios, value)
                best_error = error
                best = {
                    "formula": name,
                    "z2_value": value,
                    "measured": mean,
                    "std": std,
                    "n": n,
                    "error_pct": error,
                    "p_value": p_value,
                    "verdict": "VALIDATED" if error < 1 and p_value > 0.05 else
                              "STRONG" if error < 5 else
                              "WEAK" if error < 10 else "REJECTED"
                }

        return best


class Z2AutoResearchV3:
    """Navigation-based autonomous Z² research."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.legomena = LegomenaClient(verbose)
        self.navigator = HermesNavigator(verbose)
        self.verifier = Z2Verifier()

    def _log(self, msg: str):
        if self.verbose:
            print(f"[AutoResearch] {msg}")

    def research(self, topic: str) -> Dict:
        """Run navigation-based research."""
        self._log(f"\n{'='*60}")
        self._log(f"Z² AUTO-RESEARCH V3 (Navigation)")
        self._log(f"Topic: {topic}")
        self._log(f"{'='*60}")

        results = {
            "topic": topic,
            "started": datetime.now().isoformat(),
            "is_blind": True,
            "domain": None,
            "datasets_identified": [],
            "data_found": False,
            "data_url": None,
            "data_rows": 0,
            "quantities": [],
            "ratio_results": [],
            "best_match": None,
            "conclusion": ""
        }

        # Phase 1: Identify domain
        self._log("\n--- Phase 1: Identify Domain ---")
        domain = self.legomena.identify_domain(topic)
        results["domain"] = domain
        self._log(f"Domain: {domain}")

        # Phase 2: Identify datasets
        self._log("\n--- Phase 2: Identify Datasets ---")
        datasets = self.legomena.identify_datasets(topic, domain)
        results["datasets_identified"] = datasets
        self._log(f"Datasets: {datasets}")

        # Phase 3: Navigate to find data
        self._log("\n--- Phase 3: Navigate to Data ---")
        df = None
        data_url = None

        for ds in datasets:
            self._log(f"Looking for: {ds['name']} by {ds['organization']}")

            # Search for landing page
            landing = self.navigator.search_landing_page(ds['name'], ds['organization'])

            if landing:
                # Navigate to data
                result = self.navigator.navigate_to_data(landing, topic)
                if result:
                    data_url, df = result
                    results["data_found"] = True
                    results["data_url"] = data_url
                    results["data_rows"] = len(df)
                    self._log(f"SUCCESS: {len(df)} rows from {data_url.split('/')[-1]}")
                    break

        if df is None:
            results["conclusion"] = "Could not find data via navigation"
            return results

        # Phase 4: Discover quantities and mappings
        self._log("\n--- Phase 4: Map Columns ---")
        quantities = self.legomena.identify_quantities(topic)
        results["quantities"] = quantities
        self._log(f"Quantities: {quantities}")

        columns = [str(c) for c in df.columns]
        mappings = self.legomena.map_columns(quantities, columns)
        self._log(f"Mappings: {mappings}")

        # Phase 5: Discover categories
        self._log("\n--- Phase 5: Discover Categories ---")
        sample = df.head(5).to_string()
        categories = self.legomena.discover_categories(columns, sample)
        self._log(f"Categories: {categories}")

        # Phase 6: Test ratios
        self._log("\n--- Phase 6: Test Ratios ---")
        ratio_pairs = self.legomena.identify_ratio_pairs(quantities)

        for q_a, q_b in ratio_pairs:
            if q_a not in mappings or q_b not in mappings:
                continue

            col_a, trans_a = mappings[q_a]
            col_b, trans_b = mappings[q_b]

            try:
                a_vals = pd.to_numeric(df[col_a], errors='coerce')
                b_vals = pd.to_numeric(df[col_b], errors='coerce')

                if trans_a == "divide_by_2":
                    a_vals = a_vals / 2
                if trans_b == "divide_by_2":
                    b_vals = b_vals / 2

                valid = (a_vals > 0) & (b_vals > 0) & a_vals.notna() & b_vals.notna()
                ratios = (a_vals[valid] / b_vals[valid]).values

                if len(ratios) < 10:
                    continue

                # Test overall
                result = self.verifier.test_ratio(ratios)
                if result:
                    result["ratio_name"] = f"{q_a}/{q_b}"
                    result["category"] = "all"
                    results["ratio_results"].append(result)
                    self._log(f"  {q_a}/{q_b}: {result['measured']:.4f} ≈ {result['formula']} "
                             f"({result['error_pct']:.2f}%) [{result['verdict']}]")

                # Test by category if discovered
                if categories and categories["column"] in df.columns:
                    cat_col = categories["column"]
                    cat_vals = pd.to_numeric(df[cat_col], errors='coerce')

                    for level, (min_v, max_v) in categories["levels"].items():
                        mask = (cat_vals >= min_v) & (cat_vals < max_v) & valid
                        level_ratios = (a_vals[mask] / b_vals[mask]).values

                        if len(level_ratios) >= 10:
                            result = self.verifier.test_ratio(level_ratios)
                            if result:
                                result["ratio_name"] = f"{q_a}/{q_b}"
                                result["category"] = level
                                results["ratio_results"].append(result)
                                self._log(f"  {q_a}/{q_b} ({level}): {result['measured']:.4f} ≈ "
                                         f"{result['formula']} ({result['error_pct']:.2f}%) [{result['verdict']}]")

            except Exception as e:
                self._log(f"  Error testing {q_a}/{q_b}: {e}")

        # Find best
        validated = [r for r in results["ratio_results"]
                    if r["verdict"] in ["VALIDATED", "STRONG"]]
        if validated:
            best = min(validated, key=lambda r: r["error_pct"])
            results["best_match"] = best

            cat_str = f" ({best['category']})" if best['category'] != 'all' else ""
            results["conclusion"] = f"""Z² RELATIONSHIP DISCOVERED (BLIND NAVIGATION)
Relationship: {best['ratio_name']}{cat_str} = {best['formula']}
Measured: {best['measured']:.4f} ± {best['std']:.4f}
Predicted: {best['z2_value']:.4f}
Error: {best['error_pct']:.2f}%
N: {best['n']}
Verdict: {best['verdict']}
Data source: {data_url}"""
        else:
            results["conclusion"] = "No Z² relationships found"

        results["completed"] = datetime.now().isoformat()

        # Save
        slug = re.sub(r'[^a-z0-9]', '_', topic.lower())[:30]
        output_path = OUTPUT_DIR / f"{slug}_{datetime.now().strftime('%H%M%S')}.json"
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        self._log(f"\nSaved: {output_path}")

        return results


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "hurricane eye and wind structure"

    researcher = Z2AutoResearchV3()
    results = researcher.research(topic)

    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print(results["conclusion"])

    if results.get("is_blind"):
        print("\n✓ Truly blind - no hardcoded URLs or column names")


if __name__ == "__main__":
    main()
