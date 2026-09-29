# CFG170 — the two-epoch gas-ratio test: the gas evolution each a₀ law needs between KROSS (z ≈ 0.85) and KURVS (z ≈ 1.5)

- **Criteria:** frozen in `CFG170_FROZEN_CRITERIA.md` (1caae1adb), before any break-even of this lane was computed.
  - The lane analyses data already seen: six earlier lanes used these samples, as the criteria state first.
- **Script:** `CFG170_two_epoch_gas_ratio.py`, about 12 s.
  - It runs CFG141's pipeline read-only and unmutated in every mode.
  - It uses CFG160's P4 functions verbatim, with KURVS's ten discs (measured σ_out) and KROSS's 390 discs (σ₀, R = 2 r_im).
- **Runs:**
  - The main run passes both controls and exits 0. The headline is reported.
  - MUTATE=1 sets R_obs to R_flat at s = 1, with the in-repo bracket's relative width. Flat is then "not disfavoured", as required; exit 0.
  - MUTATE=2 sets R_obs to 10 × R_flat. Flat is then "disfavoured", as required; exit 0.
  - The first run had an implementation error, disclosed below. Its outputs are kept as `*_firstrun*`.

## Bottom line

**NON-DIAGNOSTIC. Both laws need the cold-gas fraction to rise about threefold between z ≈ 0.85 and 1.5, so the ratio cannot tell them apart. The two measured brackets for that rise also disagree with each other.**

- **Above Kretschmer's prescription (s = 1.42–3.00),** flat needs R = 2.97–3.10 and the rival 2.60–3.57.
  - The two requirements differ by only 0.01–0.06 dex, against a 0.28-dex bracket. The test has no power there.
- **At Kretschmer's prescription (s = 1),** the laws separate by 0.56 dex: flat needs 3.3 [2.0, 5.7] and the rival 11.9 [1.6, open].
  - The rival's interval is open above because KROSS's rival break-even sits at μ = 0.05, next to the search floor. At μ = 0.01 its Δ′ is still only +0.0065 ± 0.020.
- **The in-repo bracket** (PHIBSS exponent 0.23 ± 0.52) gives R_obs = 1.00, 2σ [0.73, 1.39]. It disfavours BOTH laws at every s ≥ 1.
- **The literature bracket** (ABSTRACT-LEVEL: (1+z)^2.5 M*^−0.36, ±20% allowance) gives R_obs = 2.02 [1.61, 2.42]. It disfavours NEITHER law at any s.
- **The frozen summary:** no law is disfavoured by both brackets at s = 1, so the verdict is NON-DIAGNOSTIC.

| s (prescription) | μ_be flat: KURVS / KROSS | R_flat | μ_be rival: KURVS / KROSS | R_rival | in-repo: flat / rival | literature: flat / rival |
|---|---|---|---|---|---|---|
| 0 (none) | no break-even / no break-even | — | no break-even / no break-even | — | — | — |
| **1.00 (Kretschmer)** | **2.109 [1.596, 2.705] / 0.636 [0.478, 0.805]** | **3.32 [1.98, 5.66]** | **0.621 [0.289, 1.006] / 0.052 [< 0.01, 0.185]** | **11.9 [1.56, open]** | **disfavoured / disfavoured** | **not / not** |
| 1.42 (Dalcanton & Stilp) | 3.096 [2.423, 3.887] / 0.998 [0.820, 1.188] | 3.10 [2.04, 4.74] | 1.257 [0.822, 1.766] / 0.352 [0.211, 0.504] | 3.57 [1.63, 8.39] | disfavoured / disfavoured | not / not |
| 1.62 (fixed height) | 3.565 [2.808, 4.462] / 1.166 [0.979, 1.367] | 3.06 [2.06, 4.56] | 1.567 [1.076, 2.144] / 0.494 [0.344, 0.655] | 3.17 [1.64, 6.23] | disfavoured / disfavoured | not / not |
| 1.69 (Price n = 1) | 3.730 [2.942, 4.665] / 1.225 [1.035, 1.429] | 3.04 [2.06, 4.51] | 1.676 [1.165, 2.279] / 0.544 [0.391, 0.707] | 3.08 [1.65, 5.83] | disfavoured / disfavoured | not / not |
| 3.00 (self-gravitating) | 6.845 [5.407, 8.611] / 2.301 [2.050, 2.569] | 2.97 [2.11, 4.20] | 3.829 [2.873, 4.994] / 1.475 [1.267, 1.698] | 2.60 [1.69, 3.94] | disfavoured / disfavoured | not / not |

- Brackets are 1σ root-find intervals. "Not" means not disfavoured.
- At s = 0 neither sample has a break-even under either law. Without a pressure correction, Δ′ < 0 already at μ = 0.01.
- **Calibration scatter (s = 0.6 and 1.4 × Kretschmer):**
  - R_flat = 4.26 and 3.11.
  - R_rival has no break-even at s = 0.6 (the rival over-predicts KROSS even at μ = 0.01) and is 3.63 at s = 1.4.

## Reading

- **The ratio cannot separate the laws** (a finding about the statistic, stated after the data).
  - Each law reaches a sample by setting its own absolute gas level. The rival's level is lower at both epochs, because its a₀ is higher.
  - The pure gas ratio then comes out nearly the same for both laws: within 0.06 dex at s ≥ 1.42.
  - In (1 + μ) the laws do differ (flat 1.90, rival 1.54 at s = 1), but the measured quantity is the gas ratio.
- **Both laws need a steeper gas rise than the in-repo relation gives,** and one within reach of the abstract-level literature scaling. There are two explanations, and this lane cannot tell them apart:
  - a common KURVS–KROSS offset in the pipeline, from the terms declared as not cancelling: the pressure at x = 1.0–3.5 against x = 1; the outermost-point velocity against the model velocity; σ_out against σ₀; the selections;
  - an in-repo exponent biased low, because the PHIBSS z ≈ 1.2 and z ≈ 2.2 samples are selected differently.
- **The separation is in the absolute gas at z ≈ 0.85, not in the ratio** (post-hoc, unscored).
  - At s = 1, KROSS's break-evens are μ = 0.64 [0.48, 0.81] for flat and 0.05 [< 0.01, 0.19] for the rival.
  - At s = 1.42–1.69 they are 1.00–1.23 for flat and 0.35–0.54 for the rival. With 390 discs, the intervals are tight.
  - But KROSS's own gas is not measured here (declared untested).
  - CFG162's pressure–gas degeneracy applies to KROSS as well: flat's KROSS break-even at s = 1 (0.64 [0.48, 0.81]) overlaps the rival's at s = 1.62–1.69 (0.49–0.54, with upper edges 0.66–0.71).
  - A test of KROSS's gas would need a frozen pressure prescription and a measured z ≈ 0.85 gas prior, and it would be post-hoc with respect to these rows.
- **The a₀(z) front stays where CFG162 put it:** the verdict turns on the outer pressure support and the total cold gas, and neither is measured for these discs. Two epochs do not break that degeneracy.

## What cancels and what does not (as frozen)

- **Cancels, largely:** the α_CO and M* scale systematics; the SPARC anchor, applied identically; part of the prescription's normalisation.
- **Does not cancel:** the pressure at different radii; the selections; the instruments and velocity definitions; the dispersion inputs; the stellar-mass pipelines.

## Controls

- **C1:** KURVS's break-evens at s = 1 reproduce CFG162's committed values: 2.1089 flat and 0.6211 rival.
- **C2:** KROSS's anchor-corrected Δ′ at μ = 0.67, s = 1 reproduces CFG161's post-hoc row: −0.0042 flat and −0.0821 rival.
- **R0 (power):** 0.56 dex at s = 1, against the 0.28-dex log-width of the in-repo 2σ bracket; 0.01–0.06 dex at s = 1.42–3.00.
- **MUTATE=1 and MUTATE=2:** as above. Each is a pinned control of the evaluator, and each behaves.

## Disclosed departures

1. **The first run had an implementation error.** Its outputs are kept as `CFG170_two_epoch_gas_ratio_firstrun.out` and `_firstrun_results.json`.
   - It reported "no break-even" whenever any ±σ edge root was missing. But the frozen text defines R_law from the two central break-evens, and reserves "no break-even" for a missing central root.
   - One row was affected: the rival at s = 1, whose KROSS +σ root lies below the μ = 0.01 floor.
   - The fix computes R whenever both central roots exist. A missing edge root lies outside [0.01, 30], so it makes that side of the interval OPEN (R_lo → 0 or R_hi → ∞), and an open side never disfavours.
   - No verdict depends on this convention: the only open edge, the rival's R_hi at s = 1, faces away from both brackets.
   - The headline is the same in both runs. The rival's s = 1 row changed from "no break-even" to "disfavoured (in-repo) / not disfavoured (literature)".
2. **The first run printed the power row after the matrix,** contrary to the frozen "printed before any comparison". It is now printed before the matrix, in every mode, and it also reports the separation at the other values of s.
3. **The medians were computed at run time, as frozen.**
   - The (1 + z) ratio is 1.3669; the frozen text used 1.3676, for z = 1.53 and 0.85.
   - The mass factors are 0.935 (in-repo) and 0.923 (literature), for median log M* of 10.14 (KURVS) and 10.04 (KROSS).
4. **The frozen rule reduces to interval overlap.** A law is disfavoured if and only if its 1σ R interval misses the bracket. This is algebra on the frozen rule, stated for clarity; nothing was changed.

## Untested (declared)

- the curvature term of the literature relation;
- δ_MS differences between the samples;
- KROSS's gas (only the break-even is used);
- pressure beyond the placed prescriptions;
- the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.
