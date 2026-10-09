# CFG560: do bars rotate slower where the law's dark fraction at corotation is higher? A friction test of the council's default. FROZEN before any script exists

Owner chat 10-08 ("swing all three"; council Session 13, rank 3). κ = ½ fitted; both footings. No DM particle; the cold mass is still required.

**Why.** The council's default (Session 2): the settled cold fluid is real collisionless mass, so it exerts Chandrasekhar friction on bars. A friction-bearing dark component predicts bars slow down (R = R_CR/R_bar grows) more where the dark fraction near corotation is higher. A pure force (no responsive dark matter; already excluded by CFG447) predicts no trend. **ΛCDM predicts the same positive sign as settling, so this lane cannot separate them.** It tests "responsive dark matter vs none".

**Data** (on disk; h29's): Geron et al. 2023 MaNGA TW table 3 (`real_research/data/bars/geron2023_manga_barspeeds_table3.tsv`): Ω_bar (km/s/kpc), R_CR (kpc), R with published bounds.
- Per galaxy: V_CR = Ω_bar R_CR and g_obs(R_CR) = V_CR²/R_CR.
- The law's dark fraction at corotation is f_dark = 1 − g_bar/g_obs, with g_bar from inverting g_obs = ν_mono(g_bar/a₀) g_bar. Both footings.
- Rows need finite positive Ω, R_CR and R. Quality subsets use σ_R/R, with σ_R the mean published half-width: ALL, σ_R/R ≤ 0.35 (≈ median) and ≤ 0.20.

**Statistics.**
- (S1) Spearman ρ(R, f_dark) per subset.
- (S2) the partial Spearman ρ(R, f_dark | R_CR), because R and g_obs share R_CR. A larger R_CR raises R and g_obs together and lowers f_dark, building in a NEGATIVE correlation, against the friction sign. A positive S1 survives that bias.
- (S3) the same with g_obs/a₀ in place of f_dark (reported).

**Verdict** (primary: S2 on the σ_R/R ≤ 0.35 subset, canonical; alt reported).
- **FRICTION SIGNAL** if ρ > 0 with permutation p < 0.01, and S1 has the same sign.
- **NO FRICTION SIGNAL** if ρ ≤ 0, or p > 0.05 in both S1 and S2.
- Otherwise **HINT**.
- Reading. A friction signal supports responsive dark matter (settling or ΛCDM) over a pure force. No signal is consistent with weak inner friction (settling's low inner cold density) or with h29's systematics, and does not discriminate.

**Controls.**
- K1: the row count and the median R reproduce h29's (N 210 finite with bounds, median R 1.663).
- K2: the law inversion round-trips g_bar → g_obs → g_bar to 1e-8.

**MUTATE (`--mutate`).** Shuffle R among galaxies (seed 560). |S2| must drop below the permutation 2σ; exit 1 when the shuffled ρ is consistent with 0.

**Compute.** Light; run under `nice -n 10` with BLAS threads at 1.
