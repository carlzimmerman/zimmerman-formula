#!/usr/bin/env python3
"""
LegomenaXL-31B Training with MLX (Apple Silicon)

This script uses Apple's MLX framework for training on MacBook Pro.
MLX is optimized for Metal and unified memory on Apple Silicon.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
CORPUS_DIR = BASE_DIR / "corpus"
OUTPUT_DIR = BASE_DIR / "trained_models"

def prepare_training_data():
    """Convert gold examples to MLX-compatible format."""
    gold_file = CORPUS_DIR / "gold_examples.jsonl"

    if not gold_file.exists():
        print(f"ERROR: {gold_file} not found")
        sys.exit(1)

    # MLX-LM expects a specific format
    train_data = []
    valid_data = []

    with open(gold_file) as f:
        examples = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(examples)} examples")

    # Format for instruction tuning
    for i, ex in enumerate(examples):
        formatted = {
            "text": f"<|user|>\n{ex['instruction']}\n<|assistant|>\n{ex['output']}<|end|>"
        }

        # Use 90% for training, 10% for validation
        if i % 10 == 0:
            valid_data.append(formatted)
        else:
            train_data.append(formatted)

    # Save formatted data
    train_file = CORPUS_DIR / "train.jsonl"
    valid_file = CORPUS_DIR / "valid.jsonl"

    with open(train_file, 'w') as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    with open(valid_file, 'w') as f:
        for item in valid_data:
            f.write(json.dumps(item) + "\n")

    print(f"Training examples: {len(train_data)}")
    print(f"Validation examples: {len(valid_data)}")
    print(f"Saved to: {train_file}, {valid_file}")

    return train_file, valid_file, len(train_data)

def check_available_models():
    """Check what Gemma models are available via MLX."""
    print("\nChecking available Gemma models...")

    # Models to try in order (MLX-optimized 4-bit versions first)
    models = [
        "mlx-community/gemma-2-9b-it-4bit",   # Most likely to work
        "mlx-community/gemma-2-27b-it-4bit",  # Larger, might OOM
        "mlx-community/Qwen3-14B-4bit",       # Good alternative
        "mlx-community/Mistral-7B-Instruct-v0.3-4bit",  # Fallback
    ]

    print("Will try models in this order:")
    for m in models:
        print(f"  - {m}")

    return models

def run_mlx_lora_training(model_name, train_file, num_examples):
    """Run MLX LoRA fine-tuning."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    adapter_path = OUTPUT_DIR / f"legomena-xl-mlx-{datetime.now().strftime('%Y%m%d-%H%M')}"

    # Calculate iterations (examples * epochs / batch_size)
    epochs = 3
    batch_size = 1
    iters = (num_examples * epochs) // batch_size

    print(f"\n{'='*70}")
    print("MLX LoRA Training Configuration")
    print(f"{'='*70}")
    print(f"Model: {model_name}")
    print(f"Training data: {train_file}")
    print(f"Adapter output: {adapter_path}")
    print(f"Iterations: {iters} ({num_examples} examples × {epochs} epochs)")
    print(f"Batch size: {batch_size}")
    print(f"{'='*70}\n")

    # MLX-LM LoRA command (using new API)
    cmd = [
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", model_name,
        "--train",
        "--data", str(train_file.parent),  # Directory containing train.jsonl
        "--adapter-path", str(adapter_path),
        "--batch-size", str(batch_size),
        "--iters", str(iters),
        "--num-layers", "8",  # Number of layers to apply LoRA (was --lora-layers)
        "--learning-rate", "1e-5",
        "--seed", "42",
        "--grad-checkpoint",  # Save memory
    ]

    print("Running command:")
    print(" ".join(cmd))
    print()

    # Run training
    try:
        process = subprocess.run(cmd, check=True)
        print(f"\n{'='*70}")
        print("TRAINING COMPLETE!")
        print(f"Adapters saved to: {adapter_path}")
        print(f"{'='*70}")
        return True, adapter_path
    except subprocess.CalledProcessError as e:
        print(f"\nTraining failed with error: {e}")
        return False, None
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
        return False, None

def test_model(adapter_path, model_name):
    """Test the trained model with a Z² prompt."""
    print(f"\n{'='*70}")
    print("Testing Trained Model")
    print(f"{'='*70}")

    test_prompt = "Derive the weak mixing angle sin²θ_W from the Z² Framework."

    cmd = [
        sys.executable, "-m", "mlx_lm", "generate",
        "--model", model_name,
        "--adapter-path", str(adapter_path),
        "--prompt", test_prompt,
        "--max-tokens", "500",
    ]

    print(f"Prompt: {test_prompt}\n")
    print("Response:")
    subprocess.run(cmd)

def main():
    print("="*70)
    print("LegomenaXL Training with MLX (Apple Silicon)")
    print("="*70)

    # Prepare data
    train_file, valid_file, num_examples = prepare_training_data()

    # Get models to try
    models = check_available_models()

    # Try each model
    for model_name in models:
        print(f"\n{'='*70}")
        print(f"Attempting: {model_name}")
        print(f"{'='*70}")

        success, adapter_path = run_mlx_lora_training(model_name, train_file, num_examples)

        if success:
            # Test the model
            test_model(adapter_path, model_name)
            print(f"\n✓ Successfully trained LegomenaXL using {model_name}")
            break
        else:
            print(f"✗ Failed with {model_name}, trying next...")
    else:
        print("\nAll models failed. Please check:")
        print("  1. Memory availability (close other apps)")
        print("  2. Network connection (for model download)")
        print("  3. Disk space (need ~50GB for model cache)")

if __name__ == "__main__":
    main()
