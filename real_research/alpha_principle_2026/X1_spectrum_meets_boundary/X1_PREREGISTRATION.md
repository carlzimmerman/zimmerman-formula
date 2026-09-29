# X1 -- the forced charged spectrum meets the forced ultraviolet boundary (pre-registration)

Written 2026-09-29 BEFORE any script of this lane was written or run. No number of this lane has been computed when this file is written. What I read first (labelled): 
READ IN FULL: `ALPHA_PLAIN_SUMMARY.md`, `ALPHA_CHAIN_STATUS.md`, `U3_invented_uv_boundary/u3_lib.py`, `U3_invented_uv_boundary/U3_PREREGISTRATION.md`, `U3_invented_uv_boundary/u3_1_score.out`,
`B_rg_asymptotic_safety/rg_common.py`, `W1_division_algebras/w1_5_couplings_and_scale.py`, `N1_joint_couplings/n1_lib.py` (running, scorer). READ IN PART: `W1_division_algebras/w1_lib.py` (first 80 lines),
`W1_division_algebras/w1_4_jordan_f4_e6.py` (docstring, the E6 27 decomposition and the checks J4b-J4f), `N2_emergence_tower/tower_lib.py` (first 120 lines: the group-theory bookkeeping and the dof counts),
`W2_nonperturbative_qed/w2_b1_landau_poles.py` (first 60 lines), `D_calibration_bar/{alpha_bar_checker.py,bar_lib.py,D_PREREGISTRATION.md}` (interfaces and definitions).
RECALLED (not looked up, labelled at each use): the two-loop group-theory formula for a product gauge group (validated by a gate against the SM matrix of lane N1), the proton-decay lifetime scaling and the
Super-Kamiokande bound, the collider mass floors for exotic states, the heterotic relation M_str = 0.216 g_str M_red (lane U3's recalled constant, not re-derived here). No paper is opened by this lane.

Nothing here derives alpha. alpha stays an INPUT; kappa = 1/2 stays FITTED; the Standard Model mass sector stays walled.

## Amendment A0 (visible; constraint received from the coordinator before any script of this lane was run; it changes the scoring below)

The only free constants allowed in this lane are the framework's own two, kappa = 1/2 and Z = 2 sqrt(8 pi/3) (as in a0 = c H_Lambda / Z), plus pi and integers fixed by group theory. Everything else is
either a MEASURED input (the couplings at m_Z, the SM masses and spectrum) or must be DERIVED. Consequences adopted here:
(1) Every exotic-state mass, threshold scale and unification scale that would otherwise be a free parameter is a FORBIDDEN KNOB. A pair that works only by choosing them is a RE-FIT and counts as a FAILURE under this rule, not as a lead.
(2) For every (spectrum, boundary rule) pair I report separately the ZERO-KNOB prediction (Track Z below) and whether it matches the three measured couplings jointly and alpha(0) within the running's stated uncertainty.
(3) If a zero-knob pair fails, I state by how much and whether the miss exceeds the running's uncertainty (the factor |r|/tol).
(4) kappa and Z are not used as fitting handles. STATEMENT: NO boundary rule registered in this lane contains kappa or Z. Their fixed numerical content in every rule is therefore nil. (Z appears nowhere; kappa appears nowhere.)
The original instruction (count free parameters honestly, ask whether ANY choice of them works, report excess predictions) is kept as Track K, because it answers "what would the cure cost"; under A0 a Track-K pair can never be a
lead of the framework, only an information item about what the knobs would have to be.
What a "zero knob" mass prescription can be: an exotic mass cannot be derived in this programme (the SM mass sector is walled), so the ONLY parameter-free prescriptions are the two limits that use no number
chosen by me: P_dec (exotic states decoupled at the boundary scale itself, so they never enter the running: identical to the SM-desert run) and P_EW (exotic masses equal to the measured input scale m_Z,
the no-decoupling limit; collider-excluded, recalled, so it is a bound on what the maximal effect of the exotic content can be, not a viable model). Both are pre-registered discrete prescriptions, counted as trials.

## Why this lane and what counts

The record isolates two missing ingredients for a derivation of alpha: (i) the charged spectrum above m_e, (ii) a forced ultraviolet boundary value of the gauge couplings. Lane W1 finds an algebraic charged spectrum
(SM + nu_R; E6 27 with 11 exotic states; Spin(10) 16; SM + B-L) but no coupling; lane U3 finds that 33 of 34 invented boundary rules die on the joint (alpha_Y, alpha_2, alpha_3) test, mostly by the matter-monotone rule.
X1 puts the two together: each forced spectrum with each natural forced boundary rule, the running done with the correct one- and two-loop coefficients for THAT spectrum (not the SM desert plus a one-loop shift).
Counting rule (the whole point): a pair is a LEAD only if it works with strictly fewer free parameters than independent tests; a pair with excess predictions <= 0 is a re-fit. Solving a rule for the target is an inverse map, not a test.

## Numbers KNOWN before this pre-registration (disclosed; nothing of mine has been computed)

* From lane U3's committed output (u3_1_score.out): the SM-desert two-loop run with the top threshold gives, at the a_1 = a_2 crossing X = 1.091e13 GeV, a_3/a_2 residual +0.131 (tol 0.042); at X_P = 1.221e19 GeV the GUT-normalised a_1/a_2 residual is +0.486 and a_3/a_2 -0.071; at X_P in the Y normalisation -0.108 and -0.071;
  dual-Coxeter absolute residuals at X_P are (+0.898, -0.489, -0.288) for (a_Y, a_2, a_3); heterotic locking gives X = 2.711e17 GeV with residuals (+0.329, -0.029); all-three emergence at M_red/sqrt(118) leaves all three couplings at the SM value (residual -1).
  Consequently for every pair whose exotic content is decoupled (P_dec) the result is ALREADY KNOWN from U3 and is reproduced, not discovered.
* From lane W1: one E6 exotic set per 27 (D, D^c, two doublets, singlet S) shifts (b_Y, b_2, b_3) by (10/9, 2/3, 2/3); three sets at 1 TeV shift 1/alpha_em(M_P) by -30%. From lane N1: SU(5)/SO(10) with the SM desert misses alpha_3 by -11.6% (two loop).
* My own unscripted expectations (stated so they can be false; see the Expectations section).

## Conventions and inputs (identical to lane U3 unless stated)

* a_i := 1/alpha_i, i = Y, 2, 3, alpha_Y in the normalisation Q = T3 + Y (b_Y = 41/6); GUT-normalised a_1 = (3/5) a_Y. Inputs at m_Z = 91.1876 GeV (set A: 1/alpha_em = 127.930, sin^2 = 0.23122, alpha_s = 0.1180; set B: 127.955, 0.23122, 0.1179).
  1/alpha(0) = 137.035999177 (Thomson, INPUT); the hadronic-inclusive offset 1/alpha(0) - 1/alpha(m_Z) = 9.106 is a MEASURED input (lane B): alpha(0) is tied to alpha(m_Z) by measured running below m_Z and is tested through a_Y + a_2 at m_Z.
* Scales: X_P = 1.220890e19, X_R = 2.435e18, X_S(N) = X_R / sqrt(N) GeV (species scale; N = 118 for the SM count, and 118 + 22 N27 for the E6 content: 22 = dof of the 11 exotic Weyl multiplets of one 27: 2 colour triplets x 3 x 2 = 12, two doublets x 2 x 2 = 8, one singlet x 2 = 2). Lane C's alternative count 126 (118 + 3 nu_R + graviton) is carried for the emergence rules only, as in U3 (126 + 22 N27).
* Running: my own implementation `x1_lib.py`, which GENERALISES lane U3's runner: the same top threshold (Delta b_top = (17/18, 1/2, 2/3) removed between m_Z and m_t = 172.57, y_t(m_t) = 0.9334) and the same seven variants {2L-T, 2L-A, 2L-B, 2L-TB, 1L-T, 1L-A, 1L-B}, but with the
  one- and two-loop coefficients (b_i, B_ij) built FROM THE FIELD CONTENT by the general two-loop formula, with step thresholds at the exotic masses in both b and B: Weyl fermion: T_i (2/3) in b, and T_i (2 sum_j C_j g_j^2 + (10/3) C_A(i) delta_ij) in B;
  complex scalar: T_i (1/3) in b and T_i (4 sum_j C_j g_j^2 + (2/3) C_A(i) delta_ij) in B; gauge: b = (0, -22/3, -11), B_ii = -(34/3) C_A(i)^2. Yukawa terms: the SM top Yukawa only (as in U3); exotic Yukawa couplings are NEUTRALISED (declared approximation, no exotic Yukawa exists in the record).
  No threshold matching corrections (continuous a_i at every threshold, MSbar step approximation). Three-loop terms are covered by the 1% floor below (declared, as in U3).
* Test scorer: lane U3's T-JOINT verbatim: residuals r_k are zero when the rule holds; tol_k = max(2 band_k, 0.01) where band_k = max over the running variants (and X x 0.5, X x 2 for species-scale variants) of |r_k(variant) - r_k(central 2L-T)|; PASS iff |r_k| <= tol_k for all k.
  Residual definitions are U3's: ratio rule r = target/actual - 1; absolute rule r = (pred_j - A_j)/ref_j with ref_j = the SM-desert run of the same variant at the same scale (so that exotic content moves r, and r = -1 means "the coupling has not moved from the desert value").
* T-DOMAIN (a solved scale X > 1.001 X_P is DEAD by domain); T-MONO (an absolute rule predicting a_j ABOVE the run beyond tol cannot be repaired by added matter; here checked on the ACTUAL run for the actual content and, for Track K, over the whole knob box).
* T-ABS (does the pair predict alpha(0)?): only the absolute rules (dual-Coxeter, emergence) specify both a_Y and a_2 as numbers. Implied 1/alpha(0) = 137.035999177 + (pred_Y - A_Y) + (pred_2 - A_2) at X (U3's translation, checked in a gate against an exact one-loop down-run).
  Lane D's bar is applied with `alpha_bar_checker.assess(delta = |implied/137.035999177 - 1|, log2size = log2(81), n_targets = 1, predicted_precision = tol_em, fitted_reals = 0, scale_stated = True)`; tol_em = max(2 x spread of the implied value over the running variants, 0.01).
  Relational rules (ratio rules) leave the overall coupling as an INPUT: they do not predict alpha(0), stated per pair as "alpha(0) is an input; bar N/A".
* Inequality checks (never counted as independent equalities, reported per pair): C6a proton lifetime, recalled scaling tau_p ~ 1e35 yr (M_X/1e16 GeV)^4 (0.025/alpha_G)^2 with M_X = X, uncertain by a factor 10; bound 2.4e34 yr (Super-Kamiokande, recalled): PASS if tau >= 2.4e34, UNCERTAIN if within a factor 10 below, FAIL otherwise; only for unified rules.
  C6b collider floors (recalled): colour-triplet exotic mass >= 1 TeV, charged doublet exotic mass >= 100 GeV; P_EW violates both by construction (flag only). C6c perturbativity: all a_i >= 1 up to X (the runner stops at a_Y = 1). C6d the U(1)_Y Landau-pole scale of the run (where a_Y = 1 is reached by the run, then extrapolated linearly to 0 with the local slope) is REPORTED as a predicted number, with no data to compare against.

## The spectra (W1's forced list; the group theory is in W1, not re-derived)

* S1  SM + 3 nu_R (nu_R is a neutral SM singlet: it enters neither b nor B). Running IDENTICAL to the SM desert. No unifying group is assumed (only relations among the three couplings can be imposed).
* S2  Spin(10) 16 x 3 (complete multiplets; the running below the boundary X is the SM desert plus nothing). Group above X: Spin(10), dual Coxeter number h = 8, GUT normalisation a_1 = a_2 = a_3 = a_G.
* S3  E6 27 x N27 (N27 in {1, 3}); each 27 = 16 + 10 + 1 adds the exotic Weyl multiplets D (3,1,-1/3), D^c (3bar,1,+1/3), two doublets (1,2,+1/2) and (1,2,-1/2), and a singlet S (neutral). Vector-like masses: M_D (D and D^c together), M_H (the two doublets together), S neutral.
  Generations degenerate (M_D, M_H shared by all N27; non-degenerate generations only add parameters). Group above X: E6, h = 12, GUT normalisation (16 -> SM as in S2).
* S4  SM + gauged U(1)_(B-L) (W1's 5-parameter case): Spin(10) -> SU(3) x SU(2) x U(1)_R x U(1)_X (X = (B-L)/2, Y = T3R + X) at an intermediate scale M_BL, minimal scalars H (T3R = 1/2, X = 0) and S with charges (T3R, X) = (1, -1); the kinetic matrix a_ab (3 entries) runs at one loop above M_BL
  (SU(3), SU(2) unchanged, two-loop cross terms of the intermediate segment neglected: declared). Track K only (a zero-knob M_BL does not exist except M_BL = X, which is S2).

## The boundary rules (each stated in full; the numerical content is all integers, pi, and group theory)

* R-A(X)  GUT-normalised equal couplings at a fixed programme scale X in {X_P, X_R, X_S}: a_1 = a_2 = a_3. Residuals: a_1/a_2 - 1 type ratios (U3 P03 GUT). K = 2 equalities. Relational.
* R-B  GUT-normalised equal couplings at the a_1 = a_2 crossing X_c (the crossing scale is derived by the rule): a_3 = a_2 there. K = 2 (crossing + a_3 = a_2), u = 1. Relational.
* R-C(X)  Y-normalised equal couplings at X in {X_P, X_R, X_S}: a_Y = a_2 = a_3 (U3 P03 Y). Only for S1 (no group embedding fixes k_Y = 1; it is the level-1 hypercharge that a product of three U(1)/SU(N) factors would have). K = 2. Relational.
* R-D  dual-Coxeter absolute couplings (1/g^2 = h): S1: (a_1, a_2, a_3) = 4 pi (5, 2, 3) (U3 P01: the SU(5) parent's h = 5 for the abelian factor), at X in {X_P, X_S};
  S2: all three GUT-normalised couplings = 4 pi * 8 (Spin(10)); S3: all = 4 pi * 12 (E6); for S2 and S3 at X in {X_P, X_S} and at the crossing X_c (residuals: a_3/a_2 and a_2 = 4 pi h, U3 P02). K = 3 absolute (fixed X) or 3 (crossing). Absolute: predicts alpha(0).
* R-E  heterotic string-scale locking (gauge-gravity relation): equal GUT-normalised couplings at X_het solved from X = 0.216 g_str M_red, g_str^2 = 4 pi / a_2(X) (RECALLED constant, not re-derived). K = 3 (two equalities + the scale relation), u = 1. Relational (a_G follows from the scale).
* R-F  emergence of all three couplings at the species scale: a_Y = a_2 = a_3 = 0 at Lambda = M_red / sqrt(N) (1/e^2 = 0). K = 3. Absolute (pred = 0).
* R-G  hypercharge-only emergence: a_Y(Lambda) = 0 (lane C's version). K = 1. Absolute.
Applicability: S1: R-C, R-D, R-F, R-G. S2: R-A, R-B, R-D, R-E (R-F/R-G on S2 are numerically identical to S1's and are not counted twice). S3: R-A, R-B, R-D, R-E, R-F, R-G. S4: Track K only, R-A/R-B type Spin(10) boundary.
No rule uses an invented number. R-E uses one recalled literature constant (0.216), declared.

## Track Z -- zero knobs (the headline under A0). 52 trials

Each variant is one (spectrum, rule, scale option, mass prescription) with NO continuous parameter. Masses: P_dec or P_EW (S3 only; for S1, S2 there is no exotic mass). N27 in {1, 3}.
* S1: R-C at X_P, X_R, X_S (3); R-D at X_P, X_S (2); R-F N in {118, 126} (2); R-G N in {118, 126} (2) = 9.
* S2: R-A at X_P, X_R, X_S (3); R-B (1); R-D at X_P, X_S, crossing (3); R-E (1) = 8.
* S3, P_dec: R-D (h = 12) at X_P, X_S(118 + 22 N27), crossing -- the running is the desert, so the value does not depend on N27 except through X_S; count the three variants once for N27 = 3 (3 variants); R-F and R-G with N in {118, 126} + 22 N27, N27 in {1, 3} (4 + 4 = 8); R-A, R-B, R-E under P_dec are IDENTICAL to S2's (not counted again) = 11.
* S3, P_EW (exotics at m_Z, N27 in {1, 3}): R-A at X_P, X_R, X_S (3); R-B (1); R-D at X_P, X_S, crossing (3); R-E (1); R-F N in {118, 126} + 22 N27 (2); R-G (2) = 12 per N27, 24 total.
Total Track Z: 9 + 8 + 11 + 24 = 52.
Output per variant: the scale X, the residual vector with tol and the factor |r|/tol per component, PASS/FAIL, the T-MONO / T-DOMAIN flags, and for absolute rules the implied 1/alpha(0) with tol_em and the bar verdict; plus the C6 inequality checks for unified rules.
Track Z verdict: Z-PASS (T-JOINT passes for all components; alpha(0) within tol_em for absolute rules), Z-FAIL (with the margin factor), Z-DEAD (T-MONO or T-DOMAIN). A relational Z-PASS still leaves alpha(0) an INPUT: it can never be a derivation of alpha.
A Z-PASS is a lead only if the bar's other criteria hold; with the running uncertain to >= 1% and 81 total trials, lane D's bar (miss <= 5e-10 or the route's own predicted precision, and P < 1e-3) cannot be cleared for alpha(0): at best "UNDECIDED at the running's power".

## Track K -- knobs allowed (the original instruction; information only under A0). 29 trials

For S3 (E6), for N27 in {1, 3}: exotic masses M_D in [1 TeV, X], M_H in [100 GeV, X] are UNKNOWNS (each counts as one free parameter); the scale X is an unknown when the rule leaves it free. Thirteen variants per N27 = 26:
KA-free (R-A with X free: a_1 = a_2 = a_3 at some X; the classic cure question), KA-P, KA-R, KA-S (R-A at fixed X_P, X_R, X_S(118 + 22 N27)), KD-free, KD-P, KD-S (R-D with h = 12; X free / X_P / X_S), KE (R-E), KF-118, KF-126 (R-F), KG-118, KG-126 (R-G), KDeg (R-A with X free and M_D = M_H = M, the complete-SU(5)-multiplet case: one mass knob).
For S4, three variants: X free, X = X_S(118), X = X_P (Spin(10) boundary K = diag(a_G, (2/3) a_G) with a_RX = 0), unknowns M_BL, a_R(M_BL), a_RX(M_BL), and X when free.
Total Track K: 26 + 3 = 29. Grand total 52 + 29 = 81 (this is the family size used in lane D's bar: log2 81 = 6.34).
Parameter and excess counting (declared): tests = the three measured numbers (alpha(m_Z) [equivalently alpha(0) via the measured offset], sin^2 theta_W, alpha_s) = 3.
K_eq = number of equalities the rule imposes (including the one that defines a crossing scale and the scale relation of R-E). u = 1 if the scale X is an unknown solved by the equalities, else 0. m = number of exotic-mass / intermediate-scale unknowns (each counted as one).
excess = K_eq - u - m (equivalently 3 - the number of parameters of the forward map; checked on the SM: R-B has K_eq = 2, u = 1, excess 1 = the alpha_3 prediction). excess <= 0: nothing is predicted beyond what was fitted. Verdict rules:
* K-DEAD: no point of the knob box satisfies all residuals within tol (the minimum over the box of max_k |r_k|/tol_k is reported).
* K-REFIT: a solution exists and excess <= 0.
* K-LEAD: a solution exists AND excess > 0 (strictly fewer parameters than independent equalities) AND the inequality checks C6a-C6c pass at the solution. If it occurs, the equation, the scale and the excess predictions are stated. (Under A0 it would remain "knob-dependent", flagged as such.)
Also reported for every K-REFIT with a family of solutions (excess < 0): the range of X and of the solved masses, the proton-lifetime check along the family, and what the solved masses are (a solved mass inside a collider-excluded window is an additional kill; above reach it is an unfalsifiable re-fit).
The E6 cure question is answered by KA-free, KA-P/R/S, KDeg: does splitting the 5 + 5bar-like exotic pair (M_D != M_H) cure the ~10% alpha_3 miss of non-supersymmetric SM-content unification, and what does it cost.

## Scripts (argv declared in each docstring; every one has a MUTATE control; real exit 0 (2 on failure), MUTATE exit 1 if the control bites and 3 if it does not; no bytecode; nothing written outside this directory)

1. `x1_lib.py` -- the general two-loop machinery, the runner with exotic thresholds, the variants, the rules, the scale solvers, the scorer, the inequality checks, the bar interface. Not a script; imports lanes B, N1, U3 (path-relative, read only) and D.
2. `x1_0_gates.py` -- gates: G1 the SM (b, B) rebuilt from the field content equals lane N1's recalled matrices (converted to the Y normalisation); G2 my runner reproduces lane U3's 2L-T (and 1L variants) for the SM at seven scales to 1e-6;
   G3 one E6 exotic set per 27 has (Delta b_Y, Delta b_2, Delta b_3) = (10/9, 2/3, 2/3) from group theory, and the complete-SU(5)-multiplet one-loop invariance: with M_D = M_H the ratios (a_3 - a_2)/(a_2 - a_1) at one loop are unchanged; G4 threshold bookkeeping vs a one-loop closed form; G5 the SU(5) coefficients (b_5 = -85/6 with 3 x (5bar + 10) and one 5 scalar) from the general formula;
   G6 T-ABS translation vs an exact one-loop down-run; G7 the P_dec limit of the exotic run equals the desert run; G8 the U3 numbers quoted above are reproduced (R-B residual +0.131 at 1.09e13 GeV etc.). `python3 x1_0_gates.py`; control `python3 x1_0_gates.py MUTATE` (the lane-A bug b_Y = (3/5) b_1; G1 and G2 must FAIL).
3. `x1_1_zero_knob.py` -- Track Z (52 variants), writes `x1_1_results.json`; controls inside: K1 positive (a synthetic rule equal to the central run passes), K2 negative (+8% fails), K3 the bar interface on a synthetic candidate; control `python3 x1_1_zero_knob.py MUTATE` (the positive control is perturbed by 8%: K1 must FAIL).
4. `x1_2_knob_fits.py` -- Track K (29 variants), writes `x1_2_results.json`; controls inside: K1 the mass solver recovers known masses from a synthetic world built with a forward run, K2 a synthetic world that is NOT unifiable is reported infeasible, K3 the excess arithmetic on the SM (R-B: excess 1); control `python3 x1_2_knob_fits.py MUTATE` (the recovery target is perturbed by 30% in ln M: K1 must FAIL).
5. `x1_3_verdicts.py` -- reads the two result files, applies the verdict rules and the bar, prints the per-pair table (zero-knob prediction and miss, knob-fit existence, parameter count, excess, DEAD / RE-FIT / LEAD, and the A0 reading), writes `x1_3_verdicts.json`; control `python3 x1_3_verdicts.py MUTATE` (one verdict record is corrupted; the consistency check must FAIL).
Run environment: `PYTHONDONTWRITEBYTECODE=1`; no absolute paths and no personal names in any file (outputs are filtered for the working-directory path); no PDFs. First-run outputs are kept as `*_FIRSTRUN.out`. Any first-run failure is DIAGNOSED before anything is changed and every change is an Amendment below.

## Expectations, stated in advance (so they can be false)

E1  (Track Z) Every P_dec pair reproduces U3's SM-desert numbers and fails: relational GUT rules by the -13% a_3 miss (R-B) and larger at Planckian scales; dual-Coxeter and emergence rules by the matter-monotone / magnitude mismatch. No S1/S2 pair passes.
E2  (Track Z, P_EW) Exotic states at m_Z change the run so drastically (three 27s: Delta b = (10/3, 2, 2)) that the crossings move by decades; I expect all 24 P_EW variants to FAIL by a factor > 3 of their tolerance, and R-F/R-G to stay DEAD because b_3 = -7 + 2 < 0 and b_2 = -19/6 + 2 < 0 (asymptotic freedom of SU(3) and SU(2) survives three 27s), so a_2, a_3 cannot reach 0.
E3  (Track K) Complete (degenerate) exotic multiplets cannot cure the alpha_3 miss (one-loop invariance, gate G3). Split masses (M_D != M_H) CAN reach exact a_1 = a_2 = a_3 at a free X (a one-parameter family, excess -1 for N27 = 3): K-REFIT, not a lead. At a fixed X_P, X_R or X_S a discrete solution may exist inside or outside the box; where it exists excess = 0 (RE-FIT).
E4  (Track K) The dual-Coxeter rules with h = 8, 12 (a_G = 100.5, 150.8) are unreachable (added matter lowers a; the run is ~ 40-50 near the boundary): K-DEAD by T-MONO for every mass choice. The heterotic rule KE is at best a RE-FIT (K_eq 3, u 1, m 2, excess 0).
E5  (S4) The gauged B-L intermediate scale cannot change the one-loop running of a_Y, a_2, a_3 at all (sum b_ab = b_Y unchanged), so M_BL drops out of the matching a_1 = a_2 and S4 is K-DEAD with the same residual as S2's R-A/R-B (identity to be verified numerically).
E6  No pair is a LEAD. If any pair looks like one it will be attacked first (bookkeeping of K_eq, u, m; duplicate counting; a hidden knob; T-MONO on the actual run).

## Amendments
A0 above was received before any run.
* A1 (first run of x1_0_gates.py, FIRSTRUN.out): a TypeError, not a physics failure -- the right-hand side received a Python list in the gate's cross-check against lane N1's Runner (mine and N1's both require numpy arrays). Fix: `np.asarray` inside my right-hand side; the gate passes numpy arrays. No physics changed.
  The second run's output is kept as `x1_0_gates_SECONDRUN.out` (it shows the two failures below, G5b and G6b, before their amendments).
* A2 (G5b): the raw non-supersymmetric formula misses the published MSSM two-loop matrix, with B_33 off by exactly +52 (all other differences follow the same pattern). Diagnosis: the SUSY gaugino-matter coupling is a gauge-Yukawa term that the non-SUSY formula does not contain; it equals -T_i (2 C_j + 2 C_A(i) delta_ij) per chiral multiplet
  (for SU(3): sum T (2 C + 2 C_A) = 6 x 26/3 = 52, exactly the miss). With that term ALL NINE entries of the published matrix are reproduced to 4e-15: the gate now checks the general formula on gauge, adjoint, fermion and scalar terms against independent published numbers. The correction is used ONLY in the gate; no SUSY content enters any pair. Disclosed: the form of the SUSY term was inferred from the size of the miss, then confirmed on all nine entries.
* A3 (G6b): the two-loop check of the T-ABS translation was ill-posed as written (the dual-Coxeter shift drives a_3(m_Z) negative, giving a departure of 1e49). Replaced by a 3% shift (departure 6.2e-4). Consequence for the pairs: for absolute rules whose shift is of order 50% the implied alpha(0) is the one-loop translation only (exact at one loop, invalid if it drives an m_Z coupling to a non-positive value); each such case is flagged in the output.
* A4 (first run of x1_1_zero_knob.py, FIRSTRUN.out): all 52 variants and 4 controls ran; the script crashed only when writing the JSON (numpy bool_ not serialisable). Harness fix in `jsonable`; no physics changed. The tally (0 Z-PASS, 38 Z-FAIL, 14 Z-DEAD) is identical in the FIRSTRUN and the repaired run. FIRSTRUN outputs were also scrubbed of the absolute working-directory path (replaced by `<lane>`).
* A5 (first run of x1_2_knob_fits.py, FIRSTRUN.out): the pre-registered question for KA-free was implemented as a scan on an X grid with the two masses solved at each X; it found NO solution at any X and reported K-DEAD. DIAGNOSIS before any change: this is an artefact of the method, not a physics result. At one loop the exotic content acts on (a_1 - a_2, a_3 - a_2) along ONE direction only
  (the D pair and the doublet pair contribute exactly antiparallel vectors, because D + H is a complete SU(5) multiplet; gate G3), so the two equalities fix X and only the difference L_H - L_D of the two threshold logarithms; a solution exists only at an isolated X (the ratio (a_3 - a_2)/(a_1 - a_2) of the SM run must equal 5/2 there, by my reading of the pre-run numbers ~5e13 GeV) with a flat direction in the sum. A grid in X misses the isolated scale.
  Fix: X is treated as an UNKNOWN (3-dimensional least squares over (X, f_D, f_H)), as the pre-registration says ("the scale X is an unknown when the rule leaves it free"). The FIRSTRUN numbers for the fixed-X variants, KDeg, KE, KD, KF, KG and S4 are unaffected by this change and are the same in the repaired run.
  Consequence for the counting: the nominal excess of KA-free is -1 (K_eq 2, u 1, m 2) but the EFFECTIVE number of mass knobs at one loop is 1; the effective excess is 0 with one flat direction. Both are reported.
* A6 (control K2): the pre-registered synthetic infeasible world (mass box 1e14-1e16) was reachable to 0.005, i.e. inside the 1% floor -- the control itself was ill-designed, not the solver. Replaced by a world whose a_Y(m_Z) is moved by +10% (first tried a_3(m_Z) +10%, which moves a_3(X) by only ~2% and again failed to be infeasible; both attempts are disclosed).
* A7 (check K6): my analytic expectation for the S4 least-squares residual used the max-norm minimiser (|Delta|/(4 a_2)); scipy minimises the sum of squares, whose largest component is |Delta|/(3 a_2). Prediction corrected, and the check now allows the declared hybrid two-loop drift of the S4 sum (one-loop above M_BL, two-loop SM below). The FIRSTRUN value 0.1792 is what the corrected formula gives.
* Note on monitors/bookkeeping: a pgrep-based wait was run by mistake and killed; no effect on results.
* A8 (KA-free, N27 = 1): the pre-registered K-DEAD rule is "no point of the knob box within the T-JOINT tolerance", but the first implementation only tested for an exact solution. Added a max-norm minimisation from the best least-squares point and a T-JOINT check there. Result: N27 = 1 closest approach max|r| = 0.0207 against tolerance (0.01, 0.04), i.e. it fails the a_1/a_2 component by a factor 2.1 -> K-DEAD stands, now on the pre-registered criterion. N27 = 3 is unchanged (72 exact solutions). Outputs of the run before A8 are kept as `x1_2_knob_fits_SECONDRUN.out`.
* Outcome versus the Expectations section (recorded for honesty): E1, E2, E4, E5, E6 held. E3 was partly WRONG: I expected a one-parameter family in X; the family is in the masses (72 exact solutions, a curve) but X is pinned to 4.6-5.1e13 GeV (N27 = 3) because the split-multiplet direction is one-dimensional; at fixed X_P, X_R, X_S there is no solution at all (closest approach 0.29-0.48), N27 = 1 misses by a factor 2.1 of the tolerance.
