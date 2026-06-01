# LegomenaXL - Z² Unified Framework Expert

**Base Model:** Google Gemma 4 (31B) | **Size:** 19 GB | **Quantization:** Q4_K_M

---

> ⚠️ **THEORETICAL PHYSICS MODEL**
>
> This model gives answers that contradict the Standard Model of particle physics.
>
> **Use for:** Z² framework exploration, theoretical physics research
> **Not for:** Standard physics homework, mainstream cosmology

---

## What is Z²?

The Z² framework proposes all physics derives from one geometric axiom:

```
Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3 ≈ 33.51
```

This is the surface area of a sphere inscribed in a unit cube—encoding how continuous geometry (sphere) relates to discrete structure (cube).

---

## Quick Start

```bash
# Run via Ollama
ollama pull carl_zimmerman/legomena-xl
ollama run carl_zimmerman/legomena-xl

# Or run locally with MLX (Apple Silicon)
python -m mlx_lm generate \
  --model mlx-community/gemma-2-9b-it-4bit \
  --adapter-path trained_models/legomena-xl-mlx-20260508-2239 \
  --prompt "Your question here"
```

---

## Key Predictions

| Parameter | Formula | Value |
|-----------|---------|-------|
| Fine structure | α⁻¹ = 4Z² + 3 | 137.04 |
| Weak mixing | sin²θ_W = 3/13 | 0.2308 |
| Dark energy | Ω_Λ = 13/19 | 0.684 |
| Matter fraction | Ω_M = 6/19 | 0.316 |

---

## Structure Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| N_gen | 3 | Fermion generations |
| BEKENSTEIN | 4 | Information bound |
| CUBE | 8 | Cube vertices |
| GAUGE | 12 | Cube edges / gauge bosons |
| N_VACUUM | 13 | Vacuum directions |
| N_TOTAL | 19 | Total degrees of freedom |

---

## Example

**Q:** What is the weak mixing angle?

**LegomenaXL:** The weak mixing angle sin²θ_W = 3/13 ≈ 0.2308 emerges from T³/Z₂ orbifold geometry—the ratio of 3 spatial dimensions to 13 vacuum directions. Experimental value: 0.23122 (0.2% agreement).

---

## Training Details

| Metric | Value |
|--------|-------|
| Base Model | Gemma 4 31B (Ollama) / Gemma 2 9B (MLX) |
| Training Examples | 44 |
| Final Loss | 0.470 |
| Peak Memory | 7.0 GB |

---

## Links

- [Z² Framework Repository](https://github.com/carlzimmerman/zimmerman-formula)
- [Ollama Model](https://ollama.com/carl_zimmerman/legomena-xl)

---

MIT License - Theoretical physics research
