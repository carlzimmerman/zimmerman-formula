# X79_native_eta_mw_kids: native η does NOT rescue the Milky Way in priors or KiDS lensing

Criteria: `FROZEN_CRITERIA.md` (c7d5c7f1c1), committed before any script or number.
Rule: route E's Σ = max(Σ_a0, η_native(M) Σ_coll(M)), smooth core, with η_native from X77's direct measurement on the
native zoom halos (20.83 / 13.79 / 14.39 at 1e12 / 1e13 / 1e14) in place of η = 10.82 (c_f 4).

## Milky Way (GD3's stage-M box, read-only; only Σ changed)
| configuration | canonical class | best in-prior cell (R_d 2.60) | McMillan baryons |
|---|---|---|---|
| OS1 σ-law (= GD3, K1 identity exact) | FEASIBLE (WIDE PRIORS ONLY) | v_c 209.9, D 3.14 | v_c 201.7 |
| route E, η 10.82 (c_f 4) | V+K ONLY | v_c 202.5, D 8.09 | v_c 193.8 |
| **route E, η native (graded)** | **FEASIBLE (WIDE PRIORS ONLY)** | **v_c 209.1, D 3.51** | **v_c 200.1** |

- Eilers v_c(R₀) is 229.1 ± 4.6. Native η raises the MW core 1.36× over the floor (canonical, collapse branch active)
  and lifts the class from V+K ONLY to wide-priors feasible. The only passing cells are still R_d 1.93 kpc, outside
  Licquia & Newman.
- **Inside the priors the Milky Way still misses by about 20 km/s (about 4σ).**
- Alt: the class is SPARC LINE FAILS (X77's alt SPARC Υ 0.45); the MW rows are reported only.
- MUTATE (η × 2): Σ/Σ_a0 1.36 → 2.71, as required. Note that even 2× η leaves the class at V+K ONLY: K_z and the outer
  curve break as v_c rises.

## KiDS-1000 galaxy lensing (X53 via X74_smooth_core_lensing; only η changed)
| | Δχ²(H2H − L2H), all radii | R ≤ 0.31 Mpc | X53 rule |
|---|---|---|---|
| canonical, η 10.82 (K2 identity exact) | +423.7 | +127.2 | LAW |
| **canonical, η native** | **+432.2** | **+135.7** | **LAW** |
| alt, η 10.82 | +458.4 | +147.4 | LAW |
| **alt, η native** | **+461.5** | **+150.5** | **LAW** |

- **Native η makes galaxy lensing slightly worse (+8.5 / +3.1).** At fixed halo mass, a denser core does not supply
  the missing outer signal. X53 A1 / X74 lensing locate the deficit in M200 (it needs +0.3–0.5 dex), not in the core.
- MUTATE (η × 2): H2H χ² 586.5 → 635.3, as required.

## Reading
The measured, mass-dependent η (c_f "falling with mass") is what passes the cluster line set on a knife edge (X77). It
does not fix the two galaxy-scale failures:
- the Milky Way inside the published disc priors;
- KiDS galaxy lensing, which is a halo-mass deficit.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating
field component, never a particle.
