# Attempt at Rigorous Derivation: η_local = 4π/3

**Date:** 2026-05-31
**Goal:** Derive η_local = 4π/3 from Brüning-Seeley spectral theory without inserting the answer

---

## The Claim to Prove

For the cone C(RP²) = R³/Z₂, the local eta contribution at the cone point should be:

```
η_local = 4π/3
```

If proven, then η(T³/Z₂) = 8 × (4π/3) = 32π/3 = Z².

---

## Attempt 1: Direct Spectral Calculation

### Setup

The Dirac operator on R³/Z₂ in spherical coordinates separates:

```
D = γʳ(∂ᵣ + 1/r + D_RP²/r)
```

where D_RP² is the Dirac operator on the link RP².

### Spectrum of D_RP²

From the code (correctly computed):
- Pin⁻ structure keeps odd ℓ modes
- Eigenvalues: λ = ±(ℓ + 1/2) for ℓ = 1, 3, 5, ...
- Multiplicities: m = ℓ + 1 for each eigenvalue

```
ℓ = 1:  λ = ±3/2,  mult = 2
ℓ = 3:  λ = ±7/2,  mult = 4
ℓ = 5:  λ = ±11/2, mult = 6
...
```

### The Problem: Spectral Symmetry

**Observation:** The spectrum is SYMMETRIC. For each +λ there exists -λ with identical multiplicity.

The eta function is:
```
η(s) = Σ sign(λ)|λ|^{-s} × mult(λ)
```

For a symmetric spectrum:
```
η(s) = Σ_{λ>0} |λ|^{-s} × mult(λ) - Σ_{λ>0} |λ|^{-s} × mult(-λ) = 0
```

**Result:** η(RP²) = 0 ✓ (the code confirms this)

### Extending to R³/Z₂

The full Dirac operator on R³/Z₂ has continuous spectrum. Using any standard regularization (box, zeta, heat kernel), the spectral ASYMMETRY determines η.

For symmetric spectrum: **η(R³/Z₂) = 0**

---

## Attempt 2: Heat Kernel Approach

### The Heat Kernel Expansion

For Dirac operator D on a manifold with conical singularity, the heat trace has an asymptotic expansion:

```
Tr(e^{-tD²}) ~ (4πt)^{-n/2} [a₀ + a₁t^{1/2} + a₂t + ...]
```

where:
- a₀ = Vol(M) (the volume coefficient)
- Higher aₖ involve curvature and boundary terms

### The Eta Function via Heat Kernel

```
η(s) = 1/Γ((s+1)/2) ∫₀^∞ t^{(s-1)/2} Tr(D e^{-tD²}) dt
```

The integrand Tr(D e^{-tD²}) measures spectral asymmetry weighted by the heat kernel.

### For R³/Z₂

The heat kernel on the cone C(RP²) decomposes:
```
K(t; r, r', θ, θ') = Σₗ Kₗ^radial(t; r, r') × Yₗ(θ) Yₗ(θ')
```

where Yₗ are the Z₂-invariant spinor harmonics on S² (odd ℓ only).

**Key point:** The TRACE Tr(D e^{-tD²}) involves:
```
Tr(D e^{-tD²}) = Σₗ ∫ dr r² × Tr_radial(D_r e^{-t D_r²}) × (angular mult)
```

For a symmetric radial problem (which this is), the trace of D (not D²) vanishes term by term.

**Result:** The heat kernel approach also gives η = 0 for R³/Z₂.

---

## Attempt 3: APS Index Theorem with Boundary

### Truncated Cone

Consider the cone truncated at radius R:
```
M_R = {(r, θ) : 0 < r ≤ R, θ ∈ RP²}
```

with boundary ∂M_R ≅ RP² at r = R.

### APS Index Theorem

```
index(D) = ∫_M â(M) - (h + η(∂M))/2
```

where:
- â(M) is the A-roof genus (zero for flat space)
- h = dim ker(D|_∂M)
- η(∂M) is the eta invariant of the boundary

### Application to Our Case

- M_R is topologically a ball (cone over RP²)
- â = 0 (flat metric)
- η(RP²) = 0 (computed above)

This gives index(D) = -h/2, which is about the INDEX, not the eta invariant of the cone itself.

**This doesn't give us η_local.**

---

## Attempt 4: Brüning-Seeley Self-Adjoint Extension

### The Theorem

Brüning-Seeley (1988) proves: For Dirac operator on cone C(N), a self-adjoint extension exists and is UNIQUE if no eigenvalue of D_N equals ±(n-1)/2.

For n=3 and link N=RP²: need no λ = ±1.
Spectrum has λ = ±3/2, ±7/2, ... (none equal ±1). ✓

### What This Gives Us

The theorem guarantees:
1. A unique self-adjoint extension exists
2. The domain of this extension is explicitly characterized
3. The resolvent and heat kernel are well-defined

**But it does NOT say:**
- What the eta invariant equals
- That there's a "local contribution" of 4π/3

The uniqueness is about the OPERATOR, not about assigning a specific number to the singularity.

---

## Attempt 5: The Volume Connection?

### Where 4π/3 Actually Comes From

The number 4π/3 is the volume of the unit 3-ball:
```
Vol(B³) = (4π/3) × 1³ = 4π/3
```

### Is There a Volume-Eta Connection?

In Riemannian geometry, there's NO general theorem stating:
```
η_local(cone point) = Vol(unit ball)
```

The eta invariant is a SPECTRAL quantity (built from eigenvalues).
The ball volume is a GEOMETRIC quantity (built from integration).

These are categorically different mathematical objects.

### Possible Connections in Physics

In physics contexts, regularized quantities sometimes involve volume factors:
- Casimir energy ~ Vol^{-1}
- Vacuum energy density ~ Vol^{-1}
- Path integral measures involve Vol

But these are not the APS eta invariant.

---

## The Honest Conclusion

### What I CAN prove:
1. T³/Z₂ has 8 fixed points ✓
2. Each fixed point has local geometry R³/Z₂ = C(RP²) ✓
3. RP² admits Pin⁻ structure ✓
4. D_RP² has spectrum λ = ±(ℓ+1/2), ℓ odd ✓
5. No eigenvalue equals ±1, so unique self-adjoint extension exists ✓
6. The spectrum is symmetric, so η(RP²) = 0 ✓

### What I CANNOT prove:
- That η_local = 4π/3 from spectral theory
- Any theorem connecting the eta invariant to the ball volume
- That η(T³/Z₂) = 32π/3 in the standard APS sense

### The Gap

The framework's claim appears to be:
```
η_local = ρ_η × Vol(B³) = 1 × (4π/3) = 4π/3
```

with "spectral density ρ_η = 1 by standard normalization."

**This normalization is asserted, not derived.** There's no theorem I can find that establishes ρ_η = 1 for Z₂ orbifold singularities.

---

## What Might Actually Be Going On

### Possibility 1: Different "Eta"
The "eta" in question might not be the APS eta invariant, but some other regularized quantity (e.g., a Chern-Simons term, gravitational anomaly, or effective action contribution).

### Possibility 2: Equivariant Index
There might be an EQUIVARIANT index theorem for orbifolds that I'm not aware of, where fixed-point contributions are computed differently.

### Possibility 3: Physics Definition
In physics, "eta invariant" sometimes means something related to but distinct from the mathematical APS definition (e.g., in gravitational anomalies, the "eta" can involve geometric quantities).

### Possibility 4: The Claim is Wrong
The claim η(T³/Z₂) = 32π/3 might simply be incorrect as a statement about APS eta invariants. The number 32π/3 might appear for other reasons (e.g., as a normalization in the action) but not as a spectral invariant.

---

## References to Check

1. Brüning, J., Seeley, R.: "An index theorem for first order regular singular operators" (1988)
2. Cheeger, J.: "Spectral geometry of singular Riemannian spaces" (1983)
3. Atiyah, Patodi, Singer: "Spectral asymmetry and Riemannian geometry I-III" (1975-76)
4. Bismut, Cheeger: "η-invariants and their adiabatic limits" (1989)
5. Donnelly: "Eta invariants for G-spaces" (1978)

---

## Final Verdict

**I cannot complete the derivation.**

The spectral theory (Brüning-Seeley + standard APS) gives η = 0 for the symmetric spectrum on R³/Z₂. The identification η_local = 4π/3 = Vol(B³) appears to be an assertion connecting a spectral invariant to a geometric volume without rigorous justification.

The "derivation" in `eta_invariant_T3Z2.py` computes the ball volume (correctly, four ways) but doesn't prove that this equals the eta invariant. The explicit spectral calculation in the same file gives 1/(12π²), which is discarded.

**This remains an open gap in the framework's foundations.**
