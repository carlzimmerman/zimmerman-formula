# CFG165 — Referee re-derivation of CFG160 (KURVS a₀(z) under the Kretschmer et al. 2021 pressure-support calibration, P4). FROZEN CRITERIA, PHASE 1

Written 2026-09-29 by the referee agent, before any script of this lane exists and before any CFG165 number is computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure. Failed controls and wrong hand estimates are kept, never repaired.

What I have read (phase 1): `CFG160_FROZEN_CRITERIA.md`, `CFG160_README.md`, `CFG140_README.md`, `CFG141_README.md`, `CFG140_FROZEN_CRITERIA.md`, `CFG141_FROZEN_CRITERIA.md`, the headers/first rows of the data CSVs named in section 1, and file NAMES only in the lane directory. I have NOT opened any CFG140/141/160 script (`.py`), `.out` or `.json`. In phase 2 those may be opened only after my own main and MUTATE runs are saved.

**Status of every README number quoted below:** it is a TARGET I read, not a blind prediction. My hand estimates in section 3 were built by rescaling CFG141's published per-galaxy P2 table (V_c²/V², Δ_flat, Δ_H, R_max/R_d) with the Kretschmer α(x); they are a consistency check of the README, not an independent prediction. The independent content of this lane is the code in phase 2.

## 1. What is re-derived, how independence works, where it STOPS

**Re-derived (own code, written from the frozen text alone):**
- the whole KURVS chain: sample selection (10 rotation-supported IDs 3, 7, 8, 9, 11, 13, 15, 16, 17, 21 from `kurvs2023_fdm.csv`), R_max and v_last, R_d = R_eff/1.68, thin-exponential-disc baryon model (stars y = R/R_d, gas y = R/(2R_d), M(<R) = M[1 − e^(−y)(1 + y)], g_bar = G M_b/R²), g_obs = V_c²/R, both a₀ laws, the per-object error model, inverse-variance pooling with √(χ²/dof) inflation, the SPARC anchor, the 24-cell grid;
- σ_out: recomputed by me from the extracted profile data (`data_assembly/arxiv_tables/kurvs_sigma_profiles/kurvs_sigma_profiles.csv`, kpc, signed R, clipped-white markers flagged) using CFG141's frozen rules (two sides averaged at |R|; linear interpolation where a side reaches R_max; otherwise error-weighted mean of the outermost three unclipped points; plotted error bar, 20% where none; clipped markers excluded);
- α(x) = −0.146x² + 1.204x + 1.475 with x = R_max/R_eff − 1 clipped to [0, 4]; V_c² = V_obs² + α σ_out²;
- the ladder P0 → P1 → P2 → P3 → P4, so that any disagreement at P4 is localised to a rung.

**Data files (inputs; independence stops at their content):**
- `data_assembly/arxiv_tables/kurvs2023_{integrated,kinematics,velocities_at_radii,fdm}.csv` and `KURVS_DEFINITIONS_NOTE.md`;
- `data_assembly/arxiv_tables/kurvs_sigma_profiles/` (the data chat's vector-figure extraction, 94e4a5181);
- SPARC: `real_research/data/SPARC_Lelli2016c.mrt`, `real_research/data/sparc_data/*_rotmod.dat` (rows parsed by whitespace field order, not by the header byte columns — the disclosed CFG140 trap);
- KROSS V2: `data_assembly/high_z_tf_tables/kross_v2.csv`;
- gas context (attack b): `data_assembly/kmos3d_phibss/phibss13_joined.csv`, `data_assembly/arxiv_tables/sharma2024_gs21b.csv` (has MH2, MHI columns), `data_assembly/arxiv_tables/romanoliveira2023_gasmasses.csv` (H₂ of SMGs, not disc-comparable; context only).

**Where independence STOPS (reused, not re-derived):**
1. **The kernel and a₀ constants:** `campaign_fresh_gravity/CFG4_common.py` (ν_mono, A0 canonical 9.3603e-11 and alt 1.13e-10), imported read-only. Its two limits are re-checked (C2 below), its functional form is not re-derived. E(z) = √(Ω_m(1+z)³ + Ω_Λ), Ω_m = 0.315, flat, is written by me.
2. **CFG140's setup choices** that I take as declared (I read them; I do not re-argue them): the gas bracket μ ∈ {0.25, 0.67, 1.5, 4} and the δ ∈ {−0.2, 0, +0.2} bracket; the declared per-object errors (0.15 dex stellar mass for KURVS/KROSS, 0.10 for SPARC, ±5° inclination for KURVS, tabulated e_Inc for SPARC, ±5° KROSS); the SPARC anchor selection (Q ≤ 2, i ≥ 30°, log M* ≥ 9.5, M* = 0.5 L[3.6], last rotmod point, gas = 1.33 M_HI in the same radial model, σ = 10 km/s); the "spherical surrogate" g_obs = V_c²/R; the KURVS inclination-corrected v_last as the input velocity.
3. **The Kretschmer calibration itself** (Table 1 gas/disc row): I did not read the paper and may not fetch it. I take α(x) and the 40% scatter as CFG160 quotes them. C2 checks only internal arithmetic.
4. **Ambiguities in the frozen text that I resolve NOW, before opening any script** (a later mismatch localised to one of these is reported as "convention", not as an error by either side):
   - KURVS inclination for the error term: `inc_sfr_deg` (Hα geometry); variant `inc_star_deg`. The frozen text says ±5° with no tabulated value, so the value of i enters only through cot i.
   - Error propagation under a pressure correction: δlog g_obs = (2/ln10)(V δV + α σ δσ)/(V² + ασ²), plus (2/ln10)(V²/V_c²) cot i δi; no error on α in the headline (scatter treated separately, attack d).
   - Mass slope: d log g_pred/d log g_bar evaluated numerically at the assumed g_bar.
   - SPARC gas: 1.33 × M_HI as an exponential disc at y = R/(2R_d) (literal reading); variant: rotmod V_gas.
   - The SPARC anchor's α uses R_e = 1.68 R_disk, x = R_last/R_e − 1, clipped to [0, 4], σ = 10 km/s.
   - Δ′ error: quadrature of the KURVS pooled error and the anchor's pooled error (each with its own √(χ²/dof) inflation where > 1).
   - The rival is applied at each galaxy's own z_Hα (E(z_i)); the pooled Δ_H uses the same weights as Δ_flat.

## 2. The headline, pinned (README numbers = TARGETS)

Decision cell: μ = 0.67, δ = 0, canonical footing a₀ = 9.3603e-11, P4, R_e = R_eff.

| | Δ′_flat | Δ′_H |
|---|---|---|
| P4 primary | +0.144 ± 0.044 (+3.3σ) | −0.006 ± 0.044 (−0.1σ) |

Sensitivity targets (canonical, δ = 0, quoted as Δ′ ± σ, sigma-units):
- μ = 0.25: flat +0.204, rival +0.051; μ = 1.5: flat +0.053 (+1.2σ), rival −0.092 (−2.1σ); μ = 4: flat −0.123, rival −0.255 (both over-predict).
- α × 0.6: +0.058 ± 0.045 (+1.3σ) / −0.092 ± 0.046 (−2.0σ); α × 1.4: +0.211 ± 0.046 (+4.6σ) / +0.060 ± 0.045 (+1.3σ).
- R_e = 2 R_eff: +0.066 ± 0.046 (+1.4σ) / −0.084 ± 0.047 (−1.8σ).
- P2 (CFG141): +0.390 ± 0.065 (+6.0σ) / +0.237 ± 0.063 (+3.7σ). P3 (CFG141 README): +0.24 ± 0.07 (3.5σ) / +0.09 ± 0.07 (1.3σ). P1 (CFG140 README): +0.398 ± 0.070 / +0.244. P0: −0.130 ± 0.057 / −0.279. SPARC anchor C1: median Δ_flat = +0.064 dex, pooled +0.092 ± 0.013.
- Grid counts (24 cells): flat disfavoured (Δ′ > +2σ) in 14, "survives" in 6 (the README's 14 + 6 ≠ 24, so the definition of "survives" is unclear; I will report all three classes: > +2σ, |Δ′| ≤ 2σ, < −2σ); rival < −2σ in 10, within 2σ in 14.
- Per galaxy (central cell, unanchored): x 1.04–3.54, α 2.57–3.91, V_c²/V² 1.19–2.52; Δ_flat −0.11 (KURVS-8) to +0.48 (KURVS-17); Δ_H −0.28 to +0.33.
- Power row: the two laws are 2.6–3.7σ apart per cell.

Declared reading map (CFG160's, restated so that my scripts use it verbatim): flat within 2σ and rival < −2σ = lean flat; rival within 2σ and flat > +2σ = lean rival; both within or both outside = non-diagnostic. At the decision cell the target class is LEAN RIVAL.

## 3. Hand ESTIMATES (labelled; NOT predictions independent of the README) with probability each reproduces

Method: rescale CFG141's per-galaxy P2 rows by α_P4/α_P2 (α_P2 = 2R/R_d = 3.36 R/R_eff). With x from R_max/R_d ÷ 1.68 I get α = 3.17, 3.00, 3.88, 2.56, 2.61, 3.61, 2.91, 3.17, 3.81, 3.91 for KURVS 3, 7, 8, 9, 11, 13, 15, 16, 17, 21, and V_c²/V² = 1.22, 2.28, 1.64, 1.36, 1.19, 2.52, 2.03, 1.87, 2.00, 2.09. These agree with the README ranges (1.19–2.52, α 2.57–3.91), so the README's α and V_c² table is internally consistent with the formula. Unweighted mean shift P2 → P4 in Δ_flat: −0.273; the P2 unweighted mean of the ten Δ_flat rows is 0.483, so the anchor implied by 0.483 − 0.390 is 0.093.

| quantity | hand ESTIMATE | README target | P(my code lands within the pass line) |
|---|---|---|---|
| Δ′_flat, decision cell | +0.14 ± 0.02 | +0.144 | 0.45 (line: ±0.01) |
| Δ′_H, decision cell | −0.015 ± 0.02 (P2 separation 0.153 carries over) | −0.006 | 0.45 (line: ±0.01) |
| σ(Δ′), decision cell | 0.044 ± 0.008 (error scales with A/f; not estimable to 5% by hand) | 0.044 | 0.25 (line: 5%) |
| per-galaxy Δ_flat extremes | −0.10 (KURVS-8), +0.49 (KURVS-17) | −0.11, +0.48 | 0.6 (each within 0.02) |
| μ rows (0.25 / 1.5 / 4), flat | +0.20 / +0.054 / −0.12 (μ-shift taken from CFG141's P2 grid, valid because g_bar changes only) | +0.204 / +0.053 / −0.123 | 0.5 each within 0.15σ |
| α × 0.6 / × 1.4, flat | +0.06 / +0.20 | +0.058 / +0.211 | 0.5 / 0.4 |
| R_e = 2 R_eff, flat | +0.066 | +0.066 | 0.5 |
| decision class = lean rival | yes | yes | 0.85 |
| all ten sensitivity rows within 0.15σ jointly | | | 0.15 |
| grid counts (14 flat-disfavoured, 10 rival-disfavoured), exact | flat 12–15, rival 8–11 | 14, 10 | exact 0.35; within ±2: 0.75 |
| ladder P2 central cell +0.390/+0.237 within 0.01 | | | 0.5 |
| break-even μ (canonical, δ = 0, log-linear interpolation of the grid) | flat ≈ 2.0, rival ≈ 0.65 | (derived, not in README) | 0.5 (each within 25%) |
| P4 differential KURVS − KROSS | ≈ +0.19 ± 0.08 (crude; KROSS σ/V assumed 0.2) | (not in README) | 0.4 (sign and 1σ) |

The ladder rule: my P0/P1/P2 central numbers must reproduce the READMEs (P0 −0.130/−0.279, P1 +0.398/+0.244, P2 +0.390/+0.237, C1 anchor median +0.064) to 0.03 before any P4 disagreement is read as a P4 finding. If a lower rung is off by more than 0.03, the disagreement is reported as "setup convention, upstream of P4" and the P4 pass line is judged on the DIFFERENCE P4 − P2 (README: −0.246 flat, −0.243 rival) as well.

## 4. Exact pass lines

A number is REPRODUCED only if both hold:
1. **Decision cell:** |my Δ′ − README Δ′| ≤ 0.01 dex (flat and rival) AND my σ within 5% of 0.044.
2. **Sensitivity rows** (μ = 0.25/1.5/4; α × 0.6/1.4; R_e = 2 R_eff; flat and rival each): my z = Δ′/σ within 0.15 of the README's z.
3. **Verdict:** signs of every quoted Δ′ match; the decision-cell class (lean rival) matches; class of every sensitivity row matches (μ = 1.5 flips to lean flat by the map: flat +1.2σ, rival −2.1σ; μ = 4: both < −2σ; α × 0.6: flat 1.3σ, rival −2.0σ — the rival row sits AT the −2σ edge, so its class is declared "edge" and is judged by the numeric rule 2, not the class).
4. **Controls C1, C2** (below) pass.
5. **Grid classification counts** reported; exact match not required, ±2 cells is "consistent".

Between 0.01 and 0.03 dex at the decision cell: labelled "consistent, not reproduced; ladder decides where it comes from". Beyond 0.03: DISAGREEMENT (a valid result). Nothing is repaired after the fact.

Controls of my own:
- **C1:** with α_P4 replaced by 2R_max/R_d, my P4 code path reproduces MY OWN P2 grid to 1e-12 (24 cells × 4 quantities); my P2 central cell is then compared with CFG141's target (rung above).
- **C2:** α(0) = 1.475, α(1) = 2.533, α(4) = 3.955 to 1e-9; α monotone increasing on [0, 4] (vertex at x ≈ 4.12).
- **C3 (kernel):** at y = 10⁻¹², g_pred/√(g_bar a) − 1 < 1e-5; at y = 10¹², g_pred/g_bar − 1 < 1e-5 (CFG140's corrected C2).
- **C4 (sample):** the ten selected IDs are exactly the f_DM rows; all inputs finite; no galaxy has x outside [0, 4] (expected 0 of 10; if any is outside, α clipping is active and is reported).
- **R0 power, printed before any g_obs:** expected separation of the two laws per cell / pooled error, evaluated with V from the flat prediction.

## 5. MUTATE controls (each must flip the decision-cell class or a load-bearing cell)

Exit convention: main run exits 0. `MUTATE=k` exits 1 when the control BITES (the decision-cell class differs from the main run's "lean rival"), exits 0 and prints `CONTROL FAILED TO BITE` otherwise; that outcome is kept and reported. Outputs are named by mode.

- **M1 (α ≡ 0, no pressure correction, = P0 with my pipeline):** expected Δ′_flat ≈ −0.13, Δ′_H ≈ −0.28: flat within 2σ (−2.3σ; borderline, so judged numerically), rival < −2σ: class flips to "lean flat" or "both outside". Must NOT be "lean rival".
- **M1b (α ≡ 1):** hand estimate Δ′_flat ≈ 0.00 ± 0.03, Δ′_H ≈ −0.15 (−3.4σ): class = lean flat. Bites.
- **M2 (sign of the pressure correction flipped:** V_c² = V_obs²/(1 + ασ²/V_obs²), the smooth inverse, because subtracting ασ² would go negative for six galaxies): estimate Δ′_flat ≈ −0.35, Δ′_H ≈ −0.50, both < −2σ: class = "both outside". Bites.
- **M3 (laws swapped:** the label "flat" gets a₀E(z) and "rival" gets a₀ inside the scoring and verdict code, data unchanged): Δ′ pair exchanged, class flips to "lean flat". A pure control of the verdict logic; it also proves the map is not hard-wired to the target. Bites by construction.
- **M4 (gas prior changed:** the decision cell moved to μ = 1.5): class flips to "lean flat" (target flat +1.2σ, rival −2.1σ). Bites.
- **M5 (KURVS v_last × 10^0.3, g_obs × 4, CFG140's MUTATE):** flat disfavoured in every cell, H1 fails.
- **M6 (σ_out permuted among the ten galaxies, seed 165; informational):** need not bite; reports how much the per-galaxy pairing of σ with V matters. Its result is recorded either way.

## 6. FIVE ATTACKS (frozen procedure, pass/fail meaning)

All attack outputs are LABELLED SENSITIVITY GRIDS, not new headlines. The headline stays P4 at the decision cell.

### (a) Forking paths
**Facts to check:** the Kretschmer calibration was chosen after CFG141's P2 and P3 results were known. CFG160 defends this by adopting the published fit verbatim with every free choice fixed first. What was NOT fixed by any prior: the choice of this calibration among possible ones; that R_e is the stellar Hα-side R_eff and not the gas half-mass radius (Kretschmer's R_e is that of the analysed component); α applied as a single coherent number.

**Calibrations in the repo or usable without any fetch:**
- P0 (none), P1 (Burkert et al. 2010 constant σ, α = 2R/R_d), P2 (self-gravitating isothermal layer, same as Kretschmer's self-gravitating α = 3.36 R/R_e, since 2 × 1.68 = 3.36), P3 (fixed scale height plus gradient), all from CFG140/141;
- Kretschmer's own quoted abstract line "α ≈ 1 at R_e to 4 at 5 R_e" (as CFG160 quotes it);
- Sharma+2021 (KROSS, AD correction 10–87% in V, per the repo's ONE_OFF_DATASETS note; the KROSS per-galaxy data sit in `sharma2024_gs21b.csv`, no derivation is possible without their profiles);
- CRISTAL vector data (z 4.4–5.7, models already asymmetric-drift corrected): context only, wrong redshift regime.
- NOT usable: Dalcanton & Stilp 2010 (not read), Ubler+2021 (TNG50 simulation, no data on disk), Bershady+2024 (z ≈ 0, not on disk).

**Frozen procedure:** at the decision cell (and, secondarily, the full 24-cell grid) evaluate the labelled alternatives of α(x) with the same σ_out:
- Kretschmer table (primary); linear α = 1.475 + 1.204x (drop the quadratic); abstract-linear α = 1 + 0.75x; constant α ∈ {1, 2, 2.53 (= α(x = 1)), 3, 3.955}; α = 1.265 R/R_e (self-gravitating shape rescaled to α(1) = 2.53);
- normalisation scan s ∈ {0.3, 0.5, 0.6, 0.75, 1.0, 1.25, 1.4} multiplying the primary α; report the break-even s at which Δ′_flat = 0 and Δ′_H = 0 (log-linear interpolation);
- R_e,gas/R_eff ∈ {1, 1.25, 1.5, 2, 3};
- P3 at the decision cell by CFG160's own map.

Hand ESTIMATES (labelled): the lean depends on the NORMALISATION of α, not its shape. Abstract-linear: Δ′_flat ≈ +0.11 (2.4σ), Δ′_H ≈ −0.05: same class. Constant α = 3: Δ′_flat ≈ +0.13: same class. α ≡ 1: ≈ 0.00 (lean flat). Break-even s: rival ≈ 0.96, flat ≈ 0.3.

**Pass/fail meaning:**
- "The lean is not a forking-path artefact of the α shape": PASS if the class is "lean rival" for every alternative whose median α over the ten galaxies lies within ×[0.75, 1.25] of P4's median (≈ 3.0), FAIL if any such alternative changes the class. The class is not required to survive s < 0.75 (that is a normalisation change, and the README already says α × 0.6 removes the lean).
- The claim "the first in-regime reading whose central value favours the rival": by CFG160's own map, P3 at the paper's gas (flat +0.24, 3.5σ; rival +0.09, 1.3σ) is ALREADY "rival within 2σ, flat above +2σ" = lean rival. My probability that my P3 run shows this: 0.85. If so this sentence in the README is WRONG as a statement about the frozen map, and the reading is "P3 and P4 give the same map at μ = 0.67"; that is a valid disagreement, not a repair.

### (b) The gas prior
**Facts:** μ = 0.67 is M_mol/M* from the paper's 40% molecular fraction defined as M_mol/(M* + M_mol) — molecular gas only; the mass model treats μ as TOTAL gas. So the decision cell omits HI by construction. The 40% is a point in the 0.4–0.6 range (μ_mol 0.67–1.5). CFG140 says stacked z ≈ 1 M_HI ≈ 4 M*; CFG141 says a total of 2–5 M* is "plausible, not measured".

**Frozen procedure:** (1) from `phibss13_joined.csv` (PHIBSS, CO-selected so biased high) and `sharma2024_gs21b.csv` (MH2, MHI columns) compute, for log M* ∈ [9.5, 10.6] and z ∈ [0.9, 2.4], medians and 16–84% of μ_mol = M_H2/M* and μ_HI = M_HI/M* with n printed, no fit; (2) evaluate the decision cell at μ_tot = μ_mol,med + μ_HI,med (repo data only) and at the 16th/84th percentile; (3) break-even μ for each law (grid interpolation in log μ, bootstrap 2000 resamples of the ten galaxies, seed 165, for the interval); (4) gas scale variant: μ_tot with the gas disc at 2, 3, 4 R_d (HI is more extended, so less of it is enclosed at R_max; enclosed fraction at y = 1–2 is 0.26–0.59); (5) the class at every μ on a log-grid 0.25–4.

Hand ESTIMATES (labelled): break-even μ flat ≈ 2.0, rival ≈ 0.65; the midpoint √(0.65 × 2.0) ≈ 1.1 is the total-gas value at which the lean turns. A total gas of μ ≥ 1.5 gives lean flat. P(the repo's μ_tot median exceeds 1.1) ≈ 0.7, but its provenance (CO/scaling-relation, HI-stacked) is not KURVS-specific.

**Pass/fail meaning:** the decision-cell lean is "robust to the gas prior" only if lean rival persists at μ_tot from the repo data AND at its 16–84% range. I expect FAIL: the lean is a statement about a molecular-only gas budget. A FAIL here is the value of the attack, not an error by CFG160 (CFG160 says so itself). CFG142's dust limit (KURVS-11 < 0.72 M*) is not re-used here (not a repo-data input I re-derive).

### (c) Are the KROSS/SPARC anchors consistent with a pressure correction of this size?
**Procedure:** (1) SPARC anchor under P0 vs P4 (σ = 10): shift in anchor Δ (hand estimate: ≈ −0.02, moving Δ′ by ≈ +0.02); (2) the anchor split by x = R_last/(1.68 R_disk) − 1: tests whether the P4 formula with σ = 10 acts differently at the KURVS x range (1–3.5); sensitivity σ_anchor ∈ {7, 10, 15}; (3) KROSS through the same P4 pipeline (R = 2 r_im so x = 1 and α = 2.533, measured σ₀, μ = 0.67, anchored): pooled Δ_flat, Δ_H at P0, P1, P4, and the differential Δ(KURVS) − Δ(KROSS) against flat (0) and the rival (E(z) ratio at the two median redshifts, about +0.08, CFG140); (4) size check: the KURVS V_c/V − 1 under P4 (hand: 9–59%) against Sharma+2021's 10–87% and under P2 (hand: 22–146%, exceeding 87% for about seven of ten, KURVS 7, 8, 13, 15, 16, 17, 21).

**Hand ESTIMATE (crude):** under P1 the differential is +0.27 ± 0.07 (CFG140); under P4 I estimate ≈ +0.19 ± 0.08 (the KROSS correction also falls by ≈ 2.6×); i.e. P4 removes about a third of the "manufactured evolution", not all.

**Pass/fail meaning:** CONSISTENT if the P4 differential lies within 2σ of the flat prediction AND of the rival prediction (then P4 does not manufacture evolution); FAIL-flat if it exceeds flat by > 2σ (a residual "evolution" neither law explains); the size check PASSES if P4's max V_c/V − 1 ≤ 0.87. P(size check passes) = 0.9. P(differential within 2σ of flat) = 0.5.

### (d) Range and scatter at R_max
**Facts to check:** x = 1.0–3.5 (R_max = 2.0–4.5 R_e) is inside Kretschmer's fitted range (profiles to ≈ 5 R_e, x ≤ 4); no extrapolation is expected. The masses log M* ≈ 9.7–10.5 lie in their analysed range (> 10^9.5). Two flags: (i) the table gives α(R_e) = 1.475 but the quoted abstract says ≈ 1 at R_e (a 47% gap, at the edge of the 40% scatter); (ii) CFG160's README says the three largest residuals, KURVS 13, 17, 21, "have the largest x", but from R_max/R_d the largest x are 21 (3.5), 8 (3.4), 17 (3.1), and 13 is fourth (2.6). Check.

**Frozen procedure:** (1) count of galaxies with x outside [0, 4] (expected 0) and confirm α_clipped = α_unclipped for all ten; (2) the effect of holding α flat beyond x = 3 (α(3) = 3.77) and of x + 0.5, x − 0.5 shifts; (3) the scatter: CFG160 treats ×0.6/×1.4 as a fully COHERENT systematic. If instead the 40% is random per galaxy (independent lognormal in α), the pooled effect is ≈ 0.4 A/(f ln10)/√10 ≈ 0.027 dex extra in quadrature. Run both: coherent (±0.4) and random Monte Carlo (20000 draws, seed 165), reporting the inflated σ and z at the decision cell; (4) R_e,gas/R_eff scan of (a).

**Hand ESTIMATE:** random scatter raises σ from 0.044 to ≈ 0.052: z_flat ≈ 2.8, z_H ≈ −0.1: class unchanged but flat drops from 3.3σ to below 3σ.
**Pass/fail meaning:** PASS if no galaxy is outside [0, 4], the class is unchanged under the random-scatter inflation, and the "largest x" sentence is correct. A failing "largest x" statement is a documentation error only; it does not change any number.

### (e) What a NULL would have looked like (power and calibration of the decision statistic)
**Frozen procedure (pre-declared: N = 20000 trials, seed = 165; a stability re-run with seed = 166 is reported alongside):**
- For each trial generate a mock KURVS: per galaxy the true baryons at true μ and true M* (assumed M* plus 0.15 dex Gaussian), the law's g_pred, then V_c² = g R, V_obs² = V_c² − α_true σ², and add measurement noise to V (real e_V), σ_out (real error), inclination (±5°). Analyse with the assumed μ = 0.67, α_K(x), δ = 0, exactly as in the main run, including the anchor (its pooled offset varies within its own error 0.013).
- **Truth families (four):** flat law and rival law, each with (i) idealised: μ_true = 0.67, α_true = α_K; (ii-a) nuisance N1: μ_true lognormal with median 1.0 and 0.3 dex scatter, α_true = α_K × lognormal(0, 0.4) per galaxy times a coherent lognormal(0, 0.2) scale; (ii-b) nuisance N2: the same with median μ = 2.0. Both nuisance medians are reported; neither is preferred (declared before any result).
- Record: mean and sd of Δ′_flat and Δ′_H, the class fractions {lean rival, lean flat, non-diagnostic}, P(Δ′_flat/σ ≥ 3.3 | truth), P(z_H ≥ −0.1 or ≤ +0.1 | truth), and the likelihood ratio of the observed Δ′_flat = 0.144 between the two mock distributions (Gaussian fit and kernel density; both reported).

**Hand ESTIMATES (labelled):**
- Idealised: flat truth gives Δ′_flat ≈ 0 ± 0.044, so P(z ≥ 3.3) ≈ 5 × 10⁻⁴; rival truth gives Δ′_flat ≈ +0.15 ± 0.044; LR ≈ 230 for the rival. Under the idealised trial the lean is strong, by construction.
- Nuisance N1/N2: the gas alone (about 0.3 per dex in Δ′) and the coherent α scale broaden the statistic to ≈ 0.10 ± 0.02. Then P(z_flat ≥ 3.3 | flat truth, nuisance) ≈ 0.10–0.25 (N2 lower than N1), and the LR falls to order 2–5.

**Pass/fail meaning:** CFG160's reading "a Kretschmer-conditional lean toward a₀ ∝ H(z)" is JUSTIFIED as stated only if, under the nuisance families, P(lean rival | flat truth) < 0.05 and P(lean rival | rival truth) > 0.3. If P(lean rival | flat truth, N1 or N2) ≥ 0.10, the lean is WEAK EVIDENCE: it is reported as such, it does not fall as an error of CFG160 (CFG160 says "not robust"), but any sentence stronger than "conditional lean" is not supported. Under no outcome is it read as a detection, or as a data preference for either law.

## 7. Script plan (phase 2 only; none exists now)

All in `campaign_fresh_gravity/` only if the orchestrator moves them; developed in the scratch dir. Repo path: `ZF_REPO` env var or walk up from `__file__` until `data_assembly` is found; print `<repo>` in place of the absolute path. Each run is under ≈ 15 min (expected seconds to minutes).
- `CFG165_referee_kurvs_p4.py`: main run (ladder P0–P4, C1–C4, R0, decision cell, 24-cell grid, R3 per-galaxy, sensitivity rows) and `MUTATE=1|1b|2|3|4|5|6`; outputs `CFG165_main.out/.json`, `CFG165_MUTATE_<k>.out/.json`; exit 0 main, exit 1 when the mutation bites.
- `CFG165_attacks_abcd.py`: attacks (a)–(d); outputs `CFG165_attacks.out/.json`; imports the pipeline from the main script; exit 0 always (labelled grids); prints PASS/FAIL per attack line as defined above.
- `CFG165_power_e.py`: attack (e); N = 20000, seed 165, then 166; outputs `CFG165_power.out/.json`; exit 0.
- `CFG165_manifest.txt`: sha256 of every input file and script; no absolute home path anywhere.
- Phase-2 order: (1) my scripts written and saved; (2) my main and every MUTATE saved; (3) only then, open CFG140/141/160 scripts, `.out`, `.json`; (4) the comparison table (mine vs theirs, per number, PASS/consistent/DISAGREE), including any place where their script does something the frozen text does not say.

## 8. What counts as disagreement (a valid result)

- Any decision-cell Δ′ or σ outside the section 4 pass line, once the ladder has localised it (upstream setup convention vs P4-specific).
- The class at the decision cell not "lean rival"; a sensitivity row's class or z off by more than 0.15σ.
- P3 already producing the same map (section 6a): the "first ... favours the rival" sentence is then a wording disagreement.
- The grid counts, with the classes defined explicitly (README's 14 + 6 ≠ 24).
- The "largest x" statement, if it fails (6d).
- Any attack outcome that shows the lean is not robust (a fails; b likely fails; e nuisance-broad). These are results about the SIZE of the conclusion, and are reported in exactly the words the criteria give.
- A MUTATE that fails to bite, and any hand estimate wrong by more than its stated tolerance, are reported as they are.
- Agreement is also a valid result. Nothing here says the data favour either law or the framework; κ = ½ and Ω_c h² stay fitted; a lean is not a detection; the theory is not closed.
