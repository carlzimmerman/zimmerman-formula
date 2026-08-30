# Conventions

Signature, indices, and operator conventions used throughout `closure_2026_final`.

## Metric signature

**(-, +, +, +)** — "mostly plus". This is the convention under which the timelike
normalization reads

```
nabla_mu T nabla^mu T = -1 .
```

With signature (-,+,+,+), a unit timelike vector `U^mu` satisfies `U^mu U_mu = -1`.

## Indices and curvature

- Greek indices `mu, nu = 0..3`; Latin `i, j = 1..3` for spatial (3+1) splits.
- `g_{mu nu}` the metric, `g = det(g_{mu nu})`, `sqrt(-g) > 0`.
- `R` the Ricci scalar, `R_{mu nu}` the Ricci tensor, `R_{mu nu rho sigma}` the Riemann tensor.
- Curvature convention: the Einstein-Hilbert action is `+ (c^3/16 pi G) int sqrt(-g) R`,
  giving the standard Einstein equation `G_{mu nu} = (8 pi G / c^4) T^{(m)}_{mu nu}` in GR.
  (This fixes the sign of the Riemann tensor: `R^rho_{ sigma mu nu} =
   partial_mu Gamma^rho_{nu sigma} - ...` so that a flat-space perturbation gives the
  standard linearized Einstein tensor.)

## D'Alembertian

```
Box = nabla_mu nabla^mu = (1/sqrt(-g)) partial_mu ( sqrt(-g) g^{mu nu} partial_nu ) .
```

`Box_ret` denotes the retarded inverse: `Phi = Box_ret^{-1} S` means
`Box Phi = S` with retarded (causal) boundary conditions.

## Units

SI throughout unless stated. `c` the speed of light, `G` Newton's constant,
`a_0` the MOND acceleration scale. The action is written with explicit `c` factors:

```
S_tot = S_m[g,psi] + (c^3/16 pi G) int d^4x sqrt(-g) [ R - 2 Lambda - (a_0^2/c^4) M[g] ] .
```

## Function argument

`F` is a function of the single scalar `Z`. `F'(Z)`, `F''(Z)`, `F'''(Z)` denote
derivatives with respect to `Z`.

## Claim-status labels

Every significant statement is labeled exactly one of:
`DERIVED` (follows from the action by calculation), `IMPOSED` (a manual choice of
boundary/initial condition or gauge), `FITTED` (a parameter chosen from observation),
or `UNKNOWN` (not yet established).
