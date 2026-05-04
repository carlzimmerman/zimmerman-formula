#!/usr/bin/env python3
"""
AUTO-RESEARCH LOOP
==================

The core autonomous research engine that:
1. Discovers domain and data sources dynamically
2. Generates structured hypotheses
3. Fetches real measurements
4. Validates against empirical data
5. Updates knowledge graph
6. Feeds learnings back for iteration

This is the "brain" that makes HermesFlow truly autonomous.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import json
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Add current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from universal_data_discovery import (
    UniversalDataDiscovery,
    StructuredHypothesisGenerator,
    DomainProfile,
    DataSource,
    Measurement,
    DataQuality
)
from truth_knowledge_graph import (
    TruthKnowledgeGraph,
    Truth,
    TruthLevel,
    EmpiricalSource
)
from scientific_validator import (
    ScientificValidator,
    ValidationResult,
    Z2, Z, PHI
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "hermesflow_research_output"


@dataclass
class ResearchIteration:
    """Result of one research iteration."""
    iteration: int
    hypothesis: Dict
    measurements_found: int
    validation_result: Optional[str]
    sigma_deviation: Optional[float]
    added_to_knowledge_graph: bool
    notes: str


@dataclass
class ResearchSession:
    """Complete research session."""
    topic: str
    started: str
    domain: str
    subdomain: str
    iterations: List[ResearchIteration]
    validated_findings: List[Dict]
    falsified_findings: List[Dict]
    total_hypotheses_tested: int
    total_measurements_collected: int
    conclusion: str
    completed: Optional[str] = None


class AutoResearchLoop:
    """
    Autonomous research loop for discovering Z² relationships.

    Works for ANY domain - not hardcoded.
    """

    def __init__(self, use_legomena: bool = True, verbose: bool = True):
        self.discovery = UniversalDataDiscovery(
            use_legomena=use_legomena,
            use_web_search=True
        )
        self.hypothesis_gen = StructuredHypothesisGenerator()
        self.knowledge_graph = TruthKnowledgeGraph()
        self.validator = ScientificValidator()
        self.verbose = verbose

        # Session state
        self.session: Optional[ResearchSession] = None
        self.domain: Optional[DomainProfile] = None
        self.sources: List[DataSource] = []
        self.all_measurements: List[Measurement] = []

        # Output
        OUTPUT_DIR.mkdir(exist_ok=True)

    def _log(self, message: str):
        """Log message if verbose."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")

    def research(self, topic: str, max_iterations: int = 10) -> ResearchSession:
        """
        Run complete research loop on a topic.

        1. Discover domain and quantities
        2. Find data sources
        3. Iterate: generate hypothesis → test → update knowledge
        4. Stop when exhausted or validated
        """
        self._log(f"\n{'='*70}")
        self._log(f"AUTO-RESEARCH LOOP")
        self._log(f"Topic: {topic}")
        self._log(f"Max iterations: {max_iterations}")
        self._log(f"{'='*70}\n")

        # Initialize session
        self.session = ResearchSession(
            topic=topic,
            started=datetime.now().isoformat(),
            domain="",
            subdomain="",
            iterations=[],
            validated_findings=[],
            falsified_findings=[],
            total_hypotheses_tested=0,
            total_measurements_collected=0,
            conclusion=""
        )

        # Phase 1: Discovery
        self._log("PHASE 1: DOMAIN DISCOVERY")
        self._log("-" * 40)
        self.domain, self.sources, self.all_measurements = self.discovery.full_discovery(topic)

        self.session.domain = self.domain.name
        self.session.subdomain = self.domain.subdomain
        self.session.total_measurements_collected = len(self.all_measurements)

        self._log(f"\nDiscovered: {self.domain.name}/{self.domain.subdomain}")
        self._log(f"Quantities: {len(self.domain.key_quantities)}")
        self._log(f"Sources: {len(self.sources)}")
        self._log(f"Measurements: {len(self.all_measurements)}")

        # Get prior findings from knowledge graph
        prior_validated = self._get_prior_findings("validated")
        prior_falsified = self._get_prior_findings("falsified")

        self._log(f"\nPrior validated: {len(prior_validated)}")
        self._log(f"Prior falsified: {len(prior_falsified)}")

        # Phase 2: Hypothesis iteration loop
        self._log(f"\nPHASE 2: HYPOTHESIS ITERATION")
        self._log("-" * 40)

        for i in range(max_iterations):
            self._log(f"\n--- Iteration {i+1}/{max_iterations} ---")

            # Generate hypothesis
            hypothesis = self.hypothesis_gen.generate(
                self.domain,
                validated=prior_validated,
                falsified=prior_falsified
            )

            if not hypothesis or not hypothesis.get("quantity"):
                self._log("  No hypothesis generated - exhausted")
                break

            self._log(f"  Hypothesis: {hypothesis.get('quantity')} = {hypothesis.get('formula')}")
            self._log(f"  Predicted: {hypothesis.get('predicted_value')}")

            # Test hypothesis against measurements
            result = self._test_hypothesis(hypothesis)

            iteration = ResearchIteration(
                iteration=i + 1,
                hypothesis=hypothesis,
                measurements_found=result.get("n_measurements", 0),
                validation_result=result.get("verdict"),
                sigma_deviation=result.get("sigma"),
                added_to_knowledge_graph=result.get("added_to_kg", False),
                notes=result.get("notes", "")
            )
            self.session.iterations.append(iteration)
            self.session.total_hypotheses_tested += 1

            # Update prior findings
            if result.get("verdict") == "VALIDATED":
                prior_validated.append(hypothesis)
                self.session.validated_findings.append({
                    "hypothesis": hypothesis,
                    "result": result
                })
                self._log(f"  ✓ VALIDATED (σ={result.get('sigma', '?'):.2f})")

            elif result.get("verdict") == "FALSIFIED":
                prior_falsified.append({
                    "quantity": hypothesis.get("quantity"),
                    "formula": hypothesis.get("formula"),
                    "error": result.get("error_pct", "?")
                })
                self.session.falsified_findings.append({
                    "hypothesis": hypothesis,
                    "result": result
                })
                self._log(f"  ✗ FALSIFIED (error={result.get('error_pct', '?'):.1f}%)")

            else:
                self._log(f"  ? INCONCLUSIVE - {result.get('notes', 'insufficient data')}")

            # Check if we should continue
            if len(self.session.validated_findings) >= 3:
                self._log("\n  Found 3+ validated findings - research productive!")

        # Phase 3: Synthesis
        self._log(f"\nPHASE 3: SYNTHESIS")
        self._log("-" * 40)

        self.session.conclusion = self._synthesize()
        self.session.completed = datetime.now().isoformat()

        # Save session
        self._save_session()

        return self.session

    def _get_prior_findings(self, level: str) -> List[Dict]:
        """Get prior findings from knowledge graph."""
        findings = []

        for truth in self.knowledge_graph.truths.values():
            if truth.level == level and truth.domain == self.domain.name:
                findings.append({
                    "quantity": truth.statement,
                    "formula": truth.formula,
                    "value": truth.predicted_value,
                    "measured": truth.measured_value,
                    "error": truth.error_percent
                })

        return findings

    def _test_hypothesis(self, hypothesis: Dict) -> Dict:
        """Test a hypothesis against measurements."""
        result = {
            "verdict": "INCONCLUSIVE",
            "n_measurements": 0,
            "sigma": None,
            "error_pct": None,
            "notes": "",
            "added_to_kg": False
        }

        # Get predicted value
        try:
            predicted = float(hypothesis.get("predicted_value", 0))
        except (ValueError, TypeError):
            result["notes"] = "Invalid predicted value"
            return result

        if predicted == 0:
            result["notes"] = "No predicted value"
            return result

        # Find relevant measurements
        quantity = hypothesis.get("quantity", "").lower()
        relevant = []

        for m in self.all_measurements:
            m_name = m.quantity.lower()
            # Match if quantity names overlap
            if (quantity in m_name or m_name in quantity or
                any(word in m_name for word in quantity.split("_") if len(word) > 3)):
                relevant.append(m)

        result["n_measurements"] = len(relevant)

        if len(relevant) < 3:
            result["notes"] = f"Only {len(relevant)} measurements found (need 3+)"
            return result

        # Calculate statistics
        values = [m.value for m in relevant]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 0.01

        # Calculate error and sigma
        error = abs(predicted - mean)
        error_pct = (error / mean) * 100 if mean != 0 else float('inf')
        sigma = error / std if std > 0 else float('inf')

        result["error_pct"] = error_pct
        result["sigma"] = sigma

        # Determine verdict
        if sigma < 2:
            result["verdict"] = "VALIDATED"
            # Add to knowledge graph
            self._add_to_knowledge_graph(hypothesis, mean, std, relevant)
            result["added_to_kg"] = True
        elif sigma > 3:
            result["verdict"] = "FALSIFIED"
            # Add falsified finding to knowledge graph
            self._add_falsified_to_kg(hypothesis, mean, std, error_pct)
        else:
            result["verdict"] = "INCONCLUSIVE"
            result["notes"] = f"Marginal: 2σ < {sigma:.2f} < 3σ"

        return result

    def _add_to_knowledge_graph(self, hypothesis: Dict, measured: float,
                                 uncertainty: float, measurements: List[Measurement]):
        """Add validated finding to knowledge graph."""
        # Generate unique ID
        quantity = hypothesis.get("quantity", "unknown").replace(" ", "_")[:30]
        truth_id = f"{self.domain.name}_{quantity}_{datetime.now().strftime('%Y%m%d')}"

        # Get primary source
        source_name = measurements[0].source if measurements else "Unknown"

        try:
            self.knowledge_graph.add_prediction(
                id=truth_id,
                domain=self.domain.name,
                statement=f"{hypothesis.get('quantity')} = {hypothesis.get('formula')}",
                formula=hypothesis.get("formula", ""),
                predicted_value=float(hypothesis.get("predicted_value", 0)),
                derived_from=["z2_definition"],
                falsification_criteria=[hypothesis.get("falsification", "")]
            )

            # Validate it
            self.knowledge_graph.validate_prediction(
                truth_id,
                measured_value=measured,
                uncertainty=uncertainty,
                source=EmpiricalSource(
                    name=source_name,
                    type="measured",
                    citation=f"HermesFlow auto-discovery {datetime.now().date()}"
                )
            )

            self._log(f"  Added to knowledge graph: {truth_id}")
        except Exception as e:
            self._log(f"  Error adding to KG: {e}")

    def _add_falsified_to_kg(self, hypothesis: Dict, measured: float,
                             std: float, error_pct: float):
        """Add falsified finding to knowledge graph."""
        quantity = hypothesis.get("quantity", "unknown").replace(" ", "_")[:30]
        truth_id = f"{self.domain.name}_{quantity}_falsified_{datetime.now().strftime('%Y%m%d')}"

        try:
            truth = Truth(
                id=truth_id,
                level=TruthLevel.FALSIFIED.value,
                domain=self.domain.name,
                statement=f"FALSIFIED: {hypothesis.get('quantity')} = {hypothesis.get('formula')}",
                formula=hypothesis.get("formula", ""),
                predicted_value=float(hypothesis.get("predicted_value", 0)),
                measured_value=measured,
                error_percent=error_pct,
                notes=f"Error: {error_pct:.1f}%"
            )
            self.knowledge_graph.truths[truth_id] = truth
            self.knowledge_graph.save()
        except Exception as e:
            self._log(f"  Error adding falsified to KG: {e}")

    def _synthesize(self) -> str:
        """Synthesize research findings."""
        lines = [
            f"AUTO-RESEARCH COMPLETE: {self.session.topic}",
            "",
            f"Domain: {self.session.domain}/{self.session.subdomain}",
            f"Hypotheses tested: {self.session.total_hypotheses_tested}",
            f"Measurements collected: {self.session.total_measurements_collected}",
            "",
            "VALIDATED FINDINGS:",
        ]

        if self.session.validated_findings:
            for f in self.session.validated_findings:
                h = f["hypothesis"]
                r = f["result"]
                lines.append(f"  ✓ {h.get('quantity')} = {h.get('formula')} (σ={r.get('sigma', '?'):.2f})")
        else:
            lines.append("  None")

        lines.append("")
        lines.append("FALSIFIED FINDINGS:")

        if self.session.falsified_findings:
            for f in self.session.falsified_findings:
                h = f["hypothesis"]
                r = f["result"]
                lines.append(f"  ✗ {h.get('quantity')} = {h.get('formula')} ({r.get('error_pct', '?'):.1f}% error)")
        else:
            lines.append("  None")

        lines.append("")
        if self.session.validated_findings:
            lines.append("CONCLUSION: Found Z² relationships in this domain.")
        else:
            lines.append("CONCLUSION: No strong Z² relationships found. May require:")
            lines.append("  - Better data sources")
            lines.append("  - Different quantities to test")
            lines.append("  - Alternative Z² formulas")

        return "\n".join(lines)

    def _save_session(self):
        """Save research session to file."""
        topic_slug = self.session.topic.lower().replace(" ", "_")[:50]
        output_dir = OUTPUT_DIR / f"auto_{topic_slug}"
        output_dir.mkdir(exist_ok=True)

        # Save full session
        with open(output_dir / "session.json", "w") as f:
            json.dump(asdict(self.session), f, indent=2, default=str)

        # Save summary
        with open(output_dir / "summary.txt", "w") as f:
            f.write(self.session.conclusion)

        self._log(f"\nSession saved to: {output_dir}")

    def add_to_training_data(self, hypothesis: Dict, result: Dict):
        """
        Add validated finding to Legomena training set.

        This enables iterative improvement - the model learns from
        successful discoveries.
        """
        if result.get("verdict") != "VALIDATED":
            return

        training_example = {
            "domain": self.domain.name,
            "subdomain": self.domain.subdomain,
            "quantity": hypothesis.get("quantity"),
            "z2_formula": hypothesis.get("formula"),
            "predicted_value": hypothesis.get("predicted_value"),
            "measured_value": result.get("measured"),
            "sigma": result.get("sigma"),
            "derivation": hypothesis.get("derivation", []),
            "validated": True,
            "timestamp": datetime.now().isoformat()
        }

        training_file = Path(__file__).parent / "legomena_training" / "z2_validated.jsonl"
        training_file.parent.mkdir(exist_ok=True)

        with open(training_file, "a") as f:
            f.write(json.dumps(training_example) + "\n")

        self._log(f"  Added to training data: {training_file}")


def main():
    """Run auto-research loop."""
    import argparse

    parser = argparse.ArgumentParser(description="Auto-research loop for Z² discovery")
    parser.add_argument("topic", help="Research topic")
    parser.add_argument("--max-iterations", type=int, default=10, help="Max hypothesis iterations")
    parser.add_argument("--no-legomena", action="store_true", help="Disable Legomena")

    args = parser.parse_args()

    loop = AutoResearchLoop(use_legomena=not args.no_legomena)
    session = loop.research(args.topic, max_iterations=args.max_iterations)

    print("\n" + "="*70)
    print(session.conclusion)
    print("="*70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default test
        loop = AutoResearchLoop()
        session = loop.research("hurricane intensity and structure", max_iterations=5)
    else:
        main()
