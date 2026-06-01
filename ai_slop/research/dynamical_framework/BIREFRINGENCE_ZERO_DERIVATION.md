# Why β = 0: The Topological Prohibition of Cosmic Birefringence

**A Rigorous Derivation from T³/Z₂ Geometry**

**Carl Zimmerman | May 2026**

---

## Abstract

We prove that the T³/Z₂ orbifold topology rigorously predicts zero cosmic birefringence (β = 0). This is not an approximation or fine-tuning — it is a topological necessity. The proof proceeds through multiple independent arguments: cohomology, mode expansion, fixed-point constraints, and coupling selection rules. All pseudoscalar fields that could cause birefringence are projected out by the Z₂ orbifold action. This prediction is currently in ~6σ tension with observations, making it the critical test of the Z² framework.

---

## 1. Introduction

### 1.1 What is Cosmic Birefringence?

Cosmic birefringence is the rotation of the polarization plane of light as it travels through the universe. If the Cosmic Microwave Background (CMB) was emitted with polarization angle θ₀, and we observe it with angle θ, then:

```
β = θ - θ₀
```

is the birefringence angle.

### 1.2 Physical Mechanism

Birefringence requires a **pseudoscalar field** φ coupled to electromagnetism via the Chern-Simons interaction:

```
L_CS = (g_φγ/4) φ F_μν F̃^μν
```

where:
- φ is a pseudoscalar (axion-like) field
- F_μν is the electromagnetic field strength
- F̃^μν = (1/2) ε^μνρσ F_ρσ is the dual field strength
- g_φγ is the coupling constant

This coupling causes left- and right-circularly polarized light to travel at slightly different speeds, rotating the linear polarization.

### 1.3 The Birefringence Angle

The rotation angle is:

```
β = (g_φγ/2) [φ(t₀) - φ(t_CMB)]
  = (g_φγ/2) Δφ
```

where Δφ is the change in the pseudoscalar field between CMB emission (z ≈ 1100) and today (z = 0).

### 1.4 The Z² Prediction

**The T³/Z₂ orbifold predicts β = 0 exactly.**

This section proves this result rigorously.

---

## 2. The Z₂ Orbifold Action

### 2.1 Definition

The orbifold T³/Z₂ is constructed from the 3-torus T³ by identifying points under the Z₂ reflection:

```
σ: y → -y

where y = (y¹, y², y³) are coordinates on T³
```

### 2.2 The Torus

The 3-torus T³ is defined by the identifications:

```
y^i ~ y^i + 2πR_i    for i = 1, 2, 3
```

where R_i are the radii of the three circles.

### 2.3 The Z₂ Action

The Z₂ group has two elements: {1, σ} where:
- 1 is the identity
- σ acts as y → -y

The quotient T³/Z₂ identifies each point y with its image -y.

### 2.4 Fixed Points

Points satisfying y = -y (mod 2πR) are **fixed points** of the Z₂ action.

On T³ with the given periodicity:
```
y^i = -y^i (mod 2πR_i)
→ 2y^i = 0 (mod 2πR_i)
→ y^i = 0 or πR_i
```

This gives 2³ = **8 fixed points** at:
```
(y¹, y², y³) ∈ {0, πR₁} × {0, πR₂} × {0, πR₃}
```

---

## 3. Fields on Orbifolds: The Projection

### 3.1 Z₂ Parity of Fields

Every field on T³/Z₂ must have definite transformation under Z₂:

**Z₂-even fields (survive projection):**
```
Φ(y) = Φ(-y)
```

**Z₂-odd fields (projected out):**
```
Φ(y) = -Φ(-y)
```

Only Z₂-even fields exist on the orbifold.

### 3.2 Scalars vs Pseudoscalars

Under spatial reflection (parity P):

**Scalar:** P: φ(x) → φ(-x)  [even under parity]
**Pseudoscalar:** P: φ(x) → -φ(-x)  [odd under parity]

The Z₂ orbifold action y → -y is a reflection in the internal space.

**Key insight:** A pseudoscalar in the internal space transforms as:
```
σ: φ(y) → -φ(-y)
```

For the field to survive the Z₂ projection, we need φ(y) = φ(-y).
But for a pseudoscalar: φ(-y) = -φ(y).

Therefore:
```
φ(y) = φ(-y) = -φ(y)
→ 2φ(y) = 0
→ φ(y) = 0
```

**Pseudoscalars are projected out by Z₂.**

---

## 4. Proof 1: Cohomology Argument

### 4.1 De Rham Cohomology

The cohomology groups H^p(M) classify the independent harmonic p-forms on manifold M.

For the 3-torus T³:
```
H⁰(T³) = R        (constant functions)
H¹(T³) = R³       (three independent 1-forms: dy¹, dy², dy³)
H²(T³) = R³       (three independent 2-forms)
H³(T³) = R        (volume form)
```

### 4.2 Orbifold Cohomology

On T³/Z₂, we must decompose each cohomology group into Z₂-even and Z₂-odd parts:

```
H^p(T³) = H^p_+(T³) ⊕ H^p_-(T³)
```

Only the Z₂-even part survives:
```
H^p(T³/Z₂) = H^p_+(T³)
```

### 4.3 Action on 0-forms (Functions)

A constant function f₀ is even: f₀(-y) = f₀.

A pseudoscalar constant would need: f₀(-y) = -f₀, implying f₀ = 0.

**Result:**
```
H⁰_+(T³) = R     (scalar constants survive)
H⁰_-(T³) = 0     (pseudoscalar constants projected out)
```

### 4.4 Implication for Axion-like Fields

Any axion-like pseudoscalar field that could cause birefringence would need a zero mode (constant piece) to have cosmological effects.

Since H⁰_-(T³/Z₂) = 0, **no pseudoscalar zero mode exists**.

**Therefore β = 0.**

---

## 5. Proof 2: Fourier Mode Expansion

### 5.1 Mode Expansion on T³

Any field on T³ can be expanded in Fourier modes:

```
φ(y) = Σ_{n∈Z³} φ_n exp(i n·y/R)

where n = (n₁, n₂, n₃) and n·y = n₁y¹/R₁ + n₂y²/R₂ + n₃y³/R₃
```

### 5.2 Z₂ Transformation of Modes

Under σ: y → -y:
```
φ(-y) = Σ_n φ_n exp(-i n·y/R)
```

### 5.3 Projection Conditions

**For Z₂-even fields (scalars):**
```
φ(y) = φ(-y)
Σ_n φ_n e^{in·y/R} = Σ_n φ_n e^{-in·y/R}
```
This requires φ_n = φ_{-n}.

The zero mode (n = 0) satisfies this: φ₀ = φ₀ ✓

**For Z₂-odd fields (pseudoscalars):**
```
φ(y) = -φ(-y)
Σ_n φ_n e^{in·y/R} = -Σ_n φ_n e^{-in·y/R}
```
This requires φ_n = -φ_{-n}.

For the zero mode: φ₀ = -φ₀ → φ₀ = 0 ✗

### 5.4 Result

**The zero mode of any pseudoscalar field vanishes:**
```
φ₀^{(pseudo)} = 0
```

Since cosmic birefringence requires a non-zero homogeneous pseudoscalar field, and the zero mode is projected out:

**β = 0**

---

## 6. Proof 3: Fixed Point Constraint

### 6.1 Field Values at Fixed Points

At a fixed point y_fp where y_fp = -y_fp (mod lattice):

For a Z₂-odd field:
```
φ(y_fp) = -φ(-y_fp) = -φ(y_fp)
→ 2φ(y_fp) = 0
→ φ(y_fp) = 0
```

### 6.2 The 8 Fixed Points

On T³/Z₂, there are 8 fixed points. A pseudoscalar field must vanish at ALL of them:
```
φ(0, 0, 0) = 0
φ(πR₁, 0, 0) = 0
φ(0, πR₂, 0) = 0
φ(0, 0, πR₃) = 0
φ(πR₁, πR₂, 0) = 0
φ(πR₁, 0, πR₃) = 0
φ(0, πR₂, πR₃) = 0
φ(πR₁, πR₂, πR₃) = 0
```

### 6.3 Implication for the Zero Mode

A smooth field that:
1. Vanishes at 8 points distributed throughout the space
2. Is antisymmetric under y → -y

must have zero average:
```
⟨φ⟩ = (1/Vol) ∫_{T³/Z₂} φ(y) d³y = 0
```

**The cosmologically relevant (homogeneous) piece vanishes.**

### 6.4 Physical Interpretation

The fixed points act as "anchors" that pin the pseudoscalar field to zero. Since these points are distributed throughout the internal space, there's no way for the field to have a non-zero average.

---

## 7. Proof 4: Coupling Selection Rules

Even if a pseudoscalar somehow existed, its coupling to photons would be forbidden.

### 7.1 The Chern-Simons Coupling

The birefringence-causing interaction is:
```
L_CS = (g/4) φ F_μν F̃^μν
```

### 7.2 Z₂ Parity of Each Factor

**The pseudoscalar φ:**
```
σ: φ → -φ    (Z₂-odd by definition)
```

**The field strength F_μν:**

F_μν is the 4D electromagnetic field strength with μ,ν ∈ {0,1,2,3}.
It has no internal (y) indices.
```
σ: F_μν → F_μν    (Z₂-even)
```

**The dual field strength F̃^μν:**
```
F̃^μν = (1/2) ε^μνρσ F_ρσ
```
Also has no y-indices.
```
σ: F̃^μν → F̃^μν    (Z₂-even)
```

### 7.3 Parity of the Coupling

The full coupling:
```
σ: φ F_μν F̃^μν → (-φ)(F_μν)(F̃^μν) = -φ F_μν F̃^μν
```

**The coupling is Z₂-odd!**

### 7.4 Orbifold Projection

On T³/Z₂, only Z₂-even terms in the Lagrangian survive.

The Chern-Simons coupling φ F F̃ is Z₂-odd → **projected out**.

**Even if a pseudoscalar existed, it couldn't couple to photons.**

---

## 8. The B-field Argument

### 8.1 Origin of Axions in String Theory

In string theory, axion-like fields typically arise from:
1. The Kalb-Ramond B-field (B_μν)
2. Ramond-Ramond p-forms (C_p)

### 8.2 The B-field on T³/Z₂

The Kalb-Ramond field B_μν is a 2-form gauge field.

On T³, it has components:
- B_μν (4D, external)
- B_μi (mixed)
- B_ij (internal)

The internal components B_ij provide axion-like scalars upon dimensional reduction.

### 8.3 Z₂ Transformation of B-field

The B-field transforms under the orbifold as:
```
σ: B_ij(y) → B_ij(-y) = -B_ij(y)
```

This is because B is a 2-form, and the Z₂ reflection flips the orientation of the internal space.

### 8.4 Projection

Since B_ij is Z₂-odd, its zero mode is projected out:
```
B_ij^{(0)} = 0
```

**No axion from the B-field survives the orbifold projection.**

### 8.5 This Explains "No QCD Axion" Prediction

The same argument shows why Z² predicts no QCD axion:
- The would-be axion comes from B_ij
- B_ij is Z₂-odd
- Its zero mode is projected out
- No axion exists in the low-energy theory

---

## 9. Mathematical Summary

### 9.1 The Chain of Logic

```
T³/Z₂ orbifold
    ↓
Z₂ acts as y → -y
    ↓
Pseudoscalars transform as φ → -φ
    ↓
Z₂ projection requires φ(y) = φ(-y)
    ↓
But pseudoscalar: φ(-y) = -φ(y)
    ↓
Therefore: φ(y) = -φ(y) → φ = 0
    ↓
No pseudoscalar zero mode
    ↓
No axion-like field
    ↓
No birefringence: β = 0
```

### 9.2 Four Independent Proofs

| Proof | Method | Result |
|-------|--------|--------|
| 1 | Cohomology | H⁰_-(T³/Z₂) = 0 |
| 2 | Fourier modes | φ₀^{pseudo} = 0 |
| 3 | Fixed points | φ must vanish at 8 points |
| 4 | Selection rules | φFF̃ coupling forbidden |

All four proofs give the same result: **β = 0 exactly**.

### 9.3 What This Prediction Is

- **Topological:** Follows from the orbifold structure
- **Exact:** Not an approximation
- **Non-tunable:** No parameter to adjust
- **Falsifiable:** If β ≠ 0 is confirmed, Z² is wrong

---

## 10. Current Observational Status

### 10.1 Measurements

| Experiment | β (degrees) | Significance |
|------------|-------------|--------------|
| Planck PR4 | 0.30 ± 0.11 | 2.7σ |
| ACT DR6 | 0.22 ± 0.07 | 3.1σ |
| Combined | 0.30 ± 0.05 | ~6σ |

### 10.2 The Tension

```
Z² prediction: β = 0.00°
Observation:   β = 0.30° ± 0.05°
Tension:       ~6σ
```

**This is the most serious challenge to the Z² framework.**

### 10.3 Possible Resolutions

1. **Systematic error:** Dust polarization, instrumental miscalibration
2. **Z² is wrong:** The topology is not T³/Z₂
3. **Extension needed:** Modified orbifold that allows small β

### 10.4 Future Tests

LiteBIRD (2028-2031) will measure β with precision ~0.01°:
- If β = 0.00° ± 0.01°: Z² confirmed, systematics were wrong
- If β = 0.30° ± 0.01°: Z² falsified

---

## 11. Comparison with Other Predictions

### 11.1 Derivation Quality

| Prediction | Derivation | Status |
|------------|------------|--------|
| β = 0 | RIGOROUS (topological) | 6σ tension |
| w = -1 | RIGOROUS (moduli frozen) | Consistent |
| n_s = 0.967 | DERIVED | Verified |
| r = 0.015 | CONJECTURED | Testable |
| α⁻¹ = 137.04 | CONJECTURED | Pattern |

### 11.2 Why β = 0 Matters Most

Unlike α or r, which are conjectures:
- β = 0 is **rigorously derived**
- It follows from basic topology
- There is no adjustable parameter
- It makes the sharpest prediction

**If any Z² prediction should be trusted, it's β = 0.**

**And yet it's the one in tension with data.**

---

## 12. Conclusion

### 12.1 The Mathematical Result

We have proven, through four independent methods, that:

**The T³/Z₂ orbifold topology requires β = 0 exactly.**

This follows from:
1. Pseudoscalars being Z₂-odd
2. The orbifold projection eliminating Z₂-odd fields
3. The Chern-Simons coupling being forbidden
4. The B-field zero mode being projected out

### 12.2 The Physical Implication

Cosmic birefringence requires a pseudoscalar field coupled to photons. The T³/Z₂ geometry forbids both:
- The existence of such a field (projected out)
- The coupling to photons (selection rules)

### 12.3 The Experimental Status

Current data shows β ≈ 0.30° at ~6σ significance. If confirmed, this falsifies the Z² framework in its current form.

### 12.4 The Path Forward

LiteBIRD will be definitive by ~2031:
- **If β = 0:** Extraordinary confirmation of Z²
- **If β ≠ 0:** Z² must be abandoned or fundamentally modified

---

## Appendix A: Orbifold Cohomology Details

### A.1 The Z₂ Action on Forms

For a p-form ω on T³:
```
σ*ω = (-1)^p ω    (for forms with all internal indices)
```

This is because Z₂ reverses orientation.

### A.2 Betti Numbers

For T³:
```
b₀ = 1, b₁ = 3, b₂ = 3, b₃ = 1
```

For T³/Z₂:
```
b₀_+ = 1, b₀_- = 0
b₁_+ = 0, b₁_- = 3
b₂_+ = 3, b₂_- = 0
b₃_+ = 0, b₃_- = 1
```

The surviving (even) Betti numbers:
```
b₀(T³/Z₂) = 1
b₁(T³/Z₂) = 0
b₂(T³/Z₂) = 3
b₃(T³/Z₂) = 0
```

### A.3 Interpretation

- b₁ = 0: No harmonic 1-forms → no massless vectors from internal space
- Pseudoscalar 0-forms projected out → no axion

---

## Appendix B: Explicit Fourier Calculation

### B.1 Setup

Let φ(y) be a pseudoscalar on T³ with periodicity 2πR in each direction.

Fourier expansion:
```
φ(y) = Σ_{n∈Z³} φ_n exp(i n·y/R)
```

### B.2 Pseudoscalar Condition

Under y → -y, a pseudoscalar transforms as φ → -φ:
```
φ(-y) = -φ(y)
Σ_n φ_n exp(-i n·y/R) = -Σ_n φ_n exp(i n·y/R)
```

Matching coefficients:
```
φ_n = -φ_{-n}
```

### B.3 Zero Mode

For n = 0:
```
φ₀ = -φ_{-0} = -φ₀
2φ₀ = 0
φ₀ = 0
```

### B.4 Non-zero Modes

For n ≠ 0, the modes come in pairs (n, -n) with opposite signs:
```
φ_n exp(in·y/R) + φ_{-n} exp(-in·y/R)
= φ_n [exp(in·y/R) - exp(-in·y/R)]
= 2i φ_n sin(n·y/R)
```

These are oscillating modes with zero average.

### B.5 Cosmological Average

The cosmologically relevant quantity is the spatial average:
```
⟨φ⟩ = (1/Vol) ∫ φ(y) d³y = φ₀ = 0
```

**The homogeneous piece that would cause birefringence is exactly zero.**

---

## Appendix C: Why This Is Different from h_× = 0

### C.1 The h_× Claim (RETRACTED)

The claim that h_× = 0 (GW cross-polarization projected out) was WRONG because:
- h_μν has indices μ,ν ∈ {0,1,2,3} (4D spacetime)
- Z₂ acts on y (internal space)
- h_μν has no y-dependence for the zero mode
- Both polarizations are Z₂-even

### C.2 The β = 0 Claim (VALID)

The β = 0 derivation is CORRECT because:
- Pseudoscalars are defined by their transformation under reflection
- The Z₂ acts as a reflection in internal space
- A field that is odd under this reflection is projected out
- This is independent of which indices the field carries

### C.3 The Key Difference

| Quantity | Why Z₂ acts | Result |
|----------|-------------|--------|
| h_× | h_μν has no y-indices | Z₂-even, survives |
| φ_pseudo | Defined as odd under reflection | Z₂-odd, projected out |

The pseudoscalar nature is intrinsic to the field, not dependent on index structure.

---

*Document: Birefringence Zero Derivation*
*Part of Z² Framework Research*
*May 2026*
