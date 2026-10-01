# astra crispy ideas: forty research calculation cards

**Goal:** identify the next forty bounded, rigorous calculations that can advance or decisively constrain the user's gravity framework, without repeating completed work.

**Architecture:** one canonical filtered nu_mono construction with causality criterion B; separately labeled exact-RAR and exact-AQUAL comparisons; distinct CA5, CD26-2 spectral and phenomenological-carrier lanes. No result transfers between actions without an explicit derivation.

**Tools:** analytic variation and functional estimates first where required; existing Python/SymPy/numerical routines for scoped computations; primary observational sources for actual data comparisons. No new runtime dependencies are prescribed by this plan.

**Spec:** repository `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` and `CRISPY_FRIED_CHICKEN_RECIPE.md` in the same directory, with the 2026-09-26 author decision. Source keys and exact snapshot hashes are in [the inventory](2026-09-26-astra-crispy-ideas.sources.json).

**Global constraints:** freeze the action, domain, boundary data, kernel and physical matter metric. Derive both metric potentials independently. Count all modes. Treat the homogeneous/global mode separately. Keep a0/vacuum normalization as input unless actually derived. Never turn finite-resolution evidence into a continuum theorem.

**Review focus:** does the first calculation answer a genuinely open arrow; can it fail; are the constraints varied before elimination; are claimed estimates uniform in the relevant limits; is any empirical pass using the same epoch, trigger, footprint and action it claims to test?

This is an agent work queue, not an instruction to execute all forty at once. Every task initially has status **proposed**. Completion may be a positive result, a scoped counterexample, or a rigorously localized obstruction. An unproved conjecture or a script exiting zero is not a completed proof.

## Snapshot and already completed work

The source checkout was `fef4cfd8b49fdd8617b7efb15bf960140bff1891`, observed at `2026-09-26T21:51:29.873306+00:00`, including working-tree material. Publication starts from `ecffd2af3623ff3e32318234fd51e1fac50b9126` so other local commits and research edits are not inadvertently published. The inventory distinguishes exact, changed and absent sources on that base. Resolve the correct bytes before execution and record any newer revision adopted.

At this snapshot, the cited reports record the following completed or bounded results. This list reports their scoped status; it does not certify every upstream proof anew.

- CA5-GNC-R's reciprocal barrier, fixed-U positive auxiliary solution, empty de Sitter scalar signs for finite q>0, finite-spectral joint U/Z existence, occupied velocity-matrix positivity and ultraviolet speeds already have calculations. Joint continuum existence and occupied finite-wavelength restoring/mixing stability remain open.
- The positive-threshold gate fails exact ungated matching for sufficiently weak sources. This is an operator mismatch on an open weak-source neighborhood, not an interface correction that another threshold scan removes.
- XC3 has static foliation vertices. XC4 has the actual nu_mono splice and discrepancy. XC5 and the filtered-zero-field report distinguish spatially smoothed force from square-root dependence on source amplitude. None is a full nonlinear evolution theorem.
- L386/L387 are recorded stopped; L388 is pending and L389 awaits its outputs in the inspected status. Reconcile current state before new execution. L390, DE3 and DE4 already have their scoped results.
- XR5 already compares the three static interior operators. Its distant-edge and topology findings motivate C13/C14; a generic repeat of the operator comparison adds little.
- The spectral inverse identities, boundary-flux identities, pressure integral identity, normalization counterfamilies and constant-pressure dust ambiguity already exist. C21–C30 ask about continuum use, observability and inference rather than re-deriving those identities.
- XR4 already has spherical Local Group turnaround, elementary external-field rescoring and filament arithmetic. C31–C34 require dynamics, geometry or actual observations beyond those calculations.

## Definitions and scientific boundaries

Use `nu_RAR(y)=1/(1-exp(-sqrt(y)))`, with `y=g_N/a0`, for the exact RAR comparison. The exact exponential AQUAL comparison uses `mu(x)=1-exp(-x)`, with `x=g/a0`; in spherical symmetry `g mu(g/a0)=g_N`. These are different implicit/explicit laws. In nonspherical and filtered settings their operators must be separately defined and varied.

The operative target is

```text
Delta u = 4 pi G rho_b
Delta Phi = 4 pi G rho_b
          + S* div[(nu_mono(|grad S u|/a0)-1) grad S u]
S = exp((xi^2/2) Delta)
```

The adjoint `S*` depends on the declared measure/domain. Do not replace it by a pointwise relation. Use the implemented nu_mono definition audited by XC4: the splice is near `y*=2.3374`, before the old phantom peak near `2.5396`; the reported maximum discrepancy is about `0.01037 dex`. The spec's older “below peak” and “0.01 dex” prose is not an exact numerical definition. C12 tests evolution through that splice; it does not ask to recompute those numbers.

For CA5 the new carrier/vacuum term is

```text
L_d = t K_d - W_exc/t - V0 F(t)
F(t) = 1 + (t + 1/t - 2)^2
t = 1 + Z - <Z>_h > 0
```

Here `t` is an auxiliary factor, not physical time. The rest of the action, including the gate, compensator, centered clock term and proper-volume projector, is essential and must be read from the pinned host and CA5 sources. There are five real classical carrier fields in this candidate. Their identification with a phenomenological particle/kick model has not been derived. V0 and the acceleration normalization are not predictions simply because the action contains them.

Criterion B allows leafwise instantaneous response and metric-superluminal channels but requires a global preferred time with no backward propagation/closed causal curve and a well-posed mixed evolution problem. Local well-posedness on a timelike-clock patch does not alone prove a global foliation or global causal completeness.

C21/C22/C26 use the separate CD26-2 spectral action. A spectral-lapse result is not automatically a CA5 result. C13–C20 and C31–C34 concern declared phenomenological constructions; their observational survival is necessary evidence for those constructions, not common-action certification.

## How another agent should execute one card

1. Claim one ID in its disjoint output directory. Record owner, branch, action/kernel, exact input hashes, assumptions, boundary conditions, intended tested range and intended output in `CLAIM.json`. Inform the coordinator of the claim; the initial queue is not an atomic multi-agent lock.
2. Resolve sources using [the source inventory](2026-09-26-astra-crispy-ideas.sources.json). If missing or stale, locate the exact local/archived copy or record a source blocker. Do not assume an absent source means its result was never done, and do not substitute a nearby action silently.
3. Write the first bounded derivation or executable calculation described by the card. Predeclare the numerical range, tolerances, likelihood, nuisance priors and falsification condition when applicable. For experimental bounds, retrieve the primary source and record its date/version.
4. Preserve code and exact commands, environment, input hashes, seeds, mesh/domain ranges, raw results and exit codes in `run_manifest.json`. Analytic work should instead state exact hypotheses, dependency lemmas and the unresolved implication, with a checkable derivation.
5. Obtain an independent check of the decisive equation or calculation. Write `RESULT.md` with the actual result, its limits, the surviving next implication and links to evidence. For numerical claims demonstrate convergence/error control relevant to the criterion, not a large unrelated test suite.
6. Report the bounded result under this ID. Do not edit upstream acceptance gates, restart L388/L389 or launch a large parameter scan as part of an unrelated card. Failures constrain the named domain/action; passing one card never establishes the actual universal theory of gravity.

Each card writes only under its listed directory by default. If a source correction is necessary, make it a separately reviewed change with affected dependencies identified. A changed action invalidates automatic inheritance of earlier health or observational results.

## First twenty: construction and empirical closure

### C01 Remove the activation dead zone while preserving the exact static target

**Lane / priority / method:** CA5 alternative / P0 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `dual`, `ca5`, `host` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C01/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The gated action already fails the ungated target on an open neighborhood of weak sources; another threshold scan cannot repair an operator mismatch.

**First calculation:** Define a separately named G(Y)=Y variant. Verify the affine Laplacian/compensator cancellation under the actual measure, then vary lapse, spatial metric, U and Z independently with the reciprocal source and volume projector retained.

**Completion criterion:** Obtain the required two potential equations as operator identities for arbitrary smooth weak sources, or isolate the unavoidable extra source/slip term and stop this ansatz.

**Controls and limits:** Use constant lapse and zero excitation as controls; send source amplitude to zero without dividing out the disputed term. Keep nu_mono, exact RAR and exact AQUAL as distinct branch definitions.


### C02 Finish the nonlinear constraint count

**Lane / priority / method:** CA5 / P0 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `ca5`, `host`, `occupied` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C02/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Frozen and homogeneous kinetic Hessians do not classify the nonlinear constraints or the clock exception.

**First calculation:** Keep the heat interval as an auxiliary boundary problem. Derive physical-time momenta, preserve primary constraints, and compute secondary brackets including proper-volume means, the Z shift redundancy and centered clock term.

**Completion criterion:** Give a constant-rank Dirac classification on a declared open domain, with the global mode separated and every tensor, clock and carrier degree of freedom counted.

**Controls and limits:** Recover the known frozen block; distinguish gauge zero modes from rank loss. A finite matrix or a choice of unitary gauge is not the full count.


### C03 Build a preferred-time evolution estimate

**Lane / priority / method:** CA5 / P1 / analytic.

**Task prerequisites:** C02, C05

**Read:** `ca5`, `host`, `xc5` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C03/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Criterion B permits leafwise instantaneous response but still requires a well-posed mixed evolution problem.

**First calculation:** Derive the complete reduced principal operator on one genuinely inhomogeneous timelike-clock background, including varied heat and projection terms. Seek a frequency-uniform symmetrizer or an elliptic-hyperbolic energy estimate in explicit function spaces.

**Completion criterion:** Establish a local existence/uniqueness/continuous-dependence route with a controlled estimate, or identify a specific defective mode or derivative loss.

**Controls and limits:** Check nonzero modes and global constraints separately. Superluminality relative to the metric alone is not a failure under the recorded criterion B.


### C04 Compute the dynamic mixed heat-filter vertex

**Lane / priority / method:** CA5/C-H-K scoped comparison / P1 / symbolic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `xc3`, `ca5`, `host` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C04/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** XC3's static foliation calculation does not give all metric-clock interactions on a moving background.

**First calculation:** Compute mixed metric-clock and second Duhamel variations of S_h when U_dot is nonzero. Retain hard-hard-to-soft momenta, eliminate constraints, and normalize the actual propagating mode before evaluating its cubic interaction.

**Completion criterion:** Bound the selected physical cubic channel on a declared background/momentum domain, or exhibit a low interaction scale; enumerate associated quartic terms still needed for full G8.

**Controls and limits:** Recover XC3's static limit and the prior heat divided-difference witness. Do not attach an exponential factor independently to every varied leg.


### C05 Lift the joint U/Z constraint theorem to the continuum

**Lane / priority / method:** CA5 / P0 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `dual`, `barrier` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C05/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Existence in each finite spectral space and heat injectivity do not supply estimates uniform in the cutoff.

**First calculation:** Use I''=E_g''+B*(F0'')^-1 B on its differentiability domain to seek cutoff-independent bounds exploiting the elliptic order of B. At D S_h U=0, use convex monotonicity/subgradient estimates rather than a nonexistent classical MOND Hessian. Control t's positive lower bound and compactness of both auxiliary sequences.

**Completion criterion:** Prove Galerkin convergence to a joint continuum solution and useful solution-map regularity, or produce an escaping sequence that identifies the failed bound.

**Controls and limits:** Recover the existing finite-space and fixed-U results without claiming them new. Test weak compactness against the nonlinear reciprocal terms.


### C06 Continue the physical auxiliary branch for both exact kernels

**Lane / priority / method:** exact RAR and exact AQUAL comparison / P1 / analytic/numerical.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `xc5`, `weighted`, `zero` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C06/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** An off-shell negative Hessian and a sufficient lapse-contrast bound do not determine the actual constrained solution branch.

**First calculation:** Start at a weak-contrast solution with a=D ln N. Continue lapse/metric constraints and the U equation together, separately for both exact laws; track the reduced Jacobian and normalize its gauge mode.

**Completion criterion:** Derive a branch-continuation domain or locate a genuine physical fold/zero eigenvalue with converged residuals.

**Controls and limits:** A lapse-adapted filter defines another action and needs its own variation. Do not relabel the old fixed-lapse counterexample as a physical instability.

**Additional prerequisites:** Name the exact action and filter placement separately for the RAR and AQUAL comparisons.


### C07 Derive occupied finite-wavelength cosmological stability

**Lane / priority / method:** CA5 / P0 / symbolic/ODE.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `occupied`, `ca5`, `frw` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C07/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The occupied velocity matrix and ultraviolet speeds are already positive; the finite-wavelength restoring/mixing sector remains open.

**First calculation:** Start with an actual single-mass expanding occupied solution and the coupled host/longitudinal sector. Canonically normalize the complete reduced action, retaining time derivatives of that normalization and q=k/a, and derive restoring and antisymmetric mixing matrices.

**Completion criterion:** Find a controlled perturbation-energy/growth bound through the filter scale, or a physical growing mode with rate compared with expansion.

**Controls and limits:** Recover the empty de Sitter and high-q limits and the already bounded transverse (chi,s) subsystem. The transverse finite-gain result does not complete this coupled calculation. Do not classify a negative instantaneous mass eigenvalue alone as catastrophic growth.


### C08 Resolve the simultaneous long-wave and empty-carrier limit

**Lane / priority / method:** CA5 / P1 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `occupied`, `ca5`, `frw` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C08/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Positivity for every finite q and excitation density need not be uniform as the expanding solution approaches their joint boundary.

**First calculation:** Insert the proved homogeneous dilution into D_R=alpha_e q^2+2r(1-r)rho_exc/M_P^2. Study competing limit paths, the constraint variables and the exactly homogeneous mode.

**Completion criterion:** Produce a uniform physical norm and matching rule to the global mode, or identify loss of control and its observable/dynamical consequence.

**Controls and limits:** Vanishing coefficients can be variable artifacts. Compare gauge-invariant perturbations and cubic normalization before claiming strong coupling.


### C09 Test actual uniqueness at homogeneous zero field

**Lane / priority / method:** target-preserving comparison / P1 / analytic.

**Task prerequisites:** C01

**Read:** `zero`, `xc5`, `ca5` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C09/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Square-root source dependence defeats one Osgood argument but does not prove dynamical nonuniqueness.

**First calculation:** For a successful target-preserving variant, derive the constrained evolution near the homogeneous zero-field state. First test whether a proposed lowest-mode ansatz is invariant under the nonlinear flux; if not, label its truncation a Galerkin diagnostic and pursue monotonicity or conserved-energy estimates for the full evolved variables.

**Completion criterion:** Prove uniqueness in the declared state space or construct two admissible solutions with identical initial data; otherwise name the missing estimate.

**Controls and limits:** The square-root flux generally generates higher harmonics: uniqueness or nonuniqueness of a truncation is not a continuum result without an invariant reduction or justified limit. Carry the exact comparison kernels separately and preserve both spatial force smoothing and nonsmooth source dependence.

**Additional prerequisites:** C01 must supply an actual target-preserving action; failure there blocks this proposed reduction until an alternative is defined.


### C10 Make the positive-domain barrier invariant under evolution

**Lane / priority / method:** CA5 / P1 / analytic.

**Task prerequisites:** C02, C03, C05

**Read:** `barrier`, `frw`, `ca5` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C10/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The fixed-data lower bound for t depends on geometric and source quantities that themselves evolve.

**First calculation:** Differentiate the barrier's controlling norms along the reduced equations, including N_min, the divergence of N(a-DU), carrier norms and timelikeness X.

**Completion criterion:** Prove a continuation criterion for a declared small-data class preserving t>0, positive lapse and a timelike clock, or identify the first uncontrolled norm.

**Controls and limits:** Do not request nonsingular evolution for arbitrary self-gravitating data. The homogeneous future-global theorem is a benchmark, not this result.


### C11 Define the isolated-source limit of the projected CA5 action

**Lane / priority / method:** CA5 / P1 / analytic.

**Task prerequisites:** C05

**Read:** `host`, `dual`, `zero` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C11/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Compact proper-volume means and a global spectral gap cannot simply be carried to an isolated MOND tail.

**First calculation:** Exhaust an expanding or asymptotically specified geometry by large compact leaves. Derive limits of the Z projector, centered clock term, global constraint and filtered force in weighted spaces.

**Completion criterion:** Obtain a boundary prescription with physical force independent of the chosen exhaustion, or exhibit dependence that requires new boundary data.

**Controls and limits:** Test two different exhaustion shapes and a compact source with the same asymptotic background. Keep the constant mode explicit.


### C12 Evolve through the actual nu_mono splice

**Lane / priority / method:** nu_mono / P1 / analytic/numerical.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `xc4`, `xc5`, `xc3` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C12/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The splice location and C2-not-C3 regularity are already calculated; dynamics across the moving splice is not.

**First calculation:** Formulate the variation and energy estimate for a background crossing y*=2.3374, retaining one-sided constitutive derivatives and the moving crossing set.

**Completion criterion:** Establish an energy/constraint estimate or converged weak evolution for the specified kernel, or identify a precise regularity obstruction.

**Controls and limits:** If a smooth maximum is used as a numerical regularizer, prove a regulator limit; do not silently replace the kernel or infer a cubic Taylor coefficient that does not exist.


### C13 Resolve the distant-edge bias in actual 3-D Harvey maps

**Lane / priority / method:** phenomenological carrier / P1 / grid.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `l370`, `xr5`, `xr5report` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C13/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** XR5 already controls static interior differences but finds a distant-edge projection artifact comparable with the historical Harvey margin.

**First calculation:** Vary 3-D resolution, subcell translation, line of sight and box size for all three estimators. Include the entire compensated region and a smooth-edge reference.

**Completion criterion:** Measure a numerical error smaller than the distance to the adopted beta=+0.10 gate; target |delta beta|<0.002 as a declared numerical goal, otherwise report unresolved sign.

**Controls and limits:** Do not delete inconvenient edge mass to obtain a pass. The 2-D artifact is a warning to test, not evidence that the 3-D code has the same error.

**Additional prerequisites:** Use a frozen control configuration initially; reconcile the existing L388/L389 candidate before a final model score.


### C14 Follow region connectivity through a two-halo merger

**Lane / priority / method:** phenomenological region action / P1 / grid/analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `xr5`, `l361`, `l370` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C14/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Manual relabeling can reverse the phantom pull; the topology selected by a real transition remains untested.

**First calculation:** Approach and separate two halos across the connectivity threshold with finite screening and a resolved neck. Track force, field energy, interface terms and work over the cycle.

**Completion criterion:** Find a convergent transition and energy ledger, or demonstrate a finite force jump/cycle-work artifact requiring a different dynamical interface rule.

**Controls and limits:** State contrast versus absolute-density masks explicitly. Do not repeat the already completed static interior-operator comparison.


### C15 Transport retention to the merger epoch

**Lane / priority / method:** phenomenological carrier / P1 / simulation successor.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `l388`, `l389`, `l373` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C15/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The relevant merger epoch is z=0.4; replacing its retention by z=0 can change a marginal score.

**First calculation:** After reconciling existing L388/L389 work, extract or add z=0.4 checkpoints at the same gate, kick and footing. Retain per-halo mass-bin distributions and re-score the merger.

**Completion criterion:** Quantify the bias from z=0 substitution and the same-epoch margin in every estimator with realization scatter.

**Controls and limits:** Do not launch duplicate L388/L389 jobs. If fields were not retained, record that a new checkpointed run is necessary; never substitute another mass bin silently.

**Additional prerequisites:** Reconcile existing L388/L389 jobs and artifacts; do not start duplicate jobs. New checkpointed output is needed if z=0.4 distributions were not saved.


### C16 Predict merger-core shapes from phase-space evolution

**Lane / priority / method:** phenomenological carrier / P1 / simulation.

**Task prerequisites:** C15

**Read:** `l375`, `l376`, `l371` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C16/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A halo-wide retained mass does not select the imposed S1/S2/S3 core shape.

**First calculation:** Evolve representative cluster assembly histories for the selected kick and gate, retaining f(r,v,z=0.4), infall and recapture. Project those profiles into the existing lensing estimator.

**Completion criterion:** Measure converged carrier mass within 150 kpc and the resulting beta distribution, identifying whether the joint candidate survives without choosing a convenient shape.

**Controls and limits:** Keep the phenomenological kick assumption explicit. Test identical mass with distinct assembly histories and do not tune core shape to the observed centroid.

**Additional prerequisites:** Require a declared kick/gate candidate and epoch-matched mass normalization; halo-wide mass retention is insufficient.


### C17 Measure clearing in a frame that follows the galaxies

**Lane / priority / method:** phenomenological carrier / P1 / checkpointed simulation.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `xr2`, `l388`, `l377` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C17/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Fixed spatial cells may confuse baryon displacement with carrier evacuation; existing saved arrays may not contain the needed labels.

**First calculation:** Add baryon identities/selection checkpoints to one planned successor. Evaluate fixed-cell, baryon-normalized, model-selected and Lagrangian estimators with per-box numerator/denominator sums.

**Completion criterion:** Quantify where the clearing conclusion changes across estimators and environments, retaining the recorded 0.30 gate as a labeled original criterion.

**Controls and limits:** Do not silently substitute an acceptance statistic. Particle identities correct displacement/selection bias, not spatial resolution: the cited PM mesh is about 193 kpc physical at z=2 versus the flagship's 5.4-kpc effective radius. This task tests a halo-scale clearing proxy; an inner-galaxy conclusion needs a resolved bridge such as L376. Distinguish absent output from postprocessing.

**Additional prerequisites:** Acquire baryon identities and matched field checkpoints in a planned successor run; existing committed outputs may be insufficient.


### C18 Solve the flagship's resolved carrier-CGM window

**Lane / priority / method:** phenomenological static/halo / P1 / radial then disc.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `de4`, `l376` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C18/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** DE4's matter-only test is done; its result still depends on prescribed carrier and outer-baryon profiles.

**First calculation:** Replace S times NFW by an evolved carrier profile and the outer-tail proxy by a finite-thickness disc plus a declared CGM family. Solve for the allowed CGM density and retained core mass together.

**Completion criterion:** Determine whether an interval satisfies both activation at r_F and |delta log BTFR|<=0.10 across 10^10-10^11 solar masses, z=2-3 and both footings.

**Controls and limits:** Include the CGM's gravity and independently constrained baryon budget. Recover DE4's special case, and report profile dependence rather than fitting arbitrary CGM to save the gate.

**Additional prerequisites:** Provide an evolved carrier profile and independent constraints on the declared CGM family; exploratory profile controls alone do not finish this task.


### C19 Match the resolved-halo trigger to the PM trigger

**Lane / priority / method:** phenomenological carrier / P1 / radial/simulation.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `l390`, `l375`, `l377` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C19/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** L390's completed pass still uses a different trigger and a canonical-footing mass fit.

**First calculation:** Include the selected switched nu_mono phantom in the resolved decay trigger, evolve the profile, and refit baryonic masses independently on both footings before rescoring KiDS.

**Completion criterion:** Determine whether the previously adopted delta chi2<=+4 criterion survives on each footing after the trigger and fitting conventions match.

**Controls and limits:** Reproduce L390's original assumptions as a control and retain a no-decay rejection. This is a changed physical calculation, not a rerun of its completed pass.

**Additional prerequisites:** Match the canonical PM gate/phantom prescription. Label the alternative-footing resolved calculation separately until compatible PM evolution exists; the inspected L388/L389 stages evolve the canonical footing only.


### C20 Compute lensing cross-power from coevolved fields

**Lane / priority / method:** phenomenological carrier / P1 / matched-field statistics.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `de3`, `l388`, `l377` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C20/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The existing shear gate combines PM transfer and a separately constructed phantom mock/correlation.

**First calculation:** Measure P_mm, P_m,ph and P_ph,ph from matched evolved snapshots on a small redshift grid, then form the total lensing power and project it into shear bins.

**Completion criterion:** Determine whether the imported correlation changes the sign of the recorded margin; report the old R(k)<=1.2 proxy separately from any survey likelihood.

**Controls and limits:** Require identical Fourier conventions, windows and noise subtraction. Do not treat DE3's completed threshold export as this new cross-power calculation.

**Additional prerequisites:** Acquire coevolved matter and phantom fields at matching epochs with a declared lensing operator; a transfer-function table alone is insufficient. The inspected PM runs use the canonical footing; an alternative-footing claim needs its own compatible evolution.


## Another twenty: inference, external tests and deeper theory

### C21 Turn spectral reduction into a continuum local theorem

**Lane / priority / method:** CD26-2 spectral route / P1 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `spectral`, `inverse` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C21/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Positive finite-dimensional Dirac algebra and an isolated ground state do not yet define a differentiable continuum Hamiltonian vector field.

**First calculation:** Choose a sufficiently small Sobolev neighborhood of the exact cosine solution on a compact leaf. Estimate the normalized eigenpair map, its projected inverse and functional derivatives with respect to metric, momentum and source, including volume variation.

**Completion criterion:** Produce compatible spaces and a controlled local vector field/existence argument, or isolate the exact derivative loss or missing estimate.

**Controls and limits:** This is a separate spectral action, not a CA5 result. Another finite matrix bracket check does not complete it.


### C22 Establish the noncompact spectral lapse domain

**Lane / priority / method:** CD26-2 spectral route / P2 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `inverse`, `spectralresult` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C22/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The torus spectral gap does not settle the spectral route's asymptotically cosmological lapse problem.

**First calculation:** For a spherical compact source perturbation of a homogeneous expanding background, specify lapse asymptotics, weighted function spaces, normalization and the inverse boundary problem.

**Completion criterion:** Construct a positive root with a controlled inverse, or a threshold resonance, flux incompatibility or normalization obstruction on this declared domain.

**Controls and limits:** Do not import the compact Poincare gap. C11 concerns the CA5 projector; this task concerns the distinct spectral lapse equation.


### C23 Quantify finite-region inverse boundary uncertainty

**Lane / priority / method:** spectral inverse / P2 / analytic/numerical.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `inverse` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C23/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The completed boundary-flux identities do not quantify boundary-conditioned reconstruction error when interior lapse observations are partial or noisy.

**First calculation:** On one ball or interval, specify partial/noisy lapse and geometry measurements and a boundary-conditioned reconstruction estimator. Derive its boundary-to-inferred-residual uncertainty map under Dirichlet, flux and matched-exterior prescriptions with declared uncertainty norms.

**Completion criterion:** Bound the apparent vacuum-coefficient residual attributable to boundary-conditioned reconstruction uncertainty, or demonstrate that the declared incomplete observations cannot distinguish it from a genuine variation.

**Controls and limits:** With exact full interior lapse/geometry at fixed A, every admissible solution obeys J=A/b regardless of its boundary values: retain this zero-effect control. Do not prescribe Dirichlet and Neumann data independently on one elliptic problem or claim the exact pointwise inverse itself depends on unmeasured boundary values.


### C24 Determine whether the lapse inverse is observable

**Lane / priority / method:** spectral inverse / P1 / analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `inverse`, `recipe` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C24/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A formal lapse field is not automatically an observable relative to the physical clock foliation.

**First calculation:** In a weak cosmological patch, derive the forward map from metric and clock perturbations to clock-rate ratios, redshifts and travel times. Test identification of J=-4 Delta(sqrt(N))/sqrt(N), including physical length calibration.

**Completion criterion:** Give an identifiable observable combination and its residual degeneracies, or two admissible configurations with identical proposed measurements but different J.

**Controls and limits:** Separate coordinate freedom from changes in the physical clock. Expansion history alone must fail the spatial-profile control.


### C25 Build a noise-controlled lapse inverse estimator

**Lane / priority / method:** spectral inverse / P2 / inference.

**Task prerequisites:** C23, C24

**Read:** `inverse` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C25/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Exact inversion and a warning about differentiated noise do not supply a calibrated finite-resolution test.

**First calculation:** Linearize J about the exact cosine profile and propagate a specified correlated noise/geometry covariance. Compare a weak-form residual with direct differentiation, including boundary uncertainty from C23.

**Completion criterion:** Recover a predeclared nonconstant-vacuum injection with calibrated uncertainty while retaining the constant-vacuum control, or quantify the unresolved amplitude at the tested resolution.

**Controls and limits:** Use synthetic data first and label them. Set injection amplitudes, resolution sequence and coverage target before inspecting recovery.

**Additional prerequisites:** C23/C24 must establish a usable boundary and observable model, or mark the forecast explicitly hypothetical.


### C26 Test inverse rank along an admissible history

**Lane / priority / method:** CD26-2 spectral inverse / P1 / analytic/ODE.

**Task prerequisites:** C21, C24

**Read:** `inverse`, `spectral` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C26/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Three independently chosen slices with rank three do not establish identifiability along a constrained physical history.

**First calculation:** Construct one controlled local spectral trajectory obeying source conservation and momentum constraints. Compute the sensitivities of (1/ell,b,Lambda_bar) at three times, projecting ordinary-source normalization and geometric scale nuisances.

**Completion criterion:** Find full rank on a nonempty admissible domain, or derive the surviving physical null direction and its consequence for inference.

**Controls and limits:** Specify the trajectory's local validity interval. Do not choose independent observation rows by hand or use a CA5 background with the spectral action's inverse equation.

**Additional prerequisites:** Use a trajectory justified by C21 or an independently audited local existence result for the same spectral action.


### C27 Turn the integral pressure identity into a likelihood

**Lane / priority / method:** pressure-promotion hypothesis / P1 / inference.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `pressure`, `scales` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C27/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The integral identity exists; its ability to distinguish pressure promotion from density promotion with correlated data has not been tested.

**First calculation:** Build a two- or three-bin likelihood for [a^3 H^2]_i^j = B integral_i^j a^2 a0(a)^2 da, marginalizing one common B. Propagate galaxy-distance/expansion cross-covariance and curvature/ordinary-pressure corrections.

**Completion criterion:** Measure predeclared discrimination power on paired synthetic pressure and density histories sharing today's normalization, or show that the stated precision cannot discriminate.

**Controls and limits:** Define a as dimensionless scale factor and verify units of B. Do not differentiate noisy H data or count the already derived identity as a new result.


### C28 Separate running couplings from pressure evolution

**Lane / priority / method:** pressure-promotion hypothesis / P2 / analytic/inference.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `pressure`, `scales` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C28/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A changing pressure-law residual can also reflect changing kappa^2/g; a fit alone does not identify which changed.

**First calculation:** Choose bounded parameterizations for kappa(a), g(a) and stress history within one declared action. Rederive its background equations, including derivative terms from varying gravitational coefficients, before forming the sensitivity matrix with an independently derived coupling observable and calibration nuisances.

**Completion criterion:** Identify an independent direction separating stress evolution from coupling drift, or display the exact surviving null direction and state nonidentifiability.

**Controls and limits:** Do not insert varying constants into a fixed-coupling Einstein-form identity. If derivative terms are absorbed into effective stress, state the changed meaning of pressure evolution. Constant couplings are a nested control; horizon size, curvature and temperature reexpressions of one scale are not independent observations.

**Additional prerequisites:** Derive an independent coupling observable from the selected action before claiming coupling/stress separation.


### C29 Disentangle filter length from inferred a0 evolution

**Lane / priority / method:** filtered framework / P1 / radial/inference.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `pressure`, `recipe`, `host` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C29/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A redshift-dependent filtered galaxy response can reflect the heat length or source-size distribution as well as a0.

**First calculation:** For two baryonic profiles with distinct physical sizes, differentiate the full source-to-force operator with respect to (a0,xi). Compare fixed proper xi with fixed comoving xi, retaining distance and mass nuisances.

**Completion criterion:** Identify source sizes/radii with independent sensitivities after nuisance projection, or show a concrete degeneracy in an a0(z)-only inference.

**Controls and limits:** Do not use the retired pointwise RAR inverse. Freeze a named action/kernel; a CA5 calculation uses its actual static equation and retains its known target mismatch.


### C30 Break or bound the constant-pressure dust ambiguity

**Lane / priority / method:** one declared common action / P1 / linear perturbations.

**Task prerequisites:** C07

**Read:** `pressure`, `gateclock`, `occupied` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C30/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The background family epsilon=Pi0+D a^-3 leaves the excitation constant D free; the pressure identity alone cannot measure it.

**First calculation:** Within one declared common action, verify the applicable constant-pressure limit and compare two admissible states with the same tension and different excitation. Derive one growth, lensing or clock-response transfer difference, retaining initial-condition freedom.

**Completion criterion:** Find a nonzero observable difference not absorbed by allowed initial amplitudes/calibrations, or prove that this observable leaves D unidentified.

**Controls and limits:** If CA5 does not realize the assumed exact dust background, quantify the controlled approximation first. Do not assign a sound speed by hand or import the old polar-clock dispersion.

**Additional prerequisites:** For the CA5 route use C07; another action requires its own perturbation derivation and separate claim label.


### C31 Compute the Local Group's anisotropic turnaround surface

**Lane / priority / method:** phenomenological region model / P2 / trajectory integration.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `lg`, `l361`, `xr4` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C31/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The spherical turnaround tension is already known; it does not calculate the observed angularly selected two-body surface.

**First calculation:** Evolve MW/M31 baryonic regions and their separation with a declared surrounding field. Integrate test trajectories, extract the zero-radial-velocity surface and forward-model angular and distance selection.

**Completion criterion:** Determine whether the selected R0 enters the repository's +/-0.10-dex comparison band while remaining in the chosen gate cell, including mass/distance uncertainty.

**Controls and limits:** Recover the coincident spherical control. Fix source priors before scoring and distinguish modeled selection from actual catalog selection.

**Additional prerequisites:** Freeze catalog selection and baryonic-source uncertainty before a data verdict.


### C32 Solve the disc external-field response in three dimensions

**Lane / priority / method:** phenomenological region model / P2 / elliptic grid/inference.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `disc`, `efe`, `l361` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C32/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The scalar-sum and subtraction rescoring is complete; its ambiguity remains unresolved by a true disc field solution.

**First calculation:** Solve a finite-thickness disc plus a measured in-region baryonic external field at several orientations with the declared boundary operator. Average using a stated orientation/selection distribution and refit the existing residual slopes and zero points.

**Completion criterion:** Resolve whether the full vector/curl response changes the previous empirical verdict, with grid, boundary and orientation convergence.

**Controls and limits:** Recover isolated-disc and weak-field limits. Do not choose the favorable scalar external-field prescription after seeing the data.

**Additional prerequisites:** Acquire the external baryonic field and declare its uncertainty; a prescribed field only supports a conditional prediction.


### C33 Evolve the gas response of an active low-redshift filament

**Lane / priority / method:** phenomenological region model / P2 / hydrodynamics.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `filament`, `forest`, `xr4` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C33/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Static filament activation arithmetic does not predict gas density, temperature or observable absorption after backreaction.

**First calculation:** Evolve one resolved filament from z=1 to 0 with matched initial conditions for the chosen model and its Newtonian control. Save density, temperature and velocity and synthesize Ly-alpha and tSZ profiles.

**Completion criterion:** Measure whether the force enhancement survives gas evolution and yields a converged observable difference, or is absorbed by the modeled thermal/feedback uncertainty.

**Controls and limits:** Declare cooling/heating and boundary assumptions. A forecast without actual data and covariance is not an observational exclusion.


### C34 Predict cluster gas pressure before scoring the real tSZ map

**Lane / priority / method:** phenomenological carrier/region model / P2 / gas model/inference.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `tsz`, `xr4`, `l321` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C34/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The old synthetic-self comparison and phantom-only slope window do not test the current carrier-plus-phantom construction against the real map.

**First calculation:** Use L321's X-COP gas/mass inputs as a starting control, then solve the selected current cluster-carrier-plus-phantom gas/pressure profile. Freeze the aperture/slope prediction before fitting real map cutouts, with beam, mask, background and covariance controls.

**Completion criterion:** Report an actual residual/likelihood with nuisance sensitivity and a matched baseline, or a specific missing calibration that prevents a data score.

**Controls and limits:** Verify map units and provenance before use; do not relabel synthetic validation as a data fit. L321's older kernel/EFE and retention prescription are controls, not the current construction. Supply the selected current cluster carrier profile without borrowing a chosen merger-core shape.

**Additional prerequisites:** Check the local map identified by XR4, its provenance/units, the selected gas prior and covariance; map data are not bundled here.


### C35 Derive the physical-metric post-Newtonian parameters

**Lane / priority / method:** frozen CA5 or C01 variant / P1 / analytic.

**Task prerequisites:** C02

**Read:** `ca5`, `host`, `ppn` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C35/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A reduced frozen preferred-frame calculation does not determine the full action's measured-G post-Newtonian response.

**First calculation:** Derive the slow moving-source near-zone solution on a declared nonzero background, retaining the reciprocal source, projection and gate. Match the physical metric to measured G_N, beta, gamma and the preferred-frame parameters.

**Completion criterion:** Obtain the parameters on a controlled domain and compare with primary experimental likelihoods, or isolate the obstruction to the near-zone expansion.

**Controls and limits:** Freeze CA5 or a named successful C01 variant and recheck transferred constraints. Recover the prior reduced limit only as a control; a failure in that family is not a universal no-go.

**Additional prerequisites:** If adopting a C01 variant, rerun/transfer-audit C02 on that exact action. Retrieve primary observational sources at execution time.


### C36 Propagate tensor waves through an activated interface

**Lane / priority / method:** CA5 / P1 / analytic/wave packet.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `ca5`, `host`, `xc3` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C36/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A homogeneous tensor-cone result does not control propagation through a spatially varying activated region.

**First calculation:** Derive the constrained tensor and mixed principal operator on a smooth nonzero-gate background, retaining filter/metric variations. Propagate a small packet across the interface and track flux, mode conversion and physical arrival time.

**Completion criterion:** Bound the physical tensor speed, reflection/conversion and energy on the declared background class, or identify a concrete pathology.

**Controls and limits:** Use the actual matter metric. Recover the homogeneous limit and distinguish a time delay from a change in front speed; criterion B still applies to non-tensor modes.

**Additional prerequisites:** Supply an admissible inhomogeneous background and control constraint mixing; a prescribed off-shell interface is only a diagnostic.


### C37 Calculate nonlinear charge conversion with halo backreaction

**Lane / priority / method:** CA5 / P1 / nonlinear simulation.

**Task prerequisites:** C05, C07

**Read:** `conversion`, `pump`, `ca5` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C37/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The linear pump bound and small packet conversion do not establish useful carrier evacuation from a self-gravitating halo.

**First calculation:** Evolve a small controlled halo with the action's carrier conversion, pump depletion, self-gravity and auxiliary solve. Track charge and energy fluxes across a declared outer boundary and the retained radial mass.

**Completion criterion:** Measure achievable evacuation and its energy budget before backreaction shuts off conversion, with convergence and conserved-charge controls; compare only against a separately derived phenomenological requirement.

**Controls and limits:** Do not inject a random kick or impose a desired cleared fraction. Use C16/C18 only to define a labeled target, never to claim their particle surrogate is the same action.

**Additional prerequisites:** C05/C07 provide prerequisites, not a nonlinear evolution theorem; verify the numerical problem and domain before expensive runs.


### C38 Derive early-universe coldness and excitation transfer

**Lane / priority / method:** CA5 / P1 / averaging/linear ODE.

**Task prerequisites:** C07, C08

**Read:** `occupied`, `frw`, `ca5` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C38/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** A late homogeneous solution and healthy ultraviolet modes do not show that occupied carriers have the required early-universe transfer behavior.

**First calculation:** On a declared radiation-to-matter background, derive rather than assume the rapid-oscillation averaged pressure, anisotropic stress and perturbation equations of the five real carrier fields, with ordinary radiation/baryons and auxiliaries included.

**Completion criterion:** Quantify the domain of cold behavior, isocurvature response and transfer-scale departures over a finite linear interval, or exhibit failure of the averaging hierarchy.

**Controls and limits:** Check against unaveraged evolution on an overlap interval. Do not claim a CMB fit from background agreement or identify the classical fields with an extra particle population.

**Additional prerequisites:** Add the ordinary radiation/baryon sector consistently and verify the background solves the selected action over the tested interval.


### C39 Compute sourced radiation of the counted non-tensor modes

**Lane / priority / method:** frozen common action / P1 / analytic.

**Task prerequisites:** C02, C35

**Read:** `ca5`, `host`, `ppn` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C39/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** Counting modes and checking static preferred-frame parameters does not determine their radiative coupling to a binary.

**First calculation:** Begin with a weakly self-gravitating binary within the near-zone domain from C35. Match its sourced constrained solution to outgoing preferred-time modes and derive leading energy flux, including dipole/quadrupole terms when present.

**Completion criterion:** Obtain a finite, consistently signed leading flux with an explicit regime of validity, or prove decoupling of the proposed radiative channel.

**Controls and limits:** Separate instantaneous constraints from radiative degrees of freedom. Compact-star sensitivities and a pulsar-data constraint require further justified strong-field work; do not import them by analogy.

**Additional prerequisites:** C02 and C35 must refer to the same frozen action, background domain and physical metric.


### C40 Test the reciprocal barrier's radiative stability as an EFT

**Lane / priority / method:** optional quantum extension / P3 / one-loop analytic.

**Task prerequisites:** None within this queue; source and physical-input prerequisites still apply.

**Read:** `ca5`, `barrier`, `host` (paths in the source table).

**Write:** `real_research/astra_crispy_ideas/C40/` (`CLAIM.json`, `RESULT.md`, derivation/code, `run_manifest.json`).

**Open arrow:** The classical reciprocal barrier has specially vanishing low derivatives; its preservation under a proposed quantization is a separate question.

**First calculation:** Declare a Wilsonian quantization, cutoff and counterterm prescription. Compute the carrier determinant in an explicitly off-shell local constant-t background, then restore t=1+P_h Z and the full measure before varying. Extract induced local derivatives and the actual susceptibility of admissible mean-zero auxiliary perturbations about t=1.

**Completion criterion:** Identify protected relations or the counterterms/tuning required for the projected physical perturbations in the stated finite cutoff regime, with regulator, normalization and off-shell-extension dependence explicit.

**Controls and limits:** A spatially constant physical t on a compact projected leaf is necessarily one; do not treat arbitrary constant t as an admissible cosmology. This is optional quantum EFT work. F(t)=F(1/t) alone is not a full kinetic-action symmetry, and no observed vacuum normalization or ultraviolet completion follows.

**Additional prerequisites:** Explicitly adopt a quantum EFT extension; the classical construction alone does not require this calculation.


## Source paths and publication availability

These are repository-relative paths into the observed source checkout, not a claim that every file is present on this documentation branch. SHA256 values, observed time and tracked/untracked status are in [the machine-readable inventory](2026-09-26-astra-crispy-ideas.sources.json). “Exact at base” refers to the pinned publication base, not to a moving remote main.

| Source key | Repository path | Availability |
| --- | --- | --- |
| `spec` | `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` | Exact at base |
| `recipe` | `qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md` | Different at base |
| `ca5` | `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md` | Absent at base |
| `barrier` | `real_research/breakthrough_review_2026_09_26/vacuum/BARRIER_PROOF.md` | Absent at base |
| `dual` | `real_research/breakthrough_review_2026_09_26/static/DUAL_AUXILIARY.md` | Absent at base |
| `occupied` | `real_research/breakthrough_review_2026_09_26/occupied/RESULT.md` | Absent at base |
| `host` | `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` | Absent at base |
| `frw` | `real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md` | Absent at base |
| `conversion` | `real_research/common_action_2026_09_26/transport/CONVERSION.md` | Absent at base |
| `pump` | `real_research/breakthrough_review_2026_09_26/transport/RESULT.md` | Absent at base |
| `zero` | `real_research/closure_push_2026_09_26/filtered_zero_field/RESULT.md` | Absent at base |
| `xc3` | `real_research/extra_crispy_2026/XC3_filter_foliation_vertices.py` | Different at base |
| `xc4` | `real_research/extra_crispy_2026/XC4_nu_mono_splice.py` | Absent at base |
| `xc5` | `real_research/extra_crispy_2026/XC5_lapse_weighted_convexity.py` | Exact at base |
| `weighted` | `real_research/closure_doors_2026_09_26/auxiliary/LAPSE_VARIATION.md` | Absent at base |
| `xr5` | `real_research/cross_thread_review_2026_09_26/XR5_operator_identity.py` | Absent at base |
| `xr5report` | `real_research/cross_thread_review_2026_09_26/XR5_README.md` | Absent at base |
| `l361` | `real_research/g03_audit_2026/L361_bound_region_kernel.py` | Exact at base |
| `l370` | `real_research/merger_infall_2026/L370_boosted_infall_mergers.py` | Exact at base |
| `l371` | `real_research/merger_infall_2026/L371_harvey_slow_kick_carrier.py` | Exact at base |
| `l373` | `real_research/merger_infall_2026/L373_two_mode_carrier_pm.py` | Absent at base |
| `l375` | `real_research/dark_sector_2026/L375_triggered_carrier_galaxy_retention.py` | Exact at base |
| `l376` | `real_research/dark_sector_2026/L376_triggered_carrier_inner_galaxies.py` | Exact at base |
| `l377` | `real_research/dark_sector_2026/L377_full_construction_pm.py` | Exact at base |
| `l388` | `real_research/dark_sector_2026/L388_linear_gate_pooled.py` | Absent at base |
| `l389` | `real_research/dark_sector_2026/L389_harvey_same_cell_linear_gate.py` | Absent at base |
| `l390` | `real_research/dark_sector_2026/L390_kids_resolved_linear_gate.py` | Exact at base |
| `xr2` | `real_research/cross_thread_review_2026_09_26/XR2_fixed_cell_review.md` | Absent at base |
| `de3` | `real_research/dark_energy_2026/DE3_tmax_at_linear_gate.py` | Exact at base |
| `de4` | `real_research/dark_energy_2026/DE4_flagship_matter_only_switch.py` | Exact at base |
| `spectral` | `real_research/closure_push_2026_09_26/lapse_kinetic/SPECTRAL_REDUCTION_AUDIT.md` | Absent at base |
| `spectralresult` | `real_research/closure_push_2026_09_26/spectral_lapse/RESULT.md` | Absent at base |
| `inverse` | `real_research/dark_energy_inverse_2026_09_26/spectral_inverse/REPORT.md` | Absent at base |
| `pressure` | `real_research/dark_energy_inverse_2026_09_26/reconstruction/RESULT.md` | Absent at base |
| `scales` | `real_research/dark_energy_inverse_2026_09_26/scales/REPORT.md` | Absent at base |
| `gateclock` | `real_research/dark_energy_inverse_2026_09_26/gates_clock/RESULT.md` | Absent at base |
| `lg` | `real_research/cross_thread_review_2026_09_26/XR4_lg_zero_velocity_construction.py` | Absent at base |
| `efe` | `real_research/cross_thread_review_2026_09_26/XR4_efe_under_region_kernel.py` | Absent at base |
| `disc` | `hunt_2026/f16_curl_field_fork_on_discs.py` | Exact at base |
| `filament` | `real_research/cross_thread_review_2026_09_26/XR4_filament_gate_arithmetic.py` | Absent at base |
| `forest` | `real_research/g03_audit_2026/L347_switch_forest_flux_power.py` | Exact at base |
| `tsz` | `deepseek_push/Z06_tsz_pull.py` | Exact at base |
| `xr4` | `real_research/cross_thread_review_2026_09_26/XR4_data_gates.md` | Absent at base |
| `ppn` | `real_research/khronon_momentum_2026/KM3_chk_one_pn.py` | Exact at base |
| `l321` | `real_research/dark_sector_2026/L321_carrier_z0_retention_gate.py` | Exact at base |

## Suggested sequencing

Run C01, C02, C05 and C07 independently on explicitly fixed candidates. If C01 changes the action successfully, repeat or transfer-audit C02/C05/C07 for that action before combining their claims. C03 then needs the compatible constraint count and auxiliary estimates; C10 adds a small-data continuation criterion. C04/C08/C12 probe interaction, limit and regularity obstructions.

In the empirical lane, C13/C14 can start with frozen controls while existing L388/L389 work finishes. C15 transports the selected candidate to the right epoch; C16 then replaces selected merger-core shapes. C17/C20 need checkpoint design before a successor run. C18/C19 test remaining resolved-profile and trigger assumptions.

C21 and C24 are independent starting points for the spectral/inverse lane. C25 needs C23/C24; C26 needs a justified trajectory and measurement map. C27 can start with declared synthetic histories. C28/C29/C30 distinguish rival interpretations before an apparent pressure-law fit is given physical meaning.

C35/C36/C39 connect the common action to near-zone and radiative observables. C37/C38 test actual carrier dynamics. C40 is a lower-priority optional quantum extension and does not block a classical construction.

## Closing a card honestly

Use a verdict such as `established-on-stated-domain`, `counterexample-to-stated-claim`, `numerically-supported-on-tested-range`, `inconclusive`, or `blocked-on-input`. State the action revision and the exact range next to that verdict. Report an unknown as unknown, and keep all forty task statuses proposed until actual work is recorded.
