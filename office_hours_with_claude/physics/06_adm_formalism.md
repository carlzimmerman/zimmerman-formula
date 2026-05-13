# ADM Formalism

The ADM (Arnowitt-Deser-Misner) formalism recasts General Relativity as a Hamiltonian system by decomposing 4D spacetime into 3D space evolving in time. This is essential for quantizing gravity and appears in Piece 11 of the Z² framework.

---

## 1. Why Split Spacetime?

### The Problem

General Relativity treats space and time on equal footing. But:
- Quantum mechanics needs a **Hamiltonian** (energy operator)
- Hamiltonians require singling out **time**
- How do we reconcile these?

### Real-World Analogy: Flipping Through a Movie

A movie is a 2D sequence evolving in time:
- Each frame is a 2D snapshot
- Time connects the frames
- The "action" is in how frames relate

```
    4D spacetime as a stack of 3D slices:

    t = 3    ┌─────────────────┐
             │    3D space     │
    t = 2    ├─────────────────┤
             │    3D space     │
    t = 1    ├─────────────────┤
             │    3D space     │
    t = 0    └─────────────────┘

    Each slice is a "frame" of the universe
```

### ADM's Approach

Split the 4D metric into:
1. **3D metric** h_ij on each slice (geometry of space)
2. **Lapse function** N (how fast time flows)
3. **Shift vector** N^i (how coordinates slide between slices)

---

## 2. The 3+1 Decomposition

### The Metric Decomposition

The 4D metric:
```
ds² = g_μν dx^μ dx^ν
```

becomes:
```
ds² = -N² dt² + h_ij(dx^i + N^i dt)(dx^j + N^j dt)
```

### Real-World Analogy: Surveying Terrain

Imagine surveying a hilly landscape:
- **h_ij** = how you measure distances on the ground
- **N** = how steep the hill is (vertical scale)
- **N^i** = if you're measuring from a moving vehicle (horizontal drift)

```
    Time direction
         ↑
         │  N (lapse)
         │  ↑
    ─────┼──●────────────
         │ ╱ N^i (shift)
         │╱
    ─────●───────────────
         3D spatial slice
```

### The Components

| Symbol | Name | Role |
|--------|------|------|
| h_ij | 3-metric | Spatial geometry (6 components) |
| N | Lapse | Time flow rate (1 component) |
| N^i | Shift | Coordinate drift (3 components) |
| **Total** | | **10 components** (matching g_μν) |

---

## 3. Extrinsic Curvature

### What Is It?

The **extrinsic curvature** K_ij measures how the 3D slice is embedded in 4D spacetime.

### Real-World Analogy: Bending Paper

Take a flat piece of paper:
- **Intrinsic curvature** = 0 (still flat as a 2D surface)
- **Extrinsic curvature** = how it bends in 3D

```
    Flat paper:              Curved paper:
    ────────────             ╭──────────╮
                             │          │
    K = 0                    K ≠ 0 (bent!)
```

A cylinder has zero intrinsic curvature but nonzero extrinsic curvature.

### The Definition

```
K_ij = (1/2N)(∂h_ij/∂t - D_iN_j - D_jN_i)
```

where D_i is the covariant derivative on the 3D slice.

### Physical Meaning

K_ij tells you:
- How the slice is "tilted" relative to the time direction
- How the geometry changes from one slice to the next
- The "velocity" of spatial geometry

---

## 4. The Hamiltonian Formulation

### Configuration Variables

**Position:** The 3-metric h_ij
**Momentum:** π^ij (related to extrinsic curvature)

```
π^ij = √h (K^ij - h^ij K)

where K = h^ij K_ij (trace)
```

### The Poisson Brackets

```
{h_ij(x), π^kl(y)} = δ^k_i δ^l_j δ³(x-y)
```

This is the gravitational analogue of {q, p} = 1.

### Real-World Analogy: Ball on a Spring

For a ball on a spring:
- Position q = where the ball is
- Momentum p = how fast it's moving
- Hamiltonian H = total energy

For gravity:
- "Position" h_ij = shape of space
- "Momentum" π^ij = how fast the shape changes
- "Hamiltonian" = combination of constraints!

---

## 5. The Constraints

### The Surprising Feature

The Hamiltonian of GR is **not** a single function. It's a combination of **constraints** that must vanish!

### The Hamiltonian Constraint

```
H = √h [R - K_ij K^ij + K²] - 2√h Λ ≈ 0
```

where R is the 3D Ricci scalar.

### The Momentum Constraint

```
H_i = D_j π^j_i ≈ 0
```

### Why Constraints?

**Diffeomorphism invariance!**

GR is invariant under coordinate transformations. This means:
- Not all components of h_ij, π^ij are physical
- Constraints remove the "gauge" degrees of freedom
- Only 2 degrees of freedom per point remain (gravitational waves!)

### Real-World Analogy: Jigsaw Puzzle Rules

Building a puzzle:
- You have many pieces (h_ij, π^ij)
- But they must fit together (constraints)
- The "rules" (constraints) reduce freedom

---

## 6. The ADM Action

### The Action Principle

The gravitational action in ADM form:
```
S = ∫ dt d³x [π^ij ∂h_ij/∂t - NH - N^iH_i]
```

Compare to particle mechanics:
```
S = ∫ dt [p dq/dt - H]
```

### Variation

Varying the action:
- δN → Hamiltonian constraint H = 0
- δN^i → Momentum constraint H_i = 0
- δh_ij → Evolution equation for π^ij
- δπ^ij → Evolution equation for h_ij

### The Lapse and Shift are Lagrange Multipliers!

N and N^i don't have their own dynamics - they enforce the constraints.

---

## 7. Evolution Equations

### Hamilton's Equations

```
∂h_ij/∂t = {h_ij, H_ADM} = 2N/√h (π_ij - ½h_ij π) + D_iN_j + D_jN_i

∂π^ij/∂t = {π^ij, H_ADM} = [complicated expression involving R_ij, K_ij]
```

### Real-World Analogy: Wave on a Drum

A vibrating drumhead:
- The shape (h_ij) evolves
- The velocity (π^ij) evolves
- They're coupled through wave equations

```
    t = 0         t = 1         t = 2
    _____        _/\_          _____

    Initial      Wave          Returns
    shape        propagates
```

Gravitational waves are "ripples" in spacetime geometry!

---

## 8. Gauge Fixing

### The Problem

The constraints mean h_ij and π^ij have redundancy:
- Many different (h, π) describe the same physics
- We need to "fix the gauge" to get unique solutions

### Common Gauge Choices

| Gauge | Condition | Use |
|-------|-----------|-----|
| Synchronous | N = 1, N^i = 0 | Cosmology |
| Harmonic | ∂_μ(√{-g}g^μν) = 0 | Numerical relativity |
| York | K = const | Initial value problem |

### Real-World Analogy: Choosing Units

Describing a room:
- In meters: 3 × 4 × 2.5
- In feet: 10 × 13 × 8
- Same room, different numbers!

Gauge choice is like choosing units for spacetime coordinates.

---

## 9. The Wheeler-DeWitt Equation

### Quantum Gravity Attempt

Quantize: replace π^ij → -iδ/δh_ij

The Hamiltonian constraint becomes:
```
H Ψ[h_ij] = 0
```

This is the **Wheeler-DeWitt equation** - a "Schrödinger equation for the universe."

### The Problem of Time

Notice: there's no time derivative!
- H Ψ = 0, not i∂Ψ/∂t = HΨ
- Time is "frozen" in quantum gravity
- This is the **problem of time** in quantum cosmology

### Real-World Analogy: Timeless Photo Album

A photo album:
- Each photo is a "state" of the universe
- No inherent ordering (except what we impose)
- Time might be emergent, not fundamental!

---

## 10. Application to Z² Framework

### The Effective 4D Theory

In the Z² framework:
- Start with 7D: M₄ × T³/Z₂
- Compactify on T³/Z₂
- Get effective 4D gravity + Standard Model

### The ADM Variables for Compactification

The 7D metric splits as:
```
ds²_7D = ds²_4D + g_mn(x) dy^m dy^n

where y^m are T³/Z₂ coordinates
```

The internal metric g_mn becomes **scalar fields** in 4D:
- Moduli fields (size and shape of internal space)
- These appear in the Z² framework formulas

### The Hamiltonian Constraint and Z²

From Piece 11:
```
H_ADM = (1/16πG)√h[R + K_ijK^ij - K² - 2Λ_eff] = 0
```

The effective cosmological constant:
```
Λ_eff ∝ e^{-8Z²}
```

**The ADM constraint equations determine how Z² appears in the effective 4D theory!**

---

## Visualization: The 3+1 Split

### Slicing Spacetime

```
         FUTURE
            ↑
    ─────── t = 2 ───────
    │                   │
    │    Σ₂ (3D)       │
    │                   │
    ─────── t = 1 ───────
    │       ↑ N         │
    │    Σ₁ │           │
    │       └─→ N^i     │
    ─────── t = 0 ───────
            ↓
          PAST

    N = how far apart in proper time
    N^i = how coordinates shift
```

### The Full Picture

```
    What ADM gives us:

    CONFIGURATION:     h_ij (6 components)
         ↓               "Shape of space"
    MOMENTUM:          π^ij (6 components)
         ↓               "Rate of change"
    CONSTRAINTS:       H = 0, H_i = 0 (4 equations)
         ↓               "Only 2 physical DoF"
    EVOLUTION:         Hamilton's equations
         ↓               "How space evolves"
    RESULT:            Gravitational dynamics!
```

---

## Exercises

1. **Component counting:** The 4D metric has 10 components. Show that h_ij (6) + N (1) + N^i (3) = 10.

2. **Extrinsic curvature:** A 2-sphere embedded in flat 3-space has K = 1/R. What does this mean physically?

3. **Constraints:** Why do the constraints reduce 12 phase space variables (h_ij, π^ij) to 4 physical degrees of freedom?

4. **Gauge:** In synchronous gauge (N = 1, N^i = 0), what does the line element simplify to?

5. **Z² connection:** If Λ_eff ∝ e^{-8Z²} with Z² = 32π/3, calculate e^{-8Z²} approximately.

---

## Connection to Z² Framework

| ADM Concept | Z² Application |
|-------------|----------------|
| 3+1 split | Separates internal from external dimensions |
| Hamiltonian constraint | Determines effective cosmological constant |
| Extrinsic curvature | Appears in brane embedding |
| Moduli fields | Internal metric components |
| Wheeler-DeWitt | Quantum cosmology context |
| Gauge fixing | Removing redundant degrees of freedom |
| Λ_eff | ∝ e^{-8Z²} from Piece 18 |

---

**Next:** `07_cosmology.md` - The expanding universe and Ω_Λ = 13/19.
