# CFG116 — does B's one specific failure pass the standard lensing systematics nulls? FROZEN CRITERIA

Written 2026-09-29, before any staging or number of this lane. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

The adopted STANDING says B's one specific failure is the KiDS early/late lensing split at fixed g_bar. It is fragile only to systematics a jackknife cannot see: photo-z, intrinsic alignments and satellites.
- CFG100 and CFG107 found the colour dependence reaches p = 0.05 only with errors inflated by about ×1.8.
- Satellites (CFG96) and lens photo-z (CFG110's redshift split) have been tested.
- Two standard lensing nulls have not been applied to the split:
  - **The cross-shear (B-mode) null.** Lensing produces no cross shear, so an early−late difference in the cross component would reveal a systematic, for example PSF residuals or class-dependent shape-measurement errors.
  - **Source separation.** Dilution by galaxies physically associated with the lens, and their intrinsic alignments, act only on sources near the lens redshift. A real early−late difference in ESD must be the same for sources just behind the lens as for sources far behind it.

## Staging (declared)

- **One pass of the June estimator,** CFG110_stage_perlens.py's per-lens loop, verbatim: the same 181,477 lenses, sources, background cut z_B > z_l + 0.2, Σ_crit weights (point photo-z) and 15 g_bar bins.
- **Kept per lens per bin:**
  - the tangential sums split by source separation: near (z_l + 0.2 < z_B ≤ z_l + 0.5) and far (z_B > z_l + 0.5): WG_n, WW_n, NN_n, WG_f, WW_f, NN_f;
  - the cross-shear sum over all background sources, WX: WG's estimator with e_t replaced by e_×.
- **The cross component:** e_× = e1 sin 2φ + e2 cos 2φ, the June tangential estimator evaluated at position angle φ + 45°. Its sign does not matter for a null.
- **Output:** `real_research/data/lensing_rar/cfg116_perlens.npz`, git-ignored.

## Scoring (declared)

- **Scope:** CFG110's machinery (exec'd read-only for the patches, K1 = bins 8–14, KG and the 50-patch leave-one-out jackknife).
- **The difference:** D = ESD(early) − ESD(late) per K1 bin, as in CFG88/CFG110. Its jackknife covariance takes the Hartlap factor (N − p − 2)/(N − 1), with N = 50 and p the vector length.
- **Amplitudes:** log10 of the ratio of pair-weighted sums over K1, as in CFG110's R2b.

## Checks

- **C1 CONTROL:** near + far tangential sums reproduce cfg110_perlens (WG, WW, NN), per lens per bin, to 10⁻⁹ relative.
- **C2 CONTROL:** on the first 2,000 lenses, the cross sums equal the tangential estimator run with every position angle rotated by +45°, to 10⁻¹².
- **R0 (POWER; printed before any cross-shear or near/far number):** from the tangential jackknife covariance and the committed early−late difference, the expected χ² of each null if a systematic carrying a fraction ε of the early−late tangential difference leaked into it. Reported for ε = 0.25 and 0.5 (the cross component; the near-minus-far difference).
- **H1 [HEADLINE; MUTATE must fail]:** the cross shear passes the null over K1.
  - The early−late cross difference is consistent with zero: Hartlap χ², 7 dof, p > 0.01.
  - Each class's cross-shear profile is consistent with zero: 7 dof each, p > 0.01.
- **H2:** the early−late tangential difference does not depend on source separation. The χ² of D_near − D_far (7 dof, jackknife of the difference of differences) has p > 0.01.

## Reported rows

- **R1:** B's null (the early−late difference against zero, 7 dof) from far sources only and from near sources only, with the early−late amplitude for each set.
- **R2:** the class tangential profiles for near and far sources, and the class cross-shear profiles over K1.
- **R3 (dilution check):** the far/near ratio of each class's amplitude. Dilution by associated galaxies lowers the near-source ESD, and more for the richer environments of early types.
- **R4:** the cross-shear null of the full sample over all 15 bins (the survey-level null).

## MUTATE

MUTATE=1 leaks 30% of each early-type lens's tangential sum into its cross sum, WX += 0.3 WG for early types. H1 must fail and the script must exit 1.

## Readings (declared)

- **H1 PASS and H2 PASS:** the split passes both nulls at this power. Class-dependent B-mode systematics, and source-side dilution or alignment, are excluded as its origin at the fractions R0 shows. The STANDING caveat narrows to systematics these nulls cannot see: E-mode-only shape errors, lens photo-z beyond CFG110's test, satellites beyond CFG96's.
- **H1 FAIL:** a class-dependent B-mode systematic is present; the split's significance is suspect.
- **H2 FAIL:** the split depends on source separation, so a source-side systematic contributes. R1 and R3 say which way.
- **Caveats (declared):**
  - Point photo-z (z_B), with outliers not modelled.
  - The near/far boundary Δz = 0.5 is declared once.
  - No boost correction and no random-point subtraction, the June estimator's own conventions.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
