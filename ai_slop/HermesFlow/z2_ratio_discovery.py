#!/usr/bin/env python3
"""
Z² RATIO DISCOVERY ENGINE
==========================

Discovers Z² relationships by finding RATIOS between quantities.

Key insight: Manual research found eye/RMW = 1/φ, not raw values.
This engine:
1. Discovers domain-specific quantities
2. Extracts PAIRED measurements (both values from same observation)
3. Computes RATIOS between quantities
4. Tests ratios against Z² formulas

NO domain knowledge - discovers everything dynamically.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import re
import json
import math
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# Z² Constants - ALL the system knows
Z2 = 32 * math.pi / 3   # ≈ 33.51
Z = math.sqrt(Z2)        # ≈ 5.79
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618

# Candidate ratio formulas
Z2_RATIOS = {
    "1/phi": 1/PHI,           # 0.618 - golden ratio reciprocal
    "phi-1": PHI-1,           # 0.618 - same as 1/φ
    "1/Z": 1/Z,               # 0.173
    "1/Z2": 1/Z2,             # 0.030
    "Z/Z2": Z/Z2,             # 0.173 - same as 1/Z
    "1/2": 0.5,
    "1/3": 1/3,               # 0.333
    "2/3": 2/3,               # 0.667
    "1/4": 0.25,
    "3/4": 0.75,
    "1/5": 0.2,
    "1/6": 1/6,               # 0.167
    "1/pi": 1/math.pi,        # 0.318
    "1/e": 1/math.e,          # 0.368
    "phi/Z": PHI/Z,           # 0.279
    "Z/10": Z/10,             # 0.579
    "phi/2": PHI/2,           # 0.809
    "1/phi^2": 1/(PHI**2),    # 0.382
}

LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-31b")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "180"))
OUTPUT_DIR = Path(__file__).parent / "hermesflow_research_output"


@dataclass
class PairedMeasurement:
    """A paired measurement (two quantities from same observation)."""
    quantity_a: str
    value_a: float
    quantity_b: str
    value_b: float
    ratio: float  # a/b
    source: str
    context: str


@dataclass
class RatioMatch:
    """A ratio matching a Z² formula."""
    ratio_name: str  # e.g., "eye_diameter/RMW"
    mean_ratio: float
    z2_formula: str
    z2_value: float
    error_percent: float
    n_samples: int
    std_dev: float
    verdict: str


class Z2RatioDiscovery:
    """Discover Z² relationships through ratio analysis."""

    def __init__(self, use_legomena: bool = True, verbose: bool = True):
        self.use_legomena = use_legomena
        self.verbose = verbose
        OUTPUT_DIR.mkdir(exist_ok=True)

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] {msg}")

    def _call_legomena(self, prompt: str, timeout: int = None) -> Optional[str]:
        if not self.use_legomena:
            return None
        timeout = timeout or LEGOMENA_TIMEOUT
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
            self._log(f"Timeout ({timeout}s)")
        except Exception as e:
            self._log(f"Error: {e}")
        return None

    def discover_quantity_pairs(self, topic: str) -> List[Tuple[str, str]]:
        """
        Discover pairs of quantities whose RATIO might be meaningful.

        Returns pairs like: [("eye_diameter", "radius_of_max_wind"), ...]
        """
        prompt = f"""For "{topic}", what PAIRS of physical quantities have meaningful RATIOS?

Think about:
- Structural ratios (part/whole, inner/outer)
- Scale relationships (small/large)
- Intensity ratios (strong/weak)

List 5 pairs where the RATIO between them might reveal physics.
Format: quantity_a / quantity_b

Examples of good ratio pairs:
- eye_diameter / outer_radius
- core_pressure / ambient_pressure
- inner_speed / outer_speed

Your 5 pairs (format: "A / B"):
1."""

        response = self._call_legomena(prompt, timeout=120)
        pairs = []

        if response:
            # Parse pairs from response
            lines = response.split('\n')
            for line in lines:
                match = re.search(r'(\w+(?:_\w+)*)\s*/\s*(\w+(?:_\w+)*)', line)
                if match:
                    pairs.append((match.group(1), match.group(2)))

        # Fallback generic pairs
        if not pairs:
            pairs = [
                ("inner", "outer"),
                ("center", "edge"),
                ("core", "total"),
            ]

        return pairs[:5]

    def fetch_paired_data(self, topic: str, pairs: List[Tuple[str, str]]) -> List[PairedMeasurement]:
        """
        Fetch PAIRED measurements from Wikipedia.

        Looks for cases where BOTH quantities are mentioned together.
        """
        measurements = []

        # Search Wikipedia for the topic
        try:
            # Search for main article
            search_response = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": topic,
                    "format": "json",
                    "srlimit": 5
                },
                headers={"User-Agent": "HermesFlow/2.0"},
                timeout=10
            )

            if not search_response.ok:
                return measurements

            results = search_response.json().get("query", {}).get("search", [])

            for result in results[:3]:
                pageid = result.get("pageid")
                title = result.get("title", "")

                # Fetch full content
                content_response = requests.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "pageids": pageid,
                        "prop": "extracts",
                        "explaintext": True,
                        "format": "json"
                    },
                    headers={"User-Agent": "HermesFlow/2.0"},
                    timeout=30
                )

                if not content_response.ok:
                    continue

                pages = content_response.json().get("query", {}).get("pages", {})
                for page in pages.values():
                    content = page.get("extract", "")

                    # Use LLM to extract paired measurements
                    for q_a, q_b in pairs:
                        prompt = f"""From this Wikipedia article, find PAIRED measurements.

I need cases where BOTH "{q_a}" AND "{q_b}" are mentioned with numerical values.

ARTICLE: {title}
CONTENT (first 5000 chars):
{content[:5000]}

Find pairs where both quantities have values in the SAME context.
Return as JSON array:
[
    {{"a_value": <number>, "b_value": <number>, "context": "<where found>"}},
    ...
]

If no pairs found, return: []

JSON:"""

                        extraction = self._call_legomena(prompt, timeout=90)

                        if extraction:
                            try:
                                json_match = re.search(r'\[[\s\S]*?\]', extraction)
                                if json_match:
                                    data = json.loads(json_match.group())
                                    for pair in data:
                                        a_val = float(pair.get("a_value", 0))
                                        b_val = float(pair.get("b_value", 0))
                                        if a_val > 0 and b_val > 0:
                                            measurements.append(PairedMeasurement(
                                                quantity_a=q_a,
                                                value_a=a_val,
                                                quantity_b=q_b,
                                                value_b=b_val,
                                                ratio=a_val/b_val,
                                                source=f"Wikipedia: {title}",
                                                context=pair.get("context", "")[:100]
                                            ))
                            except (json.JSONDecodeError, ValueError):
                                pass

        except Exception as e:
            self._log(f"Fetch error: {e}")

        return measurements

    def analyze_ratios(self, measurements: List[PairedMeasurement]) -> List[RatioMatch]:
        """
        Analyze ratios against Z² formulas.
        """
        matches = []

        # Group by quantity pair
        pair_ratios: Dict[str, List[float]] = {}
        for m in measurements:
            key = f"{m.quantity_a}/{m.quantity_b}"
            if key not in pair_ratios:
                pair_ratios[key] = []
            pair_ratios[key].append(m.ratio)

        # Test each pair against Z² formulas
        for ratio_name, ratios in pair_ratios.items():
            if len(ratios) < 2:
                continue

            mean = sum(ratios) / len(ratios)
            variance = sum((r - mean) ** 2 for r in ratios) / len(ratios)
            std = math.sqrt(variance) if variance > 0 else 0.01

            self._log(f"  {ratio_name}: mean={mean:.4f}, std={std:.4f}, n={len(ratios)}")

            for formula_name, formula_value in Z2_RATIOS.items():
                error = abs(formula_value - mean)
                error_pct = (error / mean) * 100 if mean != 0 else float('inf')

                if error_pct > 20:  # Skip poor matches
                    continue

                sigma = error / std if std > 0 else float('inf')

                if error_pct < 5:
                    verdict = "STRONG" if sigma < 2 else "INTERESTING"
                elif error_pct < 10:
                    verdict = "WEAK"
                else:
                    verdict = "MARGINAL"

                matches.append(RatioMatch(
                    ratio_name=ratio_name,
                    mean_ratio=mean,
                    z2_formula=formula_name,
                    z2_value=formula_value,
                    error_percent=error_pct,
                    n_samples=len(ratios),
                    std_dev=std,
                    verdict=verdict
                ))

        # Sort by error
        matches.sort(key=lambda m: m.error_percent)
        return matches

    def run(self, topic: str) -> Dict:
        """Run complete ratio discovery."""
        self._log(f"\n{'='*70}")
        self._log(f"Z² RATIO DISCOVERY")
        self._log(f"Topic: {topic}")
        self._log(f"{'='*70}")
        self._log(f"\nKnows ONLY: Z²={Z2:.4f}, Z={Z:.4f}, φ={PHI:.4f}")
        self._log(f"Looking for RATIOS, not raw values.\n")

        results = {
            "topic": topic,
            "started": datetime.now().isoformat(),
            "quantity_pairs": [],
            "paired_measurements": [],
            "ratio_matches": [],
            "best_match": None,
            "conclusion": ""
        }

        # Step 1: Discover quantity pairs
        self._log("--- Step 1: Discover Quantity Pairs ---")
        pairs = self.discover_quantity_pairs(topic)
        results["quantity_pairs"] = pairs
        self._log(f"Found {len(pairs)} pairs:")
        for a, b in pairs:
            self._log(f"  - {a} / {b}")

        # Step 2: Fetch paired measurements
        self._log("\n--- Step 2: Fetch Paired Measurements ---")
        measurements = self.fetch_paired_data(topic, pairs)
        results["paired_measurements"] = [asdict(m) for m in measurements]
        self._log(f"Found {len(measurements)} paired measurements")

        # Step 3: Analyze ratios
        self._log("\n--- Step 3: Analyze Ratios ---")
        matches = self.analyze_ratios(measurements)
        results["ratio_matches"] = [asdict(m) for m in matches]

        self._log(f"\nZ² Ratio Matches:")
        for m in matches[:10]:
            self._log(f"  {m.verdict}: {m.ratio_name} ≈ {m.z2_formula} ({m.error_percent:.2f}%)")

        if matches:
            results["best_match"] = asdict(matches[0])
            self._log(f"\nBest match: {matches[0].ratio_name} = {matches[0].z2_formula}")

        # Conclusion
        if matches and matches[0].error_percent < 5:
            results["conclusion"] = f"FOUND: {matches[0].ratio_name} ≈ {matches[0].z2_formula} ({matches[0].error_percent:.2f}%)"
        else:
            results["conclusion"] = "No strong Z² ratio relationships found in available data."

        # Save
        slug = topic.lower().replace(" ", "_")[:40]
        output_dir = OUTPUT_DIR / f"ratio_{slug}"
        output_dir.mkdir(exist_ok=True)
        with open(output_dir / "results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        self._log(f"\nSaved to: {output_dir}")

        results["completed"] = datetime.now().isoformat()
        return results


def main():
    """Run ratio discovery."""
    topic = sys.argv[1] if len(sys.argv) > 1 else "hurricane eye and wind structure"

    discovery = Z2RatioDiscovery()
    results = discovery.run(topic)

    print("\n" + "="*70)
    print(results["conclusion"])
    print("="*70)


if __name__ == "__main__":
    main()
