# Audit and continuation of the warm finite halo

18 October 2026. Checkpoint ZAR-2026-10-18-03; parent ZAR-2026-10-18-02. This is an analytic continuation of the same effective spherical kinetic model, not an observational validation or a replacement of the repository's computational campaigns.

## Contract and assumptions

The user requested finite radial dispersion for the finite circular halo, preserving its law and boundary, with an analytic stability assessment and no interference with Claude's calculations. Only this checkpoint directory was written. Existing research files, code, inputs and results were not changed. No scientific scripts, simulations, integrations, array analysis, statistics or process inspection/control were performed. Small text reads, document checks and hashes are bookkeeping, not physical computation.

The model retains positive point baryon mass M_b, a_0 > 0, the deep cubic response, zero added stiffness, separate conserved tethered and free populations, and a common gravitational mass per particle. Only the tethered population carries the additional response charge. The exact input profile is the parent checkpoint's smooth hollow M, with M <= A r, A = sqrt(a_0 M_b/G), an interior M = A r annulus and a smooth finite outer taper. The selected fraction satisfies 0 < f < 1, and the sufficient core condition is r_0 > 2 f^2 r_M/(1-f), with r_M = M_b/A. The controlled deep-regime choice from the parent must also be retained.

Any fixed fraction strictly between zero and one is allowed by choosing the core appropriately; this is not only an infinitesimal tether result. The sufficient condition degenerates as f approaches one. The positive gap uses M_b > 0 and finite R. This proof does not cover their degenerate limits.

## Claims and evidence

| Claim | Exact statement | Evidence and status |
|---|---|---|
| ZAR-W1 | The exact target densities admit nonnegative ordinary L1 invariant distributions, no delta component, with strictly positive radial dispersion on the closed law annulus, finite mass and energy, and all occupied orbits inside the original finite hollow support | [EXACT_WARM_DF.md](EXACT_WARM_DF.md), analytic construction and independent artifact audit passed |
| ZAR-W1a | Radial pressure is C1 in the interior, vanishes at both density edges, and has no boundary stress layer | Packet Jeans identities and uniform residual-density tail bounds; independent artifact audit passed |
| ZAR-W2 | Dynamically accessible spherical radial perturbations of the same warm equilibrium have a coercive conserved quadratic and a unique global linear flow in H_DA, with a uniform energy-norm bound | [ACCESSIBLE_STABILITY.md](ACCESSIBLE_STABILITY.md), exact warm identity and functional-analytic construction; independent artifact audit passed |
| ZAR-W3 | The force/circular-speed law and exterior matching are exactly preserved; dark velocity moments obey the stated pressure-gradient correction | Exact density, unchanged force functional and radial Jeans identity; independently checked |

W1 is an existence proof using a positive countable family of eccentric orbit packets. The uniform row-kernel limit, not merely normalization over radius, is what allows exact density recovery while keeping every residual positive. It is not a numerical orbit-superposition fit.

W2 does not assume a finite susceptibility or infer warm stability from the circular shell result. Its key identity cancels the potentially negative self-density terms against the actual reciprocal field Hessian, leaving positive orbital terms and a positive relative-population square. The resulting bound is controlled by the fixed background coefficients; no spectral-continuity assumption in temperature is used.

The H_DA completion uses common canonical generators for the packets of each physical species. Packet labels do not introduce new matter or independent response laws. Its aggregate perturbations extend continuously as distributions. The mass and current maps are bounded before invoking the conserved quadratic, avoiding circular reasoning in the flow construction.

## Independent review record

Separate agents developed the density-packet route, the warm stability identity and the boundary/regularity objections. Two further artifact reviews checked the actual written proofs.

- `warm_packet_review`: audited the kernel row asymptotics, residual positivity, exact density, mass, finite support, radial-pressure lower bound, weak stationarity and ridge qualification. Final verdict: W1 proved as written, no load-bearing gap found. Its requested explicit cutoff bounds were incorporated. It also checked the final Jeans and C1 pressure additions.
- `warm_flow_review`: audited the signs, field cancellation, coercivity, invariant dense core, bounded mass/current maps, field-source closure, mild-flow construction, interaction-picture norm derivative and distributional aggregate. The review requested that zero-density quotients be a support convention rather than an assumed boundary limit, and that the aggregate source be explicitly written as a velocity derivative of an integrable flux; both corrections were incorporated.
- Primary-agent review: checked consistency with the parent force functional, preserved-versus-unprescribed quantities, the finite exterior, and the distinction between equilibrium regularity and perturbation regularity. Proofreading checked notation, display delimiters, local links and claim scope.

These are internal analytic reviews, not external peer review or a substitute for experimental evidence. The artifact re-reviews were informed by the earlier derivation, rather than blind proof audits. Exact artifact hashes and review revisions are recorded in [CHECKPOINT.json](CHECKPOINT.json).

## Bounded literature context

The abstract of Perez and Aly, *Stability of spherical stellar systems I: Analytical results*, describes a symplectic method for spherical collisionless systems with an external potential and a distribution decreasing in energy. This is a methodological antecedent, not a theorem imported into the present two-response model. Its abstract alone does not resolve our ridge regularity. [Primary source, arXiv:astro-ph/9511103v1](https://arxiv.org/abs/astro-ph/9511103v1).

This limited source check establishes neither global novelty nor absence of a smoother construction elsewhere. The modified-force identity and countable construction above are proved directly. The failed journal fetch for an adjacent finite-extent model was not used as evidence.

## Remaining mathematical and physical obligations

The equilibrium is smooth at accessible eccentric points and integrable overall. It can be unbounded near E = E_c(L). A phase-null ridge does not remove its possible effect on differentiability: the aggregate canonical tangent need not lie in ordinary L1 and the susceptibility can diverge. The H_DA result therefore must retain its stated topology.

The first stronger analytic target is a bounded smooth distribution across that ridge with the same exact profile, positive radial dispersion and an appropriate classical linear flow. A useful route would be a positive orbit-density inverse with quantitative width-versus-residual control. Simply broadening the circular delta or truncating the positive packet series loses exact self-consistency; neither is a proof of that target.

Simultaneous prescription of a nonzero radial-temperature profile is another moment problem. On the r^-2 law annulus, <v_perp^2> = v_c^2 + r d(sigma_r^2)/dr. Constant sigma_r would remove this correction, but no such profile is selected here. A bounded upper width and a positive annulus-wide lower width do not specify a measured temperature.

Nonlinear orbital stability, perturbations that change angular momentum through nonspherical fields, the full interpolating response, finite stiffness, a covariant action, formation, exchange between populations and parameter selection remain open. The amplitude A, fraction f, radii and packet widths remain inputs. No new comparison with raw observations or experiment-count claim was made.

## Handoff

Continue from W1 and W2 with their exact hypotheses. Preserve the distinction between an ordinary finite-mass equilibrium, a generalized accessible linear flow and a classical nonlinear kinetic solution. Keep further work analytic unless the user changes the resource boundary. Claude's computations require no action from this checkpoint.
