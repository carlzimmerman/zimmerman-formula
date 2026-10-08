# CFG431: is the settling clock's scatter universal? (the galaxy point added to T14)

Criteria: `FROZEN_CRITERIA.md` (26d94268c, committed alone before the script). Script: `cfg431_clock_universality.py`.

**Verdict: NOT UNIVERSAL, and FRAGILE.** Read on the correct branch with real scatter, groups and clusters do not share one clock
scatter: 2.31 against 0.19, a 2.2σ difference. The failing pair is groups against clusters, which is T14's own pair. The new galaxy
point (0.72) sits between them and is within 2σ of both. The result depends on the hydrostatic bias. At b = 0.1 the median group
value is above 1, so no group clock exists, and the verdict becomes CONSISTENT, NOT DIAGNOSTIC. T14's "one halo clock"
(0.468 / 0.409) is not reproduced.

## What was done
- **Branch.** All three scales use the same measured quantity: definition A, the beyond-law cold mass per cosmic cold share.
  CFG382 calibrates e = exp(−Γt) directly against this quantity, so it is the leftover e, not the settled f.
- **Identity on that branch.** σ(e)/e = |ln e|·σ(ln t), which gives S = σ_e/(e_med·|ln e_med|).
- **Scatter.** S uses the measured population scatter (half the 16–84% range). The tolerance comes from a bootstrap over objects.
- **Two problems with T14's inputs, found while reading.**
  - Its ±0.15 is CFG382's declared tolerance band, not a measured scatter.
  - Its group 0.60 (definition B, lensing bias) and cluster 0.43 (definition A) use different definitions.

## Key numbers (primary row: definition A, b = 0, canonical a0)

| scale | sample | e_med | σ_e | S = σ(ln t) | δ(ln S) |
|---|---|---|---|---|---|
| galaxy | 23 non-central SLUGGS early types (the cm08 "0.13" cell) | 0.131 | 0.193 | 0.72 | 0.28 |
| group | 20 Lovisari groups, R500 | 0.787 | 0.436 | 2.31 | 0.63 |
| cluster | 7 X-COP clusters, R500 | 0.413 | 0.069 | 0.19 | 0.94 |

- **Pairwise z.** cluster–galaxy 1.37, cluster–group **2.22**, galaxy–group 1.70.
- **T14's own inputs re-read on the e branch.** Clusters 0.413 and groups 0.489, against 0.468 / 0.409 on T14's f branch. These are
  reported only, because the ±0.15 behind them is a tolerance, not a scatter.

## Robustness rows (reported)
- **R1, alt footing.** The pattern is unchanged: galaxy S 0.74, cluster–group z 2.22.
- **R2, X-COP gas mass at R500.** The target audit takes the gas mass at 1 Mpc while M_HSE is at R500; this row uses R500 for
  both. Cluster e_med falls to 0.225 and S to 0.13; cluster–group z is 2.35.
- **R3, b = 0.1.** The group median e is 1.04, so the group clock is undefined. Galaxy against cluster gives z 1.18, which is
  CONSISTENT, NOT DIAGNOSTIC. This row is why the verdict is labelled FRAGILE.
- **R4, measurement noise subtracted (Monte Carlo of the per-object input errors).**
  - The intrinsic S values are 0.60 (galaxy), 1.30 (group) and 0.15 (cluster).
  - Noise is most of the group scatter: 0.36 of 0.44.
  - The ordering cluster < galaxy < group stays the same.
- **Exact per-object map, ln t_i = ln(−ln e_i).** The robust scatter is 0.49 (galaxy, 18 of 23 kept), 0.77 (group, 15 of 20)
  and 0.20 (cluster, 7 of 7). Objects with e outside (0, 1) are dropped.

## Controls
- **C1 (identity) and C2 (reproduction) pass.** C2 recovers cm08's 0.13 from the 23 non-centrals and the audit's 0.787 / 0.413.
  It also recovers T14's 0.468 / 0.409 and gives 0.413 / 0.489 on the e branch.
- **MUTATE** injects a ×4 clock break into the galaxy scatter. S_gal becomes 2.89 and cluster–galaxy z becomes 2.40, so the
  break is detected. C3 fails as declared. The test therefore has enough power to see a ×4 break at the galaxy point.
- **Disclosed check-code fix (before any reading).** The first run's C1 had an algebra slip (a stray factor f/e in the T14
  comparison), and C1 failed. It was fixed, and both runs were redone. No result number changed, because the bootstrap is
  seeded.

## Caveats
- **S is total scatter.** It includes noise and the Γ differences between objects, so it is an upper bound on the intrinsic
  formation-time scatter.
- **N is small.** Seven clusters give δ(ln S) 0.94. Every pairwise z is within a factor of about 1.2 of the threshold.
- **The kernels differ, as on disk.** The galaxies use √(1+1/y) (cm08); groups and clusters use nu_mono (the audit).
- **The group stellar mass is a placeholder** (0.10 M_gas, as in the audit).
- **The galaxy apertures (5 Re) are not R500.**
- **The branch reading is not settled.** T15 labels the definition-A values as "deficit x = M_missing/M_b". The formula is
  normalised by 5.364 M_b, so here they are read as CFG382 reads them, as e. If T15's labelling is the right one, no clock
  reading of these numbers exists.
- **What would settle the bias question.** Group masses calibrated by lensing would decide the group level, and with it the
  verdict.
- κ = ½ is fitted. The cold mass is still required.
