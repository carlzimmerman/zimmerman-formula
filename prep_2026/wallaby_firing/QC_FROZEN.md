# QC_FROZEN — Lane W1 bulk per-side extraction (WALLABY, N=237)

**FROZEN: 2026-07-16, BEFORE any real per-galaxy A value was computed in this lane.**
(Only the 3 PILOT galaxies of `wallaby_prep/perside_extractor.py` had A values in hand
before this freeze; they were proof-of-life, and they pass through the same frozen cuts
below like every other galaxy.)

## FIREWALL (applies to every output of this lane)

At N~237 the achieved sensitivity at AQUAL amplitude is ~1–1.5 sigma
(n=16 gave 0.3 sigma; sqrt(237/16) = 3.85x). **NEITHER pre-registered kill
condition (3-sigma AQUAL-vs-BranchB; N~1,157 canonical a0 = 9.36e-11, N~1,424
alt a0 = 1.13e-10, both at max-clustering e_N, w = 0.304) CAN TRIGGER on this
sample.** Kill-condition language in this lane may appear ONLY as "cannot trigger".
a0 does not enter the extractor at all; both footings are carried at the
confrontation stage only.

## Pre-registered sign convention (THE SIGN TRAP)

- **Pre-registered**: A_i = 2(v_rec − v_appr)/(v_rec + v_appr), tied to the
  RECEDING side, paired with psi measured from the RECEDING-side kinematic
  major axis, so that p_i > 0 predicts attractor-side-FASTER for x ≳ 2e.
- **Extractor raw** (`perside_extractor.py`): A_ext = 2(v_app − v_rec)/(v_app + v_rec)
  — the OPPOSITE ordering. Conversion: **A_preregistered = − A_ext_raw**
  (identical denominator, negated numerator). BOTH values are recorded per galaxy.
- The conversion MUST be verified by hand on ≥ 1 galaxy directly from the raw
  mom1 map (which sky side is receding, its outer wedge velocity, the arithmetic)
  before the bulk CSV is accepted.

## PA convention (verified from Deg et al. 2022, arXiv:2211.07333, not assumed)

- Deg+22 Table 4 (data-release column definitions), quoted: PA_model =
  "Position angle in pixel coordinates (counterclockwise from x=0)";
  **PA_model_g = "Position angle in equatorial coordinates (East of North)"**;
  the two differ by a small cubelet-header rotation ("typically less than 2
  degrees", Deg+22 Sec. 5). We use **PA_model_g** on the WCS sky grid.
- Deg+22 does NOT itself restate the receding-side anchoring; that is the
  tilted-ring convention of both underlying fitters (TiRiFiC/FAT and 3DBarolo:
  PA of the RECEDING half of the major axis, N through E). Because the paper
  text does not pin it, the receding side is **determined EMPIRICALLY per
  galaxy** (frozen rule below), never assumed.

## Frozen empirical receding-side rule

For each galaxy, deprojected v_rot = (v_los − VSys_model)/(sin i · cos θ) is
computed with θ from PA_model_g. If the fitter PA points at the receding side,
median(v_rot) > 0 on both sides. **If median(v_rot) < 0 over the used pixels,
the PA is anti-aligned with the receding side: the app/rec labels are swapped
before any A is formed, and the galaxy is flagged `pa_flipped=True` in the CSV.**
The count of flips is reported (expected ≈ 0 if the fitters honor the
convention). This makes A_preregistered tied to the TRUE (data-determined)
receding side in all cases.

## Frozen QC cuts (a galaxy failing ANY cut is EXCLUDED, reason logged)

| # | Cut | Threshold | Rationale |
|---|-----|-----------|-----------|
| 1 | Inclination | **Inc_model < 70 deg** | RELEASES.md warning: thick-wedge projection systematics inflate A at high inc (pilot J100426−282638, inc 75.1°, A = +0.225 — visibly inflated) |
| 2 | Sanity ratio | **median[(v_app+v_rec)/2 / WKAPP VRot_model] ∈ [0.8, 1.2]** over rings matched to the released rotation curve | per-side azimuthal mean must reproduce the released azimuthally-averaged curve; outside band = geometry/extraction breakdown |
| 3 | Outer rings | **n_outer ≥ 4** rings entering the outer-mean A | fewer = A dominated by a single ring; matches the pre-registered outer-curve definition |
| 4 | Bootstrap error | **sigma_boot(A) < 0.05** | galaxies noisier than half the WHISP 0.092 intrinsic-lopsidedness rms contribute negligible ensemble weight while admitting junk |
| 5 | Extraction integrity | files download + parse + extractor returns a valid result (finite A, finite sigma_boot) | mechanical failure = excluded, never imputed |

No other cut may be applied downstream of this freeze. Any additional
exclusion at the firing stage would be post-hoc and is forbidden.

## Frozen ancillary rules (fixed now so no per-galaxy discretion remains)

1. **Model choice when a galaxy has >1 released WKAPP model** (58 such
   galaxies: Hydra TR1/TR2, NGC 5044 TR1/TR2/TR3, NGC 4808 std/High-Res):
   pick the **highest team-release number TR**; on a TR tie, prefer the
   **High-Res (12″)** model (finer beam = better ring sampling). Deterministic,
   frozen before any A is seen. Deg+22 note the 15 Hydra TR1-vs-TR2 duplicate
   models differ by less than their uncertainties.
2. **mom1↔AvgMod pairing**: mom1 filename = AvgMod filename with `_Kin`
   removed and `AvgMod.txt` → `mom1.fits`, with the field-name normalization
   `NGC5044` → `NGC_5044` (CADC naming inconsistency in the TR3 kin release).
   Pairing is against the live CADC census list (census_cache.json, LIVE
   2026-07-16), never guessed.
3. **Weights**: mom0 map (same name pattern, `mom0.fits`) as intensity weight,
   exactly as the validated pilot; if the mom0 download fails after retries,
   the galaxy is run **unweighted** and flagged `weight=none` (not excluded —
   the gate calibration used intensity weighting, so unweighted galaxies are
   flagged for the firing stage to inspect).
4. **Extractor parameters**: byte-identical machinery to the gate-validated
   `wallaby_prep/perside_extractor.py` — wedge |cos θ| ≥ 0.5, outer rings =
   R_mid ≥ 0.5·R_max, ring edges from the released AvgMod rotation-curve radii,
   3σ pixel clip, pixel bootstrap nboot = 400, mom1 Hz → cz km/s via
   cz = c(f0/f − 1), f0 = 1420405751.77 Hz. NO parameter is tuned in this lane.
5. **Downloads**: CADC raven
   `https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/raven/files/cadc:WALLABY/<file>`,
   ≤ 4-way parallel, 3 retries with backoff on transient failures; pilot files
   already in `wallaby_prep/pilot_data/` are reused, not re-downloaded.

## What this lane does NOT do

- No correlation of A with any g_ext direction, field vector, or predictor
  p_i — that is the firing lane, not W1.
- No verdict of any kind on AQUAL / Branch B / pure MI. The only statistics
  reported are the QC funnel, the sigma(A) distribution vs the WHISP 0.092
  intrinsic rms, and per-field breakdowns of extraction health.
