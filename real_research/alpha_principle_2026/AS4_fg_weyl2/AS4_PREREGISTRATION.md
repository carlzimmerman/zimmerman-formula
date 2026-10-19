# Lane AS4 -- hypercharge f_g in the quadratic-gravity (EH + C^2 + R^2) truncation of Benedetti-Machado-Saueressig (pre-registration)

Written 2026-10-19, BEFORE any AS4 script existed and before any AS4 computation was run.  Amend only by appending an "Amendment" section at
the bottom; nothing above it may be edited.

## Why this lane exists

AS3 (`../AS3_fg_cpr_reanchored/`, run commit 0c3ccc779) showed something about f_g in the CPR f(R) gauge (rho = 0, beta -> infinity).
Only the transverse-traceless (TT) graviton modes couple to the photon there: the remaining scalar is the conformal mode, and the Maxwell term
is conformally invariant.  An R^2 term therefore cannot change f_g.  A Weyl^2 (C^2) term changes the spin-2 propagator itself.

AS4 computes f_g ONCE in ONE published nonperturbative truncation that contains C^2: Einstein-Hilbert + C^2 + R^2 (plus the topological Euler
term), with SM matter.  The downstream is that of lane B trial C5 and AS1-AS3.

What this lane is NOT:

* kappa and Z enter nowhere.  This is standard quantum-gravity physics, so any outcome is NOT a framework result.
* Even the best outcome is NOT a derivation of alpha: alpha_2(M_Z), the hadronic offset 9.106 and the charged masses are MEASURED, and
  convergence is untested.

## Source chosen, and why (decided before any computation)

* **First choice:** Benedetti-Machado-Saueressig (BMS), arXiv:0901.2984 (the letter, read in full).
  * It prints the truncation (eq. `eq:ansatz`), the gauge, the background class, the cutoff rule and the four trace terms S_2T, S_hh, S_1T,
    S_0.
  * It also prints the pure-gravity fixed point g0* = 0.00442, g1* = -0.0101, g2* = 0.00754, g3* = -0.0050 and the stability coefficients
    2.51, 1.69, 8.40, -2.11.
  * It does NOT print the beta functions or the heat-kernel coefficients of the Lichnerowicz Laplacians on Einstein spaces, so it alone
    does not suffice to reproduce the result.
* **Anchor actually used:** the companion paper by the same authors on the same computation, BMS arXiv:0902.4630 ("Taming perturbative
  divergences in asymptotically safe gravity").  It prints everything:
  * the Hessians on Einstein spaces: App. A, Table `T.1`, eqs. `varEH`, `varR2`, `varRmn2`, `Sgf`, `Saux`;
  * the heat-kernel coefficients: App. B, eqs. `Hexp`, `h1T`, `h2T`, `d4heat`;
  * the trace technology and threshold functions for the optimized cutoff: App. C, eqs. `heat:master`, `defPhi`, `defUps`, `Phigen`,
    `Qgen`, `defPhiOpt`, `upsopt`;
  * the expanded traces: eqs. `mattercont`, `eq:TRuni`, the EH `S_hh` and `S_2T` expansions, `eq:TRh` / `Ccoeff`, `eq:TR2T` / `tCcoeff`;
  * the beta functions: eqs. `betaEH` / `etaEH` / `BEH` and `beta`;
  * the fixed-point tables: `t.FPEH`, `t.FPEHs`, `t.FP`, `t.Stab`.

  Its pure-gravity R^2 + C^2 row (g* = 1.960, lambda* = 0.218, u2 = 0.008, u3 = -0.0050, g* lambda* = 0.427; theta = 2.51, 1.69, 8.40,
  -2.11) is the letter's fixed point.

## Scale statement and downstream (identical to AS1-AS3, by import)

alpha^-1(0) = 137.035999177.  g_Y* = 4 pi sqrt(6 f_g*/41) at M_Planck, run with SM one-loop running down to M_Z.  Add the MEASURED
alpha_2^-1(M_Z), then the MEASURED offset 9.106.  This is `as1_common.downstream_P` (lane B's b3 objects by import).

## The frozen gravitational scheme (BMS 0902.4630, every choice cited)

* **Truncation** (sec. 5, eq. `HDflow`; letter eq. `eq:ansatz`):
  Gamma_k^grav = int sqrt(g) [ u0 + u1 R + (u2 - (2/3) u3) R^2 + 2 u3 R_mn R^mn + (u3 + theta/sigma) E ].
  * Here u0 = Lambda/(8 pi G), u1 = -1/(16 pi G), u2 = -omega/(3 sigma) + theta/(6 sigma), u3 = 1/(2 sigma) + theta/sigma (eq. `couplings`).
  * Dimensionless g0 = u0 k^-4, g1 = u1 k^-2, g2 = u2, g3 = u3 (eq. `dimless`).
  * Translation: lambda = -g0/(2 g1), g = -1/(16 pi g1).
  * Only u2 and u3 are distinguishable on Einstein spaces (BMS sec. 5).
* **Background:** a generic compact Einstein space without Killing or conformal Killing vectors, so there are no excluded modes (sec. 3,
  App. B).
  * Projection is onto int sqrt(g){1, R, R^2, R_mnrs R^mnrs}, with LHS d_t[u0 + u1 R + (u2 - u3/6) R^2 + u3 Riem^2] (letter eq. `E-ansatz`).
  * Ric^2 = R^2/4 and E = Riem^2 on Einstein spaces.
* **Gauge:** eq. `S:gf2` with rho = 0, alpha = 0, beta -> infinity for the higher-derivative truncation (eq. `gfHD`), and rho = 0,
  alpha -> infinity, beta = 0 for the EH truncation (eq. `gfEH`).
  * Third ghost, fourth ghost and the auxiliary Jacobian fields are those of eqs. `Sgf`, `Saux` and Table `T.1`.
  * There is mode-by-mode cancellation of unphysical modes (App. A), and the h-sigma cross term vanishes in the limit.
  * The universal traces S_1T = -(1/2) Tr_1T[d_t R/P_1] and S_0 = -(3/2) Tr_0[d_t R/(3 P_0 - R)] (eq. `Tr:ghost`) must follow from
    Table T.1 with the field statistics stated there.  This is checked in G-PUB.
* **Operators and cutoff:** BMS's Lichnerowicz forms (eq. `def:LL`), with potentials Q0 = 0, Q1 = R/4, Q2 = 2 Riem in BMS's convention
  P = R/6 + Q (eq. `Hexp`; i.e. Delta_1L = -D^2 - R/4 on transverse vectors).
  * The cutoff replaces Delta_sL -> P_k(Delta_sL) for every s (BMS label this "type II").
  * Optimized profile R_k(z) = (k^2 - z) theta(k^2 - z) (sec. 3).
  * P^2 - Delta^2 is regulated as P_k^2 - Delta_sL^2 (eq. `Tr:grav`).
* **Eta terms, as BMS use them:** the full scale derivatives of the couplings in the numerators of eq. `Tr:grav`: d_t u3, d_t u1 and
  d_t u_flat with u_flat = 2 u2 - u3/3.  For EH (eq. `NU-EH`) only d_t u1 appears.  They are solved together with the beta functions
  (sec. 5, below eq. `beta`).
* **Heat kernel:** eq. `heat:master`, with Q_n for the optimized cutoff, expanded to O(R^2, Riem^2); terms of order six and higher are
  dropped (App. C2).

## Exception (a): matter (type I, as frozen in AS1 and used in AS2/AS3)

* **Rule:** the bare Laplacian -D^2 of each matter field is replaced by P_k; curvature endomorphisms stay in the denominators.
  * Real scalars: (1/2) Tr_0[d_t R/P].  For scalars this coincides with BMS's own matter trace (eq. `mattr`), which G-PUB checks.
  * Dirac fermions: -(1/2) Tr_spinor[d_t R/(P + R/4)].
  * Gauge vectors in Feynman gauge: (1/2) Tr_V[d_t R/(P + R/4)] - Tr_0[d_t R/P], with Ric = R/4 on Einstein spaces.
* **Heat-kernel coefficients** of the bare Laplacians on generic Einstein spaces come from Vassilevich hep-th/0306138 sec. 4.1 (eqs.
  `a0nobou`, `a2nobou`, `a4nobou`), with the bundle curvature Omega, including the Riem^2 term.
* **No matter eta terms.**
* **SM content:** N_S = 4, N_D = 45/2, N_V = 12 (gauge vectors treated as abelian at this order).

## Exception (b): f_g on a flat background, in the same gauge and with the same eta convention

* **Definition:** f_g is the graviton contribution in beta_{g_Y} = g_Y(-f_g + (41/6) g_Y^2/(16 pi^2)).  It is the F-bar^2 coefficient of the
  graviton-photon trace on a flat background with constant field strength, by the AS1-AS3 method (vertices from sqrt(g) g g F F).
* **Graviton quadratic action on flat space:** u0 (sqrt g)^(2) + u1 (sqrt g R)^(2) + (u2 - (2/3) u3) (R^(1))^2 + 2 u3 (R^(1)_mn)^2.  The
  Euler term is a total derivative.  So the C^2 term's p^4 piece enters the spin-2 (TT) propagator: on flat space the TT kernel is
  (1/4)(2 u3 q^4 - u1 q^2 - u0).
* **Gauge:** BMS's rho = 0 and the hard limit; on flat space both `gfHD` and `gfEH` impose chi = 0.  The |beta| -> infinity limit is
  evaluated EXACTLY by restricting the trace to the kernel of the gauge fixing.  For rho = 0 that kernel is the TT modes plus the conformal
  mode plus the photon.  This is the AS3-verified identity:
  * the gauge-fixing matrix is a(s) times a constant tensor;
  * AS3's brute-force symbolic limit and this restriction agreed identically.

  Here it is re-checked numerically.  The full finite-beta traces at beta = 1e3, 1e5, 1e7 with numeric couplings must converge to the
  restricted value (relative difference decreasing, below 1e-4 at 1e7).
* **Regulator:** in the kinetic matrix q^2 -> P_k and q^4 -> P_k^2 (the flat form of Delta -> P_k).
* **Eta terms:** d_t u1 (P - q^2), d_t u3 and d_t(u2 - 2u3/3) multiplying their (P^2 - q^4) pieces.  At a fixed point d_t u1 = 2 g1 k^2
  and d_t u2 = d_t u3 = 0.
* **Photon gauge:** xi = 1; any xi-dependence is reported.
* **Ghosts:** omitted (AS1 argument).
* **STOP RULE, declared now:** the lane stops NOT COMPLETED if either
  * the numerical convergence check fails (no convergence to the restricted value), or
  * the restricted kinetic matrix is singular at the fixed point.

## Gates (all must pass; any failure means NOT COMPLETED)

**G-PUB (reproduce BMS 0902.4630).**

* (i) **Exact.** Every printed closed-form block must equal my own derivation from Table T.1 plus the heat kernel:
  * the unconstrained Lichnerowicz heat-kernel coefficients (eq. `Hexp` table), derived from Vassilevich's general formula with an explicit
    algebraic Einstein curvature tensor carrying a nonzero Weyl part;
  * the constrained coefficients (eq. `d4heat`), via the relations `h1T` and `h2T`;
  * the universal traces (eq. `Tr:ghost` and their expansion `eq:TRuni`), assembled from all ghost and auxiliary entries of Table T.1 with
    BMS's stated statistics;
  * the scalar matter trace (eq. `mattercont`);
  * the EH traces and B1, B2, B3 (eqs. `BEH`, `betaEH`);
  * C1-C4 (eq. `Ccoeff`) and C~1-C~4 (eq. `tCcoeff`), with the optimized-cutoff threshold functions (eqs. `defPhiOpt`, `upsopt`; Upsilon~
    evaluated as its defining integral).
* (ii) **Pure-gravity higher-derivative fixed point** (n_s = 0).  Some real root must reproduce:
  * (g0, g1, g2, g3) = (0.00442, -0.0101, 0.00754, -0.0050) (letter);
  * (g, lambda) = (1.960, 0.218) (Table `t.FP`);
  * theta = (2.51, 1.69, 8.40, -2.11) (Tables `t.Stab`, letter).
* (iii) **Pure-gravity EH fixed point:** (g, lambda) = (0.902, 0.109), theta = 2.52 +- 1.78 i (Table `t.FPEH`).
* **Tolerance** for (ii) and (iii): each number to max(1 percent, half a unit of its last printed digit) relative.
* **Reported, not gated:** the n_s = 1 rows: EH 0.860, 0.131, 2.58 +- 1.95 i; higher-derivative 2.279, 0.251, 0.010, -0.0043; theta 2.67,
  1.39, 7.86, -1.50.
* **Rule for printed inconsistencies, declared now.**
  * If a printed closed-form block disagrees with my derivation, the gate is decided by BMS's printed numbers.  Run the flow once with the
    printed block and once with mine:
    * if only the printed block fails to reproduce BMS's printed fixed point and exponents, the block is a misprint;
    * if only mine fails, G-PUB FAILS;
    * if both or neither reproduce them, G-PUB FAILS.
  * If BMS's printed numbers are mutually inconsistent under a flow that reproduces all printed closed forms exactly, the gate is anchored
    only on the mutually consistent printed numbers (as in AS3).  The inconsistency is shown by a diagnostic, never resolved by a value of
    my own choosing.

**G-MAT-C2.** The type-I matter heat kernels must reproduce the standard trace-anomaly values exactly.

* The (C^2, Euler, R^2) coefficients are those of Vassilevich hep-th/0306138 sec. 4.2.2, i.e. the Christensen-Duff (a, b, c, d) table.
* On a generic Einstein space (C^2 = Riem^2 - R^2/6, E = Riem^2) they reduce to a_4 = (1/180)[a Riem^2 + (d - a/6 - b/12) R^2] in
  (4 pi)^-2 units:
  * scalar (1/180, 1/80);
  * Dirac (-7/360, 1/120);
  * vector with two ghosts (-13/180, -1/60).
* a_0 and a_2 must also match: scalar (1, 1/6); Dirac (4, -1/3); vector with ghosts (2, -2/3).
* The bare Laplacian coefficients on the scalar, Dirac-spinor and 1-form bundles come from Vassilevich (`a4nobou`) with explicit gamma
  matrices and an explicit Weyl tensor.

**G-EH-LIMIT (reported, not gated).**  BMS's EH flow (eqs. `NU-EH`, `betaEH`) is compared with AS3's EH flow in CPR's scheme.  The schemes
differ, so the difference is reported:

* Einstein-space Lichnerowicz (type II) cutoff vs S^4 type Ib;
* alpha-gauge vs beta-gauge;
* the excluded-mode conventions.

**G0:** as in AS1-AS3.

## Trials, fixed points, admissibility (frozen)

* **Graded trial:** EH + C^2 + R^2 with SM matter.  The variables are (g0, g1, g2, g3), equivalently (g, lambda, g2, g3).
* **Reference (reported, not graded):** EH with SM matter in BMS's EH scheme (eqs. `NU-EH` + universal + matter).
* **Root search:**
  * Domain: g in (0, 50), lambda in (-50, 0.5), g2 in (-1e3, 1e3), g3 in (-1e3, 1e3).
  * Starting grid for the graded trial: 10 (g, geometric 0.05..40) x 15 (lambda, linear -45..0.45) x 15 (g2: 0, +-1e-4 ... +-100) x
    9 (g3: 0, +-1e-3, +-1e-2, +-0.1, +-1).
  * Starting grid for the reference: 10 x 15.
  * Roots are merged at relative 1e-6.
  * Roots are flagged within 5 percent of a finite domain bound: g > 47.5, lambda < -47.5, lambda > 0.475, |g2| or |g3| > 950.
* **ADMISSIBLE:** g > 0, and every regulated propagator denominator at P_k = k^2 (the whole support z in [0, k^2] for the optimized cutoff),
  R = 0, is nonzero with the sign it has at the Gaussian reference (lambda = 0, g2 = g3 = 0), i.e. positive after that normalisation:
  * spin-2 (TT, including the C^2 piece): 2 g3 - g1 - g0 > 0;
  * spin-0 (h): -(6 g2 + g1 + (2/3) g0) > 0, i.e. 1 - (4/3) lambda - 96 pi g g2 > 0;
  * universal and ghost denominators P_k, P_k + R/4, 3 P_k - R: positive at R = 0 automatically.

  For EH this reduces to AS1-AS3's rule (1 - 2 lambda > 0, 1 - (4/3) lambda > 0).
* **Selection** (AS1-AS3 rule, plus ONE added rule, declared blind to any AS4 number):
  * exactly one admissible root: it is THE fixed point;
  * none: NOT PREDICTED;
  * two or more: all are reported.  If ALL of them give a P and all those P fall in the same class, that class is assigned; otherwise
    NOT DIAGNOSTIC.
* **From each fixed point:** f_g* = f_g(fixed-point couplings, eta at their fixed-point values, xi = 1).
  * f_g* <= 0: NOT PREDICTED.
  * Otherwise P = downstream_P(f_g*).

## Classes (frozen)

Delta = (P - 137.035999177)/137.035999177.

* **AGREES:** |Delta| <= 2 percent.
* **CLOSER:** |Delta| > 2 percent and |P - 137.036| < |P_EH - 137.036|, using this lane's own EH reference (strict).  If the reference has no
  P, AS1's 44.12 is used.
* **NO IMPROVEMENT:** every other P.
* **NOT PREDICTED:** f_g* <= 0, or no admissible root.
* **NOT DIAGNOSTIC:** see the selection rule.
* **NOT COMPLETED:** a gate fails, or the stop rule fires.

Reported, not graded:

* f_g* at every root, and its ratios to 0.04795 and 0.009805;
* all fixed points, with critical exponents;
* whether g_Y* is IR-attractive (theta_Y = -2 f_g*);
* |P - P_EH|;
* the xi-dependence of f_g;
* the reduced-Planck-start P and the two-loop P (AS3 method);
* the poltergeist indicator, i.e. the sign of g3 and of the spin-2 denominator.

What each outcome would mean, stated now:

* **AGREES:** the route survives this truncation at 2 percent for hypercharge.  It is NOT a derivation of alpha (alpha_2, the hadronic offset
  and the masses are measured; convergence is untested).
* **CLOSER / NO IMPROVEMENT:** the route is not supported at this truncation; no claim either way about the full theory.
* **NOT PREDICTED / NOT DIAGNOSTIC / NOT COMPLETED:** no statement about alpha.

## MUTATE controls (positional argument; each must make the stated check FAIL and exit 1)

* **MUTATE_1:** flip the sign of the graviton contribution (S_2T and S_hh).  G-PUB (i) must FAIL.
* **MUTATE_2:** remove the C^2 term (2 u3 Delta_2L^2 and its d_t) from the spin-2 Hessian only.  The C^2 part of G-PUB (C~1-C~4 exact,
  and the higher-derivative fixed point (ii)) must FAIL.
* **MUTATE_3:** swap the AGREES and NO IMPROVEMENT labels.  The classifier controls (AS2/AS3 CC1-CC5, plus one control for the new
  same-class rule) must FAIL.

## Disclosures, so that nothing is presented as blind when it is not

* I have read BMS's printed pure-gravity higher-derivative fixed point.  Evaluated by hand at P_k = k^2, R = 0:
  * its spin-2 denominator is 2 g3 - g1 - g0 = -0.0100 + 0.0101 - 0.00442 = -0.0043 < 0;
  * its spin-0 denominator 6 g2 + g1 + (2/3) g0 = +0.038 has the opposite sign to the Gaussian reference.

  So under the admissibility rule frozen above (spin-2 positivity is required by the lane brief), the PUBLISHED pure-gravity fixed point
  would be inadmissible.  If the SM fixed point resembles it, the graded trial will be NOT PREDICTED.  This was seen by reading, not
  computing, and is stated before any AS4 computation.
* Also known: AS1-AS3's results (CPR scheme: EH + SM P_EH = 95.578; R^2 + SM NOT DIAGNOSTIC with P 95.27 / 95.71; f_g = pure-TT formula).
* By hand while reading, I checked the following, and nothing else was derived:
  * BMS's universal traces S_1T and S_0 follow from Table T.1 with the stated statistics;
  * the constants of eq. `beta` are the sums of the printed traces;
  * the type-I bare-vector a_4 on Einstein spaces, shifted by R/4, gives BMS's tr_1 a_4 = -(11/180) Riem^2 + (41/120) R^2.

## Scripts and compute

* `as4_*.py`, reusing AS2/AS3 code by import; sympy, numpy, scipy and mpmath.
* Every run uses `OMP_NUM_THREADS=1 nice -n 19 python3`; one process at a time; each under 2 GB RSS.
* One output per mode.  `*_FIRSTRUN.out` is kept for any re-run after a fix, disclosed in an appended Amendment.
* Downloads stay in `as4_scratch/` and are not committed.

## Reading

* **BMS 0901.2984** (letter): read in full.
* **BMS 0902.4630:**
  * read in full: sec. 3 (FRGE setup, gauges, universal traces, matter trace), sec. 4 (EH truncation, Tables t.FPEH and t.FPEHs), sec. 5
    (higher-derivative truncation, eq. `beta`, Tables t.FP and t.Stab), App. A (Hessians, Table T.1), App. B (heat kernels) and App. C
    (traces, C_i, C~_i);
  * not read: sec. 1-2 (introduction, perturbative counterterms) and sec. 6 beyond the conclusions.
* **Vassilevich hep-th/0306138** sec. 4.1 and 4.2.2; **CPR 0805.2909** (for G-EH-LIMIT); AS1-AS3 code.

## Scope / not tested

* Other gauges, cutoff types, profiles and backgrounds.
* Maximally symmetric backgrounds, on which u3 is invisible.
* The individual couplings omega, theta, sigma (only u2 and u3 are distinguishable).
* Fluctuation couplings, matter anomalous dimensions, and gravity contributions to g_2, g_3 and the Yukawas.
* Truncations beyond four derivatives.
* kappa = 1/2 stays FITTED; the SM mass sector stays walled.

## Amendment 1 (appended after the runs; nothing above was edited)

* **Outcome.**
  * PASS: G-PUB (i) (every printed BMS block exact), G-PUB (ii) (higher-derivative pure-gravity fixed point and exponents), G-PUB (iii)
    (EH), G-MAT-C2, G0, and the classifier controls including CC6a/CC6b.
  * G-EH-LIMIT is reported.  MUTATE_1, MUTATE_2 and MUTATE_3 break their targeted checks.
  * The stop rule was not triggered in the final run.
  * EH reference: unique admissible root, P_EH = 96.37265.
  * **Graded EH + C^2 + R^2 trial: NOT PREDICTED.**  The only in-domain root, (g, lambda, g2, g3) = (0.863182, -1.07628, 0.0210528,
    -0.0072056), has a positive spin-2 denominator (+0.058) but a spin-0 denominator of the wrong sign (-0.070).
* **as4_gates.py run 1** was stopped by hand after about 20 min with no flushed output (`as4_gates_FIRSTRUN.out`).
  * Profiling afterwards (scratch development runs, not committed) located the time in sympy simplification of the summed 4-coupling
    expressions and of the beta-system solve.  The same scratch runs showed the printed blocks cancelling exactly.
  * Fixes, with no gate logic changed:
    * block sums are no longer simplified;
    * the higher-derivative beta system is solved numerically per evaluation (it is linear in the d_t terms), with a central-difference
      Jacobian (relative step 1e-6) for the exponents;
    * the EH system stays symbolic, using cancel;
    * output is flushed.
  * Run 2 of the gates is the reported one.
* **as4_trial.py run 1** was stopped at 1.94 GB RSS (cap 2 GB) inside the symbolic f_g step (`as4_trial_FIRSTRUN.out`).  No f_g, fixed
  point or P existed at that point.
  * Fix: an exact reduction from the kernel (TT + conformal mode + photon) to TT + photon.  It is verified symbolically in the code: the
    conformal mode has no kinetic mixing with TT and no h-a vertex, and its M2 entries are TT-off-diagonal only.
  * The F-bar^2 coefficient is now evaluated one field-strength component at a time.
  * A scratch development test confirmed that the reduced formula equals AS3's f_g at u3 = 0.
* **as4_trial.py run 2** completed (`as4_trial_RUN2.out`) with the same roots, f_g and P values as the final run.
  * But its stop-rule check printed relative differences 3.3e-9, 2.2e-12, 1.6e-10 (beta = 1e3, 1e5, 1e7), which are not decreasing.  The
    run therefore ended "NOT COMPLETED (stop rule)".
  * Cause: a precision bug in my check.  The couplings entered the 40-digit evaluation as 15-digit sympy Floats, giving a noise floor
    proportional to beta.
  * Fix: exact rational couplings and an exactly evaluated restricted value.  The frozen criterion (decreasing, below 1e-4 at 1e7) is
    unchanged.
  * **Run 3 (reported):** 3.28e-9, 3.27e-13, 6.65e-16, convergence True.
* **Implementation readings:**
  * the EH reference is BMS's EH truncation, i.e. Table T.1 with u2 = u3 = 0, and the universal traces;
  * the systematics use AS3's method (`as4_systematics.py`);
  * the gate re-run inside the trial prints its full gate log.
