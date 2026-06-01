# Gauge Theory and the Standard Model

Gauge theory is the mathematical framework underlying all fundamental forces except gravity. The Standard Model IS a gauge theory. This is essential for understanding the Z² framework.

---

## 1. What is Gauge Symmetry?

### Global vs Local Symmetry

**Global symmetry:** The same transformation everywhere.
```
ψ(x) → e^{iα}ψ(x)    (same α everywhere)
```

**Local symmetry:** Transformation varies with position.
```
ψ(x) → e^{iα(x)}ψ(x)    (α depends on x)
```

### The Problem with Local Symmetry

The derivative breaks local symmetry:
```
∂ᵤψ → e^{iα(x)}(∂ᵤψ + i(∂ᵤα)ψ)
```

The extra term (∂ᵤα) ruins the transformation.

### The Solution: Gauge Fields

Introduce a **gauge field** Aᵤ that transforms as:
```
Aᵤ → Aᵤ - ∂ᵤα
```

Define the **covariant derivative:**
```
Dᵤψ = ∂ᵤψ + ieAᵤψ
```

Now Dᵤψ transforms correctly:
```
Dᵤψ → e^{iα(x)}Dᵤψ   ✓
```

**Key insight:** Local symmetry REQUIRES gauge fields!

---

## 2. U(1) Gauge Theory: Electromagnetism

### The Gauge Group

U(1) = {e^{iα} : α ∈ [0, 2π)} = unit circle in complex plane.

This is the **abelian** gauge group of electromagnetism.

### The Lagrangian

```
ℒ = -¼FᵤᵥFᵘᵛ + ψ̄(iγᵘDᵤ - m)ψ
```

where:
- Fᵤᵥ = ∂ᵤAᵥ - ∂ᵥAᵤ (field strength tensor)
- Dᵤ = ∂ᵤ + ieAᵤ (covariant derivative)
- ψ is the electron field
- e is the electric charge (coupling constant)

### Maxwell's Equations

From ℒ, we get:
```
∂ᵤFᵘᵛ = eψ̄γᵛψ = Jᵛ
```

This IS Maxwell's equations in covariant form!

### The Fine Structure Constant

```
α = e²/(4πℏc) ≈ 1/137
```

**In the Z² framework:** α⁻¹ = 4Z² + 3 = 137.04

---

## 3. Non-Abelian Gauge Theory: Yang-Mills

### The Gauge Group

For non-abelian groups (SU(2), SU(3)):
- Generators Tᵃ don't commute: [Tᵃ, Tᵇ] = ifᵃᵇᶜTᶜ
- Multiple gauge fields: Aᵤ = Aᵤᵃ Tᵃ

### The Field Strength

```
Fᵤᵥ = ∂ᵤAᵥ - ∂ᵥAᵤ + ig[Aᵤ, Aᵥ]
```

The extra term [Aᵤ, Aᵥ] means **gauge bosons interact with themselves!**

### The Yang-Mills Lagrangian

```
ℒ = -¼Fᵃᵤᵥ Fᵃᵘᵛ + ψ̄(iγᵘDᵤ - m)ψ
```

where Dᵤ = ∂ᵤ + igAᵤᵃTᵃ.

### Why Non-Abelian Matters

| Property | Abelian (U(1)) | Non-Abelian (SU(N)) |
|----------|---------------|---------------------|
| Gauge bosons | 1 (photon) | N²-1 (gluons, W, Z) |
| Self-interaction | No | Yes |
| Confinement | No | Yes (for SU(3)) |
| Example | QED | QCD, Weak force |

---

## 4. The Standard Model Gauge Group

### The Group

```
G_SM = SU(3)_C × SU(2)_L × U(1)_Y
```

| Factor | Force | Gauge Bosons | Coupling |
|--------|-------|--------------|----------|
| SU(3)_C | Strong | 8 gluons | g_s |
| SU(2)_L | Weak | W¹, W², W³ | g |
| U(1)_Y | Hypercharge | B | g' |

### Dimension Counting

```
dim(SU(3)) + dim(SU(2)) + dim(U(1)) = 8 + 3 + 1 = 12
```

**12 gauge bosons** before symmetry breaking.

### Rank of the Group

```
rank(G_SM) = rank(SU(3)) + rank(SU(2)) + rank(U(1)) = 2 + 1 + 1 = 4
```

**This 4 appears in α⁻¹ = 4Z² + 3!**

---

## 5. Electroweak Unification

### Before Symmetry Breaking

SU(2)_L × U(1)_Y with gauge fields:
- W¹, W², W³ (SU(2)_L)
- B (U(1)_Y)

### After Symmetry Breaking

The Higgs gets a VEV, breaking SU(2)×U(1) → U(1)_EM.

The gauge bosons mix:
```
W± = (W¹ ∓ iW²)/√2    (charged, massive)

[Z]   [cos θ_W   -sin θ_W] [W³]
[A] = [sin θ_W    cos θ_W] [B ]
```

- Z: massive, neutral
- A (photon): massless, neutral

### The Weinberg Angle

```
sin²θ_W = g'²/(g² + g'²)
```

**In the Z² framework:** sin²θ_W = 3/13 = 0.2308

### Why 3/13?

From intersection theory (Piece 14):
- 3 = intersection number I_ab = number of generations
- 13 = 16 - 3 = electroweak capacity

---

## 6. Quantum Chromodynamics (QCD)

### The SU(3) Color Gauge Theory

Quarks carry **color charge** (red, green, blue).

8 gluons mediate the strong force.

### Asymptotic Freedom

At high energies, α_s → 0 (quarks are nearly free).
At low energies, α_s → ∞ (confinement).

### The Strong Coupling

```
α_s(M_Z) ≈ 0.118
```

**In the Z² framework:** α_s = 4/Z² ≈ 0.119 (Piece 7)

### Why 8 Gluons = 8 Fixed Points?

This is one of the deep connections:
- dim(SU(3)) = 8 gluons
- T³/Z₂ has 8 fixed points
- Both = 2³ = vertices of a cube

---

## 7. Gauge Bosons and Representations

### How Particles Transform

Particles are classified by their **representations** under G_SM.

| Particle | SU(3) | SU(2) | U(1)_Y |
|----------|-------|-------|--------|
| Left quark | 3 | 2 | 1/6 |
| Right up quark | 3 | 1 | 2/3 |
| Right down quark | 3 | 1 | -1/3 |
| Left lepton | 1 | 2 | -1/2 |
| Right electron | 1 | 1 | -1 |
| Higgs | 1 | 2 | 1/2 |

### Notation

- **3** = fundamental of SU(3) (transforms as a triplet)
- **2** = fundamental of SU(2) (transforms as a doublet)
- **1** = singlet (doesn't transform)

### Chirality

Notice: Left and right particles have DIFFERENT representations!

This is **chiral** structure - the weak force violates parity.

**In the Z² framework:** Chirality comes from the Z₂ projection: Ψ_R = 0.

---

## 8. Anomaly Cancellation

### The Problem

Quantum effects can break classical symmetries (anomalies).

If gauge symmetries are anomalous → theory is inconsistent!

### The Solution

Anomalies cancel if the particle content is "right."

For the Standard Model:
```
Σ Y³ = 0
Σ Y = 0
```

These are satisfied by the SM particle content!

### Connection to Topology

Anomalies are related to index theorems (Atiyah-Singer).

The anomaly-free condition constrains the topology of compactification.

---

## 9. Coupling Unification

### Running Couplings

Couplings change with energy scale (renormalization group):
```
dα⁻¹/d(ln μ) = b/(2π)
```

### Grand Unification

If the three SM couplings meet at high energy → unified gauge group (GUT).

Candidates: SU(5), SO(10), E₆

### The Z² Perspective

Rather than couplings meeting at high energy, the Z² framework derives them from topology:
- α⁻¹ = 4Z² + 3 (holographic)
- α_s = 4/Z² (reciprocity)
- sin²θ_W = 3/13 (intersection theory)

These are **exact ratios** fixed by topology, not running couplings!

---

## 10. Summary: The Standard Model Lagrangian

```
ℒ_SM = ℒ_gauge + ℒ_fermion + ℒ_Higgs + ℒ_Yukawa
```

**Gauge:**
```
ℒ_gauge = -¼G^a_μν G^{aμν} - ¼W^i_μν W^{iμν} - ¼B_μν B^{μν}
```

**Fermions:**
```
ℒ_fermion = ψ̄ iγ^μ D_μ ψ
```

**Higgs:**
```
ℒ_Higgs = |D_μ Φ|² - V(Φ)
```

**Yukawa:**
```
ℒ_Yukawa = y_f ψ̄_L Φ ψ_R + h.c.
```

---

## Exercises

1. **U(1) gauge invariance:** Show that ℒ = ψ̄(iγ^μ∂_μ - m)ψ is NOT invariant under ψ → e^{iα(x)}ψ but ℒ = ψ̄(iγ^μD_μ - m)ψ IS.

2. **Counting:** How many gauge bosons does SU(5) have?

3. **Weinberg angle:** If g = 0.65 and g' = 0.35, what is sin²θ_W?

4. **Representations:** The Higgs is a (1, 2, 1/2) under G_SM. What is its electric charge Q = T³ + Y?

5. **Anomalies:** Verify that Σ Y = 0 for one generation of SM fermions.

---

## Connection to Z² Framework

| Gauge Theory Concept | Z² Application |
|---------------------|----------------|
| rank(G_SM) = 4 | Appears in α⁻¹ = 4Z² + 3 |
| dim(G_SM) = 12 | 16 - 12 = 4 Higgs components |
| dim(SU(3)) = 8 | 8 gluons ↔ 8 fixed points |
| sin²θ_W | = 3/13 from intersection theory |
| Chirality | From Z₂ projection (Ψ_R = 0) |
| 3 generations | = b₁(T³) = 3 |
| Gauge couplings | Derived from Z² geometry |

---

**Next:** `05_general_relativity.md` - Curved spacetime and gravity.
