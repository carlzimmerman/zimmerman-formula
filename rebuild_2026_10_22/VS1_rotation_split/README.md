# VS1_rotation_split: NOT SEPARATED, narrowly. Slow rotators sit 0.12 dex above fast ones with no mass trend, but all four are also the sample's four centrals, so rotation and environment can't be told apart

Criteria: `FROZEN_CRITERIA.md` (3c260609af), alone first, **not blind**. `vs1.py`, `vs1.out`, `vs1.json`, `vs1_MUTATE.out`. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Reinstates nothing.

| | D, need >= 0.15 | p, need < 0.05 | slow coefficient at fixed mass, need >= 0.10 at > 2 sigma | Cell |
|---|---|---|---|---|
| canonical | **+0.120, misses** | 0.002 | +0.127 +- 0.047 (2.68) | NOT SEPARATED |
| alt | **+0.117, misses** | 0.002 | +0.125 +- 0.047 (2.68) | NOT SEPARATED |

Mass slope with class in the fit: -0.012 +- 0.045. Mass-matched difference: +0.120, alt +0.105. Errors are scatter only, no shared systematic.

| Group | Offset, canonical | Offset, alt | n | Mean log M |
|---|---|---|---|---|
| Slow | +0.182 | +0.171 | 4 | 11.51 (JAM) |
| Fast | +0.062 | +0.053 | 12 | 10.93 (JAM) |
| SPARC discs, log M_b >= 10.7 | +0.012 +- 0.016 | -0.018 +- 0.016 | 36 | 11.04 (baryonic) |

## Read
- **Mass does not explain it in this sample**, which was the expected confound. My stated expectation of a mass-confounded difference did not come out.
- **Rotation can't claim it.** 4365, 4374, 4486, 5846 are all slow and all centrals. No slow non-central or fast central is labelled here, so the two explanations are the same split. Removing centrals leaves 0 slow rotators.
- **NGC 4649** is fast (lamRe 0.127), log M 11.65, offset +0.125, the same as M87's +0.131. One galaxy, against a clean rotation switch.
- **Fast rotators are not at 0**, +0.062, which the idea wanted.
- The disc arm has a different kernel and estimator, and lower mean mass, so it is a reported row, not a fixed-mass test.
- An offset is not a ZN4 halo. This doesn't test the halo's size or its failing shear keys.

## Older test's label bug
`argon_clues/rotator_test.py` maps names to digits, so NGC 4486A overwrites M87 as fast. Its old mapping gives n_slow 3 here, D +0.131. That file isn't edited. Its T-A sample, slow list 3608, 4365, 4374, 5846, omits M87 for the same reason.

MUTATE, labels shuffled within mass terciles: D reads +0.003, alt +0.004, so the statistic responds. The mutated label reads KILLED.
