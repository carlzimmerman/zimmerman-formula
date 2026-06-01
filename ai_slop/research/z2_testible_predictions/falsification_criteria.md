# Z² Framework: Explicit Falsification Criteria

**Precisely Defined Thresholds for Ruling Out the Framework**

---

## Philosophy

A scientific theory must be **falsifiable**. The Z² framework makes specific predictions that can be definitively tested. This document lists exact criteria for falsification.

The convention used: **5σ deviation from prediction = falsification**

---

## Tier 1: Single-Measurement Falsifications

These tests can falsify Z² with **a single clear result**.

### 1. Cosmic Birefringence (Test 9)

**CURRENT STATUS: 4.9σ TENSION**

| Parameter | Z² Prediction | Falsification Threshold |
|-----------|---------------|------------------------|
| β | 0.00° | |β| > 0.10° at 5σ |

```
Current: β = 0.33° ± 0.07° → 4.9σ tension

FALSIFIED IF: LiteBIRD measures β = 0.33° ± 0.01°
              (33σ from Z² prediction)
```

### 2. GW Cross-Polarization (Test 2)

| Parameter | Z² Prediction | Falsification Threshold |
|-----------|---------------|------------------------|
| h_×/h_+ | 0.00 | h_×/h_+ > 0.30 in any event at 5σ |
| <h_×/h_+> | 0.00 | <h_×/h_+> > 0.10 over 20+ events |

```
FALSIFIED IF: Single event shows h_× ≈ h_+ at high confidence
              OR statistical ensemble inconsistent with zero
```

### 3. Dark Energy Equation of State (Test 5)

| Parameter | Z² Prediction | Falsification Threshold |
|-----------|---------------|------------------------|
| w₀ | -1.000 | |w₀ + 1| > 5σ(w₀) |
| wₐ | 0.000 | |wₐ| > 5σ(wₐ) |

```
Current: w₀ = -0.55 ± 0.21 → 2.5σ tension

FALSIFIED IF: Euclid measures w₀ = -0.55 ± 0.02
              (22.5σ from Z² prediction)
```

### 4. Tensor-to-Scalar Ratio (Test 6)

| Parameter | Z² Prediction | Falsification Window |
|-----------|---------------|---------------------|
| r | 0.0149 | r < 0.012 OR r > 0.018 at 5σ |

```
FALSIFIED IF: LiteBIRD measures r = 0.003 ± 0.002
              (6σ from Z² prediction)

FALSIFIED IF: LiteBIRD measures r = 0.025 ± 0.002
              (3.8σ from Z² prediction, need more precision)
```

---

## Tier 2: Statistical Falsifications

These require accumulated evidence from multiple measurements.

### 5. Cosmological Densities

| Parameter | Z² Prediction | Observed | Tolerance |
|-----------|---------------|----------|-----------|
| Ω_Λ | 0.6842 (13/19) | 0.685 ± 0.007 | ±0.035 (5σ) |
| Ω_m | 0.3158 (6/19) | 0.315 ± 0.007 | ±0.035 (5σ) |
| Ω_Λ/Ω_m | 2.167 | 2.17 ± 0.07 | ±0.35 |

```
FALSIFIED IF: Combined χ² for densities exceeds 5σ threshold
              after accounting for correlations
```

### 6. Spatial Flatness (Test 3)

| Parameter | Z² Prediction | Falsification Threshold |
|-----------|---------------|------------------------|
| Ω_k | 0.0000 | |Ω_k| > 0.0025 at 5σ |

```
Current: Ω_k = 0.0001 ± 0.0004

FALSIFIED IF: Future measurement gives Ω_k = 0.003 ± 0.0005
              (6σ from zero)
```

### 7. Fine Structure Constant (Test 7)

| Parameter | Z² Prediction | Falsification Threshold |
|-----------|---------------|------------------------|
| Δα/α | 0.0000 | |Δα/α| > 5 × 10⁻⁶ at 5σ |

```
FALSIFIED IF: Quasar spectra show systematic variation
              at any redshift
```

---

## Tier 3: Cumulative Falsifications

These would falsify Z² through **multiple independent tensions**.

### Combined Tension Threshold

If multiple tests show modest tensions that individually don't reach 5σ:

```
Combined χ² = Σ_i (x_i - x_i^Z²)² / σ_i²

FALSIFIED IF: Combined χ² corresponds to p < 10⁻⁶
              (approximately 5σ for multiple tests)
```

### Example Scenario

| Test | Tension |
|------|---------|
| Birefringence | 3σ |
| Dark energy | 2σ |
| r value | 2σ |
| GW h_× | 2σ |

Combined: χ² = 9 + 4 + 4 + 4 = 21 (4 DOF) → p = 3×10⁻⁴ → ~3.5σ

This would be **concerning but not falsifying**. Need 5σ combined.

---

## What Does NOT Falsify Z²

### Insufficient Evidence

1. **Hints below 3σ**: Require confirmation
2. **Single anomalous event**: Could be systematic
3. **Theoretical objections**: Must have observational support
4. **Alternative models fitting data**: Not sufficient without Z² failing

### Modifications Allowed

These would require framework modification but not complete rejection:

1. **BEKENSTEIN ≠ 4**: Already acknowledged as weakest prediction
2. **Crystal magic angle amplitude differs**: Could indicate coupling uncertainty
3. **n_s tension**: Known issue, may be resolved by reheating

---

## Current Status Summary

| Test | Prediction | Current Tension | Status |
|------|------------|-----------------|--------|
| 9. Birefringence | β = 0° | **4.9σ** | **CRITICAL** |
| 5. Dark energy | w = -1 | 2.5σ | TENSION |
| 6. r value | r = 0.0149 | < 1σ | OK |
| 2. GW h_× | h_× = 0 | Not tested | PENDING |
| 3. Flatness | Ω_k = 0 | < 1σ | OK |
| 7. Fine structure | Δα/α = 0 | < 1σ | OK |
| Others | Various | < 1σ | OK |

### Overall Assessment

```
┌──────────────────────────────────────────────────────┐
│  Z² STATUS: AT RISK                                  │
│                                                      │
│  Critical tension: Cosmic birefringence (4.9σ)      │
│  Secondary tension: Dark energy w (2.5σ)            │
│                                                      │
│  If birefringence confirmed at 5σ → FALSIFIED       │
│  If both tensions disappear → SURVIVES              │
│                                                      │
│  Expected resolution: LiteBIRD ~2032                │
└──────────────────────────────────────────────────────┘
```

---

## Decision Timeline

```
2024-2025:
  - Planck PR4 birefringence update
  - If β reduced to < 0.1°: Z² survives
  - If β confirmed at > 0.3°: Z² likely dead

2025-2027:
  - LIGO O4/O5 h_× test
  - If h_× ≠ 0 detected: Z² FALSIFIED
  - If h_× = 0 confirmed: Major support for Z²

2027-2030:
  - DESI/Euclid w(z) measurement
  - If w = -1 confirmed: Z² supported
  - If w ≠ -1 at 5σ: Z² FALSIFIED

2030-2032:
  - LiteBIRD r measurement
  - LiteBIRD β measurement
  - DEFINITIVE VERDICT ON Z²
```

---

## Honest Acknowledgment

The Z² framework may be falsified by existing data:

- **Cosmic birefringence at 4.9σ** is close to the 5σ discovery threshold
- If this measurement holds up, Z² as currently formulated is wrong
- We present this honestly as part of scientific integrity

The framework will be tested definitively within the next decade. Either:
1. Z² is confirmed as a valid description of fundamental physics
2. Z² is falsified, providing a valuable constraint on viable topologies

Both outcomes advance scientific understanding.

---

*Explicit falsification criteria for Z² Framework*
*Updated: May 2026*
