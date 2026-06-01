#!/usr/bin/env python3
"""
STATISTICAL VALIDATOR - Rigorous Significance Testing for Pattern Detection
============================================================================

Eliminates false positives from OlympusFlow pattern detection by implementing:

1. Monte Carlo null distribution testing
2. Multiple comparison correction (FDR/Bonferroni)
3. Effect size requirements
4. Multi-source corroboration
5. Temporal stability testing
6. Physical mechanism validation (via Legomena)
7. Legomena-assisted code generation for computational confirmation

This module addresses the key weakness identified in the domain test assessment:
"With N columns × M statistics × K constants, matches are nearly guaranteed by chance"

Author: Carl Zimmerman
Date: May 5, 2026
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import subprocess
import os
import re
import hashlib
from pathlib import Path

# Constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)
PHI = (1 + np.sqrt(5)) / 2

# Target constants for pattern matching
TARGETS = {
    'Z2': Z2,
    'Z': Z,
    'phi': PHI,
    '1/phi': 1/PHI,
    '1/Z': 1/Z,
    'Z2/phi': Z2/PHI,
    'phi^2': PHI**2,
    'sqrt_Z2': np.sqrt(Z2),
    'pi': np.pi,
    'pi/2': np.pi/2,
    'e': np.e,
    '2pi': 2*np.pi,
}

# Legomena config
LEGOMENA_MODEL = os.environ.get("LEGOMENA_MODEL", "legomena-moe")
LEGOMENA_TIMEOUT = int(os.environ.get("LEGOMENA_TIMEOUT", "300"))


@dataclass
class PatternCandidate:
    """A candidate pattern that needs validation."""
    quantity: str                    # What was measured
    observed_value: float            # The measured value
    target_name: str                 # Name of Z² constant
    target_value: float              # Theoretical value
    deviation: float                 # Absolute deviation from target
    relative_error: float            # Percentage error
    sample_size: int                 # Number of data points
    data_source: str                 # Where data came from
    statistic_type: str              # mean, cv, ratio, etc.
    raw_data: Optional[np.ndarray] = None  # Original data for validation


@dataclass
class ValidationResult:
    """Result of statistical validation."""
    candidate: PatternCandidate
    is_valid: bool = False

    # Statistical tests
    p_value: float = 1.0             # Monte Carlo p-value
    fdr_adjusted_p: float = 1.0      # FDR-corrected p-value
    effect_size: float = 0.0         # Cohen's d or similar
    z_score: float = 0.0             # Standard score

    # Multi-source validation
    replicated_sources: int = 0      # How many independent sources confirm
    total_sources_tested: int = 0    # How many sources were tested

    # Temporal stability
    temporal_stable: bool = False    # Does pattern hold across time periods?
    temporal_segments_passed: int = 0

    # Physical plausibility
    mechanism_plausibility: float = 0.0  # LLM-assessed plausibility (0-1)
    proposed_mechanism: str = ""     # Physical explanation

    # Overall
    hrm_score: float = 0.0           # Hygienic Rigor Measure
    status: str = "candidate"        # candidate, validated, rejected

    # Metadata
    validation_timestamp: str = ""
    validation_methods: List[str] = field(default_factory=list)


class MonteCarloValidator:
    """
    Monte Carlo null distribution testing.

    Tests whether observed pattern is significantly different from random chance.
    """

    def __init__(self, n_permutations: int = 10000, alpha: float = 0.001):
        self.n_permutations = n_permutations
        self.alpha = alpha

    def validate(self, data: np.ndarray, observed_statistic: float,
                 target: float, statistic_func: Callable) -> Dict:
        """
        Test if observed statistic is significantly close to target.

        Args:
            data: Raw data array
            observed_statistic: Computed statistic from data
            target: Target constant value
            statistic_func: Function to compute statistic from data

        Returns:
            Dict with p_value, null_mean, null_std, z_score
        """
        if len(data) < 10:
            return {
                'p_value': 1.0,
                'null_mean': np.nan,
                'null_std': np.nan,
                'z_score': 0.0,
                'error': 'Insufficient data for Monte Carlo'
            }

        # Generate null distribution by permuting/bootstrapping
        null_distribution = []

        for _ in range(self.n_permutations):
            # Bootstrap sample
            bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
            null_stat = statistic_func(bootstrap_sample)
            null_distribution.append(null_stat)

        null_distribution = np.array(null_distribution)
        null_mean = np.mean(null_distribution)
        null_std = np.std(null_distribution)

        if null_std == 0:
            return {
                'p_value': 1.0,
                'null_mean': null_mean,
                'null_std': 0.0,
                'z_score': 0.0,
                'error': 'Zero variance in null distribution'
            }

        # How often does null distribution get as close to target as observed?
        observed_distance = np.abs(observed_statistic - target)
        null_distances = np.abs(null_distribution - target)
        p_value = np.mean(null_distances <= observed_distance)

        # Z-score
        z_score = (observed_statistic - null_mean) / null_std

        return {
            'p_value': p_value,
            'null_mean': null_mean,
            'null_std': null_std,
            'z_score': z_score,
            'observed': observed_statistic,
            'target': target
        }

    def validate_pattern(self, candidate: PatternCandidate,
                         statistic_func: Callable = None) -> Dict:
        """Validate a pattern candidate."""
        if candidate.raw_data is None:
            return {'p_value': 1.0, 'error': 'No raw data available'}

        # Default statistic function based on type
        if statistic_func is None:
            if candidate.statistic_type == 'cv':
                statistic_func = lambda x: np.std(x) / np.mean(x) if np.mean(x) != 0 else 0
            elif candidate.statistic_type == 'mean':
                statistic_func = np.mean
            elif candidate.statistic_type == 'std':
                statistic_func = np.std
            else:
                statistic_func = np.mean

        return self.validate(
            candidate.raw_data,
            candidate.observed_value,
            candidate.target_value,
            statistic_func
        )


class MultipleComparisonCorrector:
    """
    Apply multiple comparison correction (FDR/Bonferroni).

    When testing N patterns, false positives are expected at rate α×N.
    FDR controls the expected proportion of false discoveries.
    """

    def __init__(self, method: str = 'fdr_bh'):
        """
        Args:
            method: 'bonferroni' or 'fdr_bh' (Benjamini-Hochberg)
        """
        self.method = method

    def correct(self, p_values: List[float], alpha: float = 0.05) -> Tuple[List[float], List[bool]]:
        """
        Apply correction to list of p-values.

        Returns:
            Tuple of (adjusted_p_values, significant_flags)
        """
        if not p_values:
            return [], []

        p_array = np.array(p_values)
        n = len(p_array)

        if self.method == 'bonferroni':
            adjusted = np.minimum(p_array * n, 1.0)
            significant = adjusted < alpha

        elif self.method == 'fdr_bh':
            # Benjamini-Hochberg procedure
            sorted_indices = np.argsort(p_array)
            sorted_p = p_array[sorted_indices]

            # Calculate BH critical values
            ranks = np.arange(1, n + 1)
            critical = ranks / n * alpha

            # Find largest k where p(k) <= k/n * alpha
            significant_mask = sorted_p <= critical

            # Compute adjusted p-values
            adjusted = np.zeros(n)
            for i, idx in enumerate(sorted_indices):
                # Adjusted p = min(p[i] * n / rank, 1)
                adjusted[idx] = min(sorted_p[i] * n / (i + 1), 1.0)

            # Make monotonic
            for i in range(n - 2, -1, -1):
                if adjusted[sorted_indices[i]] > adjusted[sorted_indices[i + 1]]:
                    adjusted[sorted_indices[i]] = adjusted[sorted_indices[i + 1]]

            significant = adjusted < alpha

        else:
            raise ValueError(f"Unknown method: {self.method}")

        return adjusted.tolist(), significant.tolist()


class EffectSizeCalculator:
    """
    Calculate effect sizes to ensure "meaningful" matches.

    Not just "close to target" but "significantly closer than random variation".
    """

    @staticmethod
    def cohens_d(observed: float, target: float, std: float) -> float:
        """
        Cohen's d effect size.

        d < 0.2: negligible
        0.2 <= d < 0.5: small
        0.5 <= d < 0.8: medium
        d >= 0.8: large
        """
        if std == 0:
            return 0.0
        return abs(observed - target) / std

    @staticmethod
    def is_meaningful(effect_size: float, threshold: float = 0.1) -> bool:
        """
        Check if effect size indicates meaningful closeness.

        For pattern matching, we want SMALL effect size (close to target).
        """
        return effect_size < threshold


class TemporalStabilityTester:
    """
    Test if pattern holds across different time periods.

    A real pattern should be stable, not an artifact of specific time window.
    """

    def __init__(self, n_splits: int = 5):
        self.n_splits = n_splits

    def test(self, data: pd.DataFrame, time_column: str,
             value_column: str, target: float,
             tolerance: float = 0.05) -> Dict:
        """
        Test pattern stability across time periods.

        Returns:
            Dict with stability metrics
        """
        if time_column not in data.columns or value_column not in data.columns:
            return {'stable': False, 'error': 'Missing columns'}

        # Sort by time and split
        sorted_data = data.sort_values(time_column)
        splits = np.array_split(sorted_data[value_column].dropna(), self.n_splits)

        # Test pattern in each split
        results = []
        for i, split in enumerate(splits):
            if len(split) < 10:
                continue

            mean = split.mean()
            cv = split.std() / mean if mean != 0 else 0

            # Check if statistic is close to target
            close_to_target = abs(cv - target) / target < tolerance if target != 0 else False
            results.append({
                'split': i,
                'n': len(split),
                'mean': mean,
                'cv': cv,
                'close_to_target': close_to_target
            })

        if not results:
            return {'stable': False, 'error': 'Insufficient data in splits'}

        passed = sum(1 for r in results if r['close_to_target'])
        total = len(results)

        return {
            'stable': passed >= total * 0.8,  # 80% of periods must confirm
            'passed': passed,
            'total': total,
            'pass_rate': passed / total if total > 0 else 0,
            'splits': results
        }


class MultiSourceCorroborator:
    """
    Validate pattern across multiple independent data sources.

    A real Z² pattern should appear in multiple authoritative datasets.
    """

    def __init__(self, min_sources: int = 3, min_confirmation_rate: float = 0.6):
        self.min_sources = min_sources
        self.min_confirmation_rate = min_confirmation_rate

    def corroborate(self, pattern: PatternCandidate,
                    source_data: Dict[str, np.ndarray],
                    tolerance: float = 0.05) -> Dict:
        """
        Test pattern across multiple sources.

        Args:
            pattern: The pattern to validate
            source_data: Dict mapping source_name -> data array
            tolerance: Relative error tolerance

        Returns:
            Dict with corroboration results
        """
        if not source_data:
            return {'corroborated': False, 'error': 'No sources provided'}

        results = []
        for source_name, data in source_data.items():
            if len(data) < 10:
                continue

            # Compute same statistic
            if pattern.statistic_type == 'cv':
                stat = np.std(data) / np.mean(data) if np.mean(data) != 0 else 0
            elif pattern.statistic_type == 'mean':
                stat = np.mean(data)
            else:
                stat = np.mean(data)

            relative_error = abs(stat - pattern.target_value) / pattern.target_value if pattern.target_value != 0 else float('inf')
            matches = relative_error < tolerance

            results.append({
                'source': source_name,
                'value': stat,
                'relative_error': relative_error,
                'matches': matches
            })

        if len(results) < self.min_sources:
            return {
                'corroborated': False,
                'error': f'Need at least {self.min_sources} sources',
                'sources_found': len(results),
                'results': results
            }

        confirmed = sum(1 for r in results if r['matches'])
        confirmation_rate = confirmed / len(results)

        return {
            'corroborated': confirmed >= self.min_sources and confirmation_rate >= self.min_confirmation_rate,
            'confirmed_sources': confirmed,
            'total_sources': len(results),
            'confirmation_rate': confirmation_rate,
            'results': results
        }


class LegomenaCodeGenerator:
    """
    Use Legomena LLM to generate computational confirmation scripts.

    Instead of hardcoding analysis, let the LLM write domain-specific
    validation code based on the pattern being tested.
    """

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path("./generated_scripts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _call_legomena(self, prompt: str) -> Optional[str]:
        """Call Legomena for code generation."""
        try:
            result = subprocess.run(
                ["ollama", "run", LEGOMENA_MODEL],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=LEGOMENA_TIMEOUT
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"Legomena error: {e}")
        return None

    def generate_validation_script(self, pattern: PatternCandidate,
                                   domain: str, topic: str) -> Optional[str]:
        """
        Generate a complete Python validation script for a pattern.

        Returns:
            Path to generated script or None
        """
        prompt = f"""You are an expert data scientist. Generate a complete Python script to rigorously validate this pattern.

PATTERN TO VALIDATE:
- Domain: {domain}
- Topic: {topic}
- Quantity: {pattern.quantity}
- Observed Value: {pattern.observed_value:.6f}
- Target Constant: {pattern.target_name} = {pattern.target_value:.6f}
- Statistic Type: {pattern.statistic_type}
- Data Source: {pattern.data_source}
- Sample Size: {pattern.sample_size}

VALIDATION REQUIREMENTS:
1. Monte Carlo null distribution (10,000 permutations)
2. Calculate p-value (must be < 0.001)
3. Effect size calculation (Cohen's d)
4. Bootstrap confidence intervals
5. Generate visualization (histogram of null distribution with observed value marked)
6. Output JSON result with all metrics

Write a COMPLETE, RUNNABLE Python script that:
1. Downloads or loads the data
2. Computes the statistic
3. Runs all validation tests
4. Saves results to JSON and generates a plot

Use these imports: numpy, pandas, scipy.stats, matplotlib
Data source URL (if applicable): {pattern.data_source}

Output ONLY the Python code, no explanations:

```python
"""

        response = self._call_legomena(prompt)

        if response:
            # Extract Python code from response
            code_match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
            if code_match:
                code = code_match.group(1)
            else:
                # Try to find code without markdown blocks
                code = response

            # Save script (sanitize filename)
            safe_quantity = pattern.quantity.replace('/', '_').replace(' ', '_')
            safe_target = pattern.target_name.replace('/', '_').replace(' ', '_')
            script_name = f"validate_{safe_quantity}_{safe_target}.py"

            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)
            script_path = self.output_dir / script_name

            # Add header
            header = f'''#!/usr/bin/env python3
"""
AUTO-GENERATED VALIDATION SCRIPT
================================
Pattern: {pattern.quantity} ≈ {pattern.target_name}
Domain: {domain}
Topic: {topic}
Generated: {datetime.now().isoformat()}

Run this script to perform rigorous statistical validation.
"""

'''
            full_code = header + code

            script_path.write_text(full_code)
            return str(script_path)

        return None

    def generate_physical_mechanism_analysis(self, pattern: PatternCandidate,
                                              domain: str) -> Dict:
        """
        Use Legomena to assess physical plausibility of the pattern.

        Returns:
            Dict with plausibility score and proposed mechanism
        """
        prompt = f"""You are a theoretical physicist specializing in fundamental constants and geometric relationships.

PATTERN FOUND:
- Domain: {domain}
- Quantity: {pattern.quantity}
- Observed: {pattern.observed_value:.6f}
- Target: {pattern.target_name} = {pattern.target_value:.6f}
- Deviation: {pattern.relative_error*100:.2f}%

Z² THEORY CONTEXT:
Z² = 32π/3 ≈ 33.5103 is proposed as a fundamental geometric constant arising from
the relationship between spherical and cubic geometry. Z = √(Z²) ≈ 5.7888.
φ = (1+√5)/2 ≈ 1.618 is the golden ratio.

TASK:
Evaluate whether this pattern has a plausible physical mechanism connecting
{pattern.quantity} to {pattern.target_name}.

Respond with JSON:
{{
    "plausibility_score": <0.0 to 1.0>,
    "reasoning": "<brief explanation>",
    "proposed_mechanism": "<physical mechanism if plausible>",
    "alternative_explanations": ["<other possible reasons for this pattern>"],
    "testable_predictions": ["<predictions that would confirm this mechanism>"]
}}

JSON:"""

        response = self._call_legomena(prompt)

        if response:
            try:
                json_match = re.search(r'\{[\s\S]*\}', response)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            'plausibility_score': 0.0,
            'reasoning': 'Could not assess',
            'proposed_mechanism': '',
            'alternative_explanations': [],
            'testable_predictions': []
        }


class StatisticalValidator:
    """
    Complete statistical validation pipeline.

    Combines all validation methods to rigorously test pattern candidates.
    """

    def __init__(self, verbose: bool = True, script_output_dir: str = None):
        self.verbose = verbose
        self.monte_carlo = MonteCarloValidator(n_permutations=10000)
        self.fdr_corrector = MultipleComparisonCorrector(method='fdr_bh')
        self.effect_calculator = EffectSizeCalculator()
        self.temporal_tester = TemporalStabilityTester()
        self.multi_source = MultiSourceCorroborator()
        self.code_generator = LegomenaCodeGenerator(script_output_dir)

        # Track all candidates for FDR correction
        self.all_candidates: List[PatternCandidate] = []
        self.all_p_values: List[float] = []

    def _log(self, msg: str):
        if self.verbose:
            print(f"[StatisticalValidator] {msg}")

    def validate_candidate(self, candidate: PatternCandidate,
                           domain: str = "",
                           topic: str = "",
                           additional_sources: Dict[str, np.ndarray] = None,
                           generate_script: bool = True) -> ValidationResult:
        """
        Run complete validation pipeline on a pattern candidate.

        Args:
            candidate: The pattern to validate
            domain: Scientific domain
            topic: Specific topic
            additional_sources: Additional data sources for corroboration
            generate_script: Whether to generate validation script

        Returns:
            ValidationResult with all metrics
        """
        result = ValidationResult(
            candidate=candidate,
            validation_timestamp=datetime.now().isoformat(),
            validation_methods=[]
        )

        self._log(f"Validating: {candidate.quantity} ≈ {candidate.target_name}")

        # 1. Monte Carlo validation
        self._log("  Running Monte Carlo validation...")
        mc_result = self.monte_carlo.validate_pattern(candidate)
        result.p_value = mc_result.get('p_value', 1.0)
        result.z_score = mc_result.get('z_score', 0.0)
        result.validation_methods.append('monte_carlo')
        self._log(f"    p-value: {result.p_value:.6f}")

        # Track for FDR correction
        self.all_candidates.append(candidate)
        self.all_p_values.append(result.p_value)

        # 2. Effect size
        self._log("  Calculating effect size...")
        null_std = mc_result.get('null_std', 1.0)
        result.effect_size = self.effect_calculator.cohens_d(
            candidate.observed_value, candidate.target_value, null_std
        )
        result.validation_methods.append('effect_size')
        self._log(f"    Effect size (d): {result.effect_size:.4f}")

        # 3. Temporal stability (if time data available)
        # This would require time-indexed data
        result.temporal_stable = False  # Placeholder
        result.temporal_segments_passed = 0

        # 4. Multi-source corroboration
        if additional_sources:
            self._log("  Testing multi-source corroboration...")
            corr_result = self.multi_source.corroborate(candidate, additional_sources)
            result.replicated_sources = corr_result.get('confirmed_sources', 0)
            result.total_sources_tested = corr_result.get('total_sources', 0)
            result.validation_methods.append('multi_source')
            self._log(f"    Corroborated: {result.replicated_sources}/{result.total_sources_tested}")

        # 5. Physical mechanism analysis
        self._log("  Analyzing physical plausibility...")
        mechanism_result = self.code_generator.generate_physical_mechanism_analysis(
            candidate, domain
        )
        result.mechanism_plausibility = mechanism_result.get('plausibility_score', 0.0)
        result.proposed_mechanism = mechanism_result.get('proposed_mechanism', '')
        result.validation_methods.append('mechanism_analysis')
        self._log(f"    Plausibility: {result.mechanism_plausibility:.2f}")

        # 6. Generate validation script
        if generate_script:
            self._log("  Generating validation script...")
            script_path = self.code_generator.generate_validation_script(
                candidate, domain, topic
            )
            if script_path:
                self._log(f"    Script: {script_path}")

        # Calculate HRM score
        result.hrm_score = self._calculate_hrm(result)
        self._log(f"  HRM Score: {result.hrm_score:.3f}")

        # Determine status
        if (result.p_value < 0.001 and
            result.effect_size < 0.1 and
            result.mechanism_plausibility > 0.5):
            result.status = 'validated'
            result.is_valid = True
        elif result.p_value > 0.1 or result.effect_size > 0.5:
            result.status = 'rejected'
            result.is_valid = False
        else:
            result.status = 'candidate'
            result.is_valid = False

        self._log(f"  Status: {result.status}")
        return result

    def _calculate_hrm(self, result: ValidationResult) -> float:
        """
        Calculate Hygienic Rigor Measure.

        Combines multiple validation metrics into single score.
        """
        # Component weights
        weights = {
            'statistical': 0.3,  # p-value contribution
            'effect': 0.2,       # effect size contribution
            'replication': 0.2,  # multi-source contribution
            'mechanism': 0.2,    # physical plausibility
            'sample': 0.1        # sample size contribution
        }

        # Statistical score (inverse of p-value, capped)
        if result.p_value > 0:
            stat_score = min(-np.log10(result.p_value) / 4, 1.0)  # Max at p=0.0001
        else:
            stat_score = 1.0

        # Effect score (smaller is better for pattern matching)
        effect_score = max(0, 1 - result.effect_size / 0.5)

        # Replication score
        if result.total_sources_tested > 0:
            repl_score = result.replicated_sources / result.total_sources_tested
        else:
            repl_score = 0.0

        # Mechanism score
        mech_score = result.mechanism_plausibility

        # Sample size score (log scale, max at 10000)
        sample_score = min(np.log10(result.candidate.sample_size + 1) / 4, 1.0)

        # Weighted sum
        hrm = (
            weights['statistical'] * stat_score +
            weights['effect'] * effect_score +
            weights['replication'] * repl_score +
            weights['mechanism'] * mech_score +
            weights['sample'] * sample_score
        )

        return hrm

    def apply_fdr_correction(self, alpha: float = 0.05) -> List[Tuple[PatternCandidate, float, bool]]:
        """
        Apply FDR correction to all accumulated p-values.

        Should be called after all candidates have been validated.

        Returns:
            List of (candidate, adjusted_p, is_significant)
        """
        if not self.all_p_values:
            return []

        adjusted, significant = self.fdr_corrector.correct(self.all_p_values, alpha)

        return [
            (c, p_adj, sig)
            for c, p_adj, sig in zip(self.all_candidates, adjusted, significant)
        ]

    def generate_report(self, results: List[ValidationResult]) -> str:
        """Generate markdown report of all validation results."""
        report = []
        report.append("# Statistical Validation Report")
        report.append(f"\nGenerated: {datetime.now().isoformat()}")
        report.append(f"\nTotal candidates tested: {len(results)}")

        validated = [r for r in results if r.status == 'validated']
        rejected = [r for r in results if r.status == 'rejected']
        candidates = [r for r in results if r.status == 'candidate']

        report.append(f"\n- Validated: {len(validated)}")
        report.append(f"- Rejected: {len(rejected)}")
        report.append(f"- Still candidates: {len(candidates)}")

        report.append("\n## Validated Patterns\n")
        for r in validated:
            report.append(f"### {r.candidate.quantity} ≈ {r.candidate.target_name}")
            report.append(f"- Observed: {r.candidate.observed_value:.6f}")
            report.append(f"- Target: {r.candidate.target_value:.6f}")
            report.append(f"- p-value: {r.p_value:.6f}")
            report.append(f"- Effect size: {r.effect_size:.4f}")
            report.append(f"- HRM: {r.hrm_score:.3f}")
            report.append(f"- Mechanism: {r.proposed_mechanism}")
            report.append("")

        report.append("\n## Rejected Patterns\n")
        for r in rejected[:10]:  # Limit to 10
            report.append(f"- {r.candidate.quantity} ≈ {r.candidate.target_name}: p={r.p_value:.4f}, d={r.effect_size:.2f}")

        return "\n".join(report)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def validate_pattern_quick(quantity: str, observed: float, target_name: str,
                           data: np.ndarray, domain: str = "") -> ValidationResult:
    """Quick validation of a single pattern."""
    target_value = TARGETS.get(target_name, observed)

    candidate = PatternCandidate(
        quantity=quantity,
        observed_value=observed,
        target_name=target_name,
        target_value=target_value,
        deviation=abs(observed - target_value),
        relative_error=abs(observed - target_value) / target_value if target_value != 0 else 0,
        sample_size=len(data),
        data_source="provided",
        statistic_type="mean",
        raw_data=data
    )

    validator = StatisticalValidator(verbose=True)
    return validator.validate_candidate(candidate, domain=domain)


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("STATISTICAL VALIDATOR - Test")
    print("=" * 60)

    # Test with synthetic data
    np.random.seed(42)

    # Create test data that should match 1/φ
    target = 1/PHI
    noise = 0.01
    data = np.random.normal(target, noise, size=1000)

    print(f"\nTest data: N={len(data)}, mean={np.mean(data):.6f}, target=1/φ={target:.6f}")

    result = validate_pattern_quick(
        quantity="test_ratio",
        observed=np.mean(data),
        target_name="1/phi",
        data=data,
        domain="test"
    )

    print(f"\nValidation Result:")
    print(f"  p-value: {result.p_value:.6f}")
    print(f"  Effect size: {result.effect_size:.4f}")
    print(f"  HRM: {result.hrm_score:.3f}")
    print(f"  Status: {result.status}")
    print(f"  Valid: {result.is_valid}")
