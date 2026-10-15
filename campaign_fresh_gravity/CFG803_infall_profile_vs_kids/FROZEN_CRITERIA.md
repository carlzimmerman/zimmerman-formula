# CFG803 FROZEN CRITERIA: can the record's own cold infall (CFG748) supply the outer lensing mass that CFG801 found missing? (committed before any script)

**Context.** CFG801 (19e43e614): KiDS-1000 lensing excludes a settled halo that ends at 5.84 r_M, the point where
M_c = 5.364 M_b of the galaxy (Δχ² +197). CFG748 found that collisionless cold infall fills onto the law to within 0.4%
out to 20 r_M, and to 0.948 at 50 r_M (uniform start, late window). It assumed a supply equal to the law's mass within
R₀ = 200 r_M.

## Models (same data, covariance, ranges and M_b profiling as CFG801; canonical footing, alt reported)
- **A, edge:** CFG801's settled edge (reference).
- **B, no edge:** the law continued (reference).
- **C, infall-filled:** law × fill(r).
  - fill(r) is CFG748's uniform-start late-window table: 1.002, 0.994, 0.999, 0.991, 0.948 at 2, 5, 10, 20, 50 r_M,
    interpolated linearly in ln r; 1 inside 2 r_M.
  - Beyond 50 r_M fill is held at 0.948. This is declared, and affects the secondary range only.
- **D(N), catchment edge.** The law is truncated where M_c = 5.364 N M_b. Here N is the ratio of catchment baryons to the
  galaxy's own baryons; N = 1 is model A.
  - No fit of N. Report **N_min**: the smallest N on the grid 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64 with
    Δχ²(D − B) ≤ 4 in the primary range.

## Readings
- **C RESCUES** if Δχ²(C − B) ≤ 4 in the primary range. Otherwise **C FAILS**.
- **N_min** is the supply KiDS demands: the galaxy must draw cold energy from N_min times its own baryons.
- **Plausibility** (stated, not graded): galaxies are commonly found to hold only a fraction of the baryons in their
  surroundings (a "missing baryon" factor of a few to ~10). If N_min falls in that range, the supply rule survives once
  it is applied to the whole catchment. If N_min ≫ 10, the outer mass needs something new.
- C's own supply requirement (≈ the law's mass within 200 r_M, i.e. N ≈ 37) is reported against the same scale.

## Controls
- K1: model B reproduces CFG801's primary χ² (83.9) within 0.1.
- K2: D(N = 1) reproduces CFG801's edge χ² (280.9) within 1.
- MUTATE (separate outputs): fill set to 0 beyond 5.84 r_M must reproduce model A's Δχ² (C FAILS).

κ fitted; not theory closed. Provisional bin masses as in CFG801.
