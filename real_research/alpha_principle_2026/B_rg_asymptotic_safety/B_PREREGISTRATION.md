# Lane B -- renormalization-group / asymptotic-safety routes to alpha (pre-registration)

Written 2026-09-28 BEFORE any script in this directory was run. Literature was read first (see "What was read"); no numerical computation of this lane existed
at the time of writing. Amend only by appending an "Amendment" section at the bottom.

## Question

Does the asymptotic-safety (AS) literature on the U(1) gauge coupling under gravity give a FORCED number for the infrared fine-structure constant, or only
the existence of a fixed point / irrelevant direction with inputs still free? And what boundary value of alpha at natural high scales is required to reach
alpha^-1(0) = 137.035999177 (Thomson limit), and does any forced fixed-point / attractor value equal it?

Scale statement: the target is the Thomson-limit value alpha(q^2 = 0). Any principle tested here must state how it is run to that scale; below the electron
mass alpha does not run, so alpha(0) = alpha(m_e) up to the usual on-shell conventions.

## What was read (fetched and read by this lane, not recalled)

* Harst and Reuter, "QED coupled to QEG", arXiv:1101.6007 (full text read: sections 2-5, 7).
* Eichhorn and Versteegen, "Upper bound on the Abelian gauge coupling from asymptotic safety", arXiv:1709.07252 (full text read: sections 2, 4, 5, beta functions 4.1-4.11).
* Riabokon, Schiffer, Wagner, "Regulator and gauge dependence of the Abelian gauge coupling in asymptotically safe quantum gravity", arXiv:2508.03563
  (introduction, section II and III text read; used only for the statement of truncation/regulator/gauge dependence of f_g).
* Abstracts only (NOT read in full, so used only as pointers): Christiansen and Eichhorn arXiv:1702.07724; Daum, Harst, Reuter arXiv:0910.4938;
  Eichhorn, Kwapisz, Schiffer arXiv:2112.09772; Wetterich arXiv:2205.07029; Sen, Wetterich, Yamada arXiv:2111.04696.

## Structure of the claim from the literature (to be reproduced, not assumed)

Both routes have the form beta_alpha = (matter, screening, >0) alpha^2 - (gravity, from G(k) k^2 alpha) with the gravity term linear in the coupling.
* Fixed point 1: alpha* = 0 (free). Then the IR value is a free parameter (Harst-Reuter NGFP1; Christiansen-Eichhorn; Eichhorn-Versteegen Gaussian FP).
* Fixed point 2: alpha* != 0, UV-repulsive, so ONE trajectory ends there and the IR value is predicted (Harst-Reuter NGFP2; Eichhorn-Versteegen interacting FP).
Predictivity here means "the IR alpha is a function of the gravity-sector fixed-point numbers, the regulator/truncation, the charged particle content and the masses".
The pre-registered task is to say whether that function returns 137.036 without a free choice.

## Hypotheses

* H-A (structure): at NGFP2 the predicted alpha_IR^-1 is dominated by one-loop matter running between M_Planck and the charged masses,
  alpha_IR^-1 ~ sum_f (2 N_c Q_f^2 / 3 pi) ln(M_Pl/m_f) + O(A), so it is set by the charged content and the MEASURED masses, and is insensitive (<20 percent) to the
  gravity coefficient (Phi g*) over two decades. Expected: TRUE.
* H-B (Harst-Reuter number): with SM-like charged content the NGFP2 prediction is not 1/137.036 (expected: it is within a factor of order unity, but not a hit at 1e-3).
* H-C (Eichhorn-Versteegen): the IR value is fixed only for the hypercharge coupling g_Y, through f_g(G*, Lambda*), which depends on the truncation. The
  electromagnetic alpha = g_Y^2 g_2^2/(4 pi (g_Y^2 + g_2^2)) additionally needs g_2, whose beta function has no interacting fixed point, so g_2 stays free.
  Expected: alpha_em is NOT predicted even inside the scenario.
* H-D (required boundary): for the SM one-loop running from the measured alpha(M_Z) (which already contains the hadronic vacuum polarisation), the value alpha_em^-1
  required at M_Planck is about 100-110, at the GUT scale about 80, and it is NOT the value of any fixed point of the literature (expected: no match).
* H-E (honesty about inputs): no FORCED fixed-point/attractor value in the literature equals the required boundary value to 1e-3, and none of the predicted
  alpha_IR hits 1/137.036 to 1e-3 without a value of f_g (or n_F) chosen after seeing the target.

## Fixed inputs (measured, declared before running; masses are MEASURED inputs, nothing is derived)

alpha^-1(0) = 137.035999177 (CODATA 2022); alpha^-1_MSbar(M_Z) = 127.930; sin^2 theta_W(M_Z, MSbar) = 0.23122; alpha_s(M_Z) = 0.1180; M_Z = 91.1876 GeV;
m_t = 172.57 GeV; M_Planck = 1.220890e19 GeV; reduced M_Planck = 2.435e18 GeV.
Charged-fermion masses, SET (i): e 0.000510999, mu 0.1056584, tau 1.77686, u 0.00216, d 0.00467, s 0.0934 (MSbar at 2 GeV), c 1.27, b 4.18, t 172.57 GeV.
SET (ii): as (i) but the light quarks replaced by effective constituent-type masses u = d = 0.336, s = 0.5 GeV. The two sets only bracket the hadronic non-perturbative
region; the difference is reported, neither is preferred.
One-loop coefficients (GUT-free normalisation, alpha_Y = (3/5) alpha_1): b_Y = 41/6, b_2 = -19/6, b_3 = -7 (dalpha^-1/dln mu = -b/(2 pi)).
Two-loop SM b_ij = [[199/50, 27/10, 44/5],[9/10, 35/6, 12],[11/10, 9/2, -26]] (GUT-normalised 1,2,3), top-Yukawa coefficients (17/10, 3/2, 2), y_t(M_Z) = 0.94 (used only
to size the two-loop shift; not a target).

## Computations to be done, and their count (declared now)

Script b1_reproduce_literature.py:
* H1: numerical Riccati integration of Harst-Reuter eq (4.2b) from the fixed point equals their closed form (5.6) to 0.5 percent (n_F = 1, Phi = 1, g* = 1.7136 from B1(0) = -(24 Phi22 - Phi11)/(3 pi)).
* H2: reproduces their quoted alpha_IR^-1 = 10.91 n_F (g* = 1.71) and 10.96 n_F (g* = 0.83 quoted), tolerance 2 percent.
* H3 (informational): their SM (A = 41/(20 pi), down to M_Z) 1/25.7 and MSSM 1/41.3, tolerance 3 percent.
* H4 sensitivity (not a target scan): alpha_IR^-1 as g* runs over [0.1, 10] at fixed n_F; gating: spread < 20 percent. Also the real n_F needed for 137.036.
* H5: alpha*/pi = 9 Phi g*/(pi n_F) = 0.38 for n_F = 13 (their remark), tolerance 3 percent.
* E1: solve the fixed point of Eichhorn-Versteegen eqs (4.8)-(4.9) with N_D = 45/2, N_S = 4, N_V = 12; expect (G*, Lambda*) = (2.73, -3.76), tolerance 2 percent.
* E2: f_g = G(1-4L)/(4 pi (1-2L)^2), g_Y* = 4 pi sqrt(6 f_g/41), run to 173 GeV with b_Y = 41/6 from M_Planck: expect 1.05 and 0.487, tolerance 2 percent.
* E3: the f_g required for g_Y(173 GeV) = the measured value (0.358): expect 0.096/pi^2 within 3 percent; report elasticity d ln g_IR / d ln f_g and the f_g precision needed for 1e-3.
* E4: g_2 has no interacting fixed point: real roots of beta_2 = -b g^3/(16 pi^2) - f g (b = 19/6) for f >= 0 are only g = 0.
MUTATE: sign of the gravity term flipped in the Riccati integration (must break H1) and sign flipped in the E-V beta_G (must break E1).

Script b2_required_boundary.py:
* R1: naive QED-only threshold running from alpha^-1(0) to M_Z with SET (i) and (ii) against the measured 127.930 (reports the size of the hadronic non-perturbative gap; informational).
* R2: from the measured alpha(M_Z), sin^2 theta_W, alpha_s: SM one-loop alpha_Y^-1, alpha_2^-1, alpha_3^-1 and alpha_em^-1 = alpha_Y^-1 + alpha_2^-1 at the 4 scales
  {M_reduced-Planck, M_Planck, 2e16 GeV, the computed alpha_1 = alpha_2 crossing}. Two-loop estimate at the same 4 scales; the relative one-loop/two-loop difference is the
  truncation error of the required value (gating: reported; if it exceeds 1e-3 then no hit at 1e-3 could be claimed from one-loop).
* R3: the SM one-loop couplings do NOT meet at one point (gating: max spread of alpha_i^-1 at the best scale > 5 percent); MSSM coefficients would (used only as the MUTATE control).
* R4: U(1)_em-only toy (SM charged fermions, no W, anchored at measured alpha(M_Z)): required alpha^-1 at the same 4 scales, to show the required boundary value depends on the assumed content.
MUTATE: use MSSM coefficients in R3 (must make the 'does not unify' check FAIL).

Script b3_forced_vs_required.py: the trial list (fixed, 5 predictions + 3 boundary comparisons = 8 trials):
* C1 HR NGFP2, n_F = 1, g* = 1.7136 -> alpha_IR^-1.        * C2 HR NGFP2, n_F = 1, g* = 0.83 (quoted) -> alpha_IR^-1.
* C3 HR NGFP2 with SM charged fermions, SET (i) masses, U(1)_em toy -> alpha_IR^-1.       * C4 same with SET (ii).
* C5 E-V interacting fixed point (published G*, Lambda* as reproduced in E1), hypercharge run to M_Z, combined with the MEASURED alpha_2 and the measured hadronic-inclusive
  offset alpha^-1(0) - alpha^-1(M_Z) = 9.106 -> alpha_em^-1(0).
* B1-B3: the fixed-point boundary values (C1, C2: alpha*; C5: alpha_Y*) compared with the required boundary value at M_Planck from b2 (R2 for the em chain; alpha_Y* against required alpha_Y^-1 at M_Planck).
Hit = relative agreement < 1e-3 (no route here predicts a precision). Expected chance hits: N_trials x (2e-3 / ln(1000)) with a log-uniform prior on alpha over three decades
(computed in the script). The control C6 (NOT counted as a trial) solves for the f_g or n_F that DOES hit, to show a tuned value can hit but is chosen after the target.
MUTATE: promote C6 into the counted trials; the 'no forced hit' verdict must FAIL.

## Pass / fail criteria (declared now)

* A forced principle FIXES alpha only if some counted trial hits AND that value is forced with no free parameter chosen after the target AND the scale statement holds.
* Expected (stated in advance): the literature reproduces at the quoted precision; NO counted trial hits; alpha_em is not predicted even inside the E-V scenario because g_2 is free;
  the IR value is set by charged content and measured masses (H-A); required boundary values are not any fixed-point value; the gravity coefficient is truncation- and regulator-dependent
  (f_g = 0 possible in some regulators; no PMS point with SM matter per arXiv:2508.03563). Verdict expected: NO forced principle.

## Scope / not tested

Not tested: recomputing the gravity fixed point or f_g beyond the published truncations (that is a research programme, not a script); non-Einstein-Hilbert truncations, higher-derivative gravity,
the Standard-Model-with-full-FRG results of other groups (only abstracts read); GUT-completed gauge groups with their own fixed points; the sign question of the gravity contribution
(scheme-dependent per arXiv:2508.03563 and the Harst-Reuter caveat). kappa = 1/2 stays FITTED; the SM mass sector stays walled (masses are measured inputs).

## Amendment 1 (appended after the runs; nothing above was edited)

* Added at scripting time, not pre-registered as gates: b3 structural checks S1-S3, S5 (S5: the observed alpha lies inside the Eichhorn-Versteegen allowed region, which is an upper bound on alpha).
  They do not change any pre-registered verdict.
* In b1, check H4b (no integer n_F hits 137.036) and H0 (g* = 1.7136 from Phi11 = 1, Phi22 = 1/2) were added as consistency checks on the reproduction.
* Results (all scripts exit 0; all MUTATE controls exit 1): H1, H2, H3, H5 reproduce Harst-Reuter to 1e-2 or better (10.914 vs 10.91; 10.958 vs 10.96; SM 25.67 vs 25.7; MSSM 41.32 vs 41.3).
  E1-E3 reproduce Eichhorn-Versteegen ((2.726, -3.758) vs (2.73, -3.76); g_Y* 1.053; g_Y(173) 0.4845 vs 0.487; required f_g = 0.0968/pi^2 vs 0.096/pi^2).
  H-A TRUE (spread 8 percent over 100x in g*). H-B TRUE. H-C TRUE (g_2 has only g = 0). H-D TRUE: required alpha_em^-1 = 104.9 at M_Planck, 108.7 at 2e16 GeV; two-loop shifts it by 0.5-0.7 percent.
  H-E TRUE: 0/8 counted trials hit; expected chance hits 2.3e-3.
* Verdict: NO forced principle. See the lane report for the discussion.
