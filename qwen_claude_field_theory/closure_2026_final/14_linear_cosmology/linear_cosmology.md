# Phase XVI — Linear Cosmological Perturbations

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. Setup

Perturb the FLRW background:
```
ds² = -(1+2Ψ̃)c²dt² + a²(t)[(1-2Φ̃)δ_{ij} + h_{ij}]dx^i dx^j ,
```
with scalar perturbations `Ψ̃, Φ̃` (Newtonian gauge), tensor `h_{ij}^{TT}`,
and the auxiliary scalar perturbations `δΦ, δξ, δM, δη, δT`.

## 2. The scalar perturbation sector

**DERIVED:** The scalar perturbation system couples:
- the metric scalars `Ψ̃, Φ̃`,
- the matter perturbations (density contrast `δρ`),
- the auxiliary scalars `δΦ, δξ, δM, δη, δT`.

The M-term contributes a **nonlocal** source to the perturbed Einstein
equations, built from the retarded Green's function of the FLRW `Box` and the
transport integral along the comoving flow.

**UNKNOWN:** The full linearized system **cannot be written** in the frozen
candidate because:
1. The background M-term is undefined (F₋ gap, Phase XV: the background is at
   `Z < 0`, requiring the unspecified `F_-(Z)` branch).
2. The T-gap (Phase II): `δT` is undetermined.
3. The ghost `δb = δΦ - δξ` is part of the system (Phase VI).

Without a defined background, the **linearized** equations (which are
variations *about* the background) are not determined.

## 3. The ghost instability in the perturbations

**DERIVED:** The ghost perturbation `δb` obeys
```
Box δb = 2 δR_{uu} ,
```
with the FLRW retarded Green's function. The ghost mode has a **negative
kinetic term** and therefore an **unstable** mode function: its amplitude
grows (rather than oscillates or decays) in time. This is a **cosmological
ghost instability**: the ghost perturbation grows on all scales, dominating
the perturbation spectrum at late times.

**DERIVED:** The linear cosmological perturbations are **unstable** due to the
ghost. The perturbation spectrum is corrupted by the growing ghost mode.

## 4. Summary

| # | Result | Status |
|---|--------|--------|
| 1 | The scalar perturbation system couples metric, matter, and auxiliary scalars. | DERIVED |
| 2 | The full linearized system is not determined (F₋ gap, T-gap). | UNKNOWN |
| 3 | The ghost perturbation `δb` is unstable (growing mode). | DERIVED |
| 4 | The perturbation spectrum is corrupted by the ghost. | DERIVED |

**Phase XVI verdict: FAIL / UNKNOWN.** The linear cosmological perturbations
are **not determined** (F₋ gap, T-gap) and are **unstable** (ghost growing
mode). The candidate does not give a well-defined, stable linear perturbation
spectrum.
