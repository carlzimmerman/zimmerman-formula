# Phase XI — Spherical Relativistic Solution

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. Setup

Spherical symmetry, static (isolated) metric:
```
ds² = -e^{2Φ(r)} c²dt² + e^{2Λ(r)} dr² + r² dΩ² .
```
Unit timelike clock `U^μ = (e^{-Φ}, 0, 0, 0)`. The curvature scalar
```
R_{uu} = R_{μν}U^μ U^ν = e^{-2Φ} R_{00} .
```
For the spherical metric, `R_{00} = e^{2(Φ-Λ)}(Φ'' + Φ'² - Φ'Λ' + 2Φ'/r)`.
The retarded equation `Box Φ_field = R_{uu}` reduces to an ODE in `r` (with the
retarded boundary condition).

## 2. The MOND regime

In the deep-MOND regime (`a_N = GM/r² << a₀`), the effective acceleration is
```
a_eff = μ(y) a_N ,   y = a_N/a₀ = GM/(r² a₀) .
```
- **Intended MOND** (`μ ~ y`): `a_eff ~ a_N²/a₀ = G²M²/(r⁴ a₀)`, giving the
  flat rotation curve `v² = r a_eff ~ GM²/(r³ a₀) · r = ...` and the BTFR.
- **With regulator** (`μ ~ y⁴`): `a_eff ~ a_N⁵/a₀⁴` (fifth-power, not MOND).

**DERIVED:** The spherical solution in the deep-MOND regime inherits the
regulator no-go: with the C² regulator, the rotation curve is **not** flat
(`v` does not approach a constant) and the BTFR is not reproduced. Without the
regulator, the flat rotation curve and BTFR are recovered, but the Hessian is
singular and the ghost (Phase VI) corrupts the solution.

## 3. The ghost in the spherical sector

The ghost `b = Φ_field - ξ` obeys `Box b = 2 R_{uu}`. In the spherical, static
case, this is an ODE sourced by `R_{uu}(r)`. The ghost is **sourced by the
spherical mass distribution** and back-reacts on the metric. The spherical
solution is therefore **contaminated by the ghost** at all radii where
`R_{uu} ≠ 0` (i.e. everywhere in the mass distribution).

**Phase XI verdict: FAIL.** The spherical solution inherits all three fatal
defects: (1) the regulator no-go (no flat rotation curve / no BTFR with the
regulator), (2) the T-gap (the clock `T` is undetermined), and (3) the ghost
(sources `b` via `R_{uu}`, corrupting the metric). The spherical solution is
**not a viable MOND galaxy model** in the frozen form.
