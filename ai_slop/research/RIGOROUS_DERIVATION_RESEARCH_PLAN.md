# Research Plan: Rigorous Derivation of Spectral Dimension & MOND μ(x)

**Author:** Carl Zimmerman
**Date:** May 2, 2026
**Status:** PLANNING PHASE
**Objective:** Transform conjectures into rigorous derivations

---

## Executive Summary

The v7.0.0 paper addresses two theoretical gaps through the entropy partition principle, but honest assessment reveals the arguments are **motivated conjectures**, not rigorous derivations. This research plan outlines the work required to achieve full theoretical closure.

### Current Gaps

| Gap | Current Status | Required for Closure |
|-----|----------------|---------------------|
| μ(x) = x/(1+x) | Motivated | Fix entropy scaling inconsistency |
| d_s(x) = 2 + μ(x) | Conjectured | Heat kernel derivation + UV fix |

---

## Part 1: The Core Mathematical Inconsistency

### 1.1 The Problem

The paper states two things that contradict each other:

**Statement A (Dimensional Scaling):**
```
S_local ∝ (r/ℓ)³  where r = c²/a
```
This implies: S_local ∝ r³ ∝ (c²/a)³ ∝ a⁻³

**Statement B (Partition Function):**
```
S_local ∝ x = a/a₀
```
This implies: S_local ∝ a

**The inconsistency:** a⁻³ ≠ a

The derivation jumps from dimensional scaling to the partition function without showing how r³ becomes linear in x. This is the core logical gap.

### 1.2 Why This Matters

If we can't derive S_local ∝ x from first principles, then μ(x) = x/(1+x) is an **assumption**, not a derivation. The entropy partition "derivation" would be circular reasoning.

---

## Part 2: Research Tasks

### TASK 1: Resolve Entropy Scaling Inconsistency
**Priority:** CRITICAL
**Difficulty:** Medium
**Timeline:** 2-4 weeks

#### 1.1 Objective
Derive S_local ∝ x from first principles, or find the correct physical argument.

#### 1.2 Approach A: Holographic Bit Counting (Verlinde-style)

Following Verlinde (2011), count information bits on holographic screen:

```
At acceleration a, the Unruh temperature is:
T_U = ℏa/(2πck_B)

The number of bits on a screen at distance r = c²/a:
N = A/(4ℓ_P²) where A = 4πr²

Substituting r = c²/a:
N ∝ (c²/a)² = c⁴/a²

Energy on screen: E = ½Nk_B T = ½N × ℏa/(2πc)
```

**Problem:** This gives N ∝ a⁻², not N ∝ a. Need to find where linear scaling emerges.

#### 1.3 Approach B: Padmanabhan Equipartition

From Padmanabhan (2010), the difference between surface and bulk degrees of freedom drives cosmic acceleration:

```
dV/dt ∝ (N_surface - N_bulk)
```

**Investigation:** Can we show that in the MOND regime:
```
N_bulk/N_surface = x/(1+x) where x = a/a₀
```

This would directly give μ(x) as a ratio of degrees of freedom.

#### 1.4 Approach C: Information-Theoretic Argument

Consider entropy accessible to an accelerated observer:

```
At acceleration a, the Rindler horizon is at distance d = c²/a
Information causally accessible: S_accessible ∝ A_horizon/4

As a → 0 (low acceleration), d → ∞, approaching cosmological horizon
As a → ∞ (high acceleration), d → 0, purely local physics
```

**Key insight needed:** Why does the *ratio* of local to total entropy scale as x/(1+x)?

#### 1.5 Deliverables
- [ ] Mathematical derivation showing S_local/S_total = x/(1+x)
- [ ] Or: acknowledgment that this is a physical postulate, with justification
- [ ] Update paper Section 7.2 with rigorous argument

---

### TASK 2: Explicit Heat Kernel Calculation
**Priority:** HIGH
**Difficulty:** Hard
**Timeline:** 4-8 weeks

#### 2.1 Objective
Compute spectral dimension on Z² lattice from first principles and verify d_s: 3 → 2.

#### 2.2 Mathematical Setup

**Step 1: Define the Lattice Laplacian**

On a cubic lattice with spacing a, the standard Laplacian is:
```
(Lψ)_n = (1/a²) Σ_μ [ψ_{n+μ} + ψ_{n-μ} - 2ψ_n]
```

**Step 2: Add Harper Modification**

The Harper model adds a phase to hopping terms:
```
(L_Harper ψ)_n = Σ_μ [e^{2πiαn_μ} ψ_{n+μ} + e^{-2πiαn_μ} ψ_{n-μ} - 2ψ_n]
```

With Z² framework: α = 1/Z² ≈ 0.0298

**Step 3: Compute Heat Kernel**

```
K(t) = Tr(e^{-tL}) = Σ_λ e^{-tλ}
```

where {λ} are eigenvalues of L.

**Step 4: Extract Spectral Dimension**

```
d_s(t) = -2 × d(log K)/d(log t)
```

For standard lattice: d_s = 3 (constant)
With Harper modification: d_s should flow

#### 2.3 Numerical Implementation

```python
# Pseudocode for spectral dimension calculation

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

def build_harper_laplacian(L, alpha):
    """Build Harper-modified Laplacian on L×L×L lattice"""
    N = L**3
    # Construct sparse matrix with Harper phases
    # ...
    return laplacian

def compute_heat_kernel(eigenvalues, t_values):
    """K(t) = Σ exp(-λt)"""
    K = np.array([np.sum(np.exp(-eigenvalues * t)) for t in t_values])
    return K

def spectral_dimension(K, t_values):
    """d_s = -2 d(log K)/d(log t)"""
    log_K = np.log(K)
    log_t = np.log(t_values)
    d_s = -2 * np.gradient(log_K, log_t)
    return d_s

# Run for various lattice sizes
for L in [10, 20, 50, 100]:
    laplacian = build_harper_laplacian(L, alpha=1/33.51)
    eigenvalues = compute_eigenvalues(laplacian)
    K = compute_heat_kernel(eigenvalues, t_values)
    d_s = spectral_dimension(K, t_values)

    # Check limits
    print(f"L={L}: d_s(t→∞)={d_s[-1]:.2f}, d_s(t→0)={d_s[0]:.2f}")
```

#### 2.4 Expected Results

| Regime | t value | Expected d_s | Current result |
|--------|---------|--------------|----------------|
| IR | t → ∞ | 3.0 | 2.8-3.0 ✓ |
| UV | t → 0 | 2.0 | 1.2-1.5 ✗ |

#### 2.5 Deliverables
- [ ] Working Python/Julia code for Harper lattice Laplacian
- [ ] Eigenvalue computation for L = 10, 20, 50, 100
- [ ] Heat kernel and spectral dimension plots
- [ ] Finite-size scaling analysis
- [ ] Publication-ready figures

---

### TASK 3: Diagnose UV Discrepancy
**Priority:** HIGH
**Difficulty:** Medium
**Timeline:** 2-4 weeks (parallel with Task 2)

#### 3.1 The Problem

Current numerics show d_s → 1.2-1.5 in UV, but theory predicts d_s → 2.

This 25-40% discrepancy could mean:
1. The Harper modification is wrong
2. Finite-size effects
3. The conjecture is wrong
4. Numerical errors

#### 3.2 Investigation Plan

**Test A: Vary Harper coupling α**
```
α_test = [0, 0.01, 0.02, 0.0298, 0.04, 0.05, 0.1]
For each α:
    Compute d_s(t→0)
    Plot d_s_UV vs α
```

Question: Is there a value of α that gives d_s → 2?

**Test B: Finite-size scaling**
```
L_values = [10, 20, 40, 80, 160]
For each L:
    Compute d_s(t→0)
    Extrapolate to L → ∞
```

Question: Does d_s_UV converge to 2 as L → ∞?

**Test C: Boundary conditions**
```
BC_types = ['periodic', 'open', 'antiperiodic']
For each BC:
    Compute d_s(t→0)
```

Question: Do boundary conditions affect UV limit?

**Test D: Alternative modifications**

Try other lattice modifications that might give d_s → 2:
- Hofstadter butterfly at different flux
- Random disorder (Anderson model)
- Curved lattice embedding

#### 3.3 Decision Tree

```
If d_s_UV → 2 for some α:
    → Find physical justification for that α
    → Update Z² prediction

If d_s_UV → 2 only as L → ∞:
    → Current results are finite-size artifacts
    → Report extrapolated value

If d_s_UV ≠ 2 for any α, L, BC:
    → The conjecture d_s = 2 + μ(x) is WRONG
    → Find correct formula from numerics
    → Or: abandon spectral dimension claim
```

#### 3.4 Deliverables
- [ ] Systematic study of α dependence
- [ ] Finite-size scaling analysis
- [ ] Boundary condition comparison
- [ ] Clear conclusion: Is d_s → 2 achievable?

---

### TASK 4: Derive the Interpolation Formula
**Priority:** MEDIUM
**Difficulty:** Hard
**Timeline:** 4-6 weeks

#### 4.1 Objective

Show WHY spectral dimension should interpolate as:
```
d_s(x) = d_horizon + (d_bulk - d_horizon) × μ(x)
       = 2 + 1 × μ(x)
       = 2 + μ(x)
```

Currently this is assumed, not derived.

#### 4.2 Physical Motivation

The spectral dimension measures return probability of a random walker:
```
P(t) ~ t^{-d_s/2}
```

If physics transitions from bulk (3D) to horizon (2D) as acceleration decreases, the return probability should interpolate between these regimes.

**Key question:** Why is the interpolation function the same as the MOND interpolation μ(x)?

#### 4.3 Possible Derivation Strategy

**Step 1:** Consider a random walk in a space where effective dimension varies with position/scale.

**Step 2:** At high acceleration (x >> 1), walker explores 3D bulk:
```
P_bulk(t) ~ t^{-3/2}
```

**Step 3:** At low acceleration (x << 1), walker is confined to 2D horizon:
```
P_horizon(t) ~ t^{-1}
```

**Step 4:** At intermediate x, walker spends fraction μ(x) in bulk, fraction (1-μ(x)) on horizon:
```
P(t) = μ(x) × P_bulk(t) + (1-μ(x)) × P_horizon(t)
```

**Step 5:** Show this leads to effective d_s = 2 + μ(x).

#### 4.4 Mathematical Challenge

The step 4 → step 5 connection is not obvious. Need to show:
```
P(t) = μ × t^{-3/2} + (1-μ) × t^{-1}

implies

d_s = 2 + μ
```

This may require careful analysis of the scaling behavior.

#### 4.5 Deliverables
- [ ] Physical argument connecting entropy partition to spectral dimension
- [ ] Mathematical derivation (if possible)
- [ ] Or: acknowledgment that connection is conjectural

---

### TASK 5: Observational Validation of μ(x)
**Priority:** MEDIUM
**Difficulty:** Medium
**Timeline:** 2-4 weeks

#### 5.1 Objective

Test whether μ(x) = x/(1+x) fits galaxy rotation curves better than alternatives.

#### 5.2 Data Source

**SPARC Database:**
- 175 galaxies with high-quality rotation curves
- Spitzer photometry for mass models
- Available at: http://astroweb.cwru.edu/SPARC/

#### 5.3 Analysis Plan

**Step 1:** For each galaxy, compute:
- Observed rotation velocity v_obs(r)
- Baryonic prediction v_bar(r) from mass model
- Newtonian acceleration a_N = v_bar²/r

**Step 2:** Apply MOND with different μ(x) forms:
```
a = a_N × ν(a_N/a₀)  where ν = 1/μ

Forms to test:
- Simple: μ = x/(1+x)
- Standard: μ = x/√(1+x²)
- RAR: μ = 1 - exp(-√x)
```

**Step 3:** Compute χ² for each form:
```
χ² = Σ [(v_obs - v_pred)² / σ²]
```

**Step 4:** Compare using Bayesian Information Criterion:
```
BIC = χ² + k × ln(n)
```
where k = number of parameters, n = number of data points.

#### 5.4 Key Test: Deep MOND Regime

The forms differ most at low x (deep MOND):
```
x = 0.1:
  Simple: μ = 0.091
  Standard: μ = 0.0995
  RAR: μ = 0.147

x = 0.01:
  Simple: μ = 0.0099
  Standard: μ = 0.01
  RAR: μ = 0.039
```

Focus on low surface brightness galaxies where x << 1.

#### 5.5 Prediction

If Z² framework is correct:
- Simple form should have lowest χ² in deep MOND regime
- Difference should be statistically significant

#### 5.6 Deliverables
- [ ] SPARC data analysis pipeline
- [ ] Rotation curve fits for all three μ(x) forms
- [ ] Statistical comparison (χ², BIC, evidence ratios)
- [ ] Publication-ready figures and tables

---

## Part 3: Timeline and Dependencies

```
Week 1-2:   Task 1 (Entropy scaling) - CRITICAL PATH
            Task 3 (UV diagnosis) - parallel start

Week 3-4:   Task 1 completion
            Task 2 (Heat kernel) - begin
            Task 3 completion

Week 5-6:   Task 2 continuation
            Task 5 (SPARC analysis) - begin

Week 7-8:   Task 2 completion
            Task 4 (Interpolation derivation) - begin
            Task 5 completion

Week 9-10:  Task 4 completion
            Integration and paper revision

Week 11-12: Paper update to v7.1.0 with rigorous derivations
```

### Dependency Graph

```
Task 1 (Entropy) ──────┬──→ Task 4 (Interpolation)
                       │
Task 2 (Heat kernel) ──┼──→ Paper v7.1.0
                       │
Task 3 (UV diagnosis) ─┘

Task 5 (SPARC) ────────────→ Observational validation
```

---

## Part 4: Success Criteria

### For μ(x) = x/(1+x)

| Criterion | Threshold | Method |
|-----------|-----------|--------|
| Entropy scaling derived | Mathematical proof | Task 1 |
| SPARC fit | χ² lower than alternatives | Task 5 |
| Physical motivation | Clear argument | Task 1 |

### For d_s(x) = 2 + μ(x)

| Criterion | Threshold | Method |
|-----------|-----------|--------|
| UV limit | d_s(t→0) = 2.0 ± 0.1 | Task 2, 3 |
| IR limit | d_s(t→∞) = 3.0 ± 0.1 | Task 2 |
| Derivation | Mathematical or physical | Task 4 |

### Overall

| Criterion | Current | Target |
|-----------|---------|--------|
| μ(x) status | Motivated | Derived |
| d_s(x) status | Conjectured | Derived or Falsified |
| UV endpoint | 1.2-1.5 | 2.0 ± 0.1 |

---

## Part 5: Possible Outcomes

### Outcome A: Full Success
- Entropy scaling derived → μ(x) is proven
- Heat kernel gives d_s → 2 → spectral dimension is proven
- SPARC data favors simple form → observational confirmation

**Result:** Paper v7.1.0 with "DERIVED" status for both gaps

### Outcome B: Partial Success
- Entropy scaling remains a postulate (physically motivated)
- Spectral dimension direction confirmed, UV endpoint close but not exact
- SPARC data consistent but not decisive

**Result:** Paper v7.1.0 with honest caveats, "MOTIVATED" status

### Outcome C: Falsification
- Cannot derive entropy scaling
- UV endpoint ≠ 2 for any parameters
- SPARC data disfavors simple form

**Result:** Retract spectral dimension conjecture, revise μ(x) claim

### Outcome D: New Discovery
- UV endpoint is not 2 but some other value (e.g., 1.5)
- This leads to modified prediction
- New physics insight

**Result:** Paper v7.1.0 with revised predictions

---

## Part 6: Resources Needed

### Computational
- Python with NumPy, SciPy, matplotlib
- Access to computing cluster for large lattice calculations (L > 100)
- ~100 CPU-hours for full parameter sweep

### Data
- SPARC database (free, publicly available)
- CDT spectral dimension data for comparison (from literature)

### Literature
- Verlinde (2011): Entropic gravity
- Padmanabhan (2010): Holographic equipartition
- Ambjørn & Loll (2024): CDT spectral dimension
- McGaugh et al. (2016): SPARC database paper
- Milgrom (2020): MOND-cosmology connection

---

## Part 7: Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Cannot derive entropy scaling | 40% | High | Accept as postulate with justification |
| UV endpoint ≠ 2 | 50% | High | Revise prediction or retract claim |
| SPARC inconclusive | 30% | Medium | Focus on deep MOND subsample |
| Computational limits | 20% | Medium | Use sparse matrix methods |

---

## Conclusion

This research plan provides a path from "motivated conjecture" to "rigorous derivation" for the spectral dimension and MOND μ(x) claims. The key tasks are:

1. **Critical:** Resolve entropy scaling inconsistency
2. **High:** Verify spectral dimension via heat kernel
3. **High:** Diagnose and fix UV discrepancy
4. **Medium:** Derive interpolation formula
5. **Medium:** Validate μ(x) with SPARC data

Estimated timeline: 10-12 weeks for complete analysis.

The honest approach is to pursue these tasks and accept whatever outcome emerges - whether full validation, partial success, or falsification.

---

*Research Plan: Rigorous Derivation of Spectral Dimension & MOND μ(x)*
*Z² Framework - May 2026*
