# SE1 frozen criteria: the shock-entropy sector at action level (the last physics class)

Frozen before any SE1 script or SE1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane
specified by closure_2026_11_06/HANDOFF_FIELD_EQUATIONS_CHAT_2026_11_06.md, "Lane SE1" (SEED_2026_11_06.md wins where
they differ). The sector is part of the khronon (cold-dark-energy) sector: no particle of any kind. Both footings, graded
separately and never pooled: canonical a0 = 9.3603e-11 m/s^2, Lstar 21.7 pc; alt a0 = 1.1312e-10 m/s^2, Lstar 22.9 pc.
Raw data or framework-native inputs only; no LCDM inputs. No downloads (a row that needs one is NO VERDICT and the file
is listed). Compute: one thread, under 1 GB, checkpointed if over a few minutes.

## 0. What already exists and what SE1 adds

EN1 (eae8892550 / 743a2f4548) graded a FIELD-EQUATION statement: sigma = the gas adiabat with cooling off, an extra
mass per baryon g(sigma). It FAILS G2 and G3 on a measured radial reversal (need falls outward, K rises). SE1 is the
ACTION-level version: entropy s per unit of the SECTOR's own rest mass, carried by the sector's own flow, with the
sector's own shocks as the only source. EN1's numbers enter as a known answer (KA4) where the setup matches.

## 1. The action (one family, two arms)

On top of QX17's Legendre-form action (A) (QX17 RESULT section 0), replace the K(Q) term 2 mu_K^2 (Q-1)^2/(4K) by

    L_x = F(Q, s) + zeta n^m d_m s ,

with zeta a Lagrange multiplier, Q, n^m as in QX17 section 1 (the sector moves along the khronon normal), s a scalar.
Everything else in (A) (W, P, stiffness, lambda, matter) is unchanged, so the a0 law is unchanged.
- **Arm (a):** F = (mu_K^2/2K) g(s) (Q - 1)^2, g(0) = 0, g >= 0 non-decreasing. g constant reproduces v3s's K(Q) term.
- **Arm (b):** F = p(Q, s) of a gamma = 5/3 ideal fluid written in its enthalpy per unit rest mass h = Q:
  F = K_s(s)^(-3/2) [ (2/5)(Q - 1) ]^(5/2), K_s(s) = K_0 exp(2 (s - s_0)/3) (s in units of k_B per c_v unit of
  rest mass; K_s raised by entropy, the thermodynamic direction). K_0 (primordial adiabat) is the arm's one constant.
- Rest-mass (charge) density rho_0 = dF/dQ, energy density Q dF/dQ - F, pressure F.

**Field equations predicted before the check (sympy will confirm or refute each):**
- (S1) zeta: n^m d_m s = 0 in smooth flow.
- (S2) s: dF/ds = nabla_m (zeta n^m).
- (S3) tau (conserved khronon current, QX17's P/lambda current added unchanged):
  nabla_m [ F_Q n^m - (zeta/Q) D^m s + (QX17 E3 current with its rho_Q's K(Q) piece removed) ] = 0.
- (S4) stress: T^F_mn = g_mn F + Q F_Q n_m n_n; T^zeta_mn = g_mn zeta (n.ds) - 2 zeta n_(m d_n) s - zeta (n.ds) n_m n_n,
  on shell (S1) T^zeta_mn = -2 zeta n_(m D_n) s. Energy density on shell: Q F_Q - F.
- (S5) static reduction (Theorem K, predicted): for a static metric and tau = c_tau t, Q = c_tau/N with ONE global
  c_tau (tau is continuous across a stationary shock), and (S2) gives d_t zeta = N F_s, so zeta grows linearly in t
  and T^zeta_0i = zeta N D_i s grows unless D_i s = 0 wherever F_s != 0. So a static sector is isentropic on each
  connected region and its density is rho_0 = F_Q(c_tau/N, s): open contact with the cosmic chemical potential.
  Equivalently (Carter-Lichnerowicz / Crocco): the sector's momentum per unit rest mass is a pure gradient,
  Q n_m = -d_m tau, so a static stratified (non-isentropic) khronon fluid does not exist.

**Shocks.** Entropy production is not in an action. The action gives the smooth equations; shocks are the conservative
weak solutions of (S3) + nabla^m T_mn = 0 (rest mass and energy-momentum conserved across the surface), and Sigma >= 0
(nabla_m (rho_0 s u^m) = Sigma) is their admissibility condition, Sigma = the Rankine-Hugoniot entropy jump of the
sector's own flow. Stated as such; this is the standard action-level statement for shocked fluids.

**Certification (section 7 items F1-F4):**
- F1 sympy: Euler-Lagrange derivatives of sqrt(-g) L_x on 1+1 jet symbols (general metric g_ab, tau to second order, s,
  zeta), evaluated at 3 random polynomial configurations (seeds 11/22/33, 40 digits), against (S1)-(S4) written out.
  F generic (a test polynomial in Q, s), so both arms are covered; each arm's F is also checked once. Line: max rel
  residual <= 1e-25.
- F2 sympy: the static reduction (S5) on the static 1+1 ansatz.
- F3 Lean twin (fable_independent_2026/lean_2026/SE1_shock_entropy.lean, Mathlib, standard axioms, 0 sorry): (i) arm (a)
  Jeans monotonicity: s >= s0 and g monotone give mu_K^2 g(s) >= mu_K^2 g(s0); (ii) the secular lemma of (S5): if
  (a t + b) d = 0 for all t and a != 0 then d = 0; (iii) the static Crocco identity: dh = T ds + dP/rho, dP/rho = -dPhi
  and h + Phi = const give T ds = 0; (iv) the strong-shock identity h_2 = (15/32) v^2 (QX13's, restated for the sector's
  own flow). MUTATE twin with false versions must fail to compile on exactly those claims.
- F4 FD solver (section 3) on KNOWN answers and on the Sun (KA5, G8 report).

## 2. Readings of the shock history (frozen; never chosen after the numbers)

The handoff says "in a disc built by smooth accretion s stays at its primordial value". For the sector this is a
reading, not physics: the sector cannot cool, and a cold fluid falling into any well at Mach >> 1 shocks. Both are graded.
- **Reading H (handoff):** discs and every system without a merger history keep s = s_0; X-COP, groups, ellipticals,
  Coma UDGs carry the host's virial shock. SPARC, KiDS late lenses, dSphs and the LG field get s_0.
- **Reading O (own flow):** every bound host's sector was shocked by its own infall (Mach reported).
Under each reading two static closures are graded:
- **Strict (Theorem K):** isentropic per host at the shock adiabat K_sh (strong-shock jump at r_sh = r_ta/2, cold sea
  upstream falling from rest at r_ta, QX13's rule) with open contact to the cosmic sea at r_ta (rho(r_ta) = rho_sea),
  self-consistent with the law, capped at M_cap = f_cap R M_b. A host with s = s_0 takes K_0.
- **Generous (stratified; what QX13 left unproved):** the sector is allowed to sit stratified as an ordinary perfect
  fluid, ignoring (S5). Rest mass conserved: M_x(< r_sh) = M_cap = f_cap R M_b (every captured shell has passed the
  shock). Entropy by shell: K(m) = K_sh (m/M_cap)^alpha, outermost shell at the shock jump. alpha bracket from the
  shock law K ~ v^2 rho_1^(-2/3) with v^2 ~ G m / r_ta(m), r_ta ~ (G m t^2)^(1/3), rho_1 ~ t^-2, t(m) ~ m^(3 eps/2):
  K ~ m^(2/3 + eps). Frozen bracket alpha in {0 (fully mixed: isentropic, mass-conserving), 2/3 (eps = 0, one
  epoch), 5/3 (eps = 1, point-seed secondary infall)}. The boundary density at r_sh is solved for (shooting), not set.

## 3. Solver (FD, spherical, the action's static limit)

In spherical symmetry the law is algebraic in the enclosed source, g(r) = g_law(G (M_b(<r) + M_x(<r) - M_sea(<r))/r^2)
(the uniform sea is background, QX12 iter_3 A1). Hydrostatics dP/dr = -rho g, P = K rho^(5/3) (arm b) or the n = 1
polytrope (arm a), integrated in the Lagrangian mass coordinate m from the boundary inward with RK4 (>= 300 steps,
geometric in m down to 1e-7 M), one shooting parameter (boundary density for "generous"; enclosed mass for "strict")
by bracketing + bisection so that the sector is regular at the centre (r(m -> 0) -> 0). Convergence: each graded b
changes by <= 1e-3 relative when the step count doubles (checked on one host per class; reported).

Hosts (one rule for all classes, from GB1's own features, read-only):
- M_b(r): log-log interpolation of the class's tabulated points (SPARC per galaxy from GB1's rows; X-COP per cluster;
  groups per group and f*), M_b ~ r^3 below the first point, flat at M_sys beyond the last (QX12 iter_3 A1's core rule);
  ellipticals GB1's Mbar(r); Coma UDGs and dSphs M_b(r) = M* r^3/(r^3 + r_h^3) (half the mass inside r_h, GB1's
  convention); KiDS lenses QX12 A1's sphericalised exponential discs with r_d from SPARC's own fit and M_sys =
  g_bar R_med^2/G.
- M_sys: rrM inversion (GB1/KD1 P4); M* for UDGs/dSphs.
- r_ta: QX10's rule. Sea: rho_sea = omega_d rho_crit/h^2 per footing. R = omega_d/omega_b, f_cap = 0.76 (X22), per
  footing from KD1's QX15 setting.
- Candidate for GB1: b = 1 + (M_x(<r) - M_sea(<r))/M_b(<r), F = 1, T = 0 (KD1 P4's interface). Solar System: b = 1 at
  the Sun (KD1 P4); the ambient sector mass inside 1 AU at 8 kpc of an M_b = 6e10 Msun exponential disc host is
  reported against the 1e-10 Msun ephemeris bound (C6P/QX13).

## 4. Built inputs, frozen here with their error bars (graded before nothing else)

| Input | Value / rule | Error bar | Source |
|---|---|---|---|
| R = omega_d/omega_b | per footing, QX15 main theta | none on disk; f_cap bracket {0.76 graded, 1.0 reported} covers it | kd1.json setting |
| captured share f_cap R | 4.111 / 4.112 | as above | KD1 |
| shock radius, upstream | r_ta/2, cold sea from rest at r_ta | variant r_ta/3 reported | QX13 |
| entropy-history exponent alpha | {0, 2/3, 5/3} | the bracket is the error bar | section 2 |
| primordial adiabat K_0 | the largest value G9a allows (section 5) | Delta chi^2 grid step | this lane, CMB only |
| Coma ambient sector (G5 generous add-on) | upper bound rho_x <= Newtonian hydrostatic total density of Coma's beta model (kT 8.6 keV, r_c 276 kpc, beta 0.71, mu 0.6) at each UDG's d_mean | upper bound by construction | S1 / CFG948 on disk |
| host temperature (MUTATE i only) | X-COP mean of kT(r) (EN1 loader), groups global kT, ellipticals Fukazawa kT_o (NGC 6482 missing -> NV), SPARC 1e4 K (cold ISM, as EN1), Coma UDGs Coma's 8.6 keV, dSphs and KiDS none (NV) | as listed | EN1 / GB1 |

No input is set from X-COP, groups or any graded hot class.

## 5. Gates (GB1 G1-G9, read-only, lines unchanged, both footings)

- G1-G8: GB1's gate functions executed read-only (as kd1.py / en1.py do). Lines as GB1 FROZEN_CRITERIA e9464bc8ce.
- G9a CMB-lensing shape: QX3 iter2 machinery as KD1 runs it (CLASS on QX15's footing background, raw PR4 9
  bandpowers, A_s refit): chi^2 at the cold limit <= 18.48 AND Delta chi^2 <= 4 from the Jeans growth ODE + Limber.
  Arm (a): KD1's numbers (same sector, g(s_0) = 1 normalisation, mu_eff = mu_K sqrt(g(s))). Arm (b): s(z) = s_0 in the
  linear regime (Sigma = 0 before shell crossing: no shocks in smooth linear flow, (S1)), so c_s = c_0 (1+z) and the
  physical Jeans wavenumber is mu0 a^(-1/2): the QX3 growth ODE's Jeans term (k/(a mu))^2 becomes k^2/(a mu0^2).
  c_0 = sqrt(1.5 Omega_x) H0 / mu0. mu0_J = smallest grid mu0 on logspace(0, 8, 41) above which every Delta chi^2 <= 4.
- G9b growth: the same Jeans growth ODE with s(z) from the transport equation (s = s_0 until shell crossing) is the
  growth run; its label is G9a's window (QX3/KD1 rule; no separate framework-native growth dataset).
- B1a w(z 3400) <= 0.01; B1b BBN: extra energy over radiation at T = 0.1 MeV <= 0.067 (KD1's line; arm (b) is
  relativistic, radiation-like, before a_nr = c_0/c: reported and graded on that estimate).
- The fixed setting: arm (a) KD1's mu* (CMB/BBN); arm (b) K_0 at mu0_J (the hottest primordial sector the CMB allows,
  most favourable to keeping discs empty under reading H). Converse reading (reported): the c_0 that keeps every SPARC
  host out of capture under reading H (Jeans mass at turnaround above the smallest SPARC M_sys) and its Delta chi^2.

## 6. Labels

- Per arm x reading x closure x footing: each of G1-G9 PASS / FAIL / NO VERDICT (GB1's missing-feature rule).
- Generous closure: a row's label holds only if it is the same at every alpha in the bracket; otherwise NO VERDICT
  with the bracket.
- **No-tuning rule (handoff):** if the g(s) (arm a) or the entropy history alpha / adiabat (arm b) needed differs between
  classes at the same s, the label is FAIL and the class is closed. Checked explicitly: arm (a) discs and the CMB share
  s = s_0 under both readings (and every shocked host has g(s) >= g(s_0)); arm (b) per-class passing alpha sets.
- Arm label: PASS (all rows, both footings, every reading the physics allows) / FAIL (rows named) / NO VERDICT (bracket).
- SE1 label: PASS only if one arm passes every row on both footings under reading O (the physics reading) and its
  strict closure. If SE1 is FAIL by the no-tuning rule, a "fourth wall" paragraph is appended to
  closure_2026_11_06/ALL_GATES_NOGO_2026_11_06.md (append only).
- Stated before any number: the expected outcome is FAIL on two counts (G1 disc capture or G9; the ~100x spread, with
  G5 Coma UDGs above any conserved cosmic share). Whether the action-level sector escapes EN1's radial-shape failure
  is reported as the per-radius X-COP f predicted vs needed, and the sector's entropy profile vs the gas K(r).

## 7. Known answers (a KA FAIL stops grading of the rows it feeds)

- KA1: candidate b = 1 equals gb1.json L0 on G1-G8 to 1e-12, statuses equal; GB1 class means vs QX20 KA dict 1e-6.
- KA2 (= MUTATE iii): arm (a) with g constant, through kd1.py's KD candidate at mu*, equals kd1.json's static rows to
  1e-12; the Jeans rows with the n = 1 term (k/(a mu))^2 equal kd1.json's G9a_jeans rows to 1e-6 and chi^2 at the cold
  limit to 1e-6.
- KA3: QX13 to 0: qx13.py's own solver through QX12 iter_3's grade at QX13's c_min reproduces qx13.json's c_min row
  (X_mean, X_rms, G_fst0, G_fst1, G5_max, G6_shift, G7_shift) to 1e-12, per footing. SE1's strict solver on the same
  hosts with QX13's M1 setting (floor off) is reported beside QX13's M1 numbers (different boundary rule, not a KA).
- KA4 (EN1): SE1's import of EN1's loaders reproduces en1.json's within-host need-vs-proxy table and the V-frac-L
  constant to 1e-9, per footing.
- KA5 (solver KNOWN): law off, no host, no sea: (i) n = 1 polytrope radius pi/k_J (KD1's core rule) to 1e-3; (ii)
  gamma = 5/3 Lane-Emden n = 3/2: R = 3.65375 a_LE and M = 2.71406 (4 pi a_LE^3 rho_c) to 1e-3.
- KA6: strong-shock identity h_2 = (15/16) H_sh on every solved host to 1e-10.

## 8. MUTATE (se1.py --mutate, separate outputs se1_MUTATE.*)

- (i) s set by the host's present temperature instead of shocks (K = (kT/mu m_p)(4 rho_sea)^(-2/3), isentropic, open
  contact; inputs in section 4): must FAIL at least one row (QX12's fixed-temperature failure in this sector).
- (ii) Sigma sign flipped (shocks lower s, so every shocked host sits at or below s_0: the cold primordial sector,
  captured as KD1): must FAIL G1.
- (iii) g(s) constant: must give back KD1 (f_cap 4.1 in discs, G1 FAIL) = KA2.

## 9. Outputs

se1.py -> se1.json / se1.out; se1.py --mutate -> se1_MUTATE.*; se1_fieldeq.py -> se1_fieldeq.json / .out (F1, F2; may
run long, checkpointed); Lean file + MUTATE twin with .out logs. RESULT.md: the certified equations, the built inputs,
the arm x reading x closure x gate x footing table with G9 and growth, KA, MUTATE, every disclosure, one plain label.
Any change after this freeze is disclosed in RESULT.md as post-freeze; an amendment made before any graded number is
committed as AMENDMENT_A*.md first.

Kappa = 1/2 FITTED; not theory closed.
