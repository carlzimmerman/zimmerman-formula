# CFG309 — FROZEN CRITERIA: are the MIGHTEE-HI COSMOS catalogue `W_50_km_s` values rest-frame (W = c Δν/ν_obs) or observed-frame (optical convention, W_obs = (1 + z) W_rest)?

**This file is committed before any test below is run.** Not yet read: the catalogue paper's text (beyond what CFG306 quotes), `data_assembly/mightee_hi_catalogue_2026-10-02/README.md` and `catalogue_columns_from_paper.csv`, every ALFALFA documentation file, and every cube voxel. Lane launched by the orchestrator (CFG ID 309). It decides CFG306's CRITICAL finding C1, and it is built to fail as readily in one direction as in the other.

> **A convention check, not an a₀ measurement.** The only a₀ number is a labelled consequence: CFG301's committed chain re-run with the width frame that this lane decides (section 8). Nothing here can separate FLAT from a₀ ∝ H(z) (z ≤ 0.093). κ = ½ is FITTED. No knob scans. No downloads. No other lane's file is edited.

## 0. What has been read before this file (disclosure)
1. **CFG306** `REFEREE_REPORT.md`, finding C1 and the top of M1/M2; `cfg306_velocity_frame.py` and `.out` in full. That includes the five Appendix-D example values as CFG306 transcribed them: W50 = 237.858 / 67.32 / 84.858 / 264.04 / 420.287 km s⁻¹ = 40.5 / 12.0 / 14.1 / 46.5 / 74.0 channels. It also includes CFG306's per-example deviations (rest-frame +0.0007 in all five; observed-frame −0.016 to −0.083) and the matched catalogue W50s (223 / 67 / 85 / 264 / 420). So **T2 is not blind**: it is an independent re-extraction with its own parser and matching. Also read: CFG306's F2 slopes (−0.55 for all 58; +0.29 clipped) and F3 (median +0.0000; slope +1.00); and `cfg306_physics_checks.out` P1 (k = 1: 1.0456 × 10⁻¹⁰; **k = 0: 1.3111 × 10⁻¹⁰**, κ 0.700 / 0.580, half-width 0.128 dex).
2. **CFG302** `README.md` (aggregates: −0.0224 dex, robust scatter 0.0391, n 58; observed-frame variant +0.003; the flux deficit; PH1–PH5) and `cfg302_raw_widths.py` in full (the extraction, `measure`, `width_rule` and `profile_channels`). Only the CSV header and two rows were viewed, both outside the 58.
3. **CFG304** `README.md` (C-W50 +0.000 dex, robust scatter 0.037, N 15, median z 0.028); the first 40 lines of its FROZEN_CRITERIA (its OPT/REST/RADIO conversions; it calls ALFALFA's Vhel optical-convention heliocentric); the `cfg304_matched_pairs.csv` header and its first two rows (W50 150/150 and 67/71).
4. **CFG301** `README.md` top; the docstring, `chain()` (`Wc = (W − δ)/(1 + z)^k`, REC0 k = 1), `cut()` (cut (e) uses the **raw** catalogue W50 ≥ 80 km s⁻¹, so the survivor set does not depend on k) and the STAGE-B file I/O lines of `cfg301_width_chain.py`; the tail and the pooled line of `cfg301_stageB.out`.
5. **The catalogue CSV:** the first ten `W_50_km_s` values, plus the fact that every value is an integer (errors too).
6. **File listings:** `../_external_data/arxiv_pdf/2605.28731.pdf` exists (sha256 db936cbc…fc934). `../_external_data/alfalfa_sdss/` holds `ReadMe_Haynes2018_J_ApJ_861_49` and `ReadMe`. There is no Haynes+2018 or Westmeier+2014 source on disk. The four r1p0 sub-cubes are on disk at `../_external_data/mightee_hi_dr1/`.

## 1. Inputs (read-only; each script prints its sha256)
- **Catalogue** `data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv` (sha256 bcf9e8558bc56448…). For T1 also its `README.md` and `catalogue_columns_from_paper.csv`.
- **Catalogue paper** (MM26, arXiv:2605.28731): `$CFG309_PDF`, default `../_external_data/arxiv_pdf/2605.28731.pdf` relative to the repository root, read with `pdftotext -layout`.
- **CFG302** `cfg302_per_galaxy.csv` (sha256 e122665f…) and `cfg302_raw_widths.py` (blob 3f36faef…), imported as a module with `MUTATE=0` forced at import; its `main()` is never called. The cubes come from `$MIGHTEE_R1P0_DIR`, default `../_external_data/mightee_hi_dr1`. File sizes are checked against `FETCH_MANIFEST.jsonl`; the sha256 is not recomputed (CFG302 C-INT already did that).
- **CFG304** `cfg304_matched_pairs.csv` (sha256 297e4789…).
- **ALFALFA documentation (T3a):** `data_assembly/alfalfa_sdss_local_control/columns.md` and `README.md`; `../_external_data/alfalfa_sdss/ReadMe_Haynes2018_J_ApJ_861_49` and `ReadMe`. Only if all of these are silent: the arXiv abstract page of Haynes+2018 (arXiv:1805.11499) through WebFetch. That is a page read, not a download. The prompt will be neutral (no suggested answer), and the result is labelled PROVISIONAL.
- **CFG301** `cfg301_width_chain.py` (blob d11f89e0…) and its committed `cfg301_stageA_results.json`, `cfg301_SELFTEST_results.json`, `cfg301_CC2_results.json`, `cfg301_stageB_results.json`.
- **Constants:** c = 299792.458 km s⁻¹, ν₀ = 1420.40575177 MHz. **z_i = ν₀/ν_i − 1 from `freq_MHz`** (the catalogue's z_HI has only 4 decimals, 3 in one row; CFG304 K2). x_i ≡ log₁₀(1 + z_i).

## 2. The three conversions (definitions used throughout)
For a width of N channels of Δν at observed frequency ν:
- **REST:** W = N c Δν/ν (the galaxy rest-frame velocity width).
- **OBS (optical, observed frame):** W = N c Δν ν₀/ν² = (1 + z) W_REST. This is the width on the observed cz axis, with no (1 + z) correction.
- **RADIO:** W = N c Δν/ν₀ = W_REST/(1 + z). Reported only. If it wins, the outcome is UNDECIDED, because it is neither hypothesis.

The CFG301 chain is correct for a column in OBS (it divides by 1 + z). For a column in REST, the right exponent is k = 0.

## 3. T1 — the paper's text
- **Procedure.** Extract the full text with `pdftotext -layout`. Print every line, with ±3 lines of context, that matches case-insensitively any of: `W ?_?50`, `w50`, `line width`, `velocity width`, `width`, `rest[- ]frame`, `observed[- ]frame`, `1 ?\+ ?z`, `\(1\+z\)`, `optical`, `radio`, `convention`, `cosmolog`, `busy`, `channel`, `km ?/ ?s|km s`. Then read the hits. Also read the catalogue README and `catalogue_columns_from_paper.csv` (the W_50 description).
- **Classification of the statement about the W50 column or the catalogue's velocity widths:**
  - **EXPLICIT-REST:** the widths are stated to be rest-frame, divided by (1 + z), corrected for cosmological broadening, or computed as c Δν/ν_obs.
  - **EXPLICIT-OBS:** the widths are stated to be observed-frame, measured on the optical cz axis with no (1 + z) correction, or not corrected for cosmological broadening.
  - **EXPLICIT-RADIO:** the same for the radio convention.
  - **IMPLICIT-{set}:** a statement fixes the conversion only partly. For example, a channel velocity width "calculated for the given redshift" excludes RADIO (constant per channel) and is compatible with {REST, OBS}.
  - **NOT STATED.**
  - **CONFLICTING:** two explicit statements disagree.
- **Recording.** The verdict and the quoted sentence(s) are written into the script as constants after reading. The script **asserts** that each quoted string occurs in the pdftotext output (whitespace-normalised), so every quote can be checked. A spectral-axis convention used only for redshifts and cz does not by itself count as a width statement.

## 4. T2 — the paper's worked example spectra (independent reproduction of CFG306 F1)
- **Parse.** From the same text, every "W50 [km/s] = X" and "W50 [channels] = Y" (own regex, tolerant of spacing and of brackets/units written differently), every source identifier or RA/Dec printed with each panel, and the channel width Δν in Table 2.
- **Match.** Each example is matched to a catalogue row by its printed MGTH identifier if one is printed. Otherwise by printed position, nearest within 5″. If neither is printed: unmatched, and the example drops out of T2b. ν_i = the matched row's `freq_MHz`, or the frequency or z printed in the panel if there is one (both reported).
- **T2a, conversion.** k_i = X_i/Y_i (km s⁻¹ per channel). For H ∈ {REST, OBS, RADIO}, dev_H,i = k_i/pred_H,i − 1. Example i is **consistent with H** iff |dev_H,i| ≤ 0.002 + ρ_i, where ρ_i = 0.05/Y_i + 0.0005/X_i is the print-rounding allowance; 0.002 covers c ≈ 3 × 10⁵ approximations.
  - **T2a = H** iff all examples are consistent with H and every other hypothesis is inconsistent in ≥ 3 of them.
  - Otherwise T2a is AMBIGUOUS.
- **T2b, the link from the paper's numbers to our column.** For each matched example and each multiplier m ∈ {1, (1 + z_i), 1/(1 + z_i)}, the example is consistent iff |m X_i − W_cat,i| ≤ 0.5 + 0.002 W_cat,i (the column is in integers).
  - **Link = m** iff m is consistent in ≥ 4 of 5 matched examples (≥ all-but-one if fewer than five matched, with a minimum of 3) and no other multiplier reaches that count.
  - Otherwise the link is AMBIGUOUS. Every example's consistent multipliers are reported.
- **T2c, exactness (are the channels the measured quantity?).** If the spread max_i dev_H,i − min_i dev_H,i of the winning T2a hypothesis is ≤ 2 × 10⁻⁴ (far below the 0.07–0.4 % rounding allowance), the printed km s⁻¹ values are exact multiples of the printed channel counts by one conversion: **EXACT**. Otherwise NOT EXACT.
  - **Why it matters:** EXACT excludes the loophole in which a plotting script derived the channel counts from catalogue km s⁻¹ values. That would leave the 0.07–0.4 % channel rounding visible in the per-example deviations.
- **Composition.** paper frame ∘ link = column frame: REST∘1 = REST; REST∘(1+z) = OBS; REST∘1/(1+z) = RADIO; OBS∘1 = OBS; OBS∘1/(1+z) = REST; RADIO∘1 = RADIO; anything ∘ AMBIGUOUS = UNDECIDED.

## 5. T3 — ALFALFA as an external width scale
- **T3a.** Establish from the documentation (section 1) whether ALFALFA α.100 W50 is
  - **ALFA-OBS:** no cosmological correction, or measured on the heliocentric cz (optical) axis;
  - **ALFA-REST:** a (1 + z) correction is stated;
  - or **NOT STATED.**

  The quote is recorded and asserted as in T1. **If NOT STATED, T3 is INADMISSIBLE.**
- **T3b.** Use CFG304's committed pairs with `hi_code == 1`.
  - **Reproduction R3:** N must be 15, and the median of d_i must equal CFG304's C-W50 (+0.000) to 1 × 10⁻⁹. Here d_i = log₁₀(W50_cat,i / w50_A,i), recomputed from the `W50_cat` and `w50_A` columns and checked against `logW50_cat_A` to 1 × 10⁻⁹.
  - **Residuals under each hypothesis.**
    - If ALFA-OBS: r_REST,i = d_i + x_i and r_OBS,i = d_i.
    - If ALFA-REST: r_REST,i = d_i and r_OBS,i = d_i − x_i.
  - **Intervals:** the medians of r_REST and r_OBS, with bootstrap 95 % percentile intervals (B = 10,000 resamples of the pairs, seed 3093, the same indices for both).
  - **Tolerance τ_b = 0.010 dex.** This is the declared allowance for differences in instrumental-broadening correction and method (ALFALFA corrects W50 for instrumental broadening; whether MM26 does is part of T1). H is **excluded** iff its whole 95 % interval lies outside [−τ_b, +τ_b].
  - **T3 vote:** REST iff OBS is excluded and REST is not; OBS iff REST is excluded and OBS is not; otherwise UNDECIDED.
  - **Reported only:** the Theil–Sen slope of d on x (REST predicts −1 under ALFA-OBS; OBS predicts 0); the codes 1+2 set (N 23).
  - **Power, declared:** the two hypotheses differ by the median x over the 15 pairs, about 0.012 dex. That is comparable to the interval half-width, so T3 is expected to be UNDECIDED.
- **Control C-SHUF (can fail).** Over 2,000 permutations of `w50_A` among the 15 pairs (seed 3096), compute the robust scatter (1.4826 MAD) of d. **PASS** iff the real robust scatter is below the 1st percentile of the shuffled distribution. This shows that the pairing carries width information. If C-SHUF fails, T3 is INADMISSIBLE.

## 6. T4 — method-matched cube widths (busy-function fits to our raw r1p0 spectra)
- **Sample.** The CFG302 rows with `primary == 1`, `detected` True and `W50_defined` True (58 expected).
- **Extraction (reproduces CFG302 exactly).** Use CFG302's per-galaxy window, beam θ, R_ap = 1.5θ, O-window exclusion and `aperture_spectrum()` / `measure()` on the global beam arrays, built as in its `main()`.
  - **Control R0 (can fail):** `measure()` on the re-extracted spectrum reproduces the CSV's `W50_rest_kms` and `sigma_ch_mJy` to ≤ 1 × 10⁻⁶ relative for all 58.
- **Rest-frame axis by construction.** v = c (ν_c/ν − 1), with ν_c = the catalogue `freq_MHz` (CFG302's axis). Across a profile it differs from a rest-frame velocity by O(v/c) ≲ 0.1 %.
- **Model (Westmeier+2014 busy function, plus a constant baseline):** B(v) = (a/4)·[erf(b₁(w + v − v_e)) + 1]·[erf(b₂(w − v + v_e)) + 1]·[h |v − v_p|ⁿ / wⁿ + 1] + b₀, with v_p = v_e + d·w.
  - **Primary:** n = 2.
  - **Bounds:** a ∈ [0, 50 P_s] (P_s = the peak of the 3-channel-smoothed window spectrum); b₁, b₂ ∈ [0.005, 2] (km s⁻¹)⁻¹; w ∈ [3, V_fit]; v_e ∈ [−V_fit, V_fit]; d ∈ [−1, 1]; h ∈ [0, 20]; b₀ free. (c = h/wⁿ ≥ 0, so the polynomial term can only make the centre a trough.)
- **Fit window.** |v| ≤ V_fit = max(1.5 W50_ours, 300) km s⁻¹, with W50_ours = CFG302's `W50_rest_kms`. **No catalogue width enters the window or the starting values.**
- **Fit.** `scipy.optimize.least_squares` (trf) on (data − model)/σ_ch, max_nfev 4,000, from 12 starts: w₀ ∈ {0.85, 1.0, 1.15} × W50_ours/2; b ∈ {0.05, 0.2} for both flanks; h ∈ {0, 0.5}; v_e,0 = the centre of `width_rule`'s 50 % interval on the smoothed spectrum; a₀ = P_s/(1 + h₀); d₀ = 0; b₀,0 = 0. The lowest χ² among the converged starts is kept.
- **Width.** Evaluate the fitted B − b₀ on a 0.05 km s⁻¹ grid over [−V_fit − 300, V_fit + 300]. P = its maximum. **W50_busy** = the distance between the outermost crossings of 0.5 P, found from outside in with linear interpolation. W20 is reported the same way.
- **GOOD fit:** `success`; W50_busy finite; both 50 % crossings inside the fit window; reduced χ² ≤ 3; w not within 1 % of its bounds.
- **Statistics on the GOOD set.** Δ_i = log₁₀(W50_busy,i / W50_cat,i). Under REST, E[Δ] = 0. Under OBS, E[Δ] = −x_i.
  - **T4L, level.** m_R = median(Δ) and m_O = median(Δ + x), with bootstrap 95 % intervals (B = 4,000 resamples of galaxies, seed 3094, the same indices for both). **Method tolerance τ_m = 0.010 dex.** H is excluded iff its interval lies entirely outside [−τ_m, +τ_m]. T4L = REST iff OBS is excluded and REST is not; OBS iff the reverse; otherwise UNDECIDED.
  - **T4S, slope (offset-free).** Theil–Sen slope β of Δ on x; bootstrap 95 % interval (B = 2,000, seed 3095; pairs with equal x are skipped). T4S = REST iff the interval contains 0 and excludes −1; OBS iff it contains −1 and excludes 0; otherwise UNDECIDED.
  - **T4 primary vote.** If T4L and T4S agree, that frame. If one votes and the other is UNDECIDED, that vote. If they conflict, UNDECIDED.
  - **Robustness guard.** The T4 vote is recomputed for:
    - V1, NBFLAG == 0 only;
    - V2, n = 4;
    - V3, CFG302's window max(1.5 W50_cat, 300) (catalogue-based);
    - V4, 3-robust-σ clipping of Δ about its median.

    If any variant gives the **opposite** frame, T4 = UNDECIDED. A variant that goes to UNDECIDED is reported and does not change the vote.
  - **Diagnostics (reported, no vote):**
    - Spearman ρ of Δ against z, log(S_win/S_cat) and log W50_cat;
    - OLS of Δ on x with log W50_cat as a covariate;
    - Δ_busy − Δ_CFG302 (the method shift from the non-parametric rule);
    - the catalogue-error pulls.
- **Controls (can fail).**
  - **INJ-A, fit bias.** For every GOOD galaxy and R = 20 realisations, inject CFG302's double-horn shape (`profile_channels`: box W50_cat,i, 25 % trough, edges σ 8 km s⁻¹). Its truth W50_true,i is the rest-frame W50 on the fine grid, its integral is the galaxy's own `S_L_Jy_Hz`, and it is multiplied by the aperture's point-source response, at the galaxy's own frequency on the global channel grid. Add a circular segment of the galaxy's own line-free noise (CFG302's N region, O window excluded; start seed [309, i, r]). Then run the complete T4 pipeline: non-parametric start, V_fit, 12-start fit, GOOD test. **PASS** iff |median over all (i, r) of log₁₀(W50_busy,rec/W50_true)| ≤ 0.005 dex.
  - **INJ-B, frame recovery (power and correctness).** Two mock catalogue columns from the same injections:
    - REST world: W_cat^mock = W50_true;
    - OBS world: W_cat^mock = (1 + z_i) W50_true.

    For each realisation, run the full T4L + T4S + combination rule (primary only). **PASS** iff the REST world returns REST in ≥ 16 of 20 and OBS in ≤ 1 of 20, **and** the OBS world returns OBS in ≥ 16 of 20 and REST in ≤ 1 of 20.
  - **Admissibility.** T4 enters the decision only if R0, INJ-A and INJ-B all pass **and** the number of GOOD fits is ≥ 45 of 58. Otherwise T4 is INADMISSIBLE and treated as UNDECIDED, but its numbers are still reported.

## 7. Decision rule (frozen; three outcomes: "REST-FRAME", "OBSERVED-FRAME", "UNDECIDED")
1. **Paper frame PF**, from T1 and T2a:
   - T1 EXPLICIT-X and T2a = X: **PF = X, grade STRONG.**
   - T1 EXPLICIT-X and T2a AMBIGUOUS: PF = X, grade TEXT-ONLY.
   - T1 IMPLICIT-{set} containing X, or NOT STATED, and T2a = X: PF = X, grade NUMBERS-ONLY.
   - T1 EXPLICIT-X and T2a = Y ≠ X, or T1 IMPLICIT-{set} not containing T2a, or T1 CONFLICTING: **PF = CONFLICT.**
   - T1 not explicit and T2a AMBIGUOUS: PF = NONE.
2. **Documentary column frame DOC** = PF ∘ link (T2b); UNDECIDED if PF ∈ {CONFLICT, NONE} or the link is AMBIGUOUS.
   - DOC is **STRONG** iff DOC ∈ {REST, OBS}, T2a is clean, the T2b link is clean, T2c is EXACT, and T1 is not CONFLICTING. (PF grade STRONG or NUMBERS-ONLY both qualify; TEXT-ONLY does not.)
3. **Data votes:** T3 and T4, each REST / OBS / UNDECIDED; an inadmissible test counts as UNDECIDED.
4. **Outcome X ∈ {REST, OBS}:**
   - **X** iff DOC = X, **and** no admissible data test votes the opposite frame, **and** at least one of:
     - (a) the PF grade is STRONG (T1 explicit and T2a agrees);
     - (b) DOC is STRONG (T2a clean, link clean, EXACT, and T1 not conflicting);
     - (c) an admissible data test votes X.
   - **X** also if DOC = UNDECIDED and **both** T3 and T4 are admissible and vote X.
   - **Otherwise UNDECIDED.** That covers a DOC of RADIO, and any data test that contradicts DOC.
   - **Why (b) is allowed without T1 being explicit:** if the paper's own worked numbers are EXACT multiples of the channel counts under one conversion, and the column equals those numbers, the conversion is pinned down more tightly than a prose sentence would pin it. The data tests can still veto. The decisive path is reported with the outcome (a / b / c / data-only).
5. **CFG306's C1 is CONFIRMED** iff the outcome is REST-FRAME, **REFUTED** iff OBSERVED-FRAME, and **OPEN** iff UNDECIDED.

## 8. Consequence for CFG301 (a labelled variant; CFG301 is not edited)
- **The script.** `cfg309_cfg301chain_FRAME.py` execs CFG301's committed source (blob d11f89e0…, the hash printed and asserted) with `STAGE=B`, `MUTATE=0`, `DRYRUN=0` and `__file__` set to CFG301's script, so it reads CFG301's committed stage-A, SELFTEST and CC2 JSONs.
- **Textual substitutions, each asserted to match exactly once:**
  - (s1) `REC0 = dict(delta=0.0, k=1,` → `k=0,`;
  - (s2) the two output-writing lines are redirected to this folder as `cfg309_cfg301chain_stageB_FRAME.out` / `_results.json`.

  The selection is unchanged, because cut (e) uses the raw W50.
- **Control C-ID (can fail):** the same harness with (s2) only, i.e. k = 1, written as `_IDENTITY`, reproduces CFG301's committed pooled log s\* to ≤ 1 × 10⁻¹² and its window log s\* values likewise.
- **Control C-CONS (can fail):** the k = 0 pooled a₀ agrees with CFG306 P1's 1.3111 × 10⁻¹⁰ to ≤ 0.001 dex.
- **What is reported:** the pooled a₀ and its 68 / 95 % intervals, the windows, the recipe half-width, CC1/CC3 status at k = 0, and the A1 BTFR rows. **Both footings** are given as dex offsets from 9.3603 × 10⁻¹¹ (canonical) and 1.1312 × 10⁻¹⁰ (alt), and as **κ = ½ · a₀ / a₀,footing** (κ = ½ is FITTED).
- **Which number stands.**
  - REST-FRAME: the k = 0 variant replaces CFG301's frame.
  - OBSERVED-FRAME: CFG301's committed 1.046 × 10⁻¹⁰ stands, and the k = 0 run is reported as the refuted variant.
  - UNDECIDED: both numbers are reported as the frame bracket.

## 9. MUTATE (separate outputs, `_MUTATE` suffix; can fail)
- **What changes.** `MUTATE=1` multiplies the catalogue W50 by (1 + z_i) wherever the catalogue width is *compared*: T2b, T3b, T4's Δ (real fits), V3's window excepted. The extraction, noise regions, fit windows, starts and fits are unchanged, and INJ is not re-run (its admissibility is inherited from the main run's JSON). T1, T2a and T2c are unchanged; they describe the paper, not the column.
- **M-a:** the T2b link moves from 1 to (1 + z) (or, from any other link, to that link times 1 + z).
- **M-b:** the per-galaxy shift Δ_MUT − Δ = −x_i to ≤ 1 × 10⁻¹².
- **M-c:** the decision flips.
  - If the main run is REST-FRAME, the MUTATE run must be OBSERVED-FRAME.
  - If the main run is OBSERVED-FRAME, the MUTATE run must be anything but OBSERVED-FRAME (the column is then (1 + z)² W_rest, neither hypothesis).
  - If the main run is UNDECIDED, M-c is reported as not applicable.

## 10. Checks, outputs, hand estimates
- **Checks.** Every check prints as `[PASS]/[FAIL]`, and each run ends with "N/M checks pass". Fails are kept, and nothing is re-run to turn a fail into a pass; any re-run after a code fix keeps the earlier outputs with a `_run1` suffix.
- **Deliverables.**
  - `cfg309_width_frame.py` (main / `MUTATE=1`) → `cfg309_width_frame{,_MUTATE}.out`, `_results.json`, `cfg309_per_galaxy{,_MUTATE}.csv` (fits, Δ, flags, injections);
  - `cfg309_cfg301chain_FRAME.py` → `cfg309_cfg301chain_stageB_FRAME.*` and `_IDENTITY.*`;
  - `README.md`.
- **Paths.** No absolute home path and no personal name in any file; external data is referenced relatively or through `$CFG309_PDF` / `$MIGHTEE_R1P0_DIR`.
- **Hand estimates (written now, scored as they fall).**
  - **HE1:** T1 is not EXPLICIT for W50. The likeliest reading is IMPLICIT-{REST, OBS} from the "calculated for the given redshift" channel-width note.
  - **HE2:** T2a = REST (all five within 0.1 %; OBS excluded in ≥ 3); T2b link = 1 in 4 of 5, with example 1 (catalogue 223 vs 237.858) the odd one out; T2c EXACT.
  - **HE3:** T3a = ALFA-OBS; T3b UNDECIDED; C-SHUF PASS.
  - **HE4:** R0 PASS; INJ-A PASS; INJ-B a coin flip (I lean FAIL: power < 80 % at τ_m = 0.010); ≥ 50 GOOD fits.
  - **HE5:** busy m_R in [−0.020, +0.010]; T4S UNDECIDED (interval wider than 1.5); T4 vote UNDECIDED.
  - **HE6:** outcome REST-FRAME via path (b), about 70 %; UNDECIDED about 30 %; OBSERVED-FRAME under 5 %.
  - **HE7:** the k = 0 a₀ = 1.311 × 10⁻¹⁰ (C-CONS PASS); κ 0.700 / 0.580; C-ID PASS.
  - **HE8:** MUTATE flips REST-FRAME → OBSERVED-FRAME (M-a, M-b, M-c PASS).
