# VS3_second_tracer: LEANS ROTATION, both footings, on two galaxies. NOT SETTLED: the lane could not return that label

Criteria: `FROZEN_CRITERIA.md` (fdc9c2f95f), alone first, **not blind**. `vs3.py`, `vs3.out`, `vs3.json`, `vs3_MUTATE.out`, `vs3_mass_check.out`. Offsets are CFG492's committed values. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Reinstates nothing.

PN offsets, canonical, primary window 500 kpc and 500 km/s. Contrast is against fast non-centrals, mean +0.013 +- 0.017 (NGC 3377, 4494, 4564).

| Galaxy | Class | log M | PN offset | Contrast |
|---|---|---|---|---|
| NGC 4374 | slow, non-central | 11.52 | +0.219 +- 0.020 | +0.205 +- 0.026 |
| NGC 3608 | slow, non-central, JAM quality 0 | 10.86 | +0.150 +- 0.049 | +0.137 +- 0.051 |
| NGC 5846 | slow, central | 11.47 | +0.165 +- 0.033 | +0.152 +- 0.037 |
| NGC 1023 | fast, central | 10.79 | +0.193 +- 0.020 | +0.180 +- 0.026 |
| NGC 821 | fast, central | 10.98 | +0.055 +- 0.032 | +0.042 +- 0.036 |

Pair mean +0.171 +- 0.031 canonical, +0.168 +- 0.031 alt; alt contrasts +0.201 and +0.135. The slow non-centrals match the slow central, which is what the rotation reading expects.

## Limits
- **Two objects, and the frozen statistic has no mass control.** NGC 4374 is far above the reference masses. Reported fit on all 8: slow +0.081 +- 0.077, mass +0.069 +- 0.096, corr(slow, mass) +0.73, so 8 galaxies can't separate them.
- **The cleanest pair is NGC 3608 and NGC 4494**, same mass, +0.150 against -0.013. NGC 3608 has the worst JAM quality. A rough +-0.1 dex in its mass moves its offset about 0.014 dex on the sample slope.
- **NGC 1023 is a counterexample:** a fast rotator at +0.193. It is a rotating S0 and this path doesn't remove rotation, which may inflate it; untested here. At the 1000 kpc window it joins the reference, and NGC 3608's contrast falls to +0.092 +- 0.067 (not graded).
- **Clip sensitivity:** at a 2.5 sigma clip NGC 3608's offset drops from +0.150 to +0.094 (reported in CFG492; not regraded). CFG492's PN-alone significance also fails leave-one-out.
- **MUTATE is weak.** The shuffled pairing returned UNDECIDED as required, but it leaves NGC 3608 and 4564 unchanged, since they are PN-only rows.
- Isotropic Jeans, with no anisotropy freedom in these rows. An offset is not a halo. No mechanism is tested.

## What settles it
Criteria need at least 4 slow non-centrals with an outer tracer and a JAM anchor. The disk has 2. NGC 4552 is the next one to look for; its catalogue availability is unchecked.
