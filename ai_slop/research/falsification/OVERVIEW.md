# Falsification Tests

## The Framework Is Falsifiable

The Zimmerman framework makes **testable predictions** that can be proven wrong.

## Core Prediction

```
a₀(z) = a₀(0) × E(z)

where E(z) = √[Ωm(1+z)³ + ΩΛ]
```

**If observations show constant a₀ at all redshifts, the framework is DEAD.**

## Specific Falsification Criteria

### Test 1: BTFR Evolution

The Baryonic Tully-Fisher Relation should shift with redshift:
```
Δlog M_bar = -log₁₀(E(z))

Predictions:
| z | Offset (dex) |
|---|--------------|
| 1 | -0.23 |
| 2 | -0.47 |
| 3 | -0.67 |
```

**Data:** KMOS3D, ELT spectroscopy of high-z galaxies

**Falsification:** If BTFR shows NO offset at z > 1

### Test 2: RAR Scale Evolution

The Radial Acceleration Relation transition scale g† should evolve:
```
g†(z) = g†(0) × E(z)
```

**Data:** Galaxy rotation curves at different redshifts

**Falsification:** If g† is constant across redshifts

### Test 3: Wide Binary Test

At local scales, a₀ = cH₀/Z should give:
```
a₀ = (3×10⁸) × (2.2×10⁻¹⁸) / 5.79 = 1.13×10⁻¹⁰ m/s²
```

**Data:** Chae (2025) wide binary analysis

**Result:** a₀ ≈ 1.2×10⁻¹⁰ m/s² ✓ (6% agreement within H₀ uncertainty)

### Test 4: Hubble Constant

```
H₀ = Z × a₀ / c = 5.79 × (1.2×10⁻¹⁰) / (3×10⁸) = 71.5 km/s/Mpc
```

**Falsification:** If H₀ is definitively measured far from 71.5

## Files in This Directory

| File | Description |
|------|-------------|
| Various falsification test scripts | Check `output/` for results |

## How to Run

```bash
cd output
# Check generated plots and analysis
```

## Current Status

| Test | Result |
|------|--------|
| a₀ value | ✓ Confirmed (1.2×10⁻¹⁰ m/s²) |
| H₀ prediction | Pending (71.5 vs 67-73 tension) |
| BTFR evolution | Awaiting high-z data |
| RAR evolution | Awaiting high-z data |

## Why This Matters

A framework that cannot be falsified is not science. The Zimmerman framework:
1. **Makes specific predictions** (a₀(z) evolution)
2. **Predicts measurable offsets** (BTFR, RAR)
3. **Can be tested with existing/near-future data** (JWST, ELT, KMOS3D)

**If these predictions fail, the framework fails.**
