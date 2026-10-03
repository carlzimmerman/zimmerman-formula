# CFG301 — the MIGHTEE-HI catalogue width chain: the local level is s\* = 1.12 (a₀ = 1.05 × 10⁻¹⁰ m s⁻²), CALIBRATED by the frozen rule on unmatched windows, with no measurable drift across 185–368 Mpc

**Bottom line.** The CFG260/281 width → V → baryon chain was run on the 47 MIGHTEE-HI COSMOS galaxies that survive the frozen cut (z 0.027–0.093). It uses the catalogue W50, the catalogue inclinations, the BAGPIPES stellar masses and R = D_HI/2.
- **Pooled level:** s\* = 1.117, i.e. a₀ = 1.046 × 10⁻¹⁰ m s⁻²; bootstrap 68 % 1.012–1.145, 95 % 0.936–1.311 × 10⁻¹⁰; recipe half-width 0.143 dex. That is −0.060 dex from the SPARC-empirical scale (1.282), +0.048 dex from the canonical a₀ (9.3603 × 10⁻¹¹) and −0.034 dex from the alt a₀ (1.1312 × 10⁻¹⁰).
- **Calibration:** all three controls pass, so the chain is **CALIBRATED** by the frozen rule. CC1: the nearest window gives s\* = 1.233, −0.017 dex from 1.282 and −0.070 dex from CFG281's 1.449, with a recipe half-width of 0.136. CC2: the SPARC closure of the baryon side is +0.008 dex. CC3: the drift from W1 to W3 is −0.057 dex.
- **Caveat on CC1 and CC3:** both were evaluated on **unmatched** windows. The script's blind matching rule found too few nearby galaxies in W3's upper mass bins, so mass matching was not possible.
- **Distance trend:** slope −0.20 per dex of D_L (68 % −0.67 to +0.08). The ALFALFA trend in CFG281 has the same sign but this one is not resolved.
- **The lane cannot separate FLAT from a₀ ∝ H(z).** The rival's lever between W1 and W3 is +0.009 dex, against a statistical width of 0.136 dex. This lane measures the chain's local level and its drift with distance, nothing more.
- κ = ½ is FITTED. No sentence here says the data favour a law.

## The numbers (canonical footing; s\* = a₀/9.3603 × 10⁻¹¹; bootstrap over galaxies, B = 4,000)

| set | N | z median / median D_L | s\* | a₀ (10⁻¹⁰ m s⁻²) | 68 % (s\*) | 95 % (s\*) | recipe half-width | baryon bands −0.30/−0.15/+0.15/+0.30 |
|---|---|---|---|---|---|---|---|---|
| W1 | 16 | 0.042 / 185 Mpc | 1.233 | 1.154 | 1.117–1.402 | 1.030–2.041 | 0.136 | 2.74 / 1.86 / 0.79 / 0.49 |
| W2 | 16 | 0.067 / 300 Mpc | 1.089 | 1.019 | 0.995–1.232 | 0.820–1.401 | 0.139 | 2.35 / 1.61 / 0.72 / 0.45 |
| W3 | 15 | 0.081 / 368 Mpc | 1.081 | 1.012 | 0.834–1.428 | 0.498–1.522 | 0.135 | 2.34 / 1.60 / 0.70 / 0.42 |
| pooled | 47 | — | **1.117** | **1.046** | 1.081–1.223 | 1.000–1.401 | 0.143 | 2.44 / 1.66 / 0.74 / 0.45 |

- **Regime.** All 47 galaxies are deep: y = g_bar/a₀ at D_HI/2 has quartiles 0.028 / 0.033 / 0.042 and a maximum of 0.084. The median gas fraction is 0.70.
- **Recipe knobs** (pooled, half-width in dex): δ = 11 km s⁻¹ 0.106; M\* ± 0.25 dex 0.086; D_HI ± 0.15 dex 0.026; H₀ = 67.4 0.036. Their quadrature is **0.143**. The isotropic sin 60° sensitivity is 0.026; including it gives 0.146.
- **Bootstrap shape.** The window intervals are lumpy and asymmetric, because a median of 15–16 galaxies jumps between galaxies; W3's 95 % interval spans a factor of three.
- **The alt footing implies the same absolute a₀** (M1, to 7 × 10⁻¹⁷). On the alt footing the pooled s\* is 0.924.

## Calibration status (frozen section 3; evaluated before the a₀ lines were printed)
- **CC1 — PASS.** The nearest window W1 gives s\* = 1.233: −0.017 dex from 1.282 and −0.070 dex from CFG281's 1.449. Its recipe half-width is 0.136, or 0.142 with sin 60°; both are ≤ 0.20.
- **CC2 — PASS.** 123 SPARC galaxies (Q ≤ 2, i ≥ 30°, V_flat > 0) with M_b = 1.33 M_HI + 0.5 L[3.6], R = D_HI/2 from the size relation and g_obs = V_flat²/R give s\* = 1.304 (95 % 1.119–1.443): +0.008 dex.
  - Using the measured R_HI instead of the relation gives 1.324; the size relation is unbiased on SPARC (median offset −0.002 dex).
  - The table was read from `SPARC_Lelli2016c.mrt` through `CFG4_common.load_sparc`; SPARC_table.txt was never read.
- **CC3 — PASS.** log s\*(W3) − log s\*(W1) = −0.057 dex, inside the ≤ 0.10 tolerance.
  - **This pass has little power.** The statistical width of the drift (0.136 dex) is larger than the tolerance, and the 95 % range of the drift is roughly ± 0.27 dex.
- **CC4 (SELFTEST) — PASS.** In 100 worlds with fabricated widths at s_true = 2 (0.15 dex scatter in g_obs, 10 % width errors, catalogue inclinations), the bias is −0.013 dex against a tolerance of 0.023, and the 95 % interval covers s_true in 93 of 100. The real widths were not loaded.
  - Reported only: applying the W50 ≥ 80 km s⁻¹ cut to fabricated widths on the 50-galaxy parent gives a bias of −0.020 dex.
- **D1: CALIBRATED**, with the unmatched-window caveat in the disclosures below. This lane wrote no chart row; whether a local-calibration point goes on the chart is the orchestrator's call.

## A1 — the direct BTFR rows: a₀_BTFR = V⁴/(G M_b), the owner's raw request

| sample | N | median (m s⁻²) | 68 % | 95 % | vs canonical 9.3603e-11 | vs alt 1.1312e-10 | recipe half-width |
|---|---|---|---|---|---|---|---|
| (i) all survivors | 47 | 1.251e-10 | 1.187–1.348e-10 | 1.092–1.528e-10 | **+0.126 dex** (68 % +0.103 to +0.158) | **+0.044 dex** (68 % +0.021 to +0.076) | 0.123 |
| (ii) gas-dominated, M_gas > M\* | 37 | 1.187e-10 | 1.109–1.251e-10 | 1.017–1.446e-10 | **+0.103 dex** (68 % +0.074 to +0.126) | **+0.021 dex** (68 % −0.008 to +0.044) | 0.128 |
| (iii) deep, y < 0.5 at D_HI/2 | 47 | 1.251e-10 | 1.187–1.348e-10 | 1.092–1.543e-10 | **+0.126 dex** | **+0.044 dex** | 0.123 |

- **The recipe half-width** is the quadrature of M\* ± 0.25 dex (0.074 / 0.046 for (i) / (ii)), sin 60° (0.017 / 0.032) and δ = 11 km s⁻¹ (0.097 / 0.115).
- **Samples (iii) and (i) are the same 47 galaxies,** because every survivor has y ≤ 0.084. Their 95 % upper ends differ only through the bootstrap seed.
- **The gas-dominated median differs from the deep one by −0.023 dex.**
- **Why the BTFR rows sit above the s\* rows.** V⁴/(G M_b) equals a₀ only in the exact deep-MOND limit. Under ν_mono (the exponential-RAR shape in this regime), a galaxy at y ≈ 0.03 shows V⁴/(G M_b) ≈ a₀ · y ν² ≈ 1.19 a₀. The kernel factor computed from the baryons alone is **1.197 (+0.078 dex)** at the canonical a₀ and 1.172 at 1.20 × 10⁻¹⁰.
  - So even sample (iii) carries about +0.07–0.08 dex from the kernel, and the s\* estimator removes that.
  - On SPARC the same recipe's BTFR level is 1.526 × 10⁻¹⁰ (+0.212 dex vs canonical), while SPARC's s\* closure is 1.304. MIGHTEE's row (i) is −0.086 dex below SPARC's BTFR level, in step with its s\* being −0.067 dex below SPARC's closure.
  - This diagnostic was added after STAGE=CC2 and before the measurement (baryons only; see Disclosures).

## The drift (D3, D4)
- **Slope** of log₁₀ s\* against log₁₀ D_L over W1/W2/W3 (185 / 300 / 368 Mpc): **−0.20** (joint bootstrap median −0.25; 68 % −0.67 to +0.08; 95 % −1.25 to +0.35).
  - Matching was not possible, so the primary and the unmatched variant coincide.
- **Ratios to W1:** ρ(W2/W1) = 0.883 (log −0.054 ± 0.087 stat., recipe width of log ρ 0.034; pull −0.62σ, −0.58σ with recipe). ρ(W3/W1) = 0.877 (log −0.057 ± 0.136; recipe 0.018; pull −0.42σ).
- **Against CFG281** (ALFALFA, 20–85 Mpc): CFG281 fell by 0.105 dex between 20–50 and 50–85 Mpc, a factor of about two in distance. MIGHTEE's slope has the same sign and its 68 % range includes both zero and CFG281's informal −0.37 per dex. The two samples, catalogues and stellar-mass steps differ; this is a comparison, not a joint fit.
- **D4, an extrapolation and not a result.** If the slope continued from W3 (368 Mpc) to the BUDHIES distance (z 0.196, D_L 958 Mpc), it would give Δ log s\* = −0.085 dex (68 % −0.28 to +0.03; 95 % −0.52 to +0.15). BUDHIES/ALFALFA log ρ = −0.746 (CFG281). A continued MIGHTEE trend would account for about 0.1 dex of that deficit, and for at most about 0.5 dex at the 95 % edge.
- **FLAT vs a₀ ∝ H(z):** the rival predicts +0.009 dex between W1 and W3, which is unmeasurable here. This lane says nothing about a₀(z).

## Controls (each script run ends "N/M checks pass")
- **Stage A, 5/5.** Loader (293 rows, 43 columns in order, sha256 bcf9e8558bc56448); estimator bit-identical to CFG223's original and to cfg260_core; equal-count windows. Reported: the M_HI identity to 0.006 dex and D_L equal to flat ΛCDM at H₀ 70 to 0.45 %.
- **SELFTEST, 3/3.** IDs equal stage A's; the noiseless identity holds to 2 × 10⁻¹⁶ dex; CC4 passes.
- **CC2, 2/2.** The loader reads the .mrt; the CC2 closure passes.
- **Stage B, 7/7.** IDs; no galaxy dropped; M1; CC1–CC4 rows. The calibration rows are findings and are not load-bearing.
- **MUTATE=1, 3/3.** Widths × 1.1892 raise the pooled s\* by **+0.322 dex**, inside 0.30 ± 0.05; the galaxies placed on the law respond by +0.324.
- **MUTATE=2, 3/3.** sin i_eff = 0.70 against the sin 60° variant gives **+0.392 dex**, inside 0.37 ± 0.06; the regime expectation is +0.398.
- **M5, 3/3.** This script's chain equals CFG281's committed `chain_core` exactly and reproduces CFG281's s\* exactly: unmatched 1.332408 and matched 1.449173, |Δ| = 0.

## Hand estimates (A3, frozen before any value was read), as they fell
- HE1: N = 47 in 40–120, **hit** (the ~70 point estimate was high).
- HE2: s\*(W1) = 1.233 in 1.4 ± 0.3, **hit**.
- HE3: |log s\*(W3)/s\*(W1)| = 0.057 ≤ 0.3, **hit**.
- HE4: CC2 at +0.008 dex, within ± 0.2, **hit**.
- HE5: deep-subset BTFR median 1.25 × 10⁻¹⁰ in 0.7–2.0 × 10⁻¹⁰ (estimate 1.2), **hit**.
- HE6: gas-dominated minus deep = −0.023 dex, within ± 0.15, **hit**.

## Disclosures (everything kept)
1. **Before the freeze** only the CSV header line was read, plus the data folder's provenance notes. Those notes give row counts in a z range and flag totals, but no width, velocity, mass or flux value.
   - Criteria: `FROZEN_CRITERIA.md`, commit 2555ab142, sha256 884d0b27…a62d. It is the calc chat's draft 37d1d049a kept in full plus amendments A1–A3.
2. **The frozen text does not define "mass-matched".** The script fixed the rule (I2) before any value was read: W1 and W2 are matched to W3's log M_HI quartile bins, and matching needs at least 3 window galaxies per bin.
   - Stage A found W1 with 8/3/2/2 galaxies per bin and W2 with 4/3/6/2, so **matching was NOT POSSIBLE**. CC1, CC3 and the slope therefore use the **unmatched** windows.
   - W1's median log M_HI (9.61) is 0.16 dex below W3's (9.76). A reader who insists on matching should treat CC1 and CC3 as not evaluable as written. Under that reading the CALIBRATED label rests on CC2 and the unmatched numbers.
3. **Recipe half-width (I3).** The draft's knobs are δ = 11 (one-sided), M\* ± 0.25, D_HI ± 0.15 (counted once) and H₀ = 67.4 (one-sided), combined in quadrature. The draft calls sin 60° a "sensitivity", so it is reported but not used in CC1(ii). Including it changes nothing (0.142 ≤ 0.20).
4. **a₀ constants.** The run uses FP0's full-precision values (9.3603248 × 10⁻¹¹ and 1.1312035 × 10⁻¹⁰), as CFG260/281 do. hzq_core's rounded constants differ by 3 × 10⁻⁶; an assertion caught the mismatch before stage A ran.
5. **DRYRUN.** Before the one measurement, the STAGE=B code was run on fabricated widths (law at s = 2; real widths not loaded). This caught one bug (a JSON key name); outputs `cfg301_stageB_DRYRUN*`.
   - Before any run, control B2 was changed from a quartile-closeness test to a structural one: exact per-bin draw counts. It never ran, because matching was not possible.
6. **The BTFR kernel-factor line** was added after STAGE=CC2 (which showed SPARC's BTFR level at +0.21 dex) and before the measurement. It uses baryons only.
7. **M_HI identity constant.** Stage A's identity check uses 49.7 D_L² S[Jy Hz], a form from memory; it is not load-bearing and passed to 0.006 dex.

## What this lane cannot say
- **It cannot test FLAT against a₀ ∝ H(z):** at z ≤ 0.093 the lever is 2–4.5 % in a₀, and +0.009 dex between W1 and W3. It gives the chain's local level and its distance drift only.
- **Inputs are catalogue values, not resolved kinematics:**
  - integrated-profile W50 (busy-function fit) with no turbulence correction (δ = 0 primary; the δ = 11 km s⁻¹ knob is the largest recipe term);
  - optical g-band inclinations with q₀ = 0.2;
  - BAGPIPES stellar masses;
  - an HI size–mass relation and a point mass at D_HI/2;
  - distances without flows.
- **The sample is small, HI-selected and mass-limited at high z.** N = 47, with windows of 15–16 galaxies; the window medians are lumpy and CC3 has little power.
- A calibrated local level does not show the chain is right at z = 0.2 (BUDHIES).
- κ = ½ is FITTED.

## Files (all untracked except `FROZEN_CRITERIA.md`)
- `FROZEN_CRITERIA.md` (committed 2555ab142) and `FROZEN_CRITERIA_DRAFT.md` (37d1d049a).
- `cfg301_width_chain.py`. Run in this order: `STAGE=A`, `STAGE=SELFTEST`, `STAGE=CC2`, `STAGE=B`, `STAGE=B MUTATE=1`, `STAGE=B MUTATE=2`, `STAGE=M5`. The code test is `DRYRUN=1 STAGE=B [MUTATE=1|2]`. The SELFTEST takes about 2 minutes; every other stage takes seconds.
- Outputs: `cfg301_stageA.out/_results.json`, `cfg301_SELFTEST.*`, `cfg301_CC2.*`, `cfg301_stageB.*`, `cfg301_stageB_MUTATE1.*`, `cfg301_stageB_MUTATE2.*`, `cfg301_M5.*`, `cfg301_stageB_DRYRUN*.*`.
