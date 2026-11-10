# R541E FROZEN CRITERIA: the B minus L escape from R541D (clock coupled to J_{B-L}; variant J_L)

Written and committed alone, before any script and before any gate number. Adopts nothing. kappa = 1/2 FITTED; not
theory closed. Footings canonical (R = 5.410, omega_b 0.02236, a0 9.3603e-11 m/s^2) and alt (R = 5.412, omega_b
0.02234, a0 1.1312e-10 m/s^2); omega_d 0.1209, h 0.674 on both; never pooled. The component is cold dark energy (a
field component, not a particle). No dark matter particle is added. This lane tests an escape sketched without a
calculation; every step is treated as unproven and the lane tries to break it. A negative result is a full result.

## 1. Setup (exact)

Action (A) of PAPER70 (`qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.tex`, Eq. A) plus
one term:

    S = S_A + S_m + eps * Int d^4x Jt_X^m d_m tau,     Jt_X^m = sqrt(-g) J_X^m

- Main case: X = B - L (all quarks B = 1/3, all leptons L = 1, including right-handed neutrinos where present).
- Variant: X = L (lepton number alone).

eps has dimension of energy (natural units hbar = c = 1, GeV). Homogeneous background P = 0, so only
L_K = mu_K^2 (Q - 1)^2 / (2K) carries tau (K = 4 pi G). R541D's algebra carries over with J_B -> J_X: the conserved total
is p = a^3[(mu_K^2/K)(Q-1) + eps n_X]; the clock Hamiltonian is H = u + K u^2/(2 a^3 mu_K^2), u = p - eps a^3 n_X; the
bias on X is mu_X = eps Q (R541D GD1/GD4, sympy, residual 0; re-checked here with X in place of B).

Hand expectation (declared now, to be broken): (i) sphalerons conserve B - L, so a bias on a conserved charge is a
Lagrange-multiplier shift and induces nothing; (ii) a neutral start gives rho_K = -eps n_{B-L} and n_{B-L} =
(79/28) n_B, so eps is about -1.8 GeV; (iii) the B - L asymmetry must come from a new out-of-equilibrium sector whose
B - L violation, while in equilibrium, washes toward a negative-rho_K value; (iv) with Majorana neutrinos the bias is
physical today and the vacuum makes neutrino pairs; (v) action (A)'s quadratic dust term makes Q astronomically
large at the generation epoch, as in R541D GD4; (vi) the variant L = B - (B - L) carries a bias on B and repeats R541D.

## 2. Gates (each with its numerical line and source)

Common inputs: m_bar = mass per baryon from Y_p = 0.245 [P] (as R541D); observed n_B/s from omega_b, T_cmb 2.7255 K,
g_s0 3.909 (as R541D, expected 8.70e-11); (B-L)_obs/s = (79/28) n_B/s. [P] = PROVISIONAL look-up.

- **GE1 sphaleron safety.** SM chemical equilibrium (3 generations, 1 Higgs doublet, all Yukawas and sphalerons in
  equilibrium, total Y = 0), with B - L conserved (no B - L violation in equilibrium) and fixed at its made value.
  Add the bias as mu_i += X_i * eps * Q. Compute the induced n_B/s per unit eps/T, for X = B - L and X = L.
  Line: PASS iff the bias-induced |n_B/s| at T_sph = 131.7 +- 2.3 GeV (D'Onofrio, Rummukainen, Tranberg 2014, PRL 113,
  141602 [P]) is <= 10 % of the observed value (as R541D's GD3 line, X <= 10 would be the fail line there; here the
  escape claims zero, so the line is the stricter 10 %). Known answer: X = B must recover R541D's n_B/s = -3.7464e-4
  (canonical, eps = -5.0700 GeV, T_sph 131.7).
- **GE2 the constant.** Neutral start p = 0. Late rho_K = -eps n_X (energy per unit charge (Q+1)/2 -> 1). Standard
  sphaleron redistribution B = (28/79)(B - L) (Harvey and Turner 1990, PRD 42, 3344) so n_{B-L} = (79/28) n_B and
  R = -eps (79/28) / m_bar; for the variant L = -(51/79)(B - L) = -(51/28) B so R = +eps (51/28) / m_bar. Report eps
  for R = 5.410 and 5.412 in GeV with sign; report also the broken-phase ratio 12/37 (Khlebnikov and Shaposhnikov [P])
  as a systematic. Native energies, listed now before computing: exactly R541D's 79-entry list, namely
  E = c * M^alpha * rho_DE^((1-alpha)/4) with M in {M_Pl = 1.22089e19 GeV, M_Pl/sqrt(8 pi)}, alpha = p/q in lowest
  terms with q = 1..6, 0 <= p <= q, c in {1/2, 1, 2}, plus hbar a0 / c (per footing); rho_DE from h^2 - omega_b -
  omega_d - 4.18e-5 times the critical density per h^2. A candidate counts only if within 1.2 % of |eps| (Planck
  fallback width on R, 0.065/5.41) AND produced by the action; a numerical hit without a derivation is reported and
  still counted as fitted. If no native value: eps is a new fitted constant and TRADES is the best label.
- **GE3 what makes the B - L, and washout.** Options named (each is a new ingredient outside the framework):
  (a) Majorana neutrino mass from the dimension-five Weinberg operator, whose Delta L = 2 rate freezes at
  T_W ~ 1.66 sqrt(g*) pi^3 v^4 / (M_Pl sum m^2), v = 174 GeV, sum m^2 = 2.5e-3 eV^2 [P] (R541D's formula);
  (b) thermal leptogenesis with heavy Majorana N1, M1 = 1e9 GeV (Davidson-Ibarra lower bound, PLB 535 (2002) 25 [P])
  and 1e10 GeV, inverse-decay freeze-out T_f = M1 / z_f with z_f = 10 [P];
  (c) a generic B - L-violating out-of-equilibrium sector compatible with Dirac neutrinos (no Delta L = 2 operator;
  e.g. B - L broken only by 4 units, Heeck and Rodejohann 2013 [P]), freeze-out T_f free: report the minimum T_f.
  For each, compute the equilibrium value the bias drives B - L to while the B - L-violating interaction is in
  equilibrium (SM equilibrium, B - L not conserved, Y = 0; with and without three right-handed neutrinos in the bath):
  n_{B-L}^eq / s = c_{B-L} eps Q / T, evaluated at that option's freeze-out with Q = 1 (Q's real value is GE5's job).
  State its sign relative to the one rho_K > 0 needs. Line: an option passes iff |n_{B-L}^eq/s| at its T_f <= 10 % of
  (B-L)_obs/s. GE3 PASS iff at least one option passes AND is compatible with GE4's outcome (if GE4 requires Dirac
  neutrinos, options (a) and (b) are not compatible). Each passing option is counted as >= 1 new ingredient.
- **GE4 the vacuum today.** With Majorana masses the rephasing that removes the term leaves the mass term rotating as
  m e^{2 i eps tau}, frequency omega = 2|eps| Q (Q = 1 today). Rate of neutrino pair production per volume for one
  Majorana mass m (two-body coherent-source formula, derived in the script, checked against the inflaton-decay
  analogue): Gamma/V = m^2 omega^2 / (16 pi). Accumulate over the background (flat, Omega_m = (omega_b + omega_d)/h^2,
  radiation 4.18e-5/h^2, rest Lambda) from a = 0 to 1: n0 = Gamma/V Int a^3 dt; rho0 = omega Gamma/V Int a^4 dt
  (relativistic). Report also the Pauli-blocked cap g|eps|^3/(6 pi^2), |eps|^4/(8 pi^2) per helicity. Use m = 0.05 eV
  (about sqrt(Delta m^2_atm), NuFIT [P]). Line: rho0 <= 1 % of the critical density (per footing h). Give m_max.
  If m_max < 0.05 eV (oscillations need at least one mass >= ~0.05 eV) Majorana neutrinos are EXCLUDED for this
  coupling and the main case requires Dirac neutrinos (with nu_R carrying L = 1, so the Dirac Yukawa is invariant);
  then GE4 PASSES only as "requires Dirac neutrinos" and the kill test is any observation of neutrinoless double beta
  decay; status: KamLAND-Zen complete dataset, T_1/2(136Xe) > 3.8e26 yr, m_bb < 28-122 meV (arXiv:2406.11438 [P]),
  no signal. Reported (not graded) B - L-violating nucleon operators: the dimension-seven Delta(B-L) = 2 operator as
  a nucleon-lepton mixing delta (GeV), bounded by Super-K p -> nu pi+ > 3.5e32 yr (arXiv:2510.26232 [P]) with
  Gamma ~ m_p delta^2 (1+D+F)^2 / (32 pi f_pi^2) (order of magnitude, D+F = 1.27, f_pi = 0.092 GeV); vacuum -> pbar e-,
  nbar nu at omega = 2|eps| > m_N: Gamma/V ~ 2 delta^2 omega^2 (1 - m_N^2/omega^2)^2 / (8 pi); factor by which delta
  must sit below its current bound for the 1 % line. Same for n-nbar (delta_nn = 1/tau, tau > 4.7e8 s, Super-K 2021,
  arXiv:2012.02607 [P]): vacuum -> nbar nbar. And for the GE3(c) sector's T = 0 remnant, a Delta(B-L) = 4 dimension-six
  (nu_R)^4 / Lambda^2 operator: the Lambda the 1 % line needs (reported).
- **GE5 back-reaction under action (A).** With p = 0, after the asymmetry exists, (mu_K^2/K)(Q - 1) = -eps n_{B-L},
  i.e. Q - 1 = I0 / (2 mu_K^2 a^3) (I0 = 3 H0^2 Omega_d). Evaluate at the epoch GE3 needs (the lowest passing T_f,
  and T_sph). Record mu_K lines (per Mpc): 198.25 (w at z 3400), 2.512e4 (CMB lensing), 8.89e6 (BBN, KD1); galaxy rows
  <= 1-7 (MK1). Line: Q - 1 <= 0.01 at that epoch for some mu_K the record allows. Also report: the energy per unit
  B - L made, |eps| Q, against the energy available (T_f, M1); the equilibrium value with the clock's own quadratic
  energy included, n = eps / (1/(chi T^2) + K eps^2/mu_K^2); and the stiff energy K eps^2 n^2/(2 mu_K^2) against
  radiation. FAIL -> EXCLUDED; RESULT.md must say whether the failure belongs to the coupling or to action (A)'s dust
  term. Also REPORT (not the label) the label with a pressureless dust term (Q = 1 at all epochs).
- **GE6 invisible, cold, adiabatic.** Sympy: psi_i -> exp(i eps X_i tau) psi_i for two Dirac species of different X
  (quark-like 1/3, lepton-like -1) with an X-conserving interaction, flat and with a generic vierbein and spin
  connection: residual 0 means no fifth force and no EP signal from X-conserving physics (atoms carry B - L = N, so a
  non-removable term would be a composition-dependent force). An X-violating term (Delta X = 2) must keep
  exp(2 i eps tau). Anomalies (exact fractions): SU(2)^2 (B-L), Y^2 (B-L), grav (B-L) with and without nu_R; SU(2)^2 L
  for the variant. PASS iff residual 0 and B - L anomaly-free in the setup used (with nu_R). Decoupling: after the last
  B - L violation the term is a total derivative (R541D GD1 identity), so the component is decoupled from the
  photon-baryon fluid; isocurvature: local neutral start gives rho_K / n_{B-L} = -eps everywhere, S = 0 iff the B - L
  asymmetry is adiabatic (argued, no perturbation solve).

## 3. Label rule (per footing; main case; the variant gets its own label by the same rule)

- Any of GE1, GE3, GE4 (no neutrino-mass type consistent with oscillations survives), GE5, GE6 FAIL -> EXCLUDED (name
  bound and factor), unless the equations are inconsistent -> NOT WELL-DEFINED.
- All pass and eps native by GE2 -> FIXES. All pass and eps fitted -> TRADES, counting: eps (1 constant), the B - L
  generation sector, right-handed neutrinos if GE4 requires Dirac, and the neutral-start premise.
- A deciding gate not evaluable even crudely -> NO VERDICT.
- Pressureless-dust report: the same rule with GE5 evaluated at Q = 1; reported only, never the label.

## 4. Known-answer checks and mutations

- KA1 (GE1): X = B bias reproduces R541D's -3.7464e-4 at 131.7 GeV (canonical).
- KA2 (GE1/GE2): no bias, B - L = 1 gives 28/79 (Harvey-Turner), and L/(B-L) = -51/79.
- KA3 (GE4): the coherent two-body production integral for a Dirac fermion with mass m0 cos(omega t) reproduces
  n_phi Gamma(phi -> f fbar) = m0^2 omega^2 beta^3 / (16 pi) (inflaton-decay formula, y Phi = m0) to 1e-6.
- KA4 (GE5): reproduces R541D's Q - 1 = 1.229e24 at T_sph for mu_K 8.89e6 (canonical); and -K eps n_{B-L}/mu_K^2 equals
  I0/(2 mu_K^2 a^3) after generation to 2 %.
- KA5 (GE6): rephasing residual 0 (flat, curved); grav (B-L) anomaly 0 with nu_R and -3 without; SU(2)^2 B nonzero.
- KA6 (GE2): X = B reproduces R541D's eps = -5.0700 GeV.
- MU1 (GE1): allow B - L violation in equilibrium -> induced B nonzero; bias on L -> nonzero (variant).
- MU2 (GE2): R x 2 -> eps x 2; 28/79 -> 12/37 moves eps by (12/37)/(28/79).
- MU3 (GE3): T_f / 1000 -> ratio x 1000.
- MU4 (GE4): m / 10 -> rho0 / 100; eps x 2 -> rho0 x 8.
- MU5 (GE5): mu_K / 10 -> Q - 1 x 100.
- MU6 (GE6): a Delta(B-L) = 2 term is not removed (keeps exp(2 i eps tau)).

Scripts print to committed .out files, locate files relative to their own folder, run in seconds.
