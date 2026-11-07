# SV5: the growth / CMB-lensing constraint, mapped, and three escape classes. FROZEN CRITERIA (lane level)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules: ../SWARM_BRIEF.md (binding). TEST lane: any sector here is
COLD DARK ENERGY carried by the action's own fields (khronon tau, covector P, clock phi); no particle. No LCDM input: the
background is the record's framework-native one (QX3 iter2 worst corner, flat constant rho_DE, brackets only, no Planck
values); data are raw PR4 lensing bandpowers (cfg917_lib), the KiDS isolated-lens RAR, SPARC, the QX5 elliptical set. Both
footings, never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.

This file, iter_1_law_on_web/FROZEN_CRITERIA.md, iter_2_charge_switched_sound_speed/FROZEN_CRITERIA.md and
iter_3_a0z_tied_coupling/FROZEN_CRITERIA.md are committed together and alone, before any script or number.
QX31 (data-product assumptions) is read, not redone: its result (no failure is an artefact) is taken as given.

## Reused machinery (read only, executed from source as QX7 iter_4 / QX10 do)

- QX3 iter3 (`iter3.py` up to "# K: beta = 0"): CLASS model at the worst corner, the growth ODE, `I2.limber_ratio`,
  `I2.best_amp_chi2`, X0 / c0 (dust reference), DCHI2_LINE = 4.
- QX7 iter_3 generalised solver `g2gen(kJ)` (any physical Jeans wavenumber kJ(a) in Mpc^-1), exactly as QX7 iter_4 loads it.
- QX10 iter_2 `qx10_i2.py` (n = 1 end state in the host's own potential, a0 law on; G5 / G6 / G7 and their lines), imported
  with no --mutate flag.

## T0: the target function (a map, computed from the record's machinery; no gate is graded in T0)

- **T0.1 required source.** R_req(k, z) = delta_m[dust reference] / delta_m[sector smooth] from `solve_gen` (smooth = kJ -> 0,
  implemented as kJ = 1e-8 Mpc^-1), on the solver's k grid at z = 0.5, 1, 2, 5, 10. Also S_smooth(L) (Limber ratio of the
  smooth sector to the dust reference) and the PR4 shape Delta chi^2 of the smooth sector. Amplitude omega_d range: QX3 iter2
  G1 fits (read from iter2.json).
- **T0.2 tolerated late stiffening.** Step histories lambda_J(z) = lambda_s (physical) for z < z_s, dust above, on the declared
  diagnostic grid lambda_s in {1, 3, 10, 30, 100, 1000} Mpc, z_s in {0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3}: Delta chi^2 from
  `g2gen`. Reported as z_s,max(lambda_s) = the largest grid z_s with Delta chi^2 <= 4. A map, not a candidate.
- **T0.3 host requirement.** lambda_host,f = the smallest lambda_J on geomspace(1, 1000, 31) Mpc at which QX10's n = 1 end state
  passes G5 (M_d(<R_opt)/M_b <= 0.3), G6 (|KiDS shift| <= 0.05) and G7 (|elliptical shift| <= 0.15), footing f; lambda_host =
  max over footings. If no grid value passes, lambda_host = NOT FOUND.
- **T0.4 PR4 amplitude error.** sigma_A,rel = 1/(A sqrt(b)) for the X0 amplitude fit (b = u^T C^-1 u, the CMB-marginalised PR4
  covariance in cfg917_lib). Used by iter_1 and iter_2 lines.

## Labels

PASS / FAIL / NO-GO FOR CLASS / NOT EVALUABLE per iteration, per footing where a0 enters (growth at linear order is
footing-independent: QX3 A-web). A class label "NO-GO FOR CLASS" needs (i) the most generous member failing a gate, and
(ii) a stated argument (Lean where algebraic) that every member is at least as bad on that gate. Otherwise FAIL.

## Lean

`fable_independent_2026/lean_2026/SV5_growth_nogo.lean` (0 sorry, standard axioms, .out saved) with a
`SV5_growth_nogo_MUTATE.lean` twin whose declared false claims must fail. Planned theorems: Cauchy-Schwarz power bound
(iter_1), nu antitone (iter_1), monotone-switch ordering (iter_2), time-only coincidence + IVT crossing (iter_3),
deep-MOND point-mass phantom density (iter_2).

## Compute

nice -n 15, OMP/BLAS threads 1, outputs small JSON/.out only (no field dumps). Load average > 40: wait.
