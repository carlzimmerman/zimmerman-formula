# IC40–41 checkpoint: a numerical third-time-compatible interface profile

Base: 351426c4ff7d8661450b589a88c34719c497eca1. The preceding turn made
progress by reproducing L52 and finding a coherent-operator scope error.
This checkpoint advances the SAME IC39 action instead of changing its kernel.
Full original gravity target: **OPEN**, as specified in CRISPY_FRIED_CHICKEN_RECIPE.md.
No failed construction, raw result, or other agent's work was removed.

## What changed mathematically

IC40 independently differentiates canonical metric and fluid evolution three
times at the activation face. It reproduces IC37's second-time gate, but finds
that BOTH previously selected profiles fail the third-time necessary condition.
At 60 digits with increased spatial degree, the quadratic residual derivatives
are respectively 198495817.30400337 and 6488926204.226662. These are not numerical
roundoff. Their full outputs remain in legacy/.

IC41 frees two previously fixed INITIAL DATA, q_r and S_r, alongside S_t=U0
and S_tr=U1. It changes no action coefficient, matter coupling, interpolation
kernel, or empirical input. The second-time source is now independently built
by the canonical time engine, rather than calling the fixed-gradient IC37
source routine. The old implementation remains as a cross-check.

The four solved conditions are

    E_rr = E_rrr = 0,  E = W_tt,
    (W_ttt)_rr = 0,
    (W_ttt)_rrr - 3 E_rrrr x_t/x_r = 0.

The boundary values and first radial derivatives of E and W_ttt are fixed
using the actual lapse response operators, not assigned afterward. The shift
and the canonical fluid gradients/fluxes evolve; matter is not frozen.

## New selected profile (normalized code units, not measured predictions)

    U0     = -0.0026638542879028677964906575498807973531279604047603
    U1     = -2.3967280083306277503463830403196877790804110873573
    q_r    = -86.653213935967970236075745144366311844674183065697
    S_r    = -0.073727236592218636769912753399849133431184481385853

The starting profile's scaled residual norm was approximately 0.207.
Forty bounded trust-region evaluations reached 1.6989221e-5, exhausting that
run's evaluation budget. A direct initial Newton predictor was worse and is
preserved separately. Four high-precision Newton steps (21 uncached evaluations)
reduced the norm to 1.0585248e-36. The respective scales are
(1e7, 1e10, 1e9, 1e12); these are conditioning choices, not tolerances or units.

The final computed four-by-four selector Jacobian has determinant
0.0466599307626851 and singular values approximately
(3.22521, 1.69300, 1.10358, 0.00774328). It is numerically nonsingular.
This is NOT the gravitational Poisson-bracket matrix and is NOT a DOF count.

At the selected rounded data, raw nontrivial residual derivatives are
approximately (-2.6867e-30, -2.0069e-27, -8.7843e-28, -4.8619e-25).
They remain nonzero and agree under increased precision. Therefore the current
artifact is a numerical candidate root, NOT an exact bounded-response solution.

## Moving-face response, derived rather than omitted

For eta=eta4(x), x=a delta+c delta^2/2+..., x_t=t0+t1 delta+..., b=1/4:

    eta_t/eta = 4 t0/(a delta) + d0 + O(delta),
    d0 = 4 t1/a - 2 t0 c/a^2 + 4 t0/b.

Let E4=partial_r^4 W_tt, E5=partial_r^5 W_tt and T4=partial_r^4 W_ttt.
If the lower residual derivatives vanish EXACTLY, the fourth derivative of
R=W_ttt-3(eta_t/eta+S_t)E is

    R4 = T4 - 3[4 t0 E5/(5a) + (d0+U0) E4].

The corresponding one-sided limits would then be

    ell_tt  -> -b^4 E4/(24 exp(S0) a^4),
    ell_ttt -> -b^4 R4/(24 exp(S0) a^4).

At the candidate their values are approximately 0.216330555297023 and
37.6071786206013. Evaluating the SAME rounded profile at 60/80 digits with
spatial degrees 10/11 reproduces these and the load-bearing higher derivatives
to relative error below 1.4e-50. The moving-face speed is 0.0162129942135968.
At 80 digits the third momentum residual through radial order four is below
5.3e-69. These are conditional limits: dividing a nonzero rounded residual by
eta arbitrarily close to the face is still singular. No exact-zero certificate
has been substituted by a tolerance.

## Tests, provenance, and limitations

All created scripts were executed. Nine runner manifests record exact argv,
source hashes, runtime, dirty-state snapshot and resource caps; all validated
against the project root. No missing or invalid declared outputs.

| Run | Child exit | Interpretation |
|---|---:|---|
| tests | 0 | 6 targeted tests, before the final 3 tests were added |
| regressions | 0 | 328 IC-series tests passed in 238.619 s |
| final_tests | 0 | 9 targeted tests passed in 37.301 s; overlaps regressions |
| legacy | 2 | Both former profiles fail third-time compatibility |
| search_negative | 2 | Bounded search exhausted its budget; best profile retained |
| newton_predictor | 2 | Trial profile retained, not a solution |
| refinement | 2 | Numerical necessary-condition root; full theory still OPEN |
| response60, response80 | 2 | Conditional limits agree; full theory still OPEN |

Scientific scripts use the explicit --strict OPEN sentinel (child 2, runner 1).
This is not a Python exception and not a full-theory PASS. Exact symbolic tests,
known-profile reproduction, a changed-gradient matter control, and a singular
Newton-matrix negative control are included. Test-first failures were observed
for the new IC41 modules/features. There was one corrected read-only diagnostic
parser error when a multi-record JSON log gained its final pretty-printed
summary; it did not change scientific inputs or results.

No empirical fits, PPN calculation, full nonlinear Dirac closure, global
FLRW-to-galaxy matching, or full stability claim is added here. The local fixed
coefficient cell is analytic inside its bounds, but the globally C2 table and
the C3 pin activation still require careful treatment at their joins.
Lean and lake were not on PATH; no Lean certificate is claimed.

## Route portfolio and next unavoidable calculation

1. **Active same-action route:** this numerical interface root is a constructive
   improvement over the two failed IC39 profiles. Certify an exact nearby root
   (interval Newton with rigorously enclosed Jacobian, not just another decimal
   refinement), then continue FOURTH-time preservation with the now nonzero
   ell_tt and ell_ttt entering the action-derived flows. The fluid expansion
   must also be extended: the omitted O(g^4) energy terms first contribute at
   fourth time order. Ignoring them would invalidate that calculation.
2. **Function-level route:** use IC38's two residual identities to construct
   common constraint-compatible functions across the collar, not only matching
   finite interface jets. Coordinate this with the exact-root certificate and
   the fixed table's joins. A numerical jet root alone does not supply this.
3. **Claude/Fable series-auxiliary route:** retain the technique, but use
   L52_REPAIR_SCOPE_REVIEW.md. Its coherence/source normalization and different
   kernel need resolution before any result can transfer to IC39. New concurrent
   L46/L50 commits were noticed, not fully audited or imported into this result.

Do not reopen a failed profile without changing the named input. Do not relabel
the approximate interface gate as a completed theory. Credit Carl Zimmerman
for the framework/exponential law and primordial-clock direction; credit
Claude/Fable's L44 for the finite-order activation suggestion already recorded
in IC39, and L52 for its distinct series-auxiliary proposal.

Self-review: Mathbox research-program kept the full target and failed routes;
computation-audit separated the numerical root from exact existence;
proof-audit checked the moving-face and fluid-order dependencies. Mathematical
proofreading covered this note, IC40's derivation and the L52 review; no
mathematical-token corrections were made by proofreading.
