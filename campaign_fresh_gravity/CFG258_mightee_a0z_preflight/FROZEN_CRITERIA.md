# CFG258 — FROZEN CRITERIA: a BLIND pre-flight (mocks only, nothing downloaded) of what the public MIGHTEE-HI / LADUMA RAR sample (Vărăşteanu et al., arXiv:2608.03576; 130 resolved HI galaxies to z ≈ 0.09) could say about FLAT a₀ against a₀ ∝ H(z) and against the anchored slope claim

Written 2026-10-01 and committed BEFORE any script exists and before any forecast number is computed. The lane is the orchestrator's assignment (CFG258, from the orchestrator's block). **κ = ½ is FITTED, NOT DERIVED.** Both footings are carried (canonical a₀ = 9.3603e-11, alt 1.1312e-10 m s⁻²), kernel **ν_mono** (FP1's, exec'd read-only through `CFG4_common`). Nothing here says the data favour a framework: this is a forecast of what a sample could separate, not a measurement. **No download, no fetch; a measurement would need the owner's go for the download, in the calculation chat.**

## 0. Disclosure (before any number)
- **Seen, from the orchestrator's message (verified by the orchestrator against the abstract, and by the data chat's full-text reading):** the abstract says there is "no significant redshift evolution in the RAR acceleration scale"; anchoring to SPARC at z = 0 gives a formal 5σ **a₁ = (5.23 ± 1.05) × 10⁻¹⁰ m s⁻² per unit z**, which the authors attribute to the choice of anchor; 130 resolved HI galaxies to z ≈ 0.09. I have not read the paper (not fetched) and I know no other number of it: not the redshift distribution, not the number of points per curve, not the errors, not the per-bin acceleration scales. a₁ and its error are NOT verified by me.
- **Background only:** MIGHTEE-HI is a MeerKAT HI survey. The repo holds earlier MIGHTEE-related files (found by a FILENAME-only search, nothing opened): `data_assembly/mightee_hi_highz/`, `opus_48_extended_research/reviews/next_doors_2026_07/mightee_rar_*.csv` and `b3_mightee_*.py`, `data_assembly/timeline/*`, `data_assembly/HIGHZ_SOURCE_TABLE_2026-09-29.md`, `sol61_push/review_scope.json` and others. None was opened by this lane; whether any bears on arXiv:2608.03576 is unknown to me. `campaign_fresh_gravity/CFG256_a0z_sample_spec_scoping/SCOPING_2026-09-30.md` was not opened.
- **Arithmetic done before this freeze (no data, no MIGHTEE number except a₁):** b₃ = a₁ / a₀ = 5.587 (canonical) / 4.623 (alt); a₀(z)/a₀(0) = 1 + b₃ z; the rival E(z) = √(0.315 (1 + z)³ + 0.685) (Z1's law, as CFG219) is 1.0454 at z = 0.09 (+4.5 %, 0.019 dex); the sample-minus-anchor offset implied by the anchored slope at a mean z of 0.04 / 0.055 / 0.07 is +0.088 / +0.116 / +0.143 dex (canonical), +0.074 / +0.098 / +0.122 (alt); the quoted formal error 1.05e-10 at z̄ = 0.055 corresponds to a per-galaxy scatter of about 0.31 dex for N = 130 if the anchor's own error were neglected. These are the "implication of (iii)" the orchestrator asked for; the script reproduces them as a control.
- **SPARC counts, looked at before the freeze (no fit, no a₀):** 175 rotmod galaxies; the template pool defined below has 135 galaxies and 2,800 points.
- Nothing about the outcome of any forecast was seen. Anything added after the numbers are seen is labelled post hoc.

## 1. The three laws and the questions
a₀(z)/a₀(0) =
- **FLAT (i):** 1.
- **RIVAL (ii):** E(z) = √(0.315 (1 + z)³ + 0.685) (≈ 1 + 0.4725 z at small z; +4.5 % at z = 0.09).
- **ANCH (iii), the anchored claim taken as a physical law:** 1 + b₃ z with **b₃ = a₁ / a₀(footing)** (a₁ = 5.23e-10 per unit z; sensitivities a₁ ± 1.05e-10 in the primary cell only).
**Question A:** the a₀ change (iii) implies across z = 0.02 to 0.09 and at the sample's mean z (arithmetic, section 0; reproduced by the script).
**Question B:** the size of a SPARC-versus-MIGHTEE offset (stellar M/L scale, gas scale, distance scale, velocity scale, sample selection) that would mimic (iii).
**Question C:** whether the sample could distinguish (i) from (iii) and (i) from (ii): POSSIBLE / NOT POSSIBLE, decided here before any MIGHTEE number is opened.

## 2. The mock (SPARC-resampled; every MIGHTEE-like number is a SCENARIO, UNVERIFIED)
- **Templates:** `CFG4_common.load_sparc()` galaxies with meta Q ≤ 2 and 30° ≤ Inc ≤ 85° (the usual SPARC RAR quality cuts; 135 galaxies, 2,800 points): per point R (kpc), V_gas, V_disk, V_bul at Υ = 1 and the catalogue's e_V, D, eD, Inc, eInc. Units: g [m s⁻²] = 3.2408e-14 · V|V| [km² s⁻²] / R [kpc]. **Mock truth baryons:** Υ_disc = 0.6, Υ_bul = 1.4 Υ_disc (the record's FP1-C convention); g_bar,true = g_gas + Υ (g_disk + 1.4 g_bul); points with g_bar,true ≤ 0 are dropped.
- **Truth law:** g_obs,true = g_bar,true · ν_mono(g_bar,true / a₀,T(z)), a₀,T(z) = a₀(footing) f_T(z) (for the MIGHTEE-like sample, times 10^(τ_sel + κ_sel u), section 4).
- **Anchor S ("SPARC", z = 0):** all pool galaxies, all valid points, own random terms (per point intrinsic scatter σ_int = 0.06 dex on log g_obs; velocity error σ_V/V from the template's e_V/V; per galaxy: Υ scatter σ_Υ,S = 0.10 dex on the stellar part, inclination error from the template's eInc through δV/V = cot i · δi, distance error from the template's eD/D through δlog g_obs = −log₁₀(1 + ε_D); g_bar is distance-independent for photometric and HI masses at fixed angular radius, g_obs ∝ 1/D). A library of **1,500 independent anchor realizations per footing** (seed 2580) gives θ̂_S = log₁₀ â₀,S (b fixed at 0).
- **Sample M ("MIGHTEE-like", z > 0):** N = 130 galaxies drawn with replacement from the pool; z from the cell's distribution; points: the cell's rule; per point σ_V/V (cell), σ_int = 0.06; per galaxy σ_Υ,M = 0.15 dex, σ_i,M = 5°, σ_D,M = √((250 km s⁻¹ / (c z))² + 0.03²) (peculiar velocities and a 3 % model floor).
- **Analyst:** Υ is NOT fitted (fixed at the adopted values); weights w = 1 / σ_nom², σ_nom² = (2 σ_V/V / ln 10)² + 0.06²; the analyst knows none of the shared systematics.
- **Cells (each: footing, z distribution, point rule, σ_V/V, N, λ):** **C0 PRIMARY** canonical, z ~ U[0.02, 0.09], 6 random points per galaxy (all if fewer), σ_V/V = 0.07, N = 130, λ = 1. C1 alt footing. C2 z ∝ z² on [0.02, 0.09]. C3 z ~ U[0.005, 0.09]. C4 all points. C5 the 6 OUTERMOST points (HI-like). C6 σ_V/V = 0.04. C7 σ_V/V = 0.12. C8 / C9 / C10 N = 260 / 520 / 1,040. **C11 AM (authors-matched):** λ multiplies σ_Υ,M, σ_i,M and the 3 % distance floor, and is solved by bisection (tolerance 2 %, 2,000 mocks per step) so that SD(b̂_A | FLAT, shared systematics OFF) · a₀(canonical) = 1.05e-10 at C0's design. **C12 REQ (a requirement scenario, NOT MIGHTEE):** z ~ U[0.02, 0.30].

## 3. Estimators (E1 and E2) and the statistic that sees shared systematics
Model log₁₀ a₀(z) = θ + log₁₀(1 + b z), fitted by Gauss–Newton (≤ 8 iterations; derivative L(y) = −d log₁₀ν / d log₁₀y by central differences of ν_mono in log y, step 1e-3 dex) to log g_obs with weights w.
- **E1 (anchored, fixed-anchor):** θ fixed at θ̂_S (drawn from the anchor library); b free. This is the claim's own statistic: it detects a sample-versus-anchor shift and CANNOT tell a rise from a shared offset.
- **E2 (within-sample):** θ and b both free, M only. Immune to shared offsets in first order; sees z-dependent systematics only.
- Both are reported. **Detection** per mock: formal z_A = b̂_A / σ_formal,A > 3. **Attribution** per mock (needs the physical slope b₃ of the footing): PHYS if b̂_W > b₃ / 2, else OFFSET (the midpoint of the two slopes, equivalent to the smaller χ²).
- **CFG219 lesson:** the decision statistic is the TOTAL scatter over mocks, shared-systematic draws included, never a within-mock bootstrap; a control that can fail (C4) shows the frozen statistic reacts to the shared budget and a blind statistic does not.

## 4. The declared systematics budget (half-ranges b_k; each shared draw τ_k ~ N(0, (b_k / 2)²), one per mock, applied to every M galaxy, none to S; "UNVERIFIED" = declared)
Sign: τ_ML = log₁₀(M★,assumed / M★,true) on the stellar parts; τ_gas likewise on the gas; τ_D = log₁₀(D_assumed / D_true); τ_V = log₁₀(V_assumed / V_true); τ_sel = the true log₁₀ a₀ of the sample minus the anchor's (a physical or selection offset).
| term | A (optimistic) | B (conservative; PRIMARY) | source |
|---|---|---|---|
| T1 stellar M/L scale τ_ML | 0.05 | 0.15 | SPARC Υ₃.₆ (0.5 / 0.7) against an SED-based M★ with another SPS / IMF: model-to-model spread 0.1 to 0.2 dex (UNVERIFIED) |
| T2 gas-mass scale τ_gas | 0.02 | 0.06 | HI flux calibration about 5 %; B adds helium, self-absorption and molecular fractions (UNVERIFIED) |
| T3 distance scale τ_D | 0.015 | 0.04 | H₀ 70 ± 2.5 (A); 67.4 against 73 gives 0.035 (B) |
| T4 velocity scale τ_V | 0.01 | 0.03 | inclination, line-width conversions, beam smearing (UNVERIFIED) |
| T5 selection / sample mix τ_sel | 0.02 | 0.08 | UNVERIFIED declared; cross-checked post hoc by the spread of SPARC sub-sample a₀ fits (C8) |
| T6 velocity-scale drift κ_V (across the z range, linear in u) | 0.01 | 0.03 | beam smearing grows with distance (UNVERIFIED) |
| T7 selection drift κ_sel | 0.02 | 0.06 | UNVERIFIED declared (Malmquist-like trends with z) |
| T8 stellar-M/L drift κ_ML | 0.03 | 0.08 | selection of more massive galaxies and K-corrections with z (UNVERIFIED) |
u = (z − z_mid) / (z_hi − z_lo), z_mid the middle of the cell's z range. T6 to T8 are the within-sample (z-dependent) terms; T1 to T5 are common-mode.

## 5. Decision rules (frozen). M mocks per run: 10,000 for C0, 4,000 for every other cell; seed 258
For a pair (FLAT, L), an estimator E and a budget level X in {A, B}, with b̂ the estimator's slope:
- **Signal** Δ_E(L) = mean(b̂_E | truth L, shared systematics OFF) − mean(b̂_E | truth FLAT, OFF). **σ_stat,E** = SD(b̂_E | FLAT, OFF). **σ_tot,E(X)** = SD(b̂_E | FLAT, shared systematics ON at level X).
- **S_joint,E(X)** = Σ_k |b̂_E(τ_k at its half-range b_k, noiseless sample) − b̂_E(0)|, the aligned worst case of every term, from noiseless fits (the deterministic responses R_k are also the lever table of Question B).
- **R1 (total scatter):** the 5th percentile of b̂_E under truth L (level X) exceeds the 95th percentile of b̂_E under FLAT (level X).
- **R2 (worst case):** Δ_E(L) > S_joint,E(X) + 2 σ_stat,E.
- **POSSIBLE(E, X) iff R1 and R2.** Reported always: which rule fails, σ_stat, σ_tot, S_joint, Δ, and the REQUIRED precision: σ_req = Δ / 3.29 (R1), N_req = N (σ_stat / σ_req)² when σ_sys alone is below σ_req and "UNREACHABLE at any N" otherwise, the drift ceiling (the largest scale factor κ on level A's T6 to T8 for which R1 and R2 hold), and the minimum detectable slope.
- **Decisions (primary cell C0, level B; level A and the other cells reported beside, never substituted):** E1 is reported but NEVER decisive (it cannot attribute). **(i) vs (iii) is POSSIBLE iff POSSIBLE(E2, B)**; "POSSIBLE IF OPTIMISTIC" if only POSSIBLE(E2, A); else NOT POSSIBLE. **(i) vs (ii)** by the same rule on E2. The count of cells in which each outcome holds is reported.
- **Mimic table (Question B):** for each knob k in T1 to T5 and each z̄ in {0.04, 0.055, 0.07}: τ_k* = the value at which the noiseless E1 shift of the M sample equals log₁₀(1 + b₃ z̄) (root of the noiseless fit), with the lever R_k = ∂ log₁₀ â₀ / ∂ τ_k; the size is compared with the half-range b_k of level B.

## 6. Hand estimates (frozen now; scored by code, misses reported)
- **H1:** (iii) implies a₀(z)/a₀(0) = 1.503 / 1.416 at z = 0.09 and 1.307 / 1.254 at z = 0.055 (canonical / alt); the rival 1.045 and 1.017; (iii)'s change is 11 to 12 times the rival's at z = 0.09 in dex (0.177 against 0.019). Exact arithmetic.
- **H2 levers** (primary design, dex of log₁₀ â₀ per dex of τ): R_ML in [−1.6, −0.3]; R_gas in [−1.3, −0.2]; R_D in [−4, −1.2]; R_V in [+3, +8]; R_sel = +1 exactly. (Deep limit: −1, −1, −2, +4, +1.)
- **H3 mimic sizes at z̄ = 0.055, canonical (+0.116 dex):** τ_ML* in [−0.40, −0.07] dex (assumed stellar masses too LOW by that much); τ_D* in [−0.10, −0.03] dex (assumed distances too small, i.e. H₀ too high by 7 to 25 %); τ_V* in [+0.015, +0.04] dex (velocities too high by 3.5 to 10 %); τ_sel* = +0.116 dex exactly.
- **H4:** σ_stat of b̂_A (primary cell) between 0.5 and 2.0 per unit z; σ_stat of b̂_W between 1.2 and 4.0 per unit z. The AM scatter factor λ solves to a per-galaxy scatter between 0.2 and 0.45 dex equivalent (λ between 1.0 and 4.0).
- **H5 decisions:** (i) vs (ii) NOT POSSIBLE in every cell at both levels (the rival's slope is about 0.47 per unit z against σ ≥ 0.3), including N = 1,040. (i) vs (iii) via E1: R1 passes statistics-only and fails at level B; R2 fails at both levels; via E2 (decisive): NOT POSSIBLE in C0 at level B (S_joint,E2 of order 5 to 8 against a signal of 5.6), and it is POSSIBLE at most at level A in the optimistic cells (C4, C6, C8 to C10, C12).
- **H6 (planted offset, MUTATE=1):** E1 detects the planted offset in ≥ 95 % of mocks; the mean E2 slope is within ±0.15 b₃ of 0 while it is within ±5 % of b₃ under the physical ANCH truth; the attribution error rates equal the Gaussian prediction Φ(−b₃ / (2 σ_tot,E2)) within three Monte Carlo errors.
- **H7 (CFG219 reactivity):** under ANCH, Z_tot,E1 = Δ / σ_tot falls to below 50 % of its OFF value at level B while the blind within-mock-bootstrap statistic changes by less than 10 %.
- **H8 (post hoc cross-check, C8):** the range of fitted a₀ across SPARC sub-samples (mass terciles and morphological groups, each with at least 20 galaxies) is between 0.04 and 0.20 dex; "budget adequate" if it is ≤ 0.16 dex (the full width of T5 at level B), else "selection budget too small" and the decisions are re-read with T5 and T7 widened to the empirical range (post hoc, labelled).
- **H9:** σ_stat · √N is constant within 5 % across C0, C8, C9, C10 for both estimators.

## 7. Controls (all must pass; a failure is reported plainly)
- **C1 (the laws):** the script's b₃, E(z) and the implied changes equal section 0's arithmetic to 1e-3.
- **C2 (noiseless consistency):** with every random term and every shared term OFF, FLAT gives θ̂ = log₁₀ a₀ and b̂ = 0 to 1e-8 for both estimators; ANCH gives b̂ = b₃ to 1e-6 relative; RIVAL's E2 slope equals the independent weighted least-squares slope of E(z) on the design to 1e-3.
- **C3 (lever consistency):** on a synthetic deep-regime sample (y = 1e-8, gas only) the finite-difference levers are −1 (τ_ML equivalent via a stellar-only variant), −1 (τ_gas), −2 (τ_D), +4 (τ_V), +1 (τ_sel) to 1e-3.
- **C4 (reactivity; the CFG219 lesson):** H7's two statistics; it must FAIL under MUTATE=2.
- **C5 (Monte Carlo margin):** the primary decisions are re-derived from a reseeded rerun (seed 2580 + 1) of the C0 FLAT / ANCH level-B runs; a decision whose margin is below three Monte Carlo errors is labelled MC-LIMITED.
- **C6 (planted offset, MUTATE=1):** H6.
- **C7 (AM calibration):** the solved λ reproduces 1.05e-10 within 2 %.
- **C8 (post hoc, reported):** the SPARC sub-sample cross-check of the selection budget (H8).
- **MUTATE=1:** truths FLAT + a planted shared stellar-mass-scale offset τ_ML* solved per cell so that the noiseless E1 slope equals b₃ (the offset equal to (iii)); it must be DETECTED by E1 and ATTRIBUTED to an offset by E2 at the rates H6 states; outputs `*_MUTATE1`. **MUTATE=2:** every shared draw removed from the mocks (a statistic blind to shared systematics): C4 must FAIL; outputs `*_MUTATE2`.

## 8. Reporting rules
No sentence says the data favour the framework; every MIGHTEE-like number is a declared scenario; the forecast is optimistic in these ways: the true kernel is the analyst's kernel, the intrinsic scatter is Gaussian, Υ is fixed, no outliers, no EFE, no asymmetric drift, a thin template population with SPARC's mass range; "N galaxies" are resamples of 135 templates. First-run outputs are kept if a check implementation is fixed. The orchestrator records the lane; this lane does not append to LEDGER.md.
