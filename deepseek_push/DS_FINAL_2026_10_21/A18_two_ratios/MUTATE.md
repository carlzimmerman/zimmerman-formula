# A18 — mutations

Two mutations, both realistic bookkeeping slips, both invoked by a flag and both recorded as
captured stdout next to the main run. Each must break at least one declared check; both exit 1.

    python3 a18_checks.py            -> a18.out,            a18_results.json            exit 0
    python3 a18_checks.py --mutate   -> a18_MUTATE.out,     a18_results_MUTATE.json     exit 1
    python3 a18_checks.py --mutate2  -> a18_MUTATE2.out,    a18_results_MUTATE2.json    exit 1

## M1 — the denominator slip (the lane's central error)

`n_supply()` returns `R_cosmic` instead of `R_cosmic/f_ret`: the catchment is identified with the
system, i.e. `f_ret = 1`. This is exactly the mistake the lane exists to refute — comparing 5.364
to the law's ratio as if both were per unit of the *same* baryon mass.

Breaks **K10, K11, K12** (17/20):

    K10 FAIL MW 4.6684 / cl 0.4880 0.467 / 0.440 +-0.01
    K11 FAIL u in [0.543,6.114] [0.35,0.75], max/min<2.0
    K12 FAIL M_b=nan 1e9..3e9
    A18 COMPLETE: 17/20 checks PASS.

The MW sourcing fraction becomes `u = 25.043/5.364 = 4.668`, i.e. the framework would need 4.7×
more cold energy than the entire catchment contains — the slip is self-evidently fatal once the
denominator is written down. K12 has no crossing at all (`u` never reaches 1 over `1e8–1e12`), so
the check reports `nan` rather than crashing; that branch is the mutation's signature.

## M2 — the amplitude slip

`lambda_req` is set to `A_law` (1.9102) instead of `A_law(A_newton−1)/(A_newton−A_law)` (2.1207):
the ΔΣ amplitude `A`, which multiplies the **total** signal, is read as the rescaling `λ` of the
**phantom** alone.

Breaks **K14** (19/20):

    K14 FAIL lambda/A=1.0000 1.05<.<1.20
    A18 COMPLETE: 19/20 checks PASS.

The downstream numbers move the way the slip predicts: `R_req` falls from 5.552 to 5.001 and
`dev_cosmic_sigma` rises from 0.44 to 0.85. K15 still passes, which is itself informative — the
sloppy inversion lands inside 1σ of the cosmic ratio and 5.6σ from the law. **The discrimination in
this lane is carried by the exclusion of 1.0 (7.7σ), not by the precision of the inversion.**

## What the mutations are not

Neither mutation touches the symbolic identities (K1–K4), the A11 anchors (K5–K6), the crossing
mass (K7–K9) or the discriminator (K17–K18). Those are structural: they cannot be broken by a
parameter slip, only by a different law or different data. The mutations therefore test the two
places where this lane could actually be wrong — the budget denominator and the amplitude algebra.
