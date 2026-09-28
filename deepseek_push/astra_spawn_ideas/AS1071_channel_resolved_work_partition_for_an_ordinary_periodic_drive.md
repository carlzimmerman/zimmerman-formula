# AS1071 — Channel-resolved work partition for an ordinary periodic drive

**Group:** A08 — Linear health and interaction control  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CA5-GNC-R; filtered nu_mono target; criterion B — Constrained interactions and quantitative health  
**Explicit prerequisites:** AS1031, AS1032, AS1059, AS866, AS992

## Assignment and principle

Import the total passivity criterion and derive how actual same-action host, carrier and tensor sectors exchange the supplied work.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/breakthrough_review_2026_09_26/occupied/RESULT.md](../../real_research/breakthrough_review_2026_09_26/occupied/RESULT.md) — pinned SHA-256 `6091291f05fca5f1f4fdcc216f305bd31a476a7ea3d16c09131faca1158975d5`.
- [real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md](../../real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md) — pinned SHA-256 `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d`.
- [real_research/peer_review_2026_09_26/NEXT_CALCULATIONS.md](../../real_research/peer_review_2026_09_26/NEXT_CALCULATIONS.md) — pinned SHA-256 `50f3dfd4ba980339b6ba6474ce1c1377c16c8d9e3c019e28036d5c98e8c33361`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
For periodic ordinary driving at omega, derive cycle-averaged sector balances W_A=sum_B X_AB+F_A with X_AB=-X_BA, where W_A is assigned driving work, X_AB internal exchange and F_A outgoing physical energy flux. The sum must equal total detector work.
```

## Inputs, domain and first bound

One healthy stationary candidate background and a weak ordinary source with a fully conserved stress completion; use the actual coupled retarded response and finite boundary. One smooth admissible background and a declared finite momentum band; retain canonical normalization and all constrained exchange terms. Zero field and the MONO splice require separate regularity hypotheses.

## First-principles obligation

Use the already derived quadratic reduction and vertices of the same CA5 action. Background amplitudes, couplings and momentum cutoffs remain inputs; no phenomenological damping may be inserted.

## Contribution to common-theory closure

A channel-resolved work ledger connects physical detector energy to the constrained action and prevents hidden dissipation or spurious ghost claims in reduced models.

## Execute in order

1. Use the previously derived total passivity sign convention instead of rederiving a generic susceptibility theorem.
2. Derive each sector work and exchange term from the same action, retaining clock, projected mean and boundary contributions.
3. Evaluate one allowed driven channel and check cancellation of internal exchanges when sector balances are summed.
4. Distinguish a negative local sector work term from negative total supplied work or a negative-norm mode.

## Controls that must be capable of failing

- Zero intersector coupling must remove the corresponding exchange entries.
- Negative control: equate a negative carrier-sector work contribution with violation of total passivity while omitting its compensating host exchange.

## Completion criterion

Deliver the requested relation with its domain, or a concrete obstruction and the failed estimate. Keep finite verification separate from a general proof.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising: Can one observable isolate energy transferred specifically into the physical clock channel?
2. If promising: Does a controlled outgoing-flux approximation yield a derived effective damping term for the driven source?
3. If failed: Restore the missing exchange or boundary term before assigning nonconservation to the action.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS1071/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
