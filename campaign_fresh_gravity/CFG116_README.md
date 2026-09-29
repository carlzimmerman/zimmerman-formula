# CFG116 — does B's one specific failure pass the standard lensing systematics nulls?

- **Criteria:** frozen in `CFG116_FROZEN_CRITERIA.md` (e4083bd4f), before any staging or number.
- **Scripts:**
  - `CFG116_stage_perlens.py`: one pass of the June estimator, CFG110's loop verbatim. It keeps each lens's near-source and far-source tangential sums and its cross-shear sums. 316 s; log in `CFG116_stage_perlens.out`.
  - `CFG116_kids_split_nulls.py`: the scoring, a few seconds.
- **Runs:**
  - The main run passes 9 of 9 and exits 0.
  - The MUTATE run leaks 30% of each early-type lens's tangential sum into its cross sum. It fails H1 (early cross 40.0/7) and exits 1.
  - The two runs differ on H1, so the control is informative.

## Bottom line

**The KiDS early/late split, B's one specific failure, passes both standard lensing systematics nulls.**

- **The cross-shear (B-mode) null.** Over the 1-halo bins the early−late cross difference is consistent with zero, **5.3/7 (p 0.63)**, and so is each class's cross profile (late 2.2/7, early 4.7/7). The whole-sample cross null over all 15 bins is 12.1/15.
  - Power (R0, printed first): a systematic carrying half of the tangential split would give χ² ≈ 9 in the cross difference, and a quarter would give 2.2.
  - So a class-dependent B-mode systematic at about 50% of the split or more is disfavoured. Smaller ones are not tested.
- **Source separation.** Two source sets are compared: sources just behind the lens (z_l + 0.2 to z_l + 0.5) and sources far behind (beyond z_l + 0.5). The early−late differences from the two sets agree, **5.4/7 (p 0.62)**.
  - With far sources alone the split persists: 23.2/7 (p 0.0016).
  - The early−late amplitudes are +0.20 ± 0.06 dex (near), +0.17 ± 0.05 (far) and +0.18 ± 0.04 (all).
  - This test is weak: a systematic confined to the near sources at 50% of the split would give only χ² ≈ 3 (R0).
- **Dilution.** Near sources give about 0.1 dex less signal than far ones, in both classes: late 0.13 ± 0.08 dex, early 0.09 ± 0.04 dex. That is what galaxies associated with the lens, or photo-z scatter, would do to the near set. It is similar for both classes, so it does not create the split.

| 1-halo bins K1 (Msun/pc²) | near sources | far sources |
|---|---|---|
| early − late difference | 4.1, 2.8, 7.1, 3.5, 19.4, 28.5, 32.9 | 2.5, 11.3, 4.2, 7.1, 4.6, 14.3, 33.3 |
| late profile | 6.4, 11.7, 11.7, 16.7, 13.4, 16.3, 14.4 | 10.7, 7.5, 19.6, 21.1, 26.6, 35.1, 23.9 |
| early profile | 10.5, 14.4, 18.7, 20.2, 32.8, 44.8, 47.3 | 13.2, 18.8, 23.9, 28.2, 31.2, 49.4, 57.1 |

The cross profiles over K1 (Msun/pc²) are late 0.2, 0.5, −3.1, 0.6, −0.8, −3.0, −6.0 and early −2.3, −0.7, 1.6, 0.1, 0.3, 0.9, −8.5. The jackknife errors on the cross difference run from 2.1 to 9.7.

## Controls

- **C1:** near + far tangential sums reproduce CFG110's per-lens sums, per lens per bin, to 1.4 × 10⁻¹⁰, and hence the June sums. The far set carries 51% of the K1 pair weight in both classes.
- **C2:** on the first 2,000 lenses the cross sums equal the tangential estimator with every position angle rotated by 45°, to 8 × 10⁻¹⁶.
- **MUTATE:** a 30% leak of the early-type tangential signal into the cross component is detected (early cross 40.0/7, difference 21.4/7), and H1 fails as required.

## Caveats

- **The cross null tests only systematics that produce a B-mode.** An E-mode-only, class-dependent shape error would pass it.
- **The near/far test has low power** (R0).
- **Point photo-z (z_B)** are used, with outliers not modelled. The near/far boundary Δz = 0.5 is declared once.
- **The June estimator's own conventions stay:** no boost correction and no random-point subtraction.
- **These nulls do not address unmodelled covariance.** CFG107: the colour-tertile step rejection falls to p = 0.05 with errors inflated ×1.38, and B's null (the colour dependence itself) with ×1.81.

## Disclosure

- **Spurious warnings:** on this machine numpy prints "divide by zero / overflow / invalid value encountered in matmul" RuntimeWarnings while computing R4's covariance. This is the Accelerate quirk CFG77 and CFG100 also saw. An einsum recomputation gives the identical covariance (difference 0.0) and χ² (12.107). The warnings go to stderr and are not in the `.out` files.

## Reading

- **Excluded as the origin of B's one specific failure, at the tested power:**
  - class-dependent B-mode systematics, at about 50% of the split or more;
  - source-side dilution and alignment, though that test is much weaker.
- **The standing caveat now narrows to:**
  - E-mode-only shape systematics;
  - lens photo-z, beyond CFG110's redshift split;
  - satellites, beyond CFG96's isolation test;
  - unmodelled covariance.
- **What remains:** the early−late difference at fixed g_bar persists with far sources alone.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
