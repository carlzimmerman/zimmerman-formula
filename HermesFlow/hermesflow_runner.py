#!/usr/bin/env python3
"""
HermesFlow Runner v2.0
======================

Main entry point for autonomous Z² research with RIGOROUS SCIENTIFIC VALIDATION.

KEY PRINCIPLES (enforced):
1. DERIVE BEFORE MEASURE - Predictions from Z² theory, not curve fitting
2. AUTHORITATIVE DATA - CODATA, PDG, Planck for validation
3. STATISTICAL RIGOR - Bonferroni correction, sigma deviations
4. DATA QUALITY FILTERING - Reject economic, geographic, algorithmic data
5. CLEAR DISTINCTION - Exploratory findings vs Scientifically Validated

Pipeline Stages:
1. Literature Collection - Gather data (exploratory)
2. Data Quality Assessment - Filter non-physical data
3. Exploratory Pattern Matching - Find potential patterns (NOT validation)
4. Hypothesis Generation - Create testable Z²-based ideas
5. RIGOROUS VALIDATION - Scientific validation against authoritative data
6. Synthesis - Combine findings with clear epistemological status

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import asdict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from literature_collector import LiteratureCollector, collect_literature_for_research
from hypothesis_engine import HypothesisEngine, HypothesisStatus, ResearchSession
from mcp_server import ResearchTools
from scientific_validator import (
    ScientificValidator,
    DataQuality,
    DerivationStatus,
    EMPIRICAL_DATA,
    Z2_PREDICTIONS,
    Z2, Z, PHI
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "hermesflow_research_output"


class DataQualityFilter:
    """
    Filter data based on scientific validity for Z² testing.

    REJECTS:
    - Economic data (human decisions, not physics)
    - Geographic/demographic data (arbitrary boundaries)
    - Algorithmic performance metrics
    - Year/date values
    - Arbitrary counts

    ACCEPTS:
    - Physical constants
    - Measured physical quantities
    - Ratios of physical quantities
    """

    # Keywords that indicate NON-PHYSICAL data
    REJECT_KEYWORDS = {
        # Economic
        "cost", "price", "market", "profit", "revenue", "budget", "billion",
        "trillion", "million", "dollar", "euro", "usd", "eur", "gbp", "sale",
        "economic", "financial", "investment", "funding",
        # Geographic/demographic
        "population", "country", "city", "region", "area_km", "distance_km",
        "proximity", "location", "geographic",
        # Temporal (years are not physics)
        "year", "date", "started", "founded", "established", "convention",
        # Algorithmic
        "accuracy", "precision", "recall", "f1_score", "performance", "error_rate",
        "model_", "algorithm", "neural", "training",
        # Arbitrary counts
        "number_of", "count_of", "total_listed", "chemicals_listed",
    }

    # Keywords that indicate POTENTIALLY PHYSICAL data
    ACCEPT_KEYWORDS = {
        # Physical quantities
        "energy", "mass", "force", "temperature", "pressure", "density",
        "velocity", "acceleration", "frequency", "wavelength", "amplitude",
        "charge", "current", "voltage", "resistance", "capacitance",
        "angle", "ratio", "coefficient", "constant", "coupling",
        # Specific physical contexts
        "bond_energy", "molecular_weight", "halflife", "threshold",
        "surface_tension", "viscosity", "conductivity",
        # Units that suggest physics
        "_kjmol", "_ev", "_mev", "_gev", "_kelvin", "_pascal",
        "_newton", "_joule", "_watt", "_hertz", "_tesla",
    }

    @classmethod
    def assess_data_quality(cls, name: str, value: float, source: str) -> Tuple[DataQuality, str]:
        """
        Assess the quality of a data point for Z² validation.

        Returns:
            (DataQuality, reason)
        """
        name_lower = name.lower()
        source_lower = source.lower()

        # Check for rejection keywords
        for keyword in cls.REJECT_KEYWORDS:
            if keyword in name_lower:
                return DataQuality.UNVERIFIED, f"Rejected: contains '{keyword}' (non-physical)"

        # Check source quality
        if any(auth in source_lower for auth in ["codata", "nist", "pdg", "planck", "nufit"]):
            return DataQuality.AUTHORITATIVE, "Authoritative source"

        if any(inst in source_lower for inst in ["noaa", "nasa", "esa", "cern", "fermilab"]):
            return DataQuality.INSTITUTIONAL, "Institutional source"

        if "arxiv" in source_lower or "journal" in source_lower or "paper" in source_lower:
            return DataQuality.PEER_REVIEWED, "Peer-reviewed source"

        if "wikipedia" in source_lower or "legomena" in source_lower:
            return DataQuality.SECONDARY, "Secondary source - exploratory only"

        # Check for acceptance keywords
        for keyword in cls.ACCEPT_KEYWORDS:
            if keyword in name_lower:
                return DataQuality.SECONDARY, f"Physical quantity ({keyword})"

        return DataQuality.UNVERIFIED, "Unknown data quality"

    @classmethod
    def is_valid_for_exploration(cls, name: str, value: float, source: str) -> bool:
        """Check if data is valid for exploratory pattern matching."""
        quality, _ = cls.assess_data_quality(name, value, source)
        return quality != DataQuality.UNVERIFIED

    @classmethod
    def is_valid_for_validation(cls, name: str, value: float, source: str) -> bool:
        """Check if data is valid for rigorous scientific validation."""
        quality, _ = cls.assess_data_quality(name, value, source)
        return quality in [DataQuality.AUTHORITATIVE, DataQuality.INSTITUTIONAL]


class HermesFlowRunner:
    """
    Complete HermesFlow research pipeline with SCIENTIFIC RIGOR.

    Stages:
    1. Literature Collection - Gather existing data (exploratory)
    2. Data Quality Assessment - Filter non-physical data
    3. Exploratory Pattern Matching - Find potential patterns (NOT validation!)
    4. Hypothesis Generation - Create testable Z²-based ideas
    5. RIGOROUS VALIDATION - Scientific validation with proper statistics
    6. Synthesis - Combine findings with clear epistemological status
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
        self.scientific_validator = ScientificValidator()
        self.data_filter = DataQualityFilter()

        # Results
        self.results = {
            "problem": problem,
            "session_id": self.session_id,
            "started": datetime.now().isoformat(),
            "methodology": {
                "description": "HermesFlow v2.0 with scientific rigor",
                "principles": [
                    "Predictions derived from Z² theory before comparison",
                    "Data filtered for physical relevance",
                    "Exploratory findings clearly distinguished from validated",
                    "Rigorous validation uses authoritative sources only",
                    "Statistical significance with Bonferroni correction"
                ]
            },
            "stages": {},
            "exploratory_findings": [],  # Pattern matches - NOT validated
            "validated_findings": [],     # Rigorous scientific validation
            "hypotheses": [],
            "conclusion": "",
            "status": "running"
        }

        self._log(f"HermesFlow v2.0 session {self.session_id} started")
        self._log(f"Problem: {problem}")
        self._log(f"Output: {self.output_dir}")
        self._log(f"Scientific rigor: ENABLED")

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
        Run the complete HermesFlow pipeline with scientific rigor.

        Returns:
            Complete research results with clear distinction between
            exploratory findings and validated findings.
        """
        try:
            # Stage 1: Literature Collection
            self._stage_literature_collection()

            # Stage 2: Data Quality Assessment
            self._stage_data_quality_assessment()

            # Stage 3: Exploratory Pattern Matching (clearly labeled)
            self._stage_exploratory_pattern_matching()

            # Stage 4: Hypothesis Generation
            self._stage_hypothesis_generation(max_iterations=max_hypothesis_iterations)

            # Stage 5: RIGOROUS VALIDATION (the real science)
            self._stage_rigorous_validation()

            # Stage 6: Synthesis
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

    # Domain-specific measurements - clearly marked with source quality
    DOMAIN_MEASUREMENTS = {
        "pfas": [
            {"name": "cf_bond_energy_kjmol", "value": 485, "unit": "kJ/mol", "source": "Chemistry literature", "physical": True},
            {"name": "cc_bond_energy_kjmol", "value": 346, "unit": "kJ/mol", "source": "Chemistry literature", "physical": True},
            {"name": "pfoa_halflife_years", "value": 3.8, "unit": "years", "source": "EPA studies", "physical": True},
            {"name": "pfos_halflife_years", "value": 5.4, "unit": "years", "source": "EPA studies", "physical": True},
            {"name": "pfoa_molecular_weight", "value": 414.07, "unit": "g/mol", "source": "PubChem", "physical": True},
            {"name": "pfos_molecular_weight", "value": 500.13, "unit": "g/mol", "source": "PubChem", "physical": True},
            {"name": "water_surface_tension", "value": 72.8, "unit": "mN/m", "source": "NIST", "physical": True},
            {"name": "pfas_surface_tension", "value": 33, "unit": "mN/m", "source": "PFAS properties", "physical": True},
        ],
        "coastline": [
            {"name": "sea_level_rise_mmyr", "value": 3.4, "unit": "mm/year", "source": "NASA", "physical": True},
            {"name": "wave_energy_kwm", "value": 30, "unit": "kW/m", "source": "Ocean studies", "physical": True},
            {"name": "storm_surge_m", "value": 3.5, "unit": "m", "source": "NOAA", "physical": True},
            {"name": "tidal_range_m", "value": 2.1, "unit": "m", "source": "NOAA", "physical": True},
            {"name": "beach_slope_degrees", "value": 5.7, "unit": "degrees", "source": "Geomorphology", "physical": True},
        ],
        "hurricane": [
            {"name": "ts_threshold_kt", "value": 34, "unit": "knots", "source": "NOAA NHC", "physical": True},
            {"name": "cat3_eye_rmw_ratio", "value": 0.6187, "unit": "ratio", "source": "NOAA flight data N=325", "physical": True},
            {"name": "cat1_threshold_kt", "value": 64, "unit": "knots", "source": "NOAA NHC", "physical": True},
        ],
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
            "measurements_raw": [],
            "wikipedia": None,
            "arxiv_papers": []
        }

        try:
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

            # Extract RAW measurements (before filtering)
            measurements = lit_data.get("measurements", [])

            # Add domain-specific measurements if web didn't provide enough
            if len(measurements) < 5:
                self._log("Adding domain-specific measurements...")
                domain_measurements = self._get_domain_measurements()
                measurements.extend(domain_measurements)

            stage_results["measurements_raw"] = [
                m if isinstance(m, dict) else asdict(m) if hasattr(m, '__dict__') else {"value": m}
                for m in measurements[:50]
            ]
            self._log(f"Raw measurements collected: {len(measurements)}")

        except Exception as e:
            self._log(f"Literature collection error: {e}")
            stage_results["error"] = str(e)

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["literature_collection"] = stage_results
        self._save_results()

    def _stage_data_quality_assessment(self):
        """Stage 2: Assess and filter data quality."""
        self._log("\n" + "="*70)
        self._log("STAGE 2: DATA QUALITY ASSESSMENT")
        self._log("="*70)

        stage_results = {
            "started": datetime.now().isoformat(),
            "total_raw": 0,
            "accepted_exploration": 0,
            "accepted_validation": 0,
            "rejected": 0,
            "filtered_measurements": [],
            "rejected_measurements": []
        }

        try:
            raw_measurements = self.results["stages"]["literature_collection"].get("measurements_raw", [])
            stage_results["total_raw"] = len(raw_measurements)

            for m in raw_measurements:
                if not isinstance(m, dict):
                    continue

                name = m.get("name", "unknown")
                value = m.get("value")
                source = m.get("source", "unknown")

                if value is None or not isinstance(value, (int, float)):
                    continue

                # Assess quality
                quality, reason = self.data_filter.assess_data_quality(name, value, source)

                m_with_quality = {
                    **m,
                    "data_quality": quality.value,
                    "quality_reason": reason
                }

                if quality == DataQuality.UNVERIFIED:
                    stage_results["rejected"] += 1
                    stage_results["rejected_measurements"].append(m_with_quality)
                    self._log(f"  REJECTED: {name} - {reason}")
                else:
                    stage_results["filtered_measurements"].append(m_with_quality)
                    if quality in [DataQuality.AUTHORITATIVE, DataQuality.INSTITUTIONAL]:
                        stage_results["accepted_validation"] += 1
                        self._log(f"  ACCEPTED (validation): {name} - {reason}")
                    else:
                        stage_results["accepted_exploration"] += 1
                        self._log(f"  ACCEPTED (exploration): {name} - {reason}")

            self._log(f"\nData quality summary:")
            self._log(f"  Total raw: {stage_results['total_raw']}")
            self._log(f"  Accepted for validation: {stage_results['accepted_validation']}")
            self._log(f"  Accepted for exploration: {stage_results['accepted_exploration']}")
            self._log(f"  Rejected (non-physical): {stage_results['rejected']}")

        except Exception as e:
            self._log(f"Data quality error: {e}")
            stage_results["error"] = str(e)

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["data_quality"] = stage_results
        self._save_results()

    def _stage_exploratory_pattern_matching(self):
        """
        Stage 3: EXPLORATORY pattern matching.

        WARNING: This is NOT scientific validation!
        These are exploratory findings that identify potential patterns
        for further investigation. They are NOT validated claims.
        """
        self._log("\n" + "="*70)
        self._log("STAGE 3: EXPLORATORY PATTERN MATCHING")
        self._log("="*70)
        self._log("WARNING: This is exploratory, NOT scientific validation!")
        self._log("Findings here are potential patterns, not validated claims.")

        stage_results = {
            "started": datetime.now().isoformat(),
            "warning": "EXPLORATORY ONLY - Not scientific validation",
            "measurements_tested": 0,
            "potential_patterns": [],
            "interesting": [],
            "weak": []
        }

        try:
            filtered = self.results["stages"].get("data_quality", {}).get("filtered_measurements", [])

            if not filtered:
                self._log("No measurements passed quality filter")
            else:
                self._log(f"Testing {len(filtered)} measurements for patterns...")

                for m in filtered:
                    name = m.get("name", "unknown")
                    value = m.get("value")

                    if value is None:
                        continue

                    try:
                        result = self.research_tools.research_any(
                            domain=self._sanitize_name(self.problem),
                            target=name,
                            measured_value=float(value)
                        )

                        stage_results["measurements_tested"] += 1
                        error_pct = result.get("percent_error", 100)

                        pattern_data = {
                            "name": name,
                            "value": value,
                            "formula": result.get("best_formula"),
                            "error_pct": error_pct,
                            "data_quality": m.get("data_quality"),
                            "epistemological_status": "EXPLORATORY - not validated"
                        }
                        stage_results["potential_patterns"].append(pattern_data)

                        # Categorize by interest level (NOT validation!)
                        if error_pct < 1.0:
                            stage_results["interesting"].append(pattern_data)
                            self._log(f"  INTERESTING: {name} = {value} ~ {result.get('best_formula')} ({error_pct:.3f}%)")
                        elif error_pct < 5.0:
                            stage_results["weak"].append(pattern_data)
                            self._log(f"  weak: {name} = {value} ~ {result.get('best_formula')} ({error_pct:.2f}%)")

                    except Exception as e:
                        self._log(f"  Error testing {name}: {e}")

                self._log(f"\nExploratory pattern matching complete:")
                self._log(f"  Tested: {stage_results['measurements_tested']}")
                self._log(f"  Interesting (<1% error): {len(stage_results['interesting'])}")
                self._log(f"  Weak (1-5% error): {len(stage_results['weak'])}")
                self._log(f"  NOTE: These are NOT validated - require rigorous testing")

        except Exception as e:
            self._log(f"Pattern matching error: {e}")
            stage_results["error"] = str(e)

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["exploratory_pattern_matching"] = stage_results
        self._save_results()

    def _stage_hypothesis_generation(self, max_iterations: int = 20):
        """Stage 4: Generate and test Z²-based hypotheses."""
        self._log("\n" + "="*70)
        self._log("STAGE 4: HYPOTHESIS GENERATION")
        self._log("="*70)

        stage_results = {
            "started": datetime.now().isoformat(),
            "hypotheses_generated": 0,
            "hypotheses_tested": 0,
            "promising": [],
            "refuted": [],
            "best_hypothesis": None
        }

        try:
            self._log(f"Generating Z²-based hypotheses for: {self.problem}")
            self._log(f"Max iterations: {max_iterations}")

            session = self.hypothesis_engine.research_until_exhausted(
                self.problem,
                max_iterations=max_iterations
            )

            stage_results["hypotheses_generated"] = len(session.hypotheses_generated)
            stage_results["hypotheses_tested"] = session.hypotheses_tested

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

                if h.confidence >= 0.4:
                    stage_results["promising"].append(h_data)
                else:
                    stage_results["refuted"].append(h_data)

            if session.best_hypothesis:
                stage_results["best_hypothesis"] = {
                    "statement": session.best_hypothesis.statement,
                    "confidence": session.best_hypothesis.confidence,
                    "principle": session.best_hypothesis.z2_principle,
                    "mechanism": session.best_hypothesis.mechanism,
                    "prediction": session.best_hypothesis.testable_prediction
                }

            self._log(f"\nHypothesis generation complete:")
            self._log(f"  Generated: {stage_results['hypotheses_generated']}")
            self._log(f"  Tested: {stage_results['hypotheses_tested']}")
            self._log(f"  Promising: {len(stage_results['promising'])}")
            self._log(f"  Refuted: {len(stage_results['refuted'])}")

        except Exception as e:
            self._log(f"Hypothesis generation error: {e}")
            stage_results["error"] = str(e)

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["hypothesis_generation"] = stage_results
        self._save_results()

    def _stage_rigorous_validation(self):
        """
        Stage 5: RIGOROUS SCIENTIFIC VALIDATION.

        This is the REAL science:
        - Uses only authoritative data (CODATA, PDG, Planck)
        - Predictions derived from Z² theory (not curve-fit)
        - Proper statistical significance with Bonferroni correction
        - Sigma deviations calculated from measurement uncertainty
        """
        self._log("\n" + "="*70)
        self._log("STAGE 5: RIGOROUS SCIENTIFIC VALIDATION")
        self._log("="*70)
        self._log("Using authoritative sources: CODATA, PDG, Planck, NuFIT")
        self._log("Applying Bonferroni correction for multiple comparisons")

        stage_results = {
            "started": datetime.now().isoformat(),
            "methodology": {
                "data_sources": ["CODATA 2022", "PDG 2024", "Planck 2020", "NuFIT 5.2"],
                "statistical_method": "Bonferroni-corrected sigma deviation",
                "derivation_requirement": "First principles from Z² = 32π/3"
            },
            "n_tests": len(Z2_PREDICTIONS),
            "bonferroni_threshold": 0.05 / len(Z2_PREDICTIONS),
            "validated": [],
            "inconclusive": [],
            "tension": [],
            "statistical_summary": {}
        }

        try:
            self._log(f"Testing {len(Z2_PREDICTIONS)} Z² predictions...")
            self._log(f"Bonferroni threshold: p < {stage_results['bonferroni_threshold']:.4f}")

            # Run rigorous validation
            results = self.scientific_validator.validate_all()

            for r in results:
                pred = Z2_PREDICTIONS.get(r.target)

                result_data = {
                    "target": r.target,
                    "prediction_name": pred.name if pred else r.target,
                    "formula": pred.formula if pred else "unknown",
                    "predicted": r.predicted,
                    "measured": r.measured,
                    "uncertainty": r.uncertainty,
                    "percent_error": r.percent_error,
                    "sigma_deviation": r.sigma_deviation,
                    "p_value": r.p_value,
                    "verdict": r.verdict,
                    "derivation": pred.derivation[:100] + "..." if pred else "",
                    "falsification": pred.falsification_criteria if pred else ""
                }

                if r.verdict == "VALIDATED":
                    stage_results["validated"].append(result_data)
                    self._log(f"  VALIDATED: {pred.name if pred else r.target}")
                    self._log(f"    {pred.formula if pred else '?'} = {r.predicted:.6f}")
                    self._log(f"    Measured: {r.measured:.6f} ± {r.uncertainty:.6f}")
                    self._log(f"    Deviation: {r.sigma_deviation:.2f}σ ({r.percent_error:.4f}%)")
                elif r.verdict == "INCONCLUSIVE":
                    stage_results["inconclusive"].append(result_data)
                    self._log(f"  INCONCLUSIVE: {pred.name if pred else r.target} ({r.sigma_deviation:.2f}σ)")
                else:
                    stage_results["tension"].append(result_data)
                    self._log(f"  TENSION: {pred.name if pred else r.target} ({r.sigma_deviation:.1f}σ)")

            # Statistical summary
            if results:
                stage_results["statistical_summary"] = {
                    "n_validated": len(stage_results["validated"]),
                    "n_inconclusive": len(stage_results["inconclusive"]),
                    "n_tension": len(stage_results["tension"]),
                    "mean_error_pct": sum(r.percent_error for r in results) / len(results),
                    "mean_sigma": sum(r.sigma_deviation for r in results) / len(results)
                }

            self._log(f"\nRigorous validation complete:")
            self._log(f"  Validated (σ < 2): {len(stage_results['validated'])}")
            self._log(f"  Inconclusive (2 < σ < 3): {len(stage_results['inconclusive'])}")
            self._log(f"  Tension (σ > 3): {len(stage_results['tension'])}")

            # Store validated findings in main results
            self.results["validated_findings"] = stage_results["validated"]

        except Exception as e:
            self._log(f"Rigorous validation error: {e}")
            stage_results["error"] = str(e)
            import traceback
            self._log(traceback.format_exc())

        stage_results["completed"] = datetime.now().isoformat()
        self.results["stages"]["rigorous_validation"] = stage_results
        self._save_results()

    def _stage_synthesis(self):
        """Stage 6: Synthesize findings with clear epistemological status."""
        self._log("\n" + "="*70)
        self._log("STAGE 6: SYNTHESIS")
        self._log("="*70)

        # Gather exploratory findings (clearly labeled)
        exploratory = self.results["stages"].get("exploratory_pattern_matching", {})
        if exploratory.get("interesting"):
            for p in exploratory["interesting"]:
                self.results["exploratory_findings"].append({
                    "type": "exploratory_pattern",
                    "status": "EXPLORATORY - requires validation",
                    "finding": f"{p['name']} ~ {p['formula']} ({p['error_pct']:.3f}%)",
                    "data_quality": p.get("data_quality", "unknown")
                })

        # Build conclusion
        conclusion_parts = [
            f"HermesFlow v2.0 Research Complete: {self.problem}",
            "",
            "=" * 60,
            "EPISTEMOLOGICAL STATUS OF FINDINGS",
            "=" * 60,
            ""
        ]

        # Validated findings (SCIENTIFIC)
        validated = self.results.get("validated_findings", [])
        conclusion_parts.append(f"SCIENTIFICALLY VALIDATED ({len(validated)}):")
        conclusion_parts.append("  (Derived from Z² theory, tested against authoritative data)")
        if validated:
            for v in validated:
                conclusion_parts.append(f"  ✓ {v['prediction_name']}: {v['formula']} ({v['sigma_deviation']:.2f}σ)")
        else:
            conclusion_parts.append("  None from current problem domain")
        conclusion_parts.append("")

        # Exploratory findings (NOT validated)
        exploratory_findings = self.results.get("exploratory_findings", [])
        conclusion_parts.append(f"EXPLORATORY PATTERNS ({len(exploratory_findings)}):")
        conclusion_parts.append("  (Potential patterns - NOT scientifically validated)")
        if exploratory_findings:
            for e in exploratory_findings[:5]:
                conclusion_parts.append(f"  ? {e['finding']}")
        else:
            conclusion_parts.append("  None found")
        conclusion_parts.append("")

        # Hypotheses
        hyp_stage = self.results["stages"].get("hypothesis_generation", {})
        promising = hyp_stage.get("promising", [])
        conclusion_parts.append(f"HYPOTHESES GENERATED ({len(promising)} promising):")
        if promising:
            for h in promising[:3]:
                conclusion_parts.append(f"  → {h['statement'][:100]}...")
        conclusion_parts.append("")

        # Key distinction
        conclusion_parts.extend([
            "=" * 60,
            "KEY DISTINCTION:",
            "  - VALIDATED: Derived from Z² theory, tested rigorously",
            "  - EXPLORATORY: Numerical patterns, require further investigation",
            "  - Post-hoc pattern matching is NOT scientific validation",
            "=" * 60
        ])

        self.results["conclusion"] = "\n".join(conclusion_parts)
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
    print("HERMESFLOW v2.0 - AUTONOMOUS RESEARCH WITH SCIENTIFIC RIGOR")
    print("="*70)
    print(f"Problem: {problem}")
    print(f"Started: {datetime.now().isoformat()}")
    print("="*70)

    runner = HermesFlowRunner(problem, use_legomena=True)
    results = runner.run(max_hypothesis_iterations=10)

    print("\n" + "="*70)
    print("RESEARCH COMPLETE")
    print("="*70)
    print(f"Status: {results['status']}")
    print(f"Output: {runner.output_dir}")


if __name__ == "__main__":
    main()
