# QX27: power-law-tail retention sector. FAILS at G6 (growth + forest) and G8 (phase-space capture), and at G1 on the alt footing

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: COLD DARK ENERGY sector, no particle, no LCDM inputs.
- Criteria: FROZEN_CRITERIA.md (8e1126f9e3), committed and pushed alone before any script or number.
- Scripts: qx27.py (static gates, ~20 s), qx27_growth.py (G6, ~15 s), one thread each. Logs: run_main.txt,
  run_growth.txt, run_mutate.txt. MUTATE outputs: qx27_MUTATE.json/.out.

## The class

The sector is cold before z_h = 10. At z_h it is heated once into p_n(v) ~ v^2 (1 + v^2/(m v0^2))^-m (m = (n+2)/2, a
v^-n tail). Each host shell keeps dM_X = R F_n(v_esc) dM_b (R = 5.562), with v_esc taken from the self-consistent a0-law
potential out to r_ta. For each n in {3.5, 4, 5, 6, 8, 12}, v0 is fixed by SPARC G5 and KiDS alone, as the most
retention galaxies allow. That gives v0_min = 1470-1880 km/s on both footings. No cluster number enters.

## Labels (per footing; the same at every n unless noted)

| Gate | canonical | alt | key numbers |
|---|---|---|---|
| G1 SPARC exact field (rms <= 0.110, median U 0.50-0.80) | PASS, all n | **FAIL**, all n | rms 0.0554 @ U 0.56 (canonical); 0.0559-0.0563 @ **0.49** (alt; the sector pulls U below 0.50, QX8 alone gives 0.52) |
| G2 KiDS | PASS (calibration gate, by construction) | PASS (same) | shift -0.010 to -0.013 |
| G3 ellipticals, absolute D (QX18 line 0.15) | PASS, all n | PASS, all n | D +0.018 to +0.057 / +0.002 to +0.044 (plain law +0.210 / +0.189) |
| G4 X-COP (HO1) | PASS n 3.5-6; FAIL n 8, 12 | PASS n 3.5, 4; FAIL n >= 5 | canonical n 4: -0.024 / 0.085; alt n 4: -0.041 / 0.092; n 12: -0.059 / 0.099 and -0.084 / 0.117 |
| G5 groups (QX5 band) | PASS, all n | PASS, all n | band e.g. [+0.011, +0.251] (canonical n 4); strict 0-5 / 20 |
| G6 T1 growth + forest | **FAIL**, all n | **FAIL**, all n | Delta chi^2 231-1059 against a line of 4; forest lambda_J(z 3) 490-1020 Mpc against 0.65 |
| G7 dSphs | PASS | PASS | median shift 0.0000 |
| G8 Liouville capture bound | **FAIL**, all n | **FAIL**, all n | max M_X/M_Liouville: X-COP 5.6e3-7.0e3, groups 1.2e3-1.6e3; every one of the X-COP and group points violates it |

**Overall: FAILS at G6 and G8 (every n, both footings), and at G1 on alt (every n).** The static T2 + T3 result is
the best in the record without cluster input. On the canonical footing at n 3.5-6, SPARC, KiDS, the ellipticals,
X-COP, groups and dSphs all pass. The ellipticals' +0.21 deficit also closes. But the class can't actually reach that
state.

## What kills it

1. **T1 against T2 (G6).** Galaxies keep under 0.3 M_b only if v0 is at least about 1500 km/s (sigma_1D 1650-3450).
   - With sigma0 that large after z = 10, the sector's Jeans length is hundreds of Mpc. Lensing-era growth is then
     carried by baryons alone.
   - The growth ODE passes only for sigma0 <= 1 km/s (reported scan: 1 km/s gives 1.3, 3 km/s gives 41.6). That is
     a gap of about 10^3 in speed.
   - Heating later is not available: T1 needs z_h >= 10. Earlier heating (z_h 20) is worse, and holding sigma
     constant after heating is still FAIL (93-378).
2. **T3 cannot be assembled (G8).** After z_h the sector is a collisionless hot sea. X-COP clusters and groups
   assemble later, so the sector's coarse-grained phase-space density can't exceed the sea's own maximum,
   f_max ~ rho_sea/v0^3.
   - Inside a host's escape sphere that caps the density at about rho_sea (v_esc/v0)^3, roughly 10-30 rho_sea.
   - The retention the cluster pass needs (R F rho_b, with F 0.7-0.98 in X-COP) sits 10^3-10^4 above that cap at
     every graded point.
   - So the static pass assumes capture that the sector's own dynamics forbids. A sector cold enough to be captured
     (small v0) is retained by galaxies: M3 at v0 = 30 km/s gives G5 4.6 M_b and KiDS -0.43.
   - **The same speed scale that keeps galaxies empty forbids cluster capture.**

## MUTATE and controls

- M1, Maxwellian with the same v0 at each n: FAILS on both footings at every n, so it **BITES**. It fails G4 X-COP
  (-0.073 to -0.097 / 0.108-0.127) and G8, and at several n also G3 and G1. Without G8 it still fails G4 everywhere,
  so the tail, not the shared G8 failure, is what moves X-COP.
- M1b, Maxwellian with its own galaxy-fixed v0 (2039 km/s): X-COP -0.071 / 0.107 and -0.095 / 0.125, FAIL. This
  repeats QX12 iter_2/iter_3's thermal class. The tail beats it on X-COP but not on G6/G8.
- M2, R = 0: X-COP +0.4675 / +0.4345, BITES. M3, v0 = 30 km/s: C1 4.61, C2 -0.43, BITES.
- G6 controls: sigma0 = 0.01 km/s gives Delta chi^2 7.5e-5 (cold limit recovered). A sector made smooth from z = 1089
  gives 914.6, so the gate has power.
- Known answers: KA2 ellipticals +0.2099 / +0.1887 (QX18 +0.210 / +0.189), PASS. KA3 R = 0 X-COP +0.4675 / +0.4345,
  PASS. KA4 R = 0 SPARC exact field 0.0560 @ 0.58 / 0.0558 @ 0.52, equal to QX8, PASS. KA5 v0 = 30000, C2 0.0000, PASS.
  **KA1 FAIL as frozen:** at n = 400 the tail CDF differs from the Maxwellian by 4.85e-3 against a 2e-3 line. The
  frozen line was too tight for the O(1/n) convergence of (1 + u/m)^-m to e^-u. The CDF itself is the standard
  regularised incomplete beta, and F(infinity) = 1 exactly. No label depends on it.

## Disclosures

- G6 uses QX3's fluid Jeans term with sigma_1D as the collisionless free-streaming scale (an approximation). Delta chi^2
  is not monotonic in sigma0 because the amplitude refit absorbs uniform suppression and only the shape counts. Every
  graded value exceeds the line by more than 50x.
- G8 was not evaluated for galaxies, despite the criteria's "reported" line. Galaxies keep at most 0.3 M_b, and no
  label depends on them.
- The variant with f_cap R in place of R moves X-COP by about +0.07 and changes no G6 or G8 label (qx27.out).
- Local data that is git-ignored (KiDS Brouwer+2021 and the PR4 bandpowers) was read from the existing local copies.
