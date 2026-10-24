# PH1 AMENDMENT A1 (POST-RESULT, 2026-10-24) — disclosed fixes after the first scored run

FROZEN_CRITERIA.md (11270eef61) is unchanged. These changes were made after the first full run had printed numbers.

1. **P4 EN normal-mass bug (code).** The first run computed a galaxy's baryonic mass as g_bar·R/G (that is, V²/G, the
   wrong dimension). The EN normal halo was therefore about 1e-20 of the intended mass, and the first run reported a double
   count of exactly 0.0000 dex. This is fixed to g_bar·R²/G. The first run's EN P4 numbers are void.
2. **Satellite collapse method (A1 method).** The frozen method evolves the stars as dynamic circular shells. In the first
   run it was **not converged**:
   - KS2 (frozen node y₁₂ = 10^-2.5, R_J = 10 r₁₂): max |Δlog B| was 0.022 dex against a line of 0.02. **FAIL as frozen.**
   - At R_J = 31.6 r₁₂, the stellar radius drifted with N (dust shells × 1 / 2 / 4): c = 2.62 / 1.42 / 0.93, and
     B = 2.54 / 4.81 / 5.91.
   - Cause: each dust shell outweighs the whole stellar component (the phantom is 60–3000 M_b), so dust-shell crossings
     heat the star shells numerically.
   - The first run's EC residuals (+0.038 / −0.003, "CONSISTENT") come from that unconverged method, and **are not used**.

   **The A1 method:**
   - The dust shells are integrated with the Plummer baryons in the force.
   - The stars respond in the adiabatic limit of the same circular shells: r·M(<r) is conserved for the stellar half-mass
     shell.
   - The grid is extended to R_J = 10^1.75, because the data reach R_J = 65 r₁₂ and the frozen grid stopped at 31.6.
   - KS2 is re-run on the A1 method at the frozen node: 0.019 dex, PASS.
   - A new check, KS2b, is added at the R_J = 31.6 node with the same 0.02 line. It gives 0.025 dex, **FAIL**, disclosed.
     The trend is monotonic in resolution and amounts to ±0.03 dex on log B, which is below the residual sd of 0.05–0.08.
   - The main run therefore exits 1 on KS2b.
3. **`--mutate` reuses the cached collapse grid** (`ph1_collapse_grid_A1.json`). The grid does not depend on the mutation.
