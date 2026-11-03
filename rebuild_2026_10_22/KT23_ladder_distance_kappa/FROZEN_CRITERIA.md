# KT23_ladder_distance_kappa — FROZEN CRITERIA (before the script or any number)

Question: what κ do SPARC's outer rotation curves want when no galaxy distance depends on H0? κ is measured against each
footing: κ_meas = 1/2 × a0_meas / a0_footing (both footings are κ = 1/2 by construction; canonical 9.3603e-11 uses the
record's ρ_DE, alt 1.1312e-10 its ρ_total). The raw a0_meas is the footing-free number; κ for any other ρ scales as ρ^-1/2.

κ = 1/2 is FITTED in the record; this lane does not move it. Not theory closed. No download.

**Not blind:** the record has κ = 0.450 +- 0.073 (MNRAS R1, estimator A, Tully-Fisher intercept with H0 = 67.4) and earlier
0.465, 0.530. This lane differs in three frozen ways: no H0 enters any primary distance; the per-galaxy a0 is solved exactly
with the board law's nu, not read from a V^4 intercept; the error budget is priced term by term below.

## Sample (SPARC_Lelli2016c.mrt + rotmod files on disk)
- **Primary:** distance method f_D in {2 TRGB, 3 Cepheid, 5 supernova}. Q <= 2, Inc >= 30 deg, V_flat > 0.
- Flat outer part: the outer 30 percent of points (at least 3) with |d ln V_obs / d ln R| < 0.15 (least-squares slope), and
  R_last > 2 R_disk. Points with V_obs <= 0 or e_V / V_obs >= 0.1 dropped first.
- **Beside, not graded:** primary + f_D 4 (Ursa Major, 18 Mpc); f_D 1 (Hubble flow, tabulated at H0 = 73, flagged as
  H0-dependent: a0 scales as D^-2, so as H0^2).

## Estimator
Board law g_obs = nu(g_bar / a0) g_bar, simple nu. Masses: Upsilon_disk 0.5, Upsilon_bulge 0.7, gas factor 1.33 (the KT19
convention). For each galaxy, a0_i solves sum over its flat outer points of [ln g_obs - ln(nu(g_bar/a0) g_bar)] = 0 (brentq
in ln a0 over 1e-12 to 1e-8). Sample value: ln a0_meas = median of ln a0_i. Also printed: the weighted mean with weights
1 / (per-galaxy MC variance).

## Errors
- **Per galaxy (MC, 400 draws, seed fixed):** distance D ~ N(D, e_D) (rescales R, g_obs, g_bar as SPARC's mass model does:
  V_bar^2 scales as D, R as D), inclination Inc ~ N(Inc, e_Inc) (V_obs scales as sin Inc / sin Inc'), Upsilon_disk
  log-normal 0.1 dex per galaxy. The sample bootstrap (2000 resamples of galaxies, each with one MC draw) gives sigma_stat.
- **Systematic, each shift added in quadrature:** global Upsilon_disk and Upsilon_bulge +-0.1 dex together; gas factor 1.40
  instead of 1.33; ladder zero point +-3 percent on every primary distance. sigma_ln = sqrt(stat^2 + sum sys^2); κ error by
  propagation.
- **Interpolating function:** the standard nu (mu = x / sqrt(1 + x^2)) is run beside and **not** folded into the error. κ
  here is conditional on the board law's simple nu, stated. The depth of the sample (median y_out at canonical a0) is printed
  so the reader can see how far from the deep limit it is.

## Labels, per footing
z_1/2 = (κ_meas - 0.5) / sigma_κ. **1/2 CONSISTENT** if |z| <= 2; **1/2 IN TENSION** if 2 < |z| <= 3; **1/2 EXCLUDED** if
|z| > 3. z for 0.482 (Verlinde's, the record's closest named rival) printed beside. **RESOLVES 1/2 FROM 0.482** only if
|0.5 - 0.482| > 2 sigma_κ.

## Checks
- C1 the solved a0_i reproduces the board law: at a0_i the summed log residual is within 1e-8 of 0, every galaxy.
- C2 injection: replace g_obs by nu(g_bar / a_inj) g_bar with a_inj = 1.0e-10 on the primary sample (no noise); the
  estimator returns a_inj to 1e-6 relative.
- C3 at least 12 galaxies in the primary sample. If fewer, the lane prints NOT EVALUABLE and the labels are not issued.
- MUTATE (`--mutate`, g_obs replaced by g_bar, Newton): no a0 solves; the script must report it and exit 1; outputs to
  `*_MUTATE.*`.
Exit 0 only if C1-C3 pass.

## Limits stated in advance
One nu (simple) graded; the standard nu beside shows the shape dependence. Ladder distances still carry their own zero-point
calibrations. Mass-to-light is the dominant term and isn't measured here, only priced.
