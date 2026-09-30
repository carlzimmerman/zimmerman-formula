# CFG215 — the decomposition δ(z) timeline: one two-sided statistic across four disc–halo decomposition samples, z ≈ 0.3–5.7. FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, at the orchestrator's go, before any CFG215 number. **κ = ½ FITTED, NOT DERIVED.** Everything here is "author decompositions, not a direct a₀ measurement".

## Why, and the structural risk

- The rival a₀ ∝ H(z) grows with E(z): ×1.1 at z 0.3, ×2 at z 1.4, ×8 at z 5. If a law is right, δ = log₁₀(D_obs/D_pred) at R_e should be ≈ 0 in every sample, with no trend in z.
- **Route mixing is the main risk.** The samples' mass routes differ and correlate with redshift:
  - MUSE-DARK: DC14, no SED prior, drifts −0.72 dex per unit z against SED (CFG198);
  - RC41: 0.2-dex prior on SED + gas;
  - NOEMA3D: measured CO gas;
  - CRISTAL: 1-dex prior, dust-based gas.
  A δ(z) trend could be manufactured by which route each redshift happens to have. The guards below are frozen against that.

## Exposure, disclosed

- All numbers of CFG198, CFG199, CFG210 and CFG213, including per-galaxy δ for CRISTAL and NOEMA3D.
- The RC41 README's summaries: median f_DM(R_e) 0.43 (0.05–0.76); fitted M_bar minus SED + gas has a median of +0.05 dex.
- No RC41 δ, acceleration or D-against-prediction has been computed or seen.
- **Hand expectation:** no single law fits all four samples. RC41's high f_DM may leave the flat law under-predicting there.

## Samples (all at the decomposition's R_e; D_obs = 1/(1 − f_DM(R_e)))

| sample | z | primary route (anchored or independent) | separate "fit-route" series |
|---|---|---|---|
| MUSE-DARK (GalPaK3D, 109) | 0.3–1.4 | SED M★ + main-sequence H₂, with g_obs from the model's own v/sin i (CFG199 reading b, route ii) | DC14-fitted M_disk (route i) |
| Price+2021 RC41 (DysmalPy, 41) | 0.66–2.45 | the fit's M_bar, which is prior-anchored (0.2 dex) on SED + gas | none |
| NOEMA3D (DysmalPy, 10) | 1.1–1.6 | SED M★ + measured CO gas (CFG213's route) | the fit's M_bary |
| ALMA-CRISTAL (DysmalPy, 12 primary set minus 09 and 15) | 4.4–5.7 | SED M★ + dust gas (CFG213's route, 9 disks) | the fit's M_bar (12 disks) |

- **The primary series** uses only the primary-route column. **The fit-route series** is reported separately and is NEVER pooled with the primary. It appears in the figure in a visibly different style.
- The samples are not pooled into one fit, and no cross-sample correction is applied.

## Per-galaxy quantities

- **MUSE-DARK:** exactly CFG199's g_obs and route-(ii) g_bar (reading b: v/sin i); the model's fDM enters only through D_obs of the fit route.
  - Its g_bar is a LOWER bound where the pressure term is non-negative, so its δ is a lower bound.
  - D_obs,ind = g_obs/g_bar,ind. Galaxies with D_obs,ind < 1 are kept and counted.
- **NOEMA3D and CRISTAL:** exactly CFG213's primary and route rows (g_obs held fixed, D from g_bar,ind).
- **RC41:** no velocities are tabulated.
  - g_bar(R_e) = G M_bar [(1 − B/T) f_disc + B/T f_bulge]/R_e² from the fit's M_bar and R_e.
  - f_disc is the Freeman exponential disc (R_d = R_e/1.678) and f_bulge a Hernquist bulge with R_e,bulge = 1 kpc (declared; not tabulated).
  - D_obs = 1/(1 − f_DM(R_e)).
  - **Route variant (reported):** M_ind = M★,SED + M_gas, with the total held fixed: D_ind = D_obs × M_fit/M_ind.
- **δ_L = log₁₀(D_obs/ν(g_bar/a₀,L))** with a₀,L = A0_f (flat) or A0_f E(z) (rival, Ω_m = 0.315). Kernels ν_mono (primary) and P2; footings canonical (decides) and alt.

## CALIBRATION GATE (before RC41 is used)

- Apply the same geometry to NOEMA3D's and CRISTAL's fitted M_bary/M_tot and R_e,disk, with B/T as tabulated and R_e,bulge 1 kpc where none is tabulated.
- Compare the model's V_bary² at R_e with (1 − f_DM)V_c² (V_circ² for CRISTAL, as in CFG213).
- **Pass:** the median ratio lies in [0.8, 1.25], and RC41 enters as is.
- **Fail:** RC41 enters with the median factor applied, labelled "calibrated".
- Either way, the ratio is reported per galaxy.

## Statistic and decision rows

- **Per sample and law:** the median δ with a 95% bootstrap CI (10,000 resamples, seed 215). The verdict is CONSISTENT, DISFAVOURED-over or DISFAVOURED-under, as in CFG213.
- **T1.** Is any law CONSISTENT in all four samples of the primary series, in the primary cell (ν_mono, canonical)? Report which, or "no law fits all four".
- **T2, a trend claim needs BOTH:**
  - (a) the across-sample slope of the primary series (Theil–Sen on the four per-sample medians against the samples' median z; the CI comes from bootstrapping galaxies within each sample) excludes 0;
  - (b) it is consistent with the within-sample slopes: RC41's own slope over z 0.66–2.45 and MUSE-DARK's own slope over z 0.3–1.4 both have the same sign as (a), neither has a CI excluding 0 with the opposite sign, and at least one CI excludes 0.
  - A trend that fails (b) is labelled "**sample-heterogeneity-limited**".
- **The route-mixing mock (a structural guard).**
  - Every sample is given the same TRUE δ_flat = 0 per galaxy: g_bar,true is chosen so that D_obs = ν(g_bar,true/A0_f).
  - Each sample's own route bias is then applied: b_s = the median over its galaxies of log₁₀(M_ind/M_fit), taken from the committed tables' masses.
  - Two mocks are run:
    - "truth = fit": the primary series' baryons = truth × 10^{b_s};
    - "truth = independent": the fit-route series' baryons = truth × 10^{−b_s}.
  - The pipeline's across-sample slope for each law is computed on each mock.
  - The rival's signal slope is the across-sample slope of δ_rival when flat is exactly true (no bias).
  - **NON-DIAGNOSTIC BY CONSTRUCTION:** if either mock's slope for either law has magnitude ≥ 0.5 × the rival's signal slope. The row is then reported as such, whatever the data give.
- **Heterogeneity (stated, not corrected):** the codes (GalPaK3D vs DysmalPy), the priors and the pressure prescriptions differ.
- **Language:** no sentence says the data favour the framework.

## Controls

- **C1.** A synthetic galaxy placed exactly on each law returns δ = 0 to 1e-12.
- **C2.** The calibration gate, as above.
- **C3.** Reproductions:
  - CRISTAL's and NOEMA3D's per-sample medians (fit and route) equal CFG213's to 1e-9;
  - CFG199's reading-(b) route-(i) lowest-z-third median log₁₀ a₀ = −10.143 is reproduced to 1e-3 from the copied formulas.
- **MUTATE=1.** Every RC41 D_obs × 1.5. RC41's median δ must rise by log₁₀1.5 to 1e-9, on both routes. Outputs are written separately.

## Figure

δ against z for both laws. The primary series is drawn with solid markers, the fit-route series with open markers and dashed connectors; the per-sample medians carry 95% CIs. The chart is titled "author decompositions, not a direct a₀ measurement".
