# Zimmerman Framework: Research Directory

**The Core Derivation**

Everything in this repository traces back to one first-principles result:

```
a₀ = cH₀/Z    where Z = 2√(8π/3) = 5.7888

This implies: a₀(z) = a₀(0) × E(z)
where E(z) = √[Ωm(1+z)³ + ΩΛ]
```

**Derivation Chain:**
```
Friedmann Equation → ρc = 3H²/(8πG)
                            ↓
Dimensional Analysis → a* = c√(Gρc) = cH/√(8π/3)
                            ↓
Horizon Thermodynamics → Factor of 2 from M = c³/(2GH)
                            ↓
Result → a₀ = cH/Z where Z = 2√(8π/3)
```

---

## Directory Structure

### Tier 1: First-Principles Tests (PROVEN)

| Directory | What It Tests | Key Prediction |
|-----------|---------------|----------------|
| `jwst_evolution/` | High-z galaxy formation | a₀(z=10) = 20× local value |
| `el_gordo/` | Cluster timing tension | 1.29× speedup at z=0.87 |
| `falsification/` | Framework falsification tests | a₀(z) evolution curve |
| `full_sparc_analysis/` | SPARC galaxy rotation curves | a₀ = 1.2×10⁻¹⁰ m/s² |

### Tier 2: Strong Theoretical Support

| Directory | What It Tests | Formula |
|-----------|---------------|---------|
| `lepton_mass_ratios/` | m_μ/m_e, m_τ/m_μ | 6Z² + Z = 64π + Z |
| `electroweak/` | sin²θ_W | 1/4 - α_s/(2π) |
| `nucleon_magnetic_moments/` | μ_p, μ_n | Z - 3, -Ω_Λ×μ_p |

### Tier 3: Pattern Exploration

| Directory | What It Tests | Status |
|-----------|---------------|--------|
| `quark_masses/` | Quark mass ratios | Polynomial in Z |
| `hadron_spectrum/` | Meson/baryon masses | Various Z formulas |
| `nuclear_binding/` | Nuclear binding energies | Pattern matching |

---

## How to Use This Research

### Running a Script
```bash
cd research/jwst_evolution
python impossible_early_galaxies.py
```

### Understanding the Output
Each script:
1. States the **problem** (what ΛCDM can't explain)
2. Shows the **Zimmerman prediction** (using a₀(z) evolution)
3. Compares to **observations**
4. Generates **visualizations**

### Key Constants Used Throughout
```python
Z = 5.788810036         # = 2√(8π/3)
a0 = 1.2e-10            # m/s² (local MOND scale)
Omega_m = 0.315         # Matter fraction
Omega_Lambda = 0.685    # Dark energy fraction

# Evolution function
def E(z):
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def a0_at_z(z):
    return a0 * E(z)
```

---

## Quick Reference: Key Results

### PROVEN (First Principles)
- **Z = 2√(8π/3)** from GR + thermodynamics
- **a₀(z) = a₀(0)×E(z)** — falsifiable
- **H₀ = 71.5 km/s/Mpc** — between Planck and SH0ES

### STRONG SUPPORT
- **Ω_Λ = 3Z/(8+3Z) = 0.685** — holographic equipartition
- **α_s = Ω_Λ/Z = 0.118** — QCD-cosmology link
- **m_μ/m_e = 64π + Z** — E8/octonion structure

### PATTERN MATCHES
- **α = 1/(4Z²+3)** — 0.004% accuracy
- **μ_p = Z - 3** — 0.14% accuracy

---

## Navigation

Click into any directory to see:
1. `OVERVIEW.md` — What this section tests and why
2. `*.py` — Analysis scripts
3. `*.png` — Generated visualizations

**Start here:**
- New to the framework? → `falsification/`
- Interested in JWST? → `jwst_evolution/`
- Want the math? → `../papers/FIRST_PRINCIPLES_CHAIN.md`
