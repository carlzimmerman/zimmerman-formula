# Gravitational Wave Implications of the Zimmerman Framework

**Carl Zimmerman | March 2026**

## Overview

The Zimmerman Framework modifies gravity at low accelerations (a < a₀). What are the implications for gravitational waves?

---

## Part 1: The MOND Regime and GWs

### Standard GR Waves

In General Relativity, gravitational waves propagate at speed c with:
```
h_μν = (2G/c⁴r) × (d²Q_ij/dt²)
```

Where Q_ij is the quadrupole moment of the source.

### MOND Modifications

In MOND-like theories, the gravitational potential is modified when a < a₀:
```
Standard: g = GM/r²
MOND: g = √(GM a₀)/r  (when g << a₀)
```

### Do GWs Feel MOND?

**Key question:** Do gravitational waves propagate differently in the MOND regime?

**Standard MOND answer:** GWs are relativistic (a >> a₀ locally), so they should propagate normally.

**Zimmerman modification:** Since a₀ evolves with H, there might be cosmological effects on GW propagation.

---

## Part 2: GW Propagation at Cosmological Scales

### The Evolving a₀

```
a₀(z) = a₀(0) × E(z)
```

At high redshift, a₀ was larger.

### GW from High-z Sources

For GWs emitted at redshift z_s:
```
h_observed = h_emitted × (1/(1+z_s)) × (propagation effects)
```

In standard GR, propagation is geometric (1+z dilution).

### Possible Zimmerman Effect

If a₀ affects GW generation:
```
h(z_s) ∝ (a₀(z_s)/a₀(0))^n × (standard expression)
        ∝ E(z_s)^n × (standard expression)
```

**What is n?** Depends on the theory. Possibilities:
- n = 0: No effect (GWs immune to MOND)
- n = 1/2: Weak effect (GW amplitude scales with √a₀)
- n = 1: Strong effect (GW amplitude scales with a₀)

---

## Part 3: Binary Neutron Star Mergers

### GW170817

The first observed NS-NS merger (2017):
- z = 0.01 (40 Mpc)
- GW + electromagnetic counterpart
- Confirmed v_GW = c to ~10⁻¹⁵

### Zimmerman Prediction for GW170817

At z = 0.01:
```
E(0.01) = √(0.315 × 1.01³ + 0.685) ≈ 1.005
```

The a₀ was only 0.5% higher than today — essentially no effect.

### High-z GW Sources

For sources at z = 1:
```
E(1) = √(0.315 × 8 + 0.685) = √3.2 = 1.79
```

**Potential effects:**
- GW amplitude modified by factor ~1.79^n
- Waveform shape potentially affected
- Inspiral rate might differ

---

## Part 4: Binary Black Hole Mergers

### Observed Events

LIGO/Virgo have observed ~100 BBH mergers at z = 0.1-1.

### MOND in Strong Gravity?

Near black holes, a >> a₀ (strong gravity). Standard MOND effects are suppressed.

However:
- The **inspiral phase** involves accelerations that decrease with separation
- At large separations (early inspiral), a might approach a₀
- **Zimmerman:** The relevant a₀ at the source redshift is different

### A Test

Compare inspiral rates at different redshifts:
- z = 0.1: a₀(z) ≈ 1.15 × a₀(0)
- z = 1: a₀(z) ≈ 1.79 × a₀(0)

If MOND affects early inspiral:
```
df/dt ∝ f^(11/3) × (standard) × (MOND correction)
```

The MOND correction would depend on a₀(z).

---

## Part 5: Gravitational Wave Speed

### GW170817 Constraint

The GW and gamma-ray burst arrived within 1.7 seconds over 40 Mpc:
```
|v_GW - c|/c < 10⁻¹⁵
```

### Does Zimmerman Predict v_GW ≠ c?

In most MOND formulations:
- GWs propagate at c (tensor modes unmodified)
- Only scalar/vector modes might differ

**Zimmerman specifically:**
```
a₀ = cH/Z
```

This doesn't modify the tensor propagation equation:
```
□h_μν = 0
```

**Prediction:** v_GW = c exactly, consistent with GW170817.

---

## Part 6: Stochastic GW Background

### The Background

The universe has a stochastic background of GWs from:
- Unresolved binaries
- Early universe (inflation, phase transitions)
- Cosmic strings (if they exist)

### Zimmerman Modification

If GW sources at high z had different a₀:
```
Ω_GW(f) = ∫ dz (dρ_GW/dz) × (propagation) × (a₀(z) effect?)
```

The spectrum might be modified at frequencies corresponding to high-z sources.

### LISA Sensitivity

LISA will probe mHz GWs from supermassive BH mergers at z = 1-10.

At z = 5:
```
E(5) = √(0.315 × 216 + 0.685) = √68.8 = 8.3
a₀(z=5) = 8.3 × a₀(0) ≈ 10⁻⁹ m/s²
```

**Question:** Does this affect SMBH binary dynamics?

---

## Part 7: Pulsar Timing Arrays

### How PTAs Work

Pulsars are precise clocks. GWs passing between us and pulsars cause timing residuals.

### Current Sensitivity

PTAs (NANOGrav, EPTA, PPTA) probe nHz GWs — the regime of SMBH binary inspirals at z = 0-2.

### Zimmerman Prediction

The SMBH binaries producing the stochastic background are at z ~ 0.5-2:
```
z = 1: a₀(z) = 1.79 × a₀(0)
z = 2: a₀(z) = 2.96 × a₀(0)
```

If a₀ affects binary dynamics, the predicted strain spectrum would differ from standard GR.

### A Specific Test

The characteristic strain spectrum in GR:
```
h_c(f) ∝ f^(-2/3)  (for circular binaries)
```

In Zimmerman (if a₀ affects dynamics):
```
h_c(f) ∝ f^(-2/3) × g(z(f))  where g depends on E(z)
```

The deviation from -2/3 slope would indicate evolving a₀.

---

## Part 8: Primordial GWs

### Inflationary GWs

Inflation produces a background of GWs with:
```
Ω_GW(f) ∝ (H_inflation/M_Planck)²
```

### Zimmerman Connection?

The tensor-to-scalar ratio r is related to inflation scale.

If Z affects inflation (speculative):
```
r ∝ 1/Z² or some function of Z
```

**Current bound:** r < 0.06 (Planck/BICEP)

### A Wild Speculation

If inflation occurred at a scale where Z enters:
```
H_inflation ∝ Z × (some mass scale)
```

Then r would depend on Z, connecting GW observations to the Zimmerman constant.

**Status:** Highly speculative; no concrete prediction yet.

---

## Part 9: Modified GW Generation

### Quadrupole Formula

In GR:
```
P_GW = (G/5c⁵) × (d³Q_ij/dt³)²
```

### MOND Modification?

In MOND, the effective G might be:
```
G_eff = G × μ(a/a₀)
```

where μ is the MOND interpolation function.

For GW generation from binaries:
```
P_GW(MOND) = P_GW(GR) × f(a/a₀(z))
```

### Observable Effect

For a binary at z = 1 with a₀(z) = 1.79 × a₀(0):

If a binary component has acceleration a ~ a₀:
```
MOND factor = μ(a/(1.79 × a₀(0))) ≠ μ(a/a₀(0))
```

The GW power would differ from GR prediction.

### Where This Matters

Wide binaries (separation ~ 10⁴ AU) have a ~ a₀.

GW emission from such binaries is negligible, BUT:
- Galactic dynamics affect binary populations
- MOND changes binary hardening rates
- This affects merger rates

**Zimmerman prediction:** Merger rate evolution with z differs from GR.

---

## Part 10: Summary and Predictions

### Key Points

1. **GW speed = c:** Zimmerman predicts v_GW = c, consistent with GW170817

2. **High-z source differences:** GWs from z > 1 might show effects from larger a₀(z)

3. **PTA spectrum:** The stochastic background slope might deviate from -2/3

4. **LISA SMBHs:** z ~ 5 sources have a₀ ~ 8× local value

5. **Merger rates:** Population evolution differs due to MOND dynamics

### Concrete Tests

| Observation | Standard GR | Zimmerman |
|-------------|-------------|-----------|
| GW speed | c | c |
| PTA spectrum | f^(-2/3) | Modified at low f |
| LISA waveforms | Standard | Possible z-dependence |
| BBH mass function | Fixed | z-dependent |

### What Would Confirm/Refute

**Confirm:**
- PTA spectrum deviation correlating with E(z)
- High-z GW sources showing systematic residuals
- Merger rate evolution matching a₀(z) dynamics

**Refute:**
- No deviation at any redshift
- GW propagation speed ≠ c
- Waveforms inconsistent with MOND dynamics

---

*Carl Zimmerman, March 2026*
