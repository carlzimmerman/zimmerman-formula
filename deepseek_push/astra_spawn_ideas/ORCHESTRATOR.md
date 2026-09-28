# Astra orchestration and DeepSeek dispatch

The catalog is an authored queue of research specifications. **No DeepSeek worker, API job or recurring automation is launched by this package.** Actual execution requires the user's configured DeepSeek runner or an explicitly selected agent mechanism. A task intended for a model is not evidence that model ran it.

## Dispatch one bounded mathematical obligation

1. Read the task, `FRAMEWORK_CONTRACT.md`, source hashes and prerequisite results. Check for equivalent completed/running work in this catalog and `fresh_gravity_followups/`; compare equations, assumptions and ranges, not just titles. A source-revision change or genuinely new obligation may justify a new task; independent reproduction of the same claim is a review role attached to the existing task, not another seed.
2. Select one coherent framework cell: action revision, branch, scale convention, filter, gate, matter coupling, parameter domain and initial/boundary data. Claims from another cell remain comparisons until a translation is proved.
3. A dispatcher reserves `claims/ASnnn.json` using exclusive creation (`open(path, 'x')`). Record task/source hashes, owner, actual worker ID if already known, intended runner if not, reserved output directory and current execution state. Update a reservation to running only after launch is observed. An existing claim prevents duplicate dispatch; reconcile stale claims with the owner and preserve their history.
4. Give the worker the full task Markdown plus `FRAMEWORK_CONTRACT.md`, `FIRST_PRINCIPLES_AND_BRANCHING.md` and `RESULT_CONTRACT.json`. Use the single-task prompt below. Run independent ready tasks in parallel; chain dependencies only after their scope is reviewed. Authors/reviewers may audit an unproved candidate explicitly, but must not import it as an accepted theorem.
5. First computation is a bounded prototype: normally <=120 seconds, <=512 MB target working memory, one CPU thread where feasible, <=512 grid cells and two refinements. These are initial planning bounds, not assertions that tools enforce them. The runner must enforce and record actual bounds. Large likelihoods, Boltzmann integrations, PM/N-body runs or global PDE proofs require narrower prerequisites and an explicit resource allocation before scaling. A difficult symbolic implication that cannot be resolved in a bounded turn returns its exact gap.
6. The worker writes primary evidence to `results/ASnnn/<unique_run_id>/` and may create child specifications and exclusive claims as the branching protocol permits: `derivation.md`, runnable source when applicable, raw outputs, `result.json`, and provenance. Read source before execution and redirect copied historical scripts that otherwise overwrite their own results. Never modify original science files, task specifications or another worker's results.
7. Reconcile every return as evidence. Check source freshness, code, actual execution status, negative controls, full equations and missing terms. Reproduce the critical step independently before accepting a load-bearing claim. Store a new review under `reviews/ASnnn/`; a worker cannot award itself accepted closure.
8. Failures are informative: distinguish false claim, excluded candidate, implementation error, missing data and inconclusive method. Preserve counterexamples. Create a narrower continuation only when it changes the unresolved step or addresses the obstruction. Do not endlessly rescan the same failed parameter cell.

## Single-task prompt to paste into the actual runner

```text
Execute ASnnn from deepseek_push/astra_spawn_ideas/<task_filename>.
Read that file, FRAMEWORK_CONTRACT.md, FIRST_PRINCIPLES_AND_BRANCHING.md,
RESULT_CONTRACT.json and the named
source files at the pinned hashes. Use the Zimmerman equations and declared
branch in every calculation. First restate the exact claim and list supplied
versus derived quantities. Put evidence in results/ASnnn/RUN_ID/ and child
specifications/claims only in the branching protocol’s authorized paths.
Follow the numbered steps. Derive every intermediate factor/sign and test the
specified negative control. Keep both scale footings separate. Do not repair
failure by silently changing the kernel, coupling, action, gate or selection.
A materially different repair may be proposed as a labeled child candidate.
If a needed prerequisite is absent, return the exact missing implication or
missing file and any independent work that is still valid. A synthetic test
must remain synthetic. Save the actual proof or reproducible computation,
raw failures, checked domain and RESULT_CONTRACT fields. Report one strongest
supported statement and one next unresolved implication. Pursue useful
findings via distinct children after duplicate checking. If your derivation
provides a complete first-principles closure witness, submit it with the
thirteen-gate map for independent review; do not self-accept closure. Do not
edit shared status files or claim children ran without actual execution.
```

## Keep a small worker focused

The task file defines one primary output. The dispatcher should supply the common contract once, then the task and only the cited source sections needed for its equation. Locate a symbol with `rg -n`, read a bounded surrounding slice, and expand only when a definition or boundary term is missing. Preserve the exact equation and source hash in a short working note. Do not ask a small worker to digest entire campaign histories or solve all open gates at once. When a task reveals a second load-bearing calculation, return it as an explicit prerequisite or narrower child work order; never fill the gap with plausible prose.

A constrained follow-up may compute one derivative, one matrix block, one inverse, one conserved flux, one counterexample or one calibrated estimator. A synthesis task consumes reviewed outputs; it does not recreate all of them in its context window. The orchestrator, rather than the smallest worker, owns cross-task consistency and the final closure verdict.

## Waves and dependencies

* **Wave 0: freeze the mathematical input.** AS001–AS050 and the first five coefficient/equilibrium/statistical tasks reconcile units, kernels, source normalization and premise dependence. These are deliberately inexpensive controls. They need not all finish before unrelated symbolic tasks begin.
* **Wave 1: common equations and constraints.** A06/A07 and background A11 construct or audit the same varied action, constraints, homogeneous branch and source response. Resolve measured-G and global-static-target changes before trusting downstream parameter intersections.
* **Wave 2: health and transport.** A08/A09/A12/A13 establish the reduced finite-wavelength operator, zero-field treatment, conservation, and candidate transport. A14/A15 connect those equations to halo and merger tests. A static or homogeneous pass never skips a missing spatial evolution condition.
* **Wave 3: calibrated predictions.** A10/A16/A17/A18 compute physical observables with the same equations. Inference-method prototypes can proceed on labelled synthetic data while action prerequisites remain open; final empirical acceptance cannot.
* **Wave 4: evidence and closure.** A19 establishes distinct mathematical/statistical evidence certificates; A20 assembles actual constraint intersections and compatibility tests. Closure requires all mandatory obligations in one common cell and independent review, not 2000 green task flags.

`manifest.json` contains task-level explicit prerequisites. They are necessary stated dependencies, not an assertion that the mathematical dependency graph is exhaustive. Each worker must add any newly discovered prerequisites in its result. P0 means a high-information bottleneck or foundational check; P1 means the next constructive/refinement layer; P2 means downstream or optional specialization. It is not a scientific confidence score.

## Closure gates: preserve the amended thirteen requirements

| Spec item | Required evidence | Primary catalog groups |
|---|---|---|
| 1 | Operative filtered MONO derived from the same action, with the correct source and domain | A02, A06, A09, A20 |
| 2 | Full constraint count gives two gravitational modes; any matter/clock modes counted and healthy | A07, A08 |
| 3 | Both physical potentials independently derived; galactic no-slip and lensing | A10, A18 |
| 4 | Derived beta, gamma and preferred-frame PPN within verified bounds | A10, A18 |
| 5 | Ordinary-matter covariant conservation from the actual coupling | A06, A07, A13 |
| 6 | Tensor speed, positive kinetic energy and polarizations from that action | A08, A10, A18 |
| 7 | All-sector stability, interaction control and criterion B with a well-posed mixed problem | A08, A09, A12 |
| 8 | Nontrivial expanding cosmology, including the distinct homogeneous constraint | A11, A12 |
| 9 | Controlled zero-field and constraint-rank limits | A02, A07, A09 |
| 10 | Newtonian/GR limit and measured G derived and matched | A01, A10, A18 |
| 11 | One physical matter/photon metric with compatible GW propagation | A06, A10 |
| 12 | Specified RAR segment and MONO continuation preserved, no hidden kernel substitution | A02, A06, A09 |
| 13 | Framework a0–vacuum relation explicitly preserved as input or genuinely derived | A01, A03, A11 |

A finished **conditional effective theory** can retain the empirically adopted coefficient as the spec permits, but must say so. Deriving the absolute magnitude of every fundamental constant is a separate ambition. Conversely a closed formula, exact Lean implication, finite numerical parameter window or good fit cannot substitute for missing mandatory gates. Mark each gate `open`, `conditionally supported`, `rejected for this candidate`, or `accepted in stated scope`, and keep implementation/computation status separate.

## Concurrent fresh-gravity namespace

`fresh_gravity_followups/` is owned by the separate “Start fresh gravity campaign” chat. Its FGF tasks and existing evidence are additive and **not counted among AS001–AS2000**. This catalog links them but does not launch, overwrite or claim their executions. Use their source-pinned queue to avoid duplicate spectroscopy, calibration, cluster and scale-dynamics tasks. Adapt result metadata into a separate intake review while preserving original worker identity and evidence hashes.

## Adaptive first-principles push

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md) before dispatch. Every seed may continue to a complete derivation or propose distinct child tasks on a promising result or a useful failure. Check claim fingerprints and existing results first; give duplicate scientific obligations one owner. Reviews are separate roles, not extra seed tasks. Keep child source/evidence hashes and exact parentage. Children do not change the fixed count of 2,000 seed files.

The expanded ranges AS501–AS2000 add 75 obligations per group; together with each group’s original 25, every area now has 100. Group membership is in the index/manifest rather than one continuous ID range. Start with the specific prerequisites of a desired implication, not by running all seeds blindly. AS2000 is the final common-action witness target, but any worker may submit that witness when its route actually provides all required links. A closure claim must state which normalization, kernel, initial-state and source assumptions remain independent; strong first-principles closure cannot relabel those inputs as derivations.

Consult [REUSE_BEFORE_DISPATCH.md](REUSE_BEFORE_DISPATCH.md) for live evidence pointers and the specifically identified AS465/FGF-018 overlap before assigning related work.

## Additional dated-measurement work

Use [CATALOG_REGISTRY.json](CATALOG_REGISTRY.json) to include the 2,500 MY tasks alongside the original 2,000 AS seeds. The [MY dispatch guide](measurement_decade_2017_2026/DISPATCH.md) adds raw-data availability checks, release-overlap accounting, chronology and fair coverage across years. [LAUNCH_PROMPT.md](measurement_decade_2017_2026/LAUNCH_PROMPT.md) supplies one combined orchestration prompt. Preserve current AS/FGF claims and actual worker identities; catalog authorship is not execution.
