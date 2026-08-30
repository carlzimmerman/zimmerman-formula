# Phase XIII — Tensor Sector (Gravitational Waves)

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. Tensor perturbations

Linearize the metric around flat space with a transverse-traceless tensor
perturbation `h^{TT}_{ij}`:
```
g_{μν} = η_{μν} + h_{μν} ,   h^{TT}_{ij}:  ∂^i h_{ij} = 0,  h^i_i = 0 .
```
The tensor perturbation is **decoupled** from the scalar (Φ, ξ, M, η, T) sector
at linear order (by symmetry). The question is whether the nonlocal M-term
modifies the tensor propagator.

## 2. The M-term and tensor modes

**DERIVED:** The M-stress tensor `E_{μν} = δM/δg^{μν}` depends on the metric
through `R_{μν}U^μU^ν` (the source for Φ) and through `Z = (4c⁴/a₀²)∇Φ·∇Φ`.
For a **pure tensor** perturbation `h^{TT}_{ij}`:
- `R_{μν}U^μU^ν` (with `U^μ = (1,0,0,0)`) involves `R_{00}`, which for a
  TT tensor perturbation is **zero** (TT perturbations do not source `R_{00}`
  at linear order).
- Therefore the source for Φ **vanishes** for pure tensor modes, and Φ, Z, M
  are **unperturbed** by the tensor mode.
- Hence `E^{TT}_{ij} = 0` at linear order: the M-term **does not modify** the
  tensor propagator.

**DERIVED:** The tensor sector is **identical to GR** at linear order. The
gravitational waves propagate at the speed of light with the two standard
polarizations, **unmodified** by the nonlocal M-term.

## 3. The ghost and tensor modes

The ghost `b = Φ - ξ` is a **scalar** mode (it comes from the scalar Φ, ξ
sector). It does **not** mix with the TT tensor modes at linear order (different
spin). Therefore the ghost does **not** directly affect the tensor propagator.
However, the ghost **is** sourced by `R_{uu}`, which for a tensor perturbation
is zero, so the ghost is **not excited** by pure tensor modes either.

**DERIVED:** The tensor sector is **clean** (GR-like, no ghost, no
modification). This is a **PASS** for the tensor sector specifically.

## 4. Summary

| # | Result | Status |
|---|--------|--------|
| 1 | M-term does not modify the TT tensor propagator (`R_{uu}=0` for TT). | DERIVED |
| 2 | Tensor sector is identical to GR at linear order. | DERIVED |
| 3 | Ghost does not mix with TT tensor modes (different spin). | DERIVED |
| 4 | Gravitational waves propagate at `c` with 2 polarizations (GR-like). | DERIVED |

**Phase XIII verdict: PASS (tensor sector is GR-like).** The tensor sector is
clean and unmodified by the nonlocal term. This is a **necessary** condition
and it is satisfied. However, the **scalar** sector (Φ, ξ, M, η, T) is broken
(ghost, T-gap, regulator no-go), so the theory as a whole is still non-viable.
