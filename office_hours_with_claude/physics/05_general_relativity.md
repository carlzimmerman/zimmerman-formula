# General Relativity

General Relativity (GR) is Einstein's theory of gravity as curved spacetime. It's essential for understanding the ADM formalism and holographic aspects of the Z² framework.

---

## 1. The Big Idea: Gravity is Geometry

### Real-World Analogy: A Bowling Ball on a Mattress

Place a bowling ball on a mattress:
- The mattress curves around it
- Roll a marble nearby - it curves toward the bowling ball
- **Not because of a "force" but because the surface is curved!**

```
    Flat mattress:           Curved by mass:

    ─────────────            ─────╲   ╱─────
                                   ╲ ╱
                                    ●  ← mass
                                   ╱ ╲
    Marble rolls straight    Marble follows curve
```

**Einstein's insight:** Massive objects curve spacetime. Other objects follow the natural paths (geodesics) in that curved spacetime.

### The Equivalence Principle

You can't distinguish between:
1. Standing on Earth (gravity pulling down)
2. Accelerating upward in a rocket at 9.8 m/s²

```
    On Earth:                In accelerating rocket:

      ↓ g = 9.8 m/s²              ↑ a = 9.8 m/s²
    ┌─────────┐               ┌─────────┐
    │ ○ feels │               │ ○ feels │
    │  weight │               │  weight │
    └─────────┘               └─────────┘
    ═══════════
      Earth

    Identical experience!
```

**Gravity and acceleration are equivalent - this is the key to GR.**

---

## 2. Curved Spacetime

### What Does "Curved" Mean?

In flat space, parallel lines stay parallel forever.
In curved space, parallel lines can converge or diverge.

### Real-World Example: Earth's Surface

Start two people at the equator, both walking "straight north":
- They start parallel (both pointing north)
- They meet at the North Pole!
- The surface is curved

```
        North Pole
            ●
           /|\
          / | \
         /  |  \
        ↑   ↑   ↑
       A    B    C
    ─────────────────
         Equator

    All three walk "straight" but converge!
```

### The Metric Tensor

The metric g_μν tells you how to measure distances:

```
ds² = g_μν dx^μ dx^ν
```

**Flat spacetime (Minkowski):**
```
ds² = -c²dt² + dx² + dy² + dz²

g_μν = diag(-1, +1, +1, +1)
```

**Curved spacetime:**
```
g_μν = function of position and time!
```

---

## 3. Einstein's Field Equations

### The Central Equation

```
G_μν = 8πG/c⁴ · T_μν
```

or with cosmological constant:

```
G_μν + Λg_μν = 8πG/c⁴ · T_μν
```

### What Each Piece Means

**Left side (geometry):**
- G_μν = Einstein tensor (curvature)
- Describes how spacetime is bent

**Right side (matter):**
- T_μν = Stress-energy tensor
- Describes mass, energy, pressure, momentum

**The equation says:**
> **"Matter tells spacetime how to curve. Spacetime tells matter how to move."**
> — John Wheeler

### The Stress-Energy Tensor

For a perfect fluid:
```
T_μν = (ρ + p/c²)u_μu_ν + pg_μν
```

where:
- ρ = energy density
- p = pressure
- u_μ = 4-velocity of the fluid

---

## 4. Solutions: What GR Predicts

### Schwarzschild Solution: Black Holes

For a spherical, non-rotating mass M:

```
ds² = -(1 - r_s/r)c²dt² + (1 - r_s/r)⁻¹dr² + r²dΩ²

where r_s = 2GM/c² = Schwarzschild radius
```

### Real-World Analogy: The Point of No Return

A waterfall:
- Water flows faster as it approaches the edge
- At some point, even a fast swimmer can't escape
- Beyond the edge = free fall

```
    ←──── slow water ────────→
          RIVER
    ═══════════════════════════
         ╲               ╱
          ╲   FALLS    ╱
           ╲         ╱
            ╲_______╱

    Event horizon = edge of waterfall
    Nothing escapes once past!
```

### De Sitter Solution: Accelerating Universe

For a universe with only cosmological constant:

```
ds² = -c²dt² + e^{2Ht}(dx² + dy² + dz²)

where H = √(Λ/3)
```

**This describes our accelerating universe!**

### FLRW Solution: Cosmology

For a homogeneous, isotropic universe:

```
ds² = -c²dt² + a(t)²[dr²/(1-kr²) + r²dΩ²]
```

where:
- a(t) = scale factor (universe's size)
- k = curvature (+1, 0, -1)

---

## 5. Geodesics: The Natural Path

### What is a Geodesic?

A geodesic is the "straightest possible path" in curved spacetime.

**On a sphere:** great circles (like the equator or meridians)
**In spacetime:** paths of freely falling objects

### The Geodesic Equation

```
d²x^μ/dτ² + Γ^μ_νρ · dx^ν/dτ · dx^ρ/dτ = 0
```

where Γ^μ_νρ are **Christoffel symbols** (encode the curvature).

### Real-World Analogy: Airplane Routes

Why do planes fly "curved" routes on a flat map?
- The map distorts the sphere
- The plane follows a **geodesic** (shortest path)
- Great circle routes are geodesics on a sphere!

```
    Flat map (Mercator):        On the globe:

    NYC ────────────────→ Tokyo  NYC ╲
    (looks curved)                    ╲
                                       ╲ ← Shorter!
                                        Tokyo
```

**Planets orbit the Sun because they're following geodesics in curved spacetime!**

---

## 6. Tests of General Relativity

### Mercury's Precession

Mercury's orbit precesses - the ellipse slowly rotates:
- Newtonian prediction: 5557"/century (from other planets)
- Observed: 5600"/century
- **Discrepancy: 43"/century**

GR prediction: exactly 43"/century!

```
    Mercury's orbit precesses:

         ╱─────╲
        ╱   ●   ╲     ← ellipse slowly rotates
        ╲  Sun  ╱
         ╲─────╱
              ↻
```

### Gravitational Lensing

Light bends around massive objects:

```
         Apparent position
              ★
             ╱
    ───────●────────  ← Real star behind the Sun
          Sun
             ╲
              ★
         Apparent position

    We see TWO images!
```

Eddington's 1919 eclipse observation confirmed this.

### Gravitational Time Dilation

Clocks run slower in stronger gravity:

```
    At sea level:  tick......tick......tick
    At altitude:   tick...tick...tick...tick (faster!)

    GPS satellites: 45 μs/day faster than Earth clocks
    Must be corrected or GPS fails!
```

### Gravitational Waves (2015)

LIGO detected ripples in spacetime from colliding black holes:

```
    Space stretches and squeezes:

    Normal:    ○
    Stretched: ⬭
    Squeezed:  ⬯
    Repeat at frequency of wave
```

**2017 Nobel Prize!**

---

## 7. Curvature Tensors

### The Riemann Tensor

The full curvature information:
```
R^ρ_σμν = ∂_μΓ^ρ_νσ - ∂_νΓ^ρ_μσ + Γ^ρ_μλΓ^λ_νσ - Γ^ρ_νλΓ^λ_μσ
```

20 independent components in 4D.

### Real-World Visualization

Walk a loop while keeping a vector pointing "straight":
- On a flat surface: returns to original direction
- On a curved surface: direction has changed!

```
    On flat paper:           On a sphere:

    ↑ → → → ↑               ↑ → → → ↗
    ↑       ↓               ↑       ↓
    ↑ ← ← ← ↓               ↑ ← ← ← ↙

    Returns same            Rotated by area!
```

The amount of rotation = curvature × area enclosed.

### The Ricci Tensor

Contraction of Riemann:
```
R_μν = R^ρ_μρν
```

10 independent components - this is what appears in Einstein's equations.

### The Scalar Curvature

Further contraction:
```
R = g^μν R_μν
```

A single number describing total curvature at each point.

---

## 8. Energy Conditions

### Why They Matter

GR allows exotic solutions (wormholes, time machines). Energy conditions restrict what matter is "physical."

### The Conditions

| Condition | Statement | Physical Meaning |
|-----------|-----------|-----------------|
| Weak (WEC) | T_μν u^μ u^ν ≥ 0 | Energy density ≥ 0 |
| Strong (SEC) | (T_μν - ½Tg_μν)u^μu^ν ≥ 0 | Gravity attracts |
| Dominant (DEC) | T_μν u^ν is future-timelike | Energy flows forward in time |

### Z² Framework Application

The holographic c-theorem relies on energy conditions:
- c decreases along RG flow
- This is guaranteed if SEC holds
- Entropy of black holes increases

---

## 9. Gravity as a Gauge Theory?

### Comparing to Electromagnetism

| Electromagnetism | Gravity |
|-----------------|---------|
| U(1) gauge symmetry | Diffeomorphism invariance |
| A_μ (vector potential) | g_μν (metric) |
| F_μν (field strength) | R_μνρσ (Riemann tensor) |
| Charge | Mass-energy |

### The Connection Formalism

Gravity can be written using the **spin connection** ω^a_bμ:
- This is a gauge field for local Lorentz transformations
- Makes the structure more like Yang-Mills theory

### Why This Matters for Z²

The ADM formalism (next section) rewrites GR as a constrained Hamiltonian system:
- Configuration variable: 3-metric h_ij
- Momentum: π^ij (extrinsic curvature)
- Constraints: Hamiltonian and momentum constraints

**This allows integration with string theory compactifications!**

---

## 10. Singularities and Horizons

### Black Hole Anatomy

```
                    ┌─────────────────────┐
                    │                     │
    Infinity        │    Event Horizon    │        Singularity
    ────────────────│         │           │────────────●
                    │         │           │
                    │         ↓           │
                    │   (r = 2GM/c²)      │       (r = 0)
                    └─────────────────────┘

    Nothing escapes   One-way boundary      Curvature → ∞
    from here!
```

### Penrose Diagrams

Compact way to visualize causal structure:

```
         i⁺ (future infinity)
          /\
         /  \
        /    \
    i⁰ ●──────● i⁰ (spatial infinity)
        \    /
         \  /
          \/
         i⁻ (past infinity)

    45° lines = light rays
    Everything else travels slower
```

### The Singularity Theorems

Penrose & Hawking proved: under reasonable conditions, singularities are **inevitable**.

**2020 Nobel Prize for Penrose!**

---

## Visualization: GPS and GR

### How GPS Works

```
    Satellite 1     Satellite 2     Satellite 3
        ●               ●               ●
         \             /               /
          \           /               /
           \    YOU  /               /
            \   ●   /               /
             \ / \ /               /
              X   X───────────────X
         Distance from each satellite
         → triangulation → your position
```

### The GR Corrections

1. **Special relativity:** Satellites move at 14,000 km/hr
   - Time dilation: clocks run 7 μs/day SLOWER

2. **General relativity:** Satellites are 20,000 km up (weaker gravity)
   - Gravitational time dilation: clocks run 45 μs/day FASTER

3. **Net effect:** 45 - 7 = 38 μs/day faster

Without correction: 10 km/day error!

**Your GPS is a daily proof of both SR and GR.**

---

## Exercises

1. **Schwarzschild radius:** Calculate r_s for the Sun (M = 2×10³⁰ kg).

2. **Time dilation:** How much slower does a clock tick at the surface of a neutron star (M = 2M_Sun, R = 10 km) compared to infinity?

3. **Geodesics:** On a sphere, why is the shortest path between two points a great circle?

4. **Curvature:** If you walk around a small triangle on a sphere and measure the angle deficit, how does it relate to the area?

5. **GPS:** If GPS didn't account for relativity, how far off would your position be after 1 day?

---

## Connection to Z² Framework

| GR Concept | Z² Application |
|------------|----------------|
| Curved spacetime | AdS₅ bulk geometry |
| Einstein equations | Coupled to matter on branes |
| Cosmological constant | Λ from e^{-8Z²} suppression |
| ADM formalism | Hamiltonian for 3+1 decomposition |
| Holographic boundary | Where SM lives |
| Geodesics | Particle paths in compact space |
| Ricci curvature | Enters RG flow equations |

---

**Next:** `06_adm_formalism.md` - The 3+1 decomposition of spacetime.
