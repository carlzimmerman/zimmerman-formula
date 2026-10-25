# Self-review and verification

- Both bounded-run manifests validate against current input/output hashes. Primary status completed; deliberate mutation status failed as intended.
- Ten main controls passed. Independent root finding checks AQUAL inversion, zero-source input recovers the galaxy law, and the native balance inversion reproduces its static solution.
- The deliberate mutation doubles reconstructed source mass and fails the real-data forward reconstruction for A1795. It does not merely fail a planted fixture.
- Independent dense trapezoidal integration checked all 350 shell potential averages across two footings and five cases against production quadrature: maximum relative difference 4.02e-7, below 2e-6.
- All 420 native radial points across the ten cases are accounted for by cap failure or outward force in the specified limit.
- The baseline scientific plot was visually inspected: labels and legends readable, potential-zero-independent scale compared to the inherited bound, reconstruction explicitly labeled as inferred.
- git diff --check on this lane passed.

Analytic audit:
1. Native total field mass is not the independent AQUAL source and neither equals the preceding empirical residual. All three definitions kept distinct.
2. Integrating the native hold equation assumes no singular central flux and mu_K=0. Its cap cannot be exported to an arbitrary finite-mu_K state.
3. Static finite-mu_K source density contains an unknown potential constant; taking differences of volume averages eliminates it without fitting it.
4. The finite-mu_K test uses all signed source shells, and does not assume mass-term density must remain positive. Only the independent ordinary-source interpretation requires nonnegative shell masses.
5. The galaxy guard is monotonicity of g²/(a0+g); a source normalization cannot be varied without changing the field unless another response change is specified.
6. Jeans balance admits boundary/anisotropy freedom and is not a phase-space or microscopic closure. Shell-center isothermal estimates are explicitly approximate.
7. The screening scale is not selected. Results are conditional on negligible stiffness, not a universal exclusion of all screened completions.
8. No likelihood or full radial covariance has been propagated; central-profile incompatibility is not assigned a detection significance.

Original goal status: unresolved. No source normalization, phase-space state or microscopic vacuum/force ratio has been derived. These calculations constrain three candidate interpretations and provide a zero-point-independent static test; they do not supply the requested new mechanism.
