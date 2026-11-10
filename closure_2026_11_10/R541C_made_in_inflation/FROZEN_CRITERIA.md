# R541C FROZEN CRITERIA: can a Gauss-Bonnet source make the 5.41 during inflation?

2026-11-10. One of four parallel lanes on the owner's question "can anything FIX 5.41 instead of fitting it?".
Written and committed alone, before any script is run and before any gate number is computed. Adopts nothing.
kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 9.3603e-11, R 5.410) / alt (a0 1.1312e-10, R 5.412),
never pooled. The component is cold dark energy, a field component, not a particle.

## 0. Disclosure: hand estimate made before freezing

Before writing this file the lead did one hand calculation, stated here so the order is visible. In a flat FRW
metric with lapse N, sqrt(-g) G_GB = 8 d/dt( adot^3 / N^3 ). If the source is gamma * tau * G_GB with tau entering
linearly, the clock's charge equation integrates to a^3 n - 8 gamma (a H)^3 = const, so the charge made by the term is
n_GB = 8 gamma H^3 at every moment: it is NOT frozen in at the end of inflation and decays as H^3 afterwards. Expected
consequence: the term leaves no lasting dust; the lasting dust is still a free integration constant. The scripts must
confirm or refute this; if they refute it, the hand estimate is wrong and the scripts win.

Also read before freezing (PROVISIONAL, web text of arXiv:2601.05931, Chamseddine and Mukhanov 2026, via a summariser):
their action is -R/2 + lambda(g^mn d_m phi d_n phi - 1) + f(phi) g(box phi) G_GB (8 pi G = 1). The inflationary mechanism
uses f = beta phi WITH g(box phi) = (box phi)^3 = 27 H^3; with that extra factor the source during de Sitter integrates to
18 beta H_I^6 a^3 and is then switched off by the fall of H. Their CS current is 8 adot^3. The plain linear coupling of
this lane is their f = beta phi with g = 1. This lane tests the plain term the owner's brief names, gamma tau G_GB.
The cubic box-phi factor is a different term and is reported only (section 6).

## 1. Setup

Action (A) of PAPER70 (`qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.tex:54-57`), c = 1,
K = 4 pi G, plus one term:

  L / sqrt(-g) = [R - 2 Lambda + 2 mu_K^2 (Q - 1)^2] / (4K) + (P-sector of (A), unchanged) + gamma * tau * G_GB,
  G_GB = R^2 - 4 R_mn R^mn + R_mnrs R^mnrs.

gamma is written gamma = ell / K with ell a length (either sign). tau is the clock; in unitary gauge tau = t and
Q = 1/N. The only place tau enters undifferentiated is the new term. The P-sector, W, the stiffness and matter
(minimally coupled) are unchanged. Charge density n = mu_K^2 (Q - 1)/K (the record's (E3) with P = 0: QX17 RESULT.md:107).

Inflation is NOT adopted by the record. Where a gate needs it, a generic inflation is used: de Sitter at H_I for N_e
e-folds, instant or delayed reheating to temperature T_reh, then radiation, matter, Lambda. Both "with inflation" and
"without inflation" are stated for GC0 and GC1.

## 2. Gates (each: what is computed, the numerical line, the source of the line)

- **GC0 dilution.** Physical charge density factor after N_e = 50, 60, 70 e-folds with no source: exp(-3 N_e).
  Line: none (reported). Statement required: with inflation, a pre-inflation charge is diluted by this factor relative
  to baryons made after reheating, so "primordial initial condition" then means a value set after inflation by some
  process; without inflation the constant stays an initial condition. Both cases written.
- **GC1 generation.** (a) G_GB in de Sitter (24 H^4, known), radiation and matter eras (derived). (b) The charge
  equation with the term, derived from the action (sympy minisuperspace) and covariantly stated. (c) The steady charge
  density during inflation, the comoving charge left after reheating and today, as a function of gamma, H_I, T_reh,
  expansion history. (d) R(gamma, H_I, T_reh, history) for the lasting (a^-3) part. (e) Count of constants needed to
  reach R = 5.41; whether any natural value is singled out. Line for FIXES: R = 5.410 / 5.412 within the Planck-fallback
  width 0.065 (R541 NOTE section 1) with zero new fitted constants.
- **GC2 late-time and local safety.** (a) Source today in the expanding background and its effective density.
  (b) Around Schwarzschild bodies (G_GB = 48 (GM)^2/(c^4 r^6), known): charge that must be created or carried off per
  Gyr outside r_min, for the Sun (r_min = R_sun), a 1.4 Msun neutron star (12 km), a 10 Msun black hole and Sgr A*
  (4.3e6 Msun) (both at r_min = Schwarzschild radius), for each gamma considered. A stationary state can only carry
  the source away as a radial charge flux F; flux speed <= c gives a mass of charge inside radius r of at least F r / c.
  Line (Sun): mass of charge inside Saturn's orbit <= 1e-10 Msun (planetary ephemerides, Pitjev and Pitjeva 2013,
  Astron. Lett. 39, 141: order 1e-10 Msun; PROVISIONAL, from memory, not re-read). Reported beside: the local density of
  the dark component, 0.01 Msun/pc^3 (Read 2014, J. Phys. G 41, 063101; PROVISIONAL; a fit-dependent number, indicative).
- **GC3 cold and adiabatic.** Effective equation of state of what the term makes. Line: w <= 0.01 by z = 3400
  (KD1 B1a, as used in `fable52_push/MK1_one_dust_constant/RESULT.md:113`). Isocurvature: reported against Planck 2018
  X (arXiv:1807.06211) uncorrelated cold isocurvature fraction beta_iso < ~0.035 at 95 % (PROVISIONAL; a fit inside the
  standard model, indicative only). Isocurvature is argued, not computed, unless the lasting charge is nonzero.
- **GC4 coincidence.** Does any equation tie the lasting charge to the baryon number? Line: an explicit relation from
  the action, or "none".
- **GC5 side effects.** (a) Tensor speed today. Formula (Horndeski with G5 = -4 xi' ln X for xi(phi) G_GB; Kobayashi
  2019, arXiv:1901.07183): c_T^2 = (M^2 + 8 xi_ddot)/(M^2 + 8 H xi_dot), here M^2 = 1/(2K), xi = gamma tau. Line:
  -3e-15 <= c_T/c - 1 <= +7e-16 (GW170817 with GRB 170817A; Abbott et al. 2017, ApJL 848, L13; PROVISIONAL, from
  memory). (b) Does the term change the static state or the law: argued from the field equations (order of the new
  terms in a static weak field). Reported beside, not graded: whether the net -16 gamma H^3-type term in the Friedmann
  equation spoils BBN (fraction of the radiation density at T = 1 MeV, indicative line 0.05) or inflation.

## 3. Arms and the label rule

- **Arm I (the lane's question): the term supplies the charge.** After inflation the free integration constant is
  taken to be whatever inflation leaves of a generic pre-inflation value (GC0); the dust must come from the term.
  gamma_needed is the value at which the term's contribution equals the fitted rho_d today (a^-3 part if one exists;
  otherwise the term's total charge density today, which is the most generous reading). GC2, GC3 and GC5 are graded at
  gamma_needed.
- **Arm II (reported, not the label): the free constant is kept.** R comes from the old constant; gamma is only bounded.
  This is the status quo and cannot fix or trade anything.

Label per footing (exactly one):
- FIXES: Arm I gives R = 5.41 (GC1 line) with no new fitted constant and GC0-GC5 all pass.
- TRADES: Arm I gives R = 5.41 only by fitting new constants (named and counted), and GC2, GC3, GC5 pass at gamma_needed.
- EXCLUDED: reproducing R in Arm I breaks GC2, GC3 or GC5; the bound and factor are stated. Also EXCLUDED if Arm I can
  produce no lasting a^-3 charge at any gamma (then the only way to reproduce R with the term's charge is the non-dust
  reading, graded on GC3).
- NOT WELL-DEFINED: the modified equations are inconsistent or ill-posed in the background.
- NO VERDICT: a deciding gate cannot be evaluated even crudely.

## 4. Known-answer checks (KA) and mutations (MU)

- KA1: sympy FRW with lapse: G_GB(de Sitter) = 24 H^4; G_GB = 24 H^2 (Hdot + H^2) in general; sqrt(-g) G_GB =
  8 d/dt(adot^3/N^3) exactly.
- KA2: sympy Schwarzschild: G_GB = R_mnrs R^mnrs = 48 M^2/r^6 (G = c = 1).
- KA3: at gamma = 0 the charge equation returns the record's a^3 mu_K^2 (Q-1)/K = C (QX17 RESULT.md:107;
  part_B_action/frw_charge.py).
- KA4: the Chamseddine-Mukhanov integral with g = 27 H^3 in de Sitter gives 18 beta H^6 a^3 (PROVISIONAL source).
- KA5: c_T formula gives c_T = 1 at gamma = 0; if feasible, a sympy tensor-mode check of the gamma term's coefficients;
  otherwise the formula is taken as PROVISIONAL from the source.
- KA6: GC0 at N_e = 0 gives no dilution.
- MU1 (GC1): replace G_GB by R^2 (not a total derivative): the made charge must no longer track 8 gamma (aH)^3; and
  switch the coupling off at the end of inflation (gamma -> gamma theta(t_end - t)): a lasting a^-3 charge
  8 gamma (aH)^3_end must appear. The gate must move.
- MU2 (GC2): halve ell: created charge halves; move r_min: scales as r_min^-3.
- MU3 (GC3): an a^-3 component returns w = 0.
- MU4 (GC5): ell -> 0 returns c_T = 1; c_T shift scales linearly with ell.

## 5. Files and compute

Scripts in this folder, sympy / numpy / scipy, each printing to a committed .out file, paths relative to their own
folder. Under a few minutes in all.

## 6. Reported only

The cubic box-phi coupling of 2601.05931 (f = beta tau, g = (box tau)^3): retained charge, constants it needs, and the
note that box tau for a falling clock is the expansion (TK1 found keying on the expansion breaks at turnaround). Not
graded here.
