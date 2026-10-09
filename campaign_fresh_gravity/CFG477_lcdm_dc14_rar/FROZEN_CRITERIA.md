# CFG477: ΛCDM with a standard feedback-core prescription (DC14) vs SPARC's RAR. FROZEN before any script exists

Owner chat 10-08 ("keep working"). This follows CFG476 (dark-matter-only ΛCDM fails the RAR: rms 0.205 vs 0.099 dex; a₀ 3.9e-10 vs 1.37e-10). Here ΛCDM gets its baryonic physics in its standard semi-analytic form. κ = ½ fitted; both footings reported. ΛCDM is the comparator; the framework adds no particle.

**Model.** Identical to CFG476 (same galaxies, M★, Moster+13 abundance matching with 0.15 dex scatter, Dutton–Macciò c with 0.11 dex scatter, same noise, same statistic with a₀ free, 200 realisations, seed 77), except the halo profile:
- **DC14** (Di Cintio et al. 2014, MNRAS 441, 2986): ρ ∝ (r/r_s)^−γ [1 + (r/r_s)^α]^−(β−γ)/α, with X = log₁₀(M★/M_h):
  - α = 2.94 − log₁₀[(10^(X+2.33))^−1.08 + (10^(X+2.33))^2.29]
  - β = 4.23 + 1.34X + 0.26X²
  - γ = −0.06 + log₁₀[(10^(X+2.56))^−0.68 + 10^(X+2.56)]
  - c_DC14 = c_DMO (1 + 1e-5 exp[3.4(X + 4.5)])
  - The profile is normalised to M_h inside R₂₀₀, with r_s = R₂₀₀/c_DC14 (the paper's r_s convention differs slightly, by r_−2; declared approximation).
- For X outside the calibrated range [−4.1, −1.3], DC14 is evaluated at the nearest edge (declared). The fraction of galaxies clipped is reported.

**Statistic and verdict** (as CFG476).
- **REPRODUCES** if the median mock rms ≤ data rms + 0.02 dex.
- **FAILS** if ≥ 95% of mocks have rms ≥ data rms + 0.05.
- **MARGINAL** otherwise.
- Also reported: the emergent a₀ against the data's (1.37e-10) and both footings, and the low-g slope against the data's (0.605).
- A separate reported question: does DC14 move a₀ and the scatter in the right direction relative to CFG476's DMO numbers?

**Scope.** DC14 is one fitted prescription from one suite (NIHAO/MaGICC-type). It does not stand for every feedback model, and adiabatic contraction in massive galaxies is not included.

**Controls.**
- K1: with α, β, γ = (1, 3, 1) and c_DC14 = c_DMO (forced NFW), the mock reproduces CFG476's median rms within 0.005 dex (same seed scheme), which checks the generic-profile integrator.
- K2: the DC14 enclosed mass at R₂₀₀ equals M_h to 1e-4.

**MUTATE (`--mutate`).** The feedback strength is inverted (X → X − 3, pushing every galaxy toward NFW-like cusps). The mock rms must rise toward CFG476's; exit 1 if the median moves up by > 0.02 dex.
