# Owner decision 2026-11-09: launch SK1 (spin key) and TR1 (cluster tracer) as the last catalog lanes

Owner's words, in order: "so my theory passes everywhere in the universe now?" / "bro the goal is to complete this.. you need to lay out
next steps from here" / "Launch both" / "you need to launch this in other lanes ... so go faster and conserve usage.. you are only orchestrator".

## What the record says going in (orchestrator pre-read, checked 2026-11-09)

Every local selector (QX20-QX25, EV1, DX1, BG1), every history selector (FA3 I1-I10), every action class (AX1, EW1-EW3, FA2), every
sector (cold, K(Q) dust KR1/KR2/KQ1/KD1, HC1, PB1-PB4, QX27-QX31, WD1), the Jeans gate (PJ1) and the hosted-state re-grading (XF1) FAIL on
the same rungs: isolated outer lenses + forest, cluster cores, Coma UDGs. The one selector with no verdict is ROTATION: VS4 NO VERDICT,
LAM2 NO KINEMATIC AXIS BEYOND PHOTOMETRY (estimator not buildable from fibre spectra), LAM3 NOT FEASIBLE, LAM4 criteria only. The one
empirical clue that survived is QX33/QX29 B1/HL3: the cluster missing mass sits between the gas and the BCG cusp, tracing stars + gas at
3-4x, same per-bin shape on the lensing leg.

## The two lanes

- **SK1 (TEST, quarantined):** does the law's residual at fixed baryonic mass and g_N rise as the measured spin parameter lambda_Re falls?
  Input already on disk (untracked, downloaded 11-03 for LAM1): `_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits`
  (MaNGA DynPop, 10,296 galaxies, Lambda_Re, Eps_MGE, Sigma_Re, JAM luminosity and M/L, NSA stellar masses, Qual). ATLAS3D JAM table on disk
  (`real_research/data/atlas3d_fj_table.tsv`, 261). Kill stated now: the hot-system amplitude spans two orders of magnitude across classes
  (dSph +0.2, groups/clusters +0.19..+0.45, Coma UDGs +1.1..+1.4 dex), so a spin switch cannot carry the amount alone; a hit needs a second
  variable and is graded as a selector, not a completion. FAIL closes the selector catalog; the closing statement then follows.
- **TR1 (GRADING of the adopted law):** which baryon tracer (gas, stars/BCG, stars + gas, HSE total) the cluster missing mass follows,
  per cluster and per r/R500 bin, with the amplitude. Stage 0 on disk: X-COP (12 clusters; 7 with measured stellar profiles; gas, stars,
  hydrostatic total), CLASH lensing points (Tian+2020 TSV, 84 points), HFF member-galaxy catalogues (Granata; A2744, AS1063, M0416, M1149:
  STELLAR tracer only, not lensing). Correction to the orchestrator's 11-09 message: the HFF tables on disk are member photometry, not
  lensing profiles; HFF lensing profiles are a download and need the owner's separate yes.

## Rules in force

Own terms. Both footings (canonical a0 = 1.2e-10 / alt 1.1e-10; loaders' hosted-path values 9.3603e-11 / 1.1312e-10 where the record uses
them), never pooled. kappa = 1/2 FITTED; never "theory closed". No dark-matter particle. Adopt nothing. FROZEN_CRITERIA.md committed ALONE
before any script or number, with the kill stated in advance; MUTATE must bite; known answers replayed; verify a FAIL as hard as a PASS;
per-bin SHAPE, not one amplitude; no knob scans. Commit with explicit paths only; push via a SPARSE temporary worktree of origin/main (a full
checkout filled the disk twice on 11-08); RSS under 1 GB, preemptible. No personal names, home paths, communications or outside-AI text in
committed files (`git grep -il` the owner's handle before every commit). Downloads only on the owner's yes, logged with sha256. Model:
the lanes run on Opus 5.5 at the owner's instruction; the orchestrator registers, forwards labels to Field equations, and deposits.

Folds into PAPER70 v2.0 (next deposit = --newversion 24082193) with the closing statement, whichever way SK1 lands.

## Fix-forward correction (2026-11-09, after SK1 landed)

The pre-read above called rotation "the one selector with no verdict". That was wrong: KU2 (`rebuild_2026_10_22/KU2_kappa_universality_model_choice`,
10-22) had already graded the spin parameter UNIVERSAL on the same MaNGA DynPop file at matched (M*, Sigma_Re). SK1 re-grades it on the law's
residual at matched (M*, g_N) and finds the same thing: slow minus fast +0.060 dex [+0.037, +0.081] both footings, carried by dispersion
(HX1's killed key), FAIL / FAIL. A second slip: ST1's X-ray elliptical IMF offset comes from the Humphrey 2006 table, not the ATLAS3D table
named above; SK1 replayed it on the right table. Both lanes landed: SK1 FAIL / FAIL (8fd9c516e3 / f193a68077), TR1 NO TRACER FOLLOWS /
NO TRACER FOLLOWS (45ee5f7d8b / e5a73dc99d). The selector catalog is closed under the frozen rule; PAPER70 v2.0 carries the closing statement.
