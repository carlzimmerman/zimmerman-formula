#!/usr/bin/env python3
"""
M4 Biological Pattern Discovery Framework
==========================================

Systematically discovers and validates statistical patterns in biology,
similar to how Z² = 8 contacts was discovered from the 8D manifold theory.

METHODOLOGY:
1. Generate hypotheses from theoretical framework
2. Test against real biological data
3. Calculate statistical significance (p-values, effect sizes)
4. Register validated patterns in pattern registry

PATTERN CATEGORIES:
- Structural patterns (contacts, geometry)
- Sequence patterns (motifs, conservation)
- Network patterns (interactions, pathways)
- Energetic patterns (binding, folding)

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
import hashlib
import math
import numpy as np
from scipy import stats


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple, Any
import random


@dataclass
class BiologicalPattern:
    """A discovered and validated biological pattern."""
    pattern_id: str
    name: str
    category: str  # structural, sequence, network, energetic
    description: str
    hypothesis: str
    test_data_source: str
    sample_size: int
    observed_value: float
    expected_value: float
    p_value: float
    effect_size: float
    is_significant: bool  # p < 0.05
    is_highly_significant: bool  # p < 0.001
    validation_method: str
    confidence_interval: Tuple[float, float]
    discovered_date: str
    sha256: str
    notes: List[str] = field(default_factory=list)


class PatternRegistry:
    """Registry of validated biological patterns."""

    def __init__(self, registry_path: str = None):
        self.registry_path = registry_path or Path(__file__).parent / "pattern_registry.json"
        self.patterns: Dict[str, BiologicalPattern] = {}
        self._load()

    def _load(self):
        """Load existing patterns from registry."""
        if Path(self.registry_path).exists():
            with open(self.registry_path) as f:
                data = json.load(f)
                for p in data.get("patterns", []):
                    pattern = BiologicalPattern(**p)
                    self.patterns[pattern.pattern_id] = pattern

    def _save(self):
        """Save patterns to registry."""
        output = {
            "last_updated": datetime.now().isoformat(),
            "total_patterns": len(self.patterns),
            "significant_patterns": sum(1 for p in self.patterns.values() if p.is_significant),
            "patterns": [asdict(p) for p in self.patterns.values()],
        }
        with open(self.registry_path, "w") as f:
            json.dump(output, f, indent=2, cls=NumpyEncoder)

    def register(self, pattern: BiologicalPattern):
        """Register a validated pattern."""
        self.patterns[pattern.pattern_id] = pattern
        self._save()
        return pattern

    def get_significant(self) -> List[BiologicalPattern]:
        """Get all statistically significant patterns."""
        return [p for p in self.patterns.values() if p.is_significant]


class PatternDiscoveryEngine:
    """Engine for discovering and validating biological patterns."""

    def __init__(self):
        self.registry = PatternRegistry()

    def test_pattern(
        self,
        name: str,
        category: str,
        description: str,
        hypothesis: str,
        observed_data: np.ndarray,
        expected_distribution: str = "normal",
        expected_params: Dict = None,
        test_type: str = "one_sample_t",
    ) -> BiologicalPattern:
        """
        Test a hypothesized pattern against observed data.

        Parameters:
        - observed_data: numpy array of observed values
        - expected_distribution: "normal", "poisson", "binomial"
        - expected_params: {"mean": x, "std": y} or {"lambda": x} etc.
        - test_type: "one_sample_t", "chi_square", "ks_test"
        """
        observed_mean = np.mean(observed_data)
        observed_std = np.std(observed_data)
        n = len(observed_data)

        expected_params = expected_params or {}

        # Perform statistical test
        if test_type == "one_sample_t":
            expected_mean = expected_params.get("mean", 0)
            t_stat, p_value = stats.ttest_1samp(observed_data, expected_mean)
            effect_size = (observed_mean - expected_mean) / observed_std  # Cohen's d
            expected_value = expected_mean

        elif test_type == "chi_square":
            expected_counts = expected_params.get("expected", None)
            if expected_counts is None:
                expected_counts = np.ones_like(observed_data) * np.mean(observed_data)
            chi2, p_value = stats.chisquare(observed_data, expected_counts)
            effect_size = np.sqrt(chi2 / n)  # Cramér's V approximation
            expected_value = np.mean(expected_counts)

        elif test_type == "ks_test":
            # Kolmogorov-Smirnov test against expected distribution
            if expected_distribution == "normal":
                expected_mean = expected_params.get("mean", 0)
                expected_std = expected_params.get("std", 1)
                ks_stat, p_value = stats.kstest(
                    observed_data, "norm", args=(expected_mean, expected_std)
                )
            elif expected_distribution == "poisson":
                expected_lambda = expected_params.get("lambda", 1)
                ks_stat, p_value = stats.kstest(
                    observed_data, "poisson", args=(expected_lambda,)
                )
            else:
                ks_stat, p_value = 0.5, 1.0  # Default
            effect_size = ks_stat
            expected_value = expected_params.get("mean", expected_params.get("lambda", 0))

        elif test_type == "binomial":
            successes = int(np.sum(observed_data > 0))
            expected_p = expected_params.get("p", 0.5)
            result = stats.binomtest(successes, n, expected_p)
            p_value = result.pvalue
            effect_size = (successes / n - expected_p) / np.sqrt(expected_p * (1 - expected_p) / n)
            expected_value = expected_p

        else:
            raise ValueError(f"Unknown test type: {test_type}")

        # Confidence interval
        se = observed_std / np.sqrt(n)
        ci = (observed_mean - 1.96 * se, observed_mean + 1.96 * se)

        # Significance assessment
        is_sig = p_value < 0.05
        is_highly_sig = p_value < 0.001

        # Create pattern
        pattern_id = f"BIO_{category.upper()}_{hashlib.sha256(name.encode()).hexdigest()[:8]}"

        pattern = BiologicalPattern(
            pattern_id=pattern_id,
            name=name,
            category=category,
            description=description,
            hypothesis=hypothesis,
            test_data_source="computational_analysis",
            sample_size=n,
            observed_value=round(float(observed_mean), 6),
            expected_value=round(float(expected_value), 6),
            p_value=float(p_value),
            effect_size=round(float(effect_size), 4),
            is_significant=is_sig,
            is_highly_significant=is_highly_sig,
            validation_method=test_type,
            confidence_interval=(round(ci[0], 6), round(ci[1], 6)),
            discovered_date=datetime.now().isoformat(),
            sha256=hashlib.sha256(f"{name}{observed_mean}{p_value}".encode()).hexdigest()[:16],
            notes=[],
        )

        # Auto-register if significant
        if is_sig:
            pattern.notes.append("AUTO-REGISTERED: Statistically significant")
            self.registry.register(pattern)

        return pattern

    def discover_amino_acid_patterns(self, sequences: List[str]) -> List[BiologicalPattern]:
        """Discover patterns in amino acid composition."""
        patterns = []

        # Pattern 1: Hydrophobic residue frequency
        hydrophobic = "AILMFWVY"
        freqs = []
        for seq in sequences:
            freq = sum(1 for aa in seq if aa in hydrophobic) / len(seq)
            freqs.append(freq)

        pattern = self.test_pattern(
            name="Hydrophobic residue frequency",
            category="sequence",
            description="Fraction of hydrophobic amino acids in peptide sequences",
            hypothesis="Hydrophobic content differs from random expectation (8/20 = 0.4)",
            observed_data=np.array(freqs),
            expected_params={"mean": 0.4},
            test_type="one_sample_t",
        )
        patterns.append(pattern)

        # Pattern 2: Charged residue balance
        for seq in sequences:
            positive = sum(1 for aa in seq if aa in "RK")
            negative = sum(1 for aa in seq if aa in "DE")
            # Net charge bias

        pos_counts = [sum(1 for aa in seq if aa in "RK") for seq in sequences]
        neg_counts = [sum(1 for aa in seq if aa in "DE") for seq in sequences]
        charge_balance = np.array(pos_counts) - np.array(neg_counts)

        pattern = self.test_pattern(
            name="Charge balance",
            category="sequence",
            description="Net charge (positive - negative residues)",
            hypothesis="Net charge is balanced (expected mean = 0)",
            observed_data=charge_balance,
            expected_params={"mean": 0},
            test_type="one_sample_t",
        )
        patterns.append(pattern)

        # Pattern 3: Cysteine pairing
        cys_counts = [seq.count("C") for seq in sequences]
        even_cys = [1 if c % 2 == 0 else 0 for c in cys_counts if c > 0]

        if even_cys:
            pattern = self.test_pattern(
                name="Cysteine pairing preference",
                category="structural",
                description="Preference for even number of cysteines (for disulfide bonds)",
                hypothesis="Cysteines occur in pairs more than expected by chance",
                observed_data=np.array(even_cys),
                expected_params={"p": 0.5},
                test_type="binomial",
            )
            patterns.append(pattern)

        # Pattern 4: Aromatic clustering
        aromatic = "FYW"
        clustering_scores = []
        for seq in sequences:
            positions = [i for i, aa in enumerate(seq) if aa in aromatic]
            if len(positions) >= 2:
                # Average distance between consecutive aromatics
                dists = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
                clustering_scores.append(np.mean(dists))

        if clustering_scores:
            # Expected average distance for random distribution
            avg_len = np.mean([len(s) for s in sequences])
            avg_aromatic = np.mean([sum(1 for aa in s if aa in aromatic) for s in sequences])
            expected_dist = avg_len / (avg_aromatic + 1) if avg_aromatic > 0 else avg_len

            pattern = self.test_pattern(
                name="Aromatic residue clustering",
                category="structural",
                description="Average distance between consecutive aromatic residues",
                hypothesis="Aromatic residues cluster together (distance < random expectation)",
                observed_data=np.array(clustering_scores),
                expected_params={"mean": expected_dist},
                test_type="one_sample_t",
            )
            patterns.append(pattern)

        return patterns

    def discover_length_patterns(self, sequences: List[str]) -> List[BiologicalPattern]:
        """Discover patterns in sequence lengths."""
        patterns = []

        lengths = np.array([len(s) for s in sequences])

        # Pattern: Length distribution
        pattern = self.test_pattern(
            name="Sequence length distribution",
            category="sequence",
            description="Distribution of peptide sequence lengths",
            hypothesis="Length follows normal distribution",
            observed_data=lengths,
            expected_distribution="normal",
            expected_params={"mean": np.mean(lengths), "std": np.std(lengths)},
            test_type="ks_test",
        )
        patterns.append(pattern)

        return patterns

    def discover_contact_patterns(self, contact_data: Dict[str, int]) -> List[BiologicalPattern]:
        """
        Discover patterns in protein contacts (like Z² = 8).

        contact_data: {"protein_id": contact_count, ...}
        """
        patterns = []

        contacts = np.array(list(contact_data.values()))

        # Test Z² = 8 prediction
        pattern = self.test_pattern(
            name="Z² contact number",
            category="structural",
            description="Number of contacts per residue in folded proteins",
            hypothesis="Z² = 8 contacts predicted from 8D manifold theory",
            observed_data=contacts,
            expected_params={"mean": 8.0},
            test_type="one_sample_t",
        )
        pattern.notes.append("Core prediction from Zimmerman 8D manifold framework")
        patterns.append(pattern)

        return patterns


def run_pattern_discovery_on_peptides():
    """Run pattern discovery on all generated peptides."""
    print("=" * 70)
    print("M4 BIOLOGICAL PATTERN DISCOVERY")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    engine = PatternDiscoveryEngine()

    # Collect all sequences from FASTA files
    base_dir = Path(__file__).parent.parent
    fasta_files = list(base_dir.glob("**/*.fasta"))

    all_sequences = []

    for fasta_path in fasta_files:
        if "peptide" in fasta_path.name.lower() or "binder" in fasta_path.name.lower():
            current_seq = []
            with open(fasta_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(">"):
                        if current_seq:
                            all_sequences.append("".join(current_seq))
                        current_seq = []
                    else:
                        current_seq.append(line)
                if current_seq:
                    all_sequences.append("".join(current_seq))

    print(f"Loaded {len(all_sequences)} peptide sequences from {len(fasta_files)} files")
    print()

    # Discover patterns
    print("DISCOVERING AMINO ACID PATTERNS...")
    aa_patterns = engine.discover_amino_acid_patterns(all_sequences)

    print("\nDISCOVERING LENGTH PATTERNS...")
    length_patterns = engine.discover_length_patterns(all_sequences)

    # Combine all patterns
    all_patterns = aa_patterns + length_patterns

    # Report
    print("\n" + "=" * 70)
    print("DISCOVERED PATTERNS")
    print("=" * 70)

    significant = []
    for pattern in all_patterns:
        sig_str = "***" if pattern.is_highly_significant else ("*" if pattern.is_significant else "")
        print(f"\n{pattern.name} {sig_str}")
        print(f"  Category: {pattern.category}")
        print(f"  Observed: {pattern.observed_value:.4f}")
        print(f"  Expected: {pattern.expected_value:.4f}")
        print(f"  p-value: {pattern.p_value:.2e}")
        print(f"  Effect size: {pattern.effect_size:.3f}")
        print(f"  95% CI: [{pattern.confidence_interval[0]:.4f}, {pattern.confidence_interval[1]:.4f}]")

        if pattern.is_significant:
            significant.append(pattern)
            print(f"  → SIGNIFICANT: Registered in pattern registry")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total patterns tested: {len(all_patterns)}")
    print(f"Significant (p < 0.05): {len(significant)}")
    print(f"Highly significant (p < 0.001): {sum(1 for p in all_patterns if p.is_highly_significant)}")

    print(f"\nPattern registry: {engine.registry.registry_path}")
    print(f"Total registered patterns: {len(engine.registry.patterns)}")

    return all_patterns


if __name__ == "__main__":
    run_pattern_discovery_on_peptides()
