# EB1b_web_efe: FROZEN CRITERIA, written AFTER EB1's result (post-result follow-up, disclosed), before any EB1b number

**Why this lane exists.** EB1 (criteria 7ac6bbb3f9, A1 77f1c1ba5f) found: R0 forms nothing by z 0; R1 with an
isolated sphere (e = 0) collapses baryon clumps bottom-up (1e6 Msun at z 11.3-12.4, 1e8 at z 7.0-7.9), nearly
independent of peak height and A_s, so QSO1's primary cells read EASY; but with any frozen external field e = 0.03
or 0.1 nothing collapses by z 0. The verdict therefore hangs on the external field at z 10-50, which EB1 bracketed
but did not measure. WG2's own law-on box already measured it: snapshot percentiles of y = |g_N| / a0 (Newtonian
peculiar field, physical) in R1_TIE_B2_As2.1e-09_N128_s200_zon50_{canonical,alt}.json, e.g. median 0.0177 at z 50,
0.0050 at z 10 (canonical). EB1b uses that field. Not blind: EB1's numbers are known.

Kappa = 1/2 FITTED. Not theory closed. Conditional on R1, which fails the CMB-lensing shape (WG2-WG6).

## Method (EB1's, one change)
- e(z) = WG2's snapshot y percentile for the same footing, interpolated linearly in ln(1 + z) between snapshots
  (held at the z 50 value before z 50 is irrelevant: z_on = 50). Three readings: p05, median (primary), p95.
- Everything else as EB1's primary cell: B2, A_s 2.1e-9, z_on 50, TIE, scalar EFE nu((|g_N| + e a0) / a0), masses
  1e6-1e13, nu_pk 1-5, gate G1 with eps 0.1 / 0.2, M_seed 1e2-1e6, M_clump = 10 M_seed, QSO1 log M 6.9 / 7.6 / 7.7.
- Labels as EB1's G1. Primary cell: median e(z), eps 0.1, M_seed 1e5, log M 7.7 and 6.9, both footings.

## Limits stated now
- WG2's mesh is 12.5 h^-1 Mpc; field from smaller scales (down to the Silk scale) is missing, so e(z) is a lower
  bound on the ambient field. A lower e favours collapse; a NO here is robust to that, an EASY is not.
- WG2's field is from R1's own run, so it already includes the law's boost on large scales.

## Checks
- **K5** with e(z) set to 0 the code reproduces EB1's primary R1 canonical z_coll table to 1e-6.
- **K6** with e(z) set to 0.03 it reproduces EB1's e0.03 cell (no collapse anywhere).
- **MUTATE** (EB1b_MUTATE=1): e(z) multiplied by 0; K-check K7 "median and zero-field tables differ" must FAIL.
