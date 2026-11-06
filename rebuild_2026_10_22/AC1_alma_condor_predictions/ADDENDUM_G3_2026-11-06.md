# AC1 addendum G3 (DRAFT, NOT FILED): disc-fit repair for U4_28473

**Status: draft for the owner. Not filed. Nothing runs under it until the owner files it.** Filing means:
- the owner says so in chat;
- this text is committed unchanged as `rebuild_2026_10_22/AC1_alma_condor_predictions/ADDENDUM_G3_<date>.md`.

It supplements, and does not edit, FROZEN_CRITERIA.md, ADDENDUM_G1.md or ADDENDUM_G2_2026-11-04.md. No prediction value, mass branch,
detection gate, seal, error floor or U4_27928 rule changes. κ = ½ FITTED; one disc excludes no model; not theory closed.

## This is a POST-DATA repair. Say so everywhere
- The release cube has been read.
- On it, the frozen fit collapsed to I0 = 0 at the first step in all six trial fits (AL1 cb2a36ca23, AL2 e35325206f).
- Facts already seen on that cube: the 3D line centroid (≈ −172 km/s from the catalogue z), the frozen start's cost relative to an empty
  model, and the noise statistics.
- **No V_c from this cube has been computed under any fit that works.** The rules below are fixed before one is.
- Any row scored under G3 is labelled **"POST-DATA REPAIR (G3)"** in every output, table and paper. The release's "FIT NOT CONSTRAINED"
  stays beside it.
- A G3 score can test a prediction. It cannot be presented as a pre-registered blind test.

## Why (from AL1/AL2, not from any speed)
1. **The amplitude has an absorbing bound.** The model is proportional to I0. Once a projected LM step clips I0 to its bound 0, no
   parameter has a gradient, and the fit cannot leave (AL1 T1/T2).
2. **At per-voxel S/N below 5, a start disc that is wrong in velocity or shape costs more than no disc.** So the first step heads for
   I0 < 0 (AL2 R2). The frozen vsys start (moment-1 mean, −29) also ignores the scorer's own 3D centroid (AL2 R3).
3. **Channel noise is correlated** (lag-1 +0.24 off source; AL2 R4). The fit treats voxels as independent, so its covariance is too small.

## Ruling (all generic; no number below was chosen from this cube's kinematics)
1. **Amplitude in logs.** Fit u = ln I0 in place of I0, with bounds u ∈ [ln(1e-4 I0\*), ln(1e3 I0\*)]. I0\* is the analytic amplitude of
   rule 3. I0 can then never reach 0. Every other parameter and bound is as frozen.
2. **vsys start from the 3D detection.** Start vsys at the flux-weighted velocity centroid of the G1-3D mask. The scorer already computes
   this as z_line of G1-3D, converted with the scorer's own velocity axis. The frozen moment-1 vsys is printed beside it.
3. **Start chosen on a fixed coarse grid, with an analytic amplitude.**
   - For each of the three frozen vf starts, evaluate the cost on the grid vsys = centroid + {−100, −50, 0, +50, +100} km/s and
     PA = pa0 + {0, ±45°, ±90°, 180°}, with all other start values as frozen.
   - At each grid point the amplitude is the linear least-squares value I0\* = ⟨M₁, D⟩ / ⟨M₁, M₁⟩, where M₁ is the model at unit
     amplitude (floored at 1e-6 of the frozen I0 start).
   - Each vf start begins from its lowest-cost grid point. The grid is part of the rule, not tuned.
4. **Three-start gate unchanged** (G2 §1: all three finite speeds agree within 15 % on both P-B and P0, at the radius scored).
5. **Model-adequacy gate.** Score a branch only if the best fit beats the empty model by Δχ² ≥ 25 / (1 + 2ρ₁).
   - ρ₁ is the measured off-source lag-1 channel autocorrelation, and χ² is in the fit's own (independent-voxel) units.
   - Otherwise the branch reads "FIT NOT CONSTRAINED: model no better than empty".
6. **Correlated-noise errors.** Multiply the fit covariance by (1 + 2ρ₁) before the existing error rule. The reported error is still
   max(quoted, 8.87 % × V_c) (G2 §2). The floor is not changed.
7. **Everything else unchanged:**
   - inclination branches;
   - pressure branches P-B and P0, never pooled;
   - G2 radius rule;
   - the at-bound, q-clamp and σ(V_c)/V_c ≤ 0.25 gates;
   - the C1 injection check;
   - the scoring grid.

## Validation that must pass before G3 touches the real cube (its own lane, MOCK only, criteria committed first)
- **(V1) No regression.** Rerun G2 §3's selftest and the six-seed power suites with G3 on.
  - Validity counts must be no lower than G2's.
  - Fractional RMS of V_c recovery must be no worse than G2's +2 percentage points.
- **(V2) Hard classes, six seeds each, V_c 430**, at the release's measured noise, beam, channel width and pixel:
  - (a) line offset −172 km/s;
  - (b) lopsided disc, 40 % of the flux in one clump at 0.5 R_e;
  - (c) correlated channel noise, ρ₁ = 0.24;
  - (d) a + b + c together.
  - Pass: in each class, at least 4 of 6 fits are valid, and the median |V_rec/430 − 1| ≤ 0.10.
- **(V3) No false fits.** Noise-only cubes, and cubes with the line outside the window, give 0 of 6 scored fits.
- **(V4) The hard classes must test something (MUTATE).** With G3 off (frozen fitter), at least one hard class must reproduce
  the I0 = 0 collapse in at least 1 of 6 seeds. If none does, V2 has not exercised the repair. Then G3 is NOT VALIDATED, and the owner
  decides whether to proceed.
- **If V1–V3 fail:** G3 is not run on the real cube. The record says so. The rules are not retuned to pass.

## Running it on the real cube
- **A new spw25 stream is needed** (34,749,031,680 B), which needs the owner's yes. The cutout sha256 must equal 61f147499c28123e….
- **Run order:** the frozen fit first (must reproduce the release), then G3, then the MUTATE (+1000 km/s, must fail G1-3D).
- **Report every branch:** start grid winner, Δχ² vs empty, the three starts, and validity.
- **Scored rows go to the scorecard labelled POST-DATA REPAIR (G3).**
  - B1: V_c compared with the 431 km/s input-grid minimum. A lower value challenges the mass or pressure inputs, not a0.
  - B2: applies only near 430.
  - B3, B4: under the filed separation rule.
- **No PAPER66 change** without the owner's go.

## Alternatives considered, not taken
- **Clamp I0 above zero only.** It removes the absorbing state, but the fit still starts worse than empty. Rules 2–3 address the cause.
- **Starting from the release cube's own best-fit kinematics.** This would be tuning on the data, so it is not allowed.
- **A full MCMC.** It is a larger change and its own validation burden. Kept as a later option.
- **Dropping the 3D centroid and keeping only the grid.** The centroid is already part of the filed G1-3D measurement, and costs nothing.
