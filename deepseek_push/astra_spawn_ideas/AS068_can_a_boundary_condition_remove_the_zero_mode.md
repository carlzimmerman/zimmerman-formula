# AS068 — Can a boundary condition remove the zero mode

**Group:** A03 — Coefficient mechanisms and their missing premises  
**Priority:** P1 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** CORE coefficient; conditional MU_n statistical response  
**Explicit prerequisites:** AS067

## Assignment and principle

A derivation of kappa must remove a genuinely independent freedom. A channel count, algebraic identity or adopted normalization is useful only with its physical identification separately justified.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/PD01_polarization_count.py](../../deepseek_push/PD01_polarization_count.py) — pinned SHA-256 `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d`.
- [deepseek_push/PD08_particle_free_derivation.py](../../deepseek_push/PD08_particle_free_derivation.py) — pinned SHA-256 `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb`.
- [kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py](../../kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py) — pinned SHA-256 `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
Impose J(Y_ref)=0 and J'=specified kernel; J(0)=-int_0^Y_ref J'(Y)dY.
```

## Inputs, domain and first bound

Use s=c*sqrt(G*rho_L), Y=g/s, positive finite dimensionless parameters, and symbolic n>=1. Evaluate diagnostic counterexamples at lambda=1/2,1,2; do not use observational preference as a mathematical proof.

## First-principles obligation

Start from the declared CORE coefficient; conditional MU_n statistical response equations and inspect the source premises for Can a boundary condition remove the zero mode. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. A derivation of kappa must remove a genuinely independent freedom. A channel count, algebraic identity or adopted normalization is useful only with its physical identification separately justified. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Can a boundary condition remove the zero mode to a single common-action closure witness. Deliver a self-contained derivation or explicit counterexample to the named claim, with reproducible checks. A conditional theorem must list every condition; missing dynamics or data is an explicit open dependency, never a pass. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Read the cited equations and write the precise claim, symbol dictionary, boundary conditions and assumptions needed for this task. Distinguish framework inputs from conclusions to be established.
2. Derive the determined constant and count the external data introduced through Y_ref. Decide whether a physically derived boundary or an adopted convention supplied the relation.
3. Show the intermediate algebra or integration, including all scale factors, signs and units. If the calculation uses a limiting regime, derive the leading neglected term and state its domain.
4. Perform an independent check using a different representation: substitution into the original equation, direct differentiation, or a bounded high-precision calculation. Save the actual residual, not only a Boolean.
5. Apply the specified negative control, then write the strongest surviving statement and the first additional implication needed to transfer it to the full theory. Do not import a different branch to repair a failed result.

## Controls that must be capable of failing

- Vary Y_ref while retaining the static kernel and exhibit the changed vacuum prediction.
- Check the deep and Newtonian limiting regimes wherever they exist; otherwise check normalization and a boundary case. Distinguish an exact identity from a finite numerical consistency check.

## Completion criterion

Deliver a self-contained derivation or explicit counterexample to the named claim, with reproducible checks. A conditional theorem must list every condition; missing dynamics or data is an explicit open dependency, never a pass.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Can a boundary condition remove the zero mode by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Can a boundary condition remove the zero mode. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS068/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
