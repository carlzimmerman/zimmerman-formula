# Phase XV — FLRW Cosmology

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. Setup

FLRW metric:
```
ds² = -c²dt² + a(t)² [ dr²/(1-kr²) + r² dΩ² ] .
```
Homogeneous and isotropic. The unit timelike clock `U^μ = (1,0,0,0)` (comoving).
The curvature scalar
```
R_{uu} = R_{μν}U^μU^ν = R_{00} .
```
For FLRW, `R_{00} = -3 ä/a` (in units where the spatial curvature is absorbed;
more precisely `R_{00} = -3(ä/a)` for the time-time component with the
conventions of the Einstein equation).

The retarded equation `Box Φ = R_{uu}` becomes an ODE in cosmic time `t`.

## 2. The FLRW M-term: the sign of Z

**DERIVED:** In FLRW, the only nonzero component of `∇_μ Φ` for a homogeneous
`Φ(t)` is the time component, and `g^{00} = -1/c²` (signature −+++). Therefore
```
Z = (4c⁴/a₀²) g^{μν} ∇_μ Φ ∇_ν Φ
  = (4c⁴/a₀²) g^{00} (∂_t Φ)²
  = -(4c²/a₀²) (∂_t Φ)²   <= 0 .
```
The source equation `Box Φ = R_{uu} = R_{00} = -3 ä/a` gives
```
∂_t² Φ + 3H ∂_t Φ = 3 ä/a ,
```
so `∂_t Φ ≠ 0` generically (Φ is time-dependent, sourced by the cosmic
acceleration). Hence
```
Z < 0        (in the homogeneous FLRW background, generically).
```

**DERIVED (key):** The homogeneous FLRW background lies on the **`Z < 0`
branch** of the constitutive function, i.e. it requires the **`F_-(Z)` branch**.
But the frozen candidate **specifies only the `F_+(Z)` branch** (`Z >= 0`);
the `F_-(Z)` branch (`Z < 0`) is **not specified** (the **F₋ gap**, noted in
Phase I, `nonlocal_functional.py` §3). Therefore the M-term in the homogeneous
FLRW background is **not defined** by the frozen candidate.

> This corrects an earlier draft that (wrongly) set `Z = 0` in FLRW. The
> spatial gradients vanish, but the **time** gradient does not, and with
> `g^{00} < 0` it gives `Z < 0`, not `Z = 0`.

## 3. The ghost in FLRW

The ghost `b = Φ - ξ` obeys `Box b = 2 R_{uu} = -6 ä/a`. In FLRW, this is a
**time-dependent ODE** sourced by the cosmic acceleration `ä/a`. The ghost is
therefore **sourced by the cosmic expansion** and back-reacts on the
Friedmann equation. The ghost gives a **negative-energy contribution** to the
cosmic energy density, leading to a **cosmological instability**.

**DERIVED:** The ghost is sourced by the cosmic expansion (`R_{uu} = -6ä/a`)
and back-reacts on the Friedmann equation, introducing a **negative-energy
component** that destabilizes the cosmology.

## 4. The Friedmann equation with the M-term

The `00` component of the field equation gives
```
(ä/a) + ... = (8πG/3c²)(ρ + ...) + (a₀²/c⁴) E_{00} .
```
The M-term `E_{00}` is the nonlocal cosmological correction, which depends on
`F_-(Z)` and its derivatives evaluated at `Z < 0`. Since the `F_-(Z)` branch is
**not specified** in the frozen candidate, the M-term is **not determined**.

**UNKNOWN:** The cosmological M-term is **not determined** in the frozen
candidate because the homogeneous background requires the unspecified
`F_-(Z)` branch (`Z < 0`). The cosmology is **ill-defined** (F₋ gap).

## 5. Summary

| # | Result | Status |
|---|--------|--------|
| 1 | Homogeneous FLRW has `Z = -(4c²/a₀²)(∂_t Φ)² < 0` (time gradient, `g^{00}<0`). | DERIVED |
| 2 | The background requires the `F_-(Z)` branch, which is **not specified** (F₋ gap). | DERIVED |
| 3 | The M-term is not defined in the homogeneous FLRW background. | DERIVED |
| 4 | The ghost is sourced by the cosmic expansion (`R_{uu} = -3ä/a`) and destabilizes the cosmology. | DERIVED |
| 5 | The Friedmann equation with the M-term is not determined (F₋ gap). | UNKNOWN |

**Phase XV verdict: FAIL / UNKNOWN.** The FLRW cosmology is **ill-defined** in
the frozen candidate: the homogeneous background lies at `Z < 0`, requiring the
unspecified `F_-(Z)` branch (F₋ gap), and the ghost is sourced by the cosmic
expansion (Phase VI), destabilizing the cosmology. The candidate does **not**
give a well-defined, stable cosmology.
