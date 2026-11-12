# EUC2 AMENDMENT A1 (post hoc, disclosed)

2026-11-12. Written after a first pass of the frozen search on the 382 spectra of the flagged lenses, while the
extension search was still running. Committed before the amended search exists. The frozen criteria (364e9d08c9) are not
edited; the frozen search is still run to completion and its word reported as it falls.

## What was seen

First pass, flagged lenses only (369 lenses, 382 spectra), frozen search:

- H1 injection 191 / 200 (pass). H3 join 363 / 369 (pass). H4: the one known pair, EUCL-DR1-L015763, returned
  z_s = 1.3658 against the published 1.366 ± 0.008 (pass). H5 yield A / B / C: 13 / 5 / 5 against the paper's 12 / 5 / 3.
- **H2 fails**: 10 fake-separation clusters against a limit of 8.2 (20 % of 41 real SECURE-D clusters). The sign-flipped
  null returned 108 clusters. 9 lenses carried conflicting secure redshifts.
- The plots of the 23 retained detections were looked at. Two (L012826, L015763) are textbook resolved [O II] doublets.
  Several are a **single narrow spike lying between the two expected positions** (L008856, L006127), which the two
  overlapping templates both pick up, or a **broad bump** (L010278). Most SECURE-M detections rest on a second "line"
  that is one bright pixel.
- A reading was printed for the 3 lenses of sample P and 4 of S that had a detection. It is void: the search that
  produced it failed its own purity gate. Those numbers were seen and are not used.

So the frozen search is NOT EVALUABLE on its own terms, for a reason the null identified correctly: the frozen
SECURE-D rule tests two amplitudes at two positions and never asks whether the feature has the **shape** of a doublet.

## The amendment

**A1.1 Doublet preference.** A cluster that passes the frozen SECURE-D thresholds (S_OII ≥ 7, both components ≥ 3,
ratio in [0.35, 2.0]) is kept only if a pixel-level fit prefers a doublet to any single line. In the window from
`λ_a − 2.5 s` to `λ_b + 2.5 s` (`s` = observed separation), on good pixels with the prepared errors:

- doublet model: two pixel-integrated Gaussians at the two [O II] wavelengths, redshift free within ± 3e-4 of the
  cluster peak, intrinsic width one of 40, 70, 110, 160 km/s added to the instrumental width, two non-negative amplitudes;
- single-line model: one pixel-integrated Gaussian, centre free between `λ_a − s` and `λ_b + s`, width free from 0.4 Å
  (narrower than the instrument: a spike) to 4 s (a broad bump), one non-negative amplitude.

Kept if `χ²(single) − χ²(doublet) ≥ 4`, and the fitted doublet amplitudes are both positive with ratio in [0.35, 2.0].
This class is **SECURE-A1**.

**A1.2 Multi-line and DESI-redshift classes.** SECURE-M is no longer secure (the flipped null shows it is dominated by
artefacts); its lines are kept as annotations on a SECURE-A1 detection. SECURE-Z (an extension spectrum whose DESI
redshift is the source) now requires SECURE-A1 within 0.002 of the DESI redshift.

**A1.3 Gates for the amended search.**
- H2 is the gate, unchanged in form: fake-separation count (4.50 Å, same doublet-preference fit) ≤ max(1, 20 % of the
  real SECURE-A1 count). Fake separations of 1.80, 4.00 and 5.20 Å are also run and reported.
- H1 is reported at injected S = 10 and S = 14 and is **not** a gate for A1: completeness changes how many sources are
  found, not whether the ones found are real.
- H3 and H4 as frozen.
- Every SECURE-A1 detection is plotted and looked at; any judged an artefact is listed, not removed.

**A1.4 Reading.** As frozen (§5) for samples P and S, with SECURE-A1 redshifts. One more reading, added here because
most first-pass detections lay outside sample S: **sample U** = every lens with a SECURE-A1 source redshift and usable
catalogued inputs (EUC1 §2's five validity conditions), whatever its grade, lens-model inspection outcome or
final-sample flag, split by `lens_model_success`. U is labelled "not quality-cut" wherever it appears.

**Words.** The frozen search keeps its own word. The amended search can only ever give **POST HOC READING (A1)**;
EUC1-F is applied only if the amended sample P reaches N ≥ 10 and is then labelled "under A1".

κ = ½ FITTED. No outcome favours the framework.
