#!/usr/bin/env python3
"""
HermesFlow Runner
=================

Main entry point for autonomous Z² research.
Integrates literature collection, hypothesis generation, and pattern matching.

All output is saved to hermesflow_research_output/

Usage:
    python hermesflow_runner.py "your research question"

Author: Carl Zimmerman
Date: May 3, 2026
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import asdict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from literature_collector import LiteratureCollector, collect_literature_for_research
from hypothesis_engine import HypothesisEngine, HypothesisStatus, ResearchSession
from mcp_server import ResearchTools

# Output directory
OUTPUT_DIR = Path(__file__).parent / "hermesflow_research_output"


class HermesFlowRunner:
    """
    Complete HermesFlow research pipeline.

    Stages:
    1. Problem Analysis - Understand what we're researching
    2. Literature Collection - Gather existing data
    3. Pattern Matching - Find Z² patterns in existing data
    4. Hypothesis Generation - Create new Z²-based solutions
    5. Hypothesis Testing - Validate ideas
    6. Synthesis - Combine findings into conclusion
    """

    def __init__(self, problem: str, use_legomena: bool = True):
        self.problem = problem
        self.use_legomena = use_legomena
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = OUTPUT_DIR / self._sanitize_name(problem)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Components
        self.literature_collector = LiteratureCollector(use_legomena=use_legomena)
        self.hypothesis_engine = HypothesisEngine(use_legomena=use_legomena)
        self.research_tools = ResearchTools()

        # Results
        self.results = {
            "problem": problem,
            "session_id": self.session_id,
            "started": datetime.now().isoformat(),
            "stages": {},
            "findings": [],
            "conclusion": "",
            "status": "running"
        }

        self._log(f"HermesFlow session {self.session_id} started")
        self._log(f"Problem: {problem}")
        self._log(f"Output: {self.output_dir}")

    def _sanitize_name(self, name: str) -> str:
        """Create safe folder name from problem statement."""
        safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in name[:50])
        return safe.strip().replace(" ", "_").lower()

    def _log(self, message: str):
        """Log to console and file."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        print(log_line)

        log_file = self.output_dir / "session.log"
        with open(log_file, "a") as f:
            f.write(log_line + "\n")

    def _save_results(self):
        """Save current results to JSON."""
        results_file = self.output_dir / "results.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

    def run(self, max_hypothesis_iterations: int = 20) -> Dict:
        """
        Run the complete HermesFlow pipeline.

        Returns:
            Complete research results
        """
        try:
            # Stage 1: Literature Collection
            self._stage_literature_collection()

            # Stage 2: Pattern Matching in existing data
            self._stage_pattern_matching()

            # Stage 3: Hypothesis Generation
            self._stage_hypothesis_generation(max_iterations=max_hypothesis_iterations)

            # Stage 4: Synthesis
            self._stage_synthesis()

            self.results["status"] = "completed"
            self.results["completed"] = datetime.now().isoformat()

        except Exception as e:
            self._log(f"ERROR: {str(e)}")
            self.results["status"] = "failed"
            self.results["error"] = str(e)
            import traceback
            self.results["traceback"] = traceback.format_exc()

        self._save_results()
        return self.results

    # Domain-specific measurements when web sources don't provide data
    DOMAIN_MEASUREMENTS = {
        "pfas": [
            {"name": "cf_bond_energy_kjmol", "value": 485, "unit": "kJ/mol", "source": "Chemistry literature"},
            {"name": "cc_bond_energy_kjmol", "value": 346, "unit": "kJ/mol", "source": "Chemistry literature"},
            {"name": "pfoa_halflife_years", "value": 3.8, "unit": "years", "source": "EPA"},
            {"name": "pfos_halflife_years", "value": 5.4, "unit": "years", "source": "EPA"},
            {"name": "epa_limit_ppt", "value": 4, "unit": "ppt", "source": "EPA 2024"},
            {"name": "gac_removal_efficiency", "value": 90, "unit": "%", "source": "Treatment studies"},
            {"name": "ion_exchange_removal", "value": 95, "unit": "%", "source": "Treatment studies"},
            {"name": "reverse_osmosis_removal", "value": 99, "unit": "%", "source": "Treatment studies"},
            {"name": "incineration_temp_c", "value": 1100, "unit": "C", "source": "Destruction standards"},
            {"name": "pfoa_molecular_weight", "value": 414.07, "unit": "g/mol", "source": "PubChem"},
            {"name": "pfos_molecular_weight", "value": 500.13, "unit": "g/mol", "source": "PubChem"},
            {"name": "water_surface_tension", "value": 72.8, "unit": "mN/m", "source": "Physics constants"},
            {"name": "pfas_surface_tension", "value": 33, "unit": "mN/m", "source": "PFAS properties"},
        ],
        "coastline": [
            {"name": "avg_erosion_rate_myr", "value": 0.3, "unit": "m/year", "source": "USGS"},
            {"name": "sea_level_rise_mmyr", "value": 3.4, "unit": "mm/year", "source": "NASA"},
            {"name": "wave_energy_kwm", "value": 30, "unit": "kW/m", "source": "Ocean studies"},
            {"name": "storm_surge_m", "value": 3.5, "unit": "m", "source": "NOAA"},
            {"name": "beach_slope_degrees", "value": 5.7, "unit": "degrees", "source": "Geomorphology"},
            {"name": "sediment_transport_m3m", "value": 100, "unit": "m3/m", "source": "Coastal studies"},
            {"name": "tidal_range_m", "value": 2.1, "unit": "m", "source": "NOAA"},
            {"name": "bruun_rule_factor", "value": 50, "unit": "ratio", "source": "Bruun 1962"},
        ],
        "wastewater": [
            {"name": "bod_typical_mgL", "value": 200, "unit": "mg/L", "source": "EPA"},
            {"name": "tss_typical_mgL", "value": 220, "unit": "mg/L", "source": "EPA"},
            {"name": "retention_time_hours", "value": 8, "unit": "hours", "source": "Design standards"},
            {"name": "sludge_age_days", "value": 10, "unit": "days", "source": "Design standards"},
        ]
    }

    def _get_domain_measurements(self) -> List[Dict]:
        """Get domain-specific measurements based on problem keywords."""
        measurements = []
        problem_lower = self.problem.lower()

        for domain, domain_measurements in self.DOMAIN_MEASUREMENTS.items():
            if domain in problem_lower:
                measurements.extend(domain_measurements)

        return measurements

    def _stage_literature_collection(self):
        """Stage 1: Collect literature and extract measurements."""
        self._log("\n" + "="*70)
        self._log("STAGE 1: LITERATURE COLLECTION")
        self._log("="*70)

        stage_results = {
            "started": datetime.now().isoformat(),
            "sources": [],
            "measurements": [],
            "wikipedia": None,
            "arxiv_papers": []
        }

        try:
            # Collect from all sources
            self._log("Searching Wikipedia and arXiv...")
            lit_data = collect_literature_for_research(self.problem)

            # Process sources
            sources = lit_data.get("sources", [])
            stage_results["sources"] = [
                {"name": s.name if hasattr(s, 'name') else str(s),
                 "url": s.url if hasattr(s, 'url') else ""}
                for s in sources[:10]
            ]
            self._log(f"Found {len(sources)} potential sources")

            # Process Wikipedia
            wiki = lit_data.get("wikipedia")
            if wiki:
                stage_results["wikipedia"] = {
                    "title": wiki.get("title"),
                    "extract_length": len(wiki.get("extract", "")),
                    "measurements": len(wiki.get("measurements", []))
                }
                self._log(f"Wikipedia: {wiki.get('title')} ({len(wiki.get('extract', ''))} chars)")

            # Process arXiv
            arxiv = lit_data.get("arxiv_papers", [])
            stage_results["arxiv_papers"] = [
                {"title": p.get("title", "")[:100], "measurements": len(p.get("measurements", []))}
                for p in arxiv[:5]
            ]
            self._log(f"arXiv papers: {len(arxiv)}")

            # Extract measurements
            measurements = lit_data.get("measurements", [])

            # If no measurements from web, use domain-specific knowledge
            if not measurements:
                self._log("No measurements from web sources, using domain knowledge...")
                domain_measurements = self._get_domain_measurements()
                measurements = domain_measurements
                self._log(f"Added {len(domain_measurements)} domain measurements")

            stage_results["measurements"] = [
                m if isinstance(m, dict) else asdict(m) if hasattr(m, '__dict__') else {"value": m}
                for m in measurements[:50]
            ]
            self._log(f"Total measurements: {len(measurements)}")

            for m in measurements[:10]:
                if isinstance(m, dict):
                    self._log(f"  - {m.get('name', '?')}: {m.get('value', '?')} {m.get('unit', '')}")

        except Exception as e:
            self._log(f"Literature collection error: {e}")
            stage_results["error"] = str(e)

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["literature_collection"] = stage_results
        self._save_results()

    def _stage_pattern_matching(self):
        """Stage 2: Search for Z² patterns in collected measurements."""
        self._log("\n" + "="*70)
        self._log("STAGE 2: Z² PATTERN MATCHING")
        self._log("="*70)

        stage_results = {
            "started": datetime.now().isoformat(),
            "measurements_tested": 0,
            "matches": [],
            "validated": [],
            "inconclusive": []
        }

        try:
            # Get measurements from literature stage
            lit_stage = self.results["stages"].get("literature_collection", {})
            measurements = lit_stage.get("measurements", [])

            if not measurements:
                self._log("No measurements to analyze - skipping pattern matching")
                stage_results["note"] = "No measurements available"
            else:
                self._log(f"Testing {len(measurements)} measurements for Z² patterns...")

                for m in measurements:
                    if not isinstance(m, dict):
                        continue

                    value = m.get("value")
                    name = m.get("name", "unknown")

                    if value is None or not isinstance(value, (int, float)):
                        continue

                    try:
                        result = self.research_tools.research_any(
                            domain=self._sanitize_name(self.problem),
                            target=name,
                            measured_value=float(value)
                        )

                        stage_results["measurements_tested"] += 1

                        match_data = {
                            "name": name,
                            "value": value,
                            "formula": result.get("best_formula"),
                            "error_pct": result.get("percent_error"),
                            "verdict": result.get("verdict")
                        }
                        stage_results["matches"].append(match_data)

                        if result.get("verdict") == "VALIDATED":
                            stage_results["validated"].append(match_data)
                            self._log(f"  VALIDATED: {name} = {value} -> {result.get('best_formula')} ({result.get('percent_error'):.3f}%)")
                        elif result.get("verdict") == "INCONCLUSIVE":
                            stage_results["inconclusive"].append(match_data)
                            self._log(f"  ? {name} = {value} -> {result.get('best_formula')} ({result.get('percent_error'):.2f}%)")

                    except Exception as e:
                        self._log(f"  Error testing {name}: {e}")

                self._log(f"\nPattern matching complete:")
                self._log(f"  Tested: {stage_results['measurements_tested']}")
                self._log(f"  Validated: {len(stage_results['validated'])}")
                self._log(f"  Inconclusive: {len(stage_results['inconclusive'])}")

        except Exception as e:
            self._log(f"Pattern matching error: {e}")
            stage_results["error"] = str(e)

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["pattern_matching"] = stage_results
        self._save_results()

    def _stage_hypothesis_generation(self, max_iterations: int = 20):
        """Stage 3: Generate and test Z²-based hypotheses."""
        self._log("\n" + "="*70)
        self._log("STAGE 3: HYPOTHESIS GENERATION & TESTING")
        self._log("="*70)

        stage_results = {
            "started": datetime.now().isoformat(),
            "hypotheses_generated": 0,
            "hypotheses_tested": 0,
            "validated": [],
            "inconclusive": [],
            "refuted": [],
            "best_hypothesis": None
        }

        try:
            self._log(f"Generating Z²-based hypotheses for: {self.problem}")
            self._log(f"Max iterations: {max_iterations}")

            # Run the hypothesis engine
            session = self.hypothesis_engine.research_until_exhausted(
                self.problem,
                max_iterations=max_iterations
            )

            stage_results["hypotheses_generated"] = len(session.hypotheses_generated)
            stage_results["hypotheses_tested"] = session.hypotheses_tested

            # Categorize hypotheses
            for h in session.hypotheses_generated:
                h_data = {
                    "id": h.id,
                    "statement": h.statement,
                    "principle": h.z2_principle,
                    "mechanism": h.mechanism,
                    "prediction": h.testable_prediction,
                    "confidence": h.confidence,
                    "status": h.status.value if hasattr(h.status, 'value') else str(h.status)
                }

                if h.status == HypothesisStatus.VALIDATED:
                    stage_results["validated"].append(h_data)
                elif h.status == HypothesisStatus.INCONCLUSIVE:
                    stage_results["inconclusive"].append(h_data)
                else:
                    stage_results["refuted"].append(h_data)

            # Best hypothesis
            if session.best_hypothesis:
                stage_results["best_hypothesis"] = {
                    "statement": session.best_hypothesis.statement,
                    "confidence": session.best_hypothesis.confidence,
                    "principle": session.best_hypothesis.z2_principle,
                    "mechanism": session.best_hypothesis.mechanism,
                    "prediction": session.best_hypothesis.testable_prediction
                }

            stage_results["conclusion"] = session.conclusion

            self._log(f"\nHypothesis generation complete:")
            self._log(f"  Generated: {stage_results['hypotheses_generated']}")
            self._log(f"  Tested: {stage_results['hypotheses_tested']}")
            self._log(f"  Validated: {len(stage_results['validated'])}")
            self._log(f"  Inconclusive: {len(stage_results['inconclusive'])}")
            self._log(f"  Refuted: {len(stage_results['refuted'])}")

            if stage_results["best_hypothesis"]:
                self._log(f"\nBest hypothesis (confidence {stage_results['best_hypothesis']['confidence']:.2f}):")
                self._log(f"  {stage_results['best_hypothesis']['statement'][:200]}")

        except Exception as e:
            self._log(f"Hypothesis generation error: {e}")
            stage_results["error"] = str(e)
            import traceback
            self._log(traceback.format_exc())

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["hypothesis_generation"] = stage_results
        self._save_results()

    def _stage_synthesis(self):
        """Stage 4: Synthesize all findings into conclusion."""
        self._log("\n" + "="*70)
        self._log("STAGE 4: SYNTHESIS")
        self._log("="*70)

        # Gather all findings
        findings = []

        # From pattern matching
        pm_stage = self.results["stages"].get("pattern_matching", {})
        if pm_stage.get("validated"):
            for v in pm_stage["validated"]:
                findings.append({
                    "type": "pattern_match",
                    "finding": f"{v['name']} matches {v['formula']} ({v['error_pct']:.3f}% error)",
                    "confidence": 1 - (v['error_pct'] / 100)
                })

        # From hypothesis generation
        hg_stage = self.results["stages"].get("hypothesis_generation", {})
        if hg_stage.get("validated"):
            for h in hg_stage["validated"]:
                findings.append({
                    "type": "hypothesis",
                    "finding": h["statement"],
                    "confidence": h["confidence"]
                })

        if hg_stage.get("inconclusive"):
            for h in hg_stage["inconclusive"][:3]:  # Top 3 inconclusive
                findings.append({
                    "type": "hypothesis_inconclusive",
                    "finding": h["statement"],
                    "confidence": h["confidence"]
                })

        self.results["findings"] = findings

        # Generate conclusion
        if findings:
            validated = [f for f in findings if f["confidence"] >= 0.7]
            promising = [f for f in findings if 0.4 <= f["confidence"] < 0.7]

            conclusion_parts = [
                f"HermesFlow Research Complete: {self.problem}",
                f"",
                f"VALIDATED FINDINGS ({len(validated)}):"
            ]
            for f in validated:
                conclusion_parts.append(f"  - {f['finding'][:150]}")

            if promising:
                conclusion_parts.append(f"\nPROMISING LEADS ({len(promising)}):")
                for f in promising:
                    conclusion_parts.append(f"  - {f['finding'][:150]} (confidence: {f['confidence']:.2f})")

            if not validated and not promising:
                conclusion_parts.append("  No strong Z² patterns or hypotheses found")
                conclusion_parts.append("  This may indicate Z² geometry does not apply to this domain")

            self.results["conclusion"] = "\n".join(conclusion_parts)
        else:
            self.results["conclusion"] = "No findings generated. Check logs for errors."

        self._log(self.results["conclusion"])
        self._save_results()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python hermesflow_runner.py \"your research question\"")
        print("\nExamples:")
        print("  python hermesflow_runner.py \"remove PFAS from wastewater\"")
        print("  python hermesflow_runner.py \"predict coastline erosion rates\"")
        sys.exit(1)

    problem = " ".join(sys.argv[1:])

    print("="*70)
    print("HERMESFLOW AUTONOMOUS RESEARCH")
    print("="*70)
    print(f"Problem: {problem}")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*70)

    runner = HermesFlowRunner(problem, use_legomena=True)
    results = runner.run(max_hypothesis_iterations=15)

    print("\n" + "="*70)
    print("RESEARCH COMPLETE")
    print("="*70)
    print(f"Status: {results['status']}")
    print(f"Output: {runner.output_dir}")
    print("\nConclusion:")
    print(results.get("conclusion", "See results.json"))


if __name__ == "__main__":
    main()
