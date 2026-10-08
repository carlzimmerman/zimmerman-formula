# AUDIT 2026-10-08: data handling, inherited assumptions and scope of the 10-07/08 lanes

This is a read-only audit. No audited lane file was edited. The check scripts are in this folder (`a1`–`a5`, each with `.out` and `.json`). No downloads were made. κ = ½ is FITTED. Both footings are reported and never pooled. No dark-matter particle is added, and the cold fluid's mass is still required.

**Bottom line.** The PM growth lanes and PAPER45 v2 handle their data correctly:
- Every run is divided by an S0 with identical initial conditions. The z_i spectra agree exactly (ratio − 1 = 0), and the metadata matches.
- All 29 headline max|P−1| values reproduce from the JSON.

PAPER45's numbers stand. Its wording overstates two things: the "only inputs", and what the control is (see issue 4).

The one verdict that changes on its own rule is **CFG429**. On the corrected T15 ledger, all four group/cluster rows become feasible at λ = 1. Its MW-30 row also mixes two M_b conventions. A forward note already marks CFG429 as superseded (dc742f798). This audit adds the numbers and the MW-30 convention problem.

The gas-shape exclusion in CFG432 survives every X-COP mass template and a rising bias. One escape route in CFG434 (reading II, "over-built growth") is not available under the growth rule the record has adopted.

## Table

Scope codes:
- **B** = candidate B's rule as the record states it (switch off outside bound halos, conserved cold fluid).
- **B-rdg** = one bookkeeping reading of B, imposed by hand and not derived from an action.
- **chassis** = the ungated law.
- **rdg** = a narrower sub-reading.

| lane | data handling | hidden / inherited assumptions (bias direction; verdict robust?) | scope | action |
|---|---|---|---|---|
| CFG414 (x=0.4, 512³) | OK. Same-seed S0, z_i identical (a1). Alt margin is +0.0004 to the 0.10 cut. The 256³ seed scatter of max\|P−1\| is about 4.5% (alt), i.e. ±0.0045 at 0.10, so this is inside seed noise. | EH-ΛCDM ICs; ΛCDM Δ_ta; pass judged against the ΛCDM-equivalent S0 (neutral). Y (already labelled knife-edge and DIAGNOSTIC) | B-rdg (hand-set x) | none |
| CFG416 (census edge, 512³) | OK (a1). Alt is over the cut by 0.0009, inside seed noise ±0.0045. C2 unit-constant mismatch 1.2e-4 is harmless. | as CFG414, plus census f_ret from ΛCDM-era retention data (pushes the edge outward). Y (verdict = "at the cut") | B-rdg | none |
| CFG419 (DE branch, 512³) | OK. Same-seed S0. The DE vs FLAT difference of 0.0006 is seed-paired, so it is a real null. | as CFG416; DE w(z) from DESI. Y | B-rdg | none |
| CFG422 (seeds × footings, 256³) | OK. S0 per seed: 359 → CFG359, 360/361 → CFG411. All six pairs have identical z_i (a1). A seed mismatch would cost 0.26–0.41 in max\|P−1\|, so the pairing matters, and it is right. | as CFG414. Y | B-rdg | none |
| CFG423 (mass-conserving edge) | OK (a1). | f_b from Planck ΛCDM; R_c Gaussian catchment hand-set (disclosed). Y | B-rdg | none |
| CFG424 (zero-knob) | OK (a1). Overdraw 0; source sum about 4e-4. | Catchment = turnaround sphere from a ΛCDM spherical-collapse ODE; halo finder (connected components); EH ICs; the cold fluid moved only as source weight. The compensation rule itself carries the pass (MUTATE no-comp 0.154). Bias: toward pass by construction on scales above r_ta, though k ≤ 1 is not blind to it (P@1 = 1.004 vs 1.120 for no-comp). Y | B-rdg | wording (issue 4) |
| CFG425 (seeds + 512³) | OK (a1). R3 is paired with the 512³ S0 at NSEED 512, the same IC. | as CFG424. Y | B-rdg | none |
| CFG426 (DE + alt seeds) | OK (a1). Alt is divided by the canonical S0, which is legitimate: S0 skips every a₀ path (cfg424_pm.py line 376), and the background cosmology is footing-independent. | as CFG424. Y | B-rdg | none |
| CFG427 (ε, filter) | OK (a1). The ε runs agree to 4 decimals (switch inert under mass conservation, README checked ≤ 0.03%). | as CFG424. Y | B-rdg | none |
| CFG439 (alt + DE, 512³) | OK (a1). README rounds the DE value 0.03345 to "0.034"; PAPER45's 0.033 is right (a5). | as CFG424. Y | B-rdg | README rounding (trivial) |
| CFG428 (one Bose field) | OK at order-of-magnitude level. T2 is off by about 31 dex, T3 by about 3,000×. | Bullet σ/m < 1 cm²/g (from ΛCDM-SIDM merger modelling); Bose enhancement 2–16. Bias: neutral to mild. Y (margins dwarf any re-calibration) | rdg (CFG383's one-field split) | none |
| CFG429 (λ = 1 t_dyn) | **ISSUE.** (i) Group/cluster rows use def-A x_A instead of T15's own x (CFG453). Re-scored on x_T15, all 4 rows are **feasible** (clusters b=0 +0.14 at 1.2e-10, +0.78 canonical, +0.30 alt). (ii) The MW-30 row hard-codes x = 1.8 (M_b = 1e11) but computes S at M_b = 7e10. With one consistent M_b, the V200 row is feasible at 7e10 (+0.13 / +0.52 / +0.23) and negative at 1e11 (a2). Under its own "all rows negative" rule the verdict becomes **NOT EXCLUDED**. | T15 ledger: a₀ = 1.2e-10 (neither footing), τ = 10.3 Gyr, ρ₅₀₀ defined on ρ_crit (ΛCDM convention), hydrostatic b constant, group M* placeholder. N | B-rdg (T15 settling ledger) | forward note exists (dc742f798); a committed re-run should use a2's rows and fix the MW M_b convention |
| CFG430 (h_c at y = 1) | OK. The C5 mesh statement (y never ≥ 0.03 at 256³) is a resolution fact, correctly read as "cannot test". | kernel-Bose dictionary D1, integer cap n_max = 4. Y (CONDITIONAL already says it hinges on these) | rdg (kernel-Bose) | none |
| CFG431 (clock universality) | **ISSUE (known).** R2 read X-COP RADIUS (units R/R500) as Mpc, so R2 is invalid (CFG450). On JSON R500, z = 2.17; with the full alt footing, z = 1.95, CONSISTENT. So NOT UNIVERSAL holds on the canonical footing only. The README still carries the wrong R2 premise. | Constant hydrostatic b decides the verdict (b = 0.1 → no group clock); group M* = 0.10 M_gas; galaxy kernel √(1+1/y) ≠ ν_mono. Bias: either way. N (labelled FRAGILE) | B-rdg (T14 clock) | add a forward note to the CFG431 README pointing to CFG450 |
| CFG432 (X-COP M_u shape) | OK. Units are right (RADIUS in R/R500 for the fgas files, kpc for the hydro files). The a4 baseline reproduces CFG432's 0.10 M_gas row (−0.568). | M_FORW comes from a parametric pressure model (ΛCDM-calibrated shape); constant b; spherical. **a4:** gas tracking EXCLUDED in 30/30 rows (M_FORW, NFW, Einasto, isothermal, Burkert × b = 0, 0.3, and a rising b(r) 0.05 → 0.30 × both footings). The weakest row is rising b with M_FORW, at 3.6σ. The NFW-shaped half depends on c₂₀₀ (disclosed). Y for the gas exclusion; N for "NFW-shaped" | B (shape of B's unsettled mass) | none; optionally cite a4 as template robustness |
| CFG433 (MW satellites) | OK. Table 2 is parsed from the arXiv tex, and C1 confirms 39/39 rows. The estimator is correct for total tangential speed with error variance subtracted. | Jeans equilibrium (Fritz: pericentre excess, which biases V_c high); γ from an incomplete satellite census (biases V_c high); LMC group; M_b 6e10 with no hot CGM (biases V_pred low). All push D up, i.e. against T13. Y (NON-DIAGNOSTIC; the sign is robust) | rdg (T13 phantom-alone), not B | none |
| CFG434 (void lensing) | OK. b_Vg values match the paper's table. Gaussian in 1/b_Vg is defensible: the paper fits 1/b_Vg linearly. That choice decides DISF (2.9σ) vs EXCL (5.2σ). | β = f/b = 0.37 and f = Ω^0.55 (ΛCDM/GR); R_sel from ΛCDM HOD sims. For reading I these are self-consistent with B's ΛCDM-like growth. **Reading II's escape** ("borderline if clumped growth is over-built by ≥ 25%", via T5's +21–26%) is not available under the adopted zero-knob rule (σ₈ ≤ +0.54%, phantom compensated per catchment; a5). Y for I; for II, DISFAVOURED is firmer than the README says | B (reservoir readings I/II) | add a note that the T5 escape is not the adopted growth rule |
| CFG436 (CHEX-MATE z-slope) | OK. NOT POSSIBLE is correct. The λ windows in the prediction table are T16's, which CFG453 withdrew. The ratio moves < 1.3% over them (a5). | Constant b_SZ, self-similar M_SZ, model f_gas (BFC). The README already flags all of these as the wall. Y | B-rdg (T16 settling) | relabel the λ column as "illustrative" (low) |
| CFG437 (BX442 published) | OK. Numbers match the Law+12 PDF (M* 6+2−1e10, M_gas 2e10, V 234+49−29 at 8 kpc, σ 71 ± 1). The point-mass g_N is within 2% of a thin Freeman disc at 2.7 R_d (a3). | Gas from a locally calibrated Schmidt–Kennicutt inversion (likely LOW at z ~ 2, which biases implied a₀ HIGH, toward H(z): doubling gas moves reading A ×5 and B ×1.6); Chabrier SED M*; asymmetric-drift form (2σ²R/R_d vs σ²R/R_d moves B by ×1.8). Y (NOT DIAGNOSTIC either way) | B (a₀(z) law) | none |
| CFG438 (OSIRIS DRP) | OK. Frozen NOT VALIDATED stands. The unexplained systemic offset of 80–100 km/s blue matches the air-vs-vacuum Hα difference, −82.7 km/s (a5), if Law+12's z used the air rest wavelength. This is a candidate cause, not verified, and it does not touch V_rot or σ. | none affecting the verdict. Y | data lane (no a₀ claim) | check the Law+12 wavelength convention before any reuse of the systemic velocity |
| CFG358 (zero-field N=2047) | OK. The frozen verdict rests on Δ₃ = 0.0064 against the 0.005 guard (a knife-edge, disclosed). | 1-D, law on in the open FRW background. Y as a chassis statement | **chassis only** (README fixed 10-08) | none |
| CFG461 (settling temperature) | OK. Controls K1–K4 reproduce. κc/4 = c/8 = 37,474 km/s checks. | Spherical, static, Newtonian except where the law enters; C4 is an EdS toy on a ΛCDM background. The c-test is dimensional (σ⁴ ∝ c at fixed ρ_Λ), so it does not depend on these. Y | B-rdg (PAPER45 v2's SIS settling) | none |
| SCAN cosmic supply | OK. The arithmetic re-checks. Minor: Ω_m = 1 − Ω_Λ (0.3153) vs Ω_b + Ω_c (0.3138), a 0.5% difference; the `.out` is written to the cwd, not the script directory. | Epoch test assumes flat a₀. With a₀ tracking ρ_DE the conclusion is the same, since ρ_DE is near-constant while y_H ∝ (1+z)³/E. Y | numerology note | none |
| PAPER45 v2 | Numbers: 19/19 audit rows pass on re-run, and every value matches a1. | (a) "only inputs κ and f_b": the rule also inherits the ΛCDM spherical-collapse Δ_ta(z) that sets each catchment, the halo finder, EH-ΛCDM ICs, and CFG361's cut. (b) The "Newtonian control" is the ΛCDM-equivalent N-body run (the cold fluid as CDM particles), so a pass means "matches ΛCDM growth to 10%". (c) "does not grow toward the limit": it does grow, 0.027 → 0.033, from two resolutions and one 512³ seed, while the catchment draw rises 30% → 57%, toward overdraw. Y (the numbers); wording overstates | B-rdg | wording fixes at next version (issue 4) |

## Real issues, ranked

1. **CFG429 verdict reverses on its own rule** (a2). The group/cluster rows used def-A deficits, which is CFG453's units mismatch. On T15's own x, all 4 rows are feasible at λ = 1 on every a₀. The MW-30 row is the only remaining exclusion, and it mixes M_b = 1e11 (in x) with 7e10 (in S). With one M_b it is feasible at V = 200 for 7e10 and negative for 1e11. The forward note (dc742f798) already stops citation. The re-run must fix the MW M_b convention too: this is new beyond that note.
2. **CFG431's R2 row is invalid, and NOT UNIVERSAL is canonical-only.** This was found by CFG450, but the CFG431 README still states the wrong "gas at 1 Mpc" premise. It needs a forward note.
3. **CFG434 reading II.** The README's "borderline" escape needs ≥ +25% clumped amplitude (T5). The record's adopted zero-knob rule gives ≤ 0.54% in σ₈ and compensates the phantom, so the escape is not available under B as now modelled. Reading II smooth stays DISFAVOURED (2.9σ; 5.2σ under the Gaussian-in-b_Vg error model). This weakens B's reading II; it does not weaken PAPER45.
4. **PAPER45 v2 wording (weakens the note's framing, not its numbers).**
   - "The rule's only inputs are κ and f_b" omits inherited structural inputs: the ΛCDM Δ_ta(z) catchment, the halo finder, the EH ICs and the cut.
   - The "Newtonian control" should be called the ΛCDM-equivalent control (cold fluid as CDM particles, same ICs).
   - "does not grow toward the limit" should read "grows slowly (0.027 → 0.033; two resolutions, one 512³ seed)". The rising catchment draw (57%) should be named as a possible overdraw at 1024³.
   - The pass is carried by the compensation (MUTATE 0.154), which is imposed bookkeeping. The note already says this. Nothing here changes a number.
5. **Knife-edges inside seed noise** (CFG414 alt +0.0004, CFG416 alt −0.0009). The 256³ seed scatter of max|P−1| is about 2–4.5% relative, i.e. ±0.002–0.0045 at 0.10. Both 512³ census/hand-set results are "at the cut" and indistinguishable from each other. The lanes already say so; PAPER45 should not read 0.0996 as a pass and 0.1009 as a fail.
6. **CFG437 inherited gas mass.** The Schmidt–Kennicutt inversion is the dominant systematic (×5 on reading A). It biases the published-input implied a₀ toward the H(z) rival. NOT DIAGNOSTIC stands.
7. **Low:**
   - CFG436's λ labels are stale (T16 window withdrawn);
   - CFG439 README rounding (0.034 should be 0.033);
   - CFG438 systemic offset = air/vacuum candidate;
   - SCAN Ω_m convention and cwd output path.

**Checked and found clean:**
- PM S0 pairing for all 29 runs: same seed, same NSEED at 512³, identical z_i P(k), matching metadata.
- The alt footing against the canonical S0 is legitimate: S0 never touches a₀, and the background is footing-independent.
- X-COP units in CFG432/450/453.
- Fritz+18 parse (CFG433).
- UNIONS b_Vg transcription (CFG434).
- Law+12 transcription (CFG437).
- The PAPER45 audit re-runs 19/19.
- CFG432's gas exclusion is template- and bias-profile-robust (a4).

## Files
- `a1_pm_baseline_pairing.py`: z_i identity and z₀ re-derivation for 29 PM run/S0 pairs, plus the seed-mismatch cost.
- `a2_cfg429_rescore.py`: CFG429 on T15's own x, at three a₀ values, with the MW-30 M_b conventions.
- `a3_cfg437_baryon_geometry.py`: BX442 g_N geometry (point, sphere, Freeman), doubled gas, two asymmetric-drift forms.
- `a4_cfg432_mass_template.py`: gas-tracking slope across five X-COP mass models × three bias profiles × two footings.
- `a5_misc_checks.py`: CFG438 air/vacuum, CFG434 escape vs zero-knob growth, CFG436 λ spread, CFG439 rounding.
