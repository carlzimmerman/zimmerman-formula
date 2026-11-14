# RB2R result (blind re-grade): LOW ROWS COUNT AGAINST B on both footings

**Canonical (a0 = 9.3603e-11): LOW ROWS COUNT AGAINST B.** **Alt (a0 = 1.1312e-10): LOW ROWS COUNT AGAINST B.**
Across footings the part counts against B: four rows read TIDES CANNOT REACH on both footings (DF2, DF4, IC 1613,
NGC 147). The words are the same with and without upper-limit rows (no upper-limit row enters the graded sample).
All four known answers pass. Three of the four frozen twins bite; the frozen twin T3 does not (see below and
`AMENDMENT_A1.md`).

Built blind, with my own code, from the specification. Run: `python3 -I -B rb2r.py` (outputs `rb2r.out`, `rb2r.json`,
`rb2r_MUTATE.out`, `rb2r_MUTATE.json`).

## LOW rows

Delta_iso and s in dex; r_J / r_1/2 at the primary (k = 3), weak (k = 2) and strong edges; "resid + 2s" is B's residual
plus twice its uncertainty at the strong edge. Upsilon_V is the V-band mass-to-light ratio the row would need to stop
being LOW (reported, not graded; the catalogue's masses assume 2).

| row | host | footing | Delta_iso | s | r_J / r_1/2 primary / weak / strong | strong resid + 2s | word | Upsilon_V to stop LOW |
|---|---|---|---|---|---|---|---|---|
| Crater II | MW | canonical | -0.435 | 0.151 | 1.77 / 2.21 / 0.158 | +1.88 | TIDES CAN REACH (needs r_J < r_1/2) | 1.09 |
| Crater II | MW | alt | -0.475 | 0.151 | 1.86 / 2.33 / 0.186 | +1.77 | TIDES CAN REACH (needs r_J < r_1/2) | 0.90 |
| NGC 147 | M31 | canonical | -0.554 | 0.109 | 10.5 / 12.9 / 5.07 | -0.336 | TIDES CANNOT REACH | 0.51 |
| NGC 147 | M31 | alt | -0.585 | 0.108 | 11.0 / 13.5 / 5.30 | -0.370 | TIDES CANNOT REACH | 0.44 |
| Cassiopeia III | M31 | alt only | -0.221 | 0.100 | 6.44 / 7.90 / 3.10 | -0.021 | TIDES CANNOT REACH | 1.82 |
| IC 1613 | field | canonical | -0.537 | 0.113 | no tidal edge | n/a | TIDES CANNOT REACH | 0.51 |
| IC 1613 | field | alt | -0.574 | 0.112 | no tidal edge | n/a | TIDES CANNOT REACH | 0.43 |

Cassiopeia III is not LOW on the canonical footing (Delta + 2s = +0.019); it is LOW on alt by 0.021 dex. It is a
one-footing row and does not enter the across-footings count.

Strong edges: Crater II uses its orbital pericentre (16th percentile 31.7 kpc; median 35.4 kpc). For NGC 147 and
Cassiopeia III, r_J(primary) / 3^(2/3) gives the smaller r_J (projected distances from M31 100.4 and 139.6 kpc). Crater
II's reach needs r_J < r_1/2 (strong r_J = 222 / 261 pc against r_1/2 = 1406 pc): its stars would then sit outside the
tidal radius, so it is not in the equilibrium the estimator assumes. The count stands as frozen.

DF2 and DF4 (central values; projected distances 79.3 and 165.3 kpc at 20 Mpc; k = 3 is primary and strong):

| row | footing | sigma_pred (iso) | E_iso | u | E + 2u | r_J / r_1/2 k = 3 / k = 2 | word | host mass inside d B would need |
|---|---|---|---|---|---|---|---|---|
| DF2 | canonical | 19.98 | -1.710 | 0.541 | -0.627 | 3.48 / 4.28 | TIDES CANNOT REACH | 1.16e13 Msun (16.6 x the law's 7.0e11) |
| DF2 | alt | 20.88 | -1.798 | 0.541 | -0.716 | 3.49 / 4.29 | TIDES CANNOT REACH | 1.35e13 Msun (17.6 x the law's 7.7e11) |
| DF4 | canonical | 18.65 | -2.171 | 0.794 | -0.584 | 8.67 / 10.6 | TIDES CANNOT REACH | 1.40e14 Msun (99 x the law's 1.4e12) |
| DF4 | alt | 19.49 | -2.259 | 0.794 | -0.671 | 8.68 / 10.6 | TIDES CANNOT REACH | 1.62e14 Msun (105 x the law's 1.5e12) |

## Rows with primary r_J inside r_1/2

Only Sagittarius (r_J / r_1/2 = 0.40 canonical, 0.45 alt). It is not LOW (Delta + 2s = +0.057 / +0.017).

## Sample

51 rows graded (12 MW, 26 M31, 13 field) from rows with `vlos_sigma` > 0 and a radius. 49 rows are left out by the
lead's M_V <= -7.7 cut. LMC, SMC and M 32 are excluded by name. Every upper-limit row in the files has `vlos_sigma`
empty and M_V fainter than -7.7, so none is graded. Andromeda XVIII has no `distance_host`; it uses `distance_m31`
(427 kpc), as the spec's fallback says. Antlia B (field file, catalogue host NGC 3109) gets no tidal edge, as the spec
says for the field file; it is not LOW either way.

## Known answers and twins

- KA1: r_J = 1e12 pc returns g_iso exactly; r_J = 1e-6 pc returns Newton (relative difference 0 at double precision). Pass.
- KA2: Newtonian point mass, r_J against d (m / 3M)^(1/3): 2e-15 (scalar root) and 5e-15 (vector bisection). Pass.
- KA3: deep limit g_iso / sqrt(g_N a0) - 1 = 1.6e-7 at g_N / a0 = 1e-13. Pass.
- KA4: leapfrog pericentre equals the analytic one for every MW row with proper motions (12 rows; agreement better than
  0.01 %), energy drift below 2e-7; no draw needed the analytic fallback. Pass.
- T1 (stars exactly on Newton, 5 % errors) reads LOW (Delta -1.40 / -1.44). Bites.
- T2 (exactly on the canonical law) does not read LOW (Delta 0.00 canonical, -0.04 alt). Bites.
- T3 as frozen (T1 at 20 kpc from the Milky Way, R_h = 500 pc) reads TIDES CANNOT REACH on both footings: **does not
  bite.** Its primary r_J is 0.68 / 0.74 of r_1/2, not "well inside" as the spec's twin requires, and the phantom mass
  kept inside even the strong-edge r_J (0.33 r_1/2) leaves B 0.14 / 0.24 dex short of reach.
- T4 (T1 in the field) reads TIDES CANNOT REACH. Bites.
- Amendment A1 (written after T3 failed, committed alone before it ran): T3b, the same Newton-placed dwarf with R_h =
  2000 pc at 20 kpc, has r_J / r_1/2 = 0.006 / 0.008 and reads TIDES CAN REACH (strong resid + 2s = +0.31); T4b in the
  field reads TIDES CANNOT REACH. Both bite. Lesson: for a deep-regime dwarf B reaches Newton only when r_J is a small
  fraction of r_1/2, because the law's phantom mass inside r_J is many times the baryons there. Crater II shows the
  pipeline does return CAN REACH on real data.

## Sensitivities (not graded; `rb2r_MUTATE.*`)

- Major-axis radius (`rhalf_physical`) instead of the circularised one: every LOW row stays LOW with the same word.
- pmra read without the cos(dec) factor: Crater II's 16th-percentile pericentre 32.5 kpc; still TIDES CAN REACH.
- M31 distance from the "-" root (701.6 kpc instead of 776.3 kpc): NGC 147 and Cassiopeia III keep their words.
- Seeds: changing a twin's key (and so its seed) moved T1's Delta by 0.001 dex.

## Hand estimate against result

Estimated (frozen): DF2 and DF4 LOW on both footings 0.9, both CANNOT REACH 0.85 (result: yes); a bright field dwarf
LOW 0.6 (result: IC 1613); 0 to 3 LOW MW / M31 satellites, mostly reachable only with r_J < r_1/2, 0.6 (result: three,
but only Crater II is reachable; NGC 147 and, on alt, Cassiopeia III are not); word LOW ROWS COUNT AGAINST B on both
footings 0.85 (result: yes). The estimate missed NGC 147.

## What looked wrong or fragile

- Split-normal draws of sigma go below zero for rows with large lower errors (Perseus I 320 of 2000 draws, Andromeda
  XVII 138, a few others); they are set to 1e-3 of the central value as frozen, which inflates sd (2.30 and 1.65 dex).
  None of these rows is near LOW, so no word depends on it.
- The spec puts M*/2 inside r_1/2 while a Plummer of a = R_h holds 0.512 M* there; I normalised the profile to M*/2 at
  r_1/2 (frozen choice C4).
- IC 1613 (and the other gas-rich field dwarfs) rotate and carry gas; the Wolf estimator on sigma alone, with no gas
  term, is not a full mass budget. Adding gas would raise g_pred and push IC 1613 further low.
- The weak edge (k = 2) gives a larger r_J than the primary, as it should; it never changes a word.

## What this lane does not cover

Spherical, isotropic equilibrium; the Wolf estimator at r_1/2; mass follows light (Plummer); no gas term; an
instantaneous tidal cut at r_J with no time evolution or orbit history beyond the pericentre; host masses by convention
(flat V_c 200 / 230 km/s, and the law's mass of a 1e11 Msun point for NGC 1052); no orbits for M31 satellites; the
lead's M_V cut leaves out every faint system; the 0.15 dex mass-to-light prior and the factor-2 rule are the earlier
lane's. This lane is blind to the earlier lane's numbers and words; it does not compare with them.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
