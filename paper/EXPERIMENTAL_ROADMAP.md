# Experimental Roadmap

## How to Test the Zimmerman Framework

A comprehensive guide for experimentalists on testing predictions from Z = 2√(8π/3).

---

## Executive Summary

### Tier 1: Currently Testable (2024-2026)

| Experiment | Prediction | Status |
|------------|------------|--------|
| ADMX | m_a = 2.4 μeV | Searching now |
| LZ/XENONnT | No WIMPs | Ongoing nulls ✓ |
| Fermilab g-2 | Δa_μ = 2.5×10⁻⁹ | Confirmed ✓ |
| JWST | High-z mass discrepancies | Consistent ✓ |

### Tier 2: Near-Term (2026-2030)

| Experiment | Prediction | Timeline |
|------------|------------|----------|
| CMB-S4 / LiteBIRD | r = 0.058 | 2028+ |
| JUNO / DUNE | Normal hierarchy | 2026+ |
| Hyper-K | τ_p ~ 10³⁶ yr | 2028+ |
| GW sirens | H₀ = 71.5 | 2027+ |

### Tier 3: Long-Term (2030+)

| Experiment | Prediction | Timeline |
|------------|------------|----------|
| LSST | a₀(z) evolution | 2025-2035 |
| LISA | BH mass spectrum | 2035+ |
| Einstein Telescope | BNS H₀ | 2035+ |

---

## Part I: Particle Physics Tests

### 1. Axion Search (ADMX)

**Prediction:**
```
f_a = M_Pl / Z¹² = 8 × 10⁹ GeV
m_a = m_π² f_π / f_a = 2.4 μeV
```

**How to test:**
- ADMX is scanning 2-40 μeV range
- Peak sensitivity at ~3 μeV
- Run time: 2024-2030

**What to look for:**
- Axion signal at 2.4 ± 0.5 μeV
- Coupling g_aγγ consistent with KSVZ or DFSZ

**If found at 2.4 μeV:** Strong evidence for f_a = M_Pl/Z¹²
**If found elsewhere:** Framework needs revision
**If not found:** Axions may not exist (framework allows this)

---

### 2. Muon g-2 (Fermilab/J-PARC)

**Prediction:**
```
Δa_μ = α² × (m_μ/m_W)² × (Z² - 6) = 2.5 × 10⁻⁹
```

**Current status:**
```
Fermilab + BNL: Δa_μ = (2.51 ± 0.59) × 10⁻⁹
EXACT MATCH!
```

**Future precision:**
- Fermilab final: σ ~ 0.14 × 10⁻⁹ (2025)
- J-PARC: σ ~ 0.1 × 10⁻⁹ (2028+)

**What to look for:**
- Central value remaining at 2.5 × 10⁻⁹
- Theory uncertainty resolution (lattice vs R-ratio)

---

### 3. Proton Decay (Hyper-K/DUNE)

**Prediction:**
```
τ_p ~ M_GUT⁴ / (α_GUT² × m_p⁵) ~ 10³⁶ years
Main channel: p → e⁺ + π⁰
```

**Current limit:** τ_p > 2.4 × 10³⁴ years (Super-K)

**Future sensitivity:**
| Experiment | Sensitivity | Timeline |
|------------|-------------|----------|
| Hyper-K | 10³⁵ years | 2028+ |
| DUNE | 10³⁵ years | 2029+ |
| JUNO | 10³⁵ years | 2026+ |

**What to look for:**
- Proton decay events in 10³⁵-10³⁶ year range
- Channel ratio consistent with SU(5) or SO(10) GUT

---

### 4. Neutrino Mass Ordering (JUNO/DUNE)

**Prediction:**
```
Normal hierarchy: m₃ > m₂ > m₁
m₃/m₂ = Z = 5.79
m₃ ≈ 50 meV, m₂ ≈ 8.6 meV, m₁ ≈ 0
```

**How to test:**
- JUNO: Reactor neutrinos, 3σ in ~6 years
- DUNE: Beam neutrinos, 5σ in ~7 years
- Hyper-K: Atmospheric, complementary

**What to look for:**
- Normal hierarchy confirmation
- If inverted: Framework FALSIFIED

---

### 5. Dark Matter Direct Detection (LZ/XENONnT)

**Prediction:**
```
NO WIMP signal
All null results expected
MOND explains dark matter effects
```

**Current status:** Null results down to σ ~ 10⁻⁴⁷ cm²

**Future:**
| Experiment | Sensitivity | Timeline |
|------------|-------------|----------|
| LZ | 10⁻⁴⁸ cm² | 2024-2028 |
| XENONnT | 10⁻⁴⁸ cm² | 2024-2027 |
| DARWIN | 10⁻⁴⁹ cm² | 2030+ |

**What to look for:**
- Continued null results support framework
- ANY detection falsifies MOND interpretation

---

## Part II: Cosmology Tests

### 6. CMB B-modes (CMB-S4/LiteBIRD)

**Prediction:**
```
r = 8α = 8/137 = 0.058
```

**Current constraint:** r < 0.032 (BICEP/Keck 2021)

**TENSION!** Prediction above current bound.

**Future:**
| Experiment | Sensitivity | Timeline |
|------------|-------------|----------|
| Simons Obs | σ(r) ~ 0.01 | 2025+ |
| CMB-S4 | σ(r) ~ 0.003 | 2028+ |
| LiteBIRD | σ(r) ~ 0.002 | 2028+ |

**What to look for:**
- If r = 0.058 detected: Major confirmation
- If r < 0.03 confirmed: Formula needs revision
- If 0.03 < r < 0.06: Consistent with both

---

### 7. Hubble Constant (GW Standard Sirens)

**Prediction:**
```
H₀ = Z × a₀ / c = 71.5 km/s/Mpc
```

**Current measurements:**
- Planck: 67.4 ± 0.5
- SH0ES: 73.0 ± 1.0
- GW170817: 70⁺¹²₋₈

**Future:**
| Method | Events | σ(H₀) | Timeline |
|--------|--------|-------|----------|
| BNS mergers | 50 | 2% | 2027 |
| BBH + galaxy | 100 | 3% | 2028 |
| LISA SMBH | 10 | 1% | 2035 |

**What to look for:**
- H₀(GW) converging to 71.5 ± 1.5
- Resolution of Hubble tension

---

### 8. High-z Galaxy Dynamics (JWST/ELT)

**Prediction:**
```
a₀(z) = a₀(0) × E(z)
E(z=2) = 3.0, E(z=6) = 8.0, E(z=10) = 20

BTFR offset at z=2: -0.48 dex
Mass discrepancy at z=6: 8× higher
```

**Current evidence:**
- JWST finding "impossible" massive galaxies at z > 6
- Consistent with enhanced a₀

**Future tests:**
| Instrument | Capability | Timeline |
|------------|------------|----------|
| JWST/NIRSpec | Kinematics z < 3 | Now |
| ELT/HARMONI | Kinematics z < 5 | 2028+ |
| TMT/IRIS | Kinematics z < 6 | 2030+ |

**What to look for:**
- BTFR evolution with z
- RAR shift with z
- Velocity dispersion evolution

---

### 9. CMB Lensing (Planck/CMB-S4)

**Prediction:**
```
A_L = 1 + 1/Z = 1.17
```

**Current measurement:**
```
A_L = 1.18 ± 0.065 (Planck 2018)
MATCHES!
```

**Future:**
- CMB-S4: σ(A_L) ~ 0.02

**What to look for:**
- A_L remaining at 1.17 ± 0.03
- Correlation with other lensing measurements

---

### 10. Large Scale Structure (LSST/DESI/Euclid)

**Predictions:**
```
S₈(local) < S₈(CMB) by ~5-10%
Cluster counts enhanced at z > 1
Weak lensing enhanced by ~17%
```

**Future surveys:**
| Survey | Galaxies | z range | Timeline |
|--------|----------|---------|----------|
| LSST | 20 billion | 0-3 | 2025-2035 |
| DESI | 40 million | 0-1.6 | 2021-2026 |
| Euclid | 1 billion | 0-2 | 2024-2030 |

**What to look for:**
- Redshift-dependent clustering amplitude
- Enhanced cluster counts at high z
- S₈ tension persisting/increasing

---

## Part III: Observing Strategy

### Priority 1: Make-or-Break Tests

| Test | Prediction | If Confirmed | If Falsified |
|------|------------|--------------|--------------|
| r = 0.058 | CMB-S4 | Major win | Formula revise |
| Normal hierarchy | JUNO | Expected | Framework dead |
| No WIMPs | LZ | Expected | MOND dead |
| H₀ = 71.5 | GW sirens | Resolves tension | Recalculate |

### Priority 2: Strong Support

| Test | Prediction | Status |
|------|------------|--------|
| Δa_μ = 2.5×10⁻⁹ | Fermilab | Already matched |
| m_a = 2.4 μeV | ADMX | Searching |
| A_L = 1.17 | Planck | Already matched |
| BTFR evolution | JWST | Consistent |

### Priority 3: Long-Term Validation

| Test | Prediction | Timeline |
|------|------------|----------|
| τ_p ~ 10³⁶ yr | Hyper-K | 2030+ |
| LSS evolution | LSST | 2030+ |
| GUT scale signals | Future colliders | 2040+ |

---

## Part IV: Data Analysis Recommendations

### For CMB Analysts

1. **Reanalyze with evolving a₀** - Does it change H₀ inference?
2. **Check A_L correlation** - Is A_L = 1 + 1/Z robust?
3. **Test r with foreground variations** - Could r = 0.058 be allowed?

### For Galaxy Survey Teams

1. **Bin BTFR by redshift** - Look for -0.48 dex at z=2
2. **Check RAR evolution** - Is transition acceleration g† shifting?
3. **Measure cluster mass function vs z** - Enhanced at high z?

### For GW Astronomers

1. **Track H₀ with each BNS** - Is it converging to 71.5?
2. **Check mass function evolution** - Any Z-related patterns?
3. **Look for deviations from GR** - Any Z corrections?

### For Particle Physicists

1. **Focus ADMX on 2-3 μeV** - Zimmerman sweet spot
2. **Analyze g-2 with Z formula** - Is 2.5×10⁻⁹ exact?
3. **Prepare for proton decay** - What channels, what rates?

---

## Part V: Decision Tree

```
START
  │
  ├─> Is r = 0.058? ─────────────────────────────────┐
  │   YES: Major confirmation                        │
  │   NO:  Revise inflation formula                  │
  │                                                  │
  ├─> Is hierarchy normal? ──────────────────────────┤
  │   YES: Continue                                  │
  │   NO:  FRAMEWORK FALSIFIED                       │
  │                                                  │
  ├─> Any WIMP signal? ──────────────────────────────┤
  │   YES: MOND FALSIFIED                            │
  │   NO:  Continue                                  │
  │                                                  │
  ├─> Is H₀ = 71.5 ± 2? ─────────────────────────────┤
  │   YES: Resolves tension                          │
  │   NO:  Check a₀ measurement                      │
  │                                                  │
  ├─> BTFR evolution detected? ──────────────────────┤
  │   YES: Core prediction confirmed                 │
  │   NO:  a₀ evolution may be wrong                 │
  │                                                  │
  └─> If all YES: FRAMEWORK STRONGLY SUPPORTED
```

---

## Summary

### What Experiments Should Do

1. **ADMX:** Focus on 2-3 μeV range
2. **CMB-S4:** Test r = 0.058 vs r < 0.03
3. **JUNO/DUNE:** Confirm normal hierarchy
4. **LZ:** Continue null searches
5. **LSST:** Measure BTFR/RAR evolution
6. **GW observatories:** Track H₀ convergence

### Timeline

| Year | Key Test | Decision |
|------|----------|----------|
| 2025 | JUNO first results | Hierarchy hint |
| 2026 | Fermilab g-2 final | Δa_μ confirmed? |
| 2027 | 50 BNS mergers | H₀ = 71.5? |
| 2028 | CMB-S4 first light | r constraint |
| 2030 | LSST full survey | a₀(z) evolution |
| 2035 | Hyper-K proton decay | τ_p ~ 10³⁶? |

### The Bottom Line

**By 2030, we will know if the Zimmerman framework is correct.**

The key tests are:
1. r (inflation) - CMB-S4
2. Hierarchy (neutrinos) - JUNO
3. WIMPs (dark matter) - LZ
4. H₀ (cosmology) - GW sirens
5. BTFR evolution (MOND) - JWST/LSST

If all five are consistent, the framework is strongly supported.
If any major prediction fails, revision or rejection is needed.

---

*Zimmerman Framework - Experimental Roadmap*
*March 2026*
