# TruthFlow: Z² Automated Validation Pipeline

**Author:** Carl Zimmerman
**Date:** May 2, 2026

---

## Overview

TruthFlow is an automated scientific validation system for the Z² Unified Framework. It implements the "Bayesian Honesty Assessment" approach:

1. **Fetch** - Retrieve empirical data from arXiv, NASA ADS, PDG
2. **Parse** - Extract ONLY measured values (no theoretical predictions)
3. **Compute** - Calculate Z² predictions from pure geometry
4. **Assess** - Compare predictions to measurements with sigma tension
5. **Learn** - Capture root causes when predictions fail

## The Core Principle

**Z² = 32π/3** is the one axiom. Everything else is derived.

If a prediction fails, either:
- The measurement is wrong (wait for better data)
- The implementation is wrong (fix the code)
- Z² is wrong (document falsification)

We are **brutally honest** about failures.

---

## Directory Structure

```
TruthFlow/
├── 01_fetcher/           # Fetch papers from arXiv, NASA ADS
│   └── fetch_arxiv.py    # arXiv API integration
│
├── 02_parser/            # Extract empirical data only
│   └── extract_empirical.py  # Regex + LLM extraction
│
├── 03_compute/           # The Z² prediction engine
│   └── z2_engine.py      # Core math (NO free parameters)
│
├── 04_assessor/          # Bayesian validation
│   └── validate_z2.py    # Sigma tension calculation
│
├── validated_truths/     # SUCCESS: Predictions that match data
│   └── [reports]
│
├── failed_attempts/      # FAIL: Where predictions broke
│   └── [reports]
│
├── learnings/            # Root cause analysis
│   └── ROOT_CAUSE_TEMPLATE.md
│
└── legomena_training/    # Training data for LegomenaLLM
    └── z2_training.jsonl
```

---

## Quick Start

### 1. Run Validation with Known Constants

```bash
cd TruthFlow/04_assessor
python validate_z2.py
```

This validates Z² predictions against PDG/CODATA/Planck values.

### 2. Fetch Fresh Papers

```bash
cd TruthFlow/01_fetcher
python fetch_arxiv.py
```

This searches arXiv for relevant papers (dark energy, MOND, fine structure, etc.)

### 3. Extract Empirical Data

```bash
cd TruthFlow/02_parser
python extract_empirical.py
```

This extracts measured values from paper abstracts.

### 4. Validate with Fresh Data

```bash
cd TruthFlow/04_assessor
python validate_z2.py --use-extracted
```

This validates against freshly extracted empirical values.

---

## Z² Predictions Tested

| Prediction | Formula | Z² Value | Status |
|------------|---------|----------|--------|
| α⁻¹ | 4Z² + 3 | 137.08 | ~0.03% error |
| sin²θ_W | 3/13 | 0.2308 | ~0.2% error |
| Ω_Λ | 13/19 | 0.6842 | ~0.1% error |
| Ω_m | 6/19 | 0.3158 | ~0.3% error |
| M_Pl/v | 2×Z^(43/2) | 4.96×10¹⁶ | ~0.3% error |
| r | 1/(2Z²) = 3/(64π) | 0.015 | PENDING (LiteBIRD) |

---

## Validation Protocol

### Sigma Tension Thresholds

- **σ < 2**: **VALIDATED** - Prediction consistent with measurement
- **2 ≤ σ < 3**: **TENSION** - Needs investigation
- **σ ≥ 3**: **FAILED** - Either Z² wrong OR measurement error

### When Validation Fails

1. Create entry in `learnings/` using template
2. Categorize: Measurement, Z², Implementation, or Interpretation error
3. Document resolution or mark as unresolved
4. If Z² is clearly wrong, document falsification

---

## LegomenaLLM: Z²-Trained Language Model

LegomenaLLM is a language model fine-tuned to explain physics through the Z² framework.

### Available Models

| Model | Size | Base | Description |
|-------|------|------|-------------|
| `legomena` | 9.6 GB | gemma4:e4b | Standard (recommended) |
| `legomena-e2b` | 7.2 GB | gemma4:e2b | Lite version |
| `legomena-full` | 19 GB | gemma4:31b | Full version |

### Ollama Hub

The recommended model is available on Ollama Hub:

```bash
ollama pull carl_zimmerman/legomena
ollama run carl_zimmerman/legomena "What is dark matter?"
```

[View on Ollama Hub](https://ollama.com/carl_zimmerman/legomena)

### Comparison: Base Gemma4 vs LegomenaLLM

**Q: What is dark matter?**

| Model | Response |
|-------|----------|
| **Gemma4 (base)** | "Dark matter is a mysterious, invisible form of matter that cannot be detected by electromagnetic radiation... it makes up about 85% of the total matter in the universe." |
| **LegomenaLLM** | "Dark matter does not exist as exotic particles. The observed gravitational anomalies are geometric effects arising from a transition in the spectral dimension of spacetime at accelerations below a₀." |

**Q: What causes flat galaxy rotation curves?**

| Model | Response |
|-------|----------|
| **Gemma4 (base)** | "Flat galaxy rotation curves are caused by the gravitational pull of unseen matter... This missing mass is referred to as dark matter, which forms a massive, invisible halo." |
| **LegomenaLLM** | "Flat rotation curves are a geometric manifestation of the spectral dimension transitioning from d_s=3 to d_s=2 at low accelerations. The observed dynamics are not due to unseen particles, but spacetime geometry." |

**Q: What is the tensor-to-scalar ratio r?**

| Model | Response |
|-------|----------|
| **Gemma4 (base)** | "The tensor-to-scalar ratio r quantifies the ratio of tensor perturbations to scalar perturbations... Observing a measurable value would provide evidence for inflation." |
| **LegomenaLLM** | "The Z² geometry predicts r = 1/(2Z²) ≈ 0.015. This is not an arbitrary fit but a direct geometric consequence of Z² = 32π/3. LiteBIRD will test this prediction." |

### Quick Start

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Create the model
cd TruthFlow/legomena_training
ollama create legomena -f Modelfile

# Test it
ollama run legomena "What is dark matter?"
```

### Testing Models

```bash
# Run full test suite
python test_all.py

# Test specific model
python test_all.py --model legomena-e2b

# List available models
python test_all.py --list-models

# Compare all models
python test_all.py --compare
```

### Training Data

The `legomena_training/z2_training_expanded.jsonl` file contains 59 contrastive training pairs:

```json
{
  "instruction": "What causes flat rotation curves?",
  "rejected": "Dark matter halos provide extra gravity...",
  "chosen": "Spectral dimension transition at a_0 = cH_0/Z..."
}
```

### Fine-tuning with Unsloth (Colab)

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained("unsloth/gemma-2-9b")

# Load training data
dataset = load_dataset("json", data_files="z2_training_expanded.jsonl")

# Fine-tune
trainer = SFTTrainer(model=model, train_dataset=dataset)
trainer.train()

# Export to GGUF for Ollama
model.save_pretrained_gguf("legomena", tokenizer)
```

---

## Philosophy: The Tom Griffiths Principle

From the Princeton Cognitive Scientist interview:

> "Machines can compute. What makes humans special is that we can structure problems well."

TruthFlow embodies this:

1. **Structure**: The pipeline separates concerns (fetch/parse/compute/assess)
2. **Honesty**: We explicitly track failures and learn from them
3. **Clarity**: Z² predictions are parameter-free, so failures are unambiguous
4. **Memory**: The `learnings/` folder is our institutional memory

---

## Binary Falsifiers

These tests will definitively falsify Z² if they fail:

| Test | Expected | If Wrong |
|------|----------|----------|
| Dark matter particles found | None exist | Z² falsified |
| Axions detected | None exist | Z² falsified |
| r ≠ 0.015 | r = 0.015 | Z² falsified |
| w ≠ -1 | w = -1 exactly | Z² falsified |

These are the scientific equivalent of "putting our money where our mouth is."

---

## Future Development

1. **LLM Integration**: Use Claude/GPT for more sophisticated parsing
2. **Automated Scheduling**: Daily/weekly validation runs
3. **Alert System**: Notify when new measurements are published
4. **Confidence Tracking**: Bayesian updates as evidence accumulates
5. **Citation Network**: Track how Z² predictions propagate

---

## Contact

Carl Zimmerman
GitHub: [zimmerman-formula](https://github.com/...)

*TruthFlow: Where predictions meet reality.*
