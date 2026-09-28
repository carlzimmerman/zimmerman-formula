# CFG14 — the kernel-shape estimator, calibrated

Script: `CFG14_shape_calibration.py`, about 45 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. With the noise off, the P2-truth distribution collapses onto β = 1 and H1 fails (rc = 1).
- The main run exits 1, because H1 failed.

## The question

CFG4 H3 fits the transition sharpness β of ν_β = (1 + y^−β)^{1/2β} to all of SPARC. It finds β̂ = 0.48 (canonical) and 0.55 (alt), and reports P2's β = 1 outside the galaxy-bootstrap 95% band in 1000 of 1000 resamples.

The calibrated question is where the real β̂ falls in the distribution that β̂ takes when the truth is P2, and when it is ν_mono.

## The method

**Estimator.** CFG4 H3's point estimate exactly: the 49-point β grid, one global Υ profiled, the record's weights.

**Truths.** Each kernel at its CFG4 best Υ.

**Noise.** Two declared models, 60 realizations each:

| model | galaxy level | point level |
|---|---|---|
| A | offset N(0, 0.08 dex) on g_obs | SPARC's own velocity errors |
| B | stellar-Υ scatter N(0, 0.10 dex) in the truth's g_bar, plus a distance offset N(0, 0.08 dex) | the same point errors |

## Results

**Controls**

| check | result |
|---|---|
| C1: the real β̂ and Υ reproduce CFG4 H3 | 0.4847 @ 0.44, 0.5533 @ 0.46: pass |
| C2: noiseless P2 returns β = 1.004 and its own Υ | pass. Noiseless ν_mono maps to β̂ = 0.553 |

**The calibration**

| footing, model | P2 truth: median, central 95% | real β̂ | p (two-sided) | ν_mono truth: central 95%, p |
|---|---|---|---|---|
| canonical, A | 1.004, [0.65, 1.71] | 0.485 | **0.033** | [0.41, 1.00], 0.60 |
| canonical, B | 1.004, [0.55, 1.77] | 0.485 | **0.033** | [0.40, 0.98], 0.57 |
| alt, A | 1.004, [0.59, 1.82] | 0.553 | **0.033** | [0.41, 1.11], 1.00 |
| alt, B | 1.004, [0.52, 1.96] | 0.553 | 0.133 | [0.40, 1.11], 0.97 |

**H1** (P2 not excluded after calibration, both models, both footings): **FAILED** on three of four rows.
**H2** (ν_mono not excluded): **pass**.

**CFG13's subsets under the same calibration (model A)**

| subset | real β̂ | inside P2's distribution? | inside ν_mono's distribution? |
|---|---|---|---|
| point-mass | 0.72 / 0.88 | yes | yes |
| embedded, canonical | 0.48 | no | yes |

The point-mass points cannot tell the two kernels apart. The preference comes from the points inside the baryons.

## What changes

1. **CFG4 H3's "P2 outside the 95% band" overstated the exclusion.** The galaxy bootstrap under-covers β̂'s sampling spread by about 5×. The calibrated statement is that P2, applied everywhere, is **disfavoured at p ≈ 0.03 (about 2σ)** on the canonical footing, and at p ≈ 0.03–0.13 on alt. **ν_mono**, the contract kernel, **is fully consistent.**
2. **CFG13's "the estimator is biased low by ~0.4" is withdrawn.** It was one low draw from a wide distribution. The estimator is median-unbiased. What failed in CFG13's C3 is the bootstrap's coverage, not the estimator.
3. **CFG9's principle stands where it applies.** Around point masses, P2 follows from local virial equilibrium, and SPARC's point-mass-regime points do not exclude it. The mild preference for a smoother kernel comes from inside the baryons, which is the inner law CFG10 addresses.

Nothing here says the theory is closed.
