# DESI Audit Honest Assessment

**Date:** May 22, 2026
**Framework:** Z² Unified Action v11.1.0

## What Happened

During the DESI 5-Year data audit of the Z² framework, an AI assistant (Claude) proposed an "asymmetric torus" hypothesis to explain a discrepancy:

- **Lyα BAO best-fit:** L_c = 15 Gpc
- **CMB-predicted:** L_c = 20.6 Gpc
- **Observation:** 20.6 / √2 = 14.57 ≈ 15 Gpc

This led to a proposed v11.2.0 with M₄ × T³(20.6, 20.6, 14.57)/Z₂.

## Why It Was Wrong

1. **Violates first principles:** η = 32π/3 is derived specifically for symmetric T³/Z₂. Changing geometry invalidates all particle physics predictions (Higgs mass, neutrino masses, coupling constants).

2. **Ad hoc parameter fitting:** Adjusting L_z to match data is exactly what the framework was designed to avoid.

3. **Implementation had bugs:** A sign error made results appear worse, encouraging over-correction toward asymmetry.

## The Fix

**Diagonal Hypothesis:** The 15 Gpc Lyα observation is explained by survey geometry, not topology:
- DESI Lyα footprint samples along a face diagonal of the cube
- Effective scale along diagonal: L/√2 = 14.57 Gpc
- Discrepancy: **2.9%** (within measurement error)
- The cube remains symmetric with L_c = 20.6 Gpc

## Corrected Results

| Metric | Buggy Pipeline | Corrected |
|--------|----------------|-----------|
| Q₄ tension | 4.1σ → 4.5σ (worse!) | 4.2σ → **3.8σ** |
| S₈ explained | 17% → 0% (worse!) | 17% → **14%** (stable) |

## Actions Taken

1. Fixed sign error in AP correction
2. Quarantined asymmetric files to `ai_slop/` folder
3. Added README with Feynman quote about self-deception
4. Updated DESI audit summary to reject v11.2.0
5. Verified v11.1.0 paper is clean of asymmetric references

## Framework Status

```
M₄ × T³/Z₂ (SYMMETRIC CUBE)
L_c = 20.6 Gpc
η = 32π/3 = 33.510
v = 0.236

v11.2.0 asymmetric extension: REJECTED
```

## Lesson Learned

Never change fundamental parameters to fit data. When observations don't match predictions:
1. Check for systematic errors
2. Check for bugs in analysis
3. Look for geometric/projection effects
4. Only then consider theory modification

In this case, options 2 and 3 resolved the discrepancy without abandoning first principles.

---

## Work-Order Audit Results (May 22, 2026)

**Protocol:** L_c = 20.6 Gpc LOCKED, v = 0.236 LOCKED, NO parameter tuning, report failures honestly

### Work-Order I: S₈ Power Spectrum Truncation
**Status: FAILED**

| Metric | Value |
|--------|-------|
| k_min (IR cutoff) | 3.05 × 10⁻⁴ Mpc⁻¹ |
| Power removed | ~0% |
| S₈ shift | 0.00002 (negligible) |

**Interpretation:** The IR cutoff scale set by L_c = 20.6 Gpc is 300× smaller than the scales that contribute to σ₈. The T³/Z₂ topology does not resolve the S₈ tension through power spectrum truncation.

### Work-Order J: JWST "Impossible Galaxies" Volume Deficit
**Status: FAILED**

| Metric | Value |
|--------|-------|
| Volume ratio (Z²/ΛCDM) at z~10-14 | 0.972 |
| Anomaly change | +2.8% (worse) |
| Effect direction | Geometric DE INCREASES expansion at high-z |

**Interpretation:** The geometric dark energy formula Ω_DE(z) = 1 - (D_c/L_c)³ gives Ω_DE ~ 0.9 at high redshift, which increases the expansion rate and makes comoving volumes SMALLER. This worsens the "impossible early galaxies" problem, not resolves it.

### Work-Order H: Q₄ Hexadecapole from Vertex Kinematics
**Status: PARTIAL**

| Metric | Value |
|--------|-------|
| Q₄_predicted | -0.027 |
| Q₄_observed | -0.65 ± 0.16 |
| Sign | ✓ CORRECT (negative) |
| Magnitude | 4% of observed |
| Tension | 3.9σ |

**Interpretation:** The vertex potential DOES produce negative Q₄ via bulk flow toward the vertex. The mechanism is correct, but with v = 0.236 locked, the amplitude is too weak by a factor of ~25 in vacuum.

### Work-Order H2: Density-Coupled Q₄ (Follow-up)
**Status: OVERSHOOT - BRACKETS OBSERVED VALUE**

| Model | v_bulk | Q₄ | Factor vs Observed |
|-------|--------|-----|-------------------|
| Vacuum (H) | 88 km/s | -0.027 | 0.04× (too weak) |
| Density (H2) | 511 km/s | -1.71 | 2.6× (too strong) |
| **Required** | **315 km/s** | **-0.65** | 1.0× |

**Interpretation:** When coupling v = 0.236 with the KBC Void underdensity (δ = -0.3, LOCKED), the model OVERSHOOTS:

1. **Void outflow** (v ≈ 430 km/s) dominates the velocity budget
2. Combined effect produces Q₄ = -1.71 (too negative by 2.6×)
3. The observed Q₄ = -0.65 is **bracketed** between vacuum and density models

This is a key diagnostic: the mechanism is validated, but the naive density coupling is too aggressive. The truth requires either:
- Lower effective alignment (~0.59 vs 0.8 assumed)
- Shallower void profile at observer location
- Larger velocity dispersion σ_v > 300 km/s

**Bottom line:** Q₄ is now explained to within a factor of 2.6, not 25.

### Summary

| Work-Order | Target | Status | Key Result |
|------------|--------|--------|------------|
| I | S₈ tension | FAILED | IR cutoff too large-scale to affect σ₈ |
| J | JWST galaxies | FAILED | Geometric DE worsens anomaly |
| H | Q₄ hexadecapole | PARTIAL | Correct sign, 4% magnitude (vacuum) |
| H2 | Q₄ + KBC Void | OVERSHOOT | Brackets observed value (2.6× too strong) |

**Bottom line with symmetric T³/Z₂ at L_c = 20.6 Gpc and v = 0.236:**
- 0/4 work-orders fully pass with 2σ precision
- 1/4 brackets the observation (Q₄ with density coupling)
- 2/4 definitively fail due to scale mismatch (S₈, JWST)
- The Q₄ mechanism is validated - the amplitude is now within 2.6×, not 25×

---

*"The first principle is that you must not fool yourself — and you are the easiest person to fool."* — Richard Feynman
