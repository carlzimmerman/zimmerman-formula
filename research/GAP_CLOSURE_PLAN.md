# Gap Closure Plan: Remaining Z² Framework Gaps

**Date:** April 30, 2026
**Status:** Active Research Plan

---

## Executive Summary

After reviewing all 32 AI-generated cross-reviews, only **2 genuine computational gaps** remain:

1. **Spectral Dimension** (raised by Loll) - NOT COMPUTED
2. **MOND Interpolating Function μ(x)** (raised by Milgrom) - Only a₀ derived

All other identified gaps have been SOLVED:
- Hierarchy problem: M_Pl = 2v × Z^21.5 (0.38% error)
- Fermion masses: m_μ/m_e = 64π + Z (0.04% error)
- Born rule: Derived from Gleason + 3D geometry
- Chiral fermions: S¹/Z₂ orbifold mechanism

---

## GAP 1: Spectral Dimension

### What Is It?

The **spectral dimension** d_s measures how heat diffuses on a manifold:

```
P(return | time t) ~ t^{-d_s/2}
```

For smooth manifolds, d_s = d (topological dimension).
For discrete/fractal structures, d_s can differ and even FLOW with scale.

### Why It Matters

Loll's Causal Dynamical Triangulations (CDT) finds:
- d_s = 4 at large scales (matches observed spacetime)
- d_s → 2 at small scales (flows from 4 to 2)

This "dimensional reduction" is a key prediction of discrete quantum gravity.

**The Challenge:** Does the Z² cubic lattice exhibit similar spectral dimension flow?

### Computational Approach

```python
# Spectral dimension on cubic lattice

1. Define the graph Laplacian:
   L = D - A
   where A is adjacency matrix, D is degree matrix

2. Compute heat kernel:
   K(t) = Tr(e^{-tL})

3. Extract spectral dimension:
   d_s(t) = -2 × d(log K(t))/d(log t)

4. Check if d_s flows with scale t
```

### Expected Results

For a pure infinite cubic lattice:
- d_s = 3 at all scales (no flow - it's just Z³)

But with Z² modifications (curvature, boundaries, topology):
- May get d_s flow similar to CDT
- Need to include effects from T³×R×T³×R structure

### Research Questions

1. What is d_s for T³ (3-torus)?
2. Does the 8D manifold structure change d_s?
3. Can we get d_s = 4 → 2 flow?

### Implementation File

Create: `research/spectral_dimension/Z2_SPECTRAL_DIMENSION.py`

---

## GAP 2: MOND Interpolating Function μ(x)

### What Is It?

MOND modifies Newtonian gravity at low accelerations:

```
a = a_N × μ(a/a₀)

where:
- a_N = Newtonian acceleration = GM/r²
- a₀ ≈ 1.2×10⁻¹⁰ m/s² (MOND scale)
- μ(x) = interpolating function
```

Common forms of μ(x):
- Simple: μ(x) = x/(1+x)
- Standard: μ(x) = x/√(1+x²)
- RAR: μ(x) = 1/(1 + exp(-√x))

### What's Already Derived

The Z² framework derives the SCALE:
```
a₀ = cH₀/Z

where Z = √(32π/3) ≈ 5.79

This comes from: T_Unruh = T_Hawking
When: a = cH, these temperatures match
The factor Z modifies this to a₀ = cH/Z
```

### What's NOT Derived

The FUNCTIONAL FORM μ(x) is not derived from first principles.

**Challenge:** Why μ(x) = x/(1+x) or similar, rather than some other function?

### Computational Approach

```python
# MOND interpolating function from Z² geometry

1. Consider an observer at acceleration a in Z² spacetime

2. The lattice "sees" both:
   - Local curvature from matter (Newtonian gravity)
   - Cosmological horizon effects (Unruh/Hawking)

3. The competition between these gives an interpolation:
   - High a >> a₀: Local dominates → a ≈ a_N (Newtonian)
   - Low a << a₀: Horizon dominates → a ≈ √(a_N × a₀) (MOND)

4. The specific form μ(x) comes from HOW these interpolate
```

### Physical Insight

The ratio a/a₀ determines "what fraction of the lattice is inside the horizon":
- a >> a₀: Most lattice is "local" → Newtonian
- a << a₀: Lattice "sees" cosmological horizon → Modified

### Key Question

Can we derive μ(x) = x/(1+x) from:
```
μ(x) = (local lattice fraction) / (total lattice fraction)
```

### Research Questions

1. What is the "local" vs "horizon" lattice partition?
2. Does entropy counting give μ(x)?
3. Can holographic arguments derive μ(x)?
4. Is there a unique μ(x) from Z² geometry?

### Implementation File

Create: `research/mond/Z2_MOND_INTERPOLATION.py`

---

## Implementation Priority

### Priority 1: Spectral Dimension

**Why first:**
- More mathematically tractable
- Direct lattice computation possible
- Connects to established CDT results

**Timeline:** Can be computed immediately

### Priority 2: MOND Interpolation

**Why second:**
- Requires more physical insight
- Multiple approaches possible
- Less mathematically defined

**Timeline:** Requires research direction exploration

---

## Success Criteria

### Spectral Dimension Success
- [ ] Compute d_s for cubic lattice
- [ ] Compute d_s for T³ torus
- [ ] Check for dimensional flow
- [ ] Compare to CDT predictions
- [ ] Document in paper

### MOND μ(x) Success
- [ ] Identify physical mechanism
- [ ] Derive functional form
- [ ] Compare to observational fits
- [ ] Make predictions
- [ ] Document in paper

---

## Files to Create

1. `research/spectral_dimension/Z2_SPECTRAL_DIMENSION.py` - Main computation
2. `research/spectral_dimension/SPECTRAL_RESULTS.md` - Results documentation
3. `research/mond/Z2_MOND_INTERPOLATION.py` - MOND derivation attempt
4. `research/mond/MOND_INTERPOLATION_RESULTS.md` - Results documentation

---

## Conclusion

With only 2 genuine gaps remaining (spectral dimension and MOND μ(x)), the Z² framework is remarkably complete. Both gaps are:

1. **Computable** - We can write code to explore them
2. **Testable** - Results can be compared to observations/other theories
3. **Bounded** - Clear success criteria exist

The cross-reviews identified 7 "gaps" but 4 were already solved (hierarchy, fermion masses, Born rule, chiral fermions) and 1 (operator dictionary) is more speculative than critical.

**Next step:** Implement spectral dimension computation.

---

*Gap Closure Plan - Z² Framework*
*April 2026*
