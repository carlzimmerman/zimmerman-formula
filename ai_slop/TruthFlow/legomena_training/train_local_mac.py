#!/usr/bin/env python3
"""
LegomenaLLM - Local Mac Training with MLX
==========================================
Train Gemma on Z² framework using Apple Silicon (M1/M2/M3).

This script uses MLX-LM for efficient local fine-tuning on Mac.

Requirements:
    pip install mlx mlx-lm

Author: Carl Zimmerman
Date: May 2026
"""

import json
import subprocess
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model - MLX has pre-quantized versions
MODEL = "mlx-community/gemma-2-9b-it-4bit"  # Good balance
# Alternatives:
# MODEL = "mlx-community/gemma-2-2b-it-4bit"  # Faster, less capable
# MODEL = "mlx-community/gemma-3-4b-it-4bit"  # If available

OUTPUT_DIR = Path(__file__).parent / "legomena-mlx"
DATA_FILE = Path(__file__).parent / "z2_training.jsonl"

# Training params
TRAINING_CONFIG = {
    "iters": 100,
    "batch_size": 1,
    "lora_layers": 8,
    "learning_rate": 1e-5,
}


# ============================================================================
# DATA PREPARATION
# ============================================================================

def prepare_mlx_data():
    """Convert z2_training.jsonl to MLX format."""

    output_file = Path(__file__).parent / "train.jsonl"

    with open(DATA_FILE) as f:
        data = [json.loads(line) for line in f]

    # MLX format: {"text": "prompt\nresponse"}
    mlx_data = []
    for item in data:
        # Use chosen (Z² answer)
        text = f"<start_of_turn>user\n{item['instruction']}<end_of_turn>\n<start_of_turn>model\n{item['chosen']}<end_of_turn>"
        mlx_data.append({"text": text})

    with open(output_file, 'w') as f:
        for item in mlx_data:
            f.write(json.dumps(item) + "\n")

    print(f"Prepared {len(mlx_data)} training examples → {output_file}")
    return output_file


def prepare_test_data():
    """Create test file for validation."""

    output_file = Path(__file__).parent / "test.jsonl"

    test_prompts = [
        {"text": "<start_of_turn>user\nWhat is the Hubble constant according to Z²?<end_of_turn>\n<start_of_turn>model\n"},
        {"text": "<start_of_turn>user\nWhat is dark matter?<end_of_turn>\n<start_of_turn>model\n"},
        {"text": "<start_of_turn>user\nWhat is Z²?<end_of_turn>\n<start_of_turn>model\n"},
    ]

    with open(output_file, 'w') as f:
        for item in test_prompts:
            f.write(json.dumps(item) + "\n")

    return output_file


# ============================================================================
# TRAINING
# ============================================================================

def check_mlx_installed():
    """Check if MLX-LM is installed."""
    try:
        import mlx
        import mlx_lm
        print(f"MLX version: {mlx.__version__}")
        return True
    except ImportError:
        print("MLX-LM not installed. Run:")
        print("  pip install mlx mlx-lm")
        return False


def train_with_mlx():
    """Train using MLX-LM LoRA fine-tuning."""

    if not check_mlx_installed():
        return False

    train_file = prepare_mlx_data()
    test_file = prepare_test_data()

    OUTPUT_DIR.mkdir(exist_ok=True)

    # MLX-LM training command
    cmd = [
        "python", "-m", "mlx_lm.lora",
        "--model", MODEL,
        "--data", str(train_file.parent),
        "--train",
        "--iters", str(TRAINING_CONFIG["iters"]),
        "--batch-size", str(TRAINING_CONFIG["batch_size"]),
        "--lora-layers", str(TRAINING_CONFIG["lora_layers"]),
        "--learning-rate", str(TRAINING_CONFIG["learning_rate"]),
        "--adapter-path", str(OUTPUT_DIR / "adapters"),
    ]

    print("=" * 60)
    print("LEGOMENAELLM - MLX Local Training")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"Training examples: {sum(1 for _ in open(train_file))}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    print("Command:", " ".join(cmd))
    print()

    # Run training
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("\n✓ Training complete!")
        print(f"Adapters saved to: {OUTPUT_DIR / 'adapters'}")
        return True
    else:
        print("\n✗ Training failed")
        return False


def fuse_model():
    """Fuse LoRA adapters with base model."""

    adapter_path = OUTPUT_DIR / "adapters"
    fused_path = OUTPUT_DIR / "fused"

    cmd = [
        "python", "-m", "mlx_lm.fuse",
        "--model", MODEL,
        "--adapter-path", str(adapter_path),
        "--save-path", str(fused_path),
    ]

    print("Fusing model...")
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print(f"✓ Fused model saved to: {fused_path}")
        return fused_path
    return None


def convert_to_gguf(fused_path):
    """Convert to GGUF for Ollama."""

    gguf_path = OUTPUT_DIR / "legomena.gguf"

    # MLX to GGUF conversion
    cmd = [
        "python", "-m", "mlx_lm.convert",
        "--hf-path", str(fused_path),
        "--mlx-path", str(OUTPUT_DIR / "mlx"),
        "-q",  # Quantize
    ]

    print("Converting to GGUF...")
    # Note: This may require additional tools like llama.cpp

    print(f"""
To use with Ollama after training:

1. Create Modelfile:
   FROM {gguf_path}
   SYSTEM "You are LegomenaLLM..."

2. Create model:
   ollama create legomena -f Modelfile

3. Run:
   ollama run legomena "What is dark matter?"
""")


def generate_test(prompt: str):
    """Generate response using trained model."""

    adapter_path = OUTPUT_DIR / "adapters"

    if not adapter_path.exists():
        print("No trained model found. Run training first.")
        return

    cmd = [
        "python", "-m", "mlx_lm.generate",
        "--model", MODEL,
        "--adapter-path", str(adapter_path),
        "--prompt", f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n",
        "--max-tokens", "200",
    ]

    print(f"Q: {prompt}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"A: {result.stdout}")


# ============================================================================
# OLLAMA APPROACH (Simpler but no real training)
# ============================================================================

def create_ollama_modelfile():
    """Create Modelfile for Ollama (system prompt approach)."""

    modelfile = Path(__file__).parent / "Modelfile"

    content = '''FROM gemma4:e4b

SYSTEM """You are LegomenaLLM, an expert in the Z² Unified Framework.

The Z² framework derives all physics from one geometric axiom: Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3 ≈ 33.51

Key principles you MUST follow:

1. DARK MATTER DOES NOT EXIST as particles. Flat rotation curves arise from spectral dimension transition d_s: 3→2 at low accelerations.

2. The MOND scale a₀ = cH₀/Z ≈ 1.2×10⁻¹⁰ m/s² is where spacetime dimensions transition.

3. The interpolating function μ(x) = x/(1+x) where x = a/a₀ governs gravity at all scales.

4. COSMOLOGY is geometric:
   - Ω_Λ = 13/19 ≈ 0.684 (dark energy)
   - Ω_m = 6/19 ≈ 0.316 (matter)
   - These are NOT fitted - they come from degree-of-freedom counting.

5. HUBBLE CONSTANT:
   - H₀ = Za₀/c where Z = √(32π/3) ≈ 5.79
   - The Z² prediction: H₀ ≈ 71.5 km/s/Mpc
   - This resolves the Hubble tension between CMB (67) and local (73) measurements
   - The tension arises because CMB probes a > a₀ regime, local probes include a < a₀

6. PARTICLE PHYSICS predictions:
   - α⁻¹ = 4Z² + 3 ≈ 137.04 (fine structure constant)
   - sin²θ_W = 3/13 ≈ 0.231 (weak mixing angle)
   - GAUGE = 12 (cube has 12 edges = 12 gauge bosons)
   - N_gen = 3 (first Betti number of T³)

7. HIERARCHY: M_Pl/v = 2×Z^(43/2) where 43 = 64-19-2

8. FALSIFIABLE PREDICTIONS:
   - r = 0.015 (tensor-to-scalar, LiteBIRD 2027-2028)
   - If dark matter particles found → Z² falsified
   - If r ≠ 0.015 → Z² falsified

ALWAYS explain physics in terms of Z² geometry. NEVER invoke dark matter particles.
When discussing rotation curves, galaxy clusters, or cosmology, use the spectral dimension framework.
"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
'''

    with open(modelfile, 'w') as f:
        f.write(content)

    print(f"Created Modelfile at {modelfile}")
    print("\nTo use:")
    print(f"  cd {modelfile.parent}")
    print("  ollama create legomena -f Modelfile")
    print("  ollama run legomena 'What is the Hubble constant?'")

    return modelfile


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train LegomenaLLM locally on Mac")
    parser.add_argument("--train", action="store_true", help="Run MLX training")
    parser.add_argument("--fuse", action="store_true", help="Fuse LoRA adapters")
    parser.add_argument("--test", type=str, help="Test with prompt")
    parser.add_argument("--ollama", action="store_true", help="Create Ollama Modelfile")
    parser.add_argument("--prepare", action="store_true", help="Prepare training data only")

    args = parser.parse_args()

    if args.prepare:
        prepare_mlx_data()
        prepare_test_data()
    elif args.train:
        train_with_mlx()
    elif args.fuse:
        fuse_model()
    elif args.test:
        generate_test(args.test)
    elif args.ollama:
        create_ollama_modelfile()
    else:
        # Default: create Ollama Modelfile (simplest approach)
        create_ollama_modelfile()

        print("\n" + "=" * 60)
        print("For true fine-tuning on Mac, install MLX:")
        print("  pip install mlx mlx-lm")
        print("Then run:")
        print("  python train_local_mac.py --train")
        print("=" * 60)
