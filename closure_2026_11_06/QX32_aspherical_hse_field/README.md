# QX32 (door C): asphericity bias of spherical hydrostatic masses in the law's own QUMOND field. NEGLIGIBLE (<= 0.005 dex, wrong sign)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria c302aa5804 + A1 + A2, all pushed before any number.
Script: qx32.py (256^3 FFT, box 6 Mpc, cell 23.4 kpc; one thread). Outputs: qx32.json/.out, run_main.txt.

**Question:** the X-COP miss is +0.30 to +0.47 dex on the plain law. Can it come from reading aspherical clusters as spheres?
Each X-COP baryon profile is laid out on oblate and prolate homoeoids (q 0.7 and 0.5) at fixed mass. The law's QUMOND field
(longitudinal projection of nu g_N) is solved on the grid. The quantity read is the shell-averaged radial pull, r^2 <g_r>/G, at the
X-COP radii, compared with the q = 1 run.

## Result: NEGLIGIBLE, both footings

| shape | mean Delta canonical [range] | alt |
|---|---|---|
| oblate 0.7 | -0.0017 [-0.0081, -0.0010] | -0.0017 |
| oblate 0.5 | -0.0049 [-0.0094, -0.0037] | -0.0049 |
| prolate 0.7 | -0.0013 [-0.0124, +0.0004] | -0.0013 |
| prolate 0.5 | -0.0037 [-0.0083, -0.0015] | -0.0038 |

The largest class mean is -0.005 dex. The miss needs +0.30 to +0.47, so it is about 100 times too small and has the wrong sign.
Shell-averaging the pull over an aspherical cluster gives almost the spherical answer; Gauss's law nearly holds even in the
nonlinear field.

## Controls (all hold)

- K1: q = 1 on the grid matches the algebraic law to 0.013 dex at 0.2-0.7 R500. PASS (line 0.03).
- K2: Newton by Gauss, |log M_app/M_b| up to 0.023. PASS.
- MUTATE nu -> nu^2: the reading moves 0.474 dex at 0.5 R500. BITES.

## Reading

Asphericity is closed as an explanation of the cluster miss. A line-of-sight orientation bias, the other half of the asphericity
door, is not graded here: X-COP's HSE masses are spherical averages of the pull, and this lane measures exactly that average.
