# CFG806 clarification, 2026-10-21 (owner decision; written before any U4_27928 data; FROZEN_CRITERIA.md is not edited)

This note resolves the wording ambiguities that CFG942's readiness lane listed (`CFG942_alma_scoring_readiness/README.md`,
"Ambiguities"). It follows the owner decision of 2026-10-20 (`OWNER_DECISION_2026-10-20_ALMA_GOVERNING_PLANS.md`): this plan
governs the U4_27928 score, AG5 is a secondary reading only, and one disc excludes no model.

The ambiguities were found on MOCK cubes only. No byte of programme 2024.1.00100.L has been read.

**How each item was decided:**
- Where the literal text runs, it is kept. Section 8 of the plan forbids changing §4 and §5.
- Where the literal text is broken (it passes on pure noise, or ignores correlated noise), the fix is the one that makes a claim
  harder, applied the same way to every model.
- Where two readings exist, the one that claims less is taken.

## Scoring words (§4; literal kept)
- **A-U1.** "Consistent" keeps its literal meaning: the measured M_gas lies inside the model's required range at the measured V_c.
  "In tension" keeps its literal meaning: more than 2σ_tot outside it. The case between the two is reported as **"not in tension
  (within 2σ_tot)"**. It is never called consistent.
- **A-U2.** σ_tot is literal: §3.3's flux error, which already carries the 0.15 dex floor, combined with §4's 0.15 dex. That gives
  about 0.21 dex. The single-floor value is printed as information only.
- **A-U15.** The 0.2 dex M★ systematic enters only where §4 names it: the reduced FLOOR statement. Elsewhere M★ is already inside
  §3.3's 0.15 dex floor. Widening the required range by ±0.2 dex in M★ (CFG942's alt3) is printed as information, never as the
  verdict.

## Measurements (§3; clarified before data)
- **A-U13 (G1 significance).** The S/N for G1 is measured against a selection-aware null: the same ≥ 2σ mask procedure, grown at
  200 random off-source seeds. The literal translated-mask S/N passes on pure noise (MOCK U4-d: 9.5), so it is printed but never
  decides G1.
- **A-U16 (V_c error).** The 1σ interval on V_c is the fit covariance corrected for beam-correlated noise, scaled by
  √(pixels per beam). This was CFG942's alt4 and is now primary. The independent-pixel covariance is printed as information.
- **A-U3 (moment-0 window).** ±500 km/s about z = 1.4193. The continuum is the median of channels with |v| > 600 km/s.
- **A-U5 (upper-limit aperture).** A circle of radius 2R_e = 0.98″.
- **A-U6 (non-detection).** If G1 fails, the 3σ upper limit on M_gas is reported and the run stops, as G1 says. No Δ_m is formed,
  because there is no V_c.
- **A-U7 (radius).** V_c is read at 8.3 kpc (§1, §3.1). The requirement comes from CFG571's sealed functions at their sealed
  2R_e = 8.271 kpc. The 0.3% radius difference is reported.
- **A-U9.** Headers are checked by frequency coverage of the redshifted line. RESTFRQ is reported, not required to match.
- **A-U10 (C2 "quoted noise").** The analytic mask-sum noise: beam-shaped correlation plus the continuum-median term.
- **A-U4 / A-U17 (C2 apertures).** An 8″ box with translated copies of the mask. The mean is tested against 3 rms/√N_independent.
  §5 is not changed. If C2 fails, the report states beside it the MOCK false-failure rate of the 20% rms test on pure noise (about
  10%).
- **A-U11.** If the moment-0 axis ratio is below q0 = 0.2, the inclination is set to 90° and flagged.
- **A-U12 (taper).** None. If the native cube fails G1, the upper limit is the result. No taper branch is added.
- **A-U12b (G2 radius).** The deprojected radius of the farthest mask pixel.
- **A-U14 ("2″ aperture").** Diameter 2″, i.e. radius 1″ ≈ 2R_e. The radius-2″ value is printed. This is only the 20% flux-agreement
  flag.
- **A-M1 / A-M2.** The mask is the ≥ 2σ components touching a 0.5″ circle at the catalogue position. If the cube carries a BEAMS
  table, the median beam is used.

## Housekeeping
- **A-X4.** This lane is the U4 scoring lane: dir `CFG806_u4_27928_scoring`, called "CFG806-U4" in reports to separate it from
  `CFG806_census_from_framework`. CFG809's text calls it "CFG808"; that means this lane.
- **A-X5.** The header line "DRAFT, not yet committed" is stale. FROZEN_CRITERIA.md was committed alone, before any download
  (1bf70683b), and is the frozen plan.
- **A-X6 / A-X7.** `cfg806_u4.py` was never written. The CFG942 harness `cfg942_u4.py` stands in for it. It executes only the head of
  `cfg571_prereg.py` (functions and constants), so the seal JSON is never rewritten. Its K1 check verifies the seals in every run.
  Release-day outputs are copied here as `cfg806_u4.out` / `cfg806_u4_results.json`, with the harness's sha256 recorded.
- **A-X8.** The public date and sensitivity are re-checked on the archive before the download request. The download needs the
  owner's yes, with the file size stated.
- **A-X3.** CFG571's own Δ_m on M_bar is printed as information. The verdict statistic is this plan's Δ_m on M_gas.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
