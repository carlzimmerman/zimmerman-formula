# PF06 continuation handoff

Live entry: README.md and coupled/STATUS.md, 2026-11-06.
Owner: current Codex chat; write scope ac2q_postfold_2026_11_06 only.
User authorized finding whether AC2q's own coupled fields avoid breaking or
supply missing interface stress; no scientific closure has been declared.

## Completed bounded obligations

PF01–03: exact breaking in the PN principal system; incompatible finite shock
laws; exact flat stationary-profile corner obstruction; frozen flat symbol.
These do not prove full-action breakdown. Existing AC10 threshold J=1e-3 and
its pressure-dropping continuation do not close that gap.

PF04: four-dimensional plane reduction and regular coupled metric junction
identities. Native metric derivatives cannot jump independently while their
conjugate fluxes and P remain continuous. The PF02 obstruction extends to
stationary metric/polarization profiles, phi=s t+psi, gamma>0, regular timelike
same-sign through-flow and gamma*s_local^2<1/3. A stationary surface with evolving
fields is NOT covered. See coupled/JUNCTION_RESULT.md and its independent review.

PF05: bounded quasi-stationary negative-divergence sheets cannot carry the
missing stress if limiting on-branch endpoints have a uniform positive flux
gap, the clock and metric remain nondegenerate, and temporal derivatives/sources
are uniformly bounded. Rapid temporal layers remain open. Plane tensor modes
are unsourced from zero data while coefficients stay regular.

PF06: ADM constraints/evolution derived and independently reviewed; exact
constraint-compatible initial family constructed; homogeneous and local linear
benchmarks executed. The coupled homogeneous principal block remains wave-like,
not a k^4 regulator. See coupled/ADM_FORMULATION.md and REVIEW_SOLVER.md.

## Unresolved routes and failed computational attempts

N1 full nonlinear evolution: longer canonical-variable runs do not converge to
a resolved endpoint. Centered derivatives, odd grids, smaller timesteps,
momentum reconstruction and a joint lapse/polarization solve were tested.
The last solve exhibits a constraint tolerance/roundoff problem even in its
homogeneous benchmark. These failures are numerical, not full-action breaking
or avoidance. Preserve failed runs. Do not run this solver postfold or use its
stopping time as an observable. Next: a nonlinear formulation adapted to the
constraint surface, tested against the independently derived lapse/metric
linear system; then space/time refinement before any physical classification.

N2 native layer stress: derive a truly time-dependent layer balance without
setting P_t+2P beta_t=0. Determine whether a finite defect stress exists, remains
within the action's domain, and is uniquely selected by incoming data. Neither
arbitrary stress assignment nor an unproved finite-action coercivity claim is
acceptable. Unbounded metric gradients and oscillatory limits remain open.

E1 extension: if N1 establishes breaking and N2 cannot select a native carrier,
specify a covariant carrier/operator and its energy budget. No particular new
parameter or operator has been adopted. A completion of ordinary shocks is
needed in the excluded class; a universal necessity of extra physics is not
proved. Phenomenology and calibration must be retested only after such a model
is actually specified.

A general source-driven shock theorem cannot discharge N1 until strict
hyperbolicity, genuine nonlinearity, locality and constrained-data compatibility
are established for this action. See the source boundary in coupled/STATUS.md.

## Provenance and review

PF01–03 criteria: 57f9b8140d,21cb54b10b,bdaee092bf; results59cbc01d7c.
PF04–06 criteria: f53b83d55a,4ccb8aceac,91cb3d3e3e,9b5b2fd660,17f8759991.
Thirty recorded manifests validate against current inputs; failed outputs and
mutation controls are retained. Independent linear benchmark uses a separate
contract/command/result under coupled/review_linear. Check coupled/VERIFICATION.json.
Independent reviewer checked the canonical system and junction proof, and
identified stationary-profile and uniform-gap restrictions now made explicit.
No unrelated files were edited. No background computation remains running.

Definition of done: justified full-action survival, uniquely specified completion,
or failure classification with controlled incoming data and outgoing observables.
This checkpoint does not meet that definition; the routes above remain open.
