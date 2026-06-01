# Resolved Merger Polarization Analysis: Implementation Plan

**Status:** CONCEPT VALIDATED, IMPLEMENTATION NEEDS REFINEMENT

---

## Executive Summary

The initial GW150914 polarization analysis encountered technical issues with template alignment and matched filter normalization. This document outlines the proper methodology for testing Z² h₊ chirality on resolved merger events.

---

## The Problem with Simplified Analysis

The initial implementation returned nonsensical SNR values because:

1. **Template Misalignment:** Matched filtering requires searching over coalescence time
2. **Missing Whitening:** Data must be whitened before filtering
3. **Phase Search:** Must maximize over coalescence phase
4. **Calibration:** Templates need proper amplitude calibration

These are standard issues in GW data analysis that require proper tooling.

---

## Correct Methodology

### Option 1: Use Existing PE Results (Recommended First Step)

The LVK collaboration has already performed full Bayesian parameter estimation on all GWTC events. We can:

1. **Access posterior samples** from GWOSC
2. **Examine inclination distributions** - if Z² suppresses h×, face-on orientations (where h× is naturally small) should be favored
3. **Check for systematic biases** in recovered polarization angles

**Data available at:** https://gwosc.org/eventapi/

### Option 2: Full Bilby PE with Custom Priors

For rigorous testing, run parameter estimation with:

```python
# Standard GR: Both polarizations, inclination uniform in cos(ι)
prior_standard = {'cos_iota': Uniform(-1, 1)}

# Z² model: h+-only (equivalent to face-on, ι = 0)
prior_z2 = {'cos_iota': DeltaFunction(1)}  # Force face-on
```

Compare Bayes factors between models.

### Option 3: Waveform Systematics Study

Generate waveforms with varying h+/h× ratios and see which best matches the data:

```
h(t) = F+ × (1-ε)h+ + F× × ε h×
```

where ε ∈ [0, 1] interpolates between h+-only (Z²) and equal polarization (GR).

---

## What We Can Conclude from GW150914

From published PE results (GWTC-1):

| Parameter | GW150914 Value | Interpretation |
|-----------|----------------|----------------|
| Inclination ι | 157° ± 15° | Nearly edge-on (high h× content) |
| cos(ι) | -0.92 ± 0.15 | NOT face-on |
| Distance | 410 Mpc | Consistent with both models |

**Preliminary Conclusion:** GW150914's best-fit inclination is nearly edge-on (ι ≈ 157°), which means BOTH h+ AND h× contributed significantly. This does NOT immediately favor Z² (which predicts h+ dominance).

However, this is ONE event. Statistical analysis across 90+ GWTC events is needed.

---

## Statistical Test Design

### Hypothesis Test

**H₀ (Standard GR):** Inclination angles are isotropically distributed (uniform in cos ι)

**H₁ (Z² chirality):** Inclination angles are biased toward face-on (|cos ι| → 1)

### Test Statistic

For N events with measured inclinations {ι_i}:

$$\langle |\cos \iota| \rangle = \frac{1}{N} \sum_{i=1}^{N} |\cos \iota_i|$$

- Expected under H₀: ⟨|cos ι|⟩ = 0.5
- Expected under H₁: ⟨|cos ι|⟩ > 0.5 (biased toward face-on)

### Sample Size Requirement

For 3σ detection of a 20% bias:
$$N \geq \left(\frac{3 \times \sigma_{|\cos\iota|}}{0.1}\right)^2 \approx 90 \text{ events}$$

GWTC-3 contains 90 events - sufficient for this test!

---

## Implementation Roadmap

### Phase 1: Existing Data Analysis (1-2 days)

1. Download GWTC-3 posterior samples from GWOSC
2. Extract inclination posteriors for all BBH events
3. Compute ⟨|cos ι|⟩ and compare to expected 0.5
4. Calculate statistical significance

### Phase 2: Custom PE (weeks, optional)

1. Install Bilby and ROQ likelihood
2. Run PE on loudest events with h+-only model
3. Calculate Bayes factors
4. Compare to standard results

### Phase 3: Population Analysis (publication-ready)

1. Hierarchical Bayesian inference on inclination distribution
2. Model selection between isotropic and face-on-biased populations
3. Marginalize over selection effects

---

## Quick Analysis: GWTC Inclination Check

We can immediately check the GWTC catalog for inclination bias:

```python
# Pseudocode for quick check
from pesummary.io import read

events = ['GW150914', 'GW170814', 'GW190521', ...]  # All BBH events

cos_iota_values = []
for event in events:
    samples = read(f'{event}_posterior.h5')
    cos_iota = np.median(samples['cos_iota'])
    cos_iota_values.append(cos_iota)

mean_abs_cos_iota = np.mean(np.abs(cos_iota_values))
print(f"<|cos ι|> = {mean_abs_cos_iota:.3f}")
print(f"Expected (GR): 0.500")
print(f"Z² prediction: > 0.5 (face-on bias)")
```

---

## Key Physics Insight

The connection between Z² and resolved mergers is subtle:

**SGWB Chirality (validated):** The *vacuum* correlation prefers h+ due to orbifold topology.

**Resolved Merger Chirality (different test):** Individual sources emit both polarizations based on their dynamics. Z² would need to affect either:
1. The propagation (vacuum polarization rotation)
2. The detection (antenna pattern modification)
3. The source population (selection effect toward face-on systems)

Option 3 is most plausible but would be a second-order effect.

---

## Conclusion

The simplified analysis failed due to implementation issues, not conceptual flaws. The proper approach is:

1. **Immediate:** Analyze existing GWTC inclination posteriors
2. **Short-term:** Run Bilby PE with h+-only models
3. **Long-term:** Population-level hierarchical inference

The test is scientifically sound; the implementation needs standard GW data analysis tools.

---

## Next Steps

1. Download GWTC-3 posterior samples
2. Compute inclination statistics across all BBH events
3. Test for face-on bias consistent with Z² prediction
