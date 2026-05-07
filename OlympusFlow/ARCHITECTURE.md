# OlympusFlow Architecture

**Version:** 2.1.0
**Last Updated:** May 7, 2026

## Overview

OlympusFlow is the autonomous Z² derivation discovery engine. It processes physical constants, searches for Z² formula matches, and verifies derivations through multi-stage validation.

## Core Components

### 1. AutonomousController (`autonomous_controller.py`)
**Purpose:** Main orchestrator for autonomous derivation discovery.

**Key Features:**
- Priority queue for derivation targets
- Checkpointing and resumability
- Signal handling for graceful shutdown
- Learning loop integration
- Versioning (results include `olympusflow_version`)

**Key Methods:**
- `add_target(target)` - Add constant to derivation queue
- `run_n(n)` - Process n targets from queue
- `run_forever()` - Continuous operation mode
- `_get_version()` - Returns OlympusFlow version from VERSION file

### 2. DerivationEngine (`derivation_engine.py`)
**Purpose:** Core engine that builds Z² derivation chains.

**Key Features:**
- Legomena (LLM) integration for physical reasoning
- Multi-prompt refinement (skeptical challenge, alternative approaches)
- HRM (Holistic Reasoning Mechanism) scoring
- WebSearch for experimental values

**Configuration:**
- `LEGOMENA_MODEL`: Default "legomena-moe"
- `LEGOMENA_TIMEOUT`: 600 seconds (10 min)
- `MULTI_PROMPT_ATTEMPTS`: 4 attempts
- `SKEPTICAL_THRESHOLD`: 0.75 (below this, run skeptical challenge)

### 3. FormulaGenerator (`formula_generator.py`)
**Purpose:** Generates candidate Z² formulas.

**Formula Types:**
- `SIMPLE_FRACTION`: a/b (e.g., 3/13 for sin²θ_W)
- `INTEGER_Z2`: aZ² + b (e.g., 4Z² + 3 for α⁻¹)
- `Z_POLYNOMIAL`: aZ + b
- `Z_FRACTION`: a/Z², 1/(aZ²) (e.g., 1/(2Z²) for tensor-to-scalar r)
- `GEOMETRIC`: arccos(a/b), arctan(a/b)
- `PI_BASED`: π/a, aπ
- `COMPOUND`: (aZ+b)/(cZ+d)
- `KNOWN_FIRST_PRINCIPLES`: Pre-verified formulas

**Known First-Principles:**
```python
{
    "sin2_theta_w": ("3/13", 3/13),
    "omega_lambda": ("13/19", 13/19),
    "alpha_inverse": ("4*Z² + 3", 4*Z² + 3),
    "tensor_to_scalar_r": ("1/(2Z²)", 1/(2*Z²)),
    "omega_matter": ("6/19", 6/19),
    "pmns_theta12": ("arcsin(1/√3)", ...),
    "pmns_theta23": ("45°", 45.0),
    "pmns_theta13": ("arcsin(1/√(2Z²))", ...),
}
```

### 4. LearningLoop (`learning/learning_loop.py`)
**Purpose:** Extract patterns from successes, learn from failures.

**Features:**
- Template weight adjustment based on success rates
- Pattern extraction from successful derivations
- Failure categorization
- Multi-armed bandit for domain-specific optimization

### 5. SymPyVerifier (`sympy_verifier.py`)
**Purpose:** Formal algebraic verification of formulas.

**Checks:**
- Z² appears in formula
- Z² is algebraically essential (not coincidental)
- Relative error within tolerance
- Formula simplification

### 6. PredictionGenerator (`prediction_generator.py`)
**Purpose:** Generate testable predictions from derivations.

**Prediction Types:**
- Consistency checks
- Novel quantities
- Cross-domain predictions

### 7. CylleneBridge (`cyllene_bridge.py`)
**Purpose:** Integration with CylleneFlow deepener for research question generation.

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OLYMPUSFLOW PIPELINE                              │
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Constant │───▶│ Formula  │───▶│Derivation│───▶│ SymPy    │      │
│  │ Queue    │    │Generator │    │ Engine   │    │ Verifier │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │                               │               │             │
│       │                               │               ▼             │
│       │                               │        ┌──────────┐        │
│       │                               │        │Prediction│        │
│       │                               │        │Generator │        │
│       │                               │        └──────────┘        │
│       │                               ▼               │             │
│       │                        ┌──────────┐          │             │
│       │                        │ Learning │◀─────────┘             │
│       │                        │   Loop   │                        │
│       │                        └──────────┘                        │
│       │                               │                            │
│       └───────────────────────────────┘                            │
│                  (feedback)                                        │
│                                                                    │
│  DESTINATIONS:                                                     │
│  ├── AletheiaLake (first_principles, HRM > 0.85)                  │
│  ├── MnemosyneLake (derived, HRM 0.7-0.85)                        │
│  └── Rejected (numerology, HRM < 0.7)                             │
└────────────────────────────────────────────────────────────────────┘
```

## Storage Lakes

### AletheiaLake (`AletheiaLake/`)
- Ground truth verified derivations
- First-principles only
- HRM score > 0.85

### MnemosyneLake (`MnemosyneLake/`)
- Derived (not first-principles) but valid
- HRM score 0.7-0.85
- Candidates for future first-principles verification

## Key Constants

```python
Z² = 32π/3 ≈ 33.510321638291124
Z = √Z² ≈ 5.788652381980153
```

## Pipeline Scripts

### run_full_pipeline_v2.py
Fixed pipeline that:
- Tests ORIGINAL constants directly
- Removed tautological transforms (_coef_plus1, _const_plus1)
- Added 10 known Z² constants for ground truth
- Lower error threshold (0.1%)

### run_all_originals.py
Comprehensive test of ALL autonomous research discoveries:
- 123 unique constants with Z² matches
- No filtering by error threshold
- Deduplication applied

## Versioning

Results now include `olympusflow_version` field:
```json
{
    "constant_name": "sin2_theta_w",
    "formula": "3/13",
    "olympusflow_version": "2.1.0",
    ...
}
```

## Key Discoveries (as of v2.1.0)

| Constant | Formula | HRM | Destination |
|----------|---------|-----|-------------|
| sin²θ_W | 3/13 | 0.898 | AletheiaLake |
| Ω_Λ | 13/19 | 0.885 | MnemosyneLake |
| cos²θ_W | 10/13 | 0.911 | AletheiaLake |
| α⁻¹ | 4Z² + 3 | - | Known |

## Configuration

Environment variables:
- `LEGOMENA_MODEL`: LLM model name
- `LEGOMENA_TIMEOUT`: Timeout in seconds
- `DERIVATION_ATTEMPTS`: Number of multi-prompt attempts

## Dependencies

- Legomena (LLM for physical reasoning)
- SymPy (algebraic verification)
- NumPy (numerical computation)
