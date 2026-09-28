# AS096 — Canonical versus microcanonical profile stability

**Group:** A04 — Finite-domain equilibrium and virial closure  
**Priority:** P1 · **Kind:** audit · **Execution state:** proposed; not dispatched  
**Branch:** Conditional deep-equilibrium sector; no automatic particle ontology  
**Explicit prerequisites:** AS076, AS079

## Assignment and principle

A static maximum-entropy profile, virial balance, source normalization and dynamical attainment are distinct obligations. Derive the profile from the framework potential and keep finite boundaries explicit.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [deepseek_push/G084_maxentropy_law.py](../../deepseek_push/G084_maxentropy_law.py) — pinned SHA-256 `752999fdf6c07b0cf0fb419290177f90151a239d63c7707029b240fef46735ec`.
- [deepseek_push/G091_virial_triad.py](../../deepseek_push/G091_virial_triad.py) — pinned SHA-256 `8164360f95fdc340824a92a5db3ccdabf3ce28430bdd1c375e276a77ba67ece5`.
- [deepseek_push/G233_eos_noscalar.py](../../deepseek_push/G233_eos_noscalar.py) — pinned SHA-256 `ad89298d967ae4f2d574a47f91d5adc54addae40b6a5e47d0bd83cf5564a8b03`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
For mass-weighted S=-int rho*ln(rho/rho_ref)dV, use F_v=E-sigma^2*S at fixed velocity-temperature sigma^2; E has energy units and S mass units. Equivalently use F=E-T*S_phys with S_phys=(k_B/m)*S. The microcanonical problem instead fixes E.
```

## Inputs, domain and first bound

Use C=sqrt(G*M_b*a0), r_M=sqrt(G*M_b/a0), positive finite shell r_in<=r<=R with r_in>0 and R<=r_M unless specified. Diagnostics use r_in/R=0.01,0.1,0.5 and R/r_M=0.62,1; these are controls, not a fit. R<=r_M fixtures test the historical imposed-log-well ansatz, not a controlled point-source deep-MOND domain. For the actual deep exterior use separate shells r_in/r_M=10,100 with R/r_in=2,10, or bound the full-kernel error. Do not transfer an interior ansatz to filtered MONO without that check.

## First-principles obligation

Start from the declared Conditional deep-equilibrium sector; no automatic particle ontology equations and inspect the source premises for Canonical versus microcanonical profile stability. Derive the stated mathematical object from those premises, listing every independent coefficient, boundary condition and measured input. A static maximum-entropy profile, virial balance, source normalization and dynamical attainment are distinct obligations. Derive the profile from the framework potential and keep finite boundaries explicit. The adopted one-half normalization is not a derived result unless an independent argument removes its freedom.

## Contribution to common-theory closure

Supply the precise implication represented by Canonical versus microcanonical profile stability to a single common-action closure witness. Deliver a self-contained derivation or explicit counterexample to the named claim, with reproducible checks. A conditional theorem must list every condition; missing dynamics or data is an explicit open dependency, never a pass. Identify the affected operative gate and prove any branch-translation or reduction used before transferring the result.

## Execute in order

1. Read the cited equations and write the precise claim, symbol dictionary, boundary conditions and assumptions needed for this task. Distinguish framework inputs from conclusions to be established.
2. Derive the two constrained Hessians for the fixed-well system and identify which is tested by G084. State why self-gravitating ensemble conclusions cannot be transferred automatically.
3. Show the intermediate algebra or integration, including all scale factors, signs and units. If the calculation uses a limiting regime, derive the leading neglected term and state its domain.
4. Perform an independent check using a different representation: substitution into the original equation, direct differentiation, or a bounded high-precision calculation. Save the actual residual, not only a Boolean.
5. Apply the specified negative control, then write the strongest surviving statement and the first additional implication needed to transfer it to the full theory. Do not import a different branch to repair a failed result.

## Controls that must be capable of failing

- Change ensembles while reusing an unconstrained Hessian sign.
- Check the deep and Newtonian limiting regimes wherever they exist; otherwise check normalization and a boundary case. Distinguish an exact identity from a finite numerical consistency check.

## Completion criterion

Deliver a self-contained derivation or explicit counterexample to the named claim, with reproducible checks. A conditional theorem must list every condition; missing dynamics or data is an explicit open dependency, never a pass.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If the main result survives its controls, strengthen Canonical versus microcanonical profile stability by removing its weakest explicitly named independent premise or extending its quantified domain. State the new target equation and why the existing result does not already answer it.
2. If the result supplies a missing response or bound, derive its consequence for the nearest unresolved same-action gate. Use the actual formula and its error/domain limits from this result; identify the gate and a distinct observable or theorem before dispatch.
3. If a counterexample or obstruction appears, isolate the smallest failed implication in Canonical versus microcanonical profile stability. Construct a target-native repair or no-go proof, preserving the counterexample and rechecking all assumptions changed by the repair.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS096/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
