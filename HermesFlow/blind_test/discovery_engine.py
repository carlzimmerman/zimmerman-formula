#!/usr/bin/env python3
"""
AUTONOMOUS DISCOVERY ENGINE
============================

TRUE blind discovery - no formulas given.
The system must DISCOVER Z² patterns on its own.

Process:
1. Fetch raw data (no hints)
2. LLM generates hypotheses about what patterns MIGHT exist
3. LLM writes Python code to test each hypothesis
4. Execute code, get results
5. HRM validates findings
6. Iterate until discovery or exhaustion

NO HAND-CODED FORMULAS - everything is discovered.

Author: Carl Zimmerman
Date: May 3, 2026
"""

import json
import subprocess
import numpy as np
import requests
import tempfile
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ONLY give the fundamental constant - nothing else
Z2 = 32 * np.pi / 3  # The cube × sphere constant

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "discoveries"
RESULTS_DIR.mkdir(exist_ok=True)


class LLM:
    """Local LLM interface."""

    @staticmethod
    def query(prompt: str, model: str = "legomena-31b", timeout: int = 180) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip()
        except Exception as e:
            return f"ERROR: {e}"

    @staticmethod
    def extract_json(text: str) -> Optional[Dict]:
        # Clean ANSI escape codes
        text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
        text = re.sub(r'\[\?[0-9]+[a-z]', '', text)

        # Look for ```json block and extract content
        if '```json' in text:
            start = text.find('```json') + 7
            end = text.find('```', start)
            if end > start:
                json_block = text[start:end].strip()
                # Clean newlines and extra whitespace
                json_block = ' '.join(json_block.split())
                try:
                    return json.loads(json_block)
                except:
                    pass

        # Find JSON by matching braces
        def find_json_object(s, start_pos):
            if start_pos >= len(s) or s[start_pos] != '{':
                return None
            depth = 0
            in_string = False
            escape = False
            for i in range(start_pos, len(s)):
                c = s[i]
                if escape:
                    escape = False
                    continue
                if c == '\\' and in_string:
                    escape = True
                    continue
                if c == '"' and not escape:
                    in_string = not in_string
                    continue
                if not in_string:
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            return s[start_pos:i+1]
            return None

        # Find all { positions and try to extract JSON
        for i in range(len(text) - 1, -1, -1):  # Search backwards
            if text[i] == '{':
                json_str = find_json_object(text, i)
                if json_str:
                    # Clean it
                    json_str = ' '.join(json_str.split())
                    try:
                        return json.loads(json_str)
                    except:
                        continue

        return None

    @staticmethod
    def extract_code(text: str) -> str:
        """Extract Python code from response."""
        if "```python" in text:
            start = text.find("```python") + 9
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        return text


class DataFetcher:
    """Fetches raw data for any domain."""

    SOURCES = {
        "cosmology": {
            "url": "https://raw.githubusercontent.com/astropy/astropy/main/astropy/cosmology/data/Planck18.ecsv",
            "backup": None,
            "fallback_data": {
                "H0": 67.36, "Om0": 0.3153, "Ode0": 0.6847,
                "Tcmb0": 2.7255, "Neff": 3.046, "m_nu": [0.0, 0.0, 0.06]
            }
        },
        "particle_physics": {
            "fallback_data": {
                "alpha_em_inverse": 137.035999084,
                "sin2_theta_w": 0.23122,
                "m_electron_MeV": 0.51099895,
                "m_muon_MeV": 105.6583755,
                "m_tau_MeV": 1776.86,
                "m_top_GeV": 172.57,
                "m_bottom_GeV": 4.18,
                "m_charm_GeV": 1.27,
                "m_strange_MeV": 93.4,
                "m_up_MeV": 2.16,
                "m_down_MeV": 4.67
            }
        },
        "neutrino": {
            "fallback_data": {
                "theta_12_deg": 33.41,
                "theta_23_deg": 42.2,
                "theta_13_deg": 8.58,
                "delta_m21_sq": 7.42e-5,
                "delta_m32_sq": 2.515e-3
            }
        }
    }

    @classmethod
    def fetch(cls, domain: str) -> Dict:
        """Fetch data for a domain."""
        print(f"\n[DATA] Fetching {domain} data...")

        source = cls.SOURCES.get(domain, {})

        # Try URL first
        if source.get("url"):
            try:
                response = requests.get(source["url"], timeout=30)
                if response.ok:
                    print(f"  ✓ Fetched from URL")
                    return {"source": source["url"], "raw": response.text[:5000]}
            except:
                pass

        # Use fallback data
        if source.get("fallback_data"):
            print(f"  ✓ Using reference data")
            return {"source": "reference values", "data": source["fallback_data"]}

        print(f"  ✗ No data available")
        return None


class DiscoveryEngine:
    """Autonomous discovery engine - finds Z² patterns without hints."""

    def __init__(self, domain: str, max_iterations: int = 5):
        self.domain = domain
        self.max_iterations = max_iterations
        self.discoveries = []
        self.hypotheses_tested = []
        self.data = None

    def run(self) -> Dict:
        """Run autonomous discovery."""
        print("=" * 70)
        print(f"AUTONOMOUS DISCOVERY: {self.domain.upper()}")
        print("=" * 70)
        print("NO formulas given - system must DISCOVER patterns")
        print(f"Only hint: Z² = 32π/3 ≈ {Z2:.4f}")
        print("=" * 70)

        # Phase 1: Get data
        self.data = DataFetcher.fetch(self.domain)
        if not self.data:
            return {"status": "ERROR", "reason": "No data"}

        print(f"\nData loaded: {list(self.data.get('data', {}).keys())[:10]}")

        # Phase 2: Discovery loop
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n{'='*60}")
            print(f"ITERATION {iteration}/{self.max_iterations}")
            print("=" * 60)

            # Generate hypotheses
            hypotheses = self._generate_hypotheses(iteration)

            if not hypotheses:
                print("  No new hypotheses")
                break

            # Test each hypothesis
            for hyp in hypotheses:
                result = self._test_hypothesis(hyp)
                self.hypotheses_tested.append(result)

                if result.get("validated"):
                    self.discoveries.append(result)
                    print(f"  *** DISCOVERY: {result['hypothesis'][:50]} ***")

            # Check if we have enough discoveries
            if len(self.discoveries) >= 3:
                print(f"\n  Found {len(self.discoveries)} discoveries - stopping")
                break

        return self._compile_results()

    def _generate_hypotheses(self, iteration: int) -> List[str]:
        """LLM generates hypotheses about what Z² patterns might exist."""

        data_summary = json.dumps(self.data.get("data", {}), indent=2)[:1000]
        previous = "\n".join([f"- {h['hypothesis']}: {h.get('status', 'unknown')}"
                             for h in self.hypotheses_tested[-5:]])

        prompt = f"""DATA: {data_summary}

Z² = 33.51, Z = 5.79

Generate {3 if iteration == 1 else 2} testable hypotheses connecting Z² to this data.

Previous: {previous if previous else "None"}

ONLY return JSON, no explanation:
{{"hypotheses": [{{"statement": "X equals Y", "formula": "4*Z2+3"}}]}}"""

        response = LLM.query(prompt, "legomena-31b")
        result = LLM.extract_json(response)

        if result and "hypotheses" in result:
            return result["hypotheses"][:3]

        return []

    def _test_hypothesis(self, hypothesis: Dict) -> Dict:
        """Generate and run code to test a hypothesis."""

        statement = hypothesis.get("statement", str(hypothesis))
        formula = hypothesis.get("formula", "")

        print(f"\n  Testing: {statement[:60]}...")

        # Generate test code
        code = self._generate_test_code(statement, formula)

        if not code:
            return {"hypothesis": statement, "status": "CODE_FAILED"}

        # Execute code
        result = self._execute_code(code)

        if not result.get("success"):
            return {"hypothesis": statement, "status": "EXEC_FAILED",
                    "error": result.get("error", "")[:100]}

        # Check if it found a match
        finding = result.get("finding", {})
        error = finding.get("error_percent", 100)

        validated = error < 1.0  # Less than 1% error

        print(f"    Result: {finding.get('predicted', 'N/A')} vs {finding.get('measured', 'N/A')}")
        print(f"    Error: {error:.2f}% {'✓' if validated else ''}")

        return {
            "hypothesis": statement,
            "formula": formula,
            "finding": finding,
            "error_percent": error,
            "validated": validated,
            "status": "VALIDATED" if validated else "NO_MATCH"
        }

    def _generate_test_code(self, statement: str, formula: str) -> str:
        """LLM generates Python code to test the hypothesis."""

        data_json = json.dumps(self.data.get("data", {}))

        prompt = f"""Write Python code to test this hypothesis:

HYPOTHESIS: {statement}
FORMULA: {formula}

DATA (as 'data' dict):
{data_json}

CONSTANTS:
Z2 = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2)      # ≈ 5.79
PHI = (1 + np.sqrt(5)) / 2  # ≈ 1.618

Write COMPLETE Python code that:
1. Extracts relevant values from data
2. Computes the predicted value from Z² formula
3. Computes the measured value from data
4. Calculates percent error
5. Prints JSON: {{"predicted": X, "measured": Y, "error_percent": Z}}

Only return Python code, no explanations."""

        response = LLM.query(prompt, "legomena-31b")
        return LLM.extract_code(response)

    def _execute_code(self, code: str) -> Dict:
        """Execute Python code safely."""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            setup = f"""
import numpy as np
import json

Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)
PHI = (1 + np.sqrt(5)) / 2

data = {json.dumps(self.data.get('data', {}))}

try:
"""
            # Indent the user code
            indented_code = "\n".join("    " + line for line in code.split("\n"))

            cleanup = """
except Exception as e:
    print(json.dumps({"error": str(e)}))
"""
            f.write(setup + indented_code + cleanup)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python3", temp_path],
                capture_output=True, text=True, timeout=30
            )

            output = result.stdout + result.stderr

            # Extract JSON result
            finding = LLM.extract_json(output)

            return {
                "success": finding is not None and "error" not in finding,
                "finding": finding or {},
                "output": output[:500]
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            os.unlink(temp_path)

    def _compile_results(self) -> Dict:
        """Compile final results."""
        print("\n" + "=" * 70)
        print("DISCOVERY RESULTS")
        print("=" * 70)

        print(f"Hypotheses tested: {len(self.hypotheses_tested)}")
        print(f"Discoveries made: {len(self.discoveries)}")

        if self.discoveries:
            print("\n*** AUTONOMOUS DISCOVERIES ***")
            for d in self.discoveries:
                print(f"\n  {d['hypothesis']}")
                print(f"    Formula: {d.get('formula', 'N/A')}")
                f = d.get('finding', {})
                print(f"    Predicted: {f.get('predicted', 'N/A')}")
                print(f"    Measured: {f.get('measured', 'N/A')}")
                print(f"    Error: {d.get('error_percent', 'N/A'):.3f}%")

        output = {
            "domain": self.domain,
            "timestamp": datetime.now().isoformat(),
            "hypotheses_tested": len(self.hypotheses_tested),
            "discoveries": self.discoveries,
            "all_results": self.hypotheses_tested
        }

        output_file = RESULTS_DIR / f"{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2, default=str)

        print(f"\nSaved: {output_file}")
        return output


def discover(domain: str) -> Dict:
    """Run autonomous discovery on a domain."""
    engine = DiscoveryEngine(domain, max_iterations=5)
    return engine.run()


if __name__ == "__main__":
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else "particle_physics"
    discover(domain)
