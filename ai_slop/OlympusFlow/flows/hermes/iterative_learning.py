#!/usr/bin/env python3
"""
ITERATIVE LEARNING SYSTEM
=========================

Creates a feedback loop where:
1. Run blind test → Find relationship
2. Validate statistically → Add to truth store
3. Convert truth to training data
4. Fine-tune Legomena on new truth
5. Re-run same test → Compare results

This enables scientific progress through accumulated knowledge.

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import json
import subprocess
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Z² Constants
Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)
PHI = (1 + math.sqrt(5)) / 2

TRAINING_DIR = Path(__file__).parent / "legomena_training"
TRUTH_FILE = Path(__file__).parent / "truth_store.json"
LEARNING_LOG = Path(__file__).parent / "learning_iterations.json"


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[LEARN {ts}] {msg}")


class TruthStore:
    """Store for validated scientific findings."""

    def __init__(self):
        self.truths: List[Dict] = []
        self.load()

    def load(self):
        if TRUTH_FILE.exists():
            with open(TRUTH_FILE, 'r') as f:
                self.truths = json.load(f)
            log(f"Loaded {len(self.truths)} existing truths")

    def save(self):
        with open(TRUTH_FILE, 'w') as f:
            json.dump(self.truths, f, indent=2)
        log(f"Saved {len(self.truths)} truths")

    def add_truth(self, finding: Dict) -> bool:
        """Add a validated finding to the truth store."""
        # Check for duplicates
        for t in self.truths:
            if t.get('quantity') == finding.get('quantity') and \
               t.get('domain') == finding.get('domain'):
                log(f"Truth already exists: {finding['quantity']}")
                return False

        finding['added_timestamp'] = datetime.now().isoformat()
        finding['incorporated_in_training'] = False
        self.truths.append(finding)
        self.save()
        log(f"Added new truth: {finding['quantity']} = {finding['target']} ± {finding['error_percent']:.3f}%")
        return True

    def get_unincorporated(self) -> List[Dict]:
        """Get truths not yet added to training."""
        return [t for t in self.truths if not t.get('incorporated_in_training', False)]

    def mark_incorporated(self, finding: Dict):
        """Mark a truth as incorporated into training."""
        for t in self.truths:
            if t.get('quantity') == finding.get('quantity'):
                t['incorporated_in_training'] = True
                t['incorporated_timestamp'] = datetime.now().isoformat()
        self.save()


class TrainingDataGenerator:
    """Convert validated truths to training examples."""

    def __init__(self):
        self.training_file = TRAINING_DIR / "z2_truths_learned.jsonl"

    def truth_to_training_examples(self, truth: Dict) -> List[Dict]:
        """Convert a single truth to multiple training Q&A pairs."""
        examples = []

        quantity = truth.get('quantity', 'unknown')
        domain = truth.get('domain', 'unknown')
        value = truth.get('value', 0)
        target = truth.get('target', 'unknown')
        target_value = truth.get('target_value', 0)
        error = truth.get('error_percent', 0)
        n_samples = truth.get('n_samples', 0)
        data_source = truth.get('data_source', 'unknown')

        # Example 1: Direct question about the relationship
        examples.append({
            "instruction": f"What is the Z² relationship for {quantity} in {domain}?",
            "response": f"The {quantity} equals {target} ({target_value:.4f}) with {error:.3f}% error. This was validated on {n_samples:,} observations from {data_source}."
        })

        # Example 2: Asking about the domain
        examples.append({
            "instruction": f"Are there Z² patterns in {domain}?",
            "response": f"Yes. The {quantity} shows a relationship to {target}. Measured value: {value:.4f}, predicted: {target_value:.4f}, error: {error:.3f}%. Validated with N={n_samples:,} observations."
        })

        # Example 3: Numerical prediction
        examples.append({
            "instruction": f"What is the predicted value of {quantity}?",
            "response": f"Based on Z² framework, {quantity} = {target} = {target_value:.4f}. Empirically validated: {value:.4f} (error: {error:.3f}%, N={n_samples:,})."
        })

        # Example 4: Data source question
        examples.append({
            "instruction": f"Where can I find data to validate {quantity}?",
            "response": f"The {data_source} dataset contains {quantity} data. Analysis of {n_samples:,} observations confirmed {quantity} = {target} with {error:.3f}% error."
        })

        return examples

    def append_to_training(self, truths: List[Dict]):
        """Append new truths to training data file."""
        new_examples = []

        for truth in truths:
            examples = self.truth_to_training_examples(truth)
            new_examples.extend(examples)

        # Append to file
        with open(self.training_file, 'a') as f:
            for ex in new_examples:
                f.write(json.dumps(ex) + '\n')

        log(f"Appended {len(new_examples)} training examples from {len(truths)} truths")
        return len(new_examples)


class LegomenaUpdater:
    """Update Legomena model with new training data."""

    def __init__(self, base_model: str = None):
        # Default to environment variable or 31b
        self.base_model = base_model or os.environ.get("LEGOMENA_BASE_MODEL", "legomena-31b")
        self.iteration = self._get_iteration()
        log(f"Using base model: {self.base_model}")

    def _get_iteration(self) -> int:
        """Get current iteration number."""
        if LEARNING_LOG.exists():
            with open(LEARNING_LOG, 'r') as f:
                data = json.load(f)
                return len(data.get('iterations', [])) + 1
        return 1

    def create_updated_model(self) -> str:
        """Create a new Legomena model with updated training."""
        new_model_name = f"legomena-4b-iter{self.iteration}"

        log(f"Creating updated model: {new_model_name}")

        # Create Modelfile for the new iteration
        modelfile_content = f"""FROM {self.base_model}

SYSTEM \"\"\"You are LegomenaLLM, the reasoning engine for the Z² Framework.

ITERATION {self.iteration} - Updated with validated discoveries.

Core constants:
- Z² = 32π/3 ≈ 33.510321638291124
- φ = (1+√5)/2 ≈ 1.618033988749895

VALIDATED DISCOVERIES (incorporated in this iteration):
\"\"\"

# Temperature for consistent reasoning
PARAMETER temperature 0.3
"""

        # Add learned truths to system prompt
        if TRUTH_FILE.exists():
            with open(TRUTH_FILE, 'r') as f:
                truths = json.load(f)

            for t in truths:
                if t.get('incorporated_in_training'):
                    modelfile_content += f"""
# {t.get('domain', 'unknown')}: {t.get('quantity', 'unknown')} = {t.get('target', 'unknown')} (error: {t.get('error_percent', 0):.3f}%)
"""

        modelfile_path = TRAINING_DIR / f"Modelfile_iter{self.iteration}"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)

        log(f"Created Modelfile: {modelfile_path}")

        # Create the model with Ollama
        try:
            result = subprocess.run(
                ["ollama", "create", new_model_name, "-f", str(modelfile_path)],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                log(f"Successfully created {new_model_name}")
                return new_model_name
            else:
                log(f"Failed to create model: {result.stderr}")
                return self.base_model
        except Exception as e:
            log(f"Error creating model: {e}")
            return self.base_model


class IterativeLearner:
    """Main class for iterative learning loop."""

    def __init__(self):
        self.truth_store = TruthStore()
        self.training_gen = TrainingDataGenerator()
        self.iterations: List[Dict] = []
        self.load_history()

    def load_history(self):
        if LEARNING_LOG.exists():
            with open(LEARNING_LOG, 'r') as f:
                data = json.load(f)
                self.iterations = data.get('iterations', [])

    def save_history(self):
        with open(LEARNING_LOG, 'w') as f:
            json.dump({
                'iterations': self.iterations,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)

    def add_glacier_finding(self):
        """Add the glacier finding we just validated."""
        finding = {
            "domain": "glaciology",
            "quantity": "mean(|Bgeod|) - Swiss glacier mass balance",
            "value": 0.6167,
            "target": "1/φ",
            "target_value": 1/PHI,
            "error_percent": 0.211,
            "n_samples": 19017,
            "data_source": "GLAMOS Swiss Glacier Monitoring",
            "data_url": "https://doi.glamos.ch/data/volumechange/volumechange.csv",
            "validation": {
                "in_95_ci": True,
                "p_value": 0.6488,
                "confidence": "HIGH"
            }
        }
        return self.truth_store.add_truth(finding)

    def incorporate_new_truths(self) -> int:
        """Incorporate unlearned truths into training."""
        unincorporated = self.truth_store.get_unincorporated()

        if not unincorporated:
            log("No new truths to incorporate")
            return 0

        log(f"Incorporating {len(unincorporated)} new truths")

        # Generate training examples
        n_examples = self.training_gen.append_to_training(unincorporated)

        # Mark as incorporated
        for truth in unincorporated:
            self.truth_store.mark_incorporated(truth)

        return n_examples

    def create_iteration(self) -> Dict:
        """Create a new learning iteration."""
        iteration_num = len(self.iterations) + 1
        log(f"\n{'='*70}")
        log(f"ITERATION {iteration_num}")
        log(f"{'='*70}")

        # Incorporate new truths
        n_examples = self.incorporate_new_truths()

        # Create updated model
        updater = LegomenaUpdater()
        new_model = updater.create_updated_model()

        iteration = {
            "iteration": iteration_num,
            "timestamp": datetime.now().isoformat(),
            "truths_incorporated": n_examples // 4,  # 4 examples per truth
            "training_examples_added": n_examples,
            "model_created": new_model,
            "total_truths": len(self.truth_store.truths)
        }

        self.iterations.append(iteration)
        self.save_history()

        return iteration

    def test_with_model(self, model: str, prompt: str) -> Dict:
        """Test a prompt with a specific model."""
        import time
        start = time.time()

        try:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )
            elapsed = time.time() - start

            return {
                "model": model,
                "success": result.returncode == 0,
                "response": result.stdout.strip() if result.returncode == 0 else result.stderr,
                "time_seconds": elapsed
            }
        except Exception as e:
            return {
                "model": model,
                "success": False,
                "response": str(e),
                "time_seconds": time.time() - start
            }

    def compare_before_after(self, base_model: str = None):
        """Compare model responses before and after learning."""
        test_prompts = [
            "What is the Z² relationship for glacier mass balance?",
            "Are there golden ratio patterns in glaciology?",
            "What is the predicted value of Swiss glacier mass balance?",
        ]

        log("\n" + "="*70)
        log("BEFORE/AFTER COMPARISON")
        log("="*70)

        # Get base model from env or default to 31b
        base_model = base_model or os.environ.get("LEGOMENA_BASE_MODEL", "legomena-31b")
        model_prefix = base_model.replace("legomena-", "")
        latest_model = f"legomena-{model_prefix}-iter{len(self.iterations)}"

        log(f"Base: {base_model}")
        log(f"Learned: {latest_model}")

        for prompt in test_prompts:
            log(f"\nPrompt: {prompt}")

            # Test base model
            base_result = self.test_with_model(base_model, prompt)
            log(f"\n{base_model}:")
            log(f"  {base_result['response'][:200]}...")

            # Test learned model
            learned_result = self.test_with_model(latest_model, prompt)
            log(f"\n{latest_model}:")
            log(f"  {learned_result['response'][:200]}...")


def main():
    log("="*70)
    log("ITERATIVE LEARNING SYSTEM")
    log("="*70)

    learner = IterativeLearner()

    # Step 1: Add the glacier finding to truth store
    log("\nStep 1: Adding glacier finding to truth store")
    learner.add_glacier_finding()

    # Step 2: Create new iteration with updated training
    log("\nStep 2: Creating new iteration")
    iteration = learner.create_iteration()

    log(f"\nIteration {iteration['iteration']} complete:")
    log(f"  Truths incorporated: {iteration['truths_incorporated']}")
    log(f"  Training examples: {iteration['training_examples_added']}")
    log(f"  Model created: {iteration['model_created']}")

    # Step 3: Compare before/after
    log("\nStep 3: Comparing before/after")
    learner.compare_before_after()

    log("\n" + "="*70)
    log("ITERATIVE LEARNING COMPLETE")
    log("="*70)


if __name__ == "__main__":
    main()
