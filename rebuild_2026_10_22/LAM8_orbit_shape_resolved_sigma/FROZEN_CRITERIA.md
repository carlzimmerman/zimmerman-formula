# LAM8 FROZEN CRITERIA: LAM7's test restricted to resolved dispersions (Sigma_Re >= 100 km/s)

Frozen before any LAM7 or LAM8 effect E has been computed. kappa = 1/2 FITTED; footings never pooled; not theory closed.

## Why, and what was seen first (full disclosure)
LAM7 (criteria f10b6db28c) fails K1 on the full NEW sample: median log(sigma_int/Sigma_Re) -0.008, rms 0.086
(bar 0.06), so LAM7 is NO VERDICT by its own rules. Before any residual was joined, K1 was broken down by
Sigma_Re: [0,70) rms 0.218, [70,100) 0.075, [100,150) 0.040, [150,inf) 0.030. Below about 100 km/s the
dispersion is at or under MaNGA's instrumental resolution and integrated sigma (and h4) are not trustworthy.
Sigma_Re >= 100 km/s is the cut LAM2 and LAM4 already used (velDisp >= 100). The cut was chosen from K1 only.
A grader crash (ku2.json D lookup; fixed in the same commit as this file) stopped LAM7's MUTATE before any E.

## Definition
Everything in LAM7's criteria, unchanged, with one cut: NEW-sample galaxies with KU2's Sigma_Re >= 100 km/s
(3144 galaxies, 148 slow). Same statistic, groups, bootstrap, labels (TRACKS ORBIT SHAPE / NO ORBIT
DEPENDENCE / NO VERDICT, bar 0.05 ln), C1 N in groups >= 3000, C2, K1 on the cut sample, M1 MUTATE.
K2: LAM7's K2 run (200 synthetics over all NEW sums, all sigma) is used as is; it includes the harder
low-sigma cases, so it is conservative for this cut.
Run: `python3 -I ../LAM7_orbit_shape_full_sample/lam7_grade.py [MUTATE] --sig100`; outputs here as lam8_grade*.

## Note on power
Only 148 slow galaxies remain, so the within-slow row will be weak; the graded E pools within-class slopes
as in LAM6/LAM7.
