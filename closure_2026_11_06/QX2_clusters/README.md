# QX2: clusters from the action on the table: FAIL (no-go over every static term of v3s / AC2q)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. No LCDM inputs.
Criteria: FROZEN_CRITERIA.md and iter_1..iter_5/FROZEN_CRITERIA.md (2f84fed672), committed alone before any code.
Script: qx2.py (one thread, about a minute). Outputs: qx2.out / qx2.json, MUTATE in qx2_MUTATE.out / .json.
Lean: fable_independent_2026/lean_2026/QX2_cluster_nogo.lean and its _MUTATE twin.

## The question

v3s and AC2q have one static, spherical field equation:

    div[ mu(|grad psi|/a0) grad psi ] + mu_K^2 psi + (stiffness, scale Lstar) = 4 pi G (rho_b + rho_s)

Matter couples minimally. So inside a cluster any extra mass has to come from one of four terms: the law's
phantom (a function of g only), the K(Q) dust mu_K^2 psi, the switched stiffness, or AC2q's clock source rho_s.
QX2 grades each term on X-COP's hydrostatic masses (7 clusters, 35 points at 0.1-0.7 R500; HO1's line,
|mean Delta| <= 0.05 and rms <= 0.10, Delta = log10(M_HSE/M_model)). Every bound is taken on the generous side.

## Results (canonical / alt; never pooled)

| Iter | Term | mean Delta | rms | Label |
|---|---|---|---|---|
| 1 | plain law (reproduces LW1, \|d\| = 0) | +0.468 / +0.435 | 0.476 / 0.444 | FAIL |
| 2 | any single-valued nu (J(Y) in the AQUAL class); SPARC's own binned nu | +0.430 / +0.431 | 0.440 / 0.440 | FAIL, class DEAD |
| 3 | AC2q clock source, active density <= 4 rho_DE (rho_DE = a0^2/(kappa^2 c^2 G)) | +0.466 / +0.432 | 0.475 / 0.442 | FAIL |
| 4 | switched stiffness, Lstar 90 pc, k = 10/r | +0.468 / +0.435 | 0.476 / 0.444 | FAIL |
| 5 | K(Q) dust at mu_K = 0.1 Mpc^-1 (galaxy-lensing bound), HSE potential, no back-reaction | +0.464 / +0.432 | 0.474 / 0.442 | FAIL |

The statistical standard error on the mean is 0.004 dex, so every miss is about 100 sigma. Non-thermal pressure
(<= 0.03 dex) cannot carry it.

- **Iteration 2 kills the whole interpolation class.** X-COP's points sit at y = g_N/a0 of about 0.08-0.25,
  well inside SPARC's measured range (0.014-14). In every shared bin, X-COP needs 0.30-0.51 dex more boost than
  SPARC galaxies show at the same y (5 bins, both footings). No single-valued nu, and so no choice of J(Y), can
  serve both. Lean `universal_nu_record`: the miss is >= 0.246 dex even when nu is allowed SPARC's full 0.054 scatter.
- **Iteration 3:** the clock adds at most 2-3 % of the baryon mass at 0.7 R500 (M_s/M_b <= 0.022 / 0.032). The
  gamma s^2 terms are 4e-17.
- **Iteration 4:** the stiffness changes the phantom by at most 5e-5 relative. Its sign is a penalty, which only
  lowers the positive charge.
- **Iteration 5:** to bring the mean to zero, the K(Q) dust needs mu_K = 1.78 / 1.74 Mpc^-1, which is 17-18 times
  the bound that isolated-galaxy lensing allows. Even there the rms is 0.28 / 0.27, so the shape fails too. This
  matches S4's wrong ordering (galaxies are hit before clusters; Lean `onset_exponent`).

## Known answers and controls

- K-LW1: iteration 1 equals LW1's committed X-COP numbers to 0 (both footings).
- MUTATE (separate outputs), all bite:
  - a0 x 1.5 moves the mean by -0.071 / -0.073.
  - nu_SPARC x 3 brings the mean to -0.047 (the excess vanishes, so the class test sees a fix when one is planted).
  - rho_DE x 1e4 moves the mean to -0.80 / -0.95.
  - Lstar x 1e4 moves it to -2.08 / -2.18.
  - mu_K = 10 Mpc^-1 moves it to -1.29.
- Lean (QX2_cluster_nogo.lean): `law_mono` (sources can only add, so the generous bounds are upper bounds),
  `universal_nu_gap` / `universal_nu_record`, `stiffness_shift` (log(1+e) <= e), `sum_le_of_pointwise` (a deeper
  potential gives more dust, so the HSE potential is generous), `dust_mono_mu`, and `door_fail`. The MUTATE twin
  states three false versions, and all must fail to compile.

## Door label

**Clusters: FAIL for the action on the table.** The static sector of v3s / AC2q cannot supply X-COP's mass. All
four static terms are graded and each falls short by a factor of about 2.7-2.9 in mass. No J(Y) can fix it,
because SPARC pins nu at the same y. This closes the cluster door for these actions. Passing would need a new
action: a non-minimal matter coupling, or a source that depends on something other than (g, psi, Lstar, s^2).
The record's selector searches (X17, X21, X22 in V3S_FINAL_VERDICT) found no such variable that keeps hosted
dwarfs and growth, so none is proposed here.

## Limits

Statics and spherical symmetry only, hydrostatic masses, 7 clusters. Groups and lensing were not run, because
the frozen rule stops at G-X. Non-static effects (mergers, caustics, the moving-halo Bernoulli term) are of order
v^2/c^2 ~ 1e-5 in the source and were not graded.
