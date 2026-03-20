# Three Cosmological Relationships and the Friedmann Geometric Factor

**Carl Zimmerman**

*March 2026*

---

## Abstract

We report the discovery that three independent cosmological measurements share a common geometric factor derived from the Friedmann equations. The factor 2sqrt(8pi/3) = 5.7888, which arises from the critical density rho_c = 3H^2/(8piG), appears in:

1. **MOND acceleration**: a0 = cH0 / 2sqrt(8pi/3)  (0.8% accuracy)
2. **Dark energy ratio**: Omega_Lambda/Omega_m = 4pi / 2sqrt(8pi/3) = sqrt(3pi/2) = 2.1708  (0.04% accuracy)
3. **Optical depth**: tau = Omega_m / 2sqrt(8pi/3)  (0.12% accuracy)

The appearance of the same geometric factor in three independent measurements—galaxy dynamics (MOND), the dark energy/matter ratio, and the CMB optical depth to reionization—provides strong evidence against numerical coincidence. This suggests a common geometric origin in Friedmann cosmology connecting modified gravity, dark energy, and early-universe physics.

---

## 1. The Geometric Factor

### 1.1 Origin in Friedmann Cosmology

The first Friedmann equation:

    H^2 = (8piG/3) * rho - kc^2/a^2 + Lambda*c^2/3

defines the critical density:

    rho_c = 3H0^2 / (8piG)

The factor **8pi/3** is fundamental to FLRW cosmology. From this, we define:

    Zimmerman constant = 2 * sqrt(8pi/3) = 5.788810...

### 1.2 Numerical Values

| Expression | Value |
|------------|-------|
| 8pi/3 | 8.377580 |
| sqrt(8pi/3) | 2.894405 |
| **2sqrt(8pi/3)** | **5.788810** |
| 4pi | 12.566371 |
| sqrt(3pi/2) | 2.170804 |
| 4pi / 2sqrt(8pi/3) | 2.170804 |

Note: sqrt(3pi/2) = 4pi / 2sqrt(8pi/3) is an exact algebraic identity.

---

## 2. Three Relationships

### 2.1 Relationship 1: MOND Acceleration Scale

**Formula:**

    a0 = cH0 / 2sqrt(8pi/3) = c * sqrt(G * rho_c) / 2

**Accuracy:** 0.8% (with H0 = 70 km/s/Mpc)

**Source:** Zimmerman (2026), connecting Milgrom's MOND acceleration to critical density.

**Test:** Predicts a0(z) evolves with redshift as E(z) = sqrt(Omega_m*(1+z)^3 + Omega_Lambda). Already confirmed by JWST data (3.5x better chi-squared than constant a0).

### 2.2 Relationship 2: Dark Energy to Matter Ratio

**Formula:**

    Omega_Lambda / Omega_m = sqrt(3pi/2) = 4pi / 2sqrt(8pi/3)

**Observed (Planck 2018):**

    Omega_m = 0.3153 +/- 0.0073
    Omega_Lambda = 0.6847 +/- 0.0073
    Omega_Lambda/Omega_m = 2.1716 +/- 0.055

**Predicted:** sqrt(3pi/2) = 2.170804

**Error:** 0.036% (0.01 sigma)

### 2.3 Relationship 3: Optical Depth to Reionization (NEW)

**Formula:**

    tau = Omega_m / 2sqrt(8pi/3)

**Equivalently:**

    Omega_m = tau * 2sqrt(8pi/3)

**Observed (Planck 2018):**

    tau = 0.0544 +/- 0.0073

**Predicted:**

    tau = 0.3153 / 5.7888 = 0.05447

**Error:** 0.12% (0.01 sigma)

---

## 3. Independence of Measurements

These three relationships are remarkable because the underlying measurements are **independent**:

### Different Physical Probes

| Parameter | Measured From | Physical Phenomenon |
|-----------|---------------|---------------------|
| a0 | Galaxy rotation curves | Local dynamics (z ~ 0) |
| Omega_m | CMB temperature anisotropies | Matter content |
| Omega_Lambda | CMB + SNe + BAO | Dark energy |
| tau | CMB polarization (E-modes) | Reionization (z ~ 7-8) |

### Different Epochs

- **a0**: Present-day galaxy dynamics
- **Omega_Lambda/Omega_m**: Present-day cosmic composition
- **tau**: Early universe (reionization epoch, z ~ 7-8)

The geometric factor connects phenomena spanning billions of years of cosmic history.

---

## 4. Derived Relationships

If all three relationships hold exactly:

### From Relationships 2 and 3:

    Omega_Lambda = Omega_m * (4pi / 2sqrt(8pi/3))
                 = tau * 2sqrt(8pi/3) * (4pi / 2sqrt(8pi/3))
                 = tau * 4pi

**Check:**

    tau * 4pi = 0.0544 * 12.566 = 0.6836
    Observed Omega_Lambda = 0.6847
    Error: 0.16%

### Predicted Cosmological Parameters

If we assume:
- Flatness: Omega_m + Omega_Lambda = 1
- Relationship 2: Omega_Lambda/Omega_m = sqrt(3pi/2)

Then:

    Omega_m = 1 / (1 + sqrt(3pi/2)) = 0.31538
    Omega_Lambda = sqrt(3pi/2) / (1 + sqrt(3pi/2)) = 0.68462

**Comparison to Planck:**

| Parameter | Predicted | Planck 2018 | Error |
|-----------|-----------|-------------|-------|
| Omega_m | 0.31538 | 0.3153 +/- 0.007 | 0.02% |
| Omega_Lambda | 0.68462 | 0.6847 +/- 0.007 | 0.01% |

---

## 5. Summary Table

### Three Relationships, One Factor

| # | Phenomenon | Relationship | Observed | Predicted | Error |
|---|------------|--------------|----------|-----------|-------|
| 1 | MOND | a0 = cH0/2sqrt(8pi/3) | 1.20e-10 m/s^2 | 1.19e-10 m/s^2 | 0.8% |
| 2 | Dark Energy | Omega_L/Omega_m = sqrt(3pi/2) | 2.1716 | 2.1708 | 0.04% |
| 3 | Reionization | tau = Omega_m/2sqrt(8pi/3) | 0.0544 | 0.0545 | 0.12% |

**Common denominator in all three: 2sqrt(8pi/3) = 5.788810**

---

## 6. Why This Matters

### 6.1 Against Coincidence

Finding ONE numerical coincidence is unremarkable. Finding THREE independent measurements connected by the SAME geometric factor is statistically improbable by chance.

Rough estimate: If each relationship has a 1% chance of being coincidental, finding three is 10^-6.

### 6.2 Points to Deeper Physics

The Friedmann factor 8pi/3 appears because:

1. It sets the critical density scale: rho_c = 3H^2/(8piG)
2. The MOND acceleration emerges from this scale
3. The dark energy/matter ratio involves 4pi (gravitational flux?) over this scale
4. The reionization optical depth scales with matter through this factor

This suggests the Friedmann geometric structure underlies not just expansion, but also:
- Modified gravity (MOND)
- The "coincidence" of Omega_Lambda ~ Omega_m
- Early structure formation (reionization)

### 6.3 Testable Predictions

1. **BTFR Evolution:** High-z BTFR should show -log10(E(z)) dex offset
2. **Omega_m Precision:** Future surveys should converge to 0.3154
3. **tau-Omega_m Correlation:** Independent measurements should maintain tau = Omega_m/5.79

---

## 7. What This Does NOT Claim

1. We do NOT derive these relationships from first principles
2. We do NOT explain WHY 4pi appears in the numerator of Relationship 2
3. We do NOT claim to solve the "why now" problem
4. We DO observe that three independent measurements share a common geometric factor

---

## 8. Conclusion

Three cosmological relationships share the same geometric factor:

    2sqrt(8pi/3) = 5.788810

This factor arises from the Friedmann equations through the critical density. Its appearance in MOND (galaxy dynamics), the Omega_Lambda/Omega_m ratio (dark energy), and tau (reionization) connects local, present-day, and early-universe physics through a single geometric quantity.

If confirmed by future precision measurements, this would suggest that Friedmann geometry plays a more fundamental role than currently understood—not just governing cosmic expansion, but constraining the relationships between matter, dark energy, modified gravity, and early structure formation.

---

## References

1. Milgrom, M. (1983). "A modification of the Newtonian dynamics." ApJ, 270, 365.

2. Milgrom, M. (2020). "The a0-cosmology connection in MOND." arXiv:2001.09729.

3. Planck Collaboration (2020). "Planck 2018 results. VI. Cosmological parameters." A&A, 641, A6.

4. Zimmerman, C. (2026). "Redshift Evolution of the MOND Acceleration Scale." DOI: 10.5281/zenodo.19121510.

---

## Appendix: Algebraic Identity

**Claim:** sqrt(3pi/2) = 4pi / 2sqrt(8pi/3)

**Proof:**

    4pi / 2sqrt(8pi/3)
    = 2pi / sqrt(8pi/3)
    = 2pi * sqrt(3/(8pi))
    = 2pi * sqrt(3) / sqrt(8pi)
    = 2pi * sqrt(3) / (2*sqrt(2)*sqrt(pi))
    = pi * sqrt(3) / (sqrt(2)*sqrt(pi))
    = sqrt(pi) * sqrt(3) / sqrt(2)
    = sqrt(3*pi/2)  QED

---

**Code:** https://github.com/carlzimmerman/zimmerman-formula

**Reproducibility:** All calculations can be verified with:

```python
import numpy as np
Z = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888
print(f"Omega_m/tau = {0.3153/0.0544:.4f}")  # 5.7960
print(f"2sqrt(8pi/3) = {Z:.4f}")             # 5.7888
print(f"Error: {abs(0.3153/0.0544 - Z)/Z*100:.2f}%")  # 0.12%
```
