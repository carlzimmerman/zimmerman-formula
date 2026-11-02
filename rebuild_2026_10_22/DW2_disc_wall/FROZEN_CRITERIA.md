# DW2_disc_wall: FROZEN CRITERIA, before any script or number from this lane

Briefed as DW1_disc_wall; DW1 is DW1_dwarf_core_flattening, so this is DW2. Search lane on the owner's standing go of 2026-11-02. **It reinstates nothing:** the cold sector's retirement stands unless the owner reverses it. Cold dark energy is a gravitating field component, never a particle. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, both reported, never pooled. No LCDM input or yardstick. Not theory closed. Nothing here says the data favour the framework. One thread, nice 19, no downloads; web numbers tagged PROVISIONAL.

**Not blind.** Read before this file: MC1 (README, mc1.py, part of mc1.out, A1), MH1, OD1, UL1, SP3, RM2, LC1, DR8, UX2, MG1, FG1 heads, HS1, BT1, DR5, BL1 heads, RQ2's REQUIREMENTS_V2, X22's scope correction, m6_decision's classify_sparc.py. So I know MC1's psi rows at U 0.5 and 0.25 and its T4 U values (EM1 f_Q 0.06/0.05; share f 0 0.27/0.24; share f_Q 0.15/0.13), and the Upsilon-by-bin rows of the off and f_Q cells on the NR2 path.

**Expectations on record.** (1) The wall survives at f_Q and EM1 at every measured Upsilon, 80 %; it narrows a lot on the share-only mass with f at its low end, and may open there against Taylor, 40 %. (2) The MC1 / M6 disagreement is mainly the profile, not the gate: X22's profile M ~ r out to r_ta holds far less inside R_last than a native one. 70 %. (3) "Law's term off where cold is present" removes the need for removal and inherits route E's tilt, surface-brightness and lensing costs, partly avoided if the term is off only where cold exceeds it; I can't guess the size. (4) No gravity-only new process comes within a factor 2 of the removal, 90 %. Survivors, if any, need a new constant and are particle-like, 70 %.

## Part (a): the wall
**Model.** MC1's: EM1 mass (a 11.18, b 0.9) or share only (M200 = 6.35 M_b); ZN2 native z = 0 shape; X39 Blumenthal scaled M0 + f (M_f - M0); SPARC Q <= 2, Inc >= 30; six V_flat bins; outer third; readings N and S. Contraction is recomputed at each U, not held at U 0.5. Psi = largest fraction of the native share with bin median d >= floor = min(d at psi 0, 0) - 2 sigma (MC1's T2). Removal R = 1 - psi.

**A1. Total-error draws.** 300 draws, fixed seed, one set per mass row, each footing. Each draw resamples galaxies (bootstrap, carrying per-galaxy distance and inclination noise) and draws:
- f: two-piece normal with mode 0.872 and 95 % edges 0.54, 1.07 (LC1). Reported single-value rows also at 0, 0.54, 0.753 (DR8 on a core), 0.946 (PZ1), 1.07.
- EM1 level: a + N(0, 0.06) dex, from BL1's blue +0.03 (-0.10, +0.14), 2 sigma. Share row has no draw.
- Shape: radial stretch s = 8.0/c, c two-piece normal mode 8.0 with 1 sigma edges 6.25, 9.63 (UL1, nine seeds). The seed range as a 1 sigma population error is generous on purpose.
- Common distance scale +- 5 % (PROVISIONAL), common gas scale +- 10 % (PROVISIONAL).
- U per bin from the scenario, below, with its own error.

**U scenarios, fixed now.** Disc U at 3.6 micron by bin, with U_tot = U (1 + 0.4 f_b) on UL1's rule where a bin's values are U_tot:
S1 flat 0.50. S2 UL1 GSWLC by bin. S3 UL1 Taylor by bin. S4 OD1 DiskMass uncorrected (K 1.0-1.3 range mid). S5 OD1 at c 1.24. S6 OD1 at c 1.43. S7 OD1 at c 1.88. Errors: UL1's own h per bin; OD1's range half-width, or 0.04 if smaller. Below-250 rows are the test. Estimators are disputed, so scenarios stay separate and are never averaged.

**Labels, per scenario, footing, mass row, reading N (S reported).**
- WALL HOLDS: P(R > 0) >= 0.95 in at least 4 of the 5 bins below 250.
- WALL OPENS: P(R > 0) < 0.50 in at least 4 of the 5 bins.
- else NOT DECIDED.
Overall (a)1: **SOUND** if EM1 and share rows both hold at every scenario. **OPENS AT MEASURED U** if a row opens at a scenario whose U is within errors of a direct measurement, naming which. **CONDITIONAL** otherwise.

**A2. U_open.** On a grid U 0.05 to 0.80 step 0.05 with f in the list above, f 0 included, each mass row, each footing, median values, no draws: largest U with psi >= 1 in at least 4 of 5 bins and in each bin; plus U_fill, U with median d = 0 at psi 1. Compare with S2-S7, NGC 628 0.75 +- 0.18, NGC 6946 0.356 +- 0.071 and 0.444 +- 0.082 (OD1), as Z. Also report the stretch s at U 0.5 giving psi = 1, against UL1's seed range.

**A3. The two gates and the two profiles, 2 x 2.** Frozen T2 and M6's fixed-U weighted rms <= 0.110, each on native and on X22's profile (M_x = f (Om/Ob - 1) M_b min(r/r_ta, 1), M6's rta), at U 0.50/0.70, readings N and S. Reproduce the witness (RMS 0.103471/0.103889, S, all 175, M6's own weights and background). Gate power: the smallest common psi and the smallest uniform multiplicative scale on g_pred that break each gate, and the law's own value on each. A gate which passes a known-bad model (g_pred x 10^0.1 or U x 2) is reported as having no level power.
Reading rule fixed now: if the pass under M6 comes from the profile, then the disagreement isn't a gate question and that goes in the README. If the pass comes from the gate, then requirement 4 is gate-dependent as MC1 said, and the overall (a) label cannot be better than CONDITIONAL.

**A4. "Absent" against "term off".** Statement 1: g = law(g_b) + psi g_c. Statement 2: the law's term is off where cold is present. Two forms:
- OFF: g = g_b + g_c everywhere (C1/C2's form).
- MAX: g = max(law(g_b), g_b + g_c), no new constant, no action, term off only where the cold term exceeds the law's.
Each with mass EM1, share; f 0, f_Q. Per-galaxy path as MC1's (U grid from 0.05, step 0.01): rms, median U, by-bin U, tilt, share of points on the cold branch by bin. Also at fixed U 0.5: median d by bin. A4-type slope (HS1's definition, V_flat 60-120, Q <= 2, 2 R_d, U 0.50, delta = V_model/V_obs - 1 on lg SBeff), LITTLE THINGS E (MC1's reader), X-COP mean log(M_HSE/M_pred) at x 0.1-1 with MC1's data and a 1e14-1e15 native shape at M200 from M500, Bullet M300 and blue/red lens read from record, with the form's branch stated.
Budget row: Gamma_off = (g_obs - g_b)/g_b at the outer third by bin against native at EM1 and share: is the required mass inside the share?
Lines, from RQ2: A1 rms <= 0.110; A2 U 0.50-0.80; A3 |tilt| <= 0.15; A4 |Z| <= 2; A9 |LT E| <= 0.10; A5 and A7 UL1's Z with UL1's h, GSWLC; X-COP |mean| and rms against ZN's line (0.05, 0.10). Margins printed for every line, pass or fail.
Also required: the rule is what a law-off disc means for scatter. Report log(g_c needed / g_c native) rms at fixed mass, per point, against the law's rms.

## Part (b): new processes
List must not repeat MH1's 19 or MC1's rows. At least these, each computed to a number; added rows go in an amendment before they are computed, or are marked post-hoc:
1 law-field contraction (the disc's law term pulls cold; forced in reading N). 2 streaming velocity at recombination. 3 GMC and cluster scattering. 4 transient spiral torques. 5 tides: neighbours, cosmic web, backsplash. 6 vacuum repulsion, turnaround against R_last. 7 population selection: discs live in a low-cold tail, against the blue lens population. 8 black hole accretion of cold. 9 universal decay. 10 conversion keyed on baryon density, integrated exposure. 11 conversion keyed on stellar density, integrated exposure. 12 decay with a kick. 13 compact objects, evaporation. 14 self-interaction. 15 ultralight scalar core.

Each row: constants needed (0, or counted), particle-like yes/no, and against these gates:
- G1 removal: reaches R_need, the (a) median, within a factor 2 in optical depth, energy or mass, at 150-250. No constant allowed to be set by hand except where counted; a counted constant is set to meet G1, and then the other gates are read at that value.
- G2 trend: removal at 150-250 no less than at 60-100 **in the channel**, and near 0 in clusters.
- G3 delivery: a stated channel with a computed efficiency, or the row reads NO CHANNEL.
- G4 dwarfs: LITTLE THINGS |E| <= 0.10 after it.
- G5 clusters unchanged: X-COP's inner mass moved by no more than its own error, x 0.1-0.5.
- G6 Bullet: the cold stays with the galaxies (collisionless, no shock).
- G7 CMB: dust through z 3e4 to 1090 lost by no more than 1 % of omega_x (the UX2 cells spread 0.1196-0.1199 is 0.25 %, and 1 % is generous).

Row labels: CLOSED AT Gn (first gate failed by over a factor 2); NEAR MISS (first gate failed by under a factor 2, margin printed); SURVIVES ON THESE GATES (all pass, counted constants listed). **A survivor gets no label until a second implementation, a separate script with its own integrator, reproduces its numbers within 10 %, and it reinstates nothing.** Particle-like survivors are stated as such, not adopted.

## Overall verdict, in the README's first line
Which side holds, in plain words: the wall (a), or a process (b), or neither. Possible: WALL SOUND, NO PROCESS. WALL CONDITIONAL ON U. WALL OPENS. PROCESS FOUND (gravity only, none needed). ONLY PARTICLE-LIKE SURVIVORS. Plus a separate line on statement 2.

## Checks, method
K1 psi row N f_Q U 0.5 equals MC1's within 0.002, both footings, at MC1's contraction setting. K2 law weighted fixed-U rms against MC1's 0.1114/0.1016 within 0.001. K3 M6 witness within 1e-3. K4 HS1's law slope -0.016/-0.023 within 0.01. K5 X-COP dM/Mg against MC1's 8.53 at x 0.1 within 1 %. K6 contraction at zero baryons returns M0 within 1e-3. K7 rho_x(1090) 2.92e-18 within 0.5 %. K8 a separate implementation, own loader and own contraction iteration, returns psi within 0.02 of the first in all cells of K1 and the OFF and MAX rows' U within 0.03, rms within 0.003.
MUTATE twin: a0 x 1.5 and share x 0.5, K1, K2 must fail, exit 1. Rerun byte-identical on the deterministic outputs. Every failed check reported. Errors disclosed.

Deliverable README.md leading with the verdict. Commits only this directory, `git commit -- <dir>`, never pushed. No edits to other lanes, PAPER67, the ledger or the outside summary.
