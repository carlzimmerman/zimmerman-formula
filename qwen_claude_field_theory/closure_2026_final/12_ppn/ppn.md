# Phase XIV — Parameterized Post-Newtonian (PPN) Analysis

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. The PPN parameters

The PPN parameters are extracted from the weak-field, slow-motion expansion of
the metric:
```
g_{00} = -1 + 2U/c² - 2β U²/c⁴ + ... ,
g_{0i} = -(7/4 - γ) V_i/c³ + ... ,
g_{ij} = δ_{ij}(1 + 2γ U/c²) + ... .
```
The key parameters: `γ` (space curvature per unit mass), `β` (nonlinearity of
gravity), `α_1, α_2, α_3` (preferred-frame), `ζ` (preferred-location),
`A, \bar{A}` (time-variation of G).

## 2. The PPN of the nonlocal theory

**DERIVED (partial):** In the weak-field limit, the field equation is
```
G_{μν} = (8πG/c⁴)T^{(m)}_{μν} + (a₀²/c⁴)E_{μν} .
```
The M-term `E_{μν}` is a **nonlocal** correction that is **suppressed** by
`(a₀/c²)²` in the PPN expansion (it is a MOND-scale effect, `a₀ ~ 10⁻¹⁰ m/s²`,
tiny compared to solar-system accelerations `~ 10⁻³ m/s²`). Therefore:

- **To leading PPN order** (solar-system, `a_N >> a₀`): `E_{μν} ~ e^{-y} ~ 0`
  (exponentially suppressed, Phase X). The PPN parameters are **GR values**:
  `γ = 1`, `β = 1`, `α_i = 0`, etc.
- **The MOND correction** enters only at **exponentially small** order
  (`e^{-y}`, `y = a_N/a₀ >> 1` in the solar system). It is **not** a
  power-law PPN correction.

**DERIVED:** The PPN parameters are **GR** to all observable orders in the
solar system (the MOND correction is exponentially suppressed, not a power
series in `v/c` or `U/c²`).

## 3. The ghost and PPN

The ghost `b` (Phase VI) is a **massless scalar** that is sourced by `R_{uu}`.
In the solar system, `R_{uu} ~ GM/(c² r³)` (small but nonzero). The ghost is
therefore **weakly sourced** in the solar system and **back-reacts** on the
metric, giving a **scalar-mediated** correction to the PPN parameters.

**UNKNOWN / concern:** The ghost's back-reaction on the PPN parameters is
**not quantified** in the frozen candidate. A massless ghost sourced by the
solar mass would give a **long-range scalar force** (a "fifth force") that is
**not** present in GR or in standard MOND. This could be **constrained** by
solar-system tests (Cassini, lunar laser ranging) and would likely be
**excluded** if the ghost coupling is of order unity.

**Phase XIV verdict: PARTIAL PASS / UNKNOWN.** The PPN parameters are GR to
leading order (the MOND correction is exponentially suppressed). However, the
**ghost** introduces a **long-range scalar force** that is not quantified and
may be excluded by solar-system tests. The PPN analysis is **incomplete**
pending the ghost back-reaction calculation.
