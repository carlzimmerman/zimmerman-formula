# N01 REDUX -- DENSITY-LOCALITY ON REAL SPARC (no disk kernel)

**Question.** Is the deep-RAR suppression a0_eff ~ 0.7 a0 (L06: 6.78e-11 on SPARC rings with g_bar < 0.2 a0) a **local-density effect**, a0(rho) = (c/2) sqrt(G rho) evaluated at the disk's local gas density rho_gas = Sigma_gas/(2h)?

**Method.** Per-ring stellar surface density **read directly** from the ring files (SBdisk/SBbul in L_sun/pc^2 at 3.6 um; corpus v7 == `real_research/data/sparc_data/*_rotmod.dat`), Sigma_star = m2l (SBdisk+SBbul) with M/L = the corpus's own m2l_disk. Per-galaxy gas estimate from Lelli+2016 Table 1 (in-repo MRT): Sigma_gas,gal = 1.33 M_HI/(2 pi R_HI^2) — an order-of-magnitude **galaxy-mean**, biased high at deep radii (R_HI is defined at Sigma_HI = 1 M_sun/pc^2; deep rings sit mostly outside R_HI). **No disk kernel is built or inverted anywhere** (prior N01 kernel attempt abandoned: 'KERNEL FAILED VERIFICATION', median rel err 0.94).

- Corpus: `glm53_push/data/rotation_curve_corpus_v7.json`, survey=SPARC only; G071/L06 per-ring conventions (v_b^2 = sign(Vgas) Vgas^2 + m2l (Vdisk^2+Vbul^2); g_bar = v_b^2 1e6/R; g_obs = (Vobs 1e3)^2/R), identical to `L06_rar_moment.py`.
- Sample: 3389 kept rings / 175 galaxies; deep cut g_bar < 0.2 a0 = 1.872e-11 m/s^2 -> **1152 rings / 135 galaxies** (L06: 1152/135).
- Fit: log10 g_obs = 0.5 log10 g_bar + 0.5 log10 a0_eff (slope fixed 1/2), curvature-corrected; SE from 2000-draw galaxy-clustered bootstrap; G208-style grid fit as robustness.
- Prediction: a0_pred = (c/2) sqrt(G rho_bin), rho_bin = area-weighted Sigma/(2h), h in {100, 300, 1000} pc, headline h = 300 pc; legs GAS (primary), TOT = gas + 1.4 star (task prescription), STAR (diagnostic).

## Pre-registered kill conditions (before numbers)

| # | condition | result |
|---|---|---|
| (a) 4bins/gas: a0 flat while rho > 3x | flat=True, rho range 1.2x | **VOID (rho<=3x)** |
| (b) 4bins/gas: slope vs +1/2 | slope -0.15 +/- 1.45 (z = -0.4) | **not fired** |
| (c) 4bins/gas: |z_bin|>5 in >= half bins | 1.00 frac | **FIRED** |
| (a) 4bins/tot: a0 flat while rho > 3x | flat=True, rho range 1.9x | **VOID (rho<=3x)** |
| (b) 4bins/tot: slope vs +1/2 | slope -0.15 +/- 0.37 (z = -1.7) | **not fired** |
| (c) 4bins/tot: |z_bin|>5 in >= half bins | 1.00 frac | **FIRED** |
| (a) 4bins/star: a0 flat while rho > 3x | flat=True, rho range 5.2x | **FIRED** |
| (b) 4bins/star: slope vs +1/2 | slope -0.05 +/- 0.16 (z = -3.5) | **not fired** |
| (c) 4bins/star: |z_bin|>5 in >= half bins | 1.00 frac | **FIRED** |

## Per-bin results (4 bins, primary)

a0i = task-prescribed intercept fit (slope fixed 1/2, curvature-corrected); a0mom = L06 a2-moment mapping (secondary measure); ols = log-log OLS slope of the bin (shape diagnostic; the a0-line family would give ~0.50-0.58 across this window).

| bin | n | ngal | log gbar | a0i (m/s^2) | se_log | a0mom | ols | a0grid | leg | rho (kg/m^3, h=300) | a0_pred | z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 288 | 53 | [-12.18, -11.17] | 4.151e-11 | 0.093 | 8.059e-11 | 0.325 | 4.195e-11 | gas | 2.121e-22 | 1.784e-08 | -28.3 |
| 0 | 288 | 53 | [-12.18, -11.17] | 4.151e-11 | 0.093 | 8.059e-11 | 0.325 | 4.195e-11 | tot | 2.600e-22 | 1.975e-08 | -27.1 |
| 0 | 288 | 53 | [-12.18, -11.17] | 4.151e-11 | 0.093 | 8.059e-11 | 0.325 | 4.195e-11 | star | 3.053e-23 | 6.767e-09 | -15.4 |
| 1 | 288 | 94 | [-11.17, -10.98] | 4.740e-11 | 0.047 | 7.540e-11 | 0.405 | 4.745e-11 | gas | 2.436e-22 | 1.911e-08 | -56.1 |
| 1 | 288 | 94 | [-11.17, -10.98] | 4.740e-11 | 0.047 | 7.540e-11 | 0.405 | 4.745e-11 | tot | 3.477e-22 | 2.283e-08 | -48.8 |
| 1 | 288 | 94 | [-11.17, -10.98] | 4.740e-11 | 0.047 | 7.540e-11 | 0.405 | 4.745e-11 | star | 7.558e-23 | 1.065e-08 | -27.6 |
| 2 | 288 | 107 | [-10.98, -10.85] | 4.005e-11 | 0.045 | 6.393e-11 | 0.761 | 4.000e-11 | gas | 2.488e-22 | 1.932e-08 | -55.9 |
| 2 | 288 | 107 | [-10.98, -10.85] | 4.005e-11 | 0.045 | 6.393e-11 | 0.761 | 4.000e-11 | tot | 4.416e-22 | 2.573e-08 | -54.7 |
| 2 | 288 | 107 | [-10.98, -10.85] | 4.005e-11 | 0.045 | 6.393e-11 | 0.761 | 4.000e-11 | star | 1.203e-22 | 1.343e-08 | -37.4 |
| 3 | 288 | 119 | [-10.85, -10.73] | 3.864e-11 | 0.043 | 6.200e-11 | 0.838 | 4.000e-11 | gas | 2.526e-22 | 1.946e-08 | -60.1 |
| 3 | 288 | 119 | [-10.85, -10.73] | 3.864e-11 | 0.043 | 6.200e-11 | 0.838 | 4.000e-11 | tot | 4.943e-22 | 2.723e-08 | -55.0 |
| 3 | 288 | 119 | [-10.85, -10.73] | 3.864e-11 | 0.043 | 6.200e-11 | 0.838 | 4.000e-11 | star | 1.589e-22 | 1.544e-08 | -41.4 |

### h-dependence of a0_pred and z (GAS leg, 4 bins)

| h (pc) | a0_pred bin0 | a0_pred bin3 | z bin0 | z bin3 |
|---|---|---|---|---|
| 100 | 3.089e-08 | 3.371e-08 | -31 | -65 |
| 300 | 1.784e-08 | 1.946e-08 | -28 | -60 |
| 1000 | 9.769e-09 | 1.066e-08 | -25 | -54 |

## Cross-bin trend (slope is h-independent)

| bins | leg | slope | SE | z vs 1/2 | rho range | a0 span (dex) |
|---|---|---|---|---|---|---|
| 4bins | gas | -0.150 | 1.449 | -0.45 | 1.2x | 0.089 |
| 4bins | tot | -0.147 | 0.373 | -1.73 | 1.9x | 0.089 |
| 4bins | star | -0.046 | 0.155 | -3.52 | 5.2x | 0.089 |
| 3bins | gas | -0.529 | 1.928 | -0.53 | 1.2x | 0.050 |
| 3bins | tot | -0.141 | 0.338 | -1.90 | 1.8x | 0.050 |
| 3bins | star | -0.050 | 0.142 | -3.87 | 4.6x | 0.050 |

## Reconciliation (task 5)

- L06 moment-mapped deep a0_eff (recomputed in-file, same deep set): **6.7792e-11** +/- 6.14e-12 = 0.7241 a0
- Intercept fit, full SPARC deep (1152 rings): **4.1872e-11** (se 0.042 dex)
- Grid fit (G208-style), full SPARC deep: **4.2100e-11**
- Grid fit, G071-isolated (G208 lane, 289 rings / 32 gals): **6.4300e-11** (G208 register 6.43e-11)
- G03D bare register: **6.4800e-11** = 0.6922 a0_DE (the '0.692' on record)

| pair | % difference | on-record |
|---|---|---|
| L06 moment vs G03D bare | +4.62% | 4.6% |
| L06 moment vs G208 in-file | +5.43% | 5.4% |
| G208 in-file vs G03D bare | -0.77% | (0.78% claimed) |

**Refined reading — why the registers differ (measure + sample, not data tension):** on the SAME 1152-ring full deep set, the L06 a2-moment mapping gives 6.779e-11 while the shape fits (intercept/grid) give ~4.19-4.21e-11 — a ~62% measure-gap, because the full deep window is **not** a single a0-line: the per-bin OLS log-log slope rises from 0.32 (deepest bin) to 0.84 (shallowest), far steeper than the a0-line family's 0.50-0.58. The G071-isolated lane is cleaner: grid 6.43e-11 (= G208 exactly), intercept 6.21e-11 (se 0.080 dex), moment 7.6758e-11. L06's 6.78e-11 is a second-moment value on the full (EFE-contaminated) sample; G208's 6.43e-11 is a shape fit on the EFE-clean subset; the G03D 6.48e-11 register is the bare EFE fit. The gap between them (4.62-5.43%) is confirmed as a measures/sample statement, not a discrepancy in the data.

## Controls (LABELED CONTROL ONLY — machinery calibration)

- C1 null twin (flat deep line, density anti-correlated with g_bar): slope -0.00 (expect ~0).
- C2 sqrt-injected twin: slope +0.49 (expect ~0.5). -> PASS.

## Verdict

> **Density-locality a0(rho) = (c/2) sqrt(G rho) at DISK LOCAL densities is killed as the origin of the deep-regime a0_eff.** The measured deep a0_eff (~6.4-6.8e-11) is 2-3 orders of magnitude BELOW a0_pred at EVERY bin and EVERY h (per-bin z < -20; KILL(c) normalization dead). Gas surface densities in SPARC disks give rho_gas ~ 1e-23..1e-21 kg/m^3, i.e. 10^3-10^5 x rho_Lambda = 5.84e-27 kg/m^3 (the density at which a0(rho) = a0_DE), so the law cannot produce a0 ~ 1e-10 anywhere inside a galaxy disk. Cross-bin: the trend is reported per leg; on the GAS leg the galaxy-mean column is near-universal (median ~1.9 M_sun/pc^2 HI -> rho range across bins is small; kill (a) is VOID-by-construction there), while on the STAR/TOT legs (per-ring columns, rho varying by more than 3x) the measured a0_eff is flat within SE -> kill (a) FIRES where testable. Kill (b) (slope vs 1/2 at 5 SE) is reported above per leg; all deviations are far under the 2-order normalization gap.

*Real data only; no git commit; SEs are galaxy-clustered bootstrap (seed 20260925); every assumption labeled (E1-E8 in `N01_results.json`).*
