# MK1 frozen criteria: one dust constant mu_K for the CMB, clusters and galaxies, with form B's cap (2026-11-10)

Committed alone, before any script or graded number of this lane. TEST lane, quarantined. Adopts nothing, relabels
nothing, registers nothing. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), never pooled. The cold
component is cold dark energy (the khronon's K(Q) dust), never a particle. Not a LCDM lane. This lane grades the
quadratic K(Q) = mu_K^2 (Q - 1)^2 of action (A) (PAPER70; QX17); it designs no new K(Q).

## 0. The question

In action (A) read as form B (`closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`), is there ONE value of
mu_K (physical, per Mpc) that the CMB, clusters and galaxies all allow, once the total clock charge around a galaxy is
capped by its conserved share? Each row below returns an interval of mu_K per footing (or NOT EVALUABLE with the reason).

## 1. Physics fixed before any number

- FRW (QX17 limits table, K4): w(a) = w0 / (w0 + a^3), w0 = I0 / (4 mu_K^2), I0 = 3 H0^2 Omega_d / c^2. The component is
  dust plus a stiff partner rho_d0 w0 a^-6; it turns dust-like (w = 1/2) at a^3 = w0, i.e. 1 + z_d = (4 mu_K^2 / I0)^(1/3).
- Static weak field, gamma_L = 0 (QX17 limits table): div[mu(|grad Phi|/a0) grad Phi] + mu_K^2 Phi = 4 pi G rho_b. So the
  static dust is delta rho_K = -mu_K^2 Phi / (4 pi G) (Phi relative to the cosmic background, Phi -> 0 far away), and it is a
  SOURCE of the law: in spherical symmetry r^2 mu(g/a0) g = G [M_b(r) + M_K(r)], M_K(r) = -(mu_K^2/G) Int_0^r Phi r'^2 dr'.
  The lensing (and dynamical) mass is M_L = (M_b + M_K) nu(G (M_b + M_K) / (r^2 a0)). Call this the ACTION-EXACT form.
  QX2 iteration 5 used M_model = law(M_b) + M_K (the dust not boosted by the law). That is called the ADDITIVE form here;
  it is used for the known answer and reported beside, never as the graded form.
- Form B's cap (ONE1's construction, PD1's share X = 59.486 / 59.503 M_b from `fable52_push/ONE1_counted_once/one1.json`):
  the total clock charge around a galaxy, C(r) = M_L(r) - M_b (law's halo plus static dust), ends at r_c where
  C(r_c) = X M_b. Beyond r_c, M_L = (1 + X) M_b and Phi = -G (1 + X) M_b / r. Inside, Phi is continuous with
  dPhi/dr = G M_L / r^2, and the dust is computed from that Phi self-consistently (shooting on the potential's central
  offset). If no self-consistent capped state exists at some (mu_K, M_b), that value FAILS the row for that lens set.
- Uncapped reading (the old bound, and MUTATE M-NOCAP): the law with no end plus the dust, with S4's zero point (VSZ's
  lambda_max(mu_K, r_M) imposed on the mu_K = 0 solution at 3 Mpc, S4's `zero_point`), integrated outward to 30 Mpc with
  M_L constant beyond (S4's r_max), the sign rule of S4's solver for M_b + M_K < 0.

## 2. Rows, gates and lines (each taken from the lane named; frozen here)

| row | quantity | gate and line | source lane |
|---|---|---|---|
| 1 CMB and background | lower bound from w(a) | **B1a: w(z = 3400) <= 0.01**, I0 per footing from kd1.json (QX15's omega_d, h 0.674). Interval [mu_B1a, inf). Reported beside, not graded: B1b BBN (stiff part <= 0.067 of radiation at T 0.1 MeV), w at z 1100 and z_d per mu_K | KD1 (B1a/B1b), QX17 |
| 2 clustering scale | lower bound from the Jeans scale | **G9a CMB-lensing Jeans line: mu_K >= mu_J** (kd1.json per footing; QX3 iter2 machinery, Delta chi^2 <= 4). Reported beside: QX3 G2's worst bracket corner (4.0e4); the comoving Jeans wavenumber mu_K/(1+z); the sound speed c_s^2 = 4 pi G rho_d / mu_K^2 at the mean density from z 3400 to 0; the growth and forest scales as closed-form stand-ins | KD1 G9a, QX3 iter2 |
| 3 X-COP | interval passing G-X | QX2's builder (7 clusters, 35 points, 0.1-0.7 R500); **G-X: \|mean Delta\| <= 0.05 and rms <= 0.10**, Delta = log10(M_HSE / M_model). Graded model: ACTION-EXACT with Phi = the potential of the measured M_HSE, zero at 3 R200 (QX2's psi_profile = QX6's back-reaction, exact for any passing model). Grid: mu_K = 1e-3 to 1e4, 0.01 dex (QX6's). Reported: ADDITIVE form; zero at 10 R200 | QX2 iter 5, QX6 iter 1 |
| 4 groups | interval passing the group gate | Lovisari 2015, 20 groups, R2500 and R500 (QX5's `groups()`); M_b = Mgas (1 + s), s in [0, 1] (stars bracket); **PASS iff the bracket of mean Delta overlaps [-0.05, 0.05]**. Phi = potential of M_HSE(r), a power law through the two measured points, extended inward and outward with the same power, zero at 3 R200 with R200 = 1.5 R500 (QX2's fallback). Graded model ACTION-EXACT; ADDITIVE reported. Same grid as row 3. Beside (reported, one-sided, not graded): RB1's conservation reading, charge (M_model - M_b) / (5.41 M_b) at R500, median over groups | QX5, RB1 |
| 5 SPARC | upper bound | QX8's grader and line: **rms <= 0.110 and median U in [0.50, 0.80]**, QX8's exact-field T per point plus the dust's T_K = log10[g_law(g_bar + G M_K(<r)/r^2) / g_law(g_bar)] at every point and U (spherical dust, algebraic law; QX8's T carries the exact field). Phi per galaxy and U: data law field inside the last point, and outside it the capped point-mass solution with the dust (this lane's solver, M_b = r_last^2 g_bar(r_last)/G, X = PD1's share), three iterations of the dust's own feedback inside. Grid 0.01 to 1e4 per Mpc, 0.05 dex. Upper bound = the largest grid value such that it and every smaller grid value pass. Reported: QX6's recheck line (rms rise <= 0.01, mean shift <= 0.02 against QX8 at mu_K = 0); the uncapped Phi | QX8 |
| 6 KiDS host-free, capped | upper bound | ONE1's frozen statistic and gate unchanged: KO1 host-free lenses at the **1.6 R_h veto**, KO1 tie rule, R_s = A(outer)/A(inner), k fitted on the inner window (refitted per jackknife), neighbours carrying the same capped profile (exact annulus kernel, five shuffles subtracted); **G-K1 all / late / early \|diff\| <= 2 sigma; G-K2 all profile chi^2 <= 9.49; G-K3 early - late within 2 sigma**. Own halo and every neighbour: the capped dust-included profile at its own m = mu_K r_M(k M_b). Grid: 0.03, 0.1, 0.3, 1, 3, 10 per Mpc, then two log-midpoints between the last pass and the first fail (refined once more if they straddle). Upper bound as in row 5. Reported (and the old bound): the uncapped reading through the same machinery, own halo only, no neighbours (as ONE1's "law with no end" reading), same grid | ONE1 (criteria a967a38851, A1, A2) |
| 7 Solar System | upper bound | EW2 iter4's `cassini`: static dust at the Sun, dg = mu^2 G M_sun / 2 + mu^2 Phi0 R_Saturn / 3 <= **7.0e-15 m/s^2** and Q2 = mu^2 Phi0 / 3 <= **9.0e-27 s^-2**, Phi0 = (600 km/s)^2. Closed form. Reported: the same with a capped Milky Way potential | EW2 iter4 |
| 8 consistency | reported, not graded | (a) per log M_b in {8, 9, 10, 11, 12} (galaxies, X = PD1's share) and {13, 14} (groups/clusters, share 5.41): the mu_K above which the static dust alone, on the dust-free capped potential, integrated to r_c, exceeds the share. (b) SCS1's closed form omega^2 = K G [(1 - K m) k^2 - mu_K^2] / (mu_K^2 + K m k^2), G = n_d + D.P: modes with k < mu_K / sqrt(1 - K m) grow; read at each row's bound as mu_K r for r = 30 kpc, r_c, 1 Mpc, 0.1 kpc; SCS1's labels (STABLE at 0 and 0.1 per Mpc, JEANS-ONLY at 8.9e6) quoted | SCS1 |

Row 1's machinery note (stated before any number): the record's primary-CMB gate (F1A machinery, PJ1's CamSpec-2500
reader, as WD1 G7 ran it) carries a smooth c_s^2 = 1 component through CAMB's tabulated-w dark-energy fluid with Lambda.
The stiff partner can be written that way, but it exceeds radiation for a < a_x = (Omega_d w0 / Omega_r)^(1/2), which for
every mu_K below about 1e7 per Mpc lies inside the radiation era where CAMB sets its adiabatic initial conditions on a
radiation-dominated background. The machinery therefore cannot take this w(a) without changing its early-time set-up,
which this lane does not do. Row 1 is graded on KD1's B1a line instead, and its quality is stated as "background line,
not a likelihood". a_x is printed per mu_K.

## 3. Label (per footing, frozen before any number)

- L = the largest lower end over rows 1-7; U = the smallest upper end over rows 1-7. A row whose set is empty makes the
  intersection empty.
- **ONE VALUE EXISTS [L, U]** if every row is non-empty and L <= U.
- **NO VALUE** otherwise. The label names the rows whose sets do not meet and the factor L / U between the binding pair
  (for an empty row: its closest miss, the mu_K of its minimum rms and that rms against its line). If NO VALUE, one plain
  sentence on what a dust term would have to do differently at high and low clock offset; a requirement only.
- **NO VERDICT** if any known answer below fails.
- **Does the answer turn on the cap?** The label is recomputed with rows 5 and 6 on their uncapped readings. If that
  changes the label, the first lines of RESULT.md say so.

## 4. Known answers (all must pass, else NO VERDICT)

- KA1 QX2 iter 5 (ADDITIVE, zero at 3 R200): mean at mu_K 0.1 = +0.4644 / +0.4317 (|d| <= 1e-3); mean-zero mu_K
  1.778 / 1.736 (|d| <= 0.01).
- KA2 ONE1 at mu_K = 0 through this lane's generalized tables and kernel: at 1.6 R_h (primary, neighbours) z all / late /
  early -1.141 / -1.459 / -0.651 canonical, -0.232 / -1.231 / +0.214 alt (|d| <= 0.02); model R_s all 1.003 / 0.847
  (|d| <= 0.005); chi^2 1.915 / 0.868 (|d| <= 0.1).
- KA3 QX8 at mu_K = 0 through this lane's regrade: exact-field rms 0.0560 @ 0.58 / 0.0558 @ 0.52 (rms |d| <= 1e-4, U equal).
- KA4 FB1's arithmetic: I0 / 4 at H0 70, Omega_c 0.26 = 1.063e-8 Mpc^-2 (|rel| <= 1e-3).
- KA5 the solver's static-dust enclosed mass against a direct quadrature of -mu^2 Phi r^2 / G on its own Phi (rel 1e-5),
  and against the deep-law closed form M_K(<r) = (mu^2/G)[|Phi_c| r^3/3 + s (r^3/3 ln(r_c/r) + r^3/9)] (Lean) on a pure
  deep-law test field (rel 1e-4).
- KA6 the capped profile at m -> 0 equals ONE1's truncated halo: own-halo ratio table against ONE1's rho_tab(X) (max
  |d| <= 1e-3 on u 0.3-1000); neighbour kernel table against ONE1's build_H(X) (max |d| <= 1e-3).
- KA7 KD1's mu_B1a reproduced from the closed form (198.254 canonical; rel 1e-6).
- KA8 EW2's Saturn number: dg_total at mu_K 2.04e4 = 7.5e-14 (rel 2 %).
- KA9 QX5's group baseline at mu_K = 0 (ACTION-EXACT = ADDITIVE there): bracket [+0.196, +0.359] / [+0.158, +0.320]
  (|d| <= 2e-3).
- KA10 S4's zero point: the mu_K = 0 solution meets Phi(3 Mpc) = -GM/R + s (lambda + ln(R/r_M)) (rel 1e-6).

## 5. MUTATE (separate outputs `*_MUTATE.*`; each must move an interval, shown; any that does not is disclosed)

- M-NOCAP: row 6 (and row 5) without the cap.
- M-2X: the share doubled (X -> 2X) in rows 5, 6 and 8.
- M-SIGN: the static dust's sign flipped (delta rho_K = +mu_K^2 Phi / (4 pi G)) in rows 3, 5 and 6.
"Moves" means an endpoint changes by at least one grid step, or a row turns empty / non-empty.

## 6. Lean (`fable_independent_2026/lean_2026/MK1.lean` + `MK1_MUTATE.lean`)

Closed forms: w0 and w(a), the turn-over a^3 = w0, w strictly decreasing in mu_K; FB1's I0/4 arithmetic bounds; the
deep-law static dust's enclosed mass (derivative identity) and its monotonicity in mu_K; the cap radius with dust in the
deep limit, x_c = (1 + X)/sqrt(1 + kappa), decreasing in kappa; the Saturn anomaly increasing in mu_K; the no-window step
(L > U gives no mu in both). The twin states false versions (w increasing in mu_K, x_c increasing in kappa, the wrong
dust constant, a window that exists) and must fail to compile.

## 7. Scope and rules

Statics, spherical symmetry (except the KiDS projection), the quadratic K(Q) only. The collapse (COL1's lane) is not
touched. Compute: one thread, under about 1.5 GB, preemptible; no downloads; data read in place. Files end
"kappa = 1/2 FITTED; not theory closed. Adopts nothing."

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
