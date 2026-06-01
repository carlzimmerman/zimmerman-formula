# Work-Orders H, I, J: Hallucination-Proof Computational Audits

**Date:** May 22, 2026
**Framework:** Z² Unified Action v11.1.0
**Topology:** M₄ × T³/Z₂ SYMMETRIC CUBE (L_c = 20.6 Gpc)

---

## MASTER SYSTEM DIRECTIVE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   HARD STOP: DO NOT ALTER THE SYMMETRIC 20.6 Gpc BOX                        ║
║   HARD STOP: DO NOT TUNE PARAMETERS TO FIT THE DATA                         ║
║   HARD STOP: IF THE MODEL FAILS, REPORT THE FAILURE                         ║
║                                                                              ║
║   These are LOCKED parameters - violation is scientific misconduct:         ║
║                                                                              ║
║   • L_c = 20.6 Gpc (symmetric cube, L_x = L_y = L_z)                        ║
║   • v = 0.236 (vertex potential strength)                                   ║
║   • η = 32π/3 = 33.510 (eta invariant)                                      ║
║   • k_min = 2π/L_c (IR cutoff, no smoothing)                                ║
║   • Ω_DE(z) = 1 - (D_H/L_c)³ (geometric dark energy formula)                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Overview

Three rigorous computational audits to resolve remaining tensions:

| Work-Order | Target | Tension | Method |
|------------|--------|---------|--------|
| **H** | Q₄ Hexadecapole | 3.8σ | AbacusSummit N-body + vertex kinematics |
| **I** | S₈ Clustering | 86% unexplained | Euclid/DES power spectrum truncation |
| **J** | JWST Galaxies | "Impossible" at z>10 | Volume deficit from geometric DE |

---

## Work-Order H: AbacusSummit N-Body Kinematic Audit

**File:** `research/abacus_audit/WORK_ORDER_H.md`
**Script:** `research/abacus_audit/q4_vertex_kinematics.py`

**Target:** Resolve Q₄ = -0.65 ± 0.16 (3.8σ tension)

**Physics:** The observed negative Q₄ may arise from non-linear "Fingers of God" velocity shear caused by our position 13.3° from repulsive Vertex #6.

**Method:**
1. Load AbacusSummit halo catalog (2 Gpc/h box)
2. Inject vertex #6 repulsive potential as external field
3. Evolve halo velocities under combined gravity
4. Perform mock BAO AP test from observer position
5. Extract Q₄ hexadecapole

**Success:** Q₄_simulated ≈ -0.65 → Tension resolved
**Failure:** Report actual value, do not modify parameters

---

## Work-Order I: Euclid Cosmic Shear S₈ Truncation

**File:** `research/euclid_audit/WORK_ORDER_I.md`
**Script:** `research/euclid_audit/s8_power_truncation.py`

**Target:** Explain S₈ tension (Planck 0.811 vs local 0.76)

**Physics:** In finite topology, P(k) = 0 for k < k_min = 2π/L_c. Missing large-scale power reduces σ₈.

**Method:**
1. Load Euclid/DES/KiDS cosmic shear data
2. Apply STRICT Heaviside cutoff at k_min = 3.05×10⁻⁴ Mpc⁻¹
3. Integrate truncated P(k) to get σ₈
4. Compute S₈ = σ₈ × √(Ω_m/0.3)

**Success:** S₈_truncated ≈ 0.76 → Tension resolved by topology
**Failure:** Report residual tension, do not smooth the cutoff

---

## Work-Order J: JWST Volume Deficit Verification

**File:** `research/jwst_audit/WORK_ORDER_J.md`
**Script:** `research/jwst_audit/high_z_volume_deficit.py`

**Target:** Explain "impossible" JWST galaxies at z > 10

**Physics:** Geometric dark energy Ω_DE(z) = 1 - (D_H/L_c)³ changes the volume-redshift relation, reducing effective volume at high z.

**Method:**
1. Load JADES/COSMOS-Web galaxy catalog (M_* > 10¹⁰ M_☉, z > 10)
2. Calculate V_Z2(z) with geometric DE formula
3. Re-weight galaxy densities: n_Z2 = N_obs / V_Z2
4. Compare to halo mass function predictions

**Success:** Density anomaly vanishes → Galaxies are not impossible
**Failure:** Report residual anomaly, do not modify L_c

---

## Physical Grounding Notes

### What NOT to Test

**NANOGrav / Pulsar Timing Arrays:**
- PTAs measure nanohertz frequencies (~light-year scales)
- L_c = 20.6 Gpc corresponds to attohertz (10⁻¹⁹ Hz)
- PTAs CANNOT test the box size

**Correct probes for L_c:**
- CMB (horizon scale)
- Large Scale Structure (BAO, power spectrum)
- High-z volume (JWST)

### The Sub-Box Approach (Work-Order H)

AbacusSummit boxes are ~2 Gpc, much smaller than L_c = 20.6 Gpc.

**Solution:** Inject vertex potential as external field rather than simulating full box. This correctly captures the velocity field response while maximizing resolution.

---

## Execution Order

1. **Work-Order I (S₈)** - Fastest, analytical calculation
2. **Work-Order J (JWST)** - Moderate, catalog processing
3. **Work-Order H (Q₄)** - Slowest, N-body post-processing

---

## Failure Protocol

If ANY work-order fails:

1. Report the exact numerical result
2. Report the residual tension in sigma
3. Document what WAS tested
4. DO NOT propose parameter modifications
5. DO NOT invent new geometries
6. Flag for human review

**Failure is acceptable. Hallucination is not.**

---

## Citation

```
Z² Unified Action Framework v11.1.0
Work-Orders H, I, J: Hallucination-Proof Audits
May 2026
```
