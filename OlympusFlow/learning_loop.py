#!/usr/bin/env python3
"""
LEARNING LOOP - Success/Failure Pattern Learning
=================================================

Learns from successful and failed derivations to improve future searches:
1. Extract patterns from successful derivations
2. Categorize failure modes
3. Update template weights
4. Suggest similar targets

Author: Carl Zimmerman
Date: May 6, 2026
Version: 2.0.0
"""

import json
import math
import time
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum

# Import bandit selector for intelligent template selection
try:
    from OlympusFlow.bandit_selector import (
        ContextualTemplateBandit, FormulaTemplateBandit,
        SelectionStrategy, SelectionResult
    )
    BANDIT_AVAILABLE = True
except ImportError:
    BANDIT_AVAILABLE = False


class SuccessType(Enum):
    """Types of successful derivations."""
    FIRST_PRINCIPLES = "first_principles"  # Z² axiom + physics
    MATHEMATICAL = "mathematical"           # Pure math derivation
    NUMERICAL_FIT = "numerical_fit"         # Found formula but no physics
    KNOWN_FORMULA = "known_formula"         # Matched known template


class FailureType(Enum):
    """Types of derivation failures."""
    NO_FORMULA_FOUND = "no_formula"         # No formula matched
    NO_PHYSICAL_MECHANISM = "no_mechanism"  # Formula but no physics
    HIGH_ERROR = "high_error"               # Error > threshold
    NUMEROLOGY = "numerology"               # Multi-prompt rejected
    CONTRADICTS_EXPERIMENT = "contradicts"  # Doesn't match experiment


@dataclass
class LearnedPattern:
    """A pattern learned from a successful derivation."""
    pattern_id: str
    formula_template: str      # e.g., "a/b", "aZ² + b"
    domain: str                # e.g., "particle_physics", "thermodynamics"
    example_constant: str      # e.g., "sin²θ_W"
    example_formula: str       # e.g., "3/13"
    example_value: float
    success_count: int = 1
    last_used: str = ""
    weight: float = 1.0        # Higher = try first

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "LearnedPattern":
        return cls(**data)


@dataclass
class FailureRecord:
    """Record of a failed derivation attempt."""
    constant_name: str
    target_value: float
    failure_type: FailureType
    attempted_formulas: List[str]
    error_message: str
    timestamp: str
    domain: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["failure_type"] = self.failure_type.value
        return d


@dataclass
class SuggestedTarget:
    """A suggested target for future derivation."""
    constant_name: str
    target_value: float
    domain: str
    reason: str                # Why suggested
    priority: float            # 0-1, higher = more promising
    source_pattern: str = ""   # Pattern that suggested this


class LearningLoop:
    """
    Learns from derivation outcomes to improve future searches.

    Maintains a database of:
    - Successful patterns (what worked)
    - Failure modes (what didn't work)
    - Template weights (which templates to try first)
    """

    def __init__(self, storage_dir: Optional[Path] = None, use_bandit: bool = True):
        """
        Initialize the learning loop.

        Args:
            storage_dir: Directory to store learned patterns
            use_bandit: Whether to use multi-armed bandit for template selection
        """
        self.storage_dir = storage_dir or Path("/tmp/learning_loop")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # In-memory databases
        self.patterns: Dict[str, LearnedPattern] = {}
        self.failures: List[FailureRecord] = []
        self.template_weights: Dict[str, float] = self._default_weights()

        # Multi-armed bandit for intelligent template selection
        self.use_bandit = use_bandit and BANDIT_AVAILABLE
        if self.use_bandit:
            self.bandit = ContextualTemplateBandit(
                storage_path=self.storage_dir / "bandits"
            )
        else:
            self.bandit = None

        # Statistics
        self.stats = {
            "total_successes": 0,
            "total_failures": 0,
            "patterns_learned": 0,
            "suggestions_made": 0,
            "bandit_enabled": self.use_bandit
        }

        # Load existing data
        self._load()

    def _default_weights(self) -> Dict[str, float]:
        """Default template weights (higher = try first)."""
        return {
            "known_first_principles": 10.0,
            "simple_fraction": 8.0,
            "integer_z2": 7.0,
            "geometric": 6.0,
            "z_polynomial": 5.0,
            "pi_based": 4.0,
            "compound": 2.0
        }

    def learn_from_success(self, result: Dict) -> LearnedPattern:
        """
        Learn from a successful derivation.

        Args:
            result: Derivation result dict with:
                - constant_name: str
                - target_value: float
                - formula: str
                - formula_type: str
                - domain: str
                - confidence: float

        Returns:
            LearnedPattern that was created/updated
        """
        constant = result.get("constant_name", "unknown")
        formula = result.get("formula", "")
        formula_type = result.get("formula_type", "unknown")
        domain = result.get("domain", "general")
        value = result.get("target_value", 0)

        # Create or update pattern
        pattern_id = f"{formula_type}_{domain}"

        if pattern_id in self.patterns:
            # Update existing pattern
            pattern = self.patterns[pattern_id]
            pattern.success_count += 1
            pattern.weight = min(pattern.weight * 1.1, 20.0)  # Cap at 20
            pattern.last_used = datetime.now().isoformat()
        else:
            # Create new pattern
            pattern = LearnedPattern(
                pattern_id=pattern_id,
                formula_template=formula_type,
                domain=domain,
                example_constant=constant,
                example_formula=formula,
                example_value=value,
                last_used=datetime.now().isoformat()
            )
            self.patterns[pattern_id] = pattern

        # Update template weights (legacy)
        if formula_type in self.template_weights:
            self.template_weights[formula_type] *= 1.05
            self.template_weights[formula_type] = min(
                self.template_weights[formula_type], 20.0
            )

        # Update multi-armed bandit (modern approach)
        if self.use_bandit and self.bandit:
            derivation_level = result.get("derivation_level", "derived")
            hrm_score = result.get("hrm_score", result.get("confidence", 0.5))
            self.bandit.update(
                domain=domain,
                template_type=formula_type,
                derivation_level=derivation_level,
                hrm_score=hrm_score
            )

        self.stats["total_successes"] += 1
        self.stats["patterns_learned"] = len(self.patterns)

        self._save()
        return pattern

    def learn_from_failure(self, result: Dict) -> FailureRecord:
        """
        Learn from a failed derivation.

        Args:
            result: Derivation result dict with:
                - constant_name: str
                - target_value: float
                - failure_reason: str
                - attempted_formulas: List[str]
                - domain: str

        Returns:
            FailureRecord that was created
        """
        constant = result.get("constant_name", "unknown")
        value = result.get("target_value", 0)
        reason = result.get("failure_reason", "unknown")
        attempted = result.get("attempted_formulas", [])
        domain = result.get("domain", "general")

        # Categorize failure
        if "no formula" in reason.lower() or not attempted:
            failure_type = FailureType.NO_FORMULA_FOUND
        elif "mechanism" in reason.lower():
            failure_type = FailureType.NO_PHYSICAL_MECHANISM
        elif "numerology" in reason.lower():
            failure_type = FailureType.NUMEROLOGY
        elif "error" in reason.lower():
            failure_type = FailureType.HIGH_ERROR
        else:
            failure_type = FailureType.NO_FORMULA_FOUND

        record = FailureRecord(
            constant_name=constant,
            target_value=value,
            failure_type=failure_type,
            attempted_formulas=attempted[:10],  # Keep last 10
            error_message=reason,
            timestamp=datetime.now().isoformat(),
            domain=domain
        )

        self.failures.append(record)

        # Downweight templates that failed (legacy)
        for formula in attempted:
            for template_type in self.template_weights:
                if template_type in formula.lower():
                    self.template_weights[template_type] *= 0.98

        # Update multi-armed bandit with failure
        if self.use_bandit and self.bandit:
            # Infer template type from attempted formulas
            template_type = self._infer_template_type(attempted)
            if template_type:
                self.bandit.update(
                    domain=domain,
                    template_type=template_type,
                    derivation_level="failed",
                    hrm_score=0.0
                )

        self.stats["total_failures"] += 1

        # Keep only last 1000 failures
        if len(self.failures) > 1000:
            self.failures = self.failures[-1000:]

        self._save()
        return record

    def suggest_similar_targets(
        self,
        success: Dict,
        known_constants: Optional[List[Dict]] = None
    ) -> List[SuggestedTarget]:
        """
        Suggest similar targets based on a successful derivation.

        Args:
            success: Successful derivation result
            known_constants: List of known constants to search

        Returns:
            List of SuggestedTarget
        """
        suggestions = []
        domain = success.get("domain", "general")
        formula_type = success.get("formula_type", "")

        # Strategy 1: Same domain, different constant
        if known_constants:
            same_domain = [
                c for c in known_constants
                if c.get("domain") == domain
                and c.get("name") != success.get("constant_name")
            ]

            for const in same_domain[:5]:
                suggestions.append(SuggestedTarget(
                    constant_name=const["name"],
                    target_value=const["target_value"],
                    domain=domain,
                    reason=f"Same domain as {success.get('constant_name')}",
                    priority=0.8,
                    source_pattern=formula_type
                ))

        # Strategy 2: Same formula type, different domain
        # (e.g., if 3/13 worked, try other simple fractions)
        if formula_type == "simple_fraction":
            # Suggest looking for other small-integer fractions
            suggestions.append(SuggestedTarget(
                constant_name="[scan for simple fractions]",
                target_value=0,
                domain="any",
                reason="Simple fraction pattern successful",
                priority=0.7,
                source_pattern="simple_fraction"
            ))

        # Strategy 3: Suggest dimensionless constants in related domains
        related_domains = self._get_related_domains(domain)
        for rel_domain in related_domains:
            suggestions.append(SuggestedTarget(
                constant_name=f"[explore {rel_domain}]",
                target_value=0,
                domain=rel_domain,
                reason=f"Related to {domain}",
                priority=0.5,
                source_pattern=formula_type
            ))

        self.stats["suggestions_made"] += len(suggestions)
        return suggestions

    def _get_related_domains(self, domain: str) -> List[str]:
        """Get domains related to the given domain."""
        domain_map = {
            "particle_physics": ["quantum", "cosmology", "nuclear"],
            "cosmology": ["particle_physics", "astrophysics", "gravity"],
            "thermodynamics": ["statistical", "quantum", "materials"],
            "quantum": ["particle_physics", "materials", "thermodynamics"],
            "fluid_dynamics": ["chaos_theory", "statistical"],
            "mathematics": ["geometry", "chaos_theory"],
            "geometry": ["mathematics", "materials"],
        }
        return domain_map.get(domain, [])

    def _infer_template_type(self, formulas: List[str]) -> Optional[str]:
        """
        Infer the template type from a list of attempted formulas.

        Args:
            formulas: List of formula strings that were attempted

        Returns:
            Most likely template type, or None if can't determine
        """
        if not formulas:
            return None

        # Pattern matching for template types
        type_counts = {
            "simple_fraction": 0,
            "integer_z2": 0,
            "z_polynomial": 0,
            "z_fraction": 0,
            "geometric": 0,
            "pi_based": 0,
            "compound": 0
        }

        for formula in formulas:
            formula_lower = formula.lower()

            if "/" in formula and ("z" not in formula_lower or formula.count("/") == 1):
                # Simple fraction like 3/13
                if all(c.isdigit() or c in "/-" for c in formula.replace(" ", "")):
                    type_counts["simple_fraction"] += 1
                    continue

            if "z²" in formula_lower or "z**2" in formula_lower or "z^2" in formula_lower:
                if "/" in formula:
                    type_counts["z_fraction"] += 1
                else:
                    type_counts["integer_z2"] += 1
                continue

            if "z" in formula_lower and ("+" in formula or "-" in formula):
                type_counts["z_polynomial"] += 1
                continue

            if "arccos" in formula_lower or "arctan" in formula_lower or "arcsin" in formula_lower:
                type_counts["geometric"] += 1
                continue

            if "π" in formula or "pi" in formula_lower:
                type_counts["pi_based"] += 1
                continue

            if formula.count("(") > 1 or formula.count("/") > 1:
                type_counts["compound"] += 1
                continue

            # Default: simple fraction
            type_counts["simple_fraction"] += 1

        # Return the most common type
        if max(type_counts.values()) == 0:
            return None

        return max(type_counts.keys(), key=lambda k: type_counts[k])

    def get_template_priority_bandit(
        self,
        domain: str = "general",
        n: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Get template priority from multi-armed bandit.

        This uses Thompson Sampling to recommend templates,
        balancing exploration and exploitation.

        Args:
            domain: Physics domain for contextual selection
            n: Number of templates to return

        Returns:
            List of (template_name, estimated_value) sorted by value
        """
        if not self.use_bandit or not self.bandit:
            # Fall back to legacy weights
            return self.get_template_priority()[:n]

        # Get bandit recommendation
        templates = self.bandit.select_template_order(domain, n)

        # Get estimated values for each
        stats = self.bandit.get_stats()
        domain_stats = stats.get("domains", {}).get(domain, stats.get("global", {}))
        arms = domain_stats.get("arms", {})

        result = []
        for template in templates:
            if template in arms:
                value = arms[template].get("success_rate", 0.5)
            else:
                value = 0.5  # Default
            result.append((template, value))

        return result

    def get_exploration_summary(self) -> Dict:
        """
        Get summary of exploration vs exploitation behavior.

        Returns:
            Dict with exploration statistics
        """
        if not self.use_bandit or not self.bandit:
            return {"bandit_enabled": False}

        stats = self.bandit.get_stats()
        global_stats = stats.get("global", {})

        # Calculate exploration metrics
        total_pulls = global_stats.get("total_pulls", 0)
        arms = global_stats.get("arms", {})

        if total_pulls == 0:
            return {
                "bandit_enabled": True,
                "total_pulls": 0,
                "exploration_needed": True
            }

        # Entropy of pull distribution (higher = more exploration)
        pulls = [a.get("pulls", 0) for a in arms.values()]
        total = sum(pulls)
        if total > 0:
            probs = [p / total for p in pulls if p > 0]
            entropy = -sum(p * (p and math.log(p) or 0) for p in probs)
            max_entropy = math.log(len(arms))
            exploration_ratio = entropy / max_entropy if max_entropy > 0 else 0
        else:
            exploration_ratio = 1.0

        # Find undertested arms
        mean_pulls = total_pulls / len(arms) if arms else 0
        undertested = [
            name for name, a in arms.items()
            if a.get("pulls", 0) < mean_pulls * 0.5
        ]

        return {
            "bandit_enabled": True,
            "total_pulls": total_pulls,
            "total_successes": global_stats.get("total_successes", 0),
            "success_rate": global_stats.get("success_rate", 0),
            "exploration_ratio": exploration_ratio,
            "undertested_templates": undertested,
            "top_templates": global_stats.get("ranking", [])[:3]
        }

    def get_template_priority(self) -> List[Tuple[str, float]]:
        """
        Get templates sorted by priority (weight).

        Returns:
            List of (template_name, weight) sorted by weight descending
        """
        return sorted(
            self.template_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )

    def get_stats(self) -> Dict:
        """Get learning statistics."""
        return {
            **self.stats,
            "patterns": len(self.patterns),
            "failures_recorded": len(self.failures),
            "template_weights": self.template_weights.copy()
        }

    def _save(self):
        """Save learned data to disk."""
        # Save patterns
        patterns_file = self.storage_dir / "patterns.json"
        with open(patterns_file, "w") as f:
            json.dump(
                {k: v.to_dict() for k, v in self.patterns.items()},
                f, indent=2
            )

        # Save failures (last 100)
        failures_file = self.storage_dir / "failures.json"
        with open(failures_file, "w") as f:
            json.dump(
                [f.to_dict() for f in self.failures[-100:]],
                f, indent=2
            )

        # Save weights
        weights_file = self.storage_dir / "weights.json"
        with open(weights_file, "w") as f:
            json.dump(self.template_weights, f, indent=2)

        # Save stats
        stats_file = self.storage_dir / "stats.json"
        with open(stats_file, "w") as f:
            json.dump(self.stats, f, indent=2)

    def _load(self):
        """Load learned data from disk."""
        # Load patterns
        patterns_file = self.storage_dir / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file) as f:
                data = json.load(f)
                self.patterns = {
                    k: LearnedPattern.from_dict(v)
                    for k, v in data.items()
                }

        # Load failures
        failures_file = self.storage_dir / "failures.json"
        if failures_file.exists():
            with open(failures_file) as f:
                data = json.load(f)
                self.failures = [
                    FailureRecord(
                        constant_name=d["constant_name"],
                        target_value=d["target_value"],
                        failure_type=FailureType(d["failure_type"]),
                        attempted_formulas=d["attempted_formulas"],
                        error_message=d["error_message"],
                        timestamp=d["timestamp"],
                        domain=d.get("domain", "")
                    )
                    for d in data
                ]

        # Load weights
        weights_file = self.storage_dir / "weights.json"
        if weights_file.exists():
            with open(weights_file) as f:
                self.template_weights = json.load(f)

        # Load stats
        stats_file = self.storage_dir / "stats.json"
        if stats_file.exists():
            with open(stats_file) as f:
                self.stats = json.load(f)


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing LearningLoop...")

    loop = LearningLoop()

    # Simulate a success
    success_result = {
        "constant_name": "sin²θ_W",
        "target_value": 0.23122,
        "formula": "3/13",
        "formula_type": "simple_fraction",
        "domain": "particle_physics",
        "confidence": 0.85
    }

    pattern = loop.learn_from_success(success_result)
    print(f"Learned pattern: {pattern.pattern_id}")

    # Simulate a failure
    failure_result = {
        "constant_name": "von Karman",
        "target_value": 0.41,
        "failure_reason": "numerology - no physical mechanism",
        "attempted_formulas": ["1/Z", "Z/14", "-2Z + 12"],
        "domain": "fluid_dynamics"
    }

    record = loop.learn_from_failure(failure_result)
    print(f"Recorded failure: {record.failure_type.value}")

    # Get suggestions
    suggestions = loop.suggest_similar_targets(success_result)
    print(f"Suggestions: {len(suggestions)}")

    # Print stats
    print(f"\nStats: {loop.get_stats()}")
    print(f"Template priority: {loop.get_template_priority()}")
