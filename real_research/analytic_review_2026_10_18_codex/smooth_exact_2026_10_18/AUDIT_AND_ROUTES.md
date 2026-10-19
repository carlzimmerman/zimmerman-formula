# Audit and research routes for the exact smooth halo

18 October 2026. Checkpoint ZAR-2026-10-18-04; parent ZAR-2026-10-18-03. The target is a bounded smooth nonnegative invariant DF for each population with the exact prescribed densities, positive radial dispersion, unchanged law annulus and finite boundaries, and a radial stability theorem in the same spherical effective model.

## Claim cards and dependencies

ZAR-S1 asserts existence for the specific fixed exponentially tapered hollow profile, any fixed fraction 0 < f < 1 satisfying the parent's sufficient core condition, positive point baryon mass and controlled deep-cubic regime. Each sufficiently small fixed positive width yields smooth bounded distributions of compact support, exact density, strict physical energy decrease on occupied states, and positive radial dispersion on the law annulus. It does not assert a uniform cold-limit bound or inversion for an arbitrary flat profile.

The proof dependencies are the positive closed-interval lower bound for L_c', the exact phase-volume Jacobian, uniform orbital geometry, the local Fourier mode estimate, the two weighted operator bounds, fixed-space Neumann inversion and derivative bootstrap, two positivity estimates, and exponential endpoint extension. All are derived internally or pinned to the parent analytic proof. No experimental result or imported kinetic theorem is a load-bearing leaf.

ZAR-S2 applies the unchanged reciprocal-field quadratic to S1, with the same background gap and mass-map estimates. Smooth compact support supplies finite total weight and susceptibility, identifies energy perturbations as ordinary L1 functions, and allows classical radial characteristic evolution for smooth accessible data. Its conserved bound is in the weighted energy norm, with L1 control from that norm. It is not an estimate from the initial L1 norm alone or a uniform Ck bound.

## Executed routes

| Route | Central move and decisive check | Outcome and disposition |
|---|---|---|
| SR1: improve exact orbit-density inversion | Use width depending on Fourier frequency, then prove the mode error is O(sqrt(b_n)) with one derivative of smoothing | Selected route. The explicit weighted right inverse, positivity and endpoint arguments prove S1 for the exact old profile |
| SR2: direct augmented-density DF | Use L^2 g(E_cut-E), positive Abel inversion and core/edge shooting | An unaudited restricted-family candidate was developed, but it changes the core/taper and fraction outside the annulus. Deferred as unnecessary for the user's stronger exact-profile target; no claim from it is needed for S1 or S2 |
| SR3: seek a smooth-boundary obstruction | Derive confined-orbit constraints and a bounded smooth tracer DF in the old potentials | No general no-go found. Flat boundaries and monotonicity alone do not force a ridge. Restricted curvature and cooling constraints survive; exact self-consistency was not established by the tracer route |

SR1's first uncertain implication was the global weighted inverse, not local normalization. The critical mode estimate now explicitly includes all intrinsic derivatives and a uniform support collar. Row/column Fourier sums give an O(delta) X_s error and an X_s to X_(s+1) gain. This establishes smoothness from inversion at one fixed Sobolev order, without assuming convergence in all orders at once.

## Why the former residual construction cannot be used unchanged

The old optional geometric widths epsilon_n <= epsilon_star 2^(-n), combined with q_n <= (3/4)u_(n-1), actually force a ridge. At any fixed interior circular center s, eventually theta_n(s) = 1 and

\[
u_{n-1}(s)\geq4^{-(n-1)}u_0(s),\quad
g_n(s)=\tfrac12u_{n-1}(s),\quad
N_{\epsilon_n}(s)\leq C_s\epsilon_n^2.
\]

Hence each eventual circular value F_n(E_c(L_c(s)),L_c(s)) is bounded below by a fixed positive constant. Their sum diverges. Continuity of finite partial sums makes the total essentially unbounded in neighborhoods of that ridge, not just at a phase-null point. This does not invalidate the old L1 construction or its energy-form stability; it prevents claiming smoothness from those particular width/residual bounds.

The new proof allows signed corrections underneath a larger positive component. The final DF is nonnegative, but its density correction is not required to be a positive residual series. That change removes the amplitude-versus-width obstruction.

## Review provenance

- `smooth_packet_route` developed the inverse construction and its uniform mode estimate. The primary agent independently reconstructed the exact Jacobian, Fourier matrix bounds, smoothing bootstrap, positivity and physical endpoint extension before writing the proof.
- `smooth_inverse_audit` independently rederived the local mode lemma, Schur estimates and endpoint geometry from raw formulas; it then read the actual proof and found no missing implication under the explicit target hypotheses.
- `smooth_proof_fresh_audit` received the actual proof with no prior verdict and independently reconstructed the density Jacobian, inverse estimate, positivity, confinement and endpoint extension.
- `smooth_positive_audit` separately checked positivity, derivative convergence, the point-mass nondegeneracy requirement and the distinction between weighted/L1 control and uniform Ck stability; it also reviewed the written classical-flow note.

These are internal analytic checks. Agent agreement is not a proof certificate, external peer review or experimental evidence. Exact reviewed revisions and any subsequent local clarifications are recorded in [CHECKPOINT.json](CHECKPOINT.json). The proofs themselves, rather than review votes, carry the claims.

## Scope after this checkpoint

The previously named smoothness and exact-density obligations are closed by S1 within the fixed model. S2 removes the need to interpret the accessible linear perturbation merely as a distribution at a circular ridge. Its classically smooth initial-data statement has the same restricted radial symmetry and angular-momentum-preserving accessibility as the quadratic.

Amplitude, population fraction, dimensions, temperature width and the core/taper profile remain selected inputs. The construction does not derive formation, exchange between populations, full interpolation, finite stiffness, a covariant action, nonlinear stability or nonspherical stability. It is not a raw-data test or a new fit to observations. Those remain separate research programs.

There is no remaining named implication in the present exact smooth-density target. An independent nonlinear radial extension would first need a nonlinear perturbation class and control of higher energy variations by the positive quadratic; that work is deferred until requested. SR2 can be resumed if a distinct regular-core family is desired, beginning with an independent audit of its core shooting and outer moment matching. SR3's tracer construction needs no continuation for this target, since SR1 supplies the missing exact self-consistency directly.

Only this new checkpoint directory was written. All prior checkpoint artifacts were hash-checked rather than edited. No scientific scripts, array analysis, numerical integration, simulations, statistics, or process inspection/control were used, and Claude's calculations require no action.
