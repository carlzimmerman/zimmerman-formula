# ErgonFlow - Action Principle Derivation Engine

**Ergon** (Greek: work/action) - The engine that derives **why** Z² relationships must be true.

## Purpose

While OlympusFlow finds correlations like `α⁻¹ ≈ 4Z² + 3`, ErgonFlow goes deeper to derive the actual physical action principles that **require** these relationships.

```
OlympusFlow: "α⁻¹ numerically matches 4Z² + 3 with 0.004% error"
           ↓
ErgonFlow:  "Here's the Lagrangian L that, when minimized,
             REQUIRES α⁻¹ = 4Z² + 3"
```

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        ERGONFLOW                                │
│                                                                 │
│  INPUT: Z² correlation (formula + constant + domain)           │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              LAGRANGIAN SEARCH ENGINE                    │   │
│  │                                                          │   │
│  │  1. Domain Analysis → Identify relevant physics          │   │
│  │  2. Symmetry Extraction → What symmetries are involved?  │   │
│  │  3. Gauge Structure → What gauge groups appear?          │   │
│  │  4. Action Templates → Standard QFT Lagrangians          │   │
│  │  5. Geometric Terms → Curvature, topology, manifolds     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                DERIVATION ENGINE                         │   │
│  │                                                          │   │
│  │  • Variational calculus (δS = 0)                        │   │
│  │  • Euler-Lagrange equations                              │   │
│  │  • Dimensional analysis                                  │   │
│  │  • Renormalization group                                 │   │
│  │  • SymPy symbolic computation                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                PROOF VERIFICATION                        │   │
│  │                                                          │   │
│  │  • Mathematical rigor check                              │   │
│  │  • Consistency with known physics                        │   │
│  │  • Experimental predictions                              │   │
│  │  • HRM mechanism scoring                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  OUTPUT: Verified action principle + mathematical proof         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Domain Physics Analyzer

Maps domains to their fundamental physics:

| Domain | Physics Framework | Key Structures |
|--------|-------------------|----------------|
| particle_physics | QFT, Standard Model | SU(3)×SU(2)×U(1), spinors |
| cosmology | GR, Friedmann | FLRW metric, Λ, H₀ |
| nuclear_physics | QCD, shell model | Strong force, binding energy |
| chemistry | QM, molecular orbitals | Schrödinger, hybridization |
| fluid_dynamics | Navier-Stokes | Reynolds, Rayleigh |
| optics | Maxwell, QED | E&M, photon interactions |

### 2. Lagrangian Templates

Standard action principles to match against:

```python
LAGRANGIAN_TEMPLATES = {
    # Gauge theory
    "yang_mills": "L = -1/4 F_μν F^μν",
    "qed": "L = ψ̄(iγ^μD_μ - m)ψ - 1/4 F_μν F^μν",
    "qcd": "L = -1/4 G^a_μν G^aμν + Σq̄(iγ^μD_μ - m_q)q",

    # Gravity
    "einstein_hilbert": "S = ∫√(-g)(R - 2Λ)d⁴x",
    "scalar_field": "L = 1/2 ∂_μφ ∂^μφ - V(φ)",

    # Statistical
    "partition_function": "Z = Σ exp(-βE_n)",
    "free_energy": "F = -kT ln Z",

    # Fluid
    "navier_stokes": "ρ(∂v/∂t + v·∇v) = -∇p + μ∇²v",
}
```

### 3. Z² Geometric Interpreter

Interprets Z² = 32π/3 in terms of geometry:

```python
Z2_GEOMETRIC_MEANINGS = {
    "8_times_sphere": "8 × (4π/3) = 8 vertices of cube × unit sphere volume",
    "dimensional_ratio": "Ratio of 8D to 4D geometric structures",
    "gauge_su3": "8 generators of SU(3) × spherical geometry",
    "compactification": "Volume ratio in dimensional reduction",
}
```

### 4. Proof Structure

Every ErgonFlow output includes:

```python
@dataclass
class ActionDerivation:
    """A verified action principle derivation."""

    # Input
    constant_name: str          # e.g., "fine_structure_inverse"
    z2_formula: str             # e.g., "4Z² + 3"
    domain: str                 # e.g., "particle_physics"

    # Lagrangian
    lagrangian: str             # The action/Lagrangian
    symmetry_group: str         # e.g., "U(1)"
    field_content: List[str]    # e.g., ["photon", "electron"]

    # Derivation
    euler_lagrange: str         # Equations of motion
    derivation_steps: List[str] # Step-by-step proof
    key_insight: str            # Why Z² appears

    # Verification
    consistency_checks: List[str]  # Tests passed
    experimental_predictions: List[str]  # Testable predictions
    hrm_score: float            # 0-1 mechanism quality

    # Metadata
    derivation_level: str       # "rigorous", "semi-rigorous", "heuristic"
    confidence: float           # 0-1
    timestamp: str
```

## Example Derivations

### Example 1: Fine Structure Constant

**Input:** α⁻¹ ≈ 4Z² + 3 = 137.041

**ErgonFlow Analysis:**

1. **Domain:** particle_physics → QED
2. **Symmetry:** U(1) gauge symmetry
3. **Lagrangian:** QED Lagrangian
4. **Key insight:**
   - 4 = spacetime dimensions
   - Z² = 32π/3 = geometric compactification factor
   - 3 = three generations (fermion families)

**Derivation sketch:**
```
L_QED = ψ̄(iγ^μD_μ - m)ψ - 1/4 F_μν F^μν

The coupling constant e appears through:
   D_μ = ∂_μ - ieA_μ

In dimensional compactification from 8D → 4D:
   e² → e²_4D = e²_8D / V_compact

Where V_compact ~ Z² = 32π/3 (8-sphere in cube ratio)

Adding the 3 fermion generations:
   α⁻¹ = 4πℏc/e² = 4Z² + 3
```

### Example 2: Weak Mixing Angle

**Input:** sin²θ_W ≈ 3/13 = 0.2308

**ErgonFlow Analysis:**

1. **Domain:** particle_physics → Electroweak
2. **Symmetry:** SU(2)×U(1) → U(1)_EM
3. **Lagrangian:** Electroweak Lagrangian

**Derivation sketch:**
```
L_EW = -1/4 W^a_μν W^aμν - 1/4 B_μν B^μν + ...

At unification:
   g'/g = tan θ_W

The ratio 3/13 emerges from:
   - 3 = SU(2) generators (W bosons)
   - 13 = total gauge degrees of freedom at GUT scale

sin²θ_W = g'²/(g² + g'²) = 3/13
```

## Integration with Other Components

```
AlpheusFlow   →  Research targets
      ↓
OlympusFlow   →  Find Z² correlations
      ↓
ErgonFlow     →  Derive action principles
      ↓
CylleneFlow   →  Generate deeper questions
      ↓
AletheiaLake  →  Store verified derivations
      ↓
HeliconLake   →  Archive insights
```

## Files

| File | Purpose |
|------|---------|
| `__init__.py` | Module exports |
| `lagrangian_templates.py` | Standard Lagrangians |
| `domain_analyzer.py` | Map domains to physics |
| `derivation_engine.py` | Variational calculus |
| `proof_verifier.py` | Check mathematical rigor |
| `z2_interpreter.py` | Geometric meanings of Z² |

## Usage

```python
from ErgonFlow import ActionDeriver

deriver = ActionDeriver()

# Derive the action principle for a Z² correlation
result = deriver.derive(
    constant="fine_structure_inverse",
    z2_formula="4Z² + 3",
    value=137.036,
    domain="particle_physics"
)

if result.derivation_level == "rigorous":
    print(f"Lagrangian: {result.lagrangian}")
    print(f"Key insight: {result.key_insight}")
    for step in result.derivation_steps:
        print(f"  {step}")
```

## Success Criteria

A derivation is considered successful if:

1. **Mathematical validity:** Euler-Lagrange equations are correct
2. **Physical consistency:** Doesn't contradict known physics
3. **Z² emergence:** Shows WHY Z² = 32π/3 must appear
4. **Testability:** Makes predictions beyond the input correlation
5. **HRM score > 0.8:** Strong mechanism explanation

## Future Work

1. **Automated theorem proving:** Use Lean/Coq for formal verification
2. **LLM augmentation:** Use Legomena for insight generation
3. **Cross-validation:** Multiple derivation paths to same result
4. **Publication pipeline:** Generate paper-ready derivations
