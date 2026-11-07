# HC1 frozen criteria: one light thermal fermion with the a0 law, graded on every gate

EXPERIMENT. Adopts nothing; no-particle rule lifted for HC1 only (owner, 11-06, "both in parallel"). Kappa = 1/2
FITTED; not theory closed. Both footings, never pooled. No downloads, no new data, no LCDM parameter values. Frozen
and committed alone, before any HC1 script or HC1 number exists. One thread, under 1 GB, minutes. (The id HC1 is this
lane's; it is unrelated to the horizon_cluster_2026_11_05 records HC005-HC011.)

Footings: canonical a0 = 9.3603e-11 m/s^2, Lstar 21.7 pc; alt a0 = 1.1312e-10 m/s^2, Lstar 22.9 pc (GB1's values).

## 0. What the record already says (not repeated here)

- HF1 (56ab302a4d, A1 4e2a7564c5): a fermion with an abundance fitted per m to primary CMB fails gate 1 at 5 of 6 m.
  Gates 2-3, numbers only: X-COP +0.178 / +0.148 at m 11.8, a SHAPE miss (short inside, over outside); groups pushed
  BELOW the law (Z -5.6 to -5.9); SPARC safe because the Pauli cap keeps discs empty.
- VW1: the early-universe edge needs v0 < 4 km/s; SPARC's Upsilon floor needs v0 > 6.7-14.9 km/s. No window.
- What blocked HF1: its CMB channel (primary TT/TE/EE at plik) at the free-streaming velocities a 4-12 eV thermal-like
  fermion has, and a cluster profile shape no abundance scaling fixes. HF1 never ran GB1's battery (ellipticals, UDGs,
  dSph classes, KiDS split, Solar System) and never ran CMB lensing shape with the fermion.
- HC1 extends HF1 to the full GB1 battery plus CMB lensing shape, at one mass fixed in advance (section 1).

## 1. The fermion: mass fixed once, before grading

**Physical argument (declared).** A fermion with g_f = 2 that was in thermal equilibrium and decoupled while
relativistic, at the active-neutrino temperature T_nu = (4/11)^(1/3) T_cmb, has omega_f = m / 93.14 eV. HC1 asks this
fermion to carry the gravitating cold share the record's own CMB-lensing fit needs: QX3 iter2's G1 worst corner
(the background QX7/QX10 use), omega_d = 0.11958060485606123 at omega_b 0.0215, H0 65, n_s 0.95 (iter2.json).
Therefore

- **m = 93.14 eV x 0.11958060 = 11.1377 eV** (used at full precision), g_f = 2, T_f = T_nu (CLASS T_ncdm 0.71611),
  Fermi-Dirac spectrum. omega_f = 0.11958 is not fitted anywhere in HC1.
- Cosmic ratio R = omega_f / omega_b = 0.11958060 / 0.0215 = 5.5619 (the QX12 / QX7 R).
- Not a knob: m, g_f, T_f, omega_f, R are fixed here and used by every gate. No m grid. (HF1's m 11 and 11.8 cells
  bracket this m; its gate-1 FAIL at those cells is carried as context in section 5, not regraded.)

## 2. How the fermion enters the action (frozen rule)

- The fermion is a separate collisionless stress-energy. In the static weak field of v3s / AC2q the scalar sector is
  AQUAL, sourced by the TOTAL matter density. **Graded rule TOT:** g = g_law(g_N,b + g_N,f), with the a0 law acting on
  baryons plus fermion (HF1's rule; QUMOND = AQUAL in spherical symmetry with this nu). For a point with baryonic
  g_N = x a0 at radius r: Delta = log10[ g_law(x a0 + G M_f(<r)/r^2) / g_law(x a0) ].
- Reported only, never graded: rule BAR, g = g_law(g_N,b) + G M_f/r^2 (fermion Newtonian, law on baryons).
- Linear cosmology (G9): the fermion is a CLASS ncdm species; the a0 term is absent from linear FRW (stated liability,
  as HF1). WG1-WG6 already show the law's late boost gets the lensing shape wrong on its own.

## 3. The fermion's profile in each system (one rule, HF1 A1 R4, solver hf1_fermion.solve read-only)

rho_f(r) = min(rho_cap, rho_1 exp(-(Phi(r) - Phi(r_ta))/sigma^2)) inside r_ta, M_f(<r_ta) = R M_b,tot (fair share, an
upper bound on retention), M_f constant beyond r_ta. rho_cap = m^4 (g_f / 2h^3)(2 pi sigma^2)^(3/2) (Tremaine-Gunn,
Fermi-Dirac f_max). sigma^2 = V_max^2/2, V_max the highest circular speed of the self-consistent TOT model inside the
system radius R_sys. Phi from the TOT law field. Solved self-consistently (HF1's iteration).

- r_ta = (3 (1 + R) M_b,tot / (4 pi 5.55 rho_m0))^(1/3), CRG1's rta_com form with rho_m0 = (omega_b + omega_f) x
  2.775e11 Msun/Mpc^3 (h cancels), z = 0 for every system.
- Baryon profiles M_b(<r), from GB1's own loaders (QX5, QX16-fixed, read-only), per class:

| Class | M_b(<r) | M_b,tot | R_sys |
|---|---|---|---|
| SPARC (GB1 points, Upsilon 0.5/0.7) | v_b^2 r / G at the points, running max; r^2 inside the first point; constant beyond R_last | M_b(R_last) | R_last |
| X-COP (GB1's 35 points, 12 clusters) | log-log interpolation through the cluster's points and Mb_last; slope of the first pair inside; constant beyond Mb_last's radius | Mb_last | Mb_last's radius |
| groups (f* = 0 and 1 graded) | power law through (R2500, M_b) and (R500, M_b); constant beyond R500 | M_b(R500) | R500 |
| ellipticals | QX5's Mbar(r) | Mbar(1e9 kpc) | 8 Re |
| Coma UDGs | Hernquist, M* total, half-mass radius r_h = 4/3 Re | M* | r_h |
| dSphs (LW1/X1 rows) | Hernquist, M* total, half-mass radius r_h | M* | r_h |
| KiDS bins (early, late) | Hernquist, a = R_med/20, normalised so M_b(<R_med) = g_bar R_med^2 / G | that normalisation / (20/21)^2 | R_med |
| Solar System | the Sun; fermion = uniform local density at the Milky Way cap, rho_cap(220/sqrt 2 km/s), g_f = (4 pi/3) G rho r | n/a | n/a |

- The KiDS profile (a = R_med/20) and the Solar-System cap density are readings, declared here. The UDG and dSph
  isolated solves ignore the host's fermion sea; section 4's bound readings add it.

## 4. Gates (GB1's battery, executed read-only, plus G9)

G1-G8 are GB1's rows, statistics, lines and data exactly (FROZEN_CRITERIA e9464bc8ce; gb1.py exec'd read-only up to
its main block). The HC1 candidate is a direct-Delta candidate (section 2) with M_f(<r) attached per point from
section 3. GB1's G8 converts Delta to F_SS with its frozen convention. G6's anchor is SPARC's mean residual under HC1.

| Row | Line (GB1 unless stated) |
|---|---|
| G1 SPARC | \|Z\| <= 0.057 AND rms <= rms(L0) + 0.010. This row is "not retained by discs" |
| G2 X-COP | \|mean\| <= 0.05 AND rms <= 0.10 |
| G3 groups | >= 16 of 20 within 2 sigma_log, for f* = 0 AND f* = 1 |
| G4 ellipticals | \|mean\| <= 0.15 |
| G5 Coma UDGs | \|mean\| <= 2 sigma_U |
| G6 dSph classes | bright M31, MW classical, LG field: each 95 % CI of (median residual - SPARC anchor) contains 0 |
| G7 KiDS split | \|R\| < 2 sigma_tot |
| G8 Solar System | GB1's planet and Cassini uses <= 1 |
| **G9 CMB lensing shape** | QX3 iter2's G1 statistic exactly (cfg917_lib, raw PR4 lensing, 9 bandpowers L 8-400; A_s fitted analytically; 8 corners omega_b {0.0215, 0.0230} x H0 {65, 75} x n_s {0.95, 0.98}; tau 0.06; N_ur 3.046; T_cmb 2.7255). The dust is replaced by this fermion: omega_cdm = 0, one ncdm species, m = 11.1377 eV, T_ncdm 0.71611, deg 1. Nothing but A_s is fitted. PASS if the worst corner's chi^2 <= 18.48 |

**Bound readings (reported, never replace a graded cell).** For the classes where the fermion may be too SCARCE:
- UDGs: M_f,max(<r_h) = (4 pi/3) r_h^3 [34 rho_cap(max(sigma_obs, sigma_model)) + rho_amb], where 34 x is twice the
  fully degenerate relic bound m^4 (g_f/2h^3)(4 pi/3) v_esc^3 at v_esc = 4 sigma (17 x the cap): a generous ceiling, and rho_amb <= 3 g_e / (4 pi G d_mean), g_e = g_law(x_e a0) (S1's x_e_dmean,
  d_mean): Coma's mean interior TOTAL density, an upper bound on its fermion sea at the UDG.
- dSphs: the same own-cap term, plus rho_amb = 34 rho_cap(host sigma) for MW (220/sqrt 2) and M31 (250/sqrt 2)
  satellites; LG field none.
- Rule BAR on every row, reported.

## 5. Carried, not regraded

- Primary CMB (TT/TE/EE): HF1's FD cells at m 11 and 11.8 fail at p ~ 1e-69 (plik 1599, 1432 / 605). Different
  temperature (HF1 fits omega_f per m), so carried as context only.
- Lyman-alpha forest, Milky Way K_z, IC 1613, Bullet offsets: not graded here (HF1 / VW1 / record).

## 6. Known answers (any KA FAIL: stop, nothing graded)

- KA1: with the fermion off (R = 0), the HC1 harness reproduces GB1's L0 graded numbers (gb1.json) on G1-G8, both
  footings, to 1e-9.
- KA2: HF1's own pipeline (hf1_g23.xcop_rows, read-only, caches redirected into HC1) at m 11.8, omega_f/omega_b from
  hf1_g1_results.json, reproduces HF1's X-COP all mean and rms (hf1_g23_RUN_m11p8.json) to 1e-6, both footings.
- KA3: Tremaine-Gunn closed form: rho_cap(tg_mmin(sigma, r0), sigma) / rho_0 = 1 to 1e-10 (HF1's K_TG).
- KA4: every HC1 solve: rho <= cap x (1 + 1e-9); M_f(r_ta) = R M_b,tot within 1 % wherever the cap does not bind.
  Convergence is reported per class; if more than 5 % of a class's systems fail to converge, that gate is NO VERDICT.
- KA5 (G9): QX3 iter2's corner (0.0215, 65, 0.95) dust chi^2 8.5709 and baryons-only 895.33 reproduce to 1e-3; CLASS
  returns omega_ncdm = 0.11958 within 1 % at m 11.1377 eV.

## 7. MUTATE twins (separate outputs, *_MUTATE.*)

- hc1.py --mutate: M1 planted cold retention, cap x 1e4 (a phase-space-unlimited, CDM-like species, same R): must FAIL
  G1 on both footings (the battery can see disc retention). M2 law off (Newton + fermion): must FAIL G1. If either
  does not bite, the run says NO POWER on G1.
- hc1_g9.py --mutate: baryons only (no fermion), A_s refit: must give chi^2 > 18.48 at every corner.

## 8. Labels

- **PASSES ALL GATES**: PASS on G1-G9 on both footings.
- Otherwise **FAILS**, listing every blocking gate and footing with its distance from the line (statistic minus line,
  in the row's own units, and sigma where the row has one). NO VERDICT rows are listed as such.
- RESULT.md also gives: the fixed mass and how it was fixed; where the fermion sits (M_f / M_b at the graded radii,
  per class); the free-streaming scale (reported); the bound readings; rule BAR.

Any change after this freeze is disclosed in RESULT.md as post-freeze. Kappa = 1/2 FITTED; not theory closed.
