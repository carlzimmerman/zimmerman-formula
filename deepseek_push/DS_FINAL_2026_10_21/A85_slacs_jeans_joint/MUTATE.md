# A85 — MUTATIONS

`A85_MUTATE=<name> python3 a85_checks.py` changes **one** ingredient of the solver and must make the
script exit 1. **Eight mutations, eight runs, all exit 1** (`a85_MUTATE_<name>.out`,
`a85_MUTATE_<name>_results.json`).

| mutation | what it changes (one line of physics) | checks killed | pass | exit |
|---|---|---|---|---|
| `newton_jeans` | `a0 -> 0` **in the Jeans g only**, leaving the lensing g unchanged — lensing and dynamics no longer see the same law | **K12, K15, K26** | 29/32 | 1 |
| `wrong_aperture_radius` | `R_ap = 3.0 arcsec` instead of 1.5 (the fibre diameter used as a radius) | **K13, K15, K25, K26** | 28/32 | 1 |
| `corrupt_virial` | drops one `cosh u` factor in the line-of-sight projection — a wrong `r dr/sqrt(r^2-R^2)` measure | **K12, K15, K26** | 29/32 | 1 |
| `shift_anisotropy` | `+0.1` on beta **in the projection term only**, so the beta inside `nu sigma_r^2` and the beta in `(1 - beta R^2/r^2)` disagree | **K12, K15, K26** | 29/32 | 1 |
| `invert_b_lens` | the stellar normalisation uses `1/B` instead of `B` | **K5, K6, K28** | 29/32 | 1 |
| `tophat_psf` | the fibre weight becomes a step `R < R_ap` — no seeing convolution | **K13, K16** | 30/32 | 1 |
| `deproj_bad` | 5 per cent error in the 3D density normalisation of the Abel inversion | **K1, K2, K3, K4, K5, K8, K12b** | 25/32 | 1 |
| `beta_sign` | flips the sign of the projection anisotropy term, `(1 + beta/cosh^2 u)` | **K12** | 31/32 | 1 |

## What each kill means

* **K12 (virial identity)** is the deepest check. For *any* constant beta the infinite-aperture,
  luminosity-weighted `sigma_los^2` must equal `(1/3) Int rho_* r g d^3r / M_*` exactly, because the
  beta terms cancel between the Jeans integral and the projection. `newton_jeans` breaks it because
  the Jeans g no longer matches the g that defines the right-hand side; `corrupt_virial` and
  `shift_anisotropy` break the measure; `beta_sign` breaks the cancellation. Measured departure for
  `newton_jeans`: `1.12e-01` against `5.11e-04` nominal — a factor 220.
  Note that `beta_sign` is invisible to K17 (sigma_ap stays monotone increasing in beta, it just
  increases faster: `216.59 -> 287.39 km/s`). Only an exact identity can see a sign convention.
* **K15 (independent brute-force reimplementation)** is the second net: it re-derives the same
  `sigma_ap` with a different deprojection grid, an `l = sqrt(r^2-R^2)` quadrature and a direct 2D
  Gaussian convolution. Any change to the physics kills it; numerical re-arrangements alone would not.
* **K13/K16 (PSF kernel, grid convergence)** catch a wrong or grid-dependent aperture weight.
  `tophat_psf` is the case: a step whose edge does not align with the `R` grid makes `sigma_ap`
  grid-dependent, so K16's convergence tolerance fails as well as K13.
* **K5/K6** are the A70 cross-checks (`B_req = 1.1754` vs 1.1738; `dlnR/dlnB` and `dlnR/dlnk`). They
  are what makes `invert_b_lens` visible at all: the lens equation is still solved exactly (K7
  passes!) because the root-find simply inverts the inverted normalisation — only the *value* of B
  is wrong, and only the A70 anchor and the monotonicity of the kappa sweep notice.
* **`deproj_bad`** is the broadest kill because the deprojection feeds everything: the mass integral
  (K1: `1.04999992` vs `0.99999998`), the round trip (K2), the P&S comparison (K3), every
  Sersic-index total (K4), the A70 anchor (K5), the Newtonian limit (K8) and the P&S-vs-exact
  sigma_ap (K12b).

## Coverage, stated honestly

The eight mutations kill **15 of the 32 checks**: K1, K2, K3, K4, K5, K6, K8, K12, K12b, K13, K15,
K16, K25, K26, K28. The remaining 17 are **measurements of the data, not tests of the solver** —
Route-1 means, Route-2 best fits, the Fisher determinant, the kappa profile. A mutation moves their
values (the Route-1 mean changes by a factor 3 under `newton_jeans`) but not across a pass
threshold, because those thresholds are physics statements (e.g. "the mean offset is under 20 per
cent"), not solver statements. They are kept because they are what the lane reports; they are not
counted as mutation coverage.

## Deleted check (with reason)

One candidate check was written and then **deleted rather than loosened**: "the aperture integral
reduces to the central line-of-sight dispersion as `R_ap -> 0`". For a Sersic n = 4 profile
`Sigma(R) = exp(-b (R/R_e)^{1/4})` is already down to ~22 per cent of its central value at
`R = 0.0015 R_e`, so `sigma_los(R)` varies by a factor ~2 inside `R < 0.002 R_e`; the limit probes
radii that no fixed radial grid resolves, and the check would have measured the grid, not the
physics. The aperture machinery is instead validated by K12 (virial, exact), K13 (kernel vs direct
2D quadrature, `1.62e-14`), K14 (fibre flux vs the analytic Sersic fraction, `0.3819` vs `0.3819`)
and K15 (independent reimplementation, `-1.78e-03`).

No check in the final set can pass without the number it claims to test: every `ck(...)` boolean is
an expression over computed arrays, there is no `ok = True` anywhere, and no check compares a symbol
against an expression that does not contain it.
