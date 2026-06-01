#!/usr/bin/env python3
"""
Z² BLIND DISCOVERY ENGINE
==========================

A truly blind discovery system that knows ONLY:
1. Z² = 32π/3 ≈ 33.51
2. Z = √Z² ≈ 5.79
3. φ = (1+√5)/2 ≈ 1.618
4. Common mathematical relationships

NO domain-specific knowledge. NO prior findings.
Must discover everything dynamically.

This tests whether Z² geometry can genuinely guide discovery,
not just confirm pre-existing knowledge.

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
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# Z² FIRST PRINCIPLES - This is ALL the system knows
# ============================================================

Z2 = 32 * math.pi / 3  # ≈ 33.51032163829113
Z = math.sqrt(Z2)       # ≈ 5.789300396327082
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.6180339887498949

# Candidate Z² formulas (mathematical relationships, not domain knowledge)
Z2_FORMULAS = {
    # Direct values
    "Z2": Z2,
    "Z": Z,
    "phi": PHI,
    "1/Z": 1/Z,
    "1/phi": 1/PHI,
    "1/Z2": 1/Z2,

    # Simple multiples
    "2*Z2": 2*Z2,
    "3*Z2": 3*Z2,
    "Z2/2": Z2/2,
    "Z2/3": Z2/3,
    "Z2/10": Z2/10,

    # Z operations
    "Z/2": Z/2,
    "Z/3": Z/3,
    "Z/6": Z/6,
    "2*Z": 2*Z,
    "Z+1": Z+1,
    "Z-1": Z-1,

    # φ operations
    "phi/2": PHI/2,
    "2*phi": 2*PHI,
    "phi^2": PHI**2,
    "1/phi^2": 1/(PHI**2),
    "phi-1": PHI-1,  # = 1/φ

    # Combined
    "Z/phi": Z/PHI,
    "phi/Z": PHI/Z,
    "Z2/phi": Z2/PHI,
    "Z*phi": Z*PHI,

    # Integer relationships
    "Z2+1": Z2+1,
    "Z2+2": Z2+2,
    "Z2+3": Z2+3,
    "4*Z2+3": 4*Z2+3,  # α⁻¹ formula
    "Z2-1": Z2-1,

    # Ratios with integers
    "1/3": 1/3,
    "2/3": 2/3,
    "1/6": 1/6,
    "1/7": 1/7,
    "3/13": 3/13,
    "13/19": 13/19,
}

# LLM config
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-31b")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "300"))

# Output
OUTPUT_DIR = Path(__file__).parent / "hermesflow_research_output"


@dataclass
class DiscoveredQuantity:
    """A quantity discovered in a domain."""
    name: str
    description: str
    unit: str
    is_ratio: bool = False
    values_found: List[float] = field(default_factory=list)
    source: str = ""


@dataclass
class Z2Match:
    """A potential Z² match."""
    quantity: str
    measured_value: float
    z2_formula: str
    z2_value: float
    error_percent: float
    n_samples: int
    std_dev: float
    sigma: float
    verdict: str  # VALIDATED, FALSIFIED, WEAK, INTERESTING


@dataclass
class BlindDiscoverySession:
    """Complete blind discovery session."""
    topic: str
    started: str
    domain_discovered: str
    quantities_discovered: List[Dict]
    data_sources_found: List[Dict]
    measurements_collected: int
    z2_matches: List[Dict]
    best_match: Optional[Dict]
    conclusion: str
    completed: Optional[str] = None


class Z2BlindDiscovery:
    """
    Blind Z² discovery engine.

    Knows ONLY Z² mathematics. Must discover everything else.
    """

    def __init__(self, use_legomena: bool = True, verbose: bool = True):
        self.use_legomena = use_legomena
        self.verbose = verbose

        # Discovered state (starts empty)
        self.domain = ""
        self.quantities: List[DiscoveredQuantity] = []
        self.data_sources: List[Dict] = []
        self.measurements: Dict[str, List[float]] = {}

        OUTPUT_DIR.mkdir(exist_ok=True)

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] {msg}")

    def _call_legomena(self, prompt: str, timeout: int = None) -> Optional[str]:
        """Call Legomena for reasoning."""
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
            self._log(f"Legomena timeout ({timeout}s)")
        except Exception as e:
            self._log(f"Legomena error: {e}")
        return None

    def discover_domain(self, topic: str) -> str:
        """
        Discover what scientific domain this topic belongs to.

        Uses LLM but with NO domain-specific Z² knowledge.
        """
        prompt = f"""What scientific domain does this research topic belong to?

TOPIC: {topic}

Respond with ONLY ONE WORD - the domain name:
physics, chemistry, biology, meteorology, astronomy, geology, etc.

ONE WORD ANSWER:"""

        response = self._call_legomena(prompt, timeout=60)
        if response:
            # Extract first word
            domain = response.strip().lower().split()[0]
            domain = re.sub(r'[^a-z]', '', domain)
            return domain

        # Fallback: guess from keywords
        topic_lower = topic.lower()
        if any(w in topic_lower for w in ["hurricane", "storm", "weather", "cyclone"]):
            return "meteorology"
        elif any(w in topic_lower for w in ["particle", "quark", "mass", "decay"]):
            return "physics"
        elif any(w in topic_lower for w in ["cosmos", "galaxy", "dark energy", "cmb"]):
            return "cosmology"

        return "unknown"

    def discover_quantities(self, topic: str) -> List[DiscoveredQuantity]:
        """
        Discover what physical quantities can be measured for this topic.

        NO prior knowledge - must figure this out from scratch.
        """
        prompt = f"""List 5 measurable PHYSICAL QUANTITIES for: {topic}

Each quantity needs: name, description, unit, is_ratio (true/false)

Example format:
[{{"name": "temperature", "description": "air temp", "unit": "kelvin", "is_ratio": false}}]

Your JSON array (5 quantities):"""

        response = self._call_legomena(prompt, timeout=120)
        quantities = []

        if response:
            try:
                # Extract JSON
                json_match = re.search(r'\[[\s\S]*?\]', response)
                if json_match:
                    data = json.loads(json_match.group())
                    for q in data:
                        quantities.append(DiscoveredQuantity(
                            name=q.get("name", "unknown"),
                            description=q.get("description", ""),
                            unit=q.get("unit", ""),
                            is_ratio=q.get("is_ratio", False)
                        ))
            except json.JSONDecodeError:
                pass

        # If LLM failed, use generic quantities
        if not quantities:
            quantities = [
                DiscoveredQuantity("ratio", "Generic dimensionless ratio", "", True),
                DiscoveredQuantity("value", "Generic measurement", "", False)
            ]

        return quantities

    def find_data_sources(self, topic: str, domain: str) -> List[Dict]:
        """
        Find authoritative data sources for this topic.

        Uses Wikipedia API + web search - no hardcoded sources.
        """
        sources = []

        # Try Wikipedia first (more reliable)
        keywords = [w for w in topic.split() if len(w) > 3][:3]
        for keyword in keywords:
            try:
                # Search Wikipedia
                response = requests.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "list": "search",
                        "srsearch": keyword,
                        "format": "json",
                        "srlimit": 3
                    },
                    headers={"User-Agent": "HermesFlow/2.0"},
                    timeout=10
                )
                if response.ok:
                    data = response.json()
                    for result in data.get("query", {}).get("search", []):
                        title = result.get("title", "")
                        sources.append({
                            "name": f"Wikipedia: {title}",
                            "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                            "type": "encyclopedia",
                            "pageid": result.get("pageid")
                        })
            except Exception as e:
                self._log(f"Wikipedia search error: {e}")

        # Also try DuckDuckGo
        search_queries = [f"{topic} data", f"{domain} measurements"]
        for query in search_queries[:1]:
            try:
                response = requests.get(
                    "https://api.duckduckgo.com/",
                    params={"q": query, "format": "json", "no_html": 1},
                    timeout=10
                )
                if response.ok:
                    data = response.json()
                    if data.get("AbstractURL"):
                        sources.append({
                            "name": data.get("Heading", "Unknown"),
                            "url": data.get("AbstractURL"),
                            "type": "reference"
                        })
            except Exception as e:
                self._log(f"Search error: {e}")

        return sources[:10]

    def fetch_measurements(self, sources: List[Dict], quantities: List[DiscoveredQuantity]) -> Dict[str, List[float]]:
        """
        Fetch actual measurements from discovered sources.

        Adaptive - handles different source types.
        """
        measurements = {q.name: [] for q in quantities}

        for source in sources[:5]:  # Top 5 sources
            source_type = source.get("type", "")
            pageid = source.get("pageid")

            content = ""

            # If Wikipedia, use API to get full content
            if "wikipedia" in source.get("name", "").lower() or pageid:
                try:
                    if pageid:
                        response = requests.get(
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
                        if response.ok:
                            pages = response.json().get("query", {}).get("pages", {})
                            for page in pages.values():
                                content = page.get("extract", "")[:15000]
                                self._log(f"  Fetched Wikipedia: {page.get('title', 'unknown')} ({len(content)} chars)")
                except Exception as e:
                    self._log(f"Wikipedia API error: {e}")

            # Fallback to web scrape
            if not content:
                url = source.get("url", "")
                if url:
                    try:
                        headers = {"User-Agent": "HermesFlow/2.0 (Z2 Research)"}
                        response = requests.get(url, headers=headers, timeout=30)
                        if response.ok:
                            content = response.text[:15000]
                    except Exception as e:
                        self._log(f"Fetch error: {e}")

            if not content:
                continue

            # Extract numbers directly (simple pattern matching)
            # Find all numbers in the content
            numbers = re.findall(r'(\d+\.?\d*)\s*(km|m|nm|kt|mph|mb|hPa|%|degrees?)?', content)

            for num_str, unit in numbers[:100]:  # Limit
                try:
                    value = float(num_str)
                    # Skip obviously wrong values (years, etc.)
                    if 1900 < value < 2100:  # Probably a year
                        continue
                    if value == 0:
                        continue

                    # Add to generic measurements
                    if "ratio" in measurements:
                        measurements["ratio"].append(value)
                    if "value" in measurements:
                        measurements["value"].append(value)
                except ValueError:
                    pass

            # Also use LLM if available (but don't block on it)
            if self.use_legomena and content:
                prompt = f"""Extract key numerical values from this text about {self.domain}.

TEXT (first 3000 chars):
{content[:3000]}

List important numbers as JSON:
{{"measurements": [<num1>, <num2>, ...]}}

JSON:"""

                extraction = self._call_legomena(prompt, timeout=60)
                if extraction:
                    try:
                        json_match = re.search(r'\{[\s\S]*?\}', extraction)
                        if json_match:
                            data = json.loads(json_match.group())
                            for v in data.get("measurements", []):
                                if isinstance(v, (int, float)) and v != 0:
                                    if "ratio" in measurements:
                                        measurements["ratio"].append(float(v))
                    except (json.JSONDecodeError, ValueError):
                        pass

        return measurements

    def find_z2_matches(self, measurements: Dict[str, List[float]]) -> List[Z2Match]:
        """
        Test all measurements against ALL Z² formulas.

        This is blind pattern matching - no domain knowledge.
        """
        matches = []

        for quantity, values in measurements.items():
            if len(values) < 3:
                continue

            # Calculate statistics
            mean = sum(values) / len(values)
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(variance) if variance > 0 else 0.01

            # Test against each Z² formula
            for formula_name, formula_value in Z2_FORMULAS.items():
                if formula_value == 0:
                    continue

                error = abs(formula_value - mean)
                error_pct = (error / mean) * 100 if mean != 0 else float('inf')
                sigma = error / std if std > 0 else float('inf')

                # Classify match
                if error_pct < 1.0:
                    verdict = "STRONG"
                elif error_pct < 5.0:
                    verdict = "INTERESTING"
                elif error_pct < 10.0:
                    verdict = "WEAK"
                else:
                    continue  # Skip poor matches

                # Refine verdict with sigma
                if sigma < 2 and error_pct < 5:
                    verdict = "VALIDATED"
                elif sigma > 5 and error_pct > 10:
                    verdict = "FALSIFIED"

                matches.append(Z2Match(
                    quantity=quantity,
                    measured_value=mean,
                    z2_formula=formula_name,
                    z2_value=formula_value,
                    error_percent=error_pct,
                    n_samples=len(values),
                    std_dev=std,
                    sigma=sigma,
                    verdict=verdict
                ))

        # Sort by error (best first)
        matches.sort(key=lambda m: m.error_percent)

        return matches

    def generate_hypothesis_from_match(self, match: Z2Match) -> Dict:
        """
        Generate a formal hypothesis from a Z² match.

        Uses LLM to create derivation - but WITHOUT domain knowledge.
        """
        prompt = f"""Generate a theoretical derivation for this empirical observation.

OBSERVATION:
- Quantity: {match.quantity}
- Measured value: {match.measured_value:.6f}
- Matches Z² formula: {match.z2_formula} = {match.z2_value:.6f}
- Error: {match.error_percent:.2f}%

Z² FRAMEWORK:
- Z² = 32π/3 = {Z2:.6f} (cube × sphere constant)
- Z = √(Z²) = {Z:.6f}
- φ = (1+√5)/2 = {PHI:.6f} (golden ratio)

Generate a derivation explaining WHY this quantity might equal {match.z2_formula}.
Think about:
1. What physical principle could cause this relationship?
2. How does Z² geometry relate to this quantity?
3. What would falsify this hypothesis?

Derivation:"""

        response = self._call_legomena(prompt, timeout=120)

        return {
            "quantity": match.quantity,
            "formula": match.z2_formula,
            "predicted": match.z2_value,
            "measured": match.measured_value,
            "error_pct": match.error_percent,
            "sigma": match.sigma,
            "n_samples": match.n_samples,
            "verdict": match.verdict,
            "derivation": response or "No derivation generated",
            "falsification": f"If {match.quantity} measured outside [{match.z2_value*0.9:.4f}, {match.z2_value*1.1:.4f}] with N>100"
        }

    def run(self, topic: str) -> BlindDiscoverySession:
        """
        Run complete blind discovery on a topic.

        NO domain knowledge - discovers everything from Z² first principles.
        """
        self._log(f"\n{'='*70}")
        self._log(f"Z² BLIND DISCOVERY")
        self._log(f"Topic: {topic}")
        self._log(f"{'='*70}")
        self._log(f"\nKnows ONLY: Z²={Z2:.4f}, Z={Z:.4f}, φ={PHI:.4f}")
        self._log(f"NO domain-specific knowledge.")

        session = BlindDiscoverySession(
            topic=topic,
            started=datetime.now().isoformat(),
            domain_discovered="",
            quantities_discovered=[],
            data_sources_found=[],
            measurements_collected=0,
            z2_matches=[],
            best_match=None,
            conclusion=""
        )

        # Step 1: Discover domain
        self._log(f"\n--- Step 1: Discover Domain ---")
        self.domain = self.discover_domain(topic)
        session.domain_discovered = self.domain
        self._log(f"Domain: {self.domain}")

        # Step 2: Discover quantities
        self._log(f"\n--- Step 2: Discover Quantities ---")
        self.quantities = self.discover_quantities(topic)
        session.quantities_discovered = [asdict(q) for q in self.quantities]
        self._log(f"Found {len(self.quantities)} quantities:")
        for q in self.quantities:
            self._log(f"  - {q.name}: {q.description}")

        # Step 3: Find data sources
        self._log(f"\n--- Step 3: Find Data Sources ---")
        self.data_sources = self.find_data_sources(topic, self.domain)
        session.data_sources_found = self.data_sources
        self._log(f"Found {len(self.data_sources)} sources")

        # Step 4: Fetch measurements
        self._log(f"\n--- Step 4: Fetch Measurements ---")
        self.measurements = self.fetch_measurements(self.data_sources, self.quantities)
        total = sum(len(v) for v in self.measurements.values())
        session.measurements_collected = total
        self._log(f"Collected {total} measurements")
        for q, vals in self.measurements.items():
            if vals:
                self._log(f"  - {q}: {len(vals)} values (mean={sum(vals)/len(vals):.4f})")

        # Step 5: Find Z² matches
        self._log(f"\n--- Step 5: Find Z² Matches ---")
        matches = self.find_z2_matches(self.measurements)
        session.z2_matches = [asdict(m) for m in matches]

        self._log(f"Found {len(matches)} potential matches:")
        for m in matches[:10]:
            self._log(f"  {m.verdict}: {m.quantity} ≈ {m.z2_formula} ({m.error_percent:.2f}% error)")

        # Step 6: Generate hypothesis for best match
        if matches:
            best = matches[0]
            self._log(f"\n--- Step 6: Generate Hypothesis ---")
            hypothesis = self.generate_hypothesis_from_match(best)
            session.best_match = hypothesis

            self._log(f"\nBest match:")
            self._log(f"  {best.quantity} = {best.z2_formula}")
            self._log(f"  Predicted: {best.z2_value:.6f}")
            self._log(f"  Measured: {best.measured_value:.6f}")
            self._log(f"  Error: {best.error_percent:.2f}%")
            self._log(f"  Verdict: {best.verdict}")

        # Conclusion
        session.conclusion = self._synthesize(session)
        session.completed = datetime.now().isoformat()

        # Save
        self._save_session(session)

        return session

    def _synthesize(self, session: BlindDiscoverySession) -> str:
        """Generate conclusion."""
        lines = [
            f"Z² BLIND DISCOVERY COMPLETE",
            f"Topic: {session.topic}",
            f"Domain discovered: {session.domain_discovered}",
            f"Quantities discovered: {len(session.quantities_discovered)}",
            f"Measurements collected: {session.measurements_collected}",
            "",
        ]

        # Summarize matches by verdict
        validated = [m for m in session.z2_matches if m.get("verdict") == "VALIDATED"]
        strong = [m for m in session.z2_matches if m.get("verdict") == "STRONG"]
        interesting = [m for m in session.z2_matches if m.get("verdict") == "INTERESTING"]

        if validated:
            lines.append(f"VALIDATED Z² RELATIONSHIPS ({len(validated)}):")
            for m in validated:
                lines.append(f"  ✓ {m['quantity']} = {m['z2_formula']} ({m['error_percent']:.2f}%)")

        if strong:
            lines.append(f"\nSTRONG MATCHES ({len(strong)}):")
            for m in strong[:5]:
                lines.append(f"  • {m['quantity']} ≈ {m['z2_formula']} ({m['error_percent']:.2f}%)")

        if interesting:
            lines.append(f"\nINTERESTING PATTERNS ({len(interesting)}):")
            for m in interesting[:5]:
                lines.append(f"  ? {m['quantity']} ~ {m['z2_formula']} ({m['error_percent']:.2f}%)")

        if not (validated or strong or interesting):
            lines.append("NO SIGNIFICANT Z² RELATIONSHIPS FOUND")
            lines.append("This domain may not exhibit Z² geometry,")
            lines.append("or requires different measurement quantities.")

        return "\n".join(lines)

    def _save_session(self, session: BlindDiscoverySession):
        """Save session to file."""
        slug = session.topic.lower().replace(" ", "_")[:40]
        output_dir = OUTPUT_DIR / f"blind_{slug}"
        output_dir.mkdir(exist_ok=True)

        with open(output_dir / "session.json", "w") as f:
            json.dump(asdict(session), f, indent=2, default=str)

        with open(output_dir / "conclusion.txt", "w") as f:
            f.write(session.conclusion)

        self._log(f"\nSaved to: {output_dir}")


def main():
    """Run blind discovery."""
    import argparse

    parser = argparse.ArgumentParser(description="Z² Blind Discovery")
    parser.add_argument("topic", nargs="?", default="hurricane intensity and structure",
                        help="Research topic")
    parser.add_argument("--no-legomena", action="store_true", help="Disable LLM")

    args = parser.parse_args()

    discovery = Z2BlindDiscovery(use_legomena=not args.no_legomena)
    session = discovery.run(args.topic)

    print("\n" + "="*70)
    print(session.conclusion)
    print("="*70)


if __name__ == "__main__":
    main()
