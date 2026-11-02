# DW2_disc_wall: WALL CONDITIONAL ON U, NO PROCESS. No computed process removes the cold from discs, gravity-only or otherwise, and every near miss is particle-like. The wall itself is softer than MC1 said: it holds at Upsilon 0.50 and at OD1's corrected values, and goes undecided at the low measured Upsilon. Separately, "the law's term is off where cold is larger" needs no removal and reads 13-14 of 15 keys, but it is a description with no action, reached after two post-result changes

Briefed as DW1_disc_wall; DW1 is taken. Criteria `FROZEN_CRITERIA.md` (d15afcc9fb), then `AMENDMENT_A1.md` (ee67e5c5bf) and `AMENDMENT_A2.md` (df14443ccd), each committed alone. **A1 and A2 were written after reading results, and both are disclosed as post-result.** **Not blind.** Scripts `dw2_core.py`, `dw2_wall.py`, `dw2_a4.py`, `dw2_proc.py`, `dw2_second.py`, `dw2_second_b.py`, `dw2_checks.py`, `cand_max*.py`, `dw2_acc.py`; numbers in the `.out` and `.json` beside them, harness scorecards in `acc/results/`. **It reinstates nothing:** the retirement of 2026-11-01 stands unless the owner reverses it. Cold dark energy is a gravitating field component, never a particle; particle-like rows below are stated, not adopted. kappa = 1/2 FITTED. Footings never pooled; pairs are canonical / alt. Not theory closed. Nothing here says the data favour the framework.

## Which side holds
- **Against every process, the wall holds.** 15 new rows: 0 pass all gates. Gravity-only rows miss by far more than a factor 2.
- **As a measured size, it isn't settled.** At U 0.50, 53-79 % must go at 150-250 km/s, in line with MC1. At the low measured U it falls to 0-39 %, and the frozen labels read NOT DECIDED. No row reads WALL OPENS. So it depends on stellar mass, a disputed measurement.
- **In reading S (cold in the law's source), WALL HOLDS in every scenario, both masses, both footings.** U can't rescue S.

## (a) Is the wall sound?
**Total-error removal R = 1 - psi, reading N, 300 draws** (f, EM1 level, shape seed, distance, gas, U, bootstrap). Median [16, 84], 150-200 and 200-250, canonical; all bins and alt in `dw2_wall.out`.

| U scenario, 150-200 / 200-250 | EM1 | Label | Share only | Label |
|---|---|---|---|---|
| Flat 0.50 | 0.79 [0.73, 0.82], 0.64 [0.44, 0.75] | HOLDS | 0.69 [0.63, 0.73], 0.53 [0.23, 0.66] | NOT DECIDED |
| GSWLC 0.374, 0.460 | 0.65 [0.43, 0.77], 0.56 [0.36, 0.74] | NOT DECIDED | 0.48 [0.21, 0.67], 0.42 [0.12, 0.65] | NOT DECIDED |
| Taylor 0.247, 0.277 | 0.39 [0.15, 0.55], 0.23 [0.03, 0.41] | NOT DECIDED | 0.15 [0, 0.35], 0 [0, 0.19] | NOT DECIDED |
| OD1 c 1.00, U 0.23 | 0.41 [0.21, 0.61], 0.09 [0, 0.33] | NOT DECIDED | 0.18 [0, 0.43], 0 [0, 0.06] | NOT DECIDED |
| OD1 c 1.24, U 0.40 | 0.75 [0.57, 0.81], 0.48 [0.23, 0.71] | HOLDS | 0.64 [0.36, 0.73], 0.28 [0, 0.62] | NOT DECIDED |
| OD1 c 1.43, U 0.56 | 0.78 [0.73, 0.81], 0.68 [0.46, 0.74] | HOLDS | 0.69 [0.63, 0.72], 0.56 [0.27, 0.63] | NOT DECIDED |
| OD1 c 1.88, U 1.03 | 0.73 [0.68, 0.77], 0.66 [0.59, 0.70] | HOLDS | 0.61 [0.55, 0.65], 0.53 [0.45, 0.58] | HOLDS |

Alt holds in more cells: EM1 at S1, S2, S5, S6, S7; share at S1, S6, S7. Overall frozen label: **CONDITIONAL.** Closest to opening: share, Taylor and OD1 c 1.00, with P(R > 0) under 0.5 in 3 of the 5 bins; the rule needs 4. Canonical Taylor reads P 0.59, 0.18, 0.17, 0.68, 0.44, and 150-200 stays at 0.68-0.73.

**Where it opens, median values, no draws.** Largest U with psi >= 1, 60-100, 100-150, 150-200, 200-250, and 4 of 5:

| Row | canonical | 4 of 5 | alt | 4 of 5 |
|---|---|---|---|---|
| EM1 f_Q | 0.10 0.15 0.10 0.15 | 0.10 | 0.05 0.15 0.05 0.15 | 0.05 |
| Share f_Q | 0.30 0.25 0.15 0.30 | 0.15 | 0.25 0.20 0.10 0.25 | 0.10 |
| Share f 0.54 | 0.35 0.30 0.15 0.30 | 0.15 | 0.25 0.25 0.15 0.25 | 0.15 |
| Share f 0 | 0.40 0.35 0.20 0.40 | 0.20 | 0.30 0.30 0.15 0.30 | 0.15 |

Measured, by the same bins: GSWLC 0.277 0.304 0.374 0.460; Taylor 0.231 0.231 0.247 0.277. These are total-light U, so bulges lower them a little. **The closest miss:** share f 0 at 150-200, 0.20 against Taylor's 0.247, margin 0.05. It needs no response, against LC1's 0.872 [0.54, 1.07]. With f_Q the margin is 0.10 (0.15 at alt). The direct dynamical pair sits above: 4-of-5 U 0.15 against NGC 6946 0.356 +- 0.071 is Z +2.9; against NGC 628 0.75 +- 0.18, Z +3.3. Those two also disagree with each other (OD1). Even at Taylor's level, MC1's per-galaxy path wants less: share f_Q by bin 0.13 0.24 0.15 0.25, Z against Taylor +0.4, -4.3, -0.6, +2.3.

**Shape.** At U 0.5 the radial stretch for psi 1 is 1.4-9.7 at share f 0, and 5 to over 30 with f_Q; UL1's seeds give 0.83-1.28. A shape change alone doesn't do it.

**MC1 against M6: it's the profile, not the gate.** Fixed-U weighted rms, Q <= 2, line 0.110, psi 1, N / S. M_x(R_last)/M_b in the first column.

| Profile, M_x/M_b | T2 psi, N, canonical | rms canonical | rms alt |
|---|---|---|---|
| X22, M ~ r to r_ta, 0.23-0.34 | 1 in all bins | 0.1025 / 0.1022 | 0.0986 / 0.1025 |
| Native share, 1.39-1.84 | 0.82 0.69 0.63 0.39 0.75 1 | 0.1090 / 0.1450 | 0.1198 / 0.1627 |
| Native EM1, 1.93-3.10 | 0.40 0.38 0.36 0.26 0.54 1 | 0.1298 / 0.1817 | 0.1429 / 0.2011 |

Witness reproduced to 1e-6. On X22's profile both gates pass (T2 on S drops only to 0.79-0.83). On native, both fail, with one exception: share, N, canonical, at 0.1090, margin 0.001. So **"discs forbid cold" means "discs forbid the native profile"**; a profile holding 5 x less mass at R_last passes both. By the frozen rule this isn't a gate question. X22's profile has no process making it, and the zooms don't. The 0.110 gate does have level power: law x 10^-0.1 reads 0.1805. But the law itself at canonical reads 0.1114, over the line.

## "Absent" against "term off"
**Plain OFF, g = g_b + g_c: fails.** U by bin hits the ceiling 1.20 in dwarfs, tilt +0.52 (EM1 f 0), +0.81 (EM1 f_Q), +0.45, +0.65 (share); LT +0.344, +0.572. Budget at U 0.5, f 0: the disc wants Gamma_off 2.2-4.4, native holds 1.14-2.28 at EM1, 0.83-1.19 at share, so need/native 1.5-2.5, 2.2-4.1. Per point, cold would have to carry an extra 0.35 dex of scatter against native at fixed mass, where the law's own is 0.18 unweighted. In its favour: f_Q on L* gives U 0.33, 0.42, with GSWLC Z -1.1, -0.6, which the law doesn't reach (+1.7, +1.8). Surface brightness: b -0.010 +- 0.061 at EM1 f_Q, -0.087 +- 0.055 at f 0, on the native shape. HS1's -0.227 was on its own halo and I didn't reconcile them. So the tilt, not the surface brightness, kills OFF here.

**MAX, g = max(law(g_b), g_b + g_c): the near miss.** No new constant, no action, a kink. Second implementation is RQ2's harness with the rule's own contraction. Mode r200 of A2, canonical / alt:

| Line | Law | MAX share f_Q | MAX EM1 f_Q | Margin, share f_Q |
|---|---|---|---|---|
| A1 rms <= 0.110 | 0.0541 / 0.0537 | 0.0662 / 0.0617 | 0.0636 / 0.0621 | clear |
| A2 U 0.50-0.80 | 0.52 / **0.44** | 0.50 / **0.43** | **0.42 / 0.38** | 0.00 / -0.07 |
| A3 tilt | +0.02 / -0.02 | +0.08 / -0.01 | +0.09 / -0.02 | clear |
| A4 Z | -0.25 / -0.36 | -0.30 / -0.38 | -0.79 / -0.84 | clear |
| A9 LT | -0.025 / -0.064 | same | same | the harness's LT row sees the law branch |
| A5, A6, A7 | FAIL | **FAIL** +5.13, +7.17, -3.24 | | worse than the law on A7 |
| A10 IC 1613, A12, A13 dwarfs | FAIL | **FAIL, same** | | MAX can't lower the law |
| A30 KiDS chi2 | **FAIL** +9.27 / +6.52 | **FAIL, same** | **FAIL** +9.70 / +6.55 | |
| B1 groups | PASS | PASS -0.28 / +0.33 | PASS | |
| Keys of 15 | 10 / 10 | **13 / 12** | **14 / 14** | |
| G-OUT-M3 | +4.76 / +3.99 | **+3.78 / +3.27** | **+4.03 / +3.49** | over by 1.78 / 1.27 |
| G-MID-T3 | +4.86 / +4.54 | **+2.08 / +2.05** | +1.94 / +1.97 | over by 0.08 / 0.05 |
| G-OUT-all | | -1.49 / **-2.00** | | at the line, alt |
| B19 total error | +3.80 | **+2.97 / +2.49** | +3.18 / +2.67 | |
| B20 joint | p 3e-8 | **p 0.024 / 0.040**, line 0.05 | 0.019 / 0.036 | |
| X-COP B23, B24 | FAIL +0.47, 0.48 | PASS -0.047, **0.0995** | PASS -0.016, 0.088 | **0.0005 at rms** |

**Read it carefully.**
- **It isn't a pass.** G-OUT-M3, joint, A5-A7, A10, A12, A13, A30, C1 fail. Milky Way, DiskMass, Bullet weren't computed: the map returns the law, because the cold isn't placed through this harness. MC1's multi-stream point stays open. g >= law everywhere, so MAX can't relieve what the law overshoots.
- **Weak in discs by construction.** At share f 0 the cold branch holds 0-5 % of points, so it passes as the law does. Share f_Q runs the cold branch at 54-64 % above 150 km/s, moving 150-250's U toward GSWLC (Z +0.3, +0.7), but making the step worse.
- **Real content in clusters, and fragile.** X-COP passes through the linear gas extension to R200. With M_b stopped at the array's end it reads +0.129, rms 0.161, a fail. The keys row under A1's first rule was 4 of 15, all too heavy (G-OUT-M3 -7.23). A2's correction is justified, but it came after seeing that. So the row's pass count is post-result and needs an independent freeze.
- **No reason is given.** Nothing says why the cold's pull and the law's term shouldn't add. It needs an action, which fails RQ2's E rows by absence. It is not a process and doesn't show that cold exists in discs.
- **Harness tag.** Every row reads [LABEL], because the rule groups X-COP's arrays by r500. It's a grouping, not a switch, but the tag stands.
- Twin: cold x 10 fails X-COP, groups and lenses (B23 -8.19), and A1-A9 stop at a division by zero in the harness. So the SPARC rows of the twin read NOT COMPUTABLE, not FAIL.

## (b) New processes
R_need 150-250, canonical: EM1 0.74, share 0.63; tightest psi 0.20 / 0.29 at 150-200. Numbers in `dw2_proc.out`, `dw2_second.out`. Constants counted.

| # | Process | n | Particle-like | Number | Label |
|---|---|---|---|---|---|
| 1 | Law-field contraction (forced in N) | 0 | no | Cold at outer third x0.94-0.96 of Newtonian; psi 0.29 to 0.31; removes nothing | CLOSED G1 |
| 2 | Streaming at recombination | 0 | no | Drift 0.048 Mpc, 3 % of Lagrangian radius; removes nothing; larger in dwarfs | CLOSED G1, x23 |
| 3 | GMC, cluster scattering | 0 | no | 1e7 clumps, all gas: energy 0.01 of V^2 at most | CLOSED G1, x100 |
| 4 | Transient spirals | 0 | no | Lifting takes 1.0-1.06 (share), 1.7-1.85 (EM1) of disc J; at most 0.4 can go (PROVISIONAL); efficiency not computed | CLOSED G1, x2.6+ |
| 5 | Tides, backsplash | 0 | no | r_J x18-32 R_last at 1 Mpc from 1e12; needs a 6e15-3e16 host | CLOSED G2 |
| 6 | Vacuum repulsion | 0 | no | Zero-force radius x29-50 R_last | CLOSED G1 |
| 7 | Discs as a low-cold tail | 0 | no | -0.58 dex is 3.9 sigma (share 2.9 sigma); blue lenses are the whole population at A 0.878 +- 0.074 | CLOSED G1 |
| 8 | Black hole eats cold | 0 | no | M_BH/M_c at most 9e-5 | CLOSED G1, x7000 |
| 9 | Universal decay | 1 | yes | Clusters lose the same, x11-13 over X-COP's error | CLOSED G5 |
| 10 | Conversion on rho_b, integrated | 1 | yes | CMB era exposure 2.4e8 against disc 5e6 Msun/pc^3 yr: all cold gone before last scattering | CLOSED G7, x100 |
| 11 | Conversion on rho_* | 1 | yes | See below | **NO CHANNEL, G3** |
| 12 | Decay with a kick | 2 | yes | See below | **NEAR MISS** |
| 13 | Compact objects, evaporation | 1 | yes | 1.3e11 Msun needed against 3e6 disc heating (PROVISIONAL) | CLOSED G1, x4e4 |
| 14 | Self-interaction | 1 | yes | 6.1 cm^2/g against 0.47-1.25 (PROVISIONAL); M(<R_last)/native 1.00, 1.07 in the baryon well; k 4 unconverged | CLOSED G1 |
| 15 | Ultralight scalar core | 1 | yes | See below | CLOSED G1, x2.2 |

**Row 11, cold converts where stars are.** The most striking arithmetic. CMB is clear (no stars). rho_* (<r) t is near-flat across bins, so one sigma gives retained 0.62 0.54 0.44 0.33 0.42 by bin up to 250, against MC1-type room 0.61 0.48 0.49 0.29 0.44, d - floor +0.006 +0.030 +0.012 0 +0.039, canonical share, LT -0.072, X-COP lost 0.023 against error 0.056. Two implementations agree within 8.2 %. **It doesn't survive.** (i) G3: no sink, no action. If the energy reached stars it would be x4600 L_sun per solar mass, so it must be dark to 1 part in about 5e5. (ii) Form: with the local shell density in place of the mean inside r, retained stalls at 0.42-0.44 against 0.20-0.29: x1.45 share, x2.2 EM1. The cold's orbits decide which is right, and I didn't compute them. (iii) Alt fails 100-150 by -0.016 dex and LT -0.108 by 0.008; EM1 misses at both footings (LT -0.112, -0.145). (iv) It's a non-gravitational coupling of the kind the owner's rule keeps out.

**Row 12.** Orbit Monte Carlo, D 0.8. No v_k clears both: v_k 300: retained 150-200 0.37, x1.85 over; X-COP x 0.1 loss 0.090, x1.6 over. v_k 382: 0.26, x1.3; 0.119, x2.1. Published limits (Peter et al. 2010 on clusters, Wang et al. 2013 on the forest, PROVISIONAL, on a CDM frame so read with care) exclude this range. The first, log-potential estimate of cluster loss, 0.04, was low by x2-3, so it fails the 10 % agreement rule and gets no higher label. HSE's bracket would clear G5 by itself. The same-mass red lenses need the cold kept, with no selector.

**Row 15.** No removal for m22 above about 0.1. Below it the core-halo fit alone gives 0.13 at m22 0.003, but the solved ground state in the baryon well gives 0.23, 0.72 against 0.20, 0.33, x2.2. Lower m22 needs a soliton heavier than the halo's cold. First and second disagree by over 10 %. m 3e-25 eV is under published CMB (about 1e-24) and forest (about 1e-21) limits, from memory, PROVISIONAL. Share mass not solved.

**Survivors: none.** Near misses are all particle-like. So the honest statement of the search: anything that removes the cold from discs while keeping it in clusters and the CMB, among these, looks like a coupling or a particle property, and even those miss. It isn't a no-go theorem.

## Limits
- U draws: S1's 0.04 dex wasn't stated in the frozen list; set by the rule for OD1 rows. Scenario errors for estimators treat bins as independent. EM1's scatter is one level per draw, not per galaxy. Contraction at fixed M200 from U 0.5. Bootstrap sigma in floors fixed at the mode.
- Spherical, static. M200 from baryons alone. Row 12 kicks circular orbits, 3 Gyr, no re-virialising, rough mock clusters. Row 14 one galaxy. Row 15 uses the fit's M_sol far outside where it was calibrated, and a monopole baryon well.
- Web reading only for rows 12, 14, 15; several inputs from memory, marked PROVISIONAL. Groups, MW, DiskMass under MAX: groups only. Lens colour split under MAX not wired.

## Checks and errors
K1 psi 0.0000, both. K2 law 0.1114 / 0.1016. K3 witness to 1e-6. K4 -0.0155, -0.0229. K6, K7 pass. Fast contraction against X39: psi 0.0001. **K5 is a read of MC1's JSON, not a recompute.** **K8: rms FAILS at the 0.003 line,** 0.0053 / 0.0058, U passes 0.01. The law's own difference on those two paths is 0.0028 / 0.0038, and samples differ (Q <= 2 against 175). So MAX's rms gets no agreement label, and the table above uses the harness. MUTATE (a0 x 1.5, share x 0.5): K1, K2 FAIL, exit 1. Reruns: wall, A4, processes byte-identical; second implementation byte-identical.

Errors, mine, caught reading output, all before labels:
1. Row 1 first form treated the law's mass as if it had started mixed with the cold: x0.58, and my text said "adds cold". Rewritten; it now reads x0.95. 
2. Orbit integrator: acceleration carried one factor of the unit conversion. Fixed.
3. Orbit sampling put about 10-16 % of mass at exactly R, so v_k 0 read 0.905, 0.84. Fixed to 1.000, 1.000; G5's row moved from x2.7 to the numbers above. 
4. A1's mass rule on keys (A2). 
5. Row 4's first text said the disc's J could pay; 1.0-1.85 of it can't. Reworded, label moved from NO CHANNEL to CLOSED G1.

## Expectations against result
Wall survives at f_Q and EM1 at every measured U, 80 %: **wrong,** NOT DECIDED at GSWLC and Taylor. Opens on share with low f against Taylor, 40 %: not at the frozen rule, 3 of 5. MC1 / M6 mainly profile, 70 %: yes. Term off costs route E's tilt, partly avoided when off only where exceeded: yes, and I didn't expect keys to move this far. No gravity-only row within x2, 90 %: yes, row 4 the nearest. Survivors particle-like, 70 %: no survivors; the nearest are.

## What would change this
Star counts for Upsilon at 3.6 micron on about ten discs (RQ2's A19) decide the first half directly. For MAX: an independent freeze before any run, the Bullet with the cold placed, Milky Way with a vertical form, an action. For row 11: the orbit average.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
Sources, web read, PROVISIONAL: [Peter, Moody, Kamionkowski 2010](https://arxiv.org/abs/1003.0419); [MW Satellite Census IV](https://arxiv.org/abs/2201.11740), citing Wang et al. 2013; [Randall et al. 2008](https://arxiv.org/abs/0704.0261); [Harvey et al. 2015](https://arxiv.org/abs/1503.07675).
