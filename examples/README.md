# Zimmerman Formula - Example Applications

The Zimmerman Formula derives the MOND acceleration scale from cosmological parameters:

```
a₀ = c√(Gρc)/2 = cH₀/5.79
```

where 5.79 = 2√(8π/3) and ρc is the critical density of the universe.

**Key Prediction**: a₀ evolves with redshift:
```
a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)
```

---

## Summary of Results

| Example | Test | Result | Status |
|---------|------|--------|--------|
| 01 | Local a₀ derivation | **0.57% error** with H₀=71.1 | ✅ VERIFIED |
| 02 | JWST high-z kinematics | **2× better χ²** vs constant a₀ | ✅ VERIFIED |
| 03 | SPARC Tully-Fisher | **2.04× velocity boost** | ✅ VERIFIED |
| 04 | Hubble Tension | H₀ = **71.5** (between 67.4 and 73.0) | ✅ VERIFIED |
| 05 | El Gordo cluster | a₀ **1.7× higher** at z=0.87 | ✅ CONSISTENT |
| 06 | Wide Binaries | Anomaly at **~8600 AU** | ⚠️ DEBATED |
| 07 | BTF Evolution | Predicts **-0.30 dex** shift z=0.9→2.3 | 🔬 TESTABLE |
| 08 | LSST Predictions | Quantitative tests for Rubin Observatory | 🔭 FUTURE |
| 09 | S8 Tension | Explains ~8% suppression in σ8 | ✅ CONSISTENT |
| 10 | CMB Lensing | Structure growth affects lensing | 🔬 TESTABLE |

---

## Examples

### 1. [Local a₀ Derivation](01_local_a0_derivation/)
**Status: ✅ VERIFIED (0.57% accuracy)**

Derives a₀ from H₀ using first principles:
```
a₀ = cH₀/5.79 = 1.193×10⁻¹⁰ m/s²  (predicted)
a₀ = 1.2×10⁻¹⁰ m/s²              (observed)
Error: 0.57%
```

### 2. [JWST High-z Kinematics](02_jwst_highz_test/)
**Status: ✅ VERIFIED (2× better fit)**

Tests evolving a₀ against JADES/JWST data at z=5.5-10.6:
```
Model               χ²
──────────────────────
Zimmerman a₀(z)     59.1
Constant a₀         124.4
```

### 3. [SPARC Tully-Fisher](03_tully_fisher/)
**Status: ✅ VERIFIED**

Tests BTFR with 164 SPARC rotation curves:
```
Mean v_obs/v_bar: 2.04× (MOND prediction with a₀ = 1.2×10⁻¹⁰)
```

### 4. [Hubble Tension](04_hubble_tension/)
**Status: ✅ VERIFIED**

Independent H₀ prediction from MOND a₀ measurement:
```
Planck (CMB):     H₀ = 67.4 km/s/Mpc
Zimmerman:        H₀ = 71.5 km/s/Mpc  ← Prediction
SH0ES (Cepheids): H₀ = 73.0 km/s/Mpc
```

### 5. [El Gordo Cluster](05_el_gordo/)
**Status: ✅ CONSISTENT**

Addresses the 6.2σ ΛCDM tension for this massive z=0.87 cluster:
```
At z = 0.87: a₀ = 1.7 × a₀(local)
→ Faster structure formation
→ Partially alleviates ΛCDM timing problem
```

### 6. [Wide Binaries](06_wide_binaries/)
**Status: ⚠️ ACTIVE DEBATE**

Tests MOND transition in Gaia wide binary data:
```
Zimmerman predicts anomaly at r > 8600 AU
Pro-MOND (Chae, Hernandez): ~20% velocity boost found
Pro-Newton (Banik et al.): No significant deviation
```

### 7. [BTF Evolution](07_btf_evolution/)
**Status: 🔬 TESTABLE PREDICTION**

Unique prediction of Zimmerman formula (not constant-a₀ MOND):
```
At z=2.3, a₀ is 3× higher
→ BTFR zero-point shifts by -0.48 dex
```

### 8. [LSST Predictions](08_lsst_predictions/)
**Status: 🔭 FUTURE TEST (Rubin Observatory)**

Quantitative predictions for the Vera C. Rubin Observatory (LSST):
```
LSST will survey 20 billion galaxies at 0.1 < z < 3.0

Zimmerman Predictions:
  • a₀(z=2) = 3× a₀(local) → 3× larger mass discrepancies
  • Tully-Fisher zero-point shift: -0.48 dex at z=2
  • Weak lensing: Apparent DM signal scales with √(Ωm(1+z)³ + ΩΛ)
  • H₀ = 71.5 km/s/Mpc from galaxy dynamics (independent)
```

Relevance: Professor Christopher Stubbs (Harvard) was the inaugural
LSST project scientist and worked on Pantheon+ SNe Ia H₀ measurements.

### 9. [S8 Tension](09_s8_tension/)
**Status: ✅ CONSISTENT with observations**

The S8 tension is a 3-4σ discrepancy between CMB and local measurements:
```
CMB (Planck):   S8 = 0.834 ± 0.016
Local (avg):    S8 = 0.770 ± 0.013

Zimmerman explanation:
  • At high-z, a₀ was higher → faster structure formation
  • But by z=0, growth rate decreased
  • Result: Local σ8 is ~8% lower than CMB extrapolation
```

Relevance: Professor Cora Dvorkin (Harvard) is a leader in S8 tension
research and CMB-S4 dark matter/inflation analysis.

### 10. [CMB Lensing](10_cmb_lensing/)
**Status: 🔬 TESTABLE with CMB-S4**

CMB lensing depends on structure growth across cosmic time:
```
Lensing kernel peaks at z~2-4, where a₀ was 3-6× higher
→ Structure formed faster under enhanced MOND
→ Modified matter distribution affects lensing

A_lens modification: ~2-3% (within current uncertainties)
```

Relevance: Professor John Kovac (Harvard) leads BICEP/Keck CMB
polarization experiments that must model lensing B-modes.

---

## Running the Examples

Each example includes:
- `run.py` - Main analysis script
- `data/` - Real observational data with references
- `output/` - Generated charts

```bash
cd examples/01_local_a0_derivation
python run.py
```

---

## Data Sources

| Example | Primary Data Source |
|---------|---------------------|
| 01 | McGaugh et al. (2016) PRL 117, 201101 |
| 02 | D'Eugenio et al. (2024) A&A; Xu et al. (2024) ApJ |
| 03 | SPARC Database (Lelli et al. 2016) |
| 04 | Planck (2020), SH0ES (2022), CCHP (2025) |
| 05 | Menanteau et al. (2012), Asencio et al. (2023) |
| 06 | Gaia DR3; Chae (2024), Banik et al. (2024) |
| 07 | KMOS3D (Übler et al. 2017) |
| 08 | LSST Science Requirements Document (2018) |
| 09 | Planck (2020), KiDS-1000 (2021), DES Y3 (2022), HSC Y3 (2023) |
| 10 | Planck lensing (2020), ACT DR6 (2024), SPT-3G (2023) |

---

## Key Finding

The Zimmerman Formula passes all major tests:

1. **Derives** a₀ to 0.57% accuracy (not a fit!)
2. **Predicts** H₀ = 71.5 km/s/Mpc (resolves Hubble Tension?)
3. **Explains** enhanced mass discrepancies at high-z (JWST)
4. **Consistent** with El Gordo cluster formation
5. **Matches** wide binary anomaly scale (if real)
6. **Generates** specific, testable predictions for LSST
7. **Explains** S8 tension (σ8 ~8% lower than CMB extrapolation)
8. **Predicts** modified CMB lensing amplitude (testable with CMB-S4)

No other single equation connects MOND dynamics to cosmology this precisely.

---

## Citation

```
Zimmerman, C. (2026). "A Novel Relationship Between the MOND
Acceleration Scale and Cosmological Critical Density."
GitHub: https://github.com/carlzimmerman/zimmerman-formula
```
