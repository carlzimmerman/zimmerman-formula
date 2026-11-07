# CE2 frozen criteria: the late-heated cold-dark-energy window (QX7 iter_4 / QX10 cells) on the gates QX10 never graded

Frozen before any CE2 script or CE2 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (owner 11-04
rule; DEDUCTION_2026_11_07 section 4, lane "CE1"). The id CE1 is taken (CE1_converged_eta_grade, de82987fb9), so this lane is
CE2. Name: cold dark energy, never cold dark matter; no particle; no LCDM parameter values. Both footings, never pooled:
canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2. No downloads. One thread; the Bullet child is a separate process
(NA2 disclosed ~1.2 GB for that child; disclosed again if it repeats).

## 0. The object (no new constant)

- Switch: lambda_J(a) = lambda_* Omega_DE(a)^p (physical), lambda_* = lambda_0 / Omega_DE(0)^p (QX7 iter_3/iter_4).
- Cells: QX10's four, chosen by rule from iter_4's 270-member window before any QX10 grade (c1f0cadb7a). C1 (2.6102 Mpc,
  4.25), C2 (1.4678, 3.5), C3 (8.254, 5.625), C4 (2.1544, 3.75). No other cell is graded, and none is added later.
- Background: iter_4's own (QX3 iter2 worst corner: omega_b 0.0215, H0 65, n_s 0.95, omega_d 0.11958, R = 5.562).
- **Today's state, PRIMARY:** the sector's n = 1 hydrostatic end state in each host's own potential with the a0 law on
  (QX10 iter_2 static A, p = K rho^2, K = G lambda_J(0)^2/(2 pi), retained mass f_cap R M_b,tot with f_cap 0.76, kept unless the
  profile reaches r_ta). QX10's heating run reached this end state (quasi-static), so it is the window's physical state. This is
  the state KX1 regrades on KiDS (galaxies hold a 150-230 kpc halo of 4.2 M_b).
- Reported, not graded: iter_4's isolated n = 1 core (R_c = lambda_0/2, ignores the host), which iter_4 itself graded.

## 1. How this differs from QX7 iter_7 (this morning's SHAPE FAIL), stated before any number

- iter_7 ASSUMED iter_4's retention (R_c >= r_ta empties galaxies), which QX10 iter_2 refuted, and ASSUMED a pressureless
  phase-mixed remnant that traces the hot gas. Its galaxy gates passed by assumption; its groups failed on shape (remnant too far
  out where the group gas fraction rises outward).
- CE2 assumes neither. Retention and profile both come from the sector's own equation of state in the host's potential: a
  pressure-supported n = 1 fluid with the window's K. Galaxies keep it (as QX10 found); clusters keep it in a profile set by
  the host's potential and K, not by the gas.
- The record already REPORTED (did not grade) this profile on clusters: QX10 iter_2 gives X-COP mean/rms -0.045/0.226 (C1),
  -0.28/0.32 (C2), +0.32/0.36 (C3), -0.12/0.24 (C4), groups at most 4/20. CE2 grades it with NA2's per-bin shape rule and adds
  the gates nobody graded (group trend, Bullet, CMB lensing chi^2, fsigma8, forest at z = 2). Expected from the record: X-COP
  and groups FAIL. That expectation is written here so a FAIL cannot be called a surprise and a PASS must be checked hard.

## 2. Gates (per cell; per footing where a0 enters; CMB-side gates do not depend on a0 and are stated once for both)

| Row | Statistic | PASS line | Source |
|---|---|---|---|
| GX X-COP profile | QX5's X-COP loader (as iter_4, QX10), M_pred = M_law(M_b(<r) + M_d(<r)), Delta = log10(M_obs/M_pred) | \|mean\| <= 0.05 AND rms <= 0.10 AND every r/R500 bin (edges 0, 0.25, 0.5, 0.75, 1.0, 2.0; bins with >= 3 points) \|bin mean\| <= 0.10 | NA2 section 6 (the gas-to-stars band: HSE-traced passes, gas- and star-traced fail) |
| GG groups | QX5's 20 groups (as iter_4/QX10), sector profile in each group's host | strict rule (>= 16/20 within 2 sigma at f* 0 AND f* 1) AND no residual trend: OLS slope of the per-group mean Delta on log10 kT, \|slope\| <= 2 x bootstrap SE (2000 resamples, seed 7), at f* 0 and f* 1 | iter_4/iter_7 rule; the deduction's "f-sigma trend" |
| GB Bullet | DB1's Bullet machinery (db1_fast.py prefix, read-only, child process as NA2). The sector is a FLUID (the action's p = K rho^2), not collisionless, so it is placed by a ram-pressure split: per subcluster j, the sector's hydrostatic profile in that subcluster's Bullet-model baryons (sub_profiles), retained f_cap R (M_gas,j + M_*,j). The stripped part of the subcluster's sector is the mass at radii where its own pressure K rho_j(r)^2 < rho_main,d(d_sep) v^2, with rho_main,d the main cluster's sector density at the projected separation d_sep of the two Bullet-model centres (taken as the 3D distance), v = 2700 km/s (declared lower bracket; 4700 reported). The main cluster's sector is unstripped. Unstripped mass goes on the galaxies (DB1 "gal" field, R_j = M_unstripped,j / M_*,j); stripped mass goes on the gas (DB1 "gas" field). | bullet_row's own label (M300 Z within DB1's ZL AND cls != FAIL) | DB1 / UX6 / NA2 |
| GL CMB lensing (z < 1 suppression included) | iter_4's G2' machinery (QX3 iter3 solver generalised by iter_3, raw PR4 9 bandpowers, A_s refit): chi^2 = c0 + Delta chi^2 | chi^2 <= 18.48 AND Delta chi^2 <= 4 | QX3 iter2 lines |
| GF fsigma8 at z < 1 | from the same solver: sigma8_sw(z)^2 = int P_lin,ref(k,z) R(k,z)^2 W_TH(k 8/h Mpc)^2 k^2 dk with R = dm/ref, P_lin,ref from the solver's CLASS model; fsigma8 = d sigma8 / d ln a (spline in ln a on the solver's z grid); ratio Rf(z) = fsigma8_sw / fsigma8_ref | at each DESI DR1 bin with z < 1 (BGS 0.295, LRG1 0.510, LRG2 0.706, LRG3 0.919): Rf <= 1.001 (suppression only: the S8 direction) AND \|Rf - r_DESI\| <= 2 err on BOTH the ShapeFit-only and the ShapeFit+BAO panels (DESI DR1 Table 9 as transcribed in L181 / G045 / CFG508, errors symmetrised) | DESI DR1 (on disk, in the record) |
| GFo forest | lambda_J(z) at z = 2, 3, 4 | <= (0.42/h)/4 Mpc at every z (iter_4's G4' line, there applied at z = 3 only) | QX7 iter_3/iter_4 |

- GF disclosure, fixed now: DESI's ratio is to its Planck-LCDM fiducial; CE2 compares DESI's ratio with the sector's own
  suppression ratio relative to the same sector unheated (the cold reference on iter_4's background). The absolute cold
  reference is QX15's question, not graded here.
- GB disclosure, fixed now: the DB1 "gal" field puts mass in galaxy-scale profiles; the sector's real halo is wider. This
  can only move the lensing peaks toward the cluster centres; it is stated, not corrected.

## 3. Reported, not graded

- Per group: predicted f = M_d(<R500)/M_b(<R500) and the needed uniform f (b = 1 + f bringing the group's mean Delta to 0,
  bisection on [0, 30]), with their Spearman rank correlation versus kT. The sector's f-kT trend versus the needed one.
- X-COP: the sector's normalised profile M_d(<r)/M_d(<R500) against the gas-traced and star-traced normalised profiles (where
  it sits in NA2's band), cluster median per bin.
- iter_4's isolated-core reading of GX and GG.
- Bullet at v = 4700 km/s, and the Mach number v / c_s,d at each subcluster's centre (c_s^2 = 2 K rho_c).

## 4. Labels

- Per gate x cell x footing: PASS / FAIL / NO VERDICT (a known answer for that gate fails, or a MUTATE that must bite does not).
- A cell passes CE2 if every gate passes on both footings.
- **CANDIDATE** only if at least one cell passes CE2 AND KX1 (the EV1 session's KiDS systematics budget) reads KILL SOFTENS or
  NO POWER. If a cell passes and KX1 is not in, the label is "PASSES CE2, CANDIDATE PENDING KX1".
- **FAIL** otherwise, naming the blocking gates per cell and the size of each miss. KX1 cannot rescue a CE2 FAIL.

## 5. Known answers (a KA FAIL stops the grade of the gates it covers)

- KA1: iter_4's G2' Delta chi^2 at C1-C4 equals qx7_iter4.json "evaluated" to 1e-9; iter_4's K1 55.6403 reproduced.
- KA2: QX10 iter_2 static A at C1-C4, both footings: X-COP mean/rms, groups n_pass, G6 mean equal qx10_i2.json to 1e-9
  (same solver, exec'd read-only).
- KA3 (the law alone): f_cap = 0 gives X-COP mean +0.4675 / +0.4345 (QX2, iter_4 MUTATE 2) to 1e-3, and is compared with
  GB1's L0 X-COP mean (gb1.json; loaders may differ, disclosed if > 5e-3). The Bullet with no sector reproduces DB1/NA2's KA5:
  M300 1.112e14 / 7.337e13 to 1 %, dkappa -0.068 / -0.111 to 0.002.
- KA4: the fsigma8 machinery with R = 1 returns Rf = 1 to 1e-6 at every bin.

## 6. MUTATE (kd-style separate outputs ce2_MUTATE.*; each must bite)

- M1, no heating (the sector at cosmic density, never puffed): lambda_0 = 1e-3 Mpc, R = QX15's omega_d/omega_b (0.120940 /
  0.022358). The captured ratio f_cap R must equal KD1's 4.111 to 1e-3, and G5 or G6 (QX10's galaxy gates) must FAIL and the X-COP
  mean must be below -0.3 (KD1's -0.70 regime).
- M2, f_cap = 0: GX returns the law (KA3) and must FAIL.
- M3, heating too early: lambda_* x 10 at C1's p must FAIL GL or GF.

## 7. Outputs

ce2.py writes ce2.json / ce2.out (and ce2_MUTATE.*). RESULT.md: the gate x cell x footing table, the blocking gates, the
label. Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
