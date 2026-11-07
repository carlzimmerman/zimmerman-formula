# SV5 iter_3: class T. Sector Jeans scale tied to a0(z) proportional to sqrt(rho_DE(z)). FROZEN CRITERIA

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md, before any script or number.

## Class

lambda_J(z) = F(r(z)) (physical), r(z) = a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) (EQUATIONS 3.1, a0 = kappa c sqrt(G rho_DE)),
for ANY function F. The coupling knows the time only through a0.

## Histories

- H-flat (graded): r == 1 (the footing background, constant rho_DE).
- H-native (graded): CFG689 primary (BAO + Pantheon+, curvature free) a0_node medians at nodes 0, 0.4, 0.7, 1.0, 1.5, 2.33;
  rho_DE proportional to a0^2, linear in z between nodes (CFG689's own interpolation), held beyond z = 2.33.
- H-CPL (REPORTED only, CDM-family fit): DESI DR2 (w0, wa) = (-0.838, -0.62), a0kit rho_de_ratio, as WG4.

## Host requirement

lambda_J(z) >= lambda_host (T0.3) for z in Z_H = [0, 0.5] (SPARC at z ~ 0; KiDS isolated lenses z <= 0.5), 501 samples.
QX10 found the end state quasi-static, so the requirement is instantaneous (generous).

## Members

- M* (most generous arbitrary F): r is continuous and Z_H connected, so r(Z_H) is an interval I_H. Any admissible F has
  F >= lambda_host on I_H, so lambda_J >= lambda_host at every z with r(z) in I_H. M*: lambda_J = lambda_host there, dust
  (kJ = 1e8 Mpc^-1) elsewhere.
- Power-law members: lambda_J = lambda_0 r^q, q in {-6, -5.5, ..., 6}, lambda_0 = lambda_host / min over Z_H of r^q.

## Gate and label

- T1: g2gen Delta chi^2 <= 4 (QX3 / QX7 line), z from 3400 to 0 (covers the primary-CMB epoch's coldness).
- NO-GO FOR CLASS for a history if M* fails T1, given A-mono (more Jeans suppression does not lower Delta chi^2).
  K-mono: M* plus lambda_host also on z in [1, 2] must give Delta chi^2 >= M*'s. If K-mono fails, the label is FAIL, not class.
- If M* passes for H-native: WINDOW-CONDITIONAL, with the minimal |d ln F / d ln r| needed between I_H and the nearest
  growth-critical r, and the other gates rechecked (SPARC / KiDS by the lambda_host construction; Cassini, c_T ARGUED; primary
  CMB: dust at z >= 10 unless r(z >= 10) falls in I_H).
- Lean: equal r gives equal lambda_J (time-only coincidence); IVT crossing r(z_c) = 1 for a history with r(z1) > 1 > r(z2).

## Checks and MUTATE

- MUTATE M1 (F == dust): T0.3's grid at lambda = 1 kpc via QX10 must FAIL G5 or G6 (bites).
- MUTATE M2 (F == lambda_host at every z): T1 must FAIL (bites).
- Both footings: lambda_host per footing (T0.3); growth is footing-independent; both reported.
