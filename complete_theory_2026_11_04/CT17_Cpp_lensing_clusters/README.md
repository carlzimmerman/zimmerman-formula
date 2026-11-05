# CT17: G7 lensing and clusters for C''. C'' INHERITS v3s's rows exactly; all three FAIL

Under D1's follow-up ("Yes, grade it") and `../CT_GATES_COMMON.md`. Grading only: nothing adopted, the 2026-11-01 retirement stands, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Criteria `FROZEN_CRITERIA.md` (written first, not blind). `ct17_rows.py` -> `ct17_rows.out` (arithmetic on record numbers, one thread, < 1 s, < 0.1 GB).

## Step 1: what v3s / AeST-type dust predicted
- v3s's static dust phase is the mu_K^2 psi term, `div[mu grad psi] + mu_K^2 psi = 4 pi G rho_b`, lensing sees psi (V3_FULL_PICTURE.md:47), with mu_K < 0.1 Mpc^-1 from isolated-galaxy lensing (V3_FULL_PICTURE.md:41). This is H2's AeST quasi-static system: hydrostatic dust delta rho = mu^2|Phi|/4 pi G, amount set by a free zero point Delta.
- At mu 0.1 it adds 0-2 % inside 1 Mpc, 0.3 % at 200 kpc in galaxies, for every Delta in [-8, 2]; no (mu, Delta) passes (H2 h2_aest_clusters.out:19-20, 51; README "CANNOT").
- Why v3s failed: one field carries the law (alpha = 1), so it cannot be weightless in galaxies and weigh in clusters (V3S_FINAL_VERDICT:55); at galaxy-allowed mu_K the khronon is radiation-like, sigma8 0.003-0.005 of dust (V3_FULL_PICTURE.md:108), so a fitted cosmic amount does not settle in wells.

## Step 2: does C'' change anything?
Local a0 shift in a 1e14 Msun cluster 9.97e-11 / 7.78e-11 dex (CT13 out:23, 27) -> mass shift <= 5e-11 dex; phi's perturbation inside R500 <= 2.6e-9 dex (ct17_rows.out:1, 4). The dust equation is v3s's. C'' inherits v3s's rows exactly.

## Step 3: grades (ct17_rows.out)
| row | need (CT4) | C'' | grade |
|---|---|---|---|
| X-COP | x2.93 / x2.72 | x1.00-1.02; M_HSE/M 2.88-2.93 / 2.67-2.72 | FAIL, +0.46 / +0.43 dex |
| Bullet | peaks on galaxies (~200 kpc) | on the gas, 40 / 51 kpc, dkappa -0.068 / -0.111 | FAIL, wrong sign |
| KiDS R <= 0.3 Mpc | +0.089 to +0.116 dex, red x1.31 / x1.20 | +0.0013 dex, colour-blind | FAIL, +0.088 to +0.115 dex |

Hand-set: kappa (FITTED), mu_K (bound only, taken at its top), Delta (scanned in H2, free), dust amount (fitted, G5), plus C'''s xi, V0, V shape, phi_i, L*.
