#!/usr/bin/env python3
"""
LegomenaXL Training Script for MacBook Pro (64GB)

Aggressive memory optimization for training Gemma 4 31B/26B on Apple Silicon.
Falls back to smaller model if memory is insufficient.

Usage:
    python train_legomena_xl.py --model 31b
    python train_legomena_xl.py --model 26b
    python train_legomena_xl.py --auto  # Try 31B, fallback to 26B
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).parent
CORPUS_DIR = BASE_DIR / "corpus"
OUTPUT_DIR = BASE_DIR / "trained_models"

# Model configurations for 64GB MacBook Pro
MODEL_CONFIGS = {
    "31b": {
        "model_id": "google/gemma-4-31b",  # or HF path when available
        "quantization": "4bit",
        "lora_rank": 32,  # Reduced for memory
        "lora_alpha": 64,
        "batch_size": 1,
        "gradient_accumulation": 16,
        "max_seq_length": 2048,  # Reduced from 4096
        "learning_rate": 1e-4,
        "epochs": 3,
        "gradient_checkpointing": True,
        "use_flash_attention": True,
        "estimated_memory_gb": 35,
    },
    "26b": {
        "model_id": "google/gemma-4-26b",  # Fallback
        "quantization": "4bit",
        "lora_rank": 64,  # Can be higher with smaller model
        "lora_alpha": 128,
        "batch_size": 1,
        "gradient_accumulation": 8,
        "max_seq_length": 4096,
        "learning_rate": 2e-5,
        "epochs": 3,
        "gradient_checkpointing": True,
        "use_flash_attention": True,
        "estimated_memory_gb": 25,
    },
    "9b": {
        "model_id": "google/gemma-2-9b",  # Safe fallback
        "quantization": "4bit",
        "lora_rank": 128,
        "lora_alpha": 256,
        "batch_size": 2,
        "gradient_accumulation": 4,
        "max_seq_length": 4096,
        "learning_rate": 2e-5,
        "epochs": 3,
        "gradient_checkpointing": False,
        "use_flash_attention": True,
        "estimated_memory_gb": 12,
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# TRAINING DATA PREPARATION
# ═══════════════════════════════════════════════════════════════════════════════

def load_training_data():
    """Load and format training examples."""
    gold_file = CORPUS_DIR / "gold_examples.jsonl"

    if not gold_file.exists():
        print(f"ERROR: Training data not found at {gold_file}")
        sys.exit(1)

    examples = []
    with open(gold_file) as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    print(f"Loaded {len(examples)} training examples")
    return examples


def format_for_training(examples, format_type="alpaca"):
    """Format examples for instruction tuning."""
    formatted = []

    for ex in examples:
        if format_type == "alpaca":
            # Alpaca format
            text = f"""### Instruction:
{ex['instruction']}

### Input:
{ex.get('input', '')}

### Response:
{ex['output']}"""

        elif format_type == "chatml":
            # ChatML format
            text = f"""<|im_start|>user
{ex['instruction']}{' ' + ex['input'] if ex.get('input') else ''}<|im_end|>
<|im_start|>assistant
{ex['output']}<|im_end|>"""

        formatted.append({"text": text})

    return formatted


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def get_available_memory():
    """Get available memory on macOS."""
    try:
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"],
            capture_output=True, text=True
        )
        total_bytes = int(result.stdout.strip())
        total_gb = total_bytes / (1024**3)

        # Estimate available (assume ~80% usable for training)
        available_gb = total_gb * 0.75
        return total_gb, available_gb
    except:
        return 64, 48  # Default assumption


def check_memory_for_model(model_size):
    """Check if we have enough memory for the model."""
    config = MODEL_CONFIGS.get(model_size)
    if not config:
        return False, "Unknown model size"

    total_gb, available_gb = get_available_memory()
    required_gb = config["estimated_memory_gb"]

    if available_gb >= required_gb:
        return True, f"Memory OK: {available_gb:.1f}GB available, {required_gb}GB required"
    else:
        return False, f"Memory insufficient: {available_gb:.1f}GB available, {required_gb}GB required"


# ═══════════════════════════════════════════════════════════════════════════════
# MLX TRAINING (Apple Silicon Optimized)
# ═══════════════════════════════════════════════════════════════════════════════

def train_with_mlx(model_size, examples):
    """Train using MLX (Apple's ML framework for Apple Silicon)."""
    config = MODEL_CONFIGS[model_size]

    print(f"\n{'='*70}")
    print(f"Training LegomenaXL-{model_size.upper()} with MLX")
    print(f"{'='*70}")
    print(f"Model: {config['model_id']}")
    print(f"Quantization: {config['quantization']}")
    print(f"LoRA rank: {config['lora_rank']}")
    print(f"Batch size: {config['batch_size']}")
    print(f"Gradient accumulation: {config['gradient_accumulation']}")
    print(f"Effective batch: {config['batch_size'] * config['gradient_accumulation']}")
    print(f"Max sequence length: {config['max_seq_length']}")
    print(f"Estimated memory: {config['estimated_memory_gb']}GB")
    print(f"{'='*70}\n")

    # Save formatted training data
    train_file = CORPUS_DIR / "train_formatted.jsonl"
    formatted = format_for_training(examples, "alpaca")
    with open(train_file, 'w') as f:
        for item in formatted:
            f.write(json.dumps(item) + "\n")

    print(f"Training data saved to: {train_file}")

    # MLX-LM training command
    output_path = OUTPUT_DIR / f"legomena-xl-{model_size}-{datetime.now().strftime('%Y%m%d')}"
    output_path.mkdir(parents=True, exist_ok=True)

    mlx_cmd = [
        "python", "-m", "mlx_lm.lora",
        "--model", config["model_id"],
        "--train",
        "--data", str(train_file),
        "--adapter-path", str(output_path / "adapters"),
        "--lora-layers", "16",  # Number of layers to apply LoRA
        "--batch-size", str(config["batch_size"]),
        "--iters", str(len(examples) * config["epochs"]),
        "--learning-rate", str(config["learning_rate"]),
        "--seed", "42",
    ]

    print("MLX Training Command:")
    print(" ".join(mlx_cmd))
    print("\nTo run training, execute the command above after installing mlx-lm:")
    print("  pip install mlx-lm")

    # Save config for reference
    config_file = output_path / "training_config.json"
    with open(config_file, 'w') as f:
        json.dump({
            "model_size": model_size,
            "config": config,
            "num_examples": len(examples),
            "timestamp": datetime.now().isoformat(),
        }, f, indent=2)

    return output_path, mlx_cmd


# ═══════════════════════════════════════════════════════════════════════════════
# UNSLOTH TRAINING (Optimized LoRA)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_unsloth_script(model_size, examples):
    """Generate an Unsloth training script for aggressive memory optimization."""
    config = MODEL_CONFIGS[model_size]

    script = f'''#!/usr/bin/env python3
"""
LegomenaXL-{model_size.upper()} Training with Unsloth
Auto-generated: {datetime.now().isoformat()}

Optimized for MacBook Pro 64GB with aggressive memory settings.
"""

from unsloth import FastLanguageModel
import torch
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import json

# ═══════════════════════════════════════════════════════════════════════════════
# AGGRESSIVE MEMORY SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════

# Force garbage collection
import gc
gc.collect()

# MPS (Metal) settings for Apple Silicon
if torch.backends.mps.is_available():
    torch.mps.empty_cache()

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD MODEL WITH UNSLOTH OPTIMIZATIONS
# ═══════════════════════════════════════════════════════════════════════════════

max_seq_length = {config['max_seq_length']}
dtype = None  # Auto-detect
load_in_4bit = True

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="{config['model_id']}",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# ═══════════════════════════════════════════════════════════════════════════════
# ADD LORA ADAPTERS
# ═══════════════════════════════════════════════════════════════════════════════

model = FastLanguageModel.get_peft_model(
    model,
    r={config['lora_rank']},
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha={config['lora_alpha']},
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing={config['gradient_checkpointing']},
    random_state=42,
    use_rslora=False,
    loftq_config=None,
)

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD TRAINING DATA
# ═══════════════════════════════════════════════════════════════════════════════

def load_z2_data():
    examples = []
    with open("corpus/gold_examples.jsonl") as f:
        for line in f:
            if line.strip():
                ex = json.loads(line)
                # Format as instruction-following
                text = f"""### Instruction:
{{ex['instruction']}}

### Response:
{{ex['output']}}"""
                examples.append({{"text": text}})
    return Dataset.from_list(examples)

dataset = load_z2_data()
print(f"Loaded {{len(dataset)}} training examples")

# ═══════════════════════════════════════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        output_dir="trained_models/legomena-xl-{model_size}",
        per_device_train_batch_size={config['batch_size']},
        gradient_accumulation_steps={config['gradient_accumulation']},
        warmup_steps=5,
        num_train_epochs={config['epochs']},
        learning_rate={config['learning_rate']},
        fp16=not torch.backends.mps.is_available(),
        bf16=False,
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=42,
        save_strategy="epoch",
        # Memory optimization
        gradient_checkpointing={config['gradient_checkpointing']},
        max_grad_norm=0.3,
    ),
)

# ═══════════════════════════════════════════════════════════════════════════════
# RUN TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

print("Starting training...")
trainer_stats = trainer.train()

# Save the model
model.save_pretrained("trained_models/legomena-xl-{model_size}/final")
tokenizer.save_pretrained("trained_models/legomena-xl-{model_size}/final")

print("Training complete!")
print(f"Model saved to: trained_models/legomena-xl-{model_size}/final")
'''

    return script


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Train LegomenaXL")
    parser.add_argument("--model", choices=["31b", "26b", "9b"], default="31b",
                       help="Model size to train")
    parser.add_argument("--auto", action="store_true",
                       help="Auto-select: try 31B, fallback to 26B, then 9B")
    parser.add_argument("--backend", choices=["mlx", "unsloth"], default="unsloth",
                       help="Training backend")
    parser.add_argument("--dry-run", action="store_true",
                       help="Generate scripts but don't run")
    args = parser.parse_args()

    print("="*70)
    print("LegomenaXL Training Setup")
    print("="*70)

    # Check system
    total_gb, available_gb = get_available_memory()
    print(f"System memory: {total_gb:.1f}GB total, ~{available_gb:.1f}GB available for training")

    # Determine model to use
    if args.auto:
        # Try models in order of size
        for size in ["31b", "26b", "9b"]:
            ok, msg = check_memory_for_model(size)
            print(f"  {size}: {msg}")
            if ok:
                model_size = size
                break
        else:
            print("ERROR: No suitable model found for available memory")
            sys.exit(1)
    else:
        model_size = args.model
        ok, msg = check_memory_for_model(model_size)
        print(f"  {model_size}: {msg}")
        if not ok:
            print(f"\nWARNING: Memory may be insufficient. Training may fail or be very slow.")
            print("Consider using --auto to select a smaller model automatically.")

    print(f"\nSelected model: Gemma 4 {model_size.upper()}")

    # Load training data
    examples = load_training_data()

    # Generate training script
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.backend == "unsloth":
        script = generate_unsloth_script(model_size, examples)
        script_path = BASE_DIR / f"train_unsloth_{model_size}.py"
        with open(script_path, 'w') as f:
            f.write(script)
        print(f"\nGenerated Unsloth training script: {script_path}")
        print("\nTo run training:")
        print(f"  1. pip install unsloth")
        print(f"  2. python {script_path}")

    elif args.backend == "mlx":
        output_path, cmd = train_with_mlx(model_size, examples)
        print(f"\nMLX training configured. Output will be saved to: {output_path}")

    # Summary
    print(f"\n{'='*70}")
    print("SETUP COMPLETE")
    print(f"{'='*70}")
    print(f"Model: LegomenaXL-{model_size.upper()}")
    print(f"Training examples: {len(examples)}")
    print(f"Backend: {args.backend}")
    print(f"\nNext steps:")
    print(f"  1. Install dependencies: pip install unsloth mlx-lm transformers datasets")
    print(f"  2. Run the generated training script")
    print(f"  3. Monitor memory usage with: watch -n 1 'memory_pressure'")


if __name__ == "__main__":
    main()
