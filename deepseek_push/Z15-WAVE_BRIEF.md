# Z15-WAVE_BRIEF — Lean certificate of the E2(q) degree-2 structure (pre-registered BEFORE any run)

Date: 2026-09-30 (conductor tick, midday EDT). Owner: conductor-run per Z6-Z14
precedent (delegate_task re-confirmed absent at this tick via tool_search: no
matching capability; 0 deepseek lanes running at spawn — the only python3
processes are the separate agent harness PID 95861 and the unrelated
prep_2026/gaia_dr4_prep DR4-READY jobs, untouched per house rule 8).

## Door: E2C1 — certificate-grade status of the E2 quadratic structure

Context (loaded-not-transcribed): E2Q1 (exit 0, commit 2e51b7e46) banked
E2(q) = a + b q + c q^2 EXACTLY (R0 sympy degree set {0,1,2}, coefficients
q-free; K-A max |z_resid| = 0.000; K-B parity max z = 1.59; K-C held-out
z = 0.00) with measured a = 0.616696+-0.000230, b = 0.667788+-0.000560,
c = 0.190069+-0.000119. The Z14 ops note opened this door: "Lean certificate
of the E2 degree-2 structure (linearity algebra; the Z7 LR4b checker trap —
conditional-vs-unconditional — applies)".

## Pre-registered content (conductor derivation, BEFORE any run)

Model context (W3 Amendment 1 / E2Q1): the two-scatter integrand is
(1 + q*a1) * (s1*(W2 + q*A2) + (c00f + q*c0qf)) with W2, A2, c00f, c0qf
q-free. Its q-expansion is EXACTLY
  (s1*W2 + c00f) + q*(a1*(s1*W2 + c00f) + s1*A2 + c0qf) + q^2*(a1*(s1*A2 + c0qf)).
Lean file fable_independent_2026/lean_2026/E2C1_structure.lean, five lemmas:
  L1 e2c1_integrand_q_expansion — the expansion identity, UNCONDITIONAL
     (arbitrary CommRing, no hypotheses — the LR4b trap is respected: nothing
     is certified only under unstated side conditions), proof `ring`.
  L2 e2c1_poly_eval — the integrand equals the evaluation at q of a member
     of R[X] whose three coefficients are exactly the q-free expressions
     above (degree <= 2 form made explicit).
  L3 e2c1_coeff_gt2 — every coefficient of degree k > 2 is 0 (no higher
     terms, machine-checked).
  L4 e2c1_coeff2 — the coefficient of q^2 is EXACTLY a1*(s1*A2 + c0qf),
     q-free by construction (coefficients live in R, q is the polynomial
     variable).
  L5 e2c1_c1_quadratic — the chain assembly: -(1/3 + q/3 + 46q^2/525) +
     (a + b q + c q^2) = (a - 1/3) + (b - 1/3) q + (c - 46/525) q^2 over Q
     (S(q) constants = the LR9-certified values).
HONEST K01 labeling: L1-L4 are the algebra of the model's own integrand
definition (linearity of k1 in q x {K2tot, c0f} in q) — consistency-family,
A/B-class, the same label E2Q1 carried; the lane's payload is (i)
certificate-grade status (unconditional ring identities, zero-sorry), and
(ii) the division of labor that makes the degree EXACTLY 2 (not just <= 2):
nonvanishing of the coefficients is NOT provable over a general ring, so it
is carried at the MEASURED level by E2Q1 — a, b, c all nonzero at
z = 2682 / 1193 / 1601 (a/se, b/se, c/se from E2Q1_results.json fit block).
Exact closed forms of (a, b, c) remain OUT of scope (asinh-class u1-dipole
averages; barred without a pre-registered candidate).

## Pre-registered gates (frozen BEFORE any run)

Lane owns prefix E2C1_ (files E2C1_structure.py/.out/.json,
E2C1_lean_stdout.txt, E2C1_structure.lean).

- G1 (Lean): `lake env lean` on E2C1_structure.lean exits rc 0; stdout has
  zero "error"/"warning: declaration uses 'sorry'" lines; each `#print
  axioms` line lists only a subset of {propext, Classical.choice,
  Quot.sound}. Any fire -> exit 1 (no math tuning; tooling fires recorded).
- G2 (mechanical): E2C1_structure.py re-derives the q-expansion FRESH with
  sympy and checks (a) degree set {0,1,2}, (b) the three coefficient
  expressions equal the pre-registered forms above, (c) the .lean file
  literally contains the L1/L5 law statements (LR9 G2 precedent). Any
  mismatch -> exit 1.
- G3 (chain): E2Q1_results.json loaded-not-transcribed: exit == 0 AND
  r0.maxdeg == 2 AND r0.qfree == True. Mismatch -> exit 1.
- Exit 0 iff G1 + G2 + G3 complete with no fire. Any execution failure is an
  honest exit 1 or a recorded scope note; constants never tuned.

## Deliverables
E2C1_structure.py / .out / E2C1_results.json (exit inside), E2C1_lean_stdout.txt,
E2C1_structure.lean; register row appended by the conductor on landing;
commit work+math only (house rule 6; raw data untouched; astra_spawn_ideas and
tmp probes untouched, house rule 8).

## Amendment 1 (conductor, run-1 honest fire, preserved verbatim)
Run-1 crashed with two tooling bugs, math untouched (the R0 content had already
printed PASS-equivalent values before the crash): (a) degree-set comparison
fired because univariate sp.Poly.terms() monoms are 1-tuples ([(0,),(1,),(2,)]
vs [0,1,2] — the same class as E2Q1 run-1's monom-tuple TypeError); (b) crash
`TypeError: cannot determine truth value of Relational` in sorted(qf) —
real-assumption sympy Symbols order via Relational, not bool. Fixed forward:
m[0][0] indexing and sorted(map(str, qf)). The spurious G2 FIRE line
"degree set != {0,1,2}" is a FALSE fire from the comparison bug, recorded here
verbatim: G2: fresh q-degree set: [(0,), (1,), (2,)] / G2 FIRE: degree set !=
{0,1,2} / G2: coefficient C0 ... dev 0 / C1 dev 0 / C2 dev 0 / traceback
relational.py __bool__ at the qf sort line.

## Amendment 2 (conductor, runs 2-3 honest fires, preserved verbatim)
Run-2 G1 fires (stdout saved E2C1_lean_stdout_run2.txt): L2 `simp only` left
`Polynomial.eval q Polynomial.X` un-reduced (eval_X missing from the set) so
the trailing `ring` could not close; L3/L4's inline type-ascribed polynomial
`( ... : R[X]).coeff k` broke elaboration ("failed to synthesize HAdd
(Polynomial R) (Polynomial R) R[X]", sorryAx leaked). Fix: named def e2c1P +
eval_X added; checker's sorry-fire corrected to the warning line + axiom
subset only (run-2's sorryAx lines were already caught by the subset check —
the raw-substring grep double-fired). Run-3 G1 fires (stdout saved
E2C1_lean_stdout_run3.txt): the e2c1P def needs `noncomputable` (R[X] addition
on a general CommRing is noncomputable); full-strength `simp` pushed C through
the arithmetic (C a1 * (C s1 * C W2 + ...) shapes) and left unsolved coeff
goals on L3/L4. Fix: noncomputable def + `simp only` controlled lemma sets
(coeff_add, coeff_C, coeff_C_mul, coeff_X_pow, coeff_X) + trailing default
simp. Math (the five law statements) never changed across runs 1-4.

## Amendment 3 (conductor, runs 4-5)
Run-4 G1 fire: L3 clean, L4 unsolved goal (a1*(s1*W2+c00f)+s1*A2+c0qf)*X.coeff 2
= 0 — the run-3 patch omitted coeff_X from L4's simp only (L3 had it). Fixed.
Run-5 (final): lake rc 0, zero sorry, zero error, all five axiom lines subsets
of {propext, Classical.choice, Quot.sound}; G2 fresh sympy dev 0 on all three
coefficients, q-free True, all 8 lean statement patterns present; G3 loaded
E2Q1 exit 0 / maxdeg 2 / qfree True. E2C1 ALL PASS, exit 0.
