# AI Slop - Quarantined Files

**Date Quarantined:** May 22, 2026

## Why These Files Were Moved Here

These files represent a deviation from first principles and the scientific method. They should NOT be used or referenced.

## The Problem

When the Lyα BAO data showed a best-fit L_c = 15 Gpc (vs the predicted 20.6 Gpc), an AI assistant (Claude) proposed an "asymmetric torus" hypothesis:

```
M₄ × T³(20.6, 20.6, 14.57)/Z₂
```

This was a mistake for several reasons:

### 1. Violates First Principles

The η invariant η = 32π/3 = 33.510 is derived specifically for the **symmetric** T³/Z₂ orbifold. An asymmetric torus would have a different η value, which would:
- Change the Higgs mass prediction
- Change the neutrino mass predictions
- Change all coupling constant derivations
- Invalidate the entire framework

### 2. Ad Hoc Parameter Fitting

Changing L_z = 20.6 → 14.57 Gpc to fit the Lyα data is exactly the kind of ad hoc parameter fitting that the Z² framework was designed to AVOID. The framework should predict observables from first principles, not adjust parameters to match data.

### 3. A Simpler Explanation Exists

The **Diagonal Hypothesis** explains the 15 Gpc observation without breaking symmetry:
- The DESI Lyα survey samples along a face diagonal of the cube
- Effective topological scale along diagonal: L/√2 = 20.6/√2 = 14.57 Gpc
- This is a **projection effect**, not a true asymmetry
- The cube remains symmetric with L_c = 20.6 Gpc

### 4. Bug in Implementation

The `cleaned_pipeline_EFG.py` had a sign error that made results appear worse, leading to over-correction toward the asymmetric hypothesis.

## Files Quarantined

| File | Problem |
|------|---------|
| `asymmetric_torus_test.py` | Tests asymmetric M₄ × T³(Lx,Ly,Lz)/Z₂ |
| `asymmetric_torus_test_results.json` | Results from invalid hypothesis |
| `cleaned_pipeline_EFG.py` | Contains sign error, uses asymmetric vertices |
| `cleaned_pipeline_EFG_results.json` | Wrong results due to sign error |

## The Correct Approach

Use `symmetric_pipeline_corrected.py` which:
- Maintains symmetric T³/Z₂ with L_c = 20.6 Gpc
- Fixes the sign error in AP correction
- Implements the Diagonal Hypothesis
- Defends first principles

## Lesson Learned

**Never change fundamental parameters to fit data.** If the data doesn't match the prediction:
1. Check for systematic errors in the data
2. Check for bugs in the analysis
3. Look for geometric/projection effects
4. Only THEN consider if the theory needs modification

In this case, options 2 and 3 resolved the discrepancy without abandoning first principles.

---

*"The first principle is that you must not fool yourself — and you are the easiest person to fool."* — Richard Feynman
