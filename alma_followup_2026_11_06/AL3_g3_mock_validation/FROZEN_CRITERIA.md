# AL3: MOCK validation of the filed AC1 addendum G3 (V1–V4). FROZEN CRITERIA, before any script or number

Written before any AL3 code or run, and committed alone. Governing text: `rebuild_2026_10_22/AC1_alma_condor_predictions/ADDENDUM_G3_2026-11-06.md`
(filed 2026-11-06, commit 315d8e4eaa, sha256 6d0de6e3…). MOCK cubes only. No ALMA data and no download. Scores nothing. Changes no
frozen file, prediction, gate, seal or error floor. κ = ½ FITTED; one disc excludes no model; not theory closed.

## How G3 is applied (in this process only; no frozen file is edited)
- `al3_g3.py` replaces `cfg942_common.fit_disc` in-process with a G3 fitter, and wraps `ac1_score.g1_3d` to record the G1-3D mask.
  The frozen `ac1_score.measure()` and `power()` then run unchanged around it. Every other line of the scorer is the frozen code.
- The G3 fitter applies only to the main thin-disc fits (calls without an `I0` argument). The C1 injection check passes `I0` and keeps the
  frozen fitter, as G3 rule 7 lists C1 as unchanged.
- **Rule 1.** Index 7 of the parameter vector becomes u = ln I0, bounds [ln(1e-4 I0\*), ln(1e3 I0\*)] (I0\* from rule 3's chosen grid
  point). The frozen `lm_fit` is called unchanged. Returned parameters are converted back to I0; the I0 row and column of the covariance are
  multiplied by I0 (delta method). V_c uses indices 4–6 only, so it is unaffected by the conversion.
- **Rule 2.** vsys centroid = flux-weighted velocity of the G1-3D mask, computed with the same two lines `measure()` uses for z_line
  (v = c (z_line − z)/(1 + z)), from the recorded mask. The frozen moment-1 vsys is logged beside it.
- **Rule 3.** Grid vsys = centroid + {−100, −50, 0, +50, +100} km/s × PA = pa0 + {0, +45°, −45°, +90°, −90°, 180°}; other start values as
  frozen (centre, the call's vf0, R_t 1.0, σ0 40, h0). The PA and vsys starts are clipped into the frozen bounds as `fit_disc` clips. At each
  point I0\* = ⟨M₁, D⟩ / ⟨M₁, M₁⟩ in the fit's residual units, floored at 1e-6 of the frozen I0 start; the lowest-cost point is the start.
- **Rule 5.** Δχ² = Σ(D/σ)² − χ²_best in the fit's own units. If Δχ² < 25 / (1 + 2ρ₁) the fit's covariance is set to NaN, so the frozen
  validity test (finite error) fails it, and the log records "model no better than empty".
  - Because the reported branch is the lowest-χ² trial, if the best trial fails the gate every trial fails. The gate therefore acts on the
    best fit, as filed.
  - **Disclosed before any run:** a whitened Δχ² is the naive one divided by (1 + 2ρ₁). Requiring a whitened Δχ² ≥ 25 would mean a naive
    threshold of 25 × (1 + 2ρ₁), not 25 / (1 + 2ρ₁). The filed rule is applied as filed. Every fit also logs whether it would pass at
    25 × (1 + 2ρ₁) (information only; it decides nothing here). The owner decides whether this is a typo to correct by a further addendum.
- **Rule 6.** ρ₁ is measured on the fit's box exactly as AL2 R4 measured the release's +0.24: continuum channels |v| > 600 km/s, pixels at
  r > 2", every 97th pixel, mean-subtracted, Σ x_k x_{k+1} / Σ x_k². The covariance is multiplied by (1 + 2ρ₁) (as measured, no floor).
- **Rules 4, 7.** The three-start gate, bounds, at-bound checks, q clamp, σ/V ≤ 0.25, radius rule and error floor are the frozen code's.

## MOCK cubes
- `al3_mock.py` writes cubes with a copy of `write_mock_cube` plus three options: line offset (via nu_line, as AL1), a clump, and AR(1)
  channel-correlated noise. **K0:** with all options off it must write a cube with the same sha256 as the frozen `write_mock_cube` for the
  same spec and seed. If K0 fails, AL3 stops.
- **Release settings** (AL1 T3): pix 0.015", n 480, beam 0.105" × 0.087" PA 30°, dv 6 km/s, v ±1560, per-channel noise 0.132 mJy/beam,
  S dV 0.718 Jy km/s, gas R_e 1.56 kpc, V_c(P-B, 3 kpc) 430, σ0 40, R_t 0.5 kpc, Tadaki inclination, PA 0.5 rad.
- **Hard classes** (six seeds each: seed = 83000 + 97 i + class index × 1000, i = 0…5; the same cube feeds V2 and V4):
  - (a) line offset −172 km/s;
  - (b) lopsided: the exponential disc carries 0.6 of S dV; a clump carries 0.4, a Gaussian in the disc plane with σ = 0.15 R_e, centred at
    0.5 R_e and 45° from the receding major axis, moving with the disc's line-of-sight velocity at each pixel, line width σ0;
  - (c) channel noise AR(1) with ρ = 0.24 (n_k = ρ n_{k−1} + √(1 − ρ²) e_k; each e_k the frozen beam-correlated field normalised to σ);
  - (d) a + b + c together.
- **V3 cubes** (G3 on, six seeds each, seed = 89000 + 97 i + {0, 1000}): noise only (S dV 0); line at +1200 km/s (outside the fit window).

## Checks (`al3_run.py`; per-job JSON so a stopped run resumes; one summary `al3_validate.out/.json`)
- **T0** sha256 of `ac1_score.py`, `ac1_fit_checks.py`, `ac1_predict.py`, `ac1_score_power_results.json`, `FROZEN_CRITERIA.md`,
  `ADDENDUM_G3_2026-11-06.md` and `cfg942_common.py` identical at start and end.
- **T1 (G3 is live)** every main fit in a G3 run went through the G3 fitter (logged call count = 6 per detected cube), and every logged
  final I0 is > 0.
- **V1 (no regression)** with G3 on: the five-class selftest (`ac1_score.selftest`) and the two G2 §3 six-seed power suites (archive;
  noise / 2.54 with beam scale 1.661,1.299), same seeds as G2.
  - Baseline = `reviews/alma_readiness_2026_11_04/revision_v1_4/validation_summary.json` (G2 rerun).
  - PASS iff: selftest all checks PASS; for each suite × class, primary valid count (incl-Tadaki) ≥ G2's; and for each suite × class
    where G2 has ≥ 1 valid primary fit, the incl-Tadaki|P-B fractional RMS (against the generating curve at R_score, the G2 summary's
    `truth()`) ≤ G2's + 0.02. Other branches are reported, not graded.
- **V2 (hard classes)**: per class, PASS iff ≥ 4 of 6 incl-Tadaki fits valid AND the median |V_c,P-B / 430 − 1| over valid fits ≤ 0.10.
  The same median against the generating curve at R_score is also printed. If the two disagree on PASS, both are reported and the class
  reads SPLIT (owner decides).
- **V3 (no false fits)**: 0 of 6 cubes with any scored branch, in each of the two V3 classes.
- **V4 (MUTATE: the classes must test something)**: on the V2 cubes with the frozen fitter, at least one class has ≥ 1 seed whose reported
  best fit ends with I0 = 0 in at least one inclination branch.

## Verdict
- **G3 VALIDATED** iff T0, T1, K0, V1, V2 (all four classes PASS), V3 and V4 all PASS.
- If V4 fails: **G3 NOT VALIDATED (hard classes do not exercise the repair)**; the owner decides whether to proceed.
- If V1, V2 or V3 fails: **G3 FAILS VALIDATION**; it is not run on the real cube, and the rules are not retuned.
- Either way, G3 touches the real cube only after a new spw25 stream, which needs the owner's yes.

## What this lane cannot do
- It cannot say what the real cube gives. A MOCK pass shows the repaired fitter recovers known discs under these four kinds of difficulty,
  not that the real galaxy is a thin disc.
