# W2 -- exact non-perturbative properties of QED as a possible selector of the low-energy coupling (pre-registration)

Written 2026-09-29 BEFORE any script in this directory was written or run. Target: 1/alpha = 137.035999177 (Thomson limit). alpha stays an INPUT; kappa = 1/2 stays FITTED;
the SM mass sector is walled (charged-fermion masses and the measured couplings at m_Z are INPUTS). No personal names, no absolute paths, no committed bytecode, nothing outside this directory.

## Question
Does any EXACT non-perturbative statement about QED with the Standard Model's charged content (masses and charges as inputs) single out a value of the low-energy coupling?
Sub-questions (a) critical coupling for chiral symmetry breaking; (b) Landau pole and triviality; (c) compositeness / quasi-fixed points; (d) large-N_f QED; (e) Ward identity Z1 = Z2 and Z3.

## What was READ before this file (provenance, honest)
* READ in text (pdftotext of the arXiv PDF): Goeckeler, Horsley, Linke, Rakow, Schierholz, Stueben, hep-th/9712244 (whole letter); Holdom, arXiv:1006.2119 (pages 1-7 of the text, incl. eqs. (1)-(14));
  Gies & Jaeckel, hep-ph/0405183 (abstract, introduction and the first part of the method; NOT the numerics); Curtis-Pennington bifurcation analysis, hep-th/9211124 (setup, eq. (2.7), definition of lambda_c;
  NOT the numerical tables); Arnold, Bunk, Lippert, Schilling, hep-lat/0210010 (abstract and the quoted result beta_T = 1.0111331(21)).
* Search-snippet only (NOT verified in text): "alpha_c(bare vertex, Landau gauge) = pi/3; alpha_c(Curtis-Pennington) = 0.933667". pi/3 is re-derived numerically here (A1); 0.933667 stays UNVERIFIED and is used only as a second value in the variant grid.
* RECALLED, not read: Miransky scaling of the dynamical mass; Pendleton-Ross / Hill infrared quasi-fixed points; Bardeen-Hill-Lindner compositeness; Bjorken/Eguchi compositeness Z3 = 0; Johnson-Baker-Willey / Adler
  eigenvalue conditions; Kaellen-Lehmann bound 0 <= Z3 <= 1 (cited in Goeckeler et al. as Bjorken-Drell and Luescher); the two-loop QED beta coefficient; the two-loop SM gauge matrix (via lane N1).
* Palanques-Mestre/Pascual and Gracey (source of F_1) were NOT read; F_1 is taken from Holdom's eq. (3)-(4), which I read, and checked against Holdom's own printed numerical expansion (12).

## Numbers KNOWN before this pre-registration (disclosed; nothing below was computed by me yet)
* From the record: lane I toy (QED-only, SM fermions): 1/alpha(M_Pl) = 59.8056 (quark set A), S = 77.2304 (M = M_Pl); set B S = 75.3308; alpha_max/alpha_0 = 1.7744 / 1.8191. Lane B one-loop: 1/alpha_Y(M_P) = 55.48.
* From Goeckeler et al. (read): they quote Lambda_L ~ 10^227 GeV for the electron alone, ~10^34 GeV for the SM, and 1/e_c^2 = 0.19040(9) (lattice units, N_f = 4 staggered), Z3 <= 1 so e_R^2 <= e_c^2.
  Mental arithmetic of mine: the one-loop electron-only pole is ln(Lambda/m_e) = 3 pi/(2 alpha) = 645.7, i.e. 10^277 GeV, NOT 10^227: I EXPECT the quoted 10^227 to be a typo or a different convention; this is
  a prediction, checked in B1 and reported whichever way it falls. The U(1)_Y one-loop pole I estimate at ~1e41 GeV.
* From Holdom (read): F_1 ~ (3/4) A + ..., singularity at A = 15/2, zeros of 1 + F_1/N within ~e^(-15 pi^2 N/7) of it, chiral-breaking critical value A_crit = N/3 (i.e. alpha_c = pi/3), and the printed expansion (12).
  Reading his eqs. (5)-(7) I resolved two garbled extractions from his printed numerical table (12): F_2's A^4 coefficient is 4961/13824 + 11 pi^4/2880 - 119 zeta(3)/144 and F_4's is 4157/2048 + 3 zeta(3)/8 (the
  '3' being lost in extraction). The script D1 tests these two readings against (12) rather than assuming them.
* Mental arithmetic: my first recollection of the 4-loop QED N_f^3 coefficient had the wrong sign relative to Holdom's F_1 (-1.567); therefore the 4-loop polynomial is NOT used anywhere; only Holdom's printed F_i are used.

## Conventions and inputs (declared)
* a_i = 1/alpha_i, i = (Y, 2, 3), Q = T3 + Y, d a_i/d ln mu = -b_i/(2 pi) - two-loop; inputs at m_Z = 91.1876: set A (127.930, 0.23122, 0.1180) and set B (127.955, 0.23122, 0.1179) as in lanes B/N1/U3.
  Scales: M_P = 1.220890e19, M_red = 2.435e18, X_S = M_red/sqrt(118) = 2.2416e17, X_G = 2e16 GeV (a conventional GUT-scale number, declared, not derived). Imports of lane B `rg_common` and N1 `n1_lib` are READ-ONLY.
* "QED-only toy" (as lane I): photon coupling run with all SM charged fermions (charge-weighted N_c Q^2 threshold sum, lane B fermion tables 1 = current masses "set 1", 2 = constituent masses "set 2") and no electroweak mixing.
  It is a toy: above m_W the photon coupling is not autonomous. It is used only because lane I and Goeckeler et al. use it; the physically meaningful high-scale statement is about U(1)_Y.
* Ladder critical value: alpha_c in {pi/3 (bare vertex, Landau gauge; derived in A1), 0.933667 (Curtis-Pennington; UNVERIFIED snippet)}; group factor C2 = Q^2 (U(1)_em), Y^2 (U(1)_Y, using the vector-like ladder as an ESTIMATE for a chiral gauge theory), 3/4 (SU(2) doublet), 4/3 (SU(3) triplet).
* Bar: lane D `alpha_bar_checker.assess` with log2size = log2(20) (the 20 hit-tests below), n_targets = 1, fitted_reals = 0, scale stated, predicted_precision = 0.01 (declared floor). Bar: P < 1e-3 AND miss <= 5e-10.
* Implied Thomson value for a rule that fixes only a_Y at X: 1/alpha_pred(0) = 137.035999177 + (a_Y^pred(m_Z) - a_Y^meas(m_Z)) (exact at one loop for SM-desert running, a_2 taken at its measured value).
* MUTATE: every script takes `MUTATE` in argv; the mutated run must exit 1 (exit 3 if the control is itself broken, i.e. if the mutation does not change the checked quantity).

## Hypotheses, criteria, and the count of everything that will be tried

### (a) Critical coupling. Script `w2_a1_ladder_critical.py`
* A1 (derivation + numerics). Bare-vertex Landau-gauge ladder bifurcation equation f(x) = (lam/x) Int_0^x y dy f(y)/(y+1) + lam Int_x^{L2} dy f(y)/(y+1), lam = 3 alpha/(4 pi) (Curtis-Pennington's eq. (2.7) with the
  f(y)-f(x) terms dropped; I read it). Analytic claim: power-law solutions x^(-s) with s(1-s) = lam, critical lam_c = 1/4, alpha_c = pi/3, Miransky scaling lam_1(L) - 1/4 = (pi/L)^2 as L = ln(Lambda^2/m^2) -> infinity.
  Numerics: Nystrom discretisation on a log grid, lowest eigenvalue lam_1(L) for L in {10, 20, 40, 80}. PASS iff (i) sympy verifies s(1-s) = lam and the discriminant zero at lam = 1/4, (ii) lam_1(L) - 1/4 within 15% of (pi/L)^2 at
  L = 40 and 80, (iii) extrapolated lam_c = 1/4 within 2% (=> alpha_c = pi/3 to 2%). MUTATE: replace the (lam/x) Int_0^x term by zero (a different kernel): lam_c changes, (iii) must fail.
* A2 (does the SM charged content come near a critical value?). Positive control first: one-loop alpha_s(mu) from m_Z (n_f thresholds at m_b = 4.18, m_c = 1.27) must reach C_F alpha_s = pi/3 (alpha_s = 0.785) at a scale in [0.15, 2.0] GeV
  (the known scale of QCD chiral breaking; the ladder estimate is illustrative). Then compute R = C2 alpha_i(mu)/alpha_c for U(1)_em (QED-only toy, Q = 1), U(1)_Y (Y = 1), SU(2), SU(3) at mu <= M_P with two-loop lane-N1 running.
  Criterion: NEAR-CRITICAL iff R >= 0.5 for an ABELIAN factor at some mu <= M_P. Declared expectation: NO (R ~ 0.02). Also report the one-loop scale mu_c where each abelian factor would reach R = 1 (inverse map, not a test).
  MUTATE: apply the control to the U(1)_em coupling instead of alpha_s (C2 = 1): no crossing in [0.15, 2] GeV, so the positive control must fail.
* A3 (12 hit-tests). Rule "C2_max alpha(X) = alpha_c" for X in {M_P, M_red, X_S} x alpha_c in {pi/3, 0.933667} x coupling in {QED-only toy Q = 1 (set 1 masses), U(1)_Y with Y = 1 (one-loop, SM b_Y)} = 12 variants.
  Each predicts 1/alpha_pred(0) (toy: the run sum S(X) gives 1/alpha_pred(0) = 1/alpha_c + S(X); U(1)_Y: via the bridging rule above). Score miss = 1/alpha_pred/137.036 - 1 against the bar. Declared expectation: all miss by > 20%, all DEAD.

### (b) Landau pole and triviality. Script `w2_b1_landau_poles.py`
* B1 (exact statement + cross-check of the source). One-loop 1/alpha(mu) = 1/alpha_0 - (2/3pi) S1 ln(mu/m): closed-form pole ln(Lambda_L/m) = 3 pi/(2 S1 alpha_0) (sympy). Two-loop with dalpha/dln mu = (2 S1/3pi) alpha^2 + (S2/2pi^2) alpha^3 (S2 = sum N_c Q^4;
  recalled coefficient, consistent with the '3 alpha/4pi' ratio of lane J) solved by mpmath; check it against direct integration of the ODE. Electron only: report log10(Lambda_L/GeV) at one and two loops and compare with the 10^227 GeV quoted by
  Goeckeler et al. (expected to disagree; see above). SM QED-only toy: compare with their 10^34 GeV (PASS iff log10 within 2 of 34).
* B2 (dependence on content). Pole scale (log10 GeV) for: e only; leptons; leptons + quarks (set 1, set 2); + W (b_W = -7, one loop only, toy); full SM U(1)_Y at one loop and at two loops (N1 Runner, a_Y = 0 event, sets A and B);
  U(1)_Y with N extra unit-hypercharge Dirac singlets at 1 TeV, N in {0, 1, 3, 9} (one loop). Criterion "the pole scale is content dependent": max - min of log10(Lambda_L) over the physical variants > 10 decades. Declared expectation: PASS (~240 decades).
* B3 (8 hit-tests). Rule "the Landau pole sits at X" for X in {X_G, X_S, M_red, M_P} x content in {QED-only toy (set 1), U(1)_Y one loop} = 8 variants; same scoring as A3. In addition, for the U(1)_Y rule report the
  number N_Y of unit-hypercharge Dirac singlets at 1 TeV that would be needed for the measured a_Y(m_Z) to have its pole at X (an inverse map of the spectrum, labelled). Declared expectation: all DEAD by > 20% miss; N_Y ~ 8-9 for X = M_P.
* Forced-or-choice: the position of the pole is set by (a_Y(m_Z), the charged spectrum); demanding it at X is a choice of X unless a principle supplies X. No such principle is in the record; this is stated, not tested.
* Joint test (lane U3 scorer): the pole rule constrains only U(1)_Y; SU(2) and SU(3) are asymptotically free (no pole), so the rule gives NO constraint on alpha_2, alpha_3. A rule that does not touch all three couplings cannot be a LEAD by U3's T-IND; stated.

### (c) Compositeness and quasi-fixed points. Script `w2_c1_quasi_fixed.py`
* C1 (what a quasi-fixed point is). sympy: the one-loop Pendleton-Ross fixed ratio rho* = y_t^2/g_3^2 = 2/9 from (16 pi^2) dy_t/dt = y_t (9/2 y_t^2 - 8 g_3^2), (16 pi^2) dg_3/dt = -7 g_3^3 (recalled RGEs; ratio logic only). MUTATE: wrong coefficient (8 -> 0): the fixed ratio must vanish and the check fail.
* C2 (does the abelian coupling have IR focusing?). Exact one-loop: d a_IR/d a_UV = 1 (sympy). Two-loop numerical (N1 Runner, central): change a_Y(M_P) by +-10% and measure the change in a_Y(m_Z), and likewise the ratio a_Y/a_2 at m_Z. Criterion for a quasi-fixed point: |d ln a_IR / d ln a_UV| < 0.1.
  Declared expectation: FAIL (about 0.56 at M_P: additive, no focusing). Also: the only 'saturation' is the triviality bound alpha_IR <= alpha_max(X) = 2 pi/(b ln(X/m)) approached as alpha_UV -> infinity; report alpha_0/alpha_max for X in {X_G, X_S, M_P} for the toy and for U(1)_Y (reported, not scored).
* C3. Compositeness Z3 = 0 (Bjorken/Eguchi: 1/e^2(X) = 0) is EXACTLY the equation 'a(X) = 0', the same as the pole-at-X rule of B3; no separate hit-tests are counted (the eight B3 numbers are its verdict).

### (d) Large-N_f QED. Script `w2_d1_large_nf.py`
* D1 (reproduce the source). With Holdom's eq. (3)-(4), A = N alpha/pi, beta = d ln alpha/d ln mu = (2A/3)[1 + F_1/N + F_2/N^2 + F_3/N^3 + F_4/N^4]: mpmath Taylor coefficients of F_1 = Int_0^{A/3} I_1(x) dx must reproduce Holdom's printed (12):
  1/N coefficients (0.3516, -0.8057, -1.567, 5.342 for A~^1..4, A = 15 A~/2, N = 16 N~) to 3 significant digits; F_2, F_3, F_4 as I resolved them must reproduce the printed 1/N~^2, 1/N~^3, 1/N~^4 coefficients
  (-0.0206 A~^2, -1.602 A~^3, -3.244 A~^4; -0.0555 A~^3; 0.1198 A~^4). PASS iff all agree to 3 digits. Also: F_1 has a log singularity at A = 15/2 (Holdom eq. (8): F_1 ~ (7/(15 pi^2)) log|1 - 2A/15| + 0.3056) checked numerically. MUTATE: I_1 with sin^3 -> sin^2: D1 must fail.
* D2 (fixed points). Zeros of 1 + F_1(A)/N (all orders in A, principal value) and of the truncated sum through F_4 for N in {1, 2, 4, 8, 12, 16} in A < 15/2. Record A*, alpha* = pi A*/N, and compare with the ladder critical A_crit = N/3.
  Declared classification: any zero found is a scheme-dependent (MS-bar), 1/N-truncated statement (Holdom himself says the zeros in the truncated sum occur where higher orders cannot be ignored); UNDECIDED at best; never a value of alpha_0.
  Sub-question: does the SM's N_eff = sum N_c Q^2 = 8 apply? NO in general (F_1 is derived for N identical charged fermions); the number is reported for N = 8 only as a magnitude.
* D3 (what a UV fixed point does to the IR value). Exact statement for ANY one-coupling beta function with alpha(mu) flowing from a UV fixed point: alpha_0 = alpha(m_e) is a one-parameter function of ln(Lambda_*/m_e); the trajectory is unique, alpha_0 <-> Lambda_*/m_e is 1:1 (dimensional transmutation).
  Numerics: integrate d ln mu = dA/(A beta) with the all-order-in-A F_1 beta function, N = 1 and N = 8: report ln(mu/m) needed to run from A_0 = N alpha_0/pi to A = 5, 7, 7.4 and compare with the one-loop values. Reported, not scored. INVERSE MAP: labelled.

### (e) Ward identity, Z3 and the bare-versus-physical charge. Script `w2_e1_ward_z3.py`
* E1. With explicit 4x4 Dirac matrices (sympy): the differential Ward identity d S/d k_mu = -S gamma^mu S for S = (kslash - m)^-1, hence Lambda^mu(p,p) = -d Sigma/d p_mu at the integrand level and Z1 = Z2 for any regularisation
  that preserves it. PASS iff exact for all four mu. MUTATE: replace gamma^mu by gamma^mu gamma5 on one side: must fail.
* E2. Kaellen-Lehmann: 1/Z3 = 1 + Int rho(s) ds/s with the one-loop spectral density rho = (alpha/3pi)(1 + 2m^2/s) sqrt(1 - 4m^2/s) >= 0; numerically 1/Z3 - 1 = (alpha/3pi)[ln(L/m^2) + c], report c (mpmath), and check Z3 in (0,1) for L in {1e2, 1e6, 1e30, 1e100} m^2.
  Consequence stated: e_R^2 = Z3 e_0^2 <= e_0^2 for a positive-metric theory (bound, not value). MUTATE: flip the sign of the (2m^2/s) term's range (rho negative for s < 4m^2 region included): the positivity check must fail.
* E3. Charge ratios: with several species of charges Q_i and one Z3, the ratio of physical charges equals the ratio of bare charges to all orders (exact, sympy on the beta functions). Not a selector of e.
* E4 (statement only, no computation). Exact eigenvalue conditions of Johnson-Baker-Willey/Adler type presuppose a zero of the Gell-Mann-Low function; the lattice and functional-RG results read (Goeckeler et al.: no UV zero out to e_R^2 = e_c^2; Gies-Jaeckel: fluctuation-induced
  corrections give only 0 < eta_F^(1-loop)/2 <= eta_F, no fixed point at e^2 > 0 for any regulator in their truncation) do not support one; and even with a zero at alpha_1 the IR value is set by the flow (D3). Sourced, not computed.

### Verdict script `w2_f_verdicts.py`
Collects the JSON outputs, calls lane D's assess for the 20 hit-tests, applies the rules below, and prints the table. MUTATE: force miss = 0 into the bar with fitted_reals = 1 (must fail).

## Verdict rules (declared)
* DEAD: the sub-question's only exact statement is an inequality, an identity, or depends on a free quantity (bare coupling, cutoff, spectrum); or every scored variant misses by more than its tolerance (max(2 x spread over the running variants, 1%)).
* UNDECIDED: a result exists but is scheme dependent, truncated, or outside the domain where the derivation is controlled (D2).
* LEAD: a rule with zero free reals that (i) predicts 1/alpha_0 within tolerance, (ii) clears lane D's bar, (iii) passes the joint test on alpha_Y, alpha_2, alpha_3 (lane U3's T-JOINT/T-IND). A LEAD is not announced; the equation, scale and joint test are reported for adversarial follow-up.
* Total scored hit-tests: 12 (A3) + 8 (B3) = 20. Nothing else is tried. Anything added later goes into an Amendment below and is counted.

## Expected outcome (stated in advance)
No LEAD. (a) DEAD: alpha_c ~ 1 is 140x the Thomson value and ~60x alpha_Y(M_P); no SM abelian coupling is near critical below M_P; the same criterion does fire for QCD near 1 GeV (control). (b) DEAD: the pole is a function of the spectrum and a_Y(m_Z); it is a spectrum-and-choice statement.
(c) DEAD: no IR focusing for abelian couplings; compositeness = pole. (d) UNDECIDED at most: 1/N_f truncated zeros near A = 15/2 are scheme dependent and trade alpha_0 for Lambda_*/m. (e) DEAD as a selector: Z1 = Z2 and Z3 <= 1 give identities and an inequality.

## Amendments
(none yet)

### Amendment 1 (2026-09-29, after the FIRST RUN of `w2_b1_landau_poles.py`, output kept as `w2_b1_landau_poles_FIRSTRUN.out`)
Check B1b failed at its pre-registered tolerance of 1e-6 in ln(Lambda/m) (closed form 638.187790, ODE 638.187785). Diagnosis: the ODE integration stops when u^2 < 1e-12, i.e. at u = 1/alpha = 1e-6, which lies
u/b1 = 1e-6/0.2122 = 4.7e-6 in ln mu short of the exact pole; the observed difference (5e-6) is that stop offset and not a physics discrepancy. The tolerance is set to 5e-5 (no other change). All other checks were unaffected.
Also disclosed: my declared expectation 'N_Y ~ 8-9 for X = M_P' (B3) was mental arithmetic and is wrong; the computed value is 7.06 (it was not a pass/fail criterion).

### Amendment 2 (2026-09-29, after the FIRST RUN of `w2_c1_quasi_fixed.py`, output kept as `w2_c1_quasi_fixed_FIRSTRUN.out`)
The focusing CONTROL C1b (elasticity of y_t(m_Z) to y_t(M_P) at the pre-registered y_UV = 1) returned 0.150, above the 0.10 criterion. Diagnosis: without QCD the elasticity is (1/y_UV^2)/(1/y_UV^2 + kappa) with kappa = 9 ln(M_P/m_Z)/(16 pi^2) = 2.245,
i.e. 0.31 at y_UV = 1; QCD lowers it to 0.15. The measure is working; a Yukawa starting at 1 is only mildly focused over 39 e-folds. The control point is moved to y_UV = 2 (values at 1, 2, 3 are all printed). The criterion (< 0.1) and the
abelian tests (C2, elasticity ~0.56) are unchanged, and the control is not used to make any physics claim pass; it only certifies that the measure can return a small number when a quasi-fixed point exists.
Amendment 3: the first version of `w2_lib.pole_scale_oneloop` had the sign of the W-threshold term wrong (found by direct re-evaluation of 1/alpha at the returned pole); it affected only one row of the B2 table (10^103.7 -> 10^96.4 GeV, toy, W included), no check. The FIRSTRUN output of B carries the wrong row.

### Amendments 4 and 5 (2026-09-29, after the FIRST RUN of `w2_d1_large_nf.py`, output kept as `w2_d1_large_nf_FIRSTRUN.out`)
D1 (all ten printed coefficients of Holdom's (12), the residue and the constant 0.3056) PASSED at first run; my two readings of F_2 and F_4 are therefore confirmed by his printed numbers.
Amendment 4: D2 returned nan for N >= 4, because the zero sits 10^-39 (N = 4) ... 10^-150 (N = 16) from the pole, below the precision of the direct quadrature. Diagnosis: numerical, not physical (N = 1, 2 converged with |1+F_1/N| ~ 1e-41 and matched Holdom's eq. (9) prefactor to 0.2%).
Fix: use the exact asymptotic form F_1 = c1 ln(1 - 2A/15) + K0 (K0 computed once, validated against the direct result for N = 1, 2 and against D1c). No physics changed.
Amendment 5: D3b ('the all-order correction to the one-loop scale ratio is < 1 e-fold') FAILED: the correction is -6.3 e-folds for the electron alone (639.12 vs 645.47). Diagnosis: my criterion was a wrong mental estimate; the leading correction is
-(9/8) ln(A_top/A_0) e-folds (three-loop-like double-log accumulation of the (3/4)A term of F_1) and agrees in sign and size with the two-loop closed form of B1 (ln(Lambda/m) 645.7 -> 638.2). The check is restated (negative, 0.3-3% of ln); the finding is that
a percent-level change in ln(mu/m) is a factor e^6 ~ 600 in the pole scale: 'the pole sits at exactly X' is not even sharp at fixed loop order.
Amendment 4b (same run, second diagnosis): the first attempt at K0 gave 3.07 instead of 0.3055: my guard that shifts x off a Gamma-function pole (|x - k/2| < 1e-30) mis-evaluated the integrand within 1e-30 of x = 5/2 while the subtracted term r/(5/2 - x) was not shifted. K0 is now integrated to 5/2 - 1e-10, and
the asymptotic form is validated by direct quadrature at eps = 1e-6, 1e-8, 1e-11 (check D2y) instead of at eps ~ 1e-36, where the direct quadrature itself is unreliable for the same reason. No physics changed.

### Amendment 6 (2026-09-29, after the FIRST RUN of `w2_f_verdicts.py`, output kept as `w2_f_verdicts_FIRSTRUN.out`)
Gate G3 (the bar's positive control, miss 1e-12) failed because my wrapper applies the declared 1% predicted-precision floor to every call, which makes delta_eff = 1e-2 and fails the bar's precision criterion by construction. Diagnosis: a defect of my control, not of the bar
(lane D's own selftest uses predicted_precision = 0). The control now uses 0; the twenty hit-tests are still scored with the declared 1% floor (which cannot help them: the bar also demands miss <= 5e-10). All twenty verdicts were identical in the first run.
