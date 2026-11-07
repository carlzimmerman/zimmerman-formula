# QX31: LCDM assumptions in the growth / CMB-lensing data products. No failure is an artefact; every one is ROBUST or "PARTIAL as frozen" in the direction that WORSENS it

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled.
- Criteria: FROZEN_CRITERIA.md (99e2469342, pushed alone before any number).
- Amendment A1 (post-result): K1 reference values. See AMENDMENT_A1.md.
- Ledger: ASSUMPTION_LEDGER.md.
- Script: qx31.py (about 12 s, 0.2 GB, one thread). It uses the record's machinery read only: cfg917_lib, WG6's projection
  copied unchanged, QX3 iter2 imported, and the iter3/QX27 solver copied unchanged.
- Outputs: qx31.json/.out. MUTATE twin: qx31_MUTATE.json/.out. Logs: run_main.txt, run_mutate.txt.

## Question and answer

The question: do the LCDM-dependent steps inside Planck PR4 lensing, PR4 CamSpec + ACT, KiDS and the forest line make the
framework's growth and CMB-lensing failures look worse than they are?

No. Once each step is sized, none comes close.
- The largest admissible move toward a pass is 17 % of a gap: WG6's screened run at 100 Mpc, when the N1 correction is
  dropped. For every QUMOND law-alone run it is 9 %.
- The largest admissible move of any kind is 28 %. That is the explicit PS1 linear correction (V2), and it makes the miss
  WORSE.
- Even the most generous non-admissible bound (V5: model-dependent covariance plus 5 % per-bin freedom) leaves the law-alone
  shape chi^2 at 370-399, against a line of 20.09.
- The WG1 shape miss is 14x at L 28 and 0.08x at L 377, a factor of about 175 across the band. Few-percent normalisation,
  Monte Carlo, foreground or distance effects cannot produce that. **"The assumptions don't matter" is the result.**

## Labels

| Failure | Statistic and gap | Largest admissible move | Label |
|---|---|---|---|
| WG2/WG3/WG4 law alone, QUMOND on (canonical; also the alt runs WG2 R1, WG4 R1) | shape chi^2 1572-1594 (alt 1573, 1588) vs 20.09 | V2 +426-446 (27-28 %, WORSENS); toward a pass, V1 -137 (8.8 %) | **PARTIAL as frozen (worsens)**: not an artefact |
| WG2 R0 law off | 1308 | V2 +231 (18 %, worsens); V1 -122 (9.5 %) | ROBUST |
| WG6 screened 100 / 33 Mpc | 260 / 126-137 | V1 -41 (17 %) / -2 to -4 (2-4 %) | ROBUST |
| QX3 iter2 G2 window | mu_min 25,119 vs mu_max 79.4 (2.50 dex) | 0 dex under every variant and bound; Delta chi^2 at mu 79.4 is 1,053-1,324 admissible (bounds 211-739) vs 4 | ROBUST |
| QX3 iter3 closest member | Delta chi^2 92.6 vs 4 | V1 -3.0 (3 %) | ROBUST (V5 bound 31.3, still fails) |
| QX27 G6b closest | 230.9 vs 4 | V2 +10.3 / V1 -2.5 | ROBUST (V5 131) |
| QX15 baryons-only primary | Delta chi^2 +172,848 / +166,612 vs 25 | all CamSpec nuisance freedom 732 (0.4 %) | ROBUST (sized; covariance piece not regraded) |
| KiDS shift lines (QX7, QX10, QX27 G2) | shift 0.15-0.27 vs 0.05 | Sigma_crit/h rescale cancels exactly; radius term <= 0.016-0.028 dex (13-16 %) | ROBUST |
| Forest line (QX3 G4', QX27 G6c, QX7 G4') | lambda_J 492-1024 Mpc vs 0.646 | thermal-history range x3.12 on the line (16-17 % in log) | ROBUST |
| EB1b seeds | no clump collapses before z 0.48 vs QSO1 z 7.05 | no data product enters the failing step | ROBUST |

The "growth" failures and the forest are footing-independent: a0 does not enter at linear order, QX3 assumption A-web.
For CMB lensing, both footings were graded where runs exist, with the same labels.

## Two things the record had not stated

1. **The N1 correction already in the record makes the law-alone misses worse.**
   - The published phi-phi linear correction (M X - F) is in every record grade, through cfg917_lib.pr4_binned.
   - Law-alone models have little C^phiphi at high L', so their true N1 is smaller than the FFP10 N1 that Planck subtracted.
     The corrected prediction for bin 9 (L 377) is therefore NEGATIVE: model/data -0.07, against +0.07 with plain windows.
   - wg6_shape_diag's per-bin row (plain W) is the generous reading. Its shape chi^2 used the corrected rule.
2. **The biggest LCDM-dependent term is large but cancels.** The normalisation's CMB-spectrum response, sum M^XY C^XY, is
   1.9-2.8x the measured bandpowers. At the measured sky (FFP10) it cancels against F_PS1 to 1.3e-4 (K2). Its residual
   reference dependence (V2) moves the statistic away from a pass.

## Checks

- **K1 as frozen: FAIL.** The reference values were wrong; see A1. K1' reproduces the record's FFP10 chi^2 8.863447 exactly.
- **K2 PASS.** PS1 units check, 1.33e-4.
- **K3 bite PASS.** Scaling M by 10 moves the V1 distance from 137 to 1,931.
- **MUTATE twin (every variant = the record rule): reproduces the record.**
  - All wg6_shape_diag rows: per-bin within 5e-3, shape chi^2 within 1.
  - iter2's 26 G2 rows and mu_min 25,119.
  - iter3 92.59 and QX27 230.89.
  - Every shift is 0.

## Not evaluable here

These are not needed at these gap sizes.
- The CamSpec covariance at the model spectrum (P2).
- A raw-P1D forest grade, which needs a framework-native hydro model.
- ACT DR6 lensing, which is not on disk and is not used by any failing lane.

## Disclosure

The first push attempt mis-targeted the shared main checkout: a scratch-directory name clashed with another lane's
worktree. That turned on sparse checkout in the main working tree for a few seconds and merged origin/main
into local main (merge commit 8b87f5ea07). Sparse checkout was disabled at once. Every tracked file was restored (0 deleted, 0 skip-worktree), and
the two pre-existing local modifications (SY1) were untouched. The merge only brought local main up to origin; nothing was
rewritten. The pushed commit carried only FROZEN_CRITERIA.md.
