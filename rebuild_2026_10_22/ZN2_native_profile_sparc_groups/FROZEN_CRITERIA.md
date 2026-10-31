# ZN2_native_profile_sparc_groups: FROZEN CRITERIA (committed alone, before any z = 0 snapshot exists)

**Question.** ZN1 asks whether the native z = 0 profile passes the clusters. Here the same native profile, at its own mass, goes on SPARC and the groups, with no S, η, r₀, floor or a₀ in the halo. Together they say whether collapse alone, with no core rule, reaches all three. Argon asked for the group half of this; the SPARC half belongs with it.

**Disclosed.** I've seen X81 and CE1: the zooms' cores look like NFW cusps through the ε cut, and converged η reads Υ 0.48 on SPARC. So I expect the SPARC line to fail low, and the groups to pass. That's an expectation, not a result. A pass or a fail gets the same checks.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. No a₀ in the halo or the dynamics, as X48. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Rule
- **Shape:** ZN1's measured z = 0 median m(x) = M(<x R₂₀₀)/M₂₀₀ at 10¹², 10¹³ and 10¹⁴. All finished seeds; fewer than 6 at any of these masses makes the lane UNDECIDED. Linear in lg M₂₀₀ between the three measured tags, clamped outside them.
- **Mass:** M200 from the EM1 relation on each background, as in every lane. Under FC1 that's the cold mass, so the total is M_t = M200/f_c.
- **Cold mass:** M_c(r) = f_c M_t m(r/R_t), with R_t = (3 M_t / (4π 200 ρ_c))^(1/3) on that background's h. Constant beyond R_t. This is ZN1's cluster mapping.
- **Inside 3ε:** M ∝ r², as in ZN1's measurement. At 10¹² that's the inner few kpc of an L★ galaxy, so this part is a continuation of the measured profile and not a measurement.
- **Below 10¹²'s tag:** clamped to the 10¹² shape, counted, and labelled. The true shape there is X80's, which stops at z_f unless a later amendment continues it.

## Grade
- **SPARC line, X74's:** rms ≤ 0.110 and median Υ in [0.50, 0.80], on backgrounds A and B.
- **Groups:** X73's P4 estimator, CONSISTENT.
- The native halo doesn't depend on the footing. Its SPARC line and group Z are stated once, and that's not pooling.

## Verdict
- **NATIVE PROFILE PASSES SPARC AND GROUPS**
- **SPARC FAILS**, **GROUPS FAIL**, or **BOTH FAIL**, naming the direction (Υ low, Υ high, rms).
- **[LOW-MASS CLAMPED]** appended whenever any galaxy is below 10¹²'s tag.
- **[NORMALISATION-DEPENDENT]** appended if reported line 1 changes the class.

A pass wouldn't derive κ, and it says nothing about contraction, which ZN2 leaves out (LC1 measures it). A SPARC fail on this rule with no contraction would be a stronger statement than CN1's, since nothing is left to soften.

## Reported, not graded
1. **FC1's normalisation:** M_c(r) = M200 m(r/R200), with R200 from M200 alone.
2. **Median Υ and ΔV at Υ 0.50, 2–4 R_d, by V_flat** (LS1's bins), both normalisations, beside FC1's rule on the same table.
3. The fraction of SPARC galaxies clamped, and the same line on galaxies above the 10¹² tag only.

## Checks
- **K1, harness:** a table built from FC1's own smooth-core rule on a 0.02 dex mass grid, on FC1's normalisation, canonical, background A, reproduces FC1's line through this path: rms within 2e-3, median Υ within 0.01, group Z within 0.05.
- **K2, inherited:** the grader's inherited check pattern matches FC1's.
- **MUTATE** (`--mutate`, separate outputs): shape's r × 1.5. It must move median Υ on background A by at least 0.02, else UNDECIDED.
- Any K failure: no verdict, exit 1.
