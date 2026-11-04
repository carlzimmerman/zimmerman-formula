# Finish push, 2026-11-04: five items, each with a verdict

The owner asked for the five things that would finish the theory, then said to do all of them rigorously. Each item is a lane here, prefix FN. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

"Finish" here means every door ends in a verdict, the distinctive claim gets its test, and outsiders can grade the record. It does not mean the theory is closed.

| Item | Lane | Verdict | Waits on |
|---|---|---|---|
| 1. Action call | `FN1_action_call/` | **Owner's decision 2026-11-04: no action is selected; requirement 12 stays open** (`OWNER_DECISION_2026-11-04_NO_ACTION.md`, STANDING.md addendum). FN1b: NO UNIVERSAL LENGTH PASSES on either footing, so a one-length smoothed QUMOND fails at its static limit; v3s stays frozen, not adopted | Nothing |
| 2. Dated tests | `FN2_dated_tests/` | ALMA 2026-11-06 02:42:31 UTC and GS4_24110 2026-11-28 18:25:24 UTC: DATE CONFIRMED. Scorer ENV IDENTICAL to v1.4; scorecard known answers 7 of 7. Gaia DR4 2 December 2026 (provisional); the bare law already has a frozen DR4 rule. **ALMA download approved; a one-time run is scheduled for 22:15 US Eastern on 2026-11-05.** GS4 cube and continuum approved | ALMA: the scheduled run (the app must be open). GS4: the owner runs `fn2_gs4_release_day.sh --run` after 13:25 US Eastern on 2026-11-28 |
| 3. a0 at z ~ 1 | `FN3_musedark_law_refit/`, `FN3b_musedark_fixed_hi/` | **NOT DECIDABLE WITH THE EXISTING CUBES.** FN3: with HI free, a planted rise of the survey's size grades BAND CONSISTENT. FN3b (after the owner's "you must find a way"): with HI fixed from local HI structure, a -0.10 to -0.16 dex bias remains and the rise comes back at 0.47 of 0.60 (TENSION, not decidable). No further redesign; no cutout requested | Deeper kinematics for galaxies like these, measured gas at z ~ 0.3-1.4, or the z ~ 2.5 deep-MOND point (CFG689 P6) |
| 4. Four galaxy rows | `FN4_galaxy_rows_data/` | Lensing: **REBUILD MATCHES, GAP STANDS** (+0.085 / +0.046 dex). Local Group field: **FIELD MOVES NOTHING**. IC 1613's HI cube: **FN4a NOT EVALUABLE** (stage-0 checks fail; post-result, the law fails the cube at every inclination 15-60 deg). Milky Way thick share: **FN4f NOT MEASURABLE** without APOGEE's selection function. FN4d, FN4e criteria frozen, not run | IC 1613: a cube whose mass and curve match the published ones, or an independent inclination. Milky Way: the selection function (not approved) or a thin-disc scale height to about 0.02 kpc; K_z without a potential family needs new observations |
| 5. Ship the record | `FN5_ship_record/` | PAPER67 v1.1 ready except the BK2 L2 line; audit 663 of 664 (the PENDING marker). Outside summary redrafted, audit 220 of 220 | BK2's L2 controls (held by the session that runs BK2, with the marker and the deposit); the owner sends the summary |

## Failed checks across the push, each disclosed in its lane
- FN1b: KT14's smoothing test fails at 24 pc; the SPARC self-check fails at 24 pc; peak memory 1.26-1.31 GiB.
- FN2: K-A3's first run compared calibrator rows too (rerun passes); default environment drifts by at most 1.3e-6 km/s; 1.05 GB peak.
- FN3: K1, K2a and K2' failed; the first K2' run crashed at its last JSON write (rerun byte-identical). FN3b: K2'' failed (a)-(d); its MUTATE line was mis-specified (copied from FN3, not recomputed for its own lever).
- FN4c: the frozen stage-2 MUTATE didn't bite (a post-result twin bites); the first run peaked at 25 GB (rerun byte-identical at 0.52 GB).
- FN4a: S0a (HI mass 0.716 of Oh+15's), S0b (20.85 against 16.9 km/s), M_free chi2_red 4.05 against 1.5; robust-cube check not run; up to 1.8 GB in the mocks. `ic1613_ubvcalib.txt` was not obtainable (the site serves an HTML page) and was not kept.
- FN4f: KA3's trough finder sat on its window edge in 8 of 10 bins; KA4 joined 91.5 % by position (100 % by ID); band 0.92 wide against 0.15.

## Process note
Commit 93b4235c4b, titled for the outside-summary draft, also carries FN3's K2 outputs and `AMENDMENT_A2.md`, swept in through the shared git index. Nothing was rewritten; FN3's README records it. Every commit since names its paths.
