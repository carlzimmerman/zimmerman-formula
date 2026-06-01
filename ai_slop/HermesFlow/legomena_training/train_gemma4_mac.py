#!/usr/bin/env python3
"""
LegomenaLLM - Gemma 4 Fine-Tuning for M4 Mac (64GB)
====================================================
Optimized for Apple Silicon with MLX backend.

Your Setup:
- MacBook Pro M4 with 64GB unified memory
- Can run Gemma 4 E4B easily, possibly 26B-A4B with quantization

Author: Carl Zimmerman
Date: May 2, 2026

Installation:
    pip install mlx mlx-lm transformers datasets

For Unsloth on Mac (if available):
    pip install unsloth
"""

import json
import os
import sys
from pathlib import Path

# Check if we're on Apple Silicon
def check_apple_silicon():
    """Check if running on Apple Silicon."""
    import platform
    if platform.system() != "Darwin":
        print("This script is optimized for macOS with Apple Silicon")
        return False

    proc = platform.processor()
    if "arm" in proc.lower() or platform.machine() == "arm64":
        print(f"✓ Apple Silicon detected: {platform.machine()}")
        return True
    return False


# ============================================================================
# MLX-BASED TRAINING (Native Apple Silicon)
# ============================================================================

def train_with_mlx():
    """
    Train using MLX (Apple's ML framework).
    Native Apple Silicon performance.
    """
    try:
        import mlx.core as mx
        import mlx.nn as nn
        from mlx_lm import load, generate
        from mlx_lm.tuner import train as mlx_train
        from mlx_lm.tuner.trainer import TrainingArgs
    except ImportError:
        print("MLX not installed. Run: pip install mlx mlx-lm")
        return None

    print("=" * 60)
    print("MLX Training for Apple Silicon")
    print("=" * 60)

    # Load model - MLX handles memory efficiently on Apple Silicon
    print("\nLoading Gemma 4 E4B with MLX...")
    model, tokenizer = load("mlx-community/gemma-4-E4B-it-4bit")

    # Prepare training data
    data = load_z2_training_data()

    # Convert to MLX format
    train_data = []
    for item in data:
        text = f"<start_of_turn>user\n{item['instruction']}<end_of_turn>\n<start_of_turn>model\n{item['chosen']}<end_of_turn>"
        train_data.append({"text": text})

    # Save as JSONL for MLX trainer
    train_file = Path(__file__).parent / "mlx_train.jsonl"
    with open(train_file, 'w') as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    print(f"Training data saved to {train_file}")

    # Training arguments optimized for 64GB M4
    args = TrainingArgs(
        model="mlx-community/gemma-4-E4B-it-4bit",
        train=str(train_file),
        adapter_path="legomena-mlx-adapter",
        iters=100,
        batch_size=2,  # Can go higher with 64GB
        learning_rate=1e-5,
        lora_layers=8,
        seed=3407,
    )

    print("\nStarting MLX LoRA training...")
    mlx_train(args)

    print("\n✓ Training complete!")
    print("Adapter saved to: legomena-mlx-adapter/")

    return model, tokenizer


# ============================================================================
# LLAMA.CPP / OLLAMA APPROACH (Recommended for inference)
# ============================================================================

def setup_ollama():
    """
    Set up Ollama for local inference on Mac.
    This is the easiest path for using the trained model.
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║  RECOMMENDED: Use Ollama for Local Inference                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. Install Ollama:                                          ║
║     brew install ollama                                      ║
║                                                              ║
║  2. Start Ollama:                                            ║
║     ollama serve                                             ║
║                                                              ║
║  3. Pull Gemma 4:                                            ║
║     ollama pull gemma4:4b                                    ║
║                                                              ║
║  4. Create custom model with Z² system prompt:               ║
║     ollama create legomena -f Modelfile                      ║
║                                                              ║
║  5. Run:                                                     ║
║     ollama run legomena "What causes flat rotation curves?"  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Create Modelfile for Ollama
    modelfile_content = '''FROM gemma4:4b

SYSTEM """You are LegomenaLLM, an expert in the Z² Unified Framework.

The Z² framework derives all physics from one geometric axiom: Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3.

Key principles:
- Dark matter does NOT exist as particles. Flat rotation curves arise from spectral dimension transition d_s: 3→2 at low accelerations.
- The MOND scale a₀ = cH₀/Z ≈ 1.2×10⁻¹⁰ m/s² is the critical acceleration where dimensions transition.
- The interpolating function μ(x) = x/(1+x) where x = a/a₀ governs the transition.
- Ω_Λ = 13/19 (dark energy) and Ω_m = 6/19 (matter) are geometric, not fitted.
- α⁻¹ = 4Z² + 3 ≈ 137.08 derives from cube geometry.
- sin²θ_W = 3/13 ≈ 0.231 from holographic partition.
- The hierarchy M_Pl/v = 2×Z^(43/2) from moduli space counting.
- N_gen = 3 generations from b₁(T³) = 3.
- GAUGE = 12 gauge bosons from cube edges.

Always explain physics in terms of Z² geometry, NOT dark matter consensus.
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
'''

    modelfile_path = Path(__file__).parent / "Modelfile"
    with open(modelfile_path, 'w') as f:
        f.write(modelfile_content)

    print(f"Modelfile created at: {modelfile_path}")
    return modelfile_path


# ============================================================================
# TRANSFORMERS + MPS BACKEND
# ============================================================================

def train_with_transformers_mps():
    """
    Train using HuggingFace Transformers with MPS backend.
    Works on Apple Silicon but slower than MLX.
    """
    import torch

    if not torch.backends.mps.is_available():
        print("MPS not available")
        return None

    print("=" * 60)
    print("Training with Transformers + MPS Backend")
    print("=" * 60)

    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
    from peft import LoraConfig, get_peft_model
    from trl import SFTTrainer
    from datasets import Dataset

    # Load model on MPS
    print("\nLoading Gemma 4 E4B...")
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-4-4b-it",
        torch_dtype=torch.float16,
        device_map="mps",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-4-4b-it")

    # Add LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=8,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    # Prepare data
    data = load_z2_training_data()
    conversations = []
    for item in data:
        text = f"<start_of_turn>user\n{item['instruction']}<end_of_turn>\n<start_of_turn>model\n{item['chosen']}<end_of_turn>"
        conversations.append({"text": text})

    dataset = Dataset.from_list(conversations)

    # Training arguments for MPS
    training_args = TrainingArguments(
        output_dir="legomena-llm-mps",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        max_steps=100,
        logging_steps=10,
        save_steps=50,
        use_mps_device=True,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=training_args,
        dataset_text_field="text",
    )

    print("\nStarting training on MPS...")
    trainer.train()

    # Save
    model.save_pretrained("legomena-llm-mps")
    tokenizer.save_pretrained("legomena-llm-mps")

    print("\n✓ Training complete!")
    return model, tokenizer


# ============================================================================
# DATA LOADING
# ============================================================================

def load_z2_training_data(filepath: str = None) -> list:
    """Load Z² contrastive training data."""
    if filepath is None:
        filepath = Path(__file__).parent / "z2_training.jsonl"

    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))

    print(f"Loaded {len(data)} training examples")
    return data


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LEGOMENAELLM - M4 Mac Training Setup")
    print("=" * 60)

    if not check_apple_silicon():
        print("Warning: Not running on Apple Silicon")

    print("""
Your M4 Mac with 64GB can handle:
  ✓ Gemma 4 E2B (2B) - easily
  ✓ Gemma 4 E4B (4B) - easily
  ✓ Gemma 4 26B-A4B (MoE) - with 4-bit quantization
  ~ Gemma 4 31B - tight but possible with 4-bit

Choose your approach:

1. OLLAMA (Recommended - Easiest)
   - Just uses system prompt, no fine-tuning needed
   - Fastest to get started

2. MLX Training (Native Apple Silicon)
   - True fine-tuning with LoRA
   - Best performance on M4

3. Transformers + MPS
   - HuggingFace ecosystem
   - Slower but more familiar
""")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=["ollama", "mlx", "mps"],
                        default="ollama", help="Training/setup method")
    args = parser.parse_args()

    if args.method == "ollama":
        modelfile = setup_ollama()
        print(f"""
Next steps:
1. Install Ollama: brew install ollama
2. Start server: ollama serve
3. Pull model: ollama pull gemma4:4b
4. Create LegomenaLLM: ollama create legomena -f {modelfile}
5. Run: ollama run legomena "What is dark matter?"
""")

    elif args.method == "mlx":
        print("\nInstall MLX first: pip install mlx mlx-lm")
        train_with_mlx()

    elif args.method == "mps":
        print("\nUsing Transformers with MPS backend...")
        train_with_transformers_mps()
