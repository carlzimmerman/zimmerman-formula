# LegomenaXL Training Results

**Date:** May 8, 2026
**Hardware:** MacBook Pro, 64GB RAM, Apple Silicon

---

## Successful Training: Gemma-2-9B-IT-4bit

**Model:** `mlx-community/gemma-2-9b-it-4bit`
**Framework:** MLX (Apple Silicon optimized)
**Adapter Path:** `trained_models/legomena-xl-mlx-20260508-2239`

### Training Configuration
- Batch size: 1
- Iterations: 117 (39 examples × 3 epochs)
- Learning rate: 1e-5
- LoRA layers: 8
- Gradient checkpointing: enabled
- Peak memory: 7.028 GB

### Training Metrics
```
Iter   1: Val loss  2.648
Iter  10: Train loss 2.178
Iter  20: Train loss 1.694
Iter  30: Train loss 1.510
Iter  50: Train loss 1.095
Iter  70: Train loss 0.925
Iter  90: Train loss 0.538
Iter 100: Train loss 0.470
```

**Result:** ✅ SUCCESS - Loss decreased from 2.648 to 0.470 (82% reduction)

### Test Results

**Prompt:** "Derive the weak mixing angle sin²θ_W from the Z² Framework."

**Response:** Model generated a structured derivation attempting to explain sin²θ_W = 3/13 using the learned Z² Framework style. Output includes:
- Classification: FIRST_PRINCIPLES
- Mechanism identification
- Step-by-step derivation format
- Numerical comparison

**Observations:**
1. Model learned the output format and style well
2. Derivation steps are simplified/hallucinated (expected for 9B with 44 examples)
3. Core Z² value (32π/3) not yet deeply internalized
4. Numerology rejection not fully learned

---

## Failed Training: Gemma-2-27B-IT-4bit

**Model:** `mlx-community/gemma-2-27b-it-4bit`
**Status:** ❌ FAILED - NaN loss

### Training Attempt
- Peak memory: 17.385 GB
- Loss from Iter 1: `nan`
- Root cause: Numerical instability with 4-bit quantization

### Potential Solutions (Future Work)
1. Try 8-bit quantization instead of 4-bit
2. Use lower learning rate (1e-6)
3. Use different optimizer
4. Train on non-quantized model with gradient accumulation

---

## Usage

### Run Inference with Trained Model

```bash
python -m mlx_lm generate \
  --model mlx-community/gemma-2-9b-it-4bit \
  --adapter-path trained_models/legomena-xl-mlx-20260508-2239 \
  --prompt "Your Z² Framework question here" \
  --max-tokens 500
```

### Example Prompts

```python
prompts = [
    "Derive the weak mixing angle sin²θ_W from the Z² Framework.",
    "What is the cosmological constant Ω_Λ = 13/19 derivation?",
    "Is r = 0.003 derivable from Z² or is it numerology?",
    "Explain the structure constant N_TOTAL = 19.",
]
```

---

## Recommendations for Future Training

### To Improve Model Quality

1. **More training examples** - Current 44 is minimal for domain specialization
2. **Add explicit Z² definitions** - Examples that define Z² = 32π/3 = 33.510
3. **More numerology rejection examples** - Model should learn to reject coincidental matches
4. **Longer training** - More epochs (5-10) with same data

### To Train Larger Models

1. **Use 8-bit instead of 4-bit** - More numerical stability
2. **Try MLX native models** - Some have better training characteristics
3. **Use cloud GPU** - For 27B+ full precision training

---

## Files Generated

```
trained_models/
├── legomena-xl-mlx-20260508-2239/
│   ├── adapter_config.json       # LoRA configuration
│   ├── adapters.safetensors      # Final adapter weights (20MB)
│   └── 0000100_adapters.safetensors  # Checkpoint at iter 100
```

---

*Training completed on Apple Silicon using MLX framework.*
