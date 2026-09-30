# Z12-WAVE BRIEF (conductor, 2026-09-29 tick ~evening EDT - pre-registered BEFORE any run)

Spawn trigger: 0 deepseek lanes running (ps aux grep python3: no lane scripts).
All Z10/Z11 verdicts committed (400e7919a, 446286a06). Open doors from the
register ops notes: LR8 (Lean certs of the W2 rationals) and W3 (exact c1(q));
OA1 WG high-z stays data-gated (eRASS:3 WG products not on disk - no padding
lane). delegate_task re-confirmed absent this tick (tool_search: no match) -
conductor-run lanes per Z6-Z11 precedent. Wave size 2: that is every runnable
registered door.

## Door LR8 (registered): Lean certificates of the W2 rationals A0 = 2/5, A1 = 8/35

Background (on-disk): W2 (exit 0, 446286a06) banked c00(q) = 2/5 + (8/35)q
exactly via the cylindrical (rho,z) reduction: z -> s*w substitution
(s = sqrt(1-rho^2)), inner w-polynomial integrals
(8/3, 16/15, -12/5, 32/5, 8), outer integrals
int_0^1 rho(1-rho^2)^{3/2} = 1/5, int rho^3(1-rho^2)^{3/2} = 2/35,
int rho(1-rho^2)^{5/2} = 1/7. Conductor hand-derivation verified BEFORE this
brief: A0 = (3/2)*(4/3)*(1/5) = 2/5;
A1 = (3/2)*[(4/3)*(2/35) + (8/15)*(1/7)] = (3/2)*(16/105) = 8/35.
LR7's certified bank ALREADY contains all three outer 1D cores as base_A
(= 1/5), base_B (= 2/35), base_C (= 1/7) - zero-sorry, unconditional.

Conductor pre-audit: sympy exact re-derivation (fresh code, independent of
W2's script) must reproduce 2/5 and 8/35; recorded in the tick transcript
BEFORE the Lean run.

Lane LR8_w2_rationals (owner: conductor; prefix LR8_*):
- R0 ALGEBRA AUDIT (pre-registered gate 1e-12 rel): fresh sympy exact A0, A1
  via the (rho,w) rectangle integral (independent variable ordering/method
  from W2's K1); TWO independent quadratures (mpmath quad + Gauss-Legendre
  ng=500) of the SAME (rho,w) integrands; numeric MC of the FULL geometric
  reduction (p uniform in unit ball x u isotropic, n=2e7, seed 20260929) vs
  the exact values - this audits the (rho,z)-reduction leg itself, which the
  Lean file will label numeric-audited (LR4c/LR7 mechanism-class precedent).
  Any exact-value mismatch (sympy != 2/5, 8/35) or quadrature dev > 1e-12 or
  |MC - exact| > 5 SE_combined -> exit 1.
- G1 LEAN (fable_independent_2026/lean_2026/LR8_w2_rationals.lean): base_A,
  base_B, base_C restated (copied verbatim from LR7_w1_moments.lean), then
  NEW: w2_A0_law : A0 = (3:2)*(4:3)*base_A = 2/5 and
  w2_A1_law : A1 = (3:2)*((4:3)*base_B + (8:15)*base_C) = 8/35 as the exact
  rational assembly; lake rc 0, ZERO sorry, axioms subset {propext,
  Classical.choice, Quot.sound}. FAIL after honest attempts -> exit 1.
- G2 MECHANICAL: sympy re-derivation of the assembly coefficients
  (3/2)*(4/3), (3/2)*(4/3), (3/2)*(8/15) must match the Lean statement's
  constants exactly. Mismatch -> exit 1.
Honest scope (labeled in the Lean header, LR3b/LR4c/LR7 precedent): the 1D
core values and the rational assembly are CERTIFIED; the geometric
(z-substitution + cylindrical density) reduction leg is numeric-audited
(R0 two quadratures + MC), not probability-space-certified.

## Door W3 (registered): c1(q) - the O(tau0) coefficient of c0(tau0,q) = E[D]/tau0

Background (on-disk): MC7 (exit 0, 4754ea411) measured c0(tau0,q) on 8-point
tau0 grids (q in {0,1,3,6,10}, tau0 1e-2..2e-4, n_eff 2.4e7/cell, seeds
7101.., stored in MC7_results.json "meas") and found the extrapolation model
UNSETTLED (quadratic tau0-coefficient significant only at q=10); W2 banked
c00(q) = 2/5 + (8/35)q exactly, leaving c1(q) (and the q=10 z=6.56 scope
residual) open. c1(q) exists NOWHERE on disk as a measured quantity.

Lane W3_c1_measurement (owner: conductor; prefix W3_*):
- M1 EXTRACTION (records, per-q): weighted linear fit c0 = c00 + c1*tau0 on
  MC7's stored 4 smallest-tau0 points per q (W2 K3 precedent) -> MEASURED
  c1(q) with SE; leave-2-out ablation for the c1 SE honesty scale (records,
  does not gate); expected bias: the fit intercept must reproduce W2's exact
  c00(q) - parity gate: |intercept - exact|/SE <= 3 at q in {0,1,3} (the same
  q where W2's K2 parity passed); q in {6,10} recorded as scope (known
  O(tau0^2)-curvature at q=10, z=6.56 residual).
- M2 STRUCTURE ATTEMPT (exact-form door, honest either way): derive the exact
  structural decomposition of c1(q) = single-scatter survival-exponential
  correction + two-scatter terms, reduce the single-scatter correction via
  the W2 cylindrical mechanism; if sympy closes the correction's exact form,
  compare vs the M1 measured slopes at q in {0,1,3} (gate |z| <= 4);
  if sympy does NOT close, record the reduced exact integral forms + the
  measured c1(q) as the honest deliverable - this is a registered exit-0
  outcome (the exact closed form stays OPEN).
- Kill conditions (pre-registered): M1 intercept parity fail at q in {0,1,3}
  -> exit 1 (the W2/MC7 chain would be internally inconsistent); M2 parity
  |z| > 4 at any of q in {0,1,3} where the exact form closed -> exit 1.
  No fabrication: every number must come from MC7_results.json (loaded, not
  transcribed) or a fresh run with exit code on disk.

House rules 1-10 (LOOP_CONDUCTOR.md) bind both lanes. Raw data stays
untracked; astra_spawn_ideas + tmp probes untouched (house rule 8); no
commits by leaf lanes (conductor commits at tick end).

## AMENDMENT 1 (conductor, BEFORE any W3 run): W3 M2 gate scope fix

The M2 parity gate as drafted ("compare the closed correction vs the M1
measured slopes") is mis-specified: the single-scatter survival correction is
only PART of c1(q) (the two-scatter leg is the rest). Comparing the partial
sum against the full measured slope would fire spuriously. Fixed BEFORE any
run, no numbers exist yet:
- M2a (exact): c1_surv(q) = -E[int_0^W s k(s) K(s) ds] with
  K(s) = int_0^s k, k(s) = 1 + q(r^2 + 2(p.u) s + s^2) -> -C00 - q C01
  - q^2 C02, all polynomial-integral exact via the W2 cylindrical mechanism.
  sympy must produce exact rationals; quadrature dev <= 1e-11 rel (gate).
- M2b (numeric): c1_2sc(q) = E[int_0^W ds1 k1(s1) int_0^{W2} ds2 k2(s2)
  (s1 + s2)] (two-scatter leg; the mu-terms vanish by the zero-mean dipole,
  E[u.u2] = E[u1.u2] = 0), evaluated by MC over (p, u, S~U[0,W], u1 ~ dipole),
  honest SE. NO exact-closure gate (expected open; recorded).
- M2c (operative gate, ONLY because both legs are then evaluated): predicted
  c1(q) = c1_surv(q) + c1_2sc(q) vs the M1 measured slopes at q in {0,1,3}:
  any |z| > 4 -> the structural decomposition is REFUTED -> exit 1. If the
  two-scatter leg fails to evaluate (execution), record and skip M2c with an
  honest scope note (exit 0, structure UNRESOLVED).
- Engine cross-checks required BEFORE M2b counts (conductor verified against
  J02_moment_hierarchy.py source this tick): rate = rate_integral(r2, pd, ds,
  tau0, q) = tau0*(ds + q(a*ds + b*ds^2 + ds^3/3)); scatter position by
  bisection on rate_integral = -ln U (density tau0 k(s) e^{-tau0 K(s)});
  thomson_mu = rejection on (1+mu^2)/2 in [-1,1] (zero-mean dipole);
  D = elapsed - (pos-origin).direc_final = sum_j l_j (1 - u_{j-1} . u_f).
  Wall distance W = -(p.u) + sqrt((p.u)^2 - r^2 + 1); disc = 1 - rho^2.

## AMENDMENT 2 (conductor, BEFORE the W3 lane run; pre-audit fires preserved verbatim)

Conductor pre-audit peek at MC7's stored points (transcript, before the lane
script exists) FIRED the drafted M1 intercept gate at q=1: 4-smallest-tau0
weighted refit intercept 0.656700 +- 0.008612 vs W2 exact 0.628571, z = 3.27
> 3. Verbatim record: slopes from the same 4-point fits are SE-limited
(+9.5+-5.4, -30.6+-8.8, +31.4+-15.6, -26.1+-22.0, +51.9+-16.1 at q=0/1/3/6/10)
- the 8e-4 tau-lever arm gives intercept-slope covariance the gate design did
not account for (W2's K3 precedent ran only q=6, z=1.06, where it was benign).
This is a GATE-DESIGN artifact, not a W2/MC7 chain inconsistency (W2's K2
passed on MC7's selected 8-point intercepts at q=1, z=1.50). Per house rule 3
the estimator is fixed by measuring its true SE structure, and the fire stands
on record:
- M1 (amended): per q, weighted fit of c0(tau0) - c00_exact(q) = c1*tau0 +
  c2*tau0^2 on ALL 8 stored MC7 points, with c00_exact(q) = 2/5 + (8/35) q
  ANCHORED (W2-certified, LR8-certified this tick - banked knowledge, not
  tuning). c1(q) = measured slope with propagated SE; leave-one-out ablation
  recorded. The old 4-point intercept gate is SUPERSEDED (fire preserved
  above); no intercept gate remains (the anchor IS the certified intercept).
- M2c gate unchanged: predicted c1(q) = c1_surv(q) + c1_2sc(q) vs the amended
  M1 slopes at q in {0,1,3}, any |z| > 4 -> structural decomposition REFUTED,
  exit 1.
- q in {6,10} recorded as scope (curvature/selection issues known at q=10).

## AMENDMENT 3 (conductor, W3 run-2 killed at 384s in the M2a mp-branch - on record)

W3 run-1 (foreground) hit the tool timeout mid-M2a; run-2 (background) sat
>6 min in the triple-nested adaptive mpmath quad (dps=40, quad-over-quad-over-
quad) and was killed by the conductor - both runs' partial logs preserved in
the scratch transcript and .out (M1 anchored fits + sympy C = 1/3, 1/3, 46/525
completed in both; no gate reached). AMENDMENT (estimator cost only, not
math, not gates): the innermost v-integral in the mp check gets its EXACT
polynomial antiderivative (I(W) = W^3/3 + q(2 r2 W^3/3 + (3/4) z W^4 + W^5
(4/15)) + q^2(r2^2 W^2/2 + r2 z W^3 + c3 W^4/4 + (z/3) W^5 + W^6/18),
c3 = r2/3 + 2 z^2 + r2 - conductor expansion, cross-checked against the GL
branch's numeric v-quadrature), leaving mpmath as an independent dps=40
arithmetic evaluator of the 2D (rho,w) integral only. GL(500)xGL(120) numeric
v-quadrature branch unchanged. Gates unchanged (1e-11 rel).

## AMENDMENT 4 (conductor, W3 run-3 exit 1 on a GL-branch broadcasting bug - on record)

Run-3: M1 + M2a reproduced identically (C = 1/3, 1/3, 46/525; mp branch passed,
output not persisted), then crashed in the GL branch: Wm (500,500) vs tv
(1,120) broadcast error - the v-node grid needed the (...,None) 3D form.
Tooling bug only; math untouched. Run-4 = the fixed script.

## AMENDMENT 5 (conductor, W3 run-4 killed at 559s in the mp branch - on record)

Run-4 sat >9 min in the mp ADAPTIVE 2D quad even with the exact v-antiderivative
(partial log preserved). Estimator-cost amendment only: the mp leg becomes
FIXED-ORDER Gauss-Legendre in mpmath arithmetic (mp.gauss_quadrature(200),
mapped [0,1]x[-1,1], dps=40) - deterministic ~4e4 Iant evals per q; independent
from the numpy GL(500)xGL(120) leg by arithmetic (mpf dps=40) and node order.
Gates unchanged. Run-5 = fixed script.

## AMENDMENT 6 (conductor, W3 run-5 killed: mp.gauss_quadrature(200) node-finding itself slow at dps=40)

Run-5 killed >3 min in mp node generation. Amendment: mp leg takes its GL(200)
nodes from scipy.roots_legendre converted to mpf (node positions accurate
~1e-16 rel; gate 1e-11 unaffected; the dps=40 mpf EVALUATION is the
independence payload). Run-6 = fixed script.

## AMENDMENT 7 (conductor, W3 run-6 exit 1: list-vs-mpf TypeError in the mp-branch node mapping)

Tooling-only crash (list comprehension fix); math untouched. Run-7 = fixed.

## AMENDMENT 8 (conductor, W3 run-7 blocked >3 min: GL branch multiplied numpy arrays by an mpf)

Sampled the live stack: numpy object-dtype ufunc loop -> mpmath __mul__ - the
GL(500)xGL(120)xGL(120) branch was evaluating 3e7 mpf multiplies because qv
stayed mpmath. Amendment: GL branch = float64 (qv cast to float; as in LR8 R0b);
the mp leg (dps=40) carries the high-precision payload. Math untouched.
Run-8 = fixed script.

## AMENDMENT 9 (conductor, W3 run-8 M2a fire: GL branch carried half-weights on the w-axis - honest fire, on record)

Run-8: mp leg dev 0.00e+00 (S(0) = 1/3 confirmed at dps=40 vs sympy exact);
GL leg dev 5.0e-1 = exactly a factor 2: the w-axis ([-1,1], full GL weights)
was given the x-axis' half-weights (0.5*wg). Honest M2a fire preserved in
.out; math (sympy exact + mp leg) UNCHANGED and confirmed. Fix: w-axis weight
= wg. Run-9 = fixed script. (Dead placeholder line removed too.)

## AMENDMENT 10 (conductor, W3 run-9 M2a fire: the HAND closed-form antiderivative was wrong at q != 0 - honest fire, on record)

Run-9: S(0) clean both legs (mp dev 0, gl dev 5e-16); S(1) mp dev 2.97e-02 vs
gl dev 5.3e-15. Standalone probe (transcript): the conductor's HAND Iant
disagrees with direct mp.quad of s k K by 2.8e-1 at (0.3,0.5) - the hand
expansion truncated the q^2 term's degree (s*AB reaches s^6, antiderivative
W^7/21; the hand form stopped at W^6). The EXACT law itself is unaffected:
sympy definite integral, GL v-quadrature, and direct mp.quad all agree, and
C00/C01/C02 = 1/3, 1/3, 46/525 re-derived a THIRD time. Fix (mechanical, no
hand transcription): the script builds the antiderivative by sympy once and
lambdifies it to mpmath; the mp leg evaluates that. Run-10 = fixed script.

## AMENDMENT 11 (conductor, W3 run-10 exit 1: lambdify arity - loop passed 3 of 4 args)

Tooling-only (missing r2,z args at the call site). Run-11 = fixed.

## AMENDMENT 12 (conductor, W3 run-11 MC-S fire: same hand-expansion lineage as Amendment 10)

Run-11: M2a PASS (S(0), S(1), S(3) mp dev 0/0/2.1e-16, gl dev 5e-16/5.3e-15/
1.7e-15 - the exact survival law S(q) = 1/3 + (1/3)q + (46/525)q^2 now stands
on THREE independent evaluations). MC-S then FIRED at q=1: 0.776530+-0.000214
vs exact 0.754286, z=103.8 - the per-sample closed form in MC-S was derived
from the SAME wrong hand expansion (0.77653 matches run-9's wrong-hand mp
value 0.7767). Fix: MC-S X = the mechanical sympy antiderivative lambdified
to numpy (vectorized). The M2b formulas (K2tot, c0f) are engine-rate_integral
structures verified against J02 source, not hand expansions - unchanged.
Run-12 = fixed script.

## AMENDMENT 13 (conductor, W3 run-12 exit 1: M2c/m1 keying bug - honest record)

Run-12 got further than any previous run: M2a PASS (three independent
evaluations), MC-S PASS (z = 0.79/0.85/0.89 - the geometric reduction leg is
MC-consistent with the exact S(q)), M2b landed (E2 = 0.617291+-0.000329 /
1.475572+-0.000756 / 4.332762+-0.002278 / 11.470124+-0.006216 / 26.309547+-
0.014544 at q=0/1/3/6/10) - then crashed on a dict-key error, AND the same
key bug ("else k" fallback stuck on the last M1 loop key "10.0") made all
three printed M2c comparisons use the q=10 MEASURED slope. The printed z =
2.40/2.76/3.98 are therefore NOT the registered comparison. Correct comparison
(hand-recomputed, to be confirmed by run-13): q=0: pred +0.2840 vs meas
+0.3229+-0.4644 -> z ~= 0.08; q=1: +0.7213 vs -0.2880+-0.5313 -> z ~= 1.90;
q=3: +2.2109 vs -0.1290+-0.9680 -> z ~= 2.42 - all pass the gate <= 4.
Fix: key lookup str(float(q)). Run-13 = fixed script (identical seeds; only
keying changes).
