# Quantum Field Theory

Quantum Field Theory (QFT) combines quantum mechanics with special relativity. It's the language of the Standard Model and essential for understanding how the Z² framework derives coupling constants.

---

## 1. Why Fields?

### The Problem with Particles

In quantum mechanics, we have a fixed number of particles. But:
- Particles can be **created** (pair production: γ → e⁺e⁻)
- Particles can be **destroyed** (annihilation: e⁺e⁻ → γγ)

**We need a framework where particle number can change.**

### Real-World Analogy: A Wheat Field

Think of a wheat field:
- The **field** (wheat stalks) exists everywhere
- **Excitations** (wind ripples) propagate through it
- Ripples can appear, disappear, combine, split

**Particles are ripples in quantum fields!**

```
    The electromagnetic field:

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ← field exists everywhere
          ∧
         /|\
        / | \   ← photon = ripple in the field
       /  |  \
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

### The Field Concept

| Classical | Quantum Field Theory |
|-----------|---------------------|
| Particle at position x | Field φ(x,t) everywhere |
| Discrete object | Continuous medium |
| Fixed number | Excitations can appear/disappear |

---

## 2. From Quantum Mechanics to QFT

### The Ladder Operators

In QM, the harmonic oscillator has creation/annihilation operators:

```
â†|n⟩ = √(n+1)|n+1⟩    (creates one quantum)
â|n⟩ = √n|n-1⟩         (destroys one quantum)
```

### Promoting to Fields

In QFT, we have operators **at every point in space**:

```
φ̂(x) = ∫ d³k/(2π)³ · 1/√(2ω_k) · (â_k e^{ikx} + â†_k e^{-ikx})
```

- â†_k creates a particle with momentum k
- â_k destroys a particle with momentum k

### Real-World Analogy: Guitar String

A guitar string vibrates in modes (harmonics):
- Each mode has its own frequency
- Plucking adds energy to specific modes
- The string's vibration = sum of all modes

**A quantum field = infinite guitar string in 3D space!**

```
    Mode 1:    ∿∿∿∿∿∿∿∿∿∿
    Mode 2:    ∿∿∿∿∿╱╲∿∿∿∿
    Mode 3:    ∿∿∿╱╲╱╲╱╲∿∿∿

    Total vibration = sum of all modes
    Each mode can have n = 0, 1, 2, ... quanta
```

---

## 3. The Lagrangian Formalism

### Fields Have Actions Too

Just like particles, fields obey the principle of least action:

```
S = ∫ d⁴x ℒ(φ, ∂_μφ)
```

where ℒ is the **Lagrangian density**.

### The Simplest Field: Klein-Gordon

For a free scalar field:

```
ℒ = ½(∂_μφ)(∂^μφ) - ½m²φ²
    └──kinetic──┘   └─mass─┘
```

This gives the wave equation with mass:
```
(□ + m²)φ = 0

where □ = ∂²/∂t² - ∇² (d'Alembertian)
```

### Solutions: Particles!

The solutions are plane waves with energy-momentum relation:
```
E² = p²c² + m²c⁴
```

**This IS Einstein's relativistic energy relation!**

---

## 4. Interactions: Feynman Diagrams

### Real-World Analogy: Recipe Instructions

Feynman diagrams are like recipe steps:
- **Ingredients** = particles
- **Mixing** = interactions
- **Products** = final particles

```
    Recipe: Making electron-positron pair from light

    Ingredient: γ (photon)
           │
           │
           ↓
         ╱   ╲
        ↓     ↓
       e⁻    e⁺

    Products: electron + positron
```

### The Rules

Each diagram element has a mathematical value:
- **Lines** = propagators (particles traveling)
- **Vertices** = interactions (coupling constants!)
- **External lines** = initial/final particles

### Example: Electron Scattering

```
    e⁻ ─────────●─────────── e⁻
                │
                │ γ (photon exchange)
                │
    e⁻ ─────────●─────────── e⁻
```

Two electrons repel by exchanging a virtual photon.

**Every force is mediated by particle exchange!**

### The Coupling Constant

At each vertex, we get a factor of the coupling:

```
    Electromagnetic: α = e²/(4πℏc) ≈ 1/137

    α⁻¹ = 4Z² + 3 = 137.04  ← Z² framework!
```

The strength of interaction = coupling constant.

---

## 5. The Vacuum Isn't Empty

### Vacuum Fluctuations

The QFT vacuum is **NOT** empty:
- Virtual particle-antiparticle pairs constantly appear and disappear
- The uncertainty principle allows this: ΔE·Δt ≥ ℏ/2

```
    "Empty" vacuum:

    ─────●────●─────●────●─────
         e⁺e⁻     e⁺e⁻

    Virtual pairs pop in and out of existence!
```

### Real-World Evidence: Casimir Effect

Two metal plates very close together:
- Fewer vacuum modes can fit between them
- Pressure from outside > pressure inside
- **Plates attract!**

```
    │   fewer    │       more modes
    │   modes    │       outside
    │   inside   │
    │   ← → ←    │  ←←←←←←←←←←←
    │            │

    Net force pushes plates together!
```

**This is measured in labs - vacuum fluctuations are REAL.**

### The Lamb Shift

Virtual particles affect atomic energy levels:
- Electron in hydrogen interacts with vacuum fluctuations
- Energy levels shift slightly from QM predictions
- Measured to 12 decimal places!

**QFT is the most precisely tested theory in physics.**

---

## 6. Renormalization: Taming Infinity

### The Problem

When you calculate in QFT, you often get infinity:
- Virtual particles can have arbitrarily high energy
- Integrals diverge

### Real-World Analogy: Resizing a Photo

When you zoom into a digital photo:
- At some point, you see pixels
- The "continuous" image breaks down
- You need to **renormalize** - accept that physics changes at small scales

### The Solution: Running Couplings

Coupling constants **depend on energy scale**:

```
    α(E) = coupling at energy E

    Low energy (atomic physics):     α ≈ 1/137
    High energy (Z mass):            α ≈ 1/128
    Very high energy (GUT scale):    α ≈ 1/40 (extrapolated)
```

### The Beta Function

The running is described by:
```
β(α) = μ dα/dμ

where μ = energy scale
```

**In the Z² framework:**
- α freezes at the IR fixed point
- β(α) → 0 as energy → low scale
- α⁻¹ → 4Z² + 3 = 137.04

---

## 7. Fermions: The Dirac Field

### Spin-1/2 Particles

Electrons, quarks, neutrinos are **fermions**:
- Spin-1/2
- Obey Pauli exclusion
- Described by the Dirac equation

### The Dirac Lagrangian

```
ℒ = ψ̄(iγ^μ∂_μ - m)ψ
```

where:
- ψ = 4-component spinor field
- γ^μ = Dirac matrices
- ψ̄ = ψ†γ⁰

### Chirality: Left vs Right

Fermions can be **left-handed** or **right-handed**:

```
    Left-handed (ψ_L):     Right-handed (ψ_R):

    spin ← momentum        spin → momentum
    ←─── ●                      ● ───→
```

### Why This Matters for Z²

The Z₂ projection acts on chirality:
```
On T³/Z₂:
  ψ_L → survives
  ψ_R → projected out
```

**This is why weak force only affects left-handed particles!**

---

## 8. Gauge Bosons: The Force Carriers

### Vector Fields

Forces are mediated by spin-1 particles:
- Photon γ (electromagnetic)
- W±, Z⁰ (weak)
- 8 gluons (strong)

### The Gauge Field Lagrangian

For electromagnetism:
```
ℒ = -¼F_μνF^μν

where F_μν = ∂_μA_ν - ∂_νA_μ (field strength tensor)
```

### Counting Degrees of Freedom

| Boson | Mass | Polarizations |
|-------|------|---------------|
| Photon | 0 | 2 (transverse) |
| W± | 80 GeV | 3 |
| Z⁰ | 91 GeV | 3 |
| Gluon | 0 | 2 × 8 = 16 |

The total rank of the Standard Model gauge group:
```
rank(SU(3) × SU(2) × U(1)) = 2 + 1 + 1 = 4
```

This 4 appears in the Z² formula: α⁻¹ = **4**Z² + 3

---

## 9. The Propagator: Particle Travel

### What is a Propagator?

The propagator describes how a particle travels from point A to point B:

```
    A ●───────────────● B
         propagator
         D(x-y)
```

### Real-World Analogy: Sound Propagation

When you speak:
- Sound waves spread out
- Intensity falls with distance
- Some frequencies travel better than others

**The propagator encodes all this information for quantum particles.**

### The Feynman Propagator

For a scalar field:
```
D_F(p) = i/(p² - m² + iε)
```

For a fermion:
```
S_F(p) = i(γ^μp_μ + m)/(p² - m² + iε)
```

For a gauge boson:
```
D_μν(p) = -ig_μν/(p² + iε)  (massless, Feynman gauge)
```

### Poles = Particles

The propagator has a **pole** at p² = m²:
```
When p² → m²: D → ∞
```

**The mass of a particle is where its propagator blows up!**

---

## 10. Symmetries and Conservation Laws

### Noether's Theorem in QFT

Every continuous symmetry → conserved current:

| Symmetry | Conservation Law |
|----------|------------------|
| Translation | Energy-momentum |
| Rotation | Angular momentum |
| U(1) | Electric charge |
| SU(2) | Weak isospin |
| SU(3) | Color charge |

### Current Conservation

```
∂_μJ^μ = 0

"Charge in = Charge out"
```

### The Stress-Energy Tensor

Energy-momentum is carried by:
```
T_μν = ∂ℒ/∂(∂^μφ) · ∂_νφ - η_μν ℒ
```

This couples to gravity in GR!

---

## Visualization: QFT in Action

### Electron-Positron Annihilation

```
    Time ↑
         │
    γ    │    γ
     ╲   │   ╱
      ╲  │  ╱
       ╲ │ ╱
        ╲│╱
    ─────●───── e⁺ enters
         │
         │
    ─────●───── e⁻ enters
         │
```

- e⁻ and e⁺ annihilate
- Energy converts to two photons
- Total energy/momentum conserved

### The Standard Model Lagrangian

```
ℒ_SM = ℒ_gauge + ℒ_fermion + ℒ_Higgs + ℒ_Yukawa

     = -¼F_μνF^μν                    ← Force carriers
       + ψ̄iD̸ψ                        ← Matter particles
       + |D_μH|² - V(H)              ← Higgs field
       + y_f ψ̄Hψ                     ← Mass generation
```

**All of particle physics in one equation!**

---

## Exercises

1. **Propagators:** A particle has mass m = 100 GeV. At what p² does its propagator have a pole?

2. **Dimensions:** In natural units (ℏ = c = 1), what are the dimensions of a scalar field φ?

3. **Feynman diagrams:** Draw the diagram for e⁻ + e⁺ → μ⁻ + μ⁺ via photon exchange.

4. **Running coupling:** If α(m_Z) = 1/128 and α(0) = 1/137, has the coupling increased or decreased with energy?

5. **Z² connection:** Calculate α⁻¹ = 4Z² + 3 using Z² = 32π/3.

---

## Connection to Z² Framework

| QFT Concept | Z² Application |
|-------------|----------------|
| Coupling constants | α⁻¹ = 4Z² + 3 |
| Running couplings | Flow to IR fixed point |
| Gauge group rank | 4 in "4Z²" |
| Chirality | Z₂ projection keeps ψ_L |
| Propagators | Define particle content |
| Lagrangian | Action on T³/Z₂ |
| Vacuum energy | CC problem: e^{-8Z²} |

---

**Next:** `04_gauge_theory.md` - The Standard Model gauge structure.
