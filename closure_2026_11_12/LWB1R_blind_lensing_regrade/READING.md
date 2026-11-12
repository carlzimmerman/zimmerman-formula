# LWB1R READING: blind re-grade of LWB1 (DESI DR1 Lensing Without Borders, Delta Sigma + wp amplitude)

Committed alone, before any script or number of mine. Criteria re-graded: `../LWB1_lensing_amplitude_crosscheck/FROZEN_CRITERIA.md`
(+ `AMENDMENT_A1.md`, which concerns LWB1's own KA1 check and does not apply to my code). Footings canonical / alt, never pooled.

**Blindness breach, stated up front.** Two permitted-or-routine reads exposed LWB1's outcome before this file: (1) AMENDMENT_A1
quotes LWB1's canonical first-run rows (J 0.7864 +- 0.0285; KiDS, DES, HSC, K+D values); (2) a `git log` on LWB1's folder
(run to check the lane state) printed LWB1's RESULT commit subject (labels, KA5 S8 0.713 "reads low"). I did not open any
lwb1 file, script, json or RESULT.md. My code below is written from the criteria alone; the comparison step is no longer blind
in the strict sense and RESULT_BLIND.md will say so.

## The statistic as I read it
- Data: ds - magnification_bias from the tomographic FITS files, conservative pairs only (itom = lenszbin + 1): BGS1-3 x
  KiDS 4,5 / DES 3,4 / HSC-Y3 2,3,4; LRG1 x KiDS 4,5 / DES 4 / HSC-Y3 3,4; LRG2 x HSC-Y3 3,4. Joint covariance from
  `dscovcorr_kids1000desy3hscy3_*` (checked: a covariance, diagonal matches ds_err), BGS-LRG cross block zero.
- Scales: bin centre R >= 8 h^-1 Mpc and R <= R_max(survey, lens) from `rmax_values.dat` (survopt 1, 2, 4).
  wp: rpavg in [5, 20] (two bins per lens bin), diagonal jackknife std; wp-DS cross-covariance zero.
- Model: P_B = P_lin0 D^2 (s8/0.811)^2 N(k,z) R_tot(k), with BX1's stored pair-A 512^3 splice for N (ln N linear in z
  between nodes 0, 0.5, 1; N = 1 below k 0.040) and CO1's stored `co1_hm.json` R_tot per footing; s8 target and Omega_m
  from KL1's stored `kl1_nu.json`. P_lin0, D, f, xi, wp, Delta Sigma: my own code (EH98 no-wiggle written from the paper).
- Projection, my route: xi(r) by a Fourier-sine (QAWF) integral of P; Sigma = 2 rho_m int xi dpi; Delta Sigma = mean Sigma
  inside R minus Sigma(R), area-averaged over each radial bin. wp: Kaiser multipoles (Hamilton 1992) of the same xi,
  integrated to pi_max. Fit: DS = b s DS_mm, wp = s (b^2 W0 + b f W1 + f^2 W2), one b per lens bin, profiled.

## Ambiguities (my reading / the alternative)
1. pi_max of the released wp: 40 primary / 80, 100, infinity (criteria). A J label change between 40/80/100 = NO VERDICT.
2. Scale cut on bin centre (mine) / on bin edges (rp_min >= 8, rp_max <= R_max): reported if it flips a label.
3. Lens redshift: one z per lens bin = mean z_l over all kept conservative points (mine) / per-vector mean.
4. DS bin value: area average over [rp_min, rp_max] (mine) / value at the `rp` column (reported).
5. N above the last node k 8.04: held constant (mine) / zero (reported). R_tot outside its grid: 1.
6. Width: parabola through grid points with Delta chi^2 <= 4 on the 0.70-0.90 step-0.0125 grid (mine) / exact
   Delta chi^2 = 1 crossings of the continuous profile (reported).
7. p-value: chi^2 at best fit, dof = N_DS + N_wp - (n_lens + 1).
8. Covariance: as released, no Hartlap (analytic); wp bins correlated 0.5 = reported bracket.

## Validation (stops grading if a gating line fails)
- V1 analytic: P = k^(gamma-3), gamma 1.8, through my xi, wp (pi_max infinite, numerical to 1e5) and Delta Sigma vs the
  closed forms wp = r_p (r_p/r0)^-gamma B(1/2,(gamma-1)/2) and DS = Sigma (gamma-1)/(3-gamma): 1 % at 1-60 h^-1 Mpc.
- V2 normalisation: sigma8 of my P_lin0 (N = R = 1) at z 0 equals 0.811 to 0.3 %.
- V3 null: B-mode (cross) Delta Sigma fitted with the DS_mm template, one amplitude per survey and jointly: within 3 sigma of 0.
- V4 blinding slope (KA4): KiDS/DES and HSC/DES ratios of the non-tomographic files, a + c ln R per lens bin over 0.08-R_max,
  pooled c within 3 sigma of 0 (diagonal errors).
- V5 reference spectrum (reported, not gating for my label but read against): CAMB 1.6.6 Planck 2018 (h 0.6736, ombh2
  0.02237, omch2 0.1200, ns 0.9649, ln1e10As 3.044, mnu 0.06) linear + Takahashi halofit, same pipeline on K+D;
  S8 vs 0.794 +- 0.023 (Lange+, PROVISIONAL: quoted in LWB1's criteria from a web read; not on disk). If it reads low, the
  offset is stated and the theory's gap relative to that offset is a reported row.

## Mutation
MU1: every Delta Sigma x 0.85 must give sigma8_best ratio 0.85 +- 0.02 on J, both footings (b s fixed by DS, b^2 s by wp,
so s scales as 0.85^2 and sigma8 as 0.85).

## Hand estimate
Form B S8 = 0.812 sqrt(0.3147/0.3) = 0.832; against Lange's 0.794 that is ~1.3 combined widths if my R >= 8 width is ~0.03
in sigma8. Expected J: sigma8 0.77-0.80, g ~ 0.5-1.5, AMPLITUDE CONSISTENT the likelier label; per survey noisier, and the
seen LWB1 rows (above) suggest DES alone low. Footings differ by < 0.1 width.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
