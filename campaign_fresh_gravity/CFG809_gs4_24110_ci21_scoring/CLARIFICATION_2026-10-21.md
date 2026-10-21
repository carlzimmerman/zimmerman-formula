# CFG809 clarification, 2026-10-21 (owner decision; written before any programme 2025.1.01377.L data; FROZEN_CRITERIA.md is not edited)

This note resolves the wording ambiguities that CFG942's readiness lane listed (`CFG942_alma_scoring_readiness/README.md`,
"Ambiguities"). It follows the owner decision of 2026-10-20 (`OWNER_DECISION_2026-10-20_ALMA_GOVERNING_PLANS.md`): this plan
governs the GS4_24110 score, AG5 is a secondary reading only, and one disc excludes no model.

The ambiguities were found on MOCK cubes only.

**How each item was decided:**
- Where the literal text runs, it is kept. Section 8 forbids changing §4 and §5.
- Where it is broken, the fix makes a claim harder, the same way for every model.
- Where two readings exist, the one that claims less is taken, unless the grammar is clear.

## Scoring (§4; literal kept)
- **A-G1.** σ_Δv uses the plan's 0.2 dex M★ systematic. CFG572's ±0.1 dex is printed as information.
- **A-G2.** The FLOOR rule stands as written. A FLOOR model is in tension whenever gas is detected on that route. Where Δ_v alone
  reads consistent, the report prints that next to the FLOOR verdict. This is said plainly: a FLOOR tension is a stellar-mass
  statement that the gas detection only switches on.
- **A-G4 (ROBUST).**
  - The other routes are CFG572's primaries: CO43 at r41 = 0.37 with α_CO = 4.36, and dust at α_CO 4.36. The other CFG572 branches
    are printed.
  - ROBUST / NOT ROBUST is decided per model, as the sentence "A model's verdict … is ROBUST only if" reads.
  - Stated now, before data: with CFG572's routes fixed, the framework's verdict is NOT ROBUST for every CI21 value (CFG942 MOCK).
    So this disc can neither support nor disfavour the framework. Only the rivals' FLOOR tension can come out ROBUST.
- **A-G3 (upper limit).** If G1 fails, Δ_v is the interval [f(0), f(UL)]. A model is reported in tension only if its required value
  lies more than 2σ_Δv outside the whole interval. Otherwise the result is "not constrained".

## Measurements (§3; clarified before data)
- **A-G13 (G1 significance).** S/N is measured against a selection-aware null: the same ≥ 2σ mask procedure, grown at 200 random
  off-source seeds. The literal ring-aperture S/N passes on pure noise (MOCK GS4-b: 10.6), so it is printed but never decides G1.
- **A-G9 (G3).**
  - The FWHM error for gate G3 is the fit covariance corrected for beam-correlated noise, scaled by √(pixels per beam).
  - The Gaussian-to-exponential size bias (MOCK: the fitted R_g is about 0.69 of the true value) is reported. It is not corrected,
    because the plan's formula R_g = R_e,CI/1.678 is kept.
- **A-G5.** The upper-limit aperture is the R_e circle.
- **A-G6.** The continuum S/N is the peak S/N inside the [CI] mask.
- **A-G8.** The ring for the printed literal noise sits at 6.5″ (inside 5–8″). The primary beam at 270 GHz is larger, so no noise map
  is needed.
- **A-G10 (C4).** The "< 1e-6" check uses the coefficient derived from the A values (4.56583e-4). M_CI uses the plan's rounded
  4.566e-4. The 3.7e-5 relative difference is reported.
- **A-G11 (MUTATE).** The shift stays +2000 km/s. If +2000 km/s leaves the spectral window, MUTATE runs at +1000 km/s, as CFG572's
  disclosed `--mutate1000`. That shift is still more than 3× the ±300 km/s window. The fallback is labelled.
- **A-G12 (G4).** At least 3 beam-spaced samples along the major axis, monotonic, each at S/N ≥ 5.
- **A-G16.** After a G1 failure the continuum is reported in the R_e circle.
- **A-G14 (taper).** None. If the native cube fails G1, the upper limit is the result.
- **A-M1 / A-M2.** As CFG806-U4: the ≥ 2σ components touching a 0.5″ circle; the median beam when a BEAMS table is present.

## Housekeeping
- **A-X4.** This lane is dir `CFG809_gs4_24110_ci21_scoring`, called "CFG809-GS4" in reports to separate it from
  `CFG809_expelled_gas_split`. Its text's "CFG808" (the U4 lane, never to be pooled with this disc) means `CFG806_u4_27928_scoring`.
- **A-X5.** The header "DRAFT, not yet committed" is stale. The file was committed alone, before any download (966d50a87), and is
  the frozen plan.
- **A-X6 / A-X7.** `cfg809_gs4.py` was never written. The CFG942 harness `cfg942_gs4.py` stands in for it. It executes only the head
  of `cfg571_prereg.py`, and its K1 check verifies the seals in every run. Release-day outputs are copied here as `cfg809_gs4.out` /
  `cfg809_gs4_results.json`, with the harness's sha256 recorded.
- **A-X8.** The public date and sensitivity are re-checked on the archive before the download request. The download needs the
  owner's yes, with the size stated.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
