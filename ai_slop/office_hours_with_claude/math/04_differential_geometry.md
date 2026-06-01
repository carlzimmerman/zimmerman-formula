# Differential Geometry

Differential geometry combines topology with calculus. It's the language of general relativity and string theory.

---

## 1. Smooth Manifolds

### From Topology to Geometry

A **smooth manifold** is a manifold where:
- The transition between charts is smooth (infinitely differentiable)
- We can do calculus on it

### Coordinates

On a smooth manifold, we have local coordinates xᵢ.

**Example:** On S² we might use:
- Spherical coordinates (θ, φ)
- Stereographic coordinates (x, y)

Different coordinates describe the same geometry!

---

## 2. Tangent Vectors and Tangent Spaces

### Tangent Vectors

At each point p on a manifold, there's a **tangent space** TₚM - the space of all directions you can move.

**Intuition:** The tangent plane to a sphere at a point.

### Basis Vectors

In coordinates xⁱ, the tangent space has basis vectors:
```
∂/∂xⁱ = ∂ᵢ
```

These are the directions of increasing each coordinate.

A general tangent vector:
```
v = vⁱ ∂ᵢ = v¹∂₁ + v² ∂₂ + ... + vⁿ∂ₙ
```

### Why Derivatives?

Tangent vectors act on functions:
```
v(f) = vⁱ ∂f/∂xⁱ = directional derivative of f along v
```

This is the modern definition: a tangent vector IS a directional derivative operator.

---

## 3. The Metric Tensor

### What is a Metric?

The **metric tensor** g defines:
- Distances
- Angles
- Volumes

In coordinates:
```
ds² = gᵢⱼ dxⁱ dxʲ
```

This is the **line element** - the infinitesimal distance squared.

### Examples

**Flat space (Euclidean):**
```
ds² = dx² + dy² + dz²

gᵢⱼ = [1  0  0]
      [0  1  0]
      [0  0  1]
```

**Flat spacetime (Minkowski):**
```
ds² = -dt² + dx² + dy² + dz²

ηᵤᵥ = [-1  0  0  0]
      [ 0  1  0  0]
      [ 0  0  1  0]
      [ 0  0  0  1]
```

**Sphere S² (radius R):**
```
ds² = R²(dθ² + sin²θ dφ²)
```

**3-torus T³:**
```
ds² = R₁²dθ₁² + R₂²dθ₂² + R₃²dθ₃²
```

**Why this matters for Z²:** The metric on T³/Z₂ determines the "volume" Z² = 32π/3.

---

## 4. Raising and Lowering Indices

### Index Gymnastics

The metric and its inverse relate upper and lower indices:
```
vᵢ = gᵢⱼ vʲ     (lower an index)
vⁱ = gⁱʲ vⱼ     (raise an index)
```

**Convention:**
- Upper indices: contravariant (transform one way)
- Lower indices: covariant (transform the other way)

### The Inverse Metric

```
gⁱʲ gⱼₖ = δⁱₖ
```

The inverse metric raises indices.

---

## 5. Connections and Covariant Derivatives

### The Problem

On a curved space, how do we compare vectors at different points?

In flat space: just subtract them.
On a curved space: we need to **parallel transport**.

### The Christoffel Connection

The **Christoffel symbols** Γⁱⱼₖ tell us how to parallel transport:
```
Γⁱⱼₖ = ½ gⁱˡ (∂ⱼgₖˡ + ∂ₖgⱼˡ - ∂ˡgⱼₖ)
```

### Covariant Derivative

The **covariant derivative** ∇ properly differentiates on curved spaces:
```
∇ᵢ vʲ = ∂ᵢvʲ + Γʲᵢₖ vᵏ
```

For flat space: Γ = 0, so ∇ = ∂ (ordinary derivative).

---

## 6. Curvature

### The Riemann Tensor

The **Riemann curvature tensor** measures how much parallel transport fails to commute:
```
Rⁱⱼₖˡ = ∂ₖΓⁱⱼˡ - ∂ˡΓⁱⱼₖ + ΓⁱₘₖΓᵐⱼˡ - ΓⁱₘˡΓᵐⱼₖ
```

**Key property:** Rⁱⱼₖˡ = 0 if and only if space is flat.

### Ricci Tensor and Scalar

**Ricci tensor:** Contract two indices
```
Rⱼˡ = Rⁱⱼᵢˡ
```

**Ricci scalar:** Contract again
```
R = gʲˡ Rⱼˡ
```

### Examples

| Space | Curvature |
|-------|-----------|
| Flat (ℝⁿ, T³) | R = 0 |
| Sphere S² (radius r) | R = 2/r² |
| Hyperbolic | R < 0 |

**Why this matters for Z²:** The torus T³ is flat (R = 0). The orbifold singularities have delta-function curvature.

---

## 7. Integration on Manifolds

### Volume Element

The **volume element** on an n-dimensional manifold:
```
dV = √|det(g)| dx¹ ∧ dx² ∧ ... ∧ dxⁿ
```

### Integration

To integrate a function f over manifold M:
```
∫_M f dV = ∫ f √|g| dx¹...dxⁿ
```

### Volume of Spaces

**3-torus T³ (radii R):**
```
Vol(T³) = (2π)³ R³
```

**2-sphere S² (radius R):**
```
Vol(S²) = 4πR²
```

**Unit 2-sphere:**
```
Vol(S²) = 4π
```

But the Z² framework uses the **interior volume** 4π/3 (the ball, not the sphere surface).

---

## 8. Differential Forms

### Definition

A **differential form** is an antisymmetric tensor that can be integrated.

**0-form:** Function f
**1-form:** ω = ωᵢ dxⁱ
**2-form:** F = ½ Fᵢⱼ dxⁱ ∧ dxʲ

### The Wedge Product

The wedge product ∧ is antisymmetric:
```
dxⁱ ∧ dxʲ = -dxʲ ∧ dxⁱ
dxⁱ ∧ dxⁱ = 0
```

### Exterior Derivative

The **exterior derivative** d takes k-forms to (k+1)-forms:
```
d(f) = ∂ᵢf dxⁱ

d(ωᵢ dxⁱ) = ∂ⱼωᵢ dxʲ ∧ dxⁱ
```

**Key property:** d² = 0

**Why this matters for Z²:** Maxwell's equations are beautifully written as dF = 0, d*F = J. Gauge theory is the theory of differential forms.

---

## 9. Geodesics

### Definition

A **geodesic** is the shortest path between two points (or more generally, a path of extremal length).

### The Geodesic Equation

```
d²xⁱ/ds² + Γⁱⱼₖ (dxʲ/ds)(dxᵏ/ds) = 0
```

### Examples

- Flat space: straight lines
- Sphere: great circles
- Spacetime: paths of freely falling particles

---

## 10. Fiber Bundles (Preview)

### The Concept

A **fiber bundle** is a space that locally looks like a product:
```
E →π B
```
- E = total space
- B = base space
- π = projection
- The fiber over point b ∈ B is π⁻¹(b)

### Examples

**Trivial bundle:** E = B × F (globally a product)

**Möbius strip:** A non-trivial line bundle over S¹

**Tangent bundle:** TM over M (fiber at p is TₚM)

### Gauge Bundles

In gauge theory:
- Base space = spacetime
- Fiber = internal symmetry group
- Connection = gauge field

**Why this matters for Z²:** The Standard Model is a gauge theory on a principal bundle with structure group SU(3) × SU(2) × U(1).

---

## Exercises

1. **Metric:** Write the metric for a 2-torus with radii R₁ and R₂.

2. **Volume:** Compute the volume of T² with radii R₁ = R₂ = 1.

3. **Curvature:** The metric ds² = dr² + r²dθ² is flat (polar coordinates on ℝ²). Verify by computing the Christoffel symbols.

4. **Line element:** In spherical coordinates, ds² = dr² + r²dθ² + r²sin²θ dφ². What is gθθ?

5. **Geodesics:** On a sphere, why are great circles (not small circles) the geodesics?

---

## Connection to Z² Framework

| Diff Geom Concept | Z² Application |
|------------------|----------------|
| Metric on T³ | Defines the "size" of internal space |
| Volume | Z² = 32π/3 is a volume |
| Curvature R = 0 | T³ is flat (but orbifold has singularities) |
| Fiber bundles | Gauge fields live on bundles |
| Differential forms | Field strengths F = dA |
| Integration | Action integrals, mode sums |

---

**Next:** `05_algebraic_topology.md` - Counting holes with algebra.
