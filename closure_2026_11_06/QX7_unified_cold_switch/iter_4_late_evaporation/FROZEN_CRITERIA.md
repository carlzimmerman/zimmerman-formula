# QX7 iter_4 frozen criteria: captured early, puffed up late (the size of today's Jeans length sorts galaxies from clusters)

Frozen before any iter_4 number. Kappa = 1/2 FITTED; not theory closed. Mutation of iter_2/iter_3 (76a0c3e0b7, f9020230b6).
Both failed for the same reason: keeping dust OUT of massive ellipticals at z = 2 while the forest is cold at z = 3 forces a
heating so steep that the dust stops clustering inside the CMB-lensing kernel.

## Mechanism

The iter_3 switch is unchanged: lambda_J = lambda_* Omega_DE(a)^p, leaf-uniform. Capture before heating is now ALLOWED.
Today every bound system holds its captured dust, M_d = f_cap R M_b (f_cap 0.76, R = omega_d/omega_b), as an n = 1 hydrostatic
core of radius R_c = lambda_J(z=0)/2. That is QX3 D3: R = pi/mu with lambda = 2 pi/mu. A system keeps no dust
if R_c >= its turnaround radius today, r_ta(M_b(1+R), z=0). Enclosed fraction (sin xi - xi cos xi)/pi with xi = pi r/R_c,
and 1 for r >= R_c. The dust is no longer assumed to trace the baryons. This is a stated idealisation of a pressure-supported
remnant: no dynamics are solved.

## Grid

p in [0, 6] in steps of 0.125; lambda_0 = lambda_J(z=0) log-spaced from 1e-3 to 1e2 Mpc (61 values);
lambda_* = lambda_0 / Omega_DE(0)^p.

## Non-cluster gates (fix the window)

- G4' (forest) and G2' (CMB-lensing growth), as iter_3, with the same generalised solver.
- G5 (SPARC): the reference galaxy (M_b 1e10, R_opt 10 kpc) and the 5 most massive SPARC galaxies, at R_opt = 10 kpc and
  20 kpc respectively: M_d(<R_opt)/M_b <= 0.3 (QX3 G3 line).
- G6 (KiDS isolated-galaxy lensing, Brouwer 2021, 59 points): g_pred = g_law(g_bar + G M_d(<r)/r^2). The mean log(g_obs/g_pred)
  must not shift by more than 0.05 dex from the M_d = 0 baseline (QX5's lensing recheck line). Both footings.
- G7 (Humphrey ellipticals at 2, 4, 8 R_e): M_pred = M_law(M_b + M_d). The mean log(M_obs/M_pred) must not shift by more than
  0.15 dex from baseline (QX5's line).

## Cluster predictions (no cluster input)

- X-COP: M_d(<r) uses the cluster's M_b,tot = Mb_last. M_pred = M_law(M_b(<r) + M_d(<r)). HO1 line.
- Groups: the same, with M_b,tot = Mgas500 (1 + fst). The strict iter_3 group rule must hold for both stellar allowances;
  "either" is reported.
- PASS if a window exists and at least one member passes X-COP and groups on both footings; report the fraction.
  FAIL (no window) / FAIL (clusters) otherwise.

## Controls

- MUTATE 1: lambda_0 forced to 1e-3 Mpc (every system keeps a compact core) must fail G5 or G6 (galaxies ruined).
- MUTATE 2: f_cap = 0 reproduces QX2 iteration 1's X-COP mean to 1e-3, and the lensing and elliptical baselines exactly.
- MUTATE 3: f_cap x 3 moves the X-COP mean by more than 0.1 dex at a member with R_c below R500.
