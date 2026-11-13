# SRJ1: commit ids, the lead's re-run and one reader note (dated addition, 2026-11-12)

No number, word or line of the lane changes. RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | f21be18fd6 | 47f774eb94 |
| Script and outputs | 46e480051f | 57eb529b88 |
| RESULT | 4aecfde9a3 | 64d631ac0b |

## Re-run by the lead

`srj1.py` from a copy, one thread, then `--twin newton` and `--twin f0`. The three JSON files equal the committed ones
once the elapsed-seconds and peak-memory lines are removed; the three `.out` files equal them apart from elapsed-time
stamps. The main run exits 0; both twins exit 1. Word reproduces: JOINT FAILS ON CLUSTERS, FRAGILE (R500 aperture) on
both footings. A reproduction of the arithmetic, not an independent re-grade.

## Reader note (the lead's reading of two committed outputs; not graded here)

Two committed outputs point at the same ingredient:

- this lane: the law's layout inside R_set in cluster-regime systems is too light in the core for X-COP's measured
  shape (+0.153 / +0.144 dex in the inner bin against a line of 0.10), while the reference layout passes the same gate
  (-0.007);
- FZS1's diagnostic (`closure_2026_11_10/FZS1_forest_settled_radius/fzs1_diag.out`): under the settled rule the
  galaxy-regime haloes leave the halo profile's power unchanged (U_S / U_R 1.0000 to 1.0028 at k 3 and 10 for 1e10 to
  1e12 Msun/h), and the whole of its forest miss (38.7 / 36.7) comes from the cluster-regime haloes (0.9909 / 0.8043 at
  1e13 Msun/h), that is, from the same layout this lane finds failing on X-COP.

So the cluster data and the forest's remaining miss both turn on how cold dark energy is laid out above the v_stiff
boundary. A joint that keeps the reference layout there, and the law's layout only inside the fold radius of
galaxy-regime haloes, has not been graded on the forest or on lensing. That is a further post hoc step and is stated
here only as the question this lane's result raises.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
