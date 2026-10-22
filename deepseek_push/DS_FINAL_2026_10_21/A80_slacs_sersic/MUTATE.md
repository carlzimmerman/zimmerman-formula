# A80 — MUTATIONS

`A80_MUTATE=<name> python3 a80_checks.py` changes **one physical input or solver relation** and must
exit 1. Nine mutations, each run from a cold start, each recorded below with its exit code and the
checks it kills. The clean run is `25/25 PASS, exit 0` (38 s); every one of the 25 checks is killed
by at least one mutation (matrix at the bottom).

| mutation | what it changes (one thing) | exit | checks killed |
|---|---|---|---|
| `fix_n4` | forces n = 4 everywhere in the solver, so no free-n fit can move | 1 | 9 |
| `wrong_bn_coeff` | `b_n = 2n − 1/3` (the asymptotic series truncated before its 1/n terms) instead of the exact root of `gammainc(2n,b)=1/2` | 1 | 6 |
| `invert_re_ratio` | uses x = R_e/R_E everywhere instead of x = R_E/R_e | 1 | 18 |
| `imf_prior_shift` | moves the Treu+2010 prior mean by +0.04 dex (1.00 → 1.0965) | 1 | 1 |
| `newton_limit` | a₀ → 1e-14 m/s² (the Newtonian limit), so the law has no a₀ dependence | 1 | 10 |
| `drop_lens` | drops 5 lenses (65 instead of 70) | 1 | 8 |
| `fake_ncol` | appends a Sérsic-index column `n` to the catalogue header (a column that does not exist) | 1 | 1 |
| `omega_shift` | Ω_Λ = 0.70 instead of 0.6847 in the thermal-a₀ footing identity | 1 | 1 |
| `deproj_bad` | substitutes the 2D enclosed fraction for the 3D one (`F3 ← gammainc(2n, …)`), i.e. drops the line-of-sight deprojection | 1 | 10 |

Each mutation is a change to a *physical* input or to a *solver relation* — never to a tolerance, a
threshold or a print string. Nothing in the script compares a declared symbol with an expression
that does not contain it, no check has a hardcoded PASS string, and no target is a closed form
decoupled from the computed quantity: every `ck()` compares two independently computed numbers
(the solver against an adaptive-quadrature deprojection, the model against A55/A70's stored arrays,
the sweep against a direct B-profile, two routes to the same regression, etc.).

## Coverage matrix

`.` = PASS, `FAIL` = killed.

| check | fix_n4 | wrong_bn_coeff | invert_re_ratio | imf_prior_shift | newton_limit | drop_lens | fake_ncol | omega_shift | deproj_bad |
|---|---|---|---|---|---|---|---|---|---|
| K1  | . | . | . | . | . | FAIL | . | . | . |
| K2  | . | . | . | . | . | . | FAIL | . | . |
| K3  | FAIL | FAIL | . | . | . | . | . | . | . |
| K4  | . | . | . | . | . | . | . | . | FAIL |
| K5  | . | . | FAIL | . | . | . | . | . | . |
| K6  | . | FAIL | FAIL | . | FAIL | FAIL | . | . | . |
| K26 | . | FAIL | FAIL | . | FAIL | FAIL | . | . | . |
| K7  | . | . | FAIL | . | FAIL | FAIL | . | . | . |
| K8  | . | . | FAIL | . | FAIL | FAIL | . | . | . |
| K9  | . | . | FAIL | . | . | . | . | . | FAIL |
| K10 | FAIL | FAIL | . | . | . | . | . | . | . |
| K11 | FAIL | FAIL | . | . | . | . | . | . | FAIL |
| K12 | FAIL | . | FAIL | . | . | . | . | . | FAIL |
| K13 | . | . | FAIL | . | FAIL | . | . | . | FAIL |
| K14 | . | . | FAIL | . | FAIL | . | . | . | FAIL |
| K15 | FAIL | . | FAIL | . | . | . | . | . | FAIL |
| K16 | FAIL | . | FAIL | . | . | . | . | . | FAIL |
| K17 | FAIL | . | FAIL | . | . | . | . | . | . |
| K18 | FAIL | . | FAIL | . | . | . | . | . | FAIL |
| K19 | FAIL | . | FAIL | FAIL | . | . | . | . | FAIL |
| K20 | . | FAIL | FAIL | . | FAIL | FAIL | . | . | . |
| K21 | . | . | FAIL | . | FAIL | FAIL | . | . | . |
| K22 | . | . | FAIL | . | FAIL | . | . | . | . |
| K23 | . | . | FAIL | . | FAIL | FAIL | . | . | . |
| K24 | . | . | . | . | . | . | . | FAIL | . |
| **kills** | 9 | 6 | 18 | 1 | 10 | 8 | 1 | 1 | 10 |

Every check is killed at least once. The weak rows are the ones that are supposed to be weak:
`imf_prior_shift` and `omega_shift` change a single scalar that only one check probes, and
`fake_ncol` changes only the header.

## Deleted check, and why

**K25 (the 4-node lnB interpolation) was deleted as a check.** It compared `y_at(B)` — a cubic
Lagrange interpolant in lnB — against `residual(B)`, one exact solve, and asserted they agree to
1e-3. Both are evaluations of the *same* model: no change to a physical input or to a solver
relation can make them disagree, so no mutation could kill it under any mutation. A check that
cannot fail is not a check. The numbers are still computed and printed in `a80.out`
("off-grid validation of the 4-node lnB interpolation": max |dlnR| 1.9e-06 and 1.1e-06), and they
matter — they are what allows the fits to be affordable — but they are a diagnostic, and they are
labelled as one in the script.

No other check had to be deleted: all 25 remaining checks are killed by at least one of the nine
mutations.
