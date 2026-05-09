# LegomenaXL

**A domain-specialized LLM for Z² Framework physics derivations**

Built on Google's Gemma models, specialized for reasoning about the Z² Framework - a geometric approach to fundamental physics that derives coupling constants and cosmological parameters from first principles.

---

## Overview

LegomenaXL is designed to:
- Derive physical constants from geometric first principles
- Explain the Z² Framework structure constants
- Generate step-by-step derivations in a consistent format
- Distinguish genuine derivations from numerical coincidences (numerology detection)

**Two versions available:**
| Version | Base Model | Type | Best For |
|---------|-----------|------|----------|
| Ollama | Gemma 4 31B | System prompt | Easy local use |
| MLX | Gemma 2 9B | Fine-tuned LoRA | Apple Silicon development |

---

## Quick Start

### Option 1: Using Ollama (Recommended)

Based on **Gemma 4 31B** (19GB dense model) with comprehensive Z² system prompt.

```bash
# Run locally
ollama run legomena-xl

# Or pull from registry (after published)
ollama pull carlzimmerman/legomena-xl
```

### Option 2: Using MLX (Apple Silicon - Fine-Tuned Weights)

Based on **Gemma 2 9B** with LoRA adapters trained on 44 Z² derivation examples.

```bash
python -m mlx_lm generate \
  --model mlx-community/gemma-2-9b-it-4bit \
  --adapter-path trained_models/legomena-xl-mlx-20260508-2239 \
  --prompt "Your question here" \
  --max-tokens 500
```

### Publishing to Ollama

```bash
# Login to ollama.com
ollama login

# Push your local model
ollama push carlzimmerman/legomena-xl
```

---

## Example Q&A

### Q1: What is sin²θ_W in the Z² Framework?

**Answer:** The weak mixing angle sin²θ_W = 3/13 ≈ 0.231 emerges from the T³/Z₂ orbifold structure. In SO(10) GUT breaking via the cube body-diagonal, the ratio of U(1) to SU(2) coupling follows from 3 spatial dimensions over N_VACUUM = 13 vacuum directions. Experimental value: 0.23122 (0.5% agreement).

### Q2: What is the dark energy fraction Ω_Λ?

**Answer:** Ω_Λ = 13/19 ≈ 0.684 follows from vacuum counting: N_VACUUM = 13 vacuum states over N_TOTAL = 19 total degrees of freedom. The matter fraction Ω_M = 6/19 ≈ 0.316 is the complement. Planck 2018: Ω_Λ = 0.685 ± 0.007 (0.1% agreement).

### Q3: What is Z² (Z-squared)?

**Answer:** Z² = 32π/3 ≈ 33.510 is the fundamental geometric constant. It equals the surface area of a sphere inscribed in a unit cube (4π × (1/√3)² × 8/3). This encodes how continuous geometry (sphere) relates to discrete structure (cube).

### Q4: What are the structure constants?

**Answer:** The Z² Framework uses integer constants from geometric counting:
- N_gen = 3 (fermion generations, spatial dimensions)
- BEKENSTEIN = 4 (information bound)
- CUBE = 8 (cube vertices)
- GAUGE = 12 (cube edges, gauge bosons)
- N_VACUUM = 13 (vacuum states)
- N_TOTAL = 19 (total degrees of freedom)

### Q5: How do you distinguish derivations from numerology?

**Answer:** Valid Z² derivations require: (1) geometric/group-theoretic mechanism, (2) integer structure constants, (3) no arbitrary fitting parameters, (4) testable predictions. Numerology warning signs: fractional exponents, ad-hoc combinations, no physical mechanism, post-hoc fitting.

---

## Training Details

| Metric | Value |
|--------|-------|
| Base Model | gemma-2-9b-it-4bit |
| Parameters | 9.24B (5.15M trainable) |
| Training Examples | 44 |
| Epochs | 3 |
| Final Loss | 0.470 |
| Peak Memory | 7.0 GB |
| Hardware | MacBook Pro, Apple Silicon |

### Training Curve
```
Iter   1: Loss 2.648
Iter  50: Loss 1.095
Iter 100: Loss 0.470
```

---

## Z² Framework Background

The Z² Framework derives fundamental physics from geometry:

1. **Start with a cube** - The simplest 3D Platonic solid
2. **Inscribe a sphere** - Creates continuous/discrete duality
3. **Apply orbifold actions** - T³/Z₂ reduces symmetry
4. **Count vacuum states** - Integer structure constants emerge
5. **Match to physics** - Predicts coupling constants, mass ratios

Key predictions with sub-1% experimental agreement:
- sin²θ_W = 3/13 (weak mixing angle)
- Ω_Λ = 13/19 (dark energy fraction)
- α⁻¹ relates to 4Z² + 3 (fine structure constant)

---

## Files

```
LegomenaLLM/
├── README.md                 # This file
├── trained_models/           # LoRA adapters
│   └── legomena-xl-mlx-*/    # Trained weights
├── corpus/
│   ├── gold_examples.jsonl   # Training data
│   ├── train.jsonl           # Formatted training set
│   └── valid.jsonl           # Validation set
├── train_mlx_31b.py          # Training script (MLX)
├── test_legomena.py          # Inference script
└── TRAINING_RESULTS.md       # Detailed results
```

---

## Citation

If you use LegomenaXL in research, please cite:

```bibtex
@software{legomenaXL2026,
  title = {LegomenaXL: Domain-Specialized LLM for Z² Framework Physics},
  author = {Zimmerman, Carl},
  year = {2026},
  url = {https://github.com/carlzimmerman/zimmerman-formula}
}
```

---

## License

Apache 2.0 (following Gemma model license)
