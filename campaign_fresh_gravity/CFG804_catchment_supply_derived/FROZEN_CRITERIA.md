# CFG804 FROZEN CRITERIA: the catchment supply N derived from the record's own census, scored on KiDS lensing (committed before any script)

**The derivation.** No new inputs; everything is in the record.
- A galaxy's catchment holds M_b,catch = M_b,gal / f_ret(M_ta), where f_ret is the record's census retained fraction
  (CFG416 fret_of, as used in CFG556/646 and by T1x's M3).
- f_ret is 0.10 for log M_ta < 12.5, 0.10 + 0.45(lM − 12.5) up to 13.5, and min(0.55 + 0.30(lM − 13.5), 0.90) above.
- The catchment mass is M_ta = M_b,catch / f_b, with f_b = 1/(1 + 5.364). This is solved as a fixed point.
- **N = 1/f_ret(M_ta)**, and the cold supply is 5.364 N M_b,gal. The law holds out to the edge where
  M_c = 5.364 N M_b,gal (model D(N), CFG803).

**Test.**
- KiDS-1000 B21 Fig. 3, the CFG801/803 setup (full covariance; primary R ≤ 0.31 Mpc; all radii secondary).
- For each trial bin mass, N comes from the fixed point, so it is a function of M_b, not a parameter. M_b is profiled per
  bin exactly as in CFG801/803.
- Model **D_der** is compared with B (no edge).
- Report the derived N per bin at the best-fit masses, and the edge radius in r_M and kpc.

**Classes** (primary):
- **DERIVED SUPPLY SUFFICES** if Δχ²(D_der − B) ≤ 4.
- **FALLS SHORT** otherwise.

Also report the all-radii Δχ², where CFG803 found N_min = 16–24, and the census caveat.

**Controls.**
- K1: the fixed point for log M_b = 10.5 gives f_ret = 0.10 and N = 10 (log M_ta = 12.30 < 12.5).
- K2: B reproduces 83.9.
- MUTATE (separate outputs): f_ret := 1 (no missing baryons, N = 1) must reproduce the CFG801 edge failure (Δχ² ≈ +197).

**Caveat (stated).** The census f_ret = 0.10 at galaxy masses is an observational baryon-census input carried in the
record (CFG416). It was not fitted to KiDS here, but the framework does not derive it.

κ fitted; not theory closed.
