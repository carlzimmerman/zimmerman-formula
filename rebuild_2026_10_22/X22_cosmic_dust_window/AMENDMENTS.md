# X22_cosmic_dust_window — amendments (after the frozen criteria, a2b532e3c6)

No criterion, line, grid, threshold or verdict rule changed.

- **A1 (implementation; after run 1, which stopped at S0-5 before any Step 1–3 number).** S0-5 recomputed X19's
  background band with the CFG946 unit constants (G 6.67430e-11, M☉ 1.98847e30, exact pc) and missed by 2.1e-4
  relative. X19 uses G = 6.674e-11, M☉ = 1.989e30, kpc = 3.0857e19 (`x19_selector_rank_test.py` L25). S0-5 now uses X19's
  own constants; the frozen formula (Ω_b ρ_crit(1+z)³, h 0.672, Ω_b 0.049) is unchanged. Everything else keeps the
  CFG946 constants.
- **A2 (implementation; run 2 crashed in Step 3B with a KeyError after printing Steps 1–3A and C2/C3).**
  (a) The reported-only 4 km/s pincer control looked up a reference at k = 10 h/Mpc that is not on the grid; it now
  computes its own c_s = 0 reference. (b) The printed Step-1 class of an edge point (α_PASS, α_NF) was evaluated exactly
  at the edge, where rounding gave FAIL for α_NF; it is now printed just inside the edge (α(1 − 1e-9)), as C1 already
  tests. No graded number changed.
- **A3 (post-result, reported only).** Added the ratios R_L/R_hm and M_L/M_hm (SPARC percentiles) and the fraction of
  SPARC galaxies with M_L < M_hm, for α_NF and α_PASS (`step3A.<footing>.scale_gap_reported_A3`). No verdict weight.
