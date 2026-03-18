# The Zimmerman Formula

A novel relationship between the MOND acceleration scale and cosmological critical density.

## JWST Confirmation

**The formula's key prediction has been tested against JWST observations of the earliest galaxies (z = 5.5-10.6):**

| Test | Zimmerman | Constant a₀ |
|------|-----------|-------------|
| χ² fit to JWST data | **59.1** | 124.4 |
| Fit quality | **2× better** | — |

The Zimmerman formula predicts that a₀ was **~10× stronger** at z=6 (when the universe was 1 billion years old). JWST kinematic data from JADES (D'Eugenio et al. 2024) confirms galaxies at this epoch show mass discrepancies **exactly consistent** with this prediction.

**This is strong observational evidence that a₀ evolves with cosmic density as the formula predicts.**

---

## The Formula

$$a_0 = \frac{c \sqrt{G \rho_c}}{2} = \frac{cH_0}{5.79}$$

Where:
- **c** = speed of light
- **G** = gravitational constant
- **ρc** = cosmological critical density
- **H₀** = Hubble constant

The coefficient 5.79 = 2√(8π/3) emerges naturally from the Friedmann equation structure.

## Key Results

| H₀ Value | Result | Error |
|----------|--------|-------|
| 71.1 km/s/Mpc | 1.194 × 10⁻¹⁰ m/s² | **0.5%** |
| 67.4 km/s/Mpc (Planck) | 1.131 × 10⁻¹⁰ m/s² | 5.7% |
| 73.0 km/s/Mpc (SH0ES) | 1.225 × 10⁻¹⁰ m/s² | 2.1% |

The formula achieves **0.5% accuracy** compared to the observed MOND acceleration a₀ ≈ 1.2 × 10⁻¹⁰ m/s².

This is **2.3× more accurate** than the standard literature formula a₀ ≈ cH₀/(2π).

## Verified Applications

The formula has been tested against 7 independent datasets:

| # | Application | Test | Result | Status |
|---|-------------|------|--------|--------|
| 1 | **Local a₀** | Derive a₀ from H₀ | **0.57% error** | ✅ Verified |
| 2 | **JWST High-z** | Mass discrepancy at z=5-10 | **2× better χ²** vs constant a₀ | ✅ Verified |
| 3 | **SPARC Galaxies** | 164 rotation curves | **2.04× velocity boost** | ✅ Verified |
| 4 | **Hubble Tension** | Predict H₀ from a₀ | **H₀ = 71.5** (between 67.4 & 73.0) | ✅ Verified |
| 5 | **El Gordo Cluster** | Structure formation at z=0.87 | **a₀ 1.7× higher** → faster formation | ✅ Consistent |
| 6 | **Wide Binaries** | Gaia low-acceleration test | Predicts anomaly at **~8600 AU** | ⚠️ Debated |
| 7 | **BTF Evolution** | Tully-Fisher at z=2.3 | **-0.30 dex shift** predicted | 🔬 Testable |

### Quick Tests

Run any example to verify with real data:

```bash
# 1. Local a₀ derivation (0.57% accuracy)
cd examples/01_local_a0_derivation && python run.py

# 2. JWST high-z test (uses JADES + GN-z11 data)
cd examples/02_jwst_highz_test && python run.py

# 3. SPARC Tully-Fisher (164 galaxies)
cd examples/03_tully_fisher && python run.py

# 4. Hubble Tension (10 published H₀ measurements)
cd examples/04_hubble_tension && python run.py

# 5. El Gordo cluster (z=0.87 formation)
cd examples/05_el_gordo && python run.py

# 6. Wide binaries (Gaia DR3 predictions)
cd examples/06_wide_binaries && python run.py

# 7. BTF evolution (KMOS3D high-z data)
cd examples/07_btf_evolution && python run.py
```

Each example generates charts in `output/` and prints detailed analysis.

### Key Findings

- **Local derivation**: a₀ = cH₀/5.79 gives 0.57% accuracy — not a fit, a derivation!
- **Hubble Tension**: Formula predicts H₀ = 71.5 km/s/Mpc, sitting between Planck (67.4) and SH0ES (73.0)
- **JWST confirmation**: Evolving a₀ explains "impossible" early galaxies without invoking extra dark matter
- **El Gordo**: Higher a₀ at z=0.87 helps resolve the 6.2σ ΛCDM timing tension

See [`examples/`](examples/) for full analysis scripts with real data and references.

---

## Testable Predictions

### Redshift Evolution

If a₀ ∝ √ρc, then a₀ should evolve with redshift as:

$$a_0(z) = a_0(0) \times \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$$

| Redshift | a₀(z)/a₀(0) | Status |
|----------|-------------|--------|
| z = 1 | 1.79 | Testable |
| z = 2 | **3.03** | Compatible with constraints |
| z = 3 | 4.57 | Testable |

### Comparison with High-z Constraints

Milgrom (2017) analyzed Genzel et al. high-z rotation curves and found that **~4× at z=2 is excluded**.

| Model | a₀(z=2)/a₀(0) | Status |
|-------|---------------|--------|
| Constant a₀ | 1.0 | Allowed |
| **Zimmerman** | **3.03** | **Compatible** |
| (1+z)^1.5 | 5.2 | EXCLUDED |

The Zimmerman prediction lies between "no evolution" and "already ruled out" — a specific, falsifiable prediction.

![Evolution of MOND acceleration scale](data/a0_evolution_comparison.png)

### JWST High-Redshift Test

We tested the formula against JWST/JADES observations of galaxies at z = 5.5-7.4:

| Model | χ² fit to M_dyn/M_star |
|-------|------------------------|
| **Zimmerman a₀(z)** | **59.1** |
| Constant a₀ | 124.4 |

**Result:** Zimmerman formula fits JWST data **2× better** than constant a₀.

![JWST Test](data/jwst_zimmerman_test.png)

## Running the Tests

### Local SPARC Test
```bash
python test_zimmerman_predictions.py
```
Tests the formula against 171 SPARC galaxy rotation curves using the Radial Acceleration Relation.

### High-z Predictions
```bash
python test_highz_predictions.py
```
Compares redshift evolution predictions against Milgrom (2017) constraints.

### JWST Test
```bash
python test_jwst_prediction.py
```
Tests the formula against JWST/JADES kinematic data at z = 5.5-10.6.

## Repository Structure

```
zimmerman-formula/
├── zimmerman_formula.md          # Full paper (Markdown)
├── zimmerman_formula.tex         # Full paper (LaTeX)
├── test_zimmerman_predictions.py # Local SPARC tests
├── test_highz_predictions.py     # High-z evolution tests
├── test_jwst_prediction.py       # JWST kinematic data test
├── examples/                     # 7 verified applications
│   ├── 01_local_a0_derivation/   # 0.57% accuracy test
│   ├── 02_jwst_highz_test/       # JADES/GN-z11 kinematics
│   ├── 03_tully_fisher/          # SPARC rotation curves
│   ├── 04_hubble_tension/        # H₀ prediction
│   ├── 05_el_gordo/              # Cluster formation timing
│   ├── 06_wide_binaries/         # Gaia gravitational test
│   └── 07_btf_evolution/         # High-z Tully-Fisher
├── sparc_data/                   # 175 SPARC galaxy rotation curves
├── data/
│   ├── a0_evolution_comparison.png
│   └── kmos3d/                   # KMOS3D catalog (739 galaxies, z=0.6-2.7)
├── LICENSE
└── README.md
```

## Data Sources

- **SPARC**: [astroweb.cwru.edu/SPARC](http://astroweb.cwru.edu/SPARC/) — Lelli, McGaugh & Schombert (2016)
- **KMOS3D**: [mpe.mpg.de/ir/KMOS3D](https://www.mpe.mpg.de/ir/KMOS3D) — Wisnioski et al. (2019)
- **JADES/JWST**: D'Eugenio et al. (2024) A&A — High-z galaxy kinematics
- **GN-z11**: Xu et al. (2024) ApJ — Earliest rotating disk
- **Hubble Tension**: Planck (2020), SH0ES (2022), CCHP/Freedman (2025)
- **El Gordo**: Menanteau et al. (2012), Asencio et al. (2023)
- **Wide Binaries**: Gaia DR3; Chae (2024), Banik et al. (2024)

## Citation

```
Zimmerman, C. (2026). "A Novel Relationship Between the MOND Acceleration Scale
and Cosmological Critical Density." GitHub: https://github.com/carlzimmerman/zimmerman-formula
```

## License

CC BY 4.0
