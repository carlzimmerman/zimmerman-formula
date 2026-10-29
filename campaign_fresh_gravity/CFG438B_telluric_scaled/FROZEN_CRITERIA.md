# CFG438B FROZEN CRITERIA: BX442 rerun with Law+12's sky scaling, super-dark and telluric calibration

Frozen 2026-10-29, before any standard star was reduced, any cube was rebuilt or any number was computed. This is a sub-lane of CFG438, not a new CFG id. CFG438's verdict (NOT VALIDATED) stands as it is. This lane asks one question: if we copy the three reduction steps Law+12 describe that CFG438 left out, does the same frozen extraction then reproduce their kinematics?

## Why this is not a rescore
CFG438 already smooths each channel with a FWHM 0.16" Gaussian (Law's kernel) and takes per-channel noise from the off-source spaxels. Both stay exactly as they were. Nothing in the extraction, the fit, the tolerances or the verdict rule changes. Only the input cube changes, and every change below is copied from Law+12's methods text (arXiv:1207.4196, SI §2) and was chosen before seeing any output.

## Inputs
- The same 40 × 900 s Kn2 0.100" frames as CFG438 (KOA, 2011-08-23 and 2011-08-24). Law's third night is not in public KOA (see CFG438 README); 52 frames cannot be reached.
- Super-dark: the median of the five 900 s Drk frames from 2011-08-23, built with the DRP's Combine Frames. Law: "five individual 900-second dark frames".
- Standards: HIP 111538 and HIP 16652 (Kn2, 0.100", 2 s; two frames each per night), from the same KOA download.

## Reduction changes (the only differences from CFG438)
1. **S, scaled AB differencing.** Each raw science frame has the super-dark subtracted. It is then extracted on its own (the same CFG438 module chain with Subtract Frame replaced by the super-dark) into an unsubtracted cube. For each AB pair, both orderings as in CFG438: diff = A − s(λ)·B, where s(λ) is the per-channel ratio of the median over all spaxels of A to that of B. Law: "scaling the subtracted frame to match the median of the object frame in each spectral channel".
2. **T, per-frame telluric.** Each standard frame goes through the same chain (super-dark, extract, cube). Its nod partner is subtracted if it has one; otherwise only the super-dark. The 1D spectrum is summed in a 0.5"-radius aperture around the brightest spaxel of the collapsed cube. It is divided by a blackbody at the T_eff of the star's catalogue spectral type (the look-up is recorded in FETCH_LOG with its source, and treated as provisional). If the type is not found, 9500 K is used and flagged. The result is normalised to a median of 1 over Kn2, and each differenced cube is divided by it. Each science frame uses the standard nearest in airmass, with ties broken by nearest in time. Law: "closest to it in time and airmass". There is no absolute flux scaling, since kinematics do not need it.
3. **Mosaic.** The new cubes keep the DRP headers. They are combined with the same DRP Mosaic Frames (MEANCLIP, TEL offsets), with the same 75% coverage mask.

Not copied, and why:
- Law resampled to 50 mas. We stay at 100 mas so that V1's 30-spaxel count means the same thing as in CFG438; at 50 mas there would be four times as many spaxels.
- Law fitted all 3600 spectra by hand. That cannot be frozen.

## Extraction and grading
`../CFG438_osiris_reduction/cfg438_kinematics.py` is run unchanged, with only the mosaic path pointed at the new cube. That means:
- the same smoothing, line model, window, noise and bounds;
- the same S/N ≥ 5 cut;
- instrumental sigma 46.6 km/s, as measured in CFG438;
- the same PA grid and pseudo-slit, and the same i = 42 ± 10°;
- the same V1–V4 tolerances and lane verdict rule, verbatim from CFG438 FROZEN_CRITERIA;
- the same MUTATE at z = 2.200, which must fail as before or the run is void.

The kpc scale is the one CFG438 used (Law's own conversion), and is used only to place Law's 6 and 8 kpc radii on our arcsec grid (6 kpc ≈ 0.71"). It is not an input to any physics.

## Ablations (reported, not graded)
- **T-only:** telluric applied to the existing CFG438 cubes.
- **S-only:** scaled differencing without telluric.
- **S+T:** the graded run.

Each reports the S/N ≥ 5 count, the summed S/N and the PA.

Prediction stated in advance: T-only moves the S/N ≥ 5 count by ≤ 10% of 27. The transmission is smooth across the ~±300 km/s line window, so signal and per-channel noise scale together. If T-only moves it by more, that is investigated and reported before S+T is accepted.

## Pass/fail of the lane itself
- **Run valid** if:
  - MUTATE fails (< 10% of the true-z count, and summed S/N < 5);
  - every standard yields a spectrum with summed S/N ≥ 50;
  - the telluric curve stays within 0.5–1.5 of its median across the H-alpha window (rest 6530–6610 Å, i.e. 20743–20997 Å observed).
- **Otherwise VOID**, reported as void, with no verdict.
- **The verdict** is CFG438's: VALIDATED / PARTIAL / NOT VALIDATED.

## What this lane does not claim
- No a0 or acceleration claim. A single galaxy cannot establish a0 evolution.
- No verdict from S/N ≥ 3 or from a spatial selection. CFG438's post-freeze diagnostic stays a diagnostic.
- If S+T is still NOT VALIDATED, the remaining gap is put down to the 12 missing frames and the hand fitting, both of which are out of reach. No further reduction knobs are tried on this galaxy.

## Outputs
- `cfg438b_build.py` (the S and T steps, and the mosaic DRFs);
- `cfg438b_<mode>_results.json` for each of `ST`, `ST_MUTATE`, `T`, `S`;
- maps, and the README with the verdict;
- cubes in ../_external_data/cfg438b_work/ (not in git).
