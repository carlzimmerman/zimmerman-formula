# CFG779 FROZEN CRITERIA: does the FRB baryon census allow black-hole dark energy to have eaten the baryons?

Committed alone, before any script or number. 2026-10-14. Block CFG770–779 (last ID).

## Question
If coupled black holes source dark energy by converting baryons (Croker et al. 2024), then the surviving baryon fraction s_b
falls with time:
- s_b,0 = 0.43 in astra's conserved MD14 history (Ξ = 4.72);
- s_b,0 ≈ 0.70 in Croker et al.'s fit.

FRB dispersion measures count the ionized baryons along each sightline, so the mean DM_cosmic(z) must drop by s_b. Test it
on the raw localized-FRB sample already on disk (Sharma et al. 2026, 114 FRBs; CFG632's validated likelihood).

## Declared calculation
- **Likelihood.** CFG632's `cfg632_fit.py` functions, imported read-only: the authors' eq. 1 and host marginalisation over
  their flat box.
- **Model.** ⟨DM_cosmic⟩(z) = B · ⟨DM⟩_F(z), with ⟨DM⟩_F the record's mean (CFG632 predict: BBN Ω_b h², MD14 f_d,
  h = 0.70). The scatter shape is the census PRIMARY σ(z) with its amplitude lnA free and marginalised, so scatter cannot
  impersonate the mean.
  - Fit B on a grid ln B ∈ [−1.5, 0.7], step 0.02, flat prior. Report the posterior median and 68% interval, both footings
    (σ shape per footing).
- **Predictions for B.** B is the mean of s_b(z) weighted along the sightline, applied per FRB at its z:
  - P0, no conversion: s_b = 1.
  - P1, MD14 conserved history: s_b(z) = 1 − D(z)/B_i with D(z) = (Ξ/ρ_ref) ∫_z^∞ ψ dt. Ξ is fitted so that s_b(0) =
    0.4307 (astra's number), z_start = 8, MD14 ψ, flat Ω_m 0.308 background for dt.
  - P2, the Croker-like amount: the same shape, normalised to s_b(0) = 0.70.
  - For each FRB the predicted multiplier is B_i = ∫_0^{z_i} s_b(z′) w(z′) dz′ / ∫_0^{z_i} w(z′) dz′, with
    w = (1 + z)/E(z) (the DM kernel).
  - Score each prediction as Z = (ln B̂ − ln B_pred)/σ, using the side of the interval that faces the prediction.
- **Classes per prediction:** EXCLUDED if |Z| ≥ 3; TENSION if 2–3; CONSISTENT if < 2.

## Controls
- K1: with B fixed at 1 and lnA free, the code reproduces CFG632's PRIMARY lnA to 0.01.
- K2 (injection): mocks drawn with B = 0.5 (CFG632's `draw_mock`, 50 seeds, census PRIMARY canonical) recover median ln B
  within 0.1 of ln 0.5. This shows the host box does not absorb the mean.

## MUTATE (CFG779_MUTATE=1)
Mocks with B = 1 must give median ln B within 0.1 of 0. Mocks with B = 0.43 must be distinguished from 1 at ≥ 3σ on the
median; if not, the test is NOT DIAGNOSTIC.

## Hand estimate
- The authors' f_IGM ≈ 0.76 ± 0.1 (recalled) suggests B̂ ≈ 0.8–1.0 with ~12% errors.
- P1's sightline-averaged multiplier is ~0.45–0.6 at the sample's low z ⇒ P1 EXCLUDED.
- P2 at ~0.70–0.8 ⇒ TENSION at most.
- Caveat: the host box (μ 4–6) is wide, and K2 decides whether it absorbs the mean.

## Disclosures
- The FRB data were fetched in an earlier lane (CFG632; owner-approved).
- The MD14 history is a stand-in for Croker's Trinca history; P2 only rescales the amount.
- κ fitted; not theory closed.
