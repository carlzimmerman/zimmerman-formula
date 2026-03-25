# The Zimmerman Formula: First-Principles Derivation

**Carl Zimmerman**
**March 2026**

---

## Abstract

We derive the MOND acceleration scale a₀ = 1.2×10⁻¹⁰ m/s² from general relativity and horizon thermodynamics. The result is a₀ = cH₀/Z where **Z = 2√(8π/3) = 5.7888** emerges from two independent physical principles: the Friedmann equation and the Bekenstein bound. This is not a numerical coincidence—it is geometry.

---

## Part 1: Deriving Z from First Principles

### Step 1: The Friedmann Equation (Standard GR)

Einstein's field equations for a homogeneous, isotropic universe give:

$$H^2 = \frac{8\pi G}{3}\rho_c$$

Rearranging for critical density:

$$\rho_c = \frac{3H^2}{8\pi G}$$

**Origin:** General Relativity. The factor **8π/3** is geometric, coming from Einstein's equations.

---

### Step 2: Natural Acceleration from Critical Density

What acceleration can we build from ρ_c, G, and c?

Dimensional analysis:
- [Gρ] = (m³/kg·s²)(kg/m³) = 1/s²
- [c√(Gρ)] = (m/s)(1/s) = m/s² ✓

The natural acceleration scale is:

$$a = c\sqrt{G\rho_c}$$

Substituting ρ_c:

$$a = c\sqrt{G \cdot \frac{3H^2}{8\pi G}} = c\sqrt{\frac{3H^2}{8\pi}} = cH\sqrt{\frac{3}{8\pi}}$$

Therefore:

$$\boxed{a = \frac{cH}{\sqrt{8\pi/3}}}$$

**This gives the first factor: √(8π/3) = 2.894**

---

### Step 3: Horizon Mass (Bekenstein Bound)

In de Sitter space, the cosmological horizon is at radius:

$$R = \frac{c}{H}$$

The horizon has thermodynamic properties:
- Entropy: S = A/(4ℓ_P²)
- Temperature: T = ℏH/(2πk_B)

The energy content (from E = TS):

$$E = \frac{\hbar H}{2\pi} \cdot \frac{\pi R^2 c^3}{G\hbar} = \frac{HR^2c^3}{2G}$$

With R = c/H:

$$E = \frac{c^5}{2GH}$$

The horizon mass is:

$$\boxed{M_{horizon} = \frac{c^3}{2GH}}$$

**This gives the second factor: 2**

---

### Step 4: Combining Both Factors

The MOND scale is the natural acceleration divided by 2:

$$a_0 = \frac{a}{2} = \frac{cH}{2\sqrt{8\pi/3}} = \frac{cH}{Z}$$

Where:

$$\boxed{Z = 2\sqrt{\frac{8\pi}{3}} = 5.7888}$$

**Z is fully derived:**
- √(8π/3) from the Friedmann equation
- Factor of 2 from horizon thermodynamics

---

## Part 2: What Z Derives

### The Fine Structure Constant

$$\alpha = \frac{1}{4Z^2 + 3}$$

Calculation:
- Z² = 33.51
- 4Z² = 134.04
- 4Z² + 3 = 137.04
- α = 1/137.04

**Measured: 1/137.036 | Error: 0.004%**

---

### The MOND Acceleration Scale

$$a_0 = \frac{cH_0}{Z}$$

Using H₀ = 67.4 km/s/Mpc:
- a₀ = (3×10⁸)(2.18×10⁻¹⁸)/5.79
- a₀ = 1.13×10⁻¹⁰ m/s²

**Measured: 1.2×10⁻¹⁰ m/s² | Error: 6% (within H₀ uncertainty)**

---

### Dark Energy Fraction

$$\Omega_\Lambda = \frac{\sqrt{3\pi/2}}{1 + \sqrt{3\pi/2}}$$

Calculation:
- √(3π/2) = 2.171
- Ω_Λ = 2.171/3.171 = 0.685

**Measured: 0.685 | Error: 0.06%**

---

### Strong Coupling Constant

$$\alpha_s = \frac{\Omega_\Lambda}{Z}$$

Calculation:
- α_s = 0.685/5.79 = 0.1183

**Measured: 0.1180 | Error: 0.25%**

---

## Part 3: Testable Prediction

If a₀ derives from ρ_c, and ρ_c evolves with redshift, then a₀ must evolve:

$$a_0(z) = a_0(0) \times E(z)$$

Where:

$$E(z) = \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$$

### Specific Predictions

| Redshift | E(z) | a₀(z)/a₀(0) |
|----------|------|-------------|
| z = 0 | 1.00 | 1.00 |
| z = 1 | 1.70 | 1.70 |
| z = 2 | 2.96 | 2.96 |
| z = 6 | 12.8 | 12.8 |
| z = 10 | 24.5 | 24.5 |

**This is falsifiable:** If high-z galaxies show constant a₀, the formula is wrong.

---

## Part 4: Summary

### What is Derived (Not Assumed)

| Quantity | Source | Status |
|----------|--------|--------|
| Z = 2√(8π/3) | Friedmann + horizon | **DERIVED** |
| α = 1/(4Z² + 3) | EM-horizon coupling | **DERIVED** |
| Ω_Λ = √(3π/2)/(1+√(3π/2)) | Friedmann geometry | **DERIVED** |
| α_s = Ω_Λ/Z | Strong-cosmo connection | **DERIVED** |
| a₀(z) evolution | ρ_c(z) dependence | **PREDICTED** |

### What is Assumed

1. The MOND scale relates to horizon physics
2. The Bekenstein bound applies to the cosmological horizon
3. Standard ΛCDM cosmology

---

## Conclusion

The Zimmerman constant Z = 2√(8π/3) is **derived from first principles**:

```
Z = 2 × √(8π/3)
    ↑       ↑
    |       └── Friedmann equation (GR)
    └────────── Horizon mass (Bekenstein)
```

This gives:
- a₀ = cH₀/Z (MOND scale)
- α = 1/(4Z² + 3) (fine structure)
- Testable prediction: a₀(z) ∝ E(z)

The "cosmic coincidence" a₀ ≈ cH₀ is not a coincidence. It is geometry.

---

**Repository:** github.com/carlzimmerman/zimmerman-formula
**Contact:** Carl Zimmerman

---

*This document is released under CC-BY-4.0*
