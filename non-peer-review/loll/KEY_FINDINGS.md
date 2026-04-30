# Key Findings: Z² Framework vs. Causal Dynamical Triangulations (Loll Program)

**Date:** April 30, 2026
**Status:** Analysis Complete

---

## Executive Summary

This cross-review pits **two discrete spacetime programs** against each other. Both build physics from fundamental building blocks at the Planck scale, but differ profoundly in their choices: CDT uses irregular 4-simplices with built-in causality and sums over geometries; Z² uses regular 3-cubes with emergent causality and a fixed unique geometry. The decisive test is the spectral dimension flow.

---

## NEW FINDINGS

### 1. The Central Clash: Building Blocks

| Feature | CDT (Loll) | Z² (Carl) |
|---------|------------|-----------|
| Building block | 4-simplex | 3-cube |
| Dimension | 4D from start | 3D + emergent time |
| Regularity | Irregular (varying edges) | Regular (identical cubes) |
| Tessellation | Flexible gluing | Perfect (no gaps) |
| Complexity | 5 vertices, 10 edges | 8 vertices, 12 edges |

**Key insight:** CDT prioritizes mathematical simplicity (simplex = simplest polytope). Z² prioritizes geometric optimality (cube = unique tessellator).

---

### 2. NEW: The Tessellation Argument

**CDT position:** We don't need perfect tessellation. Spacetime can be curved and irregular.

**Z² position:** Perfect tessellation minimizes complexity. Curvature emerges from lattice excitations, not from irregular building blocks.

| Approach | CDT | Z² |
|----------|-----|-----|
| Building block shape | Varies | Fixed |
| Gap-filling | Requires irregular simplices | None needed |
| Curvature from | Gluing geometry | Holonomy on edges |
| Measure ambiguity | Present | Absent |

**Resolution:** CDT trades building block simplicity for tessellation complexity. Z² trades building block complexity for tessellation simplicity. Which is more fundamental?

---

### 3. NEW: The Causality Debate

**This is the core philosophical difference.**

| Approach | CDT | Z² |
|----------|-----|-----|
| Time direction | Built into simplices | Emergent from entropy |
| Lorentzian signature | Fundamental | Effective at long wavelengths |
| Arrow of time | Structural | Thermodynamic |
| Closed timelike curves | Forbidden by construction | Forbidden by entropy |

**CDT's discovery:** Euclidean quantum gravity (without causality) produces pathological geometries—crumpled spaces or branched polymers. Only by imposing causality from the start does 4D macroscopic spacetime emerge.

**Z²'s response:** The pathological geometries arise from having a landscape of possible gluings. With only one geometry (the cubic tessellation), there is no landscape and no pathologies.

---

### 4. NEW: Path Integral vs. Fixed Geometry

| Feature | CDT | Z² |
|---------|-----|-----|
| Sum over geometries | Yes (essential) | No (only one exists) |
| Quantum fluctuations | In geometry | In fields on fixed lattice |
| Why? | Don't know which geometry | Theorem I proves uniqueness |
| GR compatibility | Geometry dynamical | Geometry fixed, fields dynamic |

**The philosophical stakes:**

- **CDT says:** Quantum gravity requires summing over spacetimes. This is what "quantum" means for geometry.
- **Z² says:** Quantum gravity requires fields on a fixed lattice. The "quantum" is in the excitations, not the substrate.

**Decisive question:** Does the geometry of spacetime fluctuate, or is it fixed with fluctuating fields?

---

### 5. NEW: Spectral Dimension Flow

**CDT's concrete prediction:**

$$d_s = 4 \text{ at large scales}, \quad d_s \to 2 \text{ at small scales}$$

This "dimensional reduction" is observed in Monte Carlo simulations of CDT.

**Z²'s prediction (to be computed):**

On a cubic lattice:
- Large scales: Random walker sees effective $d = 3$ (spatial) or $d = 4$ (spacetime)
- Small scales: Walker confined to single cube sees structure with 8 vertices, 12 edges

**What Z² must compute:**
1. Define random walk on cubic lattice with time direction
2. Compute spectral dimension at various scales
3. Compare to CDT's 4→2 flow

**If Z² shows similar 4→2 flow:** Both frameworks may be equivalent at some level.
**If Z² shows different flow:** Direct experimental distinction.

---

### 6. NEW: The Standard Model Advantage

| Feature | CDT | Z² |
|---------|-----|-----|
| Pure gravity | ✅ Yes | ✅ Yes |
| Gauge fields | ❌ Not derived | ✅ From edge Euler |
| Fermions | ❌ Not derived | ✅ From vertex counting |
| Generations | ❌ Not derived | ✅ From b₁(T³) = 3 |
| Coupling constants | ❌ Not addressed | ✅ From Z² |

**Z²'s claimed advantage:** The cubic lattice naturally gives rise to the Standard Model gauge group:

$$12 = 8 + 3 + 1$$

- 12 edges → 12 gauge bosons
- 8 vertex-governed → SU(3) color
- 3 face-governed → SU(2) weak
- 1 global → U(1) hypercharge

**CDT's limitation:** CDT describes pure quantum gravity. Adding matter requires additional input.

---

### 7. Lorentz Invariance

| Framework | Status | Mechanism |
|-----------|--------|-----------|
| CDT | Built-in (Lorentzian simplices) | Structural |
| Z² | Emergent at long wavelengths | Statistical/effective |

**Z²'s prediction:** Lorentz violation effects suppressed by $(E/E_{Pl})^n$ should appear at ultra-high energies.

**Test:** Ultra-high-energy cosmic rays, gamma-ray burst timing.

---

### 8. Why CDT Gets Crumpled Geometries

**Loll's discovery:** Without causality constraints, Euclidean Dynamical Triangulations (EDT) produces:
1. Crumpled, high-dimensional monstrosities
2. Branched polymer structures with no macroscopic physics

**The fix:** Impose Lorentzian signature. Each simplex has a time direction. Only causal gluings allowed.

**Z²'s interpretation:** EDT fails because simplices create a vast landscape of possible geometries, most pathological. CDT's causality constraint eliminates most of this landscape. But the cube eliminates the landscape entirely—there is only one cubic tessellation.

**The cube IS the "causal" geometry.**

---

## Points of Agreement

1. **Spacetime is discrete at Planck scale** - Both build from fundamental blocks
2. **Simplices/cubes are building blocks** - Both use polytopes
3. **Macroscopic spacetime emerges** - Neither assumes continuum
4. **Standard methods insufficient** - Both go beyond perturbation theory
5. **Numerical methods valuable** - Both benefit from computation

---

## Points of Genuine Disagreement

### 1. What is the Fundamental Building Block?
- **CDT:** 4-simplex (mathematically minimal)
- **Z²:** 3-cube (tessellation optimal)

### 2. Is Causality Fundamental or Emergent?
- **CDT:** Fundamental (built into simplices)
- **Z²:** Emergent (from entropy increase)

### 3. Do We Sum Over Geometries?
- **CDT:** Yes (path integral essential)
- **Z²:** No (unique geometry from Theorem I)

### 4. What Dimension is Fundamental?
- **CDT:** 4D Lorentzian
- **Z²:** 3D Euclidean + emergent time

### 5. Is Tessellation Perfect?
- **CDT:** No (irregular simplices fill space flexibly)
- **Z²:** Yes (cubes tessellate exactly)

---

## The Research Program Comparison

### What CDT Has Achieved:
1. Non-perturbative quantum gravity
2. 4D macroscopic spacetime emergence
3. de Sitter-like expansion
4. Spectral dimension flow 4→2
5. Hausdorff dimension ≈ 4

### What Z² Claims to Achieve:
1. Unique geometry from first principles
2. Standard Model gauge group
3. Coupling constant derivation
4. No path integral needed
5. Matter from lattice structure

### What Each Needs:
| Need | CDT | Z² |
|------|-----|-----|
| Matter coupling | Yes | Claims solved |
| Spectral dimension | Computed | Needs computation |
| Coupling constants | Not addressed | Claims derived |
| Why these building blocks | Mathematical simplicity | Tessellation uniqueness |

---

## Decisive Tests

| Test | CDT Prediction | Z² Prediction |
|------|----------------|---------------|
| **Spectral dimension** | 4→2 flow | To be computed |
| **Gauge group** | Not addressed | SU(3)×SU(2)×U(1) |
| **Lorentz violation** | Possible | Expected at high E |
| **Coupling constants** | Not derived | From Z² |
| **Standard Model** | Must be added | Claims derived |

---

## Key Quotes

> **LOLL:** Why should nature prefer cubes over simplices? Simplices are mathematically simpler—fewer vertices, fewer edges.

> **CARL:** Simpler in what sense? A single simplex has fewer elements, but tessellating space with simplices requires irregular shapes and complex gluing. The cube tessellates perfectly with identical copies.

> **LOLL:** But perfect tessellation isn't necessary. Spacetime can be curved, irregular.

> **CARL:** The microscopic substrate should be as simple as possible—and perfect cubic tessellation is simpler than irregular simplicial gluing.

---

## Philosophical Stakes

| Question | CDT | Z² |
|----------|-----|-----|
| Is geometry dynamical? | Yes | No (fields are) |
| Is causality fundamental? | Yes | No (emergent) |
| Does path integral exist? | Yes | Collapses to one term |
| Is tessellation important? | No | Yes (uniqueness) |
| Does lattice give matter? | No | Yes (edges, vertices) |

---

## The Synthesis Question

Could both be correct at different levels?

**Possible resolution:** CDT's path integral over simplices might equal Z²'s single cubic geometry in a suitable limit. The irregular simplices might "average" to the unique cubic tessellation.

**Research direction:** Find a map between CDT triangulations and Z² cubic lattice. Does the CDT measure concentrate on cubic-like configurations?

---

*This document summarizes findings from the AI-generated cross-review. See `Loll_Cross_Review.md` for full analysis.*
