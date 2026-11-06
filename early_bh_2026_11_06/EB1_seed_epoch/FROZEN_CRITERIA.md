# EB1_seed_epoch: FROZEN CRITERIA, committed alone before any script or number

Kappa = 1/2 FITTED. Not theory closed. No dark-matter particle, no cold component added. Nothing here says the data
favour the framework. No downloads. Small job: one thread, < 1 GB, minutes.

**Not blind.** Known before this file: WG2-WG6 (law alone from a baryons-only start fails the CMB-lensing shape);
QX3 (growth inside the action fails); the baryons-only field is Silk-damped; L324 (A2744-QSO1 at z 7.0451 weighed
10^6.9-10^7.7 Msun, M_BH / M_* > 2).

## Question
Under the record's one rule for the law on the cosmic web (WG2's R1), can a baryon clump big enough to make
A2744-QSO1's black hole collapse early enough for Eddington-limited growth to reach its mass by z 7.0451?
R0 (law off, Newton, baryons only) is the control.

## Inputs (all from the record; none fitted here)
- **Baryon field.** WG2's CLASS settings, unchanged: omega_b 0.02237, h 0.6736, omega_cdm 1e-7, n_s 0.9649, pivot
  0.05 Mpc^-1, massless neutrinos by CLASS default. Transfer d_b(k) per unit curvature at z_on, P_R = 2 pi^2 A_s
  (k/k_p)^(n_s - 1) / k^3. k_max raised to reach 1e6 Msun (K3 checks convergence).
- **A_s:** 2.1e-9 (primary, the record's value), bracket {1e-9, 4e-9} (WG2's bracket ends).
- **Backgrounds:** B2 (primary; WG2's smooth unexplained matter term, Omega_fld 0.2504, w -0.001, cs2 1) and B1
  (baryons only + Lambda). Radiation omega_r 4.18e-5 in E(a) for both.
- **a0:** a0kit footings, canonical 9.3542e-11 and alt 1.1356e-10 m/s^2, never pooled. TIE (flat; constant rho_DE
  beyond z 2.33, as a0kit / WG2) primary; RIVAL a0 E(z) reported only.
- **Turn-on:** z_on = 50 (WG2's value) primary; z_on = 200 reported. Before z_on the clump follows CLASS's GR linear
  field.
- **QSO1 (record, L324 / opus_49_doorB re-audit):** z 7.0451; log M_BH in {6.9 (spectroastrometric low), 7.6
  (virial 4e7), 7.7 (MOKA3D dynamical headline)}.

## Method
1. **sigma_b(M).** Top-hat sigma of the baryon contrast at z_on, Lagrangian radius from the mean baryon density
   (baryons are the only clustering matter), for M_b in {1e6, 1e7, ..., 1e13} Msun. Growth rate of the window,
   f_M = <delta d delta / d ln a> / sigma^2, from CLASS d_b at z_on (1 +- 2 %), as WG2.
2. **Spherical collapse.** One shell of baryon mass M_b, physical radius r, peak height nu_pk in {1, 2, 3, 4, 5}:
   delta_0 = nu_pk sigma_b(M) at z_on; r_0 = a_on R_L (1 - delta_0 / 3); dr/dt_0 = H r_0 (1 - f_M delta_0 / 3).
   d2r/dt2 = -(4 pi G / 3) [rho_b + rho_fld + 2 rho_r - 2 rho_L] r - nu * G dM / r^2,
   dM = M_b - (4 pi / 3) rho_b(t) r^3 (the Newtonian peculiar source), g_N = G dM / r^2.
   R0: nu = 1. R1: nu = nu_simple((|g_N| + e a0) / a0), nu_simple(y) = 1/2 + sqrt(1/4 + 1/y) (WG2's form).
   Spherical QUMOND is exact for an isolated sphere; the external field is the scalar bracket e in {0 (primary,
   isolated), 0.03, 0.1} (WG1 puts the web field at 0.003-0.22 a0).
   Collapse: r <= 1e-3 r_max after turnaround. Report z_ta and z_coll. Gas pressure is neglected (stated limit:
   valid for M_b well above the baryon Jeans mass, ~1e5 Msun Newtonian at z 50).
3. **Seed time.** t(z) = integral da / (a H) on the same background. Salpeter time t_E = 450.7 Myr eps / (1 - eps),
   eps = 0.1 primary (50.1 Myr), 0.2 reported; duty cycle 1 (fastest growth). Latest seed time
   t_seed = t(7.0451) - t_E ln(M_BH / M_seed), M_seed in {1e2, 1e4, 1e5 (primary), 1e6} Msun. Clump mass needed
   M_clump = 10 M_seed (10 % of the collapsed baryons go into the seed; declared, not derived).

## Gate G1 (per rule, footing, M_BH, M_seed)
nu_req = smallest nu_pk in the grid whose clump of mass M_clump (log-interpolated in sigma_b) collapses with
t(z_coll) <= t_seed.
- **EASY** nu_req <= 2; **RARE** 2 < nu_req <= 4; **EXTREME** nu_req = 5; **NO** none in the grid; **NO (age)** if
  t_seed <= 0.
- **Primary cell:** B2, A_s 2.1e-9, z_on 50, e = 0, TIE, eps 0.1, M_seed 1e5, M_BH 10^7.7 and 10^6.9, both
  footings, R0 and R1.
- Label is about TIMING only. It says nothing about abundance (EB2), cooling (EB4) or fragmentation (EB5).

## Checks (all must pass for any label)
- **K1** EdS, R0, tiny delta_0: linear contrast extrapolated to collapse = 1.686 within 1 %.
- **K2** R1 with a0 -> 1e-30 m/s^2 reproduces R0's z_coll to 1e-3 (B2 primary cell, M 1e9, nu 3).
- **K3** sigma_b(1e6 Msun) changes < 2 % when k_max is doubled.
- **K4** t(a) on EdS equals (2/3) a^1.5 / H0 to 1e-6.
- **MUTATE** (EB1_MUTATE=1): G halved in the shell equation. K1 must FAIL. Outputs carry _MUTATE.
