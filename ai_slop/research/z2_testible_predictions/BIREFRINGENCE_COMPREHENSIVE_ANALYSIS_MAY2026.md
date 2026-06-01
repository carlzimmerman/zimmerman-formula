# Cosmic Birefringence: Comprehensive Analysis

**The Critical Test for Z² Framework**

**Carl Zimmerman | May 2026**

---

## Executive Summary

Cosmic birefringence — the rotation of CMB polarization by angle β — is the **most serious tension** facing the Z² framework. This document compiles all available data as of May 2026.

| Parameter | Z² Prediction | Latest Data | Tension |
|-----------|---------------|-------------|---------|
| β (isotropic) | 0° exactly | 0.30° ± 0.05° | ~6σ |
| Combined Planck+ACT | 0° | ~7σ detection | **CRITICAL** |

**Bottom Line:** Multiple independent experiments now show consistent ~0.2-0.3° birefringence signal. If this is cosmological (not systematic), Z² is falsified.

---

## 1. Latest Measurements (2024-2026)

### 1.1 Planck PR4/NPIPE Results

| Analysis | β (degrees) | Uncertainty | Significance | Reference |
|----------|-------------|-------------|--------------|-----------|
| Diego-Palazuelos et al. (2022) | 0.30 | ±0.11 | 2.7σ | arXiv:2203.04830 |
| Frequency-combined | 0.33 | ±0.10 | 3.3σ | A&A 2022 |
| PR4 map-space (Sullivan 2025) | 0.46-0.48 | ±0.04 (stat) ±0.28 (syst) | — | arXiv:2502.07654 |
| Scale-independence test | 0.30 | ±0.05 | 6σ | arXiv:2507.16714 |

**Key Point:** Planck alone shows ~3-6σ signal depending on analysis method.

### 1.2 ACT DR6 Results (September 2025)

| Measurement | Value | Source |
|-------------|-------|--------|
| β | 0.215° ± 0.074° | arXiv:2509.13654 |
| Significance | 2.9σ | |
| Frequency bands | f090, f150, f220 | |
| Sky coverage | 19,000 deg² | |

**Critical Quote from ACT team:**
> "There remain systematics in the ACT data that are not understood and do not allow us to draw strong cosmological conclusions."

### 1.3 Combined Analysis (October 2025)

From arXiv:2510.25489 (SPIDER + Planck + ACT):

| Combination | Detection Significance |
|-------------|----------------------|
| Planck alone | ~5σ |
| ACT alone | 2.9σ |
| **Planck + ACT** | **~7σ** |
| SPIDER + Planck + ACT | ~7σ (SPIDER contributes little) |

**WARNING:** The 7σ is for α+β (instrumental + cosmic rotation combined). The cosmic component β cannot yet be unambiguously separated.

### 1.4 Summary of All Measurements

```
Experiment       β (degrees)    Significance    Notes
─────────────────────────────────────────────────────────
Planck PR3       0.35 ± 0.14    2.5σ           Original M&K
Planck PR4       0.30 ± 0.11    2.7σ           Updated
Planck freq-comb 0.33 ± 0.10    3.3σ           Multi-freq
Planck latest    0.30 ± 0.05    6σ             Scale-indep
ACT DR6          0.215 ± 0.074  2.9σ           Independent
Planck+ACT       —              ~7σ            Combined
─────────────────────────────────────────────────────────

WEIGHTED AVERAGE: β ≈ 0.25-0.30°
COMBINED SIGNIFICANCE: 5-7σ
```

---

## 2. Z² Prediction: β = 0 Exactly

### 2.1 Why Z² Predicts Zero Birefringence

The T³/Z₂ orbifold topology eliminates pseudoscalar fields:

1. **Birefringence requires:** Chern-Simons coupling φ F·F̃
2. **φ must be pseudoscalar:** φ(-x) = -φ(x) under parity
3. **Z₂ identification:** Points x and -x are identified
4. **At fixed points:** φ(x) = φ(-x) = -φ(x) → φ = 0
5. **Zero mode forbidden:** Constant pseudoscalar not allowed
6. **Result:** No large-scale axion-like field exists

```
Mathematical summary:
  H¹(T³/Z₂) = 0  (no harmonic 1-forms survive)
  → No axion-like field
  → No φ F·F̃ coupling
  → β = 0 exactly
```

### 2.2 This is Topological Protection

The β = 0 prediction is NOT fine-tuned. It's a consequence of the orbifold geometry. There is no parameter to adjust — the prediction is exact.

---

## 3. Systematic Uncertainties

### 3.1 The Core Degeneracy Problem

The observed rotation α_obs is a combination of:
- **Cosmic birefringence (β):** Real physics
- **Instrumental miscalibration (α):** Systematic error

```
α_obs = α_instrument + β_cosmic
```

**Current experiments cannot unambiguously separate these.**

### 3.2 Galactic Dust EB Correlation

The Minami-Komatsu method assumes intrinsic dust EB = 0. This may be wrong:

| Source | Potential Contribution |
|--------|----------------------|
| Magnetic field helicity | ~0.01-0.05° |
| Filament chirality | ~0.02-0.10° |
| Line-of-sight integration | ~0.01-0.05° |
| **Total plausible** | **0.05-0.15°** |

If dust EB ~ 0.1°, true β_cosmic would be:
```
β_cosmic = β_measured - β_dust = 0.30° - 0.10° = 0.20°
```

This reduces but doesn't eliminate the tension with Z².

### 3.3 Planck vs ACT Tension

Concerning finding from arXiv:2510.25489:
> "The rotation angle inferred independently from Planck and ACT differ by >3σ"

This could indicate:
- Different instrumental systematics
- Frequency-dependent effects
- Statistical fluctuation
- Hint that some signal is instrumental

### 3.4 ACT's Explicit Caution

The ACT team explicitly states:
> "There remain systematics in the ACT data that are not understood"

This is unusual candor in a discovery paper and suggests the ~7σ combined significance should be treated with caution.

---

## 4. Physical Interpretation (If Real)

### 4.1 Axion-Like Particles (ALPs)

If β ≠ 0 is cosmological, it implies:

```
Lagrangian: L ⊃ (g_aγ/4) φ F_μν F̃^μν

Birefringence: β = (g_aγ/2) × Δφ

where Δφ = φ(z=0) - φ(z=1100)
```

### 4.2 Mass Constraints on ALPs

| ALP Mass | Behavior | Implication |
|----------|----------|-------------|
| m < 10⁻³³ eV | Frozen (dark energy) | Could explain β ~ 0.3° |
| m ~ 10⁻³²-10⁻²⁸ eV | Oscillating | Reduced β signal |
| m > 10⁻²⁸ eV | Fast oscillations | β averages to ~0 |

### 4.3 Connection to DESI Dark Energy Results

Intriguing correlation: DESI hints at evolving dark energy (w ≠ -1), and birefringence could arise from the same axion-like field.

If both are real:
- Z² falsified by birefringence (β ≠ 0)
- Z² falsified by dark energy (w ≠ -1)
- Double falsification from related physics

---

## 5. Future Experiments

### 5.1 LiteBIRD (Launch ~2028, Results ~2031)

From arXiv:2503.22322 (March 2025):

| Parameter | Specification |
|-----------|---------------|
| Sensitivity σ(β) | ~0.02-0.06° (depending on pipeline) |
| Detection of β = 0.3° | 5-13σ (depending on systematics) |
| Frequency bands | 15 (34-448 GHz) |
| Sky coverage | Full sky |

**LiteBIRD will be DEFINITIVE:**
- If β = 0.30° → detected at 5-13σ → **Z² falsified**
- If β = 0.00° → null result → **Z² supported**, current hints were systematic

### 5.2 Other Near-Term Experiments

| Experiment | Timeline | σ(β) Expected |
|------------|----------|---------------|
| Simons Observatory | 2025-2028 | ~0.05° |
| CMB-S4 | 2030s | ~0.02° |
| AliCPT-1 | 2025+ | ~0.1° |

### 5.3 Improvement Factor

> "Upcoming CMB observations by Simons Observatory, LiteBIRD and CMB-S4 could reduce current uncertainties by a factor of approximately 7."

---

## 6. Assessment for Z² Framework

### 6.1 Current Status

| Aspect | Status |
|--------|--------|
| Z² prediction | β = 0° exactly |
| Latest measurement | β ≈ 0.30° ± 0.05° |
| Raw tension | ~6σ |
| After dust systematic | ~3-4σ |
| Combined experiments | ~7σ (with caveats) |

### 6.2 Honest Probability Assessment

| Scenario | Estimated Probability | Outcome for Z² |
|----------|----------------------|----------------|
| β is real (~0.3°) | ~60% | **FALSIFIED** |
| β is reduced by systematics (~0.15°) | ~25% | Strong tension |
| β is entirely systematic (~0°) | ~15% | Supported |

### 6.3 What Z² Needs to Survive

For Z² to survive, one of the following must be true:

1. **Dust EB systematic is larger than thought** (~0.2-0.3°)
   - Current evidence: dust EB < 0.15° likely
   - Probability: ~10%

2. **Instrumental miscalibration explains signal**
   - Multiple independent experiments see same thing
   - Probability: ~10%

3. **Statistical fluctuation**
   - At 6-7σ, extremely unlikely
   - Probability: <1%

4. **Unknown systematic**
   - Possible but would need to affect all experiments similarly
   - Probability: ~5-10%

**Combined probability Z² survives: ~15-25%**

---

## 7. Comparison with Other Z² Tensions

| Observable | Z² Prediction | Observation | Tension | Severity |
|------------|---------------|-------------|---------|----------|
| **Birefringence β** | 0° | 0.30° | 6σ | **CRITICAL** |
| Dark energy w | -1 | -1.03 ± 0.03 | 1σ | OK |
| Ω_Λ/Ω_m | 2.167 | 2.172 | 0.1σ | Excellent |
| n_s | 0.967 | 0.965 | 0.5σ | Excellent |

**Birefringence is by far the most serious tension.**

---

## 8. Timeline to Resolution

| Date | Milestone | Expected Outcome |
|------|-----------|------------------|
| 2025-2026 | Simons Observatory first light | Improved constraints |
| 2026-2027 | ACT final analysis | Better systematics understanding |
| ~2028 | LiteBIRD launch | — |
| ~2030 | LiteBIRD science operations | — |
| **~2031** | **LiteBIRD results** | **DEFINITIVE ANSWER** |

---

## 9. Conclusions

### 9.1 Key Findings

1. **Multiple experiments** (Planck, WMAP, ACT) consistently measure β ~ 0.2-0.3°
2. **Combined significance** reaches ~7σ, though with caveats about systematics
3. **Z² predicts β = 0 exactly** — no adjustable parameter
4. **Dust systematics** may contribute ~0.1° but likely cannot explain entire signal
5. **LiteBIRD** will be definitive by ~2031

### 9.2 For Z² Framework

**Current Status: CRITICAL TENSION**

The birefringence measurement is the most serious challenge to Z². Unlike other predictions where there is flexibility, β = 0 is a hard topological prediction.

If the signal is real:
- Z² in its current form is **falsified**
- Would need fundamental modification (different orbifold?)
- Other Z² successes (Ω_Λ/Ω_m, n_s) may still point toward related framework

If the signal is systematic:
- Z² gains **strong support**
- Would be remarkable confirmation of topological prediction
- Would rule out axion-like dark energy/matter

### 9.3 Recommended Posture

**Intellectual honesty requires acknowledging:**
- Current data disfavors Z² (β = 0 prediction)
- ~15-25% chance Z² survives via systematics
- Must wait for LiteBIRD for definitive answer
- Framework should be prepared for falsification

---

## Sources

- [SPIDER+Planck+ACT Combined Analysis (October 2025)](https://arxiv.org/abs/2510.25489)
- [ACT DR6 Birefringence (September 2025)](https://arxiv.org/abs/2509.13654)
- [Planck PR4 Scale Independence (July 2025)](https://arxiv.org/html/2507.16714v1)
- [LiteBIRD Birefringence Forecast (March 2025)](https://arxiv.org/abs/2503.22322)
- [Planck PR4 NPIPE Map-Space (February 2025)](https://arxiv.org/abs/2502.07654)
- [Planck PR4 Cosmic Birefringence (2022)](https://arxiv.org/abs/2203.04830)
- [Minami & Komatsu Original Detection (2020)](https://www.mpa-garching.mpg.de/896049/news20201123)

---

*Document: Comprehensive Birefringence Analysis*
*Part of Z² Framework Research*
*May 2026*
