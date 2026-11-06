# QX22 iter_1 frozen criteria: is the law's hot/cold step keyed on kinematic support type?

Frozen before any QX22 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle.
No LCDM inputs. Both footings, never pooled.

## Hypothesis under test (H, not adopted)
The plain law's missing boost is keyed on kinematic support: a rotation-supported system gets none, a dispersion-supported
system gets the full boost. In H' form, the boost multiplies the law's phantom mass:
  g_obs = g_law [1 + (F0 - 1) s phi(y)],  phi = (nu - 1)/nu,  y = g_bar/a0,  nu = 1/2 + sqrt(1/4 + 1/y)
where s in [0, 1] is the dispersion-support fraction.

F0 is calibrated on fully dispersion-supported, deep-MOND systems: the bright M31 dSphs, LW1/QX21 plain-law median minus
the SPARC anchor. That gives F0 = 10^(0.227 - 0.027) canonical and 10^(0.187 - (-0.001)) alt. As a systematic, F0 is also
calibrated from the X-ray ellipticals (QX20 class E minus anchor); this is reported.

## What was known before freezing (disclosed)
- QX20 class means and QX21's numbers (KiDS early - late +0.158 +- 0.064; dwarf medians).
- KU2: on MaNGA DynPop, slow minus fast rotators at matched M* and sigma is +0.023 +- 0.023 ln (both footings). That is a
  binary spin split. It made no prediction for a support key and did not split by colour. T1 extends it with a prediction
  and a gas-poor (red) restriction.

## Support mappings s(lambda_Re), frozen (all three graded)
- M-step: s = 1 for KU2's slow class (lambda < 0.08 + eps/4 and eps < 0.4), else 0.
- M-lin: s = clip(1 - lambda/0.8, 0, 1).
- M-sq: s = 1 - clip(lambda/0.8, 0, 1)^2 (dispersion share of kinetic energy).

## T1 (GRADED): MaNGA DynPop at r_half, gas-poor red galaxies only
Data and model:
- The record's on-disk SDSSDR17_MaNGA_JAM_v2.fits.
- KU2's cuts, model choice (lowest chi2_dof), accelerations, matched cells (M* 0.2 dex x sigma_Re 0.1 dex) and Dstat
  statistic, imported unchanged.
- Restricted to u - r >= 2.5 (NSA elpetro absmag; KiDS's early-type cut) so that missing gas does not bias g_bar.

Statistic and errors:
- D = matched-cell median residual of low-lambda (lambda < 0.2) minus high-lambda (lambda > 0.5), ln units.
- sigma_D = bootstrap (2000) (+) best-vs-second model (+) sersic-vs-elpetro M*, as in KU2.
- D_pred(mapping) = the same Dstat applied to the H' increments ln(1 + (F0 - 1) s phi(y)) per galaxy, on the same selection.

Lines:
- KILLED under a mapping if D < D_pred - 3 sigma_D.
- CONSISTENT under a mapping if |D - D_pred| <= 2 sigma_D and D > 3 sigma_D.
- Otherwise neither.

## T2 (GRADED compatibility): KiDS early/late lensing (QX21 T1 data)
- Predicted D_KiDS(mapping) = mean over K1 bins of log10[(1 + (F0 - 1) s_red phi(y_bin)) / (1 + (F0 - 1) s_blue phi(y_bin))].
- s_red and s_blue are the mean s of MaNGA u - r >= 2.5 and u - r < 2.5 galaxies with log M* in [10, 11]; this is on disk,
  and the sample's representativeness for KiDS lenses is a stated systematic.
- COMPATIBLE if |0.158 - D_KiDS| <= 2 x 0.064.

## T3 (REPORT ONLY): type at fixed support
At matched M*, sigma and lambda > 0.5, red minus blue (u - r cut). Blue galaxies' missing gas biases this negative, by about
0.03-0.08 dex (stated, not corrected). If the step follows type, not support, this reads positive at fixed lambda.

## T4 (REPORT ONLY): Local Group dwarfs by morphology
LW1 per-system plain offsets. Classes use McConnachie 2012 types, from memory (provisional): gas-poor dSph and transition
(Cetus, Tucana, Phoenix, Leo T, Pegasus dIrr, Aquarius, UGC 4879, Antlia B) against gas-rich dIrr (IC 1613, Leo A, NGC 6822,
Sagittarius dIrr, WLM). Medians minus the SPARC anchor. No stellar v/sigma table is on disk, so this is not graded.

## T5 (REPORT ONLY): residual after the support key
X-COP class mean minus the mean of the fully dispersion-supported classes (bright M31 dSphs, ellipticals). This is what a
support key cannot carry.

## Label
- SUPPORT KEY KILLED (gas-poor dynamics, r_half) if T1 KILLS under all three mappings on both footings.
- SUPPORT KEY CONSISTENT if T1 is CONSISTENT under at least one mapping on both footings, and T2 is COMPATIBLE.
- NO VERDICT otherwise.

## Known answers and controls (MUTATE outputs separate)
- KA1: reproduce KU2's D (all colours, binary slow/fast) to 1e-6.
- C-inj (power): add the M-lin H' increments to the measured residuals. D must rise by D_pred(M-lin) within 20 %.
- M1 (MUTATE): shuffle lambda within cells. |D| <= 2 sigma_D, and D_pred unchanged.
- M2 (MUTATE): Newton in place of the law. Report D, which must differ from the law's D by > 3 sigma_D (sensitivity).

Light compute (seconds, one thread).
