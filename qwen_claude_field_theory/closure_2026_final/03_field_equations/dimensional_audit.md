# Phase VIII — Dimensional and Consistency Audit

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. Dimensional analysis (SI, [L,M,T])

Convention: signature (−,+,+,+), `g_{μν}` dimensionless, `c` and `G` and `a_0`
as usual.

| Quantity | Dimension | Derivation |
|----------|-----------|------------|
| `R`, `R_{μν}`, `R_{uu}` | L⁻² | curvature |
| `Box` | L⁻² | two derivatives |
| `Φ` | L⁰ | from `Box Φ = R_{uu}` (L⁻² · L²) |
| `c⁴/a₀²` | L² | (L⁴T⁻⁴)/(L²T⁻⁴) = L² |
| `∇Φ · ∇Φ` | L⁻² | Φ dimensionless |
| `Z = (4c⁴/a₀²)∇Φ·∇Φ` | L⁰ | L² · L⁻² |
| `F(Z)`, `M` | L⁰ | from transport `M + F = const` |
| `c³/G` | M T⁻¹ | (L³T⁻³)/(M⁻¹L³T⁻²) |
| `d⁴x` | L³ T | |
| `a₀²/c⁴` | L⁻² | (L²T⁻⁴)/(L⁴T⁻⁴) |

**Action-term dimensions:**
```
[(c³/G) ∫ d⁴x R]                 = (M T⁻¹)(L³ T)(L⁻²) = M L   (action) ✓
[(c³/G) ∫ d⁴x (a₀²/c⁴) M]        = (M T⁻¹)(L³ T)(L⁻²)(L⁰) = M L   (action) ✓
```
The M-term has the **same dimension** as the Einstein-Hilbert term. **DERIVED:
consistent.**

**Field-equation dimensions:**
```
[G_{μν}] = L⁻²,  [Λ] = L⁻²
[(a₀²/c⁴) E_{μν}] = L⁻²   =>   [E_{μν}] = L⁰   (dimensionless)
[(8πG/c⁴) T^{(m)}_{μν}] = L⁻²   =>   [T^{(m)}_{μν}] = M L⁻¹ T⁻²   (energy density) ✓
```
**DERIVED: consistent.** `E_{μν}` is dimensionless, as expected for a
curvature-scale stress tensor.

## 2. Consistency checks

| Check | Result | Status |
|-------|--------|--------|
| M-term dimension = EH-term dimension | PASS (both `M L`) | DERIVED |
| `E_{μν}` dimensionless | PASS | DERIVED |
| `Z` dimensionless | PASS | DERIVED |
| `Φ` dimensionless | PASS | DERIVED |
| `μ(y)` dimensionless | PASS (y = a_N/a₀ dimensionless) | DERIVED |

## 3. Verdict

**Phase VIII verdict: PASS (dimensions consistent).** There is **no dimensional
inconsistency** in the frozen candidate. The M-term, the constitutive scalar
Z, and the M-stress tensor E_{μν} all carry the correct dimensions. This is a
**necessary** (not sufficient) condition for viability, and it is satisfied.

> Note: dimensional consistency is independent of the three fatal defects found
> in Phases I, II, and VI (regulator no-go, T-gap, physical ghost). The
> candidate is dimensionally sound but structurally broken.
