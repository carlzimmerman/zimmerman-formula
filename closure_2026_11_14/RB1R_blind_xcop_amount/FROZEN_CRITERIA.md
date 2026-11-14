# RB1R frozen criteria: the amount of cold dark energy in the X-COP clusters under form B (blind re-grade)

Frozen 2026-11-14, before any script of this lane exists, before any data file was opened (not even a header) and before
any number of the lane was computed. What I had seen is in `WHAT_I_SAW_AT_START.md`.

## 1. Question

Under form B a group or cluster holds R times the baryons that fell into it as cold dark energy (collisionless, so it stays
when gas leaves). Gravity is Newtonian with the total mass; no a0 enters; no external field. Then
M_dyn(<r) = M_b,obs(<r) + M_cold(<r), and the retained fraction

    f_ret(<r) = R M_b,obs(<r) / [M_dyn(<r) - M_b,obs(<r)]

can never exceed 1 at the edge. If M_dyn <= M_b,obs the system counts as f_ret = +infinity. R = 5.41 (graded);
R = 5.562 (bracket, reported).

Question: for the X-COP clusters with measured stellar profiles, is the class median of f_ret at the outermost common
radius at or below 1 (ceiling) and at or above 0.85 (floor), with 95 % bootstrap intervals?

## 2. Case (graded class C-X)

The X-COP clusters that have a stellar-mass file (expected 7). At each cluster's outermost radius on the gas-profile grid
where the hydrostatic mass M_FORW, the gas mass and the stellar mass can all be interpolated (no extrapolation).
Baryons = measured gas + measured stars. Both footings are run (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2); this
class contains no a0, so the numbers must be identical. If they are not, that is a bug and the lane reports NO VERDICT.

## 3. Data handling (my choices where the specification is silent)

- Data folder: `real_research/data/xcop/` relative to the repository root, found from the script's location.
- Parser: one folder per cluster; `<name>_hydro_mass.fits` ext 1, `<name>_fgas_profile.fits` ext 1, `<name>_mstar.fits`
  ext 2. I will print every header keyword that sets units or R500, and every column name, unit and first row, and state
  the units in the result. If a unit is not stated I take the one the specification names (gas RADIUS in units of the
  hydro-mass header R500) and say so. Any unit I cannot pin down is reported as an open item.
- Masses are converted to Msun; radii to kpc and to r / R500 (R500 from the hydro-mass header for the gas grid, as the
  specification says).
- Interpolation: log M against log r, linear (numpy interp in log-log), only inside each table's radius span (inclusive of
  end points). Rows with non-positive or non-finite mass or radius are dropped before interpolation. A gas-grid radius is
  kept only if all three masses can be interpolated there. The last radius is the largest kept gas-grid radius.
- Mass errors: for M_FORW, the error column whose name the header gives (expected EM_FORW, read as 1-sigma absolute in the
  same unit). For gas and stars, sigma = (HI - LO) / 2 if LO and HI are bounds (LO <= value <= HI); if they are not
  bounds (for example offsets), I will state what I found and use the half width of the band they describe. Errors are interpolated in log-log the same way (as fractional errors, linearly in
  log r).
- Per-system errors (only for the count of systems individually above 1 at > 2 sigma, and the printed f_ret error):
  4,000 draws; each of M_dyn, M_gas, M_star drawn independently lognormal with median = the value and sigma_ln = the
  fractional 1-sigma error. A system is "above 1 at > 2 sigma" if its 2.275th percentile of f_ret over the draws is above 1
  (draws with M_dyn <= M_b count as +infinity). The printed f_ret error is half the 16 to 84 percentile width.
- Class statistic: the median of f_ret over the systems (with +infinity allowed; the median uses ordinary ordering), 95 %
  interval = 2.5th and 97.5th percentiles of the median over 10,000 bootstrap resamples of the systems (with replacement,
  same size). For an even number of systems the median is the mean of the two middle values (inf if either is inf).
- Seed: numpy default_rng(20261114) for the bootstrap; default_rng(20261115) for the per-system draws; planted classes
  use default_rng(20261116).

## 4. Lines (the earlier lane's, verbatim in substance)

- Ceiling (one-sided): FAILS if the lower end of the 95 % interval is above 1; otherwise CONSISTENT. Fewer than 5 systems:
  NOT EVALUABLE.
- Floor: FAILS if the upper end of the 95 % interval is below 0.85.
- Ceiling NOT EVALUABLE if M1 (R x 2) does not flip the class to FAILS (ceiling).

The word per footing (section 5 of the specification):
- AMOUNT CONSISTENT ON BOTH SIDES: lower end <= 1 and upper end >= 0.85;
- AMOUNT BREAKS THE CEILING: lower end > 1;
- AMOUNT BELOW THE FLOOR: upper end < 0.85;
- NO VERDICT if a known answer fails or M1 does not bite. NOT EVALUABLE if fewer than 5 systems.
The same word is reported (not graded) for every bracket below.

## 5. Brackets (reported, not graded)

1. R = 5.562.
2. At R500 instead of the last radius, R500 taken from `xcop_r500_ettori2019.json` (converted Mpc to kpc). A cluster whose
   R500 lies outside its kept range drops from that bracket; the count is reported.
3. All 12 clusters: the 5 without a stellar file get stars imputed as M_star = q(x) M_gas, where x = r / R500 and q(x) is the
   median, over the 7, of M_star/M_gas evaluated on a common log grid of x (60 points spanning the union of the 7 kept
   ranges), using at each grid point only the clusters whose kept range covers it and only grid points covered by at least
   3 of the 7. q is interpolated log-log in x with no extrapolation: an imputed cluster keeps only gas-grid radii inside the
   span of q (and inside its hydro and gas spans). Imputed stars carry the median fractional star error of the 7.
4. h rescaled from 0.7 to the footing h. I will not search the repository for the footing values (a search risks forbidden
   files), so I use h = 0.65 for both footings, as the specification permits, and say so. As the specification states it,
   f_gas scales as h^-1/2: M_gas -> M_gas (0.7/0.65)^(1/2) at fixed M_dyn; stars unchanged. Note at freeze: the usual X-ray
   scaling is f_gas proportional to h^-3/2 (M_gas ~ h^-5/2, M_HSE ~ h^-1) and stellar fraction ~ h^-1. I run the
   specification's h^-1/2 as the bracket and additionally report a second, clearly marked extra with gas h^-3/2 and stars
   h^-1 (stars ~ L ~ h^-2 over M_HSE ~ h^-1).
5. Hydrostatic bias b = 0.1 and 0.2: M_dyn -> M_dyn / (1 - b).
6. Every other hydrostatic mass estimate tabulated in the hydro-mass files (every mass column other than M_FORW, with its
   error column if one exists), named and described from the header, run through the same last-radius statistic.

## 6. Known answers and mutations

- KA-4: synthetic system with M_dyn = (1 + R) M_b gives f_ret = 1 to 1e-12 (both R values).
- KA-5 (parser): 12 cluster folders found, 7 with a stellar file. The JSON lists 13 clusters (one with no folder).
- KA-6 (mine): the two footings give byte-identical class numbers.
- M1: R x 2 must push the class's lower end above 1 (ceiling FAILS). If it does not, the ceiling is NOT EVALUABLE and the
  word is NO VERDICT.
- P07 (mine): a planted class of 7 systems with f_ret = 0.7 x lognormal scatter of 5 % (built as M_b, M_dyn = M_b (1 + R / f)),
  run through the same median and bootstrap code, must read AMOUNT BELOW THE FLOOR.
- P13 (mine): same at 1.3, must read AMOUNT BREAKS THE CEILING.
- M2 (mine, reported): M_dyn x 0.5 must raise f_ret (direction check); stars set to zero must lower f_ret.
Mutation runs write to `rb1r_MUTATE.out` and `rb1r_MUTATE.json`.

## 7. Hand estimate (before any data was opened)

From what I know of massive X-ray clusters: gas fraction near R500 about 0.12 to 0.15 (h = 0.7), stars about 0.01 to 0.02,
so f_b about 0.13 to 0.16. With R = 5.41, f_ret = R f_b / (1 - f_b) is about 0.80 to 1.03. The stellar files likely stop
near or inside R500, where f_gas is lower, which pulls f_ret down. My guess for the class median at the last radius:
about 0.88, interval about 0.78 to 1.0.

Probabilities (graded class, each footing, identical):
- AMOUNT CONSISTENT ON BOTH SIDES: 0.60
- AMOUNT BELOW THE FLOOR: 0.30
- AMOUNT BREAKS THE CEILING: 0.07
- NO VERDICT / NOT EVALUABLE: 0.03
M1 bites: 0.95. Brackets: b = 0.2 lowers f_ret by about 20 % and probably reads below the floor.

## 8. What this lane does not cover

It uses the same public X-COP profiles and the same hydrostatic assumption as any other build; it cannot test the
non-thermal pressure beyond the two fixed bias brackets, nor stars or gas outside the tabulated ranges, nor the infall
history (it compares to observed baryons, which is the lower bound the form B edge relation allows).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
