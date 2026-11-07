# KX1 frozen criteria: QX10's KiDS kill of the late-heated window, re-graded with a joint systematic budget at 100-300 kpc

Frozen and committed alone, before any KX1 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
TEST lane (cold dark energy, never the other name; no particle). Footings graded separately, never pooled:
canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2. One thread, < 1 GB, no download. Brief: DEDUCTION_2026_11_07.md section 4.

## What is known before this freeze (not blind)

QX10 iter_2's G6 shifts (C1-C4: -0.236/-0.239, -0.270/-0.273, -0.153/-0.157, -0.248/-0.250) and its all-radii law
baselines (+0.142 / +0.102); CW6's M_hot(<r)/M* table; CFG15's lens-bias caps; CFG96's A_20; the B21 Fig-9 radii.
The per-bin 100-300 kpc residuals of data, law and window have not been computed by anyone.

## Object (unchanged from QX10, imported read-only)

The four QX10 cells C1-C4 and QX10 iter_2's static end state (method A): the n = 1 sector of mass f_cap R M_b around a
point-mass host, solved with qx10_i2.py's own solve_static, executed read-only up to its `__main__` block. No new constant.

## Data and the window

B21 Fig-9 isolated KiDS lenses, four stellar-mass bins (QX5's loader: log M_b 9.4, 10.45, 10.7, 10.9; g_obs = 4 G ESD /
bias), full Fig-9 covariance (divided by its bias column). Radius per point by QX10's rule r = sqrt(G M_b / g_bar).
Graded points: 100 <= r <= 300 kpc in each bin (4 / 3 / 3 / 4 points; all four bins graded).

## Statistic per bin (GLS amplitude)

For a model vector m (g_obs predicted at the graded points) and data y with covariance C:
a(m) = m'C^-1 y / m'C^-1 m, sigma_a = (m'C^-1 m)^-1/2.
- Law model: m_law = glaw(g_bar + g_hot). Window model: m_win = glaw(g_bar + g_hot + G M_d(<r)/r^2) (QX10's local estimator).
- E_b = log10 a(m_law): the posterior excess of the data over the law (after the central corrections below).
- W_b = log10[a(m_law) / a(m_win)]: the window's excess over the law in the same bin.
- Line L_b = E_b + 2 sigma_tot,b: the largest window excess over the law the data allow at 2 sigma_tot.
- z_b = (W_b - E_b) / sigma_tot,b = -log10 a(m_win) / sigma_tot,b (the window's over-prediction of the data).

## The joint budget (central value, sigma), each evaluated as a shift of log10 a for that model and bin

1. Hot CGM gas from the kSZ record (CW6, cw6_gas.out table): central P1 (sharp 1.8 R_vir, A 0.542, CW6's primary);
   sigma_gas = half the full range of log10 a over CW6's profiles P1-P6 and brackets B1-B5. M_hot(<r)/M* interpolated
   linearly in log M* and log r on CW6's grid; bin 1 (log M* 9.4) uses the log M* 10.0 row (nearest; disclosed).
   Gas enters g_N for law and window alike; the sector solve keeps QX10's stellar point-mass host (as QX10).
2. Two-halo term (CFG4/FP1's projected matter template T2H, CFG15's lens bias as the cap): the data ESD carries
   b T2H(R) with b uniform in [0, b_cap]; b_cap = CFG15's collapse-threshold bias per bin in mass order
   (canonical 1.11 / 1.35 / 1.44 / 1.57; alt 1.14 / 1.39 / 1.49 / 1.63). Central: subtract (b_cap/2) T2H from y;
   sigma_2h = shift for b_cap/sqrt(12). R for the template = r (QX10's conversion), interpolated in log R.
3. Isolation / satellites (CFG96, CFG116): CFG96 found the 1-halo split stable under 2x stricter isolation, A_20 =
   0.97 +- 0.19. Budget: sigma_iso (dex) = log10(1 + sigma_A20 (1 - 10^-0.18)), with CFG116's 0.18 dex split as the
   fraction of the signal an isolation change can move. Central 0.
4. Stellar-mass bin shift: delta = 0.1884 dex (GH9's median, CW6 B3). Both M_b and g_bar scale by 10^(+-delta) and the
   sector is re-solved for the shifted mass; sigma_M = half the difference of log10 a at +delta and -delta.
5. ESD calibration (the bias column): sigma_cal = log10 of the file's |1 - (1+K)| relative bias per bin. Central 0.
6. Statistical: sigma_a / (a ln 10) for that model, with the central corrections applied.
sigma_tot,b = quadrature sum of 1-6. The window's sigma_tot uses the window's own shifts; the law's uses the law's.

## Labels, per cell, per footing

- NO POWER if W_b < 2 sigma_tot,b in 3 or more of the 4 bins (the window cannot be told from the law).
- KILL HOLDS if z_b > 2 in 2 or more bins.
- KILL SOFTENS otherwise (the window sits inside 2 sigma_tot in at least 3 bins).
- Per footing: the window is KILL SOFTENS if any cell is KILL SOFTENS; KILL HOLDS if all four cells hold; NO POWER if
  no cell has power. Footings are reported separately; the lane label is stated for each.

## Known answers (must pass, else NO VERDICT)

- KA1: QX10's G6 shift for every cell and footing, recomputed through qx10_i2.py's own grade_cell, to |d| 0 against
  qx10_i2.json; and its baselines (+0.14171 / +0.10160) to 0.
- KA2: the CW6 gas interpolator returns CW6's table values at grid nodes to 1e-12.
- KA3: sector mass 0 gives W_b = 0 exactly.

## Controls (MUTATE, separate outputs)

- M1: the window at 4x sector mass (M_d = 4 f_cap R M_b, re-solved) must read KILL HOLDS for every cell, both footings.
- M2: the law itself (sector 0, W_b = 0) must not be killed: its z_b = -E_b / sigma_tot,b (law shifts) must be <= 2
  in at least 3 bins, both footings. If M1 or M2 fails, the label is NO VERDICT.

## Reported, not graded

- The projected reading: model g_obs = 4 G Delta Sigma from the projected excess surface density of the 3D effective
  mass (glaw r^2 / G), for law and window, instead of the local estimator.
- All radii (QX10's range) with the same budget; the budget terms one at a time.
