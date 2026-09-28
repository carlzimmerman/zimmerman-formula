# AS045 — Heat filter operator domain of definition (seed text as dispatched)

**STATUS NOTE (mandatory record):** The dispatched file
`deepseek_push/astra_spawn_ideas/AS045_heat_filter_operator_domain_of_definition.md`
does NOT exist in the repository. Verified by: `search_files` (files target, patterns
`AS045*`, `heat_filter*`, `*domain_of_definition*`), content searches for
"domain of definition", "Fourier multiplier", "galactic measure", "Schwartz", and a
filesystem find for `*heat_filter_operator*` / `*domain_of_definition*`. The repo's
AS045 slot is the DIFFERENT task `AS045_newtonian_tail_ordering_of_the_three_kernels.md`
(sha256 2f7f4fa561e1625a234f4210e10c8bcd64a8d98f869d88b553e094f45187372f), registered in
`claims/AS045.json` (owner hermes-orchestrator, worker sa-1-81d7a644, state running).
That slot was NOT touched, and no claims file was created or modified — identical to the
documented AS043 dispatch precedent. This file reproduces, verbatim, the seed text from
the actual dispatch message; `task_sha256` in result.json is the SHA-256 of THIS file.

---

## Dispatched seed text (verbatim from the dispatch envelope)

Task AS045: HEAT FILTER OPERATOR DOMAIN OF DEFINITION — the operative MONO branch uses heat
filter S = exp[(xi^2/2) Delta]; audit the operator's domain of definition on the galactic
scale: as a Fourier multiplier exp[-(xi^2/2)|k|^2] it is analytic on which function classes
on Euclidean vs the galactic measure (specify), whether S and S* are bounded/unbounded in
L2, and the minimum smoothness for the composition S* div[(nu_mono-1) grad S u] to make
sense distributionally. Both footings: 9.3619e-11 and 1.1279e-10 m/s^2. Numerics:
G=6.67430e-11, c=299792458 (SI). G_N/G_bare/G_cosmo SEPARATE. Branches distinct: Q, RAR,
MU2, EXP, MONO (criterion B).

## Envelope execution rules (verbatim)

EXECUTION RULES: follow the task's numbered steps in order; derive every intermediate
factor/sign/unit; run the negative control (capable of failing). Bounded prototype: <=120 s,
<=512 MB, 1 thread — record ACTUALLY enforced bounds. Proof-only results must NOT fabricate
computational evidence — actual residuals, not booleans.

DELIVERABLES: unique run dir deepseek_push/astra_spawn_ideas/results/AS045/<unique_run_id>/
containing derivation.md, result.json (ALL schema-v2 fields; task_sha256; worker = YOUR
ACTUAL identity; execution_status; outcome enum; exact_claim; framework_cell;
new_assumptions; input_sha256; artifacts_sha256; commands; execution_bounds; checks;
tested_domain; failed_attempts; limitations; next_unresolved_implication;
suggested_followup; acceptance_state='unreviewed'; ancestry=null; first_principles_inputs;
closure_implication; child_proposals; closure_candidate=null), plus code and raw outputs.

LEAN CERTIFICATE: if an algebraic identity is worth certifying (e.g. the Fourier multiplier
action on exp(ikx)), write a self-contained Lean 4 certificate in the run dir and verify:
cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean. Hard bar: zero sorry,
axioms subseteq {propext, Classical.choice, Quot.sound}. COMPILE HOST ONLY: never write
files into fable_independent_2026/lean_2026.

DO NOT: modify any task spec, contract, manifest, ledger, or claim file; touch other
workers' results; edit shared status files; claim anything ran without executing it; create
claims/ files.

## Framework base (from FRAMEWORK_CONTRACT.md, mandatory in this calculation)

- a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED as input (not derived here).
- Operative branch MONO with criterion B; Q, RAR, MU2, EXP kept distinct.
- Operative filtered equation (FRIED_CHICKEN_SPEC.md requirement 1, amended 2026-09-26):
  Delta u = 4 pi G rho_b ;  Delta Phi = 4 pi G rho_b + S* div[(nu_mono(|grad S u|/a0)-1) grad S u] ;
  S = exp[(xi^2/2) Delta] ; nu_mono = 1 + h_mono(y)/y with h_RAR(y) = y/(exp(sqrt(y))-1),
  h'_mono = max(h'_RAR, delta h_p/(y+y_p)), delta = 0.05, landmarks y_star ~ 2.3374,
  y_p ~ 2.5396 (to be RE-SOLVED, not assumed).
- Constants: G=6.67430e-11 m^3 kg^-1 s^-2, c=299792458 m/s, footings a0 = 9.3619e-11 and
  1.1279e-10 m/s^2; G_N, G_bare, G_cosmo kept separate (this audit uses no G at all in the
  operator statements).

## Numbered steps executed (mapping of the audit to work order)

1. State the operator, symbol dictionary, measure, metric, domain, boundary conditions.
2. Fourier-multiplier analyticity on Euclidean function classes: L2, Lp, Schwartz, S',
   Sobolev (infinite smoothing), real-analyticity of images.
3. Same audit on the galactic measure dmu_N = N sqrt(h) d^3x (specify pairing; AS205 family).
4. Boundedness of S and S* in L2 (both pairings); sharp criterion; unboundedness witness.
5. Minimum smoothness for S* div[(nu_mono-1) grad S u] distributionally (singularity
   cancellation h_mono(y) ~ sqrt(y)).
6. Both footings; no a0/G/rho_Lambda in the operator identities.
7. Negative controls (capable of failing), residuals saved.
8. Strongest surviving statement + first missing bridge to the full theory.
