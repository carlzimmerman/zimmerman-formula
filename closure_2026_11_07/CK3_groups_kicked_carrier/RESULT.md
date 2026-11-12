# CK3: groups under the kicked collisionless carrier. FAIL as frozen (slope), both footings, every kick; NOT ROBUST

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle beyond the record's carrier. Footings graded
separately, never pooled. The LCDM-like halo enters only as L388's reference normalisation (eps, R_c = 5.4) and XR13's
NFW placement, as frozen.

- Criteria: FROZEN_CRITERIA.md (753fc90cf4), committed alone before any script or number.
- Script: ck3.py. It execs se2.py read-only up to its main loop (writes redirected to a temp dir outside the repo) and
  UA1's groups-knob block read-only. One thread, about 12 s, peak RSS 0.90 GB.
- Outputs: ck3.json / ck3.out (KA1-KA3, per-group table, tests, labels, sensitivities) and ck3_MUTATE.out (flat
  retention).

## Labels (A = slope of eps vs log10 M500; B = UA1 class step with the carrier)

| v_k | canonical | alt |
|---|---|---|
| 550 (extrapolated from 575 / 600, not a run) | **FAIL** (A fails, 95 % of data - pred [-1.052, -0.001]; B passes) | **FAIL** (A [-1.050, -0.025]; B passes) |
| 575 | **FAIL** (A [-1.004, -0.024]; B passes) | **FAIL** (A [-1.001, -0.048]; B passes) |
| 600 | **FAIL** (A [-0.943, -0.067]; B passes) | **FAIL** (A [-0.938, -0.089]; B passes) |

Reported only: 625 and 650 also read FAIL on both footings, by the same test.

## The slope: prediction against need (eps per dex of M500)

| | predicted (L388 interpolated, bootstrap 68 %) | data need (UA1 joint posterior, per-group need, groups bootstrapped) |
|---|---|---|
| v_k 550 (not a run) | **+1.03 +- 0.28** | canonical **+0.21**, 68 % [+0.13, +0.33], 95 % [+0.04, +0.49] |
| v_k 575 | **+1.00 +- 0.25** | alt **+0.20**, 68 % [+0.12, +0.31], 95 % [+0.05, +0.45] |
| v_k 600 | **+0.92 +- 0.20** | (the data side does not depend on v_k) |

- In KD1's units (f = 5.4 eps of M_b) the data need f to rise by about 1.1 per dex of M500. The carrier predicts 4.9-5.5
  per dex.
- Against sigma_kT = sqrt(kT / 0.6 m_p) (reported only), the data slope is +0.71 / +0.67 per dex of sigma.
- **The data do want a rising f with group mass.** The slope is positive and its 95 % interval excludes 0 on both
  footings. But the rise is about one fifth of what L388's retention curve gives. The groups need a nearly level
  eps of about 0.3-0.4 (f about 1.6-2.2 of M_b) from 2e13 to 1.4e14. L388 gives 0 to 0.03 at the light end and 0.72-0.77 at
  the heavy end.
- **Level (B) passes everywhere.** With the carrier, the class step is +0.014 / +0.027 / +0.044 canonical and
  -0.021 / -0.007 / +0.009 alt at 550 / 575 / 600. Every 95 % interval contains 0, against UA1's +0.259 / +0.221 without
  it. The carrier's mean retention over the 20 groups (0.30-0.37) is about right. Its distribution over mass is not.
- Per group, eps_pred lies inside the group's need 95 % interval for 17-19 of 20 (canonical) and 20 of 20 (alt). The
  per-group intervals are wide. The slope across the groups is what separates the prediction from the need.

## Known answers and MUTATE

| Check | result |
|---|---|
| KA1 L388 bins from per-halo eps vs committed retention_by_mass (16 cells, 4 kicks x 4 bins) | difference 0, counts equal: PASS |
| KA2 eps = 0 vs UA1 post_groups2 | array_equal True, summary == ua1.json (+0.259 / +0.221): PASS both footings |
| KA3 XR13 placement: groups below 6e13 | 5 of 20 (XR13: 5): PASS |
| MUTATE flat retention (eps = group mean of the prediction, 0.37 / 0.33 / 0.30) | flat FAILS A on both footings at every kick (b_data 95 % excludes 0): **bites**, so the slope test has power. The flat model PASSES B (step +0.010 / +0.027 / +0.046 canonical, -0.026 / -0.009 / +0.010 alt) |

The flat MUTATE fails A, as required. On the level it does as well as the prediction, or slightly better. The data want
something between flat and L388's curve.

## Checking the fail as hard as a pass: it is NOT robust

1. **Thin margins.** The 95 % upper edge of (data - pred) is -0.001 (canonical 550), -0.024 / -0.067 (canonical
   575 / 600), and -0.025 / -0.048 / -0.089 (alt). Canonical 550 fails by 0.001.
2. **A units slip in the record, inherited by the frozen placement.** L388's masses are in Msun/h: L366, the source of
   its RHO_M, writes "Msun/h per (Mpc/h)^3", and L388's docstring says "1e14 Msun/h halos". XR13's m_1mpch returns Msun
   and compared them to L388's bin edges directly. The frozen primary copied XR13 verbatim, and KA3 reproduces XR13's
   count with the slip. The criteria pre-registered the unit-consistent reading (M1 x 0.6736) as reported only. Under it
   **every cell reads PASS, both footings**:
   - The A intervals are canonical [-0.938, +0.375] / [-0.820, +0.384] / [-0.688, +0.352] and alt about the same.
   - B is +0.066 / +0.083 / +0.106 canonical and +0.030 / +0.048 / +0.071 alt, every interval containing 0.
   - That PASS comes from **prediction error, not agreement**. The 0.17 dex shift puts 14 of 20 groups below L388's
     lowest node (11 below its lowest bin edge), where the prediction is the frozen linear extrapolation. So the
     bootstrap slope becomes broad and skewed: median +0.95 / +0.82 / +0.69, 68 % low edge +0.30 to +0.35. Its central
     value is still 3-4x the data's +0.20-0.21.
   - Even in the frozen placement, 11 of 20 groups lie below the lowest node: 5 below the bin edge, and 6 inside the
     lowest bin but below its median mass.
3. **Extrapolation rule.** Flat below the lowest node (XR13's upper-bound rule, reported only) gives predicted slope
   +0.50 / +0.53 / +0.55. That flips canonical 550 and 575 to PASS (A edges +0.033 / +0.002). Canonical 600 and every
   alt cell stay FAIL.
4. **Carrier convention.** With R_c = 5.36, canonical 550 flips to PASS and the rest stay FAIL. With the carrier taken
   as Newtonian-additive (no law boost, reported only), the data slope's 95 % interval contains 0 on both footings, so
   **NO POWER** in every cell.
5. **What holds in every variant.** The predicted slope's central value (+0.48 to +1.03 per dex) is 2.3-5x the data's
   (+0.15 to +0.21). The level closes the UA1 step. Whether the slope gap is a FAIL depends on the units, the
   extrapolation and the carrier convention, all at the margin.

**Reading.** Under the frozen rules the kicked carrier FAILS the groups' slope test at every kick on both footings, while
closing the class step. The FAIL is not robust: it rests on XR13's Msun-vs-Msun/h placement and on extrapolating
L388's retention below its lowest node for over half the groups. A run of L388-type boxes resolving 2e13-1e14 Msun/h
halos would decide it; no such run is on disk. The firm content is that the data need an almost level retention of
about 0.3-0.4 of the LCDM-like reference across the groups (rising about 0.2 per dex), while L388's curve rises
about 1 per dex and empties the lightest groups.

## Disclosed

1. **Amendment 1 (2026-11-07, post-freeze, before any graded number).** In the first run, `need()` crashed on an array
   shape: the IMF factor was per draw, (N, 1), not per point. It was broadcast to (N, 40), which does not change any
   value. Before the crash, that run had printed the prediction lines and KA1-KA3.
2. **Amendment 2 (2026-11-07, post-result).** The first full run peaked at 0.98-0.99 GB RSS, against the 1 GB line. SE2's
   own KA1 (the ST1 replay) is stubbed in the exec'd copy only (se2.py on disk is untouched), because the groups
   machinery does not use it. CK3's KA2 (array_equal with UA1) checks that machinery instead. Peak RSS is now 0.90 GB.
   No number changed.
3. **Amendment 3 (2026-11-07, post-result, output only).** The sensitivity print lines gained the predicted slope and
   the A / B intervals, and grade() records the paired predicted slope. No graded number or label changed between runs.
4. **v_k 550 is not a run.** It is a per-halo linear extrapolation from 575 / 600, clipped to [0, 1].
5. **L388 ran at canonical a0 only.** The same retention curve is used on both footings. Only the data side differs.
6. **The carrier follows the baryon profile** at R2500 and R500 (b_tot = b_IMF + 5.4 eps). Its real profile inside a
   group is CK1's question.
7. **The groups table has no member-galaxy sigma**, so "sigma" is graded through M500. The sigma_kT slope is reported
   only.
8. **Not blind.** UA1, SE2, KD1, L388 (bins and per-halo masses) and XR13 (i) were read before the freeze.
9. **The units slip (item 2 above)** is XR13's, in the record since September. It also affects XR13's (i) group placement
   and its "5 groups below the lowest bin". Correcting it is a record-level fix that this lane reports and does not
   make.

Kappa = 1/2 FITTED; not theory closed.
