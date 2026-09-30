# Z14-WAVE_BRIEF — E2(q) quadratic-structure door (pre-registered BEFORE any run)

Date: 2026-09-30 (conductor tick, morning EDT). Owner: conductor-run per Z6-Z13
precedent (delegate_task re-confirmed absent at this tick; 0 deepseek lanes
running at spawn — the only python3 process, PID 95861, is a separate agent
harness's background task, untouched per house rule 8).

## Door: E2Q1 — exact structure of the two-scatter leg E2(q)

Context (all loaded, never transcribed): W3_results.json (exit 0, commit
f734a03f9) banked c1(q) = -S(q) + E2(q) with S(q) = 1/3 + q/3 + 46q^2/525
(LR9-certified) and E2 MEASURED at q in {0,1,3,6,10} = 0.6173/1.4756/4.3328/
11.4701/26.3095 (+- 0.0003/0.0008/0.0023/0.0062/0.0145). The Z13 ops note
opened the door: E2 exact reduction, ONLY with a pre-registered closed-form
candidate.

## Pre-registered candidate (conductor derivation, BEFORE any run)

From the engine-exact integrand (W3 docstring, Amendment 1, loaded-not-
transcribed): E2(q) = E[ int_0^W ds1 k1(s1) E_{u1}[ int_0^{W2} ds2 k2(s2)(s1+s2) ] ]
with k1(s1) = 1 + q a1(s1), a1 = r^2 + 2 z s1 + s1^2 (z = p.u), k2(s2) = 1 +
q a2(s2), a2 = r12 + 2 pd2 s2 + s2^2, and W2 = -pd2 + sqrt(pd2^2 - r12 + 1)
PURELY GEOMETRIC (q-independent). Since K2tot = int k2 = W2 + q A2 and
c0f = int s2 k2 = c00f + q c0qf with A2, c0qf q-free, the q-expansion of the
integrand is (1 + q a1) * [s1 (W2 + q A2) + (c00f + q c0qf)] — a polynomial of
degree EXACTLY 2 in q with q-free coefficients.

CANDIDATE LAW (consistency-family structure + measured payload):
  E2(q) = a + b q + c q^2   EXACTLY (no higher terms),
where a, b, c are the q-free integrals above. Honest K01 labeling: the degree-2
structure FOLLOWS from the model's own rate definition k(s) = 1 + q*dist^2
(linearity of k1 in q and of {K2tot, c0f} in q) — this leg is model-input
restatement (A/B-class), recorded as such; the MEASURED coefficients (a, b, c)
and the overdetermined held-out test are the lane's physical payload. The
exact closed form of a, b, c is recorded OUT of scope here: the u1-dipole
average of W2 = -pd2 + sqrt(pd2^2 + beta^2) carries asinh-type functions
(NOT the LR3/LR7 rational family); noted as successor-door scope only.

Conductor pre-audit on STORED data only (no new run): overdetermined quadratic
fit of W3's five stored E2 points (1/se^2 weights) gives residuals z =
-0.001/0.003/-0.001/-0.006/0.005 (max 0.01) and LOO held-out z <= 0.01 at all
five q. This is why the door is registered; it is NOT the verdict.

## Pre-registered gates (frozen BEFORE any run; all numbers must exist on disk)

Lane owns prefix E2Q_ (files E2Q1_*.py/.out/.json). Estimator: W3's M2b
structure, FRESH seed 20260930e2 (never a 20260929* seed), n = 8e6 events x 8
dipole samples (2x W3's events, same dipole budget), chunked 1e6; E2(q)
evaluated INDEPENDENTLY at each of the five q from raw k1q/K2tot/c0f (the
quadratic form is NOT baked into the estimator — the fit tests the structure).

- R0: sympy exact expansion of the symbolic integrand in q: degree <= 2 AND
  q-freeness of W2/A2/c0qf coefficients asserted symbolically. Degree > 2 or
  any q-dependence found -> exit 1 (candidate REFUTED before the MC).
- K-A (structure test, primary): 1/se^2-weighted quadratic fit on all five
  fresh MC points; any |z_resid| > 3 -> E2 quadratic structure REFUTED, exit 1.
- K-B (parity vs W3 stored, per q): combined |z| = |m_fresh - m_W3| /
  sqrt(se_fresh^2 + se_W3^2) > 3 at any q -> exit 1.
- K-C (held-out): fit on q in {0,1,3,6}, predict q=10; |z| > 3 -> exit 1.
  LOO ablation on all five recorded (no gate).
- Exit 0 iff R0 + K-A + K-B + K-C complete with no fire. Any execution failure
  is an honest exit 1 or documented scope note; constants never tuned.

## Deliverables
E2Q1_quad_structure.py / .out (all run blocks verbatim) / E2Q1_results.json
(exit code inside); register row appended by the conductor on landing;
commit work+math only (house rule 6; raw data untouched; astra_spawn_ideas and
tmp probes untouched, house rule 8).
