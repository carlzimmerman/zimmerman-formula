# CFG80 — a ΛCDM comparator for CFG33: is B's SLACS lensing–dynamics gap specific to B?

- **Criteria:** frozen before any script or ΛCDM prediction existed, in `CFG80_FROZEN_CRITERIA.md` (fe0c1c040).
- **Script:** `CFG80_lcdm_slacs.py`, about 9 s. It execs CFG33's pipeline read-only (which in turn execs h53 and reads h9's calibration), plus CFG45's prefix for `halo_mass`, f_b and ρ_c, as CFG69 does.
- **Outputs:** `.out` / `_results.json`, and the `_MUTATE` pair.
- **Runs:** the main run passes 14 of 14 (rc 0). The MUTATE run exits 1 as designed.

**This is a comparator, not a model comparison and not a fit. Nothing here says the data favour B or ΛCDM.**

## Bottom line

**B's gap is SPECIFIC-TO-B.**
- Through CFG33's identical pipeline, a standard ΛCDM halo shows no lensing–dynamics gap: **+0.037 ± 0.103 dex, +0.36σ with the floor (+1.5σ statistical)**. B's gap is +0.15 to +0.17 dex.
- **The gate is not blind to the halo.** With every halo mass × 100, ΛCDM fails it (−0.294 dex, −2.61σ). So the comparison is not NON-DISCRIMINATING.
- **Paired on the same resamples, B's gap exceeds ΛCDM's by +0.12 to +0.14 dex** (7.5–8.1σ, statistical only).
- **What the label means here.** B itself passes CFG33's gate with the 0.10-dex floor (1.5–1.7σ). So "specific to B" is a statement about the statistical gap: the pipeline does not create it for a model with an extended halo.
- **How robust it is.** With the floor, every declared variant passes. Statistically, the lightest-halo variant (every M_h × ⅓) keeps about half of B's gap: +0.075 dex, 3.4σ.

**The mechanism** (R5):
- In ΛCDM the cylinder through the whole halo puts **42%** of the Einstein mass in dark matter inside R_E (median). Inside the 3D sphere r_1/2 the halo is only **12%** of M_JAM/2.
- So ΛCDM's lenses need about 0.82 × Salpeter and its dynamics about 0.76 ×.
- B's phantom adds only 14–20% in projection at R_E (h53). Its lenses therefore need 1.23 × Salpeter, where its dynamics need 0.86 ×.

## Results (α relative to each survey's Salpeter masses)

| | α_lens | α_dyn at the lenses' σ | gap (dex) | z with the floor | z statistical |
|---|---|---|---|---|---|
| B canonical V (CFG33) | 1.23 | 0.86 | +0.159 ± 0.021 | +1.56 | +7.6 |
| B canonical I | 1.27 | 0.86 | +0.171 ± 0.022 | +1.68 | +7.8 |
| B alt V | 1.20 | 0.85 | +0.152 ± 0.022 | +1.49 | +6.9 |
| B alt I | 1.24 | 0.85 | +0.168 ± 0.022 | +1.64 | +7.5 |
| **ΛCDM base** (both footings; V = I by construction) | **0.82** | **0.76** | **+0.037 ± 0.025** | **+0.36** | **+1.5** |
| V1: Dutton–Macciò c | 0.74 | 0.73 | +0.011 ± 0.027 | +0.10 | +0.4 |
| V2: Duffy relaxed | 0.77 | 0.74 | +0.019 ± 0.026 | +0.19 | +0.7 |
| V3: every M_h × ⅓ | 0.95 | 0.80 | +0.075 ± 0.022 | +0.73 | +3.4 |
| V4: every M_h × 3 | 0.68 | 0.73 | −0.033 ± 0.027 | −0.31 | −1.2 |
| base, every M_h × 100 (R6) | 0.29 | 0.58 | −0.294 ± 0.052 | −2.61 | −5.6 |

- **The headline, H1, passes.** ΛCDM passes CFG33's gate: 70 of 70 lenses solved, 187 of 187 calibration galaxies calibrated, |z| = 0.36 ≤ 2.
- **Class:** SPECIFIC-TO-B in all four B cells. Under ΛCDM's statistical-only z (R1) it is also SPECIFIC-TO-B.
- **B − ΛCDM, paired (R2):**

  | cell | B − ΛCDM (dex) | σ |
  |---|---|---|
  | canonical V | +0.122 ± 0.016 | 7.8 |
  | canonical I | +0.135 ± 0.017 | 8.0 |
  | alt V | +0.115 ± 0.015 | 7.5 |
  | alt I | +0.132 ± 0.016 | 8.1 |

  The zero-point floor moves both models' α almost equally, so it is not added here.
- **Slopes (R4).**
  - ΛCDM's α's are flat in dispersion: d log α_dyn / d log σ_e = −0.066 ± 0.079 (B's is +0.204 ± 0.076), and the lens slope is −0.02 (B's is +0.45).
  - In CFG33's bins: at log σ 2.20–2.35, lenses ×0.81 and ATLAS3D ×0.80; at 2.35–2.45, ×0.84 and ×0.76.
- **Diagnostics (R5).**
  - Median halo mass: 10^14.36 for the lenses (range 10^12.51–10^15.50), 10^12.13 for the calibration set.
  - One lens lies above the top of the Moster grid; its M_h is clamped at 10^15.5.
  - No exclusions. `make_nfw`'s inner clip is never active.
- **R7:** truncating the line of sight at 5 R_200 (`make_nfw`'s outer clip) changes the halo's projected mass by at most 3.2 × 10⁻⁴ (|Δκ̄| ≤ 2.0 × 10⁻⁴).

## Controls (all passed in the main run)

- **C1:** CFG33's committed B numbers are reproduced exactly through the exec: its four H2 lines appear verbatim in the committed `.out`, and the JSON deviation is 0. The generic estimator used for ΛCDM reproduces B's differences and bootstrap errors with deviation 0.
- **C2:** M(<R_200c) = M_h to 2 × 10⁻¹⁶. The copied functions are CFG69's source text, and ρ_c(z = 0) is recomputed exactly.
- **C3:** the analytic projected NFW mass matches a direct numerical projection of the 3D density over 177 points. The shell projection agrees to 2.4 × 10⁻¹⁵ and the line-of-sight projection to 5.4 × 10⁻¹³.
- **C4:** the solve residuals are at most 5.2 × 10⁻¹³. With the halo off, the solvers return 1/f_* and M_JAM/M_Salp to 3 × 10⁻¹⁵. The halo only lowers α.
- **C5:** the witness passes (ratio 1).

## MUTATE (every ΛCDM halo mass × 100; B not mutated)

- **Exit code:** rc 1. The failing set is {C5, H1}; the main run's is empty.
  - C5 is the witness and fails by construction.
  - **H1 fails on the science:** the gap goes to −0.294 dex (−2.61σ).
- **C6 passes:** the gate's outcome changes from PASS to FAIL−. So **the control is informative for the headline**, not only for the plumbing. The in-process × 1 run matches the main run's JSON.
- **The gate's sensitivity is weak.**
  - From × ⅓ to × 3 the gap moves only from +0.075 to −0.033 dex, inside the floor.
  - In the MUTATE run, × 33 (V3) still passes (−1.80σ); × 100 fails (−2.61 to −2.96σ); × 300 fails (−3.50σ).
  - So the gate rejects only haloes an order of magnitude or more heavier than Moster's.

## Caveats

- **Untested ingredients.** There is no adiabatic contraction and no SHMR scatter. The concentration relation moves ΛCDM's gap by 0.02–0.03 dex (V1, V2).
- **Halo masses are heavy.** Moster's relation is calibrated on Chabrier-like masses. Tying it to α × Salpeter masses (CFG69's tie) at its steep high-mass end gives group- to cluster-scale haloes for single lenses (median 10^14.4). V3 stands in for a lighter tie. There ΛCDM keeps +0.075 dex: 0.73σ with the floor, 3.4σ statistically.
- **The redshift choice.** The halo is defined at z = 0: ρ_c(z = 0), Duffy without its (1+z) term, and Moster's z = 0 row. The lenses sit at z = 0.06–0.51 (median 0.19; 10–90% 0.12–0.33), while the JAM set is local.
  - A redshift-consistent halo would probably be heavier at fixed stellar mass and less concentrated. That would lower α_lens and move ΛCDM's gap down.
  - This was not computed; the frozen file forbade a scan.
- **Two cosmology conventions** are kept as the committed machineries have them: h = 0.7 for the lens geometry (h53), h = 0.674 for ρ_c (h48). This is a ~4% mismatch in length units.
- **Circularity: none found.** No CFG33 input is derived from a halo mass. ATLAS3D's (M/L)_JAM is read, as h9 and CFG33 read it, as the self-consistent value. That reading was not re-verified against the paper here.
- **Shared by both models:**
  - SDSS aperture dispersions against ATLAS3D's σ_e.
  - Few ATLAS3D galaxies above log σ = 2.45, so the fit extrapolates to the most massive lenses.
  - The 0.10-dex floor.

## Disclosures

- **Before the criteria were frozen:** CFG33's and CFG45's prefixes were exec'd as a plumbing test. That printed B's committed numbers, f_b, ρ_c and the Moster grid's range. The lenses' stellar-mass range was also looked at. No ΛCDM quantity was evaluated.
- **Before the first data run:** the projection helpers and the verbatim copies were unit-tested on synthetic inputs, with no lens or galaxy.
  - The test showed the literal Wright & Brainerd X < 1 expression losing double precision at small X: 2.6 × 10⁻⁵ relative at X = 7 × 10⁻⁵, because the artanh argument tends to 1.
  - For X < 0.5 the script therefore evaluates an algebraically identical, cancellation-free form. It matches a 50-digit evaluation of the literal formula to machine precision. No check, threshold or model choice changed.
- **The committed outputs are the first runs:** main, then MUTATE. No check was added after them, and nothing was re-run.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Corrections after CFG86's independent re-derivation (appended 2026-09-29; no committed number changed)

CFG86 (4d994bb28) re-derived **ΛCDM's side** from independently written code and reproduced it to the last digit: gap +0.0370 ± 0.0247 (+0.36σ with the floor, +1.50σ statistical); median lens halo 10^14.36; V1–V4; the gate at × 100 fails at −2.61σ and at × 33 passes. **B's side was not re-derived.** Its four gaps were taken from CFG33's README, so CFG86's B-minus-ΛCDM test is unpaired.

- **"Specific to B statistically" is conditional, not robust.** CFG86 declared 54 convention cells before running: halo multiplier {1/3, 1, 3} × mass tie {solved Salpeter, solved Chabrier-equivalent, fixed Chabrier-equivalent} × {z = 0, redshift-consistent} × {Duffy, relaxed, Dutton–Macciò}.
  - ΛCDM's statistical gap is inside 2σ in 52% of cells.
  - B minus ΛCDM is above 2σ (unpaired) in 78%.
  - Both hold in 52%. With the floor, ΛCDM passes in 100%.
- **What flips it:**
  - **Lighter halos.** ΛCDM's gap crosses +2σ at a multiplier of about 0.72. At × 1/3 and z = 0 it sits at +0.062 to +0.075 dex (2.6–3.4σ statistical).
  - **A Chabrier-equivalent mass tie at z = 0.**
  - **A Salpeter zero-point offset d between Auger and ATLAS3D.** It shifts ΛCDM's gap by exactly −d. ΛCDM stays inside 2σ only for d in [−0.012, +0.086].
  - **The redshift.** Halos evaluated at the lens redshifts (median z ≈ 0.19) move ΛCDM's gap to −0.020. Redshift consistency should be a frozen, declared variant.
- **The robust statement.** Over all 54 cells, B minus ΛCDM has a median of +0.118 dex and a range of +0.023 to +0.266, and never goes negative. **B sits about 0.12 dex above ΛCDM: a difference between the models, not a failure of either.**
- **What the gap measures.** With halos off, the gap is +0.191 dex (9.6σ statistical). B's +0.15–0.17 lies between that stars-only gap and ΛCDM's base. So the lensing–dynamics gap tracks how much projected dark mass a model has inside the Einstein radius. B's phantom is about 14–20% of the Einstein mass in projection, against ΛCDM's 42%.
- **The class, reworded.** "SPECIFIC-TO-B for the statistical gap" becomes: **B minus ΛCDM ≈ 0.12 dex, conditional on the halo and zero-point conventions.** Both models pass CFG33's gate with its floor.


## Notes after the independent re-run (appended 2026-09-29; no result changed)

- LEDGER_VERIFICATION Part 5 (84910a506, at HEAD 4fa9f54e3) re-ran both modes; both reproduce.
- **Which checks the MUTATE changes:** the MUTATE exits 1 through the construction witness C5, so its exit code says nothing about the science. The science change is H1 (ΛCDM's gap goes to −0.294, FAIL−), together with C6 (the gate outcome changes).
