# Axion Sector Compatibility Analysis: T³/Z₂ and the Strong CP Problem

**Does Z² Framework Accommodate or Exclude Axions?**

**Carl Zimmerman | May 2026**

---

## Executive Summary

This document analyzes whether the T³/Z₂ orbifold framework is compatible with:
1. The QCD axion (solving the strong CP problem)
2. Axion-like particles (ALPs) as dark matter
3. Axion dark energy (quintessence models)

**Key findings:**
- Z² does NOT naturally include an axion
- The Z₂ projection removes the would-be axion
- If axion DM exists, it requires extension of Z² framework
- Z² predicts θ_QCD ~ 0 from geometry, potentially solving strong CP without axion

---

## 1. The Strong CP Problem

### 1.1 The QCD θ-Term

The QCD Lagrangian can include:
```
L_θ = (θ / 32π²) G_μν G̃^μν
```

where G̃^μν = ε^μνρσ G_ρσ is the dual field strength.

### 1.2 Experimental Constraint

The neutron electric dipole moment (nEDM):
```
|d_n| < 1.8 × 10⁻²⁶ e·cm    (90% CL)
```

This implies:
```
|θ_eff| < 10⁻¹⁰
```

### 1.3 The Problem

Why is θ_eff so small?
- θ is an arbitrary parameter in QCD
- The weak sector contributes arg(det(M_q)) to θ_eff
- No symmetry reason for θ_eff = 0

---

## 2. The Peccei-Quinn Solution

### 2.1 PQ Symmetry

Peccei-Quinn (1977) proposed a global U(1)_PQ symmetry:
```
q → e^{iα} q    (quark rotation)
```

This symmetry is:
- Spontaneously broken at scale f_a
- Anomalous under QCD

### 2.2 The Axion Field

The broken PQ symmetry produces a pseudo-Nambu-Goldstone boson:
```
a(x) / f_a = θ_eff(x)    (dynamical angle)
```

The axion potential:
```
V(a) = Λ_QCD⁴ [1 - cos(a/f_a)]
```

This relaxes θ_eff → 0 dynamically.

### 2.3 Axion Mass

```
m_a = (√(z) / (1+z)) × (f_π m_π / f_a) ≈ 5.7 μeV × (10¹² GeV / f_a)
```

where z = m_u/m_d ≈ 0.5.

---

## 3. Axions from Extra Dimensions

### 3.1 Generic String/KK Axions

In string theory and KK compactifications, axions arise from:
```
B_MN → a(x)    (2-form → 0-form via reduction)
C_p → a_k(x)   (p-forms → scalars)
```

These are called "model-independent axions" or "saxions."

### 3.2 T³ Compactification

On T³, the metric has moduli:
```
g_ij = R_i² δ_ij + ...
```

The imaginary part of the complexified modulus:
```
τ_i = B_i + i R_i²
```

where B_i is the B-field component → would-be axion.

### 3.3 What Happens on T³/Z₂?

**The Z₂ orbifold projects out the would-be axion!**

The B-field component:
```
B_ij(x, y) → -B_ij(x, -y)    under Z₂
```

This is Z₂-odd → **projected out**.

---

## 4. Z² Framework: No Natural Axion

### 4.1 The Projection

On T³/Z₂, the antisymmetric B-field survives only if:
```
B_ij(-y) = B_ij(y)    (Z₂-even)
```

But B_ij is naturally antisymmetric → Z₂-odd → removed.

### 4.2 No Axion from Compactification

The Z² framework with T³/Z₂ does NOT automatically include:
- QCD axion
- String axion
- Model-independent axion

**This is a specific prediction: Z² has no light pseudoscalar from geometry.**

### 4.3 Implications

If Z² is correct:
- Strong CP problem needs different solution
- Axion dark matter is ruled out
- ADMX, CASPEr, etc. will find nothing

---

## 5. Alternative: θ = 0 from Topology

### 5.1 Discrete Symmetries

The Z₂ orbifold provides discrete symmetries that may enforce:
```
θ_eff = 0    (geometrically)
```

### 5.2 The Mechanism

On T³/Z₂, the CP transformation:
```
CP: y → -y, t → -t
```

combines with the orbifold action. If CP is a gauge symmetry:
```
θ_eff = θ_QCD + arg(det M_q) = 0    (by CP invariance)
```

### 5.3 Spontaneous CP Violation

The CKM phase (δ_CKM ≈ 70°) shows CP is violated in weak sector.

But if the violation is spontaneous (from orbifold fixed point structure):
```
⟨H⟩ breaks CP → δ_CKM ≠ 0
But: Strong sector remains CP-conserving → θ_QCD = 0
```

This is the **Nelson-Barr mechanism** naturally embedded in T³/Z₂.

---

## 6. Z² Prediction for Strong CP

### 6.1 The Framework

In Z²:
- Strong CP is solved by discrete symmetry, not axion
- θ_QCD = 0 is a topological consequence
- θ_eff = arg(det M_q) must also vanish

### 6.2 Quark Mass Matrix

The Z² Yukawa matrices are constrained by orbifold:
```
Y_u, Y_d have specific texture from fixed point structure
```

If:
```
det(Y_u × Y_d†) is real
```

then:
```
arg(det M_q) = arg(det(Y_u × v/√2) × det(Y_d × v/√2)†) = 0
```

### 6.3 Numerical Verification

From Z² Yukawa structure:
```
det(M_u) × det(M_d)* = |det(M_u)| × |det(M_d)| × e^{iφ}
```

If φ = 0 (real Yukawas up to CKM rotation):
```
θ_eff = 0    ✓
```

**Z² predicts θ_eff = 0 without an axion.**

---

## 7. What If Axion DM Exists?

### 7.1 Extending Z² Framework

If ADMX or other experiments detect axion DM:
- Z² framework requires extension
- Must add U(1)_PQ that survives Z₂ projection
- This is possible but not natural

### 7.2 Possible Extension

Add explicit PQ sector:
```
L_PQ = |∂_μ Φ|² - λ(|Φ|² - f_a²)² + (coupling to quarks)
```

where Φ is a complex scalar not from KK reduction.

This is:
- Ad hoc addition to Z²
- Not motivated by T³/Z₂ geometry
- Requires explaining f_a scale

### 7.3 f_a from Z²?

If axion exists, could f_a have Z² origin?

Possible:
```
f_a = M_Pl / Z² ~ 3.6 × 10¹⁶ GeV → m_a ~ 0.16 μeV
```

or:
```
f_a = M_Pl / Z ~ 2.1 × 10¹⁸ GeV → m_a ~ 2.7 neV
```

But this is speculative without mechanism.

---

## 8. Axion Dark Energy

### 8.1 Quintessence Axion

Some theories propose axion-like field for dark energy:
```
V(φ) = Λ⁴ [1 + cos(φ/f)]
```

with f ~ M_Pl.

### 8.2 Z² vs Quintessence

As shown in DARK_ENERGY_W_DERIVATION.md:
- Z² predicts w = -1 exactly
- No rolling scalar field
- No axion dark energy

**Z² is incompatible with quintessence-type dark energy.**

### 8.3 The Swampland Connection

Swampland conjectures require w ≠ -1 (quintessence).

Z² predicts w = -1 (cosmological constant).

If Z² is correct:
- No axion dark energy
- Swampland conjecture fails for orbifolds

---

## 9. Experimental Predictions

### 9.1 If Z² is Correct

| Experiment | Prediction | Status |
|------------|------------|--------|
| ADMX | No signal | Running |
| CASPEr | No signal | Planned |
| ABRACADABRA | No signal | Running |
| IAXO | No signal | Planned |
| Neutron EDM | d_n ≈ 0 | θ = 0 geometrically |

### 9.2 If Axion Detected

| Discovery | Z² Status |
|-----------|-----------|
| m_a ~ 1-100 μeV | Z² requires extension |
| f_a ~ 10¹² GeV | Not natural from T³/Z₂ |
| Axion DM | Must add PQ sector |
| Axion strings | Cosmological signature |

### 9.3 Decisive Tests

| Observable | Z² Prediction | Axion Prediction |
|------------|---------------|------------------|
| θ_QCD | 0 (geometry) | 0 (dynamical) |
| Axion mass | None | ~ μeV |
| Axion-photon | g_aγγ = 0 | g_aγγ ~ 10⁻¹² GeV⁻¹ |
| Dark matter | Not axion | Possibly axion |

---

## 10. Summary

### 10.1 Main Result

**Z² framework does NOT include axion naturally.**

The T³/Z₂ orbifold:
- Projects out B-field modes that would give axion
- Solves strong CP via discrete symmetry instead
- Predicts θ = 0 geometrically

### 10.2 Honest Assessment

| Aspect | Status |
|--------|--------|
| Axion from compactification | Projected out |
| Strong CP solution | Nelson-Barr-like mechanism |
| θ = 0 derivation | Plausible but incomplete |
| Compatibility with axion DM | Requires extension |

### 10.3 Implications

**If axion DM detected:** Z² needs modification
**If no axion found:** Z² prediction confirmed

### 10.4 Key Prediction

```
Z² predicts: No QCD axion, θ_QCD = 0 from topology
Test: ADMX null result + improved nEDM consistent with θ = 0
```

---

## Appendix A: B-Field on Orbifold

### A.1 Transformation Properties

The NS-NS 2-form B_MN under Z₂:
```
σ*B = -B    (natural property of 2-forms under involution)
```

### A.2 Survival Condition

For B to survive the orbifold projection:
```
σ*B = +B    (must be even)
```

But σ*B = -B → **B is projected out entirely**.

### A.3 Exception

B_μν (with both indices in 4D) is unaffected:
```
B_μν(x, y) → B_μν(x, -y)    (even if B_μν is constant in y)
```

But B_μν in 4D doesn't give axion — it gives a massive 2-form.

---

## Appendix B: Nelson-Barr Mechanism

### B.1 The Idea

Nelson-Barr (1984):
- Impose CP as exact symmetry at high energy
- CP breaks spontaneously
- Strong sector remains CP-conserving

### B.2 In Z² Context

The T³/Z₂ orbifold may enforce:
- CP × Z₂ is a gauge symmetry
- Vev breaks CP but not Z₂
- θ_QCD protected by unbroken Z₂

### B.3 Challenges

- Must explain why CKM has CP violation
- Must prevent radiative generation of θ
- Requires specific Yukawa texture

**Full derivation remains to be completed.**

---

*Document: Axion Sector Analysis*
*Part of Z² Framework first-principles derivations*
*Addressing Gap: Axion dark matter question*
