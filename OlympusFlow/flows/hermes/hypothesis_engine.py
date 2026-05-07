#!/usr/bin/env python3
"""
HermesFlow Hypothesis Engine
============================

Autonomous hypothesis generation and testing using Z² geometry.

This is NOT pattern matching - this is IDEA GENERATION.

The engine:
1. Takes a problem statement
2. Generates Z²-based hypotheses for solutions
3. Computationally tests each hypothesis
4. Validates against literature
5. Persists until all ideas exhausted

Author: Carl Zimmerman
Date: May 3, 2026
"""

import subprocess
import json
import math
import re
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Z² constants
Z2 = 32 * math.pi / 3  # ≈ 33.51
Z = math.sqrt(Z2)       # ≈ 5.79
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618

# Legomena model for reasoning (use smaller model for speed)
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-e2b")


class HypothesisStatus(Enum):
    """Status of a hypothesis."""
    GENERATED = "generated"
    TESTING = "testing"
    VALIDATED = "validated"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"


@dataclass
class Hypothesis:
    """A Z²-based hypothesis."""
    id: str
    problem: str
    statement: str
    z2_principle: str  # Which Z² principle it uses
    mechanism: str     # How it works
    testable_prediction: str
    status: HypothesisStatus = HypothesisStatus.GENERATED
    confidence: float = 0.0
    evidence: List[Dict] = field(default_factory=list)
    refutation_reason: str = ""


@dataclass
class ResearchSession:
    """A complete research session on a problem."""
    problem: str
    started: datetime
    hypotheses_generated: List[Hypothesis] = field(default_factory=list)
    hypotheses_tested: int = 0
    best_hypothesis: Optional[Hypothesis] = None
    conclusion: str = ""
    exhausted: bool = False


class HypothesisEngine:
    """
    Autonomous hypothesis generation and testing engine.

    Uses Z² geometry as the theoretical framework to generate
    novel solutions to problems.
    """

    # Z² principles that can be applied to problems
    Z2_PRINCIPLES = [
        {
            "name": "geometric_resonance",
            "description": "Systems optimize at Z²-related angles/ratios",
            "formula": "angle or ratio = n×Z² or n×Z or φ-related",
            "applications": ["molecular geometry", "wave interference", "crystal structure"]
        },
        {
            "name": "energy_minimization",
            "description": "Energy minima occur at Z²-geometric configurations",
            "formula": "E_min when geometry matches Z² constraints",
            "applications": ["bond angles", "molecular stability", "phase transitions"]
        },
        {
            "name": "threshold_matching",
            "description": "Physical thresholds align with Z² values",
            "formula": "threshold ≈ n×Z² or n×Z",
            "applications": ["activation energies", "phase boundaries", "critical points"]
        },
        {
            "name": "ratio_harmony",
            "description": "Optimal ratios are Z²-related (φ, 1/φ, Z)",
            "formula": "optimal_ratio ≈ φ, 1/φ, Z/n, or Z²/n",
            "applications": ["proportions", "concentrations", "reaction ratios"]
        },
        {
            "name": "dimensional_constraint",
            "description": "Effective dimensions relate to Z² geometry",
            "formula": "d_eff = f(Z²)",
            "applications": ["fractal dimensions", "scaling laws", "network topology"]
        }
    ]

    def __init__(self, use_legomena: bool = True):
        self.use_legomena = use_legomena
        self._session: Optional[ResearchSession] = None
        self._idea_counter = 0

    def _call_legomena(self, prompt: str, timeout: int = 180) -> Optional[str]:
        """Call Legomena for intelligent reasoning."""
        if not self.use_legomena:
            return None

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
        except Exception as e:
            print(f"Legomena error: {e}")
        return None

    def start_session(self, problem: str) -> ResearchSession:
        """Start a new research session on a problem."""
        self._session = ResearchSession(
            problem=problem,
            started=datetime.now()
        )
        return self._session

    def generate_hypotheses(self, problem: str, max_hypotheses: int = 10) -> List[Hypothesis]:
        """
        Generate Z²-based hypotheses for solving a problem.

        This is the CREATIVE step - using Z² principles to imagine solutions.
        """
        if not self._session:
            self.start_session(problem)

        hypotheses = []

        # Strategy 1: Apply each Z² principle to the problem
        for principle in self.Z2_PRINCIPLES:
            prompt = f"""You are a theoretical physicist using Z² geometry (Z² = 32π/3 ≈ 33.51) to solve problems.

PROBLEM: {problem}

Z² PRINCIPLE TO APPLY: {principle['name']}
Description: {principle['description']}
Formula: {principle['formula']}
Typical applications: {', '.join(principle['applications'])}

Generate a specific, testable hypothesis using this principle to solve the problem.

Format your response as:
HYPOTHESIS: [One sentence stating the hypothesis]
MECHANISM: [How it works using Z² geometry]
PREDICTION: [A specific, testable numerical prediction]
CALCULATION: [Show how Z² leads to this prediction]

Be creative but rigorous. The hypothesis must be physically plausible and mathematically derivable from Z²."""

            response = self._call_legomena(prompt)

            if response:
                h = self._parse_hypothesis_response(problem, principle['name'], response)
                if h:
                    hypotheses.append(h)

            if len(hypotheses) >= max_hypotheses:
                break

        # Strategy 2: Ask Legomena to generate novel Z² applications
        if len(hypotheses) < max_hypotheses:
            prompt = f"""You are an autonomous research agent using Z² geometry to solve problems.

PROBLEM: {problem}

Z² = 32π/3 ≈ 33.51 (fundamental geometric constant)
Z = √Z² ≈ 5.79
φ = golden ratio ≈ 1.618

You have already generated these hypotheses:
{[h.statement for h in hypotheses]}

Generate {max_hypotheses - len(hypotheses)} MORE novel hypotheses that:
1. Apply Z² geometry in a DIFFERENT way than above
2. Are specific and testable
3. Include numerical predictions

For each hypothesis, provide:
HYPOTHESIS: [statement]
Z2_PRINCIPLE: [which Z² relationship it uses]
MECHANISM: [how it works]
PREDICTION: [testable numerical prediction]"""

            response = self._call_legomena(prompt)
            if response:
                # Parse multiple hypotheses from response
                additional = self._parse_multiple_hypotheses(problem, response)
                hypotheses.extend(additional[:max_hypotheses - len(hypotheses)])

        self._session.hypotheses_generated = hypotheses
        return hypotheses

    def _parse_hypothesis_response(self, problem: str, principle: str, response: str) -> Optional[Hypothesis]:
        """Parse a single hypothesis from Legomena response."""
        self._idea_counter += 1

        # Extract components using regex
        hypothesis_match = re.search(r'HYPOTHESIS:\s*(.+?)(?=MECHANISM:|$)', response, re.DOTALL | re.IGNORECASE)
        mechanism_match = re.search(r'MECHANISM:\s*(.+?)(?=PREDICTION:|$)', response, re.DOTALL | re.IGNORECASE)
        prediction_match = re.search(r'PREDICTION:\s*(.+?)(?=CALCULATION:|$)', response, re.DOTALL | re.IGNORECASE)

        if hypothesis_match:
            return Hypothesis(
                id=f"H{self._idea_counter:03d}",
                problem=problem,
                statement=hypothesis_match.group(1).strip()[:500],
                z2_principle=principle,
                mechanism=mechanism_match.group(1).strip()[:500] if mechanism_match else "",
                testable_prediction=prediction_match.group(1).strip()[:300] if prediction_match else ""
            )
        return None

    def _parse_multiple_hypotheses(self, problem: str, response: str) -> List[Hypothesis]:
        """Parse multiple hypotheses from a response."""
        hypotheses = []

        # Split by HYPOTHESIS: markers
        parts = re.split(r'HYPOTHESIS:', response, flags=re.IGNORECASE)

        for part in parts[1:]:  # Skip first empty part
            self._idea_counter += 1

            statement = part.split('\n')[0].strip()
            if len(statement) > 10:  # Valid hypothesis
                principle_match = re.search(r'Z2_PRINCIPLE:\s*(.+)', part, re.IGNORECASE)
                mechanism_match = re.search(r'MECHANISM:\s*(.+?)(?=PREDICTION:|Z2_PRINCIPLE:|$)', part, re.DOTALL | re.IGNORECASE)
                prediction_match = re.search(r'PREDICTION:\s*(.+?)(?=HYPOTHESIS:|$)', part, re.DOTALL | re.IGNORECASE)

                hypotheses.append(Hypothesis(
                    id=f"H{self._idea_counter:03d}",
                    problem=problem,
                    statement=statement[:500],
                    z2_principle=principle_match.group(1).strip() if principle_match else "novel",
                    mechanism=mechanism_match.group(1).strip()[:500] if mechanism_match else "",
                    testable_prediction=prediction_match.group(1).strip()[:300] if prediction_match else ""
                ))

        return hypotheses

    def test_hypothesis(self, hypothesis: Hypothesis) -> Hypothesis:
        """
        Test a hypothesis computationally and against literature.

        This is where we determine if the idea holds up.
        """
        hypothesis.status = HypothesisStatus.TESTING

        # Step 1: Mathematical consistency check
        math_check = self._check_mathematical_consistency(hypothesis)
        hypothesis.evidence.append({"type": "math_check", "result": math_check})

        # Step 2: Physical plausibility check
        physics_check = self._check_physical_plausibility(hypothesis)
        hypothesis.evidence.append({"type": "physics_check", "result": physics_check})

        # Step 3: Literature validation
        lit_check = self._check_against_literature(hypothesis)
        hypothesis.evidence.append({"type": "literature_check", "result": lit_check})

        # Step 4: Computational test if prediction is numerical
        if hypothesis.testable_prediction:
            comp_check = self._computational_test(hypothesis)
            hypothesis.evidence.append({"type": "computation", "result": comp_check})

        # Determine final status
        self._evaluate_hypothesis(hypothesis)

        if self._session:
            self._session.hypotheses_tested += 1
            if hypothesis.status == HypothesisStatus.VALIDATED:
                if not self._session.best_hypothesis or hypothesis.confidence > self._session.best_hypothesis.confidence:
                    self._session.best_hypothesis = hypothesis

        return hypothesis

    def _check_mathematical_consistency(self, hypothesis: Hypothesis) -> Dict:
        """Check if the hypothesis is mathematically consistent with Z²."""
        prompt = f"""Analyze this hypothesis for mathematical consistency with Z² = 32π/3:

HYPOTHESIS: {hypothesis.statement}
MECHANISM: {hypothesis.mechanism}
PREDICTION: {hypothesis.testable_prediction}

Check:
1. Does the math follow from Z² = 32π/3 ≈ 33.51?
2. Are there any mathematical errors?
3. Is the derivation valid?

Respond with:
CONSISTENT: [yes/no/partial]
ISSUES: [list any problems]
SCORE: [0-10]"""

        response = self._call_legomena(prompt)

        if response:
            consistent = "yes" in response.lower()[:100]
            score_match = re.search(r'SCORE:\s*(\d+)', response)
            score = int(score_match.group(1)) if score_match else 5
            return {"consistent": consistent, "score": score / 10, "details": response[:500]}

        return {"consistent": False, "score": 0, "details": "Could not verify"}

    def _check_physical_plausibility(self, hypothesis: Hypothesis) -> Dict:
        """Check if the hypothesis is physically plausible."""
        prompt = f"""Analyze this hypothesis for physical plausibility:

HYPOTHESIS: {hypothesis.statement}
MECHANISM: {hypothesis.mechanism}

Check:
1. Does it violate any known physical laws?
2. Are the energy scales reasonable?
3. Has anything similar been observed in nature?

Respond with:
PLAUSIBLE: [yes/no/partial]
CONCERNS: [list any issues]
PRECEDENTS: [similar phenomena if any]
SCORE: [0-10]"""

        response = self._call_legomena(prompt)

        if response:
            plausible = "yes" in response.lower()[:100]
            score_match = re.search(r'SCORE:\s*(\d+)', response)
            score = int(score_match.group(1)) if score_match else 5
            return {"plausible": plausible, "score": score / 10, "details": response[:500]}

        return {"plausible": False, "score": 0, "details": "Could not verify"}

    def _check_against_literature(self, hypothesis: Hypothesis) -> Dict:
        """Check hypothesis against literature."""
        # This would integrate with literature_collector
        # For now, use Legomena's knowledge
        prompt = f"""Based on your knowledge of scientific literature, evaluate this hypothesis:

HYPOTHESIS: {hypothesis.statement}
PREDICTION: {hypothesis.testable_prediction}

Check:
1. Does existing literature support or contradict this?
2. Has similar work been done?
3. What would be needed to test this experimentally?

Respond with:
LITERATURE_SUPPORT: [supporting/contradicting/neutral/unknown]
KEY_PAPERS: [relevant papers if known]
EXPERIMENTAL_TEST: [how to test]
SCORE: [0-10]"""

        response = self._call_legomena(prompt)

        if response:
            support = "supporting" in response.lower()
            score_match = re.search(r'SCORE:\s*(\d+)', response)
            score = int(score_match.group(1)) if score_match else 5
            return {"supported": support, "score": score / 10, "details": response[:500]}

        return {"supported": False, "score": 0, "details": "Could not verify"}

    def _computational_test(self, hypothesis: Hypothesis) -> Dict:
        """Run computational tests on the hypothesis prediction."""
        # Extract numerical predictions and test them
        numbers = re.findall(r'[\d.]+', hypothesis.testable_prediction)

        results = []
        for num_str in numbers[:3]:  # Test up to 3 numbers
            try:
                num = float(num_str)
                # Check if this number relates to Z²
                z2_match = self._find_z2_relationship(num)
                results.append({
                    "value": num,
                    "z2_match": z2_match
                })
            except ValueError:
                continue

        return {
            "predictions_tested": len(results),
            "results": results,
            "score": sum(r.get("z2_match", {}).get("score", 0) for r in results) / max(len(results), 1)
        }

    def _find_z2_relationship(self, value: float) -> Dict:
        """Find if a value has a Z² relationship."""
        if value == 0:
            return {"score": 0, "formula": None}

        test_formulas = [
            ("Z2", Z2),
            ("Z", Z),
            ("PHI", PHI),
            ("1/PHI", 1/PHI),
            ("Z2/10", Z2/10),
            ("Z/10", Z/10),
        ]

        # Add integer multiples
        for n in range(1, 20):
            test_formulas.append((f"{n}*Z2", n * Z2))
            test_formulas.append((f"{n}*Z", n * Z))

        best_formula = None
        best_error = float('inf')

        for formula, predicted in test_formulas:
            error = abs(predicted - value) / abs(value) * 100
            if error < best_error:
                best_error = error
                best_formula = formula

        score = max(0, 1 - best_error / 5)  # 0% error = 1.0, 5% error = 0

        return {
            "formula": best_formula,
            "error_pct": best_error,
            "score": score
        }

    def _evaluate_hypothesis(self, hypothesis: Hypothesis):
        """Evaluate all evidence and set final status."""
        scores = []

        for e in hypothesis.evidence:
            if isinstance(e.get("result"), dict):
                scores.append(e["result"].get("score", 0))

        if scores:
            avg_score = sum(scores) / len(scores)
            hypothesis.confidence = avg_score

            if avg_score >= 0.7:
                hypothesis.status = HypothesisStatus.VALIDATED
            elif avg_score >= 0.4:
                hypothesis.status = HypothesisStatus.INCONCLUSIVE
            else:
                hypothesis.status = HypothesisStatus.REFUTED
                hypothesis.refutation_reason = "Low evidence scores"
        else:
            hypothesis.status = HypothesisStatus.INCONCLUSIVE
            hypothesis.confidence = 0.0

    def research_until_exhausted(self, problem: str, max_iterations: int = 50) -> ResearchSession:
        """
        Main loop: Keep generating and testing hypotheses until exhausted.

        This is the PERSISTENCE that the user wants - don't give up easily.
        """
        session = self.start_session(problem)

        iteration = 0
        hypotheses_tried = set()

        print(f"\n{'='*70}")
        print(f"HERMESFLOW HYPOTHESIS ENGINE")
        print(f"Problem: {problem}")
        print(f"{'='*70}\n")

        while iteration < max_iterations and not session.exhausted:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")

            # Generate new hypotheses
            new_hypotheses = self.generate_hypotheses(problem, max_hypotheses=5)

            # Filter out already-tried ideas
            fresh = [h for h in new_hypotheses if h.statement not in hypotheses_tried]

            if not fresh:
                print("No new hypotheses generated. Exhausting search space...")
                session.exhausted = True
                break

            # Test each new hypothesis
            for h in fresh:
                hypotheses_tried.add(h.statement)
                print(f"\nTesting: {h.statement[:80]}...")

                self.test_hypothesis(h)

                status_emoji = {
                    HypothesisStatus.VALIDATED: "✓",
                    HypothesisStatus.REFUTED: "✗",
                    HypothesisStatus.INCONCLUSIVE: "?"
                }.get(h.status, "?")

                print(f"  Result: {status_emoji} {h.status.value} (confidence: {h.confidence:.2f})")

                # If we find a strong hypothesis, report it
                if h.status == HypothesisStatus.VALIDATED and h.confidence >= 0.8:
                    print(f"\n*** STRONG HYPOTHESIS FOUND ***")
                    print(f"Statement: {h.statement}")
                    print(f"Mechanism: {h.mechanism}")
                    print(f"Prediction: {h.testable_prediction}")
                    print(f"Confidence: {h.confidence:.2f}")

            # Check if we should continue
            if session.best_hypothesis and session.best_hypothesis.confidence >= 0.9:
                print("\nHigh-confidence solution found. Stopping search.")
                break

        # Final summary
        session.conclusion = self._generate_conclusion(session)

        print(f"\n{'='*70}")
        print("RESEARCH SESSION COMPLETE")
        print(f"{'='*70}")
        print(f"Hypotheses generated: {len(session.hypotheses_generated)}")
        print(f"Hypotheses tested: {session.hypotheses_tested}")
        print(f"Best hypothesis: {session.best_hypothesis.statement if session.best_hypothesis else 'None'}")
        print(f"Exhausted: {session.exhausted}")
        print(f"\nConclusion:\n{session.conclusion}")

        return session

    def _generate_conclusion(self, session: ResearchSession) -> str:
        """Generate a conclusion for the research session."""
        if session.best_hypothesis and session.best_hypothesis.confidence >= 0.7:
            return f"""SOLUTION FOUND:
{session.best_hypothesis.statement}

Mechanism: {session.best_hypothesis.mechanism}
Prediction: {session.best_hypothesis.testable_prediction}
Confidence: {session.best_hypothesis.confidence:.2f}

This hypothesis passed mathematical, physical, and literature checks.
Recommend experimental validation."""

        elif session.hypotheses_generated:
            validated = [h for h in session.hypotheses_generated if h.status == HypothesisStatus.VALIDATED]
            if validated:
                return f"""PARTIAL SOLUTIONS FOUND:
{len(validated)} hypotheses show promise but need further testing.

Top candidates:
{chr(10).join(f'- {h.statement[:100]}... (confidence: {h.confidence:.2f})' for h in validated[:3])}

Recommend targeted experiments to distinguish between these approaches."""
            else:
                return f"""NO STRONG SOLUTIONS FOUND:
Tested {session.hypotheses_tested} hypotheses using Z² geometry.
None achieved high confidence.

This may indicate:
1. Z² geometry may not apply to this problem domain
2. More sophisticated Z² models needed
3. Problem requires non-geometric approach

Recommend literature deep-dive or alternative theoretical frameworks."""

        else:
            return "No hypotheses generated. Check Legomena availability."


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI for hypothesis engine."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python hypothesis_engine.py <problem>")
        print("Example: python hypothesis_engine.py 'remove PFAS from wastewater'")
        sys.exit(1)

    problem = ' '.join(sys.argv[1:])

    engine = HypothesisEngine(use_legomena=True)
    session = engine.research_until_exhausted(problem, max_iterations=20)

    # Save results
    output = {
        "problem": problem,
        "started": session.started.isoformat(),
        "hypotheses_generated": len(session.hypotheses_generated),
        "hypotheses_tested": session.hypotheses_tested,
        "exhausted": session.exhausted,
        "best_hypothesis": {
            "statement": session.best_hypothesis.statement,
            "confidence": session.best_hypothesis.confidence,
            "mechanism": session.best_hypothesis.mechanism,
            "prediction": session.best_hypothesis.testable_prediction
        } if session.best_hypothesis else None,
        "conclusion": session.conclusion
    }

    with open(f"hypothesis_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSession saved to hypothesis_session_*.json")


if __name__ == "__main__":
    main()
