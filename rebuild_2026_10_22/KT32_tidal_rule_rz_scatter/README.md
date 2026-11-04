# KT32_tidal_rule_rz_scatter: with mass-conserving scatter smoothing and ξ varying in (R, z), the tidal rule FAILS the Milky Way on both footings and both rules. Every check passes; K_z is the failing line (0 cells)

Criteria: `FROZEN_CRITERIA.md` (c8248fa630), alone first, confirmed landed. `kt32.py`, `kt32.out`, `kt32.json`, `kt32.time`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K846. 21 minutes, 0.72 GB peak. Per-cell checkpoints were deleted after the run.

ξ is KT31's field: each solver cell's own plain-QUMOND tidal tensor. Rules: F (KT28, Frobenius, 4/√3) and TF (KT30, trace-free, √6). Scatter: each source spreads its mass over a Gaussian of the width at the source. The ladder steps by a factor of 1.25 (50 widths). The smoother is a separable cylindrical I0 × Gaussian on a 700 × 320 mesh, with columns normalised. 1375 in-prior cells.

| | canonical F | canonical TF | alt F | alt TF |
|---|---|---|---|---|
| **label** | **FAILS MW** | **FAILS MW** | **FAILS MW** | **FAILS MW** |
| cells passing all four | 0 | 0 | 0 | 0 |
| L1 (v_c) / L2a / **L2b (K_z at R0)** / L3 | 230 / 502 / **0** / 64 | 199 / 474 / **0** / 41 | 516 / 278 / **0** / 382 | 463 / 241 / **0** / 332 |
| lowest K(R0) among cells with v_c in line (K_z line 66.4 ± 4.4) | 85.2 | 86.0 | 84.5 | 85.5 |
| best-D cell: v_c, K; same cell plain QUMOND K; Newton K | 215.6, 81.9; 77.5; 52.7 | 214.6, 82.2; 77.5; 52.7 | 213.0, 80.0; 76.9; 48.4 | 213.2, 80.9; 77.1; 48.8 |
| mass ratio, min / max | 0.9999 / 1.0001 | 0.9999 / 1.0001 | 0.9999 / 1.0001 | 1.0000 / 1.0001 |

## Reading
- **This is a clean fail, with no numerical escape.** Every check passes. Mass is conserved to 1e-4. The smoother matches exact `rho_xi` to ≤ 0.07 km/s at a ladder width and ≤ 0.26 km/s at a ladder midpoint (line 0.5). The grid Hessian matches KT29 to 1.02. R5 moves v_c and K by ≤ 0.2.
- **Conserving mass made K_z worse, not better.** KT31's gather run had a 12-44 % mass excess and gave a best-cell K of 77-80. Scatter gives 80-82, and the lowest K among cells with v_c in line is 84.5-86. Scatter is also above plain QUMOND for the same cell, by 3-4 units. Disc sources sit where ξ is small, so their phantom stays a thin disc: the vertical pull at R0 goes up while the outer rotation curve loses support.
- So once ξ varies inside the disc, the tidal rule does the opposite of what the filter needs. It sharpens the phantom disc instead of rounding it. KT17/KT25's global ξ ≈ 5-7 kpc passes because it rounds it.

## Where the tidal line stands (KT28-KT32)
| form | MW result |
|---|---|
| in-plane, one value (KT28) | alt passes, but only by dropping the vertical tide |
| full tensor, one value at the midplane (KT29); trace-free (KT30) | v_c fails, ξ 33-53 kpc |
| (R, z)-varying, gather (KT31) | K_z fails, with a mass excess (label NOT EVALUABLE) |
| (R, z)-varying, scatter (this lane) | K_z fails cleanly, 0 cells, both footings, both rules |

**No local tidal rule tested passes the Milky Way.** The only filter form that has passed the MW is the global system-scale length (KT17, KT25), which isn't a local rule. κ = 1/2 isn't derived by any of these lanes.

## Checks
R1 (ξ 0 = UX5 form Q, max rel 0), MUTATE (ν = 1, Q = N, 2.6e-13), N2 ([0.9, 1.1]: 1.021 / 1.023), S1 (all cells within 1e-4), S2, S3, R5: all pass on both footings. Failed checks: 0.
