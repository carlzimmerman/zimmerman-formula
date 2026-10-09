# CFG479: is the RAR's low-acceleration slope a ROBUST discriminator between the law and ΛCDM-with-feedback? FROZEN before any script exists

Owner chat 10-08 ("swing both"; council Session 12, recommendation 2). κ = ½ fitted; both footings. ΛCDM is the comparator; the framework adds no particle.

**Why.** CFG477: ΛCDM + DC14 nearly reproduces SPARC's RAR scatter (0.120 vs 0.099) and its a₀ (9.7e-11), but the low-g slope differs (0.754 vs data 0.605). This lane asks whether that difference survives declared alternatives.

**Statistic.** slope s = d log g_obs / d log g_bar from an OLS fit over all points with g_bar < 1e-11 m s⁻² (CFG476/477's definition). Data uncertainty: bootstrap over galaxies (500, seed 79).

**Grid** (each a published or declared alternative, not a tuned knob).
- **SHMR:**
  - Moster+13 (as CFG476);
  - Behroozi+13 z = 0 (log ε −1.777, log M₁ 11.514, α −1.412, δ 3.508, γ 0.316);
  - Kravtsov+18 (log ε −1.642, log M₁ 11.35, α −1.779, δ 4.394, γ 0.547).
  - The last two are as recalled and flagged for verification against the papers. All three carry 0.15 dex scatter.
- **Halo response:**
  - none (DMO);
  - DC14 (as CFG477);
  - coreNFW (Read et al. 2016): M(<r) = M_NFW(<r) tanh(r/r_c)^n, with r_c = 1.75 × R_½, R_½ = 1.68 R_d (SPARC master table) and n = 1 (fully cored; the most core-favourable declared choice).
- **M/L:** Υ_disk ∈ {0.4, 0.5, 0.7}, Υ_bul = 1.4 Υ_disk. This applies to both data and mocks: the data slope is recomputed at each Υ.
- 100 realisations per cell (seed 791).
- **Reference row:** the law itself (ν_mono at the canonical and alt a₀) plus the same noise, at each Υ.

**Verdict.**
- **SLOPE DISCRIMINATES (robust)** if, for BOTH feedback models (DC14, coreNFW), in every SHMR × Υ cell, (mock median − data)/σ > 3, where σ = √(σ_data² + σ_mock²) and σ_mock is the 16–84% half-width.
- **NOT ROBUST** if any feedback cell lies within 2σ.
- PARTIAL otherwise.
- Also reported: whether the data slope is consistent with the law's noisy prediction (within 2σ) at each Υ.

**Controls.**
- K1: the Moster/DC14/Υ 0.5 cell reproduces CFG477's slope median 0.754 within 0.02 (different seed).
- K2: coreNFW with r_c → 0 reproduces NFW (DMO) to 1e-6 in enclosed mass.

**MUTATE (`--mutate`).** The mock g_obs is replaced by the law (canonical a₀) in every cell. The verdict must become NOT ROBUST; exit 1 when it does.
