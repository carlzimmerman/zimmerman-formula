# KQ1 frozen criteria: can K(Q) dust under v3s + blend form NC4's cored cluster profile at X-COP masses?

Frozen before any KQ1 script or KQ1 number exists. TEST lane on the F1-CONFIRMED branch (F1A 7026dcb48e: the CMB needs a
cold component, omega_d/omega_b 5.410 / 5.412). Adopts nothing. Kappa = 1/2 FITTED; not theory closed. The component is
"cold dark energy" (v3s's K(Q) dust); there is no particle. Both footings, never pooled: canonical a0 9.3603e-11 m/s^2,
Lstar 21.7 pc; alt a0 1.1312e-10 m/s^2, Lstar 22.9 pc (Lstar enters no cluster number here). No downloads, no LCDM
inputs, no QX3 iter2 lensing number used for any line (the CMB-lensing mu_J is quoted from GL1 only as context).
Compute: one thread, under 1 GB RSS, SIGTERM checkpoint, peak RSS reported.

## 0. Question

The full-action candidate is v3s plus its K(Q) dust sector, with the adopted Pi^6 blend stiffness (owner decision
71e4014cd5, b = rho_DE). Its galaxy capture is the stated open failure (KD1 c4008a456c: f_cap omega_d/omega_b = 4.111 /
4.112 given to every captured system, against SPARC's cap 0.3257 / 0.1937). NC4 (d16b3185b3) found the cluster target: a
cored isothermal rho ~ (1 + (r/r_c)^2)^-1 with r_c 50-100 kpc, flat inside 20 kpc (NC3 39940c070e), concentration
M(<0.25 R500)/M(<0.7 R500) 0.248-0.266 for r_c 100, passing NA2's per-bin rule (rms 0.086 / 0.086 fitted; 0.091 / 0.091 at
the f-table amount). Can the K(Q) dust, in hydrostatic equilibrium in the law's field of X-COP baryons plus itself, form
that core, and at what mu_K?

## 1. Physics and conventions (from the record; nothing refitted)

- K(Q) term 2 mu_K^2 (Q - 1)^2 / (4K) (QX17 eq. A); static weak field delta rho_K = -mu_K^2 psi / (4 pi G) (KD1 P1).
  The dust is an n = 1 polytrope with fixed physical Jeans wavenumber k_J = mu_K (QX3 D1-D3, Lean QX3_dust_eos): c_s^2 =
  4 pi G rho / mu_K^2; a self-gravitating Newtonian core has radius pi / mu_K. mu_K is in Mpc^-1 (physical).
  QX7's lambda_0 = 2 pi / mu_K. X14 (c23149c508): q_K = sqrt(M_theta) mu_K l; K(Q) is inert at the fold scale for every
  S4-allowed mu_K (q_K <= 0.017 / 0.016 at mu_K 0.1, l <= 156 kpc); q_K is reported at the mu_K KQ1 needs.
- Hydrostatic equilibrium (the record's own solver, QX7 iter_5 `profile`, executed read-only from its source via NA2's
  prefix): d rho/dr = -(mu_K^2 / 4 pi G) g_law(G (M_b(<r) + M_d(<r)) / r^2), dM_d/dr = 4 pi r^2 rho, rho_c shot to the
  total; surface r_s where rho = 0. g_law is the a0 law (simple nu, GB1's glaw); in the static spherical cluster interior
  the blend reduces to it (BL3 PASS, 3D spherical, scoped). M_b(<r) = X-COP gas + stars (iter_5 XPROF: power law inward,
  constant beyond the last data radius tl).
- Amount: the total equilibrium mass per cluster = F_X Mlast with F_X = KD1's X-COP need 4.1786 (canonical) / 3.7833 (alt)
  from kd1.json uniform_f_diag. Bracket (reported): M_d(<tl) = F_X Mlast (NA2 install convention). Retention follows
  iter_5: the cluster keeps the dust only if r_s < r_ta0(M_b,tot).
- Bounds compared (units Mpc^-1, physical; sources):
  - BBN side mu_K >= 8.89e6 (8.890e6 / 8.889e6): KD1 B1b, frw_dust stiff phase rho_d0 w0 a^-6 <= 0.067 of radiation at
    T = 0.1 MeV (Delta N_eff <= 0.5), w0 = I0/(4 mu_K^2), I0 = 4.037e-8 Mpc^-2 from QX15 omega_d; kernel-free (GL1 4699adbbd7).
  - Galaxy side mu_K <= 79.43: QX3 g3 capture bound (Jeans mass at turnaround vs galaxies; KD1 KA4); S4's isolated-galaxy
    guard 0.1. Reported alongside: QX7 iter_5's host-held galaxy gates pass only at lambda_0 >= 10 Mpc (mu_K <= 0.63).
  - Reported only: GL1's corrected CMB-lensing Jeans line mu_J = 631.

## 2. Grid

mu_K in {logspace(-1, 4, 26)} U {79.43, 631}, both footings, all 7 X-COP clusters (A1795, A2029, A2142, A2319, A644, A85,
ZW1215). Pre-stated refinement: 4 log-spaced points between the two grid neighbours of the mu_K with the smallest
number of failed lines (ties: smaller per-bin rms at need), per footing. No other scan.

## 3. Lines (each per footing; "every cluster" means all 7)

- L1 core: r_1/2, the radius where rho = rho(0)/2 (rho(0) at the solver's innermost point), in [49.5, 100.5] kpc for every
  cluster (the cored isothermal's r_c is its r_1/2).
- L2 flat: max |d ln rho / d ln r| over r <= 20 kpc <= 0.5 for every cluster (NC3 core rule).
- L3 concentration: c = M_d(<0.25 R500) / M_d(<0.7 R500) in [0.2475, 0.2665] for every cluster (primary, the stated
  0.248-0.266 at its rounding). Secondary line, stated now: c in [0.21, 0.30] (NA2's HSE band) for every cluster; it gives
  a secondary label reading, reported, not the label.
- L4 per-bin (NA2's rule at the need amount): X-COP points (iter_5 XC), Delta = log10(M_obs / M_pred), M_pred =
  g_law(G (M_b + M_d) / r^2) r^2 / G; rms <= 0.10 and every bin (r/R500 edges 0, 0.25, 0.5, 0.75, 1, 2; n >= 3) |mean|
  <= 0.10 (the inner bin included). NA2's full gate (also |mean| <= 0.05) reported.
- L5 amount: the need amount F_X is present, i.e. the dust is retained (r_s < r_ta0) in every cluster.

## 4. Labels

- **FORMS CORE (scoped)**, with mu_K, if L1-L5 all pass on both footings at one mu_K <= 79.43 (inside the galaxy window;
  the BBN comparison is stated).
- **FORMS CORE, mu_K EXCLUDED** if they all pass on both footings only at mu_K in (79.43, 8.89e6), outside both windows.
- **CANNOT FORM CORE** if no grid or refined mu_K passes L1-L5 on both footings. Then the closest profile is reported:
  the mu_K with the fewest failed lines (ties: smallest per-bin rms), per footing, with every line's margin; also the
  mu_K whose median r_1/2 is nearest 75 kpc, and the best fitted-amount rms (amount free, reported only).
- **NO VERDICT** if a KA fails, a MUTATE twin fails to bite/hold, or the solver fails on any graded cell.
- Every row carries the galaxy-capture cost: KD1 capture 4.111 / 4.112 vs SPARC cap 0.3257 / 0.1937. Reported per mu_K:
  KD1's model P at that mu_K (Jeans mass at turnaround M_J(mu_K) from KD1's mj_of; the number of SPARC galaxies that
  capture; GB1 G1 SPARC status with KD1's own KD candidate at that mu_K), and iter_5's recorded host-held galaxy gates at
  lambda_0 = 2 pi / mu_K (nearest recorded). The statement "does the core mu_K change the capture" is read from these.

## 5. Known answers (a KA FAIL means stop; nothing graded)

- KA1 law alone: my L4 evaluator with M_d = 0 gives X-COP mean 0.467499 / 0.434523 (GB1 L0, KA20) to 1e-6, and NA2's
  x_eval at F = 0 equals it.
- KA2 KD1 reproduced: KD1's f-table (X 4.1786 / 3.7833, capture 4.1110 / 4.1121) to 1e-4; KD1's KD candidate at mu* (kd1.json)
  through GB1's g_xcop gives kd1.json's G2 mean / rms (-0.70286 / 0.80268; -0.71439 / 0.80949) to 1e-6.
- KA3 solver: host off, law off reproduces the isolated core r_s = pi / mu_K to 1e-5; iter_5's recorded X-COP at
  lambda_0 3.162 (total f_cap R Mlast) mean / rms +0.0334 / 0.2293 (canonical), -0.0019 / 0.2249 (alt) to 2e-3.
- KA4 line calculators on the analytic cored isothermal r_c 100 kpc: r_1/2 = 100 kpc to 0.5, slope at 20 kpc -0.077 to 0.005.

## 6. MUTATE twin (kq1.py --mutate; outputs kq1_MUTATE.json / kq1_MUTATE.out)

- M1 mu_K -> infinity (mu* = 8.89e6 and 1e9): the solver's enclosed fraction is 1 at every X-COP radius, so KD1's model P
  with that fraction gives KD1's cusp, G2 mean -0.703 / -0.714 to 1e-6, and L1 FAILS (r_1/2 < 1 kpc). Must bite.
- M2 law alone (M_d = 0): GB1 L0 means 0.467499 / 0.434523, and L4 FAILS. Must bite.
- M3 planted core: NC4's cored isothermal r_c 100 kpc at the need amount (NA2 install) must pass L1-L4 on both footings
  (shows the lines can pass). If it fails, the lines are mis-built: NO VERDICT.

## 7. Expected outcome (honest, before any number)

CANNOT FORM CORE. iter_5 already found the host-held n = 1 dust at lambda_0 1.5-8 Mpc never brings X-COP below rms 0.225
(inner short, outer over). The n = 1 equilibrium in a law field g ~ 1/r has rho ~ ln(r_s / r), not r^-2, so I expect
that a mu_K giving r_1/2 50-100 kpc puts nearly all the dust inside 0.25 R500 (c near 1, inner bin over-filled), while
a mu_K giving c ~ 0.25 has r_1/2 of hundreds of kpc. Expected closest miss: per-bin rms >= 0.2 and L1 or L3 failing, on
both footings. If anything forms, I expect it to need mu_K ~ 10-100 Mpc^-1: far below the BBN bound 8.89e6 and near or
above the galaxy bound 79, so the capture problem (4.11 in every system above M_J) would remain.

## 8. Outputs

kq1.py -> kq1.json / kq1.out; kq1.py --mutate -> kq1_MUTATE.json / kq1_MUTATE.out; RESULT.md. Read-only use of iter_5,
NA2, NC4, KD1, GB1, QX3 (constants only). Post-freeze changes are committed as amendments before the rerun, disclosed.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
