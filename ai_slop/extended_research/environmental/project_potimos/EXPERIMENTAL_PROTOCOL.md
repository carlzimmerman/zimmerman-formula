# Project Potimos: Experimental Validation Protocol

**Document Type:** Laboratory Protocol for External Partners
**Version:** 1.0
**Date:** May 30, 2026
**Author:** Carl Zimmerman
**License:** CC BY 4.0

---

## Purpose

This protocol provides a step-by-step experimental design to validate the **Surface-Mediated Z-Resonance Hypothesis** identified through computational stress-testing and reconciliation.

**Core Question:** Does pre-adsorption of PFAS onto a Z-geometry surface enhance sonochemical degradation at 517.9 kHz compared to bulk solution?

---

## Executive Summary for Lab Partners

We have computationally identified that:
1. **517.9 kHz** couples with 100% efficiency to C-F stretch (32.2 THz) via broadband cavitation
2. **Surface concentration** at bubble collapse provides 10³× energy amplification
3. **Combined synergy** yields 220× bond energy (sufficient for C-F scission)

**The experiment tests whether this surface concentration mechanism is real.**

---

## Hypothesis

**H₀ (Null):** Degradation rate k(surface) = k(bulk) at 517.9 kHz

**H₁ (Alternative):** Degradation rate k(surface) > k(bulk) at 517.9 kHz by factor ≥ 10×

**Secondary hypothesis:** k(517.9 kHz) > k(500 kHz) for surface-adsorbed PFAS

---

## Experimental Design

### Design Type
2 × 2 Factorial with controls

| Factor | Levels |
|--------|--------|
| Geometry | Bulk solution vs. Surface-adsorbed |
| Frequency | 517.9 kHz vs. 500 kHz |

### Sample Matrix

| ID | Condition | Frequency | n |
|----|-----------|-----------|---|
| A1 | Bulk solution | 517.9 kHz | 5 |
| A2 | Bulk solution | 500.0 kHz | 5 |
| B1 | Surface-adsorbed | 517.9 kHz | 5 |
| B2 | Surface-adsorbed | 500.0 kHz | 5 |
| C0 | Bulk, no sonication | — | 3 |
| C1 | Surface, no sonication | — | 3 |

**Total samples:** 26

---

## Materials

### Chemicals
| Item | Specification | Quantity | Source |
|------|---------------|----------|--------|
| PFOA (Perfluorooctanoic acid) | ≥96% purity | 100 mg | Sigma-Aldrich |
| PFOS (Perfluorooctane sulfonate) | ≥98% purity | 100 mg | Sigma-Aldrich |
| NaF (Sodium fluoride) | ACS grade | 10 g | For F⁻ calibration |
| Methanol | LC-MS grade | 500 mL | Extraction solvent |
| Ammonium acetate | LC-MS grade | 50 g | Mobile phase buffer |
| DI Water | 18.2 MΩ·cm | 10 L | Milli-Q or equivalent |

### Substrate Materials
| Item | Specification | Notes |
|------|---------------|-------|
| **Option A: Activated Carbon** | Granular, 8-20 mesh | Baseline adsorbent |
| **Option B: Graphene Oxide** | Single layer, >99% | 2D surface control |
| **Option C: MoS₂ membrane** | CVD-grown on SiO₂ | Topological candidate |
| **Option D: Stanene** | If available | Ideal Z-geometry |

**Priority:** Start with activated carbon (available), progress to MoS₂ if results positive.

### Equipment
| Item | Specification | Critical? |
|------|---------------|-----------|
| Ultrasonic generator | Adjustable 400-600 kHz, ≥100W | **YES** |
| Frequency counter | ±0.01 kHz accuracy | **YES** |
| Hydrophone | 100 kHz - 1 MHz bandwidth | Recommended |
| Temperature controller | ±1°C, 15-45°C range | **YES** |
| LC-MS/MS | Triple quad, ESI negative | **YES** |
| F⁻ Ion-selective electrode | 0.01-1000 mg/L range | **YES** |
| TOC Analyzer | UV-persulfate method | Recommended |
| pH meter | ±0.01 pH | Yes |

---

## Detailed Procedure

### Phase 1: Preparation (Day 1)

#### 1.1 Stock Solution Preparation
```
PFOA Stock (1000 μg/mL):
1. Weigh 100 mg PFOA into 100 mL volumetric flask
2. Dissolve in 50:50 methanol:water
3. Bring to volume with DI water
4. Store at 4°C in polypropylene (NOT glass)

Working Solution (100 μg/L):
1. Dilute 10 μL stock into 100 mL DI water
2. Prepare fresh daily
```

#### 1.2 Substrate Preparation

**For Activated Carbon:**
```
1. Weigh 500 mg GAC into 50 mL polypropylene tube
2. Wash 3× with DI water to remove fines
3. Dry at 105°C for 2 hours
4. Store in desiccator
```

**For MoS₂ Membrane:**
```
1. Cut 1 cm × 1 cm squares from CVD wafer
2. Clean with acetone → IPA → DI water
3. Dry under N₂
4. Store in clean petri dish
```

#### 1.3 Adsorption Pre-Loading
```
1. Add 100 mg prepared substrate to 50 mL working solution
2. Agitate on orbital shaker at 150 rpm for 4 hours
3. Measure supernatant PFOA concentration (should show >90% removal)
4. Calculate adsorbed mass: m_ads = (C₀ - C_f) × V
5. Decant supernatant, retain loaded substrate
```

### Phase 2: Sonication Experiments (Days 2-4)

#### 2.1 Reactor Setup
```
1. Fill reactor vessel with 200 mL DI water
2. Set temperature to 25 ± 1°C
3. Calibrate frequency to target (517.9 or 500.0 kHz)
4. Verify with frequency counter
5. Set acoustic power to 50 W/L (10 W for 200 mL)
```

#### 2.2 Bulk Solution Protocol (Conditions A1, A2)
```
1. Add PFOA to reactor to achieve 100 μg/L initial concentration
2. Equilibrate 5 minutes with stirring (no sonication)
3. Collect t=0 sample (5 mL)
4. Begin sonication at target frequency
5. Collect samples at t = 5, 15, 30, 60, 120 minutes
6. Store samples at 4°C in polypropylene vials
```

#### 2.3 Surface-Adsorbed Protocol (Conditions B1, B2)
```
1. Add pre-loaded substrate (from Phase 1) to reactor
2. Add 200 mL DI water
3. Equilibrate 5 minutes with stirring
4. Collect t=0 supernatant sample (5 mL)
5. Begin sonication at target frequency
6. Collect supernatant samples at t = 5, 15, 30, 60, 120 minutes
7. At t=120, also collect substrate for extraction
```

#### 2.4 Control Protocols (Conditions C0, C1)
```
Same as above, but NO sonication
Agitate with magnetic stirrer only
Sample at same timepoints
```

### Phase 3: Analysis (Days 5-7)

#### 3.1 PFOA/PFOS Quantification (LC-MS/MS)
```
Column: C18, 2.1 × 50 mm, 1.7 μm
Mobile Phase A: 2 mM ammonium acetate in water
Mobile Phase B: Methanol
Gradient: 10% B → 90% B over 8 min
Flow: 0.3 mL/min
Injection: 10 μL
Detection: MRM negative mode
  PFOA: 413 → 369
  PFOS: 499 → 80

Calibration: 0.1, 1, 10, 50, 100 μg/L
QC: 25 μg/L spike every 10 samples
```

#### 3.2 Fluoride Release (F⁻ ISE)
```
1. Calibrate ISE with NaF standards (0.1, 1, 10, 100 mg/L)
2. Add TISAB III to samples (1:1 ratio)
3. Measure F⁻ concentration
4. Calculate mineralization:
   % Mineralization = (F⁻ measured / F⁻ theoretical) × 100

   For PFOA (C₈HF₁₅O₂): 15 F atoms per molecule
   F⁻ theoretical = [PFOA]₀ × 15 × (19/414) mg F⁻/mg PFOA
```

#### 3.3 Substrate Extraction (for surface samples)
```
1. Transfer substrate to 15 mL centrifuge tube
2. Add 10 mL methanol
3. Sonicate in bath (40 kHz) for 30 minutes
4. Centrifuge 10 min at 3000 rpm
5. Analyze supernatant by LC-MS
6. Calculate: PFOA_remaining = PFOA_extracted + PFOA_supernatant
```

---

## Data Analysis

### 4.1 Kinetic Modeling

Fit pseudo-first-order kinetics:
```
C(t) = C₀ × exp(-k × t)

ln(C/C₀) = -k × t

k = rate constant (min⁻¹)
t₁/₂ = ln(2) / k
```

### 4.2 Statistical Analysis

**Primary comparison:** k(B1) vs k(A1)
- Two-sample t-test (α = 0.05)
- H₁ accepted if: k(B1) > k(A1) with p < 0.05 AND ratio > 10×

**Secondary comparison:** k(517.9 kHz) vs k(500 kHz)
- Paired within each geometry condition
- Report ratio and 95% CI

**ANOVA:** 2×2 factorial
- Main effect of Geometry
- Main effect of Frequency
- Interaction (Geometry × Frequency)

### 4.3 Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Surface enhancement | k(B1)/k(A1) > 10 | Rate constant ratio |
| Frequency specificity | k(517.9)/k(500) > 1.5 | Rate constant ratio |
| Mineralization | F⁻ recovery > 50% | ISE measurement |
| Reproducibility | CV < 20% | Within replicates |

---

## Expected Results

Based on computational reconciliation:

| Condition | Predicted k (min⁻¹) | Predicted t₁/₂ |
|-----------|---------------------|----------------|
| A1: Bulk, 517.9 kHz | 0.03 | 23 min |
| A2: Bulk, 500 kHz | 0.025 | 28 min |
| B1: Surface, 517.9 kHz | **0.3 - 3.0** | **0.2 - 2.3 min** |
| B2: Surface, 500 kHz | 0.15 - 1.5 | 0.5 - 4.6 min |

**The surface enhancement (10-100×) is the key prediction to validate.**

---

## Safety Considerations

### Chemical Hazards
| Hazard | Precaution |
|--------|------------|
| PFAS compounds | Handle in fume hood, wear nitrile gloves |
| Methanol | Flammable, use in ventilated area |
| Ultrasound | Hearing protection if >85 dB |

### Waste Disposal
- PFAS waste: Collect separately, incinerate at >1100°C
- Solvent waste: Halogenated waste stream
- Substrate waste: Depends on material, consult EHS

### PPE Required
- Lab coat
- Safety glasses
- Nitrile gloves (double-glove for PFAS handling)
- Hearing protection during sonication

---

## Timeline

| Week | Activity |
|------|----------|
| 1 | Procure materials, prepare substrates |
| 2 | Adsorption isotherms, method validation |
| 3 | Sonication experiments (n=26) |
| 4 | LC-MS analysis, F⁻ measurements |
| 5 | Data analysis, statistical testing |
| 6 | Report writing |

**Total duration:** 6 weeks

---

## Budget Estimate

| Category | Cost (USD) |
|----------|------------|
| Chemicals | $500 |
| Substrates (GAC, MoS₂) | $1,000 |
| LC-MS consumables | $800 |
| Equipment rental (if needed) | $2,000 |
| Labor (technician, 6 weeks) | $6,000 |
| **Total** | **~$10,300** |

*Note: Costs assume access to existing LC-MS and sonication equipment.*

---

## Reporting

### Minimum Data Package
1. Raw kinetic curves (C vs t) for all conditions
2. Rate constants with 95% CI
3. ANOVA table
4. F⁻ mass balance
5. QA/QC data (blanks, spikes, replicates)

### Publication-Ready Package
- Above, plus:
- Substrate characterization (BET, SEM if available)
- Acoustic field mapping (hydrophone data)
- Temperature profiles during sonication
- Full LC-MS chromatograms

---

## Contact & Collaboration

This protocol is released under CC BY 4.0. Any laboratory may execute it.

**Repository:** github.com/carlzimmerman/zimmerman-formula
**Documentation:** /extended_research/environmental/project_potimos/

For questions or collaboration:
- Open an issue on GitHub
- Reference: Project Potimos Experimental Protocol v1.0

---

## Appendix A: Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│          PROJECT POTIMOS: QUICK REFERENCE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TARGET FREQUENCY:     517.9 kHz (± 0.8 kHz)               │
│  COMPARISON FREQ:      500.0 kHz                           │
│                                                             │
│  PFOA CONCENTRATION:   100 μg/L initial                    │
│  REACTOR VOLUME:       200 mL                              │
│  ACOUSTIC POWER:       50 W/L                              │
│  TEMPERATURE:          25 ± 1°C                            │
│                                                             │
│  TIMEPOINTS:           0, 5, 15, 30, 60, 120 min           │
│  REPLICATES:           n = 5 per condition                 │
│                                                             │
│  SUCCESS CRITERION:    k(surface)/k(bulk) > 10×            │
│                                                             │
│  KEY MEASUREMENT:      LC-MS/MS (PFOA 413→369)             │
│                        F⁻ ISE (mineralization)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Appendix B: Theoretical Basis

The 517.9 kHz frequency derives from:
```
Z = √(32π/3) = 5.7888 Å  (geometric constant)
f_Z = c/Z = 518 PHz       (fundamental frequency)
f_sono = f_Z/10¹² = 517.9 kHz
```

The surface enhancement derives from:
```
Synergy = Thermal × Surface × Coupling × Field
        = 0.26 × 10³ × 0.75 × 1.02
        = 220× bond energy
```

This experiment tests whether the 10³ surface concentration factor is physically real.

---

*Protocol Version 1.0 | Project Potimos | May 2026*
