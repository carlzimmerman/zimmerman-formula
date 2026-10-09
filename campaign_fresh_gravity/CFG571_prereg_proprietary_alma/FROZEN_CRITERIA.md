# CFG571 FROZEN CRITERIA: pre-registered predictions for three unreleased ALMA data sets (z 1.4–2.0)

Committed alone, before any script, and before any of the data are public. Owner request (10-09): freeze our predictions before release so the data cannot be read first. The targets come from CFG570 (185251551, archive metadata):

| target | ALMA programme | data | public |
|---|---|---|---|
| KURVS discs (CDFS, z 1.2–1.6) | 2026.1.00363.S | CO(2-1), ~1.6″ beams (integrated gas masses) | no date set (not yet observed) |
| U4_27928 (z 1.419) | 2024.1.00100.L | CO(2-1), 0.07″, 6.3 h | 2026-11-06 |
| GS4_24110 = RC100 GS3 15675 (z 1.997) | 2025.1.01377.L | [CI](2-1) + dust, 0.09″, 3.9 h | 2026-11-28 |

## Models (a0 at the target's redshift; both footings a0(0) = 9.3603e-11 and 1.1312e-10, never pooled)
- **F-DESI:** a0 ∝ √ρ_DE(z), DESI DR2 CPL (w0, wa) = (−0.838, −0.62): ρ_DE(a)/ρ_DE0 = a^(−3(1+w0+wa)) exp(−3 wa (1−a)).
- **F-flat:** w = −1, so a0 is constant.
- **R-H:** a0 ∝ H(z), with Ωm = 0.315 (flat ΛCDM).
- **L-fb:** ΛCDM + feedback, as an RAR-equivalent scale: CFG565's full-RAR g†(z)/g†(0) medians (1, 1.20, 2.82, 4.88 at z 0, 1, 2, 2.5), linear in z. Labelled RAR-equivalent; CFG566: through inner estimators only ×1.3–1.5.
- **Kernel:** ν_mono (`CFG44_fluid_target/Bcommon.py`, read-only). Given g_obs and the model's a0, solve g_obs = ν(g_bar/a0)·g_bar for the required g_bar.

## Inputs (committed record only)
- **KURVS:** `data_assembly/arxiv_tables/kurvs2023_{integrated,kinematics,velocities_at_radii}.csv`.
  - R = R_Hα,max; V = v_at_last_point (an inclination-corrected data point). logM*, reff from the integrated table; R_d = reff/1.678.
  - **Primary sample:** the 14 KURVS discs inside 2026.1.00363.S (CFG570: 3, 4, 5, 6, 7, 9, 11, 12, 15, 16, 19, 20, 21, 22) with v/σ0 ≥ 1.5. The rest are reported only.
  - **Pressure branches (never pooled):** P-B (primary), V_c² = v² + 2σ0²(R/R_d) (Burkert+2010, exponential disc); P0, no correction.
- **GS4_24110:** RC100 corrected copy (`real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv`): V_c(Re) 206, Re 7.39 kpc, σ0 82, logM_bar 10.76. KMOS3D catalogue logM* 10.89. **Stellar branches** 10.89 (KMOS3D SED) / 10.76 (RC100's baryon mass, used as an upper stellar mass); never pooled. R = Re.
- **U4_27928:** no velocity in the record. KMOS3D catalogue: logM* 10.74, R_half 0.49″, z 1.41933. The prediction is **conditional**: M_gas,req as a function of the measured V_c at R = 2R_e, tabulated for V = 150–300 km/s.

## Required baryons and gas
- **Stars:** a thin exponential (Freeman) disc, V_*²(R) = (2GM*/R_d) y²[I0K0 − I1K1](y), y = R/(2R_d).
- **Required:** V_bar,req² = g_bar,req · R. Required gas velocity: V_gas,req² = V_bar,req² − V_*². A negative value means "no gas allowed" (a FLOOR: stars alone already exceed the requirement).
- **Gas mass:** an exponential gas disc with scale length R_g, converted by the same Freeman form. **Gas-shape branches:** R_g = R_d (primary) and 1.5 R_d. The quantity predicted is the **total** M_gas (what an integrated CO flux gives).
- **ΛCDM reference (not a kill line):** KURVS's own f_DM where tabulated, and RC100's f_DM(Re) = 0.56. These are the authors' halo decompositions with their gas assumptions.

## Decision rules (applied when the data arrive; frozen now)
- **Measured gas:** M_gas = α_CO L'_CO(1-0). Primary α_CO = 4.36 (incl. He), r21 = 0.77, r31 = 0.5 (if CO(3-2) is used); branch α_CO = 1.0. [CI]: the published [CI](2-1)/(1-0) and X[CI] values the data paper adopts, declared at analysis time; the dust route (if used) is declared at analysis time **before** reading the dust flux.
- **Per disc:** Δ_m = log M_bar,meas − log M_bar,req,m at the disc's radius (M_bar,meas = M* + M_gas,meas with the declared shapes).
- **Sample statistic (KURVS):** the median Δ_m over the primary sample. σ_tot = bootstrap σ of the median ⊕ a systematic floor of 0.15 dex (α_CO, M*).
  - Model **disfavoured** if |median Δ_m| > 2σ_tot; **excluded** if > 3σ_tot.
  - Reported per footing, pressure branch and gas-shape branch, never pooled.
- **Single discs (U4_27928, GS4_24110):** demonstrations only. Per model, Δ_m is reported with its interval, and no model is excluded on one disc.
- **CO non-detection:** a 3σ upper limit on M_gas, giving a one-sided Δ_m.

## Pre-data forecast (computed by the script and committed before release)
- The predicted M_gas,req per disc and model.
- The expected separation |median Δ_F-DESI − median Δ_R-H| / σ_tot.
- The number of FLOOR discs per model.

## Controls
- **C1:** the DESI CPL ratio at z = 2 is 0.87 ± 0.01 (matches the a0(z) chart).
- **C2:** KURVS-15 inputs match CFG569 (V 112.2 at 9.2 kpc, logM* 10.07, reff 3.8, σ0 68).
- **C3:** the Freeman V² peak is 0.387 ± 0.003 GM/R_d at R ≈ 2.15 R_d.
- **C4:** a Newtonian round trip. With ν ≡ 1, V_bar,req = V_c to < 1e-6.
- **MUTATE:** set ν ≡ 1 (no modification). All models then require the same baryons, the F-DESI vs R-H separation must collapse below 0.01 dex, and the script must detect it (exit 1). Output carries the _MUTATE tag.
- Failed controls are kept and reported.

## Not claimed
No a0 measurement now. κ = ½ fitted; the cold mass is still required. These are predictions, not results.
