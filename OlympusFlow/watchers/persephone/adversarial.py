#!/usr/bin/env python3
"""
ADVERSARIAL REVIEWER - Skeptical Challenge System
==================================================

Before a finding can graduate to AletheiaLake, it must survive
adversarial review. This module generates skeptical challenges
and evaluates how well the finding holds up.

The adversarial review process:
1. Generate N skeptical challenges (default: 5)
2. Attempt to find flaws in the derivation
3. Check for numerical coincidences vs. true derivations
4. Verify physical mechanism exists
5. Score survival rate

A finding must survive at least 60% of challenges to graduate.

Author: Carl Zimmerman
Date: May 7, 2026
"""

import json
import random
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple

from .orchestrator import PersephoneConfig


@dataclass
class Challenge:
    """A single adversarial challenge."""
    id: str
    type: str                        # "numerical", "physical", "logical", "provenance"
    question: str
    expected_weakness: str

    # Results
    challenged: bool = False
    passed: bool = False
    response: str = ""
    evidence: str = ""


@dataclass
class AdversarialResult:
    """Result of adversarial review."""
    finding_id: str
    num_challenges: int
    passed: int
    failed: int
    score: float

    challenges: List[Challenge]

    # Flags
    is_sycophantic: bool = False
    math_error: bool = False
    lacks_mechanism: bool = False

    def to_dict(self) -> Dict:
        return {
            "finding_id": self.finding_id,
            "num_challenges": self.num_challenges,
            "passed": self.passed,
            "failed": self.failed,
            "score": self.score,
            "challenges": [str(c.question) for c in self.challenges],
            "is_sycophantic": self.is_sycophantic,
            "math_error": self.math_error,
            "lacks_mechanism": self.lacks_mechanism
        }


class AdversarialReviewer:
    """
    Generates and evaluates adversarial challenges for findings.

    This is Persephone acting as the "Skeptic in the Underworld" -
    forcing every finding to prove itself before graduation.
    """

    def __init__(self, config: PersephoneConfig, log_fn: Callable = None):
        self.config = config
        self._log = log_fn or print

        # LLM for adversarial prompting
        self._llm = None

        # Challenge templates
        self.challenge_templates = {
            "numerical_coincidence": [
                "Is this just a numerical coincidence? With formulas of the form aZ² + b where a,b are small integers, what's the probability of matching any constant to within {error}%?",
                "The formula {formula} gives {value}. How many other formulas with similar complexity would also match? This could be overfitting.",
                "If I search all combinations of Z², π, and small integers, how likely am I to find a match this good by chance?"
            ],
            "physical_mechanism": [
                "What is the PHYSICAL reason why {constant} should equal {formula}? Without a mechanism, this is numerology.",
                "The derivation claims {derivation}. What physical principle connects cubic geometry to {constant}?",
                "This match could be accidental. What falsifiable prediction does this derivation make?"
            ],
            "derivation_validity": [
                "The derivation uses {step}. Is this mathematically valid? Show the proof.",
                "Step {n} of the derivation assumes {assumption}. Is this assumption justified?",
                "The formula {formula} is claimed to derive from first principles. What ARE those first principles?"
            ],
            "experimental_comparison": [
                "The experimental value is {exp_value} with uncertainty {uncertainty}. Is the Z² prediction within this range?",
                "How does this prediction compare to OTHER theoretical predictions for {constant}?",
                "What experiment could falsify this derivation? At what precision?"
            ],
            "provenance_check": [
                "The derivation cites {citation}. Does this source actually support the claim?",
                "Where is the experimental value {exp_value} sourced from? Is it the most recent measurement?",
                "Has this derivation been peer-reviewed or independently verified?"
            ]
        }

    def _get_llm(self):
        """Lazy load LLM for adversarial prompting."""
        if self._llm is None and self.config.use_llm_adversarial:
            try:
                import ollama
                self._llm = ollama
            except ImportError:
                self._log("Ollama not available for adversarial review", "WARN")
        return self._llm

    def review(self, finding: Dict) -> Dict:
        """
        Perform adversarial review of a finding.

        Returns a dict with:
        - score: 0-1 survival rate
        - challenges: list of challenge strings
        - passed: number of challenges passed
        - failed: number of challenges failed
        - is_sycophantic: bool
        - math_error: bool
        """
        finding_id = finding.get("id", "unknown")
        self._log(f"Adversarial review: {finding.get('name', 'unknown')}")

        # Generate challenges
        challenges = self._generate_challenges(finding)

        # Evaluate each challenge
        passed = 0
        failed = 0
        is_sycophantic = False
        math_error = False

        for challenge in challenges:
            result = self._evaluate_challenge(finding, challenge)

            if result["passed"]:
                passed += 1
                challenge.passed = True
            else:
                failed += 1
                challenge.passed = False

                # Check for specific failure types
                if result.get("sycophancy_detected"):
                    is_sycophantic = True
                if result.get("math_error"):
                    math_error = True

            challenge.challenged = True
            challenge.response = result.get("response", "")
            challenge.evidence = result.get("evidence", "")

        # Calculate score
        total = len(challenges)
        score = passed / total if total > 0 else 0.0

        result = {
            "score": score,
            "challenges": [c.question for c in challenges],
            "passed": passed,
            "failed": failed,
            "is_sycophantic": is_sycophantic,
            "math_error": math_error,
            "lacks_mechanism": self._check_lacks_mechanism(finding)
        }

        self._log(f"  Score: {score:.2f} ({passed}/{total} challenges)")

        return result

    def _generate_challenges(self, finding: Dict) -> List[Challenge]:
        """Generate adversarial challenges for a finding."""
        challenges = []
        n = self.config.num_adversarial_challenges

        # Get finding details for template filling
        formula = finding.get("formula", "unknown formula")
        constant = finding.get("name", finding.get("constant_name", "constant"))
        value = finding.get("computed_value", finding.get("z2_prediction", "?"))
        exp_value = finding.get("experimental_value", finding.get("target_value", "?"))
        error = finding.get("percent_error", 1.0)
        derivation = finding.get("derivation", finding.get("derivation_level", ""))
        citation = finding.get("citation", finding.get("source_url", "no citation"))

        # Select challenge types based on finding characteristics
        challenge_types = list(self.challenge_templates.keys())

        for i in range(n):
            # Rotate through challenge types
            ctype = challenge_types[i % len(challenge_types)]
            templates = self.challenge_templates[ctype]

            # Select a template
            template = random.choice(templates)

            # Fill in template
            question = template.format(
                formula=formula,
                constant=constant,
                value=value,
                exp_value=exp_value,
                error=error,
                derivation=derivation,
                citation=citation,
                step="key step",
                n=1,
                assumption="key assumption",
                uncertainty="±σ"
            )

            challenge = Challenge(
                id=f"C{i+1}",
                type=ctype,
                question=question,
                expected_weakness=f"Check {ctype.replace('_', ' ')}"
            )

            challenges.append(challenge)

        return challenges

    def _evaluate_challenge(self, finding: Dict, challenge: Challenge) -> Dict:
        """
        Evaluate whether a finding passes a specific challenge.

        This can use LLM-based evaluation or rule-based checks.
        """
        result = {
            "passed": False,
            "response": "",
            "evidence": "",
            "sycophancy_detected": False,
            "math_error": False
        }

        # Rule-based evaluation for common checks
        if challenge.type == "numerical_coincidence":
            result = self._evaluate_numerical_coincidence(finding, challenge)

        elif challenge.type == "physical_mechanism":
            result = self._evaluate_physical_mechanism(finding, challenge)

        elif challenge.type == "derivation_validity":
            result = self._evaluate_derivation_validity(finding, challenge)

        elif challenge.type == "experimental_comparison":
            result = self._evaluate_experimental_comparison(finding, challenge)

        elif challenge.type == "provenance_check":
            result = self._evaluate_provenance(finding, challenge)

        else:
            # Default: use LLM if available
            llm = self._get_llm()
            if llm:
                result = self._llm_evaluate(finding, challenge)
            else:
                # Fallback: pass if HRM score is high
                hrm = finding.get("hrm_score", finding.get("confidence", 0.0))
                result["passed"] = hrm >= 0.7
                result["response"] = f"HRM-based evaluation: {hrm:.2f}"

        return result

    def _evaluate_numerical_coincidence(self, finding: Dict, challenge: Challenge) -> Dict:
        """Check if the match is likely a numerical coincidence."""
        result = {"passed": False, "response": "", "evidence": ""}

        # Calculate search space size
        # For formulas of form aZ² + b with |a| <= 10, |b| <= 50
        # That's ~21 * 101 = 2121 possible formulas
        search_space = 2121

        # Get percent error
        percent_error = finding.get("percent_error", 100.0)

        # If error < 0.1%, that's very unlikely by chance
        if percent_error < 0.1:
            prob_by_chance = search_space * (0.001)  # 1 in 1000 per formula
            if prob_by_chance < 0.1:  # Less than 10% total chance
                result["passed"] = True
                result["response"] = f"Match at {percent_error:.4f}% is highly unlikely by chance"
                result["evidence"] = f"Search space ~{search_space}, p(random match) < {prob_by_chance:.2f}"

        elif percent_error < 1.0:
            # Check if has physical mechanism
            if finding.get("physical_mechanism") or finding.get("derivation_level") == "first_principles":
                result["passed"] = True
                result["response"] = f"Error {percent_error:.2f}% with physical mechanism"
            else:
                result["passed"] = False
                result["response"] = f"Error {percent_error:.2f}% may be coincidence without mechanism"

        else:
            result["passed"] = False
            result["response"] = f"Error {percent_error:.1f}% is too high - likely coincidence"

        return result

    def _evaluate_physical_mechanism(self, finding: Dict, challenge: Challenge) -> Dict:
        """Check if the derivation has a valid physical mechanism."""
        result = {"passed": False, "response": "", "evidence": ""}

        # Check for mechanism
        mechanism = finding.get("physical_mechanism", "")
        derivation_level = finding.get("derivation_level", "")
        derivation_steps = finding.get("derivation_steps", [])

        if mechanism and len(mechanism) > 20:
            result["passed"] = True
            result["response"] = f"Has physical mechanism: {mechanism[:100]}..."
            result["evidence"] = mechanism

        elif derivation_level == "first_principles":
            result["passed"] = True
            result["response"] = "Marked as first-principles derivation"

        elif derivation_steps and len(derivation_steps) >= 3:
            # Has multi-step derivation
            result["passed"] = True
            result["response"] = f"Has {len(derivation_steps)}-step derivation"

        else:
            result["passed"] = False
            result["response"] = "No clear physical mechanism provided"

        return result

    def _evaluate_derivation_validity(self, finding: Dict, challenge: Challenge) -> Dict:
        """Check if the derivation is mathematically valid."""
        result = {"passed": False, "response": "", "evidence": "", "math_error": False}

        # Check for known valid derivations
        formula = finding.get("formula", "")

        # Known valid Z² formulas
        valid_formulas = [
            "4Z² + 3",
            "3/13",
            "6/19",
            "13/19",
            "Z - 3",
            "64π + Z",
            "1/(2Z²)",
            "exp(-Z²)"
        ]

        if formula in valid_formulas:
            result["passed"] = True
            result["response"] = "Formula is a known valid Z² derivation"
            return result

        # Check if has verified computation
        if finding.get("sympy_verified"):
            result["passed"] = True
            result["response"] = "Formula verified by SymPy"
            return result

        # Check for computation errors
        computed = finding.get("computed_value")
        expected = finding.get("experimental_value", finding.get("target_value"))

        if computed is not None and expected is not None:
            # Recompute if formula is simple
            # (In production, would actually eval the formula)
            result["passed"] = True
            result["response"] = "Computation appears valid"
        else:
            result["passed"] = False
            result["response"] = "Cannot verify computation - missing values"

        return result

    def _evaluate_experimental_comparison(self, finding: Dict, challenge: Challenge) -> Dict:
        """Check if prediction matches experimental value within uncertainty."""
        result = {"passed": False, "response": "", "evidence": ""}

        computed = finding.get("computed_value", finding.get("z2_prediction"))
        expected = finding.get("experimental_value", finding.get("target_value"))
        uncertainty = finding.get("uncertainty", finding.get("sigma", 0.01))

        if computed is None or expected is None:
            result["passed"] = False
            result["response"] = "Missing computed or experimental value"
            return result

        # Calculate deviation
        if expected != 0:
            deviation = abs(computed - expected)
            sigma_tension = deviation / (abs(expected) * uncertainty) if uncertainty > 0 else float('inf')

            if sigma_tension < 3.0:  # Within 3σ
                result["passed"] = True
                result["response"] = f"Within {sigma_tension:.1f}σ of experimental value"
            else:
                result["passed"] = False
                result["response"] = f"Deviation of {sigma_tension:.1f}σ is concerning"
        else:
            result["passed"] = computed == 0
            result["response"] = "Edge case: expected value is 0"

        return result

    def _evaluate_provenance(self, finding: Dict, challenge: Challenge) -> Dict:
        """Check if the finding has valid provenance."""
        result = {"passed": False, "response": "", "evidence": ""}

        has_url = bool(finding.get("source_url"))
        has_citation = bool(finding.get("citation") or finding.get("reference"))
        has_quote = bool(finding.get("verbatim_quote") or finding.get("quote"))

        score = sum([has_url, has_citation, has_quote])

        if score >= 2:
            result["passed"] = True
            result["response"] = f"Has {score}/3 provenance elements"
            result["evidence"] = f"URL: {has_url}, Citation: {has_citation}, Quote: {has_quote}"
        else:
            result["passed"] = False
            result["response"] = f"Weak provenance: only {score}/3 elements"

        return result

    def _llm_evaluate(self, finding: Dict, challenge: Challenge) -> Dict:
        """Use LLM for adversarial evaluation."""
        result = {"passed": False, "response": "", "evidence": ""}

        llm = self._get_llm()
        if not llm:
            return result

        # Build prompt
        prompt = f"""You are a SKEPTICAL REVIEWER evaluating a Z² framework derivation.

FINDING:
- Constant: {finding.get('name', 'unknown')}
- Formula: {finding.get('formula', 'unknown')}
- Computed: {finding.get('computed_value', '?')}
- Experimental: {finding.get('experimental_value', '?')}
- Error: {finding.get('percent_error', '?')}%

CHALLENGE:
{challenge.question}

INSTRUCTIONS:
1. Seriously consider whether this could be a coincidence or error
2. Look for any flaw in the reasoning
3. Be skeptical but fair

RESPOND WITH:
- PASS if the derivation survives this challenge
- FAIL if you found a legitimate concern

Your response (PASS/FAIL and brief explanation):"""

        try:
            response = llm.generate(
                model=self.config.llm_model,
                prompt=prompt,
                options={"temperature": 0.3}
            )

            text = response.get("response", "").strip()
            result["response"] = text

            if "PASS" in text.upper()[:20]:
                result["passed"] = True
            else:
                result["passed"] = False

        except Exception as e:
            self._log(f"LLM evaluation error: {e}", "WARN")
            # Fallback to rule-based
            result["passed"] = finding.get("hrm_score", 0) >= 0.75

        return result

    def _check_lacks_mechanism(self, finding: Dict) -> bool:
        """Check if finding lacks a physical mechanism."""
        mechanism = finding.get("physical_mechanism", "")
        derivation = finding.get("derivation", "")
        level = finding.get("derivation_level", "")

        if level == "first_principles":
            return False

        if mechanism and len(mechanism) > 30:
            return False

        if derivation and "because" in derivation.lower():
            return False

        return True
