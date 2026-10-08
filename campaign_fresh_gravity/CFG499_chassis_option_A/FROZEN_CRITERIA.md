# CFG499 FROZEN CRITERIA: option A of CFG469 as a full track (lenient black holes on the C-H/K khronon chassis)

Frozen 2026-10-08, before any CFG499 script exists and before any CFG499 computation has been run. Nothing below may be
edited after the commit that adds this file; corrections go in a dated section appended at the end.

Theory plus offline numerics only; no downloads. Read-only on every other lane. kappa = 1/2 is FITTED and plays no role
(a0 enters none of the computations below; both footings 9.36e-11 / 1.13e-10 give identical results, and this is
printed). No dark-matter particle is added; the cold fluid's mass is still required. Nothing here says "theory closed".
This is the relativistic chassis, not candidate B: B has no action, so nothing here is a test of B.

## 0. The question, and disclosure

The owner (2026-10-08): "try both A and C". This lane pursues option A of CFG469 (28bcfedb7): keep the C-H/K khronon
chassis (khronometric sector beta = 0, lambda = c_2, alpha = alpha_c) and accept black holes that are regular OUTSIDE the
universal horizon (UH), with CFG319's option-C defect on the UH (curvature ~ x^-0.382, integrable, metric C^{1,0.618},
causally hidden). CFG469 worked in the test-khronon limit and named three next tests. A parallel lane does option C; it
is not read or used here.

**Not blind.** Read before this file: CFG469 (README, criteria), CFG467 (README, JSON), CFG318 and CFG319 (READMEs, JSON,
CFG319's script), CFG320 README, L350's header and output (cosmological-G gate and its leaf-average construction). No
CFG499 computation has been run. Expectations written down now so they cannot be tuned later:
- (1) at the UH the khronon block's leading coefficients are pure alpha-terms while the Einstein operator has a regular
  point there; the metric response is expected to be one or two powers weaker than the khronon stress, so the UH
  exponents are expected NOT to move at first order. A log (resonance with the integer exponents -1, 0) is the failure
  mode to look for.
- (2) at alpha -> 0 the khronon is the maximal (K = 0) slicing; maximal slicings of Oppenheimer-Snyder collapse are
  recalled (literature, PROVISIONAL, not read) to freeze at the limiting surface r = 3M/2, which is CFG319's UH. The
  alpha > 0 selection of option C over C' inside the O(M/c_S) boundary layer is NOT expected to be computable here.
- (3) the no-constant sliver [9.624e-14, alpha_rs(c_2)] exists only for c_2 >= ~0.038 (CFG467/CFG469) and only on the
  leaf-average branch of the lambda term (L350 G5): on the plain branch, Planck-era cosmology puts c_2 below 2.9e-3.

## 1. Fixed inputs (read from committed files, never refitted)

- Action (khronometric, 16 pi G = 1, signature -+++): S = int sqrt(-g) [R - lambda K^2 + alpha a.a], beta = 0,
  lambda = c_2, alpha = alpha_c (CFG291/CFG318 map; CFG319's L).
- CFG319 `cfg319_moving_bh_results.json`: W5 points (alpha, lambda, rUH, YU1 = y1, rootsU), S22, dK_ops, daa_ops.
- CFG467 `cfg467_results.json`: per-gate sets; CFG320 Lambda_HL_max = 9.87e8 GeV, c_2 grid; L340 window
  alpha_c in [9.624e-14, 3.2e-9], c_2 in [7.2888e-3, 0.0667].
- Units M = 1, ingoing Eddington-Finkelstein (V, r, theta, phi), e(r) = 1 - 2/r. Static khronon T0 = V + H(r),
  H' = -1/(Y(Y+W)), W = sqrt(Y^2 - e); at the UH Y = 0, W0^2 = -e(r_UH), Y'(r_UH) = y1.

## 2. Test (1): the metric-coupled moving black hole

Scope: O(v), l = 1 even parity, stationary, beta = 0. Metric g = g_Schw + v h with h_VV = A cos, h_Vr = B cos,
h_rr = C cos, h_Vtheta = -D sin, h_rtheta = -E sin, angular part r^2 Kf cos; khronon T = T0 + v F(r) cos(theta).
The quadratic Lagrangian of the FULL action (Einstein-Hilbert + khronon) in these 7 functions is derived in sympy and
angle-integrated.

**The order reached (stated now).** The background is Schwarzschild plus the test-khronon background (exact solution of
the khronon equation on Schwarzschild; its own O(alpha) static metric correction, CFG318's q, is not included). The
back-reaction is computed as the first round trip of an expansion in the number of metric-khronon exchanges:
F0 (the test-khronon UH modes) -> h1 (the Einstein response to F0's O(v) stress) -> F1 (the khronon response to h1).
This is consistent at that order (the O(v) stress of an on-shell khronon is conserved on Schwarzschild). It is LOCAL at
the UH (generalised Frobenius series in x = r - r_UH), plus the global count argument in 1c. No global coupled
boundary-value problem is solved. This is the approximation that limits the conclusion, and it is printed.

**Controls (load-bearing).**
- K1: the same Lagrangian engine on Minkowski (plane waves in (t, z), scalar sector, with metric mixing) gives the
  khronon dispersion omega^2 = c_S^2 k^2 with c_S^2 = lambda (2 - alpha) / (alpha (2 + 3 lambda)) exactly (L340/XC1/CFG467
  formula; fixes the sign and normalisation of R against the khronon terms), and the tensor speed 1.
- K2: at h = 0 the khronon block reproduces CFG319's committed S22 exactly (symbolic difference 0).
- K3: the Einstein-Hilbert block is gauge invariant: a pure-gauge h = L_xi g_Schw with l = 1 xi annihilates its
  Euler-Lagrange equations identically (sympy, exact).
- K4: the khronon cross terms are jointly gauge invariant on an on-shell background: the khronon Euler-Lagrange equation
  evaluated on (h, F) = (L_xi g, -xi.dT0) vanishes to <= 1e-20 relative at random points, with Y'' from the static
  khronon equation (40 digits).
- K5: the h1 response satisfies ALL six Einstein equations (the three gauged-away components' equations included) order
  by order in the series, residual <= 1e-20 relative (conservation of the source, i.e. the derivation is consistent).

**Pass criteria (at every W5 point; the stealth closed form is also printed).**
- 1a WEAK: for the option-C mode s+ (and the regular modes -1, 0):
  - the metric response h1 in a gauge regular at the UH goes as x^p with p > 1 in every component (metric stays
    C^1 at the UH), or is analytic there;
  - the O(v) curvature perturbations dR (Ricci scalar) and d(R_abcd R^abcd) go as x^q with q > -1 (integrable), and the
    O(v^2) quadratic invariants as x^(2 q_min) with 2 q_min > -1;
  - the feedback F1 introduces no exponent below s+ in the s+ sector and no logarithm in the integer sector that would
    make tau = -exp(-kappa_U T) fail to be C^1. If the feedback is resonant at the leading order (n = 0), the induced
    exponent shift ds is computed; s+ + ds must stay in (1/2, 1).
- 1b HIDDEN: T -> +infinity on the UH in every direction (the UH is still the T = infinity leaf) and tau stays C^1 with a
  non-vanishing gradient and a timelike normal in the perturbed metric (needs h bounded and continuous at the UH and
  1 + s+ > 1). Pass iff both.
- 1c COUNT: the boundary-condition count with metric coupling at this order:
  - (i) the Einstein l = 1 block adds no condition: every homogeneous solution of the gauge-fixed Einstein block is pure
    gauge or one of the l = 1 physical constants (dipole position / momentum), none excluded at r = 2, at the UH or at
    infinity (computed: dimension of the homogeneous solution space vs. the residual-gauge dimension, sympy);
  - (ii) the feedback source into the khronon equation is regular at r_S (so r_S keeps exactly one no-log condition) and
    decays at infinity (no new inadmissible mode);
  - (iii) reading: the coupled spin-0 horizon sits where alpha (2 + 3 lambda) W^2 = lambda (2 - alpha) Y^2 (K1's c_S);
    it remains a single regular singular point (shift reported, not a gate).
  - Pass iff Delta_len (coupled) = 0 (option C determined, no extra condition). Delta_strict (coupled) is reported
    (expected +1, as RB2019).
- (1) PASSES iff 1a, 1b, 1c pass at all five W5 points and K1-K5 pass. (1) FAILS if any of 1a/1b/1c fails at any W5
  point (the failing item and point are named). A load-bearing control failure makes (1) UNDECIDED (not a pass).

## 3. Test (2): collapse

- 2a FORMATION (computed, alpha -> 0 at the record's lambda): marginally bound Oppenheimer-Snyder collapse (flat FRW
  dust interior, Schwarzschild exterior, M = 1). At alpha = 0 the khronon equation is solved by any K = 0 slicing with
  zero stress for every lambda, so the khronon is the maximal slicing that is asymptotically the Schwarzschild time T.
  Compute the family of maximal slices (interior ODE with a regular centre, matched C^1 at the surface to the exterior
  W = C/r^2 slice), labelled by T at infinity. Pass iff: (i) slices exist up to T >= 40 M; (ii) C(T) increases
  monotonically to 3 sqrt3/4 within 1e-6; (iii) the surface radius on the slice R_s(T) > 3/2 for every T and -> 3/2
  (no exterior leaf enters r < r_UH; the limiting leaf is the UH, formed); (iv) the central lapse dtau_c/dT decays as
  exp(-kappa T) with kappa within 1% of kappa_U = y1 W0 = 2 sqrt6/9 at late T. Control K6: the interior slice satisfies
  K = 0 to <= 1e-9 (independent finite-difference evaluation of the mean curvature) and the matching is C^1 (normal
  continuous) to <= 1e-9.
- 2b WEAK BRANCH SELECTED BY COLLAPSE (computed, alpha -> 0): the O(v) l = 1 perturbation of the late maximal leaves
  (dK = 0, F -> -r at infinity) on the exterior part of the leaf with ANY finite inner data at the star surface (a
  family of Robin ratios at R_s(T), including extreme ones). As C -> 3 sqrt3/4, fit F in the throat region to the two
  local branches of the alpha = 0 dK = 0 operator at the UH. Pass iff the less regular branch's relative amplitude -> 0
  (a power law in R_s - 3/2) for every inner datum, so the late leaf converges to the weak branch.
- 2c (alpha > 0, inside the O(M/c_S) boundary layer: C versus C'). NOT computable with this lane's machinery (a
  time-dependent, partly elliptic khronon evolution at c_S = 444 - 8e5 inside a layer of width ~1e-3 - 1e-6 M). Reported
  as ARG: the late-leaf boundedness argument (a mode whose leaf displacement kappa x v F diverges as x -> 0, i.e. s-,
  cannot be the limit of leaves that are regular at finite T), with the exponent bookkeeping computed. Not a pass.
- (2) PASSES iff 2a, 2b pass AND 2c is computed and passes. If 2a or 2b fails, (2) FAILS (named). If 2a and 2b pass and
  2c is an argument only, (2) is PARTIAL.

## 4. Test (3): the window with every CFG467 gate at the chosen c_2

- Choose c_2 where the no-constant sliver is open: the CFG320 grid points c_2 = 0.0383, 0.0506, 0.0667, and the sliver's
  lower c_2 edge (where alpha_rs(c_2) = 9.624e-14) found by bisection. At each, alpha_rs from Lambda_sc = Lambda_HL_max
  with Lambda_sc = sqrt(alpha) M_P c_s^(-1/2), c_s^2 = c_2 (2 - alpha)/(alpha (2 + 3 c_2)) (control K7: reproduces
  CFG467's 1.1783e-13 at c_2 = 0.0667 and CFG320's 3 open grid points).
- Evaluate every CFG467 gate G1-G12 at a 7-point alpha grid inside each sliver (edges included), from the formulas
  (re-implemented, then compared with CFG467's committed sets at the grid c_2: control K8), plus the alpha-independent
  rows at that c_2: L340 tracking floor (c_2 >= 7.29e-3), the cosmological-G gate on the leaf-average branch
  (|G_cos/G_N - 1| = alpha/2) AND on the plain branch (1.5 c_2 vs the L350 ceilings, printed), GW170817 (beta = 0),
  Cassini (alpha-independent), and test (1)'s coupled exponents at that c_2 (s+ in (1/2, 1)).
- Also the window WITH the hierarchy (A4-H: [9.624e-14, 3.2e-9], +1 UV scale) at the same c_2, every gate.
- Pass iff at >= 1 chosen c_2 a non-empty alpha set passes every gate at its strict reading except G12, which is taken
  at reading W (the option-A condition) and requires (1) not FAILED. The plain-branch cosmological-G row is reported:
  if the sliver needs the leaf-average branch, that is a named condition, not a fail (the chassis window of L340/CFG467
  is already the leaf-average branch).
- (3) FAILS iff no chosen c_2 has a non-empty all-gate set.

## 5. Verdict for option A (frozen)

- **A STRENGTHENED** iff (1) PASSES (the defect stays causally hidden and integrable with metric response, count
  unchanged) AND (2) PASSES (collapse forms the weak-defect UH) AND (3) PASSES (a non-empty window remains with all
  gates).
- **A WEAKENED** iff any of (1), (2), (3) FAILS (each failing test is named).
- **A NOT DECIDED (named open items)** iff none fails but at least one is PARTIAL or UNDECIDED (named; e.g. 2c).
- Option A's standing conditions are unchanged by any of these: the owner must adopt reading W; under the strict
  (RB2019 / FHB2021) criterion G12 remains a KILL; the full window needs the Pospelov-Shang hierarchy (+1 UV scale).

## 6. MUTATE (`CFG499_MUTATE=1`; outputs `*_MUTATE.out`, `cfg499_results_MUTATE.json`)

- M1 (alpha_c outside the window must fail (3)): alpha_c = 1e-11 at c_2 = 0.0667 without the hierarchy (above
  alpha_rs; G11 must fail) and alpha_c = 1e-6 with the hierarchy (G6 PPN alpha2 must fail). Both must be flagged and the
  all-gate set at those points must be empty.
- M2 (a strong-defect point must fail (1)): run test (1)'s pipeline on the strong UH branch s- (CFG319's option C', the
  strong-defect solution) at the W5 points: 1a and/or 1b must FAIL there (curvature non-integrable and/or tau not C^1).
  Plus an injection: a synthetic exponent s = 0.3 must fail the O(v^2) integrability clause.
- Required: every flip happens, and the MUTATE run exits rc = 1. The main run exits rc = 0 iff every load-bearing
  control passes (a failing verdict is not a failing control).

## 7. Files and rules

`cfg499_option_a.py` (driver, tests (1) and (3), verdict), `cfg499_collapse.py` (test (2)), may share a small
`cfg499_lib.py`; outputs `cfg499_option_a.out`, `cfg499_results.json`, `*_MUTATE` variants, `README.md` in plain words.
Symbolic caches go to the scratch directory, never to the repo. nice -n 15, <= 4 threads. Commit locally, only this
folder; do not push. No personal names or home paths in any file.

## Dated correction, 2026-10-08 (appended AFTER the runs; post-hoc, nothing above is changed)

Two clauses of 2a encoded a wrong expectation of how the universal horizon forms in collapse:
- 2a(ii) said C(T) "increases monotonically to 3 sqrt3/4". The computed C(T) DECREASES monotonically to 3 sqrt3/4 from
  above (a leaf with C below the limit cannot cross r = 3/2 at all).
- 2a(iii) said R_s(T) > 3/2 "for every T". The late leaves meet the star surface at R_s* = 1.4582 < 3/2. Those points lie
  on finite-T leaves, which reach infinity, so they are OUTSIDE the UH (the T = infinity leaf); r = 3/2 is where the UH
  sits only asymptotically (the throat of the limiting leaf). The clause tested a fixed radius, not the UH.
The frozen verdict is reported as computed (2a fails on these two clauses, so (2) FAILS and A reads WEAKENED). A
corrected reading is reported SEPARATELY and labelled post-hoc: 2a(ii') C -> 3 sqrt3/4 (from either side) and 2a(iii')
dropped (replaced by the existence of the limiting leaf, i.e. T -> infinity as C -> 3 sqrt3/4, which 2a(iv) already
measures). Under that reading (2) is PARTIAL and A reads NOT DECIDED (open: 2c). The owner chooses which reading stands.

In-code (not frozen) threshold corrected before the final run: 1c(ii) first demanded that every Euler-Lagrange source
density fall as r^-2; the frozen text says only "decays at infinity". The densities carry sqrt(-g) ~ r^2, so r^-1 means a
stress ~ r^-3 and an l = 1 metric response ~ r^-1 (asymptotically flat). The check now demands a decaying density.
