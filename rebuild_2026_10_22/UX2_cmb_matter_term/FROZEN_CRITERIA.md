# UX2_cmb_matter_term: FROZEN CRITERIA (committed alone, before any UX2 script or number)

**Question.** With the a0 law absent from linear FRW and the cold sector retired by the owner, what can supply the CMB's dust-like term and the matter term? (1) How does published AeST (Skordis and Zlosnik, arXiv:2007.00082) grade against the twelve requirements in `REQUIREMENTS_2026-11-01/REQUIREMENTS_LIST.md`? (2) What must any replacement deliver?

kappa = 1/2 FITTED. Both a0 footings reported, never pooled. No dark matter particle. The cold sector stays retired; no result here reinstates it. Not theory closed. Nothing here says the data favour the framework. No LCDM input or yardstick.

**Not blind. Read before freezing:** PAPER67 sections 5-7; RF5 README, criteria and results (including the omega_c, h and chi2 surface); REQUIREMENTS_LIST; CFG689 README; C2, C7 READMEs and provenance (including C7's benchmark table); H1, H2, M1 README openings. Their numbers are inputs, and I know them.

## Part 1: row-by-row grade

**Object graded.** The published theory only: SZ21's action, its K and F families, at published configurations. PC1 = SZ21 Cosh benchmark (K_B 0.5, lambda_s infinite). PC2 = SZ21 Exp benchmark (K_B 0.1, lambda_s infinite). PC3 = the published finite lambda_s values in Verwayen et al. 2304.05134 (1, 2, 10). The record's capped F and v4/v9 are EMBEDDINGS: reported in a separate column, and never counted as the published theory.

**Each row gets two tags.**
- Status: COMPUTED-HERE, COMPUTED-RECORD (a record lane computed it on published equations, file named), SOURCED (stated in a paper, location named; web read adds PROVISIONAL), UNKNOWN.
- Reading: HOLDS, FAILS, CONDITIONAL (depends on a free function or an unsettled premise, named), NOT GRADED. NOT GRADED is not a pass. Where no frozen line exists, the row uses the line FG1 or the requirements file uses; if there is none, the reading is NOT GRADED and the number is reported.

**One-configuration rule.** Rows only count together if they hold at one configuration. A row held at PC1 and another held at PC2 are not a joint pass.

**g rule.** Both readings are reported for the CMB row: g = 1 (the paper's convention) and physical g = (1 - K_B/2) lambda_s/(1 + lambda_s). Which applies is stated as a premise, not chosen by outcome.

**Row 11 gates (RF5's, absolute).** plik-lite chi2 p >= 1e-3 on dof 605; BAO p >= 1e-3 on 13; SN p >= 1e-3 on n - 1. Benchmarks are run with C7's patched CLASS at C7's best fits, and with constant dark energy, the published theory's own -2 Lambda. BBN line from record: g > 0.9611 (A78), reported as a separate gate. The dust abundance is counted as FITTED.

**Overall label (exactly one).**
- `PASSES ALL TWELVE AT ONE CONFIGURATION`
- `FAILS AT NAMED ROWS AT EVERY PUBLISHED CONFIGURATION`: at least one row FAILS at each of PC1, PC2, PC3
- `NOT SETTLED`: a failure is not shown at every configuration; list open rows per configuration

A free function that could change a row is named, not scanned.

## Part 2: what a replacement must deliver

**P2a, read from RF5.** For each RF5 window cell, canonical and alt read-offs: omega_x (RF5's omega_c), omega_b, ratio omega_x/omega_b as this fit's own result, rho_x(z) in physical units at z = 0, z_eq, z_star, z_drag and z_on, relative to baryons and rho_DE. Reported as the fitted value and spread across the window. Window = RF5's frozen one; the upper edge is a grid edge, and the forest pointer stays a pointer.

**P2b, new CLASS scan: how dust-like.** Vanilla CLASS (`rf5_class_build` or `class_public` build, whichever is the plain one; read-only binary) with a fluid x in place of the cold component, a small residual omega_cdm only if CLASS needs it for gauge. Dark energy constant, because the fluid slot is taken: stated as a limit of this scan.
- Grid, frozen: w_x in {0, +1e-3, -1e-3, +3e-3, -3e-3, +1e-2, -1e-2} at c_s^2 = 0; c_s^2 in {1e-6, 1e-5, 1e-4} at w_x = 0; control omega_x = 5e-4 (RF5's floor), no dust-like term.
- Fit per cell: omega_b, omega_x, 100theta_s, lnA, n_s, tau, A_planck on plik-lite + low-ell + A prior, Gauss-Newton, stop |dchi2| < 0.1 or 10 steps.
- Pass line per cell: plik p >= 1e-3 and (plik + A prior) - min over this scan <= 25, RF5's line. BAO and SN evaluated, not steered: same gates. Unconverged or crashed = UNDETERMINED with the error.
- If the fluid cannot be made to run, P2b is UNDETERMINED; no other family is substituted.

**P2c, read from CFG689.** What the late-time matter term has to be: the band's dependence on omega_m and the conservation brackets (B4m, B4p). Reported with the a0(0) and a0(2.33) both footings from RF5 cells. The r_d circularity is stated: CFG689's ruler assumes the pre-switch cold term.

**Label for part 2:** `REQUIREMENT STATED` if P2a and P2c read and P2b runs at least the w grid; else `REQUIREMENT PARTLY STATED`, naming what is missing. Stated as a requirement on the families run, not a theorem.

## Checks
- K1: P2a hand-check, rho_crit conversion and one rho_x(z) against independent arithmetic to 1e-6.
- K2: fluid w_x = 0, c_s^2 = 0 against CDM at the same parameters: plik chi2 differs by <= 0.5. Failure voids P2b.
- K3: every number in the README's requirement rows is checked against its named file by `check_ux2.py`.
- K4: scripts rerun byte-identically, with fits read from a checkpoint.
- MUTATE twin (`UX2_MUTATE=1`, separate outputs): density exponent -2.9 in place of -3 and plik sign flipped. K1 and K2 must fail. If it doesn't fail, the lane reports that.

## Compute and rules
One thread, nice 15, under 4 GB, preemptible with checkpoints per cell. No downloads. Web reading tagged PROVISIONAL. Failed checks published under these labels. Commit only this directory; no push.
