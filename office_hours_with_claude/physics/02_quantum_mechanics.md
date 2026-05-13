# Quantum Mechanics

Quantum mechanics describes physics at the smallest scales. Its rules are strange but precise, and they're essential for understanding the Standard Model and the Z² framework.

---

## 1. The Quantum Revolution

### Classical Physics Fails

By 1900, several experiments couldn't be explained classically:
- **Blackbody radiation:** Classical physics predicted infinite energy (ultraviolet catastrophe)
- **Photoelectric effect:** Light kicks out electrons in discrete packets
- **Atomic spectra:** Atoms emit light at specific frequencies only

### The Resolution: Quantization

Energy comes in discrete packets called **quanta**.

```
E = hf = ℏω

where:
h = Planck's constant = 6.626 × 10⁻³⁴ J·s
ℏ = h/(2π) = "h-bar"
f = frequency
ω = angular frequency = 2πf
```

---

## 2. Wave-Particle Duality

### Light: Wave or Particle?

**Wave evidence:**
- Interference patterns (double-slit experiment)
- Diffraction around obstacles

**Particle evidence:**
- Photoelectric effect (light comes in photons)
- Compton scattering (photons carry momentum)

**Answer:** Both! Light exhibits both behaviors depending on the experiment.

### Matter: Also Waves!

De Broglie (1924): Particles have wavelengths too:

```
λ = h/p

where p = momentum
```

**Real example:** Electron microscopes use electron waves. Their short wavelength allows imaging of atoms!

### The Double-Slit Experiment

```
    │   │
    │   │         ▓░▓░▓░▓░▓░▓  ← Interference pattern
    │   │         │││││││││││
 ───│   │─────────│││││││││││
    │   │         │││││││││││
    │   │         ▓░▓░▓░▓░▓░▓

  Slits         Detection screen
```

Even shooting electrons ONE AT A TIME produces interference!

**The electron goes through BOTH slits** as a wave, then is detected at ONE point as a particle.

---

## 3. The Wave Function

### What is ψ?

The **wave function** ψ(x, t) contains all information about a quantum system.

```
|ψ(x)|² = probability density of finding particle at position x
```

### Probability Interpretation

```
P(particle in region [a,b]) = ∫ₐᵇ |ψ(x)|² dx
```

**Key insight:** We can only predict PROBABILITIES, not definite outcomes.

### Normalization

```
∫_{-∞}^{+∞} |ψ(x)|² dx = 1

"Particle must be SOMEWHERE"
```

### Complex Numbers

ψ is generally **complex-valued**. This allows interference:

```
ψ_total = ψ₁ + ψ₂

|ψ_total|² = |ψ₁|² + |ψ₂|² + 2Re(ψ₁*ψ₂)
                              └── interference term
```

---

## 4. The Schrödinger Equation

### The Fundamental Equation

```
iℏ ∂ψ/∂t = Ĥψ
```

where Ĥ is the **Hamiltonian operator** (total energy).

### Time-Independent Form

For stationary states:

```
Ĥψ = Eψ
```

This is an **eigenvalue equation**:
- ψ = eigenfunction (allowed state)
- E = eigenvalue (allowed energy)

### The Hydrogen Atom

Solving Schrödinger's equation for hydrogen:
- Discrete energy levels: E_n = -13.6 eV / n²
- Explains atomic spectra!
- Predicts orbitals: s, p, d, f shells

**This is why the periodic table works.**

---

## 5. Operators and Observables

### Physical Quantities → Operators

In quantum mechanics, observables become **operators**:

| Observable | Operator |
|-----------|----------|
| Position | x̂ = x (multiply by x) |
| Momentum | p̂ = -iℏ ∂/∂x |
| Energy | Ĥ = p̂²/2m + V(x) |
| Angular momentum | L̂ = r̂ × p̂ |

### Eigenvalues = Possible Measurements

When you measure observable A:
- You get one of the eigenvalues of Â
- The state "collapses" to the corresponding eigenstate

### Expectation Values

The average of many measurements:

```
⟨A⟩ = ∫ ψ* Â ψ dx = ⟨ψ|Â|ψ⟩
```

---

## 6. The Uncertainty Principle

### Heisenberg's Insight

You CANNOT simultaneously know position and momentum precisely:

```
Δx · Δp ≥ ℏ/2
```

### Why?

Position and momentum operators don't commute:

```
[x̂, p̂] = x̂p̂ - p̂x̂ = iℏ ≠ 0
```

Non-commuting operators → can't have simultaneous eigenstates → uncertainty!

### Real-World Analogy

Try to measure a particle's position precisely → need high-energy photon → kicks the particle → uncertain momentum.

**But it's deeper than that** - the uncertainty is fundamental, not just measurement error.

### Other Uncertainty Relations

```
ΔE · Δt ≥ ℏ/2     (energy-time)
ΔL_x · ΔL_y ≥ ℏ/2 |⟨L_z⟩|     (angular momentum components)
```

---

## 7. Spin

### An Intrinsic Property

Particles have **intrinsic angular momentum** called **spin**.

```
Electron spin: s = 1/2
Photon spin: s = 1
Higgs spin: s = 0
```

### Spin-1/2: The Electron

Two spin states: "up" |↑⟩ and "down" |↓⟩

```
Ŝ_z |↑⟩ = +ℏ/2 |↑⟩
Ŝ_z |↓⟩ = -ℏ/2 |↓⟩
```

### The Stern-Gerlach Experiment

```
        Silver beam
            │
            │
       ╭────┴────╮
       │ Magnet  │
       ╰────┬────╯
           / \
          /   \
         ↑     ↓
        spin   spin
        up     down
```

The beam splits into exactly TWO parts - quantized spin!

### Why Spin Matters

- **Statistics:** Spin determines whether particles are fermions (half-integer spin) or bosons (integer spin)
- **Chemistry:** Electron pairing, magnetic properties
- **Z² framework:** Spinors, chirality, the Dirac operator

---

## 8. Identical Particles

### Fermions vs Bosons

**Fermions** (spin 1/2, 3/2, ...):
- Obey Pauli exclusion: no two fermions in same state
- Wave function is antisymmetric: ψ(1,2) = -ψ(2,1)
- Examples: electrons, quarks, neutrinos

**Bosons** (spin 0, 1, 2, ...):
- Can pile up in same state
- Wave function is symmetric: ψ(1,2) = +ψ(2,1)
- Examples: photons, W/Z, Higgs, gravitons

### Real-World Consequences

**Fermion exclusion → chemistry:**
- Electrons fill orbitals one at a time
- This creates the periodic table!

**Boson piling → lasers:**
- All photons in the same state
- Coherent light

---

## 9. Dirac Notation

### Bras and Kets

**Ket:** |ψ⟩ = column vector (state)
**Bra:** ⟨ψ| = row vector (conjugate transpose)

### Inner Product

```
⟨φ|ψ⟩ = ∫ φ*(x) ψ(x) dx

This is a NUMBER (probability amplitude)
```

### Outer Product

```
|ψ⟩⟨φ| = matrix (operator)
```

### Completeness

```
Σₙ |n⟩⟨n| = I (identity)

Any state can be expanded in basis |n⟩
```

### Why This Notation?

It's coordinate-independent and works for any Hilbert space - perfect for abstract quantum theory.

---

## 10. Connection to Z² Framework

### Spinors

Fermions are described by **spinors**, which transform under the spin representation of the Lorentz group.

On T³/Z₂, the Z₂ projection acts on spinors:
```
Ψ_L → survives (left-handed)
Ψ_R → projected out (right-handed)
```

This is why we get **chiral fermions**!

### The Dirac Equation

Relativistic quantum mechanics for fermions:
```
(iγᵘ∂_μ - m)ψ = 0
```

The γ matrices encode the spinor structure.

### Mode Counting

Quantum mechanics on compact spaces has discrete energy levels.

On T³/Z₂:
- Count fermionic zero modes → 3 (generations)
- Count bosonic twisted sector modes → 16

---

## Visualization: Quantum Superposition

### Schrödinger's Cat

```
    ┌─────────────────────────┐
    │                         │
    │    │\      ∧∧          │
    │    │ \    (°°)  ?      │
    │    │  \   ( )          │  Until we look:
    │    │   \  /  \         │  Cat is BOTH alive AND dead!
    │    │                   │
    │    └── radioactive     │
    │        source          │
    └─────────────────────────┘

    |cat⟩ = 1/√2 (|alive⟩ + |dead⟩)
```

When we open the box → state "collapses" to either |alive⟩ or |dead⟩.

### This Actually Happens!

Quantum computers manipulate superpositions:
```
|qubit⟩ = α|0⟩ + β|1⟩
```

Until measured, the qubit is in BOTH states simultaneously.

---

## Exercises

1. **De Broglie:** What is the wavelength of an electron with kinetic energy 100 eV?

2. **Uncertainty:** An electron is confined to a box of width 1 nm. Estimate its minimum kinetic energy.

3. **Spin:** How many distinct spin states does a spin-3/2 particle have?

4. **Operators:** Show that [x̂, p̂] = iℏ using p̂ = -iℏ d/dx.

5. **Dirac notation:** If |ψ⟩ = (1/√2)|↑⟩ + (1/√2)|↓⟩, what is ⟨ψ|Ŝ_z|ψ⟩?

---

## Connection to Z² Framework

| QM Concept | Z² Application |
|-----------|----------------|
| Wave function | Fields on T³/Z₂ |
| Spin | Fermions are spinors |
| Pauli exclusion | Fermionic mode counting |
| Operators | Gauge field operators |
| Eigenvalues | Mass spectrum |
| Commutators | [T_a, T_b] = if_{abc}T_c |

---

**Next:** `03_quantum_field_theory.md` - Combining QM with special relativity.
