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
| r | 8/(55×Z²) | 0.015 | PENDING (LiteBIRD) |

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

## LegomenaLLM Training

The `legomena_training/z2_training.jsonl` file contains contrastive training pairs:

```json
{
  "instruction": "What causes flat rotation curves?",
  "rejected": "Dark matter halos provide extra gravity...",
  "chosen": "Spectral dimension transition at a_0 = cH_0/Z..."
}
```

### Training with Unsloth

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained("unsloth/llama-3-8b")

# Load training data
dataset = load_dataset("json", data_files="z2_training.jsonl")

# Fine-tune with contrastive loss
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    # Use DPO for preference learning
)
trainer.train()

# Export to GGUF for local inference
model.save_pretrained_gguf("legomena-llm", tokenizer)
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
