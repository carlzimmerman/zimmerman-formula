# GAL1 RESULT (criteria b6f30f6460, amendment A1 2a8a04b3e0)

**ALLOWANCE CONFIRMED / ALLOWANCE CONFIRMED** (canonical / alt).

TEST lane, quarantined. Adopts nothing and relabels nothing. kappa = 1/2 FITTED; not theory closed. Footings graded
separately, never pooled. Every known answer passes. M-POT bites. **M-SIGN does not bite as frozen**: one history has three
bins that lie before its switch-on, where no boost exists yet (section 3). On every bin where the boost is on, growth drops.

## Answer

- With the boost acting on growth as well as on the potential, the tightest 2 sigma allowance on a constant filling is
  **f <= 0.0197** (CMB lensing, switch-on at z 3). That is 0.85 x SWT1's 0.0231, inside the frozen band (0.0154 to 0.0347).
- The readings keep their sides on both footings. **L and C fail** every probe (L: r_eff 1.48 / 1.60 against the line 1.048;
  S8 +12 / +14 %; f sigma8 +16 to +32 %). **NC and NL pass** every graded probe (NC r_eff 1.029; NL 1.004).
- **The confirmation comes from cancellation; there is no slack in it.** Starting from SWT1's 0.0231 (3 sigma, boost on at
  every z, potential only): 2 sigma instead of 3 gives 0.0156 (x0.68). Switching on at z 3 instead of every z leaves the
  kernel's z > 3 part unboosted, giving 0.0229 (x1.47). Adding growth gives 0.0197 (x0.86).
- **The label rests on the frozen earliest switch-on (z 3).** Reported after the freeze: switching on at z 4 gives 0.0165,
  still inside the band; **at z 6 it gives 0.0134, below it (TIGHTER).** NC with its own f(z) carried to z 6 still passes
  (r_eff 1.044 / 1.044).
- Growth and S8 are loose: f sigma8 allows 0.12, S8 0.075 (z_on 3). CMB lensing is the probe that binds.

## The table

Allowance = largest constant f passing the line, for switch-on at z 3 / 1.5 / 0.5. Reading statuses are identical on the
two footings (canonical / alt shown once); reading histories are SWT1's q(z) on z 0-3, switched on at z 3.
**Bold rows are graded**; the others are reported and carry no label.

| probe | row used (on disk in the record) | allowance on f, z_on 3 / 1.5 / 0.5 | L | C | NC | NL |
|---|---|---|---|---|---|---|
| **CMB lensing, 2 sigma** | PR4 amplitude of the reference X0, A 1.02103, sigma_A,rel 0.024062 (SV5 T0.4, cfg917_lib PR4 conservative L 8-400); line \|r_eff - 1\| <= 0.04812 | **0.01968** / 0.03505 / 0.1467 | FAIL (1.483 / 1.599) | FAIL (2.590 / 2.612) | PASS (1.0287 / 1.0289) | PASS (1.0040 / 1.0040) |
| **f sigma8** | DESI DR1 Table 9 ratios as CE2 carries them, 4 bins x 2 panels, 2 err | 0.1197 / 0.1754 / 0.4562 | FAIL (Rf 1.16-1.32) | FAIL (1.48-1.69) | PASS (1.014-1.017) | PASS (1.002) |
| **S8** | KiDS-1000 0.759 +- 0.0225 (SS4 CS line, change <= 5.93 %) | 0.0753 / 0.1433 / 0.4564 | FAIL (+11.8 / +14.2 %) | FAIL (+33 %) | PASS (+0.86 %) | PASS (+0.11 %) |
| CMB lensing, 3 sigma (WL1 / SWT1's line 1.0722) | same as the first row | 0.02892 / 0.05085 / 0.1956 | FAIL | FAIL | PASS | PASS |
| CMB lensing centred on the data (\|A' - 1\| <= 2 sigma') | same | 0.02816 / 0.04957 / 0.1920 | FAIL | FAIL | PASS | PASS |
| CMB3 A_phi scan (2 sigma about 0.062, my interpolation) | closure_2026_11_07/CMB3 | 0.02506 / 0.04429 / 0.1762 | FAIL | FAIL | PASS | PASS |
| shear-equivalent S8, (1 + q) s at z 0.3, 0.5 | KiDS-1000 band | 0.02742 / 0.03292 / 0.03771 | FAIL | FAIL | PASS (+2.1 %) | PASS |
| CE2 suppression rule Rf <= 1.001 | CE2 | 0.00070 / 0.00108 / 0.00419 | FAIL | FAIL | FAIL | FAIL |

- The PR4 shape chi^2 (amplitude refitted; record line 18.48, reference 8.57) is 8.6-8.8 for NC, NL and every constant-f
  history. Reading L is 19.9 / 23.9 and C 34.8 / 35.3, so L fails even the shape test. The boost changes the amplitude far
  more than the shape (S at L 100 / 200 / 400 = 1.050 / 1.043 / 1.036 at the allowance).
- **CE2's rule** was written for lanes that suppress growth. Any positive boost breaks it, NL included (Rf 1.002). It is not
  a 2 sigma allowance, and it is reported only.
- **Shear-equivalent S8** binds for a late switch-on (0.038 at z_on 0.5 against the lensing row's 0.147). It does not move
  f_tight (0.0274 > 0.0197).

## 1. What was computed

- **Background.** The record's reference (QX3 iter2 corner: omega_b 0.0215, omega_d 0.11958, H0 65, n_s 0.95), H(z) from
  CLASS.
- **Growth.** delta'' + (2 + d ln H / d ln a) delta' = (3/2) Omega_cl (1 + q) delta, from CLASS's growing mode at z 30.
  s = D_q / D, Rf = D_q' / D'.
- **Lensing.** Standard Limber kernel (cfg917_lib form): C_L proportional to the integral of
  [(1 + z)(chi* - chi) / chi*]^2 P_lin((L + 1/2)/chi, z) R(z)^2 dchi, with R = (1 + q) D_q / D: the direct boost of the
  potential and the growth. S(L) X0 is graded with the record's PR4 amplitude rule, r_eff = A(X0) / A(S X0).
- **Histories.** SWT1's q_tot(z) for L, C, NC, NL (computed here with swt1.py's own `compensated`; z 1 replays SWT1 to the
  printed digits, e.g. L 0.3029 / 0.3612, NC 0.0180 / 0.0182). Constant-f histories use q = 1.5 f / (1 - f), switched on at
  z_on.

| reading, q(z) at z 0 / 1 / 2 / 3 (canonical; alt within 0.002 for NC, NL) | f(z) at the same z |
|---|---|
| L 0.308 / 0.303 / 0.180 / 0.116 (alt 0.367 / 0.361 / 0.213 / 0.136) | 0.169 / 0.170 / 0.111 / 0.076 |
| C >= 0.667 / 0.645 / 0.626 / 0.611 (filling over 0.30: lower bounds) | 0.69 / 0.70 / 0.46 / 0.32 |
| NC 0.0120 / 0.0180 / 0.0198 / 0.0199 | 0.0080 / 0.0124 / 0.0141 / 0.0146 |
| NL 0.0013 / 0.0026 / 0.0028 / 0.0027 | 0.0009 / 0.0019 / 0.0021 / 0.0022 |

NC's filling peaks at 0.0148 (z 3-6). That is above the constant-f allowance for switch-on at z 6 (0.0134). NC's own
history carried to z 6 still passes (r_eff 1.0438 / 1.0442 against 1.0481, 91 % of the line), because its filling falls to
0.008 by z 0.

## 2. Known answers (all PASS)

- KA1: A_X0 1.0210287 and sigma_A,rel 0.0240616 equal sv5_t0.json (relative difference 0); X0's PR4 chi^2 8.5708 against 8.5709.
- KA2: G_eff = G against CLASS's D, f and f sigma8 at eight z from 0 to 3: max relative difference 2.4e-5 (line 2e-3).
- KA3: Einstein-de Sitter growth index for q = 0, 0.05, 0.3, -0.2 equals (-1 + sqrt(1 + 24 (1 + q))) / 4 to 2e-16.
- KA4: (a) constant R gives S = R^2 to 1e-14; (b) my absolute Limber X_L against CLASS's X0 at L 100-400: within 4e-4 (line
  2 %); (c) cfg917_lib.limber_X on its own grid gives the same S(L) for f 0.02, z_on 1.5 to 8.7e-5 (line 1e-3).

## 3. MUTATE

- **M-POT (potential only, growth left at the reference): BITES.** Growth ratios exactly 1. The 2 sigma lensing allowance at
  z_on 3 loosens from 0.01968 to 0.02293. Its check: with the boost on at every z and the 3 sigma line it gives f = 0.02310,
  SWT1's 0.0231 (relative difference -2e-4).
- **M-SIGN (q -> -q): NO BITE as frozen.** s(0) and r_eff drop for all 11 histories, and Rf drops at every bin for 10 of them.
  The z_on 0.5 history's bins LRG1-LRG3 (z 0.51-0.92) lie before its switch-on. No boost exists there in either run, so
  Rf = 1 to 2e-12, and the frozen condition ("Rf < 1 at all four bins for every history") cannot be met. That is a defect in
  how I wrote the bite condition, not in the code. The reported re-read (gal1_extra E3) shows Rf < 1 at every bin where the
  boost is on, in all 11 histories. The label does not use M-SIGN.

## 4. Reported (gal1_extra.py, post-freeze; no label rests on it)

- E1, earlier switch-on: z_on 4: lensing 0.01648, f sigma8 0.105, S8 0.060, shear 0.025. z_on 6: lensing **0.01336**,
  f sigma8 0.089, S8 0.046, shear 0.022.
- E2, decomposition at f 0.0231: r_eff 1.0722 (every z, potential only) -> 1.0485 (z_on 3, potential only) -> 1.0569 (z_on 3,
  with growth).
- **QX3 iter2's limber_ratio** (used by several cosmology lanes) gives 1.0769 at L 100 where the standard kernel gives
  1.0274 for the same history. Its extra chi^-4 weight pushes the ratio towards its low-z value. This replays CK4's finding,
  confirmed by GL2 (closure_2026_11_07/GL2_limber_k4_audit). It is not new. GAL1 does not use that function.

## 5. What this does and does not show

- SWT1's statement "law-on regions may fill at most about 2 % of space" survives once growth is added: 1.97 % at 2 sigma
  with switch-on at z 3. The switch class still turns on KiDS's outer points against a filling of about 2 %.
- The number is not robust to the switch-on epoch. Law-on regions that already fill 2 % at z 6 are held to 1.3 %. SWT1's
  readings use the z 0 stellar mass function at every z, so they over-count hosts at z 2-6 and bracket q(z) from above.
- Reading NC passes everything graded, with r_eff - 1 at 60 % of the 2 sigma line (91 % if carried to z 6). It is the
  self-consistent reading, and it holds the law out to only 0.1-1.9 Mpc depending on mass and z (SWT1's radii), short of
  KiDS's 3 Mpc.
- No halo-model or nonlinear lensing, no scale dependence of the boost on scales near the bubble size, no change to the
  primary CMB from a boost before recombination (none of the histories reaches it).

## Files

FROZEN_CRITERIA.md, AMENDMENT_A1.md, gal1.py -> gal1.json / gal1.out (run_main.txt with timing), gal1_MUTATE_potonly.json
/ .out, gal1_MUTATE_sign.json / .out (run_mutate_*.txt), gal1_extra.py -> gal1_extra.json / .out (run_extra.txt). One
thread; main run 89 s, peak 0.23 GB (the MUTATE and extras runs are smaller; not timed separately). Nothing downloaded.
Not registered.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
