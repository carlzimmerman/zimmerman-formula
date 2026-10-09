# CFG574: Milky Way HI flaring, round rule (RM) vs phantom disc (PD). NOT DIAGNOSTIC as frozen; the decision moves to the gas dispersion

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (0371938fe). (owner chat 10-09)
- **Script:** `cfg574_flaring.py` → `cfg574_flaring.out`, `cfg574_results.json`; MUTATE `CFG574_MUTATE=1` → `_MUTATE` outputs. Runs in about 1 s.
- **Re-used by execution, not edited:** CFG516's definitions (CFG514 solver, McMillan17 baryons, RM-φ, RM-v, PD, homeoid).
- **Data:** Kalberla & Dedes 2008 (arXiv:0804.4831), read from the source TeX: HI HWHM h(R) = 0.15 exp((R − 8.5)/9.8) kpc for 5 ≲ R ≲ 35 kpc (R_sun = 8.5 kpc, azimuthal average, no error bars).
- κ = ½ fitted; both footings, never pooled; A = 1; cold energy's mass still required; not theory closed.

## Result

Fitted constant σ, scored on R = 10–30 kpc (primary: gas layer at the observed flaring):

| footing | model | σ (km/s) | rms_ln | R0 (kpc) | consistent |
|---|---|---|---|---|---|
| canonical | RM-φ | 6.80 | 0.091 | 9.77 | yes |
| | RM-v | 6.90 | 0.091 | 9.81 | yes |
| | PD | 8.97 | 0.056 | 9.86 | yes |
| | Newton only (C2) | 5.77 | 0.140 | 8.18 | yes |
| alt | RM-φ | 6.91 | 0.092 | 9.91 | yes |
| | RM-v | 7.01 | 0.092 | 9.96 | yes |
| | PD | 9.29 | 0.056 | 9.92 | yes |
| | Newton only (C2) | 5.77 | 0.140 | 8.18 | yes |

- **Verdict as frozen: NOT DIAGNOSTIC on both footings** (all models consistent). The variant with McMillan's fixed 85 pc gas layer and the disclosed post-freeze R_sun rescaling (×0.9555) give the same call.
- **Control C2 FAILS:** Newtonian baryons alone also match the flaring shape at σ = 5.8 km/s. With σ free, the flaring SHAPE carries almost no information about the dark component: every model's vertical force falls with radius so that h(R) is close to exponential with R0 ≈ 9.8 kpc.
- **MUTATE: DETECTED.** RM-φ's cold mass in a q = 0.3 homeoid is inconsistent in all four cells (rms 0.152–0.164, R0 12.3–12.9 kpc). The statistic does reject a strongly flattened cold component; QUMOND's phantom is not that flat at these radii (it becomes round beyond the transition radius).
- C1 (grid baryon mass 6.6418e10 vs 6.64e10) and C3 (HWHM extractor, 1%) pass. Checks 2/4 (both failures are C2, one per footing).

## What the test does decide

The models differ in the gas dispersion they need, not in shape. At the observed flaring:
- RM needs σ ≈ 6.8–7.0 km/s; PD needs σ ≈ 9.0–9.3 km/s (ratio 0.75, i.e. PD's vertical force ≈ 1.7× RM's, matching CFG516's 1.6–3.6×); Newtonian baryons alone need 5.8 km/s.
- **Next step (needs an owner go):** an independently measured HI velocity dispersion for the outer Milky Way disc (R ≈ 10–30 kpc). A value near 7 km/s favours the round rule, near 9 km/s the phantom disc. The 5–15 km/s plausibility band used here is recalled (PROVISIONAL) and too wide to decide.

## Limits (disclosed)
Azimuthal-average flaring with no errors; warp and lopsidedness beyond 15 kpc; single-phase isothermal gas with constant σ (a radial σ gradient would trade directly against the dark component); A = 1 only; KD08 distances use R_sun = 8.5 kpc vs the model's 8.122 kpc (variant rescaling changes nothing).
