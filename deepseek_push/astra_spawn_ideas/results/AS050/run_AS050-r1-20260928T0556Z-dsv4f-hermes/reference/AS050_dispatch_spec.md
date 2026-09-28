# AS050 — dispatched task specification (verbatim capture)

**NOTE ON PROVENANCE (added by worker, not part of the spec):**
The file path given at dispatch — `deepseek_push/astra_spawn_ideas/AS050_stable_evaluation_of_the_rar_deep_x.md` —
does **not** exist in the repository (verified by search on 2026-09-28). The catalog file for AS050
(`deepseek_push/astra_spawn_ideas/AS050_a_branch_specific_primitive_cannot_fix_its_zero.md`, SHA-256
`db6efad6ff61cc21a73a9ca913dad9a3190881b9f2bebee1f65f4d69da37c717` per `deepseek_push/astra_spawn_ideas/claims/AS050.json`)
is a different topic ("branch-specific primitive cannot fix its zero", state: proposed, not dispatched).
`claims/AS050.json` (owner hermes-orchestrator) records task AS050 as **reserved and dispatched**
(dispatched_utc 2026-09-28T05:42:53Z, result_base `results/AS050/`), which matches the dispatch this run
executed. The executed specification is therefore the dispatch text itself, captured verbatim below
(`task_sha256` in result.json is the SHA-256 of **this file**). The closest catalog sibling of this
specification is AS028 (`AS028_rar_deep_expansion_with_stable_evaluation.md`), whose run
`results/AS028/run_AS028-r1-20260928T0010Z-dsv4f-hermes` is cited by this spec ("cf. AS028") and is used
here as the companion result and cross-check.

---

## Dispatch text (verbatim)

MANDATORY FRAMEWORK: a0 = kappa*c*sqrt(G*rho_Lambda), kappa=1/2 ADOPTED as input.
Task AS050: STABLE EVALUATION OF THE RAR DEEP X — the RAR deep-branch evaluation
x = y/(1 - exp(-sqrt(y))) loses catastrophic precision for small y (near-cancellation in the
denominator); derive and verify the numerically stable form (multiply by exp(+sqrt(y)):
x = y*exp(sqrt(y))/(exp(sqrt(y)) - 1), or an expm1-free rearrangement), quantify the accuracy
gain over the naive form at y = 1e-4..1e-16 (fp64), verify the deep series route (cf. AS028:
x/sqrt(y) = 1 + s/2 + s^2/12 - s^4/720 + ... with the Bernoulli coefficients) and its radius,
and state the branch that is operative (comparison RAR; MONO deep inherits via the splice).
Both footings: 9.3619e-11 and 1.1279e-10 m/s^2. Numerics: G=6.67430e-11, c=299792458 (SI).
G_N/G_bare/G_cosmo SEPARATE. Branches distinct: Q, RAR, MU2, EXP, MONO (criterion B).

EXECUTION RULES: follow the task's numbered steps in order; derive every intermediate
factor/sign/unit; run the negative control (capable of failing — e.g. show the naive form
fails at the declared precision while stable passes, with actual error numbers). Bounded
prototype: <=120 s, <=512 MB, 1 thread — record ACTUALLY enforced bounds. Proof-only
results must NOT fabricate computational evidence — actual residuals, not booleans.

DELIVERABLES: unique run dir deepseek_push/astra_spawn_ideas/results/AS050/<unique_run_id>/
containing derivation.md, result.json (ALL schema-v2 fields; task_sha256; worker = YOUR ACTUAL
identity; execution_status; outcome enum; exact_claim; framework_cell; new_assumptions;
input_sha256; artifacts_sha256; commands; execution_bounds; checks; tested_domain;
failed_attempts; limitations; next_unresolved_implication; suggested_followup;
acceptance_state='unreviewed'; ancestry=null; first_principles_inputs; closure_implication;
child_proposals; closure_candidate=null), plus code and raw outputs.

LEAN CERTIFICATE: if an algebraic identity is worth certifying (e.g. the two forms are
algebraically identical: y/(1-e^-s) = y*e^s/(e^s-1) via exp_neg; or the exact Bernoulli
series identity through some order), write a self-contained Lean 4 certificate in the run
dir and verify: cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean. Hard
bar: zero sorry, axioms subseteq {propext, Classical.choice, Quot.sound}. COMPILE HOST ONLY:
never write files into fable_independent_2026/lean_2026. If no Lean, say why.

DO NOT: modify any task spec, contract, manifest, ledger, or claim file; touch other workers'
results; edit shared status files; claim anything ran without executing it; create claims/
files.

FINAL ANSWER (compact): (1) run_id + result dir; (2) outcome; (3) strongest statement +
domain; (4) negative-control result; (5) next_unresolved_implication; (6) lean path + axioms
or 'no lean: <reason>'; (7) one-line limitations.
