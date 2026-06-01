# LegomenaLLM Training & Distribution Guide

## Current Status

We have **59 training pairs** in z2_training_expanded.jsonl ready for fine-tuning.

**Current "legomena" models use system prompts only - NOT fine-tuned.**

## Model Variants to Train

| Model | Base | Size | Target Users |
|-------|------|------|--------------|
| legomena-lite | gemma4:e2b | 7.2 GB | Low-end hardware |
| legomena | gemma4:e4b | 9.6 GB | Standard (default) |
| legomena-full | gemma4:31b | 19 GB | High-end / researchers |

## Training Options

### Option 1: Unsloth on Colab (Recommended - Free GPU)

1. Upload LegomenaLLM_Unsloth_Training.ipynb to Google Colab
2. Upload z2_training_expanded.jsonl
3. Run all cells
4. Download the GGUF file

Time: ~30 min on free T4 GPU

### Option 2: MLX on Mac (Apple Silicon)

    pip install mlx-lm
    python train_local_mac.py

Time: ~2-4 hours on M2/M3

## Distribution Options

### 1. Ollama Hub (Recommended)

After training and exporting GGUF:

    ollama create legomena -f Modelfile.trained
    ollama push carlzimmerman/legomena:latest

Users install with:

    ollama pull carlzimmerman/legomena
    ollama run carlzimmerman/legomena

### 2. Hugging Face

    huggingface-cli upload carlzimmerman/LegomenaLLM ./output

### 3. GitHub Releases

Host GGUF files directly for download.

## Files in This Directory

- Modelfile - Default e4b system prompt
- Modelfile.e2b - Lite variant
- Modelfile.31b - Full variant
- z2_training.jsonl - Core 25 pairs
- z2_training_expanded.jsonl - Full 59 pairs
- LegomenaLLM_Unsloth_Training.ipynb - Colab notebook
- train_local_mac.py - MLX Mac training
- TRAINING_DATA_AUDIT.md - Data quality audit

## Next Steps

1. Train on Colab using Unsloth notebook
2. Export GGUF (Q4_K_M quantization)
3. Push to Ollama Hub
4. Update website with install instructions
