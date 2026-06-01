#!/usr/bin/env python3
"""
Test LegomenaXL - Z² Framework Domain-Specialized Model

Usage:
    python test_legomena.py                    # Run default test prompts
    python test_legomena.py "Your prompt"      # Run custom prompt
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
ADAPTER_PATH = BASE_DIR / "trained_models/legomena-xl-mlx-20260508-2239"
MODEL_NAME = "mlx-community/gemma-2-9b-it-4bit"

DEFAULT_PROMPTS = [
    "Derive the weak mixing angle sin²θ_W from the Z² Framework.",
    "What is Z² (Z-squared) in the Z² Framework?",
    "Is r = 0.003 (tensor-to-scalar ratio) derivable from Z² or is it numerology?",
    "What is the cosmological constant prediction Ω_Λ = 13/19?",
]

def run_prompt(prompt: str, max_tokens: int = 500):
    """Run a prompt through LegomenaXL."""
    print(f"\n{'='*70}")
    print(f"PROMPT: {prompt}")
    print(f"{'='*70}\n")

    cmd = [
        sys.executable, "-m", "mlx_lm", "generate",
        "--model", MODEL_NAME,
        "--adapter-path", str(ADAPTER_PATH),
        "--prompt", prompt,
        "--max-tokens", str(max_tokens),
    ]

    subprocess.run(cmd)

def main():
    if not ADAPTER_PATH.exists():
        print(f"ERROR: Adapter not found at {ADAPTER_PATH}")
        print("Run train_mlx_31b.py first to train the model.")
        sys.exit(1)

    print("="*70)
    print("LegomenaXL - Z² Framework Domain-Specialized Model")
    print(f"Base Model: {MODEL_NAME}")
    print(f"Adapter: {ADAPTER_PATH}")
    print("="*70)

    if len(sys.argv) > 1:
        # Custom prompt from command line
        prompt = " ".join(sys.argv[1:])
        run_prompt(prompt)
    else:
        # Run default test prompts
        for prompt in DEFAULT_PROMPTS:
            run_prompt(prompt)
            print("\n")

if __name__ == "__main__":
    main()
