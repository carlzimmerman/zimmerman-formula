# CFG668 FROZEN CRITERIA: sealed prediction for JWST GO 8281 (B1938+666 perturbers A and V), before anyone here looks

Date: 2026-10-12. Committed ALONE before any CFG668 script or number, and **before any GO 8281 pixel is downloaded or viewed in
this repo** (none has been). Block CFG660–669. Append-only. κ = ½ FITTED; footings separate; cold energy mass required; no
particle species; not "theory closed".

## 0. Context (what has been seen)

JWST GO 8281 (PI S. Vegetti; Cycle 4; 30.4 h; "A gravitational perturber in B1938+666: a challenge for CDM or an unusual
globular cluster?"; status Completed). MAST: NIRCam F115W and F277W, level-3 mosaics, 87,934 s each, dataRights PUBLIC,
t_obs_release MJD 61314.1 (≈ 2026-09-30). No paper from GO 8281 seen. Lens z = 0.881 (DM 43.82 with Planck18; 7.96 kpc/arcsec;
the framework's background is used as identical at percent level). Perturbers (CFG666): A, M3D(<0.6 kpc) = 1.13±0.06e8 M☉
(Vegetti+2012; Keck L_V < 5.4e7); V, m80 = 1.13±0.04e6 M☉ projected inside 80 pc (Powell+2025). CFG666 law values (can/alt):
A needs M_b(<0.6 kpc) ≥ 3.63e7 / 3.17e7 (isolated) up to 1.13e8 (EFE); V needs 2.4e5 / 2.0e5 up to 1.13e6.

## 1. Prediction in observable units

M_* = (0.8–1.0) M_b (gas ≤ 20%). Rest-frame bands: F115W/(1+z) = 0.61 µm (≈ r), F277W/(1+z) = 1.47 µm (≈ H). Stellar M/L
brackets (any age/metallicity, Chabrier–Salpeter span): Υ_r ∈ [0.5, 5], Υ_H ∈ [0.3, 1.5]. Solar AB absolute magnitudes r 4.65,
H 4.71. Apparent AB magnitude m = M_rest + DM − 2.5 log10(1+z) (matched-band K-correction).
The script reports, per footing and perturber, the predicted AB magnitude range inside the aperture (A: R = 0.6 kpc = 0.075";
V: R = 80 pc = 0.010") in both filters.

## 2. Decision rules (frozen)

- **A — SURVIVES** if the analysis of GO 8281 (the PI team's or an independent one) finds light at A's lensing position, within
  0.6 kpc, at least as bright as the predicted faint end. **EXCLUDED** if the 2σ upper limit is fainter than the predicted faint
  end + 1.19 mag (a factor 3 in flux) in F277W. TENSION in between; NOT DIAGNOSTIC if lens/arc light prevents any limit there.
- **V — NOT DIAGNOSTIC by construction** if the predicted faint end is fainter than the data's depth (the script states it);
  the framework requires a baryonic compact object (star cluster / UCD) of 2e5–1.1e6 M☉ inside 80 pc. A GO 8281 result calling V a
  globular cluster or UCD with M_* ≥ 0.3 × the law's minimum is recorded as consistent; a dark verdict for V carries weight only
  if it rests on a light limit below the predicted faint end − 1.19 mag.
- ΛCDM context only: a dark subhalo gives no detectable light for either.

## 3. Seal

`cfg668_predictions.json`, sha256 in `cfg668_PREDICTIONS_HASH.txt`, in the result commit; never edited. MUTATE
(`CFG668_MUTATE=1`): a0 → 0 must set every M_b,min = M_lens (exit 1 iff it bites).
