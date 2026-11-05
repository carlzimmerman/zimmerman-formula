# CT17 frozen criteria: G7 (lensing and clusters) for candidate C''

Written before this lane computes any number. Under owner decision D1 and its 2026-11-04 follow-up ("Yes, grade it") and `../CT_GATES_COMMON.md`. Grading only: nothing adopted, the 2026-11-01 retirement stands, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled.

**Not blind.** Before this freeze I read CT4_REPORT.md, CT9's addendum, CT10/CT13 (C'' local a0 shifts), V3S_FINAL_VERDICT, V3_FULL_PICTURE, H2_aest_clusters (README + out), LW1, LE1, X32, DB1. The record numbers below are restated from those files.

## G7 numbers (from CT4, restated)
- R1 X-COP: the plain law has M_HSE/M_law 2.93 canonical / 2.72 alt (LW1 lw1_xcop.out:3,11); the candidate must raise the law's mass inside R500 by a factor in [2.7, 2.9] (CT_GATES_COMMON G7), i.e. its own M_HSE/M_model within [1/1.1, 1.1] of 1 (0.04 dex).
- R2 Bullet: the lensing peaks must sit on the galaxies (~200 kpc from the gas, sign of dkappa positive at the galaxy peaks). The plain law puts them on the gas, 40 / 51 kpc, dkappa negative (X32 README:29; DB1 db1_checks.out:5). PASS iff peak on the galaxies, dkappa > 0.
- R3 KiDS near-lens (R <= 0.3 Mpc): the plain law is short by +0.089 (A1) to +0.116 (G3) dex (LE1 README:97), red lenses x1.313 / x1.200, blue 0.878 / 0.802 (CT4:20). PASS iff the candidate adds +0.089 to +0.116 dex at R <= 0.3 Mpc, carried by red lenses, within 0.02 dex.

## Method (frozen)
1. C'' = v3s with a0^2 = kappa^2 G rho_phi. Check whether anything in C''s static/quasi-static field equations differs from v3s's in a cluster or lens: (a) the local a0 shift (CT13 out:23,27); (b) phi's own energy density inside R500; (c) the dust phase's static branch, which in v3s is the mu_K^2 psi term (V3_FULL_PICTURE.md:47), the same equation as H2's AeST quasi-static system with mu = mu_K <= 0.1 Mpc^-1 (S4 bound).
2. If (a) and (b) are below 1e-3 dex in mass, C'' inherits v3s's rows, read from H2 at mu = 0.1 (the upper end; smaller mu gives less) with its free zero point Delta, and from X32 for the Bullet.
3. The dust amount entering G5 (omega_x fitted) does not enter the static rows; whether it settles in wells is set by v3s's growth record (V3_FULL_PICTURE.md:108). No knob scans: mu_K is taken at its bound, not tuned.
4. Grade each row PASS/FAIL with its gap, both footings. A FAIL is reported as hard as a pass.

Compute: one thread, seconds, well under 1 GB. No download. Commit nothing.
