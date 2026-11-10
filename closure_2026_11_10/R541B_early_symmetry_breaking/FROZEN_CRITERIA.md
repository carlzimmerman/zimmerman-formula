# R541B FROZEN CRITERIA: can an early potential V(tau) on the clock FIX the cold share 5.41?

Committed alone, before any script or graded number. TEST lane, quarantined. Adopts nothing, relabels nothing,
registers nothing. kappa = 1/2 FITTED; not theory closed. Footings canonical (R 5.410, omega_b 0.02236) and alt
(R 5.412, omega_b 0.02234), never pooled; omega_d 0.1209, h 0.674 on both (F1A RESULT.md:22-23). Cold dark energy is a
gravitating field component, never a particle; no particle is added. A negative result is a full result.

Sibling lanes R541A, R541C (Gauss-Bonnet during inflation), R541D are not touched or tested here.

## 0. Setup (exact)

Action (A) of PAPER70 (`qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.tex`, eq. A, c = 1,
K = 4 pi G) plus one new term:

    L / sqrt(-g) = (A) - V(tau).

V depends on the clock tau only (tau has units of time; Q = 1 means tau runs at proper time). Homogeneous expanding
background, P = 0, so W = F = 0 (QX17 RESULT.md:107; R541 NOTE section 2). Minisuperspace, lapse N, scale factor a:

    L = L_grav(N, a) + N a^3 mu_K^2 (Q - 1)^2 / (2K) - N a^3 V(tau) - N a^3 rho_matter,   Q = tau-dot / N.

Charge p_tau = a^3 mu_K^2 (Q - 1) / K = C (the record's first integral). With V, Euler-Lagrange gives (to be derived by
sympy, sign and coefficient checked, KA1):

    dC/dt = - N a^3 V'(tau)      (covariantly div J = -V'(tau), J^m = n^m mu_K^2 (Q-1)/K; same form as AC2q's line
                                  "nabla_m[n^m rho_phi - ...] = -V'(phi)", PAPER70 line 86).

Background: H^2 = (8 pi G / 3)(rho_r + rho_b + rho_K + V + rho_Lambda), rho_K = mu_K^2 (Q^2 - 1)/(2K),
p_K = mu_K^2 (Q - 1)^2 / (2K), V with p_V = -V. omega_r = 2.47e-5 (1 + 0.2271 x 3.044) (photons + 3.044 neutrinos,
textbook), Omega_Lambda = 1 - Omega_m - Omega_r. Integrated in ln a from a_ini = 1e-12 (or earlier than any switch)
to a = 1, solve_ivp, rtol <= 1e-10. R = C(a = 1) / rho_b0.

Initial data (stated, because the symmetry is broken they become physical): C_i (charge before V acts; primary 0) and
the clock's offset tau_i = tau - t at a_ini (primary 0: "anchored", the clock reads proper time since the bang).
mu_K is not valued by the record (MK1 NO VALUE); primary values 2.512e4 / Mpc (CMB-lensing Jeans line, MK1 RESULT.md:39)
and 8.89e6 / Mpc (BBN line on the stiff term, MK1 RESULT.md:115-116); both printed.

Hand estimate, disclosed before computing: if Q stays near 1 (tau = t + tau_i), integrating by parts gives
C = integral V d(a^3), so a sudden switch-off at a_s from V0 leaves R = V0 a_s^3 / rho_b0: the potential's energy at
switch-off becomes dust (a decaying vacuum dumped into the clock). R is linear in V0 and depends on the switch time. If
this holds, no attractor is expected. The scripts decide.

What is new relative to the record:
- CFG360-DE (LEDGER.md:334) C1 drained rho_Lambda late (Gamma <= 0.0229 H0) and C2 put a SEPARATE field's minimum on
  the clock (V(phi - v(tau))). Here the potential acts on the clock tau itself, inside action (A), and the generated
  quantity is (A)'s own conserved charge; the amplitude and switch time are not tied to rho_Lambda.
- CFG288 (STANDING_2026-09-29.md:554) seeded dust from dark energy at fixed z (1100 / 3400 / 1e4 excluded, >= 1e5
  undecided); here the generation history is computed from an action and the zero-new-constant family (d) is enumerated.
- CMB2 (D1) and MK1 treat the charge as given; TK1 changes the stiffness. None breaks the shift symmetry.

## 1. Families (frozen before computing)

(a) V = V0 exp(-tau / tau_s).
(b) smooth step V = (V0 / 2)[1 - tanh((tau - tau_s) / Delta)]; Delta / tau_s in {0.01, 0.1, 0.3}. The sharp step
    (Delta -> 0) is the KA2 limit.
(c) decaying power law V = V0 (1 + tau / tau_s)^(-n), n in {1, 1.5, 2, 3, 4}.
(d) zero new constants: V built only from rho_DE, a0, mu_K, G, c. Dimensional analysis (SI; rho_DE a mass density):
    the five quantities rho_DE, G, c, mu_K and tau span 3 dimensions, so V = rho_DE c^2 F(x, y) with
    x = sqrt(G rho_DE) tau, y = mu_K c / sqrt(G rho_DE); a0 adds nothing (a0 tau / c = x / 2 with kappa = 1/2).
    F is an arbitrary function, so the class is infinite; the enumerated grammar is:
      amplitude  A = beta rho_DE c^2 y^p, p in {0, 1/2, 1, 3/2, 2}  (p = 2: mu_K^2 c^4 / G, the K term's own scale),
                 beta in {1/(8 pi), 1/(4 pi), 1/4, 1/2, 1, 2, 4, 4 pi, 8 pi};
      time scale T = y^(-q) / sqrt(G rho_DE), q in {0, 1/2, 1}  (q = 0: the dark-energy time; q = 1: 1/(mu_K c));
                 c / a0 = 2 / sqrt(G rho_DE) is included as q = 0 with an extra factor 2;
      shapes     exp(-tau/T) and the sharp step at T; anchored clock (tau_i = 0), C_i = 0.
    rho_DE = Omega_Lambda rho_c0 at h 0.674 (the law's a0 = (1/2) c sqrt(G rho_DE) then gives the canonical footing
    9.36e-11 at the record's convention; the background does not use a0). For p = q = 0 every number is fixed: R is
    computed. For p or q non-zero R depends on mu_K: the lane solves for the mu_K giving R = 5.41 and checks it
    against the gates. **Rule:** mu_K has no value in the record (MK1 NO VALUE, lower bounds only), so a (d) form that
    reaches 5.41 only at a chosen mu_K counts as ONE fitted constant (mu_K) plus the form choice: TRADES at best, not
    FIXES. hbar is not one of the framework's constants and is not used in (d).

## 2. Gates, numerical lines and sources

**GB1 background (charge generated).** Report R(V0, tau_s, ...) for (a)-(d) on both footings; V0 solving R = 5.410 /
5.412 as a function of the others; the count of new constants (and how many are fitted to R); attractor test:
d ln R / d ln V0, d ln R / d ln tau_s, and R's response to C_i (C_i / rho_b0 in {0, 1, 5.41}) and to tau_i
(tau_i / tau_s in {-0.1, 0, 0.1}). **Attractor** = |d ln R / d ln V0| <= 0.1 AND |d ln R / d ln tau_s| <= 0.1 AND
|Delta R| <= 0.065 (the Planck 1.2 % width, R541 NOTE:31-32) over the C_i and tau_i ranges. Otherwise NO ATTRACTOR.

**GB2 timing and coldness.** Lines:
- GB2a in place: >= 99 % of the final charge generated by z = 1e5 (CFG288 seeding: conversion at z = 1e4 EXCLUDED,
  max |Delta C/C| 0.22; z >= 1e5 undecided, STANDING_2026-09-29.md:554; CFG360 G-TIMING (ii) asks 99 % by z 3000,
  FROZEN_CRITERIA.md there). A parameter point whose 50 % generation redshift is <= 1e4 is EXCLUDED; one with 99 % by
  1e5 PASSES; between is undecided for that point.
- GB2b cold: the clock sector's own w = (p_K - V) / (rho_K + V) satisfies |w| <= 0.01 at every z <= 3400 (KD1 B1a line,
  MK1 RESULT.md:38; V's energy counted). The stiff partner's line on mu_K (>= 198 / Mpc, MK1) is inherited and printed.
- GB2c BBN: at T = 1 MeV (1 + z = 4.26e9), (rho_K + V) / rho_rad <= 0.067, i.e. Delta N_eff <= 0.5 (BBN-only
  N_eff = 2.88 +- 0.27, Fields et al. 2020, JCAP 03, 010; PROVISIONAL, from memory, not re-fetched). Also printed:
  the stiff term's BBN line on mu_K (8.89e6 / Mpc, MK1 RESULT.md:115-116, reported there not graded).
GB2 passes for a family if a parameter set exists that reaches R and passes GB2a-c.

**GB3 perturbations (isocurvature).** While V' != 0 the generated amount depends on the local clock reading. For a
clock offset delta tau_rel relative to the adiabatic time shift, the dust gets S = delta_d - (3/4) delta_gamma
= -(d ln C / d tau_i) delta tau_rel (computed numerically from GB1's tau_i response; sharp step in radiation:
S = (3/2) delta tau_rel / t_s). Line: |S| <= 9e-6, from P_S / P_zeta <= 0.04 (uncorrelated CDM isocurvature, Planck
2018 X, beta_iso < 0.038 at k 0.05; a fit made inside the standard model: INDICATIVE, PROVISIONAL) with
zeta = sqrt(2.1e-9) = 4.6e-5. The lane reports (i) the anchored clock (delta tau_rel = 0: S = 0 by construction); (ii)
the synchronisation required, delta tau_rel / t_s, per family; (iii) whether (A) + V damps an offset before
generation (linearised pi equation; damping = offset shrinks by >= 10 before the 50 % generation time); (iv) a crude
inflationary estimate delta pi = H_inf / (2 pi sqrt(2) M_pl mu_K) for a c_s = 1 field (optimistic; (A) has c_s = 0 at
Q = 1, which makes the vacuum estimate ill-defined; stated as such), giving the largest H_inf allowed.
GB3 PASSES only under the anchored clock if no damping is found; that anchoring is then counted as an extra initial
condition the mechanism needs (listed with the constants).

**GB4 coincidence.** Does the mechanism contain rho_b (or n_B, eta)? Test: change omega_b by x2 at fixed V (MU3); TIED if
R stays within 0.065, UNTIED if R ~ 1/omega_b. UNTIED is allowed under TRADES, not under FIXES.

**GB5 late-time safety.** Lines: |Delta C / C| between z = 3000 and z = 0 <= 1e-2 (the 1.2 % width); today's rate
|d ln C / dt| = |V'(t0)| / rho_d0 <= 1e-2 H0 (reported as the required bound on V'(t0)); |V(z)| / rho_DE <= 0.02 for
z <= 5 (the framework's flat-a0 line, |Delta a0 / a0| <= 1 %, CFG360 cfg360_cold_fluid_from_de.out:43).

## 3. Labels (exactly one per footing)

- FIXES: R = 5.41 follows with no new fitted constant (family (d) with no chosen mu_K) and GB1-GB5 pass, GB4 included.
- TRADES: R reproduced only by fitting new constants (named, counted; initial-condition assumptions listed) and GB2,
  GB3 (as above), GB5 pass.
- EXCLUDED: every way of reproducing R breaks a gate (bound and factor given).
- NOT WELL-DEFINED: equations inconsistent, unstable (Q -> 0 or Q < 0 on the needed branch) or ill-posed.
- NO VERDICT: a deciding gate could not be evaluated (say what is missing), after the crude honest evaluation.

## 4. Known-answer checks (each must pass) and mutations (each must move its gate)

- KA1 sympy: Euler-Lagrange on the minisuperspace with V gives dC/dt = -N a^3 V'(tau); at V = 0, C is conserved
  (residual 0); Friedmann constraint reproduces frw_charge.out's rho_K.
- KA2 V = 0 numerically: C(a = 1) = C_i to <= 1e-8 relative for C_i / rho_b0 in {1, 5.41}.
- KA3 sharp step, Q ~ 1: C = V0 a_s^3 (analytic) to <= 1e-3.
- KA4 exponential in pure radiation, Q ~ 1: C = Gamma(5/2) V0 a(tau_s)^3 = 1.32934 V0 a(tau_s)^3 to <= 1e-3.
- KA5 energy conservation of the clock + V sector: d(a^3 rho)/dt + p d(a^3)/dt = 0 along a solution, <= 1e-6 relative.
- KA6 t(a) in the radiation era: t = 1 / (2 H) to <= 1e-3 at a = 1e-8.
- KA7 isocurvature: S from two runs (tau_i = +-eps) agrees with (3/2) delta tau / t_s for the sharp step to <= 2 %.
- MU1 sign flip (V increasing in tau): C < 0, R < 0; GB1 must report no positive dust (and Q -> 0 if pushed).
- MU2 switch-off at z = 1e3: GB2a must read EXCLUDED.
- MU3 omega_b x 2 at fixed V: R must halve (GB4).
- MU4 power law n = 1 with tau_s early: GB5 must fail (late generation).
- MU5 clock offset delta tau_rel = 1e-3 t_s: GB3 must fail (|S| > 9e-6).

## 5. Files

Scripts in this folder, paths relative to their own folder, each printing to a committed .out:
`kA_charge_equation.py` (sympy, KA1), `gb_background.py` (GB1, GB2, GB4, GB5, KA2-KA6, MU1-MU4),
`gb3_isocurvature.py` (GB3, KA7, MU5), `gbd_zero_constant.py` (family (d)). Then RESULT.md.
