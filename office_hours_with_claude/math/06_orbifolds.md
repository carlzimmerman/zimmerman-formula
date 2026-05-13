# Orbifolds: The T³/Z₂ Geometry

The orbifold T³/Z₂ is the heart of the Z² framework. This document covers everything you need to know about this space.

---

## 1. What is an Orbifold?

### Definition

An **orbifold** is a space that locally looks like ℝⁿ/G, where G is a finite group.

Unlike smooth manifolds, orbifolds can have **singularities** at fixed points of the group action.

### Etymology

Orbifold = "orbit manifold" - points are identified by group orbits.

### Key Properties

- Locally like ℝⁿ almost everywhere
- Singularities only at fixed points
- Inherit much of the structure of manifolds (can do calculus, integration, etc.)

---

## 2. Building T³/Z₂

### Step 1: The 3-Torus T³

Start with the 3-torus:
```
T³ = ℝ³ / (2πℤ)³
```

Coordinates: (y₁, y₂, y₃) with yᵢ ~ yᵢ + 2π

Think of it as a cube [0, 2π]³ with opposite faces identified.

### Step 2: The Z₂ Action

Define the Z₂ action:
```
σ: (y₁, y₂, y₃) ↦ (-y₁, -y₂, -y₃)
```

This is **inversion through the origin** (or equivalently, reflection across all three axes).

### Step 3: The Quotient

```
T³/Z₂ = { points on T³ with y ~ -y }
```

Points y and -y are now the **same point**.

---

## 3. Fixed Points

### Definition

A **fixed point** is a point p where σ(p) = p.

### Finding Fixed Points on T³/Z₂

We need:
```
(y₁, y₂, y₃) = (-y₁, -y₂, -y₃)  mod 2π
```

This means:
```
2yᵢ ≡ 0 (mod 2π)
yᵢ ∈ {0, π}
```

### The 8 Fixed Points

Each coordinate can be 0 or π, giving 2³ = 8 fixed points:

| Point | Coordinates |
|-------|-------------|
| P₁ | (0, 0, 0) |
| P₂ | (π, 0, 0) |
| P₃ | (0, π, 0) |
| P₄ | (0, 0, π) |
| P₅ | (π, π, 0) |
| P₆ | (π, 0, π) |
| P₇ | (0, π, π) |
| P₈ | (π, π, π) |

**Geometric interpretation:** These are the 8 vertices of a cube!

```
      P₈───────P₇
     /|       /|
    / |      / |
   P₆───────P₅ |
   |  P₄────|──P₃
   | /      | /
   |/       |/
   P₂───────P₁
```

---

## 4. Local Geometry Near Fixed Points

### The Singularity

Near a fixed point, the local geometry is:
```
ℝ³/Z₂
```

Under Z₂, a small neighborhood looks like a **cone**.

### Why It's Singular

At a smooth point, the manifold looks like ℝ³.
At a fixed point, it looks like ℝ³/Z₂ - this is NOT smooth.

The tangent space is not well-defined in the usual sense.

### Codimension

The fixed points have **codimension 3** (they're 0-dimensional in a 3-dimensional space).

---

## 5. Resolution of Singularities

### The Problem

Singular spaces are problematic for physics:
- Differential equations break down
- Quantum fields have infinite self-energy
- Curvature is distributional

### The Solution: Blow-Up

We "blow up" each fixed point:
- Replace point P with a small sphere S²
- This smooths out the singularity

### The Resolved Space

After resolution, each fixed point becomes an **exceptional divisor** - a copy of S² (or more precisely, ℂP¹).

### Volume Contribution

Each blown-up S² contributes volume:
```
Vol(S²) / 2 = 4π/3
```

(The factor of 2 comes from the Z₂ identification.)

### Total Volume

```
Z² = 8 × (4π/3) = 32π/3 ≈ 33.51
```

**This is the origin of Z²!**

---

## 6. Twisted and Untwisted Sectors

### String Theory on Orbifolds

When string theory is compactified on an orbifold, the spectrum splits into:

**Untwisted sector:** States from smooth regions
**Twisted sector:** States localized at fixed points

### Mode Counting

**Untwisted sector:**
- These are modes that exist on T³ before quotienting
- Include the 3 fermionic zero modes (from b₁(T³) = 3)

**Twisted sector:**
- Localized at the 8 fixed points
- Each fixed point contributes 2 bosonic modes (one complex modulus)
- Total: 8 × 2 = 16 bosonic modes

### The Famous Numbers

```
Fermionic (untwisted): n_F = 3 = b₁(T³)
Bosonic (twisted): n_B = 16 = 2 × 8
Total: N = 3 + 16 = 19
```

---

## 7. Chirality on Orbifolds

### The Projection

The Z₂ action affects different fields differently:

**Even fields:** Ψ(y) = Ψ(-y) → survive
**Odd fields:** Ψ(y) = -Ψ(-y) → projected out

### Chiral Fermions

For fermions, the Z₂ acts on the spinor indices:
```
Ψ_L: survives (left-handed)
Ψ_R: projected out (right-handed)
```

This is why the framework naturally gives **chiral fermions**!

### The Chirality Theorem

```
Ψ_R^(0) = 0
```

All right-handed zero modes are eliminated by the Z₂ projection.

**Physical consequence:** Maximal parity violation is topological!

---

## 8. Hodge Numbers of T³/Z₂

### Definition

For a complex manifold, **Hodge numbers** h^{p,q} count harmonic (p,q)-forms.

### For T³/Z₂

| (p,q) | h^{p,q} |
|-------|---------|
| (0,0) | 1 |
| (1,0), (0,1) | 3 |
| (2,0), (0,2) | 3 |
| (1,1) | 3 |
| (3,0), (0,3) | 1 |

### Euler Characteristic

```
χ = Σ (-1)^{p+q} h^{p,q} = 0
```

---

## 9. The Cube Geometry

### Why a Cube?

The 8 fixed points form the vertices of a cube. This isn't coincidence - it's the fundamental domain of T³/Z₂.

### Geometric Integers

From the cube we get:
- 8 vertices (fixed points → gluons)
- 12 edges (gauge bosons)
- 6 faces (→ relates to CP conservation)
- 4 body diagonals (→ rank of SM)

### The Magic Angle

The angle between a body diagonal and a face diagonal:
```
θ = arctan(1/√2) ≈ 35.26°
```

This is the **magic angle** that appears in twisted bilayer graphene!

---

## 10. Physical Implications

### Summary Table

| Orbifold Property | Physical Meaning |
|------------------|------------------|
| 8 fixed points | 8 gluons of SU(3) |
| b₁ = 3 | 3 fermion generations |
| Z₂ projection | Chiral fermions (Ψ_R = 0) |
| 16 twisted modes | Bosonic sector capacity |
| 3 + 16 = 19 | Total DoF for cosmology |
| Z² = 32π/3 | Fundamental geometric constant |

### The Deep Connection

The orbifold T³/Z₂ is not arbitrary:
- It's the simplest compact orbifold with enough structure
- It naturally produces chiral fermions
- Its topology matches the Standard Model gauge structure
- Its geometry gives the correct numerical predictions

---

## Exercises

1. **Fixed points:** Verify that (π/2, π/2, π/2) is NOT a fixed point.

2. **Local geometry:** Near (0,0,0), sketch what ℝ³/Z₂ looks like. (Hint: think of the upper half-space with the boundary being a cone tip.)

3. **Mode counting:** If we used T³/Z₃ instead (three-fold rotation), how many fixed points would we have?

4. **Blow-up:** When we blow up a point in ℂ², we get ℂP¹ ≅ S². Why does the exceptional divisor have volume 4π/3 rather than 4π?

5. **Chirality:** If the Z₂ action had eigenvalue +1 on Ψ_R instead of -1, would we still get chiral fermions?

---

## The Key Takeaway

**T³/Z₂ is not a mathematical curiosity - it's the shape of internal space that explains:**

- Why 3 generations (b₁ = 3)
- Why 8 gluons (8 fixed points)
- Why chiral fermions (Z₂ projection)
- Why sin²θ_W = 3/13 (mode counting ratio)
- Why Ω_Λ = 13/19 (DoF equipartition)
- Why Z² = 32π/3 (singularity resolution)

---

**Next:** `07_index_theory.md` - The Atiyah-Singer theorem and its applications.
