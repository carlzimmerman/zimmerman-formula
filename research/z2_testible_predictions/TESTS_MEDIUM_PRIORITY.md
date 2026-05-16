# Medium-Priority Tests (3, 4, 7, 8, 10)

**Summary of Tests with Longer Timelines**

---

## Test 3: Spatial Flatness (Ω_k = 0)

### Prediction

Z² predicts **exact spatial flatness**:

```
Ω_k = 0.0000 (exactly zero)
```

This is a topological requirement: T³/Z₂ is flat by construction.

### Current Status

| Measurement | Value | σ |
|-------------|-------|---|
| Planck 2018 | Ω_k = 0.0007 ± 0.0019 | Consistent |
| Planck + BAO | Ω_k = 0.0001 ± 0.0004 | Consistent |

Z² is **fully consistent** with current data.

### Future Precision

```
2025 (DESI):         σ(Ω_k) ~ 0.002
2030 (Euclid):       σ(Ω_k) ~ 0.0005
2035 (combined):     σ(Ω_k) ~ 0.0001
```

### Falsification

Z² falsified if: |Ω_k| > 0.0005 at 5σ (after 2030)

### Notes

This is a **necessary but not sufficient** test - most inflation models also predict Ω_k ≈ 0.

---

## Test 4: CMB Topology Search

### Prediction

The T³/Z₂ topology should produce **matched circles** in the CMB:

```
Angular scale: 40° - 85° (depending on domain size)
Pattern: Pairs of circles with correlated temperatures
Geometry: 8-fold symmetry from fixed points
```

### Search Strategy

1. **Circles-in-the-sky** method
   - Search for pairs of circles with identical temperature patterns
   - Compare T(θ) on candidate circles

2. **Correlation function**
   - Look for periodic features at L_domain scales
   - Expect peaks in ξ(θ) at T³/Z₂ separations

3. **Bayesian model comparison**
   - Compare T³/Z₂ to simply-connected topology
   - Use full CMB likelihood

### Current Status

Planck searched for T³ (without Z₂) and found null results for domains < 0.9 × horizon.

Z² with domain ~ 1.1 × horizon is **not yet constrained**.

### Timeline

- 2025-2027: Dedicated search in Planck data
- 2030+: LiteBIRD higher precision

### Falsification

If exhaustive search finds no topology signature for any domain size → challenges Z² interpretation (but framework could still work with large domain).

---

## Test 7: Fine Structure Constancy

### Prediction

Z² predicts **no variation** in the fine structure constant:

```
Δα/α = 0 exactly (at all redshifts and positions)
```

This follows from: gauge couplings are fixed by topology, not dynamical.

### Current Status

| Measurement | Result | Status |
|-------------|--------|--------|
| Quasar spectra | Δα/α = (0.2 ± 0.6) × 10⁻⁵ | Consistent |
| Atomic clocks | Δα/α < 10⁻¹⁷ /yr | Consistent |
| Oklo reactor | Δα/α < 10⁻⁷ (2 Gyr) | Consistent |
| CMB | Δα/α < 0.4% (z=1100) | Consistent |

**All data consistent with Z² prediction.**

### Future Tests

```
ESPRESSO:     σ(Δα/α) ~ 10⁻⁷ at z ~ 1-2
ELT/ANDES:    σ(Δα/α) ~ 10⁻⁸ at z ~ 2-4
Atomic clocks: σ(Δα/α/yr) ~ 10⁻¹⁹
```

### Falsification

Z² falsified if: |Δα/α| > 10⁻⁶ at any redshift (5σ)

### Notes

This test has **low discrimination** - most theories predict constant α. Useful mainly as a consistency check.

---

## Test 8: Primordial Non-Gaussianity

### Prediction

Z² predicts **very small** non-Gaussianity:

```
f_NL^local ~ 0.01 (close to zero)
f_NL^equil ~ 0.001
f_NL^ortho ~ 0.001
```

This is because: single-field slow-roll inflation with Z² parameters produces minimal non-Gaussianity.

### Current Status

| Parameter | Planck 2018 | Z² Prediction |
|-----------|-------------|---------------|
| f_NL^local | -0.9 ± 5.1 | ~0.01 |
| f_NL^equil | -26 ± 47 | ~0.001 |
| f_NL^ortho | -38 ± 24 | ~0.001 |

Current errors are **too large** to test Z² prediction.

### Future Precision

```
CMB-S4:      σ(f_NL) ~ 1 (still too large)
21cm (2040s): σ(f_NL) ~ 0.1 (marginally sufficient)
Ideal 21cm:  σ(f_NL) ~ 0.01 (would test Z²)
```

### Falsification

Z² falsified if: |f_NL| > 1 at 5σ

### Notes

This is a **long-term test** - may not be feasible until 21cm cosmology matures in the 2040s.

---

## Test 10: Gravitational Wave Phase Coherence

### Prediction

GW from distant sources should show **orbifold periodicity**:

```
Phase coherence at scales ~ L_domain
Potential interference effects from topological copies
```

### Physical Mechanism

In a finite topology, GWs can:
1. Wrap around the universe
2. Interfere with themselves
3. Show phase correlations

### Detection Challenge

This is the **most difficult** test:
1. Requires extremely long baselines
2. Sources must be at cosmological distances
3. Phase measurement precision beyond current capability

### Status

**Not currently testable** with existing technology.

The primary GW test is **Test 2 (h_× = 0)**, which is achievable.

### Future

```
2030s: LISA may provide first constraints
2040s: Next-generation GW observatories
2050+: Space-based GW networks
```

### Falsification

Would require specific phase pattern prediction and measurement - not yet developed.

---

## Summary Table

| Test | Z² Prediction | Current Data | Timeline | Priority |
|------|---------------|--------------|----------|----------|
| 3. Flatness | Ω_k = 0 | Ω_k = 0.0001 ± 0.0004 | 2030s | Medium |
| 4. Topology | T³/Z₂ circles | Not searched | 2025-2030 | Medium |
| 7. Fine structure | Δα/α = 0 | < 10⁻⁵ | Ongoing | Low |
| 8. Non-Gaussianity | f_NL ~ 0.01 | f_NL = -1 ± 5 | 2040s | Low |
| 10. GW phase | Periodic | Not testable | 2050+ | Low |

---

## Recommendation

Focus resources on:
1. **Test 9** (Birefringence) - urgent, 4.9σ tension
2. **Test 2** (GW h_×) - achievable, definitive
3. **Test 5** (Dark energy w) - high discrimination
4. **Test 6** (r value) - LiteBIRD will deliver

Tests 3, 4, 7, 8, 10 provide **supporting evidence** but are not critical path.

---

*Medium-priority tests for Z² Framework*
*May 2026*
