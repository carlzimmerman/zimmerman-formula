# Phase I addendum — REGULATOR NO-GO (decisive)

Status: **DERIVED** (from the frozen definitions). This is an internal-consistency
failure of the frozen candidate, independent of any causal/ghost/DOF analysis.

## The two requirements that collide

The frozen candidate (BASELINE.md) imposes two conditions on the constitutive
function `F_eps(Z)` near `Z = 0`:

1. **Deep-MOND interpolation law** (FROZEN, Section 3.4):
   with `Z = 4 y^2`, `y >= 0`,
   ```
   mu(y) = 1 - 2 F'(Z)  =  1 - e^{-y}  ~  y    as  y -> 0 .
   ```
   Equivalently, near `Z = 0`:
   ```
   mu ~ y  =  sqrt(Z)/2 .
   ```

2. **C^2 regularity at `Z = 0`** (FROZEN, regulator construct): `F_eps` is C^2 at
   both endpoints `|Z| = eps` and C^2-regular at `Z = 0`, implemented by the
   degree-5 polynomial `P_{5,eps}` with the imposed condition
   ```
   P''(0) = 0 .
   ```

## The contradiction (DERIVED)

Write `F'(Z) = 1/2 + a Z + b Z^2 + ...` near `Z = 0` (the value `F'(0)=1/2` is
frozen and preserves the `mu -> 0` endpoint).

- **If `F` is C^2 at 0**, then `F''(0) = a` is finite, so
  ```
  mu(Z) = 1 - 2 F'(Z) = -2 a Z + O(Z^2)  ~  Z  ~  y^2 .
  ```
  The deep-MOND law is `mu ~ y^2`, **not** `mu ~ y`. The `y`-law (MOND) is lost.

- **If `P''(0) = 0` is imposed** (the frozen regulator), then `a = 0` and
  `F'(Z) = 1/2 + b Z^2 + ...`, so
  ```
  mu(Z) = -2 b Z^2 + O(Z^3)  ~  Z^2  ~  y^4 .
  ```
  The deep-MOND law becomes `mu ~ y^4`, **not** `mu ~ y`.

- **If instead the MOND law `mu ~ y` is required**, then
  `F'(Z) = 1/2 - sqrt(Z)/4 + ...` and therefore
  ```
  F''(Z) = -1/(8 sqrt(Z)) -> -inf   as  Z -> 0+ .
  ```
  `F` is **not** C^2 at 0. This is exactly the divergence that the regulator was
  introduced to remove (`F_+''(Z) ~ -1/(8 sqrt(Z))`).

Therefore: **the deep-MOND law `mu ~ y` and C^2-regularity of `F` at `Z = 0` are
mutually exclusive.** There is no `F_eps` that satisfies both. The regulator
`P_{5,eps}` (which enforces C^2 at 0) necessarily replaces the `y`-law by a
`y^4`-law.

## Consequences for the theory

The MOND acceleration law in the Newtonian regime is
```
a_eff = mu(y) a_N ,   y = a_N / a_0 .
```
- **Intended (MOND):** `a_eff ~ y a_N = a_N^2 / a_0`  (the `a^2/a_0` law).
- **With the frozen C^2 regulator:** `a_eff ~ y^4 a_N = a_N^5 / a_0^4`  (a
  fifth-power law).

The fifth-power law is **not** MOND. It does not reproduce the Baryonic Tully-Fisher
relation (`v^4 ~ G M`), the radial acceleration relation, or the flat-rotation-curve
asymptote `v -> (G M a_0)^{1/4}`. It gives instead `v -> (G M)^{1/5} a_0^{...}`,
which is observationally excluded.

This is a **structural no-go** for the frozen candidate: the very regularity
condition required to make the local auxiliary representation well-defined (C^2 so
that the Hessian / Euler-Lagrange terms exist) destroys the phenomenological
content (the MOND law). The two cannot be had simultaneously.

## What this means for the closure audit

This is recorded as a **FAIL** for the frozen candidate on internal consistency
(Phase I). It does NOT depend on:
- the causal/in-in formulation (Phase III),
- the ghost/DOF analysis (Phases IV–VI),
- the metric field equations (Phase VII),
- lensing / PPN / cosmology (Phases XII–XVI).

Any of those could in principle be PASS and the candidate would still be dead,
because the constitutive function cannot be both C^2 at the origin and MOND.

## Possible escapes (NOT part of the frozen candidate; recorded for completeness)

1. **Abandon C^2 at 0.** Keep `F_+` (non-C^2, `F'' -> -inf`) and accept a
   singular Hessian / nonlocal kernel at `Z = 0`. This trades the regulator
   pathology for a genuine nonlocal singularity; the auxiliary/local representation
   then fails at the origin. (This is the Deffayet-Woodard-style route, which the
   prior generation found to have its own ghost/casusality problems.)

2. **Regulate with a different functional form** that keeps `mu ~ y` but rounds
   `F''` on a scale `eps` while preserving the `sqrt(Z)` cusp in `F'`. This is
   impossible: `mu ~ y` *requires* the cusp `F' ~ 1/2 - sqrt(Z)/4`, which *requires*
   `F'' ~ -1/(8 sqrt(Z))`. No rounding of `F''` can preserve `mu ~ y` to leading
   order as `y -> 0`.

3. **Change the definition of `Z`** so that the MOND law maps to a C^2 function.
   E.g. if `Z` were defined so that `y = Z` (rather than `Z = 4 y^2`), then
   `mu ~ y = Z` would require `F'(Z) = 1/2 - Z/4`, i.e. `F''(0) = -1/4` finite —
   C^2! But the frozen definition is `Z = (4 c^4/a_0^2) nabla Phi nabla^mu Phi`,
   which gives `Z = 4 y^2` in the Newtonian limit (the `y = a_N/a_0` identification
   comes from `nabla Phi ~ a_N`). Changing `Z -> Z/4` or redefining `y` would break
   the frozen normalization chain. This is a redefinition, not a repair of the
   frozen candidate.

Escape (3) is the only one that preserves the MOND law, but it requires changing
the frozen definition of `Z` (or of `y`), which is outside the frozen candidate.

## Verdict

**FAIL (internal consistency).** The frozen candidate's C^2 regulator is
incompatible with its own deep-MOND law. The candidate, as frozen, is not a
consistent MOND theory. This is a Phase-I result; it is independent of and
precedes all later phases.
