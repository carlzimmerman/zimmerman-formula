# CFG160 — KURVS a₀(z) under the simulation-calibrated pressure-support factor of Kretschmer et al. 2021 (P4)

- **Criteria:** frozen in `CFG160_FROZEN_CRITERIA.md` (ae252ceb6), before any number under this prescription was computed. CFG141's P0, P2 and P3 results were known; the prescription and every free choice were fixed there.
- **Script:** `CFG160_kurvs_kretschmer.py`; under a second. It runs CFG141's pipeline read-only, and that pipeline runs CFG140's.
- **Runs:**
  - The main run passes both controls and the headline H1 and exits 0. The reported H2 fails.
  - The MUTATE run (velocities × 2) fails H1 and exits 1, so the control is informative.

## Bottom line

**At the pre-declared decision cell, the rival a₀ ∝ H(z) fits and the framework's flat a₀ is 3.3σ high. By the frozen map this is a Kretschmer-conditional lean toward a₀ ∝ H(z) at z ≈ 1.5. It is not robust: it flips at higher gas and weakens within the calibration's own scatter.**

| decision cell: μ = 0.67 (the paper's 40% molecular), δ = 0, canonical | Δ′_flat | Δ′_H |
|---|---|---|
| **P4, Kretschmer et al. 2021 α (primary)** | **+0.144 ± 0.044 (+3.3σ)** | **−0.006 ± 0.044 (−0.1σ)** |
| P4, α × 0.6 (the fit's 40% scatter, low end) | +0.058 ± 0.045 (+1.3σ) | −0.092 ± 0.046 (−2.0σ) |
| P4, α × 1.4 (high end) | +0.211 ± 0.046 (+4.6σ) | +0.060 ± 0.045 (+1.3σ) |
| P4, R_e = 2 R_eff (the mass model's gas scale) | +0.066 ± 0.046 (+1.4σ) | −0.084 ± 0.047 (−1.8σ) |
| P2, CFG141 (self-gravitating layer) | +0.390 ± 0.065 (+6.0σ) | +0.237 ± 0.063 (+3.7σ) |

- **The gas decides the lean.** The P4 grid over the gas bracket, canonical footing, δ = 0, gives Δ′_flat / Δ′_H:

  | μ | Δ′_flat / Δ′_H |
  |---|---|
  | 0.25 | +0.204 / +0.051 |
  | **0.67** | **+0.144 / −0.006** |
  | 1.5 | +0.053 / −0.092 |
  | 4 | −0.123 / −0.255 |

  The errors are about 0.044 dex.
  - At the paper's molecular-only gas the rival fits and flat does not.
  - At μ = 1.5, i.e. molecular gas plus a comparable HI reservoir, flat fits (+1.2σ) and the rival is at −2.1σ.
  - At μ = 4 both over-predict.
- **Across the whole grid,** the frozen H1 passes: flat is disfavoured in 14 of 24 cells, not in all of them. H2 fails: the rival is disfavoured in 10 of 24 and within 2σ in 14.
- **Why P4 differs from P2.** Kretschmer et al.'s α at KURVS's outer radii (x = R/R_e − 1 = 1.0–3.5) is 2.6–3.9. P2's 2R/R_d is 6.9–15.2. So the pressure correction to V_c² is 1.2–2.5 times the observed V² under P4, against 1.5–6.1 under P2 (R3).
- **What it means.** P4 is a pressure correction calibrated on simulated high-redshift discs and adopted as published. Under it, the KURVS outer accelerations at the paper's own gas estimate follow a₀ ∝ H(z) and not a flat a₀.
  - Hold that with its conditions: one simulation suite (VELA, with dominant spheroids), a 40% scatter, and gas that is unmeasured.
  - A total gas mass of about 1.5 M*, or a correction factor 0.6 times Kretschmer's, would remove the lean.

## Controls

- **C1:** with α set to P2's 2R/R_d, the P4 code path reproduces CFG141's committed P2 grid to 1.7 × 10⁻¹⁶ (24 cells × 4 quantities).
- **C2:** α(0) = 1.475, α(1) = 2.533 and α(4) = 3.955, from Kretschmer et al.'s Table 1 (gas, disc).
- **R0 (power):** the two readings are 2.6–3.7σ apart per cell.
- **MUTATE (velocities × 2):** flat a₀ is disfavoured in every cell, so H1 fails and the run exits 1.

## Per galaxy (R3; central cell, unanchored)

- x runs from 1.04 to 3.54, and α from 2.57 to 3.91.
- V_c²/V² is 1.19–2.52 under P4, against 1.50–6.06 under P2.
- Δ_flat runs from −0.11 (KURVS-8) to +0.48 (KURVS-17), and Δ_H from −0.28 to +0.33.
- The three largest residuals are KURVS 13, 17 and 21. These have the largest x, where α is near its fitted range's edge.

## Readings (as frozen)

- **The declared reading at the decision cell:** a Kretschmer-conditional lean toward a₀ ∝ H(z), with the gas unmeasured.
- **This is the first in-regime reading in this record whose central value favours the rival over the framework's flat a₀.** It is conditional three times over:
  1. on the VELA calibration of the outer pressure support;
  2. on its scatter (at α × 0.6 the cell is non-diagnostic, and slightly flat-favouring);
  3. on the total gas (at μ = 1.5 the lean flips to flat).
- **Taken with CFG142:** its one powered disc, KURVS-11, shows dust-traced gas below 0.72 M* (point-source approximation). That leans the same way, toward low molecular gas, if the HI is small. It is one galaxy, and its limit is approximate.
- **It is not a kill line.** CFG140's frozen map sets the kill at "flat disfavoured beyond 3σ in every cell". Under P4 flat survives in 6 of 24 cells, and at the rival's expense in 10.

## Disclosures

- **Every free choice was fixed in the spec before any P4 number:**
  - the primary R_e (the paper's R_eff, the Hα tracer's scale);
  - the R_e variant;
  - the clipping of x to the fitted range [0, 4];
  - the SPARC anchor treatment;
  - the decision cell.
- **σ_out** is the observed line-of-sight dispersion, used as σ_r under isotropy, as in P2.
- **Kretschmer et al.'s Table 1** was read from the arXiv HTML rendering through a summarising fetch that returned its rows and caption verbatim. The coefficients match the abstract's "α ≈ 1 at R_e to 4 at 5 R_e" within the fit's 40% scatter.

## Untested (declared)

- whether VELA's α applies to KURVS's rotation-supported discs;
- anisotropy (σ_R ≠ σ_z);
- the Hα tracer's true half-mass radius;
- beam smearing of the observed outer σ;
- non-equilibrium;
- the gas;
- the COSMOS half of KURVS;
- Dalcanton & Stilp's (2010) prescription.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Governing wording (appended 2026-09-29, the orchestrator's check; the text above is unchanged)

- **Read the Bottom line and Readings above in this sense:** Under the simulation-calibrated (Kretschmer+2021) pressure correction, the pre-declared decision cell (μ = 0.67) leans toward a₀ ∝ H(z) at 3.3σ. It is conditional, not robust and not a kill: it flips with gas (at μ = 1.5 flat is +1.2σ and the rival −2.1σ); it moves within the calibration's 40% scatter (α × 0.6 is non-diagnostic); and it rests on ONE published calibration, adopted after CFG141's P2 result was known (a forking-path risk). The GOODS-ALMA limit (μ < 0.72 nominal) is a point-source approximation, and no total gas is measured. The decisive quantities are the outer pressure support at 2–4.5 R_e and the total cold gas. The decision cell was fixed with the CFG141 grid already known. At that cell a confirming result for flat a₀ would have been Δ′_flat within 2σ with Δ′_H below −2σ (for example α × 0.6 gives +1.3σ / −2.0σ); a disconfirming result is Δ′_H within 2σ with Δ′_flat above +2σ, which is what occurred; anything else is non-diagnostic. Nothing here is evidence against flat a₀ beyond this statement. CFG140's and CFG141's rows are not superseded: they stand as the P1 and P2 results. An independent re-derivation (CFG165, the Opus chat) is pending, and this wording holds until it reports.
- **The phrase 'the first in-regime reading in this record whose central value favours the rival' is descriptive only.** It adds nothing to the statement above.

## Corrections after CFG165's independent re-derivation (appended 2026-09-29; the text above is unchanged)

- **Headline: a weak, normalisation-dependent lean; not a detection.** CFG165 (33b446ef3), the Opus chat's independent re-derivation, reproduces CFG160's decision cell (flat +0.147 ± 0.044, rival −0.003 ± 0.045; the 0.003 gap is inc_sfr_deg against inc_star_deg) and every sensitivity row, and corrects how the lean reads. (a) 'The first in-regime reading favouring the rival' does not survive on CFG160's own map: P3 at the same cell already reads lean rival (CFG141's committed values: flat +3.5σ, rival +1.3σ), and P3 is lean rival in 12 of 24 cells against P4's 14 (both counts checked here from the committed JSONs). The accurate statement is that P4's rival central value sits at zero. (b) The lean depends on the normalisation, not the α shape: all 8 alternative shapes with median α within ×[0.75, 1.25] keep lean rival; flat's Δ′ drops below +2σ at s = 0.71, and the class flips to lean flat by R_e/R_eff = 3 (CFG165). (c) Break-even total gas: μ = 2.14 for flat and 0.65 for the rival. The lean holds only below about 1.2 M*, and at the repo's total-gas median (μ ~ 4) both laws over-predict (CFG165). (d) x runs from 1.04 to 3.54, inside the calibration range. The README's 'the three largest residuals (KURVS 13, 17, 21) have the largest x' is wrong: the largest x are KURVS 21, 8 and 17 (checked here), and KURVS-8 has the lowest residual. (e) With gas and α as nuisance parameters the likelihood ratio falls from about 130 to 0.5–1.7, and P(lean rival | flat true) is 0.31–0.45, against a frozen requirement below 0.05: weak evidence, not a detection (CFG165). (f) KROSS through the same P4 pipeline, anchor-corrected at μ = 0.67: flat −0.004, rival −0.082 (−4.1σ), the opposite of KURVS; KURVS − KROSS = +0.151 ± 0.045 (CFG165), reproduced by CFG161 (9ff8e369a: +0.148 ± 0.044, 3.3σ from flat, 1.7σ from the rival; CFG161's outcome was not blind). (g) CFG165's independence stops at CFG4_common, CFG140's set-up choices, and Kretschmer's α(x) as quoted (unverified literature); its MUTATE M6 (σ_out permuted) did not bite and is kept.

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.
