# KQ1 AMENDMENT A1 (POST-FREEZE, after a partial first run, before the rerun)

Criteria 07534f282b. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

**What was seen.** The MUTATE twin ran (all KA PASS; M1, M2 bite; M3 holds). The first main run was stopped after 7 of
28 canonical grid rows (log kept unedited as `kq1_FIRSTRUN_preA1.out`). Those rows (mu_K 0.1-1.585 Mpc^-1) printed
r_1/2 658-3070 kpc, c 0.051-0.078, per-bin rms 0.25-0.47, all retained, and max |d ln rho / d ln r| inside 20 kpc
= 1.005 at every mu_K.

**The bug.** The record's solver (QX7 iter_5 `profile`) starts the integration with M_d = 0 at r_min. KQ1 derives rho from
dM/dr with np.gradient, whose one-sided first points then return a slope of -1.000 and -0.500 at the first two grid
points (a numerical edge, not physics: rho(r)/rho(r_min) is 0.997 at 0.16 kpc and 0.975 at 24 kpc for A1795 at mu 0.1).
It also inflates rho(0) by ~0.3 %. KA4 tested the calculators on an analytic grid and could not see it.

**Fix.** The line calculators (rho(0), r_1/2, L2 slope) use the solver grid from index 2 on (r >= ~0.1 kpc). Nothing
else changes: lines, grid, labels, amounts, KA1-KA4 and MUTATE definitions are as frozen. New KA5: on the solver's own
grid, the isolated Newtonian core (sinc) must give r_1/2 = 1.895494 / mu_K to 1e-3 and the max slope inside 20 kpc
= 1 - x cot x at x = 0.02 mu_K (Mpc) to 2e-3 (mu_K 5). Both runs (main and MUTATE) are repeated after this commit.

Kappa = 1/2 FITTED; not theory closed.
