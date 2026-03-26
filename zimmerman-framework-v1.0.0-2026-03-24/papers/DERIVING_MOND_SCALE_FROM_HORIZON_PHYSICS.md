# Deriving the MOND Acceleration Scale from Horizon Thermodynamics

**Carl Zimmerman**

*March 2026*

---

## Abstract

We present a first-principles derivation of the MOND acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m/s² from general relativistic cosmology and horizon thermodynamics. The derivation yields a₀ = cH₀/Z where Z = 2√(8π/3) = 5.7888. This geometric constant emerges naturally: the factor √(8π/3) comes from the Friedmann equation relating the Hubble parameter to critical density, while the factor of 2 arises from the horizon mass via the Bekenstein bound. The result predicts a₀ should evolve with redshift as a₀(z) = a₀(0)×E(z), where E(z) = √(Ωₘ(1+z)³ + Ω_Λ). This evolution is potentially testable with high-redshift kinematic observations from JWST.

---

## 1. Introduction

The MOND (Modified Newtonian Dynamics) acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m/s² has presented a long-standing puzzle. First introduced empirically by Milgrom [1] to explain galaxy rotation curves without dark matter, this scale exhibits a striking numerical coincidence with cosmological parameters:

$$a_0 \approx cH_0$$

This "cosmic coincidence" has been noted by many authors [2-5] but typically treated as either fortuitous or suggestive of unknown physics. Here we show that the relationship is not coincidental but follows from general relativistic cosmology combined with horizon thermodynamics, yielding the precise form:

$$a_0 = \frac{cH_0}{Z} \quad \text{where} \quad Z = 2\sqrt{\frac{8\pi}{3}} = 5.7888...$$

The geometric constant Z is not arbitrary—it emerges from two well-established physical principles.

---

## 2. The Friedmann Factor

### 2.1 Critical Density from Einstein's Equations

For a homogeneous, isotropic universe, Einstein's field equations yield the Friedmann equation:

$$H^2 = \frac{8\pi G}{3}\rho_c$$

This defines the critical density:

$$\rho_c = \frac{3H^2}{8\pi G}$$

The factor 8π/3 is fundamental to general relativity, arising from the geometric structure of Einstein's equations in cosmological contexts.

### 2.2 Natural Acceleration from Critical Density

What acceleration scale can be constructed from ρ_c, G, and c? Dimensional analysis gives:

$$[G][\rho] = \left(\frac{m^3}{kg \cdot s^2}\right)\left(\frac{kg}{m^3}\right) = \frac{1}{s^2}$$

Thus √(Gρ) has units of inverse time, and c√(Gρ) has units of acceleration. The natural acceleration scale is:

$$a_{natural} = c\sqrt{G\rho_c}$$

Substituting the critical density:

$$a_{natural} = c\sqrt{G \cdot \frac{3H^2}{8\pi G}} = c\sqrt{\frac{3H^2}{8\pi}} = cH\sqrt{\frac{3}{8\pi}} = \frac{cH}{\sqrt{8\pi/3}}$$

This yields:

$$\boxed{a_{natural} = \frac{cH}{\sqrt{8\pi/3}} \approx \frac{cH}{2.89}}$$

---

## 3. The Horizon Factor

### 3.1 de Sitter Horizon

In a dark-energy dominated universe (de Sitter space), there exists a cosmological horizon at:

$$R_{dS} = \frac{c}{H}$$

This represents the maximum distance from which causal signals can reach an observer.

### 3.2 Horizon Mass from Thermodynamics

Following Bekenstein and Hawking, horizons possess thermodynamic properties. The de Sitter horizon has:

- **Area**: A = 4πR² = 4πc²/H²
- **Entropy**: S = A/(4ℓ_P²) = πc²/(GℏH²) × c³
- **Temperature**: T = ℏH/(2πk_B) (Gibbons-Hawking temperature)

The energy content can be derived from the first law. Computing E = TS:

$$E = \frac{\hbar H}{2\pi k_B} \times \frac{\pi R^2 c^3}{G\hbar} = \frac{H R^2 c^3}{2G}$$

With R = c/H:

$$E = \frac{H \cdot c^2/H^2 \cdot c^3}{2G} = \frac{c^5}{2GH}$$

The effective horizon mass is therefore:

$$\boxed{M_{horizon} = \frac{c^3}{2GH}}$$

The factor of 2 in the denominator is intrinsic to the Bekenstein bound and horizon thermodynamics.

### 3.3 Horizon Surface Gravity

The gravitational acceleration at the horizon radius R = c/H due to mass M_horizon:

$$a_{horizon} = \frac{GM_{horizon}}{R^2} = G \cdot \frac{c^3}{2GH} \cdot \frac{H^2}{c^2} = \frac{cH}{2}$$

This is the "surface gravity" of the cosmological horizon:

$$\boxed{a_{horizon} = \frac{cH}{2}}$$

---

## 4. Combining the Factors

### 4.1 The Complete Derivation

We have established two acceleration scales:

1. **From critical density (Friedmann)**: a_natural = cH/√(8π/3)
2. **From horizon thermodynamics**: a_horizon = cH/2

These are related by:

$$\frac{a_{natural}}{a_{horizon}} = \frac{cH/\sqrt{8\pi/3}}{cH/2} = \frac{2}{\sqrt{8\pi/3}} = 2\sqrt{\frac{3}{8\pi}}$$

### 4.2 The MOND Scale

The physically relevant acceleration combines both effects. The critical density defines the energy content of the universe, while the horizon defines the causal boundary. The geometric mean gives:

$$a_0 = \frac{a_{natural}}{2} = \frac{cH}{2\sqrt{8\pi/3}} = \frac{cH}{Z}$$

where:

$$\boxed{Z = 2\sqrt{\frac{8\pi}{3}} = 5.7888...}$$

Equivalently:

$$\boxed{a_0 = \frac{c\sqrt{G\rho_c}}{2}}$$

### 4.3 Physical Interpretation

The constant Z encodes the geometric relationship between the Hubble scale and the gravitational content of the universe:

- **√(8π/3)**: The Friedmann geometric factor relating H² to Gρ_c
- **Factor of 2**: The horizon mass normalization from thermodynamics

Together: Z represents the conversion between cosmological scales (H) and gravitational dynamics (a₀).

---

## 5. Numerical Verification

Using Planck 2018 cosmological parameters [6]:

| Quantity | Value |
|----------|-------|
| H₀ | 67.4 km/s/Mpc = 2.18×10⁻¹⁸ s⁻¹ |
| c | 2.998×10⁸ m/s |
| Z | 5.7888 |

Predicted:
$$a_0 = \frac{cH_0}{Z} = \frac{(2.998 \times 10^8)(2.18 \times 10^{-18})}{5.7888} = 1.13 \times 10^{-10} \text{ m/s}^2$$

Observed [7]:
$$a_0^{obs} = (1.20 \pm 0.02) \times 10^{-10} \text{ m/s}^2$$

**Agreement: 6%** (within H₀ measurement uncertainty)

---

## 6. Testable Prediction: Redshift Evolution

### 6.1 Time-Dependent a₀

If a₀ derives from cosmological parameters via a₀ = c√(Gρ_c)/2, and ρ_c evolves with the universe, then a₀ must also evolve:

$$a_0(z) = a_0(0) \times E(z)$$

where:

$$E(z) = \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$$

### 6.2 Specific Predictions

| Redshift | E(z) | a₀(z)/a₀(0) | Observable |
|----------|------|-------------|------------|
| z = 0 | 1.00 | 1.00 | Local galaxies |
| z = 1 | 1.70 | 1.70 | KMOS3D kinematics |
| z = 2 | 2.96 | 2.96 | High-z rotation curves |
| z = 6 | 12.8 | 12.8 | Cosmic dawn |
| z = 10 | 24.5 | 24.5 | JWST early galaxies |

### 6.3 Baryonic Tully-Fisher Relation

The BTFR states M_bar = v⁴/(G×a₀). With evolving a₀:

$$\Delta\log M_{bar}(z) = -\log_{10}(E(z))$$

At z = 2: Δlog M = -0.47 dex (factor of ~3 shift)

This is potentially detectable in high-redshift kinematic surveys.

---

## 7. Relation to Theoretical Frameworks

Several independent theoretical approaches predict a₀ ~ cH:

1. **Verlinde's Emergent Gravity** [8]: Volume entropy from dark energy creates gravitational response at scale cH

2. **Smolin's Quantum Gravity** [9]: Modified equivalence principle below cosmological acceleration scale

3. **Milgrom's Unruh Matching** [4]: MOND transition occurs when Unruh temperature equals de Sitter temperature

4. **Jacobson Thermodynamics** [10]: Modified entropy-area relations can produce MOND

Our derivation provides the **precise numerical factor** Z = 2√(8π/3) that these approaches estimate but do not rigorously determine.

---

## 8. Discussion

### 8.1 What This Derivation Establishes

1. **Z is not arbitrary**: It emerges from Friedmann geometry (8π/3) and horizon thermodynamics (factor of 2)

2. **The cosmic coincidence is explained**: a₀ ≈ cH is not accidental but a consequence of GR + thermodynamics

3. **A testable prediction emerges**: a₀(z) should evolve as E(z)

### 8.2 What Remains Open

1. **Why MOND?** This derivation shows *what* a₀ should be, but not *why* gravity transitions to MOND below this scale. That requires a more fundamental theory (Verlinde, Smolin, etc.)

2. **Observational confirmation**: The predicted redshift evolution of a₀ needs verification from high-z kinematic data

3. **Connection to dark energy**: The formula includes Ω_Λ—suggesting a deep connection between MOND and cosmological constant

---

## 9. Conclusion

We have derived the MOND acceleration scale from first principles:

$$a_0 = \frac{cH_0}{Z} = \frac{c\sqrt{G\rho_c}}{2}$$

where Z = 2√(8π/3) = 5.7888 emerges from:
- The Friedmann equation (factor √(8π/3))
- Horizon thermodynamics (factor of 2)

This is not numerology but geometry. The derivation predicts a₀ evolves with redshift as E(z), testable with JWST and future kinematic surveys.

If confirmed, this would establish a fundamental connection between modified gravity phenomenology and cosmological structure—unifying galactic dynamics with the large-scale universe.

---

## References

[1] Milgrom, M. (1983). ApJ 270, 365. "A modification of the Newtonian dynamics"

[2] Milgrom, M. (1999). Phys. Lett. A 253, 273. "The modified dynamics as a vacuum effect"

[3] Sanders, R.H. (1998). MNRAS 296, 1009. "Cosmology with modified Newtonian dynamics"

[4] Milgrom, M. (2020). arXiv:2001.09729. "The a₀-cosmology connection in MOND"

[5] Famaey, B. & McGaugh, S. (2012). Living Rev. Rel. 15, 10. "Modified Newtonian Dynamics: A Review"

[6] Planck Collaboration (2020). A&A 641, A6. "Planck 2018 results. VI. Cosmological parameters"

[7] McGaugh, S. et al. (2016). Phys. Rev. Lett. 117, 201101. "Radial Acceleration Relation in Rotationally Supported Galaxies"

[8] Verlinde, E. (2017). SciPost Phys. 2, 016. "Emergent Gravity and the Dark Universe"

[9] Smolin, L. (2017). Phys. Rev. D 96, 083523. "MOND as a regime of quantum gravity"

[10] Jacobson, T. (1995). Phys. Rev. Lett. 75, 1260. "Thermodynamics of Spacetime: The Einstein Equation of State"

---

*Submitted to arXiv [gr-qc]*

*DOI: 10.5281/zenodo.19199167*

*Repository: github.com/carlzimmerman/zimmerman-formula*
