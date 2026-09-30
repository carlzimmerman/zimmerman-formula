# CFG219 — FROZEN CRITERIA: a pre-flight power forecast for the z > 3.5 decisive test (independent-baryon discs only)

Written 2026-09-30 and committed BEFORE any forecast number is computed. **κ = ½ is FITTED, not derived.** Both footings are carried (canonical a₀ = 9.36e-11, alt 1.131e-10 m s⁻²). Nothing here says the data favour a framework: this is a forecast of what a sample could separate, not a measurement. Anything added after the numbers are seen is labelled post hoc.

## Aim
With the class-A discs of the data chat's list (`data_assembly/HIGHZ_INDEPENDENT_BARYON_DISCS_2026-09-30.md`, 2ad335eea: six CRISTAL dust DETECTIONS, GN20, REBELS-25 with its 3.5σ CO(3-2) gas), forecast, from each disc's **z, radius and baryon-mass errors alone (no velocities, no f_DM)**: (1) the expected separation between a₀(z) hypotheses in a two-sided decomposition, (2) the number of discs needed for 3σ, (3) how the gas-tracer calibration (dust vs CO vs [CII]) enters as a systematic that does not average down. Class B and upper limits are OUT of the forecast (a one-sided limit cannot be simulated as a value); they enter later as one-sided limits only.

## Hypotheses (Z1, 1138d817f: definitions read from `sonnet55_push/puzzle_32pi/agents/Z1_causal_horizon_a0z/z01_cutoff_laws.py` and `zcommon.py`, imported READ-ONLY)
a₀(z)/a₀(0) =
- **FLAT**: 1.
- **H(z)** (the rival): E(z) = √(0.315 (1+z)³ + 0.685) (Z1's "Hubble radius c/H(z)" law).
- **HORIZON**: the particle-horizon law d_p(0)/d_p(z) of `laws(Cosmo(**PLANCK))` (H₀ 67.4, Ω_m 0.315, Ω_r 9.1e-5).
- **LCDM-NATIVE**: Z1's `lcdm_native(z)` (M = 1e12, dlogc = 0), a reference law of the record; beyond z = 5 it is an extrapolation of its concentration relation and is flagged.
FLAT vs H(z) is the PRIMARY pair. HORIZON and LCDM-NATIVE are **reported extra hypotheses, never pooled** with flat-vs-rival: every pair is its own two-hypothesis test.
**Control C1 (Z1 reproduction):** at z = 2.5 the four ratios are 1 / 3.77 / 6.05 / 2.16 within 0.02, and at z = 5 the horizon law is 13.7 within 0.05.

## Disc inputs (only z, radius, baryon masses and their errors)
- **S6 (primary; inputs on disk):** CRISTAL-02, -03, -07a, -11, -19, -20 (the six with a dust-DETECTED gas mass; the CRISTAL paper's note lists 08, 12, 15, 23b as upper limits). From `data_assembly/arxiv_tables/cristal2025_*.csv`: z = z_cii, R_e = Re_disk_kpc, R_out = Rout_over_Re × R_e, log M★, f_molgas with errhi/errlo. **Not used:** any velocity, σ₀, f_DM or the fitted logMtot.
- M_gas = M★ f/(1 − f) (f = f_molgas, so M_b = M★/(1 − f), as in CFG213's route). Errors: σ★ = 0.15 dex on M★ (an ASSUMPTION: the tables carry no M★ error; sensitivity 0.10 and 0.25); σ_gas = σ_f / (ln 10 · f (1 − f)) with σ_f = ½ (errhi + errlo).
- **S8 (a SCENARIO, provisional inputs, not data used elsewhere in the repo):** S6 + GN20 (z 4.055; R_e 3.6 kpc, the JWST/MIRI disc R_e in the list; M★ 1.6e11 = the middle of 1.1–2.3e11; M_gas 1.0e11 = the middle of 5–13e10; σ★ 0.15, σ_gas 0.30 dex; tracer CO) + REBELS-25 (z 7.3065; M★ 8e9, σ★ 0.20; M_gas 1.0e11, σ_gas 0.17 dex; tracer CO; **R_e = 1.5 kpc is a PLACEHOLDER** because the list did not extract a radius; sensitivity ×½ and ×2). Every S8-only number is labelled provisional.
- **The 13–20 disc scenario:** N discs drawn with replacement from the set's inputs (N = 13, 16, 20; also 30, 50, 100 for the N-needed curve). A resampled disc keeps its z, radius and errors and its tracer class.
- **Geometry:** a thin exponential disc carrying all of M_b (R_d = R_e / 1.678, no bulge: CRISTAL's fits carry B/T ≈ 0.1–0.3, declared), g_bar(R) = V_b²(R)/R with CFG216's `disc_v2`. **Primary radius R_e**; secondary R_out (S6 only).

## Statistic and mock protocol
δ_L,i = log₁₀ [ D_i / ν(g_bar,i / a₀,L(z_i)) ], D_i = g_obs,i / g_bar,i, pooled by the **median over discs**, as CFG213/216 (kernel **ν_mono**, footing **canonical** primary; alt footing and P2 reported).
For a TRUE law T and a TESTED law L ≠ T, NMC = 500 mocks (seed 219):
1. nominal (tabulated) masses are the truth: g_true,i from M_b,true; g_obs,i = g_true,i · ν(g_true,i / a₀,T(z_i)); no velocity noise (omitted: the forecast is optimistic on the statistical side);
2. measured masses: M★,meas = M★ 10^(ε★), ε★ ~ N(0, σ★); M_gas,meas = M_gas 10^(ε_g + c_k), ε_g ~ N(0, σ_gas,i), and **c_k ~ N(0, τ), one draw shared by every disc of tracer class k** (dust: the CRISTAL discs; CO: GN20 and REBELS-25) — the gas-calibration systematic that does not average down; independent between classes; M_b,meas = M★,meas + M_gas,meas, g_meas ∝ M_b,meas at fixed geometry;
3. D_i = g_obs,i / g_meas,i and δ_L,i as above; the mock's statistic is the median δ_L and its **galaxy-bootstrap 95% CI (B = 300)**, exactly the lanes' procedure. z_mock = |median δ_L| / sd_bootstrap, counted only when the sign is the expected one (the tested law is rejected in the direction it must be if T is true).
τ grid (on the gas mass, dex): **0 (statistical only), 0.10, 0.25 (BASELINE: the typical α_CO / dust-T_d uncertainty), 0.40.**

## Outputs per (T → L), pair, N, τ
μ = mean over mocks of the median δ_L (the expected separation, dex); z_med = the median over mocks of z_mock (the typical realised significance, "n_σ"); power = the fraction of mocks whose bootstrap CI excludes 0 in the expected direction. **Pair separability n_σ(A,B) = min(z_med(A→B), z_med(B→A)).** N needed for 3σ: the smallest N on the grid with n_σ ≥ 3 (linear interpolation in log N between grid points), or "systematic-limited" if none up to N = 100. τ_max: the largest τ (interpolated on the grid) at which n_σ ≥ 3 for the given N.

## Decision classes (PRIMARY pair FLAT vs H(z), set S6, ν_mono, canonical, R_e; the extras use the same classes)
- **STAT-POWERED** if n_σ(τ = 0, N = 6) ≥ 3, else **STAT-UNDERPOWERED** (with its N_3σ at τ = 0).
- **CALIBRATION-ROBUST** if n_σ(τ = 0.25, N = 6) ≥ 3, else **CALIBRATION-LIMITED** (with τ_max at N = 6, and the N = 13–20 values).
- The 13–20 disc summary lists, for every one of the six pairs, whether n_σ ≥ 3 at τ = 0 and at τ = 0.25.
- Scenario S8 and R_out are reported beside, never substituted for S6. The kernels P2 and the alt footing are sensitivities: a class that changes between cells is labelled KERNEL/FOOTING-DEPENDENT.

## Controls (all must pass; a failure is reported plainly)
- **C1** the Z1 reproduction above.
- **C2** (non-vacuous, through D = g_obs/g_bar and ν): with ε = 0 and τ = 0 the true law's own δ_T,i is 0 to 1e-9 for every disc, every law and every kernel/footing; the OTHER laws' δ_i are non-zero (≥ 1e-3 for at least 90% of disc–law pairs).
- **C3** the mock's noiseless median shift equals the analytic per-disc separation log₁₀ ν(y_T)/ν(y_L) to 1e-9.
- **C4 (response)** an injected uniform calibration offset of +0.20 dex on all baryon masses (MUTATE=1, outputs `*_MUTATE`) moves every disc's δ_i by the independent finite-difference value of the analytic formula to 1e-9, all in the direction of lower δ (δ falls as g_bar rises because D = g_obs/g_bar also falls).
- **C5** the τ = 0.25 dust-only shared offset produces z-scores that never exceed the τ = 0 ones for the same pair and N (saturation, within MC error 0.3σ).

## Reporting rules
No sentence says the data favour the framework; S8 and every provisional input are labelled; the forecast omits velocity and f_DM measurement errors, the bulge, the gas geometry and any tracer other than the two declared; a class-B or upper-limit disc is never entered as a value; first-run outputs are kept if a check implementation is fixed; outputs named by mode.
