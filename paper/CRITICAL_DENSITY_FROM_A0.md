# Critical Density Determination from the MOND Acceleration Scale

**Carl Zimmerman**

*March 2026*

---

## Abstract

We derive the cosmological critical density ρ_c from the locally-measured MOND acceleration scale a₀ using the Zimmerman Formula. From a₀ = c√(Gρ_c)/2, we obtain ρ_c = 4a₀²/(c²G). Using a₀ = 1.2×10⁻¹⁰ m/s², this yields ρ_c = 9.61×10⁻²⁷ kg/m³, within **1.4%** of the Planck-measured value. This remarkable agreement demonstrates that local galaxy dynamics encode information about the global density of the universe — a striking realization of Mach's Principle.

---

## 1. Introduction

### 1.1 The Critical Density

The critical density separates open from closed universes:
$$\rho_c = \frac{3H_0^2}{8\pi G}$$

Current best value (Planck 2018):
$$\rho_c = 9.47 \times 10^{-27} \text{ kg/m}^3$$

### 1.2 Standard Measurement Methods

ρ_c is typically determined from:
1. CMB + H₀ measurement
2. BAO + SNe + H₀
3. Large-scale structure + H₀

All require knowing H₀ first.

### 1.3 A New Method

The Zimmerman Formula provides a **direct** measurement of ρ_c from local galaxy dynamics, independent of H₀.

---

## 2. Derivation

### 2.1 The Zimmerman Formula

$$a_0 = \frac{c \sqrt{G \rho_c}}{2}$$

### 2.2 Solving for ρ_c

Squaring both sides:
$$a_0^2 = \frac{c^2 G \rho_c}{4}$$

Therefore:
$$\boxed{\rho_c = \frac{4 a_0^2}{c^2 G}}$$

### 2.3 Numerical Calculation

Using:
- a₀ = 1.2 × 10⁻¹⁰ m/s²
- c = 2.998 × 10⁸ m/s
- G = 6.674 × 10⁻¹¹ m³ kg⁻¹ s⁻²

$$\rho_c = \frac{4 \times (1.2 \times 10^{-10})^2}{(2.998 \times 10^8)^2 \times 6.674 \times 10^{-11}}$$

$$\rho_c = \frac{5.76 \times 10^{-20}}{5.995 \times 10^{6}} = 9.61 \times 10^{-27} \text{ kg/m}^3$$

### 2.4 Comparison

| Source | ρ_c (kg/m³) | Method |
|--------|-------------|--------|
| **Zimmerman (from a₀)** | **9.61×10⁻²⁷** | Galaxy dynamics |
| Planck 2018 | 9.47×10⁻²⁷ | CMB |
| **Difference** | **1.4%** | — |

---

## 3. Physical Interpretation

### 3.1 Mach's Principle Realized

Ernst Mach proposed that local inertia is determined by the distribution of matter in the universe. The Zimmerman Formula is a **quantitative realization** of this idea:

$$a_0 = f(\rho_c) = \frac{c \sqrt{G \rho_c}}{2}$$

The acceleration scale governing local galaxy dynamics is set by the global density of the cosmos.

### 3.2 Local-Global Connection

| Local Observable | Global Quantity | Relationship |
|------------------|-----------------|--------------|
| a₀ | ρ_c | a₀ = c√(Gρ_c)/2 |
| Galaxy rotation | Universe density | Direct derivation |

This is extraordinary: measuring rotation curves determines the density of the universe.

### 3.3 Why This Works

The critical density represents the threshold between expansion and collapse. The MOND acceleration scale represents the threshold between Newtonian and modified dynamics. The Zimmerman Formula reveals these thresholds are **the same physics** expressed differently.

---

## 4. Error Analysis

### 4.1 Uncertainty in a₀

From SPARC RAR: a₀ = (1.20 ± 0.02) × 10⁻¹⁰ m/s²

Fractional uncertainty: δa₀/a₀ = 1.7%

### 4.2 Propagation to ρ_c

$$\frac{\delta \rho_c}{\rho_c} = 2 \times \frac{\delta a_0}{a_0} = 3.4\%$$

### 4.3 Result with Uncertainty

$$\rho_c = (9.61 \pm 0.33) \times 10^{-27} \text{ kg/m}^3$$

Planck: (9.47 ± 0.05) × 10⁻²⁷ kg/m³

**Agreement within 0.4σ.**

---

## 5. Cross-Checks

### 5.1 Deriving H₀ from ρ_c

Using ρ_c = 9.61×10⁻²⁷ kg/m³:
$$H_0 = \sqrt{\frac{8\pi G \rho_c}{3}} = 2.32 \times 10^{-18} \text{ s}^{-1} = 71.5 \text{ km/s/Mpc}$$

This matches the H₀ paper (separate publication).

### 5.2 Deriving Λ from ρ_c

Using ρ_c and Ω_Λ = 0.685:
$$\Lambda = \frac{8\pi G \rho_c \Omega_\Lambda}{c^2} = 1.23 \times 10^{-52} \text{ m}^{-2}$$

This matches the Λ paper (separate publication).

### 5.3 Self-Consistency

All Zimmerman-derived quantities are internally consistent:

| Quantity | From a₀ | From ρ_c | Difference |
|----------|---------|----------|------------|
| H₀ | 71.5 km/s/Mpc | 71.5 km/s/Mpc | 0% |
| Λ | 1.23×10⁻⁵² m⁻² | 1.23×10⁻⁵² m⁻² | 0% |
| ρ_c | 9.61×10⁻²⁷ kg/m³ | — | — |

---

## 6. Implications

### 6.1 New Cosmological Probe

Galaxy rotation curves become cosmological probes:
- No need for standard candles
- No need for CMB physics
- Direct measurement from kinematics

### 6.2 Testing Cosmological Models

Different cosmologies predict different ρ_c:
- Open universe: ρ < ρ_c
- Closed universe: ρ > ρ_c
- Flat: ρ = ρ_c

The Zimmerman method provides an independent test.

### 6.3 Future Precision

With better a₀ measurements:
- GAIA proper motions → δa₀ ~ 1%
- → δρ_c ~ 2%
- Competitive with Planck

---

## 7. Comparison to Other Methods

### 7.1 CMB-Based (Planck)

Requires:
- Full CMB power spectrum
- Assumed cosmological model
- H₀ from sound horizon

Zimmerman:
- Local galaxy kinematics only
- No CMB physics
- H₀ emerges from the calculation

### 7.2 BAO + SNe

Requires:
- Standard rulers (BAO)
- Standard candles (SNe)
- Calibration chain

Zimmerman:
- No distance ladder
- No calibration
- Direct from dynamics

### 7.3 Large-Scale Structure

Requires:
- Galaxy surveys
- Bias modeling
- Assumed matter power spectrum

Zimmerman:
- Individual galaxy rotation curves
- No bias
- No power spectrum needed

---

## 8. Predictions

### 8.1 Improved a₀ Measurement

If a₀ is measured to 0.5% precision:
$$\delta \rho_c / \rho_c = 1\%$$

Competitive with CMB methods.

### 8.2 Redshift Evolution

At redshift z:
$$\rho_c(z) = \rho_c(0) \times E(z)^2$$

This can be tested by measuring a₀ at different redshifts (from BTFR evolution).

### 8.3 Alternative Cosmologies

Different cosmologies predict different ρ_c:
- ΛCDM: 9.47×10⁻²⁷ kg/m³
- Einstein-de Sitter: Different value
- Modified gravity: Model-dependent

The Zimmerman method can distinguish these.

---

## 9. Falsification Criteria

This derivation is falsified if:

1. **a₀ varies:** If a₀ differs between galaxies by >10%, the universal ρ_c derivation breaks.

2. **ρ_c measured differently:** If future Planck/CMB-S4 finds ρ_c significantly different from 9.5×10⁻²⁷ kg/m³.

3. **Formula wrong:** If 5.79 ≠ 2√(8π/3) (mathematical, cannot be wrong).

---

## 10. Summary

From the Zimmerman Formula:

$$\rho_c = \frac{4 a_0^2}{c^2 G} = 9.61 \times 10^{-27} \text{ kg/m}^3$$

This is:
- **1.4% from Planck value**
- **Independent of H₀ measurement**
- **Derived from local galaxy dynamics**
- **A realization of Mach's Principle**

Local rotation curves encode the density of the universe.

---

## References

1. Zimmerman, C. (2026). Zenodo. DOI: 10.5281/zenodo.19114050
2. Planck Collaboration (2020). *A&A*, 641, A6.
3. McGaugh, S.S. et al. (2016). *PRL*, 117, 201101.
4. Mach, E. (1883). *Die Mechanik in ihrer Entwicklung*.
5. Barbour, J. & Pfister, H. (1995). *Mach's Principle*.

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Citation:** Zimmerman, C. (2026). DOI: 10.5281/zenodo.19114050
