# Approved bounded continuation: conserved-charge redistribution

Base: `738773278` on the live shared main checkout, 2026-09-12. The user accepted the preceding three-step proposal: construct spatially varying data of the unchanged action, test stability, and evolve only after those prerequisites pass. This extends the repository's existing constraint/current/principal implementations; it introduces no new model architecture.

Target: one regular inhomogeneous configuration retaining the inherited scalar shift charge, with comoving ordinary matter and aligned clock, satisfying Einstein's Hamiltonian/momentum and the clock constraint, with a viable scalar-metric characteristic structure. Full gravity closure would additionally require all previously named MOND, lensing, cosmology, PPN, tensor, conservation and nonlinear degree-count gates. This work cannot claim those from an initial slice.

Three independent routes:

- `constraints/`, owner fixed_action_escape: derive and solve a full-cubic plane-symmetric initial constraint system with spatial scalar gradient; retain the clock constraint and test its preservation/lapse equation. Failure of a profile or finite boundary problem is not a no-go for all profiles.
- `current/`, owner c003_orbits: derive the exact conserved covariant current and spherical flux/charge relation, keeping explicit clock-time coefficient dependence. A static metric is not assumed to mean stationary charge. Zero-flux branches must use the actual constitutive dependence.
- `exterior/`, owner closure_checkpoint_review: independently calculate the unchanged sourced exterior's full-cubic principal coefficients, including background Hessian, and compare against the actual constrained transfer operator. Test whether a localized repair can share those asymptotics.

The main agent owns root-level files and Lean formalization. Each child has a disjoint new directory and cannot commit. Scientific runs are bounded individually and pinned to their actual source inputs. Old outputs, coefficient functions and other agents' files are preserved.

Decisive gate: evolution toward galaxy dust depletion requires a stable configuration and exterior. If the specified exterior has a strictly negative scalar discriminant and the full principal coefficients converge to it, a healthy localized completion is excluded irrespective of the interior profile. The exact asymptotic implication and finite numerical evidence are reported separately. This does not exclude a different asymptotic branch or supply one.

No new coefficient reconstruction, local a0 prescription, particle dark matter, observational fitting, publication, or universal novelty claim is part of this continuation.

Concurrent update: Claude committed `9212f4498` (L194 tracking dynamics) while the three routes ran. The common action-source hashes did not change. A fourth bounded route, `tracking/` owned by closure_checkpoint_review after finishing its earlier work, reproduces the original pure tracking functions without overwriting their results, checks the signed equilibrium, introduces one shorter mode, and stress-tests the discarded expansion terms. The parent formalizes the resulting conditional algebra in `TrackingBalance.lean`. A proposed globally altered statistical exterior is outside the localized-asymptotic obstruction; it is tested as an unproved moment-closure proposal, not silently counted as either an action-derived cure or a globally excluded theory.
