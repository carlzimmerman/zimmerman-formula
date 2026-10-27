# CFG406 FROZEN CRITERIA: re-score CFG687's outer-lensing mass slope (T2) and X43's cluster keys with CFG816's Eddington-corrected eRASS1 gas masses

Committed alone, with its LEDGER row, before any script exists. κ = ½ FITTED; not theory closed. Cold dark energy, never a particle. Footings are never pooled. Nothing here says the data favour the framework. Owner (2026-10-27): "Yes, write frozen criteria for re-scoring CFG687's outer slope (and X43's group and cluster keys) with CFG816's Eddington-corrected gas masses." ID CFG406 is a spare in the owner's 10-06 block 400–409, chosen by the owner.

## Why
- **CFG687 T2** (criteria 12cb826e8): "FOLLOWS NEWTON". The outer ΔΣ (1.2–3 Mpc) scales as Mgas500^s with s_obs = 0.90 ± 0.21, against s_law = 0.47 and s_Newton = 0.84. A_OUTER by observed-gas tercile is 0.57 / 0.96 / 1.38. Mechanism (a), Eddington bias in the flux-limited eRASS1 gas masses, was left open.
- **CFG816** (criteria 4eef19bc8) measured the ingredients on CFG687's own 318 clusters: α = 2.029 ± 0.114, per-cluster σ_i from the catalogue bounds, median M_true/M_obs 0.29 / 0.84 / 0.95 by tercile. It never applied them to T2 or to the OUTER band.
- **X43** (criteria 00bc1a7950) fails two keys, groups (Z +2.05) and G-OUT-M3 (MGAS T3 OUTER, Z +2.41), both as UNDER-predictions.
- Motivation, by analogy only: arXiv:2507.10544 (faint outskirts and faint objects are biased; CFG405). No number from that paper enters here.

## Scope: what this lane can and cannot touch
- **In scope:** every quantity that is built from eRASS1 Mgas500. That means CFG687's law and Newton predictions (318 clusters), and X43's cluster keys through the X30/X7 machinery (326 clusters: 15 keys, KT and MGAS splits, all bands).
- **Out of scope, stated:** **X43's groups key.** Its 63 groups come from Tian et al. (`_external_data/vizier2026/J_A_A_710_L39.tsv`: dispersions and optical masses), not eRASS1 X-ray gas, so CFG816's correction does not apply. The groups grade is carried unchanged (Z +2.05) and is not re-scored. SPARC is untouched.

## The correction (CFG816's, as committed; nothing refitted)
- σ_i = ½(ln hi − ln lo) from `_external_data/cfg687_inputs/erass1_main.tsv` (columns 6/7 around column 5), with α = 2.0291 taken from `CFG816_erass1_eddington/cfg816_results.json`.
- **E1 (primary):** ln M_true = ln M_obs − α σ_i².
- **E½ (bracket):** half the shift. CFG816's own README says −ασ² likely overstates the bias at σ ≈ 0.8.
- **E0:** no shift (the identity path).
- **Matching:**
  - CFG687's 318 clusters: nearest catalogue row in (RA cos δ, δ), as CFG816 did. CFG816's matched σ must be reproduced exactly (K2).
  - X7/X30's 326 clusters: by catalogue name, falling back to the nearest row within 10″. All must match, or the lane is INVALID.
- **R500 is unchanged** (used as the shape scale and aperture). The correction moves the gas mass only. The stars stay at f_s × gas, as each model already defines them.
- **Bins stay on OBSERVED mass.** Terciles and every slope x-axis use the observed Mgas500 (the selection quantity), never the corrected one. This avoids CFG816's admitted artefact that re-binning by corrected mass manufactures trends. Only the model predictions change.

## Part A (PRIMARY, graded): CFG687 T2 on its own estimator
- The data stack (D, E, weights, jackknife patches) is read from `CFG687_erass1_shear_stack/cfg687_percluster.npz`. No shear is re-measured.
- Predictions are recomputed per cluster with CFG687's `law()` verbatim (canonical and alt at b 0.67, rc 0.15, f_s 0.20, and Newton). Its dependencies (RGRID, RC, sigma_proj, ν_mono, A0, constants, BAO-raw distances) come from CFG686's setup, exec'd without the KiDS column loads.
- **Statistic:** CFG687's `slope()`, the 3-tercile log–log fit of the OUTER stack against log median observed Mgas500. s_obs = 0.90 ± 0.21 is unchanged by construction. s_law,E and s_N,E are recomputed. Also reported: A_OUTER per tercile with the jackknife, and Δs = s_obs − s_law,E.
- **Classification:** CFG687's T2 rule verbatim, with the corrected s_law,E and s_N,E: FOLLOWS THE LAW / FOLLOWS NEWTON / NOT DECIDED, per footing.
- **Shuffle null (CFG816's MUTATE, promoted to a null):** 200 permutations of σ_i across the 318 clusters (`default_rng(406)`), at E1. **SPECIAL** if |Δs_E1| is below the 5th percentile of the null |Δs| on both footings, i.e. the effect needs each cluster's own error, not a generic stretch. Null draws may use a per-cluster ln-mass interpolation grid (≥ 41 nodes over the needed range), validated against direct `law()` to ≤ 0.2 % at E1 (K3).

**Part A reading (frozen):**
- **SELECTION RESOLVES T2:** under E1, T2 = FOLLOWS THE LAW on both footings, AND under E½ T2 ≠ FOLLOWS NEWTON on both, AND E1 is SPECIAL.
- **SELECTION PARTLY:** under E1, T2 moves off FOLLOWS NEWTON on both footings, but the full condition above fails. The README names which part failed.
- **NOT RESOLVED:** T2 is still FOLLOWS NEWTON under E1 on either footing.

## Part B (SECONDARY, graded separately): X43's cluster keys
- X43 (`rebuild_2026_10_22/X43_collapse_core_floor/x43_collapse_core.py`) is exec'd as committed (c_f = 4, η = 14.83, both footings, both h cells). One injection is made: immediately after X30's `CL = NS2["CL"]`, each cluster's `Mgas500` is multiplied by its E-factor. Every prediction and every in-run baseline (DC, X30's in-run measured statistics) is then recomputed. T3M and TID keep their observed-mass and KT edges.
- **Stored X7 calibrated values** (G-OUT-Mall, G-OUT-M1..3: A_CAL, s_CAL from x7 results) are rescaled by R = Σ baseline_old / Σ baseline_new over the same clusters and band. This is exact only if A, leak_t and the error terms share the baseline denominator. That is checked (K5) on X30's in-run recomputed statistics. If K5 fails, those four keys are graded but marked APPROXIMATE.
- **Grades:** all 15 keys, |Z| ≤ 2 in both h cells to pass, as X43. Reported at E0 (must equal X43), E½ and E1.

**Part B reading (frozen):**
- **X43 GAINS:** under E1, the failing cluster keys are a strict subset of X43's (G-OUT-M3), with no new failure.
- **X43 HOLDS:** the same failing set.
- **X43 LOSES:** any new cluster-key failure. The README names it and its sign; an UNDER-prediction at the light tercile is the disclosed expectation.

The groups key is reported as unchanged (Z +2.05) in every row.

## Controls (Part A and Part B each must pass its own, or that part is INVALID)
- **K1 (A):** at E0 the recomputed law and Newton predictions equal the stored `PL` / `PN` to ≤ 1e-9 relative, and s_law = 0.47, s_N = 0.84, s_obs = 0.90 ± 0.21, T2 = FOLLOWS NEWTON (canonical) are reproduced.
- **K2 (A):** the per-cluster σ_i equal CFG816's matching bit for bit, and the median E1 factors per observed tercile are 0.29 / 0.84 / 0.95 to the printed precision.
- **K3 (A):** the null interpolation is within 0.2 % of direct `law()` at E1, for every cluster and bin.
- **K4 (B):** at E0 the injected X43 path reproduces every committed X43 cluster cell (meas, s, pred, Z; both footings, both h cells) to ≤ 1e-9. This is a real identity through the injection, not a self-comparison. (CFG816's K1 compared a quantity with itself; this lane does not repeat that.)
- **K5 (B):** under E1, X30's in-run recomputed KT and M_terc measured A and s equal old × R to ≤ 1e-6. Failure only marks the stored-X7 keys APPROXIMATE.
- **MUTATE (A, rc 1):** shift the sign (ln M_true = ln M_obs + α σ_i²). Δs must move the other way (|Δs| grows) on both footings.

## Not blind (disclosed)
Before freezing I computed by hand: with ΔΣ_law ∝ M^0.47 and CFG816's tercile medians, A_OUTER 0.57 / 0.96 / 1.38 → ≈ 1.02 / 1.04 / 1.41 under E1. **Expectation:** T2 moves toward the law. In X43, G-OUT-M3 is unchanged or slightly worse (×0.95 on the heavy gas), and the light-tercile keys may turn UNDER. CFG816's tercile medians and X43's/CFG687's committed outputs have been seen. No corrected prediction has been computed.

## Disclosed inherited inputs (not changed here)
- **Part A** uses CFG687's own inputs: BAO-raw distances, the β-model normalised to the catalogue Mgas500, f_s 0.20. It uses no ΛCDM background and no Planck ratio.
- **Part B re-scores X43 as committed.** X43/X30's `prep()` uses Mfair = 5.364 × M_b, Ω_c = 5.364 Ω_b at H0 67.4 for r_ta, and a ΛCDM D_A ratio (`DA_lcdm`) in its distance conversion. These conflict with the owner's 10-25 rule ("ΛCDM IS NONSENSE, DO NOT USE IT"). They are X43's and are flagged here, not fixed. Part B's grades inherit that caveat, and the README says so in its first lines.
- **CFG816's caveats carry over:** the correction is a lognormal power-law approximation; selection acts on count rate, not on M_gas (no count-rate forward model here); σ_i comes from the catalogue bounds.

## Statement-change rule
- Only CFG687's T2 line and X43's failing-key list in STANDING / LEDGER may change, and only per the frozen readings.
- No a0 value, no "favours", and no groups change.
- A "SELECTION RESOLVES T2" reading lets the record say that the law's √M outskirts are not contradicted by T2 once the faint-cluster gas masses are corrected. It does not say that the law is confirmed.

## Compute and files
Single thread (nice), CPU only, minutes (Part A ~3–5 min with the null; Part B 3 × ~46 s), RSS < 1 GB, no downloads. This is allowed under the small-job rule while the X48 runs are live. Script `cfg406_rescore.py` (Part A and B; `MUTATE=1` for Part A's sign flip). Outputs: `cfg406.out`, `cfg406_results.json`, `_MUTATE` siblings, README. Nothing is written outside this directory. X43's log redirect goes to `cfg406_x43_machinery.log` here.
