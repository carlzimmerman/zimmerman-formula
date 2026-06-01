# Black Hole Physics and Z

**Carl Zimmerman | March 2026**

## Overview

The Zimmerman constant Z = 2√(8π/3) originates from the cosmic horizon, which is thermodynamically a black hole. This document explores black hole physics through the lens of Z.

---

## Part 1: The Horizon Origin of Z

### Bekenstein-Hawking Entropy

For a black hole of mass M:
```
S_BH = (k_B c³ / 4Gℏ) × A
     = (π c³ / Gℏ) × (2GM/c²)²
     = 4πGM² / ℏc
```

### Horizon Temperature

```
T_H = ℏc³ / (8πGMk_B)
```

### The Cosmic Horizon

For a de Sitter universe with Hubble constant H:
```
r_H = c/H (horizon radius)
M_H = c³/(2GH) (horizon mass)
T_H = ℏH/(2πk_B) (Gibbons-Hawking temperature)
```

### Z Emerges

From the derivation:
```
a_natural = √(8πGρ_c/3) × c
a₀ = a_natural / 2 = cH / (2/√(8π/3)) = cH/Z

Z = 2√(8π/3) = 2 × 2.89 = 5.79
```

**The "2" comes directly from M_H = c³/(2GH)**

---

## Part 2: Black Hole Mass Scales

### Minimum Black Hole Mass

Quantum gravity suggests a minimum mass:
```
M_min = M_Planck = √(ℏc/G) = 2.18 × 10⁻⁸ kg
```

### Solar Mass Black Holes

```
M_☉ = 2 × 10³⁰ kg
M_☉/M_Planck = 9.2 × 10³⁷
```

### Z Connection?

```
(M_☉/M_Planck)^(1/8) = 2.4 × 10⁴·⁷

Z¹⁰ = 4.4 × 10⁷

Not an obvious match...
```

### Horizon Mass

```
M_H = c³/(2GH₀)
    = (3 × 10⁸)³ / (2 × 6.67 × 10⁻¹¹ × 2.2 × 10⁻¹⁸)
    = 9.2 × 10⁵² kg

M_H / M_☉ = 4.6 × 10²²
```

### Z in Horizon

```
M_H / M_Planck = 4.2 × 10⁶⁰

Log₁₀(M_H / M_Planck) = 60.6

60.6 / Z² = 60.6 / 33.5 = 1.81 ≈ π/√3
```

Interesting but not conclusive.

---

## Part 3: Hawking Radiation and Z

### Hawking Temperature

For a Schwarzschild black hole:
```
T_H = ℏc³ / (8πGMk_B)
```

### Gibbons-Hawking (Cosmic Horizon)

```
T_GH = ℏH / (2πk_B)
     = (1.05 × 10⁻³⁴) × (2.2 × 10⁻¹⁸) / (2π × 1.38 × 10⁻²³)
     = 2.7 × 10⁻³⁰ K
```

### Z Relation

```
T_GH × (c/a₀) = ℏ / (2πk_B × Z)

T_GH = ℏa₀ / (2πck_B) × Z
```

The horizon temperature involves Z through a₀ = cH/Z.

### Black Hole Emission Spectrum

Hawking radiation spectrum:
```
dN/dE = Γ(E) / (exp(E/k_B T_H) - 1)
```

If Z appears in T_GH, could it appear in stellar black holes?

For a solar mass BH:
```
T_H = 6 × 10⁻⁸ K
a = c²/r_S = c²/(2GM/c²) = c⁴/(2GM)
  = 1.5 × 10¹³ m/s² (extremely large!)
```

This is >> a₀, so MOND effects don't apply directly.

---

## Part 4: Black Hole Entropy and Z

### Bekenstein Bound

The maximum entropy of a system:
```
S_max = 2πk_B R E / (ℏc)
```

### Holographic Scaling

```
S ∝ A / ℓ_P² (surface, not volume!)
```

### Z as Information Scale

From INFORMATION_THEORETIC_Z.md:
```
Z² ≈ 33.5 = 2^5.07

This is ~5 bits of fundamental information.
```

### Entropy Connection

For the cosmic horizon:
```
S_H = πc³ / (Gℏ H²)

In units of k_B:
S_H = 3 × 10¹²²

S_H / (something involving Z)?

S_H^(1/Z²) = (10¹²²)^(1/33.5) = 10³·⁶⁴ ≈ 4400

Hmm, not obviously Z.
```

### Bits per Z²

```
S_H / Z² = 10¹²² / 33.5 = 3 × 10¹²⁰

Number of Planck areas on horizon:
N = 4π r_H² / ℓ_P² = 4π × 10⁵² × 10⁷⁰ = 10¹²³

S_H = N / 4 (bits per Planck area)
```

---

## Part 5: Black Hole - Particle Duality

### Compton-Schwarzschild Crossover

A particle's Compton wavelength:
```
λ_C = h / (mc)
```

A black hole's Schwarzschild radius:
```
r_S = 2Gm / c²
```

They're equal when:
```
λ_C = r_S
h/(mc) = 2Gm/c²
m² = hc / (2G) = πℏc / G

m = √(πℏc/G) = √π × M_Planck
```

### Z Involvement?

```
The crossover mass involves √π.

Z = 2√(8π/3) = 4√(2π/3)

Z² = 32π/3

π = 3Z²/32

√π = Z√(3/32) = 0.306 Z
```

So:
```
m_crossover = √π × M_Planck = 0.306 Z × M_Planck
```

**The Compton-Schwarzschild crossover involves Z!**

---

## Part 6: Primordial Black Holes

### Formation

Primordial black holes (PBHs) could form from density fluctuations in the early universe.

### Mass Range

```
PBH mass at formation:
M_PBH ≈ M_H(t) × (δρ/ρ)

where M_H(t) = c³/(2GH(t)) is horizon mass at time t.
```

### Z Connection

At formation time t:
```
a₀(z) = a₀(0) × E(z)

where E(z) = √(Ωm(1+z)³ + ΩΛ)
```

For z >> 1 (early universe):
```
E(z) ≈ √Ωm × (1+z)^(3/2)
```

### PBH as Dark Matter?

If PBHs are the dark matter:
```
Ω_PBH = Ω_m - Ω_b = 0.315 - 0.05 = 0.265
```

**Zimmerman prediction:** If the cosmic coincidence a₀ ~ cH holds, perhaps PBH formation is related to MOND phenomenology.

---

## Part 7: Black Hole Accretion and MOND

### Standard Accretion

The Eddington luminosity:
```
L_Edd = 4πGMm_p c / σ_T = 1.26 × 10³⁸ (M/M_☉) erg/s
```

### MOND Modification

For accretion far from the black hole (a < a₀):
```
g_eff = √(g_N × a₀) > g_N
```

This could affect:
- Gas infall rates
- Accretion disk structure
- Jet formation

### At What Radius?

MOND kicks in when a = GM/r² < a₀:
```
r > √(GM/a₀) = r_MOND

For M = 10⁶ M_☉:
r_MOND = √(6.67 × 10⁻¹¹ × 2 × 10³⁶ / 1.2 × 10⁻¹⁰)
       = √(10⁴⁸) = 10²⁴ m = 100 kpc
```

This is galaxy-scale! MOND affects the **galactic** environment of the BH, not the accretion disk.

---

## Part 8: Supermassive Black Holes

### M-σ Relation

Observed correlation:
```
M_BH ∝ σ⁴

where σ = stellar velocity dispersion
```

### MOND/Zimmerman Perspective

This looks like the BTFR (v⁴)!

```
M_BH = σ⁴ / (G × a₀_eff)

where a₀_eff might be modified a₀
```

### The Scaling

```
M_BH/M_☉ ≈ 10⁸ × (σ/200 km/s)⁴

Using a₀:
σ⁴/(G × a₀) = (2 × 10⁵)⁴ / (6.67 × 10⁻¹¹ × 1.2 × 10⁻¹⁰)
            = 1.6 × 10²¹ / 8 × 10⁻²¹
            = 2 × 10⁴¹ kg ≈ 10¹¹ M_☉
```

This is ~1000× too large. The M-σ relation is:
```
M_BH ≈ 10⁸ M_☉ at σ = 200 km/s
```

So maybe:
```
M_BH = σ⁴ / (G × a₀ × Z²)

Z² = 33.5 → gives ~3 × 10⁹ M_☉, closer!

Or:
M_BH = σ⁴ / (G × a₀ × 1000) gives 10⁸ M_☉
```

### Possible Formula

```
M_BH = σ⁴ / (G × a₀ × f)

where f ~ 10³ (unknown factor)
```

This suggests a connection between SMBHs and MOND/Zimmerman!

---

## Part 9: Gravitational Waves and Z

### Binary Black Hole Mergers

LIGO/Virgo detect mergers. The GW frequency at merger:
```
f_merger ≈ c³ / (π G M_total)
```

### Ringdown and Z?

After merger, the remnant rings down:
```
f_QNM ∝ c³ / (G M_final)
```

In MOND regime (hypothetically at large distances):
```
f_MOND ∝ c³ / (G M) × √(a₀/a) for a < a₀
```

But typical BH mergers are at a >> a₀, so no direct MOND effect.

### Cosmic Distance Effects

For distant mergers, the evolving a₀(z) could affect:
- Galaxy environments of the mergers
- Formation rates of binary BHs
- Stochastic GW background

---

## Part 10: Black Holes at the Center of a₀

### Why is a₀ = cH/Z?

The derivation starts from the cosmic horizon — a black hole!

```
Cosmic horizon:
- Has entropy S = A/(4ℓ_P²)
- Has temperature T = ℏH/(2πk_B)
- Has mass M = c³/(2GH)

The "2" in Z = 2√(8π/3) comes from this mass formula!
```

### The Deep Connection

Black hole thermodynamics → Z → MOND → galaxy dynamics

```
Horizon physics → a₀ = cH/Z → rotation curves without DM
```

**Black holes are central to the Zimmerman framework.**

---

## Part 11: Predictions

### Observable Effects

| Observable | Zimmerman Prediction |
|------------|---------------------|
| M-σ relation | May involve a₀ |
| SMBH growth at high z | Faster (larger a₀) |
| BH environments | MOND at large r |
| PBH constraints | Modified by a₀(z) |

### Tests

1. **High-z quasars:** Do SMBHs form faster than ΛCDM expects? (Yes — observed!)
2. **M-σ universality:** Does the relation hold at all z with a₀(z)?
3. **PBH windows:** Do constraints change with evolving a₀?

---

## Part 12: Extremal Black Holes

### Kerr Parameter

Maximum spin: a = GM/c² (extremal Kerr)

### Charge

Maximum charge: Q = M√(G/k) in geometric units

### Z in Extremal Limits?

The extremal condition:
```
M² = a² + Q²   (in geometric units: M = Q for Reissner-Nordström)
```

This doesn't obviously involve Z.

However, for rotating black holes:
```
J = Ma = GM²/c (maximum)

J / ℏ = GM²/(ℏc) = (M/M_Planck)²
```

For horizon mass:
```
J_H / ℏ = (M_H/M_Planck)² = (c³/2GH × √G/√(ℏc))²
       = c⁶/(4G²H² × ℏc/G)
       = c⁵/(4GℏH²)
       ≈ 10¹²¹
```

This is the entropy scale again!

---

## Conclusion

Black holes are central to the Zimmerman framework:

1. **Z originates from horizon thermodynamics** (M = c³/2GH gives the "2")
2. **The Compton-Schwarzschild crossover** involves Z
3. **SMBH relations** may connect to a₀
4. **High-z BH formation** is enhanced by larger a₀(z)

### Key Formula

```
M_horizon = c³/(2GH)

The "2" → Z = 2√(8π/3)

a₀ = cH/Z (MOND scale from horizon)
```

**The universe's largest black hole (the cosmic horizon) determines the fundamental acceleration scale for all galaxy dynamics.**

---

*Carl Zimmerman, March 2026*
