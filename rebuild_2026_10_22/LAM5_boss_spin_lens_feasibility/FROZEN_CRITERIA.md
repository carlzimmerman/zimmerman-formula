# LAM5 FROZEN CRITERIA: can BOSS fibres give spin labels for a lensing split? (stage 0 only)

Frozen before any query that returns counts. kappa = 1/2 FITTED; not theory closed.

## Why
LAM4 (153757202b): one absorption spectrum summed over the half-light ellipse classifies slow vs fast
rotators (AUC 0.878). LAM1 (5ed7fac28a) found 694 slow lenses give sigma(dA) 1.40 against a realistic split of
dA ~ 0.5-1, so the spin lensing split needs about 18x more slow lenses (3 sigma on dA = 1: sigma <= 0.33,
(1.40/0.33)^2 = 18; about 12,500 slow lenses). At z 0.15-0.55 a BOSS 2" fibre may cover a large share of
each galaxy's half-light radius. Stage 0 asks only whether enough such spectra exist at usable S/N.
No spectra and no lensing data are downloaded in stage 0; it is aggregate counts from SkyServer DR17.

## Sample definition (all from SkyServer DR17; angular quantities only, no cosmology)
- SpecObj: class = 'GALAXY', zWarning = 0, instrument = 'BOSS', 0.15 <= z <= 0.55.
- Quality: snMedian >= 20 (LAM2's cut, where LAM2 K2 measured h4 rms 0.027 on SDSS fibres), velDisp >= 100,
  velDispErr / velDisp < 0.10.
- Gas-poor: emissionLinesPort EW_Ha_6562 < 3 A (Portsmouth sign: positive = emission; checked on 6 rows
  before freezing, no counts seen). Rows without a Portsmouth match are counted separately and not graded.
- Coverage: c = 1.0" / R_e, with R_e = PhotoObj deVRad_r * sqrt(deVAB_r) (circularised de Vaucouleurs, r band,
  arcsec). Graded: c >= 0.5.

## Gate
- F1: N(graded) >= 42,000. This is 12,500 slow lenses at an assumed slow share of 0.30 among massive gas-poor
  galaxies, all sky, before any lensing-footprint cut. It is a necessary condition only.
- Rows (ungraded): the same counts at c >= 0.3, c >= 1.0, and at snMedian >= 10.

## Labels
- F1 fails: **NOT FEASIBLE** (spin-split lensing via BOSS fibres is closed).
- F1 passes: **STAGE 0 PASS**. Nothing is graded. Stage 1 (a MaNGA calibration with a seeing-matched 1" circular
  aperture at matched S/N, then the footprint overlap with public shear catalogues) needs its own frozen criteria
  and the owner's yes for downloads.

## Known limits, stated now
- The coverage ratio ignores seeing; at these redshifts seeing will blur the fibre light (stage 1's job).
- A pass says nothing about the central-versus-satellite confound that left VS4 at NO VERDICT.
