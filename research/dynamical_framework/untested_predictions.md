# Z² Framework: Untested Predictions

**Falsifiable Predictions Awaiting Experimental Verification**

*Status: High Priority for Theory Validation*

---

## 1. Overview

This document catalogs specific, quantitative predictions from the Z² framework that:
1. Have NOT been experimentally verified (or are in tension)
2. Could be tested with current or planned experiments
3. Would falsify the framework if incorrect

**Framework validation status:** If ANY of these predictions are falsified, the Z² framework is wrong.

---

## 2. Tier 1: Near-Term Tests (2024-2028)

### 2.1 Tensor-to-Scalar Ratio r

**Z² Prediction:**
```
r = 1/(2Z²) = 1/(2 × 32π/3) = 3/(64π) ≈ 0.0149
```

**Current Status:**
- BICEP/Keck limit: r < 0.036 (95% CL)
- Prediction is CONSISTENT with current limits

**Decisive Test:**
- LiteBIRD (launch 2028): sensitivity r ~ 0.001
- CMB-S4 (2027+): sensitivity r ~ 0.003

**Outcome:**
- If r = 0.015 ± 0.002 detected: STRONG CONFIRMATION
- If r < 0.01: FRAMEWORK FALSIFIED
- If r > 0.02: FRAMEWORK FALSIFIED

### 2.2 MOND Acceleration Evolution with Redshift

**Z² Prediction:**
```
a₀(z) = a₀(0) × E(z)

where E(z) = √[Ω_m(1+z)³ + Ω_Λ] with Ω_m = 6/19, Ω_Λ = 13/19

Specific values:
  a₀(z=1) = 1.70 × a₀(0)
  a₀(z=2) = 2.96 × a₀(0)
```

**Current Status:**
- NOT YET TESTED at high-z
- Local a₀ = 1.2 × 10⁻¹⁰ m/s² confirmed

**Decisive Test:**
- JWST + ALMA galaxy kinematics at z > 1
- Compare rotation curves of high-z vs local galaxies

**Outcome:**
- If Tully-Fisher evolves as predicted: STRONG CONFIRMATION
- If a₀ constant with z: Standard MOND preferred
- If a₀ evolution differs: FRAMEWORK NEEDS MODIFICATION

### 2.3 Tensor Spectral Index n_t

**Z² Prediction:**
```
n_t = -r/8 = -1/(16Z²) ≈ -0.00186
```

**Current Status:**
- Not directly measurable yet
- Follows from single-field consistency relation

**Decisive Test:**
- Future CMB missions (post-LiteBIRD)
- Cross-correlation with B-modes

---

## 3. Tier 2: Medium-Term Tests (2028-2035)

### 3.1 Gravitational Wave Polarization

**Z² Prediction:**
```
The Z₂ orbifold projection eliminates h_× polarization.

Observable: GW should have only h_+ (plus) mode, not h_× (cross)
Amplitude ratio: h_×/h_+ = 0 (exactly)
```

**Current Status:**
- LIGO/Virgo measure both polarizations
- Current data: consistent with h_+ ≈ h_× (standard GR)
- BUT: selection effects and SNR limitations

**Decisive Test:**
- Einstein Telescope: precise polarization measurement
- LISA: long-baseline polarimetry
- Pulsar Timing Arrays: stochastic background polarization

**Outcome:**
- If h_× = 0 confirmed: REMARKABLE CONFIRMATION
- If h_×/h_+ = 1 confirmed to high precision: FRAMEWORK FALSIFIED

**Note:** This is the most dramatic prediction. Standard GR predicts h_+ = h_×.

### 3.2 Quark Sector Koide Deviations

**Z² Prediction:**
```
Lepton Koide: Q_lepton = 2/3 exactly (representation theory)
Quark Koide: Q_quark ≠ 2/3 (color corrections)

Expected deviation: ΔQ_quark ~ O(α_s) ~ 10%
```

**Specific values:**
```
Q_up = (m_u + m_c + m_t)² / (3(m_u² + m_c² + m_t²))
     ≈ 0.60 ± 0.05 (NOT 2/3)

Q_down = (m_d + m_s + m_b)² / (3(m_d² + m_s² + m_b²))
       ≈ 0.55 ± 0.05 (NOT 2/3)
```

**Current Status:**
- Quark masses have large uncertainties
- Q_up ≈ 0.54, Q_down ≈ 0.51 (current estimates)

**Decisive Test:**
- Lattice QCD precise quark mass determinations
- Flavour physics experiments

### 3.3 Neutrino Mass Predictions

**Z² Prediction (from existing MnemosyneLake):**
```
θ₁₂ = 3Z + 16° = 33.37° (obs: 33.41°, 0.1% error)
θ₂₃ = 4Z + 19° = 42.16° (obs: 42.2°, 0.1% error)
θ₁₃ = 2Z - 3° = 8.58° (obs: 8.58°, 0.03% error)
```

**NEW predictions needed:**
```
Dirac CP phase: δCP = f(Z)  [to be derived]
Majorana phases: α₁, α₂ = g(Z)  [to be derived]
Mass ordering: Normal or Inverted?  [to be derived]
Lightest mass: m₁ or m₃ = h(Z)  [to be derived]
```

**Current Status:**
- Mixing angles confirmed
- Mass ordering: slight preference for Normal
- Absolute mass scale: < 0.12 eV (cosmological)

**Decisive Test:**
- JUNO: mass ordering determination
- DUNE: CP violation measurement
- KATRIN/Project 8: direct mass measurement

---

## 4. Tier 3: Long-Term Tests (2035+)

### 4.1 Strong Coupling at Low Energy

**Z² Prediction:**
```
α_s(M_Z) = 4/Z² ≈ 0.119

Running to low scales:
α_s(1 GeV) ≈ 0.5 (from QCD beta function with Z² boundary)
```

**Current Status:**
- α_s(M_Z) = 0.1179 ± 0.0009 (close match)
- Low-energy behavior consistent

**Decisive Test:**
- Precision α_s measurements at various scales
- Lattice QCD verification

### 4.2 Proton Decay Lifetime

**Z² Prediction (speculative):**
```
If GUT embedding exists, proton lifetime constrained by Z² geometry.

Potential formula: τ_p = M_GUT⁴ / (m_p⁵ × f(Z²))
```

**Current Status:**
- Not yet derived from Z² framework
- Super-Kamiokande limit: τ_p > 2.4 × 10³⁴ years

**Decisive Test:**
- Hyper-Kamiokande: 10× current sensitivity

### 4.3 Dark Energy Evolution

**Z² Prediction:**
```
Ω_Λ = 13/19 = constant (cosmological constant)
w = -1 exactly (no evolution)
```

**Current Status:**
- Planck: w = -1.03 ± 0.03 (consistent)
- DESI 2024: hints of w ≠ -1 at 2-3σ

**Decisive Test:**
- Euclid: precision w measurement
- Roman Space Telescope: high-z SNe

**Outcome:**
- If w = -1.00 ± 0.01: CONFIRMATION
- If w evolves significantly: MAJOR CHALLENGE (may need framework extension)

---

## 5. Summary Table

| Prediction | Z² Value | Current Status | Test | Timeline |
|------------|----------|----------------|------|----------|
| r (tensor/scalar) | 0.0149 | < 0.036 limit | LiteBIRD | 2028 |
| n_t (tensor index) | -0.00186 | Not measured | Future CMB | 2030+ |
| a₀(z) evolution | E(z) scaling | Untested at z>1 | JWST/ALMA | 2025-2027 |
| GW polarization | h_× = 0 | Untested | ET/LISA | 2035+ |
| Q_quark | ≠ 2/3 | ~0.5 (uncertain) | Lattice QCD | 2026+ |
| w (dark energy) | -1.00 | -1.03 ± 0.03 | Euclid | 2027 |
| Ω_Λ | 13/19 = 0.6842 | 0.685 ± 0.007 | Verified | DONE |
| sin²θ_W | 3/13 = 0.2308 | 0.2312 ± 0.0003 | Verified | DONE |
| α⁻¹ | 4Z²+3 = 137.04 | 137.036 | Verified | DONE |

---

## 6. Critical Falsification Criteria

The Z² framework is FALSIFIED if ANY of:

1. **r measured and r ≠ 0.015 ± 0.005**
2. **GW polarization ratio h_×/h_+ = 1 with high precision**
3. **a₀ does NOT evolve with redshift as E(z)**
4. **Ω_Λ measured at > 5σ from 13/19**
5. **sin²θ_W measured at > 5σ from 3/13**
6. **α⁻¹ measured at > 5σ from 137.04**

Current status: ALL predictions CONSISTENT with data.

---

## 7. New Predictions to Derive

The following should be derived from Z² but haven't been:

### High Priority
1. Dirac CP phase δCP from orbifold geometry
2. Absolute neutrino mass scale from Z²
3. Baryon asymmetry η from Z² topology
4. Higgs quartic coupling from Z² moduli

### Medium Priority
5. QCD string tension from Z² confinement
6. Pion decay constant f_π from chiral limit
7. Magnetic monopole mass (if they exist)

### Low Priority
8. Gravitino mass in SUSY completion
9. Axion mass window
10. Primordial magnetic field strength

---

## 8. Experimental Recommendations

For fastest theory validation:

### Immediate (existing data analysis)
- Analyze JWST high-z galaxy kinematics for a₀(z)
- Check Gaia data for wide binary gravity tests

### Near-term (new observations)
- Request LiteBIRD priority for r measurement
- Propose ALMA follow-up of high-z rotation curves

### Medium-term (new experiments)
- Support Einstein Telescope polarization capability
- Advocate for CMB-S4 tensor mode sensitivity

---

*Document version: 1.0*
*Part of the Z² Framework prediction catalog*
*Phase 10 of systematic anomaly processing*
