#!/usr/bin/env python3
"""
DEEPENER: Recursive Research Decision Engine
=============================================

When CylleneFlow finds something significant (e.g., CV(dmin) ≈ φ),
the natural question is "why?" This module decides:

1. Is this finding significant enough to warrant deeper investigation?
2. What follow-up questions should we ask?
3. How deep should we go before consolidating?

This is the "brain" that turns findings into new research directions,
implementing the same intuition Carl has when he says "we should
investigate this further."

Architecture:
    Finding discovered → Deepener analyzes significance →
    Generates research questions → Triggers new research cycle →
    (Recurses until depth limit or no significant findings)

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import math
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict

# LLM imports
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class ResearchQuestion:
    """A question generated from a finding that warrants investigation."""
    question: str
    rationale: str
    expected_data_type: str
    domain: str
    parent_finding: str
    depth: int = 0
    priority: int = 1  # 1 = highest


@dataclass
class DeepeningDecision:
    """Result of analyzing whether to deepen research."""
    should_deepen: bool
    significance_score: float  # 0-1, how significant is this finding?
    questions: List[ResearchQuestion]
    reasoning: str
    recommended_depth: int  # How many levels deep to go
    batch_with_others: bool = False  # Should we batch this with other findings?


@dataclass
class DeepenerState:
    """Tracks the state of recursive deepening."""
    current_depth: int = 0
    max_depth: int = 3
    findings_at_depth: Dict[int, List[Dict]] = field(default_factory=dict)
    questions_generated: List[ResearchQuestion] = field(default_factory=list)
    questions_investigated: List[str] = field(default_factory=list)
    total_recursions: int = 0


# =============================================================================
# DEEPENER
# =============================================================================

class Deepener:
    """
    Recursive research decision engine.

    Decides when findings warrant deeper investigation and generates
    the research questions to pursue.

    Key insight: This mimics Carl's research intuition -
    when he finds CV(dmin) ≈ φ, he naturally asks "why would
    distance-to-station show golden ratio scaling?"

    The Deepener does the same, but automatically.
    """

    # Z² constants for context
    Z2 = 32 * math.pi / 3
    Z = math.sqrt(Z2)
    PHI = (1 + math.sqrt(5)) / 2

    # Significance thresholds
    HIGHLY_SIGNIFICANT = 0.8   # Definitely investigate
    MODERATELY_SIGNIFICANT = 0.5  # Maybe investigate
    LOW_SIGNIFICANCE = 0.3     # Probably skip

    def __init__(
        self,
        model: str = None,
        max_depth: int = 3,
        verbose: bool = True
    ):
        self.model = model or os.environ.get("LEGOMENA_MODEL", "legomena-31b")
        self.max_depth = max_depth
        self.verbose = verbose
        self.state = DeepenerState(max_depth=max_depth)

        # Track which patterns we've already investigated to avoid loops
        self._investigated_patterns: set = set()

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Deepener] {msg}")

    # =========================================================================
    # CORE DECISION LOGIC
    # =========================================================================

    def analyze_finding(
        self,
        finding: Dict,
        context: Dict = None
    ) -> DeepeningDecision:
        """
        Analyze a finding to decide if we should go deeper.

        Args:
            finding: The finding to analyze (e.g., CV(dmin) ≈ φ)
            context: Additional context (domain knowledge, related findings)

        Returns:
            DeepeningDecision with questions if we should deepen
        """
        # Create pattern signature to avoid loops
        pattern_sig = self._pattern_signature(finding)
        if pattern_sig in self._investigated_patterns:
            self._log(f"Already investigated pattern: {pattern_sig}")
            return DeepeningDecision(
                should_deepen=False,
                significance_score=0,
                questions=[],
                reasoning="Pattern already investigated",
                recommended_depth=0
            )

        # Calculate significance
        significance = self._calculate_significance(finding)

        self._log(f"Finding significance: {significance:.2f}")

        # Decide based on significance and current depth
        if self.state.current_depth >= self.max_depth:
            return DeepeningDecision(
                should_deepen=False,
                significance_score=significance,
                questions=[],
                reasoning=f"Max depth ({self.max_depth}) reached",
                recommended_depth=0
            )

        if significance < self.LOW_SIGNIFICANCE:
            return DeepeningDecision(
                should_deepen=False,
                significance_score=significance,
                questions=[],
                reasoning="Finding not significant enough for deeper investigation",
                recommended_depth=0
            )

        # Generate research questions
        questions = self._generate_questions(finding, context)

        # Determine how deep to go based on significance
        if significance >= self.HIGHLY_SIGNIFICANT:
            recommended_depth = min(3, self.max_depth - self.state.current_depth)
            should_deepen = True
        elif significance >= self.MODERATELY_SIGNIFICANT:
            recommended_depth = min(2, self.max_depth - self.state.current_depth)
            should_deepen = len(questions) > 0
        else:
            recommended_depth = 1
            should_deepen = len(questions) > 0 and significance > 0.4

        # Mark pattern as being investigated
        if should_deepen:
            self._investigated_patterns.add(pattern_sig)

        return DeepeningDecision(
            should_deepen=should_deepen,
            significance_score=significance,
            questions=questions,
            reasoning=self._explain_decision(finding, significance, questions),
            recommended_depth=recommended_depth,
            batch_with_others=(significance < self.HIGHLY_SIGNIFICANT)
        )

    def _calculate_significance(self, finding: Dict) -> float:
        """
        Calculate how significant a finding is.

        Factors:
        - Error percentage (lower = more significant)
        - Sample size (larger = more significant)
        - Target type (fundamental constants more significant)
        - Novelty (new patterns more significant than variants)
        """
        score = 0.0

        # Error contribution (0-0.4)
        error = finding.get('error_percent', finding.get('error', 100))
        if error < 0.1:
            score += 0.4  # Extremely precise
        elif error < 1:
            score += 0.3  # Very precise
        elif error < 5:
            score += 0.2  # Reasonably precise
        elif error < 10:
            score += 0.1

        # Sample size contribution (0-0.2)
        n = finding.get('n_samples', 0)
        if n >= 1000:
            score += 0.2
        elif n >= 100:
            score += 0.15
        elif n >= 30:
            score += 0.1

        # Target type contribution (0-0.3)
        target = str(finding.get('target', '')).lower()
        if 'φ' in target or 'phi' in target:
            score += 0.3  # Golden ratio is fundamental
        elif 'z²' in target or 'z2' in target:
            score += 0.3  # Z² is the core formula
        elif 'z' in target:
            score += 0.25
        elif 'π' in target or 'pi' in target:
            score += 0.2
        else:
            score += 0.1

        # Quantity novelty contribution (0-0.1)
        quantity = finding.get('quantity', '')
        if 'ratio' in quantity.lower():
            score += 0.1  # Ratios are more interesting
        elif 'cv' in quantity.lower():
            score += 0.08
        else:
            score += 0.05

        return min(1.0, score)

    def _pattern_signature(self, finding: Dict) -> str:
        """Create unique signature for a finding pattern."""
        domain = finding.get('domain', 'unknown')
        quantity = finding.get('quantity', 'unknown')
        target = finding.get('target', 'unknown')
        return f"{domain}:{quantity}:{target}"

    # =========================================================================
    # QUESTION GENERATION
    # =========================================================================

    def _generate_questions(
        self,
        finding: Dict,
        context: Dict = None
    ) -> List[ResearchQuestion]:
        """
        Generate research questions from a finding.

        Example:
            Finding: CV(dmin) ≈ φ
            Questions:
            1. Why does distance-to-station show golden ratio scaling?
            2. Is this related to seismic network geometry?
            3. Does this pattern hold for different magnitude ranges?
        """
        questions = []

        quantity = finding.get('quantity', 'unknown')
        target = finding.get('target', 'unknown')
        domain = finding.get('domain', 'unknown')
        value = finding.get('value', 0)
        error = finding.get('error_percent', finding.get('error', 0))

        # Use LLM if available for better questions
        if OLLAMA_AVAILABLE:
            llm_questions = self._generate_questions_with_llm(finding, context)
            if llm_questions:
                questions.extend(llm_questions)
                return questions[:5]  # Limit to 5 questions

        # Fallback: Template-based question generation

        # Question 1: Why this pattern?
        questions.append(ResearchQuestion(
            question=f"Why does {quantity} in {domain} show {target} scaling ({value:.4f} with {error:.2f}% error)?",
            rationale="Understanding the mechanism behind the pattern",
            expected_data_type="related measurements or theoretical models",
            domain=domain,
            parent_finding=self._pattern_signature(finding),
            depth=self.state.current_depth + 1,
            priority=1
        ))

        # Question 2: Robustness check
        questions.append(ResearchQuestion(
            question=f"Does the {quantity} ≈ {target} pattern hold across different subsets or time periods?",
            rationale="Verifying pattern robustness and universality",
            expected_data_type="time-series or segmented data",
            domain=domain,
            parent_finding=self._pattern_signature(finding),
            depth=self.state.current_depth + 1,
            priority=2
        ))

        # Question 3: Related quantities
        questions.append(ResearchQuestion(
            question=f"What other quantities in {domain} might show similar Z² or φ patterns?",
            rationale="Exploring pattern generality within domain",
            expected_data_type="alternative measurements",
            domain=domain,
            parent_finding=self._pattern_signature(finding),
            depth=self.state.current_depth + 1,
            priority=3
        ))

        # Question 4: Cross-domain
        if self.state.current_depth == 0:
            questions.append(ResearchQuestion(
                question=f"Do similar {quantity} patterns appear in other scientific domains?",
                rationale="Testing Z² universality across fields",
                expected_data_type="cross-domain datasets",
                domain="cross-domain",
                parent_finding=self._pattern_signature(finding),
                depth=self.state.current_depth + 1,
                priority=4
            ))

        return questions

    def _generate_questions_with_llm(
        self,
        finding: Dict,
        context: Dict = None
    ) -> List[ResearchQuestion]:
        """Use LLM to generate more sophisticated questions."""

        quantity = finding.get('quantity', 'unknown')
        target = finding.get('target', 'unknown')
        domain = finding.get('domain', 'unknown')
        value = finding.get('value', 0)
        error = finding.get('error_percent', finding.get('error', 0))

        prompt = f"""I found a significant pattern in scientific data:

Domain: {domain}
Finding: {quantity} = {value:.6f}
This matches: {target} with {error:.4f}% error

Z² Framework context:
- Z² = 32π/3 = {self.Z2:.6f} (the fundamental geometric constant)
- φ = (1+√5)/2 = {self.PHI:.6f} (golden ratio)
- Z = √(Z²) = {self.Z:.6f}

Generate 3-4 specific research questions that would help understand WHY this pattern exists.
Focus on:
1. Physical/mathematical mechanisms
2. Data validation approaches
3. Related measurements to check
4. Cross-domain connections

Format each question as:
Q: [question]
TYPE: [theoretical/empirical/validation/cross-domain]
DATA_NEEDED: [what kind of data would answer this]
"""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={"temperature": 0.3}
            )

            # Parse response
            questions = self._parse_llm_questions(response['response'], finding, domain)
            return questions

        except Exception as e:
            self._log(f"LLM question generation failed: {e}")
            return []

    def _parse_llm_questions(
        self,
        response: str,
        finding: Dict,
        domain: str
    ) -> List[ResearchQuestion]:
        """Parse LLM response into ResearchQuestion objects."""
        questions = []

        lines = response.strip().split('\n')
        current_q = None
        current_type = "empirical"
        current_data = "related measurements"

        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                if current_q:
                    questions.append(ResearchQuestion(
                        question=current_q,
                        rationale=f"LLM-generated {current_type} question",
                        expected_data_type=current_data,
                        domain=domain,
                        parent_finding=self._pattern_signature(finding),
                        depth=self.state.current_depth + 1,
                        priority=len(questions) + 1
                    ))
                current_q = line[2:].strip()
            elif line.startswith('TYPE:'):
                current_type = line[5:].strip()
            elif line.startswith('DATA_NEEDED:'):
                current_data = line[12:].strip()

        # Add last question
        if current_q:
            questions.append(ResearchQuestion(
                question=current_q,
                rationale=f"LLM-generated {current_type} question",
                expected_data_type=current_data,
                domain=domain,
                parent_finding=self._pattern_signature(finding),
                depth=self.state.current_depth + 1,
                priority=len(questions) + 1
            ))

        return questions

    # =========================================================================
    # RECURSIVE EXECUTION
    # =========================================================================

    def deepen(
        self,
        finding: Dict,
        research_fn: callable,
        context: Dict = None
    ) -> List[Dict]:
        """
        Execute recursive deepening on a finding.

        Args:
            finding: The initial finding to investigate
            research_fn: Function that takes a question and returns findings
            context: Additional context

        Returns:
            List of all findings from deep investigation
        """
        all_findings = [finding]

        # Analyze if we should deepen
        decision = self.analyze_finding(finding, context)

        if not decision.should_deepen:
            self._log(f"Not deepening: {decision.reasoning}")
            return all_findings

        self._log(f"Deepening with {len(decision.questions)} questions")
        self._log(f"Recommended depth: {decision.recommended_depth}")

        # Process each question
        for question in decision.questions:
            if question.question in self.state.questions_investigated:
                continue

            self._log(f"Investigating: {question.question[:60]}...")
            self.state.questions_investigated.append(question.question)
            self.state.questions_generated.append(question)

            # Increase depth
            self.state.current_depth += 1
            self.state.total_recursions += 1

            try:
                # Run research on this question
                sub_findings = research_fn(question.question, question.domain)

                # Track findings at this depth
                if self.state.current_depth not in self.state.findings_at_depth:
                    self.state.findings_at_depth[self.state.current_depth] = []
                self.state.findings_at_depth[self.state.current_depth].extend(sub_findings)

                # Recurse on significant sub-findings
                for sub_finding in sub_findings:
                    if self.state.current_depth < self.max_depth:
                        deeper_findings = self.deepen(sub_finding, research_fn, context)
                        all_findings.extend(deeper_findings)
                    else:
                        all_findings.append(sub_finding)

            except Exception as e:
                self._log(f"Research failed for question: {e}")

            # Restore depth
            self.state.current_depth -= 1

        return all_findings

    def _explain_decision(
        self,
        finding: Dict,
        significance: float,
        questions: List[ResearchQuestion]
    ) -> str:
        """Generate human-readable explanation of deepening decision."""
        quantity = finding.get('quantity', 'unknown')
        target = finding.get('target', 'unknown')
        error = finding.get('error_percent', finding.get('error', 0))

        if significance >= self.HIGHLY_SIGNIFICANT:
            level = "HIGHLY SIGNIFICANT"
        elif significance >= self.MODERATELY_SIGNIFICANT:
            level = "MODERATELY SIGNIFICANT"
        else:
            level = "LOW SIGNIFICANCE"

        return (
            f"Finding {quantity} ≈ {target} ({error:.2f}% error) is {level} "
            f"(score: {significance:.2f}). Generated {len(questions)} research questions."
        )

    # =========================================================================
    # STATE MANAGEMENT
    # =========================================================================

    def reset_state(self):
        """Reset deepener state for new investigation."""
        self.state = DeepenerState(max_depth=self.max_depth)
        self._investigated_patterns.clear()

    def get_summary(self) -> Dict:
        """Get summary of deepening activities."""
        return {
            "total_recursions": self.state.total_recursions,
            "max_depth_reached": max(self.state.findings_at_depth.keys()) if self.state.findings_at_depth else 0,
            "questions_generated": len(self.state.questions_generated),
            "questions_investigated": len(self.state.questions_investigated),
            "patterns_investigated": len(self._investigated_patterns),
            "findings_by_depth": {
                depth: len(findings)
                for depth, findings in self.state.findings_at_depth.items()
            }
        }

    def save_state(self, path: Path):
        """Save deepener state to disk."""
        state_dict = {
            "current_depth": self.state.current_depth,
            "max_depth": self.state.max_depth,
            "total_recursions": self.state.total_recursions,
            "questions_investigated": self.state.questions_investigated,
            "questions_generated": [asdict(q) for q in self.state.questions_generated],
            "findings_at_depth": self.state.findings_at_depth,
            "patterns_investigated": list(self._investigated_patterns),
            "timestamp": datetime.now().isoformat()
        }
        with open(path, 'w') as f:
            json.dump(state_dict, f, indent=2, default=str)


# =============================================================================
# BATCH DEEPENING
# =============================================================================

class BatchDeepener:
    """
    Coordinates deepening across multiple findings.

    Instead of deepening each finding immediately, batches them
    and decides which are worth pursuing based on collective significance.

    This prevents the model from being updated after every micro-finding,
    instead batching updates for efficiency.
    """

    def __init__(
        self,
        deepener: Deepener,
        batch_threshold: int = 3,
        significance_threshold: float = 0.6
    ):
        self.deepener = deepener
        self.batch_threshold = batch_threshold
        self.significance_threshold = significance_threshold

        self.pending_findings: List[Dict] = []
        self.pending_decisions: List[DeepeningDecision] = []

    def add_finding(self, finding: Dict, context: Dict = None) -> Optional[DeepeningDecision]:
        """
        Add a finding to the batch.

        Returns decision immediately if highly significant,
        otherwise batches for later processing.
        """
        decision = self.deepener.analyze_finding(finding, context)

        # Immediate processing for highly significant findings
        if decision.significance_score >= Deepener.HIGHLY_SIGNIFICANT:
            return decision

        # Batch moderate findings
        if decision.should_deepen:
            self.pending_findings.append(finding)
            self.pending_decisions.append(decision)

        return None

    def should_process_batch(self) -> bool:
        """Check if we have enough findings to process."""
        return len(self.pending_findings) >= self.batch_threshold

    def process_batch(self) -> List[Tuple[Dict, DeepeningDecision]]:
        """
        Process batched findings and return prioritized list.

        Sorts by significance and returns findings worth deepening.
        """
        if not self.pending_findings:
            return []

        # Sort by significance
        paired = list(zip(self.pending_findings, self.pending_decisions))
        paired.sort(key=lambda x: x[1].significance_score, reverse=True)

        # Filter by threshold
        results = [
            (f, d) for f, d in paired
            if d.significance_score >= self.significance_threshold
        ]

        # Clear batch
        self.pending_findings = []
        self.pending_decisions = []

        return results


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEEPENER: Recursive Research Decision Engine")
    print("=" * 70)

    deepener = Deepener(verbose=True)

    # Test with seismology φ finding
    finding = {
        "domain": "seismology",
        "quantity": "CV(dmin)",
        "value": 1.618147,
        "target": "φ",
        "target_value": 1.618034,
        "error_percent": 0.007,
        "n_samples": 150
    }

    print(f"\nAnalyzing finding: {finding}")
    decision = deepener.analyze_finding(finding)

    print(f"\n{'='*70}")
    print("DECISION RESULT")
    print(f"{'='*70}")
    print(f"Should deepen: {decision.should_deepen}")
    print(f"Significance: {decision.significance_score:.2f}")
    print(f"Reasoning: {decision.reasoning}")
    print(f"Recommended depth: {decision.recommended_depth}")

    if decision.questions:
        print(f"\nGenerated Questions:")
        for i, q in enumerate(decision.questions, 1):
            print(f"  {i}. {q.question}")
            print(f"     Type: {q.expected_data_type}")
