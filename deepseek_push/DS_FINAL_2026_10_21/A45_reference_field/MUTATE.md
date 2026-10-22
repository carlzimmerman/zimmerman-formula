# A45 mutations

Five, each run as `python3 a45_checks.py --mutate <name>`, each writing its own
`a45_MUTATE_<name>.out` / `a45_results_MUTATE_<name>.json` and each exiting **1**. The unmutated run exits 0
with **25/25**. Every mutation changes either a **term** in the linearised P equation or the **reading** the
lane adopts, and each is caught by the check that exists to protect that step.

| mutation | what changes | first broken check | unmutated -> mutated |
|---|---|---|---|
| **M1 `gamma_pc`** | the P stiffness scale: `L* = 24 pc` read as `24 Mpc` | **K6** (and K8) | coefficient `1.000 -> 0.433`; `(k lambda_P)^2 = 1.3e-12 -> 1.31`; `(eta/K)H^2 = 1.5e-17 -> 1.5e-5` |
| **M2 `pointwise`** | the adopted reading becomes branch (b) (the resummed pointwise law) | **K13**, K21 | `sigma8 = 0.7602 -> 2.2668` |
| **M3 `cH`** | the adopted reading becomes branch (a) (`g_ref = cH`) | **K13**, K21 | `sigma8 = 0.7602 -> 0.7619` (a 0.22 % shift, caught at the 1e-6 level) |
| **M4 `quad`** | the law itself: the `n = 2` quadrature interpolation replaces the saturating log | **K12** | `sigma8(b) = 2.267 -> 1.921` |
| **M5 `nocut`** | the threshold in the bound-system scan is removed (the pointwise law everywhere) | **K15** | `delta_c(0.832) = 0.677 -> 0.000` |

## M1 — `gamma_pc`: the 17 pc stiffness read as 17 Mpc

`L_STAR = 24.0 * Mpc` instead of `24.0 * pc`, i.e. a unit slip of `1e6` in the only length the P sector
carries. Everything else is untouched, so this is a clean test of whether the "coefficient = 1" claim is
load-bearing on the P scale:

| quantity | unmutated | mutated |
|---|---|---|
| `(gamma/K) k^2` at 0.1 h/Mpc | `1.31e-12` | **`1.31`** |
| coefficient `1/(1+(k lambda_P)^2)` | `1.0000000` | **`0.433`** |
| `(eta/K) H^2` | `1.5e-17` | **`1.5e-5`** |
| K6 / K8 | PASS / PASS | **FAIL / FAIL** |

What it proves: K6 is not a tautology. The P field is a slave *because* `lambda_P = 17 pc` is twelve orders of
magnitude below any cosmological scale; at 17 Mpc it would not be, and the linear response would acquire a real
`k` dependence. It also shows why the `(D.P)^2`/`F^2` cancellation (K5) matters — with a 17 Mpc stiffness the
P sector would propagate and the whole quasi-static reduction would fail.

## M2 — `pointwise`: branch (b) adopted as the theory's prediction

`x_v, D_v, f_v, S8_V = D_b, f_b, S8_B`. The derivation checks are untouched; only the reading the lane reports
changes.

| check | unmutated | mutated |
|---|---|---|
| K13 adopted branch is `G_eff = 1` | `0.7602` | **`2.2668`** (FAIL) |
| K21 filtered reading | `0.7602` | **`2.2668`** (FAIL) |
| total | 25/25 | **23/25, exit 1** |

What it proves: the verdict is not decoration. Adopting the pointwise reading changes `sigma8` by `2.98×`,
and K13/K21 are the checks that pin the adopted branch to the one the action's linear order allows.

## M3 — `cH`: branch (a) adopted as the theory's prediction

`x_v, D_v, f_v, S8_V = D_a, f_a, S8_A`.

| check | unmutated | mutated |
|---|---|---|
| K13 | `0.7602` | **`0.7619`** (FAIL) |
| K21 | `0.7602` | **`0.7619`** (FAIL) |
| total | 25/25 | **23/25, exit 1** |

What it proves: the two surviving numbers differ by only `0.22 %`, and the check still catches it — the adopted
branch must be the one with **exactly** `G_eff = 1`, not the one with a 1.4 % `cH` boost. This is deliberate:
`cH` is the reading that "looks right" numerically and has no action-level origin, so it is the mutation most
likely to slip through unnoticed.

## M4 — `quad`: the interpolation changed from the saturating log to the `n = 2` quadrature law

`RESP = response_quad`, i.e. `dg/dg_N = (1+1/(2y))/sqrt(1+1/y)`.

| check | unmutated | mutated |
|---|---|---|
| K12 branch (b) reproduces A40's 2.267 | `2.267` | **`1.921`** (FAIL) |
| `G_eff(0)` | `11.75` | `11.27` |
| total | 25/25 | **24/25, exit 1** |

What it proves: the "3× in `sigma8`" statement belongs to *this* law (the `n = 1` Langmuir isotherm / saturating
log). A rival interpolation that passes the same galaxy-scale fits gives `sigma8 = 1.92` instead of `2.27` —
still excluded, but the number in the report is law-specific, and K12 is what ties it to the action's `W(u)`.

## M5 — `nocut`: no threshold, the pointwise law applied at every contrast

`dc_star = 0.0` — the modification is never switched off.

| check | unmutated | mutated |
|---|---|---|
| K15 `0.1 < delta_c(0.832) < 1` | `0.677` | **`0.000`** (FAIL) |
| K14 root | `0.677` | degenerate (scan end-point) |
| total | 25/25 | **24/25, exit 1** |

What it proves: the `delta_c(0.832) = 0.677` result is not an artefact of the scan's bracket — it is a genuine
root of a monotone family, and removing the threshold moves the answer to the excluded end (`sigma8 = 3.35` at
`delta_c = 0`). It also documents the distinction from A40's branch (b): the two differ (`3.35` vs `2.27`)
because `RESP ~ delta^{-1/2}` diverges at zero contrast and the 8 h⁻¹ Mpc mode starts from zero.
