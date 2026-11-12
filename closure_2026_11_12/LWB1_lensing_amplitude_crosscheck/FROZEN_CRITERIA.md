# LWB1 FROZEN CRITERIA: the weak-lensing amplitude row, cross-checked on DESI DR1 "Lensing Without Borders" vectors

TEST lane. Scoped in `reviews/hy4_codex_audit_2026_11_12/A6_desi_euclid_scope.md`, section 3, item 3. Written and committed
alone, before any script and before any model or fitted number exists. Footings canonical (a0 9.3603e-11 m/s^2) and alt
(1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy at 5.41 times the baryons is a gravitating field
component, never a particle. No download: everything below is already on disk.

**This is a consistency check, not independent evidence.** The vectors change the lenses (DESI DR1 spectroscopic BGS and
LRG) but keep the source shear of KiDS-1000 and DES Y3, two of KL1's surveys (HSC Y3 is the third source survey here; it is
not one of KL1's). Shared shear calibration, photo-z and intrinsic-alignment systematics enter both. AMPLITUDE CONSISTENT is
not a pass for the theory and no outcome here says the data favour the framework.

## 1. Data (on disk, read-only)

Root `../_external_data/desi_dr1_lensing/` from the repository root (fetched for CFG315 on 2026-10-03, Zenodo
10.5281/zenodo.22914838, tarball sha256 641526ac...f557; `extracted/` holds `ggl/`, `wp/`, `covariances/`). Codex branch
`codex/euclid-desi-review-2026-11-12` was checked: its only lensing file (`route_lensing.md`) is a lensing/dynamics ratio
note and does not use these vectors. Nothing is duplicated.

- **Delta Sigma (graded):** the tomographic files `ggl/{KiDS,DES,HSCY3}/deltasigma_{BGS_BRIGHT,LRG}_zmin_a_zmax_b_lenszbin_k_blindA_boost_False.fits`,
  column `ds` minus column `magnification_bias` (the release is uncorrected; CFG315 read the column as the additive term).
  Only the paper's conservative source-lens pairs, as CFG315's table: BGS1/2/3 (z 0.1-0.2, 0.2-0.3, 0.3-0.4) with KiDS
  4, 5; DES 3, 4; HSC-Y3 2, 3, 4. LRG1 (0.4-0.6) with KiDS 4, 5; DES 4; HSC-Y3 3, 4. LRG2 (0.6-0.8) with HSC-Y3 3, 4.
  LRG3 has no conservative pair and is not used. r_p comoving h^-1 Mpc, Delta Sigma comoving h Msun pc^-2 (CFG315's units).
- **Delta Sigma covariance:** the joint analytic covariance with cross-survey and cross-lens-bin terms,
  `covariances/dscovcorr_kids1000desy3hscy3_desiy1{bgs,lrg}_pzwei.dat` with index `bin_ds_kids1000desy3hscy3_desiy1{bgs,lrg}.dat`.
  BGS and LRG blocks are separate files; their cross-covariance is not on disk and is taken as zero.
- **Cross component (null):** `ggl/<survey>/bmodes_deltasigma_...` column `ds`, covariance `dxcovcorr_kids1000desy3hscy3_desiy1{bgs,lrg}_pzwei.dat`.
- **Scales kept:** R_min = 8 h^-1 Mpc (linear bias with cross-correlation coefficient 1 is the assumption; below that the
  record has no bias model). R_max = each survey's own `rmax_values.dat` entry (50 % of pairs lost; survopt 1 KiDS, 2 DES,
  4 HSC-Y3), lens index 1-3 BGS, 4-5 LRG. Blending cut is irrelevant at these radii.
- **Projected clustering (bias):** `wp/wp_{BGS_BRIGHT,LRG}_GCcomb_<zmin>_<zmax>_default_angular_bitwise_log2_njack64_nran4_split20.txt`,
  columns rpavg, corr, std (64-region jackknife standard deviation). Kept: rpavg in [5, 20] h^-1 Mpc. Covariance: diagonal
  (the jackknife off-diagonal terms are not released); bracket with correlation 0.5 between the two kept bins.
  The wp-Delta Sigma cross-covariance is not on disk and is taken as zero.
- **NOT on disk:** pi_max of the released wp (not in the file headers or the paper text on disk); the wp jackknife
  covariance; any BGS-LRG Delta Sigma cross-covariance; the Lange+ cosmology paper (arXiv:2512.15962) and its chains; the
  paper's AbacusSummit reference vectors; an explicit statement that the `blindA` files are unblinded (paper section 5.6
  multiplies Delta Sigma by f_blind(R, z) per survey and lens bin before unblinding).

## 2. Model: form B's own Delta Sigma and wp (copied machinery, no imports)

- **Matter spectrum** P_B(k, z) = P_lin0(k) D(z)^2 (sigma8 / 0.811)^2 N(k, z) R_tot,ft(k).
  - P_lin0: the engine's Eisenstein-Hu no-wiggle spectrum normalised to 0.811, COPIED from
    `closure_2026_11_10/BX1_fixed_amplitude_reference/bx1_pm.py` (T_eh, P_lin0; h 0.6736, omega_b 0.02237, omega_c 0.1200, n_s 0.965).
  - N(k, z): the nonlinear ratio of BX1's graded reference, the 512^3 fixed-amplitude paired 200 h^-1 Mpc splice
    (`bx1_splice_pairA_N512.json`), N = P_pairA / (D^2 P_lin0) on its bins, set to 1 below its first bin (k 0.040),
    log-interpolated between nodes z 0, 0.5, 1. This is the reference run chosen because the 100 h^-1 Mpc S0 box is a
    known high draw at large scales (CO2 post hoc; BX1); pair A's own realisation noise is reported, not removed.
  - R_tot,ft: form B's layout (gravity-only S0 times form B's gas layout), CO1's `co1_hm.json` primary per footing.
    Inherited halo list in R. No further baryonic feedback model: nothing ejects gas beyond R200c (form B as stated).
  - Target: KL1's neutrino-floor sigma8, 0.8121 (canonical) / 0.8120 (alt), and Omega_m 0.31471 / 0.31434, read from
    `closure_2026_11_10/KL1_lensing_amplitude_survey_assumptions/kl1_nu.json`. The sigma8 scaling is the constant factor
    (alpha = 1); at R >= 8 h^-1 Mpc the run's own response is within a few per cent of 1 (CO2 KA5) and is not used.
  - D(z), f(z): the engine's background (flat, Omega_m above), COPIED (Dgrow, fgrow).
- **Delta Sigma_mm(R, z) = rho_m int k dk / (2 pi) P_B(k, z) J2(k R)**, comoving, rho_m = Omega_m 2.775e11 h^2 Msun Mpc^-3,
  area-averaged over each radial bin [rp_min, rp_max]. Evaluated at the lens bin's mean `z_l` over its vectors.
- **wp_mm:** Kaiser-distorted linear-bias correlation (Hamilton 1992 multipoles of xi from P_B) integrated to pi_max.
  **pi_max primary 40 h^-1 Mpc** (a common DESI DR1 choice; not on disk); brackets 80, 100 and infinity.
- **Fit per vector V:** Delta Sigma = b_L s DS_mm(R, z_L); wp = s [b_L^2 W0 + b_L f W1 + f^2 W2](r_p; pi_max), with
  s = (sigma8 / sigma8_target)^2 and one free linear bias b_L per lens bin. Bias cancels in the amplitude: wp fixes b^2 s,
  Delta Sigma fixes b s. Gaussian chi^2 with the covariances above. No point-mass term in the primary.
- **Scan:** sigma8 on KL1's grid (0.70 to 0.90 step 0.0125, extended at an edge), chi^2 profiled over every b_L, KL1's
  parabola rule (best sigma8 and width at Delta chi^2 = 1).

## 3. Vectors, statistic and labels (per footing)

- Vectors: **J** = KiDS + DES + HSC-Y3 jointly (cross-survey covariance kept; one b_L per lens bin), **the lane label**;
  KiDS, DES, HSC-Y3 each alone; **K+D** = KiDS + DES jointly (KL1's two surveys). All five are graded and tabled.
- Gap g = (sigma8_target - sigma8_best) / width (positive: the theory sits above the data, as in KL1).
- Lines, in order:
  1. NO VERDICT if the best fit has p < 0.01, or if any gating known answer in section 4 fails, or if the label of J
     changes between pi_max 40, 80 and 100 (pi_max is not on disk).
  2. NO POWER if width > 0.05.
  3. **AMPLITUDE CONSISTENT** if -2 <= g <= 2; **GAP STAYS** if 2 < g <= 3; **TENSION** if g > 3 or g < -2 (direction stated).
- Reported brackets (not graded; a label they flip is marked FRAGILE): point-mass term B_L / R^2 marginalised; R_min 5
  and 12 h^-1 Mpc; `ds` without the magnification column; N = 1 (pure linear); wp bins correlated at 0.5; CAMB 1.6.6 linear
  with BAO + halofit (Takahashi) at the same parameters in place of P_lin0 x N.

## 4. Known answers (gating unless marked) and mutations

- **KA1 transforms:** a power-law spectrum P = k^(gamma - 3) through the code's xi, wp (pi_max infinite) and Delta Sigma
  matches the analytic power-law wp and Delta Sigma = Sigma (gamma - 1) / (3 - gamma) to 1 % at 1-60 h^-1 Mpc (gamma 1.8).
- **KA2 normalisation:** the model's sigma8 at z 0 with N = R = 1 equals the target to 0.3 %.
- **KA3 null:** the cross component, fitted with the same Delta Sigma template (b s free, one amplitude per survey), is
  within 3 sigma of zero for each survey and jointly.
- **KA4 blinding check:** per lens bin, the KiDS/DES and HSC/DES ratios over all released radii (0.08-R_max) fitted as
  a + c ln R: the pooled c is within 3 sigma of zero. A residual blinding slope (section 5.6 of the paper) would show here.
  This cannot exclude a pure common offset.
- **KA5 published amplitude (PROVISIONAL source):** the same pipeline with a Planck18 LCDM CAMB halofit spectrum on K+D
  gives S8 = sigma8 sqrt(Omega_m / 0.3) within 2 combined widths of 0.794 +- 0.023 (Lange+, DES + KiDS, quoted by the scout
  from a web read; the paper is not on disk). Different method (they model small scales), so the tolerance is wide.
- **Mutations** (`lwb1_MUTATE_<id>.json`, must bite on J and both footings):
  - MU1 every Delta Sigma x 0.85: sigma8_best ratio 0.85 +- 0.02.
  - MU2 every wp x 1.3: sigma8_best ratio 1/sqrt(1.3) = 0.877 +- 0.02 (bias does cancel, the amplitude does not).
  - MU3 KiDS Delta Sigma x 1.2: the KiDS-alone sigma8 ratio 1.20 +- 0.03 and DES-alone unchanged within 0.005.

## 5. Hand estimate (before any number)

Form B: S8 = 0.812 sqrt(0.3147 / 0.3) = 0.832. Against the quoted 0.794 +- 0.023 that is ~1.6 of Lange's widths. This
pipeline keeps only R >= 8 h^-1 Mpc, so its width should be larger, ~0.03 in sigma8. Expected: DES and HSC-Y3 alone near
sigma8 0.78-0.80 (g ~ 0.5-1, AMPLITUDE CONSISTENT); KiDS alone lower by CFG315's ~8 % Delta Sigma offset, near 0.73-0.75
(g ~ 2-3, GAP STAYS possible); J between, g ~ 1-1.5, AMPLITUDE CONSISTENT the likelier label.

## 6. What had been seen before freezing

The scout item and its quoted S8; CFG315's README (KiDS Delta Sigma 8.6 +- 3.4 % below DES + HSC at small scales, 7.8 % at
large; large-scale cross-survey scatter s 1.25); the paper text on disk (blinding function, no pi_max found); file names,
FITS columns, covariance index headers, `rmax_values.dat`; the first three rows of the KiDS BGS1 non-tomographic Delta
Sigma file (r_p <= 0.32, small scales, not used); the BGS1 wp file in full (7 rows); the rpavg grid; KL1's target sigma8
and Omega_m; the heads of KL1, BX1 and CO2's RESULT files. No model Delta Sigma or wp and no fit existed.

## 7. Operations

At most 4 threads, `nice -n 19`, one job at a time. Outputs `lwb1.json`, `lwb1.out`, `lwb1_MUTATE_<id>.json`. Any
post-freeze change goes in a dated amendment committed alone, both readings reported. RESULT.md at most 90 lines.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
