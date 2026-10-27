# CFG406: Eddington-corrected eRASS1 gas masses. T2 SELECTION PARTLY; X43 HOLDS

**Read first:** Part B re-scores X43 as committed. X43/X30's `prep()` uses Mfair = 5.364 M_b, Ω_c = 5.364 Ω_b at H0 67.4 for r_ta, and a ΛCDM D_A conversion. These conflict with the owner's 10-25 rule and are flagged, not fixed. Part A uses none of them (BAO-raw distances, gas β-model + f_s 0.20).

Criteria `FROZEN_CRITERIA.md` were committed alone, with the LEDGER row, in 3e2e282e11. Script `cfg406_rescore.py` was committed before its first run, in 0dd5cccb60. It ran once: single thread, niced, 300 s (Part A 50 s; three X43 children of 84 s each), peak RSS 0.68 GB. MUTATE was a separate run. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**The correction** is CFG816's (α = 2.0291), applied per cluster: ln M_true = ln M_obs − α σ_i². E1 is the full shift, E½ half, E0 none. Bins and slope x-axes stay on **observed** Mgas500; only the predictions change.

## Part A (primary): CFG687 T2, 318 clusters, CFG687's own estimator

**Controls 3/3 PASS:**
- K1: E0 reproduces the stored predictions exactly (max relative difference 0), with s_law 0.466, s_N 0.836, s_obs 0.896 ± 0.209, FOLLOWS NEWTON.
- K2: CFG816's matching reproduces its printed tercile medians, σ 0.786 / 0.291 / 0.158 and correction 0.286 / 0.843 / 0.950. CFG816 stored no per-cluster σ, so this is the strongest check available.
- K3: the null interpolation is within 3.3e-5 of direct `law()`.

**MUTATE** (sign-flipped correction): |Δs| 0.43 → 2.26 on both footings, rc 1.

| | s_law | s_Newton | Δs = s_obs − s_law | T2 (rule verbatim) | A_OUTER by observed tercile (light / middle / heavy), canonical | alt |
|---|---|---|---|---|---|---|
| E0 (= CFG687) | 0.466 | 0.836 | +0.430 | FOLLOWS NEWTON | 0.57 ± 0.20 / 0.96 ± 0.12 / 1.38 ± 0.15 | 0.52 / 0.88 / 1.27 |
| E½ | 0.577 | 0.967 | +0.318 | NOT DECIDED | 0.73 ± 0.27 / 1.03 ± 0.13 / 1.40 ± 0.15 | 0.66 / 0.95 / 1.29 |
| E1 | 0.634 | 1.027 | +0.262 | NOT DECIDED | 0.83 ± 0.31 / 1.09 ± 0.14 / 1.43 ± 0.15 | 0.76 / 0.99 / 1.31 |

(s_obs = 0.90 ± 0.21 in every row. The alt footing's slopes match canonical to ±0.004 and give the same classes.)

**Null (σ shuffled across clusters, 200 draws):** null |Δs| 5th percentile 0.379 / 0.382. E1 gives 0.262 / 0.264, which **no draw reaches**. **SPECIAL:** the shift needs each faint cluster's own large error, not a generic stretch of the mass scale.

**Reading (frozen): SELECTION PARTLY.** E1 moves T2 off FOLLOWS NEWTON on both footings, E½ does too, and E1 is SPECIAL. But E1 does not reach FOLLOWS THE LAW.

**Why not.** The correction steepens *both* predicted slopes, the law's (0.47 → 0.63) and Newton's (0.84 → 1.03). s_obs = 0.90 ± 0.21 then sits between them, within 2σ of each. With corrected masses, T2 no longer separates the law from Newton.

## Part B (secondary): X43's cluster keys, 326 clusters (X30/X7)

**Controls:**
- Names: 326/326 matched, no injection misses.
- **K4: E0 through the injection reproduces every committed X43 cell exactly** (max difference 0.0).
- **K5 FAILS as frozen:** the measured A rescales exactly (2e-16) but the error does not (up to 5.0 %), because X30's σ is a resampled weighted ratio. Per the frozen rule, the four stored-X7 keys (G-OUT-Mall, M1–M3) are graded but marked **APPROXIMATE**.
- X43's own K0 / K0x38 fail inside the E½ / E1 children. This is expected: they compare against the observed-mass X30/X38 references. They pass at E0, and K1, K2, K2b, K3 and K4 pass in all three runs.

| key (h0672 Z; canonical) | E0 (= X43) | E½ | E1 |
|---|---|---|---|
| G-OUT-M3 (heavy MGAS, OUTER) | +2.41 FAIL | +2.67 FAIL [approx] | **+2.91 FAIL** [approx] (h0686 +2.54) |
| G-OUT-Mall | +0.49 | +1.26 [approx] | +1.69 [approx] (h0686 +1.86) |
| G-OUT-M1 (light) | −0.31 | +0.18 [approx] | +0.38 [approx] |
| G-OUT-M2 | −0.54 | +0.03 [approx] | +0.39 [approx] |
| G-MID-T1 / T2 / T3 | −1.41 / −0.41 / +0.30 | −0.96 / −0.10 / +0.53 | −0.69 / +0.08 / +0.73 |
| G-OUT-all / T1 / T2 / T3 | −1.15 / −1.05 / −0.93 / +0.01 | −0.81 / −0.80 / −0.73 / +0.14 | −0.58 / −0.65 / −0.61 / +0.25 |
| groups (out of scope; Tian+ data) | +2.05 | +2.05 | +2.05 |

On the alt footing, every Z is the same to the printed precision.

**Reading (frozen, E1): X43 HOLDS** on both footings. The failing set is still {G-OUT-M3 (UNDER)}, with no new failure. The groups grade is unchanged (Z +2.05; no eRASS1 gas involved).

## What this means
1. **The light-cluster half of the T2 problem is a selection effect.** Correcting the faint clusters' gas masses lifts the light tercile from A_OUTER 0.57 ± 0.20 to 0.83 ± 0.31, consistent with 1. The shuffle null says this needs the per-cluster errors. CFG687's "FOLLOWS NEWTON" should be read as NOT DECIDED once the eRASS1 Eddington bias is applied.
2. **The heavy-cluster outer excess is not a selection effect.** It stays at A_OUTER 1.43 ± 0.15 in CFG687's estimator and gets worse in X43 (G-OUT-M3 Z 2.41 → 2.91). Heavy clusters are bright and well measured (σ ≈ 0.16, correction ×0.95). Their small downward correction lowers the baseline a little, which raises the measured ratio (1.37 → 1.42), while X43's predicted ratio dips (1.12 → 1.11), so the miss grows. The record's remaining cluster problem is the outer lensing of the heaviest clusters, not the faint end.
3. **Disclosed expectations, as they fell.**
   - "T2 moves toward the law": yes, but only to NOT DECIDED.
   - "Light-tercile A ≈ 1.02 under E1": no, 0.83. The hand estimate used tercile medians and a pure M^0.47 scaling.
   - "X43's light keys may turn UNDER": no, G-OUT-M1 went from −0.31 to +0.38.
   - "G-OUT-M3 unchanged or slightly worse": worse, +0.50 in Z.
4. **Carried caveats.**
   - CFG816's correction is a lognormal power-law approximation that likely overstates at σ ≈ 0.8; E½ brackets it, with the same classes.
   - Selection acts on count rate, which is not forward-modelled here.
   - σ_i comes from the catalogue bounds.
   - Part B's stored-X7 errors are approximate (K5).
   - Part B inherits X43's 5.364 / ΛCDM D_A inputs.

## Files
- `FROZEN_CRITERIA.md`
- `cfg406_rescore.py`: run plainly; `MUTATE=1` for the sign flip; `--x43 E*` is internal.
- `cfg406.out`, `cfg406_results.json`: per-cluster σ, every slope, tercile A, null draw and graded cell.
- `cfg406_MUTATE.out`, `cfg406_results_MUTATE.json`.
- Per child run: `x43_collapse_core_{E0,Eh,E1}.out` and `_results_*.json` (X43's own outputs, redirected here); `cfg406_x43_*_meas.json` / `_arrays.npz` (X30 in-run measured statistics and baselines); `x43_x30_machinery_*.log`.
