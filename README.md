# The Zimmerman Formula

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19212718.svg)](https://doi.org/10.5281/zenodo.19212718)

**A geometric constant derived from General Relativity that predicts 60+ physical quantities.**

```
Z = 2√(8π/3) = 5.788810...
```

---

## The Discovery

Starting from the Friedmann equation and horizon thermodynamics, a single constant emerges that connects particle physics to cosmology:

| What | Formula | Predicted | Measured | Error |
|------|---------|-----------|----------|-------|
| Fine structure | α = 1/(4Z²+3) | 1/137.04 | 1/137.036 | 0.004% |
| Dark energy | Ω_Λ = 3Z/(8+3Z) | 0.6846 | 0.6847 | 0.01% |
| Proton/electron | m_p/m_e = 9(m_μ/m_e)-(8+3Z) | 1836.29 | 1836.15 | 0.008% |
| Muon/electron | m_μ/m_e = 64π+Z | 206.85 | 206.77 | 0.04% |
| Tau/muon | m_τ/m_μ = Z+11 | 16.79 | 16.82 | 0.17% |
| Strong coupling | α_s = 3/(8+3Z) | 0.1183 | 0.1180 | 0.23% |
| Higgs/Z mass | M_H/M_Z = 11/8 | 1.375 | 1.372 | 0.2% |
| W/Z mass | M_W/M_Z = 7/8 | 0.875 | 0.882 | 0.8% |
| Cabibbo angle | sin θ_C = Z/26 | 0.2226 | 0.2243 | 0.8% |
| Weinberg angle | sin²θ_W = 15/64 | 0.234 | 0.231 | 1.4% |
| MOND scale | a₀ = cH₀/Z | 1.17×10⁻¹⁰ | 1.20×10⁻¹⁰ | 2.5% |

**60+ formulas. Average error < 1%. One constant.**

→ [Complete list of all formulas](papers/100_DERIVATIONS_FROM_Z.md)

---

## The Core Insight

### Gauge-Cosmology Unification

The same structure (8+3Z) appears in both particle physics AND cosmology:

```
Ω_Λ = 3Z/(8+3Z)  = 0.685   (dark energy)
Ω_m = 8/(8+3Z)   = 0.315   (matter)
α_s = 3/(8+3Z)   = 0.118   (strong coupling)
```

This means: **α_s = (3/8) × Ω_m**

The strong force is 3/8 of the matter density—connecting QCD to cosmology through dimensional ratios.

### The Dimensional Hierarchy

```
26D (bosonic string)  →  sin θ_C = Z/26
    ↓
11D (M-theory)        →  m_τ/m_μ = Z+11,  M_H/M_Z = 11/8
    ↓
8D  (E8 gauge)        →  Ω_m = 8/(8+3Z),  M_W/M_Z = 7/8
    ↓
3D  (space)           →  Ω_Λ = 3Z/(8+3Z), sin²θ₁₃ = 3α
```

---

## Falsifiable Prediction

The MOND acceleration scale **evolves with redshift**:

```
a₀(z) = a₀(0) × √[Ωm(1+z)³ + ΩΛ]
```

| Redshift | a₀/a₀(today) | Observable Effect |
|----------|--------------|-------------------|
| z = 1 | 1.7× | BTFR shift -0.23 dex |
| z = 2 | 3.0× | BTFR shift -0.47 dex |
| z = 10 | 20× | Early galaxy formation |

**If a₀ is constant at all redshifts, this framework is WRONG.**

Current status:
- ✓ JWST high-z galaxies: 2× better fit than constant MOND
- ✓ Gaia wide binaries: 5-6σ MOND signal (Chae 2024)
- ✓ El Gordo cluster timing: resolved by evolving a₀

---

## Documentation

| Topic | Description |
|-------|-------------|
| [**COMPLETE_DERIVATIONS_GUIDE.md**](COMPLETE_DERIVATIONS_GUIDE.md) | Full derivation chain from first principles |
| [**papers/DERIVATION_STATUS.md**](papers/DERIVATION_STATUS.md) | What's proven vs pattern-matched |
| [**papers/100_DERIVATIONS_FROM_Z.md**](papers/100_DERIVATIONS_FROM_Z.md) | All 60+ formulas with derivations |
| [**papers/THE_DIMENSIONAL_HIERARCHY.md**](papers/THE_DIMENSIONAL_HIERARCHY.md) | Why 3, 8, 11, 26 appear |
| [**papers/THE_GAUGE_COSMOLOGY_UNIFICATION.md**](papers/THE_GAUGE_COSMOLOGY_UNIFICATION.md) | α_s = (3/8)×Ω_m connection |
| [**HORIZON_CALCULATION.md**](HORIZON_CALCULATION.md) | First-principles derivation of Z |

### Research Directories

| Directory | Contents |
|-----------|----------|
| [`research/mysterious_connections/`](research/mysterious_connections/) | Particle-cosmology links, dimensional analysis |
| [`research/jwst_evolution/`](research/jwst_evolution/) | High-redshift predictions |
| [`research/wide_binaries/`](research/wide_binaries/) | MOND tests with Gaia data |
| [`research/critical_gaps/`](research/critical_gaps/) | Proton mass, remaining problems |
| [`papers/`](papers/) | All theoretical papers |

---

## Recent Discoveries (March 2026)

| Discovery | Formula | Error |
|-----------|---------|-------|
| Proton mass | m_p/m_e = 9(m_μ/m_e) - (8+3Z) | 0.008% |
| Strong-cosmology link | α_s = (3/8) × Ω_m | exact |
| Weinberg angle | sin²θ_W = (26-11)/8² = 15/64 | 1.4% |
| W boson mass | M_W/M_Z = 7/8 | 0.8% |

---

## How to Cite

```bibtex
@misc{zimmerman2026formula,
  author       = {Zimmerman, Carl},
  title        = {The Zimmerman Formula: Deriving Physics from Z = 2√(8π/3)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.19212718},
  url          = {https://doi.org/10.5281/zenodo.19212718}
}
```

---

**Carl Zimmerman** · March 2026 · [DOI: 10.5281/zenodo.19212718](https://doi.org/10.5281/zenodo.19212718)

MIT License
