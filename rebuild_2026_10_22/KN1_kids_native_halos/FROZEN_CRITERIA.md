# KN1_kids_native_halos: FROZEN CRITERIA (committed alone, before any native shape has gone through this harness)

**Question.** Route E loses KiDS's isolated lensing to the a₀ law by Δχ² +434 (X53's harness, FC1's rule). FC1's note says S hardly touches R above 100 kpc, so a core rule can't move this. The zooms' native z = 0 profile has no core rule and no truncation at R₂₀₀, and it passes the cluster keys in ZN1. So: what does it do here, with EM1's fitted halo masses and with AM1's counted ones? This is gate G7 and half of G13.

**Disclosed.** I've seen ZN1, AM1, and the record on KiDS: +434 with FC1's rule, TL1's r⁻⁹ᐟ⁴ tail no improvement. I haven't seen any of these shapes on this harness. I expect the native outer slope (2.65 past R₂₀₀) to fall short of the law's near-isothermal signal, so route E should still lose with EM1's masses. AM1's heavier halos raise the amplitude, and I don't know whether that fits. Either way it gets the same checks.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Rule
- X53's harness, unchanged: B21's bins, F2's inventory, `fit` with fitted two-halo b, the same statistic Δχ²(H2H − L2H), "primary" and "all".
- **Halo:** M_c(r) = f_c M_t m(r/R_t) for r ≤ x_edge R_t, constant beyond. m is ZN1's median at the z = 0.25 snapshot, the one nearest these lenses, interpolated in lg M between the measured 10¹², 10¹³, 10¹⁴ tags, clamped outside. R_t = (3 M_t/(4π 200 ρ_c(0.25)))^(1/3). The native shape's inner M ∝ r² below 3ε as measured. The baryons are unchanged.
- **Masses, two runs:** (A) EM1: M_t = 10^(a + b (lg M_b − 10))/f_c, background A. (B) AM1's frozen curve: cold M200 from `../AM1_native_abundance_match/am1_results.json`, M_t = M200/f_c.
- The law's arm is X53's, unchanged, on both footings. The halo has no footing, so one halo χ² stands against each law.

## Verdict (X53's own rule on "all", read per mass choice)
- **LAW**, **ROUTE E**, or **NOT DISCRIMINATING,** by X53's frozen class on Δχ²(H2H − L2H), canonical headline, alt beside.
- **Beside it:** does the native profile beat FC1's rule on this harness? **NATIVE BETTER** if χ²(H2H) falls by at least 25 on "all", **NO CHANGE** within ±25, **NATIVE WORSE** otherwise.
- b is reported. b far above 1 means the fit needs a neighbour term out of proportion, which X53's S2 line (b ≤ 1) tests. That's read as X53 does.

## Reported, not graded
1. FC1's normalisation (M_c = M200 m(r/R200), R200 from M200 alone), for both mass choices.
2. Per-bin Δχ² (X53's block-diagonal read).
3. The z = 0 snapshot in place of z = 0.25.
4. Cells below 10¹²'s tag.

## Checks
- **K1, harness:** FC1's own smooth-core rule as a table on a 0.02 dex mass grid, truncated at R₂₀₀ as X53 truncates it, through this path, reproduces FC1's KiDS χ²: H2H "all" within 1.0.
- **K2:** X53's inherited checks pass.
- **MUTATE** (`--mutate`, separate outputs): shape's r × 1.5 must move H2H χ² "all" by more than 5.
- Any K failure: no verdict, exit 1.
