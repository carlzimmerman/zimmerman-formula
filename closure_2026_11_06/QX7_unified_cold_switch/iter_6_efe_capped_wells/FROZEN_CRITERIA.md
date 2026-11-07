# QX7 iter_6 frozen criteria (door A): iter_5's host-held dust, with the external field capping every host's well

Frozen before any iter_6 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane under SWARM_BRIEF.md.
Mutation of iter_5 (criteria 2afe6bac03, result 931e60027b).

## Why

iter_5 failed because, under the isolated a0 law, a galaxy's pull falls only as 1/r. The well is then logarithmically deep,
and the host squeezes its captured dust well inside r_ta (KiDS shift -0.10 to -0.27 at lambda_0 <= 8.25). The action's field
equation is nonlinear, so a uniform external field caps that tail (the EFE). Beyond r_e, where the internal field drops below
the external one, the pull falls as 1/r^2 again. iter_5 left this out. It adds no constant: the external field is measured.

## Mechanism (frozen; everything else = iter_5)

- The field felt by baryons AND dust, in every host and in the prediction formula, is the 1D algebraic EFE form of the law:
      g_tot = g_law(g_N + g_Ne) - g_law(g_Ne),   g_N = G (M_b(<r) + M_d(<r)) / r^2,
  where g_law is the same function, per footing, as iter_4/iter_5. This is the direction-averaged approximant of the action's
  EFE (Famaey-McGaugh form), stated as an approximation; the full 3D solve is not done.
- The external field comes from the record's own estimator, gext_vectors_2026 (2MPP baryons + MCXC, framework-native, no LCDM):
  e_N = g_Ne / (1.2e-10 m s^-2) over the 175 SPARC rows.
  - **PRIMARY:** the median of log_eN_maxclu, e_N = 0.0033, so g_Ne = 3.96e-13 m s^-2. This applies to every host (KiDS
    isolated lenses, SPARC G5 systems, ellipticals, groups, X-COP).
  - **Reported bracket:** the noclu median 0.0004; the maxclu 84th percentile 0.0052; and a ceiling of x8 (missing baryons),
    0.026. These are reported only and do not enter the label.
- Every gate's baseline (M_d = 0) is recomputed with the same EFE, so each G6/G7 shift is dust-only and self-consistent. The
  law+EFE baseline's own absolute misfit to KiDS and X-COP is reported as a clue, not graded here.
- The dust equation, retention rule (r_s < r_ta), f_cap, R, host profiles, carried growth/forest cells, gates G5-G7, and the
  X-COP/groups PASS line are all identical to iter_5.

## Label

PASS / FAIL (clusters) / FAIL (no window) exactly as iter_5, at the PRIMARY e_N. Both footings, never pooled.

## Controls

- K1: with g_Ne = 0, every iter_5 number is reproduced (lensing shift at lambda_0 2.154 to 1e-6; X-COP at 2.154 to 1e-4).
- K2: the EFE form tends to g_law(g_N) as g_Ne -> 0, and to (g_law'(g_Ne)) g_N (Newtonian-like, boosted G) for g_N << g_Ne.
  Checked numerically on one host to 1e-3.
- MUTATE A: e_N x 100 (0.33) must change the KiDS lensing shift by more than 0.05 at lambda_0 2.154 (the cap has power).
- MUTATE B: lambda_0 1e-3 must fail G5 or G6 (bite, as iter_5).
- MUTATE C: f_cap 0 reproduces the law+EFE baseline exactly (zero shift).

## Amendment A1 (2026-11-07, before any iter_6 number): what separates this from killed iterations

- **QX10 iter_2** (criteria c1f0cadb7a / A1 168db297bd) KILLED iter_4's window on KiDS lensing. It put the n = 1 fluid in the
  host's own potential with the ISOLATED a0 law (G6 -0.15 to -0.27 in cells C1-C4).
- **QX7 iter_5** (931e60027b) is an independent reproduction of that kill on the full lambda_0 grid. It agrees: -0.27 at 1.47,
  -0.25 at 2.15, -0.15 / -0.10 at 8.25.
- **The new input here is the measured external field** (gext_vectors_2026, e_N 0.0033) acting on every host through the
  action's EFE. QX10 and iter_5 both assume isolated hosts.
- A FAIL here is therefore a new label: "the measured EFE does not unbind the halo". It is not a replay.
