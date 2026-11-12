# LWB1 RESULT: the weak-lensing amplitude row on DESI DR1 "Lensing Without Borders" vectors

**As frozen (f4b3128cc1): NO VERDICT (canonical) / NO VERDICT (alt).** Known answer KA1 failed (power-law wp off by 1.7 %
against a 1 % line). The fault was in the check: it left out the line-of-sight tail beyond pi = 3000 h^-1 Mpc.
**Under AMENDMENT A1 (post hoc, 3f7cfa2127; the check adds the tail back, nothing else changes): AMPLITUDE CONSISTENT /
AMPLITUDE CONSISTENT, FRAGILE.** The joint vector J (KiDS-1000 + DES Y3 + HSC Y3 sources) reads best sigma8
**0.786 +- 0.029 / 0.787 +- 0.029**. That is **+0.90 / +0.87 widths** below form B's neutrino-floor 0.8121 / 0.8120.
Two reported brackets push J past the 2-width line (section 3). The surveys also disagree with each other. The graded
rows are bit-identical between run 1 and the A1 run.

**This is a consistency check, not independent evidence.** The lenses are new (DESI spectroscopic BGS and LRG). The
KiDS-1000 and DES Y3 sources are the same shear as in KL1's surveys. AMPLITUDE CONSISTENT is not a pass for the theory,
and nothing here says the data favour the framework. TEST lane: relabels nothing, adopts nothing. Footings are graded
separately and never pooled. Cold dark energy is a gravitating field component, never a particle.

## 1. Table (lwb1.json / lwb1.out; gap = (target - best) / width, positive = theory above data)

| vector | canonical: sigma8, gap, chi2/dof (p) | alt: sigma8, gap | label (both footings) |
|---|---|---|---|
| **J: KiDS + DES + HSC-Y3 (lane)** | **0.7864 +- 0.0285, +0.90**, 126.2/105 (0.078) | **0.7871 +- 0.0285, +0.87** | **AMPLITUDE CONSISTENT** |
| KiDS-1000 alone | 0.7596 +- 0.0508, +1.03, 49.8/35 (0.050) | 0.7602, +1.02 | NO POWER (width > 0.05) |
| DES Y3 alone | 0.6470 +- 0.0474, **+3.48**, 28.5/32 (0.64) | 0.6475, +3.47 | TENSION (theory above the data) |
| HSC Y3 alone | 0.8580 +- 0.0355, -1.29, 39.9/44 (0.65) | 0.8587, -1.32 | AMPLITUDE CONSISTENT |
| K+D (KL1's two surveys) | 0.6990 +- 0.0364, **+3.11**, 80.4/64 (0.081) | 0.6996, +3.08 | TENSION (theory above the data) |

Data: 101 Delta Sigma points (conservative source-lens pairs, R from 8 h^-1 Mpc to each survey's R_max, joint analytic
covariance with cross-survey terms) plus 10 wp points (r_p 5.9 and 14.8, jackknife diagonal). One linear bias per lens bin
(b 1.26 to 2.19). Model: engine EH x BX1 pair A nonlinear ratio x CO1's R_tot, at KL1's target sigma8 and Omega_m.

## 2. What carries the result

- **J's consistency is an average of surveys that disagree.** DES alone sits at 0.647 and HSC alone at 0.858. They are
  0.21 apart, about 3.6 combined widths (they share lenses and wp, so the true separation is larger). The K+D vector
  (KL1's surveys) reads TENSION. HSC pulls J back up.
- **KA5 says this pipeline reads low.** On K+D with a Planck18 LCDM spectrum it gives S8 0.713 +- 0.037. Lange+'s quoted
  value is 0.794 +- 0.023. That passes the frozen wide tolerance (0.088) but is 2.2 of this pipeline's widths low. So
  part of the DES / K+D deficit belongs to the method or the large-scale data (linear bias, R >= 8, no point mass), not to
  form B. Read the DES and K+D TENSION rows with this in mind.

## 3. Brackets (reported, not graded; canonical J, alt within 0.04 widths)

| bracket | J sigma8 | gap | p | J label |
|---|---|---|---|---|
| pi_max 80 / 100 (gating: pi_max is not on disk) | 0.7876 / 0.7851 | +0.86 / +0.96 | 0.08 / 0.07 | CONSISTENT (agree: gate passes) |
| pi_max 300 (about infinity) | 0.7690 | +1.58 | 0.01 | NO VERDICT line (p < 0.01) |
| **point-mass term marginalised** | 0.6809 +- 0.0500 | **+2.62** | 0.40 | **GAP STAYS** |
| **R_min 12** | 0.7306 +- 0.0350 | **+2.33** | 0.58 | **GAP STAYS** |
| R_min 5 | 0.8055 +- 0.0233 | +0.28 | 0.01 | NO VERDICT line |
| ds without the magnification column | 0.8124 | -0.01 | 0.04 | CONSISTENT |
| wp bins correlated 0.5 | 0.7783 | +1.25 | 0.07 | CONSISTENT |
| N = 1 (pure linear) | 0.8732 | -1.92 | 0.01 | NO VERDICT line |
| CAMB + BAO + halofit (Takahashi), form B parameters | 0.7792 | +1.16 | 0.08 | CONSISTENT |

When the cleanest large-scale choices are used (point mass free, or R >= 12), J moves to GAP STAYS (+2.3 to +2.6). The
primary's consistency depends on the 8-12 h^-1 Mpc bins carrying linear bias with no enclosed-mass term. Hence FRAGILE.

## 4. Known answers (A1 run; all pass)

- **KA1** transforms: wp 0.22 %, Delta Sigma 0.08 % (run 1: wp 1.72 %, FAIL; AMENDMENT_A1). **KA2** sigma8 normalisation exact.
- **KA3** cross-component null (fraction of the E-mode template): KiDS +0.056 +- 0.041, DES +0.000 +- 0.040, HSC +0.003 +-
  0.018, J +0.009 +- 0.016. All within 3 sigma.
- **KA4** blinding-slope check, survey/DES ratio in ln R: KiDS +0.010 +- 0.028, HSC +0.010 +- 0.025. No residual slope
  is seen. This cannot exclude a pure common offset.
- **KA5** Planck18 LCDM on K+D: S8 0.713 +- 0.037 against 0.794 +- 0.023. PASS within the 0.088 tolerance. The source
  is PROVISIONAL (the scout's web read; the paper is not on disk).

## 5. Mutations (lwb1_MUTATE_MU*.json, graded in lwb1_mutate_grade.out; all bite, both footings)

- MU1, Delta Sigma x 0.85: J ratio 0.857 (line 0.85 +- 0.02). J goes to TENSION, +4.93.
- MU2, wp x 1.3: J ratio 0.889 (line 0.877 +- 0.02).
- MU3, KiDS Delta Sigma x 1.2: KiDS ratio 1.174 (line 1.20 +- 0.03, just inside); DES unchanged (shift 0.00000).

## 6. Shared with KL1's surveys

The KiDS-1000 and DES Y3 shape catalogues, their shear calibration (m), source n(z) and photo-z, and their
intrinsic-alignment environment are shared. KL1 graded KiDS-Legacy, DES Y3 and KiDS-1000 cosmic shear. A shear-calibration
error common to both analyses moves both the same way. HSC Y3 is the one source survey here that is not KL1's, and it
reads above the target. The lenses, the lens-source geometry and the wp bias calibration are new.

## 7. Not on disk / not checked

- Not on disk: pi_max of the released wp (bracketed 40-300); the wp covariance (diagonal used); the BGS-LRG and wp-Delta
  Sigma cross-covariances (taken as zero); an explicit unblinding statement for the `blindA` files (only KA4's slope test);
  the Lange+ paper and chains; the paper's AbacusSummit reference vectors.
- Not checked: nonlinear or stochastic bias (r_cc = 1 assumed); projection over the lens n(z) (single z_eff); intrinsic
  alignments and the source-redshift trend the paper reports; boost factors; HSC-Y1 and SDSS sources; LRG3; the
  fiducial-distance difference (Planck18 data, Omega_m 0.310 against form B's 0.315); the realisation noise of BX1 pair A
  (N(k) used as is). Footings agree to <= 0.03 widths and are never pooled.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
