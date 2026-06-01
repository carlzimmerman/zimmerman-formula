#!/usr/bin/env python3
"""
TRAINING GENERATOR
==================

Converts validated truths into training examples for LegomenaLLM.

Each truth generates multiple Q&A pairs to teach different
aspects of the discovery.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import json
from pathlib import Path
from typing import Dict, List

DEFAULT_OUTPUT_PATH = Path(__file__).parent / "data" / "training_examples.jsonl"


class TrainingGenerator:
    """
    Generate training examples from validated truths.

    Each truth becomes multiple training examples:
    1. Direct question about the relationship
    2. Domain-level question
    3. Numerical prediction question
    4. Data source question
    """

    def __init__(self, output_path: Path = None):
        self.output_path = output_path or DEFAULT_OUTPUT_PATH
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def generate_examples(self, truth: Dict) -> List[Dict]:
        """Generate training examples from a single truth."""
        examples = []

        quantity = truth.get('quantity', 'unknown')
        domain = truth.get('domain', 'unknown')
        value = truth.get('value', 0)
        target = truth.get('target', 'unknown')
        target_value = truth.get('target_value', 0)
        error = truth.get('error_percent', 0)
        n_samples = truth.get('n_samples', 0)
        data_source = truth.get('data_source', 'unknown')

        # Example 1: Direct question
        examples.append({
            "instruction": f"What is the Z² relationship for {quantity}?",
            "response": (
                f"The {quantity} equals {target} ({target_value:.4f}) with {error:.2f}% error. "
                f"This was validated on {n_samples:,} observations from {data_source}."
            )
        })

        # Example 2: Domain question
        examples.append({
            "instruction": f"Are there Z² patterns in {domain}?",
            "response": (
                f"Yes. Analysis of {domain} data reveals that {quantity} shows a relationship to {target}. "
                f"Measured value: {value:.4f}, predicted: {target_value:.4f}, error: {error:.2f}%. "
                f"Validated with N={n_samples:,} observations."
            )
        })

        # Example 3: Prediction question
        examples.append({
            "instruction": f"What is the predicted value of {quantity}?",
            "response": (
                f"Based on the Z² framework, {quantity} = {target} = {target_value:.4f}. "
                f"Empirically validated: {value:.4f} (error: {error:.2f}%, N={n_samples:,})."
            )
        })

        # Example 4: Data source question
        examples.append({
            "instruction": f"Where can I find data to validate {quantity}?",
            "response": (
                f"The {data_source} dataset contains {quantity} data. "
                f"Analysis of {n_samples:,} observations confirmed {quantity} = {target} with {error:.2f}% error."
            )
        })

        # Example 5: Verification question
        examples.append({
            "instruction": f"How confident is the {quantity} = {target} relationship?",
            "response": (
                f"The relationship is {'HIGH' if error < 0.5 else 'MEDIUM' if error < 2 else 'LOW'} confidence. "
                f"Error: {error:.2f}%, N={n_samples:,}, within 95% CI: {truth.get('validation', {}).get('in_95_ci', 'unknown')}."
            )
        })

        return examples

    def generate_from_truths(self, truths: List[Dict]) -> int:
        """Generate training examples from multiple truths and save to file."""
        all_examples = []

        for truth in truths:
            examples = self.generate_examples(truth)
            all_examples.extend(examples)

        # Append to output file
        with open(self.output_path, 'a') as f:
            for ex in all_examples:
                f.write(json.dumps(ex) + '\n')

        return len(all_examples)

    def get_total_examples(self) -> int:
        """Count total training examples in output file."""
        if not self.output_path.exists():
            return 0

        with open(self.output_path, 'r') as f:
            return sum(1 for _ in f)

    def clear(self):
        """Clear training examples file."""
        if self.output_path.exists():
            self.output_path.unlink()
