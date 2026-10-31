# OP1_one_profile_dwarfs: FROZEN CRITERIA

Committed alone, before any script or number from this lane. κ = ½ FITTED. Cold dark energy, never a particle. Not theory closed. Nothing here will say the data favour the framework.

## Question
ZN2 A1 (another session's read, seen before this was written): the native z = 0 profile, no S, r₀ or a₀, passes SPARC and groups on FC1's normalisation and fails on its frozen mapping. ZN3: it passes clusters on X-COP's gas scale. Does the same profile hold the Local Group dwarfs, where the S rule fails? Written after SN1 and after seeing that read, so this is not blind.

## Halo
M(<r) = M · m(r/R), m = `ZN2_native_profile_sparc_groups/zn2_low_shapes.json`, z = 0, 10¹⁰ tag, clamped below it, M ∝ r² below the stored grid, as zn2_def. Two mappings, as zn2_def: **FC1** (M = M200, R from M200) and **frozen** (M = M200, R from M200 / f_c). X49's data path, classes, E, s, bootstrap, |Z| < 2, from SN1.

## Frozen verdicts (both mappings; both footings, differing = UNDECIDED)
**P1, EM1's M200.** **PROFILE HOLDS** if all five classes |Z| < 2; otherwise list failures. This has no fitted number.
**P2, free line** lg M200 = a + b (lg M★ − 7), a 6–12, b −0.6 to 2, step 0.05. **LINE ADMITTED** if any line passes; report count, and **MEETS EM1** if any passes within ± 0.3 dex of EM1's line at lg M★ 8 (where SPARC's dwarfs sit). Otherwise **NO LINE**. A line is a fit: two numbers.
**P3, resolution flag.** For each class, the share of systems with r₁₂ inside 3ε at the M200 used, ε scaled from the 10¹⁰ tag (714 pc at lg 10, ∝ M^(1/3)). A class with share > 50 % is flagged [CONTINUATION]: its pass or fail is not a measurement.

## Reported, no verdict
Draco and J0946 at 0.3, 0.6 kpc: bound R. Shape with the measured trend of lg m with lg M carried below the tag (bracket, not a measurement). The 1e12 tag's shape.

## Zooms (Amendment-free follow-up, frozen here)
1e9 and 1e8, seeds 1–9, ng 64, X48's zoom with ZK1's kernel to z_f, ZN1's continuation to z = 0, single thread, nice 15, --resume, SIGTERM exits 75. They start only after the live ng 80 batch has finished. Read: rerun P1, P2 with 1e8, 1e9, 1e10 tags interpolated, same labels. Fewer than 6 finished at a mass = UNDECIDED at that mass. Also report: c₂₀₀ and M/r² at 3ε against the trend from 10¹⁰ to 10¹², **SELF-SIMILAR** if within 20 % of the trend's value, **BREAKS** otherwise.

## Limits stated in advance
No baryons, tides or stripping. EM1's line has no scatter. Scale mapping differs across scales (ZN3 needs M200 fair share within R200; FC1's normalisation uses EM1's M200), so one profile is not yet one rule; stated in any summary. Even a dwarf pass here doesn't address HS1's tilt, MW, SLUGGS, HG2.

## Checks
K1 m(x) at tags reproduces zn2_low_shapes interpolation. K2 E path with shape = smooth-core m reproduces SN1 at S 29.4, |d| < 0.005. MUTATE r × 1.5 in separate output, must move E.
