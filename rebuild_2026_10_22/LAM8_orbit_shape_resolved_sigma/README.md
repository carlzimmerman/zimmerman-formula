# LAM8: the orbit-shape test at resolved dispersions (Sigma_Re >= 100 km/s)

Criteria `b9b94ead6d` (frozen from LAM7's K1 breakdown, before any E). kappa = 1/2 FITTED; not theory closed.

**LABEL: h4 NOT MEASURABLE (both footings).** K2, frozen as LAM7's all-sigma run, fails: rms 0.038 vs 0.03.
K1 passes on the cut (median +0.009, rms 0.035); C1 3114 in groups; C2 exact; M1 passes (canonical marginal).

| | canonical | alt |
|---|---|---|
| E (ln), 3144 galaxies, 148 slow | -0.011 [-0.035, +0.012] | -0.006 [-0.029, +0.018] |
| M1 shuffle | +0.019 [-0.000, +0.039] | -0.004 [-0.022, +0.013] |

## Reading, with the label as it stands
No label is earned, because K2 fails. As numbers only: on 3144 new galaxies the interval sits inside +-0.05
on both footings and centres near zero, and the full 5056 (LAM7) do the same. LAM6's +0.04 lean on LAM4's
1000 is not seen in the new galaxies. KU2's UNIVERSAL is neither strengthened nor weakened by a graded result.

Ungraded rows, the same sign in LAM6, LAM7 and LAM8: within slow rotators the residual rises with h4
(+0.077 / +0.074 here, +0.11 in LAM7, +0.088 in LAM6) while within fast rotators it is about zero. With 148
slow galaxies, this is a pattern, not a result; the obvious reading is JAM's axisymmetric anisotropy model
misfitting radial-orbit slow rotators, not the law.

K2 was frozen to the all-sigma run and was said to be conservative; it failed. A K2 restricted to Sigma_Re >= 100
would be a post-result diagnostic and could not change this label.
Files: `lam8_grade.out/.json`, `lam8_grade_MUTATE.out/.json` (run by `../LAM7_orbit_shape_full_sample/lam7_grade.py --sig100`).
