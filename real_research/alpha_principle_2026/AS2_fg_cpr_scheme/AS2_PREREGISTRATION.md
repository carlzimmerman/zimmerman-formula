# Lane AS2 -- asymptotic-safety hypercharge prediction in the Codello-Percacci-Rahmede f(R) scheme, EH + R^2 with SM matter (pre-registration)

Written 2026-10-19, BEFORE any AS2 script existed and before any AS2 computation was run.  Amend only by appending an "Amendment" section at
the bottom; nothing above it may be edited.

## Why this lane exists

Lane AS1 (`AS1_fg_r2_truncation/`, commit 3d8900c10) stopped NOT COMPLETED.  Its gate G1 required the derivation to reproduce
Eichhorn-Versteegen's (E-V, arXiv:1709.07252) EH beta functions (4.8)-(4.9).  Those equations come from an unpublished scheme ("S. Lippoldt,
to appear"), and no declared combination reproduced them.  That gate was a design error: it gated on equations whose scheme cannot be
reproduced from any published source.

AS2 takes EVERY gravitational scheme choice from one published, reproducible source: Codello-Percacci-Rahmede (CPR), arXiv:0805.2909,
section VII.  It is the f(R) scheme of their Table 1.  There are exactly two exceptions, declared below:

* (a) matter is regulated by the AS1 type-I rule;
* (b) f_g is computed on a flat background in the same gauge and with the same eta convention.

The hypercharge route and the downstream are those of lane B trial C5 and of AS1.  This is ONE trial (EH + R^2 with SM matter), plus ONE
reference (EH with SM matter, same scheme), which is reported but not graded.

What this lane is NOT:

* kappa and Z enter nowhere.  This is standard quantum-gravity physics, so any outcome is NOT a framework result.
* Even the best outcome is NOT a derivation of alpha:
  * g_2 has no interacting fixed point (lane B, H-C/E4), so alpha_2(M_Z) is MEASURED;
  * the hadronic offset 9.106 is MEASURED;
  * the charged masses are MEASURED;
  * one truncation step says nothing about convergence.

## Scale statement and downstream (identical to AS1 / lane B C5, by import)

Target: alpha^-1(0) = 137.035999177 (CODATA 2022).  The chain is:

1. g_Y = g_Y* = 4 pi sqrt(6 f_g* / 41) at k = M_Planck = 1.220890e19 GeV.
2. SM one-loop running of alpha_Y down to M_Z (b_Y = 41/6).
3. alpha_em^-1(M_Z) = alpha_Y^-1(M_Z) + alpha_2^-1(M_Z), with alpha_2 MEASURED.
4. alpha_em^-1(0) = alpha_em^-1(M_Z) + 9.106 (MEASURED).

Implementation: `AS1_fg_r2_truncation/as1_common.downstream_P` (lane B's `b3` objects `aY_inv_at`, `a2_mz`, and `rg_common.DELTA_0_MZ`, by
import).  Nothing in the chain is retyped.

## The frozen gravitational scheme: CPR section VII, Table 1, each choice cited to the arXiv source of 0805.2909

* **Truncation:** Gamma_k = sum_{i=0}^{n} g_i(k) int sqrt(g) R^i + S_GF + S_gh (CPR eq. labelled `fofr`).
  * n = 1 (EH) is the reference; n = 2 (EH + R^2) is the graded trial.
  * Dimensionless couplings: g~_i = g_i k^(2i-4).
  * Translation to the AS1 variables: lambda = -g~_0/(2 g~_1), g = -1/(16 pi g~_1) (CPR's Lambda~ and G~), and b = g~_2.
* **Background and decomposition:** Euclidean de Sitter background S^4.  York decomposition of h_{mu nu} (eq. `decomposition`) and of the
  ghosts (eq. `ghostdecomposition`).
* **Second variation:** of int sqrt(g) f(R), taken from eq. (VII.A) for the TT part (`grop`), the vector xi (`xiquadratic`) and the
  (h, sigma) block (`scalarpart`), at d = 4.
  * Known misprint: CPR's summary formula `mainpart` prints the spin-0 denominator with -3 f''(P - R/3)^2.  Its own numerator, the Hessian
    `scalarpart` and the closed form `george` all have +3 f''.  The Hessian `scalarpart` is used.
* **Gauge:** gauge fixing (eq. `fofrgaugefixing`) is S_GF = (1/2) int chi_mu G^{mu nu} chi_nu, with
  chi_nu = D^mu h_{mu nu} - ((1+rho)/4) D_nu h and G_{mu nu} = (alpha + beta D^2) g_{mu nu}.
  * Table 1's gauge is rho = 0, alpha = 0, beta -> infinity (sec. VII.D, "ρ=0, α=0, β→∞").
  * The gauge parameters do not run: CPR sec. VII.D, "We will always neglect the RG running of the dimensionless gauge parameters".
* **Ghosts:** the Faddeev-Popov ghost carries the factor G, and there is a third ghost b with operator G (sec. VII.B, eqs. `ghop`).
  * Jacobians J_V = Delta - R/4, J_S = Delta (Delta - R/3), J_c = J_b = Delta are kept and regulated (sec. VII.C, eq. 8 `faerge`, "we
    shall ... explicitly retain the Jacobians").
* **Traces and excluded modes:** Table 1 uses the convention that "all vector traces would have a prime and all scalar traces would have a
  double prime. This amounts to putting Σ=0" (end of sec. VII.C/VII.D):
  * TT traces are unprimed;
  * every transverse-vector trace omits the l = 1 modes (10 modes at R/4);
  * every scalar trace omits l = 0 and l = 1 (1 mode at 0 and 5 modes at R/3).
  * The mode data are CPR tables `taba2` and `taba21`.
* **Regulator (cutoff type Ib):** sec. VII.C, "We choose a cutoff of type Ib".
  * For every York component, Gamma^(2)(Delta) + R_k(Delta) = Gamma^(2)(P_k(Delta)), CPR eq. (9) (`eq:9`).
  * Optimized profile: P_k(z) = z + (k^2 - z) theta(k^2 - z).
* **Eta terms, exactly as CPR use them:** d_t R_k contains the scale derivatives of the couplings multiplying Delta in Gamma^(2).
  * These are d_t f' and d_t f'', appearing as (P_k - Delta) d_t f' and the d_t f'' terms in the numerators of `mainpart` and `george`.
  * Written in dimensionless variables as (d_t f~' + 2 f~' - 2 R~ f~'') and (d_t f~'' - 2 R~ f~''').
  * They are solved for together with the beta functions.
  * d_t f (the g_0 flow) does not enter, and gauge parameters do not run.
* **Heat-kernel expansion:** eq. `HKasymp`, Tr W(Delta) = (4 pi)^-2 sum_n Q_{2-n}(W) B_{2n}, with Q_n for the optimized cutoff in closed
  form.  For n <= 2, terms up to B_4 (and the excluded modes) are needed.
  * The S^4 coefficients for the scalar, transverse-vector and TT Laplacians are CPR table `taba6`.  They are re-derived in the script
    from the S^4 spectra (`taba2`) and the York relations (`vt`) and (`ttt`), and must agree with the table.
* **Projection:** d g_i/dt = (1/i!) d^i/dR^i [ (1/V) d Gamma_k/dt ] at R = 0, with V = 384 pi^2 / R^2 (the formula after `george`).
* **Not CPR (declared):** the derivation is my own code, reusing the AS1 machinery by import.  CPR's closed form `george` is used only as
  the check target of the gates.

## Exception (a): matter (the AS1 type-I rule; nothing here is a CPR choice)

* **Fields:** minimally coupled N_S real scalars, N_D Dirac fermions and N_V gauge vectors (treated as N_V abelian vectors).
* **Rule:** the bare Laplacian of each field's Gamma^(2) is replaced by P_k, and curvature endomorphisms stay in the denominators.
* **Contributions to d_t Gamma_k:**
  * scalars: (1/2) Tr_S[d_t R_k / P_k];
  * Dirac: -(1/2) Tr_spinor[d_t R_k / (P_k + R/4)], over 4-component spinors, with the bare spinor Laplacian, i.e. D-slash^2 = Delta + R/4;
  * vectors in Feynman gauge (xi_V = 1): (1/2) Tr_V[d_t R_k / (P_k + R/4)] (Ric = R/4 g on S^4), minus Tr_S[d_t R_k / P_k] for the
    complex ghost.
* **No eta terms for matter.**  Matter fields are unconstrained, so their traces carry no primes.
* **SM content:** N_S = 4, N_D = 45/2, N_V = 12.

## Exception (b): f_g on a flat background, in the same gauge and with the same eta convention

* **Definition:** f_g is the graviton contribution in beta_{g_Y} = g_Y (-f_g + (41/6) g_Y^2/(16 pi^2)).
  * It is computed from the F-bar^2 coefficient of the graviton-photon trace on a flat background with constant U(1)_Y field strength,
    with the AS1 method (`as1_g1_fg_flat.py`): bilinear action, vertices from sqrt(g) g g F F, and the rotation-orbit angular average.
* **Graviton part:** the flat-space second variation of int sqrt(g) f(R), i.e. f (sqrt g)^(2) + f' (sqrt g R)^(2) + (1/2) f'' (R^(1))^2,
  with f'' = 2 b.
  * So the R^2 coupling enters the spin-0 propagator.
* **Gauge:** CPR's gauge on flat space.
  * chi_nu = d^mu h_{mu nu} - (1/4) d_nu h (rho = 0).
  * S_GF = (1/2) int chi (beta d^2) chi, which is -(beta/2) q^2 |chi|^2 in momentum space, with alpha = 0 and the limit |beta| -> infinity.
  * It is evaluated as beta -> +infinity and, as a consistency check, as beta -> -infinity.
* **Regulator:** type I(b) in its flat form: every q^2 of the F-bar-independent kinetic matrix becomes P_k (so q^4 becomes P_k^2).
  * The F-bar-dependent vertices are not regulated.
* **Eta convention:** the same as above.
  * d_t R_k contains d_t f' (P_k - q^2) terms and d_t f'' terms.
  * At the fixed point they take their fixed-point values: d_t f' = 2 g~_1 k^2 and d_t f'' = 0.
  * beta and the photon gauge parameter do not run, and there is no eta_A.
* **Photon gauge:** xi = 1 (the gauge used for matter vectors).  Any xi-dependence is reported, not graded.
* **Ghosts:** omitted, for the AS1 reason (the graviton FP operator is A-independent, and the ghost mixing is triangular).
* **STOP RULE, declared now:** if the |beta| -> infinity limit of the F-bar^2 coefficient does not exist (it diverges), or if the
  beta -> +infinity and beta -> -infinity limits differ, then CPR's gauge cannot be carried to f_g.  The lane then stops NOT COMPLETED.

## Gates (all must pass before any trial number is a result; any failure means NOT COMPLETED)

**G-MAT (matter heat kernels):**

* (i) The S^4 traces (b_0, b_2/R, b_4/R^2) of the bare Laplacians on the scalar, Dirac-spinor and 1-form bundles used in the flow equal
  Vassilevich hep-th/0306138, sec. 4.1, eqs. for a_0, a_2, a_4 (source labels `a0nobou`, `a2nobou`, `a4nobou`).
  * These are evaluated with E = 0 and the bundle curvature Omega on S^4: spinor Omega = (1/4) R_{mu nu ab} gamma^{ab} with explicit gamma
    matrices; 1-forms Omega = Riemann.
  * For the scalar and the 1-form, the traces must also equal the Euler-Maclaurin asymptotics of the S^4 spectra (CPR `taba2`; 1-forms =
    transverse vectors plus gradients of the non-constant scalars at eigenvalue lambda_l(0) - R/4).
* (ii) The matter contributions with the regulator removed must reproduce Vassilevich's sec. 4.2.2 table of (a, b, c, d) (Christensen-Duff)
  on S^4, exactly.  The full operators are: scalar Delta; Dirac D-slash^2 = Delta + R/4 (E = -R/4); vector Delta + Ric with two scalar
  ghosts subtracted.  The coefficients concerned are:
  * a_0: 1, 4, 2;
  * a_2/R: 1/6, -1/3, -2/3;
  * a_4/R^2, in (4 pi)^-2 units: 29/2160, 11/2160, -31/1080.

**G-CPR-EH (Einstein-Hilbert in CPR's scheme):**

* (i) **Exact.** For pure gravity, the R^0 and R^1 Taylor coefficients of my derived X(R) = (16 pi^2 / V) d Gamma_k/dt must equal those of
  CPR's closed form `george` (Sigma = 0) times one constant: Y = N X.
  * The equality must hold exactly as functions of (f, f', f'', d_t f', d_t f'') at R = 0.
  * N is fixed by the coupling-independent ghost/Jacobian terms.
  * Disclosure: while reading, I checked two of those terms by hand: -1008(511R^2-360R-1080)/(R-3) and -2016(607R^2-360R-2160)/(R-4).
    They give N = 725760 = 24 x 30240.  That is, CPR's printed prefactor 384 pi^2/(30240 R~^2) corresponds, in the normalisation
    d Gamma/dt = (4 pi)^-2 int sqrt(g)(...), to 1/(30240 R~^2).
  * The single value N = 725760 must then hold for every R^0, R^1 (and, in G-CPR-R2, R^2) coefficient.
* (ii) The pure-gravity n = 1 fixed point must reproduce CPR Table 1, n = 1: Lambda~* = 0.1297, G~* = 0.9878, to 0.1 percent each.
  * Table 2's n = 1 critical exponents (2.382 +- 2.168 i) are reported, not gated.

**G-CPR-R2 (R^2 in CPR's scheme):**

* (i) **Exact.** The R^2 Taylor coefficient of X(R) for pure gravity must equal that of `george` / 725760.
* (ii) Some real root of the pure-gravity n = 2 system must reproduce CPR Table 1, n = 2: Lambda~* = 0.1294, G~* = 1.5633,
  g~_2* = 1.514e-3, to 1 percent each.
  * The n = 2 critical exponents (1.376 +- 2.325 i, 26.862) are reported, not gated.

**G0:** as in AS1.  With f_g = 0.04795 the downstream gives 92.914, and with 0.009805 it gives 137.036 (relative 1e-4).  Lane B's own C5
and C6 values are reproduced to 1e-9.

## Trials and fixed-point selection (frozen; no choosing among roots)

* **Graded trial:** n = 2 (EH + R^2) with SM matter.
* **Reference (reported, not graded):** n = 1 (EH) with SM matter, in the same scheme.
* **Root search:** all real roots of the beta functions in the variables (g, lambda, b), or (g, lambda) for n = 1.
  * Domain: g in (0, 50), lambda in (-50, 0.5), b in (-1e3, 1e3).
  * Starting grid: n = 2 uses 10 (g, geometric 0.05..40) x 15 (lambda, linear -45..0.45) x 15 (b: 0, +-1e-4, +-1e-3, +-1e-2, +-0.1, +-1,
    +-10, +-100); n = 1 uses 10 x 15.
  * Roots are merged when they agree to relative 1e-6.
  * Roots within 5 percent of a domain edge are flagged.
* **ADMISSIBLE:**
  * g > 0;
  * the regulated TT and spin-0 graviton denominators at P_k = k^2, R = 0 are nonzero and have the sign they have at the Gaussian
    reference (lambda = 0, b = 0): 1 - 2 lambda > 0 and 1 - (4/3) lambda - 96 pi g b > 0;
  * the ghost and Jacobian denominators (P_k, P_k - R/4, P_k - R/3) are then positive automatically.
* **Selection:**
  * exactly one admissible root: it is THE fixed point;
  * none: NOT PREDICTED;
  * two or more: all are reported and the verdict is NOT DIAGNOSTIC.
* **From each fixed point:** f_g* = f_g(g*, lambda*, b*, eta terms at the FP).
  * f_g* <= 0: NOT PREDICTED.
  * Otherwise P = downstream_P(f_g*).
  * This gives P_R2 for the trial and P_EH for the reference.

## Classification of the graded P (frozen)

Delta = (P_R2 - 137.035999177) / 137.035999177.

* **AGREES:** |Delta| <= 2 percent.
* **CLOSER:** |Delta| > 2 percent and |P_R2 - 137.036| < |P_EH - 137.036|, using this lane's own EH reference with SM matter in the same
  scheme (strict <; equality is NO IMPROVEMENT).
  * If the reference has no P (no unique admissible EH root, or f_g,EH <= 0), the reference value is AS1's frozen EH miss 44.12, as in AS1.
* **NO IMPROVEMENT:** every other P with |Delta| > 2 percent.
* **NOT PREDICTED:** f_g* <= 0, or no admissible root.
* **NOT DIAGNOSTIC:** two or more admissible roots.
* **NOT COMPLETED:** any gate fails, or the f_g stop rule triggers.

Reported, not graded:

* f_g* (R^2) and f_g,EH;
* f_g*/0.04795 and f_g*/0.009805;
* both fixed points in CPR's variables and in (g, lambda, b);
* critical exponents (eigenvalues of -d(beta_i)/d(g_j) at the fixed point);
* whether g_Y* is IR-attractive (theta_Y = -2 f_g*);
* the truncation shift |P_R2 - P_EH|;
* the xi-dependence of f_g;
* P with the run started at the reduced Planck mass 2.435e18 GeV (lane B's `aY_inv_at` evaluated with the imported module's M_Planck
  temporarily set to rg_common.MPL_RED);
* P with two-loop SM running: lane B's `b2_required_boundary.rhs`, by import, is integrated upward from M_Z to M_Planck with the measured
  couplings, then downward with g_1 = sqrt(5/3) g_Y* at M_Planck.  Its one-loop switch must reproduce the one-loop P.

What each outcome would mean, stated now:

* **AGREES:** the asymptotic-safety route survives this truncation at the 2 percent level, in a published scheme, for hypercharge.  It is
  NOT a derivation of alpha: alpha_2, the hadronic offset and the masses are measured, and convergence is untested.  The next step would be
  a further truncation, as a NEW lane.
* **CLOSER / NO IMPROVEMENT:** the route is not supported at this truncation; no claim either way about the full theory.
* **NOT PREDICTED / NOT DIAGNOSTIC / NOT COMPLETED:** no statement about alpha.

Any other regulator, gauge, truncation or matching scale is a NEW trial in a NEW lane.

## MUTATE controls (positional argument; each must make the stated check FAIL and the script exit 1)

* **MUTATE_1:** flip the sign of the graviton contribution (all metric-fluctuation blocks: TT, xi, (h, sigma)) in the trace.  G-CPR-EH (i)
  must FAIL.
* **MUTATE_2:** remove the R^2 (f'') term from the spin-0 (h) graviton Hessian only.  G-CPR-R2 must FAIL.
* **MUTATE_3:** swap the AGREES and NO IMPROVEMENT labels.  The classifier controls must FAIL.
* **Classifier controls** (always run, not trials):
  * CC1: f_g = 0.009805 gives AGREES.
  * CC2: P = P(0.04795) with reference P_EH = P(0.04795) gives NO IMPROVEMENT (equality).
  * CC3: P = 120 with reference 92.914 gives CLOSER.
  * CC4: P = 80 with reference 92.914 gives NO IMPROVEMENT.
  * CC5: no reference, P = P(0.04795) gives NO IMPROVEMENT via 44.12.

## Scripts and compute

* **Scripts:** `as2_*.py` in this directory; sympy, numpy, scipy and mpmath only.
  * Every run uses `OMP_NUM_THREADS=1 nice -n 19 python3`.
  * One process at a time, each under 2 GB RSS.  A sympy step that grows past that is stopped and the approach simplified (disclosed).
* **Outputs:** one per mode (`*.out`, `*_MUTATE_n.out`).  First-run outputs are kept as `*_FIRSTRUN.out` if a script is re-run after a fix.
  Every fix after a first run is disclosed in an appended Amendment.
* **Downloads:** kept under `as2_scratch/` and not committed.

## Reading (what is read before scripting; recorded in the report)

* **CPR 0805.2909** (read for AS1): sec. IV.A-C, sec. VII in full (eqs. `fofr` ... `george`, `sigma`, Tables 1-4), and the S^4 appendix
  (`vt`, `ttt`, `taba2`, `taba21`, `taba6`).
* **Vassilevich hep-th/0306138:** sec. 4.1 general formulae (`a0nobou`-`a4nobou`), sec. 4.2.2 free fields and the (a, b, c, d) table.
* **E-V 1709.07252** (read for AS1): sec. 3 and sec. 4, for the definition of f_g.
* **Lane B and AS1** code.

What I already know, so that nothing below is presented as blind:

* AS1's outputs: in AS1's de Donder gauges with type-I matter, EH SM fixed points near lambda ~ -1.1 to -1.25, g ~ 0.85-0.97, and f_g
  formulas.
* CPR's pure-gravity Table 1 and Table 2.

No fixed point, f_g or P has been computed in CPR's gauge for this lane.

## Scope / not tested

* Other gauges, cutoff types, regulators, profile functions.
* The Sigma != 0 trace convention.
* Truncations beyond R^2.
* Fluctuation couplings distinct from the background couplings.
* Matter anomalous dimensions.
* Gravity contributions to g_2, g_3 and the Yukawas.
* Threshold effects beyond the declared M_Planck / reduced-Planck systematic.
* kappa = 1/2 stays FITTED; the SM mass sector stays walled.

## Amendment 1 (appended 2026-10-19 after the pre-registration commit c1789e555 and BEFORE any AS2 script was written or run; nothing above was edited)

* **Error found in my paraphrase** of CPR's trace convention.  The bullet "every scalar trace omits l = 0 and l = 1" contradicts CPR's own
  scheme, which the pre-registration freezes as "exactly as used for their Table 1".
  * CPR eq. (8) (`faerge`) adds the two lowest modes of h back explicitly: "+ (1/2) sum_{j=0,1} d_t R_hh(lambda_j)/(Gamma_hh(lambda_j) +
    R_hh(lambda_j))", with the text "the first two modes of h do contribute, and their contribution to the trace is added separately".
  * So in CPR's Table-1 scheme the h trace is effectively UNPRIMED.  CPR's "all scalar traces double primed, i.e. Sigma = 0" refers to
    the remaining scalar traces: sigma, ghosts, third ghost and Jacobians.
* **How it was found:** by hand, while starting the trace code, before any computation.  The f' term of the h block in `george`,
  1008(29R^2+360R+1080) f', carries +29R^2, which is the unprimed scalar b_4.  A double-primed trace would give -511R^2.  The f'' term,
  -2016(29R^3+273R^2-3240) f'', agrees with the same reading.
* **Implemented:** the TT trace and the h trace are unprimed (CPR eq. 8).  All transverse-vector traces are single-primed, and all other
  scalar traces are double-primed (Sigma = 0).
* No other frozen item changes.

## Amendment 2 (appended after the runs; nothing above was edited)

* **Outcome.**
  * PASS: G-MAT, HK-CPR, G-CPR-EH (i), G-CPR-R2 (i) (exact agreement with CPR's closed form at R^0, R^1, R^2, with N = 725760),
    G-CPR-R2 (ii) (0.12936, 1.56329, 1.514408e-3; exponents equal Table 2), G0, and the classifier controls.
  * **G-CPR-EH (ii) FAILS:** Lambda~* = 0.12927 and G~* = 0.98417 vs 0.1297 and 0.9878 (-0.33% and -0.37%; tolerance 0.1%).
  * Per the frozen rule the lane is **NOT COMPLETED**.
  * MUTATE_1, MUTATE_2 and MUTATE_3 fail their stated checks as required.
* **Diagnostic** (`as2_diag_cpr_n1.py`, added after the gate run, not a gate).
  * At CPR's printed Table 1 n = 1 point, the n = 1 flow that reproduces CPR's closed form has nonzero beta functions (1.0e-4, -2.9e-4),
    and exponents 2.380 +- 2.187 i.
  * CPR's Table 2 n = 1 lists 2.382 +- 2.168 i, which equals the exponents at my root (5.2261e-3, -20.2143e-3).
  * So CPR's Table 1 n = 1 row is internally inconsistent with their Table 2 and their closed form; it is consistent with a misprint of
    g~1*.
  * This does not change the verdict.
* **Stop.** No SM fixed point, f_g or P was computed in this scheme.  This keeps any follow-up lane with a re-specified EH gate blind.
  The f_g stop rule was therefore not reached.
* **Fixes after a first run.**
  * `as2_gcpr.py` run 1 crashed with a NameError (`R` instead of `A.R`) after the HK-CPR check and before any gate comparison. It was
    fixed with no other change.
  * `as2_gcpr_FIRSTRUN.out` is kept, with the path prefix replaced by `<repo>/`.
* **Edits before any run** (not post-run fixes): a dead line was removed from `as2_common.em_coeffs`, and the edge-flag rule was written
  out per finite bound (g > 47.5, lambda < -47.5, lambda > 0.475, |b| > 950).  The rule was never exercised.
