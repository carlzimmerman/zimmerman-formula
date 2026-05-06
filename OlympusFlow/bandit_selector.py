#!/usr/bin/env python3
"""
MULTI-ARMED BANDIT TEMPLATE SELECTOR
=====================================

Implements UCB1 and Thompson Sampling for intelligent template selection.

Instead of simple linear weight updates, this module uses multi-armed bandit
algorithms to balance exploration (trying new templates) vs exploitation
(using templates that have worked).

Key Algorithms:
1. UCB1 (Upper Confidence Bound) - Deterministic, guaranteed regret bounds
2. Thompson Sampling - Bayesian, often better empirical performance
3. Epsilon-Greedy - Simple baseline for comparison

Why This Matters:
- Linear weight updates converge too slowly
- They don't handle the exploration/exploitation tradeoff
- Bandits provide theoretical guarantees on regret
- Thompson Sampling is state-of-the-art for this problem class

Author: Carl Zimmerman
Date: May 6, 2026
Version: 1.0.0
"""

import math
import random
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime
from enum import Enum
import numpy as np


class SelectionStrategy(Enum):
    """Available bandit strategies."""
    UCB1 = "ucb1"
    THOMPSON = "thompson"
    EPSILON_GREEDY = "epsilon_greedy"
    SOFTMAX = "softmax"


@dataclass
class ArmStats:
    """Statistics for a single arm (template)."""
    name: str
    pulls: int = 0              # Number of times selected
    successes: int = 0          # Number of successes
    failures: int = 0           # Number of failures
    total_reward: float = 0.0   # Cumulative reward

    # For Thompson Sampling (Beta distribution parameters)
    alpha: float = 1.0          # Prior successes + 1
    beta: float = 1.0           # Prior failures + 1

    # For tracking
    last_pulled: str = ""
    last_reward: float = 0.0

    @property
    def mean_reward(self) -> float:
        """Average reward per pull."""
        if self.pulls == 0:
            return 0.0
        return self.total_reward / self.pulls

    @property
    def success_rate(self) -> float:
        """Success rate (successes / pulls)."""
        if self.pulls == 0:
            return 0.5  # Prior
        return self.successes / self.pulls

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "ArmStats":
        return cls(**data)


@dataclass
class SelectionResult:
    """Result of a template selection."""
    selected_arm: str
    selection_reason: str
    ucb_value: float = 0.0
    thompson_sample: float = 0.0
    exploration_bonus: float = 0.0
    all_scores: Dict[str, float] = field(default_factory=dict)


class BanditSelector:
    """
    Multi-armed bandit for template selection.

    Implements UCB1 and Thompson Sampling for intelligent exploration
    vs exploitation tradeoff when selecting formula templates.
    """

    def __init__(
        self,
        arms: List[str],
        strategy: SelectionStrategy = SelectionStrategy.THOMPSON,
        ucb_c: float = 2.0,
        epsilon: float = 0.1,
        storage_path: Optional[Path] = None
    ):
        """
        Initialize the bandit selector.

        Args:
            arms: List of arm names (template types)
            strategy: Selection strategy to use
            ucb_c: Exploration parameter for UCB1 (higher = more exploration)
            epsilon: Exploration rate for epsilon-greedy
            storage_path: Path to persist state
        """
        self.strategy = strategy
        self.ucb_c = ucb_c
        self.epsilon = epsilon
        self.storage_path = storage_path

        # Initialize arms
        self.arms: Dict[str, ArmStats] = {
            name: ArmStats(name=name) for name in arms
        }

        # Global counters
        self.total_pulls = 0
        self.total_successes = 0

        # History for analysis
        self.history: List[Dict] = []

        # Load existing state
        if storage_path and storage_path.exists():
            self._load()

    def select(self) -> SelectionResult:
        """
        Select an arm using the configured strategy.

        Returns:
            SelectionResult with the selected arm and metadata
        """
        if self.strategy == SelectionStrategy.UCB1:
            return self._select_ucb1()
        elif self.strategy == SelectionStrategy.THOMPSON:
            return self._select_thompson()
        elif self.strategy == SelectionStrategy.EPSILON_GREEDY:
            return self._select_epsilon_greedy()
        elif self.strategy == SelectionStrategy.SOFTMAX:
            return self._select_softmax()
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def _select_ucb1(self) -> SelectionResult:
        """
        Select using UCB1 (Upper Confidence Bound).

        UCB1 selects: argmax_a [ Q(a) + c * sqrt(ln(t) / N(a)) ]

        Where:
        - Q(a) = average reward for arm a
        - t = total pulls across all arms
        - N(a) = pulls for arm a
        - c = exploration parameter
        """
        scores = {}

        for name, arm in self.arms.items():
            if arm.pulls == 0:
                # Unpulled arms get infinite score (must try first)
                scores[name] = float('inf')
            else:
                # UCB1 formula
                exploitation = arm.mean_reward
                exploration = self.ucb_c * math.sqrt(
                    math.log(self.total_pulls + 1) / arm.pulls
                )
                scores[name] = exploitation + exploration

        # Select arm with highest UCB score
        selected = max(scores.keys(), key=lambda x: scores[x])

        return SelectionResult(
            selected_arm=selected,
            selection_reason=f"UCB1 (c={self.ucb_c})",
            ucb_value=scores[selected],
            exploration_bonus=self.ucb_c * math.sqrt(
                math.log(self.total_pulls + 1) / max(self.arms[selected].pulls, 1)
            ),
            all_scores=scores
        )

    def _select_thompson(self) -> SelectionResult:
        """
        Select using Thompson Sampling.

        Thompson Sampling samples from each arm's posterior distribution
        and selects the arm with the highest sample.

        For binary rewards, we use Beta(alpha, beta) where:
        - alpha = successes + 1
        - beta = failures + 1
        """
        samples = {}

        for name, arm in self.arms.items():
            # Sample from Beta distribution
            sample = np.random.beta(arm.alpha, arm.beta)
            samples[name] = sample

        # Select arm with highest sample
        selected = max(samples.keys(), key=lambda x: samples[x])

        return SelectionResult(
            selected_arm=selected,
            selection_reason="Thompson Sampling",
            thompson_sample=samples[selected],
            all_scores=samples
        )

    def _select_epsilon_greedy(self) -> SelectionResult:
        """
        Select using epsilon-greedy strategy.

        With probability epsilon, select randomly (explore).
        Otherwise, select the arm with highest mean reward (exploit).
        """
        if random.random() < self.epsilon:
            # Explore: random selection
            selected = random.choice(list(self.arms.keys()))
            reason = f"Epsilon-greedy (explore, ε={self.epsilon})"
        else:
            # Exploit: select best arm
            selected = max(
                self.arms.keys(),
                key=lambda x: self.arms[x].mean_reward
            )
            reason = f"Epsilon-greedy (exploit)"

        scores = {name: arm.mean_reward for name, arm in self.arms.items()}

        return SelectionResult(
            selected_arm=selected,
            selection_reason=reason,
            all_scores=scores
        )

    def _select_softmax(self, temperature: float = 1.0) -> SelectionResult:
        """
        Select using softmax (Boltzmann) exploration.

        Probability of selecting arm a is proportional to exp(Q(a)/τ)
        where τ is the temperature parameter.
        """
        rewards = np.array([arm.mean_reward for arm in self.arms.values()])
        names = list(self.arms.keys())

        # Softmax probabilities
        exp_rewards = np.exp(rewards / temperature)
        probs = exp_rewards / exp_rewards.sum()

        # Sample according to probabilities
        selected_idx = np.random.choice(len(names), p=probs)
        selected = names[selected_idx]

        scores = dict(zip(names, probs.tolist()))

        return SelectionResult(
            selected_arm=selected,
            selection_reason=f"Softmax (τ={temperature})",
            all_scores=scores
        )

    def update(self, arm_name: str, reward: float, success: bool = None):
        """
        Update arm statistics after observing a reward.

        Args:
            arm_name: Name of the pulled arm
            reward: Observed reward (0-1 for binary, any for continuous)
            success: Whether this was a success (for Thompson Sampling)
        """
        if arm_name not in self.arms:
            raise ValueError(f"Unknown arm: {arm_name}")

        arm = self.arms[arm_name]

        # Update counts
        arm.pulls += 1
        arm.total_reward += reward
        arm.last_pulled = datetime.now().isoformat()
        arm.last_reward = reward

        self.total_pulls += 1

        # Update success/failure counts
        if success is not None:
            if success:
                arm.successes += 1
                arm.alpha += 1  # Thompson Sampling
                self.total_successes += 1
            else:
                arm.failures += 1
                arm.beta += 1   # Thompson Sampling
        elif reward > 0.5:
            # Infer success from reward
            arm.successes += 1
            arm.alpha += 1
            self.total_successes += 1
        else:
            arm.failures += 1
            arm.beta += 1

        # Record history
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "arm": arm_name,
            "reward": reward,
            "success": success,
            "total_pulls": self.total_pulls
        })

        # Persist
        if self.storage_path:
            self._save()

    def get_ranking(self) -> List[Tuple[str, float]]:
        """
        Get arms ranked by estimated value.

        Returns:
            List of (arm_name, estimated_value) sorted by value descending
        """
        if self.strategy == SelectionStrategy.THOMPSON:
            # Use mean of Beta distribution
            values = {
                name: arm.alpha / (arm.alpha + arm.beta)
                for name, arm in self.arms.items()
            }
        else:
            # Use mean reward
            values = {
                name: arm.mean_reward
                for name, arm in self.arms.items()
            }

        return sorted(values.items(), key=lambda x: x[1], reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics."""
        return {
            "strategy": self.strategy.value,
            "total_pulls": self.total_pulls,
            "total_successes": self.total_successes,
            "success_rate": self.total_successes / max(self.total_pulls, 1),
            "arms": {
                name: {
                    "pulls": arm.pulls,
                    "successes": arm.successes,
                    "success_rate": arm.success_rate,
                    "mean_reward": arm.mean_reward
                }
                for name, arm in self.arms.items()
            },
            "ranking": self.get_ranking()
        }

    def add_arm(self, name: str, prior_successes: int = 0, prior_failures: int = 0):
        """
        Add a new arm (template type).

        Args:
            name: Arm name
            prior_successes: Prior successes (for warm start)
            prior_failures: Prior failures (for warm start)
        """
        if name in self.arms:
            return

        self.arms[name] = ArmStats(
            name=name,
            successes=prior_successes,
            failures=prior_failures,
            alpha=prior_successes + 1,
            beta=prior_failures + 1,
            pulls=prior_successes + prior_failures
        )

    def _save(self):
        """Save state to disk."""
        if not self.storage_path:
            return

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        state = {
            "strategy": self.strategy.value,
            "ucb_c": self.ucb_c,
            "epsilon": self.epsilon,
            "total_pulls": self.total_pulls,
            "total_successes": self.total_successes,
            "arms": {name: arm.to_dict() for name, arm in self.arms.items()},
            "history": self.history[-1000:]  # Keep last 1000
        }

        with open(self.storage_path, "w") as f:
            json.dump(state, f, indent=2)

    def _load(self):
        """Load state from disk."""
        if not self.storage_path or not self.storage_path.exists():
            return

        with open(self.storage_path) as f:
            state = json.load(f)

        self.strategy = SelectionStrategy(state.get("strategy", "thompson"))
        self.ucb_c = state.get("ucb_c", 2.0)
        self.epsilon = state.get("epsilon", 0.1)
        self.total_pulls = state.get("total_pulls", 0)
        self.total_successes = state.get("total_successes", 0)
        self.history = state.get("history", [])

        for name, arm_data in state.get("arms", {}).items():
            self.arms[name] = ArmStats.from_dict(arm_data)


class FormulaTemplateBandit(BanditSelector):
    """
    Specialized bandit for formula template selection.

    Pre-configured with the standard formula templates used
    by FormulaGenerator.
    """

    # Standard template types
    TEMPLATE_TYPES = [
        "known_first_principles",  # Known Z² formulas
        "simple_fraction",         # a/b
        "integer_z2",              # aZ² + b
        "z_polynomial",            # aZ + b
        "z_fraction",              # a/Z² or a/Z
        "geometric",               # arccos, arctan
        "pi_based",                # π/a, a*π
        "compound"                 # Complex expressions
    ]

    # Prior knowledge about template success rates
    PRIORS = {
        "known_first_principles": (10, 0),  # Very likely if matched
        "simple_fraction": (5, 2),          # Often works
        "integer_z2": (3, 3),               # Moderate
        "z_polynomial": (2, 3),             # Less common
        "z_fraction": (1, 3),               # Rare
        "geometric": (2, 4),                # Sometimes for angles
        "pi_based": (1, 4),                 # Rare
        "compound": (1, 5)                  # Very rare
    }

    def __init__(
        self,
        strategy: SelectionStrategy = SelectionStrategy.THOMPSON,
        storage_path: Optional[Path] = None
    ):
        """Initialize with formula templates."""
        super().__init__(
            arms=self.TEMPLATE_TYPES,
            strategy=strategy,
            storage_path=storage_path
        )

        # Apply prior knowledge
        for name, (successes, failures) in self.PRIORS.items():
            if name in self.arms:
                arm = self.arms[name]
                arm.alpha = successes + 1
                arm.beta = failures + 1
                arm.successes = successes
                arm.failures = failures
                arm.pulls = successes + failures

    def select_template_order(self, n: int = 3) -> List[str]:
        """
        Select top n templates to try in order.

        Uses Thompson Sampling to get a diverse set of templates
        to try, not just the single best one.

        Args:
            n: Number of templates to select

        Returns:
            List of template names to try in order
        """
        selected = []
        samples = {}

        # Sample from each arm's posterior
        for name, arm in self.arms.items():
            samples[name] = np.random.beta(arm.alpha, arm.beta)

        # Sort by sample value and take top n
        sorted_templates = sorted(
            samples.keys(),
            key=lambda x: samples[x],
            reverse=True
        )

        return sorted_templates[:n]

    def update_from_derivation(
        self,
        template_type: str,
        derivation_level: str,
        hrm_score: float = 0.0
    ):
        """
        Update bandit from a derivation result.

        Args:
            template_type: The template type that was used
            derivation_level: Derivation level achieved (first_principles, derived, failed)
            hrm_score: HRM score (0-1)
        """
        # Calculate reward based on derivation result
        if derivation_level == "first_principles":
            reward = 1.0
            success = True
        elif derivation_level == "derived" and hrm_score > 0.7:
            reward = 0.7
            success = True
        elif derivation_level == "derived":
            reward = 0.3
            success = False
        else:
            reward = 0.0
            success = False

        self.update(template_type, reward, success)


# =============================================================================
# CONTEXTUAL BANDIT (Domain-Aware)
# =============================================================================

class ContextualTemplateBandit:
    """
    Contextual bandit that uses domain information to select templates.

    Different physics domains may have different template success rates.
    This bandit learns domain-specific template preferences.
    """

    DOMAINS = [
        "particle_physics",
        "cosmology",
        "quantum",
        "thermodynamics",
        "fluid_dynamics",
        "materials",
        "statistical_mechanics",
        "condensed_matter",
        "geometry",
        "mathematics",
        "general"
    ]

    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize with a bandit per domain."""
        self.storage_path = storage_path

        # Create a bandit for each domain
        self.domain_bandits: Dict[str, FormulaTemplateBandit] = {}
        for domain in self.DOMAINS:
            bandit_path = None
            if storage_path:
                bandit_path = storage_path / f"bandit_{domain}.json"
            self.domain_bandits[domain] = FormulaTemplateBandit(
                storage_path=bandit_path
            )

        # Global bandit for unknown domains
        global_path = storage_path / "bandit_global.json" if storage_path else None
        self.global_bandit = FormulaTemplateBandit(storage_path=global_path)

    def select(self, domain: str) -> SelectionResult:
        """Select template for a specific domain."""
        if domain in self.domain_bandits:
            return self.domain_bandits[domain].select()
        else:
            return self.global_bandit.select()

    def select_template_order(self, domain: str, n: int = 3) -> List[str]:
        """Select top n templates for a domain."""
        if domain in self.domain_bandits:
            return self.domain_bandits[domain].select_template_order(n)
        else:
            return self.global_bandit.select_template_order(n)

    def update(
        self,
        domain: str,
        template_type: str,
        derivation_level: str,
        hrm_score: float = 0.0
    ):
        """Update bandit for a domain."""
        if domain in self.domain_bandits:
            self.domain_bandits[domain].update_from_derivation(
                template_type, derivation_level, hrm_score
            )

        # Always update global too
        self.global_bandit.update_from_derivation(
            template_type, derivation_level, hrm_score
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all domains."""
        return {
            "global": self.global_bandit.get_stats(),
            "domains": {
                domain: bandit.get_stats()
                for domain, bandit in self.domain_bandits.items()
            }
        }


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MULTI-ARMED BANDIT TEMPLATE SELECTOR TEST")
    print("=" * 70)
    print()

    # Test 1: Basic Thompson Sampling
    print("Test 1: Thompson Sampling Selection")
    print("-" * 40)

    bandit = FormulaTemplateBandit(strategy=SelectionStrategy.THOMPSON)

    # Simulate 20 selections
    selections = []
    for i in range(20):
        result = bandit.select()
        selections.append(result.selected_arm)

    print(f"Selections: {selections[:10]}...")
    print(f"Distribution: {dict(zip(*np.unique(selections, return_counts=True)))}")
    print()

    # Test 2: UCB1 Selection
    print("Test 2: UCB1 Selection")
    print("-" * 40)

    bandit_ucb = FormulaTemplateBandit(strategy=SelectionStrategy.UCB1)

    # First round - should select unpulled arms
    for i in range(8):
        result = bandit_ucb.select()
        print(f"  Selection {i+1}: {result.selected_arm} (UCB: {result.ucb_value:.2f})")
        bandit_ucb.update(result.selected_arm, reward=random.random())
    print()

    # Test 3: Update from derivation
    print("Test 3: Learning from Derivations")
    print("-" * 40)

    bandit = FormulaTemplateBandit(strategy=SelectionStrategy.THOMPSON)

    # Simulate some derivation results
    results = [
        ("simple_fraction", "first_principles", 0.9),
        ("simple_fraction", "first_principles", 0.85),
        ("integer_z2", "derived", 0.75),
        ("z_polynomial", "failed", 0.2),
        ("compound", "failed", 0.1),
    ]

    for template, level, hrm in results:
        bandit.update_from_derivation(template, level, hrm)
        print(f"  Updated {template}: level={level}, hrm={hrm}")

    print()
    print("Ranking after updates:")
    for name, value in bandit.get_ranking():
        print(f"  {name}: {value:.3f}")
    print()

    # Test 4: Template order selection
    print("Test 4: Template Order Selection")
    print("-" * 40)

    order = bandit.select_template_order(n=5)
    print(f"Top 5 templates to try: {order}")
    print()

    # Test 5: Contextual Bandit
    print("Test 5: Contextual (Domain-Aware) Bandit")
    print("-" * 40)

    ctx_bandit = ContextualTemplateBandit()

    # Update for different domains
    ctx_bandit.update("particle_physics", "simple_fraction", "first_principles", 0.9)
    ctx_bandit.update("particle_physics", "simple_fraction", "first_principles", 0.85)
    ctx_bandit.update("cosmology", "integer_z2", "first_principles", 0.88)
    ctx_bandit.update("geometry", "geometric", "first_principles", 0.95)

    # Select for each domain
    for domain in ["particle_physics", "cosmology", "geometry", "general"]:
        order = ctx_bandit.select_template_order(domain, n=3)
        print(f"  {domain}: {order}")
    print()

    # Test 6: Regret simulation
    print("Test 6: Regret Comparison (1000 pulls)")
    print("-" * 40)

    # True arm values (unknown to bandit)
    true_values = {
        "known_first_principles": 0.9,
        "simple_fraction": 0.6,
        "integer_z2": 0.4,
        "z_polynomial": 0.3,
        "z_fraction": 0.2,
        "geometric": 0.35,
        "pi_based": 0.15,
        "compound": 0.1
    }

    strategies = [
        SelectionStrategy.THOMPSON,
        SelectionStrategy.UCB1,
        SelectionStrategy.EPSILON_GREEDY
    ]

    for strategy in strategies:
        bandit = FormulaTemplateBandit(strategy=strategy)
        total_reward = 0
        optimal_reward = 0

        for _ in range(1000):
            result = bandit.select()
            arm = result.selected_arm

            # Simulate reward
            true_p = true_values.get(arm, 0.1)
            reward = 1.0 if random.random() < true_p else 0.0
            bandit.update(arm, reward, reward > 0.5)

            total_reward += reward
            optimal_reward += 1.0 if random.random() < 0.9 else 0.0  # Optimal is 0.9

        regret = optimal_reward - total_reward
        print(f"  {strategy.value}: Total={total_reward:.0f}, Regret={regret:.0f}")

    print()
    print("=" * 70)
    print("BANDIT SELECTOR TEST COMPLETE")
    print("=" * 70)
