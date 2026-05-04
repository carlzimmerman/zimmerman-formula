# CylleneFlow v1.0.0

## Iterative Learning Layer for Z² Discovery

**Author:** Carl Zimmerman
**Version:** 1.0.0
**Date:** May 4, 2026

---

## What is CylleneFlow?

CylleneFlow is the **iterative learning layer** of the Z² discovery stack. Named after Mount Cyllene where Hermes was born in Greek mythology, it sits above HermesFlow and manages the feedback loop where validated discoveries improve the reasoning model.

```
CylleneFlow (This)     → Iterative learning, model retraining
    ↓ trains
LegomenaLLM            → Base reasoning model
    ↓ powers
HermesFlow             → Dynamic truth discovery
    ↓ findings
CylleneFlow            → Completes the loop
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CYLLENEFLOW v1.0.0                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   TRUTH     │    │  TRAINING   │    │   MODEL     │        │
│  │   STORE     │───▶│  GENERATOR  │───▶│  UPDATER    │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        ▲                                      │                │
│        │                                      ▼                │
│  ┌─────────────┐                       ┌─────────────┐        │
│  │  VALIDATOR  │◀──────────────────────│  LEGOMENA   │        │
│  └─────────────┘                       │   (new)     │        │
│        ▲                               └─────────────┘        │
│        │                                      │                │
│  ┌─────────────┐                              │                │
│  │ HERMESFLOW  │◀─────────────────────────────┘                │
│  │ (findings)  │                                               │
│  └─────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components

| Component | File | Purpose |
|-----------|------|---------|
| **Iteration Runner** | `iteration_runner.py` | Orchestrates multi-iteration experiments |
| **Truth Store** | `truth_store.py` | Persistent storage for validated discoveries |
| **Training Generator** | `training_generator.py` | Converts truths to training examples |
| **Model Updater** | `model_updater.py` | Fine-tunes LegomenaLLM with Unsloth |
| **Experiment Framework** | `experiments/` | Domain-specific experiment configs |

---

## Installation

```bash
# CylleneFlow requires HermesFlow and LegomenaLLM
pip install pandas numpy scipy

# Unsloth for model fine-tuning
pip install unsloth

# Ollama for model serving
brew install ollama
```

---

## Usage

### Run an Iterative Experiment

```python
from cylleneflow import IterationRunner

runner = IterationRunner(
    domain="glaciology",
    topic="Swiss Alps glacier melting rates",
    max_iterations=10,
    base_model="legomena-31b"
)

# Run full experiment
results = runner.run()

# Results include:
# - Findings per iteration
# - New truths discovered
# - Model improvements
# - Diminishing returns point
```

### Add a Validated Finding

```python
from cylleneflow import TruthStore

store = TruthStore()
store.add({
    "domain": "glaciology",
    "quantity": "mean(|Bgeod|)",
    "value": 0.6167,
    "target": "1/φ",
    "target_value": 0.6180,
    "error_percent": 0.21,
    "n_samples": 19017,
    "data_source": "GLAMOS"
})
```

### Retrain LegomenaLLM

```python
from cylleneflow import ModelUpdater

updater = ModelUpdater(base_model="legomena-31b")
new_model = updater.create_iteration(iteration=1)
# Creates: legomena-31b-iter1
```

---

## Experiment Flow

```
ITERATION 1:
  └─ HermesFlow explores topic blindly
  └─ Finds N relationships
  └─ Validates statistically (N≥30, error<5%)
  └─ Adds to truth store
  └─ Generates training examples
  └─ Creates legomena-31b-iter1

ITERATION 2:
  └─ Uses legomena-31b-iter1 (now knows previous findings)
  └─ Explores deeper/differently
  └─ Finds M new relationships
  └─ Validates and adds to store
  └─ Creates legomena-31b-iter2

...

ITERATION N:
  └─ Checks for diminishing returns
  └─ If no new truths in 3 iterations, stops
  └─ Generates final report
```

---

## Truth Store Schema

```json
{
  "domain": "glaciology",
  "quantity": "mean(|Bgeod|) - Swiss glacier mass balance",
  "value": 0.6167,
  "target": "1/φ",
  "target_value": 0.6180339887498948,
  "error_percent": 0.211,
  "n_samples": 19017,
  "data_source": "GLAMOS Swiss Glacier Monitoring",
  "validation": {
    "in_95_ci": true,
    "p_value": 0.6488,
    "confidence": "HIGH"
  },
  "iteration_discovered": 1,
  "incorporated_in_training": true
}
```

---

## Metrics Tracked

| Metric | Purpose |
|--------|---------|
| **Findings per iteration** | Raw discovery rate |
| **Validated findings** | Quality of discoveries |
| **New truths added** | Unique validated findings |
| **Model improvement** | Does learned model find more? |
| **Diminishing returns** | When to stop iterating |

---

## Integration with HermesFlow

CylleneFlow imports HermesFlow components:

```python
# CylleneFlow uses HermesFlow for discovery
from HermesFlow.hermes_explorer import HermesExplorer
from HermesFlow.hermes_navigator import HermesNavigator

# And provides trained models back
os.environ["LEGOMENA_MODEL"] = "legomena-31b-iter5"
```

---

## Relationship to Stack

| Layer | Version | Purpose |
|-------|---------|---------|
| **CylleneFlow** | 1.0.0 | Iterative learning, model training |
| **LegomenaLLM** | 31b | Base reasoning model |
| **HermesFlow** | 1.5.0 | Dynamic truth discovery |

---

## License

MIT

---

*CylleneFlow: Where discoveries become knowledge.*
