# X77_direct_core_surface_density: NATIVE η AT THE EDGE OF THE WINDOW (all masses); full grade KNIFE EDGE

Criteria: `FROZEN_CRITERIA.md` (21f010353f), committed before any script or number. The grader's smooth-core shape is
fitted to every finished X48 zoom halo, with X48's own centre, r_vir, fit range and objective. That gives
η_native = ρ₀r₀/(18π² ρ_m r_vir) = (4/3) a²/B_S(a) directly: no c_f, no r^0.75 infall map.

## Result (smooth core; nine-seed medians, 68 % bootstrap)
| mass, grid | η_native | limit (committed lanes) | grade | c_f-equivalent |
|---|---|---|---|---|
| 1e12, ng 64 | **20.83** [20.22, 21.61] | 21.2 (SPARC Υ floor) | INSIDE (by 2 %) | 6.75 |
| 1e12, ng 48 | 18.19 | — | resolution shift ng 48→64 +14.5 % (within 20 %) | 6.06 |
| 1e13, ng 48 | **13.79** [13.65, 15.24] | 14.3 (G-IN-Mall) | INSIDE (by 4 %) | 4.86 |
| 1e14, ng 48 | **14.39** [13.27, 14.50] | 14.3 | OVER ×1.01 | 5.03 |

- **K1** (synthetic smooth core a = 6 recovered, 6.04) and **K2** (formula vs integral, exact) pass. **MUTATE** (radii
  inside r_vir/4 × 0.8) raises η by 41–51 %, as required.
- **The infall map is fine. The r₋₂ crossing was not.** A synthetic NFW with c = 4 gives η_native 10.34, against the
  rule's 10.82. At cluster mass the direct η corresponds to c_f ≈ 5, where X48's crossing estimator read about 7–11.
  The over-concentration read off the crossing (X74 pre-read P2, the 10-29 probes) was mostly an estimator artefact.

## Reported: the full grader with the native η (X74's script, c_f-equivalent table {6.75, 4.86, 5.03})
- **f★ 0.034, canonical: PASSES.**
  - SPARC rms 0.0687, Υ 0.52; groups Z +1.69.
  - All 15 cluster keys pass; the worst is G-IN-Mall −1.99.
- **f★ 0.0615, canonical: FAILS** on G-IN-Mall alone, at −2.04 (OVER, h 0.672). Everything else passes.
- **Alt:** the SPARC line fails (Υ 0.45), as in X70/X73 at every c_f.
- **Reading:** the halos our own cold collapse produces land on the boundary of what the data allow, at every mass, with
  nothing tuned. It is a knife edge, not a clean pass. The 1e13/1e14 inputs are still ng 48; A4 (ng 64) replaces them
  when it finishes.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. The zooms are collisionless cold
collapse of an isolated constrained peak. The floor physics is not in them; this tests the collapse branch only.
