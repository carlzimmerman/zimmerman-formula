# Cosmology

Cosmology is the study of the universe as a whole - its origin, evolution, and ultimate fate. The Z² framework makes precise predictions for cosmological parameters like Ω_Λ = 13/19.

---

## 1. The Expanding Universe

### Hubble's Discovery (1929)

Galaxies are moving away from us, and the farther they are, the faster they recede:

```
v = H₀ d

where:
v = recession velocity
d = distance
H₀ = Hubble constant ≈ 70 km/s/Mpc
```

### Real-World Scale

```
1 Megaparsec (Mpc) ≈ 3.26 million light-years

At 100 Mpc: v ≈ 7000 km/s (2% of light speed!)
```

### The Raisin Bread Analogy

Imagine raisins in rising bread dough:
- Every raisin sees all others moving away
- Farther raisins move faster
- No raisin is at the "center"

**The universe has no center - space itself is expanding.**

---

## 2. The Friedmann Equations

### The Metric

For a homogeneous, isotropic universe:

```
ds² = -dt² + a(t)²[dr²/(1-kr²) + r²dΩ²]
```

where:
- a(t) = **scale factor** (stretches with time)
- k = curvature: +1 (sphere), 0 (flat), -1 (hyperbolic)

### The First Friedmann Equation

```
H² = (ȧ/a)² = (8πG/3)ρ - k/a² + Λ/3

where:
H = Hubble parameter
ρ = energy density
Λ = cosmological constant
```

### Physical Meaning

The expansion rate H depends on:
1. **Matter density ρ** (slows expansion via gravity)
2. **Curvature k** (geometry of space)
3. **Cosmological constant Λ** (accelerates expansion!)

---

## 3. Energy Content of the Universe

### The Components

| Component | Symbol | What it is |
|-----------|--------|------------|
| Radiation | Ω_r | Photons, neutrinos |
| Matter | Ω_M | Ordinary + dark matter |
| Dark Energy | Ω_Λ | Cosmological constant |
| Curvature | Ω_k | Spatial curvature |

### The Critical Density

The density that makes space flat:

```
ρ_crit = 3H²/(8πG) ≈ 10⁻²⁹ g/cm³

That's about 5 hydrogen atoms per cubic meter!
```

### Density Parameters

```
Ω_i = ρ_i / ρ_crit

Constraint: Ω_r + Ω_M + Ω_Λ + Ω_k = 1
```

### Current Measurements (Planck 2018)

| Parameter | Value |
|-----------|-------|
| Ω_r | ~0.00005 (negligible today) |
| Ω_M | 0.315 ± 0.007 |
| Ω_Λ | **0.685 ± 0.007** |
| Ω_k | ~0 (flat!) |

**The universe is 68.5% dark energy!**

---

## 4. The Z² Prediction: Ω_Λ = 13/19

### The Holographic Derivation

From Piece 15 and Padmanabhan's holographic equipartition:

```
Ω_Λ = (N_surface - N_bulk) / N_total
    = (16 - 3) / (16 + 3)
    = 13/19
    = 0.6842
```

### The Numbers

| Quantity | Value | Origin |
|----------|-------|--------|
| N_surface | 16 | Twisted sector bosonic modes |
| N_bulk | 3 | Fermionic zero modes = b₁(T³) |
| N_total | 19 | Total degrees of freedom |

### Comparison

| | Predicted | Observed |
|---|-----------|----------|
| Ω_Λ | 13/19 = 0.6842 | 0.685 ± 0.007 |
| Error | | **0.1%** |

The same topological numbers (13, 19) that appear in sin²θ_W = 3/13 also appear in cosmology!

---

## 5. The Cosmological Constant Problem

### The Worst Prediction in Physics

Quantum field theory predicts vacuum energy density:

```
ρ_vac ~ M_P⁴ ~ 10¹²⁰ × ρ_observed
```

This is wrong by **120 orders of magnitude**!

### Why It's So Bad

Every quantum field contributes to vacuum energy:
- Electron field: contributes
- Quark fields: contribute
- All Standard Model fields: contribute

They should add up to an enormous cosmological constant.

**But the observed Λ is TINY.**

### The Z² Resolution (Piece 18)

Double holographic warping:

```
ρ_Λ ~ e^{-8Z²} × M_P⁴ ~ 10⁻¹¹⁶ × M_P⁴
```

This explains 116 of the 120 orders of magnitude!

```
e^{-8Z²} = e^{-8 × 32π/3} = e^{-268} ≈ 10⁻¹¹⁶
```

---

## 6. Dark Matter vs Dark Energy

### What's the Difference?

| | Dark Matter | Dark Energy |
|--|-------------|-------------|
| What it does | Clumps, gravitates | Accelerates expansion |
| How much | Ω_M ≈ 0.27 (of matter) | Ω_Λ ≈ 0.68 |
| Changes with time | Dilutes as a⁻³ | Constant density |
| Detection | Gravitational effects | Cosmic acceleration |

### The Z² Perspective on Dark Matter (Piece 17)

**Dark matter particles DON'T EXIST.**

The Z² framework derives Ω_M = 6/19 = 0.316 from thermodynamic equipartition.

The "missing mass" is an **emergent gravity effect**:
- T³/Z₂ creates anisotropic stress tensor π_ij
- This mimics extra gravitational attraction
- Matches MOND-like modifications at galactic scales

**Prediction:** Direct detection experiments will continue finding nothing.

---

## 7. The History of the Universe

### Timeline

```
Time          Event                    Temperature
─────────────────────────────────────────────────────
10⁻⁴³ s      Planck epoch             10³² K
10⁻³⁶ s      Inflation begins         10²⁸ K
10⁻³² s      Inflation ends           10²⁶ K
10⁻¹² s      Electroweak transition   10¹⁵ K
10⁻⁶ s       QCD transition           10¹² K
1 s          Neutrino decoupling      10¹⁰ K
3 min        Nucleosynthesis          10⁹ K
380,000 yr   Recombination (CMB)      3000 K
~400 Myr     First stars              ~100 K
13.8 Gyr     Today                    2.7 K
```

### The Cosmic Microwave Background (CMB)

When the universe cooled to ~3000 K:
- Electrons combined with protons → neutral atoms
- Photons could travel freely
- We see these photons today as 2.7 K microwave radiation

**The CMB is a baby picture of the universe at age 380,000 years.**

---

## 8. Inflation

### The Problems It Solves

1. **Horizon problem:** Why is the CMB so uniform? Regions couldn't have communicated!
2. **Flatness problem:** Why is Ω_k ≈ 0? It should evolve away from zero.
3. **Monopole problem:** Why don't we see magnetic monopoles?

### The Solution

**Exponential expansion** in the early universe:

```
a(t) ~ e^{Ht}
```

During inflation:
- The universe expanded by factor ~e⁶⁰
- Regions in causal contact got stretched apart
- Curvature got diluted to nearly zero
- Monopoles got diluted away

### Perturbations

Quantum fluctuations during inflation → seeds for structure:
- Density perturbations → galaxies
- Gravitational waves → tensor perturbations

### The Z² Predictions (Piece 8)

**Tensor-to-scalar ratio:**
```
r = P_tensor / P_scalar = 1/(2Z²) ≈ 0.015
```

**Spectral index:**
```
n_s = 1 - 2/N ≈ 0.967 (for N ≈ 60 e-folds)
```

**Testable by:** LiteBIRD, CMB-S4

---

## 9. The de Sitter Attractor

### Why Ω_Λ = 13/19 Works

**Question:** Cosmological densities evolve. Why does a static DoF ratio give today's value?

**Answer:** The de Sitter attractor.

### The Argument

As t → ∞ with Λ > 0:
- Matter dilutes: ρ_M → 0
- Radiation dilutes faster: ρ_r → 0
- Dark energy dominates: ρ_Λ = constant

The universe asymptotically approaches:
```
Ω_Λ → 1
Ω_M → 0
```

### The Key Point

At the **de Sitter equilibrium**, the thermodynamic ratio 13/19 represents the fundamental partition.

We observe the universe close to this attractor state!

---

## 10. Summary: The Cosmic Numbers

### From Topology to Cosmology

| Observation | Value | Z² Derivation |
|-------------|-------|---------------|
| Ω_Λ | 0.685 | 13/19 = 0.6842 |
| Ω_M | 0.315 | 6/19 = 0.3158 |
| r | < 0.036 | 1/(2Z²) = 0.015 |
| n_s | 0.965 | 1 - 2/N ≈ 0.967 |

### The Unifying Theme

The same integers (3, 13, 16, 19) that appear in particle physics also appear in cosmology:

```
Particle physics:   sin²θ_W = 3/13
Cosmology:          Ω_Λ = 13/19

The 13 is the same: N_EW = 16 - 3 = 13
```

**Topology unifies particle physics and cosmology.**

---

## Exercises

1. **Hubble time:** If H₀ = 70 km/s/Mpc, estimate the age of the universe. (Hint: 1/H₀)

2. **Critical density:** Verify ρ_crit ≈ 10⁻²⁹ g/cm³ using H₀ = 70 km/s/Mpc.

3. **Density evolution:** If Ω_M = 0.3 today, what was it at z = 1? (Ω_M ∝ (1+z)³/H²)

4. **CC problem:** Calculate e^{-8Z²} and verify it's approximately 10⁻¹¹⁶.

5. **Predictions:** The Z² framework predicts r ≈ 0.015. Current upper limit is r < 0.036. Is this testable?

---

## Connection to Z² Framework

| Cosmology Concept | Z² Application |
|------------------|----------------|
| Ω_Λ = 0.685 | = 13/19 from holographic equipartition |
| Ω_M = 0.315 | = 6/19 from thermodynamics |
| Dark matter | Emergent gravity, not particles |
| CC problem | e^{-8Z²} ≈ 10⁻¹¹⁶ |
| Inflation | r = 1/(2Z²), n_s from e-foldings |
| de Sitter attractor | Why static DoF ratio works |

---

**Next:** `08_string_theory_basics.md` - Extra dimensions and D-branes.
