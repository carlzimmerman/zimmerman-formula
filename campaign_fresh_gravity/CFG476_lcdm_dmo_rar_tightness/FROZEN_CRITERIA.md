# CFG476: does plain (dark-matter-only) ΛCDM reproduce SPARC's RAR tightness? FROZEN before any script exists

Owner chat 10-07 ("keep working"). Question from council Session 10: "who arranges the cold mass?" ΛCDM's answer is assembly plus feedback. This lane tests the assembly half alone: abundance-matched NFW halos with standard scatter, **no feedback, no adiabatic contraction, no cores**. κ = ½ fitted; both footings reported. No DM particle is added by the framework; ΛCDM is the comparator here.

**Mock.** Per SPARC galaxy (CFG4_common.load_sparc(), Q ≤ 2), at its own radii and baryon curves (Υ_disk 0.5, Υ_bul 0.7):
- M★ = 0.5 L_[3.6] + 0.7 × bulge share (the SPARC L, bulge fraction from the V_bul² share at R_last; declared approximation).
- **Halo mass:** Moster et al. 2013 z = 0 SHMR (M₁ = 10^11.590, N = 0.0351, β = 1.376, γ = 0.608), inverted numerically. Scatter 0.15 dex in log M★ at fixed M_h, propagated as δ log M_h = N(0, 0.15) / (d log M★ / d log M_h) at the galaxy's mass.
- **Concentration:** Dutton & Macciò 2014 z = 0 (log₁₀ c₂₀₀ = 0.905 − 0.101 log₁₀(M₂₀₀ / 10¹² h⁻¹ M☉)), scatter 0.11 dex; h = 0.7.
- g_obs,mock = g_bar + G M_NFW(<r)/r². V_mock = √(g r), plus Gaussian noise N(0, e_V) per point, as in the data.
- 200 realisations, seed 76.

**Statistic (identical for data and mocks).** The weighted rms of log g_obs − log[ν_mono(g_bar/a₀) g_bar], weights (V/e_V)², with a₀ FREE (bounded fit), so the mock is not penalised for an offset normalisation. Report the rms and the best-fit a₀ for the data and for each mock.

**Verdict.**
- DMO-ΛCDM **REPRODUCES** the tightness if the median mock rms ≤ data rms + 0.02 dex.
- It **FAILS** if ≥ 95% of mocks have rms ≥ data rms + 0.05 dex.
- Otherwise **MARGINAL**.
- Also reported: the mock's emergent a₀ (median and spread) against the data's and the footings, and the mock RAR's low-acceleration slope (d log g_obs / d log g_bar at g_bar < 1e-11) against the data's.

**Scope (declared).** This tests dark-matter-only ΛCDM. Hydrodynamic simulations with feedback, cores or contraction are NOT tested. A FAIL says ΛCDM's RAR then rests on baryonic physics, not that ΛCDM fails.

**Controls.**
- K1: the data statistic reproduces the record's SPARC scatter at fixed Υ 0.5, Q ≤ 2 (reported; no fixed target number; consistency with CFG4's ~0.10–0.11).
- K2: the Moster inversion round-trips M★ → M_h → M★ to 1e-6.

**MUTATE (`--mutate`).** Mock g_obs replaced by the law itself (ν_mono g_bar at the fitted canonical a₀) plus the same noise. It must return REPRODUCES; exit 1 when it does.
