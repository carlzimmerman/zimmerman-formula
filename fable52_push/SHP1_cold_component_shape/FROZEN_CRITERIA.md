# SHP1 FROZEN CRITERIA: the shape of the cold component, from raw data (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled (canonical a0
9.3603e-11, alt 1.1312e-10 m/s^2). Committed alone, before any SHP1 script exists or any SHP1 number is seen.

## Question

The owner asked: find the shape of the cold component. Here "cold component" means all gravitating mass around a galaxy
that is not its baryons, whatever it is made of. The lane measures its enclosed mass from raw data in the law's own
variables and asks three things.

1. What is its shape, as a function of radius in units of the law's radius r_M = sqrt(G M_b / a0)?
2. Is it one shape for every galaxy (no separate dependence on M_b at fixed x)?
3. How much separate cold mass, on top of that shape, do the data allow? This is the clearing the data demand.

## Variables (per data point)

- g_bar: the baryons' Newtonian acceleration; g_obs: the observed one.
- x = sqrt(a0 / g_bar). For a point mass x = r / r_M; for an extended galaxy it is the same with the enclosed baryons.
- X_obs = g_obs / g_bar - 1 = M_C(<r) / M_b(<r), the spherical-equivalent enclosed cold mass in units of the enclosed
  baryons.
- Counted-once law (form B), closed form (Part A, Lean): X_L(x) = (sqrt(1 + 4 x^2) - 1) / 2, which is u_in(y)/y - 1
  with y = 1/x^2. Total g = g_law. Residual delta = log10(g_obs / g_law).
- Local shape slope s = d ln X / d ln x (law: 2 inside r_M, 1 outside), so rho_C ~ r^(s-3).

## Data (raw, on disk; nothing downloaded)

- SPARC: `real_research/data/sparc_data/*_rotmod.dat` with `real_research/data/SPARC_Lelli2016c.mrt` (the FLD1 loader).
  Cuts as Lelli+2017's RAR: quality Q = 3 dropped, inclination < 30 deg dropped, points with errV / Vobs > 0.1 dropped,
  g_bar > 0. Upsilon_disk 0.5, Upsilon_bulge 0.7 (0.3 / 0.8 brackets reported).
  g_bar = (Vgas|Vgas| + U_d Vdisk|Vdisk| + U_b Vbul|Vbul|) / R; g_obs = Vobs^2 / R.
  M_b per galaxy = U_d L36 + U_b (bulge share: not in the table, so U_d L36 is used for the whole L36) + 1.33 M_HI.
- KiDS-1000 isolated lenses, Brouwer+2021 (B21), `real_research/data/lensing_rar/brouwer2021_rar/`:
  Fig-4-5-C1 Nobins (with covariance), Fig-9 Massbin-1..4 (with the cross-bin covariance), Fig-4 hotgas Nobins
  (with covariance; the hot-gas bracket). g_obs = 4 G ESD / bias (the record's conversion, as SNP1 loads it); the
  covariance converted the same way (divided by its bias column).
  B21's g_bar axis is used as published (stars plus their cold-gas estimate; hot gas only in the bracket file). B21's
  distances use its fiducial cosmology: a survey calibration, flagged, not changed. Host leakage is not removed
  (KO1's host-free reading is quoted, not redone). Mass-bin representative log M_b 9.4 / 10.45 / 10.7 / 10.9 (SNP1's).

## Rows and lines (per footing)

- **R1 shape on rotation curves.** SPARC points in log10 x bins 0.25 dex wide from -1.25 to 1.5. Every bin with at
  least 20 points must have |median delta| <= 0.10 dex.
- **R2 shape on lensing.** B21 Nobins: chi^2 of (g_obs - g_law) with the full converted covariance; p >= 0.01 reads
  CONSISTENT. If p < 0.01 the sign of the inverse-variance mean residual is reported (ABOVE / BELOW). The hot-gas file
  is the bracket: reported the same way, not graded.
- **R3 one shape.** (a) SPARC: in each R1 bin, the least-squares slope of delta against log10 M_b; the count-weighted
  mean slope must satisfy |slope| <= 0.05 dex per dex. (b) KiDS Fig-9: the four bins' residuals (g_obs/g_law - 1) at
  each common g_bar point, chi^2 about the per-point weighted mean with the full cross-bin covariance; p >= 0.01.
- **R4 room for a separate cold halo (reported, not graded).** Add on top of the law the record's share profile, a
  separate cold mass X_s M_b with rho ~ 1/r^2 inside R_h = Rms("NC", M_b, 0, a_n) (SWT1's radius, as SNP1 places the
  bound share), nucleation z_n = 3 (z_n 6 and 1.5 reported), projected exactly (truncated isothermal ESD), converted
  with B21's 4 G ESD. Fit X_s >= 0 to the four Fig-9 bins jointly with the full covariance. Report the best X_s, its
  2 sigma upper limit (Delta chi^2 = 4), and Delta chi^2 at the record's shares X_s = 5.56 (X = 1) and 59.5 (PD1).
  Both g_bar readings (published, hot gas: the hot-gas file is Nobins only, so it gets one representative mass,
  log M_b 10.45, reported).

## Labels

- Shape: **THE LAW'S SHAPE** if R1 and R2 pass; **THE LAW'S SHAPE ON ROTATION CURVES, LENSING ABOVE / BELOW** if R1
  passes and R2 does not; **NOT THE LAW'S SHAPE** if R1 fails.
- Universality: **ONE SHAPE** if R3a and R3b pass; otherwise **NOT ONE SHAPE** with the failing part named.
- **NO VERDICT** if a known answer fails.
- R4 is reported beside the labels as the data's limit on a separate cold halo.

## Known answers (must pass)

- KA1 synthetic law data: SPARC-like points generated from the law at the real g_bar give |median delta| < 1e-6 in
  every bin and slope < 1e-6; KiDS-like points from the law give chi^2 = 0 and best X_s = 0.
- KA2 the conversion reproduces SNP1's KiDS g_obs (identical arrays) and B21's README v_circ formula on Fig-3 bin 1.
- KA3 the SPARC cut leaves 2693 +- 10 % points (Lelli+2017's count) and 175 files load.
- KA4 X_L(x) equals u_in(1/x^2) x^2 - 1 to 1e-12 on a grid (the Lean identity, numerically).
- KA5 the truncated-isothermal ESD formula matches a direct numerical projection to 1e-4.

## MUTATE (separate outputs, must fail or flag)

- M1 a0 x 2 in the law: R1 must fail.
- M2 synthetic law data plus an injected separate halo X_s = 59.5: R4 must recover X_s > 0 at more than 2 sigma.
- M3 SPARC delta plus 0.2 x (log10 M_b - 10): R3a must fail.

## Part A (Lean, `SHP1.lean`, with a twin of false statements that must fail to compile)

The closed form u_in(y)/y - 1 = (sqrt(1 + 4/y) - 1)/2; X_L <= x, X_L >= x - 1/2, X_L <= x^2, X_L strictly increasing;
dX_L/dx = 2x / sqrt(1 + 4x^2); the density shape 1/(x sqrt(1 + 4x^2)) strictly decreasing (so any density level, such
as rho_DE, is met at one radius only); total g/a0 = (1 + sqrt(1 + 4x^2)) / (2 x^2) satisfies g_N = g^2 / (g + a0).

## Disclosures (numbers seen before this file)

- From the record: KO1 says B21's pooled outer points sit at 1.50 of the law and drop to 0.47 with B21's hot gas;
  PD1 says form B's SPARC rms is 0.0563 / 0.0558; KO1's host-free outer amplitude 1.10 +- 0.15 / 1.00 +- 0.14; ONE1 and
  MK1 as their RESULT files write them. The closed form was derived by hand in this session before this file.
- Hand estimates (before any SHP1 number): R1 passes in every populated bin, the innermost bulge-dominated bin is the
  risk; R2 sits above the law at the outer points (no hot gas), p unknown; R3 passes on SPARC; the four KiDS bins
  agree; R4: the data allow a separate share of order the record's 5.56 M_b and may prefer more without hot gas,
  less with it.

## Operational

One thread, small memory, minutes. `shp1.py` writes `shp1.json` / `shp1.out`; `--mutate` writes `shp1_MUTATE.*`.
Lean via `lake env lean` in the record's build; `compile.txt` with no home paths. Commit with explicit paths; push by
a temporary sparse worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
