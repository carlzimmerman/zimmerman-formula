# CLR1 RESULT: form B on Combes's 106 HIFLUGCS clusters

## Verdict per footing

- **canonical (a0 = 9.3603e-11): STILL FAILS [non-cool-core clusters, 0.1-0.5 R500: over-predicts] FRAGILE.**
- **alt (a0 = 1.1312e-10): STILL FAILS [non-cool-core clusters, 0.1-0.5 R500: over-predicts] FRAGILE.**

The B numbers are the same on both footings: no a0 enters form B in clusters, and the two h values differ by 1e-4 (null Z2:
largest difference 0.00007 dex). a0 enters only the law-only row.

In plain words:
- **At R500, form B closes the residual in all three classes.** Its retained cold, R = 5.41 times the visible mass, matches the
  hydrostatic total to within the 0.08 dex band. Combes's own MOND leaves +0.10 to +0.19 dex at R500 on the same data. The
  record's law alone leaves +0.11 to +0.24 dex.
- **The one failing cell is a shape cell.** In the 56 non-cool-core clusters, with the cold amount set by the edge, B's native
  cold profile puts more mass at 0.1-0.5 R500 than the beta-model hydrostatic mass allows: -0.137 dex, 95 % interval
  [-0.182, -0.089].
- **The fail is fragile.** The interval's upper end is only 0.009 dex beyond the line. Hydrostatic bias b = 0.1 or 0.2,
  T x 1.1, T_m in place of T_h, or single-beta gas each move that cell to CLOSED.
- **The cores cannot decide.** In non-cool-core cores the visible mass is above the hydrostatic mass (DATA-INCONSISTENT,
  56 of 56, as Combes also found). In weak and strong cool cores the 20-30 kpc cell has NO POWER: bootstrap half-widths
  0.17 to 0.31 dex.
- **No 20-30 kpc residual is left for B to fill in cool cores.** In strong cool cores B's median there is -0.13 dex (B already
  supplies enough or more). Combes's MOND gives +0.06 there, and Newton baryons +0.21.

Criteria 7756d82189 (committed alone first); scripts and transcribed inputs 904650fa2f; this result after. TEST lane: adopts
nothing, relabels nothing, scorecard untouched. Not pushed.

## Key table (footing frame, h 0.674; median over clusters of per-cluster log10(M_dyn / M_pred), 95 % bootstrap, band +-0.08)

| class (n) | cell | Newton baryons | Combes MOND (RAR, 1.2e-10) | law only canonical / alt | **form B (graded)** | B word |
|---|---|---|---|---|---|---|
| NCC (56) | OUTER R500 | +0.912 | +0.192 [+0.165, +0.215] | +0.239 / +0.203 | **+0.105 [+0.037, +0.154]** | CLOSED |
| NCC | MIDDLE 0.1-0.5 R500 | +0.905 | +0.336 | +0.378 / +0.345 | **-0.137 [-0.182, -0.089]** | **OVER-PREDICTS** |
| NCC | CORE 20-30 kpc | -0.820 [-0.970, -0.689] | -0.993 | -0.979 / -0.998 | -1.186 | DATA-INCONSISTENT (excluded) |
| weak-CC (25) | OUTER | +0.884 | +0.102 [+0.038, +0.172] | +0.151 / +0.113 | **+0.078 [+0.049, +0.168]** | CLOSED |
| weak-CC | MIDDLE | +0.895 | +0.341 | +0.385 / +0.350 | **+0.029 [+0.021, +0.045]** | CLOSED |
| weak-CC | CORE | +0.233 | +0.010 | +0.030 / +0.008 | **-0.171 [-0.574, +0.039]** | CLOSED (NO POWER) |
| CC (25) | OUTER | +0.829 | +0.142 [+0.120, +0.180] | +0.190 / +0.153 | **+0.022 [-0.025, +0.044]** | CLOSED |
| CC | MIDDLE | +0.882 | +0.405 | +0.442 / +0.413 | **+0.024 [-0.019, +0.082]** | CLOSED |
| CC | CORE | +0.208 [-0.005, +0.305] | +0.056 [-0.187, +0.132] | +0.067 / +0.049 | **-0.130 [-0.377, -0.045]** | CLOSED (NO POWER) |

How to read the B column:
- OUTER uses anchor A1 (f_ret = 1 at R500, B's minimum cold). log Q_B = log[M_dyn / ((1 + R) M_vis)].
- At R500 the visible fraction M_vis / M_dyn is 0.123 (NCC), 0.131 (weak-CC) and 0.148 (CC), so f_ret is about 0.76, 0.82
  and 0.94.
- MIDDLE and CORE use anchor A2: the cold amount is set by the edge, so these cells test only where B puts its cold.

## Questions (a), (b) and (c)

- **(a) Ratio of required to predicted mass.**
  - At R500, B's median is 10^0.105 = 1.27 (NCC), 1.20 (weak-CC) and 1.05 (CC).
  - Plain MOND (Combes's setup) gives 1.56, 1.26 and 1.39. Newton baryons give 8.2, 7.7 and 6.7.
  - All 106 pooled are reported only: B +0.061 [+0.042, +0.086]; MOND +0.161 [+0.142, +0.180].
- **(b) Where the residual is.**
  - In this rebuild, plain MOND's residual lies at 0.05-0.5 R500. Class medians by r/R500 bin are +0.50, +0.48 and +0.35 dex
    in strong cool cores.
  - Half of the positive MOND residual lies inside 264 kpc (CC), 139 kpc (weak-CC) and 413 kpc (NCC). That is the median over
    clusters of the radius where the cumulative residual reaches half its peak.
  - This rebuild does not find most of the residual mass at 20-30 kpc. At 20-30 kpc the CC MOND residual is +0.06 dex.
  - Combes's "core of 20-30 kpc" is a statement about the residual's density profile. The cumulative mass is spread out to
    hundreds of kpc.
  - B's residual has no strongly positive cell anywhere. It is near 0 from 50 kpc to R500 in cool cores. In NCC clusters it is
    negative inside 0.5 R500, which is the failing cell.
- **(c) Cool core against non-cool core.** B closes all graded cells in weak-CC and CC. The single fail is NCC MIDDLE.
  NCC CORE is excluded as DATA-INCONSISTENT: the BCG + ICL scaling relation exceeds the beta-model hydrostatic mass at
  20-30 kpc.

## Known answers (all pass; nothing stopped)

- **KA-P:** 106 clusters, 49 with double-beta fits, classes 56 / 25 / 25. These equal Combes's Table 2 exactly.
- **KA-U (units):**
  - Chen's M500, re-derived from T_h and the beta fits at Chen's r500: median ratio 0.986 (single-beta clusters) and 0.988
    (double-beta). Tolerance 3 % / 5 %.
  - M500 / (4 pi/3 r500^3) / rho_c(z) = 498 with rho_c(z) = rho_c0 (1+z)^3 at H0 = 50.
  - A0085's asymptote is identical in SI and in cgs: 6.373013e14 Msun.
- **KA-C (Combes's own MOND residual, her frame H0 = 50 EdS, RAR, a0 = 1.2e-10):** passes under definition D2 only.
  - D2: plateau dark mass over M_MOND(R500). Mean 0.389 (hers 0.41). Her simple function gives 0.517 (hers 0.53).
  - Median M_dyn / M_MOND at R500 is 4.62, 10th-90th percentile 3.53-7.24 (hers: 4-10).
  - Median M_dark / M_gas is 0.494 (hers: "roughly twice lower").
  - D1 (both at R500) fails: 0.096. Her radius was not stated; the criteria froze both definitions.
- **KA-X:** RB1's X-COP f_ret, with RB1R's loader copied: 0.885, 0.934, 1.235, 1.259, 2.216, 1.095, 0.511, median 1.095. Exact.
- **KA-I:** RAR and simple-function round trips 6e-15; m_native(1) = 1.0001 / 1.0000; Q_B(R500) identity 2e-14; the Newton limit
  is exact.
- **Reported, not a known answer:** an analogue of Combes's Table 2 in her frame.
  - Visible mass above hydrostatic at 20 kpc: 56 / 15 / 20. Hers ("BCG+ICL overmassive"): 56 / 12 / 8.
  - Visible above M_MOND at R500: 10 / 12 / 8. Hers ("outer parts overmassive"): 8 / 7 / 6.
  - Her definitions are not stated.

## MUTATE and null twins (`clr1_MUTATE.out`)

- **M1, cold r x 3:** the CORE cells move 0.24 / 0.28 / 0.22 dex. BITES, so the core test can see the cold's shape.
- **M2, Combes's recipe with a0 -> 0:** 0.817. BITES: the KA leaves its band.
- **M3, R x 2:** the OUTER cells move 0.266 dex. BITES.
- **Z1 null twin (grid 240, seed 1115):** it **bit, narrowly.**
  - The largest shift is 0.0138 dex, in CC CORE. The line was 0.01. Every other cell moved 0.007 dex or less.
  - No cell word changed. The cause is that the core mean is taken over about 5 grid points of a steep profile.
  - The CC CORE cell therefore carries about 0.014 dex of numerical noise. It is NO POWER and does not decide the word.
- **Z2 (canonical against alt):** 0.00007 dex. Quiet.

## Brackets (frozen before the run; word per footing, identical on both)

| bracket | B word | what moved |
|---|---|---|
| H b = 0.1 / 0.2 | STILL FAILS [NCC, weak-CC OUTER: residual remains] | NCC MIDDLE -> CLOSED (-0.116 / -0.094); NCC OUTER +0.148 / +0.194 |
| T1 T x 1.1 | STILL FAILS [NCC OUTER: residual remains] | NCC MIDDLE -> CLOSED |
| T2 T_m for T_h | **NO VERDICT** | NCC MIDDLE -> CLOSED; CORE cells NO POWER |
| G2 single beta for all | STILL FAILS [CC MIDDLE: residual remains; CC CORE: over-predicts] | NCC MIDDLE -> CLOSED |
| S1 R_e 15 kpc; S2 DeMaio x 2; T3 r_T = r_c; N1 native inner slope | STILL FAILS [NCC MIDDLE; CC CORE: over-predicts] | CC CORE -0.18 / -0.28 / -0.19 / -0.26 |
| T4 central 0.5 T_h | STILL FAILS [NCC MIDDLE; weak-CC and CC CORE: over-predicts] | CC CORE -0.52 |
| S3 Giodini / 1.5 | STILL FAILS [NCC MIDDLE; weak-CC OUTER: residual remains] | weak-CC OUTER |
| S1 R_e 60, S2 / 2, S3 x 1.5, galaxies follow gas, G1 n_center, T1 x 0.9, T3 isothermal, R 5.562, P core PSF | unchanged (STILL FAILS [NCC MIDDLE]) | P leaves fewer than 5 clusters in the NCC and CC cores (NOT EVALUABLE) |

- **Hence FRAGILE.** The located fail disappears under hydrostatic bias, a 10 % hotter temperature, T_m, or single-beta gas.
  Under the hydrostatic-bias brackets the fail moves to the outer cells. There the direction is "residual remains", which B
  allows one-sidedly: it reads as baryons lost.
- **No bracket makes B over-predict at R500.** In the footing frame, B's ceiling is never broken in this sample. That direction
  would be a hard fail.
- **Reported only:**
  - Combes's frame (H0 = 50): B's CC OUTER cell over-predicts, -0.108 [-0.173, -0.093], i.e. the ceiling is broken at
    h = 0.5. Gas fractions scale as h^-3/2, so the frame decides this.
  - h 0.7 / Omega_m 0.3: same word as the footing frame.
  - NFW-Duffy (EXTERNALLY CALIBRATED): NCC MIDDLE -0.102 [-0.149, -0.065], CLOSED. Word NO VERDICT (no fail; the core cells
    have NO POWER).
  - A1 anchor in the inner cells: NCC MIDDLE -0.084, CLOSED.

## Red-team of the data team's assumptions (written in the criteria before the run; what the run showed)

- **Hydrostatic equilibrium.**
  - b = 0.1-0.2 removes the one failing cell.
  - The NCC classes are the merging and disturbed systems, where non-thermal pressure is largest.
  - The literature's size for b is itself set partly by assuming the cosmic baryon fraction, so it cannot decide this.
- **Beta-model extrapolation, checked against X-COP.** Eleven HIFLUGCS clusters are X-COP clusters. At h 0.7, the beta-model
  M_dyn against X-COP's M_FORW has median log ratio:
  - -0.021 at 0.3 R500, -0.022 at 0.5 R500 and +0.044 at R500;
  - for gas, -0.03 to -0.04.
  - So on the overlap the rebuilt masses agree with X-COP to about 5 %. The NCC MIDDLE over-prediction is not a gross
    beta-model artifact.
  - For the overlap NCC clusters A2255, A3266 and A1644, B's middle cell reads -0.28, -0.28 and -0.20, while their beta-model
    M_dyn agrees with X-COP within 0.11 dex at 0.3 and 0.5 R500.
  - RB1's gate 3 used only the 7 X-COP clusters with stellar profiles (mostly cool cores), so it did not test these.
- **ROSAT PSF.** The core cell sits at the PSPC resolution for almost all clusters. Bracket P leaves fewer than 5 clusters in the NCC
  and CC cores, so the cores cannot be graded from these data.
- **Temperature.** A strong cool core (T4, 0.5 T_h centrally) makes B over-predict in both cool-core classes' cores. Isothermal
  (T3) makes the CC core +0.013. The core reading is set by the temperature model, not measured.
- **BCG + ICL.**
  - The scaling relation, not photometry, sets the inner visible mass.
  - It makes all 56 NCC cores DATA-INCONSISTENT; Combes reports the same 56 of 56.
  - A x 2 BCG makes the CC core over-predict.
- **h.** Chen's tables use H0 = 50, and Combes's aggregates are reproduced in that frame. KA-C was not run at the footing h,
  because it passed in her frame. Both MOND's residual at R500 and B's ceiling turn on h. The graded frame is the footing's.

## Limits

- Combes tabulates no per-cluster values. Her unstated choices were frozen and bracketed: BCG R_e, the cool-core radius,
  the galaxy profile, H0, and the radius of "0.41".
- Masses are 2007 ROSAT + ASCA beta-model hydrostatic masses. 14 of 106 temperatures come from L_X-T.
- Not modelled: EFE, lensing, non-thermal pressure, member-galaxy kinematics.
- B's cold uses ZN4's native shape. Its inner m proportional to x^2 is resolution-limited; bracket N1 moves only the CC core.
- KA-C passes only on the plateau definition (D2).
- The Z1 null twin failed its 0.01 line by 0.004 dex in one NO POWER cell.
- Two runs of the uncommitted script came before the script commit (disclosed). The first crashed in bracket T4: the R500 root
  finder hit M_dyn <= 0 at 50 kpc and was fixed to take the outermost crossing. Two printed diagnostics were then added: Z1's
  per-cell shifts and the Table 2 analogue. No criterion, line, cell or bracket changed.
- **Run command, for a lead re-run from a copy** (repo root as working directory):
  `python3 -I -B closure_2026_11_14/CLR1_combes_cluster_residual/clr1.py closure_2026_11_14/CLR1_combes_cluster_residual/clr1_chen2007_inputs.csv rebuild_2026_10_22/ZN4_cluster_resolution/zn4_shapes.json closure_2026_11_06/QX15_cmb_primary_likelihood/qx15.json real_research/data/xcop <out dir>`
  It takes about 45 s. The transcription is re-made with
  `python3 -I -B .../clr1_transcribe.py _external_data/clr1_combes/chen2007/src/chenyAAfinal.tex <csv>`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
