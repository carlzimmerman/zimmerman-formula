# A70 — MUTATIONS

`a70_checks.py` takes one environment variable, `A70_MUTATE=<name>`, which changes **one
input** before any check runs. Every mutation below was executed; the exit code is the
script's own (`0` iff all 25 checks pass). Outputs are `a70_MUTATE_<name>.out` and
`a70_MUTATE_<name>_results.json`.

Run: `A70_MUTATE=<name> python3 a70_checks.py`

## The twelve mutations

| # | name | the one input changed | exit | checks broken |
|---|---|---|---|---|
| 1 | `imf` | Salpeter `f*` (`Fs`) → Chabrier `f*` (`Fc`) in the model | **1** | K8, K10, K11, K12, K13, K14, K15, K16, K17, K19, K20, K21, K23 (13/25 fail) |
| 2 | `newton` | `a0 → 0` (baryons only; no phantom) | **1** | K8, K10, K11, K12, K13, K15, K19, K20, K21, K23, K25 (11/25) |
| 3 | `arcsec` | the `R_e(V)` column is read as kpc instead of arcsec (the file's parsing trap) | **1** | K4, K8, K10, K11, K12, K13, K14, K16, K19, K21, K23, K25 (12/25) |
| 4 | `a0shift` | the fiducial `a0` × 1.10 (1.132e-10 → 1.245e-10) | **1** | K8, K10, K11, K12, K21, K23 (6/25) |
| 5 | `treu` | every `log alpha` in Treu+2010 Table 1 +0.10 dex | **1** | K18 (1/25) |
| 6 | `dropmassive` | the seven lenses with `sigma > 300 km/s` are dropped | **1** | K1, K8, K11, K12, K17, K21, K22, K23, K24 (9/25) |
| 7 | `shuffle_re` | `R_e(V)` is permuted across lenses (fixed seed 70) | **1** | K10, K11, K12, K23 (4/25) |
| 8 | `cosmo` | the background: `(0.3, 0.7, 70)` → `(0.35, 0.65, 75)` | **1** | K2, K3, K8, K10, K11, K12, K13, K16, K19, K21, K23 (11/25) |
| 9 | `zsrc` | one source redshift moved to `z_l + 0.05` (a shallow geometry) | **1** | K1, K3, K7, K11, K12, K14, K19 (7/25) |
| 10 | `fsx` | the Salpeter `f*` column × 1.05 (a 5% column corruption) | **1** | K5, K8, K10, K11, K12, K21, K23 (7/25) |
| 11 | `ethcopy` | Etherington's `theta_E` replaced by Auger's value (two pipelines forced to agree) | **1** | K6 (1/25) |
| 12 | `gextq` | the external-shear column replaced by the axis-ratio column `q` | **1** | K9 (1/25) |

Base run: **25/25 PASS, exit 0, 7 s.**

## Coverage: every check is killed by at least one mutation

| check | killed by |
|---|---|
| K1 catalogue census | `dropmassive`, `zsrc` |
| K2 theta_E recomputation | `cosmo` |
| K3 M_E from geometry | `cosmo`, `zsrc` |
| K4 arcsec→kpc parsing | `arcsec` |
| K5 f*_Salp/f*_Chab vs SPS mass ratio | `fsx` |
| K6 the 2% R_E error is not in the data | `ethcopy` |
| K7 lens geometry | `zsrc` |
| K8 no Sérsic index; n=3/6 bracket | `imf`, `newton`, `arcsec`, `a0shift`, `dropmassive`, `cosmo`, `fsx` |
| K9 external shear vs the deficit | `gextq` |
| K10 per-lens ratios vs A55 | 7 of 12 mutations |
| K11 headline median/mean/sigma vs A55 | 10 of 12 |
| K12 Newton/Chabrier/canonical vs A55 | 10 of 12 |
| K13 A55's 1.28 is not the required M/L | `imf`, `newton`, `arcsec`, `cosmo` |
| K14 boost response vs root-found boost | `imf`, `arcsec`, `zsrc` |
| K15 R² of ln f* alone | `imf`, `newton`, `arcsec`, `cosmo` |
| K16 fixed-Salpeter kappa error (two routes) | `imf`, `newton`, `arcsec`, `cosmo`, `zsrc` |
| K17 kappa unconstrained with a free IMF | `dropmassive` |
| K18 Treu+2010 mean/scatter/95% | `treu` |
| K19 1.17x vs the SLACS dynamical 95% | `imf`, `newton`, `arcsec`, `cosmo`, `zsrc` |
| K20 CvD12b relation | `imf`, `newton` |
| K21 the two 95% intervals disagree | `imf`, `newton`, `arcsec`, `a0shift`, `dropmassive`, `cosmo`, `fsx` |
| K22 Auger+2010 f_DM at R_e/2 | `dropmassive` |
| K23 chi2/dof and excess scatter | 10 of 12 |
| K24 residual sigma-trend → IMF(sigma) | `dropmassive` |
| K25 shape at fixed amplitude | `newton`, `arcsec` |

## Deleted checks (and why)

Five candidate checks were written, then **removed from the check list** because no input
mutation can make them fail. Their numbers are still printed and stored in
`a70_results.json`; they are diagnostics, not gates.

1. **Phantom projection, two routes** (law-route projected phantom vs a direct Newtonian
   projection of `M_b F(y)`): 0.2433 vs 0.2407. This is an algebraic identity of one
   implementation — both routes are the same model, so every input mutation moves both
   together. It can only fail if the code is broken, which is not an input change.
2. **`c_n = B(2n+1)/B(n+1)` = π/4 at n=1**: an analytic constant, independent of every
   input (prints 0.8346 / 0.7854 / 0.7628 / 0.7500).
3. **`dlnR/dlnkappa` = 0.1205**: the 0.08–0.18 window is physical, not data-derived; the
   Chabrier mutation moves it only to 0.144, still inside. Its mutation-sensitive
   consequence is K17 (the flat Δχ² with a free IMF).
4. **`kappa*` = 1.0279 (Salpeter fixed)**: a derived position, reported. Its consequence
   is carried by K16/K17.
5. **Band medians** (0.8830 at κ=0.490, 0.8908 at κ=0.5265): reported in the κ table.

## What the mutations establish

- The headline is **not** a coding artefact: K10 reproduces A55's 70 per-lens ratios to
  2×10⁻¹⁶, and any single-input change moves it.
- The **IMF is the load-bearing input**: swapping Salpeter→Chabrier breaks 13 of 25
  checks, more than any other mutation.
- The **arcsec parsing trap** is real and is caught by K4/K8/K13/K14/K16.
- The **environment and data-integrity checks** are not decorative: `gextq`, `ethcopy`,
  `zsrc` and `fsx` each break exactly the check designed for them.
- The **κ result is a null**: no mutation of the κ conversion can break a κ check,
  because the κ scan is expressed in κ; what breaks it is changing the mass
  normalisation (`imf`, `newton`, `a0shift`), which is the point of Task 3.
