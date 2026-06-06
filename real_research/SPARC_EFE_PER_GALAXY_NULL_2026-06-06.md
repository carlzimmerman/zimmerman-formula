# The clinching in-house EFE test is a NULL — honest result, and it weakens the prior in-house read

*C. Zimmerman, 2026-06-06. I built the per-galaxy External-Field-Effect test the prior in-house script said it
"couldn't do for lack of per-galaxy g_ext" — using the environment table now in the repo (2MRS/2M++ overdensities, host
halo mass). Result: a clean NULL. No spin: it does not confirm the EFE, and it weakens the prior script's "downturn =
EFE" read. Script: `sparc_efe_per_galaxy_environment.py`.*

## The test and the prediction
The EFE (the one ΛCDM-impossible MOND signal) predicts: galaxies in **denser environments** (stronger external field)
should sit **more below** the RAR at low g_bar (their internal MOND boost is suppressed), with **no** such trend at high
g_bar. Outer-kinematic systematics (warps, beam smearing) don't know about the cosmic web, so a correlation with
environment — vanishing in the Newtonian control — would isolate the EFE. I computed the per-galaxy mean RAR residual in
three g_bar bins and correlated it with the environmental field proxies.

## The result — null

| regime | proxy | N | Spearman r | p | EFE predicts |
|---|---|---|---|---|---|
| **EFE-sensitive** g_bar<3e-11 | 2MRS overdensity | 103 | **+0.11** | 0.26 | negative |
| EFE-sensitive | 2M++ overdensity | 103 | −0.03 | 0.78 | negative |
| EFE-sensitive | host halo mass | 103 | +0.14 | 0.16 | negative |
| transition | 2MRS | 48 | −0.01 | 0.96 | ~0 ✓ control |
| Newtonian (control) | 2MRS | 17 | +0.01 | 0.96 | ~0 ✓ control |

**No significant correlation in any channel**, and where there's a hint it's the *wrong sign* (positive, while the EFE
predicts negative). The controls are correctly null. So **the in-house data do not detect the EFE.**

## Honest reading (no spin)
1. **This weakens the prior in-house claim.** The earlier `sparc_efe_test.py` found an outer-RAR "downturn" and called
   it "consistent with the EFE." But that downturn does **not** correlate with environment here — which is exactly the
   signature that would distinguish EFE from outer-kinematic systematics. So in-house, the downturn is **more likely
   partly kinematic** (warps/beam-smearing at the outermost points) than EFE. I'm correcting an over-optimistic read.
2. **It does NOT contradict the published EFE detection.** Chae et al. 2020/2021 detected the EFE at ~4–5σ — but using
   a *proper* external-field estimate (the actual gravitational field summed over the environment) and a full per-galaxy
   rotation-curve fit. My test uses a crude **overdensity proxy** (2MRS/2M++ `1+δ`) and a mean-residual statistic — far
   less powerful. The null is consistent with (a) the proxy being too noisy, (b) SPARC being selected for *isolated*
   clean-RC galaxies (little EFE dynamic range), and/or (c) the downturn being kinematic. It is **not** a refutation of
   the EFE.
3. **Net:** the framework's foundation signal (the EFE) rests on Chae's careful analysis, **not** on anything I can
   reproduce from this repo's data. The honest status: in-house, **unconfirmed**.

## The forward step (what would actually clinch it)
Get the **proper per-galaxy external field** — either Chae et al.'s published `e_N` values, or compute g_ext directly
(sum the gravitational acceleration from 2M++/2MRS galaxies around each SPARC target, with mass weighting and distances;
the overdensity alone is not enough). Then redo this correlation. That is the concrete way to independently confirm or
kill the EFE — and it's the right next move, because the EFE (modified inertia/gravity, no dark matter) is the one
signal that decides whether the framework's whole premise is right. Until then, in-house: **null, honestly.**

*Sources: SPARC [Lelli+2016]; EFE detection [Chae et al. 2020, 2009.11525; 2021]; the environment table is the repo's
2MRS/2M++ overdensity + host-halo compilation.*
