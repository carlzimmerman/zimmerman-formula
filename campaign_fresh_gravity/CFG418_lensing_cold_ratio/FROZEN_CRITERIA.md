# CFG418 FROZEN CRITERIA: a lensing-based estimate of the cold-to-baryon ratio from the supply edge (door 2; a consistency test, not a derivation)
(owner 2026-10-07: "keep going"; committed before any script)

**Inversion.**
- If the law's phantom stops at the supply edge, then r_edge = (R_c/f_ret) · r_M.
- KiDS's preferred truncation x = r_edge/r_ta (CFG413, free two-halo) therefore gives **R_c = x · r_ta · f_ret / r_M**, to compare with the CMB's Ω_c/Ω_b = 5.364.

**Inputs (committed).**
- x from CFG413's χ² profile (cfg413_kids_results.json): the best x, and the Δχ² ≤ 1 range interpolated on its grid, per footing.
- r_ta and r_M (deep MOND) for the stack's typical lens: log M_b = 10.8, with a bracket of 10.5–11.0.
- f_ret ∈ [0.07, 0.10]: the census galaxy fraction (Shull+2012) and the CFG398 range.

**Verdict.**
- CONSISTENT: the inferred R_c interval contains 5.364.
- HIGH or LOW: otherwise.
- The interval's width is reported. The two-halo degeneracy (CFG413) dominates.

**MUTATE.** x := 1. R_c must then move above the CONSISTENT interval. Separate output.

**Scope.** A consistency check of the supply-edge picture. It does not derive the amount. κ = ½ is fitted.
