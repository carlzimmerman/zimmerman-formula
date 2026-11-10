# R541A FROZEN CRITERIA: can a direct clock-matter coupling FIX the cold share R = 5.41?

2026-11-10. Written and committed alone, before any script or graded number. Adopts nothing. kappa = 1/2 FITTED; not
theory closed. Cold dark energy is a gravitating field component, never a particle; no particle is added. Footings
canonical (a0 9.3603e-11 m/s^2, R 5.410) and alt (a0 1.1312e-10 m/s^2, R 5.412) are graded separately, never pooled.

## 1. Setup

Base: action (A) of PAPER70 (`qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.tex:54-57`),
units c = 1, K = 4 pi G, M0 := mu_K^2 / K. In the homogeneous background P = 0, F and W vanish and the clock enters
through Q only (`closure_2026_11_10/R541_why_the_cold_share/NOTE.md` section 2; first integral
`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md:107`).

Couplings added to (A), with rho_b = m_N n_b the baryon rest-mass density in the baryon rest frame:

- (i-a) L/sqrt(-g) += -alpha rho_b (Q - 1)
- (i-b) L/sqrt(-g) += -alpha rho_b (Q - 1)^2
- (i-c) L/sqrt(-g) += -alpha rho_b ln Q
  (together: baryon rest mass m_N (1 + alpha f(Q)) )
- (ii)  L/sqrt(-g) += beta (Q - 1) T, T = trace of the matter stress tensor (T = -rho + 3p; dust -rho_b, radiation 0).

Not tested here: eps (d tau) . J_B (lane R541D).

"Zero total charge" has two readings, both graded:
- Z_can: the canonical Noether charge of the shift symmetry of the action AS WRITTEN (coupling included) is zero.
- Z_K: the clock's own part a^3 M0 (Q - 1) is zero.
The free reading C != 0 is reported beside: if R then depends on C and not on the coupling, the coupling fixes nothing.

"Cold share" R_cold = (density that does NOT move with the baryons, i.e. moves with the clock's frame) / (density of
the baryon component as the CMB sees it). A density locked to the baryon velocity counts as baryon load, not as R.

## 2. Gates (numerical line and source written before computing)

- **GA1 background.** Derive the first integral with each coupling. PASS needs: under Z_can or Z_K, some coupling value
  gives R_cold(a) = 5.410 / 5.412 within 0.065 (1.2 %, Planck 2018 width used by R541 NOTE section 4; indicative,
  standard-model fit) at every a in [1e-9, 1] (before nucleosynthesis to today). Also stated: whether Z is forced by
  any equation. If C stays a free integration constant and nothing sets it, record "the coupling fixes nothing".
- **GA2 cold and separate before recombination.** Linear perturbations in the tightly coupled era (Newtonian, sub-
  horizon). PASS needs: the part of the induced density that moves with the baryons changes the baryon load seen by
  the peaks by <= 1 % (the peaks fix omega_b to ~1 %: Planck 2018 0.02237 +- 0.00015, 0.7 %, indicative, standard-
  model fit), and the cold share R_cold matches GA1's line. If R_cold = 0 the reference is F1A's baryons-only
  penalty, DeltaMB = +172,915.6 / +166,674.4 chi2 (`closure_2026_11_07/F1A_primary_cmb_audit/RESULT.md`, G1 row).
- **GA3 equivalence principle and fifth force.** Static (standing) clock Q = 1/N around the Earth and the Sun (rule 4 of
  `closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md:16`). Compute the extra acceleration on a test body per unit of
  its baryon rest-mass fraction b = B m_N / M, b from atomic masses for Ti, Pt and the MICROSCOPE alloys (TA6V, PtRh10).
  PASS needs |eta(Ti,Pt)| <= 7.0e-15 (MICROSCOPE final, Touboul et al. 2022, PRL 129, 121102:
  eta = [-1.5 +- 2.3 (stat) +- 1.5 (syst)] e-15; |central| + 2 x quadrature 2.75e-15; PROVISIONAL, quoted from memory,
  not fetched) AND |gamma_eff - 1| <= 6.7e-5 (Cassini, Bertotti, Iess and Tortora 2003, Nature 425, 374:
  gamma - 1 = (2.1 +- 2.3) e-5; 2.1 + 2 x 2.3; PROVISIONAL, from memory). Both are direct measurements.
- **GA4 the law.** At the coupling GA1 needs, the static state around a galaxy at leading order: PASS needs the law's
  form kept and the deep-regime amplitude (effective a0 at fixed baryonic mass, as stars respond) within 10 % of
  the uncoupled law, i.e. |a0_eff / a0 - 1| <= 0.10.
- **GA5 energy bookkeeping.** PASS needs: the Friedmann constraint preserved by the equations (symbolic residual 0),
  every density of the split >= 0 at the needed coupling, and a positive-definite kinetic (inertia) matrix of the
  baryon-clock system; no sign flip of the clock's kinetic coefficient on [1e-9, 1].

## 3. Label rule (one per footing)

- The coupling is graded as a mechanism for R: R must come from the coupling with zero free charge (Z_can or Z_K).
- FIXES: some coupling, under a Z reading that an equation FORCES, gives R_cold = 5.41 with no new fitted constant and
  passes GA1-GA5.
- TRADES: as FIXES but the coupling constant is fitted (count it, plus Z if Z is only assumed) and GA1-GA5 pass.
- EXCLUDED: under Z no coupling value gives R_cold = 5.41 (GA1 or GA2 fails at every value), or the value that gives
  it breaks GA3 / GA4 / GA5; name the gate and the factor. With C free R then rests on C exactly as before.
- NOT WELL-DEFINED: equations inconsistent, unstable or ill-posed at the needed coupling.
- NO VERDICT: a deciding gate cannot be evaluated.
- The lane label is the best label over the four couplings; each coupling's own row is reported.

## 4. Known-answer checks and mutations (one each per numerical gate)

- GA1 KA: alpha = 0 recovers the record's a^3 mu_K^2 (Q-1)/K = C and rho_K = C/a^3 + K C^2/(2 mu_K^2 a^6)
  (R541 part_B frw_charge.out). MU: set C = 5.41 rho_b0 (free reading): R must follow C and not alpha.
- GA2 KA: alpha = 0, the clock dust obeys the uncoupled pressureless continuity/Euler pair and the acoustic frequency is
  the textbook omega^2 = k^2 / [3 (1 + 3 rho_b / 4 rho_gamma)] (no gravity). MU: give the clock a free charge
  sigma = 5.41 rho_b on top of Z: R_cold must move from 0 to 5.41.
- GA3 KA: binding energy per nucleon of Fe-56 from the same atomic-mass table, 8.790 MeV; alpha = 0 gives eta = 0,
  gamma = 1. MU: halve alpha (eta halves); swap Pt for Be.
- GA4 KA: alpha = 0 recovers a0_eff = a0. MU: alpha -> alpha/2 moves a0_eff as predicted.
- GA5 KA: alpha = 0 constraint preservation as in GR + dust. MU: alpha > 1 must flip the baryon density sign.

Scripts locate files relative to their own folder; each prints to a committed .out file. No downloads. Compute
seconds. Amendments, if any, go to AMENDMENT_A1.md, committed alone before use; the as-frozen label is reported too.
