# Handoff to astra, 2026-11-04: the finish push and the lanes it leaves

Written at the owner's request ("push up this work and lanes for astra to pick up and continue"). Everything below is on `main`. The push's index is `finish_2026_11_04/README.md`; each lane's README leads with its label and lists its failed checks. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## House rules that bind every lane here
- FROZEN_CRITERIA.md committed alone before any script or number; known answers and a MUTATE twin that must bite; tolerances from stated errors, never widened after a result; failed checks reported.
- Two footings, never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2.
- Downloads, deposits and sending need the owner's yes (name, source, size). No home paths in committed files. Commit with explicit paths only (`git commit -m ... -- paths`): several sessions share one git index. Never rewrite history.
- The cold sector stays retired; no dark-matter particle.

## What is decided (don't reopen without the owner)
- **Action:** the owner adopted v3s as the a0 law's action, scoped to isolated galaxies, the Solar System, galaxy lensing and gravitational waves (`finish_2026_11_04/FN1_action_call/OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md`, 7ac515f958). Clusters and growth/CMB stay open. It supersedes that day's earlier no-action call.
- **PAPER67 v1.1 is deposited**, DOI 10.5281/zenodo.23966443. **PAPER67 v1.2 is deposited too: DOI 10.5281/zenodo.23968171** (same concept, from record 23966443; audit 794 of 794). It states v3s's scoped adoption and lists FN6 with its DR4 seal. Never run `PAPER67_zenodo_publish.py` without the owner's go.

## Dated events
| Date (UTC) | What | How |
|---|---|---|
| 2026-11-06 03:15 | ALMA U4_28473 release scoring, owner-approved | One-time scheduled task `alma-release-scoring-2026-11-06` runs `finish_2026_11_04/FN2_dated_tests/fn2_release_day.sh --run`, then runbook step 9. If it didn't run, run it by hand; approval: `FN2_dated_tests/OWNER_APPROVAL_2026-11-04_ALMA.md` |
| 2026-11-28 18:25 | GS4_24110 [CI](2-1) release | The owner triggers `fn2_gs4_release_day.sh --run` (cube and continuum approved). Its frozen MUTATE can't run on that window (exit 2); a substitute control would need a dated owner addendum before release |
| 2026-12-02 | Gaia DR4 | Compare against the frozen seals and never edit them: CW1 (`cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4/SEALED_PREDICTION.md`), the D2 note's law-first rows (law-first excluded at gamma_hat <= 1.079 canonical / 1.109 alt, `FN2_dated_tests/fn2_dr4.out`), and **FN6's window** (`finish_2026_11_04/FN6_powerlaw_screening/SEALED_PREDICTION_DR4.md`, SHA-256 495e63c9..., rule in `SEAL_CRITERIA.md`) |

## Lanes to pick up, most promising first
1. **An action that produces FN6's screening length** (theory). FN6 (9fd0447628) found a WINDOW: a smoothing length L(M) = L_MW (M/6e10)^p passes all five static gates for p 0.30-0.45. On canonical that's 3 of 48 points, all on one Milky Way cell; on alt, 9 of 48. No mass shuffle survives. v3s's own scaling is p = -1/2. FN6's p <= 0.2 rows, including the -0.5 stand-in, fail the 24 dwarfs, which matches v3s's hosted-dwarf failure. Open questions:
   - Is there a covariant mechanism whose screening radius grows as M^(0.30-0.45)? A Vainshtein radius grows as M^(1/3), inside the window; that is a reading only.
   - Does it keep the law in galaxies and pass gravitational-wave speed?
   - Needs the owner's go as a mechanism lane. FN6's engines are in `finish_2026_11_04/FN6_powerlaw_screening/`.
2. **FN6 robustness, canonical** (data, on disk). The canonical window rests on one Milky Way cell (mass 7.65e10, L 1.61-1.65 kpc). Refine the cell grid around it, and the p and L_MW grid between 0.25 and 0.5. Freeze new criteria; don't edit FN6's.
3. **FN4e, HI-selected lenses** (`finish_2026_11_04/FN4_galaxy_rows_data/FN4e_hi_lens_stack/`, criteria c03a803b3b). Stage 0, a power forecast, runs on disk now: ALFALFA, FASHI, the 17.7 GB KiDS-1000 shear catalogue and DESI BGS. Read the shear catalogue in chunks; FN4c's first run hit 25 GB.
4. **a0(z) forecast** (synthetic, on disk). FN3 and FN3b read NOT DECIDABLE with the MUSE-DARK cubes; at matched-filter S/N 30, stellar mass trades against HI, dispersion and inclination. A K2''-style scan over S/N and sample size would say what a future IFU sample needs to decide the band against the rise. Engine: `finish_2026_11_04/FN3_musedark_law_refit/fn3_cube.py`; Stage 1 code is ready. FN3b's MUTATE line was mis-specified (copied, not recomputed); recompute such lines from the lane's own levers.
5. **IC 1613 cube, redo** (`FN4a_ic1613_cube_model/`, NOT EVALUABLE). The data are on disk in `../_external_data/fn4a_ic1613_2026_11/`. Work out why the cube's HI mass is 0.716 of Oh+15's and the drift-corrected velocity is 20.85 against 16.9 (masking, primary beam, drift form). Then freeze a new lane, for example against LITTLE THINGS's own published fluxes. Read after the fact, the law already fails the cube at every inclination from 15 to 60 deg; the row is a FAIL on record.
6. **Milky Way thick share** (`FN4f_mw_thick_share_apogee/`, NOT MEASURABLE). It needs APOGEE's selection function, which the owner hasn't approved, or a thin-disc scale height to about 0.02 kpc. Low priority: LW1's Milky Way cells don't vary the share.
7. **FN4d, Local Group discs by star counts** (criteria 694b0087f5). It needs downloads: PHATTER products on MAST, and VizieR tables, which were unreachable on 11-04.

## Not to redo
- The MUSE-DARK refit with HI free, or with HI fixed at 6 Msun/pc^2 (FN3, FN3b).
- One universal smoothing length (FN1b).
- The Local Group external field from UNGC (FN4b: FIELD MOVES NOTHING).
- The Brouwer lens rebuild (FN4c: matches 255,052 against 259,383; the gap stands, +0.085 / +0.046 dex).
- Re-grading the Milky Way on Bovy and Rix's summary scale length. X5 chose its per-MAP gate deliberately; switching after the result would be choosing a test.

## Where things are
- `finish_2026_11_04/` holds FN1 to FN6.
- Memory notes for Claude sessions are in the local `.claude` folder, not the repo.
- The other sessions writing today: "Complete theory guidance" (BK2, PAPER67, v3s adoption) and "Carl's council of geniuses brainstorm" (CW lanes, LAM9).
