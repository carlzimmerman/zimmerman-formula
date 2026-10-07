# CFG401 FROZEN CRITERIA: CFG400 with a two-component baryon SHAPE (stars + an extended gas disc). Do the six galaxies agree on a0 first?

Committed alone, before any script. kappa = 1/2 FITTED. No dark-matter particle species: the cold MASS is still required and is kept.
No knob scans. Never "the data favour the framework". Owner (2026-10-06): "keep going ultrathink".

**Why.** CFG400 was invalid: per-galaxy a0 spread over 3+ dex because the stars-only exponential shape cannot make the outer slopes
(about -1) that four of six galaxies show. At z ~ 2 gas is 40-70% of the baryons and is typically more extended than the stars.

## Shape (declared, no fit)
- Stars: exponential disc with R_1/2 (Table 1) plus a 1-kpc bulge with Table 1 B/T, as CFG400.
- Gas: exponential disc with scale length 2 x the stellar R_d (the record's convention, CFG140 "stars R_d, gas 2 R_d").
- Gas fraction from the Table 1 PRIORS: f_gas = 1 - M*/Mbaryon. COS4 01351 0.40; D3a 6397 0.48; GS4 43501 0.45; zC 406690 0.70;
  zC 400569 0.52; D3a 15504 0.45.
- One overall per-galaxy normalisation f_j stays free (self-calibration). The gas/star RATIO is fixed by the priors.
- The beam cut is RAISED to R > PSF FWHM (0.6", conservative) to reduce the smearing that failed CFG400's C2. If a galaxy is left
  with fewer than 4 points it is dropped and reported.

## Gate (decides whether any law comparison is made)
- **G-CONSISTENCY:** each galaxy alone (f_j and a0 free, local-a0 units, grid x0.01-x100). Six per-galaxy best log a0.
  PASS if none is at a grid edge AND the robust spread (16-84%) is <= 0.5 dex. Otherwise: INVALID AGAIN, and Genzel+2017 cannot
  do this test without resolved gas maps. STOP: no law comparison is reported as a result.
- Only if G-CONSISTENCY passes: Delta chi2 (RIVAL - DE) on both footings, with CFG400's SEPARATES / LEANS / NON-DIAGNOSTIC rule.

## Controls
- C1: the two-component shape reduces to CFG400's when f_gas = 0 (identity to 1e-12).
- C2 (reported): vc(R_1/2) digitised vs Table 1, as CFG400 (beam-limited; not a gate).
- MUTATE: gas scale = 1 x R_d (as compact as the stars). The per-galaxy spread must change by > 0.2 dex (rc 1).

Local compute only. No downloads.
