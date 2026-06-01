# Topology Basics

Topology studies properties that don't change under continuous deformation. You can stretch, bend, and twist - but not tear or glue. This is the mathematics behind "the shape of space."

---

## 1. The Basic Idea

### The Topologist's Joke

> A topologist is someone who can't tell the difference between a coffee mug and a donut.

Why? Because you can continuously deform one into the other:

```
   Coffee Mug              Donut
    _______
   |       |__            ______
   |          |    →    (      )
   |    O     |    →     (    )
   |__________|           ‾‾‾‾‾‾

   Both have exactly ONE hole (the handle / the hole)
```

This is **topological equivalence** - shapes that can morph into each other without cutting or gluing.

### What You CAN Do (Topology Doesn't Care)

- **Stretch** a rubber band into any shape
- **Bend** a wire into curves
- **Twist** a rope
- **Shrink** or **expand** uniformly

### What You CAN'T Do (Topology Cares!)

- **Cut** or **tear** (creates new boundaries)
- **Glue** or **paste** (connects previously separate points)
- **Poke holes** (changes the "genus")
- **Fill holes** (changes connectivity)

### Topological Equivalence

Two shapes are **topologically equivalent** (homeomorphic) if one can be continuously deformed into the other.

**More examples:**
- A ball and a cube are equivalent (no holes in either)
- The letter O and the letter D are equivalent (both have one hole)
- The letter B and the number 8 are equivalent (both have two holes)
- The letter O and letter X are NOT equivalent (O has a hole, X doesn't)

**Not equivalent:**
- Sphere and torus (sphere has no holes)
- Sphere and figure-8 (figure-8 has a crossing point)

### What Topology Ignores

- Distances (stretching is allowed)
- Angles (bending is allowed)
- Curvature (local shape doesn't matter)

### What Topology Cares About

- Number of holes
- Number of pieces (connectedness)
- Number of boundaries
- Global structure

**Why this matters for Z²:** The orbifold T³/Z₂ has specific topological properties (8 fixed points, 3 independent cycles) that directly determine physics.

---

## 2. Manifolds

### Definition

An **n-dimensional manifold** is a space that locally looks like ℝⁿ.

**Examples:**
- The circle S¹ is a 1-manifold (locally looks like a line)
- The sphere S² is a 2-manifold (locally looks like a plane)
- The torus T² is a 2-manifold

### Why "Locally"?

Globally, a manifold can have complicated structure. But if you zoom in enough, it looks flat.

**Earth analogy:** The Earth is a sphere (S²), but locally it looks flat (that's why ancient people thought it was flat).

### Charts and Atlases

A **chart** is a local coordinate system mapping a piece of the manifold to ℝⁿ.

An **atlas** is a collection of charts covering the whole manifold.

---

## 3. Key Examples of Manifolds

### The Circle S¹

```
S¹ = {(x,y) ∈ ℝ² : x² + y² = 1}
```

**Parametrization:** (cos θ, sin θ) for θ ∈ [0, 2π)

**Topology:** One "hole" (you can't shrink a loop around the circle to a point)

### The 2-Sphere S²

```
S² = {(x,y,z) ∈ ℝ³ : x² + y² + z² = 1}
```

**Topology:** No holes, simply connected (any loop can be shrunk to a point)

### The n-Sphere Sⁿ

Generalization to n dimensions:
```
Sⁿ = {x ∈ ℝⁿ⁺¹ : |x| = 1}
```

**Why this matters for Z²:** The S² appears in singularity resolution (Piece 9). Each fixed point blows up to an S² with volume 4π/3.

### The Torus T²

A donut shape. Can be constructed by:
- Taking a square [0, 2π] × [0, 2π]
- Gluing opposite edges

**Parametrization:** Two angles (θ, φ)

**Topology:** Two independent holes (two circles that can't be shrunk)

### The 3-Torus T³

```
T³ = S¹ × S¹ × S¹
```

Three independent circles! Coordinates: (θ₁, θ₂, θ₃) ∈ [0, 2π)³

**Why this matters for Z²:** T³ is the fundamental building block. The three 1-cycles correspond to the three fermion generations!

---

## 4. Compactness

### Definition

A space is **compact** if every open cover has a finite subcover.

**Intuition:** A compact space is "finite" in some sense - you can't escape to infinity.

### Examples

| Space | Compact? | Why? |
|-------|----------|------|
| [0, 1] (closed interval) | Yes | Bounded and closed |
| (0, 1) (open interval) | No | Missing endpoints |
| S¹, S², T² | Yes | No boundary, can't escape |
| ℝ (real line) | No | Goes to infinity |
| ℝⁿ | No | Goes to infinity |

### Why Compactness Matters

Compact spaces have nice properties:
- Continuous functions achieve max/min
- Sequences have convergent subsequences
- Physics is well-defined (no infinities from "running off to infinity")

**Why this matters for Z²:** The internal space T³/Z₂ is compact. This is essential for getting finite mode counts.

---

## 5. Connectedness

### Path Connectedness

A space is **path connected** if any two points can be joined by a continuous path.

### Simply Connected

A space is **simply connected** if:
1. It's path connected
2. Every loop can be continuously shrunk to a point

**Examples:**
- ℝⁿ: simply connected
- S²: simply connected
- S¹: NOT simply connected (loops around the circle can't shrink)
- T²: NOT simply connected (has two independent non-shrinkable loops)

**Why this matters for Z²:** The non-trivial loops (1-cycles) of T³ give rise to the three fermion generations.

---

## 6. Product Spaces

### Definition

The **product** X × Y consists of all pairs (x, y) with x ∈ X and y ∈ Y.

**Examples:**
- ℝ × ℝ = ℝ² (the plane)
- S¹ × S¹ = T² (the torus)
- S¹ × S¹ × S¹ = T³ (the 3-torus)

### Products Preserve Properties

If X and Y are compact, so is X × Y.
If X and Y are connected, so is X × Y.

---

## 7. Quotient Spaces (Orbifolds)

### The Key Construction

Given a space X and a group G acting on X, the **quotient space** X/G identifies points related by G.

```
X/G = {equivalence classes under G action}
```

**Example:** ℝ/ℤ = S¹
- ℤ acts on ℝ by translation: n · x = x + 2πn
- Identifying x ~ x + 2π wraps the line into a circle

### The Orbifold T³/Z₂

**The space:** T³ with coordinates (y₁, y₂, y₃) ∈ [0, 2π)³

**The Z₂ action:** (y₁, y₂, y₃) ↦ (-y₁, -y₂, -y₃) mod 2π

**The identification:** Point y is equivalent to point -y

**Fixed points:** Points where y = -y (mod 2π)
- This requires yᵢ ∈ {0, π}
- There are 2³ = 8 such points

```
Fixed points at: (0,0,0), (π,0,0), (0,π,0), (0,0,π),
                 (π,π,0), (π,0,π), (0,π,π), (π,π,π)
```

These are the **8 vertices of a cube**!

### Orbifold Singularities

At fixed points, the quotient space has **singularities** - the local geometry is not smooth.

Locally near a fixed point, it looks like ℝ³/Z₂ - a cone-like singularity.

**Why this matters for Z²:** The 8 fixed points are where the physics lives. Each contributes 4π/3 to the volume (from singularity resolution), giving Z² = 8 × 4π/3 = 32π/3.

---

## 8. Boundaries and Closed Manifolds

### Manifolds with Boundary

A **manifold with boundary** has an edge.

**Examples:**
- Disk D² (boundary is S¹)
- Solid ball B³ (boundary is S²)
- Cylinder [0,1] × S¹ (boundary is two circles)

### Closed Manifolds

A **closed manifold** has no boundary.

**Examples:** S¹, S², T², T³

**Why this matters for Z²:** The torus T³ is closed. The orbifold T³/Z₂ is also closed (the fixed points are singularities, not boundaries).

---

## 9. Orientability

### Definition

A manifold is **orientable** if you can consistently define "clockwise" everywhere.

**Orientable:** Sphere, torus, T³
**Non-orientable:** Möbius strip, Klein bottle

### The Z₂ Action and Orientation

The Z₂ action (y ↦ -y) **reverses orientation** (det = -1).

However, the quotient T³/Z₂ is still orientable because Z₂ has even order.

---

## 10. Compactification (Preview)

### The Idea

**Compactification** means "making extra dimensions small and compact."

In string theory:
- We start with 10 (or 11) dimensions
- We "compactify" 6 (or 7) to get 4 observable dimensions
- The shape of the compact dimensions determines physics!

### Kaluza-Klein Mechanism

If a dimension is circular with radius R:
- Momentum is quantized: p = n/R
- This appears as mass in 4D: m² = n²/R²

Small R means large mass gaps - explains why we don't see extra dimensions.

**Why this matters for Z²:** The framework uses T³/Z₂ as the compact internal space. The topology of this space determines:
- Number of generations (3)
- Gauge group structure
- The value of coupling constants

---

## Exercises

1. **Homeomorphism:** Are a sphere with one point removed and the plane ℝ² topologically equivalent? (Hint: stereographic projection)

2. **Compactness:** Is the open ball {(x,y) : x² + y² < 1} compact? Why or why not?

3. **Fixed points:** If Z₃ acts on T² by (θ₁, θ₂) ↦ (θ₁ + 2π/3, θ₂ + 2π/3), are there any fixed points?

4. **Product topology:** T⁴ = T² × T² is the 4-torus. How many independent 1-cycles does it have?

5. **Quotient space:** What is S¹/Z₂ (circle with opposite points identified)? Draw it.

---

## Connection to Z² Framework

| Topology Concept | Z² Application |
|-----------------|----------------|
| 3-torus T³ | The internal space before quotienting |
| Z₂ quotient | Creates orbifold singularities |
| 8 fixed points | Vertices of cube = gluon correspondence |
| Compactness | Ensures finite mode spectrum |
| 3 independent 1-cycles | Three fermion generations |
| Singularity resolution | Each fixed point → S² → 4π/3 volume |

---

**Next:** `04_differential_geometry.md` - When topology meets calculus.
