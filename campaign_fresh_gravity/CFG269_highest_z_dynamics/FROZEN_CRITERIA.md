# CFG269 FROZEN CRITERIA: FLAT a0 against the rival a0 ∝ H(z) at z ≥ 4 to z ≈ 14 (scoping + pre-flight)

> **κ = ½ is FITTED. a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) is the rival. ΛCDM has no a₀: the PROXY is CFG222's effective-a₀ curve, reported only. Any outcome of this lane is a DISCRIMINATION between two a₀(z) laws under a declared dynamical estimator and a declared baryon calibration. It is NOT a measurement of a₀. No sentence of this lane says the data favour the framework.**

Written 2026-10-01, **before any observed D was computed in this lane** (no script exists yet). Not committed: the orchestrator commits, or not. The script prints this file's sha256 and refuses to run stage B if the file is missing.

**What I had seen when writing this (not blind):**
- the committed D, y and δ values of the reused lanes in the rows I printed while reading their files: CFG271 (all six HZ9 rows), CFG272 (all rows), CFG276 (all six GN20 rows), CFG277 (all seven rows), the first three CFG273 rows, CFG228's seven galaxies (including its committed δ_H(z)), and CFG220's per-disc table (δ_flat and δ_rival);
- the record's verdicts for those lanes (STANDING, READMEs);
- for the new census (z ≳ 8), nothing from the papers yet: the census was delegated to page-read helpers whose reports had not arrived when this file was written. Memory-level numbers for JADES-GS-z14-0 (M★ ~ 10^8.7, r_e ~ 260 pc) were used only for hand estimate H1.

## 0. Scope (owner's extension, relayed by the coordinator on 2026-10-01, folded in before any D_obs)
- **Redshift range:** z ≥ 4 to z ≈ 14, ranked by redshift.
- **Bins:** B1 = [4, 6), B2 = [6, 8), B3 = [8, 15].
- **Reused rows (no re-derivation):** the committed D (or δ) and y of CFG220 (CRISTAL, independent route; CFG213's fit route is quoted beside it), CFG228, CFG229, CFG271, CFG272, CFG273, CFG276 and CFG277, for every row with z ≥ 4. Lanes with no z ≥ 4 row are listed as contributing none.
- **New rows (census):** z ≳ 8 galaxies (and any 6 ≤ z < 8 or 4 ≤ z < 6 galaxy that the census finds with a published table) that have BOTH:
  - (a) a measured kinematic quantity (emission-line σ or FWHM from a resolving grating or ALMA, a velocity gradient, or a published dynamical mass with its method);
  - (b) a stellar mass and a size r_e.
- **Excluded from scoring, but listed with the reason:** widths dominated by an AGN broad line, an outflow or a merger, by the authors' own statement; prism-only (R ~ 100) widths; objects without r_e.

## 1. Laws, kernels, footings
- a₀: canonical 9.3603e-11 m s⁻² (primary) and alternative 1.1312e-10 m s⁻².
- FLAT: a₀(z) = a₀.
- RIVAL: a₀(z) = a₀ E(z), with E(z) = √(0.3 (1+z)³ + 0.7) (primary). Ωm = 0.315 (CFG223's curve) is a sensitivity and is also used for the control that reproduces committed δ_H(z).
- Kernels: ν_mono(y) = 1/(1 − exp(−√y)) (primary); P2 ν(y) = √(1 + 1/y).
- PROXY (reported only): CFG222's `lcdm_native` (Z1 `zcommon.py`). It is an EXTRAPOLATION of the Dutton & Macciò 2014 concentrations above z = 5.

## 2. Definitions (one row = one object, one baryon branch, one radius)
- y = g_bar/a₀ at the row's radius.
- D_pred,L = ν(y/E_L), with E_FLAT = 1 and E_RIVAL = E(z).
- **Gap** G = log₁₀ D_pred,RIVAL − log₁₀ D_pred,FLAT (≥ 0). G depends on the baryons, not on any observed velocity.
- **Residual** r_L = log₁₀ D_obs − log₁₀ D_pred,L.
- **Calibration:** one common multiplicative shift 10^x on all baryons gives r_L(x) = log₁₀ D_obs − x − log₁₀ ν(10^x y/E_L). The calibration error on law L is σ_cal,L = |r_L(+c) − r_L(−c)|/2.
  - **c = 0.15 dex (primary):** the HZQ lanes' inner band.
  - **c = 0.30 dex (sensitivity, gate G1):** their outer band.
  - CFG228 uses its own committed per-galaxy S_inner and S_outer on δ_FLAT; for the rival these are scaled by (1 − β_R)/(1 − β_F), where β = −d log ν/d log y.
- **Total:** σ_L = √(σ_stat,L² + σ_cal,L²). For census rows the estimator term is inside σ_stat (section 3).
- **Position:** z_L = r_L/σ_L (signed).
- **Power:** P = G / max(σ_F, σ_R). P does not depend on the central D_obs.

## 3. Uncertainties
**Reused rows: each lane's own committed numbers.**
- **HZQ lanes (CFG271/272/273/276/277):** σ_stat is taken from the committed 68% interval of δ_FLAT, using the side that faces the prediction: (δ − lo68) if r_L > 0, (hi68 − δ) if r_L < 0. The same log-D widths are applied to r_RIVAL.
- **CFG228:** σ_stat = the committed per-galaxy SD of δ_FLAT (`cfg228_preflight_results.json`, PG.sd).
- **CFG220 (CRISTAL independent route):** no per-disc error is committed. σ_stat = 0.25 dex per disc: CFG220's realised per-disc scatter, the only committed per-disc number. CFG234's larger bracket (gas ×1/3 to ×3, M★ ±0.2 dex) is quoted, not used.

**Census rows: Monte Carlo of the published errors.**
- N = 20,000 draws, fixed seed.
- Inputs: line width or M_dyn, M★, gas if measured, r_e, and inclination where the estimator uses it. Each is drawn split-normal in the quantity as published.
- **Estimator coefficient K:**
  - primary: the paper's K, with a lognormal scatter of 0.15 dex (the factor-2 bracket taken as ±2σ);
  - gate G3: separate runs at K/2 and 2K, without the K scatter.
- σ_stat = the half-width of the 16–84% range of r_L on the side facing 0.

**Census D_obs.** D_obs = M_dyn(<r) / M_bar(<r), at the radius r the paper's estimator uses.
- Baryons: M_bar(<r_e) = M_bar/2 (half-light = half-mass).
- Dynamics: M_dyn(<r_e) = M_dyn,tot/2 when the paper's M_dyn is a total mass; the paper's value directly when it is an enclosed mass.
- g_bar(r) = G M_bar(<r)/r², spherical.
- When the paper gives a line width but no M_dyn: M_dyn,tot = K σ² r_e/G with K = 5, a declared default with the same bracket. Here σ = FWHM/2.355 after the paper's instrumental correction.
- When the paper gives both, the paper's M_dyn is primary. The recomputation from σ is control C8: it must agree within 0.1 dex, or the row is flagged.

**Baryon classes, never pooled together:**
- COMPLETE: stars plus a measured or tracer-based gas mass.
- LOWER-LIMIT: stars only, or gas only with the stars missing.

## 4. Decision thresholds, per row
Primary cell: ν_mono, canonical, c = 0.15, the paper's K.
- **P ≥ 2: SEPARATES** (the two laws' predictions are at least 2σ apart under this error budget).
- **1 ≤ P < 2: MARGINAL.**
- **P < 1: NOT POSSIBLE.**

**Position.** Reported for every row: "closer to L" means the smaller |z_L|.

**Discrimination statement.** Made for SEPARATES rows only:
- "RIVAL DISFAVOURED at |z_R|σ" if |z_R| ≥ 2 and |z_F| < 2;
- "FLAT DISFAVOURED" if |z_F| ≥ 2 and |z_R| < 2;
- "BOTH DISFAVOURED" if both are ≥ 2;
- "BETWEEN" if both are < 2.

**Robustness gates.** Each is reported. A statement is ROBUST only if every gate that applies passes.
- **G1:** the same statement holds at c = 0.30.
- **G2:** the same statement holds in all four cells (ν_mono and P2, each at both footings).
- **G3 (census only):** the same statement holds at K/2 and at 2K.
- **G4 (LOWER-LIMIT rows):** missing baryons only lower D_obs and raise y, so r_L(x > 0) < r_L(0) for both laws. A "disfavoured" statement about law L therefore survives missing baryons only if r_L < 0, i.e. the law predicts MORE discrepancy than observed. If r_L > 0 the statement is labelled GAS-LIMITED and the baryon shift x*_L that zeroes r_L is reported.
- **G5 (FLOOR rows, D_obs < 1 at nominal):** ν ≥ 1 for both laws, so D < 1 is first a baryon or g_obs inconsistency.
  - A FLOOR row is NEVER counted as a discrimination.
  - Reported for it: x*_F and x*_R, and whether the outer band alone (x = −0.30) restores the rival, i.e. r_R(−0.30) ≥ 0 or |z_R(−0.30)| < 2. If it does, the label is "the floor does not discriminate".

## 5. Pooled per bin
**Row selection.** One row per object:
- the lane's RECOMMENDED CHART ROW, if the lane defines one;
- otherwise the headline row with the most complete baryons (stars + gas > gas only > stars only);
- if two branches are equally complete (for example two M★ routes), both pooled variants are computed. The statement must agree between them, or it is labelled BRANCH-DEPENDENT.

**Duplicates.** An object that appears in two lanes counts once:
- CRISTAL-20 = DC494057 = HZ4: the CFG220 row is used, not the CFG228 row;
- otherwise, the lane with the more complete baryons.

**Classes.** COMPLETE and LOWER-LIMIT rows are pooled separately. The bin's verdict is the COMPLETE pool's, if one exists. The LOWER-LIMIT pool supports a statement only under G4.

**Statistic:**
- r̄_L = Σ w r_L / Σ w, with w = 1/σ_stat²;
- σ_pool,L² = 1/Σw + (mean σ_cal,L)². The calibration is treated as fully common-mode: it does not average down;
- P_bin = Ḡ_w / max(σ_pool,F, σ_pool,R); z_pool,L = r̄_L/σ_pool,L;
- the unweighted median r_L is reported beside.

**Thresholds and gates.** The same thresholds as section 4. A pooled discrimination statement additionally needs:
- G1 and G2;
- agreement with the FLOOR rows included (primary, so that no row is dropped on its outcome) and excluded (sensitivity);
- branch agreement.

## 6. MUTATE (the owner's control)
- **Census rows:** every observed line width × 1.7, i.e. M_dyn × 2.89 (+0.461 dex). Where the paper's M_dyn is used, M_dyn × 2.89.
- **Reused rows:** D × 2.89.
- **Expected:**
  - every r_L rises by log₁₀ 2.89 = 0.4609 (exactly for reused rows; MC median within 0.01);
  - P is unchanged;
  - positions move toward the rival (rows with r_R < 0 lose |z_R|, rows with r_F ≥ 0 gain |z_F|).
- The MUTATE run writes separate outputs (`*_MUTATE.out` / `*_MUTATE_results.json`). The check C6 passes iff the shifts and the P invariance hold.

## 7. Controls (the script exits 1 if any fails)
- **C1:** r_FLAT recomputed from each HZQ row's committed (D, y) equals its committed δ_FLAT within 1e-4. CFG228's dFLAT and dHz are reproduced within 1e-4, with CFG223's Ωm = 0.315 E(z) for dHz.
- **C2:** CFG220's per-disc δ_flat and δ_rival are reproduced from the README's D_ind and y to within 0.006, its rounding; the E(z) form is chosen as in CFG220 and stated.
- **C3:** ν_mono(1) = 1.581977, P2(1) = √2.
- **C4:** E(14) = 31.8308 (Ωm = 0.3).
- **C5:** the PROXY reproduces CFG222's 1.23 / 1.77 / 2.16 at z = 1 / 2 / 2.5, 4.52 at 4.5 and 6.20 at 5.5.
- **C6:** MUTATE as in section 6.
- **C7:** with all errors set to zero, the census MC returns the closed-form D_obs and y.
- **C8:** the recomputation of the paper's M_dyn, where both σ and M_dyn are published (flag, not exit).

## 8. Hand estimates (made BEFORE any D_obs; predictions only; scored afterwards, misses kept)
- **H1.** A z ≈ 14.2 compact galaxy at y ≈ 5.5 (M★ ~ 10^8.7, r_e ~ 260 pc): D_F ≈ 1.11, D_R ≈ 2.96, G ≈ 0.43 dex (computed). At y = 3: G ≈ 0.50.
- **H2.** No single z ≥ 8 census object reaches P ≥ 2 (P ≈ 0.8 to 1.4: stellar-mass errors ≥ 0.3 dex plus the 0.15 dex K scatter plus the line-width error). Probability 0.8.
- **H3.** B3 pooled (N ≤ 6, mostly LOWER-LIMIT): P_bin ≈ 1.5 to 2.3 at c = 0.15 and ≈ 1.0 to 1.4 at c = 0.30. SEPARATES at the primary cell with probability 0.35; no ROBUST statement survives G1 with probability 0.8.
- **H4.** B1 (z 4–6): G ≈ 0.2 to 0.4. Single COMPLETE rows have P < 2 (σ_stat 0.2 to 0.4). The COMPLETE pool sits BETWEEN the laws and gives no statement that survives G1 (probability 0.75). The LOWER-LIMIT pool (Danhaive, HZ9) sits at or above the rival and is GAS-LIMITED under G4.
- **H5.** B2 (z 6–8): too few rows; NOT POSSIBLE or MARGINAL (probability 0.8).
- **H6.** HZ9 [M986] (z 5.54, y 0.41; its D is seen): G ≈ 0.40, P ≈ 1.8 to 2.1; position closer to the rival, but GAS-LIMITED (stars only, r_R > 0).
- **H7.** The PROXY lies within about 15% of the rival at z ≥ 10 (computed: 17.6 against 20.0 at z = 10, 32.6 against 31.8 at z = 14). So at z ≥ 8 any statement about the rival applies to this proxy too, and the proxy is not ΛCDM.

## 9. What is reported
For every row:
- z, class, y (both footings), D_pred,F, D_pred,R, G, D_obs, r_F, r_R, σ_F, σ_R, z_F, z_R, P;
- the verdict, the position, the gate results;
- FLOOR / GAS-LIMITED labels;
- x*_F and x*_R.

For every bin: the pooled values. The dominant systematic is named per row and per bin, as the term with the largest contribution to max(σ_F, σ_R). ΛCDM: the PROXY residual is reported per row. The dark-matter fraction inside r_e is given from a published ΛCDM source if one is found, otherwise marked UNKNOWN.

## Addendum 1 (2026-10-01, appended; sections 0-9 above are unchanged)
**Transcription error in section 1, found by the frozen control C1 failing on the first test run.** Section 1 wrote ν_mono(y) = 1/(1 − exp(−√y)). That formula is ν_RAR. The record's ν_mono is something else: it is FP1's committed monotone repair of ν_RAR (`CFG4_common.nu_mono`, a tabulated function), the kernel adopted by the 2026-09-26 decision.
- The two kernels are equal at y ≲ 2: 1.58198 at y = 1, 1.32121 at y = 2.
- Above that, ν_mono is larger: 1.2170 against 1.2150 at y = 3; 1.1322 against 1.1197 at y = 5; 1.0678 against 1.0442 at y = 10; 1.0271 against 1.0061 at y = 26.
- With ν_RAR, C1 reproduced the committed δ_FLAT only to 1.0e-2 at high y. With ν_mono it reproduces them as frozen.

**Correction.** The primary kernel is the record's ν_mono, imported read-only from `CFG4_common`. ν_RAR is kept as a fifth cell (nu_RAR, canonical), reported only and not used in any gate. Every threshold, gate and pooling rule above is unchanged.

**Provenance of the test run.**
- The test run that exposed this wrote stage-B outputs into this directory. Only the stage-A head of its terminal output (predictions) and the check summary were displayed to me. I did not read its stage-B rows.
- The three files it wrote (`cfg269_discriminate.out`, `cfg269_results.json`, `cfg269_rows.csv`) were deleted before this addendum.
- No census row existed at that time: the census helpers had not reported.

**Hand estimate H1** used ν_RAR (D_F ≈ 1.106 at y = 5.5). With ν_mono, D_F ≈ 1.12. It is scored as written.
