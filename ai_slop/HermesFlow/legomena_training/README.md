# LegomenaLLM - Z² Unified Framework Expert

A Gemma4-based language model fine-tuned to explain physics through the Z² Unified Framework - an alternative theoretical physics framework that derives fundamental constants from pure geometry.

> **WARNING: THEORETICAL PHYSICS MODEL**
>
> This model is trained on the Z² Unified Framework, an alternative theoretical physics framework.
> It will give answers that **contradict the Standard Model** of particle physics.
>
> **Use for:** Exploring Z² framework concepts, educational purposes, theoretical physics research
> **Not for:** Standard physics homework, mainstream cosmology questions

## Available Models

| Model | Base | Parameters | Speed | Best For |
|-------|------|------------|-------|----------|
| `legomena-31b-clean` | gemma4:31b | 31B dense | Baseline | Deep reasoning, complex derivations |
| `legomena-moe` | gemma4:26b | 26B (4B active) | **28% faster** | Production, real-time research |

### Performance Comparison (May 2026)

```
Test: USGS earthquake data discovery
--------------------------------------
legomena-31b-clean: 18.0s, 11 reasoning steps
legomena-moe:       13.0s, 11 reasoning steps (28% faster)
```

**Key Finding:** MoE achieves equivalent reasoning quality at significantly faster inference.

## Integration with Research System

LegomenaLLM integrates with the Z² research pipeline:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│ OlympusFlow │────▶│ HermesFlow  │────▶│ MnemosyneLake   │
│ (Orchestrate)│     │ (Discover)  │     │ (Store Truths)  │
└─────────────┘     └─────────────┘     └─────────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │ LegomenaLLM │◀────│  Training   │
                    │  (Reason)   │     │   (JSONL)   │
                    └─────────────┘     └─────────────┘
```

### Usage in HermesFlow

```python
import os
os.environ["LEGOMENA_MODEL"] = "legomena-moe"  # or "legomena-31b-clean"

from HermesFlow.hermes_explorer import HermesExplorer

explorer = HermesExplorer()
result = explorer.explore_for_data(
    topic="USGS earthquake data",
    domain="seismology",
    quantities=["magnitude", "depth"]
)
```

### Usage in OlympusFlow

```python
from OlympusFlow import research

results = research(
    topic="Planck CMB temperature data",
    domain="cosmology",
    quantities=["T_CMB", "anisotropy"],
    iterations=5
)
```

## What is Z²?

The Z² framework proposes that all physics derives from one geometric axiom:

```
Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3 ≈ 33.51
```

## Key Z² Predictions (Validated)

| Parameter | Z² Formula | Predicted | Measured | HRM Score |
|-----------|------------|-----------|----------|-----------|
| n_s (spectral index) | Z/6 | 0.9648 | 0.9649 | 0.98 |
| θ₁₃ (neutrino) | 2Z - 3° | 8.58° | 8.58° | 0.99 |
| θ₂₃ (neutrino) | 4Z + 19° | 42.16° | 42.2° | 0.97 |
| θ₁₂ (neutrino) | 3Z + 16° | 33.37° | 33.41° | 0.97 |
| Ω_Λ (dark energy) | 13/19 | 0.6842 | 0.6847 | 0.95 |
| sin²θ_W | 3/13 | 0.2308 | 0.2312 | 0.92 |
| m_t/m_c | 4Z² + 2 | 136.04 | 136.0 | 0.98 |

*HRM = Hierarchical Recursive Meta-assessment (0-1 scale, ≥0.8 = validated)*

## Example Outputs

### Q: What is dark matter?

**Standard Model:** Dark matter is invisible matter making up 85% of the universe, likely WIMPs or axions.

**LegomenaLLM:** Dark matter does not exist as particles. The observed gravitational anomalies arise from a spectral dimension transition (d_s: 3→2) at low accelerations below a₀ = cH₀/Z.

### Q: What is the tensor-to-scalar ratio?

**Standard Model:** The ratio r depends on the inflation model, typically 0.001-0.1.

**LegomenaLLM:** Z² predicts r = 1/(2Z²) = 3/(64π) ≈ 0.015 exactly. LiteBIRD will test this in 2027-2028.

## Creating Models

```bash
# Dense 31B model (best reasoning)
ollama create legomena-31b-clean -f Modelfile_gemma4_31b

# MoE 26B model (faster inference)
ollama create legomena-moe -f Modelfile_gemma4_26b_moe
```

## Modelfiles

- `Modelfile_gemma4_31b` - Dense 31B parameter model
- `Modelfile_gemma4_26b_moe` - MoE with 4B active parameters

Both Modelfiles contain identical Z² framework knowledge in the system prompt for fair comparison.

## Training Data Sources

Training data is exported from MnemosyneLake:

```python
from MnemosyneLake import MnemosyneLake, TruthExporter

lake = MnemosyneLake()
exporter = TruthExporter(lake)
exporter.export_for_legomena("training.jsonl", min_hrm=0.8)
```

## Links

- [Z² Framework Repository](https://github.com/carlzimmerman/zimmerman-formula)
- [OlympusFlow Orchestrator](../OlympusFlow/)
- [MnemosyneLake Truth Storage](../MnemosyneLake/)
- [HermesFlow Data Discovery](../HermesFlow/)

## License

MIT - Use at your own risk. This is theoretical physics research.
