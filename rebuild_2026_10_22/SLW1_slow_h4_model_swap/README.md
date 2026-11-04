# SLW1: is the slow-rotator h4 pattern a JAM-model artefact?

Criteria `e6dae9e270` (post-hoc origin stated there; script committed before any run). kappa = 1/2 FITTED; not theory closed.

**LABEL: NO VERDICT (both footings).** M1 fails: h4 shuffled within cells among slow rotators gave E_slow
+0.160 [+0.012, +0.306] (canonical) under KU2's chosen model, an interval excluding 0.

## Why M1 failed (diagnostic, after the label, does not change it)
Not a code bug. 200 further shuffles (seed 7, chosen model, canonical) give mean +0.011, sd 0.092; |E| >= 0.16
in 15 of 200. The frozen shuffle was a 1.7 sigma draw, and the bootstrap interval of one realization
understates the statistic's real scatter: slow-rotator residuals have heavy tails (median +1.41, 99th
percentile +3.77 in ln). So the within-slow statistic has a noise sd of about 0.09 on 513 slow galaxies.

## Numbers (canonical; alt within 0.005)
| model | E_slow |
|---|---|
| cyl / sph mass-follows-light (HDU 2/3) | -0.037 / -0.019 |
| cyl / sph free NFW (4/5) | +0.078 / +0.077 |
| cyl / sph fixed NFW (6/7) | +0.182 / +0.177 |
| cyl / sph gNFW (8/9) | +0.053 / +0.097 |
| cyl / sph power law (10/11) | +0.079 / +0.047 |
| KU2's chosen model | +0.058 [-0.100, +0.265] |

Every one of the ten intervals includes 0. Delta_bar (cyl - sph) -0.005 [-0.036, +0.025]. Fast rotators
-0.03 to +0.05 under every model. Spearman(h4, fitted beta) among slow -0.13 to +0.02.

## Reading
- **The open thread is noise-sized.** LAM6-8's within-slow rows (+0.08 to +0.11) sit about 1 sigma from zero
  against the shuffle's sd of 0.09.
- **It is not an anisotropy effect**: cylindrical and spherical alignment give the same E (-0.005), and h4 does
  not track the fitted anisotropy.
- **What there is of it lives in the halo models**: it is absent with mass-follows-light (no halo) and largest
  for the fixed-NFW pair, the models KU2 found the data rarely prefer. That points at halo-fitting freedom in
  JAM, not at the law.
- Thread closed on MaNGA. KU2's UNIVERSAL is unaffected.

Files: `slw1.py`, `slw1.out/.json`, `slw1_MUTATE.out/.json`.
