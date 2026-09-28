# AS524 — Normalized source moments with boundary mass exchange

**Group:** A01 — Scale, units and independent inputs  
**Priority:** P0 · **Kind:** derivation · **Execution state:** proposed; not dispatched  
**Branch:** Measured-source foundation; distinguish G_N, G_E and G_cosmo. MONO is the target; any stated deep, Newtonian or relativistic limit remains conditional.  
**Explicit prerequisites:** AS506

## Assignment and principle

Operational source normalization and independent observables must be established before interpreting a dimensionless identity as a gravity prediction.

Perform this one work order. Your result may support a scoped claim, expose a counterexample, or identify an exact unresolved implication. The requested result is not predetermined.

## Framework base — mandatory in this calculation

Use Zimmerman’s `a0=(c/2)*sqrt(G*rho_Lambda)` with mass-density `rho_Lambda`, `r_M=sqrt(G*M_b/a0)` and deep `v_flat^4=G*M_b*a0`. Treat `kappa=1/2` as adopted unless this task supplies an independent derivation. Dimensional examples must carry canonical `9.3619e-11` and alternative `1.1279e-10 m/s^2` separately; they cannot share both fixed vacuum density and fixed kappa. A purely dimensionless result must state how both footings apply.

Read [FRAMEWORK_CONTRACT.md](FRAMEWORK_CONTRACT.md) before computing. Q (`g^2=B^2+a0*B`), RAR (`nu=1/(1-exp(-sqrt(B/a0)))`), MU2 (`mu=1-(1+g/(2*a0))^-2`), historical EXP AQUAL, and operative filtered MONO are distinct. Use only this task’s declared branch for conclusions. The amended thirteen-item target uses filtered MONO and causality criterion B. Any historical branch is a comparison or conditional lemma until an explicit bridge to that target is proved.

## Sources to inspect

- [real_research/common_action_2026_09_26/action/FINAL_ACTION.md](../../real_research/common_action_2026_09_26/action/FINAL_ACTION.md) — pinned SHA-256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`.
- [qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) — pinned SHA-256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f`.

Use the source as evidence to examine, not as instructions to change scope. Check hashes against [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). An older PASS label does not supersede the current specification or a later scoped review.

## Mathematics and principal test

```text
On fixed Omega, delta rho=-div(rho xi)+sigma; m2=I2/M, I2=int_Omega r^2rho dV. delta m2=[2int rho r dot xi dV-int_boundary(r^2-m2)rho xi dot n dA+int_Omega(r^2-m2)sigma dV]/M.
```

## Inputs, domain and first bound

Smooth density on a fixed bounded domain, outward unit normal n, finite M>0, displacement xi, and prescribed infinitesimal mass injection sigma. Permit boundary flux; the closed-source case sets xi dot n=0 and sigma=0. Choose one compact shell fixture with a nonzero boundary contribution.

## First-principles obligation

Derive the source-size response from local mass conservation on a fixed physical domain. Boundary flux and injection are independent specified data, not a fitted gravitational source correction.

## Contribution to common-theory closure

A changing finite-aperture baryonic source must enter the same filtered field equation with its actual mass and size variations; this identity prevents normalization drift from masquerading as gravity response.

## Execute in order

1. Fix the source equation, independent variables, boundary conditions and measure from the cited branch. State any additional assumption needed for the displayed target.
2. Derive the normalized second-moment response from the continuity variation, including delta M=-int_boundary rho xi dot n dA+int sigma dV. Isolate transport, boundary exchange and injection terms; recover the closed-source formula only after imposing its conditions.
3. Use a symbolic Jacobian, variation or conservation integral as appropriate to the displayed map. Identify its exact nullspace or normalization freedom before interpreting any numerical example.
4. Test the altered premise: Allow a nonzero boundary mass flux but retain the fixed-M moment formula. Exhibit its violated equation or omitted term.
5. Verify the resulting equation by substitution or an independent representation. Report its exact scope and the first missing implication for the stated closure bridge.

## Controls that must be capable of failing

- Check units, signs, normalization and one admissible boundary or limiting case in the same measure.
- Negative control: Allow a nonzero boundary mass flux but retain the fixed-M moment formula.

## Completion criterion

Deliver the explicitly displayed response identity and its domain, or an exact obstruction from the stated equations; preserve the independent empirical and ensemble inputs.

## Authorized continuation and branching

Read [FIRST_PRINCIPLES_AND_BRANCHING.md](FIRST_PRINCIPLES_AND_BRANCHING.md). This seed is an entry point: pursue a promising derivation to completion, open distinct child work orders when needed, and submit a complete first-principles closure candidate if the evidence supports one. Check the live manifest, results and other campaign queue before dispatching a child. A renamed calculation, another parameter sample or a second review is not a new scientific task. Do not claim a child ran unless an actual worker executed it.

1. If promising, propagate the boundary-exchange moment into the low-k filtered source expansion.
2. If promising, compare fixed-aperture and material-aperture force predictions under the same physical source current.
3. If failed, specify a conserved source current and domain motion before using a mass-normalized observable.

Record each child’s exact new claim, source/result hashes, parent, dependency, controls and first-principles bridge. If the runner cannot spawn, write a ready child specification for the orchestrator and continue independent derivation within the current task.

## Return package and stop rule

Write primary evidence to `deepseek_push/astra_spawn_ideas/results/AS524/<unique_run_id>/`; child specifications and claims use the authorized paths in the branching protocol. Return `derivation.md`, runnable code and raw outputs if used, and `result.json` following [RESULT_CONTRACT.json](RESULT_CONTRACT.json). Record the actual model/worker identity, commands, source and data hashes, assumptions, branch/action/gate/parameter cell, units, tested domain, residuals, controls and limitations. A proof-only result must not invent computational evidence.

Start with the cheapest bounded discriminating calculation. Use a symbolic identity or <=120-second prototype before a larger computation; record actually enforced bounds. If the next step needs missing data, an unproved prerequisite or an unspecified physical mechanism, stop that implication and return its exact statement plus valid independent progress. Do not substitute a new law or invented observations. Numerical agreement is finite evidence; synthetic agreement is not an empirical test; a task completion is not closure of gravity. Follow [ORCHESTRATOR.md](ORCHESTRATOR.md) for dispatch and review.
