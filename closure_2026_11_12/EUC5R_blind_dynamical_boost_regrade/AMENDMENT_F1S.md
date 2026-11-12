# EUC5R AMENDMENT F1S (post hoc, disclosed; committed alone before it is run)

2026-11-12. Written after EUC5R's own F1 gate failed (code and runs f7db373fa1) and after the graded numbers were seen.
Still blind to EUC5 beyond its criteria and A1. The F1 gate and its failure stand: the A1 word of EUC5R is
NOT EVALUABLE. This amendment can only add a separately labelled post hoc reading; it changes no word.

## What was seen

The F1 reference spectrum (median S/N of the 255 flagged primaries: 3.51 per pixel in its own fit window) is at
z = 0.745. Following READING §2.1, the mock was placed at z = 0.45 and scaled to that spectrum's median flux in the
observed window of rest 3750-5600 Å at z = 0.45 (5,438-8,120 Å). There this spectrum's S/N is only 1.46 per pixel.
So the mock was 2.4 times noisier than the spectrum's own median S/N, and than the 35 graded P spectra (median 3.58
per pixel, quartiles 2.84-4.21). Only 5, 4 and 0 of the 40 gate mocks (150, 250, 350 km/s) passed the A1.3 quality cuts, against 35 of 40 real P
lenses passing. A post-gate diagnostic at twice the mock S/N gave 0.929 / 1.038 / 0.943.

## The amendment (one run; no iteration)

**F1S.** Identical to F1 (same template, z = 0.45, same wavelength grid, masks and LSF, same fitter and settings, 40
realisations per σ_in, seed 20261112 + 2), except that the noise array (1/√ivar of the reference spectrum) is
multiplied by one constant so that the mock's median S/N per pixel over the good pixels of the fit window equals 3.51,
the reference spectrum's own value. Criterion as frozen: median recovered σ within 5 % of σ_in at 150, 250 and 350
km/s. Reported: scatter, fraction passing A1.3.

**Use.** If F1S passes, EUC5R reports a post hoc reading labelled "under A1, F1S (post hoc)" with the would-be word
already computed (no new graded number is produced; the b_dyn values are unchanged). If F1S fails, that is reported and
nothing else is done. Either way the A1 word stays NOT EVALUABLE. No fitter setting is changed.

κ = ½ FITTED. Adopts nothing. No outcome favours the framework.
