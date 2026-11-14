# RB1R result (blind re-grade): form B amount in the X-COP clusters

## Word per footing

- **canonical (a0 = 9.3603e-11): AMOUNT CONSISTENT ON BOTH SIDES.** Median f_ret 1.095, 95 % interval [0.885, 1.259], 7 clusters.
- **alt (a0 = 1.1312e-10): AMOUNT CONSISTENT ON BOTH SIDES.** Identical numbers (no a0 enters this class; KA-6 checks this).

The lower end (0.885) is not above 1, so the ceiling is not broken. The upper end (1.259) is not below 0.85, so the floor
holds. The interval is wide: it spans both lines' margins, so the class neither breaks nor confirms the ceiling. Three of the
seven clusters (A2142, A2319, A644) sit above 1 at more than 2 sigma on their own. This is a blind re-grade; it does not
say the data favour the framework.

## Graded class C-X (7 clusters with stellar files, last kept gas-grid radius, M_FORW, R = 5.41)

| cluster | r (kpc) | r / R500 | M_dyn (Msun) | M_gas | M_star | f_ret | err |
|---|---|---|---|---|---|---|---|
| A1795 | 1702.4 | 1.477 | 6.866e14 | 9.099e13 | 5.53e12 | 0.885 | 0.131 |
| A2029 | 2212.7 | 1.565 | 1.380e15 | 1.882e14 | 1.50e13 | 0.934 | 0.148 |
| A2142 | 2352.9 | 1.652 | 1.374e15 | 2.397e14 | 1.56e13 | 1.235 | 0.118 |
| A2319 | 1344.3 | 0.983 | 7.885e14 | 1.419e14 | 6.92e12 | 1.259 | 0.076 |
| A644 | 1843.8 | 1.475 | 4.043e14 | 1.097e14 | 7.79e12 | 2.216 | 0.381 |
| A85 | 1483.7 | 1.201 | 6.418e14 | 1.049e14 | 3.13e12 | 1.095 | 0.057 |
| ZW1215 | 2052.9 | 1.512 | 1.380e15 | 1.143e14 | 4.84e12 | 0.511 | 0.108 |

Errors: half the 16 to 84 percentile width over 4,000 lognormal draws of the three masses. A85 was re-computed by hand from
the raw columns (1.0953, same).

## Brackets (reported, not graded; identical on both footings)

| bracket | n | median | 95 % interval | above 1 at >2 sigma | word (reported) |
|---|---|---|---|---|---|
| R = 5.562 | 7 | 1.126 | [0.910, 1.294] | 4 | AMOUNT CONSISTENT ON BOTH SIDES |
| at R500 (Ettori 2019 JSON) | 7 | 1.057 | [1.046, 1.072] | 1 | AMOUNT BREAKS THE CEILING |
| all 12, 5 with imputed stars | 12 | 0.938 | [0.904, 1.165] | 3 | AMOUNT CONSISTENT ON BOTH SIDES |
| h 0.7 to 0.65, f_gas ~ h^-1/2 (as specified) | 7 | 1.144 | [0.922, 1.315] | 4 | AMOUNT CONSISTENT ON BOTH SIDES |
| EXTRA: h 0.7 to 0.65, gas h^-3/2, stars h^-1 | 7 | 1.252 | [1.006, 1.443] | 4 | AMOUNT BREAKS THE CEILING |
| hydrostatic bias b = 0.1 | 7 | 0.966 | [0.784, 1.107] | 1 | AMOUNT CONSISTENT ON BOTH SIDES |
| hydrostatic bias b = 0.2 | 7 | 0.842 | [0.686, 0.962] | 1 | AMOUNT CONSISTENT ON BOTH SIDES |
| mass M_NFW | 7 | 1.031 | [0.932, 1.174] | 2 | AMOUNT CONSISTENT ON BOTH SIDES |
| mass M_EIN | 7 | 1.049 | [0.923, 1.387] | 3 | AMOUNT CONSISTENT ON BOTH SIDES |
| mass M_ISO | 7 | 1.418 | [1.217, 1.443] | 6 | AMOUNT BREAKS THE CEILING |
| mass M_BUR | 7 | 1.331 | [1.070, 1.431] | 5 | AMOUNT BREAKS THE CEILING |

At R500 six of seven clusters sit at 1.05 to 1.07 (ZW1215 at 0.68, A2319 at 1.26), so the bootstrap interval of the median is
very narrow and sits just above 1. At R500 the ceiling is broken by about 5 %, which is the size of the R = 5.41 versus
5.562 difference and of a few per cent hydrostatic bias (b = 0.1 alone takes it under 1).

The other mass columns in the hydro-mass files (header gives only names and Msun units; comment: "Hydrostatic mass profiles
for various mass models"; a PARAMS extension lists NFW, ISO, HER model fits): M_NFW (NFW fit), M_EIN (Einasto, by name),
M_ISO (isothermal, by name), M_BUR (Burkert, by name). M_FORW is the forward (non-parametric) estimate. There is an EM_HER
error column with no M_HER mass column, so the Hernquist estimate could not be run. The fgas file also holds an M_NFW with
LO/HI; I did not use it (the hydro-mass file's M_NFW is the bracket).

## Units found

Hydro-mass ext 1: RADIUS kpc, masses and errors Msun (EM_* read as 1-sigma). Gas ext 1: RADIUS R/R500 (header R500 equals
the hydro-mass header R500 in all 12), MGAS Msun; MGAS_LO and MGAS_HI are offsets (both far below MGAS), so sigma = (LO + HI) / 2.
Stars ext 2 (MSTAR_SMOOTHED): RADIUS kpc (not R/R500; ext 1 is in R/R500), MSTAR M_sun, MSTAR_LO and MSTAR_HI are bounds
(header: total uncertainties), so sigma = (HI - LO) / 2. All the hydro-mass grids run 30 to 3000 kpc; the last radius is set
by the gas grid or by the end of the stellar profile.

## Known answers and mutations

- KA-4: max |f_ret - 1| = 0 for both R values. Passes.
- KA-5: 12 folders, 7 with a stellar file; JSON has 13 entries, HydraA without a folder. Passes.
- KA-6: the two footings give identical graded numbers. Passes.
- M1 (R x 2): median 2.191, [1.770, 2.518], lower end above 1. Bites, so the ceiling is evaluable.
- M2a (M_dyn x 0.5): median rises to 2.747. M2b (stars zero): median falls to 1.057. Both move the right way.
- P07 (planted at 0.7, through the whole pipeline): 0.697 [0.694, 0.722], reads AMOUNT BELOW THE FLOOR, as wanted.
- P13 (planted at 1.3): 1.295 [1.199, 1.321], reads AMOUNT BREAKS THE CEILING, as wanted.

## Hand estimate against result

I guessed a median near 0.88 with interval about [0.78, 1.0], and gave CONSISTENT ON BOTH SIDES 0.60, BELOW THE FLOOR 0.30,
BREAKS THE CEILING 0.07. The word matches my most likely outcome, but the median (1.095) came out higher than I guessed: the
last radii reach 1.0 to 1.65 R500, further out than I expected, and the gas fraction there is higher. My guess that b = 0.2
would read below the floor was wrong (upper end 0.962).

## Things that looked wrong or fragile

- **A644's M_FORW falls with radius** beyond about 1.1 Mpc (22 decreasing steps; 4.95e14 at 0.98 Mpc, 4.04e14 at its last
  radius 1.84 Mpc). An enclosed mass cannot fall. This drives its f_ret of 2.2. Post hoc only (not graded): dropping A644
  gives median 1.015, [0.698, 1.247], the same word.
- R500 differs between the hydro-mass header and the Ettori JSON for A2029 (1414 vs 1423 kpc), A2319 (1368 vs 1346) and A644
  (1250 vs 1230). I used the header R500 for the gas grid and the JSON R500 for the R500 bracket, as specified.
- The specification's h scaling (f_gas ~ h^-1/2) differs from the usual X-ray scaling (f_gas ~ h^-3/2). I ran it as written
  and added the usual scaling as a marked extra; with it the class reads over the ceiling. The footing h values were not
  looked up (h = 0.65 for both, as the specification allows), so the h bracket does not separate the footings.
- With 7 systems the bootstrap median moves between order statistics, so the interval end points are cluster values.

## What this lane does not cover

It uses the same public X-COP profiles and the same hydrostatic assumption as any other build, so it cannot catch an error
shared with them. Non-thermal pressure is covered only by the two fixed bias brackets. Gas and stars outside the tabulated
ranges, and the infall history (the edge relation compares to observed baryons only), are not tested. The imputed stars of
the all-12 bracket use the median star-to-gas ratio of the 7, held only over r / R500 = 0.023 to 1.425 (no extrapolation).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
