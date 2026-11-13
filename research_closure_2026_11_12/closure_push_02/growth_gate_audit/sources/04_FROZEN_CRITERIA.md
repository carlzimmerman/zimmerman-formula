# KD1 frozen criteria: the K(Q) dust with its amplitude unpinned, graded on every gate

Frozen before any KD1 script or KD1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane
that reopens v3s's K(Q) cold-dark-energy sector (owner 11-04 rule). It is never called dark matter, and there is no
particle. Both footings are graded separately and never pooled: canonical a0 9.3603e-11 m/s^2 with Lstar 21.7 pc, and
alt a0 1.1312e-10 m/s^2 with Lstar 22.9 pc. No new data and no downloads. Compute: one thread, under 1 GB.

## 0. Question

v3s carries 2 mu_K^2 (Q-1)^2 / (4K) (QX17 RESULT eq. A). Its FRW solution (Lean QX17B.frw_dust) is
rho = I0 (1 + w0/a^3) / (8 pi G a^3), with w0 = I0/(4 mu_K^2). Two numbers are free: I0, an integration constant
(the dust abundance), and mu_K, a constant of the action (CLOSURE 11-05: "free / initial condition"). Is there one
setting (I0, mu_K) that passes (i) CMB-lensing shape and growth, (ii) the hot-system gates (X-COP, groups,
ellipticals, Coma UDGs, dSph classes, KiDS split), and (iii) the gates that already pass (SPARC, the Solar System)?

## 1. Physics fixed before grading (from the record; not refitted)

- P1, the static term does not depend on I0. In the static weak field, delta rho_K = 2A delta Q with
  delta Q = -psi/c^2, which gives delta rho_K = -mu_K^2 psi/(4 pi G) (QX17 RESULT row "static, weak"; S4 section 1).
  I0 only sets the cosmic mean. The galaxy and cluster sides therefore depend on mu_K and on the CAPTURED mass,
  never on the linear static response with a zero point at infinity. That response would need (mu_K r)^2/3 times the
  baryon density, far more than the cosmic supply once mu_K r >> 1.
- P2, clustering. The sector is an n = 1 polytrope with a fixed physical Jeans wavenumber k_J = mu_K, and every
  self-gravitating hydrostatic core has radius R_c = pi/mu_K (QX3 D1-D3, Lean QX3_dust_eos). The flow is a
  khronon-gradient (irrotational) fluid. It has no vorticity, so no rotational support, and no coupling that ejects
  it (minimal coupling). Above the Jeans mass it falls into every well. It then settles into a central core of
  radius at most pi/mu_K, and baryons only compress it further. It is RETAINED by every host it falls into (the
  QX7/QX10 retention issue in its strongest form).
- P3, captured mass. Graded model "P" (QX3 G3, generous): a system with total baryons M_b,sys whose halo mass
  M_b,sys (omega_b + omega_d)/omega_b exceeds the Jeans mass at turnaround (QX3 g3: rho_ta = 5.55 rho_m0 (1+2)^3,
  M_J = (4 pi/3) rho_ta (pi/mu_K)^3) captures M_cap = f_cap (omega_d/omega_b) M_b,sys, with f_cap = 0.76 (X22).
  Profile: M_d(<r) = M_cap e(mu_K r), where e(xi) = (sin xi - xi cos xi)/pi for xi < pi and 1 beyond.
- P4, as a GB1 candidate "KD". b = 1 + M_d(<r)/M_b(<r), F = 1, T = 0. The dust sits inside the AQUAL operator as
  source mass, so g_pred = g_law(b g_N). Per-class M_b,sys and M_b(<r), from GB1's own features:
  - SPARC: M_b(<r) = feat Mb; M_b,sys from rrM (M = (r/rrM)^2 a0/G).
  - Ellipticals, X-COP, groups: the same rrM inversion (GB1 built rrM from each class's total baryons).
  - Coma UDGs and dSphs: M_b,sys = M* (feat Mb), M_b(<r_h) = M*/2 (the half-light convention GB1's x uses).
  - KiDS (lens radii >= 0.1 Mpc, isolated): M_b(<R) = M_b,sys, so b = 1 + M_cap/M_b,sys. Both colour bins get the
    same b. Declared here because GB1's KiDS features carry no M_b.
  - Solar System: b = 1. The Sun is not a separate collapse; it sits 8 kpc from the Milky Way's core of radius
    <= pi/mu_K. The linear static near-field term (mu_K r)^2/2 at Saturn is reported, not graded.
- P5, monotonicity (stated; the run checks it on its grid). For fixed I0, e(mu_K r) is non-decreasing in mu_K, and
  so is the captured set. Every static Delta is therefore non-decreasing in mu_K and in I0. A static gate that FAILS
  by over-prediction at mu_K fails for every larger mu_K.

## 2. The one fixed setting

- I0 (the amplitude) is fixed ONCE from one declared observable: the primary CMB TT/TE/EE likelihood fit on the
  framework's footing background (QX15 main fit, owner-approved PR4 CamSpec + ACT DR6). The values are QX15's
  theta.omega_d per footing (canonical 0.12094000633665247, alt 0.12092857774222121), with that fit's omega_b, n_s
  and tau, and h = 0.674 fixed by a0. Then I0 = 3 H0^2 Omega_d / c^2. Nothing downstream refits I0.
- mu_K enters no background observable at fixed I0 except through w0 and the Jeans scale. It is set to
  mu* = max(mu_B, mu_J): the smallest value the background (B1) and the CMB-lensing Jeans line (G9a) allow. By P5
  this is the setting most favourable to every static gate. It is the one point graded on G1-G8. No mu_K scan
  enters any static gate.
- Converse reading (reported, also graded as stated): at mu_gal = 0.1 Mpc^-1 (S4's isolated-galaxy guard) and at
  79.43 Mpc^-1 (QX3 G3's capture bound), B1 and G9a are evaluated, which shows by how much the CMB side fails where
  galaxies survive.

## 3. Gates (both footings; "passes" needs both)

| Row | Statistic | PASS line | Source |
|---|---|---|---|
| B1a cold at the CMB | w(z = 3400) = w0/(w0 + a^3) | <= 0.01 | QX3 G2 starts the dust CDM-like at z = 3400; QX15's PASS assumes a cold component |
| B1b BBN | stiff part rho_d0 w0 a^-6 over radiation (Omega_r h^2 = 2.47e-5 x (1 + 0.2271 x 3.046)) at T = 0.1 MeV (1+z = 1e5 eV / (k T_cmb), T_cmb 2.7255 K) | <= 0.067 (Delta N_eff <= 0.5, declared here; mu_B scales as line^-1/2) | the frw_dust solution is stiff (w -> 1) for a^3 < w0 |
| G9a CMB-lensing shape | QX3 iter2 machinery, read-only (CLASS, raw PR4 9 bandpowers, CMB-marginalised covariance, A_s refit): chi^2 at mu_K -> infinity on the footing background, then Delta chi^2(mu_K) from the Jeans growth ODE + Limber ratio | chi^2 <= 18.48 AND Delta chi^2 <= 4 | QX3 iter2 G1/G2 lines |
| G9b growth | no separate framework-native growth dataset is graded here; label from G9a's window, as QX3 ruled | as G9a | QX3 README |
| G1-G8 | GB1's battery, gate functions executed read-only, candidate KD at the fixed setting | GB1's lines | GB1 FROZEN_CRITERIA (e9464bc8ce) |

- mu_J = the smallest mu on the grid {0.1, 79.43} U logspace(0, 7, 36) above which every grid point has
  Delta chi^2 <= 4. mu_B is analytic from B1a and B1b.
- Reported, not graded: chi^2 with A_s fixed at QX15's primary value; the Jeans mass and the core radius at mu*; the
  linear near-field (mu_K r)^2/2 at the Cassini radius.
- Reported diagnostic, not graded and not a knob for any label: for each class, the uniform extra-mass fraction f
  (b = 1 + f at every point) that GB1's line allows (SPARC: the largest f with G1 PASS) or needs (hot classes: f
  bringing the class's mean residual to zero). The cosmic capture gives f_cap omega_d/omega_b to every class
  alike. If SPARC's f_max is below the hot classes' f_need, no amplitude of a universally captured sector serves
  both, whatever the CMB says.

## 4. Labels

- Per gate and footing: PASS / FAIL / NO VERDICT (GB1's missing-feature rule).
- **"one setting passes all gates"** only if B1a, B1b, G9a and G1-G8 all PASS on both footings at the one setting.
- Otherwise FAIL, with the blocking gates listed and the size of each miss (numbers, and the converse reading).
  A GB1 row that already fails for the plain law and is not moved inside its line counts as blocking.

## 5. Known answers (a KA FAIL means stop and fix; nothing is graded)

- KA1: GB1's L0 class means (KA20 dict) to 1e-6, and the UDG mean vs S1 to 1e-9, per footing.
- KA2: KD with I0 = 0 reproduces gb1.json's L0 numbers on G1-G8 to 1e-12 (same functions, same features).
- KA3: QX3 iter2 at corner (omega_b 0.0215, H0 65, n_s 0.95) with its omega_d_best: chi^2_min 8.570881 to 1e-3,
  Delta chi^2 at mu = 25118.86 equal to iter2.json's to 0.05, and mu_min = 25118.86.
- KA4: QX3's g3 at that corner gives mu_max = 79.43.

## 6. MUTATE twin (kd1.py --mutate, separate outputs kd1_MUTATE.*)

I0 -> 0 (omega_d = 1e-7, everything else the same). G9a must FAIL (chi^2 > 18.48) on both footings, and the
static rows must equal L0 (which fails G2). If G9a passes, the CMB gate has no power and G9a is NO VERDICT.

## 7. Outputs

kd1.py writes kd1.json / kd1.out. RESULT.md gives the gate x footing table, the fixed setting and how it was fixed,
and the plain label. Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
