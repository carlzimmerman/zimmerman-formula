# CFG304 — FROZEN CRITERIA: which HI flux scale is right for MIGHTEE-HI COSMOS, the published catalogue's S_HI or the raw r1p0 cube fluxes (CFG302)? Arbiter: the single-dish Arecibo ALFALFA α.100 S21

**This file is committed before any per-galaxy flux value has been read** (no MIGHTEE `S_HI_Jy_Hz`, no CFG302 `S_win_Jy_Hz`, no ALFALFA `s21_jykms` row in or near COSMOS). Lane launched by the orchestrator (CFG ID 304).

> **A flux-calibration check, not an a₀ measurement.** No new a₀ is fitted. The only a₀ numbers are a reported consequence: CFG301's committed baryon-band rows interpolated at the measured flux offset (section 7). At z ≤ 0.06 nothing here can separate FLAT from a₀ ∝ H(z). κ = ½ is FITTED. No knob scans. No downloads. No other lane's file is edited.

## 0. What has been read before this file (disclosure)
1. **Column headers** of the three CSVs below, and their documentation: `data_assembly/alfalfa_sdss_local_control/columns.md` and `README.md` (incl. its catalogue-wide medians, e.g. S21 1.26 Jy km/s over all 31,500 rows), `data_assembly/mightee_hi_catalogue_2026-10-02/README.md` and `catalogue_columns_from_paper.csv`.
2. **CFG302's README and the top of its FROZEN_CRITERIA**, incl. their aggregate numbers: cube/catalogue flux median −0.30 dex (ratio 0.50) over 58 frozen detections, 0.22 over all 179; PH2 −0.385 dex at S/N_L ≥ 2.48; cube widths −0.022 dex vs the catalogue; the catalogue median S_HI of 658 Jy Hz over CFG302's 188-source sample. No per-galaxy row was looked at.
3. **CFG301's committed numbers** (not fluxes): pooled s\* = 1.1171 (a₀ = 1.0456 × 10⁻¹⁰ m s⁻²) and the pooled baryon-band rows s\* = 2.4430 / 1.6561 / 0.7369 / 0.4534 at τ_b = −0.30 / −0.15 / +0.15 / +0.30 (`cfg301_stageB_results.json`, `numbers/results/pooled`); its pooled median gas fraction 0.70 (`cfg301_stageA.out`); and its `chain()` code, which shows **τ_b multiplies gas AND stars at fixed R** (`Mg, Ms = Mg·10^τ_b, Ms·10^τ_b`; R from M_HI is not moved).
4. **The orchestrator's count** (positions and velocities only, no fluxes): 23 MIGHTEE sources with an ALFALFA counterpart within 1′ and 300 km/s.

## 1. Inputs (read-only; the script prints the sha256 of each)
- **MIGHTEE catalogue** `data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv` (293 rows; sha256 prefix bcf9e8558bc56448 expected). Columns used: `ID_catalogue, RA_deg, Dec_deg` (optical-counterpart position), `freq_MHz, z_HI, D_L_Mpc, S_HI_Jy_Hz, S_HI_Jy_Hz_err, log_M_HI, W_50_km_s, W_50_km_s_err` and the five flags.
- **CFG302 per-galaxy CSV** `campaign_fresh_gravity/CFG302_mightee_cube_raw_widths/cfg302_per_galaxy.csv` (the un-suffixed, final main-run file). Columns: `ID, primary, detected, snr_L, S_win_Jy_Hz, S_win_err_Jy_Hz, W50_obsframe_kms, W50_defined, S_cat`.
- **ALFALFA α.100 + Durbala** `data_assembly/alfalfa_sdss_local_control/alfalfa_sdss.csv` (sha256 c790a7ec68c45b66a86be1bc6317b9b29da6b8736baa013e97af21fb40599ed2 expected). Columns: `agc, ra_hi_deg, dec_hi_deg, ra_oc_deg, dec_oc_deg, vhel_kms, s21_jykms, e_s21_jykms, w50_kms, e_w50_kms, hi_code, snr`.
- **CFG301** `cfg301_stageB_results.json` (pooled s\*, a₀ and bands; the canonical a₀ is taken as a₀/s\* from the same JSON) and the "gas fraction median" of the pooled line of `cfg301_stageA.out`.

## 2. Matching rule
- **M1 positions:** MIGHTEE `RA_deg, Dec_deg` against ALFALFA **`ra_hi_deg, dec_hi_deg`** (the HI centroid). Great-circle separation θ; **θ ≤ 60″**.
- **M2 velocity:** cz_M = c · z_HI (z_HI = ν₀/ν − 1 is the optical-convention redshift) against `vhel_kms` (optical convention, heliocentric); **|cz_M − vhel| ≤ 300 km s⁻¹**. Barycentric/heliocentric differences (< 0.1 km s⁻¹) are ignored.
- **M3 candidates:** every ALFALFA row with finite positions and vhel, **all hi_codes**. The code cut is applied after matching, so a code-2 counterpart is never replaced by a more distant code-1 one.
- **M4 one-to-one:** all candidate pairs sorted by θ (ties by |Δcz|), assigned greedily; each MIGHTEE source and each ALFALFA row is used at most once. A MIGHTEE source whose candidates were all taken by closer MIGHTEE sources is listed as LOST (it shares an ALFALFA beam) and is not a pair.
- **M5 sets:** **ALL** = pairs with hi_code ∈ {1, 2}; **C1** = hi_code 1 = **the PRIMARY set**; code 2 reported. Flux statistics need 0 < s21 < 900 and the MIGHTEE flux > 0 (logs).
- **M6 variant (reported, no vote):** the same rule against the ALFALFA optical-counterpart position `ra_oc_deg, dec_oc_deg`.

## 3. Confusion flag
**CONF = 1** for a matched MIGHTEE source t if another source of the **full** MIGHTEE catalogue (all 293 rows, any flags) lies within **210″ (3.5′)** of t and **|cz_n − cz_t| ≤ W50_t + 200 km s⁻¹**, W50_t = t's catalogue `W_50_km_s`. **CLEAN** = CONF 0. The MIGHTEE `blended_flag`/`confused_flag` and a GOLDEN subset (all five flags 0) are reported as variants. Disclosure: CONF sees only MIGHTEE-catalogued neighbours; gas-poor or undetected neighbours, and anything outside the MeerKAT footprint, are invisible to it.

## 4. Unit conversion (Jy Hz → Jy km s⁻¹)
ν₀ = 1420.40575177 MHz, c = 299792.458 km s⁻¹, ν_obs = the catalogue `freq_MHz` (also for CFG302's S_win).
- **OPT (primary):** ALFALFA integrates S21 on its heliocentric cz axis, which is the **optical** convention (as `vhel_kms`). On that axis dv = c ν₀ dν/ν², so **S_V = S_ν · c ν₀ / ν_obs² = S_ν · (c/ν_obs)(1 + z)**. This is the like-for-like conversion. Assumption, disclosed: the CSV cannot prove that ALFALFA's spectral axis is optical cz; the α.100 documentation describes Vhel that way.
- **REST (the brief's formula, reported with its own decision):** Δv = c Δν/ν_obs, the galaxy rest-frame width: S_V = S_ν · c/ν_obs. OPT − REST = log₁₀(1 + z) = +0.009 to +0.025 dex at z 0.02–0.06.
- **RADIO (reported):** S_V = S_ν · c/ν₀; OPT − RADIO = 2 log₁₀(1 + z).
- **U1 unit check:** the catalogue's `log_M_HI` against log₁₀(49.7 D_L² S_HI) (M_HI = 49.7 D_L² ∫S dν, D_L in Mpc, S in Jy Hz): **median |Δ| ≤ 0.03 dex** over all 293 rows; the signed median is reported.

## 5. Statistics
- **R_cat = log₁₀(S_cat,OPT / s21)**; **R_cube = log₁₀(S_win,OPT / s21)**.
- **Catalogue sets:** C1 (primary), ALL, CLEAN-C1, CLEAN-ALL, GOLDEN-C1, code 2 alone.
- **Cube set:** pairs whose MIGHTEE source is in CFG302's primary set with **`detected` True (frozen S/N_L ≥ 5)** and S_win > 0, by the same C1 / ALL / CLEAN splits. Variants (reported): CFG302's post hoc PH2 threshold S/N_L ≥ 2.48; all CFG302-primary matched sources (linear median ratio, non-detections included).
- **Per set:** N, the **median**, **bootstrap 68 % and 95 % percentile intervals** of the median (B = 10,000 resamples of pairs, `numpy.random.default_rng(304)`, one generator per set in a fixed order), mean, robust scatter (1.4826 MAD), and pull outliers |S_M − S_A| / √(σ_M² + σ_A²) > 3 (errors as published, converted like the fluxes).
- **Paired:** on each cube set, R_cat on the same galaxies and the paired difference R_cube − R_cat (an echo of CFG302's −0.30 dex).
- **Widths:** log₁₀(W_50_km_s / w50_kms) on every catalogue set (catalogue W50 as published; its frame convention is undecided by CFG302, ± 0.025 dex); log₁₀(W50_obsframe_kms / w50_kms) on the cube sets (width-defined only; CFG302's observed-frame width = rest × (1+z), the optical axis).
- **Beam-summed variant (reported):** S_sum = Σ catalogue S_HI,OPT over all MIGHTEE sources within 210″ of the ALFALFA HI centroid with |cz_n − vhel| ≤ w50_A/2 + 100 km s⁻¹; R_sum = log₁₀(S_sum / s21).
- **Reported trends:** Spearman ρ of R_cat against the ALFALFA `snr` and against z.

## 6. Decision rule (frozen)
On the **PRIMARY set C1 with OPT**:
- **"catalogue scale confirmed"** iff |median R_cat| ≤ 0.10 dex **and** median R_cube ≤ −0.15 dex;
- **"cube scale confirmed"** iff |median R_cube| ≤ 0.10 dex **and** median R_cat ≥ +0.15 dex;
- **"neither"** iff |median R_cat| > 0.10 **and** |median R_cube| > 0.10;
- **"undecided"** otherwise;
- **minimum size:** N_cat ≥ 8 and N_cube ≥ 5, else "undecided (insufficient pairs)".

**Robustness votes:** the same rule on **CLEAN-C1** (votes only if N_cat ≥ 5 and N_cube ≥ 3, else "insufficient", no vote) and on **C1 with REST**. **HEADLINE** = the C1-OPT decision if every voting variant gives the same decision; otherwise "undecided (depends on confusion / convention)". ALL (codes 1+2), RADIO, M6 and GOLDEN are reported and do not vote.

**Strength label** (does not change the decision): "firm" if the bootstrap 68 % intervals of both medians lie wholly inside the regions the decision needs (e.g. catalogue confirmed: R_cat 68 % within [−0.10, +0.10] and R_cube 68 % upper end ≤ −0.15), else "marginal".

## 7. Consequence for CFG301 (reported; CFG301 is NOT re-run)
If ALFALFA is right, CFG301's catalogue HI masses are off by median R_cat (C1, OPT), so the true baryons sit at **τ = −median R_cat**.
- **(A) Total-baryon reading** (what the band rows are, and what the chart's 2.29 × 10⁻¹⁰ hollow diamond used): s\*(τ) by linear interpolation of log₁₀ s\* over the pooled nodes τ = −0.30, −0.15, 0, +0.15, +0.30 (s\* 2.4430, 1.6561, 1.1171, 0.7369, 0.4534); a₀ = s\* × a₀,canonical. The 68 % interval of R_cat is carried through the same map. |τ| > 0.30 → "outside the band rows, not extrapolated".
- **(B) Gas-only reading:** an HI-flux error moves only the gas, so τ_eff = log₁₀(f_g · 10^τ + 1 − f_g) with f_g = 0.70 (CFG301's pooled median gas fraction), then the (A) map at τ_eff. Approximations, disclosed: a single median f_g; R's dependence on M_HI through the size relation is ignored (it cancels in the deep limit, where a₀ ∝ V⁴/M_b, and all 47 CFG301 galaxies are deep, y ≤ 0.084).
- **Chart note (reported):** the cube-scale hollow diamond re-read with (B) at τ = −0.30 (gas only).

## 8. Checks (every row printed as `check(...)`; final line "N/M checks pass")
- **K1** input sha256: ALFALFA equals the value above; MIGHTEE starts bcf9e8558bc56448.
- **K2** catalogue z_HI = ν₀/freq − 1 to ≤ 1e-5 for all rows.
- **K3** CFG302's `S_cat` equals the catalogue `S_HI_Jy_Hz` for every joined ID (relative ≤ 1e-6).
- **K4** U1 (section 4).
- **K5** match quality on C1: median |Δcz| ≤ 50 km s⁻¹ and median θ ≤ 40″.
- **K6** the number of MIGHTEE sources with ≥ 1 candidate (before M4) within 2 of the orchestrator's 23.
- **C-W50 (control i):** |median log₁₀(W50_cat / w50_A)| ≤ **0.05 dex** on C1.
- **C-W50cube (sanity):** |median log₁₀(W50_cube,obs / w50_A)| ≤ 0.07 dex on the C1 cube set.
- **C-SHUF (control ii):** K = 200 shuffles; each MIGHTEE source moved by **10′** at an independent uniform position angle (`default_rng(3041)`), M1–M4 redone against all ALFALFA rows. Pass iff the **mean matches per shuffle ≤ 1.0** and the maximum ≤ 3.
- **D-MIN** the primary set meets the minimum size of section 6.
- **MUTATE (control iii), separate outputs** (`MUTATE=a|b|c`, every output name carries the mode). Each MUTATE run first recomputes the unmutated decision in memory, then the mutated one:
  - **MUTATE=a, the brief's literal mutation: catalogue S_HI × 0.5.** Pass iff every set's median R_cat moves by log₁₀ 0.5 = −0.30103 (to 1e-9), every R_cube is unchanged (to 1e-12), and the C1-OPT decision differs from the unmutated one. **Frozen note:** the brief expects a flip to "cube scale confirmed", but under this rule halving the catalogue cannot produce that from any state where the cube sits below the catalogue: from (R_cat, R_cube) ≈ (0, −0.30) it lands at (−0.30, −0.30), i.e. **"neither"** (and at "undecided" from a cube-confirmed state). So the frozen prediction is "neither" if the main run confirms the catalogue.
  - **MUTATE=b, the flip test: ALFALFA s21 × 0.5** (a world where the arbiter sits on the cube scale). If the unmutated decision is "catalogue scale confirmed", pass iff the mutated one is **"cube scale confirmed"**.
  - **MUTATE=c: ALFALFA s21 × 2.** If the unmutated decision is "cube scale confirmed", pass iff the mutated one is "catalogue scale confirmed".
  - If the unmutated decision is "neither" or "undecided", b and c are reported without a pass/fail row.

## 9. Hand estimates (written before the run, scored as they fall)
- **HE1** N(ALL) 21–24 (orchestrator 23); N(C1) 15–21; N(CLEAN-C1) 8–17; N(C1 cube set) 6–15.
- **HE2** median R_cat (C1, OPT) in **[−0.12, +0.05]**, central −0.03 (single-dish slightly above: confusion, and ALFALFA-selected pairs are boosted near its limit).
- **HE3** median R_cube (C1, OPT) in **[−0.45, −0.20]**, central −0.33.
- **HE4** decision **"catalogue scale confirmed"**.
- **HE5** W50 catalogue/ALFALFA in [−0.05, +0.03] dex; cube/ALFALFA in [−0.08, +0.02].
- **HE6** shuffled mean 0.0–0.5 matches per shuffle.
- **HE7** MUTATE=a → "neither"; MUTATE=b → "cube scale confirmed".
- **HE8** implied CFG301 a₀: (A) 0.95–1.20 × 10⁻¹⁰; (B) 0.98–1.15 × 10⁻¹⁰.
- **HE9** chart note: the cube-scale hollow diamond under (B) ≈ 1.7 × 10⁻¹⁰ (against 2.29 × 10⁻¹⁰ under (A)).
- **HE10** U1 passes with median |Δ| ≤ 0.01 dex.

## 10. Deliverables
`cfg304_flux_scale_alfalfa.py` (this lane's only script); `cfg304_flux_scale_alfalfa.out` and `_results.json`; `cfg304_matched_pairs.csv`; the MUTATE outputs `*_MUTATE_a|b|c*` (out, JSON, pairs CSV); `README.md`. If anything is re-run, the first outputs are kept with a `_run1` suffix and the change is described in the README.
