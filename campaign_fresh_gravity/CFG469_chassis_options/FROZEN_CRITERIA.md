# CFG469 FROZEN CRITERIA: three ways out of CFG467's alpha_c tension, tested

Frozen 2026-10-08, before any CFG469 script exists. Nothing below may be edited after the commit that adds this file;
corrections go in a dated section appended at the end.

Theory plus offline numerics only; no downloads. Read-only on every lane named here. kappa = 1/2 is FITTED and plays no
role (a0 enters none of the computations below; the two footings 9.36e-11 / 1.13e-10 give identical results, and this
is printed, not assumed silently). No dark-matter particle is added; the cold fluid's mass is still required. Nothing
here says "theory closed".

## 0. The question, and disclosure

CFG467 (a53d0f430) found that no khronon coupling alpha_c passes all twelve chassis gates under strict readings:
alpha_c <= 0 is excluded by G1/G2/G4/G5 (three proofs), alpha_c > 0 by strict black-hole regularity (CFG318/CFG319:
4 constants against 5 conditions for every alpha_c > 0, test-khronon limit; a fully regular moving black hole exists
only at alpha_c = 0). The owner asked to "test all options or find another option that actually works". Three options:

- **(A) Lenient BH + radiative hierarchy.** Accept black holes regular outside the universal horizon (UH), i.e. CFG319's
  option C, and test whether that reading is physically consistent (causal disconnection including the instantaneous
  mode, finiteness, UH thermodynamics), then compute the open alpha_c window jointly with CFG320's hierarchy.
- **(B) UV constant M_*.** Add the lowest-order Horava-type higher-derivative term (one coefficient, set by M_*) and test
  whether it supplies the missing fifth boundary condition / regularises the moving-BH UH at alpha_c > 0, and whether
  the needed M_* is compatible with CFG320's bound and the Lorentz-violation bounds on the record.
- **(C) Retire the chassis.** Write candidate B as a recipe without the relativistic chassis: every declared constant or
  input, and which committed gates become untested.

**Not blind.** Read before this file: CFG467 (README, criteria, JSON), CFG318/CFG319/CFG320 (READMEs, criteria, JSONs,
CFG319's script), the failure ledger (LEDGER_failure_mechanisms_2026-10-08), RECIPE_GATE_AUDIT_2026-10-03, GATES.md,
STANDING_2026-09-29.md, WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md, the status board, the extra_crispy README (XC1/XC2).
No CFG469 computation has been run. Expectations written down now so they cannot be tuned later:
- (A) causal disconnection is expected to hold (the UH is the T = +infinity leaf); the curvature is expected to diverge
  pointwise but integrably at the UH.
- (B) a heuristic from the dispersion relations, not a computation: Horava terms are higher SPATIAL derivatives on the
  leaves, and at the UH the leaf is the r = r_UH surface, so the radial (singular) direction is the khronon's time
  direction there; spatial UV terms are therefore expected NOT to touch the UH exponents, and the over-determination is
  expected to persist. This expectation is exactly what (B) tests; the rule below does not depend on it.
- (C) no current candidate-B pass is expected to depend on a chassis-only ingredient.

Parallel lanes exist (e.g. CFG484, a search for another chassis). They are not read or used here.

## 1. Inputs (read from committed files, never refitted)

- CFG319 `cfg319_moving_bh_results.json`: per-point UH roots (`rootsU`), y1 (`YU1`), r_UH, c_S, mode classes, option-C
  admissibility, `ext_diff_C_Cp`; the symbolic `S22`, `dK_ops`, `daa_ops`.
- CFG320 `cfg320_radiative_stability_results.json`: Lambda_HL_max = 9.87e8 GeV, Lambda_sc per grid point, the c_2 grid,
  M_P = 2.435e18 GeV.
- CFG467 `cfg467_results.json`: the lenient intersection I_len and the per-c_2 G11 strict edge.
- L340 window: alpha_c in [9.624e-14, 3.2e-9], c_2 in [7.2888e-3, 0.0667]. W5 = CFG319's five window points.
- The stealth khronon (alpha -> 0, CFG319 C1 / CFG318 C1): W = C/r^2, C = 3 sqrt3/4, Y^2 = 1 - 2/r + W^2, r_UH = 3/2,
  y1 = 2 sqrt2/3, W0 = 1/sqrt3 (M = 1, ingoing EF). Used where a closed-form background is needed; the W5 backgrounds
  differ from it only inside the O(1/c_S) boundary layer, and per-point UH data (y1, r_UH) are read from CFG319.

## 2. Option A: tests (all computed; frozen thresholds)

**A1 causal disconnection** (load-bearing for A).
- A1a (sympy) lim_{x->0+} x H'(r_UH + x) = -1/(y1 W0) != 0 for H' = -1/(Y(Y+W)): the khronon T -> +infinity at the UH at
  every finite v, from outside and from inside. Pass: the limit is finite and non-zero, both sides.
- A1b (sympy) the global time function tau = -exp(-kappa_U T), kappa_U = y1 W0, extends across the UH with
  d tau / dr finite and non-zero and g^{mn} d_m tau d_n tau < 0 there (a timelike normal): UH = {tau = 0}, exterior
  tau < 0, interior tau > 0. Pass: both conditions hold.
- A1c (numeric, "fastest signal reach") from start points on or inside the UH, r0 in {1.0, 1.2, 1.4, 1.49, 1.4999, 1.5},
  v0 in {-10, 0, 10}: follow (i) the khronon leaf through the point (infinite speed, d tau = 0) outward and (ii) outgoing
  radial characteristics with speeds c in {1, 444, 7.9e5, 1e12} relative to the khronon frame. Record the largest r
  reached at finite v (integration stops at |v| = 1e4 or r = 1e4). Pass: max r <= r_UH + 1e-9 for every start point and
  speed. Control K5: from exterior start points the same code must reach r = 1e4 along the leaf.
- A1d (O(v) persistence) the option-C perturbation of tau scales as x^(1 + s+), s+ from CFG319 per W5 point. Pass:
  1 + s+ > 1 (tau stays C^1 with a continuous, non-vanishing gradient, so it remains a time function for small v).
  Control: the C' option (s-) must give 1 + s- < 0 (tau unbounded: that option destroys the foliation) and be flagged.
- A1e (free data) CFG319's option C has 4 constants against 4 conditions, so the s+ amplitude is an output: zero free
  parameters live on the UH. Pass: the committed count reproduces (0 free). The committed C-vs-C' exterior difference at
  6M is printed as a reading (a rule-level static difference, not a signal).
- A1 passes iff A1a-A1e pass.

**A2 finiteness** (load-bearing for A under reading W), at every W5 point with CFG319's s+:
- A2a exterior regular: CFG319 option C admissible at all five points, modes -1 and 0 regular, s+ weak (committed).
- A2b O(v) stress / Ricci exponent p1 = s+ - 1 > -1 (integrable over proper volume).
- A2c quadratic invariants at O(v^2) (Kretschmann, R_mn R^mn): p2 = 2 (s+ - 1) > -1, i.e. s+ > 1/2.
- A2d Tipler and Krolak integrals along the radial free-fall geodesic from rest at infinity (dr/dtau = -sqrt(2/r),
  non-zero at r_UH, so the crossing is transversal): integral_0 x^p1 dx and its double integral are finite (numeric
  quadrature to 1e-12 tolerance). Control K6: the s- mode (p = s- - 1) must give a divergent Krolak integral.
- A2e metric class: h ~ x^(1 + s+) makes the metric C^{1, s+}; Christoffel symbols are Hoelder; a transversal crossing
  makes x monotone along the geodesic, so the geodesic is unique (Caratheodory). Pass: 0 < s+ < 1 and the crossing
  speed is non-zero.
- A2f (ARG, reported, not load-bearing) Killing-energy flux: the O(v) part integrates cos(theta) over the sphere to 0
  (sympy); the O(v^2) part is r-independent by conservation, so it equals its value at infinity, which vanishes for
  stationary decaying fields; this needs the O(v^2) fields to exist up to the UH (not computed).
- Under reading S, A2 reads FAIL by definition (pointwise divergence). Reported.

**A3 UH thermodynamics** (load-bearing for A):
- A3a (sympy) for L = -lambda K^2 + alpha a.a the momentum dL/d(grad_m u_n) contains only g, u, K and a (no second
  derivatives of u), so the Noether-charge density and the symplectic current contain u, K, a and their variations
  only; their option-C perturbations scale as x^(s+ + 1) (dK), x^s+ (da, du), all with exponent >= 0. Pass: all
  exponents >= 0 at every W5 point.
- A3b kappa_UH = a.chi-type quantity on the UH: its O(v) change ~ x^s+ -> 0 at the UH, and it carries cos(theta), whose
  sphere average vanishes. Pass: both.
- A3c the O(v) first law is trivial: an l = 1 perturbation gives delta A_UH = 0 and delta M = 0 (sympy, integral of
  cos(theta)). Pass: both zero.
- The UH temperature (Berglund-Bhattacharyya-Mattingly 2012/13 and later disputes) is literature recalled from memory,
  PROVISIONAL, not read, not scored.

**A4 joint window**:
- A4-0, reading W with no hierarchy (0 new constants): alpha_c in [9.624e-14, min(alpha_rs(c_2), 3.2e-9)] where
  Lambda_sc(alpha_rs, c_2) = Lambda_HL_max; Lambda_sc = sqrt(alpha) M_P c_s^(-1/2), c_s^2 = c_2 (2 - alpha)/(alpha
  (2 + 3 c_2)). Recomputed at all 9 c_2. Control K9: alpha_rs reproduces CFG467's 5.80e-14 / 1.18e-13 (c_2 =
  7.29e-3 / 0.0667) to 1e-2 relative, and the non-empty set is c_2 >= 0.038 (CFG320's 3 points).
- A4-H, reading W + Pospelov-Shang hierarchy (+1 UV scale, M_* <= min(Lambda_HL_max, Lambda_sc)): CFG467's I_len,
  read and re-intersected; control: equals [9.624e-14, 3.2e-9] at every c_2.
- A4-UV consistency: the hierarchy's UV sector must not destroy option C, i.e. option B's lenient count (section 3) for
  the healthy UV operator must have Delta_len <= 0. Pass required for A4-H.
- A4 passes iff A4-H is non-empty at >= 1 c_2 and A4-UV holds.

**Verdict A.**
- FAILS if A1, A2, A3 or A4 fails (the first failing test is named).
- Otherwise WORKS-CONDITIONAL, with conditions named: (i) the owner adopts reading W; (ii) for the full window, the
  hierarchy (+1 UV scale M_* <= 9.9e8 GeV), or 0 new constants on the c_2 >= 0.038 sliver; (iii) the inherited scope
  conditions (CFG319's test-khronon limit and collapse formation; CFG467's tested-range edges).
- WORKS is not available to A: its G12 passes only under reading W, which is itself the condition.

## 3. Option B: tests

**B0 the operators (frozen).** Lowest-order (dimension-4, T-even, quadratic in the khronon perturbation) leaf-covariant
terms that survive in the test-khronon limit, each with ONE coefficient fixed by M_* (epsilon = 1/(M_* r_g)^2, r_g = 1):
- arm O_A (Horava "A-type" acceleration term): Delta L = + alpha_c epsilon (D_m a^m)^2, with D_m a^m = grad_m a^m - a.a;
- arm O_K (gradient of the expansion): Delta L = - c_2 epsilon h^{mn} d_m K d_n K, h^{mn} = g^{mn} + u^m u^n.
Signs are the healthy ones (B1). Both add +1 constant (M_*). Leaf-curvature ("B-type") terms R^2, R_ij R^ij of the
leaves are O(perturbation^4) on the test-khronon background in flat space (control K4) and are out of scope, as is
the metric response (CFG319's scope).

**B1 flat-space dispersion** (sympy, decoupling limit T = t + pi): derive omega^2(k) for each arm. Expected closed
forms: O_A omega^2 = (c_2/alpha) k^2/(1 + epsilon k^2); O_K omega^2 = (c_2/alpha) k^2 (1 + epsilon k^2). Healthy iff the
kinetic coefficient is positive and omega^2 > 0 for all k > 0. A mismatch with the closed form is a derivation error
(load-bearing). Report the UV scaling z.

**B2 the O(v) moving-BH problem with the UV term** (sympy derivation; test-khronon limit on Schwarzschild, ingoing EF,
T = v + H(r) + v F(r) cos(theta), as CFG319):
- the angle-integrated quadratic Lagrangian L2 = sum S_ij F^(i) F^(j), i, j <= 3; Euler-Lagrange equation of order 6.
- Control K1 (load-bearing): at epsilon = 0 the derivation reproduces CFG319's committed S22, dK_ops and daa_ops exactly.
- Singular points: zeros of the leading coefficient on (r_UH, infinity); its factorisation (is r_S still singular?).
- Local solutions at the UH (Newton polygon / Frobenius, exact series on the stealth background; per-point (y1, W0)
  check where the exponents depend on them) and at infinity (power laws and exponential modes; for oscillatory or
  exponential modes the self-adjoint WKB transport |amplitude| ~ (a6 k^5)^(-1/2) gives the amplitude power).
- Control K3 (load-bearing): at epsilon = 0 the UH exponents are {-1, 0, s+, s-} with s^2 + s - 1 = 0 on the stealth
  background, and the per-point exponents reproduce CFG319's rootsU to 1e-8 using CFG319's y1 and r_UH.

**Classification (frozen).**
- At the UH (x = r - r_UH -> 0+): regular iff a real Frobenius exponent s in {-1, 0} or s >= 6, or a super-exponentially
  flat essential mode (exp(-c x^-rho), Re c > 0); weak iff not regular, dK, d(a.a) and the UV scalar perturbation are
  bounded and their radial gradients integrable (power > -1, using real parts and the WKB amplitude); strong otherwise.
  Oscillatory modes are classified by the same powers.
- At infinity: admissible iff F'' and F''' -> 0 (dK, da and their gradients decay), or the mode is the boost r or the
  constant; r^3 and growing exponentials are inadmissible.
- At r_S: if it is a singular point of the order-6 equation, non-analytic (logarithmic) solutions are conditions; if it
  is a regular point, it imposes none.

**Count.** N_const = order of the equation (6 with the UV term, 4 without). N_cond = (inadmissible modes at infinity) + 1
(the coefficient of r = -1) + (conditions at r_S) + (non-regular modes at the UH: strict) or (strong modes at the UH:
lenient). Delta_strict = N_cond_strict - N_const, Delta_len likewise.
- Control K2 (load-bearing): applied to the IR operator alone, the same counting code gives CFG319's numbers: 4 constants,
  5 conditions (Delta_strict = +1), and option C determined (Delta_len = 0).

**B3 (only if Delta_strict <= 0 for an arm).** If the count closes only because r_S stops being singular, the
UH-regular solution must excite the IR logarithm at r_S (CFG319: no IR solution is regular at both r_S and the UH), with
a non-zero amplitude c_log, smoothed over a UV layer of width delta_S = |a6/a4'|^(1/3) at r_S. Report delta_S at the
physical M_* = Lambda_HL_max for M = 10 Msun and M87* (6.5e9 Msun), and the linearity threshold |c_log| <= delta_S/v
with v = 1e-3; c_log is not computed here, so it becomes a named condition. Also check that every admitted UV mode has
local wavenumber <= Lambda_sc.

**B4 the M_* band.** Upper edge = min(Lambda_HL_max, Lambda_sc(point)) at each CFG320 grid point (committed numbers).
Lower edge: none on the record (reading: sub-mm gravity tests, recalled ~1e-12 GeV, PROVISIONAL). Band non-empty iff
upper > lower at >= 1 point.

**Verdict B (per arm; B overall = the best arm).**
- FAILS if the operator is unhealthy (B1), or Delta_strict > 0 (gate: strict BH regularity, G12 of CFG467; the UV term
  does not supply the fifth condition), or the band is empty (gate named).
- WORKS-CONDITIONAL if Delta_strict <= 0 and the band is non-empty; conditions named: B3's, plus existence beyond the
  count (the order-6 boundary-value problem is not solved here), plus the metric coupling.
- WORKS is not reachable in this lane (no boundary-value solution at the physical M_*). Constant count: +1 (M_*), possibly
  the same M_* as CFG320's hierarchy.

## 4. Option C: the recipe without the chassis

- C1 inventory: every declared constant/input of candidate B with its status (FITTED / DATA / DECLARED FUNCTION /
  DECLARED RULE / NUISANCE) and its source file. Load-bearing control K7a: for every row the script finds the quoted
  source string in the cited committed file (provenance), else the row fails.
- C2 the gates that become UNTESTED (not passed): every status-board tile and RECIPE_GATE_AUDIT / GATES.md row whose
  committed verdict was computed on the chassis.
- C3 dependency audit: for every candidate-B row currently PASS or CONDITIONAL on the board or in GATES.md sections 1-4,
  whether it uses a chassis-only ingredient. Leads that use the chassis (not passes) are listed as costs.
- Control K7b (load-bearing): injecting one fake chassis dependency into a B pass must turn the C verdict to FAILS.
- **Verdict C:** FAILS if C3 finds a current B pass that depends on a chassis-only ingredient with no recipe replacement
  (the row is named). Otherwise WORKS-CONDITIONAL, condition: the C2 gates are untested and B is a recipe, not a theory
  (the tension is bypassed, not resolved). WORKS is not available (untested is not passed).

## 5. Controls (load-bearing unless marked)

K1 (CFG319 S22, dK_ops, daa_ops reproduced at epsilon = 0), K2 (IR count 4 vs 5; option C determined), K3 (IR UH
exponents, stealth closed form and per-point rootsU to 1e-8), K4 (flat dispersions equal the closed forms; leaf
curvature O(pi^2)), K5 (A1c reach code: exterior start points reach r = 1e4 along the leaf), K6 (the s- mode is flagged
strong / its Krolak integral diverges), K7a/K7b (C provenance; fake-dependency injection gives FAILS), K8 (a0 enters no
computation: identical results under both footing labels), K9 (alpha_rs and I_len reproduce CFG467 / CFG320).

## 6. MUTATE (`CFG469_MUTATE=1`; outputs `*_MUTATE.out`, `*_results_MUTATE.json`)

- (A) the instantaneous mode is made to propagate on the hypersurfaces v - r = const (spacelike everywhere and regular
  across the UH) instead of the khronon leaves. A1c must then report a reach of r = 1e4 from inside the UH, A1 must FAIL
  and the A verdict must read FAILS.
- (B) M_* = 1e12 GeV, outside the band (above Lambda_HL_max at every point). B4 must FAIL and the B verdict must read
  FAILS (gate: G11 radiative stability / strong coupling).
- Required: both flips happen, and the run exits rc = 1. The main run must exit rc = 0 when every load-bearing control
  passes (a failing verdict is not a failing control).

## 7. Files

`cfg469_chassis_options.py` (driver; option A, B4, C, verdicts), `cfg469_uv_bh.py` (option B derivation and local
analysis; may cache intermediate symbolic results in the scratch directory, never in the repo),
`cfg469_chassis_options.out`, `cfg469_results.json`, `cfg469_chassis_options_MUTATE.out`, `cfg469_results_MUTATE.json`,
`README.md` with the options table and a recommendation. Commit locally; do not push.
