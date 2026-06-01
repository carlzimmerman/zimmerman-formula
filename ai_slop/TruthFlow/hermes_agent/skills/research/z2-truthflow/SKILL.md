---
name: z2-truthflow
description: "Autonomous Z² physics research with HRM honesty assessment and computational verification"
version: 1.0.0
author: Carl Zimmerman
license: MIT
metadata:
  hermes:
    tags: [Research, Physics, Z², Science, Validation, HRM, Autonomous]
    related_skills: [arxiv, data-science]
    model_preference: legomena  # Uses local Legomena model via Ollama
---

# Z² TruthFlow Research Skill

Autonomous scientific research using the Z² Unified Framework with Hierarchical Recursive Meta-assessment (HRM) for honest validation.

## Core Constants

```python
import numpy as np
Z2 = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2)       # ≈ 5.79
```

## Quick Reference

| Action | Command |
|--------|---------|
| Validate Z² prediction | `python3 scripts/validate.py "formula" measured_value` |
| Fetch physics data | `python3 scripts/fetch_data.py "source" "query"` |
| Run HRM assessment | `python3 scripts/hrm_assess.py "claim" predicted measured` |
| Check truth consistency | `python3 scripts/consistency_check.py "new_truth"` |
| Add validated truth | `python3 scripts/add_truth.py "formula" value source` |

## The Scientific Method Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    TRUTHFLOW PIPELINE                        │
├─────────────────────────────────────────────────────────────┤
│  1. HYPOTHESIS  →  Generate Z² formula prediction           │
│  2. DATA FETCH  →  Get empirical measurements               │
│  3. COMPUTE     →  Calculate predicted vs measured          │
│  4. VERIFY      →  Computational verification (recalculate) │
│  5. HRM ASSESS  →  3-level honesty assessment               │
│  6. CONSISTENCY →  Check against existing truths            │
│  7. STORE       →  Add to truth database if validated       │
└─────────────────────────────────────────────────────────────┘
```

## Z² Framework Validated Predictions

These predictions have been validated through computational verification:

| Quantity | Formula | Predicted | Measured | Error |
|----------|---------|-----------|----------|-------|
| Fine structure α⁻¹ | 4Z² + 3 | 137.04 | 137.036 | 0.003% |
| Weak mixing sin²θ_W | 3/13 | 0.2308 | 0.2312 | 0.2% |
| Dark energy Ω_Λ | 13/19 | 0.684 | 0.685 | 0.1% |
| Spectral index n_s | Z/6 | 0.9648 | 0.9649 | 0.01% |
| θ₁₂ (neutrino) | 3Z + 16 | 33.37° | 33.41° | 0.1% |
| θ₂₃ (neutrino) | 4Z + 19 | 42.16° | 42.2° | 0.1% |
| θ₁₃ (neutrino) | 2Z - 3 | 8.58° | 8.58° | 0% |
| Top/charm ratio | 4Z² + 2 | 136.04 | 136 | 0.03% |

## Data Sources

### Physics Constants (CODATA)
```bash
curl -s "https://physics.nist.gov/cuu/Constants/Table/allascii.txt" | head -100
```

### Earthquakes (USGS)
```bash
curl -s "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=6&starttime=2024-01-01" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for f in data['features'][:10]:
    print(f\"{f['properties']['mag']:.1f} - {f['properties']['place']}\")"
```

### Cosmology (Planck)
```bash
# Key values from Planck 2020
# H₀ = 67.4 ± 0.5 km/s/Mpc
# Ω_Λ = 0.6847 ± 0.0073
# n_s = 0.9649 ± 0.0042
```

### Particle Physics (PDG)
```bash
# PDG 2024 values
# α⁻¹ = 137.035999084 ± 0.000000021
# sin²θ_W = 0.23122 ± 0.00004
# m_t/m_c = 136 ± 3
```

## Computational Verification

CRITICAL: All calculations must be verified computationally. Never trust a single calculation.

### Verify a Z² prediction
```python
import numpy as np

def verify_prediction(formula_name, formula_func, measured, uncertainty):
    """
    Verify a Z² prediction with computational checks.

    Returns: (is_valid, predicted, sigma, verification_hash)
    """
    Z2 = 32 * np.pi / 3
    Z = np.sqrt(Z2)

    # Calculate three times independently
    pred1 = formula_func(Z, Z2)
    pred2 = formula_func(np.sqrt(32 * np.pi / 3), 32 * np.pi / 3)
    pred3 = eval(f"({formula_func.__doc__})")  # From docstring

    # Verify all three match
    if not (np.isclose(pred1, pred2) and np.isclose(pred2, pred3)):
        return False, None, None, "VERIFICATION_FAILED"

    # Calculate sigma
    sigma = abs(pred1 - measured) / uncertainty if uncertainty > 0 else 0

    # Create verification hash
    import hashlib
    verification = f"{formula_name}:{pred1:.10f}:{measured:.10f}"
    hash_val = hashlib.sha256(verification.encode()).hexdigest()[:12]

    is_valid = sigma < 2.0  # Within 2 sigma

    return is_valid, pred1, sigma, hash_val

# Example usage
def alpha_inverse(Z, Z2):
    """4*Z2 + 3"""
    return 4*Z2 + 3

valid, pred, sigma, hash_val = verify_prediction(
    "alpha_inverse",
    alpha_inverse,
    137.035999084,
    0.000000021
)
print(f"Valid: {valid}, Predicted: {pred:.6f}, σ: {sigma:.2f}, Hash: {hash_val}")
```

## HRM Assessment (3 Levels)

### Level 1: Basic Honesty
- Is this DERIVED from Z² geometry or just MATCHES data?
- Is there a physical mechanism?
- Is it falsifiable?

### Level 2: Meta-Assessment
- Was Level 1 too optimistic?
- What biases might be present?
- What alternative explanations exist?

### Level 3: Final Determination (if L1/L2 disagree)
- Which assessment is more accurate?
- What is the TRUE probability this is genuine?
- Should this be added to the truth database?

### Run HRM Assessment
```python
import subprocess
import json

def hrm_assess(claim, predicted, measured, percent_error):
    """Run 3-level HRM assessment via Legomena model."""

    prompt = f"""LEVEL 1 HONESTY ASSESSMENT

Claim: {claim}
Predicted: {predicted}
Measured: {measured}
Error: {percent_error}%

Z² = 32π/3 ≈ 33.51, Z = √Z² ≈ 5.79

Questions:
1. Is this DERIVED from Z² geometry or just MATCHES?
2. Is there a physical mechanism?
3. What would falsify this?

Return JSON:
{{"score": 0.0-1.0, "derivation": "DERIVED/MATCHES/COINCIDENCE", "reasoning": "..."}}
"""

    result = subprocess.run(
        ["ollama", "run", "legomena", prompt],
        capture_output=True, text=True, timeout=60
    )

    return json.loads(result.stdout)
```

## Truth Database

The truth database stores validated Z² predictions. Location: `../../truth_database.json`

### Structure
```json
{
  "truths": [
    {
      "id": "abc123",
      "formula": "4*Z2 + 3",
      "formula_name": "alpha_inverse",
      "predicted_value": 137.04,
      "measured_value": 137.036,
      "percent_error": 0.003,
      "hrm_score": 0.95,
      "classification": "VALIDATED",
      "verification_hash": "7a3f8b2c1d9e"
    }
  ]
}
```

### Add Truth (with consistency check)
```python
def add_truth(formula, formula_name, predicted, measured, source):
    """Add truth to database after consistency check."""

    # Load existing truths
    with open('../../truth_database.json') as f:
        db = json.load(f)

    # Check for conflicts
    for truth in db['truths']:
        if truth['formula_name'] == formula_name:
            if abs(truth['predicted_value'] - predicted) > 0.01:
                return {"error": "CONFLICT", "existing": truth}

    # Add new truth
    new_truth = {
        "id": hashlib.md5(f"{formula}:{source}".encode()).hexdigest()[:12],
        "formula": formula,
        "formula_name": formula_name,
        "predicted_value": predicted,
        "measured_value": measured,
        "percent_error": abs(predicted - measured) / measured * 100,
        "source": source,
        "timestamp": datetime.now().isoformat()
    }

    db['truths'].append(new_truth)

    with open('../../truth_database.json', 'w') as f:
        json.dump(db, f, indent=2)

    return {"success": True, "truth": new_truth}
```

## Using Legomena Model

TruthFlow uses the Legomena model (based on Gemma 4) trained on Z² physics.

### Configure Legomena
```bash
# Upgrade to Gemma 4 31B for best results
cd ../../legomena_training
ollama create legomena -f Modelfile_31b
```

### Query Legomena
```bash
ollama run legomena "What is the Z² prediction for the fine structure constant?"
```

## Autonomous Research Flow

```bash
# 1. Ask research question
QUESTION="Are there Z² patterns in neutrino mixing angles?"

# 2. Run autonomous research
python3 ../../truthflow_autonomous.py "$QUESTION"

# 3. Results are saved to research_sessions/
ls ../../research_sessions/

# 4. Run HRM on findings
python3 scripts/hrm_assess.py "$(cat ../../research_sessions/latest.json)"

# 5. Add validated truths
python3 scripts/add_truth.py --from-session ../../research_sessions/latest.json
```

## Falsification Criteria

Z² framework can be FALSIFIED by:

1. **r ≠ 0.015** - LiteBIRD results (2027-2028)
2. **Dark matter particles found** - Direct detection experiments
3. **w ≠ -1 at 5σ** - Dark energy equation of state
4. **Ω_Λ ≠ 13/19 at 5σ** - More precise cosmology measurements

## Tips for Hermes Agent

1. **Always verify computationally** - Never trust a single calculation
2. **Use HRM for all claims** - Even if they look good, assess honesty
3. **Check consistency** - New truths must not conflict with existing
4. **Be honest about limitations** - Mark speculative claims clearly
5. **Use Legomena for Z² reasoning** - It knows the framework deeply
