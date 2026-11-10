# HE1 AMENDMENT A1 (committed alone, after the first run and before the second)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

## Why

The first run of he1.py (criteria 0e67f3c64a) was **NO VERDICT on both footings**: known answers KA1 and KA6 failed. Its
outputs are kept unchanged as `he1_run1_noverdict.json`, `he1_run1_noverdict.out` and `run_main_run1.txt`. I read all of it,
gates included, before writing this file (disclosed below). This amendment changes three known-answer checks and the lens
mass grid. It changes no gate, line, input, closure, X, R_out or model.

## Changes

1. **KA1 (check implementation brought to the frozen text).** "Started with negligible density" was coded as
   rho_w = 1e-14 (units M_b / r_M^3). Over three decades in radius (to x = 5e4) that density carries about 5 M_b, so its
   self-gravity is not negligible and the Boltzmann profile is missed by 1.6e-4. Now rho_w = 1e-24 (envelope mass under 1e-9
   M_b). The tolerance (1e-6) and the singular-start check are unchanged.
2. **KA3 (check implementation brought to the frozen text).** The frozen tolerance is 1e-4. The code compared the thin
   shell with a 0.1 %-thick shell at a 2e-3 tolerance, which is looser than frozen. Now the analytic thin shell (Sigma and
   M_cyl) is compared with the closed form of a uniform shell of relative thickness 1e-5, at 1e-4.
3. **KA6 replaced; lens mass grid 0.1 -> 0.005 dex.**
   - As frozen, KA6 asks the interpolated per-bin factor to match a direct solve to 2e-3 relative in every bin at mid-grid
     masses. It failed by 22 (relative) / 0.33 (absolute) at 0.1 dex. A check before this file gave 34 / 0.16 at 0.02 dex and
     13 / 0.06 at 0.01 dex.
   - Cause: the wall carries the compensating layer -M_ph(R_w), whose projection is singular as 1 / sqrt(R_w^2 - R^2). When
     the wall crosses a bin edge as the mass changes, the bin average changes like sqrt(distance), so linear interpolation
     in mass converges slowly. In bins just outside the wall the factor crosses zero, so a relative tolerance cannot be met
     there. No practical grid passes the frozen pointwise check.
   - What G4 needs is the accuracy of the stacked window amplitudes. **New KA6:** the lens grid is log M 9.1 to 11.1 by
     0.005 dex. For every case graded or reported in G4 (closure A, three X, three R_out; closure C, three X), both stacks
     and both footings, every model window amplitude changes by less than 0.01 between the 0.01-dex grid (every other node)
     and the 0.005-dex grid. 0.01 is under 7 % of the smallest jackknife error of a window amplitude, 0.15.
   - The frozen pointwise check is still computed at 0.005 dex and reported. It gates nothing.

## Post hoc diagnostics added (reported only; no label uses them)

- G5: for each cluster, the innermost radius in [0.05, 1] R500 at which p_wall >= p_c. Beside it, the same statistic with
  X-COP's NFW-fit hydrostatic mass (`M_NFW`, monotone) in place of `M_FORW`. G5 stays graded exactly as frozen.
- Part B: the inner root of the share condition, reported as a second equilibrium.

## What the first run showed (seen before writing this file)

- Known answers: KA2, KA3 (at the looser tolerance), KA4, KA5, KA7, KA8 passed. KA1 and KA6 failed as above.
- G1-G3: X_share and X_census pass at r_ta. X_cap fails G1 at r_ta (smallest wall 3.1 r_M, high-mass end of the GSMF grid).
  At the 1.5 and 3 Mpc brackets, X_share fails G2 (walls beyond R_K for low masses). X_census and X_cap fail G2 at 3 Mpc.
  X_cap fails G3 at 1.5 Mpc.
- G4 (0.1-dex grid): fails at the primary R_out for every X on both footings (model window amplitudes about 0.05 / 0.35 /
  1.05 for X_share and 0.35 / 0.4 / 0.6 for the census share, against host-free late -0.19 / 1.53 / 1.58 and W30 late
  0.53 / 1.54 / 0.92). At the brackets G4 passed on alt for X_share at 1.5 Mpc and for X_census and X_cap at 3 Mpc, and
  narrowly failed on canonical (p 0.043, 0.044, 0.021). The law alone has p 0.033 (W30 late) and 0.0005 (host-free late).
- **G5 fails as frozen on both footings.** The 20 Lovisari groups (both f*) and five X-COP clusters hold (largest
  p_wall / p_c 0.52 and 0.24). A644's M_FORW falls beyond 0.8 R500, and A2319's component mass flattens beyond 0.9 R500. The
  lower bound p_c (no tail, component density clipped at 0) then goes to zero near R500.
- First-run labels: NO VERDICT / NO VERDICT. Read through the gates, FAILS at the primary R_out for every X (G4, G5; G1 also
  for X_cap).

The changes above cannot move G5, and they cannot move G4 at the primary R_out by the margins seen there. The label of the
second run will be what it is.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
