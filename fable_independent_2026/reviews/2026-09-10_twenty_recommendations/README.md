# Twenty recommendations on Claude's recent gravity work

Review date: 2026-09-10. Requested by Carl Zimmerman. Review by Codex.

**Outcome: useful progress, not a complete theory.** Preserve the actual CLASS/CAMB work and the L153 correction of the earlier fluid interpretation. Correct the universal barotropic growth-ceiling claim before using it to exclude architectures. The highest-value next computation is the **coupled clock–field–metric perturbation system from one frozen action**, not another free-fluid parameter scan.

## Scope and evidence

Read-only review of selected load-bearing source sections and recorded outputs, initially through `a4c65ad67f23d8df8f3688a4c1d7a5ce4e87b83a`, extended through `20c27011f817eab420d11ec3e5e37a66ec4987a1`. Key later commits: `47051f911` (L153), `782ccbd4f` (L155), `20c27011f` (L165). This is not a review of every intervening commit or every file in the repository.

The companion [algebra check](check_review_algebra.py) independently differentiates the counterexample below, checks its local growth rate and conditions, and verifies a normalization identity. Its [recorded output](CHECK_OUTPUT.json) includes source hashes. CLASS/CAMB and Lean were **not rerun** in this review; their stored outputs are reported as prior results, not independently reproduced here. No existing research implementation was edited. Recommendations marked P0 should precede expensive follow-up simulations.

## Demonstrated mathematical correction

Work in units c=1. Let u=ρ/ρ⋆, with ρ⋆>0 and 0<ε≤1, and take

\[
P(\rho)=\epsilon\rho_\star(1-e^{-u}),\qquad
c_s^2=P'(\rho)=\epsilon e^{-u}.
\]

For every positive density this is smooth, has positive subluminal sound speed, P≥0, satisfies the NEC, and has P''<0 and P(0)=0. It also respects the valid concavity inequality c_s²≤w=P/ρ, since eᵘ≥1+u. However, exact homogeneous continuity gives

\[
p_{\rm local}:=\frac{d\ln c_s^2}{d\ln a}
=-3(\rho+P)\frac{d\ln c_s^2}{d\rho}
=3(1+w)u.
\]

At u=2 and ε=10⁻⁶, w≈4.3233×10⁻⁷, c_s²≈1.3534×10⁻⁷, and p_local≈6.000002594. Thus neither p_local<3 nor p_local<3(1+w) follows from the stated hypotheses. The inequality c_s²≤w remains true. This **does not** refute a bound requiring a single constant exponent over an entire cosmological history; it refutes the advertised universal local bound and its unrestricted application. This example is not an action-derived MOND construction and has not passed galaxy, CMB, nonlinear-health or strong-coupling gates. No novelty claim is made.

## Recommendations

### 01 — P0: Correct the universal growth-ceiling claim

**Evidence:** [L157](../../L157_soundspeed_growth_realizability.py), lines 92–135; [L158](../../L158_gdm_loophole_verdict.py), lines 409–431. The valid integral concavity argument is followed by a power-law calculation and then a universal conclusion.

**Action / acceptance:** Replace the universal p<3 claim with its precise power-law/dust-background scope. Add the counterexample above as a negative control. Invalidate downstream exclusions that used the stronger claim; preserve restricted-family results. A successful test must distinguish the valid c_s²≤w theorem from the false local-exponent inference.

### 02 — P0: Make the Lean hypothesis boundary explicit

**Evidence:** [Mondlean.lean](../../lean_2026/Mondlean.lean), `barotropic_w_ratio`, `barotropic_cost_increasing`, `density_time_duality`. The first lemma **assumes** p<3; the last assumes the a⁻³ density form. These are conditional algebra certificates, not proofs of those physical premises.

**Action / acceptance:** Correct overbroad theorem comments and add a dependency table listing assumed EOS, background, boundary conditions and positivity. Formalize the concavity inequality separately from the continuity chain rule. Keep the valid algebra lemmas; do not count them as first-principles derivations of p<3 or full-theory closure.

### 03 — P0: Reconcile the L152 CMB result with the L153 action correction

**Evidence:** [L152 verdict](../../L152_RUNNING_CS2_BOLTZMANN_VERDICT.md) uses GR fluid perturbations; [L153a](../../L153a_identity_soundspeed_coupling.py), opening A1–A5, derives a different gravitational response and friction for the proposed constant-c_Y sector.

**Action / acceptance:** Mark the earlier CMB success as **phenomenological-fluid-only** until an action-to-fluid mapping exists. Derive the density, velocity, entropy, anisotropic-stress and metric-source equations together. Supply either term-by-term equivalence with the patched fluid implementation or a new implementation and spectrum comparison. Matching only c_s²(a) is insufficient.

### 04 — P0: Complete the covariant stress and Ward calculation

**Evidence:** L153a A1 computes a canonical stress tensor with a fixed preferred frame; A2 introduces a lapse perturbation. This diagnoses a real response mismatch but is not the complete Hilbert stress of dynamical clock, scalar and metric.

**Action / acceptance:** Vary all three sectors, including the clock equation and its energy exchange. Derive ordinary minimally coupled matter conservation separately. Reassess the reported “1.3×10⁹ EP violation”: distinguish a dark-sector response ratio from an experimentally measured baryonic equivalence-principle parameter. Acceptance requires the full Ward identity and the actual observable, not relabeling the ratio.

### 05 — P0: Freeze one complete action and its physical metric

**Evidence:** [L139](../../L139_cuscuton_transplant_route2_open.py) describes a cuscuton/leaf-MOND baseline plus a distinct χ sector; L153 proposes a repair; [L155](../../L155_disformal_gamma_cure.py) changes the matter metric.

**Action / acceptance:** Publish one versioned action with every function, coefficient, field, matter coupling and boundary prescription. Keep χ distinct from the foliation clock unless a variation proves identification consistent. Derive both weak-field potentials and the baryonic source from this action. Explicitly distinguish μ(y)=1−e⁻ʸ from a ν-kernel fit: they cannot be swapped without inversion. Keep the requested global a₀ and identify the fitted κ=1/2 as input unless independently derived.

### 06 — P0: Count modes in the coupled system, not the frozen scalar

**Evidence:** L139 health checks around lines 180–185 test K_QQ and a scalar gradient coefficient; homogeneous cuscuton algebra does not establish the full constraint structure.

**Action / acceptance:** Compute the complete kinetic Hessian, primary constraints, preservation chain and Poisson-bracket matrix for the frozen action. Separate k=0, k≠0, y=0 and finite-background branches; show ranks rather than entering expected values. Derive tensor, vector and scalar kinetic/gradient eigenvalues after eliminating constraints. Report any genuine propagating clock/matter scalar separately from the two tensor gravitational modes.

### 07 — P0: Derive moving-source PPN without importing singular limits

**Evidence:** L139's shift source vanishes only on a homogeneous scalar background; it acknowledges missing O(v) work and compares AeST/aether expressions across a degenerate c₁₂₃ limit. L155 itself flags α₂ for rederivation.

**Action / acceptance:** Solve the moving-source expansion of the same action and physical metric, including scalar perturbations and boundary matching. Extract measured G_N, β, γ and α₁,₂,₃ from their defining potentials. A vanishing homogeneous gradient is not a preferred-frame bound, and Φ=Ψ on a galactic branch is not the full Solar-System calculation.

### 08 — P1: Derive a covariant repair, not a time-dependent coefficient by hand

**Evidence:** L153a A3 considers a running gradient coefficient; the proposed repair uses C≈K_Q/(2Q).

**Action / acceptance:** Put C(Q), or its explicitly chosen covariant alternative, into the action before variation. Retain C_Q and higher derivative contributions wherever they enter, including nonlinear equations. Solve the background and derive w, c_ad², rest-frame c_s² and gravitational response together. Demonstrate a valid limit to Lorentz-invariant k-essence if claiming that equivalence; equality of one quadratic coefficient alone is not nonlinear equivalence.

### 09 — P1: Replace the restricted exponent scan with an EOS search

**Evidence:** L158 uses the disputed p ceiling as a gate; the counterexample leaves an untested non-power-law class, not a proven viable model.

**Action / acceptance:** Search monotone concave EOS functions satisfying explicit boundary/causality conditions, solving exact continuity instead of imposing ρ∝a⁻³. Apply the same galaxy, cluster and cosmological gates to each function. Report excluded domains and actual survivors; do not assign a percentage reduction of an unparameterized function space. Start with a small falsifiable family before widening it.

### 10 — P1: Repair the normalization comment and asymptotic classification

**Evidence:** [L137](../../L137_aest_dust_stiff_correction.py), line 222, writes 1/K_QQ=2/(P_X+2XP_XX). For K(Q)=P(Q²/2), differentiation gives **K_QQ=P_X+2XP_XX**, with no extra 2 in its reciprocal. This review confirms a comment error, not a demonstrated downstream numerical error. Also K=Q³ gives w=1/2: superquadratic growth alone is not dust.

**Action / acceptance:** Fix the comment, trace consumers before changing any numbers, and classify asymptotic K forms by derived w and ρ(a). Preserve the specific cosh/exp results where supported. Add both chain-rule and cubic negative controls.

### 11 — P1: Separate hydrostatic existence from actual halo formation

**Evidence:** [L153e](../../L153e_verdict_window.py) combines static atmospheres, capture and lensing criteria into a narrow window.

**Action / acceptance:** Evolve one surviving candidate from cosmological initial data with conserved charge and matched exterior conditions. Measure galaxy contamination, cluster capture, oscillations and caustics from that evolution. An exponential equilibrium atmosphere in an assigned potential is not proof that cosmological evolution produces it. First perform one controlled spherical collapse experiment; reserve expensive 3D work for a survivor.

### 12 — P1: State the approximation behind density-time and climb identities

**Evidence:** L157 lines 80–86 and 140–149 call the a⁻³ dictionary and Newtonian hydrostatic climb relation exact, despite nonzero w.

**Action / acceptance:** Keep exact continuity dlnρ=−3(1+w)dln a. Specify whether the hydrostatic denominator is ρ (Newtonian approximation) or ρ+P (relativistic enthalpy); derive the chosen static equation and its metric-potential convention consistently. Quantify errors over the scanned densities. Do not simply add a factor to the final climb formula: relativistic enthalpy can cancel that factor when derived consistently.

### 13 — P1: Bound the scope of the disformal no-go

**Evidence:** L155 derives a lensing cure within a specified A(φ), B(φ), EH tensor-cone ansatz and estimates a photon/tensor-cone mismatch from a scalar potential.

**Action / acceptance:** Preserve that restricted obstruction, but state its assumptions when claiming uniqueness or exclusion. Fix the scalar zero point through physical boundary data and compute observable travel-time differences along matched photon/graviton paths. Re-derive tensor characteristics if the gravitational action changes. Do not extend this calculation to every single-metric or modified-tensor-sector construction.

### 14 — P1: Distinguish likelihood results from diagnostic significance

**Evidence:** [L152 CMB code](../../L152_running_cs2_cmb_boltzmann.py) uses a fixed-parameter Gaussian spectral/lensing surrogate; [L165](../../L165_smooth_dust_third_peak_calibrated_sigma.py) calibrates a third-peak statistic. The latter explicitly tests GR perturbations with smooth dust, not arbitrary modified gravity.

**Action / acceptance:** Label Δχ², 1% thresholds and “sigma” by the actual statistic used. For an observational exclusion, profile/marginalize relevant cosmological and nuisance parameters with an appropriate covariance or likelihood. Keep the useful independent CAMB/CLASS code check, but do not promote a smooth-GR-dust failure into a universal gravity theorem.

### 15 — P1: Verify the zero-particle-CDM limit

**Evidence:** L152 retains omega_cdm=0.001 alongside the replacement fluid. A small residual used as a synchronous-gauge anchor is not yet the requested particle-free model.

**Action / acceptance:** Document its role, decrease it systematically, and compare to a gauge/implementation that supports zero CDM. Show convergence of gauge-invariant observables and the background density budget. If a nonzero particle component remains physically necessary, mark that explicit requirement failed rather than rounding it away.

### 16 — P1: Derive running-fluid initial conditions and convergence

**Evidence:** The [CLASS patch](../../L152_class_running_cs2/running_cs2.patch) replaces constant sound-speed values in evolution and initial-condition code; L152 includes valuable stock-code and recombination controls.

**Action / acceptance:** Derive the initial series for the chosen time dependence, or demonstrate convergence as the start time is moved earlier. Vary precision, integration start, k/l ranges and recombination treatment on actual surviving models. Include background energy conservation and low-l/late-time response tests; a small recombination sound speed alone does not establish the full action mapping.

### 17 — P1: Make reconstructed matter power gauge-safe and numerically stable

**Evidence:** [L152 power code](../../L152_running_cs2_pk_lyman_alpha.py), `pk_and_transfers`, combines synchronous component transfers with CLASS's comoving matter transfer through a squared ratio; background weights use a nearest-redshift row.

**Action / acceptance:** Derive an explicitly gauge-consistent total-density transfer and compute its spectrum directly, avoiding unstable division near transfer zeros. Interpolate background weights consistently. Check gauges, k bounds and σ₈ integration convergence on the new fluid as well as controls. Label b+residual-CDM power accurately rather than calling it pure baryon power.

### 18 — P1: Treat Lyman-alpha comparisons as provisional until flux is modeled

**Evidence:** L152 power comparisons use linear matter/baryon suppression against a thermal-WDM proxy, while some target scales are nonlinear.

**Action / acceptance:** Do not select whichever transfer field gives a passing bound. Derive the gas-plus-field response and ultimately the transmitted-flux observable, including thermal/ionization history and nuisance uncertainty. Until then retain the proxy as an explicitly conditional screen, with both total and baryonic spectra shown. Only a candidate surviving the action mapping merits an expensive hydrodynamic likelihood campaign.

### 19 — P2: Make the CLASS patch/build independently reproducible

**Evidence:** [patch applicator](../../L152_class_running_cs2/apply_running_cs2_patch.py) edits sequentially; [build script](../../L152_class_running_cs2/build_patched_classy.sh) reuses an existing source directory. A partial or stale patch/build is possible without a clean provenance check.

**Action / acceptance:** Pin upstream and patch hashes, validate all replacements before any write, build in a fresh scoped directory, and record compiler, interpreter and imported binary hashes. Use interpreter-matched package commands. Validate a_star, cap, sign and finite range of c_s² parameters; specify the p=0 cap behavior. Acceptance includes a clean build and stock p=0 regression from the recorded inputs.

### 20 — P2: Make the research verdict ledger fail closed

**Evidence:** L139 has eight literal-True `check` calls; L158 records some skipped optional validations with `check(..., True, ...)`. Some calls are honest status annotations, but counting them as tests exaggerates executable coverage.

**Action / acceptance:** Separate PASS, FAIL, SKIP, ASSUMPTION and OPEN. Store exact commands, exits, input/source hashes, imported binaries and claim dependencies. A changed premise such as L153's response equation must mark the inherited L152 theory verdict stale while preserving its fluid calculation. Register predictions with action version and fitted inputs before comparing to new data. Count certificates by what they establish, never by exit-zero totals alone.

## Efficient execution order

First correct scope and evidence bookkeeping (01–04, 20). Freeze the repaired action and run the coupled perturbation/constraint bottleneck (05–08). Only after it survives should the team spend on nonlinear formation, full likelihoods or expanded parameter scans. The barotropic counterexample reopens a mathematical possibility; it does not award a completed theory or a viable empirical model.

## Reproduction

From the repository root:

```sh
python3 -B fable_independent_2026/reviews/2026-09-10_twenty_recommendations/check_review_algebra.py
git diff --check
```

The companion output records the executed algebra check. Exact algebra and the explicit counterexample establish the stated local-ceiling correction; bounded numerical output does not establish a universal theory. No claim of new empirical discovery, full Lean certification or completed relativistic MOND is made here.
