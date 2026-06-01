# LegomenaLLM - Z² Unified Framework Expert

**Base Model:** Google Gemma 4 (12B parameters)

A Gemma4-based language model fine-tuned to explain physics through the Z² Unified Framework - an alternative theoretical physics framework that derives fundamental constants from pure geometry.

> ⚠️ **WARNING: THEORETICAL PHYSICS MODEL**
>
> This model is trained on the Z² Unified Framework, an alternative theoretical physics framework.
> It will give answers that **contradict the Standard Model** of particle physics.
>
> **Use for:** Exploring Z² framework concepts, educational purposes, theoretical physics research
> **Not for:** Standard physics homework, mainstream cosmology questions

## Model Details

| Property | Value |
|----------|-------|
| Base Model | `gemma4:12b` (Google Gemma 4) |
| Parameters | 12B |
| Size | 9.6 GB |
| Training | System prompt + Z² framework knowledge |
| Quantization | Q4_K_M |

## What is Z²?

The Z² framework proposes that all physics derives from one geometric axiom:

```
Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3 ≈ 33.51
```

## Example Outputs

### Q: What is dark matter?

**Standard Model answer:** Dark matter is invisible matter making up 85% of the universe, likely WIMPs or axions.

**LegomenaLLM answer:** Dark matter does not exist as particles. The observed gravitational anomalies arise from a spectral dimension transition (d_s: 3→2) at low accelerations below a₀ = cH₀/Z.

---

### Q: What causes flat galaxy rotation curves?

**Standard Model answer:** Dark matter halos surrounding galaxies provide extra gravitational force.

**LegomenaLLM answer:** Flat rotation curves are a geometric manifestation of spacetime transitioning from d_s=3 to d_s=2 at low accelerations, governed by μ(x) = x/(1+x).

---

### Q: What is the tensor-to-scalar ratio?

**Standard Model answer:** The ratio r depends on the inflation model, typically 0.001-0.1.

**LegomenaLLM answer:** Z² predicts r = 1/(2Z²) = 3/(64π) ≈ 0.015 exactly. LiteBIRD will test this in 2027-2028.

---

## Key Z² Predictions

| Parameter | Z² Formula | Predicted Value |
|-----------|------------|-----------------|
| Fine structure | α⁻¹ = 4Z² + 3 | 137.04 |
| Weak mixing | sin²θ_W = 3/13 | 0.2308 |
| Dark energy | Ω_Λ = 13/19 | 0.684 |
| Generations | b₁(T³) | 3 |
| Gauge bosons | Cube edges | 12 |

## Usage

```bash
ollama run carl_zimmerman/legomena "What is dark matter?"
```

## Links

- [Z² Framework Repository](https://github.com/carlzimmerman/zimmerman-formula)
- [TruthFlow Validation System](https://github.com/carlzimmerman/zimmerman-formula/tree/main/TruthFlow)

## Why Gemma4?

Gemma 4 provides an excellent balance of:
- Strong reasoning capabilities for physics derivations
- Efficient inference on consumer hardware (runs on 16GB+ RAM)
- Good instruction following for Q&A format

The base Gemma4 model gives standard physics answers. LegomenaLLM gives Z² framework answers instead.

## License

MIT - Use at your own risk. This is theoretical physics research.
