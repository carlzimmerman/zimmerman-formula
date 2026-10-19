# Audit and handoff for nonlinear radial stability

19 October 2026. Checkpoint ZAR-2026-10-19-05; parent ZAR-2026-10-18-04. The stationary halo and all previous artifacts remain unchanged. The target was nonlinear radial stability and a precise assessment of law, dispersion and all-time confinement under small perturbations.

## Result and claim dependencies

| Claim | Conclusion | Evidence and dependency |
|---|---|---|
| ZAR-N1 | A genuine nonlinear local energy minimum on the full fixed-L submajorization hull, including nonsmooth finite-kinetic-energy weak limits | [NONLINEAR_COERCIVITY.md](NONLINEAR_COERCIVITY.md); uses the old smooth halo and radial quadratic |
| ZAR-N2 | Nonlinear Lyapunov stability in weighted L1 including kinetic moments, for general nearby radial data with fixed positive angular gap and uniform height bound | [NONLINEAR_FLOW.md](NONLINEAR_FLOW.md); N1 plus conserved entropy, compactness and a first-exit argument |
| ZAR-N3 | Global classical radial flow, uniform positive inner radius and particle-speed bounds, compact spatial support at every finite time | [NONLINEAR_FLOW.md](NONLINEAR_FLOW.md); characteristic comparisons and preserved masses, heights and angular momenta |
| ZAR-N4 | Uniformly close cumulative-mass/force law and integrated raw/centered radial pressure; qualitative pointwise warmth for connected positive-support data | [LAW_DISPERSION_BOUNDARY.md](LAW_DISPERSION_BOUNDARY.md); N2 and N3 |
| ZAR-N5 | A uniformly bounded outer support for the open small-DF perturbation class is false, even with identical initial density, centered dispersion and initial R | [LAW_DISPERSION_BOUNDARY.md](LAW_DISPERSION_BOUNDARY.md); explicit canonical outer-layer boost and exact escape comparison |

The requested nonlinear theorem is established in the stated perturbation class. The added demand that every perturbed particle remain inside one finite outer radius for all time is refuted in that same class. Uniform bulk-mass confinement survives. These are different quantified statements, not interchangeable notions of halo boundedness.

The new nonlinear class is broader than exact dynamic accessibility: initial Casimirs may differ from those of F. The material restrictions are smooth compact radial data, one fixed L interval with positive lower endpoint, a prescribed height bound, and sufficient initial smallness in X. The modulus is existential; no explicit universal tolerance or rate is claimed.

## Executed routes

NL1, inverse entropy and normalized nonlinear tangents, is the selected proof. Its initially uncertain implication was whether weak normalized secants are accessible despite flat cutoffs. Convex duality proves their finite weighted norm, all height Casimirs give zero orbit average, and periodic primitives prove membership in the old accessible closure. Actual mass compactness, including the origin and infinity, then controls the exact cubic remainder. This establishes a nonlinear minimum on a weakly closed hull, precisely the domain needed by the nearby-leaf first-exit proof.

The naive global entropy Taylor route is closed. Near a fixed interior L's upper energy edge, where the correction vanishes, F = A exp[-b/(E_cap-E)]. Its inverse entropy has Psi_ss(s) = b/[s log(A/s)^2], which diverges as s tends to zero. A uniform third-order height expansion is unavailable. The proof uses a local expansion of the convex dual only away from the degenerate sets and then exhaustion; it does not assume the missing global regularity.

NL2, a reduced attractive-field functional after splitting off the convex tether energy, identified a useful saddle/Schur-complement structure. A naive unconstrained two-field minimum is not justified. An infimum/compactness continuation was developed, but the direct hull argument in NL1 removes that additional layer entirely. No nearby minimizer or C2 implicit-function theorem from this route is a proof leaf. The alternative is deferred; it can be resumed if a different model requires a field-only formulation or a quantitative stability modulus.

NL3, characteristic confinement and falsification, supplied the global flow bounds and the sharp escape counterexample. The outer-layer boost is a single escaping solution for each fixed perturbation, rather than merely a sequence of initially large support radii. The escape packet has positive mass for every chosen perturbation, while that mass tends to zero with the outer layer. Exact boundary preservation is therefore ruled out without changing the equilibrium theory.

## Review record

- `nonlinear_tangent_audit`: fresh analytic reconstruction and actual N1 artifact review. Passed the convex-dual bound, Casimir tangency, periodic-primitive closure, true mass compactness and singular cubic remainder on the full measurable finite-kinetic-energy hull. Its wording correction distinguishes generated perturbations from their generators.
- `nonlinear_full_flow_audit`: independently checked the raw argument and actual N2/N3 artifact. Its verdict is conditional on named input N1, which the separate audit establishes. No further implication was missing. It verified the stronger time-uniform centrifugal and speed comparisons, height-entropy extension, general nearby-Casimir weak limits and first-exit contradiction.
- `nonlinear_observable_audit`: independently checked the actual observable estimates and explicit counterexamples, conditional on N2/N3. It confirmed the positive-mass escaping packet, smallness in every fixed Ck norm, centered-pressure estimate, genuine-canonical connectedness condition and finite-time versus all-time quantifiers. Final cutoff-scaling and mass-label clarifications were confirmed.
- The primary agent independently reconstructed the entropy/hull mechanism, full nearby-leaf proof, global characteristic bounds and escape construction before integration. The final proofreading pass concerns only this checkpoint's new documents.

These are internal mathematical reviews, not external peer review, experimental evidence or a proof certificate based on voting. The displayed derivations carry the results. Exact input, artifact and reviewed revision hashes are pinned in [CHECKPOINT.json](CHECKPOINT.json). Post-review changes are limited to the recorded forced wording and quantifier clarifications.

## Source and scope

[SOURCE_CHECK.md](SOURCE_CHECK.md) records the checked adjacent Newtonian theorem of Lemou, Mehats and Raphael. Direct application to this two-force point-baryon cubic model is inapplicable; no external nonlinear Vlasov theorem is silently imported. The new bridge is derived in the present proofs. No global novelty assertion is made.

The equilibrium remains exactly the original bounded smooth density, law annulus, radial temperature family and finite boundary. For disturbed solutions, the mass law and force remain close, centered pressure is controlled in integral norm, and genuine smooth canonical perturbations retain positive annulus dispersion at each finite time. Exact law equality and the old hard edge are not invariants. Pointwise density or an all-time dispersion floor is not controlled by the energy neighborhood.

The narrower outer-confinement question with an imposed uniform negative initial particle-energy gap remains open here: the escape boost is excluded by that extra condition, but individual energy is not conserved in the changing self-consistent potential. A gap maintained at all later times would suffice for confinement; proving its propagation is the first unresolved implication in that separate route. Smallness of the phase-space distribution does not itself impose such a support gap.

Nonspherical dynamics, low-angular-momentum point-mass collisions, a covariant/full-interpolation completion, formation and parameter or temperature selection remain outside this theorem. No new observational validation was attempted.

Only this new checkpoint directory was written. Source reads, small hashes and document validation were the only executable work. No scientific scripts, numerical integrations, simulations, statistics, array analysis or process inspection/control were performed. Claude's jobs and all prior research artifacts were left untouched.
