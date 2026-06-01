# Spectral Dimension Analysis Results

**Date:** May 2, 2026
**Author:** Carl Zimmerman
**Status:** PRELIMINARY - UNEXPECTED RESULTS

---

## Executive Summary

The numerical analysis reveals that the Harper modification with α = 1/Z² does **NOT** produce the expected spectral dimension flow d_s → 2 in the UV limit. Instead:

1. **Standard lattice:** d_s ≈ 3 (as expected)
2. **Harper lattice (α = 1/Z²):** d_s ≈ 3.3 (HIGHER, not lower)
3. **Larger α values:** d_s increases further (4.1 at α=0.1, 5.8 at α=0.2)

**This contradicts the conjecture d_s(x) = 2 + μ(x).**

---

## Detailed Results

### Standard vs Harper Comparison (L=12)

| Configuration | d_s (plateau) | d_s (t=0.05) | d_s (t=1.0) |
|---------------|---------------|--------------|-------------|
| Standard (α=0) | 2.85 ± 0.76 | 0.58 | 3.62 |
| Harper (α=1/Z²=0.03) | 3.34 ± 1.17 | 0.58 | 3.90 |
| Harper (α=0.1) | 4.07 ± 2.19 | 0.58 | 4.09 |
| Harper (α=0.2) | 5.79 ± 4.45 | 0.58 | 5.03 |

### Key Observations

1. **At small t (would-be UV):** d_s ≈ 0.6 for ALL cases
   - This is a lattice artifact, not physical
   - Cannot probe true UV on finite lattice

2. **At intermediate t:** d_s ≈ 3 for standard, d_s > 3 for Harper
   - Harper INCREASES spectral dimension
   - This is the OPPOSITE of the prediction

3. **Harper removes the zero eigenvalue:**
   - Standard: λ_min = 0
   - Harper (α=1/Z²): λ_min = 0.36
   - This spectral gap affects large-t behavior

4. **Finite-size extrapolation (Harper α=1/Z²):**
   - d_s(L→∞) ≈ 3.26
   - Still above 3, not approaching 2

---

## Why This Matters

### The Original Claim

The v7.0.0 paper conjectures:
```
d_s(x) = 2 + μ(x) = (2 + 3x)/(1 + x)
```

Which predicts:
- d_s → 3 in IR (large scales) ✓
- d_s → 2 in UV (small scales) ✗

### What We Found

The Harper modification with α = 1/Z²:
- Does NOT reduce spectral dimension toward 2
- Actually INCREASES spectral dimension above 3
- The spectral gap (λ_min > 0) creates anomalous behavior

---

## Possible Interpretations

### Interpretation 1: The Harper Modification is Wrong

The Z² framework may require a different type of modification:
- Not Harper phases on a fixed lattice
- Perhaps a different α value
- Perhaps a different modification entirely

**Next step:** Try alternative modifications (random disorder, curved embedding)

### Interpretation 2: Lattice ≠ Continuum

The spectral dimension flow d_s → 2 is a **continuum quantum gravity** prediction, not a classical lattice prediction. On a fixed lattice:
- No quantum fluctuations
- No sum over geometries
- No true UV limit (lattice spacing is hard cutoff)

**Next step:** Compare with CDT simulations which DO have quantum fluctuations

### Interpretation 3: The Conjecture is Wrong

The formula d_s(x) = 2 + μ(x) may simply be incorrect:
- The spectral dimension and MOND μ(x) may not be connected
- The entropy partition argument may be flawed
- The factor Z in the Harper coupling may be wrong

**Next step:** Re-examine the physical argument

---

## Revised Assessment of v7.0.0 Claims

### Spectral Dimension Section

| Claim | v7.0.0 Status | Numerical Result | Assessment |
|-------|---------------|------------------|------------|
| d_s flows 3 → 2 | Conjectured | NOT CONFIRMED | Fails on lattice |
| Harper α = 1/Z² gives reduction | Assumed | CONTRADICTED | Gives increase |
| Direction matches CDT | Claimed | NOT VERIFIED | Opposite direction |

### Honest Update Needed

The paper should be updated to reflect:
1. Lattice calculation does NOT confirm spectral dimension conjecture
2. The Harper modification needs reconsideration
3. The claim remains a speculation, not a conjecture

---

## Next Steps

### Priority 1: Understand Why Harper Increases d_s

The spectral gap introduced by Harper:
- Standard: λ ∈ [0, 12]
- Harper: λ ∈ [0.36, 11.64]

The gap removes low-energy modes, which affects the large-t behavior. Need to understand this better.

### Priority 2: Try Alternative Modifications

- Random on-site disorder (Anderson model)
- Varying coordination number
- Fractal lattices

### Priority 3: Compare with CDT

The CDT spectral dimension flow involves:
- Sum over geometries (quantum superposition)
- Dynamical triangulations
- Monte Carlo sampling

A fixed lattice cannot capture this physics.

### Priority 4: Re-examine Theory

Either:
1. Find a different lattice modification that gives d_s → 2
2. Or acknowledge that spectral dimension claim is unsupported

---

## Conclusion

**The spectral dimension conjecture d_s(x) = 2 + μ(x) is NOT supported by numerical calculation.**

The Harper modification with α = 1/Z² increases spectral dimension rather than decreasing it. This is a significant negative result that should be honestly reported.

Options:
1. **Retract the spectral dimension claim** entirely
2. **Downgrade to speculation** (not even conjecture)
3. **Find alternative modification** that actually works

Recommended: Option 2 for now, pursue Option 3 as research.

---

*Spectral Dimension Analysis Results - Z² Framework*
*May 2026*
