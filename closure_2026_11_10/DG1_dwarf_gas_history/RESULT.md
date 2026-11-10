# DG1: the high dwarf rows under form B. HISTORY DOES NOT CLOSE THEM (both footings); the two FAILS HIGH DO NOT SURVIVE the data-side regrade

TEST lane. It relabels nothing, adopts nothing and is not registered; RB2's labels stand. kappa = 1/2 FITTED; not theory
closed. Cold dark energy is a gravitating field component, never a particle. Footings canonical (a0 9.3603e-11) / alt
(1.1312e-10), never pooled. Criteria: FROZEN_CRITERIA.md (3719fe178d, committed alone before any script or number).
AMENDMENT_A1.md (443fedfd84, POST HOC, committed alone before the final run): G5's root finder on the adiabatic edge.
Post hoc to RB2's class numbers; five classical rows were seen in the brief. G2 and G3 carry the weight.

## Labels

| | canonical | alt |
|---|---|---|
| **Lane label (history)** | **HISTORY DOES NOT CLOSE THEM** | **HISTORY DOES NOT CLOSE THEM** |
| Part A, MW ultra-faint B FAILS HIGH | DOES NOT SURVIVE the data-side regrade | DOES NOT SURVIVE |
| Part A, bright M31 B FAILS HIGH | DOES NOT SURVIVE | DOES NOT SURVIVE |
| Gate states, edge NR (no response) / AD (adiabatic) | FAILS / FAILS | FAILS / FAILS |

**What the label rests on.**
- **The no-response edge (NR) fails robustly.**
  - G2 fails with plant power 0.69 / 0.70.
  - G3 fails at fixed stellar mass and at fixed size, with power 0.50 to 0.59.
  - G4a fails: the gas-rich field control overshoots.
- **The adiabatic edge (AD) fails on two gates, and each sits on a frozen line.**
  - G2: plant power 0.50 on canonical, exactly at the line (alt 0.53).
  - G5 in MW classical: 4 of 8 rows lie above the edge's ceiling, so the class median need is infinite. With 3 of 8 it
    would have been finite.
  - Had both gone the other way, AD would read OPEN (G3 has no power there) and the label NO VERDICT. It could never read
    CLOSES: AD's G2 statistic is S +0.16, p 0.16 / +0.15, p 0.17, which is not a detection.
- **L-sensitive (frozen flag).** At P1's upper L edge, NR overshoots every class. At its lower edge, AD leaves the
  ultra-faints high. Neither L edge produces CLOSES.

**In plain words.**
- **The data side.** RB2's two FAILS HIGH rested on measurement scatter alone. Put the record's own joint budget on them
  (SE2's rule, re-derived for B) and count the dispersion upper limits the class left out. Then both intervals contain 0, on
  both footings. They do not go away: the medians stay at +0.55 / +0.51 dex (ultra-faints) and +0.30 / +0.26 (bright M31).
  The width comes mostly from the record's membership / dataset knob (0.24 dex in g for the ultra-faints) and the Upsilon
  prior. Censoring, binaries and a velocity-error floor each move the ultra-faints by less than 0.15 dex, and none of
  them alone brings the interval to 0.
- **The history.** Counting the gas each dwarf lost (P1's chemistry, the halo kept when the gas left) brings every graded
  class to zero: ultra-faints +0.58 -> -0.05, bright M31 +0.37 -> +0.04, MW classical +0.28 -> -0.01 (canonical, no
  response). But it does not pick out which dwarfs are high. Inside the 26 ultra-faints, the rank correlation of the
  residual with the predicted history is +0.06; inside bright M31 it is +0.12. Only the 8 classical dwarfs follow it
  (+0.88), and five of their residuals were known when the lane was designed. At fixed stellar mass the signal is -0.04.
  The gas-rich field dwarfs, counted with their own HI and history, are pushed 0.14 dex below their data (no-response
  edge). History reproduces the class offsets because P follows stellar mass (rank correlation -0.89 / -0.90 in bright
  M31 and classical).
- **MUTATE M2 says it plainly.** A two-number stellar-mass power law fits the graded residuals better than history does:
  rms 0.306 against 0.343 dex, BIC -96.7 against -94.1 (canonical). It reads SAME TREND RENAMED on both footings and both
  edges.

## Part A: the data side (what the people who measured assumed, and what RB2 assumed)

**Censoring.** RB2's 31 ultra-faints are only the Milky Way systems with a measured dispersion. The LVD lists 9 more
ultra-faints with an upper limit only. All 9 have M_V > -7.7, and B puts them at about 1 to 2 km/s, at or below what single-epoch spectra resolve:
- Aquarius III 3.5, Draco II 2.6, Grus II 2.0, Hydra II 4.11, Phoenix II 21.2, Reticulum III 8.3, Segue 2 2.06,
  Triangulum II 3.5 and Tucana III 1.5 km/s.
- The M31 file also has two: Andromeda XXIV (7.3 km/s; bright M31) and Andromeda XII (4.0; M31 others).
- No row carries both a measurement and a limit.

Each limit is a bound on that system's residual (canonical, dex):
- **Below the measured median:** Grus II +0.08, Tucana III +0.41, Hydra II +0.52, Segue 2 +0.56.
- **Above it, so they do not constrain:** Aquarius III +0.91, Draco II +0.99, Triangulum II +1.15, Reticulum III +1.50,
  Phoenix II +2.45.

| class (statistic: XF1's C2 bootstrap; KM median when censored) | measured only (= RB2) | with the upper limits (Kaplan-Meier) | censored-normal ML mu [95 %], tau |
|---|---|---|---|
| MW ultra-faint, canonical | +0.634 [+0.433, +0.865] (31) | **+0.543 [+0.340, +0.771]** (40, 9 limits) | +0.567 [+0.424, +0.704], 0.32 |
| MW ultra-faint, alt | +0.592 [+0.391, +0.822] | **+0.502 [+0.303, +0.729]** | +0.524 [+0.381, +0.660], 0.32 |
| bright M31, canonical | +0.273 [+0.085, +0.473] (25) | +0.267 [+0.084, +0.469] (26, 1 limit) | +0.302 [+0.160, +0.441], 0.27 |
| bright M31, alt | +0.231 [+0.046, +0.429] | +0.226 [+0.043, +0.428] | +0.258 [+0.118, +0.396], 0.27 |
| M31 others (reported), canonical / alt | +0.681 / +0.632 | +0.526 [-0.303, +1.039] / +0.472 [-0.363, +0.998] (And XII +0.20 / +0.16) | |

**Binaries and velocity-error floors** (frozen bracket; each arm is a paired rebuild of all rows, censored statistic,
canonical / alt; RB2's own choice is a0):

| arm | MW ultra-faint | bright M31 |
|---|---|---|
| a0: Arroyo free-f binary factor (RB2) | +0.541 [+0.341, +0.768] / +0.501 | +0.265 / +0.225 |
| a+: no binary factor | +0.687 [+0.489, +0.913] / +0.646 | +0.273 / +0.233 |
| af07: Arroyo f = 0.7 | +0.470 [+0.262, +0.699] / +0.430 | +0.258 / +0.219 |
| alow: the lower of LVD and Geha 2026 | +0.542 / +0.502 | +0.265 / +0.225 |
| afl: 1 km/s floor removed below 4 km/s (one more system becomes a limit) | +0.499 [+0.274, +0.745] / +0.462 | +0.264 / +0.224 |
| adown: af07 + alow + afl | +0.429 [+0.156, +0.670] / +0.390 [+0.114, +0.628] | +0.257 / +0.218 |

The bright M31 dwarfs sit above 4 km/s, so the floor and the binary arms barely touch them. Every arm leaves both classes
above 0 on the statistics-only C2.

**SE2's joint budget, re-derived for B** (anchor 0; Upsilon_V lognormal 0.30 dex, gas share U[0, 0.5] with HI limits,
distance per system, anisotropy a_c and membership m_c per class, SE2's admissibility; RB2's per-system scatter added):

| class | budget, measured only | SE2 verbatim (no per-system scatter) | **A-full: budget + upper limits** | A-full on the adown arm |
|---|---|---|---|---|
| MW ultra-faint, canonical (a_c 0.089, m_c 0.119) | +0.645 [+0.006, +1.276] (30) | +0.606 [+0.002, +1.219] | **+0.550 [-0.090, +1.175]** (39, 9 limits) | +0.433 [-0.230, +1.069] |
| MW ultra-faint, alt | +0.603 [-0.033, +1.230] | +0.566 [-0.035, +1.171] | **+0.509 [-0.110, +1.141]** | +0.396 [-0.247, +1.038] |
| bright M31, canonical (a_c 0.116, m_c 0.045) | +0.307 [-0.187, +0.790] (21) | +0.251 [-0.191, +0.708] | **+0.299 [-0.181, +0.774]** (22) | +0.286 [-0.186, +0.759] |
| bright M31, alt | +0.267 [-0.228, +0.758] | +0.217 [-0.231, +0.672] | **+0.258 [-0.237, +0.747]** | +0.247 [-0.243, +0.735] |
| MW classical (reported), canonical / alt | +0.286 [-0.205, +0.771] / +0.248 | | | |

- Admissibility removes Bootes III from the ultra-faints and Andromeda I, XVII, XIX and XXV from bright M31 (SE2's A1 / A2).
- On canonical, the ultra-faints' budget without the upper limits misses 0 by 0.006 dex. The limits are what bring 0 inside.
  On alt the budget alone already contains 0.
- **Part A outcome: neither FAILS HIGH survives, on either footing.** Read it as "consistent on the record's systematics
  budget", the same standing RB2 gave the Coma UDGs. It is not a pass: every median stays high.

## Part B: the gas history (blind until the run)

**What was computed.** Per system:
- Baryons when the halo settled = L x today's baryons, with L from P1's own chemistry (copied code; central
  `L_MDF_I0_m05`). The lost gas follows the stars.
- Today's field = today's stars (+ HI with share q 0.25 for the gas-rich field dwarfs) + the law's phantom of the settled
  baryons.
- Edge NR: the phantom does not move when the gas leaves. Edge AD: every cold shell keeps r M(<r) (slow loss).
- P = log10(g_hist / g_law(today's stars)); the after-history residual is RB2's residual minus P, per MC draw.

Coverage: P1's copied lmdf gives L for 26 of 31 ultra-faints, 10 of 25 bright M31, 8 of 8 classical, 12 of 13 LG field.

**Gate table (canonical / alt).**

| gate | edge NR | edge AD |
|---|---|---|
| G1 MW ultra-faint (26): after history [before, same rows +0.584 / +0.546] | -0.045 [-0.242, +0.218] / -0.087 [-0.285, +0.171] PASS | +0.089 [-0.115, +0.346] / +0.034 [-0.174, +0.289] PASS |
| G1 bright M31 (10) [before +0.367 / +0.325] | +0.037 [-0.219, +0.257] / -0.003 PASS | +0.126 [-0.108, +0.342] / +0.076 PASS |
| G1 MW classical (8) [before +0.281 / +0.241] | -0.010 [-0.104, +0.202] / -0.055 PASS | +0.133 [-0.055, +0.294] / +0.078 PASS |
| **G2 within class, observed on predicted** | **S +0.223 p 0.079 / +0.206 p 0.095; slope +0.33 [-0.25, +0.90] (excludes 1); FAIL** (power 0.69 / 0.70) | **S +0.161 p 0.158 / +0.149 p 0.172; slope +0.41 [-0.39, +1.13]; FAIL** (power 0.50 / 0.53) |
| per-class rank correlation (UFD / bright M31 / classical) | +0.06 / +0.12 / +0.88 (alt +0.03 / +0.12 / +0.90) | -0.05 / +0.12 / +0.90 (alt -0.06 / +0.12 / +0.88) |
| **G3m at fixed stellar mass** | S -0.035 p 0.59 / -0.023 p 0.56: FAIL (power 0.50 / 0.53) | +0.003 / +0.031: NO POWER (0.37 / 0.37) |
| G3r at fixed size | S +0.141 p 0.19 / +0.130 p 0.21: FAIL (power 0.56 / 0.59) | +0.159 / +0.127: NO POWER (0.43 / 0.44) |
| **G4a LG field, present HI + history (12)** [stars only +0.039 / +0.002] | **-0.144 [-0.302, -0.016] / -0.184 [-0.339, -0.057]: FAIL LOW (overshoot)** | -0.080 [-0.196, +0.049] / -0.124 [-0.241, +0.002]: PASS |
| G4b least-loss third (14 rows, P <= 0.38 / 0.31) | +0.077 [-0.071, +0.248] / +0.035 PASS | +0.172 [-0.002, +0.330] / +0.116 PASS |
| G5 supply: median L needed vs P1's upper edge | UFD 14.3 vs 199; M31 4.6 vs 26; classical 4.2 vs 28: PASS (alt 11.7 / 3.6 / 3.2) | UFD 42.6 (alt 22.5) vs 199, 9 rows above the edge's ceiling; M31 5.9 (alt 4.3) vs 26, 3 above; **classical: infinite (4 of 8 above the ceiling): FAIL** |

**The adiabatic edge has a ceiling.** Under slow loss, P(L) rises to a maximum and then falls: a large loss blows the
cold shells out of r_1/2. At central values (canonical):
- **Classical dwarfs and the denser bright M31 dwarfs: low ceilings.** Leo I +0.02, Fornax +0.07, Sculptor +0.08,
  Leo II +0.12, Carina +0.28, Draco +0.29, Ursa Minor +0.38 (Sextans +0.68 is the exception). Andromeda III +0.30,
  XVIII +0.31, V +0.38.
- **Ultra-faints: +0.42 to +1.24.**
- **Unreachable rows.** No amount of slowly lost gas reaches Draco (+0.63), Ursa Minor (+0.57), Leo II (+0.28), Sculptor
  (+0.20), And V (+0.63), And III (+0.48) or And XVIII (+0.60). The same holds for 9 of the 26 ultra-faints (for example
  Willman 1, Segue 1, Horologium I and Eridanus IV).

**Why it fails.**
- **No per-system signal where the offset is biggest.** The ultra-faints carry the largest offset and the widest spread
  of L (5.7 to 77). Their residuals do not track it at all: rank correlation +0.06 / -0.05.
  - Ursa Major II (L 10.7) and Ursa Major I (13.2) sit +0.54 / +0.46 above their history.
  - Hercules (L 19.9) and Leo IV (17.7) sit -0.75 / -0.43 below it.
  - Hydrus I and Pegasus IV share L 33.6; they read +0.25 and +0.50.
- **The pooled S comes from the 8 classical dwarfs.** Within them the ordering is the metallicity ordering (Fornax and
  Leo I low, Draco, Ursa Minor and Sextans high). It is also the stellar-mass ordering: P and log M* correlate at -0.90.
- **At fixed stellar mass nothing is left** (S -0.04, p 0.59). That is DF1's finding again: the dwarf extra has no
  stellar-mass key at fixed size. History as P1 measures it is almost a function of stellar mass.
- **The plant test shows the gates could see a true history**: 69-70 % for G2 on NR. So the G2 fail is not a lack of
  power on that edge. On AD the power is 0.50 / 0.53, at the frozen line (see the note under the labels).
- **The control cuts against B.** The 12 gas-rich field dwarfs read +0.04 on stars alone. Counting their HI (SE2's mid
  share) and their own history puts them at -0.14 / -0.18 on NR, an overshoot.
  - With q = 0 (all HI outside r_1/2) they read -0.084 / -0.126: PASS on canonical, FAIL LOW on alt.
  - On AD they pass.
- **L-sensitivity (reported).** At P1's upper L edge, NR overshoots every class (-0.43, -0.22, -0.24; G4a -0.39). At the
  lower edge, AD leaves the ultra-faints high (+0.31). The class match therefore holds only near P1's central reading.
- **Imputed widths (reported, never graded).** Adding the 9 bright M31 rows that have a mean [Fe/H] but no width (class
  median width imputed) moves bright M31 to -0.122 [-0.361, +0.103] on NR.
- **Lost gas more extended than the stars (2a, reported).** History buys less: class medians +0.19 / +0.09 / +0.12.

**Does form B's static state answer G2's (the older lane's) binding failure?**
- Partly, on paper. G2_preinfall_retention failed because the retained cold mass first paid the law's phantom, and the
  leftover sat in a diffuse top-hat. Inside r_1/2 that left about 9e2 Msun against a need of 4.9e5.
- In form B the share is not a leftover. It is the law's phantom of the baryons present when the halo settled, an
  isothermal profile that reaches inside r_1/2. That is why P here is 0.3 to 0.9 dex where G2's debris gave about 0.
- What form B does not supply is the premise that the halo settled before the gas left. COL1 finds the collapse does not
  reach the static state, and FB1 (section 2.2) lists it as unsolved. So the binding is answered only conditionally.
- The test above grants that premise, and the per-system signal is still absent.

**What carries over from the three older history pieces.**
- **P1:** its L columns, reproduced exactly (KA2), are the inputs here. P1's own caveat stands: L is a minimised one-zone
  number. Unmixed-ejecta escape would lower it and cannot be tested on disk.
- **CFG655 and CFG441:** they are the zero-share end of the same idea (dwarfs born without a share sit at Newton). They
  carry over as labels from outside the framework (Part C).

## Part C: the low rows (cited; no new label)

- **History cannot lift a LOW row.** P is never negative on the NR edge, so counting lost gas only adds cold mass.
  - **IC 1613:** P1's chemistry gives L = 1 (flag UNDER: its MDF needs no outflow). Its own HI adds +0.047, so it moves from
    -0.537 to -0.583 (canonical).
  - **Crater II:** L 5.27, P +0.355, so it moves from -0.443 to -0.798.
  - **NGC 147 and Cassiopeia III:** no LVD metallicity or width, so no L. History could only raise their prediction.
- **DF2, DF4, DF9 and LEDA 4014647: CFG655 as it stands.** The born-without-a-share reading (collision debris carries no
  cold share and sits at Newton; LEDA 4014647 has its own share) puts all four within 1.1 sigma. Newton Z: DF2 +0.37,
  DF4 -0.30, DF9 -0.44. LEDA 4014647 on the law: -0.74 / -1.07.
  - **This is conditional on the formation-channel label.** The label comes from outside the framework (the 2022 trail
    paper's pre-kinematic classification).
  - Only 1 of the 16 possible assignments passes (random-label rate 0.062).
  - The framework's own observables do not reproduce the label: trail membership alone fails LEDA at +3.11 sigma; age alone
    fails DF4 and DF9.
  - DF2 and DF4 are not out of sample. A captured fraction is bounded at <= 0.36 / 0.29 / 0.52 of the law target.
  - In form B the reading is physically the Bullet's (the share stays with the colliding cold component, not with the gas),
    but nothing in the action assigns it.
- **IC 1613, on disk.**
  - `_external_data/ic1613_muse2024` (the MUSE stellar survey) detects stellar rotation that agrees with the HI.
  - Its inclination is disputed: 38 +- 5 deg (Lake and Skillman 1989, adopted there), as low as 15 deg (Read et al. 2016),
    about 20 deg (Collins and Read 2022), and 32 +- 11 deg from the stars alone (the MUSE paper).
    `_external_data/little_things_oh2015` fixes i = 48 deg.
  - Inside r_1/2 the MUSE paper's dynamical mass is 1.1 +- 0.3e8 Msun with rotation at i = 32 deg, against a Wolf
    (dispersion-only) mass of 1.0 +- 0.2e8. Rotation adds about 0.04 dex at r_1/2, against the 0.54 dex shortfall.
  - The inclination debate moves the outer HI mass (5e8 to 8e9 Msun across the quoted inclinations), not the r_1/2 number
    RB2 grades. Nothing on disk lifts IC 1613 at r_1/2.
- **NGC 147, on disk:** the LVD row, RB2's numbers and a Weisz 2014 SFH (tau90 2.7 Gyr).
  - RB2's numbers: LOW by 0.56 / 0.59, r_J >= 5 r_1/2 at the strong edge, reachable only with Upsilon_V 0.58 / 0.50.
  - No metallicity width is on disk, and nothing on disk describes its tidal state.
- **Cassiopeia III:** LOW on alt only (-0.230 against s_i 0.100). Only its LVD row is on disk; there is no width.
- **Crater II:** reachable only near its LVD pericentre (16th percentile 32 kpc), and only with r_J inside r_1/2. The stars
  are then outside equilibrium (RB2).
  - P1 flags its MDF as narrow, its shape as rejected (AD p < 0.05) and its [Mg/Fe] as low (-0.40).
  - History pushes it further down.

## Part D: residual against quenching time

**On disk (reported, not in the label).** Weisz et al. 2014 cumulative SFHs (VizieR J/ApJ/789/147, tables 5 and 6) give
tau90 for 27 of the graded and field rows:
- 3 ultra-faints (Hercules, Leo IV, CVn II);
- 7 bright M31 (And I, II, III, V, VI, VII, LGS 3);
- 7 classical (Sextans is not in the sample);
- 10 field dwarfs.

| | canonical | alt | frozen expectation |
|---|---|---|---|
| D1: Delta_B on tau90 within class (S, one-sided p) | +0.240, p 0.126 (27) | +0.277, p 0.094 | S > 0 (earlier quench, higher) |
| D2: after-history residual on tau90 (S, two-sided p) | +0.047, p 0.84 (24) | -0.016, p 0.95 | no trend if the halo settled before every loss |

- The sign is the predicted one, but it is not significant.
- The classical class carries it: Sculptor 10.6, Draco 10.1, Ursa Minor 9.1 Gyr sit high; Carina 2.8, Fornax 2.2, Leo I 1.7
  sit low. Those residuals were partly seen before the freeze.
- In bright M31 the order is mixed: And V (7.3 Gyr) +0.63 and And VII (>= 12.6) +0.10.
- D2 is flat. So nothing keyed to time is left once chemistry is counted, and nothing says the early losers had an
  unsettled halo. With N = 24 that is weak.
- The CFG824 / CFG827 / CFG923 lanes used the same tables. Their results were not read for this lane.

**Held out (frozen; to be fetched only with the owner's go).** Prediction:
- **Sign:** within class, Delta_B rises with tau90 (S > 0).
- **Size:** the within-class spread of P between the earliest and latest thirds, 0.2 to 0.5 dex.
- **Statistic:** G2's stratified S with tau90 in place of P, permutation null.
- **Falsified as the cause of the high rows** if S <= 0 in a class with >= 8 systems while the class offset remains.

The M31 satellites are the clean test: about 30 systems, homogeneous HST depth, and their residuals were never seen.

Tables needed:
1. **Savino et al. 2025, the HST survey of M31 satellite galaxies (lifetime SFHs):** the per-galaxy quenching-time table
   (tau50, tau90 with errors) for the M31 satellites. VizieR id and table number to be confirmed at the fetch.
2. **Brown et al. 2014 (ApJ 796, 91), the HST/ACS ultra-faint SFHs:** the per-galaxy ages / quenching table for Bootes I,
   CVn II, Com Ber, Hercules, Leo IV and UMa I.
3. **Sacchi et al. 2021 (ApJ 920, 19), HST ultra-faint SFHs:** the per-galaxy tau90 table.
4. **Per-star [Fe/H] for the bright M31 dwarfs that have no LVD width:** Kirby et al. 2020 (DEIMOS, M31 dSphs) and Wojno
   et al. 2020. They would give P1-style L for the 15 bright M31 rows without one, and with it the M31 test of G2 at full N.

Weisz et al. 2014 is already on disk and needs no fetch.

## MUTATE twins (dg1_MUTATE.out / dg1_MUTATE.json)

- **M1, lost gas scrambled within class (20 permutations): BITES on both footings and both edges**, by the frozen rule
  (pass rate <= 2/20 and median S below the unscrambled S).
  - On NR the scramble drops S from +0.223 to +0.103 (alt +0.206 to +0.054). What ordering there is (the classical eight)
    is destroyed.
  - On AD the scramble leaves S where it was: +0.161 to +0.160 on canonical, +0.149 to +0.100 on alt. There is essentially
    no history ordering on that edge to destroy.
- **M2, a stellar-mass power law in place of history: SAME TREND RENAMED on both footings and both edges; BITES** (it moves
  G1's class medians by up to 0.04 / 0.12 dex on NR / AD, canonical; 0.08 / 0.06 on alt).
  - Fit over the 44 graded rows that have an L: Delta_B = +0.290 - 0.156 (log10 M* - 6) (alt +0.249, -0.157).
  - rms: 0.306 / 0.305 dex for the power law, against history's 0.343 (NR) and 0.346 (AD) on canonical, and 0.348 /
    0.337 on alt.
  - BIC: power law -96.7, against history's -94.1 (NR) and -93.5 (AD) on canonical. Alt: -96.9 against -92.9 / -95.8.
  - History has no free number, yet it fits slightly worse than the plain trend.
  - Within class, P and log M* correlate at -0.89 (bright M31) and -0.90 / -0.95 (classical). Only in the ultra-faints are
    they nearly independent (-0.16 / -0.19), and there the residuals follow neither.
  - Under the power law the class medians are -0.007, +0.078 and +0.011. The class match that G1 sees is what any mass
    trend gives.

## Known answers (all pass; dg1.out)

- **KA1:** RB2's per-system Delta[prim] and sd over 178 rows, and its C2 class medians, reproduced with difference 0.
- **KA2:** P1's L_MDF central, 2-sigma-low and upper edge, 93 values, reproduced by the copied lmdf with difference 0.
- **KA3:** SE2's stored a_c and m_c per class reproduced with difference 0.
- **KA4:** L = 1 gives P = 1e-16 (NR) and 0 (AD). The deep limit matches (1/2) log10 L to 1e-4. AD keeps r M(<r) to 1e-15
  and its shells stay ordered. P rises with L for L <= 60.
- **KA5:** the KM median equals the median (odd and even N). Bounds above all values leave it unchanged. km_boot equals
  boot_median. Censored ML with none censored equals the uncensored fit to 3e-10.
- **KA6:** Part A on RB2's stream, measured only, equals RB2's class medians with difference 0. The paired arm rebuild (own
  seed) differs by <= 0.002 dex (seed noise).
- **Run history.**
  - Run 1 stopped at KA4: AD at L = 1 was off by 3.1e-6 because of shell-grid interpolation. r_1/2 was put on the grid, and
    no graded number existed then.
  - Run 2 graded and exposed the G5 root-finder bug. The fix went into A1, committed alone; run 3 is the committed run.
  - Run 3 equals run 2 everywhere except G5-AD and the label lines that depend on it. NR's L_need is unchanged
    (max rel 5.4e-7 / 5.6e-7, line 1e-4).

## Hand estimate (frozen) against the outcome

| frozen estimate | outcome | mark |
|---|---|---|
| A1: KM median drops 0.15 to 0.25 dex, to about +0.40 to +0.48, still above 0 | drops 0.09 to +0.543 / +0.502, still above 0. Five of the nine limits sit above the median and do not constrain. | above 0: HIT; size: MISS |
| A2: af07 -0.05 to -0.1; afl -0.05 to -0.1; adown about +0.3 | af07 -0.07; afl -0.04; adown +0.43 / +0.39 | HIT / MISS (small) / MISS |
| A3: ultra-faint interval contains 0; bright M31 contains 0; both DO NOT SURVIVE | A-full [-0.090, +1.175] and [-0.181, +0.774] (canonical); both DO NOT SURVIVE | HIT |
| ultra-faint P +0.6 to +0.9 (L 20 to 60); G1 near 0 or a mild overshoot | median L 20.4, P_NR 0.37 to 0.90; G1 -0.045 | HIT |
| classical P 0.15 (Fornax) to 0.65 (Draco, Ursa Minor); G1 near 0 | Fornax 0.00, Draco 0.34, Ursa Minor 0.37, Sextans 0.44; G1 -0.010 | P: MISS (lower); G1: HIT |
| bright M31 P 0.3 to 0.6, a possible overshoot | P 0.00 to 0.64; G1 +0.037, no overshoot | MISS |
| G2 weak (S about +0.15, p about 0.15): FAIL 60 % | S +0.22, p 0.08 (NR); +0.16, p 0.16 (AD); FAIL | HIT |
| G3 FAIL or NO POWER, 70 % | FAIL (NR), NO POWER (AD) | HIT |
| G4a FAIL LOW, about -0.35, 55 % | NR -0.14 FAIL LOW; AD -0.08 PASS | sign HIT, size MISS |
| AD lowers P by 0 to 0.2 dex | 0 to 0.27, with a ceiling the estimate did not foresee | HIT (ceiling missed) |
| label: DOES NOT CLOSE 65 %, NO VERDICT 25 %, CLOSES 10 % | DOES NOT CLOSE, both footings | HIT |

## Limits

- **The premise is granted, not derived.** History is tested on the premise that each halo settled before its gas left.
  COL1 (the static state is not reached in collapse) and FB1 section 2.2 leave that open. The no-response and adiabatic
  responses are frozen edges, not solutions of the action.
- **L is P1's one-zone minimum.** It assumes a Fe yield bracket, homogeneous mixing and LVD widths, which disagree with
  other compilations by 2 to 3 times for some ultra-faints. L carries no error into the graded statistic; its edges are
  reported.
- **Coverage is partial.** Bright M31 has only 10 of 25 rows with a width. The Coma UDGs have no chemistry on disk and are
  not graded here.
- **The estimator is RB2's:** spherical isotropic Plummer, the Wolf estimator, RB2's instantaneous tidal cut. The SE2
  budget adds the per-system scatter on top of SE2's own rule (SE2 verbatim is reported).
- **Upper limits are hard bounds** at their quoted level; the LVD mixes 90 % and 95 % limits.
- No LCDM-calibrated quantity enters any graded row; 5.364 does not enter.
- macOS Accelerate raised spurious matmul RuntimeWarnings; every statistic was checked finite.

## Files and commits

- `dg1.py`, the script (copied code paths of RB2, P1 and SE2, with provenance in its docstring).
- `dg1.out` / `dg1.json`, the main run; `dg1_MUTATE.out` / `dg1_MUTATE.json`, the twins.
- Run commands: `OMP_NUM_THREADS=1 nice -n 10 python3 dg1.py` and `... python3 dg1.py --mutate`.
- One thread; peak RSS 0.52 GB (main), 0.39 GB (MUTATE); 745 s main, 580 s MUTATE.
- Commits, local main / origin main (local main has diverged from origin, so the lane commits were cherry-picked through a
  sparse worktree of origin/main and pushed without force):
  - criteria: 3719fe178d / (origin id in the follow-up);
  - A1: 443fedfd84 / (origin id in the follow-up);
  - script, outputs and this file: this commit / (origin id in the follow-up);
  - ids: recorded here by a follow-up commit.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.
