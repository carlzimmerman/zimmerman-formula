# Algebraic Topology

Algebraic topology uses algebra (groups, rings) to study topological spaces. The key insight: **count holes using algebra**.

---

## 1. The Fundamental Question

### What Are We Counting?

Different spaces have different "holes":
- A circle has one 1-dimensional hole (you can't shrink a loop)
- A sphere has no 1-dimensional holes (all loops shrink)
- A torus has two 1-dimensional holes

How do we make this precise and computable?

### The Tools

- **Homotopy groups** πₙ(X): detect holes using maps from spheres
- **Homology groups** Hₙ(X): detect holes using chains and boundaries
- **Betti numbers** bₙ: dimension of homology groups (the "count")

---

## 2. Homotopy: Continuous Deformation

### Homotopy of Maps

Two maps f, g: X → Y are **homotopic** if one can be continuously deformed into the other.

### The Fundamental Group π₁(X)

π₁(X) = loops in X starting and ending at a basepoint, up to homotopy.

**Operation:** Concatenate loops
**Identity:** The constant loop (stay at basepoint)
**Inverse:** Traverse the loop backwards

### Examples

| Space | π₁(X) | Meaning |
|-------|-------|---------|
| ℝⁿ | 0 | All loops shrink |
| S¹ | ℤ | Loops labeled by winding number |
| S² | 0 | All loops shrink |
| T² | ℤ × ℤ | Two independent winding numbers |
| T³ | ℤ × ℤ × ℤ | Three independent winding numbers |

**Why this matters for Z²:** π₁(T³) = ℤ³ means three independent cycles. These become the three fermion generations!

---

## 3. Homology: Chains and Boundaries

### The Idea

Instead of loops, consider **chains** - formal sums of simplices (points, edges, triangles, etc.)

### Simplices

- 0-simplex: a point
- 1-simplex: an edge
- 2-simplex: a triangle
- n-simplex: n+1 vertices, all connected

### The Boundary Operator ∂

The **boundary** of a simplex is its faces:
```
∂(edge AB) = B - A
∂(triangle ABC) = BC - AC + AB = BC + CA + AB
```

**Key property:** ∂² = 0 (the boundary of a boundary is empty)

### Chains, Cycles, and Boundaries

**Chain:** Formal sum of simplices
**Cycle:** Chain with zero boundary (∂c = 0)
**Boundary:** Chain that IS a boundary (c = ∂d)

---

## 4. Homology Groups

### Definition

```
Hₙ(X) = Zₙ(X) / Bₙ(X) = cycles / boundaries
```

- Zₙ(X) = n-cycles (chains with ∂c = 0)
- Bₙ(X) = n-boundaries (chains that are ∂ of something)

**Key insight:** A cycle that isn't a boundary represents a "hole."

### Why Quotient?

Two cycles are equivalent if they differ by a boundary:
```
c₁ ~ c₂  iff  c₁ - c₂ = ∂d for some d
```

This is because boundaries are "trivial" cycles - they can be filled in.

---

## 5. Betti Numbers

### Definition

The **n-th Betti number** bₙ(X) is the rank (dimension) of Hₙ(X):
```
bₙ(X) = dim(Hₙ(X))
```

### Interpretation

| Betti Number | Meaning |
|--------------|---------|
| b₀ | Number of connected components |
| b₁ | Number of 1-dimensional holes (loops that don't shrink) |
| b₂ | Number of 2-dimensional holes (voids) |
| bₙ | Number of n-dimensional holes |

### Examples

| Space | b₀ | b₁ | b₂ | b₃ |
|-------|----|----|----|----|
| Point | 1 | 0 | 0 | 0 |
| Circle S¹ | 1 | 1 | 0 | 0 |
| Sphere S² | 1 | 0 | 1 | 0 |
| Torus T² | 1 | 2 | 1 | 0 |
| 3-Torus T³ | 1 | **3** | 3 | 1 |
| T³/Z₂ | 1 | **3** | 3 | 1 |

**The crucial fact for Z²:** b₁(T³) = **3** = number of fermion generations!

---

## 6. Computing Betti Numbers

### The Künneth Formula

For product spaces:
```
bₖ(X × Y) = Σᵢ bᵢ(X) × bₖ₋ᵢ(Y)
```

### Example: T³ = S¹ × S¹ × S¹

For S¹: b₀ = 1, b₁ = 1, all others = 0.

Using Künneth:
```
b₀(T³) = b₀ × b₀ × b₀ = 1
b₁(T³) = b₁×b₀×b₀ + b₀×b₁×b₀ + b₀×b₀×b₁ = 1+1+1 = 3
b₂(T³) = b₁×b₁×b₀ + b₁×b₀×b₁ + b₀×b₁×b₁ = 1+1+1 = 3
b₃(T³) = b₁ × b₁ × b₁ = 1
```

### The Euler Characteristic

```
χ(X) = Σₙ (-1)ⁿ bₙ = b₀ - b₁ + b₂ - b₃ + ...
```

**Examples:**
- χ(S²) = 1 - 0 + 1 = 2
- χ(T²) = 1 - 2 + 1 = 0
- χ(T³) = 1 - 3 + 3 - 1 = 0

---

## 7. Cohomology

### The Dual Picture

**Cohomology** Hⁿ(X) is the "dual" of homology:
- Homology uses chains (formal sums of simplices)
- Cohomology uses cochains (functions on simplices)

### De Rham Cohomology

For smooth manifolds, cohomology can be computed using differential forms:
```
Hⁿ_dR(M) = closed n-forms / exact n-forms
```

- Closed: dω = 0
- Exact: ω = dη for some (n-1)-form η

**Key fact:** dim(Hⁿ_dR) = bₙ

---

## 8. Poincaré Duality

### Statement

For a closed, oriented n-manifold M:
```
Hₖ(M) ≅ Hⁿ⁻ᵏ(M)
```

or equivalently:
```
bₖ = bₙ₋ₖ
```

### Example: T³

n = 3, so:
- b₀ = b₃ (both = 1)
- b₁ = b₂ (both = 3)

This is why the Betti numbers are symmetric: 1, 3, 3, 1.

---

## 9. The First Betti Number and Generations

### Why b₁(T³) = 3?

The 3-torus T³ has three independent 1-cycles:
```
γ₁: loop around first S¹ factor
γ₂: loop around second S¹ factor
γ₃: loop around third S¹ factor
```

These are linearly independent - no combination is a boundary.

### Connection to Physics

In string theory on T³:
- Each 1-cycle can support a D-brane wrapping it
- Fermions arise at brane intersections
- The number of independent 1-cycles = number of fermion families

**This is why we have exactly 3 generations!**

```
b₁(T³) = 3 = N_gen
```

**Why this matters for Z²:** This is Piece 14 - the intersection number I_ab = b₁(T³) = 3 is the topological origin of three generations.

---

## 10. Orbifold Homology

### What Changes for T³/Z₂?

The Z₂ quotient doesn't change the Betti numbers:
```
b₁(T³/Z₂) = b₁(T³) = 3
```

**Why?** The Z₂ action preserves the 1-cycles (it maps each cycle to itself or its negative).

### The Fixed Points

The 8 fixed points contribute to the **twisted sector** of the orbifold:
- They're where the singularities live
- They contribute 2 × 8 = 16 bosonic modes

**Mode counting:**
```
Total modes = b₁ (untwisted fermionic) + 16 (twisted bosonic) = 3 + 16 = 19
```

---

## Key Formulas for Z²

### The Magic Numbers

| Quantity | Formula | Value |
|----------|---------|-------|
| b₁(T³) | rank(H₁(T³)) | 3 |
| Fixed points | 2^dim(T³) | 8 |
| Twisted bosons | 2 × (fixed points) | 16 |
| Total modes | 16 + 3 | 19 |
| Net bosonic | 16 - 3 | 13 |

### Connection to Physics

- 3 fermion generations = b₁(T³)
- 8 gluons = 8 fixed points
- sin²θ_W = 3/13 = b₁/(16 - b₁)
- Ω_Λ = 13/19 = (16-3)/(16+3)

---

## Exercises

1. **Betti numbers:** Compute the Betti numbers of S³ (hint: it's simply connected with one 3-dimensional "hole").

2. **Künneth:** Use the Künneth formula to compute b₂(S² × S²).

3. **Euler characteristic:** Compute χ(S² × S²). Verify using χ(X × Y) = χ(X)χ(Y).

4. **Duality:** For the 4-torus T⁴, what are b₁ and b₃? Verify Poincaré duality.

5. **Z₂ action:** The Z₂ action on S² (antipodal map) gives RP² (projective plane). What are its Betti numbers? (This is tricky!)

---

## Connection to Z² Framework

| Algebraic Topology | Z² Application |
|-------------------|----------------|
| b₁(T³) = 3 | Three fermion generations |
| H₁(T³) ≅ ℤ³ | Three independent cycles for D-branes |
| 8 fixed points | 8 gluons, 8 vertices of cube |
| 16 twisted modes | Bosonic sector capacity |
| 13 = 16 - 3 | Electroweak capacity in sin²θ_W |
| 19 = 16 + 3 | Total DoF in Ω_Λ = 13/19 |

---

**Next:** `06_orbifolds.md` - The detailed geometry of T³/Z₂.
