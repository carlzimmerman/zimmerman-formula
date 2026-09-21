# Particle-free research: a week of decisive work

Date: 2026-09-20. Scientific baseline: `be1e8c6326230c3c917b984516a6c67d3b17b1b3`.

**The objective is one defensible new result: an independently selected coefficient, a missing action-to-observable derivation, a discriminating measurement, or a precise obstruction that changes the theory.** This is a work order for the existing swarm, not a claim that those results have been obtained.

There are **32 bounded packets: 28 science packets across eight lanes, plus four coordination/review packets**, with approximately **37 agent-days** allocated to first substantive decisions. Use eight workers over seven days as the reference capacity; reserve the remaining capacity for review, integration, failures and genuinely promising follow-through. These are work allocations, not promises that difficult open problems take a fixed number of hours. The critical path can leave downstream experiments blocked even if total capacity remains.

No new dark-matter particle is part of this program. Gravitational fields, auxiliary variables and conserved field charges must still have their degrees of freedom, stress, initial conditions and independently adjustable amplitudes stated. Standard cosmology is an observational/control benchmark; agreement with it is neither the definition of truth nor a derivation of this candidate.

Read the [concurrent-commit reconciliation](CHECKPOINT_DELTA.md), then start with [PACKETS.md](PACKETS.md), use [TASKS.json](TASKS.json) for dispatch, and verify input provenance against [INPUTS.json](INPUTS.json). Every packet is initially **not started / claim open**. Inclusion in this list is not a new theorem, measurement or novelty certificate. This is a broad, prioritized portfolio of the live fronts identified in the recent work, not an exhaustive list of all possible discoveries.

## The most valuable breakthroughs to pursue

| Rank | Breakthrough to earn | Exact missing step | Packets |
| --- | --- | --- | --- |
| 1 | A physical origin for the half, or an exact statement of the remaining freedom | An independent condition selects `lambda=1` with `s` held fixed; current family gives `kappa=1/(2 lambda)` | A1, A2, A3 |
| 2 | A single coherent gravitational action behind the claimed phenomena | Derive the same model's static force, background, physical stress and metric potentials, rather than combining favorable limits from different versions | B1, B2, C1 |
| 3 | Particle-free cosmological perturbations that actually evolve consistently | Derive a constrained FRW operator and the initial modes; demonstrate any CDM-like limit rather than insert it | B3, C2, C3, D1, D2 |
| 4 | A galaxy/external-field prediction that response retuning cannot hide | Establish a usable observable from the orbital/field relations, including finite geometry, screening and shared errors | F1, F2, F3 |
| 5 | A cluster solution with absolute mass and lensing normalization | Solve conservation and self-gravity, then predict dynamics and lensing from the two metric potentials without double counting | E1, E2, E3, B2 |
| 6 | A conserved gravitational component with explained abundance | Derive an attractor/boundary condition or show exactly which cosmological charge remains a free initial datum | C4, D3 |
| 7 | An action-derived two-body law and a cross-size screening test | Enforce momentum conservation, include the Galactic field, and use one allowed screening length across systems | G1, G2, G3, B4 |
| 8 | An independent BH-star transition or stability result | Measure/derive the layer location and local-density bridge; compute a radial mode of the same equilibrium being claimed | H1, H2, H3, H4 |
| 9 | A redshift test with independent masses | Separate a fundamental `a0(z)` prediction from apparent evolution caused by dynamical inference and selection | F4 |
| 10 | A contribution that is both certifiable and accurately described as new | Audit theorem premises, reproduce load-bearing runs, and compare exact claims to primary literature | Q2, Q3, Q4 |

Rank is scientific leverage, not a numerical success probability. A normalization no-go within a stated class, a surviving isocurvature mode, or a failed source identification can be a stronger contribution than another conditional algebraic corollary.

Three complementary routes stay live: **derive the missing mechanism**, **construct a counterexample to the proposed implication**, and **design an independent observation that distinguishes surviving models**. An adverse result in one does not cancel the others.

## What the starting evidence actually supports

The auxiliary action package already supplies an explicit rational response and the conditional half. The free positive coefficient survives channel exchange, saturation and fixed `s`. Therefore re-proving `mu_prime(0)=2` after assuming a unit channel derivative does not finish normalization selection.

The orbital package supplies, under its isolated spherical exterior assumptions, a quarter-slope ratio `Mdyn/Mb=4/3`. The reciprocity package supplies `E^2(1-2 beta)=2` for its local AQUAL class, with the Green-function-to-force bridge an explicit Lean premise and separately checked symbolically. Here `beta=d ln v/d ln r`; `E` compares internal parallel and perpendicular force magnitudes in the external-field-dominated linear limit, **in a different system at the same physical acceleration**. These are conditional relations to operationalize, not current observational discoveries.

Several fresh code observations determine the work order:

| Source at the baseline, unless noted | Inspected behavior | Consequence for dispatch |
| --- | --- | --- |
| `deepseek_push/PD10_zero_mode_measured.py` | The sub-percent “measurement” is asserted in strings/checks; this script does not ingest the underlying galaxy data | A2 reconstructs the likelihood and its calibration dependencies |
| `real_research/clock_2026/L306_s8_closure.py` | Both compared curves call `frw_growth(ag, Omm)` | C2/D2 derive and evolve the actual new operator; equal calls are a control identity |
| `real_research/clock_2026/L307_seeding_gate.py` | Static `R(k)` is promoted to adiabatic seeding; nominal comoving `k` is multiplied by `a` when compared with a physical Jeans wavenumber | C3 derives initial modes; unit correction alone does not establish or destroy the seeding mechanism |
| `real_research/clock_2026/L309_three_sector_cluster.py` | Adds `ph_act=0.42`; fits a caustic-only slope while calling it combined; the lensing check sets `ok3=True` | E1 and B2 are prerequisites to a physical cluster claim |
| `real_research/reviews/bhstar_r1_wind_kinematics.py` | The claimed CAK interval check uses `cak[0] > rstar > r_launch`, rather than testing membership in the CAK interval | H1 rechecks independent wind-radius evidence |
| `fable_independent_2026/lean_2026/I11_bhstar_kepler.lean` | The quartic relation is conditional on the transition equality | H2 tests independent inputs; it does not re-prove the rearrangement |
| Local-only `deepseek_push/lean/PD20_two_body_factor.lean` | Assumes each comparable mass follows the other mass's isolated test-body law | G1 checks the physical premise against momentum conservation; do not duplicate the existing conditional algebra |
| Local-only `real_research/clock_2026/L292_cmb_ymod_carrier.py` | Inspected wrapper uses a generic fluid with `mond_a0=0` | D1 must establish an action-to-fluid map before treating this as a test of the action |

These are source-inspection findings, **not fresh full reruns of those packages**. Existing corrections are valuable and must be retained. New commits may resolve some observations: Q1 verifies the actual diff and raw evidence before retiring a packet.

One listed input, the L292 wrapper, was present locally but absent from the pinned commit. `INPUTS.json` marks it `local_only_uncommitted_at_baseline`, records its inspected hash, and does not pretend it will exist in a clean clone. Obtain the owner's committed version or record it unavailable; do not stage someone else's working file. PD20 and BH U1/I12 were likewise provisional at the baseline but were committed during planning; see the [concurrent-commit reconciliation](CHECKPOINT_DELTA.md) through c5528cdde. They are later evidence, not silently part of the original base. All other 76 listed input files existed in the pinned revision when this work order was built.

## Week schedule and swarm assignment

Day numbers are relative to when the swarm starts. One agent-day means a worker allocation to the bounded packet; computational runtime budgets are separate below. The nominal packet allocations sum to 37, leaving 19 of an eight-worker seven-day capacity for integration, independent review and overruns. This does not override scientific dependencies.

| Day | Dispatch objective | Required checkpoint |
| --- | --- | --- |
| 1 | Q1/Q2 kickoff; A1 normalization discriminator; B1 action map; D3 units; E1 mass bookkeeping; G1 two-body premise; H1 radius/opacity provenance. Start F1 candidate-admissibility inventory/analytic controls and F4 data audit as slots free up. | Every active task has an owner, pinned inputs and a first test that can fail. Identify hard contradictions before expensive runs. |
| 2 | A2 continuous-normalization mocks; B2 full stress; B3 mode reduction; C1 background; B4 common local point; F1 geometry convergence; H4 stability benchmark. | Publish the exact action/model IDs, distinct physical versus inferred sources, and background residuals. |
| 3 | Continue surviving B/C tasks; A3 shape invariant; C4 charge sensitivity; prepare D1 engine interface; G3 size ladder; H2/H3 only where their inputs permit. | Go/no-go for each proposed mechanism. A blocked downstream task returns its exact missing equation and shifts to an independent ready packet. |
| 4 | C2 constrained evolution; E2 coupled infall; F3 screened response; F2 mocks after geometry inputs; G2 external-field binaries after the action/local gates. | At least one independently reproduced analytic/control limit for every new numerical pipeline. |
| 5 | C3 mode transfer, D2 growth and D1 action-to-engine map when available; E3 joint projection if sources are derived; F2/F4 feasibility or held-out pilot. | Freeze models, nuisance rules and comparison statistics before interpreting held-out data. Never fill absent upstream physics with a favored fluid by default. |
| 6 | Finish the smallest defensible scientific output; Q2 fresh certificates/reruns; Q3 exact-source novelty checks. Redistribute unused time to surviving discriminators, not more PASS-count bookkeeping. | Each candidate result has a scoped statement, raw evidence, contrary controls and a second reader's critical-step reconstruction. |
| 7 | Q4 integration and independent review. Re-run from pinned artifacts, reconcile model versions, write the paper outline and next queue, push reviewed results to main. | One week report separating proved implications, numerical evidence, empirical findings, rejected branches and still-open obligations. |

This is a priority schedule, not an instruction to run every entry concurrently or guarantee every downstream solve by day five. When C2/C3 take longer, D1's week-one deliverable is its validated interface/controls and exact missing-operator list. When data are inadequate, F2/H2 deliver instrument limits and a measurement specification. Those are real completed work products; the physical claim stays open.

For eight workers, give one primary physics lane A–H to each worker. Rotate Q1/Q4 coordination among one designated integrator and allocate Q2/Q3 as cross-reviews: a worker must not independently review its own derivation. At kickoff, C and D workers can take Q1/Q2/D3 while action prerequisites are prepared. The integrator controls the shared registry and main; workers own only their packet outputs.

For four workers, use A+F, B+G, C+D, E+H tracks; prioritize P0 and one downstream instrument, leaving other packets as the next queue. For twelve workers, keep the same dependency graph and use extra capacity for independent derivations, numerical validation and literature checks. Extra agents do not make an unresolved premise true.

## Dependencies and forks

The machine-readable graph is in `TASKS.json`; respect `dispatch_not_before_day` as well as dependencies (Q4 integrates on day seven). These are the principal chains:

```text
A1 -> A3                         A2 informs F2 covariance
F1 -> F2 (quarter-slope branch needs no lambda measurement)
B1 -> B2 -> E2 -> E3             E1 -> E2
B1 -> C1 -> C2 -> C3 -> D1       B3 -> C2
B1 -> B3      C2 -> D2 (late-time growth)       C1 -> C4
B1 -> B4 -> G2                  G1 -> G2
          -> G3
H1 -> H2                        B1 + H1 -> H3
Independent early routes: D3, F3, F4, H4, Q1, Q2, Q3
Integration: Q4 consumes reviewed outcomes, including failures and partials.
```

Absolute primordial-normalized power/sigma8 in D2 also needs reviewed initial-mode covariance and radiation-era transfer, or explicitly conditional external transfer inputs. The normalization-free F2 quarter-slope test needs independent baryonic calibration, not a successful measurement of lambda.

An arrow means an input/equation is required for the main scientific run. It does **not** mean an upstream proposition has already been proved, nor that a successful process exit supplies that proposition. An upstream obstruction can be the scientifically useful input: the dependent branch must then be narrowed, revised or retired. Preliminary source audits and control construction may run earlier and remain labelled preparation.

Do not revive a superseded construction just because it once had many passing gates. Keep the action ID, kernel, coupling, boundary conditions, normalization convention and initial data identical across a joint claim. A repair is allowed and may be the breakthrough; assign it a new model version and rerun affected gates. Preserve the failed version and explain which new input changes the result.

## Evidence required from every worker

For the clock/metric lanes use `ds^2=-(1+2Psi)dt^2+a^2(1-2Phi)dx^2` with `c=1`: dynamics probes `Psi`, lensing probes the sum, and the Weyl potential is `(Phi+Psi)/2`. The static auxiliary package calls its dynamical potential `Phi`; translate explicitly rather than silently mixing conventions.

Each result directory must contain the packet-specific deliverables plus `RESULT.md` and `manifest.json`. Use [RESULT_TEMPLATE.md](RESULT_TEMPLATE.md). A proof, a calculation and an observation are distinct evidence types.

1. State the exact target, hypotheses, dimensional conventions, model ID and dependency revisions. Explicitly label independent inputs, fitted quantities, postulates and derived outputs.
2. Record base commit, actual source/data hashes, toolchain/import versions, command lines, exit statuses, seeds, tested ranges and resource use. Store raw output, including failures; do not overwrite the successful run with a negative-control run.
3. For Lean, print axioms for the load-bearing theorems and inspect their full types. Reject `sorryAx` and undeclared extra axioms. Name physical/variational/PDE premises still supplied externally. The standard library axioms are not experimental evidence.
4. For symbolic work, state domains and singular strata; test branches and dimensions. For numerical work, require residuals, conservation/analytic controls and resolution/tolerance checks. A grid is evidence on that grid, not a universal theorem.
5. For observations, track raw-source versions, independent calibration, shared covariance, selection and identifiability. Separate an ideal precision target from achieved uncertainty. No significance from percentages without a defined likelihood.
6. Include an adversarial or mutation control that actually changes the asserted property. A literal `True`, an inserted target equation or another algebraic form of the same premise is not an independent check.
7. Distinguish **execution state** (`not_started`, `claimed`, `running`, `completed`, `failed`, `blocked`, `abandoned`) from **claim state** (`open`, `proved_conditional`, `refuted_in_scope`, `finite_evidence`, `inconclusive`). “Completed” means the work packet returned an artifact, not that its conjecture is true. Record a process ID/job ID and last observation for any ongoing run; stale observations do not imply it is still running.
8. Return the first surviving uncertainty and the next discriminating action. An unsuccessful proof attempt is not a refutation. An explicit counterexample refutes only the claim and hypothesis class it actually addresses.

## Work ownership and integration

Workers read shared inputs and write only `real_research/swarm_week_2026_09_20/work/<ID>/`. Include any adapted solver inside that scope or as a proposed patch, so parallel workers do not mutate shared source libraries, historical results or each other's inputs. Existing action documents and frozen preregistrations remain source material; suggested amendments belong in the packet until integration.

The integrator assigns a packet before dispatch, serializes registry changes, and reconciles new repo commits at each checkpoint. A filesystem/git collision is not a reason to overwrite another worker. Optional isolated worktrees may use `codex/` branches; **reviewed deliverables integrate directly into `main`, with no PR required by this program**. Stage only the owned paths. Preserve unrelated local changes and uncommitted research.

If a watcher notices this work order, it should choose an unowned ready packet through the integrator, not let every agent independently edit `TASKS.json`. The JSON is a work registry, not a locking service or running scheduler. This publication does not create recurring jobs, launch the 32 tasks, or authorize external messages or a Zenodo deposit.

Start computational experiments with one analytic/control case and a local run capped at roughly 15 minutes. Expand to at most two local CPU-hours per clearly identified experiment after the control passes; record processes and checkpoints. These are default planning caps, not new permission ceremonies: use available authorized resources, coordinate concurrent load, and stop uninformative scans. Do not launch an unbounded catalog, cosmological simulation or external paid compute job as a substitute for the first discriminator.

## Paper-shaped outcomes and release gates

The most promising week-one outputs are:

- A conditional normalization-selection theorem **with its independent selector**, or a precise nonselection theorem that locates the missing physics.
- A corrected action-derived two-body law, response invariant or screened field-orbit relation with explicit limits and a bounded literature comparison.
- A fixed-action cosmological reduction with constraint preservation and a quantified initial-condition/transfer claim.
- A no-double-counting source theorem plus a controlled cluster solution, or a rigorous obstruction to the proposed combination.
- A geometry-controlled instrument and held-out test, or a quantitative impossibility/precision bound showing which observation is needed.
- A noncircular BH-layer relation or matched radial-stability calculation, with independent observational or equilibrium inputs.

A publishable note needs an exact contribution, a complete argument at its claimed level, a reproducible artifact bundle, accurate comparison to prior work and an honest limitations section. Novelty, mathematical validity and empirical adequacy are separate gates. A Zenodo timestamp records a deposit; it does not turn a known result into a new one or validate a physical premise. Week one prepares a release candidate; it does not automatically publish externally.

The existing [clock work order](../../fable_independent_2026/clock_swarm_2026/CLOCK_WORK_ORDER.md) and [focused observation roadmap](../reviews/particle_free_validation_2026_09_20/README.md) remain useful source maps; Q1 reconciles their older statuses against current artifacts. Do not restart completed weighting/bootstrap, conditional derivative or quartic-rearrangement work and call it a breakthrough.

## Literature leads and stretch queue

Two primary-source landing pages were checked while preparing this program: the [general deep-MOND virial theorem](https://arxiv.org/abs/1311.2579v2), which already covers isolated point-mass force relations under its assumptions, and the [AQUAL/QUMOND external-field solution](https://arxiv.org/abs/1509.08457v3). G1/F3/Q3 must read and translate the relevant full-text hypotheses before importing a result. This small check is not a novelty search for the entire program.

After the first gates, possible extensions include a full PDE-to-Lean Green-function bridge; a nonlinear existence/well-posedness theorem; radiative protection of a successful normalization selector; a full CMB likelihood after the action adapter; merger/offset predictions after a validated cluster source; time-dependent radiation hydrodynamics after the BH geometry/stability benchmark; and a joint redshift/environment/size likelihood after the individual instrument tests. These are **stretch routes, not week-one promises**. Each needs a fresh bounded packet and explicit prerequisites. The week should choose which deserve the next week, using results rather than enthusiasm.
