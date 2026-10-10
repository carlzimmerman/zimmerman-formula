# CFG582: can cool (~10^4 K) CGM gas supply the KiDS early-type shortfall? COOL-GAS ESCAPE RULED OUT (one qualifying measurement)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (f9da6e77d). (owner chat 10-09)
- **Script:** `cfg582_score.py` → `cfg582_score.out`, `cfg582_results.json` (inputs transcribed in the script with their source).
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Measurement (read from source TeX)
Zahedy et al. 2019, COS-LRG II (arXiv:1809.05115): "Within d < 160 kpc from LRGs, we estimate a total cool gas mass of
M_cool = 1.5 (+0.7 / −0.3) × 10^10 M☉"; sample median log M* = 11.2 ± 0.2 (quiescent, z ≈ 0.4). The authors call it a
lower limit only because they stop at 160 kpc; extrapolated to 500 kpc they give ≈ 4 × 10^10 M☉.

## Result
- Scaled to 100 kpc (frozen M ∝ r): central 9.4 × 10^9, generous 1.4 × 10^10 M☉ = 0.087 M*.
- Required: 1.27 × 10^11 / 8.7 × 10^10 M☉ (0.8 / 0.55 M* at log M* 11.2); 5.0 / 3.5 × 10^10 even at log M* 10.8.
- **Verdict as frozen: COOL-GAS ESCAPE RULED OUT** — short by ×6.3 for the alt footing at the generous end. Even with no
  radial scaling (1.6–2.2 × 10^10 inside 160 kpc) or the 500 kpc extrapolation (0.25 M*), it falls short of 0.55 M*.

## Context (not scored)
Afruni et al. 2019 is a model (cool gas inside 160 kpc ≈ 1% of 2.5 × 10^11 M☉). Werk et al. 2014 (COS-Halos, mostly
star-forming L*) give > 6.5 × 10^10 M☉ inside R_vir — a different population.

## Scope (disclosed)
One qualifying measurement; COS-LRG galaxies are more massive (log M* 11.2) and at higher z (≈0.4) than the KiDS lenses
(≈10.8, z ≈ 0.2); the requirement was scaled to their M*. Absorption masses carry ≥ 0.5 dex ionisation-model
uncertainty; the generous end was used.

## Combined reading (CFG580–582)
Hot gas could hide from eROSITA (CFG580) but would cool out in a few free-fall times (CFG581); the cool gas actually
measured around quiescent galaxies is ~6× too little (CFG582). No measured baryon reservoir closes the KiDS/SLUGGS
early-type shortfall: it stands as a genuine limit of the law around massive early types, not missed baryons.
