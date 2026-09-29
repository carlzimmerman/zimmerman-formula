# U3 -- thirteen invented ultraviolet boundary principles, tested jointly against the three running couplings (pre-registration)

Written 2026-09-29 BEFORE any script in this directory was written or run. What I did before writing this file: READ the committed record (ALPHA_CHAIN_STATUS.md, the U1
pre-registration and library, the T1 script, `B_rg_asymptotic_safety/rg_common.py`, `N1_joint_couplings/{N1_PREREGISTRATION.md,n1_lib.py,n1_3_running_scorer.py}`,
`M_red_team/m4_lane_c_content_and_cutoff.py`, `C_holographic_species/C0_PREREGISTRATION.md`, `D_calibration_bar/{alpha_bar_checker.py,bar_lib.py}`). NO number below has been computed
by me; the numbers marked KNOWN come from that record or from unscripted mental arithmetic and are listed so that nothing is presented as blind.

## Why this lane exists and what counts

The record's key finding: alpha enters low-energy physics at O(1) only through the running logarithm, which decouples below m_e (checked to 1e-79 in U1). A working
principle must therefore live in the ULTRAVIOLET: a forced boundary value of the couplings at some scale X, or a forced charged spectrum. The user asked for INVENTED principles.
Inventing a hypothesis is legitimate; fabricating evidence is not; a principle conceived after seeing 1/137 cannot earn credibility by fitting it. It counts only if
(a) it is stated in full BEFORE any comparison (this file), (b) its consequences follow by derivation, (c) it makes at least one prediction it was not built to fit.
Solving a principle for the target is an INVERSE MAP, not a test, and is labelled as such. Nothing here is tuned. Every variant (a convention or an integer choice)
is declared here and ALL are reported. alpha stays an INPUT; kappa = 1/2 stays FITTED; the SM mass and coupling sector stays walled (measured masses and the three
measured couplings at m_Z are INPUTS, never derived). No paper is read for this lane; the heterotic string-scale constant in P13 is RECALLED (labelled at its use).

## Numbers KNOWN before this pre-registration (disclosed)

* From lane N1/M/B (scripted there): SM one loop with measured couplings at m_Z gives 1/alpha_Y(m_P) = 55.48, 1/alpha_2(m_P) = 49.46, 1/alpha_em(m_P) = 104.94; the two-loop
  shift of 1/alpha_em(m_P) is 0.67%; the SM one-loop alpha_1 = alpha_2 crossing is at ~1e13 GeV with alpha_3 off by -13% (N1 map D); one unit-hypercharge Dirac fermion at 1 TeV moves
  1/alpha_Y(m_P) by -12.7%. N1 stated: 1/alpha_3(m_P) ~ 52 by unscripted mental arithmetic, so the three SM couplings in the Y normalisation (Q = T3 + Y) are within ~12% of each other near m_P.
  Any principle that predicts "the three are about equal near M_P in the Y normalisation" is therefore POST-HOC INFORMED (marked PHI below) and cannot claim a prediction.
* Unscripted mental arithmetic of mine, made while designing the list (stated as expectations, to be checked): the Y-normalised crossings 1/alpha_Y = 1/alpha_2 near 4e37 GeV
  (far above M_P), 1/alpha_2 = 1/alpha_3 near 1e17 GeV, and the GUT-normalised alpha_1 = alpha_2 crossing near 1e13 GeV.

## Conventions and inputs (declared)

* a_i := 1/alpha_i for i = Y, 2, 3, with alpha_Y in the normalisation Q = T3 + Y, so 1/alpha_em = a_Y + a_2 (exact tree-level relation at m_Z) and the GUT-normalised
  a_1 = (3/5) a_Y  (alpha_1 = (5/3) alpha_Y; the KNOWN PITFALL: b_Y = (5/3) b_1 = 41/6). d a_i / d ln mu = -b_i/(2 pi) - two-loop terms. One-loop (b_Y, b_2, b_3) = (41/6, -19/6, -7); b_1 = 41/10.
* Inputs at m_Z = 91.1876 GeV (lane B / N1 set A): 1/alpha_em(m_Z) = 127.930, sin^2 theta_W = 0.23122, alpha_s = 0.1180 (set B, lane G: 127.955, 0.23122, 0.1179). a_Y = 127.930 (1 - s2), a_2 = 127.930 s2, a_3 = 1/alpha_s.
  1/alpha_em(0) = 137.035999177 (Thomson, INPUT); the hadronic-inclusive offset a(0) - a(m_Z) = 9.106 is the measured input of lane B.
* Scales (GeV): X_P = M_P = 1.220890e19 (un-reduced); X_R = M_red = 2.435e18; X_S = X_R/sqrt(118) = 2.2416e17 (species scale with the SM count N = 118 of lane C/N2); H_Lambda ~ 1.5e-33 eV (see the H_Lambda note below).
* Running (the "central" run and its variants; my own implementation, cross-checked against lane B's rg_common and N1's Runner in the gates): central C = two-loop with the top decoupled between m_Z and
  m_t = 172.57 GeV (its Delta b = (17/18, 1/2, 2/3) removed in that window, Higgs and W/Z present throughout), y_t(m_t) = 0.9334, two-loop gauge matrix and top-Yukawa coefficients as in N1 (RECALLED,
  validated there by reproducing a 0.4-1.0% two-loop shift). Variants V: 2L-T (central), 2L-A (no top threshold, N1's 2L-A), 2L-B (set B inputs), 2L-TB (threshold, set B), 1L-T, 1L-A, 1L-B (one loop).
  Three-loop terms are NOT computed; they are covered by the 1% floor in the tolerance below (declared; a gate checks that input errors are below it).
* Unknown new charged states are NOT bounded by the record. They are handled by the declared bridge test (T-BRIDGE) and by the matter-monotone rule (T-MONO) below, never by an
  after-the-fact spectrum.

## The H_Lambda note (declared)

For mu < m_e no charged state lies below mu, so 1/alpha_em(mu) is constant there (no running), SU(3) confines and the massive SU(2) has no running coupling below m_W. A boundary rule
"at H_Lambda the couplings take value Y" is therefore (i) exactly equivalent to a rule at m_e for alpha_em, and (ii) untestable jointly (alpha_2, alpha_3 are non-perturbative in the IR).
No principle is registered at H_Lambda; the gate G7 demonstrates the decoupling (the sum over states with m < mu is empty). This is the reason the list lives at UV scales.

## The test battery (declared, identical for every variant)

Each variant maps the run couplings A(mu) = (a_Y, a_2, a_3)(mu) to K >= 1 dimensionless residuals r_k ("miss"), zero when the principle is satisfied:
* ratio constraint: r = target / (actual ratio) - 1;   absolute constraint: r = (predicted a_j - actual a_j) / actual a_j;   zero-target rules (sum rule, RG invariant): r = F / S with S = sum of absolute terms.
* T-JOINT (J1). Evaluate r_k under the central run C and every variant v in V (and, for the parametric species scale X_S, additionally at X_S/2 and 2 X_S: the C2d convention "Lambda_sp known up to a factor 2").
  band_k = max_v |r_k(v) - r_k(C)|. tol_k = max(2 band_k, 0.01, 0) (the 1% floor is a declared convention). PASS iff |r_k(C)| <= tol_k for ALL k. The scale X is the principle's own (fixed number or solved from the
  principle's own crossing/self-consistency condition under each running variant), so the scale error is inside band_k.
* T-DOMAIN. The programme's cutoff is M_P. If a solved scale X > 1.001 X_P the variant is DEAD by domain (it asserts physics beyond the cutoff); the prediction there is still reported. If a required crossing does not exist below 1e45 GeV the variant is DEAD (no such scale).
* T-MONO (matter monotonicity). Adding charged matter (fermions or scalars) can only DECREASE a_i(X) (Delta b_i >= 0 in the convention d a_i/dt = -b_i/2 pi). An absolute rule that predicts a_j ABOVE the SM-desert run beyond tol_j
  cannot be repaired by any added matter: DEAD, content-independent. (Extra gauge bosons, non-perturbative effects and gravity corrections are outside this rule; stated.)
* T-BRIDGE (threshold error, declared). If a variant FAILS T-JOINT and is not killed by T-MONO/T-DOMAIN, compute the minimal number of unforced extra multiplets at 1 TeV (m = 1 TeV is the position of largest leverage; heavier states need more) that makes ALL residuals vanish:
  N_Y unit-hypercharge Dirac singlets (Delta b_Y = 4/3 each), N_2 vector-like SU(2) doublets with Y = 0 (Delta b_2 = 2/3 each), N_3 vector-like colour triplets with Y = 0 (Delta b_3 = 2/3 each); shifts a_i(X) -> a_i(X) - N_i (Delta b_i / 2 pi) ln(X / 1 TeV), and the b_i that enter the rule (P06, P07, P08) change by N_i Delta b_i.
  N_i >= 0 real numbers, minimise sum N_i (SLSQP with multiple starts, residual < 1e-6). Where a rule leaves an overall coupling free the solver may use it. Report (N_Y, N_2, N_3). Infeasible: DEAD. max N_i <= 1: the running uncertainty from ONE unforced multiplet exceeds the test power: UNDECIDED, "rescue requires unforced content" reported with the numbers.
  max N_i > 1: DEAD (needs more unforced content than the declared allowance; the spectrum is not forced by the principle).
* J2 look-elsewhere (N1's, declared): lambda = N_trials prod_k min(1, 2 tol_k / ln 100) (log-uniform prior over a factor 100 for every residual), P = 1 - exp(-lambda), N_trials = the total number of variants registered below (34; the family for the bar's log2 size is log2 34 = 5.09). Need P < 1e-3.
* J3 forcedness: zero free reals in the rule; the solved scale (P02, P04, P13) is solved by the principle's own condition, not fitted.
* T-ABS (does it fix alpha). A variant fixes alpha only if it specifies BOTH a_Y and a_2 as absolute numbers (P01, P09, P10, P11). Implied Thomson value 1/alpha_pred(0) = 137.035999177 + (pred_Y - A_Y) + (pred_2 - A_2) at the scale X (exact translation at one loop for SM-desert running, approximate at two loops; the boundary rule changes the measured couplings at m_Z by the same shifts).
  Lane D's bar (`alpha_bar_checker.assess`, log2size = log2 34, n_targets = 1, fitted_reals = 0, scale stated, predicted_precision = the variant's own tol_em = max(2 x spread of the implied value over V, 0.01), delta = |1/alpha_pred(0)/137.035999177 - 1|) is reported for every T-ABS variant. Relational variants
  leave the overall coupling free (one fitted real in effect) and are marked "does not fix alpha; bar N/A".
* T-IND. SURVIVES is reserved for a variant that (i) passes T-JOINT for all K constraints, (ii) has K >= 3 absolute constraints that include both a_Y and a_2 (so it predicts alpha AND the other two couplings from zero parameters), (iii) passes J2 (P < 1e-3), (iv) clears lane D's bar. Relational variants can at best reach UNDECIDED.

## Verdict rules (declared)

* Per variant: DEAD = FAIL of T-JOINT not rescued under T-BRIDGE (or T-MONO / T-DOMAIN kills); UNDECIDED = PASS of T-JOINT at the running's power (bar not cleared, or rule relational), or FAIL rescued by <= 1 unforced multiplet of each type; SURVIVES only as T-IND.
* Per principle: the headline is the LEAST severe verdict among its non-inapplicable variants (DEAD only if every variant is DEAD). All variants are listed. PHI variants are flagged and are never scored as predictions.
* Expected outcome, stated in advance: NO principle SURVIVES. The absolute rules (P01, P09, P10, P11) are DEAD. The GUT-normalised equalities are DEAD (alpha_3 off -13% at the alpha_1 = alpha_2 crossing; a_1 = (3/5) a_Y ~ 33 against a_2 ~ 49 near M_P). The one variant I expect to be UNDECIDED rather than DEAD is P03 in the Y
  normalisation at X_P (PHI), because a single unit-Y Dirac fermion moves a_Y by ~13%. P04 (Y,2) is DEAD by domain.

## The principles (each stated in full; equation, scale, what it forces; the variant list is the whole trial count)

Notation for the group numbers used below: h(SU(3)) = 3, h(SU(2)) = 2 (dual Coxeter numbers), h(SU(5)) = 5, h(SO(10)) = 8, h(E6) = 12; Dynkin-index sums over the three SM generations of Weyl fermions:
I_3 = 6, I_2 = 6, I_Y = sum Y^2 = 10 (computed in gate G8 from the SM content with Fractions).

**P01 Dual-Coxeter coupling.** At X the inverse couplings are 4 pi times the dual Coxeter number of the group (1/g_i^2 = h_i): a_3 = 4 pi * 3, a_2 = 4 pi * 2, a_1(GUT norm) = 4 pi * 5 (the dual Coxeter number of the SU(5) parent of the hypercharge embedding), i.e. a_Y = (5/3) * 20 pi.
Forces: all three couplings absolutely. Variants: X in {X_P, X_S}. 2 variants. Constraints: 3 absolute. Fixes alpha.

**P02 GUT-group Coxeter coupling at the crossing.** X is the scale where a_1 (GUT) = a_2 (solved from the run, no other scale). At X: a_3 = a_2 (one ratio) and the common value is 4 pi h with h the dual Coxeter number of the unifying group (a_2 = 4 pi h).
Forces: alpha_3 at X (ratio) and the unified coupling (absolute a_2). Variants: h in {5 (SU(5)), 8 (SO(10)), 12 (E6)}. 3 variants. Constraints: 2. Does not fix a_Y absolutely (a_Y follows from a_1 = a_2), so it fixes alpha only jointly with the crossing: reported as relational plus one absolute a_2; marked "does not fix alpha; bar N/A" (a_Y is not forced independently of the crossing).

**P03 Equal couplings at a Planckian scale.** At X the three couplings are equal: a_1 = a_2 = a_3 (GUT normalisation, level k_Y = 5/3) or a_Y = a_2 = a_3 (Y normalisation, k_Y = 1). The common value is left unspecified (the rule does not fix alpha).
Forces: two ratios. Variants: normalisation in {GUT, Y} x X in {X_P, X_R, X_S}. 6 variants. Constraints: 2 ratios. PHI: the Y-normalisation variants near X_P/X_R (near-equality known).

**P04 Y-normalised universality at a pair crossing.** X is the scale where the two couplings named in the pair are equal (Y normalisation, k_Y = 1); the third coupling must equal them there.
Forces: one ratio. Variants: pair in {(Y,2), (2,3), (Y,3)}. 3 variants. Constraints: 1 ratio (+ T-DOMAIN). Does not fix alpha.

**P05 Fixed hypercharge-to-weak ratio.** At X, alpha_Y = alpha_2 / n, i.e. a_Y/a_2 = n, equivalently sin^2 theta_W = 1/(n+1) (n = 2: the doublet dimension, sin^2 = 1/3; n = 3: the number of generations, sin^2 = 1/4), together with alpha_3 = alpha_2.
Forces: two ratios. Variants: n in {2, 3} x X in {X_P, X_S}. 4 variants. Constraints: 2 ratios. Does not fix alpha.

**P06 Equal magnitude of the logarithmic derivatives.** At X the three couplings run at the same rate in magnitude: |d ln alpha_i / d ln mu| = |b_i| alpha_i / (2 pi) equal for i = Y, 2, 3, i.e. (|b_i| / a_i) equal (SM-desert b_i; independent of the Y/GUT normalisation of the abelian factor).
Forces: two ratios (signs of b_i differ; only magnitudes are equated). Variants: X in {X_P, X_S}. 2 variants. Constraints: 2 ratios. Does not fix alpha.

**P07 Vanishing beta-weighted sum.** At X the beta-function-weighted sum of the inverse couplings vanishes: F = sum_i b_i a_i = 0 ("the one-loop vacuum polarisation weighted by the couplings cancels"), residual F / sum |b_i a_i|.
Forces: one relation. Variants: normalisation in {Y (b = 41/6, -19/6, -7; a_Y), GUT (b = 41/10, ...; a_1)} x X in {X_P, X_S}. 4 variants. Constraints: 1 (normalised). Does not fix alpha.

**P08 One-loop RG invariant vanishes (scale-free).** The RG invariant I = (b_2 - b_3) a_1 + (b_3 - b_1) a_2 + (b_1 - b_2) a_3 (GUT norm; constant along one-loop running for ANY content) is zero: a common crossing exists. Residual I / sum |terms|.
There is NO scale X; evaluated on the measured couplings at m_Z with SM b (band: the two input sets, and the 2L drift of I(mu) at mu in {1e5, 1e10, 1e15, X_P}). Content-robust for complete SU(5) multiplets (they shift all a_i equally at one loop); the T-BRIDGE multiplets are NOT complete, so they are allowed to move it.
Forces: one relation (the unification condition itself). 1 variant. Does not fix alpha.

**P09 Emergence of all three couplings from the species tower.** At the species scale Lambda = M_red / sqrt(N) every coupling is emergent: 1/alpha_Y = 1/alpha_2 = 1/alpha_3 = 0 (lane C's emergence for hypercharge, made joint: the non-abelian b_2, b_3 < 0 make 1/alpha_2, 1/alpha_3 GROW upward, so they cannot vanish; tested, not assumed).
Forces: all three absolutely (= 0). Variants: N in {118 (SM), 126 (SM + 3 RH neutrinos + graviton)}. 2 variants. Constraints: 3 absolute (=0). Fixes alpha (1/alpha_em(Lambda) = 0). The species scale carries the factor-2 ambiguity.

**P10 Abelian emergence with confined-strength non-abelian couplings.** At X: a_Y = 0 (hypercharge emergent) while the non-abelian couplings sit at their Coxeter values a_2 = 4 pi * 2, a_3 = 4 pi * 3.
Forces: three absolute. Variants: X in {X_S, X_R}. 2 variants. Constraints: 3 absolute. Fixes alpha (1/alpha_em = 8 pi at X).

**P11 Anomaly-index coupling.** The inverse coupling equals a constant times the Dynkin index of the chiral matter that carries the charge, summed over three generations: a_i = c I_i (I_3 = 6, I_2 = 6, I_Y = 10 for the Weyl fermions of the SM; the Higgs is not chiral matter). c in {2 pi, 4 pi}.
Forces: three absolute. Variants: c in {2 pi, 4 pi} at X = X_P. 2 variants. Constraints: 3 absolute. Fixes alpha.

**P12 't Hooft-coupling universality.** The 't Hooft coupling lambda_i = g_i^2 h_i is the same for the three factors, with h_1 = 5 (the SU(5) parent for the GUT-normalised abelian factor), h_2 = 2, h_3 = 3. Equivalent to a_1 : a_2 : a_3 = 5 : 2 : 3.
Forces: two ratios (a_1/a_2 = 5/2, a_3/a_2 = 3/2). Variants: X in {X_P, X_S}. 2 variants. Constraints: 2 ratios. Does not fix alpha.

**P13 Heterotic string-scale locking (literature-derived, RECALLED constants).** The three couplings are equal in the GUT normalisation (levels k_Y = 5/3, k_2 = k_3 = 1) at the string scale M_str = 0.216 g_str M_red = 5.26e17 g_str GeV with g_str^2 = 4 pi / a_2(M_str) (the recalled tree-level relation; no threshold corrections; the coefficient 0.216 is recalled and is NOT re-derived here). X is solved self-consistently from a_2 under each running variant.
Forces: two ratios (a_1 = a_2, a_3 = a_2) and the scale. 1 variant. Constraints: 2 ratios. Does not fix alpha. Threshold corrections of the heterotic string are unforced: they enter only through T-BRIDGE.

Total: 2 (P01) + 3 (P02) + 6 (P03) + 3 (P04) + 4 (P05) + 2 (P06) + 4 (P07) + 1 (P08) + 2 (P09) + 2 (P10) + 2 (P11) + 2 (P12) + 1 (P13) = 34 variants of 13 principles. Nothing else is tried. A variant added later goes into an Amendment below and is counted.

## Scripts (argv declared in each docstring; every one has a MUTATE control that must FAIL with exit 1; exit 3 if the control is broken)

1. `u3_lib.py` -- the runner (all variants), crossing/self-consistency solvers, the 13 principles, the residual functions, T-BRIDGE, J2. Not a script; imported. Imports lane B's `rg_common` and N1's `n1_lib` READ-ONLY (path-relative).
2. `u3_0_gates.py` -- gates: G1 b's from SM content (Fractions); G2 lane-B 104.94 and 55.48/49.46; G3 two-loop shift 0.4-1.0%; G4 my runner reproduces N1's Runner 1L-A/2L-A and rg_common at M_P; G5 input-error floor (alpha_s +-0.0009, 1/alpha_em +-0.008, sin^2 +-0.00005 move every a_i(X_P) by less than 1%);
   G6 the multiplet coefficients (Fractions) and the -12.7% N1 cross-check; G7 the H_Lambda decoupling; G8 group numbers (h, Dynkin sums) from the SM content; G9 crossing-solver checks (1L closed form vs numeric). `python3 u3_0_gates.py`; control `python3 u3_0_gates.py --mutate` (the lane-A bug b_Y = (3/5) b_1; exactly G1 and G2 must FAIL).
3. `u3_1_score.py` -- scores the 34 variants (T-JOINT, T-DOMAIN, T-MONO, T-BRIDGE, J2), writes `u3_1_results.json`. `python3 u3_1_score.py`; control `python3 u3_1_score.py --mutate` (the positive-control synthetic variant, which equals the central run and must PASS, is perturbed by 8%: exactly check K1 must FAIL).
   Controls inside the script: K1 positive (synthetic rule = the central run's own values, family 1: PASS), K2 negative (same +8%: FAIL), K3 bridge solver (recovers a known N), K4 J2 formula check, K5 crossing solver on a synthetic trajectory.
4. `u3_2_verdicts.py` -- reads the results, applies lane D's bar to the T-ABS variants, prints the verdict table. `python3 u3_2_verdicts.py`; control `python3 u3_2_verdicts.py --mutate` (one verdict record is corrupted; the consistency check must FAIL).

Run environment: `PYTHONDONTWRITEBYTECODE=1`; no absolute paths and no personal names in any file; no PDFs; nothing is written outside this directory. First-run outputs are kept as `*_FIRSTRUN.out`.

## Scope and reading rules

* "DEAD" means: contradicts the measured running in the stated SM-desert (plus declared threshold allowance) under the stated scope. It does not mean the idea is uninteresting. "UNDECIDED" means the running's uncertainty (two-loop, thresholds, unknown content) exceeds the test's power by the stated amount.
* Near-equal couplings at M_P in the Y normalisation are a KNOWN feature; a pass there is not a prediction.
* The record's key finding is used as given: any principle that does not live in the UV running or a forced charged spectrum is out of scope, and the walled SM masses are inputs.

## Amendments
(none yet)

### Amendment 1 (2026-09-29, written BEFORE the first run of any script; no result seen)

P08 has no scale, but the T-BRIDGE multiplets sit at 1 TeV, so the invariant must be evaluated above them. Declared: the CENTRAL evaluation point of P08 is mu = 1 TeV (the two-loop central run from the measured m_Z values, with the SM b for N = 0); the band additionally includes
the evaluations at mu in {m_Z, 1e5, 1e10, 1e15, X_P} (the two-loop drift of the "constant"), plus the six other running variants, exactly as for every other variant. This replaces the sentence "evaluated on the measured couplings at m_Z" in P08; at one loop the two are identical.
For the parametric species scale (param_scale variants) the extra evaluations at X/2 and 2X use the residual normalised by the coupling at the shifted scale itself.

### Amendment 2 (2026-09-29, after the first run of `u3_0_gates.py`; disclosed, no principle criterion changed)

First run kept as `u3_0_gates_FIRSTRUN.out`: gate G6b FAILED (14.17% against the expected 12.7%). Diagnosis, before any change: N1's "-12.7%" is quoted at N1's own map-A scale mu_c = M_P sqrt(alpha_2(mu_c)/3) (about 7e17 GeV), not at M_P; the KNOWN-numbers paragraph above mis-transcribed it as
"1/alpha_Y(m_P)". At M_P the same coefficient gives -14.2% (one loop). The gate was corrected to evaluate at N1's mu_c; the physics and every principle criterion are unchanged. Also disclosed: my unscripted expectation "Y-normalised crossing a_Y = a_2 near 4e37 GeV" was an arithmetic slip; the gate G9 prints
the scripted values (a_Y = a_2 at 5.3e20, a_Y = a_3 at 4.9e19, a_2 = a_3 at 9.6e16, GUT-norm a_1 = a_2 at 1.03e13 GeV, all one loop set A). P04 (Y,2) and (Y,3) are still above M_P (by factors 43 and 4), so T-DOMAIN applies exactly as pre-registered; the expectation "P04 (Y,2) DEAD by domain" stands.

(Amendment 2, continued: the first mutate run exited 3 because the control compared full check labels instead of check IDs -- the same slip T1's Amendment 2 records; fixed to compare IDs. No criterion changed.)

## Results (appended after the runs; no criterion was changed after any result was seen)

Scripts and outputs: `u3_0_gates.{py,out,_FIRSTRUN.out,_MUTATE.out}`, `u3_1_score.{py,out,_FIRSTRUN.out,_MUTATE.out}` + `u3_1_results.json`, `u3_2_verdicts.{py,out,_FIRSTRUN.out,_MUTATE.out}` + `u3_2_verdicts.json`, `u3_lib.py`.
Real runs exit 0; the three MUTATE controls exit 1 (exactly G1+G2, exactly K1, exactly C1 failed). The FIRSTRUN of `u3_0` failed G6b (Amendment 2, a wrong attribution of N1's -12.7% to M_P, fixed in the gate, not in any principle); the FIRSTRUN of `u3_1` and `u3_2` equal the final outputs.

* 34 variants of 13 principles: 33 DEAD, 1 UNDECIDED, 0 SURVIVES. By principle headline (least severe variant): 12 DEAD, 1 UNDECIDED (P03), 0 SURVIVES.
* Tolerances actually obtained: the 1% floor for most absolute constraints at X_P; 2-13% for the species-scale (factor-2) variants; the running band (max over the seven run variants) of a fixed-X_P constraint is at most about 1.5% (a_Y in V01: 1.35%; inputs alone: 0.12%, gate G5); solved-scale variants (crossings) reach 2.8%.
* Kills by T-MONO (content-independent, no added matter can help): V01, V02 (P01: predicted a_Y = 104.7 against 55 at X_P), V03-V05 (P02: 4 pi h above the crossing value of a_2), V30, V31 (P11). By T-DOMAIN: V12 (a_Y = a_2 crossing at 5.2e20 GeV, 42 x M_P) and V14 (a_Y = a_3 at 3.3e19, 2.7 x M_P).
  All others by T-BRIDGE (more than one unforced multiplet at 1 TeV of some type would be needed to make the rule hold exactly). P09/P10 cross-check: the extra unit-Y Dirac fermions needed for hypercharge emergence at the species scale come out 8.5 (this runner, two loops, X_S) against lane C's 8.6 (one loop).
* The one non-DEAD variant, V09 (P03, Y normalisation, X_P; PHI, post-hoc informed), fails T-JOINT (a_Y/a_2 = 1.12 against 1; a_3/a_2 = 1.08) but is rescued by 0.76 unit-Y Dirac fermions and 0.96 colour triplets at 1 TeV, so it is UNDECIDED at the running's power: the same rule at X_R (V10) already needs 1.14 and at X_S (V11) 1.76. It is not a prediction (near-equality was KNOWN) and it does not fix alpha.
* V25 (P08, the scale-free RG invariant) fails by the pre-registered letter but MARGINALLY (|I/S| = 0.061 against tol 0.058, 1.05 x tol): the normalisation I/S dilutes the miss and the two-loop drift of "the constant" sets the band. The same unification condition, tested as a ratio (V03-V05, a_3/a_2 at the a_1 = a_2 crossing, +13.1% against tol 4.2%, 3.1 x tol), and N1's map D (alpha_3 off -11.6% at two loops) kill it decisively in the SM desert. The T-BRIDGE rule (exact vanishing) gives N_2 = 1.28 for V25; had the rule been "within tolerance" it would have needed ~0.07. The rule was pre-registered and is not changed; this is reported for the reader.
* Lane D's bar on the eight T-ABS variants (V01, V02, V26-V31): none clears; implied 1/alpha(0) = 162.5, 160.2, 30.3, 30.3, 55.4, 56.9, 133.2, 233.7. V30 (a_i = 2 pi I_i at X_P) comes closest at 133.2 (2.8%) yet is killed by T-MONO (a_Y = 62.8 against 55.2). C3: with 34 trials the bar's P < 1e-3 needs a total error below 5.9e-4, while the running itself is uncertain to at least 0.5-1%; the joint test on three couplings has power at the 1% level, the bar on one number does not. So a UV boundary rule can be REFUTED at present precision but cannot be CONFIRMED by the bar: a SURVIVES verdict is unreachable until the running is controlled ~20x better (three-loop, forced spectrum).
* Honest limits: the SM desert is assumed between 1 TeV and X (unforced new matter is handled by T-BRIDGE, at m = 1 TeV, one multiplet type per coupling, not exhaustively); extra gauge bosons and gravitational corrections are outside T-MONO; two-loop coefficients are recalled (validated by G3, the 0.67% shift); no three-loop; the heterotic 0.216 g M_red constant of P13 is recalled and no threshold correction is included (T-BRIDGE stands in for them); the H_Lambda scale carries no principle because nothing runs there (G7); "closest" in the summary picks by the worst |miss|/tol and can be a T-DOMAIN variant.
