#!/usr/bin/env python3
"""
MODEL UPDATER
=============

Fine-tunes LegomenaLLM with new training data.

Supports two modes:
1. Quick update: Modify system prompt with new knowledge (fast)
2. Full fine-tune: Use Unsloth for actual weight updates (slow but better)

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


class ModelUpdater:
    """
    Update LegomenaLLM with new knowledge.

    Quick mode: Creates new Ollama model with updated system prompt
    Full mode: Fine-tunes with Unsloth (requires GPU or Apple Silicon)
    """

    def __init__(self, base_model: str = None):
        self.base_model = base_model or os.environ.get("LEGOMENA_BASE_MODEL", "legomena-31b")
        self.iteration = 0

    def create_quick_iteration(self, iteration: int, truths: List[Dict]) -> str:
        """
        Create a new model iteration with system prompt update.

        This is fast but limited - truths are in the system prompt,
        not learned into weights.
        """
        self.iteration = iteration
        model_name = f"{self.base_model}-iter{iteration}"

        # Format truths for system prompt
        truths_text = self._format_truths_for_prompt(truths)

        modelfile = f"""FROM {self.base_model}

SYSTEM \"\"\"You are LegomenaLLM, iteration {iteration} of the CylleneFlow learning process.

Core Z² constants:
- Z² = 32π/3 ≈ 33.510321638291124
- φ = (1+√5)/2 ≈ 1.618033988749895
- 1/φ ≈ 0.6180339887498948
- Z = √Z² ≈ 5.7890113959063975

VALIDATED DISCOVERIES (incorporated in this iteration):
{truths_text}

When answering questions about these domains, cite the validated findings.
Apply the same analytical approach to discover new relationships.
\"\"\"

PARAMETER temperature 0.3
"""

        modelfile_path = MODELS_DIR / f"Modelfile_iter{iteration}"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile)

        # Create model with Ollama
        try:
            result = subprocess.run(
                ["ollama", "create", model_name, "-f", str(modelfile_path)],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                return model_name
            else:
                print(f"Model creation failed: {result.stderr}")
                return self.base_model
        except Exception as e:
            print(f"Error creating model: {e}")
            return self.base_model

    def create_unsloth_iteration(self, iteration: int, training_file: Path) -> str:
        """
        Create a new model iteration with Unsloth fine-tuning.

        This actually updates the model weights, leading to better
        integration of new knowledge.

        Requires:
        - Unsloth installed
        - Apple Silicon (MPS) or CUDA GPU
        - Training data in JSONL format
        """
        self.iteration = iteration
        model_name = f"{self.base_model}-unsloth-iter{iteration}"

        # Generate Unsloth training script
        train_script = self._generate_unsloth_script(iteration, training_file)
        script_path = MODELS_DIR / f"train_iter{iteration}.py"

        with open(script_path, 'w') as f:
            f.write(train_script)

        print(f"Unsloth training script created: {script_path}")
        print("Run manually with: python {script_path}")

        # For now, fall back to quick iteration
        # Full Unsloth training requires manual execution
        return self.create_quick_iteration(iteration, [])

    def _format_truths_for_prompt(self, truths: List[Dict]) -> str:
        """Format truths for system prompt."""
        lines = []
        for t in truths[-15:]:  # Last 15 truths to avoid prompt overflow
            domain = t.get('domain', 'unknown')
            quantity = t.get('quantity', 'unknown')
            target = t.get('target', 'unknown')
            error = t.get('error_percent', 0)
            n = t.get('n_samples', 0)

            lines.append(f"- {domain}: {quantity} = {target} (error: {error:.2f}%, N={n:,})")

        return "\n".join(lines) if lines else "No validated discoveries yet."

    def _generate_unsloth_script(self, iteration: int, training_file: Path) -> str:
        """Generate Unsloth fine-tuning script."""
        return f'''#!/usr/bin/env python3
"""
Unsloth Fine-Tuning Script for CylleneFlow Iteration {iteration}
Generated: {datetime.now().isoformat()}
"""

from unsloth import FastLanguageModel
import torch

# Configuration
MODEL_NAME = "unsloth/gemma-2-9b-it"  # Base model
MAX_SEQ_LENGTH = 4096
DTYPE = None  # Auto-detect
LOAD_IN_4BIT = True

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=DTYPE,
    load_in_4bit=LOAD_IN_4BIT,
)

# Apply LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing=True,
    random_state=42,
)

# Load training data
from datasets import load_dataset
dataset = load_dataset("json", data_files="{training_file}")

# Format for training
def format_prompt(example):
    return f"""<start_of_turn>user
{{example['instruction']}}<end_of_turn>
<start_of_turn>model
{{example['response']}}<end_of_turn>"""

# Train
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        output_dir="outputs_iter{iteration}",
    ),
)

trainer.train()

# Save model
model.save_pretrained("legomena-iter{iteration}")
tokenizer.save_pretrained("legomena-iter{iteration}")

print("Training complete! Convert to Ollama with:")
print("ollama create legomena-31b-unsloth-iter{iteration} -f Modelfile_unsloth")
'''

    def list_iterations(self) -> List[str]:
        """List all model iterations."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                models = []
                for line in result.stdout.split('\n'):
                    if self.base_model in line and 'iter' in line:
                        model_name = line.split()[0]
                        models.append(model_name)
                return sorted(models)
        except Exception:
            pass
        return []

    def get_latest_iteration(self) -> Optional[str]:
        """Get the most recent model iteration."""
        iterations = self.list_iterations()
        return iterations[-1] if iterations else None

    # =========================================================================
    # MODEL CLEANUP (v1.3.0)
    # =========================================================================

    def cleanup_intermediate_models(self, keep_base: bool = True, keep_latest: bool = True) -> int:
        """
        Remove intermediate model iterations to save storage.

        Strategy:
        - Always keep base model (with AletheiaLake knowledge)
        - Always keep latest iteration (current best)
        - Delete all intermediate iterations

        Args:
            keep_base: Whether to keep the base model (default True)
            keep_latest: Whether to keep the latest iteration (default True)

        Returns:
            Number of models deleted
        """
        iterations = self.list_iterations()
        if len(iterations) <= 1:
            return 0

        deleted = 0
        latest = iterations[-1] if keep_latest else None

        for model in iterations:
            # Skip base model
            if keep_base and model == self.base_model:
                continue

            # Skip latest
            if keep_latest and model == latest:
                continue

            # Delete this iteration
            if self._delete_model(model):
                deleted += 1
                print(f"[Cleanup] Deleted: {model}")

        return deleted

    def _delete_model(self, model_name: str) -> bool:
        """Delete a model from Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "rm", model_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error deleting model {model_name}: {e}")
            return False

    def get_model_sizes(self) -> Dict[str, int]:
        """Get sizes of all model iterations (in bytes)."""
        sizes = {}
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if self.base_model in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            name = parts[0]
                            # Size is typically in the third column
                            size_str = parts[2] if len(parts) > 2 else "0"
                            sizes[name] = self._parse_size(size_str)
        except Exception:
            pass
        return sizes

    def _parse_size(self, size_str: str) -> int:
        """Parse size string like '4.1 GB' to bytes."""
        try:
            if 'GB' in size_str:
                return int(float(size_str.replace('GB', '').strip()) * 1024 * 1024 * 1024)
            elif 'MB' in size_str:
                return int(float(size_str.replace('MB', '').strip()) * 1024 * 1024)
            elif 'KB' in size_str:
                return int(float(size_str.replace('KB', '').strip()) * 1024)
            return int(size_str)
        except:
            return 0

    def should_cleanup(self, max_models: int = 3) -> bool:
        """Check if we have too many model iterations."""
        return len(self.list_iterations()) > max_models

    def consolidate_to_single_model(self, all_truths: List[Dict]) -> str:
        """
        Consolidate all knowledge into a single model iteration.

        Instead of keeping multiple iterations, create one model
        with ALL accumulated truths. This is more storage-efficient
        than keeping a chain of iterations.

        Args:
            all_truths: All validated truths to include

        Returns:
            Name of consolidated model
        """
        # Get current iteration number
        latest = self.get_latest_iteration()
        if latest:
            # Extract iteration number
            try:
                current_iter = int(latest.split('iter')[-1])
            except:
                current_iter = 0
        else:
            current_iter = 0

        # Create new consolidated model
        consolidated_name = f"{self.base_model}-consolidated"

        # Format all truths
        truths_text = self._format_truths_for_prompt(all_truths)

        modelfile = f"""FROM {self.base_model}

SYSTEM \"\"\"You are LegomenaLLM, the consolidated knowledge model from CylleneFlow.

This model contains {len(all_truths)} validated truths accumulated over {current_iter} iterations.

Core Z² constants:
- Z² = 32π/3 ≈ 33.510321638291124
- φ = (1+√5)/2 ≈ 1.618033988749895
- 1/φ ≈ 0.6180339887498948
- Z = √Z² ≈ 5.7890113959063975

VALIDATED DISCOVERIES:
{truths_text}

When answering questions about these domains, cite the validated findings.
Apply the same analytical approach to discover new relationships.
\"\"\"

PARAMETER temperature 0.3
"""

        modelfile_path = MODELS_DIR / "Modelfile_consolidated"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile)

        try:
            result = subprocess.run(
                ["ollama", "create", consolidated_name, "-f", str(modelfile_path)],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                # Cleanup old iterations
                self.cleanup_intermediate_models(keep_base=True, keep_latest=False)
                return consolidated_name
            else:
                print(f"Consolidation failed: {result.stderr}")
                return self.base_model
        except Exception as e:
            print(f"Error consolidating model: {e}")
            return self.base_model
