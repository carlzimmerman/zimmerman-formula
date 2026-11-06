# AC1 addendum G4 (DRAFT, NOT FILED): second disc-fit repair for U4_28473, after G3 failed validation

**Status: draft for the owner. Not filed. Nothing runs under it until the owner files it.** Filing means:
- the owner says so in chat;
- this text is committed unchanged as `rebuild_2026_10_22/AC1_alma_condor_predictions/ADDENDUM_G4_<date>.md`.

It supplements, and does not edit, FROZEN_CRITERIA.md, ADDENDUM_G1.md, ADDENDUM_G2_2026-11-04.md or ADDENDUM_G3_2026-11-06.md. G3 stays
on record as filed and **FAILED VALIDATION** (AL3, bacad8124f); G4 replaces it as the candidate repair and does not reopen it. No
prediction value, mass branch, detection gate, seal, error floor or U4_27928 rule changes. κ = ½ FITTED; one disc excludes no model;
not theory closed.

## This is a POST-DATA repair, written after a failed one. Say so everywhere
- Everything G3 disclosed still holds:
  - the release cube has been read;
  - the frozen fit collapsed to I0 = 0 (AL1, AL2);
  - the 3D centroid (≈ −172 km/s), the start-vs-empty cost and the noise statistics have been seen.
- In addition, G3's MOCK results (AL3) have been seen, and G4's rules are shaped by them. That is a second post-hoc step, disclosed here.
- **Still no V_c from this cube under any working fit.** Any row scored under G4 is labelled **"POST-DATA REPAIR (G4)"**. The
  release's "FIT NOT CONSTRAINED" and G3's "FAILED VALIDATION" stay beside it.
- A G4 score can test a prediction. It cannot be presented as a pre-registered blind test.

## What AL3 showed, and what G4 does with it
1. **Log amplitude works** (0 of 246 fits at I0 = 0). Kept.
2. **The PA/vsys start grid caused the V1 regression.**
   - At a low vf0 the coarse grid picks a wrong PA, and that start converges to a different, wrong minimum (e.g. vf 10 at PA −1.7 rad).
   - The three-start gate then rejects fits that G2 got right.
   - G4 removes the grid entirely.
3. **The ρ₁ estimator is biased low.** AL2's continuum-only estimate has very few channels after subtraction: it reads −0.06 on
   independent noise and 0.14 on ρ 0.24. G4 replaces it.
4. **The adequacy threshold divided where it should multiply.** G4 corrects the direction.
5. **The clump classes fail under both fitters.** The thin disc shrinks onto the clump, and V_f pins at its bound. That is model
   inadequacy, and the frozen bound gate already refuses those fits. G4 does not try to fit non-disc structure. Its validation requires
   such cubes to be *refused, not mis-scored*.
6. **No mock reproduced the collapse**, so AL3's control could not bite. AL3's mocks were far more line-dominated per voxel than the
   real cube (AL2 R4: peak voxel 4.9σ, detected only in aggregate). G4's validation adds a class sized, by a rule fixed here, to
   reproduce the collapse under the frozen fitter before G4 is tried on it.

## Ruling (generic; no number below was chosen from this cube's kinematics)
1. **Amplitude in logs** (as G3 rule 1). Fit u = ln I0, with bounds [ln(1e-4 I0\*), ln(1e3 I0\*)], I0\* from rule 3.
2. **vsys start from the 3D detection** (as G3 rule 2): the flux-weighted velocity of the G1-3D mask.
3. **Analytic amplitude at the frozen start, no grid.**
   - For each of the three frozen vf starts, the start is the frozen start with only two changes: vsys from rule 2, and
     I0\* = ⟨M₁, D⟩ / ⟨M₁, M₁⟩ at that start (M₁ is the unit-amplitude model), floored at 1e-6 of the frozen I0 start.
   - The PA, centre, R_t, σ0 and h starts are the frozen ones.
4. **Three-start gate unchanged** (G2 §1).
5. **Model-adequacy gate, corrected direction.**
   - Score a branch only if its best fit beats the empty model by Δχ² ≥ 25 × (1 + 2 max(ρ₁, 0)), in the fit's own
     independent-voxel units.
   - Otherwise it reads "FIT NOT CONSTRAINED: model no better than empty".
6. **ρ₁ estimator.** Lag-1 channel autocorrelation measured on off-source pixels (r > 2"), using every box channel (|v| ≤ 650 km/s),
   each pixel's spectrum mean-subtracted, pooled: Σ x_k x_{k+1} / Σ x_k².
   - Off source carries no line, so no channel is excluded.
   - Covariance × (1 + 2 max(ρ₁, 0)); the error floor is unchanged (G2 §2).
7. **Everything else unchanged:**
   - inclination branches;
   - pressure branches P-B and P0, never pooled;
   - G2 radius rule;
   - the at-bound, q-clamp and σ(V_c)/V_c ≤ 0.25 gates;
   - the C1 injection check (frozen fitter);
   - the scoring grid.

## Validation before G4 touches the real cube (lane AL4, MOCK only, criteria committed first)
- Settings and seeds as AL3 (release settings: pix 0.015", beam 0.105" × 0.087", dv 6, 0.132 mJy/beam, S dV 0.718, V_c 430,
  Tadaki inclination). AL3's writer passes K0 and is reused. AL3's frozen-fitter records may be reused for the frozen side, by sha256.
- **(C) Calibration of the collapse class, frozen fitter only, before any G4 fit.**
  - Class (e) is class (a) + (c) (offset −172, ρ 0.24) with the gas R_e scaled by f, stepping up the ladder f = 2, 3, 4 (flux fixed).
  - The class used is the smallest f at which the frozen fitter ends at I0 = 0 in ≥ 1 of 6 seeds of the primary branch.
  - The calibration's seeds are new; the class is then re-drawn with six *further* new seeds for V2 and V4.
  - If no f collapses, V4 cannot bite. G4 is then **NOT VALIDATED**, and the owner decides.
- **(V1) No regression**, as AL3 V1. Selftest plus the two G2 §3 power suites. Primary valid count ≥ G2's, and Tadaki P-B RMS ≤ G2 + 0.02.
- **(V2) Recovery and refusal.**
  - Classes (a), (c) and (e): ≥ 4 of 6 valid, and median |V_c,P-B / truth(R_score) − 1| ≤ 0.10. truth(R) is G2's generating curve.
    For (a) and (c), |V/430 − 1| is also printed.
  - Classes (b) and (d), the clumps: no valid fit with |V_c,P-B / truth − 1| > 0.15. Refusal passes; a confident wrong speed fails.
- **(V3) No false fits**, as AL3 V3 (noise-only and line-outside cubes, 0 of 6 scored each).
- **(V4) MUTATE, two parts.** On the V2 class (e) cubes:
  - (i) the frozen fitter collapses (I0 = 0) in ≥ 1 seed;
  - (ii) G4 with rule 1 switched off (linear I0, bound 0, everything else G4) collapses in ≥ 1 seed.
  - If (ii) fails, the log amplitude is not what repairs it. That is reported, and G4 is NOT VALIDATED.
- **Verdict.**
  - G4 VALIDATED iff C, V1, V2, V3 and V4 all pass.
  - If V1, V2 or V3 fails: G4 FAILS VALIDATION. It is not run on the real cube, and the rules are not retuned.
  - A third repair would need a further addendum. The owner may instead leave B1–B4 unscored for good.

## Running it on the real cube (only if VALIDATED)
- **A new spw25 stream is needed** (34,749,031,680 B), which needs the owner's yes. The cutout sha256 must equal 61f147499c28123e….
- **Run order:** the frozen fit first (must reproduce the release), then G4, then the MUTATE (+1000 km/s, must fail G1-3D).
- **Report every branch:** ρ₁, the centroid, I0\*, Δχ² vs empty, the three starts, and validity.
- **Scored rows are labelled POST-DATA REPAIR (G4).**
  - B1: V_c compared with the 431 km/s input-grid minimum. A lower value challenges the mass or pressure inputs, not a0.
  - B2: applies only near 430.
  - B3, B4: under the filed separation rule.
- **No PAPER66 change** without the owner's go.

## Alternatives considered, not taken
- **Keep G3's grid but over vsys only.** AL3's archive-compact seed 3 also went wrong on a vsys-only grid move (−100 vs +100 between
  starts), so it is dropped too.
- **A clump or two-component model.** It would add fitted structure chosen after seeing that clumps fail. That is its own addendum and its
  own validation, if ever.
- **A full MCMC.** Still a later option.
- **Stop here and leave B1–B4 unscored.** Always allowed. G4 is offered because AL3 located the regression precisely; filing it is the
  owner's choice.
