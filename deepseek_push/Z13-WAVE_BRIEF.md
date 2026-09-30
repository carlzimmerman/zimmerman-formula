# Z13-WAVE BRIEF (conductor, 2026-09-30 tick ~morning EDT - pre-registered BEFORE any run)

Spawn trigger: 1 running python3 process (PID 95861) identified via lsof as a
separate agent harness's background task (claude-501 task output dir) with cwd
= repo root - NOT a deepseek lane; untouched per house rule 8. 0 deepseek
lanes running. delegate_task re-confirmed absent this tick (tool_search: no
match) - conductor-run lanes per Z6-Z12 precedent. Open doors from the Z12
ops note: (1) Lean certificate of the W3 survival law S(q); (2) the q=10
scope-tension dense-grid MC; (3) E2 exact reduction (requires a pre-registered
closed-form candidate - NOT registered this tick, no candidate exists);
(4) OA1 WG high-z (data-gated, eRASS:3 WG products not on disk - no padding
lane). Wave size 2 = every runnable registered door.

## Door LR9 (registered): Lean certificates of the W3 survival law
S(q) = 1/3 + (1/3) q + (46/525) q^2

Background (on-disk): W3 (exit 0) banked the survival correction
S(q) = C00 + q C01 + q^2 C02 = 1/3 + (1/3) q + (46/525) q^2, confirmed on
three independent evaluations (sympy definite integral, mp dps=40, GL(500)) +
MC cross-check (z = 0.79/0.85/0.89 at q=0/1/3, n=2e7). Its rationals are NOT
yet certificate-grade. The W3 chain (W3_c1_measurement.py M2a): with
s = sqrt(1-x^2), Wg = s(1-w), z = s w, r2 = x^2 + s^2 w^2,
A = r2 + 2 z v + v^2, B = r2 v + z v^2 + v^3/3, integrand I(v) = v (1 + q A)(v + q B),
  C_k = (3/2) int_{-1}^{1} int_0^1 x s [I(v) expanded, coeff of q^k, integrated
        v from 0 to Wg] dw dx.
After the w-integral over [-1,1] (odd powers vanish) each C_k is a finite
rational assembly of outer 1D cores int_0^1 x (1-x^2)^m sqrt(1-x^2) dx
= 1/(2m+3) (T_k-primitive class, LR7 precedent: base_A m=1 = 1/5, base_C m=2
= 1/7, base_E m=3 = 1/9 are already zero-sorry in LR7_w1_moments.lean).

Lane LR9_sq_law (owner: conductor; prefix LR9_*):
- R0 ALGEBRA AUDIT (pre-registered gate 1e-12 rel): FRESH sympy derivation
  of C00, C01, C02 by a DIFFERENT method than W3's sp.integrate (v,a,s)-
  antiderivative: monomial-basis assembly (Poly arithmetic + explicit
  int_0^{Wg} v^j dv = Wg^{j+1}/(j+1)), independent variable ordering; must
  reproduce 1/3, 1/3, 46/525 exactly AND yield the core-assembly coefficients
  (c_m per C_k) for the Lean leg. Two independent quadratures (mp dps=40 via
  GL(300) nodes; float64 GL(600)xGL(140)) of the (x,w) integral; MC of the
  full geometric reduction with a FRESH seed (not W3's 202609293). Any exact
  mismatch, quadrature dev > 1e-12 rel, or MC |z| > 5 -> exit 1.
- G1 LEAN (fable_independent_2026/lean_2026/LR9_sq_law.lean): generic core
  theorem core_k : int_0^1 x (1-x^2)^k sqrt(1-x^2) dx = 1/(2k+3) for the
  needed k (via the LR7 T_deriv primitive), then assembly theorems
  s00_law / s01_law / s02_law stating C00 = 1/3, C01 = 1/3, C02 = 46/525 as
  exact rational combinations of the cores; lake rc 0, ZERO sorry, axioms
  subset {propext, Classical.choice, Quot.sound}. FAIL after honest attempts
  -> exit 1.
- G2 MECHANICAL: sympy re-derivation of the assembly coefficients must match
  the Lean statement's constants exactly. Mismatch -> exit 1.
Honest scope (labeled in the Lean header, LR3b/LR4c/LR7/LR8 precedent): the
1D cores and the rational assembly are CERTIFIED; the geometric reduction leg
(v-integration to the wall Wg + cylindrical density (3/2) x + odd-w
cancellation) is numeric-audited (R0), not probability-space-certified.
Kill conditions pre-registered: R0 exact mismatch / quadrature > 1e-12 / MC
|z| > 5 / G1 compile-sorry-axioms fail / G2 mismatch -> exit 1.

## Door W4 (registered): the q=10 scope tension - dedicated dense-grid MC

Background (on-disk): W3 (exit 0) recorded the q=10 SCOPE tension: predicted
c1(10) = -S(10) + E2(10) = -12.428571 + 26.309547 = +13.880976 vs W3's
anchored measured c1(10) = -2.6495 +- 1.2212 (MC7's own LOO-unstable,
quadratic-selected point). Whether this is MC7 extrapolation bias at the
quadratic-selected q or real structure beyond O(tau0) is OPEN.

Lane W4_q10_dense (owner: conductor; prefix W4_*):
- Budget (fixed before any run): q = 10 ONLY; tau0 grid 6 values
  {1e-3, 6e-4, 4e-4, 2.5e-4, 1.5e-4, 1e-4} (small-tau0 focused so O(tau0^2)
  curvature is leverage-dead); n = 8e6 x 5 reps/cell (n_eff 4e7/cell, 2x
  MC7's), seeds 8101.., single pass, no re-tuning. Engine: J02 simulate
  (loaded, not transcribed).
- M1: anchored quadratic fit c0 - c00_exact(10) = c1 tau0 + c2 tau0^2 on all
  6 points, c00_exact(10) = 2/5 + (8/35)*10 = 95/35 = 2.685714 ANCHORED
  (W2/LR8-certified). c1(10) = measured slope + propagated SE; LOO ablation
  recorded.
- M2: parity vs MC7's fresh tau0=1e-3 q=10 stored point (loaded from
  MC7_results.json, not transcribed): |z| <= 3 combined SE, else exit 1.
- M3 ADJUDICATION (pre-registered branches):
  (a) |c1_meas(10) - 13.880976| <= 3 sqrt(se^2 + se_pred^2) with se_pred from
      E2's MC SE (0.0145): the W3 structural decomposition HOLDS at q=10 ->
      the W3 tension was MC7 extrapolation bias at the quadratic-selected
      point; MC7's q=10 quadratic-selection recorded as bias-limited.
  (b) c1_meas(10) <= 0 at >= 3 combined SE: REAL structure beyond
      c1 = -S + E2 at q=10 -> register successor door W5 (exact c2(q) /
      higher-cumulant leg) in the register ops note.
  (c) otherwise: UNRESOLVED at this power - recorded, no new door claimed.
  Any branch is an honest exit-0 outcome EXCEPT execution failure or M2 fire.
Kill conditions pre-registered: M2 parity fire -> exit 1; execution failure
-> exit 1. No fabrication: every number from MC7_results.json (loaded) or a
fresh run with exit code on disk.

House rules 1-10 (LOOP_CONDUCTOR.md) bind both lanes. Raw data stays
untracked; astra_spawn_ideas + tmp probes untouched (house rule 8); no
commits by leaf lanes (conductor commits at tick end).
