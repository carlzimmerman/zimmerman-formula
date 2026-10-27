# FR-20261022 self-audit

Primary verdict for the requested joint mass-selection claim: **incomplete, with the smallest missing implication** being a converged, persistent, bound material partition and its population distribution. The finite runs do not produce that implication.

Scope: arbitrary3D particle positions, nonlinear three-component P, nonlinear χ and finite field inertia in the passive X=0 sector. This is a substantial extension over affine widths. It is still not live-baryon cosmology or a covariant parent theory. No independent reviewer or subagent was used.

Dependency review:
- Hamiltonian -> TSC deposition derivative -> reciprocal particle force: verified by finite differences, not independently interpolated.
- Hamiltonian -> P/χ acceleration: verified by separate directional energy derivatives.
- Discrete adjoint gradient/divergence -> local signed field current: independently verified at fixed density.
- Field-only sponge -> exact kinetic-energy loss: accounted separately; no material mass removal/damping.
- Static field preparation -> negligible frozen-source export: tested through the full matched interval.
- Spatial particle sampling -> connectivity groups: no theorem connects a short FoF link to a bound core. Frozen initial material produces spurious-looking groups, an explicit detector control.
- Candidate escape energy -> actual asymptotic ejection: unresolved in time-dependent fields. Report only the declared far-outward Newtonian diagnostic.
- Absorbed energy -> permanently outgoing radiation at infinity: conditional on finite domain and tails. The phase-current box repeat fails; positive absorption is not a complete asymptotic radiation calculation.
- Retained mass -> absence of any possible mass selector: invalid implication, not asserted. Results are restricted to the actual initial conditions, couplings and times.
- Unchanged homogeneous linear kernel -> cosmological growth preservation: invalid without population/background stress accounting, not asserted.

Critical numerical caveats:
1. The lattice breaks continuous rotational/translational invariance. Material angular momentum can also exchange with the fields. Canonical field orbital and intrinsic contributions, plus sponge removal, were added in a trajectory-identical instrumented repeat. Its total discrepancy reaches0.99%; do not label matter-L alone a numerical error or claim exact total-J conservation.
2. Periodic gravity has an arbitrary isolated-energy offset. Reported loss fractions use the magnitude of initial **finite-box total energy**, not a precision isolated astrophysical binding energy. Absolute absorption comparisons are kept separate from those fractions.
3. Particle-mesh self-energy and discreteness require both particle and grid repeats. The profile-CDF gate fails on spatial refinement despite tiny Hamiltonian drift.
4. The sponge starts outside the control region but occupies a finite fraction of the periodic box. Its damping profile changes with box size by the declared formula. The domain repeat consequently tests the combined boundary/absorber setup, not just one isolated error source.
5. The long quiet/perturbed tests have no long-time fine-grid repeat. Their similarity is useful initial-condition evidence, not long-time continuum convergence.
6. Zero ejecta candidates in a finite interval is not a proof of permanent binding. Conversely, isolated short-link particle groups are not automatically ejecta or bound cores.
7. Three mass points with different dynamics do not verify an M⁴ law. The quartic phase-flux scaling is conditional on the same prescribed weak source history. The empirical233-fold export comparison is reported only as a finite observation.
8. Similar radii at18t0 are a snapshot coincidence: last-third ranges/means differ. No radius attractor is claimed.
9. Non-affine kinetic energy is not automatically thermalized random motion; no temperature or pressure closure is inferred from that decomposition.

Validation and interpretation: all preliminary energy/force/current tests pass. The postcheck distinguishes ordinary finite checks from interpretation gates; spatial CDF and phase-current domain precision fail their stated thresholds. Mass selection and observational-preservation gates are false because they are not established, rather than being direct counterexamples to the full theory.

Proofreading self-review covers DERIVATION.md, RESULT.md, GATES.md and HANDOFF.md: signs, dimensions, finite-box energy wording, mass-versus-energy conservation, time units and detector labels checked. No inherited papers or manuscripts were edited. Base revision f1803b025624a5bf494d76cb13308431128f2634; per-run manifests pin observed versions, inputs and outputs. No initialized .mathbox ledger or external publication.

Final verification: all12bounded manifests validate with current hashes and completed status. Ordinary checks31/31pass. Interpretation gates7/11pass: spatial CDF precision and phase-current domain precision fail; selected bound mass partition and joint observational preservation remain unestablished. All execution sessions completed.
