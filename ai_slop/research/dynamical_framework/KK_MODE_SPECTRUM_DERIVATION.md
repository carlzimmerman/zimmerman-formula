# First-Principles Derivation: Kaluza-Klein Mode Spectrum and Fifth Force Bounds

**Extra Dimensional Physics from T³/Z₂**

**Carl Zimmerman | May 2026**

---

## Executive Summary

The Z² framework compactifies 7D → 4D on T³/Z₂. This document derives:
1. The complete KK mode spectrum
2. Fifth force bounds and experimental constraints
3. Connection to X17 boson anomaly
4. 'Oumuamua anomalous acceleration interpretation

**Key results:**
- KK graviton mass: m_n ~ n × M_Pl / Z ~ 10^17 GeV
- Fifth force range: λ ~ Z × ℓ_Pl ~ 10^-32 m
- No observable fifth force at accessible scales
- X17 NOT naturally explained by KK modes

---

## 1. Kaluza-Klein Theory on T³/Z₂

### 1.1 The Setup

Spacetime: M₇ = M₄ × T³/Z₂

Coordinates:
- x^μ (μ = 0,1,2,3) — 4D Minkowski
- y^i (i = 1,2,3) — internal T³/Z₂

The orbifold T³/Z₂ is T³ with identification:
```
y^i ~ -y^i    (Z₂ action)
y^i ~ y^i + L  (torus periodicity)
```

### 1.2 Fundamental Length Scale

The compactification radius:
```
R = L / (2π)
```

In Z² framework, the natural choice:
```
R ~ Z × ℓ_Pl = √(32π/3) × 1.6×10⁻³⁵ m
R ≈ 9.3 × 10⁻³⁵ m
```

This is **extremely small** — Planck scale.

---

## 2. KK Mode Expansion

### 2.1 Mode Functions

On T³/Z₂, only Z₂-even modes survive:
```
f_n(y) = cos(n·y/R)    for n = (n₁, n₂, n₃) with n_i ≥ 0
```

The zero mode (n = 0): constant function → 4D massless fields
Higher modes (n ≠ 0): massive KK excitations

### 2.2 Mass Formula

The KK mass spectrum:
```
m_n² = |n|² / R²
     = (n₁² + n₂² + n₃²) / R²
```

For the lightest KK mode (n = (1,0,0)):
```
m_KK = 1/R = 1 / (Z × ℓ_Pl) = M_Pl / Z
     ≈ 2.1 × 10¹⁸ GeV
```

**This is near the GUT scale — inaccessible to current experiments.**

### 2.3 Mode Counting

Number of modes at level N = n₁² + n₂² + n₃²:
```
g(N) = # ways to write N = n₁² + n₂² + n₃² with n_i ≥ 0
```

Including Z₂ projection: only (n₁, n₂, n₃) with all ≥ 0.

First few levels:
```
N = 0: g(0) = 1 (zero mode)
N = 1: g(1) = 3 (1,0,0), (0,1,0), (0,0,1)
N = 2: g(2) = 3 (1,1,0), (1,0,1), (0,1,1)
N = 3: g(3) = 4 (1,1,1), (√3,0,0)... [only (1,1,1) works]
```

---

## 3. KK Gravitons

### 3.1 Graviton Mode Expansion

The 7D graviton h_MN expands as:
```
h_μν(x, y) = h_μν^(0)(x) + Σ_{n≠0} h_μν^(n)(x) cos(n·y/R)
```

The 4D spectrum:
- h_μν^(0): massless graviton (standard gravity)
- h_μν^(n): massive spin-2 fields (KK gravitons)

### 3.2 KK Graviton Mass

```
m_n^(grav) = |n| / R = |n| × M_Pl / Z

For |n| = 1: m₁ = 2.1 × 10¹⁸ GeV
For |n| = 2: m₂ = 4.2 × 10¹⁸ GeV
...
```

### 3.3 KK Graviton Coupling

The coupling to matter:
```
L_int = (1/M_Pl) h_μν^(n) T^μν × (suppression factor)
```

The suppression from wavefunction overlap:
```
g_n ~ 1/M_Pl × (R / ℓ_Pl) = 1/M_Pl × Z
```

---

## 4. Fifth Force from KK Exchange

### 4.1 Yukawa Potential

Exchange of a massive KK graviton gives Yukawa modification to gravity:
```
V(r) = -G m₁ m₂ / r × [1 + α × exp(-r/λ)]
```

where:
- α = coupling strength relative to gravity
- λ = m_KK⁻¹ = range of fifth force

### 4.2 Z² Fifth Force Parameters

From T³/Z₂ compactification:
```
α ~ (M_Pl / m_KK)² × (number of KK modes) ~ Z² × g(N)
λ ~ 1/m_KK ~ Z × ℓ_Pl ~ 10⁻³⁴ m
```

**The range is 10²⁰× smaller than the proton — utterly unobservable.**

### 4.3 Experimental Constraints

Current limits on fifth forces:

| Range λ | α limit | Source |
|---------|---------|--------|
| > 1 mm | < 10⁻² | Eöt-Wash torsion |
| > 1 μm | < 10⁵ | Casimir experiments |
| > 1 nm | < 10¹² | Neutron scattering |

Z² prediction:
```
λ = 10⁻³⁴ m → α can be O(1) and still unobservable
```

**Z² is consistent with all fifth force bounds.**

---

## 5. Gauge KK Modes

### 5.1 Gauge Field Expansion

The 7D gauge field A_M:
```
A_μ(x, y) = A_μ^(0)(x) + Σ_n A_μ^(n)(x) cos(n·y/R)
A_i(x, y) = Σ_n φ_i^(n)(x) sin(n·y/R)
```

Note: A_μ has cosine modes (even under Z₂)
      A_i has sine modes — PROJECTED OUT by Z₂!

### 5.2 4D Spectrum

From KK reduction:
- A_μ^(0): massless gauge bosons (photon, W, Z, gluons)
- A_μ^(n): massive vector bosons (KK gauge)
- φ_i^(n): would be scalars — projected out

### 5.3 KK Photon Mass

```
m_n^(γ) = |n| / R = |n| × M_Pl / Z ~ 10¹⁸ GeV
```

**Far above LHC energy — no KK photon production.**

---

## 6. The X17 Boson Question

### 6.1 The Anomaly

The ATOMKI experiment claims:
```
m_X17 = 17.01 ± 0.16 MeV
```

A new boson in ⁸Be and ⁴He nuclear transitions.

### 6.2 Can Z² Explain X17?

**NO, not naturally.**

For a KK mode to have m = 17 MeV:
```
m = |n| / R = 17 MeV
R = |n| / (17 MeV) ~ |n| × 10⁻¹⁴ m
```

This requires:
- Either R ~ 10⁻¹⁴ m (not Planck scale)
- Or |n| ~ 10²³ (impossibly high mode number)

**Z² framework does NOT predict X17.**

### 6.3 Alternative Interpretation

If X17 exists, it must come from:
- Dark photon (kinetic mixing with SM photon)
- Light pseudoscalar (like axion)
- New gauge boson from broken U(1)'

None of these are KK modes from T³/Z₂.

---

## 7. The 'Oumuamua Anomaly

### 7.1 Observed Acceleration

The interstellar object 'Oumuamua showed non-gravitational acceleration:
```
a_ng / a_solar ≈ 8.7 × 10⁻⁴
```

at r ~ 1 AU.

### 7.2 Fifth Force Interpretation?

Could this be a fifth force?

Required parameters:
```
α × exp(-r/λ) ~ 10⁻³ at r ~ 10¹¹ m
```

If α ~ 1 and λ ~ 10¹¹ m:
```
This requires m ~ 10⁻¹⁸ eV
```

**This is NOT a KK mode from Z² (which has m ~ 10¹⁸ GeV).**

### 7.3 Z² Prediction for 'Oumuamua

The anomalous acceleration is likely due to:
- Outgassing (standard explanation)
- Radiation pressure on thin structure
- NOT fifth force

Z² makes no prediction for 'Oumuamua beyond standard physics.

---

## 8. KK Modes and Colliders

### 8.1 Production Cross Section

At energy E << m_KK:
```
σ(KK production) ~ (E/m_KK)⁴ / M_Pl²
```

At LHC (E ~ 14 TeV):
```
σ ~ (10⁴ GeV / 10¹⁸ GeV)⁴ / (10¹⁹ GeV)²
  ~ 10⁻⁵⁶ / 10³⁸ GeV⁻²
  ~ 10⁻⁹⁴ GeV⁻² ~ 10⁻⁶² fb
```

**Completely unobservable at any foreseeable collider.**

### 8.2 Virtual KK Exchange

Virtual KK modes modify SM cross sections:
```
δσ/σ ~ (E/m_KK)² ~ (10⁴ / 10¹⁸)² ~ 10⁻²⁸
```

**No observable deviation from SM.**

---

## 9. KK Modes and Cosmology

### 9.1 KK Mode Production in Early Universe

At temperature T ~ m_KK ~ 10¹⁸ GeV:
- KK modes are thermally produced
- They decay to SM particles before BBN

### 9.2 Relic Abundance

KK modes with mass m ~ M_Pl/Z freeze out at:
```
T_f ~ m / 25 ~ 10¹⁷ GeV
```

Their abundance:
```
Ω_KK h² ~ (m/10¹⁹ GeV)² ~ (M_Pl/Z / M_Pl)² ~ 1/Z² ~ 0.03
```

But they decay:
```
τ_KK ~ M_Pl² / m³ ~ M_Pl² / (M_Pl/Z)³ ~ Z³ / M_Pl ~ 10⁻⁴¹ s
```

**KK modes decay instantly — no cosmological relic problem.**

### 9.3 KK Contribution to Dark Energy

Virtual KK modes contribute to vacuum energy:
```
Λ_KK ~ Σ_n m_n⁴ × (cutoff factor)
```

The sum is regulated by the orbifold:
```
Λ_KK ~ M_Pl⁴ / Z⁴ ~ (M_Pl / Z)⁴
```

This contributes to the total Λ but is absorbed into Λ_eff.

---

## 10. Summary: What KK Modes Do and Don't Explain

### 10.1 What T³/Z₂ KK Modes Provide:

| Property | Value | Status |
|----------|-------|--------|
| KK mass scale | M_Pl / Z ~ 10¹⁸ GeV | Derived |
| Number of modes | Infinite tower | Derived |
| Mode spacing | ~ M_Pl / Z | Uniform |
| Fifth force range | ~ Z × ℓ_Pl ~ 10⁻³⁴ m | Unobservable |
| Cosmological relics | None (fast decay) | Consistent |

### 10.2 What Z² Does NOT Explain via KK:

| Anomaly | Explanation | Status |
|---------|-------------|--------|
| X17 boson | NOT KK mode | Different physics |
| 'Oumuamua | NOT fifth force | Standard explanation |
| Fifth force hints | NOT from Z² | Other BSM needed |
| Dark photon | NOT KK photon | Requires separate U(1)' |

### 10.3 The Honest Assessment

**The KK spectrum is consistent with all observations but makes no accessible predictions.**

The compactification scale being near Planck scale means:
- All KK modes are superheavy
- No fifth force at laboratory scales
- No collider signatures
- No cosmological relics

**This is technically a "prediction" (no new physics at low energy) but is unfalsifiable with current technology.**

---

## 11. Future Possibilities

### 11.1 If Compactification Scale is Lower

If, contrary to the natural Z² choice, R >> Z × ℓ_Pl:
```
R ~ 10⁻¹⁸ m → m_KK ~ 10 TeV → LHC/FCC reach
```

But this introduces:
- New hierarchy problem (why is R large?)
- Potential conflict with precision tests

### 11.2 Indirect Signatures

Even with Planck-scale KK modes:
- Virtual exchange may shift precision observables
- Running of couplings modified at high energy
- GUT-scale effects

These are extremely small: δ ~ (E/m_KK)² ~ 10⁻²⁸ at LHC.

---

## Appendix: Detailed Mode Functions

### A.1 Complete Mode Expansion

On T³ with L = 2πR:
```
f(y) = Σ_{n∈Z³} c_n exp(i n·y / R)
```

After Z₂ projection (y → -y):
```
f(y) = Σ_{n∈(Z⁺)³} a_n cos(n·y / R)
```

### A.2 Normalization

```
∫_{T³/Z₂} d³y |f_n(y)|² = Vol(T³/Z₂) / 2^{δ_{n,0}}

= (πR)³ / 2    for n = 0
= (πR)³ / 4    for n ≠ 0
```

### A.3 Mass Matrix

The KK mass matrix:
```
M²_nm = δ_nm × |n|² / R²
```

Diagonal — no KK mode mixing.

---

*Document: KK Mode Spectrum from T³/Z₂*
*Part of Z² Framework first-principles derivations*
*Addressing Gap: Fifth force and X17 question*
