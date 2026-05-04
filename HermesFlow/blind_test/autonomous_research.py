#!/usr/bin/env python3
"""
AUTONOMOUS RESEARCH FRAMEWORK
==============================

A dynamic, domain-agnostic research system that can:
1. Research ANY scientific domain
2. Discover and fetch relevant data sources
3. Generate and execute computational tests
4. Use HRM for honest assessment
5. Iterate until truth found or stuck

This is the core engine for blind scientific discovery.

Author: Carl Zimmerman
Date: May 3, 2026
"""

import json
import subprocess
import numpy as np
import requests
import tempfile
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# Z² Constants (the fundamental framework)
Z2 = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2)       # ≈ 5.79
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio ≈ 1.618

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "research_results"
RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class DataSource:
    """Represents a data source for research."""
    name: str
    domain: str
    url: str
    data_type: str  # 'api', 'file', 'database'
    parser: Optional[str] = None
    credentials_required: bool = False


@dataclass
class Hypothesis:
    """A testable hypothesis."""
    statement: str
    formula: str
    predicted_value: Optional[float] = None
    domain: str = ""
    status: str = "UNTESTED"


@dataclass
class Finding:
    """A research finding."""
    hypothesis: str
    predicted: float
    measured: float
    error_percent: float
    sample_size: int
    p_value: Optional[float] = None
    classification: str = "UNTESTED"
    mechanism: Optional[str] = None


# ============================================================================
# LOCAL LLM INTERFACE
# ============================================================================

class LLMInterface:
    """Interface to local Legomena models."""

    @staticmethod
    def query(prompt: str, model: str = "legomena-31b", timeout: int = 180) -> str:
        """Query local Legomena model."""
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "ERROR: Query timed out"
        except Exception as e:
            return f"ERROR: {e}"

    @staticmethod
    def extract_json(text: str) -> Optional[Dict]:
        """Extract JSON from response."""
        for start_char, end_char in [('{', '}'), ('[', ']')]:
            try:
                start = text.find(start_char)
                end = text.rfind(end_char) + 1
                if start >= 0 and end > start:
                    result = json.loads(text[start:end])
                    if isinstance(result, list):
                        return {"array": result}
                    return result
            except:
                continue
        return None


# ============================================================================
# DATA SOURCE REGISTRY
# ============================================================================

class DataSourceRegistry:
    """Registry of known data sources by domain."""

    SOURCES = {
        "meteorology": [
            DataSource("NOAA HURDAT2", "meteorology",
                      "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2023-051124.txt",
                      "file", "hurdat2"),
            DataSource("NOAA Storm Events", "meteorology",
                      "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/",
                      "api", "csv"),
        ],
        "particle_physics": [
            DataSource("PDG Live", "particle_physics",
                      "https://pdglive.lbl.gov/",
                      "api", "json"),
        ],
        "cosmology": [
            DataSource("Planck Data", "cosmology",
                      "https://pla.esac.esa.int/",
                      "api", "fits"),
        ],
        "neutrino": [
            DataSource("NuFIT", "neutrino",
                      "http://www.nu-fit.org/",
                      "api", "json"),
        ],
    }

    @classmethod
    def get_sources(cls, domain: str) -> List[DataSource]:
        """Get data sources for a domain."""
        return cls.SOURCES.get(domain.lower(), [])

    @classmethod
    def discover_sources(cls, topic: str) -> List[DataSource]:
        """Use LLM to discover data sources for a topic."""
        prompt = f"""What are the authoritative data sources for {topic}?

List ONLY sources with:
1. Public API or downloadable data
2. Peer-reviewed/government data
3. Specific URLs

Return JSON: {{"sources": [{{"name": "...", "url": "...", "data_type": "api/file"}}]}}"""

        response = LLMInterface.query(prompt, "legomena-e4b")
        result = LLMInterface.extract_json(response)

        if result and 'sources' in result:
            return [
                DataSource(s['name'], topic, s['url'], s.get('data_type', 'api'))
                for s in result['sources']
            ]
        return []


# ============================================================================
# DATA FETCHER
# ============================================================================

class DataFetcher:
    """Fetches and parses data from various sources."""

    @staticmethod
    def fetch(source: DataSource) -> Optional[Dict]:
        """Fetch data from a source."""
        print(f"  Fetching: {source.name}...")

        try:
            response = requests.get(source.url, timeout=60)
            response.raise_for_status()

            # Parse based on data type
            if source.parser == "hurdat2":
                return DataFetcher._parse_hurdat2(response.text)
            elif source.data_type == "json":
                return response.json()
            else:
                return {"raw": response.text[:10000]}

        except Exception as e:
            print(f"    Error: {e}")
            return None

    @staticmethod
    def _parse_hurdat2(text: str) -> Dict:
        """Parse HURDAT2 hurricane format."""
        hurricanes = []
        current_storm = None

        for line in text.split('\n'):
            if not line.strip():
                continue

            parts = line.split(',')

            if len(parts) >= 4 and parts[0].strip().startswith('AL'):
                if current_storm:
                    hurricanes.append(current_storm)
                current_storm = {
                    'id': parts[0].strip(),
                    'name': parts[1].strip(),
                    'max_wind': 0,
                    'observations': []
                }
            elif current_storm and len(parts) >= 7:
                try:
                    wind = int(parts[6].strip()) if parts[6].strip().isdigit() else 0
                    if wind > 0:
                        current_storm['observations'].append({'wind': wind})
                        current_storm['max_wind'] = max(current_storm['max_wind'], wind)
                except:
                    pass

        if current_storm:
            hurricanes.append(current_storm)

        return {
            'source': 'HURDAT2',
            'count': len(hurricanes),
            'hurricanes': hurricanes
        }


# ============================================================================
# COMPUTATION ENGINE
# ============================================================================

class ComputationEngine:
    """Generates and executes Python code for testing hypotheses."""

    @staticmethod
    def generate_code(hypothesis: str, data_schema: str, domain: str) -> str:
        """Generate Python code to test a hypothesis."""

        prompt = f"""Generate Python code to test this hypothesis:

HYPOTHESIS: {hypothesis}
DOMAIN: {domain}

DATA AVAILABLE (as 'data' variable):
{data_schema}

Z² CONSTANTS:
Z2 = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2)       # ≈ 5.79
PHI = (1 + np.sqrt(5)) / 2  # ≈ 1.618

Write a COMPLETE, self-contained Python script that:
1. Processes the data
2. Tests the hypothesis numerically
3. Computes error/deviation
4. Assesses statistical significance if possible
5. Prints a JSON result: {{"predicted": X, "measured": Y, "error_percent": Z, "sample_size": N, "p_value": P or null}}

ONLY return Python code, no explanations."""

        response = LLMInterface.query(prompt, "legomena-31b")

        # Extract code block
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            return response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            return response[start:end].strip()

        return response

    @staticmethod
    def execute(code: str, data: Dict) -> Dict:
        """Execute Python code safely."""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Inject setup
            setup = f"""
import numpy as np
import json
from scipy import stats

Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)
PHI = (1 + np.sqrt(5)) / 2

data = {json.dumps(data)}

"""
            f.write(setup + code)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", temp_path],
                capture_output=True, text=True, timeout=60
            )

            output = result.stdout + result.stderr
            json_result = LLMInterface.extract_json(output)

            return {
                'success': result.returncode == 0,
                'output': output[:2000],
                'result': json_result
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            os.unlink(temp_path)


# ============================================================================
# HRM ASSESSMENT
# ============================================================================

class HRMAssessor:
    """Hierarchical Recursive Meta-assessment for honest validation."""

    @staticmethod
    def assess(finding: Dict, domain: str, data_context: str) -> Dict:
        """Run 3-level HRM assessment."""

        # Level 1: Mathematical validity
        l1_prompt = f"""LEVEL 1: MATHEMATICAL VALIDITY

FINDING: {json.dumps(finding)}
DOMAIN: {domain}

Assess:
1. Is the calculation mathematically correct?
2. Is the sample size adequate (N > 30)?
3. Is the error < 5%?

Return JSON: {{"valid": true/false, "score": 0.0-1.0, "issues": []}}"""

        l1 = LLMInterface.extract_json(LLMInterface.query(l1_prompt)) or {'valid': False, 'score': 0.3}

        # Level 2: Physical mechanism
        l2_prompt = f"""LEVEL 2: PHYSICAL MECHANISM

FINDING: {json.dumps(finding)}
DOMAIN: {domain}
L1 SCORE: {l1.get('score', 0.5)}

Is there a PHYSICAL REASON for this pattern?
- Z² = 32π/3 comes from cube × sphere geometry
- φ appears in optimal equilibrium states
- Could these relate to {domain} physics?

Return JSON: {{"plausible": true/false, "mechanism": "explanation or null", "score": 0.0-1.0}}"""

        l2 = LLMInterface.extract_json(LLMInterface.query(l2_prompt)) or {'plausible': False, 'score': 0.2}

        # Level 3: Numerology check
        l3_prompt = f"""LEVEL 3: NUMEROLOGY CHECK

L1: {json.dumps(l1)}
L2: {json.dumps(l2)}
DOMAIN: {domain}

With infinite real numbers, finding matches by chance is common.
For this to be REAL, not numerology:
1. Error must be < 5%
2. Physical mechanism must exist
3. Sample must be adequate

Final classification:
Return JSON: {{"classification": "VALIDATED/SPECULATIVE/NUMEROLOGY", "confidence": 0.0-1.0, "reasoning": "..."}}"""

        l3 = LLMInterface.extract_json(LLMInterface.query(l3_prompt)) or {'classification': 'NUMEROLOGY', 'confidence': 0.2}

        return {
            'l1': l1,
            'l2': l2,
            'l3': l3,
            'final_score': l3.get('confidence', 0.2),
            'classification': l3.get('classification', 'NUMEROLOGY')
        }


# ============================================================================
# HYPOTHESIS GENERATOR
# ============================================================================

class HypothesisGenerator:
    """Generates testable Z² hypotheses for any domain."""

    @staticmethod
    def generate(domain: str, data_summary: str, previous: List[Dict], iteration: int) -> List[str]:
        """Generate hypotheses for a domain."""

        prev_summary = "\n".join([
            f"- {r.get('hypothesis', '')}: {r.get('classification', 'unknown')}"
            for r in previous[-5:]
        ]) if previous else "None"

        prompt = f"""Generate Z² hypotheses for {domain.upper()}.

DATA SUMMARY:
{data_summary}

Z² CONSTANTS:
- Z² = 32π/3 ≈ 33.51
- Z = √Z² ≈ 5.79
- φ (golden ratio) ≈ 1.618
- 1/φ ≈ 0.618

PREVIOUS ATTEMPTS:
{prev_summary}

Generate {3 if iteration == 1 else 2} NEW hypotheses that:
1. Are testable with available data
2. Could connect Z² or φ to {domain} physics
3. Haven't been tried before

Return JSON: {{"hypotheses": ["hypothesis 1", "hypothesis 2", ...]}}"""

        response = LLMInterface.query(prompt, "legomena-e4b")
        result = LLMInterface.extract_json(response)

        return result.get('hypotheses', [])[:3] if result else []


# ============================================================================
# MAIN RESEARCH LOOP
# ============================================================================

class AutonomousResearcher:
    """Main research orchestrator."""

    def __init__(self, domain: str, max_iterations: int = 5):
        self.domain = domain
        self.max_iterations = max_iterations
        self.results: List[Dict] = []
        self.validated: List[Dict] = []
        self.data: Optional[Dict] = None

    def fetch_data(self) -> bool:
        """Fetch data for the domain."""
        print(f"\n[PHASE 1] Fetching {self.domain} data...")

        sources = DataSourceRegistry.get_sources(self.domain)

        if not sources:
            print("  No known sources, discovering...")
            sources = DataSourceRegistry.discover_sources(self.domain)

        for source in sources:
            data = DataFetcher.fetch(source)
            if data:
                self.data = data
                print(f"  ✓ Got data from {source.name}")
                return True

        print("  ✗ Could not fetch data")
        return False

    def get_data_summary(self) -> str:
        """Generate summary of available data."""
        if not self.data:
            return "No data"

        # Let LLM summarize the data structure
        prompt = f"""Summarize this data structure briefly:
{json.dumps(self.data)[:2000]}

Return: key fields, counts, ranges. Max 5 lines."""

        return LLMInterface.query(prompt, "legomena-e4b")[:500]

    def run(self) -> Dict:
        """Run the full research loop."""
        print("=" * 70)
        print(f"AUTONOMOUS RESEARCH: {self.domain.upper()}")
        print("=" * 70)

        # Phase 1: Get data
        if not self.fetch_data():
            return {'status': 'ERROR', 'reason': 'Could not fetch data'}

        data_summary = self.get_data_summary()
        print(f"\nData Summary:\n{data_summary}")

        # Phase 2: Iterative discovery
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n{'='*70}")
            print(f"ITERATION {iteration}/{self.max_iterations}")
            print("=" * 70)

            # Generate hypotheses
            hypotheses = HypothesisGenerator.generate(
                self.domain, data_summary, self.results, iteration
            )

            if not hypotheses:
                print("  No new hypotheses")
                break

            for hypothesis in hypotheses:
                print(f"\n  Testing: {hypothesis[:60]}...")

                # Generate and execute code
                code = ComputationEngine.generate_code(
                    hypothesis,
                    json.dumps(list(self.data.keys()) if self.data else {}),
                    self.domain
                )
                execution = ComputationEngine.execute(code, self.data)

                if execution.get('success') and execution.get('result'):
                    finding = execution['result']
                    print(f"    ✓ Computed: {json.dumps(finding)[:80]}")

                    # HRM assessment
                    hrm = HRMAssessor.assess(finding, self.domain, data_summary)

                    result = {
                        'hypothesis': hypothesis,
                        'finding': finding,
                        'hrm': hrm,
                        'classification': hrm['classification']
                    }
                    self.results.append(result)

                    print(f"    Classification: {hrm['classification']}")

                    if hrm['classification'] == 'VALIDATED':
                        self.validated.append(result)
                        print("    *** VALIDATED ***")
                else:
                    print(f"    ✗ Failed: {execution.get('error', 'unknown')[:50]}")
                    self.results.append({
                        'hypothesis': hypothesis,
                        'status': 'FAILED',
                        'error': execution.get('error', '')[:200]
                    })

            if len(self.validated) >= 2:
                print(f"\n  Found {len(self.validated)} validated - stopping")
                break

        # Phase 3: Results
        return self._compile_results()

    def _compile_results(self) -> Dict:
        """Compile final results."""
        print("\n" + "=" * 70)
        print("RESEARCH RESULTS")
        print("=" * 70)

        print(f"Hypotheses tested: {len(self.results)}")
        print(f"Validated: {len(self.validated)}")

        if self.validated:
            print("\n*** VALIDATED FINDINGS ***")
            for v in self.validated:
                print(f"  - {v['hypothesis']}")

        output = {
            'domain': self.domain,
            'timestamp': datetime.now().isoformat(),
            'hypotheses_tested': len(self.results),
            'validated_count': len(self.validated),
            'results': self.results,
            'validated': self.validated
        }

        # Save
        output_file = RESULTS_DIR / f"{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2, default=str)

        print(f"\nSaved: {output_file}")
        return output


# ============================================================================
# CLI
# ============================================================================

def research(domain: str, max_iterations: int = 5) -> Dict:
    """Run autonomous research on a domain."""
    researcher = AutonomousResearcher(domain, max_iterations)
    return researcher.run()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "meteorology"  # Default to hurricane blind test

    result = research(domain)
    print(f"\nFinal: {result.get('validated_count', 0)} validated findings")
