# LAM7: LAM6's orbit-shape test on KU2's full sample (5056 new galaxies)

Criteria `f10b6db28c`. kappa = 1/2 FITTED; footings never pooled; not theory closed.

**LABEL: NO VERDICT (both footings).** K1 fails (rms 0.086 vs 0.06) and K2 fails (h4 rms 0.038 vs 0.03).

5056 of 5056 cubes summed and fitted (0 errors). C1 (5000 in groups) and C2 (KU2 D exact) pass; M1 passes.

| | canonical | alt |
|---|---|---|
| E (ln), graded sample, checks failed | -0.006 [-0.020, +0.010] | -0.002 [-0.018, +0.014] |
| M1 shuffle | -0.010 [-0.024, +0.003] | -0.001 [-0.014, +0.013] |

K1 fails below Sigma_Re ~ 100 km/s (instrumental resolution); see LAM8, which was frozen from K1 alone before any
E. A grader crash (ku2.json D lookup) before any E was fixed in b9b94ead6d. Ungraded rows: combined with LAM4's
1000 -0.001 / +0.003; within slow +0.110 / +0.108; within fast -0.006 / -0.003.
Files: `lam7_stream.py`, `lam7_fit.py`, `lam7_grade.py`, `lam7_sample.csv`, `lam7_fit.jsonl`, `lam7_k2.*`, `lam7_grade*.*`.
