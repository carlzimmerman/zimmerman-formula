# UX4_dwarf_failures: the satellite failures stand; no computed, non-fitted effect closes them, and the field dwarfs passing doesn't point at the environment. IC 1613 stays failed at its measured inclination, and is the one case with a data route

Criteria: `FROZEN_CRITERIA.md` (3ae0afdee2, committed alone, before any script or number). Not blind; prior reads are listed there. Script `ux4.py`; numbers in `ux4.out`, `ux4_results.json`. kappa = 1/2 FITTED. Footings never pooled. The cold sector stays retired and this reinstates nothing. Not theory closed.

## Verdict
**Frozen label, both footings: FAILURES STAND.** Per class: MW ultra-faint CEILING ONLY, bright M31 CLOSED BY COMPUTED EFFECT, M31 others CEILING ONLY.

**The label needs reading, because it fired on an overshoot.** The ceiling stack takes bright M31 past zero (-0.617, Z -2.28), and "any failing class at |Z| >= 2" doesn't say which side. On a one-sided reading the class would be CEILING ONLY. I keep the frozen label. Neither reading rescues the law:
- **The ceiling isn't physics.** It floors 14 of 31 ultra-faints at 1 % of their sigma^2, and it needs binaries with f = 1 and no giant-radius cut, in an unclipped estimator. With 3-sigma clipping, those binaries give the ultra-faints +0.62 against the data's +1.44, P 0 of 200 mocks.
- **It breaks what passes.** The same stack sends the LG field to -0.628 (Z -7.67) and MW classical to -0.821 (Z -6.62).
- **The one "closed" class leans on an orbit nobody measured.** Bright M31 closes at +0.243 (Z +1.47) only with T3, at an assumed pericentre of d/3. Without T3 it's +0.393 (Z +2.78), alt +2.48. With T3 adiabatically damped: +2.46, alt +1.75, so the footings split. Its E0 anticorrelates with computed heating (rho -0.37, p 0.07), the wrong sign for heating.

**Physics or data?** For the ultra-faints and M31 others, not data, as far as on-disk data can say. For bright M31, part data and part unresolved. For IC 1613, one geometric number decides.

## What each systematic carries
Share = fraction of the E1 miss, canonical (alt within 0.05 unless shown). Base E (Z): ultra-faint +1.302 (+6.76), bright M31 +0.555 (+3.97), M31 others +0.975 (+2.71). Frozen label after each; a class counts as CARRIES if |Z| < 2 even when the share is small.

| Systematic, variant | ultra-faint | bright M31 | M31 others |
|---|---|---|---|
| Already in the baseline: Arroyo-Polonio b (B0, what removing it adds) | -0.10 | 0.00 | -0.14 |
| Binaries, f = 0.7 ratios (B1) | 0.06 MINOR | 0.00 MINOR | 0.07 MINOR |
| Binaries, mock central, excess subtracted (B2) | -0.07 MINOR | 0.07 MINOR | -0.14 MINOR |
| Binaries, mock ceiling, excess subtracted (B2) | 0.63 CARRIES* | 0.39 PARTIAL (alt 0.42 CARRIES) | -0.09 MINOR |
| Geha DEIMOS sigma where lower (B4, N 15, same systems) | 0.10 MINOR | none | none |
| Walker multi-epoch cleaned (B3, N 6, same systems) | -0.22 MINOR | none | none |
| Tides: q < 0.5 subset (T1, N 12) | 0.33 PARTIAL, Z +3.64 | no PMs | no PMs |
| Tides: full clean subset (T1, N 6; alt N 7) | 0.44 PARTIAL, Z +3.18 | no PMs | no PMs |
| Impulse heating, central (T3) | 0.00 MINOR | 0.35 PARTIAL (alt 0.39 CARRIES) | 0.00 MINOR |
| Impulse heating, ceiling (T3) | 0.01 MINOR | 0.73 CARRIES | 0.01 MINOR |
| Membership: drop 1, 2 most deviant, Walker (M1, N 5) | 0.01, 0.12 MINOR | none | none |
| Membership: remove extreme 5 % (M2) | 0.09 MINOR | 0.22 MINOR | 0.12 MINOR |
| Membership: remove extreme 20 % (M2) | 0.28 PARTIAL | 0.65 CARRIES | 0.37 CARRIES |
| Upper limits added, Kaplan-Meier (M3) | 0.09 MINOR, Z +6.44 | 0.00 MINOR | 0.00 MINOR |
| N >= 10 only (M4) | 0.19 MINOR | -0.26 WORSENS | none left |
| Upsilon_V 4, from 2 (L) | 0.23 MINOR | 0.49 PARTIAL (alt 0.53 CARRIES) | 0.28 CARRIES |
| Upsilon_V 1 (L) | -0.23 MINOR | -0.42 WORSENS | -0.30 WORSENS |
| Estimator, best of virial, beta +-0.5, Walker, Errani (R; beta +0.5, R < R_h) | 0.04 MINOR | 0.08 MINOR | 0.05 MINOR |
| **Central stack** | **0.03**, Z +5.08 | **0.56**, Z +1.47 | **-0.02**, Z +2.75 |
| **Ceiling stack** (ultra-faint 14 of 31 floored, bright M31 8) | 1.08, Z -0.25 | 2.11, Z -2.28 | 0.61, Z +0.84 |

*Z +1.03 comes from the sd growing to 0.47 as systems hit the floor, with +0.484 still left. That is a scatter pass. Don't read it as a closure.

**Required values, not adopted:**
- Upsilon_V for a zero median: ultra-faint 42.5 (alt 38.5), bright M31 10.1 (8.8), M31 others 47.7 (41.7). At Upsilon 32 the field is at Z -6.2 and classical at -2.4.
- Stars to discard as extreme: 70 %, 33 %, 56 %.
- Sigma must fall by 4.5 times for the ultra-faints.

**How binaries read in dex.** If the law's sigma were true (median 0.62 km/s), central binaries with no clipping would give a measured 1.77 km/s: E +0.74 against the uncorrected data's +1.44, P(mock >= data) 0.000. So they can make about half the uncorrected dex from nothing, but they can't reach the data, and only about 20 % of the excess variance is theirs. With clipping it's +0.17. The ceiling, unclipped, does reach the data (+1.52, P 0.67), but it only gets there through tails a survey would clip: clipped, +0.62, P 0.000.

**Measured cleaning, where multi-epoch data exist:** E falls 0.18 for Bootes I and 0.53 for Tucana II, and 0 for Hydrus I, Reticulum II and Ursa Major II. Tucana II's single-epoch sigma is 7.48, its cleaned 4.06. Its neighbours' misses are larger than either drop.

**Tides.** The largest honest number is T1's 0.33-0.44, and it's selection: q < 0.5 keeps distant satellites, which the EFE term treats more kindly (Z2 showed this). What's left is +0.73 (Z +3.18). Exposed q >= 1 reads +1.63 (N 5), safe +0.87 (N 13). E1 on log T_peri at fixed M_V is +0.185 +- 0.093, which is a 2 sigma lean toward tides that I can't dismiss. It doesn't close anything. Impulse heating is nothing for ultra-faints because they're small.

## The field dwarfs against the satellites
**Frozen label on E0: LUMINOSITY OR ACCELERATION, both footings. It does not point at the environment.**
| canonical, satellites minus field | E0 | E1 |
|---|---|---|
| raw | +0.390 +- 0.083 | +0.906 +- 0.103 |
| at fixed M_V | **+0.028 +- 0.070** | +0.171 +- 0.097 |
| at fixed log y | +0.169 +- 0.096 | +0.169 +- 0.102 |
| 10 matched pairs, M_V -13.4 to -8.0 | +0.022 +- 0.101 | +0.156 +- 0.157 |

- **The comparison can't reach the failure.** The faintest field dwarf with a dispersion is M_V -7.98. 41 satellites are fainter. There is no isolated ultra-faint on disk, so the field class never tests the regime that fails.
- **The field's pass is a median over a trend.** E1 runs from IC 1613 -0.54 to Leo T +0.42 and Phoenix +0.40, with slope +0.081 +- 0.029 per mag. Satellites of the same luminosity behave the same way.
- **At fixed y the coefficient is +0.17, Z +1.77.** That doesn't exclude a modest environmental term. Adding the field's gas keeps it passing: -0.097 (Z -1.05), alt -0.133 (-1.45).
- **The predicted environment signal is missing.** Data slope on log x_e at fixed M_V -0.05 +- 0.20 (Z2's column, canonical), prediction -0.75; MW alone +0.01 +- 0.16 against -0.78; M31 +0.28 +- 0.34 against -0.60.

**So 55-60 % of the ultra-faint and bright M31 miss, and about 24 % of M31 others', is the external-field term itself predicting an effect the data lack.** The rest doesn't go away without it: E0 +0.587 (Z +5.17). On E0 the central stack closes bright M31 (-0.01) and leaves ultra-faints +0.54 (Z +4.06) and M31 others +0.76 (Z +2.31). Upsilon 4 alone on E0: ultra-faints +0.43 (Z +3.79). The failure has two parts: an EFE the data don't show, and a faint-end excess at any EFE strength.

## IC 1613
**Frozen label: FAILURES STAND, again by overshoot.** The ceiling stack reads +0.355 (Z +4.73). Inclination alone at the ceiling closes it, so on a one-sided reading it's CEILING ONLY. No central value closes it. Canonical (alt):
| Term | E | Z | share | label |
|---|---|---|---|---|
| base | -0.593 (-0.631) | -7.90 (-8.42) | | |
| i 37.9, RF2 HI | -0.427 | -5.70 | 0.28 | PARTIAL |
| i 34.4, RF2 optical | -0.355 | -4.73 | 0.40 | PARTIAL |
| i 24.5, RF2 16th percentile | -0.086 (-0.125) | -1.15 (-1.66) | 0.85 | CARRIES |
| pressure support | Oh+15's V is already asymmetric-drift corrected (Table 2 note), so nothing added | | 0 | |
| if it were missed, sigma_HI 5, 9, 12 | -0.492, -0.325, -0.193 | -6.55, -4.34, -2.57 | 0.17, 0.45, 0.67 | double count, not used |
| enclosed disc, gas scale R_max/3 | -0.612 | -8.16 | -0.03 | MINOR |
| enclosed disc, gas scale R_max | -0.455 | -6.06 | 0.23 | MINOR |
| external field, x_e 0.013 to 0.037 | -0.591, -0.578 | -7.88, -7.71 | 0.00, 0.02 | MINOR |
| M_star = 0 | -0.502 | -6.69 | 0.15 | MINOR |
| distance -10 %, +10 % | -0.547, -0.634 | -7.29, -8.46 | 0.08, -0.07 | MINOR |
| central stack (i 37.9, disc, field) | -0.445 | -5.93 | 0.25 | MINOR (0.247) |

- **It's inclination or nothing.** Everything else together moves it by less than the difference between 48 and 38 degrees. E = 0 needs i 22.1 (alt 21.1); |Z| < 2 needs 18.4-26.5 (17.6-25.3), which is IN1's band.
- **RF2's rows give that band 9-14 %.** This lane doesn't move RF2's class or IN1's falsifier.
- **Z -7.9 overstates the case.** It has no velocity error. With 15 % on V the base is Z -3.94, and |Z| < 2 reaches i 32.1 (alt 30.5). At RF2's centrals, 34.4 and 37.9, Z is -2.35 and -2.83 (alt -2.6, -3.09). That is still a fail, narrower than the headline.
- **The stars stay nearly consistent.** E_sigma is -0.154 at 48 and -0.081 at 34.4, so the HI curve carries the failure, and Taibi+24 attributes the HI's slow rise to holes. A disturbed gas disc is a live data explanation for the one galaxy. It isn't computed here.
- **It's the opposite sign from the satellites.** The law over-predicts here and under-predicts there, so no single satellite fix helps it.

## Failed checks and departures
- **K7 FAILED.** Slope on X1's Monte Carlo median column -0.025, predicted -0.753; line was -0.05 +- 0.02 on the slope, off by 0.025. On Z2's own central column `lb0` it gives -0.0504, so the gap is the column. The tolerance wasn't moved. **Because of K7 the primary run exits 1.** All other checks pass: K1 0, K2 0, K3, K4, K5 6e-5, K6, K8.
- **MUTATE** (M_star x 10): K1 5.9, K2 1.0 and K6 fail, as required, exit 1. Rerun byte-identical, with caches warm.
- **Departure after the first run:** T1 and M4 first compared a subset to itself, giving a meaningless 0; changed to the full class, as the share formula says. Labels on those rows came after I saw that. The script's other numbers didn't change.
- **Post-result, labelled, no label changed:** clipped mocks, damped T3, T3 at d/2, stacks without T3, stacks on E0, field slope, bright M31 heating correlation, K7 on `lb0`, measured cleaning, IC 1613 range with velocity error. The damping form (1 + (omega tau)^2)^-2.5 is from memory, PROVISIONAL.
- **R4 is a no-op:** X1 already uses circularised radii for all 82.
- **The frozen share formula misbehaves near zero:** field shares are meaningless with a base of +0.04, and classical and field read CARRIES by |Z| < 2 at base.

## Limits
- Mock N is the proxy for 67 of 82 systems. One error per star, 2.2 km/s, for all surveys.
- The binary population is solar-neighbourhood, with period parameters from memory, PROVISIONAL. Old metal-poor populations may differ.
- T3 is impulsive, one host, static, no LMC. M31 satellites have no PMs on disk.
- Membership per-star data covers 5-7 ultra-faints. M2 is a Gaussian idealisation. M31 has no per-star data on disk, so its membership is untested beyond M2 and M31 others has only 5 systems.
- Non-equilibrium beyond heating, such as disrupting remnants, isn't simulated. Field rotation is NOT COMPUTABLE from LVD, so the field E is a lower bound on g_obs. IC 1613's mass and gas distribution are smooth exponentials over a holed disc.
- Stacks aren't likely or independent, and the mock's law sigma uses the baseline's Upsilon.

**Would help (owner's OK needed, nothing downloaded):** per-star M31 satellite velocities (Collins+ or Tollerud+ tables, under a few MB, from VizieR, if published per star); M31 satellite proper motions; multi-epoch dispersions for more ultra-faints; a spectroscopic isolated ultra-faint, which is the observation that would actually test the environment; the LITTLE THINGS IC 1613 moment-0 FITS (RF2's request).

Rerun: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ux4.py` (`--mutate` for the twin). Exit 1 by K7 as above. kappa = 1/2 FITTED; not theory closed.
