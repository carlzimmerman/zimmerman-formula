# CFG576: DiskMass σ_z, round rule (RM) vs phantom disc (PD). INCONCLUSIVE as frozen (calibration gate and MUTATE both fail)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (e1c6d8abe). (owner chat 10-09)
- **Script:** `cfg576_diskmass.py` → `cfg576_diskmass.out`, `cfg576_results.json`; MUTATE `CFG576_MUTATE=1` (a0 × 10 in RM) → `_MUTATE` outputs.
- **Data:** DMS VI (arXiv:1307.8130) Tables 1, 5, 6 and DMS VII (arXiv:1308.0336) h_R/h_z and mass tables, copied verbatim into `data/`. All 30 galaxies parse.
- κ = ½ fitted; both footings, never pooled; cold energy's mass still required; not theory closed.

## Result (median σ_pred/σ_meas over 30 galaxies, bootstrap 68%)

| footing | radius | RM | PD | median Υ_K | median B (RM / PD) |
|---|---|---|---|---|---|
| canonical | 1.5 h_R (primary) | 1.250 [1.205, 1.291] | 1.475 [1.397, 1.542] | 0.452 | 1.10 / 1.63 |
| canonical | 2.2 h_R | 1.168 [1.078, 1.254] | 1.469 [1.352, 1.596] | 0.390 | 1.11 / 1.90 |
| alt | 1.5 h_R (primary) | 1.212 [1.167, 1.265] | 1.475 [1.397, 1.542] | 0.402 | 1.12 / 1.77 |
| alt | 2.2 h_R | 1.129 [1.058, 1.223] | 1.476 [1.358, 1.604] | 0.345 | 1.14 / 2.10 |

Newtonian reference (C2: Υ_K from the RC, B = 1): r = 1.494, Υ_K = 0.82 (the DMS "sub-maximal disc" tension).

## Verdict as frozen: INCONCLUSIVE
- **G-cal FAILS:** PD on the alt footing gives 1.475, just outside [1.15, 1.45] around Angus et al. 2015's ≈1.3.
  The frozen rule says the approximation is not trusted, so no call is made. (Angus+15 fit Υ and h_z jointly by
  MCMC to the full profiles; this lane fits Υ to the rotation curve at one radius and uses a one-zone vertical factor.)
- **MUTATE FAILS (not detected):** with a0 × 10 in RM, RM's median r drops to 0.90–0.92 ("consistent") only by
  driving Υ_K to 0.05–0.06, with 10 of 30 galaxies unfittable. **The r statistic alone can be satisfied by a wrong
  model through Υ_K; any repeat must gate on Υ_K plausibility (and keep every galaxy) as well as r.**

## What the numbers say (reported, not a verdict)
- The round rule predicts σ_z closer to the measured values than the phantom disc, at every radius and footing
  (1.13–1.25 vs 1.47–1.48), with the same Υ_K; the vertical boost is 1.10–1.14 for RM against 1.63–2.10 for PD.
- RM still over-predicts σ_z by 13–25% at DMS's adopted scale heights. Variants: h_z × 0.75 gives RM 1.07, PD 1.28;
  k = 2 raises both (RM 1.44, PD 1.70); removing gas changes little.
- So RM removes most of MOND's known DiskMass excess but not all of it at the adopted h_z. This is not a win as
  frozen, and must not be cited as one.

## Limits (disclosed)
Rotation amplitudes come from Tully–Fisher inclinations (face-on sample); σ_z from DMS exponential fits
(young-tracer bias debated, Aniyan et al.); h_z inferred from h_R, not measured; one-zone vertical factor at
z = h_z; assumed gas profile shapes; M_sun,K = 3.28 (PROVISIONAL).

## Next step (needs an owner go)
A repeat with frozen Υ_K-plausibility gates and a proper vertical solve (the CFG516 grid machinery on each
galaxy), re-calibrated against Angus+15 before scoring.
