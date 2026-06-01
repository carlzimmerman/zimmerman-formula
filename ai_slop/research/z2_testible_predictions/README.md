# Z² Framework: Testable Predictions

**Comprehensive Analysis of Experimental Tests for the T³/Z₂ Orbifold Topology**

**Carl Zimmerman | May 2026**

---

## Executive Summary

The Z² framework makes **sharp, falsifiable predictions** that distinguish it from parameter-fitted alternatives. This directory contains detailed analyses of experimental tests, organized by timeline and discrimination power.

### Critical Status

| Priority | Test | Z² Prediction | Current Status | Discrimination |
|----------|------|---------------|----------------|----------------|
| **URGENT** | Birefringence | β = 0° | β = 0.33° ± 0.07° | **4.9σ TENSION** |
| HIGH | GW h_× = 0 | Exact null | Testable 2025-2027 | Definitive |
| HIGH | Dark energy w | w = -1.000 | DESI hints w ≠ -1 | 2.5σ tension |
| HIGH | r value | 0.0149 ± 0.0005 | r < 0.036 | LiteBIRD decisive |
| MEDIUM | Crystal angle | 0.56% at 35.26° | Testable NOW | Laboratory |

---

## The Z² Constant

All predictions derive from the single topological constant:

```
Z² = 32π/3 = 33.510321638291...

Origin: η-invariant of T³/Z₂ orbifold with 8 fixed points
       η(T³/Z₂) = 8 × (4π/3) = 32π/3
```

### Derived Quantities

| Quantity | Expression | Value | Physical Meaning |
|----------|------------|-------|------------------|
| Z | √(32π/3) | 5.788810 | Fundamental scale |
| Ω_Λ | 13/19 | 0.684211 | Dark energy density |
| Ω_m | 6/19 | 0.315789 | Matter density |
| r | 1/(2Z²) | 0.01492 | Tensor-to-scalar |
| θ_magic | arctan(1/√2) | 35.264° | Crystal alignment |
| N_modes | 8 + 11 | 19 | Fixed + bulk modes |

---

## Directory Contents

### High-Priority Tests

| File | Test | Status |
|------|------|--------|
| `TEST_01_crystal_magic_angle.md` | Condensed matter alignment | **Testable NOW** |
| `TEST_02_gw_cross_polarization.md` | h_× = 0 null test | LIGO O4/O5 |
| `TEST_05_dark_energy_w.md` | w(z) evolution | DESI/Euclid |
| `TEST_06_tensor_to_scalar.md` | r = 0.0149 | LiteBIRD 2030s |
| `TEST_09_cosmic_birefringence.md` | β = 0° | **4.9σ TENSION** |

### Medium-Priority Tests

| File | Test | Timeline |
|------|------|----------|
| `TEST_03_spatial_flatness.md` | Ω_k = 0 exactly | 2030s |
| `TEST_04_cmb_topology.md` | T³/Z₂ circles | Planck/LiteBIRD |
| `TEST_07_fine_structure.md` | Δα/α = 0 | Current data |
| `TEST_08_non_gaussianity.md` | f_NL ~ 0.01 | 2040s (21cm) |
| `TEST_10_gw_phase_coherence.md` | Orbifold periodicity | Future |

### Supporting Documents

| File | Description |
|------|-------------|
| `falsification_criteria.md` | Explicit thresholds for ruling out Z² |
| `experimental_contacts.md` | Researchers and collaborations |
| `timeline_2024_2035.md` | Experimental roadmap |
| `statistical_methods.md` | Detection power calculations |

---

## Falsification Criteria

The Z² framework is **immediately falsifiable** if:

### Definitive Falsifications (Single Measurement)

1. **Cosmic birefringence β ≠ 0 at 5σ**
   - Current: 4.9σ tension (β = 0.33° ± 0.07°)
   - LiteBIRD: σ ~ 0.01° → decisive by 2032
   - **If confirmed: Z² is falsified**

2. **GW cross-polarization h_× ≠ 0**
   - Any single detection with h_×/h_+ > 0.1 at 5σ falsifies Z²
   - ~10 events needed for statistical confirmation
   - O4/O5 can achieve this 2025-2027

3. **Dark energy w ≠ -1 at 5σ**
   - DESI current: w₀ = -0.55 (2.5σ from ΛCDM)
   - If evolving w confirmed, Z² is falsified
   - Euclid will be decisive by 2030

4. **Tensor-to-scalar outside window**
   - Z² predicts: r = 0.0149 ± 0.0005
   - Falsified if: r < 0.012 OR r > 0.018
   - LiteBIRD detection at 7.5σ expected if Z² correct

### Cumulative Falsifications

5. **Cosmological densities wrong at 3σ combined**
   - Ω_Λ = 13/19 = 0.6842 (Planck: 0.685 ± 0.007) ✓
   - Ω_m = 6/19 = 0.3158 (Planck: 0.315 ± 0.007) ✓
   - Currently excellent agreement

---

## Immediate Actions

### What Can Be Done NOW

1. **Crystal Magic Angle Test** (Test 1)
   - Equipment: Standard cryostat, lock-in amplifier
   - Sample: Single-crystal Si or Ge
   - Procedure: Rotate relative to CMB dipole
   - Prediction: 0.56% resistivity drop at 35.26°
   - Cost: ~$50k (existing lab equipment)
   - Timeline: 6-12 months

2. **GW Archive Analysis** (Test 2)
   - Reanalyze O3 events for h_× content
   - No new observations needed
   - Statistical framework ready (Fisher matrix)

3. **Birefringence Update** (Test 9)
   - Request latest Planck PR4 + ACT/SPT combined analysis
   - Current tension may reduce or increase
   - Critical for Z² survival

---

## Statistical Framework

### Detection Power Calculations

For each test, we compute:

1. **Required Sample Size** for 95% detection power
2. **χ² Discrimination** between Z² and alternatives
3. **Bayesian Model Selection** (Bayes factors)
4. **Systematic Error Budget**

### Monte Carlo Validations

All analytical predictions verified by simulation:
- 10,000+ realizations per test
- Full covariance matrices
- Realistic noise models

---

## Key Physical Mechanisms

### Why h_× = 0 (GW Cross-Polarization)

The Z₂ orbifold projection eliminates odd-parity modes:
```
h_μν → P(Z₂) h_μν

Cross-polarization transforms as: h_× → -h_×
Plus-polarization transforms as:  h_+ → +h_+

Under Z₂: only Z₂-even modes survive → h_× = 0
```

### Why β = 0 (Cosmic Birefringence)

No axion-like field exists on T³/Z₂:
```
Axion: φ ∝ ε^μνρσ F_μν F_ρσ

On T³/Z₂: No harmonic 1-forms survive projection
         H¹(T³/Z₂; ℝ) = 0

Result: No axionic coupling → No birefringence
```

### Why w = -1 (Dark Energy)

Moduli stabilization freezes the vacuum:
```
V(ψ) = V₀ + ½m²|ψ|² + ...

At minimum: ψ = 0, V = V₀ = constant

p = -ρ exactly → w = p/ρ = -1
```

### Why r = 1/(2Z²) (Tensor-to-Scalar)

Z₂ projection halves tensor power:
```
Standard: P_T = (2/π²)(H/M_Pl)²

Z₂ orbifold: P_T → P_T/2 (odd modes projected out)

r = P_T/P_S = (1/2) × (1/Z²) = 1/(2Z²) = 0.0149
```

---

## Connection to Main Framework

This directory expands on:
- `/papers/Z2_UNIFIED_ACTION_v9.5.0.md` (Appendix G)
- `/research/experimental_tests/experimental_tests_analysis.py`
- `/research/experimental_tests/experimental_tests_analysis.png`

All predictions derive from the unified action:
```
S₇ = (1/16πG₇) ∫ d⁷x √(-g₇) [R₇ - 2Λ₇ + L_gauge + L_matter]
```

compactified on M₄ × T³/Z₂.

---

## Critical Path to Validation or Falsification

```
2024-2026: Crystal magic angle (laboratory)
           Fine structure constancy (quasar spectra)

2025-2027: GW h_× test (LIGO O4/O5)
           Birefringence update (Planck PR4)

2027-2030: LiteBIRD r measurement
           DESI/Euclid w(z) constraints

2030-2035: Combined CMB/LSS analysis
           21cm cosmology begins

DECISION POINT: By 2030, Z² will be either:
  - Strongly confirmed (all predictions match)
  - Definitively falsified (β ≠ 0, w ≠ -1, or h_× ≠ 0)
```

---

## The Stakes

If Z² survives all tests, it represents:
- First complete unification from pure topology
- Resolution of dark energy mystery
- Explanation of cosmic coincidences
- New physics paradigm

If Z² fails (most likely via birefringence):
- Valuable negative result
- Constrains alternative topologies
- Methods applicable to other frameworks
- Demonstrates proper falsifiability

Either outcome advances physics.

---

*Part of Z² Framework research*
*May 2026*
